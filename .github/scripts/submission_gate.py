#!/usr/bin/env python3
"""submission_gate.py — 凍結済みの版を license-review へ出す日に、段 6b と 6c を機械で確かめる。

**なぜ在るか (2026-11-23・6d の指摘・fc)**: 段 6b (出す版を license-discuss に少なくとも 30 日置く) の止めは、
`prepare_version_freeze.py` の gate_6b だけが持ち、それは「確定するとき」に草案の冒頭の "Changes since the version posted
on <日付>" を読む。1.4 は list に出す前に `--not-for-submission` で確定したので、1.4 そのものを出す日には確定の道具が
回らず、6b を見る機械が 1 つも無かった (REVISION-PROTOCOL §3.6 の 6b の行は「手で確かめる」と書いていた)。この道具は、
凍結済みの版について、投稿の記録 (FROZEN.md の POSTED-VERSION marker) から 30 日を数え、6c (未読 0・反映) と写しの鮮度を
gate_6c で見る。止まれば理由を出して非 0 で終わる。何も書き換えない。

投稿の記録 (オーナーの投稿が公開アーカイブに届いたのを確かめた人が FROZEN.md に足す。送信控えでなくアーカイブの URL):
    <!-- POSTED-VERSION: ACD-1.4 2026-12-01 https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-December/123456.html -->
拒否された投稿 (届いていない) の道:
    <!-- POSTING-REJECTED: ACD-1.4 2026-12-01 LICENSES/rounds/<stub>.txt -->  と、その日より後の
    <!-- STAGE-6B-DECISION: <日付> proceed … -->  (gate_6b の拒否の道と同じ形)

使い方:
    python3 .github/scripts/submission_gate.py ACD-1.4
"""
from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / "LICENSES"
URL = re.compile(r"https://lists\.opensource\.org/pipermail/license-discuss_lists\.opensource\.org/(\d{4}-[A-Z][a-z]+)/\d+\.html")
POSTED = re.compile(r"<!--\s*POSTED-VERSION:\s*(ACD-\d+\.\d+)\s+(\d{4}-\d{2}-\d{2})\s+(\S+)\s*-->")
REJECTED = re.compile(r"<!--\s*POSTING-REJECTED:\s*(ACD-\d+\.\d+)\s+(\d{4}-\d{2}-\d{2})\s+(LICENSES/rounds/[\w.\-]+\.txt)\s*-->")


def posted_problems(frozen_text: str) -> list[str]:
    """POSTED-VERSION marker の形の誤り (Check 453b が毎回見る・確定の日まで待たない)。"""
    bad = []
    for ver, day, url in POSTED.findall(frozen_text):
        if not (L / f"{ver}.txt").exists():
            bad.append(f"POSTED-VERSION {ver}: 凍結した本文 {ver}.txt が無い")
        u = URL.fullmatch(url)
        if not u:
            bad.append(f"POSTED-VERSION {ver}: URL が license-discuss の公開アーカイブの通の形でない ({url[:80]})")
        elif u.group(1) != datetime.date.fromisoformat(day).strftime("%Y-%B"):
            bad.append(f"POSTED-VERSION {ver}: 届いた日 {day} と URL の月 {u.group(1)} が合わない")
    return bad


def gate(version: str, today: datetime.date | None = None) -> list[str]:
    today = today or datetime.date.today()
    frozen = (L / "FROZEN.md").read_text(encoding="utf-8")
    out = []
    if not (L / f"{version}.txt").exists() or f"LICENSES/{version}.txt" not in frozen:
        return [f"{version} は凍結した版でない (LICENSES/{version}.txt と FROZEN.md の FREEZE-DATA に無い)。確定する版は "
                "prepare_version_freeze.py が gate_6b / gate_6c を見る"]
    out += posted_problems(frozen)
    posts = [(d, u) for v, d, u in POSTED.findall(frozen) if v == version]
    rejs = [(d, s) for v, d, s in REJECTED.findall(frozen) if v == version]
    if posts:
        day = max(d for d, _u in posts)
        left = (datetime.date.fromisoformat(day) + datetime.timedelta(days=30) - today).days
        if left > 0:
            out.append(f"段 6b: {version} が license-discuss に届いた {day} から 30 日の窓が、あと {left} 日残っている")
    elif rejs:
        day, stub = max(rejs)
        if not (ROOT / stub).exists():
            out.append(f"段 6b (拒否の道): stub {stub} が無い")
        dm = re.search(r"<!--\s*STAGE-6B-DECISION:\s*(\d{4}-\d{2}-\d{2})\s+(proceed|wait)\b", frozen)
        if not dm or dm.group(1) < day or dm.group(2) != "proceed":
            out.append(f"段 6b (拒否の道): {day} の拒否より後の STAGE-6B-DECISION proceed が FROZEN.md に無い")
    else:
        out.append(f"段 6b: {version} を license-discuss に出した記録 (FROZEN.md の POSTED-VERSION marker) が無い —— 30 日の窓が"
                   "始まっていない。投稿はオーナーが自分の言葉で書く (B14)。届いたら公開アーカイブの URL と日付を marker に書く")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from prepare_version_freeze import gate_6c
    out += [f"段 6c: {x}" for x in gate_6c()]
    return out


def main(argv: list[str]) -> int:
    vers = [a for a in argv if re.fullmatch(r"ACD-\d+\.\d+", a)]
    if len(vers) != 1:
        print(__doc__.split("使い方:")[1].strip())
        return 2
    problems = gate(vers[0])
    for p in problems:
        print(f"STOP: {p}")
    if not problems:
        print(f"OK: {vers[0]} は段 6b (30 日) と 6c (未読 0・反映・写しの鮮度) を満たす。提出の文面はオーナーが書く (B14)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
