---
file: e2e/print.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-11
canonical-ref: style.css / playwright.config.cjs / .github/workflows/playwright-regression.yml
---

# e2e/print.spec.js

## What

`@media print` の**実効性**を検証する behavior e2e。`page.emulateMedia({ media: 'print' })` で
印刷メディアに切り替え、(1) ナビ chrome（sidebar / topbar / drawer）が消えて本文が全幅化し
横あふれしないこと、(2) 外部リンクの URL が `::after` で紙面に併記されることを assert する。

## Why

`style.css` の `@media print` ブロックは、**この spec を書くまで検証している層が一つも無かった**。

- **screenshot** は 1280x720 の **screen media** で撮るので print media には到達しない（かつ ADVISORY）
- **behavior e2e** は print を emulate していなかった
- **consistency Check** は CSS の存在を見ても *効果* は見ない

つまり `@media print` を丸ごと削除しても**全ゲートが緑のまま通る**（Check 133 / 134 / 135 で
繰り返し見つけた「silent-critical だが捕捉層ゼロ」と同じ class）。

このサイトは採用担当が Resume / About を紙に出す想定があるため、印刷の破損は
「機能性（loads / displays / comprehensible）」の毀損に当たる。暗色テーマのまま印刷されれば
インクを大量に消費し、sidebar が残れば紙面の左に空白帯と重複ナビが出る。

## How (usage)

```
npx playwright test --config=playwright.config.cjs e2e/print.spec.js
```

対象ルートは `#/resume` / `#/about` / `#/role-split`（紙に出す動機が実在する面）。

## Constraints

- **`emulateMedia({ media: null })` で必ず戻す**: 同一 page を使い回すため、戻し忘れると
  後続ルートの測定が print のまま行われ、何を検証したのか分からなくなる。
- **不在検査の前に描画確定を待つ**: `#content h1, h2` の visible を待ってから評価する
  （goto 直後の評価は非同期描画とレースして「まだ無い」を「無い」と誤認する）。
- **Check 408**: 本 spec が `file-size-budget.md` の §2 表と §4 BUDGET-DATA に登録されていること。
- **Check 108**: 本 mirror doc の存在。

## Change impact

- `@media print` の要素セレクタを変える場合、本 spec の `disp()` 対象 id も合わせる。
- 印刷対象ルートを増やす場合は `PRINT_ROUTES` に足す（全ルートを回すほどの価値は無いと判断し、
  紙に出す動機が実在する 3 つに絞ってある）。

## Audience-specific notes

### For AI agents
- 役割タグ: `print-media`, `silent-critical-coverage`

### For human engineers (新卒レベル)
- 「CSS に書いてある」と「実際に効いている」は別、を測る例。`emulateMedia` で検証できる。

### For third parties
- 静的サイトでも印刷体験を自動検証できる、という最小実装。
