const { test, expect } = require('@playwright/test');

// ===== agentic surface — body[data-ai-state] の機械可読契約 =====
// `e2e/aio-meta.spec.js` から分離 (2026-08-23)。同 file が advisory 予算 900 行を超えており
// (907)、**BLOCKING(1,000) に当たる前に**単一の契約という coherent な塊として切り出した。
//
// この面が守るもの: main.js と js/router.js が `<body data-ai-state>` へ
// `{route, filter, loading}` を JSON で書き込む。**AI エージェントが DOM から現在状態を読む
// 唯一の機械可読サーフェス**で、壊れても視覚には一切出ないため screenshot も通常の behavior
// test も素通りする (#929 class)。
//
// 4 つの壊れ方をそれぞれ別テストで押さえている:
//   - route が遷移に追従しない        → エージェントが今どこにいるか判らない
//   - filter が確定後に空へ戻る       → 絞り込み状態が読めない (#1226 の実バグ)
//   - 敵対的 query で JSON が壊れる    → **面ごと解釈不能になる** (攻撃者が中身を決められる唯一の field)
//   - loading の系列が壊れる          → 「今読んで良いか」が判らない / 永遠に待つ

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


// ===== 7.1c: data-ai-state.filter が **確定後**も URL の絞り込みを表すこと =====
// 上の 7.1b は `expect.poll(...filter).toContain('q=AI')` で「いつか正しい値になる」ことを
// 見る。だが `filter` の書き手は 3 箇所あり、**正しい値が一過性で上書きされる**という
// 壊れ方をしていた。実測 (2026-08-21) の書き込み系列:
//
//   {filter:"", loading:true} → {filter:"q=AI"} → {filter:"", loading:false}
//                                  ↑ poll はここで成功して緑になる  ↑ 実際に残るのはこれ
//
// つまり **7.1b はバグがある状態でも通る** (修正を戻して実測済み)。さらに悪いことに、
// `#/projects?q=AI` を**直接開いた**場合 (ブックマーク / 共有リンク / エージェントの追跡) は
// 正しい値が一度も書かれず、18 件中 4 件に絞られているのに「絞り込みなし」と宣言していた。
// 原因は render パス (main.js の描画前 / 描画後) が `filter: ''` をハードコードしていたこと。
//
// この test は **確定後の値を 1 度だけ読み、さらに安定していること**まで見る
// (CLAUDE.md §7: 変化の検査には poll、不変性の検査には settle 後に 1 度読む)。
//
// 登録した mutation は router の単一ソース `getFilterString` を潰すもの 1 件だけ。
// 実測した帰属 (2026-08-21):
//   - router の getFilterString を空に        → RED
//   - main.js の **描画後** rAF を `''` に戻す → RED
//   - main.js の **描画前** (loading:true) だけを `''` に戻す → **緑**
// 3 つ目は「その直後に描画後の writer が正しい値で上書きする」ため単一 mutation では
// 原理的に RED にできない (defense-in-depth ゆえの構造的制約で、test が vacuous なわけ
// ではない)。RED を実測できないものは安全網に混ぜない (#1096 の reduced-motion と同型)。
test('data-ai-state.filter は確定後も URL の絞り込みを表す (機械可読面の単一ソース)', async ({ page }) => {
  const stateOf = () => page.evaluate(() => {
    try { return JSON.parse(document.body.getAttribute('data-ai-state')); } catch { return null; }
  });
  // **変化を待ってから、確定していることを確かめる** の 2 段。
  //   前段の poll が無いと stale な値を掴む —— 実測 (2026-08-21): `#/projects?q=AI` から
  //   `#/projects` への同一文書遷移では `article` の可視も `aria-busy='false'` も
  //   **前の描画の値で満たされる**ため、直前ルートの `q=AI` を「確定値」と誤読した
  //   (CI 負荷下でのみ再現。ローカル単独では新描画が先に終わって隠れる)。
  //   後段の停止確認が無いと一過性の値で緑になる (それが本 test の動機そのもの)。
  const settledFilter = async (expected, label) => {
    await expect.poll(async () => (await stateOf())?.filter,
        { message: `${label}: filter が期待値に到達しない` }).toBe(expected);
    await page.waitForTimeout(400);
    expect(await page.evaluate(() => {
      try { return JSON.parse(document.body.getAttribute('data-ai-state')).filter; } catch { return null; }
    }), `${label}: filter が一過性で上書きされた`).toBe(expected);
  };

  // --- A: 直接 URL (正しい値が一度も書かれなかった経路) ---
  await page.goto('/#/projects?q=AI', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content .grid-projects article').first()).toBeVisible();
  const shown = await page.locator('#content .grid-projects article').count();
  const total = 18;
  // control: 実際に絞り込まれていなければ「絞り込みを表す」ことを検証できない
  expect(shown, `control: q=AI で絞り込めていない (${shown} 件)`).toBeLessThan(total);
  await settledFilter('q=AI', 'A 直接 URL で開いた絞り込み');

  // --- B: 検索欄への入力 (正しい値が一過性で上書きされていた経路) ---
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content .grid-projects article').first()).toBeVisible();
  await settledFilter('', 'control: 絞り込み前');
  await page.getByPlaceholder(/検索|search/i).first().fill('AI');
  await expect.poll(async () => page.evaluate(() => location.hash)).toContain('q=AI');
  await settledFilter('q=AI', 'B 入力後の絞り込み');

  // --- C: 絞り込みの無いルートでは空 (何かを常に入れているだけ、を排除する) ---
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await settledFilter('', 'C 絞り込みの無いルート');
});

// ===== 7.1d: data-ai-state は敵対的な query でも壊れない JSON であり続ける =====
// #1226 で `filter` は **URL の query をそのまま echo する**ようになった。つまり
// **攻撃者が中身を決められる文字列が機械可読面へ流れる**唯一のフィールドになっている。
//
// 実害の形は「クラッシュ」ではなく **agent 側が丸ごと解釈不能になる**こと ——
// 例えば `JSON.stringify` をやめて文字列連結にすると、引用符を含む query 1 つで
// 属性全体が壊れた JSON になり、`route` も `loading` も読めなくなる。視覚には一切出ないので
// screenshot でも目視でも気付けない (#929 / #930 と同じ機械可読面の class)。
//
// 実測 (2026-08-21) では 4,000 文字 / `"><script>` / 改行 / `__proto__` / 不正 percent の
// いずれでも JSON は valid で fatal も無い。**上限は設けていない** —— 通常操作では作れない
// URL であり、必要性を実測で示せないまま bound を足すのは padding だと判断した
// (CLAUDE.md §7「一般論を根拠にコードを足すな」)。ここで固定するのは **パース可能性**。
test('data-ai-state は敵対的な query でも valid JSON であり続ける (機械可読面の頑健性)', async ({ page }) => {
  const cases = [
    ['引用符とタグ', 'q=' + encodeURIComponent('"><script>alert(1)</script>')],
    ['バックスラッシュ', 'q=' + encodeURIComponent('a\\"b\\\\c')],
    ['改行', 'q=' + encodeURIComponent('a\nb\rc')],
    ['プロトタイプ継承キー', 'q=__proto__&cat=constructor'],
    ['不正 percent', 'q=%E0%A4%A'],
    ['長大', 'q=' + 'A'.repeat(2000)],
  ];

  for (const [label, qs] of cases) {
    await page.goto('/#/projects?' + qs);
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('#content h1', { hasText: 'プロジェクト' })).toBeVisible();

    const r = await page.evaluate(() => {
      const raw = document.body.getAttribute('data-ai-state') || '';
      try {
        const o = JSON.parse(raw);
        return { ok: true, route: o.route, hasFilter: typeof o.filter === 'string',
                 loading: typeof o.loading === 'boolean' };
      } catch (e) { return { ok: false, raw: raw.slice(0, 60) }; }
    });

    expect(r.ok, `${label}: data-ai-state が valid JSON でない (agent は route も loading も読めない) — ${r.raw}`).toBe(true);
    // control 兼: 壊れていないだけでなく、他のフィールドが正しく読めること
    expect(r.route, `${label}: route が正しくない`).toBe('projects');
    expect(r.hasFilter, `${label}: filter が文字列でない`).toBe(true);
    expect(r.loading, `${label}: loading が真偽値でない`).toBe(true);

    const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
    expect(fatal, `${label}: 敵対的 query が fatal を起こした: ${fatal}`).toBeNull();
  }
});


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

