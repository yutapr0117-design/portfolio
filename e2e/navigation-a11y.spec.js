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
    // [FIX] 不在アサーションは初回 poll で成立すると再検査されないため、描画前に評価すると
    //   「NotFound がまだ無い」を「NotFound ではない」と誤認して壊れた nav リンクでも PASS しうる
    //   (多行 assertion ゆえ Check 402 初版の検出からも漏れていた)。h1 の描画を待って確定させる。
    await expect(page.locator('h1').first(), `nav href ${href} でページが描画されない`).toBeVisible();
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
  // route 遷移後の focus 移動は render 内で非同期に起きる。固定 sleep(150ms) は負荷下で焦点移動より
  // 早く評価すると flake るため、expect.poll で activeElement が Contact の H1 になるまでリトライする
  // (焦点が移らない/誤要素へ移る regression では poll が timeout し RED = 非 vacuous を保つ)。
  await expect.poll(async () => page.evaluate(() => {
    const el = document.activeElement;
    return !!(el && el.tagName === 'H1' && (el.textContent || '').includes('Contact'));
  }), { message: 'route change must move focus to the new page Contact H1' }).toBe(true);
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

  // AIO entity anchor (© footer entity) / RAG チャンクアンカー — AIO 戦略上 load-bearing な
  // sr-only エンティティ情報。
  // [FIX] 従来は `if (await entity.count()) { ... }` の skip-on-missing で、要素を丸ごと削除すると
  //   条件が false になりテストが**黙って PASS** する vacuous gate だった (実測: <div
  //   id="aio-footer-entity"> を削除しても本テストは PASS・consistency も 0 errors)。存在を必須に
  //   してから不可視性を検査する (presence は Check 403 が静的にも BLOCKING 強制)。
  for (const id of ['#aio-footer-entity', '#aio-main-footer']) {
    const entity = page.locator(id);
    await expect(entity, `${id} must exist (AIO load-bearing anchor)`).toHaveCount(1);
    const ebox = await entity.boundingBox();
    expect(ebox, `${id} should have a bounding box`).not.toBeNull();
    expect(ebox.width, `${id} must stay visually hidden`).toBeLessThanOrEqual(4);
    expect(ebox.height, `${id} must stay visually hidden`).toBeLessThanOrEqual(4);
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
// NOTE (mutation 非登録の理由): 本テストと下の 'Rapid route switches...' が守るのは
//   **結果** (#content にページが必ず 1 枚・最終ルートが勝つ) であって、それを実現する
//   AbortController 機構そのものではない。実測で `_renderAbortController.abort()` を no-op に
//   しても、さらに 2 箇所の `_signal.aborted` ガードを両方外しても、どちらのテストも緑のまま
//   だった —— ローカル/CI の速度では描画が事実上直列に終わるため abort が発火しない。
//   テストが vacuous なのではなく、**abort 機構には behavioral な観測点が無い** (利用者に
//   見える性質は「ページが 1 枚であること」で、それは abort が無くても成り立つ)。
//   RED を実測できない mutation は安全網に混ぜない規律に従い登録しない。
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

    // ── project-detail (sub-route) の aria-current ────────────────────────────────
    // components.js の Projects nav は `active: route.name.startsWith('project')` で projects と
    // project-detail の両方を active 化する唯一の非-exact-match ロジック。base #/projects だけの検証
    // だと、これを `=== 'projects'` へ退行させても #/projects は両方マッチしてテストが緑のまま、全
    // プロジェクト詳細ページの aria-current(WCAG 2.4.8 Location / 4.1.2) が silent に消える盲点だった。
    // 【非 vacuous 化の要点】直前を #/about にして stale な「プロジェクト」active を消し、detail の
    // h1 描画完了 (sidebar 再描画の同期点) を待ってから検査する。#/projects→detail を直列に並べると
    // 同一ラベル「プロジェクト」の stale 状態を poll が拾って mutated でも緑になる (実測済) ため、
    // 必ず異なるラベルの route を経由する。slug=task-manager は home の主デモ (demoRoute==='task') の
    // 安定 default。startsWith 経路を `=== 'projects'` へ退行させると currents=[] で RED になる。
    await page.goto('/#/about', { waitUntil: 'domcontentloaded' });
    await expect.poll(currents).toEqual(['About']);
    await page.goto('/#/projects/task-manager', { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1', { hasText: 'タスク管理アプリ' })).toBeVisible();
    await expect.poll(currents).toEqual(['プロジェクト']);

    // quiz は route.query.type で active nav が切り替わる (AWS 既定 / PM / 品質)
    await page.goto('/#/quiz?type=pm', { waitUntil: 'domcontentloaded' });
    await expect.poll(currents).toContain('PM 問題集');
    await expect.poll(async () => (await currents()).length).toBe(1);
    await page.goto('/#/quiz?type=quality', { waitUntil: 'domcontentloaded' });
    await expect.poll(currents).toContain('品質・プロセス');

    // 無効な quiz type (#/quiz?type=zzz = stale bookmark / 手打ち) は QuizPage が
    // `QUIZ_DATA_MAP[type] || aws` で AWS へフォールバック描画する。AWS nav の active 述語
    // (`type ∉ {pm,quality,architecture}`) はそのフォールバックを鏡写し、AWS quiz 描画時は必ず
    // AWS nav を aria-current にする (control↔content desync 防止・#781 projects cat= と同 class)。
    // 旧述語 `!type || type==='aws'` は無効 type で AWS 描画なのに nav 無 highlight の desync だった。
    // 直前 #/quiz?type=quality (別ラベル) で stale を消し、AWS quiz h1 を sync point に非 vacuous 化。
    await page.goto('/#/quiz?type=zzinvalid', { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1', { hasText: 'AWS問題集' })).toBeVisible();
    await expect.poll(currents).toEqual(['AWS 問題集']);
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
    // maxHeight は data-collapsed=false で 0→展開値へ CSS transition する。click 直後の即時測定は
    // transition 途中で 0 を拾い間欠赤化する (reflow/transition probe は settle 待ちが必須)。
    // expect.poll で maxHeight>0 に落ち着くまでリトライし、flake を排除しつつ「展開が効く」を検証。
    await expect.poll(
      async () => body.evaluate(el => parseFloat(getComputedStyle(el).maxHeight) || 0),
      { message: '展開時は maxHeight>0 (実際に折りたたみが解除される)' }
    ).toBeGreaterThan(0);
    expect(await page.evaluate(() => localStorage.getItem('portfolio_nav_lab_open_v69'))).toBe('true');

    // 再 click で collapse へ戻る (状態追従の双方向性)
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(body).toHaveAttribute('data-collapsed', 'true');
    expect(await page.evaluate(() => localStorage.getItem('portfolio_nav_lab_open_v69'))).toBe('false');
  });

  // 上のテストは localStorage への WRITE と同一セッション内のトグルを検証するが、reload を跨いだ
  // RESTORE 経路 (components.js isLabOpen() が localStorage を読み戻し labOpen として初期描画へ反映)
  // は未カバーだった。永続の read-back が壊れる (キー相違 / === 'true' 比較崩れ / labOpen 未反映) と
  // reload 後に展開状態が失われるのに、write のみ見る既存テストは素通りする (#294/#568/#684 と同じ
  // field-persist reload round-trip class)。home(#/・Lab は既定 collapsed)で展開→reload→展開維持、
  // collapse→reload→collapse 維持、の両方向 restore を検証する。
  test('Lab nav-group collapse state restores from localStorage across reload (persist round-trip)', async ({ page }) => {
    await page.goto('/#/', { waitUntil: 'domcontentloaded' });
    const toggle = page.locator('.nav-group-toggle').first();
    const body = page.locator('#nav-lab-body');
    // 既定は collapsed。
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');

    // 展開 → localStorage='true' → reload → 展開状態が復元される。
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    expect(await page.evaluate(() => localStorage.getItem('portfolio_nav_lab_open_v69'))).toBe('true');
    await page.reload({ waitUntil: 'domcontentloaded' });
    await expect(page.locator('.nav-group-toggle').first()).toHaveAttribute('aria-expanded', 'true');
    await expect(page.locator('#nav-lab-body')).toHaveAttribute('data-collapsed', 'false');

    // 折りたたみ → localStorage='false' → reload → collapsed が復元される。
    await page.locator('.nav-group-toggle').first().click();
    await expect(page.locator('.nav-group-toggle').first()).toHaveAttribute('aria-expanded', 'false');
    expect(await page.evaluate(() => localStorage.getItem('portfolio_nav_lab_open_v69'))).toBe('false');
    await page.reload({ waitUntil: 'domcontentloaded' });
    await expect(page.locator('.nav-group-toggle').first()).toHaveAttribute('aria-expanded', 'false');
    await expect(page.locator('#nav-lab-body')).toHaveAttribute('data-collapsed', 'true');

    const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
    expect(fatal, `nav-lab restore caused a fatal: ${fatal}`).toBeNull();
  });
});


// ===== ブラウザの戻る/進む (hash ルーティングの中核操作・従来 e2e 完全未被覆) =====
// hash SPA では戻る/進むは hashchange 経由で router に届く。ここが壊れると「戻ると前のページの
// URL になるのに描画は変わらない」「戻ると fatal」といった、利用者が最も戸惑う壊れ方をする。
// 併せて **フィルタ操作が履歴を汚さないこと** を検証する: ProjectsPage の syncURL は
// Router.replaceSilently を使い、検索語 1 文字ごとに履歴 entry を積まない設計になっている。
// これが navigate (pushState) に変わると、3 文字打っただけで「戻る」を 3 回押さないとページを
// 離れられない典型的な SPA 退行になる (実測: replaceSilently なら Back 1 回で前ページへ戻る)。
test('Browser back/forward moves between routes and filtering does not pollute history', async ({ page }) => {
  const routeState = () => page.evaluate(() => ({
    hash: location.hash,
    h1: (document.querySelector('#content h1') || {}).textContent || '',
    fatal: window.__fatalError ? window.__fatalError.message : null,
  }));

  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1')).toBeVisible();

  await page.goto('/#/projects');
  await expect(page.locator('#content h1')).toHaveText('プロジェクト一覧');

  // 1. 戻ると URL だけでなく **描画も** 前のページに戻る (hashchange → render の配線)
  //    NOTE: hash は再描画より先に変わる。hash を poll してから内容を 1 度読むと **再描画前の
  //    stale な内容**を掴んでしまう (この test の初版で実際に踏んだ)。内容側の auto-retry する
  //    assertion で待つこと。
  await page.goBack();
  await expect(page.locator('#content h1')).toContainText('About');
  expect(await page.evaluate(() => location.hash)).toBe('#/about');
  expect((await routeState()).fatal, 'back navigation caused a fatal').toBeNull();

  // 2. 進むも同様
  await page.goForward();
  await expect.poll(async () => (await routeState()).hash).toBe('#/projects');
  await expect(page.locator('#content h1')).toHaveText('プロジェクト一覧');

  // 3. 検索を 3 文字打っても履歴は積まれない → Back 1 回で前ページ (#/about) へ戻る
  const box = page.getByRole('searchbox', { name: 'プロジェクト検索' });
  await box.click();
  await page.keyboard.type('タスク');
  await expect.poll(async () => (await routeState()).hash).toContain('q=');

  await page.goBack();
  await expect(page.locator('#content h1')).toContainText('About');
  expect(await page.evaluate(() => location.hash), 'フィルタ操作が履歴を積んでいたら 1 回の Back では前ページへ戻れない').toBe('#/about');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `history navigation caused a fatal: ${fatal}`).toBeNull();
});

