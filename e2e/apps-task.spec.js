const { test, expect } = require('@playwright/test');


// ===== 7.2: タスク管理アプリの追加 + リロード永続化 Behavior Check =====
// #/apps/task は #task-input に入力 → Enter で State.update 経由でタスクを追加し、
// localStorage (State auto-save) へ永続化する。apps セクションは従来「ルートが描画される」
// テストのみで、実際のデータ操作 (add → 永続 → reload で復元) は未カバーだった。State の
// Proxy 永続パスを実ブラウザで動的検証する (theme/drawer/quiz に続く interactive coverage)。
// [A11Y 3.3.2/4.1.2] task/todo の主入力は可視ラベルを持たず placeholder のみだった。
// placeholder は入力開始で消え SR が accessible name として一貫して読まないため、
// getByLabel (aria-label 解決) が主入力を特定できることを実検証する。aria-label を
// 除去すると getByLabel が要素を見つけられず本テストが RED になる (非 vacuous)。
test('Task and Todo main inputs expose an accessible name (not placeholder-only)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByLabel('新しいタスクを入力')).toHaveAttribute('id', 'task-input');

  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByLabel('やることを入力')).toHaveAttribute('id', 'todo-input');
});

test('Task app adds a task and persists it across reload', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();

  // 一意なタイトルで衝突を避ける (固定文字列 + 数値を埋め込み、Math.random は使わない)
  const title = 'E2E-PERSIST-CHECK-TASK-7421';
  await input.fill(title);
  await input.press('Enter');

  // 追加直後にカードが描画される
  await expect(page.getByText(title)).toBeVisible();

  // リロード後も State (localStorage) から復元される
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(title)).toBeVisible();
});


// ===== 7.2: タスク入力の IME composition ガード (日本語入力の誤確定防止) =====
// task-input の Enter ハンドラは IME 変換確定の Enter (e.isComposing=true) でタスクを追加しては
// ならない (todo は todoComposing で対応済みだが task は未対応だった = 日本語が主対象の本サイトで
// 実バグ)。修正で `!e.isComposing` ガードを追加。composing 中の Enter では追加されず、通常の Enter
// では追加されることを実検証する。
test('Task input ignores Enter during IME composition (Japanese input safety)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  const t = 'IME-COMPOSING-TASK-2200';

  // IME 変換確定の Enter (isComposing=true) ではタスクを追加しない
  await input.fill(t);
  await input.evaluate((el) => {
    el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', isComposing: true, bubbles: true, cancelable: true }));
  });
  await expect(page.getByText(t)).toHaveCount(0);

  // 通常の Enter (isComposing=false) では追加される
  await input.press('Enter');
  await expect(page.getByText(t)).toBeVisible();
});


// ===== 7.2: タスクの kanban ステータス移動 (未着手→進行中→完了) + 永続 =====
// タスクカードの「→」は moveStatus(task, +1) で status を backlog→in-progress→done と進める
// (backlog で「←」/ done で「→」は disabled)。add+persist テストはあるがこの kanban 列移動という
// 別 operation は未カバーだった。追加→「→」で進行中列へ→もう一度「→」で完了列へ移り、リロード後も
// 完了列に残る (status 永続) ことを実検証する。
test('Task moves across kanban columns and persists the status', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  const title = 'KANBAN-MOVE-TASK-4400';
  await input.fill(title);
  await input.press('Enter');

  const inProgress = page.locator('section.card.bg-secondary').filter({ has: page.getByRole('heading', { name: '進行中' }) });
  const done = page.locator('section.card.bg-secondary').filter({ has: page.getByRole('heading', { name: '完了' }) });

  // 追加直後は未着手。→ で 進行中 へ
  await page.locator('article', { hasText: title }).getByRole('button', { name: '→' }).click();
  await expect(inProgress.getByText(title)).toBeVisible();

  // もう一度 → で 完了 へ
  await page.locator('article', { hasText: title }).getByRole('button', { name: '→' }).click();
  await expect(done.getByText(title)).toBeVisible();

  // リロード後も 完了 列に残る (status 永続)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  const doneAfter = page.locator('section.card.bg-secondary').filter({ has: page.getByRole('heading', { name: '完了' }) });
  await expect(doneAfter.getByText(title)).toBeVisible();
});


