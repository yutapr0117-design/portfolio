const { test, expect } = require('@playwright/test');


// ===== 7.1: 壊れた localStorage からの graceful 復帰 (resilience) =====
// 永続データ (localStorage) が破損 JSON でも、Storage.parse の try/catch + Store.load の default
// fallback でアプリは crash せず既定状態で描画を継続すべき (fail-open)。破損値を仕込んで load し、
// FatalPage / NotFound に落ちず home が正常描画されることを検証する。設定画面 crash バグ (#93) で
// 「render 時クラッシュは致命的」と分かったため、永続層破損というもう一つの入力境界も固定する。
test('App recovers gracefully from corrupt localStorage (no FatalPage)', async ({ page }) => {
  await page.addInitScript(() => {
    try {
      localStorage.setItem('portfolio_enhanced_v45', 'not-valid-json-%%%');
      localStorage.setItem('portfolio_brand_v45', 'garbage-not-json');
    } catch (e) { /* noop */ }
  });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(200);

  // ErrorBoundary の FatalPage に落ちていない (window.__fatalError が falsy)
  const fatal = await page.evaluate(() => {
    const e = window.__fatalError;
    return e ? (e.message || String(e)) : null;
  });
  expect(fatal, `corrupt storage caused a fatal render: ${fatal}`).toBeNull();
  // home が正常描画され NotFound でもない
  await expect(page.locator('.hero-section')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Not Found', exact: true })).toHaveCount(0);

  // [coverage] 不正な brand 値 ('garbage-not-json') が Brand.sanitize で DEFAULT='indigo' へ
  // fallback すること。theme-init.js は pre-paint で raw 値を適用する (data-brand='garbage-...')
  // が、main.js の Brand.init() が ALLOWED[indigo/classic] 外を DEFAULT へ sanitize して最終
  // data-brand を確定する。従来テストは no-crash のみ検証し sanitize fallback を assert して
  // いなかった (sanitize が regress しても crash しないため素通り)。Brand.sanitize の ALLOWED
  // ガードを外すと data-brand が 'garbage-not-json' のままになり本アサーションが RED (非 vacuous)。
  await expect(page.locator('html')).toHaveAttribute('data-brand', 'indigo');
});


// ===== 7.1: スキーマ version 不一致時の安全マイグレーション (旧データ退避 → defaults リセット) =====
// Store.load() は parse 可能でも schemaVersion が現行 (CONSTANTS.SCHEMA_VERSION) と異なる旧データを
// 検出したとき、それを SNAPSHOT_KEY に {reason:'schema-mismatch', from, to, data} で退避してから
// createDefaultStore() で初期化する (将来のスキーマ変更で旧ユーザを crash させず、かつ旧データを
// 失わせない安全弁)。corrupt-storage テスト (parse 不能) とは別経路。古い schemaVersion の有効
// JSON を仕込んで load し、(1) crash せず home 描画 (2) 旧データが反映されず初期化 (3) snapshot に
// schema-mismatch で退避、を検証する。
test('Store migrates safely on schema version mismatch (snapshots old data, resets to defaults)', async ({ page }) => {
  await page.addInitScript(() => {
    try {
      // parse 可能だが旧 schemaVersion のデータ (現行は 12)。旧タスクを 1 件含める。
      localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
        schemaVersion: 1,
        type: 'full-store',
        theme: 'system',
        appsData: { tasks: [{ id: 'old-1', title: 'OLD-SCHEMA-TASK-9001', status: 'backlog', priority: 'med', tags: [] }] }
      }));
    } catch (e) { /* noop */ }
  });
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  // (1) crash せず home 描画
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `schema mismatch caused a fatal render: ${fatal}`).toBeNull();
  await expect(page.locator('.hero-section')).toBeVisible();

  // (3) 旧データが schema-mismatch として snapshot に退避される
  const snap = await page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('portfolio_snapshot_v45')); } catch { return null; }
  });
  expect(snap, 'old data should be snapshotted on schema mismatch').not.toBeNull();
  expect(snap.reason).toBe('schema-mismatch');
  expect(snap.from).toBe(1);

  // (2) 旧タスクは現行ストアに反映されない (defaults へ初期化)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  // 描画確定を待ってから不在検査 (未描画を「無い」と誤認する vacuous PASS 防止・Check 402)
  await expect(page.getByLabel('新しいタスクを入力')).toBeVisible();
  await expect(page.getByText('OLD-SCHEMA-TASK-9001')).toHaveCount(0);
});


// ===== 7.1: 設定インポートの不正 JSON 耐障害性 (graceful error) =====
// settings の importJSON は FileReader + JSON.parse を try/catch で囲み、不正ファイルでも crash
// せず「JSONのパースに失敗しました」エラー Toast を出す (fail-soft)。不正 JSON ファイルを与え、
// エラー Toast 表示 + FatalPage に落ちないことを検証する (もう一つの入力境界 = ファイルアップロード)。
test('Settings import shows an error for malformed JSON file without crashing', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles({
    name: 'broken.json',
    mimeType: 'application/json',
    buffer: Buffer.from('this is definitely not valid json ###'),
  });

  // 不正 JSON → エラー Toast 表示・crash しない（エラーは #toast-container と sr-only aria-live の
  // 両方に出る = 視覚 + screen reader 両対応。toast 側を検証する）。
  await expect(page.locator('#toast-container').getByText('JSONのパースに失敗しました')).toBeVisible();
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `malformed import caused a fatal render: ${fatal}`).toBeNull();
});


