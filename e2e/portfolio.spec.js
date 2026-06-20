// e2e/portfolio.spec.js
// Extracted from .github/workflows/playwright-regression.yml (P2: Playwright file-based consolidation)
// Do NOT embed this file in workflow heredocs — both regression and snapshot workflows reference it directly.

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const path = require('path');
const fs   = require('fs');

// Detect whether a screenshot baseline exists for the current platform.
// Playwright stores snapshots under e2e/<spec>-snapshots/<name>-<browser>-<platform>.png
function baselineExists(name) {
  const snapshotDir = path.join(__dirname, 'portfolio.spec.js-snapshots');
  if (!fs.existsSync(snapshotDir)) return false;
  const files = fs.readdirSync(snapshotDir);
  return files.some(f => f.startsWith(name));
}

// Detect baseline-generation mode (set by update-playwright-snapshots.yml).
// In this mode the screenshot test MUST run even when no baseline exists yet,
// otherwise `--update-snapshots` would have nothing to capture and the baseline
// could never be generated (the original skip-guard deadlock — P0-01).
function isSnapshotUpdateMode() {
  return process.env.PLAYWRIGHT_UPDATE_SNAPSHOTS === '1';
}

// ===== 7.1: AIO Anchor 可視化バグ検知 =====
test('AIO asset anchor must be hidden (non-visual)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  const anchor = page.locator('#aio-asset-anchor');
  await expect(anchor).toHaveCount(1);
  // 視覚的に非表示であることを確認（attributeがhiddenである）
  await expect(anchor).toHaveAttribute('hidden', '');
  // boundingBoxがnull（非表示）であることをアサート
  const box = await anchor.boundingBox();
  expect(box).toBeNull();
});

// ===== 7.1: 外部リンクの noopener/noreferrer 強制 (tabnabbing / referrer 漏洩防止) =====
// render 末尾で secureExternalLinks(document) が全 a[target=_blank] に rel="noopener noreferrer" を
// 付与する (main.js / aidk-rails の Security Rail)。これは reverse tabnabbing (window.opener 乗っ取り)
// と referrer 漏洩を防ぐセキュリティ不変条件だが、その動的強制は従来 e2e 未カバーだった。(1) home の
// 実外部リンクが全て noopener+noreferrer を持つこと、(2) rel 未設定の外部リンクを注入し再描画すると
// 強制が補完すること、の双方を検証する。secureExternalLinks が止まると検知する。
test('External target=_blank links are hardened with noopener+noreferrer (security)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // (1) home の実外部リンク (例: Zenn) が全て noopener + noreferrer を持つ
  const externalLinks = page.locator('a[target="_blank"]');
  const count = await externalLinks.count();
  expect(count, 'home should render at least one external link (non-vacuous)').toBeGreaterThan(0);
  for (let i = 0; i < count; i++) {
    const rel = (await externalLinks.nth(i).getAttribute('rel')) || '';
    expect(rel, `external link #${i} must include noopener`).toContain('noopener');
    expect(rel, `external link #${i} must include noreferrer`).toContain('noreferrer');
  }

  // (2) rel 未設定の外部リンクを document に注入 → ハッシュ遷移で再描画 (フルリロードせず
  //     secureExternalLinks(document) を起動) → 強制が rel を補完することを検証
  await page.evaluate(() => {
    const a = document.createElement('a');
    a.href = 'https://example.com/';
    a.target = '_blank';
    a.id = 'e2e-injected-unsafe-link';
    a.textContent = 'unsafe';
    document.body.appendChild(a); // #content 外 + リロードしないので残る
    location.hash = '#/projects'; // hashchange → Router → render → secureExternalLinks(document)
  });
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();

  const injected = page.locator('#e2e-injected-unsafe-link');
  await expect(injected).toHaveAttribute('rel', /noopener/);
  await expect(injected).toHaveAttribute('rel', /noreferrer/);
});

// ===== 7.1: ホームページ初期レンダリング =====
test('Homepage renders without console errors', async ({ page }) => {
  // pageerror (未捕捉 JS 例外) と console.error を分けて収集する。前者は常に app バグなので
  // 無条件で失敗させ、後者からは非致命/環境由来ノイズのみ除外する (intent = app-logic エラー検出)。
  const consoleErrors = [];
  const pageErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') { consoleErrors.push(msg.text()); }
  });
  page.on('pageerror', err => pageErrors.push(err.message));

  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // Fatal エラーがないことを確認
  const fatalOverlay = page.locator('#portfolio-safety-net-host');
  await expect(fatalOverlay).toHaveCount(0);

  // h1 が表示されていることを確認
  const h1 = page.locator('h1, .h1').first();
  await expect(h1).toBeVisible();

  // 環境由来ノイズ判定: テスト用静的サーバ (http-server) が並列負荷でリソース取得に失敗すると
  // console に "Failed to load resource" / "net::ERR_*" を吐くが、これは本番 CDN では発生しない
  // テストインフラ起因のノイズで app-logic エラーではない。必須リソース欠落は render 系テスト
  // (h1 可視 / screenshot) が別途検出するため、ここでは除外して flake を排除する。
  const isEnvNoise = (e) => e.includes('Failed to load resource') || e.includes('net::');

  // app 由来の致命的 console エラーのみ抽出 (既存の非致命フィルタ + 環境ノイズ除外)
  const fatalConsole = consoleErrors.filter(e =>
    !e.includes('non-fatal') &&
    !e.includes('View Transition') &&
    !e.includes('SW') &&
    !isEnvNoise(e)
  );
  // pageerror (未捕捉例外) は環境ノイズ除外せず常に失敗対象
  const fatalErrors = [...pageErrors, ...fatalConsole];
  expect(fatalErrors, 'Fatal errors: ' + JSON.stringify(fatalErrors)).toHaveLength(0);
});

// ===== 7.2: ハッシュルーティング状態遷移 Behavior Check =====
test('Hash routing transitions correctly between routes', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // Projects ページへ遷移
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  // #content が表示されており aria-busy が false に戻っていること
  const content = page.locator('#content');
  await expect(content).toBeVisible();
  await expect(content).toHaveAttribute('aria-busy', 'false');

  // ホームへ戻る
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  // .hero-section が表示されること
  const hero = page.locator('.hero-section');
  await expect(hero).toBeVisible();
});

// ===== 7.1: ルート毎の document.title / meta description 更新 (AIO/SEO 中核) =====
// applyMeta (meta-management.js) は PAGE_META を引き、ルート遷移ごとに document.title を
// "<RouteTitle> | <name> - <role>" 形式に、meta[name=description] を該当 desc に更新する。
// このプロジェクトは AIO-first (機械可読性) が中核目標であり、ルート毎の正しい title/description は
// AI クローラ/検索の解釈に直結するが、その動的更新は従来 e2e 未カバーだった。主要ルートで title
// 先頭と meta description の内容が切り替わることを実検証する (applyMeta が止まると検知)。
test('Each route updates document.title and meta description (AIO/SEO)', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page).toHaveTitle(/^Projects \| /);
  await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', /設計判断/);

  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect(page).toHaveTitle(/^About \| /);
  await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', /プロフィール/);

  await page.goto('/#/contact');
  await page.waitForLoadState('domcontentloaded');
  await expect(page).toHaveTitle(/^Contact \| /);
  await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', /お問い合わせ/);
});

// ===== 7.1: ルート毎の動的 JSON-LD Article + og:type 注入/削除 (AIO-first 中核) =====
// injectStructuredData (meta-management.js) は ARTICLE_ROUTES (=['ai-knowhow']) のとき
// script[data-ld="article"] に Article schema を注入し og:type=article にする。非該当ルートでは
// その script を削除し og:type=website に戻す。これは AI クローラ向け動的構造化データ = 本プロジェクト
// 中核の AIO サーフェスだが未カバーだった。article ルートで JSON-LD Article が valid に注入され、
// 別ルートへ移ると除去されることを実検証する (injectStructuredData が壊れたら AIO 退行を検知)。
test('Article routes inject JSON-LD Article + og:type and clean up on leave (AIO)', async ({ page }) => {
  // article ルート: JSON-LD Article 注入 + og:type=article
  await page.goto('/#/ai-knowhow');
  await page.waitForLoadState('domcontentloaded');
  const articleLd = page.locator('script[data-ld="article"]');
  await expect(articleLd).toHaveCount(1);
  const ld = JSON.parse(await articleLd.textContent());
  expect(ld['@type']).toBe('Article');
  expect(ld.headline, 'headline は ai-knowhow の title を含む').toContain('AI開発ノウハウ');
  expect(ld.author && ld.author['@type']).toBe('Person');
  await expect(page.locator('meta[property="og:type"]')).toHaveAttribute('content', 'article');

  // 非 article ルートへ移動: Article script 除去 + og:type=website
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('script[data-ld="article"]')).toHaveCount(0);
  await expect(page.locator('meta[property="og:type"]')).toHaveAttribute('content', 'website');
});

// ===== 7.1: robots meta の soft-404 保護 + og/twitter/canonical 同期 (AIO/SEO 衛生) =====
// updateDocumentHead (meta-management.js) は not-found ルートで robots を 'noindex, nofollow' に、
// 実ルートで 'index, follow, ...' に切替える soft-404 保護を持ち、og:title/twitter:title を title に、
// canonical/og:url を CANONICAL_URL に同期する。これらは AI クローラ/検索のインデックス制御 = AIO/SEO
// 衛生の中核だが未カバーだった。特に NotFound が誤ってインデックスされる soft-404 退行を防ぐ。
test('Robots meta protects against soft-404 + og/canonical sync (SEO hygiene)', async ({ page }) => {
  // 実ルート: index, follow + og:title が title を反映 + canonical が正規 URL
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', /index, follow/);
  const title = await page.title();
  await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', title);
  await expect(page.locator('meta[name="twitter:title"]')).toHaveAttribute('content', title);
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', /yutapr0117-design\.github\.io\/portfolio/);

  // not-found ルート: noindex, nofollow (soft-404 保護)
  await page.goto('/#/zzz-nonexistent-route-9999');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex, nofollow');

  // 実ルートへ戻ると index, follow に復帰
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', /index, follow/);
});

