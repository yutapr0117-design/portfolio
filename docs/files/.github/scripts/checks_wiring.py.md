---
file: .github/scripts/checks_wiring.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_wiring.py

## What

`check_repository_consistency.py` 分割トラックの 13 個目の split module。shipped-asset と AIO evidence が実際に「配線・発見可能」であることを保証する連続クラスタ Check **132-134** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 132**: AIO evidence ↔ sitemap discoverability（manifest の text evidence が sitemap に掲載）。
- **Check 133**: aio-guard.js `<script src>` wiring（AIO self-repair monitor が配線済）。
- **Check 134**: root-script wiring completeness（theme-init/karte-init/main.js が全て配線済）。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 16**）。132-134 は「shipped-asset & AIO wiring / discoverability」という単一テーマの **連続 self-contained クラスタ**。「file が存在する」だけでなく「file が配線/発見可能」であることを守る checks。各 Check は対象ファイル（index.html / sitemap.xml / aio-manifest.json）を自前で `read_text()` し、**free-variable 分析で外部 `_var` ゼロ・global content 依存ゼロを確認**してから抽出した。**NOTE: Check 135（stylesheet wiring）は natural な 4 つ目だが global `style` content を読むため、ctx-enrich phase まで monolith 残置。**

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 131 の後・135 の前）**で `checks_wiring.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。free-var 分析で外部依存ゼロ確認済。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  132.`〜`  134.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 13,058 → 12,948（−110・Phase 16）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `wiring`, `discoverability`, `ctx-injection`, `phase16`
- **連続 self-contained クラスタ抽出**（free-var 分析で事前検証）。135（stylesheet wiring）は `style` global 依存ゆえ ctx-enrich phase で扱う候補。
- 残ターゲット候補（free-var ゼロ確認済）: 125-126（dead-const/eslint）/ 104/106/107（CI/node/runbook config）。要 ctx enrich: 122-124（`_member_paths`）/ 125-127 の 127（`_binary_edited`）/ 135 と 149-360 の html/style 系大カテゴリ（813 参照の最大の塊）。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 13 個目。今回は「公開ファイルがちゃんと読み込まれる配線になっているか・検索エンジンから発見可能か確かめる 3 つの検査」をまとめて移した。「存在する」と「繋がっている」は別物。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 13 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 16 で 13,058→12,948）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