// ===== 7.2: 有効 JSON インポートの正常系ラウンドトリップ (data-recovery) =====
// importJSON は FileReader→JSON.parse→トグル (既定: include profile/projects/apps, mode=append)
// に従い State.update でマージ→validateAndNormalize→「インポートが完了しました」。malformed
// (error 系) は被覆済みだが、バックアップ復元という data-recovery の中核=正常系は未カバーだった。
// 新 id のプロジェクトを含む有効 JSON を import し、(1) 完了通知 (2) append でそのプロジェクトが
// /#/projects に現れる (3) リロード永続、を実検証する (import のマージ/正規化破壊を検知)。
test('Settings import (valid JSON) appends projects and persists (data recovery)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const imported = {
    projects: [{
      id: 'p_import_e2e_9911',
      slug: 'imported-proj-9911',
      name: 'IMPORTED-PROJ-9911',
      category: 'Imported',
      summary: 'e2e import roundtrip',
      problem: '', approach: '',
      tech: ['JS'], tags: ['import']
    }]
  };

  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles({
    name: 'backup.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(imported)),
  });

  // (1) 完了通知
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  // (2) append モードで新 id のプロジェクトが公開一覧に追加される
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('IMPORTED-PROJ-9911').first()).toBeVisible();

  // (3) リロード後も永続 (validateAndNormalize が user-added を保持)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('IMPORTED-PROJ-9911').first()).toBeVisible();
});


// ===== 7.2: import で slug 衝突するプロジェクトが一意化される (詳細到達性) =====
// mergeProjectsWithDefaults は ID でのみ dedupe するため、import データ内に同一 slug の別 id
// プロジェクトが 2 件あると slug が重複し、ProjectDetailPage の find(p.slug===slug) が先頭のみ返して
// 片方の詳細が到達不能になっていた (addProjectManual の slug 衝突修正の import パス版・全経路チョーク
// ポイントで根治)。同一 slug の 2 件を import → 結果の slug が一意化されることを State から検証する。
test('Importing projects with colliding slugs yields unique slugs (detail reachability)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const imported = {
    projects: [
      { id: 'p_imp_collide_a', slug: 'collide-slug', name: 'IMPORT-COLLIDE-A-5511', category: 'X', summary: '', problem: '', approach: '', tech: [], tags: [] },
      { id: 'p_imp_collide_b', slug: 'collide-slug', name: 'IMPORT-COLLIDE-B-5512', category: 'X', summary: '', problem: '', approach: '', tech: [], tags: [] },
    ]
  };
  await page.locator('input[type="file"]').setInputFiles({
    name: 'collide.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(imported)),
  });
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  // State 上で 2 件の slug が一意化されていること (重複なし)
  const readSlugs = () => page.evaluate(() => {
    try {
      const st = JSON.parse(localStorage.getItem('portfolio_enhanced_v45'));
      return (st.projects || []).filter(p => /^IMPORT-COLLIDE-[AB]-/.test(p.name)).map(p => p.slug);
    } catch { return []; }
  });
  await expect.poll(async () => (await readSlugs()).length).toBe(2);
  const slugs = await readSlugs();
  expect(new Set(slugs).size, `imported colliding slugs must be unique: ${JSON.stringify(slugs)}`).toBe(2);
});


// ===== 7.2: upsert インポートが既存を更新しつつ新規も追加する (data-loss 回帰) =====
// importJSON の upsert モード (UI ラベル「更新+追加」) は既存 id を更新し未知 id を追加するはず。
// 旧実装は未知 id を s.projects.push したのち Map.values() で上書きし、push した新規が破棄される
// data-loss バグがあった (append は被覆済みだが upsert は 0 カバレッジで未検知だった。strict は
// 直下の別テストで被覆)。既存 default (p01) の更新 + 新規 id の追加を含む JSON を upsert import し、
// 両方が一覧に出ることを検証する (修正前は新規 'UPSERT-NEW-*' が消えて fail する)。
test('Settings upsert import updates existing AND adds new projects (data-loss regression)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // インポートモードを upsert に切替
  await page.locator('select[aria-label="インポートモード"]').selectOption('upsert');

  const imported = {
    projects: [
      // 既存 default (id=p01) を更新
      { id: 'p01', slug: 'task-manager', name: 'UPSERT-UPDATED-7711', category: 'Productivity', summary: 'upsert update', problem: '', approach: '', tech: ['JS'], tags: [] },
      // 未知 id を追加 (旧バグで消えていた)
      { id: 'p_upsert_new_7712', slug: 'upsert-new-7712', name: 'UPSERT-NEW-7712', category: 'Imported', summary: 'upsert add', problem: '', approach: '', tech: ['JS'], tags: [] },
    ]
  };
  await page.locator('input[type="file"]').setInputFiles({
    name: 'upsert.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(imported)),
  });
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  // 追加パス (バグ修正の核): 新規 id のプロジェクトが一覧に出る
  await expect(page.getByText('UPSERT-NEW-7712').first()).toBeVisible();
  // 更新パス: 既存 p01 の name が更新され、元の default 名は消える (append では更新されない)
  await expect(page.getByText('UPSERT-UPDATED-7711').first()).toBeVisible();
  await expect(page.getByText('タスク管理アプリ')).toHaveCount(0);
});


