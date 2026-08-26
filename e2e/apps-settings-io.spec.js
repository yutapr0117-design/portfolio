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

  // Projectsのみ → { projects: [...], projectPrefs: {...} }
  // [契約変更 2026-08-26] 以前は projects の**素の配列**を書き出していたが、既定プロジェクトは
  //   削除できず「非表示」が唯一の非公開手段 (#886) なので、素の配列だと**非表示設定を運べず**
  //   復元時に隠したプロジェクトが黙って再公開されていた。projectPrefs を同梱する形へ変更した。
  //   このテストが守るのは「**正しいスライスだけ**を出す」ことなので、その意図は変わらない ——
  //   projects スライスが入っていること / 他スライス (appsData・profile) を含まないこと。
  //   旧形式 (素の配列) の取り込みは apps-settings-import-shape.spec.js が別に守る。
  const [dlP] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Projectsのみ' }).click(),
  ]);
  expect(dlP.suggestedFilename()).toMatch(/^portfolio_projects_\d+\.json$/);
  const projectsFile = JSON.parse(fs.readFileSync(await dlP.path(), 'utf8'));
  expect(Array.isArray(projectsFile.projects), 'projects slice must be an array').toBe(true);
  expect(projectsFile.projects.length).toBeGreaterThan(0);
  expect(projectsFile, 'projects export must carry visibility prefs').toHaveProperty('projectPrefs');
  expect(projectsFile, 'projects export must NOT be the full store').not.toHaveProperty('appsData');
  expect(projectsFile, 'projects export must NOT be the full store').not.toHaveProperty('profile');

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
    page.once('dialog', d => d.accept());   // 全置換は confirm を通す (#1331)
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
    page.once('dialog', d => d.accept());   // 全置換は confirm を通す (#1331)

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
    page.once('dialog', d => d.accept());   // 全置換は confirm を通す (#1331)
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

// ===== 書き出しの成否が利用者に届くこと =====
// downloadJSON は成功しても失敗しても無言だった。実測 (2026-08-27):
//   成功時 … ファイルは落ちるが toast も SR 通知も空。**このアプリの他の操作は全て報告する**
//            のに書き出しだけ黙る非対称で、SR 利用者は成否を知る手段が無い (WCAG 4.1.3)。
//   失敗時 … 例外がそのまま致命エラーへ昇格し、FatalPage + 全画面オーバーレイで Settings が
//            消える (fatalPage=true / overlay=true / settingsStillThere=false)。
//            **バックアップを取ろうとして画面を失う**のは、失敗の伝え方として最悪。
// 「取れたつもり」が最も危ないのがバックアップなので、成功も明示する。
test('書き出しは成功を報告する', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'フルバックアップ', exact: true }).click(),
  ]);
  // control: 実際にファイルが落ちている (落ちていないのに成功と報告したら、それは別の欠陥)
  expect(await download.path(), 'control: ファイルが書き出されていない').toBeTruthy();
  await expect(page.locator('#toast-container')).toContainText('書き出しました');
  await expect(page.locator('#action-announcement')).toContainText('書き出しました');
});

test('書き出しが失敗しても致命エラーにせず理由を伝える', async ({ page }) => {
  await page.addInitScript(() => { URL.createObjectURL = () => { throw new Error('blocked'); }; });
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.getByRole('button', { name: 'フルバックアップ', exact: true }).click();

  await expect(page.locator('#toast-container')).toContainText('失敗');
  // 2 秒の最終安全網 (#298) より後まで見る — 昇格していれば全画面オーバーレイが被さる
  await page.waitForTimeout(2600);
  expect(await page.evaluate(() => !!window.__fatalError), '書き出し失敗が致命エラーへ昇格している').toBe(false);
  await expect(page.locator('#content'), 'Settings が失われている').toContainText('エクスポート');
});

