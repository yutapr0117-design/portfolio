# check-repository-consistency-map.md

```
Last-Updated  : 2026-06-10
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — Stage 5-k CI hygiene fix; Check 55/56 added; Stage 5-c〜5-j で Check 47 モジュール数 14+ へ拡張)
Subject       : .github/scripts/check_repository_consistency.py（≈2,250 行・Check 1〜56）の構造地図
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/total-check-runbook.md / repository-maintainability-map.md
Status        : 本 increment で新設。物理分割はまだ行わない（本文書は分割の準備＝カテゴリ化と helper 識別）。
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルはそれらに従属するアーキテクチャ文書であり、矛盾時は上位を正とする。
> **本文書の目的:** `check_repository_consistency.py` は検証基盤の中核でありながら約 2,059 行へ肥大化している。将来この巨大スクリプトを安全に分割するための **準備地図** として、(1) Check 1〜54 を機能カテゴリへ分類し、(2) 共有ユーティリティ（helper）と抽出候補を識別し、(3) 分割の際に守るべき不変条件を明文化する。**本 increment では物理分割は行わない**（`改善文書.md` §5.4 の推奨順「いきなり分割しない → map を作る → その後 lib 抽出可否を判断」に従う）。

---

## 0. このスクリプトを「いきなり分割してはいけない」理由

`check_repository_consistency.py` は、このリポジトリの安全性の前提そのものである。AI が実装し人間が統制するという運用は、`npm run verify`（54 の BLOCKING/ADVISORY 整合チェック + lint + CSS lint + 構文チェック）が緑であることに全面的に依存している。ここを雑に分割すると、CI の信頼性が静かに崩れ、「壊れていないつもりで壊れている」状態を招く。したがって分割は、(a) まず本マップで全チェックの責務とカテゴリを把握し、(b) 共有 helper を識別し、(c) helper だけを `lib/` へ切り出せるかを Python import path・GitHub Actions・ローカル実行の三者で検証し、(d) 既存入口 `python3 .github/scripts/check_repository_consistency.py` を維持する、という順序を厳守する。

加えて、このスクリプト自身が **Check 45** によって自己整合を機械強制されている点に注意が要る。Check 45 は「docstring の番号付きインベントリ」と「コード本体の `# ── N.` セクション見出し」が 1..N で連続一致することを BLOCKING で検査する。したがって分割で個別チェックを別ファイルへ移すと、Check 45 の前提（インベントリと本体セクションが同一ファイル内で対応する）が変わる。分割を行うなら Check 45 の検査対象も同時に再設計する必要があり、これが「helper（番号を持たない補助関数）の抽出から始めるのが安全」である理由でもある——helper は Check 45 の番号体系の外にあるため、抽出しても 45 の前提を壊さない。

---

## 1. 共有ユーティリティ（helper）— 番号を持たない基盤関数

スクリプト冒頭に、全チェックが依拠する小さな helper 群がある。これらは Check 番号を持たず、`lib/` への最初の抽出候補である（Check 45 の番号体系の外にあるため、抽出が 45 の自己整合を壊さない）。

| helper | 役割 | 抽出容易性 |
|---|---|---|
| `check(condition, msg_ok, msg_fail, blocking=True)` | 全チェックの結果記録器。`errors`/`warnings` リストへ積み、`blocking` で BLOCKING/ADVISORY を分ける | 中（グローバル `errors`/`warnings` への副作用があるため、状態を引数化するか collector オブジェクト化が要る） |
| `read(path)` | テキストファイル読み取り（UTF-8） | 高（純関数に近い） |
| `read_bytes(path)` | バイナリ読み取り | 高 |
| `extract(pattern, text)` | 正規表現で最初のグループを取り出す | 高（純関数） |
| `_csp_sri_hash(content)` | CSP 用 SHA-256 ハッシュ計算（Check 7b/7c が依拠） | 高（純関数。`hashlib` のみ） |
| `_repo_member_paths()` | 追跡対象パスの列挙（Check 37 が依拠） | 中（ファイルシステム走査） |
| モジュール定数 `ROOT` | リポジトリルート（`Path(__file__).resolve().parents[2]`） | — （全チェックの基準点。`lib/` 化時は引数で渡す設計が要る） |

