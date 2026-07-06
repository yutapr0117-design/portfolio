---
file: .github/scripts/checks_seo_coherence_b.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-06
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / .github/scripts/checks_seo_coherence.py (part A) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md
---

# .github/scripts/checks_seo_coherence_b.py

## What

`checks_seo_coherence.py`（元 30-check・273-302）を ≤1,000 行に収めるため 2 分割した **part B**。AIO/SEO の entity/meta coherence Check **288-302** を内包し、`run(ctx)` で monolith から呼ばれる（part A = 273-287 は `checks_seo_coherence.py`）。

- 288(ARTICLE_ROUTES ⊆ router) / 289(evidence list counts) / 290-292(entity role/name_alt/name_ja strict) / 293-294(disambiguation) / 295(publisher meta) / 296(link alternate) / 297(sitemap canonical entry) / 298(og:image dims int) / 299(twitter:card) / 300(og:image:alt) / 301(preconnect) / 302(body data-canonical)。

## Why

owner 目標「A 以外の全ファイル ≤1,000 行」に向け、**本トラックが Phase 18 で作った `checks_seo_coherence.py` 自身が 1,252 行と >1,000 だった**ため、Check 288 を境に 2 module へ分割（part A 273-287=690 行 / part B 288-302=590 行・各 ≤1,000）。module-to-module split ゆえ monolith の checks 実装は不変・自己整合 Check 45/70/105 は全 module 横断集約で緑・全 check 出力 diff で byte-equivalent。READ-ONLY ゆえ C6 対象外。

## How

- monolith が既存 `checks_seo_coherence.run(_ctx)` の直後に `import checks_seo_coherence_b; run(_ctx)` を呼ぶ（273-287 → 288-302 の list 順維持）。両 module を `CHECK_SOURCE_FILES` に登録。
- `run()` は part A と同じ `ROOT`/`check` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（両 module 含む）を横断集約。

## Constraints

- **part A/B の完全性**: 273-287 は part A、288-302 は part B。inventory と section の bijection は両 module 合わせて Check 45 が検証。
- **module-global 結合なし**: `re`/`json` のみ import。`exec` 不使用。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- `checks_seo_coherence.py` 1,252 → 690（part A）/ `checks_seo_coherence_b.py` 590（part B）。両者 ≤1,000。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `seo-coherence`, `module-split`, `≤1000`, `phase52`
- **module-to-module split パターン: split module 自身が >1,000 になったら、docstring inventory と run() 内 section を境界 Check で 2 分し、新 module を CHECK_SOURCE_FILES 登録 + dispatch 追加。monolith の checks 実装は不変ゆえ全 check 出力 diff で byte-equivalent。** 他の >1,000 非 A: e2e spec(3,475)/style.css(2,178)/AI2AI-archive(1,513)/index.html(1,308)/docs 複数。

### For human engineers（新卒レベル）
- 分割で作った検査ファイルが今度は自分が大きくなりすぎたので、さらに半分に割った（part A/B）。目標「全ファイル 1,000 行以下」を守るため。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が全 module 横断で緑。抽出前後の全 check 出力 diff で byte-equivalence を実証。
