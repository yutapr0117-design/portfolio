---
file: e2e/portfolio.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: playwright.config.cjs / .github/workflows/playwright-regression.yml / Check 16/28/29/58
---

# e2e/portfolio.spec.js

## What

Playwright e2e + visual regression spec。`ALL_ROUTES` (17 ルート) を順次訪問 + screenshot 比較 + 振る舞いチェック (focus order / drawer toggle / theme cycle 等)。`baselineExists()` + `isSnapshotUpdateMode()` で baseline 不在時は screenshot test をスキップ。

## Why

Stage 5 物理分割の安全ゲート。視覚回帰を baseline と比較し、コード変更が描画に意図しない影響を与えていないか確認。Stage 5-j 教訓 (未訪問ルートの hidden ReferenceError) を全 17 ルート訪問で防止。

## How (usage)

```
npm run test:e2e
  └─ Playwright + http-server
  └─ ALL_ROUTES (17) 順次訪問
  └─ toHaveScreenshot() で baseline 比較
  └─ behavior assertions
```

## Constraints

- **Check 16**: screenshot test に baseline-skip ガード
- **Check 28**: test() のネスト無し
- **Check 29**: baseline-generation の env signal 整合
- **Check 58**: ALL_ROUTES と main.js renderer switch case 集合一致

## Change impact

- ALL_ROUTES 追加 → main.js renderer switch + sitemap.xml + page-meta + router 同期
- assertion 追加 → CI 時間 + 信頼性

## Audience-specific notes

### For AI agents
- 役割タグ: `e2e-spec`, `visual-regression`, `all-routes-coverage`

### For human engineers (新卒レベル)
- 新ルート追加したら ALL_ROUTES に必ず追加 (Check 58 がブロック)
- snapshot diff が出たら意図的か確認 → 意図的なら baseline 更新 workflow を回す

### For third parties
- AI 実装下での全ルート視覚回帰 + behavior 検証の実装例
