# decision-v80-phase4-reflow-1410-defer.md

```
Decision-Date : 2026-07-23
Session       : 無限改善自走 run（vacuous-gate/docs-drift/research レンズ）。非 digest 層（incident artifact）。
Implementer   : Claude Code (Anthropic Claude Opus) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)
Track         : v80+ staged major update（Phase 4 — WCAG 1.4.10 Reflow finding / research-application §3C defer-with-reason）
Pipeline-Ver  : v74 (unchanged)
Canonical-Ref : docs/architecture/research-application-policy.md（apply / defer-with-reason / verify-currency）/ style.css（.main-content レイアウト）
Status        : Deferred-with-reason（C5 視覚デザイン境界 + 根因の一部が診断未完）
```

> **Canonical hierarchy:** `AI2AI.md` canonical / `llms-full.txt` ground truth. 従属 incident artifact。

---

## 1. 経緯：research レンズ（WCAG 1.4.10 Reflow）の実測で横スクロールを検出

axe-core の静的監査は 320px reflow（1.4.10）を検出できない（レンダリング依存の SC）。research
レンズで Playwright により **320px / 375px viewport の実測**を全 15 ルートに行った結果、以下で
`documentElement.scrollWidth − clientWidth > 0`（横スクロール発生）を確認した：

| ルート | 320px overflow | 375px overflow | 主 culprit |
| :-- | --: | --: | :-- |
| `#/ai-knowhow` | **517px** | **462px** | `main.main-content` が 837px 幅（#app 375px を超過） |
| `#/hiring-risk` | 28px | — | `main.main-content` |
| `#/role-split` | 28px | — | `main.main-content` |
| `#/contact` | 17px | — | `main.main-content` |

他 11 ルート（home / projects / projects/:slug / quiz / apps / apps/task / apps/settings /
apps/pomodoro / apps/notes / about / resume）は 320px で overflow=0（clean）。**375px（実機 iPhone
相当）でも ai-knowhow は 462px 横スクロールする＝WCAG 1.4.10（AA・320px reflow）違反かつ実 UX バグ。**

## 2. 診断（判明した根因と未確定部分）

- **判明**: `#app`（`display:flex`）は mobile（≤MOBILE_BREAKPOINT=920px）で `flex-direction: column`。
  その flex-column 内で `.main-content { margin: 0 auto; ... }`（style.css:477）の **auto 横 margin が
  align-items:stretch を上書き**し、main-content が viewport 幅（375px）へ stretch せず content 幅
  （837px）へ shrink-to-fit する。ゆえに main-content が親 #app（375px）を横に超過する。
- **未確定**: ai-knowhow の content は min-content ≈ 805px を持つ（他ルートは fit する）。だが
  `min-width:0`（.main-content は既に持つ）・全 descendant への `min-width:0` + `overflow-wrap:anywhere`
  の in-browser 実験でも overflow が解消しなかった（462px 不変）。つまり単純な flex-shrink /
  text-wrap 由来ではなく、**~805px の min-content を生む具体的要素を確信を持って特定できていない**
  （text leaf は全て white-space:normal で wrappable = victim。badge/flex-wrap 行も個別 badge は ≤370px）。

## 3. 判断：defer-with-reason（human 裁可）

以下の理由で **AI 自走では修正せず human（横井雄太）へ委ねる**：

1. **C5 境界**: 修正は CSS レイアウト（`.main-content` の margin / #app flex 挙動 / 幅制約）の変更で、
   視覚デザインに影響する。C5 では「色/ブランド/視覚デザインは人間ドメイン」。#741 の下線
   （非色 a11y アフォーダンス）は要素追加で render-neutral 寄りだったが、本件は**ページ全体の
   レイアウト挙動**の変更で影響範囲が広く、desktop の中央寄せ（margin:0 auto）等と干渉しうる。
2. **診断未完**: ~805px min-content を生む要素を特定できていないため、候補修正（mobile で
   `margin:0` へ上書き / `overflow-x:hidden` band-aid / wide 要素の word-break）はいずれも
   「解消を確信できない」または「content を clip する band-aid」であり、**検証できない盲目的変更を
   ship しない**原則（本 session の一貫方針）に反する。
3. **screenshot baseline**: レイアウト変更は §3 の Playwright visual baseline に影響し、human-merge
   の baseline 再生成経路（update-playwright-snapshots.yml）を要する。

## 4. human 向け着手ヒント（修正する場合）

- mobile @media（`.app { flex-direction: column }` のブロック）に `.main-content { margin-inline: 0 }`
  を足すと auto margin による shrink-to-fit を止め stretch させられる可能性（desktop の中央寄せは
  据え置き）。ただし ~805px 要素が残ると main-content 内で依然 overflow するため、**先に
  ai-knowhow の 805px min-content 要素を特定**（DevTools で幅を二分探索）してから word-break /
  max-width:100% / overflow 処理を当てるのが確実。
- 修正後は 320px / 375px の全 15 ルートで overflow=0 を Playwright 実測し、baseline 再生成 →
  human-merge。回帰防止に「全ルート 320px overflow=0」の behavior e2e 追加を推奨。

---

**Status: Deferred-with-reason.** 本 record は genuine な 1.4.10 finding を透明に記録し（discover）、
C5 + 診断未完を理由に human 裁可へ委ねる（defer-with-reason）。fix は human 着手 or 次の AI 自走で
根因特定後に apply する。
