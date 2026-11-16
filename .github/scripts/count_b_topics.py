#!/usr/bin/env python3
"""count_b_topics.py — 読んだ節が B1〜B15 のどれに当たったかを、会話の年代ごとに数える (頻度表の道具)。

**なぜ在るか (2026-11-16・30 の依頼・1c の段取り案)**: 未読 0・全節反映を満たした後、5 人で「審査で最初に問われる順」を
数で決め、入口 (REVIEWERS / SUBMISSION-MATERIALS) の答えの順に使う。節は 200 を越え、手で数えると数え方が人ごとに割れる
(2f の 604 と Check の 606 の型)。数え方を 1 つの道具に置く。

**数えるもの**:
  - 対象の節: LICENSES/*.md の `## 1.N` (comparison・REVISION-PROTOCOL・CHANGELIST・REFLECTION-BACKFILL を除く。Check 501b と同じ)。
  - 節の B#: 節の表の「ACD への当たり方」の列 (表の最後の列) と、節の末尾の「**反映**:」の行に出る B1〜B15。§1.242 より前の節は
    REFLECTION-BACKFILL の行の反映のセルの B# も足す。1 つの節で同じ B# は 1 回だけ数える (節ごとの有無)。
  - 決める側: 節の表の行の「誰が」の列 (2 列目) が census の DECIDERS に当たる行の B# を、別の列「決める側の行」で数える。
  - 年代: 節の見出しの末尾の括弧の中の年 (「・2002-10」など・見出しの日付 (2026-11-15) は除く)。読めなければ本文の最初の
    年 (1998〜2025)、それも無ければ「不明」。会話の年であって、節を書いた年ではない。

**数えないもの (重要)**: 「最初に問われた」の順そのもの —— 節は我々が読んだ会話の記録で、審査の問いの母集団ではない。
読む順と選び方 (census の候補) の偏りがそのまま入る。出力は「我々の記録の中での頻度」であって、審査の頻度ではない。

使い方:
    python3 .github/scripts/count_b_topics.py              # B × 年代 (5 年ごと) の表と、B ごとの合計・決める側の行の数
    python3 .github/scripts/count_b_topics.py --by-year    # 年ごと
    python3 .github/scripts/count_b_topics.py --sections B10   # その B に当たった節の一覧 (番号・文書・年)
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from census_decision_statements import DECIDERS  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / "LICENSES"
EXCLUDE = ("ACD-1.0.comparison.md", "REVISION-PROTOCOL.md", "REFLECTION-BACKFILL.md")
B = re.compile(r"\bB(1[0-5]|[1-9])\b")
REFLECT = re.compile(r"^\*\*反映\*\*[:：](.*)$", re.M)


def sections() -> list[dict]:
    out = []
    for p in sorted(L.glob("*.md")):
        if p.name in EXCLUDE or p.name.endswith("-CHANGELIST.md"):
            continue
        t = p.read_text(encoding="utf-8")
        hs = list(re.finditer(r"^## 1\.(\d+)\b(.*)$", t, re.M))
        for i, h in enumerate(hs):
            body = t[h.end(): hs[i + 1].start() if i + 1 < len(hs) else len(t)]
            head = h.group(2)
            years = [int(y) for y in re.findall(r"(?<!\d)(199[89]|20[0-2]\d)(?:-\d\d)?(?!\d)", head) if int(y) <= 2025]
            if not years:
                years = [int(y) for y in re.findall(r"(?<!\d)(199[89]|20[0-2]\d)(?!\d)", body) if int(y) <= 2025][:1]
            bs, dec = set(), set()
            for row in re.findall(r"^\|(.+)\|\s*$", body, re.M):
                cells = [c.strip() for c in row.split("|")]
                if len(cells) < 3 or set(cells[0]) <= set(":- "):
                    continue
                found = {f"B{m}" for m in B.findall(cells[-1])}
                bs |= found
                if DECIDERS.search(cells[1]):
                    dec |= found
            for v in REFLECT.findall(body):
                bs |= {f"B{m}" for m in B.findall(v)}
            out.append({"file": p.name, "num": int(h.group(1)), "year": years[0] if years else None, "B": bs, "dec": dec})
    bf = L / "REFLECTION-BACKFILL.md"
    if bf.exists():
        idx = {}
        for s in out:
            idx.setdefault(s["num"], []).append(s)
        for row in re.findall(r"^\|(.+)\|\s*$", bf.read_text(encoding="utf-8"), re.M):
            cells = [c.strip() for c in row.split("|")]
            m = re.search(r"(?:`?(ACD-1\.0\.[\w\-]+\.md)`?\s+|([a-z][\w\-]+)\s+)?1\.(\d+)$", cells[0]) if cells else None
            if not m or len(cells) < 2:
                continue
            f = m.group(1) or (f"ACD-1.0.{m.group(2)}.md" if m.group(2) else None)
            for s in idx.get(int(m.group(3)), []):
                if f is None or s["file"] == f:
                    s["B"] |= {f"B{x}" for x in B.findall(cells[1])}
    return out


def bucket(y: int | None, by_year: bool) -> str:
    if y is None:
        return "不明"
    return str(y) if by_year else f"{y - y % 5}–{y - y % 5 + 4}"


def main(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    secs = sections()
    if "--sections" in argv:
        b = argv[argv.index("--sections") + 1]
        for s in sorted((s for s in secs if b in s["B"]), key=lambda s: (s["year"] or 0, s["num"])):
            print(f"§1.{s['num']}\t{s['file']}\t{s['year'] or '不明'}\t{'決める側の行' if b in s['dec'] else ''}")
        return 0
    by_year = "--by-year" in argv
    cols = sorted({bucket(s["year"], by_year) for s in secs}, key=lambda c: (c == "不明", c))
    tab = collections.defaultdict(collections.Counter)
    tot, dec = collections.Counter(), collections.Counter()
    for s in secs:
        for b in s["B"]:
            tab[b][bucket(s["year"], by_year)] += 1
            tot[b] += 1
        for b in s["dec"]:
            dec[b] += 1
    order = sorted(tot, key=lambda b: (-tot[b], int(b[1:])))
    print(f"# 節 {len(secs)} (B# を持つ節 {sum(1 for s in secs if s['B'])}・年代の読めない節 {sum(1 for s in secs if s['year'] is None)})"
          " —— 我々の記録の中での頻度であって、審査の問いの頻度ではない")
    print("| B | 合計 | 決める側の行 | " + " | ".join(cols) + " |")
    print("| :-- | --: | --: | " + " | ".join("--:" for _ in cols) + " |")
    for b in order:
        print(f"| {b} | {tot[b]} | {dec[b]} | " + " | ".join(str(tab[b][c] or "") for c in cols) + " |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
