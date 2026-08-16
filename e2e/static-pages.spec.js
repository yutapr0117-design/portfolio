const { test, expect } = require('@playwright/test');

// ===== 静的ページ (role-split / hiring-risk / ai-knowhow) =====
// データを持たず、内容が JS に直書きされている 3 ページ。プロジェクト一覧のような
// 状態を持たないので壊れ方も違う —— 「描画されているか」と「機械可読な構造
// (ARIA table 意味論) が保たれているか」が主な関心事になる。
// role-split の表は WebMCP のツールが `data-ai-role` で走査する **機械向けの契約**でも
// あり (#929)、崩れると視覚に出ないまま agentic surface が壊れる。
//
// 元は projects.spec.js にあったが、同 file が早期警告 (900 行) を超えたため
// **BLOCKING (1,000 行) を踏む前に**このテーマの塊を切り出した。
// mutation の `test` フィールドは title 一致ゆえ file 移動の影響を受けない。

// ===== 7.2: thesis ページの key 構造化コンテンツ presence (role-split 分担表) =====
// role-split は本プロジェクトの中核命題「Human vs AI 役割分担」を #role-split-table (region,
// aria-label='Human vs AI 詳細分担表') で提示する。route-render テストは「エラーなく描画」しか
// 見ないため、ページは描画されるが分担表が欠落する退行を捕捉できなかった。table region が
// 実際に描画されることを検証する。
test('Role-split page renders the Human-vs-AI division table', async ({ page }) => {
  await page.goto('/#/role-split');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#role-split-table')).toBeVisible();
  await expect(page.locator('#role-split-table')).toHaveAttribute('aria-label', /Human vs AI/);
});

// ===== 7.2: 分担表が ARIA table として構造露出される (WCAG 1.3.1) =====
// 分担表は div グリッドで組まれ table 要素を持たないため、SR には「カテゴリ / 人間（Human）の役割 /
// AI の役割 / 設計 / システムアーキテクチャの決定 …」という平坦なテキスト列にしか聞こえず、どのセルが
// どの列 (人間 or AI) に属するかという**本ページの主題そのもの**が伝わらなかった。ARIA table roles で
// 構造を露出する (属性のみ = render-neutral)。axe (a11y-axe.spec.js) は role の妥当性しか見ないため、
// 「表として読める」ことは role の実在と行/列見出しの対応でここに固定する。
test('Role-split division table exposes ARIA table semantics (rows, column and row headers)', async ({ page }) => {
  await page.goto('/#/role-split');
  await page.waitForLoadState('domcontentloaded');

  const table = page.getByRole('table', { name: 'Human と AI の役割分担' });
  await expect(table).toBeVisible();

  // 列見出し 3 つ (カテゴリ / 人間 / AI) が columnheader として露出する
  const colHeaders = table.getByRole('columnheader');
  await expect(colHeaders).toHaveCount(3);
  await expect(colHeaders.nth(0)).toHaveText('カテゴリ');
  await expect(colHeaders.nth(1)).toContainText('人間');
  await expect(colHeaders.nth(2)).toContainText('AI');

  // データ行は行見出し (カテゴリ名) + 2 セル (人間/AI) を持つ
  const rows = table.getByRole('row');
  await expect(rows).toHaveCount(9);                       // header 1 + data 8
  const designRow = rows.filter({ has: page.getByRole('rowheader', { name: '設計', exact: true }) });
  await expect(designRow.getByRole('cell')).toHaveCount(2);
  await expect(designRow.getByRole('cell').first()).toContainText('システムアーキテクチャの決定');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `role-split table semantics caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: thesis ページの key コンテンツ presence (hiring-risk lead) =====
// hiring-risk は採用側リスク低減という命題を h1「採用リスク低減」(data-ai-content='lead') で
// 提示する。route-render とは別に、この lead 見出しが描画されることを検証し、ページが空/別内容に
// なる退行を捕捉する。
test('Hiring-risk page renders its risk-reduction lead heading', async ({ page }) => {
  await page.goto('/#/hiring-risk');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByRole('heading', { name: /採用リスク低減/ })).toBeVisible();
});

// ===== 7.2: thesis ページの key コンテンツ presence (ai-knowhow lead) =====
// ai-knowhow は「AI-Driven PM の開発ノウハウ公開」命題を h1「AI開発ノウハウ」
// (data-ai-section='ai-knowhow') で提示する。role-split / hiring-risk と並ぶ thesis trio の 3 つ目。
// route-render とは別に lead 見出しの描画を検証し、ページが空/別内容になる退行を捕捉する。
test('AI-knowhow page renders its lead heading', async ({ page }) => {
  await page.goto('/#/ai-knowhow');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByRole('heading', { name: /AI開発ノウハウ/ })).toBeVisible();
});


// ===== 役割分担表: セル内の箇条書きがリストとして読める =====
// 各セルには 3〜4 件の箇条書きが並ぶ。role が無いと SR 利用者は「このセルに何項目あるか」も
// 項目の切れ目も掴めない (視覚的には ✦ の記号で分かる)。表の意味論 (#929 で機械向け契約として
// 固定した ARIA table) を壊さずに、セルの中だけへリストを足す。
//
// **wrapper は `display: contents`** —— セル自身は `role="cell"` を保つ必要があるので 1 段挟むが、
// 素の div だとレイアウトが変わる (#1076 で実測)。ページ高が変更前と完全一致することと、
// table / row / cell / rowheader の数が変わらないことの両方を確認する。
test('役割分担表のセル内箇条書きがリストとして公開される', async ({ page }) => {
  await page.goto('/#/role-split');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: '役割分担' })).toBeVisible();

  const bullets = await page.locator('.cell-bullet-row').count();
  expect(bullets, 'control: 箇条書きが描画されていない').toBeGreaterThan(10);

  // 箇条書きが listitem として公開される
  expect(await page.getByRole('listitem').count(),
    'セル内の箇条書きが listitem として公開されていない').toBe(bullets);
  expect(await page.getByRole('list').count(),
    '箇条書きを束ねる list が無い').toBeGreaterThan(0);

  // 表の意味論が壊れていない (#929 の機械向け契約)
  expect(await page.getByRole('table').count(), '表の意味論が壊れた').toBe(1);
  expect(await page.getByRole('cell').count(), 'セルが listitem に置き換わってしまった').toBeGreaterThan(8);
  expect(await page.getByRole('rowheader').count(), '行見出しが失われた').toBeGreaterThan(4);
});
