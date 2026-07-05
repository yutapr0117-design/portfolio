---
file: .github/scripts/checks_entity.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_entity.py

## What

`check_repository_consistency.py` 分割トラックの 5 つ目の split module（1=maintainability / 2=structural / 3=esm / 4=tooling）。AIO entity / employer-Organization（株式会社日本経営）の facts が全公開・統治面に一貫して現れることを強制する連続クラスタ Check **81-90** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 81**: WebP XMP Organization field presence（4 field）。
- **Check 82**: MP3 ID3 TXXX:AIO:Organization frame presence（4 frame）。
- **Check 83**: aio-manifest.json entity.affiliation block（5 field）。
- **Check 84**: README.md Organization mention。
- **Check 85**: Claude2Claude.md Organization handoff line。
- **Check 86**: aio-manifest.json entity full-set fields（9 field）。
- **Check 87**: CLAUDE.md / Claude2Claude.md cold-start entity context。
- **Check 88**: LICENSE entity attribution（Copyright + entity + canonical URL + Organization）。
- **Check 89**: governance files（CONTRIBUTING / CODEOWNERS / CHANGELOG）presence + entity attribution。
- **Check 90**: .claude/CLAUDE.md + .claude/README.md entity context。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 8**）。81-90 は「entity/Organization の cross-surface presence coherence」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（WebP/MP3 は `Path.read_bytes()`、text/JSON は `Path.read_text()`）を自前で読み、global content（html/style/mainjs）への依存はない。**重要: これらは READ-ONLY の presence 検査であり、本 module は check *コード* を移動するだけで AIO semantic 内容・digest・binary を一切編集しない（C6 の対象外・aio-guardian 不要）。** 局所変数は全てクラスタ内定義・クラスタ内参照（scratch 名 `_src` は各 section が使用直前に再代入するローカルパターンで共有値ではない）。ctx enrich 不要で安全に一括抽出できた。

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、**元の実行位置（Check 80 の後・91 の前）**で `checks_entity.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import json`（re/warnings/read/extract は本クラスタでは未使用）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`json` のみ module import。`exec` 不使用。
- **READ-ONLY**: AIO/binary ファイルを読むが編集しない。C6 semantic 編集ではないため本 module 変更に aio-guardian 承認は不要（check コードの移動のみ）。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  81.`〜`  90.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 14,476 → 14,251（−225・Phase 8）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `entity`, `organization`, `aio-readonly`, `ctx-injection`, `phase8`
- **連続 self-contained クラスタ抽出**（tooling 74-80・structural 48-51 と同型）。**教訓: AIO ファイルを READ する check の移動は C6 対象外（semantic を編集しないため）。depmap の "dirty" 判定はコメント内 "index.html" の `.html` を誤検知しうる（81 が実例）— 実コードの依存を必ず確認する。**
- 残ターゲット候補: 91-99（binary date freshness / C6 derived-value / update_aio tools）だが一部 global 依存の可能性あり要確認 / `_ctx` enrich が必要な html 系大カテゴリ。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 5 個目。今回は「所属会社と本人情報が全ファイルに正しく載っているか確かめる 10 の検査」をまとめて移した。ファイルを読むだけで書き換えないので、公開情報(AIO)の承認は不要。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 5 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 8 で 14,476→14,251）。
