const { test, expect } = require('@playwright/test');

// ===== 外部 ingestion の正規化と型ガード =====
// 取り込み経路 (import / cross-tab / snapshot 復元 / load) は **信用できない入力**を受ける。
// ここで正規化を一つでも省くと、その経路のユーザーだけが FatalPage に落ちたり、
// `[object Object]` が画面に描かれたり、巨大データで localStorage が膨らんだりする。
// 本 spec はその型ガードと bound をまとめて固定する。過去の実バグ:
//   #93  Settings が Storage 依存の注入漏れで全ユーザー crash
//   #230 AI history が無制限保存
//   #295 cross-tab だけ正規化を省いていた
//   #561 snapshot 復元が未正規化採用
//   #568/#572/#573 非配列フィールドで `.filter` が TypeError
//   #968/#969/#970 truthy な非文字列が `String()` を素通りし空欄 / [object Object] 化
//
// 元は apps-settings-io.spec.js にあったが、同 file が早期警告 (900 行) を超えたため
// **BLOCKING (1,000 行) を踏む前に**このテーマの塊を切り出した。
// mutation の `test` フィールドは title 一致ゆえ file 移動の影響を受けない。

// 通知の検証は sr-only の通知領域で行う (toast は 3 秒で自動消滅するため CI 負荷で
// 間欠 RED になる・#1018)。`#action-announcement` は次の通知まで消えない。
async function expectNotified(page, text) {
  await expect(page.locator('#action-announcement')).toContainText(text);
}

// ===== 7.2: AI history ingestion の文字列長 bound (import/cross-tab 側 #230 class) =====
// write 側 (apps.js) は prompt を AI_MESSAGE(5000) で bound 済だが、load/import/cross-tab の
// 正規化 (normalizeAppsData) は従来 entry 数(80) だけ bound し個々の prompt/response の文字列長を
// bound していなかった。巨大 prompt を含む store を seed → load(validateAndNormalize) を通し、
// 正規化後に prompt/response が AI_MESSAGE 以下へ切り詰められることを実検証する (localStorage
// bloat を招く ingestion 側 gap の退行検知)。
test('AI history strings are length-bounded on normalize ingestion (#230 class)', async ({ page }) => {
  // load() が通る前に localStorage を巨大 prompt/response 入りの正しい schema で seed
  await page.addInitScript(() => {
    try {
      const big = 'x'.repeat(20000);
      localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
        schemaVersion: 12,
        type: 'full-store',
        appsData: { ai: { history: [{ prompt: big, response: big, timestamp: 1 }] } },
        theme: 'system',
        lastModified: 1,
      }));
    } catch (e) { /* noop */ }
  });
  // settings の「正規化」ボタンは validateAndNormalize を明示実行し、正規化後の store を
  // localStorage へ保存確定する (load 直後は in-memory ゆえ localStorage 未反映のため、この経路で
  // 永続化を確定させてから読み戻す)。
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const normSection = page.locator('section.card').filter({ has: page.getByRole('heading', { name: '整合性チェック / 正規化' }) });
  await normSection.getByRole('button', { name: '実行' }).click();
  await expectNotified(page, '正規化を完了しました');

  // 正規化後、ai.history の prompt/response が AI_MESSAGE(5000) 以下へ bound されている。
  // 保存は debounce (scheduleSave) されるため expect.poll で localStorage 反映を待つ。
  await expect.poll(async () => {
    return await page.evaluate(() => {
      try {
        const s = JSON.parse(localStorage.getItem('portfolio_enhanced_v45') || '{}');
        const h = (s.appsData && s.appsData.ai && s.appsData.ai.history) || [];
        if (!h.length) { return -1; }
        return Math.max(...h.map(e => Math.max(String(e.prompt || '').length, String(e.response || '').length)));
      } catch (e) { return -2; }
    });
  }, { timeout: 8000 }).toBe(5000); // 20000 → AI_MESSAGE(5000) へ厳密 bound (entry 保持 + 切詰)

  // crash していない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `normalize caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.1f: normalizeAppsData は ai.history / pomodoro.history が非配列でも crash しない (#93/#295/#561 class) =====
