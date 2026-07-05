---
file: .github/scripts/checks_ci_verify.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_ci_verify.py

## What

`check_repository_consistency.py` 分割トラックの 27 個目の split module。CI 検証チェーンの配線を守る連続クラスタ Check **345-347** を内包し、`run(ctx)` で monolith から呼ばれる。

- 345(package.json verify が全 4 検証層を連結) / 346(CI workflow が consistency guard 自体を実行) / 347(CI behavior e2e gate が実行され BLOCKING)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 30**）。345-347 は「CI verification-chain wiring」テーマの **連続 self-contained クラスタ**。各 Check は package.json / CI workflow YAML を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。global→nonlocal 変換 0 箇所。**NOTE: 隣接の 344（style.css @layer・style glob）/ 348（`_has_pr_main_trigger348` gap）は残置。**

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 344 の後・348 の前）**で `checks_ci_verify.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  345.`〜`  347.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 6,965 → 6,840（−125・Phase 30）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `ci`, `verify-chain`, `phase30`
- 残ターゲット（freevars4-clean）: 341-343(3) / 349(1) / 357-359(3)。以降は ctx-enrich（style/html glob）か helper 同梱が必要（handoff §0 参照）。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 27 個目。今回は「CI が全検証層を正しく呼ぶか確かめる 3 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 27 split module 横断で緑（Phase 30 で 6,965→6,840）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
