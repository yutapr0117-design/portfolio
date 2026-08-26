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




// ===== 7.4: 上限で断られたとき、打った文字を消さない (#1259 の実バグ) =====
// addTask / addTodo は上限 (MAX_TASKS=500 / MAX_TODOS=1000) に達していると Toast で断るが、
// 呼び出し側の onkeydown は **addTask を呼ぶ前に無条件で入力欄をクリア**していた。
// クリア自体は必要 (キーリピートでの二重登録防止・#1061) だが、断られた場合まで消すと
// 「不要なタスクを削除してください」と言われた時点で **打った内容が既に失われている**。
// 実測 (2026-08-21・修正前): 500 件の状態で「大事な新しいタスク」+ Enter →
//   toast="タスクは 500 件までです…" / 入力欄="" ── 削除して戻っても打ち直しになる。
//
// seed は **アプリ自身に store を作らせてから膨らませる**。schemaVersion や key を決め打ちすると
// 不一致で既定値へフォールバックし、**上限に達していない状態を測って緑になる** (実際に 1 度踏んだ)。
//
// 非 vacuity: `if (!addTask(_v)) { e.target.value = _v; }` を `addTask(_v);` へ戻すと入力欄が
// 空になり RED。対照として「上限に達していなければ従来どおり消える」も同じ test で見る
// (無条件に復元する実装 = 二重登録ガードを殺した実装 も落とせるようにするため)。
test('Task input keeps the typed text when the add is refused by the cap', async ({ browser }) => {
  // 1) アプリ自身に store を作らせ、実際の key と中身を得る
  const seedCtx = await browser.newContext();
  const seedPage = await seedCtx.newPage();
  await seedPage.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(seedPage.locator('#task-input')).toBeVisible();
  await seedPage.locator('#task-input').fill('CAP-SEED');
  await seedPage.locator('#task-input').press('Enter');
  await expect(seedPage.getByText('CAP-SEED')).toBeVisible();
  const dump = await seedPage.evaluate(async () => {
    // debounce 保存の完了を待ってから読む (直後は null のことがある)
    for (let i = 0; i < 40; i++) {
      for (const k of Object.keys(localStorage)) {
        const v = localStorage.getItem(k);
        if (v && v.includes('CAP-SEED')) { return { k, v }; }
      }
      await new Promise(r => setTimeout(r, 50));
    }
    return null;
  });
  await seedCtx.close();
  expect(dump, 'store が保存されていること (control)').not.toBeNull();

  // 2) tasks を上限まで膨らませて注入
  const parsed = JSON.parse(dump.v);
  const template = parsed.appsData.tasks[0];
  parsed.appsData.tasks = Array.from({ length: 500 }, (_, i) =>
    Object.assign({}, template, { id: 'cap' + i, title: 'CAP-' + i }));
  const ctx = await browser.newContext();
  await ctx.addInitScript(([k, v]) => localStorage.setItem(k, v), [dump.k, JSON.stringify(parsed)]);
  const page = await ctx.newPage();
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  // control: 実際に上限へ達していること (達していなければ以下は何も検査しない)
  await expect(page.locator('article.bg-surface')).toHaveCount(500);

  await input.fill('CAP-KEEP-MY-TEXT');
  await input.press('Enter');
  await expect(page.locator('#toast-container')).toContainText('500 件までです');
  // 本題: 断られたのだから、打った文字は残っている
  await expect(input).toHaveValue('CAP-KEEP-MY-TEXT');
  await ctx.close();
});

// 上限に達していない通常時は従来どおり **同期で** 消える (#1061 の二重登録ガードが生きている)。
// 上の test と対で、「常に復元する」実装を落とすための片割れ。
//
// **同期で読むのが要点**。`press('Enter')` のあと await して読むと、非同期の再描画が入力欄を
// 作り直して空にするので、**常に復元する実装でも緑になる** (最初にそう書いて実測で気付いた)。
// キーリピートは再描画を待たずに次の keydown が来る現象なので、検査もその窓で行う。
test('Task input is cleared synchronously when the add succeeds (key-repeat guard intact)', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  const valueRightAfterEnter = await page.evaluate(() => {
    const el = document.getElementById('task-input');
    el.value = 'CAP-CLEARED-ON-SUCCESS';
    el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
    return el.value;   // 再描画を挟まない同じ tick で読む
  });
  expect(valueRightAfterEnter).toBe('');
  // control: 実際に追加されている (Enter 経路そのものが死んでいない)
  await expect(page.getByText('CAP-CLEARED-ON-SUCCESS')).toBeVisible();
});

// [DATA] 貼り付けで消えた分を黙らせない。maxlength は**打鍵なら「入らなくなる」ことが見える**が、
//   **貼り付けは無反応で切られる**。実測 (2026-08-26): タスク入力へ 500 文字を貼ると 200 文字だけ
//   残り、300 文字が通知ゼロで消えた。既定動作は妨げず、**報告だけ**を足す。
//   合成 ClipboardEvent は既定の挿入を行わない (信頼されたイベントでないため) が、リスナーは
//   clipboardData を読んで判定するので、**報告の有無**はこの形で正しく測れる。
test('上限を超える貼り付けは、消えた文字数を通知する', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  const input = page.locator('#task-input');
  await expect(input).toBeVisible();

  // control: 通知領域が最初は空であること。これが無いと、前の操作の残留を拾っても緑になる。
  expect(await page.evaluate(() =>
    (document.getElementById('action-announcement') || {}).textContent),
  'control: 通知領域が最初から埋まっていると、この検査は何も測っていない').toBe('');

  await input.click();
  await page.evaluate((t) => {
    const el = document.getElementById('task-input');
    const dt = new DataTransfer();
    dt.setData('text/plain', t);
    el.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  }, 'X'.repeat(500));

  // TASK_TITLE = 200 なので 300 文字が入らない
  await expect(page.locator('#action-announcement')).toContainText('300 文字');
  await expect(page.locator('#action-announcement')).toContainText('上限 200 文字');
});

// 上限内の貼り付けでは黙っていること。**失っていないのに警告を出すと、本物の警告が信用されなくなる**
//   (#1187 で同じ理由から過剰報告を取り消している)。
test('上限内の貼り付けでは何も言わない', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  const input = page.locator('#task-input');
  await expect(input).toBeVisible();
  await input.click();
  await page.evaluate((t) => {
    const el = document.getElementById('task-input');
    const dt = new DataTransfer();
    dt.setData('text/plain', t);
    el.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  }, 'Y'.repeat(50));
  await page.waitForTimeout(200);
  expect(await page.evaluate(() =>
    (document.getElementById('action-announcement') || {}).textContent),
  '失っていないのに警告を出している').toBe('');
});
