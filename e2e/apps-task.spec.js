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
  await page.locator('article', { hasText: title }).getByRole('button', { name: '次のステータスへ進める' }).click();
  await expect(inProgress.getByText(title)).toBeVisible();

  // もう一度 → で 完了 へ
  await page.locator('article', { hasText: title }).getByRole('button', { name: '次のステータスへ進める' }).click();
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


// ===== 7.2: task per-card priority 変更が reload を跨いで永続する (normalize round-trip) =====
// updateTask で変更した非デフォルト priority ('high') が localStorage → load → normalizeAppsData の
// round-trip を跨いで保持されることを検証する。既存の add-persist (#23) は既定 'med' のみ、per-card
// visual (#174) は同一セッションのみ、filter (#134) は reload しない。store.js normalizeAppsData の
// priority 正規化行 (`priority: [...].includes(t.priority) ? t.priority : 'med'`) を `priority: 'med'`
// 等へ regress しても既存テストは全て緑で素通りする (#294/#568/#684 = normalize が reload で field を
// drop/default する同 class)。非デフォルト priority を設定→reload→保持を検証し正規化 round-trip の穴を塞ぐ。
test('Task per-card priority change persists across reload (normalize round-trip)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  const title = 'PRIORITY-PERSIST-TASK-8830';
  await input.fill(title);
  await input.press('Enter');
  await expect(page.getByText(title)).toBeVisible();

  // 既定 'med' から非デフォルト 'high' へ変更 (updateTask → State.update → scheduleSave)
  const cardSel = page.locator('article', { hasText: title }).getByLabel('タスクの優先度');
  await cardSel.selectOption('high');
  await expect(cardSel).toHaveValue('high');

  // reload (visibilitychange → saveNow で flush) → load → normalizeAppsData を跨いで 'high' が保持される
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  const cardSelAfter = page.locator('article', { hasText: title }).getByLabel('タスクの優先度');
  await expect(cardSelAfter).toHaveValue('high');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `priority reload persist caused a fatal: ${fatal}`).toBeNull();
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

  // [重要] 注入前に blur する。タスク追加の Enter 後は #task-input に focus が戻るため、
  //   そのまま注入すると state.js の「編集中は cross-tab 採用を blur まで延期する」ガード
  //   (in-progress edit の破壊を防ぐ実バグ修正) を通ってしまい、本テストが検証したい
  //   **採用経路そのもの** が走らない = 何を壊しても緑になる vacuous テストになる。
  await page.evaluate(() => document.activeElement && document.activeElement.blur());

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

  // [FIX 2026-08-10] **順序が逆だった**。復元は State.set → notify → `await yieldToMain()` を挟む
  //   非同期 render なので、click 直後に `__fatalError` を単発で読むと「まだ crash していない」を
  //   「crash しない」と誤認する (このリポジトリが記録している absence-assertion race / Check 402 と
  //   同じ class)。週次 probe が CI でのみ本 test の mutation を SURVIVED と報告した
  //   (ローカルはフル probe でも 145/145 caught) 事象の、唯一特定できた timing 依存がこれ。
  //   **先に「描画が成立したこと」を positive assertion で待ってから** fatal を読む。
  //
  //   NOTE: fatal 検査に expect.poll は使わない。ここで守るのは「fatal にならない」という
  //   **不変性**で、poll は最初の観測で成功すると以降の変化を見逃す (§7 の教訓)。
  //   settle させてから 1 度だけ読むのが正しい。

  // (1) settings が描画され続ける (正規化で projects 等が backfill され render が成立)
  await expect(page.getByRole('heading', { name: 'Settings' })).toBeVisible();
  // FatalPage は #fallback-details を持つ。描画が確定した後に「無いこと」を確認する
  await expect(page.locator('#fallback-details')).toHaveCount(0);

  // (2) FatalPage crash していない (render 確定後に単発で読む)
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `snapshot restore of a partial snapshot caused a fatal render: ${fatal}`).toBeNull();
});


