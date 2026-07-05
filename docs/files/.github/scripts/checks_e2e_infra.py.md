---
file: .github/scripts/checks_e2e_infra.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_e2e_infra.py

## What

`check_repository_consistency.py` 分割トラックの 11 個目の split module。Playwright behavior-e2e ハーネスの健全性を守る **非連続クラスタ** Check **110 / 111 / 114 / 116 / 117** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 110**: e2e A11Y_ROUTES ↔ ALL_ROUTES coverage bijection。
- **Check 111**: e2e no-`networkidle` guard（外部 Fonts/SW で CI hang する flake 防止）。
- **Check 114**: e2e no-`.only` guard（`.only` 混入で他テストが silent skip するのを防止）。
- **Check 116**: playwright.config.cjs `reuseExistingServer=false`。
- **Check 117**: playwright.config.cjs screenshot tolerance sanity ceiling。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 14**）。110/111/114/116/117 は「e2e / Playwright test-infrastructure hygiene」という単一テーマだが monolith 上では 112（IME guard・shipped-JS ゆえ checks_behavioral 系）/ 113（canon discipline）/ 115（CSP・html 依存）と interleave していた。これら 3 つは monolith 残置し、テーマ一致する 5 Check だけを **非連続抽出**した（Phase 6 の esm クラスタと同じ非連続抽出パターン）。各 Check は対象ファイル（`e2e/*.spec.js` / `playwright.config.cjs`）を自前で `read_text()` し global content 依存なし。全 bare 局所変数（`_pwcfg`/`_pwsrc`/`_reuse_ok`/`_mdpr`/`_mdpr_val`）はターゲット内に閉じる（抽出前に outside-target 参照 0 を grep で確認）。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**Check 110 の元の実行位置**で `checks_e2e_infra.run(_ctx)` を呼ぶ。110/111/114/116/117 は本 module 内で連続実行される（各 Check は共有 errors/warnings に append するだけゆえ **順序非依存**・抽出前後で全 364 出力を `sort | diff` して byte-identical を実証）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  110.`/`  111.`/`  114.`/`  116.`/`  117.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **クラスタの完全性**: 110/111/114/116/117 の局所変数を参照する Check は必ず本 module 内に置く。112/113/115 は monolith 残置（別テーマ / html 依存）。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 13,280 → 13,161（−119・Phase 14）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `e2e`, `playwright`, `test-infra`, `non-contiguous`, `ctx-injection`, `phase14`
- **非連続クラスタ抽出**（esm 47/56/57/61 と同型）。**教訓: interleave した別テーマ Check（ここでは 112/113/115）は残置し、テーマ一致する Check だけを非連続抽出できる。抽出前に bare 局所変数の outside-target 参照が 0 であることを grep で確認し、抽出後は全出力 diff で byte-identical を証明する。**
- 残ターゲット候補: 122-124（privacy/policy）/ 118-120（shipped-JS structural + perf budget）/ 104/106/107/109（CI/node/doc config）/ 125-127（dead-code/eslint/digest）/ 132-134（AIO sitemap + wiring・135 は style 依存）/ 115 含む html 系は ctx enrich 要。**105/108 は self-integrity/mirror-full 系ゆえ慎重に。**

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 11 個目。今回は「自動テスト(Playwright)の設定・書き方が壊れていないか確かめる 5 つの検査」をまとめて移した。間に別テーマの検査が挟まっていたが、テーマの合う 5 つだけを飛び飛びに移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 11 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 14 で 13,280→13,161）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
