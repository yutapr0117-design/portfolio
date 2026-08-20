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


// ===== 通知が topbar のボタンを覆わない (操作不能にしない) =====
// 通知コンテナは `position: fixed; top: 1.5rem; right: 1.5rem` で右上に出る。モバイルでは
// **そこに topbar のボタンがある**ため、実測 (2026-08-20) では通知表示中に
// `document.elementFromPoint` がテーマ / BGM ボタンの中心で `.alert` を返し、**操作不能**だった。
// 通知は 3 秒 × 連続操作で継続しうるので、その間これらの導線が死ぬ。
//
// 判定は「その座標で実際に何が取れるか」で行う。可視・サイズだけでは覆いを検出できない。
test('Toasts never cover the topbar controls on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  // reducedMotion: View Transition の overlay が出ている間は `elementFromPoint` が
  //   ページ要素ではなく root を返す (実測: control が「通知が無いのに操作できない」と誤判定した)。
  //   遷移を切って hit-test を安定させる。落とし穴表の VT artifact と同じ class。
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#task-input')).toBeVisible();

  const hitTest = () => page.evaluate(() => {
    const out = {};
    for (const id of ['menuBtn', 'themeBtnTop', 'bgm-btn-top']) {
      const el = document.getElementById(id);
      if (!el || !el.getClientRects().length) { out[id] = 'hidden'; continue; }
      const b = el.getBoundingClientRect();
      const hit = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2);
      out[id] = (el === hit || el.contains(hit)) ? 'ok' : 'covered';
    }
    out.toasts = document.querySelectorAll('#toast-container .alert').length;
    return out;
  });

  // control: 通知が無い状態では当然すべて操作できる
  const before = await hitTest();
  expect(before.toasts, 'control: 通知が最初から出ている').toBe(0);
  expect(before.menuBtn, 'control: 通知が無くても topbar が操作できない').toBe('ok');

  await page.locator('#task-input').fill('topbar 被り確認');
  await page.locator('#task-input').press('Enter');
  await expect.poll(async () => (await hitTest()).toasts, { timeout: 5000 }).toBeGreaterThan(0);

  const during = await hitTest();
  expect(during.menuBtn, '通知がメニューボタンを覆っている').toBe('ok');
  expect(during.themeBtnTop, '通知がテーマ切替ボタンを覆っている').toBe('ok');
  expect(during['bgm-btn-top'], '通知が BGM ボタンを覆っている').toBe('ok');
});


// ===== 固定オーバーレイが操作要素を覆っていない (全ルート・汎用ゲート) =====
// #1171 (通知が topbar のボタンを覆う) と同じ「固定要素が操作要素を覆う」class を、
// **既定状態の全ルート**で見る層。`position: fixed` は他にも `.overlay` / `.drawer` /
// `.cmdk-host` があり、将来どれかが既定で覆いを作っても個別 test では気付けない。
//
// **このゲートの射程を正直に書いておく**: #1171 自体は捕捉できない —— あの覆いは
// **通知が出ている間だけ**発生し、本ゲートは既定状態 (通知なし) を見るため。実際に #1171 の
// 修正を戻しても本テストは緑のままだった (実測)。あちらは上の専用テストが担当する。
// 本ゲートが守るのは「**何も操作していないのに押せない要素がある**」状態で、
// `.overlay` を `display: block` にすると RED になることを実測済み。
//
// 判定は「その座標で実際に何が取れるか」。可視・サイズだけでは覆いを検出できない。
// reducedMotion: View Transition の overlay 表示中は `elementFromPoint` が root を返すため
//   (実測 2026-08-20)、遷移を切ってから測る。
test('No fixed overlay covers an interactive element on any route', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.emulateMedia({ reducedMotion: 'reduce' });

  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  const routes = await page.evaluate(() => Array.from(new Set(
    Array.from(document.querySelectorAll('a[href^="#/"]')).map((a) => a.getAttribute('href'))
  )));
  expect(routes.length, 'ナビからルートを導出できていない (control 失敗)').toBeGreaterThan(8);

  const offenders = [];
  for (const route of routes) {
    await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1, #content h2').first()).toBeVisible();
    const found = await page.evaluate(() => {
      const sel = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled])';
      const out = [];
      for (const el of document.querySelectorAll(sel)) {
        const b = el.getBoundingClientRect();
        if (b.width === 0 || b.height === 0) { continue; }
        const cx = b.left + b.width / 2;
        const cy = b.top + b.height / 2;
        // 画面外は別の問題 (このゲートは「覆い」だけを見る)
        if (cx < 0 || cy < 0 || cx > window.innerWidth || cy > window.innerHeight) { continue; }
        const hit = document.elementFromPoint(cx, cy);
        if (!hit || el === hit || el.contains(hit) || hit.contains(el)) { continue; }
        out.push(`${(el.getAttribute('aria-label') || el.textContent || el.id || el.tagName).trim().slice(0, 18)}`
          + ` <- ${(hit.id || hit.className || hit.tagName).toString().slice(0, 22)}`);
      }
      return out;
    });
    for (const f of found) { offenders.push(`${route}: ${f}`); }
  }

  expect(offenders,
    `固定要素が操作要素を覆っている (押せない):\n${offenders.slice(0, 8).join('\n')}`
  ).toEqual([]);
});
