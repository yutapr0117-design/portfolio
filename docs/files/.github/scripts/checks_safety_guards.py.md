---
file: .github/scripts/checks_safety_guards.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_safety_guards.py

## What

`check_repository_consistency.py` 分割トラックの 43 個目の split module。shipped-JS/AIO の安全ガードを守る連続クラスタ Check **123-127** を内包し、`run(ctx)` で monolith から呼ばれる。

- 123(operating-model description coherence site ↔ AIO) / 124(site visible-text anonymity guard・実名を視覚 renderer に出さない) / 125(no dead CONSTANTS key) / 126(ESLint bug-catcher safety-net presence) / 127(AIO digest tool binary re-bake guard = `_binary_edited()` gate presence)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 49**）。123-127 の clean な 5 checks を抽出。各 Check は対象ファイル（js/components.js / llms-full.txt / js/constants.js / eslint.config.mjs / update_aio_digests.py）を自前で読む。**教訓: Check 127 が探す `_binary_edited` は update_aio_digests.py 内の文字列（tool が持つべき関数名を string で検索）であって Python 変数ではない — free-var analyzer が string 内の identifier token を誤って free 変数と flag した false-positive。同様に `_f124` は Check 124 内定義。extract→全出力 diff で clean を実証。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 123 の位置）**で `checks_safety_guards.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 1,702 → 1,505（−197・Phase 49）。track 元 15,913 から **約 90.5%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `safety-guards`, `anonymity`, `phase49`
- **教訓: free-var analyzer は「string 内の identifier token」（Check 127 が検索する `_binary_edited` 等）を誤 flag しうる — 疑わしければ extract→diff で確認（string false-positive は clean）。** 残る section: 4/5/9/10/12/13/15(csp helper+html) / 37(FORBIDDEN ctx 化) / 45(不動点) / 17-18(`root_lastmod`) / 141/190/201/215/338-348/349/360。**owner 目標 ≤1,000 まであと ~505 行。** 不動点(残置): 45/70/105 aggregator + load/ctx-setup infra + setup producer。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 43 個目。今回は「運用方針の一貫性・匿名性・不要定数・ESLint 安全網・digest 再生成ガードを確かめる 5 の安全検査」を移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 43 split module 横断で緑（Phase 49 で 1,702→1,505）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
