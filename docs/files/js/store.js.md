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
- **id の一意化 (#1058)**: 取り込んだ tasks / todos / projects は `uniquifyIds` で id を一意にする。
  同じ id の項目が並ぶと **削除の `filter(t => t.id !== id)` が同 id を全て落として「1 件消したつもりが
  両方消える」**、逆に更新は `find` が先頭しか拾わずもう片方に効かない。DOM 側でも
  `task-delete-<id>` 等が重複し focus 復元が別カードを掴む。#154 の slug 一意化と同型で、方式も同じ
  「**後から来た方に連番を振る**」(先に来た方の id を変えると既存の参照が壊れる)。projects は
  **id → slug の順**で一意化する (slug の fallback が `p-${p.id}` なので順序が逆だと後追いになる)。
- **Check 364 / 417**: `(X || []).<throwing method>` 禁止 / untrusted 生値を `String()` へ直接渡さない。
  静的 Check が「書き方」を、`e2e/apps-settings-ingestion.spec.js` が「挙動」を固定する二層。

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `data-store`, `schema-validation`

### For human engineers (新卒レベル)
- localStorage に保存されるユーザーデータの主管理者
- 古い schema との互換を normalize で吸収

### For third parties
- factory pattern + validation の組み合わせによる data store 実装
