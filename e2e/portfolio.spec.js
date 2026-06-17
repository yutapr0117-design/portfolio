// e2e/portfolio.spec.js
// Extracted from .github/workflows/playwright-regression.yml (P2: Playwright file-based consolidation)
// Do NOT embed this file in workflow heredocs — both regression and snapshot workflows reference it directly.

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const path = require('path');
const fs   = require('fs');

// Detect whether a screenshot baseline exists for the current platform.
// Playwright stores snapshots under e2e/<spec>-snapshots/<name>-<browser>-<platform>.png
function baselineExists(name) {
  const snapshotDir = path.join(__dirname, 'portfolio.spec.js-snapshots');
  if (!fs.existsSync(snapshotDir)) return false;
  const files = fs.readdirSync(snapshotDir);
  return files.some(f => f.startsWith(name));
}

// Detect baseline-generation mode (set by update-playwright-snapshots.yml).
// In this mode the screenshot test MUST run even when no baseline exists yet,
// otherwise `--update-snapshots` would have nothing to capture and the baseline
// could never be generated (the original skip-guard deadlock — P0-01).
function isSnapshotUpdateMode() {
  return process.env.PLAYWRIGHT_UPDATE_SNAPSHOTS === '1';
}

// ===== 7.1: AIO Anchor 可視化バグ検知 =====
test('AIO asset anchor must be hidden (non-visual)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  const anchor = page.locator('#aio-asset-anchor');
  await expect(anchor).toHaveCount(1);
  // 視覚的に非表示であることを確認（attributeがhiddenである）
  await expect(anchor).toHaveAttribute('hidden', '');
  // boundingBoxがnull（非表示）であることをアサート
  const box = await anchor.boundingBox();
  expect(box).toBeNull();
});

// ===== 7.1: ホームページ初期レンダリング =====
test('Homepage renders without console errors', async ({ page }) => {
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') { errors.push(msg.text()); }
  });
  page.on('pageerror', err => errors.push(err.message));

  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // Fatal エラーがないことを確認
  const fatalOverlay = page.locator('#portfolio-safety-net-host');
  await expect(fatalOverlay).toHaveCount(0);

  // h1 が表示されていることを確認
  const h1 = page.locator('h1, .h1').first();
  await expect(h1).toBeVisible();

  // 致命的コンソールエラーがないことをアサート
  const fatalErrors = errors.filter(e =>
    !e.includes('non-fatal') &&
    !e.includes('View Transition') &&
    !e.includes('SW')
  );
  expect(fatalErrors, 'Fatal console errors: ' + JSON.stringify(fatalErrors)).toHaveLength(0);
});

// ===== 7.2: ハッシュルーティング状態遷移 Behavior Check =====
test('Hash routing transitions correctly between routes', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // Projects ページへ遷移
  await page.goto('/#/projects');
  await page.waitForLoadState('networkidle');
  // #content が表示されており aria-busy が false に戻っていること
  const content = page.locator('#content');
  await expect(content).toBeVisible();
  await expect(content).toHaveAttribute('aria-busy', 'false');

  // ホームへ戻る
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  // .hero-section が表示されること
  const hero = page.locator('.hero-section');
  await expect(hero).toBeVisible();
});

// ===== 7.2: aria-busy 状態遷移 Behavior Check =====
test('content div transitions aria-busy correctly during navigation', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const content = page.locator('#content');
  await expect(content).toHaveAttribute('aria-busy', 'false');

  await page.goto('/#/projects');
  await page.waitForLoadState('networkidle');
  await expect(content).toHaveAttribute('aria-busy', 'false');
});

// ===== 7.2: prefers-reduced-motion でのナビゲーション (WCAG 2.3.3 / 前庭安全) =====
// main.js は prefers-reduced-motion: reduce のとき View Transition を完全スキップする専用経路を
// 持つ (doc b §13.1 二重防衛)。この distinct code path でもナビゲーションが機能し (#content 更新・
// aria-busy 収束)、ErrorBoundary に落ちないことを検証する。動きに敏感なユーザーがアニメ無しでも
// 壊れず操作できることの保証。
test('Navigation works under prefers-reduced-motion (View Transition skipped)', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  await page.goto('/#/projects');
  await page.waitForLoadState('networkidle');
  const content = page.locator('#content');
  await expect(content).toHaveAttribute('aria-busy', 'false');
  await expect(page.locator('h1', { hasText: 'プロジェクト一覧' })).toBeVisible();

  // 別ルートへもう一度遷移しても reduced-motion 経路で正常更新
  await page.goto('/#/about');
  await page.waitForLoadState('networkidle');
  await expect(content).toHaveAttribute('aria-busy', 'false');
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `reduced-motion navigation caused a fatal: ${fatal}`).toBeNull();
});