// ===== 7.1: import ingestion が MAX_TASKS 件数上限で切り詰められる (bloat/DoS ガード) =====
// store.js normalizeAppsData は tasks を `.slice(0, CONSTANTS.LIMITS.MAX_TASKS)` (=500) で件数上限
// 切り詰めする。これは import/cross-tab/snapshot 経由で巨大タスク配列が localStorage を bloat させ
// 描画を重くする DoS を防ぐ ingestion ガード。文字列長 bound (AI_MESSAGE #230) は test 済だが件数
// 上限 (MAX_TASKS/MAX_TODOS/MAX_PROJECTS) の切り詰めは未被覆だった。600 件を seed して load し、
// 先頭 500 (TASK-CAP-000) は残り 501 件目以降 (TASK-CAP-599) は drop されることを検証する。
// slice(0, MAX_TASKS) を除去すると 600 件全部残り TASK-CAP-599 が現れ本テストが RED (非 vacuous)。
test('Import truncates tasks to MAX_TASKS (bloat/DoS ingestion guard)', async ({ page }) => {
  await page.addInitScript(() => {
    const tasks = [];
    for (let i = 0; i < 600; i++) {
      const n = String(i).padStart(3, '0');
      tasks.push({ id: 't' + n, title: 'TASK-CAP-' + n, status: 'backlog', priority: 'med', tags: [] });
    }
    localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
      schemaVersion: 12, type: 'full-store', appsData: { tasks }
    }));
  });

  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  // 先頭 (index 0) は残る
  await expect(page.getByText('TASK-CAP-000', { exact: true })).toBeVisible();
  // MAX_TASKS(500) を超える index 599 は slice(0,500) で切り詰められ存在しない
  await expect(page.getByText('TASK-CAP-599', { exact: true })).toHaveCount(0);
  // ちょうど上限内の index 499 は残り、上限直上の index 500 は落ちる
  await expect(page.getByText('TASK-CAP-499', { exact: true })).toBeVisible();
  await expect(page.getByText('TASK-CAP-500', { exact: true })).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `MAX_TASKS truncation caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: タスク移動ボタン (←/→) の SR アクセシビリティ (aria-label で目的明示) =====
// カンバンのステータス移動ボタンは矢印グリフ (←/→) のみを content に持ち、従来 aria-label が
// 無く SR には「← ボタン」としか聞こえず、タスクをステータス間で移動する目的が不明だった
// (WCAG 2.4.4 Link Purpose / 4.1.2 Name,Role,Value)。方向を aria-label で明示する。本テストは
// 追加したタスクの → ボタンが「次のステータスへ進める」の accessible name を持ち、クリックで実際に
// ステータスが進む (backlog→in-progress) ことを検証する (aria-label を外すと getByRole 名前引きが
// 失敗し RED = 非 vacuous)。
test('Task move buttons expose an aria-label describing their purpose for screen readers', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  const input = page.locator('#task-input');
  await input.fill('A11Y-MOVE-BTN-9021');
  await input.press('Enter');
  await expect(page.getByText('A11Y-MOVE-BTN-9021')).toBeVisible();

  // 新規タスクは backlog(未着手)。「次のステータスへ進める」ボタンが accessible name で引ける。
  const forwardBtn = page.getByRole('button', { name: '次のステータスへ進める' }).first();
  await expect(forwardBtn).toBeVisible();
  // 「前のステータスへ戻す」ボタンも存在する (backlog なので disabled)。
  await expect(page.getByRole('button', { name: '前のステータスへ戻す' }).first()).toBeDisabled();

  // クリックで実際にステータスが進む (backlog→in-progress)。進行中列にタスクが現れる。
  await forwardBtn.click();
  const inProgressCol = page.locator('section').filter({ has: page.getByRole('heading', { name: '進行中' }) });
  await expect(inProgressCol.getByText('A11Y-MOVE-BTN-9021')).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `task move btn a11y caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.1: タスクカードの削除/優先度/移動ボタンが accessible name に task.title を含み一意化 =====
