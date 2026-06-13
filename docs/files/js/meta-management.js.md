---
file: js/meta-management.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-k') / js/page-meta.js
---

# js/meta-management.js

## What

Meta Management factory module (201 行)。`createMetaManagement({deps})` を export。updateDocumentHead / announceRouteForAccessibility / injectRouteEntityAnchor / injectStructuredData / applyMeta facade を含む。

## Why

main.js Stage 5-k' (changelog 命名) で物理分割。ページ毎の SEO meta + AIO route entity anchor + JSON-LD route 注入を 1 モジュールに集約。

`5-k'` 命名は Stage 5-l (AIDK Rail) との衝突回避: PR #33 (Meta Management) と PR #37 (AIDK Rail) が同じ 5-l を使ったため、honest dating で前者を 5-k' とリネーム。

## How (usage)

```
main.js
  └─ import { createMetaManagement } from './js/meta-management.js'
  └─ const { applyMeta } = createMetaManagement({ PAGE_META, AUTHOR, SITE_CONFIG })
       └─ Router の change イベントで applyMeta(routeName) を呼ぶ
```

## Constraints

- **factory pattern** (Check 56, 61), closure-deps = none
- **Check 47**: import/export bijection
- **Check 52**: 201 行 ≤ 280

## Change impact

- meta 戦略変更 → js/page-meta.js (PAGE_META データ) と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `meta-injection`, `aio-route-anchor`

### For human engineers (新卒レベル)
- 各ルートに切り替わるたびに、title / og:* / JSON-LD route entity anchor を更新する
- AIO 上重要な役割 (route ごとに entity context を再宣言)

### For third parties
- SPA における meta 同期 + route-level entity anchor 注入の実装例
