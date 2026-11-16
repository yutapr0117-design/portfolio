---
file: LICENSES/READ-THREADS-LOG-2026-11-15.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/READ-THREADS-LOG.md / LICENSES/READ-THREADS.txt
---

# LICENSES/READ-THREADS-LOG-2026-11-15.md

## What

未読スレッドを読んだ記録のうち、2026-11-15 以前の 2 節（「2026-11-15 の読了」と「2026-11-12 以前の読了」）。

## Why

`READ-THREADS-LOG.md` は `record_read.py` が 1 件ずつ先頭に足すので増え続け、2026-11-16 に 870 行（advisory 950）になった。古い節は書き足されないので、別の file に移した（752 行）。

## How

本文は移す前と 1 字も変えていない（移した部分を元の file の同じ範囲と diff して一致を確かめた）。`READ-THREADS-LOG.md` の末尾に、この file を指す節を置いた。

## Constraints

書き足さない（新しい記録は `READ-THREADS-LOG.md` の先頭）。

## Change impact

ドシエの節が「READ-THREADS-LOG」と書いて 11-15 以前の記録を指すときは、この file に在る。

## Audience-specific notes

- **AI / 後任**: また `READ-THREADS-LOG.md` が予算に近づいたら、同じ形で古い日の節を `READ-THREADS-LOG-<最後の日>.md` へ移す。
