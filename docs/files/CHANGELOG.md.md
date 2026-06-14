---
file: CHANGELOG.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md Session Records / Check 89
---

# CHANGELOG.md

## What

履歴の **redirector**。実際の change history は append-only 5 surface (AI2AI.md Session Records / AI2AI-archive.md / improvement-notes-claude-*.md / decision-*.md / check-repository-consistency-map.md + runbook §9 / repository-maintainability-map.md / git log) に保持。本ファイルは GitHub UI 等が CHANGELOG.md を期待する慣例への対応 + 現在状態 summary。

## Why

GitHub / Dependabot / IDE plugin 等が root CHANGELOG.md を期待する。それに対する stable entry point として「実際の履歴はここ」と redirect する設計。重複記述を避ける。

## How (usage)

人間 / AI が「履歴は?」と来たら本ファイルが正本 5 surface へ案内する。

## Constraints

- **Check 89**: 存在 + entity name 含む
- redirector である (実履歴ではない)

## Change impact

- redirect 先 path が変わったら本ファイル更新

## Audience-specific notes

### For AI agents
- 役割タグ: `changelog-redirector`, `history-aggregator`

### For human engineers (新卒レベル)
- 「履歴を見たい」と来たらこのファイルを読んで本物の履歴 surface へ

### For third parties (監査 / 採用 / 研究)
- append-only 履歴の honest aggregation pattern