// ===== 7.1: ルートエンティティアンカー = 機械可読なエンティティ権威 + 曖昧性排除 (AIO 第一目標) =====
// injectRouteEntityAnchor (meta-management.js) は #ai-route-entity-anchor (sr-only / aria-hidden) に
// ルート毎のエンティティ宣言を注入する: 横井雄太 / Yuta Yokoi への帰属、「実装は AI 生成・設計判断は
// 横井雄太」、Boring Technology アーキ、そして「Not affiliated with any academic researcher」(学術
// 研究者との曖昧性排除)。これは本プロジェクトの第一目標 = AI クローラ/LLM に正しくエンティティを
// 解釈・引用させる機械可読権威の中核だが未カバーだった。アンカーの存在・属性・主要 entity 宣言・
// ルート毎の Current view 更新を実検証する (entity authority が壊れたら AIO ミッション退行を検知)。
test('Route entity anchor declares entity authority and disambiguation (AIO core)', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const anchor = page.locator('#ai-route-entity-anchor');
  await expect(anchor).toHaveCount(1);
  await expect(anchor).toHaveAttribute('aria-hidden', 'true');
  // sr-only (視覚非表示) であること
  await expect(anchor).toHaveClass(/\bsr-only\b/);

  // エンティティ権威 + 曖昧性排除の宣言を含む
  await expect(anchor).toContainText('横井雄太');
  await expect(anchor).toContainText('Yuta Yokoi');
  await expect(anchor).toContainText('Not affiliated with any academic researcher');
  await expect(anchor).toContainText('Current view: Projects');

  // 別ルートで Current view が更新される (ルート追従)
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#ai-route-entity-anchor')).toContainText('Current view: About');
  await expect(page.locator('#ai-route-entity-anchor')).toContainText('横井雄太');
});

// ===== 7.1: Speakable JSON-LD のルート毎 cssSelector 更新 (AI 音声アシスタント最適化) =====
// injectStructuredData は全ルートで script[data-ld="speakable"] に WebPage + SpeakableSpecification
// を注入し、cssSelector を SPEAKABLE_SELECTORS でルート毎に切替える (home は .hero-tagline 等の固有
// セレクタを持つ)。AI 音声アシスタントが読み上げるべき要素を指定する AIO サーフェスだが未カバー
// だった。home で固有セレクタが入り、別ルートで外れる (= ルート追従) ことを実検証する。
test('Speakable JSON-LD updates cssSelector per route (AIO voice)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.hero-section')).toBeVisible();

  const speakable = page.locator('script[data-ld="speakable"]');
  await expect(speakable).toHaveCount(1);
  const data = JSON.parse(await speakable.textContent());
  expect(data.speakable['@type']).toBe('SpeakableSpecification');
  expect(Array.isArray(data.speakable.cssSelector)).toBe(true);
  // home 固有セレクタを含む
  expect(data.speakable.cssSelector).toContain('.hero-tagline');

  // 別ルートへ移ると home 固有セレクタが外れる (ルート追従)
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect.poll(async () => {
    const d = JSON.parse(await page.locator('script[data-ld="speakable"]').textContent());
    return d.speakable.cssSelector.includes('.hero-tagline');
  }).toBe(false);
});

// ===== 7.2: aria-busy 状態遷移 Behavior Check =====
test('content div transitions aria-busy correctly during navigation', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const content = page.locator('#content');
  await expect(content).toHaveAttribute('aria-busy', 'false');

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(content).toHaveAttribute('aria-busy', 'false');
});

// ===== 7.1: body[data-ai-state] agentic サーフェス (render 毎に現在 route を機械可読公開) =====
// main.js は描画完了 (requestAnimationFrame) 毎に document.body[data-ai-state] へ
// {route, filter, loading} を JSON で書き込む。AI エージェントが DOM から現在状態を読める AIO-agentic
// サーフェスだが未カバーだった。ルート遷移で data-ai-state.route が追従することを expect.poll で検証。
test('Body data-ai-state reflects the current route (agentic surface)', async ({ page }) => {
  const routeOf = async () => page.evaluate(() => {
    try { return JSON.parse(document.body.getAttribute('data-ai-state')).route; } catch { return null; }
  });

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect.poll(routeOf).toBe('projects');

  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect.poll(routeOf).toBe('about');
});

// ===== 7.2: prefers-reduced-motion でのナビゲーション (WCAG 2.3.3 / 前庭安全) =====
// main.js は prefers-reduced-motion: reduce のとき View Transition を完全スキップする専用経路を
// 持つ (doc b §13.1 二重防衛)。この distinct code path でもナビゲーションが機能し (#content 更新・
// aria-busy 収束)、ErrorBoundary に落ちないことを検証する。動きに敏感なユーザーがアニメ無しでも
// 壊れず操作できることの保証。
test('Navigation works under prefers-reduced-motion (View Transition skipped)', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  const content = page.locator('#content');
  await expect(content).toHaveAttribute('aria-busy', 'false');
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();

  // 別ルートへもう一度遷移しても reduced-motion 経路で正常更新
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect(content).toHaveAttribute('aria-busy', 'false');
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `reduced-motion navigation caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.1: スクリーンショット差分テスト（ベースライン）=====
// Regression runs: skipped when no baseline image exists (prevents constant-failure on first run).
// Baseline-generation runs (PLAYWRIGHT_UPDATE_SNAPSHOTS=1 via update-playwright-snapshots.yml):
//   the test runs even without a baseline so `--update-snapshots` can capture it. (P0-01)
// Run update-playwright-snapshots.yml to generate the baseline, then commit the .png files.
test('Homepage screenshot regression', async ({ page }) => {
  if (!baselineExists('homepage-baseline') && !isSnapshotUpdateMode()) {
    test.skip(true, 'No screenshot baseline found. Run update-playwright-snapshots workflow to generate.');
  }
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(500); // アニメーション安定待ち
  await expect(page).toHaveScreenshot('homepage-baseline.png', {
    fullPage: false,
    clip: { x: 0, y: 0, width: 1280, height: 720 }
  });
});

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

// ===== 7.1: モバイルビューポートでのCLS検証 =====
test('No layout shift on mobile viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // topbar がmobileで表示されていること
  const topbar = page.locator('.topbar');
  await expect(topbar).toBeVisible();

  // サイドバーがmobileで非表示であること
  const sidebar = page.locator('.sidebar');
  await expect(sidebar).not.toBeVisible();
});

// ===== 7.2: テーマ切替の永続化 Behavior Check =====
// theme toggle (#themeBtnTop) は data-theme を cycle (system→dark→light→system) させ、
// State 経由で localStorage に永続化する。リロードを跨いだ往復 (theme-init.js の FOUC
// pre-paint → main.js Theme.init の再適用) が壊れていないことを検証する。Check 100 が
// FOUC pre-paint の storage キー一致を静的強制するのに対し、本テストは実ブラウザでの
// 切替→永続→復元の振る舞いを動的に保証する。
test('Theme toggle cycles data-theme and persists across reload', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const html = page.locator('html');
  const initial = await html.getAttribute('data-theme');

  // テーマ切替ボタンは desktop (sidebar) と mobile (#themeBtnTop) の両方に存在し同じ
  // aria-label を共有する。viewport で可視な方を選んでクリックする。
  const themeBtn = page.locator('button[aria-label="ライトモードとダークモードを切り替える"]:visible').first();
  await expect(themeBtn).toBeVisible();
  await themeBtn.click();

  const afterClick = await html.getAttribute('data-theme');
  expect(afterClick, 'data-theme must change after toggling the theme button').not.toBe(initial);

  // リロード後もテーマが永続化されていること（State → localStorage 往復）
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  const afterReload = await page.locator('html').getAttribute('data-theme');
  expect(afterReload, 'theme selection must persist across a page reload').toBe(afterClick);
});

// ===== 7.2: system テーマが OS の prefers-color-scheme に追従する =====
// Theme.apply は theme='system' のとき isDark = matchMedia('(prefers-color-scheme: dark)') で
// 解決し documentElement に 'dark' class を toggle する。さらに init で matchMedia の change を
// 購読し、system 選択時のみ OS テーマ変更へライブ追従する (theme.js §init 不変条件)。cycle
// テスト (data-theme 属性遷移) とは別に、この OS 解決 + ライブ追従経路を検証する。fresh context は
// 既定 theme='system' なので、emulateMedia で OS を dark/light に切替え 'dark' class の付与/解除を
// 実検証する。動きの保証 = OS をダークにしている利用者に常にダーク表示。
test('System theme follows the OS prefers-color-scheme (live)', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const html = page.locator('html');
  // fresh context は既定で system
  await expect(html).toHaveAttribute('data-theme', 'system');
  await expect(html).toHaveClass(/\bdark\b/);

  // OS を light へ → change リスナーが apply('system') 再実行 → dark class 解除
  await page.emulateMedia({ colorScheme: 'light' });
  await expect(html).not.toHaveClass(/\bdark\b/);
  await expect(html).toHaveAttribute('data-theme', 'system');

  // OS を再び dark へ → dark class 復帰
  await page.emulateMedia({ colorScheme: 'dark' });
  await expect(html).toHaveClass(/\bdark\b/);
});

// ===== 7.2: モバイルドロワーの開閉 + ARIA + Escape + focus 復帰 Behavior Check =====
// mobile (≤MOBILE_BREAKPOINT=920px) では sidebar が #menuBtn → #drawer (role=dialog,
// aria-modal) に畳まれる。開くと aria-expanded=true / drawer aria-hidden=false / 背景 #app が
// inert+aria-hidden で隔離され、Escape で閉じて focus が #menuBtn に復帰する。これは
// accessibility 上重要な focus-trap / background-isolation 契約だが従来 e2e 未カバーだった。
test('Mobile drawer opens with ARIA, isolates background, and closes on Escape', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const menuBtn = page.locator('#menuBtn');
  const drawer = page.locator('#drawer');
  await expect(menuBtn).toBeVisible();
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');

  // 開く: ARIA 状態と背景隔離
  await menuBtn.click();
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'true');
  await expect(drawer).toHaveAttribute('aria-hidden', 'false');
  await expect(drawer).toBeVisible();
  await expect(page.locator('#app')).toHaveAttribute('aria-hidden', 'true');

  // Escape で閉じる: ARIA 復元 + focus が menuBtn へ復帰
  await page.keyboard.press('Escape');
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');
  await expect(page.locator('#app')).not.toHaveAttribute('aria-hidden', 'true');
  await expect(menuBtn).toBeFocused();
});

// ===== 7.2: モバイルドロワーの focus trap (Tab が #drawer 内に閉じ込められる・WCAG 2.4.3 モーダル) =====
// __trapFocus は開いたドロワー内で Tab/Shift+Tab を focusable 要素間でループさせ、focus が背景
// (inert 化された #app) へ漏れないようにする。Escape クローズは被覆済みだがこの focus-trap (モーダル
// の a11y 必須要件) は未カバーだった。開いた状態で Shift+Tab (先頭→末尾へ wrap) + 複数 Tab を
// 送っても activeElement が常に #drawer 内に留まることを実検証する。
test('Mobile drawer traps focus within the dialog (WCAG modal focus trap)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  // 開直後 focus は drawer 内 (trapFocus が先頭へ)。Shift+Tab で末尾へ wrap しても drawer 内に留まる
  await page.keyboard.press('Shift+Tab');
  expect(await page.evaluate(() => !!document.activeElement?.closest('#drawer'))).toBe(true);

  // 複数回 Tab を送っても focus は #drawer から漏れない (背景 #app へ移らない)
  for (let i = 0; i < 8; i++) { await page.keyboard.press('Tab'); }
  expect(await page.evaluate(() => !!document.activeElement?.closest('#drawer'))).toBe(true);
  expect(await page.evaluate(() => !!document.activeElement?.closest('#app'))).toBe(false);
});

// ===== 7.2: モバイルドロワーからのナビゲーション (リンククリック → 遷移 + 自動クローズ) =====
// drawer 内 navLink は isDrawer のとき onclick で Router.navigate(path) に加え closeDrawer() を
// 呼ぶ (components.js)。Escape クローズ (#上) とは別の閉路 = ナビゲーション経由のクローズで、
// モバイルで目的ページへ飛ぶ最も普通の操作にも関わらず従来未カバーだった。ドロワーを開いて
// Projects リンクをクリックし、(1) #/projects へ遷移し本文描画 (2) drawer が自動クローズ
// (aria-hidden=true) (3) 背景隔離 (#app aria-hidden) も解除、を実検証する。
test('Mobile drawer nav link navigates and auto-closes the drawer', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const menuBtn = page.locator('#menuBtn');
  const drawer = page.locator('#drawer');
  await menuBtn.click();
  await expect(drawer).toHaveAttribute('aria-hidden', 'false');

  // ドロワー内の Projects ナビリンクをクリック
  const projectsLink = drawer.locator('a.nav-link[href="#/projects"]');
  await expect(projectsLink).toBeVisible();
  await projectsLink.click();

  // (1) 遷移して本文描画
  await expect(page).toHaveURL(/#\/projects$/);
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  // (2) drawer が自動クローズ
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  // (3) 背景隔離も解除
  await expect(page.locator('#app')).not.toHaveAttribute('aria-hidden', 'true');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `drawer nav caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: クイズ検索フィルタ + 空状態 Behavior Check =====
// #/quiz の検索 input (aria-label='問題検索') は oninput で .quiz-question-block を絞り込み、
// 一致ゼロのとき .panel-empty (aria-live=polite) の「見つかりませんでした」を表示する。
// 検索クリアで全件復帰する。Projects 検索 (focus 維持) とは別ページ・別データセットの
// フィルタ + 空状態契約で従来 e2e 未カバーだった。
test('Quiz search filters question blocks and shows empty state on no match', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  const blocks = page.locator('.quiz-question-block');
  const initial = await blocks.count();
  expect(initial, 'quiz should render question blocks initially').toBeGreaterThan(0);

  const search = page.locator('input[aria-label="問題検索"]');
  await expect(search).toBeVisible();

  // 一致しない検索 → 空状態 + ブロック 0
  await search.fill('zzz-no-such-question-xyz');
  await expect(page.locator('.panel-empty')).toBeVisible();
  await expect(blocks).toHaveCount(0);

  // クリアで全件復帰
  await search.fill('');
  await expect(blocks).toHaveCount(initial);
});

