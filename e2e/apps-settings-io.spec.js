const { test, expect } = require('@playwright/test');

// ===== 通知の検証は sr-only の通知領域で行う (toast は 3 秒で自動消滅する) =====
// [FIX] `#toast-container` のテキストを待つ assertion は **CI 負荷で間欠 RED** になる。
//   Toast は `duration = 3000ms` で自動消滅するため、import / snapshot のような重い操作の
//   あとに読むと「出て、消えたあと」に評価されうる (実測 #1018: CI で
//   `インポートが完了しました` が element(s) not found で落ち、ローカル 3/3 + CI 再実行では緑)。
//   `Toast.show` は必ず `announce(message)` で `#action-announcement` にも同じ文言を書き、
//   そちらは **次の通知まで消えない**。通知チャネルは #901 でこの sr-only 領域へ一本化済みで
//   (Check 407 が単一 writer を強制)、こちらを見るのが意味論的にも正しい。
//   視覚 toast そのものの表示は apps-pomodoro.spec.js 側で引き続き検証している。
async function expectNotified(page, text) {
  await expect(page.locator('#action-announcement')).toContainText(text);
}

const fs = require('fs');




// ===== 7.2: 設定アプリのデータエクスポート整合性 Behavior Check =====
// #/settings の「フルバックアップ」は downloadJSON(State.get()) で blob を生成し
// portfolio_full_<ts>.json として download する (data-integrity 機能)。CRUD とは別系統の
// 「State 全体を妥当な JSON として書き出せるか」を、Playwright の download イベントで動的検証。
test('Settings app exports a full backup as a valid JSON download', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const exportBtn = page.getByRole('button', { name: 'フルバックアップ' });
  await expect(exportBtn).toBeVisible();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    exportBtn.click(),
  ]);
  expect(download.suggestedFilename()).toMatch(/^portfolio_full_\d+\.json$/);

  // ダウンロード本体が State の妥当な JSON であること
  const content = fs.readFileSync(await download.path(), 'utf8');
  const parsed = JSON.parse(content);
  expect(parsed, 'export must contain the appsData State slice').toHaveProperty('appsData');
});


// ===== 7.2: 部分エクスポート (Projectsのみ / AppsDataのみ / Profileのみ) のスライス整合 =====
// exportProjects/Apps/Profile は downloadJSON で State の各スライス (projects 配列 / appsData /
// profile) を別ファイル名で書き出す。フルバックアップは被覆済みだが、部分エクスポートが「正しい
// スライスだけ」を出すか (誤って full store を出していないか) は未カバーだった。各ボタンの download
// 内容の shape + ファイル名 + 負アサーション (他スライスを含まない) を実検証する。
test('Settings partial export buttons download the correct State slice', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // Projectsのみ → projects 配列
  const [dlP] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Projectsのみ' }).click(),
  ]);
  expect(dlP.suggestedFilename()).toMatch(/^portfolio_projects_\d+\.json$/);
  const projects = JSON.parse(fs.readFileSync(await dlP.path(), 'utf8'));
  expect(Array.isArray(projects), 'projects export must be an array').toBe(true);
  expect(projects.length).toBeGreaterThan(0);

  // AppsDataのみ → appsData (tasks を持つ object・full store ではない)
  const [dlA] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'AppsDataのみ' }).click(),
  ]);
  expect(dlA.suggestedFilename()).toMatch(/^portfolio_apps_\d+\.json$/);
  const apps = JSON.parse(fs.readFileSync(await dlA.path(), 'utf8'));
  expect(apps).toHaveProperty('tasks');
  expect(apps, 'appsData export must NOT be the full store').not.toHaveProperty('projects');

  // Profileのみ → profile (email を持つ object・appsData を含まない)
  const [dlPr] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Profileのみ' }).click(),
  ]);
  expect(dlPr.suggestedFilename()).toMatch(/^portfolio_profile_\d+\.json$/);
  const profile = JSON.parse(fs.readFileSync(await dlPr.path(), 'utf8'));
  expect(profile).toHaveProperty('email');
  expect(profile, 'profile export must NOT contain appsData').not.toHaveProperty('tasks');
});


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


