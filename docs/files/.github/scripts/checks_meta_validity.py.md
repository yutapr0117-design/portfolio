---
file: .github/scripts/checks_meta_validity.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_meta_validity.py

## What

`check_repository_consistency.py` 分割トラックの 28 個目の split module。og/twitter meta の非空・robots.txt の安全性・.well-known JSON の妥当性を守る連続クラスタ Check **341-343** を内包し、`run(ctx)` で monolith から呼ばれる。

- 341(全 og:*/twitter:* meta content 非空) / 342(robots.txt に破滅的 Disallow なし) / 343(.well-known/**/*.json が全て valid JSON)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 31**）。341-343 は「og/twitter meta 非空 + robots 安全 + .well-known JSON 妥当性」テーマの **連続 self-contained クラスタ**。各 Check は index.html / robots.txt / .well-known を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。global→nonlocal 変換 0 箇所。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 340 の後・344 の前）**で `checks_meta_validity.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  341.`〜`  343.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 6,840 → 6,738（−102・Phase 31）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `meta-validity`, `robots`, `phase31`
- 残ターゲット（freevars4-clean）: 349(1) / 357-359(3)。以降は ctx-enrich（style/html glob）か helper 同梱が必要（handoff §0 参照）。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 28 個目。今回は「SNS 用 meta が空でないか・robots が全面拒否していないか・設定 JSON が壊れていないか確かめる 3 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 28 split module 横断で緑（Phase 31 で 6,840→6,738）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
