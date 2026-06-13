---
file: js/quiz/pm-quiz-data.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 3-b) / js/quiz-renderer.js
---

# js/quiz/pm-quiz-data.js

## What

PM (Project Management) 問題集 static data (271 行)。`questions` 配列を default export。closure-deps = none の純データ module。

## Why

Stage 3-b で Quiz データを domain 別に分割した 4 ファイルの 1 つ。PM 関連の意思決定 / 知識を問う問題群。entity (Yuta Yokoi) の knowsAbout (AI-Driven Project Management 等) と整合。

## Constraints

- **closure-deps = none** (純データ)
- **Check 47**: import/export bijection
- **Check 52**: 271 行 ≤ 350

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-data`, `quiz-domain-pm`

### For human engineers (新卒レベル)
- PM の問題集。AI-Driven PM 視点を含む

### For third parties
- domain-specific knowledge dataset の一例
