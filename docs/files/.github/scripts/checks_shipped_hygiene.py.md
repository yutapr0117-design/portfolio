---
file: .github/scripts/checks_shipped_hygiene.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_shipped_hygiene.py

## What

`check_repository_consistency.py` 分割トラックの 22 個目の split module。index.html の inline-handler hygiene・日付・JSON-LD 構造妥当性・meta baseline を守る連続クラスタ Check **242-249** と、shipped JS h() prop の外部リンク hygiene Check **366**、shipped JS h('select') value attr 禁止 Check **367** を内包し、`run(ctx)` で monolith から呼ばれる。

- 242(inline on*= allowlist) / 243(LAST_UPDATED + ai:last-modified 未来なし) / 244(JSON-LD @graph node @type) / 245(FAQPage mainEntity 構造) / 246(BreadcrumbList itemListElement 構造) / 247(ImageObject/AudioObject/VideoObject 必須 fields) / 248(charset utf-8) / 249(viewport mobile baseline) / 366(shipped JS target='_blank' ±2行以内で noreferrer あり) / 367(shipped JS h('select') attrs に value: キーなし・HTML 仕様違反 #7cbc4d9 class 構造封じ)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 25**）。242-249 は「shipped index.html hygiene + JSON-LD structural validity + meta baseline」テーマの **連続 self-contained クラスタ**。各 Check は index.html を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。**global→nonlocal 変換 3 箇所（245/246/247 の JSON-LD 走査 accumulator）。** 242-249 の mutation は shipped file を mutate ゆえ Check 362 anchor 追従不要。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 241 の後・250 の前）**で `checks_shipped_hygiene.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。global 使用 nested-fn は `nonlocal` へ機械変換（245/246/247）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  242.`〜`  249.`, `  366.`, `  367.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 8,444 → 8,036（−408・Phase 25）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `hygiene`, `jsonld-structure`, `phase25`
- 残ターゲット（freevars4-clean）: 216-219(4・218 global) / 251-254(4) / 256-261(6・global) / 266-268(3) / 341-347 / 351-359。gap の多くは html/style glob（ctx-enrich 要）か `_walkNNN`/`_glob237` 共有。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 22 個目。今回は「公開 HTML のイベントハンドラ・文字コード・構造化データの構造が正しいか確かめる 8 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 22 split module 横断で緑（Phase 25 で 8,444→8,036）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
