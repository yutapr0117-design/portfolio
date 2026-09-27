---
file: LICENSES/rounds/2019-05-license-review-master-console-withdrawn-observed-2of2.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #261
---

# LICENSES/rounds/2019-05-license-review-master-console-withdrawn-observed-2of2.txt

## What

全 15 通の **2/2 部**。**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**非弁護士の起草に対する、記録上いちばん鋭い警告が在る** —— Bruce Perens 氏 *"I have previously worked on the case **Jacobsen v. Katzer**, in which an Open Source developer paid **tens of thousands of dollars in losses and five years of hardship in court** because he relied on the Artistic License ... rather than a license from an attorney. ... it is an **active disservice to the programmers of the world** ... **So, please get a lawyer to write a license for you.**"*

**そして委員長が示した経路が、我々がいま辿っている経路そのものである** —— *"withdraw the license for now ... start a thread on **license-discuss** ... and resubmitting"*（#262）。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/`
から**ブラウザ相当の UA** で取得（2026-09-27）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **2 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **ここに分析を書かない**（規約 2）。読みは `ACD-1.0.review-outcomes.md` §1.120 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: 本文は非 ASCII を多く含み、アーカイブの文字化けもそのまま保存してある。
- **第三者**: 他人の提出についての議論であって、ACD-1.0 への応答ではない。
