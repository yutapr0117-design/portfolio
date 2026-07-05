---
file: .github/scripts/checks_aio_derived.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_aio_derived.py

## What

`check_repository_consistency.py` 分割トラックの 7 つ目の split module（1=maintainability / 2=structural / 3=esm / 4=tooling / 5=entity / 6=docs_mirror）。C6 derived-value（日付・digest 自動同期）機構の整合性を守る連続クラスタ Check **91-95** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 91**: binary metadata date freshness（WebP/MP3/manifest の日付フィールドが 1 つの日付を共有）。
- **Check 92**: C6 derived-value exception canon presence（CLAUDE.md + AI2AI.md が A1/A2 例外を文書化）。
- **Check 93**: aio-manifest.json last_metadata_update field present（ISO-8601）。
- **Check 94**: update_aio_digests.py / update_binary_aio_organization.py tool integrity（日付 sync helper 参照）。
- **Check 95**: _lib_io.py date helpers（now_iso8601 / update_webp_xmp_dates / update_mp3_metadata_date）。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 10**）。91-95 は「C6 derived-value & AIO date-sync tooling の整合性」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（WebP/MP3 は `Path.read_bytes()`、text/JSON/py は `Path.read_text()`）を自前で読み、global content（html/style/mainjs）依存はない。**checks_entity.py と同様 READ-ONLY 整合性検査であり、本 module は check *コード* を移動するだけで AIO semantic 内容・digest を一切編集しない（C6 対象外）。** 局所 scratch 変数（`_src`/`_m_lmu`/`_m_metadata`/`_m_modify`/`_m_id3`）は各 section が使用直前に再代入するローカルで全てクラスタ内に閉じる。ctx enrich 不要で安全に一括抽出できた。

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、**元の実行位置（Check 90 の後・96 の前）**で `checks_aio_derived.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`（warnings/read/extract は本クラスタ未使用・read_bytes は Path メソッド）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **READ-ONLY**: AIO/binary ファイルを読むが編集しない。C6 semantic 編集ではないため本 module 変更に aio-guardian 承認は不要。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  91.`〜`  95.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 14,053 → 13,930（−123・Phase 10）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `aio-derived`, `c6`, `date-sync`, `aio-readonly`, `ctx-injection`, `phase10`
- **連続 self-contained クラスタ抽出**（entity 81-90・docs_mirror 96-99 と同型）。**教訓: 精緻な depmap は「full-comment 行 skip + inline comment strip + 文字列リテラル/属性アクセスを除外した bare-word global 検知」で判定せよ（naive 版はコメント "index.html" と文字列 "main.js" を誤検知した）。**
- 残ターゲット候補: 104/106/107/109（CI/node config meta）/ 110/111/112/114/116/117（e2e guard + playwright config）/ 118-146 の各テーマ束。**105 は self-integrity 固定点ゆえ monolith 残置必須。**

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 7 個目。今回は「公開情報の日付やダイジェストを自動同期する仕組みが壊れていないか確かめる 5 つの検査」をまとめて移した。ファイルを読むだけで書き換えないので公開情報の承認は不要。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 7 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 10 で 14,053→13,930）。
