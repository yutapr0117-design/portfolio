---
file: .github/scripts/checks_jsonld_meta.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_jsonld_meta.py

## What

`check_repository_consistency.py` 分割トラックの 19 個目の split module。JSON-LD の参照型安全・meta タグ長・sitemap 値の spec 妥当性を守る連続クラスタ Check **221-235** を内包し、`run(ctx)` で monolith から呼ばれる。

- 221-223(JSON-LD image/agent-slot/isPartOf ref 型解決) / 224(description length) / 225(title length) / 226(og:title/description length) / 227(Person.name canonical) / 228(sitemap changefreq) / 229(sitemap priority range) / 230(sitemap 1 priority=1.0==canonical) / 231(SITE_CONFIG.ROLE_TITLE) / 232-234(ai:*/asset:* URL HTTPS + canonical prefix) / 235(Article/TechArticle required fields)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 22**）。221-235 は「JSON-LD ref-type + meta length + sitemap value coherence」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（index.html / sitemap.xml / main.js）を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。**global→nonlocal 変換 1 箇所（Check 235 の Article 走査 accumulator）。** 221-235 の mutation（`mutation_samples_archive.py`）は shipped file（index.html JSON-LD / sitemap.xml / meta）を mutate するため anchor 追従不要（Check 362 の find-anchor は移動しない）。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 220 の後・236 の前）**で `checks_jsonld_meta.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。global 使用 nested-fn は `nonlocal` へ機械変換済（235）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  221.`〜`  235.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 10,025 → 9,298（−727・Phase 22）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `jsonld`, `meta-length`, `sitemap-value`, `phase22`
- 残ターゲット（clean・def-aware 確認済）: 175-180(6) / 202-207(6) / 209-214(6) / 216-219(4) / 242-249(8・global 245-247) / 251-254(4) / 256-261(6・global) / 341-347 / 351-359。gap セクション（201/208/215/220/236/239-241/250/255/262-265/269-272/303/306/310/321-323/338-340/344/348-350/356/360）は `_walkNNN` 共有 nested-fn / html/style glob / cross-section 共有ゆえ ctx-enrich か helper 統合が必要。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 19 個目。今回は「構造化データの参照先の型・meta タグの文字数・サイトマップの値が正しいか確かめる 15 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 19 split module 横断で緑（Phase 22 で 10,025→9,298）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
