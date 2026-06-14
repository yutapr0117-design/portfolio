# docs/files/ — 1-to-1 file documentation inventory

```
Last-Updated  : 2026-06-14
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — Docs 7 Phase 全完了 + Final audit で 137 ファイル 1-to-1 docs 完遂)
Subject       : リポジトリ内の全ファイルに対する 1 対 1 説明ドキュメントの inventory
Canonical-Ref : AI2AI.md (canon) / CLAUDE.md (router) / docs/architecture/repository-maintainability-map.md
Status        : Phase 1-6 + Final audit 完了。全 137 ファイル (元ファイル) に対し docs/files/<path>.md ミラー構造で 1 対 1 doc 完備。Check 96 で bijection を pre-commit 機械強制。
```

> **このディレクトリの目的:** リポジトリ内の **全ファイル** に対し、**1 対 1 の説明ドキュメント** を `docs/files/<repo-relative-path>.md` のミラー構造で配置する。対象読者は AI (LLM / クローラ / AI search / AI bot 全般) + 人間 (新卒エンジニアでも理解できるレベル) + 第三者 (監査人 / 採用担当 / 学術研究者) 等。例外なし。

---

## 1. 配置規約 (mirror structure)

| 元ファイル | 説明ドキュメント |
|---|---|
| `main.js` | `docs/files/main.js.md` |
| `js/state.js` | `docs/files/js/state.js.md` |
| `js/quiz/aws-quiz-data.js` | `docs/files/js/quiz/aws-quiz-data.js.md` |
| `index.html` | `docs/files/index.html.md` |
| `style.css` | `docs/files/style.css.md` |

path 対応が機械的に推論可能 = AI / 人間どちらにとっても予測可能。

---

## 2. ドキュメント template (5 軸 + frontmatter)

各 doc は以下の 5 セクション構成:

| セクション | 内容 | 規模目安 |
|---|---|---|
| **frontmatter** | `file:` / `audience:` / `last-updated:` / `canonical-ref:` | 5-7 行 |
| **What** | このファイルは何か (1-2 文) | 2-3 行 |
| **Why** | なぜ存在するか / 暗黙の前提 / 制約 / 歴史的経緯 | 5-15 行 |
| **How (usage)** | どう使われるか / 呼び出し関係 / entry point からの距離 | 5-15 行 |
| **Constraints** | このファイルへの制約 (C1-C7 番号 / 機械強制 Check 番号) | 3-10 行 |
| **Change impact** | 変更時の影響範囲 / 同時更新が必要なファイル | 3-10 行 |
| **Audience-specific notes** | AI 向け machine-readable metadata + 人間 (新卒) 向け平易解説 | 5-15 行 |

**書かないこと**: コードがどう動くか (= what the code does)。コードを読めば分かる内容は drift の原因。書くのは「why / when / where / impact」のみ。

---

## 3. 全 Phase の進捗

