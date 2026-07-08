---
file: .github/scripts/checks_date_sync.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol)
---

# .github/scripts/checks_date_sync.py

## What

`check_repository_consistency.py` 分割トラックの split module。日付同期一貫性を守る **Check 17/18** を内包し、`run(ctx)` で monolith から呼ばれる。

- **17** (ai:last-modified ↔ LAST_UPDATED 同期): `index.html` の `name="ai:last-modified"` meta タグの日付 と `main.js` の `SITE_CONFIG.LAST_UPDATED` が一致することを強制。
- **18** (sitemap.xml root lastmod ↔ ai:last-modified 同期): `sitemap.xml` のルート URL エントリ `<lastmod>` が `ai:last-modified` と一致することを強制（per-URL policy: 他 URL は honest 日付、root URL のみ必須一致）。

## Why

owner 合意 C-first の check.py 段階分割 (Phase 3B)。Check 17 が `html_date` 変数を定義し Check 18 が同変数を消費するため、2 つを coupled-var cluster として同一 module に抽出。ctx-enrich 型: monolith が事前 load した `ctx.html`・`ctx.mainjs` を受け取るため再 read 不要。

## How

- monolith: Check 17 の位置で `checks_date_sync.run(_ctx)` を 1 回呼ぶ。
- `run()` は `ROOT`/`check`/`html`/`mainjs`/`extract`/`warnings` を ctx から unpack。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約し、Check 45/70/105 が自己整合を BLOCKING 強制。

## Constraints

- **ctx-enrich**: `ctx.html`・`ctx.mainjs`・`ctx.extract` が必須 (pre-loaded by monolith)。
- **module-global 結合なし**: `exec` 不使用。依存は全て ctx 経由。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- monolith 行数: Phase 3B 適用後に約 30 行縮小。
- 新 tracked file ゆえ Check 108 が本 doc を BLOCKING で要求。

## Audience-specific notes

### For AI agents（次担当）

- 役割タグ: `check-split`, `date-sync`, `phase3b`
- ctx-enrich cluster パターン。monolith が事前 load した content を ctx で受け取り、run() 内で共有変数 (`html_date`) を定義して後続 Check が消費する結合 cluster。

### For human engineers（新卒レベル）

- サイト更新日の統合チェック。HTML meta タグ・JS 設定定数・sitemap.xml の 3 箇所に同じ日付を持つ invariant を機械強制する。

### For third parties / auditors

- Phase 3B: ctx-enrich cluster の抽出。verify exit 0 + Check 45/70/105 緑で byte-equivalent を実証。
