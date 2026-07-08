---
file: js/apps.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-n) / docs/architecture/repository-maintainability-map.md
---

# js/apps.js

## What

Productivity Apps 5 関数の合成 factory module (1,030 行)。`createApps({deps})` を export。TaskPage / TodoPage / PomodoroPage / AIPage / SettingsPage の 5 ページ component + private state を含む。

## Why

main.js から Stage 5-n で物理分割した productivity 系ページ群。closure-deps = none + 引数注入で外部依存を明示化。

## How (usage)

```
main.js
  └─ import { createApps } from './js/apps.js'
  └─ const { TaskPage, TodoPage, PomodoroPage, AIPage, SettingsPage }
        = createApps({ h, createIcon, Router, Storage, Store, Theme, BGM })
```

## Constraints

- **factory pattern** (Check 56, 61)
- **Check 47**: import/export bijection
- **Check 52**: 1,030 行 ≤ 1,200
- **select visual selection — `selected:` on options (#7cbc4d9 class)**: `h('select', { value: ... })` は HTML 仕様上 `el.setAttribute('value', ...)` となり `<select>` の選択状態に反映されない。task priority filter / per-card priority / todo filter の各 select で各 `<option>` に `selected: value === cur ? true : undefined` を付与する (h() の undefined-skip line 128 が非選択 option に属性を付けるのを防ぐ)。

## Change impact

- 新ページ追加 → main.js renderer switch (Check 58) + e2e/portfolio.spec.js ALL_ROUTES (Check 58) + index.html sitemap-relevant 箇所

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `productivity-apps`, `closure-deps-none`

### For human engineers (新卒レベル)
- 5 つの page component を 1 factory にまとめている — ページ数が増えたら別 module に切り出すか判断
- private state は factory closure 内に保持される (module scope を汚さない)

### For third parties
- factory pattern + closure-based private state の実装例