// ===== 7.2: JSON インポート (upsert) のラウンドトリップ — 新規 project 追加 + profile 保全 =====
// Settings の importJSON は file アップロードを起点に projects を append/upsert/strict でマージし、
// 末尾で validateAndNormalize を通す data-integrity 経路。export 側はテスト済だが round-trip の
// 危険な半分 = import 側は未カバーで、ここは過去に 2 大データ損失バグの発生源だった:
//   #192 = upsert モードが「未知 id を push 後に Map.values() で上書き」して新規 project を破棄、
//   #139 = validateAndNormalize が profile の github/linkedin/location を strip。
// 本テストは upsert モードで「新規 project + profile フィールド」を含む JSON を setInputFiles で
// アップロードし、(1) 新規 project が公開一覧に追加される (#192 guard)、(2) profile の github が
// Contact に保持表示される (#139 guard)、を実検証する。import 経路が壊れたら退行検知。
test('Settings JSON import (upsert) adds a new project and preserves profile fields (round-trip)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // upsert モードを選択 (#192 が起きたモード)。対象 = Profile + Projects (既定で全 ON)。
  await page.getByLabel('インポートモード').selectOption('upsert');

  const projName = 'E2E-IMPORT-UPSERT-PROJ-5571';
  const ghUrl = 'https://github.com/e2e-import-test';
  const payload = {
    schemaVersion: 12,
    type: 'full-store',
    // profile.name はテストで非アサート。Check 58 の route 抽出 (name:'<lowercase>') と衝突しないよう
    // 大文字始まりにする (小文字literal だと profile name が e2e route と誤認され Check 58 が赤化する)。
    profile: { name: 'ImportUser', title: 'AI-Driven PM', bio: '', email: 'x@example.com', github: ghUrl, linkedin: '', location: 'E2E-CITY-5571' },
    projects: [
      { id: 'p_e2e_import_5571', slug: 'e2e-import-upsert-5571', name: projName, category: 'User Added', summary: 'imported via upsert', tech: ['JS'], tags: [], demoRoute: null },
    ],
  };

  // file input (accept=application/json) へ in-memory バッファをアップロード
  await page.getByLabel('インポートする JSON ファイルを選択').setInputFiles({
    name: 'backup.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(payload)),
  });
  await expectNotified(page, 'インポートが完了しました');

  // (1) #192 guard: upsert で新規 project が破棄されず公開一覧に追加される
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(projName).first()).toBeVisible();

  // (2) #139 guard: validateAndNormalize が profile.github を strip せず Contact に保持表示する
  await page.goto('/#/contact');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByRole('link', { name: ghUrl })).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `JSON import caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: strict モードで malformed projects を import しても壊れない (未テストの ingestion 経路 coverage) =====
// 既存 import テストは upsert + valid data のみ。strict（全置換）モードで parsed.projects に null/非
// オブジェクト entry を含む malformed JSON を import する経路は未カバーだった。strict は
// `merged.projects = parsed.projects` の生代入で normalize を通ってから State.set される（restoreSnapshot と
// 同じ「外部 ingestion は adopt する前に validateAndNormalize を通せ」#295/#561 invariant・importJSON も
// 本 increment で raw State.update→後 normalize から normalize-before-commit へ整合させた）。malformed
// strict import 後に (1) FatalPage に落ちず設定 UI が生きている、(2) 正規化で null/文字列 entry は除去され
// valid entry は残る、を実検証し、この ingestion 経路が壊れたら（normalize が外れる等）退行検知する。
// upsert/append は p.id を deref するため malformed entry で commit 前に throw し error toast になる別経路。
test('Settings strict import of malformed projects stays graceful (untested ingestion path)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // strict（全置換）を選択。null / 非オブジェクト entry を含む malformed projects を送る。
  await page.getByLabel('インポートモード').selectOption('strict');
  const payload = {
    schemaVersion: 12,
    type: 'full-store',
    projects: [null, 'not-an-object', { id: 'p_e2e_ok_8801', name: 'OK-STRICT-8801', category: 'User Added' }],
  };
  await page.getByLabel('インポートする JSON ファイルを選択').setInputFiles({
    name: 'malformed.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(payload)),
  });
  await expectNotified(page, 'インポートが完了しました');

  // 修正前は生 projects の render crash で __fatalError が set され FatalPage に stuck していた。
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `malformed strict import caused a fatal: ${fatal}`).toBeNull();

  // 設定 UI が生きている (FatalPage でなく正規の設定画面が描画されている)
  await expect(page.getByRole('heading', { name: '整合性チェック / 正規化' })).toBeVisible();

  // 正規化で malformed entry (null / 文字列) は除去され、valid entry は残る
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('OK-STRICT-8801').first()).toBeVisible();
});


// ===== 7.2: import のファイル読み込み失敗 (FileReader onerror) に明示フィードバックを出す =====
// importJSON は onload (parse+commit) と、その中の JSON.parse 失敗 (catch→error toast) は扱うが、
// FileReader.readAsText 自体の読み込み失敗 (mid-read でファイルが消える / リムーバブルメディア・
// ネットワークドライブ切断 / ブラウザのセキュリティ制約) は従来 onerror 未処理で silent no-op
// (Toast も出ず無反応) になり、ユーザーは成功/失敗を判別できなかった。本テストは window.FileReader を
// readAsText が必ず onerror を発火する stub へ差し替えて読み込み失敗を模し、明示エラー toast が
// 出ることを検証する。onerror ハンドラを外すと toast が出ず RED になる (非 vacuous)。
test('Settings JSON import surfaces an error toast when the file read itself fails (FileReader onerror)', async ({ page }) => {
  // app スクリプトが new FileReader() する前に FileReader を stub へ差し替える。
  await page.addInitScript(() => {
    window.FileReader = class {
      readAsText() {
        // 実 FileReader と同じく非同期に error イベントを発火 (onload は呼ばない)。
        setTimeout(() => { if (typeof this.onerror === 'function') { this.onerror(new Event('error')); } }, 0);
      }
    };
  });
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 有効な JSON を選んでも、読み込み (readAsText) 段階で失敗する経路を通す。
  await page.getByLabel('インポートする JSON ファイルを選択').setInputFiles({
    name: 'backup.json',
    mimeType: 'application/json',
    buffer: Buffer.from('{"schemaVersion":12,"type":"full-store"}'),
  });

  // 読み込み失敗の明示フィードバック (silent no-op でない)。
  await expectNotified(page, 'ファイルの読み込みに失敗しました');

  // 読み込み失敗はデータに触れないので FatalPage に落ちない (設定 UI が生存)。
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `FileReader onerror path caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: スナップショット復元のラウンドトリップ (保存→変更→復元で巻き戻る) =====
// save テスト (#上) は保存と保存日時表示の往復を見るが、復元 (restoreSnapshot → State.set(snap.data))
// で「保存時点へ実際に巻き戻る」中核機能は未カバーだった。これはユーザの undo/復旧の data-integrity
// 経路。タスク A を追加→保存→タスク B を追加→復元、で A は残り B が消える (保存時点へ revert) ことを
// 実検証する。復元が State.set を正しく通し永続データを差し替えることの保証。
test('Settings snapshot restore reverts state to the saved point', async ({ page }) => {
  // 1. タスク A を追加 (保存に含める状態)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  const input = page.locator('#task-input');
  await input.fill('SNAP-TASK-A-7700');
  await input.press('Enter');
  await expect(page.getByText('SNAP-TASK-A-7700')).toBeVisible();

  // 2. スナップショット保存 (A を含む)
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByText(/保存日時:/)).toBeVisible();

  // 3. 保存後にタスク B を追加 (この変更は snapshot に含まれない)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await input.fill('SNAP-TASK-B-7701');
  await input.press('Enter');
  await expect(page.getByText('SNAP-TASK-B-7701')).toBeVisible();

  // 4. 復元 → 保存時点 (A のみ) へ巻き戻る
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '復元', exact: true }).click();
  await expectNotified(page, 'スナップショットを復元しました');

  // 5. タスク画面: A は残り B は消える (= 保存時点へ revert)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('SNAP-TASK-A-7700')).toBeVisible();
  await expect(page.getByText('SNAP-TASK-B-7701')).toHaveCount(0);
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


