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
  // [FIX] 名前でボタンを引く (#1085 で矢印だけの名前から「上へ移動：<名前>」へ一意化した)。
  //   矢印は aria-hidden の装飾になったため、name: '↑' では解決しない。
  await rowA.getByRole('button', { name: new RegExp('^上へ移動：') }).click();
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
  // 検査範囲を #content に限る。削除の通知 (#1185 で追加) は「「<名前>」を削除しました」と
  // **名前を含み**、通知コンテナは #content の外でルート遷移後も数秒残るため、ページ全体を
  // 対象にすると「一覧から消えたか」ではなく「通知が出ているか」を測ってしまう。
  // このテストの意図は **公開一覧に出ないこと**なので、その範囲で測る。
  await expect(page.locator('#content').getByText(name)).toHaveCount(0);
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
  // dismiss されたので削除されず、公開一覧にも残る。
  // **検査範囲は #content に限る**: 削除の通知 (#1185) は「「<名前>」を削除しました」と
  // 名前を含み、通知コンテナは #content の外でルート遷移後も数秒残る。ページ全体を
  // 対象にすると **削除されていても通知が名前を満たしてしまい**、confirm ガードを外す
  // mutation を素通しする (2026-08-20 の週次 probe が実際に SURVIVED で検出)。
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.grid-projects article h2').first()).toBeVisible();
  await expect(page.locator('#content').getByText(name).first()).toBeVisible();
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

  // [FIX] **appsData 以外にも差分を作る。** 従来はタスクを 1 件足すだけで、検証も
  //   「そのタスクが消えたこと」しか見ていなかった。つまり「全リセット」が
  //   **appsData しか戻さない部分リセットへ退行しても緑のまま**になる
  //   (実測 2026-08-21: `State.set(Store.createDefaultStore())` を
  //   `State.update(s => { s.appsData = ... })` へ差し替えても PASS)。
  //   「全」リセットは全領域が対象なので、appsData の外にも差分を置いて検証する。
  //   ここでは projectPrefs (非表示) を使う —— 既定プロジェクトは削除できず
  //   「非表示」が唯一の非公開手段 (#886) なので、リセットで戻らないと
  //   **利用者が意図的に隠したものが公開状態のまま残る**。
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  const hideBtn = page.getByRole('button', { name: /^非表示：/ }).first();
  await expect(hideBtn, 'control: 非表示ボタンが無いと appsData 外の差分を作れない').toBeVisible();
  await hideBtn.click();
  await expect.poll(async () => page.evaluate(() => {
    const k = Object.keys(localStorage).find(x => x.includes('portfolio'));
    return ((JSON.parse(localStorage.getItem(k) || '{}').projectPrefs || {}).hiddenIds || []).length;
  }), { message: 'control: 非表示の差分が保存されていない' }).toBeGreaterThan(0);

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

  // appsData 外 (projectPrefs) も既定へ戻っている —— ここが部分リセットへの退行を捕捉する。
  //   **poll で待つ**: 保存は debounce されており、リセット直後に読むと ["p01"] のまま
  //   (実測 2026-08-21: 直後 ["p01"] → 600ms 後 []) で、製品が正しくても落ちる。
  //   これは「変化」の検査なので poll が正しい (不変性の検査なら settle 後に 1 度読む)。
  await expect.poll(async () => page.evaluate(() => {
    const k = Object.keys(localStorage).find(x => x.includes('portfolio'));
    return ((JSON.parse(localStorage.getItem(k) || '{}').projectPrefs || {}).hiddenIds || []).length;
  }), { message: '全リセットなのに非表示 (projectPrefs) が残っている = 部分リセットへ退行している' }).toBe(0);

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
  // NOTE: スナップショット削除は confirm を通す (唯一の復元点ゆえ他の破壊的操作と対称にした)。
  //   Playwright は dialog を既定で dismiss する = 承認しないと削除自体が起きないため、
  //   「削除できること」を検証する本 test では明示的に accept する。
  page.once('dialog', (d) => d.accept());
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
  // confirm を承認する (既定の dismiss では削除が起きず affordance も変化しない)。
  page.once('dialog', (d) => d.accept());
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

