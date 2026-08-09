---
file: e2e/apps-settings-io.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-09
canonical-ref: playwright.config.cjs / .github/workflows/playwright-regression.yml / js/settings-page.js / js/store.js
---

# e2e/apps-settings-io.spec.js

## What

Settings アプリの **データ I/O 面** の e2e。フルバックアップ / 部分 export・JSON import (upsert / strict / FileReader
エラー)・選択的 import ゲート・snapshot restore・ingestion 正規化 (AI history bound / 非配列 history / 非配列
project field / 数値 relatedProjectIds / profile email bound) を検証する。

## Why

2026-08-09 に apps-settings.spec.js が 1,021 行となり Check 365 (1000 行 capstone) が BLOCKING 化したため、
**データ I/O テーマ 12 テストを本ファイルへ分離**した (残る apps-settings.spec.js は CRUD / 破壊操作 / a11y /
brand / snapshot affordance)。テストの移設ではなく肥大化そのものの解消 (owner の 1,000 行方針) であり、
mutation の `test` フィールドは title 一致ゆえ file 移動の影響を受けない。

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
- 役割タグ: `e2e-spec`, `behavior-gate`, `apps-settings`
- portfolio.spec.js から 2026-07-07 に肥大化解消 (3,475 行) の一環でテーマ別分割された 1 ファイル

### For human engineers (新卒レベル)
- 新規 e2e は `e2e/<theme>.spec.js` 命名 (testMatch デフォルトが `.spec.js` を要求)
- test title は全 spec 横断で一意にする (Check 151 がブロック)

### For third parties
- AI 実装下での behavior e2e (機能ゲート) の実装例。テーマ別分割で 1 ファイル ≤1,000 行を維持
