const { test, expect } = require('@playwright/test');
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


// ===== 7.2: 設定からのプロジェクト手動追加 (CRUD create → Projects ページ反映 + 永続) =====
// settings の addProjectManual はプロジェクト名を入力→「追加」で s.projects.unshift し slugify する。
// tasks/todos (appsData slice) とは別の projects domain への create 経路で、ProjectsPage の
// hiddenIds フィルタを通って公開一覧に現れる。空入力バリデーション (エラー Toast) と、追加後に
// /#/projects へ反映 + リロード永続を実検証する。projects への書き込み導線が壊れたら退行検知。
test('Settings can add a project manually and it appears on the Projects page', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const nameInput = page.getByPlaceholder('プロジェクト名');
  const addBtn = page.getByRole('button', { name: '追加', exact: true });
  await expect(nameInput).toBeVisible();

  // 空入力バリデーション: エラー Toast、追加されない
  await addBtn.click();
  await expect(page.locator('#toast-container').getByText('プロジェクト名を入力してください')).toBeVisible();

  // 正常追加
  const name = 'E2E-MANUAL-PROJECT-8420';
  await nameInput.fill(name);
  await addBtn.click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();

  // Projects ページ (hiddenIds フィルタ通過) に現れる
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();

  // リロード後も永続
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();
});


// ===== 7.2: 同名プロジェクト追加時の slug 一意化 (詳細ページ到達性) =====
// slugify は決定的なので、同名プロジェクトを 2 つ追加すると slug が重複し、ProjectDetailPage の
// find(p.slug===slug) が先頭のみ返して 2 つ目の詳細が到達不能になるバグがあった。修正で衝突時に
// -2 等を付与して一意化する。同名を 2 件追加し、両方の slug が異なる (= 詳細ページが別個に存在) ことを
// State から実検証する。
test('Adding two projects with the same name yields unique slugs (detail reachability)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const dupName = 'DUP-SLUG-PROJECT-7340';
  const addBtn = page.getByRole('button', { name: '追加', exact: true });
  const nameInput = page.getByPlaceholder('プロジェクト名');

  await nameInput.fill(dupName);
  await addBtn.click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();
  await nameInput.fill(dupName);
  await addBtn.click();

  const readSlugs = () => page.evaluate((nm) => {
    try {
      const st = JSON.parse(localStorage.getItem('portfolio_enhanced_v45'));
      return (st.projects || []).filter(p => p.name === nm).map(p => p.slug);
    } catch { return []; }
  }, dupName);

  // debounce save 完了 (2 件永続) を待つ
  await expect.poll(async () => (await readSlugs()).length).toBe(2);

  // 同名 2 件の slug が一意 (重複しない) こと
  const slugs = await readSlugs();
  expect(new Set(slugs).size, `slugs must be unique: ${JSON.stringify(slugs)}`).toBe(2);
});


// ===== 7.2: プロジェクト非表示/表示トグル (公開一覧の curation) =====
// settings の toggleHiddenProject は projectPrefs.hiddenIds に id を出し入れし、ProjectsPage は
// hiddenIds を filter して公開一覧から除外する (components.js)。これは公開ページの見せ方を制御する
// curation 機能だが従来未カバーだった。カスタムプロジェクトを追加→「非表示」で /#/projects から
// 消える→「表示」で復帰、を実検証する。hiddenIds の State 往復とフィルタ適用の保証。
test('Hiding a project removes it from the public Projects list, unhide restores it', async ({ page }) => {
  // カスタムプロジェクトを追加 (一意名)
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const name = 'HIDE-TOGGLE-PROJ-3050';
  await page.getByPlaceholder('プロジェクト名').fill(name);
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();

  // 公開一覧に出る
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();

  // settings の該当行で「非表示」
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const row = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name });
  await row.getByRole('button', { name: '非表示' }).click();
  // 行に hidden バッジ + 「表示」ボタンへ切替わる
  await expect(row.getByRole('button', { name: '表示' })).toBeVisible();

  // 公開一覧から消える
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name)).toHaveCount(0);

  // 再表示 → 公開一覧へ復帰
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const row2 = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name });
  await row2.getByRole('button', { name: '表示' }).click();
  await expect(row2.getByRole('button', { name: '非表示' })).toBeVisible();

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();
});


