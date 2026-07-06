---
file: .github/scripts/checks_residual_coherence.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_residual_coherence.py

## What

`check_repository_consistency.py` 分割トラックの 36 個目の split module。2 つの小 self-contained 群 Check **146/147/148 + 304/305/307/308/309** を内包し、`run(ctx)` で monolith から呼ばれる。

- 146(default-project relatedProjectIds integrity) / 147(Speakable cssSelector → live shipped elements) / 148(ARTICLE_ROUTES ⊆ PAGE_META) / 304(theme-color 6-digit hex) / 305(theme-color light+dark media) / 307(sitemap XML decl + close) / 308(sitemap namespaces) / 309(aio-manifest all-URLs HTTPS)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 42**）。残存する 2 つの小 clean 群（project/Speakable/route と theme-color/sitemap/manifest）を効率のため 1 module に統合抽出。各 Check は対象ファイルを自前で読み、free-var/glob 依存ゼロ確認。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 146 の位置）**で `checks_residual_coherence.run(_ctx)` を呼ぶ。
- `run()` は `ROOT`/`check`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 3,672 → 3,333（−339・Phase 42）。track 元 15,913 から **約 79%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `residual-coherence`, `phase42`
- 残る section: 4/5/9/10/12/13/15 / 31-41(`_repo_member_paths` setup-global) / 100/102/104-113(105 self-integrity+`_member_paths`) / 121-127(`_binary_edited`+`_member_paths`) / 141 / 190(`_assets`) / 201/215/236/238/266-268(`_walk`) / 338-340/348 / 349/360 / 43-60(structural・59+72 ESLint pair)。**不動点: 45/70/105 aggregator + load/ctx-setup infra。** 残り ~55 section の多くは setup-global(`_member_paths`/`_repo_member_paths`/`_assets`/`root_lastmod`)や self-integrity 依存 → setup-global を module へ移すか ctx に足す判断が要る。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 36 個目。今回は残っていた小さな検査群(プロジェクト関連・テーマ色・サイトマップ形式など 8 個)を効率のためまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 36 split module 横断で緑（Phase 42 で 3,672→3,333）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
