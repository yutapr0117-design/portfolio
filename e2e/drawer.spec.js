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

// ===== 7.3: レスポンシブ切替の behavioral 検証 — 全幅で sidebar XOR topbar menuBtn (broken band なし) =====
// MOBILE_BREAKPOINT(=920) 前後で、desktop sidebar と mobile topbar の menuBtn は排他表示される
// (@media max-width:920 で .sidebar{display:none}、JS は matchMedia で topbar を出す)。Check 378 は
// JS 定数 ↔ CSS @media の**値の一致**を強制するが、CSS の display:none ルール自体の除去や menuBtn の
// 誤非表示など「値は一致するが実 display 挙動が壊れる」回帰 (= sidebar+topbar 両表示 or 両非表示の
// broken band・#262/#297 class) は捕捉しない。本テストは境界 (919/920/921) と代表幅で **ちょうど
// 一方のみ可視** を実測し、実 display 挙動を behavioral に guard する。
test('responsive: exactly one of {desktop sidebar, mobile menuBtn} is visible at every width (no broken band)', async ({ page }) => {
  // [FIX] 「viewport を変えてから goto」→ 固定 150ms 待ち、をやめる。
  //   実測 (#1018) で判ったこと: この順序だと **init 時点の viewport がまだ前の幅**で、
  //   `syncMobileDrawer()` が mobile 判定のまま `topbar.style.display='flex'` を書く。
  //   正しい値は **その後に届く resize イベント**で入るため、150ms はその到着に賭けていた
  //   (CI で w=921 が sidebar と menuBtn の同時可視として間欠 RED になった)。
  //   代わりに **一度 goto してから viewport を変え**、JS 側の反映が済むまで状態で待つ。
  //   resize は `debounce(syncMobileDrawer, DEBOUNCE_DELAY)` 経由なので、150ms はその
  //   debounce 値に賭けていたことになる。
  //   NOTE: 途中で `#content h1` の visible を待つ案も試したが、index.html には AI クローラ向けの
  //   **静的 h1 が既にある**ため JS init 前に満たされ、150ms より弱い待ちになって即 RED になった。
  const probe = async (w) => {
    await page.setViewportSize({ width: w, height: 800 });
    // resize → `debounce(syncMobileDrawer, DEBOUNCE_DELAY)` なので、幅を変えても JS 側の
    // 反映は **遅れて**来る。旧実装の固定 150ms 待ちはこの debounce 値に賭けており、
    // CI 負荷で追い越されて間欠 RED になっていた。ここは「変化」を待つので poll が正しい。
    await expect.poll(
      () => page.evaluate(() => {
        const t = document.getElementById('topbar');
        if (!t) { return false; }
        const isMobile = window.matchMedia('(max-width: 920px)').matches;
        return t.style.display === (isMobile ? 'flex' : 'none');
      }),
      { message: 'debounce された syncMobileDrawer が topbar の表示を更新しない' }
    ).toBe(true);
    return page.evaluate(() => {
      const vis = (el) => !!el && getComputedStyle(el).display !== 'none' && el.getBoundingClientRect().width > 0;
      return { sidebar: vis(document.querySelector('.sidebar')), menuBtn: vis(document.getElementById('menuBtn')) };
    });
  };
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#sidenav-home')).toHaveCount(1);   // JS init 完了 (静的 HTML には無い要素)
  // 920 は @media max-width:920 (inclusive) ゆえ mobile 側、921 から desktop 側
  for (const [w, mode] of [[390, 'mobile'], [919, 'mobile'], [920, 'mobile'], [921, 'desktop'], [1280, 'desktop']]) {
    const s = await probe(w);
    // 排他: ちょうど一方のみ (両表示=broken layout / 両非表示=ナビ喪失 を捕捉)
    expect(s.sidebar !== s.menuBtn, `w=${w}: sidebar(${s.sidebar}) と menuBtn(${s.menuBtn}) は排他であるべき`).toBe(true);
    if (mode === 'mobile') {
      expect(s.menuBtn, `w=${w} は mobile ゆえ topbar menuBtn が可視`).toBe(true);
    } else {
      expect(s.sidebar, `w=${w} は desktop ゆえ sidebar が可視`).toBe(true);
    }
  }
});


