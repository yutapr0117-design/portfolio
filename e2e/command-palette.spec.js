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