// ===== WCAG 1.4.10 (Reflow): 320px 幅で横スクロールを発生させない =====
// WHY この test が必要か:
//   基底の `.main-content` は `max-width: 1200px; margin: 0 auto` で本文カラムを中央寄せする。
//   ところが `@media (max-width: 920px)` で `.app` が `flex-direction: column` になると、その
//   左右 margin が **cross 軸の auto margin** になる。flexbox 仕様上、cross 軸に auto margin を
//   持つ flex item には `align-self: stretch` が適用されず fit-content でサイズが決まり、
//   fit-content は min-content を下回れないため、本文の min-content が viewport を超えた
//   ルートでは item 自体が viewport より広くなってページ全体が横に溢れていた
//   (実測: role-split +51px / quiz +31px / hiring-risk +28px / pomodoro +16px)。
//   修正は media query 内の `max-width: 100%` 1 行だが、**視覚 baseline では検出できない**
//   (screenshot は 1280x720 clip = 920px 超なのでこの media query に到達しない) ため、
//   回帰を捕まえられるのはこの behavior test だけ。
//
// NOTE: 幅を 320px にするのは WCAG 1.4.10 が「400% ズーム相当 = 320 CSS px」を基準にするため。
//
// NOTE (2026-08-12 実測・再調査不要): **利用者データが長い連続文字列でも**この契約は保たれる。
//   プロジェクト名に改行機会の無い 120 文字を入れて projects / settings を 320px で測ったところ、
//   document の overflow は **0** で、Settings の並べ替えリストは `overflow-x: auto` により
//   **自分のコンテナ内でスクロール**していた (scrollWidth 1284 / clientWidth 238)。
//   この「長文データ版」の test は**追加していない** —— containment を壊す mutation
//   (media query 内の `max-width: 100%` 無効化) を当てても長文版は緑のままで、
//   **RED を実測できないテストは安全網に混ぜない**規律に従った。
//   同じ mutation で本 test は RED (role-split +51px) になるので、契約の番人はこちらで足りている。
test('WCAG 1.4.10: 320px 幅でどのルートも横スクロールしない', async ({ page }) => {
  // 過去に実際あふれていた 4 ルート + あふれていなかった 2 ルート (対照)
  const routes = ['#/role-split', '#/quiz', '#/hiring-risk', '#/apps/pomodoro', '#/', '#/projects'];
  await page.setViewportSize({ width: 320, height: 800 });

  for (const route of routes) {
    await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
    // NOTE: 不在系ではなく「描画され切ったか」を先に待つ。goto 直後に幅を読むと
    // 非同期描画とレースして「まだ狭い」状態を「あふれていない」と誤認する。
    await expect(page.locator('#main-content h1, #main-content h2').first()).toBeVisible();

    const overflow = await page.evaluate(() => {
      const de = document.documentElement;
      return { doc: de.scrollWidth - de.clientWidth, main: Math.round(document.getElementById('main-content').getBoundingClientRect().width) };
    });
    expect(overflow.doc, `${route} が 320px 幅で横に ${overflow.doc}px あふれている (WCAG 1.4.10)`).toBe(0);
    expect(overflow.main, `${route} の #main-content が viewport (320px) より広い`).toBeLessThanOrEqual(320);

    const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
    expect(fatal, `${route} で fatal: ${fatal}`).toBeNull();
  }
});

