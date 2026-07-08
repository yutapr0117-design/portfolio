const { test, expect } = require('@playwright/test');


// ===== 7.2: Projects 検索フォーカス維持 Behavior Check =====
test('Projects search input retains focus during filtering', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const searchInput = page.locator('input[type="text"]').first();
  await searchInput.click();
  await searchInput.type('AI', { delay: 50 });

  // 検索後もフォーカスが維持されていること（バグ: v52以前はフォーカス喪失していた）
  await expect(searchInput).toBeFocused();
});


// ===== 7.2: Projects 検索の 0 件マッチ empty-state =====
// ProjectsPage の renderGrid は getFilteredProjects() が空のとき「条件に一致するプロジェクトは
// ありません。」(role=status, aria-live) を表示し件数を 合計 0 件 にする。検索フォーカス維持は
// 被覆済みだが、この empty-state 分岐 (quiz の empty-state とは別 page) は未カバーだった。一致しない
// 検索 → 空状態メッセージ + 0 件 + カード 0、を実検証する。
test('Projects search shows an empty state when nothing matches', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const searchInput = page.locator('input[type="text"]').first();
  await searchInput.fill('zzz-no-such-project-xyz-9999');

  await expect(page.getByText('条件に一致するプロジェクトはありません。')).toBeVisible();
  await expect(page.getByText('合計 0 件')).toBeVisible();
  await expect(page.locator('.grid-projects article.card')).toHaveCount(0);
});


// ===== 7.2: 検索の fill→絞り込み→clear→全件復帰 lifecycle =====
// 既存テストは「0 件マッチ empty-state」(非マッチ語) と「タグクリック由来の絞り込み」は被覆するが、
// 検索語を入れて部分集合に絞り → クリアで全件に戻る round-trip (getFilteredProjects の token あり/
// なし分岐の往復) は未カバーだった。tokenizer のスコアリング詳細に依存しない robust 形 (絞込後 <
// 全件 かつ >=1、クリア後 == 全件) で検証する。'ポモドーロ' は default では p03 のみが持つ語。
test('Projects search filters to a subset then clears back to the full list', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const cards = page.locator('.grid-projects article.card');
  await expect(cards.first()).toBeVisible(); // [FIX] SPA 描画完了を auto-wait してから数える (snapshot count flake 防止)
  const total = await cards.count();
  expect(total, 'projects page should list multiple projects initially').toBeGreaterThan(1);

  const search = page.locator('input[type="text"]').first();
  await search.fill('ポモドーロ');
  // 絞り込まれる: 全件未満かつ 1 件以上 (default では p03 のみ該当)
  await expect.poll(async () => await cards.count()).toBeLessThan(total);
  await expect(cards.first()).toBeVisible();

  // クリアで全件復帰 (token なし分岐 → category 'All' の全件)
  await search.fill('');
  await expect(cards).toHaveCount(total);
});


// ===== 7.2: プロジェクトカードのタグクリックでフィルタ (#tag → 検索) =====
// 各カードのタグ badge (`#tag` ボタン) クリックは q=tag / cat=All に設定し検索入力値も更新して
// 再描画 + syncURL する (components.js)。category select / 検索入力フィルタとは別の「カードの
// タグから絞り込む」distinct な導線で未カバーだった。先頭タグをクリック → 検索入力にタグが入り
// URL に q= が反映、結果 >=1 件、を実検証する。
test('Clicking a project card tag filters projects by that tag', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const tagBtn = page.locator('.grid-projects button.badge').filter({ hasText: '#' }).first();
  await expect(tagBtn).toBeVisible();
  const tagText = (await tagBtn.textContent()).replace('#', '').trim();

  await tagBtn.click();

  // 検索入力にタグが入り、URL に q= 反映、絞り込み結果 >=1
  await expect(page.locator('input[type="text"]').first()).toHaveValue(tagText);
  await expect(page).toHaveURL(/[?&]q=/);
  await expect(page.locator('.grid-projects article.card').first()).toBeVisible();
});


