---
file: js/store.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-22
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-g) / js/storage.js
---

# js/store.js

## What

Store factory module。`createStore({ AUTHOR, CONSTANTS, Storage, generateId, deepClone, slugify, sanitizeUrl, clamp })` を export。default data + load + validate + normalize + similarity 検索を含む。

## Why

main.js Stage 5-g で物理分割。サイトの persistence 系データ (settings / progress / records 等) を一元管理し、validation / normalization で schema drift を防ぐ。

## How (usage)

```
main.js
  └─ import { createStore } from './js/store.js'
  └─ const Store = createStore({ AUTHOR, CONSTANTS, Storage, generateId, deepClone, slugify, sanitizeUrl, clamp })
       └─ Store.load()                        // localStorage から読み込み + 正規化
       └─ Store.createDefaultStore()          // 既定ストア生成
       └─ Store.validateAndNormalize(data)    // 外部 ingestion の正規化 (総関数・load/import/cross-tab/snapshot が通る choke point)
       └─ Store.autoRelatedCandidates(target, projects) // 類似度ベースの関連プロジェクト推薦
```

## Change impact

- default data schema 変更 → validate / normalize logic + 既存ユーザーデータの migration
- similarity アルゴリズム変更 → 検索 UI の結果が変わる

## Constraints

- **factory pattern** (Check 56, 61), closure-deps = none
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 600 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `data-store`, `schema-validation`

### For human engineers (新卒レベル)
- localStorage に保存されるユーザーデータの主管理者
- 古い schema との互換を normalize で吸収

### For third parties
- factory pattern + validation の組み合わせによる data store 実装
