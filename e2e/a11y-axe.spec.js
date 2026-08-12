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

// ===== WCAG 1.4.3 (Contrast Minimum・AA): ブランド primary が白に対し 4.5:1 を満たす =====
// axe の `color-contrast` は **serious** で報告されるが、このリポジトリの a11y ゲートは
// **critical のみ**を対象にするため、contrast 不足は長らく素通りしていた (2026-08-10 に
// axe-core 4.13.0 で全ルートを無フィルタ走査して初めて可視化された)。
// 既定ブランド indigo は白背景に対し **4.467** で、要求 4.5:1 を **0.04 だけ** 下回っており、
// 1 ルートあたり 15〜59 ノードが violation になっていた (quiz は 63 ノード中 59 が
// 白文字 on primary のボタン)。各チャンネル -1 の rgb(98,101,240) で 4.527 となり AA を満たす。
//
// NOTE: axe 全体を gate にすると、**別クラスの未解決 violation** (muted text `#94a3b8` = 2.56 /
//   淡色チップ上の primary = 4.0) まで巻き込んで落ちる。それらは実際に色が変わる = C5 (設計) の
//   領域で、単独で決められない (research-application-policy.md に defer として実測値つきで記録済)。
//   ここでは **トークン単体の契約** だけを固定する — 将来パレットを触ったときに
//   「白に対する primary が AA を割る」退行だけは必ず赤くする、という最小で確実な層。
test('WCAG 1.4.3: 各ブランドの primary は白に対し 4.5:1 以上', async ({ page }) => {
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('.hero-section')).toBeVisible();

  const results = await page.evaluate(() => {
    const lin = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    const lum = (r, g, b) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
    const contrastVsWhite = (rgbTriplet) => {
      const [r, g, b] = rgbTriplet;
      const l = lum(r, g, b);
      return (1.0 + 0.05) / (l + 0.05);
    };
    const root = document.documentElement;
    const prev = root.getAttribute('data-brand');
    const out = [];
    for (const brand of ['classic', 'indigo']) {
      root.setAttribute('data-brand', brand);
      // --color-primary-rgb は "r, g, b" のカンマ区切り。computed から読むことで
      // CSS 変数の実効値 (brand ごとの上書き込み) を検査する。
      const raw = getComputedStyle(root).getPropertyValue('--color-primary-rgb').trim();
      const triplet = raw.split(',').map((n) => Number(n.trim()));
      out.push({ brand, raw, ratio: Math.round(contrastVsWhite(triplet) * 1000) / 1000 });
    }
    if (prev === null) { root.removeAttribute('data-brand'); } else { root.setAttribute('data-brand', prev); }
    return out;
  });

  for (const r of results) {
    expect(r.raw, `brand=${r.brand} の --color-primary-rgb を読めない`).toMatch(/^\d+\s*,\s*\d+\s*,\s*\d+$/);
    expect(
      r.ratio,
      `brand=${r.brand} (rgb ${r.raw}) の白背景コントラストが ${r.ratio} で AA (4.5:1) 未満`
    ).toBeGreaterThanOrEqual(4.5);
  }
});


// ===== ダークテーマの a11y (render-neutral critical) =====
// 上の A11Y_ROUTES ループは **ライトテーマでしか走っていなかった**。ダークは利用者が選べる
// 第一級のモードで、独自のトークン集合 (背景・前景・境界) を持ち、ARIA ではなく CSS 由来の
// 違反 (contrast など) が別物になる。にもかかわらず **a11y 被覆はゼロ**だった。
//
// テーマの適用は **アプリ本来の経路** (OS の colorScheme に追従する既定の theme='system') を
// 通す。`data-theme` を直接書き換えると、テーマ適用のロジックそのものが壊れていても
// テストが通ってしまう (内部状態を偽装した vacuous な検査になる)。
//
// NOTE: 判定は既存と同じ **render-neutral な rule の allowlist** に限定する。ダークの
//   color-contrast には未解決の違反が実在する (primary #6265f0 on #0f172a = 3.94 /
//   muted #64748b on #0f172a = 3.75 など) が、それらは実際に色が変わる = C5 (設計) の領域で、
//   research-application-policy.md に実測値つきで defer 記録済。ここでそれを gate にすると
//   「直せない理由が記録済みの既知課題」で CI が恒久的に赤くなる。
test('a11y axe: ダークテーマの全ルートに render-neutral critical 違反が無い', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'dark' });
  const offenders = [];
  for (const route of A11Y_ROUTES) {
    await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1, #content h2').first()).toBeVisible();
    // ダークが実際に効いていることを確認してから走査する (light のまま走らせると
    // 「ダークを検査したつもりで light を検査していた」vacuous な結果になる)
    const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    expect(bg, `${route}: OS 追従でダーク背景にならなかった (bg=${bg})`).toBe('rgb(2, 6, 23)');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'])
      .analyze();
    results.violations
      .filter((v) => A11Y_RENDER_NEUTRAL_RULES.includes(v.id))
      .forEach((v) => offenders.push(`${route}: ${v.id}(${v.nodes.length})`));
  }
  expect(offenders, `ダークテーマの render-neutral a11y violations: ${JSON.stringify(offenders)}`).toHaveLength(0);
});