**抽出順の指針:** `read` / `read_bytes` / `extract` / `_csp_sri_hash` のような純関数を最初に `.github/scripts/lib/` へ切り出すのが最も安全である。`check()` は副作用（グローバルリストへの追記）を持つため、抽出するなら collector を明示的に渡す形へ設計変更が要る。`ROOT` は全チェックの基準点なので、分割時は各モジュールへ引数注入する。

---

## 2. Check 1〜54 の機能カテゴリ分類

54 のチェックを 6 つの機能カテゴリへ分類する。各カテゴリは、将来 `lib/` 分割を行う場合の自然なモジュール境界の候補でもある（例: `lib/version_checks.py` / `lib/aio_checks.py` …）。ただし前述の通り、本 increment では分割しない。

### カテゴリ A — バージョン整合（version sync）

ポートフォリオのバージョン番号が、HTML・JS・manifest・SW・sitemap の全所で一致していることを守る。version bump を atomic に行うための単一ソース整合の核。

| # | 検査内容（要約） | 級 |
|---|---|---|
| 1 | `ai:version`（index.html）== `Pipeline-Version`（AI2AI.md） | BLOCKING |
| 2 | `ai:version` == `SITE_CONFIG.VERSION`（main.js） | BLOCKING |
| 3 | `mcp.json` の `server.version` メジャー == `ai:version` | BLOCKING |
| 17 | `ai:last-modified`（index.html）== `SITE_CONFIG.LAST_UPDATED`（main.js） | BLOCKING |
| 18 | `sitemap.xml` root `<lastmod>` == `ai:last-modified` | BLOCKING |
| 19 | `sw.js` の `CACHE_NAME` バージョン == `ai:version` | BLOCKING |
| 21 | llms エイリアス各ファイルの `Last-Updated` 同期 | BLOCKING |

### カテゴリ B — AIO 正本層 invariants（AIO canon integrity）

`llms*` / `AI2AI.md` / JSON-LD / manifest / canary など、AIO 正本層の byte 同一性・構造妥当性・クロス整合を守る。AIO 戦略の機械可読な権威性を支える。

| # | 検査内容（要約） | 級 |
|---|---|---|
| 4 | llms 4 エイリアスが byte-identical | BLOCKING |
| 5 | `.well-known/index.json` == `agent-skills/index.json`（byte-identical） | BLOCKING |
| 11 | `aio_monitoring.py` summary に `enabled_engines` / `total_cited_count` | BLOCKING |
| 14 | v1→v74 canonical 宣言が index.html か AI2AI.md に存在 | BLOCKING |
| 15 | Project Pages の robots/.well-known 制約が文書化されている | BLOCKING |
| 22 | AI2AI.md の Session Record 見出しが昇順 | BLOCKING |
| 24 | llms-full.txt の `Last-Updated` が AI2AI.md の 7 日以内かつ v75-v78 floor 以上 | BLOCKING |
| 25 | `aio-monitoring-log.json` に `evidence_policy` キー（attempt_log_only honesty） | BLOCKING |
| 26 | `aio-manifest.json` の archive role #1-#N が AI2AI-archive.md の最大 Session Record と一致 | BLOCKING |
| 27 | llms-full.txt の現行制約文脈に stale な C1–C6 が無い（C1–C7 であるべき） | BLOCKING |
| 31 | `Claude2Claude.md` が AI2AI.md の現行最大 Session Record を参照 | BLOCKING |
| 32 | index.html の `application/ld+json` ブロックが妥当な JSON | BLOCKING |
| 33 | Zenn featuring 層が canonical な記事 slug 集合 + PRIMARY を共有 | BLOCKING |
| 44 | AIO provenance canary トークンの published 面と monitor 面のクロス整合（44a/44b/44c） | BLOCKING |
| 49 | index.html JSON-LD の `Person.worksFor` ↔ Organization linkage 整合（宙吊り防止） | BLOCKING |

### カテゴリ C — 配信・SEO・クローラ面（delivery / SEO / crawler surface）

sitemap・robots・CSP メタ・og メタ・GitHub Pages 配信制約など、公開面の妥当性を守る。