// normalizeAppsData は「どんな入力でも throw しない総関数」契約を持つ (tasks/todos は Array.isArray で
// ガード済)。だが ai.history は旧 `if (data.ai?.history)`・pomodoro.history は旧 `if (data.pomodoro.history)`
// と truthy 判定のみで、別 schema / 破損 store がこれらを非配列 (文字列等) で持つと ai は `.filter` が
// TypeError を throw → validateAndNormalize が例外 → load()(state.js init)/cross-tab/import/snapshot-restore
// の全 ingestion 経路が FatalPage crash する。本テストは current schema(12) + ai.history=文字列 の store を
// addInitScript で seed し load() を通して (1) FatalPage crash しない (2) app(ai ページ)が描画され続ける
// ことを検証する。修正前は load() が init で throw し fatal になるため非 vacuous。
test('normalizeAppsData tolerates a non-array ai/pomodoro history without crashing (#93 class)', async ({ page }) => {
  // load() が state.js init で走る前に、current schema だが history を非配列で持つ破損 store を seed。
  await page.addInitScript(() => {
    try {
      localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
        schemaVersion: 12,           // 現行と一致 = schema guard を通過し validateAndNormalize へ到達する
        type: 'full-store',
        appsData: {
          ai: { history: 'CORRUPT-NON-ARRAY' },       // 旧実装は .filter で TypeError → crash
          pomodoro: { history: 'CORRUPT-NON-ARRAY' },  // 旧実装は String.slice で型崩れ
          tasks: [{ title: '破損タスク', tags: 'NOT-AN-ARRAY' }]  // task.tags 非配列 → 旧 .filter で TypeError → crash
        },
        theme: 'system',
        lastModified: 1,
      }));
    } catch (e) { /* noop */ }
  });

  await page.goto('/#/apps/ai');
  await page.waitForLoadState('domcontentloaded');

  // (1) FatalPage crash していない (修正前は init の load() が throw)
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `non-array history ingestion caused a fatal render: ${fatal}`).toBeNull();

  // (2) AI ページが描画され続ける (非配列 history は空配列にフォールバックし page は機能する)。
  //     修正前は load() が state.js init で throw し app が boot しないため #ai-input は描画されない。
  await expect(page.locator('#ai-input')).toBeVisible();

  // (3) ポモドーロページも同様に描画され続ける (pomodoro.history 非配列でも crash しない)
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.font-mono.text-stat').first()).toBeVisible();
  const fatal2 = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal2, `non-array pomodoro.history caused a fatal render: ${fatal2}`).toBeNull();

  // (4) タスクページも描画され続ける (task.tags 非配列でも normalize が空配列にフォールバックし crash しない)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#task-input')).toBeVisible();
  const fatal3 = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal3, `non-array task.tags caused a fatal render: ${fatal3}`).toBeNull();
});

// ===== 7.1g: normalizeProject は project の tech/tags/links が非配列でも crash しない (#93/#295/#561/#568 class) =====
// normalizeProject は untrusted import project を正規化する総関数だが、tech/tags/highlights/
// relatedProjectIds/links を旧 `(raw.tech || [])` = truthy 判定のみで扱っていた。import/cross-tab/
// snapshot の project がこれらを非配列 (文字列等) で持つと `|| []` が置換せず `.filter` が TypeError を
// throw → validateAndNormalize が例外 → load()(state.js init) 等が FatalPage crash する。default の
// proj() builder は Array.isArray でガード済だが本 normalizer は漏れていた。本テストは current
// schema(12) + project.tech=文字列 の store を seed し load() を通して (1) crash しない (2) Projects
// ページに project card が描画される (非配列 field は空配列にフォールバック) ことを検証する。
// 修正前は load() が init で throw し app が boot しないため card が描画されず RED = 非 vacuous。
test('normalizeProject tolerates a non-array project field without crashing (#93 class)', async ({ page }) => {
  await page.addInitScript(() => {
    try {
      localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
        schemaVersion: 12,
        type: 'full-store',
        projects: [
          // 破損 project: tech/tags/links が非配列 (旧 .filter で TypeError)
          { id: 'corrupt1', slug: 'corrupt-one', name: '破損プロジェクト', tech: 'NOT-AN-ARRAY', tags: 42, links: { a: 1 } }
        ],
        theme: 'system',
        lastModified: 1,
      }));
    } catch (e) { /* noop */ }
  });

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  // (1) FatalPage crash していない (修正前は init の load()→normalizeProject が throw)
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `non-array project field caused a fatal render: ${fatal}`).toBeNull();

  // (2) Projects ページに project card が描画される (defaults + 破損 project が正規化されて残る)
  const cards = page.locator('.grid-projects article.card');
  await expect(cards.first()).toBeVisible();
  expect(await cards.count(), 'projects should render after normalizing a corrupt project').toBeGreaterThan(1);
});

