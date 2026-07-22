const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;


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
// color-contrast / color-contrast-enhanced 等の未修正（baseline-gated or 別 increment）rule は
// analyze 結果に含まれても本 allowlist 外ゆえ無視する。
// 注: link-in-text-block (WCAG 1.4.1) は hero-meta のインラインリンクに下線を付与して修正済だが、
// 下線は pixel 変化 (非 render-neutral) ゆえ本 allowlist ではなく専用の computed-style 回帰
// テスト (末尾) で守る。
// 注: heading-order は render-neutral (DOM 構造で修正可・pixel 不変) ゆえ allowlist に含め
// enforce 済 — 以前この例示リストに誤って混じっていた doc-code drift を是正した。
const A11Y_RENDER_NEUTRAL_RULES = ['aria-valid-attr-value', 'select-name', 'button-name', 'label', 'page-has-heading-one', 'heading-order', 'aria-allowed-attr', 'aria-required-attr', 'aria-roles', 'duplicate-id-aria', 'aria-required-children', 'aria-required-parent'];
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


// ===== 7.1: プロジェクト詳細 (#/projects/:slug) の axe a11y (パラメータ化ルートの被覆) =====
// A11Y_ROUTES ループは静的ルートのみ (Check 110 が A11Y_ROUTES ↔ ALL_ROUTES の bijection を強制する
// ため slug 付きルートを配列に混ぜられない)。ProjectDetailPage は related links / architecture /
// metrics + 複数セクション見出しを持つ別 render 面で、従来どの axe 面にも被覆されず、h1(project.name)
// 直後に h2 を挟まず h3 が並ぶ見出しレベルスキップ (heading-order / WCAG 1.3.1) が逃れていた。
// drawer-open / palette-open と同じ standalone パターンで、default プロジェクト 'task-manager' の実
// slug を踏んで detail 面の render-neutral critical 違反ゼロを機械強制する (見出しを h3→h2 に戻すと
// heading-order で RED = 非 vacuity)。
test('a11y axe: project detail (#/projects/:slug) has no render-neutral critical violations', async ({ page }) => {
  await page.goto('/#/projects/task-manager');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(150);
  // 実プロジェクト詳細が描画されている (NotFound フォールバックでない) ことを確認してから scan
  await expect(page.locator('h1')).not.toHaveText('プロジェクトが見つかりません');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'])
    .analyze();
  const offenders = results.violations.filter(v => A11Y_RENDER_NEUTRAL_RULES.includes(v.id));
  expect(
    offenders,
    'project-detail render-neutral a11y violations: ' +
    JSON.stringify(offenders.map(v => `${v.id}(${v.nodes.length}): ${v.nodes[0] && v.nodes[0].html.slice(0, 100)}`))
  ).toHaveLength(0);
});

// ===== WCAG 1.4.1 Use of Color: hero-meta インラインリンクの下線アフォーダンス =====
// ホームの .hero-meta 段落内リンク (Zenn 記事) は周囲テキスト内で色 (.color-primary) のみで
// 判別され axe link-in-text-block (serious) を出していた。色トークンは変えず下線を付与して修正。
// text-decoration underline を除去すると本テストが RED (非 vacuity)。下線は pixel 変化ゆえ
// A11Y_RENDER_NEUTRAL_RULES ではなく本 computed-style テストで守る。
test('Hero-meta inline link is distinguishable by underline (WCAG 1.4.1, not color-only)', async ({ page }) => {
  await page.goto('/#/');
  await page.waitForLoadState('domcontentloaded');
  const link = page.locator('.hero-meta a').first();
  await expect(link).toBeVisible();
  const deco = await link.evaluate((el) => getComputedStyle(el).textDecorationLine);
  expect(deco).toContain('underline');
});
