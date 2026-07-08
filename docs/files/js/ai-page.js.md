---
file: js/ai-page.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: js/apps.js (抽出元) / main.js (配線) / js/state.js (appsData.ai) / js/constants.js (LIMITS.AI_MESSAGE)
---

# js/ai-page.js

## What

`route 'apps/ai'` (AI アシスト・ローカル版 — 外部 API 非依存のブラウザ内 AI 支援) をレンダリングする葉モジュール。`createAIPage({ h, createIcon, State, CONSTANTS })` が `AIPage()` 関数を返す factory。private state `aiLoading` と local helper (analyzeInput / generateResponse / submit / buildUI) を内包する。

## Why

肥大化解消 (2026-07-04): `js/apps.js` は TaskPage / TodoPage / PomodoroPage / AIPage / NotesPage / SettingsPage を 1 ファイルに抱え 1,179 行に肥大化していた。AIPage は private state が `aiLoading` 1 個のみで local helper と共に完全自己完結する (最も安全な抽出単位) ため別葉モジュールへ分離。apps.js は ~1,179 → ~1,037 行に縮小。挙動 byte-equivalent。

## How

- `main.js` が `createAIPage({ h, createIcon, State, CONSTANTS })` で生成し、render dispatch (route 'apps/ai') が `AIPage()` を呼ぶ。
- `submit()` は入力を analyzeInput で troubleshoot/design/general に分類し generateResponse でローカル応答を生成、`State.update` で ai.history (last `CONSTANTS.LIMITS.AI_HISTORY` = 80 件) に push。
- **stuck-state fail-safe (#555)**: setTimeout 本体を try/finally で包み、generateResponse/State.update が throw しても finally で必ず `aiLoading=false` + 再描画 + focus 復元。
- **IME ガード (#151/152 class)**: Enter submit は `!e.isComposing` で日本語変換確定の誤送信を防ぐ。
- **prompt bound (#230)**: prompt を `CONSTANTS.LIMITS.AI_MESSAGE` で slice し localStorage bloat を防ぐ。
- **履歴上限の単一ソース (Check 369)**: `ai.history` の `.slice(-CONSTANTS.LIMITS.AI_HISTORY)` は store.js normalize と同じ定数を参照する (マジックナンバー 80 を直接持たない)。

## Constraints

- **葉契約 (Check 47c)**: ローカル ESM import ゼロ。h / createIcon / State / CONSTANTS は全て引数注入。window.render / document はグローバル。
- **非破壊**: 関数本体と private state (aiLoading) は抽出元から無改変 (byte-equivalent)。behavior e2e (AI assist 応答生成 / AI history bound) が保証。
- **import bijection (Check 47)**: main.js の `import { createAIPage }` ↔ 本ファイルの `export function createAIPage` が一致。
- **IME ガード (Check 112b)** / **focus-loss ガード (Check 130)**: Enter ハンドラの isComposing 参照・oninput の State.update 非使用は本ファイルでも維持。

## Change impact

- 本ファイル / apps.js / main.js の 3 点セットで 1 つの分離。単独変更は import bijection (Check 47) / route↔switch coherence (Check 58/137) が捕捉。
- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。

## Audience-specific notes

- **AI (次担当)**: AI アシストページの編集は本ファイルで完結。stuck-state fail-safe / IME ガード / prompt bound の 3 つの過去修正が集約されている — 変更時は各 e2e (AI assist 応答生成 / AI history bound) を必ず緑に保つ。
- **監査人**: apps.js 肥大化解消の Stage 5 系 leaf 抽出の 1 つ。private state 最少 (aiLoading のみ) ゆえ最初に抽出した最安全単位。
