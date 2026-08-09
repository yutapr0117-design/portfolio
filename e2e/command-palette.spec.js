const { test, expect } = require('@playwright/test');


// ===== 7.2: コマンドパレット (Cmd/Ctrl+K) 横断ナビ =====
// js/command-palette.js は Cmd/Ctrl+K で overlay を開き、入力で行き先を絞り込み、Enter/クリックで
// Router.navigate、Esc/背景で閉じる純追加機能 (新ルート無し)。検索 input / category / タグに続く
// 第 4 のナビ導線で未カバー。CI は linux ゆえ Control+k。open→絞込→遷移→close と Esc-close を検証。
test('Command palette (Ctrl+K) opens, filters, navigates, and closes', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const host = page.locator('#command-palette-host');
  const cmdInput = page.locator('.cmdk-input');

  // 開く: Ctrl+K で overlay 表示 + input フォーカス
  await page.keyboard.press('Control+k');
  await expect(host).toHaveAttribute('aria-hidden', 'false');
  await expect(cmdInput).toBeFocused();

  // 絞り込み → 候補がフィルタされる
  await cmdInput.fill('projects');
  await expect(page.locator('.cmdk-item').first()).toBeVisible();

  // Enter で先頭候補へ遷移 + パレットが閉じる
  await page.keyboard.press('Enter');
  await expect(host).toHaveAttribute('aria-hidden', 'true');
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();

  // 再度開いて Esc で閉じる (行き止まりでない)
  await page.keyboard.press('Control+k');
  await expect(host).toHaveAttribute('aria-hidden', 'false');
  await page.keyboard.press('Escape');
  await expect(host).toHaveAttribute('aria-hidden', 'true');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `command palette caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: コマンドパレットの focus trap が Tab で背景へ抜けない (回帰) =====
// palette panel は aria-modal="true" role="dialog" で、開いている間 focus を overlay 内に
// 封じ込めるべき (docstring も明言)。修正前は trapHandler が Tab を一切処理せず、唯一の
// focusable な input から Tab を押すと背景コンテンツへ focus が抜けていた (ARIA modal 違反)。
// Tab/Shift+Tab 後も focus が #command-palette-host 内に留まることを検証する。
test('Command palette traps Tab focus inside the modal (a11y regression)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const host = page.locator('#command-palette-host');
  await page.keyboard.press('Control+k');
  await expect(host).toHaveAttribute('aria-hidden', 'false');
  await expect(page.locator('.cmdk-input')).toBeFocused();

  // Tab を複数回押しても focus が overlay 内 (#command-palette-host 配下) に留まる。
  // (注: cmdk-list <ul> は overflow スクローラとして Tab-focusable なため、Tab 1 回では
  //  input→UL で偶然 host 内に留まり区別できない。修正前は 2 回目の Tab で UL→背景へ抜ける。
  //  複数回 Tab して初めて trap の有無を検出できる＝vacuous でない回帰テスト。)
  for (let i = 0; i < 4; i++) { await page.keyboard.press('Tab'); }
  let inside = await page.evaluate(() => {
    const h = document.getElementById('command-palette-host');
    return !!h && h.contains(document.activeElement);
  });
  expect(inside, 'repeated Tab should not move focus outside the open command palette').toBe(true);

  // Shift+Tab でも同様 (逆方向の trap)
  for (let i = 0; i < 4; i++) { await page.keyboard.press('Shift+Tab'); }
  inside = await page.evaluate(() => {
    const h = document.getElementById('command-palette-host');
    return !!h && h.contains(document.activeElement);
  });
  expect(inside, 'repeated Shift+Tab should not move focus outside the open command palette').toBe(true);

  await page.keyboard.press('Escape');
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `command palette focus trap caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: コマンドパレットがプロジェクトも検索対象にする (omni-nav) =====
// createCommandPalette は固定 NAV に State の現在プロジェクト一覧を加えて検索する。プロジェクト名で
// 絞り込み → 選択で projects/<slug> の詳細へ飛べることを検証する (top-nav 専用でない omni-nav)。
test('Command palette searches projects and jumps to a project detail', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const cmdInput = page.locator('.cmdk-input');
  await page.keyboard.press('Control+k');
  await cmdInput.fill('タスク管理');

  // プロジェクト候補 (default p01 'タスク管理アプリ') が出る
  const projItem = page.locator('.cmdk-item', { hasText: 'タスク管理アプリ' }).first();
  await expect(projItem).toBeVisible();
  await projItem.click();

  // プロジェクト詳細へ遷移 (「← 一覧に戻る」が出る = ProjectDetailPage) + パレットが閉じる
  await expect(page.getByRole('button', { name: '← 一覧に戻る' })).toBeVisible();
  await expect(page.locator('#command-palette-host')).toHaveAttribute('aria-hidden', 'true');
});


