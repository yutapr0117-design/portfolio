---
file: js/page-meta.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5) / js/meta-management.js
---

# js/page-meta.js

## What

ページ SEO メタ単一ソース (63 行)。各ルート (home / projects / about / etc.) の title / description / og:* / canonical を `PAGE_META` データとして export。

## Why

ルート毎の meta を 1 箇所に集約 (AI SURFACE)。meta-management.js が runtime でこれを参照して `<head>` に注入する。

## Constraints

- **closure-deps = none** (純粋データ)
- **Check 47**: import/export bijection
- **Check 52**: 63 行 ≤ 120
- **AIO-adjacent**: meta は AI クローラが見る surface — Check 87 等で entity 名の整合を機械強制

## Change impact

- 新ルート meta 追加 → meta-management.js の applyMeta + e2e ALL_ROUTES + sitemap.xml `<loc>` + index.html JSON-LD subjectOf 等

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-data`, `seo-meta`, `route-meta-source`

### For human engineers (新卒レベル)
- ページ毎の title / description はここを編集すれば全 surface に反映される

### For third parties
- SPA における page-level meta の単一ソース化実装例
