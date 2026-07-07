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
