const { test, expect } = require('@playwright/test');


// ===== 7.2: モバイルドロワーの開閉 + ARIA + Escape + focus 復帰 Behavior Check =====
// mobile (≤MOBILE_BREAKPOINT=920px) では sidebar が #menuBtn → #drawer (role=dialog,
// aria-modal) に畳まれる。開くと aria-expanded=true / drawer aria-hidden=false / 背景 #app が
// inert+aria-hidden で隔離され、Escape で閉じて focus が #menuBtn に復帰する。これは
// accessibility 上重要な focus-trap / background-isolation 契約だが従来 e2e 未カバーだった。
test('Mobile drawer opens with ARIA, isolates background, and closes on Escape', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const menuBtn = page.locator('#menuBtn');
  const drawer = page.locator('#drawer');
  await expect(menuBtn).toBeVisible();
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');

  // 開く: ARIA 状態と背景隔離
  await menuBtn.click();
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'true');
  await expect(drawer).toHaveAttribute('aria-hidden', 'false');
  await expect(drawer).toBeVisible();
  await expect(page.locator('#app')).toHaveAttribute('aria-hidden', 'true');

  // Escape で閉じる: ARIA 復元 + focus が menuBtn へ復帰
  await page.keyboard.press('Escape');
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');
  await expect(page.locator('#app')).not.toHaveAttribute('aria-hidden', 'true');
  await expect(menuBtn).toBeFocused();
});


// ===== 7.2: drawer 開放中に mobile→desktop リサイズすると閉じて isolation 解除される (stuck 回帰) =====
// openDrawer は drawer/overlay に inline display:block を付与するが、これは media query より優先される。
// 従来 syncMobileDrawer は topbar 表示のみ切替で drawer を閉じなかったため、mobile で drawer を開いた
// まま desktop へリサイズすると drawer/overlay が残り __setAppInert(true)+__lockBodyScroll(true) の
// stuck 状態 (app inert・scroll lock・topbar 非表示で menuBtn も隠れる) になった。desktop 遷移時に
// 開いている drawer を閉じて isolation を解除する fix の回帰検知。
test('Mobile drawer closes and releases isolation on resize to desktop (stuck-state guard)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // mobile で drawer を開く → 背景隔離 (inert) が有効
  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');
  await expect(page.locator('#app')).toHaveAttribute('aria-hidden', 'true');

  // desktop へリサイズ (resize→debounce(syncMobileDrawer)) → drawer が閉じ isolation 解除
  await page.setViewportSize({ width: 1280, height: 900 });
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'true');
  await expect(page.locator('#app')).not.toHaveAttribute('aria-hidden', 'true');
  // body scroll lock (position:fixed) が解除されている
  await expect.poll(async () => page.evaluate(() => document.body.style.position || '')).not.toBe('fixed');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `resize caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: モバイルドロワーの focus trap (Tab が #drawer 内に閉じ込められる・WCAG 2.4.3 モーダル) =====
// __trapFocus は開いたドロワー内で Tab/Shift+Tab を focusable 要素間でループさせ、focus が背景
// (inert 化された #app) へ漏れないようにする。Escape クローズは被覆済みだがこの focus-trap (モーダル
// の a11y 必須要件) は未カバーだった。開いた状態で Shift+Tab (先頭→末尾へ wrap) + 複数 Tab を
// 送っても activeElement が常に #drawer 内に留まることを実検証する。
test('Mobile drawer traps focus within the dialog (WCAG modal focus trap)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  // 開直後 focus は drawer 内 (trapFocus が先頭へ)。Shift+Tab で末尾へ wrap しても drawer 内に留まる
  await page.keyboard.press('Shift+Tab');
  expect(await page.evaluate(() => !!document.activeElement?.closest('#drawer'))).toBe(true);

  // 複数回 Tab を送っても focus は #drawer から漏れない (背景 #app へ移らない)
  for (let i = 0; i < 8; i++) { await page.keyboard.press('Tab'); }
  expect(await page.evaluate(() => !!document.activeElement?.closest('#drawer'))).toBe(true);
  expect(await page.evaluate(() => !!document.activeElement?.closest('#app'))).toBe(false);
});


// ===== 7.2: ドロワーを開放中に再 open しても閉じた時に scroll 位置が保たれる (scroll-clobber 回帰) =====
// #menuBtn は #topbar 内 = #app の外にあり __setAppInert の inert 対象外ゆえ drawer 開放中も
// クリック可能。menuBtn は toggle でなく常に openDrawer を呼ぶため、開放中に再クリックすると
// __lockBodyScroll(true) が body=position:fixed 状態の window.scrollY(=0) を読み __drawerScrollY を
// 0 に上書きし、close 時に先頭へジャンプする (#262 と同 scroll-clobber 症状・別トリガ)。openDrawer の
// idempotency ガードでこれを封じる。プログラム的 click (overlay 越しでも ActionDelegator へ bubble) で
// 再 open を再現し、閉じた後に元の scroll 位置が復元されることを実検証する。
test('Re-opening the drawer while open preserves scroll position on close (scroll-clobber regression)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/hiring-risk');
  await page.waitForLoadState('domcontentloaded');

  // SPA の render() が #content を描画し終える (= ページが十分高くなる) のを待ってからスクロールする。
  // domcontentloaded は render 前に発火するため、待たずに scrollTo すると #content が空で scrollY=0 になる。
  await expect(page.getByText('採用リスク低減')).toBeVisible();

  // 長いページで下方へスクロール (instant: CSS scroll-behavior:smooth のアニメーションを避け同期確定)。
  await page.evaluate(() => window.scrollTo({ top: 400, left: 0, behavior: 'instant' }));
  const before = await page.evaluate(() => Math.round(window.scrollY));
  expect(before, 'precondition: page must be scrollable so the test is non-vacuous').toBeGreaterThan(0);

  // open #1 → __drawerScrollY = before。programmatic click を使う: Playwright の通常 click は
  // actionability で要素を可視化するためページを scroll(=scrollY を 0 にリセット)してしまい、
  // sticky な menuBtn をタップする実機挙動 (scroll 維持) と乖離するため。
  await page.evaluate(() => document.getElementById('menuBtn').click());
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  // 開放中に再 open を試みる (programmatic click は overlay 越しでも ActionDelegator へ bubble する)。
  // 修正前は __drawerScrollY が 0 に上書きされる。
  await page.evaluate(() => document.getElementById('menuBtn').click());

  // Escape で閉じる → scroll が復元される (smooth アニメーションの settle を poll で待つ)
  await page.keyboard.press('Escape');
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'true');

  // 修正前は __drawerScrollY=0 ゆえ先頭(0)へ戻り poll が before に到達せず fail する。
  await expect.poll(() => page.evaluate(() => Math.round(window.scrollY)),
    { message: `scroll must restore to ${before}, not jump to top` }).toBe(before);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `drawer re-open caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: ドロワー overlay(背景)クリックで閉じる (モーダル backdrop dismiss) =====
