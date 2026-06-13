---
file: .github/workflows/playwright-regression.yml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: e2e/portfolio.spec.js / playwright.config.cjs
---

# .github/workflows/playwright-regression.yml

## What

PR 用の **Playwright 視覚回帰 + 振る舞いテスト** workflow。index.html / main.js / js/** / style.css / asset 等の関連 path が変更されたら Chromium で e2e + 視覚回帰 (toHaveScreenshot) を実行。

## Why

「コードが動くか」「画面が変わっていないか」を AI 実装変更時に pre-merge で確認。Stage 5 物理分割の安全ゲートとして取得済の visual baseline を活用。

## How (usage)

```
on:
  pull_request to main
  paths: [index.html, main.js, js/**, style.css, AIO 系...]
└─ checkout + setup-node + npm ci + playwright install
└─ npx playwright test (Chromium)
└─ snapshot diff があれば fail
└─ artifact upload (test-results + diff PNG)
```

## Constraints

- **Check 23**: YAML 構文 valid
- **Check 67**: permissions: contents:read
- **Check 51**: Playwright pin (1.60.0) が runbook と一致

## Change impact

- paths 拡張 → 新 shipped surface も視覚回帰対象
- Chromium バージョン更新 → baseline 再取得 (update-playwright-snapshots.yml)

## Audience-specific notes

### For AI agents
- 役割タグ: `visual-regression`, `e2e`, `chromium-pinned`

### For human engineers (新卒レベル)
- CSS / DOM 構造を変えると Playwright が落ちる
- 意図的な変更なら `update-playwright-snapshots.yml` で baseline 更新 → PR 経由でレビュー

### For third parties
- AI 実装下での視覚回帰防止 + 段階的 baseline 更新の実装例
