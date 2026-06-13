#!/usr/bin/env python3
"""
check_repository_consistency.py — P0-23 / Cross-file consistency check (BLOCKING)

Verifies that key version, date, and structural invariants hold across the repository.

Checks performed (the numbering is historical/incremental; this list is the
authoritative inventory and is kept in sync with the implementation below):
  1.  ai:version (index.html) == Pipeline-Version (AI2AI.md)
  2.  ai:version == SITE_CONFIG.VERSION or main.js VERSION string
  3.  mcp.json server.version major matches ai:version
  4.  llms.txt / .well-known/llms.txt / llms_well-known.txt / .well-known/llms_well-known.txt are byte-identical
  5.  .well-known/index.json == .well-known/agent-skills/index.json (byte-identical)
  6.  style.css has no stale "Current release: v73" or "NEXT_PLANNED_RELEASE" markers
  7.  index.html CSP meta appears before inline suppressor script (error-suppressor inlined)
  7b. index.html CSP authorizes inline suppressor (hash recomputed from live content)
  7c. index.html CSP authorizes inline speculation rules (hash recomputed from live content)
  8.  index.html has no <meta http-equiv="X-Content-Type-Options"> (header-only control)
  9.  sitemap.xml is valid XML
  10. All .github/scripts/*.py parse without syntax errors
  11. aio_monitoring.py summary dict contains 'enabled_engines' and 'total_cited_count'
  12. No stale "72回/72回以上" in current-description files (history lines exempt)
  13. "70超" appears only in history/log context
  14. v1→v74 canonical declaration present in index.html or AI2AI.md
  15. Project Pages robots/.well-known constraint documented (llms-full.txt / AI2AI.md / README.md)
  16. e2e/portfolio.spec.js screenshot test has a baseline-skip guard
  17. ai:last-modified (index.html) == SITE_CONFIG.LAST_UPDATED (main.js)
  18. sitemap.xml root <lastmod> == ai:last-modified (per-URL lastmod policy)
  19. sw.js CACHE_NAME version == ai:version
  20. index.html has og:image:width / og:image:height / og:image:alt
  21. llms alias files Last-Updated are in sync
  22. AI2AI.md Session Record headers are in ascending order
  23. .github/workflows/*.yml and dependabot.yml parse without YAML syntax errors
  24. llms-full.txt Last-Updated is within 7 days of AI2AI.md and >= v75-v78 floor
  25. aio-monitoring-log.json has an evidence_policy key (attempt_log_only honesty)
  26. aio-manifest.json archive role #1-#N matches AI2AI-archive.md max Session Record
  27. llms-full.txt has no stale C1–C6 in current-constraint context (should be C1–C7)
  28. e2e/portfolio.spec.js has no test() nested inside another test()
  29. Playwright baseline-generation linkage intact (snapshot workflow <-> spec env signal)
  30. v80+ maintainability anchor docs present (repository-maintainability-map / main-js-extraction-map)
  31. Claude2Claude.md references AI2AI.md's current max Session Record
  32. index.html application/ld+json blocks are valid JSON (BLOCKING)
  33. Zenn featuring layers share the canonical article slug set + PRIMARY (BLOCKING)
  34. doc Last-Updated equals its sitemap <lastmod> — honest dating (WARNING)
  35. robots.txt advertises a Sitemap: directive resolving to sitemap.xml (BLOCKING)
  36. sitemap.xml has no future-dated <lastmod> (WARNING)
  37. No generated/cache artifacts (node_modules, __pycache__, *.pyc, test-results,
      playwright-report, blob-report, .DS_Store, …) are tracked in the repository.
      Authoritatively uses `git ls-files`; falls back to a pruned filesystem walk
      for non-git contexts (ZIP/zipball export). (BLOCKING)
  38. package.json <-> package-lock.json sync: lockfileVersion 3, lock root
      name/version/devDependencies match package.json, package.json is private,
      and has no runtime dependencies (dev-tooling-only manifest invariant). (BLOCKING)
  39. Every same-project sitemap.xml <loc> resolves to a committed file
      (root/trailing-slash -> index.html; external URLs skipped). Prevents
      advertising crawler-404 URLs. (BLOCKING)
  40. CSS lint execution-path hygiene: package.json devDependencies declares
      stylelint; check_css_stylelint.py references node_modules/.bin/stylelint
      (local-binary-preferred); npx remains a documented fallback. Guards the
      Phase 2 CI-hygiene increment #3 contract against a false-green-prone
      npx-primary regression. (BLOCKING)
  41. AIO monitoring log ↔ manifest atomic-commit invariant: any workflow that
      stages docs/evidence/aio-monitoring-log.json for commit must also run
      update_aio_digests.py and stage .well-known/aio-manifest.json in the same
      workflow, so the log and its recorded digest are committed atomically.
      Guards the CI-hygiene increment #4 fix against a non-atomic-commit
      regression that would drift the BLOCKING digest gate. (BLOCKING)
  42. docs/ artifact placement & naming hygiene: (42a) every file directly under
      docs/incident-artifacts/ matches an allowed naming pattern (decision-*.md /
      improvement-notes-*.md / *.yml / README.md); (42b) no decision-*.md or
      improvement-notes-*.md file lives outside docs/incident-artifacts/. Turns the
      placement convention documented in docs/README.md into an enforced invariant
      (artifact-placement governance increment). (BLOCKING)
  43. main.js AIDK Isolated Kernel structural integrity: the "DO NOT EDIT: AIDK
      Isolated Kernel" header marker, the startViewTransition proxy installer, and
      the Trusted Types 'default' policy are all present, and the file is wrapped in
      a single top-level IIFE (C2). Converts the kernel-protection posture — until
      now enforced only by a code comment and the architecture docs — into a
      machine-enforced invariant, so kernel removal/un-wrapping fails CI. (BLOCKING)
  44. AIO provenance canary token cross-surface consistency: the single canary token
      string (SAKURA-AIO-PROVENANCE-CANARY-<YYYY>-<8 hex>) appears identically on every
      published AIO surface (llms.txt + its 3 byte-identical mirrors, llms-full.txt) AND
      in every monitor that searches for it (aio_monitoring.py, check_public_deployment_
      freshness.py), with exactly one canonical value across the whole repository. The
      canary's entire evidentiary value rests on the published token and the searched
      token being the same string; a silent edit to one side would make the monitor hunt
      for a token that is no longer published, yielding permanent false negatives that no
      other check would catch. This turns that load-bearing assumption into a machine-
      enforced invariant. (BLOCKING)
  45. This check file's self-documentation matches its implementation: the numbered
      entries in THIS module docstring (the "N. ..." inventory above) and the numbered
      "# ── N." section-header comments in the code body describe the same set of checks,
      are contiguous 1..N with no gaps or duplicates on each side, and agree with each
      other. The inventory and the section headers are two hand-maintained descriptions of
      the same checks; until now nothing stopped them from silently drifting apart (a new
      check added in the body but forgotten in the inventory, or renumbered on one side
      only), which would make this file's own documentation lie about what it enforces.
      This is a self-referential meta-check: it is true precisely because anyone adding a
      check updates BOTH descriptions together — exactly the discipline it exists to keep.
      It asserts structural agreement of the documentation, not the behaviour of any
      individual check. (BLOCKING)
  46. package.json lint scripts cover a consistent JavaScript file set: the files named in
      the `lint` script (ESLint) and the files named in the `lint:js` script (node --check
      syntax pass) are exactly the same set, and that set is exactly the shipped *.js files
      on disk — the repository-root *.js files together with everything under js/ (where the
      v80+ staged split places extracted modules). These two script lists are hand-maintained
      duplicates of the same fact ("which JS files does this project ship and gate?"); if a
      future JS file is added to one script but forgotten in the other — or added to the
      repo but to neither — the lint coverage and the syntax-check coverage would silently
      diverge, leaving a shipped file ungated with nothing to catch it. This makes the two
      lists' agreement, and their match to the actual shipped JS files (root ∪ js/), a
      machine-enforced invariant. (BLOCKING)
  47. main.js ⇄ js/ module ESM import/export contract: for each local module main.js imports
      from (js/brand.js, js/constants.js, js/identity.js, js/meta-management.js,
      js/page-meta.js, js/pages.js, js/pure-utils.js, js/router.js, js/state.js, js/storage.js,
      js/store.js, js/theme.js, js/ui-components.js and js/quiz/{architecture,aws,pm,quality}-
      quiz-data.js — 17 modules), every name main.js imports is actually exported by that
      module, and (symmetrically) every name the module exports is imported by main.js — an
      exact bijection per module. This guards the physical module split (v80+ Stage 2 pure
      utilities, Stage 3/3-b static quiz data, Stage 4 UI components, Stage 5 Router+PAGE_META,
      Stage 5-b page components, Stage 5-c Safe Storage, Stage 5-d CONSTANTS, Stage 5-e AUTHOR
      identity, Stage 5-f Brand factory, Stage 5-g Store factory, Stage 5-h State factory,
      Stage 5-i Theme factory, Stage 5-l Meta Management factory). Because the site is
      build-free
      and served directly, a mismatch is a *runtime* failure: importing a name a module does
      not export throws a module-load error and the whole SPA fails to boot, while a
      left-behind unused export signals the split has drifted. (This check is exactly what
      would have caught the Stage 3 near-miss where main.js referenced four quiz datasets but
      an early draft of the module exported only two.) The import lists carry inline `//`
      comments, so the parser strips per-line comments before extracting identifiers, and it
      matches each `import {…} from '<module>'` block in isolation (the captured brace group
      excludes braces so a match cannot span an adjacent import block). The export-side parser
      recognises three forms — (1) `export function name()`, (2) `export const|let|var name`,
      and (3) `export { name1, name2, ... };` named-list (with optional `as` aliasing) — so a
      module that re-exports already-declared identifiers at file tail (e.g. js/pages.js) is
      correctly inventoried. Each module must also stay import-free (a dependency-free leaf).
      This turns the hand-maintained cross-file contract into a machine-enforced invariant.
      (BLOCKING)
  48. Playwright baseline-commit pipeline permission coupling: if
      update-playwright-snapshots.yml contains the pull-request-creation step (the action
      that commits the generated baseline PNGs via a PR), then the workflow must also declare
      both `contents: write` (to push the baseline branch) and `pull-requests: write` (to open
      the PR). These two facts live in the same file but in different sections — the
      permissions block near the top and the PR step near the bottom — so they can drift
      apart silently. If a later edit trimmed the permissions back to read-only while leaving
      the PR step in place (for example by copying from the read-only regression workflow),
      the step would fail at *runtime* with a confusing permissions error and nothing would
      catch it beforehand. This check converts that latent runtime failure into an immediate
      pre-commit error, in the same spirit as the Check 29 env-signal linkage. (BLOCKING)
  49. index.html JSON-LD worksFor ↔ Organization linkage integrity: the entity-linkage
      strategy that connects the Person to the established employer organization only works
      if three facts inside the first JSON-LD @graph stay in agreement — the Person node
      carries a worksFor whose (possibly nested) reference points at the organization's
      canonical @id, AND an Organization node with that exact @id actually exists as a sibling
      in the same @graph. Because the site is served statically and consumed by knowledge-graph
      engines, a dangling reference is a *silent* failure: a worksFor pointing at an @id that
      no node defines simply fails to resolve the employment edge, so the whole "link the
      person to a strongly-established entity" strategy quietly collapses while the page still
      looks fine. If a future edit renamed the organization @id without updating the Person's
      worksFor (or deleted the Organization node but left the reference), this check fails at
      pre-commit time rather than letting the broken linkage ship. It also confirms the first
      JSON-LD block parses as valid JSON. Same cross-reference-integrity spirit as Check 47
      (import/export bijection) and Check 48 (permission coupling). (BLOCKING)
  50. ESLint flat-config migration integrity: the lint toolchain has migrated off the
      End-of-Life ESLint 8.x / eslintrc format onto flat config (introduced as default in 9.x;
      now pinned at v10). Two facts must
      stay true for that migration to remain intact. First, eslint.config.mjs (the flat config)
      must exist at the repository root — it is the sole config ESLint 9.x auto-discovers, and
      deleting it would make every lint run fall back to "no configuration" and pass vacuously.
      Second, the package.json `lint` script must NOT carry the legacy eslintrc-era flags
      (`--no-eslintrc`, `--config .eslintrc.json`, `--env`): ESLint 9.x removed those flags, so
      their presence would make `npm run lint` exit 2 (config/flag error) — and the historical
      vacuous-gate incident showed exactly how a flag mismatch can be silently swallowed. The
      legacy `.eslintrc.json` must also be absent (its lingering presence would invite a
      regression back onto the EOL format). This check converts a silent reversion to the EOL
      linter into an immediate pre-commit error, in the same discover→systematize spirit that
      added Checks 46–49. (BLOCKING)
  51. Active-runbook Playwright baseline-generation version matches the pin: the Playwright
      version named in total-check-runbook.md's baseline-generation instruction must equal the
      @playwright/test pin in package.json. Visual-regression baselines depend on the generating
      Playwright (Chromium) version, and the operational "generate the baseline with version X"
      instruction lives in the active runbook in prose — a different place from the pin — so a
      dependency bump can leave the runbook's version behind (this happened across the
      1.49.1→1.55.1→1.60.0 bumps, where the runbook kept saying 1.55.1 after the pin moved to
      1.60.0). A human following a stale runbook would generate the baseline with the wrong engine
      and produce spurious visual diffs against CI's pinned version. This extracts every concrete
      Playwright version the active runbook names and requires all of them to equal the pin
      (vacuously true if it names none, but the pin must be readable). Scope is the active runbook
      only: the decision records under docs/incident-artifacts/ are append-only history that
      legitimately preserve the version current at each increment and must NOT be rewritten, and
      repository-maintainability-map.md keeps the version-evolution narrative as a layer — only the
      single-source operational runbook is pinned. Same "surface a latent operational failure at
      pre-commit time" spirit as Check 48 (permission coupling) and Check 29 (baseline linkage). (BLOCKING)
  52. File-size budget advisory: each file listed in the machine-readable BUDGET-DATA block of
      docs/architecture/file-size-budget.md whose budget is a concrete integer must have a current
      line count at or below that budget. This is the bloat-governance counterpart to the staged
      split: main.js carries a strong-advisory ceiling so its growth is actively discouraged, while
      protected AIO canon and archive/evidence files are recorded with budget "-" (no ceiling)
      because line growth there is itself valuable (digests, session records, incident history). The
      budget lives single-source in file-size-budget.md (as-decided) and this check only parses and
      compares against reality — it never hardcodes a line number, the same "documentation must match
      reality" philosophy as Check 44/45/47, applied to the line-budget domain. Deliberately
      NON-BLOCKING (ADVISORY): an over-budget file raises a warning a human reviews, never a CI
      failure, so a justified increase (a new safety comment, a new archive entry) is never blocked;
      main.js is the file whose advisory the owner treats as near-hard. A missing or unparseable
      budget file is itself a (non-blocking) advisory. (ADVISORY)
  53. index.html modulepreload href resolution: every <link rel="modulepreload" href="..."> in
      index.html must resolve to a file that exists in the repository. This systematizes the
      dangling-preload 404 class — when js/quiz-data.js was split into js/quiz/*.js, the
      modulepreload hint kept pointing at the deleted module and produced a guaranteed console
      404 on every page load. A modulepreload to a non-existent module is always a defect, so
      this is BLOCKING. Same-origin repo-relative hrefs only (./js/..., js/..., /portfolio/js/...);
      absolute cross-origin preloads are out of scope (not resolvable against the working tree). (BLOCKING)
  54. ESLint <-> @eslint/js major-version coupling: package.json's `eslint` and `@eslint/js`
      devDependencies must share the same MAJOR version. ESLint v10 reorganised how the
      recommended-config package resolves, and a major mismatch (e.g. eslint 10.x with
      @eslint/js 9.x) causes a duplicate/incompatible install and config-resolution conflict.
      They version independently within a major (eslint 10.4.1 pairs with @eslint/js 10.0.1), so
      only the major is compared, not exact equality. (BLOCKING)
  55. CI lint-target authoritative coupling: architecture-validation.yml's `node --check` and
      `npx eslint` steps must either (a) enable `shopt -s globstar` before expanding
      `js/**/*.js`, or (b) call the package.json scripts (`npm run lint:js` / `npm run lint`).
      Without globstar, bash collapses `js/**/*.js` to `js/<subdir>/<file>.js` and silently
      skips direct `js/<file>.js` leaf modules. This was the root cause of the Stage 5-j
      hidden ReferenceError in js/pages.js — the file was extracted, listed in package.json,
      and exported names — but ESLint never scanned it because the CI glob missed it for
      weeks. This check converts that vacuous-gate class into a structural BLOCKING signal.
      (BLOCKING)
  56. js/ leaf module factory-pattern parameter coverage: for each js/ module that uses the
      factory pattern (`export function createFoo({deps})` — note: the leading argument MUST
      be a destructured object `{...}` so that a plain utility named `createXxx` like
      `createIcon(name, size)` is correctly NOT classified as a factory), main.js MUST invoke
      the factory `createFoo({...})` at least once. A factory exported but never invoked is
      the Stage 5-j bug class: the module compiles fine, ESLint passes, Check 47 passes
      (import/export bijection holds), but at runtime any caller of the page/manager hits
      ReferenceError because the dependency identifiers are never bound. This check converts
      that latent runtime failure into a pre-commit BLOCKING error. (BLOCKING)
  57. index.html modulepreload ↔ _modules47 set equality: index.html の
      `<link rel="modulepreload" href="./js/<name>.js">` の集合と check_repository_
      consistency.py の `_modules47` リストの集合が完全一致することを機械強制する。これにより、
      新しい葉モジュールを抽出したが modulepreload に追加し忘れた場合（初期ロード遅延）や、
      modulepreload に存在するが _modules47 から脱落した場合（lint カバレッジ漏れ）の
      drift を pre-commit でブロックする。Check 47（import/export bijection）と Check 53
      （modulepreload href 解決）を補完する「集合カバレッジ」検査。(BLOCKING)
  58. e2e/portfolio.spec.js の ALL_ROUTES ↔ main.js switch case 集合一致: e2e spec の
      `ALL_ROUTES` 配列に列挙されたルート名と main.js の renderer switch 内の `case '<name>':`
      列の集合が一致することを機械強制。新ルートを main.js に追加したが e2e に追加し忘れた
      場合（テスト未カバレッジ）や、main.js から削除したルートが e2e に残った場合
      （404 fallback テスト）の drift を pre-commit でブロックする。Stage 5-j の hidden
      ReferenceError class（未訪問ルートに残る runtime error）を構造的に閉じた Check 55/56
      の延長で、「ルートカバレッジ」も機械強制する。(BLOCKING)
  59. file-size-budget.md §2 表 ↔ §4 BUDGET-DATA 集合一致: docs/architecture/file-size-
      budget.md の人間可読 §2 表に列挙されたファイル集合と、機械可読 §4 BUDGET-DATA
      ブロックに列挙されたファイル集合が完全一致することを機械強制する。両者が drift すると
      「人間が見ている表」と「Check 52 が読む真値」が乖離し、運用上の見えない不整合を生む。
      Check 52（ADVISORY 行数予算）と Check 45（自己整合）の発想を、複数文書間にも適用した
      structural coherence 検査。(BLOCKING)
  60. ESLint warning baseline regression guard: docs/architecture/file-size-budget.md の
      `<!-- ESLINT-BASELINE-DATA -->` ブロックに記録された warning 数 baseline よりも、
      現状の `npm run lint` 実測値が増えていないことを ADVISORY で機械監視する。CI ログから
      "ESLint PASS — 0 errors, N advisory" を grep して N と baseline を比較し、N > baseline
      なら ADVISORY 警告を発する（exit に影響しない）。これにより、保護領域内の `no-var`/
      `curly`/`no-shadow` 等が無自覚に増える「lint 負債の静かな増加」を可視化する。
      Check 52 と同じ ADVISORY 級。(ADVISORY)
  61. js/*.js factory documentation marker: 各 js/ 葉モジュールが factory pattern を export
      する場合（`export function createXxx`）、ファイル先頭の docstring に "factory pattern"
      キーワードが含まれていることを機械強制する。これは「factory として抽出した経緯」を
      後続 AI / 人間レビュアーが file 単体を読むだけで認識できることを保証し、抽出経緯の
      ドキュメント drift を構造的に閉じる。(BLOCKING)
  62. AIO entity canonical_url cross-surface identity: aio-manifest.json の `entity.canonical_url`
      と llms-full.txt の `Canonical URL:` 値が 1 バイトも違わずに一致することを機械強制する。
      Entity の canonical URL は AIO 識別子の最重要 anchor — manifest と canon (llms-full) の
      双方が同じ URL を主張していないと、引用先 / クローラの ground-truth が分かれ、entity
      disambiguation が崩れる。C6 範疇内で「両者が drift したら BLOCKING」する Check 4 (llms 系
      byte-identity) の発想を entity-URL 単位に降ろした検査。(BLOCKING)
  63. Crawler discovery origin alignment: robots.txt `Sitemap:` URL の origin、aio-manifest.json
      `entity.canonical_url` の origin、sitemap.xml の全 `<loc>` の origin が完全に同一である
      ことを機械強制する。クローラは robots.txt → sitemap.xml の順に discover するため、両者
      が origin drift していると crawler は別ホストの URL を「同サイトの一部」と誤認するか
      丸ごと取りこぼす。さらに entity.canonical_url の origin もこれらと一致していないと、AIO
      引用先が外部ホストを指す事態になる。Check 35 (robots.txt の Sitemap directive 存在確認)
      と Check 39 (sitemap loc 実在確認) を補完する「同一 origin 一致」の structural integrity
      検査。(BLOCKING)
  64. check-repository-consistency-map.md table row ascending order: 当該文書の Check 一覧表が
      `| Check N | ... |` 形式で番号昇順に並ぶことを機械強制する。table 行が降順／重複してい
      ると新規 Check の挿入位置を誤り、番号衝突を引き起こす（Stage 5-l / 5-k' の naming 衝突
      と同種 class）。本 Check は表内の `Check N` を順次抽出し、ascending strict であることを
      機械強制する。(BLOCKING)
  65. docs/architecture/*.md Last-Updated ISO-8601 format: 全 docs/architecture/*.md について
      `Last-Updated:` フィールドが存在する場合は値が ISO-8601 `YYYY-MM-DD` 形式に厳密に従うこ
      とを機械強制する。Last-Updated は「文書がいつ真値だったか」を読み手 (AI/human) に伝える
      正本シグナルで、フォーマット揺れ (e.g. `06-13-2026`) は honest-dating 原則を内部から
      侵食する。Check 34 が sitemap lastmod との一致を ADVISORY で見るのに対し、本 Check は
      「日付フォーマットそのもの」を BLOCKING で固定する責務分離。(BLOCKING)
  66. index.html <title> entity-identifier presence: index.html の `<title>` 要素に entity
      primary identifier (`yuta` または `横井`、いずれも case-insensitive) が含まれることを
      機械強制する。`<title>` は SEO/AIO 検索結果の最重要 anchor で、entity 名が含まれていな
      いと SERP/LLM 引用時に「これは誰のサイトか」が一瞬で判定できなくなり、AIO 戦略（「機械
      可読な authority building」）の効果が消失する。C6 範疇内で title の「ブランディング
      anchor」性を機械強制する。(BLOCKING)
  67. GitHub Actions workflow explicit permissions: .github/workflows/*.yml の全ファイルに
      top-level `permissions:` ブロックが明示宣言されていることを機械強制する。permissions: が
      無いと GitHub の default token は full read/write 相当の広い権限になり、CWE-275
      (Missing Actions Permissions) クラスのセキュリティ問題となる。Check 48 (snapshot
      workflow の permissions 二重宣言整合) を補完する「全 workflow 適用版」の security
      baseline。(BLOCKING)
  68. dependabot.yml dual-ecosystem coverage: .github/dependabot.yml が `npm` (devDependencies
      の月次更新) と `github-actions` (workflow action major tag の月次更新) の両 ecosystem を
      update 対象に含むことを機械強制する。Dev tooling と GitHub Actions の自動更新は v80+ CI
      hygiene の基盤で、どちらかが欠落すると人手で月次更新を追跡する負債が積み上がる。設定
      ファイル drift を BLOCKING で防ぐ。(BLOCKING)
  69. package.json engines.node ↔ CI node-version pin alignment: package.json `engines.node`
      が CI workflow の Node version pin (`node-version: '24'`) を許容する範囲を含むことを機械
      強制する。両者が drift していると CI は 24 でビルドするが package.json は別 version を
      強制するため、ローカル開発と CI で実行 Node が分かれる inconsistency が生まれる。
      setup-node@v6 の pin と engines が許容範囲で揃っていることを pre-commit で保証する。
      (BLOCKING)
  70. total-check-runbook.md §9 check-count cross-reference: docs/architecture/total-check-
      runbook.md §9 の「consistency Check 総数」行に記述された Check 件数 (`**N**`) が
      check_repository_consistency.py の実装上の Check 番号最大値と一致することを機械強制する。
      Check 45 が docstring inventory ↔ section header の bijection を見るのに対し、本 Check
      は「実装ファイル ↔ runbook §9」の cross-document 整合性を担う。新 Check 追加時に runbook
      を更新し忘れる drift を pre-commit で構造的に閉じる。(BLOCKING)
  71. file-size-budget.md BUDGET-DATA path existence: docs/architecture/file-size-budget.md
      §4 BUDGET-DATA に列挙された各エントリのパスが実在ファイルを指すことを機械強制する。
      BUDGET-DATA は Check 52 (ADVISORY 行数予算) の真値だが、ファイル rename / 削除後に
      BUDGET-DATA から行を消し忘れると Check 52 が「存在しないファイル」を黙ってスキップし、
      削除後の monitoring drift が見えなくなる。本 Check は「BUDGET-DATA に登録された path は
      全て実在する」を BLOCKING で保証する。(BLOCKING)

Exit codes:
  0 — all checks passed
  1 — one or more checks failed (BLOCKING)
"""

