---
file: docs/incident-artifacts/decision-v80-maintainability-roadmap.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md / Check 42
---

# docs/incident-artifacts/decision-v80-maintainability-roadmap.md

## What

v80+ maintainability roadmap の意思決定記録 (Stage 0〜5 計画 / 危険度別ゲート / Playwright baseline 前提)。

## Why

「いきなり分割しない、map を先に作る」原則の出発点。

## Constraints

- **Check 42**: `decision-*.md`

## How (usage) / Change impact

過去判断参照 / append-only。


## Change impact

- append-only: 既存内容は変更しない
- 新規 increment 時のみ新ファイル追加

## Audience-specific notes

### For AI agents
- 役割タグ: `decision-record`, `roadmap-origin`

### For human engineers (新卒レベル)
- main.js 分割計画の出発点

### For third parties
- 大規模 refactor の roadmap 設計例