// ===== 7.2: strict インポートはユーザー追加層を全置換しつつ defaults は温存する =====
// importJSON の strict モード (UI ラベル「全置換」) は s.projects=parsed.projects で置換するが、
// 直後の validateAndNormalize→mergeProjectsWithDefaults が v2 baseline の defaults を必ず再注入する
// ため「全置換」されるのは実質ユーザー追加層のみで defaults は温存される (label が直感より狭い実挙動)。
// strict は従来 0 カバレッジで、この surprising な実セマンティクスが未文書だった。append で投入した
// ユーザー project が strict import 後に消え、import 分は残り、default は健在、を実検証して固定する
// (append との distinct: append なら victim も残るため strict 固有の破壊性をこのテストだけが捉える)。
test('Settings strict import replaces user-added layer but preserves defaults', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // (1) append で victim ユーザー project を投入
  await page.locator('input[type="file"]').setInputFiles({
    name: 'victim.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ projects: [
      { id: 'p_strict_victim_8810', slug: 'strict-victim-8810', name: 'STRICT-VICTIM-8810', category: 'X', summary: '', problem: '', approach: '', tech: [], tags: [] },
    ] })),
  });
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  // (2) strict に切替え、victim を含まない別 project を import
  await page.locator('select[aria-label="インポートモード"]').selectOption('strict');
  await page.locator('input[type="file"]').setInputFiles({
    name: 'strict.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ projects: [
      { id: 'p_strict_new_8811', slug: 'strict-new-8811', name: 'STRICT-NEW-8811', category: 'Imported', summary: '', problem: '', approach: '', tech: [], tags: [] },
    ] })),
  });
  // append の toast が auto-dismiss 前で 2 件並ぶことがあるため最新 (strict) を対象に
  await expect(page.locator('#toast-container').getByText('インポートが完了しました').last()).toBeVisible();

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  // import 分は残る
  await expect(page.getByText('STRICT-NEW-8811').first()).toBeVisible();
  // strict 固有の破壊性: victim (import に含まれないユーザー project) は消える
  await expect(page.getByText('STRICT-VICTIM-8810')).toHaveCount(0);
  // defaults は mergeProjectsWithDefaults で温存される (「全置換」でも消えない)
  await expect(page.getByText('タスク管理アプリ').first()).toBeVisible();
});


// ===== 7.1: profile の github/linkedin が import で保持される + URL サニタイズ (data fidelity + XSS) =====
// validateAndNormalize は従来 profile の name/title/bio/email だけを残し github/linkedin/location を
// strip していたため、バックアップ import でこれらが silently 消え ContactPage の該当リンクが
// dead code 化していた。修正で schema 定義済みフィールドを保持しつつ、github/linkedin は href 描画
// されるため http(s) のみ許可して javascript: 等の XSS を遮断する。有効 URL は ContactPage に
// 反映され、危険な URL は描画されないことを実検証する。
test('Profile github/linkedin survive import and are URL-sanitized (XSS-safe)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 注: profile.name は付けない (Check 58 が spec 内の `name: '<lowercase>'` を route 名として
  // 抽出するため。本テストは github/linkedin の保持/サニタイズのみ検証するので name は不要)。
  const backup = {
    profile: {
      github: 'https://github.com/e2e-test-acct',
      linkedin: 'javascript:alert(1)', // 危険スキーム → サニタイズで除去されるべき
    }
  };
  await page.locator('input[type="file"]').setInputFiles({
    name: 'profile-backup.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(backup)),
  });
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

  // Contact ページ: 有効な github は href として保持される
  await page.goto('/#/contact');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('a[href="https://github.com/e2e-test-acct"]')).toBeVisible();

  // 危険スキームの linkedin は描画されない (サニタイズで '' に落ちて条件描画が抑止)
  expect(await page.locator('a[href^="javascript:"]').count()).toBe(0);
});