| # | 検査内容（要約） | 級 |
|---|---|---|
| 6 | `style.css` に stale な "Current release: v73" / "NEXT_PLANNED_RELEASE" マーカーが無い | BLOCKING |
| 7 | index.html の CSP メタが inline suppressor スクリプトより前にある | BLOCKING |
| 7b | index.html CSP が inline suppressor を hash で許可（live 内容から再計算） | BLOCKING |
| 7c | index.html CSP が inline speculation rules を hash で許可（live 内容から再計算） | BLOCKING |
| 8 | index.html に `<meta http-equiv="X-Content-Type-Options">` が無い（ヘッダ専用制御） | BLOCKING |
| 9 | `sitemap.xml` が妥当な XML | BLOCKING |
| 18 | （カテゴリ A と重複: sitemap root lastmod 整合） | BLOCKING |
| 20 | index.html に `og:image:width` / `:height` / `:alt` | BLOCKING |
| 34 | doc の `Last-Updated` がその sitemap `<lastmod>` と一致（honest dating） | WARNING |
| 35 | `robots.txt` が sitemap.xml へ解決する `Sitemap:` ディレクティブを宣言 | BLOCKING |
| 36 | `sitemap.xml` に未来日付の `<lastmod>` が無い | WARNING |
| 39 | 同一プロジェクトの sitemap `<loc>` がすべて commit 済みファイルへ解決（crawler 404 防止） | BLOCKING |
| 53 | index.html の全 `modulepreload` href がリポジトリ実体ファイルへ解決（dangling preload 404 防止） | BLOCKING |

### カテゴリ D — 歴史記述・honesty（historical-claim hygiene）

「72 回」「70 超」など、過去の主張・回数表現が現行記述に紛れ込まないことを守る。proof-of-work の事実性を保つ。

| # | 検査内容（要約） | 級 |
|---|---|---|
| 12 | 現行記述ファイルに stale な "72回/72回以上" が無い（履歴行は除外） | BLOCKING |
| 13 | "70超" が履歴/ログ文脈にのみ出現 | BLOCKING |

### カテゴリ E — 構造パース・CI 配線・ツール整合（structural parse / CI wiring / tooling）

JSON/YAML/XML/Python の構文妥当性、package.json ↔ lockfile、lint 配線、ESLint flat-config、Playwright 版数など、ビルドレス配信を支えるツールチェーンの整合を守る。

| # | 検査内容（要約） | 級 |
|---|---|---|
| 10 | `.github/scripts/*.py` がすべて構文エラーなくパース | BLOCKING |
| 23 | `.github/workflows/*.yml` と `dependabot.yml` が YAML 構文エラーなし | BLOCKING |
| 37 | 生成物/キャッシュ（node_modules / __pycache__ / *.pyc / test-results 等）が追跡されていない | BLOCKING |
| 38 | package.json ↔ package-lock.json 整合（lockfileVersion 3・名前・版・devDeps・private・runtime 依存ゼロ） | BLOCKING |
| 40 | CSS lint 実行経路の衛生（40a: devDeps に stylelint / 40b: check_css_stylelint.py が node_modules/.bin 参照 / 40c: npx を documented fallback に保持） | BLOCKING |
| 41 | AIO monitoring log ↔ manifest の atomic-commit 不変条件 | BLOCKING |
| 46 | package.json `lint`/`lint:js` が同一 JS ファイル集合を被覆し、ディスク上 root ∪ js/ と一致（46a/46b） | BLOCKING |
| 47 | main.js ⇄ js/ 各モジュールの ESM import/export bijection と葉性（47a/47b/47c・現行 14+ モジュール（Stage 5-c〜5-j で大幅増）をループ検査・named-list export 対応） | BLOCKING |
| 48 | `update-playwright-snapshots.yml` が PR 作成ステップを含む場合に `contents:write` + `pull-requests:write` を宣言（権限結合） | BLOCKING |
| 50 | ESLint flat-config 移行不変条件（50a: eslint.config.mjs 存在 / 50b: lint が旧 eslintrc フラグ非使用 / 50c: .eslintrc.json 不在） | BLOCKING |
| 51 | active runbook の Playwright baseline 生成版数が `@playwright/test` pin と一致 | BLOCKING |
| 54 | package.json の `eslint` と `@eslint/js` が同一メジャー（ESLint v10 系での解決衝突防止） | BLOCKING |
| 55 | architecture-validation.yml の lint 対象が package.json と整合（`shopt -s globstar` 有効化または `npm run lint(:js)` 利用 — Stage 5-j vacuous-gate 防止） | BLOCKING |
| 56 | js/ 葉モジュールの factory パターン引数被覆（factory export → main.js で createXxx 呼出を機械強制・Stage 5-j 隠れ ReferenceError class 防止） | BLOCKING |

