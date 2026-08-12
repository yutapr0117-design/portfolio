const { test, expect } = require('@playwright/test');


// ===== Live-input focus retention 回帰防止 =====
// oninput→State.update→notify→render() は #content を clear して全再描画するため、focused input が
// 毎キーストロークで破棄され focus を失う。quiz 検索 / Markdown notes はこのバグで「1 文字目で focus が
// 外れ以降の文字が落ちる」状態だった。State.updateSilently + sub-DOM 手動更新で是正済。本テストは
// per-keystroke の type() で「全文字が着弾し focus が保持される」ことを検証する (fill() は値直接設定
// ゆえ focus-loss を検出できない — それが本バグが素通りした理由)。
test('Quiz search input retains focus and filters live while typing (focus-loss regression)', async ({ page }) => {
  await page.goto('/#/quiz?type=aws', { waitUntil: 'domcontentloaded' });
  const input = page.locator('input[aria-label="問題検索"]');
  await expect(input.first()).toBeVisible();
  await input.first().click();
  await page.keyboard.type('ecs', { delay: 40 });
  // 全文字が着弾 (再描画で input が破棄されると 1 文字目しか残らない)
  await expect(input.first()).toHaveValue('ecs');
  // focus が input に残っている
  const activeLabel = await page.evaluate(() => document.activeElement && document.activeElement.getAttribute('aria-label'));
  expect(activeLabel).toBe('問題検索');
  // 検索クエリ消去でリストが復活する (手動 renderList が機能している)
  await input.first().fill('');
  await page.keyboard.type(' ', { delay: 10 });
  await input.first().fill('');
});


// [FIX] focus だけを見ていると **この test は #994 の focus 復元機構に守られてしまい**、
//   `updateSilently` → `State.update` へ戻す mutation を素通しする (週次 probe が SURVIVED として
//   検出・#1024)。復元機構は「消えた後に戻す」ので、focus は結果的に維持されるからである。
//   `updateSilently` が固有に保証しているのは **そもそも再描画しない** こと。
//   よって **textarea の DOM ノードが 1 文字ごとに作り直されていないこと** を直接見る
//   (再描画は #content を clear して作り直すので、同一ノードなら再描画は起きていない)。
test('Notes textarea retains focus while typing (focus-loss regression)', async ({ page }) => {
  await page.goto('/#/apps/notes', { waitUntil: 'domcontentloaded' });
  const ta = page.locator('#notes-input');
  await expect(ta.first()).toBeVisible();

  // 入力前のノードに印を付ける。再描画で作り直されると印は失われる。
  await page.evaluate(() => { document.getElementById('notes-input').dataset.probeMark = 'kept'; });

  await ta.first().click();
  await page.keyboard.press('End');
  await page.keyboard.type('ZZZ', { delay: 40 });

  const s = await page.evaluate(() => {
    const t = document.getElementById('notes-input');
    return {
      activeId: document.activeElement && document.activeElement.id,
      sameNode: t.dataset.probeMark === 'kept',
    };
  });
  expect(s.activeId).toBe('notes-input');
  expect(s.sameNode, '1 文字ごとに textarea が作り直されている (oninput が全再描画を起こしている) — '
    + 'focus は #994 の復元機構が戻すので focus だけでは検出できない').toBe(true);
  await expect(ta.first()).toHaveValue(/ZZZ$/);
});


// ===== Topbar data-action button double-fire 回帰防止 =====
// topbar の menuBtn/themeBtnTop/bgm-btn-top は data-action を持ち ActionDelegator が処理する。
// 以前は main.js init が同じボタンに直接 click リスナーも付けており、1 クリックで各ハンドラが
// 二重発火していた (theme が 1 クリックで 2 段送り＝1 つ飛ばし / drawer 二重 open で
// __lockBodyScroll が scrollY=0 を読み閉じると先頭ジャンプ / BGM 二重 toggle)。直接リスナーを
// 撤去し ActionDelegator に一本化。本テストは theme が 1 クリックで「ちょうど 1 段」進むことで
// 単発発火を検証する (二重発火だと system→dark→light で 'light' に飛ぶ)。topbar は mobile 表示。
test('Topbar theme button advances exactly one step per click (double-fire regression)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 700 });
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  const btn = page.locator('#themeBtnTop');
  await expect(btn).toBeVisible();
  const before = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
  expect(before).toBe('system');
  await btn.click();
  const after = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
  expect(after).toBe('dark');
});