// main.js は #overlay のクリックで closeDrawer を呼ぶ (main.js:800)。Escape / nav-link クローズ
// とは別の「背景クリックで閉じる」モーダル標準挙動で未カバーだった。開いて overlay をクリック →
// aria-hidden 復帰 + 背景隔離 (#app aria-hidden) 解除 + menuBtn aria-expanded=false を検証。
test('Mobile drawer closes on overlay (backdrop) click', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const menuBtn = page.locator('#menuBtn');
  const drawer = page.locator('#drawer');
  await menuBtn.click();
  await expect(drawer).toHaveAttribute('aria-hidden', 'false');

  // 背景 overlay クリックで閉じる (overlay 中央は drawer に覆われ得るため click ハンドラを
  // dispatchEvent で直接発火 = main.js:800 の overlay→closeDrawer 配線を検証)
  await page.locator('#overlay').dispatchEvent('click');
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  await expect(page.locator('#app')).not.toHaveAttribute('aria-hidden', 'true');
});


// ===== 7.2: モバイルドロワーからのナビゲーション (リンククリック → 遷移 + 自動クローズ) =====
// drawer 内 navLink は isDrawer のとき onclick で Router.navigate(path) に加え closeDrawer() を
// 呼ぶ (components.js)。Escape クローズ (#上) とは別の閉路 = ナビゲーション経由のクローズで、
// モバイルで目的ページへ飛ぶ最も普通の操作にも関わらず従来未カバーだった。ドロワーを開いて
// Projects リンクをクリックし、(1) #/projects へ遷移し本文描画 (2) drawer が自動クローズ
// (aria-hidden=true) (3) 背景隔離 (#app aria-hidden) も解除、を実検証する。
test('Mobile drawer nav link navigates and auto-closes the drawer', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const menuBtn = page.locator('#menuBtn');
  const drawer = page.locator('#drawer');
  await menuBtn.click();
  await expect(drawer).toHaveAttribute('aria-hidden', 'false');

  // ドロワー内の Projects ナビリンクをクリック
  const projectsLink = drawer.locator('a.nav-link[href="#/projects"]');
  await expect(projectsLink).toBeVisible();
  await projectsLink.click();

  // (1) 遷移して本文描画
  await expect(page).toHaveURL(/#\/projects$/);
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  // (2) drawer が自動クローズ
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  // (3) 背景隔離も解除
  await expect(page.locator('#app')).not.toHaveAttribute('aria-hidden', 'true');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `drawer nav caused a fatal: ${fatal}`).toBeNull();
});
