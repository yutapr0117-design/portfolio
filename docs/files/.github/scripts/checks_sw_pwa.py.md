---
file: .github/scripts/checks_sw_pwa.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_sw_pwa.py

## What

`check_repository_consistency.py` 分割トラックの 25 個目の split module。service-worker / PWA registration と potentialAction / well-known skill の構造を守る連続クラスタ Check **251-254** を内包し、`run(ctx)` で monolith から呼ばれる。

- 251(JSON-LD potentialAction @type+target) / 252(sw.js install+activate+fetch handlers) / 253(main.js serviceWorker.register('./sw.js')) / 254(.well-known/index.json skill name uniqueness + digest format)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 28**）。251-254 は「service-worker / PWA registration + potentialAction / well-known structure」テーマの **連続 self-contained クラスタ**。各 Check は index.html / sw.js / main.js / .well-known を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。global→nonlocal 変換 1 箇所（251）。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 250 の後・255 の前）**で `checks_sw_pwa.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。global 使用 nested-fn は `nonlocal` へ機械変換（251）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  251.`〜`  254.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 7,345 → 7,165（−180・Phase 28）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `sw`, `pwa`, `phase28`
- 残ターゲット（freevars4-clean）: 266-268(3・global) / 341-343(3) / 345-347(3) / 351-355(5) / 357-359(3)。gap の多くは html/style glob（ctx-enrich 要）か `_walkNNN`/`_glob237`/`_src` 共有。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 25 個目。今回は「Service Worker / PWA の登録・スキル定義が正しいか確かめる 4 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 25 split module 横断で緑（Phase 28 で 7,345→7,165）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
