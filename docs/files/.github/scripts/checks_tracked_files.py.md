---
file: .github/scripts/checks_tracked_files.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_tracked_files.py

## What

`check_repository_consistency.py` 分割トラックの 40 個目の split module。tracked-files list（`_member_paths`）を消費する Check **108/122** を内包し、`run(ctx)` で monolith から呼ばれる。

- 108(docs/files mirror ↔ tracked-files FULL bijection) / 122(no private source documents tracked = resume/career の pdf/docx/office/archive が tracked でない privacy guard)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 46**・**producer-relocation パターンの実証**）。108/122 はともに repository member-paths list `_member_paths`（`git ls-files`）を消費する。この `_member_paths` は元々 **Check 37 の inline PRODUCER**（`_repo_member_paths()` 定義 + 計算）で、consumer(108/122)と結合していたため抽出できなかった。**本 phase 前半で producer（FORBIDDEN_GENERATED_* 定数 + `_repo_member_paths()` def + `_member_paths = _repo_member_paths()`）を setup 領域（checks 実行前）へ移設し `_ctx._member_paths` として attach**（byte-equivalent: `git ls-files` はいつ呼んでも同結果）。これで consumer が `_member_paths = ctx._member_paths` で unpack でき、後半で 108/122 を抽出した。**Check 37（artifact-scan）は FORBIDDEN_GENERATED_* setup 定数も使うため monolith 残置**（37 を抽出するなら FORBIDDEN も ctx 化が要る）。READ-ONLY ゆえ C6 対象外。

## How

- monolith: setup 領域で producer を一度計算し `_ctx._member_paths = _member_paths` を attach。**元の実行位置（Check 108 の位置）**で `checks_tracked_files.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract`/**`_member_paths`** を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **ctx-enrich `_member_paths` 依存**: monolith が setup で `_ctx._member_paths` を attach 済み前提。
- **module-global 結合なし（ctx 除く）**: `re`/`json` のみ module import。`exec` 不使用。
- **Check 37 は producer の home ゆえ残置**（FORBIDDEN 定数を setup で共有）。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 2,467 → 2,416（producer 移設 +6 − 108/122 抽出 = 純 −51・Phase 46）。track 元 15,913 から **約 84.8%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `tracked-files`, `producer-relocation`, `ctx-enrich`, `phase46`
- **producer-relocation パターン確立（本 phase が実証）: 「Check の inline で計算され後続 consumer が使う setup-global(`_member_paths`型)」は、(1) producer の計算を setup 領域(checks 実行前)へ移し `_ctx.<name>` attach(byte-equivalent 確認) → (2) consumer を `ctx.<name>` unpack で抽出、の 2 段で解放する。同一 PR にまとめれば純減。** 残る同型: `_binary_edited`(Check 127 producer)・`root_lastmod`(Check 17/18)。他残 section: 4/5/9/10/12/13/15 / 37(FORBIDDEN も ctx 化すれば抽出可) / 45(self-integrity・不動点) / 100/102/104-107/109-113/121/123-127 / 141/190/201/215/236/238/266-268/338-348/349/360。**不動点: 45/70/105 aggregator + load/ctx-setup infra。**

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 40 個目。今回は「全ファイルに説明ドキュメントが揃っているか(108)・機密書類が混入していないか(122)を確かめる 2 の検査」を移した。両者が使う「リポジトリのファイル一覧」を、先に一度だけ計算して渡す形に整理した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 40 split module 横断で緑（Phase 46 で 2,467→2,416）。producer 移設は全 check 出力 diff で byte-equivalent を実証（`git ls-files` の計算位置移動が結果に影響しないことを確認）。
