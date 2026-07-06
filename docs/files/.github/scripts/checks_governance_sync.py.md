---
file: .github/scripts/checks_governance_sync.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_governance_sync.py

## What

`check_repository_consistency.py` 分割トラックの 33 個目の split module。AIO / AI2AI / llms の freshness と session-record governance sync を守る連続クラスタ Check **21-27** を内包し、`run(ctx)` で monolith から呼ばれる。

- 21(llms alias files Last-Updated sync) / 22(AI2AI Session Record order) / 23(workflow/dependabot YAML syntax) / 24(llms-full freshness vs AI2AI) / 25(aio-monitoring-log evidence_policy key) / 26(AI2AI-archive max record == manifest role) / 27(llms-full no stale C1-C6)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 39**）。21-27 は「AIO/AI2AI/llms freshness & governance sync」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（llms*.txt / AI2AI.md / workflow YAML / aio-monitoring-log / manifest）を自前で読み、free-var/glob 依存ゼロ確認。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 21 の位置）**で `checks_governance_sync.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 4,455 → 4,313（−142・Phase 39）。track 元 15,913 から **約 73%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `governance`, `freshness`, `phase39`
- 残る clean クラスタ: 4/5/9/10/12/13/15(early AIO) / 31-41(`_repo_member_paths` setup-global) / 62-69/72(**70=self-integrity 除く**) / 100/102/104-127 / 141/146-148 / 181-190 / 201/215/236/238/266-268 / 304-340/348 / 単発 189/349/360。**不動点: 45/70/105 aggregator + load/ctx-setup infra。**

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 33 個目。今回は「AIO 文書・AI2AI 履歴・llms の日付や整合性が最新か確かめる 7 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 33 split module 横断で緑（Phase 39 で 4,455→4,313）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