// ===== ユーザー設定メディアの実効性 (forced-colors / prefers-contrast) =====
// style.css には `@media (forced-colors: active)` と `@media (prefers-contrast: more)` があるが、
// **この 2 つを検証している層が一つも無かった**:
//   - screenshot は通常モードで撮るので、どちらのブロックにも到達しない (かつ ADVISORY)
//   - Check 101 は forced-colors ブロックの **存在** を静的に強制するだけで、効果は見ない
//   - prefers-contrast は静的にも動的にも無被覆だった
// つまりブロックを丸ごと消しても全ゲートが緑のまま通る。どちらも Windows ハイコントラスト
// モードや弱視のユーザーにだけ効く面なので、壊れても開発者の画面には一切現れない。
//
// 対象は **button** で測る。`<select>` に programmatic focus すると `:focus-visible` が
// マッチせず (実測)、何を測っているのか分からなくなる。
async function focusRing(page) {
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  return page.evaluate(() => {
    const btn = document.querySelector('#content button');
    btn.focus();
    const cs = getComputedStyle(btn);
    const rs = getComputedStyle(document.documentElement);
    return {
      matchesFocusVisible: btn.matches(':focus-visible'),
      outlineColor: cs.outlineColor,
      outlineWidth: cs.outlineWidth,
      border: rs.getPropertyValue('--border-color').trim(),
      muted: rs.getPropertyValue('--text-muted').trim(),
    };
  });
}

test('ハイコントラストモードでフォーカスリングが system color になる (WCAG 1.4.1)', async ({ page }) => {
  await page.emulateMedia({ forcedColors: 'active' });
  const s = await focusRing(page);

  expect(s.matchesFocusVisible, 'そもそも :focus-visible が当たっていない (測定対象が誤り)').toBe(true);
  // 壊れ方の実測: フォールバックが無いと Chromium はブランド色を強制変換して
  // `rgba(5, 0, 73, 0.8)` = **半透明** の暗い青を描く。HCM で最も困る「薄くて見えない」状態。
  expect(s.outlineColor, `HCM でフォーカスリングが半透明になっている (${s.outlineColor}) — `
    + 'system color (CanvasText) の不透明な outline を補う必要がある').not.toContain('rgba');
  expect(s.outlineWidth, 'HCM でのフォーカスリングの太さが宣言と違う').toBe('2px');
});

test('高コントラスト設定で境界線と補助テキストが濃くなる (WCAG 1.4.11)', async ({ page }) => {
  const normal = await focusRing(page);
  await page.emulateMedia({ contrast: 'more' });
  const more = await focusRing(page);

  // 具体値をハードコードせず「通常時より変わっていること」で表現する
  // (ブランド色や token の値を変えたときに、意味のない false RED を出さないため)。
  expect(more.border, `高コントラスト設定で --border-color が変わっていない (${more.border})`)
    .not.toBe(normal.border);
  expect(more.muted, `高コントラスト設定で --text-muted が変わっていない (${more.muted})`)
    .not.toBe(normal.muted);
  // 補助テキストは境界線と同じ濃さまで寄せる設計 (薄いグレーのままだと読めない)
  expect(more.muted).toBe(more.border);
  expect(parseFloat(more.outlineWidth), 'フォーカスリングが太くなっていない')
    .toBeGreaterThan(parseFloat(normal.outlineWidth));
});

