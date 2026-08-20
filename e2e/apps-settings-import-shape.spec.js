const { test, expect } = require('@playwright/test');

// ===== Settings の import が「どの形のファイルを、どこまで受け付けるか」の契約 =====
// エクスポートは 4 つの形を書き出す (full backup / Projectsのみ / AppsDataのみ / Profileのみ)。
// import 側がその一部しか受け付けないと、**バックアップとして提示している機能が
// 「戻せないファイル」を作る**ことになる。しかも従来は戻せないときでも
// 「インポートが完了しました」と報告していたため、利用者は復元できたと信じてしまう
// (#1038/#1040)。本 spec はこの契約 —— 受け付ける形・受け付けない形・
// 「対象」の選択で全部落ちる形 —— の 3 面をまとめて固定する。
//
// 元は apps-settings-io.spec.js にあったが、同 file が早期警告 (900 行) を超えたため
// **BLOCKING (1,000 行) を踏む前に**このテーマの塊を切り出した (CLAUDE.md §7 の
// 「advisory は BLOCKING を踏む前に効かせる」)。

// 通知の検証は sr-only の通知領域で行う (toast は 3 秒で自動消滅するため CI 負荷で
// 間欠 RED になる・#1018)。`#action-announcement` は次の通知まで消えない。
async function expectNotified(page, text) {
  await expect(page.locator('#action-announcement')).toContainText(text);
}

// ===== 部分 export したファイルも import で戻せること =====
// `Projectsのみ` は projects の **素の配列**を、`AppsDataのみ` / `Profileのみ` はそれぞれの
// **素のオブジェクト**を書き出すが、import は full-state 形 (`parsed.projects` 等) しか見て
// おらず、**何も起きないのに「インポートが完了しました」と報告**していた (実測 #1038)。
// バックアップとして提示している機能が「戻せないファイル」を作り、しかも成功したと言うのは
// **失敗するより悪い** —— 利用者は復元できたと信じてしまう。
test('部分 export (Projectsのみ) を import で戻せる', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  await page.locator('#settingsNewName').fill('部分往復テスト');
  await page.getByRole('button', { name: '追加', exact: true }).click();
  await expect(page.getByRole('button', { name: '削除：部分往復テスト' })).toBeVisible();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Projectsのみ', exact: true }).click(),
  ]);
  const file = await download.path();

  page.once('dialog', d => d.accept());
  await page.getByRole('button', { name: '全リセット', exact: true }).click();
  // control: リセットで消えていること (消えていなければ import の効果を測れない)
  await expect(page.getByRole('button', { name: '削除：部分往復テスト' })).toHaveCount(0);

  await page.selectOption('#settingsImportMode', 'strict');
  await page.setInputFiles('#content input[type="file"]', file);
  await expectNotified(page, 'インポート');

  await expect(page.getByRole('button', { name: '削除：部分往復テスト' }),
    '部分 export したプロジェクトが import で戻らない (素の配列を受け付けていない)').toBeVisible();
});

// 認識できない形は **エラーとして伝える**。silent no-op に成功メッセージを付けない。
test('認識できない形式の JSON は成功と report しない', async ({ page }, testInfo) => {
  const fs = require('fs');
  const path = require('path');
  const bad = path.join(testInfo.outputDir, 'unrecognized.json');
  fs.mkdirSync(testInfo.outputDir, { recursive: true });
  fs.writeFileSync(bad, JSON.stringify({ somethingElse: 1 }));

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.setInputFiles('#content input[type="file"]', bad);

  await expectNotified(page, '認識できない形式');
  const ann = await page.evaluate(() => (document.getElementById('action-announcement') || {}).textContent);
  expect(ann, '認識できない形式なのに「完了しました」と報告している').not.toContain('完了');
});

