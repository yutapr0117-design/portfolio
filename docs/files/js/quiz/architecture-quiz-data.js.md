---
file: js/quiz/architecture-quiz-data.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 3-b) / js/quiz-renderer.js
---

# js/quiz/architecture-quiz-data.js

## What

Architecture (v29 意思決定) 問題集 static data (137 行)。`questions` 配列を default export。closure-deps = none の純データ module。

## Why

Stage 3-b で Quiz データを domain 別に分割した 4 ファイルの 1 つ。`js/quiz-renderer.js` (Stage 5-o factory) が runtime でこれらを統合 render する。

## Constraints

- **closure-deps = none** (純データ)
- **Check 47**: import/export bijection
- **Check 52**: 137 行 ≤ 250

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-data`, `quiz-domain-architecture`

### For human engineers (新卒レベル)
- v29 アーキテクチャ意思決定の問題集
- 問題を追加するときはここに question object を追記

### For third parties
- domain-driven data split (Stage 3-b) の実装例