// ===== 長い本文に小見出しが実在すること (WCAG 1.3.1 / 2.4.6) =====
// 実測 (#1011 / #1012) で、読み物系の 2 ルートが **見出し H1 の 1 個だけ**だった:
//   #/quiz        本文 24,500 文字 / 章題 7 個が `<div class="quiz-section-title">`
//   #/ai-knowhow  本文  4,056 文字 / 節題 8 個が `<span class="text-head-lg">`
// 節タイトルは見た目だけ大きい div/span で描かれており、アクセシビリティツリーに見出しとして
// 現れない。スクリーンリーダーの主要なナビゲーション手段である「見出しジャンプ」で本文が
// 一切辿れない状態だった (section の role=region + aria-label でランドマーク移動は効く)。
//
// **axe は「長い本文に小見出しが無い」をルール化していない**ため、同 spec の axe スキャンは
// 緑のままだった (heading-order も『存在する見出しの順序』しか見ない)。捕捉層はこの test だけ。
// NOTE: test 題名は **静的リテラル**にする。テンプレートリテラルで組むと Check 379/397 が
//   静的セグメントしか parse できず、mutation の `test` アンカーを一意に解決できない
//   (安全網に登録できない = この test が守られない)。
async function measureLongRead(page, hash, heading) {
  await page.goto(`/${hash}`, { waitUntil: 'domcontentloaded' });
  // 他ルートの DOM を掴まないよう、このページ固有の見出しで待つ
  // (連続 goto + 汎用 `#content h1` 待ちは前ルートの描画で満たされてしまう)。
  await expect(page.locator('#content h1', { hasText: heading })).toBeVisible();

  return page.evaluate(() => {
    const content = document.getElementById('content');
    // 「見出しに見える」= 太字かつ本文より大きく、短いテキストを持つ葉要素。
    // 見出し要素でないものだけを違反として拾う。
    const looksLikeHeading = Array.from(content.querySelectorAll('span,div,p,strong')).filter(e => {
      if (e.querySelector('span,div,p,h1,h2,h3,h4,h5,h6')) { return false; }  // 葉のみ
      const t = (e.textContent || '').trim();
      if (!t || t.length > 40) { return false; }
      const cs = getComputedStyle(e);
      return parseFloat(cs.fontSize) >= 17 && parseInt(cs.fontWeight, 10) >= 600;
    }).map(e => `${e.tagName}.${(e.className || '').slice(0, 24)}:${e.textContent.trim().slice(0, 18)}`);

    return {
      textLength: content.textContent.length,
      headings: Array.from(content.querySelectorAll('h1,h2,h3,h4,h5,h6')).map(h => h.tagName),
      notHeadings: looksLikeHeading,
    };
  });
}

function assertLongReadStructure(s, label, minText) {
  // control: そもそも「長い読み物」であることを確かめる。短ければ見出しが少なくても問題ない
  // ので、この前提が崩れたまま緑になると何も検証していないことになる。
  expect(s.textLength, `${label}: 本文が短くなっている — この test の前提 (長い読み物) が崩れている`)
    .toBeGreaterThan(minText);
  expect(s.notHeadings, `${label}: 見出しに見えるのに見出し要素でない節タイトル: `
    + `${s.notHeadings.join(' / ')} — スクリーンリーダーの見出しジャンプで本文を辿れない`).toEqual([]);
  expect(s.headings.filter(t => t !== 'H1').length,
    `${label}: 見出しが H1 だけ (${s.headings.join(',')}) — 長い本文に構造が露出していない`)
    .toBeGreaterThanOrEqual(5);
}

test('quiz の章題が実際の見出し要素である', async ({ page }) => {
  assertLongReadStructure(await measureLongRead(page, '#/quiz', '問題集'), '#/quiz', 10000);
});

test('ai-knowhow の節タイトルが実際の見出し要素である', async ({ page }) => {
  assertLongReadStructure(await measureLongRead(page, '#/ai-knowhow', 'AI開発ノウハウ'), '#/ai-knowhow', 2000);
});

// ===== 同列カードの集合にリスト意味論があること (WCAG 1.3.1) =====
// 実測 (#1013) で、全ルートに `ul` / `ol` / `role=list` が **1 つも無かった**。
// projects は 18 件、apps は 5 件の同列カードが並ぶのに、スクリーンリーダーは
// 「リスト・18 項目」とアナウンスできず、リスト単位のジャンプ操作も効かない。
//
// **`<ul>` へ置き換えず ARIA ロールで与える**のが要点。grid レイアウトの `display` を
// 変えないので描画は構造上不変で、`<li>` 化して `display:list-item` とマーカーが入り
// grid が崩れる、という副作用も無い。
async function listSemantics(page, hash, heading) {
  await page.goto(`/${hash}`, { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: heading })).toBeVisible();
  return page.evaluate(() => {
    const list = document.querySelector('#content [role="list"]');
    return {
      hasList: !!list,
      items: list ? list.querySelectorAll(':scope > [role="listitem"]').length : 0,
      cards: document.querySelectorAll('#content article').length,
    };
  });
}