// ===== 7.2: 設計判断問題集 (?type=architecture) の構造化レンダリング分岐 =====
// QuizPage は quizType=architecture のとき isArchitecture 分岐で intro banner + 状況/
// ステークホルダー主張/問の構造化ゾーン (.quiz-stakeholder-quote / .quiz-question-prompt) を
// 描画する (他 3 種 aws/pm/quality とは別 code path)。既存 quiz テストは default(aws) の検索
// のみ見ており、この distinct な構造化分岐は未カバーだった。?type= query 経由のルーティング
// (router の queryPart 解析) + architecture 専用 DOM の描画を実検証する。
test('Quiz architecture type renders structured stakeholder/question zones (?type query)', async ({ page }) => {
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');

  // タイトルが architecture 用に切り替わる (QUIZ_DATA_MAP lookup)
  await expect(page.locator('h1', { hasText: '設計判断問題集' })).toBeVisible();

  // architecture 専用の構造化ゾーンが描画される
  await expect(page.locator('.quiz-stakeholder-quote').first()).toBeVisible();
  await expect(page.locator('.quiz-question-prompt').first()).toBeVisible();
  await expect(page.locator('.quiz-question-block').first()).toBeVisible();

  // ErrorBoundary に落ちていない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `architecture quiz render caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: タスク管理アプリの追加 + リロード永続化 Behavior Check =====
// #/apps/task は #task-input に入力 → Enter で State.update 経由でタスクを追加し、
// localStorage (State auto-save) へ永続化する。apps セクションは従来「ルートが描画される」
// テストのみで、実際のデータ操作 (add → 永続 → reload で復元) は未カバーだった。State の
// Proxy 永続パスを実ブラウザで動的検証する (theme/drawer/quiz に続く interactive coverage)。
test('Task app adds a task and persists it across reload', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();

  // 一意なタイトルで衝突を避ける (固定文字列 + 数値を埋め込み、Math.random は使わない)
  const title = 'E2E-PERSIST-CHECK-TASK-7421';
  await input.fill(title);
  await input.press('Enter');

  // 追加直後にカードが描画される
  await expect(page.getByText(title)).toBeVisible();

  // リロード後も State (localStorage) から復元される
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(title)).toBeVisible();
});

// ===== 7.2: タスク入力の IME composition ガード (日本語入力の誤確定防止) =====
// task-input の Enter ハンドラは IME 変換確定の Enter (e.isComposing=true) でタスクを追加しては
// ならない (todo は todoComposing で対応済みだが task は未対応だった = 日本語が主対象の本サイトで
// 実バグ)。修正で `!e.isComposing` ガードを追加。composing 中の Enter では追加されず、通常の Enter
// では追加されることを実検証する。
test('Task input ignores Enter during IME composition (Japanese input safety)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  const t = 'IME-COMPOSING-TASK-2200';

  // IME 変換確定の Enter (isComposing=true) ではタスクを追加しない
  await input.fill(t);
  await input.evaluate((el) => {
    el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', isComposing: true, bubbles: true, cancelable: true }));
  });
  await expect(page.getByText(t)).toHaveCount(0);

  // 通常の Enter (isComposing=false) では追加される
  await input.press('Enter');
  await expect(page.getByText(t)).toBeVisible();
});

// ===== 7.2: タスクの kanban ステータス移動 (未着手→進行中→完了) + 永続 =====
// タスクカードの「→」は moveStatus(task, +1) で status を backlog→in-progress→done と進める
// (backlog で「←」/ done で「→」は disabled)。add+persist テストはあるがこの kanban 列移動という
// 別 operation は未カバーだった。追加→「→」で進行中列へ→もう一度「→」で完了列へ移り、リロード後も
// 完了列に残る (status 永続) ことを実検証する。
test('Task moves across kanban columns and persists the status', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  const title = 'KANBAN-MOVE-TASK-4400';
  await input.fill(title);
  await input.press('Enter');

  const inProgress = page.locator('section.card.bg-secondary').filter({ has: page.getByRole('heading', { name: '進行中' }) });
  const done = page.locator('section.card.bg-secondary').filter({ has: page.getByRole('heading', { name: '完了' }) });

  // 追加直後は未着手。→ で 進行中 へ
  await page.locator('article', { hasText: title }).getByRole('button', { name: '→' }).click();
  await expect(inProgress.getByText(title)).toBeVisible();

  // もう一度 → で 完了 へ
  await page.locator('article', { hasText: title }).getByRole('button', { name: '→' }).click();
  await expect(done.getByText(title)).toBeVisible();

  // リロード後も 完了 列に残る (status 永続)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  const doneAfter = page.locator('section.card.bg-secondary').filter({ has: page.getByRole('heading', { name: '完了' }) });
  await expect(doneAfter.getByText(title)).toBeVisible();
});

// ===== 7.2: タスク削除 (task CRUD: add/move/delete を完成) =====
// タスクカードの削除ボタン (aria-label='タスクを削除') は deleteTask(id) で State から該当タスクを
// 除去し「タスクを削除しました」を出す。add/move はカバー済みだが削除は未カバーだった。追加→削除で
// カードが消え通知が出ることを実検証し task CRUD のカバレッジを完成させる。
test('Task can be deleted from the board', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  const title = 'DELETE-ME-TASK-7799';
  await input.fill(title);
  await input.press('Enter');

  const card = page.locator('article', { hasText: title });
  await expect(card).toBeVisible();

  // 削除 → カードが消える + 通知
  await card.getByRole('button', { name: 'タスクを削除' }).click();
  await expect(page.locator('#toast-container').getByText('タスクを削除しました')).toBeVisible();
  await expect(page.getByText(title)).toHaveCount(0);
});

// ===== 7.2: タスク優先度フィルタ (カードで優先度変更 → high/med/all で振り分け) =====
// タスクカードの優先度 select (aria-label='タスクの優先度') は updateTask で priority を変更し、
// ヘッダの絞り込み select (aria-label='優先度で絞り込み') は getFilteredTasks で
// taskFilter.priority に一致するものだけ表示する。card 優先度変更 + フィルタ分岐は未カバーだった。
// 1 件を high に変更し、high/med/all フィルタで表示集合が切り替わることを実検証する。
test('Task priority filter narrows the board by priority', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  const hi = 'PRIO-HIGH-TASK-3301';
  const md = 'PRIO-MED-TASK-3302';
  await input.fill(hi);
  await input.press('Enter');
  await expect(page.getByText(hi)).toBeVisible();
  // hi の優先度を high に変更 (既定は med)
  await page.locator('article', { hasText: hi }).getByLabel('タスクの優先度').selectOption('high');
  await input.fill(md);
  await input.press('Enter');
  await expect(page.getByText(md)).toBeVisible();

  const filter = page.getByLabel('優先度で絞り込み');

  // high → hi のみ
  await filter.selectOption('high');
  await expect(page.getByText(hi)).toBeVisible();
  await expect(page.getByText(md)).toHaveCount(0);

  // med → md のみ
  await filter.selectOption('med');
  await expect(page.getByText(md)).toBeVisible();
  await expect(page.getByText(hi)).toHaveCount(0);

  // all → 両方
  await filter.selectOption('all');
  await expect(page.getByText(hi)).toBeVisible();
  await expect(page.getByText(md)).toBeVisible();
});