import ast
import base64
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []
warnings: list[str] = []


def check(condition: bool, msg_ok: str, msg_fail: str, blocking: bool = True) -> None:
    if condition:
        print(f"OK: {msg_ok}")
    else:
        tag = "ERROR" if blocking else "WARNING"
        print(f"{tag}: {msg_fail}")
        (errors if blocking else warnings).append(msg_fail)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_bytes(path: str) -> bytes:
    return (ROOT / path).read_bytes()


def extract(pattern: str, text: str) -> str | None:
    m = re.search(pattern, text)
    return m.group(1) if m else None


# ── Load files ──────────────────────────────────────────────────────────────
html       = read("index.html")
ai2ai      = read("AI2AI.md")
mainjs     = read("main.js")
style      = read("style.css")
aio_mon    = read(".github/scripts/aio_monitoring.py")

mcp_data   = json.loads(read(".well-known/mcp.json"))

# ── 1. ai:version == Pipeline-Version ────────────────────────────────────────
html_v    = extract(r'name="ai:version"\s+content="(v\d+)"', html)
ai2ai_v   = extract(r"Pipeline-Version\s*:\s*(v\d+)", ai2ai)
check(
    html_v is not None and ai2ai_v is not None and html_v == ai2ai_v,
    f"ai:version ({html_v}) == Pipeline-Version ({ai2ai_v})",
    f"ai:version mismatch: index.html={html_v}, AI2AI.md={ai2ai_v}",
)

# ── 2. main.js VERSION string ────────────────────────────────────────────────
mainjs_v = extract(r"VERSION:\s*['\"]?(v\d+)['\"]?", mainjs)
if mainjs_v:
    check(
        html_v == mainjs_v,
        f"main.js VERSION ({mainjs_v}) == ai:version ({html_v})",
        f"main.js VERSION mismatch: main.js={mainjs_v}, index.html={html_v}",
    )

# ── 3. mcp.json server.version major ─────────────────────────────────────────
mcp_v     = mcp_data.get("server", {}).get("version", "")
mcp_major = mcp_v.split(".")[0] if mcp_v else None
html_major = html_v.lstrip("v") if html_v else None
check(
    mcp_major is not None and mcp_major == html_major,
    f"mcp.json server.version major ({mcp_major}) == ai:version major ({html_major})",
    f"mcp.json server.version major ({mcp_major}) != ai:version major ({html_major})",
)

# ── 4. llms alias files byte-identical ───────────────────────────────────────
llms_paths = [
    "llms.txt",
    ".well-known/llms.txt",
    "llms_well-known.txt",
    ".well-known/llms_well-known.txt",
]
llms_bytes = [(p, read_bytes(p)) for p in llms_paths if (ROOT / p).exists()]
if len(llms_bytes) >= 2:
    ref_path, ref_bytes = llms_bytes[0]
    for p, b in llms_bytes[1:]:
        check(
            b == ref_bytes,
            f"{p} is byte-identical to {ref_path}",
            f"llms alias mismatch: {p} differs from {ref_path}",
        )

# ── 5. .well-known/index.json == agent-skills/index.json ─────────────────────
idx_bytes = read_bytes(".well-known/index.json")
ask_bytes = read_bytes(".well-known/agent-skills/index.json")
check(
    idx_bytes == ask_bytes,
    ".well-known/index.json == .well-known/agent-skills/index.json",
    ".well-known/index.json and .well-known/agent-skills/index.json differ",
)

# ── 6. style.css stale markers ───────────────────────────────────────────────
check(
    "Current release: v73" not in style,
    "style.css: no stale 'Current release: v73' marker",
    "style.css: stale 'Current release: v73' marker found",
)
check(
    "NEXT_PLANNED_RELEASE" not in style,
    "style.css: no 'NEXT_PLANNED_RELEASE' marker",
    "style.css: stale 'NEXT_PLANNED_RELEASE' marker found",
)

# ── 7. CSP meta before inline suppressor script ───────────────────────────────
# error-suppressor.js is now inlined in <head> to eliminate the network-fetch
# timing gap that caused intermittent "message channel closed" console errors.
_INLINE_SUPPRESSOR_ANCHOR = "window.addEventListener('unhandledrejection'"
pos_csp = html.find('<meta http-equiv="Content-Security-Policy"')
pos_err = html.find(_INLINE_SUPPRESSOR_ANCHOR)
check(
    pos_csp != -1 and pos_err != -1 and pos_csp < pos_err,
    f"CSP meta (pos {pos_csp}) appears before inline suppressor (pos {pos_err})",
    f"CSP meta must appear before inline suppressor (CSP={pos_csp}, inline={pos_err})",
)

# ── 7b/7c. inline-script CSP hashes are present AND match actual content ──────
# Both the inline suppressor and the inline speculation-rules block are subject to
# script-src CSP in Chrome. Each requires its exact-content SHA-256 hash in script-src.
# We compute the hash from the live content (not a hardcoded constant) so this check
# catches BOTH a removed hash AND content edited without recomputing the hash —
# the exact failure mode that produced "Applying inline speculation rules violates ... script-src".
def _csp_sri_hash(content: str) -> str:
    return "sha256-" + base64.b64encode(
        hashlib.sha256(content.encode("utf-8")).digest()
    ).decode()

# Strip HTML comments first: comments may contain literal <script>...</script> strings
# (e.g. the CSP architecture note documents the speculationrules tag), which would
# otherwise corrupt regex-based extraction. The browser never hashes comment text.
_html_nc = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

# 7b. inline suppressor (plain <script> containing the unhandledrejection listener)
_plain_scripts = re.findall(r"<script>(.*?)</script>", _html_nc, re.DOTALL)
_sup_content = next((s for s in _plain_scripts if "unhandledrejection" in s), None)
if _sup_content is not None:
    _sup_hash = _csp_sri_hash(_sup_content)
    check(
        f"'{_sup_hash}'" in html,
        f"index.html CSP authorizes inline suppressor (content hash {_sup_hash})",
        f"index.html CSP does NOT authorize inline suppressor — computed {_sup_hash} "
        f"is absent from script-src. Inline content and CSP hash are out of sync.",
    )
else:
    check(
        False,
        "",
        "index.html: inline suppressor <script> block not found "
        "(expected a plain <script> containing 'unhandledrejection').",
    )

# 7c. inline speculation rules (<script type="speculationrules">)
_m_spec = re.search(r'<script type="speculationrules">(.*?)</script>', _html_nc, re.DOTALL)
if _m_spec is not None:
    _spec_hash = _csp_sri_hash(_m_spec.group(1))
    check(
        f"'{_spec_hash}'" in html,
        f"index.html CSP authorizes inline speculation rules (content hash {_spec_hash})",
        f"index.html CSP does NOT authorize inline speculation rules — computed {_spec_hash} "
        f"is absent from script-src. Chrome will block prerender with "
        f"\"Applying inline speculation rules violates ... script-src\". "
        f"Add '{_spec_hash}' to script-src (recompute if the JSON was edited).",
    )
else:
    warnings.append("index.html: speculationrules block not found — Check 7c skipped")

# ── 8. No X-Content-Type-Options meta ────────────────────────────────────────
check(
    '<meta http-equiv="X-Content-Type-Options"' not in html,
    "index.html: no X-Content-Type-Options meta (header-only control)",
    "index.html: X-Content-Type-Options meta present (must be removed; it's a header-only control)",
)

# ── 9. sitemap.xml valid XML ──────────────────────────────────────────────────
try:
    ET.parse(ROOT / "sitemap.xml")
    print("OK: sitemap.xml valid XML")
except ET.ParseError as e:
    errors.append(f"sitemap.xml XML parse error: {e}")
    print(f"ERROR: sitemap.xml XML parse error: {e}")

# ── 10. .github/scripts/*.py syntax ──────────────────────────────────────────
for py_path in sorted((ROOT / ".github/scripts").glob("*.py")):
    try:
        ast.parse(py_path.read_text(encoding="utf-8"))
        print(f"OK: {py_path.name} — Python syntax valid")
    except SyntaxError as e:
        errors.append(f"{py_path.name}: Python syntax error: {e}")
        print(f"ERROR: {py_path.name}: Python syntax error: {e}")

# ── 11. aio_monitoring.py summary dict ───────────────────────────────────────
check(
    "enabled_engines" in aio_mon,
    "aio_monitoring.py: 'enabled_engines' present in summary",
    "aio_monitoring.py: 'enabled_engines' missing from summary (P0-06)",
)
check(
    "total_cited_count" in aio_mon,
    "aio_monitoring.py: 'total_cited_count' present in summary",
    "aio_monitoring.py: 'total_cited_count' missing from summary (P0-06)",
)


# ── 12. No stale 72回/72回以上 in current-description context ─────────────────
# History records (e2e comments, version history lines) are exempt — we only
# check the files that form the "current description" layer.
CURRENT_DESC_FILES = [
    "index.html", "main.js", "README.md",
    "llms-full.txt", "llms.txt", "llms_well-known.txt",
    "robots.txt",
]
stale_72_hits = []
for fname in CURRENT_DESC_FILES:
    fpath = ROOT / fname
    if not fpath.exists():
        continue
    text = fpath.read_text(encoding="utf-8")
    # Exclude known history-record lines (v73到達時点, history section indicators)
    for lineno, line in enumerate(text.splitlines(), 1):
        if re.search(r"72回(?:以上)?", line):
            # Allowed: clearly a history/version-record line
            if re.search(r"v73到達時点|履歴|history|record|session", line, re.IGNORECASE):
                continue
            stale_72_hits.append(f"{fname}:{lineno}: {line.strip()[:80]}")
check(
    len(stale_72_hits) == 0,
    "No stale '72回/72回以上' in current-description files",
    f"Stale 72回 found in current-description files: {stale_72_hits}",
)

# ── 13. 70超 only in history/log context ─────────────────────────────────────
stale_70_hits = []
for fname in CURRENT_DESC_FILES:
    fpath = ROOT / fname
    if not fpath.exists():
        continue
    text = fpath.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), 1):
        if "70超" in line:
            # Allowed if it's a history/session record
            if re.search(r"履歴|history|record|session|Session Record|Task|v7[0-3]", line, re.IGNORECASE):
                continue
            stale_70_hits.append(f"{fname}:{lineno}: {line.strip()[:80]}")
check(
    len(stale_70_hits) == 0,
    "No current-description '70超' outside history context",
    f"'70超' found outside history context: {stale_70_hits}",
)

# ── 14. v1→v74 / 73 transitions consistency ─────────────────────────────────
has_v74_declaration = "v1→v74" in html or "v1→v74" in ai2ai
check(
    has_v74_declaration,
    "v1→v74 canonical declaration present in index.html or AI2AI.md",
    "v1→v74 canonical declaration missing — add to index.html or AI2AI.md",
)

# ── 15. Project Pages robots/.well-known constraint documented ───────────────
constraint_phrase = "project-scoped"
has_constraint = (
    constraint_phrase in read("llms-full.txt") or
    constraint_phrase in read("AI2AI.md") or
    constraint_phrase in read("README.md")
)
check(
    has_constraint,
    "Project Pages robots/.well-known constraint documented in llms-full.txt / AI2AI.md / README.md",
    "Project Pages robots/.well-known constraint not documented — add explanation to llms-full.txt, AI2AI.md, or README.md",
)

# ── 16. Playwright spec references baseline-skip guard ───────────────────────
spec_path = ROOT / "e2e" / "portfolio.spec.js"
if spec_path.exists():
    spec = spec_path.read_text(encoding="utf-8")
    check(
        "baselineExists" in spec or "test.skip" in spec,
        "e2e/portfolio.spec.js: screenshot test has baseline-skip guard",
        "e2e/portfolio.spec.js: toHaveScreenshot() without baseline-skip guard — add test.skip when no baseline exists",
    )
else:
    print("WARNING: e2e/portfolio.spec.js not found — Playwright spec check skipped")


# ── 17. Date sync: ai:last-modified == SITE_CONFIG.LAST_UPDATED ──────────────
html_date = extract(r'name="ai:last-modified" content="([0-9-]+)"', html)
mainjs_date = extract(r'LAST_UPDATED:\s+[\'"]([0-9-]+)[\'"]' , mainjs)
check(
    html_date is not None and mainjs_date is not None and html_date == mainjs_date,
    f"ai:last-modified ({html_date}) == SITE_CONFIG.LAST_UPDATED ({mainjs_date})",
    f"Date sync mismatch: index.html ai:last-modified={html_date}, main.js LAST_UPDATED={mainjs_date}",
)

# ── 18. sitemap.xml: root <lastmod> == ai:last-modified (per-URL policy) ──────
# Policy (v74 maintenance finalizer):
#   - Root URL (/): lastmod MUST match ai:last-modified / SITE_CONFIG.LAST_UPDATED
#   - AIO document URLs: lastmod may reflect their own update date (honest per-URL)
#   - Binary asset URLs: lastmod may follow asset baseline policy (intentional lag)
#   - Mixed dates across the sitemap are ALLOWED and expected after AIO doc updates
try:
    sitemap_tree = ET.parse(ROOT / "sitemap.xml")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    CANONICAL_ROOT = "https://yutapr0117-design.github.io/portfolio/"
    root_lastmod: str | None = None
    for url_el in sitemap_tree.findall(".//sm:url", ns):
        loc_el = url_el.find("sm:loc", ns)
        lastmod_el = url_el.find("sm:lastmod", ns)
        if loc_el is not None and lastmod_el is not None:
            if loc_el.text and loc_el.text.rstrip("/") == CANONICAL_ROOT.rstrip("/"):
                root_lastmod = lastmod_el.text
                break
    if html_date and root_lastmod is not None:
        check(
            root_lastmod == html_date,
            f"sitemap.xml root <lastmod> ({root_lastmod}) == ai:last-modified ({html_date})",
            f"Date sync: sitemap.xml root lastmod={root_lastmod} vs ai:last-modified={html_date}",
        )
    elif html_date:
        warnings.append("sitemap.xml: root URL entry not found for per-URL lastmod check")
except ET.ParseError:
    pass  # already caught in check 9

# ── 19. sw.js CACHE_NAME matches app version ──────────────────────────────────
sw_js = read("sw.js")
sw_cache = extract(r"CACHE_NAME = 'portfolio-aio-(v\d+)'" , sw_js)
check(
    sw_cache is not None and html_v is not None and sw_cache == html_v,
    f"sw.js CACHE_NAME version ({sw_cache}) == ai:version ({html_v})",
    f"sw.js CACHE_NAME mismatch: sw.js={sw_cache}, index.html ai:version={html_v}",
)

# ── 20. og:image:width / og:image:height / og:image:alt present ──────────────
check(
    'property="og:image:width"' in html,
    "index.html: og:image:width present",
    "index.html: og:image:width missing (add <meta property=og:image:width>)",
)
check(
    'property="og:image:height"' in html,
    "index.html: og:image:height present",
    "index.html: og:image:height missing (add <meta property=og:image:height>)",
)
check(
    'property="og:image:alt"' in html,
    "index.html: og:image:alt present",
    "index.html: og:image:alt missing (add <meta property=og:image:alt>)",
)

# ── 21. llms alias files Last-Updated sync ───────────────────────────────────
llms_date_pattern = r"Last-Updated: ([0-9-]+)"
llms_check_paths = ["llms.txt", ".well-known/llms.txt", "llms_well-known.txt", ".well-known/llms_well-known.txt"]
llms_dates = {}
for p in llms_check_paths:
    fpath = ROOT / p
    if fpath.exists():
        d = extract(llms_date_pattern, fpath.read_text(encoding="utf-8"))
        if d:
            llms_dates[p] = d
