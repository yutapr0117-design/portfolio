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
// ===== 検索語が上限で黙って切られない (入力できる範囲 == 保存される範囲) =====
// store.js の normalize は `quizSearch` を `LIMITS.QUIZ_SEARCH` で slice するのに、検索欄には
// maxlength が無かった。超過分は**入力欄にも検索結果にも出たまま**で、**reload して初めて消える**
// (実測 2026-08-21: 260 文字入力 → 保存 260 → reload 後 200)。利用者から見ると
// 「さっきと同じ語で検索しているのに結果が違う」としか見えない silent truncation。
// #924 (ノート) / #1063 (プロジェクト名) / #1064 (Tech) と同じ class の 4 例目。
//
// NOTE: 一般化した Check は**足していない**。実行時に全入力欄の maxlength を測ったところ、
//   未設定なのは他に「プロジェクト検索」(URL 由来で localStorage へ保存されず切り詰めなし) と
//   `settingsNewTech` (追加時に validateAndNormalize を通すので即座に反映される・#1064) だけで、
//   どちらも**切り詰めが起きない正当な未設定**だった。「全テキスト入力に maxlength を要求」
//   という Check はこの 2 つを誤検出し、意味のない上限を足す圧力になる (§7 の brittle-gate 禁止)。
// ===== 問題集データは遅延読み込みされる (クリティカルパスから 130,595 bytes を外す) =====
// 従来は main.js が 4 つの問題集 (計 130,595 bytes = 配信 JS+CSS の 15.6%) を静的 import し、
// **modulepreload まで宣言**していたため、quiz を一度も開かない訪問者も毎回 4 ファイルすべてを
// 高優先度で取得していた (実測 2026-08-21: home を開くだけで 4 件 fetch)。
// 見出し・検索欄は同期のまま描けるので、データだけ動的 import へ移した。
//
// この test が守るのは 3 点: (a) home で取りに行かない (b) quiz を開くと**該当 1 件だけ**取りに行く
// (c) 到着後に実際の問題が描画される。(c) が無いと「取得しない」だけを満たす壊れた実装が通る。
test('Quiz data is fetched only when the quiz is opened, and only the requested set', async ({ page }) => {
  const fetched = [];
  page.on('response', (r) => {
    const u = r.url();
    if (u.includes('/js/quiz/')) { fetched.push(u.split('/js/')[1]); }
  });

  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1').first()).toBeVisible();
  // control: home が描画済みであること (描画前に読むと「まだ取得していない」を「取得しない」と誤読する)
  await expect(page.locator('.hero-section')).toBeVisible();
  expect(fetched, 'quiz を開いていないのに問題集データを取得している').toEqual([]);

  await page.goto('/#/quiz?type=pm');
  await page.waitForLoadState('domcontentloaded');
  // (c) 到着後に実際の問題が出る
  //   [FIX] `.card` で待ってはいけない —— **「問題を読み込んでいます…」のボックス自体が
  //   `.card`** なので、データが来る前に成立してしまい (c) を検証できない
  //   (実測 2026-08-21: 読み込み中でも `#content .card` は 2 件あり visible 待ちが通る)。
  //   章見出し (h2) はデータからしか生えないので、これを実コンテンツの目印にする。
  await expect(page.locator('#content h1', { hasText: 'PM問題集' })).toBeVisible();
  await expect(page.locator('#content h2').first(), '問題データ由来の章見出しが描画されていない').toBeVisible();
  await expect(page.locator('[data-quiz-loading]'), '読み込み中ボックスが残っている').toHaveCount(0);
  await expect(page.locator('#content [aria-busy]').first(),
    '読み込み完了後も aria-busy が true のまま').toHaveAttribute('aria-busy', 'false');

  // (b) 開いた種別だけを取りに行く (4 件まとめて取ると遅延化の意味が無い)
  expect(fetched, `取得したのは ${JSON.stringify(fetched)}`).toEqual(['quiz/pm-quiz-data.js']);
});


