const { test, expect } = require('@playwright/test');


// ===== 7.1: モバイルビューポートでのCLS検証 =====
test('No layout shift on mobile viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

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
  await page.waitForLoadState('domcontentloaded');

  const html = page.locator('html');
  const initial = await html.getAttribute('data-theme');

  // テーマ切替ボタンは desktop (#themeBtnSidebar) と mobile (#themeBtnTop) の両方に存在する。
  // viewport で可視な方を選んでクリックする (id で locate。aria-label は現在テーマで動的に変わる
  // ため locator に使わない)。
  const themeBtn = page.locator('#themeBtnSidebar:visible, #themeBtnTop:visible').first();
  await expect(themeBtn).toBeVisible();
  await themeBtn.click();

  const afterClick = await html.getAttribute('data-theme');
  expect(afterClick, 'data-theme must change after toggling the theme button').not.toBe(initial);

  // [a11y WCAG 4.1.2] 可視なテーマボタンの aria-label が現在テーマ状態を露出すること。
  //   apply()/render 由来で「現在: <テーマ名>」に更新される (static 2 状態ラベルからの是正)。
  //   theme.js の themeToggleAriaLabel を戻すと現在状態が露出せず RED = 非 vacuity。
  const expectLabel = { system: 'システム設定', dark: 'ダーク', light: 'ライト' }[afterClick];
  await expect(page.locator('#themeBtnSidebar:visible, #themeBtnTop:visible').first())
    .toHaveAttribute('aria-label', `テーマを切り替える（現在: ${expectLabel}）`);

  // リロード後もテーマが永続化されていること（State → localStorage 往復）
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  const afterReload = await page.locator('html').getAttribute('data-theme');
  expect(afterReload, 'theme selection must persist across a page reload').toBe(afterClick);
});


// ===== theme cycle の完全な 3 状態遷移順 (system → dark → light → system) =====
// 既存の cycle テストは 1 クリックのみで「data-theme が変わる」ことしか見ておらず、cycle() の
// 遷移順 (theme.js: current==='system'?'dark':current==='dark'?'light':'system') が壊れても
// (例 system→light に変わる / 3 クリックで元に戻らない) 素通りする。default theme='system'
// (store.js) から 3 クリックして dark→light→system と一周し初期状態へ戻ることを検証する。
// cycle() の三項順を崩すと中間状態のアサーションが RED になる (非 vacuous)。
test('Theme toggle follows the full 3-state cycle order (system → dark → light → system)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const html = page.locator('html');
  // 既定は 'system' (store.js 既定 theme)。前テストと独立の fresh context で確認する。
  await expect(html).toHaveAttribute('data-theme', 'system');

  const themeBtn = page.locator('#themeBtnSidebar:visible, #themeBtnTop:visible').first();
  await expect(themeBtn).toBeVisible();

  await themeBtn.click();
  await expect(html).toHaveAttribute('data-theme', 'dark');    // system → dark
  await themeBtn.click();
  await expect(html).toHaveAttribute('data-theme', 'light');   // dark → light
  await themeBtn.click();
  await expect(html).toHaveAttribute('data-theme', 'system');  // light → system (一周)
});


// ===== theme='system' の runtime OS-color-scheme 追従 (system-follow regression) =====
// theme.js init は matchMedia('(prefers-color-scheme: dark)') の 'change' を購読し、選択が
// 'system' のとき OS テーマ変化に追従して apply('system') を再実行する (data-theme='system' の
// まま .dark クラスだけを OS に合わせ toggle)。theme-cycle / FOUC テストは「クリック切替」と
// 「保存済み初期適用」を見るが、この "起動後に OS テーマが変わったら追従する" runtime listener
// (js/theme.js の matchMedia change ハンドラ) は未カバーだった。default theme は 'system' ゆえ
// seed 不要。emulateMedia で OS テーマを切替え、.dark が追従することを検証する。listener を除去
// すると .dark が更新されず RED になる non-vacuous ガード。
test('Theme "system" follows runtime OS color-scheme changes', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'light' });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  const html = page.locator('html');
  // default = 'system'。light OS ではダークではない
  await expect(html).toHaveAttribute('data-theme', 'system');
  await expect(html).not.toHaveClass(/\bdark\b/);
  // OS→dark: system-follow listener が .dark を付与 (選択は 'system' のまま)
  await page.emulateMedia({ colorScheme: 'dark' });
  await expect(html).toHaveClass(/\bdark\b/);
  await expect(html).toHaveAttribute('data-theme', 'system');
  // OS→light: .dark が外れる
  await page.emulateMedia({ colorScheme: 'light' });
  await expect(html).not.toHaveClass(/\bdark\b/);
});


