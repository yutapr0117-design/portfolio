const { test, expect } = require('@playwright/test');


// ===== 7.2: AI アシストアプリの応答生成 Behavior Check =====
// #/apps/ai は #ai-input + 「送信」で submit() → analyzeInput → (300ms 後) generateResponse +
// State.update で appsData.ai.history に push し再描画する。task/todo とは別 State slice・別ロジック
// (ローカル生成・非同期 setTimeout) の distinct な対話パス。送信した prompt が履歴に現れることで
// submit→生成→State 反映→render の一連が壊れていないことを動的検証する。
test('AI assist app generates and renders a response for a prompt', async ({ page }) => {
  await page.goto('/#/apps/ai');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#ai-input');
  await expect(input).toBeVisible();
  const prompt = 'E2E-AI-PROMPT-デプロイ手順-5512';
  await input.fill(prompt);
  await page.getByRole('button', { name: '送信', exact: true }).click();

  // 生成完了後、prompt が history (テキスト) として描画される (input value ではなく本文)
  await expect(page.getByText(prompt)).toBeVisible();
});


// ===== 7.2: Markdown ノートアプリ (innerHTML 不使用のライブプレビュー + 永続) =====
// js/apps.js NotesPage は textarea の Markdown を h() のみ（innerHTML 不使用）で DOM へレンダリングし
// live preview + localStorage 永続する純追加アプリ。# 見出し / **太字** / `code` / - リストを
// h('h1'/'strong'/'code'/'li') へ変換する。入力→プレビュー反映→リロード永続を検証する。
test('Markdown notes app live-previews (innerHTML-free) and persists', async ({ page }) => {
  await page.goto('/#/apps/notes');
  await page.waitForLoadState('domcontentloaded');

  const ta = page.locator('#notes-input');
  await expect(ta).toBeVisible();
  await ta.fill('# E2E-NOTE-見出し-7733\n\n**太字テキスト** と `inlineコード`\n\n- 項目A');

  // プレビューが h() で構造化レンダリング (innerHTML 不使用) されること。
  // [FIX] Markdown 見出しは 2 段 demote される (# → h3・preview の h2「プレビュー」配下に nest)。
  // 従来 `#` を <h1> で描画しページに h1 が 2 個 (app タイトル + note 見出し) 生じる heading-semantics
  // 崩れ (default note "# メモ" で out-of-the-box 発生) を是正。視覚サイズは 'h1' class 維持で不変。
  const preview = page.locator('.md-preview');
  await expect(preview.locator('h3', { hasText: 'E2E-NOTE-見出し-7733' })).toBeVisible();
  await expect(preview.locator('strong', { hasText: '太字テキスト' })).toBeVisible();
  await expect(preview.locator('code.md-code', { hasText: 'inlineコード' })).toBeVisible();
  await expect(preview.locator('ul.md-ul li', { hasText: '項目A' })).toBeVisible();
  // ページ h1 はアプリタイトル「Markdown ノート」の 1 個のみ (note 見出しは h1 に昇格しない)。
  // demote を戻すと note `#` が <h1> になり h1 が 2 個 → RED = 非 vacuity。
  await expect(page.locator('h1')).toHaveCount(1);
  await expect(preview.locator('h1')).toHaveCount(0);

  // リロード後も永続 (appsData.notes): preview AND textarea の両方を確認
  // [FIX] h() の textarea 特殊処理 (el.value = src) を追加するまで textarea は
  // setAttribute('value', ...) で attribute を書くだけで el.value は "" になっていた
  // (HTML spec: textarea に value content attribute は存在しない)。
  // 修正後は preview だけでなく textarea の value も永続する。
  await page.reload();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('.md-preview h3', { hasText: 'E2E-NOTE-見出し-7733' })).toBeVisible();
  // textarea の value が再描画後も復元されること (fix の regression gate)
  await expect(page.locator('#notes-input')).toHaveValue(/E2E-NOTE-見出し-7733/);

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `notes app caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: AI アシストの analyzeInput キーワード分岐 (troubleshoot/design/breakdown/writing/general) =====
// analyzeInput は入力に含まれるキーワードで応答タイプを 5 分岐する: 「エラー/バグ/失敗」→
// troubleshoot、「設計/計画/構成」→ design、「分解/タスク/手順/ステップ/段取り」→ breakdown、
// 「文章/書い/説明/ライティング/文言」→ writing、それ以外 → general。既存 AI テスト (#上) は
// prompt が履歴に出ることのみ見ており、この分類ロジック (generateResponse の type 別出力) は
// 未カバーだった。各キーワードで送信し、対応する応答マーカーが描画されることを実検証する。
// 分類ロジックが壊れたら (例: キーワード変更で全部 general に倒れる) 退行を捕まえる。
test('AI assist routes prompts to troubleshoot/design/breakdown/writing/general responses by keyword', async ({ page }) => {
  await page.goto('/#/apps/ai');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#ai-input');
  const submit = page.getByRole('button', { name: '送信', exact: true });

  // 「エラー」→ troubleshoot
  await expect(input).toBeVisible();
  await input.fill('本番でエラーが出た');
  await submit.click();
  await expect(page.getByText('[AI分析: トラブルシューティング]')).toBeVisible();

  // 「設計」→ design
  await input.fill('新機能の設計を相談したい');
  await submit.click();
  await expect(page.getByText('[AI分析: 設計支援]')).toBeVisible();

  // 「分解/タスク/手順」→ breakdown (placeholder が示唆する用途)
  await input.fill('デプロイ手順を分解して');
  await submit.click();
  await expect(page.getByText('[AI分析: タスク分解]')).toBeVisible();

  // 「文章/書い/説明」→ writing (placeholder が示唆する用途)
  await input.fill('説明文を書いて');
  await submit.click();
  await expect(page.getByText('[AI分析: 文章生成支援]')).toBeVisible();

  // キーワードなし → general
  await input.fill('こんにちは');
  await submit.click();
  await expect(page.getByText('[AI分析: 一般支援]')).toBeVisible();

  const fatal = await page.evaluate(() => (window.__fatalError ? window.__fatalError.message : null));
  expect(fatal, `AI assist branching caused a fatal: ${fatal}`).toBeNull();
});


// ===== 7.2: AI アシストの loading 状態機械 (送信→生成中→応答) =====
// submit() は aiLoading=true で即時再描画し、入力/送信を disabled にしてボタンを「生成中...」に変え、
// 300ms 後 (setTimeout) に generateResponse + aiLoading=false で「送信」へ戻す。分岐テストは応答内容を
// 見るが、この非同期 loading state machine (生成中表示 + disabled) は未カバーだった。fake clock で
// 300ms を決定的に制御し、loading 中→解決の遷移を検証する。
test('AI assist shows a loading state then resolves (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/ai');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#ai-input');
  await expect(input).toBeVisible();
  await input.fill('ローディング検証の質問');
  await page.getByRole('button', { name: '送信', exact: true }).click();

  // loading 中: ボタンが「生成中...」になり「送信」は消える
  await expect(page.getByRole('button', { name: '生成中' })).toBeVisible();
  await expect(page.getByRole('button', { name: '送信', exact: true })).toHaveCount(0);

  // 300ms 進める → 応答生成 + 「送信」へ復帰
  await page.clock.fastForward(300);
  await expect(page.getByRole('button', { name: '送信', exact: true })).toBeVisible();
  await expect(page.getByText('[AI分析:').first()).toBeVisible();
});


// ===== 7.2: Toast の自動消滅ライフサイクル (duration 経過で消える) =====
// Toast.show は duration(既定 3000ms) 後に remove() を呼び、さらに 300ms のアニメ後に DOM から
// 除去する (ui-components.js)。toast が表示される検証は多数あるが「時間経過で自動消滅する」
// ライフサイクルは未カバーだった (消えないと toast が画面に積み上がる UX バグ)。fake clock で
// duration+アニメ経過後に toast が消えることを決定的に検証する。
test('Toast auto-dismisses after its duration (deterministic clock)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  // タスク追加で success toast を発火
  const input = page.locator('#task-input');
  await input.fill('TOAST-DISMISS-TASK-9501');
  await input.press('Enter');
  const toast = page.locator('#toast-container').getByText('タスクを追加しました');
  await expect(toast).toBeVisible();

  // duration(3000) + remove アニメ(300) を超えて進める → 自動消滅
  await page.clock.fastForward(3500);
  await expect(toast).toHaveCount(0);
});


// ===== 7.2: アクションの sr-only aria-live 通知 (screen reader フィードバック・a11y) =====
// Toast.show は視覚 toast に加え #action-announcement (sr-only, aria-live=assertive) にも message を
// 書き込む。視覚 toast の検証は多数あるが、SR 利用者向け assertive 通知チャネルは未カバーだった。
// 通知領域が assertive aria-live を持つこと + アクションでメッセージが announce されることを検証する。
test('Actions announce to the assertive sr-only aria-live region (screen reader a11y)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');

  const live = page.locator('#action-announcement');
  await expect(live).toHaveAttribute('aria-live', 'assertive');

  // アクション (タスク追加) でメッセージが SR 通知領域に入る
  const input = page.locator('#task-input');
  await input.fill('SR-ANNOUNCE-TASK-9601');
  await input.press('Enter');
  await expect(live).toHaveText('タスクを追加しました');
});


// ===== 7.2: SPA ルート変更の sr-only aria-live 通知 (screen reader a11y) =====
// SPA はページ全体が再読込されないため、SR 利用者にルート変更を能動的に通知する必要がある
// (SPA a11y の既知要件)。#page-announcement (sr-only, aria-live=polite) はルート遷移ごとに
// RouteState の a11y_announcement バインディング (main.js, route.name ベースで「<route> ページを
// 表示中」) で更新される。視覚 title 更新 (別テスト) とは別チャネルで未カバーだった。route 遷移で
// polite 領域が現在 route 名に追従することを検証する。
test('Route changes announce to the polite sr-only aria-live region (SPA a11y)', async ({ page }) => {
  await page.goto('/#/projects');
  await page.waitForLoadState('domcontentloaded');

  const announcer = page.locator('#page-announcement');
  await expect(announcer).toHaveAttribute('aria-live', 'polite');
  await expect.poll(async () => (await announcer.textContent()) || '').toContain('projects');

  // 別ルートへ遷移すると announcement が現在 route 名に追従更新される
  await page.goto('/#/about');
  await page.waitForLoadState('domcontentloaded');
  await expect.poll(async () => (await announcer.textContent()) || '').toContain('about');
});


// ===== 7.2: 同一ページの State.update 再描画で route アナウンスを繰り返さない (over-announce 防止) =====
// applyMeta は _renderCore から呼ばれ、_renderCore は State.update 由来の「同一ページ再描画」
// (task 追加 / pomodoro tick 等) でも走る。従来 applyMeta は announceRouteForAccessibility を
// 無条件呼びしていたため、同一ページの状態変化のたびに #page-announcement へ「○○ページを
// 表示しています。」を再書き込みし、SR 利用者へ同じルート名を繰り返しアナウンスする over-announce
// ノイズ (WCAG 4.1.3 反パターン) を生んでいた。修正で applyMeta に isRouteChange を渡し、実ルート
// 遷移時のみ announce するよう gate した。本テストは「同一ページで 3 回 State.update しても
// route アナウンス (『表示しています』) が 1 度も再発火しない」ことを MutationObserver で検証する
// (fix を戻すと 3 回発火し RED = 非 vacuous)。
test('Same-page State.update does not re-announce the route (over-announce guard)', async ({ page }) => {
  await page.goto('/#/apps/task');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('#app input').first()).toBeVisible();

  // #page-announcement の「表示しています」書き込み回数を MutationObserver で計測開始
  await page.evaluate(() => {
    window.__routeAnnounceCount = 0;
    const el = document.getElementById('page-announcement');
    new MutationObserver(() => {
      if ((el.textContent || '').includes('表示しています')) { window.__routeAnnounceCount++; }
    }).observe(el, { childList: true, characterData: true, subtree: true });
  });

  // 同一ページ (task) でタスクを 3 個追加 = State.update 再描画 3 回
  const input = page.locator('#app input').first();
  for (let i = 0; i < 3; i++) {
    await input.fill('over-announce-guard-' + i);
    await input.press('Enter');
    await expect(page.getByText('over-announce-guard-' + i)).toBeVisible();
  }
  await page.waitForTimeout(150);

  // 同一ページの State.update では route アナウンスが 1 度も再発火しないこと (fix 前は 3)
  const count = await page.evaluate(() => window.__routeAnnounceCount);
  expect(count).toBe(0);
});


// ===== 7.2: AI 入力の IME composition ガード (日本語入力の誤送信防止) =====
// ai-input の Enter ハンドラは e.isComposing をチェックせず、日本語入力で IME 変換確定の Enter が
// 未確定テキストを誤って submit していた (task と同クラスの実バグ)。修正で `!e.isComposing` ガードを
// 追加。fake clock で「composing 中の Enter は submit されず応答が出ない」「通常 Enter は応答が出る」
// を決定的に検証する。
test('AI input ignores Enter during IME composition (Japanese input safety)', async ({ page }) => {
  await page.clock.install();
  await page.goto('/#/apps/ai');
  await page.waitForLoadState('domcontentloaded');

  const input = page.locator('#ai-input');
  await expect(input).toBeVisible();
  await input.fill('未確定の質問テキスト');

  // IME 変換確定の Enter (isComposing=true) では submit しない
  await input.evaluate((el) => {
    el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', isComposing: true, bubbles: true, cancelable: true }));
  });
  await page.clock.fastForward(500); // submit されていれば応答が出るはずの時間
  await expect(page.getByText('[AI分析:')).toHaveCount(0);

  // 通常の Enter (isComposing=false) では submit → 応答
  await input.press('Enter');
  await page.clock.fastForward(500);
  await expect(page.getByText('[AI分析:').first()).toBeVisible();
});
