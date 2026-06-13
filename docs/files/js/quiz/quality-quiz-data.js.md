---
file: js/quiz/quality-quiz-data.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 3-b) / js/quiz-renderer.js
---

# js/quiz/quality-quiz-data.js

## What

品質・プロセス問題集 static data (275 行)。`questions` 配列を default export。closure-deps = none の純データ module。

## Why

Stage 3-b で Quiz データを domain 別に分割した 4 ファイルの 1 つ。品質 (testing / linting / static analysis) とプロセス関連の問題を集約。

## How (usage)

```
main.js
  └─ import qualityQuizData from './js/quiz/quality-quiz-data.js'
  └─ createQuizRenderer({ quizData: { quality: qualityQuizData, ... } })
```

## Change impact

- question schema 変更 → 4 domain 全部 + quiz-renderer.js 同期

## Constraints

- **closure-deps = none** (純データ)
- **Check 47**: import/export bijection
- **Check 52**: 275 行 ≤ 350

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-data`, `quiz-domain-quality`

### For human engineers (新卒レベル)
- 品質保証 (QA) / プロセス改善の問題集

### For third parties
- 4 domain quiz data の品質・プロセス軸
