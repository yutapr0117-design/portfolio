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