if len(set(llms_dates.values())) > 1:
    check(
        False,
        "llms alias files Last-Updated are in sync",
        f"llms alias files Last-Updated mismatch: {llms_dates}",
    )
else:
    d = list(llms_dates.values())[0] if llms_dates else "N/A"
    print(f"OK: llms alias files Last-Updated are in sync ({d})")

# ── 22. AI2AI.md Session Record order: no #10 before #9 ──────────────────────
ai2ai_text = read("AI2AI.md")
import re as _re
header_records = _re.findall(r'^## \[HANDOFF\] Session Record #(\d+)', ai2ai_text, _re.MULTILINE)
record_nums = [int(n) for n in header_records]
order_ok = len(record_nums) == 0 or all(record_nums[i] <= record_nums[i+1] for i in range(len(record_nums)-1))
check(
    order_ok,
    f"AI2AI.md Session Record headers are in ascending order: {record_nums}",
    f"AI2AI.md Session Record headers out of order: {record_nums}",
)


# ── 23. YAML syntax: .github/workflows/*.yml and dependabot.yml ───────────────
try:
    import yaml as _yaml
    yaml_targets = list((ROOT / ".github" / "workflows").glob("*.yml"))
    dep_yml = ROOT / ".github" / "dependabot.yml"
    if dep_yml.exists():
        yaml_targets.append(dep_yml)
    yaml_errors = []
    for ypath in sorted(yaml_targets):
        try:
            _yaml.safe_load(ypath.read_text(encoding="utf-8"))
        except Exception as ye:
            yaml_errors.append(f"{ypath.name}: {ye}")
    check(
        len(yaml_errors) == 0,
        f"All GitHub Actions YAML files parse successfully ({len(yaml_targets)} files)",
        "YAML parse errors: " + "; ".join(yaml_errors),
    )
except ImportError:
    print("WARNING: PyYAML not available — YAML syntax check skipped")
    warnings.append("PyYAML not available — YAML syntax check skipped")


# ── 24. P1-01: llms-full.txt Last-Updated freshness vs AI2AI.md ──────────────
import re as _re2, datetime as _dt
ai2ai_lu_m = _re2.search(r'^Last-Updated\s*:\s*([0-9-]+)', read("AI2AI.md"), _re2.MULTILINE)
llms_full_lu_m = _re2.search(r'^## Last-Updated\n+(\d{4}-\d{2}-\d{2})', read("llms-full.txt"), _re2.MULTILINE | _re2.DOTALL)
# also check header line
llms_full_header_m = _re2.search(r'Last-Updated:\*\*\s*([0-9-]+)', read("llms-full.txt"))
if ai2ai_lu_m and llms_full_lu_m:
    ai2ai_date = _dt.date.fromisoformat(ai2ai_lu_m.group(1))
    llms_full_date = _dt.date.fromisoformat(llms_full_lu_m.group(1))
    diff_days = abs((ai2ai_date - llms_full_date).days)
    check(
        diff_days <= 7,
        f"llms-full.txt Last-Updated ({llms_full_date}) is within 7 days of AI2AI.md Last-Updated ({ai2ai_date})",
        f"llms-full.txt Last-Updated ({llms_full_date}) differs from AI2AI.md Last-Updated ({ai2ai_date}) by {diff_days} days (>7)"
    )
    llms_full_text = read("llms-full.txt")
    has_maintenance = any(f"v{n}" in llms_full_text for n in ["75", "76", "77", "78"])
    if has_maintenance:
        check(
            llms_full_date >= _dt.date(2026, 5, 28),
            f"llms-full.txt Last-Updated ({llms_full_date}) >= 2026-05-28 (v75-v78 content detected)",
            f"llms-full.txt Last-Updated ({llms_full_date}) is stale: v75-v78 content detected but date < 2026-05-28"
        )
else:
    warnings.append("P1-01: Could not parse Last-Updated from AI2AI.md or llms-full.txt")

# ── 25. P1-04: aio-monitoring-log.json evidence_policy key ──────────────────
aio_log_path = ROOT / "docs" / "evidence" / "aio-monitoring-log.json"
if aio_log_path.exists():
    try:
        aio_log = json.loads(aio_log_path.read_text(encoding="utf-8"))
        check(
            "evidence_policy" in aio_log,
            "aio-monitoring-log.json: evidence_policy key present",
            "aio-monitoring-log.json: evidence_policy key missing — add to clarify attempt_log_only status"
        )
    except Exception as _e:
        warnings.append(f"P1-04: Could not parse aio-monitoring-log.json: {_e}")
else:
    warnings.append("P1-04: docs/evidence/aio-monitoring-log.json not found")

# ── 26. P1-02: AI2AI-archive.md max session record == aio-manifest.json role ─
import re as _re
archive_path = ROOT / "docs" / "session-records" / "AI2AI-archive.md"
manifest_path = ROOT / ".well-known" / "aio-manifest.json"
if archive_path.exists() and manifest_path.exists():
    try:
        archive_text = archive_path.read_text(encoding="utf-8")
        nums = [int(m) for m in _re.findall(r"\[HANDOFF\] Session Record #(\d+)", archive_text)]
        manifest_json = json.loads(manifest_path.read_text(encoding="utf-8"))
        archive_role = ""
        for entry in manifest_json.get("supporting_evidence", []):
            if "AI2AI-archive.md" in entry.get("path", ""):
                archive_role = entry.get("role", "")
                break
        m = _re.search(r"#1-#(\d+)", archive_role)
        if nums and m:
            expected_max = max(nums)
            manifest_max = int(m.group(1))
            check(
                expected_max == manifest_max,
                f"aio-manifest.json archive role #1-#{manifest_max} matches AI2AI-archive.md max Session Record #{expected_max}",
                f"aio-manifest.json archive role says #1-#{manifest_max} but AI2AI-archive.md max is #{expected_max}",
            )
        else:
            warnings.append("P1-02: Could not parse session record numbers from archive or manifest role")
    except Exception as _e:
        warnings.append(f"P1-02: Archive session record check failed: {_e}")
else:
    warnings.append("P1-02: AI2AI-archive.md or aio-manifest.json not found")

# ── 27. P1-03: llms-full.txt has no stale C1–C6 in current-description context
llms_full_path = ROOT / "llms-full.txt"
if llms_full_path.exists():
    lf_text = llms_full_path.read_text(encoding="utf-8")
    # Stale C1–C6 patterns that should now read C1–C7 (current constraint envelope)
    stale_patterns = [
        "violates C1\u2013C6",         # "Reject any syntax or pattern that violates C1–C6"
        "C1\u2013C6 constraint envelope",  # "remain within the C1–C6 constraint envelope"
    ]
    found_stale = [p for p in stale_patterns if p in lf_text]
    check(
        len(found_stale) == 0,
        "llms-full.txt: no stale C1\u2013C6 in current-constraint context",
        f"llms-full.txt: stale C1\u2013C6 found (should be C1\u2013C7): {found_stale}",
    )

# ── 28. P0-02: e2e/portfolio.spec.js — no test() nested inside another test() ─
_spec_path_28 = ROOT / "e2e" / "portfolio.spec.js"
if _spec_path_28.exists():
    _spec_lines_28 = _spec_path_28.read_text(encoding="utf-8").splitlines()

    # Verify the 'No Trusted Types' test exists at all
    _has_ttt = any(
        "No Trusted Types or CSP violations in console" in ln
        for ln in _spec_lines_28
    )
    check(
        _has_ttt,
        "e2e/portfolio.spec.js: 'No Trusted Types or CSP violations in console' test exists",
        "e2e/portfolio.spec.js: 'No Trusted Types or CSP violations in console' test is missing",
    )

    # Detect test() nested inside another test() by tracking brace depth.
    # Only top-level test() calls (column 0, matching ^test\() are tracked as test-openers.
    # Parameterised tests inside a for-loop are indented and do NOT match ^test\(,
    # so they are intentionally excluded from this check.
    import re as _re_spec28
    _brace_depth_28 = 0
    _test_start_depth_28 = None   # None = not currently inside a top-level test()
    _nesting_errors_28: list[str] = []

    for _ln28, _line28 in enumerate(_spec_lines_28, 1):
        # A top-level test() definition starts at column 0
        if _re_spec28.match(r"^test\s*\(", _line28):
            if _test_start_depth_28 is not None:
                _nesting_errors_28.append(
                    f"line {_ln28}: test() opened while previous test() "
                    f"(started at brace-depth {_test_start_depth_28}) is not yet closed"
                )
            _test_start_depth_28 = _brace_depth_28  # record depth *before* this line

        # Naive brace counting (works for this file; strings do not contain unbalanced braces)
        _brace_depth_28 += _line28.count("{") - _line28.count("}")

        # When brace depth returns to the level before the test opened, the test is closed
        if _test_start_depth_28 is not None and _brace_depth_28 <= _test_start_depth_28:
            _test_start_depth_28 = None

    check(
        len(_nesting_errors_28) == 0,
        "e2e/portfolio.spec.js: all test() definitions are top-level (no nesting detected)",
        "e2e/portfolio.spec.js: nested test() detected — " + "; ".join(_nesting_errors_28[:3]),
    )
else:
    warnings.append("P0-02: e2e/portfolio.spec.js not found — test-nesting check skipped")

# ── 29. P0-01: Playwright baseline-generation linkage is intact ─────────────
# The baseline generation flow only works if BOTH sides agree on the env signal:
#   - update-playwright-snapshots.yml passes PLAYWRIGHT_UPDATE_SNAPSHOTS
#   - e2e/portfolio.spec.js reads it and does NOT skip the screenshot test in that mode
# Without this, --update-snapshots runs but the skip-guard prevents capture (deadlock).
_snap_wf = ROOT / ".github" / "workflows" / "update-playwright-snapshots.yml"
_spec_29 = ROOT / "e2e" / "portfolio.spec.js"
if _snap_wf.exists() and _spec_29.exists():
    _wf_txt = _snap_wf.read_text(encoding="utf-8")
    _spec_txt = _spec_29.read_text(encoding="utf-8")
    check(
        "PLAYWRIGHT_UPDATE_SNAPSHOTS" in _wf_txt,
        "update-playwright-snapshots.yml: passes PLAYWRIGHT_UPDATE_SNAPSHOTS env",
        "update-playwright-snapshots.yml: PLAYWRIGHT_UPDATE_SNAPSHOTS env missing — baseline generation will skip the screenshot test (P0-01 deadlock)",
    )
    check(
        "PLAYWRIGHT_UPDATE_SNAPSHOTS" in _spec_txt,
        "e2e/portfolio.spec.js: reads PLAYWRIGHT_UPDATE_SNAPSHOTS (baseline-generation mode aware)",
        "e2e/portfolio.spec.js: does not read PLAYWRIGHT_UPDATE_SNAPSHOTS — screenshot test cannot run in baseline-generation mode (P0-01 deadlock)",
    )
    # The screenshot skip-guard must not be closed by baselineExists() alone:
    # it must also allow the snapshot-update mode to bypass the skip.
    _guard_ok = bool(
        re.search(
            r"!baselineExists\([^)]*\)\s*&&\s*!isSnapshotUpdateMode\(\)",
            _spec_txt,
        )
    )
    check(
        _guard_ok,
        "e2e/portfolio.spec.js: screenshot skip-guard combines baselineExists() with isSnapshotUpdateMode()",
        "e2e/portfolio.spec.js: screenshot skip-guard is not gated by isSnapshotUpdateMode() — baseline can never be generated (P0-01 deadlock)",
    )
else:
    warnings.append("P0-01: update-playwright-snapshots.yml or e2e/portfolio.spec.js not found — baseline-linkage check skipped")

# ── 30. v80+ Stage 0/1: architecture maintainability docs are present ────────
# These docs anchor the staged main.js decomposition and the repository update map.
# Their absence means a later AI agent has no extraction/maintainability contract to follow.
for _arch_doc in (
    "docs/architecture/repository-maintainability-map.md",
    "docs/architecture/main-js-extraction-map.md",
):
    check(
        (ROOT / _arch_doc).exists(),
        f"{_arch_doc} present (v80+ maintainability anchor)",
        f"{_arch_doc} missing — v80+ staged maintainability doc absent",
    )

# ── 31. Claude2Claude.md references AI2AI.md's current max Session Record ─────
# Mechanizes the Claude2Claude.md "本文書の更新タイミング" rule: whenever a Session
# Record is appended to AI2AI.md, Claude2Claude.md's 現在状態 MUST be bumped to match.
# Prevents the supporting-evidence adapter note from silently lagging the canonical handoff
# (this exact drift was found and fixed in Session Record #17).
_ai2ai_p31 = ROOT / "AI2AI.md"
_c2c_p31 = ROOT / "Claude2Claude.md"
if _ai2ai_p31.exists() and _c2c_p31.exists():
    import re as _re31
    _ai_nums31 = [int(m) for m in _re31.findall(r"Session Record #(\d+)", _ai2ai_p31.read_text(encoding="utf-8"))]
    _c2c_txt31 = _c2c_p31.read_text(encoding="utf-8")
    if _ai_nums31:
        _max31 = max(_ai_nums31)
        check(
            f"#{_max31}" in _c2c_txt31,
            f"Claude2Claude.md references AI2AI.md current max Session Record #{_max31}",
            f"Claude2Claude.md does not reference AI2AI.md max Session Record #{_max31} — bump its 現在状態 section (Claude2Claude.md 本文書の更新タイミング rule)",
        )
    else:
        warnings.append("Check 31: no Session Record number found in AI2AI.md")
else:
    warnings.append("Check 31: AI2AI.md or Claude2Claude.md not found — Claude2Claude sync check skipped")

# ── 32. index.html JSON-LD blocks are valid JSON (BLOCKING) ──────────────────
# Mechanizes a gap found in Session #18: the checker validated CSP inline-script
# hashes but never parsed the application/ld+json blocks. JSON-LD is the core AIO
# structured-data asset and is hand-edited (e.g. the Zenn subjectOf/citation lists),
# so a stray comma/bracket would ship invalid structured data silently.
import json as _json32
import re as _re32
_idx32 = ROOT / "index.html"
if _idx32.exists():
    _html32 = _idx32.read_text(encoding="utf-8")
    _blocks32 = _re32.findall(
        r'<script type="application/ld\+json">(.*?)</script>', _html32, _re32.DOTALL
    )
    if not _blocks32:
        warnings.append("Check 32: no application/ld+json blocks found in index.html")
    for _i32, _b32 in enumerate(_blocks32):
        try:
            _json32.loads(_b32)
            check(True, f"index.html JSON-LD block #{_i32} parses as valid JSON", "")
        except Exception as _e32:  # noqa: BLE001
            check(False, "", f"index.html JSON-LD block #{_i32} is INVALID JSON: {_e32}")
else:
    warnings.append("Check 32: index.html not found — JSON-LD parse check skipped")

# ── 33. Zenn featuring layers share the same article slug set (BLOCKING) ──────
# Mechanizes the Session #18 Zenn re-selection policy (see repository-maintainability-map.md
# §6). The canonical featured set must appear in EVERY featuring layer, and the PRIMARY
# slug must be present everywhere. Prevents the omission-drift that was present at the
# start of Session #18 (the high-AIO articles #8/#10/#11 were referenced in zero files).
_PRIMARY_SLUG = "5d1d7a7438d48d"
_CANON_SLUGS = {
    "5d1d7a7438d48d", "d99f8171bcf275", "3735dc2683f900", "c82fe055816454",
    "91cf894e1072c6", "27fa4c511cd972", "340dbb85491fc8", "7e18e6ee1577aa",
    "931f6e781d91f8", "49326c5c4e0aae", "6dad78f20f2505",
}
# v80+ Stage 5-m: UI components (HomePage の Zenn featured card list を含む) が
# js/components.js へ抽出された。main.js / js/components.js のどちらかに slug が含まれて
# いれば Zenn featuring 契約は満たされる。検査ロジックも main.js を JS 統合面として扱う。
_ZENN_LAYERS = [
    "robots.txt", "index.html", "main.js", "llms.txt", "llms-full.txt", "README.md",
]
_JS_SHIPPED_AGGREGATE = None  # main.js + js/components.js を 1 度だけ結合
for _layer33 in _ZENN_LAYERS:
    _p33 = ROOT / _layer33
    if _layer33 == "main.js":
        # main.js + js/components.js を結合して検査
        if _JS_SHIPPED_AGGREGATE is None:
            _agg33 = ""
            for _aux33 in (_p33, ROOT / "js" / "components.js"):
                if _aux33.exists():
                    _agg33 += _aux33.read_text(encoding="utf-8") + "\n"
            _JS_SHIPPED_AGGREGATE = _agg33
        _txt33 = _JS_SHIPPED_AGGREGATE
        if not _txt33:
            warnings.append("Check 33: main.js not found — Zenn slug check skipped for it")
            continue
        _layer_label33 = "main.js∪js/components.js"
    elif not _p33.exists():
        warnings.append(f"Check 33: {_layer33} not found — Zenn slug check skipped for it")
        continue
    else:
        _txt33 = _p33.read_text(encoding="utf-8")
        _layer_label33 = _layer33
    _missing33 = sorted(s for s in _CANON_SLUGS if s not in _txt33)
    check(
        not _missing33,
        f"{_layer_label33}: contains all {len(_CANON_SLUGS)} canonical Zenn article slugs",
        f"{_layer_label33}: missing Zenn slug(s) {_missing33} — featuring layers have drifted out of sync (repository-maintainability-map.md §6)",
    )
    check(
        _PRIMARY_SLUG in _txt33,
        f"{_layer_label33}: contains the PRIMARY Zenn slug ({_PRIMARY_SLUG})",
        f"{_layer_label33}: missing the PRIMARY Zenn slug ({_PRIMARY_SLUG})",
    )

# ── 34. honest per-file dating: doc Last-Updated == its sitemap <lastmod> (WARNING) ──
# Mechanizes the "honest dating" policy applied by hand in Session #18: a file's
# declared Last-Updated should equal the lastmod its sitemap entry advertises. WARNING
# (not BLOCKING) because the per-URL lastmod policy legitimately allows mixed dates and
# some docs intentionally lag; this surfaces accidental divergence without breaking CI.
_sitemap34 = ROOT / "sitemap.xml"
if _sitemap34.exists():
    import re as _re34
    _sm34 = _sitemap34.read_text(encoding="utf-8")
    # path-suffix -> declared Last-Updated regex in that file
    _date_docs34 = {
        "llms.txt": r"Last-Updated:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})",
        "llms-full.txt": r"Last-Updated:\*\*\s*([0-9]{4}-[0-9]{2}-[0-9]{2})",
        "AI2AI.md": r"Last-Updated\s*:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})",
    }
    for _suffix34, _re_pat34 in _date_docs34.items():
        _fp34 = ROOT / _suffix34
        if not _fp34.exists():
            continue
        _m_decl = _re34.search(_re_pat34, _fp34.read_text(encoding="utf-8"))
        # find the sitemap <url> block whose <loc> ends with this suffix
        _m_sm = _re34.search(
            r"<loc>[^<]*/" + _re34.escape(_suffix34) + r"</loc>\s*<lastmod>([0-9-]+)</lastmod>",
            _sm34,
        )
        if _m_decl and _m_sm:
            if _m_decl.group(1) != _m_sm.group(1):
                warnings.append(
                    f"Check 34: {_suffix34} declares Last-Updated {_m_decl.group(1)} "
                    f"but sitemap lastmod is {_m_sm.group(1)} (honest-dating divergence)"
                )
            else:
                check(True, f"{_suffix34}: Last-Updated matches sitemap lastmod ({_m_decl.group(1)})", "")
else:
    warnings.append("Check 34: sitemap.xml not found — honest-dating check skipped")

# ── 35. robots.txt advertises the sitemap, and that sitemap exists (BLOCKING) ─
# Configuration self-consistency: a Sitemap: directive that points at a missing or
# wrong-host file silently breaks crawler discovery (AIO + SEO).
_robots35 = ROOT / "robots.txt"
if _robots35.exists():
    import re as _re35
    _rb35 = _robots35.read_text(encoding="utf-8")
    _sm_directive35 = _re35.search(r"(?im)^Sitemap:\s*(\S+)", _rb35)
    check(
        bool(_sm_directive35),
        "robots.txt: advertises a Sitemap: directive",
        "robots.txt: no Sitemap: directive — crawlers cannot discover sitemap.xml",
    )
    if _sm_directive35:
        _sm_url35 = _sm_directive35.group(1)
        check(
            _sm_url35.endswith("/sitemap.xml") and (ROOT / "sitemap.xml").exists(),
            "robots.txt: Sitemap: directive points at the existing sitemap.xml",
            f"robots.txt: Sitemap: directive '{_sm_url35}' does not resolve to an existing sitemap.xml",
        )
