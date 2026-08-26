const { test, expect } = require('@playwright/test');

// ポモドーロと**他アプリの相互作用**に関する behavior。apps-pomodoro.spec.js が advisory
// 行数を超えたため、テーマの塊としてここへ切り出した (advisory は BLOCKING の手前で効かせる)。
// 扱うのは「全リセットが同時に生きている複数の状態をまとめて初期化するか」「裏で走るタイマーが
// 別アプリの未送信入力を壊さないか」「取り込み・別タブ・リロードが稼働中の runtime をどう扱うか」。

// ===== 全リセットは「同時に生きている 3 つの状態」をまとめて初期化する =====
// 下の test は **ポモドーロ単体**を見る。だが実際の利用者は複数のアプリに同時に状態を持つ ——
// タイマーが走り、quiz の検索語が永続化され (#684)、ノートに未送信の本文がある、という具合。
// 「全リセット」はその**全部**を初期化する契約で、どれか 1 つでも取り残すと
// 「初期化したのに前の状態が残っている」という一貫性の破れになる。
//
// とくに **稼働中タイマーの interval** は state だけ戻して interval を止め損ねると
// **幽霊 tick** が残り、リセット後の表示が勝手に動く。state と runtime の両方を見る。
test('Full reset clears pomodoro / quiz search / notes together (multi-app state)', async ({ page }) => {
  // 3 つの状態を同時に作る
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '開始' }).click();

  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');
  await page.getByLabel('問題検索').fill('EC2');

  await page.goto('/#/apps/notes');
  await page.waitForLoadState('domcontentloaded');
  await page.locator('#notes-input').fill('未送信のメモ本文');

  const read = () => page.evaluate(() => {
    const k = Object.keys(localStorage).find((x) => x.includes('portfolio'));
    const d = JSON.parse(localStorage.getItem(k) || '{}');
    return {
      active: !!(((d.appsData || {}).pomodoro || {}).runtime || {}).isActive,
      quizSearch: (d.appsData || {}).quizSearch || '',
      notes: (d.appsData || {}).notes || '',   // notes は文字列そのもの (実測: .text ではない)
    };
  });

  // control: 3 つとも実際に立っていること (立っていなければ「消えたか」を検証できない)
  await expect.poll(async () => (await read()).active,
    { message: 'control: タイマーが稼働していない' }).toBe(true);
  await expect.poll(async () => (await read()).quizSearch,
    { message: 'control: quiz 検索語が永続化されていない' }).toContain('EC2');
  await expect.poll(async () => (await read()).notes,
    { message: 'control: ノート本文が永続化されていない' }).toContain('未送信のメモ本文');

  page.on('dialog', (d) => d.accept());
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '全リセット' }).click();
  await expect(page.locator('#toast-container')).toContainText('初期化');

  // 3 つとも既定へ戻る
  await expect.poll(async () => (await read()).active,
    { message: '全リセット後もタイマーが稼働中のまま' }).toBe(false);
  await expect.poll(async () => (await read()).quizSearch,
    { message: '全リセット後も quiz 検索語が残っている' }).toBe('');
  expect((await read()).notes,
    '全リセット後も未送信のノート本文が残っている').not.toContain('未送信のメモ本文');

  // 幽霊 tick が残っていない (state を戻しても interval を止め損ねると表示が動く)
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');
  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();
  const t0 = (await timer.textContent()).trim();
  await page.waitForTimeout(2500);
  expect((await timer.textContent()).trim(),
    'リセット後もタイマーが動いている = interval が止まっていない (幽霊 tick)').toBe(t0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `multi-app reset caused a fatal: ${fatal}`).toBeNull();
});