// ===== 7.2: import の対象 checkbox が未チェックのセクションを skip する (選択的 ingestion gate) =====
// importJSON は `if (settingsIncludeProjects && ...)` 等で対象 checkbox(Profile/Projects/AppsData)ごとに
// セクションを取り込むか判定する。既存 import テストは全 ON(既定)のみで、あるセクションを OFF にすると
// そのセクションだけ skip される選択的 gate は未カバーだった。gate が壊れて常時取り込みになると、
// ユーザーが意図的に除外したデータを上書きしてしまう。本テストは Projects を OFF・AppsData を ON にして
// import し、(1) import 専用 project が公開一覧に出ない(=Projects skip)、(2) 既存の既定 project は残る、
// (3) import 専用 task は反映される(=AppsData 取り込み・非 vacuous に import 経路が動いた証拠) を検証する。
test('Settings import skips a section whose target checkbox is unchecked (selective gate)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByLabel('インポートモード').selectOption('strict');

  // 取り込み前の既定 project 名を 1 つ控える (Projects skip 後も残ることの確認用)。
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  const keptProject = (await page.locator('article.card--flex-col h2').first().innerText()).trim();
  expect(keptProject).not.toBe('');

  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // Projects を OFF、AppsData を ON(既定), Profile は影響回避のため OFF にする。
  // 各 checkbox の onchange は window.render() で settings ページ全体を再描画し file input を作り直す。
  // uncheck 直後に setInputFiles すると、再描画で detach された古い input に file を set して onchange が
  // 発火せず import が起きない race がある (CI 負荷下で間欠 fail)。最終状態を assert して再描画の settle を
  // 保証してから setInputFiles する (checkbox 状態が確定=最後の render 完了の証跡)。
  await page.getByRole('checkbox', { name: 'Projects' }).uncheck();
  await expect(page.getByRole('checkbox', { name: 'Projects' })).not.toBeChecked();
  await page.getByRole('checkbox', { name: 'Profile' }).uncheck();
  await expect(page.getByRole('checkbox', { name: 'Profile' })).not.toBeChecked();

  // [FIX] 上の「状態を assert して settle を待つ」だけでは **CI 負荷で間欠 RED** になる
  //   (実測: `#action-announcement` が空 = import が一度も発火していない)。checkbox の
  //   onchange が起こす再描画は `await yieldToMain()` を挟む**非同期**なので、checkbox の
  //   状態 assert が通った時点ではまだ古い file input が生きており、そこへ file を set すると
  //   **直後に detach されて change が誰にも届かない**。同じ罠は #1040 でも踏んだ。
  //   一度ルートを離れて戻り、描画が確定した DOM を掴んでから set する
  //   (「対象」チェックボックスは factory closure state なので遷移では消えない)。
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  // control: 遷移を跨いでも選択が保持されていること (保持されていなければ gate を測れない)
  await expect(page.getByRole('checkbox', { name: 'Projects' })).not.toBeChecked();
  await expect(page.getByRole('checkbox', { name: 'Profile' })).not.toBeChecked();
  await expect(page.getByRole('checkbox', { name: 'AppsData' })).toBeChecked();
  await expect(page.getByLabel('インポートする JSON ファイルを選択')).toBeVisible();

  const skippedProj = 'IMPORT-SECTION-GATE-PROJ-9930';
  const importedTask = 'IMPORT-SECTION-GATE-TASK-9931';
  const payload = {
    schemaVersion: 12,
    type: 'full-store',
    projects: [
      { id: 'p_gate_9930', slug: 'import-section-gate-9930', name: skippedProj, category: 'User Added', summary: 's', tech: ['JS'], tags: [], demoRoute: null },
    ],
    appsData: { tasks: [{ id: 't_gate_9931', title: importedTask, status: 'backlog', priority: 'med', createdAt: 1 }], todos: [], pomodoro: { history: [], settings: { focus: 25, short: 5, long: 15 }, runtime: {} }, ai: { history: [] }, notes: { content: '' } },
  };
  await page.getByLabel('インポートする JSON ファイルを選択').setInputFiles({
    name: 'gate.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(payload)),
  });
  await expectNotified(page, 'インポートが完了しました');

  // (3) AppsData は ON ゆえ import 専用 task が反映される (import 経路が実際に動いた=非 vacuous)。
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(importedTask)).toBeVisible();

  // (1)(2) Projects は OFF ゆえ import 専用 project は出ず、既存の既定 project は残る (skip が効いた)。
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  // [非 vacuity] 先に既定 project の可視を待つ = projects grid の描画完了を保証してから absence を検査する。
  //   `toHaveCount(0)` を描画前に評価すると async render とレースし、skippedProj がまだ無いだけで
  //   即 pass する vacuous な absence アサーションになる (gate 除去 mutation を素通しする)。描画確定後に
  //   0 件を確認して初めて「skip が効いた」を意味する。
  await expect(page.getByText(keptProject).first()).toBeVisible();
  await expect(page.getByText(skippedProj)).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `selective import gate caused a fatal: ${fatal}`).toBeNull();
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