// ===== 7.2: import mode select が再描画後も visual 選択を保持する (#7cbc4d9 class) =====
// settingsImportMode select の onchange は window.render() を直接呼び設定ページを完全再描画する。
// 修正前は h('select', { value: settingsImportMode }) が el.setAttribute('value', ...) 経由となり、
// <select> の value は content attribute に反映されない HTML 仕様のため初回再描画で最初の option
// ('append') に戻っていた。修正後は各 option に selected: mode===cur ? true : undefined で
// h() の undefined-skip (line 128) を活用する — projects-page と同パターン。
test('Settings import mode select retains visual selection after re-render (#7cbc4d9 class)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const sel = page.locator('select[aria-label="インポートモード"]');
  await expect(sel).toBeVisible();

  // 初期値 'append'
  await expect(sel).toHaveValue('append');

  // 'upsert' に変更 → 値が反映される
  await sel.selectOption('upsert');
  await expect(sel).toHaveValue('upsert');

  // [FIX] **離脱して戻る**ところまで見る。#1054 でこのトグルを部分更新へ変えた (全再描画が
  //   隣の file input を差し替えて import を取りこぼしていたため) 結果、同一ページに留まる限り
  //   select は作り直されず、`selected:` を外しても値が保たれてしまう (= この test が守っている
  //   性質を検査しなくなり、対応する mutation が SURVIVED した)。ページを作り直すのは
  //   **ルートを離れて戻ったとき**で、そこでは module state から `selected:` で復元する必要が
  //   ある。外すと 'append' へ戻る (実測)。
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'About' })).toBeVisible();
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await expect(page.locator('select[aria-label="インポートモード"]'),
    'ルートを離れて戻るとインポートモードの選択が失われている (state と UI の desync)').toHaveValue('upsert');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `import mode select caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.1: localStorage 自体が使えない環境で SPA が動作する (private mode 等) =====
// Safari のプライベートブラウジングやストレージ遮断設定では localStorage への **アクセス自体** が
// SecurityError を投げる (quota 超過 = 書き込み失敗とは別クラス)。storage.js の try/catch と
// theme-init.js の早期ガードがこれを吸収しているが、この堅牢性は e2e 未被覆で、将来 module scope に
// 素の localStorage アクセスが 1 つ混ざるだけで **その環境の全ユーザーが白画面**になり得た。
// localStorage getter が例外を投げる状態でトップが描画され fatal も pageerror も出ないことを固定する。
test('SPA still renders when localStorage access itself throws (private-mode class)', async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', {
      configurable: true,
      get() { throw new DOMException('The operation is insecure.', 'SecurityError'); }
    });
  });
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(e.message));

  await page.goto('/#/');
  await page.waitForLoadState('domcontentloaded');

  // 実コンテンツが描画される (白画面や FatalPage でない)
  await expect(page.locator('h1').first()).toBeVisible();
  await expect(page.locator('#content')).not.toBeEmpty();
  await expect(page.locator('#fallback-details')).toHaveCount(0);

  // 別ルートへ遷移しても壊れない (保存を伴う経路も含む)
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByLabel('やることを入力')).toBeVisible();
  await page.getByLabel('やることを入力').fill('NO-STORAGE-TODO-9950');
  await page.getByLabel('やることを入力').press('Enter');
  await expect(page.getByText('NO-STORAGE-TODO-9950')).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `localStorage 不在で fatal: ${fatal}`).toBeNull();
  expect(pageErrors, `localStorage 不在で uncaught error: ${pageErrors.join(' / ')}`).toEqual([]);
});


// ===== 7.1: crypto.randomUUID 不在でも一意 ID 生成が壊れない (非セキュアコンテキスト) =====
// `crypto.randomUUID` は **セキュアコンテキスト限定** API で、http:// の LAN プレビュー
// (例: PC の http-server を同一 LAN のスマホから開く) では undefined になる。pure-utils.js の
// generateId は Math.random ベースの RFC 4122 互換フォールバックを持つが e2e 未被覆で、
// フォールバックを失うと **その閲覧経路でだけ** 項目追加が例外になり誰も気付けなかった。
// randomUUID を undefined にした状態でプロジェクト追加が成功し uncaught error も出ないことを固定する。
test('Item creation still works when crypto.randomUUID is unavailable (insecure-context class)', async ({ page }) => {
  await page.addInitScript(() => {
    try { Object.defineProperty(crypto, 'randomUUID', { configurable: true, value: undefined }); } catch (e) { /* noop */ }
  });
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(e.message));

  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  expect(await page.evaluate(() => typeof crypto.randomUUID), 'probe 前提: randomUUID は不在').toBe('undefined');

  const name = 'NO-UUID-PROJ-9960';
  await page.getByPlaceholder('プロジェクト名').fill(name);
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();

  // 公開一覧にも出る (= 生成した id/slug が正常に機能している)
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
  await expect(page.getByText(name).first()).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `randomUUID 不在で fatal: ${fatal}`).toBeNull();
  expect(pageErrors, `randomUUID 不在で uncaught error: ${pageErrors.join(' / ')}`).toEqual([]);
});


// ===== 複数アプリの状態が「同時に」共存してリロードを跨ぐ (cross-app 統合) =====
// 各アプリの永続化は個別に e2e 被覆されているが、いずれも **そのアプリ単独** の往復しか見ていない。
// 実際のユーザーは複数アプリを行き来し、State には task / todo / notes / quiz 検索語が同居する。
// 片方の保存経路がもう片方を巻き戻す class の回帰 (draft の取り違え / normalize の落とし穴 /
// scheduleSave の欠落による最後の silent 書き込みの喪失) は、単体テストを全て緑のまま通過する:
//   - State.update 経由 (task/todo) と State.updateSilently 経由 (notes/quiz 検索語) は
//     **別経路**であり、後者は notify せず scheduleSave だけで永続化する。
//   - よって「update 経由は残るが updateSilently 経由だけ消える」退行が起こりうる。
// 4 アプリを 1 セッションで触ってから 1 回だけリロードし、**全部が同時に残っている**ことを検証する。
test('State written across four apps in one session all survives a single reload (no cross-app clobber)', async ({ page }) => {
  const TASK = 'CROSSAPP-タスク-4821';
  const TODO = 'CROSSAPP-TODO-4821';
  const NOTE = '# CROSSAPP-ノート-4821';
  const QUERY = 'CROSSAPP検索';

  // 1. task (State.update 経由)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await page.locator('#task-input').fill(TASK);
  await page.locator('#task-input').press('Enter');
  await expect(page.locator('#content')).toContainText(TASK);

  // 2. todo (State.update 経由)
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');
  await page.locator('#todo-input').fill(TODO);
  await page.locator('#todo-input').press('Enter');
  await expect(page.locator('#content')).toContainText(TODO);

  // 3. notes (State.updateSilently 経由 — notify せず scheduleSave のみ)
  await page.goto('/#/apps/notes');
  await page.waitForLoadState('domcontentloaded');
  await page.locator('#notes-input').fill(NOTE);

  // 4. quiz 検索語 (State.updateSilently 経由・種別付きで保持される)
  await page.goto('/#/quiz?type=aws');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('searchbox').first().fill(QUERY);

  // 1 回だけリロード = 実ユーザーの離脱→再訪に相当
  await page.reload();
  await page.waitForLoadState('domcontentloaded');

  // 4 つすべてが同時に残っていること (どれか 1 つでも消えれば cross-app clobber)
  await expect(page.getByRole('searchbox').first()).toHaveValue(QUERY);

  await page.goto('/#/apps/notes');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#notes-input')).toHaveValue(NOTE);

  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content')).toContainText(TASK);

  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content')).toContainText(TODO);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `cross-app persistence caused a fatal: ${fatal}`).toBeNull();
});

// ===== 採用される経路の敵対的ストア（parse でき schema も一致するが各フィールドの型が壊れている） =====
// 既存の resilience テストは「壊れた JSON」「schema 不一致」「storage 例外」を被覆するが、
// いずれも **store が採用されない** 経路。ここで守るのはその逆 — **parse でき schemaVersion も
// 一致するので実際に adopt され、normalize を通って描画まで到達する** 経路である。
// #968 / #969 / #970 は import 側の同じ形（`[]` / `{}` / null が必須フィールドに入る）で
// 実バグ（宛先の消えた mailto / "[object Object]" の描画）を出しており、初回ロードは
// **import とは別の入口**（JSON.parse・schemaVersion gate・boot 時 State.set）を通る。
//
// **schemaVersion をハードコードしない**: 最初にアプリ自身へ 1 件保存させ、書き出された
// schemaVersion を読み取ってから種を蒔く。ハードコードすると版数が上がった瞬間に全ケースが
// 「schema 不一致 → 既定」経路へ落ち、**何も検査していないのに緑**になる（このテストを
// 書く過程で実際にそうなった: 45 と決め打ちして 14 ケース全部が同じ経路を測っていた）。
// さらに control ケース（正常な store）を先頭に置き、種蒔き自体が効いていることを毎回確認する。
test('Hostile-but-adoptable localStorage: every field type survives the boot path', async ({ page }) => {
  const KEY = 'portfolio_enhanced_v45';

  // (1) アプリ自身に 1 度保存させ、現行 schemaVersion を実行時に得る
  await page.goto('/#/apps/todo', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();
  await page.getByPlaceholder(/.*/).first().fill('schema-probe');
  await page.keyboard.press('Enter');
  await expect.poll(async () => page.evaluate((k) => {
    try { return JSON.parse(localStorage.getItem(k)).schemaVersion; } catch (e) { return null; }
  }, KEY)).not.toBeNull();
  const V = await page.evaluate((k) => JSON.parse(localStorage.getItem(k)).schemaVersion, KEY);

  const CASES = [
    // control: 正常な store が **実際に採用される** ことを先に確認する（種蒔きの非 vacuity 検査）
    ['control(正常)', { schemaVersion: V, projects: [{ id: 'p_seed', slug: 'seed-proj', name: 'SEEDED-PROJECT', category: 'Misc', summary: 's' }], appsData: {}, profile: {} }, true],
    ['projects 欠落', { schemaVersion: V, appsData: {}, profile: {} }, false],
    ['全フィールド null', { schemaVersion: V, projects: null, appsData: null, profile: null }, false],
    ['projects が object', { schemaVersion: V, projects: { a: 1 }, appsData: {}, profile: {} }, false],
    ['projects に null/数値/文字列 要素', { schemaVersion: V, projects: [null, 0, 'x'], appsData: {}, profile: {} }, false],
    ['appsData.tasks が null 要素', { schemaVersion: V, projects: [], appsData: { tasks: [null, null] }, profile: {} }, false],
    ['projectPrefs が文字列', { schemaVersion: V, projects: [], appsData: {}, profile: {}, projectPrefs: 'x' }, false],
    ['hiddenIds が object', { schemaVersion: V, projects: [], appsData: {}, profile: {}, projectPrefs: { hiddenIds: { a: 1 } } }, false],
    ['profile が配列', { schemaVersion: V, projects: [], appsData: {}, profile: [] }, false],
    ['appsData が配列', { schemaVersion: V, projects: [], appsData: [], profile: {} }, false],
    ['巨大 name (50k 文字)', { schemaVersion: V, projects: [{ id: 'p_big', slug: 'big', name: 'あ'.repeat(50000) }], appsData: {}, profile: {} }, false],
    ['__proto__ を含む store', JSON.parse(`{"schemaVersion":${V},"__proto__":{"polluted":"YES"},"projects":[],"appsData":{},"profile":{}}`), false],
  ];

  for (const [label, store, expectSeed] of CASES) {
    const ctx = await page.context().newPage();
    await ctx.addInitScript(([k, v]) => { try { localStorage.setItem(k, v); } catch (e) { /* noop */ } }, [KEY, JSON.stringify(store)]);
    await ctx.goto('/#/projects', { waitUntil: 'domcontentloaded' });
    await expect(ctx.locator('#content h1')).toBeVisible();

    const st = await ctx.evaluate(() => {
      const text = (document.getElementById('content')?.textContent || '');
      return {
        fatal: window.__fatalError ? window.__fatalError.message : null,
        len: text.trim().length,
        seeded: text.includes('SEEDED-PROJECT'),
        objectObject: (text.match(/\[object Object\]/g) || []).length,
        polluted: ({}).polluted,
      };
    });
    await ctx.close();

    expect(st.fatal, `${label}: boot が fatal になった (${st.fatal})`).toBeNull();
    expect(st.len, `${label}: 実質空のページが描画された`).toBeGreaterThan(20);
    expect(st.objectObject, `${label}: "[object Object]" が描画された`).toBe(0);
    expect(st.polluted, `${label}: プロトタイプ汚染が起きた`).toBeUndefined();
    if (expectSeed) {
      // 種蒔き経路が生きていることの確認。ここが落ちたら以降のケースは
      // 「adopt されない store」を測っているだけで無意味 (vacuous) になる。
      expect(st.seeded, `${label}: 正常な store が採用されていない — 種蒔きが効いておらず、以降のケースは vacuous`).toBe(true);
    }
  }
});

// ===== 足元の state が変わったときの詳細ページ =====
// 詳細ページを開いたまま、その project が **別の画面から消える**経路がある
// (Settings の削除 / 別タブの更新 / import)。project を無条件に dereference していると
// ここで FatalPage になる —— #93 / #295 / #561 / #568 で繰り返し出た ingestion-crash と
// 同じ形が「参照側」に出る版。実測 (#1008) では graceful に「見つかりません」へ落ちており
// 正しいが、**この経路を踏むテストが一つも無かった**ので固定する。
test('開いている詳細ページのプロジェクトを削除しても FatalPage にならない', async ({ page }) => {
  // デフォルトは削除不可なので、ユーザー追加のプロジェクトを 1 件作る
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.locator('#settingsNewName').fill('消えるプロジェクト');
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.getByRole('button', { name: '削除：消えるプロジェクト' })).toBeVisible();

  await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  await page.getByRole('button', { name: '詳細を見る：消えるプロジェクト' }).first().click();
  await expect(page.locator('#content h1', { hasText: '消えるプロジェクト' })).toBeVisible();
  const detailUrl = page.url();

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  page.once('dialog', d => d.accept());
  await page.getByRole('button', { name: '削除：消えるプロジェクト', exact: true }).first().click();
  await expect(page.getByRole('button', { name: '削除：消えるプロジェクト' })).toHaveCount(0);

  // 消えた詳細 URL へ戻る (ブックマークや履歴から来るのと同じ状況)
  await page.goto(detailUrl, { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toHaveText('プロジェクトが見つかりません');

  // NOTE: fatal の検査は「起きていないこと」なので poll を使わず、上の positive assertion で
  //   描画成立を待ってから 1 度だけ読む (#984 で踏んだ assertion race の回避)。
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `削除済みプロジェクトの詳細 URL で fatal: ${fatal}`).toBeNull();
});

// 非同期の応答待ち (AI ページの 300ms) の最中に、別ルートで全データをリセットする。
// 応答が返ったときに参照する state は既に置き換わっているので、State.update の中で
// 消えた枝を触ると crash する形になりうる。
test('AI の応答待ちの最中に全リセットしても FatalPage にならない', async ({ page }) => {
  await page.goto('/#/apps/ai', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();
  await page.locator('#ai-input').fill('設計について教えて');
  await page.getByRole('button', { name: '送信', exact: true }).click();

  // 応答が返る前に別ルートへ移り、全リセットする
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  page.once('dialog', d => d.accept());
  await page.getByRole('button', { name: '全リセット', exact: true }).click();

  // 応答の setTimeout(300ms) を確実に跨いでから、両ルートの健全性を確認する
  await page.waitForTimeout(900);
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  let fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `全リセット直後に fatal: ${fatal}`).toBeNull();

  await page.goto('/#/apps/ai', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();
  await expect(page.locator('#ai-input')).toBeVisible();
  fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `リセット後の AI ページで fatal: ${fatal}`).toBeNull();

  // control: そもそもリセットが効いていることを確かめる。これが無いと、リセットが
  // 何らかの理由で走らなかった場合に「何も起きなかったから緑」という**何も検証しない緑**になる
  // (schemaVersion 決め打ちで 14 ケース全滅させた過去の失敗と同型)。
  const history = await page.evaluate(() => {
    const raw = localStorage.getItem('portfolio_enhanced_v45');
    if (!raw) { return 'no-store'; }
    const d = JSON.parse(raw);
    return (d.appsData && Array.isArray(d.appsData.ai && d.appsData.ai.history))
      ? d.appsData.ai.history.length : 'no-history';
  });
  expect(history, `全リセットが効いていない (AI 履歴が残っている: ${history}) — `
    + 'この test はリセットが走った上で fatal が出ないことを検証するものなので、'
    + 'リセット自体が走っていないと何も検証していないことになる').not.toBeGreaterThan(0);
});


// ===== localStorage がどんな形で壊れていても起動できる =====
// 既存の resilience テストは「壊れた JSON / schema 不一致 / storage 例外」を見ているが、
// **保存値の形そのものが想定外**のケース (トップレベルが配列 / 文字列 / 数値 / null / 空文字、
// 未来の schemaVersion、projects が数値) は通っていなかった。
// localStorage は利用者が devtools で編集でき、別バージョンや別タブが書き、拡張機能が
// 触ることもある —— **アプリが最初に読む外部入力**なので、ここで落ちると
// 「サイトが真っ白で何もできない」という最悪の壊れ方になる。しかも当人の環境でしか
// 再現しないので報告からの特定も難しい。
// 実測ではすべて既定 store へフォールバックして正常起動する。その graceful さを固定する。
test('localStorage がどんな形で壊れていても既定 store で起動する', async ({ page }) => {
  const CASES = [
    ['壊れた JSON', '{"schemaVersion":12,'],
    ['トップレベルが配列', '[1,2,3]'],
    ['トップレベルが文字列', '"hello"'],
    ['null リテラル', 'null'],
    ['数値', '42'],
    ['空文字', ''],
    ['旧 schema', '{"schemaVersion":1,"projects":[]}'],
    ['未来 schema', '{"schemaVersion":9999,"projects":[]}'],
    ['projects が数値', '{"schemaVersion":12,"projects":42}'],
  ];

  for (const [label, raw] of CASES) {
    await page.addInitScript((r) => {
      try { localStorage.setItem('portfolio_enhanced_v45', r); } catch { /* noop */ }
    }, raw);
    await page.goto('/#/projects');
    await page.waitForLoadState('domcontentloaded');

    await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' }),
      `${label}: プロジェクト一覧が描画されない`).toBeVisible();

    const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
    expect(fatal, `${label}: FatalPage に落ちた — ${fatal}`).toBeNull();

    // control: 既定 store へフォールバックしている (0 件なら「描画された」だけで中身が無い)
    expect(await page.locator('.grid-projects article.card').count(),
      `${label}: 既定プロジェクトが 1 件も出ていない`).toBeGreaterThan(1);
  }
});


// ===== URL サニタイズの古典的な回避手口が通らない =====
// 上のテストは素の `javascript:` を見ているが、実際の攻撃では **大文字混在** や
// **前後の空白** で単純な前方一致チェックをすり抜けようとする。`data:` / `vbscript:` も
// 同じく描画されると危険。safeUrl は `.trim()` してから `^https?://` を試すので現状は
// すべて弾けるが、「たまたま弾けている」のか「意図して弾いている」のかは実測しないと
// 分からない —— 実装を素朴な `startsWith('javascript:')` へ変えると通ってしまう形なので、
// **回避手口ごと**に固定する。
//
// 1 ケース 1 コンテキストで確認する (import は debounce 保存と絡み、同じページの使い回しでは
// 条件が壊れる・#1080 で実測)。
test('URL サニタイズが大文字混在・前後空白・data:/vbscript: を弾く', async ({ browser }) => {
  const BYPASS = [
    ['大文字混在', 'JaVaScRiPt:alert(1)'],
    ['前後空白', '   javascript:alert(1)   '],
    ['data スキーム', 'data:text/html,<script>alert(1)</script>'],
    ['vbscript スキーム', 'vbscript:msgbox(1)'],
  ];

  const hrefsFor = async (github) => {
    const context = await browser.newContext();
    try {
      const page = await context.newPage();
      await page.addInitScript((v) => {
        localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
          schemaVersion: 12, type: 'full-store',
          profile: { title: 'T', bio: '', email: 'a@b.co', github: v, linkedin: '', location: '' }
        }));
      }, github);
      await page.goto('/#/contact');
      await page.waitForLoadState('domcontentloaded');
      await expect(page.locator('#content h1').first()).toBeVisible();
      return page.evaluate(() => Array.from(document.querySelectorAll('#content a')).map((a) => a.getAttribute('href')));
    } finally {
      await context.close();
    }
  };

  for (const [label, value] of BYPASS) {
    const hrefs = await hrefsFor(value);
    expect(hrefs.some((h) => /^(javascript|data|vbscript):/i.test((h || '').trim())),
      `${label}: 危険スキームの href が描画されている — ${JSON.stringify(hrefs)}`).toBe(false);
  }

  // control: 正常な URL は描画される (何でも落としていたら検査になっていない)
  expect(await hrefsFor('https://github.com/e2e-bypass-control'),
    'control: 正常な URL まで落としている').toContain('https://github.com/e2e-bypass-control');
});