// ===== 7.1: theme-init.js の FOUC pre-paint (保存 dark テーマの初期適用) =====
// theme-init.js は main.js (ESM) ロード前に localStorage の theme を読み data-theme / .dark を
// pre-paint 適用し FOUC (light→dark のちらつき) を防ぐ。theme-cycle テストは「クリックで切替→永続」
// を見るが、「保存済み dark を初期ロードで復元する」FOUC 防止経路は未カバーだった。dark を seed して
// 読み込み、html[data-theme=dark] + .dark が初期適用されることを検証する。
test('theme-init.js applies stored dark theme on initial load (FOUC prevention)', async ({ page }) => {
  // main.js ロード前に走る theme-init.js が読む localStorage キーへ dark を seed
  await page.addInitScript(() => {
    try {
      localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
        schemaVersion: 12, type: 'full-store', theme: 'dark'
      }));
    } catch (e) { /* noop */ }
  });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const html = page.locator('html');
  await expect(html).toHaveAttribute('data-theme', 'dark');
  await expect(html).toHaveClass(/\bdark\b/);
});


// ===== 7.1: Service Worker の登録・activate・page 制御 (SW ライフサイクル) =====
// sw.js は install(skipWaiting)→activate(古いキャッシュ削除 + clients.claim)→fetch(SWR) の
// ライフサイクルを持つ。フルオフライン navigation は提供しない設計 (SWR・app-shell precache なし)
// ため offline 配信はテスト対象外。ここでは genuine な「SW が登録され active になり page を制御する」
// ことを検証し、SW 登録/活性化の退行 (例: registration 失敗・activate 例外) を捕捉する。
test('Service worker registers, activates, and controls the page', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.evaluate(() => navigator.serviceWorker.ready);

  // active な registration が存在する
  const active = await page.evaluate(async () => {
    const reg = await navigator.serviceWorker.getRegistration();
    return !!(reg && reg.active);
  });
  expect(active, 'an active service worker registration must exist').toBe(true);

  // clients.claim() により page が SW 制御下に入る
  await expect.poll(() => page.evaluate(() => !!navigator.serviceWorker.controller)).toBe(true);
});


// ===== 7.1: theme-init.js の brand pre-paint (保存 brand の初期適用) =====
// theme-init.js は localStorage 'portfolio_brand_v45' を main.js ロード前に読み data-brand を
// pre-paint 適用する (brand 別パレットの FOUC 防止)。dark テーマ FOUC と同クラスだが brand 軸は
// 未カバーだった。非デフォルト brand 'classic' を seed して初期ロード → html[data-brand=classic] が
// 適用されることを検証する (DEFAULT='indigo' でなく保存値が復元されることを示す)。
test('theme-init.js applies stored brand on initial load (brand FOUC prevention)', async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.setItem('portfolio_brand_v45', 'classic'); } catch (e) { /* noop */ }
  });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  await expect(page.locator('html')).toHaveAttribute('data-brand', 'classic');
});


// ===== 7.2: system テーマが OS の prefers-color-scheme に追従する =====
// Theme.apply は theme='system' のとき isDark = matchMedia('(prefers-color-scheme: dark)') で
// 解決し documentElement に 'dark' class を toggle する。さらに init で matchMedia の change を
// 購読し、system 選択時のみ OS テーマ変更へライブ追従する (theme.js §init 不変条件)。cycle
// テスト (data-theme 属性遷移) とは別に、この OS 解決 + ライブ追従経路を検証する。fresh context は
// 既定 theme='system' なので、emulateMedia で OS を dark/light に切替え 'dark' class の付与/解除を
// 実検証する。動きの保証 = OS をダークにしている利用者に常にダーク表示。
test('System theme follows the OS prefers-color-scheme (live)', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const html = page.locator('html');
  // fresh context は既定で system
  await expect(html).toHaveAttribute('data-theme', 'system');
  await expect(html).toHaveClass(/\bdark\b/);

  // OS を light へ → change リスナーが apply('system') 再実行 → dark class 解除
  await page.emulateMedia({ colorScheme: 'light' });
  await expect(html).not.toHaveClass(/\bdark\b/);
  await expect(html).toHaveAttribute('data-theme', 'system');

  // OS を再び dark へ → dark class 復帰
  await page.emulateMedia({ colorScheme: 'dark' });
  await expect(html).toHaveClass(/\bdark\b/);
});
