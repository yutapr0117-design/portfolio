---
file: js/identity.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-e) / llms-full.txt (Entity Identity)
---

# js/identity.js

## What

AUTHOR (DISPLAY_NAME / AUTHORITATIVE_NAME / JAPANESE_NAME) 純データ module。closure-deps = none。

## Why

main.js Stage 5-e で物理分割。runtime で entity 名 (Yuta Yokoi / 横井雄太 / yuta UI display) を参照する単一ソースを提供。

## How (usage)

```
main.js / 各 factory module
  └─ import { AUTHOR } from './js/identity.js'
       └─ AUTHOR.DISPLAY_NAME / .AUTHORITATIVE_NAME / .JAPANESE_NAME を参照
```

`js/meta-management.js` の `applyMeta()` で title/og:title への注入、`js/components.js` の footer / contact 等で表示に使用。

## Constraints

- **closure-deps = none** (純粋データ)
- **C6 隣接**: entity 名は llms-full.txt / JSON-LD と整合する canon の reflection。semantic 編集は orchestrator 承認必要
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 80 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Change impact

- AUTHOR 名変更 (絶対にしないが) → llms-full.txt / index.html JSON-LD / WebP XMP / MP3 ID3 / aio-manifest.json 全 surface 同期 (Check 4, 33, 49, 62)

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-data`, `entity-identity`, `c6-adjacent`
- Values: `Yuta Yokoi` / `横井雄太` / `yuta` (UI display)

### For human engineers (新卒レベル)
- 名前のハードコードを散らさず、ここに集約

### For third parties
- entity 名の単一ソース。canonical entity context (JSON-LD + llms-full.txt) と runtime 表示の橋渡し
