const { test, expect } = require('@playwright/test');

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
  // third-party ノイズ判定: KARTE (分析サービス) が connect-src 未登録の telemetry エンドポイント
  // (例 client-log.karte.io/dd/metrics) へ接続を試み、CSP が正しくブロックすると console に CSP
  // 違反エラーが出る。これは CSP がセキュリティ境界として意図どおり動作している結果であり (C7:
  // KARTE 接続は CSP で制限する方針)、当サイトの app-logic バグではなく KARTE 側の外部挙動ノイズ。
  // karte.io ドメイン かつ CSP 違反文言のものだけを narrow に除外し、当サイト自身の CSP 違反や
  // 非 KARTE の third-party 違反は引き続き検出させる (security 境界は不変・テストの検出意図を保持)。
  const isKarteCspNoise = (e) => e.includes('karte.io') &&
    (e.includes('Content Security Policy') || e.includes('Refused to connect') || e.includes('violates'));

  // app 由来の致命的 console エラーのみ抽出 (既存の非致命フィルタ + 環境ノイズ除外)
  const fatalConsole = consoleErrors.filter(e =>
    !e.includes('non-fatal') &&
    !e.includes('View Transition') &&
    !e.includes('SW') &&
    !isEnvNoise(e) &&
    !isKarteCspNoise(e)
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
