---
file: js/pure-utils.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 2)
---

# js/pure-utils.js

## What

純ユーティリティ module。escape / tokenize / clamp / debounce / throttle / id 生成 等の副作用ゼロ関数群を export。Stage 2 で最初に抽出された安定 module。

## Why

main.js から最初に切り出した pure function 群。Stage 2 で抽出されてから現在まで安定 (factory pattern 化以前の純 named export 形式)。

## How (usage)

```
main.js / 各 factory module
  └─ import { escape, tokenize, clamp, debounce, throttle, ... } from './js/pure-utils.js'
       └─ 必要な関数を named import して呼ぶ
```

副作用ゼロ・外部依存ゼロなので、どこから呼んでも安全。

## Constraints

- **closure-deps = none**, factory pattern なし (純関数 named export)
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 400 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Change impact

- 既存関数 signature 変更 → 呼び出し側 (複数 factory) に影響

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-functions`, `stage-2-stable`

### For human engineers (新卒レベル)
- ここに「副作用ゼロ」「外部依存ゼロ」の関数を集約
- 新しい util を書くときも、まずここに置けるか検討

### For third parties
- Stage 2 で最初に抽出された安定 module。物理分割の安全な起点
