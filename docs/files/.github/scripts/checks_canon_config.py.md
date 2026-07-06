---
file: .github/scripts/checks_canon_config.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_canon_config.py

## What

`check_repository_consistency.py` 分割トラックの 41 個目の split module。canon-policy / config / meta-governance を守る非連続クラスタ Check **100/102/104/106/107/109/112/113** を内包し、`run(ctx)` で monolith から呼ばれる。

- 100(theme-init.js hardcoded storage keys ↔ constants/brand) / 102(core operating-model policy in canon・102a-f) / 104(verify-gate scripts Python 3.10+ guard) / 106(.nvmrc ↔ CI node single-major) / 107(runbook §11 CI-workflow inventory bijection) / 109(living-doc Check-count hardcode drift guard) / 112(shipped-JS IME composition guard) / 113(commit/PR handoff discipline in canon)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 47**）。canon/config/meta-governance 系の clean な 8 checks を抽出。各 Check は対象ファイル（theme-init.js / AI2AI.md / CLAUDE.md / .nvmrc / runbook / e2e spec 等）を自前で読み、free-var/glob 依存ゼロ確認。**本抽出で monolith が 2,416 → 1,986 行となり、check.py が遂に 2,000 行を下回った（track 元 15,913 から 87.5%減）。** READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 100 の位置）**で `checks_canon_config.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 2,416 → 1,986（−430・Phase 47・**2,000 行突破**）。track 元 15,913 から **約 87.5%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `canon`, `config`, `meta-governance`, `phase47`
- 残る section: 4/5/9/10/12/13/15(early AIO・一部 csp helper+html) / 37(FORBIDDEN も ctx 化で抽出可) / 45(self-integrity・不動点) / 121/123-127(`_binary_edited` producer=127 の relocation で解放可) / 141/190/201/215/236/238/266-268/338-348/349/360。**不動点: 45/70/105 aggregator + load/ctx-setup infra + setup 領域の `_member_paths`/FORBIDDEN producer。** producer-relocation(Phase 46)で `_binary_edited`(127)/`root_lastmod`(17/18) も同様に解放できる。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 41 個目。今回は「規約・設定・運用方針が正しく文書化/設定されているか確かめる 8 の検査」を移した。**これで check.py が 2,000 行を下回った（元 15,913 行の約 8 分の 1）。**

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 41 split module 横断で緑（Phase 47 で 2,416→1,986）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