// ===== 7.2: プロジェクト並び替え (moveProject ↑/↓ で順序入替) — projects 管理 CRUD 完成 =====
// settings の moveProject(idx, dir) は state.projects[idx] と [idx+dir] を入替える。add/hide/delete は
// 被覆済みだが reorder は未カバーだった。一意名 2 件 (A→B の順で追加 = unshift で [B, A, ...defaults])
// を作り、A の行の「↑」で A を先頭へ繰り上げ、State 上で A が B より前に来る (順序入替) ことを検証する。
// 順序は localStorage State 読み取りで決定的に判定する。
test('Projects can be reordered with the up/down controls', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const nameInput = page.getByPlaceholder('プロジェクト名');
  const addBtn = page.getByRole('button', { name: '追加', exact: true });
  const A = 'REORDER-PROJ-A-6701';
  const B = 'REORDER-PROJ-B-6702';
  await nameInput.fill(A); await addBtn.click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();
  await nameInput.fill(B); await addBtn.click();

  const orderAB = () => page.evaluate((names) => {
    try {
      const st = JSON.parse(localStorage.getItem('portfolio_enhanced_v45'));
      const list = (st.projects || []).map(p => p.name);
      return { a: list.indexOf(names[0]), b: list.indexOf(names[1]) };
    } catch { return { a: -1, b: -1 }; }
  }, [A, B]);

  // 初期は unshift で [B, A, ...] → B が A より前
  await expect.poll(async () => { const o = await orderAB(); return o.a > o.b && o.a >= 0; }).toBe(true);

  // A の行の「↑」で A を 1 つ繰り上げ → A が B より前へ
  const rowA = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: A });
  await rowA.getByRole('button', { name: '↑' }).click();
  await expect.poll(async () => { const o = await orderAB(); return o.a < o.b && o.a >= 0; }).toBe(true);
});


// ===== 7.2: ユーザープロジェクトの削除 (confirm 受諾 → 永久削除) =====
// settings の deleteProjectHard は confirm() 確認の上 s.projects から id で除外する。デフォルト
// プロジェクト (defaultProjectIds) は削除不可 (ボタン disabled) で、ユーザー追加分のみ削除できる。
// add/hide とは別の destructive な CRUD 経路で、confirm ダイアログ + State からの完全除去が
// 従来未カバーだった。カスタム追加→confirm 受諾で削除→ settings リスト + /#/projects 双方から
// 消える、を実検証し projects CRUD (追加/非表示/削除) のカバレッジを完成させる。
test('Deleting a user project (confirm accepted) removes it everywhere', async ({ page }) => {
  // confirm() を常に受諾
  page.on('dialog', (dialog) => dialog.accept());

  // カスタムプロジェクトを追加
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const name = 'DELETE-PROJ-5560';
  await page.getByPlaceholder('プロジェクト名').fill(name);
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();

  // 公開一覧に出る
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();

  // settings の該当行で「削除」(user プロジェクトなので有効) → confirm 受諾
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const row = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name });
  await row.getByRole('button', { name: '削除' }).click();
  // settings リストから行が消える
  await expect(page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name })).toHaveCount(0);

  // 公開一覧からも消える (永続削除)
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name)).toHaveCount(0);
});


// ===== 7.2: destructive 操作の confirm-cancel ガード (data-safety) =====
// deleteProjectHard / resetData は `if (!confirm(...)) return;` で「キャンセル時は何もしない」分岐を
// 持つ。accept 経路は被覆済みだが cancel 経路は未カバーだった。cancel したのに実行されると重大な
// データ損失になるため、confirm を dismiss しても (1) プロジェクトが削除されない (2) データが初期化
// されない、を実検証する。
test('Canceling the delete confirm keeps the project (data-safety)', async ({ page }) => {
  page.on('dialog', (dialog) => dialog.dismiss());

  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const name = 'DELETE-CANCEL-PROJ-8120';
  await page.getByPlaceholder('プロジェクト名').fill(name);
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();

  // 削除 → confirm を dismiss → 行は残る
  const row = page.locator('div.flex.items-center.justify-between.gap-2').filter({ hasText: name });
  await row.getByRole('button', { name: '削除' }).click();
  // dismiss されたので削除されず、公開一覧にも残る
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(name).first()).toBeVisible();
});


test('Canceling the reset confirm keeps data (data-safety)', async ({ page }) => {
  page.on('dialog', (dialog) => dialog.dismiss());

  // タスクを追加
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  const input = page.locator('#task-input');
  await input.fill('RESET-CANCEL-TASK-8121');
  await input.press('Enter');
  await expect(page.getByText('RESET-CANCEL-TASK-8121')).toBeVisible();

  // 全リセット → confirm を dismiss → タスクは残る (初期化されない)
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '全リセット' }).click();
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('RESET-CANCEL-TASK-8121')).toBeVisible();
});


