---
file: js/pages.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-22
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-b → 5-j fix) / Stage 5-j 教訓
---

# js/pages.js

## What

Page components factory (267 行)。`createPages({h, createIcon, Router, ContactCTA})` を export し、**RoleSplitPage / NotFoundPage の 2 つ**を返す。Stage 5-b 抽出後、Stage 5-j で hidden ReferenceError バグが発覚し factory pattern へリファクタ。2026-07-04 bloat-reduction で HiringRiskPage + 専用 helper を `js/hiring-risk-page.js` へ分離し 650→267 行へ縮小した。

## Why

Stage 5-b で main.js から物理分割した際、`h` / `createIcon` / `Router` を implicit global として使っていたため、未訪問ルートで ReferenceError が runtime に発生する hidden bug (Stage 5-j 教訓) が混入。これを factory pattern (createPages({deps})) で構造的に閉じた。

教訓: 物理分割では closure-deps = none + 引数注入を厳格に守る (Check 56 / 61 で機械強制)。

## How (usage)

```
main.js
  └─ import { createPages } from './js/pages.js'
  └─ const { RoleSplitPage, NotFoundPage } = createPages({ h, createIcon, Router, ContactCTA })
       └─ Router の change イベントで各 Page 関数を呼んで render
```

## Constraints

- **factory pattern** (Check 56, 61)
- **closure-deps = none** (h / createIcon / Router / ContactCTA を注入)
- **Check 47**: import/export bijection
- **Check 56**: factory invocation orphan 防止 (Stage 5-j class)
- **Check 52**: 行数予算 ≤ 400 行（現在値は file-size-budget.md §4 / `wc -l` が権威）

## Change impact

- ContactCTA component 追加で createPages の deps が拡張された経緯あり (PR #34)

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `page-components`, `stage-5-j-fix`

### For human engineers (新卒レベル)
- ここは「Stage 5-j バグの教訓」を背負った module
- factory pattern を厳格に守る (deps は必ず引数注入、globals 禁止)

### For third parties
- factory pattern 確立の history。「動いていたコードが動かなくなる」隠れバグ class の構造的解消事例
