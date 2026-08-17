---
file: e2e/reduced-motion.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-17
canonical-ref: playwright.config.cjs / main.js / js/home-page.js / style.css / e2e/navigation-a11y.spec.js
---

# e2e/reduced-motion.spec.js

## What

`prefers-reduced-motion: reduce` を選んだ利用者に対して、サイトが**本当に動かない**ことを
固定する behavior e2e。このサイトの動きは 2 系統ある。

1. **home の in-page ジャンプ** — 「ケースを見る →」が 1,000px 超スクロールする
   (`scrollIntoView`)。あわせて移動先へ focus を移すこと (WCAG 2.4.3) も見る
2. **ルート遷移の View Transition** — ページ全体のクロスフェード。三層防御を検証する

## Why

前庭障害のある利用者にとって大きなスクロールや全画面のクロスフェードは実害がある
(WCAG 2.3.3)。しかも**壊れても fatal が出ず**、視覚 baseline は 1280x720 の 1 枚だけ
かつ ADVISORY なので、**捕捉層はこの behavior test しかない**。

### 過去に実際に壊れていた (#993)

`scrollIntoView({behavior:'smooth'})` は **behavior を明示している**ため、CSSOM-View 仕様に
より CSS の `scroll-behavior` は参照されない。つまり style.css の reduce override は
**この呼び出しには効いていなかった**。紛らわしいのは、同じ実測で `window.scrollTo(0, 0)` は
reduce のとき即時に完了しており、**CSS の override 自体は正しく働いていた**こと。
「近くが正常に動いていることは、対象が守られている証拠にならない」。

### View Transition は三層防御 (実測で確認)

| 層 | 実体 | 役割 |
| :-- | :-- | :-- |
| 1 | `render()` の `!prefersReducedMotion` ガード | そもそも呼ばない |
| 2 | `startViewTransitionProxy` の reduce 判定 | **素の API を直接呼ばれても**尊重する (Check 43b) |
| 3 | `style.css` の `::view-transition-*` `animation: none` | 最後の安全網 |

実測 (2026-08-17): 層 1 を丸ごと外しても behavior e2e 390 件が**全て緑**だった。
つまりこの契約はどの層からも見られていなかった。

## How (usage)

```
npm run test:e2e
  └─ Playwright + http-server (playwright.config.cjs testDir: ./e2e)
```

## Constraints

- **Check 28**: 全 e2e/*.spec.js に test() のネスト無し
- **Check 111**: networkidle 待ちは screenshot (portfolio.spec.js) 以外で禁止
- **Check 114**: test.only/describe.only 無し
- **Check 151**: 全 e2e/*.spec.js 横断で test() title 一意
- **Check 108**: docs/files ミラー 1 対 1 bijection
- **Check 408**: e2e spec は file-size-budget.md の BUDGET-DATA へ登録必須
- **Check 420**: 登録する mutation の `find` は対象 file 内で一意
- **Check 421**: `'smooth'` リテラルを持つ shipped JS は同 file で `prefers-reduced-motion` を
  問い合わせる (静的側の対の層)

## Change impact

- `main.js` の View Transition 判定 / proxy、`js/home-page.js` の scrollIntoView を
  変更すると本 spec が RED になる
- spec ファイル rename → docs/files ミラー同期 (Check 108) + BUDGET-DATA 同期 (Check 408)

## Audience-specific notes

### For AI agents
- 役割タグ: `e2e-spec`, `behavior-gate`, `a11y`, `motion`
- **測定の要点**: `document.startViewTransition` を `addInitScript` で包んでも、proxy が
  install 時に `.bind(document)` で捕まえるのは *その包み*。よって**proxy が native へ
  委譲したときだけ**カウントが増える = 「実際にアニメーションが走ったか」を測っている
- **冗長な層があるとき、片方を潰しても緑**なのは vacuous の証拠ではない。「効いている行」を
  狙わないと RED にならない。ルート遷移テストは層 1 だけ / 層 2 だけを外しても緑で、
  両方外すと RED —— defense-in-depth ゆえ**単一 mutation では RED にできないので登録しない**

### For human engineers (新卒レベル)
- CSS の `@media (prefers-reduced-motion: reduce)` を書いただけでは足りない。JS が
  `behavior: 'smooth'` のように**明示**した呼び出しは CSS を参照しないので、JS 側でも
  `matchMedia` を見る必要がある

### For third parties
- 「設定を尊重している」と主張するだけでなく、**実際に動いていないことを機械的に測る**例
