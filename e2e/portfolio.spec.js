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

// ===== 7.1: AIO Anchor 可視化バグ検知 =====
test('AIO asset anchor must be hidden (non-visual)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  const anchor = page.locator('#aio-asset-anchor');
  await expect(anchor).toHaveCount(1);
  // 視覚的に非表示であることを確認（attributeがhiddenである）
  await expect(anchor).toHaveAttribute('hidden', '');
  // boundingBoxがnull（非表示）であることをアサート
  const box = await anchor.boundingBox();
  expect(box).toBeNull();
});

// ===== 7.1: ホームページ初期レンダリング =====
test('Homepage renders without console errors', async ({ page }) => {
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') { errors.push(msg.text()); }
  });
  page.on('pageerror', err => errors.push(err.message));

  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // Fatal エラーがないことを確認
  const fatalOverlay = page.locator('#portfolio-safety-net-host');
  await expect(fatalOverlay).toHaveCount(0);

  // h1 が表示されていることを確認
  const h1 = page.locator('h1, .h1').first();
  await expect(h1).toBeVisible();

  // 致命的コンソールエラーがないことをアサート
  const fatalErrors = errors.filter(e =>
    !e.includes('non-fatal') &&
    !e.includes('View Transition') &&
    !e.includes('SW')
  );
  expect(fatalErrors, 'Fatal console errors: ' + JSON.stringify(fatalErrors)).toHaveLength(0);
});

// ===== 7.2: ハッシュルーティング状態遷移 Behavior Check =====
test('Hash routing transitions correctly between routes', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // Projects ページへ遷移
  await page.goto('/#/projects');
  await page.waitForLoadState('networkidle');
  // #content が表示されており aria-busy が false に戻っていること
  const content = page.locator('#content');
  await expect(content).toBeVisible();
  await expect(content).toHaveAttribute('aria-busy', 'false');

  // ホームへ戻る
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  // .hero-section が表示されること
  const hero = page.locator('.hero-section');
  await expect(hero).toBeVisible();
});

// ===== 7.2: aria-busy 状態遷移 Behavior Check =====
test('content div transitions aria-busy correctly during navigation', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const content = page.locator('#content');
  await expect(content).toHaveAttribute('aria-busy', 'false');

  await page.goto('/#/projects');
  await page.waitForLoadState('networkidle');
  await expect(content).toHaveAttribute('aria-busy', 'false');
});

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

// ===== 7.2: Projects 検索フォーカス維持 Behavior Check =====
test('Projects search input retains focus during filtering', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('networkidle');

  const searchInput = page.locator('input[type="text"]').first();
  await searchInput.click();
  await searchInput.type('AI', { delay: 50 });

  // 検索後もフォーカスが維持されていること（バグ: v52以前はフォーカス喪失していた）
  await expect(searchInput).toBeFocused();
});

// ===== 7.1: モバイルビューポートでのCLS検証 =====
test('No layout shift on mobile viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // topbar がmobileで表示されていること
  const topbar = page.locator('.topbar');
  await expect(topbar).toBeVisible();

  // サイドバーがmobileで非表示であること
  const sidebar = page.locator('.sidebar');
  await expect(sidebar).not.toBeVisible();
});

// ===== 7.2: テーマ切替の永続化 Behavior Check =====
// theme toggle (#themeBtnTop) は data-theme を cycle (system→dark→light→system) させ、
// State 経由で localStorage に永続化する。リロードを跨いだ往復 (theme-init.js の FOUC
// pre-paint → main.js Theme.init の再適用) が壊れていないことを検証する。Check 100 が
// FOUC pre-paint の storage キー一致を静的強制するのに対し、本テストは実ブラウザでの
// 切替→永続→復元の振る舞いを動的に保証する。
test('Theme toggle cycles data-theme and persists across reload', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const html = page.locator('html');
  const initial = await html.getAttribute('data-theme');

  // テーマ切替ボタンは desktop (sidebar) と mobile (#themeBtnTop) の両方に存在し同じ
  // aria-label を共有する。viewport で可視な方を選んでクリックする。
  const themeBtn = page.locator('button[aria-label="ライトモードとダークモードを切り替える"]:visible').first();
  await expect(themeBtn).toBeVisible();
  await themeBtn.click();

  const afterClick = await html.getAttribute('data-theme');
  expect(afterClick, 'data-theme must change after toggling the theme button').not.toBe(initial);

  // リロード後もテーマが永続化されていること（State → localStorage 往復）
  await page.reload();
  await page.waitForLoadState('networkidle');
  const afterReload = await page.locator('html').getAttribute('data-theme');
  expect(afterReload, 'theme selection must persist across a page reload').toBe(afterClick);
});