// ===== スナップショット削除は確認を求める (破壊的操作の非対称の是正) =====
// プロジェクト 1 件の削除 (deleteProjectHard) と全リセット (resetData) は confirm を通すのに、
// **スナップショット削除だけが無確認**だった。スナップショットは単一スロットでありユーザーの
// 唯一の復元点なので、失う影響はむしろプロジェクト 1 件より大きい。
// 「1 ケースだけ処理して他を忘れる」非対称 (CLAUDE.md §7 の反復 class) がデータ喪失面に
// 残っていたもの。キャンセルで **本当に残る** ことまで検証する (確認を出すだけで実際には
// 消えてしまう実装なら、確認は気休めにしかならない)。
test('Deleting the snapshot asks for confirmation and cancelling keeps it', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // スナップショットを保存 → 「削除」が押せる状態になる
  await page.getByRole('button', { name: '保存' }).first().click();
  const delBtn = page.getByRole('button', { name: '削除', exact: true });
  await expect(delBtn).toBeEnabled();

  // (1) 確認ダイアログが出る。文言に「何を失うか」が含まれる
  let dialogMessage = null;
  page.once('dialog', (d) => { dialogMessage = d.message(); d.dismiss(); });
  await delBtn.click();
  await expect.poll(() => dialogMessage, { timeout: 5000 }).not.toBeNull();
  expect(dialogMessage, '復元できなくなる旨が伝わること').toContain('復元できなくなります');

  // (2) キャンセルしたらスナップショットは残る (削除ボタンが有効なまま)
  await expect(delBtn).toBeEnabled();

  // (3) 承認したら実際に削除される (確認が「気休め」でないこと)
  page.once('dialog', (d) => d.accept());
  await delBtn.click();
  await expect(page.getByRole('button', { name: '削除', exact: true })).toBeDisabled();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `snapshot delete confirm caused a fatal: ${fatal}`).toBeNull();
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