### カテゴリ F — 自己統治・テスト健全性・保守ガバナンス（self-governance / test health / maintainability）

チェックスクリプト自身の自己整合、E2E テストの構造健全性、保守性アンカー文書の存在、肥大化予算など、リポジトリの自己統治機構を守る。

| # | 検査内容（要約） | 級 |
|---|---|---|
| 16 | `e2e/portfolio.spec.js` の screenshot テストに baseline-skip ガードがある | BLOCKING |
| 28 | `e2e/portfolio.spec.js` に `test()` のネストが無い | BLOCKING |
| 29 | Playwright baseline 生成リンク健全（snapshot workflow ↔ spec env signal） | BLOCKING |
| 30 | v80+ 保守性アンカー文書が存在（repository-maintainability-map / main-js-extraction-map） | BLOCKING |
| 42 | docs/ アーティファクト配置・命名衛生（42a: incident-artifacts 直下の命名規約 / 42b: decision・improvement-notes の配置） | BLOCKING |
| 43 | main.js AIDK Isolated Kernel の構造健全性（43a: ヘッダマーカー / 43b: startViewTransition proxy / 43c: Trusted Types default policy / 43d: 単一トップレベル IIFE） | BLOCKING |
| 45 | 本チェックファイルの docstring インベントリ ↔ コードセクション見出しの自己整合（45a/45b/45c） | BLOCKING |
| 52 | file-size budget advisory（BUDGET-DATA ブロックと現行行数の照合・main.js は strong-advisory） | **ADVISORY** |

---

## 3. 級別サマリ（BLOCKING / ADVISORY）

| 級 | チェック数 | 該当 |
|---|---:|---|
| BLOCKING（失敗で exit 1） | 53 | Check 52 を除く全カテゴリのチェック（Check 53/54/55/56 を含む。サブチェックを持つものは全サブが BLOCKING） |
| ADVISORY/WARNING（exit に影響しない） | 3 | Check 34（honest dating）・Check 36（future-dated lastmod）・Check 52（file-size budget） |

注: Check 34/36 は元から WARNING 級として設計されている（公開面の軽微な日付ずれを観測するが、ビルドを止めない）。Check 52 は quiz-domain-split + bloat-governance increment で追加した advisory（肥大化予算は CI を止めるべきでないため）。Check 53（modulepreload 解決）・Check 54（eslint↔@eslint/js メジャー一致）は console-fix increment で追加（ともに BLOCKING）。Check 55（CI lint-target 整合）・Check 56（factory-pattern 引数被覆）は v80+ Stage 5-k CI hygiene fix で追加（Stage 5-j 隠れバグ再発防止・ともに BLOCKING）。残るチェックはすべて BLOCKING である。

---

## 4. 将来の `lib/` 分割に向けた指針（本 increment では実行しない）

第一段階として、§1 の純 helper（`read` / `read_bytes` / `extract` / `_csp_sri_hash`）を `.github/scripts/lib/io_utils.py` のような単一モジュールへ切り出す案が最も安全である。これらは Check 番号を持たず副作用も小さいため、Check 45 の自己整合（番号体系）を壊さない。切り出し後は、(a) `python3 .github/scripts/check_repository_consistency.py` をローカルで実行して同一結果になること、(b) GitHub Actions の `architecture-validation.yml` でも同じ import path が解決すること、の両方を確認する。Python の import path は、スクリプトが `.github/scripts/` 配下で実行される前提に依存するため、`sys.path` への追加か相対 import の設計を慎重に行う。

第二段階以降として、カテゴリ単位（A〜F）でのチェック本体の分割が考えられるが、これは Check 45 の前提（docstring インベントリとコードセクションが同一ファイル内で対応する）の再設計を伴うため、helper 抽出が安定し、かつ Check 45 を「複数ファイルにまたがるインベントリ」に対応させる設計が固まってから着手する。本マップは、その判断のための地図である。**結論として、本 increment は分割を行わず、カテゴリ化と helper 識別という準備に止める。**