// ===== debounce 前に離脱しても書きかけが失われない (visibilitychange flush) =====
// 保存は `scheduleSave()` の debounce (CONSTANTS.DEBOUNCE_DELAY = 150ms) 越しに行われるので、
// 最後の打鍵から 150ms 以内にリロード/タブ終了すると **書きかけがそのまま消えうる**。
// それを防いでいるのは state.js の visibilitychange(hidden) → saveNow() の 1 本だけで、
// この increment まで **その機構を見ているテストが 1 つも無かった**。
//
// 失われ方が「エラー」ではなく「戻ったら数文字前の状態」なので、利用者は自分の打ち間違いと
// 区別できない。fatal も視覚差分も出ないため behavior test 以外に捕捉層が無い。
//
// 非 vacuity は実測済み: visibilitychange リスナーを外すと本テストは RED になる。
//
// 測定上の注意 (実際に 1 度誤診した):
//   textarea を click してから type すると **既定文のキャレット位置に挿入**されるので、
//   `inputValue().slice(0, N)` で先頭だけ見ると挿入部に届かず「消えた」と誤読する。
//   包含 (`toContain`) で見ること。
test('debounce 前にリロードしても書きかけのノートが失われない', async ({ page }) => {
  await page.goto('/#/apps/notes');
  await expect(page.locator('#content h1')).toBeVisible();

  const ta = page.locator('#content textarea').first();
  await ta.click();
  await page.keyboard.type('FLUSH-BEFORE-RELOAD');

  // control: そもそも打鍵が textarea に届いている (届いていなければ以降は何も検査しない)
  await expect(ta).toHaveValue(/FLUSH-BEFORE-RELOAD/);

  // debounce を待たずに離脱する
  await page.reload();
  await expect(page.locator('#content h1')).toBeVisible();

  await expect(page.locator('#content textarea').first(),
    'debounce 前の離脱で書きかけが消えた — state.js の visibilitychange(hidden) → saveNow() が '
    + '唯一の防波堤なので、そこが外れると最後の打鍵から 150ms 以内の入力が黙って失われる'
  ).toHaveValue(/FLUSH-BEFORE-RELOAD/);
});