// 同じ契約を **より厳しい条件** でも通す。ブランド `classic` は本文フォントが Inter になり、
// 既定 (DM Sans) より **約 5.9% 幅広**に描画される (実測 2026-08-18: 同一文字列の幅が
// 248.31px → 262.98px)。既存の gate は既定ブランドしか通しておらず、
// **非既定ブランドでだけあふれる回帰**を素通りさせる。実測では classic でも全ルート 0 だが、
// 幅が広い側を通しておかないと gate が守っているのは「既定フォントでの契約」に留まる。
//
// NOTE: フォントが実際に切り替わっていることを control として確かめる。切り替わらなければ
//   これは既定ブランドの test をもう 1 本増やしただけの vacuous なテストになる。
test('WCAG 1.4.10: 320px 幅で classic ブランド (より幅広なフォント) でもあふれない', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('portfolio_brand_v45', 'classic'));
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto('/#/role-split', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#main-content h1, #main-content h2').first()).toBeVisible();

  // control: ブランドが実際に適用され、Inter 系のフォントで描画されている
  const applied = await page.evaluate(() => ({
    brand: document.documentElement.getAttribute('data-brand'),
    family: getComputedStyle(document.body).fontFamily,
  }));
  expect(applied.brand, 'classic ブランドが適用されていない').toBe('classic');
  expect(applied.family, '本文フォントが Inter 系に切り替わっていない').toContain('Inter');

  for (const route of ['#/role-split', '#/quiz', '#/hiring-risk', '#/apps/pomodoro']) {
    await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#main-content h1, #main-content h2').first()).toBeVisible();
    const doc = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(doc, `${route} が classic ブランドの 320px 幅で横に ${doc}px あふれている`).toBe(0);
  }
});