else:
    warnings.append("Check 35: robots.txt not found — Sitemap directive check skipped")

# ── 36. sitemap.xml has no future-dated <lastmod> (WARNING) ──────────────────
# A lastmod in the future is an unnatural freshness signal and usually a typo
# (e.g. a transposed year). WARNING so a clock-skew edge case never breaks CI.
if _sitemap34.exists():
    import re as _re36
    from datetime import date as _date36
    _today36 = _date36.today()
    for _lm36 in _re36.findall(r"<lastmod>([0-9]{4}-[0-9]{2}-[0-9]{2})</lastmod>", _sm34):
        try:
            if _date36.fromisoformat(_lm36) > _today36:
                warnings.append(f"Check 36: sitemap.xml has a future-dated <lastmod> {_lm36} (>{_today36})")
        except ValueError:
            warnings.append(f"Check 36: sitemap.xml has a malformed <lastmod> '{_lm36}'")

# ── 37. No generated/cache artifacts are tracked in the repository (BLOCKING) ──
# .gitignore prevents *new* accidental staging, but it does NOT detect artifacts
# that are already tracked, nor ones that slipped into a distributed ZIP. This check
# makes re-introduction a hard CI failure. It judges *repository membership*, so the
# source of truth is `git ls-files` — which correctly ignores the runtime node_modules/
# and __pycache__/ that CI itself creates via `npm ci` / py_compile (a naive os.walk
# would false-positive on those in CI). For non-git contexts (ZIP/zipball export with
# no .git), it falls back to a filesystem walk that prunes those same ignored runtime
# dirs so a local `npm ci` / py_compile in the export cannot cause false positives.
FORBIDDEN_GENERATED_PATH_PARTS = {
    "__pycache__",
    "node_modules",
    "test-results",
    "playwright-report",
    "blob-report",
    ".pytest_cache",
}
FORBIDDEN_GENERATED_NAMES = {
    ".DS_Store",
    "Thumbs.db",
    "npm-debug.log",
}
FORBIDDEN_GENERATED_SUFFIXES = (".pyc", ".pyo")


def _repo_member_paths() -> list[str]:
    """Repo-relative POSIX paths that constitute the repository.

    Prefer `git ls-files` (authoritative: excludes untracked/ignored runtime dirs).
    Fall back to a pruned filesystem walk for ZIP/zipball contexts without .git."""
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=str(ROOT), capture_output=True, timeout=30,
        )
        if proc.returncode == 0 and proc.stdout:
            return [p for p in proc.stdout.decode("utf-8", "replace").split("\0") if p]
    except (OSError, subprocess.SubprocessError):
        pass
    import os as _os37
    _prune = {".git"} | FORBIDDEN_GENERATED_PATH_PARTS
    out: list[str] = []
    for dirpath, dirnames, filenames in _os37.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in _prune]
        for fn in filenames:
            out.append((Path(dirpath) / fn).relative_to(ROOT).as_posix())
    return out


_member_paths = _repo_member_paths()
_artifact_hits = []
for _p in _member_paths:
    _name = _p.rsplit("/", 1)[-1]
    if set(_p.split("/")) & FORBIDDEN_GENERATED_PATH_PARTS:
        _artifact_hits.append(_p)
    elif _name in FORBIDDEN_GENERATED_NAMES:
        _artifact_hits.append(_p)
    elif _p.endswith(FORBIDDEN_GENERATED_SUFFIXES):
        _artifact_hits.append(_p)

check(
    not _artifact_hits,
    f"Check 37: no generated/cache artifacts tracked in repository (scanned {len(_member_paths)} paths)",
    "Check 37: generated/cache artifact(s) present in repository tree — remove from Git and "
    "keep them in .gitignore: " + ", ".join(sorted(_artifact_hits)[:10])
    + (" …" if len(_artifact_hits) > 10 else ""),
    blocking=True,
)

# ── 38. package.json <-> package-lock.json sync (BLOCKING) ────────────────────
# Phase 2-A centralizes dev tooling in package.json + package-lock.json (npm ci).
# These invariants catch a hand-edited lockfile or any drift between the two files,
# and assert the dev-tooling-only contract (private, no runtime dependencies) that
# keeps the published site dependency-free Vanilla JS (Boring Technology).
_pkg_path = ROOT / "package.json"
_lock_path = ROOT / "package-lock.json"
if _pkg_path.exists() and _lock_path.exists():
    try:
        _pkg = json.loads(_pkg_path.read_text(encoding="utf-8"))
        _lock = json.loads(_lock_path.read_text(encoding="utf-8"))
        _lock_root = _lock.get("packages", {}).get("", {})
        _pkg_dev = _pkg.get("devDependencies", {})
        _lock_dev = _lock_root.get("devDependencies", {})
        _pkg_runtime = _pkg.get("dependencies", {})

        check(_lock.get("lockfileVersion") == 3,
              "Check 38: package-lock.json lockfileVersion == 3",
              f"Check 38: package-lock.json lockfileVersion is {_lock.get('lockfileVersion')!r}, expected 3",
              blocking=True)
        check(_lock.get("name") == _pkg.get("name") and _lock_root.get("name") == _pkg.get("name"),
              f"Check 38: lockfile name matches package.json name ({_pkg.get('name')!r})",
              f"Check 38: lockfile name mismatch — package.json={_pkg.get('name')!r} "
              f"lock={_lock.get('name')!r} lock.packages['']={_lock_root.get('name')!r}",
              blocking=True)
        check(_lock.get("version") == _pkg.get("version") and _lock_root.get("version") == _pkg.get("version"),
              f"Check 38: lockfile version matches package.json version ({_pkg.get('version')!r})",
              f"Check 38: lockfile version mismatch — package.json={_pkg.get('version')!r} "
              f"lock={_lock.get('version')!r} lock.packages['']={_lock_root.get('version')!r}",
              blocking=True)
        check(_pkg_dev == _lock_dev,
              "Check 38: package.json devDependencies == package-lock.json root devDependencies",
              f"Check 38: devDependencies drift — package.json={_pkg_dev} vs lock={_lock_dev} "
              "(regenerate with `npm install`; never hand-edit package-lock.json)",
              blocking=True)
        check(_pkg.get("private") is True,
              "Check 38: package.json is private (never published)",
              f"Check 38: package.json 'private' must be true, got {_pkg.get('private')!r}",
              blocking=True)
        check(not _pkg_runtime,
              "Check 38: package.json declares no runtime dependencies (dev-tooling-only manifest)",
              f"Check 38: package.json has runtime dependencies {_pkg_runtime} — the published site "
              "must stay dependency-free (Boring Technology). Keep tools under devDependencies.",
              blocking=True)
    except (ValueError, KeyError) as _e38:
        check(False, "",
              f"Check 38: package.json/package-lock.json parse or structure error: {_e38}",
              blocking=True)
else:
    check(_pkg_path.exists() and _lock_path.exists(),
          "Check 38: package.json and package-lock.json both present",
          "Check 38: package.json and package-lock.json must both exist "
          "(Phase 2-A central dev-dependency management)",
          blocking=True)

# ── 39. sitemap <loc> -> committed file existence (BLOCKING) ──────────────────
# Checks 9/18/34/35/36 cover sitemap XML validity, lastmod policy, and the
# robots Sitemap: directive — but none verify that each advertised URL actually
# resolves to a file in the deployed tree. A sitemap entry without a backing
# file is a real AIO/SEO defect (crawler 404). This gate maps each same-project
# <loc> to its repo-relative path and asserts the file exists.
#   - project base is the GitHub Pages path segment '/portfolio/'
#   - the SPA root ('.../portfolio/') and any trailing-slash path map to index.html
#   - URLs outside the project path are skipped (Check 39 governs local-file
#     integrity only, not external-URL policy)
_sitemap_path = ROOT / "sitemap.xml"
if _sitemap_path.exists():
    _sm_text = _sitemap_path.read_text(encoding="utf-8")
    _sm_missing = []
    _sm_checked = 0
    for _loc in re.findall(r"<loc>\s*(.*?)\s*</loc>", _sm_text):
        if "/portfolio/" not in _loc:
            continue  # external / non-project URL — not a local-file invariant
        _rel = _loc.split("/portfolio/", 1)[1]
        if _rel == "" or _rel.endswith("/"):
            _rel = _rel + "index.html"
        _sm_checked += 1
        if not (ROOT / _rel).exists():
            _sm_missing.append(_rel + "  (<- " + _loc + ")")
    check(
        not _sm_missing,
        f"Check 39: all {_sm_checked} project sitemap <loc> URLs resolve to committed files",
        "Check 39: sitemap.xml advertises URL(s) with no backing file (crawler 404 risk) — "
        "add the file or remove the <loc>: " + "; ".join(sorted(_sm_missing)[:10])
        + (" …" if len(_sm_missing) > 10 else ""),
        blocking=True,
    )

# ── 40. CSS lint execution-path hygiene (BLOCKING) ────────────────────────────
# Phase 2-A centralized dev tooling under package.json + `npm ci`; Phase 2
# CI-hygiene increment #3 (decision-v80-phase2-ci-hygiene-3) then rewired
# check_css_stylelint.py to PREFER the local node_modules/.bin/stylelint binary
# over `npx`, escalating execution/config failures to BLOCKING when stylelint is
# expected to run cleanly. This check guards that contract so a future edit
# cannot silently revert CSS linting to an npx-primary, false-green-prone path:
#   (40a) package.json devDependencies declares "stylelint"
#   (40b) check_css_stylelint.py references the local binary path
#         "node_modules/.bin/stylelint" (local-preferred execution)
#   (40c) the npx path is documented as a *fallback* (not the primary), i.e. the
#         source mentions both "npx" and a fallback rationale.
_pkg40_path = ROOT / "package.json"
_css_checker_path = ROOT / ".github" / "scripts" / "check_css_stylelint.py"
if _pkg40_path.exists() and _css_checker_path.exists():
    try:
        _pkg40 = json.loads(_pkg40_path.read_text(encoding="utf-8"))
        _pkg40_dev = _pkg40.get("devDependencies", {})
        _css_src = _css_checker_path.read_text(encoding="utf-8")
        _css_src_low = _css_src.lower()

        # (40a) stylelint is a managed dev dependency
        check("stylelint" in _pkg40_dev,
              "Check 40a: package.json devDependencies declares 'stylelint' "
              f"({_pkg40_dev.get('stylelint', '?')})",
              "Check 40a: package.json devDependencies is missing 'stylelint' — the CSS "
              "lint gate depends on a pinned, `npm ci`-installed stylelint",
              blocking=True)

        # (40b) checker prefers the local binary installed by `npm ci`
        check("node_modules/.bin/stylelint" in _css_src,
              "Check 40b: check_css_stylelint.py references node_modules/.bin/stylelint "
              "(local-binary-preferred execution)",
              "Check 40b: check_css_stylelint.py does not reference "
              "node_modules/.bin/stylelint — it must prefer the locally installed binary "
              "over npx (reproducibility / no npm-cache false-green)",
              blocking=True)

        # (40c) npx remains only a documented fallback
        check(("npx" in _css_src_low) and ("fallback" in _css_src_low or "falls back" in _css_src_low),
              "Check 40c: check_css_stylelint.py documents npx as a fallback path",
              "Check 40c: check_css_stylelint.py must keep npx as a *documented fallback* "
              "(local binary preferred); the fallback condition is no longer described",
              blocking=True)
    except (ValueError, KeyError) as _e40:
        check(False, "",
              f"Check 40: package.json / check_css_stylelint.py parse or structure error: {_e40}",
              blocking=True)
else:
    check(_pkg40_path.exists() and _css_checker_path.exists(),
          "Check 40: package.json and check_css_stylelint.py both present",
          "Check 40: package.json and .github/scripts/check_css_stylelint.py must both "
          "exist (CSS lint execution-path hygiene contract)",
          blocking=True)

# ── 41. AIO monitoring log ↔ manifest atomic-commit invariant (BLOCKING) ──────
# Root-cause guard for CI hygiene increment #4. docs/evidence/aio-monitoring-log.json
# is registered in aio-manifest.json (observational_evidence) and is therefore a
# BLOCKING digest target (check_aio_digests.py). It is also the one digest-tracked
# file that an automated workflow MUTATES and COMMITS (aio_monitoring.py appends a
# run weekly). If a workflow commits the log WITHOUT regenerating the manifest in
# the SAME commit, the committed log sha and the manifest's recorded sha diverge for
# the window until a separate digest-sync commit lands — and during that window the
# BLOCKING validation can run and red the build. (That is exactly the failure this
# increment fixes.) This check makes the atomic-commit contract machine-enforced:
#   any workflow that stages the monitoring log for commit (git add … + git commit)
#   MUST also run update_aio_digests.py AND stage .well-known/aio-manifest.json,
#   so the log and its digest are always committed together.
_MON_LOG = "aio-monitoring-log.json"
_wf_dir = ROOT / ".github" / "workflows"
if _wf_dir.is_dir():
    for _wf in sorted(_wf_dir.glob("*.yml")):
        _wf_text = _wf.read_text(encoding="utf-8")
        # A workflow "commits the monitoring log" iff it references the log AND both
        # stages (git add) and commits (git commit). Comment-only mentions without a
        # commit do not trip this (conservative — avoids false positives).
        _commits_log = (_MON_LOG in _wf_text) and ("git add" in _wf_text) and ("git commit" in _wf_text)
        if _commits_log:
            _has_regen = "update_aio_digests.py" in _wf_text
            _stages_manifest = "aio-manifest.json" in _wf_text
            check(_has_regen and _stages_manifest,
                  f"Check 41: {_wf.name} commits the monitoring log AND regenerates/stages the "
                  "manifest in the same workflow (atomic log+digest commit)",
                  f"Check 41: {_wf.name} stages '{_MON_LOG}' for commit but does not "
                  "(run update_aio_digests.py AND stage .well-known/aio-manifest.json) in the same "
                  "workflow — the log and its digest must be committed atomically or the BLOCKING "
                  "digest gate will drift (CI hygiene increment #4). "
                  f"[update_aio_digests.py present={_has_regen}, aio-manifest.json staged={_stages_manifest}]",
                  blocking=True)

# ── 42. docs/ artifact placement & naming hygiene (BLOCKING) ──────────────────
# Mechanism that enforces the placement convention documented in docs/README.md.
# The repository convention is: decision records and improvement notes live ONLY
# under docs/incident-artifacts/, and every file directly under that directory
# follows one of the agreed naming patterns. Without a machine check this is just
# tribal knowledge that erodes as files accumulate; this Check turns the written
# rule into an enforced invariant (the repository's discover -> document ->
# systematize philosophy). Two complementary assertions:
#   (42a) every file directly in docs/incident-artifacts/ matches an allowed name
#         pattern (decision-*.md, improvement-notes-*.md, *.yml preserved
#         experiment artifacts, or README.md);
#   (42b) no decision-*.md or improvement-notes-*.md file exists ANYWHERE outside
#         docs/incident-artifacts/ (a misplacement guard).
import fnmatch as _fnmatch

_INCIDENT_DIR = ROOT / "docs" / "incident-artifacts"
_ALLOWED_INCIDENT_PATTERNS = ("decision-*.md", "improvement-notes-*.md", "*.yml", "README.md")

if _INCIDENT_DIR.is_dir():
    # 42a — names inside docs/incident-artifacts/ must match an allowed pattern.
    _bad_named = []
    for _f in sorted(_INCIDENT_DIR.iterdir()):
        if _f.is_file():
            if not any(_fnmatch.fnmatch(_f.name, _pat) for _pat in _ALLOWED_INCIDENT_PATTERNS):
                _bad_named.append(_f.name)
    check(not _bad_named,
          f"Check 42a: all {sum(1 for _f in _INCIDENT_DIR.iterdir() if _f.is_file())} files in "
          "docs/incident-artifacts/ follow an allowed naming pattern "
          "(decision-*.md / improvement-notes-*.md / *.yml / README.md)",
          f"Check 42a: docs/incident-artifacts/ contains file(s) violating the naming convention "
          f"(see docs/README.md): {_bad_named}",
          blocking=True)

    # 42b — decision-*.md / improvement-notes-*.md must not live outside the incident dir.
    _misplaced = []
    for _pat in ("decision-*.md", "improvement-notes-*.md"):
        for _f in ROOT.rglob(_pat):
            # ignore anything under node_modules / .git, and the legitimate incident dir
            _parts = _f.relative_to(ROOT).parts
            if "node_modules" in _parts or ".git" in _parts:
                continue
            if _f.parent != _INCIDENT_DIR:
                _misplaced.append(str(_f.relative_to(ROOT)))
    check(not _misplaced,
          "Check 42b: all decision-*.md / improvement-notes-*.md files live under "
          "docs/incident-artifacts/ (no misplacement)",
          f"Check 42b: decision/improvement-notes file(s) found outside docs/incident-artifacts/ "
          f"(see docs/README.md): {sorted(set(_misplaced))}",
          blocking=True)
else:
    check(False, "",
          "Check 42: docs/incident-artifacts/ directory is missing — the artifact placement "
          "convention (docs/README.md) requires it to exist",
          blocking=True)

# ── 43. main.js AIDK Isolated Kernel structural integrity (BLOCKING) ──────────
# Until now, the AIDK Isolated Kernel ("DO NOT EDIT") was protected only by a code
# comment in main.js and prose in docs/architecture/*. Nothing in CI would catch the
# kernel being deleted, relabeled, or the whole-file IIFE being un-wrapped — yet those
# are precisely the C2/P0-4 invariants the whole orchestration model relies on. This
# check makes the kernel boundary a machine-enforced invariant by asserting the presence
# of the kernel's stable, safety-critical anchors:
#   (43a) the literal "DO NOT EDIT: AIDK Isolated Kernel" header marker,
#   (43b) the startViewTransition proxy installer (View Transition safety device),
#   (43c) the Trusted Types 'default' policy (innerHTML/XSS block, CSP-linked),
#   (43d) a single top-level IIFE wrapper (C2 — no global-namespace pollution).
# These anchors live inside the kernel and are untouched by legitimate AI-SURFACE edits,
# so the check does not false-positive on normal work; it only fires if the kernel itself
# is removed or its wrapper broken. NOTE: this is a *structural presence* invariant, not a
# behavioural audit of kernel logic (that remains a human/orchestrator responsibility).
_mainjs43 = ROOT / "main.js"
if _mainjs43.exists():
    _src43 = _mainjs43.read_text(encoding="utf-8")
    # 43a — kernel demarcation header must remain.
    check("DO NOT EDIT: AIDK Isolated Kernel" in _src43,
          "Check 43a: main.js retains the AIDK Isolated Kernel 'DO NOT EDIT' header marker",
          "Check 43a: main.js is missing the 'DO NOT EDIT: AIDK Isolated Kernel' header — "
          "the kernel demarcation (C2/P0-4) has been removed or relabeled",
          blocking=True)
    # 43b — startViewTransition proxy installer must remain (View Transition safety).
    check("startViewTransitionProxy" in _src43,
          "Check 43b: main.js retains the startViewTransition proxy (View Transition safety device)",
          "Check 43b: main.js is missing the startViewTransition proxy installer — "
          "the kernel's View Transition / ErrorBoundary safety device (C3) is gone",
          blocking=True)
    # 43c — Trusted Types 'default' policy must remain (innerHTML/XSS block, CSP-linked).
    check(("trustedTypes.createPolicy('default'" in _src43)
          or ('trustedTypes.createPolicy("default"' in _src43),
          "Check 43c: main.js retains the Trusted Types 'default' policy (innerHTML/XSS block)",
          "Check 43c: main.js is missing the Trusted Types 'default' policy — "
          "the kernel's innerHTML/XSS defense (C5, CSP-linked) is gone",
          blocking=True)
    # 43d — single top-level IIFE wrapper (C2). Heuristic that tolerates legitimate edits:
    # after stripping line/block comments, the first executable statement must open an IIFE
    # — `(function`/`(()=>`/`(async function`/`!function` — i.e. the global scope is not
    # polluted by top-level declarations. This is intentionally lenient about *which* IIFE
    # form is used so it never blocks a legitimate refactor that keeps the wrapper intact.
    #
    # v80+ staged split: main.js is now an ES module that imports its extracted layers
    # (js/pure-utils.js, js/quiz-data.js) BEFORE running its body in the IIFE. ESM requires
    # `import` to sit at module top level (outside any function), so a module-level import
    # section may now legitimately precede the IIFE. We therefore strip leading `import ...;`
    # statements (alongside the optional "use strict" directive) before looking for the IIFE
    # opener. This does NOT weaken C2: only `import` statements — which create module-scoped
    # bindings, not global-scope pollution — are allowed ahead of the IIFE. Any other
    # top-level construct (a bare `const`/`let`/`var`/`function` declaration, etc.) still
    # leaves a non-IIFE token first and fails the check, exactly as before.
    _nocomments43 = re.sub(r"/\*.*?\*/", "", _src43, flags=re.DOTALL)
    _nocomments43 = re.sub(r"^\s*//.*$", "", _nocomments43, flags=re.MULTILINE)
    _exec43 = _nocomments43.strip()
    # An optional leading "'use strict';" / "\"use strict\";" directive is allowed before the IIFE.
    _exec43 = re.sub(r"^(['\"]use strict['\"]\s*;\s*)+", "", _exec43)
    # Strip any leading ESM import statements (module-scoped, not global pollution).
    # Matches both `import { a, b } from '...';` and `import '...';` forms, repeatedly.
    _exec43 = re.sub(r"^(import\b[^;]*;\s*)+", "", _exec43, flags=re.DOTALL)
    # A "use strict" directive is also legal after the imports; allow it there too.
    _exec43 = re.sub(r"^(['\"]use strict['\"]\s*;\s*)+", "", _exec43)
    _iife_opener43 = re.match(r"^[!+\-~]?\(\s*(async\s+)?(function\b|\()", _exec43)
    check(_iife_opener43 is not None,
          "Check 43d: main.js is wrapped in a single top-level IIFE (C2 — no global namespace pollution; module-level imports may precede it)",
          "Check 43d: main.js does not open with a top-level IIFE — the IIFE wrapper (C2) "
          "appears to have been broken (global namespace pollution risk)",
          blocking=True)
