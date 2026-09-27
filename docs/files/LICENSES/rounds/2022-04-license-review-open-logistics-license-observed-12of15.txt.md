---
file: LICENSES/rounds/2022-04-license-review-open-logistics-license-observed-12of15.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #254
---

# LICENSES/rounds/2022-04-license-review-open-logistics-license-observed-12of15.txt

## What

**Open Logistics License の承認審査**（`license-review`・2022-04〜2023-03・全 106 通）の
**12/15 部**。**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**理事会が承認の際に、準拠法条項について自分の立場を述べている** ——
*"The Board did so with the comment that **it does not believe that choice of law provisions are
necessary or advisable in open source licenses**."*（2023-03-18）。
**ACD-1.0 §15.7 は準拠法を置いていない**（#254）。

**そして、法律事務所が起草に同伴し社内弁護士が査読した提出でも、承認まで 11 か月・3 版を要した**
（v1.1 → v1.2 → v1.3）。**Bradley M. Kuhn 氏が vanity の判定基準を 2 段で述べている** ——
*"a **widespread need for many different FOSS communities**, *and* ... **wholly unserved by all
existing FOSS licenses**"*（#255）。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/`
から**ブラウザ相当の UA** で取得（2026-09-27）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **15 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **束ね方は件名**（v1.1 / v1.2 / v1.3 を通して束ねてある）。
- **ここに分析を書かない**（規約 2）。読みは `ACD-1.0.review-precedents.md` §1.116 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: 結末は **2023-03-19 の理事会で承認**（special purpose category）。
- **第三者**: 他人の提出についての議論であって、ACD-1.0 への応答ではない。
