---
file: playwright.config.cjs
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: e2e/portfolio.spec.js / .github/workflows/playwright-regression.yml
---

# playwright.config.cjs

## What

Playwright 設定。CJS 形式 (Node 24 でも安全)。Chromium で e2e 実行、http-server で `./` を serve、snapshot 比較設定、retries 等。

## Why

ESM (config.mjs) を選ばずに CJS にしたのは Playwright v1.60 の安定性と CI 環境互換性のため。

## How (usage)

```
npx playwright test --config=playwright.config.cjs
  └─ webServer: npx http-server -p <port>
  └─ projects: chromium のみ
  └─ snapshot pixel diff threshold 設定
```

## Constraints

- **Check 23**: JS 構文 valid (node --check)
- **Check 51**: バージョン pin が runbook と一致 (1.60.0)

## Change impact

- threshold 変更 → visual baseline の感度に影響
- webServer 変更 → http-server 等の依存と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `playwright-config`, `cjs-format`

### For human engineers (新卒レベル)
- e2e の設定。CSS 変更で snapshot diff が出るかの threshold もここ

### For third parties
- Boring Technology + e2e の組み合わせ実装例
