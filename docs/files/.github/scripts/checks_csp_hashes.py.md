---
file: .github/scripts/checks_csp_hashes.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol)
---

# .github/scripts/checks_csp_hashes.py

## What

`check_repository_consistency.py` 分割トラックの split module。inline-script CSP ハッシュ検証 **Check 7b/7c** を内包し、`run(ctx)` で monolith から呼ばれる。

- **7b** (inline suppressor ハッシュ): `index.html` の `unhandledrejection` リスナーを含む plain `<script>` ブロックの SHA-256 content hash が CSP `script-src` に存在することを強制。
- **7c** (speculationrules ハッシュ): `<script type="speculationrules">` ブロックの SHA-256 content hash が CSP `script-src` に存在することを強制。Chrome は hash 不一致時 "Applying inline speculation rules violates ... script-src" でプリレンダをブロックする。

両 Check とも live 内容からハッシュを計算するため、ハッシュ欠落と「内容編集後のハッシュ未更新」の両方を捕捉する。

## Why

owner 合意 C-first の check.py 段階分割 (Phase 3C)。Check 7b/7c は `ctx.html` + `_lib_io.csp_sri_hash` + `re` だけで自己完結するため、ctx-enrich なしで最小コスト抽出が可能。

## How

- monolith: Check 7b の位置で `checks_csp_hashes.run(_ctx)` を 1 回呼ぶ。
- `run()` は `check`/`html`/`warnings` を ctx から unpack、`_lib_io.csp_sri_hash` を module 内で直接 import。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約し、Check 45/70/105 が自己整合を BLOCKING 強制。

## Constraints

- **ctx-enrich**: `ctx.html` が必須 (pre-loaded by monolith)。
- **module-global 結合なし**: `exec` 不使用。依存は全て ctx 経由または module 内 import。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。7b/7c は sub-check 番号ゆえ Check 45 の 1..N カウントに含まれない (正常動作)。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- monolith 行数: Phase 3C 適用後に約 45 行縮小。
- 新 tracked file ゆえ Check 108 が本 doc を BLOCKING で要求。

## Audience-specific notes

### For AI agents（次担当）

- 役割タグ: `check-split`, `csp-hashes`, `phase3c`
- `_lib_io.csp_sri_hash` を module 内で `from _lib_io import csp_sri_hash as _lib_csp_sri_hash` でインポートする ctx-independent helper 依存パターン。

### For human engineers（新卒レベル）

- CSP (Content Security Policy) の `script-src` には inline `<script>` ごとの SHA-256 ハッシュが必要。このモジュールは index.html の実際の内容からハッシュを計算して、CSP に正しく登録されているかを検証する。

### For third parties / auditors

- Phase 3C: ctx-enrich 最小 cluster の抽出。verify exit 0 + Check 45/70/105 緑で byte-equivalent を実証。