// command palette から Markdown ノートアプリ (apps/notes) へ遷移できることを behavioral に検証。
// Check 128 は NAV エントリの「存在」を静的に強制するが、実遷移は未カバーだった。notes は A 群で
// 後追加され Cmd+K から到達不能だったバグ (#257) の回帰防止 = 実 destination が機能することを担保。
test('Command palette navigates to the Markdown notes app', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.keyboard.press('Control+k');
  await page.locator('.cmdk-input').fill('ノート');
  const notesItem = page.locator('.cmdk-item', { hasText: 'ノート' }).first();
  await expect(notesItem).toBeVisible();
  await notesItem.click();
  // notes アプリへ遷移 (textarea#notes-input が出る) + パレットが閉じる
  await expect(page.locator('#notes-input')).toBeVisible();
  await expect(page.locator('#command-palette-host')).toHaveAttribute('aria-hidden', 'true');
});

// ===== WAI-ARIA combobox: aria-activedescendant が arrow 移動に同期 (a11y regression) =====
// cmdk は focus を input に留めたまま ↑↓ で listbox を操作する combobox パターン。SR が active
// option をアナウンスするには input の aria-activedescendant が active option の id へ同期していな
// ければならない (option の aria-selected 単独では focus が移らず一部 SR で読み上げられない)。
// 本テストは open 直後に先頭 option (cmdk-opt-0) を指し、ArrowDown で cmdk-opt-1 へ同期することを
// 検証する。fix (aria-activedescendant 同期) を戻すと属性が更新されず RED になる non-vacuous ガード。
test('Command palette input tracks active option via aria-activedescendant', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  const cmdInput = page.locator('.cmdk-input');
  await page.keyboard.press('Control+k');
  await expect(page.locator('#command-palette-host')).toHaveAttribute('aria-hidden', 'false');
  // combobox セマンティクスが配線されている
  await expect(cmdInput).toHaveAttribute('role', 'combobox');
  await expect(cmdInput).toHaveAttribute('aria-controls', 'cmdk-listbox');
  // 描画直後は先頭 option が active
  await expect(cmdInput).toHaveAttribute('aria-activedescendant', 'cmdk-opt-0');
  // ArrowDown で 2 番目の option へ active が移り、activedescendant も同期する
  await page.keyboard.press('ArrowDown');
  await expect(cmdInput).toHaveAttribute('aria-activedescendant', 'cmdk-opt-1');
  // 指し先の option が実在し aria-selected=true である (dangling id 参照でない)
  await expect(page.locator('#cmdk-opt-1')).toHaveAttribute('aria-selected', 'true');
});

// ===== close 後に focus を起動元へ復元する (WCAG 2.4.3 focus order / a11y regression) =====
// palette は open 時に lastFocused=document.activeElement を保持し、close 時に lastFocused.focus()
// で直前 focus を復元する。open 時の focus-trap / restore は別テストが input への focus を見るが、
// 「Esc で閉じた後に開く前の要素へ focus が戻る」復元経路は未カバーだった。復元を欠くと SR/keyboard
// ユーザーは閉じた後に focus を失い body へ落ちる (文脈喪失)。常在の .skip-link を起動元 focus にし、
// Ctrl+K→Esc 後に .skip-link へ focus が戻ることを検証する。close() の lastFocused.focus() を外すと
// RED になる non-vacuous ガード。
test('Command palette restores focus to the opener on close (a11y regression)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  const opener = page.locator('.skip-link');
  await opener.focus();
  await expect(opener).toBeFocused();
  // 開く → input へ focus が移る
  await page.keyboard.press('Control+k');
  await expect(page.locator('.cmdk-input')).toBeFocused();
  // Esc で閉じる → 起動元 (.skip-link) へ focus が復元される
  await page.keyboard.press('Escape');
  await expect(page.locator('#command-palette-host')).toHaveAttribute('aria-hidden', 'true');
  await expect(opener).toBeFocused();
});