// ===== 読み込み中であることが SR にも伝わる (WCAG 4.1.3) =====
// 遅延読み込みにしたことで「データが来るまでの間」が生まれた。視覚的には
// 「問題を読み込んでいます…」と見えるが、**それだけでは SR に「まだ来ていない」ことが
// 伝わらない**。#content が aria-busy で描画中を宣言しているのと同じ契約を listHost にも与える。
//
// 通信を遅らせて「読み込み中」の窓を実際に作ってから測る (遅延させないと窓が短すぎて
// 何も検証できないまま緑になる)。
// ===== 読み込みに失敗しても黙って空にしない (silent failure 禁止) =====
// 遅延読み込み (#1239) にしたことで **「取得に失敗する」経路が新しく生まれた**。
// ここで何も出さないと、利用者には「問題が 0 件の問題集」と区別が付かない —— 通信を直せば
// 直る話なのに、壊れているのかデータが無いのか判らない (§7 の silent-failure 禁止)。
//
// 併せて「失敗しても FatalPage へ落ちない」ことも見る。`_filterBy` はデータ未着を空集合として
// 扱う総関数にしてあるが、そこが throw する形へ退行すると **ページ全体が表示不能**になる。
test('Quiz reports a failed data load instead of showing an empty question set', async ({ page }) => {
  await page.route('**/js/quiz/aws-quiz-data.js', (route) => route.abort());

  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');
  // 見出しと検索欄は同期に描かれる (データを待たない設計) ので、失敗しても枠は出る
  await expect(page.locator('#content h1', { hasText: 'AWS問題集' })).toBeVisible();

  // 失敗が利用者に伝わる
  const alertBox = page.locator('#content [role="alert"]');
  await expect(alertBox, '読み込み失敗が何も表示されない (空の一覧と区別が付かない)').toBeVisible();
  await expect(alertBox).toContainText('読み込みに失敗');

  // 読み込み中の表示は残さない / busy も解除する (「永久に読み込み中」に見せない)
  await expect(page.locator('[data-quiz-loading]')).toHaveCount(0);
  await expect(page.locator('#content [aria-busy]').first()).toHaveAttribute('aria-busy', 'false');

  // FatalPage へ落ちない
  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `quiz data load failure caused a fatal: ${fatal}`).toBeNull();
});


test('Quiz announces the loading window with aria-busy while data is in flight', async ({ page }) => {
  await page.route('**/js/quiz/aws-quiz-data.js', async (route) => {
    await new Promise((r) => setTimeout(r, 900));
    await route.continue();
  });

  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'AWS問題集' })).toBeVisible();

  // control: 遅延が効いて「読み込み中」の窓が実在すること (無ければ以下は何も検証しない)
  await expect(page.locator('[data-quiz-loading]'),
    'control: 読み込み中の窓が作れていない — 以降の検証が vacuous になる').toHaveCount(1);
  await expect(page.locator('#content [aria-busy="true"]').first(),
    '読み込み中なのに aria-busy が立っていない').toBeVisible();

  // 到着 → busy 解除 + 実データ由来の章見出しが出る
  await expect(page.locator('#content h2').first()).toBeVisible();
  await expect(page.locator('[data-quiz-loading]')).toHaveCount(0);
  await expect(page.locator('#content [aria-busy]').first()).toHaveAttribute('aria-busy', 'false');
});


