const { test, expect } = require('@playwright/test');

// ===== WCAG 1.4.10 (Reflow): 320px 幅で横スクロールを発生させない =====
//
// 元は e2e/navigation-a11y.spec.js にあったが、同 file が 917 行となり advisory (900) を
// 超えたため、**BLOCKING (1,000 行) を踏む前に**このテーマの塊を切り出した
// (CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。
//
// なぜ Reflow が独立したテーマか:
//   この面は **視覚 baseline では原理的に守れない**。screenshot は 1280×720 clip なので
//   `@media (max-width: 920px)` に到達せず、320px であふれていても緑のまま通る (#962)。
//   つまり behavior e2e だけが捕捉層で、しかも真因は「封じ込めの欠陥」—— `.main-content` の
//   左右 auto margin が flex の cross 軸で `align-self: stretch` を無効化し、
//   fit-content が min-content を下回れないため **item 自体が viewport より広くなる**。
//   ブランドごとにフォント幅が違うので **classic でも別途測る**必要がある。

// ===== WCAG 1.4.10 (Reflow): 320px 幅で横スクロールを発生させない =====
// WHY この test が必要か:
//   基底の `.main-content` は `max-width: 1200px; margin: 0 auto` で本文カラムを中央寄せする。
//   ところが `@media (max-width: 920px)` で `.app` が `flex-direction: column` になると、その
//   左右 margin が **cross 軸の auto margin** になる。flexbox 仕様上、cross 軸に auto margin を
//   持つ flex item には `align-self: stretch` が適用されず fit-content でサイズが決まり、
//   fit-content は min-content を下回れないため、本文の min-content が viewport を超えた
//   ルートでは item 自体が viewport より広くなってページ全体が横に溢れていた
//   (実測: role-split +51px / quiz +31px / hiring-risk +28px / pomodoro +16px)。
//   修正は media query 内の `max-width: 100%` 1 行だが、**視覚 baseline では検出できない**
//   (screenshot は 1280x720 clip = 920px 超なのでこの media query に到達しない) ため、
//   回帰を捕まえられるのはこの behavior test だけ。
//
// NOTE: 幅を 320px にするのは WCAG 1.4.10 が「400% ズーム相当 = 320 CSS px」を基準にするため。
//
// NOTE (2026-08-12 実測・再調査不要): **利用者データが長い連続文字列でも**この契約は保たれる。
//   プロジェクト名に改行機会の無い 120 文字を入れて projects / settings を 320px で測ったところ、
//   document の overflow は **0** で、Settings の並べ替えリストは `overflow-x: auto` により
//   **自分のコンテナ内でスクロール**していた (scrollWidth 1284 / clientWidth 238)。
//   この「長文データ版」の test は**追加していない** —— containment を壊す mutation
//   (media query 内の `max-width: 100%` 無効化) を当てても長文版は緑のままで、
//   **RED を実測できないテストは安全網に混ぜない**規律に従った。
//   同じ mutation で本 test は RED (role-split +51px) になるので、契約の番人はこちらで足りている。