// ===== 「対象」の選択で中身が全部落ちるファイルも、成功と report しない =====
// #1039 で「形を認識できないファイル」の silent no-op は塞いだが、**形は認識できるのに
// 「対象」チェックボックスの選択で全部落ちる**残り半分が空いていた (実測 #1040:
// `AppsDataのみ` のファイルを AppsData のチェックを外した状態で読み込むと、タスクは
// 1 件も置き換わらないのに「インポートが完了しました」)。どちらも利用者からは
// 「バックアップを戻したのに戻っていない」としか見えない。
//
// このテストは同時に `AppsDataのみ` の形 (素の appsData オブジェクト) を import が
// 受け付けることも固定する —— #1039 の e2e は `Projectsのみ` の枝しか通っておらず、
// 残り 2 枝は誰も踏んでいなかった。
test('対象から外した形の import を成功と report しない', async ({ page }) => {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await page.getByLabel('新しいタスクを入力').fill('IMPORT-SHAPE-A');
  await page.getByLabel('新しいタスクを入力').press('Enter');
  await expect(page.locator('#content').getByText('IMPORT-SHAPE-A')).toBeVisible();

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'AppsDataのみ', exact: true }).click(),
  ]);
  const file = await download.path();

  // AppsData を「対象」から外す。この状態でファイルの中身は全部落ちる。
  // checkbox の onchange は window.render() で settings ページ全体を再描画し file input を
  // 作り直すので、状態を assert して settle を保証してから先へ進む (detach された古い input に
  // file を set すると onchange が発火せず import が起きない race がある・CI 負荷下で間欠 fail)。
  await page.locator('#settingsIncludeApps').uncheck();
  await expect(page.locator('#settingsIncludeApps')).not.toBeChecked();
  await expect(page.getByLabel('インポートする JSON ファイルを選択')).toBeVisible();

  // 別のタスクを足して状態を変えておく (import が効いたかを区別するため)
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await page.getByLabel('新しいタスクを入力').fill('IMPORT-SHAPE-B');
  await page.getByLabel('新しいタスクを入力').press('Enter');
  await expect(page.locator('#content').getByText('IMPORT-SHAPE-B')).toBeVisible();

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  expect(await page.locator('#settingsIncludeApps').isChecked(),
    'control: 対象から外れていなければ、この経路を測れない').toBe(false);
  await page.setInputFiles('#content input[type="file"]', file);

  await expectNotified(page, '対象');
  const ann = await page.evaluate(() => (document.getElementById('action-announcement') || {}).textContent);
  expect(ann, '中身が全部落ちたのに「完了しました」と報告している').not.toContain('完了');

  // 実際に何も適用されていないこと (B が残り、A に巻き戻っていない)
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await expect(page.locator('#content').getByText('IMPORT-SHAPE-B')).toBeVisible();

  // 対象に戻せば、同じファイルが今度は実際に適用される (AppsDataのみ の形を受け付ける)
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.locator('#settingsIncludeApps').check();
  await expect(page.locator('#settingsIncludeApps')).toBeChecked();
  // [FIX] ここで直に setInputFiles すると **CI でだけ間欠 RED** になる (実測: 通知が前の
  //   「対象の選択に一致するデータが…」のまま = change が発火していない)。checkbox の
  //   onchange は window.render() で settings ページ全体を再描画して file input を作り直すが、
  //   その再描画は非同期 (await yieldToMain) なので、checkbox の状態 assert が通った時点では
  //   まだ古い input が生きている。そこへ file を set すると、**直後に detach されて change が
  //   誰にも届かない**。上の 1 回目の import と同じく **一度ルートを離れて戻り**、描画が
  //   確定した DOM を掴んでから set する (「対象」は factory closure state なので遷移で消えない)。
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  expect(await page.locator('#settingsIncludeApps').isChecked(),
    'control: 対象に戻っていなければ、適用される経路を測れない').toBe(true);
  await page.setInputFiles('#content input[type="file"]', file);
  await expectNotified(page, 'インポートが完了しました');

  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await expect(page.locator('#content').getByText('IMPORT-SHAPE-A'),
    'AppsDataのみ の形が import で受け付けられていない').toBeVisible();
  await expect(page.locator('#content').getByText('IMPORT-SHAPE-B'),
    'appsData が置き換わっていない (import 後のタスクが export 時点のものになっていない)').toHaveCount(0);
});

