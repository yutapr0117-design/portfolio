---
file: .github/scripts/checks_ci_supply.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_ci_supply.py

## What

`check_repository_consistency.py` 分割トラックの 9 つ目の split module（1=maintainability / 2=structural / 3=esm / 4=tooling / 5=entity / 6=docs_mirror / 7=aio_derived / 8=app_route）。CI trigger/coverage と supply-chain surface を守る連続クラスタ Check **142-145** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 142**: Playwright e2e gate covers its own toolchain（playwright-regression.yml paths に package.json/lock を含む）。
- **Check 143**: Auto-digest workflow covers every digested manifest file（11 件被覆）。
- **Check 144**: Digest-regen tool's file map matches the manifest（`MANIFEST_PATH_TO_LOCAL` ↔ manifest bijection・**ast で dict 抽出**）。
- **Check 145**: GitHub Actions are pinned to a full commit SHA（supply-chain hardening）。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 12**）。142-145 は「CI trigger/coverage & supply-chain hardening」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（workflow YAML / update_aio_digests.py / aio-manifest.json）を自前で `read_text()` し、global content（html/style/mainjs）依存はない。全局所変数が `_NNN` 接尾辞で section 内に閉じる。ctx enrich 不要で安全に一括抽出できた。**教訓: Check 144 は `ast` を使う — 抽出コードが使う stdlib（re/json 以外の ast 等）は module import 必須。初回抽出で `NameError: name 'ast'` が出て安全網が検知 → `import ast` を追加して解消した。**

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、**元の実行位置（Check 141 の後・146 の前）**で `checks_ci_supply.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json, ast`（144 が ast を使用）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json`/`ast` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  142.`〜`  145.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **クラスタの完全性**: 142-145 の局所変数を参照する Check は必ず本 module 内に置く。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 13,711 → 13,467（−244・Phase 12）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `ci`, `supply-chain`, `workflow-coverage`, `ctx-injection`, `phase12`
- **連続 self-contained クラスタ抽出**。**教訓: 抽出コードが使う stdlib を必ず module import する（142-145 の 144 は `ast`）。初回 NameError が出たら stdlib import 漏れを疑え — 安全網（consistency check の NameError → exit 1）が確実に捕捉する。**
- 残ターゲット候補: 133-134（wiring・135 は style 依存で ctx enrich 要）/ 128-132（behavioral guards）/ 141+146（default-project integrity・非連続）/ 104/106/107/109（CI/node config・105/108 除外）/ ctx enrich が必要な html 系大カテゴリ。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 9 個目。今回は「CI が正しいタイミングで走るか・外部 Action がバージョン固定されているか等、CI と供給網の安全を確かめる 4 つの検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 9 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 12 で 13,711→13,467）。
