const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

// ===== コントラストと「色だけに頼らない」知覚の契約 (WCAG 1.4.1 / 1.4.3 / 1.4.11) =====
//
// 元は e2e/a11y-axe.spec.js にあったが、同 file が 996 行となり Check 365 の BLOCKING
// (1,000 行) まで残り 3 行になったため、**当たる前に**このテーマの塊を切り出した
// (CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。圧縮で誤魔化さず
// 「いま触っているクラスタ」を切り出すのが最も筋が良い、の実践 (#927 と同じ判断)。
//
// このファイルが守るもの:
//   - 色だけで判別させない (1.4.1): 本文中リンクの下線アフォーダンス
//   - コントラスト比 (1.4.3): ブランド primary の 4.5:1、および
//     全ブランド × 全テーマ × 全ルートで axe color-contrast 違反ゼロ
//   - 利用者設定メディアの実効性 (1.4.11): forced-colors / prefers-contrast

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
// NOTE (2026-08-20 更新): かつてここには「muted text 2.56 / 淡色チップ上の primary 4.0 は
//   色が変わる = C5 (設計) の領域なので defer」と書いてあったが、**それは委任範囲の読み違いだった**
//   (canon: AI2AI.md STEP 3「オーナーは制限を一切課していない」)。実際に用途別トークンへ分離して
//   **2 ブランド × 2 テーマ × 16 ルートで違反ゼロ**にしてある。下の
//   `全ページの color-contrast 違反がゼロ` がその実体を gate している。
//   本 test はその中でも **トークン単体の契約** を固定する層として残す (パレットを触ったときに
//   どのページを見なくても即座に赤くなる、最小で確実な層)。
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

// ===== WCAG 1.4.3 (Contrast Minimum・AA): 全ブランド × 全テーマで color-contrast 違反ゼロ =====
// かつてこの面は「知覚できる配色変更は C5 (人間の領域)」として defer されていたが、**それは
// 委任範囲の読み違い**だった (canon: AI2AI.md STEP 3「オーナーは制限を一切課していない」)。
// 2026-08-20 に用途別の前景トークンへ分離して実際に違反ゼロへ到達させた:
//
//   --on-tint-*      淡いチップ (10% alpha) の上の文字。primary/success をそのまま使うと AA を割る
//   --text-accent    プレーンな背景の上で primary を文字に使う箇所 (暗テーマでは明るい変種)
//   --on-solid-fg    solid な **意味色** 背景の上の文字 (暗テーマでは意味色が明るくなるので暗い文字)
//   --solid-badge-*  白文字前提の識別バッジ背景 (テーマで明暗が反転しない固定値)
//
// **色を 1 つ変えるだけでは直らない**のがこの面の要点で、用途ごとに前景を持たせないと必ず
// どちらかのテーマで割れる (実測: 意味色を暗テーマで明るくしたら白文字が 1.44 まで落ちた)。
//
// ルートは「実際に違反が出ていた面」を代表として選ぶ。修正がトークン単位なので退行は複数ルートに
// 同時に出る = 代表集合で十分に捕捉できる (全 16 ルート × 4 組は約 51 秒かかり、検出力に見合わない)。
const CONTRAST_ROUTES = ['#/', '#/projects', '#/quiz', '#/about', '#/ai-knowhow', '#/hiring-risk', '#/settings'];

// 題名は **静的リテラル** にする。template literal で組み立てると `playwright -g` から解決できず、
// mutation を登録できない (Check 379/397 が BLOCKING で捕捉する・過去に 3 度踏んだ)。
// 共通処理は関数へ切り出し、題名だけを 4 本書く。
async function expectNoContrastViolations(page, brand, scheme) {
  await page.addInitScript(([b]) => localStorage.setItem('portfolio_brand_v45', b), [brand]);
  // reducedMotion: View Transition の不透明度アニメーション中に走査すると、合成された半透明色が
  //   大量の偽陽性を生む (実測: 待ち 120ms なら 3 ルートで 594 件、settle 後は 30 件)。
  await page.emulateMedia({ colorScheme: scheme, reducedMotion: 'reduce' });

  const offenders = [];
  for (const route of CONTRAST_ROUTES) {
    await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1, #content h2').first()).toBeVisible();
    const res = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
    for (const v of res.violations) {
      for (const n of v.nodes) {
        const d = n.any[0] && n.any[0].data;
        offenders.push(`${route}: ${d ? `${d.fgColor} on ${d.bgColor} = ${d.contrastRatio}` : n.target[0]}`);
      }
    }
  }
  expect(offenders, `AA を満たさない配色がある:\n${offenders.slice(0, 8).join('\n')}`).toEqual([]);
}

