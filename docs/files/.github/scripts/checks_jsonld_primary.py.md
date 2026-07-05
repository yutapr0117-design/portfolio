---
file: .github/scripts/checks_jsonld_primary.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_jsonld_primary.py

## What

`check_repository_consistency.py` 分割トラックの 23 個目の split module。index.html JSON-LD の primary ノード（WebPage/Person/WebSite/Organization/hero ImageObject/BGM AudioObject）が必須フィールドを完備することを守る連続クラスタ Check **256-261** を内包し、`run(ctx)` で monolith から呼ばれる。

- 256(primary WebPage: dateModified+inLanguage+isPartOf) / 257(primary Person 5 fields) / 258(primary WebSite: inLanguage+potentialAction) / 259(primary Organization 5 fields) / 260(primary hero ImageObject 4 fields) / 261(primary BGM AudioObject fields)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 26**）。256-261 は「JSON-LD primary-node required-field completeness」という単一テーマの **連続 self-contained クラスタ**。各 Check は index.html を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。**global→nonlocal 変換 6 箇所（各 section の primary-node 探索が accumulator を module-global 経由で mutate していた）。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 255 の後・262 の前）**で `checks_jsonld_primary.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。global 使用 nested-fn は `nonlocal` へ機械変換（256-261 各 1）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  256.`〜`  261.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 8,036 → 7,615（−421・Phase 26）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `jsonld`, `primary-node`, `phase26`
- 残ターゲット（freevars4-clean）: 216-219(4・218 global) / 251-254(4) / 266-268(3・global) / 341-347 / 351-359。gap の多くは html/style glob（ctx-enrich 要）か `_walkNNN`/`_glob237`/`_src` 共有。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 23 個目。今回は「構造化データの主要ノード(ページ/人物/サイト/会社/画像/音声)に必須項目が揃っているか確かめる 6 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 23 split module 横断で緑（Phase 26 で 8,036→7,615）。抽出前後の全 check 出力 diff で byte-equivalence を実証（global→nonlocal 6 変換後も 364 出力 identical）。
