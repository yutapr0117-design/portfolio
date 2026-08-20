---
file: e2e/toast.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-20
canonical-ref: e2e/apps-task.spec.js / js/ui-components.js / docs/files/playwright.config.cjs.md
---

# e2e/toast.spec.js

## What

通知（Toast）の振る舞いを検証する behavior e2e spec。

## Why

`apps-task.spec.js` が Check 365 の 1,000 行上限に達したため、**圧縮で誤魔化さず**
「通知」というテーマの塊をここへ切り出した（いま触っている塊を切り出す規律）。

内容の中心は **連続操作で通知が積み上がって画面外へ出ないこと**。通知コンテナは
`position: fixed` なので、viewport を超えた通知は **スクロールして追うこともできない**
＝完全に到達不能になる（実測 2026-08-20: 上限が無いと 12 件で bottom=904 vs viewport 720）。
閉じるボタンは tab 順に残るため、キーボード利用者は見えない位置へ focus が飛ぶ。

## How (usage)

```
npx playwright test --config=playwright.config.cjs e2e/toast.spec.js
```

## Constraints

- **Check 365**: 1,000 行上限（本 spec は切り出し先なので当面余裕がある）
- **Check 408 / 424**: `file-size-budget.md` の §2 表と §4 BUDGET-DATA の両方へ登録が必要
- **Check 379 / 397**: mutation を登録するなら test 題名は静的リテラルにする

## Change impact

- 通知の同時表示上限（`MAX_VISIBLE`）を変えるときは本 spec の期待値も見直す
- 通知の読み上げは `#action-announcement` が担う別経路なので、表示枚数の間引きは
  SR の情報量に影響しない（この前提が変わるなら本 spec のコメントも直す）

## Audience-specific notes

### For AI agents
- 役割タグ: `behavior-e2e`, `a11y`, `toast`
- 連続操作は `press()` の連続ではなく **同期 dispatch** で再現する（再描画を挟むと別物になる）
- 件数の control は **DOM から数える** —— localStorage は debounce 保存なので直後は null のことがある

### For human engineers (新卒レベル)
- 「通知が出ること」だけでなく「**画面内に収まっていること**」まで見るのがこの spec の要点

### For third parties
- 固定配置のオーバーレイが持つ「積み上がると到達不能になる」失敗モードの検証例