test('Quiz search input cannot hold more text than it persists (maxlength == LIMITS.QUIZ_SEARCH)', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  const search = page.getByLabel('問題検索');
  await expect(search).toBeVisible();

  // control: 上限そのものが宣言されていること (未宣言なら以下の比較は無意味)
  const max = Number(await search.getAttribute('maxlength'));
  expect(max, 'control: 検索欄に maxlength が宣言されていない').toBeGreaterThan(0);

  // 上限を超えて入力しても、その場で上限に収まる (reload まで気付けない状態を作らない)
  await search.fill('あ'.repeat(max + 60));
  const typed = await search.inputValue();
  expect(typed.length, '入力欄が保存される範囲より多く保持している').toBe(max);

  // reload を跨いでも長さが変わらない = 黙って切られていない
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  const after = page.getByLabel('問題検索');
  await expect(after).toBeVisible();
  await expect(after, 'reload で検索語が黙って短くなった').toHaveValue(typed);
});


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
// [FIX] 旧版は **見出しとブロックの存在しか見ていなかった**。見出しは QUIZ_DATA_MAP の
//   `title` から出るので、`data:` を別の問題集へ取り違えても (map 内の copy-paste 事故)
//   「PM問題集」の見出しで AWS の問題が並ぶ状態が **緑のまま通る** (実測: pm の data を
//   awsQuizData へ差し替えても pass した)。**題名は「render their data files」と主張して
//   いるのに、どのデータかを検証していなかった。** 各データ固有の本文で中身まで見る。
test('Quiz pm and quality types render their data files', async ({ page }) => {
  await page.goto('/#/quiz?type=pm');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1', { hasText: 'PM問題集' })).toBeVisible();
  await expect(page.locator('.quiz-question-block').first()).toBeVisible();
  // pm データ固有の本文 (aws/quality には無い)
  await expect(page.locator('#content'),
    'PM問題集の見出しなのに PM データが描画されていない — QUIZ_DATA_MAP の data 取り違え'
  ).toContainText('要求が曖昧なまま始まりそうなとき');

  await page.goto('/#/quiz?type=quality');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('h1', { hasText: '品質・プロセス問題集' })).toBeVisible();
  await expect(page.locator('.quiz-question-block').first()).toBeVisible();
  await expect(page.locator('#content'),
    '品質問題集の見出しなのに品質データが描画されていない — QUIZ_DATA_MAP の data 取り違え'
  ).toContainText('品質が落ち始めた兆候');
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
  // NOTE: 2026-08-21 以降、`fill()` が発火する input イベントでも aria-invalid は落ちる
  //   (下の「入力した瞬間に外れる」test を参照)。よってこの assertion は
  //   **送信時の解除だけを切り分けてはいない** —— 利用者から見た契約
  //   「直して送り直せばマークが外れている」は両経路のどちらでも成立するため、
  //   ここではその契約を守る。入力時の解除そのものは下の test が単独で守る。
  await nameInput.fill('E2E-NAME');
  await page.getByRole('button', { name: '送信' }).click();
  await expect(nameInput).not.toHaveAttribute('aria-invalid', 'true');
  await expect(emailInput).toHaveAttribute('aria-invalid', 'true');
  expect(await page.evaluate(() => document.activeElement?.getAttribute('aria-label'))).toBe('メールアドレス');

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `form error identification caused a fatal: ${fatal}`).toBeNull();
});


// ===== 修正した瞬間に aria-invalid が外れる (WCAG 3.3.1 / 状態の鮮度) =====
// 上の test は「送信 → マーク」「直して再送信 → 解除」を見る。だが**直してから再送信するまでの
// 間**、フィールドは「不正」のままだった (実測 2026-08-21: 空送信 → 正しい値を入力しても
// aria-invalid=true が残る)。SR 利用者が直した欄へ戻ると **正しく直したのに「不正」と読まれ**、
// 修正が効いたのか判別できない。
//
// 入力途中で「不正」と marking し直すのは敵対的なので **付けるのは送信時のみ・外すのは入力時**
// という非対称が正しい (ARIA APG のフォーム検証の作法)。この test はその非対称を固定する。
test('Quiz contact form clears aria-invalid as soon as the field is corrected (WCAG 3.3.1)', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  const nameInput = page.getByRole('textbox', { name: 'お名前' });
  const emailInput = page.getByRole('textbox', { name: 'メールアドレス' });
  await expect(nameInput).toBeVisible();

  // control: そもそもマークが付かないと「外れること」を検証できない
  await page.getByRole('button', { name: '送信' }).click();
  await expect(nameInput, 'control: 空送信でマークが付いていない').toHaveAttribute('aria-invalid', 'true');
  await expect(emailInput, 'control: 空送信でマークが付いていない').toHaveAttribute('aria-invalid', 'true');

  // 入力しただけで (送信せずに) 当該フィールドのマークが外れる
  await nameInput.fill('E2E-CORRECTED');
  await expect(nameInput, '直したのに aria-invalid が残っている').not.toHaveAttribute('aria-invalid', 'true');
  // 直していない側は残る (無条件に外していないこと = 一括解除への退行を捕捉)
  await expect(emailInput, '直していない欄まで一緒に解除されている').toHaveAttribute('aria-invalid', 'true');

  await emailInput.fill('e2e@example.com');
  await expect(emailInput, '直したのに aria-invalid が残っている').not.toHaveAttribute('aria-invalid', 'true');

  // 空に戻しても入力途中で「不正」とは marking しない (付けるのは送信時のみ)
  await nameInput.fill('');
  await expect(nameInput, '入力途中で不正マークを付け直している').not.toHaveAttribute('aria-invalid', 'true');
});