// ===== JavaScript が無効でも「説明のある画面」を出す =====
// 実測 (2026-08-17・修正前): JS を切ると `#content` は空のまま、可視の見出しは **0 個**、
// 可視テキストは sr-only の AIO エンティティアンカーだけで、利用者には **説明の無い白紙**
// にしか見えなかった。`<noscript>` は index.html に 2 つあるが、どちらもフォントの
// stylesheet 用で利用者向けの文言は無かった。
//
// このサイトは Vanilla JS の SPA (C1) なので JS 無しで動かないこと自体は設計どおり。
// だが **「白紙」と「動かない理由が書いてある」は別物**で、§3(B) が死守すると定めた
// 機能性は loads / displays / **comprehensible**。採用担当が JS を切った環境で開いた
// ときに何も分からないのは、その最後の 1 つを満たしていない。
//
// noscript の中身は **JS 有効時には要素として DOM に入らない**ので、通常描画も
// screenshot baseline も不変 (同じテストで漏れが無いことも確認する)。
test('JavaScript 無効時に説明メッセージが表示される', async ({ browser }) => {
  const ctx = await browser.newContext({ javaScriptEnabled: false });
  const page = await ctx.newPage();
  await page.goto('/', { waitUntil: 'domcontentloaded' });

  // NOTE: `expect(body).toContainText(...)` は使わない。javaScriptEnabled: false の
  //   コンテキストでは Playwright の body テキスト抽出が noscript 配下を拾わず、
  //   **中身が正しく描画されていても落ちる** (実測: 同じ状態で h1 の
  //   allTextContents() は正しく返る)。要素そのものを locator で指す。
  const heading = page.locator('h1');
  expect(await heading.count(), 'JS 無効時に見出しが無い — 利用者には白紙にしか見えない').toBe(1);
  expect(await heading.textContent(), 'JS 無効時の説明文が出ていない')
    .toContain('JavaScript を有効にしてください');
  // 機械可読な形で読みたい相手への導線も出す。
  //   **noscript 配下にスコープする** —— index.html には sr-only の AIO ブロックにも
  //   llms-full.txt へのリンクがあるので、スコープ無しだと noscript が無くても 1 件以上
  //   マッチして **何も検査しない緑**になる (実測: スコープ無しは 2 件)。
  expect(await page.locator('noscript a[href$="llms-full.txt"]').count(),
    'JS 無効時に権威コンテキストへの導線が無い').toBe(1);

  await ctx.close();
});

test('JavaScript 有効時に noscript の内容が漏れない', async ({ page }) => {
  // 上のテストの対。noscript が誤って通常描画へ混入すると、全ページの先頭に
  // 「JavaScript を有効にしてください」が出る (screenshot は ADVISORY なので気付けない)。
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1').first()).toBeVisible();
  const leaked = await page.evaluate(() => document.body.innerText.includes('JavaScript を有効に'));
  expect(leaked, 'noscript の内容が JS 有効時にも描画されている').toBe(false);
});