// ===== 7.1: スクリーンショット差分テスト（ベースライン）=====
// Regression runs: skipped when no baseline image exists (prevents constant-failure on first run).
// Baseline-generation runs (PLAYWRIGHT_UPDATE_SNAPSHOTS=1 via update-playwright-snapshots.yml):
//   the test runs even without a baseline so `--update-snapshots` can capture it. (P0-01)
// Run update-playwright-snapshots.yml to generate the baseline, then commit the .png files.
test('Homepage screenshot regression', async ({ page }) => {
  if (!baselineExists('homepage-baseline') && !isSnapshotUpdateMode()) {
    test.skip(true, 'No screenshot baseline found. Run update-playwright-snapshots workflow to generate.');
  }
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(500); // アニメーション安定待ち
  await expect(page).toHaveScreenshot('homepage-baseline.png', {
    fullPage: false,
    clip: { x: 0, y: 0, width: 1280, height: 720 }
  });
});

// ===== 7.2: Projects 検索フォーカス維持 Behavior Check =====
test('Projects search input retains focus during filtering', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('networkidle');

  const searchInput = page.locator('input[type="text"]').first();
  await searchInput.click();
  await searchInput.type('AI', { delay: 50 });

  // 検索後もフォーカスが維持されていること（バグ: v52以前はフォーカス喪失していた）
  await expect(searchInput).toBeFocused();
});

// ===== 7.1: モバイルビューポートでのCLS検証 =====
test('No layout shift on mobile viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // topbar がmobileで表示されていること
  const topbar = page.locator('.topbar');
  await expect(topbar).toBeVisible();

  // サイドバーがmobileで非表示であること
  const sidebar = page.locator('.sidebar');
  await expect(sidebar).not.toBeVisible();
});

// ===== 7.2: テーマ切替の永続化 Behavior Check =====
// theme toggle (#themeBtnTop) は data-theme を cycle (system→dark→light→system) させ、
// State 経由で localStorage に永続化する。リロードを跨いだ往復 (theme-init.js の FOUC
// pre-paint → main.js Theme.init の再適用) が壊れていないことを検証する。Check 100 が
// FOUC pre-paint の storage キー一致を静的強制するのに対し、本テストは実ブラウザでの
// 切替→永続→復元の振る舞いを動的に保証する。
test('Theme toggle cycles data-theme and persists across reload', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const html = page.locator('html');
  const initial = await html.getAttribute('data-theme');

  // テーマ切替ボタンは desktop (sidebar) と mobile (#themeBtnTop) の両方に存在し同じ
  // aria-label を共有する。viewport で可視な方を選んでクリックする。
  const themeBtn = page.locator('button[aria-label="ライトモードとダークモードを切り替える"]:visible').first();
  await expect(themeBtn).toBeVisible();
  await themeBtn.click();

  const afterClick = await html.getAttribute('data-theme');
  expect(afterClick, 'data-theme must change after toggling the theme button').not.toBe(initial);

  // リロード後もテーマが永続化されていること（State → localStorage 往復）
  await page.reload();
  await page.waitForLoadState('networkidle');
  const afterReload = await page.locator('html').getAttribute('data-theme');
  expect(afterReload, 'theme selection must persist across a page reload').toBe(afterClick);
});

// ===== 7.2: モバイルドロワーの開閉 + ARIA + Escape + focus 復帰 Behavior Check =====
// mobile (≤MOBILE_BREAKPOINT=920px) では sidebar が #menuBtn → #drawer (role=dialog,
// aria-modal) に畳まれる。開くと aria-expanded=true / drawer aria-hidden=false / 背景 #app が
// inert+aria-hidden で隔離され、Escape で閉じて focus が #menuBtn に復帰する。これは
// accessibility 上重要な focus-trap / background-isolation 契約だが従来 e2e 未カバーだった。
test('Mobile drawer opens with ARIA, isolates background, and closes on Escape', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const menuBtn = page.locator('#menuBtn');
  const drawer = page.locator('#drawer');
  await expect(menuBtn).toBeVisible();
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');

  // 開く: ARIA 状態と背景隔離
  await menuBtn.click();
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'true');
  await expect(drawer).toHaveAttribute('aria-hidden', 'false');
  await expect(drawer).toBeVisible();
  await expect(page.locator('#app')).toHaveAttribute('aria-hidden', 'true');

  // Escape で閉じる: ARIA 復元 + focus が menuBtn へ復帰
  await page.keyboard.press('Escape');
  await expect(menuBtn).toHaveAttribute('aria-expanded', 'false');
  await expect(drawer).toHaveAttribute('aria-hidden', 'true');
  await expect(page.locator('#app')).not.toHaveAttribute('aria-hidden', 'true');
  await expect(menuBtn).toBeFocused();
});

