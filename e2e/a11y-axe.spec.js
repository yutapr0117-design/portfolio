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

// ===== ダークテーマの a11y (render-neutral critical) =====
// 上の A11Y_ROUTES ループは **ライトテーマでしか走っていなかった**。ダークは利用者が選べる
// 第一級のモードで、独自のトークン集合 (背景・前景・境界) を持ち、ARIA ではなく CSS 由来の
// 違反 (contrast など) が別物になる。にもかかわらず **a11y 被覆はゼロ**だった。
//
// テーマの適用は **アプリ本来の経路** (OS の colorScheme に追従する既定の theme='system') を
// 通す。`data-theme` を直接書き換えると、テーマ適用のロジックそのものが壊れていても
// テストが通ってしまう (内部状態を偽装した vacuous な検査になる)。
//
// NOTE (2026-08-20 更新): 判定は render-neutral な rule の allowlist に限定する。
//   ダークの color-contrast はかつて未解決 (primary 3.94 / muted 3.75) で「C5 ゆえ defer」と
//   書いてあったが、**それは委任範囲の読み違い**で、現在は用途別トークンへ分離して
//   **違反ゼロ**にしてある。contrast は下の専用 test が全ブランド × 全テーマで gate する。
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

// data 由来のテキスト (利用者が編集できる profile / project) にも同じ判定が効くこと。
// 判定は js/pure-utils.js の `langOfText` に一本化されており、quiz / home / resume の
// 3 箇所が注入で共有する (1 行の正規表現でもコピーすれば invariant の二重化になる)。
test('data 由来のテキストにも lang="en" が付く (home badge / resume 職種)', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();
  await expect(page.locator('#content span.badge-primary').first()).toHaveAttribute('lang', 'en');

  await page.goto('/#/resume', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Resume' })).toBeVisible();
  await expect(page.locator('#content h2').first()).toHaveAttribute('lang', 'en');

  // 英語だけなのに lang 指定が無い塊が resume に残っていないこと
  const remaining = await page.evaluate(() => {
    const c = document.getElementById('content');
    return Array.from(c.querySelectorAll('h1,h2,h3,p,span,div,li,td,th,button'))
      .filter(e => !e.querySelector('h1,h2,h3,p,span,div,li,td,th,button'))
      .filter(e => { const t = (e.textContent || '').trim(); return t.length >= 12 && /^[\x20-\x7E]+$/.test(t) && /[A-Za-z]{4,}/.test(t); })
      .filter(e => !e.closest('[lang="en"]'))
      .map(e => `${e.tagName}:${e.textContent.trim().slice(0, 24)}`);
  });
  expect(remaining, `英語だけなのに lang 指定が無い: ${remaining.join(' / ')}`).toEqual([]);
});

