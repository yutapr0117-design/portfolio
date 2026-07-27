const { test, expect } = require('@playwright/test');


// ===== 7.2: skip link が main コンテンツへ focus を移す (WCAG 2.4.1 Bypass Blocks) =====
// `<a href="#main-content" class="skip-link">` はキーボード利用者がナビを飛ばして本文へ直接
// 到達する手段。focus → Enter で focus が #main-content (tabindex=-1) へ移ることを検証する。
// また hash routing (#/...) と競合して NotFound に落ちたり focus が移らない退行も同時に防ぐ。
// 【非 home 始点が必須】: 旧テストは home(`/`) 始点で「skip-link が hash を #main-content に変え
// hashchange→router が home 再描画してユーザーを現在ページから飛ばす」バグを home→home ゆえ
// vacuous に見逃していた。#/projects 始点にし、focus 移動 + 現在ルート(表示 h1・URL hash)の保持を
// 同時検証する。main.js の skip-link preventDefault ハンドラを外すと home hero が描画され RED。
test('Skip link moves focus to #main-content without navigating away from the current route (WCAG 2.4.1)', async ({ page }) => {
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => !!document.querySelector('#content h1, #content .h1'));
  // 前提: Projects ページが描画されている
  await expect(page.getByRole('heading', { name: 'プロジェクト一覧' })).toBeVisible();

  const skip = page.locator('.skip-link');
  await skip.focus();
  await expect(skip).toBeFocused();

  await skip.press('Enter');
  // (a) focus が #main-content へ移る
  await expect(page.locator('#main-content')).toBeFocused();
  // (b) 現在ルートが保持される: Projects の見出しが残り、home hero へ誤遷移していない
  await expect(page.getByRole('heading', { name: 'プロジェクト一覧' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'AI を自走させ、統治する PM' })).toHaveCount(0);
  // (c) URL hash が #/projects のまま (native fragment 挙動で #main-content に desync しない)
  await expect(page).toHaveURL(/#\/projects$/);
  // (d) NotFoundPage に落ちていない
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

// ===== 7.3: 重なった再描画で #content の integrity が保たれる (no dup / no empty) =====
// main.js の _renderCore は「clear(content) → build → appendChild(page)」を各描画で行い、
// 重なった描画は AbortController lifecycle (新 render が前 render の signal を abort・前 render は
// await 後の `_signal.aborted` で return) + clear-before-append で協調する。結果として、
// 短時間に複数の render() が重なっても #content は「ちょうど 1 ページ」に収束し、二重描画
// (h1 が複数) にも空 (h1 が 0) にもならない。この observable integrity 不変条件は e2e で未被覆
// だった。**非 vacuity 実測**: clear(content) を除去すると 6 回の重なり描画が 6 ページ append され
// h1 が 6 つになり toHaveCount(1) が RED (確認済)。abort-check 自体の除去は clear-before-append の
// last-wins ゆえ本 observable では benign (これは overclaim しない — 本テストが守るのは integrity)。
test('Overlapping re-renders keep #content intact — exactly one page, no dup/empty', async ({ page }) => {
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();

  // 同一 microtask 内で複数 render() を発火 — 各 render が前の render を mid-flight で abort する
  await page.evaluate(() => { for (let i = 0; i < 6; i++) { if (window.render) { window.render(); } } });

  // 最終状態: プロジェクト一覧が「ちょうど 1 つ」描画され、空でも二重でもない
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toHaveCount(1);
  await expect(page.locator('.grid-projects')).toBeVisible();
  const fatal = await page.evaluate(() => window.__fatalError);
  expect(fatal, `overlapping re-render caused a fatal: ${fatal}`).toBeNull();
});

// 重なった「ルート遷移」でも最終ルートが正しく描画される (hashchange 連打 → 最後の route が勝つ)。
test('Rapid route switches settle on the final route intact (render abort under nav)', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();

  // 連続で hash を切り替え — router の transition-lock replay + _renderCore abort が協調する
  await page.evaluate(() => {
    location.hash = '#/projects';
    location.hash = '#/about';
    location.hash = '#/quiz';
  });

  // 最終ルート = quiz が「実際に」描画される (URL=quiz なのに表示=about のままの
  // transition-lock replay desync = #167 FIX の回帰を捕捉するため quiz 固有要素で確認)。
  await expect.poll(() => page.evaluate(() => location.hash)).toBe('#/quiz');
  await expect(page.locator('input[aria-label="問題検索"]')).toBeVisible();
  await expect(page.locator('#content h1')).toHaveCount(1);
  const fatal = await page.evaluate(() => window.__fatalError);
  expect(fatal, `rapid route switch caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.4: sidebar nav の aria-current が現在ルートを正しく指し、遷移で追従する (WCAG 2.4.8) =====
// sidebar の nav link は現在ルートに `aria-current="page"` を付け、SR/支援技術の利用者へ「今どこに
// いるか」を伝える (WCAG 2.4.8 Location)。active 判定は route.name ベース (projects は startsWith で
// project-detail も内包、quiz は route.query.type で AWS/PM/品質/設計を区別)。この observable は
// e2e 未被覆で、active 判定が壊れても (例: 常時 active / 誤 item / 複数点灯) どのテストも捕捉しなかった。
// desktop viewport (sidebar 表示) で各ルートの aria-current が「ちょうど 1 個・正しい nav ラベル」を
// 指し、ルート遷移・quiz type 切替に追従することを検証する。
test.describe('sidebar aria-current follows the current route (WCAG 2.4.8)', () => {
  test.use({ viewport: { width: 1280, height: 900 } });
  test('aria-current marks exactly the active nav item across routes and quiz types', async ({ page }) => {
    const currents = async () => page.evaluate(() =>
      [...document.querySelectorAll('.sidebar [aria-current="page"], nav [aria-current="page"]')]
        .map(el => (el.textContent || '').trim())
    );

    for (const [route, label] of [
      ['#/about', 'About'],
      ['#/apps/task', 'タスク管理'],
      ['#/apps/pomodoro', 'ポモドーロ'],
      ['#/projects', 'プロジェクト'],
      ['#/settings', '設定・データ'],
    ]) {
      await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
      await expect.poll(currents).toContain(label);
      // ちょうど 1 個 (誤って複数 nav が aria-current になる回帰を捕捉)
      await expect.poll(async () => (await currents()).length).toBe(1);
    }

    // quiz は route.query.type で active nav が切り替わる (AWS 既定 / PM / 品質)
    await page.goto('/#/quiz?type=pm', { waitUntil: 'domcontentloaded' });
    await expect.poll(currents).toContain('PM 問題集');
    await expect.poll(async () => (await currents()).length).toBe(1);
    await page.goto('/#/quiz?type=quality', { waitUntil: 'domcontentloaded' });
    await expect.poll(currents).toContain('品質・プロセス');
  });
});

// ===== 7.5: sidebar の Lab nav グループ折りたたみトグル (WCAG 4.1.2 状態 + 折りたたみ + 永続化) =====
// sidebar 下部の Lab グループ ("Lab▼") は nav-group-toggle で開閉する collapsible。toggleLab は
// (1) aria-expanded を状態に追従 (WCAG 4.1.2 Name/Role/Value)、(2) body(#nav-lab-body) の
// data-collapsed + maxHeight で実際に折りたたみ、(3) localStorage(portfolio_nav_lab_open_v69) へ永続化
// する。この observable は e2e 未被覆で、aria-expanded が状態に追従しない / 折りたたみが効かない /
// aria-controls が実在しない 等の回帰をどのテストも捕捉しなかった。home ルート (Lab は既定 collapsed)
// で開閉を検証する。
test.describe('sidebar Lab nav-group collapse toggle (WCAG 4.1.2 + collapse + persistence)', () => {
  test.use({ viewport: { width: 1280, height: 900 } });
  test('toggle flips aria-expanded, collapses #nav-lab-body, and persists', async ({ page }) => {
    await page.goto('/#/', { waitUntil: 'domcontentloaded' });
    const toggle = page.locator('.nav-group-toggle').first();
    await expect(toggle).toBeVisible();

    // aria-controls が実在する body を指す (dangling 参照でない)
    await expect(toggle).toHaveAttribute('aria-controls', 'nav-lab-body');
    const body = page.locator('#nav-lab-body');
    await expect(body).toHaveCount(1);

    // home では Lab は既定で collapsed (aria-expanded=false / data-collapsed=true)
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(body).toHaveAttribute('data-collapsed', 'true');

    // click で展開: aria-expanded=true / data-collapsed=false / maxHeight>0 / localStorage 永続化
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await expect(body).toHaveAttribute('data-collapsed', 'false');
    const maxH = await body.evaluate(el => parseFloat(getComputedStyle(el).maxHeight) || 0);
    expect(maxH, '展開時は maxHeight>0 (実際に折りたたみが解除される)').toBeGreaterThan(0);
    expect(await page.evaluate(() => localStorage.getItem('portfolio_nav_lab_open_v69'))).toBe('true');

    // 再 click で collapse へ戻る (状態追従の双方向性)
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(body).toHaveAttribute('data-collapsed', 'true');
    expect(await page.evaluate(() => localStorage.getItem('portfolio_nav_lab_open_v69'))).toBe('false');
  });
});
