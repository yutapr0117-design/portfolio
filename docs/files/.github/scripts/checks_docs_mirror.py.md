---
file: .github/scripts/checks_docs_mirror.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_docs_mirror.py

## What

`check_repository_consistency.py` 分割トラックの 6 つ目の split module（1=maintainability / 2=structural / 3=esm / 4=tooling / 5=entity）。`docs/files/` の 1 対 1 ミラードキュメント層を統治する連続クラスタ Check **96-99** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 96**: Phase 1 shipped-code 1-to-1 docs bijection（curated shipped/AIO/config/binary/dot/meta-docs 集合が `docs/files/<path>.md` を持つ）。
- **Check 97**: `docs/files/*.md` frontmatter integrity（file / audience / last-updated / canonical-ref + file:==derived path）。
- **Check 98**: `docs/files/*.md` 5+1-axis section presence（What / Why / How / Constraints / Change impact / Audience-specific notes）。
- **Check 99**: `docs/files/README.md`（inventory）+ `_template.md`（5-軸 template）presence。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 9**）。96-99 は「`docs/files` ミラードキュメントのガバナンス」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（`docs/files/**` と curated shipped-file 一覧）を自前で読み、global content（html/style/mainjs）依存はない。局所 scratch 変数（`_fm`/`_fm_body`/`_missing_sec`/`_doc`/`_src`）は各 section が使用直前に再代入するローカルパターンで、全てクラスタ内に閉じる。ctx enrich 不要で安全に一括抽出できた。**NOTE: Check 108（`docs/files` ↔ tracked-files FULL bijection）は兄弟だが非連続ゆえ monolith 残置**（将来 docs-mirror 系を集約する場合の候補）。

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、**元の実行位置（Check 95 の後・100 の前）**で `checks_docs_mirror.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`（warnings/read/extract は本クラスタ未使用）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  96.`〜`  99.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **クラスタの完全性**: 96-99 の局所変数を参照する Check は必ず本 module 内に置く。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす（本ファイルも 96/108 の被覆対象になる = 自己ミラー）。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 14,251 → 14,053（−198・Phase 9）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `docs-mirror`, `governance`, `ctx-injection`, `phase9`
- **連続 self-contained クラスタ抽出**（entity 81-90・tooling 74-80・structural 48-51 と同型）。**教訓: Check 96 の shipped-file 一覧は文字列リテラル（`"main.js", "index.html", ...`）で、depmap の bare-word global 検知を誤発火させる — 文字列リテラルと変数参照を区別して self-containment を判定する。**
- 残ターゲット候補: 92-95（AIO C6 derived-value / date tools）/ 104-114（verify-gate / e2e guard / canon policy）/ `_ctx` enrich が必要な html 系大カテゴリ。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 6 個目。今回は「全ファイルに 1 対 1 の説明ドキュメントが揃っているか・各ドキュメントの体裁(見出し/frontmatter)が正しいか確かめる 4 つの検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 6 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 9 で 14,251→14,053）。
