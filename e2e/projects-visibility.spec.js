const { test, expect } = require('@playwright/test');

// ===== プロジェクトの「非表示」(curation) の契約 =====
//
// 元は e2e/apps-settings.spec.js にあったが、同 file が 968 行となり Check 365 の
// BLOCKING (1,000 行) まで残り 32 行になったため、**当たる前に**このテーマの塊を
// 切り出した (CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。
//
// なぜ「非表示」が独立したテーマか:
//   既定プロジェクトは**削除できない**ため、非表示が**唯一の非公開手段**である (#886)。
//   つまりこれは単なる表示設定ではなく **公開/非公開の意思**そのもの。しかも読み手は
//   ProjectsPage だけでなく home の注目枠 / 詳細の推薦 / Cmd+K / カテゴリ選択肢と
//   **5 面**あり、1 面でも漏れると「隠したのに出ている」になる (#886 で実際に漏れた)。
//   read 面の mesh をまとめて 1 file で守る。



// ===== 7.2: プロジェクト非表示/表示トグル (公開一覧の curation) =====
// settings の toggleHiddenProject は projectPrefs.hiddenIds に id を出し入れし、ProjectsPage は
// hiddenIds を filter して公開一覧から除外する (components.js)。これは公開ページの見せ方を制御する
// curation 機能だが従来未カバーだった。カスタムプロジェクトを追加→「非表示」で /#/projects から
// 消える→「表示」で復帰、を実検証する。hiddenIds の State 往復とフィルタ適用の保証。
test('Hiding a project removes it from the public Projects list, unhide restores it', async ({ page }) => {
  // カスタムプロジェクトを追加 (一意名)
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const name = 'HIDE-TOGGLE-PROJ-3050';
  await page.getByPlaceholder('プロジェクト名').fill(name);
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();

  // 公開一覧に出る
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();

  // settings の該当行で「非表示」
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const row = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name });
  await row.getByRole('button', { name: '非表示' }).click();
  // 行に hidden バッジ + 「表示」ボタンへ切替わる
  await expect(row.getByRole('button', { name: '表示' })).toBeVisible();

  // 公開一覧から消える
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  // [FIX] 不在アサーションは「まだ描画されていない」を「無い」と誤認して vacuous に PASS しうる
  //   (toHaveCount(0) は初回 poll で成立すると再検査されない)。先に「必ず在るはず」の要素を待って
  //   描画を確定させてから不在を検査する (#825/#830 class・Check 402 が構造強制)。
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
  await expect(page.getByText(name)).toHaveCount(0);

  // 再表示 → 公開一覧へ復帰
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const row2 = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name });
  await row2.getByRole('button', { name: '表示' }).click();
  await expect(row2.getByRole('button', { name: '非表示' })).toBeVisible();

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();
});


