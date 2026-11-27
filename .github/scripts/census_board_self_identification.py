#!/usr/bin/env python3
"""送り手自身が OSI の理事・役員であると述べた行を、公開アーカイブの写しから送り手×月で数える。

**在任の下限の根拠だけに使う。在任の否定の根拠にはしない。** 署名の帯の役は本人の自己申告で、役の正式な記録
（理事会の議事録の名簿・理事会ページ）ではない。名乗っていない月が在任でなかったことにはならない（2008-07 の
Prabhakar 氏の 6 通は "-- Ernie P." だけで、前後の月は "OSI Board Observer" と署名していた）。
**CI には入れない・Check も作らない** —— 支えが出るのはドシエの窓の外の役の文 71 件のうち少数で、否定の根拠に
できないものは RED の基準にならない（2026-11-27・d7 が数え、7e が判断した）。

なぜ在るか: ドシエの「当時の理事」「当時の会長」の根拠は、repo では議事録の名簿（2025-06〜2026-06・
`rounds/2026-09-13-osi-board-meeting-minutes-2025-06-to-2026-06.txt`）だけで、それより前の文は根拠を持てなかった。
理事会ページの過去の写しは取得の経路で拒否された（web.archive.org・2026-11-27）。この道具は、手元の写しの
本人の通（月の file と行）を根拠として指せるようにする。

使い方:
    DOSSIER_ARCHIVE_CACHE=<dir> python3 .github/scripts/census_board_self_identification.py [<名の正規表現>]

<dir> は `census_decision_statements.py` と同じ写し（`<list>-<YYYY>-<Month>.txt`）。既定は ~/osi-archive-cache。
出力は人ごと、役を述べた行ごとに「最初の月..最後の月 (通数) 行 [最初の写しの file]」。sig = 本文の末尾 12 行（署名の帯）、
body = それ以外。**body の行の多くは理事会への言及で、自己申告ではない**（"the OSI Board shares that belief"）。根拠に使うのは
sig の役の名乗りと、body のうち本人が役を述べた文（"in my capacity as a Board member"）だけで、読んで選ぶ。
引用（`>` で始まる行）と、"-----Original Message" より後は、他人の文なので数えない。
"""
from __future__ import annotations

import collections
import os
import re
import sys
from pathlib import Path

MON = {m: i for i, m in enumerate("January February March April May June July August September October November December".split(), 1)}
ROLE = re.compile(
    r"(OSI|Open Source Initiative)[^\n]{0,40}\b(Board|Director|Treasurer|Secretary|President|Vice[ -]President|General Manager|Executive Director)\b"
    r"|\b(Board (of Directors|member|Member|Director)|Director|Treasurer|Secretary|President|Chair(man)?)\b[^\n]{0,25}(OSI|Open Source Initiative)"
    r"|\b(I am|I'm|I was|as an?|speaking as)[^\n.]{0,20}(OSI )?(board member|director|member of the (OSI )?[Bb]oard)"
    r"|\bon the (OSI )?[Bb]oard\b")
MSG = re.compile(r"\n(?=From \S+ at \S+ +\w{3} \w{3} +\d+ )")


def own_lines(msg: str) -> list[str]:
    """通の本文のうち送り手自身の行 (`>` の引用と、"-----Original Message" より後を除く)。

    "wrote:" で切らない: 行間に答える形では、本人の署名は引用の後ろに来る。"wrote:" で切った初版は、Prabhakar 氏の
    2008-03 の "L-D Moderator, OSI Board Observer" を落とした (2026-11-27)。`>` の付かない引用 (Outlook の形) だけ切る。
    """
    body = msg.split("\n\n", 1)[1] if "\n\n" in msg else ""
    lines = [ln for ln in body.split("-------------- next part")[0].split("\n") if not ln.lstrip().startswith(">")]
    for i, ln in enumerate(lines):
        if re.match(r"\s*-----\s*Original Message", ln):
            return lines[:i]
    return lines


def census(cache: Path) -> dict[str, list[tuple[str, str, str, str]]]:
    """{送り手: [(YYYY-MM, 写しの file 名, sig|body, 行)]}。"""
    rows: dict[str, list[tuple[str, str, str, str]]] = collections.defaultdict(list)
    for f in sorted(cache.glob("license-*-*.txt")):
        m = re.match(r"license-\w+-(\d{4})-(\w+)\.txt$", f.name)
        if not m or m.group(2) not in MON:
            continue
        month = f"{m.group(1)}-{MON[m.group(2)]:02d}"
        for msg in MSG.split(f.read_text(encoding="utf-8", errors="replace")):
            fm = re.search(r"^From: .*?\((.*?)\)\s*$", msg, re.M)
            who = fm.group(1).strip() if fm else "?"
            lines = own_lines(msg)
            for i, ln in enumerate(lines):
                if ROLE.search(ln):
                    rows[who].append((month, f.name, "sig" if i >= len(lines) - 12 else "body", " ".join(ln.split())[:120]))
    return rows


def main(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    cache = Path(os.environ.get("DOSSIER_ARCHIVE_CACHE", Path.home() / "osi-archive-cache"))
    if not cache.is_dir():
        print(f"写しが無い: {cache}", file=sys.stderr)
        return 2
    name = re.compile(argv[0]) if argv else None
    rows = census(cache)
    for who in sorted(rows, key=lambda w: (-len(rows[w]), w)):
        if name and not name.search(who):
            continue
        print(f"## {who}")
        by = collections.defaultdict(list)
        for month, fname, kind, ln in rows[who]:
            by[(kind, ln)].append((month, fname))
        for (kind, ln), ms in sorted(by.items(), key=lambda x: min(x[1])):
            print(f"   {kind:4} {min(ms)[0]}..{max(ms)[0]} ({len(ms)}) {ln}  [{min(ms)[1]}]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