// ===== 7.2: プロジェクトのカテゴリフィルタ (件数絞り込み + URL ディープリンク) =====
// ProjectsPage は select(aria-label='カテゴリフィルター') で cat を切替え、getFilteredProjects が
// p.category===cat で絞り込み、syncURL が ?cat= を replaceSilently で URL に反映する (focus 喪失を
// 避けるため grid のみ再描画)。検索フォーカス維持テストはあるが、カテゴリ絞り込み + URL 反映は
// 未カバーだった。実カテゴリ名をハードコードせず「2 番目の option 選択 → 件数が減る + URL に cat=
// → All で総数復帰」を実検証する (フィルタ条件 / URL sync が壊れたら検知)。
test('Projects category filter narrows the list and syncs to the URL', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const countLabel = page.getByText(/合計 \d+ 件/);
  const total = parseInt((await countLabel.textContent()).match(/\d+/)[0], 10);
  expect(total, 'should have multiple projects to filter').toBeGreaterThan(1);

  const catSelect = page.locator('select[aria-label="カテゴリフィルター"]');
  // 先頭 'All' の次=最初の実カテゴリ (名前はデータ依存なので index で選ぶ)
  const firstRealCat = await catSelect.locator('option').nth(1).getAttribute('value');
  await catSelect.selectOption(firstRealCat);

  // 件数が絞られる (0 < filtered < total)
  const filtered = parseInt((await page.getByText(/合計 \d+ 件/).textContent()).match(/\d+/)[0], 10);
  expect(filtered).toBeGreaterThan(0);
  expect(filtered).toBeLessThan(total);
  // URL に cat= が反映 (deep-link 可能)
  await expect(page).toHaveURL(/[?&]cat=/);

  // All に戻すと総数復帰 + URL から cat= が消える
  await catSelect.selectOption('All');
  const restored = parseInt((await page.getByText(/合計 \d+ 件/).textContent()).match(/\d+/)[0], 10);
  expect(restored).toBe(total);
  await expect(page).not.toHaveURL(/[?&]cat=/);
});