// カンバンは複数タスクを並べるが、修正前は各カードの削除ボタン(「タスクを削除」)/優先度 select
// (「タスクの優先度」)/移動ボタン(「前/次のステータスへ…」)が全カードで同一 aria-label を持ち、
// SR ユーザーがどのタスクの操作か区別できなかった (WCAG 4.1.2)。task.title を suffix し一意化する
// (既存フレーズは prefix として残るため getByRole/getByLabel の substring 引きは非破壊)。2 タスク
// 追加し各操作要素が title 込みの一意名で個別に引けることを検証 (title suffix を外すと衝突し RED)。
test('Task card controls include the task title in their accessible name (unique per card)', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  const t1 = 'TASK-A11Y-NAME-ONE-81';
  const t2 = 'TASK-A11Y-NAME-TWO-82';
  await page.locator('#task-input').fill(t1);
  await page.locator('#task-input').press('Enter');
  await expect(page.getByText(t1)).toBeVisible();
  await page.locator('#task-input').fill(t2);
  await page.locator('#task-input').press('Enter');
  await expect(page.getByText(t2)).toBeVisible();

  // 削除ボタン: title 込みで各カード一意に引ける。
  await expect(page.getByRole('button', { name: `タスクを削除：${t1}`, exact: true })).toHaveCount(1);
  await expect(page.getByRole('button', { name: `タスクを削除：${t2}`, exact: true })).toHaveCount(1);
  // 優先度 select: title 込みで一意 (getByLabel exact)。
  await expect(page.getByLabel(`タスクの優先度：${t1}`, { exact: true })).toHaveCount(1);
  await expect(page.getByLabel(`タスクの優先度：${t2}`, { exact: true })).toHaveCount(1);
  // 移動ボタン: 「次のステータスへ進める：<title>」で一意。
  await expect(page.getByRole('button', { name: `次のステータスへ進める：${t1}`, exact: true })).toHaveCount(1);
  await expect(page.getByRole('button', { name: `次のステータスへ進める：${t2}`, exact: true })).toHaveCount(1);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `task card a11y caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.1: task move ボタンの done 境界 disabled (backlog 境界と対称) =====
// カンバンの「次のステータスへ進める」は done で `disabled: task.status === 'done'`、「前のステータスへ
// 戻す」は backlog で disabled。move-button テストは backlog 境界 (prev disabled) を見るが done 境界
// (next disabled) は未カバーだった。moveStatus は clamp で範囲外遷移を防ぐが、disabled 属性はユーザ/SR
// への「これ以上進めない」affordance で、外れると done でも次へ進めるかに見える UX 退行になる。タスクを
// done まで進め、next が disabled・prev が有効になることを検証する (backlog 境界と対称の被覆)。
test('Task move forward button is disabled at the done boundary (symmetry with backlog)', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  const title = 'TASK-DONE-BOUNDARY-9701';
  await page.locator('#task-input').fill(title);
  await page.locator('#task-input').press('Enter');
  await expect(page.getByText(title)).toBeVisible();

  const fwdName = `次のステータスへ進める：${title}`;
  const backName = `前のステータスへ戻す：${title}`;
  // backlog→in-progress→done へ 2 回進める (各クリックで再描画されるため都度引き直す)。
  await page.getByRole('button', { name: fwdName, exact: true }).click();
  await page.getByRole('button', { name: fwdName, exact: true }).click();

  // done 列にタスクが入る。
  const doneCol = page.locator('section').filter({ has: page.getByRole('heading', { name: '完了' }) });
  await expect(doneCol.getByText(title)).toBeVisible();

  // done 境界: next は disabled、prev は有効 (backlog 境界の鏡)。
  await expect(page.getByRole('button', { name: fwdName, exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { name: backName, exact: true })).toBeEnabled();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `task done-boundary caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.1: task/todo の空/空白入力ガード (addTask/addTodo の trim ガード) =====
// addTask は `if (!title.trim()) return`、addTodo は `if (!text.trim()) return` で空文字/空白のみの
// Enter を握り潰す。settings のプロジェクト追加は空入力バリデーションを検証するが、task/todo の空入力
// ガードは未カバーだった。ガードが外れると空/空白 Enter が空タイトルの項目を積み UI/localStorage を汚す。
// 各アプリで空・空白 Enter が項目数を増やさないこと + 対照の非空入力は +1 することを検証する
// (seed 項目があるため絶対数でなくベースラインからの増分で判定)。
test('Task and Todo ignore empty/whitespace-only input (no item created)', async ({ page }) => {
  // --- Task ---
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  const taskInput = page.locator('#task-input');
  await expect(taskInput).toBeVisible();
  const taskCards = page.locator('article.bg-surface');
  const baseTasks = await taskCards.count();
  await taskInput.fill(''); await taskInput.press('Enter');
  await expect(taskCards).toHaveCount(baseTasks);
  await taskInput.fill('   '); await taskInput.press('Enter');
  await expect(taskCards).toHaveCount(baseTasks);
  // 対照: 非空は +1 (ガードが Enter-submit 自体を殺していない)。
  await taskInput.fill('TASK-EMPTY-GUARD-CTRL'); await taskInput.press('Enter');
  await expect(page.getByText('TASK-EMPTY-GUARD-CTRL')).toBeVisible();
  await expect(taskCards).toHaveCount(baseTasks + 1);

  // --- Todo ---
  await page.goto('/#/apps/todo', { waitUntil: 'domcontentloaded' });
  const todoInput = page.locator('#todo-input');
  await expect(todoInput).toBeVisible();
  const todoItems = page.locator('section.flex.flex-col.gap-2 article.card');
  const baseTodos = await todoItems.count();
  await todoInput.fill(''); await todoInput.press('Enter');
  await expect(todoItems).toHaveCount(baseTodos);
  await todoInput.fill('   '); await todoInput.press('Enter');
  await expect(todoItems).toHaveCount(baseTodos);
  // 対照: 非空は +1。
  await todoInput.fill('TODO-EMPTY-GUARD-CTRL'); await todoInput.press('Enter');
  await expect(page.getByText('TODO-EMPTY-GUARD-CTRL')).toBeVisible();
  await expect(todoItems).toHaveCount(baseTodos + 1);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `task/todo empty guard caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.1: import ingestion が MAX_PROJECTS 件数上限で切り詰められる (bloat/DoS ガード) =====
// store.js mergeProjectsWithDefaults は projects の件数を MAX_PROJECTS (=1000) で 2 層 cap する:
// (1) normalizedIncoming を slice(0, MAX_PROJECTS)、(2) 最終 merged を slice(0, MAX_PROJECTS)。
// MAX_TASKS/MAX_TODOS は単層 slice で test 済だが MAX_PROJECTS は未被覆だった。1050 件 (defaults 込みで
// cap 超過) を seed して load し、先頭は残り 1000 件超の高 index (PROJ-CAP-1049) は drop されることを
// 検証する。NOTE: 2 層 cap は冗長防御ゆえ片層 slice の除去は他層が self-heal し observable が変わらない
// (mutation SURVIVED)。よって clean な単一 mutation を E2E_MUTATIONS へ登録できない (両 slice 除去で
// 初めて 1049 が出現し RED = total cap failure に対する非 vacuity は手動実測済)。
test('Import truncates projects to MAX_PROJECTS (bloat/DoS ingestion guard)', async ({ page }) => {
  await page.addInitScript(() => {
    const projects = [];
    for (let i = 0; i < 1050; i++) {
      const n = String(i).padStart(4, '0');
      projects.push({ id: 'pcap' + n, slug: 'pcap-' + n, name: 'PROJ-CAP-' + n, category: 'Cap', summary: 's', tech: [], tags: [], demoRoute: null });
    }
    localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({ schemaVersion: 12, type: 'full-store', projects }));
  });

  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('PROJ-CAP-0000', { exact: true })).toBeVisible();
  await expect(page.getByText('PROJ-CAP-1049', { exact: true })).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `MAX_PROJECTS truncation caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: フィルタ変更が SR に announce される (WCAG 4.1.3) =====
// task/todo のフィルタ変更は視覚的には一覧が変わるのに **SR には完全に無音**だった (実測: 変更後も
// 通知領域には直前のアクション文言が残ったままで、#content 内に live region は 0 個)。選択肢名と
// 件数を唯一の通知チャネル #action-announcement (sr-only) へ流す。両アプリで検証する。
test('Task and Todo filter changes are announced with the option name and count (WCAG 4.1.3)', async ({ page }) => {
  const ann = page.locator('#action-announcement');

  // TODO: 「完了」へ絞り込む → 選択肢名 + 件数が announce される
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByLabel('やることを入力')).toBeVisible();
  await page.getByLabel('TODO を絞り込み').selectOption('completed');
  await expect(ann).toHaveText(/^TODO: 完了 \d+ 件$/);

  // Task: 優先度 High へ絞り込む → 同様に announce される
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByLabel('新しいタスクを入力')).toBeVisible();
  await page.getByLabel('優先度で絞り込み').selectOption('high');
  await expect(ann).toHaveText(/^優先度: High \d+ 件$/);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `filter announce caused a fatal: ${fatal}`).toBeNull();
});


