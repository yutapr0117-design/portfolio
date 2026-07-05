---
file: .github/scripts/checks_shipped_structure.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_shipped_structure.py

## What

`check_repository_consistency.py` 分割トラックの 12 個目の split module。shipped-JS のモジュール構造と資産サイズを守る連続クラスタ Check **118-120** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 118**: PAGE_META route coverage（全 17 shipped route の metadata を PAGE_META が網羅）。
- **Check 119**: factory docstring dependency coherence（全 factory の docstring【依存】節が署名の注入依存を網羅）。
- **Check 120**: shipped JS+CSS byte-weight budget（page-weight / CWV 保護）。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 15**）。118-120 は「shipped-JS structural coherence & byte budget」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（main.js / js/*.js / style.css）を自前で `read_text()` し、global content（html/style/mainjs）依存はない。**free-variable 分析（使用のみ・未定義の `_`-var 検出）で外部 `_var` ゼロを確認**してから抽出した（この手法は Phase 15 で `_member_paths` 型の shared-infra 結合を事前検知するために導入 — 122-124 の抽出試行で Check 122 が `_member_paths`（tracked-files 共有リスト）に依存し NameError で abort した反省から）。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 117 の後・121 の前）**で `checks_shipped_structure.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re` のみ module import。`exec` 不使用。free-var 分析で外部依存ゼロを確認済。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  118.`〜`  120.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 13,161 → 13,058（−103・Phase 15）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `shipped-structure`, `byte-budget`, `ctx-injection`, `phase15`
- **連続 self-contained クラスタ抽出**。**最重要教訓（Phase 15 で確立）: 抽出前に free-variable 分析を必ず行う — 「定義されず使用のみ」の `_`-var（例 `_member_paths`・`_binary_edited`）は monolith 上流で計算される shared-infra への結合で、DEFINED-var スコープ検査では見つからない。`/tmp/freevars.py` 型の free-var 検出を候補範囲に走らせ、外部 `_var` が 0 であることを確認してから抽出せよ。** 122-124(`_member_paths` 依存) と 125-127(`_binary_edited` 依存) は ctx enrich か helper 再取得が必要。
- 残ターゲット候補（free-var ゼロ確認済）: 133-134（wiring）。要 ctx enrich: 122-124（`_member_paths`）/ 125-127（`_binary_edited`）/ 115 含む html 系。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 12 個目。今回は「アプリの各ページに必要な情報が揃っているか・ファイルサイズが予算内か等、公開コードの構造と重さを確かめる 3 つの検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 12 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 15 で 13,161→13,058）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
