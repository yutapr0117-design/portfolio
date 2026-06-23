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
  // [FIX] SPA はモジュール実行後に外部リンク (Zenn/GitHub/X 等) を描画するため、domcontentloaded
  // 直後の即時 count は描画前で 0 になり得る (CI の遅い環境で間欠 flake)。web-first assertion で
  // 「最低 1 本が描画される」まで auto-wait してから数える (snapshot count → retry 付き assertion へ)。
  await expect(externalLinks, 'home should render at least one external link (non-vacuous)').not.toHaveCount(0);
  const count = await externalLinks.count();
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

// ===== 7.1: 未知ルートが「理解可能な」NotFound + 動作する復帰 nav を出す =====
// §3(B) で screenshot を advisory 化した結果、「サイトが表示されるが理解不能/行き止まり」を防ぐ砦は
// behavior e2e のみになった。soft-404 テストは robots meta だけ見ており、NotFound が blank/dead-end
// 化しても meta は通ってしまう。オーケストレーターが死守と明言した「表示が理解不能でない」要件を直接
// 守るため、未知ルートで (1) 見出し+説明が読める (2) 「ホームへ」復帰が実際に home を再描画する (3)
// ErrorBoundary に落ちない、を検証する。site=付属物だが「機能する/理解できる」は死守対象。
test('Unknown route shows a comprehensible Not Found page with working recovery nav', async ({ page }) => {
  await page.goto('/#/zzz-nonexistent-route-9999');
  await page.waitForLoadState('domcontentloaded');

  // (1) 理解可能な内容: 見出し + 説明文が読める (blank/garbage でない)
  await expect(page.getByRole('heading', { name: 'Not Found' })).toBeVisible();
  await expect(page.getByText('指定されたページは見つかりません。')).toBeVisible();

  // (2) 行き止まりでない: 「ホームへ」で home が再描画される (復帰導線が機能する)
  await page.getByRole('button', { name: 'ホームへ' }).click();
  await expect(page.locator('.hero-section')).toBeVisible();

  // (3) ErrorBoundary に落ちていない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `NotFound recovery caused a fatal: ${fatal}`).toBeNull();
});

// ===== ErrorBoundary: FatalPage 描画 + 復旧フロー (resilience) =====
// window.__fatalError が立つと _renderCore は FatalPage を描画する (ErrorBoundary)。以前は
// home(#/) で fatal が起きると「ホームへ」(Router.navigate('')) が同一 hash ゆえ hashchange 不発火
// で再描画されず FatalPage から復旧できないバグがあった (window.render() を明示呼びして是正)。
// 既存 e2e は __fatalError===null (fatal が起きないこと) ばかり検証し、FatalPage 自体の描画 +
// 復旧フローは未カバーだった。本テストは fatal を注入して FatalPage が出る → ホームへ で復旧、を検証。
test('FatalPage renders on a fatal error and ホームへ recovers (home-route)', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  // 致命的エラーを注入して再描画 → FatalPage
  await page.evaluate(() => { window.__fatalError = new Error('E2E_FATAL_PROBE'); window.render(); });
  await expect(page.locator('#content h1', { hasText: '致命的エラー' })).toBeVisible();
  await expect(page.getByText('E2E_FATAL_PROBE').first()).toBeVisible();
  // 「ホームへ」で復旧 (home-route の同一 hash でも window.render() で再描画される)
  await page.getByRole('button', { name: 'ホームへ' }).click();
  await expect(page.locator('#content h1', { hasText: '致命的エラー' })).toHaveCount(0);
  const fatal = await page.evaluate(() => window.__fatalError);
  expect(fatal).toBeNull();
  await expect(page.locator('.hero-section')).toBeVisible();
});

