---
file: docs/incident-artifacts/decision-v80-phase2-ci-hygiene.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: Check 42
---

# docs/incident-artifacts/decision-v80-phase2-ci-hygiene.md

## What

Phase 2-A CI hygiene 起点 (package.json/lockfile/npm ci 中央管理 + ESLint vacuous-gate fix) の意思決定記録。

## Constraints

- **Check 42**: `decision-*.md`

## How (usage) / Change impact

過去判断参照 / append-only。

## Why

CI が「動いてるが本当は何も検査していなかった」class のバグを構造的に閉じる出発点。

## Audience-specific notes

### For AI agents
- 役割タグ: `decision-record`, `ci-hygiene-origin`

### For human engineers (新卒レベル)
- 「lint OK だけど実は何も lint してなかった」class 防止の出発

### For third parties
- vacuous gate 防止の出発記録