// ===== 絞り込みの件数は polite な status で伝えること (WCAG 4.1.3 / ARIA APG) =====
// 従来 task/todo の件数は `announce()` 経由で `#action-announcement`
// (`aria-live="assertive"`) へ書かれており、絞り込むたびに **スクリーンリーダーの読み上げを
// 割り込んで**いた。assertive は緊急 (エラー等) に限るのが ARIA APG の作法で、件数は status。
// ProjectsPage / QuizPage は既に polite なローカル status を持っており、**task/todo だけが
// assertive** という非対称だった (実測 #1031)。
test('絞り込みの件数が polite な status でアナウンスされる (assertive を使わない)', async ({ page }) => {
  for (const [hash, heading, sel, expected] of [
    ['#/apps/task', 'タスク', '#task-filter-priority', /優先度: High \d+ 件/],
    ['#/apps/todo', 'TODO', '#todo-filter', /TODO: 未完了 \d+ 件/],
  ]) {
    await page.goto(`/${hash}`, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1', { hasText: heading })).toBeVisible();

    const assertiveBefore = await page.evaluate(() =>
      (document.getElementById('action-announcement') || {}).textContent);

    // キーボードで選択肢を変えたときと同じ「focus したまま change が飛ぶ」形
    await page.evaluate((s) => {
      const el = document.querySelector(s);
      el.focus();
      el.value = Array.from(el.options).map(o => o.value)[1];
      el.dispatchEvent(new Event('change', { bubbles: true }));
    }, sel);
    await page.waitForTimeout(400);

    const r = await page.evaluate(() => ({
      assertive: (document.getElementById('action-announcement') || {}).textContent,
      polite: Array.from(document.querySelectorAll('#content [role="status"][aria-live="polite"]'))
        .map(e => e.textContent.trim()),
    }));

    expect(r.polite.join(' | '), `${hash}: polite な status に件数が出ていない`).toMatch(expected);
    expect(r.assertive, `${hash}: 件数が assertive 領域へ書かれ、SR の読み上げを割り込んでいる`)
      .toBe(assertiveBefore);
  }
});

// ===== 通知は目的別の小さな領域が担う（#content 全体を live region にしない） =====
// `#content` にはかつて `aria-live="polite"` が付いていた（根拠コメントも decision record も
// 無く、"全体微改善" というコミットで入っていた）。ここは**ページ本文そのもの**で quiz では
// 24,500 文字あり、ルート遷移や State 更新のたびに丸ごと差し替わる。大きな live region は
// スクリーンリーダーが本文全体を読み直す "chatty" なアンチパターンで、**ポモドーロ稼働中は
// 毎秒再描画される**ため特に害が大きい (#1032)。
//
// 代わりに通知は目的別の小さな専用領域が担う。この test は「外したことで通知能力が
// 失われていない」ことを同時に確かめる（control）。
test('#content は live region ではなく、通知は専用領域が担う', async ({ page }) => {
  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();

  // (1) #content 自体は live region でない
  const contentLive = await page.evaluate(() =>
    document.getElementById('content').getAttribute('aria-live'));
  expect(contentLive, '#content が live region になっている (本文全体が読み直される)').toBeNull();

  // (2) control: ルート遷移の通知は生きている
  await page.goto('/#/about', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'About' })).toBeVisible();
  await expect(page.locator('#page-announcement')).toHaveText(/ページを表示しています/);

  // (3) control: 状態メッセージ (件数) の通知も生きている
  await page.goto('/#/apps/todo', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'TODO' })).toBeVisible();
  await page.getByLabel('TODO を絞り込み').selectOption('completed');
  await expect(page.locator('#content [role="status"][aria-live="polite"]')).toHaveText(/TODO: 完了 \d+ 件/);
});


// ===== 実行時の aria-* idref が実在要素に解決する (静的 Check 392 の動的面) =====
// `aria-labelledby` / `aria-describedby` / `aria-controls` / `aria-activedescendant` /
// `aria-errormessage` / `aria-owns` は **id 参照**であり、指す先が無いと支援技術は
// その関連付けを黙って無視する —— 画面上は何も変わらず、axe にも該当ルールが無いため
// **どの層も捕捉しない**。Check 392 は静的に idref を検証するが、**描画時に組み立てられる
// id**（`cmdk-opt-<i>` のようにループで採番されるもの、条件付きで付け外しされるもの）は
// ソースを読んでも解決できない。実際 #997 では `aria-controls` を変数化した瞬間に
// Check 392 が false RED になっており、静的検査の射程はそこで尽きている。
//
// 危ないのは静止状態より **一過性の状態** —— palette を開いた瞬間、候補がゼロになった瞬間、
// drawer を開いた瞬間、検証エラーが出た瞬間。これらは DOM が入れ替わるので、参照先だけが
// 消えて属性が残る形の壊れ方をする。全 16 ルート + 主要な一過性状態で走査する。
//
// 非 vacuity: 実在しない id を指す要素を注入すると検出されることを control で実証済
// (probe 実測: `DIV[aria-controls=nonexistent-target-xyz]` を検出)。
const IDREF_ATTRS = ['aria-labelledby', 'aria-describedby', 'aria-controls',
  'aria-activedescendant', 'aria-errormessage', 'aria-owns'];