// ===== 7.2: タスク削除 (task CRUD: add/move/delete を完成) =====
// タスクカードの削除ボタン (aria-label='タスクを削除') は deleteTask(id) で State から該当タスクを
// 除去し「タスクを削除しました」を出す。add/move はカバー済みだが削除は未カバーだった。追加→削除で
// カードが消え通知が出ることを実検証し task CRUD のカバレッジを完成させる。
test('Task can be deleted from the board', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  const title = 'DELETE-ME-TASK-7799';
  await input.fill(title);
  await input.press('Enter');

  const card = page.locator('article', { hasText: title });
  await expect(card).toBeVisible();

  // 削除 → カードが消える + 通知
  await card.getByRole('button', { name: 'タスクを削除' }).click();
  await expect(page.locator('#toast-container').getByText('タスクを削除しました')).toBeVisible();
  await expect(page.getByText(title)).toHaveCount(0);
});


// ===== 7.2: タスク優先度フィルタ (カードで優先度変更 → high/med/all で振り分け) =====
// タスクカードの優先度 select (aria-label='タスクの優先度') は updateTask で priority を変更し、
// ヘッダの絞り込み select (aria-label='優先度で絞り込み') は getFilteredTasks で
// taskFilter.priority に一致するものだけ表示する。card 優先度変更 + フィルタ分岐は未カバーだった。
// 1 件を high に変更し、high/med/all フィルタで表示集合が切り替わることを実検証する。
test('Task priority filter narrows the board by priority', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  const hi = 'PRIO-HIGH-TASK-3301';
  const md = 'PRIO-MED-TASK-3302';
  await input.fill(hi);
  await input.press('Enter');
  await expect(page.getByText(hi)).toBeVisible();
  // hi の優先度を high に変更 (既定は med)
  await page.locator('article', { hasText: hi }).getByLabel('タスクの優先度').selectOption('high');
  await input.fill(md);
  await input.press('Enter');
  await expect(page.getByText(md)).toBeVisible();

  const filter = page.getByLabel('優先度で絞り込み');

  // high → hi のみ
  await filter.selectOption('high');
  await expect(page.getByText(hi)).toBeVisible();
  await expect(page.getByText(md)).toHaveCount(0);

  // med → md のみ
  await filter.selectOption('med');
  await expect(page.getByText(md)).toBeVisible();
  await expect(page.getByText(hi)).toHaveCount(0);

  // all → 両方
  await filter.selectOption('all');
  await expect(page.getByText(hi)).toBeVisible();
  await expect(page.getByText(md)).toBeVisible();
});


