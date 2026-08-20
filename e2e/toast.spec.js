const { test, expect } = require('@playwright/test');

// 通知 (Toast) の振る舞いを扱う spec。apps-task.spec.js が Check 365 の 1,000 行上限に達したため、
// 「通知」というテーマの塊をここへ切り出した (圧縮で誤魔化さず、いま触っている塊を切り出す規律)。

// ===== 通知が積み上がって画面外へ出ない (WCAG 2.4.3 / UX) =====
// 通知コンテナは `position: fixed` で上端に固定される。同時表示数に上限が無いと連続操作で
// 積み上がり、**新しいものから順に画面外へ出て到達不能**になる —— fixed なので
// **スクロールして追うこともできない**。実測 (2026-08-20): 12 件を素早く出すと
// コンテナが bottom=904 まで伸び、viewport 720 (desktop) / 844 (mobile) を超えていた。
// 画面外に出た通知の閉じるボタンは tab 順に残るため、キーボード利用者は見えない位置へ focus が飛ぶ。
//
// 新しい通知ほど重要なので、超えたぶんは **古い方から**取り除く。読み上げは
// #action-announcement が別途担うので、この間引きで SR の情報は失われない。
test('Toasts do not stack past the viewport during rapid actions', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#task-input')).toBeVisible();

  // 連続操作を再現する。press() を並べると再描画を挟むので、同期で dispatch する
  // (落とし穴表の「連打を press() の連続で表現するな」と同じ理由)。
  await page.evaluate(() => {
    const el = document.getElementById('task-input');
    for (let i = 0; i < 12; i++) {
      el.value = 'burst-toast-' + i;
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
    }
  });

  const state = () => page.evaluate(() => {
    const c = document.getElementById('toast-container');
    const box = c.getBoundingClientRect();
    return {
      count: c.querySelectorAll('.alert').length,
      bottom: Math.round(box.bottom),
      viewport: window.innerHeight,
      // NOTE: 件数は **DOM から数える**。localStorage は debounce 保存なので、この時点では
      //   まだ null / 古い値のことがある (実際に踏んだ)。
      tasks: document.querySelectorAll('#content [data-testid], #content .card, #content li').length
        && Array.from(document.querySelectorAll('#content *'))
          .filter((el) => el.children.length === 0 && /burst-toast-/.test(el.textContent || '')).length,
    };
  });

  await expect.poll(async () => (await state()).count, { timeout: 5000 }).toBeGreaterThan(0);
  const s = await state();

  // control: 操作そのものは全件通っている (通知を間引くだけで機能は落とさない)
  expect(s.tasks, 'control: 連続追加が反映されていない').toBeGreaterThanOrEqual(12);

  expect(s.bottom, `通知が画面外へはみ出している (bottom=${s.bottom} > viewport=${s.viewport})`)
    .toBeLessThanOrEqual(s.viewport);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `toast burst caused a fatal: ${fatal}`).toBeNull();
});
