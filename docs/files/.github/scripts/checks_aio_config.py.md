---
file: .github/scripts/checks_aio_config.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_aio_config.py

## What

`check_repository_consistency.py` 分割トラックの 34 個目の split module。AIO entity/crawler identity と CI/config governance を守る連続クラスタ Check **62-69** を内包し、`run(ctx)` で monolith から呼ばれる。

- 62(AIO entity canonical_url cross-surface) / 63(crawler discovery origin) / 64(check-map Check-number uniqueness) / 65(doc Last-Updated ISO-8601) / 66(title entity-identifier) / 67(workflow explicit permissions) / 68(dependabot dual-ecosystem) / 69(engines.node ↔ CI node pin)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 40**）。62-69 は「AIO entity/crawler identity + CI/config governance」テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（llms-full / manifest / sitemap / robots / check-map / index.html / workflow YAML / dependabot / package.json）を自前で読む。**教訓再確認: Check 63/64 が `ET.ParseError`（xml.etree.ElementTree・sitemap 解析）を使うため module に `import xml.etree.ElementTree as ET` が必要（初回 NameError で判明）— stdlib import 漏れは安全網が捕捉。** Check 72(ESLint baseline)は `_bsrc59`/`_budget59` を Check 59 と共有する ESLint-baseline pair(59+72)ゆえ残置。70/71 は self-integrity / 抽出済。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 62 の位置）**で `checks_aio_config.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json, xml.etree.ElementTree as ET`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json`/`ET` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 4,313 → 4,049（−264・Phase 40）。track 元 15,913 から **約 75%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `aio-config`, `ci-governance`, `phase40`
- **stdlib import 漏れの教訓（再）: 抽出コードが使う stdlib（`ET`=xml.etree.ElementTree / `ast` / `Path` / `glob` 等）は module import 必須。初回 NameError で安全網が捕捉するので、出たら import を足す。** 残る clean クラスタ: 4/5/9/10/12/13/15 / 31-41(`_repo_member_paths`) / 100/102/104-127 / 141/146-148 / 181-190 / 201/215/236/238/266-268 / 304-340/348 / 単発 189/349/360 / 59+72(ESLint pair) / helper 190/201。不動点: 45/70/105 + load infra。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 34 個目。今回は「AIO の識別情報とクローラ設定・CI の設定が正しいか確かめる 8 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 34 split module 横断で緑（Phase 40 で 4,313→4,049）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