// ===== 関連プロジェクト: import の数値 id 参照が String 正規化される (relatedProjectIds type-coercion) =====
// normalizeProject は id を `String(raw.id || ...)` で常に文字列化するが、relatedProjectIds の「要素」を
// 正規化しないと、import/cross-tab/snapshot の数値 id 参照 (例 [9002]) が canonical な文字列 id 空間と
// strict 不一致になり、ProjectDetailPage の `relatedProjectIds.includes(p.id)`(p.id=文字列) と
// autoRelatedCandidates の `fixed.has(p.id)` が両方外れる → 手動関連が「関連プロジェクト」から silent に
// 消える desync (#93/#295 の「外部 ingestion は全経路正規化」class の relatedProjectIds 版)。
// A→B を数値 id で関連付け、A/B を低類似度 (別カテゴリ・タグ/技術/本文全て disjoint) にして autoRelated
// 混入を排除 → B が「関連プロジェクト」に出るのは manual related 経路が生きている時のみ = 非 vacuous。
test('Imported numeric relatedProjectIds resolve to string ids (related section shows the link)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByLabel('インポートモード').selectOption('upsert');

  const nameA = 'RelSourceProjE2E9001';
  const nameB = 'RelTargetProjE2E9002';
  const payload = {
    schemaVersion: 12,
    type: 'full-store',
    projects: [
      // id は数値、relatedProjectIds も数値 (import データが number id を持つ現実シナリオ)。
      // A/B は category/tags/tech/summary が全 disjoint ゆえ similarityScore=0 → autoRelated には出ない。
      { id: 9001, slug: 'e2e-rel-src-9001', name: nameA, category: 'ZetaCat', summary: 'alpha bravo charlie', tech: ['Xlang'], tags: ['xtag'], relatedProjectIds: [9002], demoRoute: null },
      { id: 9002, slug: 'e2e-rel-tgt-9002', name: nameB, category: 'OmegaCat', summary: 'delta echo foxtrot', tech: ['Ylang'], tags: ['ytag'], relatedProjectIds: [], demoRoute: null },
    ],
  };
  await page.getByLabel('インポートする JSON ファイルを選択').setInputFiles({
    name: 'backup.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(payload)),
  });
  await expectNotified(page, 'インポートが完了しました');

  // A の詳細ページへ (slug で解決)
  await page.goto('/#/projects/e2e-rel-src-9001');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: nameA })).toBeVisible();

  // 「関連プロジェクト」card 内に B へのリンクが出る (String 正規化が効いている時のみ)。
  const relatedCard = page.locator('#content section.card', {
    has: page.getByRole('heading', { name: '関連プロジェクト' }),
  });
  await expect(relatedCard.getByRole('button', { name: nameB })).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `numeric relatedProjectIds import caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: profile email の ingestion 文字列長 bound (import bloat 防止・#230/#801 class) =====
// store.js normalizeAppsData/validateAndNormalize は profile.email を slice(0, 254)(RFC 5321 上限)で
// bound し import bloat を防ぐ。AI history 文字列 bound(#230)・MAX_TASKS 件数 bound(#801)は test 済だが
// profile email の文字列長 bound は未カバーだった。巨大 email を含む profile を import → Contact ページの
// mailto リンク表示が 254 文字に切り詰められることを検証する (bound が外れると巨大文字列が href/表示に
// 載り localStorage/DOM を bloat させる)。
test('Profile email is length-bounded to 254 on import (ingestion bloat guard)', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  const hugeEmail = 'x'.repeat(300) + '@example.com'; // 312 文字 → 254 へ bound されるべき
  await page.getByLabel('インポートする JSON ファイルを選択').setInputFiles({
    name: 'profile-huge-email.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ schemaVersion: 12, type: 'full-store', profile: { name: 'BoundUser', email: hugeEmail } })),
  });
  await expectNotified(page, 'インポートが完了しました');

  await page.goto('/#/contact', { waitUntil: 'domcontentloaded' });
  const emailLink = page.locator('a.font-mono[href^="mailto:"]').first();
  await expect(emailLink).toBeVisible();
  const len = (await emailLink.textContent() || '').length;
  expect(len, `email は 254 へ bound されるべき (実測 ${len})`).toBe(254);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `profile email bound caused a fatal: ${fatal}`).toBeNull();
});

// ===== profile 正規化: truthy な非文字列がフィールドを空にしない (外部 ingestion の型ガード) =====
// 旧実装は `String(v || fallback)` だったため、`[]` や `{}` のような **truthy な非文字列** が
// `||` を素通りし、`String([]) === ''` でフィールドが空になっていた。email が空になると
// ContactPage からアドレス表示が消え、「メールを作成」ボタンが宛先の無い
// `mailto:?subject=...` を開く (= 連絡導線が黙って壊れる)。name が `{}` の場合は表示名が
// "[object Object]" になっていた。どちらも fatal を出さないので ErrorBoundary にも掛からず、
// 視覚 baseline は ADVISORY ゆえ、**この behavior test 以外に捕捉層が無い**。
// #93/#295/#561/#568/#572/#573 と同じ「外部 ingestion の型ガード」class の profile 面。
test('Hostile profile import: a truthy non-string must not blank a field', async ({ page }) => {
  const importProfile = async (profile) => {
    await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#main-content h1').first()).toBeVisible();
    await page.getByLabel('インポートする JSON ファイルを選択').setInputFiles({
      name: 'hostile-profile.json',
      mimeType: 'application/json',
      buffer: Buffer.from(JSON.stringify({ profile })),
    });
    // NOTE: 2 回目の import 時にはまだ 1 回目の Toast が残っていることがあるため .first()
    //   (strict mode violation を避ける)。ここでは「完了 Toast が出たこと」だけを待てば十分。
    await expectNotified(page, 'インポートが完了しました');
  };

  // (1) email: [] — `[]` は truthy なので `||` の fallback を素通りし String([]) が '' になる
  await importProfile({ email: [] });
  await page.goto('/#/contact', { waitUntil: 'domcontentloaded' });
  // NOTE: 先に「あるはずの要素」を待って描画を確定させてから中身を読む (Check 402)
  await expect(page.locator('#content')).toContainText('Contact');
  const emailLink = page.locator('#content a[href^="mailto:"]');
  await expect(emailLink, 'email が空になり ContactPage から宛先が消えた').toHaveCount(1);
  const href = await emailLink.getAttribute('href');
  expect(href, `mailto に宛先が無い (href=${href})`).not.toBe('mailto:');
  expect((href || '').length, `mailto の宛先が空 (href=${href})`).toBeGreaterThan('mailto:'.length);

  // (2) name: {} — String({}) は "[object Object]" で、そのまま表示名として描画されていた
  await importProfile({ name: {} });
  await page.goto('/#/contact', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content')).toContainText('Contact');
  await expect(
    page.locator('#content'),
    '非文字列の name がそのまま stringify されて表示された'
  ).not.toContainText('[object Object]');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `hostile profile import caused a fatal: ${fatal}`).toBeNull();
});

// ===== project 正規化: 非文字列が "[object Object]" として描画されない =====
// profile と同じ class の projects 面。`String(raw.name || 'Untitled')` は `{}` が truthy なので
// fallback が働かず、そのまま `"[object Object]"` が一覧カードと詳細ページへ描画されていた
// (実測: 一覧に 3 箇所 / 詳細に 4 箇所)。tech/tags/highlights の `filter(Boolean)` も `{}` を
// 素通りさせ、チップとして同じ文字列が出ていた。fatal を出さないので ErrorBoundary に掛からず、
// 視覚 baseline は ADVISORY ゆえ **この behavior test 以外に捕捉層が無い**。
// 同時に「正当な値まで落としていない」ことも検査する (型ガードが過剰だと機能を壊すため)。
test('Hostile project import: non-string fields must not render as [object Object]', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#main-content h1').first()).toBeVisible();

  await page.getByLabel('インポートする JSON ファイルを選択').setInputFiles({
    name: 'hostile-project.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      projects: [{
        id: 'p_hostile_e2e', slug: 'hostile-e2e', name: {}, category: [], summary: {},
        // 非文字列と正当値を混在させ、前者だけが落ちることを見る
        tech: [{}, null, 'tech-kept'], tags: [{}, 'tag-kept'], highlights: [{}, 'hl-kept'],
        links: [{ label: {}, url: 'https://example.com' }],
        outcome: { impact: {}, metrics: [{ label: {}, value: {} }] },
        demoRoute: null, relatedProjectIds: [{}],
      }],
    })),
  });
  await expectNotified(page, 'インポートが完了しました');

  // NOTE: 一覧カードは **tags** を描画し、tech は詳細ページにしか出ない。ルートごとに
  //   「そのページに必ずあるはずの正当値」を positive anchor にして描画を確定させてから
  //   不在を検査する (Check 402)。同じ anchor を使い回すと片方で必ず落ちる。
  for (const [route, kept] of [['#/projects', 'tag-kept'], ['#/projects/hostile-e2e', 'tech-kept']]) {
    await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
    await expect(
      page.locator('#content'),
      `${route}: 正当な値が型ガードで落ちた (過剰なガード)`
    ).toContainText(kept);
    await expect(
      page.locator('#content'),
      `${route}: 非文字列フィールドが "[object Object]" として描画された`
    ).not.toContainText('[object Object]');
  }

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `hostile project import caused a fatal: ${fatal}`).toBeNull();
});

// ===== appsData 正規化: 必須テキストが非文字列でも "[object Object]" を描画しない =====
// profile (#968) / projects (#969) と同じ class の appsData 面。`filter(t => t && t.title)` は
// `{}` が truthy なので素通りし、後段の `String(t.title)` が "[object Object]" を作って
// タスク一覧・TODO 一覧へ描画していた (実測: 各ルート 1 箇所)。
// **この class は entry を落とすのが正** — 既存の「title/text が無い entry は落とす」挙動と
// 同じ扱いに揃える (プレースホルダを捏造して「壊れた項目がある」ことを隠さない)。
// fatal を出さないので ErrorBoundary に掛からず、視覚 baseline は ADVISORY ゆえ
// **この behavior test 以外に捕捉層が無い**。
test('Hostile appsData import: non-string title/text must not render as [object Object]', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#main-content h1').first()).toBeVisible();

  await page.getByLabel('インポートする JSON ファイルを選択').setInputFiles({
    name: 'hostile-apps.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      appsData: {
        // 壊れた entry と正当な entry を混在させ、前者だけが落ちることを見る
        tasks: [{ id: 't_hostile', title: {}, tags: [{}] }, { id: 't_ok', title: 'task-kept-e2e' }],
        todos: [{ id: 'd_hostile', text: {} }, { id: 'd_ok', text: 'todo-kept-e2e' }],
      },
    })),
  });
  await expectNotified(page, 'インポートが完了しました');

  for (const [route, kept] of [['#/apps/task', 'task-kept-e2e'], ['#/apps/todo', 'todo-kept-e2e']]) {
    await page.goto(`/${route}`, { waitUntil: 'domcontentloaded' });
    // NOTE: 先に「あるはずの正当値」を待って描画を確定させてから不在を検査する (Check 402)。
    //   これは同時に「型ガードが過剰で正当な entry まで落としていない」ことの検査でもある。
    await expect(
      page.locator('#content'),
      `${route}: 正当な entry が型ガードで落ちた (過剰なガード)`
    ).toContainText(kept);
    await expect(
      page.locator('#content'),
      `${route}: 非文字列の必須テキストが "[object Object]" として描画された`
    ).not.toContainText('[object Object]');
  }

  // NOTE (非 vacuity 上の要点): 描画側の検査だけでは **filter の欠落を捕捉できない**。
  //   `String(t.title)` を safeStr にした時点で `{}` は空文字になり "[object Object]" は
  //   消えるため、filter を外しても DOM 検査は緑のままだった (最初に書いた版が実際そうなり、
  //   mutation 2 本とも素通りした)。壊れた entry が **落ちている** ことは永続化側で確かめる。
  //   さもないと「本文の無い空カードが残る」退行が無検査で通る。
  const persisted = await page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('portfolio_enhanced_v45')).appsData; } catch (e) { return null; }
  });
  expect(persisted, '永続化された appsData を読めない').not.toBeNull();
  expect(
    persisted.tasks.map(t => t.id),
    '必須テキストが非文字列の task が落ちずに残っている (本文の無い空カードになる)'
  ).not.toContain('t_hostile');
  expect(
    persisted.todos.map(t => t.id),
    '必須テキストが非文字列の todo が落ちずに残っている'
  ).not.toContain('d_hostile');
  expect(persisted.tasks.map(t => t.id), '正当な task が落ちた').toContain('t_ok');
  expect(persisted.todos.map(t => t.id), '正当な todo が落ちた').toContain('d_ok');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `hostile appsData import caused a fatal: ${fatal}`).toBeNull();
});


// ===== 同じ id の項目を取り込んでも「1 件だけ操作する」が成り立つ =====
// id は自前生成なら一意だが、**取り込みは信用できない入力**なので保証されない
// (手編集の JSON / 別バージョンが書いた store / 壊れた localStorage)。同じ id の項目が
// 並ぶと、id で操作する処理が巻き添えを起こす:
//   - 削除: `filter(t => t.id !== id)` が **同 id を全て落とす** → 1 件消したつもりが両方消える
//   - 更新: `find` は先頭しか拾わない → もう片方に効かない (逆向きの非対称)
//   - DOM: `task-delete-<id>` 等が重複し、focus 復元 (getElementById) が別カードを掴む
// 実測 (#1058): 同 id のタスク 2 件で片方を削除 → **2 件とも消えた**。
// #154 で slug に対して同じことをしたのと同型なので、同じ「後から来た方に連番を振る」方式で
// normalize が一意化する。
test('同じ id のタスクを取り込んでも片方だけ削除できる', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
      schemaVersion: 12, type: 'full-store',
      appsData: {
        tasks: [
          { id: 'dup-ing-1', title: 'DUP-ING-A', status: 'backlog', priority: 'med', tags: [], createdAt: 1 },
          { id: 'dup-ing-1', title: 'DUP-ING-B', status: 'backlog', priority: 'med', tags: [], createdAt: 2 }
        ]
      }
    }));
  });
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();

  // control: 2 件とも描画されている (片方が落ちていたら削除の巻き添えを測れない)
  await expect(page.locator('#content').getByText('DUP-ING-A')).toBeVisible();
  await expect(page.locator('#content').getByText('DUP-ING-B')).toBeVisible();

  // DOM id が重複していない (focus 復元が別カードを掴む原因)
  const dups = await page.evaluate(() => {
    const seen = new Map();
    document.querySelectorAll('[id]').forEach((e) => seen.set(e.id, (seen.get(e.id) || 0) + 1));
    return [...seen.entries()].filter(([, n]) => n > 1).map(([id]) => id);
  });
  expect(dups, `取り込みで DOM id が重複している: ${dups.join(', ')}`).toEqual([]);

  await page.getByRole('button', { name: 'タスクを削除：DUP-ING-B' }).click();

  await expect(page.locator('#content').getByText('DUP-ING-B'),
    '削除した方が消えていない').toHaveCount(0);
  await expect(page.locator('#content').getByText('DUP-ING-A'),
    '1 件消したつもりが、同じ id の別項目まで巻き添えで消えている').toBeVisible();
});

// projects 側も同じ (削除・非表示が id で引く)。「1 ケースだけ処理して他を忘れる」非対称を作らない。
test('同じ id のプロジェクトを取り込んでも片方だけ削除できる', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
      schemaVersion: 12, type: 'full-store',
      projects: [
        { id: 'p-dup-ing', slug: 'p-dup-ing-a', name: 'PROJ-DUP-A', category: 'User Added', summary: 's', tech: [], tags: [], demoRoute: null },
        { id: 'p-dup-ing', slug: 'p-dup-ing-b', name: 'PROJ-DUP-B', category: 'User Added', summary: 's', tech: [], tags: [], demoRoute: null }
      ]
    }));
  });
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  await expect(page.getByRole('button', { name: '削除：PROJ-DUP-A' })).toBeVisible();  // control
  await expect(page.getByRole('button', { name: '削除：PROJ-DUP-B' })).toBeVisible();

  page.once('dialog', (d) => d.accept());
  await page.getByRole('button', { name: '削除：PROJ-DUP-B' }).click();

  await expect(page.getByRole('button', { name: '削除：PROJ-DUP-B' })).toHaveCount(0);
  await expect(page.getByRole('button', { name: '削除：PROJ-DUP-A' }),
    '1 件消したつもりが、同じ id の別プロジェクトまで巻き添えで消えている').toBeVisible();
});