// ===== 7.2: task per-card priority select が再描画後も visual 選択を保持する (#7cbc4d9 class) =====
// updateTask は State.update() を呼び全再描画を発生させる。修正前は h('select', { value: task.priority })
// が el.setAttribute('value', ...) となり HTML 仕様上 <select> の選択状態に無効なため再描画後に
// 最初の option ('high') に戻り、'med'/'low' を設定したタスクが UI 上で 'high' に見えていた。
// 修正後は各 option に selected: priority===cur ? true : undefined を付与する。
test('Task per-card priority select retains visual selection after re-render (#7cbc4d9 class)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await input.fill('PRIORITY-SELECT-FIX-TASK-4401');
  await input.press('Enter');
  await expect(page.getByText('PRIORITY-SELECT-FIX-TASK-4401')).toBeVisible();

  // Change priority to 'low' → updateTask → State.update → full re-render
  const cardSel = page.locator('article', { hasText: 'PRIORITY-SELECT-FIX-TASK-4401' }).getByLabel('タスクの優先度');
  await cardSel.selectOption('low');
  // 再描画後も 'low' のまま (fix 前はここで 'high' に戻った)
  await expect(cardSel).toHaveValue('low');

  // 'med' も同様に保持される
  await cardSel.selectOption('med');
  await expect(cardSel).toHaveValue('med');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `priority select caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: task priority filter select が再描画後も visual 選択を保持する (#7cbc4d9 class) =====
// taskFilter.priority select の onchange は window.render() を直接呼ぶため同クラスのバグが発生。
// filter select が再描画後も選択した priority を visual に保持することを検証する。
test('Task priority filter select retains visual selection after re-render (#7cbc4d9 class)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const filter = page.getByLabel('優先度で絞り込み');
  await expect(filter).toBeVisible();

  // 'high' に変更 → window.render() → 再描画後も 'high'
  await filter.selectOption('high');
  await expect(filter).toHaveValue('high');

  // 'low' に変更 → 再描画後も 'low'
  await filter.selectOption('low');
  await expect(filter).toHaveValue('low');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `priority filter select caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.1b: localStorage QuotaExceeded 時の graceful degradation =====
// State の保存経路 (state.js scheduleSave/saveNow) は Storage.set が false を返したとき
// notifyStorageError() でユーザーに通知し、in-memory state はそのまま維持する設計
// (storage.js は容量超過例外を握りつぶして false を返す)。read 側 (corrupt-storage) とは
// 別の write 側耐障害性: localStorage.setItem が QuotaExceededError を投げても (1) タスク
// 追加は in-memory で機能し描画される (2) ErrorBoundary (FatalPage) に落ちない
// (3) ストレージエラーがログされる。動きの保証 = ディスク満杯でも操作を失わない。
test('Task app degrades gracefully when localStorage write quota is exceeded', async ({ page }) => {
  // setItem だけを QuotaExceededError で失敗させる (getItem は機能させ、初期 theme 読込等は壊さない)
  await page.addInitScript(() => {
    const proto = window.Storage && window.Storage.prototype;
    if (proto) {
      proto.setItem = function () {
        const err = new Error('quota');
        err.name = 'QuotaExceededError';
        throw err;
      };
    }
  });

  const consoleErrors = [];
  page.on('console', msg => { if (msg.type() === 'error') {consoleErrors.push(msg.text());} });

  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();

  const title = 'E2E-QUOTA-DEGRADE-TASK-3390';
  await input.fill(title);
  await input.press('Enter');

  // (1) 書き込みは失敗しても in-memory state で描画される
  await expect(page.getByText(title)).toBeVisible();

  // (2) FatalPage (ErrorBoundary) に落ちていない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quota write failure caused a fatal: ${fatal}`).toBeNull();

  // (3) ストレージ上限エラーが通知 (console.error) される (debounce save 後)
  await expect.poll(
    () => consoleErrors.some(t => t.includes('ストレージ上限')),
    { timeout: 5000 }
  ).toBe(true);
});


// ===== 7.1c: クロスタブ同期 (storage イベント → 別タブの更新を採用) =====
// state.js は window 'storage' イベントを購読し、別タブ (modifiedBy ≠ 自タブの TAB_ID) からの
// より新しい書き込み (lastModified 比較) を採用 → 再描画 + 「別タブで更新されました」toast を出す。
// この multi-tab 経路は単一ページのテストでは発火しない (storage イベントは書き込んだタブ自身には
// 飛ばない) ため従来未カバー。同一 context の 2 ページ (localStorage 共有・sessionStorage=TAB_ID は
// タブ毎に独立) で実検証する。複数タブで同じポートフォリオを開いても状態が同期される保証。
test('Cross-tab sync: a task added in one tab appears in another tab', async ({ context }) => {
  const tabA = await context.newPage();
  const tabB = await context.newPage();

  await tabA.goto('/#/apps/task');
  await tabA.waitForLoadState('domcontentloaded');
  await tabB.goto('/#/apps/task');
  await tabB.waitForLoadState('domcontentloaded');

  // タブ B にはまだ存在しないことを確認 (negative baseline)
  const title = 'E2E-CROSS-TAB-SYNC-TASK-5108';
  await expect(tabB.getByText(title)).toHaveCount(0);

  // タブ A でタスクを追加 → State debounce save で localStorage 書き込み
  const inputA = tabA.locator('#task-input');
  await expect(inputA).toBeVisible();
  await inputA.fill(title);
  await inputA.press('Enter');
  await expect(tabA.getByText(title)).toBeVisible();

  // タブ B が storage イベントを受信 → 採用 → 再描画でタスクが現れる
  await expect(tabB.getByText(title)).toBeVisible({ timeout: 5000 });
  // 「別タブで更新されました」通知 (info toast) が出る
  await expect(tabB.locator('#toast-container').getByText('別タブで更新されました')).toBeVisible();

  await tabA.close();
  await tabB.close();
});


// ===== 7.1d: クロスタブ同期は別 schema / 欠損 store を raw 採用せず crash しない =====
// state.js の 'storage' リスナーは別タブの新しい書き込みを採用するが、load()/import が必ず通す
// 正規化 (schema 検証 + validateAndNormalize) を以前は省いていた。デプロイ跨ぎで 2 タブを開くと、
// 旧バージョンのタブが別 schema / 欠損フィールドの store を書き、新バージョンのタブがそれを raw 採用
// → render が未定義参照 (例 appsData.tasks) で FatalPage crash する (#93 = 未正規化外部データ取り込み
// と同 class)。本テストは synthetic StorageEvent で「より新しいが schema 不一致 + appsData 欠落」な
// 書き込みを注入し、(1) FatalPage crash しない (2) 不正データを採用せず現タブの正常 state を保持する
// ことを検証する。修正前は (1) が fatal で落ちるため非 vacuous。
test('Cross-tab sync ignores a foreign-schema/malformed store without crashing', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  // 既存タスクを 1 件作って「現タブの正常 state」を確立する
  const ownTitle = 'E2E-XTAB-OWN-TASK-6620';
  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  await input.fill(ownTitle);
  await input.press('Enter');
  await expect(page.getByText(ownTitle)).toBeVisible();

  // 別タブからの「より新しいが schema 不一致 + appsData 欠落」な書き込みを synthetic に注入する。
  // STORAGE_KEY / SCHEMA_VERSION は js/constants.js の値 (Check 100 が theme-init と一致を強制)。
  await page.evaluate(() => {
    const malformed = JSON.stringify({
      schemaVersion: 1,              // 現行 (12) と不一致 = デプロイ跨ぎの旧 store を模す
      type: 'full-store',
      lastModified: 9999999999999,   // data.lastModified より十分新しい (採用条件を満たす)
      modifiedBy: 'E2E-OTHER-TAB',   // 自タブ TAB_ID と異なる (別タブ判定)
      theme: 'dark'
      // appsData / projects 等を意図的に欠落させる (raw 採用すると render が落ちる)
    });
    window.dispatchEvent(new StorageEvent('storage', {
      key: 'portfolio_enhanced_v45',
      newValue: malformed
    }));
  });

  // (1) FatalPage crash していない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `cross-tab malformed store caused a fatal render: ${fatal}`).toBeNull();

  // (2) 不正データは採用されず現タブの state は保持される (タスクが消えていない・page は機能する)
  await expect(page.getByText(ownTitle)).toBeVisible();
  await expect(page.locator('#task-input')).toBeVisible();
});