// ===== 配色 (brand) も backup として往復すること =====
// `theme` は store 内なので `State.get()` を書き出すフル export に自動的に入るが、**brand は
// store の外の独自キー (portfolio_brand_v45)** に保存されるため、同じ export から構造的に
// 抜けていた。Settings の隣り合う 2 つの表示設定で、片方だけ「フルバックアップ」に入らない
// 非対称になっていた —— 復元しても選んだ配色だけが既定へ戻る。
// import 側は store の正規化を通さない (brand は store のキーではないので merged に載せると
// validateAndNormalize が落とす) ため、theme と同じく取り込み時に直接適用する。
// 掃引の結果 (2026-08-27): アプリが使う localStorage キーは 6 つで、brand 以外は**対象外が正しい**。
//   portfolio_enhanced_v45  = store 本体 (フル export はこれを書き出す)
//   portfolio_brand_v45     = 配色。本 test が守る唯一の genuine な欠落だった
//   portfolio_snapshot_v45  = 復元点そのもの。バックアップの中に入れるものではない
//   portfolio_last_error    = 診断用。利用者の設定ではない
//   portfolio_tab_id_v45    = タブ固有の識別子。復元したら別タブと衝突する
//   portfolio_nav_lab_open_v69 = ナビの開閉という一時的な UI 状態 (スクロール位置と同類)
// つまり「store の外にある利用者の設定」は brand だけで、この面は閉じている。増やすときは
// **フル export に入れるか / 入れないならなぜか**を同時に決めること。
test('配色 (brand) が export → import で復元される', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  // control: 開始が既定であること (前提は測ってから使う — theme 版 #1036 の教訓)
  const start = await page.locator('html').getAttribute('data-brand');
  await page.selectOption('#brandSelect', 'classic');
  await expect(page.locator('html')).toHaveAttribute('data-brand', 'classic');
  expect(start, 'control: 開始が既に classic なら切替を検証できない').not.toBe('classic');

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'フルバックアップ', exact: true }).click(),
  ]);
  const file = await download.path();

  // 既定へ戻してから取り込む (戻さないと「元々 classic だった」と区別できない)
  await page.selectOption('#brandSelect', 'indigo');
  await expect(page.locator('html')).toHaveAttribute('data-brand', 'indigo');

  await page.selectOption('#settingsImportMode', 'strict');
  page.once('dialog', d => d.accept());   // 全置換は confirm を通す (#1331)
  await page.setInputFiles('#content input[type="file"]', file);
  await expect(page.locator('html'), 'export した配色が import で戻らない')
    .toHaveAttribute('data-brand', 'classic');
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

  // control: 開始テーマが 'system' であること。**この前提を暗黙に置いていた**ため、
  //   何らかの理由で 'light' で始まると 1 クリックが system へ戻り「dark を期待して system」
  //   という紛らわしい失敗になる (2026-08-20 に CI で 1 度この形の赤が出た)。
  //   前提は測ってから使う。
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'system');

  // system → dark へ。サイクル順に依存せず **dark に到達するまで**押す
  //   (押す回数を決め打ちにすると、開始位置が変わった瞬間に別の値へ着地する)。
  const themeBtn = () => page.evaluate(
    () => (document.getElementById('themeBtnSidebar') || document.getElementById('themeBtnTop')).click()
  );
  for (let i = 0; i < 3; i++) {
    if (await page.locator('html').getAttribute('data-theme') === 'dark') { break; }
    await themeBtn();
  }
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
    page.once('dialog', d => d.accept());   // 全置換は confirm を通す (#1331)
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
    page.once('dialog', d => d.accept());   // 全置換は confirm を通す (#1331)
  await page.setInputFiles('#content input[type="file"]', file);
  await expectNotified(page, 'インポート');

  expect(await visibleCards(),
    'backup を戻したのに、意図的に隠したプロジェクトが再び公開されている').toBe(allCount - 1);
});

// [DATA] スナップショットは**単一スロット**なので、2 度目の「保存」は前の内容を消して現在の状態で
//   置き換える —— **削除と同じく不可逆**である。ところが clearSnapshot は #1185 で confirm を得たのに
//   **上書きだけ取り残されていた**（実測 2026-08-26: 2 回目のクリックで dialog ゼロのまま保存日時が
//   置き換わった）。壊れた状態を実験したあと反射的に「保存」を押すと、**戻るはずだった良い状態を
//   自分で消す**という最も痛い形になる。
test('スナップショットの上書きは確認を求め、キャンセルすると元が残る', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  // 1 回目は破壊的でないので訊かない (control: ここで訊くなら過剰確認である)
  let asked = 0;
  page.on('dialog', d => { asked += 1; d.dismiss(); });
  await page.locator('#settings-snapshot-save').click();
  await expect.poll(async () => page.evaluate(() =>
    !!localStorage.getItem('portfolio_snapshot_v45'))).toBe(true);
  expect(asked, 'control: 初回保存で確認を求めている (過剰確認)').toBe(0);

  const before = await page.evaluate(() =>
    JSON.parse(localStorage.getItem('portfolio_snapshot_v45')).at);

  // 2 回目は上書き = 不可逆なので確認する。ここでは dismiss (キャンセル) する
  await page.locator('#settings-snapshot-save').click();
  await expect.poll(async () => asked).toBe(1);

  // キャンセルしたのだから元のスナップショットが残っていること
  const after = await page.evaluate(() =>
    JSON.parse(localStorage.getItem('portfolio_snapshot_v45')).at);
  expect(after, 'キャンセルしたのに上書きされている').toBe(before);
});

// [DATA] 破壊的操作の確認文は**何を失うか**を言わなければ判断材料にならない。とくに
//   FatalPage の「保存データを削除して再読み込み」は **SNAPSHOT_KEY も削除する**のに、
//   従来の文言は「LocalStorage のデータ」としか言わず、**利用者の唯一の復元点が黙って
//   消えていた**。全リセット側は逆に「スナップショットは残る」ことを言う —— **残るものを
//   伝えるほうが判断できる**（消える恐れで踏みとどまる必要が無くなる）。
test('全リセットの確認文は、元に戻せないことと残るものを伝える', async ({ page }) => {
  const dialogs = [];
  page.on('dialog', d => { dialogs.push(d.message()); d.dismiss(); });

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  // control: 先にスナップショットを作る。残ることを伝える文言が意味を持つ前提。
  await page.locator('#settings-snapshot-save').click();
  await expect.poll(async () => page.evaluate(() =>
    !!localStorage.getItem('portfolio_snapshot_v45'))).toBe(true);

  await page.getByRole('button', { name: '全リセット' }).click();
  await expect.poll(async () => dialogs.length).toBe(1);
  expect(dialogs[0], '元に戻せないことを伝えていない').toContain('元に戻せません');
  expect(dialogs[0], '何が残るかを伝えていない').toContain('スナップショットは残ります');

  // キャンセルしたので実際に残っていること
  expect(await page.evaluate(() =>
    !!localStorage.getItem('portfolio_snapshot_v45')), 'キャンセルしたのに消えている').toBe(true);
});
