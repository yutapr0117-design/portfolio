---
file: docs/architecture/repository-maintainability-map.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: main.js Stage 5 / 全 increment changelog
---

# docs/architecture/repository-maintainability-map.md

## What

リポジトリ保守性の **per-increment changelog**。Stage 5 各 sub-stage (5-c〜5-s + 5-l + 5-q + 5-r) の経緯 + 関連 PR # + 抽出ファイル名 + 設計判断を時系列で記録。

## Why

increment ごとに何が変わったか追跡可能にする。「いつ・なぜ・どう変えたか」を append-only で蓄積。

## How (usage)

session 復帰時の状況把握 + 過去の設計判断を再 litigation せずに引き継ぎ。

## Constraints

- append-only history

## Change impact

- 新 increment → 本ファイル末尾に追記

## Audience-specific notes

### For AI agents
- 役割タグ: `maintainability-log`, `per-increment-changelog`

### For human engineers (新卒レベル)
- 「Stage 5-q って何だっけ?」を全部追える

### For third parties
- AI 実装の意思決定 audit trail