// ===== export → import の往復忠実性（バックアップとしての契約） =====
// 既存テストは「部分 export が正しいスライスを落とす」ことと「手書き JSON の import」を
// 見ているが、**アプリ自身が書き出したファイルを import し直して同じ状態に戻るか**は
// 誰も見ていなかった。フル export は利用者にとって**バックアップ**なので、
// export 側で 1 フィールド落ちる（あるいは import 側が無視する）だけで
// **黙ってデータが失われる**。部分 export のテストも手書き JSON の import テストも、
// この経路を通らないので気付けない。
test('full export → 全リセット → import で状態が再現する (backup round-trip)', async ({ page }) => {
  // 特徴的な状態を作る (既定データと区別できる値)
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' })).toBeVisible();
  await page.getByLabel('新しいタスクを入力').fill('RT-タスク');
  await page.getByLabel('新しいタスクを入力').press('Enter');
  await expect(page.locator('#content')).toContainText('RT-タスク');

  await page.goto('/#/apps/notes', { waitUntil: 'domcontentloaded' });
  await page.locator('#notes-input').click();
  await page.keyboard.type('RT-ノート');
  await page.waitForTimeout(600);   // updateSilently の debounce save を確定させる

  const snapshot = () => page.evaluate(() => {
    const raw = localStorage.getItem('portfolio_enhanced_v45');
    const d = raw ? JSON.parse(raw) : {};
    return {
      tasks: ((d.appsData || {}).tasks || []).map(t => t.title).sort(),
      todos: ((d.appsData || {}).todos || []).map(t => t.text).sort(),
      notes: String((d.appsData || {}).notes || ''),
      projects: (d.projects || []).length,
      profileName: (d.profile || {}).name,
    };
  });
  const before = await snapshot();
  expect(before.tasks, 'seed が入っていない — この test の前提が崩れている').toContain('RT-タスク');
  expect(before.notes).toContain('RT-ノート');

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'フルバックアップ', exact: true }).click(),
  ]);
  const file = await download.path();

  page.once('dialog', d => d.accept());
  await page.getByRole('button', { name: '全リセット', exact: true }).click();
  await page.waitForTimeout(600);

  const wiped = await snapshot();
  expect(wiped.tasks, 'リセットが効いていない — import の効果を測れない').not.toContain('RT-タスク');

  await page.selectOption('#settingsImportMode', 'strict');
  await page.setInputFiles('#content input[type="file"]', file);
  await expectNotified(page, 'インポート');
  await page.waitForTimeout(600);

  const after = await snapshot();
  expect(after.tasks, 'export したタスクが import で戻らない').toEqual(before.tasks);
  expect(after.todos, 'export した TODO が import で戻らない').toEqual(before.todos);
  expect(after.notes, 'export したノート本文が import で戻らない').toBe(before.notes);
  expect(after.projects, 'プロジェクト件数が一致しない').toBe(before.projects);
  expect(after.profileName, 'profile が import で戻らない').toBe(before.profileName);
});

