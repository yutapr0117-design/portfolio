---
file: e2e/reflow.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-20
canonical-ref: e2e/navigation-a11y.spec.js / style.css / playwright.config.cjs
---

# e2e/reflow.spec.js

## What

**WCAG 1.4.10 (Reflow)** の behavior e2e spec (BLOCKING gate)。320px 幅で
どのルートにも**横スクロールが発生しない**ことを、既定ブランドと classic ブランドの
両方で検証する。

## Why

この面は **視覚 baseline では原理的に守れない**。screenshot は 1280×720 clip なので
`@media (max-width: 920px)` に到達せず、320px であふれていても緑のまま通る。
つまり **behavior e2e だけが捕捉層**。

実バグ (#962) の真因は「封じ込めの欠陥」だった: `.main-content` の左右 auto margin が
flex の cross 軸で `align-self: stretch` を無効化し、fit-content が min-content を
下回れないため **item 自体が viewport より広くなる**。同 media query 内の
`max-width: 100%` 1 行で 15 ルート × 幅 320/375/768/920 のすべてであふれ 0 になった。

**ブランドごとにフォント幅が違う**ので classic でも別途測る。

元は `e2e/navigation-a11y.spec.js` にあったが、同 file が **917 行**で advisory (900) を
超えたため、**BLOCKING (1,000 行) を踏む前に**切り出した。

## How (usage)

```
npx playwright test e2e/reflow.spec.js --project=chromium
```

## Constraints

- **BLOCKING gate**: `playwright-regression.yml` の behavior job に含まれる。
- **Check 365** (1,000 行) / **Check 408** (BUDGET-DATA 登録必須) /
  **Check 424** (§2 表の実測行数一致)。
- 測定は **≥300ms settle してから**全要素を走査する (120ms では false-negative)。
- **印刷メディアでは `<= 0` で判定する** —— スクロールバーの gutter が予約されず
  CI (Linux) で負値になるため (`=== 0` だと環境差で false RED)。

## Change impact

- レイアウトの封じ込めに関わる CSS (`max-width` / `margin: auto` / flex 方向) を触ったら
  **必ずこの spec を通す**。screenshot は到達しないので、ここが唯一の防波堤。
- ルートを追加したら走査対象に含める。

## Audience-specific notes

### For AI agents
- 役割タグ: `behavior-e2e`, `wcag-1.4.10`, `reflow`, `blocking-gate`

### For human engineers (新卒レベル)
- flex の cross 軸で auto margin を持つ item は `align-self: stretch` が効かず、
  幅が **fit-content** で決まる。fit-content は min-content を下回れないので、
  中身が広いと **箱そのものが viewport を超える**。

### For third parties
- 視覚回帰テストでは原理的に捕捉できない a11y 要件を、behavior テストで守る実装例。
