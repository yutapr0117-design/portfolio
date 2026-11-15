---
file: LICENSES/rounds/2021-09-license-discuss-afl-reuse-crane-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/rounds/README.md (置き方の規約)
---

# LICENSES/rounds/2021-09-license-discuss-afl-reuse-crane-observed.txt

## What

"Status of earlier AFL licenses?"（`license-discuss` 2021-09）から Sebastian Crane 氏の 1 通を無改変で置いた。AFL の文言は REUSE と SPDX の識別子での使用を妨げるようなので、スクリプトは MIT-0 にした、という通。

## Why

`ACD-1.0.review-readings-2.md` §1.231 の一次資料として置く。告知の形を本文で固定したライセンスが機械可読の慣行と衝突しうる例で、§2.6（T69）が SPDX 式や REUSE file でも足りると開くことへの当て。

## How

公開アーカイブのローカルの写しから 2026-11-15 に切り出した（`add_round.py`）。先頭に最小限のヘッダを足し、`----- begin verbatim -----` より下は無改変である。

## Constraints

無改変保存の場所なので本文を直さない（`rounds/README.md`）。

## Change impact

このファイルの通を引く節を直すときは、引用が本文に在るかを確かめる。

## Audience-specific notes

- **監査人**: 引用は元のアーカイブの月に当てて確かめられる。