async function danglingIdrefs(page) {
  return page.evaluate((attrs) => {
    const out = [];
    document.querySelectorAll('*').forEach((el) => attrs.forEach((a) => {
      const v = el.getAttribute(a);
      if (!v) { return; }
      v.split(/\s+/).filter(Boolean).forEach((id) => {
        if (!document.getElementById(id)) { out.push(el.tagName + '[' + a + '="' + id + '"]'); }
      });
    }));
    return [...new Set(out)];
  }, IDREF_ATTRS);
}

const IDREF_ROUTES = ['', '#/projects', '#/quiz', '#/about', '#/resume', '#/contact',
  '#/role-split', '#/hiring-risk', '#/ai-knowhow', '#/apps', '#/apps/task', '#/apps/todo',
  '#/apps/notes', '#/apps/ai', '#/apps/pomodoro', '#/settings'];

test('全ルートの aria-* id 参照が実在要素へ解決する', async ({ page }) => {
  for (const route of IDREF_ROUTES) {
    await page.goto('/' + route, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1').first()).toBeVisible();
    expect(await danglingIdrefs(page), `${route || 'home'} に解決しない aria-* id 参照がある`).toEqual([]);
  }
});

test('palette / drawer / 検証エラーの一過性状態でも aria-* id 参照が解決する', async ({ page }) => {
  // command palette: 開いた直後 → 矢印で active option を指した状態 → 候補ゼロ
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.keyboard.press('Control+k');
  const cmdkInput = page.locator('[role="combobox"]').first();
  await expect(cmdkInput).toBeVisible();
  expect(await danglingIdrefs(page), 'palette を開いた状態').toEqual([]);

  await page.keyboard.press('ArrowDown');
  // control: 矢印操作で active option が実際に指されていること (指していなければ何も検査していない)
  await expect(cmdkInput).toHaveAttribute('aria-activedescendant', /.+/);
  expect(await danglingIdrefs(page), 'palette で active option を指した状態').toEqual([]);

  await cmdkInput.fill('zzzzzz-no-match-expected');
  // control: 候補ゼロの表示になっていること (候補が残っていればこの状態を測れない)。
  // 空表示も <li> として描かれるので role="option" で数える。
  await expect(page.locator('#cmdk-listbox li[role="option"]')).toHaveCount(0);
  await expect(page.locator('.cmdk-empty')).toBeVisible();
  expect(await danglingIdrefs(page), 'palette の候補がゼロの状態').toEqual([]);
  await page.keyboard.press('Escape');

  // mobile drawer
  await page.setViewportSize({ width: 390, height: 780 });
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');
  expect(await danglingIdrefs(page), 'drawer を開いた状態').toEqual([]);

  // 検証エラー (aria-errormessage が出る経路)
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#settingsNewName')).toHaveAttribute('aria-invalid', 'true');
  expect(await danglingIdrefs(page), '検証エラーが出ている状態').toEqual([]);
});


// ===== 設計判断 quiz のステークホルダー意見がリストとして読める =====
// 1 つの問いに 2〜3 人分の意見が並ぶ。リスト意味論が無いと SR 利用者は
// **「意見が何件あるか」も「どこからどこまでが 1 人の発言か」も掴めず**、項目単位の
// 移動もできない (視覚的には引用の体裁で区切りが分かる)。axe には該当ルールが無く、
// この e2e 以外に捕捉層が無い。#1013 で projects / apps のカードへ同じことをしたのと同型。
//
// **描画不変にするため wrapper は `display: contents`** にしてある。素の div を挟むと
// ブロックが 1 段増えてページ高が変わった (実測: 5919 → 5823px)。display:contents なら
// レイアウトから外れつつロールは残る —— ページ高が完全に一致することと、
// アクセシビリティツリーに list/listitem が出ることの両方を実測で確認済み。
test('設計判断 quiz のステークホルダー意見がリストとして公開される', async ({ page }) => {
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: '設計判断' })).toBeVisible();

  // control: 意見そのものが描画されている (0 件ならリスト化を測れない)
  const quotes = page.locator('.quiz-stakeholder-quote');
  expect(await quotes.count(), 'control: ステークホルダーの意見が描画されていない').toBeGreaterThan(1);

  // アクセシビリティツリー経由で解決する (getByRole は role 計算を通す)
  const items = await page.getByRole('listitem').count();
  expect(items, 'ステークホルダーの意見が listitem として公開されていない').toBe(await quotes.count());
  expect(await page.getByRole('list').count(),
    'ステークホルダーの意見を束ねる list が無い').toBeGreaterThan(0);

  // 描画不変の担保: wrapper がレイアウトへ影響しない (display:contents)
  const display = await page.evaluate(() => {
    const li = document.querySelector('[role="listitem"]');
    return li ? getComputedStyle(li.parentElement).display : null;
  });
  expect(display, 'list wrapper がレイアウトへ影響している (描画が変わる)').toBe('contents');
});


