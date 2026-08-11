const { test, expect } = require('@playwright/test');

// ===== 印刷 (@media print) の実効性 =====
// style.css には `@media print` があり、ナビ chrome を隠して本文を全幅化し、外部リンクの URL を
// 紙面へ併記する。**しかしこの契約を検証している層が一つも無かった**:
//   - screenshot は 1280x720 の screen media で撮る (print media には到達しない・かつ ADVISORY)
//   - behavior e2e は print を emulate していなかった
//   - consistency Check は CSS の存在を見ても *効果* は見ない
// つまり `@media print` ブロックを丸ごと消しても全ゲートが緑のまま通る (#133/#134/#135 と
// 同じ「silent-critical だが捕捉層ゼロ」の class)。
//
// このサイトは採用担当が Resume/About を紙に出す想定があるので、印刷が壊れることは
// 「機能性 (loads / displays / comprehensible)」の毀損に当たる。
const PRINT_ROUTES = ['#/resume', '#/about', '#/role-split'];

test('印刷時はナビ chrome が消え、本文が全幅で横あふれしない', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });

  for (const route of PRINT_ROUTES) {
    await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
    // NOTE: 不在検査の前に「在るはず」の要素で描画確定を待つ (goto 直後の評価は
    //   非同期描画とレースして『まだ無い』を『無い』と誤認する)。
    await expect(page.locator('#content h1, #content h2').first()).toBeVisible();

    await page.emulateMedia({ media: 'print' });
    // 変化 (screen → print) の反映を待つ。ここは settle 後に 1 度読む。
    await page.waitForTimeout(200);

    const s = await page.evaluate(() => {
      const disp = (id) => {
        const el = document.getElementById(id);
        return el ? getComputedStyle(el).display : 'absent';
      };
      const mc = document.getElementById('main-content');
      const de = document.documentElement;
      return {
        sidebar: disp('sidebar'),
        topbar: disp('topbar'),
        drawer: disp('drawer'),
        mainWidth: mc ? Math.round(mc.getBoundingClientRect().width) : null,
        overflow: de.scrollWidth - de.clientWidth,
        bodyBg: getComputedStyle(document.body).backgroundColor,
      };
    });

    expect(s.sidebar, `${route}: 印刷でサイドバーが残っている（紙面の左に空白帯と重複ナビが出る）`).toBe('none');
    expect(s.topbar, `${route}: 印刷でトップバーが残っている`).toBe('none');
    expect(s.drawer, `${route}: 印刷でドロワーが残っている`).toBe('none');
    // sidebar が消えた分、本文が全幅化していること（1200px の画面幅制限が外れる）
    expect(s.mainWidth, `${route}: 本文が全幅化していない（sidebar 用の余白が残っている）`).toBeGreaterThan(1200);
    // NOTE: `toBe(0)` にしてはいけない。印刷メディアではスクロールバーの gutter が予約されない
    //   ため `scrollWidth - clientWidth` が **負** になる環境がある (CI の Linux で -15px、
    //   ローカル macOS では 0 だった)。検証したいのは「あふれていないこと」なので ≤ 0 で表す。
    expect(s.overflow, `${route}: 印刷で横に ${s.overflow}px あふれている`).toBeLessThanOrEqual(0);
    expect(s.bodyBg, `${route}: 背景が白でない（暗色テーマのままだとインクを大量に消費する）`).toBe('rgb(255, 255, 255)');

    await page.emulateMedia({ media: null });
  }
});

test('印刷時は外部リンクの URL が紙面に併記される', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/#/resume', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1, #content h2').first()).toBeVisible();

  const link = page.locator('#content a[href^="http"]').first();
  await expect(link).toBeVisible();
  const href = await link.getAttribute('href');

  await page.emulateMedia({ media: 'print' });
  await page.waitForTimeout(200);

  // 紙にはクリックできる要素が無いので、リンク先が本文に出ていないと参照できない。
  const after = await page.evaluate(() =>
    getComputedStyle(document.querySelector('#content a[href^="http"]'), '::after').content);
  expect(after, `印刷時に外部リンクの URL が併記されていない（紙面からリンク先を辿れない）: ${after}`)
    .toContain(href);
});
