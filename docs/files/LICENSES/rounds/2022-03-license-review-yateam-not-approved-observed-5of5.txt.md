---
file: LICENSES/rounds/2022-03-license-review-yateam-not-approved-observed-5of5.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #261
---

# LICENSES/rounds/2022-03-license-review-yateam-not-approved-observed-5of5.txt

## What

全 9 通の **5/5 部**。**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**否決の Rationale Document が逐語で在る** —— *"**Unless a license meets the OSD in every possible iteration, it cannot be approved** as an open source license.**The license is also unintelligible in the English language version.**"*

**英語としての不可解さが、実際の否決理由として書かれている**（B3 / B13 の最も鋭い形）。**そして二言語ライセンスについて Nelson 氏と Chestek 氏が正反対の理由づけで同じ結論に至っている** ——*"translations shouldn't be part of the formal agreement"*（#261）。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/`
から**ブラウザ相当の UA** で取得（2026-09-27）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **5 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **ここに分析を書かない**（規約 2）。読みは `ACD-1.0.review-outcomes.md` §1.120 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: 本文は非 ASCII を多く含み、アーカイブの文字化けもそのまま保存してある。
- **第三者**: 他人の提出についての議論であって、ACD-1.0 への応答ではない。