// ===== 7.1e: snapshot 復元は schema 不一致 / 欠損 snapshot を正規化して crash しない (#93/#295 class) =====
// SettingsPage の restoreSnapshot は importJSON (validateAndNormalize を通す) と違い
// State.set(snap.data) を生採用する未被覆 ingestion 経路だった。getSnapshot は旧 schema の
// legacy-snapshot を明示サポートし schema mismatch も warn するため、旧版が保存した projects/appsData
// 欠落 snapshot を復元すると state.projects.map 等でフィールド不在により SettingsPage 自身の render が
// crash し得た (#93/#295 と同 class = 外部入力 ingestion は全て正規化を通せ)。fix は restore も
// validateAndNormalize を通す。本テストは欠損 snapshot を注入 → 復元 → (1) FatalPage crash しない
// (2) settings が描画され続ける、を検証する (修正前は state.projects.map で落ちるため非 vacuous)。
test('Snapshot restore normalizes a foreign-schema/partial snapshot without crashing', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 旧版が保存した「schema 不一致 + projects/appsData 欠落」snapshot を localStorage に注入する。
  // SNAPSHOT_KEY は js/constants.js の 'portfolio_snapshot_v45' (raw key・Storage は JSON 文字列を格納)。
  await page.evaluate(() => {
    localStorage.setItem('portfolio_snapshot_v45', JSON.stringify({
      at: Date.now(),
      data: { schemaVersion: 1 }   // 現行 (12) と不一致・projects/appsData 等を意図的に欠落
    }));
  });
  await page.reload();
  await page.waitForLoadState('domcontentloaded');

  // 復元ボタン (snap があれば enabled) を押す
  const restoreBtn = page.getByRole('button', { name: '復元' });
  await expect(restoreBtn).toBeEnabled();
  await restoreBtn.click();

  // (1) FatalPage crash していない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `snapshot restore of a partial snapshot caused a fatal render: ${fatal}`).toBeNull();

  // (2) settings が描画され続ける (正規化で projects 等が backfill され render が成立)
  await expect(page.getByRole('heading', { name: 'Settings' })).toBeVisible();
});