// ===== WCAG 2.1.1: 再描画で消えるコントロールの focus 復元 =====
// SPA の `State.update` / `window.render()` は #content を作り直すため、change ハンドラを持つ
// コントロール (select / checkbox / number input) は **自分で自分を消してしまう**。実測 (#994) では
// task/todo の絞り込み・タスクの優先度・TODO の完了チェック・ポモドーロの設定のすべてで、
// 変更直後の `document.activeElement` が **BODY** になっていた。
//
// マウス利用者には見えにくいが、キーボード利用者には重い:
//   - focus が body へ落ちるので、続きの Tab は**ドキュメント先頭から**やり直しになる
//   - number input は特に致命的で、ArrowUp の 1 回目で focus を失うため **2 回目以降が効かない**
//     (＝値を 1 段しか動かせない = そのコントロールが実質キーボード操作不能)
//
// 修正は main.js `_renderCore` が「clear の前に focus 中の id を控え、同一ルート再描画で focus が
// 失われていたら同じ id へ戻す」もの。「奪う」のではなく「失われた時だけ復元する」条件は
// route-focus (#267) と共有していて、command palette の input などとは race しない。
test('WCAG 2.1.1: ポモドーロの設定を ArrowUp で連続操作できる (focus が維持される)', async ({ page }) => {
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'ポモドーロ' })).toBeVisible();

  const work = page.locator('#pomo-setting-work');
  await expect(work).toBeVisible();
  const before = Number(await work.inputValue());

  await work.focus();
  await page.keyboard.press('ArrowUp');
  await page.waitForTimeout(300);
  await page.keyboard.press('ArrowUp');
  await page.waitForTimeout(300);

  // 2 回押したら 2 段上がること。focus を失うと 1 段で止まる (実測の壊れ方そのもの)。
  await expect(page.locator('#pomo-setting-work')).toHaveValue(String(before + 2));

  // NOTE: toBeFocused() は並列ワーカーで document が inactive になり間欠 RED になるため使わない。
  const active = await page.evaluate(() => (document.activeElement ? document.activeElement.id : null));
  expect(active, '設定変更のたびに focus が失われている (WCAG 2.1.1)').toBe('pomo-setting-work');
});