// ===== 7.2: プロジェクト browse→detail→back のコア導線 =====
// ProjectsPage のカード「詳細を見る」は Router.navigate(`projects/<slug>`) で ProjectDetailPage
// へ遷移し、詳細側「← 一覧に戻る」で navigate('projects') で戻る。route-render テストは直接 URL で
// 詳細が描画されることのみ見ており、一覧からのクリック導線 (params slug 解決 + 往復) は未カバー
// だった。最も基本的な閲覧ジャーニーを実検証する: 一覧→詳細 (slug URL + 詳細描画)→一覧。
test('Project card navigates to detail and back (browse journey)', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  // 最初のカードの「詳細を見る」で詳細へ
  const detailBtn = page.getByRole('button', { name: '詳細を見る' }).first();
  await expect(detailBtn).toBeVisible();
  await detailBtn.click();

  // slug URL へ遷移し詳細ページ (戻るボタン) が描画される
  await expect(page).toHaveURL(/#\/projects\/[^/]+$/);
  const backBtn = page.getByRole('button', { name: '← 一覧に戻る' });
  await expect(backBtn).toBeVisible();
  let fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `project detail caused a fatal: ${fatal}`).toBeNull();

  // 「← 一覧に戻る」で一覧へ復帰
  await backBtn.click();
  await expect(page).toHaveURL(/#\/projects$/);
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `back navigation caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: project detail「おすすめ（自動）」からの遷移 (autoRelatedCandidates 実行) =====
// ProjectDetailPage は Store.autoRelatedCandidates(project, all, 8) の出力を「おすすめ（自動）」
// セクションのボタン群として描画し、各ボタンが Router.navigate(projects/slug) で別詳細へ飛ぶ。
// この類似度計算 → 実ナビの導線は未カバーだった。一覧→詳細へ入り、おすすめセクションの先頭ボタンが
// 存在する (非 vacuous) ことを assert し、クリックで別 slug の詳細へ遷移 + fatal なしを検証する。
test('Project detail "auto-recommended" card navigates to another project (autoRelated)', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '詳細を見る' }).first().click();
  await expect(page).toHaveURL(/#\/projects\/[^/]+$/);
  const firstUrl = page.url();

  // 「おすすめ（自動）」= autoRelatedCandidates 由来セクションの先頭ボタン (非 vacuous に存在を要求)
  const recSection = page.locator('section.card').filter({ has: page.getByRole('heading', { name: 'おすすめ（自動）' }) });
  const recBtn = recSection.getByRole('button').first();
  await expect(recBtn).toBeVisible();

  // クリック → 別 slug の詳細へ遷移
  await recBtn.click();
  await expect(page).toHaveURL(/#\/projects\/[^/]+$/);
  expect(page.url(), 'must navigate to a different project').not.toBe(firstUrl);
  await expect(page.getByRole('button', { name: '← 一覧に戻る' })).toBeVisible();
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `autoRelated navigation caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: home「注目のプロジェクト」→ 詳細への遷移 (home→detail ジャーニー) =====
// HomePage の featured セクション「詳細 →」は Router.navigate(projects/featured.slug) で featured
// プロジェクト詳細へ飛ぶ。projects 一覧→詳細 (別テスト) とは別の、home からの導線で未カバーだった。
// home の featured「詳細 →」クリックで slug URL の詳細へ遷移 + 戻るボタン描画 + fatal なしを検証。
test('Home featured project navigates to its detail page', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const featured = page.locator('article.card').filter({ has: page.getByRole('heading', { name: '注目のプロジェクト' }) });
  const detailBtn = featured.getByRole('button', { name: /詳細/ });
  await expect(detailBtn).toBeVisible();
  await detailBtn.click();

  await expect(page).toHaveURL(/#\/projects\/[^/]+$/);
  await expect(page.getByRole('button', { name: '← 一覧に戻る' })).toBeVisible();
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `home featured nav caused a fatal: ${fatal}`).toBeNull();
});


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


// ===== 7.2: URL ディープリンクから検索クエリを復元 (q= param) =====
// ProjectsPage は `let q = route.query.q || ''` で初期 q を決め、input の value: q で入力欄に
// 反映し、renderGrid() で絞り込んだ状態で初期描画する。「URL をコピーして共有」「ブラウザ戻る」
// などで ?q=xxx に直接到達した場合に検索状態が復元されることが前提だが、この「初期復元」経路は
// 既存テストが全て goto('/#/projects') → fill() でフィルタするパターンであり、URL から直接
// 到達する分岐は被覆されていなかった (route.query.q の代入が消えても既存 e2e が通る vacuous gap)。
test('Projects page restores search query from URL deep-link (?q=)', async ({ page }) => {
  await page.goto('/#/projects?q=ポモドーロ');
  await page.waitForLoadState('domcontentloaded');

  // route.query.q が input の初期 value に復元されていること (deep-link restore の核心 assertion)
  const searchInput = page.locator('input[type="text"]').first();
  await expect(searchInput).toHaveValue('ポモドーロ');

  // 絞り込みが実際に機能していること (input 値を set するだけで filter が動かない退行も検知)
  await expect(page.locator('.grid-projects article.card').first()).toBeVisible();
});


// ===== 7.2: URL ディープリンクからカテゴリフィルタを復元 (cat= param) =====
// ProjectsPage は `let cat = route.query.cat || 'All'` で初期カテゴリを決め、renderGrid() で
// 絞り込んだ状態で初期描画する。option 側の selected 属性で select の視覚選択も反映する。
// ?cat=xxx への直接到達時にフィルタ状態が復元されることを検証する。
// 注意: 一度 projects に来て selectOption 後に同じ URL へ goto しても DOM 状態が残るため vacuous に
// なる。ホーム(/) → deep-link の 2 段 goto で必ず fresh な SPA 初期化を経ること。
test('Projects page restores category filter from URL deep-link (?cat=)', async ({ page }) => {
  // 1. 最初の実カテゴリ名を取得 (select の option 値をページ描画前に確認)
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  const catSelect = page.locator('select[aria-label="カテゴリフィルター"]');
  const firstRealCat = await catSelect.locator('option').nth(1).getAttribute('value');

  // 2. ホームへ移動して既存 DOM 状態を破棄 → deep-link で直接到達 (hashchange 経由で fresh 初期化)
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.goto(`/#/projects?cat=${encodeURIComponent(firstRealCat)}`);
  await page.waitForLoadState('domcontentloaded');

  // 3. option の selected 属性により select が cat= の値で視覚的に選択されていること
  await expect(catSelect).toHaveValue(firstRealCat);
  // 4. 絞り込みが実際に機能していること
  await expect(page.locator('.grid-projects article.card').first()).toBeVisible();
});


// ===== 7.2: ProjectDetailPage の "not found" 状態 + 復帰ナビ =====
// ProjectDetailPage(slug) は state.projects.find(p => p.slug === slug) が null のとき
// 「プロジェクトが見つかりません」h1 + 「一覧へ戻る」ボタンを描画する。
// この !project 分岐は他のテストでカバーされておらず、バグが発生してもサイレントに素通りする gap だった。
// (security-proxy.spec.js は実在 slug の描画のみを確認; aio-meta.spec.js は NotFoundPage (別コンポーネント) のみ)
test('ProjectDetailPage shows not-found message and returns to list for nonexistent slug', async ({ page }) => {
  await page.goto('/#/projects/nonexistent-slug-99999');
  await page.waitForLoadState('domcontentloaded');

  // !project 分岐で「プロジェクトが見つかりません」h1 が描画されること
  await expect(page.getByRole('heading', { name: 'プロジェクトが見つかりません' })).toBeVisible();

  // 行き止まりでなく「一覧へ戻る」ボタンが存在すること
  await expect(page.getByRole('button', { name: '一覧へ戻る' })).toBeVisible();

  // 「一覧へ戻る」クリックで projects 一覧ページへ遷移すること
  await page.getByRole('button', { name: '一覧へ戻る' }).click();
  await expect(page.locator('.grid-projects')).toBeVisible();
});