// ===== 7.2: TODO アプリの追加→完了トグル→一括削除フロー Behavior Check =====
// #/apps/todo は TodoPage (task とは別 factory / 別 State slice) で、addTodo (Enter) /
// toggleTodo (checkbox) / clearCompleted (「完了済み削除」一括操作) という distinct な
// コードパスを持つ。task テスト (#91) が add+persist を見るのに対し、本テストは toggle と
// bulk 削除という別 operation class を実ブラウザで動的検証する。
// ===== 7.2b: TodoPage が ErrorBoundary/FatalPage の a11y 属性を誤って持たない (copy-paste leak 回帰ガード) =====
// TodoPage のルート div に role="alert" / aria-invalid="true" / aria-errormessage="fallback-details" /
// class="error-boundary-fallback" / aria-description="…unstable state transition" が紛れ込んでおり
// (実 FatalPage ですら error-boundary-fallback を使わず本箇所のみに存在＝leak)、スクリーンリーダーが
// TODO ページ全体をエラーアラート・invalid として読み上げ、aria-errormessage は TodoPage に存在しない
// #fallback-details を指す dangling 参照だった。fix は a11y 属性を除去 (視覚不変)。本テストは todo ルートで
// これらの error-boundary 痕跡が存在しないことを検証する (fix を戻すと count 1 で fail = 非 vacuous)。
test('Todo page carries no leaked ErrorBoundary a11y attributes (role=alert leak)', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByRole('heading', { name: 'クイックTODO' })).toBeVisible();
  // error-boundary-fallback class / aria-errormessage="fallback-details" は FatalPage 専用の痕跡で、
  // 正常な TODO ページには 1 つも存在してはならない (leak なら各 count が 1)。
  expect(await page.locator('.error-boundary-fallback').count()).toBe(0);
  expect(await page.locator('[aria-errormessage="fallback-details"]').count()).toBe(0);
});


test('Todo app add, complete-toggle, then clear-completed removes the item', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  const text = 'E2E-TODO-FLOW-CHECK-3389';
  await input.fill(text);
  await input.press('Enter');

  // 追加された
  const item = page.locator('article', { hasText: text });
  await expect(item).toBeVisible();

  // 完了トグル (checkbox) → clearCompleted (「完了済み削除」) でリストから消える
  await item.locator('input[type="checkbox"]').check();
  await page.getByRole('button', { name: '完了済み削除' }).click();
  await expect(page.getByText(text)).toHaveCount(0);

  // リロード後も削除が永続している (State auto-save)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(text)).toHaveCount(0);
});


// ===== 7.2: TODO 入力の IME composition ガード (compositionstart/end フラグ機構) =====
// todo-input は task/ai の e.isComposing とは別に、手動 todoComposing フラグ
// (oncompositionstart→true / oncompositionend→false) で IME 変換確定 Enter の誤追加を防ぐ。
// この既存ガードは未テストだった。composition 中の Enter では追加されず、compositionend 後の Enter
// では追加されることを実検証し、3 入力 (task/ai/todo) すべての IME 保護カバレッジを完成させる。
test('Todo input ignores Enter during IME composition (compositionstart flag)', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  const t = 'TODO-IME-COMPOSING-2300';
  await input.fill(t);

  // composition 中 (todoComposing=true) の Enter では追加しない
  await input.evaluate((el) => el.dispatchEvent(new CompositionEvent('compositionstart', { bubbles: true })));
  await input.evaluate((el) => el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true })));
  await expect(page.getByText(t)).toHaveCount(0);

  // compositionend 後 (todoComposing=false) の Enter では追加される
  await input.evaluate((el) => el.dispatchEvent(new CompositionEvent('compositionend', { bubbles: true })));
  await input.evaluate((el) => el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true })));
  await expect(page.getByText(t)).toBeVisible();
});


