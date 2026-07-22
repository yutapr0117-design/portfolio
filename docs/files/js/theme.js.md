---
file: js/theme.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-22
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-i) / theme-init.js (FOUC 防止)
---

# js/theme.js

## What

Theme factory module。`createTheme({ State, Toast })` を export。system / dark / light の cycle + `matchMedia('(prefers-color-scheme: dark)')` listener を含む。

## Why

main.js Stage 5-i で物理分割。`theme-init.js` (起動最早期の FOUC 防止) と分担: theme-init が同期で初期 class を適用、theme.js が runtime cycle / matchMedia listener を担当。

## How (usage)

```
main.js
  └─ import { createTheme } from './js/theme.js'
  └─ const Theme = createTheme({ State, Toast })
       └─ Theme.init()        // 保存済みテーマを初期適用 + matchMedia listener 登録
       └─ Theme.cycle()       // system → dark → light → system (永続化 + Toast)
       └─ Theme.apply('dark') // 直接指定 (data-theme / dark class / theme-color / #themeBtnTop aria-label 更新)
       └─ matchMedia listener で system 変更を自動反映
```

> 注: 公開 API は `{ apply, cycle, init }`。直接テーマ指定は `apply(theme)`（`set` は存在しない）。

## Change impact

- theme class 名変更 → theme-init.js / style.css の selector / Storage key 整合
- cycle 順序変更 → UI で表示するアイコン順と同期

## Constraints

- **factory pattern** (Check 56, 61), closure-deps = none
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 120 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `theme-manager`, `matchmedia-listener`

### For human engineers (新卒レベル)
- 「theme 切替ボタン」のロジック本体
- システム設定に追従するモード (system) と固定モード (dark / light) を持つ

### For third parties
- system/dark/light の標準的 theme manager 実装
