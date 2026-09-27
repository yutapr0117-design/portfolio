---
file: LICENSES/rounds/2017-11-license-review-unicode-data-files-observed-1of3.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #259
---

# LICENSES/rounds/2017-11-license-review-unicode-data-files-observed-1of3.txt

## What

**Unicode の 2 つの承認**（*Unicode Data Files and Software License* の legacy 承認・2017-11 提出
→ 2018-09 承認 / *Unicode License v3*・2023-08 提出 → 2023-11-17 承認）の議論、全 16 通の
**1/3 部**。**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**OSI は「data files」を主題に明記したライセンスを 2 度承認している**（どちらも
Special Purpose / redundant のカテゴリつき）。**B15（主題適格）にとって、
フォント（§1.110）に続く 2 つ目の counterweight である**（#259）。

**そして 2023 年の提出は「一般化」を目的として明記し、
著作権表示を *"fill in the blanks"* にした本文で承認されている** ——
*"to **genericize it so that it may be used by entities other than the Unicode Consortium**"*。
**提出パケット §4b（提出者専用でないこと）と §16.1 の 1 欄の雛形を支える先例**（#260）。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/`
から**ブラウザ相当の UA** で取得（2026-09-27）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **3 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **束ね方は件名**で、**2017-11 と 2023-08 の 2 つの審査にまたがる。**
- **ここに分析を書かない**（規約 2）。読みは `ACD-1.0.review-outcomes.md` §1.119 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: 旧版は **superseded** と記され、新版は **Special Purpose** カテゴリで承認された。
- **第三者**: 他人の提出についての議論であって、ACD-1.0 への応答ではない。
