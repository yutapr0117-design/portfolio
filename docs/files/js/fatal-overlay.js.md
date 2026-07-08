---
file: js/fatal-overlay.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-r)
---

# js/fatal-overlay.js

## What

Fatal overlay + Global Safety Net factory module。`createFatalOverlay({render})` を export。fatal error 判定ロジック + Shadow DOM フォールバック UI + `setInterval` ウォッチャを含む。

## Why

main.js Stage 5-r で物理分割。fatal error の最終救済 UI を独立 module に切り出した。render への late binding で循環依存を解消。

## How (usage)

```
main.js
  └─ import { createFatalOverlay } from './js/fatal-overlay.js'
  └─ const { installFatalOverlay, normalizeError }
        = createFatalOverlay({ render: (...args) => render(...args) })  // forward ref
```

## Constraints

- **factory pattern** (Check 56, 61), dual-binding factory return (helpers + install)
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 300 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Change impact

- fatal 判定ロジック変更 → C3 ErrorBoundary 範疇 → orchestrator 確認推奨

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `safety-net`, `c3-error-boundary`

### For human engineers (新卒レベル)
- 「fatal error」= ユーザーに何も表示できなくなる致命エラー
- Shadow DOM で隔離した overlay UI を最終フォールバックとして表示する

### For third parties
- error boundary の Shadow DOM 隔離実装例
