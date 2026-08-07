const { test, expect } = require('@playwright/test');


// ===== 7.2: ポモドーロのモード切替→タイマー表示更新 Behavior Check =====
// #/apps/pomodoro は集中/短休憩/長休憩ボタンで switchMode() → State 更新 + remaining を新モードの
// duration へリセットし、`.font-mono.text-stat` の MM:SS 表示が変わる。timer の tick に依存しない
// 非 flaky な対話 (mode 切替は即時)。apps 5 種 (task/todo/settings/ai/pomodoro) の対話カバレッジ完成。
test('Pomodoro mode switch resets and updates the timer display', async ({ page }) => {
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();
  const initial = (await timer.textContent()).trim();

  // 既定 (集中) から短休憩へ切替 → remaining が短休憩 duration にリセットされ表示が変化
  await page.getByRole('button', { name: '短休憩', exact: true }).click();
  await expect(timer).not.toHaveText(initial);
});


// ===== 7.2: ポモドーロ 長休憩モード (3 つ目の mode 分岐 / settings.long duration) =====
// switchMode('long-break') は getDuration で settings.long(既定 15)*60 を remaining にセットする。
// mode-switch テストは短休憩のみで、長休憩は distinct な 3 つ目の mode 分岐として未カバーだった。
// 「長休憩」クリックで表示が既定の長休憩 duration 15:00 になることを検証する。
test('Pomodoro long-break mode sets the long-break duration', async ({ page }) => {
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  await page.getByRole('button', { name: '長休憩', exact: true }).click();
  await expect(page.locator('.font-mono.text-stat').first()).toHaveText('15:00');
});


// ===== 7.2: ポモドーロの開始→カウントダウン→一時停止 Behavior Check (page.clock で決定的) =====
// timer は endAtMs (Date.now() ベース) で remaining を算出する。page.clock で時刻を決定的に進め、
// 開始でカウントダウンが進み、一時停止で停止することを flaky なしに検証する (mode 切替テストが
// 即時遷移のみだったのに対し、本テストは時間経過を伴う中核ロジックをカバー)。
test('Pomodoro start counts down and pause halts it (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();
  const t0 = (await timer.textContent()).trim();

  // 開始 → 3 秒進める → カウントダウンが進む
  await page.getByRole('button', { name: '開始' }).click();
  await page.clock.fastForward(3000);
  await expect(timer).not.toHaveText(t0);

  // 一時停止 → さらに進めても表示は変化しない (停止)
  await page.getByRole('button', { name: '一時停止' }).click();
  const tPaused = (await timer.textContent()).trim();
  await page.clock.fastForward(3000);
  await expect(timer).toHaveText(tPaused);
});


// ===== 7.2: ポモドーロ reset ボタン (満了値へ復帰 + 停止) =====
// reset() は stopTimer + remainingSec をモード duration へ戻す。switchMode (モード切替) や complete
// (0 到達) とは別経路で、稼働中の「リセット」ボタン押下は未カバーだった。開始→進める→リセットで
// 満了値に戻り、以降 clock を進めても変化しない (= 停止) ことを fake clock で決定的に検証する。
test('Pomodoro reset button restores full duration and stops (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();
  const full = (await timer.textContent()).trim();

  // 開始 → 5 秒進める → カウントダウン
  await page.getByRole('button', { name: '開始' }).click();
  await page.clock.fastForward(5000);
  await expect(timer).not.toHaveText(full);

  // リセット → 満了値へ復帰 + 「開始」へ戻る (停止)
  await page.getByRole('button', { name: 'リセット' }).click();
  await expect(timer).toHaveText(full);
  await expect(page.getByRole('button', { name: '開始' })).toBeVisible();

  // 停止後は clock を進めても変化しない
  await page.clock.fastForward(5000);
  await expect(timer).toHaveText(full);
});


