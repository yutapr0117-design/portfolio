---
file: js/perf-guards.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-10
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-s)
---

# js/perf-guards.js

## What

Performance Guard factory module。`createPerfGuards()` を export し、現在は **Media Lifecycle 管理** (DOM から外れた audio/video の blob: src を MutationObserver で解放) の 1 guard のみを持つ。

かつては IntersectionObserver(lazy load) / _blobMap(img-video blob 追跡) / URL.createObjectURL フック (いずれも never-activated な vestigial・#261 で除去) と、**Layout Thrashing 防止 hook** (`CSSStyleDeclaration.prototype.setProperty` と `Element.prototype.setAttribute('style', …)` を rAF まで遅延バッチする) を持っていた。後者も **2026-08-10 に除去した** — 理由は下の Why を参照。

## Why

main.js Stage 5-s で物理分割。runtime での media leak を防ぐ guard を集約。引数注入なし。

### なぜ Layout Thrashing hook を除去したか (2026-08-10)

狙いは「素朴な同期スタイル書き込みループの透過的な最適化」だったが、**一度も発火していなかった**。

- **実測**: 15 ルート走査 + drawer / command palette / theme / 入力の対話を通して **`setProperty` 0 回 / `setAttribute('style')` 0 回**。shipped JS は例外なく `el.style.x = …` か `style.cssText` を使い、hook 自身の NOTE が明記するとおり**直接代入は hook 対象外**だったため。
- **コストは実在した**: (i) アプリの**全** `setAttribute` 呼び出し (ARIA 更新など hot path) にラッパーが 1 段挟まる、(ii) `removeProperty` は hook されないので `setProperty(x,v)` → `removeProperty(x)` の順に書くと**順序が反転して x が設定されたまま残る**、(iii) DOM API の意味論がこのサイトの中だけ非標準になる。
- **実害も出た**: e2e で候補 CSS を当てて同期で読む診断が**全て偽陰性**になり (書き込み前の値が返り `getAttribute('style')` すら `null`)、「要素を隠しても幅が変わらない ＝ コンテンツは無関係」と誤結論しかけた。レイアウト調査 1 サイクル分が無効になった。

利益ゼロ・実コストあり・診断を壊す、の三点で除去した。再混入は **Check 414** (BLOCKING) が構造的に禁止する。

## How (usage)

```
main.js
  └─ import { createPerfGuards } from './js/perf-guards.js'
  └─ createPerfGuards().installMediaLifecycleGuard()  // MutationObserver を 1 つ張る
```

起動時に 1 度だけ呼べばよい。**組み込み prototype はもう触らない** (Check 414 が禁止)。

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
