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
    reuseExistingServer: false,
    timeout: 15000,
  },
});
