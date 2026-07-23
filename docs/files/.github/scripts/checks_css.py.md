---
file: .github/scripts/checks_css.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-23
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_css.py

## What

`check_repository_consistency.py` 分割トラックの 28 個目の split module・**初の ctx-enrich module**。style.css / CSS contract を守る非連続クラスタ Check **6/73/101/103/135/174/321/322/323/344/356/378/383/384**（14 checks）を内包し、`run(ctx)` で monolith から呼ばれる。

- 6/135(design-token / stylesheet baseline) / 73(a11y-CWV attribute contract) / 101(forced-colors HCM focus) / 103(prefers-contrast) / 174(theme-color literals) / 321(@import 0) / 322(inline `<style>` 0) / 323(style attribute 0) / 344(@layer allowlist) / 356(Google Fonts CSP pair) / 378(MOBILE_BREAKPOINT JS↔CSS coherence) / 383(prefers-reduced-motion global reset) / 384(base :focus-visible outline)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 34**・**ctx-enrich パターンの確立**）。これらは monolith の `style` global（pre-loaded style.css content）を読むため、これまで残置していた（file を自前 read せず global を参照する）。**解決 = `_ctx` を enrich**: monolith が globals load 後に `_ctx.style = style` を attach し、本 module が `run()` で `style = ctx.style` を unpack する。これで glob-dependent なカテゴリが抽出可能になった（残る html/mainjs/ai2ai/mcp_data 依存カテゴリも同パターンで解放できる）。**教訓（Phase 34）: ctx-enrich module は glob 値（style）に加え、section が使う `read`/`extract` も ctx から unpack する必要がある（Check 73 が `read("index.html")` 使用・初回 NameError で判明）。** style 以外の cross-section 結合はなし。READ-ONLY ゆえ C6 対象外。

## How

- monolith: `_ctx` 定義（globals load 前）の後、globals load 直後に `_ctx.style = style` を attach（`# ctx enrichment for split modules` ブロック）。
- **元の実行位置（Check 6 の位置・最小番号 target）**で `checks_css.run(_ctx)` を呼ぶ。14 checks は list 順で連続実行（順序非依存・全出力 diff で byte-identical 実証）。
- `run()` は `ROOT`/`check`/**`style`**/`read`/`extract` を ctx から unpack し `import re, json`。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **ctx-enrich 依存**: 本 module は `ctx.style` を必要とする。monolith が `_ctx.style = style` を attach していること（globals load 後）が前提。将来 html/mainjs 等を使う module は monolith 側で `_ctx.<name> = <name>` を追加してから unpack する。
- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 6,100 → 5,710（−390・Phase 34）。track 元 15,913 から **約 64%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `css`, `ctx-enrich`, `phase34`
- **ctx-enrich パターン確立**（本 module が初例）。残る glob-dependent カテゴリ: `html` glob=7/8/14/17/20/115/152/187/220/250/255/303/306 / `mainjs` glob=2/17 / `ai2ai` glob=1/14 / `mcp_data` glob=3 / version 系(html_v/ai2ai_v/mainjs_v)=1/2/3/19。**各カテゴリ抽出時に monolith 側 `_ctx.<name> = <name>` を追加し module で unpack する。version 系（html_v 等）は Check 内で computed されるため、それらを使う下流 check も同 module に含めるか _ctx に足すか要検討。** section が `read`/`extract` を使う場合は必ず unpack（Check 73 の教訓）。
- 残る非-glob ターゲット: helper 同梱（`_lib_csp_sri_hash`=350 / `_walkNNN`=190/201）/ 単発(189/349/360)。自己整合 aggregator + load/ctx-setup infra は残置（不動点）。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 28 個目・初の「共有データを渡して切り出す」方式。今回は「CSS(見た目の定義)が正しいか確かめる検査群」を、事前に読み込んだ style.css の中身を渡す形で移した（分離時 11・その後 378/383/384 を追加し現在 14）。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 28 split module 横断で緑（Phase 34 で 6,100→5,710）。抽出前後の全 check 出力 diff で byte-equivalence を実証。ctx-enrich という新パターンの初適用を透明に記録。