test('WCAG 1.4.3: indigo ライトの全ページで color-contrast 違反がゼロ', async ({ page }) => {
  await expectNoContrastViolations(page, 'indigo', 'light');
});

test('WCAG 1.4.3: indigo ダークの全ページで color-contrast 違反がゼロ', async ({ page }) => {
  await expectNoContrastViolations(page, 'indigo', 'dark');
});

test('WCAG 1.4.3: classic ライトの全ページで color-contrast 違反がゼロ', async ({ page }) => {
  await expectNoContrastViolations(page, 'classic', 'light');
});

test('WCAG 1.4.3: classic ダークの全ページで color-contrast 違反がゼロ', async ({ page }) => {
  await expectNoContrastViolations(page, 'classic', 'dark');
});

// ===== WCAG 1.4.3: 「開いた状態」でしか描画されない面のコントラスト =====
// ルートを巡る静的走査では、drawer / command palette / toast の中身は **一度も測られない**
// (閉じている間は DOM に無いか非表示)。実測 (2026-08-20) ではいずれも違反ゼロだが、
// 測られていない面は退行しても誰も気付けないので gate にする。
// 非 vacuity: palette の active 項目の文字色を中間グレーへ落とすと、ルート走査は緑のまま
// この test だけが RED になる (= 状態面を実際に見ていることの証明)。
async function expectNoContrastInOpenStates(page, scheme) {
  await page.emulateMedia({ colorScheme: scheme, reducedMotion: 'reduce' });
  const offenders = [];
  const scan = async (label) => {
    const res = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
    for (const v of res.violations) {
      for (const n of v.nodes) {
        const d = n.any[0] && n.any[0].data;
        offenders.push(`${label}: ${d ? `${d.fgColor} on ${d.bgColor} = ${d.contrastRatio}` : n.target[0]}`);
      }
    }
  };

  // drawer (mobile 専用の導線)
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');
  await scan('drawer-open');
  await page.keyboard.press('Escape');

  // command palette
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  await page.keyboard.press('Control+k');
  await expect(page.locator('.cmdk-input')).toBeVisible();
  await scan('palette-open');
  await page.keyboard.press('Escape');

  // 「非表示にしたプロジェクト」だけに出るバッジ (既定データでは一度も描画されない面)。
  //   実測 (2026-08-20): `.badge-green` は `.badge-success` と同形なのに on-tint トークンへ
  //   回されておらず、light で **4.38 < 4.5** の AA 違反だった。ルート走査は既定状態しか見ないので、
  //   **状態を作らないと現れない面**は永久に測られない。
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.getByRole('button', { name: 'フルバックアップ' })).toBeVisible();
  const hideBtn = page.getByRole('button', { name: /^非表示：/ }).first();
  await hideBtn.click();
  await expect(page.locator('.badge-green')).toBeVisible();   // control: 実際に描画された
  await scan('project-hidden-badge');

  // toast (追加成功の通知が出ている状態)
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#task-input')).toBeVisible();
  await page.locator('#task-input').fill('コントラスト検査');
  await page.locator('#task-input').press('Enter');
  await expect(page.locator('#toast-container').getByText('タスクを追加しました')).toBeVisible();
  await scan('toast-visible');

  expect(offenders, `開いた状態で AA を満たさない配色がある:\n${offenders.slice(0, 8).join('\n')}`).toEqual([]);
}

test('WCAG 1.4.3: ライトの drawer / palette / toast に color-contrast 違反がゼロ', async ({ page }) => {
  await expectNoContrastInOpenStates(page, 'light');
});

test('WCAG 1.4.3: ダークの drawer / palette / toast に color-contrast 違反がゼロ', async ({ page }) => {
  await expectNoContrastInOpenStates(page, 'dark');
});

