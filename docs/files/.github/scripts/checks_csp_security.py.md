---
file: .github/scripts/checks_csp_security.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_csp_security.py

## What

`check_repository_consistency.py` 分割トラックの 26 個目の split module。shipped-JS のセキュリティ契約と CSP による外部 script host 認可を守る連続クラスタ Check **351-355** を内包し、`run(ctx)` で monolith から呼ばれる。

- 351(sitemap `<url>` block が `<loc>` を厳密 1 個) / 352(h() fail-closed innerHTML 禁止保持) / 353(js/ui-components.js に DOMParser 不在) / 354(外部 script host が CSP script-src で authorize) / 355(外部 script host が CSP connect-src で authorize)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 29**）。351-355 は「shipped-JS security contract + CSP script authorization」テーマの **連続 self-contained クラスタ**。各 Check は index.html / js/ui-components.js / sitemap.xml を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。global→nonlocal 変換 0 箇所。READ-ONLY ゆえ C6 対象外。**NOTE: 隣接の 356（Google Fonts CSP pair）は global `style` 依存ゆえ ctx-enrich phase まで monolith 残置。**

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 350 の後・356 の前）**で `checks_csp_security.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  351.`〜`  355.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 7,165 → 6,965（−200・Phase 29）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `csp`, `security`, `phase29`
- 残ターゲット（freevars4-clean・非連続でも可）: 341-343(3) / 345-347(3) / 349(1) / 357-359(3)。**ctx-enrich が必要な残 gap**: 344/356（`style` glob）/ 174/187/220/250/255（`html` glob）/ 350（`_lib_csp_sri_hash` helper 依存）/ 190・201・237-241・262-265・269-272（`_walkNNN`/`_glob237`/`_src`/`_assets`/`_template` の cross-section 共有 nested-fn/var）。これらは `_ctx` を html/style/`_member_paths`/helper で enrich するか、共有 helper を module へ同梱して抽出する（次フェーズの主題）。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 26 個目。今回は「公開 JS の安全契約(危険な HTML 生成禁止)と外部スクリプトの許可設定(CSP)が正しいか確かめる 5 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 26 split module 横断で緑（Phase 29 で 7,165→6,965・track 元 15,913 から約 56%減）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
