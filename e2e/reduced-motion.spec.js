const { test, expect } = require('@playwright/test');

// ===== モーション低減 (prefers-reduced-motion) の behavior gate =====
// このサイトの動きは 2 系統ある —— home の in-page ジャンプ (scrollIntoView) と、
// ルート遷移の View Transition (ページ全体のクロスフェード)。前庭障害のある利用者には
// どちらも実害があるので、reduce を選んだときに **本当に動かない** ことを固定する。
//
// navigation-a11y.spec.js から切り出した理由は肥大化の**予防**。同 file が 917 行となり
// 早期警告 (900) を超えたため、Check 365 の BLOCKING (1,000 行) を踏む前にこのテーマの
// 塊を移した (CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。
// mutation の `test` フィールドは title 一致ゆえ file 移動の影響を受けない。

// ===== WCAG 2.3.3 / 2.4.3: home の in-page ジャンプボタン =====
// home の「まずはこの3つだけ見てください」1 枚目のボタンは #evidence-heading へ 1,000px 超
// スクロールする。ここには 2 つの欠陥があった (2026-08-11 #993 で実測して発見):
//
//  (1) WCAG 2.3.3 — `scrollIntoView({behavior:'smooth'})` は **behavior を明示している**ため、
//      CSSOM-View 仕様により CSS の `scroll-behavior` は参照されない。つまり style.css の
//      `@media (prefers-reduced-motion: reduce) { scroll-behavior: auto !important }` は
//      **この呼び出しには効かない**。実測でも reduce / no-preference でスクロール曲線が
//      完全に一致していた (t0=0 → t150≈475 → t600≈1075)。
//      紛らわしいのは、同じ実測で `window.scrollTo(0, 0)` は reduce のとき即時に完了しており、
//      **CSS の reduce override 自体は正しく働いていた**こと。効かないのは明示呼び出しだけ。
//
//  (2) WCAG 2.4.3 — `scrollIntoView` は viewport を動かすだけで focus は動かない。移動先が
//      見えないユーザーには何も起きず、キーボードユーザーの次の Tab は画面外へ去った
//      ボタンから続いてしまう。
//
// どちらも fatal を出さず、視覚 baseline は 1280x720 の 1 枚だけ (かつ ADVISORY) なので、
// **捕捉層はこの behavior test しかない**。静的側は Check 421 が (1) を構造的に守る。
test('WCAG 2.3.3: reduced-motion では in-page ジャンプが即時になる (アニメーションしない)', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();

  const btn = page.getByRole('button', { name: 'ケーススタディセクションへ移動' });
  await expect(btn).toBeVisible();

  // NOTE: 「アニメーションしないこと」は *不変性* ではなく「click と同じ tick で完了する」
  // という一点の観測なので poll を使わない (poll は最初の観測で成立した瞬間に成功するため
  // アニメーションの途中を拾って誤って緑になりうる)。click 直後の同期読み 1 回で判定する。
  const scrolled = await page.evaluate(() => {
    window.scrollTo(0, 0);
    // NOTE: aria-label は WCAG 2.5.3 で可視テキストを先頭に含む形へ変えた (#1091) ので
    // 完全一致セレクタは使わない。前方一致で「行き先」部分だけを見る。
    document.querySelector('[aria-label*="ケーススタディセクションへ移動"]').click();
    return window.scrollY;   // 即時なら既に目的地、smooth なら 0 付近のまま
  });

  expect(
    scrolled,
    `reduced-motion なのに click 直後の scrollY が ${scrolled}px しか進んでいない ` +
    '= アニメーションしている (WCAG 2.3.3)。behavior を明示すると CSS の scroll-behavior は ' +
    '参照されないので、JS 側で matchMedia を見て behavior:\'auto\' に落とす必要がある'
  ).toBeGreaterThan(300);
});

test('WCAG 2.4.3: in-page ジャンプが移動先へ focus を移す', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();

  const btn = page.getByRole('button', { name: 'ケーススタディセクションへ移動' });
  await expect(btn).toBeVisible();
  await btn.click();

  // NOTE: toBeFocused() は並列ワーカーで document が inactive になり間欠 RED になるため使わない
  // (playwright.config.cjs の落とし穴表を参照)。activeElement を evaluate で直接読む。
  await expect
    .poll(async () => page.evaluate(() => (document.activeElement ? document.activeElement.id : null)))
    .toBe('evidence-heading');

  // スクロールも実際に到達していること (focus の preventScroll でスクロールを打ち消していない)
  const y = await page.evaluate(() => window.scrollY);
  expect(y, 'focus は移ったがスクロールしていない (preventScroll が移動そのものを潰している)').toBeGreaterThan(300);
});

