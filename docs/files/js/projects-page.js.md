---
file: js/projects-page.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-04
canonical-ref: js/components.js (抽出元) / main.js (配線) / js/pure-utils.js (tokenize)
---

# js/projects-page.js

## What

`route 'projects'` (プロジェクト一覧 + 検索/フィルタ) をレンダリングする葉モジュール。`createProjectsPage({ h, createIcon, Router, State, tokenize, clear })` が `ProjectsPage` 関数を返す factory。

## Why

肥大化解消 (2026-07-04): `js/components.js` からプロジェクト一覧ページ ProjectsPage (~172 行) を分離。AIKnowhowPage (#548) / HomePage (#549) に続く肥大化解消トラック第 4 弾。挙動 byte-equivalent (関数本体を無改変で移設)。

## How

- `main.js` が `createProjectsPage({ h, createIcon, Router, State, tokenize, clear })` で `ProjectsPage` を生成し、render dispatch (route 'projects') へ従来配線。
- 検索フィルタは ProjectsPage 内で `updateSilently`(state.js) + 手動 renderList により focus を失わず絞り込む (#258 class の対策済パターン)。tokenize は検索スコアリング。

## Constraints

- **葉契約 (Check 47c)**: ローカル ESM import ゼロ。h / createIcon / Router / State / tokenize / clear は全て引数注入。
- **非破壊**: 関数本体は抽出元から無改変。検索/フィルタ/並び替えの focus 保持挙動は不変で behavior e2e (route 'projects' + 検索操作) が保証。
- **import bijection (Check 47)**: main.js の `import { createProjectsPage }` ↔ 本ファイルの `export function createProjectsPage` が一致。

## Change impact

- 本ファイル / components.js / main.js の 3 点セットで 1 つの分離。単独変更は import bijection (Check 47) / route↔switch coherence (Check 58/137) が捕捉。
- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。

## Audience-specific notes

- **AI (次担当)**: projects 一覧の編集は本ファイルで完結。検索は updateSilently + 手動 renderList で focus 喪失を防ぐパターンを踏襲する。
- **監査人**: components.js からの Stage 5 系 leaf 抽出の 1 つ。factory + 依存注入で葉性を維持。
