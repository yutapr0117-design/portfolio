---
file: js/ai-knowhow-page.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: js/components.js (抽出元) / main.js (配線) / js/ui-components.js (h/createIcon)
---

# js/ai-knowhow-page.js

## What

`route 'ai-knowhow'` のページ (AI 開発ワークフロー / マルチエージェント構成の解説) をレンダリングする葉モジュール。`createAIKnowhowPage({ h, createIcon, ContactCTA })` が `AIKnowhowPage` 関数を返す factory。

## Why

肥大化解消 (2026-07-04): `js/components.js` (1,370 行) に同居していた最大の単一ページ AIKnowhowPage (~295 行) を分離し、components.js を ~1,075 行へ縮小して保守性・拡張性・AI 自走のコンテキスト負荷を改善した。挙動は byte-equivalent (関数本体を無改変で移設)。

## How

- `main.js` が `createComponents({...})` を実行後、その返り値から共有 helper `ContactCTA` を取り出し、`createAIKnowhowPage({ h, createIcon, ContactCTA })` で `AIKnowhowPage` を生成する。
- render dispatch (main.js の route 分岐 `case 'ai-knowhow'` 相当) で従来どおり `AIKnowhowPage()` を呼ぶ。
- 生成タイミングが createComponents の「後」なのは、ContactCTA が createComponents 内で定義され複数ページで共有される helper だから (HomePage / AboutPage / ResumePage / AIKnowhowPage で使用、js/pages.js へも注入)。

## Constraints

- **葉契約 (Check 47c)**: ローカル ESM import ゼロ。h / createIcon / ContactCTA は全て引数注入。
- **非破壊**: 関数本体は抽出元から無改変。ページ表示・article schema route (og:type=article) 挙動は不変で behavior e2e (route 'ai-knowhow' 訪問) が保証。
- **import bijection (Check 47)**: main.js の `import { createAIKnowhowPage }` ↔ 本ファイルの `export function createAIKnowhowPage` が一致すること。

## Change impact

- 本ファイル / components.js / main.js の 3 点セットで 1 つの分離。どれか単独の変更は import bijection (Check 47) / route↔switch coherence (Check 58/137) が捕捉。
- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。

## Audience-specific notes

- **AI (次担当)**: ai-knowhow ページの編集は本ファイルで完結。他ページと同じ h() ベースの DOM 構築。ContactCTA は末尾 CTA の共有 helper ゆえ触らず注入されたものを使う。
- **監査人**: components.js からの Stage 5 系 leaf 抽出の 1 つ。factory pattern + 依存注入で葉性を維持。
