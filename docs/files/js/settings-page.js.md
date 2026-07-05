---
file: js/settings-page.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: js/apps.js (抽出元) / main.js (配線) / js/store.js (validateAndNormalize) / js/storage.js (snapshot)
---

# js/settings-page.js

## What

`route 'settings'` (設定ページ — import/export・snapshot 保存/復元/削除・手動プロジェクト追加・整合性チェック/正規化) をレンダリングする葉モジュール。`createSettingsPage({ h, Toast, State, Brand, Store, Storage, CONSTANTS, generateId, slugify })` が `SettingsPage()` 関数を返す factory。private state `settings*` (settingsImportMode / settingsIncludeProfile / settingsIncludeProjects / settingsIncludeApps / settingsNewName / settingsNewTech / settingsNewDemo, let × 7) と local helper (getSnapshot / setSnapshot / restoreSnapshot / clearSnapshot / downloadJSON / exportFull / exportProjects / exportApps / exportProfile / importJSON / addProjectManual / buildUI) を内包する。

## Why

肥大化解消 (2026-07-05): `js/apps.js` は AIPage / PomodoroPage 分離後も 837 行あり、SettingsPage が最大の page (~373 行) で肥大化の主因だった。owner 受諾の 1,000 行しきい値 (Check 363 で BLOCKING 化) への headroom を確保するため、SettingsPage を独立葉モジュールへ分離し apps.js を 837→461 行に縮小した。挙動 byte-equivalent。肥大化「解消」と「防止」(Check 363) をセットで進める owner directive の解消側。

## How

- `main.js` が `createSettingsPage({ h, Toast, State, Brand, Store, Storage, CONSTANTS, generateId, slugify })` で生成し、render dispatch (route 'settings') が `SettingsPage()` を呼ぶ。
- import/export は JSON blob の download / FileReader read。snapshot は `CONSTANTS.SNAPSHOT_KEY` に save/restore/clear。手動追加は slug 衝突回避 (#154 class) 付き。

## Constraints

- **葉契約 (Check 47c)**: ローカル ESM import ゼロ。h / Toast / State / Brand / Store / Storage / CONSTANTS / generateId / slugify は全て引数注入。document / Blob / URL / FileReader はグローバル。
- **外部 ingestion 全経路正規化 (#93/#295/#561)**: `restoreSnapshot` / `importJSON` は必ず `Store.validateAndNormalize` を通す。生 `State.set(snap.data)` は別 schema/欠損データで FatalPage crash するため禁止。behavior e2e (snapshot restore normalizes) が保証。
- **upsert data-loss 温存 (#192)**: importJSON の upsert モードは 1 つの Map に更新も追加も集約し新規 id を確実に残す。
- **Demo セレクタ coherence (#294 / Check 140)**: 手動追加フォームの Demo `<select>` option は router whitelist と一致させる (task/todo/pomodoro/ai/notes)。
- **非破壊**: 関数本体と private state は抽出元から無改変 (byte-equivalent)。
- **import bijection (Check 47)**: main.js の `import { createSettingsPage }` ↔ 本ファイルの `export function createSettingsPage` が一致。

## Change impact

- 本ファイル / apps.js / main.js の 3 点セットで 1 つの分離。単独変更は import bijection (Check 47) / route↔switch coherence が捕捉。
- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。Check 361 が BUDGET-DATA 登録・Check 363 が 1,000 行上限を強制。
- snapshot-restore の mutation anchor (mutation_samples E2E_MUTATIONS) は本ファイルへ移動済 (Check 362)。

## Audience-specific notes

- **AI (次担当)**: 設定ページの編集は本ファイルで完結。**外部データ ingestion (restore/import) は必ず `Store.validateAndNormalize` を通すこと** — 過去の実バグ (#561 snapshot / #295 cross-tab / #93 load) が全てこのクラス。手動追加は slug 一意化 (#154) を壊さないこと。
- **監査人**: apps.js 肥大化解消の 3 番目の apps ページ分離 (AIPage / PomodoroPage に続く)。これにより apps.js は 461 行、全 shipped JS ロジック leaf が 1,000 行しきい値 (Check 363 BLOCKING) に対し十分な headroom を持つ。