test('プロジェクト一覧がリストとしてアナウンスされる', async ({ page }) => {
  const s = await listSemantics(page, '#/projects', 'プロジェクト一覧');
  expect(s.hasList, 'カードの集合にリスト意味論が無い — SR が「リスト・N 項目」を伝えられない').toBe(true);
  // control: そもそもカードが並んでいることを確かめる (0 件なら何も検証していない)
  expect(s.cards, 'カードが 1 枚も無い — この test の前提が崩れている').toBeGreaterThanOrEqual(5);
  expect(s.items, `listitem の数 (${s.items}) がカード数 (${s.cards}) と一致しない`).toBe(s.cards);
});

test('アプリ一覧がリストとしてアナウンスされる', async ({ page }) => {
  const s = await listSemantics(page, '#/apps', 'アプリ');
  expect(s.hasList, 'カードの集合にリスト意味論が無い').toBe(true);
  expect(s.cards, 'カードが 1 枚も無い — この test の前提が崩れている').toBeGreaterThanOrEqual(3);
  expect(s.items, `listitem の数 (${s.items}) がカード数 (${s.cards}) と一致しない`).toBe(s.cards);
});

// ===== ラベルが入力欄に結び付いていること (WCAG 1.3.1 / 3.3.2) =====
// 実測 (#1014) で、**宙に浮いた `<label>` が 6 個**あった (ポモドーロの 集中/短休憩/長休憩、
// Settings の モード/対象/Demo)。`for` も無く control も包んでいないので、
//   - ラベル文字をクリック/タップしても何も起きない (通常はラベルで control を活性化できる)
//   - タップ標的が入力欄だけに縮む
// 入力欄側に `aria-label` があるため SR の読み上げ名は出ており、**axe も緑**だった
// (axe は「label 要素が孤立していること」をルール化していない)。捕捉層はこの test だけ。
//
// 「対象」だけは 3 つの checkbox をまとめる **グループ名**で、単一 control を指す `for` は
// 使えない。span + `role="group"` + `aria-labelledby` へ変えた (span は label と同じ inline
// なので描画は不変)。
// NOTE: test 題名は **静的リテラル**にする。テンプレートリテラルで組むと Check 379/397 が
//   静的セグメントしか parse できず mutation の `test` アンカーを一意に解決できない
//   (#1012 で同じ罠を踏み、今回も Check 379/397 が即座に検出してくれた)。
async function labelWiring(page, hash, heading) {
  await page.goto(`/${hash}`, { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: heading })).toBeVisible();
  return page.evaluate(() => {
    const labels = Array.from(document.querySelectorAll('#content label'));
    return {
      total: labels.length,
      dangling: labels.filter(l => !l.getAttribute('for') && !l.querySelector('input,select,textarea'))
        .map(l => (l.textContent || '').trim().slice(0, 14)),
      broken: labels.filter(l => l.getAttribute('for') && !document.getElementById(l.getAttribute('for')))
        .map(l => `${(l.textContent || '').trim().slice(0, 10)}→${l.getAttribute('for')}`),
    };
  });
}

function assertLabelWiring(s, label) {
  // control: そもそも label が存在するページであること
  expect(s.total, `${label}: label が 1 つも無い — この test の前提が崩れている`).toBeGreaterThanOrEqual(3);
  expect(s.dangling, `${label}: どの control にも結び付いていない label: ${s.dangling.join(' / ')}`).toEqual([]);
  expect(s.broken, `${label}: 存在しない id を指す label: ${s.broken.join(' / ')}`).toEqual([]);
}

test('ポモドーロに宙に浮いた label が無い', async ({ page }) => {
  assertLabelWiring(await labelWiring(page, '#/apps/pomodoro', 'ポモドーロ'), '#/apps/pomodoro');
});

test('Settings に宙に浮いた label が無い', async ({ page }) => {
  assertLabelWiring(await labelWiring(page, '#/settings', 'Settings'), '#/settings');
});

test('ポモドーロはラベル文字のクリックで入力欄が活性化する', async ({ page }) => {
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'ポモドーロ' })).toBeVisible();

  // NOTE: locator に `for` を含めない。`for` を外す mutation が「要素が見つからない」で
  //   落ちると、**ラベルで入力欄を活性化できたか**を検証できたのか帰属できなくなる。
  //   `label` 要素に絞って文字で引く (`getByText('長休憩')` はモード切替ボタンにも当たるため)。
  await page.locator('#content label').filter({ hasText: '長休憩' }).first().click();
  const active = await page.evaluate(() => (document.activeElement ? document.activeElement.id : null));
  expect(active, 'ラベルをクリックしても入力欄が活性化しない (for が結ばれていない)').toBe('pomo-setting-long');
});

