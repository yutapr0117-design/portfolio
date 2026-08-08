const { test, expect } = require('@playwright/test');


// ===== 7.2: Projects 検索フォーカス維持 Behavior Check =====
test('Projects search input retains focus during filtering', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const searchInput = page.getByLabel('プロジェクト検索');
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

  const searchInput = page.getByLabel('プロジェクト検索');
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

  const search = page.getByLabel('プロジェクト検索');
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
  await expect(page.getByLabel('プロジェクト検索')).toHaveValue(tagText);
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
  const searchInput = page.getByLabel('プロジェクト検索');
  await expect(searchInput).toHaveValue('ポモドーロ');

  // 絞り込みが実際に機能していること (input 値を set するだけで filter が動かない退行も検知)
  await expect(page.locator('.grid-projects article.card').first()).toBeVisible();
});

// ===== 7.1b: silent フィルタ後の full re-render で検索が消えない (route-state stale 退行) =====
// projects の検索は Router.replaceSilently('projects?q=..') で URL を静かに書き換える (再描画なし)。
// この silent 更新後に notify() 由来の full re-render (State.subscribe(render) — 例: cross-tab
// storage sync / 任意 State.update / window.render()) が起きると、_renderCore は Router.getRoute()
// から route を得るため、getRoute()(currentRoute) が silent 更新を反映していないと query.q が
// stale('') で読まれ ProjectsPage が未フィルタで再描画され検索が消える一方 URL は ?q=.. のまま残る
// desync バグになる。replaceSilently が currentRoute も同期することで防ぐ。window.render() は
// notify() 駆動の full re-render を代表する決定的トリガとして使う (mechanism 非依存の退行検知)。
test('Projects filter survives a full re-render after a silent URL update (getRoute stays in sync)', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const searchInput = page.getByLabel('プロジェクト検索');
  await searchInput.fill('ポモドーロ');
  await expect(searchInput).toHaveValue('ポモドーロ');
  // silent 更新で URL に ?q= が乗る
  await expect.poll(() => page.evaluate(() => location.hash)).toContain('q=');

  // 現在の input に印を付け、full re-render が #content を作り直して input を置換した瞬間を
  // 確定検知できるようにする (window.render() は promise を返さず async のため、単純な assert は
  // 再構築前の旧 input='ポモドーロ' に即マッチして vacuous になる — 印の消滅を待って新 input を見る)。
  await page.evaluate(() => {
    const el = document.querySelector('[aria-label="プロジェクト検索"]');
    if (el) { el.dataset.pretest = '1'; }
  });
  // notify() 由来の full re-render を強制 (cross-tab sync / State.update と同じ経路)
  await page.evaluate(() => window.render && window.render());
  // 印付き (旧) input が消える = #content 再構築完了
  await page.waitForFunction(
    () => !document.querySelector('[aria-label="プロジェクト検索"][data-pretest="1"]'),
    { timeout: 5000 }
  );

  // 再構築後の新 input が検索を保持し (getRoute() が URL と同期)、URL とも整合していること
  // (fix が無いと getRoute().query.q が stale('') で新 input は '' へリセットされ RED)。
  await expect(page.getByLabel('プロジェクト検索')).toHaveValue('ポモドーロ');
  await expect.poll(() => page.evaluate(() => location.hash)).toContain('q=');
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


// URL の cat= が現存カテゴリに無い場合 (stale bookmark / 手打ち / カテゴリ削除後) は 'All' へ正規化する。
// 修正前は <select> が該当 option 不在で先頭 'All' を表示するのに cat 変数は無効値のまま filter され
// list が空 = control 表示 (全カテゴリー) と実 filter の desync でユーザーに「All なのに 0 件」と誤提示していた。
// (外部入力 = URL query の validate discipline・#93/#295 の ingestion 正規化と同族)
test('Projects page normalizes an invalid ?cat= to All (control↔filter desync guard)', async ({ page }) => {
  // ホーム経由で fresh 初期化 → 存在しないカテゴリの deep-link で直接到達
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.goto('/#/projects?cat=DevOpsNonExistent');
  await page.waitForLoadState('domcontentloaded');

  const catSelect = page.locator('select[aria-label="カテゴリフィルター"]');
  // select は 'All' を表示している
  await expect(catSelect).toHaveValue('All');
  // 正規化により list は空でなくプロジェクトが表示される (修正前は 0 件・"条件に一致する…" が出て RED)
  await expect(page.locator('.grid-projects article.card').first()).toBeVisible();
  await expect(page.locator('#content', { hasText: '条件に一致するプロジェクトはありません' })).toHaveCount(0);
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


// ===== 7.2: ProjectsPage カードの デモ/詳細を見る ボタンが accessible name に p.name を含み一意化 =====
// #819/#820/#821 と同 class。一覧は複数カードを並べるが、修正前は各カードの「デモ」「詳細を見る」
// ボタンが全カードで同一 accessible name (可視テキスト由来) を持ち、SR ユーザーがどのプロジェクトへ
// 遷移するボタンか区別できなかった (WCAG 4.1.2)。可視テキストは維持しつつ aria-label に p.name を
// suffix し一意化する (可視語を prefix に含むため WCAG 2.5.3 Label in Name も充足)。先頭 2 カードの
// 見出し名を読み、その名前入りの「詳細を見る：<name>」ボタンが各々一意に存在することを検証する。
test('Project card action buttons include the project name in their accessible name (unique per card)', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const cards = page.locator('article.card--flex-col');
  await expect(cards.first()).toBeVisible();
  const n0 = (await cards.nth(0).locator('h2').innerText()).trim();
  const n1 = (await cards.nth(1).locator('h2').innerText()).trim();
  expect(n0).not.toBe('');
  expect(n1).not.toBe(n0); // 先頭 2 件は別プロジェクト (一意性検証の前提)

  // 各カードの「詳細を見る」が見出し名込みの一意な accessible name で exact 引きできる。
  await expect(page.getByRole('button', { name: `詳細を見る：${n0}`, exact: true })).toHaveCount(1);
  await expect(page.getByRole('button', { name: `詳細を見る：${n1}`, exact: true })).toHaveCount(1);

  // クリックで実際にその slug の詳細へ遷移する (aria-label 追加が導線を壊さない)。
  await page.getByRole('button', { name: `詳細を見る：${n0}`, exact: true }).click();
  await expect(page).toHaveURL(/#\/projects\/[^/]+$/);
  await expect(page.getByRole('heading', { name: n0 }).first()).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `projects card a11y caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: default プロジェクトの並べ替えが reload を跨いで保持される (mergeProjectsWithDefaults 順序保持) =====
// settings の ↑↓ は state.projects を swap して並べ替え、表示順 (= state.projects 順) に反映する。
// 従来 mergeProjectsWithDefaults は defaults を「元の定義順」で再構築し incoming 順を無視したため、
// default project 同士の並べ替えが reload の normalize round-trip で silent に元順へ戻る data-fidelity
// バグがあった (user 追加 project は incoming 順 append で保持されるので default だけが失われた)。
// 先頭 default を 1 つ下げて描画順の入れ替えを確認 → reload → 入れ替えが保持されることを検証する。
// localStorage は load で再書き込みされないため「描画順」(in-memory state.projects) を読む
// (localStorage を読む検査は pre-reload の値を拾い vacuous になる)。
test('Default project reorder persists across reload (mergeProjectsWithDefaults preserves saved order)', async ({ page }) => {
  const rendered = () => page.evaluate(() =>
    Array.from(document.querySelectorAll('.grid-projects article h2')).map(el => el.textContent.trim()));

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
  const initial = await rendered();

  // settings で先頭 default 行を 1 つ下げる
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const rows = page.locator('div.flex.items-center.justify-between.gap-2');
  await rows.first().getByRole('button', { name: '↓' }).click();

  // projects へ戻り描画順が入れ替わっている (先頭 2 件が swap)
  await page.goto('/#/projects');
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
  await expect.poll(async () => (await rendered()).slice(0, 2).join(',')).toBe([initial[1], initial[0]].join(','));
  const afterSwap = await rendered();

  // reload 後も入れ替えが保持される (normalize round-trip で元順へ戻らない)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
  await expect.poll(async () => (await rendered()).slice(0, 3).join(',')).toBe(afterSwap.slice(0, 3).join(','));

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `default reorder persist caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: プロジェクトの非表示 (projectPrefs.hiddenIds) が reload を跨いで保持される =====
// settings の「非表示」は projectPrefs.hiddenIds に id を push し、ProjectsPage は
// hiddenIds を filter して公開一覧から除く。既存の hide/unhide test は同一セッション内の
// route 往復のみで、reload の normalize round-trip (store.js が projectPrefs.hiddenIds を
// 読み戻すか) は未検証だった。hiddenIds が normalize で drop されると reload 後に非表示に
// したプロジェクトが公開一覧へ復活する silent な persist-drift になる (#294/#568/#684/#871 と
// 同 class)。非表示 → reload → 依然 公開一覧に不在、を検証する。
test('Hidden project stays hidden on the public list across reload (projectPrefs.hiddenIds normalize round-trip)', async ({ page }) => {
  const name = 'HIDE-PERSIST-PROJ-3170';

  // 一意プロジェクトを追加し非表示にする
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByPlaceholder('プロジェクト名').fill(name);
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();
  const row = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name });
  await row.getByRole('button', { name: '非表示' }).click();
  await expect(row.getByRole('button', { name: '表示' })).toBeVisible();

  // 公開一覧から消えている (同一セッション)
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
  await expect(page.getByText(name)).toHaveCount(0);

  // reload しても非表示が保持される (normalize round-trip で hiddenIds が drop されない)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
  await expect(page.getByText(name)).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `hidden project persist caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: プロジェクト検索が search landmark (role='search') で公開される (ARIA APG) =====
// 検索入力を role='search' の landmark で包み、SR ユーザーが landmark ナビゲーションで検索領域へ
// 直接ジャンプできる (WCAG 1.3.1)。landmark が検索 input を内包することを検証する。
test('Projects search is exposed as an ARIA search landmark containing the query input', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const searchLandmark = page.getByRole('search');
  await expect(searchLandmark).toBeVisible();
  // landmark が検索 input (aria-label='プロジェクト検索') を内包する
  await expect(searchLandmark.getByRole('searchbox', { name: 'プロジェクト検索' })).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `search landmark caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: プロジェクト件数表示が status live region で絞り込み時にアナウンスされる (WCAG 4.1.3) =====
// 検索/カテゴリ絞り込みで `合計 N 件` が変わっても、従来は SR ユーザーへ通知されなかった (非 0 件の
// 件数変化は silent)。countDisplay を role=status + aria-live=polite にし、focus を移さず件数変化を
// アナウンスする。live region が件数テキストを持ち、絞り込みで更新されることを検証する。
test('Projects result count is an aria-live status region that updates on filtering (WCAG 4.1.3)', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  // 件数表示は role=status + aria-live=polite の live region
  const countStatus = page.locator('p[role="status"][aria-live="polite"]').filter({ hasText: '合計' });
  await expect(countStatus).toBeVisible();
  const before = (await countStatus.textContent()).trim();

  // 検索で絞り込む → 件数テキストが更新される (live region が変化を announce)
  const search = page.getByRole('searchbox', { name: 'プロジェクト検索' });
  await search.fill('zzz-no-match-xyzzy-9999');
  await expect(countStatus).toHaveText(/合計 0 件/);
  expect((await countStatus.textContent()).trim()).not.toBe(before);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `count live region caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: 自動推薦が「自分自身」と「明示 related」を除外する (二重表示ガード) =====
// Store.autoRelatedCandidates は `p.id !== target.id && !fixed.has(p.id)` で (a) 対象自身と
// (b) target.relatedProjectIds に既にある明示 related を候補から落とす。この除外が壊れると
// 「関連プロジェクト」節と「おすすめ（自動）」節に同じプロジェクトが二重表示され、さらに自分自身
// への自己リンクが出る (実害: 推薦枠 8 件が既知の関連で埋まり新規発見価値が失われる)。従来の
// autoRelated テストは「先頭ボタンが別 slug へ飛ぶ」だけを見ており、この除外 invariant は未カバー
// だった。default p01(task-manager) は relatedProjectIds=["p02","p03","p04"] を実際に持ち、同一
// カテゴリ Productivity ゆえ類似度 > 0 = 除外を外せば必ず両節に出る (非 vacuous)。
test('Auto-recommendations exclude self and explicitly-related projects (no duplicate listing)', async ({ page }) => {
  await page.goto('/#/projects/task-manager');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1', { hasText: 'タスク管理アプリ' })).toBeVisible();

  const relSection = page.locator('section.card').filter({ has: page.getByRole('heading', { name: '関連プロジェクト' }) });
  const recSection = page.locator('section.card').filter({ has: page.getByRole('heading', { name: 'おすすめ（自動）' }) });
  await expect(relSection).toBeVisible();
  await expect(recSection).toBeVisible();

  // 両節ともに候補を持つ (空集合同士の積は自明に空 = vacuous になるため件数を先に要求)
  const relNames = (await relSection.getByRole('button').allInnerTexts()).map(t => t.trim()).filter(Boolean);
  const recNames = (await recSection.getByRole('button').allInnerTexts()).map(t => t.trim()).filter(Boolean);
  expect(relNames.length, 'explicit related list must be non-empty').toBeGreaterThan(0);
  expect(recNames.length, 'auto-recommendation list must be non-empty').toBeGreaterThan(0);

  // (b) 明示 related は自動推薦から除外される → 2 節の積集合は空
  const overlap = recNames.filter(n => relNames.includes(n));
  expect(overlap, `auto-recommendations duplicated explicit related: ${overlap.join(', ')}`).toEqual([]);

  // (a) 対象自身は自動推薦に出ない (自己リンク禁止)
  expect(recNames, 'auto-recommendations must not include the project itself').not.toContain('タスク管理アプリ');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `auto-related exclusion check caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: 非表示プロジェクトが「公開一覧以外の全 listing 面」からも消える =====
// projectPrefs.hiddenIds を見ていたのは ProjectsPage (公開一覧) と SettingsPage (管理 UI) だけで、
// home の「注目のプロジェクト」/ 詳細ページの推薦 (関連・おすすめ) / Cmd+K 候補は素の state.projects
// から描いていた。default project は削除ボタンが disabled (「デフォルトは非表示のみ」) ＝非表示が
// 唯一の非公開手段なのに、既定 featured の p01 を隠してもトップ最上位の注目枠に出続けるなど、
// 「一覧だけの部分的な隠蔽」に留まっていた (producer/consumer mesh の read 面漏れ)。
// 既定 featured である「タスク管理アプリ」(p01・p02 の関連にも入る) を隠し、3 面すべてから
// 消えることを検証する。各面 fix の除去でこのテストが RED になる (mutation 登録済)。
test('Hidden project disappears from home featured, detail recommendations and Cmd+K', async ({ page }) => {
  const target = 'タスク管理アプリ';

  // 既定 featured を非表示にする (aria-label は行ごとに一意 — #563 の a11y 対応による)
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: `非表示：${target}` }).click();
  await expect(page.getByRole('button', { name: `表示：${target}` })).toBeVisible();

  // (1) home の「注目のプロジェクト」に出ない (描画確定を待ってから不在検査)
  await page.goto('/#/');
  await page.waitForLoadState('domcontentloaded');
  const featuredCard = page.locator('article.card').filter({ has: page.getByRole('heading', { name: '注目のプロジェクト' }) });
  await expect(featuredCard).toBeVisible();
  await expect(featuredCard.getByText(target)).toHaveCount(0);

  // (2) 詳細ページの推薦に出ない (p02 todo-list は relatedProjectIds に p01 を持つ)
  await page.goto('/#/projects/todo-list');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1', { hasText: 'TODOリスト' })).toBeVisible();
  const recHeading = page.getByRole('heading', { name: 'おすすめ（自動）' });
  await expect(recHeading).toBeVisible();   // 推薦セクション自体は描画されている (非 vacuous)
  await expect(page.getByRole('button', { name: target })).toHaveCount(0);

  // (3) Cmd+K の候補に出ない (候補リスト自体は描画されていることを先に確認)
  await page.keyboard.press('Control+k');
  await expect(page.locator('#command-palette-host')).toHaveAttribute('aria-hidden', 'false');
  await page.locator('.cmdk-input').fill('タスク');
  await expect(page.locator('.cmdk-item').first()).toBeVisible();
  await expect(page.locator('.cmdk-item').filter({ hasText: target })).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `hidden-project listing leak check caused a fatal: ${fatal}`).toBeNull();
});