// ===== 7.2: クイズ検索フィルタ + 空状態 Behavior Check =====
// #/quiz の検索 input (aria-label='問題検索') は oninput で .quiz-question-block を絞り込み、
// 一致ゼロのとき .panel-empty (aria-live=polite) の「見つかりませんでした」を表示する。
// 検索クリアで全件復帰する。Projects 検索 (focus 維持) とは別ページ・別データセットの
// フィルタ + 空状態契約で従来 e2e 未カバーだった。
test('Quiz search filters question blocks and shows empty state on no match', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('networkidle');

  const blocks = page.locator('.quiz-question-block');
  const initial = await blocks.count();
  expect(initial, 'quiz should render question blocks initially').toBeGreaterThan(0);

  const search = page.locator('input[aria-label="問題検索"]');
  await expect(search).toBeVisible();

  // 一致しない検索 → 空状態 + ブロック 0
  await search.fill('zzz-no-such-question-xyz');
  await expect(page.locator('.panel-empty')).toBeVisible();
  await expect(blocks).toHaveCount(0);

  // クリアで全件復帰
  await search.fill('');
  await expect(blocks).toHaveCount(initial);
});

// ===== 7.2: タスク管理アプリの追加 + リロード永続化 Behavior Check =====
// #/apps/task は #task-input に入力 → Enter で State.update 経由でタスクを追加し、
// localStorage (State auto-save) へ永続化する。apps セクションは従来「ルートが描画される」
// テストのみで、実際のデータ操作 (add → 永続 → reload で復元) は未カバーだった。State の
// Proxy 永続パスを実ブラウザで動的検証する (theme/drawer/quiz に続く interactive coverage)。
test('Task app adds a task and persists it across reload', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('networkidle');

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
  await page.waitForLoadState('networkidle');
  await expect(page.getByText(title)).toBeVisible();
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
  await page.waitForLoadState('networkidle');

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
  await tabA.waitForLoadState('networkidle');
  await tabB.goto('/#/apps/task');
  await tabB.waitForLoadState('networkidle');

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

// ===== 7.2: TODO アプリの追加→完了トグル→一括削除フロー Behavior Check =====
// #/apps/todo は TodoPage (task とは別 factory / 別 State slice) で、addTodo (Enter) /
// toggleTodo (checkbox) / clearCompleted (「完了済み削除」一括操作) という distinct な
// コードパスを持つ。task テスト (#91) が add+persist を見るのに対し、本テストは toggle と
// bulk 削除という別 operation class を実ブラウザで動的検証する。
test('Todo app add, complete-toggle, then clear-completed removes the item', async ({ page }) => {
  await page.goto('/#/apps/todo');
  await page.waitForLoadState('networkidle');

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
  await page.waitForLoadState('networkidle');
  await expect(page.getByText(text)).toHaveCount(0);
});

// ===== 7.2: 設定アプリのデータエクスポート整合性 Behavior Check =====
// #/settings の「フルバックアップ」は downloadJSON(State.get()) で blob を生成し
// portfolio_full_<ts>.json として download する (data-integrity 機能)。CRUD とは別系統の
// 「State 全体を妥当な JSON として書き出せるか」を、Playwright の download イベントで動的検証。
test('Settings app exports a full backup as a valid JSON download', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('networkidle');

  const exportBtn = page.getByRole('button', { name: 'フルバックアップ' });
  await expect(exportBtn).toBeVisible();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    exportBtn.click(),
  ]);
  expect(download.suggestedFilename()).toMatch(/^portfolio_full_\d+\.json$/);

  // ダウンロード本体が State の妥当な JSON であること
  const content = fs.readFileSync(await download.path(), 'utf8');
  const parsed = JSON.parse(content);
  expect(parsed, 'export must contain the appsData State slice').toHaveProperty('appsData');
});

// ===== 7.2: 設定アプリのスナップショット保存→反映 Behavior Check =====
// #/settings の「保存」は setSnapshot() で Storage.set(SNAPSHOT_KEY, ...) し、再描画後に
// getSnapshot()(=Storage.parse) が読み戻して「保存日時: …」を表示する。これは PR #93 で
// 注入漏れを修正した Storage 依存 (set/parse) の往復を実際に通す data-integrity パスで、
// 修正前は Storage.parse が render 時に throw して到達すらできなかった経路。
test('Settings app saves a snapshot and reflects the saved-at status', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('networkidle');

  // 初期 (fresh context) は未保存
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();

  // 保存 → Storage.set → 再描画 → getSnapshot(Storage.parse) が読み戻し「保存日時:」表示
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByText(/保存日時:/)).toBeVisible();

  // リロード後も Storage から読み戻せる (永続)
  await page.reload();
  await page.waitForLoadState('networkidle');
  await expect(page.getByText(/保存日時:/)).toBeVisible();
});