test('Full reset stops a running pomodoro timer (cross-app interaction)', async ({ page }) => {
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(e.message));

  // (1) タイマーを実際に開始し、永続化された runtime が isActive であることを確認する
  //     (ここが false なら以降は「止まっているものを止める」検査になり vacuous)
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();
  await page.getByRole('button', { name: '開始' }).first().click();
  await expect.poll(async () => page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('portfolio_enhanced_v45')).appsData.pomodoro.runtime.isActive; } catch (e) { return null; }
  }), { message: 'タイマーが開始されていない — 以降の検査が vacuous になる' }).toBe(true);

  // (2) 別アプリ (settings) から全リセット
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();
  page.once('dialog', (d) => d.accept());
  await page.getByRole('button', { name: '全リセット' }).click();
  await expect(page.locator('#toast-container')).toContainText('初期化しました');

  // (3) 永続化された runtime が停止していること
  await expect.poll(async () => page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('portfolio_enhanced_v45')).appsData.pomodoro.runtime.isActive; } catch (e) { return 'ERR'; }
  }), { message: '全リセット後も runtime.isActive が true のまま (走り続けた interval が初期化を上書きしうる)' }).toBe(false);

  // (4) ポモドーロへ戻ると停止状態の UI (「開始」ボタン) が出る
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();
  await expect(
    page.getByRole('button', { name: '開始' }).first(),
    'リセット後も「一時停止」のまま = UI と state が乖離している'
  ).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `cross-app reset caused a fatal: ${fatal}`).toBeNull();
  expect(pageErrors, `cross-app reset raised page errors: ${JSON.stringify(pageErrors.slice(0, 2))}`).toHaveLength(0);
});


// ===== 裏で走るタイマーの完了が、別のアプリで入力中のテキストを消さない =====
// ポモドーロのタイマーは**別のアプリを開いていても走り続ける**。完了処理は State.update →
// notify → #content の全再描画を起こすため、従来は **利用者が何も操作していないのに**
// 別ページの未送信入力が消えていた (実測: タスク名 'POMO-DRAFT-KEEP' → "")。
// 自分の操作が引き金でない分、#982 (テーマ切替) や #1055 (絞り込み) より驚きが大きい。
// 表示中だけ再描画し、それ以外は updateSilently で state と保存だけ進める形へ是正した。
//
// 3 秒後に完了する runtime を seed して待つ (実時間。時計を偽装すると State/描画の
// タイミングまで変わってしまい、測りたい「裏で完了したとき」の再現にならない)。
test('裏でタイマーが完了しても別アプリの未送信入力が消えない', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
      schemaVersion: 12, type: 'full-store',
      appsData: {
        pomodoro: {
          history: [], settings: { work: 25, short: 5, long: 15 },
          runtime: { isActive: true, mode: 'work', endAtMs: Date.now() + 3000, remainingSec: 3, linkedTaskId: null }
        }
      }
    }));
  });

  // control 1: 稼働中の runtime が実際に採用されている (採用されていなければ完了が来ない)
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('[role="timer"]')).toBeVisible();

  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();

  const draft = 'POMO-COMPLETE-DRAFT-8801';
  await page.locator('#task-input').fill(draft);

  // 完了を跨ぐまで待つ (localStorage の isActive が false になったら完了済み)
  await expect.poll(async () => page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('portfolio_enhanced_v45')).appsData.pomodoro.runtime.isActive; }
    catch { return null; }
  }), { timeout: 15000 }).toBe(false);

  // control 2: 完了処理が実際に走った (履歴が 1 件増えている)
  expect(await page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('portfolio_enhanced_v45')).appsData.pomodoro.history.length; }
    catch { return -1; }
  }), 'control: 完了処理が走っていなければ、この経路を測れない').toBe(1);

  await expect(page.locator('#task-input'),
    '裏のタイマー完了に巻き込まれて未送信の入力が消えている').toHaveValue(draft);
});


// ===== 稼働中タイマーの復帰はルートに依存しない =====
// 従来 auto-resume は PomodoroPage() の**描画中にしか走らなかった**ため、リロード後に
// 別ページにいると interval が誰にも作られず、集中し続けても完了が記録されなかった。
// 実測 (修正前): 別ページ着地 history=0 / isActive=true のまま・ポモドーロ画面着地
// history=1 / isActive=false。リロードしなければ裏で完了する (#1056 が扱ったのがその経路)
// ので、**リロードを跨いだときだけ**挙動が違う非対称だった。
//
// 測定の作り方:
//   - 1 ケース 1 コンテキスト。同じページで localStorage を書き換えて reload すると、
//     直前の描画が仕込んだ debounce 保存が後から書き戻して seed を潰す (実測で 1 度踏んだ)。
//   - 期限は **未来** に置く。期限切れの runtime は store.js の normalize が isActive=false へ
//     落とすので (観測していないセッションを credit しない設計)、過去に置くと何も検査しない。
//   - reload 直後の localStorage は **保存済みバイト列**であって正規化後の state ではない。
//     ここでは「完了が history へ書かれたか」を見るので、書き込みが起きた事実そのものが signal。
const POMO_KEY = 'portfolio_enhanced_v45';

