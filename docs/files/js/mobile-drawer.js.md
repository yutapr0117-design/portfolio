---
file: js/mobile-drawer.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-q) / js/components.js (circular dep)
---

# js/mobile-drawer.js

## What

Mobile Drawer factory module。`createMobileDrawer({deps})` を export。syncMobileDrawer / secureExternalLinks / focus trap / body scroll lock / openDrawer / closeDrawer を含む。

## Why

main.js Stage 5-q で物理分割。`js/components.js` と循環依存を持つため、`_drawer = {}` の late-binding holder で解決。

## How (usage)

```
main.js
  └─ import { createMobileDrawer } from './js/mobile-drawer.js'
  └─ const drawer = createMobileDrawer({ CONSTANTS, clear, Sidebar })
  └─ Object.assign(_drawer, drawer)  // late-binding holder へ wire
```

## Constraints

- **factory pattern** (Check 56, 61)
- **late-binding holder**: 循環依存解決
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 280 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Change impact

- API 名変更 → js/components.js の `_drawer = {}` holder への wire 変更
- focus trap / inert 制御変更 → mobile UI accessibility テストへの影響

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `mobile-drawer`, `late-binding-holder`
- accessibility: focus trap + body scroll lock + inert attribute 制御

### For human engineers (新卒レベル)
- mobile の hamburger menu (drawer) を開閉する
- focus trap / scroll lock / inert は accessibility (WCAG 2.4.3 等) 要件

### For third parties
- accessible mobile drawer の実装例