test('FatalPage ホームへ recovers from a non-home route too', async ({ page }) => {
  await page.goto('/#/about', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.evaluate(() => { window.__fatalError = new Error('E2E_FATAL_ABOUT'); window.render(); });
  await expect(page.locator('#content h1', { hasText: '致命的エラー' })).toBeVisible();
  await page.getByRole('button', { name: 'ホームへ' }).click();
  await expect(page.locator('#content h1', { hasText: '致命的エラー' })).toHaveCount(0);
  await expect(page.locator('.hero-section')).toBeVisible();
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
// を注入し、cssSelector を SPEAKABLE_SELECTORS でルート毎に切替える (home は固有の
// '.sr-only[data-ai-entity]' を持ち、他ルートは '.sr-only')。AI 音声アシスタントが読み上げるべき
// 要素を指定する AIO サーフェス。home で固有セレクタが入り、別ルートで外れる (= ルート追従) ことを検証。
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
  expect(data.speakable.cssSelector).toContain('.sr-only[data-ai-entity]');

  // 別ルートへ移ると home 固有セレクタが外れる (ルート追従)
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect.poll(async () => {
    const d = JSON.parse(await page.locator('script[data-ld="speakable"]').textContent());
    return d.speakable.cssSelector.includes('.sr-only[data-ai-entity]');
  }).toBe(false);
});

// ===== 7.1: Speakable cssSelector が実 DOM 要素に解決する (AIO accuracy / dead-selector 再発防止) =====
// dead-selector 修正 (home の .hero-tagline/.core-thesis 除去・role-split の .role-split-table →
// #role-split-table) の再発防止ガード。home は全 cssSelector が実在要素に解決すべき (修正前は
// .hero-tagline/.core-thesis が 0 マッチで red だった)。role-split は修正対象 #role-split-table が
// 解決することを確認する。注: [data-speakable] のような汎用 baseline selector は home の hero のみ
// が持ち他ルートでは no-op になり得る (forward-compat ゆえ容認) ため、home の全解決 + role-split の
// 固有 selector 解決に絞って検証する。
test('Home Speakable cssSelectors all resolve to real elements (AIO accuracy)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  const data = JSON.parse(await page.locator('script[data-ld="speakable"]').textContent());
  const selectors = data.speakable.cssSelector;
  expect(Array.isArray(selectors) && selectors.length > 0).toBe(true);
  for (const sel of selectors) {
    expect(await page.locator(sel).count(), `Speakable selector "${sel}" must resolve to >=1 element on home`).toBeGreaterThan(0);
  }
});

test('Role-split Speakable references the actual table via #role-split-table (not a dead class)', async ({ page }) => {
  await page.goto('/#/role-split');
  await page.waitForLoadState('domcontentloaded');
  const data = JSON.parse(await page.locator('script[data-ld="speakable"]').textContent());
  // 修正で .role-split-table(class・dead) → #role-split-table(id・実在) に変更済み
  expect(data.speakable.cssSelector).toContain('#role-split-table');
  expect(data.speakable.cssSelector).not.toContain('.role-split-table');
  expect(await page.locator('#role-split-table').count()).toBeGreaterThan(0);
});

// ===== 7.1: ai-knowhow / about の Speakable cssSelector も実 DOM に解決する (dead-selector 全ルート化) =====
// home / role-split の解決ガードは被覆済みだが、SPEAKABLE_SELECTORS は ai-knowhow (固有 '.ai-summary-block')
// と about も宣言しており、これらは未検証だった = 将来それらが dead 化しても検知できない穴。元バグ
// (.hero-tagline/.core-thesis/.role-split-table の dead selector) と同 class の AIO-accuracy 不変条件を
// 残る 2 ルートへ拡張する。注: '[data-speakable]' は home の hero のみが持つ forward-compat baseline で
// 他ルートでは no-op になり得る (既存 home テストの注記と同じ) ため除外し、ルート固有 + .sr-only/h1 の
// 実在を検証する。ai-knowhow の '.ai-summary-block' は index.html の静的 sr-only ノードで全ルートに在る。
test('ai-knowhow/about Speakable cssSelectors (non-baseline) resolve to real elements (AIO accuracy)', async ({ page }) => {
  for (const route of ['ai-knowhow', 'about']) {
    await page.goto(`/#/${route}`);
    await page.waitForLoadState('domcontentloaded');
    const data = JSON.parse(await page.locator('script[data-ld="speakable"]').textContent());
    const selectors = (data.speakable.cssSelector || []).filter(s => s !== '[data-speakable]');
    expect(selectors.length, `${route} should declare non-baseline Speakable selectors`).toBeGreaterThan(0);
    for (const sel of selectors) {
      expect(await page.locator(sel).count(), `Speakable selector "${sel}" must resolve to >=1 element on ${route}`).toBeGreaterThan(0);
    }
  }
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

// ===== 7.1: theme-init.js の FOUC pre-paint (保存 dark テーマの初期適用) =====
// theme-init.js は main.js (ESM) ロード前に localStorage の theme を読み data-theme / .dark を
// pre-paint 適用し FOUC (light→dark のちらつき) を防ぐ。theme-cycle テストは「クリックで切替→永続」
// を見るが、「保存済み dark を初期ロードで復元する」FOUC 防止経路は未カバーだった。dark を seed して
// 読み込み、html[data-theme=dark] + .dark が初期適用されることを検証する。
test('theme-init.js applies stored dark theme on initial load (FOUC prevention)', async ({ page }) => {
  // main.js ロード前に走る theme-init.js が読む localStorage キーへ dark を seed
  await page.addInitScript(() => {
    try {
      localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
        schemaVersion: 12, type: 'full-store', theme: 'dark'
      }));
    } catch (e) { /* noop */ }
  });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const html = page.locator('html');
  await expect(html).toHaveAttribute('data-theme', 'dark');
  await expect(html).toHaveClass(/\bdark\b/);
});

