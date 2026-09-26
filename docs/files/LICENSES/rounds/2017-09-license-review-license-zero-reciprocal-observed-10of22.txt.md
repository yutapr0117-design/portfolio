---
file: LICENSES/rounds/2017-09-license-review-license-zero-reciprocal-observed-10of22.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-26
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #248
---

# LICENSES/rounds/2017-09-license-review-license-zero-reciprocal-observed-10of22.txt

## What

**License Zero Reciprocal Public License (L0-R) の承認審査**
（`license-review` / `license-discuss`・2017-09〜2018-12・全 220 通）の **10/22 部**。
**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**記録の中で、単独の起草者による審査がいちばん長く続いた例**（15 か月・220 通）で、
**結末は「委員長が却下を勧告 → 提出者が事実上取り下げ → 理事会は決定せず」**である。

**ここに、OSD に書かれていない審査基準が、参加者自身の言葉で列挙されている** ——
Rick Moen 氏 *"perception that the license is a **vanity license or duplicative**, that it is
**needlessly specific to one business entity**, that it is **unjustifiably opaque or ambiguous in
its wording**, that it **was not drafted with a lawyer**"*、
Luis Villa 氏（元理事）*"**OSI approval is a political game, not an actual objective test**"*、
John Cowan 氏 *"The OSI approves OSD-conforming licenses **only if it believes that they further
the goals of OSI**."*（#248）

## How

`https://lists.opensource.org/pipermail/license-{review,discuss}_lists.opensource.org/`
から**ブラウザ相当の UA** で取得（2026-09-26）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **22 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **束ね方は件名**（`License Zero` / `L0-R` / `resolving ambiguities`）で、
  スレッドは途中で件名を変えている。**1 本の連続した往復として読まないこと。**
- **ここに分析を書かない**（規約 2）。読みは `ACD-1.0.review-venue.md` §1.113 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: 主題（maximalist copyleft）は ACD とは遠い。**還元したのは手続きと基準についてだけである。**
- **第三者**: これは他人の提出についての議論であって、ACD-1.0 への応答ではない。