// ===== 既定プロジェクトの並べ替えが reload を跨いで保持される (normalize round-trip の data-fidelity) =====
// 上の reorder テストは **ユーザー追加**プロジェクトを **reload なし**で検査している。だが
// store.js の [FIX] が直した実バグは **既定プロジェクト同士**の並べ替えが **reload 後**に
// 元の定義順へ silent に戻るというもので、その失敗モードは上のテストでは踏めない
// (旧実装は `normalizedDefaults` を定義順で再構築し incoming 順を無視していた。user 追加分は
//  incoming 順で append されるため保持され、**default だけが戻る**という非対称だった)。
//
// **localStorage を読んではいけない**: reload 直後の localStorage は「保存済みのバイト列」であって
//   正規化後の state ではない (アプリは state が変わるまで書き戻さない)。順序を壊す mutation を
//   当てても localStorage は変わらず、**テストが vacuous になる** (この test の初版が実際そうだった)。
//   ユーザーが見るのは描画順なので、**DOM の行順**を検査する。
test('Default-project reorder survives a reload (normalize round-trip)', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();

  const rows = page.locator('div.flex.items-center.justify-between.gap-2');
  const rowNames = async () => (await rows.allTextContents()).slice(0, 4).map((t) => t.replace(/[\u2191\u2193]/g, '').trim());

  const before = await rowNames();
  expect(before.length, 'プロジェクト行が読めない').toBeGreaterThan(2);

  // 2 番目の行の「↑」で先頭 2 件を入れ替える (どちらも既定プロジェクト)
  // [FIX] #1085 で矢印は装飾になり、名前は「上へ移動：<名前>」へ一意化された。
  await rows.nth(1).getByRole('button', { name: new RegExp('^上へ移動：') }).click();

  // 入れ替えが描画に反映されるまで待つ (ここが動いていないと以降は vacuous)
  await expect.poll(rowNames, { message: '\u2191 操作が描画順に反映されていない — 以降の検査が vacuous' })
    .not.toEqual(before);
  const afterClick = await rowNames();

  await page.reload();
  await expect(page.locator('#content h1')).toBeVisible();

  // reload 後も **同じ描画順** であること。旧実装ではここで定義順 (= before) へ戻っていた。
  await expect.poll(rowNames, {
    message: 'reload の normalize round-trip で既定プロジェクトの並べ替えが失われた',
  }).toEqual(afterClick);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `reorder reload caused a fatal: ${fatal}`).toBeNull();
});

