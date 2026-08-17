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
  page.on('pageerror', err => {
    // KARTE (外部分析サービス) の edge.js が telemetry endpoint への fetch に失敗すると
    // uncaught TypeError: Failed to fetch を投げ pageerror として捕捉される。これは third-party
    // (cdn-edge.karte.io) の外部障害で当サイトの app-logic バグではない (C7: KARTE 接続は CSP で
    // 制限する方針ゆえ CI で fetch が失敗しうる)。err.message は "Failed to fetch" のみで発生源が
    // 不明だが err.stack は cdn-edge.karte.io を含むため、stack が KARTE 由来のものだけ narrow に
    // 除外する。当サイト自身のコードから出た uncaught 例外 (stack が我々の file) は引き続き無条件で
    // fatal 扱いし、app バグを検出する intent を保持する。
    const stack = (err && err.stack) || '';
    if (stack.toLowerCase().includes('karte')) { return; }
    pageErrors.push(err.message);
  });

  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // Fatal エラーがないことを確認 (先に h1 を待って描画を確定させる・Check 402)
  await expect(page.locator('h1').first()).toBeVisible();
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
  // CSP 違反文言 かつ KARTE サービス名を含むものだけを narrow に除外し、当サイト自身の CSP 違反や
  // 非 KARTE の third-party 違反は引き続き検出させる (security 境界は不変・テストの検出意図を保持)。
  // 注: ホスト名の部分文字列判定 (e.includes('karte.io')) は CodeQL js/incomplete-url-substring-
  // sanitization を誤発火させる (e は URL でなく console 診断文字列でセキュリティ判定ではないため
  // 誤検知)。ドット無しの 'karte' + CSP 文言で判定し URL 部分文字列パターンを避ける。
  const isKarteCspNoise = (e) =>
    (e.includes('Content Security Policy') || e.includes('Refused to connect')) &&
    e.toLowerCase().includes('karte');

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
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
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
// NOTE: 本テストには mutation を登録していない。`data-ai-state` の writer は **3 箇所**あり
//   (main.js のローディング宣言・main.js の確定状態・js/router.js の URL 同期)、
//   **どれか 1 つを潰しても他の 2 つが満たす**ため単一 anchor の mutation では RED にできない
//   ことを実測した (2026-08-17)。defense-in-depth ゆえの構造的制約で、テストが vacuous
//   なわけではない。RED を実測できないものは安全網に混ぜない (#1096 の reduced-motion と同型)。
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