// ===== 7.2: AI アシストアプリの応答生成 Behavior Check =====
// #/apps/ai は #ai-input + 「送信」で submit() → analyzeInput → (300ms 後) generateResponse +
// State.update で appsData.ai.history に push し再描画する。task/todo とは別 State slice・別ロジック
// (ローカル生成・非同期 setTimeout) の distinct な対話パス。送信した prompt が履歴に現れることで
// submit→生成→State 反映→render の一連が壊れていないことを動的検証する。
test('AI assist app generates and renders a response for a prompt', async ({ page }) => {
  await page.goto('/#/apps/ai');
  await page.waitForLoadState('networkidle');

  const input = page.locator('#ai-input');
  await expect(input).toBeVisible();
  const prompt = 'E2E-AI-PROMPT-デプロイ手順-5512';
  await input.fill(prompt);
  await page.getByRole('button', { name: '送信', exact: true }).click();

  // 生成完了後、prompt が history (テキスト) として描画される (input value ではなく本文)
  await expect(page.getByText(prompt)).toBeVisible();
});

// ===== 7.2: ポモドーロのモード切替→タイマー表示更新 Behavior Check =====
// #/apps/pomodoro は集中/短休憩/長休憩ボタンで switchMode() → State 更新 + remaining を新モードの
// duration へリセットし、`.font-mono.text-stat` の MM:SS 表示が変わる。timer の tick に依存しない
// 非 flaky な対話 (mode 切替は即時)。apps 5 種 (task/todo/settings/ai/pomodoro) の対話カバレッジ完成。
test('Pomodoro mode switch resets and updates the timer display', async ({ page }) => {
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('networkidle');

  const timer = page.locator('.font-mono.text-stat').first();
  await expect(timer).toBeVisible();
  const initial = (await timer.textContent()).trim();

  // 既定 (集中) から短休憩へ切替 → remaining が短休憩 duration にリセットされ表示が変化
  await page.getByRole('button', { name: '短休憩', exact: true }).click();
  await expect(timer).not.toHaveText(initial);
});

// ===== 7.2: ポモドーロの開始→カウントダウン→一時停止 Behavior Check (page.clock で決定的) =====
// timer は endAtMs (Date.now() ベース) で remaining を算出する。page.clock で時刻を決定的に進め、
// 開始でカウントダウンが進み、一時停止で停止することを flaky なしに検証する (mode 切替テストが
// 即時遷移のみだったのに対し、本テストは時間経過を伴う中核ロジックをカバー)。
test('Pomodoro start counts down and pause halts it (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('networkidle');

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

// ===== 7.2: ポモドーロのセッション完了 (0 到達 → complete: history 記録 + リセット) =====
// start/pause テスト (#上) はカウントダウン継続/停止を見るが、タイマーが 0 に到達する complete()
// 経路 (setInterval 内の remaining<=0 分岐) は未テストだった。complete は history へ push し
// 「セッション完了！」toast を出して runtime を満了状態 (isActive=false / remainingSec=duration)
// に戻す。集中時間を 1 分に設定し fake clock で 0 到達まで進め、完了通知 + 「開始」へ戻る (停止) +
// 満了表示への復帰を決定的に検証する。集中→0 という apps の自動完了サイクルの保証。
test('Pomodoro completes at zero: shows done toast and resets to full duration (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/pomodoro');
  await page.waitForLoadState('networkidle');

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

// ===== 7.2: skip link が main コンテンツへ focus を移す (WCAG 2.4.1 Bypass Blocks) =====
// `<a href="#main-content" class="skip-link">` はキーボード利用者がナビを飛ばして本文へ直接
// 到達する手段。focus → Enter で focus が #main-content (tabindex=-1) へ移ることを検証する。
// また hash routing (#/...) と競合して NotFound に落ちたり focus が移らない退行も同時に防ぐ。
test('Skip link moves focus to #main-content without breaking routing (WCAG 2.4.1)', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const skip = page.locator('.skip-link');
  await skip.focus();
  await expect(skip).toBeFocused();

  await skip.press('Enter');
  // focus が #main-content へ移り、NotFoundPage に落ちていないこと
  await expect(page.locator('#main-content')).toBeFocused();
  await expect(page.getByRole('heading', { name: 'Not Found', exact: true })).toHaveCount(0);
});