// ===== 同質な項目の並びがリストとして読める (記事シリーズ / プロジェクト行) =====
// SR 利用者にとって「何件あるか」「どこからどこまでが 1 項目か」は、視覚利用者が
// カードの体裁から一目で得ている情報。role が無いとそれが得られず、項目単位の移動もできない。
// axe には「同質な並びなのにリストでない」を検出するルールが無く、この e2e 以外に捕捉層が無い。
// #1013 (projects / apps カード) → #1076 (quiz の意見) に続く同じ class の 3 例目。
//
// **既存のラッパーへ role を足すだけ**にしてあるので DOM は増えず描画は不変
// (#1076 で新しい div を挟んだらページ高が変わったため、ここは要素を追加しない形にした)。
// ページ高が変更前と完全一致することを実測済 (home 3414 / settings 2034)。
test('同質な項目の並びがリストとして公開される (記事シリーズ / Settings のプロジェクト行)', async ({ page }) => {
  // home: AIO 実践シリーズの記事カード
  await page.goto('/#/');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1').first()).toBeVisible();

  const articles = page.locator('#content .aio-article-card');
  const articleCount = await articles.count();
  expect(articleCount, 'control: 記事カードが描画されていない').toBeGreaterThan(2);
  expect(await page.locator('#content [role="listitem"]').count(),
    '記事カードが listitem として公開されていない').toBe(articleCount);
  expect(await page.locator('#content [role="list"]').count(),
    '記事カードを束ねる list が無い').toBeGreaterThan(0);

  // settings: プロジェクトの並び替え行 / 表示切替行
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  const lists = await page.locator('#content [role="list"]').count();
  expect(lists, 'プロジェクト行を束ねる list が無い').toBeGreaterThanOrEqual(2);
  const items = await page.locator('#content [role="listitem"]').count();
  // 並び替えと表示切替の 2 リスト × プロジェクト数
  expect(items, 'プロジェクト行が listitem として公開されていない').toBeGreaterThan(lists);
});


