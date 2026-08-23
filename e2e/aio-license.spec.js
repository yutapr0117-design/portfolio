const { test, expect } = require('@playwright/test');

// ===== ライセンス宣言が「実際にレンダリングされた DOM」で機械可読であること =====
// 静的 Check (444) は index.html のソースを読むが、**このサイトは runtime で JSON-LD を
// 注入する** —— route 追従ノード (`#webpage-dynamic`) と speakable ノードは MutationObserver
// と meta 適用のあとにしか存在しない。したがって「クローラが実際に見る状態」は e2e でしか
// 測れない。
//
// なぜ守る価値があるか: ACD-1.0 §6.5 は
//   「a permission that an automated system cannot determine is ... no permission at all」
// と述べている。宣言が 1 ノードでも欠けると、その経路から来た agent は学習可否を判定できず、
// **ライセンスが自分の主張を満たしていない**状態になる。
//
// 実測 (2026-08-23) で見つかった欠落: ImageObject ×3 / AudioObject ×3 / TechArticle /
// FAQPage / route 追従 WebPage / speakable WebPage —— とくにバイナリ資産は
// **XMP と ID3 が ACD-1.0 と言っているのに JSON-LD だけ無言**という面ごとの食い違いだった。

// schema.org で `license` が定義されるのは CreativeWork とその派生。
// Person / Organization / BreadcrumbList は CreativeWork ではないので対象外。
const CREATIVE_WORK_TYPES = new Set([
  'CreativeWork', 'WebSite', 'WebPage', 'ImageObject', 'AudioObject',
  'VideoObject', 'TechArticle', 'Article', 'FAQPage', 'MediaObject',
]);

async function collectLicenseState(page) {
  return page.evaluate((types) => {
    const CW = new Set(types);
    const missing = [];
    const urls = new Set();
    let covered = 0;
    document.querySelectorAll('script[type="application/ld+json"]').forEach((s) => {
      let doc;
      try { doc = JSON.parse(s.textContent); } catch (e) { missing.push('PARSE-ERROR'); return; }
      (doc['@graph'] || [doc]).forEach((node) => {
        if (!node || !CW.has(node['@type'])) { return; }
        if ('license' in node) { covered += 1; urls.add(node.license); }
        else { missing.push((s.getAttribute('data-ld') || 'static') + ':' + node['@type'] + ':' + (node['@id'] || '')); }
      });
    });
    return { covered, missing, urls: [...urls] };
  }, [...CREATIVE_WORK_TYPES]);
}

// **ルート一覧に `#/ai-knowhow` を必ず含める。** Article JSON-LD は ARTICLE_ROUTES の
// ルートでしか注入されないので、他のルートだけを見ていると **そのノードを一度も検査しない**。
// 実測 (2026-08-23): この死角のため Article ノードだけが license を持たないまま素通りしていた
// —— 「既定の状態だけが偶然 clean」class (#1213 / #1214 / #1219 と同型)。
// **なぜ 2 ルートで足りるのか (意図的な絞り込み・見落としではない)**:
//   CreativeWork ノードの大半は静的で全ルート共通。ルートによって変わるのは
//     - route 追従 WebPage (`#webpage-dynamic`) —— 全ルートで注入される
//     - speakable WebPage —— 全ルートで注入される
//     - **Article (`#article-<route>`) —— ARTICLE_ROUTES のルートでのみ注入される**
//   なので「article ルート 1 つ + 非 article ルート 1 つ」で**ノード種別の全パターンを覆う**。
//   ルートを増やしても新しい種別は現れない。逆に **article ルートを外すと Article ノードを
//   一度も検査しなくなる** (2026-08-23 に実際その死角で license 欠落を見逃していた)。
const LICENSE_ROUTES = ['/#/projects', '/#/ai-knowhow'];

test('レンダリング後の全 CreativeWork ノードが同一のライセンスを宣言する (静的 + runtime 注入)', async ({ page }) => {
  for (const route of LICENSE_ROUTES) {
  await page.goto(route);
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1')).toBeVisible();

  // route 追従ノードは MutationObserver の debounce (300ms) + requestIdleCallback のあとに
  // 注入される。**その注入を待つのが本テストの主眼**なので、注入されたこと自体を待つ。
  await expect.poll(
    async () => page.locator('script[data-ld="dynamic-route"]').count(),
    { message: 'route 追従 JSON-LD が注入されない — semantic drift guard が動いていない' },
  ).toBe(1);

  const state = await collectLicenseState(page);

  // control: そもそも CreativeWork ノードが十分に存在すること。
  //   ここが 0 や極小だと、以下の「未宣言ゼロ」は何も検証していない。
  expect(state.covered + state.missing.length,
    'control: CreativeWork ノードが少なすぎる — 走査対象が壊れている').toBeGreaterThanOrEqual(10);

  expect(state.missing,
    'license を宣言しない CreativeWork ノードがある — その経路の agent は学習可否を判定できない').toEqual([]);

  // 面ごとに違う URL を指していたら「どれが正か」を機械が決められない
  expect(state.urls, `${route}: ライセンス URL が面ごとに食い違っている`).toEqual([
    'https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt',
  ]);
  }
});

test('HTML 標準の license リンクが全ルートで解決可能な形で存在する', async ({ page }) => {
  for (const route of ['/', '/#/projects', '/#/quiz']) {
    await page.goto(route);
    await page.waitForLoadState('domcontentloaded');
    const href = await page.locator('link[rel="license"]').getAttribute('href');
    expect(href, `${route}: rel=license の link が無い`).toBeTruthy();
    expect(href, `${route}: license リンクが全文を指していない`).toContain('LICENSES/ACD-1.0.txt');

    // 宣言だけで届かないのを防ぐため、実際に取得できることまで確かめる。
    // [環境] 本番は GitHub Pages の project site なので `/portfolio/` 配下だが、
    //   e2e の http-server は**リポジトリ root を配信する** (playwright.config.cjs)。
    //   そのため href の `/portfolio` prefix を外して引く —— これは製品の問題ではなく
    //   配信 root の違いなので、prefix を落とした上で **実ファイルに届くこと**を見る。
    //   本番側の到達性は check_deployed_freshness.py (週次) が別途検証している。
    const localPath = href.replace(/^\/portfolio\//, '/');
    const res = await page.request.get(localPath);
    expect(res.status(), `${route}: license リンク先 ${localPath} が ${res.status()}`).toBe(200);
    expect(await res.text()).toContain('Autonomous Commons Dedication');
  }
});
