---
file: js/constants.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-d)
---

# js/constants.js

## What

実行時定数 module。STORAGE_KEY / LIMITS / **POMODORO_DEFAULT_SETTINGS** / **POMODORO_DEFAULT_REMAINING_SEC** / timing / DEBUG / TAB_ID を export。closure-deps = none の純粋データ module。LIMITS には PROJECT_NAME / TODO_TEXT / AI_MESSAGE / **NOTES_TEXT** (20000) / **AI_HISTORY** (80) / **POMODORO_HISTORY** (200) 等の各バリデーション上限・履歴保持件数が集中管理される。pomodoro 既定状態 (settings {work:25,short:5,long:15} + remainingSec 1500) も単一ソースとして集約される。

## Why

main.js から Stage 5-d で物理分割。実行時の定数を 1 箇所に集約して、複数 factory が同じ truth を参照する構造に整理。

## How (usage)

```
main.js
  └─ import { CONSTANTS, STORAGE_KEY, ... } from './js/constants.js'
       └─ 各 factory に注入: createXxx({ CONSTANTS, ... })
```

## Constraints

- **closure-deps = none** (純粋データ)
- **Check 47**: import/export bijection
- **Check 52**: 93 行 ≤ 150

## Change impact

- 定数値変更 → 参照する全 factory + 関連 e2e テスト
- **NOTES_TEXT** 変更 → apps.js (NotesPage oninput) + store.js (validateAndNormalize) が CONSTANTS.LIMITS.NOTES_TEXT 経由で参照（Check 368 が直接 20000 リテラルを BLOCKING 禁止）
- **AI_HISTORY** (80) 変更 → store.js (normalize) + ai-page.js (add) が CONSTANTS.LIMITS.AI_HISTORY 経由で参照（Check 369 が `.slice(-80)` マジックを BLOCKING 禁止）
- **POMODORO_HISTORY** (200) 変更 → store.js (normalize) + pomodoro-page.js (complete) が CONSTANTS.LIMITS.POMODORO_HISTORY 経由で参照（Check 369 が `.slice(-200)` マジックを BLOCKING 禁止）
- **POMODORO_DEFAULT_SETTINGS / POMODORO_DEFAULT_REMAINING_SEC** 変更 → state.js (clone fallback) + store.js (default + normalize clamp fallback) が経由参照（Check 370 が `{work:25...}` / `1500` マジックを BLOCKING 禁止・利用側は参照共有 mutation 回避のため spread 必須）

## Audience-specific notes

### For AI agents
- 役割タグ: `pure-data`, `constants`, `closure-deps-none`

### For human engineers (新卒レベル)
- グローバル変数の代わりに、ここに集約 → factory に引数注入する
- 「Magic Number」を排除する場所

### For third parties
- pure data module の最小例
