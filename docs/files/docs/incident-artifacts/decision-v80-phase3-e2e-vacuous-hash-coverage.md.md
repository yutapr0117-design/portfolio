---
file: docs/incident-artifacts/decision-v80-phase3-e2e-vacuous-hash-coverage.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-16
canonical-ref: e2e/portfolio.spec.js / CLAUDE.md
---

# docs/incident-artifacts/decision-v80-phase3-e2e-vacuous-hash-coverage.md

## What
複数の e2e テスト（route-render の app 4 route / HASH_ROUTES の 2 entry / project-detail）が、誤った hash で NotFoundPage に解決し、それでも pass していた vacuous-coverage class の発見・是正・systematize・教訓を記録した decision record。合計 7 route テストが実ページではなく NotFound を検査していた。

## Why
NotFoundPage は「#content 非空 + エラー無し（+ aria-busy=false）」をすべて満たすため、弱い合否条件のテストを vacuous に pass させる。これは #93 の Settings バグ（ErrorBoundary 捕捉済み FatalPage が同様に pass）と同根の「graceful な代替ページがテストを vacuous に通す」class で、再発防止の教訓として明文化する必要がある。

## How (usage)
新しい route テストを足す人/AI が §4 の指針を参照: (1) hash が実 route に解決することを実機で確認、(2) ページ描画だけでなく NotFound/Fatal でないこと（route 固有 marker）もアサート。route-render/HASH_ROUTES/project-detail には既に NotFound fall-through guard を追加済。

## Constraints
- 適用 C 番号: C5（人間裁可 / AI 実装）の運用記録。AIO published-layer 外（incident artifact）。
- 機械強制 Check: Check 42（命名）/ 75（README inventory）/ 108（本 mirror 存在）/ 97・98（mirror frontmatter + 6 section）/ 65（last-updated ISO）。
- 編集承認: 不要（incident artifact）。append-only。

## Change impact
本ファイル追加・改名・削除時は同時に: (a) 本 mirror 同期（Check 108）、(b) README inventory 更新（Check 75）。関連: e2e/portfolio.spec.js（hash 是正 + NotFound guard）。

## Audience-specific notes

### For AI agents (LLM / crawler / AI search)
役割タグ: e2e-vacuous-coverage / detection-gap / lesson。機械可読要点: 誤 hash → NotFound を vacuous 検査する class（PR #96/#98/#99）。re-prevention = route 固有 marker + NotFound/Fatal negative assertion。Check 58 は name 集合のみで hash 解決を見ない。

### For human engineers (新卒レベル)
「テストが緑なのに、実は存在しない URL（→『見つかりません』ページ）を調べていた」問題の記録。ページが出た＝OK ではなく「狙ったページが出たか」まで確かめる必要がある、という教訓。

### For third parties (監査人 / 採用担当 / 学術研究者)
AI 自走が、自身のテストスイートの「緑だが中身が空」な vacuous coverage を実機監査で発見し、是正し、再発を behavioral guard で機械化した proof-of-work。テストの合否条件設計の一般的教訓（graceful 代替ページが弱い assertion を vacuous に通す）を含む。