// ===== 7.2: ポモドーロのセッション完了 (0 到達 → complete: history 記録 + リセット) =====
// start/pause テスト (#上) はカウントダウン継続/停止を見るが、タイマーが 0 に到達する complete()
// 経路 (setInterval 内の remaining<=0 分岐) は未テストだった。complete は history へ push し
// 「セッション完了！」toast を出して runtime を満了状態 (isActive=false / remainingSec=duration)
// に戻す。集中時間を 1 分に設定し fake clock で 0 到達まで進め、完了通知 + 「開始」へ戻る (停止) +
// 満了表示への復帰を決定的に検証する。集中→0 という apps の自動完了サイクルの保証。
// ===== 7.2: ポモドーロ稼働中の reload で interval が resume する (frozen 回帰) =====
// pomodoroTimer は createApps factory 変数ゆえ reload で null に戻るが、runtime.isActive は
// endAtMs>now なら normalize が保持する。startTimer は start() ボタンからのみ呼ばれ auto-resume が
// 無かったため、reload 後は「一時停止表示 (isActive=true) だが countdown が frozen で complete() が
// 永遠に発火しない」stuck 状態だった。PomodoroPage render 時に isActive かつ interval 不在なら
// resume する fix の回帰検知。reload 後に clock を進めても表示が更新される (=resume) ことを検証。
test('Pomodoro resumes ticking after a reload mid-run (frozen-timer guard)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();

  // 開始 → 稼働中 (一時停止ボタン表示)
  await page.getByRole('button', { name: '開始' }).click();
  await page.clock.fastForward(2000);
  await expect(page.getByRole('button', { name: '一時停止' })).toBeVisible();

  // リロード: state は isActive=true で復元されるが interval は失われる
  await page.clock.install();
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  // isActive が保持され「一時停止」表示 (稼働中扱い)
  await expect(page.getByRole('button', { name: '一時停止' })).toBeVisible();

  // clock を進める → resume していれば表示が更新される (frozen なら不変で fail)
  const tReload = (await timer.textContent()).trim();
  await page.clock.fastForward(3000);
  await expect(timer).not.toHaveText(tReload);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `pomodoro resume caused a fatal: ${fatal}`).toBeNull();
});


test('Pomodoro completes at zero: shows done toast and resets to full duration (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  // 集中時間を 1 分に短縮 (onchange は blur で発火) → 満了まで 60 秒に
  const workInput = page.getByLabel('集中時間（分）');
  await workInput.fill('1');
  await workInput.blur();

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toHaveText('01:00');

  // 開始 → 61 秒進めて 0 到達 → complete()
  await page.getByRole('button', { name: '開始' }).click();
  await page.clock.fastForward(61000);

  // 完了通知が出る
  await expect(page.locator('#toast-container').getByText('セッション完了！')).toBeVisible();
  // runtime が満了状態へ戻る: 「一時停止」ではなく「開始」が再表示 (isActive=false)
  await expect(page.getByRole('button', { name: '開始' })).toBeVisible();
  // 表示は満了 duration (01:00) に復帰
  await expect(timer).toHaveText('01:00');
  // ErrorBoundary に落ちていない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `pomodoro completion caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: 稼働中に集中時間を変更 → 完了時のリセットが新しい設定値を使う (stale-closure 修正) =====
// getDuration も getRemaining と同じく render 毎キャプチャの closure `pomo` を読んでいたため、
// タイマー稼働中 (interval は start() 時の closure に固定) に集中時間を変更すると、完了時の
// remainingSec リセットが古い設定値になるバグがあった (getDuration を live state 参照に修正)。
// work=1 で開始→稼働中に work=2 へ変更→満了、で完了後の表示が新しい 02:00 になることを検証する。
test('Pomodoro completion uses the latest focus-duration setting changed mid-run', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const workInput = page.getByLabel('集中時間（分）');
  await workInput.fill('1');
  await workInput.blur();
  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toHaveText('01:00');

  // 開始 (work=1 の endAtMs で稼働)
  await page.getByRole('button', { name: '開始' }).click();

  // 稼働中に集中時間を 2 分へ変更 (active なので remainingSec/endAtMs は据え置き=稼働継続)
  await workInput.fill('2');
  await workInput.blur();

  // 満了まで進める → complete() の duration リセットは最新設定 (2 分) を使うべき
  await page.clock.fastForward(61000);
  await expect(page.locator('#toast-container').getByText('セッション完了！')).toBeVisible();
  await expect(page.getByRole('button', { name: '開始' })).toBeVisible();
  // 修正前は stale 設定で 01:00 に戻っていた。修正後は最新の 02:00。
  await expect(timer).toHaveText('02:00');
});