// ===== 7.1b: silent フィルタ更新でも data-ai-state.route が正規化名を保つ =====
// projects の検索/カテゴリ絞り込みは Router.replaceSilently('projects?q=...') で URL を静かに
// 書き換える (再描画なし)。この silent パスは render パスと同じ route.name ('projects') を agentic
// surface へ公開せねばならない。旧実装は生 path 'projects?q=...' を route へ入れ render パスと
// drift していた。フィルタ後も route が 'projects' を保ち、filter に query が入ることを検証。
test('Body data-ai-state keeps a clean route name after a silent projects filter', async ({ page }) => {
  const stateOf = async () => page.evaluate(() => {
    try { return JSON.parse(document.body.getAttribute('data-ai-state')); } catch { return null; }
  });

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect.poll(async () => (await stateOf())?.route).toBe('projects');

  // 検索入力 → syncURL() が replaceSilently('projects?q=...') を呼ぶ (silent パス)
  const search = page.getByPlaceholder(/検索|search/i).first();
  await search.fill('AI');

  // route は正規化名 'projects' を保ち (生 'projects?q=AI' に drift しない)、filter に query が入る
  await expect.poll(async () => (await stateOf())?.route).toBe('projects');
  await expect.poll(async () => (await stateOf())?.filter).toContain('q=AI');
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

// ===== 7.2b: reduced-motion で View Transition が「実際にスキップされる」ことの behavioral 検証 =====
// 上の 7.2 test は reduced-motion 経路で「ナビゲーションが壊れない」ことを検証するが、View Transition
// が**実際に呼ばれない**(= 動きが抑制される WCAG 2.3.3 の核心) は未検証だった (VT が動いてもナビ自体は
// 機能するため上の test は VT-skip 回帰を捕捉できない)。document.startViewTransition を spy し、
// reduced-motion 遷移で呼び出し 0 回、no-preference 遷移で >0 回 を検証する。この 2 段構成が
// **self-non-vacuity**: reduced で 0・normal で >0 の両方を要求するため、(i) VT が reduced で動けば
// (a) が RED、(ii) spy が不作動なら (b) が RED となり、vacuous に pass しない (main.js の VT-skip は
// 585 の pre-check + Check 43b 保護の startViewTransitionProxy 189-191 の二重防衛ゆえ単一行 break では
// RED 化できず、対照測定 reduced=0/normal>0 で非 vacuity を実証する設計)。
test('View Transition is skipped under reduced-motion but fires under no-preference (WCAG 2.3.3 motion suppression)', async ({ page }) => {
  await page.addInitScript(() => {
    window.__vtSupported = typeof document.startViewTransition === 'function';
    window.__vtCalls = 0;
    if (window.__vtSupported) {
      const orig = document.startViewTransition.bind(document);
      document.startViewTransition = function (cb) { window.__vtCalls++; return orig(cb); };
    }
  });

  // (a) reduced-motion: ルート遷移で startViewTransition が呼ばれない (動き抑制・前庭安全)
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  await page.goto('/#/about', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(200);
  expect(
    await page.evaluate(() => window.__vtCalls),
    'reduced-motion では View Transition を完全スキップ (startViewTransition 呼び出し 0 回)'
  ).toBe(0);

  const supported = await page.evaluate(() => window.__vtSupported);

  // (b) 対照: no-preference では遷移で startViewTransition が発火する (spy 作動 + reduced が抑制要因で
  //     あることの実証 = 非 vacuity の self-demonstration)。reload で __vtCalls をリセット + 再 wrap。
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await page.goto('/#/about', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(200);
  const normalCalls = await page.evaluate(() => window.__vtCalls);
  if (supported) {
    expect(
      normalCalls,
      'no-preference では View Transition が発火 (spy が機能し (a) の 0 が抑制の結果であることを実証)'
    ).toBeGreaterThan(0);
  }
});


// ===== 7.1: 未知の *app* サブルート (apps/<unknown>) が NotFound になる (router whitelist else 分岐) =====
// router は `apps/<app>` で app が ['task','todo','pomodoro','ai','notes'] whitelist に無いとき
// route.name='not-found' にする (js/router.js の三項 else)。既存の未知ルートテストは top-level の
// `/#/zzz-...` を見るが、この apps-whitelist else 分岐は distinct な code path で未カバーだった。
// whitelist が壊れて未知 app を app-* 扱いすると存在しないアプリを描画しようとする退行になる。
// 未知 app サブルートで NotFound の見出し+説明が出て ErrorBoundary に落ちないことを検証する。
test('Unknown app subroute (apps/<unknown>) resolves to Not Found (router whitelist else branch)', async ({ page }) => {
  await page.goto('/#/apps/nonexistent-app-9999', { waitUntil: 'domcontentloaded' });
  await expect(page.getByRole('heading', { name: 'Not Found' })).toBeVisible();
  await expect(page.getByText('指定されたページは見つかりません。')).toBeVisible();
  // 復帰導線が機能する。
  await page.getByRole('button', { name: 'ホームへ' }).click();
  await expect(page.locator('.hero-section')).toBeVisible();
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `unknown app route caused a fatal: ${fatal}`).toBeNull();
});


// ===== ルート追従の動的 JSON-LD (Semantic Drift Prevention) が実際に注入・更新される =====
// main.js の _installSemanticDriftGuard は #content の childList を MutationObserver で監視し、
// ルート遷移のたび `script[data-ld="dynamic-route"]` の構造化データを現在のコンテンツで書き直す。
// 目的は「AI クローラがどの hash ルートでも文脈一致した structured data を見る」こと = 本リポジトリの
// 中核 (機械可読性) の一部。
// だが **この機構を守る gate は従来ひとつも無かった**: IIFE ごと消しても consistency は緑、
// behavior e2e も緑、screenshot は advisory。視覚に一切出ないため完全に silent に失われる
// (#133/#134/#135 で塞いだ「silent-critical な配線」class の AIO 面)。
// 注: 注入は 300ms debounce + requestIdleCallback(timeout 2000) 経由ゆえ固定 wait では脆い。
// expect.poll で「いずれ文脈一致する」ことを待つ (更新されなければ poll がタイムアウトして RED)。
async function dynamicLdName(page) {
  return page.evaluate(() => {
    const el = document.querySelector('script[data-ld="dynamic-route"]');
    if (!el) { return null; }
    try { return JSON.parse(el.textContent).name; } catch { return 'INVALID_JSON'; }
  });
}

test('Route-following dynamic JSON-LD is injected and tracks the current route (semantic drift guard)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // 1 つ目のルート: h1 と JSON-LD の name が一致する (文脈一致 = 本機構の契約)
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1')).toHaveText('プロジェクト一覧');
  await expect.poll(() => dynamicLdName(page), { timeout: 10000 }).toBe('プロジェクト一覧');

  // 2 つ目のルートへ遷移すると **追従して書き換わる** (初回注入だけでは drift 防止にならない)
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  const aboutHeading = (await page.locator('#content h1').textContent()).trim();
  await expect.poll(() => dynamicLdName(page), { timeout: 10000 }).toBe(aboutHeading);

  // 構造化データとして妥当であること (JSON 破損や @type 欠落を弾く)
  const ld = await page.evaluate(() => {
    const el = document.querySelector('script[data-ld="dynamic-route"]');
    return el ? JSON.parse(el.textContent) : null;
  });
  expect(ld['@context']).toBe('https://schema.org');
  expect(ld['@type']).toBe('WebPage');
  expect(ld.inLanguage).toBe('ja');
  // entity ノードへの参照が保たれている (Person / WebSite への接続が AIO 上の意味を持つ)
  expect(ld.about['@id']).toContain('#person');
  expect(ld.isPartOf['@id']).toContain('#website');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `dynamic JSON-LD test caused a fatal: ${fatal}`).toBeNull();
});

// ===== Speakable の **固有セレクタ** が実在要素へ解決する (AIO 機械向け宣言の used\u21d2defined) =====
// Speakable は AI 音声アシスタントへ「読み上げるべき要素」を宣言する機械向け面で、視覚に一切
// 出ないため screenshot も通常の behavior test も素通りする (#929 で WebMCP の幻セレクタが
// 一度も対象を持っていなかったのと同じ class)。ルート毎の **固有セレクタ** (home の
// `.sr-only[data-ai-entity]` / role-split の `#role-split-table` / ai-knowhow の
// `.ai-summary-block`) が実際に要素へ解決することを固定する。
//
// NOTE (意図的に検査しないもの): `[data-speakable]` は **home 以外で 0 件**であることを実測済。
//   `data-speakable` 属性は js/home-page.js にしか存在しない。これは宣言と実態の乖離だが、
//   Speakable は AIO の semantic content ゆえ **C6 (orchestrator の書面承認)** の領域で、
//   AI 単独では直せない。実測値・提案する最小修正・順序 (宣言を直してから Check を張る) は
//   docs/architecture/research-application-policy.md に defer として記録済。
//   ここでそれを assert すると **恒久 RED** になるため対象外にしている。
const SPEAKABLE_ROUTE_SELECTORS = [
  ['#/', '.sr-only[data-ai-entity]'],
  ['#/role-split', '#role-split-table'],
  ['#/ai-knowhow', '.ai-summary-block'],
];
for (const [hash, selector] of SPEAKABLE_ROUTE_SELECTORS) {
  test(`Speakable route selector resolves on ${hash} (${selector})`, async ({ page }) => {
    await page.goto(`/${hash}`, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1, #content h2').first()).toBeVisible();

    // (1) 宣言側: 注入された Speakable JSON-LD が当該セレクタを含む
    const declared = await page.evaluate(() => {
      const el = document.querySelector('script[data-ld="speakable"]');
      if (!el) { return null; }
      try { return JSON.parse(el.textContent).speakable.cssSelector; } catch (e) { return null; }
    });
    expect(declared, 'Speakable JSON-LD が注入されていない').not.toBeNull();
    expect(declared, `${hash} の Speakable が ${selector} を宣言していない`).toContain(selector);

    // (2) 実態側: そのセレクタが実際に要素へ解決する (宣言だけで実体が無い状態を禁じる)
    await expect(
      page.locator(selector),
      `${hash}: Speakable が宣言する ${selector} が 1 件も解決しない (機械向け宣言が実態と乖離)`
    ).not.toHaveCount(0);
  });
}

// ===== data-ai-state.loading のライフサイクル (agentic な「描画完了」信号) =====
// `data-ai-state` は {route, filter, loading} を公開する機械可読面。既存テストは route と
// filter を見ているが、**loading は未被覆**だった。AI エージェントにとって loading は
// 「今読んで良いか / まだ描画中か」を判断する唯一の信号で、壊れ方は 2 通りある:
//   (a) `loading:true` が一度も出ない → エージェントは描画中を検知できない
//   (b) 最後が `loading:true` のまま → **永遠に読み込み中**と誤解して待ち続ける
// どちらも視覚に一切出ないため screenshot も通常の behavior test も素通りする (#929 class)。
//
// NOTE: 属性の**単発読み**では瞬間値を取り逃す (実測: 単発だと常に loading:false しか見えない)。
//   MutationObserver で **遷移の系列**を記録してから検証する。
test('data-ai-state exposes a true->false loading lifecycle per route (agentic settle signal)', async ({ page }) => {
  await page.addInitScript(() => {
    window.__aiStates = [];
    const start = () => {
      const mo = new MutationObserver(() => {
        const v = document.body.getAttribute('data-ai-state');
        if (v && window.__aiStates[window.__aiStates.length - 1] !== v) { window.__aiStates.push(v); }
      });
      mo.observe(document.body, { attributes: true, attributeFilter: ['data-ai-state'] });
    };
    if (document.body) { start(); } else { document.addEventListener('DOMContentLoaded', start); }
  });

  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('.grid-projects article.card').first()).toBeVisible();
  await page.goto('/#/quiz', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();

  // 遷移が記録されるまで待つ (0 件なら以降は vacuous)
  await expect.poll(
    async () => (await page.evaluate(() => (window.__aiStates || []).length)),
    { message: 'data-ai-state の変化が 1 度も観測されない — observer が動いておらず以降が vacuous' }
  ).toBeGreaterThan(1);

  // 最終状態が settle するまで待つ (loading:false で終わること)
  await expect.poll(async () => {
    const s = await page.evaluate(() => (window.__aiStates || []).slice(-1)[0] || '');
    try { return JSON.parse(s).loading; } catch (e) { return null; }
  }, { message: '最終状態が loading:false にならない (エージェントが永遠に読み込み中と誤解する)' }).toBe(false);

  const states = (await page.evaluate(() => window.__aiStates || [])).map((s) => {
    try { return JSON.parse(s); } catch (e) { return null; }
  }).filter(Boolean);

  // (a) 描画中を示す loading:true が実際に公開される
  expect(
    states.some((s) => s.loading === true),
    'loading:true が一度も公開されない (エージェントが描画中を検知できない)'
  ).toBe(true);

  // (b) true が false より先に現れる (順序が逆なら信号として使えない)
  const firstTrue = states.findIndex((s) => s.loading === true);
  const lastFalse = states.map((s) => s.loading).lastIndexOf(false);
  expect(firstTrue, 'loading:true が見つからない').toBeGreaterThanOrEqual(0);
  expect(lastFalse, 'loading:true の後に loading:false が来ていない').toBeGreaterThan(firstTrue);
});

// ===== WebMCP ツールが実 DOM から抽出できる (agentic 面の実行被覆) =====
// main.js は `navigator.modelContext.registerTool` が存在する場合だけ WebMCP ツールを登録する。
// **どのブラウザもまだ WebMCP を実装していない**ため、この登録は実環境でも Playwright でも
// 一度も起きず、`execute()` は **実行被覆ゼロ**だった。#929 では走査セレクタがリポジトリの
// どこにも存在せず「現在の DOM 状態から抽出します」と謳いながら常に静的フォールバックを
// 返していた — **宣言と実態の乖離が長期間 silent に残る典型**で、しかも壊れるのは
// 本プロジェクトの中核賭け金 (機械可読な権威付け) の面。
//
// API を shim して **実際に execute() を呼ぶ**ことで、#929 の class を構造的に閉じる。
test('WebMCP tool extracts from the live DOM on its route and falls back off-route', async ({ page }) => {
  await page.addInitScript(() => {
    window.__mcpTools = [];
    // 実ブラウザには存在しない API を shim する (登録経路自体を通すため)
    window.navigator.modelContext = { registerTool: (t) => { window.__mcpTools.push(t); return true; } };
  });

  await page.goto('/#/role-split', { waitUntil: 'domcontentloaded' });
  // 表が描画され切ってから測る (前ルートの残骸を読まないための positive anchor)
  await expect(page.locator('#role-split-table')).toBeVisible();

  const onRoute = await page.evaluate(async () => {
    const tools = window.__mcpTools || [];
    if (!tools.length) { return { registered: 0 }; }
    const t = tools[0];
    const text = (await t.execute({})).content[0].text || '';
    const json = (await t.execute({ format: 'json' })).content[0].text || '';
    let parsed = null;
    try { parsed = JSON.parse(json); } catch (e) { /* noop */ }
    return {
      registered: tools.length,
      name: t.name,
      readOnly: !!(t.annotations && t.annotations.readOnlyHint),
      hooks: document.querySelectorAll('[data-ai-role]').length,
      text,
      detailsCount: parsed && Array.isArray(parsed.details) ? parsed.details.length : -1,
    };
  });

  expect(onRoute.registered, 'WebMCP ツールが 1 つも登録されない — 以降が vacuous').toBe(1);
  expect(onRoute.name).toBe('extract_human_vs_ai_role_split');
  expect(onRoute.readOnly, 'readOnlyHint が落ちている (エージェントが副作用ありと誤解する)').toBe(true);
  expect(onRoute.hooks, 'data-ai-role フックが描画されていない').toBeGreaterThan(0);

  // 実 DOM から抽出できていること = 静的フォールバック文字列ではないこと
  expect(
    onRoute.text.startsWith('Human: Architecture'),
    'role-split 上なのに静的フォールバックを返した (走査セレクタが実描画に解決していない・#929 class)'
  ).toBe(false);
  expect(onRoute.text.length, '抽出結果が実質空').toBeGreaterThan(100);
  // format=json 分岐が到達可能で、DOM 由来の details を含むこと
  expect(onRoute.detailsCount, 'format=json が有効な JSON を返さない / details が空').toBeGreaterThan(0);

  // 別ルートでは graceful に静的フォールバックへ落ちる (宣言どおりの挙動)
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('.grid-projects article.card').first()).toBeVisible();
  await expect.poll(
    () => page.evaluate(() => document.querySelectorAll('[data-ai-role]').length),
    { message: 'ルート遷移後も role-split のフックが DOM に残っている' }
  ).toBe(0);

  const offRoute = await page.evaluate(async () => {
    const t = (window.__mcpTools || [])[0];
    return ((await t.execute({})).content[0].text || '');
  });
  expect(
    offRoute.startsWith('Human: Architecture'),
    'フック不在のルートで静的フォールバックに落ちない (エージェントへ古いデータを返す)'
  ).toBe(true);
});


// ===== 全ルートの title / description が一意で非空 =====
// 既存テストは 3 ルートを個別のパターンで確認しているが、**全ルートを横断した一意性**は
// 見ていなかった。PAGE_META の追加時に既存エントリをコピーして書き換え忘れると、
// 2 つのルートが同じ title / description を名乗る —— AI クローラや検索にとっては
// 「同じページが複数ある」ことになり、AIO を中核に据えたこのサイトでは実害が大きい。
// しかも **見た目には一切出ない** (画面の内容は正しく変わる) ので、この種の gate 以外に
// 気付く経路が無い。og:title の欠落も同様。
//
// canonical はハッシュ SPA ゆえ全ルートでサイトルートを指すのが設計どおりなので、
// ここでは一意性を要求しない (指し先が正しいことだけ確認する)。
test('All routes expose a unique, non-empty title and description (AIO)', async ({ page }) => {
  const ROUTES = ['', '#/projects', '#/quiz', '#/about', '#/resume', '#/contact', '#/role-split',
    '#/hiring-risk', '#/ai-knowhow', '#/apps', '#/apps/task', '#/apps/todo', '#/apps/notes',
    '#/apps/ai', '#/apps/pomodoro', '#/settings'];

  const seen = [];
  let previousTitle = null;
  for (const route of ROUTES) {
    await page.goto('/' + route, { waitUntil: 'domcontentloaded' });
    // [重要] `#content h1` の visible を待つのは **役に立たない** —— 前ルートの DOM で
    //   既に満たされるため、全ルートで同じ値を読んでしまい「全部重複」という誤判定になる
    //   (実測でこの形の誤りを踏んだ)。**変化**を待つのが正しく、ここでは title が
    //   直前のルートと変わったことを待つ (title の更新が applyMeta の最後段)。
    if (previousTitle !== null) {
      await expect.poll(() => page.title(), { message: `${route}: title が更新されない` })
        .not.toBe(previousTitle);
    }
    const meta = await page.evaluate(() => ({
      title: document.title,
      desc: (document.querySelector('meta[name="description"]') || {}).content || '',
      og: (document.querySelector('meta[property="og:title"]') || {}).content || '',
      canonical: (document.querySelector('link[rel="canonical"]') || {}).href || '',
    }));
    seen.push([route || 'home', meta]);
    previousTitle = meta.title;
  }

  const empty = seen.filter(([, m]) => !m.title || !m.desc || !m.og).map(([r]) => r);
  expect(empty, `title / description / og:title が空のルート: ${empty.join(', ')}`).toEqual([]);

  for (const key of ['title', 'desc']) {
    const values = seen.map(([, m]) => m[key]);
    const dups = [...new Set(values.filter((v, i) => values.indexOf(v) !== i))];
    const owners = dups.map((d) => seen.filter(([, m]) => m[key] === d).map(([r]) => r).join(' / '));
    expect(dups, `${key} が重複しているルート: ${owners.join(' | ')}`).toEqual([]);
  }

  // canonical は全ルート共通でサイトルート (hash SPA の単一 canonical 戦略)
  const canonicals = [...new Set(seen.map(([, m]) => m.canonical))];
  expect(canonicals, 'canonical が単一のサイトルートを指していない').toHaveLength(1);
  expect(canonicals[0]).toMatch(/yutapr0117-design\.github\.io\/portfolio\/$/);
});
