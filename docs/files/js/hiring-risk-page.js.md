---
file: js/hiring-risk-page.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-04
canonical-ref: js/pages.js (抽出元) / main.js (配線) / js/components.js (ContactCTA 供給)
---

# js/hiring-risk-page.js

## What

`route 'hiring-risk'` (採用リスク低減 / v28 採用決裁資料レベルの静的コンテンツページ) をレンダリングする葉モジュール。`createHiringRiskPage({ h, createIcon, Router, ContactCTA })` が `HiringRiskPage()` 関数を返す factory。専用 helper (`impactRow` / `kpiRow` / `decisionFlow` / `riskCard`) を内包する。

## Why

肥大化解消 (2026-07-04): `js/pages.js` は HiringRiskPage / RoleSplitPage / NotFoundPage + helper を 1 ファイルに抱え 642 行に肥大化していた。HiringRiskPage は単独で最大 (~326 行) の静的ページで、専用 helper と共に完全自己完結 (mutable state ゼロ・helper 呼び出しは本ページ内のみ) するため別葉モジュールへ分離。pages.js は ~642 → ~265 行に縮小。挙動 byte-equivalent。

## How

- `main.js` が `createHiringRiskPage({ h, createIcon, Router, ContactCTA }).HiringRiskPage` で生成し、render dispatch (route 'hiring-risk') が `HiringRiskPage()` を呼ぶ。
- 4 レイヤー構成 (思想/不可逆ライン → 経営インパクト → 意思決定アルゴリズム → 実務リスクカード) + 30秒要約 + Executive Summary + KPI + 証拠 + 採用側への約束 + CTA の静的セクション群。
- 末尾で `ContactCTA(...)` を呼ぶ (createComponents から供給される共有 CTA)。

## Constraints

- **葉契約 (Check 47c)**: ローカル ESM import ゼロ。h / createIcon / Router / ContactCTA は全て引数注入。
- **非破壊**: 関数本体と helper は抽出元から無改変 (byte-equivalent)。behavior e2e (route 'hiring-risk' レンダリング) が保証。
- **import bijection (Check 47)**: main.js の `import { createHiringRiskPage }` ↔ 本ファイルの `export function createHiringRiskPage` が一致。

## Change impact

- 本ファイル / pages.js / main.js の 3 点セットで 1 つの分離。単独変更は import bijection (Check 47) / route↔switch coherence (Check 58/137) が捕捉。
- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。

## Audience-specific notes

- **AI (次担当)**: 採用リスクページの編集は本ファイルで完結。helper (impactRow/kpiRow/decisionFlow/riskCard) も本ファイル内にローカル化済。
- **採用担当**: 本ページが「採用側が負うリスクを構造的に低減する仕組み」を経営インパクト・KPI・意思決定モデルで提示する採用決裁資料レベルのコンテンツ。
- **監査人**: pages.js 肥大化解消の Stage 5 系 leaf 抽出。project-detail-page.js / home-page.js / ai-knowhow-page.js と同じ factory pattern。
