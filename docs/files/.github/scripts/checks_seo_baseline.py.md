---
file: .github/scripts/checks_seo_baseline.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_seo_baseline.py

## What

`check_repository_consistency.py` 分割トラックの 35 個目の split module。SEO/AIO の date-ISO・URL-resolution・HTTPS/meta baseline を守る非連続クラスタ Check **181/182/183/184/185/186/188/189** を内包し、`run(ctx)` で monolith から呼ばれる。

- 181(SITE_CONFIG.LAST_UPDATED ISO-8601) / 182(ai:* meta URL resolve) / 183(sitemap lastmod ISO) / 184(sw.js AIO_FILES resolve) / 185(canonical HTTPS) / 186(meta author entity id) / 188(robots Sitemap URL resolve) / 189(meta robots no-noindex)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 41**）。181-189 は「SEO/AIO date-ISO + URL-resolution + HTTPS/meta baseline」テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（main.js / index.html / sitemap.xml / sw.js / robots.txt）を自前で読む。**NOTE: 187（og:locale）は checks_html.py へ抽出済ゆえ除外。190（.nojekyll）は setup-global `_assets` list（line ~396 で computed）を消費するため monolith 残置。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 181 の位置）**で `checks_seo_baseline.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 4,049 → 3,672（−377・Phase 41）。track 元 15,913 から **約 77%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `seo-baseline`, `phase41`
- 残る clean クラスタ: 146-148(3) / 304-309(5) / 236-268(`_walk`nested-fn 大半 false-positive・_mo/_y scratch・要 diff 確認) / 31-41(`_repo_member_paths` setup-global) / 190(`_assets` setup-global)。coupled: 104-113(105 self-integrity+`_member_paths`) / 121-127(`_binary_edited`+`_member_paths`) / 59+72(ESLint pair) / 338-348(`_parse_webp_dims`/`_walk`) / 4-15(csp helper)。不動点: 45/70/105 aggregator + load/ctx-setup infra。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 35 個目。今回は「日付形式・URL の実在・HTTPS・meta タグの基本が正しいか確かめる 8 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 35 split module 横断で緑（Phase 41 で 4,049→3,672）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