// ===== 外部入力 ?type= のプロトタイプ継承キーで quiz が表示不能になる回帰の防止 =====
// QuizPage は `?type=` を QUIZ_DATA_MAP の添字にして問題集を選ぶ。素の `MAP[type] || fallback` は
// プロトタイプ継承キー ('constructor' / 'toString' / '__proto__' / 'valueOf' / 'hasOwnProperty') に対し
// **truthy な非 config 値** (Object コンストラクタ等) を返すため fallback が効かず、sourceData が
// undefined のまま Object.keys(undefined) が throw → **ErrorBoundary の FatalPage でページ全体が
// 表示不能**になっていた (実測: "Cannot convert undefined or null to object")。
// 同じ添字が js/page-meta.js のタイトル解決にもあり、そちらは document.title が
// "function Object() { [native code] }" に化けていた (AIO 面の可視 drift)。
// 外部入力を object の添字に使う箇所は自前キーだけを採用する (#350 の不正 ?cat= 正規化と同 class)。
const PROTO_KEYS = ['constructor', 'toString', '__proto__', 'valueOf', 'hasOwnProperty'];
for (const key of PROTO_KEYS) {
  // NOTE: 題名を template literal でなく文字列連結で書く。Check 379 / 397 (mutation の test
  //   フィールドが実 test title に一意解決することの強制) は `test('…')` の引用符リテラルのみを
  //   parse するため、backtick 題名は「解決不能」として false RED になる (safe-fail だが
  //   パラメタライズド test に mutation を登録できなくなる)。
  test('Quiz falls back to the default set for prototype-inherited ?type=' + key + ' (no fatal)', async ({ page }) => {
    // ホーム経由の 2 段 goto で fresh 初期化 (同一 URL 再訪の DOM 残留で vacuous になるのを避ける)
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.goto(`/#/quiz?type=${key}`);
    await page.waitForLoadState('domcontentloaded');

    // 1. 既定 (AWS) の問題集にフォールバックして描画される
    await expect(page.locator('#content h1')).toHaveText('AWS問題集');
    // 2. FatalPage ではない (代替ページは弱い合否条件を vacuous に通すため negative assertion を併用)
    await expect(page.locator('#fallback-details')).toHaveCount(0);
    // 3. ページタイトルが関数の文字列化に化けていない (page-meta 側の同 class fix)
    await expect(page).toHaveTitle(/^Quiz \|/);

    const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
    expect(fatal, `?type=${key} caused a fatal: ${fatal}`).toBeNull();
  });
}


// ===== 装飾絵文字が支援技術に読み上げられない (WCAG 1.1.1 Non-text Content) =====
// quiz の章アイコン (🏛️ 🗄️ 🔌 …) とゾーンラベルの接頭絵文字 (📋 状況 / 💬 … / 🎯 問) は純粋な装飾で、
// 意味は隣接するテキストが担う。aria-hidden が無いと SR は章題の前に「classical building」等を読み上げ、
// 全章・全問で意味の無い語が挟まる (実測: アクセシビリティツリーに絵文字がそのまま露出していた)。
// axe は装飾テキストの露出をルール化していないため、本テストが唯一の gate。
// 検証は DOM 属性ではなく **アクセシビリティツリー** を見る (属性の有無ではなく「AT に何が渡るか」が契約)。
const QUIZ_DECORATIVE_EMOJI = ['🏛️', '🗄️', '🔌', '⚖️', '🚨', '🔁', '📌', '📝', '📋', '💬', '🎯'];
test('Quiz decorative emoji are hidden from the accessibility tree (WCAG 1.1.1)', async ({ page }) => {
  await page.goto('/#/quiz?type=architecture');
  await page.waitForLoadState('domcontentloaded');

  // 描画確定を待ってから不在検査する (goto 直後の評価は async 描画とレースし vacuous になる)
  await expect(page.locator('#content h1')).toHaveText('設計判断問題集');
  await expect(page.locator('.quiz-section-icon').first()).toBeVisible();

  const snapshot = await page.locator('#content').ariaSnapshot();
  const leaked = QUIZ_DECORATIVE_EMOJI.filter(e => snapshot.includes(e));
  expect(leaked, `装飾絵文字がアクセシビリティツリーに露出: ${JSON.stringify(leaked)}`).toEqual([]);

  // 視覚的には従来どおり表示され続ける (aria-hidden は描画に影響しない = 非破壊)
  await expect(page.locator('.quiz-section-icon').first()).toContainText('🏛️');
  // ラベルの意味語は AT に残る (絵文字だけを隠し、テキストは隠していないことの確認)
  expect(snapshot).toContain('状況');
});