else:
    check(False, "",
          "Check 43: main.js not found — the published SPA entry point is missing",
          blocking=True)

# ── 44. AIO provenance canary token cross-surface consistency (BLOCKING) ──────
# The passive provenance canary is the linchpin of the AIO ingestion experiment: a
# unique token is published in the canonical AIO text, and the monitors search AI
# responses for that exact token (its reproduction is the *only* positive proof of
# ingestion). That design has a single point of silent failure that no other check
# guards: if an edit changes the token on the published side but not in the monitor
# (or vice-versa), the monitor will forever hunt for a string that is no longer
# published — producing permanent false negatives while every existing check stays
# green (Check 4 only proves the four llms mirrors are byte-identical to EACH OTHER;
# it says nothing about llms-full.txt, and nothing about the Python monitors). This
# check closes that gap by asserting one canonical token value across all surfaces:
#   (44a) every published AIO surface contains the token at least once,
#   (44b) every monitor that consumes the token hardcodes the same string,
#   (44c) the repository contains exactly ONE canary value (no drifted variants).
# Like the kernel check, this is a *consistency* invariant, not a claim that the
# canary has been reproduced in the wild (that remains an external observation and is
# deliberately NOT asserted here — see the honesty rule in the runbook).
_CANARY_RE = re.compile(r"SAKURA-AIO-PROVENANCE-CANARY-\d{4}-[0-9A-F]{8}")
# Published AIO surfaces a crawler / LLM actually reads (ground truth + entry + mirrors).
_canary_published = [
    "llms.txt",
    "llms-full.txt",
    ".well-known/llms.txt",
    "llms_well-known.txt",
    ".well-known/llms_well-known.txt",
]
# Monitors that must look for the SAME token they expect to be published.
_canary_monitors = [
    ".github/scripts/aio_monitoring.py",
    ".github/scripts/check_public_deployment_freshness.py",
]
# Collect every canary-shaped token across the whole repo to detect drift (44c).
_canary_values = set()
_canary_present = {}
for _rel in _canary_published + _canary_monitors:
    _p = ROOT / _rel
    if _p.exists():
        _txt = _p.read_text(encoding="utf-8", errors="ignore")
        _hits = _CANARY_RE.findall(_txt)
        _canary_present[_rel] = len(_hits)
        _canary_values.update(_hits)
    else:
        _canary_present[_rel] = -1  # file missing

# 44a — every published surface carries the token.
_missing_pub = [f for f in _canary_published if _canary_present.get(f, -1) < 1]
check(not _missing_pub,
      "Check 44a: the AIO provenance canary token is present on every published surface "
      "(llms.txt + 3 mirrors, llms-full.txt)",
      "Check 44a: the AIO provenance canary token is missing from published surface(s): "
      f"{', '.join(_missing_pub)} — the canary experiment's published anchor is broken",
      blocking=True)

# 44b — every monitor hardcodes the token it is supposed to find.
_missing_mon = [f for f in _canary_monitors if _canary_present.get(f, -1) < 1]
check(not _missing_mon,
      "Check 44b: every AIO monitor hardcodes the canary token it searches for "
      "(aio_monitoring.py, check_public_deployment_freshness.py)",
      "Check 44b: the canary token is absent from monitor(s): "
      f"{', '.join(_missing_mon)} — the monitor would search for a token it never defines",
      blocking=True)

# 44c — exactly one canonical canary value exists repo-wide (no drift between sides).
check(len(_canary_values) == 1,
      "Check 44c: the repository declares exactly one canonical AIO canary token value "
      f"({next(iter(_canary_values)) if len(_canary_values)==1 else 'n/a'})",
      "Check 44c: multiple distinct canary token values found across published/monitor "
      f"surfaces ({sorted(_canary_values)}) — published and searched tokens have drifted "
      "apart, which silently breaks ingestion detection",
      blocking=True)

# ── 45. This file's self-documentation matches its implementation (BLOCKING) ──
# Two hand-maintained descriptions of the check set live in this file: the numbered
# inventory inside the module docstring ("N. ...") and the numbered section-header
# comments in the code body ("# ── N."). They are currently in agreement, but nothing
# stops them from drifting — e.g. a future check added to the body whose inventory line
# is forgotten, or a renumber applied on one side only. If they drift, this file's own
# documentation starts lying about what it enforces, and no other check notices. This
# meta-check makes their agreement an invariant.
#
# Why this is not circular reasoning: we deliberately parse the docstring and the body
# SEPARATELY and compare them to EACH OTHER. The check passes only when the two
# independent descriptions coincide; it cannot pass by "describing itself", because
# Check 45 must appear as a line in BOTH the docstring inventory AND as a body section
# header to be counted on both sides. The assertion is about structural agreement of the
# documentation, never about the behaviour of any individual check.
#
# We read THIS source file from disk (not via introspection) so the check sees exactly
# the committed bytes a reviewer would read.
_selfsrc = (ROOT / ".github" / "scripts" / "check_repository_consistency.py").read_text(encoding="utf-8")
# Isolate the module docstring (first triple-quoted block) from the executable body so
# the two number sets are extracted from genuinely different regions of the file.
_doc_m = re.search(r'"""(.*?)"""', _selfsrc, re.DOTALL)
if _doc_m:
    _docstring45 = _doc_m.group(1)
    _body45 = _selfsrc[_doc_m.end():]
    # Inventory numbers: lines like "  N. " at the top level of the docstring.
    _inv45 = sorted(int(n) for n in re.findall(r'^\s{2}(\d+)\.\s', _docstring45, re.MULTILINE))
    # Section-header numbers: lines like "# ── N." in the body (── = U+2500 box drawing).
    _sec45 = sorted(int(n) for n in re.findall(r'^#\s*\u2500\u2500\s*(\d+)\.', _body45, re.MULTILINE))

    def _contiguous(seq):
        # True when seq is exactly [1, 2, ..., max] with no gaps and no duplicates.
        return bool(seq) and seq == list(range(1, seq[-1] + 1))

    # 45a — the docstring inventory is a clean contiguous 1..N with no gaps/dupes.
    check(_contiguous(_inv45),
          f"Check 45a: docstring check inventory is contiguous 1..{_inv45[-1] if _inv45 else 0} "
          "(no gaps or duplicate numbers)",
          f"Check 45a: docstring check inventory is not a clean 1..N sequence ({_inv45}) — "
          "a check number is missing, duplicated, or out of order in the module docstring",
          blocking=True)
    # 45b — the body section headers are a clean contiguous 1..N with no gaps/dupes.
    check(_contiguous(_sec45),
          f"Check 45b: code section headers are contiguous 1..{_sec45[-1] if _sec45 else 0} "
          "(no gaps or duplicate numbers)",
          f"Check 45b: code section headers are not a clean 1..N sequence ({_sec45}) — "
          "a '# ── N.' header is missing, duplicated, or out of order in the code body",
          blocking=True)
    # 45c — the two descriptions agree: same set of check numbers on both sides.
    check(set(_inv45) == set(_sec45),
          f"Check 45c: docstring inventory and code section headers describe the same "
          f"{len(_sec45)} checks (self-documentation matches implementation)",
          "Check 45c: docstring inventory and code section headers have drifted apart — "
          f"only in docstring: {sorted(set(_inv45) - set(_sec45))}; "
          f"only in code body: {sorted(set(_sec45) - set(_inv45))}",
          blocking=True)
else:
    check(False, "",
          "Check 45: could not locate this file's module docstring to self-verify "
          "documentation/implementation agreement",
          blocking=True)

# ── 46. package.json lint scripts cover a consistent JS file set (BLOCKING) ───
# Adding the `lint:js` (node --check) and `verify` aggregate scripts introduced a new
# hand-maintained duplication: the `lint` script (ESLint) and the `lint:js` script each
# enumerate the project's JavaScript files by name. They describe the SAME underlying
# fact — "which JS files does this project ship and gate?" — in two places. If a future
# JS file is added to one list but not the other, or added to the repo root but to
# neither, lint coverage and syntax-check coverage would silently diverge and a shipped
# file would go ungated. This check makes their agreement an invariant, and ties both to
# the actual top-level *.js files on disk so neither list can quietly fall behind reality.
# We compare THREE sets: lint's files, lint:js's files, and the real root JS files; all
# three must coincide. This is a configuration-consistency invariant (it checks the lint
# wiring, not the JS behaviour, which ESLint/node --check themselves cover).
_pkg_path46 = ROOT / "package.json"
if _pkg_path46.exists():
    _pkg46 = json.loads(_pkg_path46.read_text(encoding="utf-8"))
    _scripts46 = _pkg46.get("scripts", {})
    _lint_cmd46 = _scripts46.get("lint", "")
    _lintjs_cmd46 = _scripts46.get("lint:js", "")
    # `lint` lists files as bare eslint args (before the `--flags`); capture *.js tokens
    # that are NOT part of a flag value. Splitting on the first " --" isolates the file args.
    _lint_args46 = _lint_cmd46.split(" --", 1)[0]
    _lint_files46 = set(re.findall(r"([A-Za-z0-9_./-]+\.js)\b", _lint_args46))
    # `lint:js` lists files as `node --check <file>` clauses.
    _lintjs_files46 = set(re.findall(r"node\s+--check\s+([A-Za-z0-9_./-]+\.js)\b", _lintjs_cmd46))
    # Ground truth: every shipped *.js file on disk = root-level *.js ∪ js/**/*.js.
    # v80+ staged split: extracted modules live under js/ (Stage 2 js/pure-utils.js,
    # Stage 3 js/quiz-data.js, and future Stage 4/5 modules), so the shipped JS surface is
    # no longer root-only. Paths are repo-relative with POSIX separators so they match the
    # script tokens ("main.js", "js/pure-utils.js") regardless of OS. As new js/ modules are
    # extracted, this check automatically REQUIRES them in both lint scripts — lint coverage
    # cannot silently fall behind the split.
    _disk_js46 = {p.name for p in ROOT.glob("*.js") if p.is_file()}
    _disk_js46 |= {p.relative_to(ROOT).as_posix() for p in ROOT.glob("js/**/*.js") if p.is_file()}

    # 46a — lint and lint:js name the same set of JS files.
    check(_lint_files46 == _lintjs_files46,
          "Check 46a: package.json `lint` and `lint:js` scripts cover the same JS file set",
          "Check 46a: package.json `lint` and `lint:js` scripts have drifted apart — "
          f"only in lint: {sorted(_lint_files46 - _lintjs_files46)}; "
          f"only in lint:js: {sorted(_lintjs_files46 - _lint_files46)}",
          blocking=True)
    # 46b — that lint set matches the actual shipped *.js files on disk (root ∪ js/),
    # so no shipped file is ungated and no phantom file is listed. Guards against a new
    # JS file being added to neither script, or a js/ module being left unlinted.
    check(_lint_files46 == _disk_js46,
          "Check 46b: the lint script's JS file set matches the shipped *.js files on disk "
          f"(root ∪ js/ — {len(_disk_js46)} files)",
          "Check 46b: the lint script's JS file set does not match the repository's shipped "
          f"*.js files (root ∪ js/) — only in lint: {sorted(_lint_files46 - _disk_js46)}; "
          f"on disk but unlinted: {sorted(_disk_js46 - _lint_files46)}",
          blocking=True)
else:
    check(False, "",
          "Check 46: package.json not found — cannot verify lint-script JS coverage",
          blocking=True)

# ── 47. main.js ⇄ js/ module ESM import/export contract (BLOCKING) ────────────
# The v80+ staged split physically extracted layers of main.js into local ES modules
# (Stage 2: js/pure-utils.js — pure utilities; Stage 3: js/quiz-data.js — static quiz
# datasets). main.js now `import`s specific names from each module, and each module
# `export`s a set of names. Those lists are a hand-maintained cross-file contract spread
# across three files. Because the site is build-free and served directly by GitHub Pages,
# a mismatch is a *runtime* failure, not a lint nit:
#   - importing a name a module does NOT export → the browser throws a module-load error
#     (e.g. "does not provide an export named 'foo'") and the ENTIRE SPA fails to boot. No
#     other check catches this: node --check validates each file's syntax in isolation; it
#     never cross-checks one file's import names against another file's exports.
#   - an export nothing imports → a harmless but real signal that the split has drifted (a
#     name was removed from main.js's import list but left in the module, or added to the
#     module speculatively). We require an exact bijection per module so the split stays
#     intentional. NOTE: this is precisely the guard that would have caught the Stage 3
#     near-miss in which main.js referenced four quiz datasets (aws/pm/quality/architecture)
#     while an early draft of js/quiz-data.js exported only two — the dangling references
#     would have failed this check immediately.
# Parsing notes (both learned from real bugs while authoring this check):
#   (a) the import lists carry one inline `//` comment per name, so we strip per-line
#       comments BEFORE extracting identifiers — a naive split would read a comment fragment
#       as a name; and
#   (b) the captured brace group is [^{}]*? so each `import {…} from '<module>'` block is
#       matched in isolation and a match cannot span across an adjacent import block (with a
#       greedy/dotall group, the pure-utils block bled into the quiz-data match).
# We also assert each module stays import-free: it is a dependency-free leaf of the module
# graph (Boring Technology — the utility/data layers depend on nothing), so an accidental
# import into one is itself a regression.
# This is a configuration/wiring invariant (it checks the module contract, not the JS
# behaviour, which node --check and the browser cover).
_main_src47 = (ROOT / "main.js").read_text(encoding="utf-8")
# Each tuple: (import specifier as written in main.js, module file path on disk).
# v80+ Stage 3-b: the single js/quiz-data.js was split into four domain leaf modules under
# js/quiz/, each exporting exactly one dataset. The check loops over all module specs, so the
# per-module import/export bijection (47a/47b) and leaf-ness (47c) now cover all four — adding
# or removing a quiz module without wiring main.js's import would fail this check immediately.
# v80+ Stage 4: js/ui-components.js added — DOM builder (h), SVG icon helper (createIcon),
# Toast notification system, and BGM manager extracted as a single leaf module (no local imports).
# All four exports are used in main.js's IIFE; Check 47b enforces bijection.
# v80+ Stage 5: js/router.js (hash-based SPA router) and js/page-meta.js (per-page SEO metadata)
# extracted as leaf modules. Router had one closure dep (CONSTANTS.DEBUG, production dead code)
# which was removed. PAGE_META's dynamic entries are pure functions that accept state/params as
# arguments — no closure deps. Both are leaves (no local imports).
# v80+ Stage 5-b → 5-j fix: js/pages.js (HiringRiskPage / RoleSplitPage / NotFoundPage + 4 helpers)
# was originally extracted with IMPLICIT GLOBAL references to h/createIcon/Router (Stage 5-b).
# That was a hidden ReferenceError bug — ESM module scope doesn't see main.js IIFE bindings,
# so calling the page functions at runtime would throw. Playwright never visited /#/hiring-risk
# or /#/role-split, so CI stayed green and the bug latent. Stage 5-j refactored to the same
# factory pattern as Brand/Store/State/Theme: `createPages({h, createIcon, Router})` accepts
# the dependencies as injected arguments and the closure binds them for the returned page
# functions. main.js destructures the result: `const { HiringRiskPage, RoleSplitPage,
# NotFoundPage } = createPages({ h, createIcon, Router })`. Public usage sites unchanged.
# v80+ Stage 5-c: js/storage.js (Safe localStorage wrapper) extracted as a leaf module. The
# four methods (get/set/remove/parse) operate purely on the (key, value) arguments and the
# global localStorage API — no IIFE closure state, no DOM, no CONSTANTS dependency. The earlier
# extraction-map §3.5 classification "Safe Storage = mid/high risk (schema backward-compat)"
# referred to the callers' contract over localStorage keys/values, not to module-level closure
# deps, so the module itself extracts cleanly. The schema backward-compat responsibility stays
# with the callers (main.js controls all key/value formats).
# v80+ Stage 5-d: js/constants.js (application runtime constants: STORAGE_KEY / LIMITS /
# timing / DEBUG / TAB_ID) extracted as a leaf module. SITE_CONFIG.VERSION/LAST_UPDATED stay
# in main.js (Check 2 / 17 extract them by name from main.js). CONSTANTS only references
# browser globals (crypto, sessionStorage, location, URLSearchParams, Date, Math) — no IIFE
# closure deps. TAB_ID's IIFE side-effect (one-time sessionStorage write) executes once at
# module load, equivalent to its prior one-time evaluation inside main.js's IIFE.
# v80+ Stage 5-e: js/identity.js (AUTHOR: DISPLAY_NAME / AUTHORITATIVE_NAME / JAPANESE_NAME)
# extracted as a leaf module. Pure data with closure-deps = none. Values are byte-equivalent
# and main.js is not in the AIO digest chain, so AI citation / entity identity is unaffected.
# The UI vs AIO dependency-direction contract (UI → DISPLAY_NAME only / AIO → AUTHORITATIVE_NAME)
# stays enforced by the values themselves, not by module location.
# v80+ Stage 5-f: js/brand.js (Brand: primary palette/font manager) extracted via the factory
# pattern. The module exports `createBrand(storage)` rather than a pre-built Brand object —
# main.js composes `const Brand = createBrand(Storage)` to inject the Storage dependency
# while the module itself stays a dependency-free leaf (Check 47c: zero imports). This is the
# canonical pattern for extracting service-rail modules that have logical dependencies on
# other extracted modules without forming a cross-module import graph.
# v80+ Stage 5-g: js/store.js (Store: default data + load/validate/normalize/similarity) extracted
# via the same factory pattern. createStore({AUTHOR, CONSTANTS, Storage, generateId, deepClone,
# slugify, sanitizeUrl, clamp}) accepts all dependencies as injected arguments. The 488-line
# Store IIFE body (defaultProfile / defaultProjects / defaultAppsData + helpers + validation +
# tokenizeForSimilarity local) is preserved byte-equivalent inside the factory. Public API
# {load, createDefaultStore, validateAndNormalize, autoRelatedCandidates} unchanged.
# v80+ Stage 5-h: js/state.js (State: Proxy type-safety monitor + subscriber + cross-tab sync +
# auto-save) extracted via the factory pattern. createState({CONSTANTS, Store, Storage, Toast})
# accepts dependencies as injected arguments. The 209-line State IIFE body (Proxy wrapper /
# subscribe-notify / save debounce / cross-tab storage event listener) is preserved
# byte-equivalent. Public API {get, set, update, subscribe, saveNow} unchanged.
# v80+ Stage 5-i: js/theme.js (Theme: system/dark/light cycle + matchMedia listener) extracted
# via the factory pattern. createTheme({State, Toast}) accepts the State and Toast dependencies.
# The 38-line Theme IIFE body (apply/cycle/init + DOM data-theme attribute + meta theme-color
# + window.matchMedia subscription) is preserved byte-equivalent. Public API {apply, cycle, init}
# unchanged.
# v80+ Stage 5-l: js/meta-management.js (4 SRP sub-functions: updateDocumentHead /
# announceRouteForAccessibility / injectRouteEntityAnchor / injectStructuredData + applyMeta
# facade) extracted via the factory pattern. createMetaManagement({SITE_CONFIG, AUTHOR,
# PAGE_META, Router, State}) accepts dependencies as injected arguments. The 165-line Meta
# Management block (document.head/title/meta/OG/Twitter/canonical/robots + aria-live +
# AIO entity anchor + Article/Speakable JSON-LD) is preserved byte-equivalent. Public API
# {applyMeta} unchanged. EffectRails dispatch and renderer (_renderCore) both call applyMeta
# through the same closure binding.
_modules47 = [
    ("./js/aidk-rails.js",                  ROOT / "js" / "aidk-rails.js"),
    ("./js/apps.js",                        ROOT / "js" / "apps.js"),
    ("./js/brand.js",                       ROOT / "js" / "brand.js"),
    ("./js/components.js",                  ROOT / "js" / "components.js"),
    ("./js/constants.js",                   ROOT / "js" / "constants.js"),
    ("./js/fatal-overlay.js",               ROOT / "js" / "fatal-overlay.js"),
    ("./js/identity.js",                    ROOT / "js" / "identity.js"),
    ("./js/meta-management.js",             ROOT / "js" / "meta-management.js"),
    ("./js/mobile-drawer.js",               ROOT / "js" / "mobile-drawer.js"),
    ("./js/page-meta.js",                   ROOT / "js" / "page-meta.js"),
    ("./js/pages.js",                       ROOT / "js" / "pages.js"),
    ("./js/perf-guards.js",                 ROOT / "js" / "perf-guards.js"),
    ("./js/pure-utils.js",                  ROOT / "js" / "pure-utils.js"),
    ("./js/quiz-renderer.js",               ROOT / "js" / "quiz-renderer.js"),
    ("./js/router.js",                      ROOT / "js" / "router.js"),
    ("./js/state.js",                       ROOT / "js" / "state.js"),
    ("./js/storage.js",                     ROOT / "js" / "storage.js"),
    ("./js/store.js",                       ROOT / "js" / "store.js"),
    ("./js/theme.js",                       ROOT / "js" / "theme.js"),
    ("./js/ui-components.js",               ROOT / "js" / "ui-components.js"),
    ("./js/quiz/architecture-quiz-data.js", ROOT / "js" / "quiz" / "architecture-quiz-data.js"),
    ("./js/quiz/aws-quiz-data.js",          ROOT / "js" / "quiz" / "aws-quiz-data.js"),
    ("./js/quiz/pm-quiz-data.js",           ROOT / "js" / "quiz" / "pm-quiz-data.js"),
    ("./js/quiz/quality-quiz-data.js",      ROOT / "js" / "quiz" / "quality-quiz-data.js"),
]
for _spec47, _mpath47 in _modules47:
    if not _mpath47.exists():
        check(False, "",
              f"Check 47: {_spec47} is missing while main.js may still import from it "
              "(the staged-split module was removed without updating main.js)",
              blocking=True)
        continue
    _msrc47 = _mpath47.read_text(encoding="utf-8")

    # ── Names main.js imports from THIS module ──
    # [^{}]*? keeps the match inside a single import block (cannot span an adjacent block).
    _imp_m47 = re.search(r"import\s*\{([^{}]*?)\}\s*from\s*'" + re.escape(_spec47) + r"'",
                         _main_src47, re.DOTALL)
    _imported47 = set()
    if _imp_m47:
        _block_nc47 = re.sub(r"//[^\n]*", "", _imp_m47.group(1))  # strip inline comments first
        for _tok47 in re.split(r"[,\n]", _block_nc47):
            _name47 = _tok47.strip()
            if re.fullmatch(r"[A-Za-z_$][\w$]*", _name47):
                _imported47.add(_name47)

    # ── Names THIS module exports (function / const / let / var / named-list) ──
    # Supports three ECMAScript export forms:
    #   1. `export function name() ...` / `export async function name() ...`
    #   2. `export const name = ...` / `export let name = ...` / `export var name = ...`
    #   3. `export { name1, name2, name3 };` (named-list, optionally with `as` aliasing)
    # The named-list form is the canonical way to export multiple already-declared
    # identifiers in one statement — js/pages.js uses it at the file tail. Failing to
    # parse it would silently mask import/export drift (this exact gap was caught when
    # js/pages.js was first added to _modules47: Check 47a flagged HiringRiskPage /
    # RoleSplitPage / NotFoundPage as "not exported" because only forms (1) and (2)
    # were recognised). The parser strips per-line comments inside the brace block,
    # handles `as`-aliased re-exports by taking the exposed (right-hand) name, and
    # only accepts valid identifier tokens.
    _exported47 = set(re.findall(r"^export\s+(?:async\s+)?function\s+([A-Za-z_$][\w$]*)",
                                 _msrc47, re.MULTILINE))
    _exported47 |= set(re.findall(r"^export\s+(?:const|let|var)\s+([A-Za-z_$][\w$]*)",
                                  _msrc47, re.MULTILINE))
    for _named_block47 in re.findall(r"^export\s*\{([^{}]*)\}\s*;?", _msrc47, re.MULTILINE):
        _block_nc47 = re.sub(r"//[^\n]*", "", _named_block47)  # strip inline comments
        for _tok47 in re.split(r"[,\n]", _block_nc47):
            _name47 = _tok47.strip()
            # `export { foo as bar }` — bar is the exposed external name
            if re.search(r"\bas\b", _name47):
                _name47 = re.split(r"\s+as\s+", _name47)[-1].strip()
            if re.fullmatch(r"[A-Za-z_$][\w$]*", _name47):
                _exported47.add(_name47)

    _short47 = _spec47.replace("./", "")

    # 47a — every imported name is actually exported (else the SPA fails to boot).
    _missing47 = _imported47 - _exported47
    check(not _missing47,
          f"Check 47a [{_short47}]: every name main.js imports is exported by the module "
          f"({len(_imported47)} names)",
          f"Check 47a [{_short47}]: main.js imports name(s) the module does NOT export: "
          f"{sorted(_missing47)} — this throws a module-load error and the SPA fails to boot",
          blocking=True)

    # 47b — every export is imported (exact bijection; no drifted/orphan exports).
    _orphan47 = _exported47 - _imported47
    check(not _orphan47,
          f"Check 47b [{_short47}]: every name the module exports is imported by main.js "
          "(exact import/export bijection — no orphan exports)",
          f"Check 47b [{_short47}]: the module exports name(s) main.js does not import: "
          f"{sorted(_orphan47)} — the split has drifted; remove the unused export or wire it up",
          blocking=True)

    # 47c — the module stays a dependency-free leaf (no imports of its own).
    _leaf_imports47 = re.findall(r"^\s*import\b", _msrc47, re.MULTILINE)
    check(not _leaf_imports47,
          f"Check 47c [{_short47}]: the module is a dependency-free leaf (imports nothing)",
          f"Check 47c [{_short47}]: the module has {len(_leaf_imports47)} import statement(s) "
          "— extracted leaf layers must not depend on other modules (Boring Technology)",
          blocking=True)

