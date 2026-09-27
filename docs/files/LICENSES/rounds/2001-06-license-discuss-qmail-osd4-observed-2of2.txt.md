---
file: LICENSES/rounds/2001-06-license-discuss-qmail-osd4-observed-2of2.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-26
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #251
---

# LICENSES/rounds/2001-06-license-discuss-qmail-osd4-observed-2of2.txt

## What

全 21 通の **2/2 部**。**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**OSD 3 の後半（*"to be distributed under the same terms as the license of the original software"*）が、実際に判定の決め手として使われている例。** Moen 氏 *"OSD clause #3, immediately preceding, strikes me as disambiguating this."*

**そして条件一般について** —— Cowan 氏 *"a claim that 'X must allow Y' is satisfied by a statement by X that 'Y is allowed under conditions Z' **can't be true in general, since the conditions Z can be arbitrarily restrictive**."*（#251）

## How

`https://lists.opensource.org/pipermail/license-{review,discuss}_lists.opensource.org/`
から**ブラウザ相当の UA** で取得（2026-09-26）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **2 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **ここに分析を書かない**（規約 2）。読みは `LICENSES/ACD-1.0.against.md #251` へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: 束ね方は件名で、主題ごとに分けていない。
- **第三者**: これは他人の提出・他人の相談についての議論であって、ACD-1.0 への応答ではない。
