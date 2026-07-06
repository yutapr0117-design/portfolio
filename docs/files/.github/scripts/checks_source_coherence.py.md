---
file: .github/scripts/checks_source_coherence.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_source_coherence.py

## What

`check_repository_consistency.py` 分割トラックの 31 個目の split module・ctx-enrich + helper 同梱 module。glob/helper-dependent な残存 Check **7/11/14/350** を内包し、`run(ctx)` で monolith から呼ばれる。

- 7(CSP meta が inline suppressor script より前・`_lib_io.csp_sri_hash` helper) / 11(AIO-monitoring summary shape・aio_mon) / 14(v1→v74 transition consistency across AI2AI+index.html) / 350(CSP inline-handler content-hash authorization・helper)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 37**）。これらは (a) glob content（html/ai2ai/aio_mon）を読み、(b) 一部が `_lib_io.csp_sri_hash` helper を使うため残置していた。**ctx-enrich（`_ctx.aio_mon` を追加）+ helper 同梱（module が `from _lib_io import csp_sri_hash as _lib_csp_sri_hash`）** で解放。Check 7 は helper を local `_csp_sri_hash` alias で wrap、350 は直接使用。**NOTE: date-sync Check 17/18 は含めない — `html_date`（17→18）と setup-global `root_lastmod` を共有する別 mini-cluster ゆえ、後の date-coherence 抽出に回す（逆結合を安全網が検知）。** READ-ONLY ゆえ C6 対象外。

## How

- monolith: globals load 後に `_ctx.style/html/ai2ai/mainjs/mcp_data/aio_mon` を attach。**元の実行位置（Check 7 の位置）**で `checks_source_coherence.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`html`/`ai2ai`/`aio_mon`/`read`/`extract` を ctx から unpack、`import re, json` + `from _lib_io import csp_sri_hash as _lib_csp_sri_hash`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **ctx-enrich + helper 依存**: `ctx.html/ai2ai/aio_mon` + `_lib_io.csp_sri_hash` を必要とする。
- **module-global 結合なし（ctx/helper 除く）**: `re`/`json`/`csp_sri_hash` のみ import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 5,342 → 5,269（−73・Phase 37）。track 元 15,913 から **約 67%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `source-coherence`, `ctx-enrich`, `helper-colocate`, `phase37`
- **これで glob-dependent カテゴリは 17/18(date-sync)を除き抽出完了。** 残り: date-sync 17/18（`html_date` 17→18 逆結合 + setup-global `root_lastmod`。17+18 を一括抽出しつつ `root_lastmod` の定義(line ~792)も module へ移すか ctx に足す）/ 単発 clean=189/349/360 / helper=190/201(`_walkNNN`)。自己整合 aggregator + load/ctx-setup infra は不動点残置。
- **教訓の総括: 逆結合（cluster 内定義・外部使用）は free-var analyzer で検出できない。setup-global（`root_lastmod` 等・line <929 で computed）を使う check も同様。抽出前に `grep -nw '<候補 check が使う疑いの var>' check.py` で定義位置と全消費者を map せよ。安全網（extract→NameError + 全出力 diff + Check 362）が最終防衛線。**

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 31 個目。今回は「CSP(セキュリティ設定)の順序とハッシュ・AIO 監視・バージョン遷移が正しいか確かめる 4 の検査」を、共有ヘルパー関数ごと移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 + Check 362 が monolith + 31 split module 横断で緑（Phase 37 で 5,342→5,269）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
