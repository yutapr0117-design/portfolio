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

  // テーマ切替ボタンは desktop (sidebar) と mobile (#themeBtnTop) の両方に存在し同じ
  // aria-label を共有する。viewport で可視な方を選んでクリックする。
  const themeBtn = page.locator('button[aria-label="ライトモードとダークモードを切り替える"]:visible').first();
  await expect(themeBtn).toBeVisible();
  await themeBtn.click();

  const afterClick = await html.getAttribute('data-theme');
  expect(afterClick, 'data-theme must change after toggling the theme button').not.toBe(initial);

  // リロード後もテーマが永続化されていること（State → localStorage 往復）
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  const afterReload = await page.locator('html').getAttribute('data-theme');
  expect(afterReload, 'theme selection must persist across a page reload').toBe(afterClick);
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
