const { test, expect } = require('@playwright/test');
const fs = require('fs');




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


// ===== 7.2: 手動プロジェクト追加フォームの入力にアクセシブル名がある (WCAG 3.3.2 / 4.1.2) =====
// 名前 / Tech 入力は visible <label> を持つが従来 for/id 未関連付けで、アクセシブル名が入力すると
// 消失する placeholder のみだった (SR 利用者はどのフィールドか判別不能)。修正で label↔input を
// for/id 関連付け (同ファイル brand select の既存パターン)。getByLabel は関連付けが正しい場合のみ
// 入力を解決するため、本テストは関連付けの存在を検証する (for/id を外すと getByLabel が解決せず RED)。
test('Manual project-add inputs have accessible names via associated labels (a11y)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // getByLabel は <label for> ↔ <input id> の関連付けが成立して初めて入力を解決する
  const nameByLabel = page.getByLabel('名前', { exact: true });
  const techByLabel = page.getByLabel('Tech（カンマ区切り）', { exact: true });
  await expect(nameByLabel).toBeVisible();
  await expect(techByLabel).toBeVisible();

  // 解決した要素が実際の入力であることを確認 (fill できる = ラベルが入力に結び付いている)
  await nameByLabel.fill('a11y-label-probe');
  await expect(nameByLabel).toHaveValue('a11y-label-probe');
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
  // [FIX] 不在アサーションは「まだ描画されていない」を「無い」と誤認して vacuous に PASS しうる
  //   (toHaveCount(0) は初回 poll で成立すると再検査されない)。先に「必ず在るはず」の要素を待って
  //   描画を確定させてから不在を検査する (#825/#830 class・Check 402 が構造強制)。
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
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
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
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
  await expect(page.getByLabel('新しいタスクを入力')).toBeVisible();
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


// ===== 7.2: プロジェクト行の 非表示/削除 ボタンが accessible name に p.name を含み一意化 =====
// #819/#820 (todo/task) と同 class。settings のプロジェクト一覧は複数行を並べるが、修正前は各行の
// トグル(「表示/非表示」)/削除(「削除」)ボタンが全行で同一 accessible name (可視テキスト由来) を持ち、
// SR ユーザーがどのプロジェクトの操作か区別できなかった (WCAG 4.1.2)。可視テキストは維持しつつ
// aria-label に p.name を suffix し一意化する (可視語を prefix に含むため WCAG 2.5.3 Label in Name も充足)。
// 2 プロジェクト追加し各行の非表示/削除ボタンが name 込みの一意名で exact 引きできることを検証する。
test('Settings project-row buttons include the project name in their accessible name (unique per row)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const p1 = 'SETTINGS-A11Y-NAME-ALFA-91';
  const p2 = 'SETTINGS-A11Y-NAME-BETA-92';
  await page.getByPlaceholder('プロジェクト名').fill(p1);
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();
  await page.getByPlaceholder('プロジェクト名').fill(p2);
  await page.getByRole('button', { name: '追加', exact: true }).click();

  // 非表示トグル: name 込みで各行一意に引ける (追加直後は非表示ボタン)。
  await expect(page.getByRole('button', { name: `非表示：${p1}`, exact: true })).toHaveCount(1);
  await expect(page.getByRole('button', { name: `非表示：${p2}`, exact: true })).toHaveCount(1);
  // 削除ボタンも name 込みで一意。
  await expect(page.getByRole('button', { name: `削除：${p1}`, exact: true })).toHaveCount(1);
  await expect(page.getByRole('button', { name: `削除：${p2}`, exact: true })).toHaveCount(1);

  // 非表示化後は toggle の accessible name が「表示：<name>」へ追従する。
  await page.getByRole('button', { name: `非表示：${p1}`, exact: true }).click();
  await expect(page.getByRole('button', { name: `表示：${p1}`, exact: true })).toHaveCount(1);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `settings project-row a11y caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: 設定の brand セレクタで選んだ値が localStorage へ書かれ reload を跨いで復元される =====
// theme-sw.spec.js の brand テストは localStorage を直接 seed して theme-init.js の pre-paint 読み込み
// (consumer 側) を検証するが、設定 UI の brand <select>(onchange→Brand.set→storage.set) が値を
// 正しく WRITE する producer 側の round-trip は未カバーだった (#294/#825 と同じ producer/consumer 非対称)。
// onchange の配線が壊れる / Brand.set が storage.set を呼ばない等の regression で、UI で選んだ brand が
// reload 後に失われるのに既存テストは素通りする。UI で 'classic' を選択→data-brand 即時反映→reload→
// 復元、を検証する。data-brand 属性のみ検証ゆえ視覚(C5)には非依存。
test('Settings brand selector persists the chosen brand across reload (UI write round-trip)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 既定は indigo。UI の <select> で classic を選ぶと data-brand が即時反映される (Brand.set→apply)。
  await expect(page.locator('html')).toHaveAttribute('data-brand', 'indigo');
  await page.getByLabel('ブランド').selectOption('classic');
  await expect(page.locator('html')).toHaveAttribute('data-brand', 'classic');
  // UI 経由の書き込みが localStorage に載っている (producer 側)。
  expect(await page.evaluate(() => localStorage.getItem('portfolio_brand_v45'))).toBe('classic');

  // reload → Brand.init が localStorage を読み戻し classic を復元する (consumer 側 round-trip)。
  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(page.locator('html')).toHaveAttribute('data-brand', 'classic');
  // 設定 <select> の選択状態も復元値に追従する。
  await expect(page.getByLabel('ブランド')).toHaveValue('classic');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `brand round-trip caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: snapshot の 復元/削除 ボタンが未保存時 disabled (disabled affordance) =====
// 復元/削除ボタンは `disabled: !snap` で snapshot 未保存時は無効。restoreSnapshot/clearSnapshot は
// snap 不在時 no-op だが、disabled 属性はユーザへの「まだ復元/削除するものが無い」affordance で、
// 外れると空 snapshot に対し操作できるように見える UX 退行になる。既存の snapshot テストは save/
// restore/clear の flow と「未保存です」表示は見るが、この disabled 状態は未カバーだった。未保存→
// 両ボタン disabled、保存→有効、削除→再び disabled の遷移を検証する。
test('Snapshot restore/clear buttons are disabled until a snapshot exists (affordance)', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();

  const restoreBtn = page.getByRole('button', { name: '復元', exact: true });
  const clearBtn = page.locator('button.btn-ghost', { hasText: '削除' });
  // 未保存: 両ボタン disabled。
  await expect(restoreBtn).toBeDisabled();
  await expect(clearBtn).toBeDisabled();

  // 保存 → 両ボタン有効。
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('スナップショットを保存しました')).toBeVisible();
  await expect(restoreBtn).toBeEnabled();
  await expect(clearBtn).toBeEnabled();

  // 削除 → 未保存へ戻り両ボタン再び disabled。
  await clearBtn.click();
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();
  await expect(restoreBtn).toBeDisabled();
  await expect(clearBtn).toBeDisabled();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `snapshot affordance caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: 追加フォームの検証エラーが不正フィールドを特定できる (WCAG 3.3.1) =====
// プロジェクト追加は名前未入力時に Toast を出すだけで、aria-invalid も focus 移動も無く SR 利用者は
// どの入力が不正か判別できなかった (quiz フォーム #913 と同 class の残り 1 面)。不正入力へ
// aria-invalid を立て focus を移す。focus 判定は document.activeElement を評価する
// (並列ワーカーでは toBeFocused が "inactive" で落ちうるため・#903 実測)。
test('Settings add-project form marks the empty name aria-invalid and focuses it (WCAG 3.3.1)', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  const nameInput = page.locator('#settingsNewName');
  await expect(nameInput).toBeVisible();

  // 空のまま追加 → 不正マーク + focus
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクト名を入力してください')).toBeVisible();
  await expect(nameInput).toHaveAttribute('aria-invalid', 'true');
  expect(await page.evaluate(() => document.activeElement?.id)).toBe('settingsNewName');

  // 名前を入れて追加 → マークが外れる (再描画後の input にも残らない)
  await nameInput.fill('E2E-A11Y-PROJ-9910');
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('プロジェクトを追加しました')).toBeVisible();
  await expect(page.locator('#settingsNewName')).not.toHaveAttribute('aria-invalid', 'true');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `settings form error identification caused a fatal: ${fatal}`).toBeNull();
});