// ===== 7.2: BGM トグルの a11y 状態同期 (aria-pressed / aria-label) =====
// topbar の BGM ボタン (#bgm-btn-top・data-action='bgm:toggle') は ui-components.js の BGM.toggle →
// _syncAll() で aria-pressed と aria-label ('BGMを再生する'/'BGMを停止する') とアイコン (volume2/volumeX)
// を状態同期する。これまで BGM は behavior e2e 完全未カバーで、_syncAll が呼ばれなくなっても
// (a) SR には常に「押されていない」と報告され (b) ラベルとアイコンが実状態と食い違う、という退行が
// どの gate も通り抜けた (Check 376 は action が handler に解決することしか見ない)。
// 注: BGM ボタンは topbar = mobile 専用ゆえ mobile viewport で検証する (desktop では sidebar 表示)。
test('BGM toggle syncs aria-pressed and aria-label with playback state (a11y)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/');
  await page.waitForLoadState('domcontentloaded');

  const btn = page.locator('#bgm-btn-top');
  await expect(btn).toBeVisible();
  await expect(btn).toHaveAttribute('aria-pressed', 'false');

  // 再生 → pressed=true + 「停止する」ラベルへ同期
  await btn.click();
  await expect(btn).toHaveAttribute('aria-pressed', 'true');
  await expect(btn).toHaveAttribute('aria-label', 'BGMを停止する');

  // 停止 → pressed=false + 「再生する」ラベルへ戻る
  await btn.click();
  await expect(btn).toHaveAttribute('aria-pressed', 'false');
  await expect(btn).toHaveAttribute('aria-label', 'BGMを再生する');

  // [FIX] **名前の出どころは aria-label だけ**であること。
  //   index.html は長らく `<span class="sr-only">BGMを再生する</span>` を内包していたが、
  //   `aria-label` が要素内容を上書きするので **一度も読み上げられず**、しかも
  //   `_syncAll()` の更新対象外なので **再生中も「再生する」のまま**だった (実測 2026-08-21)。
  //   同じ topbar の menuBtn / themeBtnTop は aria-label 単独で、これだけが outlier。
  //   実害は「誰かが aria-label を消すと名前が永久に古い文言で固定される」latent trap で、
  //   除去した。再混入すると accessible name の出どころが 2 つになるのでここで捕捉する。
  expect((await btn.textContent()).trim(),
    'BGM ボタンに aria-label と競合するテキストが入っている (名前の出どころは 1 つに保て)').toBe('');
  expect(await btn.evaluate((el) => {
    const s = el.querySelector('.sr-only');
    return s ? s.textContent.trim() : null;
  }), '除去した sr-only ラベルが再混入している').toBeNull();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `BGM toggle caused a fatal: ${fatal}`).toBeNull();
});

// ===== BGM の再生失敗を利用者に伝える =====
// `audio.play()` は拒否されうる (デコード失敗・資産の取得失敗・端末側の制約)。従来は
// console.warn だけで、実測 (2026-08-18) では **toast も announcement も状態変化も一切出ず**、
// 利用者から見ると「ボタンを押したのに何も起きない」だった。console は開発者向けの信号で
// 利用者には見えない —— 同じ非対称をストレージ上限の警告でも踏んでいる (そちらは Toast があり
// こちらだけ欠けていた)。BGM は topbar = mobile 専用の導線で、通信が不安定な環境ほど audio の
// 読み込みに失敗しやすく、まさにその場面で無言になる。
//
// 検査先に #action-announcement を選ぶ理由: Toast は duration で自動消滅するため、そちらを
// 待つ形は「実装内部の定数への賭け」になる (落とし穴表に記録済)。
test('BGM reports a failed playback attempt instead of doing nothing visible', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  // play() だけを拒否させる (要素の読み込みや他の再生経路は壊さない)
  await page.addInitScript(() => {
    HTMLMediaElement.prototype.play = function () { return Promise.reject(new Error('NotSupportedError')); };
  });
  await page.goto('/#/');
  await page.waitForLoadState('domcontentloaded');

  const btn = page.locator('#bgm-btn-top');
  await expect(btn).toBeVisible();
  await expect(btn).toHaveAttribute('aria-pressed', 'false');

  await btn.click();

  // 失敗が利用者に届く
  await expect.poll(
    () => page.evaluate(() => (document.getElementById('action-announcement') || {}).textContent || ''),
    { timeout: 5000 }
  ).toContain('BGM を再生できませんでした');

  // 「再生中」と嘘をつかない (状態は false のまま)
  await expect(btn).toHaveAttribute('aria-pressed', 'false');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `BGM play failure caused a fatal: ${fatal}`).toBeNull();
});