// ===== cross-tab 更新が「入力中」のテキストと focus を破壊しない (実バグ #939 系) =====
// storage イベントによる採用は notify() = #content 全再描画を伴う。従来はこれを無条件に適用して
// いたため、**別タブでタスクを 1 件追加しただけで、こちらのタブで書きかけの notes が巻き戻り
// activeElement が body へ落ちた**（実測）。#258 の「再描画が focused input を破棄する」class が、
// 自分のキーストロークではなく外部イベント起点で起きていたもの。
// 修正は「編集中なら採用を blur まで延期する」。延期であって破棄ではないため、cross-tab 更新自体は
// 失われない — 後半でそれも検証する（延期が握り潰しになっていたら、それは別の退行になる）。
test('Cross-tab update does not destroy an in-progress edit, and is adopted on blur', async ({ context }) => {
  const tabA = await context.newPage();
  await tabA.goto('/#/apps/notes');
  await tabA.waitForLoadState('domcontentloaded');
  await tabA.locator('#notes-input').click();
  await tabA.keyboard.type('TAB-A-編集中');
  // 自タブの debounce save を先に確定させ、incoming が「より新しい」状況を確実に作る
  await tabA.waitForTimeout(700);

  const tabB = await context.newPage();
  await tabB.goto('/#/apps/task');
  await tabB.waitForLoadState('domcontentloaded');
  await tabB.locator('#task-input').fill('TAB-B-タスク');
  await tabB.locator('#task-input').press('Enter');
  await expect(tabB.locator('#content')).toContainText('TAB-B-タスク');

  await tabA.bringToFront();
  await tabA.waitForTimeout(600);

  // 1. 書きかけのテキストが残っている (修正前はここで巻き戻っていた)
  await expect(tabA.locator('#notes-input')).toHaveValue(/TAB-A-編集中/);
  // 2. focus も奪われていない (toBeFocused は並列ワーカーで不安定なため activeElement を直接読む)
  const focusedId = await tabA.evaluate(() => (document.activeElement && document.activeElement.id) || 'none');
  expect(focusedId, 'cross-tab 更新が編集中フィールドから focus を奪った').toBe('notes-input');

  // 3. blur すると保留していた cross-tab 更新が採用される (= 握り潰していない)
  //    リロードすると localStorage の書き込み競合を見てしまうため、SPA 内遷移で in-memory state を見る
  await tabA.evaluate(() => document.getElementById('notes-input')?.blur());
  await tabA.waitForTimeout(700);
  await tabA.evaluate(() => { location.hash = '#/apps/task'; });
  await expect(tabA.locator('#content')).toContainText('TAB-B-タスク');

  const fatal = await tabA.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `cross-tab defer caused a fatal: ${fatal}`).toBeNull();
});


