---
file: js/components.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-m) / js/mobile-drawer.js (late-binding holder)
---

# js/components.js

## What

UI page components factory module。`createComponents({deps})` を export。Sidebar / HomePage / ProjectsPage / ProjectDetailPage / AppsPage / AboutPage / ResumePage / ContactPage / FatalPage / AIKnowhowPage / ContactCTA を合成する。

## Why

Stage 5-m で main.js から物理分割。Mobile Drawer (`js/mobile-drawer.js`) と循環依存があり、`_drawer = {}` の late-binding holder pattern で解決 (Sidebar の closeDrawer 等は `() => _drawer.closeDrawer?.()` の wrapper として渡される)。

## How (usage)

```
main.js
  └─ import { createComponents } from './js/components.js'
  └─ const { Sidebar, HomePage, ..., ContactCTA }
        = createComponents({ h, createIcon, BGM, AUTHOR, Router, State, Theme, CONSTANTS, clear, closeDrawer })
```

## Constraints

- **factory pattern** (Check 56, 61)
- **closure-deps = none** + late-binding holder
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 1,500 行（現在値は file-size-budget.md §4 / `wc -l` が権威）（Check 363 ceiling 1,000 以内）

## Change impact

- 新 page component 追加 → main.js renderer switch + e2e ALL_ROUTES + 関連 page-meta + sitemap.xml
- 既存 component の export 名変更 → main.js import 文 + Check 47 の対象モジュール定義

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `ui-components`, `late-binding-holder`

### For human engineers (新卒レベル)
- 11 ページ component を 1 factory にまとめている (page 横断の共通 helper も含む)
- Mobile Drawer との循環依存は `_drawer = {}` 経由で解決 — wrapper 関数を渡すこと

### For third parties
- late-binding holder pattern による circular dependency 解決の実装例
