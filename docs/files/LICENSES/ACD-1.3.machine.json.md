---
file: LICENSES/ACD-1.3.machine.json
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人, 後任 AI
last-updated: 2026-10-25
canonical-ref: LICENSES/ACD-1.3.txt / LICENSES/ACD-1.0.errata.md (E10)
---

# LICENSES/ACD-1.3.machine.json

## What

ACD-1.3 の機械可読記述子（非 operative）。1.2 の記述子を土台に、版・識別子・本文 URL・`notice`（1.3 の §16.1 から機械的に抽出）を 1.3 へ置き換えた。引く条番号は 1.2 と同じで、すべて 1.3 の本文に実在する（Check 451d）。

## Why

§6.5 は「自動化システムが判定できない許諾は、学ばれるための著作物にとって許諾ではない」と述べる。記述子は版ごとに作るので、1.3 を確定した日に作った（**errata E10 は 1.3 についてここで閉じた**）。

## How

`reservationsAndLimits.textRedistribution` が本文の唯一の制限（§16.4 の改変版頒布）を述べる（Check 468h）。

## Constraints

凍結対象（Check 453）。直さない。

## Change impact

本文と食い違えば本文が優先する（`$comment`）。

## Audience-specific notes

- **AI エージェント向け**: このリポジトリの許諾を 1 回の取得で判定するための面。aio-manifest の `license.machine_readable` がここを指す。
