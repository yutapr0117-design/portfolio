#!/usr/bin/env python3
"""suggest_reflection.py — §1.N の節が、どこへ反映されているかの候補を出す (REFLECTION-BACKFILL の行を書くための道具)。

**なぜ在るか (2026-11-15・9b)**: オーナーの前提「全て読んで反映してこそ出せる」で、§1.242 より前の 78 節に反映先を
書く (30 の表 `LICENSES/REFLECTION-BACKFILL.md`)。30 の調べ方 —— 節の番号を review-readings 以外の LICENSES/*.md から
grep し、当たった行が against の行ならその番号、B の節や行ならその B、SUBMISSION-MATERIALS・REVIEWERS なら「入口」——
を 5 人が手で回すと同じ grep を 78 回書くので、道具にした。**出すのは候補であって反映の判断ではない** —— 当たった行が
その節の論点を運んでいるかは読む人が決める。当たらない節は「なし（理由）」か、いまから反映するかを決める。

使い方:
    python3 .github/scripts/suggest_reflection.py 1.223 1.241      # 範囲 (両端を含む)
    python3 .github/scripts/suggest_reflection.py 1.223 1.241 --rows   # 表の行の下書き (候補の無い節は「未定」。Check 501b が照らす)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / "LICENSES"
ENTRY = ("SUBMISSION-MATERIALS.md", "REVIEWERS.md", "REVIEWERS-RECORD.md", "QUESTION-INDEX.md", "READY-TO-SUBMIT.md", "REVISION-PROTOCOL.md", "OSI-APPROVAL-PLAN.md")


def section_b(lines: list[str], i: int) -> str | None:
    """行 i が属する B の見出し (`## B10 ——` など) を上へ辿る。B の文書の段落は B の番号を行に持たないことが多い。"""
    for j in range(i, -1, -1):
        m = re.match(r"^#{2,4} .*?\b(B\d+)\b", lines[j])
        if m:
            return m.group(1)
    return None


def kinds(fname: str, line: str, b: str | None = None) -> list[str]:
    out = []
    m = re.match(r"^\| (\d+) \|", line)
    if fname.startswith("ACD-1.0.against") and m:
        out.append(f"against #{m.group(1)}")
    m = re.match(r"^\| (E\d+) \|", line)
    if fname == "ACD-1.0.errata.md" and m:
        out.append(f"errata {m.group(1)}")
    if fname.startswith("ACD-OSI-BOTTLENECKS"):
        out += sorted(set(re.findall(r"\bB\d+\b", line)))[:3] or [b or "B?"]
    if fname in ENTRY:
        out.append("入口")
    if fname.startswith("ACD-1.4-") and ("TRIAL" in fname or "CHANGELIST" in fname or "DRAFT" in fname):
        out.append("1c")
    return out


def main(argv: list[str]) -> int:
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    lo, hi = (int(x.split(".")[1]) for x in argv[:2])
    rows = "--rows" in argv
    files = [p for p in sorted(L.glob("*.md")) if "review-readings" not in p.name and p.name != "REFLECTION-BACKFILL.md"
             and not p.name.startswith(("READ-THREADS", "AS-OF"))]
    texts = {p.name: p.read_text(encoding="utf-8").split("\n") for p in files}
    for n in range(lo, hi + 1):
        rx = re.compile(rf"§1\.{n}(?![\d])")
        hits = [(f, i + 1, ln) for f, lines in texts.items() for i, ln in enumerate(lines) if rx.search(ln)]
        cand = sorted({k for f, i, ln in hits for k in kinds(f, ln, section_b(texts[f], i - 1))})
        if rows:
            where = "・".join(sorted({f"{f}:{i}" for f, i, _ in hits})[:4]) or "当たり無し"
            # 「入口」と「1c」は行き先の文書を backtick で添える (Check 501b は、grep と言う行の行き先を、反映のセルの
            #   against の行・E の行・B の文書・backtick の file に探す。添えないと照合に落ちる・2026-11-15)。見出しの無い「B?」は出さない
            cell = []
            for k in [c for c in cand if c != "B?"]:
                fs = sorted({f for f, i, ln in hits if k in kinds(f, ln, section_b(texts[f], i - 1))})
                cell.append(f"{k}（{'・'.join(f'`{f}`' for f in fs[:3])}）" if k in ("入口", "1c") else k)
            print(f"| 1.{n} | {' / '.join(cell) if cell else '未定'} | 反映先の文書がこの節の番号を引いていることを grep で確かめた（{where}） |")
            continue
        print(f"1.{n}: 候補 {', '.join(cand) or '(無し)'} · 当たり {len(hits)} 行")
        for f, i, ln in hits[:6]:
            print(f"    {f}:{i}  {' '.join(ln.split())[:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
