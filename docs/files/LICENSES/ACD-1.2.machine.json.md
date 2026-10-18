---
file: LICENSES/ACD-1.2.machine.json
audience: 採用者・自動化システム・監査人・後任 AI
last-updated: 2026-10-18
canonical-ref: LICENSES/ACD-1.2.txt (operative な本文・記述子と食い違えば本文が優先) / LICENSES/ACD-1.1.machine.json (同じ構造の前版)
---

# LICENSES/ACD-1.2.machine.json

## What

**ACD-1.2 の機械可読記述子（非 operative）。** 各事実が根拠の条項番号を引く。`textRedistribution`（§16.4）を持つ（errata E10 は版ごとに閉じ直す）。

## Why

ACD §6.5「自動化システムが判定できない許諾は、学習されるための著作物にとっては許諾ではない」を自分に当てるため。

## How

1.1 の記述子を土台に、版・識別子・本文 URL・`notice`（1.2 の §16.1 から機械的に抽出）を 1.2 のものへ置き換えた。引く 34 件の条項はすべて 1.2 の本文に実在する。

## Constraints

- **Check 451d** が「引く条項が本文に在る / notice が §16.1 と一致 / text が自分の版を指す / version と spdxId が file 名と一致」を BLOCKING で見る。
- **Check 468h** が `textRedistribution.clause == 16.4` を見る。
- 凍結対象（Check 453）。

## Change impact

本文の条番号を変えた版では、この記述子ではなく次版の記述子を作る。

## Audience-specific notes

**採用者**: そのまま複製してよい（`$comment`）。
