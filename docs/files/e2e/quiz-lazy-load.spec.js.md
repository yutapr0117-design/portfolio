---
file: e2e/quiz-lazy-load.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: e2e/quiz.spec.js / js/quiz-renderer.js / main.js / docs/architecture/file-size-budget.md
---

# e2e/quiz-lazy-load.spec.js

## What

quiz データの**遅延読み込み契約**（動的 import のライフサイクル）を守る behavior e2e spec
(BLOCKING gate)。8 テスト。

## Why

#1239 で quiz データ **130,595 bytes**（配信 JS+CSS の 15.6%）を静的 import から**動的 import へ
移し、クリティカルパスから外した**。quiz を開かない訪問者は 4 file を一切取得しなくなった
(実測: home 表示だけで 4 件 fetch → 修正後 0 件)。

代わりに **「まだ届いていない」という状態が新しく生まれた**。この spec が守るのはその状態の扱い:

- 開いた種別だけを取得する（開かなければ 0 件）
- 読み込み中に打った検索語を捨てない
- **未着を「見つかりませんでした」と偽らない** —— 真実は「まだ読み込んでいない」
- 失敗を黙らず報告する / 通信断から回復する（失敗した動的 import は **module map に
  キャッシュされる**ので、別 URL で取り直さないと永久に失敗表示のまま）
- 再訪で再取得しない（ESM module cache）
- 読み込み中を `aria-busy` で伝える

オフライン時の挙動もここに含める —— 遅延化の**明示的なトレードオフ**なので、
「そういう設計だ」と記録する場所が要る。

**分離の理由**: `quiz.spec.js` が 923 行で advisory 予算 (900) を超えたため、BLOCKING (1,000) に
当たる前に単一の技術契約という coherent な塊として切り出した。

## How (usage)

```
npx playwright test e2e/quiz-lazy-load.spec.js --project=chromium
```

## Constraints

- **BLOCKING gate**: `playwright-regression.yml` の behavior job に含まれる。
- **一過性の状態を「時間」で捕まえない。** 「読み込み中」の窓は届いた瞬間に消えるので、
  `setTimeout(N)` で遅らせて N ミリ秒以内に検証が終わることに賭けると、負荷が高いときに
  **その状態が消えた後**を見て偽赤になる（2026-08-23 に実測: 3 回中 1 回 fail・main でも再現）。
  **明示的な解放ゲート**（`await gate` してから `route.continue()`）にすること。

## Change impact

- 遅延読み込みの実装（`js/quiz-renderer.js` の `sourceData` 判定 / `main.js` の動的 import と
  retry）を触ったら、ここが唯一の gate になる。**視覚には「読み込んでいます…」としか出ない**ので
  目視では壊れ方が判らない。
- 新しい quiz 種別を足したら「開いた種別だけ取得する」テストの期待値を見直す。

## Audience-specific notes

### For AI agents
- 役割タグ: `lazy-load`, `dynamic-import`, `critical-path`, `blocking-gate`
- 「まだ届いていない」と「一致が無い」を取り違えないこと。前者を後者として表示するのは**嘘**。

### For human engineers (新卒レベル)
- 動的 import は**失敗も module map にキャッシュされる**。一度失敗したら同じ URL では二度と
  成功しないので、別 URL（query 付き等）で取り直す必要がある。

### For third parties
- バイト削減のためにクリティカルパスから外した結果として生じる状態を、どこまで e2e で
  守るべきかの実例。
