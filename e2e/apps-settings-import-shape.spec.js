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

// モード (追加のみ / 更新+追加 / 全置換) を選ぶ。onchange は window.render() で settings
// ページを作り直すため、選んだ直後に setInputFiles すると **detach された古い input を掴み
// change が誰にも届かない** (このファイル冒頭の import と同じ落とし穴)。一度ルートを離れて
// 戻り、描画が確定した DOM を掴んでから使う。モードは factory closure state ゆえ遷移で消えない。
async function selectImportMode(page, mode) {
  await page.locator('#content select').first().evaluate((el, m) => {
    el.focus();
    el.value = m;
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }, mode);
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  expect(await page.locator('#content select').first().inputValue(),
    'control: モードが選択されていなければ、その意味論を測れない').toBe(mode);
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
  // このテストが測るのは「復元/上限」の意味論なので全置換モードで測る (既定の
  // 「追加のみ」は既存を残す = 置き換え/切り詰めが起きず、測りたい性質に到達しない)。
  await selectImportMode(page, 'strict');
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

  // このテストが測るのは「復元/上限」の意味論なので全置換モードで測る (既定の
  // 「追加のみ」は既存を残す = 置き換え/切り詰めが起きず、測りたい性質に到達しない)。
  await selectImportMode(page, 'strict');

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

  // このテストが測るのは「復元/上限」の意味論なので全置換モードで測る (既定の
  // 「追加のみ」は既存を残す = 置き換え/切り詰めが起きず、測りたい性質に到達しない)。
  await selectImportMode(page, 'strict');
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

// ===== Markdown ノートの切り詰めと履歴の件数落ちも報告すること =====
// notes は**単一ドキュメント**なので上限 (20,000) を超えると末尾がまるごと消えるが、
// entry も件数も減らないため全カウンタが 0 のままだった。ai.history (80) /
// pomodoro.history (200) の entry 落ちも tasks/todos/projects しか数えておらず未計上。
// 実測 (2026-08-20): notes 30,000 文字 + ai.history 100 件を取り込むと 20,000 / 80 になり
// **10,000 文字と 20 件が消える**のに通知は素の「インポートが完了しました」。
test('ノートの切り詰めと履歴の件数落ちを報告する', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();

  // このテストが測るのは「復元/上限」の意味論なので全置換モードで測る (既定の
  // 「追加のみ」は既存を残す = 置き換え/切り詰めが起きず、測りたい性質に到達しない)。
  await selectImportMode(page, 'strict');
  await page.setInputFiles('#content input[type="file"]', {
    name: 'apps.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      tasks: [],
      todos: [],
      notes: 'N'.repeat(30000),
      ai: {
        history: Array.from({ length: 100 }, (_, i) => ({
          prompt: `p${i}`, response: `r${i}`, timestamp: 1,
        })),
      },
    })),
  });

  await expectNotified(page, 'インポートが完了しました');

  // control: そもそも上限に当たっていなければ、この通知を検査する意味がない。
  await expect.poll(async () => await page.evaluate(() => {
    const raw = localStorage.getItem('portfolio_enhanced_v45');
    if (!raw) { return null; }
    const a = JSON.parse(raw).appsData;
    return `${(a.notes || '').length}/${(a.ai.history || []).length}`;
  }), 'control: 上限で削られていない (20000 文字 / 80 件)').toBe('20000/80');

  const ann = await page.evaluate(
    () => document.getElementById('action-announcement').textContent
  );
  expect(ann, '履歴 20 件が落ちたのに報告していない').toContain('20 件は取り込めませんでした');
  expect(ann, 'ノート 10,000 文字が消えたのに報告していない').toContain('1 件の項目');
});

// ===== 「対象」モードは appsData にも効くこと =====
// モード (追加のみ / 更新+追加 / 全置換) は **projects にしか効いておらず**、appsData は
// どのモードでも丸ごと置き換えていた。既定の「追加のみ」で AppsData を含むファイルを
// 取り込むと **既存のタスク・TODO・ノート・履歴が全部消える** (実測 2026-08-20)。
// 「追加のみ」は「既存を壊さない」という約束なので、**最も安全なつもりの選択が
// 最も破壊的**だった。3 モードの意味論をまとめて固定する。
async function seedAndImport(page, mode, payload) {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  await page.getByLabel('新しいタスクを入力').fill('EXISTING-TASK');
  await page.getByLabel('新しいタスクを入力').press('Enter');
  await expect(page.locator('#content').getByText('EXISTING-TASK')).toBeVisible();

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await selectImportMode(page, mode);

  await page.setInputFiles('#content input[type="file"]', {
    name: 'a.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(payload)),
  });
  await expect(page.locator('#action-announcement')).toContainText('インポート');
}

const IMPORTED = {
  tasks: [{ id: 'imp1', title: 'IMPORTED-TASK', status: 'todo' }],
  todos: [],
  notes: 'IMPORTED-NOTE',
};

