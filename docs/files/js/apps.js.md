---
file: js/apps.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-22
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-n) / docs/architecture/repository-maintainability-map.md
---

# js/apps.js

## What

Productivity Apps factory module。`createApps({deps})` を export し、**TaskPage / TodoPage / NotesPage の 3 ページ** component + private state を返す。2026-07-04〜05 の bloat-reduction で AIPage → `js/ai-page.js` / PomodoroPage → `js/pomodoro-page.js` / SettingsPage → `js/settings-page.js` へ分離済（837→458 行）ゆえ、それら 3 ページは本 module には含まれない。

## Why

main.js から Stage 5-n で物理分割した productivity 系ページ群。closure-deps = none + 引数注入で外部依存を明示化。肥大化解消 (owner 受諾の 1,000 行しきい値) で AIPage / PomodoroPage / SettingsPage を個別 leaf へ切り出し、本 module は最小 3 ページに縮小した。

## How (usage)

```
main.js
  └─ import { createApps } from './js/apps.js'
  └─ const { TaskPage, TodoPage, NotesPage }
        = createApps({ h, createIcon, Toast, State, CONSTANTS, generateId, clamp })
  // AIPage は createAIPage (js/ai-page.js) / PomodoroPage は createPomodoroPage
  // (js/pomodoro-page.js) / SettingsPage は createSettingsPage (js/settings-page.js) で別途生成
```

## Constraints

- **factory pattern** (Check 56, 61)
- **Check 47**: import/export bijection
- **Check 52**: 行数予算 ≤ 650 行（現在値は file-size-budget.md §4 / `wc -l` が権威）
- **select visual selection — `selected:` on options (#7cbc4d9 class)**: `h('select', { value: ... })` は HTML 仕様上 `el.setAttribute('value', ...)` となり `<select>` の選択状態に反映されない。task priority filter / per-card priority / todo filter の各 select で各 `<option>` に `selected: value === cur ? true : undefined` を付与する (h() の undefined-skip line 128 が非選択 option に属性を付けるのを防ぐ)。

## Change impact

- 新ページ追加 → main.js renderer switch (Check 58) + e2e/portfolio.spec.js ALL_ROUTES (Check 58) + index.html sitemap-relevant 箇所

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `productivity-apps`, `closure-deps-none`

### For human engineers (新卒レベル)
- 3 つの page component (Task/Todo/Notes) を 1 factory にまとめている — かつては 5 つだったが肥大化解消で AI/Pomodoro/Settings を別 module へ切り出した
- private state は factory closure 内に保持される (module scope を汚さない)

### For third parties
- factory pattern + closure-based private state の実装例