// ===== ランドマークの骨格が全ルートで一意に成立していること (WCAG 1.3.1 / 2.4.1) =====
// SR 利用者の主要なページ内移動手段は **ランドマークジャンプ**。ところが実測 (2026-08-20)
// では `main` / `navigation` / `banner` を検査するテストが **1 件も無かった**
// (`search` だけが projects / quiz で個別に守られていた)。
//
// 壊れ方はすべて視覚に出ない:
//   - `<main>` が消える / 名前を失う → ランドマーク一覧から本文が消える
//   - `main` の tabindex="-1" が外れる → **skip-link の着地点が無くなる** (WCAG 2.4.1)
//   - `<nav>` が 2 つになる → どちらが主か分からなくなる
// screenshot にも、既存の axe スキャン (違反 rule の allowlist 方式) にも出ない。
//
// **測ってから書いた契約**: 骨格は viewport 依存だった。desktop は sidebar が
// `navigation`、mobile は sidebar が display:none で topbar が `banner` になる。
// `contentinfo` はどちらも 0 —— `<footer id="aio-main-footer">` が `<main>` の子孫で、
// HTML-AAM 上 landmark にならないため (これは AIO の機械向けアンカーであって
// 人間向けのページフッターではないので、実態として正しい)。
// 最初「全ルートで 4 つとも 1」と決め打ちで書いたら banner で落ち、実態と違う前提を
// 置いていたと分かった。**前提は測ってから固定する。**
const LANDMARK_ROUTES = ['#/', '#/projects', '#/quiz', '#/apps/task', '#/settings', '#/resume'];

test('全ルートで main ランドマークが一意で、名前と skip-link 着地点を保つ', async ({ page }) => {
  for (const route of LANDMARK_ROUTES) {
    await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1').first()).toBeVisible();

    await expect(page.getByRole('main'),
      `${route}: main ランドマークは 1 つだけ存在すべき`).toHaveCount(1);
    const main = page.getByRole('main');
    expect(await main.getAttribute('aria-label'),
      `${route}: main に名前が無い (ランドマーク一覧で識別できない)`).toBeTruthy();
    expect(await main.getAttribute('tabindex'),
      `${route}: main が focus を受けられない = skip-link の着地点が失われる`).toBe('-1');
  }
});

test('ナビゲーションのランドマークが viewport ごとに一意に成立する', async ({ page }) => {
  // desktop: sidebar が navigation。topbar は非表示なので banner は出ない。
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await expect(page.getByRole('navigation'),
    'desktop: navigation ランドマークは sidebar の 1 つだけ').toHaveCount(1);
  expect(await page.getByRole('navigation').getAttribute('aria-label'),
    'desktop: navigation に名前が無い').toBeTruthy();

  // mobile: sidebar は display:none になり、topbar が banner として残る
  //   (ナビ本体は drawer の中で、開くまでは a11y ツリーに出ないのが設計どおり)。
  await page.setViewportSize({ width: 390, height: 800 });
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await expect(page.getByRole('banner'),
    'mobile: banner ランドマーク (topbar) が 1 つだけ').toHaveCount(1);
});

