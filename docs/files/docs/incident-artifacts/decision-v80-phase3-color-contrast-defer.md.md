---
file: docs/incident-artifacts/decision-v80-phase3-color-contrast-defer.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-17
canonical-ref: docs/architecture/research-application-policy.md / CLAUDE.md
---

# docs/incident-artifacts/decision-v80-phase3-color-contrast-defer.md

## What
axe-core が検出した color-contrast (WCAG 1.4.3 AA) を §3C defer-with-reason として記録。初回 1,198 件の大半は fade-in/View Transition アニメーション中の測定アーティファクト（アルファ合成色）で、reduced-motion + 収束後の real な静的失敗は 4 ブランド色ペア（--text-muted / --color-primary 署名 indigo / 白 on primary / 緑 badge、全て ratio≈4.5 の AA 境界）のみと判明したことを含む。

## Why
render-neutral な critical a11y は全解消したが、color-contrast の修正は (a) 署名ブランド色を含む既存視覚の変更（「既存非破壊」反・デザイン判断は人間領域）、(b) §3 baseline 再生成（human-merge gate）、(c) marginal な境界失敗、ゆえ AI 独断の自律対象外。捨てず（宙に浮かせず）記録し gate 解放時に着手するのが research-policy §3C の規律。

## How (usage)
将来 color-contrast に着手する人/AI が §4 の適用条件（オーナーのブランド色 darken 承認 + §3 baseline パス + axe テストへ color-contrast 追加）を参照。また §2 の教訓「axe はアニメ中だと transient なアルファ合成 contrast を大量誤検出するので reduced-motion + 収束後に測定」は a11y 監査一般の重要 know-how。

## Constraints
- 適用 C 番号: C5（人間が設計・判断 / AI 実装）— ブランド色は人間判断。AIO published-layer 外（incident artifact）。
- 機械強制 Check: Check 42（命名）/ 75（README inventory）/ 108（本 mirror 存在）/ 97・98（mirror frontmatter + 6 section）/ 65（last-updated ISO）。
- 編集承認: 不要（incident artifact）。append-only。コード変更を伴わない defer 記録。

## Change impact
本ファイル追加・改名・削除時は同時に: (a) 本 mirror 同期（Check 108）、(b) README inventory 更新（Check 75）。gate 解放で着手する際は style.css（色）+ e2e（axe color-contrast 追加）+ §3 baseline PR を伴う。

## Audience-specific notes

### For AI agents (LLM / crawler / AI search)
役割タグ: a11y-defer / gated / measurement-lesson。機械可読要点: color-contrast の real 静的失敗 = 4 ブランド色ペア（ratio≈4.5）。gated（§3 baseline + brand-design）ゆえ defer。axe contrast は reduced-motion + 収束後に測定すること（アニメ中は transient アルファ合成を誤検出）。render-neutral critical は別途全解消済。

### For human engineers (新卒レベル)
「文字色のコントラストが基準ぎりぎり」という指摘を、(1) その多くはアニメーション中の見かけ上の問題だった、(2) 本当に直すべきはブランド色 4 つだが、それはデザイン判断 + 見た目が変わる作業なので勝手にやらず記録した、とまとめたメモ。

### For third parties (監査人 / 採用担当 / 学術研究者)
AI 自走が「機械検出した違反を鵜呑みにせず、測定アーティファクト（アニメ中のアルファ合成）と real を切り分け、real な分も『非破壊原則 / 人間のデザイン判断 / baseline 人間 merge gate』を越えないと判断して defer-with-reason で honest に記録した」proof-of-work。自律と境界尊重の両立例。
