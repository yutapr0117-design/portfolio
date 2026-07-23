---
file: .github/scripts/checks_maintainability.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-23
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol)
---

# .github/scripts/checks_maintainability.py

## What

`check_repository_consistency.py`（元 15,913 行の中央 registry）から切り出した最初の split module。file-size / maintainability / test-health / check-infra 系の Check を内包し、`run(ctx)` で monolith から呼ばれる。**現在の全 Check（15 個・番号の権威は `# ── N.` section と Check 45）**: 16 / 28 / 29 / 30 / 42 / 52 / 71 / 361 / 362 / 363 / 364 / 365 / 379 / 380 / 385。下記の Phase 履歴は分割トラックでの抽出経緯であり、365（全非 A テキスト ≤1,000 capstone）/ 379-380（mutation-integrity mesh）/ 385（checks_*.py ctx.warnings/errors unpack）は分割後に別 increment で追加した。

- **Phase 1（#577）**: Check 361-364（js-leaf BUDGET-DATA 登録 / mutation anchor 解決 / js-leaf 1,000 行上限 / store.js ingestion array-op 安全）。
- **Phase 2（#579）**: Check 52（file-size budget advisory）+ 71（BUDGET-DATA path existence）を追加（file-size governance cluster を集約）。**非連番 Check の抽出 + 既存 module への join パターン**を確立。
- **Phase 3（#581）**: Check 28（e2e no nested test）+ 29（Playwright baseline-generation linkage）+ 30（maintainability anchor docs 存在）を追加（test-health cluster・連続ブロック 3281-3393 の一括抽出）。
- **Phase 4（本 PR）**: Check 16（e2e screenshot baseline-skip guard）+ 42（docs artifact placement/naming hygiene 42a/42b）を追加（非連番・test/docs health）。monolith 15,507→15,426。

## Why

owner との 2026-07-05 議論タイムで合意した「残存肥大化の解消を C-first で再開」の**最優先ターゲット = check.py（15,913 行）**を、自己言及的（自身の構造を検証する Check 45/70/105 を内包）ゆえ安全プロトコルで段階分割する、その **Phase 1 = 最初の 1 カテゴリ抽出 PoC**。#253 が「check.py 物理分割は net-negative」と評価した唯一の根拠 `exec()` の脆さ（自由変数の静的解決不能・未定義グローバル参照）を、**exec を使わず `run(ctx)` への明示 context 注入**で回避し、net-positive を実証する。

## How

- monolith が `_ctx = types.SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、`checks_maintainability.run(_ctx)` を「元の 361-364 と同じ実行位置・順序」で呼ぶ。
- `ctx.check` / `ctx.errors` / `ctx.warnings` は **monolith と同一の関数・list オブジェクトの参照**。抽出 Check の `check()` 呼び出しも同じ errors/warnings に append する = **挙動 byte-equivalent**。
- `_aggregate_check_numbers()`（monolith）が `CHECK_SOURCE_FILES`（本ファイルを含む）を横断し、本 module の docstring inventory（`  361.`..`  364.`）と body の `# ── N.` section header を集約。よって自己整合 Check 45/70/105 の bijection は本ファイルも跨ぐ。
- section header は `run(ctx)` 内で 4-space インデントされるため、monolith の `_sec_re` を `^\s*#\s*──` へ緩和（leading whitespace 許容）した。

## Constraints

- **葉契約に相当（module-global 結合なし）**: 依存は全て `ctx` 経由。`re` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory と `# ── N.` section は 1 対 1、かつ monolith の docstring/section と合わせて 1..N 連番・check-map・runbook §9 と bijection。
- **behavior-identical**: 抽出 Check の合否・errors/warnings への寄与は抽出前と同一（同一 list 参照）。
- **Check 108**: 本 mirror doc（`docs/files/.github/scripts/checks_maintainability.py.md`）が tracked-file bijection を満たす。
- **Check 10**: `.github/scripts/*.py` syntax 検証対象。

## Change impact

- 新規 split module ゆえ Check 108（mirror bijection）が本 doc を BLOCKING で要求。
- Check を追加/移動する際は「impl（`# ── N.` section）+ docstring inventory `  N.` + check-map 行 + runbook §9」の 4 面同期が monolith 時と同じく必要（本 module 内で完結・自己整合 Check が跨いで検証）。
- 将来 Phase 2+ で他カテゴリを別 module へ抽出する際も本ファイルと同じ `run(ctx)` + CHECK_SOURCE_FILES 登録パターンを踏襲する。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `maintainability`, `phase1-poc`, `ctx-injection`
- **check.py 分割の re-usable パターンの雛形**。Phase 2+ は「①孤立カテゴリ選定（monolith global html/mainjs 等に依存せず ROOT/check/warnings のみ使う Check 群）→ ②`checks_<cat>.py` に `run(ctx)` で移設（section は +4 indent・docstring inventory も移す）→ ③CHECK_SOURCE_FILES 登録 → ④verify で 45/70/105 緑を確認 → ⑤mirror doc」。
- **落とし穴**: 抽出対象が monolith の共有 computed 変数（例: `html_v` を後続 check が使う）に依存していると壊れる。ctx は list/helper の参照は渡すが check 間の computed state は渡さない。孤立カテゴリを選ぶこと。

### For human engineers（新卒レベル）
- 巨大な 1 ファイルを、挙動を変えずに「テーマ別の小さいファイル」へ分ける最初の一歩。`ctx`（context）= 元ファイルの道具箱（check 関数・エラー記録リスト等）を引数で手渡すことで、切り出した側も同じ道具を使える。

### For third parties / auditors
- 過去に「net-negative」と評価した判断（#253）を、根拠（exec の脆さ）を特定し別手法（明示 ctx 注入）で覆した透明な記録。PoC ゆえ小さく（4 check・~180 行削減）始め、全 Check 緑 + 自己整合維持で net-positive を実証してから段階拡大する慎重路線。