// ===== 「モード」/「対象」の切替はページを作り直さない =====
// これらのコントロールの値は import 実行時にしか読まれず、選択状態はブラウザが自分で
// 更新するので、onchange で `window.render()` を呼んでも得るものが無い。むしろ
// **#content ごと作り直されて隣の file input が差し替わる**ため、「対象を変えてすぐ
// ファイルを選ぶ」という自然な操作で change が古い input に飛び、**import が起きない**。
// 実際 CI で 2 度 RED になった (#1040 / #1053)。加えて focus も一度失われ、_renderCore が
// id を鍵に戻す往復が必要になっていた (再描画しなければそもそも失われない・WCAG 2.1.1)。
//
// 「再描画されないこと」は目視でも既存テストでも観測できない (結果だけ見れば同じ) ので、
// **要素の同一性**を直接見る。data 属性の印が生き残れば作り直されていない。
// 非 vacuity: onchange に window.render() を戻すと印が消えて RED (実測)。
test('モード / 対象の切替でページが作り直されない (file input の同一性が保たれる)', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  const mark = () => page.evaluate(() => {
    document.querySelector('#content input[type="file"]').dataset.identityProbe = 'KEEP';
  });
  // [FIX] **settle させてから 1 度だけ読む**。ここは「再描画が起きない」という *不変性* の
  //   検査で、`window.render()` は `await yieldToMain()` を挟む **非同期**。切替直後に読むと
  //   再描画が始まる前の古いノードを掴み、**再描画が起きていても KEEP のまま通る**。
  //   実測 (2026-08-17): ローカルでは再描画が先に終わって捕捉できたが、週次 probe (CI) では
  //   読み取りが先になり **SURVIVED** として報告された —— 同じ mutation が環境で結果を変える
  //   race だった。rAF を 2 回待って「起きるなら起ききった」状態にしてから読む
  //   (poll は不変性の検査には使えない: 最初の観測で成立した瞬間に成功してしまう)。
  const settle = () => page.evaluate(() => new Promise(
    (r) => requestAnimationFrame(() => requestAnimationFrame(r))
  ));
  const survives = async () => {
    await settle();
    return page.evaluate(() => (
      document.querySelector('#content input[type="file"]').dataset.identityProbe || '(recreated)'
    ));
  };

  // 「対象」チェックボックス
  await mark();
  await page.locator('#settingsIncludeApps').uncheck();
  await expect(page.locator('#settingsIncludeApps')).not.toBeChecked();  // control: 実際に切り替わった
  expect(await survives(), '対象の切替で file input が作り直されている').toBe('KEEP');
  // 再描画されないので focus も失われない (従来は _renderCore が id で戻していた)
  expect(await page.evaluate(() => document.activeElement && document.activeElement.id))
    .toBe('settingsIncludeApps');

  // 「モード」セレクト
  await mark();
  await page.locator('#settingsImportMode').selectOption('strict');
  await expect(page.locator('#settingsImportMode')).toHaveValue('strict');  // control
  expect(await survives(), 'モードの切替で file input が作り直されている').toBe('KEEP');
});


// ===== 上限超過の import は「完了しました」で済ませない =====
// 正規化は (a) 件数上限 (MAX_TASKS 500) の slice と (b) 必須フィールドを欠く entry の除去、の
// 2 つで entry を落とす。従来はどちらの場合も無条件に「インポートが完了しました」と報告して
// おり、実測 (2026-08-18) では 505 件の tasks を取り込むと保存は 500 件で **5 件が黙って消え**、
// メッセージは「完了しました」だった。バックアップから復元した利用者は **失われたことに
// 気付かないまま元データを捨てうる**。#1039/#1040 で塞いだ「何もしていないのに成功と言う」の
// *部分適用* 版で、silent なのは同じ。
//
// 検査先に #action-announcement を選ぶ理由: Toast は duration で自動消滅するため、そちらを
// 待つ形は「実装内部の定数への賭け」になる (落とし穴表に記録済)。
test('Over-limit import reports how many entries were dropped instead of claiming plain success', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByRole('button', { name: 'フルバックアップ' })).toBeVisible();

  const announcement = () => page.evaluate(
    () => (document.getElementById('action-announcement') || {}).textContent || '');

  // control: 上限内なら従来どおり素の完了メッセージ (この control が無いと、
  //   「常に件数を付ける」実装でも下の assertion が通ってしまう)
  const within = Array.from({ length: 3 }, (_, i) => ({ id: 'w' + i, title: 'W' + i, status: 'todo' }));
  await page.setInputFiles('input[type=file]', {
    name: 'within.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ tasks: within, todos: [], notes: '', ai: {}, pomodoro: {} })),
  });
  await expect.poll(announcement, { timeout: 5000 }).toContain('インポートが完了しました');
  expect(await announcement(), '上限内なのに件数が付いている').not.toContain('取り込めませんでした');

  // 上限 (500) を 5 件超える取り込み → 落ちた件数が伝わる
  const over = Array.from({ length: 505 }, (_, i) => ({ id: 'o' + i, title: 'O' + i, status: 'todo' }));
  await page.setInputFiles('input[type=file]', {
    name: 'over.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ tasks: over, todos: [], notes: '', ai: {}, pomodoro: {} })),
  });
  await expect.poll(announcement, { timeout: 5000 }).toContain('取り込めませんでした');
  expect(await announcement()).toContain('5 件');
});