test('WCAG 2.1.1: TODO の完了チェックを Space で連続操作できる (focus が維持される)', async ({ page }) => {
  await page.goto('/#/apps/todo', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'TODO' })).toBeVisible();

  const box = page.locator('[id^="todo-check-"]').first();
  await expect(box).toBeVisible();
  const id = await box.getAttribute('id');
  const wasChecked = await box.isChecked();

  await box.focus();
  await page.keyboard.press('Space');
  await page.waitForTimeout(300);
  await expect(page.locator('#' + id)).toBeChecked({ checked: !wasChecked });

  // 2 回目の Space。focus を失っていると Space はページスクロールになり、状態は戻らない。
  await page.keyboard.press('Space');
  await page.waitForTimeout(300);
  await expect(page.locator('#' + id)).toBeChecked({ checked: wasChecked });

  const active = await page.evaluate(() => (document.activeElement ? document.activeElement.id : null));
  expect(active, '1 件チェックするたび focus が失われ、次の項目へ進めない (WCAG 2.1.1)').toBe(id);
});

test('WCAG 2.1.1: 絞り込み select を変更しても focus が select に残る', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' })).toBeVisible();

  // NOTE: ここで `selectOption()` を使ってはいけない。Playwright の selectOption は選択後に
  //   focus を select に残さないため、**修正の有無にかかわらず** activeElement=BODY と読めてしまう
  //   (実測: dispatch 版が復元を観測できたのに selectOption 版は BODY のままだった = 常に false RED)。
  //   キーボードで選択肢を変えたときと同じ「focus したまま change が飛ぶ」形を自分で作る。
  await page.evaluate(() => {
    const el = document.getElementById('task-filter-priority');
    el.focus();
    el.value = 'high';
    el.dispatchEvent(new Event('change', { bubbles: true }));
  });
  await page.waitForTimeout(400);

  await expect(page.locator('#task-filter-priority')).toHaveValue('high');
  const active = await page.evaluate(() => (document.activeElement ? document.activeElement.id : null));
  expect(active, '絞り込みを変えるたび focus が body へ落ち、続きの Tab がドキュメント先頭からになる').toBe('task-filter-priority');
});

