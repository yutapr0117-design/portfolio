---
file: .github/scripts/checks_eslint_budget.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_eslint_budget.py

## What

`check_repository_consistency.py` 分割トラックの 39 個目の split module。ESLint warning-baseline と file-size-budget governance を守る producer/consumer trio Check **59/60/72** を内包し、`run(ctx)` で monolith から呼ばれる。

- 59(file-size-budget §2表 ↔ §4 BUDGET-DATA set equality・PRODUCER of `_bsrc59`/`_budget59`) / 60(ESLint warning-baseline regression guard・ADVISORY・consumer) / 72(ESLint baseline absolute-ceiling contract・consumer)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 45**）。59/60/72 は producer/consumer trio: **Check 59 が `_bsrc59`（file-size-budget.md content）/ `_budget59`（path）を定義し、60・72 が消費**する。全 3 者を full-set 一括抽出し共有 var を module-local 化（60 単独 / 72 単独の naive slice は `_budget59` NameError で crash → 安全網が検知）。**教訓: ADVISORY check（60）は `check()` でなく `warnings.append()` を直接呼ぶため、module で `warnings = ctx.warnings` を unpack する必要がある（初回 NameError で判明）。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 59 の位置）**で `checks_eslint_budget.run(_ctx)` を呼ぶ。59→60→72 の list 順で `_bsrc59`/`_budget59` が消費者より前に bind。
- `run()` は `ROOT`/`check`/`read`/`extract`/**`warnings`** を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **full-set 完全性**: 59(producer) + 60/72(consumer) は 3 つ一括でのみ抽出可能（部分 slice は crash）。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 2,575 → 2,467（−108・Phase 45）。track 元 15,913 から **約 84.5%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `eslint`, `budget`, `producer-consumer`, `phase45`
- **教訓: ADVISORY check（`warnings.append()` 直接呼び）を含むクラスタは module で `warnings = ctx.warnings` を unpack せよ（`check()` 経由でない ADVISORY は warnings に直接 append する）。** 残る section: 4/5/9/10/12/13/15(early AIO) / 37(`_member_paths` producer) / 45(self-integrity・不動点) / 100/102/104-113/121-127(`_member_paths`/`_binary_edited` consumer — 37 producer を setup 領域へ移し `_ctx._member_paths` attach する別 PR で一括解放可能) / 141/190/201/215/236/238/266-268/338-348/349/360。**不動点: 45/70/105 aggregator + load/ctx-setup infra。**

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 39 個目。今回は「ESLint の警告数とファイルサイズ予算を守る 3 つの検査」を移した。1 つ(59)が予算データを読み込み、他 2 つ(60/72)がそれを使うので、3 つ一緒でないと動かない。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 39 split module 横断で緑（Phase 45 で 2,575→2,467）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
