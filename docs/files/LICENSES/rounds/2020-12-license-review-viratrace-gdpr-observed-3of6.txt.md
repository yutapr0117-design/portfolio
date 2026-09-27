---
file: LICENSES/rounds/2020-12-license-review-viratrace-gdpr-observed-3of6.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #256
---

# LICENSES/rounds/2020-12-license-review-viratrace-gdpr-observed-3of6.txt

## What

**ViraTrace Public Source License の審査と、そこから分岐した「GDPR とライセンス条項」の議論**
（`license-review` / `license-discuss`・2018-08 と 2020-12・全 35 通）の **3/6 部**。
**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**データ保護法とライセンスの境界について、実務家（Chief Privacy Officer）の明確な一文が在る** ——
Roland Turner 氏 *"data protection law ... is about the legal obligations of organisations **in
control of personal data** ... **software licensors are not part of the picture**."*
**ACD-1.0 §1.5 が Covered Rights にデータ保護・privacy を含めず、§11.4 が
*"It reaches nothing else"* と述べていることの、外からの裏づけになる**（#256）。

**もう 1 つ** —— McCoy Smith 氏（Licensing Committee）が *"This violates **Freedom Zero**, which I
believe is, and have argued before is, **inherently, part of the OSD**"* と述べている。
**「OSD には書かれていないが内在する」という #248 / #251 の line の、委員からの実例である。**

## How

`https://lists.opensource.org/pipermail/license-{review,discuss}_lists.opensource.org/`
から**ブラウザ相当の UA** で取得（2026-09-27）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **6 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **束ね方は件名**（`ViraTrace` と `GDPR` を束ねてあり、2018 年の別議論を含む）。
- **ここに分析を書かない**（規約 2）。読みは `ACD-1.0.review-doctrine.md` §1.117 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: ViraTrace の提出は OSD 違反を複数指摘され、議論は `license-discuss` へ移された。
- **第三者**: 他人の提出についての議論であって、ACD-1.0 への応答ではない。