async function pomodoroRunningSnapshot(browser) {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto('/#/apps/pomodoro');
  await expect(page.locator('#content h1')).toBeVisible();
  await page.getByRole('button', { name: '開始' }).click();
  await expect.poll(() => page.evaluate((k) => !!localStorage.getItem(k), POMO_KEY)).toBe(true);
  await page.waitForTimeout(1200);   // debounce 保存を落ち着かせてから読む
  const raw = await page.evaluate((k) => localStorage.getItem(k), POMO_KEY);
  await ctx.close();
  return raw;
}

async function pomodoroLandOn(browser, raw, route) {
  const seeded = JSON.parse(raw);
  seeded.appsData.pomodoro.runtime.endAtMs = Date.now() + 6000;
  seeded.appsData.pomodoro.runtime.remainingSec = 6;
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.addInitScript(([k, v]) => { localStorage.setItem(k, v); }, [POMO_KEY, JSON.stringify(seeded)]);
  await page.goto(route);
  await expect(page.locator('#content h1').first()).toBeVisible();
  const result = await page.evaluate(async ([k]) => {
    const deadline = Date.now() + 14000;
    while (Date.now() < deadline) {
      const st = JSON.parse(localStorage.getItem(k));
      if ((st.appsData.pomodoro.history || []).length > 0) {
        return { hist: st.appsData.pomodoro.history.length, active: st.appsData.pomodoro.runtime.isActive };
      }
      await new Promise((r) => setTimeout(r, 300));
    }
    const st = JSON.parse(localStorage.getItem(k));
    return { hist: (st.appsData.pomodoro.history || []).length, active: st.appsData.pomodoro.runtime.isActive };
  }, [POMO_KEY]);
  await ctx.close();
  return result;
}

test('稼働中ポモドーロはリロード後どのページに着地しても完了が記録される', async ({ browser }) => {
  const raw = await pomodoroRunningSnapshot(browser);
  // control: そもそも「稼働中」の状態を捕まえられているか (isActive でなければ以降は何も検査しない)
  expect(JSON.parse(raw).appsData.pomodoro.runtime.isActive,
    'control: 開始直後の state が稼働中になっていない').toBe(true);

  const onRoute = await pomodoroLandOn(browser, raw, '/#/apps/pomodoro');
  expect(onRoute.hist, 'ポモドーロ画面に着地したのに完了が記録されない').toBe(1);

  const offRoute = await pomodoroLandOn(browser, raw, '/#/apps/task');
  expect(offRoute.hist,
    '別ページに着地すると完了が記録されない — resume が描画に紐付いており、'
    + 'リロードを跨ぐと集中し続けても記録されない (init から resumeIfActive を呼ぶこと)').toBe(1);
  expect(offRoute.active, '完了後も稼働中のまま残っている').toBe(false);
});

// ===== 稼働中のポモドーロ × 取り込み (cross-app・モード別の意味論) =====
// #1183 で取り込みモードが appsData にも効くようになり、**稼働状態の扱いがモード依存**に
// なった。ここが壊れると症状は #121/#134 と同じ class —— 「ボタンの表示と state が desync」
// あるいは「置き換えたのに古い interval が動き続ける」で、どちらも利用者からは
// 「止めたのに進む / 動いているのに止まっている」としか見えない。
//
// 追加のみ: runtime は既存優先 = **稼働は続く**
// 全置換  : runtime も置き換わる = **停止し、古い interval も残らない**
async function startPomodoroThenImport(page, mode) {
  // 全置換は confirm を通す (#1331)。既定の dismiss だと取り込みが起きない (詳細は import-shape spec)。
  if (mode === 'strict') { page.once('dialog', d => d.accept()); }
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('.font-mono.text-stat').first()).toBeVisible();
  await page.getByRole('button', { name: '開始' }).click();
  await expect(page.getByRole('button', { name: '一時停止' })).toBeVisible();

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.locator('#content select').first().evaluate((el, m) => {
    el.focus();
    el.value = m;
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }, mode);
  // モード変更の onchange は window.render() でページを作り直すため、直後の
  // setInputFiles は detach された古い input を掴む。一度ルートを離れて戻る。
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  expect(await page.locator('#content select').first().inputValue(),
    'control: モードが選択されていなければ、その意味論を測れない').toBe(mode);

  await page.setInputFiles('#content input[type="file"]', {
    name: 'pomo.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      tasks: [],
      todos: [],
      pomodoro: {
        history: [],
        settings: { work: 25, short: 5, long: 15 },
        runtime: { isActive: false, mode: 'work', remainingSec: 1500 },
      },
    })),
  });
  await expect(page.locator('#action-announcement')).toContainText('インポート');

  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('.font-mono.text-stat').first()).toBeVisible();
}

