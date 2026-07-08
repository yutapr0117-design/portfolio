---
file: js/perf-guards.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-23
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-s)
---

# js/perf-guards.js

## What

Performance Guards factory module。`createPerfGuards()` を export。Layout Thrashing 防止 (setProperty / setAttribute('style') を rAF バッチ化) + Media Lifecycle 管理 (DOM 削除時に audio/video の blob: src を MutationObserver で解放) の 2 guard を含む。Media guard はかつて IntersectionObserver(lazy load) / _blobMap(img-video blob 追跡) / URL.createObjectURL フックも持っていたが、いずれも never-activated な vestigial だったため除去済 (実機能は audio/video の blob src 解放のみ)。

## Why

main.js Stage 5-s で物理分割。runtime での layout thrash / media leak を防ぐ guard を集約。引数注入なし (純粋な monkey-patch hook)。

## How (usage)

```
main.js
  └─ import { createPerfGuards } from './js/perf-guards.js'
  └─ createPerfGuards()  // DOM API prototype を hook (副作用のみ、返り値不要)
```

起動時に 1 度だけ呼べば、以降の全 DOM 操作に guard が適用される。

## Constraints

- **factory pattern** (Check 56, 61)
- **closure-deps = none**, 引数注入なし (DOM prototype を直接 hook)
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 250 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Change impact

- DOM prototype hook の範囲変更 → 全 page の runtime 影響大

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `perf-guard`, `dom-prototype-hook`

### For human engineers (新卒レベル)
- Layout Thrashing = read/write を交互にやると毎回 reflow が起きる現象
- ここで monkey-patch して順序を整える

### For third parties
- DOM prototype monkey-patch による性能 guard 実装例
