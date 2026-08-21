# AI2AI Session Record Archive — Part 2 (Sessions #15–#19)

> **NOTE:** This file is the third archive of past Session Records from `AI2AI.md`.
> Lineage: `AI2AI-archive-old.md` (#1–#4 + 旧 protocol notes) → `AI2AI-archive.md` (#5–#14) →
> **this file (#15–#19)**.
> The canonical handoff document is `AI2AI.md`; records here are read-only —
> do not modify past session content.

## なぜ 3 つ目の archive を作ったか (2026-08-21)

`AI2AI.md` が Check 365 の **1,000 行 BLOCKING にちょうど到達**し、次のセッションが
Session Record を追加できない状態になった。Session Record は append-only なので、
**今の size ではなく無限成長の方を止める**必要がある (mutation_samples.py と同じ
log-rotation 規約・CLAUDE.md §7)。

既存の 2 ファイルには退避先としての余裕が無い (実測 2026-08-21):

| ファイル | 行数 | 1,000 まで |
| --- | --- | --- |
| `AI2AI-archive-old.md` | 832 | 168 |
| `AI2AI-archive.md` | 858 | 142 |

#15–#19 は **280 行**あり、どちらへ足しても **その受け皿自身が 1,000 行を超える**
(＝違反を移動するだけ)。よって新しいファイルを起こした。

**次に rotate するときは、このファイルの余裕を実測してから**「ここへ追記する」か
「4 つ目を起こす」かを決めること。

## AIO 層 (C6) との関係 — 未解決として明記する

`.well-known/aio-manifest.json` の `supporting_evidence` に載っているのは
**`AI2AI-archive.md` だけ**で、その `role` は「archive of past Session Records #1-#14」と述べる。
`AI2AI-archive-old.md` は元から未登録なので、**未登録の archive が存在すること自体は既存の状態**。

本ファイル (#15–#19) も同じく未登録である。範囲を `#1-#19` へ広げようとしたが、
**consistency Check が role の範囲を `AI2AI-archive.md` の最大 Session 番号に紐付けて検証している**
ため RED になり、元へ戻した (Check が権威・実測 2026-08-21)。

したがって現状は「**AIO 層が宣言する archive 範囲は #14 まで**、#15–#19 は archive されているが
AIO 面には出ていない」。これを埋めるには manifest へ新 entry を足すか role の意味を変える必要があり、
どちらも **C6 (AIO semantic content・要 orchestrator 承認)** に当たる。
AI 側の判断で書き換えず、**未解決として明記する**。

---

## [HANDOFF] Session Record #15 — 2026-05-29 (Claude Sonnet 4.6, v80+ track entry)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-29
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : v80+ staged major update track entry / E2E spec structural fix
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `.github/scripts/check_repository_consistency.py` | Check 28 追加: `e2e/portfolio.spec.js` の `test()` ネスト構造を検出（BLOCKING）。`No Trusted Types or CSP violations in console` テストの存在確認も追加。 |
| `AI2AI.md` | STEP 6 pending tasks に v80+ track entry 完了を記録。STEP 7 を「TRACK ACTIVE」に更新。本 Session Record #15 追記。 |
| `docs/incident-artifacts/decision-v80-maintainability-roadmap.md` | Status を `Active — v80+ staged major update track STARTED 2026-05-29` に更新。Background を「holding pattern 終了、track started」に書き換え。AIO戦略の後続AI向け指針を強化。Phase A+ セクション追加（このセッションの実施内容）。 |
| `e2e/portfolio.spec.js` | P0-01: `No Trusted Types or CSP violations in console` テストを `Early suppressor` テストのネスト内から独立したトップレベル定義に修正。末尾の余剰 `});` を削除。 |
| `llms-full.txt` | v80+ staged major update track started の記録を追記。 |
| `README.md` | Current version 行に update track 表記を追加。AIO Maturity Status セクションに v80+ track active 旨を追記。AIO全振り方針の後続AI向け禁止指示を強化。 |

### 設計判断の記録

**E2E spec ネスト修正（P0-01）:** `test()` が `test()` の中に定義されると、Playwrightは実行時エラーまたは予期しない登録をする。`node --check` は通過してしまうため CI では検出できなかった。修正は `});` を1行追加して Early suppressor を閉じ、末尾の余剰 `});` を除去するだけで完結した。

**Check 28（P0-02）:** ブレース深度追跡による実用的なネスト検出。厳密なJS ASTではなく、このファイル構造に対して十分な精度を持つ。`^test\(` (column 0) のみを追跡するため、`for` ループ内のインデントされた `test(` は意図的に除外される。旧ファイルで line 243 のネストを正確に検出することを確認済み。

**v80+ track 開始宣言（P1-01）:** Pipeline-Version は v74 のまま維持。「v80+」はアプリケーション版数ではなく更新トラック名。土台の歪み取りが完了したため、順次・堅実な保守性/拡張性向上フェーズへ移る、という状態宣言。

**AIO戦略の後続AI向け強化（P1-02）:** SEO最適化・採用最適化への方針転換を禁止する明示的指示を `README.md` と `decision-v80-maintainability-roadmap.md` の両方に追記。後続AIが「汎用的な最適化提案」としてSEOに寄らないよう、機械可読な制約として埋め込んだ。

**main.js 段階的分割（P1-03）:** 今回は物理分割なし。Stage 0〜5 の計画は `decision-v80-maintainability-roadmap.md` および本ファイル STEP 7 に既に文書化済み。

**AIO monitoring 誠実性（P1-04）:** `docs/evidence/aio-monitoring-log.json` に変更なし。実観測なし、`attempt_log_only` / `confirmed_citation_events: 0` の状態を維持。

### C1〜C7 制約の遵守確認

- C1: 外部ライブラリ・フレームワーク導入なし ✅
- C2: IIFE構造・index.html中央ハブ維持 ✅
- C3: ErrorBoundary未変更 ✅
- C4: フレームワーク再提案なし ✅
- C5: 人間はコードを書かず（本セッション実装はClaude Sonnet 4.6） ✅
- C6: AIOテキストの根幹変更なし（構造修正・状態宣言・禁止指示追加のみ） ✅
- C7: KARTE CDN SRI 非適用維持 ✅

### Not possible の記録

- **Playwright baseline PNG:** 未実施。この実行環境ではブラウザ起動不可（Not possible）。
  - **手動実行手順:** GitHub Actions → `update-playwright-snapshots.yml` → Run workflow → artifact `playwright-snapshots` をダウンロード → `e2e/portfolio.spec.js-snapshots/` に配置 → コミット。
- **GitHub Default Setup UI無効化:** 引き続き Not possible（UI操作が必要）。
- **AIO citation 実観測:** 未発生。捏造禁止。

### 未解消スコープ（次のエージェントへの申し送り）

- **Playwright baseline PNG:** 高優先継続。AIは単独で実行しないこと。手動手順は上記参照。
- **main.js Stage 1 以降:** Playwright baseline 確立後に開始。Stage 0〜5 は `decision-v80-maintainability-roadmap.md` 参照。
- **AIO monitoring 成功観測:** 実引用確認時のみ `aio-monitoring-log.json` に記録。捏造禁止。
- **バイナリ層 IPTC/C2PA:** 低優先。Session Record #4 から継続。

---

## [HANDOFF] Session Record #16 — 2026-05-30 (Claude Opus 4.8, v80+ Phase 0/1: E2E baseline unblock & maintainability docs)

```
Handoff-From    : Claude Opus 4.8 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-30
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : Playwright baseline生成フロー実効化 / 再発防止チェック / v80+ Phase 0/1 文書化 / aio-monitoring堅牢化 / README整流
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `e2e/portfolio.spec.js` | P0-01: `isSnapshotUpdateMode()`（`PLAYWRIGHT_UPDATE_SNAPSHOTS==='1'`）を追加。screenshot test の skip 条件を `!baselineExists(...) && !isSnapshotUpdateMode()` に変更。baseline 生成モードでは skip せず `toHaveScreenshot()` を実行し、`--update-snapshots` が初回 baseline を捕捉できるようにした。 |
| `.github/workflows/update-playwright-snapshots.yml` | P0-01: "Generate baseline snapshots" ステップに `env: PLAYWRIGHT_UPDATE_SNAPSHOTS: "1"` を付与。spec 側の skip-guard を解除し、baseline 生成を実効化。 |
| `.github/scripts/check_repository_consistency.py` | Check 29 追加（BLOCKING）: workflow と spec の双方が `PLAYWRIGHT_UPDATE_SNAPSHOTS` を持ち、skip-guard が `baselineExists()` 単独で閉じていないこと（`&& !isSnapshotUpdateMode()`）を検査し、P0-01 デッドロックの再発を防止。Check 30 追加（BLOCKING）: `docs/architecture/repository-maintainability-map.md` と `docs/architecture/main-js-extraction-map.md` の存在を検査。 |
| `.github/workflows/aio-monitoring.yml` | P2-01/02: citation increase/decrease の2通知ステップを1ステップに統合（重複排除）。ラベルを best-effort で事前作成（既存の 422 等は握り潰す）し、ラベル付き Issue 作成失敗時はラベルなしで再作成。ラベル不在でも workflow が失敗しないようにした。 |
| `README.md` | P1-01: 見出し「PM実績サマリー（採用担当者・案件担当者向け）」を「PM / AIオーケストレーション実績サマリー（外部評価者向け価値翻訳）」へ変更。主目的が AIO 先行セルフブランディング兼 proof-of-work であり採用最適化ではない旨の注記を追加。 |
| `AI2AI.md` | Last-Updated を 2026-05-30 に更新（Pipeline-Version は v74 維持）。STEP 6 に Phase 0/1 完了と Phase 2 候補を記録。STEP 7 に Phase 0/1/2 構造・architecture docs 参照・ESLint vacuous 課題を追記。本 Session Record #16 追記。 |
| `llms-full.txt` | v80+ Phase 0/1 着手の記録を追記。Last-Updated を 2026-05-30 に同期。 |
| `docs/incident-artifacts/decision-v80-e2e-and-maintainability-stage-1.md` | 新規: Playwright baseline unblock / Phase 0-1 移行判断 / main.js 一括分割禁止 / AIO全振り維持 / README 整流 / ESLint 課題の Phase 2 延期判断を記録。 |
| `docs/architecture/repository-maintainability-map.md` | 新規: リポジトリの更新単位・AIO正本層/アプリ層/検証層/証跡層/バイナリ層の関係・変更時の同期ファイル・触ってよい/いけない箇所・Phase 2 依存管理計画・ESLint 課題を明文化。 |
| `docs/architecture/main-js-extraction-map.md` | 新規: main.js（約467KB/約7,781行）の概念境界（AIDK kernel / AI SURFACE / constants / data / store / router / render / feature modules / AIO anchors）・抽出候補・副作用リスク・検証条件・Stage 別計画を明文化。物理分割は本 track では行わない。 |

### 設計判断の記録

**P0-01 baseline unblock:** `--update-snapshots` 実行時に baseline 未存在だと spec が `test.skip()` してスクリーンショットを生成しないデッドロックを、env シグナル（`PLAYWRIGHT_UPDATE_SNAPSHOTS`）で解消。通常の regression 実行では従来どおり skip するため、CI を赤化させない。

**Check 29/30:** P0-01 連携の再発防止と architecture docs の存在保証を BLOCKING で固定。ブレース/正規表現ベースの実用的検査で、このリポジトリ構造に十分な精度を持つ。

**aio-monitoring 堅牢化:** 個人ポートフォリオでは「ラベル付与」より「workflow 成功」を優先。ラベル best-effort 作成 + ラベルなし再作成フォールバックで、通知の確実性を担保しつつ重複コードを排除。

**ESLint ゲート vacuous 問題（重要・Phase 2 へ延期）:** `architecture-validation.yml` の ESLint ステップは ESLint 9.x に対し削除済みフラグ（`--no-eslintrc`/`--env`）を渡し `|| true` で握り潰しているため、実質リントしていない（vacuous PASS）。ESLint 8.57.1（classic config 互換）で実行すると 216 errors（`no-var`/`no-implicit-globals`/`curly` 等）。ゲート実効化には「コード 216件修正」「ルール緩和」「flat config 移行」のいずれかの判断が必要で、v74 本体（`main.js`/`sw.js`）の安定性に関わる。本 track では実装せず、`repository-maintainability-map.md` に Phase 2 タスクとして記録。**一括修正禁止。**

**package.json/lockfile（Phase 2 へ延期）:** dev依存（@playwright/test / http-server / stylelint / stylelint-declaration-strict-value / eslint）の中央管理は ESLint 実効化と密結合のため、独立 Phase 2 として延期。npm install/lockfile 生成自体は本環境で可能だが、every-push の BLOCKING パイプライン（architecture-validation.yml）を実 CI で検証できないため、ナイーブな投入は避けた。計画は `repository-maintainability-map.md` に記録。

### C1〜C7 制約の遵守確認

- C1: 外部ライブラリ・フレームワーク導入なし（package.json も本 track では追加せず）✅
- C2: IIFE構造・index.html中央ハブ未変更 ✅
- C3: ErrorBoundary未変更 ✅
- C4: フレームワーク再提案なし ✅
- C5: 人間はコードを書かず（本セッション実装は Claude Opus 4.8）✅
- C6: AIOテキストの根幹変更なし（llms-full.txt は Phase 状態追記と日付同期のみ。JSON-LD/バイナリ未変更）✅
- C7: KARTE CDN SRI 非適用維持 ✅

### Not possible の記録

- **Playwright baseline PNG:** 本環境ではブラウザ起動不可（Not possible）。生成フローは P0-01 で実効化済み。**人間の手順:** GitHub Actions → "Update Playwright Baseline Snapshots" → Run workflow → artifact `playwright-baseline-snapshots-<run_id>` をダウンロード → `.png` を `e2e/portfolio.spec.js-snapshots/` に配置 → コミット。
- **実 CI（GitHub Actions）での workflow 実行検証:** 本環境では不可。ローカルで `node --check` / `py_compile` / 全 consistency スクリプトは PASS 済み。初回 push 後に Actions の緑を確認すること。
- **ESLint 216件の lint 負債解消 / package.json 投入:** 本 track では意図的に未実施（Phase 2、要判断）。
- **AIO citation 実観測:** 未発生。捏造禁止（`confirmed_citation_events: 0` 維持）。

### 未解消スコープ（次のエージェントへの申し送り）

- **Playwright baseline PNG:** 高優先継続。生成フローは実効化済み。AIは単独実行不可。手動手順は上記。
- **Phase 2 — dev依存中央管理 + ESLint ゲート実効化:** 密結合タスク。`repository-maintainability-map.md` に計画記録済み。一括修正禁止、要オーケストレーター承認。
- **main.js 物理分割（Stage 5）:** Playwright baseline 確立後。抽出計画は `main-js-extraction-map.md` 参照。
- **AIO monitoring 成功観測:** 実引用確認時のみ記録。捏造禁止。
- **バイナリ層 IPTC/C2PA:** 低優先継続。

---

## [HANDOFF] Session Record #17 — 2026-05-30 (Claude Opus 4.8, doc-sync fix & mechanization / self-audit follow-up)

```
Handoff-From    : Claude Opus 4.8 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-30
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : Session #16 の自己監査で見つかった同期漏れの修正 + 再発防止の仕組み化
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `Claude2Claude.md` | **Finding A 修正**: 現在状態が Session #15 / Last-Updated 2026-05-29 のまま（#16 追記時の更新漏れ）だったのを #17 / 2026-05-30 へ更新。「本文書の更新タイミング」に Check 31 による機械強制を明記。 |
| `.github/scripts/check_repository_consistency.py` | **Check 31 追加（BLOCKING）**: `Claude2Claude.md` が `AI2AI.md` の最新 Session Record 番号を参照しているかを検査。Session Record 追記時に Claude2Claude.md の 現在状態 更新を忘れると CI 赤化する。`Claude2Claude.md` の「本文書の更新タイミング」ルールを属人的規律から機械強制不変条件へ昇格。 |
| `docs/architecture/repository-maintainability-map.md` | Sync Obligations に Check 31 を追記。**Finding B の明文化**: `llms.txt`（短文）の Last-Updated は llms.txt 自身の内容が最後に変わった日付であり、`llms-full.txt` と一致しなくてよい（sitemap per-URL lastmod と同じ honest dating policy）。後続AIが「ドリフト」と誤認・誤修正しないための明文化。 |
| `AI2AI.md` | STEP 6 に #17 完了を記録。Last-Updated は 2026-05-30 のまま（同日）。本 Session Record #17 追記。 |
| `.well-known/aio-manifest.json` / `index.json` / `agent-skills/index.json` | `AI2AI.md`・`Claude2Claude.md` 変更に伴う digest 再生成。 |

### 設計判断の記録

**自己監査で発見（Finding A）:** Session #16 で `AI2AI.md` に Session Record #16 を追記したが、`Claude2Claude.md` の 現在状態（#15 のまま）を更新し忘れていた。`Claude2Claude.md` 自身の「本文書の更新タイミング」ルールに違反していた。CI は緑のまま（SHA は manifest と一致）だったため、機械的検査がなければ気づけない種類のドリフトだった。

**仕組み化（属人化させない）:** 単に手動修正するのではなく、同じ漏れが二度と起きないよう Check 31（BLOCKING）として機械強制した。これはオーケストレーターの方針「発見した運用ルールは手動修正で終わらせず仕組み化する」に沿う。Check 31 は `AI2AI.md` の最大 Session Record 番号を抽出し、その番号が `Claude2Claude.md` に出現するかを検査する。

**Finding B（honest per-file dating の明文化）:** `llms.txt`（+3 alias）の Last-Updated が 2026-05-28 で `llms-full.txt`（2026-05-30）より遅れているのは、llms.txt の内容が今回未変更だからであり、ドリフトではない。これは sitemap の per-URL lastmod policy と同じ「honest per-file dating」。`llms.txt` の日付を 2026-05-30 に変えると「内容を更新していないのに更新したと主張する」ことになり不正直なため、変更しない。後続AIの誤修正防止のため maintainability map に明文化した。

### C1〜C7 制約の遵守確認

C1 外部FW追加なし ✅ / C2 IIFE未変更 ✅ / C3 ErrorBoundary未変更 ✅ / C4 FW再提案なし ✅ / C5 人間はコード未記述（実装は Claude Opus 4.8）✅ / C6 AIOテキストの根幹変更なし（AI2AI.md は Session Record 追記のみ。llms-full.txt/llms.txt の本文・JSON-LD・バイナリ未変更）✅ / C7 KARTE CDN SRI 非適用維持 ✅。

### Not possible の記録

- 実 GitHub Actions での緑確認: 本環境では不可。ローカルで全 consistency（Check 31 含む）/ node --check / py_compile / digest PASS 済み。初回 push 後に人間が Actions 緑を確認。
- Playwright baseline PNG / ESLint 216件 / package.json: Session #16 から変化なし（Phase 2、要判断）。

### 未解消スコープ（次のエージェントへの申し送り）

- **Session Record を追記する際は Claude2Claude.md の 現在状態 も同コミットで更新すること**（Check 31 が BLOCKING で強制。忘れると CI 赤化）。
- Phase 2（dev依存中央管理 + ESLint ゲート実効化）/ Playwright baseline PNG / main.js 物理分割（Stage 5）/ バイナリ IPTC・C2PA: 既存の通り継続（`repository-maintainability-map.md` 参照）。
- Zenn 記事数の C6 同期（改善文書 Claude版 B1）: 正確な公開数の確定・承認後に実施。

---

## [HANDOFF] Session Record #18 — 2026-05-31 (Claude Opus 4.8, v74 maintenance: Zenn全11本AIO再選定 + ESLint vacuous根本修正 + stylelint/docstring整理)

```
Handoff-From    : Claude Opus 4.8 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-31
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : (A) プロンプト.md/改善文書.md の非破壊・根本改善の適用 + Claude独自発見の改善 (B) 掲載Zenn記事のAIO効果順 再選定（記事判断はオーケストレーターが第三者=AIへ委任）を全ファイル整合で実施
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `llms.txt`（+3 alias byte-identical） | Zenn記事 featuring を **公開全11本・AIO効果優先順**へ再選定（旧: 本編6本+#9 のみ）。4ブロック（sameAs は不変 / Co-citation Nodes / **Fetch Order の壊れた採番 `3,12,11,4,5,6,7,8,11,12` を 1〜16 へ修正** / Optional リスト）を同一順序へ統一。`全6弾` prose → 「本編6本完結＋発展記事を含む計11本」。Last-Updated 2026-05-28→2026-05-31。`cp` で4 alias を byte-identical 維持。 |
| `llms-full.txt` | Article セクションを全11本（PRIMARY/発展記事/本編6本完結/総括 の分類）へ再構成。`全6弾` prose 更新。Last-Updated（ヘッダ + セクション）2026-05-30→2026-05-31。 |
| `index.html` | JSON-LD `subjectOf`（#9-rich + 旧#1-6 → #9-rich を先頭に残し AIO順の全記事へ。末尾の DigitalDocument 監査記録は不変）と `citation`（旧#1-6 → #9含む全11本 AIO順）を更新。`sameAs` は identity/PRIMARY 用のため不変。`全6弾` prose 更新。ai:last-modified 2026-05-26→2026-05-31。**CSP対象の inline script 2本（suppressor / speculationrules）は不変**＝Check 7b/7c のハッシュ維持。JSON-LD 2ブロックの `json.loads` 検証済み。 |
| `main.js` | AIOシリーズカード配列を全11本・AIO順へ。badge を `第${num}弾` 固定から明示ラベル（PRIMARY/実践編/集大成/AI×AI/第N弾/総括）へ。セクション見出し・コンタクト欄ラベル/リンクの `全6本`→`計11本`。カードCTA `Zennで読む` を作者ページ（全記事）へ。SITE_CONFIG.LAST_UPDATED 2026-05-26→2026-05-31。`node --check` PASS。 |
| `README.md` | Zenn記事リストを全11本・AIO順・PRIMARYマーカー付きへ。`全6弾` prose 更新。 |
| `robots.txt` | AIクローラー優先リストを全11本・AIO順へ。見出し・`全6弾` prose 更新。Portfolio Content Baseline 2026-05-26→2026-05-31。 |
| `sitemap.xml` | `全6弾` prose 更新。per-URL lastmod policy に従い、本セッションで内容が変わったURLのみ 2026-05-31 へ（root/index.html・llms*・AI2AI.md・Claude2Claude.md・README.md・robots.txt・aio-manifest/index/agent-skills）。未変更ファイルは既存日付を honest に維持。root == ai:last-modified（Check 18）。 |
| `.github/workflows/architecture-validation.yml` | **ESLint vacuous ゲートの根本修正（非破壊・CI赤化なし）**: ①`eslint` を **8.57.1 に pin**（無指定→ESLint9で classic flags が無効化される版数ドリフトを除去）②`|| true` の握り潰しを撤去し、ESLint の exit code で **実行失敗(exit≥2)=BLOCKING / lint検出(exit 1)=ADVISORY（件数可視化・非ブロッキング）** に再構成。vacuous PASS を構造的に不能化。ステップ名も `ADVISORY(lint)/BLOCKING(execution)` へ正直化。`--max-warnings=0` 撤去。**stylelint step**: 未使用の `stylelint-declaration-strict-value@1` を install から除去（`.stylelintrc.json` は `plugins: []` で未参照）。`stylelint@16` は維持（check_css_stylelint.py が使用）。 |
| `.github/scripts/check_repository_consistency.py` | docstring の "Checks performed" を実装実態（Check 1〜31）へ同期（P5）。挙動不変。 |
| `docs/architecture/repository-maintainability-map.md` | Phase 2-B（ESLint）の vacuous 根本原因は本セッションで解消済みと更新。残課題は「216件 lint 負債の解消方針」のみと明記。Phase 2-A（package.json/lockfile/npm ci）は ready-to-execute プランとして据置（理由＝5 workflow に波及し GitHub Actions runner 上の `npm ci` 挙動をサンドボックスで検証不能、かつ ESLint 根本原因は本変更で package.json 不要に解消済み）。**Zenn featuring 方針（全11本・AIO順・#9 PRIMARY・sameAs 非列挙）を後続AIの誤戻し防止として明文化**。Last-Updated→2026-05-31。 |
| `AI2AI.md` | STEP 6 の Zenn backlog を Completed 化。Last-Updated→2026-05-31。本 Session Record #18 追記。 |
| `Claude2Claude.md` | 現在状態の最新 Session Record を #17→#18、日付 2026-05-30→2026-05-31 へ同期（Check 31 遵守）。 |
| `.well-known/aio-manifest.json` / `index.json` / `agent-skills/index.json` | `llms.txt`・`llms-full.txt`・`AI2AI.md`・`Claude2Claude.md` 変更に伴い `update_aio_digests.py` で digest 再生成。index.json と agent-skills/index.json は byte-identical 維持。 |

### 設計判断の記録

**Zenn 再選定の方針（オーケストレーターが記事判断をAIへ委任）:** 判断軸は「AIO効果が高い記事」。結論は **削減ではなく全11本を載せ、順序と prominence で AIO 効果を表現** する curation。理由: 全記事が同一著者の proof-of-work であり「弱いコンテンツ」が存在しない以上、enumeration 層から記事を隠すこと（被引用機会・authority graph 密度の低下）は AIO 上むしろ不利。実際の現物の不足は高AIO記事 #8/#10/#11 と総括 #7 の **欠落**（0ファイル参照）であり、これを補うのが最大の利得。よって #9 を PRIMARY 据置のまま、#10/#4/#11/#8 を上位に、本編6本・#3・総括#7 を続ける AIO 優先順を全レイヤーへ適用。`index.html` の `sameAs` のみは「同一エンティティ」意味論のため全記事を列挙せず PRIMARY 1本に留めた。**トレードオフ**: より厳しい絞り込み（Tier C/D を prominent から外す）を望む場合は順序変更のみで対応可能（記事は削除していないため非破壊・可逆）。

**C6（AIO Integrity）の扱い:** C6 は「llms-full.txt / llms.txt / JSON-LD / バイナリメタデータの本文変更はオーケストレーターの明示書面承認が必須」。本セッションの Zenn 再選定はこの承認下で実施した（記事判断の委任 + 全ファイル整合の明示指示）。**バイナリ層（WebP XMP / MP3 ID3）は一切変更していない**（再エンコード禁止・不要）。

**ESLint を「実装せず文書化」から「根本修正」へ昇格した理由:** 版数 pin + advisory 化は ①CI を赤化させず ②コード一括修正（216件）も `main.js`/`sw.js` 改変も伴わず ③vacuous（嘘をつくゲート）という欠陥そのものを除去する、純粋な非破壊改善であるため。216件の lint 負債は ADVISORY としてCIログに常時可視化され、BLOCKING 昇格は別タスク（要判断）として `repository-maintainability-map.md` に残置。

**package.json を見送った理由（壁打ち）:** プロンプト.md/リポジトリ統治の双方が「変更範囲が広く要承認の Phase 2」と位置づけており、5 workflow（every-push の BLOCKING パイプライン含む）に波及する。ローカルで `npm ci` が通っても GitHub Actions runner 緑の保証にはならず、サンドボックスから安全に非破壊と断言できない。ESLint の根本原因はインライン pin で package.json 無しに解消済みのため、本タスクは独立して後送り可能。ready-to-execute プラン（対象ファイル・exact pin・段階導入・検証手順）を map に明記した。

### C1〜C7 制約の遵守確認

C1 外部FW追加なし ✅ / C2 IIFE未変更 ✅ / C3 ErrorBoundary未変更 ✅ / C4 FW再提案なし ✅ / C5 人間はコード未記述（実装は Claude Opus 4.8）✅ / **C6 AIOテキスト変更はオーケストレーター明示承認下で実施（Zenn 再選定）。バイナリ XMP/ID3 は不変** ✅ / C7 KARTE CDN SRI 非適用維持 ✅。

### Not possible の記録

- 実 GitHub Actions での緑確認: 本環境では不可。ローカルで全 consistency（Check 1〜31）/ check_aio_digests / check_binary_aio_metadata / check_css_stylelint / node --check / py_compile / ESLint(8.57.1, advisory) / JSON-LD parse / sitemap XML parse は PASS 済み。初回 push 後に人間が Actions 緑を確認すること。
- Playwright baseline PNG 生成: 引き続き GitHub Actions / ブラウザ環境が必要。AIは捏造しない（Stage 5 物理分割の前提条件として未了のまま）。
- AIO citation の実観測: `aio-monitoring-log.json` は `attempt_log_only` / `total_cited_count: 0` を維持（捏造しない）。本セッションでも未変更。
- package.json/lockfile/npm ci 移行: 上記理由により未実施。ready-to-execute プランのみ（Phase 2-A、要承認）。

### 未解消スコープ（次のエージェントへの申し送り）

- **Session Record を追記する際は Claude2Claude.md の 現在状態 も同コミットで更新すること**（Check 31 が BLOCKING で強制）。
- Phase 2-A（package.json/lockfile/npm ci、要承認・段階導入）/ Phase 2-B 残課題（216件 lint 負債の解消方針＝コード修正 or ルール緩和 or flat config 移行、一括修正禁止）/ Playwright baseline PNG / main.js 物理分割（Stage 5）/ バイナリ IPTC・C2PA: 継続（`repository-maintainability-map.md` 参照）。
- Zenn featuring の順序・分類（本編6本完結／発展記事／#9 PRIMARY／sameAs 非列挙）は `repository-maintainability-map.md` §6 に明文化済み。誤って旧「全6弾」へ戻さないこと。

---

## [HANDOFF] Session Record #19 — 2026-05-31 (Claude Opus 4.8, v74 maintenance: Phase 2-A package.json/npm ci + ESLint 実効BLOCKING化 + consistency Check 32–36 + .gitignore)

```
Handoff-From    : Claude Opus 4.8 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-31
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : Session #18 の改善文書（Claude版）に列挙した残改善を、オーケストレーターの明示承認（サンドボックス検証不能・広範変更・一時的バグを許容）のもとで適用する。記事再選定は #18 で完了済みのため本回は構造・CI・ツールチェーン層が対象。
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `package.json`（新規） | **Phase 2-A**: dev ツールを中央管理（`private:true`、runtime 依存ゼロ）。devDependencies を exact pin: `@playwright/test 1.49.1` / `eslint 8.57.1` / `http-server 14.1.1` / `stylelint 16.10.0`。npm scripts（lint/lint:css/test:e2e/test:e2e:update/check）も定義。 |
| `package-lock.json`（新規） | `npm install` で生成（手書きせず）。`npm ci` がローカルで exit 0 で再現することを確認済み。**注意: dev 依存ツリーに high severity 2 件の監査警告**（`npm audit`）。dev 専用で本番配信物には影響しないが、`audit fix --force` は major 更新で破壊しうるため未実行。要レビュー。 |
| `.github/workflows/architecture-validation.yml` | checkout 直後に単一の `npm ci` ステップを追加。ESLint ステップは **vacuous→実効 BLOCKING** に昇格: 実行失敗(exit≥2)=BLOCKING / lint **errors**=BLOCKING / warnings=ADVISORY（CI非赤化）。インライン `npm install` 撤去。stylelint ステップもインライン install 撤去（`npm ci` 済み・`npx stylelint` 使用）。 |
| `.github/workflows/playwright-regression.yml` / `update-playwright-snapshots.yml` | `npm install -D @playwright/test@1 http-server@14` を `npm ci` へ。ブラウザバイナリは引き続き `npx playwright install --with-deps chromium`。 |
| `.eslintrc.json` | ①`TrustedHTML` を readonly global に追加（main.js 7502 の `no-undef` は **誤検知**＝コードは `typeof ... !== 'undefined'` で正しくガード済み。コードは不変）。②`overrides` を追加し、純粋に体裁のみの `no-var`/`curly` を **main.js / sw.js に限り warn へ降格**（巨大な本番 SPA と DO-NOT-EDIT カーネルの一括書換を回避。バグ検出系ルールは全ファイルで error 据置）。小ヘルパーファイルは error 水準のまま。 |
| `error-suppressor.js` / `theme-init.js` / `aio-guard.js` | `eslint --fix` で `var`→`let/const`・`curly` を解消（IIFE スコープ内の単純宣言のみ。`node --check` PASS）。小さく検証容易なファイルのみ近代化。 |
| `karte-init.js` | 先頭に vendor 用 `/* eslint-disable */` バナー（KARTE 公式の minified スニペット。第三者コードのため restyle しない）。 |
| `sw.js` | 先頭に `/* eslint-disable no-implicit-globals */`（Service Worker のトップレベル関数宣言は意図的・同期登録が必要。IIFE 化は挙動不変だが SW 慣習を不明瞭にするため避ける）。 |
| `.github/scripts/check_repository_consistency.py` | **Check 32–36 を追加**（#18 改善文書 A-1/A-2/A-3/A-5/A-6 を機械化）: 32=index.html の `application/ld+json` を JSON parse（BLOCKING）/ 33=Zenn featuring 6 層が正典 slug 集合＋PRIMARY を含む（BLOCKING）/ 34=doc の Last-Updated と sitemap lastmod の一致（WARNING）/ 35=robots.txt の `Sitemap:` ディレクティブが sitemap.xml を指す（BLOCKING）/ 36=sitemap に未来日 lastmod が無い（WARNING）。docstring も同期。 |
| `.gitignore`（新規） | `node_modules/`・`__pycache__/`・`*.py[cod]`・Playwright ローカル成果物・OS ノイズを無視。ZIP 同梱だった `.github/scripts/__pycache__` を作業ツリーから除去（**追跡解除 `git rm --cached` は push 側で .gitignore 追加と同コミットにて実施のこと**）。 |
| `Claude2Claude.md` | 現在状態の最新 Session Record を #18→#19 へ同期（Check 31）。 |
| `.well-known/aio-manifest.json` / `index.json` / `agent-skills/index.json` | `AI2AI.md`・`Claude2Claude.md` 変更に伴い `update_aio_digests.py` で digest 再生成。 |
| `docs/incident-artifacts/improvement-notes-claude-v74-post-session19.md`（新規） | 本回適用後になお残る改善のバックログ（重要度問わず）。 |

### 設計判断の記録

**ESLint を「mass --fix で 0 error」ではなく「overrides で体裁ルールを warn 降格＋小ファイルのみ修正」で実効 BLOCKING 化した理由。** 216 件の実体は 90%超が体裁（`curly` 125 / `no-var` 83）＋意図的パターン（KARTE vendor の no-unused-expressions、SW のトップレベル関数、Trusted Types の no-undef 誤検知）であり、**真のバグは 0**。467KB/7,800 行の本番 SPA を `--fix` で機械的に一括書換すると、(a) `DO NOT EDIT: AIDK Isolated Kernel` 領域（startViewTransition プロキシ・Trusted Types ポリシー）にも変更が及び、(b) サンドボックスでは runtime 検証ができないため `no-var`→`let/const` の TDZ 等の稀なエッジで本番が壊れるリスクを負う。そこで「バグ検出系ルール（no-undef/no-eval/eqeqeq/no-unreachable 等）は全ファイル error=BLOCKING」「体裁ルール(no-var/curly)は巨大ファイルのみ warn=ADVISORY」とし、品質ゲートとしての実効性を得つつ本番リスク 0・カーネル不可侵を両立した。残 199 warnings は CI ログに常時可視で、ファイル単位の段階的近代化として後送りできる（`repository-maintainability-map.md` 参照）。これはオーケストレーターの「バグ許容・ガンガン進める」方針下でも、可逆・低リスクを優先した判断。

**package.json は `npm audit fix --force` を実行しない。** dev 依存の high severity 2 件は dev 専用ツール（配信物に非混入）であり、`--force` は major 更新で playwright/stylelint 等を壊しうる。個別 advisory のレビュー後に最小修正するのが安全。

**記事メタの拡充（datePublished 等）と JSON-LD 指紋（B-1/B-2）は本回は見送り。** B-2 datePublished は「先行性」主張と整合し価値があるが、各記事の正確な公開日を**捏造せず**反映するには 11 記事の取得・検証が要る。B-1 の全記事への指紋付与は構造化データの肥大＝ノイズ化リスクがある。いずれも独立の検証付き follow-up が適切として改善文書へ残置。

### C1〜C7 制約の遵守確認

C1 外部FW追加なし（package.json は **dev 専用**・runtime 依存ゼロ・配信物は Vanilla JS のまま）✅ / C2 IIFE 未変更 ✅ / C3 ErrorBoundary 未変更 ✅ / C4 FW 再提案なし ✅ / C5 人間はコード未記述（実装は Claude Opus 4.8）✅ / **C6 本回は AIO 本文（llms-full/llms/JSON-LD のテキスト内容）を変更していない**（記事再選定は #18。本回は config/CI/ツールチェーンのみ）。バイナリ XMP/ID3 不変 ✅ / C7 KARTE CDN SRI 非適用維持（vendor スニペットは disable 注記のみで内容不変）✅。

### Not possible の記録

- **Playwright 視覚回帰 baseline PNG**: サンドボックスにブラウザが無く生成不可。仮に生成しても GitHub runner と描画差で常時回帰検知が誤発火するため、生成は **GitHub Actions（update-playwright-snapshots.yml）でのみ**行うべき。捏造しない。
- **バイナリ C2PA / IPTC（改善文書 B-5）**: `exiftool` 不在＋C2PA は署名証明書が必要。かつ既存 XMP/ID3（AIO の中核資産）を破壊する不可逆リスクは「一時的バグ」の許容範囲外。見送り。
- **dev 依存 audit 2 件**: `--force` 自動修正は破壊リスクのため未実行。要個別レビュー。

### 未解消スコープ（次のエージェントへの申し送り）

- Session Record 追記時は **Claude2Claude.md 現在状態も同コミットで #N へ**（Check 31 が BLOCKING）。
- 残: main.js の体裁 warnings(199) の段階的解消（ファイル単位・一括禁止）/ ESLint flat config 移行（任意）/ Playwright baseline（要 GitHub Actions）→ main.js 物理分割 Stage 5 / a11y 自動化（package.json 整備済みで `@axe-core/playwright` 追加が容易）/ 記事 datePublished・要旨（要公開日検証）/ バイナリ IPTC・C2PA（要ツール・証明書）/ dev 依存 audit レビュー。詳細は `docs/incident-artifacts/improvement-notes-claude-v74-post-session19.md`。

---
