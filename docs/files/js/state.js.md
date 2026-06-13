---
file: js/state.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-h) / js/storage.js
---

# js/state.js

## What

State factory module (240 行)。`createState({Storage})` を export。Proxy ベースの型安全モニタ + subscriber + cross-tab sync + auto-save を含む。

## Why

main.js Stage 5-h で物理分割。Proxy traps で型違反を runtime に検出し、subscriber pattern で UI 連動、`storage` event で cross-tab 同期、debounced auto-save で localStorage 永続化。

## How (usage)

```
main.js
  └─ import { createState } from './js/state.js'
  └─ const State = createState({ Storage })
       └─ State.set(key, value) / State.get(key) / State.subscribe(fn)
            └─ Proxy traps で型違反を検出 → throw
            └─ subscribers に通知 → UI 再描画
            └─ debounced で Storage.setItem (auto-save)
            └─ 別タブの storage event で再 hydrate
```

## Change impact

- Proxy schema 変更 → js/store.js の validate/normalize と整合
- subscriber API 変更 → 全 page component の bind ロジック

## Constraints

- **factory pattern** (Check 56, 61), closure-deps = none
- **Check 47**: import/export bijection
- **Check 52**: 240 行 ≤ 320

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `state-manager`, `proxy-typed`, `cross-tab-sync`

### For human engineers (新卒レベル)
- 状態管理 (Redux に相当する役割) を Proxy + Safe Storage で実装
- 別タブで開いた状態と同期する (cross-tab) — `storage` event を使う

### For third parties
- Proxy + Safe Storage + cross-tab sync の組み合わせ実装例