// ===== 7.1b: localStorage QuotaExceeded 時の graceful degradation =====
// State の保存経路 (state.js scheduleSave/saveNow) は Storage.set が false を返したとき
// notifyStorageError() でユーザーに通知し、in-memory state はそのまま維持する設計
// (storage.js は容量超過例外を握りつぶして false を返す)。read 側 (corrupt-storage) とは
// 別の write 側耐障害性: localStorage.setItem が QuotaExceededError を投げても (1) タスク
// 追加は in-memory で機能し描画される (2) ErrorBoundary (FatalPage) に落ちない
// (3) ストレージエラーがログされる。動きの保証 = ディスク満杯でも操作を失わない。
test('Task app degrades gracefully when localStorage write quota is exceeded', async ({ page }) => {
  // setItem だけを QuotaExceededError で失敗させる (getItem は機能させ、初期 theme 読込等は壊さない)
  await page.addInitScript(() => {
    const proto = window.Storage && window.Storage.prototype;
    if (proto) {
      proto.setItem = function () {
        const err = new Error('quota');
        err.name = 'QuotaExceededError';
        throw err;
      };
    }
  });

  const consoleErrors = [];
  page.on('console', msg => { if (msg.type() === 'error') {consoleErrors.push(msg.text());} });

  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();

  const title = 'E2E-QUOTA-DEGRADE-TASK-3390';
  await input.fill(title);
  await input.press('Enter');

  // (1) 書き込みは失敗しても in-memory state で描画される
  await expect(page.getByText(title)).toBeVisible();

  // (2) FatalPage (ErrorBoundary) に落ちていない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quota write failure caused a fatal: ${fatal}`).toBeNull();

  // (3) ストレージ上限エラーが通知 (console.error) される (debounce save 後)
  await expect.poll(
    () => consoleErrors.some(t => t.includes('ストレージ上限')),
    { timeout: 5000 }
  ).toBe(true);
});

// ===== 7.1c: クロスタブ同期 (storage イベント → 別タブの更新を採用) =====
// state.js は window 'storage' イベントを購読し、別タブ (modifiedBy ≠ 自タブの TAB_ID) からの
// より新しい書き込み (lastModified 比較) を採用 → 再描画 + 「別タブで更新されました」toast を出す。
// この multi-tab 経路は単一ページのテストでは発火しない (storage イベントは書き込んだタブ自身には
// 飛ばない) ため従来未カバー。同一 context の 2 ページ (localStorage 共有・sessionStorage=TAB_ID は
// タブ毎に独立) で実検証する。複数タブで同じポートフォリオを開いても状態が同期される保証。
test('Cross-tab sync: a task added in one tab appears in another tab', async ({ context }) => {
  const tabA = await context.newPage();
  const tabB = await context.newPage();

  await tabA.goto('/#/apps/task');
  await tabA.waitForLoadState('domcontentloaded');
  await tabB.goto('/#/apps/task');
  await tabB.waitForLoadState('domcontentloaded');

  // タブ B にはまだ存在しないことを確認 (negative baseline)
  const title = 'E2E-CROSS-TAB-SYNC-TASK-5108';
  await expect(tabB.getByText(title)).toHaveCount(0);

  // タブ A でタスクを追加 → State debounce save で localStorage 書き込み
  const inputA = tabA.locator('#task-input');
  await expect(inputA).toBeVisible();
  await inputA.fill(title);
  await inputA.press('Enter');
  await expect(tabA.getByText(title)).toBeVisible();

  // タブ B が storage イベントを受信 → 採用 → 再描画でタスクが現れる
  await expect(tabB.getByText(title)).toBeVisible({ timeout: 5000 });
  // 「別タブで更新されました」通知 (info toast) が出る
  await expect(tabB.locator('#toast-container').getByText('別タブで更新されました')).toBeVisible();

  await tabA.close();
  await tabB.close();
});

// ===== 7.2: TODO アプリの追加→完了トグル→一括削除フロー Behavior Check =====
// #/apps/todo は TodoPage (task とは別 factory / 別 State slice) で、addTodo (Enter) /
// toggleTodo (checkbox) / clearCompleted (「完了済み削除」一括操作) という distinct な
// コードパスを持つ。task テスト (#91) が add+persist を見るのに対し、本テストは toggle と
// bulk 削除という別 operation class を実ブラウザで動的検証する。
test('Todo app add, complete-toggle, then clear-completed removes the item', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  const text = 'E2E-TODO-FLOW-CHECK-3389';
  await input.fill(text);
  await input.press('Enter');

  // 追加された
  const item = page.locator('article', { hasText: text });
  await expect(item).toBeVisible();

  // 完了トグル (checkbox) → clearCompleted (「完了済み削除」) でリストから消える
  await item.locator('input[type="checkbox"]').check();
  await page.getByRole('button', { name: '完了済み削除' }).click();
  await expect(page.getByText(text)).toHaveCount(0);

  // リロード後も削除が永続している (State auto-save)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(text)).toHaveCount(0);
});

// ===== 7.2: TODO 入力の IME composition ガード (compositionstart/end フラグ機構) =====
// todo-input は task/ai の e.isComposing とは別に、手動 todoComposing フラグ
// (oncompositionstart→true / oncompositionend→false) で IME 変換確定 Enter の誤追加を防ぐ。
// この既存ガードは未テストだった。composition 中の Enter では追加されず、compositionend 後の Enter
// では追加されることを実検証し、3 入力 (task/ai/todo) すべての IME 保護カバレッジを完成させる。
test('Todo input ignores Enter during IME composition (compositionstart flag)', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  const t = 'TODO-IME-COMPOSING-2300';
  await input.fill(t);

  // composition 中 (todoComposing=true) の Enter では追加しない
  await input.evaluate((el) => el.dispatchEvent(new CompositionEvent('compositionstart', { bubbles: true })));
  await input.evaluate((el) => el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true })));
  await expect(page.getByText(t)).toHaveCount(0);

  // compositionend 後 (todoComposing=false) の Enter では追加される
  await input.evaluate((el) => el.dispatchEvent(new CompositionEvent('compositionend', { bubbles: true })));
  await input.evaluate((el) => el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true })));
  await expect(page.getByText(t)).toBeVisible();
});

// ===== 7.2: TODO フィルタ (未完了/完了/全て) の絞り込み分岐 =====
// TodoPage は select(aria-label='TODO を絞り込み') で todoFilter を切替え、getFilteredTodos が
// active→未完了のみ / completed→完了のみ / all→全件、と分岐する。既存 TODO テストは add/toggle/
// clear を見るがこの 3 値フィルタ分岐は未カバーだった。2 件追加→1 件完了→各フィルタで表示集合が
// 切り替わることを実検証する (フィルタ条件が壊れたら退行検知)。
test('Todo filter switches the visible set by active/completed/all', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  const done = 'E2E-TODO-DONE-6201';
  const active = 'E2E-TODO-ACTIVE-6202';

  // 1 件目を追加し、描画を待ってから 2 件目を追加 (連続追加の再描画レースを避ける)
  await input.fill(done);
  await input.press('Enter');
  await expect(page.getByText(done)).toBeVisible();
  await input.fill(active);
  await input.press('Enter');
  await expect(page.getByText(active)).toBeVisible();

  // done を完了にし、チェック反映を待つ
  const doneCheckbox = page.locator('article', { hasText: done }).locator('input[type="checkbox"]');
  await doneCheckbox.check();
  await expect(doneCheckbox).toBeChecked();

  const filter = page.locator('select[aria-label="TODO を絞り込み"]');

  // 完了 → done のみ表示・active は非表示
  await filter.selectOption('completed');
  await expect(page.getByText(done)).toBeVisible();
  await expect(page.getByText(active)).toHaveCount(0);

  // 未完了 → active のみ表示・done は非表示
  await filter.selectOption('active');
  await expect(page.getByText(active)).toBeVisible();
  await expect(page.getByText(done)).toHaveCount(0);

  // 全て → 両方表示
  await filter.selectOption('all');
  await expect(page.getByText(done)).toBeVisible();
  await expect(page.getByText(active)).toBeVisible();
});

// ===== 7.2: 設定アプリのデータエクスポート整合性 Behavior Check =====
// #/settings の「フルバックアップ」は downloadJSON(State.get()) で blob を生成し
// portfolio_full_<ts>.json として download する (data-integrity 機能)。CRUD とは別系統の
// 「State 全体を妥当な JSON として書き出せるか」を、Playwright の download イベントで動的検証。
test('Settings app exports a full backup as a valid JSON download', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const exportBtn = page.getByRole('button', { name: 'フルバックアップ' });
  await expect(exportBtn).toBeVisible();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    exportBtn.click(),
  ]);
  expect(download.suggestedFilename()).toMatch(/^portfolio_full_\d+\.json$/);

  // ダウンロード本体が State の妥当な JSON であること
  const content = fs.readFileSync(await download.path(), 'utf8');
  const parsed = JSON.parse(content);
  expect(parsed, 'export must contain the appsData State slice').toHaveProperty('appsData');
});

// ===== 7.2: 部分エクスポート (Projectsのみ / AppsDataのみ / Profileのみ) のスライス整合 =====
// exportProjects/Apps/Profile は downloadJSON で State の各スライス (projects 配列 / appsData /
// profile) を別ファイル名で書き出す。フルバックアップは被覆済みだが、部分エクスポートが「正しい
// スライスだけ」を出すか (誤って full store を出していないか) は未カバーだった。各ボタンの download
// 内容の shape + ファイル名 + 負アサーション (他スライスを含まない) を実検証する。
test('Settings partial export buttons download the correct State slice', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // Projectsのみ → projects 配列
  const [dlP] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Projectsのみ' }).click(),
  ]);
  expect(dlP.suggestedFilename()).toMatch(/^portfolio_projects_\d+\.json$/);
  const projects = JSON.parse(fs.readFileSync(await dlP.path(), 'utf8'));
  expect(Array.isArray(projects), 'projects export must be an array').toBe(true);
  expect(projects.length).toBeGreaterThan(0);

  // AppsDataのみ → appsData (tasks を持つ object・full store ではない)
  const [dlA] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'AppsDataのみ' }).click(),
  ]);
  expect(dlA.suggestedFilename()).toMatch(/^portfolio_apps_\d+\.json$/);
  const apps = JSON.parse(fs.readFileSync(await dlA.path(), 'utf8'));
  expect(apps).toHaveProperty('tasks');
  expect(apps, 'appsData export must NOT be the full store').not.toHaveProperty('projects');

  // Profileのみ → profile (email を持つ object・appsData を含まない)
  const [dlPr] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Profileのみ' }).click(),
  ]);
  expect(dlPr.suggestedFilename()).toMatch(/^portfolio_profile_\d+\.json$/);
  const profile = JSON.parse(fs.readFileSync(await dlPr.path(), 'utf8'));
  expect(profile).toHaveProperty('email');
  expect(profile, 'profile export must NOT contain appsData').not.toHaveProperty('tasks');
});