// ===== 表示テーマも backup として往復すること =====
// `theme` は full export に含まれるのに **import が無視**しており、「フルバックアップ」を
// 復元しても表示テーマの設定だけが失われていた (実測 #1036: export に `theme:"dark"` が
// 入っていても import 後の store は `"system"`)。export が書くキーを import が読まないのは
// backup 契約の破れで、#139 (profile フィールドが strip される) と同じ data-fidelity class。
//
// 併せて **state を丸ごと置き換える経路 (import / 全リセット / snapshot 復元) は
// Theme.cycle を通らない**ため、`data-theme` と `.dark` が古いまま残っていた
// (リセット後も dark のままで、reload して初めて切り替わる)。描画の入口で state に追随させた。
test('表示テーマが export → import で復元され、リセット直後の表示も stale にならない', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'light' });
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  // 既定 system → dark へ
  await page.evaluate(() => (document.getElementById('themeBtnSidebar') || document.getElementById('themeBtnTop')).click());
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'フルバックアップ', exact: true }).click(),
  ]);
  const file = await download.path();

  page.once('dialog', d => d.accept());
  await page.getByRole('button', { name: '全リセット', exact: true }).click();

  // (1) リセット直後に表示が既定へ戻ること (従来は dark のまま残っていた)
  await expect(page.locator('html'), 'リセットしても表示テーマが古いまま残っている')
    .toHaveAttribute('data-theme', 'system');

  await page.selectOption('#settingsImportMode', 'strict');
  await page.setInputFiles('#content input[type="file"]', file);
  await expectNotified(page, 'インポート');

  // (2) backup のテーマが復元されること (store と表示の両方)
  await expect(page.locator('html'), 'import しても表示テーマが復元されない')
    .toHaveAttribute('data-theme', 'dark');
  const stored = await page.evaluate(() => {
    const raw = localStorage.getItem('portfolio_enhanced_v45');
    return raw ? JSON.parse(raw).theme : null;
  });
  expect(stored, 'backup の theme が store へ復元されていない (export が書くキーを import が読んでいない)')
    .toBe('dark');
});

// ===== 非表示設定も backup として往復すること（公開/非公開の意思） =====
// `projectPrefs.hiddenIds` も full export に入るのに **import が無視**しており、backup を
// 戻すと **意図的に隠したプロジェクトが再び公開状態になっていた** (実測 #1037)。
// 既定プロジェクトは削除できず「非表示」が唯一の非公開手段 (#886) なので、これは単なる
// 表示設定ではなく **公開/非公開の意思**が失われることを意味する。theme (#1036) と同じ
// 「export が書くキーを import が読まない」class。
test('非表示にしたプロジェクトが export → import 後も非表示のまま', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  const visibleCards = async () => {
    await page.goto('/#/projects', { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1', { hasText: 'プロジェクト一覧' })).toBeVisible();
    return page.locator('#content article').count();
  };
  const allCount = await visibleCards();

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.getByRole('button', { name: /^非表示：/ }).first().click();
  await expect(page.getByRole('button', { name: /^表示：/ }).first()).toBeVisible();

  const hiddenCount = await visibleCards();
  // control: そもそも非表示が効いていること
  expect(hiddenCount, '非表示にしても一覧の件数が変わらない — 前提が崩れている').toBe(allCount - 1);

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'フルバックアップ', exact: true }).click(),
  ]);
  const file = await download.path();

  page.once('dialog', d => d.accept());
  await page.getByRole('button', { name: '全リセット', exact: true }).click();
  expect(await visibleCards(), 'リセットで非表示が解除されていない — import の効果を測れない').toBe(allCount);

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.selectOption('#settingsImportMode', 'strict');
  await page.setInputFiles('#content input[type="file"]', file);
  await expectNotified(page, 'インポート');

  expect(await visibleCards(),
    'backup を戻したのに、意図的に隠したプロジェクトが再び公開されている').toBe(allCount - 1);
});