// ===== 7.2: 全ハッシュルート検証 — aria-busy 収束 & コンテンツ非空 =====
const HASH_ROUTES = ['#/home', '#/projects', '#/about', '#/contact', '#/skills'];

for (const route of HASH_ROUTES) {
  test(`Hash route ${route}: aria-busy resolves to false and #content is non-empty`, async ({ page }) => {
    await page.goto(`/${route}`);
    await page.waitForLoadState('networkidle');

    const content = page.locator('#content');

    await page.waitForFunction(
      () => {
        const el = document.getElementById('content');
        return el && el.getAttribute('aria-busy') === 'false';
      },
      { timeout: 5000 }
    );

    await expect(content).toHaveAttribute('aria-busy', 'false');

    const isEmpty = await page.evaluate(() => {
      const el = document.getElementById('content');
      return el ? el.children.length === 0 : true;
    });
    expect(isEmpty, `#content must not be empty on route ${route}`).toBe(false);
  });
}

// ===== 7.2: 5層防衛プロキシ — startViewTransition 上書き確認 =====
test('5-layer proxy: document.startViewTransition is overridden by proxy', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const proxyInstalled = await page.evaluate(() => {
    if (typeof document.startViewTransition !== 'function') {
      return true;
    }
    return document.startViewTransition.name === 'startViewTransitionProxy';
  });

  expect(
    proxyInstalled,
    'document.startViewTransition must be replaced by startViewTransitionProxy'
  ).toBe(true);
});

// ===== 7.2: 5層防衛プロキシ — window.addEventListener 直接上書き禁止確認 =====
test('5-layer proxy: window.addEventListener is not directly overwritten', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const isConsistent = await page.evaluate(() => {
    return !Object.prototype.hasOwnProperty.call(window, 'addEventListener');
  });

  expect(
    isConsistent,
    'window.addEventListener must not be directly overwritten; use EventTarget.prototype instead'
  ).toBe(true);
});

// ===== 7.1: AIOアンカー永続性 — ページ読み込み後も DOM に存在すること =====
test('AIO anchor persists in DOM after initial load', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const count = await page.locator('#aio-asset-anchor').count();
  expect(count, '#aio-asset-anchor must exist in DOM').toBe(1);

  await expect(page.locator('#aio-asset-anchor')).toHaveAttribute('hidden', '');
});

// ===== 7.1: AIOアンカー永続性 — ルート遷移後も保持されること =====
test('AIO anchor persists in DOM after route navigation', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  await page.goto('/#/about');
  await page.waitForLoadState('networkidle');

  const count = await page.locator('#aio-asset-anchor').count();
  expect(count, '#aio-asset-anchor must persist after route navigation').toBe(1);
  await expect(page.locator('#aio-asset-anchor')).toHaveAttribute('hidden', '');
});

// ===== 7.2: early suppressor — unhandledrejection リスナーの動作確認 =====
test('Early suppressor: unhandledrejection listener suppresses known patterns', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const wasSuppressed = await page.evaluate(() => {
    const err = new Error('message channel closed before a response was received');
    const event = new PromiseRejectionEvent('unhandledrejection', {
      promise: Promise.reject(err),
      reason: err,
      cancelable: true,
    });
    window.dispatchEvent(event);
    return event.defaultPrevented;
  });

  expect(
    wasSuppressed,
    'Early suppressor must call ev.preventDefault() for known extension error patterns'
  ).toBe(true);
});

// ===== 7.1: Trusted Types / CSP 違反なし確認 =====
test('No Trusted Types or CSP violations in console', async ({ page }) => {
  const violations = [];

  page.on('console', msg => {
    const text = msg.text();
    if (
      msg.type() === 'error' &&
      /TrustedType|Trusted Types|require-trusted-types-for|Content Security Policy|CSP/i.test(text)
    ) {
      violations.push({ type: 'console-error', text });
    }
  });

  page.on('pageerror', err => {
    if (/TrustedType|Trusted Types|require-trusted-types-for/i.test(err.message)) {
      violations.push({ type: 'pageerror', text: err.message });
    }
  });

  await page.goto('/');
  await page.waitForLoadState('networkidle');

  expect(
    violations,
    'Trusted Types / CSP violations found: ' + JSON.stringify(violations)
  ).toHaveLength(0);
});

