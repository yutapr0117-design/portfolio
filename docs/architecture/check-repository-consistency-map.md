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
| 102 | 核心運用ポリシー（AI 自走全振り / 人間は制御・監査のみ）が canon に明記（102a: AI2AI.md STEP 3 Operating Model marker / 102b: CLAUDE.md §7 参照 / 102c: 「AI proposes, human disposes」献策ポリシー / 102d: 「No terminal "done" state」継続改善ポリシー＝AI の自発停止・完了宣言を禁止 / 102e: 「Infinite improvement＝改善は無限・完璧は存在しない」真理＝AI が「収束/枯渇」の自己判断を下すことを禁止・padding ガードは増分粒度のみ）。核心ガバナンス契約の silent drift を防止 | BLOCKING |
| 103 | style.css に `@media (prefers-contrast: more)` 高コントラスト fallback 存在（WCAG 1.4.11 強化。render-neutral ゆえ §3 baseline ゲート非該当） | BLOCKING |
| 104 | npm から呼ばれる全 `.github/scripts/*.py`（package.json `scripts` から導出・hardcode せず）が `sys.version_info < (3, 10)` guard を持つ（PEP 604 `str \| None` 等の 3.10+ 構文を使うため、guard 無しでは Python 3.9 で cryptic な `TypeError` が import 時に出る。明示エラーで止める guard の silent 除去を防止＝AI-agnostic onboarding 保護） | BLOCKING |
| 105 | check-repository-consistency-map.md ↔ 実装の Check 番号 bijection（map の `\| N \|` 行が実装 `# ── N.` セクションと完全一致。alpha sub-check は整数に正規化）。Check 45（docstring↔section）の cross-document 版で、新 Check 追加時の map 行足し忘れ drift を構造的に防止 | BLOCKING |
| 106 | `.nvmrc`（ローカル dev 契約）の Node major が全 `.github/workflows/*.yml` の `node-version` pin と一致し、pin 同士も単一 major に揃う。Check 69（engines が pin を許容するか）を補完し、ローカルと CI の interpreter 分裂を防止 | BLOCKING |
| 107 | total-check-runbook.md §11「CI workflows overview」が全 `.github/workflows/*.yml`（backtick 引用の filename）を過不足なく列挙（doc ↔ ディスク bijection）。workflow 追加/削除時の索引 drift を防止。Check 75（incident README）/ 105（check-map）の CI workflow 面版 | BLOCKING |
| 108 | 全追跡ファイル（`git ls-files`・docs/files 自身除く）が `docs/files/<path>.md` の 1-to-1 ミラーを持ち、各ミラー（README.md inventory / _template.md 除く）が実 source を持つ（完全 bijection）。Check 96 は Phase-1 shipped-code 33 件のみ強制ゆえ、残り ~100 ミラーの欠落/orphan drift を本 Check が構造的に閉じる | BLOCKING |
| 109 | 現在状態を語る living 文書の全面（root CLAUDE.md / README.md / CHANGELOG.md / Claude2Claude.md / .claude/CLAUDE.md / .claude/README.md / .claude/agents/*.md / .claude/skills/*/SKILL.md / .claude/commands/*.md / runbook §9 以外 / 本 map）が、現在の Check タリーを prose にハードコードする drift（「総数」直書き / 「総数は _N_ まで成長」/ 「all _N_ Checks」/ 「consistency _N_ Check」/ 「Check count」直書き）を禁止。歴史層（per-increment changelog の maintainability-map / extraction-map・Session Record・improvement-notes・decision・docs/files ミラー）は point-in-time 記録ゆえ対象外。PR #68 が runbook/map を drift-proof 化した後も再発（PR #68 自身が §11 に新 stale 値を混入）したため機械強制化。正値は §9（Check 70 強制）を単一権威とし他所は §9 への pointer に置換 | BLOCKING |
| 110 | e2e の `A11Y_ROUTES`（axe a11y テストの対象）の hash 集合が `ALL_ROUTES`（route-render の網羅集合）の hash 集合と完全一致。新ルートを ALL_ROUTES に足したのに A11Y_ROUTES へ足し忘れる「a11y 未検証ルート」coverage gap を防ぐ（Check 58 の a11y 面版） | BLOCKING |
| 111 | e2e/portfolio.spec.js が `waitForLoadState('networkidle')` を screenshot regression テスト以外で使わない（許容は直後数行に `toHaveScreenshot` がある screenshot テストのみ）。networkidle は外部 Google Fonts / service worker SWR の background fetch で idle 到達せず CI で 30s ハングする flake クラス（PR #132 で root-fix）の再導入を防ぎ、behavior テストは `domcontentloaded` + expect auto-wait で同期させる | BLOCKING |
| 112 | js/apps.js の全 Enter-submit ハンドラ（task/todo/ai 入力）が IME composition ガードを持つ（`e.key === 'Enter'` を判定する行に必ず `Composing` = `!e.isComposing` または `!todoComposing` を併記）。日本語 IME 変換確定の Enter で未確定テキストが誤って追加/送信される footgun（task=PR #151 / ai=PR #152 で修正）の再導入を防ぐ。Enter ハンドラが 0 個なら vacuous-gate として fail | BLOCKING |
| 113 | model-agnostic 正典 AI2AI.md（STEP 5.5）と Claude router CLAUDE.md（§5）の**双方**が handoff-first commit/PR 規律（テーマ束ね PR ×`gh pr merge --rebase` ×commit 数は OUTPUT）をマーカー（rebase + no-padding 条項）で保持。オーナーがリポジトリ核として正式採用したルールが、どちらかの canon から silent に消えて squash/粗 commit へ退行するのを防ぐ | BLOCKING |
| 114 | e2e/portfolio.spec.js に `test.only` / `describe.only` が無い。`.only` が残ると Playwright がその 1 件のみ実行し他を全 skip → CI が緑のまま suite 空洞化（false-green footgun = vacuous-gate の裏返し）。デバッグ用 `.only` の commit 漏れを禁止 | BLOCKING |
| 115 | index.html CSP meta が hardening baseline を維持: `script-src` 等に `'unsafe-inline'`/`'unsafe-eval'` が無く（inline は sha256 hash + `'unsafe-hashes'` で許可）、`default-src 'self'` / `object-src 'none'` / `base-uri 'self'` が存在。CSP 弱体化（XSS 防御無効化）の高影響セキュリティ退行を防ぐ（Check 7 の position/hash に対する runtime-policy 面） | BLOCKING |
| 116 | playwright.config.cjs の `reuseExistingServer` が `false`（`: true` 不在）。true だと既存 dev server を再利用し commit 前の stale 状態を検証 → CI が false-green 化する vector を防ぐ | BLOCKING |
| 117 | playwright.config.cjs の `toHaveScreenshot.maxDiffPixelRatio` が sanity ceiling 0.05 以下。§3 baseline ゲートの許容を silent に緩めて本物の視覚 regression を見逃す退行を防ぐ | BLOCKING |
| 118 | 全 shipped route（e2e ALL_ROUTES の name を正規化＝Check 58 が main.js と結ぶ権威）が js/page-meta.js の PAGE_META に metadata を持つ（PAGE_META keys ⊇ routes）。route が PAGE_META に無いと applyMeta が early-return し title/desc/JSON-LD が出ない silent AIO/SEO gap を防ぐ（PAGE_META↔ALL_ROUTES↔main.js coherence 三角形を閉じる） | BLOCKING |

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
