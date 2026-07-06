---
file: .github/scripts/checks_structural_ci.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_structural_ci.py

## What

`check_repository_consistency.py` 分割トラックの 38 個目の split module。kernel/canary structural integrity と CI lint-coupling を守る非連続クラスタ Check **43/44/46/53/54/55/58** を内包し、`run(ctx)` で monolith から呼ばれる。

- 43(main.js AIDK Isolated Kernel structural integrity) / 44(AIO provenance canary token cross-surface) / 46(package.json lint scripts JS-set coverage) / 53(index.html modulepreload href resolution) / 54(ESLint ↔ @eslint/js major coupling) / 55(CI lint-target authoritative coupling) / 58(e2e ALL_ROUTES ↔ main.js switch set equality)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 44**）。structural/CI 系の clean な 7 checks を抽出。各 Check は対象ファイル（main.js / index.html / package.json / eslint config / e2e spec）を自前で読む。**除外: Check 45（self-documentation bijection）= self-integrity aggregator ゆえ不動点残置。Check 59/60/72（ESLint baseline trio: 59 が `_bsrc59`/`_budget59` を定義し 60・72 が消費する producer/consumer group）ゆえ残置（60 を含めた抽出試行が `_budget59` NameError で crash → 安全網が検知）。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 43 の位置）**で `checks_structural_ci.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **ESLint trio 59/60/72 は残置**: `_bsrc59`/`_budget59` の producer/consumer group ゆえ 3 つ一括でしか抽出できない（将来 pair 抽出する場合は 59+60+72 を full-set で）。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 2,958 → 2,575（−383・Phase 44）。track 元 15,913 から **約 84%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `structural`, `ci-lint`, `phase44`
- 残る section: 4/5/9/10/12/13/15(early AIO) / 37(`_member_paths` producer) / 45(self-integrity・不動点) / 59+60+72(ESLint trio full-set 要) / 100/102/104-113/121-127(`_member_paths`/`_binary_edited` consumer) / 141/190/201/215/236/238/266-268/338-348/349/360。**不動点: 45/70/105 aggregator + load/ctx-setup infra。** ESLint trio(59+60+72)は full-set 抽出可能(producer 59+consumer 60/72 を一括)。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 38 個目。今回は「カーネル構造・監査トークン・CI の lint 設定が正しいか確かめる 7 の検査」を移した。ESLint の予算検査 3 つ(59/60/72)は互いに変数を共有するので一緒でないと動かず、今回は残した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 38 split module 横断で緑（Phase 44 で 2,958→2,575）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
