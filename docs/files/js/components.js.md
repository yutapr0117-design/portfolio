---
file: js/components.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-22
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-m) / js/mobile-drawer.js (late-binding holder)
---

# js/components.js

## What

UI page components factory module。`createComponents({deps})` を export し、**Sidebar / AppsPage / AboutPage / ResumePage / ContactPage / FatalPage / ContactCTA の 7 つ**を合成する。bloat-reduction で HomePage → `js/home-page.js` / ProjectsPage → `js/projects-page.js` / ProjectDetailPage → `js/project-detail-page.js` / AIKnowhowPage → `js/ai-knowhow-page.js` を個別葉モジュールへ分離済（1,335→454 行）ゆえ、それら 4 ページは本 module には含まれない。

## Why

Stage 5-m で main.js から物理分割。Mobile Drawer (`js/mobile-drawer.js`) と循環依存があり、`_drawer = {}` の late-binding holder pattern で解決 (Sidebar の closeDrawer 等は `() => _drawer.closeDrawer?.()` の wrapper として渡される)。

## How (usage)

```
main.js
  └─ import { createComponents } from './js/components.js'
  └─ const { Sidebar, AppsPage, AboutPage, ResumePage, ContactPage, FatalPage, ContactCTA }
        = createComponents({ h, createIcon, BGM, AUTHOR, Router, State, Theme, CONSTANTS, clear, closeDrawer })
  // HomePage / ProjectsPage / ProjectDetailPage / AIKnowhowPage は個別葉 (js/home-page.js 等) で生成
```

## Constraints

- **factory pattern** (Check 56, 61)
- **closure-deps = none** + late-binding holder
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 600 行（現在値は file-size-budget.md §4 / `wc -l` が権威）（Check 363 ceiling 1,000 以内）

## Change impact

- 新 page component 追加 → main.js renderer switch + e2e ALL_ROUTES + 関連 page-meta + sitemap.xml
- 既存 component の export 名変更 → main.js import 文 + Check 47 の対象モジュール定義

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `ui-components`, `late-binding-holder`

### For human engineers (新卒レベル)
- 7 ページ component を 1 factory にまとめている (page 横断の共通 helper も含む)。かつては 11 だったが肥大化解消で Home/Projects/ProjectDetail/AIKnowhow を別 module へ切り出した
- Mobile Drawer との循環依存は `_drawer = {}` 経由で解決 — wrapper 関数を渡すこと

### For third parties
- late-binding holder pattern による circular dependency 解決の実装例