// ===== 英語だけの塊に lang="en" が付くこと (WCAG 3.1.2 Language of Parts) =====
// 文書は `html lang="ja"`。日本語文字を 1 つも含まない塊をそのまま置くと、日本語の
// スクリーンリーダーが **英語を日本語の音韻で読み上げる**。実測 (#1020) では quiz だけで
// 49 箇所あり、うち "Core Knowledge & Tech Lead's View:" が 34 回繰り返されていた。
//
// 行の言語は data (js/quiz/*.js) 側で混在するので静的には決められない。描画時にその行の
// 文字種で判定する (日本語文字が無く Latin 文字がある → en)。AWS のサービス名のような
// 固有名詞にも付くが、英語音韻で読ませたいのはむしろ正しい。
//
// axe には該当ルールが無い (`html-lang-valid` は文書全体の lang しか見ない)。捕捉層はこの test だけ。
test('quiz の英語だけの塊に lang="en" が付く', async ({ page }) => {
  await page.goto('/#/quiz', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: '問題集' })).toBeVisible();

  const s = await page.evaluate(() => {
    const c = document.getElementById('content');
    const leaves = Array.from(c.querySelectorAll('h1,h2,h3,p,span,div,li,td,th'))
      .filter(e => !e.querySelector('h1,h2,h3,p,span,div,li,td,th'));
    const isEnglishOnly = (t) => t.length >= 12 && /^[\x20-\x7E]+$/.test(t) && /[A-Za-z]{4,}/.test(t);
    const JA = /[ぁ-んァ-ヶ一-龯]/;
    return {
      leafCount: leaves.length,
      taggedEn: c.querySelectorAll('[lang="en"]').length,
      // (a) 英語だけなのに lang 指定が無い塊
      untagged: leaves.filter(e => isEnglishOnly((e.textContent || '').trim()) && !e.closest('[lang="en"]'))
        .map(e => `${e.tagName}:${e.textContent.trim().slice(0, 30)}`),
      // (b) 逆方向 — 日本語を含むのに lang="en" が付いている (過剰適用)
      overTagged: Array.from(c.querySelectorAll('[lang="en"]'))
        .filter(e => JA.test(e.textContent || ''))
        .map(e => `${e.tagName}:${e.textContent.trim().slice(0, 30)}`),
    };
  });

  // control: そもそも描画されていること (0 件なら何も検証していない)
  expect(s.leafCount, '本文が描画されていない — この test の前提が崩れている').toBeGreaterThan(100);
  expect(s.taggedEn, `lang="en" が付いた要素が少なすぎる (${s.taggedEn} 件) — 付与経路のどれかが落ちている`).toBeGreaterThanOrEqual(20);

  expect(s.untagged, `英語だけなのに lang 指定が無い塊: ${s.untagged.slice(0, 4).join(' / ')}`).toEqual([]);
  expect(s.overTagged, `日本語を含むのに lang="en" が付いている (過剰適用): ${s.overTagged.slice(0, 4).join(' / ')}`).toEqual([]);
});

// ===== 固定の英語文字列にも lang="en" が付くこと (WCAG 3.1.2) =====
// #1020 は data 由来の行 (quiz) を描画時判定で処理した。こちらは **コードに直書きされた
// 英語文字列**で、判定の余地が無いのでリテラルに付ける。
// 対象は実測 (#1021) で見つかった 5 箇所 — home の英文キャプション / hero の CTA 2 つ /
// 「Verification & Evidence」見出し / About の h1。
test('固定の英語文字列に lang="en" が付く (home / about)', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();

  await expect(page.locator('#content p.text-caption')).toHaveAttribute('lang', 'en');
  await expect(page.locator('#content .cta-primary')).toHaveAttribute('lang', 'en');
  await expect(page.locator('#content .cta-secondary')).toHaveAttribute('lang', 'en');
  await expect(page.locator('#evidence-heading')).toHaveAttribute('lang', 'en');

  await page.goto('/#/about', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'About' })).toBeVisible();
  await expect(page.locator('#content h1')).toHaveAttribute('lang', 'en');

  // 逆方向: 日本語の見出しに lang="en" が付いていないこと (過剰適用の検出)
  const overTagged = await page.evaluate(() =>
    Array.from(document.querySelectorAll('#content [lang="en"]'))
      .filter(e => /[ぁ-んァ-ヶ一-龯]/.test(e.textContent || ''))
      .map(e => (e.textContent || '').trim().slice(0, 24)));
  expect(overTagged, `日本語を含むのに lang="en" が付いている: ${overTagged.join(' / ')}`).toEqual([]);
});