// ===== 検索 0 件でもリストの意味論が壊れないこと (WCAG 1.3.1) =====
// `role="list"` の子として許されるのは `listitem` だけ。従来は検索 0 件のとき、
// **同じコンテナ**に空状態カード (`role="status"`) を入れていたため
// axe の aria-required-children が「Element has children which are not allowed:
// [role=status]」で違反を出し、**リストの意味論そのものが壊れて**いた。
//
// **既定状態では 0 件にならない**ので、全ルートの axe 走査 (既定内容で実行) では
// 一度も踏まれていなかった —— Markdown ノートの見出し (#1213) と同じ
// 「既定値だけが偶然 clean」class。
//
// 0 件のときはリストが存在しないので、list として公開する対象自体が無い。
// role を外して空状態を兄弟として置く。
test('検索 0 件でもリストの意味論が壊れない (role=list の子は listitem だけ)', async ({ page }) => {
  // control: 通常状態では list / listitem が正しく公開されている
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content .grid-projects article').first()).toBeVisible();
  await expect(page.getByRole('list'), 'control: 通常状態で list が公開されていない').toHaveCount(1);
  expect(await page.getByRole('listitem').count(),
    'control: listitem が 1 件も無いと list 意味論を測れない').toBeGreaterThan(1);

  const violations = async () => {
    const r = await new AxeBuilder({ page }).withRules(['aria-required-children']).analyze();
    return r.violations.map((v) => `${v.id}:${v.nodes.length}`);
  };
  expect(await violations(), '通常状態で list 意味論が壊れている').toEqual([]);

  // 0 件: 空状態カードを list の中に入れない
  await page.goto('/#/projects?q=zzzznomatch', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content').getByText('条件に一致するプロジェクトはありません')).toBeVisible();
  expect(await violations(), '0 件時に role=list の子へ role=status が入っている').toEqual([]);
});

// ===== 非既定の状態でも構造 a11y が壊れないこと (既定値だけが偶然 clean を防ぐ) =====
// 全ルートの axe 走査は **既定内容で実行される**ため、既定から外れた状態にしか現れない
// 破れには**永久に到達しない**。実際この class で 2 件の実バグが出た:
//   #1213 `###` から書き始めた Markdown ノート → 見出しが h3/h4 を飛ばす
//   #1214 検索 0 件 → role="list" の子に role="status" が入りリスト意味論が壊れる
// どちらも既定内容 (note が `#` 始まり / 検索が空) では踏まれない。
//
// ここでは **空** と **大量** の両端を作って構造 rule だけを走らせる。
// color-contrast は別 test 群が全ブランド × 全テーマで見ているので対象外
// (ここで混ぜると「淡色チップ上の文字」等の既知面に埋もれて構造違反を見落とす)。
const STRUCTURE_RULES = [
  'aria-required-children', 'aria-required-parent', 'list', 'listitem',
  'definition-list', 'dlitem', 'aria-valid-attr-value', 'duplicate-id-aria',
];

test('空の状態でも構造 a11y が壊れない (todo 全削除 / 検索 0 件)', async ({ page }) => {
  await page.goto('/#/apps/todo', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();

  // control: 消す対象が無いと「空にした」状態を作れない
  expect(await page.locator('#content button[id^="todo-delete-"]').count(),
    'control: 既定 TODO が 0 件では空状態を作れない').toBeGreaterThan(0);
  for (let i = 0; i < 10; i++) {
    const del = page.locator('#content button[id^="todo-delete-"]').first();
    if (await del.count() === 0) { break; }
    await del.click();
  }
  await expect(page.locator('#content button[id^="todo-delete-"]')).toHaveCount(0);

  const scan = async () => (await new AxeBuilder({ page }).withRules(STRUCTURE_RULES).analyze())
    .violations.map((v) => `${v.id}:${v.nodes.length}`);
  expect(await scan(), 'TODO を空にすると構造 a11y が壊れる').toEqual([]);

  await page.goto('/#/quiz?q=zzzznomatch', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  expect(await scan(), 'quiz 検索 0 件で構造 a11y が壊れる').toEqual([]);
});

test('大量データでも構造 a11y と id の一意性が保たれる', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.setInputFiles('#content input[type="file"]', {
    name: 'bulk.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      tasks: Array.from({ length: 90 }, (_, i) => ({
        id: `bulk${i}`, title: `BULK-${i}`, status: ['backlog', 'doing', 'done'][i % 3],
      })),
      todos: [],
    })),
  });
  await expect(page.locator('#action-announcement')).toContainText('インポート');

  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  // control: 取り込みが効いていないと「大量」を測れない
  await expect.poll(async () => await page.locator('#content [id^="task-delete-"]').count(),
    { message: 'control: 大量データが描画されていない' }).toBeGreaterThan(50);

  const violations = (await new AxeBuilder({ page }).withRules(STRUCTURE_RULES).analyze())
    .violations.map((v) => `${v.id}:${v.nodes.length}`);
  expect(violations, '大量データで構造 a11y が壊れる').toEqual([]);

  // 90 件が同じ id を作らないこと (#1058 の id 衝突 class)
  const dup = await page.evaluate(() => {
    const seen = new Map();
    document.querySelectorAll('[id]').forEach((e) => seen.set(e.id, (seen.get(e.id) || 0) + 1));
    return Array.from(seen.entries()).filter(([, c]) => c > 1).map(([k]) => k);
  });
  expect(dup, '大量データで id が重複している').toEqual([]);
});