# ── 48. Playwright baseline-commit pipeline permission coupling (BLOCKING) ────
# update-playwright-snapshots.yml was upgraded from "upload an artifact a human
# downloads and commits by hand" to "commit the generated baseline via a pull
# request" — closing the manual last-mile gap that kept the baseline unobtained.
# The PR-creation step (peter-evans/create-pull-request) cannot function unless the
# workflow also grants `contents: write` (push the baseline branch) and
# `pull-requests: write` (open the PR). Those two facts live in the same file but in
# different sections (permissions block at the top, PR step near the bottom), so they
# can silently drift apart. If a later edit reverted the permissions to read-only
# while leaving the PR step in place, the step would fail at runtime with a confusing
# permission error and nothing would catch it beforehand. This check makes the
# coupling explicit and BLOCKING — but only fires the permission requirement WHEN the
# PR step is present, so a legitimate future simplification back to artifact-only
# (which needs no write permissions) is not forbidden. Same spirit as Check 29's
# env-signal linkage between the workflow and the spec.
_snap_wf48 = ROOT / ".github" / "workflows" / "update-playwright-snapshots.yml"
if _snap_wf48.exists():
    _wf48 = _snap_wf48.read_text(encoding="utf-8")
    # The defining marker that this workflow opens a PR: the create-pull-request action.
    _has_pr_step48 = "peter-evans/create-pull-request" in _wf48
    if _has_pr_step48:
        # Both write scopes must be declared as real YAML directives. We anchor the
        # match to line structure (re.MULTILINE: start-of-line, only indentation before
        # the key) so that COMMENT lines mentioning the permission in prose — e.g.
        # "  #   contents: write  — push the branch" — do NOT satisfy the check. A bare
        # substring/loose match would read the workflow's own explanatory comments and
        # be fooled (this was caught by a negative test: reverting the real directives to
        # read-only while the comment still described them must still fail the check).
        _has_contents_write48 = re.search(r"^[ \t]*contents:[ \t]*write\b", _wf48, re.MULTILINE) is not None
        _has_pr_write48 = re.search(r"^[ \t]*pull-requests:[ \t]*write\b", _wf48, re.MULTILINE) is not None
        check(
            _has_contents_write48 and _has_pr_write48,
            "Check 48: update-playwright-snapshots.yml declares contents:write + "
            "pull-requests:write to match its PR-creation step",
            "Check 48: update-playwright-snapshots.yml contains the create-pull-request "
            "step but is missing required permission(s): "
            + ", ".join(
                p for p, ok in (
                    ("contents: write", _has_contents_write48),
                    ("pull-requests: write", _has_pr_write48),
                ) if not ok
            )
            + " — the PR step would fail at runtime",
            blocking=True,
        )
    else:
        # No PR step → artifact-only mode is legitimate and needs no write permissions.
        check(
            True,
            "Check 48: update-playwright-snapshots.yml has no PR-creation step "
            "(artifact-only mode; no write permissions required)",
            "",
            blocking=True,
        )
else:
    warnings.append(
        "Check 48: update-playwright-snapshots.yml not found — baseline-commit "
        "permission-coupling check skipped"
    )

# ── 49. index.html JSON-LD worksFor ↔ Organization linkage integrity (BLOCKING) ─
# The entity-linkage strategy (connect the Person to the established employer so a
# knowledge-graph engine resolves the employment edge to a strong entity) only holds
# if three facts in the first JSON-LD @graph agree:
#   (a) the Person node has a worksFor,
#   (b) that worksFor ultimately references an organization by @id, and
#   (c) an Organization node with that exact @id exists as a sibling in the same graph.
# A dangling reference (worksFor → an @id no node defines) is a SILENT failure: the page
# still renders, the JSON still parses, but the employment edge never resolves, so the
# whole strategy quietly collapses. This check catches that at pre-commit time.
#
# Implementation note: the worksFor value may be EITHER a direct organization reference
# ({"@id": "..."}) OR an OrganizationRole wrapper that nests the organization reference
# one level down ({"@type": "OrganizationRole", "worksFor": {"@id": "..."}}). We resolve
# the referenced @id through both shapes. Real JSON parsing (not regex) is used because
# JSON-LD nesting is exactly what regex handles poorly. We only assert the linkage WHEN a
# worksFor is present, so removing the employer entirely (a legitimate future state) does
# not trip the check.
_html_path49 = ROOT / "index.html"
if _html_path49.exists():
    _html49 = _html_path49.read_text(encoding="utf-8")
    _blocks49 = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', _html49, re.DOTALL
    )
    # The Person/Organization graph lives in the first JSON-LD block.
    if _blocks49:
        try:
            _data49 = json.loads(_blocks49[0])
            _parsed49 = True
        except json.JSONDecodeError as _e49:
            _parsed49 = False
            check(
                False,
                "",
                f"Check 49: index.html first JSON-LD block does not parse as valid JSON — {_e49}",
                blocking=True,
            )

        if _parsed49:
            _graph49 = _data49.get("@graph", []) if isinstance(_data49, dict) else []
            # Collect every @id defined by an Organization node in the graph.
            _org_ids49 = {
                n.get("@id")
                for n in _graph49
                if isinstance(n, dict) and n.get("@type") == "Organization" and n.get("@id")
            }
            # Find the Person node (there should be exactly one authoritative Person).
            _person49 = next(
                (n for n in _graph49 if isinstance(n, dict) and n.get("@type") == "Person"),
                None,
            )

            def _resolve_worksfor_id49(person):
                """Return the org @id a Person's worksFor points at, through either
                a direct {"@id": ...} reference or a nested OrganizationRole wrapper.
                Returns None if there is no worksFor at all."""
                if not person:
                    return ("no-person", None)
                wf = person.get("worksFor")
                if wf is None:
                    return ("no-worksfor", None)
                if isinstance(wf, dict):
                    # Direct reference: {"@id": "..."}
                    if "@id" in wf and wf.get("@type") != "OrganizationRole":
                        return ("ok", wf.get("@id"))
                    # OrganizationRole wrapper: nested worksFor holds the org reference.
                    nested = wf.get("worksFor")
                    if isinstance(nested, dict) and "@id" in nested:
                        return ("ok", nested.get("@id"))
                    # OrganizationRole that itself carries an @id directly.
                    if "@id" in wf:
                        return ("ok", wf.get("@id"))
                return ("malformed", None)

            _status49, _ref_id49 = _resolve_worksfor_id49(_person49)

            if _status49 == "no-person":
                check(
                    False, "",
                    "Check 49: index.html first JSON-LD @graph has no Person node — "
                    "cannot verify worksFor linkage",
                    blocking=True,
                )
            elif _status49 == "no-worksfor":
                # No employer declared. Legitimate state — nothing to enforce.
                check(
                    True,
                    "Check 49: Person has no worksFor (no employer linkage to verify)",
                    "",
                    blocking=True,
                )
            elif _status49 == "malformed":
                check(
                    False, "",
                    "Check 49: Person.worksFor exists but exposes no resolvable organization "
                    "@id (neither a direct {@id} reference nor a nested OrganizationRole.worksFor.@id)",
                    blocking=True,
                )
            else:
                # worksFor resolves to a concrete @id — that Organization must exist.
                check(
                    _ref_id49 in _org_ids49,
                    f"Check 49: Person.worksFor @id '{_ref_id49}' resolves to an Organization "
                    "node present in the same @graph (worksFor ↔ Organization linkage intact)",
                    f"Check 49: Person.worksFor references organization @id '{_ref_id49}' but no "
                    f"Organization node with that @id exists in the @graph (defined org @ids: "
                    f"{sorted(i for i in _org_ids49 if i)}) — dangling employment edge",
                    blocking=True,
                )
    else:
        warnings.append(
            "Check 49: no JSON-LD block found in index.html — worksFor linkage check skipped"
        )
else:
    warnings.append(
        "Check 49: index.html not found — worksFor linkage check skipped"
    )

# ── 50. ESLint flat-config migration integrity (BLOCKING) ─────────────────────
# The lint toolchain migrated off EOL ESLint 8.x / eslintrc onto flat config (9.x default, now v10).
# Guard the migration so it cannot silently regress:
#   50a — eslint.config.mjs (the flat config ESLint 9.x auto-discovers) exists at root.
#   50b — the package.json `lint` script carries none of the removed eslintrc-era flags
#         (--no-eslintrc / --config .eslintrc.json / --env), whose presence makes ESLint 9.x
#         exit 2 (the historical vacuous-gate failure mode).
#   50c — the legacy .eslintrc.json is absent (its return would invite an EOL-format regression).
_flat_cfg50 = ROOT / "eslint.config.mjs"
check(
    _flat_cfg50.is_file(),
    "Check 50a: eslint.config.mjs (flat config) exists at repository root",
    "Check 50a: eslint.config.mjs is missing — ESLint 9.x would run with no configuration "
    "and pass vacuously. The flat config is the sole config ESLint auto-discovers since the "
    "migration off the EOL eslintrc format.",
)
_pkg_path50 = ROOT / "package.json"
if _pkg_path50.is_file():
    try:
        _scripts50 = json.loads(_pkg_path50.read_text(encoding="utf-8")).get("scripts", {})
        _lint_cmd50 = _scripts50.get("lint", "")
        _legacy_flags50 = ["--no-eslintrc", "--config .eslintrc.json", "--env "]
        _found_legacy50 = [f for f in _legacy_flags50 if f in _lint_cmd50]
        check(
            not _found_legacy50,
            "Check 50b: package.json `lint` script uses flat-config invocation (no eslintrc-era flags)",
            "Check 50b: package.json `lint` script still contains legacy ESLint 8.x/eslintrc flags "
            f"{_found_legacy50} — ESLint 9.x removed these and would exit 2 (config/flag error). "
            "Flat config is auto-discovered from eslint.config.mjs; remove the legacy flags.",
        )
    except (ValueError, KeyError) as _e50:
        check(
            False,
            "Check 50b: package.json `lint` script parseable",
            f"Check 50b: could not parse package.json scripts to verify flat-config lint invocation: {_e50}",
        )
else:
    check(
        False,
        "Check 50b: package.json present for flat-config lint-script verification",
        "Check 50b: package.json not found — cannot verify the lint script uses flat-config invocation.",
    )
check(
    not (ROOT / ".eslintrc.json").exists(),
    "Check 50c: legacy .eslintrc.json is absent (fully migrated to flat config)",
    "Check 50c: .eslintrc.json still exists — the repository migrated to ESLint 9.x flat config "
    "(eslint.config.mjs), and the EOL eslintrc file should be removed to prevent a regression "
    "back onto the unsupported format.",
)

# ── 51. Active-runbook Playwright baseline-generation version matches the pin (BLOCKING) ──
# Playwright の視覚回帰 baseline PNG は、それを生成した Playwright（＝同梱 Chromium）の
# バージョンに依存する。CI（playwright-regression.yml / update-playwright-snapshots.yml）は
# package-lock.json に固定された @playwright/test を `npm ci` で厳密復元して使うため、baseline は
# 実質その pin バージョンで生成・比較される。ところが「baseline はどの版で生成すべきか」という
# *運用指示* は active runbook（total-check-runbook.md §7.4）に自然言語で書かれており、pin
# （package.json）とは別の場所にある。このため依存近代化で pin を bump したとき、runbook 側の
# 版数記述だけが取り残されて *ドリフト* しうる。実際 1.49.1→1.55.1→1.60.0 と bump する過程で
# runbook が「1.55.1 で生成」のまま残った履歴があり、これは人間が誤った版で baseline を生成し
# CI（pin 版）との間に偽の視覚差分を生む運用事故クラスである。
#
# 本チェックは、active runbook が baseline 生成手順で名指しする具体 Playwright 版数（X.Y.Z）を
# 一つ残らず抽出し、そのすべてが package.json の @playwright/test pin と一致することを BLOCKING で
# 強制する。runbook が具体版数を一つも名指ししない場合は vacuous に成立する（ただし pin 自体が
# 読めることは要求）。対象は active runbook のみ——decision 記録（docs/incident-artifacts/*）は
# 「その increment 時点の事実」を残す append-only な歴史であり後発 bump で遡及修正しない（歴史を
# 壊さない）ため対象外、repository-maintainability-map.md も版数進化（1.49.1→1.55.1→1.60.0）の
# 物語を層として保持するため対象外とし、運用上 single-source となる runbook の指示だけを pin に
# 拘束する。Check 48（baseline コミット経路の権限結合）/ Check 29（baseline 生成リンク）と同じ、
# latent な運用事故を pre-commit で顕在化させる思想。
_pkg51 = ROOT / "package.json"
_runbook51 = ROOT / "docs" / "architecture" / "total-check-runbook.md"
if _pkg51.is_file() and _runbook51.is_file():
    try:
        _pw_pin51 = (
            json.loads(_pkg51.read_text(encoding="utf-8"))
            .get("devDependencies", {})
            .get("@playwright/test", "")
        )
        _runbook_text51 = _runbook51.read_text(encoding="utf-8")
        # active runbook 中の「Playwright」直後に来る 3 部構成バージョン（X.Y.Z）のみを重複なく
        # 抽出する。半角・全角スペース双方を許容。版数を伴わない「Playwright 視覚回帰」「Playwright
        # は外部バイナリ依存」等の言及は拾わない（運用版数指示のみを対象化する）。
        _pw_versions51 = sorted(set(re.findall(r"Playwright[ \u3000]+(\d+\.\d+\.\d+)", _runbook_text51)))
        _mismatched51 = [v for v in _pw_versions51 if v != _pw_pin51]
        check(
            bool(_pw_pin51) and not _mismatched51,
            "Check 51: total-check-runbook.md の baseline 生成 Playwright 版数 "
            f"{_pw_versions51 or '（具体版数の名指しなし）'} が package.json の @playwright/test "
            f"pin（{_pw_pin51}）と一致",
            "Check 51: total-check-runbook.md が baseline 生成版数として "
            f"{_mismatched51} を名指ししているが、package.json の @playwright/test pin は "
            f"{_pw_pin51!r} である。視覚回帰 baseline は生成 Playwright（Chromium）版に依存するため、"
            "active runbook の生成版数指示は pin と一致させること（pin を bump したら runbook も同期）。"
            "decision 記録は歴史として版数差を残してよいが、active runbook の運用指示は pin に追従する。",
        )
    except (ValueError, KeyError) as _e51:
        check(
            False,
            "Check 51: package.json/runbook を版数整合検査のため読めた",
            f"Check 51: Playwright 版数整合の検査中に package.json/runbook の解析に失敗した: {_e51}",
        )
