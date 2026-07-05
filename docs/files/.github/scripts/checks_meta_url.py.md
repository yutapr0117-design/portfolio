---
file: .github/scripts/checks_meta_url.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_meta_url.py

## What

`check_repository_consistency.py` 分割トラックの 20 個目の split module。package.json baseline と AIO version/repository meta のクロスサーフェス coherence を守る連続クラスタ Check **175-180** を内包し、`run(ctx)` で monolith から呼ばれる。

- 175(package.json private:true + name) / 176(JSON-LD @id own-origin canonical prefix) / 177(llms-full Version == SITE_CONFIG.VERSION) / 178(ai:repository canonical derivation) / 179(ai:version == SITE_CONFIG.VERSION) / 180(ai:last-modified == SITE_CONFIG.LAST_UPDATED)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 23**）。175-180 は「package.json + AIO version/repository meta coherence」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（package.json / index.html / llms-full.txt / main.js）を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。global→nonlocal 変換 0 箇所。175-180 の mutation は shipped file（package.json / index.html / llms-full.txt）を mutate ゆえ Check 362 anchor 追従不要。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 174 の後・181 の前）**で `checks_meta_url.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  175.`〜`  180.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 9,298 → 9,047（−251・Phase 23）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `meta`, `version-coherence`, `phase23`
- **信頼できる analyzer は `/tmp/freevars4.py`（annotation+def-aware）**。tuple-unpack（`_y, _mo, _d = ...`）は false-positive にするが保守的（safe）に倒れるだけ。tuple 対応の freevars5 は逆に誤検知が増え不良だった → freevars4 を使い、最終判定は extract→全出力 diff + exit code の安全網に委ねよ。
- 残ターゲット（freevars4-clean）: 202-207(6) / 209-214(6) / 216-219(4・218 global) / 242-249(8・245-247 global) / 251-254(4) / 256-261(6・global)。tuple-unpack で誤 gap 化した 208/215 も実は clean（extract→diff で確認可）。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 20 個目。今回は「package.json とバージョン/リポジトリ情報が全ファイルで一致しているか確かめる 6 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 20 split module 横断で緑（Phase 23 で 9,298→9,047）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
