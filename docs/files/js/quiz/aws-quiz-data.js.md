---
file: js/quiz/aws-quiz-data.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 3-b) / js/quiz-renderer.js
---

# js/quiz/aws-quiz-data.js

## What

AWS 問題集 static data (819 行)。最大データセット。`questions` 配列を default export。closure-deps = none の純データ module。

## Why

Stage 3-b で Quiz データを domain 別に分割した 4 ファイルのうち最大。AWS サービスに関する問題を集約。

## How (usage)

```
main.js
  └─ import awsQuizData from './js/quiz/aws-quiz-data.js'
  └─ createQuizRenderer({ quizData: { aws: awsQuizData, ... } })
```

## Change impact

- question schema 変更 → 4 domain 全部 + quiz-renderer.js 同期
- 行数増加 → Check 52 budget (900 行) 超過時は budget 引き上げ判断

## Constraints

- **closure-deps = none** (純データ)
- **Check 47**: import/export bijection
- **Check 52**: 819 行 ≤ 900

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-data`, `quiz-domain-aws`, `largest-dataset`

### For human engineers (新卒レベル)
- AWS の問題集。問題追加はここに question object を追記

### For third parties
- 4 domain quiz data の中で最大規模 (819 行)
