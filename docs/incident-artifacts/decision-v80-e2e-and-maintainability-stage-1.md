# decision-v80-e2e-and-maintainability-stage-1.md

```
Decision-Date : 2026-05-30
Session       : AI2AI.md Session Record #16
Implementer   : Claude Opus 4.8 (Anthropic) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)
Track         : v80+ staged major update (Phase 0 / Phase 1)
Pipeline-Ver  : v74 (unchanged — "v80+" is a track name, not an application version)
Canonical-Ref : AI2AI.md STEP 7 / llms-full.txt / decision-v80-maintainability-roadmap.md
Status        : Applied
```

> **Canonical hierarchy:** `AI2AI.md` is the canonical handoff; `llms-full.txt` is ground truth.
> This decision record is a subordinate incident artifact. If it conflicts with `AI2AI.md` or `llms-full.txt`, those win.

---

## 1. 背景

v74 本体は良好状態（全 consistency check PASS）。`decision-v80-maintainability-roadmap.md` で宣言した v80+ staged major update track の **Phase 0（E2E/CI/検証導線の実効性強化）** と **Phase 1（保守性マップ整備）** に着手した。UI 刷新やフレームワーク移行ではなく、保守性・拡張性・AI実装安全性の順次・堅実な向上である。破壊的な一括変更は行わない。

---

## 2. 決定事項

### D-1 (P0-01): Playwright baseline 生成フローの実効化

**問題:** `e2e/portfolio.spec.js` の screenshot test は baseline PNG 未存在時に `test.skip()` する。一方 `update-playwright-snapshots.yml` は `--update-snapshots` で baseline を生成する意図だが、skip-guard が働くため **生成 workflow 実行時にもテストが skip され、PNG が生成されないデッドロック**だった。

**決定:**
- `update-playwright-snapshots.yml` の生成ステップに `env: PLAYWRIGHT_UPDATE_SNAPSHOTS: "1"` を付与。
- `e2e/portfolio.spec.js` に `isSnapshotUpdateMode()` を追加し、skip 条件を `!baselineExists(...) && !isSnapshotUpdateMode()` に変更。生成モードでは skip せず `toHaveScreenshot()` を実行。通常 regression では従来どおり skip（初回赤化を防止）。
- `check_repository_consistency.py` に Check 29（BLOCKING）を追加し、この連携が壊れていないこと（両側の env 参照 + skip-guard が `baselineExists()` 単独で閉じていないこと）を検査。再発防止。

**根拠:** E2E 視覚回帰が「宣言済みだが実効化できない」状態を解消し、将来の視覚差分検出へ実接続する。

### D-2 (P0-02): baseline PNG はAIが捏造しない

ブラウザ実行環境がない本セッションでは baseline PNG を生成しない（Not possible）。生成フローのみ実効化し、人間が GitHub Actions から生成・コミットできる状態にした。手順は §4 参照。

### D-3 (Phase 1): 保守性ドキュメントの新設

- `docs/architecture/repository-maintainability-map.md`
- `docs/architecture/main-js-extraction-map.md`

を新設。`main.js` は **物理分割しない**。責務境界・抽出候補・副作用リスク・検証条件を先に明文化し、後続AIが迷わず・壊さず作業できる契約とする。`check_repository_consistency.py` Check 30（BLOCKING）で両ファイルの存在を保証。

### D-4 (P1-01): README をセルフブランディング主軸へ整流

見出し「PM実績サマリー（採用担当者・案件担当者向け）」→「PM / AIオーケストレーション実績サマリー（外部評価者向け価値翻訳）」。主目的が **AIO先行セルフブランディング兼 proof-of-work（機械可読な権威形成）** であり採用最適化ではない旨を明記。採用担当者・案件担当者・AIエージェントを含む外部評価者向けの価値翻訳は残す。

### D-5 (P2-01/02): aio-monitoring.yml の通知堅牢化

citation increase/decrease の2通知ステップを1ステップに統合（重複排除）。ラベルを best-effort 作成（既存の 422 等は握り潰す）し、ラベル付き Issue 作成失敗時はラベルなしで再作成。**個人ポートフォリオでは「ラベル付与」より「workflow 成功」を優先**する設計。

---

## 3. 意図的に「やらなかった」こと（Phase 2 へ延期、要オーケストレーター判断）

### N-1: ESLint ゲートの実効化 — **重要**

**発見:** `architecture-validation.yml` の ESLint ステップは実質無効（vacuous）。`npm install --no-save eslint`（バージョン無指定 → ESLint 9.x）に対し `--no-eslintrc --env browser` を渡すが、これらフラグは ESLint 9 で削除済み。コマンドは失敗するが末尾 `|| true` で握り潰され、grep 対象の error 行が出ないため `ERROR_COUNT=0` で常に PASS していた。

**追加発見:** ESLint 8.57.1（classic `.eslintrc.json` 互換）で実行すると **216 errors**（大半が `no-var` / `no-implicit-globals` / `curly`）。つまりコードは自身の lint ルールに多数違反している。

**判断:** ゲートを実効化するには「コード 216件修正」「ルール緩和」「flat config 移行」のいずれかの方針決定が必要。これは `main.js` / `sw.js` 等 v74 本体の安定性に直結し、独立した Phase 2 タスクに値する。本 track では **実装しない**。`repository-maintainability-map.md` に Phase 2 タスクとして記録。**一括修正は禁止**（C5 のレビュー前提を超える規模の自動変更を避ける）。

### N-2: dev依存の中央管理（package.json / lockfile / npm ci）

`@playwright/test` / `http-server` / `stylelint` / `stylelint-declaration-strict-value` / `eslint` の中央管理は ESLint 実効化（N-1）と密結合。さらに every-push の BLOCKING パイプライン（architecture-validation.yml）を **実 CI で検証できない**ため、ナイーブな投入は CI 全赤化のリスクがある。Phase 2 として `repository-maintainability-map.md` に計画を記録し、本 track では投入しない。手書き lockfile は作らない。

---

## 4. Not possible と人間の手順

| 項目 | 状態 | 人間の手順 |
|---|---|---|
| Playwright baseline PNG 生成 | Not possible（本環境はブラウザ不可） | GitHub Actions → "Update Playwright Baseline Snapshots" → Run workflow → artifact `playwright-baseline-snapshots-<run_id>` を DL → `.png` を `e2e/portfolio.spec.js-snapshots/` に配置 → commit |
| 実 CI での workflow 緑確認 | Not possible（本環境は Actions 不可） | 初回 push 後、architecture-validation / playwright-regression / aio-monitoring の Actions 結果を確認 |
| ESLint 216件 / package.json | 意図的に未実施 | Phase 2 で方針決定後に着手（要承認） |
| AIO citation 実観測 | 未発生 | 実引用確認時のみ `aio-monitoring-log.json` に記録。捏造禁止 |

---

## 5. C1〜C7 遵守

C1 外部FW/ライブラリ追加なし（package.json も追加せず） / C2 IIFE未変更 / C3 ErrorBoundary未変更 / C4 FW再提案なし / C5 人間はコード未記述（実装は Claude Opus 4.8） / C6 AIOテキストは Phase 状態追記と日付同期のみ（エンティティ/権威текスト・JSON-LD・バイナリ未変更） / C7 KARTE CDN SRI 非適用維持。すべて遵守。
