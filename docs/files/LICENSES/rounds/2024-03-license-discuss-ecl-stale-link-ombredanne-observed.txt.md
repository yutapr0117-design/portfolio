---
file: LICENSES/rounds/2024-03-license-discuss-ecl-stale-link-ombredanne-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/rounds/README.md (置き方の規約)
---

# LICENSES/rounds/2024-03-license-discuss-ecl-stale-link-ombredanne-observed.txt

## What

"stale link in license terms"（`license-discuss` 2024-03）から Philippe Ombredanne 氏の 1 通を無改変で置いた。ECL-2.0 の付録の URL が死んだ件で、本文を直すと checksum で照合する道具を欺くので悪手、URL を避けて SPDX-License-Identifier の札を使え、という通。

## Why

`ACD-1.0.review-readings-2.md` §1.231 の一次資料として置く。本文に外部の場所を書くと古びることの実例で、1.4 草案の §2.6（T69）が機械可読の形式を例示することへの当て。

## How

公開アーカイブのローカルの写しから 2026-11-15 に切り出した（`add_round.py`）。先頭に最小限のヘッダを足し、`----- begin verbatim -----` より下は無改変である。

## Constraints

無改変保存の場所なので本文を直さない（`rounds/README.md`）。

## Change impact

このファイルの通を引く節を直すときは、引用が本文に在るかを確かめる。

## Audience-specific notes

- **監査人**: 引用は元のアーカイブの月に当てて確かめられる。