// ===== WCAG 2.1.1: 並べ替え・表示切替をキーボードで続けて操作できる =====
// #994/#995 の focus 復元は id を鍵にする opt-in なので、id の無いボタンは対象から漏れる。
// Settings の「並び替え（Projects）」の ↑↓ は **1 回押すたびに focus が外れ、2 回目以降が
// 効かなかった** (実測 #1000: 1 段動かしたところで止まる)。プロジェクトを何段も動かすのが
// 本来の用途なので、実質キーボードでは使えない状態だった。
//
// 鍵を **idx ではなく p.id で作る**のが要点。idx で作ると、移動後にその位置へ来た
// **別のプロジェクト**のボタンへ focus が移ってしまい、続けて押すと違う行が動く。
test('WCAG 2.1.1: プロジェクトの並べ替えをキーボードで連続実行できる', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  const rows = () => page.evaluate(() =>
    Array.from(document.querySelectorAll('#content .scroll-container-sm .text-sm')).slice(0, 6).map(e => e.textContent));
  const before = await rows();

  // 3 番目の項目の「↓」を 2 回押す。NOTE: locator に復元用 id を使わない (id を外す mutation が
  //   「要素が見つからない」で落ちると、focus が失われたことを検証できたのか帰属できない)。
  // [FIX] #1085 で矢印は aria-hidden の装飾になり、名前は「下へ移動：<名前>」へ一意化された。
  //   locator に復元用 id を使わない方針は維持したいので、**名前**で引く
  //   (id を外す mutation が『要素が見つからない』で落ちると、focus 喪失を検証できたか判らない)。
  const down = page.getByRole('button', { name: new RegExp('^下へ移動：') }).nth(2);
  await down.scrollIntoViewIfNeeded();
  await down.focus();
  const movedName = before[2];

  await page.keyboard.press('Enter');
  await page.waitForTimeout(400);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(400);

  const after = await rows();
  // 2 回押したら 2 段下がること。focus を失うと 1 段で止まる (実測の壊れ方そのもの)。
  expect(after.indexOf(movedName), `「${movedName}」が 2 段下がっていない (before=${JSON.stringify(before)} after=${JSON.stringify(after)})`)
    .toBe(before.indexOf(movedName) + 2);

  // focus が「同じプロジェクトの ↓」に残っていること (idx 鍵だと別の行へ移る)
  const active = await page.evaluate(() => (document.activeElement ? document.activeElement.id : null));
  expect(active, '並べ替えのたびに focus が失われている').toMatch(/^settings-move-down-/);
});

test('WCAG 2.1.1: 表示切替ボタンは押した後も focus が残る', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  const btn = page.getByRole('button', { name: /^非表示：/ }).first();
  await btn.scrollIntoViewIfNeeded();
  const label = await btn.getAttribute('aria-label');
  await btn.focus();
  await page.keyboard.press('Enter');
  await page.waitForTimeout(400);

  // 押すとラベルが「表示：〜」へ変わる。同じ行のボタンに focus が残っていれば、
  // もう一度 Enter で元に戻せる (= 続けて操作できる)。
  const name = label.replace(/^非表示：/, '');
  const activeLabel = await page.evaluate(() => (document.activeElement ? document.activeElement.getAttribute('aria-label') : null));
  expect(activeLabel, '表示切替のたびに focus が失われ、続けて操作できない').toBe('表示：' + name);

  await page.keyboard.press('Enter');
  await page.waitForTimeout(400);
  const back = await page.evaluate(() => (document.activeElement ? document.activeElement.getAttribute('aria-label') : null));
  expect(back).toBe('非表示：' + name);
});


// ===== 入力できる範囲と保存される範囲が一致する (silent truncation の防止) =====
// `normalizeProject` は name を `LIMITS.PROJECT_NAME` で切り詰めるのに、手動追加の入力欄は
// 無制限だった。そのため長い名前は **追加した直後は全部見えているのに、リロード後に黙って
// 短くなる** (実測: 200 文字 → 120 文字)。消えたことに気付くのが後になるほど、利用者は
// 原因を特定できない (#924 と同じ class)。
// NOTE: Check 410 は「同じ file 内で LIMITS を使って slice している」ことを条件に maxlength を
// 要求するため、上限が store.js 側にあるこのケースは静的検査の射程外 —— この behavior test が
// 唯一の捕捉層になる。
test('手動追加のプロジェクト名が入力上限と保存上限で一致する', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  const limit = await page.evaluate(() => Number(document.getElementById('settingsNewName').getAttribute('maxlength')));
  expect(limit, '入力欄に上限が設定されていない').toBeGreaterThan(0);

  await page.locator('#settingsNewName').fill('N'.repeat(limit + 80));
  // control: 入力欄が上限で止めている (止まっていなければ保存側との一致を測れない)
  expect((await page.locator('#settingsNewName').inputValue()).length).toBe(limit);

  await page.getByRole('button', { name: '追加', exact: true }).click();

  // 正規化を通す (リロード = load 経路)。ここで縮むなら「入力できたのに保存されない」状態。
  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  const rendered = await page.evaluate(() => {
    const b = Array.from(document.querySelectorAll('#content button'))
      .find((x) => /^削除：N+$/.test(x.getAttribute('aria-label') || ''));
    return b ? (b.getAttribute('aria-label') || '').replace('削除：', '').length : -1;
  });
  expect(rendered, 'リロード後に名前が黙って短くなっている (入力上限と保存上限の不一致)').toBe(limit);
});


