---
file: .github/scripts/checks_misc_governance.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_misc_governance.py

## What

`check_repository_consistency.py` 分割トラックの 44 個目の split module。AIO/SEO/governance の scattered singletons Check **9/10/12/13/15/121/141/201/215/349/360** を内包し、`run(ctx)` で monolith から呼ばれる。

- 9(sitemap valid XML) / 10(.github/scripts/*.py syntax) / 12(no stale 72回 in current-desc) / 13(70超 only in history) / 15(Project Pages robots/.well-known) / 121(STATUS.md freshness) / 141(default-project slug/id uniqueness) / 201(JSON-LD WebSite/WebPage @id canonical) / 215(ai:last-modified + SITE_CONFIG ISO) / 349(icon.svg well-formed) / 360(asset:*:canonical resolve)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 50**）。残っていた scattered な clean singletons を効率のため 1 module に統合抽出（11 checks・−338 行）。各 Check は対象ファイルを自前で読む。**教訓再確認: Check 9 が `ET.ParseError`(xml.etree)・Check 10 が `ast.parse` を使うため module に `import xml.etree.ElementTree as ET` + `import ast` が必要（初回 NameError で判明・安全網が捕捉）。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 9 の位置）**で `checks_misc_governance.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json, xml.etree.ElementTree as ET, ast`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json`/`ET`/`ast` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 1,505 → 1,167（−338・Phase 50）。track 元 15,913 から **約 92.7%減**。**owner 目標 ≤1,000 まであと ~167 行。**

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `misc-governance`, `singletons`, `phase50`
- **残る extractable section と最終手**: 4/5(csp helper `_lib_csp_sri_hash` import + `ctx.html`) / 17-18(`root_lastmod` producer relocation・Phase 46 パターン) / 37(FORBIDDEN_GENERATED_* を `_ctx` 化して抽出) / 190(`_assets` setup-global → `_ctx._assets` attach) / 338-340/348(webp-dims/workflow・`_ah`/`_aw`/`_walk` は section 内 nested-fn の false-positive の可能性→extract→diff で確認)。これらを抽出すれば ≤1,000 到達圏。**不動点(残置必須): 45/70/105 self-integrity aggregator + load/ctx-setup infra + setup の `_member_paths`/FORBIDDEN/`_repo_member_paths` producer(~100-150 行)。** ≤1,000 達成後は e2e spec 分割 → B(style.css/index.html/docs) → capstone(全ファイル ≤1,000 CI 監査) の順(§5-§7)。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 44 個目。今回は散らばっていた小さな検査 11 個をまとめて移した。**これで check.py は 1,167 行(元 15,913 行の約 13 分の 1)。目標の 1,000 行まであと少し。**

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 44 split module 横断で緑（Phase 50 で 1,505→1,167）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
