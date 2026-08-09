---
file: e2e/apps-todo.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-09
canonical-ref: playwright.config.cjs / .github/workflows/playwright-regression.yml / js/apps.js (TaskPage/TodoPage) / js/store.js / js/state.js
---

# e2e/apps-todo.spec.js

## What

TODO アプリの e2e。追加 / 完了トグル / 完了済み削除・IME composition ガード・フィルタ (active/completed/all) と
select の視覚選択保持・完了状態の reload 永続 (normalize round-trip)・`h()` の boolean child skip・
MAX_TODOS への import 切り詰め・a11y (checkbox/削除ボタンの accessible name・assertive live region 通知)・
ErrorBoundary 属性 leak の非混入 を検証する。

## Why

2026-08-09 に apps-task.spec.js が 973 行となり、新設した e2e 予算 (advisory 900・Check 408) が
**Check 365 の 1,000 行 BLOCKING に当たる前に**警告した。BLOCKING を踏んでから慌てて移設するのではなく
**警告に従って先回りで**テーマ分割した増分であり、Task アプリ面 (apps-task.spec.js) と TODO アプリ面
(本ファイル) に分離している。mutation の `test` フィールドは title 一致ゆえ file 移動の影響を受けない。

## How (usage)

```
npm run test:e2e
  └─ Playwright + http-server (playwright.config.cjs testDir: ./e2e)
  └─ e2e/*.spec.js は testMatch デフォルト (**/*.spec.js) で自動 discovery
  └─ behavior assertions (screenshot は portfolio.spec.js に残置)
```

## Constraints

- **Check 28**: 全 e2e/*.spec.js に test() のネスト無し
- **Check 111**: networkidle 待ちは screenshot (portfolio.spec.js) 以外で禁止
- **Check 114**: test.only/describe.only 無し (false-green footgun 防止)
- **Check 151**: 全 e2e/*.spec.js 横断で test() title 一意
- **Check 108**: docs/files ミラー 1 対 1 bijection

## Change impact

- test 追加/削除 → CI 時間 + behavior gate カバレッジ + mutation-probe-e2e の対応
- spec ファイル rename → docs/files ミラー同期 (Check 108) + Check 28/111/114/151 の glob 対象

## Audience-specific notes

### For AI agents
- 役割タグ: `e2e-spec`, `behavior-gate`, `apps-task`
- portfolio.spec.js から 2026-07-07 に肥大化解消 (3,475 行) の一環でテーマ別分割された 1 ファイル

### For human engineers (新卒レベル)
- 新規 e2e は `e2e/<theme>.spec.js` 命名 (testMatch デフォルトが `.spec.js` を要求)
- test title は全 spec 横断で一意にする (Check 151 がブロック)

### For third parties
- AI 実装下での behavior e2e (機能ゲート) の実装例。テーマ別分割で 1 ファイル ≤1,000 行を維持
