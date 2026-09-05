const { test, expect } = require('@playwright/test');

// ===== quiz データの遅延読み込み契約 (動的 import のライフサイクル) =====
// `e2e/quiz.spec.js` から分離 (2026-08-23)。同 file が advisory 予算 900 行を超えており (923)、
// **BLOCKING(1,000) に当たる前に**単一の技術契約という coherent な塊として切り出した。
//
// なぜこの塊なのか: #1239 で quiz データ 130,595 bytes (配信 JS+CSS の 15.6%) を静的 import から
// **動的 import へ移し、クリティカルパスから外した**。その結果 quiz を開かない訪問者は 4 file を
// 一切取得しなくなったが、代わりに **「まだ届いていない」という状態が新しく生まれた**。
// ここが守るのはその状態の扱い全部:
//   - 開いた種別だけを取得する (開かなければ 0 件)
//   - 読み込み中に検索語を打っても捨てない
//   - **未着を「見つかりませんでした」と偽らない** (嘘をつかない)
//   - 失敗を黙らず報告する / 通信断から回復する (module map に失敗がキャッシュされる #1239 の class)
//   - 再訪で再取得しない (ESM module cache)
//   - 読み込み中を aria-busy で伝える
//
// オフライン時の挙動もここに含める —— 遅延化の**明示的なトレードオフ**なので、
// 「そういう設計だ」と記録する場所が要る。

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
  //   [FIX 2/2] `#content h2` でも足りない —— 問い合わせフォームの見出し「模範解答について」は
  //   **データと無関係に同期描画される**ので、それに一致して通ってしまう (実測 2026-08-21)。
  //   一覧コンテナ (`[data-quiz-list]`) に限定して初めて「データが届いた」ことの検証になる。
  await expect(page.locator('[data-quiz-list] h2').first(),
    '問題データ由来の章見出しが描画されていない').toBeVisible();
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
// ===== 通信が落ちても枠は出て、失敗は伝わる (遅延読み込みのトレードオフを明示する) =====
// **これは遅延読み込み (#1239) が持ち込んだトレードオフの記録でもある。** 静的 import だった頃は
// home を開いた時点で問題集データも取得済みだったので、その後オフラインになっても quiz は開けた。
// 動的 import にしたことで「一度も quiz を開いていない訪問者が通信を失うと読めない」状態が生まれる。
//
// 130,595 bytes を全訪問者のクリティカルパスから外す価値の方が明確に大きいと判断したうえで、
// **その代わりに「黙って空にしない」ことを保証する**のがこの test。
//
// [訂正 2026-08-21] 当初この comment は「**SW が shell を返すので**枠は出る」と書いていたが
// **誤りだった**。実測すると (a) `caches.keys()` は空 —— この SW は AIO 目的で fetch を
// 介在させるだけで **shell をキャッシュしない** (b) オフラインで**完全リロードすると
// `ERR_INTERNET_DISCONNECTED` で失敗する** —— **このサイトはオフライン対応ではない**。
// 枠が出るのは `#/quiz` への遷移が **同一文書の hash 変更**でリロードを伴わず、shell が
// 既にメモリ上にあるから。**誤った前提の comment は次に読む人を誤らせる**ので訂正する
// (§7)。裏付けは `docs/files/sw.js.md` (「app shell を意図的にキャッシュしない設計」と明記)。
// したがってこの test が守るのは「オフラインでも動く」ではなく
// **「通信が落ちた状態でデータ取得だけが失敗したとき、黙って空にせず伝える」**。
// ===== 読み込み中に入力した検索語が捨てられない (遅延読み込みが持ち込んだ race) =====
// 遅延読み込み (#1239) で「データが来るまでの窓」が生まれた。その窓の間に検索欄へ入力できて
// しまう —— 見出しと検索欄は**同期に描かれる**設計なので、これは利用者にとって自然な操作。
//
// 到着時に「描画開始時点の語」で描くと、**入力欄には語が残ったまま一覧は絞り込み前**という
// 食い違いになる (実測 2026-08-21: 「EC2」と入れたまま全 7 章が出る。通常操作なら 4 章)。
// 利用者からは「検索したのに効いていない」としか見えず、入力欄に語が残っているので
// 原因に見当がつかない。到着時点の入力値で描き直すのが正しい。
test('Quiz applies a search typed while the data was still loading', async ({ page }) => {
  // [FIX 2026-09-05] 旧版は `setTimeout(1200)` で到着を遅らせ、その 1,200ms の間に入力と
  //   control の確認が終わることに**賭けていた**。フルスイートの並列負荷では `#content h1`
  //   の可視待ちだけで窓を使い切り、**データが先に届いて「読み込み中」が消えてから** control
  //   を読むので `toHaveCount(1)` が落ちる (実測 2026-09-05: フルスイート 1 回目で 1 failed /
  //   単独実行と 2 回目は pass = 非決定的)。同じ class は 2026-08-23 に下の aria-busy テストで
  //   一度潰しており、**このテストだけ掃引から漏れていた**。
  //   時間ではなく**明示的な解放ゲート**にして、検証が終わるまで到着させない。
  let releaseModule;
  const moduleGate = new Promise((resolve) => { releaseModule = resolve; });
  await page.route('**/js/quiz/aws-quiz-data.js*', async (route) => {
    await moduleGate;
    await route.continue();
  });

  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1', { hasText: 'AWS問題集' })).toBeVisible();

  // control: まだデータが来ていない窓の中で操作していること
  await expect(page.locator('[data-quiz-loading]'),
    'control: 読み込み中の窓が作れていない — race を再現できない').toHaveCount(1);

  await page.getByLabel('問題検索').fill('EC2');

  // 読み込み中は「読み込んでいます」を出し続ける —— データ未着で 0 件になるのを
  //   「見つかりませんでした」と出すと **嘘になる** (まだ届いていないだけ)。
  await expect(page.locator('[data-quiz-list]'),
    'データ未着なのに「見つかりませんでした」と出している').toContainText('読み込んでいます');

  // ここまでの検証が終わってから初めてデータを流す —— 窓の長さがマシン速度に依存しなくなる。
  releaseModule();

  // 到着後: 入力欄・一覧・アナウンスの 3 つが一致する
  //   [FIX] `[data-quiz-loading]` の消失で待ってはいけない —— **入力すると読み込み中の
  //   ボックスも一度作り直される**ので、到着前に条件が動きうる。章見出しの出現で待つ。
  const sections = page.locator('[data-quiz-list] h2');
  await expect(sections.first()).toBeVisible();
  await expect(page.getByLabel('問題検索')).toHaveValue('EC2');
  const filtered = await sections.count();
  expect(filtered, '読み込み中に入力した語が捨てられ、絞り込み前の一覧が出ている').toBeGreaterThan(0);
  await expect(page.locator('#content [role="status"]'),
    '件数アナウンスが検索結果と食い違っている').toContainText('に一致する問題 ' + filtered + ' 件');

  // control: そもそも「EC2」が全件より少ないこと (同数なら絞り込めておらず検証にならない)。
  //   **再訪では測れない** —— 検索語は永続化される (#684) ので `goto` し直しても "EC2" が
  //   残り、同じ 4 章になる (実測 2026-08-21 に踏んだ)。その場で空にして比べる。
  await page.getByLabel('問題検索').fill('');
  await expect.poll(async () => sections.count(),
    { message: 'control: 検索を空にしても件数が増えない — 絞り込めていない' })
    .toBeGreaterThan(filtered);
});
test('Quiz degrades gracefully when opened offline (lazy-load trade-off is explicit)', async ({ page, context }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#content h1').first()).toBeVisible();

  // control: shell が既に読み込まれていること (これが無いと「そもそもページが無い」状態と
  //   「データ取得だけ失敗」を取り違える。SW は shell をキャッシュしないので、
  //   ここで頼れるのは **同一文書のまま遷移すること** だけ)。
  await expect(page.locator('.hero-section'),
    'control: shell が読み込まれていない — データ取得だけの失敗を検証できない').toBeVisible();

  await context.setOffline(true);
  try {
    await page.goto('/#/quiz');
    await page.waitForLoadState('domcontentloaded');

    // 枠は出る —— 同一文書のまま遷移するので shell はメモリ上にある
    //   (SW は shell をキャッシュしない: docs/files/sw.js.md §How)
    await expect(page.locator('#content h1', { hasText: 'AWS問題集' })).toBeVisible();
    // データは失敗として伝わる (黙って空にしない)
    await expect(page.locator('#content [role="alert"]')).toContainText('読み込みに失敗');
    // 章見出しは出ない = データが無いことの裏取り (control の対)
    await expect(page.locator('[data-quiz-list] h2')).toHaveCount(0);

    const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
    expect(fatal, `offline quiz caused a fatal: ${fatal}`).toBeNull();
  } finally {
    await context.setOffline(false);
  }
});
test('Quiz reports a failed data load instead of showing an empty question set', async ({ page }) => {
// NOTE: route パターンの末尾 `*` は **再取得の `?retry=N` 付き URL も捕まえる**ため。
//   失敗時に別 URL で取り直す形にした (#1261) ので、`*` が無いと 2 本目が素通りして成功し、
//   「失敗を伝える」ことを検査するはずの test が緑になる (実際に踏んだ)。
  await page.route('**/js/quiz/aws-quiz-data.js*', (route) => route.abort());

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
// ===== 再訪で問題集を再ダウンロードしない (遅延化の利得を守る) =====
// 動的 import は **ESM のモジュールキャッシュ**が効くので、一度開いた問題集は再訪しても
// ネットワークに出ない。これは遅延化 (#1239) の利得を成立させている前提で、
// 例えば loader に cache-buster (`import('./x.js?v=' + Date.now())`) を足すと
// **開くたびに 83KB を落とす**ようになる —— 体感は速いままなので気付きにくいが、
// 通信量とバッテリーには効く。
//
// NOTE: 再訪時も「読み込み中」の DOM は一瞬挿入される (QuizPage は毎回新しい closure なので
//   `sourceData` は null から始まる)。ただし実測 (2026-08-21) では **1ms で content へ入れ替わる**
//   ため知覚できず、`aria-busy` も同じく 1ms。**キャッシュを足す変更はしていない** ——
//   必要性を実測で示せないまま複雑さを足すのは padding (CLAUDE.md §7)。
test('Revisiting the quiz does not re-download the question set (ESM module cache)', async ({ page }) => {
  const fetched = [];
  page.on('request', (r) => {
    const u = r.url();
    if (u.includes('/js/quiz/')) { fetched.push(u.split('/js/')[1]); }
  });

  await page.goto('/#/quiz');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('[data-quiz-list] h2').first()).toBeVisible();
  // control: 初回は実際に取りに行っていること (行っていなければ以下の比較が無意味)
  expect(fetched, 'control: 初回に問題集を取得していない').toEqual(['quiz/aws-quiz-data.js']);

  // 離れて戻る (同一文書の hash 遷移 = 実際の利用者の経路)
  await page.evaluate(() => { location.hash = '#/'; });
  await expect(page.locator('.hero-section')).toBeVisible();
  await page.evaluate(() => { location.hash = '#/quiz'; });
  await expect(page.locator('[data-quiz-list] h2').first()).toBeVisible();

  expect(fetched, `再訪で問題集を取り直している (取得: ${JSON.stringify(fetched)})`)
    .toEqual(['quiz/aws-quiz-data.js']);
});
test('Quiz announces the loading window with aria-busy while data is in flight', async ({ page }) => {
  // [FIX 2026-08-23] 旧版は `setTimeout(900)` でモジュールの到着を遅らせ、その 900ms の間に
  //   検証が終わることに**賭けていた**。負荷が高いと `#content h1` の可視待ちだけで 900ms を
  //   超え、**モジュールが先に届いて「読み込み中」の窓が消えてから** control を読むので、
  //   `toHaveCount(1)` が 0 のまま 5s poll して落ちる (実測: 単独実行 3 回で 1 failed / 2 passed、
  //   かつ main でも再現。BLOCKING gate を偽赤にする)。
  //   時間ではなく**明示的な解放ゲート**にして、検証が終わるまで到着させない。これで
  //   「読み込み中の窓が観測できる長さ」がマシン速度に依存しなくなる
  //   (docs/files/playwright.config.cjs.md「固定時間待ちは実装内部の定数への賭け」)。
  let releaseModule;
  const moduleGate = new Promise((resolve) => { releaseModule = resolve; });
  await page.route('**/js/quiz/aws-quiz-data.js*', async (route) => {
    await moduleGate;
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

  // ここまで確認できてから初めて到着させる
  releaseModule();

  // 到着 → busy 解除 + 実データ由来の章見出しが出る
  await expect(page.locator('[data-quiz-list] h2').first()).toBeVisible();
  await expect(page.locator('[data-quiz-loading]')).toHaveCount(0);
  await expect(page.locator('#content [aria-busy]').first()).toHaveAttribute('aria-busy', 'false');
});
// ===== 一時的な失敗から回復する (module map が失敗をキャッシュする問題) =====
// 遅延読み込み (#1239) が持ち込んだ 3 つ目の失敗モード。**失敗した動的 import は
// module map にキャッシュされ、以降の import は「ネットワークへ行かずに」即 reject する。**
// つまり通信が一瞬切れただけで、その文書が生きている限り quiz は永久に読めない。
//
// 実測 (2026-08-21・修正前): 1 回目を abort → 失敗表示。別ルートへ移動して `#/quiz` へ戻ると
// **リクエストが 1 本も発生しないまま**また失敗表示 (章数 0)。エラーカードは「再読み込みして
// ください」と言うので完全なリロードなら直るが、**利用者が自然にやる「開き直す」では直らない**。
//
// 修正は「失敗したらクエリを足した別 URL で取り直す」。別 URL = 新しい module map entry
// なので実際に再取得される。番号は毎回増やす (同じ URL では 2 度目の失敗も同様に固まる)。
//
// 非 vacuity: `.catch(() => _retryQuizData(type))` を外すと 1 本目しかリクエストが出ず
// 章数 0 のまま RED。control として **2 本目のリクエストが実際に発生したこと**も見る
// (「たまたま 1 本目が成功した」と区別できないと何も検査していないことになる)。
test('Quiz recovers from a transient load failure by refetching under a new URL', async ({ page }) => {
  const requested = [];
  let failFirst = true;
  await page.route('**/js/quiz/aws-quiz-data.js*', async (route) => {
    requested.push(route.request().url().split('/').pop());
    if (failFirst) { failFirst = false; await route.abort('failed'); return; }
    await route.continue();
  });

  await page.goto('/#/quiz', { waitUntil: 'domcontentloaded' });

  // 回復して中身が出る (章見出しは一覧コンテナ内にしか無いので「データが届いた」の証拠になる)
  await expect(page.locator('[data-quiz-list] h2').first(),
    '一時的な失敗から回復していない').toBeVisible({ timeout: 10000 });
  await expect(page.getByText('問題の読み込みに失敗しました'),
    '回復したのに失敗表示が残っている').toHaveCount(0);

  // control: 1 本目が失敗し、**別 URL で 2 本目が出た**こと自体を確かめる。
  //   これが無いと「1 本目がそのまま成功した」場合と区別できない。
  expect(requested.length, `再取得が発生していない: ${JSON.stringify(requested)}`).toBeGreaterThanOrEqual(2);
  expect(requested[0], '1 本目はクエリなしのリテラル URL').toBe('aws-quiz-data.js');
  expect(requested[1], '2 本目は別 URL (module map の失敗キャッシュを避けるため)').toContain('?retry=');
});
// 通信が本当に落ちている (再取得も失敗する) ときは、従来どおり失敗を伝える。
// 上の test と対で、「再取得を足したせいで失敗が握り潰される」実装を落とすための片割れ。
test('Quiz still reports failure when the refetch also fails', async ({ page }) => {
  await page.route('**/js/quiz/aws-quiz-data.js*', (route) => route.abort('failed'));
  await page.goto('/#/quiz', { waitUntil: 'domcontentloaded' });
  await expect(page.getByText('問題の読み込みに失敗しました'),
    '全て失敗しているのに黙っている').toBeVisible({ timeout: 10000 });
  await expect(page.locator('[data-quiz-list] h2')).toHaveCount(0);
  expect(await page.evaluate(() => !!window.__fatalError), 'FatalPage へ落ちている').toBe(false);
});
