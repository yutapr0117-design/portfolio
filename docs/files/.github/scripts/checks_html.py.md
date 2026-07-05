---
file: .github/scripts/checks_html.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_html.py

## What

`check_repository_consistency.py` 分割トラックの 29 個目の split module・2 個目の ctx-enrich module。index.html の document/meta baseline と `<html lang>` coherence を守る非連続クラスタ Check **8/20/115/152/187/220/250/255/303/306**（10 checks）を内包し、`run(ctx)` で monolith から呼ばれる。

- 8(nosniff meta) / 20(og:image dims) / 115(CSP hardening baseline) / 152(`<html lang>` ↔ inLanguage) / 187(og:locale ↔ lang) / 220(manifest.lang ↔ lang) / 250(lang BCP-47 valid) / 255(DOCTYPE) / 303(data-theme/data-brand) / 306(closing `</html>`)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 35**）。これらは monolith の `html` global（pre-loaded index.html content）を読むため残置していた。**checks_css と同じ ctx-enrich パターン**: monolith が globals load 後に `_ctx.html = html` を attach し、本 module が `run()` で `html = ctx.html` を unpack。**Check 7（CSP-before-suppressor）は除外**（`_lib_io.csp_sri_hash` helper 依存 = 別途 helper-consolidation task）。section が使う `read`/`extract` も unpack（checks_css の教訓）。html 以外の cross-section 結合なし。READ-ONLY ゆえ C6 対象外。

## How

- monolith: globals load 直後に `_ctx.html = html`（`_ctx.style = style` と同ブロック）。
- **元の実行位置（Check 8 の位置・最小番号 target）**で `checks_html.run(_ctx)` を呼ぶ。10 checks は list 順で連続実行（順序非依存・全出力 diff で byte-identical 実証）。
- `run()` は `ROOT`/`check`/`html`/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **ctx-enrich 依存**: `ctx.html` を必要とする（monolith が `_ctx.html = html` を attach 済み前提）。
- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 5,710 → 5,372（−338・Phase 35）。track 元 15,913 から **約 66%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `html`, `lang-coherence`, `ctx-enrich`, `phase35`
- 残る glob-dependent: `html`+other=7(csp_sri_hash helper)/14(ai2ai)/17(mainjs) / `mainjs`=2/17 / `ai2ai`=1/14 / `mcp_data`=3 / version 系=1/2/3/19。各抽出時に `_ctx.<name>` を追加。version 系(html_v 等)は Check 1/2/3 で computed → 下流 check を同 module に含めるか _ctx に computed 値を足す。
- helper 同梱=7/350(`_lib_io.csp_sri_hash`)/190/201(`_walkNNN`)。単発=189/349/360。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 29 個目。今回は「公開 HTML の meta・言語設定・文書構造が正しいか確かめる 10 の検査」を、事前に読み込んだ index.html の中身を渡す形で移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 29 split module 横断で緑（Phase 35 で 5,710→5,372）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