// ===== 7.2: 休憩モードで idle 中に休憩時間を変更 → 表示が即更新される (work との対称性回帰) =====
// 設定 onchange は work だけ「idle かつ mode 一致なら remainingSec を即更新」していたが short/long は
// 欠落しており、短休憩/長休憩モードで idle 中に設定を変えても表示が古い duration のまま (start すると
// 旧設定長で始まる) 非対称バグだった。短休憩モードで short を 10 分に変更し、表示が 05:00→10:00 へ即
// 更新されることを検証する (修正前は 05:00 のままで fail＝非 vacuous)。work の live-update と対称化。
test('Pomodoro break-duration change updates the idle timer display (symmetry with focus)', async ({ page }) => {
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();

  // 短休憩モードへ (idle・既定 short=5 → 05:00)
  await page.getByRole('button', { name: '短休憩', exact: true }).click();
  await expect(timer).toHaveText('05:00');

  // idle 中に短休憩時間を 10 分へ変更 → 表示が即 10:00 に更新される (修正前は 05:00 のまま)
  const shortInput = page.getByLabel('短休憩時間（分）');
  await shortInput.fill('10');
  await shortInput.blur();
  await expect(timer).toHaveText('10:00');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `pomodoro break-duration change caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.2: 稼働中のモード切替 → タイマー停止 + 新モード duration へリセット =====
// 既存 mode-switch テストは idle 起点のみで、「稼働中に別モードへ切替」パスが未カバーだった。
// switchMode() は isActive=false + remainingSec=新モード duration を live state に書き、稼働中の
// タイマーを停止して新モードの満了値へリセットする (getRemaining は live state を読むため、
// isActive=false になると countdown ではなく静的 remainingSec を返す)。もし switchMode が
// isActive=false を落とすと、切替後もタイマーが「稼働中」表示 (一時停止ボタン) のまま残り、
// 新モードの countdown が走る running-timer-with-wrong-mode 退行になる (mutation: isActive=false→true
// で本テストが RED = 非 vacuous を実証済)。開始→3秒進める→短休憩へ切替で (a) 表示が短休憩満了
// 05:00 にリセット、(b) 開始ボタンに戻る (停止)、(c) さらに時間を進めても 05:00 のまま (停止) を
// fake clock で決定的に検証する。
test('Pomodoro switching mode while running stops the timer and resets (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toHaveText('25:00'); // 既定 集中

  // 開始 → 稼働中 (一時停止ボタンが出る) → 3 秒進めてカウントダウン確認
  await page.getByRole('button', { name: '開始' }).click();
  await expect(page.getByRole('button', { name: '一時停止' })).toBeVisible();
  await page.clock.fastForward(3000);
  await expect(timer).not.toHaveText('25:00');

  // 稼働中に「短休憩」へ切替 → 停止 + 05:00 リセット
  await page.getByRole('button', { name: '短休憩', exact: true }).click();
  await expect(timer).toHaveText('05:00');                                  // (a) 新モード満了へリセット
  await expect(page.getByRole('button', { name: '開始' })).toBeVisible();   // (b) 停止 (開始ボタンに戻る)
  await expect(page.getByRole('button', { name: '一時停止' })).toHaveCount(0);

  // (c) 停止しているので時間を進めても 05:00 のまま (旧 interval が生き残っていないこと)
  await page.clock.fastForward(5000);
  await expect(timer).toHaveText('05:00');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `mode switch while running caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: ポモドーロ remainingSec=0 の ingestion round-trip fidelity =====
// store.js normalizeAppsData の `Number(rt.remainingSec) || DEFAULT` は 0 が falsy ゆえ、valid な
// remainingSec=0 (pause-at-zero / 完了直前の export・snapshot・cross-tab 由来) を DEFAULT(1500=25:00)
// に化けさせる round-trip fidelity 欠陥だった。remainingSec=0・isActive=false の永続 store を seed して
// リロード相当で読ませ、タイマーが 00:00 のまま復元される (25:00 に化けない) ことを検証する。
// 修正を戻すと 25:00 が表示され本 test が RED = 非 vacuous。
test('Pomodoro restores a persisted remainingSec of 0 as 00:00 (ingestion does not clobber a valid zero)', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
      schemaVersion: 12,
      type: 'full-store',
      appsData: {
        pomodoro: {
          settings: { work: 25, short: 5, long: 15 },
          runtime: { isActive: false, mode: 'work', endAtMs: null, remainingSec: 0 },
          history: []
        }
      }
    }));
  });

  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();
  await expect(timer).toHaveText('00:00');   // 修正前は Number(0)||DEFAULT → 25:00 に化ける

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `restoring remainingSec=0 caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: pomodoro 非デフォルト settings が reload を跨いで永続する (settings normalize round-trip) =====
// 集中/短休憩/長休憩時間の number input (onchange → settings.work/short/long) で設定した非デフォルト値が
// localStorage → load → normalizeAppsData (`work: clamp(Number(...) || DEFAULT, 1, 180)` 等) の round-trip
// を跨いで保持されることを検証する。既存 pomodoro テスト (mode 切替 / countdown / reset / interval-resume)
// は非デフォルト settings 値の reload 永続を検証しない。normalize の settings 行を `work: DEFAULT.work` 等へ
// regress するとユーザの custom 設定が reload 後に既定へ silent に戻るのに素通りする (#294/#568/#684/#796/
// #797/#798 = normalize が reload で field を drop/default する同 class)。非デフォルト work=40 を設定→reload→
// 保持を検証しこの穴を塞ぐ。
test('Pomodoro non-default settings persist across reload (settings normalize round-trip)', async ({ page }) => {
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('domcontentloaded');

  const workInput = page.getByLabel('集中時間（分）');
  await expect(workInput).toBeVisible();
  // 既定 25 から非デフォルト 40 へ変更 (onchange → settings.work → State.update → scheduleSave)
  await workInput.fill('40');
  await workInput.blur();
  await expect(workInput).toHaveValue('40');

  // reload (visibilitychange → saveNow で flush) → load → normalizeAppsData を跨いで work=40 保持
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByLabel('集中時間（分）')).toHaveValue('40');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `pomodoro settings reload persist caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: ポモドーロ タイマー表示の SR アクセシビリティ (role=timer + 文脈的 aria-label) =====
// カウントダウン表示は視覚的に毎秒更新されるだけで、従来 role/aria-label が無く SR ユーザーには
// 素の数字 "25:00" が何のタイマーか (残り時間か) 不明だった (WCAG 1.3.1)。role="timer" (暗黙
// aria-live=off ゆえ毎秒アナウンスしない非 chatty) + mode/残り時間を人間可読にした aria-label を付与。
// 本テストは (1) timer role が存在, (2) aria-label が mode(集中) と「残り」を含む, (3) mode 切替で
// aria-label が追従する, を検証する (role/aria-label を外すと RED = 非 vacuous)。
test('Pomodoro countdown exposes role=timer with a contextual aria-label for screen readers', async ({ page }) => {
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });

  const timer = page.getByRole('timer');
  await expect(timer).toBeVisible();
  // 既定 mode=work(集中)。aria-label は「集中 残り N分M秒」形式で文脈を与える。
  await expect(timer).toHaveAttribute('aria-label', /集中.*残り.*分.*秒/);

  // mode を短休憩へ切替 → aria-label が追従する (素の数字では表現できない状態を SR へ露出)。
  await page.getByRole('button', { name: '短休憩' }).click();
  await expect(page.getByRole('timer')).toHaveAttribute('aria-label', /短休憩.*残り.*分.*秒/);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `pomodoro timer a11y caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.3: モード切替ボタンの選択状態 SR 露出 (aria-pressed) =====
// 集中/短休憩/長休憩 の 3 ボタンは選択中モードを btn-primary の色(C5 視覚)のみで示しており、
// SR ユーザーには現在どのモードが選択中か露出されなかった (WCAG 4.1.2 Name/Role/Value)。
// 各ボタンに aria-pressed を付与し選択状態を AT へ露出する。本テストは (1) 既定で集中=true・
// 他=false, (2) 短休憩クリックで選択が追従し集中=false/短休憩=true, を検証する
// (aria-pressed を外すと選択ボタンの pressed 状態が消え RED = 非 vacuous)。
test('Pomodoro mode buttons expose selected state via aria-pressed', async ({ page }) => {
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });

  // 既定 mode=work(集中): 集中=pressed, 他は非 pressed。
  await expect(page.getByRole('button', { name: '集中' })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByRole('button', { name: '短休憩' })).toHaveAttribute('aria-pressed', 'false');
  await expect(page.getByRole('button', { name: '長休憩' })).toHaveAttribute('aria-pressed', 'false');

  // 短休憩へ切替 → 選択状態が追従する。
  await page.getByRole('button', { name: '短休憩' }).click();
  await expect(page.getByRole('button', { name: '短休憩' })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByRole('button', { name: '集中' })).toHaveAttribute('aria-pressed', 'false');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `pomodoro mode aria-pressed caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.1: pomodoro 集中時間 input の範囲外入力が clamp される (境界) =====
// work 設定 onchange は clamp(parseInt(v)||25, 1, 180) で範囲外を丸める。既存テストは非デフォルト
// 有効値(40)の reload 永続は見るが、範囲外入力の clamp 境界(上限 180 / 下限 1)は未カバーだった。
// number input の max=180 属性は programmatic/paste の範囲外値を防がないため JS clamp が実防御で、
// これが外れると 999 分などの不正 duration が設定され timer が壊れる。上限超過→180・下限未満→1 を検証。
test('Pomodoro focus-duration input clamps out-of-range values to [1,180]', async ({ page }) => {
  await page.goto('/#/apps/pomodoro', { waitUntil: 'domcontentloaded' });
  const work = page.getByLabel('集中時間（分）');
  await expect(work).toBeVisible();

  // 上限超過 999 → 180 に clamp される (onchange は blur で発火)。
  await work.fill('999');
  await work.blur();
  await expect(work).toHaveValue('180');

  // 下限未満 -5 → 1 に clamp される (parseInt('-5')=-5 は truthy ゆえ || 25 を通らず clamp(−5,1,180)=1)。
  await work.fill('-5');
  await work.blur();
  await expect(work).toHaveValue('1');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `pomodoro clamp caused a fatal: ${fatal}`).toBeNull();
});