// ===== 同じ画面に「同じ名前で行き先が違う」操作要素を残さない =====
// アプリ一覧の 5 つのボタンは全部「開く」という名前だった (実測)。カードの見出しが文脈を
// 与えるとはいえ、SR 利用者がボタンだけを辿ると **5 個の「開く」が並び行き先を区別できない**
// (WCAG 4.1.2)。リポジトリの慣習は「削除：<名前>」「上へ移動：<名前>」と **名前側に対象を
// 含める**形で統一されている (#1085) ので、それに揃える。可視ラベルは「開く」のままなので
// 描画は不変。
//
// NOTE: プロジェクト一覧のタグチップ (「#AI」が 4 個など) は **同じ名前で同じ動作** (そのタグで
// 絞り込む) なので対象にしない —— 区別できないことが問題になるのは「名前が同じなのに
// 行き先/効果が違う」ときだけで、機械的に全部を一意化すると意味論の水増しになる。
test('アプリ一覧のボタン名が行き先ごとに一意になる', async ({ page }) => {
  await page.goto('/#/apps');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'アプリ' })).toBeVisible();

  const names = await page.evaluate(() => Array.from(document.querySelectorAll('#content button'))
    .map((b) => b.getAttribute('aria-label') || (b.textContent || '').trim()));

  expect(names.length, 'control: アプリのボタンが描画されていない').toBeGreaterThan(3);
  expect(new Set(names).size,
    `行き先が違うのに同じ名前のボタンがある (${names.length} 個中 ${new Set(names).size} 種類)`).toBe(names.length);

  // 可視ラベルは「開く」のままである (名前の一意化で見た目を変えていない)
  const visible = await page.evaluate(() => Array.from(document.querySelectorAll('#content button'))
    .map((b) => (b.textContent || '').trim()));
  expect(visible.every((t) => t === '開く'), '可視ラベルが変わっている (描画不変のはず)').toBe(true);
});


// ===== WCAG 2.5.3 (Label in Name) — 可視テキスト ⊆ アクセシブル名 =====
// axe には該当ルール label-content-name-mismatch があるが `enabled: false`（experimental）
// なので、上の withTags(['wcag21a', ...]) スキャンでは**一度も走らない**。つまり Level A の
// この SC はリポジトリ全体で未検査だった。明示的に enabled: true にして走らせる。
//
// なぜ実害があるか: 音声入力の利用者は「画面に見えている文字」を読み上げて操作する。
// アクセシブル名が可視テキストを含まないと、見えているとおりに発話しても起動できない。
// 実際に home の 3 つの CTA（「ケースを見る →」「分担表を見る →」「Zennで読む →」）が
// 行き先だけを述べる aria-label を持っており、可視テキストと無関係だった。
//
// 1 テストで全ルートを歩くのは、このルールが大半のルートで inapplicable（対象要素なし）
// ゆえ per-route テストに割ると CI 時間だけが増えるため。
// 見出しは DOM の先頭に出るが、このルールが見る要素 (可視テキストと aria-label を併せ持つ
// 操作要素) は後から描かれる。#content の要素数が 2 フレーム連続で変わらなくなるまで待つ。
// 実測 (2026-08-20): control の checked 32 の内訳は / が 3・**/#/projects が 24**・
// /#/apps が 5 で、残り 13 ルートは対象要素ゼロ (inapplicable)。つまり閾値 10 は
// **実質 /#/projects のカード 18 枚だけで支えられて**おり、カード描画前に測ると 8 に
// 落ちて control が「ルールが走っていない」と RED になる。
// honest: この race の発火は稀で、観測できたのは並列実行 8 回中 1 回。待ちを外した
// 状態で 7 回連続 pass したので「この待ちが効いている」ことは実証できていない。
// 根拠は頻度ではなく**構造** (閾値が単一ルートの遅延描画に依存している) に置く。
async function settleContent(page) {
  await expect.poll(async () => await page.evaluate(() => {
    const before = document.querySelectorAll('#content *').length;
    return new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(
      () => resolve(before === document.querySelectorAll('#content *').length ? before : -1))));
  }), '#content の描画が落ち着かない').toBeGreaterThan(0);
}

const LABEL_IN_NAME_ROUTES = ['/', '/#/projects', '/#/apps', '/#/apps/task', '/#/apps/todo',
  '/#/apps/notes', '/#/apps/ai', '/#/apps/pomodoro', '/#/apps/settings', '/#/quiz',
  '/#/about', '/#/resume', '/#/contact', '/#/role-split', '/#/hiring-risk', '/#/ai-knowhow'];
