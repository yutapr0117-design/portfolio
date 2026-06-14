// playwright.config.cjs
// Shared Playwright configuration for regression and snapshot-update workflows.
// Used by:
//   .github/workflows/playwright-regression.yml
//   .github/workflows/update-playwright-snapshots.yml
// Do NOT duplicate this config inside workflow heredocs.

const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './e2e',
  timeout: 30000,
  expect: {
    timeout: 5000,
    // WHY この許容値か (baseline-gate の感度設計): threshold/maxDiffPixelRatio はフォント
    // アンチエイリアス等の環境差由来の微小ピクセル差で false-fail しない緩さを持たせつつ、
    // レイアウト崩れ等の本物の視覚 regression は捕まえる balance。0 に締めると baseline が
    // flaky になり「壊れていないのに赤」を量産し、緩めすぎると regression を見逃す。baseline は
    // CLAUDE.md §3 の Stage 5 安全ゲートの中核なので値の変更は慎重に。
    toHaveScreenshot: { threshold: 0.05, maxDiffPixelRatio: 0.02 }
  },
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
    screenshot: 'on',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: 'npx http-server . -p 8080 --silent',
    url: 'http://localhost:8080',
    // WHY reuseExistingServer: false — CI / ローカルとも必ず新しい static server を起動し、
    // commit 済みファイルに対してテストする。既存 dev server を再利用すると stale な編集前
    // 状態を検証してしまい「緑なのに実際は壊れている」false-green を招く。
    reuseExistingServer: false,
    timeout: 15000,
  },
});
