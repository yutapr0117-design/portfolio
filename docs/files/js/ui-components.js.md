---
file: js/ui-components.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-22
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 4)
---

# js/ui-components.js

## What

UI building blocks module。`h` (hyperscript) / `createIcon` (SVG icon factory) / Toast notification / BGM control 等の low-level builder を named export。Stage 4 安定 module。

## Why

main.js Stage 4 で物理分割。DOM builder と SVG icon と Toast を 1 module に集約して、各 page component から使う共通インフラ。

## How (usage)

```
main.js / 各 factory module
  └─ import { h, createIcon, Toast, BGM } from './js/ui-components.js'
  └─ const el = h('div', {class: 'card'}, ['Hello', h('br'), 'World'])
  └─ const icon = createIcon('chevron-down', 24)
  └─ Toast.show('Saved!', 'success')
  └─ BGM.toggle()   // 再生/停止トグル (公開 API は { toggle, isOn, syncAll, init }・play/pause は内部)
  └─ BGM.isOn()     // 現在の再生状態
```

## Change impact

- `h()` シグネチャ変更 → 全 page component (1,000+ 箇所) に影響
- SVG icon 追加 → createIcon の lookup table 拡張 + assets/icons.svg sprite 更新

## Constraints

- **closure-deps = none**, factory pattern なし (Stage 4 時点では純 named export)
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 400 行（現在値は file-size-budget.md §4 / `wc -l` が権威）
- **Check 411**: `querySelectorAll('[data-bgm-btn]')` の走査対象が実際に描画されていること。この属性は index.html の topbar ボタンにのみ、**値なしの bare 属性**として存在する（JS 側は一切出さない）。解決しなくなると BGM ボタンの aria-pressed / aria-label / アイコンの状態同期が静かに無効化される

## Audience-specific notes

### For AI agents
- 役割タグ: `ui-builders`, `dom-helpers`, `stage-4-stable`

### For human engineers (新卒レベル)
- `h('div', {class: 'card'}, ['Hello'])` のような hyperscript で DOM を組む
- 「React の代わり」と思って良い (ただし virtual DOM ではない)

### For third parties
- Boring Technology 哲学の hyperscript 実装。React なしで宣言的 DOM 構築する例

## `rel` は上書きではなく合併する (2026-09-06)

`h()` は `target="_blank"` の anchor に `noopener noreferrer` を強制するが、**従来は
`setAttribute` で上書きしており、呼び出し側が付けたセマンティックトークン
（`license` / `author` / `alternate` / `nofollow`）を silent に捨てていた**。
実測: `rel: 'license noopener noreferrer'` が `noopener noreferrer` になる。

誰も気付かなかったのは、**それまでセマンティックトークンを付ける呼び出し側が 1 つも
無かった**から。union へ変えても `noopener`/`noreferrer` は必ず加わるのでセキュリティ契約は
不変で、意図したセマンティクスだけが生き残る。外部リンクの `noopener noreferrer` は
既存の security e2e が引き続き強制する。