// ===== 7.2: 全データ初期化 (全リセット → confirm → defaults 復帰) =====
// settings の resetData は confirm() の上 State.set(Store.createDefaultStore()) で全状態を初期値へ
// 戻す最も破壊的な操作。snapshot/delete とは別経路で、ユーザーデータ (タスク等) を全消去し
// デフォルトへ戻す導線が未カバーだった。タスクを追加→「全リセット」confirm 受諾→初期化通知 +
// タスクが消えデフォルトに戻ることを実検証する (createDefaultStore への置換が壊れたら検知)。
test('Reset data restores defaults after confirm (destructive)', async ({ page }) => {
  page.on('dialog', (dialog) => dialog.accept());

  // タスクを追加 (デフォルトとの差分を作る)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  const input = page.locator('#task-input');
  await input.fill('RESET-TARGET-TASK-7788');
  await input.press('Enter');
  await expect(page.getByText('RESET-TARGET-TASK-7788')).toBeVisible();

  // 全リセット → confirm 受諾
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '全リセット' }).click();
  await expect(page.locator('#toast-container').getByText('初期化しました')).toBeVisible();

  // タスクが消え defaults に戻る
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('RESET-TARGET-TASK-7788')).toHaveCount(0);
  // crash していない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `reset caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: settings 正規化ボタン (normalizeNow → validateAndNormalize) =====
// 「整合性チェック / 正規化」セクションの「実行」は normalizeNow() で State を
// validateAndNormalize() に通し「正規化を完了しました」を出す (型揺れ/上限超過/破損を安全側に
// 丸めるデータ hygiene)。reset (createDefaultStore) とは別経路で未カバーだった。実行 →
// 完了通知 + crash なし + データ保持 (初期化ではない) を検証する。
test('Settings normalize button runs validateAndNormalize without data loss', async ({ page }) => {
  // 正規化が「初期化」ではないことを示すため、ユーザータスクを 1 件用意
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  const input = page.locator('#task-input');
  await input.fill('NORMALIZE-KEEP-TASK-8810');
  await input.press('Enter');
  await expect(page.getByText('NORMALIZE-KEEP-TASK-8810')).toBeVisible();

  // settings の「整合性チェック / 正規化」セクションの「実行」
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const normSection = page.locator('section.card').filter({ has: page.getByRole('heading', { name: '整合性チェック / 正規化' }) });
  await normSection.getByRole('button', { name: '実行' }).click();
  await expect(page.locator('#toast-container').getByText('正規化を完了しました')).toBeVisible();

  // crash せず、正規化はデータを保持する (初期化と異なりタスクは残る)
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `normalize caused a fatal: ${fatal}`).toBeNull();
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('NORMALIZE-KEEP-TASK-8810')).toBeVisible();
});


// ===== 7.2: 設定アプリのスナップショット保存→反映 Behavior Check =====
// #/settings の「保存」は setSnapshot() で Storage.set(SNAPSHOT_KEY, ...) し、再描画後に
// getSnapshot()(=Storage.parse) が読み戻して「保存日時: …」を表示する。これは PR #93 で
// 注入漏れを修正した Storage 依存 (set/parse) の往復を実際に通す data-integrity パスで、
// 修正前は Storage.parse が render 時に throw して到達すらできなかった経路。
test('Settings app saves a snapshot and reflects the saved-at status', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 初期 (fresh context) は未保存
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();

  // 保存 → Storage.set → 再描画 → getSnapshot(Storage.parse) が読み戻し「保存日時:」表示
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByText(/保存日時:/)).toBeVisible();

  // リロード後も Storage から読み戻せる (永続)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(/保存日時:/)).toBeVisible();
});


// ===== 7.2: スナップショット削除 (clearSnapshot → 未保存へ復帰) =====
// clearSnapshot は Storage.remove(SNAPSHOT_KEY) + 再描画で「未保存」状態へ戻す。save/restore は
// 被覆済みだが clear (snapshot ライフサイクルの最後) は未カバーだった。snapshot 削除ボタンは
// btn-ghost (プロジェクト削除の btn-danger とは別) で識別する。保存→削除で「未保存」表示へ戻り、
// リロード後も未保存が永続することを実検証し snapshot ライフサイクル (save/restore/clear) を完成させる。
test('Settings snapshot can be cleared back to the unsaved state', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 保存 → 保存日時表示
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByText(/保存日時:/)).toBeVisible();

  // 削除 (snapshot clear = btn-ghost の「削除」。project 削除は btn-danger なので衝突しない)
  await page.locator('button.btn-ghost', { hasText: '削除' }).click();
  await expect(page.locator('#toast-container').getByText('スナップショットを削除しました')).toBeVisible();

  // 未保存状態へ復帰
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();
  await expect(page.getByText(/保存日時:/)).toHaveCount(0);

  // リロード後も未保存 (clear が永続)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();
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
  await expect(page.locator('#toast-container').getByText('正規化を完了しました')).toBeVisible();

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
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

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
  await expect(page.locator('#toast-container').getByText('インポートが完了しました')).toBeVisible();

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
  await expect(page.locator('#toast-container').getByText('スナップショットを復元しました')).toBeVisible();

  // 5. タスク画面: A は残り B は消える (= 保存時点へ revert)
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('SNAP-TASK-A-7700')).toBeVisible();
  await expect(page.getByText('SNAP-TASK-B-7701')).toHaveCount(0);
});
