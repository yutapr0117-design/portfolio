const { test, expect } = require('@playwright/test');


// ===== 7.2: クイズ検索フィルタ + 空状態 Behavior Check =====
// #/quiz の検索 input (aria-label='問題検索') は oninput で .quiz-question-block を絞り込み、
// 一致ゼロのとき .panel-empty (aria-live=polite) の「見つかりませんでした」を表示する。
// 検索クリアで全件復帰する。Projects 検索 (focus 維持) とは別ページ・別データセットの
// フィルタ + 空状態契約で従来 e2e 未カバーだった。
test('Quiz search filters question blocks and shows empty state on no match', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  const blocks = page.locator('.quiz-question-block');
  await expect(blocks.first()).toBeVisible(); // [FIX] SPA 描画完了を auto-wait してから数える (snapshot count flake 防止)
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


// ===== 7.2: 設計判断問題集 (?type=architecture) の構造化レンダリング分岐 =====
// QuizPage は quizType=architecture のとき isArchitecture 分岐で intro banner + 状況/
// ステークホルダー主張/問の構造化ゾーン (.quiz-stakeholder-quote / .quiz-question-prompt) を
// 描画する (他 3 種 aws/pm/quality とは別 code path)。既存 quiz テストは default(aws) の検索
// のみ見ており、この distinct な構造化分岐は未カバーだった。?type= query 経由のルーティング
// (router の queryPart 解析) + architecture 専用 DOM の描画を実検証する。
test('Quiz architecture type renders structured stakeholder/question zones (?type query)', async ({ page }) => {
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');

  // タイトルが architecture 用に切り替わる (QUIZ_DATA_MAP lookup)
  await expect(page.locator('h1', { hasText: '設計判断問題集' })).toBeVisible();

  // architecture 専用の構造化ゾーンが描画される
  await expect(page.locator('.quiz-stakeholder-quote').first()).toBeVisible();
  await expect(page.locator('.quiz-question-prompt').first()).toBeVisible();
  await expect(page.locator('.quiz-question-block').first()).toBeVisible();

  // ErrorBoundary に落ちていない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `architecture quiz render caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: architecture quiz 検索が stakeholder 主張テキストを被覆する (回帰) =====
// architecture quiz は stakeholder の name/quote を画面描画するが、検索フィルタが従来
// title/id/content/situation/question しか見ておらず「画面に見えるのに検索できない」状態
// だった (visible-but-unsearchable バグ)。'GAFA' は architecture データ全体で CTO の quote に
// 1 度だけ出る stakeholder-only 語。検索でその問題ブロックがヒットし empty-state にならない
// ことを実検証する (修正前は 0 件 + panel-empty 表示だった)。
test('Quiz architecture search matches stakeholder quote text (visible-but-unsearchable regression)', async ({ page }) => {
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');

  const blocks = page.locator('.quiz-question-block');
  await expect(blocks.first()).toBeVisible();

  // stakeholder quote にのみ存在する語で検索
  const search = page.locator('input[aria-label="問題検索"]');
  await expect(search).toBeVisible();
  await search.fill('GAFA');

  // 該当問題がヒットし、空状態にならない (修正前はここで 0 件 + panel-empty だった)
  await expect(blocks).toHaveCount(1);
  await expect(page.locator('.panel-empty')).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `architecture quiz stakeholder search caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: quiz 検索が section 見出し (章タイトル) テキストを被覆する (回帰) =====
// quiz は各 section の章タイトル (例「第4章：可用性とFinOps（コスト）の天秤」) を section header
// として画面描画するが、検索フィルタ _filterBy は per-question フィールド (title/id/content/
// situation/question/stakeholder) しか見ておらず section 名を対象外にしていた。タイトルにのみ
// 含まれる topic 語で検索すると「見えるのに 0 件」になる (#285 の stakeholder と同 class)。
// 'FinOps' は architecture データ全体で第4章タイトルに 1 度だけ出る section-only 語。検索でその章が
// ヒットし empty-state にならないことを実検証する (修正前は 0 件 + panel-empty 表示だった)。
test('Quiz search matches section-header (chapter title) text (visible-but-unsearchable regression)', async ({ page }) => {
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');

  const blocks = page.locator('.quiz-question-block');
  await expect(blocks.first()).toBeVisible();

  // section 章タイトルにのみ存在する語で検索
  const search = page.locator('input[aria-label="問題検索"]');
  await expect(search).toBeVisible();
  await search.fill('FinOps');

  // 該当章がヒットし、空状態にならない (修正前はここで 0 件 + panel-empty だった)
  await expect(page.locator('.quiz-section-title', { hasText: 'FinOps' })).toBeVisible();
  await expect(blocks.first()).toBeVisible();
  await expect(page.locator('.panel-empty')).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quiz section-header search caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: quiz 模範解答問い合わせフォームの空入力バリデーション =====
// QuizPage の問い合わせフォームは送信時に name/email 必須を検証し、欠落時「お名前とメール
// アドレスを入力してください」エラー toast を出す (mailto は開かない)。この validation 分岐は
// 未カバーだった。空のまま送信 → エラー toast + crash なしを実検証する。
test('Quiz contact form shows validation error on empty submit', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  // 名前/メール未入力で送信
  await page.getByRole('button', { name: '送信' }).click();
  await expect(page.locator('#toast-container').getByText('お名前とメールアドレスを入力してください')).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quiz form validation caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: quiz 検索語が reload を跨いで復元される (producer/consumer normalize drift 回帰) =====
// QuizPage は検索語を State.updateSilently(s => s.appsData.quizSearch = val) で localStorage へ
// 永続化書き込みし、init で state.appsData.quizSearch を読み戻して復元する (docstring「永続化された
// 検索語を反映」)。しかし store.js normalizeAppsData は tasks/todos/pomodoro/ai/notes を preserve
// するのに quizSearch だけ preserve せず、reload 時の load()→validateAndNormalize が毎回 "" に捨てて
// いた (書き込みは永続化されるのに読み戻しが normalize で strip される半配線)。fill→debounce flush→
// reload で検索語 input の value が復元されることを実検証する (修正前はここで空だった＝非 vacuous)。
test('Quiz search term persists across reload (normalize preserve regression)', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  const search = page.locator('input[aria-label="問題検索"]');
  await expect(search).toBeVisible();

  // 検索語を入力 → updateSilently が scheduleSave(DEBOUNCE_DELAY=150ms) で localStorage へ永続化
  await search.fill('EC2');
  await expect(search).toHaveValue('EC2');
  await page.waitForTimeout(300); // debounce(150ms) flush を待って localStorage への書き込みを確定させる

  // reload: load()→validateAndNormalize→normalizeAppsData を通る (quizSearch の読み戻し経路)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');

  // 修正前は normalizeAppsData が quizSearch を drop し input が空になっていた。修正後は復元される。
  const search2 = page.locator('input[aria-label="問題検索"]');
  await expect(search2).toBeVisible();
  await expect(search2).toHaveValue('EC2');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quiz search restore caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: quiz pm / quality タイプのデータファイル描画カバレッジ =====
// QUIZ_DATA_MAP は aws / pm / quality / architecture の 4 データファイルを引く。aws(default) と
// architecture は被覆済みだが、pm(pmQuizData) / quality(qualityQuizData) はどのテストでも未訪問で
// 0 カバレッジ = malformed でも未検知だった。?type= 経由で両者の title + question block 描画を検証し
// 2 データファイルの renderability を守る (distinct data ゆえ非 padding)。
test('Quiz pm and quality types render their data files', async ({ page }) => {
  await page.goto('/#/quiz?type=pm');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1', { hasText: 'PM問題集' })).toBeVisible();
  await expect(page.locator('.quiz-question-block').first()).toBeVisible();

  await page.goto('/#/quiz?type=quality');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1', { hasText: '品質・プロセス問題集' })).toBeVisible();
  await expect(page.locator('.quiz-question-block').first()).toBeVisible();
});
