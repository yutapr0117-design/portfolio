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

  // WCAG 1.3.5 (Identify Input Purpose): 個人情報 input は autocomplete トークンを持つ
  await expect(page.getByLabel('お名前')).toHaveAttribute('autocomplete', 'name');
  await expect(page.getByLabel('メールアドレス')).toHaveAttribute('autocomplete', 'email');

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


// ===== 7.2: 検索語が quiz 種別を跨いで持ち越されない (空ページ着地の回帰) =====
// quizSearch は単一の文字列で、種別 (aws/pm/quality/architecture) を問わず適用されていた。そのため
// ある種別で検索したまま sidebar / CTA で別の種別へ切り替えると語が持ち越され、切替先が
// 「一致する問題は見つかりませんでした」の**空ページ**になっていた (実測: architecture で 'CAP' →
// PM へ切替で PM が 0 件)。quizSearchType を併せて永続化し種別一致時のみ復元する。
test('Quiz search term does not leak across quiz types (empty-page landing regression)', async ({ page }) => {
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');
  const search = page.locator('input[aria-label="問題検索"]');
  await expect(search).toBeVisible();
  await search.fill('CAP');
  await expect(search).toHaveValue('CAP');
  await page.waitForTimeout(300); // updateSilently の debounce flush

  // 別種別へ切替 → 検索語は持ち越されず、問題が描画される (空ページにならない)
  await page.goto('/#/quiz?type=pm');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1')).toHaveText('PM問題集');
  await expect(page.locator('input[aria-label="問題検索"]')).toHaveValue('');
  await expect(page.getByText(/一致する問題は見つかりませんでした/)).toHaveCount(0);

  // 元の種別へ戻ると、その種別で入力した語は復元される (種別ごとの記憶)
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1')).toHaveText('設計判断問題集');
  await expect(page.locator('input[aria-label="問題検索"]')).toHaveValue('CAP');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quiz search scoping caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: quiz 検索の結果件数が live region でアナウンスされる (WCAG 4.1.3) =====
// 従来は **0 件のときだけ** 空状態 div が role=status を持ち、**ヒット時は完全に無言**だった
// (ProjectsPage は件数を status で通知しているのに quiz 側だけ非対称)。SR 利用者は絞り込みが
// 効いたのか結果が何件なのか分からない。sr-only の status を 1 本用意し、ヒット時は件数を、
// 0 件時はその旨を announce する (視覚表示は不変・空状態 div からは live 属性を外して二重読み上げを回避)。
test('Quiz search announces the match count in a live region (WCAG 4.1.3)', async ({ page }) => {
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');

  const status = page.locator('div.sr-only[role="status"][aria-live="polite"]');
  await expect(page.getByRole('searchbox', { name: '問題検索' })).toBeVisible();

  // 初期描画では喋らない (無条件アナウンスの抑制)
  await expect(status).toHaveText('');

  // ヒット時: 件数がアナウンスされる (文言は _filterBy の正規化済みクエリ = 小文字を使う既存仕様)
  await page.getByRole('searchbox', { name: '問題検索' }).fill('CAP');
  await expect(status).toHaveText(/「cap」に一致する問題 [1-9][0-9]* 件/);

  // 0 件時: 見つからない旨がアナウンスされる (空状態 div は live region ではない = 二重読み上げなし)
  await page.getByRole('searchbox', { name: '問題検索' }).fill('zzz-no-match-9902');
  await expect(status).toHaveText(/「zzz-no-match-9902」に一致する問題は見つかりませんでした。/);
  await expect(page.locator('.panel-empty[role="status"]')).toHaveCount(0);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quiz count live region caused a fatal: ${fatal}`).toBeNull();
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


// ===== 7.2: quiz 検索が ARIA search landmark (role='search') で公開される (ARIA APG) =====
// 検索入力を role='search' の landmark で包み、SR ユーザーが landmark ナビゲーションで検索領域へ
// 直接ジャンプできる (WCAG 1.3.1)。ProjectsPage 検索 (#879) と同型。landmark が検索 input を
// 内包することを検証する。
test('Quiz search is exposed as an ARIA search landmark containing the query input', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  const searchLandmark = page.getByRole('search');
  await expect(searchLandmark).toBeVisible();
  await expect(searchLandmark.getByRole('searchbox', { name: '問題検索' })).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quiz search landmark caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: 模範解答フォームの必須フィールドが aria-required で露出される (WCAG 3.3.2) =====
// お名前・メールアドレスは submit の JS バリデーションで必須だが、従来は aria-required 未指定で
// SR ユーザーには送信してエラーが出るまで必須と分からなかった。aria-required='true' で必須状態を
// 事前露出する (メッセージは optional ゆえ非該当)。name/email が required・message が非 required
// であることを検証する。
test('Quiz contact form marks name and email as aria-required (WCAG 3.3.2)', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByRole('textbox', { name: 'お名前' })).toHaveAttribute('aria-required', 'true');
  await expect(page.getByRole('textbox', { name: 'メールアドレス' })).toHaveAttribute('aria-required', 'true');
  // メッセージは任意ゆえ aria-required を持たない
  await expect(page.getByRole('textbox', { name: 'メッセージ' })).not.toHaveAttribute('aria-required', 'true');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quiz form required caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: hiring-risk の CTA が「ラベルどおりの」問題集へ着地する (silent wrong-content) =====
// QuizPage は `QUIZ_DATA_MAP[type] || QUIZ_DATA_MAP.aws` で描画するため、CTA の ?type= が typo/
// 未定義でも例外にならず **AWS 問題集が黙って描画される**。「PM問題集を見る」を押して AWS の問題が
// 出ても throw も console error も無く、既存 e2e (直接 URL で pm/quality を開く quiz.spec:171) は
// CTA 経路を通らないため素通りする。Check 401a が静的 (リテラル ⟹ QUIZ_DATA_MAP キー) に守る面の
// **behavioral 対**として、採用担当が実際にたどる導線でラベルと着地先が一致することを検証する。
test('Hiring-risk CTAs land on the quiz named on the button (not the AWS fallback)', async ({ page }) => {
  await page.goto('/#/hiring-risk');
  await page.waitForLoadState('domcontentloaded');

  // PM: ボタンのラベルどおり PM問題集 へ着地する (AWS フォールバックでない)
  await page.getByRole('button', { name: 'PM問題集を見る' }).click();
  await expect(page).toHaveURL(/#\/quiz\?type=pm$/);
  await expect(page.locator('h1')).toHaveText('PM問題集');

  // 品質: 同じく「品質・プロセス問題集」へ着地する
  await page.goto('/#/hiring-risk');
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: '品質問題集を見る' }).click();
  await expect(page).toHaveURL(/#\/quiz\?type=quality$/);
  await expect(page.locator('h1')).toHaveText('品質・プロセス問題集');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `hiring-risk quiz CTA caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: 検証エラーが不正フィールドを特定できる (WCAG 3.3.1 Error Identification) =====
// 従来は Toast を出すだけで、**どのフィールドが不正か** が SR に伝わらず利用者はフォームを探し直す
// 必要があった (aria-invalid も focus 移動も無し)。不正な入力へ aria-invalid を立て、最初の不正
// フィールドへ focus を移す。focus 判定は並列ワーカーで document が inactive でも安定するよう
// document.activeElement の aria-label を評価して行う (toBeFocused の "inactive" 問題を回避)。
test('Quiz contact form marks the offending field aria-invalid and focuses it (WCAG 3.3.1)', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  const nameInput = page.getByRole('textbox', { name: 'お名前' });
  const emailInput = page.getByRole('textbox', { name: 'メールアドレス' });
  await expect(nameInput).toBeVisible();

  // 空のまま送信 → 名前が不正としてマークされ focus が移る
  await page.getByRole('button', { name: '送信' }).click();
  await expect(nameInput).toHaveAttribute('aria-invalid', 'true');
  await expect(emailInput).toHaveAttribute('aria-invalid', 'true');
  expect(await page.evaluate(() => document.activeElement?.getAttribute('aria-label'))).toBe('お名前');

  // 名前だけ埋めて送信 → 名前のマークは外れ、メール側が不正として focus される
  await nameInput.fill('E2E-NAME');
  await page.getByRole('button', { name: '送信' }).click();
  await expect(nameInput).not.toHaveAttribute('aria-invalid', 'true');
  await expect(emailInput).toHaveAttribute('aria-invalid', 'true');
  expect(await page.evaluate(() => document.activeElement?.getAttribute('aria-label'))).toBe('メールアドレス');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `form error identification caused a fatal: ${fatal}`).toBeNull();
});