// ===== 7.2: TODO フィルタ (未完了/完了/全て) の絞り込み分岐 =====
// TodoPage は select(aria-label='TODO を絞り込み') で todoFilter を切替え、getFilteredTodos が
// active→未完了のみ / completed→完了のみ / all→全件、と分岐する。既存 TODO テストは add/toggle/
// clear を見るがこの 3 値フィルタ分岐は未カバーだった。2 件追加→1 件完了→各フィルタで表示集合が
// 切り替わることを実検証する (フィルタ条件が壊れたら退行検知)。
// ===== 7.2: TODO「完了済み削除」ボタンの disabled 状態 (完了 0 件で無効 → 完了化で有効) =====
// clearCompleted ボタンは `disabled: !todos.some(t => t.completed)` で、完了 TODO が 1 件も無いとき
// 無効・1 件でも完了すると有効になる。filter/flow テストはあるがこの disabled binding は未カバー
// だった。active な TODO 追加直後は無効、checkbox で完了にすると有効になることを検証する。
test('Todo clear-completed button is disabled until a todo is completed', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  await input.fill('CLEAR-DISABLED-TODO-9301');
  await input.press('Enter');
  const item = page.locator('article', { hasText: 'CLEAR-DISABLED-TODO-9301' });
  await expect(item).toBeVisible();

  const clearBtn = page.getByRole('button', { name: '完了済み削除' });
  // 完了 0 件 → 無効
  await expect(clearBtn).toBeDisabled();
  // 完了にすると有効
  await item.locator('input[type="checkbox"]').check();
  await expect(clearBtn).toBeEnabled();
});


test('Todo filter switches the visible set by active/completed/all', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  const done = 'E2E-TODO-DONE-6201';
  const active = 'E2E-TODO-ACTIVE-6202';

  // 1 件目を追加し、描画を待ってから 2 件目を追加 (連続追加の再描画レースを避ける)
  await input.fill(done);
  await input.press('Enter');
  await expect(page.getByText(done)).toBeVisible();
  await input.fill(active);
  await input.press('Enter');
  await expect(page.getByText(active)).toBeVisible();

  // done を完了にし、チェック反映を待つ
  const doneCheckbox = page.locator('article', { hasText: done }).locator('input[type="checkbox"]');
  await doneCheckbox.check();
  await expect(doneCheckbox).toBeChecked();

  const filter = page.locator('select[aria-label="TODO を絞り込み"]');

  // 完了 → done のみ表示・active は非表示
  await filter.selectOption('completed');
  await expect(page.getByText(done)).toBeVisible();
  await expect(page.getByText(active)).toHaveCount(0);

  // 未完了 → active のみ表示・done は非表示
  await filter.selectOption('active');
  await expect(page.getByText(active)).toBeVisible();
  await expect(page.getByText(done)).toHaveCount(0);

  // 全て → 両方表示
  await filter.selectOption('all');
  await expect(page.getByText(done)).toBeVisible();
  await expect(page.getByText(active)).toBeVisible();
});


// ===== 7.2: TODO filter select が再描画後も visual 選択を保持する (#7cbc4d9 class) =====
// todoFilter select の onchange は window.render() を直接呼ぶため再描画が走り、修正前は
// h('select', { value: todoFilter }) の setAttribute('value', ...) が無効で最初の option
// ('all') に戻っていた。修正後は各 option に selected: filter===cur ? true : undefined を付与。
test('Todo filter select retains visual selection after re-render (#7cbc4d9 class)', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const filter = page.locator('select[aria-label="TODO を絞り込み"]');
  await expect(filter).toBeVisible();

  // 'active' に変更 → window.render() → 再描画後も 'active'
  await filter.selectOption('active');
  await expect(filter).toHaveValue('active');

  // 'completed' に変更 → 再描画後も 'completed'
  await filter.selectOption('completed');
  await expect(filter).toHaveValue('completed');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `todo filter select caused a fatal: ${fatal}`).toBeNull();
});
