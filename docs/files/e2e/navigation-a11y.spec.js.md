---
file: e2e/navigation-a11y.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-07
canonical-ref: playwright.config.cjs / .github/workflows/playwright-regression.yml / main.js render (route-focus) / js/ui-components.js (sidebar)
---

# e2e/navigation-a11y.spec.js

## What

ナビゲーション a11y の e2e。skip link が #main-content へ focus 移動しルーティングを壊さない・sidebar nav link のキーボード操作 (focus + Enter)・全 sidebar nav link が有効ルートに解決する・ルート変更が新ページ heading へ focus 移動する (WCAG 2.4.3) を検証する。

## Why

SPA の route 遷移で focus が body に落ちる WCAG 2.4.3 違反 (#267) 等の a11y 回帰を機能ゲートで守る。

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
- 役割タグ: `e2e-spec`, `behavior-gate`, `navigation-a11y`
- portfolio.spec.js から 2026-07-07 に肥大化解消 (3,475 行) の一環でテーマ別分割された 1 ファイル

### For human engineers (新卒レベル)
- 新規 e2e は `e2e/<theme>.spec.js` 命名 (testMatch デフォルトが `.spec.js` を要求)
- test title は全 spec 横断で一意にする (Check 151 がブロック)

### For third parties
- AI 実装下での behavior e2e (機能ゲート) の実装例。テーマ別分割で 1 ファイル ≤1,000 行を維持