| Phase | 対象 | 件数 | 状態 |
|---|---|---|---|
| **Phase 1** | shipped code (main.js / js/*.js / index.html / style.css / sw.js / aio-guard.js / 等) | 33 | **完了** (PR #53) |
| **Phase 2** | AIO 正本層 + crawler 制御 (llms\*.txt 4 mirror / .well-known/\* 5 / robots / sitemap) | 11 | **完了** (PR #54) |
| **Phase 3** | config / scripts / workflows (.github/\* 15 + .claude 13 + root config 5 + e2e 1) | 25 | **完了** (PR #55) |
| **Phase 4** | binary assets (webp / mp3) | 2 | **完了** (PR #56) |
| **Phase 5** | dot files / meta config (.gitignore / .editorconfig / .nvmrc / .nojekyll / .mcp.json / .gitattributes) | 6 | **完了** (PR #56) |
| **Phase 6** | meta-docs (root docs 10 + docs/architecture 7 + docs/evidence 2 + docs/incident-artifacts 25 + docs/session-records 2 + docs/README) | 47 | **完了** (PR #56) |
| **Final audit** | grep 監査で発見した 4 漏れ (.well-known/api-catalog / jsconfig.json / docs/evidence/aio-monitoring-log.json / e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png) | 4 | **完了** (本 increment) |
| **Phase 7** | 機械強制 Check 96-99 (全 137 ファイル ↔ docs/files/ bijection を BLOCKING) | — | **完了** (Check 96 final 拡張) |

---

## 4. Phase 1 完了分: shipped code (33 件)

### Root shipped (9)
- [main.js](./main.js.md) — AIDK Isolated Kernel + factory composition (1,086 行)
- [index.html](./index.html.md) — single-page SPA entry + AIO/JSON-LD/CSP の宣言面
- [style.css](./style.css.md) — 全 CSS (2,156 行, baseline 後の section 分割候補)
- [sw.js](./sw.js.md) — Service Worker (offline cache 戦略)
- [aio-guard.js](./aio-guard.js.md) — AIO asset anchor 自己修復モニタ
- [error-suppressor.js](./error-suppressor.js.md) — global error/unhandledrejection 抑制 (inline)
- [karte-init.js](./karte-init.js.md) — KARTE タグ初期化 (vendor snippet)
- [theme-init.js](./theme-init.js.md) — テーマ早期適用 (FOUC 防止)
- [googlea7059bedc6fe8bdc.html](./googlea7059bedc6fe8bdc.html.md) — GSC verification token-only file

### js/ leaf modules (20)
全 24 葉モジュールの一覧は `docs/architecture/repository-maintainability-map.md` § "Stage 5-c〜5-s" 参照。各々の独立 doc は `docs/files/js/<name>.js.md` に配置。

- [js/aidk-rails.js](./js/aidk-rails.js.md) — AIDK Rail 5 IIFE 合体 factory
- [js/apps.js](./js/apps.js.md) — Productivity Apps 5 関数 factory
- [js/brand.js](./js/brand.js.md) — Brand manager factory
- [js/components.js](./js/components.js.md) — UI page components 11 関数 factory
- [js/constants.js](./js/constants.js.md) — 実行時定数
- [js/fatal-overlay.js](./js/fatal-overlay.js.md) — Fatal overlay + Global Safety Net
- [js/identity.js](./js/identity.js.md) — AUTHOR 純データ
- [js/meta-management.js](./js/meta-management.js.md) — Meta Management factory
- [js/mobile-drawer.js](./js/mobile-drawer.js.md) — Mobile Drawer factory
- [js/page-meta.js](./js/page-meta.js.md) — ページ SEO メタ単一ソース
- [js/pages.js](./js/pages.js.md) — Page components factory
- [js/perf-guards.js](./js/perf-guards.js.md) — Performance Guards factory
- [js/pure-utils.js](./js/pure-utils.js.md) — 純ユーティリティ
- [js/quiz-renderer.js](./js/quiz-renderer.js.md) — Quiz Renderer factory
- [js/router.js](./js/router.js.md) — Hash-based SPA ルーター
- [js/state.js](./js/state.js.md) — State factory (Proxy + subscriber + cross-tab + auto-save)
- [js/storage.js](./js/storage.js.md) — Safe localStorage ラッパ
- [js/store.js](./js/store.js.md) — Store factory
- [js/theme.js](./js/theme.js.md) — Theme factory
- [js/ui-components.js](./js/ui-components.js.md) — DOM ビルダー・SVG アイコン・Toast・BGM

### js/quiz/ static data (4)
- [js/quiz/architecture-quiz-data.js](./js/quiz/architecture-quiz-data.js.md)
- [js/quiz/aws-quiz-data.js](./js/quiz/aws-quiz-data.js.md)
- [js/quiz/pm-quiz-data.js](./js/quiz/pm-quiz-data.js.md)
- [js/quiz/quality-quiz-data.js](./js/quiz/quality-quiz-data.js.md)

---

## 5. 機械強制 (Phase 7 で完成予定)

Phase 7 で以下を BLOCKING Check として追加予定:

- **Check 96**: shipped code (Phase 1 対象 33 件) と `docs/files/` の bijection (set 一致)
- **Check 97**: 各 doc に必須 frontmatter (`file:` / `audience:` / `last-updated:`) 存在
- **Check 98**: 各 doc に必須 5 セクション見出し存在
- **Check 99-100**: Phase 2-6 対象も同様に bijection 強制 (各 Phase 完了時に追加)

本 increment では Phase 1 + Phase 7 骨格のみ。
