---
file: js/project-detail-page.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-04
canonical-ref: js/components.js (抽出元) / main.js (配線) / js/store.js (autoRelatedCandidates)
---

# js/project-detail-page.js

## What

`route 'project-detail'` (個別プロジェクト詳細 + 関連プロジェクト推薦) をレンダリングする葉モジュール。`createProjectDetailPage({ h, createIcon, Router, State, Store })` が `ProjectDetailPage(slug)` 関数を返す factory。

## Why

肥大化解消 (2026-07-04): `js/components.js` からプロジェクト詳細ページ (~154 行) を分離。ProjectsPage (#551) と合わせプロジェクト系ページの分離を完結。累計 components.js は 1,370 → ~453 行 (-67%)。挙動 byte-equivalent。

## How

- `main.js` が `createProjectDetailPage({ h, createIcon, Router, State, Store })` で `ProjectDetailPage` を生成し、render dispatch (route 'project-detail') が slug を渡して `ProjectDetailPage(slug)` を呼ぶ。
- slug→project の解決は `State.get().projects.find(p => p.slug === slug)`。slug 一意化 (#154) は Store 側 normalize 済ゆえ本ページは find で一意解決できる。
- 関連プロジェクト推薦は `Store.autoRelatedCandidates` (類似度計算)。

## Constraints

- **葉契約 (Check 47c)**: ローカル ESM import ゼロ。h / createIcon / Router / State / Store は全て引数注入。
- **非破壊**: 関数本体は抽出元から無改変。詳細表示・関連推薦・到達性 (#154 slug 衝突) は不変で behavior e2e (route 'project-detail' known slug) が保証。
- **import bijection (Check 47)**: main.js の `import { createProjectDetailPage }` ↔ 本ファイルの `export function createProjectDetailPage` が一致。

## Change impact

- 本ファイル / components.js / main.js の 3 点セットで 1 つの分離。単独変更は import bijection (Check 47) / route↔switch coherence (Check 58/137) が捕捉。
- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。

## Audience-specific notes

- **AI (次担当)**: プロジェクト詳細の編集は本ファイルで完結。関連推薦は Store.autoRelatedCandidates を使う。
- **監査人**: components.js からの Stage 5 系 leaf 抽出の 1 つ (プロジェクト系ページ分離の完結)。
