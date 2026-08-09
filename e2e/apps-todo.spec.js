const { test, expect } = require('@playwright/test');




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
  // [FIX] 不在アサーションは「まだ描画されていない」を「無い」と誤認して vacuous に PASS しうる
  //   (toHaveCount(0) は初回 poll で成立すると再検査されない)。先に「必ず在るはず」の要素を待って
  //   描画を確定させてから不在を検査する (#825/#830 class・Check 402 が構造強制)。
  await expect(page.getByLabel('やることを入力')).toBeVisible();
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


// ===== 7.2: TODO の完了状態が reload を跨いで永続する (completed boolean normalize round-trip) =====
// 完了トグルで立てた completed=true が localStorage → load → normalizeAppsData
// (`completed: Boolean(t.completed)`) の round-trip を跨いで保持されることを検証する。既存 todo
// テストは add+完了+一括削除 (#412 は完了 todo を clearCompleted で除去してから reload=削除永続を見る) /
// filter / disabled で、「完了 todo を clear せず reload して completed が残る」検証は無かった。このため
// normalize の `completed: Boolean(t.completed)` を `completed: false` 等へ regress すると全 todo が
// reload 後 active に戻るが既存テストは全て緑で素通りする (#294/#568/#684/#796 = normalize が reload で
// field を drop/default する同 class)。完了→reload→保持を検証しこの穴を塞ぐ。
test('Todo completed state persists across reload (completed normalize round-trip)', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  const text = 'TODO-COMPLETED-PERSIST-7150';
  await input.fill(text);
  await input.press('Enter');

  const checkbox = page.locator('article', { hasText: text }).locator('input[type="checkbox"]');
  await checkbox.check();
  await expect(checkbox).toBeChecked();

  // reload (visibilitychange → saveNow で flush) → load → normalizeAppsData を跨いで completed=true 保持
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  const checkboxAfter = page.locator('article', { hasText: text }).locator('input[type="checkbox"]');
  await expect(checkboxAfter).toBeChecked();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `todo completed reload persist caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: 条件描画 `cond && h()` の false 子が "false" として描画されない (h() boolean skip) =====
// TodoPage は `filtered.length === 0 && h('p', 'TODOはありません')` で空状態を条件描画する。todo が
// 存在する (filtered.length !== 0) と式は false を返し、これが親 h() の子として渡る。h() が boolean 子を
// skip しないと createTextNode(String(false))='false' でリスト末尾にリテラル "false" が可視描画される
// 実バグ (デフォルト store は seed todo を持つため初期表示で発現・screenshot は advisory ゆえ素通り)。
// h() の children ループで boolean を skip する修正の回帰ガード。fix を戻すと "false" が現れ RED = 非 vacuous。
test('Todo list with items does not render a literal "false" (h() skips boolean children)', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#todo-input');
  await expect(input).toBeVisible();
  await input.fill('NO-FALSE-RENDER-TODO-4821');
  await input.press('Enter');
  await expect(page.getByText('NO-FALSE-RENDER-TODO-4821')).toBeVisible();

  // filtered.length !== 0 のとき条件描画の false 子が "false" テキストとして leak しないこと
  const txt = await page.locator('#content').innerText();
  expect(txt, 'a literal "false" leaked from a `cond && h()` child (h() must skip boolean children)').not.toMatch(/(^|\n)\s*false\s*(\n|$)/);
});


// ===== 7.1: import ingestion が MAX_TODOS 件数上限で切り詰められる (bloat/DoS ガード) =====
// MAX_TASKS (#801) と同クラスで、store.js normalizeAppsData は todos を
// `.slice(0, CONSTANTS.LIMITS.MAX_TODOS)` (=1000) で件数上限切り詰めする distinct な slice 行を持つ。
// tasks/todos はユーザが作成する 2 つのリストアプリで、両方の件数上限ガードを behavior 被覆する
// (projects は curated / ai・pomodoro history は auto 生成ゆえ本 class の対象外)。1050 件を seed して
// 先頭 1000 (TODO-CAP-0000/0999) は残り上限直上以降 (TODO-CAP-1000/1049) は drop を検証する。
// slice(0, MAX_TODOS) 除去で 1050 件全部残り TODO-CAP-1049 が現れ本テストが RED (非 vacuous)。
test('Import truncates todos to MAX_TODOS (bloat/DoS ingestion guard)', async ({ page }) => {
  await page.addInitScript(() => {
    const todos = [];
    for (let i = 0; i < 1050; i++) {
      const n = String(i).padStart(4, '0');
      todos.push({ id: 'd' + n, text: 'TODO-CAP-' + n, completed: false });
    }
    localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
      schemaVersion: 12, type: 'full-store', appsData: { todos }
    }));
  });

  await page.goto('/#/apps/todo');
  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('TODO-CAP-0000', { exact: true })).toBeVisible();
  await expect(page.getByText('TODO-CAP-0999', { exact: true })).toBeVisible();
  // MAX_TODOS(1000) を超える index 1000/1049 は slice(0,1000) で切り詰められ存在しない
  await expect(page.getByText('TODO-CAP-1000', { exact: true })).toHaveCount(0);
  await expect(page.getByText('TODO-CAP-1049', { exact: true })).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `MAX_TODOS truncation caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: TODO の checkbox / 削除ボタンが accessible name に todo.text を含み一意化される =====
// 各 TODO の完了トグル checkbox と削除ボタンは、修正前は全項目で同一 aria-label
// (「完了にする」「削除」) を持ち、SR ユーザーがリスト内でどの TODO を操作するか区別できなかった
// (WCAG 4.1.2 Name,Role,Value)。todo.text を accessible name に含め一意化する。2 件追加し、各々の
// checkbox / 削除ボタンが「…：<そのtext>」で個別に引けることを検証する (text を外すと getByLabel の
// 名前引きが両項目で衝突/失敗し RED = 非 vacuous)。
test('Todo checkbox and delete button include the todo text in their accessible name', async ({ page }) => {
  await page.goto('/#/apps/todo', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#todo-input')).toBeVisible();

  const a = 'TODO-A11Y-NAME-ALPHA-71';
  const b = 'TODO-A11Y-NAME-BRAVO-72';
  // addTodo は全体再描画で #todo-input を作り直すため、1 件確定を待ってから毎回引き直して入力する。
  await page.locator('#todo-input').fill(a);
  await page.locator('#todo-input').press('Enter');
  await expect(page.getByText(a)).toBeVisible();
  await page.locator('#todo-input').fill(b);
  await page.locator('#todo-input').press('Enter');
  await expect(page.getByText(b)).toBeVisible();

  // 各 checkbox が todo.text 込みの一意な accessible name で引ける (未完了時は「完了にする：<text>」)。
  await expect(page.getByRole('checkbox', { name: `完了にする：${a}` })).toHaveCount(1);
  await expect(page.getByRole('checkbox', { name: `完了にする：${b}` })).toHaveCount(1);
  // 削除ボタンも同様に一意 (「削除：<text>」)。
  await expect(page.getByRole('button', { name: `削除：${a}` })).toHaveCount(1);
  await expect(page.getByRole('button', { name: `削除：${b}` })).toHaveCount(1);

  // 完了トグル後は checkbox 名が「未完了に戻す：<text>」へ追従する。
  // (再描画のたびに checkbox 要素が作り直され actionability 判定が不安定なため、onchange を
  //  dispatchEvent で直接発火して toggleTodo を呼ぶ。名前の追従だけを検証する。)
  await page.getByRole('checkbox', { name: `完了にする：${a}` }).dispatchEvent('change');
  await expect(page.getByRole('checkbox', { name: `未完了に戻す：${a}` })).toHaveCount(1);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `todo item a11y caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: TODO の追加/削除が assertive aria-live 領域へアナウンスされる (WCAG 4.1.3・task 対称) =====
// addTask/deleteTask は Toast(#action-announcement へ書き込む)で SR に成功を通知するのに、todo の
// addTodo/deleteTodo だけ Toast が欠落し無通知だった (「1 ケースだけ処理・他を忘れる」asymmetry)。
// task と対称に Toast を追加。追加/削除後に assertive 領域へ status message が入ることを検証する
// (Toast を外すと空のままで RED = 非 vacuous)。
test('Todo add and delete announce to the assertive aria-live region (WCAG 4.1.3, task symmetry)', async ({ page }) => {
  await page.goto('/#/apps/todo', { waitUntil: 'domcontentloaded' });
  const announcer = page.locator('#action-announcement');
  await expect(announcer).toHaveText('');

  const t = 'TODO-ANNOUNCE-掃除-8842';
  await page.locator('#todo-input').fill(t);
  await page.locator('#todo-input').press('Enter');
  // 追加が assertive 領域へアナウンスされる。
  await expect(announcer).toHaveText('TODOを追加しました');
  await expect(page.getByText(t)).toBeVisible();

  // 削除も同様にアナウンスされる (削除ボタンは aria-label「削除：<text>」で一意)。
  await page.getByRole('button', { name: `削除：${t}`, exact: true }).click();
  await expect(announcer).toHaveText('TODOを削除しました');
  await expect(page.getByText(t)).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `todo announce caused a fatal: ${fatal}`).toBeNull();
});