// ===== drawer が開いている状態で Cmd/Ctrl+K を押しても「開くモーダルは常に 1 つ」 =====
// 修正前は mobile drawer と command palette が **同時に開き**、aria-modal="true" の領域が 2 つ
// 同時に有効になっていた (実測: drawer=open かつ palette=open)。SR にはどちらが現在のモーダルか
// 判別できず、両者の focus trap も同時に動く。さらに Escape ハンドラが両方とも document keydown で
// 走るため **Escape 1 回で両方閉じる** (preventDefault は同一要素上の他リスナーを止めない・
// #262 の二重発火と同族)。palette の open() が先に drawer を閉じることで根本を断つ。
// 注: drawer は position:fixed のため offsetParent が null になり `offsetParent !== null` 方式の
// 可視判定は誤って "閉じている" と報告する。getBoundingClientRect + computed style で判定する。
test('Opening the command palette closes the mobile drawer (never two modals at once)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/');
  await page.waitForLoadState('domcontentloaded');

  const state = () => page.evaluate(() => {
    const shown = (el) => {
      if (!el) { return 'absent'; }
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return (cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0 && r.right > 0) ? 'open' : 'closed';
    };
    return {
      drawer: shown(document.getElementById('drawer')),
      palette: shown(document.querySelector('.cmdk-panel')),
      // palette の入力は id を持たず class 識別 (実測: className='cmdk-input')。
      // id を期待すると常に '' で false-red になる。
      focus: (document.activeElement && String(document.activeElement.className || '')) || '',
    };
  });

  // drawer を開く (この時点では drawer だけが開いている)
  await page.locator('#menuBtn').click();
  await expect.poll(async () => (await state()).drawer).toBe('open');

  // Cmd+K で palette を開く → drawer は閉じ、palette だけが開く
  await page.keyboard.press('Meta+k');
  await expect.poll(async () => (await state()).palette).toBe('open');
  const both = await state();
  expect(both.drawer, 'palette を開いたら drawer は閉じていなければならない (二重モーダル禁止)').toBe('closed');
  expect(both.focus, 'focus は palette の入力にある').toContain('cmdk-input');

  // 可視な aria-modal は常に 1 つ以下
  const visibleModals = await page.evaluate(() => [...document.querySelectorAll('[aria-modal="true"]')]
    .filter(el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
      return cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0 && r.right > 0; }).length);
  expect(visibleModals, '可視な aria-modal は 1 つだけであること').toBe(1);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `overlay interaction caused a fatal: ${fatal}`).toBeNull();
});


// ===== 逆順 (palette 表示中に drawer を開く) でも「開くモーダルは常に 1 つ」 =====
// palette を先に閉じる対の処理が drawer 側 (openDrawer) にも要る。command palette は overlay で
// あって #app の inert 対象ではないため、**palette 表示中も #topbar の menuBtn はクリックでき**、
// そのまま drawer が開くと aria-modal="true" が 2 つ同時に有効になる (実測: visibleModals=2)。
// 片方向だけ塞ぐと「1 ケースだけ処理して他を忘れる」非対称バグとして残る (CLAUDE.md §7 の反復 class)。
test('Opening the drawer closes the command palette (the reverse direction)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/');
  await page.waitForLoadState('domcontentloaded');

  const state = () => page.evaluate(() => {
    const shown = (el) => {
      if (!el) { return 'absent'; }
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return (cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0 && r.right > 0) ? 'open' : 'closed';
    };
    return {
      drawer: shown(document.getElementById('drawer')),
      palette: shown(document.querySelector('.cmdk-panel')),
      visibleModals: [...document.querySelectorAll('[aria-modal="true"]')].filter(el => {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        return cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0 && r.right > 0;
      }).length,
    };
  });

  // palette を先に開く
  await page.keyboard.press('Meta+k');
  await expect.poll(async () => (await state()).palette).toBe('open');

  // その状態で menuBtn を押す (実機タップ相当。Playwright の通常 click は actionability で
  // スクロールしうるため programmatic click を使う — #297 で確立した手法)
  await page.evaluate(() => document.getElementById('menuBtn').click());
  await expect.poll(async () => (await state()).drawer).toBe('open');

  const after = await state();
  expect(after.palette, 'drawer を開いたら palette は閉じていなければならない (二重モーダル禁止)').toBe('closed');
  expect(after.visibleModals, '可視な aria-modal は 1 つだけであること').toBe(1);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `reverse overlay interaction caused a fatal: ${fatal}`).toBeNull();
});