// ===== 7.2: 設定からのプロジェクト手動追加 (CRUD create → Projects ページ反映 + 永続) =====
// settings の addProjectManual はプロジェクト名を入力→「追加」で s.projects.unshift し slugify する。
// tasks/todos (appsData slice) とは別の projects domain への create 経路で、ProjectsPage の
// hiddenIds フィルタを通って公開一覧に現れる。空入力バリデーション (エラー Toast) と、追加後に
// /#/projects へ反映 + リロード永続を実検証する。projects への書き込み導線が壊れたら退行検知。
test('Settings can add a project manually and it appears on the Projects page', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const nameInput = page.getByPlaceholder('プロジェクト名');
  const addBtn = page.getByRole('button', { name: '追加', exact: true });
  await expect(nameInput).toBeVisible();

  // 空入力バリデーション: エラー Toast、追加されない
  await addBtn.click();
  await expect(page.locator('#toast-container').getByText('プロジェクト名を入力してください')).toBeVisible();

  // 正常追加
  const name = 'E2E-MANUAL-PROJECT-8420';
  await nameInput.fill(name);
  await addBtn.click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();

  // Projects ページ (hiddenIds フィルタ通過) に現れる
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();

  // リロード後も永続
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();
});

// ===== 7.2: 同名プロジェクト追加時の slug 一意化 (詳細ページ到達性) =====
// slugify は決定的なので、同名プロジェクトを 2 つ追加すると slug が重複し、ProjectDetailPage の
// find(p.slug===slug) が先頭のみ返して 2 つ目の詳細が到達不能になるバグがあった。修正で衝突時に
// -2 等を付与して一意化する。同名を 2 件追加し、両方の slug が異なる (= 詳細ページが別個に存在) ことを
// State から実検証する。
test('Adding two projects with the same name yields unique slugs (detail reachability)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const dupName = 'DUP-SLUG-PROJECT-7340';
  const addBtn = page.getByRole('button', { name: '追加', exact: true });
  const nameInput = page.getByPlaceholder('プロジェクト名');

  await nameInput.fill(dupName);
  await addBtn.click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();
  await nameInput.fill(dupName);
  await addBtn.click();

  const readSlugs = () => page.evaluate((nm) => {
    try {
      const st = JSON.parse(localStorage.getItem('portfolio_enhanced_v45'));
      return (st.projects || []).filter(p => p.name === nm).map(p => p.slug);
    } catch { return []; }
  }, dupName);

  // debounce save 完了 (2 件永続) を待つ
  await expect.poll(async () => (await readSlugs()).length).toBe(2);

  // 同名 2 件の slug が一意 (重複しない) こと
  const slugs = await readSlugs();
  expect(new Set(slugs).size, `slugs must be unique: ${JSON.stringify(slugs)}`).toBe(2);
});

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

// ===== 7.2: ユーザープロジェクトの削除 (confirm 受諾 → 永久削除) =====
// settings の deleteProjectHard は confirm() 確認の上 s.projects から id で除外する。デフォルト
// プロジェクト (defaultProjectIds) は削除不可 (ボタン disabled) で、ユーザー追加分のみ削除できる。
// add/hide とは別の destructive な CRUD 経路で、confirm ダイアログ + State からの完全除去が
// 従来未カバーだった。カスタム追加→confirm 受諾で削除→ settings リスト + /#/projects 双方から
// 消える、を実検証し projects CRUD (追加/非表示/削除) のカバレッジを完成させる。
test('Deleting a user project (confirm accepted) removes it everywhere', async ({ page }) => {
  // confirm() を常に受諾
  page.on('dialog', (dialog) => dialog.accept());

  // カスタムプロジェクトを追加
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const name = 'DELETE-PROJ-5560';
  await page.getByPlaceholder('プロジェクト名').fill(name);
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();

  // 公開一覧に出る
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();

  // settings の該当行で「削除」(user プロジェクトなので有効) → confirm 受諾
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const row = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name });
  await row.getByRole('button', { name: '削除' }).click();
  // settings リストから行が消える
  await expect(page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name })).toHaveCount(0);

  // 公開一覧からも消える (永続削除)
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name)).toHaveCount(0);
});

// ===== 7.2: 全データ初期化 (全リセット → confirm → defaults 復帰) =====
// settings の resetData は confirm() の上 State.set(Store.createDefaultStore()) で全状態を初期値へ
// 戻す最も破壊的な操作。snapshot/delete とは別経路で、ユーザーデータ (タスク等) を全消去し
// デフォルトへ戻す導線が未カバーだった。タスクを追加→「全リセット」confirm 受諾→初期化通知 +
// タスクが消えデフォルトに戻ることを実検証する (createDefaultStore への置換が壊れたら検知)。
test('Reset data restores defaults after confirm (destructive)', async ({ page }) => {
  page.on('dialog', (dialog) => dialog.accept());

  // タスクを追加 (デフォルトとの差分を作る)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  const input = page.locator('#task-input');
  await input.fill('RESET-TARGET-TASK-7788');
  await input.press('Enter');
  await expect(page.getByText('RESET-TARGET-TASK-7788')).toBeVisible();

  // 全リセット → confirm 受諾
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '全リセット' }).click();
  await expect(page.locator('#toast-container').getByText('初期化しました')).toBeVisible();

  // タスクが消え defaults に戻る
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('RESET-TARGET-TASK-7788')).toHaveCount(0);
  // crash していない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `reset caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: 設定アプリのスナップショット保存→反映 Behavior Check =====
// #/settings の「保存」は setSnapshot() で Storage.set(SNAPSHOT_KEY, ...) し、再描画後に
// getSnapshot()(=Storage.parse) が読み戻して「保存日時: …」を表示する。これは PR #93 で
// 注入漏れを修正した Storage 依存 (set/parse) の往復を実際に通す data-integrity パスで、
// 修正前は Storage.parse が render 時に throw して到達すらできなかった経路。
test('Settings app saves a snapshot and reflects the saved-at status', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 初期 (fresh context) は未保存
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();

  // 保存 → Storage.set → 再描画 → getSnapshot(Storage.parse) が読み戻し「保存日時:」表示
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByText(/保存日時:/)).toBeVisible();

  // リロード後も Storage から読み戻せる (永続)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(/保存日時:/)).toBeVisible();
});

// ===== 7.2: スナップショット削除 (clearSnapshot → 未保存へ復帰) =====
// clearSnapshot は Storage.remove(SNAPSHOT_KEY) + 再描画で「未保存」状態へ戻す。save/restore は
// 被覆済みだが clear (snapshot ライフサイクルの最後) は未カバーだった。snapshot 削除ボタンは
// btn-ghost (プロジェクト削除の btn-danger とは別) で識別する。保存→削除で「未保存」表示へ戻り、
// リロード後も未保存が永続することを実検証し snapshot ライフサイクル (save/restore/clear) を完成させる。
test('Settings snapshot can be cleared back to the unsaved state', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 保存 → 保存日時表示
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByText(/保存日時:/)).toBeVisible();

  // 削除 (snapshot clear = btn-ghost の「削除」。project 削除は btn-danger なので衝突しない)
  await page.locator('button.btn-ghost', { hasText: '削除' }).click();
  await expect(page.locator('#toast-container').getByText('スナップショットを削除しました')).toBeVisible();

  // 未保存状態へ復帰
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();
  await expect(page.getByText(/保存日時:/)).toHaveCount(0);

  // リロード後も未保存 (clear が永続)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();
});

// ===== 7.2: スナップショット復元のラウンドトリップ (保存→変更→復元で巻き戻る) =====
// save テスト (#上) は保存と保存日時表示の往復を見るが、復元 (restoreSnapshot → State.set(snap.data))
// で「保存時点へ実際に巻き戻る」中核機能は未カバーだった。これはユーザの undo/復旧の data-integrity
// 経路。タスク A を追加→保存→タスク B を追加→復元、で A は残り B が消える (保存時点へ revert) ことを
// 実検証する。復元が State.set を正しく通し永続データを差し替えることの保証。
test('Settings snapshot restore reverts state to the saved point', async ({ page }) => {
  // 1. タスク A を追加 (保存に含める状態)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  const input = page.locator('#task-input');
  await input.fill('SNAP-TASK-A-7700');
  await input.press('Enter');
  await expect(page.getByText('SNAP-TASK-A-7700')).toBeVisible();

  // 2. スナップショット保存 (A を含む)
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByText(/保存日時:/)).toBeVisible();

  // 3. 保存後にタスク B を追加 (この変更は snapshot に含まれない)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await input.fill('SNAP-TASK-B-7701');
  await input.press('Enter');
  await expect(page.getByText('SNAP-TASK-B-7701')).toBeVisible();

  // 4. 復元 → 保存時点 (A のみ) へ巻き戻る
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '復元', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('スナップショットを復元しました')).toBeVisible();

  // 5. タスク画面: A は残り B は消える (= 保存時点へ revert)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('SNAP-TASK-A-7700')).toBeVisible();
  await expect(page.getByText('SNAP-TASK-B-7701')).toHaveCount(0);
});

// ===== 7.2: AI アシストアプリの応答生成 Behavior Check =====
// #/apps/ai は #ai-input + 「送信」で submit() → analyzeInput → (300ms 後) generateResponse +
// State.update で appsData.ai.history に push し再描画する。task/todo とは別 State slice・別ロジック
// (ローカル生成・非同期 setTimeout) の distinct な対話パス。送信した prompt が履歴に現れることで
// submit→生成→State 反映→render の一連が壊れていないことを動的検証する。
test('AI assist app generates and renders a response for a prompt', async ({ page }) => {
  await page.goto('/#/apps/ai');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#ai-input');
  await expect(input).toBeVisible();
  const prompt = 'E2E-AI-PROMPT-デプロイ手順-5512';
  await input.fill(prompt);
  await page.getByRole('button', { name: '送信', exact: true }).click();

  // 生成完了後、prompt が history (テキスト) として描画される (input value ではなく本文)
  await expect(page.getByText(prompt)).toBeVisible();
});

