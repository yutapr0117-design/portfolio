---
file: .github/scripts/checks_asset_resolve.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_asset_resolve.py

## What

`check_repository_consistency.py` 分割トラックの 29 個目の split module。shipped-asset の参照解決配線を守る連続クラスタ Check **357-359** を内包し、`run(ctx)` で monolith から呼ばれる。

- 357(local `<link rel=preload>` href が実 file に解決) / 358(sitemap image:loc 実 file 解決 + og:image と cross-surface 一致) / 359(`<audio id=bgm-audio>` 存在 + src が実 mp3 file に解決)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 32**）。357-359 は「shipped-asset resolution wiring」テーマの **連続 self-contained クラスタ**。各 Check は index.html / sitemap.xml を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。global→nonlocal 変換 0 箇所。READ-ONLY ゆえ C6 対象外。**NOTE: 隣接の 360（asset:*:canonical・`_ctx` gap）と 356（style glob）は残置。**

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 356 の後・360 の前）**で `checks_asset_resolve.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  357.`〜`  359.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 6,738 → 6,590（−148・Phase 32）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `asset-resolve`, `wiring`, `phase32`
- **これで freevars4-clean な連続 run は概ね抽出し尽くした**（残: 349 単発 / gap のみ）。次フェーズは **ctx-enrich**（`_ctx` に html/style を足して 174/187/220/250/255/344/356/360 を抽出）or **helper 同梱**（`_lib_csp_sri_hash`=350 / `_walkNNN`・`_glob237`・`_src`=190/201/237-241/262-265/269-272）。handoff §0 の残 monolith 性質を参照。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 29 個目。今回は「先読み資産・サイトマップ画像・BGM 音声が実ファイルに正しく繋がっているか確かめる 3 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 29 split module 横断で緑（Phase 32 で 6,738→6,590・track 元 15,913 から約 59%減）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
