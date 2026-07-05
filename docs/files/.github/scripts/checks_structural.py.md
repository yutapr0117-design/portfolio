---
file: .github/scripts/checks_structural.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol)
---

# .github/scripts/checks_structural.py

## What

`check_repository_consistency.py` 分割トラックの 2 つ目の split module（1 つ目は `checks_maintainability.py`）。structural parse / CI wiring / tooling 系（category E）の Check 48-51 を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 48**: Playwright baseline-commit pipeline permission coupling（workflow 権限整合）。
- **Check 49**: index.html JSON-LD worksFor ↔ Organization linkage integrity。
- **Check 50**: ESLint flat-config migration integrity（50a-…）。
- **Check 51**: active-runbook Playwright baseline-generation version が pin と一致。

## Why

owner 合意 C-first の check.py 段階分割（Phase 5）。48-51 は `_NN` 接尾辞 local を持ち対象ファイル（workflow / index.html / eslint.config.mjs / package.json / runbook）を fresh read する **self-contained cluster** ゆえ安全に抽出できた。**Check 47（ESM 契約）は `_modules47`（js-leaf source-of-truth リスト）を Check 56/57/61 と共有する coupled infrastructure ゆえ Phase 5 時点では monolith に残置**していた（抽出試行で consistency check が NameError で即検知→revert した実例。安全網が機能）。**Phase 6 でこの coupled cluster（47/56/57/61）はリスト定義＋全消費者ごと `checks_esm.py` へ一括抽出済**（共有変数が module-local 化して結合解消）。

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、**元の実行位置（Check 47 の後・53 の前）**で `checks_structural.run(_ctx)` を呼ぶ（順序保存）。
- `ctx.check`/`ctx.errors`/`ctx.warnings` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory と section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **クラスタ分離**: `_modules47` に依存する Check（47/56/57/61）は `checks_esm.py` が所有（本 module には入れない）。両 module は独立した category ゆえ変数を共有しない。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `structural`, `category-e`, `ctx-injection`
- **2 つ目の split module = 多 module パターンの確立**。Phase 6+ は category ごとに `checks_<cat>.py` を増やす。**教訓: 抽出前に「その check の `_NN` 変数が他 check から参照されていないか」を grep で確認するか、抽出→consistency check の NameError で判別する（`_modules47` class の shared-infra を踏まないため）。**

### For human engineers（新卒レベル）
- 巨大 1 ファイルを「役割別の小ファイル」へ切り出す 2 個目。ある検査が別の検査と変数を共有していると単独では切り出せない（Check 47 がその例だった）— 機械（consistency check）が即座に教えてくれる。共有している相棒同士をまとめて切り出せば独立できる（それを Phase 6 で `checks_esm.py` として実施）。

### For third parties / auditors
- 分割時に「共有インフラ変数を持つ Check は残す」判断を、安全網（consistency check の NameError）で機械的に確認しながら進めた透明な記録。