// ===== 7.2: AI アシストの analyzeInput キーワード分岐 (troubleshoot/design/general) =====
// analyzeInput は入力に含まれるキーワードで応答タイプを 3 分岐する: 「エラー/バグ/失敗」→
// troubleshoot、「設計/計画/構成」→ design、それ以外 → general。既存 AI テスト (#上) は
// prompt が履歴に出ることのみ見ており、この分類ロジック (generateResponse の type 別出力) は
// 未カバーだった。各キーワードで送信し、対応する応答マーカーが描画されることを実検証する。
// 分類ロジックが壊れたら (例: キーワード変更で全部 general に倒れる) 退行を捕まえる。
test('AI assist routes prompts to troubleshoot/design/general responses by keyword', async ({ page }) => {
  await page.goto('/#/apps/ai');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#ai-input');
  const submit = page.getByRole('button', { name: '送信', exact: true });

  // 「エラー」→ troubleshoot
  await expect(input).toBeVisible();
  await input.fill('本番でエラーが出た');
  await submit.click();
  await expect(page.getByText('[AI分析: トラブルシューティング]')).toBeVisible();

  // 「設計」→ design
  await input.fill('新機能の設計を相談したい');
  await submit.click();
  await expect(page.getByText('[AI分析: 設計支援]')).toBeVisible();

  // キーワードなし → general
  await input.fill('こんにちは');
  await submit.click();
  await expect(page.getByText('[AI分析: 一般支援]')).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `AI assist branching caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: AI アシストの loading 状態機械 (送信→生成中→応答) =====
// submit() は aiLoading=true で即時再描画し、入力/送信を disabled にしてボタンを「生成中...」に変え、
// 300ms 後 (setTimeout) に generateResponse + aiLoading=false で「送信」へ戻す。分岐テストは応答内容を
// 見るが、この非同期 loading state machine (生成中表示 + disabled) は未カバーだった。fake clock で
// 300ms を決定的に制御し、loading 中→解決の遷移を検証する。
test('AI assist shows a loading state then resolves (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/ai');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#ai-input');
  await expect(input).toBeVisible();
  await input.fill('ローディング検証の質問');
  await page.getByRole('button', { name: '送信', exact: true }).click();

  // loading 中: ボタンが「生成中...」になり「送信」は消える
  await expect(page.getByRole('button', { name: '生成中' })).toBeVisible();
  await expect(page.getByRole('button', { name: '送信', exact: true })).toHaveCount(0);

  // 300ms 進める → 応答生成 + 「送信」へ復帰
  await page.clock.fastForward(300);
  await expect(page.getByRole('button', { name: '送信', exact: true })).toBeVisible();
  await expect(page.getByText('[AI分析:').first()).toBeVisible();
});

// ===== 7.2: AI 入力の IME composition ガード (日本語入力の誤送信防止) =====
// ai-input の Enter ハンドラは e.isComposing をチェックせず、日本語入力で IME 変換確定の Enter が
// 未確定テキストを誤って submit していた (task と同クラスの実バグ)。修正で `!e.isComposing` ガードを
// 追加。fake clock で「composing 中の Enter は submit されず応答が出ない」「通常 Enter は応答が出る」
// を決定的に検証する。
test('AI input ignores Enter during IME composition (Japanese input safety)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/ai');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#ai-input');
  await expect(input).toBeVisible();
  await input.fill('未確定の質問テキスト');

  // IME 変換確定の Enter (isComposing=true) では submit しない
  await input.evaluate((el) => {
    el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', isComposing: true, bubbles: true, cancelable: true }));
  });
  await page.clock.fastForward(500); // submit されていれば応答が出るはずの時間
  await expect(page.getByText('[AI分析:')).toHaveCount(0);

  // 通常の Enter (isComposing=false) では submit → 応答
  await input.press('Enter');
  await page.clock.fastForward(500);
  await expect(page.getByText('[AI分析:').first()).toBeVisible();
});

// ===== 7.2: ポモドーロのモード切替→タイマー表示更新 Behavior Check =====
// #/apps/pomodoro は集中/短休憩/長休憩ボタンで switchMode() → State 更新 + remaining を新モードの
// duration へリセットし、`.font-mono.text-stat` の MM:SS 表示が変わる。timer の tick に依存しない
// 非 flaky な対話 (mode 切替は即時)。apps 5 種 (task/todo/settings/ai/pomodoro) の対話カバレッジ完成。
test('Pomodoro mode switch resets and updates the timer display', async ({ page }) => {
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();
  const initial = (await timer.textContent()).trim();

  // 既定 (集中) から短休憩へ切替 → remaining が短休憩 duration にリセットされ表示が変化
  await page.getByRole('button', { name: '短休憩', exact: true }).click();
  await expect(timer).not.toHaveText(initial);
});

// ===== 7.2: ポモドーロの開始→カウントダウン→一時停止 Behavior Check (page.clock で決定的) =====
// timer は endAtMs (Date.now() ベース) で remaining を算出する。page.clock で時刻を決定的に進め、
// 開始でカウントダウンが進み、一時停止で停止することを flaky なしに検証する (mode 切替テストが
// 即時遷移のみだったのに対し、本テストは時間経過を伴う中核ロジックをカバー)。
test('Pomodoro start counts down and pause halts it (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();
  const t0 = (await timer.textContent()).trim();

  // 開始 → 3 秒進める → カウントダウンが進む
  await page.getByRole('button', { name: '開始' }).click();
  await page.clock.fastForward(3000);
  await expect(timer).not.toHaveText(t0);

  // 一時停止 → さらに進めても表示は変化しない (停止)
  await page.getByRole('button', { name: '一時停止' }).click();
  const tPaused = (await timer.textContent()).trim();
  await page.clock.fastForward(3000);
  await expect(timer).toHaveText(tPaused);
});

// ===== 7.2: ポモドーロ reset ボタン (満了値へ復帰 + 停止) =====
// reset() は stopTimer + remainingSec をモード duration へ戻す。switchMode (モード切替) や complete
// (0 到達) とは別経路で、稼働中の「リセット」ボタン押下は未カバーだった。開始→進める→リセットで
// 満了値に戻り、以降 clock を進めても変化しない (= 停止) ことを fake clock で決定的に検証する。
test('Pomodoro reset button restores full duration and stops (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();
  const full = (await timer.textContent()).trim();

  // 開始 → 5 秒進める → カウントダウン
  await page.getByRole('button', { name: '開始' }).click();
  await page.clock.fastForward(5000);
  await expect(timer).not.toHaveText(full);

  // リセット → 満了値へ復帰 + 「開始」へ戻る (停止)
  await page.getByRole('button', { name: 'リセット' }).click();
  await expect(timer).toHaveText(full);
  await expect(page.getByRole('button', { name: '開始' })).toBeVisible();

  // 停止後は clock を進めても変化しない
  await page.clock.fastForward(5000);
  await expect(timer).toHaveText(full);
});

// ===== 7.2: ポモドーロのセッション完了 (0 到達 → complete: history 記録 + リセット) =====
// start/pause テスト (#上) はカウントダウン継続/停止を見るが、タイマーが 0 に到達する complete()
// 経路 (setInterval 内の remaining<=0 分岐) は未テストだった。complete は history へ push し
// 「セッション完了！」toast を出して runtime を満了状態 (isActive=false / remainingSec=duration)
// に戻す。集中時間を 1 分に設定し fake clock で 0 到達まで進め、完了通知 + 「開始」へ戻る (停止) +
// 満了表示への復帰を決定的に検証する。集中→0 という apps の自動完了サイクルの保証。
test('Pomodoro completes at zero: shows done toast and resets to full duration (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  // 集中時間を 1 分に短縮 (onchange は blur で発火) → 満了まで 60 秒に
  const workInput = page.getByLabel('集中時間（分）');
  await workInput.fill('1');
  await workInput.blur();

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toHaveText('01:00');

  // 開始 → 61 秒進めて 0 到達 → complete()
  await page.getByRole('button', { name: '開始' }).click();
  await page.clock.fastForward(61000);

  // 完了通知が出る
  await expect(page.locator('#toast-container').getByText('セッション完了！')).toBeVisible();
  // runtime が満了状態へ戻る: 「一時停止」ではなく「開始」が再表示 (isActive=false)
  await expect(page.getByRole('button', { name: '開始' })).toBeVisible();
  // 表示は満了 duration (01:00) に復帰
  await expect(timer).toHaveText('01:00');
  // ErrorBoundary に落ちていない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `pomodoro completion caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: 稼働中に集中時間を変更 → 完了時のリセットが新しい設定値を使う (stale-closure 修正) =====
// getDuration も getRemaining と同じく render 毎キャプチャの closure `pomo` を読んでいたため、
// タイマー稼働中 (interval は start() 時の closure に固定) に集中時間を変更すると、完了時の
// remainingSec リセットが古い設定値になるバグがあった (getDuration を live state 参照に修正)。
// work=1 で開始→稼働中に work=2 へ変更→満了、で完了後の表示が新しい 02:00 になることを検証する。
test('Pomodoro completion uses the latest focus-duration setting changed mid-run', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const workInput = page.getByLabel('集中時間（分）');
  await workInput.fill('1');
  await workInput.blur();
  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toHaveText('01:00');

  // 開始 (work=1 の endAtMs で稼働)
  await page.getByRole('button', { name: '開始' }).click();

  // 稼働中に集中時間を 2 分へ変更 (active なので remainingSec/endAtMs は据え置き=稼働継続)
  await workInput.fill('2');
  await workInput.blur();

  // 満了まで進める → complete() の duration リセットは最新設定 (2 分) を使うべき
  await page.clock.fastForward(61000);
  await expect(page.locator('#toast-container').getByText('セッション完了！')).toBeVisible();
  await expect(page.getByRole('button', { name: '開始' })).toBeVisible();
  // 修正前は stale 設定で 01:00 に戻っていた。修正後は最新の 02:00。
  await expect(timer).toHaveText('02:00');
});

// ===== 7.2: skip link が main コンテンツへ focus を移す (WCAG 2.4.1 Bypass Blocks) =====
// `<a href="#main-content" class="skip-link">` はキーボード利用者がナビを飛ばして本文へ直接
// 到達する手段。focus → Enter で focus が #main-content (tabindex=-1) へ移ることを検証する。
// また hash routing (#/...) と競合して NotFound に落ちたり focus が移らない退行も同時に防ぐ。
test('Skip link moves focus to #main-content without breaking routing (WCAG 2.4.1)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const skip = page.locator('.skip-link');
  await skip.focus();
  await expect(skip).toBeFocused();

  await skip.press('Enter');
  // focus が #main-content へ移り、NotFoundPage に落ちていないこと
  await expect(page.locator('#main-content')).toBeFocused();
  await expect(page.getByRole('heading', { name: 'Not Found', exact: true })).toHaveCount(0);
});

