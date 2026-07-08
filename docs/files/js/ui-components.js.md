---
file: js/ui-components.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 4)
---

# js/ui-components.js

## What

UI building blocks module。`h` (hyperscript) / `createIcon` (SVG icon factory) / Toast notification / BGM control 等の low-level builder を named export。Stage 4 安定 module。

## Why

main.js Stage 4 で物理分割。DOM builder と SVG icon と Toast を 1 module に集約して、各 page component から使う共通インフラ。

## How (usage)

```
main.js / 各 factory module
  └─ import { h, createIcon, Toast, BGM } from './js/ui-components.js'
  └─ const el = h('div', {class: 'card'}, ['Hello', h('br'), 'World'])
  └─ const icon = createIcon('chevron-down', 24)
  └─ Toast.show('Saved!', { type: 'success' })
  └─ BGM.play() / BGM.pause()
```

## Change impact

- `h()` シグネチャ変更 → 全 page component (1,000+ 箇所) に影響
- SVG icon 追加 → createIcon の lookup table 拡張 + assets/icons.svg sprite 更新

## Constraints

- **closure-deps = none**, factory pattern なし (Stage 4 時点では純 named export)
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 400 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Audience-specific notes

### For AI agents
- 役割タグ: `ui-builders`, `dom-helpers`, `stage-4-stable`

### For human engineers (新卒レベル)
- `h('div', {class: 'card'}, ['Hello'])` のような hyperscript で DOM を組む
- 「React の代わり」と思って良い (ただし virtual DOM ではない)

### For third parties
- Boring Technology 哲学の hyperscript 実装。React なしで宣言的 DOM 構築する例