// ===== WCAG 2.1.1: 押すと自分自身が消えるボタン =====
// #994 は change を持つコントロール (select / checkbox / number) を扱ったが、**同じことが
// ボタンにも起きる**。onclick が `State.update` を呼べば #content が作り直され、そのボタン自身が
// 消えて focus が body へ落ちる。実測 (#995): タスクの「次のステータスへ進める」・Todo と
// タスクの削除・ポモドーロの開始/モード/リセット・プロジェクトのタグ絞り込みが全て BODY だった。
//
// 復元は **id を持っていた要素だけ** を対象にする opt-in にしてある。無条件にすると、毎秒
// 再描画されるポモドーロ稼働中に「id の無い任意の要素」から h1 へ focus が飛び続けてしまう。
// 元の要素へ戻せない 2 ケース (削除で消えた / 移動後に disabled になった) は #content の h1 へ
// 落とす —— body に残すとドキュメント先頭からの Tab やり直しになるため。
test('WCAG 2.1.1: ポモドーロを開始した後もキーボードで一時停止できる', async ({ page }) => {
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'ポモドーロ' })).toBeVisible();

  const toggle = page.locator('#pomo-toggle');
  await expect(toggle).toContainText('開始');
  await toggle.focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('#pomo-toggle')).toContainText('一時停止');

  // ここで focus を失うと、稼働中は毎秒再描画されるため復帰の機会も無く「開始したら
  // キーボードでは止められない」状態になる。同じキーで戻せることを確かめる。
  await page.keyboard.press('Enter');
  await expect(page.locator('#pomo-toggle')).toContainText('開始');

  const active = await page.evaluate(() => (document.activeElement ? document.activeElement.id : null));
  expect(active, '開始した瞬間に focus が失われている').toBe('pomo-toggle');
});

test('WCAG 2.1.1: タスクをキーボードだけで連続してステータス移動できる', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' })).toBeVisible();

  // NOTE: locator に id を使わない。id を外す mutation で「要素が見つからない」ことによる失敗に
  //   なってしまい、**focus が失われたこと**を検証できたのか帰属できなくなるため、アクセシブル名で
  //   引いて activeElement 側もアクセシブル名で比べる。
  const next = page.getByRole('button', { name: /^次のステータスへ進める：/ }).first();
  await expect(next).toBeVisible();
  const name = await next.getAttribute('aria-label');
  const id = await next.getAttribute('id');
  await next.focus();

  await page.keyboard.press('Enter');
  await page.waitForTimeout(400);
  const mid = await page.evaluate(() => (document.activeElement ? document.activeElement.getAttribute('aria-label') : null));
  expect(mid, '1 段動かすたびに focus が失われ、続けて動かせない').toBe(name);

  // 2 回目で最終ステータスへ。ここでボタンは disabled になるので元へは戻せない。
  // focus() は disabled 要素に対して黙って無効化されるため、**activeElement を読み直して**
  // #content 内 (h1) へ退避できていることを確認する。
  await page.keyboard.press('Enter');
  await page.waitForTimeout(400);
  await expect(page.locator('#' + id)).toBeDisabled();
  const end = await page.evaluate(() => {
    const a = document.activeElement;
    return { tag: a ? a.tagName : 'null', inContent: !!(a && document.getElementById('content').contains(a)) };
  });
  expect(end.inContent, `最終ステータスへ移動後 focus が #content の外 (${end.tag}) にある`).toBe(true);
});

test('WCAG 2.1.1: 項目を削除しても focus が本文内に残る', async ({ page }) => {
  await page.goto('/#/apps/todo', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'TODO' })).toBeVisible();

  // locator に id を使わない理由は上の test の NOTE と同じ。
  const del = page.getByRole('button', { name: /^削除：/ }).first();
  await expect(del).toBeVisible();
  await del.focus();
  await page.keyboard.press('Enter');
  await page.waitForTimeout(400);

  // 削除ボタンは自分自身を消すので元の要素へは戻せない。body に残すとドキュメント先頭からの
  // Tab やり直しになるため、少なくとも #content 内へ退避していることを要求する。
  const res = await page.evaluate(() => {
    const a = document.activeElement;
    return { tag: a ? a.tagName : 'null', inContent: !!(a && document.getElementById('content').contains(a)) };
  });
  expect(res.inContent, `削除後に focus が #content の外 (${res.tag}) へ落ちている`).toBe(true);
});

