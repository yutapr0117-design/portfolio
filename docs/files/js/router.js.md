---
file: js/router.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5) / js/state.js / js/aidk-rails.js (RouteState)
---

# js/router.js

## What

Hash-based SPA ルーター module (175 行)。`Router` object を named export。`window.location.hash` を観測して route change event を発火する Vanilla 実装。

## Why

外部 router library (React Router 等) を C1 で禁止しているため Vanilla 実装。Hash-based の理由は GitHub Pages の static hosting が history fallback を持たないため。

## Constraints

- **C1 Boring Technology**: 外部 router library 禁止
- **C2 IIFE**: 内部論理は IIFE で隔離
- **closure-deps = none**
- **Check 47**: import/export bijection
- **Check 52**: 175 行 ≤ 250

## Change impact

- route 追加 → main.js renderer switch (Check 58) + e2e ALL_ROUTES (Check 58) + sitemap.xml `<loc>` + js/page-meta.js

## Audience-specific notes

### For AI agents
- 役割タグ: `spa-router`, `hash-based`, `c1-vanilla`

### For human engineers (新卒レベル)
- hash-based なので URL は `/portfolio/#/route-name` 形式
- ブラウザ back/forward に対応 (popstate / hashchange event)

### For third parties
- 外部 library なしの SPA router 実装例 (Boring Technology の reasonable form)
