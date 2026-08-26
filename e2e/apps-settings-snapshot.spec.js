const { test, expect } = require('@playwright/test');

// スナップショット (単一スロットの復元点) に関する behavior。apps-settings.spec.js が
// advisory 行数を超えたため、テーマの塊としてここへ切り出した (#1067 の教訓: advisory は
// BLOCKING を踏む前に効かせる)。保存 / 由来表示 / 削除 / 未保存時の disabled を扱う。

// ===== 7.2: 設定アプリのスナップショット保存→反映 Behavior Check =====
// #/settings の「保存」は setSnapshot() で Storage.set(SNAPSHOT_KEY, ...) し、再描画後に
// getSnapshot()(=Storage.parse) が読み戻して「保存日時: …」を表示する。これは PR #93 で
// 注入漏れを修正した Storage 依存 (set/parse) の往復を実際に通す data-integrity パスで、
// 修正前は Storage.parse が render 時に throw して到達すらできなかった経路。
test('Settings app saves a snapshot and reflects the saved-at status', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 初期 (fresh context) は未保存
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();

  // 保存 → Storage.set → 再描画 → getSnapshot(Storage.parse) が読み戻し「保存日時:」表示
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByText(/保存日時:/)).toBeVisible();

  // リロード後も Storage から読み戻せる (永続)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText(/保存日時:/)).toBeVisible();
});


// ===== 7.2b: スナップショットの由来を出す =====
// 保存日時だけでは、**自分が保存したもの**か**データ形式の変更時に自動退避されたもの**かを
// 区別できない。自動退避は store.load() の中で走るため確認を挟めず、手動保存を黙って上書き
// する。移行通知が「Settings のスナップショットから復元できます」と誘導する以上、そこで区別
// できないと利用者は「自分の復元点が残っている」と誤解したまま復元して別物を戻してしまう。
test('スナップショットは手動保存と自動退避を区別して表示する', async ({ page }) => {
  // (1) 手動保存
  await page.goto('/#/settings');
  await expect(page.locator('#settings-snapshot-save')).toBeVisible();
  await page.locator('#settings-snapshot-save').click();
  await expect(page.getByText('手動で保存')).toBeVisible();

  // control: 由来の文言が固定文字列ではなく実際の中身から出ている
  await expect(page.getByText('データ形式の変更')).toHaveCount(0);
});

test('自動退避されたスナップショットは移行元と移行先を示す', async ({ page }) => {
  await page.addInitScript(() => {
    try {
      localStorage.setItem('portfolio_enhanced_v45', JSON.stringify({
        schemaVersion: 1, type: 'full-store', theme: 'system', appsData: { tasks: [] }
      }));
    } catch (e) { /* noop */ }
  });
  await page.goto('/#/settings');
  await expect(page.locator('#settings-snapshot-restore')).toBeVisible();

  // control: 実際に自動退避が起きている (起きていなければ「手動で保存」が正しく、検査が vacuous)
  const reason = await page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('portfolio_snapshot_v45')).reason; } catch { return null; }
  });
  expect(reason, 'control: auto-snapshot must exist').toBe('schema-mismatch');

  await expect(page.getByText('データ形式の変更 v1→v')).toBeVisible();
  await expect(page.getByText('手動で保存')).toHaveCount(0);
});

// ===== 7.2: スナップショット削除 (clearSnapshot → 未保存へ復帰) =====
// clearSnapshot は Storage.remove(SNAPSHOT_KEY) + 再描画で「未保存」状態へ戻す。save/restore は
// 被覆済みだが clear (snapshot ライフサイクルの最後) は未カバーだった。snapshot 削除ボタンは
// btn-ghost (プロジェクト削除の btn-danger とは別) で識別する。保存→削除で「未保存」表示へ戻り、
// リロード後も未保存が永続することを実検証し snapshot ライフサイクル (save/restore/clear) を完成させる。
test('Settings snapshot can be cleared back to the unsaved state', async ({ page }) => {
  await page.goto('/#/settings');
  await page.waitForLoadState('domcontentloaded');

  // 保存 → 保存日時表示
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByText(/保存日時:/)).toBeVisible();

  // 削除 (snapshot clear = btn-ghost の「削除」。project 削除は btn-danger なので衝突しない)
  // NOTE: スナップショット削除は confirm を通す (唯一の復元点ゆえ他の破壊的操作と対称にした)。
  //   Playwright は dialog を既定で dismiss する = 承認しないと削除自体が起きないため、
  //   「削除できること」を検証する本 test では明示的に accept する。
  page.once('dialog', (d) => d.accept());
  await page.locator('button.btn-ghost', { hasText: '削除' }).click();
  await expect(page.locator('#toast-container').getByText('スナップショットを削除しました')).toBeVisible();

  // 未保存状態へ復帰
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();
  await expect(page.getByText(/保存日時:/)).toHaveCount(0);

  // リロード後も未保存 (clear が永続)
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();
});


// ===== 7.2: snapshot の 復元/削除 ボタンが未保存時 disabled (disabled affordance) =====
// 復元/削除ボタンは `disabled: !snap` で snapshot 未保存時は無効。restoreSnapshot/clearSnapshot は
// snap 不在時 no-op だが、disabled 属性はユーザへの「まだ復元/削除するものが無い」affordance で、
// 外れると空 snapshot に対し操作できるように見える UX 退行になる。既存の snapshot テストは save/
// restore/clear の flow と「未保存です」表示は見るが、この disabled 状態は未カバーだった。未保存→
// 両ボタン disabled、保存→有効、削除→再び disabled の遷移を検証する。
test('Snapshot restore/clear buttons are disabled until a snapshot exists (affordance)', async ({ page }) => {
  await page.goto('/#/settings', { waitUntil: 'domcontentloaded' });
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();

  const restoreBtn = page.getByRole('button', { name: '復元', exact: true });
  const clearBtn = page.locator('button.btn-ghost', { hasText: '削除' });
  // 未保存: 両ボタン disabled。
  await expect(restoreBtn).toBeDisabled();
  await expect(clearBtn).toBeDisabled();

  // 保存 → 両ボタン有効。
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.locator('#toast-container').getByText('スナップショットを保存しました')).toBeVisible();
  await expect(restoreBtn).toBeEnabled();
  await expect(clearBtn).toBeEnabled();

  // 削除 → 未保存へ戻り両ボタン再び disabled。
  // confirm を承認する (既定の dismiss では削除が起きず affordance も変化しない)。
  page.once('dialog', (d) => d.accept());
  await clearBtn.click();
  await expect(page.getByText('スナップショットは未保存です。')).toBeVisible();
  await expect(restoreBtn).toBeDisabled();
  await expect(clearBtn).toBeDisabled();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `snapshot affordance caused a fatal: ${fatal}`).toBeNull();
});