// ===== quiz の document.title が **既知の安全な集合** に収まる (title 化け防止の網羅) =====
// #926 は継承キー ('constructor' 等) で `map[type]` が関数を返し document.title が
// 「function Object() { [native code] }」に化けるバグを own-key 検証で直した。既存テストは
// 継承キー 3 種を個別に見ているが、**有効値・空値・未知値まで含めた全域**では見ていない。
// title はタブ名・履歴・AI クローラが受け取る機械可読面なので、化けると影響が広い。
//
// NOTE (実測して分かった仕様・意図的に変更しない): `?type=` が **空** のときは
//   `route.query.type || 'aws'` で AWS へ落ちるため title は「AWS問題集」になる一方、
//   `?type=zzz` のような **未知キー**では汎用「Quiz」になる。どちらも描画は AWS 問題集なので
//   title だけ食い違うが、**'Quiz' は #926 の既存テストが正規表現で pin している記録済みの
//   期待値**であり、覆すだけの根拠 (実害の測定) が無いためここでは現状を固定する。
//   3 面 (renderer / sidebar nav / title) のうち title だけ fallback を鏡写していない件は
//   観測として docs へ残した。
const QUIZ_TITLE_CASES = [
  ['aws', 'AWS問題集'],
  ['pm', 'PM問題集'],
  ['quality', '品質・プロセス問題集'],
  ['architecture', '設計判断問題集'],
  ['', 'AWS問題集'],
  ['zzz', 'Quiz'],
  ['constructor', 'Quiz'],
  ['__proto__', 'Quiz'],
];
for (const [type, expectedHead] of QUIZ_TITLE_CASES) {
  test('Quiz document.title stays in the known-safe set for ?type=' + (type || '(empty)'), async ({ page }) => {
    await page.goto('/#/quiz?type=' + type, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#content h1')).toBeVisible();

    await expect.poll(
      async () => (await page.title()).split(' | ')[0].trim(),
      { message: `?type=${type || '(empty)'}: document.title の見出し部が期待と違う` }
    ).toBe(expectedHead);

    // 関数ソースが漏れていないこと (#926 の回帰防止・全ケースで確認する)
    const title = await page.title();
    expect(title, 'title に関数ソースが漏れている').not.toContain('native code');
    expect(title, 'title に function が漏れている').not.toContain('function');
    expect(title, 'title が [object Object] 化している').not.toContain('[object');
  });
}


// ===== 模範解答フォームの入力が mailto の実行限界を超えない =====
// 3 つの入力は **`mailto:` の URL へ percent-encode して埋め込まれる**。日本語は 1 文字が
// `%XX%XX%XX` の 9 文字になるため URL が急速に伸びる (実測: メッセージ 100 文字で URL 1,252 /
// 500 文字で 4,852 / 4,000 文字で 36,352)。Windows の mailto 実行は **約 2,048 文字で切られる**
// ので、上限が無いと長文を書いて送信したときに **本文が欠けるか、そもそもメールソフトが
// 開かない** —— しかも利用者には何も伝わらない silent failure になる。
// 「入力できる範囲」と「実際に送れる範囲」を一致させる (#924/#1063/#1064 と同じ規律)。
//
// 最悪ケース (全部日本語) の URL 長を実測して上限を決めてあるので、その前提が崩れていないか
// (= 上限が外れたり緩められたりしていないか) を実際に組み立てて確認する。
test('模範解答フォームの入力上限が mailto の実行限界を超えない', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1').first()).toBeVisible();

  // 各欄に上限を大きく超える値を入れる → maxlength で止まるはず
  await page.getByLabel('お名前').fill('あ'.repeat(400));
  await page.getByLabel('メールアドレス').fill('a'.repeat(400) + '@example.com');
  await page.getByLabel('メッセージ').fill('あ'.repeat(2000));

  const measured = await page.evaluate(() => {
    const get = (label) => document.querySelector(`[aria-label="${label}"]`).value;
    const name = get('お名前');
    const email = get('メールアドレス');
    const message = get('メッセージ');
    // js/quiz-renderer.js の submit と同じ組み立て
    const body = encodeURIComponent(`お名前: ${name}\nメールアドレス: ${email}\n\nメッセージ:\n${message || '(なし)'}`);
    const subject = encodeURIComponent('AWS問題集の模範解答について');
    return {
      lengths: { name: name.length, email: email.length, message: message.length },
      url: ('mailto:yuta.pr.0117@gmail.com?subject=' + subject + '&body=' + body).length,
    };
  });

  // control: 実際に上限で止まっている (止まっていなければ URL 長の検査に意味が無い)
  expect(measured.lengths.name, 'control: お名前に上限が効いていない').toBeLessThan(400);
  expect(measured.lengths.message, 'control: メッセージに上限が効いていない').toBeLessThan(2000);

  expect(measured.url,
    `最悪ケースの mailto が実行限界を超える (実測 ${measured.url} 文字 / 目安 2048)`).toBeLessThan(2048);
});