else:
    check(
        False,
        "Check 51: 版数整合検査に必要な package.json/runbook が存在",
        "Check 51: package.json または docs/architecture/total-check-runbook.md が見つからず、"
        "baseline 生成 Playwright 版数と @playwright/test pin の一致を検証できない。",
    )

# ── 52. File-size budget advisory (ADVISORY / non-blocking) ──────────────────
# Bloat-governance counterpart to the v80+ staged split. We parse the machine-readable
# BUDGET-DATA block embedded in docs/architecture/file-size-budget.md and, for every file
# whose budget is a concrete integer, assert its current line count is at or below that
# budget. The budget is single-source in that doc (as-decided by the owner); this check only
# reads and compares — it never hardcodes a line number, mirroring the "documentation must
# match reality" philosophy of Check 44/45/47 but applied to line budgets. It is deliberately
# NON-BLOCKING: protected AIO canon and archive/evidence files are recorded with budget "-"
# (no ceiling) because growth there is itself valuable, and even a concrete over-budget only
# raises a warning a human reviews — never a CI failure that would block a justified increase
# (a new safety comment, a new archive entry). main.js carries a strong-advisory ceiling the
# owner treats as near-hard, so its growth is the one this check most actively surfaces.
# Line-count convention: number of "\n" + 1, matching `wc -l`+1 for files without a trailing
# newline and `wc -l` for files that end in a newline (we count lines, not newline characters).
_budget_doc52 = ROOT / "docs" / "architecture" / "file-size-budget.md"
if _budget_doc52.exists():
    _btext52 = _budget_doc52.read_text(encoding="utf-8")
    # The budget block is an HTML comment so it never renders in the Markdown, yet stays
    # diff-visible and parseable. Each data line: "<repo-relative-path> | <budget|-> | <kind>".
    _bm52 = re.search(r"<!--\s*BUDGET-DATA(.*?)-->", _btext52, re.DOTALL)
    if _bm52:
        _over52: list[str] = []
        _missing52: list[str] = []
        _checked52 = 0
        for _raw52 in _bm52.group(1).strip().split("\n"):
            _line52 = _raw52.strip()
            if not _line52 or _line52.startswith("#"):
                continue  # allow blank lines and "# ..." comments inside the block
            _parts52 = [p.strip() for p in _line52.split("|")]
            if len(_parts52) < 3:
                continue
            _path52, _limit52, _kind52 = _parts52[0], _parts52[1], _parts52[2]
            if _limit52 in ("-", "none", "n/a", ""):
                continue  # protected / archive-growth-ok rows carry no ceiling
            try:
                _limit_n52 = int(_limit52)
            except ValueError:
                continue
            _fp52 = ROOT / _path52
            if not _fp52.exists():
                _missing52.append(_path52)
                continue
            _actual52 = _fp52.read_text(encoding="utf-8").count("\n") + 1
            _checked52 += 1
            if _actual52 > _limit_n52:
                _over52.append(f"{_path52} ({_actual52} lines > budget {_limit_n52}; {_kind52})")
        # 52 — advisory only (blocking=False): warns but never fails CI.
        _msg_fail52_parts = []
        if _over52:
            _msg_fail52_parts.append("over advisory line budget: " + "; ".join(_over52))
        if _missing52:
            _msg_fail52_parts.append("budgeted file(s) missing on disk: " + ", ".join(_missing52))
        check(
            not _over52 and not _missing52,
            f"Check 52: all {_checked52} budgeted files are within their advisory line budget "
            "(file-size-budget.md)",
            "Check 52 (ADVISORY): " + " | ".join(_msg_fail52_parts)
            + " — review docs/architecture/file-size-budget.md (advisory, not blocking)",
            blocking=False,
        )
    else:
        check(
            False, "",
            "Check 52 (ADVISORY): docs/architecture/file-size-budget.md has no parseable "
            "<!-- BUDGET-DATA ... --> block (advisory, not blocking)",
            blocking=False,
        )
else:
    check(
        False, "",
        "Check 52 (ADVISORY): docs/architecture/file-size-budget.md is missing — the "
        "file-size budget is not recorded (advisory, not blocking)",
        blocking=False,
    )

# ── 53. index.html modulepreload href resolution (BLOCKING) ───────────────────
# Every <link rel="modulepreload" href="..."> in index.html must point to a file that
# actually exists in the repository. Directly systematizes the dangling-preload 404 class:
# when js/quiz-data.js was split into js/quiz/*.js, the modulepreload hint kept pointing at
# the deleted module, producing a console 404 on every page load. A modulepreload to a
# non-existent module is always a defect (a guaranteed 404), so this is BLOCKING. Scope:
# same-origin repo-relative hrefs (./js/..., js/..., /portfolio/js/...). Absolute cross-origin
# preloads (e.g. the github.io webp) are out of scope (not resolvable against the working tree).
_index53 = read("index.html")
_preload_hrefs53 = re.findall(r'<link\s+rel="modulepreload"\s+href="([^"]+)"', _index53)
_dangling53: list[str] = []
for _href53 in _preload_hrefs53:
    _h53 = _href53.strip()
    if _h53.startswith(("http://", "https://", "//")):
        continue  # absolute / cross-origin preload — out of scope
    _rel53 = _h53.lstrip("/")
    if _rel53.startswith("portfolio/"):
        _rel53 = _rel53[len("portfolio/"):]
    if _rel53.startswith("./"):
        _rel53 = _rel53[2:]
    if not (ROOT / _rel53).is_file():
        _dangling53.append(_href53)
check(
    not _dangling53,
    f"Check 53: all {len(_preload_hrefs53)} index.html modulepreload href(s) resolve to existing files",
    "Check 53: index.html declares modulepreload href(s) that do not exist on disk — "
    f"{_dangling53}; a dangling modulepreload causes a guaranteed 404 on page load "
    "(update the hint when the module is renamed/split/removed)",
)

# ── 54. ESLint <-> @eslint/js major-version coupling (BLOCKING) ───────────────
# package.json's `eslint` and `@eslint/js` devDependencies must share the same MAJOR version.
# ESLint v10 reorganised how the recommended-config package resolves; a major mismatch
# (e.g. eslint 10.x with @eslint/js 9.x) causes a duplicate/incompatible install and a
# config-resolution conflict. They version independently WITHIN a major (eslint 10.4.1 pairs
# with @eslint/js 10.0.1), so this compares the major only, not exact equality.
_pkg54 = json.loads(read("package.json"))
_dd54 = _pkg54.get("devDependencies", {})
_eslint_v54 = _dd54.get("eslint", "")
_eslintjs_v54 = _dd54.get("@eslint/js", "")


def _major54(spec):
    m = re.search(r"(\d+)\.", spec.lstrip("^~>=< "))
    return m.group(1) if m else None


_em54 = _major54(_eslint_v54)
_jm54 = _major54(_eslintjs_v54)
check(
    _em54 is not None and _jm54 is not None and _em54 == _jm54,
    f"Check 54: eslint ({_eslint_v54}) and @eslint/js ({_eslintjs_v54}) share major version {_em54}",
    f"Check 54: eslint ({_eslint_v54}) and @eslint/js ({_eslintjs_v54}) have mismatched major "
    "versions — pin @eslint/js to the same major as eslint (a mismatch causes ESLint v10 "
    "config-resolution conflicts)",
)

# ── 55. CI lint-target authoritative coupling (BLOCKING) ──────────────────────
# Stage 5-j で発見した「ESLint vacuous-gate 再来」を構造的に防ぐ。
# .github/workflows/architecture-validation.yml の ESLint scan は
# `LINT_TARGET="js/**/*.js main.js ..."` を bash で展開して `npx eslint` に渡す。
# bash の **globstar が無効** な状態だと `js/**/*.js` は `js/<dir>/<file>.js`
# (2 階層) のみマッチし、`js/<file>.js` (直下) が **silently skip** される。
# これが Stage 5-j の hidden ReferenceError (js/pages.js の `h` 未定義) を
# 何週間も lint で検出できなかった根本原因。
# 本 Check は workflow YAML を grep し、(a) ESLint/node --check が `shopt -s
# globstar` を有効化しているか、または (b) `npm run lint` / `npm run lint:js`
# を呼んでいるか、のいずれかを満たすことを BLOCKING で機械強制する。
# どちらでも単一 SoT (package.json の lint script) と一致する lint 対象が保証される。
_wf55 = ROOT / ".github" / "workflows" / "architecture-validation.yml"
if _wf55.exists():
    _wfsrc55 = _wf55.read_text(encoding="utf-8")
    # node --check section: identify by the comment marker that names the step
    _has_globstar55 = "shopt -s globstar" in _wfsrc55
    _uses_npm_lint55 = ("npm run lint:js" in _wfsrc55) or ("npm run lint" in _wfsrc55)
    # 古い独自 LINT_TARGET expansion が残っているなら、globstar かつ npm が無いと vacuous
    _has_raw_target55 = 'LINT_TARGET="js/**/*.js' in _wfsrc55 or 'LINT_TARGET="js/**' in _wfsrc55
    _vacuous55 = _has_raw_target55 and not (_has_globstar55 or _uses_npm_lint55)
    check(
        not _vacuous55,
        "Check 55: architecture-validation.yml lint targets are authoritatively coupled "
        "(npm run lint:js, or globstar-enabled glob — Stage 5-j vacuous-gate prevention)",
        "Check 55: architecture-validation.yml ESLint/node --check uses `js/**/*.js` without "
        "`shopt -s globstar` and without `npm run lint(:js)` — direct js/<file>.js leaves "
        "would be silently skipped. Either enable globstar (`shopt -s globstar`) or call the "
        "package.json lint scripts (single source of truth). See Stage 5-j incident.",
    )
else:
    warnings.append(
        "Check 55: architecture-validation.yml not found — cannot verify lint-target coupling"
    )

# ── 56. js/ leaf modules: factory pattern parameter coverage (BLOCKING) ───────
# Stage 5-j で発見した js/pages.js (元 Stage 5-b) の hidden ReferenceError は、
# 葉モジュール内の関数本体が IIFE 外スコープのバインディング (h, createIcon,
# Router) を未定義の暗黙グローバルとして参照していたために起きた。
# factory pattern (createFoo({deps}) → instance) で抽出すれば、deps が
# factory 引数で bind されるため安全だが、これは構造的に強制されていなかった。
#
# 本 Check は js/ 配下の各葉モジュール（_modules47）について、main.js での
# 使用パターンが以下のいずれかに該当することを検査する:
#   (A) 値 export (`export const Foo = ...` / `export function Foo() {...}` /
#       `export { Foo }`) → main.js は `import { Foo }` で取得・直接使用
#   (B) factory export (`export function createFoo(deps)` / `export function
#       createXxx(deps)`) → main.js は `import { createFoo }` で取得し
#       `const Foo = createFoo({...})` で合成
#
# (A) は closure-deps = none が前提（葉契約 = Check 47c で機械強制）。
# (B) は deps を引数で受けるため、葉契約を破らずに service-rail 結合を表現できる。
#
# 本 Check は「main.js の使用形式と module の export 形式の一致」を検査する:
# - module が `createFoo` を export しているのに main.js が `const X = createFoo(...)`
#   していない → 引数注入忘れ → 関数実行時 ReferenceError 危険
# - 逆に module が `Foo` を直接 export しているのに main.js が `createFoo(...)`
#   している → 構文 error (call on object)
_factory_usage_mismatches = []
for _spec56, _mpath56 in _modules47:
    if not _mpath56.exists():
        continue
    _msrc56 = _mpath56.read_text(encoding="utf-8")
    # factory pattern? `export function createXxx({ ... })` がある
    # 「createXxx」かつ「先頭引数が destructured object `{`」のもののみを factory とみなす。
    # 単純な純粋関数 `export function createIcon(name, size)` は factory ではない（false positive 防止）。
    _factory_re56 = re.search(r"^export\s+function\s+(create[A-Z][A-Za-z0-9_]*)\s*\(\s*\{",
                              _msrc56, re.MULTILINE)
    _short56 = _spec56.replace("./", "")
    if _factory_re56:
        _factory_name56 = _factory_re56.group(1)
        # main.js で `const ... = createXxx(...)` という使用形式があるはず
        _usage_re56 = re.search(
            r"\b" + re.escape(_factory_name56) + r"\s*\(",
            _main_src47,
        )
        if not _usage_re56:
            _factory_usage_mismatches.append(
                f"{_short56}: exports factory `{_factory_name56}` but main.js never calls it"
            )
_factory_count56 = sum(
    1 for _spec, _path in _modules47
    if _path.exists()
    and re.search(r"^export\s+function\s+create", _path.read_text(encoding="utf-8"), re.MULTILINE)
)
check(
    not _factory_usage_mismatches,
    f"Check 56: factory-pattern modules in js/ are all invoked from main.js "
    f"({_factory_count56} factories detected)",
    f"Check 56: factory-pattern module(s) exported but not invoked from main.js: "
    f"{_factory_usage_mismatches} — this is the Stage 5-j class of bug (extracted module's "
    f"functions would throw ReferenceError when called because dependencies are never bound). "
    f"Either invoke the factory in main.js or remove the orphan export.",
)

# ── 57. index.html modulepreload ↔ _modules47 set equality (BLOCKING) ─────────
# 葉モジュール抽出が進むほど、(a) index.html の modulepreload リスト、(b) _modules47
# リスト、(c) package.json の lint/lint:js リスト、の 3 つの集合を同期させ続ける運用
# 規律が重要になる。Check 46 が (b) ↔ (c) を、Check 53 が (a) の href 解決を機械強制して
# いるが、(a) ↔ (b) の集合一致は未強制だった。本 Check で (a) と (b) の対称差を 0 に
# 機械強制し、modulepreload 漏れ／余計 preload を pre-commit で即検出する。
_idx57 = ROOT / "index.html"
if _idx57.exists():
    _html57 = _idx57.read_text(encoding="utf-8")
    _preload57 = set(re.findall(r'<link\s+rel="modulepreload"\s+href="\.?/?(js/[^"]+\.js)"', _html57))
    _modules57 = {spec.replace("./", "") for spec, _ in _modules47}
    _only_preload57 = sorted(_preload57 - _modules57)
    _only_modules57 = sorted(_modules57 - _preload57)
    check(
        not _only_preload57 and not _only_modules57,
        f"Check 57: index.html modulepreload ({len(_preload57)}) and _modules47 ({len(_modules57)}) "
        f"are exact set-equal",
        f"Check 57: modulepreload ↔ _modules47 drift — only in modulepreload: "
        f"{_only_preload57}; only in _modules47: {_only_modules57}",
    )
else:
    warnings.append("Check 57: index.html not found — modulepreload set check skipped")

# ── 58. e2e ALL_ROUTES ↔ main.js switch case set equality (BLOCKING) ──────────
# Stage 5-j で発見した「未訪問ルートに残る hidden runtime error」class を構造的に閉じる
# ため、e2e/portfolio.spec.js の ALL_ROUTES に列挙されたルート名と、main.js の renderer
# switch 内の `case '<name>':` 列の集合を完全一致させる。新ルートを main.js に追加した
# が e2e に追加し忘れた場合（テスト未カバレッジ）や、main.js から削除したルートが e2e に
# 残った場合（404 fallback テスト）の drift を pre-commit でブロック。
# 注: e2e の ALL_ROUTES には 'not-found-fallback' のような alias を持つ要素があるので、
# それは main.js 側の 'not-found' と等価とみなす特例マップを持つ。
_spec58 = ROOT / "e2e" / "portfolio.spec.js"
_main58 = ROOT / "main.js"
if _spec58.exists() and _main58.exists():
    _ssrc58 = _spec58.read_text(encoding="utf-8")
    _msrc58 = _main58.read_text(encoding="utf-8")
    # ALL_ROUTES = [ { hash: '#/<name>', name: '<name>' }, ... ]
    _e2e_routes58 = set(re.findall(r"name:\s*'([a-z][a-z0-9-]*)'", _ssrc58))
    # main.js switch case '<name>':
    _main_routes58 = set(re.findall(r"case\s+'([a-z][a-z0-9-]+)'\s*:", _msrc58))
    # alias map: e2e label → main switch label
    _alias58 = {"not-found-fallback": "not-found"}
    _e2e_normalized58 = {(_alias58.get(r, r)) for r in _e2e_routes58}
    # 'home' は main.js では default ではなく case 'home' があるので、両者で含まれていればOK
    # main.js には 'home' / 'projects' / 'project-detail' / 'apps' / 'app-task' 等がある
    # ただし e2e は project-detail を別途専用テスト（slug 付き）で扱うため、e2e ALL_ROUTES
    # には 'project-detail' を含めない設計（PR #32 で確定済み）。両側からこれを除外。
    _drop58 = {"project-detail"}
    _e2e_set58 = _e2e_normalized58 - _drop58
    _main_set58 = _main_routes58 - _drop58
    _only_e2e58 = sorted(_e2e_set58 - _main_set58)
    _only_main58 = sorted(_main_set58 - _e2e_set58)
    check(
        not _only_e2e58 and not _only_main58,
        f"Check 58: e2e ALL_ROUTES ({len(_e2e_set58)}) and main.js switch cases "
        f"({len(_main_set58)}) are exact set-equal (project-detail を除く)",
        f"Check 58: e2e ↔ main.js route drift — only in e2e: {_only_e2e58}; "
        f"only in main.js: {_only_main58} — every shipped route MUST be exercised by e2e "
        f"to prevent the Stage 5-j hidden-ReferenceError class",
    )
else:
    warnings.append("Check 58: e2e/portfolio.spec.js or main.js not found — route set check skipped")

# ── 59. file-size-budget §2 表 ↔ §4 BUDGET-DATA 集合一致 (BLOCKING) ────────────
# file-size-budget.md は「人間可読 §2 表」と「機械可読 §4 BUDGET-DATA」の二段構成。Check 52
# は §4 だけをパースして予算を確認するが、§2 と §4 が drift していると「人間が読む表」と
# 「機械が真値とする値」が乖離する。本 Check で両者のファイル集合の対称差を 0 に強制し、
# §2 表に新 budget 行を追加し忘れた／§4 から脱落した、等の drift を pre-commit で検出する。
# 数値（行数・budget）の一致は honest dating で人間レビュー対象とし、本 Check は「ファイル
# 集合」のみを比較する（行数 drift は別の Check 52 が間接的に拾う構造）。
_budget59 = ROOT / "docs" / "architecture" / "file-size-budget.md"
if _budget59.exists():
    _bsrc59 = _budget59.read_text(encoding="utf-8")
    # §2: | `path` | ... という表形式
    _table59 = set(re.findall(r"\|\s*`([^`]+)`\s*\|", _bsrc59))
    # §4 BUDGET-DATA ブロック
    _budgetblock59 = re.search(r"<!--\s*BUDGET-DATA(.*?)-->", _bsrc59, re.DOTALL)
    if _budgetblock59:
        _data59 = set()
        for line in _budgetblock59.group(1).strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                _data59.add(parts[0])
        # §2 表には `path` の他に `package.json` 等の説明用バッククォートも含まれる可能性が
        # あるため、§4 BUDGET-DATA に登録されたファイルが §2 表に存在することだけを強制し、
        # §2 表側の余計エントリは許容する（false positive 防止）。
        _only_data59 = sorted(_data59 - _table59)
        check(
            not _only_data59,
            f"Check 59: file-size-budget §2 表 contains all {len(_data59)} BUDGET-DATA entries",
            f"Check 59: BUDGET-DATA entries missing from §2 表: {_only_data59} — "
            f"§4 (機械可読) と §2 (人間可読) が drift している。§2 表に該当行を追加して同期せよ",
        )
    else:
        warnings.append("Check 59: BUDGET-DATA block not found — §2/§4 set check skipped")
else:
    warnings.append("Check 59: file-size-budget.md not found — §2/§4 set check skipped")