// 保存は debounce (150ms) なので import 直後に localStorage を読むと **古い値**が返る
// (実装中に実測で踏んだ)。描画された DOM を auto-retry する assertion で見る。
// 同じモードのまま追加で取り込む (モードは factory closure state ゆえ遷移で消えない)。
async function importAgain(page, payload) {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.setInputFiles('#content input[type="file"]', {
    name: 'b.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(payload)),
  });
}

async function expectTasks(page, present, absent) {
  await page.goto('/#/apps/task', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'タスク' }).first()).toBeVisible();
  for (const t of present) {
    await expect(page.locator('#content').getByText(t, { exact: true })).toBeVisible();
  }
  for (const t of absent) {
    await expect(page.locator('#content').getByText(t, { exact: true })).toHaveCount(0);
  }
}

async function notesValue(page) {
  await page.goto('/#/apps/notes', { waitUntil: 'domcontentloaded' });
  const ta = page.locator('#content textarea').first();
  await expect(ta).toBeVisible();
  return await ta.inputValue();
}

test('「追加のみ」の import は既存タスクを消さない', async ({ page }) => {
  await seedAndImport(page, 'append', IMPORTED);
  const ann = await page.evaluate(
    () => document.getElementById('action-announcement').textContent
  );
  expect(ann, '既存を優先して取り込まなかったことを報告していない').toContain('既存を残しました');
  await expectTasks(page, ['EXISTING-TASK', 'IMPORTED-TASK'], []);
  // 追加のみ ではノートは既存を優先する (上で「残しました」と報告済み)。
  expect(await notesValue(page), '「追加のみ」なのにノートが上書きされた').not.toBe('IMPORTED-NOTE');

  // id が衝突したときの意味論。「追加のみ」は既存を**更新しない**。
  await importAgain(page, { tasks: [{ id: 'imp1', title: 'OVERWRITTEN', status: 'todo' }], todos: [] });
  await expectTasks(page, ['IMPORTED-TASK'], ['OVERWRITTEN']);
});

test('「更新+追加」の import は既存を残しつつ取り込む', async ({ page }) => {
  await seedAndImport(page, 'upsert', IMPORTED);
  await expectTasks(page, ['EXISTING-TASK', 'IMPORTED-TASK'], []);
  expect(await notesValue(page), '「更新+追加」ならノートは取り込んだ値になる').toBe('IMPORTED-NOTE');

  // id が衝突したときの意味論。「更新+追加」は既存を**更新する** (append との差)。
  await importAgain(page, { tasks: [{ id: 'imp1', title: 'OVERWRITTEN', status: 'todo' }], todos: [] });
  await expectTasks(page, ['OVERWRITTEN'], ['IMPORTED-TASK']);
});

test('「全置換」の import は宣言どおり丸ごと置き換える', async ({ page }) => {
  await seedAndImport(page, 'strict', IMPORTED);
  // control: 置き換えが起きていなければ、他 2 モードとの違いを測れていない。
  await expectTasks(page, ['IMPORTED-TASK'], ['EXISTING-TASK']);
  expect(await notesValue(page)).toBe('IMPORTED-NOTE');
});

// ===== 「追加のみ」で既存を残した報告は、実際に違うときだけ出すこと =====
// #1183 で足した「N 件の項目は「追加のみ」のため既存を残しました」は、**内容が同じでも**
// 出ていた。実測 (2026-08-20): 現在のノートと完全に同じ内容のファイルを取り込むと
// 「1 件の項目は…既存を残しました」と報告する —— 何も失っていないのに警告が出る。
// 失っていないのに警告を出すと **本物の切り捨て警告が信用されなくなる** (#1181 と同じ理由)。
test('内容が同じなら「既存を残しました」と報告しない', async ({ page }) => {
  await page.goto('/#/apps/notes', { waitUntil: 'domcontentloaded' });
  const ta = page.locator('#content textarea').first();
  await expect(ta).toBeVisible();
  const current = await ta.inputValue();
  expect(current.length, 'control: ノートが空だと「同じ内容」を作れない').toBeGreaterThan(0);

  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.setInputFiles('#content input[type="file"]', {
    name: 'same.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ tasks: [], todos: [], notes: current })),
  });

  await expectNotified(page, 'インポートが完了しました');
  const ann = await page.evaluate(
    () => document.getElementById('action-announcement').textContent
  );
  expect(ann, '何も失っていないのに「既存を残しました」と警告している').not.toContain('既存を残しました');
});

// 逆方向: 実際に違うときは従来どおり報告する (上のテストだけだと
// 「常に報告しない」実装でも通ってしまう)。
test('内容が違えば「既存を残しました」と報告する', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Settings' })).toBeVisible();
  await page.setInputFiles('#content input[type="file"]', {
    name: 'diff.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      tasks: [], todos: [], notes: 'これは現在のノートとは違う内容です',
    })),
  });

  await expectNotified(page, 'インポートが完了しました');
  const ann = await page.evaluate(
    () => document.getElementById('action-announcement').textContent
  );
  expect(ann, '実際に取り込まなかったのに報告していない').toContain('既存を残しました');
});