// ===== 7.1: 壊れた localStorage からの graceful 復帰 (resilience) =====
// 永続データ (localStorage) が破損 JSON でも、Storage.parse の try/catch + Store.load の default
// fallback でアプリは crash せず既定状態で描画を継続すべき (fail-open)。破損値を仕込んで load し、
// FatalPage / NotFound に落ちず home が正常描画されることを検証する。設定画面 crash バグ (#93) で
// 「render 時クラッシュは致命的」と分かったため、永続層破損というもう一つの入力境界も固定する。
test('App recovers gracefully from corrupt localStorage (no FatalPage)', async ({ page }) => {
  await page.addInitScript(() => {
    try {
      localStorage.setItem('portfolio_enhanced_v45', 'not-valid-json-%%%');
      localStorage.setItem('portfolio_brand_v45', 'garbage-not-json');
    } catch (e) { /* noop */ }
  });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(200);

  // ErrorBoundary の FatalPage に落ちていない (window.__fatalError が falsy)
  const fatal = await page.evaluate(() => {
    const e = window.__fatalError;
    return e ? (e.message || String(e)) : null;
  });
  expect(fatal, `corrupt storage caused a fatal render: ${fatal}`).toBeNull();
  // home が正常描画され NotFound でもない
  await expect(page.locator('.hero-section')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Not Found', exact: true })).toHaveCount(0);
});

// ===== 7.1: スキーマ version 不一致時の安全マイグレーション (旧データ退避 → defaults リセット) =====
// Store.load() は parse 可能でも schemaVersion が現行 (CONSTANTS.SCHEMA_VERSION) と異なる旧データを
// 検出したとき、それを SNAPSHOT_KEY に {reason:'schema-mismatch', from, to, data} で退避してから
// createDefaultStore() で初期化する (将来のスキーマ変更で旧ユーザを crash させず、かつ旧データを
// 失わせない安全弁)。corrupt-storage テスト (parse 不能) とは別経路。古い schemaVersion の有効
// JSON を仕込んで load し、(1) crash せず home 描画 (2) 旧データが反映されず初期化 (3) snapshot に
// schema-mismatch で退避、を検証する。
test('Store migrates safely on schema version mismatch (snapshots old data, resets to defaults)', async ({ page }) => {
  await page.addInitScript(() => {
    try {
      // parse 可能だが旧 schemaVersion のデータ (現行は 12)。旧タスクを 1 件含める。
      localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
        schemaVersion: 1,
        type: 'full-store',
        theme: 'system',
        appsData: { tasks: [{ id: 'old-1', title: 'OLD-SCHEMA-TASK-9001', status: 'backlog', priority: 'med', tags: [] }] }
      }));
    } catch (e) { /* noop */ }
  });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // (1) crash せず home 描画
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `schema mismatch caused a fatal render: ${fatal}`).toBeNull();
  await expect(page.locator('.hero-section')).toBeVisible();

  // (3) 旧データが schema-mismatch として snapshot に退避される
  const snap = await page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('portfolio_snapshot_v45')); } catch { return null; }
  });
  expect(snap, 'old data should be snapshotted on schema mismatch').not.toBeNull();
  expect(snap.reason).toBe('schema-mismatch');
  expect(snap.from).toBe(1);

  // (2) 旧タスクは現行ストアに反映されない (defaults へ初期化)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('OLD-SCHEMA-TASK-9001')).toHaveCount(0);
});

// ===== 7.1: 設定インポートの不正 JSON 耐障害性 (graceful error) =====
// settings の importJSON は FileReader + JSON.parse を try/catch で囲み、不正ファイルでも crash
// せず「JSONのパースに失敗しました」エラー Toast を出す (fail-soft)。不正 JSON ファイルを与え、
// エラー Toast 表示 + FatalPage に落ちないことを検証する (もう一つの入力境界 = ファイルアップロード)。
test('Settings import shows an error for malformed JSON file without crashing', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles({
    name: 'broken.json',
    mimeType: 'application/json',
    buffer: Buffer.from('this is definitely not valid json ###'),
  });

  // 不正 JSON → エラー Toast 表示・crash しない（エラーは #toast-container と sr-only aria-live の
  // 両方に出る = 視覚 + screen reader 両対応。toast 側を検証する）。
  await expect(page.locator('#toast-container').getByText('JSONのパースに失敗しました')).toBeVisible();
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `malformed import caused a fatal render: ${fatal}`).toBeNull();
});

// ===== 7.2: 有効 JSON インポートの正常系ラウンドトリップ (data-recovery) =====
// importJSON は FileReader→JSON.parse→トグル (既定: include profile/projects/apps, mode=append)
// に従い State.update でマージ→validateAndNormalize→「インポートが完了しました」。malformed
// (error 系) は被覆済みだが、バックアップ復元という data-recovery の中核=正常系は未カバーだった。
// 新 id のプロジェクトを含む有効 JSON を import し、(1) 完了通知 (2) append でそのプロジェクトが
// /#/projects に現れる (3) リロード永続、を実検証する (import のマージ/正規化破壊を検知)。
test('Settings import (valid JSON) appends projects and persists (data recovery)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const imported = {
    projects: [{
      id: 'p_import_e2e_9911',
      slug: 'imported-proj-9911',
      name: 'IMPORTED-PROJ-9911',
      category: 'Imported',
      summary: 'e2e import roundtrip',
      problem: '', approach: '',
      tech: ['JS'], tags: ['import']
    }]
  };

  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles({
    name: 'backup.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(imported)),
  });

  // (1) 完了通知
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  // (2) append モードで新 id のプロジェクトが公開一覧に追加される
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('IMPORTED-PROJ-9911').first()).toBeVisible();

  // (3) リロード後も永続 (validateAndNormalize が user-added を保持)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('IMPORTED-PROJ-9911').first()).toBeVisible();
});

// ===== 7.1: profile の github/linkedin が import で保持される + URL サニタイズ (data fidelity + XSS) =====
// validateAndNormalize は従来 profile の name/title/bio/email だけを残し github/linkedin/location を
// strip していたため、バックアップ import でこれらが silently 消え ContactPage の該当リンクが
// dead code 化していた。修正で schema 定義済みフィールドを保持しつつ、github/linkedin は href 描画
// されるため http(s) のみ許可して javascript: 等の XSS を遮断する。有効 URL は ContactPage に
// 反映され、危険な URL は描画されないことを実検証する。
test('Profile github/linkedin survive import and are URL-sanitized (XSS-safe)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 注: profile.name は付けない (Check 58 が spec 内の `name: '<lowercase>'` を route 名として
  // 抽出するため。本テストは github/linkedin の保持/サニタイズのみ検証するので name は不要)。
  const backup = {
    profile: {
      github: 'https://github.com/e2e-test-acct',
      linkedin: 'javascript:alert(1)', // 危険スキーム → サニタイズで除去されるべき
    }
  };
  await page.locator('input[type="file"]').setInputFiles({
    name: 'profile-backup.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(backup)),
  });
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  // Contact ページ: 有効な github は href として保持される
  await page.goto('/#/contact');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('a[href="https://github.com/e2e-test-acct"]')).toBeVisible();

  // 危険スキームの linkedin は描画されない (サニタイズで '' に落ちて条件描画が抑止)
  expect(await page.locator('a[href^="javascript:"]').count()).toBe(0);
});

// ===== 7.1: axe-core 自動アクセシビリティ監査 — render-neutral critical 回帰防止 =====
// axe-core で WCAG 2a/2aa/21a/21aa を全主要ルートでスキャンし、render-neutral に修正可能な
// critical 違反群がゼロであることを機械強制する。本 increment で是正したバグの回帰防止:
//   - aria-valid-attr-value: aria-details が `#id`（IDREF 不正）かつ dangling だった全ルート critical
//   - select-name / button-name / label: settings/task/todo の form-control に accessible name が
//     無かった critical（aria-label を付与して是正）
// これらは ARIA 属性 / accessible name の付与のみで pixel 不変ゆえ §3 baseline ゲート非該当。
// 注: color-contrast / link-in-text-block 等の render（CSS）系違反は baseline ゲート下で別途扱う
// ため本テストでは対象外（render-neutral に直せる違反のみを今は機械強制する）。
const A11Y_ROUTES = ['#/', '#/projects', '#/about', '#/contact', '#/resume', '#/apps', '#/settings', '#/quiz', '#/apps/task', '#/apps/todo', '#/apps/pomodoro', '#/apps/ai', '#/hiring-risk', '#/ai-knowhow', '#/role-split', '#/not-found'];
// 本テストで違反ゼロを機械強制する rule の allowlist（= 既に render-neutral に修正済の rule）。
// color-contrast / color-contrast-enhanced / heading-order / link-in-text-block 等の未修正
// （baseline-gated or 別 increment）rule は analyze 結果に含まれても本 allowlist 外ゆえ無視する。
const A11Y_RENDER_NEUTRAL_RULES = ['aria-valid-attr-value', 'select-name', 'button-name', 'label', 'page-has-heading-one', 'heading-order'];
for (const route of A11Y_ROUTES) {
  test(`a11y axe: ${route} has no render-neutral critical violations`, async ({ page }) => {
    await page.goto(`/${route}`);
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(150);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'])
      .analyze();
    const offenders = results.violations.filter(v => A11Y_RENDER_NEUTRAL_RULES.includes(v.id));
    expect(
      offenders,
      `Route ${route} render-neutral a11y violations: ` +
      JSON.stringify(offenders.map(v => `${v.id}(${v.nodes.length}): ${v.nodes[0] && v.nodes[0].html.slice(0, 100)}`))
    ).toHaveLength(0);
  });
}

// ===== 7.1: モバイル viewport + drawer 開 (モーダル) の a11y =====
// 上の A11Y_ROUTES ループは default(desktop) viewport で走る。モバイル (≤MOBILE_BREAKPOINT) は
// sidebar が #drawer (role=dialog/aria-modal) に畳まれる別レンダリング面で、特に drawer 開状態は
// モーダルの a11y (背景隔離・focusable な dialog 内容) が desktop scan ではカバーされない。
// 390px で drawer を開いた状態の render-neutral critical 違反ゼロを機械強制する。
test('a11y axe: mobile viewport with open drawer has no render-neutral critical violations', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'])
    .analyze();
  const offenders = results.violations.filter(v => A11Y_RENDER_NEUTRAL_RULES.includes(v.id));
  expect(
    offenders,
    'mobile+drawer render-neutral a11y violations: ' +
    JSON.stringify(offenders.map(v => `${v.id}(${v.nodes.length})`))
  ).toHaveLength(0);
});

// ===== 7.2: 全ハッシュルート検証 — aria-busy 収束 & コンテンツ非空 =====
// 注: 以前は '#/home'（home は '#/'）と '#/skills'（'skills' route は存在しない）が含まれ、
// どちらも NotFoundPage に解決していた。NotFound も aria-busy=false + #content 非空ゆえ、
// この 2 entry の aria-busy テストは vacuous に NotFound を検査していた（PR #96/#97 の
// app-route-hash と同型の vacuous-hash class）。実在 route のみへ是正し、下の guard で再発を防ぐ。
const HASH_ROUTES = ['#/', '#/projects', '#/about', '#/contact', '#/resume'];

for (const route of HASH_ROUTES) {
  test(`Hash route ${route}: aria-busy resolves to false and #content is non-empty`, async ({ page }) => {
    await page.goto(`/${route}`);
    await page.waitForLoadState('domcontentloaded');

    const content = page.locator('#content');

    await page.waitForFunction(
      () => {
        const el = document.getElementById('content');
        return el && el.getAttribute('aria-busy') === 'false';
      },
      { timeout: 5000 }
    );

    await expect(content).toHaveAttribute('aria-busy', 'false');

    const isEmpty = await page.evaluate(() => {
      const el = document.getElementById('content');
      return el ? el.children.length === 0 : true;
    });
    expect(isEmpty, `#content must not be empty on route ${route}`).toBe(false);

    // Hash-resolution guard (vacuous-hash 再発防止): これらは実在 route のみゆえ、NotFoundPage
    // に落ちてはならない。aria-busy=false + 非空は NotFound でも満たされるため、本 guard が無いと
    // 誤った hash (例: '#/home' / '#/skills') を足しても vacuous に pass してしまう。
    await expect(
      page.getByRole('heading', { name: 'Not Found', exact: true }),
      `Hash route ${route} fell through to NotFoundPage — not a real route`
    ).toHaveCount(0);
  });
}

