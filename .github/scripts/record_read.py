#!/usr/bin/env python3
"""record_read.py — スレッドを読んだ記録を、READ-THREADS・census・AS-OF・READ-THREADS-LOG へ 1 回で通す。

**なぜ在るか (2026-11-15・2f の依頼)**: 読了のたびに同じ 4 段を手で書いていた (毎回同じ python を手で書き直した)。
(1) READ-THREADS.txt に「会話の始まりの日付<TAB>件名」の行を日付の位置へ足す (会話を読んだときだけ)、
(2) `census_decision_statements.py threads --pin` を回して候補・読了・残りの数を得る、
(3) AS-OF.md の「未読スレッドの残り」のセルの日付・件数・「直近の 1 件」を入れ替える、
(4) 前の「直近の 1 件」を READ-THREADS-LOG.md の先頭 (今日の見出しの下) へ下ろす。
Check 498 (h) は AS-OF の件数を READ-THREADS と THREAD-CANDIDATES から導出して照らすので、(1) と (3) の食い違いは RED になる。

使い方:
    DOSSIER_ARCHIVE_CACHE=~/osi-archive-cache python3 .github/scripts/record_read.py \\
        --start 2018-06-04 --subject "Some notes for license submitters" \\
        --entry '"Some notes for license submitters"（`license-review` 2018-06）を `review-readings-2.md` §1.224 へ（…）'
    --no-thread を付けると (1) を飛ばす (会話を読んだのではなく、通だけを引いたとき・件数は動かない)。--dry-run は書かない。
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / "LICENSES"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--entry", required=True, help="直近の 1 件の本文 (「YYYY-MM-DD に 」の後ろ)")
    ap.add_argument("--start", help="会話の始まりの日付 (census の start・READ-THREADS の行の日付)")
    ap.add_argument("--subject", help="件名 (アーカイブのとおり)")
    ap.add_argument("--no-thread", action="store_true", help="会話を読んだのではない (READ-THREADS に足さない)")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    o = ap.parse_args(argv)
    if not o.no_thread and not (o.start and o.subject):
        print("STOP: 会話を読んだなら --start と --subject が要る (通だけなら --no-thread)")
        return 2
    rt = L / "READ-THREADS.txt"
    rtt = rt.read_text(encoding="utf-8")
    if not o.no_thread:
        row = f"{o.start}\t{o.subject}"
        if row in rtt.split("\n"):
            print(f"STOP: READ-THREADS に既に在る: {row}")
            return 1
        # 並べ直さずに、日付が新しい行より前の位置へ 1 行だけ差し込む (全体を並べ直すと同じ日付の行の順が動き、
        #   差分が 31 行になった・2026-11-15 の試し)
        lines = rtt.split("\n")
        at = next((i for i, ln in enumerate(lines) if ln and not ln.startswith("#") and ln[:10] > o.start), None)
        if at is None:
            at = max(i for i, ln in enumerate(lines) if ln) + 1
        rtt = "\n".join(lines[:at] + [row] + lines[at:])
    # (2) census を一時的な写しの上で回す (--pin は THREAD-CANDIDATES.txt を書くので、dry-run でも本物を汚さない)
    out = Path(tempfile.mkdtemp()) / "threads.json"
    if not o.dry_run:
        rt.write_text(rtt, encoding="utf-8")
    pin = [] if o.dry_run else ["--pin"]
    r = subprocess.run([sys.executable, str(ROOT / ".github/scripts/census_decision_statements.py"), "threads", str(out)] + pin,
                       cwd=ROOT, text=True, capture_output=True, env=dict(os.environ))
    m = re.search(r"AS-OF: 候補 (\d+) 本のうち (\d+) 本を読んだ。(\d+) 本は読んでいない", r.stdout)
    if not m:
        print(f"STOP: census の出力から件数を読めない (アーカイブの写しが要る: DOSSIER_ARCHIVE_CACHE)\n{r.stdout[-500:]}{r.stderr[-500:]}")
        return 1
    n, read, unread = m.groups()
    # (3) AS-OF のセル
    af = L / "AS-OF.md"
    at = af.read_text(encoding="utf-8")
    cell = re.search(r"^\| \*\*未読スレッドの残り\*\* \| \*\*(\d{4}-\d{2}-\d{2}) · (.*?)\*\* \| \*\*候補 \d+ 本のうち \d+ 本を読んだ。"
                     r"\d+ 本は読んでいない\*\*（直近の 1 件: (.*?)）。 \*\*それより前の", at, re.M | re.S)
    if not cell:
        print("STOP: AS-OF.md の「未読スレッドの残り」のセルの形を読めない (形が変わったなら道具を直す)")
        return 1
    old_recent = cell.group(3)
    new_cell = (f"| **未読スレッドの残り** | **{o.date} · {cell.group(2)}** | **候補 {n} 本のうち {read} 本を読んだ。"
                f"{unread} 本は読んでいない**（直近の 1 件: {o.date} に {o.entry}）。 **それより前の")
    at2 = at[:cell.start()] + new_cell + at[cell.end():]
    # (4) LOG の先頭へ前の直近を下ろす
    lg = L / "READ-THREADS-LOG.md"
    lt = lg.read_text(encoding="utf-8")
    heading = f"## {o.date} の読了（新しいものが上）"
    item = f"- {old_recent}\n\n"
    if heading in lt:
        i = lt.index(heading) + len(heading)
        i = lt.index("\n\n", i) + 2
        lt2 = lt[:i] + item + lt[i:]
    else:
        first = re.search(r"^## \d{4}-\d{2}-\d{2} の読了", lt, re.M)
        at_ = first.start() if first else len(lt)
        lt2 = lt[:at_] + heading + "\n\n" + item + lt[at_:]
    print(f"READ-THREADS: {'足さない (--no-thread)' if o.no_thread else row}")
    print(f"AS-OF: 候補 {n} 本のうち {read} 本を読んだ。{unread} 本は読んでいない")
    print(f"LOG の先頭へ下ろす: {old_recent[:100]}…")
    if o.dry_run:
        print("dry-run: 何も書かない")
        return 0
    af.write_text(at2, encoding="utf-8")
    lg.write_text(lt2, encoding="utf-8")
    print("書いた。verify で Check 498 (h) を確かめる")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
