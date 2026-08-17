const { test, expect } = require('@playwright/test');

// ===== プロジェクトデータの往復忠実性 (round-trip fidelity) =====
// 「保存 → 読み戻し」を跨いでも既定データが変質しないことを固定する。
//
// projects.spec.js から切り出した理由は肥大化の**予防**。同 file が 922 行となり早期警告
// (900) を超えたため、Check 365 の BLOCKING (1,000 行) を踏む前にこのテーマの塊を移した
// (CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。
// mutation の `test` フィールドは title 一致ゆえ file 移動の影響を受けない。

// ===== 既定プロジェクトが「保存 → 読み戻し」を繰り返しても変質しない (normalize の冪等性) =====
// 利用者が何か操作するたび store 全体が `validateAndNormalize` を通って localStorage へ
// 書かれ、次回以降はそれが読み戻される。**normalize が冪等でないと、操作するたびに
// データが少しずつ変質していく** —— 例えば slug 重複解消が自分自身を衝突とみなすと、
// 保存のたび `-2` が伸びて **既存のブックマークや共有リンクが全部 404 になる**。
//
// 落ちても fatal は出ず、視覚 baseline は ADVISORY で、そもそも「元々そう書いてあった」
// ようにしか見えないので、**この behavior test 以外に捕捉層が無い**。
// 過去に近い class が実バグ化している (#154 slug 衝突 / #782 relatedProjectIds の
// String 正規化不一致)。
//
// **このテストが検出しないもの (実測して確認・誤解防止)**: 「normalize が既定データの
// フィールドを落とす」class は検出**できない**。起動時の `State.load()` も同じ normalize を
// 通すので、比較する両辺がどちらも正規化後になるため (実測: `tech: []` に潰す mutation を
// 当てても両辺が同じく空になり緑のままだった)。落とす class は import 往復テスト
// (#1035〜#1040) と、そのフィールドを実際に描画するページの個別テストが担当する。
//
// 測定の作り方 (実測で 2 度誤診した):
//   - スラッグは store.js の既定値から取る。実在しないスラッグは NotFound を返し、
//     それでも「ページは描画された」ように見えるので control で弾く
//   - hash 遷移は document を作り直さないので、**各ページで reload してフルロードする**。
//     しないと前ページの DOM を読み、2,232 文字のはずが一覧の 2,272 文字を掴む
const ROUNDTRIP_SLUGS = ['task-manager', 'todo-list', 'pomodoro-timer', 'unified-data-model', 'offline-sync-notes'];

async function snapshotProjectDetails(page) {
  const out = [];
  for (const slug of ROUNDTRIP_SLUGS) {
    await page.goto('/#/projects/' + slug);
    await page.reload();
    await expect(page.locator('#content h1').first()).toBeVisible();
    const text = await page.evaluate(() => (document.querySelector('#content') || {}).innerText.replace(/\s+/g, ' '));
    // control: NotFound を掴んでいない (掴むと「短いが描画された」だけで通ってしまう)
    // このスラッグが引けないのは (a) 一覧の既定スラッグが変わった か
    //   (b) **normalize が保存のたびに slug を書き換えている (非冪等)** のどちらか。
    //   後者は「ブックマークが全部 404 になる」形で利用者に出る。
    expect(text,
      `${slug} の詳細ページが引けない — 既定スラッグが変わったか、normalize が保存のたびに `
      + 'slug を書き換えている (非冪等・共有リンクが 404 になる)')
      .not.toContain('プロジェクトが見つかりません');
    out.push(slug + '::' + text);
  }
  return out.join('\n');
}

test('既定プロジェクトの詳細が保存と読み戻しを跨いで変質しない', async ({ page }) => {
  const before = await snapshotProjectDetails(page);
  expect(before.length, 'control: 詳細ページの内容が取れていない').toBeGreaterThan(1000);

  // 何か 1 つ操作すると store 全体が normalize されて保存される (テーマ切替が最小の操作)
  await page.goto('/#/projects');
  await page.reload();
  await expect(page.locator('#content h1').first()).toBeVisible();
  await page.locator('#themeBtnSidebar').click();
  await expect
    .poll(() => page.evaluate(() => !!localStorage.getItem('portfolio_enhanced_v45')))
    .toBe(true);

  const after = await snapshotProjectDetails(page);
  expect(after,
    '初回保存 → 読み戻しで既定プロジェクトの内容が変わった — normalize がフィールドを '
    + '落としている疑い。落ちても fatal は出ず「元々そう書いてあった」ようにしか見えない'
  ).toBe(before);
});
