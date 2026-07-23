const { test, expect } = require('@playwright/test');


// ===== 7.2: skip link が main コンテンツへ focus を移す (WCAG 2.4.1 Bypass Blocks) =====
// `<a href="#main-content" class="skip-link">` はキーボード利用者がナビを飛ばして本文へ直接
// 到達する手段。focus → Enter で focus が #main-content (tabindex=-1) へ移ることを検証する。
// また hash routing (#/...) と競合して NotFound に落ちたり focus が移らない退行も同時に防ぐ。
test('Skip link moves focus to #main-content without breaking routing (WCAG 2.4.1)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const skip = page.locator('.skip-link');
  await skip.focus();
  await expect(skip).toBeFocused();

  await skip.press('Enter');
  // focus が #main-content へ移り、NotFoundPage に落ちていないこと
  await expect(page.locator('#main-content')).toBeFocused();
  await expect(page.getByRole('heading', { name: 'Not Found', exact: true })).toHaveCount(0);
});


// ===== 7.2: サイドバーナビのキーボード操作性 (focus + Enter で遷移・WCAG 2.1.1) =====
// nav-link は <a href="#/..."> + onclick(Router.navigate)。マウス click は別テストで被覆済みだが、
// キーボード利用者にとっての「focus して Enter で起動できる」操作性 (WCAG 2.1.1 Keyboard) は
// 未カバーだった。Projects ナビリンクへ focus し Enter で /#/projects へ遷移 + 本文描画を検証する。
test('Sidebar nav link is keyboard-operable (focus + Enter activates)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const projectsLink = page.locator('a.nav-link[href="#/projects"]:visible').first();
  await projectsLink.focus();
  await expect(projectsLink).toBeFocused();

  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/#\/projects$/);
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
});


// ===== 7.2: サイドバー全 nav リンクの整合性 (全て非 not-found route へ解決) =====
// navLink の href (#/ + item.path) が実在 route を指さないと click で NotFound に落ちる。route-render
// テストは ALL_ROUTES (curated 直 URL) を訪問するが、実際の nav href は検証しないため、nav path の
// タイポ等の drift を捕捉できなかった。サイドバーの全 nav リンク href を収集し、各々を訪問しても
// NotFound に落ちないことを実検証する (非 vacuous: href 6 件以上)。
test('All sidebar nav links resolve to valid (non-not-found) routes', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // [FIX] sidebar はモジュール実行後に描画されるため、domcontentloaded 直後の evaluateAll は
  // 描画前で空になり得る (CI 間欠 flake)。最初の nav-link 描画を auto-wait してから収集する。
  await expect(page.locator('a.nav-link').first()).toBeVisible();
  const hrefs = await page.locator('a.nav-link:visible').evaluateAll(
    els => els.map(e => e.getAttribute('href')).filter(Boolean)
  );
  expect(hrefs.length, 'sidebar should expose multiple nav links').toBeGreaterThan(5);

  for (const href of hrefs) {
    await page.goto('/' + href); // href は '#/...' 形式
    await page.waitForLoadState('domcontentloaded');
    await expect(
      page.getByRole('heading', { name: 'Not Found', exact: true }),
      `nav href ${href} は NotFound に落ちてはならない`
    ).toHaveCount(0);
  }
});


// ===== SPA route-change focus management (WCAG 2.4.3) =====
// SPA は route 遷移で #content を作り直すため、ナビ後に focus が body へ落ちキーボード/SR ユーザが
// 文脈を失う。route 遷移時のみ新ページ h1 へ focus を移す (isRouteChange=hash 変化 かつ
// _focusWasLost=clear 後 activeElement が body の時のみ)。State.update 由来の同一ルート再描画では
// 動かさず (#258 非回帰)、#content 外の生存要素 (command palette input) からは奪わない。
test('Route change moves focus to the new page heading (a11y WCAG 2.4.3)', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.evaluate(() => { location.hash = '#/contact'; });
  await expect(page.locator('#content h1', { hasText: 'Contact' })).toBeVisible();
  await page.waitForTimeout(150);
  const active = await page.evaluate(() => ({
    tag: document.activeElement && document.activeElement.tagName,
    text: document.activeElement && document.activeElement.textContent,
  }));
  expect(active.tag).toBe('H1');
  expect(active.text).toContain('Contact');
});

// ===== sr-only の視覚隠蔽契約 (a11y + AIO entity anchor 隠蔽) =====
// .sr-only は screen reader 専用に content を提供しつつ視覚的には position:absolute + clip +
// 1px で隠す標準ユーティリティ。#page-announcement (route announcer)・#action-announcement・
// AIO entity anchor (Canonical Entity / © footer entity 等・AIO 戦略上 load-bearing) の計 21 要素が
// これに依存する。.sr-only 定義が崩れると隠しテキストが画面に漏れる (視覚バグ + AIO entity anchor
// 露出) が、他の behavior e2e は sr-only の視覚状態を検査せず screenshot は advisory (home のみ) ゆえ
// silent だった。代表 sr-only 要素の bounding box が 1x1 相当 (≤4px) に留まることを検証する。
// .sr-only の position:absolute / clip / width:1px を崩すとテキストが自然幅で描画され bbox が
// 拡大して RED になる (非 vacuous)。
test('sr-only content (route announcer + AIO entity anchor) stays visually hidden', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();

  // #page-announcement — 常在の sr-only route announcer (ルート遷移を SR に通知)
  const announcer = page.locator('#page-announcement');
  await expect(announcer).toHaveCount(1);
  const abox = await announcer.boundingBox();
  expect(abox, '#page-announcement should have a bounding box').not.toBeNull();
  expect(abox.width, '#page-announcement must stay visually hidden (sr-only 1x1)').toBeLessThanOrEqual(4);
  expect(abox.height, '#page-announcement must stay visually hidden (sr-only 1x1)').toBeLessThanOrEqual(4);

  // AIO entity anchor (© footer entity) — AIO 戦略上 load-bearing な sr-only エンティティ情報
  const entity = page.locator('#aio-footer-entity');
  if (await entity.count()) {
    const ebox = await entity.boundingBox();
    expect(ebox, 'AIO entity anchor should have a bounding box').not.toBeNull();
    expect(ebox.width, 'AIO entity anchor must stay visually hidden').toBeLessThanOrEqual(4);
    expect(ebox.height, 'AIO entity anchor must stay visually hidden').toBeLessThanOrEqual(4);
  }
});
