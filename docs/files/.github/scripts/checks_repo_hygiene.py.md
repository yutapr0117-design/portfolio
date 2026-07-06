---
file: .github/scripts/checks_repo_hygiene.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_repo_hygiene.py

## What

`check_repository_consistency.py` 分割トラックの 37 個目の split module。repository hygiene / doc-dating / artifact-tracking / lock-sync を守る非連続クラスタ Check **31/32/33/34/35/36/38/39/40/41** を内包し、`run(ctx)` で monolith から呼ばれる。

- 31(Claude2Claude ↔ AI2AI record) / 32(index.html JSON-LD valid) / 33(Zenn slug set) / 34(per-file doc dating・WARNING) / 35(robots ↔ sitemap) / 36(sitemap no-future-date・WARNING) / 38(package.json ↔ lock sync) / 39(sitemap loc → committed file) / 40(CSS lint path hygiene) / 41(AIO monitoring-log ↔ manifest atomic-commit)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 43**）。31-41 は「repository hygiene」テーマの連続クラスタだが、**Check 37（no generated/cache artifacts tracked）は除外**した — 37 は module-level 共有変数 `_member_paths`（`_repo_member_paths()` の結果・後続 monolith checks が消費）の **PRODUCER** であり、producer/consumer 結合ゆえ monolith 残置（`_ctx._member_paths` enrich を試みたが 31-41 が `_member_paths` def より前に走るため順序不整合で crash → 37 を除外する方が clean と判断）。他 10 checks は自前 read で結合なし。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 31 の位置）**で `checks_repo_hygiene.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **Check 37 は producer ゆえ残置**: `_member_paths` を定義する check は monolith に残す（後続 consumer との結合）。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 3,333 → 2,958（−375・Phase 43）。track 元 15,913 から **約 81%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `repo-hygiene`, `phase43`
- **教訓（producer/consumer setup-global）: Check 37 のように「module-level 共有 var(`_member_paths`)を定義し後続 check が消費する PRODUCER」は、そのままだと (a) producer を含めると後続 consumer が壊れ、(b) producer を早い位置(dispatch)で ctx-enrich しようにも producer 自身が dispatch 後に走るため順序不整合。クリーンに解くには producer の定義(`_repo_member_paths` def + `_member_paths` 計算)を setup 領域(checks 実行前)へ移し `_ctx._member_paths` を attach する別 PR が要る。当面は producer(37)を残置し周辺を抽出。** 同型: 108/122 も `_member_paths` consumer。
- 残る section: 4/5/9/10/12/13/15 / 37(producer) / 43-60(structural・59+72 ESLint pair) / 100/102/104-113/121-127(`_member_paths`/`_binary_edited` consumer) / 141 / 190/201/215/236/238/266-268/338-348/349/360。不動点: 45/70/105 + load infra。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 37 個目。今回は「リポジトリの衛生(不要ファイル/日付/ロック同期など)を確かめる 10 の検査」を移した。1 つ(検査 37)は他の検査と変数を共有する「供給元」なので残した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 37 split module 横断で緑（Phase 43 で 3,333→2,958）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