// ===== 7.1: 壊れた localStorage からの graceful 復帰 (resilience) =====
// 永続データ (localStorage) が破損 JSON でも、Storage.parse の try/catch + Store.load の default
// fallback でアプリは crash せず既定状態で描画を継続すべき (fail-open)。破損値を仕込んで load し、
// FatalPage / NotFound に落ちず home が正常描画されることを検証する。設定画面 crash バグ (#93) で
// 「render 時クラッシュは致命的」と分かったため、永続層破損というもう一つの入力境界も固定する。
test('App recovers gracefully from corrupt localStorage (no FatalPage)', async ({ page }) => {
  await page.addInitScript(() => {
    try {
      localStorage.setItem('portfolio_enhanced_v45', 'not-valid-json-%%%');
      localStorage.setItem('portfolio_brand_v45', 'garbage-not-json');
    } catch (e) { /* noop */ }
  });
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(200);

  // ErrorBoundary の FatalPage に落ちていない (window.__fatalError が falsy)
  const fatal = await page.evaluate(() => {
    const e = window.__fatalError;
    return e ? (e.message || String(e)) : null;
  });
  expect(fatal, `corrupt storage caused a fatal render: ${fatal}`).toBeNull();
  // home が正常描画され NotFound でもない
  await expect(page.locator('.hero-section')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Not Found', exact: true })).toHaveCount(0);
});

// ===== 7.1: 設定インポートの不正 JSON 耐障害性 (graceful error) =====
// settings の importJSON は FileReader + JSON.parse を try/catch で囲み、不正ファイルでも crash
// せず「JSONのパースに失敗しました」エラー Toast を出す (fail-soft)。不正 JSON ファイルを与え、
// エラー Toast 表示 + FatalPage に落ちないことを検証する (もう一つの入力境界 = ファイルアップロード)。
test('Settings import shows an error for malformed JSON file without crashing', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('networkidle');

  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles({
    name: 'broken.json',
    mimeType: 'application/json',
    buffer: Buffer.from('this is definitely not valid json ###'),
  });

  // 不正 JSON → エラー Toast 表示・crash しない（エラーは #toast-container と sr-only aria-live の
  // 両方に出る = 視覚 + screen reader 両対応。toast 側を検証する）。
  await expect(page.locator('#toast-container').getByText('JSONのパースに失敗しました')).toBeVisible();
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `malformed import caused a fatal render: ${fatal}`).toBeNull();
});

// ===== 7.1: axe-core 自動アクセシビリティ監査 — render-neutral critical 回帰防止 =====
// axe-core で WCAG 2a/2aa/21a/21aa を全主要ルートでスキャンし、render-neutral に修正可能な
// critical 違反群がゼロであることを機械強制する。本 increment で是正したバグの回帰防止:
//   - aria-valid-attr-value: aria-details が `#id`（IDREF 不正）かつ dangling だった全ルート critical
//   - select-name / button-name / label: settings/task/todo の form-control に accessible name が
//     無かった critical（aria-label を付与して是正）
// これらは ARIA 属性 / accessible name の付与のみで pixel 不変ゆえ §3 baseline ゲート非該当。
// 注: color-contrast / link-in-text-block 等の render（CSS）系違反は baseline ゲート下で別途扱う
// ため本テストでは対象外（render-neutral に直せる違反のみを今は機械強制する）。
const A11Y_ROUTES = ['#/', '#/projects', '#/about', '#/contact', '#/resume', '#/apps', '#/settings', '#/quiz', '#/apps/task', '#/apps/todo', '#/apps/pomodoro', '#/apps/ai', '#/hiring-risk', '#/ai-knowhow', '#/role-split', '#/not-found'];
// 本テストで違反ゼロを機械強制する rule の allowlist（= 既に render-neutral に修正済の rule）。
// color-contrast / color-contrast-enhanced / heading-order / link-in-text-block 等の未修正
// （baseline-gated or 別 increment）rule は analyze 結果に含まれても本 allowlist 外ゆえ無視する。
const A11Y_RENDER_NEUTRAL_RULES = ['aria-valid-attr-value', 'select-name', 'button-name', 'label', 'page-has-heading-one', 'heading-order'];
for (const route of A11Y_ROUTES) {
  test(`a11y axe: ${route} has no render-neutral critical violations`, async ({ page }) => {
    await page.goto(`/${route}`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(150);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'])
      .analyze();
    const offenders = results.violations.filter(v => A11Y_RENDER_NEUTRAL_RULES.includes(v.id));
    expect(
      offenders,
      `Route ${route} render-neutral a11y violations: ` +
      JSON.stringify(offenders.map(v => `${v.id}(${v.nodes.length}): ${v.nodes[0] && v.nodes[0].html.slice(0, 100)}`))
    ).toHaveLength(0);
  });
}

// ===== 7.1: モバイル viewport + drawer 開 (モーダル) の a11y =====
// 上の A11Y_ROUTES ループは default(desktop) viewport で走る。モバイル (≤MOBILE_BREAKPOINT) は
// sidebar が #drawer (role=dialog/aria-modal) に畳まれる別レンダリング面で、特に drawer 開状態は
// モーダルの a11y (背景隔離・focusable な dialog 内容) が desktop scan ではカバーされない。
// 390px で drawer を開いた状態の render-neutral critical 違反ゼロを機械強制する。
test('a11y axe: mobile viewport with open drawer has no render-neutral critical violations', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  await page.locator('#menuBtn').click();
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'false');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'])
    .analyze();
  const offenders = results.violations.filter(v => A11Y_RENDER_NEUTRAL_RULES.includes(v.id));
  expect(
    offenders,
    'mobile+drawer render-neutral a11y violations: ' +
    JSON.stringify(offenders.map(v => `${v.id}(${v.nodes.length})`))
  ).toHaveLength(0);
});

