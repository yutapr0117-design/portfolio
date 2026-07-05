---
file: .github/scripts/checks_app_route.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_app_route.py

## What

`check_repository_consistency.py` 分割トラックの 8 つ目の split module（1=maintainability / 2=structural / 3=esm / 4=tooling / 5=entity / 6=docs_mirror / 7=aio_derived）。SPA の app-route whitelist（`js/router.js` の `[...].includes(app)`）を single source of truth として全 producer/consumer の整合を強制する連続クラスタ Check **136-140** を内包し、`run(ctx)` で monolith から呼ばれる。

- **Check 136**: store.js demoRoute whitelist ↔ router app whitelist。
- **Check 137**: main.js の `case 'app-<app>'` render switch ↔ router app whitelist。
- **Check 138**: Sidebar app-nav ↔ router app whitelist coverage。
- **Check 139**: AppsPage app index ↔ router app whitelist coverage。
- **Check 140**: Settings demo selector options ↔ router app whitelist coverage。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 11**）。136-140 は「app-route whitelist coherence-mesh」という単一テーマの **連続 self-contained クラスタ**（handoff §5 の #288-#294 app-route mesh を機械強制する 5 Check）。各 Check は対象ファイル（`js/router.js` / `main.js` / `js/components.js` / `js/settings-page.js`）を自前で `read_text()` し、global content（html/style/mainjs）依存はない。全局所変数が `_NNN` 接尾辞で綺麗に namespace 化され section 内に閉じる（app-route mesh は一貫した命名規約で authoring された）。ctx enrich 不要で安全に一括抽出できた。

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、**元の実行位置（Check 135 の後・141 の前）**で `checks_app_route.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re`（json/warnings/read/extract は本クラスタ未使用）。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播が byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断し docstring inventory + `# ── N.` section を集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: 本 module の docstring inventory（`  136.`〜`  140.`）と `# ── N.` section は 1 対 1、monolith と合わせて 1..N 連番・map・runbook §9 と bijection。
- **クラスタの完全性**: 136-140 の局所変数を参照する Check は必ず本 module 内に置く。新しい app-route producer/consumer を Check 化する際も本 module へ（mesh の追加は同一 module 内で閉じる）。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- Check 追加/移動時は impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証）。
- monolith 行数: 13,930 → 13,711（−219・Phase 11）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `app-route`, `coherence-mesh`, `ctx-injection`, `phase11`
- **連続 self-contained クラスタ抽出**（aio_derived 91-95 と同型）。app-route mesh は `_NNN` 接尾辞が徹底され最も抽出しやすいクラスタだった。**教訓: 一貫した `_NNN` 命名のクラスタは変数リークのリスクが最小 — 命名規約が抽出安全性に直結する。**
- 残ターゲット候補: 133-135（shipped-asset wiring）/ 142-145（CI/workflow coverage・supply-chain）/ 116-117（playwright config）/ 128-131（behavioral guards）/ 104/106/107/109（CI/node config・105/108 除外）。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 8 個目。今回は「アプリ一覧(task/todo/pomodoro/ai/notes)がルーター・サイドバー・設定画面など全ての場所で一致しているか確かめる 5 つの検査」をまとめて移した。1 つでもズレると特定アプリが到達不能になるのを防ぐ mesh。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 8 split module 横断で緑を保ちながら、監査可能な小刻みステップで monolith を縮小している透明な記録（Phase 11 で 13,930→13,711）。
