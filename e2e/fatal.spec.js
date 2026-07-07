const { test, expect } = require('@playwright/test');


// ===== ErrorBoundary: FatalPage 描画 + 復旧フロー (resilience) =====
// window.__fatalError が立つと _renderCore は FatalPage を描画する (ErrorBoundary)。以前は
// home(#/) で fatal が起きると「ホームへ」(Router.navigate('')) が同一 hash ゆえ hashchange 不発火
// で再描画されず FatalPage から復旧できないバグがあった (window.render() を明示呼びして是正)。
// 既存 e2e は __fatalError===null (fatal が起きないこと) ばかり検証し、FatalPage 自体の描画 +
// 復旧フローは未カバーだった。本テストは fatal を注入して FatalPage が出る → ホームへ で復旧、を検証。
test('FatalPage renders on a fatal error and ホームへ recovers (home-route)', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  // 致命的エラーを注入して再描画 → FatalPage
  await page.evaluate(() => { window.__fatalError = new Error('E2E_FATAL_PROBE'); window.render(); });
  await expect(page.locator('#content h1', { hasText: '致命的エラー' })).toBeVisible();
  await expect(page.getByText('E2E_FATAL_PROBE').first()).toBeVisible();
  // 「ホームへ」で復旧 (home-route の同一 hash でも window.render() で再描画される)
  await page.getByRole('button', { name: 'ホームへ' }).click();
  await expect(page.locator('#content h1', { hasText: '致命的エラー' })).toHaveCount(0);
  const fatal = await page.evaluate(() => window.__fatalError);
  expect(fatal).toBeNull();
  await expect(page.locator('.hero-section')).toBeVisible();
});


test('FatalPage ホームへ recovers from a non-home route too', async ({ page }) => {
  await page.goto('/#/about', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.evaluate(() => { window.__fatalError = new Error('E2E_FATAL_ABOUT'); window.render(); });
  await expect(page.locator('#content h1', { hasText: '致命的エラー' })).toBeVisible();
  await page.getByRole('button', { name: 'ホームへ' }).click();
  await expect(page.locator('#content h1', { hasText: '致命的エラー' })).toHaveCount(0);
  await expect(page.locator('.hero-section')).toBeVisible();
});


// ===== 7.1: グローバル安全網は正常描画された FatalPage を覆わない (silent-failure 専用) =====
// fatal-overlay.js の最終安全網 (Shadow DOM) は 2 秒毎の setInterval で __fatalError をチェックする。
// __fatalError は FatalPage 描画後もセットされたまま (クリアは「ホームへ」のみ) ゆえ、有無だけで判定
// すると正常な in-app FatalPage を 2 秒後に覆い、その復旧ボタン (ホームへ/データ削除) を押せなくして
// 全リロードを強制してしまうバグがあった。安全網は「FatalPage を含む全防御層をすり抜けた silent
// failure」専用なので FatalPage マーカー (#fallback-details) が無いときだけ起動すべき。(A) FatalPage
// 描画後 2 秒超でも安全網が出ないこと、(B) FatalPage が出ない silent failure では安全網が出ること、を検証。
test('Global safety net does not cover a rendered FatalPage but still fires on silent failure', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();

  // (A) fatal 注入 → FatalPage 描画。安全網 interval(2s) を超えて待っても安全網は出ない。
  await page.evaluate(() => { window.__fatalError = new Error('E2E_SAFETYNET_PROBE'); window.render(); });
  await expect(page.locator('#fallback-details')).toBeVisible(); // FatalPage 描画確認
  await page.waitForTimeout(2500); // safety-net interval(2s) を超えて待つ
  expect(await page.evaluate(() => !!document.getElementById('portfolio-safety-net-host')),
    'safety net must NOT cover a working FatalPage').toBe(false);
  await expect(page.locator('#fallback-details')).toBeVisible(); // FatalPage は健在

  // (B) silent failure を模す: FatalPage マーカーを除去 (= in-app 復旧 UI が出なかった状態)。
  // __fatalError は依然セットゆえ、次の interval tick で安全網が起動するはず (intent 保持を実証)。
  await page.evaluate(() => document.getElementById('fallback-details')?.remove());
  await expect(page.locator('#portfolio-safety-net-host')).toBeAttached({ timeout: 3000 });
});
