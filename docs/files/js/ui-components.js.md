---
file: js/ui-components.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 4)
---

# js/ui-components.js

## What

UI building blocks module (303 行)。`h` (hyperscript) / `createIcon` (SVG icon factory) / Toast notification / BGM control 等の low-level builder を named export。Stage 4 安定 module。

## Why

main.js Stage 4 で物理分割。DOM builder と SVG icon と Toast を 1 module に集約して、各 page component から使う共通インフラ。

## Constraints

- **closure-deps = none**, factory pattern なし (Stage 4 時点では純 named export)
- **Check 47**: import/export bijection
- **Check 52**: 303 行 ≤ 400

## Audience-specific notes

### For AI agents
- 役割タグ: `ui-builders`, `dom-helpers`, `stage-4-stable`

### For human engineers (新卒レベル)
- `h('div', {class: 'card'}, ['Hello'])` のような hyperscript で DOM を組む
- 「React の代わり」と思って良い (ただし virtual DOM ではない)

### For third parties
- Boring Technology 哲学の hyperscript 実装。React なしで宣言的 DOM 構築する例