test('WCAG 2.1.1: プロジェクトのタグ絞り込みは検索欄へ focus を移す', async ({ page }) => {
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();

  const tag = page.getByRole('button', { name: '#ツール' }).first();
  await expect(tag).toBeVisible();
  await tag.focus();
  await page.keyboard.press('Enter');
  await page.waitForTimeout(400);

  // このボタンは grid 内に居るので renderGrid() が自分自身を消す (_renderCore の復元経路は
  // 通らない手動再描画)。検索欄へ移すと「タグを検索語に入れた」結果そのものが focus 先になる。
  const res = await page.evaluate(() => {
    const a = document.activeElement;
    return { label: a ? a.getAttribute('aria-label') : null, value: a ? a.value : null };
  });
  expect(res.label, 'タグを押すと focus が body へ落ちる').toBe('プロジェクト検索');
  expect(res.value).toBe('ツール');
});

// ===== WCAG 2.1.1: サイドバーの focus は再描画を越えて残るか =====
// `_renderCore` は #content だけでなく **sidebar も毎回作り直す**。ポモドーロは稼働中に毎秒
// 再描画するので、id が無かった頃はキーボード利用者が **タイマーが動いている間サイドバーに
// focus を留めておけなかった** (実測 #997: 開始した瞬間に BODY、focus し直しても 1 秒で BODY)。
test('WCAG 2.1.1: ポモドーロ稼働中でもサイドバーに focus を留められる', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'ポモドーロ' })).toBeVisible();

  // 実際の順番どおり「開始してからキーボードでサイドバーへ移動する」を再現する。
  // NOTE: 先にサイドバーへ focus してから click() すると、**click 自体がボタンへ focus を移す**ので
  //   何を検証しているのか分からなくなる (最初にこれで誤検出した)。
  await page.locator('#pomo-toggle').click();
  await expect(page.locator('#pomo-toggle')).toContainText('一時停止');

  // NOTE: locator に復元用の id を使わない。id を外す mutation が「要素が見つからない」で
  //   落ちると、**focus が失われたこと**を検証できたのか帰属できなくなる。href で引いて
  //   activeElement 側も href で比べる (id が無くても両者は解決する)。
  await page.locator('#sidebar a.nav-link[href="#/"]').focus();
  const idOf = () => page.evaluate(() => {
    const a = document.activeElement;
    return a ? (a.getAttribute('href') || a.id || a.tagName) : null;
  });
  expect(await idOf()).toBe('#/');

  // 2 tick 以上またいで観測する。NOTE: ここは「変化しないこと」の検査なので expect.poll を
  //   使わない (poll は最初の観測で成立した瞬間に成功し、その後の喪失を見逃す)。
  await page.waitForTimeout(2200);
  expect(await idOf(), 'タイマーが動いている間サイドバーに focus を留められない (毎秒 body へ落ちる)').toBe('#/');
});

// sidebar と drawer は同じ navLink 実装を共有し、mobile では **両方が同時に DOM 上へ存在する**
// (sidebar は display:none で残るだけ)。focus 復元は getElementById を鍵にしているため、
// id が衝突すると復元先が別物になり、aria の id 参照も壊れる。
test('sidebar と drawer の nav が id を衝突させない', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'ポモドーロ' })).toBeVisible();
  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  const dup = await page.evaluate(() => {
    const seen = new Set(); const dups = [];
    document.querySelectorAll('[id]').forEach(e => {
      if (seen.has(e.id)) { dups.push(e.id); }
      seen.add(e.id);
    });
    return dups;
  });
  expect(dup, `重複 id: ${dup.join(', ')}`).toEqual([]);
  // drawer 側にも復元用の id が実在すること (接頭辞違いで両方揃っているのが正)
  await expect(page.locator('#drawernav-home')).toHaveCount(1);
  await expect(page.locator('#sidenav-home')).toHaveCount(1);
});

// drawer 側の Lab グループが「自分の」本体を開閉すること (相手側を掴んでいないこと)。
// 従来は id がハードコードで sidebar と drawer が同じ `nav-lab-body` を持っていたため、
// getElementById が DOM 順で先に来た方を返し、どちらのトグルがどちらを開けるかが
// **構築順という偶然**に委ねられていた。
test('drawer の Lab トグルは drawer 側の本体だけを開閉する', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  const drawerBody = page.locator('#drawer-nav-lab-body');
  const sidebarBody = page.locator('#nav-lab-body');
  await expect(drawerBody).toHaveCount(1);
  await expect(sidebarBody).toHaveCount(1);

  const before = await sidebarBody.getAttribute('data-collapsed');
  await page.locator('#drawernav-lab-toggle').click();
  await page.waitForTimeout(300);

  await expect(drawerBody).toHaveAttribute('data-collapsed', String(before !== 'true'));
  // sidebar 側は触られていないこと (aria-controls を辿らずハードコード id を掴むと、ここが動く)
  await expect(sidebarBody).toHaveAttribute('data-collapsed', String(before));
  await expect(page.locator('#drawernav-lab-toggle')).toHaveAttribute('aria-controls', 'drawer-nav-lab-body');
});

