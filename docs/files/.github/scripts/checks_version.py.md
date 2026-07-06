---
file: .github/scripts/checks_version.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_version.py

## What

`check_repository_consistency.py` 分割トラックの 30 個目の split module・3 個目の ctx-enrich module。app version の cross-surface coherence を守る非連続クラスタ Check **1/2/3/19** を内包し、`run(ctx)` で monolith から呼ばれる。

- 1(ai:version == AI2AI Pipeline-Version) / 2(main.js VERSION string == ai:version) / 3(mcp.json server.version major) / 19(sw.js CACHE_NAME == app version)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 36**）。1/2/3/19 は `html_v`（ai:version・Check 1 で extract・2/3/19 が再利用）と per-check `ai2ai_v`(1)/`mainjs_v`(2) を共有する coupled-var cluster であり、かつ複数の glob content（html/ai2ai/mainjs/mcp_data）を読む。**multi-glob ctx-enrich パターン**: monolith が `_ctx.ai2ai/mainjs/mcp_data`（+既存 style/html）を attach し、本 module が全て unpack。共有 `html_v` は Check 1 で定義され list 順（1→2→3→19）で消費者より前に bind。**mutation-anchor 追従: Check 45 の mutation（`# ── 1. ai:version` header を break する `"file": CHECK`）の target file を本 module へ更新**（Check 45 は全 module 横断集約ゆえ module 内 header 破壊も検知・Check 362）。READ-ONLY ゆえ C6 対象外。

## How

- monolith: globals load 後に `_ctx.style/html/ai2ai/mainjs/mcp_data` を attach。**元の実行位置（Check 1 の位置）**で `checks_version.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`html`/`ai2ai`/`mainjs`/`mcp_data`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **ctx-enrich 依存**: `ctx.html/ai2ai/mainjs/mcp_data` を必要とする（monolith が attach 済み前提）。
- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **mutation anchor 追従（Check 362）**: Check 45 の section-header mutation の `"file"` は本 module。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 5,372 → 5,342（−30・Phase 36。小クラスタだが version-var 結合を解消し multi-glob ctx-enrich を確立）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `version`, `ctx-enrich`, `multi-glob`, `phase36`
- **multi-glob ctx-enrich 確立**（html/ai2ai/mainjs/mcp_data を一括 attach）。残る glob-dependent: 14(ai2ai+html)/17(mainjs+html)（今や ctx に ai2ai/mainjs あり抽出可）/ 7(`_lib_io.csp_sri_hash` helper 同梱要)。単発=189/349/360、helper=190/201(`_walkNNN`)。
- **教訓: Check 45/70/105 系の section-header/count を狙う mutation は、その header を含む section を抽出すると orphan 化する → mutation の `"file"` を新 module へ追従（Check 45 は横断集約ゆえ検知能力は不変）。**

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 30 個目。今回は「アプリのバージョン番号が全ファイルで一致しているか確かめる 4 の検査」を、事前に読み込んだ複数ファイルの中身を渡す形で移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 + Check 362 が monolith + 30 split module 横断で緑（Phase 36 で 5,372→5,342）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