// ===== ルート固有の settle =====
// [FIX 2026-08-24] **汎用の「見出しが見える」待ちは、hash 遷移では前ルートの DOM で即座に
//   成立する。** 直後に `page.evaluate` で測ると **全イテレーションが最初のルートを測る**。
//   実測 (2026-08-24): reflow の 6 ルートループは `#/role-split` を 6 回測っており、#962 で
//   直した実バグの対象 (quiz +31px / hiring-risk +28px / pomodoro +16px) は**一度も測られて
//   いなかった**。axe のダーク走査は「ちょうど 1 つ前のルート」を走査していた。
//
//   待ち方: 遷移前に `#content` へ印を置き、**再描画で子ごと消える**のを待つ (render は
//   `#content` を clear する)。ルート名のハードコード表を持たずに済む —— 表は必ず drift する。
//   `loading` は quiz の動的 import 等が終わるまで true なので、遅延読み込み面も決定的に待てる。
//   例外: **目標が現在ルートと同じときは hashchange が発火せず再描画も起きない** (#269 で
//   記録済みの仕様) ので、印の消滅を待つと必ず timeout する。その場合は既に正しい DOM が
//   出ているので `loading` の確定だけ待つ。
async function gotoRouteSettled(page, hash) {
  const target = hash.startsWith('/') ? hash.slice(1) : hash;
  let cur = '';
  try { cur = new URL(page.url()).hash; } catch { cur = ''; }
  const already = cur === target || ((cur === '' || cur === '#/') && target === '#/');
  if (!already) {
    await page
      .evaluate(() => {
        const c = document.getElementById('content');
        if (c) { const m = document.createElement('span'); m.id = '__e2e_stale__'; c.appendChild(m); }
      })
      .catch(() => {});
  }
  await page.goto(`/${hash}`, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(
    (skip) => {
      if (!skip && document.getElementById('__e2e_stale__')) { return false; }
      try { return JSON.parse(document.body.dataset.aiState || '{}').loading === false; }
      catch { return false; }
    },
    already,
    { timeout: 10000 }
  );
}

test('WCAG 1.4.10: 320px 幅でどのルートも横スクロールしない', async ({ page }) => {
  // 過去に実際あふれていた 4 ルート + あふれていなかった 2 ルート (対照)
  const routes = ['#/role-split', '#/quiz', '#/hiring-risk', '#/apps/pomodoro', '#/', '#/projects'];
  await page.setViewportSize({ width: 320, height: 800 });

  for (const route of routes) {
    await gotoRouteSettled(page, route);

    const overflow = await page.evaluate(() => {
      const de = document.documentElement;
      return { doc: de.scrollWidth - de.clientWidth, main: Math.round(document.getElementById('main-content').getBoundingClientRect().width) };
    });
    expect(overflow.doc, `${route} が 320px 幅で横に ${overflow.doc}px あふれている (WCAG 1.4.10)`).toBe(0);
    expect(overflow.main, `${route} の #main-content が viewport (320px) より広い`).toBeLessThanOrEqual(320);

    const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
    expect(fatal, `${route} で fatal: ${fatal}`).toBeNull();
  }
});

// 同じ契約を **より厳しい条件** でも通す。ブランド `classic` は本文フォントが Inter になり、
// 既定 (DM Sans) より **約 5.9% 幅広**に描画される (実測 2026-08-18: 同一文字列の幅が
// 248.31px → 262.98px)。既存の gate は既定ブランドしか通しておらず、
// **非既定ブランドでだけあふれる回帰**を素通りさせる。実測では classic でも全ルート 0 だが、
// 幅が広い側を通しておかないと gate が守っているのは「既定フォントでの契約」に留まる。
//
// NOTE: フォントが実際に切り替わっていることを control として確かめる。切り替わらなければ
//   これは既定ブランドの test をもう 1 本増やしただけの vacuous なテストになる。
test('WCAG 1.4.10: 320px 幅で classic ブランド (より幅広なフォント) でもあふれない', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('portfolio_brand_v45', 'classic'));
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto('/#/role-split', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#main-content h1, #main-content h2').first()).toBeVisible();

  // control: ブランドが実際に適用され、Inter 系のフォントで描画されている
  const applied = await page.evaluate(() => ({
    brand: document.documentElement.getAttribute('data-brand'),
    family: getComputedStyle(document.body).fontFamily,
  }));
  expect(applied.brand, 'classic ブランドが適用されていない').toBe('classic');
  expect(applied.family, '本文フォントが Inter 系に切り替わっていない').toContain('Inter');

  for (const route of ['#/role-split', '#/quiz', '#/hiring-risk', '#/apps/pomodoro']) {
    await gotoRouteSettled(page, route);
    const doc = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(doc, `${route} が classic ブランドの 320px 幅で横に ${doc}px あふれている`).toBe(0);
  }
});