test('可視テキストがアクセシブル名に含まれる (WCAG 2.5.3) — 全ルート', async ({ page }) => {
  const offenders = [];
  let checked = 0;
  let prevHeading = null;
  for (const route of LABEL_IN_NAME_ROUTES) {
    await page.goto(route);
    // stale-DOM 回避: hash 遷移は document を作り直さないので、汎用の「見出しが見える」待ちは
    // **前ルートの DOM で充足してしまう**。見出しが前ルートと変わったことを待つ。
    // （この待ちを入れる前は /#/projects が home を測り続け、対象 24 個を 3 個と誤計測していた）
    await expect
      .poll(() => page.locator('#content').getByRole('heading').first().textContent().catch(() => null))
      .not.toBe(prevHeading);
    prevHeading = await page.locator('#content').getByRole('heading').first().textContent();
    await settleContent(page);

    const results = await new AxeBuilder({ page })
      .options({
        runOnly: { type: 'rule', values: ['label-content-name-mismatch'] },
        rules: { 'label-content-name-mismatch': { enabled: true } },
      })
      .analyze();
    for (const v of results.violations) {
      for (const n of v.nodes) { offenders.push(`${route} :: ${n.html.slice(0, 120)}`); }
    }
    checked += results.passes.reduce((a, v) => a + v.nodes.length, 0);
  }
  // control: ルールが実際に対象要素を見つけている（inapplicable ばかりなら何も検査していない）
  expect(checked, 'control: 検査対象の要素が 1 つも無い — ルールが走っていない疑い').toBeGreaterThan(10);
  expect(offenders, `可視テキストを含まないアクセシブル名: ${JSON.stringify(offenders)}`).toEqual([]);
});


// ===== 既定で無効な axe ルール (Level A/AA) を明示的に走らせる =====
// axe は 105 ルール中 16 を `enabled: false` で出荷する (experimental / 廃止された SC /
// AAA など理由はさまざま)。**タグは一致するのに走らない**ので、上の withTags スキャンが
// 緑でも、これらの SC はリポジトリ全体で一度も検査されていない。#1091 で
// label-content-name-mismatch (WCAG 2.5.3 Level A) の実違反 3 件がこの穴から出た。
//
// ここでは Level A/AA に属する 8 ルールを明示的に有効化して全ルートで走らせる。
// AAA (color-contrast-enhanced / identical-links-same-purpose / meta-refresh-no-exceptions)、
// best-practice、および WCAG 2.2 で廃止された duplicate-id / duplicate-id-active
// (`wcag2a-obsolete` タグ) は対象外 —— 前者は目標水準を超え、後者は W3C 自身が取り下げた SC。
//
// **対象集合は axe から実行時に導出して照合する**。ハードコードした一覧だけだと、axe を
// 上げて新しい disabled ルールが増えたときに黙って未検査のまま残る (Check 415 が
// STATUS.md の workflow 網羅を生成器と独立に導出するのと同じ設計)。
const AXE_AA_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22a', 'wcag22aa'];
const DISABLED_AA_RULES = ['aria-roledescription', 'audio-caption', 'css-orientation-lock',
  'label-content-name-mismatch', 'p-as-heading', 'table-fake-caption', 'target-size', 'td-has-header'];
