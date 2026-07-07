---
file: e2e/portfolio.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-07
canonical-ref: playwright.config.cjs / .github/workflows/playwright-regression.yml / Check 16/29
---

# e2e/portfolio.spec.js

## What

Playwright の **screenshot (visual regression) 専用 spec**。2026-07-07 の肥大化解消 (3,475 行) で behavior テストをテーマ別 `e2e/*.spec.js` に分割した結果、本ファイルには homepage screenshot regression テストと baseline helpers (`baselineExists()` / `isSnapshotUpdateMode()`) のみが残置されている。screenshot を本ファイルに残す理由は snapshot ディレクトリ名 (`portfolio.spec.js-snapshots/`) が spec ファイル名から自動生成されるため、baseline パスを不変に保つ必要があるから。

## Why

Stage 5 物理分割の安全ゲート (視覚回帰の観測)。Session Record #20 §3(B) で screenshot は BLOCKING → ADVISORY に降格され、merge ゲートは behavior e2e に移管された。本ファイルは advisory 観測のホームであり続ける。behavior 面 (全ルート訪問 / focus / drawer / theme 等) は分割された各テーマ spec が担う。

## How (usage)

```
npm run test:e2e
  └─ Playwright + http-server (playwright.config.cjs testDir: ./e2e)
  └─ portfolio.spec.js = homepage screenshot regression (advisory)
  └─ baselineExists() で baseline 不在時は skip (update mode は例外)
  └─ behavior は e2e/*.spec.js (テーマ別) が担当
```

## Constraints

- **Check 16**: screenshot test に baseline-skip ガード
- **Check 29**: baseline-generation の env signal 整合 (PLAYWRIGHT_UPDATE_SNAPSHOTS)
- **Check 111**: networkidle 待ちは本ファイルの screenshot テストのみ許容 (他 spec は禁止)
- **Check 117**: maxDiffPixelRatio ≤ 0.05 (視覚回帰感度の維持)

## Change impact

- screenshot clip/viewport 変更 → baseline 再生成 (update-playwright-snapshots.yml・human-merge)
- behavior テスト追加 → 本ファイルではなく該当テーマ `e2e/<theme>.spec.js` へ

## Audience-specific notes

### For AI agents
- 役割タグ: `e2e-spec`, `visual-regression`, `screenshot-baseline-host`
- behavior テストは `e2e/*.spec.js` に分散。ALL_ROUTES=security-proxy.spec.js / A11Y_ROUTES=a11y-axe.spec.js

### For human engineers (新卒レベル)
- 新 behavior テストは本ファイルに足さず、テーマ別 spec に足す (本ファイルは screenshot 専用)
- snapshot diff が出たら意図的か確認 → 意図的なら baseline 更新 workflow を回す

### For third parties
- AI 実装下での visual regression + テーマ別 behavior e2e の実装例。1 spec ≤1,000 行を維持
