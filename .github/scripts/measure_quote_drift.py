#!/usr/bin/env python3
"""measure_quote_drift.py — 提出側の文書が逐語で引くライセンス本文が、出す版にもまだ在るかを測る。

**なぜ在るか。** 提出パケットと入口ページは 1.0 の文面を逐語で引く。新しい版を出すなら、その引用は
**出す版の文面と一致しなければならない** ——引用が現物と違う提出は、審査者が最初に気づく種類の誤り
である。`measure_citation_drift.py` は「引いた**条番号**の意味が変わったか」を測るが、**逐語の文**が
まだ在るかは見ない。確定手順 (`ACD-1.1-CHANGELIST.md` §0.13) はこれを手で回していた
(2026-11-01 に 1.4 草案で回し、既知の §6.4 の 1 件だけだった)。portfolio-25 の依頼で道具にした。

**やること**: 提出側 5 面から 40 字以上の引用 (`*"…"*` と `"…"`) を取り、省略記号 (`…` / `...`) で
断片に分け、空白を正規化して、**旧版の本文に在り、新版の本文に無い断片**を列挙する。
どちらの版にも無い断片 (ライセンス本文以外の引用) は対象外。

**Check にしない理由**: 引用を新版に合わせるか、旧版の引用だと明示して残すかは判断であり、
正当な旧版引用 (「1.0 はこう書いていた」) まで RED にする。手で回し、出た一覧を人が当たる。

使い方:
    python3 .github/scripts/measure_quote_drift.py            # 1.0 → 現行草案
    python3 .github/scripts/measure_quote_drift.py 1.0 1.4    # 版を指定
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FACES = ["ACD-1.0.submission.md", "ACD-1.0.submission-reference.md",
         "ACD-1.0.submission-osd.md", "REVIEWERS.md", "READY-TO-SUBMIT.md"]
MIN_LEN = 40


def _path(ver: str) -> pathlib.Path:
    p = ROOT / "LICENSES" / f"ACD-{ver}.txt"
    return p if p.exists() else ROOT / "LICENSES" / f"ACD-{ver}-DRAFT.txt"


def _current_draft_version() -> str:
    for p in sorted((ROOT / "LICENSES").glob("ACD-*-DRAFT.txt")):
        if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]:
            m = re.match(r"ACD-(\d+\.\d+)-DRAFT\.txt$", p.name)
            if m:
                return m.group(1)
    raise SystemExit("ERROR: 作業中の草案 (pointer でない ACD-*-DRAFT.txt) が見つからない")


def norm(s: str) -> str:
    return " ".join(s.replace("’", "'").replace("“", '"').replace("”", '"').split())


def body(ver: str) -> str:
    """区切り線 (`-` × 80) の後の本文。区切り線が無い版 (1.0) は全文。"""
    t = _path(ver).read_text(encoding="utf-8")
    sep = "\n" + "-" * 80 + "\n"
    return norm(t.split(sep, 1)[1] if sep in t else t)


def fragments(text: str):
    """(行番号, 断片) を返す。`*"…"*` と `"…"` の中身を省略記号で割った各断片。

    **2 通りの取り方の和集合をとる (2026-11-01 実測)**: 行単位だと折り返した引用を丸ごと落とし、
    段落単位だと途中の 1 個の `"` で対応がずれて別の引用を落とす —— 1.0 → 1.4 で、行単位は §6.4 の
    1 件、段落単位は §4.4 の 2 件だけを見つけ、どちらも相手の分を見落とした。どの断片も「旧版の本文に
    逐語で在る」ことを要求するので、取り過ぎても誤検出にはなりにくい。
    """
    seen = set()
    for n, line in enumerate(text.split("\n"), 1):
        for m in re.finditer(r'"([^"\n]{%d,})"' % MIN_LEN, line):
            for frag in re.split(r"\s*(?:…|\.\.\.)\s*", m.group(1)):
                frag = norm(frag).strip(" .,;:")
                if len(frag) >= MIN_LEN and frag not in seen:
                    seen.add(frag)
                    yield n, frag
    for m in re.finditer(r'"((?:[^"\n]|\n(?!\s*\n)){%d,}?)"' % MIN_LEN, text):
        n = text.count("\n", 0, m.start()) + 1
        for frag in re.split(r"\s*(?:…|\.\.\.)\s*", m.group(1)):
            frag = norm(re.sub(r"\n\s*>?\s*", " ", frag)).strip(" .,;:")
            if len(frag) >= MIN_LEN and frag not in seen:
                seen.add(frag)
                yield n, frag


def main() -> int:
    old = sys.argv[1] if len(sys.argv) > 1 else "1.0"
    new = sys.argv[2] if len(sys.argv) > 2 else _current_draft_version()
    b_old, b_new = body(old), body(new)
    lost, total = [], 0
    for face in FACES:
        p = ROOT / "LICENSES" / face
        if not p.exists():
            print(f"  ※ {face} が無い (読み先を直せ)")
            continue
        for n, frag in fragments(p.read_text(encoding="utf-8")):
            if frag in b_old:
                total += 1
                if frag not in b_new:
                    lost.append((face, n, frag))
    print(f"提出側 {len(FACES)} 面の逐語引用のうち ACD-{old} の本文に在る断片: {total}")
    print(f"  そのうち ACD-{new} の本文に無いもの: {len(lost)}")
    for face, n, frag in lost:
        print(f"  [{face}:{n}] {frag[:160]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
