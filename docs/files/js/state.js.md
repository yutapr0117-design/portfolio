---
file: js/state.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-23
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-h) / js/storage.js
---

# js/state.js

## What

State factory module (210 行)。`createState({ CONSTANTS, Store, Storage, Toast })` を export。clone-on-update による状態隔離 + subscriber pattern + cross-tab sync + debounced auto-save + 再描画を起こさない `updateSilently`（live-input 用）を含む。

## Why

main.js Stage 5-h で物理分割。`update(fn)` が commonly-mutated ブランチ (profile / projects / projectPrefs / appsData) を深くクローンしてから fn にドラフトを渡すことで、元 state への偶発的共有参照変異を防ぐ (DEBUG 時は元 state を deep-freeze して誤書き込みを検出)。subscriber pattern で UI 連動、`storage` event で cross-tab 同期、visibilitychange での saveNow + debounced auto-save で localStorage 永続化。

## How (usage)

```
main.js
  └─ import { createState } from './js/state.js'
  └─ const State = createState({ CONSTANTS, Store, Storage, Toast })
       └─ State.get()           → 現在の state (data) を返す
       └─ State.update(fn)      → ドラフトを clone → fn(draft) → set(draft)
            └─ subscribers に通知 → UI 再描画
            └─ debounced で Storage.set (auto-save)
       └─ State.updateSilently(fn) → ドラフト commit + scheduleSave するが notify せず
            (= 再描画しない)。高頻度 live-input (quiz 検索 / notes 入力) が毎キーストロークの
            全再描画で focused input を破棄し focus を失うのを防ぐ。呼び出し側が sub-DOM を
            手動更新する契約 (cf. ProjectsPage renderGrid)。Check 130 が oninput→update を禁止。
       └─ State.set(newData)    → 置換 + notify + scheduleSave
       └─ State.subscribe(fn)   → 変更通知購読 (unsubscribe を返す)
       └─ State.saveNow()       → 即時永続化 (visibilitychange 等)
            └─ 別タブの storage event で再 hydrate (cross-tab)
```

## Change impact

- update() の clone 対象ブランチ変更 → js/store.js の validate/normalize と整合
- subscriber API 変更 → 全 page component の bind ロジック

## Constraints

- **factory pattern** (Check 56, 61), closure-deps = none
- **Check 47**: import/export bijection
- **Check 52**: 210 行 ≤ 320

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `state-manager`, `clone-isolated`, `cross-tab-sync`
- NOTE: 旧版にあった Proxy 型安全モニタ (`_wrapWithProxy`) は get() へ一度も配線されない never-activated な設計残骸だったため除去済み (実 state 安全機構は update() の clone + DEBUG deep-freeze)

### For human engineers (新卒レベル)
- 状態管理 (Redux に相当する役割) を clone-on-update + Safe Storage で実装
- 別タブで開いた状態と同期する (cross-tab) — `storage` event を使う

### For third parties
- clone-on-update isolation + Safe Storage + cross-tab sync の組み合わせ実装例
