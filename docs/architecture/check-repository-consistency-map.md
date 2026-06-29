# check-repository-consistency-map.md

```
Last-Updated  : 2026-06-16
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — 「Docs 7 Phase」全完了 + Final audit 漏れ 4 補完 で 全 137 ファイル 1-to-1 docs)
Subject       : .github/scripts/check_repository_consistency.py（≈4,000 行・全 Check）の構造地図（Check 総数の正値は total-check-runbook.md §9）
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/total-check-runbook.md / repository-maintainability-map.md
Status        : 本 increment で新設。物理分割はまだ行わない（本文書は分割の準備＝カテゴリ化と helper 識別）。
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルはそれらに従属するアーキテクチャ文書であり、矛盾時は上位を正とする。
> **本文書の目的:** `check_repository_consistency.py` は検証基盤の中核でありながら約 4,000 行へ肥大化している。将来この巨大スクリプトを安全に分割するための **準備地図** として、(1) 全 Check を機能カテゴリへ分類し、(2) 共有ユーティリティ（helper）と抽出候補を識別し、(3) 分割の際に守るべき不変条件を明文化する。**本 increment では物理分割は行わない**（`改善文書.md` §5.4 の推奨順「いきなり分割しない → map を作る → その後 lib 抽出可否を判断」に従う）。

---

## 0. このスクリプトを「いきなり分割してはいけない」理由

`check_repository_consistency.py` は、このリポジトリの安全性の前提そのものである。AI が実装し人間が統制するという運用は、`npm run verify`（全 BLOCKING/ADVISORY 整合チェック + lint + CSS lint + 構文チェック。総数の正値は total-check-runbook.md §9）が緑であることに全面的に依存している。ここを雑に分割すると、CI の信頼性が静かに崩れ、「壊れていないつもりで壊れている」状態を招く。したがって分割は、(a) まず本マップで全チェックの責務とカテゴリを把握し、(b) 共有 helper を識別し、(c) helper だけを `lib/` へ切り出せるかを Python import path・GitHub Actions・ローカル実行の三者で検証し、(d) 既存入口 `python3 .github/scripts/check_repository_consistency.py` を維持する、という順序を厳守する。

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

## 2. 全 Check の機能カテゴリ分類

全チェックを 6 つの機能カテゴリへ分類する。各カテゴリは、将来 `lib/` 分割を行う場合の自然なモジュール境界の候補でもある（例: `lib/version_checks.py` / `lib/aio_checks.py` …）。ただし前述の通り、本 increment では分割しない。

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
| 20 | index.html に `og:image:width` / `:height` / `:alt` | BLOCKING |
| 34 | doc の `Last-Updated` がその sitemap `<lastmod>` と一致（honest dating） | WARNING |
| 35 | `robots.txt` が sitemap.xml へ解決する `Sitemap:` ディレクティブを宣言 | BLOCKING |
| 36 | `sitemap.xml` に未来日付の `<lastmod>` が無い | WARNING |
| 39 | 同一プロジェクトの sitemap `<loc>` がすべて commit 済みファイルへ解決（crawler 404 防止）。さらに project `<loc>` が **1 件以上存在**することを強制（`_sm_checked > 0` ガード＝gutted/空 sitemap が「all 0 URLs resolve」で vacuous pass するのを防ぐ・AIO/SEO 中身消失検出） | BLOCKING |
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
| 47 | main.js ⇄ js/ 各モジュールの ESM import/export bijection と葉性（47a/47b/47c・現行 **24 モジュール**（Stage 5-c〜5-s + 5-l + 5-q + 5-r で最終完遂）をループ検査・named-list export 対応） | BLOCKING |
| 48 | `update-playwright-snapshots.yml` が PR 作成ステップを含む場合に `contents:write` + `pull-requests:write` を宣言（権限結合） | BLOCKING |
| 50 | ESLint flat-config 移行不変条件（50a: eslint.config.mjs 存在 / 50b: lint が旧 eslintrc フラグ非使用 / 50c: .eslintrc.json 不在） | BLOCKING |
| 51 | active runbook の Playwright baseline 生成版数が `@playwright/test` pin と一致 | BLOCKING |
| 54 | package.json の `eslint` と `@eslint/js` が同一メジャー（ESLint v10 系での解決衝突防止） | BLOCKING |
| 55 | architecture-validation.yml の lint 対象が package.json と整合（`shopt -s globstar` 有効化または `npm run lint(:js)` 利用 — Stage 5-j vacuous-gate 防止） | BLOCKING |
| 56 | js/ 葉モジュールの factory パターン引数被覆（factory export → main.js で createXxx 呼出を機械強制・Stage 5-j 隠れ ReferenceError class 防止） | BLOCKING |
| 57 | index.html modulepreload 集合 と `_modules47` 集合の完全一致（modulepreload 漏れ／余計 preload の双方向 drift 検出） | BLOCKING |
| 58 | e2e/portfolio.spec.js の ALL_ROUTES と main.js の switch case 集合一致（未訪問ルートに残る hidden runtime error class 防止） | BLOCKING |
| 59 | file-size-budget.md §2 表 と §4 BUDGET-DATA の集合一致（人間可読／機械可読のドキュメント drift 防止） | BLOCKING |
| 60 | ESLint warning baseline 回帰監視（file-size-budget.md の `<!-- ESLINT-BASELINE-DATA <N> -->` を真値に） | **ADVISORY** |
| 61 | 各 js/ 葉モジュールが factory pattern を export する場合、docstring に "factory pattern" マーカーを含む（抽出経緯のドキュメント drift 防止） | BLOCKING |
| 62 | aio-manifest.json `entity.canonical_url` と llms-full.txt の `Canonical URL:` 値完全一致（AIO entity identifier の cross-surface 整合性） | BLOCKING |
| 63 | robots.txt `Sitemap:` URL origin・aio-manifest entity origin・sitemap.xml 全 `<loc>` origin の完全同一化（crawler discovery alignment） | BLOCKING |
| 64 | check-repository-consistency-map.md Check 番号がカテゴリ間で一意（番号衝突 / Stage 5-l クラス防止） | BLOCKING |
| 65 | docs/architecture/*.md `Last-Updated:` + docs/files/*.md mirror `last-updated:` (YAML) 値が ISO-8601 `YYYY-MM-DD` 形式厳守（honest-dating 強化。143 ミラー全面へ scope 拡張・Check 97 が presence、本 Check が format を担う責務分離） | BLOCKING |
| 66 | index.html `<title>` に entity primary identifier（`yuta` または `横井`）を含む（AIO branding anchor） | BLOCKING |
| 67 | 全 .github/workflows/*.yml に top-level `permissions:` ブロック明示（CWE-275 防止 / security baseline） | BLOCKING |
| 68 | .github/dependabot.yml が `npm` + `github-actions` 両 ecosystem を update 対象に含む（月次更新の保証） | BLOCKING |
| 69 | package.json `engines.node` が CI workflow の `node-version` pin を許容（ローカル/CI 分裂防止） | BLOCKING |
| 70 | total-check-runbook.md §9 「consistency Check 総数」値が実装の最大 Check 番号と一致（cross-document 整合） | BLOCKING |
| 71 | file-size-budget.md §4 BUDGET-DATA の各 path が実在（Check 52 silent-skip 防止） | BLOCKING |
| 72 | file-size-budget.md ESLint baseline 値が sanity ceiling 200 以下（Plan A 絶対防衛線） | BLOCKING |
| 73a | index.html `<link rel="preload">` に `as=` 属性必須（preload 仕様準拠） | BLOCKING |
| 73b | index.html 全 `<img>` に `alt=` 属性必須（WCAG 1.1.1 Level A） | BLOCKING |
| 73c | hero image preload に `fetchpriority="high"`（LCP 契約） | BLOCKING |
| 74 | `.github/scripts/_lib_io.py` が 4 public 関数（read / read_bytes / extract / csp_sri_hash）を export | BLOCKING |
| 75 | docs/incident-artifacts/README.md が配下 artifact を全て列挙（inventory governance） | BLOCKING |
| 76 | .claude/settings.json が完全自走の安全境界 denies（AI2AI.md STEP 3「越えない安全境界」）を宣言: self-permission-widening 防止 `Edit/Write(.claude/settings.json)` / 破壊的操作 `git push --force`・`-f`・`rm -rf` / 全 stage 事故防止 `git add .`・`-A`・`--all` / C6 binary 保護 `*.webp`・`*.mp3`。とりわけ settings 自己編集 deny が消えると AI が自己権限拡張でき人間の制御境界が崩壊するため最重要 | BLOCKING |
| 77 | .claude/commands/*.md 全 slash-command に frontmatter + description | BLOCKING |
| 78 | .claude/agents/*.md 全 sub-agent に frontmatter + name + description、かつ `name` == ファイル名 stem（docs がファイル名で参照する agent を Claude が name で解決できる identifier-coherence。dangling reference 防止） | BLOCKING |
| 79 | .mcp.json が JSON parse 可能かつ mcpServers dict を含む（存在時 BLOCKING、不在 ADVISORY） | BLOCKING |
| 80 | .claude/skills/*/SKILL.md 全 skill に frontmatter + name + description、かつ `name` == 親ディレクトリ名（Check 78 と同型の identifier-coherence）（存在時 BLOCKING、不在 ADVISORY） | BLOCKING |
| 81 | WebP XMP に `aio:OrganizationName` / URL / Role / StartDate 4 field（binary AIO layer Organization 強制） | BLOCKING |
| 82 | MP3 ID3 に `AIO:Organization` / URL / Role / StartDate TXXX frame 4 件（binary AIO layer Organization 強制） | BLOCKING |
| 83 | aio-manifest.json `entity.affiliation` に 5 field（organization_name / url / named_position / role_name / start_date） | BLOCKING |
| 84 | README.md に Organization 名（`日本経営` または `Nihon Keiei`）を含む | BLOCKING |
| 85 | Claude2Claude.md 「現在状態」セクションに Organization handoff 記述 | BLOCKING |
| 86 | aio-manifest.json `entity` に 9 field (name/name_ja/name_alt/role/canonical_url/authoritative_context/disambiguation/architecture/affiliation) | BLOCKING |
| 87 | CLAUDE.md + Claude2Claude.md 両方に entity name + canonical URL + Organization 名 | BLOCKING |
| 88 | LICENSE に Copyright + entity name + canonical URL + Organization | BLOCKING |
| 89 | CONTRIBUTING.md + CODEOWNERS + CHANGELOG.md 3 ファイル存在 + entity name | BLOCKING |
| 90 | .claude/CLAUDE.md + .claude/README.md 両方に entity name + Organization 名 | BLOCKING |
| 91 | WebP XMP `ModifyDate`/`MetadataDate` + MP3 `AIO:MetadataLastModified` + manifest `last_metadata_update` の 4 日付フィールドが全て同一日 (C6 derived-value 同期契約) | BLOCKING |
| 92 | CLAUDE.md + AI2AI.md C6 文言に「derived-value auto-update」or「derived value」例外条項記載 | BLOCKING |
| 93 | aio-manifest.json top-level `last_metadata_update` が ISO-8601 で存在 (central anchor) | BLOCKING |
| 94 | `update_aio_digests.py` + `update_binary_aio_organization.py` が `_lib_io` 日付 helper を import (B1/B2 責務契約) | BLOCKING |
| 95 | `_lib_io.py` が `now_iso8601` / `update_webp_xmp_dates` / `update_mp3_metadata_date` の 3 helper を export (6 案 共通実装) | BLOCKING |
| 96 | Phase 1 shipped code 33 件が `docs/files/<path>.md` で 1 対 1 doc 化（Phase 7 骨格・新規追加時の漏れ防止） | BLOCKING |
| 97 | `docs/files/*.md` 各 doc に必須 frontmatter (file / audience / last-updated / canonical-ref)、かつ `file:` 値が mirror 自身の派生ソースパス (docs/files/<path>.md → <path>) と一致（copy-paste で `file:` を更新し忘れ「別ファイルを指す mirror」が通過する silent drift を防ぐ identifier-coherence。Check 78/80 と同型） | BLOCKING |
| 98 | `docs/files/*.md` 各 doc に必須 6 セクション見出し (What/Why/How/Constraints/Change impact/Audience-specific notes) | BLOCKING |
| 99 | `docs/files/README.md` (inventory) と `docs/files/_template.md` (template) が両方存在 | BLOCKING |
| 100 | theme-init.js ハードコード storage キー ↔ js/constants.js STORAGE_KEY / js/brand.js KEY 一致（100a/100b。FOUC 防止 pre-paint が main.js ESM ロード前に走るため import 不可ゆえの意図的複製・silent first-paint drift 防止） | BLOCKING |
| 101 | style.css に forced-colors (Windows HCM) の outline-based focus fallback 存在（HCM で box-shadow 非描画ゆえ box-shadow のみの focus 表示消失 = WCAG 2.4.7/1.4.1 違反を防止。render-neutral ゆえ §3 baseline ゲート非該当） | BLOCKING |
| 102 | 核心運用ポリシー（AI 自走全振り / 人間は制御・監査のみ）が canon に明記（102a: AI2AI.md STEP 3 Operating Model marker / 102b: CLAUDE.md §7 参照 / 102c: 「AI proposes, human disposes」献策ポリシー / 102d: 「No terminal "done" state」継続改善ポリシー＝AI の自発停止・完了宣言を禁止 / 102e: 「Infinite improvement＝改善は無限・完璧は存在しない」真理＝AI が「収束/枯渇」の自己判断を下すことを禁止・padding ガードは増分粒度のみ / 102f: 「reflect-then-organize」＝非自明増分前に簡潔な見解(pros/cons・レンズ確認)を出す品質ステップを AI2AI.md Operating Model + CLAUDE.md §5 に明記＝枯渇誤謬(102e)の打破。2026-06-21 に人間ゼロ入力で AI が 10 案自己生成→6 案自走可能と判明し実証）。核心ガバナンス契約の silent drift を防止 | BLOCKING |
| 103 | style.css に `@media (prefers-contrast: more)` 高コントラスト fallback 存在（WCAG 1.4.11 強化。render-neutral ゆえ §3 baseline ゲート非該当） | BLOCKING |
| 104 | npm から呼ばれる全 `.github/scripts/*.py`（package.json `scripts` から導出・hardcode せず）が `sys.version_info < (3, 10)` guard を持つ（PEP 604 `str \| None` 等の 3.10+ 構文を使うため、guard 無しでは Python 3.9 で cryptic な `TypeError` が import 時に出る。明示エラーで止める guard の silent 除去を防止＝AI-agnostic onboarding 保護） | BLOCKING |
| 105 | check-repository-consistency-map.md ↔ 実装の Check 番号 bijection（map の `\| N \|` 行が実装 `# ── N.` セクションと完全一致。alpha sub-check は整数に正規化）。Check 45（docstring↔section）の cross-document 版で、新 Check 追加時の map 行足し忘れ drift を構造的に防止 | BLOCKING |
| 106 | `.nvmrc`（ローカル dev 契約）の Node major が全 `.github/workflows/*.yml` の `node-version` pin と一致し、pin 同士も単一 major に揃う。Check 69（engines が pin を許容するか）を補完し、ローカルと CI の interpreter 分裂を防止 | BLOCKING |
| 107 | total-check-runbook.md §11「CI workflows overview」が全 `.github/workflows/*.yml`（backtick 引用の filename）を過不足なく列挙（doc ↔ ディスク bijection）。workflow 追加/削除時の索引 drift を防止。Check 75（incident README）/ 105（check-map）の CI workflow 面版 | BLOCKING |
| 108 | 全追跡ファイル（`git ls-files`・docs/files 自身除く）が `docs/files/<path>.md` の 1-to-1 ミラーを持ち、各ミラー（README.md inventory / _template.md 除く）が実 source を持つ（完全 bijection）。Check 96 は Phase-1 shipped-code 33 件のみ強制ゆえ、残り ~100 ミラーの欠落/orphan drift を本 Check が構造的に閉じる | BLOCKING |
| 109 | 現在状態を語る living 文書の全面（root CLAUDE.md / README.md / CHANGELOG.md / Claude2Claude.md / .claude/CLAUDE.md / .claude/README.md / .claude/agents/*.md / .claude/skills/*/SKILL.md / .claude/commands/*.md / runbook §9 以外 / 本 map）が、現在の Check タリーを prose にハードコードする drift（「総数」直書き / 「総数は _N_ まで成長」/ 「all _N_ Checks」/ 「consistency _N_ Check」/ 「Check count」直書き）を禁止。歴史層（per-increment changelog の maintainability-map / extraction-map・Session Record・improvement-notes・decision・docs/files ミラー）は point-in-time 記録ゆえ対象外。PR #68 が runbook/map を drift-proof 化した後も再発（PR #68 自身が §11 に新 stale 値を混入）したため機械強制化。正値は §9（Check 70 強制）を単一権威とし他所は §9 への pointer に置換 | BLOCKING |
| 110 | e2e の `A11Y_ROUTES`（axe a11y テストの対象）の hash 集合が `ALL_ROUTES`（route-render の網羅集合）の hash 集合と完全一致。新ルートを ALL_ROUTES に足したのに A11Y_ROUTES へ足し忘れる「a11y 未検証ルート」coverage gap を防ぐ（Check 58 の a11y 面版） | BLOCKING |
| 111 | e2e/portfolio.spec.js が `waitForLoadState('networkidle')` を screenshot regression テスト以外で使わない（許容は直後数行に `toHaveScreenshot` がある screenshot テストのみ）。networkidle は外部 Google Fonts / service worker SWR の background fetch で idle 到達せず CI で 30s ハングする flake クラス（PR #132 で root-fix）の再導入を防ぎ、behavior テストは `domcontentloaded` + expect auto-wait で同期させる | BLOCKING |
| 112 | Shipped-JS IME composition guard。112a（精密）=js/apps.js の全 Enter-submit ハンドラ（task/todo/ai 入力）が `e.key === 'Enter'` を判定する行に `Composing`（`!e.isComposing` または `!todoComposing`）を併記（task=PR #151 / ai=PR #152 で修正）。112b（一般網）=apps.js 以外も含む全 shipped JS module で `e.key === 'Enter'` を持つ file は同 file 内で IME ガード（isComposing/Composing）を参照する。日本語 IME 変換確定の Enter が未確定テキストの誤 submit や画面遷移を起こす footgun を全 shipped JS で構造封じ（拡張時に command-palette.js の未ガード Enter を発見・修正）。Enter ハンドラ 0 個は vacuous-gate として fail | BLOCKING |
| 113 | model-agnostic 正典 AI2AI.md（STEP 5.5）と Claude router CLAUDE.md（§5）の**双方**が handoff-first commit/PR 規律（テーマ束ね PR ×`gh pr merge --rebase` ×commit 数は OUTPUT）をマーカー（rebase + no-padding 条項）で保持。オーナーがリポジトリ核として正式採用したルールが、どちらかの canon から silent に消えて squash/粗 commit へ退行するのを防ぐ | BLOCKING |
| 114 | e2e/portfolio.spec.js に `test.only` / `describe.only` が無い。`.only` が残ると Playwright がその 1 件のみ実行し他を全 skip → CI が緑のまま suite 空洞化（false-green footgun = vacuous-gate の裏返し）。デバッグ用 `.only` の commit 漏れを禁止 | BLOCKING |
| 115 | index.html CSP meta が hardening baseline を維持: `script-src` 等に `'unsafe-inline'`/`'unsafe-eval'` が無く（inline は sha256 hash + `'unsafe-hashes'` で許可）、`default-src 'self'` / `object-src 'none'` / `base-uri 'self'` が存在。CSP 弱体化（XSS 防御無効化）の高影響セキュリティ退行を防ぐ（Check 7 の position/hash に対する runtime-policy 面） | BLOCKING |
| 116 | playwright.config.cjs の `reuseExistingServer` が `false`（`: true` 不在）。true だと既存 dev server を再利用し commit 前の stale 状態を検証 → CI が false-green 化する vector を防ぐ | BLOCKING |
| 117 | playwright.config.cjs の `toHaveScreenshot.maxDiffPixelRatio` が sanity ceiling 0.05 以下。§3 baseline ゲートの許容を silent に緩めて本物の視覚 regression を見逃す退行を防ぐ | BLOCKING |
| 118 | 全 shipped route（e2e ALL_ROUTES の name を正規化＝Check 58 が main.js と結ぶ権威）が js/page-meta.js の PAGE_META に metadata を持つ（PAGE_META keys ⊇ routes）。route が PAGE_META に無いと applyMeta が early-return し title/desc/JSON-LD が出ない silent AIO/SEO gap を防ぐ（PAGE_META↔ALL_ROUTES↔main.js coherence 三角形を閉じる） | BLOCKING |
| 119 | 各葉 factory `createX({ ...deps })` が署名で受け取る全依存名が、同ファイル冒頭 docstring の【依存（引数で注入）】節に列挙されている（word-boundary 照合）。Session #20 で手修正した factory docstring 依存 drift（aidk-rails/apps/components/pages が注入依存を docstring から欠落）の class を再発防止。docstring は次 AI の onboarding substrate（低 onboarding コスト＝トークン持続性の柱）で、署名↔docstring 乖離は誤った依存契約を読ませる onboarding 税＝flywheel 劣化要因 | BLOCKING |
| 120 | shipped JS+CSS の byte-weight 合計（main.js + js/**/*.js + style.css）が file-size-budget.md の PERF-BUDGET-DATA ceiling 以下。§3(B) で pixel screenshot を advisory 化し page-weight 保護が薄くなったのを byte-weight 軸で補う（行数予算 Check 52 とは別軸 byte≠line）。runaway bloat（巨大ファイル誤コミット等）= download/parse 負荷（LCP/CWV）増を BLOCKING 捕捉。正当成長は rationale 付きラチェット | BLOCKING |
| 121 | owner-facing STATUS.md（スマホ用 BLUF・「オーナーが repo を見ない」gap を埋める）が generate_status.py で authoritative ソースから機械生成された内容と byte 一致（regenerate-compare・AIO digest と同思想）。hand-edit/stale な dashboard = 誤情報＝flywheel 劣化を防ぐ。修正は `npm run status` | BLOCKING |
| 122 | private source document（office/文書/アーカイブ形式 = pdf/docx/doc/xlsx/pptx/rtf/odt/ods/odp/pages/key/numbers/csv + zip/7z/rar/tar/gz/tgz）が一切 tracked されない（`git ls-files` 権威・画像 png/jpg/webp は正規利用ゆえ対象外）。本人の経歴書類原本は抽象化済み docs/evidence/real-work-claims.md 生成のためのローカル入力に過ぎず、commit すると機微 PII（実名以外の個人特定情報・顧客/案件名・年収・労働条件）漏洩になる。.gitignore のブランケット ignore と二重防御で、明示 add の取りこぼし・将来の再投入を BLOCKING 捕捉 | BLOCKING |
| 123 | 運用モデル記述の coherence（site↔AIO）。123a=js/components.js が現運用モデル marker（現在の運用モデル + Claude Code + 自走）を保持、123b=llms-full.txt が（Current Operating Model + Claude Code + self-driving）を保持。Session #21 で是正した「対話型 Claude」drift が公開 surface で旧記述へ巻き戻るのを防ぐ（canon は 102a-f が別途強制・本 Check はその公開 surface 版） | BLOCKING |
| 124 | site 視覚テキストの匿名性ガード。124a=視覚 page renderer（js/components.js / pages.js / apps.js）で実名「横井雄太」が属性 context（alt/data-entity/data-ai-entity/aria-）以外の bare な h() テキスト行に出ない。124b=同 renderer が実名系 entity 定数（AUTHORITATIVE_NAME/JAPANESE_NAME）を参照しない（js/identity.js の「UI→DISPLAY_NAME only」契約を機械強制し識別子経由の漏れ path を封じる）。サイト UI は一般向けに「yuta」へ匿名化し実名は AIO/entity 層（sr-only/JSON-LD/meta/属性/llms-full・meta-management の AUTHORITATIVE_NAME 等）のみ、という二層を保つ（Session #21 で AI が視覚本文へ実名漏れ→即是正した class を構造封じ） | BLOCKING |
| 125 | dead-constant guard。js/constants.js の各キー（top-level + nested `[A-Z_]+:`）が他 shipped JS から最低 1 回参照される。Session #21 で除去した never-activated 定数（POMODORO_LOCK_TTL/SAVE_INTERVAL）class の再蓄積を防ぐ。ALL-CAPS snake ゆえ参照 grep は誤マッチしにくく、コメント言及も "not dead" 扱い（保守的 under-flag） | BLOCKING |
| 126 | ESLint bug-catcher safety-net presence。eslint.config.mjs が recommended pure bug-catcher の代表 safety-net 集合（no-import-assign/no-unsafe-finally/no-invalid-regexp/no-const-assign/valid-typeof/use-isnan/no-fallthrough/no-cond-assign/getter-return 等）を保持する。recommended 非継承方針ゆえ bug-catcher の silent 欠落が実バグを CI に素通させる #186 class（no-dupe-keys 欠落で quiz バグ流出）を、Check 50d の単体保護に加え安全網全体で構造封じ | BLOCKING |
| 127 | AIO digest tool binary re-bake guard。update_aio_digests.py が WebP/MP3 の内部日付メタ（XMP/ID3）再書き込みを `_binary_edited()`（`git diff --quiet HEAD -- <path>` による実編集判定）でガードすることを presence で強制。旧実装は binary entry の存在だけで毎回発火し、無関係なテキスト digest（週次 aio-monitoring ログ）更新のたびに binary hash を変えて manifest に記録する一方ワークフローは書き換えた binary を git add しないため commit 境界で manifest↔binary が毎週 desync し次 PR の BLOCKING digest gate を赤化させていた class（f2335ce 根治）を構造封じ | BLOCKING |
| 128 | Command palette ↔ router app-route coherence。command-palette（js/command-palette.js）の NAV が router（js/router.js）の route 可能な全 built-in app（`apps/<app>` whitelist=task/todo/pomodoro/ai/notes）に対応する `hash: 'apps/<app>'` destination を持つことを強制。router の app whitelist を source of truth に parse し、router に app を足して palette を更新し忘れ Cmd/Ctrl+K から到達不能になる drift（Markdown notes app が本 Check 追加まで欠落）を構造封じ | BLOCKING |
| 129 | Topbar data-action button double-fire guard。topbar の menuBtn/themeBtnTop/bgm-btn-top は data-action を持ち AIDK ActionDelegator が単一 delegated click で処理するため、main.js init がこれらに直接 `addEventListener('click')` を付けないことを presence-negative で強制。両方付けると 1 クリックで二重発火し theme 2 段送り / drawer 二重 open による scroll 先頭ジャンプ / BGM 二重 toggle になる実バグだった。ActionDelegator 単一経路契約を守る | BLOCKING |
| 130 | Live-input oninput focus-loss guard。shipped JS の `oninput:` ハンドラ本体を brace-balance で抽出し `State.update(` を呼ばないことを強制（`State.updateSilently(` は許可）。State.update→notify→render() の全再描画が #content を clear し focused input を毎キーストローク破棄する focus-loss class（quiz 検索 / Markdown notes 使用不能の実バグ）を、per-input e2e に加え全 oninput で構造封じ。高頻度 live-input は updateSilently + sub-DOM 手動更新 | BLOCKING |
| 131 | Service-worker decodeURIComponent guard。sw.js は全 fetch を intercept し各 pathname を normalizePath→decodeURIComponent に通すため、不正な % エスケープ URL（`/portfolio/%`）で URIError を throw すると SW fetch ハンドラが uncaught error になる。normalizePath が decodeURIComponent を try/catch でガードすることを brace-balance + presence で強制。SW は e2e 困難ゆえ e2e/Check ガードが無かった修正の回帰ガード | BLOCKING |
| 132 | AIO evidence ↔ sitemap discoverability。aio-manifest.json に authoritative evidence として登録された text doc（.md/.txt/.json）が sitemap.xml の `<loc>` にも掲載されることを強制。manifest は doc を権威宣言するが sitemap 未掲載だと sitemap 経由の crawler が到達できない silent discoverability gap（real-work-claims.md / AI2AI-archive.md が登録済なのに sitemap 欠落だった）を構造封じ。binary（.webp/.mp3）は除外 | BLOCKING |
| 133 | AIO guard script wiring。aio-guard.js（AIO asset-anchor の lifecycle monitor & self-repair）が index.html から `<script src="./aio-guard.js">` で実際に load されることを強制。mirror-bijection は FILE 存在しか見ないため script タグを消すと file は残り verify 緑のまま monitor だけが silent 無効化される（従来は非ブロック CI advisory のみ捕捉）。「guard file 存在 ⟹ guard 配線済」を invariant 化し AIO self-repair monitor の回帰を構造封じ | BLOCKING |
| 134 | Root script wiring completeness。index.html が依存する root script（theme-init.js / karte-init.js / main.js）を `<script src>` で load し続けることを強制。Check 133 と同様 mirror-bijection は FILE 存在しか見ず、タグ除去は silent に劣化する（theme-init.js=FOUC 防止・screenshot advisory ゆえ e2e 非捕捉 / karte-init.js=analytics 無音停止 / main.js=SPA entry）。error-suppressor.js は inline ゆえ Check 7/7b、aio-guard.js は Check 133 が担当。「root script 存在 ⟹ 配線済」を残る外部 root script へ invariant 化 | BLOCKING |
| 135 | Stylesheet wiring。index.html がローカル stylesheet style.css を `<link rel="stylesheet" href="./style.css">` で load し続けることを強制。Check 133/134 と同 class で最も影響大 — link 除去でサイト全体が未スタイル化するが behavior e2e は content presence しか見ず screenshot は §3(B) advisory ゆえ silent。style.css 存在（Check 108）と byte 予算（Check 52/120）は強制済だが `<link>` 配線は未被覆だった。外部 font stylesheet は graceful degradation ゆえ対象外。「style.css 存在 ⟹ link 済」を invariant 化 | BLOCKING |
| 136 | demoRoute ↔ router app whitelist coherence。store.js normalizeProject の demoRoute whitelist が router.js の `[...].includes(app)` app whitelist と集合一致することを強制。router に app が増えた（A 群 notes 追加）のに store 側が未更新だと、その app を demoRoute に持つプロジェクトを import した際に silent に null 化しデモボタンが消える（Check 128 / #139 と同じ data-fidelity loss）。両配列を parse し「router が app X をサポート ⟹ X は有効な demoRoute」を invariant 化 | BLOCKING |
| 137 | router app whitelist ↔ main.js render switch coherence。router.js が `apps/<app>` を route.name `app-<app>` に解決する whitelist と、main.js renderer switch の `case 'app-<app>':` 集合が bijection であることを強制。Check 128(cmdk)/136(store) は router whitelist の「提供側」を縛るが「消費側」の main.js switch は ALL_ROUTES 経由(Check 58)でしか間接的に縛られず、router+cmdk+store だけ更新して main.js/ALL_ROUTES を忘れると全 Check 緑のまま apps/<app> が silent に 404 化する gap を直接 edge で封じる。「router が app X を route 可能 ⟹ main.js が app X を描画可能」を invariant 化（app-route coherence mesh の欠落 edge） | BLOCKING |
| 138 | Sidebar app-nav ↔ router app whitelist coverage。Sidebar(js/components.js) の lab-nav が `path: 'apps/<app>'` で列挙する built-in app quick-nav が router whitelist の全 app を被覆することを強制。command palette(Check 128) と同 class — A 群で Markdown notes app を追加した際 AppsPage と palette(#257) には足したが sidebar には足し忘れ、notes だけが常設左ナビから到達不能だった実 UX バグを修正し再発を構造封じ。「router が app X を route 可能 ⟹ X は sidebar nav にある」を invariant 化（Check 128 の sidebar 版） | BLOCKING |
| 139 | AppsPage app index ↔ router app whitelist coverage。canonical「アプリ一覧」index である AppsPage(js/components.js) の `const apps = [...]` 配列(`id: '<app>'`)が router whitelist の全 app を被覆することを強制。palette(128)/sidebar(138) と並ぶ 3 つ目の app-route producer だが唯一未強制だった。AppsPage が drift すると、その app は他で route 可能なのに canonical index から発見不能になる。3 producer 面(palette/sidebar/AppsPage)を全て router whitelist に追従させ app-route coherence mesh を閉じる | BLOCKING |
| 140 | Settings demo selector ↔ router app whitelist coverage。Settings の手動追加フォーム(js/apps.js SettingsPage)の Demo `<select>`(onchange が settingsNewDemo を書き込む)の非空 `value: '<app>'` オプションが router whitelist と集合一致することを強制。これは「手動作成プロジェクトが demoRoute に持てる app」を決める WRITE 面で、store(Check 136)/router/main.js/cmdk/sidebar/AppsPage に新 app を足してもここを忘れると、その app は demo として silent に選択不能になる(notes が #257/#292/#293 で忘れられたのと同一再発クラス)。空の「Demoなし」option は許可。全 routable app をプロジェクト demo として選択可能に保つ | BLOCKING |
| 141 | Default-project slug & id uniqueness。store.js の defaultProjects(`proj("pNN","slug",…)` seed)の id 集合と slug 集合がともに衝突無しであることを強制。ProjectDetailPage は `find(p.slug===slug)` で先頭のみ返すため重複 slug は後者の詳細ページを silent に到達不能化する(#154 class)。user-added は addProjectManual が runtime で slug-suffix dedup するが hardcoded defaults は無保護で、将来のデータ編集で重複を入れると silently-unreachable なプロジェクトを出荷してしまう gap を機械封じ | BLOCKING |
| 142 | Playwright e2e gate covers its own toolchain。playwright-regression.yml(BLOCKING behavior e2e gate)の pull_request paths filter に package.json + package-lock.json が含まれることを強制。e2e ツールチェーン(@playwright/test runner / @axe-core/playwright a11y + transitive deps)は manifest にあり、その bump は shipped-site ファイルを変えずに e2e 挙動を変えうるが、trigger に manifest が無いと dep bump 時に behavior gate が skip され未検証で出荷される(実例 PR #318)。file-exists≠file-wired class の CI-trigger 版(cf. Check 133/134/135) | BLOCKING |
| 143 | Auto-digest workflow covers every digested manifest file。.well-known/aio-manifest.json が sha256 付きで登録する全 evidence file(source_of_truth/supporting_evidence/observational_evidence の repo-relative path)が auto-update-aio-digests.yml の push paths に literal か `prefix/**` glob で被覆されることを強制。digested file が paths に無いと main 上で編集しても digest が自動再生成されない producer/consumer drift(実例: real-work-claims.md が Session #21 で manifest 追加されたが workflow paths 未追加)。file-exists≠file-wired class(cf. Check 132/142) | BLOCKING |
| 144 | Digest-regen tool's file map matches the manifest。update_aio_digests.py の MANIFEST_PATH_TO_LOCAL dict(digest 再生成 tool が refresh できる file 集合の正本)の key 集合が manifest の digested-path 集合と bijection であることを強制。143 が workflow の発火を保証する一方、発火後 tool が refresh できるのは本 dict の file のみ。manifest entry に sha256 があり dict key が無いと該当 digest が再計算されず BLOCKING check_aio_digests.py が auto-fix 不能になる。digest-automation chain(paths→tool-dict→manifest)の consumer 側エッジ(cf. Check 143) | BLOCKING |
| 145 | GitHub Actions are pinned to a full commit SHA。.github/workflows/*.yml の全 `uses: owner/repo@ref` の ref が 40-hex commit SHA に pin されている(mutable tag @v6 / branch @main なし)ことを強制。版数タグは可変で上流の tag 移動・侵害で repo を変えずに別コードが実行されうる supply-chain risk を封じる(第三者 action が最大 attack surface)。local `./` action は exempt。`# vN` コメントは残り dependabot(Check 68)が pin を最新化。Check 67/76/115 と同 security-baseline の supply-chain 版 | BLOCKING |
| 146 | Default projects' relatedProjectIds are referentially intact。defaultProjects(store.js)の各エントリの relatedProjectIds に列挙される全 id が実在 default project id を参照することを強制。dangling 参照は SILENT — 関連プロジェクト UI が autoRelatedCandidates(類似度 fallback)で欠落を埋め section は populated に見えるため curator の明示的関連付けが無症状で失われる(graceful-fallback が bug を masking する class)。project-id 集合と relatedProjectIds 配列内 pNN 参照を収集し dangling 0 かつ参照>0(非 vacuous)を検証。Check 141(uniqueness)の兄弟で referential integrity を守る | BLOCKING |
| 147 | Speakable cssSelector tokens point to live shipped elements。js/meta-management.js の SPEAKABLE_SELECTORS (JSON-LD SpeakableSpecification の route ごとの AIO 配線) の各 selector が指す #id / .class token が、shipped DOM 面 (index.html ∪ js/*.js ∪ main.js のうち meta-management.js 自身を除く) に literal で実在することを強制。dangling は SILENT (SpeakableSpec は配信されるが voice assistant が node を見つけられず抽出空振り＝console error なし・behavior e2e 非検出の AIO 精度劣化)。同ファイル L152-156 [FIX] コメントが過去の手動修正履歴(.hero-tagline/.core-thesis 除去/.role-split-table→#role-split-table)を残す demonstrated bug-class だが未 systematize だった。配列リテラル内文字列のみを抽出 (route 名 key を取り込まない)、generic catch-all (h1 / [data-speakable] / .sr-only / .sr-only[data-ai-entity] と属性のみセレクタ) を exempt、非 generic 0 件なら vacuous-fail。dead selector の class を構造封じ | BLOCKING |
| 148 | SITE_CONFIG.ARTICLE_ROUTES ⊆ PAGE_META keys (Article JSON-LD route coherence)。main.js SITE_CONFIG.ARTICLE_ROUTES の全 route 名が js/page-meta.js の PAGE_META top-level keys に存在することを強制。dangling は SILENT — applyMeta が早期 return し fullTitle/desc が空のまま、injectStructuredData は (PAGE_META を参照せず) Article JSON-LD を空 headline/description で注入する不整合 AIO surface (console error 無し・behavior e2e 非検出)。Check 147 (dangling Speakable selector) と同 AIO 配線軸の兄弟で、Article 注入 route が必ず PAGE_META 由来 metadata を持つことを保証。ARTICLE_ROUTES が空 / 抽出不可 / PAGE_META が空 / dangling >0 なら fail | BLOCKING |
| 149 | Canonical URL three-way coherence。canonical URL の 3 declaration surface (index.html `<link rel=canonical>` href / aio-manifest.json entity.canonical_url / main.js SITE_CONFIG.CANONICAL_URL) が byte-identical であることを強制。drift は SILENT に AIO entity identity を破壊 — AI crawler が複数 canonical signal を見て entity を一つの URL に anchor できず AIO surface 全体が崩れる。Check 62 (manifest ↔ llms-full.txt) が既存ゆえ残る 2 edge (link[rel=canonical] と SITE_CONFIG) を本 Check が固定し canonical 配線を triangle で閉じる。trailing slash / origin も完全一致必須 | BLOCKING |
| 150 | og:url ↔ canonical URL coherence。index.html `<meta property=og:url>` content と `<link rel=canonical>` href が byte-identical であることを強制。drift は SILENT — OG/social card preview (LinkedIn/Slack unfurl/Twitter/Discord) が canonical link と別 URL を提示し AI/social crawler の entity 識別に drift。Check 149 の canonical-URL invariant を最も外部 mention の多い OG surface に拡張 (149 が internal 3 surface・150 が external 1 surface)。og:url か canonical が抽出不可 / drift なら fail | BLOCKING |
| 151 | e2e test() title uniqueness。e2e/portfolio.spec.js の全 `test('...')` title が一意であることを強制。重複 title は Playwright reporter で silent 上書き / 同名混在で結果区別不能になり vacuous-test-pair を生む (片方の fail が他方の pass で masked / 期待の出処不明)。test() 直接呼び出しのみ対象 (.skip/.fixme/.describe は対象外)。e2e 空 / 重複 >0 で fail。Check 111/114 と同じ test-health 軸 (vacuous-gate 防止) の補強 | BLOCKING |
| 152 | `<html lang>` ↔ JSON-LD inLanguage coherence。index.html の `<html lang>` 属性と全 JSON-LD `"inLanguage"` 宣言 (index.html ∪ main.js ∪ js/meta-management.js) が同一の言語コードであることを強制。drift は SILENT — AI/SEO crawler が conflicting な言語 signal を見て primary language を誤分類し、言語スコープ検索 (Google site: lang filter / AI search) と AIO で discovery が劣化する。全 surface から値を集めて単一集合の cardinality 1 を検証 (canonical 言語が一つに保たれる)。<html lang> 抽出不可 / inLanguage 0 件 / 集合サイズ ≠ 1 で fail | BLOCKING |
| 153 | og:image / twitter:image origin uses canonical URL prefix。index.html の `<meta property=og:image>` と `<meta name=twitter:image>` content URL が `<link rel=canonical>` href を prefix として持つことを強制。drift は SILENT — social/OG card preview が別 origin の image を提示し entity-asset coupling を破壊・stale や third-party image を見せうる。Check 149/150 の canonical-URL invariant を image surface (OG/Twitter card の視覚部分) に拡張。両 meta 必須・片方でも canonical prefix から外れたら fail | BLOCKING |
| 154 | description 3-way presence + og/twitter coherence。index.html の og:description と twitter:description が byte-identical (card preview 同尺)、`<meta name=description>` も presence 必須。drift は SILENT — LinkedIn/Slack 等 OG consumer と Twitter 等 twitter: consumer が同じ page を別 card text で見せ entity narrative が split する。`<meta name=description>` は SERP/AI crawler 向けに intentionally 長文ゆえ og/twitter と一致は強制しない (presence のみ vacuous-guard)。3 meta のいずれか欠落 / og≠twitter なら fail | BLOCKING |
| 155 | og:title ↔ twitter:title byte-identical。index.html の og:title と twitter:title content が byte-identical であることを強制 (card preview 同尺 title)。drift は SILENT — LinkedIn/Slack OG consumer と Twitter で別 headline を見せ entity の見え方が split する。Check 154 (description coherence) の title 軸兄弟。`<title>` tag は SERP vs card で intentionally 異なる尺ゆえ scope 外で og/twitter pair のみ強制。両 meta 必須・drift で fail | BLOCKING |
| 156 | og:type valid enumeration + og:site_name presence。index.html の og:type が valid OG type enumeration ('website' or 'article'・meta-management.js dynamic injection / SITE_CONFIG.ARTICLE_ROUTES で扱う唯一の type 集合) であり、og:site_name meta が presence + 非空 であることを強制。og:site_name 欠落 = card preview から site 識別子が消える / og:type invalid = article-vs-page 区別が失われ social crawler が generic fallback。presence + enumeration sanity の二段。Check 148 (ARTICLE_ROUTES) の dynamic 注入軸を補完する static surface 検証 | BLOCKING |
| 157 | Mobile / PWA baseline meta presence。index.html の `<head>` に非交渉 baseline meta 5 件すべて存在 (`<meta charset>` / `<meta name=viewport>` / `<meta name=theme-color>` / `<link rel=icon>` / `<link rel=apple-touch-icon>`) を強制。silent 削除で behavior e2e にほぼ非検出のまま劣化する: viewport=モバイルズーム破綻 / icon=タブ globe / apple-touch-icon=iOS ホーム追加が screenshot / theme-color=アドレスバー default / charset=文字化けリスク。presence-only (内容 scope 外) の vacuous-removal guard | BLOCKING |
| 158 | Google Fonts preconnect / dns-prefetch presence (CWV first-paint guard)。index.html が Google Fonts への preconnect 2 件 (fonts.googleapis.com + fonts.gstatic.com) + dns-prefetch 1 件 (fonts.googleapis.com) を保持することを強制。silent 除去は LCP/FCP を ~100-200ms 劣化させる (DNS+TLS+handshake 分) が、console error も behavior-test signal も出ず、後で bisect しづらい (壊れていない・ただ遅い)。3 marker いずれか欠落で fail | BLOCKING |
| 159 | JSON-LD `@context` cross-surface coherence。全 JSON-LD `@context` 値 (index.html 静的 ∪ main.js 動的 ∪ js/meta-management.js 動的) が canonical 値 'https://schema.org' 単一に揃うことを強制。drift (trailing slash / http: / 別 vocabulary URL) は SILENT — JSON 自体は parse できるが AI/SEO crawler が schema vocabulary を recognize できず structured-data signal 全体が unknown 扱いで崩壊する。全 surface から値を抽出し set cardinality 1 + 期待値一致を検証。0 件 / drift で fail | BLOCKING |
| 160 | sw.js hardcoded paths share the canonical URL pathname。sw.js の hardcode する `/<segment>/...` 形式の絶対パス (AIO_FILES 等) が、index.html `<link rel=canonical>` href の pathname と同じ first segment を使うことを強制。drift は SILENT — GitHub Pages の project rename / canonical URL の path 変更で SW は登録され続けるが hardcoded paths が incoming request URL と一致せず SW 介入層を silent に miss する。文字列リテラル中の `/foo/...` quoted のみ対象。literal `/` (root) は skip。canonical pathname 抽出不可 / drift >0 で fail | BLOCKING |
| 161 | robots.txt User-agent: * baseline (no full-site disallow)。robots.txt が `User-agent: *` を持ち、そのブロック内に `Disallow: /` (全 site 拒否) が無いことを強制。silent な `Disallow: /` 化は全 generic crawler (AI + search) からの deindex を意味し AIO-first サイトには category-collapse。behavior e2e は localhost に走るため crawl policy の劣化を検出できない。`User-agent: *` の section (次の `User-agent:` 行まで) を抽出し full-site disallow の存在を否定する | BLOCKING |
| 162 | `.gitignore` baseline ignore-rules for CI/build artifacts。`.gitignore` が node_modules/ / __pycache__/ / /test-results/ / /playwright-report/ / /blob-report/ の 5 ルール全て宣言することを強制。silent 削除は偶発 `git add` で CI artifact (数百 MB 級) や node_modules を staging に載せうる。Check 37 は tracked 後の artifact 検出だが本 Check は upstream gate 保護で artifact が staging に着く前に防ぐ | BLOCKING |
| 163 | `<link rel=icon>` / `<link rel=apple-touch-icon>` href resolves to actual file。index.html の `<link rel=icon>` / `<link rel=apple-touch-icon>` の非 data: href が実在 repo file に resolve することを強制。dangling は SILENT — ブラウザ default globe icon に fall back / iOS Add-to-Home が縮小 screenshot にfallback。data: URI (inline SVG fallback) は exempt。canonical URL pathname を href から strip し repo-relative path に map | BLOCKING |
| 164 | og:image / twitter:image content URL resolves to actual file。index.html の og:image / twitter:image content URL が実 repo file に resolve することを強制。dangling は SILENT — social/OG card preview が broken image を提示し console error も behavior-test signal も出ない。Check 153 (canonical URL prefix) と Check 163 (icon href resolves) を OG image surface に拡張 | BLOCKING |
| 165 | `.well-known/api-catalog` JSON + anchor canonical origin。`.well-known/api-catalog` が valid JSON + linkset array (≥1 entry) + 最初 entry の anchor URL が `<link rel=canonical>` href を prefix として持つことを強制。drift は SILENT に AI crawler の API endpoint discovery を破壊 (catalog は mcp.json / agent-skills / aio-manifest / llms-full への entry-point pointer)。JSON parse 失敗 / linkset 不在 / anchor drift で fail | BLOCKING |
| 166 | sitemap.xml `<loc>` URLs all start with canonical URL prefix。sitemap.xml の全 `<loc>` URL が `<link rel=canonical>` href を full prefix として持つことを強制。Check 63 は origin-only 整合だが、本 Check は canonical URL の full prefix (origin + base path) で揃える。drift (sibling project path 等) は SILENT — sitemap crawler が 404 する URL を index する。canonical / locs 抽出不可 / drift で fail | BLOCKING |
| 167 | `aio-monitoring.yml` weekly schedule presence。AIO 監視 workflow が `schedule.cron:` trigger を持つことを強制。silent 削除で週次 AIO discovery / citation observability loop が停止し observability データが stale 化 (workflow が単に発火しない silent 劣化)。schedule または cron rule 欠落で fail | BLOCKING |
| 168 | aio-manifest entity.architecture references C1/C2/C3 markers。aio-manifest.json `entity.architecture` 文字列が C1/C2/C3 constraint markers ("Vanilla JS", "IIFE", "ErrorBoundary") を含むことを強制。drift は SILENT に AIO entity の architectural identity 宣言を弱体化 (AI crawler が manifest 経由で本 site を Boring-Technology Vanilla JS SPA と認識できなくなる)。CLAUDE.md §1 architecture statement の manifest 側 mirror。marker 欠落で fail | BLOCKING |
| 169 | aio-manifest entity.role contains canonical role markers。aio-manifest.json `entity.role` list が CLAUDE.md §1 の canonical role identifier 3 件 ("AI-Driven PM", "IT Consultant", "KERNEL Framework Designer") を含むことを強制。drift は SILENT に AIO entity の professional role 宣言を弱体化 (AI crawler の entity disambiguation 精度劣化)。marker 欠落で fail | BLOCKING |
| 170 | aio-manifest entity.disambiguation negative-identity markers。aio-manifest.json `entity.disambiguation` 文字列が CLAUDE.md §1 の canonical negative-identity markers ("academic researcher", "diplomat", "artist", "patent inventor") を含むことを強制。drift は SILENT に disambiguation signal を弱体化 (AI crawler が学術研究者など同名の他 entity と conflate)。marker 欠落で fail | BLOCKING |
| 171 | index.html `ai:*` meta URL tags share canonical URL prefix。index.html の URL を持つ 4 つの `<meta name="ai:*">` (ai:context / ai:entrypoint / ai:canonical / ai:aio-manifest) が canonical URL prefix で始まり、ai:canonical は canonical 完全一致を強制。drift は SILENT に AIO meta layer を canonical URL family から desync させ AI crawler が ai:context / ai:aio-manifest を fetch して 404 で discovery 効果が崩壊する。canonical / 4 meta tag いずれかの欠落 / drift で fail | BLOCKING |
| 172 | aio-manifest entity name variants cover canonical identifiers。aio-manifest.json の entity.name + entity.name_ja + entity.name_alt が CLAUDE.md §1 canonical name identifier 4 件 ("Yuta Yokoi", "横井雄太", "Yokoi Yuta", "yuta") を網羅することを強制。drift は SILENT に AIO entity matching を弱体化 (AI crawler が drop された name variant で query しても本 entity が hit しない)。variant 欠落で fail | BLOCKING |
| 173 | js/identity.js AUTHOR canonical values。js/identity.js の AUTHOR constants が canonical 値を保持: DISPLAY_NAME='yuta' (視覚層 anonymity Check 124)・JAPANESE_NAME='横井雄太'・AUTHORITATIVE_NAME に "Yuta Yokoi" + "横井雄太" 含む。drift で entity-bearing JSON-LD (Person @type) や sr-only entity anchor が silent に壊れる。Check 172 (aio-manifest 側) の shipped JS 側 mirror | BLOCKING |

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
| BLOCKING（失敗で exit 1） | 114 | Check 52/60 を除く全カテゴリのチェック（Check 53〜59, 61〜118 を含む。サブチェックを持つものは全サブが BLOCKING） |
| ADVISORY/WARNING（exit に影響しない） | 4 | Check 34（honest dating）・Check 36（future-dated lastmod）・Check 52（file-size budget）・Check 60（ESLint warning baseline） |

注: Check 34/36 は元から WARNING 級として設計されている（公開面の軽微な日付ずれを観測するが、ビルドを止めない）。Check 52 は quiz-domain-split + bloat-governance increment で追加した advisory（肥大化予算は CI を止めるべきでないため）。Check 53（modulepreload 解決）・Check 54（eslint↔@eslint/js メジャー一致）は console-fix increment で追加（ともに BLOCKING）。Check 55（CI lint-target 整合）・Check 56（factory-pattern 引数被覆）は v80+ Stage 5-k CI hygiene fix で追加（Stage 5-j 隠れバグ再発防止・ともに BLOCKING）。Check 57（modulepreload ↔ _modules47 集合）・58（e2e ALL_ROUTES ↔ main.js switch 集合）・59（file-size-budget §2/§4 集合）・61（factory docstring marker）は post-Stage 5 「CI 更なる手厚化」増分で追加（structural coherence 強制・全 BLOCKING）。Check 60（ESLint warning baseline 回帰）は同 increment で追加した advisory。Check 62（AIO entity canonical_url cross-surface 一致）・63（crawler discovery origin alignment）・64（map table 昇順）・65（Last-Updated ISO-8601 形式）・66（title entity-identifier）・67（workflow permissions 明示）・68（dependabot 二 ecosystem）・69（engines.node ↔ CI pin）・70（runbook §9 cross-reference）・71（BUDGET-DATA path 実在）は post-Stage 5 「CI 更なる手厚化 v2」増分で追加した 10 件の構造整合性 BLOCKING（全て exit に影響）。残るチェックはすべて BLOCKING である。

---

## 4. 将来の `lib/` 分割に向けた指針（本 increment では実行しない）

第一段階として、§1 の純 helper（`read` / `read_bytes` / `extract` / `_csp_sri_hash`）を `.github/scripts/lib/io_utils.py` のような単一モジュールへ切り出す案が最も安全である。これらは Check 番号を持たず副作用も小さいため、Check 45 の自己整合（番号体系）を壊さない。切り出し後は、(a) `python3 .github/scripts/check_repository_consistency.py` をローカルで実行して同一結果になること、(b) GitHub Actions の `architecture-validation.yml` でも同じ import path が解決すること、の両方を確認する。Python の import path は、スクリプトが `.github/scripts/` 配下で実行される前提に依存するため、`sys.path` への追加か相対 import の設計を慎重に行う。

第二段階以降として、カテゴリ単位（A〜F）でのチェック本体の分割が考えられるが、これは Check 45 の前提（docstring インベントリとコードセクションが同一ファイル内で対応する）の再設計を伴うため、helper 抽出が安定し、かつ Check 45 を「複数ファイルにまたがるインベントリ」に対応させる設計が固まってから着手する。本マップは、その判断のための地図である。**結論として、本 increment は分割を行わず、カテゴリ化と helper 識別という準備に止める。**
