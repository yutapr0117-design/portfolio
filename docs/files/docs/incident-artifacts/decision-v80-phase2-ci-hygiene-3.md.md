---
file: docs/incident-artifacts/decision-v80-phase2-ci-hygiene-3.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: Check 40 / Check 42
---

# docs/incident-artifacts/decision-v80-phase2-ci-hygiene-3.md

## What

CI hygiene #3 (CSS lint 実行 path: local-binary preferred + npx fallback / Check 40 導入) の意思決定記録。

## Constraints / How (usage) / Change impact / Why

Check 42 命名規約 / 過去判断参照 / append-only / lint 実行 path の安定化。


## Why

当該 increment の意思決定 / 学びを後続セッション向けに保持する (append-only)。


## How (usage)

過去判断・学びの参照源。新規 session 復帰時に文脈再構成のために読む。


## Change impact

- append-only: 既存内容は変更しない
- 新規 increment 時のみ新ファイル追加

## Audience-specific notes

### For AI agents
- 役割タグ: `decision-record`, `ci-hygiene-3`, `lint-execution-path`

### For human engineers (新卒レベル)
- `node_modules/.bin/stylelint` を優先する根拠

### For third parties
- CI 実行 path 設計判断
