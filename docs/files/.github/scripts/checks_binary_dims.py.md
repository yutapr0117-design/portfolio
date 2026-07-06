---
file: .github/scripts/checks_binary_dims.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_binary_dims.py

## What

`check_repository_consistency.py` 分割トラックの 45 個目の split module。binary asset の寸法/形式整合 + gate-workflow trigger を守る非連続クラスタ Check **338/339/340/348** を内包し、`run(ctx)` で monolith から呼ばれる。

- 338(og:image:width/height == actual hero WebP dims) / 339(JSON-LD ImageObject dims == WebP dims) / 340(JSON-LD encodingFormat MIME == actual binary format) / 348(both gate workflows trigger on pull_request → main)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 51・🎉 check.py ≤1,000 達成マイルストーン**）。338-340(binary dims/format・WebP magic-byte 解析)/348(workflow trigger)を抽出。各 Check は対象ファイル（index.html / hero.webp / workflow YAML）を自前で読む。`_parse_webp_dims338`(WebP 寸法 parser)は Check 338 内の nested-fn、`_ah338`/`_aw338` は unpack で in-section(false-positive)。WebP binary parsing に `from pathlib import Path` が必要（初回 NameError で判明）。global→nonlocal 変換 2。**本抽出で monolith が 1,167 → 916 行となり、遂に owner 目標「A 以外 ≤1,000 行」を check.py で達成した。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 338 の位置）**で `checks_binary_dims.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json, from pathlib import Path`。global 使用 nested-fn は `nonlocal` へ機械変換。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json`/`Path` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 1,167 → 916（−251・Phase 51）。track 元 15,913 から **約 94.2%減**。🎉 **check.py が owner 目標 ≤1,000 行を達成。**

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `binary-dims`, `milestone`, `phase51`
- **🎉 check.py ≤1,000 達成（916 行）。** 残る 916 行 = 抽出可能な 4/5(csp helper+html)/17-18(root_lastmod)/37(FORBIDDEN ctx 化)/190(_assets ctx 化) + **不動点(残置必須): 45/70/105 self-integrity aggregator + `_aggregate_check_numbers` + load/ctx-setup infra(globals read + `_ctx` 構築 + 全 module dispatch) + setup producer(`_member_paths`/FORBIDDEN/`_repo_member_paths`)**。さらに削るなら 4/5/17/18/37/190 を抽出できるが、残りは check.py の骨格(aggregator + dispatch)。**次フェーズ: owner 合意の順序では C の 2 番目 = e2e spec(3,332 行)分割 → B(style.css 2,178/index.html 1,308/docs)→ capstone(全ファイル ≤1,000 の CI 監査化)。**
- **capstone(防止層)**: 全 tracked file が ≤1,000 であることを BLOCKING 強制する Check を新設(A=mp3/package-lock/main.js/llms-full.txt を除外リストで明示)。C+B 完了後に入れる(順序厳守・§7)。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 45 個目。今回で **check.py が目標の 1,000 行を下回った(916 行・元 15,913 行の約 17 分の 1)**。残りは検査を束ねる骨格部分。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 45 split module 横断で緑（Phase 51 で 1,167→916・**≤1,000 達成**）。抽出前後の全 check 出力 diff で byte-equivalence を実証。15,913→916 の 45-phase 段階分割を、全て非破壊・CI 全緑・byte-equivalent 検証付きで完遂。