// ===== 7.2: 全ハッシュルート検証 — aria-busy 収束 & コンテンツ非空 =====
// 注: 以前は '#/home'（home は '#/'）と '#/skills'（'skills' route は存在しない）が含まれ、
// どちらも NotFoundPage に解決していた。NotFound も aria-busy=false + #content 非空ゆえ、
// この 2 entry の aria-busy テストは vacuous に NotFound を検査していた（PR #96/#97 の
// app-route-hash と同型の vacuous-hash class）。実在 route のみへ是正し、下の guard で再発を防ぐ。
const HASH_ROUTES = ['#/', '#/projects', '#/about', '#/contact', '#/resume'];

for (const route of HASH_ROUTES) {
  test(`Hash route ${route}: aria-busy resolves to false and #content is non-empty`, async ({ page }) => {
    await page.goto(`/${route}`);
    await page.waitForLoadState('networkidle');

    const content = page.locator('#content');

    await page.waitForFunction(
      () => {
        const el = document.getElementById('content');
        return el && el.getAttribute('aria-busy') === 'false';
      },
      { timeout: 5000 }
    );

    await expect(content).toHaveAttribute('aria-busy', 'false');

    const isEmpty = await page.evaluate(() => {
      const el = document.getElementById('content');
      return el ? el.children.length === 0 : true;
    });
    expect(isEmpty, `#content must not be empty on route ${route}`).toBe(false);

    // Hash-resolution guard (vacuous-hash 再発防止): これらは実在 route のみゆえ、NotFoundPage
    // に落ちてはならない。aria-busy=false + 非空は NotFound でも満たされるため、本 guard が無いと
    // 誤った hash (例: '#/home' / '#/skills') を足しても vacuous に pass してしまう。
    await expect(
      page.getByRole('heading', { name: 'Not Found', exact: true }),
      `Hash route ${route} fell through to NotFoundPage — not a real route`
    ).toHaveCount(0);
  });
}

// ===== 7.2: 5層防衛プロキシ — startViewTransition 上書き確認 =====
test('5-layer proxy: document.startViewTransition is overridden by proxy', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const proxyInstalled = await page.evaluate(() => {
    if (typeof document.startViewTransition !== 'function') {
      return true;
    }
    return document.startViewTransition.name === 'startViewTransitionProxy';
  });

  expect(
    proxyInstalled,
    'document.startViewTransition must be replaced by startViewTransitionProxy'
  ).toBe(true);
});

// ===== 7.2: 5層防衛プロキシ — window.addEventListener 直接上書き禁止確認 =====
test('5-layer proxy: window.addEventListener is not directly overwritten', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const isConsistent = await page.evaluate(() => {
    return !Object.prototype.hasOwnProperty.call(window, 'addEventListener');
  });

  expect(
    isConsistent,
    'window.addEventListener must not be directly overwritten; use EventTarget.prototype instead'
  ).toBe(true);
});

// ===== 7.1: AIOアンカー永続性 — ページ読み込み後も DOM に存在すること =====
test('AIO anchor persists in DOM after initial load', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const count = await page.locator('#aio-asset-anchor').count();
  expect(count, '#aio-asset-anchor must exist in DOM').toBe(1);

  await expect(page.locator('#aio-asset-anchor')).toHaveAttribute('hidden', '');
});

