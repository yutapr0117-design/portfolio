---
file: .github/scripts/checks_esm.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md (Phase 6 = coupled-group 抽出)
---

# .github/scripts/checks_esm.py

## What

`check_repository_consistency.py` 分割トラックの 3 つ目の split module（1=`checks_maintainability.py` / 2=`checks_structural.py`）。**`_modules47`（js-leaf source-of-truth リスト）と `_main_src47`（main.js source）を共有する coupled cluster** を、リスト定義とその全消費者ごと 1 module へまとめて抽出したもの。`run(ctx)` で monolith から呼ばれる。

- **Check 47**: main.js ⇄ js/ 各葉モジュールの ESM import/export bijection と葉性（47a/47b/47c）。
- **Check 56**: js/ 葉モジュールの factory パターン引数被覆（factory export → main.js で createXxx 呼出）。
- **Check 57**: index.html modulepreload 集合 と `_modules47` 集合の完全一致。
- **Check 61**: 各 js/ 葉モジュールが factory pattern を export する場合、docstring に "factory pattern" マーカーを含む。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 6**）。Phase 1-5 で readily-self-contained なクラスタ（Check 16/28/29/30/42/48-52/71/361-364）を抽出し尽くした後の、質的に難度の高い **coupled-group 一括抽出** の初例。Check 47 が定義する `_modules47` を Check 56/57/61 が共有参照するため、Phase 5 までは monolith に残していた（分割の相棒同士を引き剥がすと `NameError: _modules47` になる）。**リスト定義＋全消費者をまとめて 1 module へ移せば、共有変数が module-local になり結合が解消される**。各 Check は対象ファイル（main.js / index.html / 各葉モジュール）を自前で `read_text()` するため、global content（html/mainjs 等）への依存はなく ctx enrich は不要だった。

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、**Check 47 の元の実行位置**で `checks_esm.run(_ctx)` を呼ぶ。56/57/61 は元は 53-60 の間に散在していたが、本 module では 47 の直後に連続実行される（各 Check は共有 errors/warnings に append するだけゆえ **順序非依存**・exit code は byte-equivalent）。
- `_modules47` と `_main_src47` は `run()` 内の module-local 変数として先頭で構築され、47/56/57/61 の全参照がその 1 定義を共有する。
- `ctx.check`/`ctx.errors`/`ctx.warnings` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  47.`/`  56.`/`  57.`/`  61.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **クラスタの完全性**: `_modules47`/`_main_src47` を参照する Check は必ず本 module 内に置く（monolith 側に取り残すと NameError）。将来 `_modules47` を参照する新 Check を足す場合も本 module へ。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 15,066 → 14,717（−349・Phase 6）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `esm-contract`, `coupled-group`, `ctx-injection`, `phase6`
- **coupled-group 一括抽出パターンの確立**。§4.1 handoff が示した「消費側とセットで一括抽出」を実施した初例。**教訓: 共有変数（`_modules47` 型）に結合した Check 群は、変数定義＋全消費者を同一 module へ移せば結合が解消される。抽出前に `grep '_modules47' check.py` で参照範囲を確認し、全参照が同一クラスタ内に閉じることを確かめてから移す。**
- Phase 6 以降の残ターゲット: `_ctx` enrich（html/mainjs/ai2ai/style/mcp_data）が必要な大カテゴリ（AIO 系 / SEO 系 / version 系）。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 3 個目。今回は「ある検査が別の検査と共有している変数（js モジュール一覧）」ごと 4 つの検査をまとめて移した。相棒同士を一緒に動かせば、共有していた変数がその小ファイルの中だけの変数になり、綺麗に独立する。

### For third parties / auditors
- 「共有インフラ変数を持つ Check は残す」（Phase 5 まで）から「共有変数＋全消費者をまとめて抽出する」（Phase 6）への前進。各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が 3+1 ファイル横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録。
