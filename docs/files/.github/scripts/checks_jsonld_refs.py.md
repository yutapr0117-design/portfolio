---
file: .github/scripts/checks_jsonld_refs.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_jsonld_refs.py

## What

`check_repository_consistency.py` 分割トラックの 24 個目の split module。index.html JSON-LD の参照整合性と aio-manifest path 被覆を守る連続クラスタ Check **216-219** を内包し、`run(ctx)` で monolith から呼ばれる。

- 216(@id cross-references resolve) / 217(@id definitions unique per @graph) / 218(datePublished <= dateModified) / 219(aio-manifest paths ⊆ check_aio_digests MANIFEST_PATH_TO_LOCAL)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 27**）。216-219 は「JSON-LD referential integrity + manifest path coverage」テーマの **連続 self-contained クラスタ**。各 Check は index.html / aio-manifest.json / check_aio_digests.py を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。**global→nonlocal 変換 1 箇所（218 の node 走査 accumulator）。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 215 の後・220 の前）**で `checks_jsonld_refs.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。global 使用 nested-fn は `nonlocal` へ機械変換（218）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  216.`〜`  219.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 7,615 → 7,345（−270・Phase 27）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `jsonld`, `referential-integrity`, `phase27`
- 残ターゲット（freevars4-clean）: 251-254(4) / 266-268(3・global) / 341-347 / 351-359。gap の多くは html/style glob（ctx-enrich 要）か `_walkNNN`/`_glob237`/`_src` 共有。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 24 個目。今回は「構造化データの参照先が実在するか・ID が重複しないか・日付順序が正しいか確かめる 4 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 24 split module 横断で緑（Phase 27 で 7,615→7,345）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