test('「追加のみ」の取り込みは稼働中のポモドーロを止めない', async ({ page }) => {
  await startPomodoroThenImport(page, 'append');

  await expect(page.getByRole('button', { name: '一時停止' }),
    '「追加のみ」なのに稼働状態が置き換えられて止まった').toBeVisible();
  // **変化**の検査なので poll が正しい (残り時間が進むこと)
  await expect.poll(async () => await page.locator('.font-mono.text-stat').first().textContent(),
    { timeout: 5000 }).not.toBe('25:00');
});

test('「全置換」の取り込みは稼働中のポモドーロを止め、古い interval も残さない', async ({ page }) => {
  await startPomodoroThenImport(page, 'strict');

  await expect(page.getByRole('button', { name: '開始' }),
    '全置換なのに稼働状態が残っている').toBeVisible();

  // **不変性**の検査なので poll は使わない (poll は最初の観測で成立してしまう)。
  // settle させてから 2 度読み、進んでいないことを見る = 古い interval が生きていない。
  const before = await page.locator('.font-mono.text-stat').first().textContent();
  await page.waitForTimeout(2500);
  const after = await page.locator('.font-mono.text-stat').first().textContent();
  expect(after, '停止したはずなのに古い interval が進めている').toBe(before);
});

// ===== 別タブの更新が稼働中のポモドーロを止めない (cross-tab × cross-app) =====
// cross-tab 採用は受信 store を **丸ごと** 採用する。だが別タブは「未起動」の
// pomodoro runtime を持っているのが普通なので、そのまま採用すると
// **走っているタイマーが黙って止まる**。
// 実測 (2026-08-20): tabA で開始 → tabB でタスクを 1 件足すだけで tabA の isActive が
// false へ戻り、残り時間も進まなくなった。利用者からは「別タブで作業していたら
// ポモドーロが消えていた」としか見えず、原因に見当がつかない。
// #940 (編集中テキストを守る) と同じ「*自タブで進行中のもの* を cross-tab 採用から守る」class。
test('別タブの更新が稼働中のポモドーロを止めない', async ({ browser }) => {
  const ctx = await browser.newContext();
  const tabA = await ctx.newPage();
  await tabA.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  await expect(tabA.locator('.font-mono.text-stat').first()).toBeVisible();
  await tabA.getByRole('button', { name: '開始' }).click();
  await expect(tabA.getByRole('button', { name: '一時停止' })).toBeVisible();

  // 別タブでタスクを追加する = tabA へ storage イベントが届く
  const tabB = await ctx.newPage();
  await tabB.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(tabB.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await tabB.getByLabel('新しいタスクを入力').fill('FROM-TAB-B');
  await tabB.getByLabel('新しいタスクを入力').press('Enter');
  await expect(tabB.locator('#content').getByText('FROM-TAB-B')).toBeVisible();

  await tabA.bringToFront();
  // 稼働が続いている (ボタンが「一時停止」のまま)
  await expect(tabA.getByRole('button', { name: '一時停止' }),
    '別タブの更新で稼働中のポモドーロが止まった').toBeVisible();
  // **変化**の検査なので poll が正しい (残り時間が進むこと)
  await expect.poll(async () => await tabA.locator('.font-mono.text-stat').first().textContent(),
    { timeout: 6000, message: 'タイマーが進んでいない (interval が失われた)' }).not.toBe('25:00');

  // control: 採用自体は壊していない —— 別タブの更新が tabA へ反映されること。
  //   これが無いと「cross-tab 採用を丸ごと止めた」実装でもテストが通ってしまう。
  await tabA.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(tabA.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await expect(tabA.locator('#content').getByText('FROM-TAB-B'),
    'control: 別タブの更新が反映されていない (採用ごと止めてしまっている)').toBeVisible();

  await ctx.close();
});