// ===== entry は残るのに「中身」だけ上限で削られる分も報告すること =====
// #1143 は件数上限で **entry ごと**落ちる分を数えるようにしたが、*取り込まれた* project の
// tech/tags/highlights (12/12/20) や task の tags (10) が削られる面は 0 のままだった。
// 実測 (2026-08-20): tech 20 / tags 20 / highlights 30 を持つ project を取り込むと
// 12/12/20 になり **26 項目が消える**のに通知は素の「インポートが完了しました」。
// entry ごと消えるより気付く手掛かりが薄い (一覧には出るので「戻った」ように見える)。
test('取り込んだ project の中身が上限で削られたら件数を報告する', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  await page.setInputFiles('#content input[type="file"]', {
    name: 'trim.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      schemaVersion: 12,
      projects: [{
        id: 'trim-1', name: 'TRIM-PROJ', slug: 'trim-proj', summary: 'x', category: 'AI',
        tech: Array.from({ length: 20 }, (_, i) => `T${i}`),
        tags: Array.from({ length: 20 }, (_, i) => `G${i}`),
        highlights: Array.from({ length: 30 }, (_, i) => `H${i}`),
      }],
    })),
  });

  await expectNotified(page, 'インポートが完了しました');

  // control: そもそも切り捨てが起きていなければ、この通知を検査する意味がない。
  await expect.poll(async () => await page.evaluate(() => {
    const raw = localStorage.getItem('portfolio_enhanced_v45');
    if (!raw) { return -1; }
    const p = (JSON.parse(raw).projects || []).find((x) => x.name === 'TRIM-PROJ');
    return p ? p.tech.length + p.tags.length + p.highlights.length : -1;
  }), 'control: 上限で削られていない (44 = 12+12+20)').toBe(44);

  const ann = await page.evaluate(
    () => document.getElementById('action-announcement').textContent
  );
  expect(ann, '26 項目が消えたのに素の「完了しました」と報告している').toContain('26 件');
});

// ===== 文字数上限で「短縮」された項目も報告すること =====
// 直前のテストが数える _trimmed は list の *件数* だけを見るため、name/summary/title 等の
// 文字列が上限で切られる面は 0 のままだった。実測 (2026-08-20): name 300 文字 /
// summary 900 文字の project を取り込むと 120 / 800 になり **280 文字が消える**のに
// 素の「インポートが完了しました」。#1177 は *手動追加* で既に短縮を報告しており、
// 取り込み経路だけが取り残されていた非対称。
test('取り込んだ項目が文字数上限で短縮されたら件数を報告する', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  await page.setInputFiles('#content input[type="file"]', {
    name: 'short.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      schemaVersion: 12,
      projects: [{
        id: 'short-1', name: 'N'.repeat(300), slug: 'short-proj',
        summary: 'S'.repeat(900), category: 'AI',
      }],
    })),
  });

  await expectNotified(page, 'インポートが完了しました');

  // control: そもそも短縮が起きていなければ、この通知を検査する意味がない。
  await expect.poll(async () => await page.evaluate(() => {
    const raw = localStorage.getItem('portfolio_enhanced_v45');
    if (!raw) { return -1; }
    const p = (JSON.parse(raw).projects || []).find((x) => x.slug === 'short-proj');
    return p ? p.name.length + p.summary.length : -1;
  }), 'control: 上限で短縮されていない (920 = 120+800)').toBe(920);

  const ann = await page.evaluate(
    () => document.getElementById('action-announcement').textContent
  );
  expect(ann, '280 文字が消えたのに素の「完了しました」と報告している').toContain('2 件の項目');
});

// 前後の空白の trim は「上限による損失」ではないので短縮として報告しない。
// profile の email / github / linkedin は safeEmail / safeUrl が **trim 後の値を返す**ため、
// ガードが無いと前後に空白があるだけのごく普通のファイルで毎回「短縮されました」と誤報し、
// **本物の切り捨て警告が信用されなくなる**。
test('前後の空白を落としただけでは短縮として報告しない', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  await page.setInputFiles('#content input[type="file"]', {
    name: 'ws.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      schemaVersion: 12,
      profile: { email: '  ws-probe@example.com  ', github: '  https://example.com/ws  ' },
    })),
  });

  await expectNotified(page, 'インポートが完了しました');

  // control: そもそも trim が起きていなければ、誤報しないことを測れていない。
  await expect.poll(async () => await page.evaluate(() => {
    const raw = localStorage.getItem('portfolio_enhanced_v45');
    if (!raw) { return null; }
    return (JSON.parse(raw).profile || {}).email || null;
  }), 'control: trim されていない').toBe('ws-probe@example.com');

  const ann = await page.evaluate(
    () => document.getElementById('action-announcement').textContent
  );
  expect(ann, '空白の trim を「短縮」と誤報している').not.toContain('短縮');
});
