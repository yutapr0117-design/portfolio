---
file: LICENSES/REFLECTION-BACKFILL.md
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/ACD-1.0.review-readings.md / LICENSES/REVISION-PROTOCOL.md
---

# LICENSES/REFLECTION-BACKFILL.md

## What

§1.242 より前の review-readings の節（§1.164〜§1.241）について、読んだ当時にどこへ反映したかを 1 節 1 行の表で置く文書。

## Why

提出のゲート（`REVISION-PROTOCOL.md` §3.6 の 6c）は、読んだ節がすべて反映されていることを求める。古い節には末尾の「反映:」の欄が無く、`review-readings.md` に足すと 1,000 行の上限（Check 365）を越えるので、表にした。

## How

行は「節の番号（§ なし）| 反映（Check 501 の語彙）| 確かめ方」。5 人が帯に分けて書く。Check 501 は、古い節について、この表の行と節の末尾の欄のどちらか一方があることを照らす（9b が足す）。

## Constraints

同じ節に、表の行と末尾の欄の両方を置かない。against #N と errata E# は実在する番号だけを書く。

## Change impact

`REVISION-PROTOCOL.md` の 6c、`SUBMISSION-MATERIALS.md` の確定手順、Check 501 がこの表を読む。

## Audience-specific notes

- **監査人**: 各行の反映先の文書で、その節の番号を grep すれば確かめられる。
