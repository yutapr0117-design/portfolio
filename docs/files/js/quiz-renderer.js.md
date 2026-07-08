---
file: js/quiz-renderer.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-o) / js/quiz/*.js
---

# js/quiz-renderer.js

## What

Quiz Renderer factory module。`createQuizRenderer({deps})` を export。QuizPage + 4 domain (architecture / aws / pm / quality) の lookup table を含む。

## Why

main.js Stage 5-o で物理分割。Quiz 機能の renderer logic を独立 module へ。4 domain のデータは `js/quiz/<domain>-quiz-data.js` に分散 (Stage 3-b 抽出)、quiz-renderer がそれらを統合 render する。

## How (usage)

```
main.js
  └─ import { createQuizRenderer } from './js/quiz-renderer.js'
  └─ import architectureQuizData from './js/quiz/architecture-quiz-data.js'
  └─ ... + 3 domains
  └─ const QuizPage = createQuizRenderer({ h, createIcon, Toast, Router, State, awsQuizData, pmQuizData, qualityQuizData, architectureQuizData })
```

Router が `#/quiz` route に到達したら QuizPage を render。

## Change impact

- 新 domain 追加 → js/quiz/<domain>-quiz-data.js 新設 + quiz-renderer の lookup table 拡張 + main.js import
- question schema 変更 → 4 domain data 全部に同期適用

## Constraints

- **factory pattern** (Check 56, 61), closure-deps = none
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 350 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `quiz-renderer`, `4-domain-lookup`

### For human engineers (新卒レベル)
- Quiz データは 4 ファイル (`js/quiz/*.js`) に分散
- Renderer はここに集約、データだけ別 module というのが Stage 5 の方針

### For third parties
- domain-driven data + renderer 分離の実装例
