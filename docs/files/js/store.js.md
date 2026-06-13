---
file: js/store.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-g) / js/storage.js
---

# js/store.js

## What

Store factory module (512 行)。`createStore({Storage})` を export。default data + load + validate + normalize + similarity 検索を含む。

## Why

main.js Stage 5-g で物理分割。サイトの persistence 系データ (settings / progress / records 等) を一元管理し、validation / normalization で schema drift を防ぐ。

## Constraints

- **factory pattern** (Check 56, 61), closure-deps = none
- **Check 47**: import/export bijection
- **Check 52**: 512 行 ≤ 600

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `data-store`, `schema-validation`

### For human engineers (新卒レベル)
- localStorage に保存されるユーザーデータの主管理者
- 古い schema との互換を normalize で吸収

### For third parties
- factory pattern + validation の組み合わせによる data store 実装