# ── 60. ESLint warning baseline regression guard (ADVISORY) ───────────────────
# file-size-budget.md の <!-- ESLINT-BASELINE-DATA --> ブロックに記録された warning 数 baseline
# 以下であることを ADVISORY で監視する。baseline ファイルが見つからない場合や正規表現で値を
# 取れない場合は ADVISORY skip（環境制約のため exit に影響しない）。本 Check は CI 内で直接
# `npm run lint` を実行せず、代わりに baseline 値が記録されていることだけを確認する（実測値
# の取得は CI 全体の ESLint scan ステップが担う）。これは「baseline 値が消えた／コメントアウト
# された」ことを ADVISORY で検出する役割で、warning 件数の実測比較は CI workflow 側で行う
# 設計（Check 単体での実装複雑度を抑え、責務を分離する）。
_baseline60 = re.search(r"<!--\s*ESLINT-BASELINE-DATA\s+(\d+)\s+-->", _bsrc59 if _budget59.exists() else "")
if _baseline60:
    _baseline_n60 = int(_baseline60.group(1))
    warnings.append(
        f"Check 60 (ADVISORY): ESLint warning baseline = {_baseline_n60} (recorded in file-size-budget.md)"
    )
else:
    warnings.append(
        "Check 60 (ADVISORY): ESLint warning baseline marker not found in file-size-budget.md — "
        "add `<!-- ESLINT-BASELINE-DATA <N> -->` to enable regression guard"
    )

# ── 61. js/*.js factory documentation marker (BLOCKING) ───────────────────────
# 各 js/ 葉モジュールが factory pattern (`export function createXxx({...})`) を export する
# 場合、ファイル先頭の docstring に "factory pattern" キーワードが含まれていることを機械
# 強制する。これは「factory として抽出した経緯」を後続 AI / 人間レビュアーが file 単体を
# 読むだけで認識できることを保証し、抽出経緯のドキュメント drift を構造的に閉じる。
_doc_drift61 = []
_factory_count61 = 0
_FACTORY_RE61 = re.compile(r"^export\s+function\s+create[A-Z][A-Za-z0-9_]*\s*\(\s*\{", re.MULTILINE)
for _spec61, _path61 in _modules47:
    if not _path61.exists():
        continue
    _src61 = _path61.read_text(encoding="utf-8")
    if _FACTORY_RE61.search(_src61):
        _factory_count61 += 1
        # docstring (ファイル先頭の /** ... */) に "factory pattern" を含むか
        _docstring61 = re.match(r"\s*/\*\*([\s\S]*?)\*/", _src61)
        if not _docstring61 or "factory pattern" not in _docstring61.group(1).lower():
            _doc_drift61.append(_spec61.replace("./", ""))
check(
    not _doc_drift61,
    f"Check 61: all factory-pattern modules in js/ contain 'factory pattern' marker "
    f"in their docstring ({_factory_count61} factory modules)",
    f"Check 61: factory-pattern modules missing 'factory pattern' marker in docstring: "
    f"{_doc_drift61} — add a header comment noting that the module uses the factory pattern, "
    f"for the benefit of future readers (AI or human).",
)

# ── 62. AIO entity canonical_url cross-surface identity (BLOCKING) ────────────
# aio-manifest.json の `entity.canonical_url` と llms-full.txt の `Canonical URL:` 値が
# 1 バイトも違わずに一致することを機械強制する。Entity の canonical URL は AIO 識別子の
# 最重要 anchor — manifest と canon (llms-full) の双方が同じ URL を主張していないと、
# 引用先 / クローラの ground-truth が分かれ、entity disambiguation が崩れる。C6 の
# 範疇内で「両者が drift していたら BLOCKING」する。これは Check 4 (llms 系 byte-identity)
# の発想を entity-URL 単位に降ろした検査。
_manifest62 = ROOT / ".well-known" / "aio-manifest.json"
_llmsfull62 = ROOT / "llms-full.txt"
if _manifest62.exists() and _llmsfull62.exists():
    try:
        _mdata62 = json.loads(_manifest62.read_text(encoding="utf-8"))
        _entity_url62 = _mdata62.get("entity", {}).get("canonical_url", "")
    except json.JSONDecodeError:
        _entity_url62 = ""
    _llms_match62 = re.search(r"Canonical URL:\s*\**\s*(https?://\S+?)\s*(?:\s|\*|$)", _llmsfull62.read_text(encoding="utf-8"))
    _llms_url62 = _llms_match62.group(1) if _llms_match62 else ""
    check(
        _entity_url62 and _entity_url62 == _llms_url62,
        f"Check 62: aio-manifest entity.canonical_url ({_entity_url62}) == llms-full.txt Canonical URL — entity identifier consistent across AIO layers",
        f"Check 62: AIO entity canonical_url drift — aio-manifest={_entity_url62!r}, llms-full={_llms_url62!r}. "
        f"Entity の canonical URL は最重要 anchor。両者を再同期せよ (C6 範疇)",
    )
else:
    warnings.append("Check 62: aio-manifest.json or llms-full.txt not found — entity-URL check skipped")

# ── 63. Crawler discovery origin alignment (BLOCKING) ─────────────────────────
# robots.txt の `Sitemap:` URL の origin、aio-manifest.json `entity.canonical_url` の origin、
# sitemap.xml の全 `<loc>` の origin が完全に同一であることを機械強制する。クローラは
# robots.txt → sitemap.xml の順に discover するため、両者が origin drift していると
# crawler は別ホストの URL を「同サイトの一部」と誤認するか、丸ごと取りこぼす。さらに
# entity.canonical_url の origin もこれらと一致していないと、AIO 引用先が外部ホストを
# 指す事態になる。Check 35 (robots.txt の Sitemap directive 存在確認) と Check 39
# (sitemap loc の実在確認) を補完する「同一 origin 一致」の structural integrity 検査。
_robots63 = ROOT / "robots.txt"
_sitemap63 = ROOT / "sitemap.xml"
if _robots63.exists() and _sitemap63.exists() and _manifest62.exists():
    _sm_match63 = re.search(r"^Sitemap:\s*(https?://\S+)", _robots63.read_text(encoding="utf-8"), re.MULTILINE)
    _sm_url63 = _sm_match63.group(1) if _sm_match63 else ""
    _sm_origin63 = re.match(r"(https?://[^/]+)", _sm_url63)
    _sm_origin_v63 = _sm_origin63.group(1) if _sm_origin63 else ""
    try:
        _tree63 = ET.parse(str(_sitemap63))
        _ns63 = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        _locs63 = [el.text for el in _tree63.getroot().findall(".//s:loc", _ns63) if el.text]
    except ET.ParseError:
        _locs63 = []
    _loc_origins63 = set()
    for _loc in _locs63:
        _m = re.match(r"(https?://[^/]+)", _loc)
        if _m:
            _loc_origins63.add(_m.group(1))
    _entity_origin63 = ""
    _em = re.match(r"(https?://[^/]+)", _entity_url62 or "")
    if _em:
        _entity_origin63 = _em.group(1)
    _all_origins63 = _loc_origins63 | ({_sm_origin_v63} if _sm_origin_v63 else set()) | ({_entity_origin63} if _entity_origin63 else set())
    check(
        len(_all_origins63) == 1,
        f"Check 63: crawler discovery origins all agree at {sorted(_all_origins63)[0] if _all_origins63 else '(none)'} (robots Sitemap + sitemap loc + aio-manifest entity)",
        f"Check 63: crawler discovery origin drift — distinct origins = {sorted(_all_origins63)}. "
        f"robots.txt Sitemap, sitemap.xml <loc> origins, aio-manifest entity.canonical_url origin は全て同一ホストでなければクローラが取りこぼす",
    )
else:
    warnings.append("Check 63: robots.txt / sitemap.xml / aio-manifest.json 一部欠落 — origin alignment skipped")

# ── 64. check-repository-consistency-map.md Check-row ascending (BLOCKING) ────
# docs/architecture/check-repository-consistency-map.md は本ファイル check_repository_
# consistency.py の Check 一覧を一行 = 一 Check で表形式に列挙したガバナンス文書。各行は
# `| Check N | ... |` 形式で番号が昇順に並ぶことが「人間レビュアーが Check の追加位置を
# 一瞬で判断できる」という運用前提を支える。table 行の番号が降順／重複していると、新規
# Check の挿入位置を誤り、Check 番号衝突を引き起こす（過去 Stage 5-l / 5-k' の naming 衝突
# と同種の class）。本 Check は表内の `Check N` を順次抽出し、ascending strict であることを
# 機械強制する。
_map64 = ROOT / "docs" / "architecture" / "check-repository-consistency-map.md"
if _map64.exists():
    _msrc64 = _map64.read_text(encoding="utf-8")
    _nums64 = [int(m) for m in re.findall(r"\|\s*Check\s+(\d+)[a-z]?\s*\|", _msrc64)]
    _ascending64 = all(_nums64[i] <= _nums64[i + 1] for i in range(len(_nums64) - 1))
    check(
        _ascending64 and len(_nums64) > 0,
        f"Check 64: check-repository-consistency-map.md table rows are in ascending order ({len(_nums64)} rows, range {_nums64[0] if _nums64 else 0}..{_nums64[-1] if _nums64 else 0})",
        f"Check 64: check-repository-consistency-map.md table rows NOT ascending — sequence = {_nums64}. "
        f"テーブル内の `| Check N |` 行は番号昇順に並べよ (新規 Check の挿入位置誤認防止)",
    )
else:
    warnings.append("Check 64: check-repository-consistency-map.md not found — ascending row check skipped")

# ── 65. docs/architecture/*.md Last-Updated ISO-8601 format (BLOCKING) ────────
# docs/architecture/ 配下の全 .md について、`Last-Updated:` フィールドが存在する場合は
# その値が ISO-8601 の `YYYY-MM-DD` 形式に厳密に従うことを機械強制する。Last-Updated は
# 「文書がいつ真値だったか」を読み手 (AI/human) に伝える正本シグナルであり、フォーマット
# 揺れ (e.g. `06-13-2026` / `2026.6.13`) は honest-dating 原則（Check 34/AI2AI.md カノン）
# を内部から侵食する。Check 34 が sitemap lastmod との一致を ADVISORY で見るのに対し、
# 本 Check は「日付フォーマットそのもの」を BLOCKING で固定する責務分離。
_isodate65 = re.compile(r"^\s*Last-Updated\s*:\s*(.+?)\s*$", re.MULTILINE)
_isoformat65 = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_bad_dates65 = []
for _md65 in sorted((ROOT / "docs" / "architecture").glob("*.md")):
    _src65 = _md65.read_text(encoding="utf-8")
    _m65 = _isodate65.search(_src65)
    if _m65:
        _val65 = _m65.group(1).strip()
        if not _isoformat65.match(_val65):
            _bad_dates65.append(f"{_md65.relative_to(ROOT)}: {_val65!r}")
check(
    not _bad_dates65,
    "Check 65: all docs/architecture/*.md Last-Updated values are ISO-8601 (YYYY-MM-DD)",
    f"Check 65: non-ISO-8601 Last-Updated values: {_bad_dates65} — "
    f"全 docs/architecture/*.md の Last-Updated は `YYYY-MM-DD` 形式に統一せよ (honest-dating 原則)",
)

# ── 66. index.html <title> entity-identifier presence (BLOCKING) ──────────────
# index.html の `<title>` 要素に entity primary identifier (`yuta` または `横井`、いずれも
# case-insensitive) が含まれることを機械強制する。`<title>` は SEO/AIO 検索結果の最重要
# anchor で、entity 名が含まれていないと SERP/LLM 引用時に「これは誰のサイトか」が一瞬で
# 判定できなくなり、AIO 戦略（「機械可読な authority building」）の効果が消失する。
# C6 範疇内で title の「ブランディング anchor」性を機械強制する検査。
_title66 = re.search(r"<title>([^<]+)</title>", read("index.html"), re.IGNORECASE)
_title_text66 = _title66.group(1) if _title66 else ""
_has_entity66 = bool(re.search(r"yuta", _title_text66, re.IGNORECASE) or "横井" in _title_text66)
check(
    _has_entity66,
    f"Check 66: index.html <title> contains entity primary identifier — title={_title_text66!r}",
    f"Check 66: index.html <title> ({_title_text66!r}) lacks entity primary identifier "
    f"('yuta' [case-insensitive] or '横井'). AIO/SEO の entity anchor 強度が失われる。"
    f"title に entity 名を含めて再同期せよ",
)

# ── 67. GitHub Actions workflow explicit permissions (BLOCKING) ───────────────
# .github/workflows/*.yml の全ファイルに top-level `permissions:` ブロックが明示宣言されて
# いることを機械強制する。permissions: が無いと GitHub の default token は full read/write
# 相当の広い権限になり、CWE-275 (Missing Actions Permissions) クラスのセキュリティ問題と
# なる。実運用 5 workflow は既に明示宣言済みだが、新規 workflow 追加時にこれを忘れる drift
# を pre-commit で構造的に閉じる。Check 48 (snapshot workflow の permissions 二重宣言整合)
# を補完する「全 workflow 適用版」の security baseline。
_perm_missing67 = []
for _wf67 in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
    _wsrc67 = _wf67.read_text(encoding="utf-8")
    if not re.search(r"^permissions:\s*$", _wsrc67, re.MULTILINE):
        _perm_missing67.append(_wf67.name)
check(
    not _perm_missing67,
    f"Check 67: all {len(list((ROOT / '.github' / 'workflows').glob('*.yml')))} workflows declare an explicit top-level permissions: block",
    f"Check 67: workflows missing top-level permissions: block: {_perm_missing67}. "
    f"GitHub Actions の default token は full r/w — 明示宣言で CWE-275 を防ぐ",
)

# ── 68. dependabot.yml dual-ecosystem coverage (BLOCKING) ─────────────────────
# .github/dependabot.yml が `npm` (devDependencies の月次更新) と `github-actions`
# (workflow action major tag の月次更新) の両 ecosystem を update 対象に含むことを
# 機械強制する。Dev tooling (eslint / stylelint / playwright / http-server) と GitHub
# Actions の自動更新は v80+ CI hygiene の基盤で、どちらかが欠落すると人手で月次更新を
# 追跡する負債が積み上がる。設定ファイルの drift (e.g. 1 ecosystem だけ残してもう片方を
# 消す) を BLOCKING で防ぐ。
_dependabot68 = ROOT / ".github" / "dependabot.yml"
if _dependabot68.exists():
    _dsrc68 = _dependabot68.read_text(encoding="utf-8")
    _has_npm68 = 'package-ecosystem: "npm"' in _dsrc68 or "package-ecosystem: 'npm'" in _dsrc68
    _has_gha68 = 'package-ecosystem: "github-actions"' in _dsrc68 or "package-ecosystem: 'github-actions'" in _dsrc68
    check(
        _has_npm68 and _has_gha68,
        "Check 68: dependabot.yml covers both npm and github-actions ecosystems",
        f"Check 68: dependabot.yml is missing ecosystem coverage — npm={_has_npm68}, github-actions={_has_gha68}. "
        f"両 ecosystem の月次更新は v80+ CI hygiene の基盤。両方を保持せよ",
    )
else:
    warnings.append("Check 68: .github/dependabot.yml not found — ecosystem coverage check skipped")

# ── 69. package.json engines.node ↔ CI node-version pin alignment (BLOCKING) ──
# package.json `engines.node` が CI workflow の Node version pin (`node-version: '24'`) を
# 許容する範囲を含むことを機械強制する。両者が drift していると CI は 24 でビルドするが
# package.json は別 version を強制するため、ローカル開発と CI で実行 Node が分かれる
# inconsistency が生まれる。setup-node@v6 の pin と engines が許容範囲で揃っていることを
# pre-commit で保証する。
_pkg69 = ROOT / "package.json"
_engines69 = ""
_ci_nodes69 = []
if _pkg69.exists():
    try:
        _pkgdata69 = json.loads(_pkg69.read_text(encoding="utf-8"))
        _engines69 = _pkgdata69.get("engines", {}).get("node", "")
    except json.JSONDecodeError:
        _engines69 = ""
for _wf69 in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
    for _m in re.finditer(r"node-version:\s*['\"]?(\d+)['\"]?", _wf69.read_text(encoding="utf-8")):
        _ci_nodes69.append(_m.group(1))
# engines が `>=24` または `>=20` などの major-range 表現を含むか、CI pin の major を許容するか
_ci_majors69 = set(_ci_nodes69)
_satisfied69 = True
_unsupported69 = []
for _maj in _ci_majors69:
    # engines 文字列に当該 major が含まれているか (e.g. ">=24" or "^24" or "24" )
    if not re.search(rf"(>=|\^|~|\b){_maj}(\b|\.)", _engines69):
        _satisfied69 = False
        _unsupported69.append(_maj)
check(
    _satisfied69 and _engines69,
    f"Check 69: package.json engines.node ({_engines69!r}) covers all CI node-version pins ({sorted(_ci_majors69)})",
    f"Check 69: package.json engines.node ({_engines69!r}) does NOT cover CI node-version pin major(s) {sorted(_unsupported69)}. "
    f"setup-node@v6 の pin と engines が許容範囲で揃っていないとローカル開発と CI が分裂する",
)

# ── 70. total-check-runbook.md §9 check-count cross-reference (BLOCKING) ──────
# docs/architecture/total-check-runbook.md §9 の「consistency Check 総数」行に記述された
# Check 件数 (`**N**`) が、check_repository_consistency.py の実際の Check 番号最大値と
# 一致することを機械強制する。Check 45 が docstring inventory ↔ section header の bijection
# を見るのに対し、本 Check は「実装ファイル ↔ runbook §9」の cross-document 整合性を担う。
# 新 Check 追加時に runbook を更新し忘れる drift を pre-commit で構造的に閉じる。
_runbook70 = ROOT / "docs" / "architecture" / "total-check-runbook.md"
_self70 = ROOT / ".github" / "scripts" / "check_repository_consistency.py"
if _runbook70.exists() and _self70.exists():
    _self_src70 = _self70.read_text(encoding="utf-8")
    _section_nums70 = [int(m) for m in re.findall(r"^# ── (\d+)\.\s", _self_src70, re.MULTILINE)]
    _actual_max70 = max(_section_nums70) if _section_nums70 else 0
    _runbook_src70 = _runbook70.read_text(encoding="utf-8")
    _runbook_match70 = re.search(r"consistency Check 総数\s*\|\s*\*\*(\d+)\*\*", _runbook_src70)
    _runbook_n70 = int(_runbook_match70.group(1)) if _runbook_match70 else 0
    check(
        _runbook_n70 == _actual_max70 and _actual_max70 > 0,
        f"Check 70: total-check-runbook.md §9 records {_runbook_n70} checks == implementation max {_actual_max70}",
        f"Check 70: total-check-runbook.md §9 records {_runbook_n70} but implementation has {_actual_max70}. "
        f"runbook §9 の「consistency Check 総数」を `**{_actual_max70}**` に同期せよ",
    )
else:
    warnings.append("Check 70: runbook or check script not found — count cross-reference skipped")

# ── 71. file-size-budget.md BUDGET-DATA path existence (BLOCKING) ─────────────
# docs/architecture/file-size-budget.md §4 BUDGET-DATA に列挙された各エントリのパスが
# 実在ファイルを指すことを機械強制する。BUDGET-DATA は Check 52 (ADVISORY 行数予算) の
# 真値だが、ファイル rename / 削除後に BUDGET-DATA から行を消し忘れると Check 52 が
# 「存在しないファイル」を黙ってスキップし、削除後の monitoring drift が見えなくなる。
# 本 Check は「BUDGET-DATA に登録された path は全て実在する」を BLOCKING で保証する。
_budget71 = ROOT / "docs" / "architecture" / "file-size-budget.md"
if _budget71.exists():
    _bsrc71 = _budget71.read_text(encoding="utf-8")
    _budgetblock71 = re.search(r"<!--\s*BUDGET-DATA(.*?)-->", _bsrc71, re.DOTALL)
    _missing71 = []
    _count71 = 0
    if _budgetblock71:
        for line in _budgetblock71.group(1).strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                _p71 = parts[0]
                _count71 += 1
                if not (ROOT / _p71).exists():
                    _missing71.append(_p71)
    check(
        not _missing71 and _count71 > 0,
        f"Check 71: all {_count71} BUDGET-DATA paths in file-size-budget.md exist",
        f"Check 71: BUDGET-DATA paths point at non-existent files: {_missing71}. "
        f"ファイル rename/削除後に §4 BUDGET-DATA から該当行を削除して同期せよ "
        f"(Check 52 silent-skip 防止)",
    )
else:
    warnings.append("Check 71: file-size-budget.md not found — BUDGET-DATA existence check skipped")

# ── Result ────────────────────────────────────────────────────────────────────
print()
if errors:
    print(f"REPOSITORY CONSISTENCY CHECK FAILED — {len(errors)} error(s):")
    for e in errors:
        print(f"  ::error::{e}")
    sys.exit(1)

if warnings:
    print(f"Repository consistency check passed with {len(warnings)} warning(s).")
else:
    print("Repository consistency check passed — all invariants hold.")

sys.exit(0)