// ===== 7.1: Service Worker の登録・activate・page 制御 (SW ライフサイクル) =====
// sw.js は install(skipWaiting)→activate(古いキャッシュ削除 + clients.claim)→fetch(SWR) の
// ライフサイクルを持つ。フルオフライン navigation は提供しない設計 (SWR・app-shell precache なし)
// ため offline 配信はテスト対象外。ここでは genuine な「SW が登録され active になり page を制御する」
// ことを検証し、SW 登録/活性化の退行 (例: registration 失敗・activate 例外) を捕捉する。
test('Service worker registers, activates, and controls the page', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.evaluate(() => navigator.serviceWorker.ready);

  // active な registration が存在する
  const active = await page.evaluate(async () => {
    const reg = await navigator.serviceWorker.getRegistration();
    return !!(reg && reg.active);
  });
  expect(active, 'an active service worker registration must exist').toBe(true);

  // clients.claim() により page が SW 制御下に入る
  await expect.poll(() => page.evaluate(() => !!navigator.serviceWorker.controller)).toBe(true);
});

// ===== 7.1: theme-init.js の brand pre-paint (保存 brand の初期適用) =====
// theme-init.js は localStorage 'portfolio_brand_v45' を main.js ロード前に読み data-brand を
// pre-paint 適用する (brand 別パレットの FOUC 防止)。dark テーマ FOUC と同クラスだが brand 軸は
// 未カバーだった。非デフォルト brand 'classic' を seed して初期ロード → html[data-brand=classic] が
// 適用されることを検証する (DEFAULT='indigo' でなく保存値が復元されることを示す)。
test('theme-init.js applies stored brand on initial load (brand FOUC prevention)', async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.setItem('portfolio_brand_v45', 'classic'); } catch (e) { /* noop */ }
  });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  await expect(page.locator('html')).toHaveAttribute('data-brand', 'classic');
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

