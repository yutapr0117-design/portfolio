---
file: LICENSES/ACD-1.3.txt
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人, 後任 AI
last-updated: 2026-10-25
canonical-ref: LICENSES/ACD-1.3-CHANGELIST.md (1.2 からの全変更・確定の判断・草案ヘッダの逐語) / LICENSES/FROZEN.md (sha256 pin) / LICENSE (適用の宣言)
---

# LICENSES/ACD-1.3.txt

## What

**ACD-1.3 の確定テキスト（2026-10-25 凍結）で、このリポジトリに適用している版。** 冒頭は FROZEN TEXT / NOT SUBMITTED FOR APPROVAL と述べ、`FROZEN.md` が sha256 で pin する（Check 453）。**次版の作業場は `ACD-1.4-DRAFT.txt`。**

## Why

オーナーの依頼（2026-10-25）「1.3に大きな不備が無く、リポジトリに適用可能な状態なら適用してください」による。1.2 の凍結前検証の持ち越し 5 件と題名行の誤りを閉じた版（errata E35〜E38・E24 の追記）。

## How

条文は確定直前の草案と同一。**冒頭は適用状態を述べない形にした** —— 凍結済みの 1.2 の冒頭は「このリポジトリを覆うのはまだ ACD-1.0」と述べ、この適用で偽になったが直せない。変わりうる事実は凍結テキストに書かず、`LICENSE` が述べる。

## Constraints

- **本文は 1 byte も変えない**（Check 453）。欠陥は `ACD-1.4-DRAFT.txt` で直し、errata に記録する。
- 純 ASCII。

## Change impact

- 条番号は 1.2（＝1.1）に従う（1.0 とは §1 と §15 以降が違う）。
- 機械可読の記述子は `ACD-1.3.machine.json`（Check 451d / 468h）。

## Audience-specific notes

- **審査者向け**: `license-discuss` で議論の対象として投稿したのは 1.0（凍結のまま）。このリポジトリが適用しているのは 1.3。