// ===== reduced-motion では実際の View Transition を走らせない (三層防御) =====
// WCAG 2.3.3 / 前庭障害。ルート遷移はページ全体がクロスフェードする最大のモーション源。
// 防御は 3 層ある (実測で確認):
//   1. render() の `!prefersReducedMotion` ガード — そもそも呼ばない
//   2. startViewTransitionProxy の reduce 判定 — **素の API を直接呼ばれても**
//      native へ委譲せず callback を同期実行して duck-typed な戻り値を返す
//      (「AI 実装が executeSafeTransition を経由せず直接呼ぶ」ことを想定した設計・Check 43b)
//   3. style.css の `::view-transition-*` animation: none (最後の安全網)
//
// 実測 (2026-08-17): 層 1 を丸ごと外しても behavior e2e 390 件が**全て緑**だった。
// つまりこの契約はどの層からも見られていなかった。
//
// **測定の要点**: `document.startViewTransition` を init script で包んでも、proxy が
// install 時に `.bind(document)` で捕まえるのは *その包み* なので、**proxy が native へ
// 委譲したときだけ**カウントが増える。つまりこのカウンタは「実際にアニメーションが
// 走ったか」を測っている (層 1 と層 2 のどちらが効いても 0)。冗長な層があるときは
// 「効いている行」を狙わないと RED にならない。
//
// **非 vacuity の実測 (2026-08-17)**:
//   - ルート遷移テスト: 層 1 だけ / 層 2 だけを外しても**もう片方が受けるので緑のまま**。
//     両方を外すと RED。つまりこれは「どちらか一方が生きていること」を保証する
//     defense-in-depth のテストで、単一 mutation では RED にできない (だから mutation は
//     登録していない —— RED を実測できないものは安全網に混ぜない)。
//   - 素の API テスト: 層 2 の reduce 判定を外すと**単独で** RED。こちらを mutation に登録した。
async function countViewTransitions(page, motion) {
  await page.emulateMedia({ reducedMotion: motion });
  await page.addInitScript(() => {
    window.__vtCalls = 0;
    window.__vtSupported = typeof document.startViewTransition === 'function';
    if (window.__vtSupported) {
      const orig = document.startViewTransition;
      document.startViewTransition = function (cb) { window.__vtCalls++; return orig.call(this, cb); };
    }
  });
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();
  for (const hash of ['#/projects', '#/about', '#/apps']) {
    await page.evaluate((h) => { location.hash = h; }, hash);
    await page.waitForTimeout(400);
  }
  return page.evaluate(() => ({ supported: window.__vtSupported, calls: window.__vtCalls }));
}

test('WCAG 2.3.3: reduced-motion ではルート遷移アニメーションを起動しない', async ({ page }) => {
  const reduced = await countViewTransitions(page, 'reduce');
  // control: ブラウザが View Transition を持っていなければ以降は何も検査しない
  expect(reduced.supported, 'control: このブラウザに startViewTransition が無い').toBe(true);
  expect(reduced.calls,
    'reduced-motion なのに View Transition を起動している (WCAG 2.3.3)。'
    + 'CSS 側の安全網で見た目の動きは消えるが、スナップショット取得と一時的な inert は残る'
  ).toBe(0);
});

test('通常設定ではルート遷移アニメーションが実際に動いている (前テストの control)', async ({ page }) => {
  // 上のテストが「機能自体が壊れて 0 回」でも緑になるのを防ぐ対の観測。
  const normal = await countViewTransitions(page, 'no-preference');
  expect(normal.supported).toBe(true);
  expect(normal.calls,
    'ルート遷移で View Transition が一度も起動していない — reduce 側の 0 回が '
    + '「reduce を尊重している」ではなく「機能が死んでいる」ことを意味してしまう'
  ).toBeGreaterThan(1);
});

test('WCAG 2.3.3: 素の startViewTransition を直接呼んでも reduced-motion では実遷移しない', async ({ page }) => {
  // proxy (層 2) の存在理由そのもの: 「executeSafeTransition を経由せず素の API を直接呼ぶ」
  // 経路でも reduce が尊重されること。層 1 を通らないのでこの層だけを単独で検証できる。
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.addInitScript(() => {
    window.__nativeVT = 0;
    const orig = document.startViewTransition;
    if (typeof orig === 'function') {
      document.startViewTransition = function (cb) { window.__nativeVT++; return orig.call(this, cb); };
    }
  });
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();

  const r = await page.evaluate(async () => {
    let ran = false;
    const t = document.startViewTransition(() => { ran = true; });
    // proxy は duck-typed に ready / finished / updateCallbackDone / skipTransition を返す契約
    const shape = !!(t && t.ready && t.finished && t.updateCallbackDone && typeof t.skipTransition === 'function');
    await t.finished;
    return { ran, shape, native: window.__nativeVT, proxied: /startViewTransitionProxy/.test(document.startViewTransition.name) };
  });

  expect(r.proxied, 'control: startViewTransition が proxy に差し替わっていない (Check 43b)').toBe(true);
  expect(r.ran, 'reduce 経路で callback が実行されない — DOM 更新そのものが失われる').toBe(true);
  expect(r.shape, 'duck-typed な戻り値の契約が壊れている (呼び出し側の .finished が undefined になる)').toBe(true);
  expect(r.native,
    'reduced-motion なのに native の View Transition へ委譲している (WCAG 2.3.3)。'
    + 'proxy は素の API を直接呼ばれても reduce を尊重する層なので、ここが抜けると '
    + 'executeSafeTransition を経由しない実装から動きが漏れる').toBe(0);
});
