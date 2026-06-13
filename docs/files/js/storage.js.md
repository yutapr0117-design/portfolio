---
file: js/storage.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-c)
---

# js/storage.js

## What

Safe localStorage wrapper module (74 行)。`Storage` object を named export。private browsing / quota exceeded / disabled storage 等の例外を安全に吸収。

## Why

main.js Stage 5-c で最初に物理分割した module。localStorage 直接 access は private mode / quota 等で例外を投げるため、try/catch + null fallback で吸収する wrapper を統一供給。

## How (usage)

```
main.js / state.js / store.js / brand.js / theme.js etc.
  └─ import { Storage } from './js/storage.js'
  └─ Storage.setItem(key, value)  // 例外 swallow
  └─ Storage.getItem(key)         // 失敗時 null
  └─ Storage.removeItem(key)
```

`js/storage.js` を経由しない直接 `localStorage.*` 呼び出しは禁止 (例外で SPA が止まる)。

## Change impact

- API 名 / signature 変更 → 全 caller (10+ 箇所) に影響
- key prefix 変更 → 既存ユーザーの保存データ migration が必要

## Constraints

- **closure-deps = none**, factory pattern なし (純粋 named export object)
- **Check 47**: import/export bijection
- **Check 52**: 74 行 ≤ 120
- **CodeQL**: localStorage.setItem に false-positive 抑制 comment (`js/clear-text-storage-of-sensitive-data` 警告)

## Audience-specific notes

### For AI agents
- 役割タグ: `safe-wrapper`, `localstorage`, `quota-exceeded-safe`

### For human engineers (新卒レベル)
- localStorage を直接触らず、これを経由する
- private mode で setItem が例外を投げても、サイトは動き続ける

### For third parties
- localStorage の例外安全 wrapper の標準的実装
