---
file: js/brand.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-22
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-f) / js/storage.js
---

# js/brand.js

## What

Brand manager factory module。`createBrand(Storage)` を export（位置引数で storage instance を受け取る）。primary palette / font switcher を管理する factory。

## Why

main.js から Stage 5-f で物理分割。brand (palette / font) 設定を localStorage 経由で永続化するため、Safe Storage wrapper (`js/storage.js`) を注入する設計。

## How (usage)

```
main.js
  └─ import { createBrand } from './js/brand.js'
  └─ const Brand = createBrand(Storage)   // 位置引数 (storage instance・destructure ではない)
       └─ Brand.init()          // 保存済みブランドを初期適用
       └─ Brand.set('classic')  // ブランド切替 (永続化)
       └─ Brand.get()           // 現在ブランド
       └─ Brand.KEY             // localStorage キー定数
```

## Constraints

- **factory pattern** (Check 56, 61)
- **closure-deps = none** (引数で Storage を注入)
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 120 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Change impact

- palette 選択肢追加 → style.css の CSS 変数定義 + brand.js の applyPalette 範囲

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `brand-manager`, `closure-deps-none`

### For human engineers (新卒レベル)
- 「brand」はサイトの primary 色 / フォントなどの見た目アイデンティティ
- localStorage の Safe wrapper を経由するので、quota over や private mode でも安全

### For third parties
- 小さく集中した factory module の典型例 (65 行)
