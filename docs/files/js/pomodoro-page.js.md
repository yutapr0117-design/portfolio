---
file: js/pomodoro-page.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-04
canonical-ref: js/apps.js (抽出元) / main.js (配線) / js/state.js (appsData.pomodoro) / js/store.js (normalize)
---

# js/pomodoro-page.js

## What

`route 'apps/pomodoro'` (ポモドーロタイマー — 集中/短休憩/長休憩 モード + 履歴記録) をレンダリングする葉モジュール。`createPomodoroPage({ h, createIcon, State, Router, Toast, clamp })` が `PomodoroPage()` 関数を返す factory。private state `pomodoroTimer` (interval id) と local helper (formatTime / getDuration / getRemaining / start / pause / reset / complete / switchMode / startTimer / stopTimer / buildUI) を内包する。

## Why

肥大化解消 (2026-07-04): `js/apps.js` は複数 app ページを 1 ファイルに抱え 1000 行しきい値を超えていた。PomodoroPage は private state が `pomodoroTimer` 1 個で自己完結するため別葉モジュールへ分離。apps.js は AIPage 分離後の ~1,040 → ~820 行に縮小し 1000 行以下を達成。挙動 byte-equivalent。

## How

- `main.js` が `createPomodoroPage({ h, createIcon, State, Router, Toast, clamp })` で生成し、render dispatch (route 'apps/pomodoro') が `PomodoroPage()` を呼ぶ。
- 3 モード (work/short-break/long-break) を切替、`setInterval` (1 秒) で残り時間を再描画、0 で `complete()` が history に記録 + Toast 通知。

## Constraints

- **葉契約 (Check 47c)**: ローカル ESM import ゼロ。h / createIcon / State / Router / Toast / clamp は全て引数注入。window.render / Date / setInterval / clearInterval はグローバル。
- **stale-closure 温存 (#121/#134)**: `getRemaining` / `getDuration` は必ず `State.get()` で live state を読む。start() 時 closure に固定された古い runtime/settings を読むと complete() が永遠に発火しない / 設定変更が反映されないバグになる。
- **reload auto-resume 温存**: `isActive` かつ `pomodoroTimer` 不在時のみ `startTimer()` で resume (稼働中の毎秒再描画では二重 interval にならない)。
- **非破壊**: 関数本体と private state は抽出元から無改変 (byte-equivalent)。behavior e2e (pomodoro reload resume / 完了) が保証。
- **import bijection (Check 47)**: main.js の `import { createPomodoroPage }` ↔ 本ファイルの `export function createPomodoroPage` が一致。

## Change impact

- 本ファイル / apps.js / main.js の 3 点セットで 1 つの分離。単独変更は import bijection (Check 47) / route↔switch coherence (Check 58/137) が捕捉。
- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。

## Audience-specific notes

- **AI (次担当)**: ポモドーロの編集は本ファイルで完結。**stale-closure 対策が最重要** — timer/interval が読む state は必ず `State.get()` で live を読むこと (closure 変数は再描画で stale になる)。過去 2 度の実バグ (#121/#134) がこのクラス。
- **監査人**: apps.js 肥大化解消の Stage 5 系 leaf 抽出。AIPage に続く 2 番目の apps ページ分離で、これにより apps.js が 1000 行以下に復帰。