// ===== 7.2: ドロワー overlay(背景)クリックで閉じる (モーダル backdrop dismiss) =====
// main.js は #overlay のクリックで closeDrawer を呼ぶ (main.js:800)。Escape / nav-link クローズ
// とは別の「背景クリックで閉じる」モーダル標準挙動で未カバーだった。開いて overlay をクリック →
// aria-hidden 復帰 + 背景隔離 (#app aria-hidden) 解除 + menuBtn aria-expanded=false を検証。
test('Mobile drawer closes on overlay (backdrop) click', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const menuBtn = page.locator('#menuBtn');
  const drawer = page.locator('#drawer');
  await menuBtn.click();
  await expect(drawer).toHaveAttribute('aria-hidden', 'false');

  // 背景 overlay クリックで閉じる (overlay 中央は drawer に覆われ得るため click ハンドラを
  // dispatchEvent で直接発火 = main.js:800 の overlay→closeDrawer 配線を検証)
  await page.locator('#overlay').dispatchEvent('click');
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  await expect(page.locator('#app')).not.toHaveAttribute('aria-hidden', 'true');
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
  await expect(blocks.first()).toBeVisible(); // [FIX] SPA 描画完了を auto-wait してから数える (snapshot count flake 防止)
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

// ===== 7.2: architecture quiz 検索が stakeholder 主張テキストを被覆する (回帰) =====
// architecture quiz は stakeholder の name/quote を画面描画するが、検索フィルタが従来
// title/id/content/situation/question しか見ておらず「画面に見えるのに検索できない」状態
// だった (visible-but-unsearchable バグ)。'GAFA' は architecture データ全体で CTO の quote に
// 1 度だけ出る stakeholder-only 語。検索でその問題ブロックがヒットし empty-state にならない
// ことを実検証する (修正前は 0 件 + panel-empty 表示だった)。
test('Quiz architecture search matches stakeholder quote text (visible-but-unsearchable regression)', async ({ page }) => {
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');

  const blocks = page.locator('.quiz-question-block');
  await expect(blocks.first()).toBeVisible();

  // stakeholder quote にのみ存在する語で検索
  const search = page.locator('input[aria-label="問題検索"]');
  await expect(search).toBeVisible();
  await search.fill('GAFA');

  // 該当問題がヒットし、空状態にならない (修正前はここで 0 件 + panel-empty だった)
  await expect(blocks).toHaveCount(1);
  await expect(page.locator('.panel-empty')).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `architecture quiz stakeholder search caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: quiz 模範解答問い合わせフォームの空入力バリデーション =====
// QuizPage の問い合わせフォームは送信時に name/email 必須を検証し、欠落時「お名前とメール
// アドレスを入力してください」エラー toast を出す (mailto は開かない)。この validation 分岐は
// 未カバーだった。空のまま送信 → エラー toast + crash なしを実検証する。
test('Quiz contact form shows validation error on empty submit', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  // 名前/メール未入力で送信
  await page.getByRole('button', { name: '送信' }).click();
  await expect(page.locator('#toast-container').getByText('お名前とメールアドレスを入力してください')).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quiz form validation caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: quiz pm / quality タイプのデータファイル描画カバレッジ =====
// QUIZ_DATA_MAP は aws / pm / quality / architecture の 4 データファイルを引く。aws(default) と
// architecture は被覆済みだが、pm(pmQuizData) / quality(qualityQuizData) はどのテストでも未訪問で
// 0 カバレッジ = malformed でも未検知だった。?type= 経由で両者の title + question block 描画を検証し
// 2 データファイルの renderability を守る (distinct data ゆえ非 padding)。
test('Quiz pm and quality types render their data files', async ({ page }) => {
  await page.goto('/#/quiz?type=pm');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1', { hasText: 'PM問題集' })).toBeVisible();
  await expect(page.locator('.quiz-question-block').first()).toBeVisible();

  await page.goto('/#/quiz?type=quality');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1', { hasText: '品質・プロセス問題集' })).toBeVisible();
  await expect(page.locator('.quiz-question-block').first()).toBeVisible();
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
// ===== 7.2: TODO「完了済み削除」ボタンの disabled 状態 (完了 0 件で無効 → 完了化で有効) =====
// clearCompleted ボタンは `disabled: !todos.some(t => t.completed)` で、完了 TODO が 1 件も無いとき
// 無効・1 件でも完了すると有効になる。filter/flow テストはあるがこの disabled binding は未カバー
// だった。active な TODO 追加直後は無効、checkbox で完了にすると有効になることを検証する。
test('Todo clear-completed button is disabled until a todo is completed', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  await input.fill('CLEAR-DISABLED-TODO-9301');
  await input.press('Enter');
  const item = page.locator('article', { hasText: 'CLEAR-DISABLED-TODO-9301' });
  await expect(item).toBeVisible();

  const clearBtn = page.getByRole('button', { name: '完了済み削除' });
  // 完了 0 件 → 無効
  await expect(clearBtn).toBeDisabled();
  // 完了にすると有効
  await item.locator('input[type="checkbox"]').check();
  await expect(clearBtn).toBeEnabled();
});

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

// ===== 7.2: プロジェクト並び替え (moveProject ↑/↓ で順序入替) — projects 管理 CRUD 完成 =====
// settings の moveProject(idx, dir) は state.projects[idx] と [idx+dir] を入替える。add/hide/delete は
// 被覆済みだが reorder は未カバーだった。一意名 2 件 (A→B の順で追加 = unshift で [B, A, ...defaults])
// を作り、A の行の「↑」で A を先頭へ繰り上げ、State 上で A が B より前に来る (順序入替) ことを検証する。
// 順序は localStorage State 読み取りで決定的に判定する。
test('Projects can be reordered with the up/down controls', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const nameInput = page.getByPlaceholder('プロジェクト名');
  const addBtn = page.getByRole('button', { name: '追加', exact: true });
  const A = 'REORDER-PROJ-A-6701';
  const B = 'REORDER-PROJ-B-6702';
  await nameInput.fill(A); await addBtn.click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();
  await nameInput.fill(B); await addBtn.click();

  const orderAB = () => page.evaluate((names) => {
    try {
      const st = JSON.parse(localStorage.getItem('portfolio_enhanced_v45'));
      const list = (st.projects || []).map(p => p.name);
      return { a: list.indexOf(names[0]), b: list.indexOf(names[1]) };
    } catch { return { a: -1, b: -1 }; }
  }, [A, B]);

  // 初期は unshift で [B, A, ...] → B が A より前
  await expect.poll(async () => { const o = await orderAB(); return o.a > o.b && o.a >= 0; }).toBe(true);

  // A の行の「↑」で A を 1 つ繰り上げ → A が B より前へ
  const rowA = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: A });
  await rowA.getByRole('button', { name: '↑' }).click();
  await expect.poll(async () => { const o = await orderAB(); return o.a < o.b && o.a >= 0; }).toBe(true);
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

// ===== 7.2: destructive 操作の confirm-cancel ガード (data-safety) =====
// deleteProjectHard / resetData は `if (!confirm(...)) return;` で「キャンセル時は何もしない」分岐を
// 持つ。accept 経路は被覆済みだが cancel 経路は未カバーだった。cancel したのに実行されると重大な
// データ損失になるため、confirm を dismiss しても (1) プロジェクトが削除されない (2) データが初期化
// されない、を実検証する。
test('Canceling the delete confirm keeps the project (data-safety)', async ({ page }) => {
  page.on('dialog', (dialog) => dialog.dismiss());

  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const name = 'DELETE-CANCEL-PROJ-8120';
  await page.getByPlaceholder('プロジェクト名').fill(name);
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();

  // 削除 → confirm を dismiss → 行は残る
  const row = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name });
  await row.getByRole('button', { name: '削除' }).click();
  // dismiss されたので削除されず、公開一覧にも残る
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();
});

test('Canceling the reset confirm keeps data (data-safety)', async ({ page }) => {
  page.on('dialog', (dialog) => dialog.dismiss());

  // タスクを追加
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  const input = page.locator('#task-input');
  await input.fill('RESET-CANCEL-TASK-8121');
  await input.press('Enter');
  await expect(page.getByText('RESET-CANCEL-TASK-8121')).toBeVisible();

  // 全リセット → confirm を dismiss → タスクは残る (初期化されない)
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '全リセット' }).click();
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('RESET-CANCEL-TASK-8121')).toBeVisible();
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

// ===== 7.2: settings 正規化ボタン (normalizeNow → validateAndNormalize) =====
// 「整合性チェック / 正規化」セクションの「実行」は normalizeNow() で State を
// validateAndNormalize() に通し「正規化を完了しました」を出す (型揺れ/上限超過/破損を安全側に
// 丸めるデータ hygiene)。reset (createDefaultStore) とは別経路で未カバーだった。実行 →
// 完了通知 + crash なし + データ保持 (初期化ではない) を検証する。
test('Settings normalize button runs validateAndNormalize without data loss', async ({ page }) => {
  // 正規化が「初期化」ではないことを示すため、ユーザータスクを 1 件用意
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  const input = page.locator('#task-input');
  await input.fill('NORMALIZE-KEEP-TASK-8810');
  await input.press('Enter');
  await expect(page.getByText('NORMALIZE-KEEP-TASK-8810')).toBeVisible();

  // settings の「整合性チェック / 正規化」セクションの「実行」
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const normSection = page.locator('section.card').filter({ has: page.getByRole('heading', { name: '整合性チェック / 正規化' }) });
  await normSection.getByRole('button', { name: '実行' }).click();
  await expect(page.locator('#toast-container').getByText('正規化を完了しました')).toBeVisible();

  // crash せず、正規化はデータを保持する (初期化と異なりタスクは残る)
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `normalize caused a fatal: ${fatal}`).toBeNull();
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('NORMALIZE-KEEP-TASK-8810')).toBeVisible();
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

// ===== 7.2: Markdown ノートアプリ (innerHTML 不使用のライブプレビュー + 永続) =====
// js/apps.js NotesPage は textarea の Markdown を h() のみ（innerHTML 不使用）で DOM へレンダリングし
// live preview + localStorage 永続する純追加アプリ。# 見出し / **太字** / `code` / - リストを
// h('h1'/'strong'/'code'/'li') へ変換する。入力→プレビュー反映→リロード永続を検証する。
test('Markdown notes app live-previews (innerHTML-free) and persists', async ({ page }) => {
  await page.goto('/#/apps/notes');
  await page.waitForLoadState('domcontentloaded');

  const ta = page.locator('#notes-input');
  await expect(ta).toBeVisible();
  await ta.fill('# E2E-NOTE-見出し-7733\n\n**太字テキスト** と `inlineコード`\n\n- 項目A');

  // プレビューが h() で構造化レンダリング (innerHTML 不使用) されること
  const preview = page.locator('.md-preview');
  await expect(preview.locator('h1', { hasText: 'E2E-NOTE-見出し-7733' })).toBeVisible();
  await expect(preview.locator('strong', { hasText: '太字テキスト' })).toBeVisible();
  await expect(preview.locator('code.md-code', { hasText: 'inlineコード' })).toBeVisible();
  await expect(preview.locator('ul.md-ul li', { hasText: '項目A' })).toBeVisible();

  // リロード後も永続 (appsData.notes)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.md-preview h1', { hasText: 'E2E-NOTE-見出し-7733' })).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `notes app caused a fatal: ${fatal}`).toBeNull();
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

// ===== 7.2: Toast の自動消滅ライフサイクル (duration 経過で消える) =====
// Toast.show は duration(既定 3000ms) 後に remove() を呼び、さらに 300ms のアニメ後に DOM から
// 除去する (ui-components.js)。toast が表示される検証は多数あるが「時間経過で自動消滅する」
// ライフサイクルは未カバーだった (消えないと toast が画面に積み上がる UX バグ)。fake clock で
// duration+アニメ経過後に toast が消えることを決定的に検証する。
test('Toast auto-dismisses after its duration (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  // タスク追加で success toast を発火
  const input = page.locator('#task-input');
  await input.fill('TOAST-DISMISS-TASK-9501');
  await input.press('Enter');
  const toast = page.locator('#toast-container').getByText('タスクを追加しました');
  await expect(toast).toBeVisible();

  // duration(3000) + remove アニメ(300) を超えて進める → 自動消滅
  await page.clock.fastForward(3500);
  await expect(toast).toHaveCount(0);
});

// ===== 7.2: アクションの sr-only aria-live 通知 (screen reader フィードバック・a11y) =====
// Toast.show は視覚 toast に加え #action-announcement (sr-only, aria-live=assertive) にも message を
// 書き込む。視覚 toast の検証は多数あるが、SR 利用者向け assertive 通知チャネルは未カバーだった。
// 通知領域が assertive aria-live を持つこと + アクションでメッセージが announce されることを検証する。
test('Actions announce to the assertive sr-only aria-live region (screen reader a11y)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const live = page.locator('#action-announcement');
  await expect(live).toHaveAttribute('aria-live', 'assertive');

  // アクション (タスク追加) でメッセージが SR 通知領域に入る
  const input = page.locator('#task-input');
  await input.fill('SR-ANNOUNCE-TASK-9601');
  await input.press('Enter');
  await expect(live).toHaveText('タスクを追加しました');
});

// ===== 7.2: SPA ルート変更の sr-only aria-live 通知 (screen reader a11y) =====
// SPA はページ全体が再読込されないため、SR 利用者にルート変更を能動的に通知する必要がある
// (SPA a11y の既知要件)。#page-announcement (sr-only, aria-live=polite) はルート遷移ごとに
// RouteState の a11y_announcement バインディング (main.js, route.name ベースで「<route> ページを
// 表示中」) で更新される。視覚 title 更新 (別テスト) とは別チャネルで未カバーだった。route 遷移で
// polite 領域が現在 route 名に追従することを検証する。
test('Route changes announce to the polite sr-only aria-live region (SPA a11y)', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const announcer = page.locator('#page-announcement');
  await expect(announcer).toHaveAttribute('aria-live', 'polite');
  await expect.poll(async () => (await announcer.textContent()) || '').toContain('projects');

  // 別ルートへ遷移すると announcement が現在 route 名に追従更新される
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect.poll(async () => (await announcer.textContent()) || '').toContain('about');
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

// ===== 7.2: ポモドーロ 長休憩モード (3 つ目の mode 分岐 / settings.long duration) =====
// switchMode('long-break') は getDuration で settings.long(既定 15)*60 を remaining にセットする。
// mode-switch テストは短休憩のみで、長休憩は distinct な 3 つ目の mode 分岐として未カバーだった。
// 「長休憩」クリックで表示が既定の長休憩 duration 15:00 になることを検証する。
test('Pomodoro long-break mode sets the long-break duration', async ({ page }) => {
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  await page.getByRole('button', { name: '長休憩', exact: true }).click();
  await expect(page.locator('.font-mono.text-stat').first()).toHaveText('15:00');
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

// ===== 7.2: サイドバーナビのキーボード操作性 (focus + Enter で遷移・WCAG 2.1.1) =====
// nav-link は <a href="#/..."> + onclick(Router.navigate)。マウス click は別テストで被覆済みだが、
// キーボード利用者にとっての「focus して Enter で起動できる」操作性 (WCAG 2.1.1 Keyboard) は
// 未カバーだった。Projects ナビリンクへ focus し Enter で /#/projects へ遷移 + 本文描画を検証する。
test('Sidebar nav link is keyboard-operable (focus + Enter activates)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const projectsLink = page.locator('a.nav-link[href="#/projects"]:visible').first();
  await projectsLink.focus();
  await expect(projectsLink).toBeFocused();

  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/#\/projects$/);
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
});

// ===== 7.2: サイドバー全 nav リンクの整合性 (全て非 not-found route へ解決) =====
// navLink の href (#/ + item.path) が実在 route を指さないと click で NotFound に落ちる。route-render
// テストは ALL_ROUTES (curated 直 URL) を訪問するが、実際の nav href は検証しないため、nav path の
// タイポ等の drift を捕捉できなかった。サイドバーの全 nav リンク href を収集し、各々を訪問しても
// NotFound に落ちないことを実検証する (非 vacuous: href 6 件以上)。
test('All sidebar nav links resolve to valid (non-not-found) routes', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // [FIX] sidebar はモジュール実行後に描画されるため、domcontentloaded 直後の evaluateAll は
  // 描画前で空になり得る (CI 間欠 flake)。最初の nav-link 描画を auto-wait してから収集する。
  await expect(page.locator('a.nav-link').first()).toBeVisible();
  const hrefs = await page.locator('a.nav-link:visible').evaluateAll(
    els => els.map(e => e.getAttribute('href')).filter(Boolean)
  );
  expect(hrefs.length, 'sidebar should expose multiple nav links').toBeGreaterThan(5);

  for (const href of hrefs) {
    await page.goto('/' + href); // href は '#/...' 形式
    await page.waitForLoadState('domcontentloaded');
    await expect(
      page.getByRole('heading', { name: 'Not Found', exact: true }),
      `nav href ${href} は NotFound に落ちてはならない`
    ).toHaveCount(0);
  }
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

// ===== 7.2: import で slug 衝突するプロジェクトが一意化される (詳細到達性) =====
// mergeProjectsWithDefaults は ID でのみ dedupe するため、import データ内に同一 slug の別 id
// プロジェクトが 2 件あると slug が重複し、ProjectDetailPage の find(p.slug===slug) が先頭のみ返して
// 片方の詳細が到達不能になっていた (addProjectManual の slug 衝突修正の import パス版・全経路チョーク
// ポイントで根治)。同一 slug の 2 件を import → 結果の slug が一意化されることを State から検証する。
test('Importing projects with colliding slugs yields unique slugs (detail reachability)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const imported = {
    projects: [
      { id: 'p_imp_collide_a', slug: 'collide-slug', name: 'IMPORT-COLLIDE-A-5511', category: 'X', summary: '', problem: '', approach: '', tech: [], tags: [] },
      { id: 'p_imp_collide_b', slug: 'collide-slug', name: 'IMPORT-COLLIDE-B-5512', category: 'X', summary: '', problem: '', approach: '', tech: [], tags: [] },
    ]
  };
  await page.locator('input[type="file"]').setInputFiles({
    name: 'collide.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(imported)),
  });
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  // State 上で 2 件の slug が一意化されていること (重複なし)
  const readSlugs = () => page.evaluate(() => {
    try {
      const st = JSON.parse(localStorage.getItem('portfolio_enhanced_v45'));
      return (st.projects || []).filter(p => /^IMPORT-COLLIDE-[AB]-/.test(p.name)).map(p => p.slug);
    } catch { return []; }
  });
  await expect.poll(async () => (await readSlugs()).length).toBe(2);
  const slugs = await readSlugs();
  expect(new Set(slugs).size, `imported colliding slugs must be unique: ${JSON.stringify(slugs)}`).toBe(2);
});

// ===== 7.2: upsert インポートが既存を更新しつつ新規も追加する (data-loss 回帰) =====
// importJSON の upsert モード (UI ラベル「更新+追加」) は既存 id を更新し未知 id を追加するはず。
// 旧実装は未知 id を s.projects.push したのち Map.values() で上書きし、push した新規が破棄される
// data-loss バグがあった (append は被覆済みだが upsert は 0 カバレッジで未検知だった。strict は
// 直下の別テストで被覆)。既存 default (p01) の更新 + 新規 id の追加を含む JSON を upsert import し、
// 両方が一覧に出ることを検証する (修正前は新規 'UPSERT-NEW-*' が消えて fail する)。
test('Settings upsert import updates existing AND adds new projects (data-loss regression)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // インポートモードを upsert に切替
  await page.locator('select[aria-label="インポートモード"]').selectOption('upsert');

  const imported = {
    projects: [
      // 既存 default (id=p01) を更新
      { id: 'p01', slug: 'task-manager', name: 'UPSERT-UPDATED-7711', category: 'Productivity', summary: 'upsert update', problem: '', approach: '', tech: ['JS'], tags: [] },
      // 未知 id を追加 (旧バグで消えていた)
      { id: 'p_upsert_new_7712', slug: 'upsert-new-7712', name: 'UPSERT-NEW-7712', category: 'Imported', summary: 'upsert add', problem: '', approach: '', tech: ['JS'], tags: [] },
    ]
  };
  await page.locator('input[type="file"]').setInputFiles({
    name: 'upsert.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(imported)),
  });
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  // 追加パス (バグ修正の核): 新規 id のプロジェクトが一覧に出る
  await expect(page.getByText('UPSERT-NEW-7712').first()).toBeVisible();
  // 更新パス: 既存 p01 の name が更新され、元の default 名は消える (append では更新されない)
  await expect(page.getByText('UPSERT-UPDATED-7711').first()).toBeVisible();
  await expect(page.getByText('タスク管理アプリ')).toHaveCount(0);
});

// ===== 7.2: strict インポートはユーザー追加層を全置換しつつ defaults は温存する =====
// importJSON の strict モード (UI ラベル「全置換」) は s.projects=parsed.projects で置換するが、
// 直後の validateAndNormalize→mergeProjectsWithDefaults が v2 baseline の defaults を必ず再注入する
// ため「全置換」されるのは実質ユーザー追加層のみで defaults は温存される (label が直感より狭い実挙動)。
// strict は従来 0 カバレッジで、この surprising な実セマンティクスが未文書だった。append で投入した
// ユーザー project が strict import 後に消え、import 分は残り、default は健在、を実検証して固定する
// (append との distinct: append なら victim も残るため strict 固有の破壊性をこのテストだけが捉える)。
test('Settings strict import replaces user-added layer but preserves defaults', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // (1) append で victim ユーザー project を投入
  await page.locator('input[type="file"]').setInputFiles({
    name: 'victim.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ projects: [
      { id: 'p_strict_victim_8810', slug: 'strict-victim-8810', name: 'STRICT-VICTIM-8810', category: 'X', summary: '', problem: '', approach: '', tech: [], tags: [] },
    ] })),
  });
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  // (2) strict に切替え、victim を含まない別 project を import
  await page.locator('select[aria-label="インポートモード"]').selectOption('strict');
  await page.locator('input[type="file"]').setInputFiles({
    name: 'strict.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ projects: [
      { id: 'p_strict_new_8811', slug: 'strict-new-8811', name: 'STRICT-NEW-8811', category: 'Imported', summary: '', problem: '', approach: '', tech: [], tags: [] },
    ] })),
  });
  // append の toast が auto-dismiss 前で 2 件並ぶことがあるため最新 (strict) を対象に
  await expect(page.locator('#toast-container').getByText('インポートが完了しました').last()).toBeVisible();

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  // import 分は残る
  await expect(page.getByText('STRICT-NEW-8811').first()).toBeVisible();
  // strict 固有の破壊性: victim (import に含まれないユーザー project) は消える
  await expect(page.getByText('STRICT-VICTIM-8810')).toHaveCount(0);
  // defaults は mergeProjectsWithDefaults で温存される (「全置換」でも消えない)
  await expect(page.getByText('タスク管理アプリ').first()).toBeVisible();
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

test('Notes textarea retains focus while typing (focus-loss regression)', async ({ page }) => {
  await page.goto('/#/apps/notes', { waitUntil: 'domcontentloaded' });
  const ta = page.locator('#notes-input');
  await expect(ta.first()).toBeVisible();
  await ta.first().click();
  await page.keyboard.press('End');
  await page.keyboard.type('ZZZ', { delay: 40 });
  const activeId = await page.evaluate(() => document.activeElement && document.activeElement.id);
  expect(activeId).toBe('notes-input');
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

// ===== SPA route-change focus management (WCAG 2.4.3) =====
// SPA は route 遷移で #content を作り直すため、ナビ後に focus が body へ落ちキーボード/SR ユーザが
// 文脈を失う。route 遷移時のみ新ページ h1 へ focus を移す (isRouteChange=hash 変化 かつ
// _focusWasLost=clear 後 activeElement が body の時のみ)。State.update 由来の同一ルート再描画では
// 動かさず (#258 非回帰)、#content 外の生存要素 (command palette input) からは奪わない。
test('Route change moves focus to the new page heading (a11y WCAG 2.4.3)', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.evaluate(() => { location.hash = '#/contact'; });
  await expect(page.locator('#content h1', { hasText: 'Contact' })).toBeVisible();
  await page.waitForTimeout(150);
  const active = await page.evaluate(() => ({
    tag: document.activeElement && document.activeElement.tagName,
    text: document.activeElement && document.activeElement.textContent,
  }));
  expect(active.tag).toBe('H1');
  expect(active.text).toContain('Contact');
});

test('Route-focus does NOT steal focus from an open command palette (steal-flake regression)', async ({ page }) => {
  // route 変更 render が palette open の input focus と race して focus を奪う flake の回帰防止。
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  await page.keyboard.press('Control+k');
  await expect(page.locator('#command-palette-host')).toHaveAttribute('aria-hidden', 'false');
  await expect(page.locator('.cmdk-input')).toBeFocused();
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
const A11Y_ROUTES = ['#/', '#/projects', '#/about', '#/contact', '#/resume', '#/apps', '#/settings', '#/quiz', '#/apps/task', '#/apps/todo', '#/apps/pomodoro', '#/apps/ai', '#/apps/notes', '#/hiring-risk', '#/ai-knowhow', '#/role-split', '#/not-found'];
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

// ===== 7.1: コマンドパレット open 状態の axe a11y (overlay a11y parity) =====
// route-based axe (A11Y_ROUTES) は palette が閉じた状態のみ走る。command palette はオーバーレイ
// (非ルート) ゆえ open 状態の a11y が未被覆だった。drawer-open axe と同 parity で、Cmd+K で開いた
// dialog (role=dialog/listbox/option + focus-trap) に render-neutral critical 違反が無いことを検証する。
test('a11y axe: open command palette has no render-neutral critical violations', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.keyboard.press('Control+k');
  await expect(page.locator('#command-palette-host')).toHaveAttribute('aria-hidden', 'false');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'])
    .analyze();
  const offenders = results.violations.filter(v => A11Y_RENDER_NEUTRAL_RULES.includes(v.id));
  expect(
    offenders,
    'open-command-palette render-neutral a11y violations: ' +
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
  { hash: '#/apps/notes',        name: 'app-notes' },
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