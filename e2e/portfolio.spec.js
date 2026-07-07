// e2e/portfolio.spec.js
// Extracted from .github/workflows/playwright-regression.yml (P2: Playwright file-based consolidation)
// Do NOT embed this file in workflow heredocs — both regression and snapshot workflows reference it directly.

const { test, expect } = require('@playwright/test');
const path = require('path');
const fs   = require('fs');

// Detect whether a screenshot baseline exists for the current platform.
// Playwright stores snapshots under e2e/<spec>-snapshots/<name>-<browser>-<platform>.png
function baselineExists(name) {
  const snapshotDir = path.join(__dirname, 'portfolio.spec.js-snapshots');
  if (!fs.existsSync(snapshotDir)) return false;
  const files = fs.readdirSync(snapshotDir);
  return files.some(f => f.startsWith(name));
}

// Detect baseline-generation mode (set by update-playwright-snapshots.yml).
// In this mode the screenshot test MUST run even when no baseline exists yet,
// otherwise `--update-snapshots` would have nothing to capture and the baseline
// could never be generated (the original skip-guard deadlock — P0-01).
function isSnapshotUpdateMode() {
  return process.env.PLAYWRIGHT_UPDATE_SNAPSHOTS === '1';
}



// ===== 7.1: スクリーンショット差分テスト（ベースライン）=====
// Regression runs: skipped when no baseline image exists (prevents constant-failure on first run).
// Baseline-generation runs (PLAYWRIGHT_UPDATE_SNAPSHOTS=1 via update-playwright-snapshots.yml):
//   the test runs even without a baseline so `--update-snapshots` can capture it. (P0-01)
// Run update-playwright-snapshots.yml to generate the baseline, then commit the .png files.
test('Homepage screenshot regression', async ({ page }) => {
  if (!baselineExists('homepage-baseline') && !isSnapshotUpdateMode()) {
    test.skip(true, 'No screenshot baseline found. Run update-playwright-snapshots workflow to generate.');
  }
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(500); // アニメーション安定待ち
  await expect(page).toHaveScreenshot('homepage-baseline.png', {
    fullPage: false,
    clip: { x: 0, y: 0, width: 1280, height: 720 }
  });
});
