---
file: .github/scripts/checks_behavioral.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_behavioral.py

## What

`check_repository_consistency.py` 分割トラックの 10 個目の split module（1=maintainability / 2=structural / 3=esm / 4=tooling / 5=entity / 6=docs_mirror / 7=aio_derived / 8=app_route / 9=ci_supply）。実バグから発見した shipped-JS の runtime UX invariant を静的強制する連続クラスタ Check **128-131** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 128**: Command palette ↔ router app-route coherence（cmdk NAV が router whitelist を被覆）。
- **Check 129**: Topbar data-action button double-fire guard（delegated ボタンに直接リスナーを付けない）。
- **Check 130**: Live-input oninput focus-loss guard（oninput ハンドラが `State.update` を呼ばない・brace-balance 解析）。
- **Check 131**: Service-worker decodeURIComponent guard（hot-path の decodeURIComponent が try/catch 内）。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 13**）。128-131 は「shipped-JS behavioral regression guard」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象 shipped-JS（`js/*.js` / `main.js` / `sw.js`）を自前で `read_text()` し、global content（html/style/mainjs）依存はない。Check 130 の brace-parser は汎用 scratch 局所変数（`_i`/`_j`/`_h`/`_depth`/`_nl` 等）を使うが、いずれも section 内で使用直前に再代入されるため relocate しても behavior-preserving（抽出前後で consistency check の全 364 出力行が Check 52 の行数表示以外 byte-identical であることを diff で実証）。ctx enrich 不要で安全に一括抽出できた。

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、**元の実行位置（Check 127 の後・132 の前）**で `checks_behavioral.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re`（json/ast/warnings/read/extract は本クラスタ未使用）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  128.`〜`  131.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **クラスタの完全性**: 128-131 の局所変数を参照する Check は必ず本 module 内に置く。新しい shipped-JS behavioral guard を Check 化する際も本 module へ寄せる候補。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 13,467 → 13,280（−187・Phase 13）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `behavioral`, `regression-guard`, `shipped-js`, `ctx-injection`, `phase13`
- **連続 self-contained クラスタ抽出**。**教訓（強力な検証手法）: 汎用 scratch 局所変数（`_i`/`_h` 等）を含むクラスタを抽出したら、抽出前後で consistency check の全出力行を `sort | diff` して byte-identical（Check 52 の行数表示のみ差分）を確認せよ — exit code だけでなく全 check 結果の不変を証明できる。**
- 残ターゲット候補: 132（AIO sitemap）/ 133-134（wiring・135 は style 依存で ctx enrich 要）/ 126-127（ESLint safety-net / AIO digest re-bake）/ 141+146（default-project integrity・非連続）/ 104/106/107/109（CI/node config・105/108 除外）/ ctx enrich が必要な html 系大カテゴリ。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 10 個目。今回は「過去の実バグ(二重発火/入力フォーカス喪失/日本語入力誤送信など)が再発しないか確かめる 4 つの検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 10 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 13 で 13,467→13,280）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
