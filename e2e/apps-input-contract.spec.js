const { test, expect } = require('@playwright/test');

// ===== テキスト入力の契約 (task / todo の入力欄) =====
//
// 元は e2e/apps-task.spec.js にあったが、同 file が 957 行となり Check 365 の BLOCKING
// (1,000 行) まで残り 43 行になったため、**当たる前に**このテーマの塊を切り出した
// (CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。
//
// このファイルが守るもの — いずれも「打った文字がどう扱われるか」の契約:
//   - 空 / 空白だけの入力は項目を作らない (trim ガード)
//   - **表示だけの操作** (絞り込み) の巻き添えで未送信の入力を消さない (#1055)
//   - Enter の連打 / キーリピートで同じ項目を二重登録しない (#1061)
//
// 三つとも「利用者が打った文字が黙って失われる / 意図せず増える」class で、
// 視覚的には一瞬の出来事なので**気付いたときには理由が分からない**のが共通点。



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




// ===== 絞り込みの変更が「新しいタスク」の未送信テキストを消さない =====
// 絞り込みは **表示だけの操作** なのに、従来は onchange が `window.render()` を呼んで
// #content ごとページを作り直しており、その巻き添えで **打ちかけたタスク名が消えていた**
// (実測: 8 文字 → 0)。絞り込んで既存タスクを確認してから続きを打つ、は自然な操作なので
// 実害が大きい。#982 (テーマ切替が入力を消した) / #258 (oninput の全再描画) と同じ
// 「無関係な操作の巻き添え」class で、ProjectsPage / QuizPage が既に採っている
// listHost + 手動再描画へ揃えた。
//
// NOTE: `selectOption()` は選択後に focus を select に残さないため、focus 復元を測る用途では
// 使えない (常に false RED になる)。ここでは値の保持を見るので影響しないが、キーボード相当の
// 操作を再現するため change を明示的に dispatch する。
test('タスクの絞り込みを変えても未送信の入力が消えない', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();

  const draft = 'FILTER-DRAFT-KEEP-7701';
  await page.locator('#task-input').fill(draft);

  await page.locator('#task-filter-priority').evaluate((el) => {
    el.focus();
    el.value = 'high';
    el.dispatchEvent(new Event('change', { bubbles: true }));
  });
  // control: 絞り込みが実際に切り替わっていること (切り替わっていなければ何も検査していない)
  await expect(page.locator('#task-filter-priority')).toHaveValue('high');

  await expect(page.locator('#task-input'),
    '絞り込みの巻き添えで未送信の入力が消えている').toHaveValue(draft);
});


// ===== Enter の連打 / キーリピートで同じ項目が二重登録されない =====
// 入力欄が空になるのは **再描画の副作用**だが、その再描画は非同期 (await yieldToMain) なので、
// Enter を続けて押す / 押しっぱなしでキーリピートが走ると `e.target.value` はまだ元の文字列を
// 持っており、**同じ値が何度も登録される** (実測: 3 回押して 3 件の同名タスク)。
// 値を読んだら同期でクリアし、2 回目以降は空ガードが弾くようにした。
test('タスク入力の Enter 連打で同じタスクが二重登録されない', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();

  const input = page.locator('#task-input');
  await input.fill('RAPID-ENTER-9901');
  // [重要] `press()` を 3 回呼ぶと、**1 回目が起こす再描画の速さ次第で 2 回目以降が
  //   新しい空の入力欄に当たり**、バグがあっても重複が起きないことがある (実測: ローカルでは
  //   再現するのに CI では mutation が SURVIVED した)。キーリピートは「再描画を待たずに
  //   同じ要素へ連続で keydown が来る」現象なので、**同期的に 3 回 dispatch** して
  //   その条件を正確に作る。
  await input.evaluate((el) => {
    for (let i = 0; i < 3; i++) {
      el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
    }
  });

  // [重要] ここで直に件数を数えると **重複が描画される前に** `toHaveCount(1)` が成立して
  //   しまい、バグがあっても緑になる (実測でこの形の vacuous テストを踏んだ)。
  //   State の更新は keydown で同期に済んでいるので、**一度ルートを離れて戻り**、確定した
  //   state から描き直させてから数える (時間待ちにも、描画の途中経過にも依存しない)。
  //   NOTE: 同じ入力欄へ sentinel を足す方法も試したが、フルスイートの負荷下では
  //   `fill` が再描画で detach された input を掴んで不安定だった (#1053 と同じ罠)。
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'About' })).toBeVisible();
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();

  await expect(page.locator('#content').getByText('RAPID-ENTER-9901', { exact: true }),
    'Enter の連打で同じタスクが複数登録されている').toHaveCount(1);
});