// ===== 7.1: AIOアンカー永続性 — ルート遷移後も保持されること =====
test('AIO anchor persists in DOM after route navigation', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  await page.goto('/#/about');
  await page.waitForLoadState('networkidle');

  const count = await page.locator('#aio-asset-anchor').count();
  expect(count, '#aio-asset-anchor must persist after route navigation').toBe(1);
  await expect(page.locator('#aio-asset-anchor')).toHaveAttribute('hidden', '');
});

// ===== 7.2: early suppressor — unhandledrejection リスナーの動作確認 =====
test('Early suppressor: unhandledrejection listener suppresses known patterns', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const wasSuppressed = await page.evaluate(() => {
    const err = new Error('message channel closed before a response was received');
    const event = new PromiseRejectionEvent('unhandledrejection', {
      promise: Promise.reject(err),
      reason: err,
      cancelable: true,
    });
    window.dispatchEvent(event);
    return event.defaultPrevented;
  });

  expect(
    wasSuppressed,
    'Early suppressor must call ev.preventDefault() for known extension error patterns'
  ).toBe(true);
});

// ===== 7.1: Trusted Types / CSP 違反なし確認 =====
test('No Trusted Types or CSP violations in console', async ({ page }) => {
  const violations = [];

  page.on('console', msg => {
    const text = msg.text();
    if (
      msg.type() === 'error' &&
      /TrustedType|Trusted Types|require-trusted-types-for|Content Security Policy|CSP/i.test(text)
    ) {
      violations.push({ type: 'console-error', text });
    }
  });

  page.on('pageerror', err => {
    if (/TrustedType|Trusted Types|require-trusted-types-for/i.test(err.message)) {
      violations.push({ type: 'pageerror', text: err.message });
    }
  });

  await page.goto('/');
  await page.waitForLoadState('networkidle');

  expect(
    violations,
    'Trusted Types / CSP violations found: ' + JSON.stringify(violations)
  ).toHaveLength(0);
});

// ===== v80+ Stage 5-k CI hygiene: all-routes runtime sanity =====
// Stage 5-j で発見された "hidden ReferenceError" (js/pages.js の `h` 未定義参照) は、
// Playwright が当該ルート (/#/hiring-risk, /#/role-split, /#/not-found) を訪問
// していなかったため CI 緑のまま潜在していた。本テスト群は SPA の全 17 ルートを
// 訪問して各ページの runtime 健全性 (console-error / pageerror なし + DOM 出力存在)
// を検証する。これにより同種の bug を将来的に発火前検出可能にする。
//
// 各ルートに対して個別 test() を生成し、失敗しても他ルートは独立に検査される。
// screenshot baseline は引き続き Homepage のみ (他ルートは behavior テストに留め
// baseline の re-take 負荷を避ける)。
const ALL_ROUTES = [
  { hash: '#/',                  name: 'home' },
  { hash: '#/projects',          name: 'projects' },
  { hash: '#/apps',              name: 'apps' },
  { hash: '#/apps/task',         name: 'app-task' },
  { hash: '#/apps/todo',         name: 'app-todo' },
  { hash: '#/apps/pomodoro',     name: 'app-pomodoro' },
  { hash: '#/apps/ai',           name: 'app-ai' },
  { hash: '#/settings',          name: 'settings' },
  { hash: '#/about',             name: 'about' },
  { hash: '#/resume',            name: 'resume' },
  { hash: '#/contact',           name: 'contact' },
  { hash: '#/quiz',              name: 'quiz' },
  { hash: '#/hiring-risk',       name: 'hiring-risk' },
  { hash: '#/ai-knowhow',        name: 'ai-knowhow' },
  { hash: '#/role-split',        name: 'role-split' },
  { hash: '#/not-found',         name: 'not-found-fallback' },
];