// ===== 静的ページの CTA が「宣言どおりの中身」へ着地すること =====
// Check 395 は `path:` が **実在ルート**へ解決することを静的に強制するが、**query パラメータの
// 中身までは見ない**。`quiz?type=pm` を `quiz?type=pmm` と打ち間違えても route は存在するので
// Check は緑のまま、実際には **既定の AWS 問題集が silent に表示される** (#926 の own-key ガードで
// crash はしないが、falls back するだけで誰にも伝わらない)。
// 採用担当が hiring-risk から辿る導線なので、「PM 問題集を見る」で PM 問題集が出ることは
// 主張そのもの。実測 (#1027) では 12 件の CTA すべてが期待どおりに着地していた。
test('hiring-risk の問題集 CTA が宣言どおりの問題集へ着地する', async ({ page }) => {
  for (const [label, expected] of [['PM問題集を見る', 'PM問題集'], ['品質問題集を見る', '品質・プロセス問題集']]) {
    await page.goto('/#/hiring-risk', { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1', { hasText: '採用' })).toBeVisible();

    await page.getByRole('button', { name: label, exact: true }).first().click();

    // 着地先の見出しで「どの問題集か」を確かめる (route が存在するだけでは足りない)
    await expect(page.locator('#content h1'),
      `${label} が ${expected} 以外へ着地した (query の type が違う可能性)`).toContainText(expected);

    const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
    expect(fatal, `${label} の遷移で fatal: ${fatal}`).toBeNull();
  }
});

// ===== ルート描画の実コストに上限を置く (runtime の perf 回帰ゲート) =====
// Check 120 は **byte weight** を見るが、**描画にかかる時間**を見ている層は無かった。
// 例えば quiz renderer に O(n²) が入っても、byte も行数も e2e の合否も変わらないまま
// 体感だけが劣化する。
//
// 実測 (#1028) の内訳:
//   通常 (View Transition あり) : 275〜307ms  ← ほぼ全部がアニメーション
//   reduced-motion (transition skip): 11〜25ms  ← これが**実際の描画仕事**
// つまり体感遅延の ~95% は意図的なアニメーションで、描画自体は 24,500 文字の quiz でも 25ms。
//
// アニメーション時間を含めると「意図的な演出」を測ることになり、閾値も CI 負荷で揺れる。
// **reduced-motion で測る**ことで純粋な描画コストだけを見る。閾値は実測の 12〜27 倍の
// 余裕を取り、桁が変わる回帰だけを捕まえる (微小な揺れで赤くならないように)。
test('ルート描画の実コストが桁で悪化していない (reduced-motion で測定)', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();

  for (const hash of ['#/projects', '#/quiz', '#/apps/task']) {
    const r = await page.evaluate(async (h) => {
      const c = () => document.getElementById('content');
      const before = c().textContent.length;
      const t0 = performance.now();
      location.hash = h;
      // NOTE: aria-busy=false だけを待つと **前の描画で既に false** なので即座に成立する
      //   (実測で全ルート 0ms・同じ node 数という無意味な値になった)。本文が入れ替わるまで待つ。
      await new Promise((res) => {
        const check = () => {
          const el = c();
          if (el && el.getAttribute('aria-busy') === 'false' && el.textContent.length !== before) { res(); }
          else { requestAnimationFrame(check); }
        };
        check();
      });
      const el = c();
      return { ms: Math.round(performance.now() - t0), chars: el.textContent.length };
    }, hash);

    // control: 実際に中身が描画されたこと (0 文字なら何も測っていない)
    expect(r.chars, `${hash}: 本文が描画されていない — 測定が成立していない`).toBeGreaterThan(30);
    expect(r.ms, `${hash} の描画が ${r.ms}ms — 実測基準 (11〜25ms) から桁で悪化している`).toBeLessThan(300);
  }
});