// ===== palette 表示中は背景 (#app) を inert + aria-hidden にする (drawer と同じ契約) =====
// mobile drawer は開放時に __setAppInert(true) で背景を inert + aria-hidden + pointer-events:none に
// するのに、command palette は行っていなかった (実測: drawer=inert true / palette=inert false)。
// **同じ「モーダル」でありながら背景の扱いが非対称**という #262/#946 と同族の抜け。
// aria-modal="true" だけに頼ると (a) aria-modal の解釈が AT/ブラウザ組み合わせで揺れ背景を読み
// 進められる (b) 背景がポインタで操作できる。drawer と同じ唯一の実装を共有して揃えた。
// close 側の解除も検証する — 解除漏れは「操作不能な app が residual に残る」最悪の失敗になるため。
test('Command palette makes the background inert while open and restores it on close', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/');
  await page.waitForLoadState('domcontentloaded');

  const appState = () => page.evaluate(() => {
    const app = document.getElementById('app');
    return {
      inert: !!(app && app.hasAttribute('inert')),
      ariaHidden: app ? app.getAttribute('aria-hidden') : null,
      pointerEvents: app ? app.style.pointerEvents : '',
    };
  });

  // 初期状態は背景が生きている (これを確認しないと「常に inert」でも緑になる vacuous テストになる)
  const before = await appState();
  expect(before.inert, '初期状態では背景は inert でない').toBe(false);
  expect(before.ariaHidden, '初期状態では aria-hidden も付いていない').toBeNull();

  await page.keyboard.press('Meta+k');
  await expect.poll(async () => (await appState()).inert).toBe(true);
  const open = await appState();
  expect(open.ariaHidden, 'palette 表示中は背景が AT から隠される').toBe('true');
  expect(open.pointerEvents, 'palette 表示中は背景がポインタ操作を受け付けない').toBe('none');

  // 閉じたら必ず解除される
  await page.keyboard.press('Escape');
  await expect.poll(async () => (await appState()).inert).toBe(false);
  const closed = await appState();
  expect(closed.ariaHidden, 'close 後に aria-hidden が残ってはならない').toBeNull();
  expect(closed.pointerEvents, 'close 後に pointer-events:none が残ってはならない').not.toBe('none');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `palette inert handling caused a fatal: ${fatal}`).toBeNull();
});


// ===== palette の開閉がスクロール位置を壊さない (scroll-clobber 回帰防止) =====
// 2 つの独立した原因で「Cmd/Ctrl+K を押したら / 閉じたらページ先頭へ飛ぶ」が起きていた:
//  (1) open 側: 二重モーダル防止で palette が open() 時に closeDrawer() を無条件に呼ぶが、
//      closeDrawer は末尾の __lockBodyScroll(false) で window.scrollTo(0, __drawerScrollY) を実行する。
//      drawer を一度も開いていなければ __drawerScrollY=0 なので **閉じている drawer を閉じるだけで
//      先頭へ飛ぶ**。openDrawer にはあった idempotency ガードが closeDrawer に無い非対称が原因
//      (#297 のガードの対)。
//  (2) close 側: focus 復元が素の focus() で、対象を viewport 内へスクロールしてしまう。lastFocused は
//      しばしばページ冒頭の h1 (route 遷移で #267 が focus を移す先) なので、ほぼ必ず先頭ジャンプになる。
//      main.js の route-focus と同じく preventScroll を使う。
// drawer 経路が従来どおり位置を復元することも併せて確認する (片方の修正で他方を壊さない)。
test('Opening and closing the command palette preserves the scroll position', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  // 十分な高さがあることを確認してからスクロールする (短いページでは常に 0 で vacuous になる)
  await expect(page.locator('.grid-projects article.card').first()).toBeVisible();

  await page.evaluate(() => window.scrollTo({ top: 300, behavior: 'instant' }));
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(300);

  // open してもスクロール位置は動かない。
  // **これは「変化しないこと」の検査**なので expect.poll で待ってはいけない: poll は最初の観測で
  // 300 を見た瞬間に成功してしまい、その後に起きるジャンプを見逃す (実測: この書き方だと
  // closeDrawer ガードを外す mutation が素通りした = vacuous)。スクロールが落ち着くまで待ってから
  // 1 度だけ確定値を読む (memory: absence assertion は settle 後に評価する)。
  await page.keyboard.press('Meta+k');
  await expect(page.locator('.cmdk-panel')).toBeVisible();
  await page.waitForTimeout(400);
  expect(await page.evaluate(() => window.scrollY), 'palette を開いた瞬間に先頭へ飛んではならない').toBe(300);

  // close しても戻らない (同じ理由で settle 後に 1 度だけ読む)
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  expect(await page.evaluate(() => window.scrollY), 'palette を閉じた瞬間に先頭へ飛んではならない').toBe(300);

  // drawer 経路の scroll 復元も不変 (#262/#297 の回帰防止を壊していないこと)
  await page.evaluate(() => document.getElementById('menuBtn').click());
  await page.waitForTimeout(400);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  expect(await page.evaluate(() => window.scrollY), 'drawer 経路の scroll 復元が壊れてはならない').toBe(300);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `scroll preservation test caused a fatal: ${fatal}`).toBeNull();
});