for (const route of ALL_ROUTES) {
  test(`Route ${route.name} renders without runtime errors`, async ({ page }) => {
    const consoleErrors = [];
    const pageErrors = [];

    page.on('console', msg => {
      if (msg.type() === 'error') {
        const text = msg.text();
        // Allow benign KARTE/Wicle / suppressor-known patterns and pre-existing
        // inline-style CSP advisories that pre-date Stage 5 (role-split has legacy
        // `style: {...}` chains that Object.assign(el.style, ...) emits as
        // "Applying inline style violates CSP" advisories in some Chromium builds;
        // these are advisories, not blocked execution, and pre-date this PR scope).
        if (/KARTE|Wicle|wicle|Failed to fetch|Trusted Type|Applying inline style violates/i.test(text)) { return; }
        // External-resource load failures (e.g. KARTE CDN flaking in CI) surface as
        // "Failed to load resource: net::ERR_FAILED" — note Chromium puts the FAILED URL in
        // msg.location().url, NOT in msg.text(), so the host-name filter above cannot see it.
        // Ignore such network errors only when the failing URL is a *non-self* origin: a failed
        // OWN module/asset would instead throw a pageerror AND leave #content empty (both asserted
        // below), so this never masks a real same-origin regression — it only de-flakes third-party
        // CDN failures that are outside our code's control.
        const _loc = (typeof msg.location === 'function') ? msg.location() : null;
        const _url = (_loc && _loc.url) || '';
        if (/Failed to load resource|net::ERR_/i.test(text) && _url && !/^https?:\/\/(localhost|127\.0\.0\.1)/i.test(_url)) { return; }
        consoleErrors.push(text);
      }
    });
    page.on('pageerror', err => pageErrors.push(err.message));

    await page.goto('/' + route.hash);
    await page.waitForLoadState('networkidle');
    // Wait an extra tick to let the SPA finish its render cycle
    await page.waitForTimeout(200);

    // SPA must have rendered content
    const contentLocator = page.locator('#content');
    await expect(contentLocator).toHaveCount(1);
    const contentText = await contentLocator.textContent();
    expect(contentText, `Route ${route.name} content div is empty — likely render threw`).not.toBe('');

    // No console errors (other than benign third-party patterns)
    expect(
      consoleErrors,
      `Route ${route.name} console errors: ` + JSON.stringify(consoleErrors)
    ).toHaveLength(0);

    // No uncaught page errors (ReferenceError / TypeError 等)
    expect(
      pageErrors,
      `Route ${route.name} page errors: ` + JSON.stringify(pageErrors)
    ).toHaveLength(0);

    // No CAUGHT render crash (ErrorBoundary → FatalPage). main.js stores the thrown
    // error on window.__fatalError before rendering FatalPage. A route that crashes into
    // FatalPage would otherwise PASS the three checks above — #content is non-empty (it
    // holds the fatal UI) and the error was caught (so no console/page error). This is
    // exactly how the SettingsPage Storage-injection bug hid undetected. Asserting
    // window.__fatalError is falsy closes that detection gap for every shipped route.
    const fatal = await page.evaluate(() => {
      const e = window.__fatalError;
      return e ? (e.message || String(e)) : null;
    });
    expect(fatal, `Route ${route.name} fell into the ErrorBoundary FatalPage: ${fatal}`).toBeNull();

    // Hash-resolution guard: every route EXCEPT the intentional not-found fallback must
    // resolve to its real page, never silently fall through to NotFoundPage (h1 "Not Found").
    // This catches the "wrong hash → NotFound" vacuous-coverage class — e.g. ALL_ROUTES once
    // listed #/app-task instead of #/apps/task, so 4 app route tests vacuously asserted the
    // NotFound page (non-empty + no error) and passed. Check 58 only compares route NAMES,
    // not that each hash resolves, so this behavioral guard closes that gap.
    if (route.name !== 'not-found-fallback') {
      await expect(
        page.getByRole('heading', { name: 'Not Found', exact: true }),
        `Route ${route.name} (${route.hash}) fell through to NotFoundPage — its hash does not resolve to the intended route`
      ).toHaveCount(0);
    }
  });
}

// ===== v80+ Stage 5-k CI hygiene: project-detail route requires slug =====
test('Route project-detail renders for a known slug without errors', async ({ page }) => {
  const consoleErrors = [];
  const pageErrors = [];

  page.on('console', msg => {
    if (msg.type() === 'error') {
      const text = msg.text();
      if (/KARTE|Wicle|wicle|Failed to fetch|Trusted Type|Applying inline style violates/i.test(text)) { return; }
      consoleErrors.push(text);
    }
  });
  page.on('pageerror', err => pageErrors.push(err.message));

  // p01 = task-manager (Store の defaultProjects 先頭)。
  // 注: route は複数形 '#/projects/<slug>' で project-detail に解決する。以前は単数 '#/project/...'
  // を使っており NotFoundPage に落ちて vacuous に NotFound を検査していた（PR #96-#98 と同型の
  // vacuous-hash class）。複数形へ是正し、実プロジェクト描画を直接アサートする。
  await page.goto('/#/projects/task-manager');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(200);

  const contentLocator = page.locator('#content');
  const contentText = await contentLocator.textContent();
  expect(contentText, 'project-detail content empty').not.toBe('');
  expect(consoleErrors).toHaveLength(0);
  expect(pageErrors).toHaveLength(0);

  // NotFound fall-through ではなく実 ProjectDetailPage が描画されていること
  await expect(page.getByRole('heading', { name: 'Not Found', exact: true })).toHaveCount(0);
  await expect(page.getByText('タスク管理アプリ')).toBeVisible();
});