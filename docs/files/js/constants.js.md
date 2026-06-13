---
file: js/constants.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-d)
---

# js/constants.js

## What

実行時定数 module (88 行)。STORAGE_KEY / LIMITS / timing / DEBUG / TAB_ID を export。closure-deps = none の純粋データ module。

## Why

main.js から Stage 5-d で物理分割。実行時の定数を 1 箇所に集約して、複数 factory が同じ truth を参照する構造に整理。

## How (usage)

```
main.js
  └─ import { CONSTANTS, STORAGE_KEY, ... } from './js/constants.js'
       └─ 各 factory に注入: createXxx({ CONSTANTS, ... })
```

## Constraints

- **closure-deps = none** (純粋データ)
- **Check 47**: import/export bijection
- **Check 52**: 88 行 ≤ 150

## Change impact

- 定数値変更 → 参照する全 factory + 関連 e2e テスト

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-data`, `constants`, `closure-deps-none`

### For human engineers (新卒レベル)
- グローバル変数の代わりに、ここに集約 → factory に引数注入する
- 「Magic Number」を排除する場所

### For third parties
- pure data module の最小例