test('既定で無効な axe ルール (Level A/AA) を全ルートで走らせる', async ({ page }) => {
  // (1) 対象集合が axe の現状と一致しているか (axe 更新への追従を機械化)
  const derived = require('axe-core').getRules()
    .filter((r) => r.enabled === false && r.tags.some((t) => AXE_AA_TAGS.includes(t)))
    .map((r) => r.ruleId).sort();
  expect(derived,
    'axe の既定無効ルール (Level A/AA) が変わった。新しいルールを実測してから DISABLED_AA_RULES へ足すこと'
  ).toEqual([...DISABLED_AA_RULES].sort());

  const ruleOpts = {};
  DISABLED_AA_RULES.forEach((id) => { ruleOpts[id] = { enabled: true }; });
  const offenders = [];
  // target-size (WCAG 2.2 AA) はタッチ標的の SC なので desktop だけでは意味がない。
  // モバイル幅でも同じ集合を走らせる。
  for (const viewport of [{ width: 1280, height: 720 }, { width: 390, height: 844 }]) {
    await page.setViewportSize(viewport);
    let prevHeading = null;
    for (const route of LABEL_IN_NAME_ROUTES) {
      await page.goto(route);
      // stale-DOM 回避 (上の 2.5.3 テストと同じ理由)
      await expect
        .poll(() => page.locator('#content').getByRole('heading').first().textContent().catch(() => null))
        .not.toBe(prevHeading);
      prevHeading = await page.locator('#content').getByRole('heading').first().textContent();

      const results = await new AxeBuilder({ page })
        .options({ runOnly: { type: 'rule', values: DISABLED_AA_RULES }, rules: ruleOpts })
        .analyze();
      for (const v of results.violations) {
        for (const n of v.nodes) { offenders.push(`${viewport.width}px ${route} [${v.id}] ${n.html.slice(0, 110)}`); }
      }
    }
  }
  expect(offenders, `既定で無効な axe ルールの違反: ${JSON.stringify(offenders)}`).toEqual([]);
});



// ===== 絞り込み中の完了操作でも件数アナウンスが追随すること (WCAG 4.1.3) =====
// 既存の被覆は「フィルタを**変更**したとき件数が polite status に出る」までで、
// **項目を完了させて一覧から消えたとき**に件数が追随するかは未被覆だった。
// 「未完了」で絞り込んで片付けていく使い方では、消えた項目そのものは見えなくなるので、
// **残り何件かを伝える唯一の手がかりが この status 領域**になる。ここが止まると
// SR 利用者には「押したが何件残っているか分からない」状態になる。
// 実測 (2026-08-20): 3 件 → 完了 1 件で「未完了 2 件」へ正しく追随していた (honest-clean)。
// 未被覆のまま放置すると、件数を全体数から取るような退行が silent に通る。
test('絞り込み中に完了させると残り件数のアナウンスが追随する', async ({ page }) => {
  await page.goto('/#/apps/todo', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();

  for (const t of ['COUNT-A', 'COUNT-B']) {
    await page.locator('#todo-input').fill(t);
    await page.locator('#todo-input').press('Enter');
    await expect(page.locator('#content').getByText(t, { exact: true })).toBeVisible();
  }

  // 「未完了」で絞り込む (キーボード相当の change を作る)
  await page.locator('#todo-filter').evaluate((el) => {
    el.focus();
    el.value = 'active';
    el.dispatchEvent(new Event('change', { bubbles: true }));
  });
  const status = page.locator('#todo-filter-status');
  await expect(status).toHaveText(/TODO: 未完了 \d+ 件/);
  const before = parseInt((await status.textContent()).match(/(\d+)/)[1], 10);
  // control: 件数が 2 未満だと「減った」ことを測れない
  expect(before, 'control: 未完了が 2 件未満では減少を測れない').toBeGreaterThanOrEqual(2);

  const cb = page.locator('#content input[type="checkbox"]').first();
  const label = await cb.getAttribute('aria-label');
  await cb.click();
  // 消えるまで待つ (再描画前に読むと古いノードを掴む)
  await expect(page.locator('#content').getByText(label.split('：')[1], { exact: true })).toHaveCount(0);

  await expect(status, '完了させたのに残り件数のアナウンスが追随していない')
    .toHaveText(new RegExp(`TODO: 未完了 ${before - 1} 件`));
});
