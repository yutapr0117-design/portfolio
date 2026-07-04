---
file: js/home-page.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-04
canonical-ref: js/components.js (抽出元) / main.js (配線) / js/ui-components.js (h)
---

# js/home-page.js

## What

`route 'home'` (SPA トップ / hero + サマリー) をレンダリングする葉モジュール。`createHomePage({ h, Router, State, ContactCTA })` が `HomePage` 関数を返す factory。

## Why

肥大化解消 (2026-07-04): `js/components.js` に同居していた 2 番目に大きいページ HomePage (~296 行) を分離し、components.js を更に縮小して保守性・拡張性・AI 自走のコンテキスト負荷を改善した。挙動は byte-equivalent (関数本体を無改変で移設)。AIKnowhowPage 分離 (#548) に続く肥大化解消トラック第 3 弾。

## How

- `main.js` が `createComponents({...})` を実行後、共有 helper `ContactCTA` を取り出し、`createHomePage({ h, Router, State, ContactCTA })` で `HomePage` を生成する。
- render dispatch (main.js の route 分岐 `case 'home'` 相当) で従来どおり `HomePage()` を呼ぶ。
- 生成タイミングが createComponents の「後」なのは ContactCTA が createComponents 内で定義される共有 helper だから。

## Constraints

- **葉契約 (Check 47c)**: ローカル ESM import ゼロ。h / Router / State / ContactCTA は全て引数注入。
- **非破壊**: 関数本体は抽出元から無改変。hero CTA の遷移 (Router) / プロフィール描画 (State) 挙動は不変で behavior e2e (route 'home' 訪問) が保証。
- **import bijection (Check 47)**: main.js の `import { createHomePage }` ↔ 本ファイルの `export function createHomePage` が一致すること。

## Change impact

- 本ファイル / components.js / main.js の 3 点セットで 1 つの分離。単独変更は import bijection (Check 47) / route↔switch coherence (Check 58/137) が捕捉。
- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。

## Audience-specific notes

- **AI (次担当)**: home ページの編集は本ファイルで完結。ContactCTA は末尾 CTA の共有 helper ゆえ触らず注入されたものを使う。
- **監査人**: components.js からの Stage 5 系 leaf 抽出の 1 つ。factory + 依存注入で葉性を維持。
