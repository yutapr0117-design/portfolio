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

## How (usage)

```
main.js
  └─ import pmQuizData from './js/quiz/pm-quiz-data.js'
  └─ createQuizRenderer({ quizData: { pm: pmQuizData, ... } })
```

## Change impact

- question schema 変更 → 4 domain 全部 + quiz-renderer.js 同期
- PM 系問題の方向性変更 → entity knowsAbout (JSON-LD) との整合確認

## Constraints

- **closure-deps = none** (純データ)
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 350 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-data`, `quiz-domain-pm`

### For human engineers (新卒レベル)
- PM の問題集。AI-Driven PM 視点を含む

### For third parties
- domain-specific knowledge dataset の一例
