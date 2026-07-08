---
file: js/command-palette.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-21
canonical-ref: js/router.js / js/ui-components.js / main.js (合成 + init)
---

# js/command-palette.js

## What

Cmd/Ctrl+K で開くキーボード駆動の横断ナビゲーション overlay の葉モジュール（factory）。入力で行き先を絞り込み、↑↓ で選択・Enter で `Router.navigate`・Esc/背景クリックで閉じる。**新ルートは追加せず**既存ルートへ飛ぶだけの純追加機能。overlay DOM は初回 open 時に動的生成し body へ append する（index.html 不変）。

## Why

検索 input・category・タグに続く第 4 のナビ導線として、キーボードのみで全主要ルートへ即移動できる UX を提供する。route cascade（PAGE_META/ALL_ROUTES/a11y coverage）を避けるため overlay 方式（新ルート無し）を採用。focus-trap・keyboard nav・a11y（role=dialog/listbox/option）を Vanilla JS で実装し、エンジニアリング（設計力）を実証する。

## How (usage)

```
main.js
  └─ import { createCommandPalette } from './js/command-palette.js'
  └─ const CommandPalette = createCommandPalette({ Router, h, createIcon, State })
  └─ CommandPalette.init()   // global Cmd/Ctrl+K keydown を登録（他キーは素通し）
       └─ open(): overlay 生成/表示 → focus trap (Tab/↑↓/Enter/Esc) → inputEl.focus()
       └─ _choose(i): close() → Router.navigate(dest.hash)
       └─ close(): 非表示 + trap 解除 + 直前 focus 復元
```

## Change impact

- DESTINATIONS（curated quick-nav）に行き先追加 → label/hash を 1 行追加
- 署名 deps 変更 → docstring【依存】節を同期（Check 119）
- 新 js/ モジュールゆえ package.json lint/lint:js glob・Check 47 bijection・本 mirror が必要（追加済）

## Constraints

- **葉モジュール**（ローカル import ゼロ・Check 47c）
- 既存 global keydown（Escape / aidk-rails）と非衝突: `(meta|ctrl)+k` のみ横取り
- DOM 副作用は `#command-palette-host`（body 末尾）に限定（render の #content 不可侵）

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `overlay`, `keyboard-nav`, `a11y`, `leaf`
- 新ルート無し＝Check 118/58/110 の route cascade に非該当

### For human engineers (新卒レベル)
- 「Cmd+K で出るクイックナビ」。focus-trap と矢印キー選択を素の JS で実装

### For third parties
- 外部ライブラリゼロで command palette（focus-trap + keyboard nav + a11y）を実装した例
