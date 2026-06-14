---
file: e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-14
canonical-ref: e2e/portfolio.spec.js / playwright.config.cjs / Check 16/29
---

# e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png

## What

Playwright 視覚回帰の **homepage baseline PNG** (Chromium / Linux runner)。`toHaveScreenshot('homepage-baseline')` 比較の真値。PR #13 で取得 (Stage 5 物理分割の安全ゲート開放の起点)。

## Why

「視覚回帰検出の真値」として保持。CSS / DOM 構造が意図しない変化を起こしたかを pixel diff で検出する基準画像。

baseline 更新は人間 review 必須 (`update-playwright-snapshots.yml` workflow_dispatch → PR → merge の手順)。

## How (usage)

```
.github/workflows/playwright-regression.yml (PR 時)
  └─ npx playwright test
       └─ homepage / route を Chromium で render
       └─ toHaveScreenshot('homepage-baseline') で本 PNG と pixel diff
       └─ threshold 内 → pass / 超過 → fail + diff PNG artifact
```

## Constraints

- **DO NOT EDIT directly**: 直接編集禁止 (binary baseline)
- **Check 16**: baseline-skip ガード が e2e spec にある
- **Check 29**: baseline 生成の env signal が workflow と spec で整合
- **Check 51**: Playwright pin (1.60.0) が runbook と一致

## Change impact

- baseline 更新 → 必ず `update-playwright-snapshots.yml` 経由 PR 化 → 人間 review → merge
- 手動編集 → CI 視覚回帰判定が壊れる
- Chromium バージョン変更 → baseline 再取得必要

## Audience-specific notes

### For AI agents
- 役割タグ: `visual-baseline`, `binary-png`, `do-not-edit-directly`, `human-review-gate`

### For human engineers (新卒レベル)
- 直接編集禁止
- 視覚変更したらまず `update-playwright-snapshots.yml` を手動 dispatch

### For third parties (監査 / 採用 / 研究)
- AI 実装下での視覚回帰検出基盤
- Stage 5 物理分割の安全ゲートの実体
