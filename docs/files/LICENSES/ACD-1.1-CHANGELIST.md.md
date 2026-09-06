---
file: LICENSES/ACD-1.1-CHANGELIST.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-06
canonical-ref: LICENSES/ACD-1.0.errata.md / LICENSES/REVISION-PROTOCOL.md (§1 §2) / LICENSES/FROZEN.md
---

# LICENSES/ACD-1.1-CHANGELIST.md

## What

次版 ACD-1.1 に反映する候補を集める**単一の集約点**。errata・他文書に散っていた候補・
届いた指摘の 3 系統を 1 つの表に集める。**内容は複製せず `E<n>` を引く**。

## Why

**凍結は「1.0 を通すために動かせない」ではなく「読まれている版が動かない」である。**
議論の目的は意見を集めることで、集めたものを反映した版を出すのが次の段。オーナーの運用方針
（2026-09-04）は「届いた議論をそのまま全部取り込む → 本申請 → レビュー → 全部取り込んだ改善版を
申請 → …… を承認されるまで繰り返す」。**そして反映対象は届いた意見だけではなく、
議論の最中にこちらで見つけたものも同じ入力**である（オーナー 2026-09-06）。

作った理由は具体的である ——**1.1 の入力が 4 か所以上に散っていた**（`errata.md` /
`review-responses-meta.md` の「1.1 で足すかもしれない候補」/ `review-responses-clauses.md` の
「1.1 候補」/ `discussion-log.md` の帰結値）。**議論が終わってから 4 か所を回って集める手順は
必ず落とす。**

## How

- **errata が一次記録、この文書は索引。** 複製は drift するので `E<n>` だけを引く
- **Check 464 (BLOCKING)** が errata の全件の出現を強制する ——
  **落とすことを機械的に不可能にするのが、この文書の唯一の実効部分**
- 届いた指摘は `rounds/` へ無改変保存 → `discussion-log.md` で分解 → 帰結が「1.1 候補」に
  なったものを §3 へ

## Constraints

- **1.0 の本文・`spdx.xml`・`machine.json` は編集しない**（Check 453 が sha256 で止める）
- **版管理は併置**（`REVISION-PROTOCOL.md` §2）—— 1.0 は永久凍結し、1.1 は置き換えない
- Check 459 が索引（`LICENSES/README.md`）からの到達性を、Check 461c が `last-updated` を強制

## Change impact

`errata.md` に entry を足したら同じ `E<n>` をこの表にも足す（足さないと Check 464 が RED）。

## Audience-specific notes

- **審査者**: これは「指摘を受けたらどこへ行くか」の行き先である。**この文書の存在によって
  1.0 の本文は一切変わらない**
- **後任 AI**: 議論が終わってから集めようとしないこと。貯まる先を 1 つにしてあるのは、
  4 か所を回る手順が必ず落とすからである
