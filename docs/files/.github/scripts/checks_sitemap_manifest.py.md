---
file: .github/scripts/checks_sitemap_manifest.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_sitemap_manifest.py

## What

`check_repository_consistency.py` 分割トラックの 16 個目の split module。sitemap.xml / webmanifest / aio-manifest の format & validity coherence を守る連続クラスタ Check **311-320** を内包し、`run(ctx)` で monolith から呼ばれる。

- **311**: sitemap.xml `<lastmod>` strict YYYY-MM-DD かつ未来日付なし。
- **312**: sitemap.xml `<loc>` unique。
- **313**: aio-manifest generated_at + last_metadata_update 未来日付なし。
- **314**: manifest.webmanifest theme_color ↔ index.html meta theme-color。
- **315**: webmanifest display enum + background_color 6-digit hex。
- **316**: webmanifest icons[].purpose enum + sizes format。
- **317**: aio-manifest sha256 fields strict 64-hex。
- **318**: aio-manifest evidence entries required fields。
- **319**: aio-manifest evidence.path 実在。
- **320**: robots.txt Sitemap: directive count == 1。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 19**）。311-320 は「sitemap & manifest format/validity coherence」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（sitemap.xml / manifest.webmanifest / aio-manifest.json / robots.txt）を自前で `read_text()` し global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認済。global→nonlocal 変換は本クラスタでは 0 箇所。READ-ONLY coherence 検査ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 310 の後・321 の前）**で `checks_sitemap_manifest.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  311.`〜`  320.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 11,483 → 11,070（−413・Phase 19）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `sitemap`, `manifest`, `format-validity`, `phase19`
- 汎用抽出ツール `/tmp/split_tool.py`（start-section・end-exclusive・module-stem・desc・prev-anchor・imports を取り、global→nonlocal 変換 + wire 配線 + CHECK_SOURCE_FILES 登録を自動化）で抽出。次担当も同 tool を使えば高速。
- 残ターゲット（clean・大型連続 run）: 324-337(14) / 191-200(10) / 221-235(15・global 235 要変換) / 242-249(8・global 245-247) / 256-261(6・global) / 202-207 / 209-214 / 351-359 系。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 16 個目。今回は「サイトマップとアプリ manifest の日付・形式・一意性が正しいか確かめる 10 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 16 split module 横断で緑（Phase 19 で 11,483→11,070）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
