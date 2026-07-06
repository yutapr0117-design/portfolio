---
file: .github/scripts/checks_seo_meta.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_seo_meta.py

## What

`check_repository_consistency.py` 分割トラックの 32 個目の split module。AIO/SEO meta + canonical URL + resource-resolution coherence を守る連続クラスタ Check **149/150/151/153/154/155/156/157/158/159/160/161/162/163/164/165/166**（17 checks・152 は checks_html.py へ抽出済ゆえ除外）を内包し、`run(ctx)` で monolith から呼ばれる。

- 149(canonical 3-way) / 150(og:url) / 151(e2e title uniqueness) / 153(og·twitter image origin) / 154(description 3-way) / 155(og·twitter title) / 156(og:type enum) / 157(mobile-PWA meta) / 158(Google-Fonts preconnect) / 159(JSON-LD @context) / 160(sw.js hardcoded paths) / 161(robots baseline) / 162(.gitignore baseline) / 163(icon href resolve) / 164(og·twitter image resolve) / 165(api-catalog) / 166(sitemap loc prefix)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 38・重大マイルストーン**）。149-166 は「AIO/SEO meta + canonical URL + resource-resolution coherence」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（index.html / sitemap.xml / robots.txt / .well-known / e2e spec / sw.js）を自前で読み、annotation+def-aware free-var 分析で外部 `_var` ・glob 依存ゼロ確認。**この抽出で monolith が 5,269 → 4,455 行となり、遂に Check 52 の advisory line budget（4,750）を下回った — check.py の bloat が自身の advisory 予算内に収束した歴史的節目。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 149 の位置）**で `checks_seo_meta.run(_ctx)` を呼ぶ。17 checks は list 順で連続実行（順序非依存・全出力 diff で byte-identical 実証）。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 5,269 → 4,455（−814・Phase 38）。track 元 15,913 から **約 72%減**。**Check 52 advisory budget（4,750）達成**（WARNING → OK）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `seo-meta`, `canonical-url`, `milestone`, `phase38`
- **check.py は遂に自身の advisory budget 4,750 内に収束（4,455）。** 残る大きめ clean クラスタ: 21-27(7) / 153-166 系は抽出済。残 sections（4/5/9/10/12/13/15/17/18/21-27/31-41/43-46/53-72/100/102/104-127/141/146-148/181-190/201/215/236/238/266-268/304-340/348/349/360）を継続抽出可能。**注意: 45/70/105 は self-integrity aggregator ゆえ残置。62-72 は `_aggregate_check_numbers`(70) を含むため 70 を除く。31-41 は `_repo_member_paths` setup-global 依存。**
- 単発 clean=189/349/360、date-sync=17/18(root_lastmod)、helper=190/201(`_walkNNN`)。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 32 個目。今回は「公開 URL・SNS 用 meta・SEO の基本設定・リソース参照が正しいか確かめる 17 の検査」をまとめて移した。**これで check.py が「大きすぎ」と自分で警告していた閾値を初めて下回った。**

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 32 split module 横断で緑（Phase 38 で 5,269→4,455・Check 52 budget 達成）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
