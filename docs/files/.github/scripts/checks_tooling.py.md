---
file: .github/scripts/checks_tooling.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_tooling.py

## What

`check_repository_consistency.py` 分割トラックの 4 つ目の split module（1=`checks_maintainability.py` / 2=`checks_structural.py` / 3=`checks_esm.py`）。repository dev-tooling & Claude Code config-file の整合性 Check **74-80**（連続クラスタ）を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 74**: `.github/scripts/_lib_io.py` helper module integrity（read/read_bytes/extract/csp_sri_hash の 4 helper API）。
- **Check 75**: `docs/incident-artifacts/` README inventory completeness（全 artifact file が README に列挙）。
- **Check 76**: `.claude/settings.json` security baseline（self-drive 安全境界 deny 群の presence）。
- **Check 77**: `.claude/commands/*.md` slash-command frontmatter integrity。
- **Check 78**: `.claude/agents/*.md` sub-agent frontmatter integrity（name==stem + description）。
- **Check 79**: `.mcp.json` JSON parsability（mcpServers dict）。
- **Check 80**: `.claude/skills/*/SKILL.md` frontmatter integrity（name==dir + description）。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 7**）。74-80 は「repo 開発ツールと Claude Code 設定ファイルの整合性」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（`_lib_io.py` / incident README / `.claude/**` / `.mcp.json`）を自前で `read_text()` するため global content（html/style/mainjs）への依存がなく、局所変数（`_lib74` / `_settings76` / `_mcp79` 等）も全てクラスタ内に閉じる（抽出前に `_asrc`/`_csrc`/`_ssrc` 等の汎用名も含め全変数がクラスタ内定義・クラスタ内参照であることを grep で確認済）。ctx enrich 不要で安全に一括抽出できた。

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、**元の実行位置（Check 73 の後・81 の前）**で `checks_tooling.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check`/`warnings` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors`/`ctx.warnings` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  74.`〜`  80.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **クラスタの完全性**: 74-80 の局所変数を参照する Check は必ず本 module 内に置く。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 14,717 → 14,476（−241・Phase 7）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `dev-tooling`, `claude-config`, `ctx-injection`, `phase7`
- **連続 self-contained クラスタ抽出**（structural 48-51 と同型・coupled-group ではない）。Phase 6（checks_esm の coupled-group）とは別パターン。**教訓: 連続ブロックは reorder が起きず最も安全。抽出前に汎用名局所変数（`_asrc` 等）まで grep で「クラスタ内定義・クラスタ内参照」を確認する。**
- 残ターゲット候補: AIO/entity Organization cross-surface（82-90・81 は global 依存で要 ctx enrich）/ `_ctx` enrich が必要な html 系大カテゴリ。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 4 個目。今回は「開発ツールと Claude Code の設定ファイルが壊れていないか確かめる 7 つの検査」をひとまとめに移した。連続していて他と変数を共有しないので、最も安全な切り出し。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 4 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 7 で 14,717→14,476）。