// ===== 非表示は「全 listing 面」に効き、解除で「全 listing 面」に戻る =====
// #886 では、非表示 (projectPrefs.hiddenIds) を読んでいたのが **ProjectsPage と
// SettingsPage だけ**で、**home の注目枠 / 詳細ページの推薦 / Cmd+K 候補 / カテゴリ選択肢**は
// 素の state.projects から描いていた。既定プロジェクトは削除できず「非表示」が唯一の
// 非公開手段なので、隠したはずのものがトップに出続けるのは **公開/非公開の意思**の喪失。
//
// 既存テストは **公開一覧 1 面**の往復しか見ていない。home と Cmd+K は実装だけあって
// **どの e2e も見ていなかった**ので、ここで両方向 (隠す / 戻す) × 2 面を固定する。
// 片方向だけ直す退行 (隠せるが戻らない / 隠れないが戻る) は利用者から見ると
// 「設定が効いたり効かなかったりする」形で出る。
test('非表示は home と Cmd+K にも効き、解除で両方に戻る', async ({ page }) => {
  const NAME = 'タスク管理アプリ';

  // NOTE: **そのページ固有の見出し**で待つ。`#content h1` の汎用待ちは hash 遷移では
  //   **前ページ (settings) の DOM で満たされ**、settings の行に含まれる同じ名前を読んで
  //   しまう (実測でこの罠に落ちた・落とし穴表の既存行)。
  const onHome = async () => {
    await page.goto('/#/');
    await expect(page.locator('#content h1', { hasText: 'AI を自走させ' })).toBeVisible();
    return (await page.locator('#content').innerText()).includes(NAME);
  };
  const inPalette = async () => {
    await page.goto('/#/projects');
    await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
    await page.keyboard.press('Control+k');
    await expect(page.locator('#command-palette-host')).toHaveAttribute('aria-hidden', 'false');
    await page.keyboard.type('タスク管理');
    // 候補の再描画を待ってから読む
    await expect.poll(() => page.evaluate(() =>
      (document.querySelector('#cmdk-listbox') || { textContent: '' }).textContent.length)).toBeGreaterThan(0);
    const hit = await page.evaluate(() =>
      (document.querySelector('#cmdk-listbox') || { textContent: '' }).textContent.includes('タスク管理アプリ'));
    await page.keyboard.press('Escape');
    return hit;
  };
  const toggleHidden = async () => {
    await page.goto('/#/settings');
    await expect(page.locator('#main-content h1').first()).toBeVisible();
    await page.locator('#settings-toggle-hidden-p01').click();
  };

  // control: 最初は両面に出ている (出ていなければ以降は何も検査しない)
  expect(await onHome(), 'control: 非表示前から home に出ていない').toBe(true);
  expect(await inPalette(), 'control: 非表示前から Cmd+K に出ていない').toBe(true);

  await toggleHidden();
  expect(await onHome(), '非表示にしたのに home の注目枠に出続けている (#886)').toBe(false);
  expect(await inPalette(), '非表示にしたのに Cmd+K 候補に出続けている (#886)').toBe(false);

  await toggleHidden();
  expect(await onHome(), '表示に戻したのに home へ復帰しない (片方向だけの修正)').toBe(true);
  expect(await inPalette(), '表示に戻したのに Cmd+K へ復帰しない (片方向だけの修正)').toBe(true);
});


// ===== 非表示の listing mesh 残り 2 面 (詳細の推薦 / カテゴリ選択肢) =====
// #886 で塞いだ 4 面のうち、公開一覧・home・Cmd+K は被覆済み。残る
// **詳細ページの推薦**と**カテゴリ選択肢**は実装だけあって e2e が無かった。
//
// カテゴリ面は「そのカテゴリの project を全部隠す」まで変化しないので、既定で
// 3 件しかない Security を 3 件とも隠して選択肢が消えることを見る。**1 件だけ隠して
// 「変わらない」ことを確認しても何も検査していない**（他の 2 件が残るので当然変わらない）。
test('非表示は詳細の推薦とカテゴリ選択肢にも効く', async ({ page }) => {
  const SEC = ['p13', 'p14', 'p15'];

  const recoHasTaskManager = async () => {
    await page.goto('/#/projects/todo-list');
    await expect(page.locator('#content h1', { hasText: 'TODOリスト' })).toBeVisible();
    return (await page.locator('#content').innerText()).includes('タスク管理アプリ');
  };
  const categories = async () => {
    await page.goto('/#/projects');
    await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
    return page.evaluate(() =>
      Array.from(document.querySelectorAll('#content select option')).map((o) => o.textContent));
  };
  const toggle = async (id) => {
    await page.goto('/#/settings');
    await expect(page.locator('#main-content h1').first()).toBeVisible();
    await page.locator('#settings-toggle-hidden-' + id).click();
  };

  // --- 詳細ページの推薦 ---
  // control: 隠す前は推薦に出ている
  expect(await recoHasTaskManager(), 'control: 隠す前から推薦に出ていない').toBe(true);
  await toggle('p01');
  expect(await recoHasTaskManager(),
    '非表示にしたのに詳細ページの推薦に出続けている (#886 の listing mesh)').toBe(false);
  await toggle('p01');
  expect(await recoHasTaskManager(), '表示に戻したのに推薦へ復帰しない').toBe(true);

  // --- カテゴリ選択肢 ---
  // control: 隠す前は Security がある
  expect(await categories(), 'control: 隠す前から Security が無い').toContain('Security');
  for (const id of SEC) { await toggle(id); }
  expect(await categories(),
    'そのカテゴリの project を全部隠したのに選択肢が残っている — 選んでも 0 件になる死んだ選択肢'
  ).not.toContain('Security');
  await toggle(SEC[0]);
  expect(await categories(), '1 件戻したのにカテゴリ選択肢が復帰しない').toContain('Security');
});

