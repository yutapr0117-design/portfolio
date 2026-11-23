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
    --entry は単一引用符で渡す (二重引用符だと zsh が `…` を command substitution として評価し、消える・2f が踏んだ)。
    --no-thread を付けると (1) を飛ばす (会話を読んだのではなく、通だけを引いたとき・件数は動かない)。--dry-run は書かない。
    --log-only は AS-OF の直近の 1 件を動かさず、LOG にだけ 1 項目を足す (読んだが新しい論点の無い会話をまとめた項目など・
    件数は直す)。候補の数が変わったら (候補の外の会話を読んだとき)、項目の末尾に「候補は X → Y」を書き足す (2f の依頼)。
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
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_git_guard import require_unambiguous_origin
    require_unambiguous_origin()  # origin/main が古い作業 branch に解決されないこと (2026-11-23)
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--entry", required=True, help="直近の 1 件の本文 (「YYYY-MM-DD に 」の後ろ)。単一引用符で渡す (` を含むため)")
    ap.add_argument("--start", help="会話の始まりの日付 (census の start・READ-THREADS の行の日付)")
    ap.add_argument("--subject", help="件名 (アーカイブのとおり)")
    ap.add_argument("--no-thread", action="store_true", help="会話を読んだのではない (READ-THREADS に足さない)")
    ap.add_argument("--log-only", action="store_true",
                    help="AS-OF の直近の 1 件は動かさず、LOG にだけ 1 項目を足す (新しい論点の無い会話をまとめた項目など・件数は直す)")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    o = ap.parse_args(argv)
    if not o.no_thread and not (o.start and o.subject):
        print("STOP: 会話を読んだなら --start と --subject が要る (通だけなら --no-thread)")
        return 2
    from census_decision_statements import read_rows, read_threads_file_for
    # 書く file は会話の始まりの年で選ぶ (2026-11-16 に 2 つに分けた)。--no-thread は書かないが、戻すために 1 つ持つ
    rt = read_threads_file_for(o.start or "0000", L)
    rtt = rt.read_text(encoding="utf-8")
    if not o.no_thread:
        # --start は census の会話の始まりの日付 (THREAD-CANDIDATES の行の日付) でなければならない (Check 498 (h) は
        #   (件名の key, 日付) の組で照らす)。最初の通の日付 (アーカイブの月の境で別の日になる) を渡すと、候補の外の
        #   会話を読んだと数えられ、件数が合わない (2f が 2026-11-15 に 10-04 と 10-06 で 1 度踏んだ・5 人で読む日の依頼)。
        #   同じ件名の候補が在って日付が違えば止まる。件名が候補に無いのは「候補の外」を読んだときで、正当なので知らせるだけ
        from census_decision_statements import _list_rows, title_key
        from census_decision_statements import candidate_rows
        same = [d for k, d, _t in candidate_rows(L) if k == title_key(o.subject)]
        if same and o.start not in same:
            print(f"STOP: --start {o.start} は THREAD-CANDIDATES の同じ件名の会話の日付 {', '.join(same)} のどれでもない。"
                  "census の start (会話の始まり) を渡す")
            return 2
        if not same:
            print("注意: この件名は THREAD-CANDIDATES に無い (候補の外を読んだ)。候補の数 N と読了 M が同じだけ増える")
        row = f"{o.start}\t{o.subject}"
        if (title_key(o.subject), o.start) in {(k, d) for k, d, _t in read_rows(L)}:
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
    # 後の段で STOP したら書いた file を元に戻す (2026-11-16・9b が踏んだ: AS-OF のセルを読めずに STOP し、READ-THREADS に
    #   14 行と --pin の THREAD-CANDIDATES だけが残った)。census は READ-THREADS を読むので、書いてから回すしかない
    from census_decision_statements import split_files
    backup = {f: f.read_text(encoding="utf-8") for f in [rt] + split_files("THREAD-CANDIDATES", L)}

    def stop(msg: str) -> int:
        if not o.dry_run:
            for f, txt in backup.items():
                f.write_text(txt, encoding="utf-8")
        print(msg + (" (READ-THREADS と THREAD-CANDIDATES は元に戻した)" if not o.dry_run else ""))
        return 1
    if not o.dry_run:
        rt.write_text(rtt, encoding="utf-8")
    pin = [] if o.dry_run else ["--pin"]
    r = subprocess.run([sys.executable, str(ROOT / ".github/scripts/census_decision_statements.py"), "threads", str(out)] + pin,
                       cwd=ROOT, text=True, capture_output=True, env=dict(os.environ))
    m = re.search(r"AS-OF: 候補 (\d+) 本のうち (\d+) 本を読んだ。(\d+) 本は読んでいない", r.stdout)
    if not m:
        return stop(f"STOP: census の出力から件数を読めない (アーカイブの写しが要る: DOSSIER_ARCHIVE_CACHE)\n{r.stdout[-500:]}{r.stderr[-500:]}")
        return 1
    n, read, unread = m.groups()
    # (3) AS-OF のセル
    af = L / "AS-OF.md"
    at = af.read_text(encoding="utf-8")
    cell = re.search(r"^\| \*\*未読スレッドの残り\*\* \| \*\*(\d{4}-\d{2}-\d{2}) · (.*?)\*\* \| \*\*候補 \d+ 本のうち \d+ 本を読んだ。"
                     r"\d+ 本は読んでいない\*\*（直近の 1 件: (.*?)(?:）。|。）) \*\*それより前の", at, re.M | re.S)
    # 閉じ方は「）。」と「。）」の両方を読む (2026-11-16・2f の報告: 手で追記したセルが「…無い。）」で終わり、道具が STOP した)。
    #   書くときは「）。」に揃える (下の new_cell)
    if not cell:
        return stop("STOP: AS-OF.md の「未読スレッドの残り」のセルの形を読めない (形が変わったなら道具を直す)")
    old_recent = cell.group(3)
    old_n = int(re.search(r"\*\*候補 (\d+) 本", cell.group(0)).group(1))
    entry = o.entry
    if int(n) != old_n:
        # 候補の外の会話を読むと census は読んだ会話を母数に入れ、N と M が同じだけ増える (K は動かない)。
        #   2f はそれを直近の文に手で書き足していた (2026-11-15 の依頼) ので、道具が書く
        entry += f"（候補は {old_n} → {n}・読んだので母数に入った）"
    recent = old_recent if o.log_only else f"{o.date} に {entry}"
    new_cell = (f"| **未読スレッドの残り** | **{o.date} · {cell.group(2)}** | **候補 {n} 本のうち {read} 本を読んだ。"
                f"{unread} 本は読んでいない**（直近の 1 件: {recent}）。 **それより前の")
    at2 = at[:cell.start()] + new_cell + at[cell.end():]
    # (4) LOG の先頭へ前の直近を下ろす
    lg = L / "READ-THREADS-LOG.md"
    lt = lg.read_text(encoding="utf-8")
    heading = f"## {o.date} の読了（新しいものが上）"
    item = f"- {o.date} に {entry}\n\n" if o.log_only else f"- {old_recent}\n\n"
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
    print(f"LOG の先頭へ: {item[2:102]}…" + ("" if o.log_only else " (前の直近の 1 件を下ろす)"))
    if o.dry_run:
        print("dry-run: 何も書かない")
        return 0
    af.write_text(at2, encoding="utf-8")
    lg.write_text(lt2, encoding="utf-8")
    # READ-THREADS と LOG の行数が予算表 (Check 424) とずれるので、行数の表も直す (2026-11-16・50 の依頼: 読了を足す PR が
    #   424 で赤になり、5 人とも sync-sizes を回し忘れうる)
    subprocess.run([sys.executable, str(ROOT / ".github/scripts/sync_size_table.py")], cwd=ROOT, capture_output=True)
    print("書いた (行数の表も直した)。verify で Check 498 (h) を確かめる")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
