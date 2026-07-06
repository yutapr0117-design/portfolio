---
file: .github/scripts/checks_shipped_content.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_shipped_content.py

## What

`check_repository_consistency.py` 分割トラックの 42 個目の split module。manifest date format / HTML head singleton / JSON-LD length を守る非連続クラスタ Check **236/238/266/267/268** を内包し、`run(ctx)` で monolith から呼ばれる。

- 236(aio-manifest generated_at + start_date strict format) / 238(HTML head singleton tags exactly once) / 266(JSON-LD entity description length [20,1000]) / 267(JSON-LD entity name length [3,200]) / 268(JSON-LD Article/TechArticle headline length [10,110])。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 48**）。236/238/266-268 の clean な 5 checks を抽出。各 Check は対象ファイル（aio-manifest.json / index.html）を自前で読む。**annotation+def-aware free-var 分析で `_ok236`/`_ok266-268` 等が section 内定義（false-positive）と確認**し extract→全出力 diff で byte-equivalent 実証。JSON-LD length checks(266-268)の nested walker accumulator は `global`→`nonlocal` 変換 3 箇所。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 236 の位置）**で `checks_shipped_content.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json`。global 使用 nested-fn は `nonlocal` へ機械変換。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 1,986 → 1,702（−284・Phase 48）。track 元 15,913 から **約 89%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `shipped-content`, `jsonld-length`, `phase48`
- 汎用抽出器 `/tmp/extract_gen.py`（`[sections] stem desc imports unpack-extra` を取り block 抽出 + global→nonlocal + wire + CHECK_SOURCE_FILES 登録 + inventory 移動）で抽出。残る section: 4/5/9/10/12/13/15(csp helper+html) / 37(FORBIDDEN ctx 化) / 45(不動点) / 121/123-127(`_binary_edited` producer=127 の relocation・`_binary_edited` は setup-level fn ゆえ `_ctx._binary_edited` attach で解放) / 17-18(`root_lastmod`) / 141/190/201/215/338-348/349/360。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 42 個目。今回は「manifest の日付形式・HTML の重複タグ・構造化データの文字数が正しいか確かめる 5 の検査」を移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 42 split module 横断で緑（Phase 48 で 1,986→1,702）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