// Tech は「1 項目 LIMITS.CATEGORY 文字・最大 12 項目」で切られる。件数の制限は maxlength では
// 表現できないので、**追加を受けた時点で保存される形に揃える**しかない。揃えないと、追加直後は
// 20 個の Tech がそのまま並ぶのに **リロードすると 12 個へ黙って減る** (名前の truncation と同じ class)。
test('手動追加の Tech が件数上限どおりに保存される', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  await page.locator('#settingsNewName').fill('TECH-BOUND-9904');
  await page.locator('#settingsNewTech').fill(Array.from({ length: 20 }, (_, i) => 'T' + i).join(','));
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.getByRole('button', { name: '削除：TECH-BOUND-9904' })).toBeVisible();  // control

  const stored = () => page.evaluate(() => {
    try {
      const p = (JSON.parse(localStorage.getItem('portfolio_enhanced_v45')).projects || [])
        .find((x) => x.name === 'TECH-BOUND-9904');
      return p ? p.tech.length : -1;
    } catch { return -1; }
  });

  await expect.poll(stored, { message: '追加直後に保存された Tech の件数' }).toBe(12);

  // 正規化を通しても件数が変わらない = 追加時点で保存される形になっている
  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await expect.poll(stored, { message: 'リロード後の Tech 件数' }).toBe(12);
});


// ===== 並べ替えボタンの名前がどのプロジェクトか識別できる =====
// 矢印だけだと 36 個のボタンが「↑」「↓」の 2 種類の名前しか持たず、SR 利用者はどれを
// 操作するのか区別できない (実測: uniq な名前が 2 つだけだった)。同じ行の削除・非表示は
// 既に「削除：<名前>」と一意化されており、**並べ替えだけ取り残されていた**非対称
// (「1 ケースだけ処理して他を忘れる」class)。WCAG 4.1.2。
// 視覚利用者には行の位置で自明なので、目視では気付けない種類の欠落。
test('並べ替えボタンの名前がプロジェクトごとに一意になる', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  const names = await page.evaluate(() => Array.from(
    document.querySelectorAll('#content button[id^="settings-move-"]')
  ).map((b) => b.getAttribute('aria-label') || (b.textContent || '').trim()));

  expect(names.length, 'control: 並べ替えボタンが描画されていない').toBeGreaterThan(4);
  expect(new Set(names).size,
    `並べ替えボタンの名前が重複している (${names.length} 個中 ${new Set(names).size} 種類)`).toBe(names.length);

  // 方向とプロジェクト名の両方が名前に含まれる
  expect(names.some((n) => n.startsWith('上へ移動：')), '上方向の名前が無い').toBe(true);
  expect(names.some((n) => n.startsWith('下へ移動：')), '下方向の名前が無い').toBe(true);

  // 矢印は装飾として隠され、名前に二重で出ない
  const arrowExposed = await page.evaluate(() => Array.from(
    document.querySelectorAll('#content button[id^="settings-move-"] span')
  ).some((s) => s.getAttribute('aria-hidden') !== 'true'));
  expect(arrowExposed, '矢印がアクセシビリティツリーへ露出している (二重読み上げ)').toBe(false);
});