// ===== 履歴移動で drawer が開いたまま残らない =====
// drawer 内の nav リンクは自分で closeDrawer() を呼ぶが、**それ以外の経路でルートが変わると
// drawer は開いたまま残っていた** (実測 #998)。mobile で drawer を開いてブラウザの「戻る」を
// 押すと、背後のページだけが切り替わり drawer は開いたまま・#app は inert・body は scroll lock
// のままになる。Android の戻るボタンは「開いているモーダルを閉じる」操作として使われるのに、
// 実際には**見えない場所でページが遷移していた**。
//
// この経路は #997 で全ルートの重複 id を掃く test を書こうとして見つかった —— ルートを goto で
// 渡り歩くと 2 つ目以降で #menuBtn のクリックが overlay に阻まれて timeout し、
// 「前のルートで開けた drawer が残っている」ことが判った。
test('drawer 開放中にブラウザの戻るでルートが変わったら drawer が閉じる', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();

  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  await page.goBack();
  await expect(page.locator('#content h1', { hasText: 'AI を自走させ' })).toBeVisible();

  // NOTE: 「閉じたこと」は変化なので expect の auto-wait でよいが、isolation の解除は
  //   settle 後に 1 度だけ読む (不変性の検査に poll を使わない)。
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'true');
  const state = await page.evaluate(() => ({
    overlay: getComputedStyle(document.getElementById('overlay')).display,
    inert: document.getElementById('app').hasAttribute('inert'),
    bodyPosition: document.body.style.position
  }));
  expect(state.overlay, 'overlay が残り操作を阻む').toBe('none');
  expect(state.inert, '背後のページが inert のままで操作できない').toBe(false);
  expect(state.bodyPosition, 'body の scroll lock が解除されていない').toBe('');
});

// 逆方向の非破壊確認: drawer 内の nav リンク経由は従来どおり閉じる (hashchange の
// リスナーを足したことで二重に closeDrawer が走るが、#948 の再入ガードで無害であること)。
test('drawer 内の nav リンクからの遷移も従来どおり閉じる', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  await page.locator('#drawernav-projects').click();
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'true');
  const inert = await page.evaluate(() => document.getElementById('app').hasAttribute('inert'));
  expect(inert).toBe(false);
});


// ===== モバイルの drawer でも現在地 (aria-current) が示される =====
// 既存の aria-current テストは **desktop viewport (sidebar 表示)** を見ている。だが
// mobile では sidebar は `display:none` で、**drawer が唯一のナビゲーション**になる。
// sidebar と drawer は同じ navLink 実装を共有するが、共有していることは
// 「現在ルートの判定が drawer 側にも届いている」ことの保証にはならない (drawer は開くたびに
// 組み直されるので、組み立て時の状態を読み損ねれば現在地が付かない)。
// 現在地が分からないと SR 利用者は「今どこにいるか」をナビから得られなくなる (WCAG 2.4.8)。
test('モバイルの drawer が現在ルートに aria-current を付け、遷移に追従する', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 780 });
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();

  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  const drawerCurrent = () => page.evaluate(() => Array.from(
    document.querySelectorAll('#drawer [aria-current="page"]')
  ).map((e) => e.id));

  // control: drawer に nav リンクが実際に描かれている
  expect(await page.locator('#drawer a[id^="drawernav-"]').count(),
    'control: drawer に nav リンクが無い').toBeGreaterThan(3);

  expect(await drawerCurrent(),
    'drawer が現在ルートを示していない (mobile では drawer が唯一のナビ)').toEqual(['drawernav-projects']);

  // 別ルートへ遷移して開き直すと追従する
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'About' })).toBeVisible();
  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  expect(await drawerCurrent(),
    'ルート遷移後も drawer の現在地が古いまま').toEqual(['drawernav-about']);
});
