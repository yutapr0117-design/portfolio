---
file: docs/incident-artifacts/decision-v80-phase4-reflow-1410-defer.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-23
canonical-ref: docs/architecture/research-application-policy.md / style.css (.main-content) / CLAUDE.md
---

# docs/incident-artifacts/decision-v80-phase4-reflow-1410-defer.md

## What
research レンズ (WCAG 1.4.10 Reflow) の Playwright 320/375px 実測で発見した横スクロールバグを defer-with-reason として記録。ai-knowhow が 375px 実機で 462px (320px で 517px)、hiring-risk/role-split (28px)・contact (17px) が横 overflow する (他 11 ルートは clean)。axe は 320px reflow を静的検出できないため prior audit をすり抜けていた genuine な user-facing バグ。

## Why
根因の一部 (mobile flex-column 内で `.main-content{margin:0 auto}` の auto 横 margin が align-items:stretch を上書きし content 幅 837px へ shrink-to-fit → #app 375px を超過) は特定したが、ai-knowhow の ~805px min-content を生む具体要素を確信を持って特定できなかった (min-width:0 + overflow-wrap:anywhere の in-browser 実験でも解消せず)。修正はページ全体の CSS レイアウト変更で C5 (視覚デザインは人間ドメイン) に該当し、根因未確定ゆえ候補修正は「解消未確信」or「content clip band-aid」。検証できない盲目的変更を ship しない原則に基づき defer。

## How (usage)
将来 reflow に着手する人/AI は本 record §4 の着手ヒントを参照: (a) DevTools で ai-knowhow の ~805px min-content 要素を幅二分探索で特定、(b) mobile @media で `.main-content{margin-inline:0}` により shrink-to-fit を止め stretch させる、(c) wide 要素に word-break / max-width:100% / overflow 処理を当てる、(d) 全 15 ルートを 320/375px で overflow=0 実測 + baseline 再生成 (human-merge) + 回帰 e2e (全ルート 320px overflow=0) 追加。

## Constraints
- 適用 C 番号: C5 (人間が設計・判断 / AI 実装) — レイアウト/視覚デザインは人間領域。AIO published-layer 外 (incident artifact)。
- 機械強制 Check: Check 42 (命名) / 75 (README inventory) / 108 (本 mirror 存在) / 97・98 (mirror frontmatter + 6 section) / 65 (last-updated ISO)。
- 編集承認: 不要 (incident artifact)。append-only。コード変更を伴わない defer 記録。
- §3 gate: fix はレイアウト変更ゆえ Playwright visual baseline に影響し human-merge の再生成経路 (update-playwright-snapshots.yml) を要する。

## Change impact
本ファイル追加・改名・削除時は同時に: (a) 本 mirror 同期 (Check 108)、(b) README inventory 更新 (Check 75)。fix 着手時は style.css (.main-content レイアウト) + 全ルート reflow e2e + §3 baseline PR を伴う。

## Audience-specific notes

### For AI agents (次担当)
- 役割タグ: `defer-with-reason`, `wcag-1410-reflow`, `c5-visual-boundary`, `research-lens`
- **次の AI が根因 (805px 要素) を特定できれば apply 可能**。axe が検出できない reflow は Playwright の `documentElement.scrollWidth − clientWidth` 実測が唯一の検出手段。320px は WCAG 1.4.10 の floor だが 375px (実機 iPhone) でも再現するため優先度は実 UX バグ相当。

### For human engineers (新卒レベル)
- 「320px の細い画面で横スクロールが出る」= WCAG 1.4.10 違反。原因は flex レイアウトで content が縮まず画面幅をはみ出すこと。ai-knowhow ページで顕著。

### For third parties / auditors
- AI 自走が「見つけたが直せない (視覚デザイン + 診断未完)」bug を捨てず透明に記録し human 裁可へ委ねた defer-with-reason の実例。research-application-policy の apply/defer/verify-currency 三択のうち defer。