// ===== タスク 0 件のときに「なぜ空か」を示す (TodoPage との非対称の是正) =====
// 従来は優先度フィルタで 0 件になっても 3 列に「0」が並ぶだけで、**フィルタが隠しているのか
// 本当に空なのか判別できなかった**。TodoPage は同じ状況で「TODOはありません。」を出しており、
// task 側だけが欠けていた (「1 ケースだけ処理して他を忘れる」非対称・CLAUDE.md §7 の反復 class)。
// フィルタ由来か本当に空かで文言を分け、前者は解除方法まで示す。
test('Task board explains why it is empty (filtered vs genuinely empty)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  const filter = page.locator('select[aria-label="優先度で絞り込み"]');
  await expect(filter).toBeVisible();

  // 既定ではタスクがあるのでメッセージは出ない (常時表示なら以降が vacuous)
  await expect(page.locator('#content')).not.toContainText('タスクはありません');

  // (1) フィルタで 0 件 → 「絞り込みのせい」と判る文言
  await filter.selectOption('med');
  await expect(page.locator('#content')).toContainText('この優先度に一致するタスクはありません');

  // (2) 絞り込みを戻すと消える
  await filter.selectOption('all');
  await expect(page.locator('#content')).not.toContainText('この優先度に一致するタスクはありません');

  // (3) 本当に 0 件なら追加方法を示す文言 (フィルタ由来と区別できること)
  await page.evaluate(() => {
    document.querySelectorAll('button[aria-label^="タスクを削除"]').forEach((b) => b.click());
  });
  await expect(page.locator('#content')).toContainText('上の入力欄から追加できます');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `task empty-state caused a fatal: ${fatal}`).toBeNull();
});
