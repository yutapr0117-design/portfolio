#!/usr/bin/env python3
"""measure_section4c.py — 提出パケット §4c の「機械で確かめたこと」を、任意の版について測り直す。

**なぜ在るか。** `ACD-1.0.submission-reference.md` §4c は「弁護士が読んでいない」への答えとして、
機械で確かめられる性質を数字で並べ、**後継版も同じ機械監査を通る**ことを 1 行で主張する。その行は
版を確定するたびに手で測り直していた (§0.13・portfolio-25 の依頼で 2026-11-01 に道具化)。
Check 460 face (n) は §4c の数値を **1.0** について強制するが、出す版は 1.0 とは限らない。

**測るもの** (§4c の行と同じ順):
  1. 定義語: 数・すべて §1 にあること・未使用 0 (定義した条の外での出現回数の最小値)
  2. 節番号が 1〜N で連番
  3. 非 ASCII バイト 0
  4. 内部の `Section N.M` / `Sections N.M` 参照がすべて実在する条を指す
  5. authoritative language を定める条がある
  6. 本文 (区切り線より後・草案の状態ブロックを除く) の `shall` / `must` の数
  7. 条数・語数
  8. 記述子 (`ACD-<版>.machine.json`) があれば、その `clause` がすべて実在する

**Check ではない** —— 1.0 の値は Check 460 (n) / 441b / 441d が既に強制しており、ここは版を引数に
取って確定日に 1 コマンドで §4c の後継版の行を更新するための道具。

使い方:
    python3 .github/scripts/measure_section4c.py          # 現行草案
    python3 .github/scripts/measure_section4c.py 1.3      # 版を指定
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
LIC = ROOT / "LICENSES"


def _path(ver: str) -> pathlib.Path:
    p = LIC / f"ACD-{ver}.txt"
    return p if p.exists() else LIC / f"ACD-{ver}-DRAFT.txt"


def _current_draft_version() -> str:
    for p in sorted(LIC.glob("ACD-*-DRAFT.txt")):
        if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]:
            m = re.match(r"ACD-(\d+\.\d+)-DRAFT\.txt$", p.name)
            if m:
                return m.group(1)
    raise SystemExit("ERROR: 作業中の草案 (pointer でない ACD-*-DRAFT.txt) が見つからない")


def main() -> int:
    ver = sys.argv[1] if len(sys.argv) > 1 else _current_draft_version()
    path = _path(ver)
    if not path.exists():
        raise SystemExit(f"ERROR: {path.relative_to(ROOT)} が無い")
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    sep = "\n" + "-" * 80 + "\n"
    body = text.split(sep, 1)[1] if sep in text else text

    clauses = dict(re.findall(r"^  (\d+\.\d+)\s+(.*?)(?=^  \d+\.\d+\s|^\d+\.\s|\Z)", body, re.M | re.S))
    sections = [int(n) for n in re.findall(r"^(\d+)\. [A-Z]", body, re.M)]

    # 1. 定義語
    terms = re.findall(r'^  (1\.\d+)\s+"([^"]+)"\s+means', body, re.M)
    flat = {k: " ".join(v.split()) for k, v in clauses.items()}
    alltext = " ".join(flat.values())
    uses = {}
    for num, term in terms:
        outside = alltext.replace(flat.get(num, ""), " ")
        uses[term] = len(re.findall(r"\b" + re.escape(term) + r"\b", outside))
    unused = [t for t, n in uses.items() if n == 0]

    # 4. 内部参照
    refs, occ = set(), 0
    for m in re.finditer(r"\bSections?\s+(\d+\.\d+(?:\([a-z]\))?(?:(?:,\s*|\s+(?:and|or|to)\s+)\d+\.\d+(?:\([a-z]\))?)*)", " ".join(body.split())):
        _ns = re.findall(r"\d+\.\d+", m.group(1))
        occ += len(_ns)
        refs.update(_ns)
    dangling = sorted(r for r in refs if r not in clauses)

    # 6. 義務語
    deontic = {w: len(re.findall(r"\b%s\b" % w, body)) for w in ("shall", "must")}

    print(f"ACD-{ver}  ({path.relative_to(ROOT)})")
    print(f"  1. 定義語 {len(terms)} 件 (§{terms[0][0]}–§{terms[-1][0]})・未使用 {len(unused)}"
          + (f" {unused}" if unused else "")
          + (f"・最少使用 {min(uses.values())} 回 ({', '.join(t for t, n in uses.items() if n == min(uses.values()))})" if uses else ""))
    contiguous = sections == list(range(1, len(sections) + 1))
    print(f"  2. 節 {len(sections)} 個・1–{len(sections)} 連番: {'yes' if contiguous else 'NO ' + str(sections)}")
    print(f"  3. 非 ASCII バイト: {sum(1 for b in raw if b > 127)}")
    print(f"  4. 内部参照 {occ} 箇所 ({len(refs)} 条)・解決しないもの {len(dangling)}" + (f" {dangling}" if dangling else ""))
    # 「authoritative」の語で決める (English + translation で探すと §16 の翻訳の扱いの文を拾う・初版で実測)
    al = [k for k, v in flat.items() if "authoritative" in v.lower()]
    print(f"  5. authoritative language の条: {', '.join('§' + k for k in al) or 'なし'}")
    print(f"  6. 本文の shall {deontic['shall']} / must {deontic['must']}  (区切り線より後のみ・状態ブロックは除外)")
    print(f"  7. 条 {len(clauses)}・語 {len(body.split())} (本文) / {len(text.split())} (file 全体・草案は状態ブロックを含む)")
    md = LIC / f"ACD-{ver}.machine.json"
    if md.exists():
        cited = []

        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "clause" and isinstance(v, str):
                        cited.append(v)
                    else:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)

        walk(json.loads(md.read_text(encoding="utf-8")))
        bad = sorted({c for c in cited if c not in clauses})
        print(f"  8. 記述子の clause {len(cited)} 件・本文に無いもの {len(bad)}" + (f" {bad}" if bad else ""))
    else:
        print(f"  8. 記述子 {md.name} はまだ無い (版の確定時に作る)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