// ===== v80+ Stage 5-k CI hygiene: all-routes runtime sanity =====
// Stage 5-j で発見された "hidden ReferenceError" (js/pages.js の `h` 未定義参照) は、
// Playwright が当該ルート (/#/hiring-risk, /#/role-split, /#/not-found) を訪問
// していなかったため CI 緑のまま潜在していた。本テスト群は SPA の全 17 ルートを
// 訪問して各ページの runtime 健全性 (console-error / pageerror なし + DOM 出力存在)
// を検証する。これにより同種の bug を将来的に発火前検出可能にする。
//
// 各ルートに対して個別 test() を生成し、失敗しても他ルートは独立に検査される。
// screenshot baseline は引き続き Homepage のみ (他ルートは behavior テストに留め
// baseline の re-take 負荷を避ける)。
const ALL_ROUTES = [
  { hash: '#/',                  name: 'home' },
  { hash: '#/projects',          name: 'projects' },
  { hash: '#/apps',              name: 'apps' },
  { hash: '#/app-task',          name: 'app-task' },
  { hash: '#/app-todo',          name: 'app-todo' },
  { hash: '#/app-pomodoro',      name: 'app-pomodoro' },
  { hash: '#/app-ai',            name: 'app-ai' },
  { hash: '#/settings',          name: 'settings' },
  { hash: '#/about',             name: 'about' },
  { hash: '#/resume',            name: 'resume' },
  { hash: '#/contact',           name: 'contact' },
  { hash: '#/quiz',              name: 'quiz' },
  { hash: '#/hiring-risk',       name: 'hiring-risk' },
  { hash: '#/ai-knowhow',        name: 'ai-knowhow' },
  { hash: '#/role-split',        name: 'role-split' },
  { hash: '#/not-found',         name: 'not-found-fallback' },
];

for (const route of ALL_ROUTES) {
  test(`Route ${route.name} renders without runtime errors`, async ({ page }) => {
    const consoleErrors = [];
    const pageErrors = [];

    page.on('console', msg => {
      if (msg.type() === 'error') {
        const text = msg.text();
        // Allow benign KARTE/Wicle / suppressor-known patterns and pre-existing
        // inline-style CSP advisories that pre-date Stage 5 (role-split has legacy
        // `style: {...}` chains that Object.assign(el.style, ...) emits as
        // "Applying inline style violates CSP" advisories in some Chromium builds;
        // these are advisories, not blocked execution, and pre-date this PR scope).
        if (/KARTE|Wicle|wicle|Failed to fetch|Trusted Type|Applying inline style violates/i.test(text)) { return; }
        // External-resource load failures (e.g. KARTE CDN flaking in CI) surface as
        // "Failed to load resource: net::ERR_FAILED" — note Chromium puts the FAILED URL in
        // msg.location().url, NOT in msg.text(), so the host-name filter above cannot see it.
        // Ignore such network errors only when the failing URL is a *non-self* origin: a failed
        // OWN module/asset would instead throw a pageerror AND leave #content empty (both asserted
        // below), so this never masks a real same-origin regression — it only de-flakes third-party
        // CDN failures that are outside our code's control.
        const _loc = (typeof msg.location === 'function') ? msg.location() : null;
        const _url = (_loc && _loc.url) || '';
        if (/Failed to load resource|net::ERR_/i.test(text) && _url && !/^https?:\/\/(localhost|127\.0\.0\.1)/i.test(_url)) { return; }
        consoleErrors.push(text);
      }
    });
    page.on('pageerror', err => pageErrors.push(err.message));

    await page.goto('/' + route.hash);
    await page.waitForLoadState('networkidle');
    // Wait an extra tick to let the SPA finish its render cycle
    await page.waitForTimeout(200);

    // SPA must have rendered content
    const contentLocator = page.locator('#content');
    await expect(contentLocator).toHaveCount(1);
    const contentText = await contentLocator.textContent();
    expect(contentText, `Route ${route.name} content div is empty — likely render threw`).not.toBe('');

    // No console errors (other than benign third-party patterns)
    expect(
      consoleErrors,
      `Route ${route.name} console errors: ` + JSON.stringify(consoleErrors)
    ).toHaveLength(0);

    // No uncaught page errors (ReferenceError / TypeError 等)
    expect(
      pageErrors,
      `Route ${route.name} page errors: ` + JSON.stringify(pageErrors)
    ).toHaveLength(0);
  });
}

// ===== v80+ Stage 5-k CI hygiene: project-detail route requires slug =====
test('Route project-detail renders for a known slug without errors', async ({ page }) => {
  const consoleErrors = [];
  const pageErrors = [];

  page.on('console', msg => {
    if (msg.type() === 'error') {
      const text = msg.text();
      if (/KARTE|Wicle|wicle|Failed to fetch|Trusted Type|Applying inline style violates/i.test(text)) { return; }
      consoleErrors.push(text);
    }
  });
  page.on('pageerror', err => pageErrors.push(err.message));

  // p01 = task-manager (Store の defaultProjects 先頭)
  await page.goto('/#/project/task-manager');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(200);

  const contentLocator = page.locator('#content');
  const contentText = await contentLocator.textContent();
  expect(contentText, 'project-detail content empty').not.toBe('');
  expect(consoleErrors).toHaveLength(0);
  expect(pageErrors).toHaveLength(0);
});