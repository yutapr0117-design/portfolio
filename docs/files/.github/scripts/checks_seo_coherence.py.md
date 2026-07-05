---
file: .github/scripts/checks_seo_coherence.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_seo_coherence.py

## What

`check_repository_consistency.py` 分割トラックの 15 個目の split module。AIO/SEO の cross-surface URL・canonical・format coherence を強制する大型連続クラスタ Check **273-302**（30 Check）を内包し、`run(ctx)` で monolith から呼ばれる。

テーマ: canonical URL 一貫性 / HTTPS-only / manifest↔JSON-LD entity 等価 / strict format 契約（VERSION / CACHE_NAME / manifest_version）/ og・twitter・meta coherence。代表例 — 273(JSON-LD date 未来なし) / 274-277(manifest↔JSON-LD entity/Org 等価) / 278-284(HTTPS + SITE_CONFIG↔ai:* URL 等価) / 285-287(strict format) / 288-294(ARTICLE_ROUTES / entity role・name・disambiguation) / 295-302(publisher / alternate / sitemap / og:image / twitter:card / preconnect / data-canonical)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 18**・本トラック最大の単一削減 −1,213 行）。273-302 は「AIO/SEO URL-canonical-format coherence」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（aio-manifest.json / index.html / main.js / sitemap.xml / robots.txt / sw.js）を自前で `read_text()` し global content 依存なし。**annotation-aware + def-aware free-variable 分析**で外部 `_var` ゼロを確認してから抽出した。**READ-ONLY coherence 検査ゆえ C6 対象外。**

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 272 の後・303 の前）**で `checks_seo_coherence.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- **`global` → `nonlocal` 機械変換**: 幾つかの section は nested walker/counter で section-local accumulator（`_total_dates273` 等）を mutate する。module-level ではこれに `global` 宣言を使っていたが、`run()` 内へ移すと `global` は run() の local に届かないため、移設ブロックの `global _accNNN` を機械的に `nonlocal _accNNN` へ変換（意味等価 — accumulator は section スコープ = run() の local として nested fn より前に定義済み）。本 phase で 4 箇所（273/274/275/276）変換。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。annotation+def-aware free-var 分析で外部依存ゼロ確認済。
- **READ-ONLY**: AIO/shipped ファイルを読むが編集しない。C6 semantic 編集ではないため aio-guardian 承認は不要。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  273.`〜`  302.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 12,696 → 11,483（−1,213・Phase 18・本トラック最大の単一 PR 削減）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `seo`, `url-canonical`, `format-coherence`, `aio-readonly`, `ctx-injection`, `phase18`
- **最重要教訓（Phase 18）: nested 関数が `global _accNNN`（module-level accumulator パターン）を使う section を `run(ctx)` へ移す際は、`global` → `nonlocal` へ機械変換せよ。** module-level では `global` が section-local accumulator を mutate するが、`run()` 内では `global` が run() の local に届かず `NameError` で全 run abort する（安全網が exit 1 で検知）。`^\s*global\s+` を `nonlocal ` に置換（accumulator が section スコープ = run() local として nested fn より前に定義済みであることを確認）。抽出前に候補範囲の `grep -nE '^\s*global\s'` で該当箇所を把握せよ（残る global 使用 section: 218/235/245-247/251/256-261/266-268/339/340）。
- 残ターゲット（annotation+def-aware で clean・大型連続 run）: 221-235(15・global 235 要変換) / 324-337(14) / 311-320(10) / 191-200(10) / 202-207 / 209-214 / 242-249(global 245-247 要変換) / 256-261(global 要変換) など。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 15 個目・**本トラック最大の一括移動（30 検査・約 1,200 行）**。今回は「公開 URL が全ファイルで一致しているか・HTTPS か・形式が正しいか等、SEO と AIO の URL 整合を確かめる 30 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 15 split module 横断で緑を保ちながら、監査可能なステップで monolith を縮小している透明な記録（Phase 18 で 12,696→11,483）。抽出前後の全 check 出力 diff で byte-equivalence を実証（`global`→`nonlocal` 変換後も 364 出力が identical）。