// ===== プロジェクトの並べ替えが SR に伝わる (WCAG 4.1.3) =====
// ボタンのアクセシブル名 (「下へ移動：<プロジェクト名>」) は移動後も変わらず、focus も
// 同じボタンへ戻る (#1000)。つまり SR 利用者には **押しても何も起きていないのと
// 区別がつかなかった** (実測 2026-08-17: `#action-announcement` が空のまま)。
// task のステータス移動 (#1107) と同型の非対称。
//
// **位置と総数まで読む**のは、一覧を見渡せない利用者には「何番目へ動いたか」が唯一の
// 手がかりだから。Toast (視覚ポップアップ) にしないのは並べ替えが連続操作だから。
test('プロジェクトの並べ替えがスクリーンリーダーに通知される', async ({ page }) => {
  await page.goto('/#/settings');
  await page.reload();
  await expect(page.locator('#main-content h1').first()).toBeVisible();

  const down = page.getByRole('button', { name: '下へ移動：タスク管理アプリ' });
  // control: 対象のボタンが実在する (空振りしたまま以降を検査しない)
  await expect(down, 'control: 並べ替えボタンが見つからない').toHaveCount(1);

  await down.click();

  await expect(page.locator('#action-announcement'),
    '並べ替えが SR へ通知されない — ボタン名は変わらず focus も戻るので、'
    + 'SR 利用者には押しても何も起きていないのと区別がつかない (WCAG 4.1.3)'
  ).toHaveText(/「タスク管理アプリ」を 2 番目へ移動しました（全 \d+ 件）/);

  // 視覚ポップアップは出さない (連続操作なので Toast にしない設計)
  expect(await page.locator('#toast-container').count(),
    '並べ替えで視覚 Toast が出ている — 連続操作なので sr-only 通知にとどめる設計').toBe(0);
});


// ===== プロジェクト追加も上限時は断る (task/todo #1152 と同形) =====
// `s.projects.unshift(...)` の後にロード時の正規化 `slice(0, MAX_PROJECTS)` が走るため、
// 上限に達した状態で追加すると **最古のプロジェクトが無通知で消える**。到達には 1000 件が
// 必要で実運用の可能性は低いが、**3 経路 (task / todo / project) のうち 1 つだけ無防備に
// しておくのがこのリポジトリで class を再発させてきた形**なので閉じる。
// seed は冪等にする (addInitScript は reload でも再実行される・落とし穴表参照)。
test('Adding a project at the limit is refused with a reason', async ({ page }) => {
  await page.addInitScript(() => {
    if (localStorage.getItem('__seeded_plimit')) { return; }
    const projects = Array.from({ length: 1000 }, (_, i) => ({
      id: 'LP' + i, slug: 'lp-' + i, name: '既存プロジェクト ' + i, category: 'User Added', summary: '',
    }));
    localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({ schemaVersion: 12, projects }));
    localStorage.setItem('__seeded_plimit', '1');
  });

  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByRole('button', { name: 'フルバックアップ' })).toBeVisible();

  // control: 上限ちょうどで始まっている
  const count = () => page.evaluate(
    () => JSON.parse(localStorage.getItem('portfolio_enhanced_v45')).projects.length);
  expect(await count(), 'seed が効いていない').toBe(1000);

  await page.locator('#settingsNewName').fill('上限超過プロジェクト');
  await page.getByRole('button', { name: '追加', exact: true }).click();

  await expect.poll(
    () => page.evaluate(() => (document.getElementById('action-announcement') || {}).textContent || ''),
    { timeout: 5000 }
  ).toContain('1000 件までです');

  expect(await count(), '断ったのに件数が変わっている').toBe(1000);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `project limit refusal caused a fatal: ${fatal}`).toBeNull();
});