// ===== 7.2: 5層防衛プロキシ — startViewTransition 上書き確認 =====
test('5-layer proxy: document.startViewTransition is overridden by proxy', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const proxyInstalled = await page.evaluate(() => {
    if (typeof document.startViewTransition !== 'function') {
      return true;
    }
    return document.startViewTransition.name === 'startViewTransitionProxy';
  });

  expect(
    proxyInstalled,
    'document.startViewTransition must be replaced by startViewTransitionProxy'
  ).toBe(true);
});

// ===== 7.2: 5層防衛プロキシ — window.addEventListener 直接上書き禁止確認 =====
test('5-layer proxy: window.addEventListener is not directly overwritten', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const isConsistent = await page.evaluate(() => {
    return !Object.prototype.hasOwnProperty.call(window, 'addEventListener');
  });

  expect(
    isConsistent,
    'window.addEventListener must not be directly overwritten; use EventTarget.prototype instead'
  ).toBe(true);
});

// ===== 7.1: AIOアンカー永続性 — ページ読み込み後も DOM に存在すること =====
test('AIO anchor persists in DOM after initial load', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const count = await page.locator('#aio-asset-anchor').count();
  expect(count, '#aio-asset-anchor must exist in DOM').toBe(1);

  await expect(page.locator('#aio-asset-anchor')).toHaveAttribute('hidden', '');
});

// ===== 7.1: AIOアンカー永続性 — ルート遷移後も保持されること =====
test('AIO anchor persists in DOM after route navigation', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');

  const count = await page.locator('#aio-asset-anchor').count();
  expect(count, '#aio-asset-anchor must persist after route navigation').toBe(1);
  await expect(page.locator('#aio-asset-anchor')).toHaveAttribute('hidden', '');
});

// ===== 7.2: early suppressor — unhandledrejection リスナーの動作確認 =====
test('Early suppressor: unhandledrejection listener suppresses known patterns', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const wasSuppressed = await page.evaluate(() => {
    const err = new Error('message channel closed before a response was received');
    const event = new PromiseRejectionEvent('unhandledrejection', {
      promise: Promise.reject(err),
      reason: err,
      cancelable: true,
    });
    window.dispatchEvent(event);
    return event.defaultPrevented;
  });

  expect(
    wasSuppressed,
    'Early suppressor must call ev.preventDefault() for known extension error patterns'
  ).toBe(true);
});

// ===== 7.1: Trusted Types / CSP 違反なし確認 =====
test('No Trusted Types or CSP violations in console', async ({ page }) => {
  const violations = [];

  page.on('console', msg => {
    const text = msg.text();
    if (
      msg.type() === 'error' &&
      /TrustedType|Trusted Types|require-trusted-types-for|Content Security Policy|CSP/i.test(text)
    ) {
      violations.push({ type: 'console-error', text });
    }
  });

  page.on('pageerror', err => {
    if (/TrustedType|Trusted Types|require-trusted-types-for/i.test(err.message)) {
      violations.push({ type: 'pageerror', text: err.message });
    }
  });

  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  expect(
    violations,
    'Trusted Types / CSP violations found: ' + JSON.stringify(violations)
  ).toHaveLength(0);
});

// ===== v80+ Stage 5-k CI hygiene: all-routes runtime sanity =====
// Stage 5-j で発見された "hidden ReferenceError" (js/pages.js の `h` 未定義参照) は、
// Playwright が当該ルート (/#/hiring-risk, /#/role-split, /#/not-found) を訪問
// していなかったため CI 緑のまま潜在していた。本テスト群は SPA の全 17 ルートを
// 訪問して各ページの runtime 健全性 (console-error / pageerror なし + DOM 出力存在)
// を検証する。これにより同種の bug を将来的に発火前検出可能にする。
//
// 各ルートに対して個別 test() を生成し、失敗しても他ルートは独立に検査される。
// screenshot baseline は引き続き Homepage のみ (他ルートは behavior テストに留め
// baseline の re-take 負荷を避ける)。
const ALL_ROUTES = [
  { hash: '#/',                  name: 'home' },
  { hash: '#/projects',          name: 'projects' },
  { hash: '#/apps',              name: 'apps' },
  { hash: '#/apps/task',         name: 'app-task' },
  { hash: '#/apps/todo',         name: 'app-todo' },
  { hash: '#/apps/pomodoro',     name: 'app-pomodoro' },
  { hash: '#/apps/ai',           name: 'app-ai' },
  { hash: '#/settings',          name: 'settings' },
  { hash: '#/about',             name: 'about' },
  { hash: '#/resume',            name: 'resume' },
  { hash: '#/contact',           name: 'contact' },
  { hash: '#/quiz',              name: 'quiz' },
  { hash: '#/hiring-risk',       name: 'hiring-risk' },
  { hash: '#/ai-knowhow',        name: 'ai-knowhow' },
  { hash: '#/role-split',        name: 'role-split' },
  { hash: '#/not-found',         name: 'not-found-fallback' },
];

for (const route of ALL_ROUTES) {
  test(`Route ${route.name} renders without runtime errors`, async ({ page }) => {
    const consoleErrors = [];
    const pageErrors = [];

    page.on('console', msg => {
      if (msg.type() === 'error') {
        const text = msg.text();
        // Allow benign KARTE/Wicle / suppressor-known patterns and pre-existing
        // inline-style CSP advisories that pre-date Stage 5 (role-split has legacy
        // `style: {...}` chains that Object.assign(el.style, ...) emits as
        // "Applying inline style violates CSP" advisories in some Chromium builds;
        // these are advisories, not blocked execution, and pre-date this PR scope).
        if (/KARTE|Wicle|wicle|Failed to fetch|Trusted Type|Applying inline style violates/i.test(text)) { return; }
        // External-resource load failures (e.g. KARTE CDN flaking in CI) surface as
        // "Failed to load resource: net::ERR_FAILED" — note Chromium puts the FAILED URL in
        // msg.location().url, NOT in msg.text(), so the host-name filter above cannot see it.
        // Ignore such network errors only when the failing URL is a *non-self* origin: a failed
        // OWN module/asset would instead throw a pageerror AND leave #content empty (both asserted
        // below), so this never masks a real same-origin regression — it only de-flakes third-party
        // CDN failures that are outside our code's control.
        const _loc = (typeof msg.location === 'function') ? msg.location() : null;
        const _url = (_loc && _loc.url) || '';
        if (/Failed to load resource|net::ERR_/i.test(text) && _url && !/^https?:\/\/(localhost|127\.0\.0\.1)/i.test(_url)) { return; }
        consoleErrors.push(text);
      }
    });
    page.on('pageerror', err => pageErrors.push(err.message));

    await page.goto('/' + route.hash);
    await page.waitForLoadState('domcontentloaded');
    // Wait an extra tick to let the SPA finish its render cycle
    await page.waitForTimeout(200);

    // SPA must have rendered content
    const contentLocator = page.locator('#content');
    await expect(contentLocator).toHaveCount(1);
    const contentText = await contentLocator.textContent();
    expect(contentText, `Route ${route.name} content div is empty — likely render threw`).not.toBe('');

    // No console errors (other than benign third-party patterns)
    expect(
      consoleErrors,
      `Route ${route.name} console errors: ` + JSON.stringify(consoleErrors)
    ).toHaveLength(0);

    // No uncaught page errors (ReferenceError / TypeError 等)
    expect(
      pageErrors,
      `Route ${route.name} page errors: ` + JSON.stringify(pageErrors)
    ).toHaveLength(0);

    // No CAUGHT render crash (ErrorBoundary → FatalPage). main.js stores the thrown
    // error on window.__fatalError before rendering FatalPage. A route that crashes into
    // FatalPage would otherwise PASS the three checks above — #content is non-empty (it
    // holds the fatal UI) and the error was caught (so no console/page error). This is
    // exactly how the SettingsPage Storage-injection bug hid undetected. Asserting
    // window.__fatalError is falsy closes that detection gap for every shipped route.
    const fatal = await page.evaluate(() => {
      const e = window.__fatalError;
      return e ? (e.message || String(e)) : null;
    });
    expect(fatal, `Route ${route.name} fell into the ErrorBoundary FatalPage: ${fatal}`).toBeNull();

    // Hash-resolution guard: every route EXCEPT the intentional not-found fallback must
    // resolve to its real page, never silently fall through to NotFoundPage (h1 "Not Found").
    // This catches the "wrong hash → NotFound" vacuous-coverage class — e.g. ALL_ROUTES once
    // listed #/app-task instead of #/apps/task, so 4 app route tests vacuously asserted the
    // NotFound page (non-empty + no error) and passed. Check 58 only compares route NAMES,
    // not that each hash resolves, so this behavioral guard closes that gap.
    if (route.name !== 'not-found-fallback') {
      await expect(
        page.getByRole('heading', { name: 'Not Found', exact: true }),
        `Route ${route.name} (${route.hash}) fell through to NotFoundPage — its hash does not resolve to the intended route`
      ).toHaveCount(0);
    }
  });
}

// ===== v80+ Stage 5-k CI hygiene: project-detail route requires slug =====
test('Route project-detail renders for a known slug without errors', async ({ page }) => {
  const consoleErrors = [];
  const pageErrors = [];

  page.on('console', msg => {
    if (msg.type() === 'error') {
      const text = msg.text();
      if (/KARTE|Wicle|wicle|Failed to fetch|Trusted Type|Applying inline style violates/i.test(text)) { return; }
      consoleErrors.push(text);
    }
  });
  page.on('pageerror', err => pageErrors.push(err.message));

  // p01 = task-manager (Store の defaultProjects 先頭)。
  // 注: route は複数形 '#/projects/<slug>' で project-detail に解決する。以前は単数 '#/project/...'
  // を使っており NotFoundPage に落ちて vacuous に NotFound を検査していた（PR #96-#98 と同型の
  // vacuous-hash class）。複数形へ是正し、実プロジェクト描画を直接アサートする。
  await page.goto('/#/projects/task-manager');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(200);

  const contentLocator = page.locator('#content');
  const contentText = await contentLocator.textContent();
  expect(contentText, 'project-detail content empty').not.toBe('');
  expect(consoleErrors).toHaveLength(0);
  expect(pageErrors).toHaveLength(0);

  // NotFound fall-through ではなく実 ProjectDetailPage が描画されていること
  await expect(page.getByRole('heading', { name: 'Not Found', exact: true })).toHaveCount(0);
  await expect(page.getByText('タスク管理アプリ')).toBeVisible();
});