// ===== 検証エラーが「目で見て」分かる (WCAG 3.3.1 / 1.4.1) =====
// アプリは不正な入力へ `aria-invalid="true"` を立てて focus を移すが、従来 CSS 側に
// `[aria-invalid]` の宣言が **1 つも無かった**。実測 (2026-08-20): 送信失敗直後の欄に出るのは
// 通常の primary フォーカスリングだけで **有効な欄を触ったときと見分けが付かず**、Tab で離れると
// 視覚的な痕跡はゼロになる (aria-invalid は true のまま = SR にだけ伝わる状態)。
// Toast は duration で消えるため、消えた後は「どの欄が不正か」の手がかりが無くなる。
// `--focus-ring-danger` はこの用途で定義されながら未使用だった。
//
// 色だけに依存しない (WCAG 1.4.1) よう、境界線の **太さ** も同時に変える。
test('Invalid form fields are visually distinguishable, not only announced', async ({ page }) => {
  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');

  const name = page.getByLabel('お名前');
  const optional = page.getByLabel('メッセージ');
  await expect(name).toBeVisible();

  const box = (l) => l.evaluate((el) => {
    const cs = getComputedStyle(el);
    return { color: cs.borderColor, width: cs.borderWidth };
  });

  // control: 送信前は必須欄も任意欄も同じ見た目 (ここが崩れると以下は何も検査しない)
  const before = await box(name);
  expect(before, '送信前から不正扱いになっている').toEqual(await box(optional));

  await page.getByRole('button', { name: '送信' }).first().click();
  await expect(name).toHaveAttribute('aria-invalid', 'true');

  // 不正欄は太さで区別できる (色だけに依存しない)。
  // NOTE: `.input` は `transition: all` を持つので **境界線幅はアニメーションする**。
  //   属性が付いた直後に読むと途中値 (まだ 1px) を掴む —— これは「変化」の検査なので poll が正しい
  //   (不変性の検査なら settle 後に 1 度読む・落とし穴表参照)。実際に一度踏んだ。
  await expect.poll(async () => (await box(name)).width,
    { timeout: 5000 }).not.toBe(before.width);
  const invalid = await box(name);
  expect(invalid.color, '不正欄の境界線色が変わっていない').not.toBe(before.color);

  // 任意欄は元のまま = 「全部が赤くなる」実装ではない
  expect(await box(optional), '不正でない欄まで警告表示になっている').toEqual(before);

  // focus を外しても痕跡が残る (Toast が消えた後も分かる)
  await name.blur();
  expect((await box(name)).width, 'blur で視覚的な痕跡が消えている').toBe(invalid.width);
});