// ===== 通知は種別ごとに見分けが付き、表面を持つ (WCAG 1.4.1 / UX) =====
// `Toast.show(msg, type)` は **21 箇所が error / success / info / warning を選び分けて**呼ぶが、
// `.alert` 系の宣言が style.css に 1 つも無かった (git log -S で追うと履歴上も一度も存在しない
// = 実装漏れ)。実測 (2026-08-20): 成功通知と失敗通知は色・背景・境界・影がすべて同一で
// **見分けが付かず**、しかも背景が透明のため **本文の上に文字が重なって**いた。
//
// 種別は文言でも伝わるので色だけに依存してはいない (WCAG 1.4.1) が、左の帯で一目で分かるようにした。
test('Toasts have a surface and are visually distinguishable by type', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.getByRole('button', { name: 'フルバックアップ' })).toBeVisible();

  const toast = () => page.evaluate(() => {
    const el = document.querySelector('#toast-container .alert');
    if (!el) { return null; }
    const cs = getComputedStyle(el);
    return { cls: el.className, bg: cs.backgroundColor, accent: cs.borderLeftColor, width: cs.borderLeftWidth };
  });

  // エラー通知 (プロジェクト名が空のまま追加)
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect.poll(async () => (await toast())?.cls, { timeout: 5000 }).toContain('alert-error');
  const err = await toast();
  expect(err.bg, '通知に背景が無い (本文に文字が重なる)').not.toBe('rgba(0, 0, 0, 0)');
  expect(err.width, '種別を示す帯が無い').not.toBe('0px');

  // 成功通知 (名前を入れて追加)
  await expect.poll(async () => (await toast()) === null, { timeout: 8000 }).toBe(true);  // 前の通知が消えるまで待つ
  await page.locator('#settingsNewName').fill('通知の見分けテスト');
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect.poll(async () => (await toast())?.cls, { timeout: 5000 }).toContain('alert-success');
  const ok = await toast();

  expect(ok.accent, 'エラーと成功で見た目が同じ (種別が伝わらない)').not.toBe(err.accent);
  expect(ok.bg, '成功通知に背景が無い').not.toBe('rgba(0, 0, 0, 0)');
});


// ===== 手動追加で Tech が黙って落ちない (silent truncation) =====
// `tech` は保存時に「12 項目・各 LIMITS.CATEGORY 文字」で切られるが、従来は素の
// 「プロジェクトを追加しました」だけだった。実測 (2026-08-20): 16 件・1 件目 120 文字を投入すると
// **12 件だけ保存され 1 件目は 80 文字に切断**されるのに、利用者には何も伝わらなかった。
//
// **件数の上限は maxlength では表現できない**ので、入力欄側の宣言だけでは防げない
// (Check 410 は「同一 file の slice ⟹ maxlength」を見るが、tech の slice は store.js 側にある)。
// #1143 で import の切り捨てを「完了しました」で済ませないようにしたのと同じ規律。
test('Manual project add reports dropped or truncated tech entries', async ({ page }) => {
  const announcement = () => page.evaluate(
    () => (document.getElementById('action-announcement') || {}).textContent || '');

  const add = async (name, tech) => {
    await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
    await expect(page.getByRole('button', { name: 'フルバックアップ' })).toBeVisible();
    await page.locator('#settingsNewName').fill(name);
    await page.locator('#settingsNewTech').fill(tech);
    await page.getByRole('button', { name: '追加', exact: true }).click();
  };

  // control: 上限内なら従来どおり素の完了メッセージ (常に注記を付ける実装ではない)
  await add('Tech 上限内テスト', 'React,Vue');
  await expect.poll(announcement, { timeout: 5000 }).toContain('プロジェクトを追加しました');
  expect(await announcement(), '上限内なのに注記が付いている').not.toContain('Tech:');

  // 12 件を超え、かつ 1 件目が上限文字数を超える入力
  const long = 'T'.repeat(120);
  await add('Tech 超過テスト', [long, ...Array.from({ length: 15 }, (_, i) => 'x' + i)].join(','));
  await expect.poll(announcement, { timeout: 5000 }).toContain('取り込めず');
  const msg = await announcement();
  expect(msg, '短縮された件数が伝わっていない').toContain('短縮');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `manual add caused a fatal: ${fatal}`).toBeNull();
});
