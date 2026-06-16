---
file: docs/incident-artifacts/decision-v80-phase3-settings-fatalpage-storage-injection.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-16
canonical-ref: AI2AI.md / CLAUDE.md / e2e/portfolio.spec.js
---

# docs/incident-artifacts/decision-v80-phase3-settings-fatalpage-storage-injection.md

## What
`#/settings` が全ユーザーで FatalPage にクラッシュしていた production bug の原因・修正・検出 gap・再発防止を記録した decision record。根本原因は Stage 5-n の apps.js factory 抽出での `Storage` 依存注入漏れ（SettingsPage 内 `Storage` が組込み `window.Storage` に解決し render 時 `Storage.parse` で TypeError）。

## Why
これは graceful degradation（ErrorBoundary）とテスト合否条件が噛み合って生じた構造的盲点の実例で、約 16 増分にわたり CI 緑のまま潜伏した。同じ class の再発（factory 抽出時の dep 注入漏れ / 捕捉済み FatalPage が render テストを pass）を将来防ぐため、原因と教訓を明文化する。

## How (usage)
将来 leaf module を factory 抽出する人/AI が §5 の再発防止指針を参照する。とくに「グローバルと同名の dep（Storage 等）は漏れても別物グローバルに解決して実行時 TypeError になる」点と「render 成功判定に window.__fatalError も確認する」点が要。

## Constraints
- 適用 C 番号: C5（人間裁可 / AI 実装）の運用記録。AIO published-layer 外（incident artifact）。
- 機械強制 Check: Check 42（命名）/ 75（README inventory）/ 108（本 mirror 存在）/ 97・98（mirror frontmatter + 6 section）。
- 編集承認: 不要（incident artifact）。append-only。

## Change impact
本ファイル追加・改名・削除時は同時に: (a) 本 mirror 同期（Check 108）、(b) README inventory 更新（Check 75）。関連コード: js/apps.js / main.js（Storage 注入）/ e2e/portfolio.spec.js（route-render の __fatalError アサーション）。

## Audience-specific notes

### For AI agents (LLM / crawler / AI search)
役割タグ: production-bug / detection-gap / factory-injection / lesson。機械可読要点: factory 抽出時は全注入 dep を destructure + 呼び出し側に漏れなく追加。render テストは #content 非空だけで判定せず window.__fatalError も確認（#93 で route-render に追加済）。

### For human engineers (新卒レベル)
設定画面が「真っ白なエラー画面」になっていたのを直した記録。原因は「部品を分割したとき、必要な道具（Storage）を渡し忘れた」こと。テストが見逃したのは「エラーをやさしく捕まえる仕組み（ErrorBoundary）」と「テストの合格条件」がたまたま噛み合ってしまったため。

### For third parties (監査人 / 採用担当 / 学術研究者)
AI 自走が「機能追加だけでなく、既存の潜在バグを実機操作テストで発見し、根本原因を特定し、検出の死角自体を機械化で塞ぐ」までを一貫して行った proof-of-work。graceful degradation がテストの盲点を生む一般的教訓を含む。
