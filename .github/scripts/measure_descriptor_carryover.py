#!/usr/bin/env python3
"""measure_descriptor_carryover.py — 前版の記述子が引く条のうち、新版で本文が変わった条を列挙する。

**なぜ在るか。** 機械可読記述子 (`ACD-<版>.machine.json`) は版ごとに作り、各事実が引く条
(`clause`) を持つ。新しい版の記述子は前版を下敷きに作るが、**引いている条の文言が変わっていれば、
その事実を述べ直す必要がある** —— 番号が同じでも内容が変わった条をそのまま持ち越すと、記述子が
条文と食い違う (Check 451d は条の**存在**しか見ない)。2026-11-01 に 1.3 → 1.4 を手で当て、10 条中
4 条 (§4.2 / §4.3 / §8.1 / §8.4) が該当した (portfolio-25 の依頼で道具化・`ACD-1.4-CHANGELIST.md`
E10 の項)。

**出すもの**: 前版の記述子が引く条ごとに「新版に在るか」「本文が同じか」と、変わっていれば
一致度 (difflib の ratio)。**Check ではない** —— 変わった条の事実を述べ直すかは判断である。

使い方:
    python3 .github/scripts/measure_descriptor_carryover.py            # 最新の記述子の版 → 現行草案
    python3 .github/scripts/measure_descriptor_carryover.py 1.3 1.4    # 版を指定
"""
from __future__ import annotations

import difflib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
LIC = ROOT / "LICENSES"


def _path(ver: str) -> pathlib.Path:
    p = LIC / f"ACD-{ver}.txt"
    return p if p.exists() else LIC / f"ACD-{ver}-DRAFT.txt"


def _vt(v: str) -> tuple:
    return tuple(int(x) for x in v.split("."))


def _current_draft_version() -> str:
    for p in sorted(LIC.glob("ACD-*-DRAFT.txt")):
        if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]:
            m = re.match(r"ACD-(\d+\.\d+)-DRAFT\.txt$", p.name)
            if m:
                return m.group(1)
    raise SystemExit("ERROR: 作業中の草案 (pointer でない ACD-*-DRAFT.txt) が見つからない")


def _latest_descriptor_version() -> str:
    vs = [re.match(r"ACD-(\d+\.\d+)\.machine\.json$", p.name).group(1)
          for p in LIC.glob("ACD-*.machine.json") if re.match(r"ACD-(\d+\.\d+)\.machine\.json$", p.name)]
    if not vs:
        raise SystemExit("ERROR: 記述子が 1 つも無い")
    return max(vs, key=_vt)


def clauses(ver: str) -> dict[str, str]:
    t = _path(ver).read_text(encoding="utf-8")
    sep = "\n" + "-" * 80 + "\n"
    body = t.split(sep, 1)[1] if sep in t else t
    return {k: " ".join(v.split()) for k, v in
            re.findall(r"^  (\d+\.\d+)\s+(.*?)(?=^  \d+\.\d+\s|^\d+\.\s|\Z)", body, re.M | re.S)}


def cited(ver: str) -> list[str]:
    out = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "clause" and isinstance(v, str):
                    out.append(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(json.loads((LIC / f"ACD-{ver}.machine.json").read_text(encoding="utf-8")))
    return sorted(set(out), key=_vt)


def main() -> int:
    old = sys.argv[1] if len(sys.argv) > 1 else _latest_descriptor_version()
    new = sys.argv[2] if len(sys.argv) > 2 else _current_draft_version()
    a, b = clauses(old), clauses(new)
    cs = cited(old)
    changed, missing = [], []
    for c in cs:
        if c not in b:
            missing.append(c)
        elif a.get(c) != b[c]:
            changed.append((c, difflib.SequenceMatcher(None, a.get(c, ""), b[c]).ratio()))
    print(f"ACD-{old}.machine.json が引く条 {len(cs)} 件を ACD-{new} の本文と比べた")
    print(f"  新版に無い条: {len(missing)}" + (f" {missing}" if missing else ""))
    print(f"  本文が変わった条: {len(changed)}")
    for c, r in changed:
        print(f"    §{c}  一致度 {r:.2f}" + ("  ← 別の条になっている可能性" if r < 0.5 else ""))
    print(f"  変わっていない条: {len(cs) - len(changed) - len(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
