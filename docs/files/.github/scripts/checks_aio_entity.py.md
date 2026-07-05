---
file: .github/scripts/checks_aio_entity.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_aio_entity.py

## What

`check_repository_consistency.py` 分割トラックの 14 個目の split module。AIO manifest の entity フィールドと site の identity マーカーが canonical & coherent であることを保証する連続クラスタ Check **167-173** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 167**: aio-monitoring.yml weekly schedule presence。
- **Check 168**: aio-manifest entity.architecture C1/C2/C3 markers。
- **Check 169**: aio-manifest entity.role canonical markers。
- **Check 170**: aio-manifest entity.disambiguation negative-identity markers。
- **Check 171**: index.html ai:* meta URL canonical-prefix sharing。
- **Check 172**: aio-manifest entity name-variant coverage。
- **Check 173**: js/identity.js AUTHOR canonical values。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 17**）。167-173 は「AIO manifest entity-field & identity coherence」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（aio-manifest.json / index.html / js/identity.js / aio-monitoring.yml）を自前で `read_text()` し global content 依存はない。**annotation-aware free-variable 分析**（`_x: type = ...` 注釈付き定義も defined として認識する修正版）で外部 `_var` ゼロを確認してから抽出した — Phase 15 の初版 analyzer は型注釈付き定義（`_seen151: dict = {}`）を defined と認識できず false-positive を出していたため、AIO セクションが「coupled」に見えていたが、実際は self-contained だった。**NOTE: READ-ONLY coherence 検査ゆえ check *コード* の移動のみで AIO semantic を編集しない（C6 対象外）。**

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 166 の後・174 の前）**で `checks_aio_entity.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。annotation-aware free-var 分析で外部依存ゼロ確認済。
- **READ-ONLY**: AIO ファイルを読むが編集しない。C6 semantic 編集ではないため aio-guardian 承認は不要。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  167.`〜`  173.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 12,948 → 12,696（−252・Phase 17）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `aio-entity`, `manifest-coherence`, `aio-readonly`, `ctx-injection`, `phase17`
- **重要教訓（Phase 17）: free-var analyzer は型注釈付き定義（`_x: type = ...`）を defined として認識する必要がある。annotation を見落とすと self-contained なセクションを false-positive で「coupled」と誤判定する。`^\s*(name)\s*:` と `^\s*(name)\s*=` の両方を defined パターンに含めよ。** これにより 149-360 の AIO/SEO 大カテゴリの多くが実は self-contained（各セクションが型注釈付きローカルを使う）と判明。
- 残ターゲット候補（annotation-aware で clean 確認済）: 161-166（static-file resolution）/ 149-160（`glob=['html']`ゆえ ctx enrich 要）/ 125-126 / 104 / 106-107。genuine 結合が残るのは `_walkNNN` nested 関数（`def` 検出が必要）や `_glob237` 型の cross-section 共有ゆえ、大範囲抽出前に `def` 対応も足した analyzer で再確認せよ。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 14 個目。今回は「公開情報(AIO)の会社・役割・本人識別情報が正しく一貫しているか確かめる 7 つの検査」をまとめて移した。ファイルを読むだけで書き換えないので承認は不要。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 14 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 17 で 12,948→12,696）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
