// @ts-check
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

// ===== axe の best-practice 違反の baseline (ゲートの死角を可視化する) =====
//
// ## なぜ必要か
//
// `e2e/a11y-axe.spec.js` は **WCAG タグの rule だけ**を強制する (allowlist 方式)。
// axe の `best-practice` タグの rule —— WCAG の達成基準ではないが ARIA / HTML の
// **規範的な適合要件**を見るもの —— は、違反が何件出ても **どのゲートにも現れない**。
// つまり新しい best-practice 違反が入っても **永久に無音**で、リポジトリの他の面で
// 繰り返し踏んできた「宣言されているのに見ている層が一つも無い」class そのものだった。
//
// ## 実測 (2026-08-21・全 16 ルート・既定内容)
//
// 現状の best-practice 違反は **たった 1 ルール / 2 ルート / 23 ノード**:
//
//   aria-allowed-role [minor]  #/projects (18) + #/apps (5)
//
// いずれも `<article role="listitem">`。ARIA in HTML は `<article>` に許す role を
// application / document / feed / main / none / presentation / region と定めており
// `listitem` は含まれない。
//
// ## なぜ「既知の例外」として据え置くのか (変更しない判断も成果物)
//
// 実 a11y ツリー (CDP `Accessibility.getFullAXTree`) を測ると Chromium は
// **この上書きを正しく honor している**:
//
//   list=1  listitem=18  article=0
//
// つまり #1013 が入れたリスト意味論は実際に機能しており、`<article>` 自身の意味論は
// **上書きで既に失われている** (article=0) ので、`div` へ変えても失うものは無い代わりに
// **得られるものも測れない**。他エンジン (Firefox / WebKit) は本リポジトリに
// インストールされておらず、そちらで壊れるという主張は**実測できない仮定**にとどまる。
// 一方コストは実在し、`e2e/**` の `article` 参照は 70 箇所ある。
// 「一般論を根拠にコードを足すな —— 必要性を実測で示せないなら padding」(CLAUDE.md §7)
// に従い、**変更せず・可視化する**を選んだ。
//
// ## この test が守るもの
//
// 「既知の 1 パターン以外の best-practice 違反が新たに入らないこと」。
// ノード数ではなく **`ルート + rule` の組**を pin する —— プロジェクトを 1 件足せば
// 18→19 になるが、それは同じ既知パターンであって新しい違反ではないため。
// 逆に **別ルート**や**別 rule** で出たら、それは新規の適合違反なので RED になる。
const BP_ROUTES = [
    '#/', '#/projects', '#/about', '#/contact', '#/resume', '#/apps', '#/settings',
    '#/quiz', '#/apps/task', '#/apps/todo', '#/apps/pomodoro', '#/apps/ai',
    '#/apps/notes', '#/hiring-risk', '#/role-split', '#/ai-knowhow', '#/not-found',
];

// 既知の例外 = `<article role="listitem">` (上の実測と根拠を参照)。
const BP_KNOWN = ['#/apps aria-allowed-role', '#/projects aria-allowed-role'];

test('best-practice 違反は既知の 1 パターンだけ (ゲートの死角を可視化)', async ({ page }) => {
    test.setTimeout(180000);
    const found = [];
    let scanned = 0;

    for (const route of BP_ROUTES) {
        await page.goto('/' + route, { waitUntil: 'domcontentloaded' });
        await expect(page.locator('#content h1').first()).toBeVisible();
        // View Transition のアニメーション中に走らせると **過大に出る**
        //   (実測 #1158: 3 ルートで待ち 120ms なら 594 件 / settle 後は 30 件)。
        await page.waitForTimeout(350);

        const res = await new AxeBuilder({ page })
            .include('#content')
            .withTags(['best-practice'])
            .analyze();
        scanned += 1;
        for (const v of res.violations) {
            found.push(`${route} ${v.id}`);
        }
    }

    // control: 走査が実際に成立していること。ルートを 1 つも回れていない、あるいは
    //   axe が何も見ていない状態だと「違反ゼロ」と区別が付かず vacuous に緑になる。
    expect(scanned, 'control: 全ルートを走査できていない').toBe(BP_ROUTES.length);
    expect(found.length,
        'control: 既知の例外すら検出できていない —— withTags(best-practice) が効いていない疑い')
        .toBeGreaterThan(0);

    const unique = [...new Set(found)].sort();
    expect(unique,
        '新しい best-practice 違反が入った (既知は <article role="listitem"> の 2 ルートのみ)')
        .toEqual(BP_KNOWN);
});
