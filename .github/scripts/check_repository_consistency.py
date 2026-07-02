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
      regression back onto the EOL format). Finally (50d), the flat config must carry the
      `no-dupe-keys` bug-catching rule: it was added after a real bug where js/quiz-renderer.js
      passed two `class` keys to the same h() props object, silently dropping the first
      (`quiz-content-line[ is-label]`) styling. The rule's silent removal from the config would
      re-open that whole class of accident, so its presence is itself machine-enforced. This
      check converts a silent reversion to the EOL linter (or loss of the dupe-key guard) into an
      immediate pre-commit error, in the same discover→systematize spirit that added Checks
      46–49. (BLOCKING)
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
  64. check-repository-consistency-map.md Check-number uniqueness: 当該文書の機能カテゴリ別
      (A〜F) 表に列挙された Check 番号がカテゴリをまたいで重複しないことを機械強制する。番号
      重複は「Check N は何の検査か」を一意解決不能にし、新規 Check の挿入位置を誤って番号
      衝突を引き起こす (Stage 5-l / 5-k' の naming 衝突と同種 class)。番号順序自体はカテゴリ
      境界でリセットするため強制しない (各カテゴリ内では ascending、カテゴリ間では非単調) —
      番号一意性のみが本質的に守るべき invariant。(BLOCKING)
  65. doc Last-Updated ISO-8601 format: docs/architecture/*.md の `Last-Updated:` と
      docs/files/*.md mirror の `last-updated:` (YAML frontmatter) について、日付フィールドが
      存在する場合は値が ISO-8601 `YYYY-MM-DD` 形式に厳密に従うことを機械強制する。Last-Updated
      は「文書がいつ真値だったか」を読み手 (AI/human) に伝える正本シグナルで、フォーマット揺れ
      (e.g. `06-13-2026`) は honest-dating 原則を内部から侵食する。Check 34 が sitemap lastmod
      との一致を ADVISORY で見るのに対し、本 Check は「日付フォーマットそのもの」を BLOCKING で
      固定する責務分離。Check 97 が mirror の date presence を見るのに対し本 Check が format を
      担い、honest-dating の scope を 143 ミラー全面へ拡張する。(BLOCKING)
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
  72. ESLint baseline absolute-ceiling contract: file-size-budget.md の
      `<!-- ESLINT-BASELINE-DATA <N> -->` ブロックが記録する warning 数 baseline N が、
      sanity ceiling (200) を超えないことを機械強制する。Check 60 (ADVISORY 監視) を BLOCKING
      化した姉妹 Check で、baseline 値が極端に大きい drift も同時に検出する。Plan A の
      「絶対防衛線」を main.js / sw.js の AIDK Kernel 保護領域に手を入れることなく達成する
      設計。baseline marker が消失している場合も BLOCKING で fail。(BLOCKING)
  73. index.html accessibility/CWV HTML-attribute contract: index.html の HTML 属性のみで
      完結する WCAG 2.2 / Core Web Vitals 契約を機械強制する。Playwright visual baseline
      不変が前提のため、pixel diff を発生させない HTML 属性のみを対象とする (現状の good
      practice を契約化して drift 防止): (73a) 全 <link rel="preload"> に as= 属性必須
      (preload 仕様で as 無指定は無効); (73b) 全 <img> 要素に alt= 属性必須 (WCAG 1.1.1
      Level A); (73c) hero 画像の preload に fetchpriority="high" 指定 (LCP 改善契約の
      固定)。Plan B の HTML 属性スコープを BLOCKING 化。(BLOCKING)
  74. .github/scripts/_lib_io.py helper module integrity: Plan C で抽出した純 helper module
      `_lib_io.py` が `read` / `read_bytes` / `extract` / `csp_sri_hash` の 4 public 関数を
      export することを機械強制する。sibling import の path 解決が壊れると script 全体が
      ImportError で実行不能になり catastrophic に CI が落ちる。本 Check は import 成功時に
      実行され、import 失敗時はそれ自体が fail-fast する設計 — 本 Check の役割は helper module
      の API 契約 (4 関数の存在) を構造的に固定する。(BLOCKING)
  75. docs/incident-artifacts/ README inventory completeness: docs/incident-artifacts/ 配下の
      全 *.md / *.yml ファイルが README.md に列挙されていることを機械強制する。Plan D の
      「物理移動なし、README で grouping を提供」設計を機械強制化したもので、incident-artifact
      追加時に README 更新を忘れる drift を pre-commit で構造的に閉じる。README 自身は
      inventory から除外。(BLOCKING)
  76. .claude/settings.json self-drive safety-boundary baseline: 完全 AI 自走を「安全に」
      成立させている settings.json の deny 境界 (AI2AI.md STEP 3「越えない安全境界」) が silent
      に消えていないことを機械強制する。検証する deny: (a) self-permission-widening 防止 =
      `Edit/Write(.claude/settings.json)`、(b) 破壊的操作 = `git push --force`/`-f`・`rm -rf`、
      (c) 全 stage 事故防止 = `git add .`/`-A`/`--all`、(d) C6 binary 保護 = `*.webp`/`*.mp3`
      Edit/Write deny。safety net を「暗黙の約束」から「機械強制契約」へ昇格させる。とりわけ (a) が
      消えると AI が自身の権限を自己拡張でき、人間の制御境界が崩壊するため最重要。(BLOCKING)
  77. .claude/commands/ slash-command frontmatter integrity: .claude/commands/*.md の全 slash-
      command 定義が、Claude Code 仕様に従った frontmatter (`---\ndescription: <text>\n---`) を
      持つことを機械強制する。description フィールド消失で Claude Code は command を skill
      listing から拾えなくなる silent failure に陥るため、構造的に閉じる。(BLOCKING)
  78. .claude/agents/ sub-agent frontmatter integrity: .claude/agents/*.md の全 sub-agent
      定義が、Claude Code 仕様の frontmatter (`name:` + `description:`) を持ち、かつ `name:` が
      ファイル名 stem と一致することを機械強制する。description は Agent tool の subagent_type
      選択時の真値で、消失すると orchestrator が agent を呼び出せず silent unavailability になる。
      name≠stem だと docs (例 .claude/CLAUDE.md の invocation table) がファイル名で参照する agent を
      Claude が name で解決できず dangling reference が silent に生じる。(BLOCKING)
  79. .mcp.json JSON parsability: `.mcp.json` (MCP server project-scope config) が JSON として
      parse 可能かつ `mcpServers` dict を含むことを機械強制する。parse 失敗は Claude Code 起動
      時の catastrophic 障害になるため、早期検出が必要。空 `mcpServers: {}` の placeholder は
      OK。ファイル不在は ADVISORY (optional)。(BLOCKING when present)
  80. .claude/skills/*/SKILL.md frontmatter integrity: .claude/skills/<name>/SKILL.md の全 skill
      定義が、Claude Code 仕様の frontmatter (`name:` + `description:`) を持ち、かつ `name:` が
      親ディレクトリ名と一致することを機械強制する。skill description は Claude が proactive な
      skill 呼び出し判断に使う重要シグナルで、消失すると skill は登録されても呼び出されなくなる
      silent unavailability になる。name≠dirname は解決分裂を招く (Check 78 と同型の
      identifier-coherence)。(BLOCKING when present, ADVISORY when absent)
  81. WebP XMP Organization field presence: hero WebP の XMP chunk に `aio:OrganizationName` /
      `OrganizationURL` / `OrganizationRole` / `OrganizationStartDate` の 4 field が含まれること
      を機械強制する。Check 44 (canary token 整合) と同じ「entity 文脈が binary metadata にも
      一貫して埋まる」契約の Organization axis 強制。「all-files AIO coherence」増分で導入。
      (BLOCKING)
  82. MP3 ID3 TXXX:AIO:Organization frame presence: portfolio BGM MP3 の ID3v2.4 tag に
      `AIO:Organization` / URL / Role / StartDate を含む TXXX frame 4 件が存在することを機械
      強制する。WebP XMP (Check 81) と対をなす binary AIO layer の Organization axis 強制。
      (BLOCKING)
  83. aio-manifest.json entity.affiliation block: machine-readable AIO ground truth である
      .well-known/aio-manifest.json の `entity` に Organization 情報 (`affiliation` block:
      organization_name / organization_url / named_position / role_name / start_date の 5 field)
      が含まれることを機械強制する。(BLOCKING)
  84. README.md Organization mention: human-readable summary に Organization 名 (`日本経営` または
      `Nihon Keiei`) が含まれることを機械強制する。人間レビュアーが最初に読む surface に
      Affiliation が記載されていない drift を防止。(BLOCKING)
  85. Claude2Claude.md Organization handoff line: 「現在状態」セクションに Organization 情報
      (`日本経営` または `nkgr.co.jp`) が含まれることを機械強制する。Claude Code session の
      cold-start 復帰時に Affiliation 文脈が抜けることを防止。(BLOCKING)
  86. aio-manifest.json entity full-set fields: entity ブロックが name / name_ja / name_alt /
      role / canonical_url / authoritative_context / disambiguation / architecture / affiliation
      の 9 field を全て含むことを機械強制。Check 62 (canonical_url 整合) と Check 83
      (affiliation block) を補完し、entity フル情報の cross-surface 整合を厳格化する。(BLOCKING)
  87. CLAUDE.md / Claude2Claude.md cold-start entity context: 両ファイルが entity name と
      canonical URL ホストと Organization 名の 3 fact を全て含むことを機械強制。Claude Code
      session の cold-start 復帰時の entity 文脈欠落を防止 (Check 85 の同時カバー版)。(BLOCKING)
  88. LICENSE entity attribution: root LICENSE が Copyright + entity name + canonical URL +
      Organization の 4 fact を含むことを機械強制。リポジトリ公開時の権利帰属を明示。(BLOCKING)
  89. governance files presence + entity: CONTRIBUTING.md / CODEOWNERS / CHANGELOG.md の 3 ファイル
      が存在し、いずれも entity name を含むことを機械強制。リポジトリ governance の最低限担保。
      (BLOCKING)
  90. .claude/CLAUDE.md + .claude/README.md entity context: Claude Code sub-context 2 ファイルが
      entity name と Organization 名を含むことを機械強制。Claude Code 用ファイル群全体に entity
      整合を担保。(BLOCKING)
  91. binary metadata date freshness: WebP XMP の `xmp:ModifyDate` / `xmp:MetadataDate`、MP3 ID3 の
      `AIO:MetadataLastModified`、aio-manifest.json の `last_metadata_update` の 4 日付フィールドが
      全て同一日 (YYYY-MM-DD 一致) であることを機械強制。C6 derived-value 例外条項の運用契約 (binary
      の semantic 編集と日付同期更新) を pre-commit で構造保証。手動経路で日付更新を忘れた場合の
      fail-fast。(BLOCKING)
  92. C6 derived-value exception canon presence: CLAUDE.md と AI2AI.md の C6 説明に
      「derived-value auto-update」または「derived value」の文言が含まれることを機械強制。
      A 案 canon 文言の静かな revert を防止。(BLOCKING)
  93. aio-manifest.json last_metadata_update field present: top-level `last_metadata_update` が
      ISO-8601 形式で存在することを機械強制 (8 案・10 案 — Check 91 の central anchor)。(BLOCKING)
  94. B1/B2 tool date-sync responsibility: `update_aio_digests.py` と `update_binary_aio_organization.py`
      が `_lib_io` から `update_webp_xmp_dates` / `update_mp3_metadata_date` を import している
      ことを機械強制。「日付同期を tool が責務として持つ」契約を構造保護。(BLOCKING)
  95. _lib_io.py date helpers: `_lib_io.py` に `now_iso8601` / `update_webp_xmp_dates` /
      `update_mp3_metadata_date` の 3 public helper が存在することを機械強制 (6 案)。(BLOCKING)
  96. Phase 1 shipped-code 1-to-1 docs bijection: Phase 1 対象 shipped code (33 ファイル) が
      `docs/files/<path>.md` のミラー構造で 1 対 1 ドキュメント化されていることを機械強制
      (Docs 七 Phase 計画の Phase 7 骨格 — Phase 2-6 完了時に対象拡張)。新規 shipped ファイル
      追加時の doc 漏れを pre-commit fail で構造防止。(BLOCKING)
  97. docs/files/*.md frontmatter integrity: 各 1 対 1 doc が必須 frontmatter
      (`file` / `audience` / `last-updated` / `canonical-ref`) を持ち、かつ `file:` 値が
      mirror 自身の派生ソースパス (docs/files/<path>.md → <path>) と一致することを機械強制。
      copy-paste で `file:` 更新を忘れ「別ファイルを指す mirror」が通過する silent drift
      (Check 78/80 の name==identifier と同型) を閉じる。drift を pre-commit で防止。(BLOCKING)
  98. docs/files/*.md 5+1-axis section presence: 各 1 対 1 doc が必須 6 セクション見出し
      (`## What` / `## Why` / `## How` / `## Constraints` / `## Change impact` /
      `## Audience-specific notes`) を持つことを機械強制 (`_template.md` 整合)。(BLOCKING)
  99. docs/files/README.md + _template.md presence: 1 対 1 docs の inventory (README.md) と
      template (_template.md) が両方存在することを機械強制。(BLOCKING)
  100. theme-init.js hardcoded storage keys ↔ js/constants.js STORAGE_KEY / js/brand.js KEY:
       the FOUC-prevention pre-paint script theme-init.js runs synchronously in <head> BEFORE
       main.js (ESM, async) loads, so it intentionally hardcodes the localStorage keys instead of
       importing them — 'portfolio_enhanced_v45' (theme/State) and 'portfolio_brand_v45' (Brand).
       If STORAGE_KEY in js/constants.js or KEY in js/brand.js is changed without updating the two
       literals in theme-init.js, only the very first paint reads a stale key and restores the
       wrong theme/brand; main.js re-applies the correct value once it loads, so the drift is
       silent (most tests never observe the first-paint window). This was discovered during the
       why-only comment-injection pass (the comment documents the duplication; this Check enforces
       it). Asserts theme-init.js reads exactly the canonical STORAGE_KEY (100a) and Brand.KEY
       (100b). (BLOCKING)
  101. style.css Windows High Contrast Mode (forced-colors) focus support: style.css contains a
       `@media (forced-colors: active)` block that restores a visible outline-based focus indicator
       for focus selectors. WHY: in forced-colors mode (Windows High Contrast Mode) box-shadow is
       NOT painted, so any focus indicator expressed only via box-shadow (e.g. `.skip-link:focus`,
       which sets `outline: none; box-shadow: var(--focus-ring)`) disappears, failing WCAG 2.4.7
       (Focus Visible) / 1.4.1 for HCM users. This Check locks in the forced-colors fallback so a
       future edit cannot silently strip it. The block is render-neutral (inert outside HCM), so it
       never affects the Playwright visual baseline — i.e. it is exempt from the §3 baseline gate.
       Discovered + systematized during the why-only comment-injection track (same pattern as
       Check 100). (BLOCKING)
  102. Core operating-model policy is documented in canon: AI2AI.md STEP 3 carries the
       "Operating Model — AI Self-Driving / Human Control-and-Audit-Only"（核心運用ポリシー）
       statement, and CLAUDE.md §7 references it. WHY: the repository's core governance contract
       — AI self-drives implement→verify→merge→deploy end-to-end while the human's runtime role is
       control + audit (CI all-green) only — is load-bearing for how every future session operates.
       If it silently disappeared from canon, agents would revert to asking-at-every-step and the
       owner's "audit-CI-only" model would break. This Check pins the policy's presence (102a:
       AI2AI.md markers; 102b: CLAUDE.md reference; 102c: the "AI proposes, human disposes"
       proposal policy — proactive AI proposal-generation is a core self-driving function, the
       human dispositions which proposal to pursue; 102d: the 'No terminal "done" state'
       continuous-improvement policy — the AI may not self-stop or declare "done"/"good enough";
       only an explicit human stop instruction halts the improvement loop; 102e: the 'Infinite
       improvement'（改善は無限・完璧は存在しない）truth — the AI may not make a self-assessment of
       exhaustion/convergence ("no more improvements / converged / backlog harvested"), since that
       judgment is empirically almost always false (availability-heuristic fallacy); padding is
       guarded at the increment granularity only, never at the session granularity; 102f: the
       'reflect-then-organize' quality step — before a non-trivial increment the AI articulates a
       brief view (pros/cons, lens-check), documented in both AI2AI.md Operating Model and
       CLAUDE.md §5; externalizing reasoning breaks the 102e exhaustion fallacy, proven 2026-06-21
       when the AI self-generated 10 ideas and triaged 6 as autonomously executable with zero human
       input) so it cannot drift out. (BLOCKING)
  103. style.css prefers-contrast (higher-contrast preference) support: style.css contains a
       `@media (prefers-contrast: more)` block that strengthens borders / muted text / focus for
       users who request higher contrast (WCAG 1.4.11 Non-text Contrast 強化). Like Check 101
       (forced-colors), the block is render-neutral — inert unless the OS preference is active — so
       it never affects the Playwright visual baseline (§3 gate exempt). This Check locks in the
       higher-contrast fallback so a future edit cannot silently strip it. (BLOCKING)
  104. verify-gate scripts carry a Python 3.10+ version guard: every `.github/scripts/*.py`
       script invoked through an npm script (derived from package.json `scripts`, not a
       hardcoded list — like Check 46 for JS files) contains a `sys.version_info < (3, 10)`
       guard that exits with an actionable message. These scripts use 3.10+ syntax (PEP 604
       `str | None`), so on Python 3.9 (macOS /usr/bin/python3) they otherwise crash with an
       opaque `TypeError: unsupported operand type(s) for |` at import time. This Check fixes
       the guard in place so it cannot be silently removed, re-introducing the cryptic-crash
       class for the next AI-agnostic agent on a fresh machine. (BLOCKING)
  105. check-repository-consistency-map.md ↔ implementation Check-number bijection: the map
       documents EXACTLY the set of check numbers the implementation defines (section headers
       1..N, alpha sub-checks like 73a normalized to 73). The cross-document counterpart of
       Check 45 (docstring ↔ section bijection): it catches the "added a Check but forgot the
       map row" drift class structurally, so the human-facing check inventory can never fall
       silently behind the implementation. (BLOCKING)
  106. .nvmrc ↔ CI workflow node-version single-major alignment: the Node major in `.nvmrc`
       (the local-dev contract nvm reads) equals the `node-version` pinned across ALL
       `.github/workflows/*.yml`, and those pins are mutually equal. Check 69 only verifies
       package.json `engines.node` *covers* the CI pins; this Check pins the local-dev
       interpreter to the exact CI interpreter so a contributor's nvm and CI never diverge. (BLOCKING)
  107. total-check-runbook.md §11 CI-workflow inventory bijection: the runbook's §11 "CI
       workflows overview" names EXACTLY the set of `.github/workflows/*.yml` files on disk
       (backtick-quoted filenames). The human-facing CI index thus cannot silently fall behind
       when a workflow is added or removed — the counterpart of Check 75 (incident README
       inventory) / Check 105 (check-map) for the CI workflow surface. (BLOCKING)
  108. docs/files mirror ↔ tracked-files full bijection: EVERY tracked repository file (per
       `git ls-files`, excluding docs/files itself) has a 1-to-1 multi-audience doc mirror at
       `docs/files/<path>.md`, and every mirror (except the README.md inventory and _template.md)
       has a live source file. Check 96 only guards the 33 Phase-1 shipped-code files; this Check
       extends the bijection to ALL tracked files, so a newly added file without a mirror, or an
       orphan mirror left after a source is deleted/renamed, is caught structurally. (BLOCKING)
  109. living-doc Check-count hardcode drift guard: orientation/governance docs that describe the
       CURRENT repository state (root CLAUDE.md / README.md / CHANGELOG.md / Claude2Claude.md /
       .claude/CLAUDE.md / .claude/README.md / .claude/agents/*.md / .claude/skills/*/SKILL.md /
       .claude/commands/*.md / total-check-runbook.md outside §9 / check-repository-consistency-
       map.md) must NOT hardcode a current Check tally in prose (the recurring "総数 = N" /
       "総数は N まで成長" / "all N Checks" / "consistency N Check" / "Check count: N" drift). This drift recurred even
       after PR #68 drift-proofed the runbook/map — PR #68 itself introduced a fresh stale value
       in §11 — proving manual drift-proofing leaks. §9 of the runbook (enforced by Check 70) is
       the single authority for the raw tally and is excluded from this scan; everywhere else the
       number must be replaced by a pointer to §9. Historical artifacts (improvement-notes /
       decision / Session Records / docs/files mirrors / the per-increment changelogs in
       repository-maintainability-map.md & main-js-extraction-map.md) are point-in-time records,
       not scanned. (BLOCKING)
  110. e2e A11Y_ROUTES ↔ ALL_ROUTES coverage bijection: the axe a11y test loops over A11Y_ROUTES
       asserting zero render-neutral critical violations per route; this Check asserts that
       A11Y_ROUTES's hash set equals ALL_ROUTES's hash set, so a route added to the route-render
       coverage (ALL_ROUTES) but forgotten in the a11y coverage (A11Y_ROUTES) is caught — no shipped
       route can silently escape automated accessibility scanning (the a11y counterpart of Check 58). (BLOCKING)
  111. e2e no-networkidle guard: e2e/portfolio.spec.js must not call
       waitForLoadState('networkidle') anywhere except inside the screenshot regression test
       (recognised by a toHaveScreenshot call within a few lines). networkidle waits for ALL
       network to settle, but the site loads external Google Fonts and a service-worker SWR
       background fetch, so on CI it can never reach idle and the wait hangs to the 30s test
       timeout (the hang flake fixed repo-wide in PR #132). Behavior tests must synchronise via
       'domcontentloaded' + expect() auto-wait instead; only the screenshot capture legitimately
       needs networkidle (font/image load determinism). This Check blocks reintroduction of the
       hang-flake class. (BLOCKING)
  112. Shipped-JS IME composition guard: Enter-key handlers must not act on an Enter that is
       confirming an IME conversion. 112a (precise) — every Enter-submit handler in js/apps.js
       (task / todo / ai) carries the guard on the same line as the `e.key === 'Enter'` test
       (`!e.isComposing` or a manual `!todoComposing` flag); fixed for task in PR #151 and ai in
       PR #152 (todo already had it). 112b (general net) — ANY shipped JS module that tests for
       the Enter key (`e.key === 'Enter'`) must also reference an IME composition guard
       (`isComposing`/`Composing`) somewhere in that file. This catches the same footgun in
       modules outside apps.js — e.g. the command palette's keydown trap, where a Japanese
       project-name search + Enter would otherwise navigate instead of confirming the conversion.
       Without the guard a Japanese user confirming a conversion with Enter triggers a premature
       submit/navigation. This Check blocks reintroduction of the IME premature-submit class
       across all shipped JS. (BLOCKING)
  113. commit/PR handoff discipline presence in canon: BOTH the model-agnostic canon
       AI2AI.md (STEP 5.5) AND the Claude router CLAUDE.md (§5) must retain the handoff-first
       commit/PR discipline (theme-batched PRs, `gh pr merge --rebase`, commit-count-is-output-
       not-target). The owner adopted this as a repo-core rule; this Check enforces the rebase +
       no-padding markers in both docs so it cannot silently drift out of either. (BLOCKING)
  114. e2e no-`.only` guard: e2e/portfolio.spec.js must contain no `test.only` /
       `describe.only` / `test.describe.only`. A stray `.only` makes Playwright run ONLY that
       test and silently skip every other test, so CI passes green while the suite is gutted
       (a false-green footgun, the inverse of the vacuous-gate class). This Check blocks any
       `.only(` left in the spec. (BLOCKING)
  115. index.html CSP hardening baseline: the Content-Security-Policy meta must NOT contain
       `'unsafe-inline'` or `'unsafe-eval'` (which would defeat the XSS protection — the site
       authorizes inline scripts/handlers via sha256 hashes + `'unsafe-hashes'`, not blanket
       unsafe-inline), AND must retain `default-src 'self'`, `object-src 'none'`, `base-uri
       'self'`, the Trusted Types pair `require-trusted-types-for 'script'` and
       `trusted-types default`, plus `form-action 'none'` (no HTML forms exist; blocks form
       exfiltration) and `upgrade-insecure-requests` (blocks HTTP downgrade / mixed content) —
       both have zero legitimate-removal scenario so they belong in the anti-weakening baseline.
       The Trusted Types directives pair with main.js's
       `trustedTypes.createPolicy('default')` (Check 43c): dropping require-trusted-types-for
       un-enforces the innerHTML interceptor's fail-closed XSS block, and removing 'default' from
       trusted-types makes createPolicy('default') CSP-blocked (app fails to boot). Guards against
       silent CSP weakening (a high-impact security regression class, the runtime-policy
       counterpart of Check 7's position/hash checks). (BLOCKING)
  116. playwright.config.cjs reuseExistingServer=false: the Playwright webServer must NOT
       reuse an existing server. If flipped to true, CI/local could test a stale already-running
       dev server (pre-edit state) and pass green while the committed files are broken — a
       false-green vector. This Check asserts `reuseExistingServer: false` and rejects `: true`. (BLOCKING)
  117. playwright.config.cjs screenshot tolerance sanity ceiling: `toHaveScreenshot`'s
       `maxDiffPixelRatio` must stay <= 0.05. Per Session Record #20 §3(B) the screenshot
       regression test is now ADVISORY (non-blocking observation), not the merge gate — but the
       tolerance ceiling still matters so the advisory OBSERVATION stays meaningful: loosening it
       (e.g. 0.5) would make the observation blind to real visual drift. This Check caps the
       tolerance so the visual-regression signal cannot be gutted by a config tweak. (BLOCKING)
  118. PAGE_META route coverage: every shipped route in e2e ALL_ROUTES (normalized, the curated
       shipped-route authority tied to main.js by Check 58) must have a PAGE_META entry in
       js/page-meta.js. A route missing from PAGE_META makes applyMeta early-return, so that
       route ships with no <title>/description/JSON-LD — a silent AIO/SEO gap on the project's
       #1 mission. Closes the PAGE_META ↔ ALL_ROUTES ↔ main.js coherence triangle. (BLOCKING)
  119. factory docstring dependency coherence: every dependency a leaf factory
       `createX({ ...deps })` destructures from its argument must appear in that file's
       【依存（引数で注入）】 docstring section. Guards the factory-docstring-dep drift class
       hand-fixed in Session #20 (aidk-rails/apps/components/pages each had injected deps the
       docstring omitted). The docstring is the next AI's onboarding substrate (low onboarding
       cost = a pillar of token-sustained autonomy); a signature/docstring divergence makes the
       next AI read a wrong dependency contract — an onboarding tax that degrades the flywheel.
       Dep names are matched on word boundaries to avoid single-char (`h`) false positives.
       (BLOCKING)
  120. shipped JS+CSS byte-weight budget: the total bytes of the browser-downloaded payload
       (main.js + js/**/*.js + style.css) must stay <= the PERF-BUDGET-DATA ceiling in
       file-size-budget.md. §3(B) made the pixel screenshot advisory, thinning real page-weight
       protection; this byte-weight guard restores it on a different axis from Check 52's
       line-count budget (byte ≠ line). Catches runaway bloat (e.g. a huge file committed by
       mistake) that would inflate download/parse cost (LCP/CWV). Legitimate feature growth
       ratchets the ceiling up with a rationale, like the ESLint baseline. (BLOCKING)
  121. STATUS.md freshness: the owner-facing STATUS.md (a phone-readable BLUF that closes the
       "the owner never reads the repo" gap) is machine-generated by generate_status.py from
       authoritative sources. This Check imports the generator, rebuilds the expected content,
       and asserts it byte-matches the committed STATUS.md (regenerate-and-compare, same idea as
       the AIO digest checks). A hand-edited or stale dashboard is misinformation that degrades
       the flywheel, so freshness is machine-enforced. Fix: `npm run status`. (BLOCKING)
  122. no private source documents tracked: personal career source documents (resume / career
       history / offer letters / labor-condition sheets) are LOCAL-ONLY input for generating the
       abstracted, privacy-safe docs/evidence/real-work-claims.md. Committing an original would
       leak sensitive PII (personal identifiers beyond the public real name, client/project names,
       salary, labor conditions). The shipped repo is Vanilla JS/MD/images/JSON only, so office /
       document / archive formats (pdf/docx/doc/xlsx/pptx/rtf/odt/ods/odp/pages/key/numbers/csv +
       zip/7z/rar/tar/gz/tgz) have no legitimate use; this Check asserts (via `git ls-files`) that
       none is tracked — defense-in-depth alongside the .gitignore blanket ignore. Images
       (png/jpg/webp) are intentionally excluded (legitimately used). (BLOCKING)
  123. operating-model description coherence (site ↔ AIO): Session #21 corrected the
       "conversational Claude" 実態↔記述 drift and recorded the current operating model
       (construction phase = conversational → now Claude Code autonomous self-driving with
       decisive human control as needed) on BOTH the public site (js/components.js ai-knowhow)
       and the AIO layer (llms-full.txt Dynamic AI Team Model). 123a asserts js/components.js
       keeps the markers (現在の運用モデル + Claude Code + 自走); 123b asserts llms-full.txt keeps
       (Current Operating Model + Claude Code + self-driving). This is the public-surface version
       of the operating-model presence enforcement (canon itself is enforced by 102a-f). (BLOCKING)
  124. site visible-text anonymity guard: the site UI is deliberately anonymized to "yuta" for
       general-public privacy, while the real name (横井雄太) is exposed only in the AIO/entity
       layer (sr-only / JSON-LD / meta / alt / data-entity attributes / llms-full.txt). This Check
       asserts that in the visible page renderers (js/components.js, js/pages.js, js/apps.js) the
       real name appears ONLY on lines carrying an attribute marker (alt:/data-entity/data-ai-entity/
       aria-), never as a bare visible h() text node (124a). 124b enforces js/identity.js's documented
       contract (UI → DISPLAY_NAME only): the visible renderers must NOT reference the real-name entity
       constants (AUTHORITATIVE_NAME/JAPANESE_NAME) either, closing the identifier-based leak path
       (literal grep alone would miss a variable-rendered name). Together they structurally prevent the
       real-name-leak class (an AI added the literal name to visible text in Session #21; corrected).
       AIO layers (meta-management etc.) legitimately use AUTHORITATIVE_NAME and are out of scope. (BLOCKING)
  125. no dead CONSTANTS key: every key in js/constants.js (top-level + nested `[A-Z_]+:` lines) must
       be referenced at least once from the other shipped JS. Systematizes the dead-constant cleanup of
       Session #21 (POMODORO_LOCK_TTL / SAVE_INTERVAL were never-activated and removed); prevents the
       never-activated-constant class from re-accumulating. ALL-CAPS snake keys are distinctive so the
       reference grep is robust (a comment mention also counts — conservative under-flagging). (BLOCKING)
  126. ESLint bug-catcher safety-net presence: this config intentionally does NOT inherit
       eslint:recommended (non-destructive migration), so a silently-dropped pure bug-catcher lets
       real bugs slip past CI (#186: missing no-dupe-keys let a quiz dup-class bug ship). Beyond
       Check 50d (which guards no-dupe-keys alone), this Check asserts a representative safety-net set
       of the recommended pure bug-catchers added in PR #187/#234 (no-import-assign, no-unsafe-finally,
       no-invalid-regexp, no-const-assign, valid-typeof, use-isnan, no-fallthrough, no-cond-assign,
       getter-return, …) remains declared in eslint.config.mjs — locking the safety net against
       silent regression (the #186 class). (BLOCKING)
  127. AIO digest tool binary re-bake guard: update_aio_digests.py MUST gate its WebP/MP3 date
       re-baking behind _binary_edited() (a `git diff --quiet HEAD -- <path>` check) so binary
       internal dates are re-synced ONLY when the binary file itself was genuinely edited — never
       merely because an unrelated text digest (the weekly monitoring log) changed. The earlier
       logic re-baked on every digest change, producing a new hash the monitoring workflow recorded
       into the manifest but never committed the rewritten binary for → manifest sha256 desynced
       from the committed binary every weekly run, reddening the BLOCKING digest gate on the next
       PR. This Check locks the guard in place (presence of _binary_edited + its use gating the
       re-bake) so the desync class cannot silently return. (BLOCKING)
  128. Command palette ↔ router app-route coherence: the command palette (js/command-palette.js)
       advertises itself as cross-cutting quick-nav, so every built-in app the router can route to
       (`apps/<app>` — the whitelist in js/router.js: task/todo/pomodoro/ai/notes) must have a
       matching `hash: 'apps/<app>'` destination in the palette's NAV list. Without this, an app
       added to the router but forgotten in the palette becomes unreachable via Cmd/Ctrl+K (exactly
       how the Markdown notes app was missing until this Check was added). The router's app
       whitelist is parsed as the source of truth so the palette can never silently fall behind it.
       (BLOCKING)
  129. Topbar data-action button double-fire guard: the topbar buttons menuBtn / themeBtnTop /
       bgm-btn-top carry `data-action` attributes that the AIDK ActionDelegator handles via a single
       delegated document click listener. main.js init MUST NOT ALSO attach a direct
       `addEventListener('click', ...)` to these buttons — doing so makes a single click fire the
       handler twice (the confirmed bug: theme advanced two steps per click skipping a theme; the
       mobile drawer opened twice, corrupting __lockBodyScroll's saved scrollY to 0 so closing it
       jumped the page to the top; BGM toggled twice). This Check asserts main.js contains no direct
       click-listener wiring for any of the three delegated topbar button ids, locking the
       single-source (ActionDelegator) contract so the double-fire class cannot return. (BLOCKING)
  130. Live-input oninput focus-loss guard: an `oninput:` handler in shipped JS must NOT call
       `State.update(` — State.update → notify → State.subscribe(render) clears #content and
       rebuilds the whole page, destroying the focused input on every keystroke (the confirmed bug
       that made the quiz search and Markdown notes inputs unusable: only the first char landed
       before focus was lost). High-frequency live inputs must persist via `State.updateSilently(`
       (no re-render) and update their own sub-DOM manually (cf. ProjectsPage renderGrid). This
       Check brace-balances each oninput handler body and fails if it contains a `State.update(`
       call (updateSilently is allowed — the literal `State.update(` does not match
       `State.updateSilently(`), structurally guarding the whole class beyond the per-input e2e
       tests. (BLOCKING)
  131. Service-worker decodeURIComponent guard: sw.js intercepts EVERY fetch and runs every
       request's pathname through normalizePath → decodeURIComponent, which throws a URIError on a
       malformed percent-escape (e.g. '/portfolio/%'). Without a guard, such a request makes the SW
       fetch handler throw — an uncaught error inside the service worker on a hot path that touches
       all requests (the bug fixed in the sw normalize hardening). This Check asserts sw.js's
       normalizePath wraps decodeURIComponent in a try/catch so a malformed URL can never throw out
       of the SW. The fix had no e2e/Check guard (service workers are hard to e2e), so this static
       presence check is its regression guard. (BLOCKING)
  132. AIO evidence ↔ sitemap discoverability: every text document registered as authoritative
       evidence in .well-known/aio-manifest.json (source_of_truth / supporting_evidence /
       observational_evidence whose path ends in .md / .txt / .json) must also appear as a <loc> in
       sitemap.xml. The manifest declares a doc authoritative for AI crawlers, but a crawler that
       discovers the site via sitemap.xml will never reach a registered doc that is absent from the
       sitemap — a silent discoverability gap (real-work-claims.md and AI2AI-archive.md were
       registered but missing from the sitemap until this Check was added). Binary assets
       (.webp/.mp3) are excluded (images/audio are not sitemap-indexed text). This makes
       "registered-as-evidence ⟹ sitemap-discoverable" an enforced invariant. (BLOCKING)
  133. AIO guard script wiring: aio-guard.js is the AIO asset-anchor lifecycle monitor & self-repair
       mechanism — it watches the hidden <div id="aio-asset-anchor"> and restores it if any AI-run
       "dead code purge" removes it (the anchor is invisible but semantically critical to the AIO
       layer). The monitor only works if index.html actually loads it before the main SPA IIFE.
       The mirror-bijection check only asserts the FILE exists; nothing enforced that index.html
       still REFERENCES it, so deleting the <script src="./aio-guard.js"> tag would leave the file
       present (verify green) while silently deactivating the self-repair monitor — only a
       non-blocking CI advisory caught this. This Check asserts index.html contains a
       <script src="./aio-guard.js"> reference, making "guard file exists ⟹ guard is wired" an
       enforced invariant (regression guard for the AIO self-repair monitor). (BLOCKING)
  134. Root script wiring completeness: index.html must keep loading the root scripts it depends
       on (theme-init.js / karte-init.js / main.js) via a <script src> reference. Like Check 133
       (aio-guard.js), the mirror-bijection only asserts the FILE exists — nothing enforced that the
       <script> tag remains. Removal degrades SILENTLY: theme-init.js is the pre-paint FOUC guard
       (its loss is a flash of unstyled/wrong-theme content that no behavior e2e asserts, and the
       screenshot e2e is now ADVISORY per §3(B) so it would not block); karte-init.js silently
       disables analytics; main.js is the SPA entry point (e2e catches its loss, but a static check
       makes the entry-point wiring explicit and survives an e2e outage). error-suppressor.js is
       NOT covered here because it is inlined (Check 7/7b enforce its inline byte-identity + CSP
       hash), and aio-guard.js is covered by Check 133. This makes "root script file exists ⟹ it is
       wired into index.html" an enforced invariant for the remaining external root scripts.
       (BLOCKING)
  135. Stylesheet wiring: index.html must keep loading the local stylesheet style.css via a
       <link rel="stylesheet" href="./style.css">. This is the highest-impact member of the same
       "file exists ⟹ file wired" class as Checks 133/134 — if the link is removed, the ENTIRE site
       renders unstyled, yet the loss is silent to every gate: the behavior e2e only asserts content
       presence / routes (an unstyled page still has its text), the screenshot e2e is ADVISORY per
       §3(B), and no consistency check covered the link. style.css existence (Check 108 mirror) and
       byte-budget (Check 52/120) were enforced, but never its <link> wiring. External font
       stylesheets are intentionally NOT required (their loss degrades gracefully to fallback
       fonts). This makes "style.css exists ⟹ it is linked in index.html" an enforced invariant.
       (BLOCKING)
  136. demoRoute ↔ router app whitelist coherence: store.js normalizeProject() validates an imported
       project's demoRoute against a hardcoded app whitelist, and router.js resolves apps/<app> routes
       against its own hardcoded whitelist. These two lists must stay in sync — if router gains an app
       (e.g. 'notes' was added for the A-group Markdown notes app) but the store whitelist is not
       updated, importing a project whose demoRoute names the new app SILENTLY drops it to null (the
       demo button vanishes — a data-fidelity loss of the same class as Check 128 and the #139 profile
       strip). This Check parses both arrays and asserts the store demoRoute whitelist equals the router
       app whitelist, making "router supports app X ⟹ X is a valid project demoRoute" an enforced
       invariant. (BLOCKING)
  137. router app whitelist ↔ main.js render switch coherence: router.js resolves apps/<app> to
       route.name `app-<app>` for app in its whitelist, and main.js's renderer switch consumes that
       route.name via `case 'app-<app>':` to render the app component. Check 128 (cmdk) and 136 (store)
       constrain the PRODUCER side of the router whitelist, but the CONSUMER side (main.js switch) is
       only tied INDIRECTLY through ALL_ROUTES (Check 58) — so updating router + cmdk + store while
       forgetting main.js/ALL_ROUTES leaves every Check green yet makes apps/<app> fall through to
       not-found (a SILENT 404 while the palette and project demos still offer the route). This Check
       parses the router whitelist and the set of main.js `case 'app-<X>':` labels and asserts bijection,
       making "router can route app X ⟹ main.js can render app X" a directly enforced invariant (the
       missing direct edge in the app-route coherence mesh of Check 58/118/128/136). (BLOCKING)
  138. Sidebar app-nav ↔ router app whitelist coverage: the Sidebar (js/components.js) lab-nav lists
       built-in apps as `path: 'apps/<app>'` quick-nav links, and AppsPage lists every app as a card.
       Like the command palette (Check 128), the sidebar must cover every router-routable app — when the
       Markdown notes app was added (A-group) it was added to AppsPage + the palette (#257) but FORGOTTEN
       in the sidebar, so notes was the only built-in app unreachable from the persistent left nav. This
       Check parses the router whitelist and the sidebar's `path: 'apps/<app>'` entries and asserts every
       router app appears in the sidebar, making "router can route app X ⟹ X is in the sidebar nav" an
       enforced invariant (the sidebar counterpart of Check 128). (BLOCKING)
  139. AppsPage app index ↔ router app whitelist coverage: AppsPage (js/components.js) is the canonical
       "アプリ一覧" index — it renders every built-in app as a card whose "開く" button navigates to
       apps/<id>. It is the third app-route PRODUCER surface (with the palette/Check 128 and the
       sidebar/Check 138) but was the only one left unenforced. If the AppsPage `apps` array drifts from
       the router whitelist (a new app added to router/main.js/cmdk/sidebar but forgotten here), that app
       becomes undiscoverable from the canonical index even though it routes everywhere else. This Check
       scopes to the AppsPage `const apps = [...]` array, parses its `id: '<app>'` entries, and asserts
       every router app appears, completing the app-route coherence mesh so all three producer surfaces
       (palette/sidebar/AppsPage) track the router whitelist. (BLOCKING)
  140. Settings demo selector ↔ router app whitelist coverage: The Settings page manual-add form
       (js/apps.js SettingsPage) lets a user create a project and pick which app it demos via a
       `<select>` whose onchange writes `settingsNewDemo`. Its `<option value='<app>'>` list is the WRITE
       surface that decides which apps a hand-created project can ever link as a demoRoute. store.js
       normalizeProject accepts demoRoute ∈ router whitelist (Check 136) and the router can route every
       app, but if this selector drifts (a new app added to router/store/main.js/cmdk/sidebar/AppsPage but
       forgotten here), that app is silently unselectable as a demo — the exact recurring class where
       notes was forgotten in the store/sidebar/AppsPage/palette (#257/#292/#293). This Check scopes to
       the demo selector block, parses its non-empty `value: '<app>'` options, and asserts they equal the
       router whitelist (the empty "Demoなし" option is allowed), so every routable app stays selectable
       as a project demo. (BLOCKING)
  141. Default-project slug & id uniqueness: store.js defaultProjects (the hardcoded proj("pNN","slug",…)
       seed list) must have unique ids AND unique slugs. ProjectDetailPage resolves a project via
       find(p.slug === slug) and returns the FIRST match, so a duplicate slug silently makes the later
       project's detail page unreachable (the #154 class). User-added projects get a runtime slug-suffix
       dedup in addProjectManual, but the hardcoded defaults have NO such protection — a future data edit
       introducing a duplicate slug/id would ship a silently-unreachable project. This Check parses the
       proj(...) seed entries and asserts both id-set and slug-set are collision-free. (BLOCKING)
  142. Playwright e2e gate covers its own toolchain: playwright-regression.yml (the BLOCKING
       behavior/functionality e2e gate) is path-filtered to shipped-site files so it skips on
       unrelated commits. But the e2e TOOLCHAIN itself — @playwright/test (the runner) and
       @axe-core/playwright (a11y assertions) plus transitive deps — lives in the dependency
       manifest, and a bump there can change e2e behavior with NO shipped-site file changing.
       Without package.json/package-lock.json in the trigger, such a bump skips the behavior gate
       and ships an unverified test-toolchain change (observed: PR #318 bumped @axe-core/playwright
       and playwright-validation never ran). This Check asserts both manifest files are present in
       the workflow's pull_request paths filter, keeping "the gate that proves e2e behavior"
       wired to "the files that can change e2e behavior" (the CI-trigger version of the
       file-exists≠file-wired class, cf. Check 133/134/135). (BLOCKING)
  143. Auto-digest workflow covers every digested manifest file: .well-known/aio-manifest.json
       registers source_of_truth / supporting_evidence / observational_evidence entries each with a
       sha256 digest. auto-update-aio-digests.yml is the automation that regenerates those digests
       on a push to main, and it is path-filtered. If a digested file is absent from that paths
       filter, editing it on main won't auto-refresh its digest (observed drift: real-work-claims.md
       was added to the manifest in Session #21 but never to the workflow paths). This Check asserts
       every manifest entry that has BOTH a repo-relative path AND a sha256 is covered by the
       workflow's push paths — either as a literal entry or via a `prefix/**` glob — keeping "the
       files the manifest digests" wired to "the automation that maintains those digests" (the
       producer/consumer-drift / file-exists≠file-wired class, cf. Check 132/142). (BLOCKING)
  144. Digest-regen tool's file map matches the manifest: update_aio_digests.py is the automation
       that recomputes manifest sha256 digests, and the EXACT set of files it can refresh is the
       hardcoded MANIFEST_PATH_TO_LOCAL dict. Check 143 guarantees the WORKFLOW fires on a digested
       file's change, but once fired the tool can only refresh files present in this dict. If a
       manifest entry has a sha256 but no dict key, the workflow fires yet that file's digest is
       never recomputed — and since the tool can't fix it, the BLOCKING check_aio_digests.py gate
       becomes un-auto-fixable (a human must hand-compute the sha256). This Check asserts the dict's
       key set is a bijection with the manifest's digested-path set (every dict key is a digested
       manifest path AND every digested manifest path is a dict key), closing the consumer-side edge
       of the digest-automation chain (paths→tool-dict→manifest), cf. Check 143. (BLOCKING)
  145. GitHub Actions are pinned to a full commit SHA: every `uses: owner/repo@ref` in
       .github/workflows/*.yml must pin `ref` to a full-length 40-hex commit SHA, never a mutable
       tag (@v6) or branch (@main). A mutable tag can be silently re-pointed (or hijacked) upstream
       so a workflow runs different code with no repo change — the supply-chain analog of the silent
       weakening this repo already guards against (Check 67 permissions / 76 settings deny / 115 CSP
       anti-weakening). Third-party actions (e.g. peter-evans/create-pull-request) are the highest
       attack surface. This Check parses every uses: ref and asserts a 40-hex SHA (local `./` actions
       are exempt), preventing regression to mutable tags; the human-readable `# vN` comment stays
       and dependabot (github-actions, Check 68) keeps the pins current. (BLOCKING)
  146. Default projects' relatedProjectIds are referentially intact: every id listed in a
       defaultProjects entry's relatedProjectIds (store.js) must reference an actually-existing
       default project id. A dangling reference (a typo'd or removed-project id) is SILENT: the
       related-projects UI falls back to autoRelatedCandidates (a similarity score), which quietly
       fills the gap so the section still looks populated — the curator's explicit, intended
       relation is lost with no visible symptom (the graceful-fallback-masks-a-bug class, cf. the
       NotFound/FatalPage vacuous-pass lesson). This Check collects the project-id set (proj() first
       arg) and every pNN id referenced in a relatedProjectIds array literal, asserting no reference
       is dangling (and that some references exist, so it can't pass vacuously). Sibling of Check 141
       (which guards id/slug uniqueness); this guards referential integrity. (BLOCKING)
  147. Speakable cssSelector tokens point to live shipped elements: every #id / .class token in
       js/meta-management.js's SPEAKABLE_SELECTORS literal (the route-keyed AIO wiring that drives
       JSON-LD SpeakableSpecification) must appear as a literal token somewhere in the shipped DOM
       corpus (index.html ∪ js/*.js ∪ main.js, minus meta-management.js itself to avoid self-match).
       A dangling selector (referencing an element that no renderer emits) is SILENT: the
       SpeakableSpecification still ships, but voice assistants find no node and silently fail to
       extract — an AIO precision regression with no console error and no behavior-test signal. This
       is a demonstrated bug-class: the [FIX] history block above SPEAKABLE_SELECTORS (L152-156)
       records hand-removal of dead .hero-tagline / .core-thesis selectors and a .role-split-table
       → #role-split-table correction, never systematized. This Check parses the object literal
       (arrays only, so route keys are not mis-scanned), exempts generic catch-alls (h1 /
       [data-speakable] / .sr-only / .sr-only[data-ai-entity] and attribute-only selectors), and
       asserts each remaining #id/.class token exists in the corpus by word-boundary literal scan.
       Fails vacuously if SPEAKABLE_SELECTORS cannot be extracted or yields zero non-generic tokens
       to check. (BLOCKING)
  148. SITE_CONFIG.ARTICLE_ROUTES ⊆ PAGE_META keys (Article JSON-LD route coherence): every route
       name listed in SITE_CONFIG.ARTICLE_ROUTES (main.js — the routes that get og:type=article and
       an injected Article JSON-LD node) must exist as a top-level key in PAGE_META (js/page-meta.js).
       A dangling ARTICLE_ROUTES entry is SILENT: applyMeta() early-returns when meta is missing,
       leaving fullTitle/desc empty; injectStructuredData() still runs (it does not consult
       PAGE_META) and emits an Article node with empty headline/description — a silently malformed
       AIO surface with no console error and no behavior-test signal (sibling class to Check 147
       dangling Speakable selectors). This Check parses the array literal in main.js, parses
       PAGE_META top-level keys (4-space-indented `key: {` form), and asserts ARTICLE_ROUTES is
       non-empty, PAGE_META is non-empty, and the subset holds. (BLOCKING)
  149. Canonical URL three-way coherence (`<link rel="canonical">` ↔ aio-manifest.json
       entity.canonical_url ↔ main.js SITE_CONFIG.CANONICAL_URL): the canonical URL string must be
       byte-identical across all three primary declaration surfaces. Drift is SILENT but corrupts
       AIO entity identity — AI crawlers see conflicting canonical signals from different surfaces
       and cannot anchor the entity to one URL (the entire AIO surface is built on this single
       string being the authoritative identifier). Check 62 already enforces manifest ↔ llms-full.txt
       coherence; this Check closes the third edge (the link rel=canonical + the runtime SITE_CONFIG
       used by dynamic JSON-LD injection). Trailing slashes and origin must match exactly. (BLOCKING)
  150. og:url ↔ canonical URL coherence: the index.html `<meta property="og:url">` content must be
       byte-identical to the `<link rel="canonical">` href. Drift is SILENT — the OG/social card
       preview (LinkedIn / Slack unfurl / Twitter / Discord) shows a different URL than the
       canonical link, and AI/social crawlers may resolve to a different entity URL than the
       authoritative one. Extends the Check 149 canonical-URL invariant to the social/OG surface,
       which is the most-shared external mention of the site. (BLOCKING)
  151. e2e test() title uniqueness: every `test('...', ...)` title in e2e/portfolio.spec.js must be
       unique. Duplicate titles are SILENT in some Playwright reporters (the second run silently
       overrides the first's record) and always reduce diagnostic clarity — a class of
       vacuous-test-pair where one test's failure may be misattributed or masked by the other's
       pass. This Check parses all `test('...'` direct invocations and asserts the title multiset
       has no duplicates. (BLOCKING)
  152. `<html lang>` ↔ JSON-LD `inLanguage` coherence: the index.html `<html lang>` attribute and
       every JSON-LD `"inLanguage": "..."` declaration across index.html, main.js, and
       js/meta-management.js must declare the same language code. Drift is SILENT — AI/SEO crawlers
       see conflicting language signals (e.g. `<html lang="ja">` but JSON-LD `inLanguage: "en"`)
       and may misclassify the content's primary language, degrading discovery in language-scoped
       search and AIO. This Check collects all values into a single set and asserts cardinality 1
       (single canonical language), with `<html lang>` present and at least one JSON-LD inLanguage
       declaration found. (BLOCKING)
  153. og:image / twitter:image origin uses canonical URL prefix: every index.html `<meta
       property="og:image">` and `<meta name="twitter:image">` content URL must start with the
       `<link rel="canonical">` href (sharing the same origin + path prefix). Drift is SILENT — the
       social/OG card preview shows an image from a different origin, breaking the entity-asset
       coupling and possibly serving a stale or third-party image. Extends the Check 149/150
       canonical-URL invariant to the image surface of OG/Twitter cards (the visual portion of any
       external mention of the site). Both meta tags must be present; either drifting from the
       canonical prefix fails the Check. (BLOCKING)
  154. og:description ↔ twitter:description coherence + 3-way presence: the index.html `<meta
       property="og:description">` and `<meta name="twitter:description">` content must be
       byte-identical (both are card-preview descriptions with the same length budget), and
       `<meta name="description">` (the longer SERP-targeted description) must also be present.
       Drift between og: and twitter: descriptions is SILENT — different social/AI crawlers show
       different card text for the same page (LinkedIn/Slack vs Twitter), splitting the entity
       narrative. The `<meta name="description">` is intentionally a different (longer) string for
       SERP/AI crawler ingestion, so this Check does NOT require it to match og/twitter; only that
       it exists (vacuous-guard against silent removal). (BLOCKING)
  155. og:title ↔ twitter:title coherence: the index.html `<meta property="og:title">` and
       `<meta name="twitter:title">` content must be byte-identical. Both are card-preview titles
       with the same length budget; drift is SILENT — LinkedIn/Slack/OG consumers see one title
       while Twitter shows another, splitting the entity headline across social surfaces. Sibling
       of Check 154 (description coherence) for the title axis. The `<title>` tag is intentionally
       allowed to differ (different length budget for SERP vs cards), so this Check restricts to
       og/twitter pair only. Both meta tags must be present and equal. (BLOCKING)
  156. og:type valid enumeration + og:site_name presence: the index.html `<meta property="og:type">`
       must have a content value in the small valid OG type enumeration used by this site
       ('website' or 'article' — the only types referenced by meta-management.js's dynamic injection
       per SITE_CONFIG.ARTICLE_ROUTES), and `<meta property="og:site_name">` must be present (any
       non-empty value). Silent removal of og:site_name strips the site identifier from card
       previews (entity context loss); an invalid og:type value (typo / removed enumeration member)
       leaves social crawlers fallback to a generic preview, losing article-vs-page disambiguation.
       This Check is a presence + enumeration sanity gate, complementing the dynamic-injection
       coverage of Check 148 (ARTICLE_ROUTES ⊆ PAGE_META). (BLOCKING)
  157. Mobile / PWA baseline meta presence: the index.html `<head>` must declare a non-negotiable
       baseline of platform meta tags — `<meta charset="utf-8">`, `<meta name="viewport">`,
       `<meta name="theme-color">` (any media variant), `<link rel="icon">`, and `<link
       rel="apple-touch-icon">`. Silent removal causes regressions that mostly do not break the
       behavior e2e: missing viewport → mobile zoom is broken (no `width=device-width` scale=1),
       missing icon → browser tab and bookmark show a generic globe, missing apple-touch-icon →
       iOS Add-to-Home-Screen uses a downscaled screenshot, missing theme-color → mobile address
       bar / OS card chrome stays default. Each of these is shipped today; this Check enforces
       presence-only (content correctness is out of scope) as a vacuous-removal guard. (BLOCKING)
  158. Google Fonts preconnect / dns-prefetch presence (CWV first-paint guard): index.html must
       keep `<link rel="preconnect" href="https://fonts.googleapis.com">`, `<link rel="preconnect"
       href="https://fonts.gstatic.com">`, and `<link rel="dns-prefetch" href="https://
       fonts.googleapis.com">`. The site loads Google Fonts CSS + binary; these resource hints save
       ~100-200ms of DNS+TLS+handshake latency on first paint. Silent removal regresses LCP/FCP
       without any console error or behavior-test signal, and the regression is hard to bisect
       later (the missing hints are just slow, not broken). Three-marker presence check; any one
       missing fails. (BLOCKING)
  159. JSON-LD `@context` cross-surface coherence: every `"@context"` (or `'@context'`) value in
       JSON-LD scattered across index.html (static blocks) + main.js + js/meta-management.js
       (dynamic injections) must be the single canonical value `https://schema.org`. Drift to a
       trailing slash, an http:// variant, or a different schema vocabulary is SILENT — JSON
       parses, the block ships, but AI/SEO crawlers fail to recognize the schema and the entire
       structured-data signal collapses to "unknown vocabulary". Collected into a single set with
       cardinality 1 expected (the universally accepted canonical URL). (BLOCKING)
  160. sw.js hardcoded paths share the canonical URL pathname: every absolute path string in sw.js
       that starts with a `/<segment>/` form (e.g. the AIO_FILES list) must use the same first
       path-segment as the `<link rel="canonical">` href's pathname (e.g. `/portfolio/`). Drift is
       SILENT — if the GitHub Pages project is renamed (or the canonical URL's path changes), the
       SW continues to register but its hardcoded paths no longer match any incoming request URLs,
       so SW-cached AIO file requests silently miss the SW interception layer. Skips literal `/`
       (root). (BLOCKING)
  161. robots.txt User-agent: * baseline presence: robots.txt must declare a `User-agent: *` block
       and that block must permit crawling (no `Disallow: /` directive in it). Silent regression to
       `Disallow: /` would deindex the entire site from all generic crawlers (AI + search) — a
       category-collapse for an AIO-first site that the behavior e2e cannot detect (it runs against
       localhost, not the deployed crawl policy). This Check parses the `User-agent: *` section
       (up to the next `User-agent:` line) and asserts no full-site disallow is present. (BLOCKING)
  162. `.gitignore` baseline ignore-rules for CI/build artifacts: `.gitignore` must declare ignore
       rules for `node_modules/`, `__pycache__/`, `/test-results/`, `/playwright-report/`, and
       `/blob-report/`. Silent removal would allow accidental `git add <file>` of CI artifacts and
       node_modules (hundreds of MB) to land in the repo. Check 37 catches the artifact files
       themselves after they're tracked, but this Check protects the gate upstream so they never
       arrive in the staging area. (BLOCKING)
  163. `<link rel="icon">` / `<link rel="apple-touch-icon">` href resolves to an actual file:
       every non-data: href in `<link rel="icon">` and `<link rel="apple-touch-icon">` tags in
       index.html must resolve to an existing repo file (the canonical URL pathname is stripped to
       map href to repo-relative path). A dangling href ships a broken icon and is SILENT: the
       browser falls back to a default globe icon and the apple-touch-icon path returns 404 on iOS
       Add-to-Home (which then uses a downscaled site screenshot instead of the curated icon).
       data: URI hrefs (inline SVG fallbacks) are exempt. (BLOCKING)
  164. og:image / twitter:image content URL resolves to an actual file: the index.html
       `<meta property="og:image">` and `<meta name="twitter:image">` content URLs must resolve to
       existing repo files (after stripping the canonical URL prefix to get the local path). A
       dangling image is SILENT — social/OG card previews show a broken image with no console
       error or behavior-test signal. Extends Check 153 (canonical URL prefix) and Check 163
       (icon href resolves) to the social card image surface. (BLOCKING)
  165. `.well-known/api-catalog` JSON + anchor canonical origin: `.well-known/api-catalog` must be
       valid JSON with a `linkset` array containing at least one entry, and the `anchor` URL of the
       first linkset entry must start with the canonical URL (from `<link rel="canonical">`). A
       drift / malformed file silently breaks AI crawler discovery of authoritative API endpoints
       (the catalog is the entry point that points to mcp.json / agent-skills / aio-manifest /
       llms-full). (BLOCKING)
  166. sitemap.xml `<loc>` URLs all start with canonical URL prefix: every `<loc>` URL in
       sitemap.xml must start with the `<link rel="canonical">` href value (full prefix, not just
       origin). Check 63 enforces origin alignment only; this Check tightens to the full canonical
       URL (origin + base path). Drift to a sibling project path (e.g. `/portfolio2/about`) is
       SILENT — sitemap crawlers index URLs that 404 on the deployed site. (BLOCKING)
  167. `aio-monitoring.yml` weekly schedule presence: the AIO monitoring workflow must declare a
       `schedule.cron:` trigger. Silent removal stops the weekly AIO discovery/citation
       observability loop without any visible regression — the workflow just stops firing, and
       observability data goes stale. (BLOCKING)
  168. aio-manifest entity.architecture references C1/C2/C3 markers: the
       `entity.architecture` string in aio-manifest.json must contain the three architectural
       constraint markers "Vanilla JS", "IIFE", and "ErrorBoundary" (corresponding to C1/C2/C3 in
       AI2AI.md STEP 2). Drift would silently weaken the AIO entity's architectural identity
       declaration — AI crawlers reading the manifest would no longer see this site as a Boring-
       Technology Vanilla JS SPA. Mirror of CLAUDE.md §1 architecture statement on the manifest
       side. (BLOCKING)
  169. aio-manifest entity.role contains canonical role markers: the `entity.role` list in
       aio-manifest.json must contain the three canonical role identifiers from CLAUDE.md §1:
       "AI-Driven PM", "IT Consultant", and "KERNEL Framework Designer". Drift silently weakens
       the AIO entity's professional role declaration that AI crawlers read for entity
       disambiguation. (BLOCKING)
  170. aio-manifest entity.disambiguation contains negative-disambiguation markers: the
       `entity.disambiguation` string in aio-manifest.json must contain the canonical
       negative-identity markers ("academic researcher", "diplomat", "artist", "patent inventor")
       from CLAUDE.md §1, which explicitly distinguish this entity from namesakes in other fields.
       Drift silently weakens the disambiguation signal — AI crawlers may conflate this entity
       with academic Yuta Yokoi researchers in agriculture/chemistry/medicine/etc. (BLOCKING)
  171. index.html `ai:*` meta URL tags share canonical URL prefix: the four URL-bearing
       `<meta name="ai:*">` tags in index.html (`ai:context`, `ai:entrypoint`, `ai:canonical`,
       `ai:aio-manifest`) must each have a content URL starting with the canonical URL prefix
       (from `<link rel="canonical">`), and `ai:canonical` must equal canonical exactly. Drift
       silently desynchronizes the AIO meta layer from the canonical-URL family (e.g. AI crawler
       following `ai:context` hits a 404 if a sibling-project path is mistakenly used). (BLOCKING)
  172. aio-manifest entity name variants cover canonical identifiers: the combined
       (`entity.name` + `entity.name_ja` + `entity.name_alt`) fields in aio-manifest.json must
       collectively cover all 4 canonical name identifiers from CLAUDE.md §1: "Yuta Yokoi",
       "横井雄太", "Yokoi Yuta", and "yuta". Drift (one variant dropped) silently weakens the
       AIO entity matching — AI crawlers querying for the missing variant may not find this
       entity. (BLOCKING)
  173. js/identity.js AUTHOR canonical values: the AUTHOR constants in js/identity.js (DISPLAY_NAME,
       AUTHORITATIVE_NAME, JAPANESE_NAME) must hold their canonical values — DISPLAY_NAME='yuta'
       (visible UI anonymity per Check 124), JAPANESE_NAME='横井雄太', and AUTHORITATIVE_NAME
       contains both "Yuta Yokoi" and "横井雄太". Drift would silently break the shipped JS layer
       that renders entity-bearing JSON-LD (Person @type) and sr-only entity anchors. Sibling to
       Check 172 on the aio-manifest side. (BLOCKING)
  174. `<meta name="theme-color">` values exist as literals in style.css: every theme-color content
       value in index.html (multiple media-scoped variants permitted) must appear as a literal
       string somewhere in style.css, ensuring the mobile address bar / OS card chrome color
       matches a real brand color present in the stylesheet. Drift silently desyncs the OS chrome
       from the visual brand (the address bar shows a color the site no longer uses anywhere).
       (BLOCKING)
  175. package.json `private: true` + name baseline: package.json must declare `"private": true`
       and `"name": "portfolio-aio"`. Silent removal of `private: true` would allow `npm publish`
       to succeed and leak internal dev config to the public npm registry — a security regression
       with no console error. The `name` value anchors npm tooling identification. (BLOCKING)
  176. index.html static JSON-LD `@id` URLs share canonical URL prefix (own-origin only): every
       `"@id": "URL"` in index.html where URL is on this site's origin
       (yutapr0117-design.github.io) must start with the canonical URL prefix (from
       `<link rel="canonical">`). External-origin @id (e.g. nkgr.co.jp for Organization) are
       exempt. Drift would silently break JSON-LD entity graph linking when canonical URL path
       changes (e.g. project rename); the entity's #person/#webpage/#website anchors would still
       use the old prefix and AI crawlers couldn't follow the graph. (BLOCKING)
  177. llms-full.txt `**Version:**` matches main.js SITE_CONFIG.VERSION: the version marker in
       llms-full.txt's authority header must equal `SITE_CONFIG.VERSION` from main.js. Drift would
       silently desync the AI-authoritative context's stated version from the live site —
       AI/agent ingesting llms-full.txt would think they're seeing a different version than
       what's actually deployed. Extends the version-coherence mesh (Check 1/2/3/19) to the
       llms-full.txt surface. (BLOCKING)
  178. `<meta name="ai:repository">` derives from canonical URL: the GitHub repo URL in
       `<meta name="ai:repository">` must equal `https://github.com/<owner>/<repo>` where
       owner+repo are derived from the canonical URL (hostname's first segment + URL path's
       first segment). Drift would silently point AI crawlers to the wrong GitHub repo when
       canonical URL changes (project rename / fork). (BLOCKING)
  179. `<meta name="ai:version">` matches main.js SITE_CONFIG.VERSION: the version string
       declared to AI crawlers in `<meta name="ai:version">` must equal SITE_CONFIG.VERSION
       in main.js. Drift would silently desync the AI-facing version signal from the
       running app's pipeline version, so AI agents would believe they're crawling a
       different version than what's actually deployed. Extends the version-coherence mesh
       (Check 1/2/3/19/177) to the index.html ai:* meta surface. (BLOCKING)
  180. `<meta name="ai:last-modified">` matches main.js SITE_CONFIG.LAST_UPDATED: the
       last-modified date in `<meta name="ai:last-modified">` must equal SITE_CONFIG
       .LAST_UPDATED in main.js. Drift would silently lie to AI crawlers about freshness,
       confusing recency-weighted retrieval (e.g. AI search ranking by ai:last-modified
       could surface a stale view while the app has actually been updated, or vice
       versa). Sibling Check of 179 for the timestamp axis of the ai:* meta surface.
       (BLOCKING)
  181. main.js SITE_CONFIG.LAST_UPDATED is ISO-8601 (YYYY-MM-DD) and a real calendar
       date: the LAST_UPDATED string in main.js SITE_CONFIG must match strict
       `YYYY-MM-DD` and parse as a valid date. Free-form / locale-specific formats
       (e.g. '2026/05/31', '5/31/26') would silently survive Check 180 (byte-identical
       check) and propagate to ai:last-modified, but AI/SEO crawlers expect ISO-8601
       and would either drop the freshness signal entirely or misparse the date.
       Centralizes the format invariant at the source (SITE_CONFIG) so all downstream
       coherence (Check 91 / 180) implicitly inherits ISO-8601 correctness. (BLOCKING)
  182. ai:* meta URL endpoints resolve to actual repo files: the URL content of
       `<meta name="ai:context">`, `<meta name="ai:entrypoint">`, and
       `<meta name="ai:aio-manifest">` must map (via canonical-URL strip) to an
       existing repo file. Check 171 enforces only the canonical URL *prefix*; if the
       path after the prefix drifts (e.g. `llms-full.txt` renamed to
       `llms-context.txt` but ai:context not updated, or the manifest moved), 171
       still passes but the URL 404s when AI crawlers fetch it — silent discovery
       collapse. Sibling of Check 163/164 (icon/og:image file resolution) for the
       ai:* meta surface. (BLOCKING)
  183. sitemap.xml `<lastmod>` values are strict ISO-8601 YYYY-MM-DD: every
       `<lastmod>` element in sitemap.xml must match strict `YYYY-MM-DD` and parse as
       a valid calendar date. The W3C Datetime / sitemap protocol both allow more
       liberal formats (`YYYY-MM-DDThh:mm:ss+00:00`, `YYYY/MM/DD`, etc.), but most
       crawlers normalize to date-only and locale formats break parsers silently.
       Centralizing on strict YYYY-MM-DD avoids ambiguity. Sibling of Check 65 (docs
       ISO-8601) and Check 181 (SITE_CONFIG.LAST_UPDATED ISO-8601) for the sitemap
       surface. (BLOCKING)
  184. sw.js AIO_FILES paths resolve to actual repo files: every path listed in
       sw.js's `AIO_FILES` array (the special SWR fetch-intercept list) must map (via
       canonical-URL pathname strip) to an existing repo file. Check 160 enforces
       only the first-segment pathname coherence; if the path tail drifts (e.g.
       `/portfolio/llms.txt` renamed to `/portfolio/llms-entry.txt` but sw.js not
       updated), the SW would attempt to SWR a non-existent endpoint forever and
       silently 404 every cache miss while looking healthy. Sibling of Check 182
       (ai:* meta endpoint resolves) for the service-worker AIO surface. (BLOCKING)
  185. Canonical URL uses HTTPS scheme: the `<link rel="canonical">` href in
       index.html must start with `https://`. Drift to `http://` would silently
       degrade SEO/security signals — browsers warn "Not Secure", crawlers may treat
       the page as a different origin from HTTPS variants and split entity identity,
       and Mixed Content blocks would silently break sub-resource loads in places.
       Check 149 (3-way canonical coherence) catches partial drift, but if all 3
       surfaces flip to HTTP it passes — this check anchors the scheme itself.
       (BLOCKING)
  186. `<meta name="author">` content contains canonical entity identifiers: the
       `<meta name="author">` content in index.html must contain BOTH "Yuta Yokoi"
       AND "横井雄太" (the canonical name pair from CLAUDE.md §1). Drift would
       silently desync the HTML-surface author signal from the entity identity
       (sr-only / JSON-LD / AIO surfaces remain correct, but generic SEO/HTML
       crawlers that read `<meta name="author">` would see a different entity).
       Sibling of Check 173 (js/identity.js AUTHOR) and Check 172 (aio-manifest
       entity name variants) for the HTML <meta name=author> surface. (BLOCKING)
  187. `<meta property="og:locale">` language code matches `<html lang>`: the
       language sub-tag of og:locale (e.g. `ja_JP` → `ja`) must equal the
       `<html lang>` attribute (e.g. `ja`). Drift would silently send conflicting
       language signals to social/OG crawlers (LinkedIn/Slack/Facebook unfurl) vs
       browsers and SEO crawlers — preview cards would localize to a different
       audience than the page itself. Sibling of Check 152 (lang ↔ JSON-LD
       inLanguage) for the og:locale surface. (BLOCKING)
  188. robots.txt `Sitemap:` URL resolves to actual repo file: the `Sitemap:`
       directive URL in robots.txt must (after stripping the canonical URL
       pathname) map to an existing repo file. Check 63 enforces origin coherence
       but not the path tail — rename of `sitemap.xml` (e.g. to `sitemap-v2.xml`)
       without updating robots.txt would silently 404 the sitemap pointer, so
       crawlers like Googlebot would skip indexing every URL the sitemap was meant
       to declare. Sibling of Check 182/184 (ai:* / sw.js endpoint resolves) for
       the robots.txt surface. (BLOCKING)
  189. `<meta name="robots">` does not contain `noindex` / `none`: the
       `<meta name="robots">` content in index.html must NOT contain `noindex` or
       `none` (negative invariant — presence-of-allow rather than absence-of-deny
       is implicit in non-noindex). A silent drift to `noindex` would deindex the
       entire site from all search engines (Google/Bing/DuckDuckGo + AI search
       backed by these) — a catastrophic AIO discovery failure invisible to
       browser/console/behavior e2e. Companion to Check 161 (robots.txt full-site
       disallow guard) for the HTML meta robots surface. (BLOCKING)
  190. `.nojekyll` file presence (GitHub Pages Jekyll bypass): the repository root
       must contain an empty `.nojekyll` file. Without it, GitHub Pages runs
       Jekyll on the deployed content — Jekyll silently ignores files / directories
       starting with `_` (e.g. `docs/files/_template.md`, `_assets/`), strips
       certain metadata, and applies layout munging. Loss of `.nojekyll` is
       invisible to browser/console/behavior e2e (the homepage still renders) but
       breaks underscore-prefixed paths silently. Presence-only check (file may be
       empty). (BLOCKING)
  191. CNAME file absence (canonical URL is github.io subdomain): the repository
       root must NOT contain a `CNAME` file (negative invariant). The canonical
       URL (`https://yutapr0117-design.github.io/portfolio/`) is a GitHub Pages
       subdomain, not a custom domain. Adding a CNAME file would silently
       redirect GitHub Pages deployment to that custom domain — if the domain
       is unconfigured / unowned, the entire site 404s; if it's owned but
       unconfigured, AIO entity canonical URL diverges from the actual served
       URL (silent breaking of every URL coherence Check). Companion of Check
       190 (.nojekyll presence) — the two are the structural baseline for
       canonical GitHub Pages deployment. (BLOCKING)
  192. JSON-LD Person `url` matches canonical URL: in the static JSON-LD Person
       block in index.html, the `url` property must equal the canonical URL
       (`<link rel="canonical">` href). Drift would silently desync the entity's
       declared homepage from the canonical page that crawlers actually index,
       breaking AI/social crawler entity-to-page linking. Sibling of Check 176
       (@id own-origin canonical prefix) for the `url` property axis. (BLOCKING)
  193. JSON-LD WebSite `url` matches canonical URL: in the static JSON-LD WebSite
       block in index.html, the `url` property must equal the canonical URL
       (`<link rel="canonical">` href). Drift would silently desync the WebSite
       entity's declared URL from the canonical page, breaking JSON-LD
       WebSite-to-page anchor and confusing Search Console "About this result"
       enrichment. Sibling of Check 192 (Person.url) for the WebSite axis.
       (BLOCKING)
  194. JSON-LD WebPage `url` matches canonical URL: in static JSON-LD WebPage
       blocks in index.html, the `url` property must equal the canonical URL.
       Drift would silently desync the page entity's declared URL from the
       canonical page, breaking AI/search-engine page-to-canonical resolution
       (the WebPage block is the most-directly-page-mapped JSON-LD entity).
       Completes the Person/WebSite/WebPage URL-coherence triangle for the
       canonical-URL anchor (Checks 192 + 193 + 194). (BLOCKING)
  195. JSON-LD Person `alternateName` contains canonical name variants: in the
       primary JSON-LD Person block in index.html, the `alternateName` array
       must contain BOTH "横井雄太" AND "Yokoi Yuta" (canonical name variants
       from CLAUDE.md §1). Drift would silently weaken AI entity-matching for
       queries using these variants (Google/AI search by 横井雄太 / Yokoi
       Yuta wouldn't anchor back to this Person entity). Sibling of Check 172
       (aio-manifest entity.name_alt) and Check 173 (js/identity.js AUTHOR) for
       the JSON-LD Person.alternateName surface. (BLOCKING)
  196. JSON-LD Organization (nkgr.co.jp) `name` = "株式会社日本経営": in
       index.html, the JSON-LD Organization block with `@id` containing
       `nkgr.co.jp/#organization` must have `name` "株式会社日本経営" (the
       canonical affiliation name from CLAUDE.md §1). Drift would silently
       desync the JSON-LD Organization entity from the canonical affiliation
       declaration shared by WebP XMP (Check 81) / MP3 ID3 (82) / aio-manifest
       (83) / README (84) / Claude2Claude (85). Completes the affiliation-name
       coherence mesh with the JSON-LD surface. (BLOCKING)
  197. JSON-LD Organization (nkgr.co.jp) `url` = "https://nkgr.co.jp/": in the
       Organization block from Check 196, the `url` property must be
       `https://nkgr.co.jp/` (the canonical Organization URL from CLAUDE.md
       §1). Drift would silently send AI/social crawlers to the wrong
       Organization homepage, breaking employee→employer URL resolution. URL
       axis sibling of Check 196 (name axis). (BLOCKING)
  198. JSON-LD Person `jobTitle` contains canonical role markers: in the
       primary JSON-LD Person block, the `jobTitle` string must contain BOTH
       "IT Consultant" AND "KERNEL Framework Designer" (canonical role markers
       from CLAUDE.md §1). Drift would silently weaken the Person entity's
       professional role declaration on AI/search-engine entity panels.
       Sibling of Check 169 (aio-manifest entity.role) for the JSON-LD
       Person.jobTitle surface. (BLOCKING)
  199. JSON-LD Person `knowsAbout` contains technical positioning anchors: in
       the primary JSON-LD Person block, the `knowsAbout` array must contain
       BOTH "KERNEL Framework" AND "Vanilla JavaScript SPA" (the unique
       technical positioning anchors that distinguish this entity from
       generic AI / PM practitioners). Drift would silently weaken AI search
       discovery for queries like "KERNEL Framework" or "Vanilla JavaScript
       SPA AI" (knowsAbout feeds Knowledge Panel topics & expert-finder
       systems). (BLOCKING)
  200. JSON-LD Person `@id` derives from canonical URL: in the primary
       JSON-LD Person block, the `@id` must equal canonical URL + "#person"
       (e.g. `https://yutapr0117-design.github.io/portfolio/#person`).
       Drift would silently break the JSON-LD entity graph anchor: secondary
       Person references (e.g. `{"@id": "...#person"}` inside creator /
       author / about properties) reference this @id by string equality; if
       primary @id drifts but references don't, the entity graph fragments
       into disjoint nodes. The trailing-slash + #person fragment derivation
       is mechanically checkable. (BLOCKING)
  201. JSON-LD WebSite/WebPage `@id` derive from canonical URL: in index.html
       JSON-LD, the primary WebSite block's `@id` must equal canonical URL +
       "#website" and the primary WebPage block's `@id` must equal canonical
       URL + "#webpage". Drift would fragment the entity graph in the same
       way Check 200 catches for Person — secondary `isPartOf:{"@id":...
       #website}` and `mainEntity:{"@id":...#webpage}` references would
       point to dead anchors. Completes the Person/WebSite/WebPage @id
       anchor triangle that started in Check 200. (BLOCKING)
  202. Canonical URL pathname ends with `/`: the `<link rel="canonical">`
       href pathname must end with a trailing slash. Drift (canonical →
       `.../portfolio` without slash) would silently break every Check that
       uses canonical URL as a prefix for repo-relative path stripping
       (Check 153 / 164 / 166 / 171 / 182 / 184 / 188): URLs like
       `https://.../portfolio/llms-full.txt` would no longer share a clean
       prefix with `.../portfolio` (no slash), and `startswith` checks would
       still pass (string prefix), but `[len(prefix):]` would strip too few
       characters and the path tail would start with `/`, breaking
       repo-relative resolution. The trailing-slash invariant is the implicit
       contract those Checks depend on. (BLOCKING)
  203. JSON-LD Person `givenName`/`familyName` canonical decomposition: in
       the primary JSON-LD Person block, `givenName` must equal "雄太" and
       `familyName` must equal "横井" (the canonical Japanese-order name
       decomposition from CLAUDE.md §1). Drift would silently send wrong
       name parts to Schema.org-aware AI/SEO crawlers, breaking last-name /
       first-name search alignment and Knowledge Panel name display.
       Sibling of Check 195 (Person.alternateName variants) for the
       structured name-decomposition axis. (BLOCKING)
  204. JSON-LD WebSite `name` contains site brand markers: in the primary
       JSON-LD WebSite block, the `name` string must contain BOTH "yuta"
       (display brand) AND "AI-Driven PM" (positioning identifier). Drift
       would silently desync the AI/SEO WebSite-level brand signal from the
       canonical title (Check 66 covers `<title>`, this covers JSON-LD
       WebSite.name surface). Sibling of Check 156 (og:site_name presence)
       for the JSON-LD WebSite.name axis. (BLOCKING)
  205. JSON-LD `url` fields all use HTTPS: every `"url": "<URL>"` in index.html
       JSON-LD must start with `https://` (negative invariant — no http://).
       Drift to http:// would silently downgrade AI/SEO crawler URL signals
       (browser Mixed Content blocking, search engines penalising insecure
       URLs, AI crawlers treating http vs https as different origins). Check
       185 (canonical link HTTPS) anchors only the canonical URL declaration;
       this Check extends scheme-anchor invariant to every JSON-LD url
       property across all entity blocks. (BLOCKING)
  206. JSON-LD `@id` URI fields all use HTTPS: every `"@id": "<URI>"` in
       index.html JSON-LD must start with `https://` (URN/other-scheme @ids
       are not used in this site). Drift to http:// would silently fragment
       the JSON-LD entity graph because @id is matched by string-equality —
       a Person @id with http:// would not equal references to https://#person
       elsewhere, splitting entities into disjoint nodes. Sibling of Check 205
       (url HTTPS) for the @id axis; complements Check 176 (own-origin @ids
       use canonical prefix, which is https) for the external-origin @ids
       (nkgr.co.jp/#organization etc.) that 176 does not check. (BLOCKING)
  207. index.html external `src=`/`href=` attributes all use HTTPS: every
       absolute-URL `src="<URL>"` or `href="<URL>"` in index.html that starts
       with a scheme must start with `https://` (negative invariant — no
       http://). Drift to http:// for external sub-resources (Karte CDN,
       Google Fonts CSS, etc.) would silently trigger browser Mixed Content
       blocking on the HTTPS site — the sub-resource silently fails to load
       (no console error in production builds, just missing functionality).
       Sibling of Check 205/206 (JSON-LD url/@id HTTPS) for the HTML element
       attribute axis. (BLOCKING)
  208. JSON-LD date fields are strict ISO-8601 YYYY-MM-DD: every
       `"datePublished"` / `"dateModified"` / `"dateCreated"` value in
       index.html JSON-LD must match strict `YYYY-MM-DD` regex AND parse as a
       valid calendar date. Drift to locale formats (`2026/05/31`, `5/31/26`)
       would silently corrupt freshness signals — Schema.org / Search Console
       consume these dates to determine recency-weighted ranking, and
       non-ISO-8601 dates either fail to parse (dropping freshness signal) or
       misparse (showing wrong "last updated"). Sibling of Check 183 (sitemap
       lastmod ISO-8601) for the JSON-LD date surface. (BLOCKING)
  209. JSON-LD potentialAction `target` URLs share canonical URL prefix: in
       index.html JSON-LD, every `target` URL inside any `potentialAction`
       block must start with the canonical URL prefix. Drift (e.g.
       ReadAction.target pointing at sibling project path) would silently
       advertise the wrong page to AI/voice assistants that consume
       potentialAction (the action would land on a 404). Sibling of Check 153
       (og:image canonical prefix) / Check 171 (ai:* canonical prefix) for
       the potentialAction.target surface. (BLOCKING)

  210. manifest.webmanifest `start_url` / `scope` match canonical URL pathname:
       the PWA manifest's `start_url` and `scope` fields must equal the
       pathname portion of `<link rel=canonical>` href (e.g. canonical
       `https://yutapr0117-design.github.io/portfolio/` → pathname `/portfolio/`).
       Drift would silently install the PWA pointing at a different URL than
       the AIO canonical entity URL, splitting authority signals between two
       URLs (the PWA install lands somewhere AI/search engines do not treat
       as the entity's canonical home). Sibling of Check 150 (og:url ↔
       canonical) / Check 138 (entity url) for the manifest install surface.
       (BLOCKING)

  211. JSON-LD `contentUrl` / `thumbnailUrl` fields share canonical URL prefix:
       in index.html static JSON-LD, every `"contentUrl": "..."` and
       `"thumbnailUrl": "..."` value (ImageObject / MediaObject / AudioObject)
       must start with the canonical URL prefix (own-origin assets). Drift
       (e.g. contentUrl pointing at a CDN or sibling project) would silently
       advertise non-canonical asset URLs to AI/SEO crawlers, splitting
       authority. Sibling of Check 153 (og:image canonical prefix) / Check
       171 (ai:* canonical prefix) / Check 209 (potentialAction.target
       canonical prefix) for the JSON-LD media-asset surface. (BLOCKING)

  212. manifest.webmanifest `icons[].src` is canonical-pathname-prefixed and
       each referenced file is committed: every icon `src` in manifest must
       start with canonical URL pathname (e.g. `/portfolio/`) AND the file
       (mapped to repo root by stripping the pathname prefix) must exist.
       Drift would silently make PWA install fail to load icons (icon path
       points outside the canonical scope, or the file was removed without
       updating manifest). Sibling of Check 210 (manifest start_url/scope
       canonical pathname) / Check 39 (sitemap loc resolves) for the
       manifest icon surface. (BLOCKING)

  213. HTML `<link rel="icon">` / `<link rel="apple-touch-icon">` href starts
       with canonical URL pathname (non-data: only): every non-data: href in
       these tags must start with the canonical URL pathname (e.g.
       `/portfolio/`). Drift (e.g. `/icon.svg` without the `/portfolio/`
       prefix) would silently 404 on production GitHub Pages deploy where the
       site is served under the canonical pathname. Check 163 covers
       file-existence; Check 213 covers canonical-pathname-prefix coherence.
       Sibling of Check 210 / 212 (manifest start_url/scope/icons canonical
       pathname) for the HTML head icon-link surface. (BLOCKING)

  214. JSON-LD `sameAs` URLs all use HTTPS: in index.html static JSON-LD,
       every URL inside any `"sameAs": [...]` array must start with `https://`.
       Drift would silently weaken AI/SEO trust signals (mixed-content
       warnings, authenticity-grade degradation in knowledge graph
       evaluation). Sibling of Check 206 (JSON-LD `@id` HTTPS) / Check 207
       (HTML src/href HTTPS) for the JSON-LD sameAs external-link surface.
       (BLOCKING)

  215. `<meta name="ai:last-modified">` and SITE_CONFIG.LAST_UPDATED are
       strict ISO-8601 YYYY-MM-DD (format + real calendar date): both date
       sources (the ai:* AIO meta and the main.js SITE_CONFIG constant)
       must match a strict `^\d{4}-\d{2}-\d{2}$` regex AND parse as a real
       calendar date. Check 180 enforces byte-equality between the two but
       both could silently drift together to a non-ISO format (e.g.
       `2026/06/30` or `2026-13-01`) corrupting recency signals. Sibling of
       Check 208 (JSON-LD date ISO-8601) for the ai:* / SITE_CONFIG date
       surface. (BLOCKING)

  216. JSON-LD `@id` cross-references resolve to defined nodes in the same
       graph (referential integrity): in index.html static JSON-LD blocks,
       any `{"@id": "..."}` reference appearing as the value of common
       reference properties (`author`, `about`, `isPartOf`, `mainEntity`,
       `creator`, `reviewedBy`, `publisher`, `primaryImageOfPage`) must
       point to an `@id` that is defined by some other node in the same
       JSON-LD graph (a node having BOTH `@type` and `@id`). Drift would
       silently fragment the entity graph: AI knowledge-graph consumers
       follow `@id` references and find dead anchors, breaking the linked
       structure of Person/WebSite/WebPage/Organization claims. Check 200
       /201 enforce that primary @ids derive from canonical URL; Check 216
       enforces that every reference actually resolves. (BLOCKING)

  217. JSON-LD `@id` definitions are unique within each `@graph` (BLOCKING):
       in index.html static JSON-LD, no two top-level nodes of the same
       `@graph` array (per `<script type="application/ld+json">` block) may
       claim the same `@id` (with `@type` + `@id`). Drift (e.g. two
       Article nodes both claiming `#article-1`, or accidentally reusing
       `#hero-image` for two assets in the same block) would silently make
       AI / knowledge-graph consumers ambiguous about which node is
       canonical — references via Check 216 would resolve to any one of
       the duplicates non-deterministically. Context-redundant Person
       re-definition across separate JSON-LD blocks (a self-contained
       Article that re-states its creator) is allowed and intentional.
       Sibling of Check 141 (default-project slug/id uniqueness) for the
       JSON-LD entity graph. (BLOCKING)

  218. JSON-LD `datePublished` <= `dateModified` per node (BLOCKING):
       in index.html static JSON-LD, every node containing BOTH
       `datePublished` and `dateModified` must satisfy
       `datePublished <= dateModified` (semantic invariant from Schema.org).
       Drift (e.g. modifying datePublished forward without updating
       dateModified) would silently make AI / SEO crawlers believe the page
       was modified BEFORE it was published — corrupting recency / freshness
       signals and undermining trust. Sibling of Check 208 (ISO-8601 format)
       for the JSON-LD date semantic ordering surface. (BLOCKING)

  219. aio-manifest.json declared paths ⊆ check_aio_digests.py
       MANIFEST_PATH_TO_LOCAL keys: every `path` value in aio-manifest.json
       `source_of_truth` / `supporting_evidence` / `observational_evidence`
       MUST appear as a key in `MANIFEST_PATH_TO_LOCAL` dict of
       `.github/scripts/check_aio_digests.py`. Drift (e.g. aio-guardian adds
       a new evidence entry to the manifest but forgets to register it in
       check_aio_digests.py's local-path map) would silently skip digest
       verification for the new path — the manifest could declare any
       sha256, and the tool would never check the actual file against it.
       This invariant catches silent digest-chain gaps that bypass C6.
       (BLOCKING)

  220. manifest.webmanifest `lang` matches HTML `<html lang>`: the PWA
       manifest's `lang` field MUST equal the index.html `<html lang>`
       attribute (e.g. both `ja`). Drift would silently make the installed
       PWA report a different language than the rendered HTML — screen
       readers, OS-level language selectors, and AI/SEO consumers see
       conflicting language signals. Sibling of Check 152 (<html lang> ↔
       JSON-LD inLanguage) / Check 187 (og:locale ↔ <html lang>) for the
       manifest install layer. (BLOCKING)

  221. JSON-LD `image` / `primaryImageOfPage` references resolve to
       `ImageObject` (type-safety): in index.html static JSON-LD, any
       `{"@id": "..."}` reference appearing as `image` or
       `primaryImageOfPage` MUST point to a node whose `@type` is
       `ImageObject` (allowing for subclasses by string match). Drift
       (e.g. image referring to `#person` or `#website` after rename)
       would silently make AI / SEO consumers retrieve a non-image entity
       when expecting an image asset — breaking image-card rendering,
       OG-style preview fallbacks, and knowledge-graph image extraction.
       Sibling of Check 216 (referential integrity) with type-safety added
       for image-slot references. (BLOCKING)

  222. JSON-LD `author` / `creator` / `reviewedBy` / `copyrightHolder` /
       `employee` refs resolve to Person OR Organization (type-safety):
       in index.html static JSON-LD, any `{"@id": "..."}` reference under
       these "agent-slot" properties MUST point to a node whose `@type` is
       `Person` or `Organization`. Drift (e.g. author referring to
       `#hero-image` or `#website` after rename) would silently make AI /
       SEO consumers attribute authorship to an image or website node,
       breaking the entity-graph "who created this" claim and corrupting
       knowledge-graph attribution. Sibling of Check 221 (image-slot type
       safety); Check 216 with type-safety added for agent-slot
       references. (BLOCKING)

  223. JSON-LD `isPartOf` refs resolve to `WebSite` | `WebPage` |
       `CreativeWork` (type-safety): in index.html static JSON-LD, any
       `{"@id": "..."}` reference under `isPartOf` MUST point to a node
       whose `@type` is `WebSite`, `WebPage`, or `CreativeWork` (the
       Schema.org-permitted containers). Drift (e.g. isPartOf →
       `#hero-image` after rename) would silently make AI / SEO consumers
       claim a WebPage / Article is part of an image, breaking hierarchical
       site structure for knowledge-graph rendering. Sibling of Check 221
       (image-slot) / Check 222 (agent-slot) type-safety for the structural
       isPartOf-slot. (BLOCKING)

  224. `<meta name="description">` content length in SEO-sane band: the
       index.html `<meta name="description">` content character length must
       be within [30, 300] characters. Below 30 = SERP snippet preview
       suppressed by Google (too short to extract); above 300 = silently
       truncated with ellipsis in SERP. Both extremes corrupt the SEO/AI
       crawler card. Check 154 enforces presence + og/twitter coherence;
       Check 224 enforces sanity of length. (BLOCKING)

  225. HTML `<title>` content length in SEO-sane band [10, 70]: the index
       .html `<title>` content character length must fall in [10, 70].
       Below 10 = title too sparse for SERP rendering; above 70 = silent
       truncation with ellipsis on Google SERP. Both extremes corrupt the
       primary entity card in search results. Check 66 enforces presence of
       canonical entity identifier in title; Check 225 enforces length
       sanity. (BLOCKING)

  226. og:title length in [10, 90] AND og:description length in [30, 250]:
       Open Graph card preview tools (Facebook/LinkedIn/Slack/Discord)
       render social cards using these fields. Title <10 = card title
       sparse; >90 = silent truncation by Facebook. Description <30 =
       suppressed preview; >250 = truncated. Both extremes corrupt the
       social-card entity preview. og:title byte-identical to twitter:title
       via Check 155, so this Check transitively covers Twitter as well.
       Length sanity sibling of Check 224 (description) / 225 (title) for
       the Open Graph surface. (BLOCKING)

  227. JSON-LD Person `name` matches canonical entity name: every node in
       index.html static JSON-LD with `"@type": "Person"` MUST have `name`
       equal to one of the canonical entity identifiers from CLAUDE.md §1:
       "Yuta Yokoi", "横井雄太", or "Yokoi Yuta". Drift (e.g. accidentally
       changing one of the 3 Person blocks' name to a typo or generic
       "Anonymous") would silently fragment AI/SEO entity identity across
       JSON-LD blocks. Sibling of Check 195 (Person alternateName) /
       Check 203 (Person givenName/familyName) for the Person `name`
       primary field. (BLOCKING)

  228. sitemap.xml `<changefreq>` values are valid per Sitemap Protocol:
       every `<changefreq>` element in sitemap.xml must contain one of the
       7 spec-allowed values: `always`, `hourly`, `daily`, `weekly`,
       `monthly`, `yearly`, `never`. Drift (e.g. `weakly` typo,
       `biweekly`, or empty) would silently make crawlers ignore the
       crawl-frequency hint — the URL is still discovered but the freshness
       hint that improves recrawl scheduling is lost. (BLOCKING)

  229. sitemap.xml `<priority>` values are float in [0.0, 1.0] (Sitemap
       Protocol): every `<priority>` element in sitemap.xml must parse as
       a float in the closed interval [0.0, 1.0]. Drift (e.g. `1.5` typo
       or `"high"`) is invalid per spec — crawlers silently fall back to
       the default 0.5, ignoring the priority signal entirely. Sibling of
       Check 228 (changefreq spec-valid) for the priority field. (BLOCKING)

  230. sitemap.xml has exactly one `<url>` with `<priority>1.0</priority>`,
       matching canonical URL: the sitemap must reserve `priority=1.0`
       (Sitemap Protocol's maximum) for THE single canonical homepage. Drift
       (multiple priority=1.0 entries, or priority=1.0 on a non-canonical
       URL) silently splits the SEO "this is the primary entry point"
       signal across multiple URLs, diluting the canonical authority for
       AI/search crawlers. Sibling of Check 229 (priority range) /
       Check 150 (og:url ↔ canonical) for the sitemap entry-point axis.
       (BLOCKING)

  231. main.js SITE_CONFIG.ROLE_TITLE matches canonical entity role: the
       `ROLE_TITLE` value in main.js SITE_CONFIG MUST equal one of the 3
       canonical entity roles from CLAUDE.md §1: "AI-Driven PM" /
       "IT Consultant" / "KERNEL Framework Designer". Drift silently
       misrepresents the entity in JS-rendered UI (used in page titles
       and meta descriptions emitted by the SPA renderer). Sibling of
       Check 169 (aio-manifest entity.role canonical markers) for the
       SITE_CONFIG.ROLE_TITLE axis. (BLOCKING)

  232. `<meta name="ai:*">` content URLs all use HTTPS: every
       `<meta name="ai:context|entrypoint|canonical|repository|aio-manifest|
       ...">` content value that is an absolute URL (scheme prefix) MUST
       start with `https://`. Drift to `http://` would silently downgrade
       the AIO routing layer's transport security — AI crawlers following
       these URLs hit Mixed Content blocking on HTTPS-served pages.
       Sibling of Check 207 (HTML src/href HTTPS) for the ai:* meta
       content surface. (BLOCKING)

  233. `<meta name="asset:*">` content URLs all use HTTPS: every
       `<meta name="asset:image:*|asset:audio:*">` content value that is
       an absolute URL (scheme prefix) MUST start with `https://`. Drift
       to `http://` would silently make AI / SEO crawler fetch the
       canonical asset over insecure transport — Mixed Content blocking
       and authenticity-grade degradation. Sibling of Check 232 (ai:*
       content HTTPS) for the asset:* meta surface. (BLOCKING)

  234. `<meta name="asset:*">` content URLs (absolute) share canonical URL
       prefix: every `<meta name="asset:*">` content value that is an
       absolute URL MUST start with the canonical URL prefix. Drift (e.g.
       asset:image:canonical pointing at a CDN or sibling project) would
       silently advertise non-canonical asset URLs to AI/SEO, splitting
       authority and breaking entity-asset linkage. Sibling of Check 171
       (ai:* canonical prefix) for the asset:* meta surface. (BLOCKING)

  235. JSON-LD Article/TechArticle nodes with `@id` (full definitions) have
       Schema.org required fields headline + author + datePublished:
       in index.html static JSON-LD, every Article/TechArticle node that
       has an `@id` (treated as a "full" definition rather than an external
       reference) MUST include `headline`, `author`, and `datePublished`.
       Drift (silent omission) would make Google rich-result eligibility
       fail and degrade AI search Article snippet generation. Article
       references WITHOUT `@id` (external URL pointers in `subjectOf` /
       `citation`) are exempt — they represent "this URL is an Article"
       rather than a self-described Article. (BLOCKING)

  236. aio-manifest.json `generated_at` is strict RFC 3339 datetime AND
       affiliation `start_date` is strict YYYY-MM-DD: the `generated_at`
       top-level field must match `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`
       and `entity.affiliation.start_date` must match `^\d{4}-\d{2}-\d{2}$`
       AND parse as a real calendar date/time. Sibling of Check 93
       (last_metadata_update format) for the generated_at + start_date
       fields. Drift would silently corrupt recency / employment-timeline
       signals consumed by AI/SEO. (BLOCKING)

  237. js/*.js leaf modules have ZERO ESM imports (no inter-leaf coupling):
       every leaf JS module under `js/` MUST have no top-level `import`
       statements. main.js is the SOLE orchestrator that imports leaves.
       This structural invariant prevents:
         - circular leaf↔leaf dependencies (impossible by construction)
         - hidden coupling between leaves (architectural drift)
         - bundling complexity that breaks Vanilla SPA constraint (C1)
       Drift (a leaf importing another leaf) would silently create the
       first cross-leaf edge in the dependency graph, opening the door
       to cycle formation. (BLOCKING)

  238. HTML head singleton tags each appear exactly once: index.html must
       contain exactly 1 of each of `<title>`, `<link rel="canonical">`,
       `<meta name="description">`, `<meta property="og:url">`,
       `<meta property="og:title">`. Multiple instances are SILENT class
       drift — browsers/crawlers pick "first" or "last" non-deterministically
       and the duplicate dilutes the canonical entity signal. Sibling of
       Check 17/180 (date sync) for the head singleton uniqueness axis.
       (BLOCKING)

  239. Shipped JS does NOT contain `eval(` or `new Function(` calls:
       main.js + sw.js + all `js/**/*.js` + root scripts (aio-guard /
       theme-init / karte-init / error-suppressor) MUST NOT contain
       `eval(`, `Function(`, or `new Function(` literal patterns
       (security baseline). Drift would silently introduce a CSP
       `script-src 'unsafe-eval'` requirement at runtime — which the
       current CSP rejects, causing browser console errors and broken
       functionality. Sibling of Check 115 (CSP anti-weakening) for the
       JS source-level enforcement. (BLOCKING)

  240. Shipped JS: setTimeout / setInterval first arg is NEVER a string
       (no eval-equivalent): the first arg to `setTimeout` / `setInterval`
       MUST always be a function (arrow or named), never a string. String
       arg is parsed via `eval`-equivalent semantics — a known security
       anti-pattern that bypasses CSP's static script restrictions.
       Sibling of Check 239 (no eval/Function) for the eval-equivalent
       timer-callback surface. (BLOCKING)

  241. Shipped JS no `document.write` / `document.writeln` calls: these
       legacy APIs are deprecated, break HTML5 parser sniffing, expose
       XSS vectors when fed untrusted strings, and are flagged by browser
       intervention as anti-patterns. Drift would silently introduce one
       of the most security-fragile DOM APIs into the shipped runtime.
       Sibling of Check 239 (no eval/Function) / Check 240 (no
       eval-equivalent timer) for the document-write surface. (BLOCKING)

  242. index.html inline `on*=` event handlers are restricted to the
       documented CSP-allowlisted pattern: every `on*=` attribute outside
       of HTML comments MUST match exactly `onload="this.media='all'"`
       (the documented async font-loading pattern that is whitelisted via
       CSP `'unsafe-hashes'`). Drift introduces an XSS entry vector that
       bypasses CSP `script-src` (inline event handlers execute as
       scripts). Sibling of Check 239/240/241 (eval/Function/timer/
       document.write) for the inline-event-handler surface. (BLOCKING)

  243. main.js SITE_CONFIG.LAST_UPDATED + ai:last-modified are NOT in the
       future: both date fields (synced via Check 17/180) MUST be on or
       before today. Drift to a future date silently corrupts AI/SEO
       recency-weighted retrieval (entity ranked as "from the future")
       and reveals temporal model integrity issues. This site does not
       schedule pre-publish dates; future is always a bug. Sibling of
       Check 36 (sitemap lastmod future WARNING) for the canonical-version
       date surface — BLOCKING here because LAST_UPDATED is the entity's
       primary canonical-version anchor. (BLOCKING)

  244. Every top-level node in JSON-LD `@graph` has `@type`: in index.html
       JSON-LD blocks, every direct top-level element of any `@graph`
       array MUST have a non-empty `@type` field. Drift (anonymous node)
       silently makes AI/SEO consumers ignore the node (no type → cannot
       reason about entity) and breaks Schema.org graph traversal.
       Sibling of Check 217 (top-level @id uniqueness) for the top-level
       @type presence axis. (BLOCKING)

  245. JSON-LD FAQPage `mainEntity[]` Q&A structure validity: every
       FAQPage node's `mainEntity` array MUST contain non-empty Question
       entries, each with `@type == "Question"` + non-empty `name` + an
       `acceptedAnswer` object with `@type == "Answer"` + non-empty
       `text`. Drift would silently break Google FAQ rich-result
       eligibility + AI search FAQ ingestion. Sibling of Check 235
       (Article required fields) for the FAQPage required-structure
       surface. (BLOCKING)

  246. JSON-LD BreadcrumbList `itemListElement` Schema.org structure:
       every BreadcrumbList's `itemListElement` array MUST contain
       ListItem entries, each with `@type == "ListItem"`, an integer
       `position`, a non-empty `name`, and an `item` (URL or @id ref).
       Drift would silently break Google breadcrumb rich-result and AI
       site-structure ingestion. Sibling of Check 245 (FAQPage Q&A) for
       the BreadcrumbList required-structure surface. (BLOCKING)

  247. JSON-LD ImageObject/AudioObject/VideoObject have required fields:
       every node with `@type in {ImageObject, AudioObject, VideoObject}`
       MUST have `name` AND at least one of `contentUrl` / `url`. Drift
       (e.g. silent strip of name) would silently break Google Image/
       Audio rich-result and AI/SEO entity-asset linkage. Sibling of
       Check 245 (FAQPage) / Check 246 (BreadcrumbList) for the
       MediaObject required-structure surface. (BLOCKING)

  248. `<meta charset>` value is `utf-8` (case-insensitive): the index
       .html `<meta charset>` attribute MUST resolve to `utf-8` exactly
       (case-insensitive accepts UTF-8 / utf-8). Drift to e.g.
       `shift_jis` or `iso-8859-1` silently mojibake Japanese content and
       break canonical entity name display. Check 157 enforces presence;
       Check 248 enforces value canonicality. (BLOCKING)

  249. `<meta name="viewport">` content has mobile baseline directives:
       the index.html `<meta name="viewport">` content MUST contain
       `width=device-width` AND `initial-scale=1`. Drift (e.g. fixed
       `width=900`) silently breaks mobile rendering (zoom locked,
       content cropped). Check 157 enforces presence; Check 249 enforces
       canonical mobile-baseline content. (BLOCKING)

  250. `<html lang>` value is valid BCP-47 tag: the index.html `<html
       lang="...">` attribute MUST match BCP-47 regex
       `^[a-zA-Z]{2,3}(?:-[a-zA-Z0-9]{1,8})*$`. Drift (e.g. `jp` non-spec
       2-letter / `JAPANESE` ALL-CAPS word / `ja_JP` underscore) silently
       breaks browser language selection, screen-reader voice, AI/SEO
       language signal. Check 152/187/220 enforce inter-surface equality;
       Check 250 enforces BCP-47 syntactic validity of the canonical
       source value. (BLOCKING)

  251. JSON-LD `potentialAction` block has required `@type` + `target`:
       every `potentialAction` block in index.html static JSON-LD MUST
       have a non-empty `@type` (Schema.org Action subclass — e.g.
       ReadAction / SearchAction) AND a `target` field (URL string or
       array). Drift would silently break AI/voice assistant action
       invocation. Sibling of Check 209 (target canonical prefix) for
       the potentialAction required-fields axis. (BLOCKING)

  252. sw.js registers `install` + `activate` + `fetch` event handlers:
       service-worker code MUST register all 3 event listeners. Drift
       (silent removal of any) breaks SW lifecycle (no install → no
       cache prefill, no activate → no cleanup, no fetch → no offline /
       SWR). Sibling of Check 19 (CACHE_NAME version) for the SW
       lifecycle handler presence axis. (BLOCKING)

  253. main.js registers `navigator.serviceWorker.register('./sw.js'`:
       main.js MUST contain a `navigator.serviceWorker.register('./sw.js'`
       call. Silent removal would mean sw.js exists but never installs
       on visiting browsers — Check 252 confirms the SW has handlers, but
       without registration the SW is dead code. Sibling of Check 252
       (SW handlers) for the SW registration call-site axis. (BLOCKING)

  254. .well-known/index.json skill name uniqueness + digest format:
       every entry in `.well-known/index.json` `skills[]` MUST satisfy:
       (a) non-empty `name` field, all unique within the file;
       (b) `digest` field matches `^sha-256:[0-9a-f]{64}$`. Drift would
       silently break agent-skills discovery (duplicate name causes
       conflict, malformed digest causes mismatch). Sibling of Check 5
       (.well-known/index.json byte-identical mirror) for the schema
       structural validity axis. (BLOCKING)

  255. index.html starts with `<!DOCTYPE html>` (HTML5 declaration):
       the index.html file MUST start with `<!DOCTYPE html>` (case-
       insensitive, ignoring leading BOM/whitespace). Drift silently
       triggers browser quirks mode — CSS box model regression, line-
       height drift, layout breakage. Sibling of Check 157 (head meta
       baseline) for the document-mode declaration axis. (BLOCKING)

  256. Primary JSON-LD WebPage has `dateModified` + `inLanguage` +
       `isPartOf`: in index.html static JSON-LD, the primary WebPage node
       (`@id == canonical + "#webpage"`) MUST have `dateModified` (string),
       `inLanguage` (string), AND `isPartOf` (object/string). Drift would
       silently remove recency / language / hierarchy signals from the
       primary page entity. Sibling of Check 235 (Article required fields)
       for the primary WebPage required-fields axis. (BLOCKING)

  257. primary JSON-LD Person has jobTitle + image + sameAs + worksFor +
       description: in index.html static JSON-LD, the primary Person node
       (`@id == canonical + "#person"`) MUST have all 5 fields: jobTitle
       (str), image (dict/string), sameAs (list), worksFor (dict/string),
       description (str). Drift would silently strip entity-rich-profile
       data from AI/SEO consumers (knowledge-graph card would shrink).
       Sibling of Check 256 (primary WebPage) for the primary Person
       required-fields axis. (BLOCKING)

  258. primary JSON-LD WebSite has inLanguage + potentialAction: in
       index.html static JSON-LD, the primary WebSite node (`@id ==
       canonical + "#website"`) MUST have `inLanguage` (str) AND
       `potentialAction` (dict/list). Drift would silently remove the
       site-level language signal and the AI/voice action descriptor
       from the WebSite root entity. Sibling of Check 256 (primary
       WebPage) / Check 257 (primary Person) for the primary WebSite
       required-fields axis. (BLOCKING)

  259. primary JSON-LD Organization (nkgr.co.jp) has name + url +
       alternateName + description + employee: the canonical Organization
       node (`@id == "https://nkgr.co.jp/#organization"`) MUST have all
       5 fields. Drift would silently strip employer-rich data from
       AI/SEO consumers (worksFor target loses richness, knowledge-graph
       Organization card shrinks). Sibling of Check 257 (primary Person)
       for the primary Organization required-fields axis. (BLOCKING)

  260. primary hero ImageObject has caption + width + height +
       encodingFormat: in index.html static JSON-LD, the primary hero
       ImageObject node (`@id == canonical + "#hero-image"`) MUST have
       caption (non-empty str), width + height (numeric-parsable string
       or int), encodingFormat (non-empty str). Drift would silently
       degrade Google Image rich-result eligibility (width/height
       required for CWV LCP-image preload coordination, caption required
       for accessibility / Google Lens). Sibling of Check 247
       (MediaObject required) for the hero-image required-fields axis.
       (BLOCKING)

  261. primary BGM AudioObject has encodingFormat + creator: in index.html
       static JSON-LD, the primary BGM AudioObject node (`@id == canonical
       + "#portfolio-bgm"`) MUST have `encodingFormat` (non-empty str)
       AND `creator` (dict or string @id reference). Drift would silently
       degrade AI search audio classification (no encodingFormat → mime
       type unknown) and remove attribution (no creator → audio uploaded
       by "Anonymous"). Sibling of Check 260 (hero image) for the
       primary audio required-fields axis. (BLOCKING)

  262. Shipped JS no `console.log(` calls (allow console.error / warn /
       debug / info): main.js + sw.js + js/**/*.js + root scripts MUST
       NOT contain `console.log(` literal calls. `console.log` is the
       debug-statement leak pattern in production code; the project
       allows `console.error` / `warn` (legitimate observability) but
       restricts the verbose-debug form. Sibling of Check 239/240/241
       (eval/timer-string/document.write) for the production-cleanliness
       axis. (BLOCKING)

  263. Shipped JS no `debugger;` + no `alert(`: main.js + sw.js +
       js/**/*.js + root scripts MUST NOT contain `debugger;` statement
       or `alert(` call. Both are dev-debug-only patterns:
       - `debugger;` pauses execution when DevTools open (production UX-break
         for users running with DevTools)
       - `alert(` is modal-blocking (legitimate `confirm()` for delete UX is
         allowed, `alert` rarely fits production UX)
       Sibling of Check 262 (no console.log) for the production-cleanliness
       axis. (BLOCKING)

  264. Shipped JS comments contain no TODO/FIXME/HACK/XXX markers:
       main.js + sw.js + js/**/*.js + root scripts must NOT have any
       comment containing the dev-cruft markers `TODO`, `FIXME`, `HACK`,
       `XXX` (word-boundary, case-sensitive). Drift = leftover dev-time
       notes leak into production codebase — incomplete work shipped
       without follow-up. String literals containing the word "TODO"
       (e.g. user-facing "クイック TODO" feature name) are exempt;
       only comment markers are guarded. Sibling of Check 262/263
       (production-cleanliness) for the comment-cruft axis. (BLOCKING)

  265. Shipped JS uses strict equality (no `==` / `!=`): main.js + sw.js
       + js/**/*.js + root scripts MUST NOT contain loose equality
       (`==` / `!=`) — only strict (`===` / `!==`). String literals and
       comments are exempt. Drift can introduce subtle bugs (e.g.
       `'0' == 0 === true`). Sibling of Check 262/263/264
       (production-cleanliness) for the equality-strictness axis.
       (BLOCKING)

  266. JSON-LD entity description length in [20, 1000]: every Person /
       Organization / ImageObject / CreativeWork node with a `description`
       field must have its description in [20, 1000] character length.
       Below 20: too brief to be useful for AI/SEO. Above 1000: usually
       indicates copy-paste of full body text into description (Google
       Schema.org spec recommends concise summary). Sibling of Check 224
       (meta description length) for the JSON-LD entity description axis.
       (BLOCKING)

  267. JSON-LD entity name length in [3, 200]: every Person / Organization
       / ImageObject / WebSite / WebPage / TechArticle / CreativeWork /
       AudioObject node with `@id` AND `name` field must have name length
       in [3, 200] character. Drift: <3 = stub/empty (entity disambiguation
       impossible); >200 = copy-paste over-long (often body text leaked).
       Sibling of Check 266 (entity description length) for the JSON-LD
       entity name axis. (BLOCKING)

  268. JSON-LD Article / TechArticle headline length in [10, 110]:
       every Article/TechArticle node with `headline` field MUST have
       length in [10, 110] character. Schema.org / Google Article
       rich-result spec recommends headline <= 110 char (else card
       truncates). <10 = sparse / no value for SERP card. Sibling of
       Check 235 (Article required fields) for the headline length axis.
       (BLOCKING)

  269. canonical binary asset size budget: hero.webp <= 200_000 bytes
       AND BGM.mp3 <= 1_000_000 bytes. Drift (image / audio re-encoded to
       a larger size accidentally) would silently degrade LCP / CWV /
       mobile bandwidth budget. Sibling of Check 120 (shipped JS byte
       weight budget) for the binary asset axis. (BLOCKING)

  270. canonical text asset size budget: style.css <= 100_000 bytes AND
       index.html <= 200_000 bytes. Drift = silent file bloat from
       accidental copy-paste / dead-code accretion. Sibling of Check 120
       (JS) / 269 (binary) for the text asset size axis. (BLOCKING)

  271. root JS byte budget: main.js <= 100_000 bytes AND sw.js <= 20_000
       bytes AND {aio-guard/theme-init/karte-init/error-suppressor}.js
       each <= 10_000 bytes. Drift = silent script bloat pushing
       parse/execute time beyond mobile-CPU budget. Sibling of Check 120
       (JS byte weight sum) for the per-file JS byte budget axis.
       (BLOCKING)

  272. js leaf module byte budget: every `js/**/*.js` file MUST be <=
       100_000 bytes. Drift = a leaf module bloating past canonical
       size, defeating the Stage 5 factory extraction goal (physically
       split main.js into small orchestrable leaves). Sibling of Check
       271 (root JS) for the leaf JS byte budget axis. (BLOCKING)

  273. JSON-LD `datePublished` / `dateModified` / `dateCreated` NOT in
       future: every date value in index.html static JSON-LD MUST be on
       or before today. Drift silently corrupts AI/SEO recency-weighted
       retrieval (this site does not schedule pre-publish). Sibling of
       Check 243 (SITE_CONFIG/ai:last-modified not future) / Check 218
       (datePublished <= dateModified) for the JSON-LD date not-future
       axis. (BLOCKING)

  274. aio-manifest `entity.name` matches primary Person `name` (JSON-LD):
       the `.well-known/aio-manifest.json` `entity.name` value MUST equal
       the primary JSON-LD Person `name` (where `@id == canonical +
       "#person"`) — currently both `"Yuta Yokoi"`. Drift silently splits
       the entity identity between the AIO manifest layer and the
       JSON-LD layer. Sibling of Check 172 (entity name variants combined)
       for the manifest ↔ JSON-LD name direct-equality axis. (BLOCKING)

  275. aio-manifest affiliation.organization_name == JSON-LD Organization
       `name` (nkgr.co.jp/#organization): the `.well-known/aio-manifest.json`
       `entity.affiliation.organization_name` value MUST equal the JSON-LD
       primary Organization node `name` where `@id ==
       "https://nkgr.co.jp/#organization"` (currently both "株式会社日本経営").
       Sibling of Check 274 (Person name equality) for the manifest ↔
       JSON-LD Organization name direct-equality axis. (BLOCKING)

  276. aio-manifest affiliation.organization_url == JSON-LD Organization
       `url`: the `.well-known/aio-manifest.json`
       `entity.affiliation.organization_url` value MUST equal the JSON-LD
       primary Organization node `url` (`@id ==
       https://nkgr.co.jp/#organization`, currently both
       "https://nkgr.co.jp/"). Sibling of Check 275 (Organization name)
       for the manifest ↔ JSON-LD Organization url direct-equality axis.
       (BLOCKING)

  277. aio-manifest entity.authoritative_context == canonical + llms-full.txt:
       the `.well-known/aio-manifest.json` `entity.authoritative_context`
       value MUST equal `<canonical>llms-full.txt` (canonical URL prefix +
       "llms-full.txt" — currently
       "https://yutapr0117-design.github.io/portfolio/llms-full.txt").
       Drift silently misroute AI/agent authoritative-context ingestion.
       Sibling of Check 274/275/276 for the manifest authoritative-context
       URL derivation axis. (BLOCKING)

  278. sitemap.xml all `<loc>` URLs use HTTPS: every `<loc>` value in
       sitemap.xml MUST start with `https://`. Drift to `http://` would
       silently expose crawler paths on insecure transport (Mixed Content
       intervention on HTTPS-hosted crawler contexts). Sibling of Check
       206/207/214 for the sitemap loc HTTPS-only axis. (BLOCKING)

  279. robots.txt `Sitemap:` directive URL uses HTTPS: every `Sitemap:`
       line in robots.txt MUST advertise an `https://` URL. Drift to
       `http://` would silently make crawlers fetch the sitemap over
       insecure transport. Sibling of Check 278 (sitemap.xml loc HTTPS)
       for the robots.txt sitemap-directive HTTPS axis. (BLOCKING)

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

# 純 I/O helper は sibling module `_lib_io.py` に抽出 (check-repository-consistency-
# map.md §4 で予告された helper-first 抽出の第一歩)。sibling import は Python が
# 実行スクリプトのディレクトリを自動 sys.path に含めるため、特別な path 操作不要。
# 既存呼出インターフェース (`read(path)` / `read_bytes(path)` / `extract(pat, text)`)
# は保持し、ROOT を bind した薄い wrapper で公開する。
from _lib_io import csp_sri_hash as _lib_csp_sri_hash
from _lib_io import extract
from _lib_io import read as _lib_read
from _lib_io import read_bytes as _lib_read_bytes

# Python version guard: these verification scripts use 3.10+ syntax (PEP 604
# `str | None` union annotations, e.g. `root_lastmod: str | None` below). On
# Python 3.9 (the macOS system interpreter at /usr/bin/python3) a module-level
# union annotation raises an opaque `TypeError: unsupported operand type(s) for |`
# at import time, which is hard to diagnose. Fail fast with an actionable message
# instead. The repo targets Python 3.12 (CI setup-python pin). Held in place by
# Check 104 so it cannot be silently removed.
if sys.version_info < (3, 10):
    sys.exit(
        "ERROR: this repository's verification scripts require Python 3.10+ "
        f"(found {sys.version.split()[0]}). Use python3.12 — see CLAUDE.md / .zprofile."
    )

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []
warnings: list[str] = []

# All source files that contribute numbered Check sections. The self-integrity Checks
# (45 docstring↔section bijection / 70 runbook count / 105 map bijection) aggregate the
# section headers AND the docstring inventory across ALL of these files, so the 4800-line
# monolith can be split into domain modules (each carrying its own checks + their docstring
# N. lines) without breaking self-integrity. Today: just this file. Extracting a module =
# append it here + move its sections + their docstring lines into it.
CHECK_SOURCE_FILES: list = [
    ROOT / ".github" / "scripts" / "check_repository_consistency.py",
]


def _aggregate_check_numbers():
    """(inventory_nums, section_nums) sorted, aggregated across CHECK_SOURCE_FILES.

    inventory_nums = `  N. ` lines in each file's module docstring (first triple-quoted block).
    section_nums   = the `# <box-drawing> N.` section-header numbers in each file's body.
    Self-integrity Checks 45/70/105 use this so the bijection spans every split check module.
    """
    _sec_re = re.compile(r'^#\s*──\s*(\d+)\.', re.MULTILINE)
    _inv_re = re.compile(r'^\s{2}(\d+)\.\s', re.MULTILINE)
    _doc_re = re.compile(r'"""(.*?)"""', re.DOTALL)
    inv: list = []
    sec: list = []
    for _src in CHECK_SOURCE_FILES:
        if not _src.exists():
            continue
        _txt = _src.read_text(encoding="utf-8")
        _dm = _doc_re.search(_txt)
        _doc = _dm.group(1) if _dm else ""
        _body = _txt[_dm.end():] if _dm else _txt
        inv.extend(int(n) for n in _inv_re.findall(_doc))
        sec.extend(int(n) for n in _sec_re.findall(_body))
    return sorted(inv), sorted(sec)


def check(condition: bool, msg_ok: str, msg_fail: str, blocking: bool = True) -> None:
    if condition:
        print(f"OK: {msg_ok}")
    else:
        tag = "ERROR" if blocking else "WARNING"
        print(f"{tag}: {msg_fail}")
        (errors if blocking else warnings).append(msg_fail)


def read(path: str) -> str:
    """ROOT 基準で text ファイルを読む (互換 wrapper)."""
    return _lib_read(path, root=ROOT)


def read_bytes(path: str) -> bytes:
    """ROOT 基準で binary ファイルを読む (互換 wrapper)."""
    return _lib_read_bytes(path, root=ROOT)


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
    """互換 alias — 実装は `_lib_io.csp_sri_hash` に統合 (Plan C helper 抽出)."""
    return _lib_csp_sri_hash(content)

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

    # 文字列リテラル / コメントを除去してから brace を数える stripper。素朴な count("{") は
    # 文字列・コメント内の brace も数えてしまい false-positive を生む（例: テストデータの
    # 破損 JSON 文字列 'NOT{VALID' の孤立 `{`）。これを構造ブレースのみ数えるよう堅牢化する。
    # 順序が重要: まず文字列を除去 (内部の // や /* を巻き込む) → 次に // と /* */ コメント除去。
    _str_re28 = _re_spec28.compile(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`")
    _blockc_re28 = _re_spec28.compile(r"/\*.*?\*/")

    def _strip_js_literals_28(line: str) -> str:
        line = _str_re28.sub("", line)        # 文字列リテラル除去 (escape 対応)
        line = _blockc_re28.sub("", line)     # 単一行 /* ... */ 除去
        line = _re_spec28.sub(r"//.*$", "", line)  # 行コメント除去
        return line

    for _ln28, _line28 in enumerate(_spec_lines_28, 1):
        _code28 = _strip_js_literals_28(_line28)
        # A top-level test() definition starts at column 0 (元行で判定: 列 0 固定ゆえ strip 不要)
        if _re_spec28.match(r"^test\s*\(", _line28):
            if _test_start_depth_28 is not None:
                _nesting_errors_28.append(
                    f"line {_ln28}: test() opened while previous test() "
                    f"(started at brace-depth {_test_start_depth_28}) is not yet closed"
                )
            _test_start_depth_28 = _brace_depth_28  # record depth *before* this line

        # 構造ブレースのみ数える (文字列/コメント内の brace は strip 済みゆえ無視される)
        _brace_depth_28 += _code28.count("{") - _code28.count("}")

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
        # _sm_checked > 0 ガード: project <loc> がゼロ件 (sitemap が gutted/空) のとき
        # `not _sm_missing` だけだと「all 0 URLs resolve」で vacuous pass し、AIO/SEO の
        # 根幹である sitemap の中身消失を見逃す。最低 1 件 (SPA root) は常に広告されるべき。
        _sm_checked > 0 and not _sm_missing,
        f"Check 39: all {_sm_checked} project sitemap <loc> URLs resolve to committed files",
        "Check 39: " + (
            "sitemap.xml advertises zero project <loc> URLs — gutted/empty sitemap is an AIO/SEO defect "
            "(at least the SPA root must be listed)" if _sm_checked == 0 else
            "sitemap.xml advertises URL(s) with no backing file (crawler 404 risk) — "
            "add the file or remove the <loc>: " + "; ".join(sorted(_sm_missing)[:10])
            + (" …" if len(_sm_missing) > 10 else "")
        ),
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
    # Exception: docs/files/**/<orig-name>.md (1-to-1 mirror docs from Phase 6) are doc-of-doc,
    # not actual incident records — they live next to the original file's path under docs/files/
    # by design (Check 96 bijection 強制構造). Excluding docs/files/** so the placement
    # governance only judges real decision/improvement-notes content.
    _misplaced = []
    for _pat in ("decision-*.md", "improvement-notes-*.md"):
        for _f in ROOT.rglob(_pat):
            # ignore anything under node_modules / .git, the legitimate incident dir, and
            # the 1-to-1 mirror docs under docs/files/
            _parts = _f.relative_to(ROOT).parts
            if "node_modules" in _parts or ".git" in _parts:
                continue
            if len(_parts) >= 2 and _parts[0] == "docs" and _parts[1] == "files":
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
# We read the check source files from disk (not via introspection) so the check sees exactly
# the committed bytes a reviewer would read. CHECK_SOURCE_FILES lets the inventory/section
# bijection span multiple modules once check.py is split into cohesive files.
_inv45, _sec45 = _aggregate_check_numbers()
if _inv45 or _sec45:
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
#   50d — eslint.config.mjs carries the `no-dupe-keys` bug-catching rule (added after a real
#         duplicate-`class` bug in js/quiz-renderer.js silently dropped styling); guarding the
#         rule's presence keeps that protection from being silently removed.
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
if _flat_cfg50.is_file():
    _cfg_src50d = _flat_cfg50.read_text(encoding="utf-8")
    check(
        re.search(r"['\"]no-dupe-keys['\"]\s*:", _cfg_src50d) is not None,
        "Check 50d: eslint.config.mjs carries the `no-dupe-keys` bug-catching rule",
        "Check 50d: eslint.config.mjs no longer declares `no-dupe-keys` — this rule was added "
        "after a real duplicate-`class` bug in js/quiz-renderer.js silently dropped element "
        "styling. Removing it re-opens that whole class of accident (duplicate keys in h() "
        "props passing CI unnoticed). Restore `'no-dupe-keys': 'error'` in the rules block.",
    )
else:
    check(
        False,
        "Check 50d: eslint.config.mjs present for no-dupe-keys rule verification",
        "Check 50d: eslint.config.mjs not found — cannot verify the no-dupe-keys rule is declared.",
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
        # _modules57 非空ガード: 両集合が空 (main.js が import を失い、index.html も preload ゼロ)
        # のとき対称差 0 で vacuous pass するのを防ぐ。葉モジュール集合は常に非空であるべき。
        bool(_modules57) and not _only_preload57 and not _only_modules57,
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
        # 両集合非空ガード: e2e ALL_ROUTES と main.js switch case のどちらかが空 (正規表現が
        # 何も拾えない＝構造変更や gutting) のとき対称差 0 で vacuous pass し、ルート網羅検証が
        # 無効化されるのを防ぐ。出荷ルートは常に複数存在するため両集合は非空であるべき。
        bool(_e2e_set58) and bool(_main_set58) and not _only_e2e58 and not _only_main58,
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
            # _data59 非空ガード: BUDGET-DATA ブロックが空 (エントリ全削除) のとき
            # `not _only_data59` だけだと vacuous pass し、予算定義の消失を見逃す。
            bool(_data59) and not _only_data59,
            f"Check 59: file-size-budget §2 表 contains all {len(_data59)} BUDGET-DATA entries",
            "Check 59: " + (
                "BUDGET-DATA block has zero entries — file-size 予算定義が消失している"
                if not _data59 else
                f"BUDGET-DATA entries missing from §2 表: {_only_data59} — "
                f"§4 (機械可読) と §2 (人間可読) が drift している。§2 表に該当行を追加して同期せよ"
            ),
        )
    else:
        warnings.append("Check 59: BUDGET-DATA block not found — §2/§4 set check skipped")
else:
    warnings.append("Check 59: file-size-budget.md not found — §2/§4 set check skipped")

# ── 60. ESLint warning baseline regression guard (ADVISORY) ───────────────────
# file-size-budget.md の <!-- ESLINT-BASELINE-DATA --> ブロックに warning 数 baseline が記録
# されていることを ADVISORY で確認する。baseline ファイルが見つからない場合や正規表現で値を
# 取れない場合は ADVISORY skip（環境制約のため exit に影響しない）。本 Check は CI 内で直接
# `npm run lint` を実行せず、代わりに baseline 値が記録されていることだけを確認する（実測値
# の取得と比較は CI 全体の ESLint scan ステップが担う）。これは「baseline 値が消えた／コメント
# アウトされた」ことを ADVISORY で検出する役割で、warning 件数の実測比較は CI workflow 側で
# 行う設計（Check 単体での実装複雑度を抑え、責務を分離する）。
# 実効強制（regression の実 gate）: architecture-validation.yml の ESLint scan step が本 marker
# を single source として読み、`WARN_COUNT > baseline → BLOCKING fail` で warning 増加（新規
# lint 負債）を CI で落とす。本 Check は「marker が存在し CI が比較できる状態」を保証する presence
# 層、CI step がその marker を使った count 比較層、という二層で「regression guard」を honest に
# 成立させる（以前は CI step が WARN_COUNT を表示するだけで比較せず guard が vacuous だった）。
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

# ── 64. check-repository-consistency-map.md Check-number uniqueness (BLOCKING) ─
# docs/architecture/check-repository-consistency-map.md は本ファイル check_repository_
# consistency.py の Check 一覧を機能カテゴリ別 (A〜F) の表形式で列挙したガバナンス文書。
# 各カテゴリ表は `| N | 検査内容 | BLOCKING |` 形式 (N = Check 番号) で並ぶ。番号がカテ
# ゴリをまたいで重複すると、人間レビュアーが「Check N は何の検査か」を一意に解決できなく
# なり、新規 Check の挿入位置を誤って番号衝突を引き起こす (Stage 5-l / 5-k' の naming 衝突
# と同種の class)。本 Check は全カテゴリ表の Check 番号を抽出し、重複が 0 件であることを
# 機械強制する。番号順序自体はカテゴリ境界でリセットするため強制しない (各カテゴリ内では
# ascending だが、カテゴリ間では非単調) — 番号一意性のみが本質的に守るべき invariant。
_map64 = ROOT / "docs" / "architecture" / "check-repository-consistency-map.md"
if _map64.exists():
    _msrc64 = _map64.read_text(encoding="utf-8")
    # 行頭が `| <数字><suffix?> |` 形式の行を抽出 (category 表のみ; §3 級別表は行頭 `| BLOCKING` で除外)
    # alpha suffix を含めた identifier として保存 (Check 7 / 7b / 7c は別 identifier として一意性検査)
    _ids64 = re.findall(r"^\|\s*(\d+[a-z]?)\s*\|", _msrc64, re.MULTILINE)
    _seen64: dict[str, int] = {}
    for _id in _ids64:
        _seen64[_id] = _seen64.get(_id, 0) + 1
    _dups64 = sorted([i for i, c in _seen64.items() if c > 1])
    check(
        not _dups64 and len(_ids64) > 0,
        f"Check 64: check-repository-consistency-map.md Check 番号 (alpha suffix 含む) は全カテゴリで一意 "
        f"({len(_ids64)} 行, distinct={len(_seen64)})",
        f"Check 64: check-repository-consistency-map.md に重複した Check 番号: {_dups64} — "
        f"新規 Check の挿入位置を誤って番号衝突 (Stage 5-l / 5-k' クラス)。重複番号を解消せよ",
    )
else:
    warnings.append("Check 64: check-repository-consistency-map.md not found — uniqueness check skipped")

# ── 65. doc Last-Updated ISO-8601 format (BLOCKING) ───────────────────────────
# docs/architecture/ 配下の全 .md (`Last-Updated:`) と docs/files/ 配下の全 mirror
# (`last-updated:` YAML frontmatter) について、日付フィールドが存在する場合は ISO-8601 の
# `YYYY-MM-DD` 形式に厳密に従うことを機械強制する。Last-Updated は「文書がいつ真値だったか」を
# 読み手 (AI/human) に伝える正本シグナルであり、フォーマット揺れ (e.g. `06-13-2026` /
# `2026.6.13`) は honest-dating 原則（Check 34/AI2AI.md カノン）を内部から侵食する。Check 34 が
# sitemap lastmod との一致を ADVISORY で見るのに対し、本 Check は「日付フォーマットそのもの」を
# BLOCKING で固定する責務分離。docs/files mirror (143 件) は Check 97 が presence を見るが
# フォーマットは未検証だったため、honest-dating の scope をミラー全面へ拡張する。
_isodate65 = re.compile(r"^\s*Last-Updated\s*:\s*(.+?)\s*$", re.MULTILINE)
_isodate65_lc = re.compile(r"^\s*last-updated\s*:\s*(.+?)\s*$", re.MULTILINE)
_isoformat65 = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_bad_dates65 = []
for _md65 in sorted((ROOT / "docs" / "architecture").glob("*.md")):
    _src65 = _md65.read_text(encoding="utf-8")
    _m65 = _isodate65.search(_src65)
    if _m65 and not _isoformat65.match(_m65.group(1).strip()):
        _bad_dates65.append(f"{_md65.relative_to(ROOT)}: {_m65.group(1).strip()!r}")
_docsfiles65 = ROOT / "docs" / "files"
if _docsfiles65.is_dir():
    for _mir65 in sorted(_docsfiles65.rglob("*.md")):
        if _mir65.name in ("README.md", "_template.md"):
            continue
        _fm65 = re.match(r"^---\s*\n([\s\S]*?)\n---", _mir65.read_text(encoding="utf-8"))
        if not _fm65:
            continue
        _lm65 = _isodate65_lc.search(_fm65.group(1))
        if _lm65 and not _isoformat65.match(_lm65.group(1).strip()):
            _bad_dates65.append(f"{_mir65.relative_to(ROOT)}: {_lm65.group(1).strip()!r}")
check(
    not _bad_dates65,
    "Check 65: all docs/architecture/*.md Last-Updated + docs/files/*.md last-updated values are ISO-8601 (YYYY-MM-DD)",
    f"Check 65: non-ISO-8601 date values: {_bad_dates65} — "
    f"全 doc の Last-Updated / last-updated は `YYYY-MM-DD` 形式に統一せよ (honest-dating 原則)",
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
if _runbook70.exists() and CHECK_SOURCE_FILES:
    _, _section_nums70 = _aggregate_check_numbers()
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

# ── 72. ESLint baseline absolute-ceiling contract (BLOCKING) ─────────────────
# file-size-budget.md の `<!-- ESLINT-BASELINE-DATA <N> -->` ブロックが記録する
# warning 数 baseline N が、絶対的な上限契約として固定されていることを機械強制する。
# 「現在のリポジトリ状態を確定上限 N とし、以降この値を上回ることを CI で防ぐ」と
# いう絶対防衛線。Check 60 (ADVISORY 監視) を BLOCKING 化した姉妹 Check で、
# baseline 値が極端に大きい (e.g. 数千) という drift も同時に検出する (sanity ceiling
# = 200 を超えると BLOCKING で警告し、明示的な doc 更新を強要する)。これで Plan A
# の「絶対防衛線」を sw.js / main.js の AIDK Kernel 保護領域に手を入れることなく
# 達成する。
_baseline72 = re.search(r"<!--\s*ESLINT-BASELINE-DATA\s+(\d+)\s+-->", _bsrc59 if _budget59.exists() else "")
_BASELINE_SANITY_CEILING_72 = 200
if _baseline72:
    _n72 = int(_baseline72.group(1))
    check(
        _n72 <= _BASELINE_SANITY_CEILING_72,
        f"Check 72: ESLint baseline {_n72} ≤ sanity ceiling {_BASELINE_SANITY_CEILING_72} (絶対防衛線)",
        f"Check 72: ESLint baseline {_n72} exceeds sanity ceiling {_BASELINE_SANITY_CEILING_72} — "
        f"baseline 値が制御不能な水準。保護領域外の lint 負債が静かに増えた可能性。"
        f"file-size-budget.md の ESLINT-BASELINE-DATA を見直し、増分の根拠を doc に明文化せよ",
    )
else:
    check(
        False,
        "Check 72: ESLint baseline marker present",
        "Check 72: file-size-budget.md に `<!-- ESLINT-BASELINE-DATA <N> -->` が無い — "
        "Plan A 絶対防衛線が消失している。baseline marker を追加せよ",
    )

# ── 73. index.html accessibility/CWV HTML-attribute contract (BLOCKING) ──────
# index.html の機械強制 HTML accessibility / Core Web Vitals 契約。Plan B の HTML
# 属性のみで完結する範囲を BLOCKING 化することで、style.css に触れずに WCAG 2.2 /
# CWV シグナルを構造的に固定する。Playwright visual baseline 不変が前提のため、
# pixel diff を発生させない HTML 属性のみを対象とする (現状の good practice を
# 契約化して drift 防止):
#   (73a) 全 <link rel="preload"> に `as=` 属性必須 (preload 仕様で as 無指定は無効)
#   (73b) 全 <img> 要素に `alt=` 属性必須 (WCAG 1.1.1 Level A)
#   (73c) hero 画像 (yuta-yokoi-ai-pm-orchestration-system.webp) に
#         `fetchpriority="high"` を指定 (LCP 改善契約の固定)
_html73 = read("index.html")
# HTML コメント (<!-- ... -->) を pre-strip。コメント内に literal `<img>` や preload tag を
# 記述している可能性があり、それらは実際の DOM 要素ではない (browser は描画しない) ため
# accessibility / CWV 契約の対象外。Check 7b/7c が同じ pattern で comment-strip 済み。
_html_no_comments73 = re.sub(r"<!--.*?-->", "", _html73, flags=re.DOTALL)

_preload73 = re.findall(r"<link[^>]*\brel=\"preload\"[^>]*>", _html_no_comments73)
_preload_no_as73 = [p for p in _preload73 if not re.search(r"\bas=", p)]
check(
    not _preload_no_as73,
    f"Check 73a: all {len(_preload73)} <link rel=\"preload\"> tags have an `as=` attribute (WCAG/CWV)",
    f"Check 73a: <link rel=\"preload\"> without `as=` attribute: {_preload_no_as73} — "
    f"preload は as 無指定だと無効 (Chrome は warning を出す)。as=script/style/image/font 等を指定せよ",
)

_img73 = re.findall(r"<img\b[^>]*>", _html_no_comments73)
_img_no_alt73 = [t for t in _img73 if not re.search(r"\balt=", t)]
check(
    not _img_no_alt73,
    f"Check 73b: all {len(_img73)} <img> tags have an `alt=` attribute (WCAG 1.1.1 Level A)",
    f"Check 73b: <img> without `alt=` attribute: {_img_no_alt73} — "
    f"WCAG 1.1.1 Level A 違反。装飾画像は alt=\"\" でも明示せよ",
)

_HERO_IMG_73 = "yuta-yokoi-ai-pm-orchestration-system.webp"
_hero_pattern73 = re.compile(
    rf"<link[^>]*href=\"[./]*{re.escape(_HERO_IMG_73)}\"[^>]*>",
    re.IGNORECASE,
)
_hero_tags73 = _hero_pattern73.findall(_html_no_comments73)
_hero_has_fp73 = any("fetchpriority=\"high\"" in t for t in _hero_tags73)
check(
    _hero_has_fp73 and len(_hero_tags73) > 0,
    f"Check 73c: hero image ({_HERO_IMG_73}) preload has fetchpriority=\"high\" (LCP 契約)",
    f"Check 73c: hero image preload missing fetchpriority=\"high\" — "
    f"Core Web Vitals LCP 改善契約。<link rel=\"preload\" href=\"./{_HERO_IMG_73}\" "
    f"as=\"image\" fetchpriority=\"high\"> を維持せよ",
)

# ── 74. .github/scripts/_lib_io.py helper module integrity (BLOCKING) ────────
# Plan C で抽出した純 helper module `_lib_io.py` が check_repository_consistency.py
# から import 解決され、`read` / `read_bytes` / `extract` / `csp_sri_hash` の 4 public
# 関数を export することを機械強制する。sibling import の path 解決が一度でも壊れる
# (e.g. file rename / Python のディレクトリ走査仕様変更) と、check_repository_
# consistency.py 全体が ImportError で実行不能になり CI が catastrophic に落ちる。
# 本 Check は import に成功した時点で実行されるため、import 失敗時はそれ自体が
# 上位 BLOCKING (script 起動失敗) として fail-fast する設計。本 Check の役割は
# 「helper module の API 契約 (4 関数の存在) を構造的に固定」する。
_lib74 = ROOT / ".github" / "scripts" / "_lib_io.py"
if _lib74.exists():
    _lib_src74 = _lib74.read_text(encoding="utf-8")
    _required74 = ["read", "read_bytes", "extract", "csp_sri_hash"]
    _missing_api74 = [
        fn for fn in _required74
        if not re.search(rf"^def {fn}\b", _lib_src74, re.MULTILINE)
    ]
    check(
        not _missing_api74,
        f"Check 74: _lib_io.py exports all {len(_required74)} required helpers ({_required74})",
        f"Check 74: _lib_io.py missing required helpers: {_missing_api74} — "
        f"Plan C 抽出 helper module の API 契約違反。4 関数の def を保持せよ",
    )
else:
    check(
        False,
        "Check 74: _lib_io.py exists",
        "Check 74: .github/scripts/_lib_io.py が存在しない — Plan C 抽出 helper module が消失",
    )

# ── 75. docs/incident-artifacts/ README inventory completeness (BLOCKING) ────
# docs/incident-artifacts/ 配下の全 *.md / *.yml ファイルが README.md に列挙されている
# ことを機械強制する。Plan D の「物理移動なし、README で年次/種別 grouping を提供」
# 設計を機械強制化したもので、incident-artifact 追加時に README 更新を忘れる drift
# を pre-commit で構造的に閉じる。README 自身は inventory から除外。
_artifacts75 = ROOT / "docs" / "incident-artifacts"
_readme75 = _artifacts75 / "README.md"
if _readme75.exists() and _artifacts75.is_dir():
    _readme_src75 = _readme75.read_text(encoding="utf-8")
    _entries75 = [
        p.name for p in _artifacts75.iterdir()
        if p.is_file() and p.name != "README.md" and not p.name.startswith(".")
    ]
    _missing75 = [n for n in _entries75 if n not in _readme_src75]
    check(
        not _missing75 and len(_entries75) > 0,
        f"Check 75: docs/incident-artifacts/README.md lists all {len(_entries75)} artifact files",
        f"Check 75: README.md not listing {len(_missing75)} artifact(s): {_missing75[:5]}{'...' if len(_missing75) > 5 else ''} — "
        f"新規 artifact 追加時は README.md にも列挙せよ (Plan D inventory governance)",
    )
else:
    check(
        False,
        "Check 75: docs/incident-artifacts/README.md exists",
        "Check 75: docs/incident-artifacts/README.md が無い — Plan D inventory が消失",
    )

# ── 76. .claude/settings.json security baseline (BLOCKING) ───────────────────
# .claude/settings.json は Claude Code agent の権限境界を定義する重要設定。完全 AI 自走
# (Operating Model: AI が implement→verify→merge→deploy を自走、人間は監査のみ) を「安全に」
# 成立させているのは、settings.json の deny が宣言する「越えない安全境界」そのものである。
# よってこれらの deny が silent に消えていないことを機械強制し、「設定ファイルに依存する暗黙の
# 約束」を「機械強制契約」へ昇格させる。検証する deny (AI2AI.md STEP 3「自走しても越えない安全
# 境界」と対応):
#   (a) self-permission-widening 防止 = `Edit/Write(.claude/settings.json)` deny (境界 a)。
#       これが消えると AI が自分の権限を自己拡張でき、人間の制御境界が崩壊する = 最重要。
#   (b) 破壊的操作 deny = `git push --force`/`-f` (force-push)・`rm -rf` (境界 d)。
#   (c) 全 stage 事故防止 = `git add .`/`-A`/`--all` deny。
#   (d) C6 binary 保護 = `*.webp`/`*.mp3` への Edit/Write deny。
# いずれか一つでも欠けると自走運用の安全前提が崩れるため BLOCKING。
_settings76 = ROOT / ".claude" / "settings.json"
if _settings76.exists():
    try:
        _sdata76 = json.loads(_settings76.read_text(encoding="utf-8"))
        _deny76 = _sdata76.get("permissions", {}).get("deny", [])
        # 各 safety boundary を「deny リストにその marker を含む要素が存在するか」で判定。
        _req76 = {
            "Edit(.claude/settings.json) [self-permission-widening 防止]": lambda: any("Edit(.claude/settings.json)" in d for d in _deny76),
            "Write(.claude/settings.json) [self-permission-widening 防止]": lambda: any("Write(.claude/settings.json)" in d for d in _deny76),
            "git push --force [force-push 防止]": lambda: any("git push --force" in d for d in _deny76),
            "git push -f [force-push 防止]": lambda: any("git push -f" in d for d in _deny76),
            "rm -rf [破壊的削除 防止]": lambda: any("rm -rf" in d for d in _deny76),
            "git add . [全 stage 事故 防止]": lambda: any("git add ." in d for d in _deny76),
            "git add -A [全 stage 事故 防止]": lambda: any("git add -A" in d for d in _deny76),
            "git add --all [全 stage 事故 防止]": lambda: any("git add --all" in d for d in _deny76),
            "*.webp Edit/Write [C6 binary 保護]": lambda: any("*.webp" in d for d in _deny76),
            "*.mp3 Edit/Write [C6 binary 保護]": lambda: any("*.mp3" in d for d in _deny76),
        }
        _missing76 = [name for name, fn in _req76.items() if not fn()]
        check(
            not _missing76,
            f"Check 76: .claude/settings.json declares all {len(_req76)} self-drive safety-boundary denies "
            "(settings self-edit / force-push / rm -rf / git add . / webp+mp3)",
            f"Check 76: .claude/settings.json safety baseline incomplete — missing deny markers: {_missing76}. "
            "AI2AI.md STEP 3「越えない安全境界」を settings.json の deny で固定せよ (完全自走の安全前提)",
        )
    except json.JSONDecodeError as _e76:
        check(False, "Check 76: .claude/settings.json parses as JSON", f"Check 76: settings.json JSON parse error: {_e76}")
else:
    check(False, "Check 76: .claude/settings.json exists", "Check 76: .claude/settings.json が消失")

# ── 77. .claude/commands/ slash-command frontmatter integrity (BLOCKING) ─────
# .claude/commands/*.md の全 slash-command 定義が、Claude Code 仕様に従った frontmatter
# (`---\ndescription: <text>\n---`) を持つことを機械強制する。description フィールドが
# 消失すると Claude Code は command を skill listing から拾えなくなり、UI で見えない
# silent failure に陥る。
_cmds77_dir = ROOT / ".claude" / "commands"
if _cmds77_dir.is_dir():
    _cmds77 = sorted(_cmds77_dir.glob("*.md"))
    _bad77 = []
    for _cmd in _cmds77:
        _csrc = _cmd.read_text(encoding="utf-8")
        _fm77 = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", _csrc)
        if not _fm77 or not re.search(r"^description:\s*\S", _fm77.group(1), re.MULTILINE):
            _bad77.append(_cmd.name)
    check(
        not _bad77 and len(_cmds77) > 0,
        f"Check 77: all {len(_cmds77)} .claude/commands/*.md have a valid frontmatter with description",
        f"Check 77: slash-command(s) missing valid frontmatter/description: {_bad77} — "
        f"Claude Code は description を skill listing で必須要求する",
    )
else:
    check(False, "Check 77: .claude/commands/ exists", "Check 77: .claude/commands/ ディレクトリが消失")

# ── 78. .claude/agents/ sub-agent frontmatter integrity (BLOCKING) ───────────
# .claude/agents/*.md の全 sub-agent 定義が、Claude Code 仕様に従った frontmatter
# (`name:` + `description:`) を持ち、かつ `name:` がファイル名 stem と一致することを機械強制
# する。sub-agent の description は Agent tool の subagent_type 選択時に表示される真値で、
# 消失すると orchestrator は agent を呼び出せず silent unavailability になる。さらに Claude Code
# は agent を `name:` で解決する一方、人間や docs (例: .claude/CLAUDE.md の sub-agent invocation
# table) はファイル名で参照するため、name ≠ stem だと「docs が指す agent が解決できない」
# dangling reference が silent に生じる。両者の一致を固定して footgun を構造的に閉じる。
_agents78_dir = ROOT / ".claude" / "agents"
if _agents78_dir.is_dir():
    _agents78 = sorted(_agents78_dir.glob("*.md"))
    _bad78 = []
    for _ag in _agents78:
        _asrc = _ag.read_text(encoding="utf-8")
        _fm78 = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", _asrc)
        if not _fm78:
            _bad78.append(f"{_ag.name}: missing frontmatter")
            continue
        _fm_body78 = _fm78.group(1)
        _name78 = re.search(r"^name:\s*(\S+)", _fm_body78, re.MULTILINE)
        if not _name78:
            _bad78.append(f"{_ag.name}: missing name:")
        elif _name78.group(1) != _ag.stem:
            _bad78.append(f"{_ag.name}: name '{_name78.group(1)}' != filename stem '{_ag.stem}'")
        if not re.search(r"^description:\s*\S", _fm_body78, re.MULTILINE):
            _bad78.append(f"{_ag.name}: missing description:")
    check(
        not _bad78 and len(_agents78) > 0,
        f"Check 78: all {len(_agents78)} .claude/agents/*.md have valid frontmatter (name==stem + description)",
        f"Check 78: sub-agent(s) with invalid frontmatter: {_bad78} — "
        f"Claude Code は name + description を agent 解決で必須要求し、name はファイル名 stem と一致させる",
    )
else:
    check(False, "Check 78: .claude/agents/ exists", "Check 78: .claude/agents/ ディレクトリが消失")

# ── 79. .mcp.json JSON parsability (BLOCKING) ────────────────────────────────
# `.mcp.json` (MCP server project-scope config) が JSON として parse 可能であることを
# 機械強制する。空 `mcpServers: {}` の placeholder でも parse 成功すれば OK。parse 失敗
# は Claude Code 起動時に MCP server provisioning が全て失敗する catastrophic 障害で、
# 早期検出が必要。
_mcp79 = ROOT / ".mcp.json"
if _mcp79.exists():
    try:
        _mdata79 = json.loads(_mcp79.read_text(encoding="utf-8"))
        _has_servers79 = "mcpServers" in _mdata79 and isinstance(_mdata79["mcpServers"], dict)
        check(
            _has_servers79,
            f"Check 79: .mcp.json parses as JSON and has mcpServers dict ({len(_mdata79['mcpServers'])} servers)",
            "Check 79: .mcp.json missing mcpServers dict — 空 {} でもよいので明示宣言せよ",
        )
    except json.JSONDecodeError as _e79:
        check(False, "Check 79: .mcp.json parses as JSON", f"Check 79: .mcp.json JSON parse error: {_e79}")
else:
    warnings.append("Check 79 (ADVISORY): .mcp.json not present — optional, but recommended as a placeholder for future MCP integrations")

# ── 80. .claude/skills/*/SKILL.md frontmatter integrity (BLOCKING) ───────────
# .claude/skills/<name>/SKILL.md の全 skill 定義が、Claude Code 仕様に従った frontmatter
# (`name:` + `description:`) を持ち、かつ `name:` が親ディレクトリ名と一致することを機械強制
# する。skill description は Claude が proactive な skill 呼び出し判断に使う重要シグナルで、
# 消失すると skill は登録されても呼び出されなくなる silent unavailability になる。Claude Code は
# skill をディレクトリ名で配置しつつ `name:` で解決するため、name ≠ dirname だと解決が分裂する
# (Check 78 の agent name==stem と同型の identifier-coherence 不変条件)。
_skills80_dir = ROOT / ".claude" / "skills"
if _skills80_dir.is_dir():
    _skills80 = sorted(_skills80_dir.glob("*/SKILL.md"))
    _bad80 = []
    for _sk in _skills80:
        _ssrc = _sk.read_text(encoding="utf-8")
        _fm80 = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", _ssrc)
        if not _fm80:
            _bad80.append(f"{_sk.parent.name}/SKILL.md: missing frontmatter")
            continue
        _fm_body80 = _fm80.group(1)
        _name80 = re.search(r"^name:\s*(\S+)", _fm_body80, re.MULTILINE)
        if not _name80:
            _bad80.append(f"{_sk.parent.name}/SKILL.md: missing name:")
        elif _name80.group(1) != _sk.parent.name:
            _bad80.append(f"{_sk.parent.name}/SKILL.md: name '{_name80.group(1)}' != dir '{_sk.parent.name}'")
        if not re.search(r"^description:\s*\S", _fm_body80, re.MULTILINE):
            _bad80.append(f"{_sk.parent.name}/SKILL.md: missing description:")
    if _skills80:
        check(
            not _bad80,
            f"Check 80: all {len(_skills80)} .claude/skills/*/SKILL.md have valid frontmatter (name==dir + description)",
            f"Check 80: skill(s) with invalid frontmatter: {_bad80} — Claude Code は name + description を skill 解決で必須要求し、name は親ディレクトリ名と一致させる",
        )
    else:
        warnings.append("Check 80 (ADVISORY): .claude/skills/ exists but no SKILL.md found")
else:
    warnings.append("Check 80 (ADVISORY): .claude/skills/ not present — optional, 将来 skill 追加時にディレクトリ作成")

# ── 81. WebP XMP Organization field presence (BLOCKING) ──────────────────────
# WebP XMP chunk に `aio:OrganizationName` / URL / Role / StartDate 4 field が含まれる
# ことを機械強制する。index.html JSON-LD `Person.worksFor → Organization` と llms-full.txt
# の Affiliation 記述が binary AIO layer にも cross-surface に反映されている契約を、
# bytes 単位で機械強制する。Check 44 (canary token 整合) と同じ「entity 文脈が binary
# metadata にも一貫して埋まる」契約のうち、Organization axis を担う Check。
_webp81 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
if _webp81.exists():
    _wdata81 = _webp81.read_bytes()
    _pos81 = _wdata81.find(b"XMP ")
    if _pos81 >= 0:
        _size81 = int.from_bytes(_wdata81[_pos81 + 4 : _pos81 + 8], "little")
        _xmp81 = _wdata81[_pos81 + 8 : _pos81 + 8 + _size81].decode("utf-8", errors="ignore")
        _required81 = ["aio:OrganizationName", "aio:OrganizationURL", "aio:OrganizationRole", "aio:OrganizationStartDate"]
        _missing81 = [f for f in _required81 if f not in _xmp81]
        check(
            not _missing81,
            f"Check 81: WebP XMP contains all 4 Organization fields ({_required81})",
            f"Check 81: WebP XMP missing Organization fields: {_missing81} — "
            f"`update_binary_aio_organization.py` を再実行して binary AIO layer を文書側 (llms.txt / JSON-LD) と整合させよ",
        )
    else:
        check(False, "Check 81: WebP XMP chunk locatable", "Check 81: WebP に XMP chunk が無い")
else:
    check(False, "Check 81: hero WebP asset exists", "Check 81: hero WebP asset が消失")

# ── 82. MP3 ID3 TXXX:AIO:Organization frame presence (BLOCKING) ─────────────
# MP3 ID3v2.4 tag に `AIO:Organization` / URL / Role / StartDate を含む TXXX frame が
# 存在することを機械強制する。WebP XMP (Check 81) と対をなす binary AIO layer の
# Organization axis 強制。
_mp3_82 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"
if _mp3_82.exists():
    _mdata82 = _mp3_82.read_bytes()
    if _mdata82[:3] == b"ID3" and _mdata82[3] == 4:
        _tagsize82 = ((_mdata82[6] & 0x7F) << 21) | ((_mdata82[7] & 0x7F) << 14) | ((_mdata82[8] & 0x7F) << 7) | (_mdata82[9] & 0x7F)
        _body82 = _mdata82[10 : 10 + _tagsize82]
        _required82 = [b"AIO:Organization", b"AIO:OrganizationURL", b"AIO:OrganizationRole", b"AIO:OrganizationStartDate"]
        _missing82 = [r.decode() for r in _required82 if r not in _body82]
        check(
            not _missing82,
            f"Check 82: MP3 ID3 contains all 4 Organization TXXX frames",
            f"Check 82: MP3 ID3 missing Organization TXXX frames: {_missing82} — "
            f"`update_binary_aio_organization.py` を再実行して整合せよ",
        )
    else:
        check(False, "Check 82: MP3 has ID3v2.4 header", "Check 82: MP3 に ID3v2.4 header が無い")
else:
    check(False, "Check 82: portfolio BGM MP3 exists", "Check 82: portfolio BGM MP3 が消失")

# ── 83. aio-manifest.json entity.affiliation block (BLOCKING) ────────────────
# .well-known/aio-manifest.json の `entity` に Organization 情報 (`affiliation` block)
# が含まれることを機械強制する。manifest は machine-readable AIO ground truth で、
# Organization 情報の cross-surface 反映に不可欠。
_man83 = ROOT / ".well-known" / "aio-manifest.json"
if _man83.exists():
    try:
        _mdata83 = json.loads(_man83.read_text(encoding="utf-8"))
        _aff83 = _mdata83.get("entity", {}).get("affiliation", {})
        _required83 = ["organization_name", "organization_url", "named_position", "role_name", "start_date"]
        _missing83 = [k for k in _required83 if k not in _aff83]
        check(
            not _missing83 and bool(_aff83),
            f"Check 83: aio-manifest.json entity.affiliation contains all 5 required fields",
            f"Check 83: aio-manifest.json entity.affiliation missing fields: {_missing83} — "
            f"organization_name / organization_url / named_position / role_name / start_date を含めよ",
        )
    except json.JSONDecodeError as _e83:
        check(False, "Check 83: aio-manifest.json parses as JSON", f"Check 83: parse error: {_e83}")
else:
    check(False, "Check 83: aio-manifest.json exists", "Check 83: aio-manifest.json が消失")

# ── 84. README.md Organization mention (BLOCKING) ────────────────────────────
# README.md の human-readable summary に Organization 名 (`日本経営` または
# `Nihon Keiei`) が含まれることを機械強制する。人間レビュアーが最初に読む surface に
# Affiliation が記載されていない drift を防止。
_readme84 = ROOT / "README.md"
if _readme84.exists():
    _rsrc84 = _readme84.read_text(encoding="utf-8")
    _has_org84 = ("日本経営" in _rsrc84) or ("Nihon Keiei" in _rsrc84)
    check(
        _has_org84,
        "Check 84: README.md mentions Organization (`日本経営` or `Nihon Keiei`)",
        "Check 84: README.md に Organization (`日本経営` / `Nihon Keiei`) 記述が無い — "
        "Affiliation を human-readable summary に追加せよ",
    )
else:
    check(False, "Check 84: README.md exists", "Check 84: README.md が消失")

# ── 85. Claude2Claude.md Organization handoff line (BLOCKING) ────────────────
# Claude2Claude.md の「現在状態」セクションに Organization 情報が含まれることを機械強制
# する。Claude Code session の cold-start 復帰時に Affiliation 文脈が抜けることを防止。
_c2c85 = ROOT / "Claude2Claude.md"
if _c2c85.exists():
    _csrc85 = _c2c85.read_text(encoding="utf-8")
    _has_org85 = ("nkgr.co.jp" in _csrc85) or ("日本経営" in _csrc85)
    check(
        _has_org85,
        "Check 85: Claude2Claude.md mentions Organization (entity-canonical Affiliation)",
        "Check 85: Claude2Claude.md に Organization (`日本経営` / `nkgr.co.jp`) handoff 記述が無い — "
        "「現在状態」セクションに Affiliation を追加せよ",
    )
else:
    check(False, "Check 85: Claude2Claude.md exists", "Check 85: Claude2Claude.md が消失")

# ── 86. aio-manifest.json entity full-set fields (BLOCKING) ──────────────────
# entity ブロックが name / name_ja / name_alt / role / canonical_url / authoritative_context /
# disambiguation / architecture / affiliation の 9 field を全て含むことを機械強制する。
# Check 62 (canonical_url 整合) と Check 83 (affiliation block) を補完し、entity フル情報の
# cross-surface 整合を厳格化する。
_man86 = ROOT / ".well-known" / "aio-manifest.json"
if _man86.exists():
    try:
        _mdata86 = json.loads(_man86.read_text(encoding="utf-8"))
        _ent86 = _mdata86.get("entity", {})
        _required86 = ["name", "name_ja", "name_alt", "role", "canonical_url", "authoritative_context", "disambiguation", "architecture", "affiliation"]
        _missing86 = [k for k in _required86 if k not in _ent86]
        check(
            not _missing86,
            f"Check 86: aio-manifest.json entity contains all 9 required fields",
            f"Check 86: aio-manifest.json entity missing fields: {_missing86} — entity full-set context を保持せよ",
        )
    except json.JSONDecodeError as _e86:
        check(False, "Check 86: aio-manifest.json parses as JSON", f"Check 86: parse error: {_e86}")
else:
    check(False, "Check 86: aio-manifest.json exists", "Check 86: aio-manifest.json が消失")

# ── 87. CLAUDE.md / Claude2Claude.md cold-start entity context (BLOCKING) ────
# CLAUDE.md と Claude2Claude.md の両方に entity name と canonical URL ホストと
# Organization 名が含まれることを機械強制。Claude Code session が cold-start で復帰する際の
# entity 文脈欠落を防止 (Check 85 を CLAUDE.md / Claude2Claude.md 同時カバー版へ拡張)。
for _doc87, _label87 in [(ROOT / "CLAUDE.md", "CLAUDE.md"), (ROOT / "Claude2Claude.md", "Claude2Claude.md")]:
    if _doc87.exists():
        _src87 = _doc87.read_text(encoding="utf-8")
        _facts87 = {
            "entity name": ("Yuta Yokoi" in _src87) or ("横井雄太" in _src87),
            "canonical URL": "yutapr0117-design.github.io" in _src87,
            "Organization": ("日本経営" in _src87) or ("Nihon Keiei" in _src87),
        }
        _missing87 = [k for k, v in _facts87.items() if not v]
        check(
            not _missing87,
            f"Check 87 ({_label87}): cold-start entity context complete",
            f"Check 87 ({_label87}): missing cold-start entity facts: {_missing87}",
        )
    else:
        check(False, f"Check 87 ({_label87}): exists", f"Check 87 ({_label87}): 消失")

# ── 88. LICENSE entity attribution (BLOCKING) ────────────────────────────────
# root LICENSE が Copyright + entity name + canonical URL + Organization を含むことを機械強制。
_lic88 = ROOT / "LICENSE"
if _lic88.exists():
    _lsrc88 = _lic88.read_text(encoding="utf-8")
    _facts88 = {
        "Copyright": "Copyright" in _lsrc88,
        "entity name": ("Yuta Yokoi" in _lsrc88) or ("横井雄太" in _lsrc88),
        "canonical URL": "yutapr0117-design.github.io" in _lsrc88,
        "Organization": ("日本経営" in _lsrc88) or ("Nihon Keiei" in _lsrc88),
    }
    _missing88 = [k for k, v in _facts88.items() if not v]
    check(
        not _missing88,
        "Check 88: LICENSE contains Copyright + entity + canonical URL + Organization",
        f"Check 88: LICENSE missing required attribution: {_missing88}",
    )
else:
    check(False, "Check 88: LICENSE exists", "Check 88: LICENSE が消失")

# ── 89. governance files (CONTRIBUTING / CODEOWNERS / CHANGELOG) presence (BLOCKING) ─
# 3 governance ファイルが存在し entity name を含むことを機械強制。
_gov89 = [(ROOT / "CONTRIBUTING.md", "CONTRIBUTING.md"), (ROOT / "CODEOWNERS", "CODEOWNERS"), (ROOT / "CHANGELOG.md", "CHANGELOG.md")]
_gov_missing89 = []
for _p, _label in _gov89:
    if not _p.exists():
        _gov_missing89.append(f"{_label}: missing")
        continue
    _src = _p.read_text(encoding="utf-8")
    if not (("Yuta Yokoi" in _src) or ("横井雄太" in _src)):
        _gov_missing89.append(f"{_label}: no entity name")
check(
    not _gov_missing89,
    "Check 89: CONTRIBUTING.md / CODEOWNERS / CHANGELOG.md all exist with entity attribution",
    f"Check 89: governance file issues: {_gov_missing89}",
)

# ── 90. .claude/CLAUDE.md + .claude/README.md entity context (BLOCKING) ──────
# .claude/CLAUDE.md と .claude/README.md の両方が entity name と Organization 名を含むことを
# 機械強制。Claude Code 用ファイル群全体への entity 整合担保。
for _doc90, _label90 in [(ROOT / ".claude" / "CLAUDE.md", ".claude/CLAUDE.md"), (ROOT / ".claude" / "README.md", ".claude/README.md")]:
    if _doc90.exists():
        _src90 = _doc90.read_text(encoding="utf-8")
        _facts90 = {
            "entity name": ("Yuta Yokoi" in _src90) or ("横井雄太" in _src90),
            "Organization": ("日本経営" in _src90) or ("Nihon Keiei" in _src90),
        }
        _missing90 = [k for k, v in _facts90.items() if not v]
        check(
            not _missing90,
            f"Check 90 ({_label90}): entity + Organization context present",
            f"Check 90 ({_label90}): missing context: {_missing90}",
        )
    else:
        check(False, f"Check 90 ({_label90}): exists", f"Check 90 ({_label90}): 消失")

# ── 91. binary metadata date freshness (BLOCKING) ────────────────────────────
# (C 案 + 9 案) WebP XMP の xmp:ModifyDate と xmp:MetadataDate、MP3 ID3 の
# AIO:MetadataLastModified、aio-manifest.json の last_metadata_update が全て
# 同一日 (YYYY-MM-DD 一致) であることを機械強制する。binary の semantic 編集と
# 日付フィールドの同期更新を pre-commit で構造的に保証 (C6 derived-value 例外
# 条項の運用契約)。手動経路で binary を編集して日付を忘れた場合、本 Check が
# fail で気づく。
import re as _re91
_webp91 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
_mp3_91 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"
_man91 = ROOT / ".well-known" / "aio-manifest.json"
_dates91 = {}
if _webp91.exists():
    import struct as _struct91
    _wdata91 = _webp91.read_bytes()
    _xp91 = _wdata91.find(b"XMP ")
    if _xp91 >= 0:
        _xs91 = _struct91.unpack("<I", _wdata91[_xp91 + 4 : _xp91 + 8])[0]
        _xtext91 = _wdata91[_xp91 + 8 : _xp91 + 8 + _xs91].decode("utf-8", errors="ignore")
        _m_modify = _re91.search(r"<xmp:ModifyDate>(\d{4}-\d{2}-\d{2})", _xtext91)
        _m_metadata = _re91.search(r"<xmp:MetadataDate>(\d{4}-\d{2}-\d{2})", _xtext91)
        if _m_modify: _dates91["webp:ModifyDate"] = _m_modify.group(1)
        if _m_metadata: _dates91["webp:MetadataDate"] = _m_metadata.group(1)
if _mp3_91.exists():
    _mdata91 = _mp3_91.read_bytes()
    _m_id3 = _re91.search(rb"AIO:MetadataLastModified\x00(\d{4}-\d{2}-\d{2})", _mdata91)
    if _m_id3: _dates91["mp3:AIO:MetadataLastModified"] = _m_id3.group(1).decode("ascii")
if _man91.exists():
    try:
        _md91 = json.loads(_man91.read_text(encoding="utf-8"))
        _lmu91 = _md91.get("last_metadata_update", "")
        _m_lmu = _re91.match(r"(\d{4}-\d{2}-\d{2})", _lmu91)
        if _m_lmu: _dates91["manifest:last_metadata_update"] = _m_lmu.group(1)
    except json.JSONDecodeError:
        pass
_unique_dates91 = set(_dates91.values())
check(
    len(_unique_dates91) == 1 and len(_dates91) >= 4,
    f"Check 91: all {len(_dates91)} binary/manifest date fields share one date ({list(_unique_dates91)[0] if _unique_dates91 else 'none'})",
    f"Check 91: binary/manifest date drift — {_dates91}. C6 derived-value 例外条項に従い、"
    f"`update_binary_aio_organization.py` または `update_aio_digests.py` を再実行して日付を同期せよ",
)

# ── 92. C6 derived-value exception canon presence (BLOCKING) ─────────────────
# (A 案 canon check) CLAUDE.md と AI2AI.md の両方の C6 説明に「derived-value
# auto-update」「Exception」の文言が含まれることを機械強制する。canon 文言の
# 静かな revert を防止。
_c6_canon_files = [(ROOT / "CLAUDE.md", "CLAUDE.md"), (ROOT / "AI2AI.md", "AI2AI.md")]
_c6_canon_missing = []
for _p, _label in _c6_canon_files:
    if not _p.exists():
        _c6_canon_missing.append(f"{_label}: missing")
        continue
    _src = _p.read_text(encoding="utf-8")
    if "derived-value auto-update" not in _src and "derived value" not in _src.lower():
        _c6_canon_missing.append(f"{_label}: no derived-value clause")
check(
    not _c6_canon_missing,
    "Check 92: CLAUDE.md + AI2AI.md C6 both document the derived-value auto-update exception",
    f"Check 92: C6 canon missing derived-value clause: {_c6_canon_missing} — "
    f"canon 文言が静かに revert された可能性。A 案 例外条項を再記述せよ",
)

# ── 93. aio-manifest.json last_metadata_update field present (BLOCKING) ──────
# (8 案 + 10 案) aio-manifest.json に top-level `last_metadata_update` が存在する
# ことを機械強制 (Check 91 が真値として使う central anchor)。
_man93 = ROOT / ".well-known" / "aio-manifest.json"
if _man93.exists():
    try:
        _md93 = json.loads(_man93.read_text(encoding="utf-8"))
        _lmu93 = _md93.get("last_metadata_update", "")
        _ok93 = bool(_lmu93 and _re91.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", _lmu93))
        check(
            _ok93,
            f"Check 93: aio-manifest.json last_metadata_update = {_lmu93} (ISO-8601)",
            f"Check 93: aio-manifest.json last_metadata_update missing or malformed: {_lmu93!r}",
        )
    except json.JSONDecodeError as _e93:
        check(False, "Check 93: aio-manifest.json parses", f"Check 93: parse error: {_e93}")
else:
    check(False, "Check 93: aio-manifest.json exists", "Check 93: aio-manifest.json missing")

# ── 94. update_aio_digests.py / update_binary_aio_organization.py tool integrity (BLOCKING) ─
# (B1 + B2 案) 両 tool が `_lib_io` から helper を import していることを機械強制。
# 「日付同期を tool が責務として持つ」契約を構造的に保護。
_tools94 = [
    (ROOT / ".github" / "scripts" / "update_aio_digests.py", "update_aio_digests.py"),
    (ROOT / ".github" / "scripts" / "update_binary_aio_organization.py", "update_binary_aio_organization.py"),
]
_tool_missing94 = []
for _p, _label in _tools94:
    if not _p.exists():
        _tool_missing94.append(f"{_label}: missing")
        continue
    _src = _p.read_text(encoding="utf-8")
    if "update_webp_xmp_dates" not in _src or "update_mp3_metadata_date" not in _src:
        _tool_missing94.append(f"{_label}: missing date sync responsibility")
check(
    not _tool_missing94,
    "Check 94: B1/B2 tools (update_aio_digests / update_binary_aio_organization) both reference date sync helpers",
    f"Check 94: tools missing date-sync responsibility: {_tool_missing94}",
)

# ── 95. _lib_io.py date helpers (BLOCKING) ───────────────────────────────────
# (6 案) `_lib_io.py` に `now_iso8601`, `update_webp_xmp_dates`,
# `update_mp3_metadata_date` の 3 public helper が存在することを機械強制。
_lib95 = ROOT / ".github" / "scripts" / "_lib_io.py"
if _lib95.exists():
    _lsrc95 = _lib95.read_text(encoding="utf-8")
    _req95 = ["now_iso8601", "update_webp_xmp_dates", "update_mp3_metadata_date"]
    _missing95 = [fn for fn in _req95 if not _re91.search(rf"^def {fn}\b", _lsrc95, _re91.MULTILINE)]
    check(
        not _missing95,
        f"Check 95: _lib_io.py exports all 3 date helpers ({_req95})",
        f"Check 95: _lib_io.py missing date helpers: {_missing95}",
    )
else:
    check(False, "Check 95: _lib_io.py exists", "Check 95: _lib_io.py が消失")

# ── 96. Phase 1 shipped-code 1-to-1 docs bijection (BLOCKING) ────────────────
# Docs Phase 7 骨格: Phase 1 対象 shipped code (33 ファイル) が `docs/files/<path>.md`
# のミラー構造で 1 対 1 ドキュメント化されていることを機械強制。新規 shipped ファイルを
# 追加するたびに対応 doc も同時に作成しないと pre-commit fail。Phase 2-6 は順次拡張。
_phase1_targets96 = [
    # Phase 1: shipped code (33)
    "main.js", "index.html", "style.css", "sw.js", "aio-guard.js",
    "error-suppressor.js", "karte-init.js", "theme-init.js",
    "googlea7059bedc6fe8bdc.html",
    "js/aidk-rails.js", "js/apps.js", "js/brand.js", "js/components.js",
    "js/constants.js", "js/fatal-overlay.js", "js/identity.js",
    "js/meta-management.js", "js/mobile-drawer.js", "js/page-meta.js",
    "js/pages.js", "js/perf-guards.js", "js/pure-utils.js",
    "js/quiz-renderer.js", "js/router.js", "js/state.js",
    "js/storage.js", "js/store.js", "js/theme.js", "js/ui-components.js",
    "js/quiz/architecture-quiz-data.js", "js/quiz/aws-quiz-data.js",
    "js/quiz/pm-quiz-data.js", "js/quiz/quality-quiz-data.js",
    # Phase 2: AIO 正本層 + crawler 制御 (11)
    "llms.txt", "llms-full.txt", "llms_well-known.txt",
    ".well-known/llms.txt", ".well-known/llms_well-known.txt",
    ".well-known/aio-manifest.json", ".well-known/index.json",
    ".well-known/agent-skills/index.json", ".well-known/mcp.json",
    "robots.txt", "sitemap.xml",
    # Phase 3: config / scripts / workflows / Claude Code (25)
    ".github/scripts/_lib_io.py",
    ".github/scripts/aio_monitoring.py",
    ".github/scripts/check_aio_digests.py",
    ".github/scripts/check_binary_aio_metadata.py",
    ".github/scripts/check_css_stylelint.py",
    ".github/scripts/check_public_deployment_freshness.py",
    ".github/scripts/check_repository_consistency.py",
    ".github/scripts/update_aio_digests.py",
    ".github/scripts/update_binary_aio_organization.py",
    ".github/workflows/aio-monitoring.yml",
    ".github/workflows/architecture-validation.yml",
    ".github/workflows/auto-update-aio-digests.yml",
    ".github/workflows/playwright-regression.yml",
    ".github/workflows/update-playwright-snapshots.yml",
    ".github/dependabot.yml",
    ".claude/settings.json",
    ".claude/README.md",
    ".claude/CLAUDE.md",
    ".claude/agents/aio-guardian.md",
    ".claude/agents/check-author.md",
    ".claude/agents/repo-auditor.md",
    ".claude/commands/archive-incidents.md",
    ".claude/commands/deliver.md",
    ".claude/commands/verify.md",
    ".claude/commands/audit.md",
    ".claude/commands/sync-docs.md",
    ".claude/commands/increment.md",
    ".claude/skills/repo-status/SKILL.md",
    ".stylelintrc.json",
    "eslint.config.mjs",
    "package.json",
    "package-lock.json",
    "playwright.config.cjs",
    "e2e/portfolio.spec.js",
    # Phase 4: binary assets (2)
    "yuta-yokoi-ai-pm-orchestration-system.webp",
    "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3",
    # Phase 5: dot files / meta config (6)
    ".editorconfig", ".gitattributes", ".gitignore",
    ".mcp.json", ".nvmrc", ".nojekyll",
    # Phase 6: root docs + docs/* meta-docs (47)
    "AI2AI.md", "CLAUDE.md", "Claude2Claude.md", "ChatGPT2ChatGPT.md",
    "README.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md",
    "CODEOWNERS", "CHANGELOG.md",
    "docs/README.md",
    "docs/architecture/check-repository-consistency-map.md",
    "docs/architecture/file-size-budget.md",
    "docs/architecture/main-js-extraction-map.md",
    "docs/architecture/major-update-readiness.md",
    "docs/architecture/repository-maintainability-map.md",
    "docs/architecture/research-application-policy.md",
    "docs/architecture/total-check-runbook.md",
    "docs/evidence/ai-pioneer-identity-review.md",
    "docs/evidence/public-deployment-freshness-review.md",
    "docs/incident-artifacts/README.md",
    "docs/incident-artifacts/decision-v80-e2e-and-maintainability-stage-1.md",
    "docs/incident-artifacts/decision-v80-maintainability-roadmap.md",
    "docs/incident-artifacts/decision-v80-phase2-aio-update-canary.md",
    "docs/incident-artifacts/decision-v80-phase2-artifact-governance.md",
    "docs/incident-artifacts/decision-v80-phase2-ci-hygiene.md",
    "docs/incident-artifacts/decision-v80-phase2-ci-hygiene-2.md",
    "docs/incident-artifacts/decision-v80-phase2-ci-hygiene-3.md",
    "docs/incident-artifacts/decision-v80-phase2-ci-hygiene-4.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-aio-update-canary.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-artifact-governance.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-baseline-gate-doc-hardening.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-ci-baseline-pipeline-hardening.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-ci-hygiene-4.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-consistency-invariant-hardening.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-console-fix-and-eslint-v10-and-research-application.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-dependency-modernization-and-flat-config.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-dev-ergonomics-and-lint-coverage.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-domain-authority-worksfor.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-lint-hygiene-and-doc-sync.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-public-freshness-observation.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-pure-utility-and-static-data-extraction.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-quiz-domain-split-and-bloat-governance.md",
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-self-documentation-integrity.md",
    "docs/incident-artifacts/update-portfolio.v70-experiment.yml",
    "docs/session-records/AI2AI-archive.md",
    "docs/session-records/incident-artifacts-archive-v74.md",
    # Final audit 漏れ補完 (4) — grep ベース全数監査で発見
    ".well-known/api-catalog",
    "jsconfig.json",
    "docs/evidence/aio-monitoring-log.json",
    "e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png",
    # Session handoff (本セッション末尾で AI-agnostic な引き継ぎ書を追加)
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-comment-injection.md",
    # why-only comment-injection increment record (handoff §10 の実行記録)
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-why-only-comment-injection.md",
    # self-drive operating-model 確立セッションの引き継ぎ書 (PR #60〜#64)
    "docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-self-drive-operating-model.md",
]
_missing96 = []
for _t in _phase1_targets96:
    _doc = ROOT / "docs" / "files" / f"{_t}.md"
    if not _doc.exists():
        _missing96.append(_t)
check(
    not _missing96,
    f"Check 96: all {len(_phase1_targets96)} Phase 1-6 files (shipped + AIO + config + binary + dot + meta-docs) have 1-to-1 docs",
    f"Check 96: missing 1-to-1 docs for: {_missing96} — `docs/files/_template.md` を元に作成せよ",
)

# ── 97. docs/files/*.md frontmatter integrity (BLOCKING) ─────────────────────
# 各 1 対 1 doc が必須 frontmatter (file / audience / last-updated / canonical-ref) を
# 持ち、かつ `file:` 値が自身の派生ソースパス (docs/files/<path>.md → <path>) と一致する
# ことを機械強制。drift を pre-commit で防止。`file:` の self-coherence を加えることで、
# mirror を copy-paste 新設した際に `file:` 更新を忘れ「別ファイルを指す mirror」が
# Check 97/98 を通過してしまう silent drift (Check 78/80 の name==identifier と同型) を閉じる。
_docs97_dir = ROOT / "docs" / "files"
_bad97 = []
if _docs97_dir.is_dir():
    for _md in _docs97_dir.rglob("*.md"):
        if _md.name in ("README.md", "_template.md"):
            continue
        _src = _md.read_text(encoding="utf-8")
        _fm = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", _src)
        if not _fm:
            _bad97.append(f"{_md.relative_to(_docs97_dir)}: no frontmatter")
            continue
        _fm_body = _fm.group(1)
        for _required in ["file:", "audience:", "last-updated:", "canonical-ref:"]:
            if not re.search(rf"^{_required}", _fm_body, re.MULTILINE):
                _bad97.append(f"{_md.relative_to(_docs97_dir)}: missing {_required}")
        # file: self-coherence — 値が mirror 自身の派生ソースパスと一致するか
        _relmd97 = _md.relative_to(_docs97_dir).as_posix()
        if _relmd97.endswith(".md"):
            _derived97 = _relmd97[:-len(".md")]
            _filefld97 = re.search(r"^file:\s*(\S+)", _fm_body, re.MULTILINE)
            if _filefld97 and _filefld97.group(1) != _derived97:
                _bad97.append(
                    f"{_relmd97}: file:'{_filefld97.group(1)}' != derived source path '{_derived97}' "
                    "(mirror が別ファイルを指している — copy-paste drift)"
                )
check(
    not _bad97,
    f"Check 97: all docs/files/*.md have required frontmatter (file / audience / last-updated / canonical-ref) and file:==derived path",
    f"Check 97: doc frontmatter issues: {_bad97[:5]}{'...' if len(_bad97) > 5 else ''}",
)

# ── 98. docs/files/*.md 5-axis section presence (BLOCKING) ───────────────────
# 各 1 対 1 doc が必須 5+1 セクション見出し (## What / ## Why / ## How / ## Constraints
# / ## Change impact / ## Audience-specific notes) を持つことを機械強制。template と
# のセクション整合を pre-commit で保証。
_required_sections98 = ["## What", "## Why", "## How", "## Constraints", "## Change impact", "## Audience-specific notes"]
_bad98 = []
if _docs97_dir.is_dir():
    for _md in _docs97_dir.rglob("*.md"):
        if _md.name in ("README.md", "_template.md"):
            continue
        _src = _md.read_text(encoding="utf-8")
        _missing_sec = [s for s in _required_sections98 if s not in _src]
        if _missing_sec:
            _bad98.append(f"{_md.relative_to(_docs97_dir)}: missing {_missing_sec}")
check(
    not _bad98,
    f"Check 98: all docs/files/*.md have required 5+1-axis sections (What / Why / How / Constraints / Change impact / Audience-specific notes)",
    f"Check 98: doc section issues: {_bad98[:3]}{'...' if len(_bad98) > 3 else ''}",
)

# ── 99. docs/files/README.md + _template.md presence (BLOCKING) ──────────────
# 1 対 1 docs の inventory と template が存在することを機械強制。
_inventory99 = ROOT / "docs" / "files" / "README.md"
_template99 = ROOT / "docs" / "files" / "_template.md"
check(
    _inventory99.exists() and _template99.exists(),
    "Check 99: docs/files/README.md (inventory) と _template.md (5-軸 template) が両方存在",
    f"Check 99: missing — README.md={_inventory99.exists()}, _template.md={_template99.exists()}",
)

# ── 100. theme-init.js hardcoded storage keys ↔ constants.js / brand.js (BLOCKING) ─
# theme-init.js は main.js (ESM, async) ロード前に <head> で同期実行され、FOUC を防ぐため
# localStorage から theme/brand を復元する。そのため STORAGE_KEY ('portfolio_enhanced_v45')
# と Brand.KEY ('portfolio_brand_v45') を **意図的にハードコード複製** している (import すると
# main.js ロード前に解決できない)。js/constants.js の STORAGE_KEY や js/brand.js の KEY を
# 変更したとき theme-init.js のリテラルを更新し忘れると、初期ペイントだけ旧キーを読み first-paint
# のテーマ/ブランドが壊れる — main.js ロード後は正しいキーで再適用されるため test でも気づきに
# くい silent drift。本 Check はこの 2 リテラルが canonical 値と一致することを BLOCKING で保証する。
# (why-only コメント注入 increment で発見・systematize: コメントが複製を説明し、本 Check が強制する)
_themeinit100 = ROOT / "theme-init.js"
_constants100 = ROOT / "js" / "constants.js"
_brand100 = ROOT / "js" / "brand.js"
if _themeinit100.exists() and _constants100.exists() and _brand100.exists():
    _ti_src100 = _themeinit100.read_text(encoding="utf-8")
    _const_src100 = _constants100.read_text(encoding="utf-8")
    _brand_src100 = _brand100.read_text(encoding="utf-8")
    _storage_key_m100 = re.search(r"STORAGE_KEY:\s*'([^']+)'", _const_src100)
    _brand_key_m100 = re.search(r"const\s+KEY\s*=\s*'([^']+)'", _brand_src100)
    _storage_key100 = _storage_key_m100.group(1) if _storage_key_m100 else None
    _brand_key100 = _brand_key_m100.group(1) if _brand_key_m100 else None
    # 100a — theme-init.js が constants.js の canonical STORAGE_KEY を読む。
    check(
        _storage_key100 is not None and (f"getItem('{_storage_key100}')" in _ti_src100),
        f"Check 100a: theme-init.js reads the canonical STORAGE_KEY ('{_storage_key100}') from js/constants.js",
        f"Check 100a: theme-init.js does not read STORAGE_KEY '{_storage_key100}' — "
        "the FOUC-prevention pre-paint reads a stale localStorage key (js/constants.js ↔ theme-init.js drift)",
        blocking=True,
    )
    # 100b — theme-init.js が brand.js の canonical KEY を読む。
    check(
        _brand_key100 is not None and (f"getItem('{_brand_key100}')" in _ti_src100),
        f"Check 100b: theme-init.js reads the canonical Brand.KEY ('{_brand_key100}') from js/brand.js",
        f"Check 100b: theme-init.js does not read Brand.KEY '{_brand_key100}' — "
        "the FOUC-prevention pre-paint reads a stale localStorage brand key (js/brand.js ↔ theme-init.js drift)",
        blocking=True,
    )
else:
    check(
        False,
        "",
        "Check 100: theme-init.js / js/constants.js / js/brand.js のいずれかが見つからず "
        "storage-key consistency を検証できない",
        blocking=True,
    )

# ── 101. style.css forced-colors (HCM) focus support (BLOCKING) ──────────────
# Windows High Contrast Mode (`@media (forced-colors: active)`) では box-shadow が描画されず
# author color が system color に置換される。focus 表示を box-shadow のみに依存している箇所
# (.skip-link:focus は outline:none + box-shadow) は HCM で消え WCAG 2.4.7 / 1.4.1 違反になる。
# style.css に forced-colors 専用の outline-based focus fallback が存在することを BLOCKING で
# 固定し、将来の編集で silently strip されるのを防ぐ。このブロックは forced-colors モードでのみ
# 有効で通常描画 (CI baseline) に非影響ゆえ §3 baseline ゲート非該当 (render-neutral)。
# why-only comment-injection track で発見・systematize (Check 100 と同 pattern)。
_css101 = ROOT / "style.css"
if _css101.exists():
    _src101 = _css101.read_text(encoding="utf-8")
    _fc101 = re.search(r"@media\s*\(\s*forced-colors\s*:\s*active\s*\)", _src101)
    _focus_in_fc101 = False
    if _fc101:
        # forced-colors at-rule 開始から十分な window を見て、focus selector + outline 復帰を確認。
        _window101 = _src101[_fc101.start():_fc101.start() + 800]
        _focus_in_fc101 = (":focus" in _window101) and ("outline" in _window101)
    check(
        bool(_fc101) and _focus_in_fc101,
        "Check 101: style.css has a forced-colors (HCM) block restoring outline-based focus (WCAG 2.4.7/1.4.1)",
        "Check 101: style.css is missing the @media (forced-colors: active) focus fallback — "
        "High Contrast Mode users lose the focus indicator (box-shadow is not painted in HCM)",
        blocking=True,
    )
else:
    check(
        False,
        "",
        "Check 101: style.css not found — forced-colors focus support を検証できない",
        blocking=True,
    )

# ── 102. core operating-model policy documented in canon (BLOCKING) ──────────
# このリポジトリの核心ガバナンス契約「AI が implement→verify→merge→deploy を自走し、人間の
# runtime 役割は制御 + 監査 (CI オールグリーン) のみ」が canon に明記され続けることを機械強制。
# 黙って消えると、後続セッションが「毎手確認」運用に逆戻りし、オーナーの audit-CI-only 運用が
# 壊れる。AI2AI.md STEP 3 の Operating Model marker (102a) と CLAUDE.md §7 の参照 (102b) を
# presence で固定し drift を防ぐ。
_ai2ai102 = ROOT / "AI2AI.md"
_claude102 = ROOT / "CLAUDE.md"
if _ai2ai102.exists() and _claude102.exists():
    _ai2ai_src102 = _ai2ai102.read_text(encoding="utf-8")
    _claude_src102 = _claude102.read_text(encoding="utf-8")
    # 102a — AI2AI.md に Operating Model 宣言（英語 marker + 日本語 marker + CI 緑条件）が存在。
    _102a = (
        "Operating Model" in _ai2ai_src102
        and "核心運用ポリシー" in _ai2ai_src102
        and "CI オールグリーン" in _ai2ai_src102
    )
    check(
        _102a,
        "Check 102a: AI2AI.md documents the core Operating Model policy (AI self-driving / human control-and-audit-only)",
        "Check 102a: AI2AI.md is missing the core Operating Model policy markers "
        "('Operating Model' / '核心運用ポリシー' / 'CI オールグリーン') — 核心ガバナンス契約が canon から消えた",
        blocking=True,
    )
    # 102b — CLAUDE.md が同ポリシーを参照（router からの到達性）。
    _102b = ("核心運用ポリシー" in _claude_src102) or ("Operating Model" in _claude_src102)
    check(
        _102b,
        "Check 102b: CLAUDE.md references the core Operating Model policy",
        "Check 102b: CLAUDE.md no longer references the Operating Model policy — "
        "router から核心ポリシーへの到達性が失われた",
        blocking=True,
    )
    # 102c — 「AI proposes, human disposes」献策ポリシーが Operating Model に明記。
    # AI 自走の中核機能として「AI が献策し人間が裁可する」が canon に保持されることを固定。
    _102c = ("AI proposes, human disposes" in _ai2ai_src102) and ("献策" in _ai2ai_src102)
    check(
        _102c,
        "Check 102c: AI2AI.md documents the proposal policy (AI proposes, human disposes)",
        "Check 102c: AI2AI.md is missing the 'AI proposes, human disposes'（AI 献策 / 人間裁可）policy — "
        "AI 自走の中核機能（能動的献策）の canon 明記が消えた",
        blocking=True,
    )
    # 102d — 「改善に完了状態は存在しない」継続改善ポリシーが Operating Model に明記。
    # AI 側の「もう十分」自発停止・完了宣言を canon が禁じ続けることを固定。これが消えると
    # 後続 AI が「一区切りが妥当」と停止し、オーナーの「終わりなき改善を自走」運用が壊れる。
    _102d = ('No terminal "done" state' in _ai2ai_src102) and ("完了" in _ai2ai_src102)
    check(
        _102d,
        "Check 102d: AI2AI.md documents the continuous-improvement policy (No terminal \"done\" state)",
        "Check 102d: AI2AI.md is missing the 'No terminal \"done\" state'（改善に完了状態は存在しない）"
        "continuous-improvement policy — AI の自発的停止/完了宣言を禁じる canon が消えた",
        blocking=True,
    )
    # 102e — 「改善は無限・枯渇/収束の自己判断禁止」が canon に明記。AI が「改善は尽きた/収束した」
    # という self-assessment of exhaustion を下すことを禁じる真理を固定する。102d (完了宣言禁止) の
    # 上位概念で、本セッションで AI が繰り返した「収束した」誤判断 (毎回偽だった) の再発を構造的に防ぐ。
    _102e = ("Infinite improvement" in _ai2ai_src102) and ("改善は無限" in _ai2ai_src102)
    check(
        _102e,
        "Check 102e: AI2AI.md documents the infinite-improvement truth (改善は無限・枯渇の自己判断禁止)",
        "Check 102e: AI2AI.md is missing the 'Infinite improvement'（改善は無限・完璧は存在しない・"
        "枯渇/収束の自己判断禁止）truth — AI が「改善は尽きた/収束した」と誤判断して自走を止める"
        "失敗モードを禁じる canon が消えた",
        blocking=True,
    )
    # 102f — 「reflect-then-organize」= AI が非自明な増分前に簡潔な見解 (pros/cons・レンズ確認) を
    # 出してから進む品質ステップが Operating Model に明記され、CLAUDE.md §5 The loop にも記載される
    # ことを固定。見解化＝暗黙推論の明示構造化が 102e の枯渇誤謬を破る実証 (2026-06-21: 人間ゼロ入力で
    # AI が 10 案自己生成→6 案自走可能と判明) を受けて正式フロー化した。silent に消えると AI が
    # 「枯渇」自己判断のまま停止/padding へ滑る失敗モードへ戻るため presence を BLOCKING 強制する。
    _102f = ("reflect-then-organize" in _ai2ai_src102) and ("reflect-then-organize" in _claude_src102)
    check(
        _102f,
        "Check 102f: reflect-then-organize quality step documented (AI2AI.md Operating Model + CLAUDE.md §5)",
        "Check 102f: 'reflect-then-organize'（自己見解→自己整理を品質ステップ化）の canon 明記が消えた — "
        "AI2AI.md Operating Model と CLAUDE.md §5 The loop の両方に存在させよ。"
        "これが消えると AI が枯渇誤謬(102e)のまま停止/padding へ滑る失敗モードに戻る",
        blocking=True,
    )
else:
    check(
        False,
        "",
        "Check 102: AI2AI.md / CLAUDE.md のいずれかが見つからず operating-model policy を検証できない",
        blocking=True,
    )

# ── 103. style.css prefers-contrast (higher-contrast) support (BLOCKING) ─────
# ユーザーが OS で「より高いコントラスト」を要求した時のみ有効化する fallback (境界線/補助
# テキスト/focus を濃く・太く) が style.css に存在することを固定。WCAG 1.4.11 Non-text Contrast
# 強化。Check 101 (forced-colors) と同じく render-neutral (当該設定が非アクティブな通常描画 =
# CI baseline には非影響) ゆえ §3 baseline ゲート非該当。将来 silently strip されるのを防ぐ。
_css103 = ROOT / "style.css"
if _css103.exists():
    _src103 = _css103.read_text(encoding="utf-8")
    _pc103 = re.search(r"@media\s*\(\s*prefers-contrast\s*:\s*more\s*\)", _src103)
    check(
        bool(_pc103),
        "Check 103: style.css has a prefers-contrast: more block (WCAG 1.4.11 higher-contrast support)",
        "Check 103: style.css is missing the @media (prefers-contrast: more) fallback — "
        "higher-contrast-preference users lose the strengthened borders/focus contrast",
        blocking=True,
    )
else:
    check(
        False,
        "",
        "Check 103: style.css not found — prefers-contrast support を検証できない",
        blocking=True,
    )

# ── 104. verify-gate scripts carry a Python 3.10+ version guard (BLOCKING) ────
# `npm run verify` runs these Python scripts under whatever `python3` resolves to on
# the machine. They use 3.10+ syntax (PEP 604 `str | None` union annotations), so on
# Python 3.9 (the macOS system interpreter at /usr/bin/python3)
# check_repository_consistency.py crashes with an opaque
# `TypeError: unsupported operand type(s) for |` at import time — a hard-to-diagnose
# failure for the next (AI-agnostic) agent who lands on a fresh machine. Each verify-gate
# script now fails fast with an actionable "requires Python 3.10+" message; this Check
# fixes the guard in place so it cannot be silently removed, re-introducing the
# cryptic-crash class. (Sibling to Check 55's vacuous-gate and Check 56's orphan
# detection: it closes a silent/cryptic-failure class structurally.)
# Derive the script set from package.json `scripts` (every .github/scripts/*.py invoked via
# npm) rather than hardcoding it — so a Python script newly wired into the verify gate is
# automatically required to carry the guard, exactly as Check 46 derives the JS file set.
_pkg104 = ROOT / "package.json"
_guard_scripts104 = []
if _pkg104.exists():
    _scripts104 = json.loads(_pkg104.read_text(encoding="utf-8")).get("scripts", {})
    _all_script_src104 = " ".join(_scripts104.values())
    _guard_scripts104 = sorted(set(re.findall(r"\.github/scripts/[\w./-]+\.py", _all_script_src104)))
_guard_marker104 = "sys.version_info < (3, 10)"
_missing104 = [
    p for p in _guard_scripts104
    if not (ROOT / p).exists()
    or _guard_marker104 not in (ROOT / p).read_text(encoding="utf-8")
]
check(
    bool(_guard_scripts104) and not _missing104,
    f"Check 104: all {len(_guard_scripts104)} npm-invoked Python scripts (derived from package.json) carry a Python 3.10+ version guard",
    f"Check 104: these npm-invoked Python scripts are missing the `{_guard_marker104}` guard: {_missing104}. "
    "3.10+ 専用構文 (PEP 604 `str | None`) を使うため、guard 無しでは Python 3.9 で cryptic TypeError になる。"
    "各スクリプトの import 直後に version guard を復元せよ" if _guard_scripts104 else
    "Check 104: package.json から .github/scripts/*.py を 1 つも検出できない (package.json の scripts を確認せよ)",
    blocking=True,
)

# ── 105. check-repository-consistency-map.md ↔ implementation bijection (BLOCKING) ─
# check-repository-consistency-map.md is the human-facing inventory of every Check. It is
# hand-maintained in parallel with the implementation, so it can silently fall behind when a
# Check is added but the map row is forgotten (or vice-versa). Check 45 already guards the
# docstring↔section bijection WITHIN this file; this is its cross-document counterpart. We
# extract the integer check-numbers from the map's table rows (`| N |` / `| Na |`, alpha
# sub-checks normalized to their integer) and from this file's `# ── N.` section headers,
# and require the two sets to coincide exactly — so the inventory a reviewer reads can never
# drift from what the script actually enforces.
_map105 = ROOT / "docs" / "architecture" / "check-repository-consistency-map.md"
if _map105.exists() and CHECK_SOURCE_FILES:
    _mapsrc105 = _map105.read_text(encoding="utf-8")
    _map_nums105 = {int(m) for m in re.findall(r"^\|\s*(\d+)[a-z]?\s*\|", _mapsrc105, re.MULTILINE)}
    _, _impl_sec105 = _aggregate_check_numbers()
    _impl_nums105 = set(_impl_sec105)
    _only_map105 = sorted(_map_nums105 - _impl_nums105)
    _only_impl105 = sorted(_impl_nums105 - _map_nums105)
    check(
        bool(_impl_nums105) and _map_nums105 == _impl_nums105,
        f"Check 105: check-repository-consistency-map.md documents exactly the {len(_impl_nums105)} implemented checks (map ↔ implementation bijection)",
        f"Check 105: check-map and implementation have drifted — only in map: {_only_map105}; "
        f"missing a map row (implemented but undocumented): {_only_impl105}. "
        "新 Check 追加時に map へ行を足し忘れる drift を防ぐ (Check 45 の docstring↔section bijection の cross-document 版)",
        blocking=True,
    )
else:
    check(False, "", "Check 105: check-map or implementation script not found — bijection を検証できない", blocking=True)

# ── 106. .nvmrc ↔ CI workflow node-version single-major alignment (BLOCKING) ──
# Check 69 verifies package.json `engines.node` *covers* the CI node-version pins, but two
# gaps remain: (1) `.nvmrc` — the local-dev contract `nvm` reads — is not tied to the CI pin,
# so a contributor's local Node could silently differ from CI; (2) the workflows could pin
# DIFFERENT majors from each other and still satisfy a permissive engines range. This Check
# closes both: the `.nvmrc` major must equal the node-version pinned across ALL workflows,
# and those pins must be mutually equal (a single shared major). Python-only workflows (no
# node-version) contribute nothing and are correctly ignored.
_nvmrc106 = ROOT / ".nvmrc"
_wfdir106 = ROOT / ".github" / "workflows"
if _nvmrc106.exists() and _wfdir106.exists():
    _nvm_major106 = _nvmrc106.read_text(encoding="utf-8").strip().lstrip("v").split(".")[0]
    _wf_majors106 = set()
    for _wf106 in sorted(_wfdir106.glob("*.yml")):
        for _m106 in re.finditer(r"node-version:\s*['\"]?(\d+)", _wf106.read_text(encoding="utf-8")):
            _wf_majors106.add(_m106.group(1))
    check(
        bool(_nvm_major106) and _wf_majors106 == {_nvm_major106},
        f"Check 106: .nvmrc (Node {_nvm_major106}) matches all CI workflow node-version pins ({sorted(_wf_majors106)})",
        f"Check 106: .nvmrc Node major {_nvm_major106!r} != CI workflow node-version pin major(s) {sorted(_wf_majors106)}. "
        "ローカル dev 契約 (.nvmrc) と全 workflow の node-version pin を単一 major に揃えよ "
        "(Check 69 は engines が pin を許容するかのみを見る)",
        blocking=True,
    )
else:
    check(False, "", "Check 106: .nvmrc or workflows dir not found — node alignment を検証できない", blocking=True)

# ── 107. total-check-runbook.md §11 CI-workflow inventory bijection (BLOCKING) ─
# total-check-runbook.md §11 "CI workflows overview" is the human-facing index of what runs in
# GitHub Actions and when. Like Check 75 (incident README inventory) and Check 105 (check-map),
# a hand-maintained inventory silently drifts when a workflow file is added or removed but the
# table is not updated. We slice §11 from the runbook and extract the backtick-quoted `*.yml`
# filenames it names (backtick-anchored so the `docs/files/.../<name>.yml.md` reference inside
# the section is NOT mistaken for a workflow), then require that set to equal the real
# .github/workflows/*.yml files on disk — so the CI overview can never fall behind reality.
_runbook107 = ROOT / "docs" / "architecture" / "total-check-runbook.md"
_wfdir107 = ROOT / ".github" / "workflows"
if _runbook107.exists() and _wfdir107.exists():
    _disk_wf107 = {p.name for p in _wfdir107.glob("*.yml")}
    _sec107 = re.search(r"^## 11\..*?(?=^## |\Z)", _runbook107.read_text(encoding="utf-8"), re.MULTILINE | re.DOTALL)
    _doc_wf107 = set(re.findall(r"`([\w-]+\.yml)`", _sec107.group(0))) if _sec107 else set()
    _only_disk107 = sorted(_disk_wf107 - _doc_wf107)
    _only_doc107 = sorted(_doc_wf107 - _disk_wf107)
    check(
        bool(_sec107) and _disk_wf107 == _doc_wf107,
        f"Check 107: total-check-runbook.md §11 documents exactly the {len(_disk_wf107)} CI workflows (doc ↔ .github/workflows bijection)",
        f"Check 107: CI workflow overview drift — on disk but missing from §11: {_only_disk107}; "
        f"in §11 but not on disk: {_only_doc107}. runbook §11 の workflow 一覧を同期せよ"
        + ("" if _sec107 else "（§11 セクションが見つからない）"),
        blocking=True,
    )
else:
    check(False, "", "Check 107: runbook or workflows dir not found — workflow inventory を検証できない", blocking=True)

# ── 108. docs/files mirror ↔ tracked-files full bijection (BLOCKING) ──────────
# The repo documents EVERY tracked file with a 1-to-1 mirror at docs/files/<path>.md
# (multi-audience: AI / new hire / auditor / recruiter / researcher). Check 96 only enforces
# the 33 Phase-1 shipped-code files, leaving the other ~100 mirrors unguarded: a new file added
# without a mirror, or an orphan mirror left after a source file is deleted/renamed, would erode
# the "every file is documented" guarantee silently. This Check extends the bijection to the
# FULL tracked set. Authoritative source = `git ls-files` via the already-computed `_member_paths`
# (so untracked node_modules/__pycache__ never false-positive). README.md (the inventory, Check
# 99) and _template.md are the only docs/files entries that are not themselves mirrors.
_src108 = {f for f in _member_paths if not f.startswith("docs/files/")}
_mirror108 = set()
for _f108 in _member_paths:
    if _f108.startswith("docs/files/") and _f108.endswith(".md"):
        if _f108.rsplit("/", 1)[-1] in ("README.md", "_template.md"):
            continue
        _mirror108.add(_f108[len("docs/files/"):-len(".md")])
_missing_mirror108 = sorted(_src108 - _mirror108)
_orphan_mirror108 = sorted(_mirror108 - _src108)
check(
    bool(_src108) and _src108 == _mirror108,
    f"Check 108: all {len(_src108)} tracked files have a 1-to-1 docs/files mirror (full bijection)",
    f"Check 108: docs/files mirror drift — tracked but undocumented (missing mirror): {_missing_mirror108}; "
    f"orphan mirror (doc with no source file): {_orphan_mirror108}. docs/files/<path>.md を同期せよ",
    blocking=True,
)

# ── 109. living-doc Check-count hardcode drift guard (BLOCKING) ────────────────
# stale な「現在の Check 総数」を prose にハードコードする drift class を構造的に封じる。この
# drift は PR #68 が runbook/map を drift-proof 化した後も再発し、皮肉にも PR #68 自身が §11 に
# 新たな stale 値を混入させていた（後続増分で実態へ修正）。手動の drift-proof 化では漏れが構造的に
# 生じるため、機械強制で「§9 以外の living 文書に現在総数の数値ハードコードを書けない」ことを保証
# する。正確な総数は §9（Check 70 が強制）を単一権威とし、他所はすべて §9 への pointer に置換する。
# 走査対象は「現在状態を語る」orientation/governance 文書のみ。歴史層（improvement-notes /
# decision / Session Record / docs/files ミラー）は point-in-time 記録ゆえ対象外。runbook は §9
# （生の総数が正本として住む唯一の zone）を除外して走査する。
# NOTE: 本 Check 実装ファイル自身は走査対象に含めない（下記 regex 文字列が自己発火しないため）。
# 走査対象 = 現在状態を語る living orientation/governance 文書の全面。意図的に除外するもの:
# (1) runbook §9 zone（生タリーの正本・下で個別除外）、(2) 歴史層 = per-increment changelog や
# engineering log（repository-maintainability-map.md / main-js-extraction-map.md は「Check 総数
# 42→43」等の point-in-time 記録を正当に保持するため対象外。Session Record / improvement-notes /
# decision / docs/files ミラーも同様）。新たに living 文書を足したらここへ追加する。
_living109 = [
    ".claude/CLAUDE.md",
    ".claude/README.md",
    "CLAUDE.md",
    "CHANGELOG.md",
    "Claude2Claude.md",
    "README.md",
    "docs/architecture/total-check-runbook.md",
    "docs/architecture/check-repository-consistency-map.md",
]
for _glob109 in (".claude/agents/*.md", ".claude/skills/*/SKILL.md", ".claude/commands/*.md"):
    _living109 += [str(p.relative_to(ROOT)) for p in sorted(ROOT.glob(_glob109))]
_forbidden109 = [
    (re.compile(r"総数\s*[=＝]\s*\d+"), "総数 = N"),
    (re.compile(r"総数\s*[はが]\s*\d+\s*(?:まで|に|へ)"), "総数は N まで"),
    (re.compile(r"\ball\s+\d+\s+[Cc]hecks\b"), "all N Checks"),
    (re.compile(r"consistency\s+\d+\s+[Cc]heck\b"), "consistency N Check"),
    (re.compile(r"[Cc]heck\s+count\**\s*[:：]\s*\**\d+"), "Check count: N"),
]
_hits109 = []
for _rel109 in _living109:
    _fp109 = ROOT / _rel109
    if not _fp109.exists():
        continue
    _txt109 = _fp109.read_text(encoding="utf-8")
    # runbook §9 は生の総数が正本として住む authority zone ゆえ走査から除外（§10/§11 は走査する）。
    if _rel109.endswith("total-check-runbook.md"):
        _txt109 = re.sub(r"^## 9\..*?(?=^## )", "", _txt109, flags=re.MULTILINE | re.DOTALL)
    for _rx109, _name109 in _forbidden109:
        for _m109 in _rx109.finditer(_txt109):
            _ln109 = _txt109[: _m109.start()].count("\n") + 1
            _hits109.append(f"{_rel109}:{_ln109} [{_name109}] {_m109.group(0)!r}")
check(
    not _hits109,
    f"Check 109: no stale Check-count hardcode in {len(_living109)} living docs (§9 is the single authority)",
    "Check 109: stale Check-count hardcode(s) in living docs — " + "; ".join(_hits109)
    + ". 数値を除去し「正値は total-check-runbook.md §9 (Check 70 強制)」への pointer へ phrasing せよ",
    blocking=True,
)

# ── 110. e2e A11Y_ROUTES ↔ ALL_ROUTES coverage bijection (BLOCKING) ────────────
# axe a11y テスト (A11Y_ROUTES でループ) は render-neutral critical 違反ゼロを全ルートで機械強制
# するが、その対象集合 A11Y_ROUTES が手動配列ゆえ、新ルートを ALL_ROUTES (route-render が網羅) に
# 足したのに A11Y_ROUTES へ足し忘れると「新ルートが a11y 未検証」の silent coverage gap が生じる。
# 両配列の hash 集合が一致することを機械強制し、a11y カバレッジが shipped route 集合を常に追従する
# ことを保証する (Check 58 の e2e↔main.js route 版の a11y 面)。
_spec110 = ROOT / "e2e" / "portfolio.spec.js"
if _spec110.exists():
    _src110 = _spec110.read_text(encoding="utf-8")
    _a11y_m110 = re.search(r"const A11Y_ROUTES\s*=\s*\[(.*?)\]", _src110, re.DOTALL)
    _all_m110 = re.search(r"const ALL_ROUTES\s*=\s*\[(.*?)\];", _src110, re.DOTALL)
    _a11y_set110 = set(re.findall(r"'([^']+)'", _a11y_m110.group(1))) if _a11y_m110 else set()
    _all_set110 = set(re.findall(r"hash:\s*'([^']+)'", _all_m110.group(1))) if _all_m110 else set()
    _only_all110 = sorted(_all_set110 - _a11y_set110)
    _only_a11y110 = sorted(_a11y_set110 - _all_set110)
    check(
        bool(_a11y_set110) and bool(_all_set110) and _a11y_set110 == _all_set110,
        f"Check 110: e2e A11Y_ROUTES ({len(_a11y_set110)}) covers exactly the ALL_ROUTES hash set ({len(_all_set110)}) — a11y axe runs on every shipped route",
        f"Check 110: a11y coverage drift — in ALL_ROUTES but missing from A11Y_ROUTES (a11y 未検証ルート): "
        f"{_only_all110}; in A11Y_ROUTES but not ALL_ROUTES: {_only_a11y110}. e2e の A11Y_ROUTES を同期せよ",
        blocking=True,
    )
else:
    check(False, "", "Check 110: e2e/portfolio.spec.js not found — a11y coverage bijection を検証できない", blocking=True)

# ── 111. e2e no-networkidle guard (BLOCKING) ──────────────────────────────────
# `waitForLoadState('networkidle')` は全ネット通信が 500ms 落ち着くのを待つが、本サイトは外部
# Google Fonts と service worker の SWR background fetch を持つため、CI のネット遅延窓では idle に
# 到達せず 30s test-timeout までハングする (PR #132 で repo 全体を root-fix した hang flake クラス)。
# behavior テストは 'domcontentloaded' + expect() の auto-wait で同期すべきで、networkidle が正当
# なのは screenshot capture (フォント/画像ロードの決定化が必要) のみ。本 Check は screenshot テスト
# 以外での networkidle 再導入を pre-commit でブロックし flake クラスの再発を構造的に封じる。
# 許容判定: networkidle 行の直後数行以内に toHaveScreenshot があれば screenshot テスト内とみなす。
_spec111 = ROOT / "e2e" / "portfolio.spec.js"
if _spec111.exists():
    _lines111 = _spec111.read_text(encoding="utf-8").splitlines()
    _viol111 = []
    for _i111, _line111 in enumerate(_lines111):
        if "waitForLoadState('networkidle')" in _line111 or 'waitForLoadState("networkidle")' in _line111:
            _window111 = "\n".join(_lines111[_i111:_i111 + 6])
            if "toHaveScreenshot" not in _window111:
                _viol111.append(_i111 + 1)
    check(
        not _viol111,
        "Check 111: e2e/portfolio.spec.js uses waitForLoadState('networkidle') only in the screenshot regression test",
        f"Check 111: e2e/portfolio.spec.js: waitForLoadState('networkidle') が screenshot テスト外の line {_viol111} に存在 — "
        f"'domcontentloaded' + expect() auto-wait を使え (networkidle は外部 Fonts/SW で CI hang する。PR #132 参照)",
        blocking=True,
    )
else:
    check(False, "", "Check 111: e2e/portfolio.spec.js not found — networkidle guard を検証できない", blocking=True)

# ── 112. Shipped-JS IME composition guard (BLOCKING) ──────────────────────────
# Enter ハンドラは IME 変換確定の Enter (e.isComposing) で submit/遷移してはならない。日本語入力で
# 変換候補を Enter 確定した際に未確定テキストが誤って追加/送信されたり画面遷移する footgun を防ぐ。
# 112a (精密): js/apps.js の task/todo/ai 入力は `e.key === 'Enter'` を判定する行に必ず composition
#   ガード ('Composing' = e.isComposing または手動 todoComposing) を同一行に併記する (task=PR #151 /
#   ai=PR #152 で修正・todo は既存対応)。
# 112b (一般網): apps.js 以外も含む全 shipped JS module で、`e.key === 'Enter'` を判定する file は
#   同 file 内で IME composition ガード (isComposing/Composing) を参照していなければならない。
#   command-palette の keydown trap のように apps.js 外で日本語検索 + Enter が遷移を誤発火する同クラスの
#   footgun を構造的に捕捉する (本 Check 拡張時に command-palette.js の未ガード Enter を発見・修正)。
_apps112 = ROOT / "js" / "apps.js"
if _apps112.exists():
    _lines112 = _apps112.read_text(encoding="utf-8").splitlines()
    _enter112 = 0
    _viol112 = []
    for _i112, _line112 in enumerate(_lines112):
        if "e.key === 'Enter'" in _line112 or 'e.key === "Enter"' in _line112:
            _enter112 += 1
            if "Composing" not in _line112:
                _viol112.append(_i112 + 1)
    check(
        # 両側非空ガード: Enter ハンドラが 1 つも見つからない (構造変更/gutting) 場合に vacuous pass
        # するのを防ぐ。task/todo/ai の 3 入力があるため Enter ハンドラは常に存在するはず。
        _enter112 > 0 and not _viol112,
        f"Check 112a: js/apps.js — {_enter112} 個の Enter-submit ハンドラすべてが IME composition ガードを持つ",
        f"Check 112a: js/apps.js: IME composition ガード無しの Enter-submit が line {_viol112} に存在 — "
        f"`&& !e.isComposing` を追加せよ (日本語 IME 変換確定の誤 submit を防ぐ。PR #151/#152 参照)"
        if _viol112 else
        "Check 112a: js/apps.js に Enter-submit ハンドラが見つからない (構造変更の可能性) — IME guard 検証が無効化された",
        blocking=True,
    )
else:
    check(False, "", "Check 112a: js/apps.js not found — IME composition guard を検証できない", blocking=True)
# 112b — 全 shipped JS module 横断の一般網: Enter ハンドラを持つ file は IME ガードを参照すること。
_js_files112 = sorted((ROOT / "js").rglob("*.js"))
_enter_unguarded112 = []
_enter_files112 = 0
for _f112 in _js_files112:
    _txt112 = _f112.read_text(encoding="utf-8")
    if "e.key === 'Enter'" in _txt112 or 'e.key === "Enter"' in _txt112:
        _enter_files112 += 1
        if "isComposing" not in _txt112 and "Composing" not in _txt112:
            _enter_unguarded112.append(str(_f112.relative_to(ROOT)))
check(
    _enter_files112 > 0 and not _enter_unguarded112,
    f"Check 112b: Enter ハンドラを持つ {_enter_files112} 個の shipped JS module すべてが IME composition ガードを参照",
    f"Check 112b: IME composition ガードを参照しない Enter ハンドラ module: {_enter_unguarded112} — "
    f"`e.isComposing` ガードを追加せよ (日本語 IME 変換確定の誤 submit/遷移を防ぐ)"
    if _enter_unguarded112 else
    "Check 112b: Enter ハンドラを持つ shipped JS module が 1 つも無い (構造変更の可能性) — IME guard 一般網が無効化された",
    blocking=True,
)

# ── 113. commit/PR handoff discipline presence in canon (BLOCKING) ────────────
# 「AI は交換可能なメンバ」軸の核 = AI→AI 引き継ぎ。commit/PR 規律 (fine commit ×厚い what+why ×
# テーマ束ね PR ×rebase-merge ×commit 数は OUTPUT) はオーナーが「リポジトリの核」として正式採用し、
# model-agnostic 正典 AI2AI.md (STEP 5.5) と Claude 固有 router CLAUDE.md (§5) の双方に置かれる永続
# ルール。どちらかから silent に消えると新 AI が squash/粗 commit に退行し handoff 情報が失われるため、
# 両ドキュメントに rebase + no-padding 条項のマーカーが存在することを機械強制し drift を防ぐ。
_disc113_files = [("CLAUDE.md", ROOT / "CLAUDE.md"), ("AI2AI.md", ROOT / "AI2AI.md")]
_markers113 = [
    "gh pr merge --rebase",   # commit を main に保持する merge 方式
    "OUTPUT であって TARGET",   # padding 禁止条項 (数を目的化しない)
]
_miss113 = []
for _label113, _path113 in _disc113_files:
    if not _path113.exists():
        _miss113.append(f"{_label113}:NOTFOUND")
        continue
    _src113 = _path113.read_text(encoding="utf-8")
    for _m113 in _markers113:
        if _m113 not in _src113:
            _miss113.append(f"{_label113}:{_m113}")
check(
    not _miss113,
    "Check 113: CLAUDE.md と AI2AI.md の双方が handoff-first commit/PR 規律 (rebase + no-padding) を保持",
    f"Check 113: commit/PR 規律マーカー欠落: {_miss113} — CLAUDE.md §5 / AI2AI.md STEP 5.5 の規律を復元せよ",
    blocking=True,
)

# ── 114. e2e no-`.only` guard (BLOCKING) ──────────────────────────────────────
# Playwright で test.only / describe.only が 1 つでも残ると、その test だけが走り他は全 skip され、
# CI は緑のまま suite が空洞化する (false-green footgun = vacuous-gate の裏返し)。spec 内の
# `(test|describe).only(` を検出して BLOCKING で禁止し、デバッグ用 .only の commit 漏れを封じる。
_spec114 = ROOT / "e2e" / "portfolio.spec.js"
if _spec114.exists():
    _src114 = _spec114.read_text(encoding="utf-8")
    _only114 = re.findall(r"\b(?:test|describe)(?:\.[A-Za-z]+)*\.only\s*\(", _src114)
    check(
        not _only114,
        "Check 114: e2e/portfolio.spec.js に test.only/describe.only が無い (false-green footgun 防止)",
        f"Check 114: e2e/portfolio.spec.js に .only が {len(_only114)} 個ある — 全 suite が skip され CI が false-green 化する。.only を除去せよ",
        blocking=True,
    )
else:
    check(False, "", "Check 114: e2e/portfolio.spec.js not found — no-.only guard を検証できない", blocking=True)

# ── 115. index.html CSP hardening baseline (BLOCKING) ─────────────────────────
# CSP の弱体化 (script-src への 'unsafe-inline'/'unsafe-eval' 混入や必須 directive の欠落) は XSS
# 防御を無効化する高影響のセキュリティ退行。本サイトは inline を sha256 hash + 'unsafe-hashes' で
# 許可しており blanket 'unsafe-inline' は使わない。CSP meta の content を抽出し、危険トークン不在 +
# 必須 directive 存在を BLOCKING で機械強制する (Check 7 の position/hash に対する runtime-policy 面)。
# 必須 directive には Trusted Types の 2 つ (require-trusted-types-for 'script' / trusted-types default)
# を含む: これらは main.js の trustedTypes.createPolicy('default') (Check 43c が存在を強制) と「対に
# なって機能する」security 不変条件で、(a) require-trusted-types-for が消えると innerHTML interceptor の
# fail-closed 保護がブラウザ非強制化して XSS 防御が弱体化し、(b) trusted-types の許可名から 'default' が
# 外れると createPolicy('default') が CSP にブロックされ app 自体が起動失敗する。main.js 側 (43c) のみ
# 強制し CSP 側を放置すると pairing が片肺になるため、ここで CSP 側も BLOCKING で固定する。
# さらに form-action 'none' (本サイトに HTML form は無く明示ブロック=フォーム exfiltration 遮断) と
# upgrade-insecure-requests (HTTP downgrade / mixed-content 遮断) も必須化する: いずれも除去が常に
# security weakening でゼロ legitimate-removal シナリオのため anti-weakening baseline に含める。
_csp_m115 = re.search(r'http-equiv="Content-Security-Policy"\s+content="(.*?)"', html, re.DOTALL)
if _csp_m115:
    _csp115 = _csp_m115.group(1)
    _problems115 = []
    if "'unsafe-inline'" in _csp115:
        _problems115.append("'unsafe-inline' が存在 (XSS 防御を無効化)")
    if "'unsafe-eval'" in _csp115:
        _problems115.append("'unsafe-eval' が存在")
    for _req115 in [
        "default-src 'self'", "object-src 'none'", "base-uri 'self'",
        "require-trusted-types-for 'script'", "trusted-types default",
        "form-action 'none'", "upgrade-insecure-requests",
    ]:
        if _req115 not in _csp115:
            _problems115.append(f"必須 directive 欠落: {_req115}")
    check(
        not _problems115,
        "Check 115: index.html CSP がセキュリティ baseline を維持 (unsafe-inline/eval 無し + 必須 directive 存在)",
        f"Check 115: CSP 弱体化を検出: {_problems115} — XSS 防御 baseline を復元せよ",
        blocking=True,
    )
else:
    check(False, "", "Check 115: index.html に Content-Security-Policy meta が見つからない — CSP baseline を検証できない", blocking=True)

# ── 116. playwright.config.cjs reuseExistingServer=false (BLOCKING) ────────────
# reuseExistingServer:true だと既に起動中の dev server を再利用し、commit 前の stale 状態を検証して
# CI が緑になる false-green vector。`reuseExistingServer: false` の存在 + `: true` の不在を機械強制。
_pwcfg = ROOT / "playwright.config.cjs"
_pwsrc = _pwcfg.read_text(encoding="utf-8") if _pwcfg.exists() else ""
if _pwcfg.exists():
    _reuse_ok = bool(re.search(r"reuseExistingServer\s*:\s*false\b", _pwsrc)) and \
        not re.search(r"reuseExistingServer\s*:\s*true\b", _pwsrc)
    check(
        _reuse_ok,
        "Check 116: playwright.config.cjs reuseExistingServer が false (stale-server false-green 防止)",
        "Check 116: playwright.config.cjs の reuseExistingServer が false でない — 既存 server 再利用で stale 状態を検証し false-green 化する。false に戻せ",
        blocking=True,
    )
else:
    check(False, "", "Check 116: playwright.config.cjs not found — webServer 設定を検証できない", blocking=True)

# ── 117. playwright.config.cjs screenshot tolerance sanity ceiling (BLOCKING) ──
# maxDiffPixelRatio を緩めすぎると §3 baseline ゲートが本物の視覚 regression を見逃す。<=0.05 を強制。
if _pwcfg.exists():
    _mdpr = re.search(r"maxDiffPixelRatio\s*:\s*([0-9.]+)", _pwsrc)
    _mdpr_val = float(_mdpr.group(1)) if _mdpr else None
    check(
        _mdpr_val is not None and _mdpr_val <= 0.05,
        f"Check 117: playwright.config.cjs maxDiffPixelRatio={_mdpr_val} <= 0.05 (§3 baseline 感度を維持)",
        f"Check 117: maxDiffPixelRatio={_mdpr_val} が sanity ceiling 0.05 を超過 (or 未設定) — 緩めると視覚 regression を見逃す。締め直せ",
        blocking=True,
    )
else:
    check(False, "", "Check 117: playwright.config.cjs not found — screenshot tolerance を検証できない", blocking=True)

# ── 118. PAGE_META route coverage (BLOCKING) ──────────────────────────────────
# 全 shipped route が js/page-meta.js の PAGE_META に metadata を持つことを保証する。route が
# PAGE_META に無いと applyMeta が early-return し title/desc/JSON-LD が出ない silent AIO/SEO gap に
# なる。shipped route 集合は e2e の ALL_ROUTES (Check 58 が main.js と結ぶ curated 権威) の name を
# 正規化して用い、PAGE_META keys が全 route を網羅する (⊇) ことを機械強制する。
_pm118 = ROOT / "js" / "page-meta.js"
_spec118 = ROOT / "e2e" / "portfolio.spec.js"
if _pm118.exists() and _spec118.exists():
    _pmsrc118 = _pm118.read_text(encoding="utf-8")
    _pmkeys118 = set(re.findall(r"^\s*'?([a-z][a-z0-9-]*)'?\s*:\s*\{", _pmsrc118, re.MULTILINE))
    _ssrc118 = _spec118.read_text(encoding="utf-8")
    _allm118 = re.search(r"const ALL_ROUTES\s*=\s*\[(.*?)\];", _ssrc118, re.DOTALL)
    _names118 = set(re.findall(r"name:\s*'([^']+)'", _allm118.group(1))) if _allm118 else set()
    _alias118 = {"not-found-fallback": "not-found"}
    _norm118 = {_alias118.get(n, n) for n in _names118}
    _missing118 = sorted(_norm118 - _pmkeys118)
    check(
        bool(_pmkeys118) and bool(_norm118) and not _missing118,
        f"Check 118: PAGE_META が全 {len(_norm118)} shipped route の metadata を網羅 (route 毎 AIO/SEO)",
        f"Check 118: PAGE_META に metadata 欠落の route: {_missing118} — applyMeta が early-return し title/desc/JSON-LD が出ない。js/page-meta.js に追加せよ",
        blocking=True,
    )
else:
    check(False, "", "Check 118: js/page-meta.js または e2e/portfolio.spec.js が見つからない — PAGE_META 網羅を検証できない", blocking=True)

# ── 119. factory docstring dependency coherence (BLOCKING) ────────────────────
# 各葉モジュールの factory `createX({ ...deps })` が引数で受け取る依存名のすべてが、その
# ファイル冒頭 docstring の【依存（引数で注入）】節に列挙されていることを機械強制する。これは
# Session #20 で手修正した factory docstring の依存 drift (aidk-rails に Theme/BGM/secureExternalLinks/
# openDrawer/closeDrawer、apps に Storage、components に tokenize/CONSTANTS/clear/closeDrawer、pages に
# ContactCTA が署名にあるのに docstring から欠落していた) の class を再発防止するもの。docstring は
# 次の AI の onboarding substrate（低 onboarding コスト = トークン持続性の柱）であり、署名と docstring
# の乖離は次の AI に誤った依存契約を読ませる onboarding 税＝flywheel 劣化要因。署名から派生して照合する
# ことで「依存を増やしたのに docstring 更新を忘れた」drift を pre-commit で BLOCKING 検出する。
# 照合は dep 名を word-boundary で 【依存】節テキストに探す (単一文字 dep `h` の部分一致誤検出を回避)。
_dep_problems119 = []
_checked119 = 0
for _facfile119 in sorted((ROOT / "js").glob("*.js")):
    _facsrc119 = _facfile119.read_text(encoding="utf-8")
    _facm119 = re.search(r"export function create\w+\(\{\s*([^}]*?)\}\)", _facsrc119)
    if not _facm119:
        continue  # 依存注入 factory でないファイル (純データ等) は対象外
    _checked119 += 1
    _deps119 = [d.strip() for d in _facm119.group(1).replace("\n", " ").split(",") if d.strip()]
    _secm119 = re.search(r"【依存[^】]*】(.*?)(?:【|\*/)", _facsrc119, re.DOTALL)
    _sectext119 = _secm119.group(1) if _secm119 else ""
    _miss119 = [d for d in _deps119
                if not re.search(r"(?<![\w$])" + re.escape(d) + r"(?![\w$])", _sectext119)]
    if _miss119:
        _dep_problems119.append(f"{_facfile119.name}: docstring【依存】節に欠落 {_miss119}")
check(
    not _dep_problems119,
    f"Check 119: 全 {_checked119} factory の docstring【依存】節が署名の注入依存を網羅 (onboarding 精度 / flywheel 保護)",
    "Check 119: factory 署名の依存が docstring【依存】節に欠落 (依存契約 drift): "
    + "; ".join(_dep_problems119)
    + " — 署名に dep を足したら同ファイルの【依存（引数で注入）】節にも追記せよ",
    blocking=True,
)

# ── 120. shipped JS+CSS byte-weight budget (BLOCKING) ─────────────────────────
# ブラウザが download/parse する shipped payload (main.js + js/**/*.js + style.css) の合計バイト数が
# file-size-budget.md の PERF-BUDGET-DATA ceiling 以下であることを機械強制する。§3(B) で screenshot を
# advisory 化し pixel ゲートを外したため、別軸の実 page-weight 保護が薄くなった。これを byte-weight で
# 補う。行数予算 (Check 52) とは別軸 (byte ≠ line) で、実 download/parse 負荷 (LCP/CWV に影響) を守り、
# 巨大ファイル誤コミット等の runaway bloat を BLOCKING 捕捉する。ceiling は ESLint baseline 同様、正当な
# 機能成長で超えたら rationale 付きでラチェット更新する運用 (PERF-BUDGET-DATA コメントに記録)。
_budget120 = ROOT / "docs" / "architecture" / "file-size-budget.md"
_perf_m120 = re.search(r"<!--\s*PERF-BUDGET-DATA\s+(\d+)\s+-->", _budget120.read_text(encoding="utf-8")) if _budget120.exists() else None
if _perf_m120:
    _ceiling120 = int(_perf_m120.group(1))
    _shipped120 = 0
    _files120 = [ROOT / "main.js", ROOT / "style.css"] + sorted((ROOT / "js").rglob("*.js"))
    for _f120 in _files120:
        if _f120.exists():
            _shipped120 += len(_f120.read_bytes())
    check(
        _shipped120 <= _ceiling120,
        f"Check 120: shipped JS+CSS byte-weight {_shipped120} <= budget {_ceiling120} (page-weight / CWV 保護)",
        f"Check 120: shipped JS+CSS byte-weight {_shipped120} が budget {_ceiling120} を超過 — "
        f"runaway bloat か正当な機能成長かを判断し、後者なら file-size-budget.md の PERF-BUDGET-DATA を "
        f"rationale 付きでラチェット更新せよ (byte ≠ line ゆえ Check 52 とは別軸の page-weight 保護)",
        blocking=True,
    )
else:
    check(
        False,
        "Check 120: file-size-budget.md PERF-BUDGET-DATA marker present",
        "Check 120: file-size-budget.md に `<!-- PERF-BUDGET-DATA <N> -->` が無い — "
        "shipped JS+CSS の page-weight 保護が消失。marker を追加せよ",
        blocking=True,
    )

# ── 121. STATUS.md freshness (regenerate-and-compare) (BLOCKING) ──────────────
# owner-facing STATUS.md (スマホ用 BLUF) は generate_status.py が authoritative ソース
# (AI2AI.md の Pipeline-Version / 最新 Session Record # 等) から機械生成する。手で書くと drift し、
# stale な dashboard は誤情報＝onboarding 税で flywheel を劣化させる。本 Check は generator を import
# して build_status() を再生成し、commit 済み STATUS.md と byte 一致することを BLOCKING で検証する
# (AIO digest checks と同じ regenerate-compare 思想)。authoritative 値が変わったのに STATUS.md を
# 再生成し忘れた drift を pre-commit で捕捉する。修正は `npm run status`。
_status121 = ROOT / "STATUS.md"
try:
    import generate_status as _gs121  # co-located in .github/scripts (sys.path[0] when run as script)
    _expected121 = _gs121.build_status()
    _actual121 = _status121.read_text(encoding="utf-8") if _status121.exists() else None
    check(
        _actual121 is not None and _actual121 == _expected121,
        "Check 121: STATUS.md is up to date (npm run status reproduces identical content)",
        "Check 121: STATUS.md が stale または欠落 — authoritative 値 (version / 最新 Session # 等) が "
        "変わったのに再生成し忘れている。`npm run status` を実行して commit せよ (owner dashboard の drift 防止)",
        blocking=True,
    )
except Exception as _e121:
    check(
        False,
        "Check 121: STATUS.md freshness verifiable",
        f"Check 121: STATUS.md 鮮度を検証できない (generate_status import 失敗等): {_e121}",
        blocking=True,
    )

# ── 122. no private source documents tracked (BLOCKING) ───────────────────────
# 本人の経歴書類 (履歴書・職務経歴書・内定通知書・労働条件表 等) は、抽象化済み evidence
# (docs/evidence/real-work-claims.md) を生成するためのローカル入力に過ぎず、原本を公開リポジトリへ
# commit すると機微情報 (氏名以外の個人特定情報・顧客名・案件名・年収・労働条件) の漏洩になる。
# shipped repo は Vanilla JS/MD/画像/JSON のみで、office/文書/アーカイブ形式は一切正規利用が無いため、
# これらの拡張子が tracked されていないことを BLOCKING で機械強制する (.gitignore のブランケット ignore と
# 二重防御。`git add .` は settings で deny 済みだが、明示 add の取りこぼしや将来の再投入もここで閉じる)。
# 対象は MS Office (pdf/docx/doc/xlsx/pptx) + 文書 (rtf/odt/ods/odp/pages/key/numbers/csv) +
# アーカイブ (zip/7z/rar/tar/gz/tgz)。画像 (png/jpg/webp) は webp asset / playwright baseline で
# 正規利用するため意図的に対象外 (false-positive 回避)。
_PRIVATE_DOC_SUFFIXES = (
    ".pdf", ".docx", ".doc", ".xlsx", ".pptx",
    ".rtf", ".odt", ".ods", ".odp", ".pages", ".key", ".numbers", ".csv",
    ".zip", ".7z", ".rar", ".tar", ".gz", ".tgz",
)
_private_hits = sorted(p for p in _member_paths if p.lower().endswith(_PRIVATE_DOC_SUFFIXES))
check(
    not _private_hits,
    f"Check 122: no private source documents (.pdf/.docx/...) tracked (scanned {len(_member_paths)} paths)",
    "Check 122: private source document(s) tracked in repository — 機微情報漏洩リスク。原本は "
    "ローカルのみで扱い、抽象化済み evidence のみ commit せよ。tracked 違反: "
    + ", ".join(_private_hits[:10]) + (" …" if len(_private_hits) > 10 else ""),
    blocking=True,
)

# ── 123. operating-model description coherence (site ↔ AIO) (BLOCKING) ─────────
# Session #21 で「対話型 Claude」記述の実態↔記述 drift を是正し、現在の運用モデル
# (構築期=対話型 → 現在=Claude Code 自律自走 + 人間は必要時に決定的に制御) をサイト
# (js/components.js ai-knowhow) と AIO 層 (llms-full.txt Dynamic AI Team Model) の双方へ
# 超正確に記述した。この修正が将来 silent に旧記述へ巻き戻る (= flywheel を劣化させる
# onboarding 税 + entity 記述の不正確化) のを防ぐため、両面が現運用モデルの marker を
# 保持することを BLOCKING で機械強制する。canon (AI2AI.md STEP 3 Operating Model) は
# Check 102a-f が別途強制しており、本 Check はその「公開 surface 版」(102b の site/AIO 面)。
_comp123 = ROOT / "js" / "components.js"
_comp123_t = _comp123.read_text(encoding="utf-8") if _comp123.exists() else ""
_site_ok123 = ("現在の運用モデル" in _comp123_t) and ("Claude Code" in _comp123_t) and ("自走" in _comp123_t)
check(
    _site_ok123,
    "Check 123a: js/components.js が現運用モデル (現在の運用モデル + Claude Code + 自走) を保持 (site↔canon coherence)",
    "Check 123a: js/components.js から現運用モデルの記述が失われた — 「対話型 Claude」だけの旧記述へ "
    "drift すると実態↔記述乖離 + entity 不正確化。'現在の運用モデル'/'Claude Code'/'自走' の marker を維持せよ "
    "(Session #21 で是正した運用モデル記述。canon は Check 102 が別途強制)",
    blocking=True,
)
_llms123 = ROOT / "llms-full.txt"
_llms123_t = _llms123.read_text(encoding="utf-8") if _llms123.exists() else ""
_aio_ok123 = ("Current Operating Model" in _llms123_t) and ("Claude Code" in _llms123_t) and ("self-driving" in _llms123_t)
check(
    _aio_ok123,
    "Check 123b: llms-full.txt が Current Operating Model (Claude Code self-driving) を保持 (AIO↔canon coherence)",
    "Check 123b: llms-full.txt から現運用モデル記述が失われた — AIO authority が旧編成のみへ drift する。"
    "'Current Operating Model'/'Claude Code'/'self-driving' の marker を維持せよ (C6 semantic・編集は要承認)",
    blocking=True,
)

# ── 124. site visible-text anonymity guard (BLOCKING) ─────────────────────────
# サイト UI は一般向けにプライバシー設計上「yuta」へ匿名化し、実名「横井雄太」は AIO/entity 層
# (sr-only / JSON-LD / meta / alt / data-entity 属性・llms-full.txt) のみで露出する二層構造を取る
# (リポジトリ=エンジニア/AI 向けで実名可・サイト視覚面=一般人向けで匿名)。Session #21 で AI が運用モデル
# section の視覚本文に実名を漏らした (即是正) ため、視覚 page renderer (components/pages/apps) において
# 実名が「属性 context (alt/data-entity/aria-/data-ai-entity)」以外の bare な h() テキスト行に出ないことを
# BLOCKING で機械強制し、視覚 UI への実名漏れ class を構造的に封じる。AIO 属性内の実名は entity 帰属の
# ため意図的に許可する。
_VIS_RENDERERS124 = ["js/components.js", "js/pages.js", "js/apps.js"]
_NAME124 = "横井雄太"
_ATTR_MARKERS124 = ("alt:", "data-entity", "data-ai-entity", "aria-")
_leak124 = []
_idleak124 = []
# UI → DISPLAY_NAME only / AIO → AUTHORITATIVE_NAME etc. (js/identity.js の明文契約)。
# 視覚 renderer が実名系の entity 定数を参照すると識別子経由で実名が視覚露出し得るため禁止。
_NAME_IDENTS124 = ("AUTHORITATIVE_NAME", "JAPANESE_NAME")
for _rel124 in _VIS_RENDERERS124:
    _f124 = ROOT / _rel124
    if not _f124.exists():
        continue
    for _i124, _line124 in enumerate(_f124.read_text(encoding="utf-8").splitlines(), 1):
        if _NAME124 in _line124 and not any(_mk in _line124 for _mk in _ATTR_MARKERS124):
            _leak124.append(f"{_rel124}:{_i124}")
        if any(_id in _line124 for _id in _NAME_IDENTS124):
            _idleak124.append(f"{_rel124}:{_i124}")
check(
    not _leak124,
    f"Check 124a: 視覚 site renderer に実名の bare テキスト漏れ無し (anonymity guard・scanned {len(_VIS_RENDERERS124)} files)",
    "Check 124a: 視覚 site テキストに実名「横井雄太」が漏れている — サイト UI は匿名 (yuta) が design。"
    "実名は alt/data-entity/aria- 等の AIO 属性 context でのみ許可。違反: " + ", ".join(_leak124[:10]),
    blocking=True,
)
check(
    not _idleak124,
    "Check 124b: 視覚 site renderer が実名系 entity 定数 (AUTHORITATIVE_NAME/JAPANESE_NAME) を参照しない (UI→DISPLAY_NAME only 契約)",
    "Check 124b: 視覚 renderer が AUTHORITATIVE_NAME/JAPANESE_NAME を参照している — 識別子経由で実名が視覚露出し得る。"
    "js/identity.js の契約どおり UI は DISPLAY_NAME のみ参照せよ (AIO 層=meta-management 等は AUTHORITATIVE_NAME 可)。違反: "
    + ", ".join(_idleak124[:10]),
    blocking=True,
)

# ── 125. no dead CONSTANTS key (BLOCKING) ─────────────────────────────────────
# Session #21 の pomodoro bug-hunt で、consumer ゼロの never-activated 定数 (POMODORO_LOCK_TTL /
# SAVE_INTERVAL) を発見・除去した。この dead-constant class の再発を機械封じするため、js/constants.js
# の各キー (top-level + LIMITS 等 nested を含む `[A-Z_]+:` 行) が、他の shipped JS から少なくとも 1 回
# 参照されることを BLOCKING で機械強制する。ALL-CAPS snake のキー名は識別性が高く誤マッチしにくい
# (コメント言及も "not dead" として保守的に許容＝over-flag より under-flag を選ぶ)。dead は除去すること。
_const125 = ROOT / "js" / "constants.js"
if _const125.exists():
    _keys125 = list(dict.fromkeys(re.findall(r'^\s+([A-Z][A-Z0-9_]*)\s*:', _const125.read_text(encoding="utf-8"), re.M)))
    _corpus125_parts = []
    for _p125 in [ROOT / "main.js", ROOT / "sw.js", ROOT / "theme-init.js"] + sorted((ROOT / "js").rglob("*.js")):
        if _p125.resolve() == _const125.resolve() or not _p125.exists():
            continue
        _corpus125_parts.append(_p125.read_text(encoding="utf-8"))
    _blob125 = "\n".join(_corpus125_parts)
    _dead125 = [k for k in _keys125 if not re.search(r'\b' + re.escape(k) + r'\b', _blob125)]
    check(
        not _dead125,
        f"Check 125: js/constants.js の全 {len(_keys125)} キーが他 shipped JS から参照される (dead-constant guard)",
        "Check 125: 未使用の CONSTANTS キー (never-activated dead 定数) を検出 — 他 shipped JS から参照が無い。"
        "除去せよ (Session #21 の POMODORO_LOCK_TTL/SAVE_INTERVAL と同 class)。違反: " + ", ".join(_dead125[:10]),
        blocking=True,
    )
else:
    check(False, "Check 125: js/constants.js present", "Check 125: js/constants.js が見つからない", blocking=True)

# ── 126. ESLint bug-catcher safety-net presence (BLOCKING) ────────────────────
# 本 config は eslint:recommended を敢えて継承せず明示列挙する方針 (非破壊性維持) のため、純粋
# bug-catcher が silent に欠落/除去されると実バグが CI を素通りする (#186: no-dupe-keys 欠落で
# quiz 重複 class バグが流出した実例)。Check 50d が no-dupe-keys 単体を守るのに加え、本 Check は
# PR #187 + #234 で追補した recommended pure bug-catcher の代表 safety-net 集合が eslint.config.mjs
# に残存することを BLOCKING で機械強制し、「安全網そのものの silent な後退」を #186 class として封じる。
_eslint126 = ROOT / "eslint.config.mjs"
if _eslint126.exists():
    _cfg126 = _eslint126.read_text(encoding="utf-8")
    _REQUIRED_BUGCATCHERS126 = [
        "no-dupe-keys", "no-import-assign", "no-unsafe-finally", "no-invalid-regexp",
        "no-const-assign", "valid-typeof", "use-isnan", "no-fallthrough", "no-cond-assign",
        "getter-return", "no-func-assign", "no-obj-calls", "no-dupe-args", "no-self-assign",
    ]
    _missing126 = [r for r in _REQUIRED_BUGCATCHERS126
                   if re.search(r"['\"]" + re.escape(r) + r"['\"]\s*:", _cfg126) is None]
    check(
        not _missing126,
        f"Check 126: eslint.config.mjs が recommended bug-catcher safety-net {len(_REQUIRED_BUGCATCHERS126)} 件を保持",
        "Check 126: eslint.config.mjs から pure bug-catcher が silent に欠落 — 安全網の後退 (#186 class: "
        "欠落ルールで実バグが CI を素通る)。次のルールを 'error' で復元せよ: " + ", ".join(_missing126),
        blocking=True,
    )
else:
    check(False, "Check 126: eslint.config.mjs present",
          "Check 126: eslint.config.mjs が見つからない — bug-catcher safety-net を検証できない", blocking=True)

# ── 127. AIO digest tool binary re-bake guard (BLOCKING) ──────────────────────
# update_aio_digests.py は WebP/MP3 の内部日付メタ (XMP/ID3) 再書き込みを、binary ファイル自体が
# 実際に編集された時のみ行わねばならない。旧実装は「source_of_truth に binary entry が存在するか」
# だけを見て毎回再書き込みを発火させ、無関係なテキスト digest (週次 aio-monitoring ログ) 更新の
# たびに binary hash を変え、その新 hash を manifest に記録する一方 aio-monitoring.yml は書き換えた
# binary を git add しないため、commit 境界で manifest 記録 sha と実バイナリ sha が毎週 desync し、
# 次 PR の BLOCKING digest gate (check_aio_digests.py) が赤化していた。本 Check は再発防止として、
# (a) _binary_edited helper の存在、(b) その helper が `git diff --quiet HEAD` で実編集を判定すること、
# (c) date 再書き込みが _binary_edited() でガードされていること、を presence で機械強制する。
_digtool127 = ROOT / ".github" / "scripts" / "update_aio_digests.py"
if _digtool127.exists():
    _src127 = _digtool127.read_text(encoding="utf-8")
    _has_helper127 = re.search(r"def\s+_binary_edited\s*\(", _src127) is not None
    _has_gitdiff127 = "git" in _src127 and "diff" in _src127 and "--quiet" in _src127 and "HEAD" in _src127
    _has_gate127 = re.search(r"if\s+_binary_edited\s*\(", _src127) is not None
    _missing127 = []
    if not _has_helper127:
        _missing127.append("_binary_edited() helper 定義")
    if not _has_gitdiff127:
        _missing127.append("`git diff --quiet HEAD` による実編集判定")
    if not _has_gate127:
        _missing127.append("date 再書き込みを `if _binary_edited(...)` でガード")
    check(
        not _missing127,
        "Check 127: update_aio_digests.py が binary 日付再書き込みを _binary_edited() (git HEAD diff) でガード",
        "Check 127: update_aio_digests.py の binary re-bake guard が後退 — manifest↔binary 毎週 desync の "
        "回帰リスク (f2335ce で根治した class)。次を復元せよ: " + ", ".join(_missing127),
        blocking=True,
    )
else:
    check(False, "Check 127: update_aio_digests.py present",
          "Check 127: update_aio_digests.py が見つからない — digest tool の binary guard を検証できない", blocking=True)

# ── 128. Command palette ↔ router app-route coherence (BLOCKING) ───────────────
# command-palette (js/command-palette.js) は「横断 quick-nav」を標榜するため、router
# (js/router.js) が route できる全 built-in app (`apps/<app>` = router の whitelist
# task/todo/pomodoro/ai/notes) に対応する `hash: 'apps/<app>'` destination を NAV に持た
# ねばならない。router に app を足して palette を更新し忘れると Cmd/Ctrl+K からその app へ
# 到達できなくなる (実際 Markdown notes app が本 Check 追加まで NAV から欠落していた)。
# router の app whitelist を source of truth として parse し、palette が silent に遅れない
# ことを機械強制する。
_router128 = ROOT / "js" / "router.js"
_palette128 = ROOT / "js" / "command-palette.js"
if _router128.exists() and _palette128.exists():
    _router_src128 = _router128.read_text(encoding="utf-8")
    _palette_src128 = _palette128.read_text(encoding="utf-8")
    # router の app whitelist: `['task', 'todo', 'pomodoro', 'ai', 'notes'].includes(app)`
    _wl_m128 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _router_src128)
    _apps128 = []
    if _wl_m128:
        _apps128 = re.findall(r"['\"]([a-z]+)['\"]", _wl_m128.group(1))
    _missing128 = [a for a in _apps128
                   if (f"apps/{a}'" not in _palette_src128 and f'apps/{a}"' not in _palette_src128)]
    check(
        bool(_apps128) and not _missing128,
        f"Check 128: command-palette NAV が router の全 {len(_apps128)} built-in app ({', '.join(_apps128)}) を網羅",
        f"Check 128: command-palette NAV に router app route が欠落: {_missing128} — "
        f"`{{ label: '...', hash: 'apps/<app>' }}` を NAV へ追加せよ (Cmd+K で到達不能になる)"
        if _apps128 else
        "Check 128: router.js の app whitelist (`[...].includes(app)`) を parse できない — coherence 検証が無効化された",
        blocking=True,
    )
else:
    check(False, "Check 128: router.js / command-palette.js present",
          "Check 128: router.js または command-palette.js が見つからない — palette↔router coherence を検証できない", blocking=True)

# ── 129. Topbar data-action button double-fire guard (BLOCKING) ────────────────
# topbar の menuBtn / themeBtnTop / bgm-btn-top は data-action を持ち AIDK ActionDelegator が
# 単一の delegated click リスナーで処理する。main.js init がこれらに直接 addEventListener('click')
# も付けると 1 クリックで二重発火する (theme が 2 段送り / drawer 二重 open で scroll 復元が先頭
# ジャンプ / BGM 二重 toggle の実バグだった)。本 Check は main.js にこれら 3 ボタンへの直接 click
# リスナー配線が無いことを presence-negative で機械強制し、ActionDelegator 単一経路契約を守る。
_main129 = ROOT / "main.js"
_TOPBAR_DELEGATED_IDS129 = ["menuBtn", "themeBtnTop", "bgm-btn-top"]
if _main129.exists():
    _src129 = _main129.read_text(encoding="utf-8")
    _viol129 = []
    for _line129 in _src129.splitlines():
        if "addEventListener('click'" in _line129 or 'addEventListener("click"' in _line129:
            for _id129 in _TOPBAR_DELEGATED_IDS129:
                if f"'{_id129}'" in _line129 or f'"{_id129}"' in _line129:
                    _viol129.append(_id129)
    check(
        not _viol129,
        "Check 129: main.js は topbar data-action ボタン (menuBtn/themeBtnTop/bgm-btn-top) に直接 click リスナーを付けていない (ActionDelegator 単一経路)",
        f"Check 129: main.js が data-action ボタンに直接 click リスナーを重複登録している: {sorted(set(_viol129))} — "
        "二重発火 (theme 2 段送り / drawer scroll 先頭ジャンプ / BGM 二重 toggle) になるため直接リスナーを撤去し "
        "data-action + ActionDelegator に一本化せよ",
        blocking=True,
    )
else:
    check(False, "Check 129: main.js present",
          "Check 129: main.js が見つからない — topbar double-fire guard を検証できない", blocking=True)

# ── 130. Live-input oninput focus-loss guard (BLOCKING) ───────────────────────
# shipped JS の `oninput:` ハンドラは State.update( を呼んではならない。State.update → notify →
# State.subscribe(render) が #content を clear して全再描画し、focused input を毎キーストローク破棄
# するため focus を失う (quiz 検索 / Markdown notes が使用不能だった実バグ)。高頻度 live-input は
# State.updateSilently( (再描画しない) で永続化し、自前で sub-DOM を更新せよ (cf. ProjectsPage
# renderGrid)。本 Check は各 oninput ハンドラ本体を brace-balance で抽出し State.update( を含むなら
# fail する (updateSilently は許可。リテラル "State.update(" は "State.updateSilently(" に一致しない)。
def _extract_handler_body130(text, start):
    _arrow = text.find("=>", start)
    _fn = text.find("function", start)
    # arrow か function、近い方を本体開始の手掛かりにする (どちらも無ければ空)
    _cands = [c for c in (_arrow, _fn) if c != -1]
    if not _cands:
        return ""
    _h = min(_cands)
    _i = text.find("{", _h)
    # arrow 単一式 (=> expr, 中括弧なし) は次の改行までを本体とみなす
    _arrow_nl = text.find("\n", _h)
    if _i == -1 or (_arrow != -1 and _i > (_arrow_nl if _arrow_nl != -1 else len(text))):
        _nl = text.find("\n", _h)
        return text[_h:_nl if _nl != -1 else len(text)]
    _depth = 0
    _j = _i
    while _j < len(text):
        if text[_j] == "{":
            _depth += 1
        elif text[_j] == "}":
            _depth -= 1
            if _depth == 0:
                return text[_i:_j + 1]
        _j += 1
    return text[_i:]
_js130 = sorted((ROOT / "js").rglob("*.js"))
_viol130 = []
_oninput_count130 = 0
for _f130 in _js130:
    _txt130 = _f130.read_text(encoding="utf-8")
    _pos130 = 0
    while True:
        _oi130 = _txt130.find("oninput", _pos130)
        if _oi130 == -1:
            break
        _pos130 = _oi130 + 7
        _oninput_count130 += 1
        _body130 = _extract_handler_body130(_txt130, _oi130)
        if "State.update(" in _body130:
            _viol130.append(str(_f130.relative_to(ROOT)))
check(
    not _viol130,
    f"Check 130: 全 {_oninput_count130} 個の oninput ハンドラが State.update( を呼ばない (live-input focus-loss 防止)",
    f"Check 130: oninput ハンドラが State.update( を呼んでおり focus-loss を起こす module: {sorted(set(_viol130))} — "
    "State.updateSilently( + sub-DOM 手動更新へ変更せよ (State.update は全再描画で focused input を破棄する)",
    blocking=True,
)

# ── 131. Service-worker decodeURIComponent guard (BLOCKING) ───────────────────
# sw.js は全 fetch を intercept し、各リクエストの pathname を normalizePath→decodeURIComponent に
# 通す。decodeURIComponent は不正な % エスケープ ('/portfolio/%' 等) で URIError を throw するため、
# ガード無しだと そうした URL リクエストで SW fetch ハンドラが uncaught error になる (全リクエストを
# 触る hot path)。本 Check は sw.js の normalizePath が decodeURIComponent を try/catch で囲むことを
# presence で機械強制する。この修正は e2e/Check ガードが無かった (service worker は e2e 困難) ため、
# 本静的 presence check がその回帰ガードになる。
_sw131 = ROOT / "sw.js"
if _sw131.exists():
    _swsrc131 = _sw131.read_text(encoding="utf-8")
    # normalizePath 関数本体を抽出 (function normalizePath(...) { ... })
    _m131 = re.search(r"function\s+normalizePath\s*\([^)]*\)\s*\{", _swsrc131)
    _ok131 = False
    if _m131:
        # 関数本体を brace-balance で抽出
        _i131 = _swsrc131.index("{", _m131.start())
        _depth131 = 0
        _body131 = ""
        for _k131 in range(_i131, len(_swsrc131)):
            _c131 = _swsrc131[_k131]
            if _c131 == "{":
                _depth131 += 1
            elif _c131 == "}":
                _depth131 -= 1
                if _depth131 == 0:
                    _body131 = _swsrc131[_i131:_k131 + 1]
                    break
        # body に decodeURIComponent があるなら try と catch も同 body 内に存在すること
        if "decodeURIComponent" in _body131:
            _ok131 = ("try" in _body131 and "catch" in _body131)
        else:
            # decodeURIComponent を使わない実装なら throw リスク無し ＝ guard 不要で OK
            _ok131 = True
    check(
        _m131 is not None and _ok131,
        "Check 131: sw.js normalizePath が decodeURIComponent を try/catch でガード (不正 % URL で SW が throw しない)",
        "Check 131: sw.js normalizePath が decodeURIComponent を try/catch で囲んでいない — 不正な % エスケープ URL "
        "('/portfolio/%') で SW fetch ハンドラが URIError を throw する (全リクエストを触る hot path)。try/catch で "
        "raw pathname へフォールバックせよ"
        if _m131 else
        "Check 131: sw.js に normalizePath 関数が見つからない (構造変更の可能性) — decodeURIComponent guard を検証できない",
        blocking=True,
    )
else:
    check(False, "Check 131: sw.js present",
          "Check 131: sw.js が見つからない — SW decodeURIComponent guard を検証できない", blocking=True)

# ── 132. AIO evidence ↔ sitemap discoverability (BLOCKING) ────────────────────
# aio-manifest.json に authoritative evidence として登録された text doc (.md/.txt/.json) は
# sitemap.xml の <loc> にも載っていなければならない。manifest は AI crawler 向けに doc を権威と
# 宣言するが、sitemap 経由で discovery する crawler は sitemap 未掲載の登録 doc に到達できない
# (silent discoverability gap。real-work-claims.md / AI2AI-archive.md が登録済なのに sitemap 欠落
# だった)。binary (.webp/.mp3) は sitemap-index 対象外ゆえ除外。「evidence 登録 ⟹ sitemap 到達可」
# を機械強制する。
_manifest132 = ROOT / ".well-known" / "aio-manifest.json"
_sitemap132 = ROOT / "sitemap.xml"
if _manifest132.exists() and _sitemap132.exists():
    _mdata132 = json.loads(_manifest132.read_text(encoding="utf-8"))
    _sitemap_src132 = _sitemap132.read_text(encoding="utf-8")
    _ev_paths132 = []
    for _sec132 in ("source_of_truth", "supporting_evidence", "observational_evidence"):
        for _e132 in _mdata132.get(_sec132, []):
            _p132 = _e132.get("path", "")
            if _p132.endswith((".md", ".txt", ".json")):
                _ev_paths132.append(_p132)
    _missing132 = [p for p in _ev_paths132 if ("/" + p + "<") not in _sitemap_src132 and ("/" + p + "\n") not in _sitemap_src132 and (p + "</loc>") not in _sitemap_src132]
    check(
        bool(_ev_paths132) and not _missing132,
        f"Check 132: aio-manifest の text evidence {len(_ev_paths132)} 件すべてが sitemap.xml に <loc> 掲載 (crawler discoverability)",
        f"Check 132: aio-manifest 登録 evidence が sitemap.xml に欠落: {_missing132} — "
        "登録済 doc は sitemap.xml にも <loc> を追加せよ (sitemap 経由 crawler が到達できない discoverability gap)"
        if _ev_paths132 else
        "Check 132: aio-manifest から text evidence path を抽出できない (manifest 構造を確認せよ)",
        blocking=True,
    )
else:
    check(False, "Check 132: aio-manifest.json / sitemap.xml present",
          "Check 132: aio-manifest.json または sitemap.xml が無い — AIO evidence↔sitemap 整合を検証できない", blocking=True)

# ── 133. AIO guard script wiring (BLOCKING) ───────────────────────────────────
# aio-guard.js は AIO asset-anchor の lifecycle monitor & self-repair 機構で、hidden な
# <div id="aio-asset-anchor"> を監視し AI の "dead code purge" 等で除去されたら復元する
# (anchor は不可視だが AIO 層に semantically critical)。この monitor は index.html が main SPA
# IIFE より前に aio-guard.js を実際に load して初めて稼働する。mirror-bijection は FILE の存在
# しか見ないため、<script src="./aio-guard.js"> タグを消しても file は残り verify は緑のまま
# monitor だけが silent に無効化される (従来は非ブロックの CI advisory だけが捕捉)。本 Check は
# index.html が aio-guard.js を script 参照することを BLOCKING 強制し、「guard file 存在 ⟹ guard
# が配線済」を invariant 化する (AIO self-repair monitor の回帰ガード)。
_index133 = ROOT / "index.html"
if _index133.exists():
    _html133 = _index133.read_text(encoding="utf-8")
    _wired133 = re.search(r'<script\b[^>]*\bsrc\s*=\s*["\']\.?/?aio-guard\.js["\']', _html133)
    check(
        bool(_wired133),
        "Check 133: index.html が aio-guard.js を <script src> 参照 (AIO self-repair monitor が配線済)",
        "Check 133: index.html に <script src=\"./aio-guard.js\"> 参照が無い — "
        "aio-guard.js (AIO asset-anchor self-repair monitor) が load されず silent に無効化される。"
        "main IIFE より前に <script src=\"./aio-guard.js\"></script> を index.html へ戻せ",
        blocking=True,
    )
else:
    check(False, "Check 133: index.html present",
          "Check 133: index.html が無い — aio-guard.js の配線を検証できない", blocking=True)

# ── 134. Root script wiring completeness (BLOCKING) ───────────────────────────
# index.html が依存する root スクリプト (theme-init.js / karte-init.js / main.js) を
# <script src> で実際に load し続けることを BLOCKING 強制する。Check 133 (aio-guard.js) と
# 同様、mirror-bijection は FILE 存在しか見ず <script> タグの残存は強制されない。タグ除去は
# silent に劣化する: theme-init.js は pre-paint FOUC ガード (除去すると未スタイル/誤テーマの
# 一瞬の flash になるが behavior e2e は検査せず、screenshot e2e は §3(B) で advisory ゆえ block
# しない)、karte-init.js は analytics を無音停止、main.js は SPA エントリポイント (除去は e2e が
# 捕捉するが静的 check でエントリ配線を明示し e2e 不在時も生存させる)。error-suppressor.js は
# inline ゆえ対象外 (Check 7/7b が inline byte-identity + CSP hash を強制)、aio-guard.js は
# Check 133 が担当。「root script file 存在 ⟹ index.html に配線済」を残る外部 root script へ
# invariant 化する。
_index134 = ROOT / "index.html"
if _index134.exists():
    _html134 = _index134.read_text(encoding="utf-8")
    _required134 = ["theme-init.js", "karte-init.js", "main.js"]
    _unwired134 = [
        _s for _s in _required134
        if not re.search(r'<script\b[^>]*\bsrc\s*=\s*["\']\.?/?' + re.escape(_s) + r'["\']', _html134)
    ]
    check(
        not _unwired134,
        f"Check 134: index.html が依存 root script {_required134} をすべて <script src> 配線 (silent degradation 防止)",
        f"Check 134: index.html に <script src> 配線が欠落: {_unwired134} — "
        "これらは除去しても file が残り verify 緑のまま silent に劣化する "
        "(theme-init.js=FOUC / karte-init.js=analytics / main.js=SPA entry)。index.html へ "
        "<script src> 参照を戻せ",
        blocking=True,
    )
else:
    check(False, "Check 134: index.html present",
          "Check 134: index.html が無い — root script の配線を検証できない", blocking=True)

# ── 135. Stylesheet wiring (BLOCKING) ─────────────────────────────────────────
# index.html がローカル stylesheet style.css を <link rel="stylesheet" href="./style.css">
# で load し続けることを BLOCKING 強制する。これは Check 133/134 と同じ「file 存在 ⟹ file 配線」
# class の中で最も影響が大きい: link を消すとサイト全体が未スタイルで描画されるが、損失は全
# gate に対し silent — behavior e2e は content presence / route しか検査せず (未スタイルでも
# テキストは存在)、screenshot e2e は §3(B) で advisory、consistency check も link を被覆して
# いなかった。style.css の存在 (Check 108 mirror) と byte 予算 (Check 52/120) は強制済だが
# <link> 配線は未強制だった。外部 font stylesheet は対象外 (除去しても fallback font へ graceful
# degradation するため)。「style.css 存在 ⟹ index.html に link 済」を invariant 化する。
_index135 = ROOT / "index.html"
if _index135.exists():
    _html135 = _index135.read_text(encoding="utf-8")
    _linked135 = re.search(
        r'<link\b[^>]*\brel\s*=\s*["\']stylesheet["\'][^>]*\bhref\s*=\s*["\']\.?/?style\.css["\']'
        r'|<link\b[^>]*\bhref\s*=\s*["\']\.?/?style\.css["\'][^>]*\brel\s*=\s*["\']stylesheet["\']',
        _html135,
    )
    check(
        bool(_linked135),
        "Check 135: index.html が style.css を <link rel=stylesheet> 配線 (unstyled site 防止)",
        "Check 135: index.html に <link rel=\"stylesheet\" href=\"./style.css\"> が無い — "
        "link を消すとサイト全体が未スタイルになるが behavior e2e は content しか見ず "
        "screenshot は advisory ゆえ silent。index.html へ stylesheet link を戻せ",
        blocking=True,
    )
else:
    check(False, "Check 135: index.html present",
          "Check 135: index.html が無い — stylesheet の配線を検証できない", blocking=True)

# ── 136. demoRoute ↔ router app whitelist coherence (BLOCKING) ─────────────────
# store.js normalizeProject() は import したプロジェクトの demoRoute を hardcode された app
# whitelist で検証し、router.js は apps/<app> ルートを自身の hardcode whitelist で解決する。
# 両者は同期している必要がある — router に app が増えた (例: A 群で notes app 追加) のに store
# 側 whitelist を更新し忘れると、その新 app を demoRoute に持つプロジェクトを import した際に
# silent に null へ落ち、デモボタンが消える (Check 128 / #139 と同じ data-fidelity loss)。両配列を
# parse し store demoRoute whitelist == router app whitelist を強制し、「router が app X を
# サポート ⟹ X は有効な demoRoute」を invariant 化する。
_router136 = ROOT / "js" / "router.js"
_store136 = ROOT / "js" / "store.js"
if _router136.exists() and _store136.exists():
    _rsrc136 = _router136.read_text(encoding="utf-8")
    _ssrc136 = _store136.read_text(encoding="utf-8")
    # router: [...].includes(app)
    _rm136 = re.search(r"\[([^\]]*)\]\.includes\(app\)", _rsrc136)
    # store: [...].includes(raw.demoRoute)
    _sm136 = re.search(r"\[([^\]]*)\]\.includes\(raw\.demoRoute\)", _ssrc136)

    def _parse_list136(_raw):
        return set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _raw or ""))

    _router_apps136 = _parse_list136(_rm136.group(1) if _rm136 else "")
    _store_apps136 = _parse_list136(_sm136.group(1) if _sm136 else "")
    _missing136 = _router_apps136 - _store_apps136
    _extra136 = _store_apps136 - _router_apps136
    check(
        bool(_router_apps136) and bool(_store_apps136) and not _missing136 and not _extra136,
        f"Check 136: store demoRoute whitelist == router app whitelist ({sorted(_router_apps136)})",
        f"Check 136: demoRoute ↔ router app whitelist drift — router のみ: {sorted(_missing136)} / "
        f"store のみ: {sorted(_extra136)}。store.js normalizeProject の demoRoute whitelist を "
        f"router.js の app whitelist と一致させよ (import 時の demoRoute silent-drop を防ぐ)"
        if (_router_apps136 and _store_apps136) else
        "Check 136: router/store の app whitelist 配列を parse できない (両ファイルの構造を確認せよ)",
        blocking=True,
    )
else:
    check(False, "Check 136: js/router.js and js/store.js present",
          "Check 136: js/router.js または js/store.js が無い — demoRoute coherence を検証できない", blocking=True)

# ── 137. router app whitelist ↔ main.js render switch coherence (BLOCKING) ──────
# router.js は `apps/<app>` を app ∈ whitelist のとき route.name=`app-<app>` に解決し、main.js の
# renderer switch がその route.name を `case 'app-<app>':` で受けて app コンポーネントを描画する。
# Check 128 (cmdk) / 136 (store) は router whitelist の「提供側」を縛るが、「消費側」の main.js switch
# は ALL_ROUTES 経由 (Check 58) でしか間接的に縛られない。ゆえに router + cmdk + store だけ更新して
# main.js/ALL_ROUTES を忘れると、全 Check 緑のまま apps/<app> が default(not-found) へ落ち silent に
# 404 化する (palette/project demo は依然その route を提示する)。router whitelist と main.js の
# `case 'app-<X>':` 集合を parse し bijection を強制し、「router が app X を route 可能 ⟹ main.js が
# app X を描画可能」を直接 invariant 化する (Check 58/118/128/136 の app-route coherence mesh に
# 欠けていた直接 edge)。
_router137 = ROOT / "js" / "router.js"
_main137 = ROOT / "main.js"
if _router137.exists() and _main137.exists():
    _rsrc137 = _router137.read_text(encoding="utf-8")
    _msrc137 = _main137.read_text(encoding="utf-8")
    _rm137 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _rsrc137)
    _router_apps137 = set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _rm137.group(1))) if _rm137 else set()
    _main_app_cases137 = set(re.findall(r"case\s+['\"]app-([a-z0-9_-]+)['\"]\s*:", _msrc137))
    _missing137 = _router_apps137 - _main_app_cases137  # router が生成するが main.js が描画不能 → silent 404
    _extra137 = _main_app_cases137 - _router_apps137     # main.js に case はあるが router が生成しない → dead case
    check(
        bool(_router_apps137) and bool(_main_app_cases137) and not _missing137 and not _extra137,
        f"Check 137: main.js の case 'app-<app>' == router app whitelist ({sorted(_router_apps137)})",
        f"Check 137: router ↔ main.js render switch drift — main.js に case 欠落 (silent 404): {sorted(_missing137)} / "
        f"main.js のみ (dead case): {sorted(_extra137)}。main.js renderer switch の `case 'app-<app>':` を "
        f"router.js の app whitelist と一致させよ (apps/<app> の silent not-found を防ぐ)"
        if (_router_apps137 and _main_app_cases137) else
        "Check 137: router.js の app whitelist (`[...].includes(app)`) または main.js の `case 'app-<X>':` を parse できない",
        blocking=True,
    )
else:
    check(False, "Check 137: js/router.js and main.js present",
          "Check 137: js/router.js または main.js が無い — router↔switch coherence を検証できない", blocking=True)

# ── 138. Sidebar app-nav ↔ router app whitelist coverage (BLOCKING) ────────────
# Sidebar (js/components.js) の lab-nav は built-in app を `path: 'apps/<app>'` の quick-nav
# リンクとして列挙し、AppsPage は全 app をカードで列挙する。command palette (Check 128) と同様、
# sidebar も router が route 可能な全 app を被覆すべきである。A 群で Markdown notes app を追加した際、
# AppsPage と palette (#257) には足したが sidebar には足し忘れ、notes だけが常設左ナビから到達不能
# だった。router whitelist と sidebar の `path: 'apps/<app>'` エントリを parse し、router の全 app が
# sidebar に出ることを強制し「router が app X を route 可能 ⟹ X は sidebar nav にある」を invariant
# 化する (Check 128 の sidebar 版)。
_router138 = ROOT / "js" / "router.js"
_comp138 = ROOT / "js" / "components.js"
if _router138.exists() and _comp138.exists():
    _rsrc138 = _router138.read_text(encoding="utf-8")
    _csrc138 = _comp138.read_text(encoding="utf-8")
    _rm138 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _rsrc138)
    _router_apps138 = set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _rm138.group(1))) if _rm138 else set()
    # sidebar の quick-nav リンクは `path: 'apps/<app>'` リテラル (AppsPage は `apps/${id}` テンプレ
    # ゆえ非該当)。apps index ('apps' 単体) は app ではないので slash 付きのみ抽出。
    _sidebar_apps138 = set(re.findall(r"path:\s*['\"]apps/([a-z0-9_-]+)['\"]", _csrc138))
    _missing138 = _router_apps138 - _sidebar_apps138
    check(
        bool(_router_apps138) and not _missing138,
        f"Check 138: sidebar nav が router の全 app を被覆 ({sorted(_router_apps138)})",
        f"Check 138: sidebar app-nav に router app route が欠落: {sorted(_missing138)} — "
        f"js/components.js の Sidebar labItems に `{{ ..., path: 'apps/<app>', ... }}` を追加せよ "
        f"(常設左ナビから到達不能になる・#257 と同 class)"
        if _router_apps138 else
        "Check 138: router.js の app whitelist (`[...].includes(app)`) を parse できない — coverage 検証が無効化された",
        blocking=True,
    )
else:
    check(False, "Check 138: js/router.js and js/components.js present",
          "Check 138: js/router.js または js/components.js が無い — sidebar↔router coverage を検証できない", blocking=True)

# ── 139. AppsPage app index ↔ router app whitelist coverage (BLOCKING) ──────────
# AppsPage (js/components.js) は canonical な「アプリ一覧」index で、全 built-in app をカードで描画し
# 各「開く」ボタンが apps/<id> へ遷移する。command palette (Check 128) / sidebar (Check 138) と並ぶ
# 3 つ目の app-route producer 面だが、唯一未強制だった。AppsPage の `apps` 配列が router whitelist
# から drift する (router/main.js/cmdk/sidebar には新 app を足したが AppsPage を忘れる) と、その app は
# 他では route できるのに canonical index から発見不能になる。AppsPage の `const apps = [...]` 配列に
# scope して `id: '<app>'` を parse し、router の全 app が出ることを強制する。これで 3 producer 面
# (palette/sidebar/AppsPage) が全て router whitelist に追従し app-route coherence mesh が閉じる。
_router139 = ROOT / "js" / "router.js"
_comp139 = ROOT / "js" / "components.js"
if _router139.exists() and _comp139.exists():
    _rsrc139 = _router139.read_text(encoding="utf-8")
    _csrc139 = _comp139.read_text(encoding="utf-8")
    _rm139 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _rsrc139)
    _router_apps139 = set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _rm139.group(1))) if _rm139 else set()
    # AppsPage の apps 配列に scope (他所の id: と混同しないため function AppsPage 内の const apps を抽出)
    _appspage139 = re.search(r"function AppsPage\(\)\s*\{.*?const apps\s*=\s*\[(.*?)\];", _csrc139, re.DOTALL)
    _appspage_apps139 = set(re.findall(r"id:\s*['\"]([a-z0-9_-]+)['\"]", _appspage139.group(1))) if _appspage139 else set()
    _missing139 = _router_apps139 - _appspage_apps139
    check(
        bool(_router_apps139) and bool(_appspage_apps139) and not _missing139,
        f"Check 139: AppsPage index が router の全 app を被覆 ({sorted(_router_apps139)})",
        f"Check 139: AppsPage index に router app が欠落: {sorted(_missing139)} — "
        f"js/components.js の AppsPage `const apps = [...]` に `{{ id: '<app>', title: ..., desc: ..., icon: ... }}` を追加せよ "
        f"(canonical アプリ一覧から発見不能になる)"
        if (_router_apps139 and _appspage_apps139) else
        "Check 139: router.js の app whitelist または AppsPage の `const apps = [...]` を parse できない (構造を確認せよ)",
        blocking=True,
    )
else:
    check(False, "Check 139: js/router.js and js/components.js present",
          "Check 139: js/router.js または js/components.js が無い — AppsPage↔router coverage を検証できない", blocking=True)

# ── 140. Settings demo selector ↔ router app whitelist coverage (BLOCKING) ──────
# Settings の手動追加フォーム (js/apps.js SettingsPage) は、ユーザーがプロジェクトを作成し、その
# プロジェクトがどの app をデモするかを `<select>` (onchange が settingsNewDemo を書き込む) で選ばせる。
# この `<option value='<app>'>` リストは「手動作成プロジェクトが demoRoute に持てる app」を決める
# WRITE 面である。store.js normalizeProject は demoRoute ∈ router whitelist を許容し (Check 136)、
# router は全 app を route できるが、このセレクタが drift する (新 app を router/store/main.js/cmdk/
# sidebar/AppsPage に足したがここを忘れる) と、その app は demo として silent に選択不能になる — notes が
# store/sidebar/AppsPage/palette で忘れられた #257/#292/#293 と同一の再発クラス。デモセレクタブロックに
# scope して非空の `value: '<app>'` オプションを parse し、router whitelist と一致することを強制する
# (空の "Demoなし" オプションは許可)。これで全 routable app がプロジェクト demo として選択可能に保たれる。
_apps140 = ROOT / "js" / "apps.js"
_router140 = ROOT / "js" / "router.js"
if _apps140.exists() and _router140.exists():
    _asrc140 = _apps140.read_text(encoding="utf-8")
    _rsrc140 = _router140.read_text(encoding="utf-8")
    _rm140 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _rsrc140)
    _router_apps140 = set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _rm140.group(1))) if _rm140 else set()
    # settingsNewDemo を書き込む onchange を持つ select の option 群に scope。anchor は distinctive な
    # aria-label、終端は次の addProjectManual 配線 (フォームの「追加」ボタン)。
    _anchor140 = _asrc140.find("'Demo アプリの種類'")
    _block140 = ""
    if _anchor140 != -1:
        _endpos140 = _asrc140.find("addProjectManual", _anchor140)
        _block140 = _asrc140[_anchor140:_endpos140 if _endpos140 != -1 else _anchor140 + 800]
    # value: settingsNewDemo (無引用符) は対象外。value: '' (Demoなし) は空ゆえ除外。
    _demo_opts140 = set(v for v in re.findall(r"value:\s*['\"]([a-z0-9_-]*)['\"]", _block140) if v)
    _missing140 = _router_apps140 - _demo_opts140
    _extra140 = _demo_opts140 - _router_apps140
    check(
        bool(_router_apps140) and bool(_demo_opts140) and not _missing140 and not _extra140,
        f"Check 140: Settings demo selector options == router app whitelist ({sorted(_router_apps140)})",
        f"Check 140: Settings demo selector ↔ router app whitelist drift — selector に欠落 (demo 選択不能): "
        f"{sorted(_missing140)} / selector のみ (dead option): {sorted(_extra140)}。js/apps.js SettingsPage の "
        f"Demo セレクタに `h('option', {{ value: '<app>' }}, '<app>')` を追加/削除し router whitelist と一致させよ "
        f"(全 routable app をプロジェクト demo として選択可能に保つ・#257 と同 class)"
        if (_router_apps140 and _demo_opts140) else
        "Check 140: router.js の app whitelist または Settings の Demo セレクタ option を parse できない (構造を確認せよ)",
        blocking=True,
    )
else:
    check(False, "Check 140: js/apps.js and js/router.js present",
          "Check 140: js/apps.js または js/router.js が無い — Settings demo selector coverage を検証できない", blocking=True)

# ── 141. Default-project slug & id uniqueness (BLOCKING) ────────────────────────
# store.js の defaultProjects は `proj("pNN", "slug", ...)` でハードコードされた seed list。
# ProjectDetailPage は find(p.slug === slug) で最初の一致のみを返すため、slug が重複すると後者の
# プロジェクト詳細ページが silent に到達不能になる (#154 と同 class)。user-added プロジェクトは
# addProjectManual が runtime で slug-suffix dedup するが、ハードコード defaults には同保護が無く、
# 将来のデータ編集で重複 slug/id を入れると silently-unreachable なプロジェクトを出荷してしまう。
# proj(...) seed を parse し、id 集合と slug 集合がともに衝突無しであることを BLOCKING 強制する。
_store141 = ROOT / "js" / "store.js"
if _store141.exists():
    _ssrc141 = _store141.read_text(encoding="utf-8")
    # proj("p01", "task-manager", ... の先頭 2 引数 (id, slug) を抽出
    _projs141 = re.findall(r'proj\(\s*"([a-z0-9_]+)"\s*,\s*"([a-z0-9-]+)"', _ssrc141)
    _ids141 = [p[0] for p in _projs141]
    _slugs141 = [p[1] for p in _projs141]
    _dup_ids141 = sorted({x for x in _ids141 if _ids141.count(x) > 1})
    _dup_slugs141 = sorted({x for x in _slugs141 if _slugs141.count(x) > 1})
    check(
        bool(_projs141) and not _dup_ids141 and not _dup_slugs141,
        f"Check 141: default projects ({len(_projs141)}) have unique ids and slugs (no silent-unreachable detail)",
        f"Check 141: default-project 重複検出 — 重複 id: {_dup_ids141} / 重複 slug: {_dup_slugs141}。"
        f"ProjectDetailPage は find(p.slug===slug) で先頭のみ返すため重複 slug は後者の詳細ページを到達不能化する "
        f"(#154 class)。store.js の defaultProjects で id/slug を一意にせよ"
        if _projs141 else
        "Check 141: store.js の proj(...) seed を parse できない (defaultProjects の構造を確認せよ)",
        blocking=True,
    )
else:
    check(False, "Check 141: js/store.js present",
          "Check 141: js/store.js が無い — default-project uniqueness を検証できない", blocking=True)

# ── 142. Playwright e2e gate covers its own toolchain (BLOCKING) ────────────────
# playwright-regression.yml は BLOCKING な behavior/functionality e2e gate だが、CI コスト
# 節約のため shipped-site ファイルへの path filter で発火する。しかし e2e の挙動を決める
# ツールチェーン本体 — @playwright/test (runner) と @axe-core/playwright (a11y) + transitive
# deps — は dependency manifest (package.json / package-lock.json) にあり、その bump は
# shipped-site ファイルを一切変えずに e2e 挙動を変えうる。trigger に manifest が無いと、dep
# bump 時に behavior gate が skip され未検証の test-toolchain 変更が出荷される (実例: PR #318 が
# @axe-core/playwright を bump したが playwright-validation が一度も走らなかった)。本 Check は
# pull_request の paths filter に両 manifest が存在することを強制し、「e2e 挙動を証明する gate」を
# 「e2e 挙動を変えうるファイル」に配線し続ける (file-exists≠file-wired class の CI-trigger 版・
# cf. Check 133/134/135)。
_pwf142 = ROOT / ".github" / "workflows" / "playwright-regression.yml"
if _pwf142.exists():
    _wsrc142 = _pwf142.read_text(encoding="utf-8")
    # `paths:` ブロックの `- '...'` エントリを (インデント連続する範囲で) 抽出。
    _paths142 = []
    _in_paths142 = False
    _paths_indent142 = None
    for _line142 in _wsrc142.splitlines():
        _stripped142 = _line142.strip()
        if re.match(r"^paths:\s*$", _stripped142):
            _in_paths142 = True
            _paths_indent142 = len(_line142) - len(_line142.lstrip())
            continue
        if _in_paths142:
            if _stripped142.startswith("- "):
                _paths142.append(_stripped142[2:].strip().strip("'\""))
            elif _stripped142 == "" or _stripped142.startswith("#"):
                continue  # blank/comment lines stay inside the list
            else:
                # 非リスト行 (= dedent して次キーへ) で paths ブロック終了
                _in_paths142 = False
    _missing142 = [m for m in ("package.json", "package-lock.json") if m not in _paths142]
    check(
        not _missing142,
        "Check 142: playwright-regression.yml paths filter は e2e ツールチェーン manifest "
        "(package.json + package-lock.json) を含む (dep bump で behavior gate が再実行される)",
        f"Check 142: playwright-regression.yml の paths filter に {_missing142} が無い — "
        "e2e ツールチェーン (@playwright/test / @axe-core/playwright + transitive deps) の "
        "bump 時に BLOCKING behavior gate が skip され未検証で出荷される (file-exists≠file-wired "
        "class・cf. Check 133/134/135)。paths に両 manifest を追加せよ",
        blocking=True,
    )
else:
    check(False, "Check 142: .github/workflows/playwright-regression.yml present",
          "Check 142: playwright-regression.yml が無い — e2e gate toolchain coverage を検証できない",
          blocking=True)

# ── 143. Auto-digest workflow covers every digested manifest file (BLOCKING) ────
# .well-known/aio-manifest.json は source_of_truth / supporting_evidence /
# observational_evidence の各エントリを sha256 digest 付きで登録する。
# auto-update-aio-digests.yml はそれらの digest を main への push 時に自動再生成する自動化で、
# path filter で発火する。digested file がその paths に無いと、main 上でその file を編集しても
# digest が自動更新されない (実 drift: real-work-claims.md は Session #21 で manifest に追加された
# が workflow paths には未追加だった)。本 Check は、repo-relative path と sha256 を both 持つ全
# manifest エントリが workflow の push paths に literal か `prefix/**` glob で被覆されることを強制し、
# 「manifest が digest 付きで宣言する file」を「その digest を維持する自動化」に配線し続ける
# (producer/consumer-drift / file-exists≠file-wired class・cf. Check 132/142)。
_manifest143 = ROOT / ".well-known" / "aio-manifest.json"
_autowf143 = ROOT / ".github" / "workflows" / "auto-update-aio-digests.yml"
if _manifest143.exists() and _autowf143.exists():
    _mdata143 = json.loads(_manifest143.read_text(encoding="utf-8"))
    # digest 付き repo-relative path を全カテゴリから収集 (URL-only / path 無しは除外)。
    _digested143 = []
    for _cat143 in ("source_of_truth", "supporting_evidence", "observational_evidence"):
        for _e143 in _mdata143.get(_cat143, []):
            _p143 = _e143.get("path")
            if _p143 and _e143.get("sha256"):
                _digested143.append(_p143)
    # workflow の push `paths:` ブロックを (Check 142 と同方式で) テキスト抽出。
    _wfsrc143 = _autowf143.read_text(encoding="utf-8")
    _wfpaths143 = []
    _in_paths143 = False
    for _line143 in _wfsrc143.splitlines():
        _s143 = _line143.strip()
        if re.match(r"^paths:\s*$", _s143):
            _in_paths143 = True
            continue
        if _in_paths143:
            if _s143.startswith("- "):
                _wfpaths143.append(_s143[2:].strip().strip("'\""))
            elif _s143 == "" or _s143.startswith("#"):
                continue
            else:
                _in_paths143 = False

    def _covered143(path, patterns):
        for _pat143 in patterns:
            if _pat143 == path:
                return True
            if _pat143.endswith("/**") and (
                path == _pat143[:-3] or path.startswith(_pat143[:-2])
            ):
                return True
        return False

    _uncovered143 = sorted({p for p in _digested143 if not _covered143(p, _wfpaths143)})
    check(
        bool(_digested143) and not _uncovered143,
        f"Check 143: auto-update-aio-digests.yml の paths は digest 付き manifest file "
        f"{len(_digested143)} 件を全被覆 (digest 維持の自動化に配線済)",
        f"Check 143: digest 付き manifest file が auto-update-aio-digests.yml の paths から漏れている: "
        f"{_uncovered143} — main 上で編集しても digest が自動再生成されない producer/consumer drift "
        f"(cf. Check 132/142)。workflow の push paths に literal か prefix/** で追加せよ"
        if _digested143 else
        "Check 143: aio-manifest.json から digest 付き path を 1 件も抽出できない (manifest 構造を確認せよ)",
        blocking=True,
    )
else:
    check(False, "Check 143: aio-manifest.json と auto-update-aio-digests.yml present",
          "Check 143: aio-manifest.json または auto-update-aio-digests.yml が無い — "
          "digest 自動化カバレッジを検証できない", blocking=True)

# ── 144. Digest-regen tool's file map matches the manifest (BLOCKING) ───────────
# update_aio_digests.py は manifest sha256 を再計算する自動化で、再生成できる file 集合は
# ハードコードの MANIFEST_PATH_TO_LOCAL dict が正本。Check 143 は WORKFLOW の発火を保証するが、
# 発火後 tool が refresh できるのは本 dict にある file だけ。manifest entry が sha256 を持つのに
# dict key が無いと、workflow は発火しても該当 digest は再計算されず、tool が直せないため BLOCKING
# check_aio_digests.py gate が auto-fix 不能 (人手で sha256 計算が必要) になる。本 Check は dict の
# key 集合が manifest の digested-path 集合と bijection (全 dict key が digested manifest path かつ
# 全 digested manifest path が dict key) であることを強制し、digest-automation chain
# (paths→tool-dict→manifest) の consumer 側エッジを閉じる (cf. Check 143)。
_manifest144 = ROOT / ".well-known" / "aio-manifest.json"
_tool144 = ROOT / ".github" / "scripts" / "update_aio_digests.py"
if _manifest144.exists() and _tool144.exists():
    _mdata144 = json.loads(_manifest144.read_text(encoding="utf-8"))
    _manifest_digested144 = set()
    for _cat144 in ("source_of_truth", "supporting_evidence", "observational_evidence"):
        for _e144 in _mdata144.get(_cat144, []):
            _p144 = _e144.get("path")
            if _p144 and _e144.get("sha256"):
                _manifest_digested144.add(_p144)
    # ast で MANIFEST_PATH_TO_LOCAL の dict literal key 群を抽出 (import 副作用を避ける)。
    _tool_keys144 = set()
    _parse_ok144 = False
    try:
        _tree144 = ast.parse(_tool144.read_text(encoding="utf-8"))
        for _node144 in ast.walk(_tree144):
            if isinstance(_node144, ast.AnnAssign):
                _target144 = _node144.target
            elif isinstance(_node144, ast.Assign):
                _target144 = _node144.targets[0] if _node144.targets else None
            else:
                continue
            if (isinstance(_target144, ast.Name)
                    and _target144.id == "MANIFEST_PATH_TO_LOCAL"
                    and isinstance(_node144.value, ast.Dict)):
                for _k144 in _node144.value.keys:
                    if isinstance(_k144, ast.Constant) and isinstance(_k144.value, str):
                        _tool_keys144.add(_k144.value)
                _parse_ok144 = True
    except SyntaxError:
        _parse_ok144 = False
    _missing_in_tool144 = sorted(_manifest_digested144 - _tool_keys144)
    _orphan_in_tool144 = sorted(_tool_keys144 - _manifest_digested144)
    check(
        _parse_ok144 and bool(_manifest_digested144)
        and not _missing_in_tool144 and not _orphan_in_tool144,
        f"Check 144: update_aio_digests.py の MANIFEST_PATH_TO_LOCAL ({len(_tool_keys144)} keys) は "
        f"manifest の digested-path 集合と bijection (digest 再生成 tool が全 manifest file を被覆)",
        (f"Check 144: digest-regen tool ↔ manifest drift — manifest にあり tool dict に無い "
         f"(再生成不能 = gate auto-fix 不能): {_missing_in_tool144} / tool dict にあり manifest に無い "
         f"(orphan): {_orphan_in_tool144}。update_aio_digests.py の MANIFEST_PATH_TO_LOCAL を manifest の "
         f"digested entry と一致させよ"
         if _parse_ok144 and _manifest_digested144 else
         "Check 144: MANIFEST_PATH_TO_LOCAL を ast で抽出できない、または manifest digested path が空 "
         "(update_aio_digests.py / aio-manifest.json の構造を確認せよ)"),
        blocking=True,
    )
else:
    check(False, "Check 144: aio-manifest.json と update_aio_digests.py present",
          "Check 144: aio-manifest.json または update_aio_digests.py が無い — "
          "digest-regen tool カバレッジを検証できない", blocking=True)

# ── 145. GitHub Actions are pinned to a full commit SHA (BLOCKING) ──────────────
# GitHub 公式 hardening は action を full-length commit SHA に pin することを推奨する。
# 版数タグ (@v6) や branch (@main) は可変で、上流が tag を別 commit へ移動 (or 侵害) すると
# repo を一切変えずに workflow が別コードを実行しうる (supply-chain risk)。本 Check は
# .github/workflows/*.yml の全 `uses: owner/repo@ref` の ref が 40-hex commit SHA であることを
# 強制し、mutable tag への後退を封じる (local `./` action は exempt)。可読性の `# vN` コメントは
# 残り、dependabot (github-actions・Check 68) が pin を最新に保つ。第三者 action が最大の attack
# surface。Check 67/76/115 と同 security-baseline の supply-chain 版。
_wf_dir145 = ROOT / ".github" / "workflows"
if _wf_dir145.is_dir():
    _uses_re145 = re.compile(r"^\s*uses:\s*(\S+)")
    _sha_re145 = re.compile(r"^[0-9a-f]{40}$")
    _unpinned145 = []
    for _wf145 in sorted(_wf_dir145.glob("*.yml")):
        for _i145, _line145 in enumerate(_wf145.read_text(encoding="utf-8").splitlines(), 1):
            _m145 = _uses_re145.match(_line145)
            if not _m145:
                continue
            _ref145 = _m145.group(1)
            if _ref145.startswith("./") or _ref145.startswith("docker://"):
                continue  # local / docker action は SHA-pin 対象外
            if "@" not in _ref145:
                _unpinned145.append(f"{_wf145.name}:{_i145} ({_ref145} — @ref 無し)")
                continue
            _pin145 = _ref145.rsplit("@", 1)[1]
            if not _sha_re145.match(_pin145):
                _unpinned145.append(f"{_wf145.name}:{_i145} ({_ref145})")
    check(
        not _unpinned145,
        "Check 145: 全 GitHub Actions `uses:` が full-length commit SHA に pin されている "
        "(mutable tag / branch なし・supply-chain hardening)",
        "Check 145: SHA pin されていない action ref がある: "
        f"{_unpinned145} — 版数タグ/branch は可変で上流の tag 移動・侵害で無告知に別コードを "
        "実行しうる。`uses: owner/repo@<40-hex SHA> # vN` 形式へ pin せよ (SHA は "
        "`gh api repos/<owner>/<repo>/git/ref/tags/<tag>` で解決)",
        blocking=True,
    )
else:
    check(False, "Check 145: .github/workflows ディレクトリ present",
          "Check 145: .github/workflows が無い — action SHA-pin を検証できない", blocking=True)

# ── 146. Default projects' relatedProjectIds are referentially intact (BLOCKING) ─
# defaultProjects (store.js) の各エントリの relatedProjectIds に列挙される全 id が、実在する
# default project id を参照することを強制。dangling 参照 (typo / 削除済 project の id) は SILENT:
# 関連プロジェクト UI は autoRelatedCandidates (類似度スコア) で欠落を埋めるため section は
# populated に見え、curator の明示的・意図的な関連付けが無症状で失われる (graceful-fallback が
# bug を masking する class・cf. NotFound/FatalPage の vacuous-pass 教訓)。本 Check は project-id
# 集合 (proj() 第1引数) と relatedProjectIds 配列リテラル内の全 pNN 参照を収集し、dangling が無い
# こと (かつ参照が 1 件以上存在し vacuous に pass しないこと) を検証する。Check 141 (id/slug
# 一意性) の兄弟で、こちらは referential integrity を守る。
_store146 = ROOT / "js" / "store.js"
if _store146.exists():
    _src146 = _store146.read_text(encoding="utf-8")
    _ids146 = set(re.findall(r'proj\(\s*"([a-z0-9_]+)"', _src146))
    # relatedProjectIds = pNN のみから成る配列リテラル (store.js で純 pNN 配列は relatedIds のみ)
    _ref146 = set()
    for _arr146 in re.findall(r'\[((?:\s*"p[0-9]+"\s*,?)+)\]', _src146):
        for _r146 in re.findall(r'"(p[0-9]+)"', _arr146):
            _ref146.add(_r146)
    _dangling146 = sorted(_ref146 - _ids146)
    check(
        bool(_ids146) and bool(_ref146) and not _dangling146,
        f"Check 146: defaultProjects の relatedProjectIds は全て実在 project を参照 "
        f"({len(_ids146)} projects, {len(_ref146)} 参照, dangling 0)",
        (f"Check 146: dangling relatedProjectId 検出: {_dangling146} — 実在しない project を "
         "参照している。関連プロジェクト UI は autoRelatedCandidates (類似度 fallback) で欠落を "
         "silent に埋めるため curator の明示的関連付け意図が無言で失われる。store.js の "
         "defaultProjects で参照先 id を修正せよ"
         if _ids146 and _ref146 else
         "Check 146: store.js から project id / relatedProjectIds を抽出できない "
         "(defaultProjects の構造を確認せよ)"),
        blocking=True,
    )
else:
    check(False, "Check 146: js/store.js present",
          "Check 146: js/store.js が無い — relatedProjectIds 整合性を検証できない", blocking=True)

# ── 147. Speakable cssSelector tokens point to live shipped elements (BLOCKING) ─
# js/meta-management.js の SPEAKABLE_SELECTORS は AI 音声アシスタント (JSON-LD
# SpeakableSpecification) が抽出対象とする DOM ノードを route ごとに宣言する AIO 配線。
# selector が指す要素が shipped DOM に実在しないと、宣言上は speakable でも実際の DOM ノードが
# 無く抽出が silent に空振りする AIO 精度劣化になる (console error なし・behavior e2e 非検出)。
# 同ファイル L152-156 の [FIX] コメントが過去の手動修正履歴 (.hero-tagline / .core-thesis を除去 /
# .role-split-table → #role-split-table) を残す demonstrated bug-class だが、これまで未 systematize
# だった。本 Check は SPEAKABLE_SELECTORS object literal の各配列内文字列を抽出し、generic
# catch-all (h1 / [data-speakable] / .sr-only / .sr-only[data-ai-entity] と属性のみセレクタ) を
# 除く各 #id / .class token が shipped 面 (index.html ∪ js/*.js ∪ main.js のうち
# meta-management.js 自身を除く) に literal で実在することを BLOCKING 強制する。
# SPEAKABLE_SELECTORS が空 / 抽出不可 / 非 generic token ゼロ なら vacuous-fail。
_meta147 = ROOT / "js" / "meta-management.js"
if _meta147.exists():
    _msrc147 = _meta147.read_text(encoding="utf-8")
    _block147 = re.search(r"const SPEAKABLE_SELECTORS\s*=\s*\{([^}]*)\}", _msrc147)
    _selectors147: list[str] = []
    if _block147:
        # block 内の全 quoted string を拾う (route 名 key も含むが、_m147 regex が #/. 始まりだけ通すので
        # 'home' 等の key は自然に skip される — `\[...\]` で囲もうとすると `[data-speakable]` 内の `]`
        # で早期終了し silent に末尾 selector を取りこぼす real footgun を回避する)
        for _sel147 in re.findall(r"['\"]([^'\"]+)['\"]", _block147.group(1)):
            _selectors147.append(_sel147)
    # generic catch-all — どんな well-formed page でも常に matche する想定で exempt
    _generic147 = {"h1", "[data-speakable]", ".sr-only", ".sr-only[data-ai-entity]"}
    # shipped 面 corpus を構築 (self-match を避けるため meta-management.js は除く)
    _corpus147_paths: list[Path] = [ROOT / "index.html", ROOT / "main.js"]
    _corpus147_paths += sorted((ROOT / "js").glob("*.js"))
    _corpus147 = ""
    for _p147 in _corpus147_paths:
        if _p147.name == "meta-management.js":
            continue
        if _p147.exists():
            _corpus147 += _p147.read_text(encoding="utf-8") + "\n"
    _dangling147: list[str] = []
    _checked147 = 0
    for _sel147 in _selectors147:
        if _sel147 in _generic147:
            continue
        # 属性のみセレクタ ([attr] / [attr=val]) は catch-all 的に扱い exempt
        if _sel147.startswith("["):
            continue
        # 先頭 #id か .class の token を抽出 (.foo.bar や #foo.bar は最初の token のみ評価)
        _m147 = re.match(r"^([#.])([A-Za-z][\w-]*)", _sel147)
        if not _m147:
            # 形式が想定外なら scope 外として skip (false-positive 回避)
            continue
        _token147 = _m147.group(2)
        _checked147 += 1
        # shipped 面に literal で 1 件以上存在するか (word-boundary)
        if not re.search(r"\b" + re.escape(_token147) + r"\b", _corpus147):
            _dangling147.append(_sel147)
    check(
        bool(_selectors147) and _checked147 > 0 and not _dangling147,
        f"Check 147: SPEAKABLE_SELECTORS の全 selector が shipped 面に実在 "
        f"({len(_selectors147)} selectors, {_checked147} non-generic checked, dangling 0)",
        (f"Check 147: dangling Speakable selector: {_dangling147} — 宣言した cssSelector が "
         "shipped DOM (index.html ∪ js/* ∪ main.js) に実在しない。AI 音声アシスタントが "
         "SpeakableSpecification 経由で抽出に失敗し silent に空振りする (console error 無し・"
         "behavior e2e 非検出)。js/meta-management.js の SPEAKABLE_SELECTORS を実在 id/class へ "
         "修正するか dead selector を除去せよ (cf. 同ファイル L152-156 [FIX] history)"
         if _selectors147 and _checked147 > 0 else
         "Check 147: js/meta-management.js から SPEAKABLE_SELECTORS の非 generic token を抽出 "
         "できない (object literal 構造 / generic 集合 を確認せよ)"),
        blocking=True,
    )
else:
    check(False, "Check 147: js/meta-management.js present",
          "Check 147: js/meta-management.js が無い — Speakable selector 整合性を検証できない",
          blocking=True)

# ── 148. SITE_CONFIG.ARTICLE_ROUTES ⊆ PAGE_META keys (BLOCKING) ─────────────────
# SITE_CONFIG.ARTICLE_ROUTES (main.js) は injectStructuredData が「og:type=article かつ
# Article JSON-LD ノード注入」を適用する route 集合。route 名が PAGE_META (js/page-meta.js)
# に無いと applyMeta が早期 return し fullTitle/desc が空のまま、injectStructuredData は
# (PAGE_META を参照せずに) Article JSON-LD を空 headline/description で注入する silent
# AIO 不整合 (console error 無し・behavior e2e 非検出)。本 Check は ARTICLE_ROUTES の
# 全 route 名が PAGE_META top-level keys に存在することを BLOCKING 強制し、ARTICLE_ROUTES
# が空 / 抽出不可 / PAGE_META が空 / dangling >0 なら fail。Check 147 (dangling Speakable
# selector) の AIO 配線版兄弟。
_main148 = ROOT / "main.js"
_meta148 = ROOT / "js" / "page-meta.js"
if _main148.exists() and _meta148.exists():
    _msrc148 = _main148.read_text(encoding="utf-8")
    _psrc148 = _meta148.read_text(encoding="utf-8")
    _ar148 = re.search(r"ARTICLE_ROUTES:\s*\[([^\]]+)\]", _msrc148)
    _routes148: list[str] = []
    if _ar148:
        _routes148 = re.findall(r"['\"]([^'\"]+)['\"]", _ar148.group(1))
    # PAGE_META top-level key = 4-space indent + (quoted|bare) ident + `:` + `{`
    # 値オブジェクトの内側は 8-space indent なので 4-space 完全一致で top-level だけを拾える。
    _pm_keys148: set[str] = set()
    for _k148 in re.findall(r"^\s{4}'?([A-Za-z][\w-]*)'?:\s*\{", _psrc148, re.MULTILINE):
        _pm_keys148.add(_k148)
    _dangling148 = sorted(r for r in _routes148 if r not in _pm_keys148)
    check(
        bool(_routes148) and bool(_pm_keys148) and not _dangling148,
        f"Check 148: ARTICLE_ROUTES ({_routes148}) すべて PAGE_META keys "
        f"({len(_pm_keys148)} 件) に存在 (Article JSON-LD 整合性)",
        (f"Check 148: dangling ARTICLE_ROUTES: {_dangling148} — PAGE_META に存在しない route 名。"
         "applyMeta は早期 return し fullTitle/desc が空のまま Article JSON-LD が空 headline/"
         "description で silent に注入される。main.js SITE_CONFIG.ARTICLE_ROUTES から dead "
         "route を除去するか js/page-meta.js PAGE_META に対応 entry を追加せよ"
         if _routes148 and _pm_keys148 else
         "Check 148: ARTICLE_ROUTES もしくは PAGE_META keys を抽出できない "
         "(main.js / js/page-meta.js の構造を確認せよ)"),
        blocking=True,
    )
else:
    check(False, "Check 148: main.js + js/page-meta.js present",
          "Check 148: main.js もしくは js/page-meta.js が無い — ARTICLE_ROUTES 整合性を検証できない",
          blocking=True)

# ── 149. Canonical URL three-way coherence (BLOCKING) ──────────────────────────
# canonical URL は AIO entity identifier の単一源。3 surface (index.html
# <link rel=canonical> href / aio-manifest.json entity.canonical_url / main.js
# SITE_CONFIG.CANONICAL_URL) が drift すると AI crawler が複数の canonical signal を
# 見て entity を一つの URL に anchor できず AIO 全体が崩れる。Check 62 が manifest ↔
# llms-full.txt 整合を強制済なので、本 Check は残る 2 edge (link[rel=canonical] と
# SITE_CONFIG) を manifest と byte-identical に固定する。trailing slash / origin も完全一致必須。
_idx149 = ROOT / "index.html"
_man149 = ROOT / ".well-known" / "aio-manifest.json"
_main149 = ROOT / "main.js"
if _idx149.exists() and _man149.exists() and _main149.exists():
    _isrc149 = _idx149.read_text(encoding="utf-8")
    _msrc149 = _main149.read_text(encoding="utf-8")
    try:
        _mdata149 = json.loads(_man149.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        _mdata149 = {}
    _link149_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc149
    )
    _link149 = _link149_m.group(1) if _link149_m else None
    _manifest149 = _mdata149.get("entity", {}).get("canonical_url")
    _sc149_m = re.search(r"CANONICAL_URL:\s*['\"]([^'\"]+)['\"]", _msrc149)
    _site_config149 = _sc149_m.group(1) if _sc149_m else None
    _all_extracted149 = all([_link149, _manifest149, _site_config149])
    _all_match149 = _all_extracted149 and (_link149 == _manifest149 == _site_config149)
    check(
        _all_match149,
        f"Check 149: canonical URL 3-way 一致 ({_link149!r})",
        (f"Check 149: canonical URL drift: link[rel=canonical]={_link149!r} / "
         f"aio-manifest.entity.canonical_url={_manifest149!r} / "
         f"main.js SITE_CONFIG.CANONICAL_URL={_site_config149!r}. "
         "AI crawler が一つの entity を複数 canonical signal で見て identity が崩れる。"
         "3 surface を完全一致させよ (trailing slash / origin も含めて byte-identical)"
         if _all_extracted149 else
         "Check 149: 3 surface のいずれかから canonical URL を抽出できない "
         f"(link={_link149} / manifest={_manifest149} / SITE_CONFIG={_site_config149})"),
        blocking=True,
    )
else:
    check(False, "Check 149: index.html + aio-manifest.json + main.js present",
          "Check 149: canonical URL 検証に必要な 3 source のいずれかが無い", blocking=True)

# ── 150. og:url ↔ canonical URL coherence (BLOCKING) ──────────────────────────
# index.html `<meta property="og:url">` content と `<link rel=canonical>` href が
# byte-identical であることを BLOCKING 強制する。drift は SILENT — OG/social card
# preview (LinkedIn / Slack unfurl / Twitter / Discord) が canonical link と別の URL
# を提示し AI/social crawler の entity 識別が崩れる。Check 149 の canonical-URL
# invariant を最も外部 mention の多い OG surface に拡張する。
_idx150 = ROOT / "index.html"
if _idx150.exists():
    _isrc150 = _idx150.read_text(encoding="utf-8")
    _og150 = re.search(
        r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']+)["\']', _isrc150
    )
    _link150 = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc150
    )
    _og150v = _og150.group(1) if _og150 else None
    _link150v = _link150.group(1) if _link150 else None
    check(
        _og150v is not None and _link150v is not None and _og150v == _link150v,
        f"Check 150: og:url == <link rel=canonical> ({_og150v!r})",
        (f"Check 150: og:url ({_og150v!r}) != canonical ({_link150v!r}) — "
         "OG card preview と canonical link が別 URL を提示し AI/social crawler の "
         "entity 識別に drift。index.html の og:url と <link rel=canonical> を一致させよ "
         "(Check 149 で manifest + SITE_CONFIG とも byte-identical を強制済)"
         if _og150v and _link150v else
         "Check 150: og:url もしくは <link rel=canonical> を抽出できない (index.html を確認せよ)"),
        blocking=True,
    )
else:
    check(False, "Check 150: index.html present",
          "Check 150: index.html が無い — og:url canonical 整合を検証できない", blocking=True)

# ── 151. e2e test() title uniqueness (BLOCKING) ───────────────────────────────
# e2e/portfolio.spec.js の全 `test('...', ...)` title が一意であることを BLOCKING
# 強制する。重複 title は Playwright reporter によっては silent に上書き
# (同名の二件目が記録される / report 上で結果区別がつかない) し、vacuous-test-pair
# の class を生む — 片方の fail が他方の pass で masked されたり、誰がどちらの
# 期待を表しているか読めない。test() 直接呼び出しのみ対象 (test.skip/.fixme/.describe
# は対象外 — title 衝突の影響範囲が異なる)。e2e 空 / 重複 >0 なら fail。
_e2e151 = ROOT / "e2e" / "portfolio.spec.js"
if _e2e151.exists():
    _src151 = _e2e151.read_text(encoding="utf-8")
    _titles151 = re.findall(r"^\s*test\(\s*['\"]([^'\"]+)['\"]", _src151, re.MULTILINE)
    _seen151: dict[str, int] = {}
    for _t151 in _titles151:
        _seen151[_t151] = _seen151.get(_t151, 0) + 1
    _dupes151 = sorted(t for t, c in _seen151.items() if c > 1)
    check(
        bool(_titles151) and not _dupes151,
        f"Check 151: e2e {len(_titles151)} 件の test() title すべて一意",
        (f"Check 151: 重複 e2e test title: {_dupes151} — Playwright reporter で "
         "silent 上書き / 同名で結果区別不能になり vacuous-test-pair を生む。"
         "e2e/portfolio.spec.js で title を一意化せよ"
         if _titles151 else
         "Check 151: e2e/portfolio.spec.js に test() が一つも見つからない (vacuous-fail)"),
        blocking=True,
    )
else:
    check(False, "Check 151: e2e/portfolio.spec.js present",
          "Check 151: e2e/portfolio.spec.js が無い — test title 一意性を検証できない",
          blocking=True)

# ── 152. <html lang> ↔ JSON-LD inLanguage coherence (BLOCKING) ─────────────────
# index.html `<html lang>` 属性と全 JSON-LD `inLanguage` 宣言 (index.html / main.js /
# js/meta-management.js) が同一の言語コードであることを BLOCKING 強制する。drift は
# SILENT — AI/SEO crawler が conflicting な言語 signal を見て primary language を
# 誤分類し、言語スコープ検索 (Google "site:" lang filter / AI search) と AIO で
# discovery が劣化する。本 Check は全 surface から値を集めて単一集合の cardinality
# が 1 であることを検証 (canonical 言語が一つに保たれる)。
_idx152 = ROOT / "index.html"
_main152 = ROOT / "main.js"
_meta152 = ROOT / "js" / "meta-management.js"
if _idx152.exists() and _main152.exists() and _meta152.exists():
    _isrc152 = _idx152.read_text(encoding="utf-8")
    _msrc152 = _main152.read_text(encoding="utf-8")
    _mtsrc152 = _meta152.read_text(encoding="utf-8")
    _html_lang152_m = re.search(
        r'<html[^>]+\blang\s*=\s*["\']([a-zA-Z][\w-]*)["\']', _isrc152
    )
    _html_lang152 = _html_lang152_m.group(1) if _html_lang152_m else None
    _in_lang152: list[tuple[str, str]] = []  # (where, value)
    for _src152, _label152 in [
        (_isrc152, "index.html"),
        (_msrc152, "main.js"),
        (_mtsrc152, "js/meta-management.js"),
    ]:
        for _val152 in re.findall(
            r"['\"]inLanguage['\"]\s*:\s*['\"]([a-zA-Z][\w-]*)['\"]", _src152
        ):
            _in_lang152.append((_label152, _val152))
    _all_lang152: set[str] = {v for (_, v) in _in_lang152}
    if _html_lang152:
        _all_lang152.add(_html_lang152)
    _ok152 = (
        _html_lang152 is not None
        and len(_in_lang152) > 0
        and len(_all_lang152) == 1
    )
    check(
        _ok152,
        f"Check 152: <html lang>={_html_lang152!r} と {len(_in_lang152)} 件の "
        f"JSON-LD inLanguage が全て {_all_lang152} で一致",
        (f"Check 152: 言語コード drift: <html lang>={_html_lang152!r} / "
         f"JSON-LD inLanguage={_in_lang152} / 全集合={_all_lang152}。AI/SEO crawler "
         "が conflicting 言語 signal で primary language を誤分類する。index.html "
         "<html lang> と全 JSON-LD inLanguage を同一言語コードへ統一せよ"
         if _html_lang152 and _in_lang152 else
         f"Check 152: 言語宣言を抽出できない (<html lang>={_html_lang152} / "
         f"inLanguage 件数={len(_in_lang152)}) — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 152: index.html + main.js + js/meta-management.js present",
          "Check 152: 言語 coherence 検証に必要な 3 source のいずれかが無い", blocking=True)

# ── 153. og:image / twitter:image origin uses canonical URL prefix (BLOCKING) ──
# index.html の `<meta property="og:image">` と `<meta name="twitter:image">` content
# URL が `<link rel=canonical>` href を prefix として持つことを BLOCKING 強制する。
# drift は SILENT — social/OG card preview が別 origin の image を提示し
# entity-asset coupling を破壊、stale や third-party image を見せうる。
# Check 149/150 の canonical-URL invariant を image surface (OG/Twitter card の
# 視覚部分) に拡張する。両 meta が必須で片方でも canonical prefix から外れたら fail。
_idx153 = ROOT / "index.html"
if _idx153.exists():
    _isrc153 = _idx153.read_text(encoding="utf-8")
    _link153_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc153
    )
    _canon153 = _link153_m.group(1) if _link153_m else None
    _og_img153_m = re.search(
        r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', _isrc153
    )
    _tw_img153_m = re.search(
        r'<meta\s+name=["\']twitter:image["\']\s+content=["\']([^"\']+)["\']', _isrc153
    )
    _og_img153 = _og_img153_m.group(1) if _og_img153_m else None
    _tw_img153 = _tw_img153_m.group(1) if _tw_img153_m else None
    _drift153: list[str] = []
    if _canon153:
        if _og_img153 and not _og_img153.startswith(_canon153):
            _drift153.append(f"og:image={_og_img153!r}")
        if _tw_img153 and not _tw_img153.startswith(_canon153):
            _drift153.append(f"twitter:image={_tw_img153!r}")
    _ok153 = (
        _canon153 is not None
        and _og_img153 is not None
        and _tw_img153 is not None
        and not _drift153
    )
    check(
        _ok153,
        f"Check 153: og:image / twitter:image は canonical ({_canon153!r}) を prefix",
        (f"Check 153: 画像 URL canonical prefix drift: canonical={_canon153!r} / {_drift153} "
         "— OG/Twitter card preview が別 origin の image を見せ entity-asset coupling が崩れる。"
         "index.html の og:image / twitter:image を canonical URL prefix で始まる絶対 URL へ統一せよ"
         if _canon153 and _og_img153 and _tw_img153 else
         f"Check 153: canonical / og:image / twitter:image を抽出できない "
         f"(canonical={_canon153} / og:image={_og_img153} / twitter:image={_tw_img153})"),
        blocking=True,
    )
else:
    check(False, "Check 153: index.html present",
          "Check 153: index.html が無い — image URL canonical 整合を検証できない",
          blocking=True)

# ── 154. description 3-way presence + og/twitter coherence (BLOCKING) ─────────
# index.html の og:description と twitter:description content が byte-identical
# (card preview の同尺 description)、かつ <meta name="description"> も presence
# 必須を BLOCKING 強制する。drift は SILENT — LinkedIn/Slack 等 OG consumer と
# Twitter 等 twitter: consumer が同じ page を別 card text で見せ entity narrative
# が split する。<meta name="description"> は SERP/AI crawler 向けに intentionally
# 長文ゆえ og/twitter と一致は強制しない (presence のみ vacuous-guard)。
_idx154 = ROOT / "index.html"
if _idx154.exists():
    _isrc154 = _idx154.read_text(encoding="utf-8")
    _meta154_m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', _isrc154
    )
    _og154_m = re.search(
        r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)["\']', _isrc154
    )
    _tw154_m = re.search(
        r'<meta\s+name=["\']twitter:description["\']\s+content=["\']([^"\']+)["\']', _isrc154
    )
    _meta154 = _meta154_m.group(1) if _meta154_m else None
    _og154 = _og154_m.group(1) if _og154_m else None
    _tw154 = _tw154_m.group(1) if _tw154_m else None
    _all_present154 = _meta154 and _og154 and _tw154
    _og_tw_match154 = _og154 == _tw154 if (_og154 and _tw154) else False
    check(
        bool(_all_present154) and _og_tw_match154,
        f"Check 154: description 3 surface presence ✓ + og==twitter byte-identical ✓",
        (f"Check 154: description drift / 欠落: meta-description {'OK' if _meta154 else '欠落'} / "
         f"og:description {'OK' if _og154 else '欠落'} / twitter:description "
         f"{'OK' if _tw154 else '欠落'} / og==twitter: {_og_tw_match154}。"
         "og:description と twitter:description は card preview 同尺で byte-identical 必須 "
         "(LinkedIn/Slack vs Twitter で別 card text を見せると entity narrative が split)。"
         "<meta name=\"description\"> は SERP 向けに別文字列でよいが presence は必須"
         if _all_present154 else
         f"Check 154: 必須 meta description が欠落 "
         f"(name=description={_meta154 is not None} / og:description={_og154 is not None} / "
         f"twitter:description={_tw154 is not None})"),
        blocking=True,
    )
else:
    check(False, "Check 154: index.html present",
          "Check 154: index.html が無い — description 整合を検証できない",
          blocking=True)

# ── 155. og:title ↔ twitter:title byte-identical (BLOCKING) ────────────────────
# index.html の og:title と twitter:title content が byte-identical であることを
# BLOCKING 強制する。両者は card preview の同尺 title で drift は SILENT —
# LinkedIn/Slack/OG consumer と Twitter で別 headline を見せ entity の見え方が
# split する。Check 154 (description coherence) の title 軸兄弟。`<title>` tag は
# SERP vs card で intentionally 異なる尺ゆえ scope から外し og/twitter の pair のみ
# 強制する。両 meta presence + byte-identical 必須。
_idx155 = ROOT / "index.html"
if _idx155.exists():
    _isrc155 = _idx155.read_text(encoding="utf-8")
    _og155_m = re.search(
        r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', _isrc155
    )
    _tw155_m = re.search(
        r'<meta\s+name=["\']twitter:title["\']\s+content=["\']([^"\']+)["\']', _isrc155
    )
    _og155 = _og155_m.group(1) if _og155_m else None
    _tw155 = _tw155_m.group(1) if _tw155_m else None
    _ok155 = (
        _og155 is not None and _tw155 is not None and _og155 == _tw155
    )
    check(
        _ok155,
        f"Check 155: og:title == twitter:title byte-identical ({_og155!r})",
        (f"Check 155: title drift: og:title={_og155!r} / twitter:title={_tw155!r} — "
         "LinkedIn/Slack OG consumer と Twitter で別 headline を見せ entity の見え方が split。"
         "index.html の og:title と twitter:title content を byte-identical に統一せよ"
         if _og155 and _tw155 else
         f"Check 155: og:title もしくは twitter:title meta が欠落 "
         f"(og={_og155 is not None} / twitter={_tw155 is not None})"),
        blocking=True,
    )
else:
    check(False, "Check 155: index.html present",
          "Check 155: index.html が無い — title 整合を検証できない",
          blocking=True)

# ── 156. og:type valid enumeration + og:site_name presence (BLOCKING) ─────────
# index.html の og:type content が valid OG type enumeration ('website' or
# 'article' — meta-management.js の dynamic injection / SITE_CONFIG.ARTICLE_ROUTES
# で扱う唯一の type 集合) であり、og:site_name meta が presence であることを
# BLOCKING 強制する。og:site_name 欠落は card preview から site 識別子を奪い
# entity context が失われ、og:type の invalid 値 (typo / 列挙外) は social
# crawler が generic preview にフォールバックし article-vs-page 区別が失われる。
# presence + enumeration sanity の二段。Check 148 (ARTICLE_ROUTES ⊆ PAGE_META)
# の dynamic injection 軸を補完する static surface 検証。
_idx156 = ROOT / "index.html"
if _idx156.exists():
    _isrc156 = _idx156.read_text(encoding="utf-8")
    _ogt156_m = re.search(
        r'<meta\s+property=["\']og:type["\']\s+content=["\']([^"\']+)["\']', _isrc156
    )
    _ogs156_m = re.search(
        r'<meta\s+property=["\']og:site_name["\']\s+content=["\']([^"\']+)["\']', _isrc156
    )
    _ogt156 = _ogt156_m.group(1) if _ogt156_m else None
    _ogs156 = _ogs156_m.group(1) if _ogs156_m else None
    _valid_types156 = {"website", "article"}
    _ok156 = (
        _ogt156 in _valid_types156
        and _ogs156 is not None
        and _ogs156.strip() != ""
    )
    check(
        _ok156,
        f"Check 156: og:type={_ogt156!r} ∈ {_valid_types156} + og:site_name 存在 ({_ogs156!r})",
        (f"Check 156: og 整合性 fail: og:type={_ogt156!r} (valid={_valid_types156}) / "
         f"og:site_name={_ogs156!r}. og:type は 'website'/'article' のいずれか・"
         "og:site_name は非空文字列 (card preview の site 識別子) 必須。"
         "index.html の <meta property=og:type> / <meta property=og:site_name> を修正せよ"
         if (_ogt156 is not None or _ogs156 is not None) else
         "Check 156: og:type / og:site_name meta を抽出できない"),
        blocking=True,
    )
else:
    check(False, "Check 156: index.html present",
          "Check 156: index.html が無い — og:type/og:site_name 整合を検証できない",
          blocking=True)

# ── 157. Mobile / PWA baseline meta presence (BLOCKING) ────────────────────────
# index.html の <head> に非交渉 baseline meta が必ず存在することを BLOCKING 強制
# する: charset / viewport / theme-color / icon / apple-touch-icon。これらの
# silent 除去は behavior e2e にほぼ非検出だが、viewport 欠落=モバイルズーム破綻 /
# icon 欠落=タブが generic globe / apple-touch-icon 欠落=iOS ホーム追加が縮小
# screenshot / theme-color 欠落=モバイルアドレスバーがデフォルト色、と劣化する。
# 全 5 marker が現状 shipped 済ゆえ presence-only (内容は scope 外) の
# vacuous-removal guard。
_idx157 = ROOT / "index.html"
if _idx157.exists():
    _isrc157 = _idx157.read_text(encoding="utf-8")
    _markers157 = {
        "<meta charset>": re.search(r'<meta\s+charset\s*=', _isrc157, re.IGNORECASE) is not None,
        "<meta name=viewport>": re.search(
            r'<meta\s+name=["\']viewport["\']', _isrc157, re.IGNORECASE
        ) is not None,
        "<meta name=theme-color>": re.search(
            r'<meta\s+name=["\']theme-color["\']', _isrc157, re.IGNORECASE
        ) is not None,
        "<link rel=icon>": re.search(
            r'<link\s+rel=["\']icon["\']', _isrc157, re.IGNORECASE
        ) is not None,
        "<link rel=apple-touch-icon>": re.search(
            r'<link\s+rel=["\']apple-touch-icon["\']', _isrc157, re.IGNORECASE
        ) is not None,
    }
    _missing157 = sorted(k for k, present in _markers157.items() if not present)
    check(
        not _missing157,
        f"Check 157: mobile/PWA baseline meta {len(_markers157)} 件すべて presence "
        f"({sorted(_markers157.keys())})",
        f"Check 157: mobile/PWA baseline meta 欠落: {_missing157} — silent 削除で "
        "モバイル/PWA 体験が劣化する (viewport=zoom 破綻 / icon=タブ globe / "
        "apple-touch-icon=iOS 縮小 screenshot / theme-color=アドレスバー default / "
        "charset=文字化けリスク)。index.html <head> に該当 meta を再追加せよ",
        blocking=True,
    )
else:
    check(False, "Check 157: index.html present",
          "Check 157: index.html が無い — mobile/PWA meta presence を検証できない",
          blocking=True)

# ── 158. Google Fonts preconnect / dns-prefetch presence (BLOCKING) ────────────
# CWV first-paint guard: index.html が Google Fonts への preconnect 2 件
# (fonts.googleapis.com + fonts.gstatic.com) と dns-prefetch 1 件
# (fonts.googleapis.com) を保持することを BLOCKING 強制する。silent 除去は LCP/FCP
# を ~100-200ms 劣化させるが console error も behavior-test signal も出ず、後で
# bisect しにくい (壊れていない・ただ遅い)。
_idx158 = ROOT / "index.html"
if _idx158.exists():
    _isrc158 = _idx158.read_text(encoding="utf-8")
    _hints158 = {
        "preconnect fonts.googleapis.com": re.search(
            r'<link\s+rel=["\']preconnect["\']\s+href=["\']https://fonts\.googleapis\.com["\']',
            _isrc158,
        ) is not None,
        "preconnect fonts.gstatic.com": re.search(
            r'<link\s+rel=["\']preconnect["\']\s+href=["\']https://fonts\.gstatic\.com["\']',
            _isrc158,
        ) is not None,
        "dns-prefetch fonts.googleapis.com": re.search(
            r'<link\s+rel=["\']dns-prefetch["\']\s+href=["\']https://fonts\.googleapis\.com["\']',
            _isrc158,
        ) is not None,
    }
    _missing158 = sorted(k for k, present in _hints158.items() if not present)
    check(
        not _missing158,
        f"Check 158: Google Fonts resource hint 3 件すべて presence",
        f"Check 158: Google Fonts resource hint 欠落: {_missing158} — LCP/FCP を "
        "~100-200ms silent 劣化させる (DNS+TLS+handshake)。index.html <head> に "
        "preconnect/dns-prefetch を復元せよ",
        blocking=True,
    )
else:
    check(False, "Check 158: index.html present",
          "Check 158: index.html が無い — Google Fonts hint presence を検証できない",
          blocking=True)

# ── 159. JSON-LD @context cross-surface coherence (BLOCKING) ───────────────────
# 全 JSON-LD `@context` 値 (index.html 静的 ∪ main.js 動的 ∪ js/meta-management.js
# 動的) が canonical 値 'https://schema.org' 一つに揃うことを BLOCKING 強制する。
# drift (trailing slash / http: / 別 schema vocabulary) は SILENT — JSON 自体は
# parse できるが AI/SEO crawler が schema を recognize できず structured-data signal
# 全体が unknown vocabulary 扱いで崩壊する。全 surface から値を抽出し set
# cardinality が 1 で且つ canonical 値であることを検証。
_idx159 = ROOT / "index.html"
_main159 = ROOT / "main.js"
_meta159 = ROOT / "js" / "meta-management.js"
if _idx159.exists() and _main159.exists() and _meta159.exists():
    _ctx159: set[str] = set()
    _count159 = 0
    for _p159 in [_idx159, _main159, _meta159]:
        _src159 = _p159.read_text(encoding="utf-8")
        for _v159 in re.findall(
            r"""['"]@context['"]\s*:\s*['"]([^'"]+)['"]""", _src159
        ):
            _ctx159.add(_v159)
            _count159 += 1
    _expected159 = "https://schema.org"
    _ok159 = _count159 > 0 and _ctx159 == {_expected159}
    check(
        _ok159,
        f"Check 159: JSON-LD @context {_count159} 件すべて canonical {_expected159!r}",
        (f"Check 159: @context drift: 観測値={_ctx159} (期待={_expected159!r}) — "
         "JSON-LD は parse できるが AI/SEO crawler が schema vocabulary を recognize できず "
         "structured-data signal 全体が unknown 扱いで崩壊する。"
         "index.html / main.js / js/meta-management.js の @context を 'https://schema.org' "
         "に統一せよ"
         if _count159 > 0 else
         "Check 159: JSON-LD @context が一件も見つからない (vacuous-fail)"),
        blocking=True,
    )
else:
    check(False, "Check 159: index.html + main.js + js/meta-management.js present",
          "Check 159: JSON-LD @context coherence 検証に必要な 3 source のいずれかが無い",
          blocking=True)

# ── 160. sw.js hardcoded paths share the canonical URL pathname (BLOCKING) ─────
# sw.js が hardcode する `/<segment>/...` 形式の絶対パス (AIO_FILES 等) が、
# index.html の <link rel=canonical> href の pathname と同じ first segment を
# 使うことを BLOCKING 強制する。drift は SILENT — GitHub Pages の project rename
# や canonical URL の path 変更で SW は登録され続けるが hardcoded paths が
# incoming request URL と一致せず SW 介入層を silent に miss する。
# 文字列リテラル中の `'/<segment>/...'` (quoted) のみ対象。literal '/' (root) は skip。
_sw160 = ROOT / "sw.js"
_idx160 = ROOT / "index.html"
if _sw160.exists() and _idx160.exists():
    _isrc160 = _idx160.read_text(encoding="utf-8")
    _swsrc160 = _sw160.read_text(encoding="utf-8")
    _link160 = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc160
    )
    _canon_path160 = None
    if _link160:
        # parse pathname (e.g. https://yutapr0117-design.github.io/portfolio/ -> /portfolio/)
        from urllib.parse import urlparse as _urlparse160
        _canon_path160 = _urlparse160(_link160.group(1)).path
    # extract quoted absolute paths in sw.js: '/foo/...' or "/foo/..."
    _hardcoded160: list[str] = re.findall(r"""['"](/[^\s'"]+)['"]""", _swsrc160)
    # filter to only those starting with a segment (skip bare '/')
    _segment_paths160 = [p for p in _hardcoded160 if re.match(r"^/[A-Za-z][\w-]*/", p)]
    _drift160: list[str] = []
    if _canon_path160 and _canon_path160 != "/":
        for _p160 in _segment_paths160:
            if not _p160.startswith(_canon_path160):
                _drift160.append(_p160)
    _ok160 = (
        _canon_path160 is not None
        and len(_segment_paths160) > 0
        and not _drift160
    )
    check(
        _ok160,
        f"Check 160: sw.js hardcoded paths ({len(_segment_paths160)} 件) all start with "
        f"canonical pathname {_canon_path160!r}",
        (f"Check 160: sw.js path drift: canonical pathname={_canon_path160!r} / "
         f"non-matching paths={_drift160}. canonical URL の pathname と一致しない hardcoded "
         "path は SW interception で incoming request と一致せず silent miss する。"
         "sw.js の path prefix を canonical URL pathname に揃えるか canonical URL を修正せよ"
         if _canon_path160 and _segment_paths160 else
         f"Check 160: canonical pathname もしくは sw.js segment paths が空 "
         f"(canonical={_canon_path160} / paths={len(_segment_paths160)})"),
        blocking=True,
    )
else:
    check(False, "Check 160: sw.js + index.html present",
          "Check 160: sw.js もしくは index.html が無い — SW path coherence を検証できない",
          blocking=True)

# ── 161. robots.txt User-agent: * baseline (no full-site disallow) (BLOCKING) ──
# robots.txt が `User-agent: *` を持ち、そのブロック内に `Disallow: /` (全 site
# 拒否) が無いことを BLOCKING 強制する。silent な `Disallow: /` 化は全 generic
# crawler (AI + search) からの deindex を意味し AIO-first サイトには category-
# collapse。behavior e2e は localhost に走るため crawl policy の劣化を検出できない。
# `User-agent: *` の section (次の `User-agent:` 行まで) を抽出して full-site
# disallow の存在を否定する。
_rb161 = ROOT / "robots.txt"
if _rb161.exists():
    _rbsrc161 = _rb161.read_text(encoding="utf-8")
    _lines161 = _rbsrc161.splitlines()
    _section161: list[str] = []
    _in_star161 = False
    for _ln161 in _lines161:
        _stripped161 = _ln161.strip()
        if _stripped161.startswith("#") or not _stripped161:
            continue
        if _stripped161.lower().startswith("user-agent:"):
            _agent161 = _stripped161.split(":", 1)[1].strip()
            _in_star161 = _agent161 == "*"
            continue
        if _in_star161:
            _section161.append(_stripped161)
    _has_star161 = _in_star161 or len(_section161) > 0 or any(
        ln.strip().lower() == "user-agent: *" for ln in _lines161
    )
    _full_disallow161 = any(
        _ln.lower().startswith("disallow:")
        and _ln.split(":", 1)[1].strip() == "/"
        for _ln in _section161
    )
    _ok161 = _has_star161 and not _full_disallow161
    check(
        _ok161,
        f"Check 161: robots.txt `User-agent: *` block presence + no full-site Disallow",
        (f"Check 161: robots.txt User-agent: * 不在 / 全 site Disallow 検出 "
         f"(presence={_has_star161} / full-disallow={_full_disallow161})。"
         "Disallow: / は AI + search crawler 双方からの全 site deindex を意味し AIO の "
         "全 discovery を category-collapse させる。robots.txt を修正し generic crawler を "
         "許容せよ"),
        blocking=True,
    )
else:
    check(False, "Check 161: robots.txt present",
          "Check 161: robots.txt が無い", blocking=True)

# ── 162. .gitignore baseline ignore-rules for CI/build artifacts (BLOCKING) ────
# .gitignore が node_modules / __pycache__ / test-results / playwright-report /
# blob-report の 5 ルールすべて宣言することを BLOCKING 強制する。silent 削除は
# 偶発的 `git add` で CI artifact (数百 MB 級) や node_modules を staging に
# 載せうる。Check 37 は tracked 後の artifact ファイルを検出するが、本 Check は
# その upstream の gate を守り artifact が staging 領域に着く前に防ぐ。
_gi162 = ROOT / ".gitignore"
if _gi162.exists():
    _gisrc162 = _gi162.read_text(encoding="utf-8")
    _required162 = [
        "node_modules/",
        "__pycache__/",
        "/test-results/",
        "/playwright-report/",
        "/blob-report/",
    ]
    _missing162 = [r for r in _required162 if r not in _gisrc162]
    check(
        not _missing162,
        f"Check 162: .gitignore baseline 5 rule 全て presence",
        f"Check 162: .gitignore baseline 欠落: {_missing162} — 偶発 `git add` で "
        "CI artifact や node_modules が staging に着く。.gitignore に該当 rule を復元せよ",
        blocking=True,
    )
else:
    check(False, "Check 162: .gitignore present",
          "Check 162: .gitignore が無い", blocking=True)

# ── 163. <link rel=icon> / apple-touch-icon href resolves to actual file (BLOCKING) ─
# index.html の `<link rel="icon">` / `<link rel="apple-touch-icon">` の非 data:
# href が実在 repo file に resolve することを BLOCKING 強制する。dangling は SILENT —
# ブラウザは default globe icon に fall back し、apple-touch-icon は iOS Add-to-Home
# で 404 →縮小 screenshot に fallback する。data: URI (inline SVG fallback) は exempt。
# canonical URL pathname を href から strip して repo-relative path に map する。
_idx163 = ROOT / "index.html"
if _idx163.exists():
    _isrc163 = _idx163.read_text(encoding="utf-8")
    _link163 = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc163
    )
    _canon_path163 = "/"
    if _link163:
        from urllib.parse import urlparse as _urlparse163
        _canon_path163 = _urlparse163(_link163.group(1)).path or "/"
    _icon_hrefs163: list[tuple[str, str]] = []  # (rel, href)
    for _m163 in re.finditer(
        r'<link\s+rel=["\'](icon|apple-touch-icon)["\']\s+(?:type=["\'][^"\']*["\']\s+)?href=["\']([^"\']+)["\']',
        _isrc163,
    ):
        _icon_hrefs163.append((_m163.group(1), _m163.group(2)))
    _missing163: list[str] = []
    _checked163 = 0
    for _rel163, _href163 in _icon_hrefs163:
        if _href163.startswith("data:"):
            continue
        _checked163 += 1
        # strip canonical pathname prefix if matches (e.g. /portfolio/icon.svg -> icon.svg)
        _local163 = _href163
        if _canon_path163 != "/" and _href163.startswith(_canon_path163):
            _local163 = _href163[len(_canon_path163):]
        elif _href163.startswith("/"):
            _local163 = _href163.lstrip("/")
        _target163 = ROOT / _local163
        if not _target163.exists():
            _missing163.append(f"{_rel163}={_href163!r} -> {_local163} (not found)")
    check(
        bool(_icon_hrefs163) and _checked163 > 0 and not _missing163,
        f"Check 163: <link rel=icon|apple-touch-icon> href {_checked163} 件 "
        f"全て実 file に resolve ({len(_icon_hrefs163)} link 中 data: exempt)",
        (f"Check 163: dangling icon href: {_missing163} — ブラウザは default globe / "
         "iOS Add-to-Home は 縮小 screenshot に silent fallback する。"
         "index.html の <link rel=icon> / <link rel=apple-touch-icon> href を実在ファイルへ修正せよ"
         if _icon_hrefs163 else
         "Check 163: <link rel=icon> も <link rel=apple-touch-icon> も見つからない (vacuous)"),
        blocking=True,
    )
else:
    check(False, "Check 163: index.html present",
          "Check 163: index.html が無い — icon href 解決を検証できない",
          blocking=True)

# ── 164. og:image / twitter:image content URL resolves to actual file (BLOCKING) ─
# index.html の og:image / twitter:image content URL が実 repo file に resolve
# することを BLOCKING 強制する。dangling は SILENT — social/OG card preview が
# broken image を提示し console error も behavior-test signal も出ない。
# Check 153 (canonical URL prefix) と Check 163 (icon href resolves) を OG image
# surface に拡張。canonical URL prefix を strip して repo-relative path に map。
_idx164 = ROOT / "index.html"
if _idx164.exists():
    _isrc164 = _idx164.read_text(encoding="utf-8")
    _link164 = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc164
    )
    _canon164 = _link164.group(1) if _link164 else None
    _img_metas164: list[tuple[str, str]] = []  # (name, content)
    _og164 = re.search(
        r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', _isrc164
    )
    if _og164:
        _img_metas164.append(("og:image", _og164.group(1)))
    _tw164 = re.search(
        r'<meta\s+name=["\']twitter:image["\']\s+content=["\']([^"\']+)["\']', _isrc164
    )
    if _tw164:
        _img_metas164.append(("twitter:image", _tw164.group(1)))
    _missing164: list[str] = []
    for _name164, _url164 in _img_metas164:
        _local164 = _url164
        if _canon164 and _url164.startswith(_canon164):
            _local164 = _url164[len(_canon164):]
        elif _url164.startswith("/"):
            _local164 = _url164.lstrip("/")
        _target164 = ROOT / _local164
        if not _target164.exists():
            _missing164.append(f"{_name164}={_url164!r} -> {_local164} (not found)")
    check(
        bool(_img_metas164) and not _missing164,
        f"Check 164: og:image / twitter:image {len(_img_metas164)} 件 全て実 file に resolve",
        (f"Check 164: dangling social image: {_missing164} — OG/Twitter card preview が "
         "broken image を見せ silent に entity-asset coupling 壊れる。"
         "index.html の og:image / twitter:image content を実在 file へ修正せよ"
         if _img_metas164 else
         "Check 164: og:image / twitter:image meta が見つからない (vacuous)"),
        blocking=True,
    )
else:
    check(False, "Check 164: index.html present",
          "Check 164: index.html が無い — image URL 解決を検証できない",
          blocking=True)

# ── 165. .well-known/api-catalog JSON + anchor canonical origin (BLOCKING) ─────
# `.well-known/api-catalog` が valid JSON + linkset array (≥1 entry) + 最初 entry の
# anchor URL が canonical URL prefix を持つことを BLOCKING 強制する。drift は
# SILENT に AI crawler の API endpoint discovery を破壊する (catalog は mcp.json /
# agent-skills / aio-manifest / llms-full への entry-point pointer)。
_ac165 = ROOT / ".well-known" / "api-catalog"
_idx165 = ROOT / "index.html"
if _ac165.exists() and _idx165.exists():
    _isrc165 = _idx165.read_text(encoding="utf-8")
    _canon165_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc165
    )
    _canon165 = _canon165_m.group(1) if _canon165_m else None
    _ok165 = False
    _err165 = ""
    try:
        _ac_data165 = json.loads(_ac165.read_text(encoding="utf-8"))
        _linkset165 = _ac_data165.get("linkset")
        if not isinstance(_linkset165, list) or not _linkset165:
            _err165 = f"linkset が array/非空 でない (type={type(_linkset165).__name__})"
        else:
            _anchor165 = _linkset165[0].get("anchor")
            if not isinstance(_anchor165, str):
                _err165 = f"linkset[0].anchor が文字列でない ({_anchor165!r})"
            elif not _canon165:
                _err165 = "canonical URL を index.html から抽出できない"
            elif not _anchor165.startswith(_canon165):
                _err165 = f"anchor={_anchor165!r} が canonical {_canon165!r} で始まらない"
            else:
                _ok165 = True
    except json.JSONDecodeError as e:
        _err165 = f"JSON parse 失敗: {e}"
    check(
        _ok165,
        f"Check 165: .well-known/api-catalog valid JSON + anchor starts with canonical "
        f"({_canon165!r})",
        f"Check 165: .well-known/api-catalog 整合 fail: {_err165} — AI crawler の API "
        "endpoint discovery が silent に崩壊する。.well-known/api-catalog を修正せよ",
        blocking=True,
    )
else:
    check(False, "Check 165: .well-known/api-catalog + index.html present",
          "Check 165: .well-known/api-catalog もしくは index.html が無い",
          blocking=True)

# ── 166. sitemap.xml <loc> URLs all start with canonical URL prefix (BLOCKING) ─
# sitemap.xml の全 `<loc>` URL が `<link rel=canonical>` href を full prefix と
# して持つことを BLOCKING 強制する。Check 63 は origin-only 整合だが、本 Check は
# canonical URL の full prefix (origin + base path) で揃える。drift (sibling
# project path 等) は SILENT — sitemap crawler が 404 する URL を index する。
_sm166 = ROOT / "sitemap.xml"
_idx166 = ROOT / "index.html"
if _sm166.exists() and _idx166.exists():
    _isrc166 = _idx166.read_text(encoding="utf-8")
    _smsrc166 = _sm166.read_text(encoding="utf-8")
    _canon166_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc166
    )
    _canon166 = _canon166_m.group(1) if _canon166_m else None
    _locs166 = re.findall(r"<loc>([^<]+)</loc>", _smsrc166)
    _drift166 = [u for u in _locs166 if _canon166 and not u.startswith(_canon166)]
    _ok166 = _canon166 is not None and bool(_locs166) and not _drift166
    check(
        _ok166,
        f"Check 166: sitemap.xml {len(_locs166)} 件 <loc> 全て canonical prefix で始まる "
        f"({_canon166!r})",
        (f"Check 166: <loc> prefix drift: canonical={_canon166!r} / drifted={_drift166[:3]}... "
         f"({len(_drift166)} 件) — sitemap crawler が 404 する URL を index する。"
         "sitemap.xml の <loc> を canonical URL prefix に揃えるか canonical を修正せよ"
         if _canon166 and _locs166 else
         f"Check 166: canonical もしくは <loc> 抽出不可 "
         f"(canonical={_canon166} / locs={len(_locs166)})"),
        blocking=True,
    )
else:
    check(False, "Check 166: sitemap.xml + index.html present",
          "Check 166: sitemap.xml もしくは index.html が無い", blocking=True)

# ── 167. aio-monitoring.yml weekly schedule presence (BLOCKING) ────────────────
# AIO 監視 workflow が `schedule.cron:` trigger を持つことを BLOCKING 強制する。
# silent 削除で週次 AIO discovery / citation observability loop が停止し
# observability データが stale 化する (workflow が単に発火しない silent 劣化)。
_aiowf167 = ROOT / ".github" / "workflows" / "aio-monitoring.yml"
if _aiowf167.exists():
    _src167 = _aiowf167.read_text(encoding="utf-8")
    _has_schedule167 = re.search(r"^\s*schedule:\s*$", _src167, re.MULTILINE) is not None
    _has_cron167 = re.search(r"^\s*-\s*cron:\s*['\"][^'\"]+['\"]", _src167, re.MULTILINE) is not None
    check(
        _has_schedule167 and _has_cron167,
        "Check 167: aio-monitoring.yml has schedule.cron trigger (weekly AIO monitoring)",
        f"Check 167: aio-monitoring.yml の schedule/cron trigger 欠落 "
        f"(schedule={_has_schedule167} / cron={_has_cron167}) — silent 削除で週次 AIO "
        "監視が停止し observability データが stale 化。schedule + cron rule を復元せよ",
        blocking=True,
    )
else:
    check(False, "Check 167: aio-monitoring.yml present",
          "Check 167: .github/workflows/aio-monitoring.yml が無い", blocking=True)

# ── 168. aio-manifest entity.architecture references C1/C2/C3 markers (BLOCKING) ─
# aio-manifest.json の `entity.architecture` 文字列が C1/C2/C3 architectural
# constraint markers ("Vanilla JS", "IIFE", "ErrorBoundary") を含むことを BLOCKING
# 強制する。drift は SILENT に AIO entity の architectural identity 宣言を弱体化する
# (AI crawler が manifest 経由で本 site を Boring-Technology Vanilla JS SPA と認識
# できなくなる)。CLAUDE.md §1 architecture statement の manifest 側 mirror。
_man168 = ROOT / ".well-known" / "aio-manifest.json"
if _man168.exists():
    try:
        _mdata168 = json.loads(_man168.read_text(encoding="utf-8"))
        _arch168 = _mdata168.get("entity", {}).get("architecture", "")
        _markers168 = ["Vanilla JS", "IIFE", "ErrorBoundary"]
        _missing168 = [m for m in _markers168 if m not in _arch168]
        check(
            isinstance(_arch168, str) and not _missing168,
            f"Check 168: aio-manifest entity.architecture に C1/C2/C3 marker 全て含む "
            f"({_arch168!r})",
            f"Check 168: entity.architecture marker 欠落: {_missing168} (value={_arch168!r}) — "
            "AIO entity の architectural identity 宣言が weak 化し AI crawler が "
            "Vanilla JS SPA / IIFE / ErrorBoundary の構造を認識できない。"
            "aio-manifest.json の entity.architecture を修正せよ",
            blocking=True,
        )
    except json.JSONDecodeError as e:
        check(False, f"Check 168: aio-manifest.json parse",
              f"Check 168: aio-manifest.json JSON parse 失敗: {e}", blocking=True)
else:
    check(False, "Check 168: aio-manifest.json present",
          "Check 168: .well-known/aio-manifest.json が無い", blocking=True)

# ── 169. aio-manifest entity.role contains canonical role markers (BLOCKING) ───
# aio-manifest.json の `entity.role` list が CLAUDE.md §1 の canonical role
# identifier 3 件 ("AI-Driven PM", "IT Consultant", "KERNEL Framework Designer") を
# 含むことを BLOCKING 強制する。drift は SILENT に AIO entity の professional role
# 宣言を弱体化 (AI crawler の entity disambiguation 精度劣化)。
_man169 = ROOT / ".well-known" / "aio-manifest.json"
if _man169.exists():
    try:
        _mdata169 = json.loads(_man169.read_text(encoding="utf-8"))
        _role169 = _mdata169.get("entity", {}).get("role", [])
        _required169 = ["AI-Driven PM", "IT Consultant", "KERNEL Framework Designer"]
        if not isinstance(_role169, list):
            _role169 = [str(_role169)]
        _role_joined169 = " | ".join(str(r) for r in _role169)
        _missing169 = [m for m in _required169 if m not in _role_joined169]
        check(
            not _missing169,
            f"Check 169: aio-manifest entity.role に canonical role marker 全て含む "
            f"({_role169!r})",
            f"Check 169: entity.role marker 欠落: {_missing169} (value={_role169!r}) — "
            "AIO entity の professional role 宣言が弱体化し AI crawler の "
            "entity disambiguation 精度が劣化。aio-manifest.json entity.role に "
            "canonical role identifier を復元せよ",
            blocking=True,
        )
    except json.JSONDecodeError as e:
        check(False, f"Check 169: aio-manifest.json parse",
              f"Check 169: aio-manifest.json JSON parse 失敗: {e}", blocking=True)
else:
    check(False, "Check 169: aio-manifest.json present",
          "Check 169: .well-known/aio-manifest.json が無い", blocking=True)

# ── 170. aio-manifest entity.disambiguation negative-disambiguation (BLOCKING) ─
# aio-manifest.json の `entity.disambiguation` 文字列が CLAUDE.md §1 の canonical
# negative-identity markers ("academic researcher", "diplomat", "artist", "patent
# inventor") を含むことを BLOCKING 強制する。drift は SILENT に disambiguation
# signal を弱体化 (AI crawler が学術研究者など同名の他 entity と conflate)。
_man170 = ROOT / ".well-known" / "aio-manifest.json"
if _man170.exists():
    try:
        _mdata170 = json.loads(_man170.read_text(encoding="utf-8"))
        _disambig170 = _mdata170.get("entity", {}).get("disambiguation", "")
        _required170 = ["academic researcher", "diplomat", "artist", "patent inventor"]
        _missing170 = [m for m in _required170 if m not in _disambig170]
        check(
            isinstance(_disambig170, str) and not _missing170,
            f"Check 170: aio-manifest entity.disambiguation に negative-identity marker 全て含む",
            f"Check 170: entity.disambiguation marker 欠落: {_missing170} — "
            "AIO crawler が学術研究者など同名の他 entity と conflate する disambiguation "
            "signal の弱体化。aio-manifest.json entity.disambiguation に "
            "negative-identity marker を復元せよ",
            blocking=True,
        )
    except json.JSONDecodeError as e:
        check(False, f"Check 170: aio-manifest.json parse",
              f"Check 170: aio-manifest.json JSON parse 失敗: {e}", blocking=True)
else:
    check(False, "Check 170: aio-manifest.json present",
          "Check 170: .well-known/aio-manifest.json が無い", blocking=True)

# ── 171. index.html ai:* meta URL tags share canonical URL prefix (BLOCKING) ───
# index.html の URL を持つ 4 つの `<meta name="ai:*">` (ai:context, ai:entrypoint,
# ai:canonical, ai:aio-manifest) が canonical URL prefix で始まり、ai:canonical は
# canonical 完全一致を BLOCKING 強制する。drift は SILENT に AIO meta layer を
# canonical URL family から desync させ (sibling-project path を誤用すると AI
# crawler が ai:context を fetch して 404)。
_idx171 = ROOT / "index.html"
if _idx171.exists():
    _isrc171 = _idx171.read_text(encoding="utf-8")
    _canon171_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc171
    )
    _canon171 = _canon171_m.group(1) if _canon171_m else None
    _required171 = ["ai:context", "ai:entrypoint", "ai:canonical", "ai:aio-manifest"]
    _ai_urls171: dict[str, str | None] = {}
    for _name171 in _required171:
        _m171 = re.search(
            rf'<meta\s+name=["\']{re.escape(_name171)}["\']\s+content=["\']([^"\']+)["\']',
            _isrc171,
        )
        _ai_urls171[_name171] = _m171.group(1) if _m171 else None
    _problems171: list[str] = []
    for _name171, _url171 in _ai_urls171.items():
        if _url171 is None:
            _problems171.append(f"{_name171}=<missing>")
        elif _canon171 and not _url171.startswith(_canon171):
            _problems171.append(f"{_name171}={_url171!r} (not prefix of canonical)")
    # ai:canonical exact match
    if _canon171 and _ai_urls171.get("ai:canonical") and _ai_urls171["ai:canonical"] != _canon171:
        _problems171.append(f"ai:canonical={_ai_urls171['ai:canonical']!r} != {_canon171!r}")
    _ok171 = _canon171 is not None and not _problems171
    check(
        _ok171,
        f"Check 171: 4 ai:* URL meta タグ全て canonical prefix + ai:canonical 完全一致",
        f"Check 171: ai:* meta URL drift: canonical={_canon171!r} / problems={_problems171} — "
        "AI crawler が ai:context / ai:aio-manifest を fetch して 404 になり AIO meta layer の "
        "discovery 効果が崩壊する。index.html の ai:* meta を canonical URL 系列に揃えよ",
        blocking=True,
    )
else:
    check(False, "Check 171: index.html present",
          "Check 171: index.html が無い — ai:* meta coherence を検証できない",
          blocking=True)

# ── 172. aio-manifest entity name variants cover canonical identifiers (BLOCKING) ─
# aio-manifest.json の entity.name + entity.name_ja + entity.name_alt が CLAUDE.md
# §1 の canonical name identifier 4 件 ("Yuta Yokoi", "横井雄太", "Yokoi Yuta",
# "yuta") を網羅することを BLOCKING 強制する。drift は SILENT に AIO entity
# matching を弱体化 — AI crawler が drop された variant で query しても本 entity
# が hit しない。
_man172 = ROOT / ".well-known" / "aio-manifest.json"
if _man172.exists():
    try:
        _mdata172 = json.loads(_man172.read_text(encoding="utf-8"))
        _entity172 = _mdata172.get("entity", {})
        _name_parts172 = [_entity172.get("name", ""), _entity172.get("name_ja", "")]
        _name_alt172 = _entity172.get("name_alt", [])
        if isinstance(_name_alt172, list):
            _name_parts172.extend(str(x) for x in _name_alt172)
        _joined172 = " | ".join(str(p) for p in _name_parts172)
        _required172 = ["Yuta Yokoi", "横井雄太", "Yokoi Yuta", "yuta"]
        _missing172 = [m for m in _required172 if m not in _joined172]
        check(
            not _missing172,
            f"Check 172: aio-manifest entity name variants が canonical identifier 4 件全て網羅",
            f"Check 172: entity name 4 variants 欠落: {_missing172} — AIO entity matching が "
            "弱体化し AI crawler が drop された name variant で query しても本 entity が hit しない。"
            "aio-manifest.json entity.name / name_ja / name_alt に variant を復元せよ",
            blocking=True,
        )
    except json.JSONDecodeError as e:
        check(False, f"Check 172: aio-manifest.json parse",
              f"Check 172: aio-manifest.json JSON parse 失敗: {e}", blocking=True)
else:
    check(False, "Check 172: aio-manifest.json present",
          "Check 172: .well-known/aio-manifest.json が無い", blocking=True)

# ── 173. js/identity.js AUTHOR canonical values (BLOCKING) ─────────────────────
# js/identity.js の AUTHOR constants が canonical 値を保持することを BLOCKING
# 強制する: DISPLAY_NAME='yuta' (Check 124 視覚層 anonymity)・JAPANESE_NAME=
# '横井雄太'・AUTHORITATIVE_NAME に "Yuta Yokoi" + "横井雄太" を含む。drift で
# entity-bearing JSON-LD (Person @type) や sr-only entity anchor が silent に壊れる。
# Check 172 (aio-manifest 側) の shipped JS 側 mirror。
_id173 = ROOT / "js" / "identity.js"
if _id173.exists():
    _src173 = _id173.read_text(encoding="utf-8")
    _disp173_m = re.search(r"DISPLAY_NAME:\s*['\"]([^'\"]+)['\"]", _src173)
    _auth173_m = re.search(r"AUTHORITATIVE_NAME:\s*['\"]([^'\"]+)['\"]", _src173)
    _ja173_m = re.search(r"JAPANESE_NAME:\s*['\"]([^'\"]+)['\"]", _src173)
    _disp173 = _disp173_m.group(1) if _disp173_m else None
    _auth173 = _auth173_m.group(1) if _auth173_m else None
    _ja173 = _ja173_m.group(1) if _ja173_m else None
    _problems173: list[str] = []
    if _disp173 != "yuta":
        _problems173.append(f"DISPLAY_NAME={_disp173!r} != 'yuta'")
    if _ja173 != "横井雄太":
        _problems173.append(f"JAPANESE_NAME={_ja173!r} != '横井雄太'")
    if not _auth173 or ("Yuta Yokoi" not in _auth173 or "横井雄太" not in _auth173):
        _problems173.append(f"AUTHORITATIVE_NAME={_auth173!r} missing 'Yuta Yokoi' or '横井雄太'")
    check(
        not _problems173,
        f"Check 173: js/identity.js AUTHOR canonical values OK "
        f"(DISPLAY={_disp173!r} / AUTH={_auth173!r} / JA={_ja173!r})",
        f"Check 173: AUTHOR drift: {_problems173} — entity-bearing JSON-LD (Person @type) や "
        "sr-only entity anchor の renderer 入力が silent に壊れる。"
        "js/identity.js AUTHOR を canonical 値へ復元せよ",
        blocking=True,
    )
else:
    check(False, "Check 173: js/identity.js present",
          "Check 173: js/identity.js が無い", blocking=True)

# ── 174. <meta name=theme-color> values exist in style.css (BLOCKING) ──────────
# index.html の全 theme-color content 値が style.css に literal で存在することを
# BLOCKING 強制する。drift は SILENT に OS chrome (モバイルアドレスバー / OS card)
# を visual brand から desync させ、アドレスバーが site が使わない色を表示する。
_idx174 = ROOT / "index.html"
_css174 = ROOT / "style.css"
if _idx174.exists() and _css174.exists():
    _isrc174 = _idx174.read_text(encoding="utf-8")
    _csrc174 = _css174.read_text(encoding="utf-8")
    _colors174 = re.findall(
        r'<meta\s+name=["\']theme-color["\']\s+content=["\']([^"\']+)["\']', _isrc174
    )
    _missing174 = [c for c in _colors174 if c not in _csrc174]
    check(
        bool(_colors174) and not _missing174,
        f"Check 174: theme-color 値 {_colors174} 全て style.css に literal で存在",
        (f"Check 174: theme-color drift: {_missing174} が style.css に literal で存在しない — "
         "モバイルアドレスバー色が visual brand と desync。index.html theme-color を style.css の "
         "実 brand 色に揃えよ"
         if _colors174 else
         "Check 174: theme-color meta が見つからない (vacuous; Check 157 と一致確認)"),
        blocking=True,
    )
else:
    check(False, "Check 174: index.html + style.css present",
          "Check 174: index.html もしくは style.css が無い", blocking=True)

# ── 175. package.json private: true + name baseline (BLOCKING) ─────────────────
# package.json が `"private": true` と `"name": "portfolio-aio"` を保持することを
# BLOCKING 強制する。private: true 削除は `npm publish` を成功させ内部 dev config
# を public npm registry に流出させる security regression (console error 無し)。
# name は npm tool 識別の anchor。
_pkg175 = ROOT / "package.json"
if _pkg175.exists():
    try:
        _pdata175 = json.loads(_pkg175.read_text(encoding="utf-8"))
        _problems175: list[str] = []
        if _pdata175.get("private") is not True:
            _problems175.append(f"private={_pdata175.get('private')!r} (must be True)")
        if _pdata175.get("name") != "portfolio-aio":
            _problems175.append(f"name={_pdata175.get('name')!r} (must be 'portfolio-aio')")
        check(
            not _problems175,
            "Check 175: package.json private: true + name 'portfolio-aio' OK",
            f"Check 175: package.json baseline drift: {_problems175} — "
            "private 削除で `npm publish` が成功し内部 dev config が public npm registry に "
            "流出する security regression。package.json を修正せよ",
            blocking=True,
        )
    except json.JSONDecodeError as e:
        check(False, f"Check 175: package.json parse",
              f"Check 175: package.json JSON parse 失敗: {e}", blocking=True)
else:
    check(False, "Check 175: package.json present",
          "Check 175: package.json が無い", blocking=True)

# ── 176. index.html JSON-LD @id own-origin canonical prefix (BLOCKING) ─────────
# index.html 静的 JSON-LD の全 `"@id": "URL"` のうち、URL が本サイト origin
# (yutapr0117-design.github.io) を含むものは canonical URL prefix で始まることを
# BLOCKING 強制する。external origin (例: nkgr.co.jp) は exempt。drift は SILENT
# に JSON-LD entity graph linking を破壊 (canonical path 変更時に #person/#webpage
# anchor が旧 prefix を引きずり AI crawler が graph を辿れない)。
_idx176 = ROOT / "index.html"
if _idx176.exists():
    _isrc176 = _idx176.read_text(encoding="utf-8")
    _canon176_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc176
    )
    _canon176 = _canon176_m.group(1) if _canon176_m else None
    _ids176 = re.findall(r'"@id"\s*:\s*"([^"]+)"', _isrc176)
    _own_origin176 = "yutapr0117-design.github.io"
    _own_ids176 = [u for u in _ids176 if _own_origin176 in u]
    _drift176 = [u for u in _own_ids176 if _canon176 and not u.startswith(_canon176)]
    _ok176 = _canon176 is not None and bool(_own_ids176) and not _drift176
    check(
        _ok176,
        f"Check 176: index.html JSON-LD @id (own-origin {len(_own_ids176)} 件) 全て "
        f"canonical {_canon176!r} prefix",
        (f"Check 176: @id prefix drift: canonical={_canon176!r} / drifted={_drift176[:3]}... "
         f"({len(_drift176)} 件) — JSON-LD entity graph linking が崩壊し AI crawler が "
         "#person/#webpage anchor を辿れない。index.html の @id を canonical prefix に揃えよ"
         if _canon176 and _own_ids176 else
         f"Check 176: canonical もしくは own-origin @id 抽出不可 "
         f"(canonical={_canon176} / own_ids={len(_own_ids176)})"),
        blocking=True,
    )
else:
    check(False, "Check 176: index.html present",
          "Check 176: index.html が無い — JSON-LD @id coherence を検証できない",
          blocking=True)

# ── 177. llms-full.txt Version marker == main.js SITE_CONFIG.VERSION (BLOCKING) ─
# llms-full.txt authority header の `**Version:**` 値が main.js SITE_CONFIG.VERSION
# と一致することを BLOCKING 強制する。drift は SILENT に AI-authoritative context
# の version 宣言を live site から desync させる (AI/agent が llms-full.txt を
# 読み込んでも deploy 中の version と違う番号を信じる)。Check 1/2/3/19 の
# version-coherence mesh を llms-full.txt に拡張。
_lf177 = ROOT / "llms-full.txt"
_main177 = ROOT / "main.js"
if _lf177.exists() and _main177.exists():
    _lsrc177 = _lf177.read_text(encoding="utf-8")
    _msrc177 = _main177.read_text(encoding="utf-8")
    _lver177_m = re.search(r"\*\*Version:\*\*\s*(v[0-9]+)", _lsrc177)
    _sver177_m = re.search(r"VERSION:\s*['\"](v[0-9]+)['\"]", _msrc177)
    _lver177 = _lver177_m.group(1) if _lver177_m else None
    _sver177 = _sver177_m.group(1) if _sver177_m else None
    _ok177 = _lver177 is not None and _sver177 is not None and _lver177 == _sver177
    check(
        _ok177,
        f"Check 177: llms-full.txt Version={_lver177!r} == main.js SITE_CONFIG.VERSION={_sver177!r}",
        (f"Check 177: version drift: llms-full.txt={_lver177!r} / SITE_CONFIG={_sver177!r} — "
         "AI/agent が llms-full.txt を読み込んでも deploy 中の version と違う番号を信じる "
         "(AI-authoritative context の version 宣言が live site から desync)。"
         "llms-full.txt の **Version:** または main.js SITE_CONFIG.VERSION を同期せよ"
         if _lver177 and _sver177 else
         f"Check 177: version 抽出不可 (llms-full={_lver177} / SITE_CONFIG={_sver177})"),
        blocking=True,
    )
else:
    check(False, "Check 177: llms-full.txt + main.js present",
          "Check 177: llms-full.txt もしくは main.js が無い", blocking=True)

# ── 178. <meta name=ai:repository> derives from canonical URL (BLOCKING) ───────
# `<meta name="ai:repository">` の content URL が canonical URL から派生する
# GitHub repo URL (`https://github.com/<owner>/<repo>`) と一致することを BLOCKING
# 強制する。owner+repo は canonical URL の hostname 第 1 segment (例
# yutapr0117-design.github.io → yutapr0117-design) と URL path 第 1 segment
# (例 /portfolio/ → portfolio) から導出。drift は SILENT に AI crawler を別 repo
# へ誘導する。
_idx178 = ROOT / "index.html"
if _idx178.exists():
    _isrc178 = _idx178.read_text(encoding="utf-8")
    _canon178_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc178
    )
    _repo178_m = re.search(
        r'<meta\s+name=["\']ai:repository["\']\s+content=["\']([^"\']+)["\']', _isrc178
    )
    _canon178 = _canon178_m.group(1) if _canon178_m else None
    _ai_repo178 = _repo178_m.group(1) if _repo178_m else None
    _expected178 = None
    if _canon178:
        from urllib.parse import urlparse as _urlparse178
        _parsed178 = _urlparse178(_canon178)
        # hostname e.g. yutapr0117-design.github.io → owner = yutapr0117-design
        _host_parts178 = (_parsed178.hostname or "").split(".")
        _owner178 = _host_parts178[0] if _host_parts178 else ""
        # path e.g. /portfolio/ → repo = portfolio
        _path_parts178 = [p for p in (_parsed178.path or "").split("/") if p]
        _repo_name178 = _path_parts178[0] if _path_parts178 else ""
        if _owner178 and _repo_name178:
            _expected178 = f"https://github.com/{_owner178}/{_repo_name178}"
    _ok178 = (
        _canon178 is not None
        and _ai_repo178 is not None
        and _expected178 is not None
        and _ai_repo178 == _expected178
    )
    check(
        _ok178,
        f"Check 178: ai:repository={_ai_repo178!r} は canonical URL 由来 ({_expected178!r})",
        (f"Check 178: ai:repository drift: ai:repository={_ai_repo178!r} / "
         f"expected={_expected178!r} (canonical={_canon178!r} から導出) — "
         "AI crawler が別 GitHub repo へ誘導される。index.html ai:repository を "
         "canonical URL 由来 GitHub URL に揃えよ"
         if _canon178 and _ai_repo178 else
         f"Check 178: canonical / ai:repository 抽出不可 "
         f"(canonical={_canon178} / ai:repository={_ai_repo178})"),
        blocking=True,
    )
else:
    check(False, "Check 178: index.html present",
          "Check 178: index.html が無い", blocking=True)

# ── 179. <meta name=ai:version> matches main.js SITE_CONFIG.VERSION (BLOCKING) ─
# index.html の `<meta name="ai:version">` content と main.js SITE_CONFIG.VERSION が
# byte-identical であることを BLOCKING 強制。drift は SILENT に AI-facing version
# signal を deploy 中の version から desync (AI agent は ai:version を読んで pipeline
# version を判断するため、誤値 = 旧 release の挙動を期待して crawl)。Check 177 が
# llms-full.txt 軸を被覆するのに対し本 Check は ai:* meta 軸を被覆。
_idx179 = ROOT / "index.html"
_main179 = ROOT / "main.js"
if _idx179.exists() and _main179.exists():
    _isrc179 = _idx179.read_text(encoding="utf-8")
    _msrc179 = _main179.read_text(encoding="utf-8")
    _ai_ver179_m = re.search(
        r'<meta\s+name=["\']ai:version["\']\s+content=["\']([^"\']+)["\']', _isrc179
    )
    _site_ver179_m = re.search(
        r"VERSION:\s*['\"]([^'\"]+)['\"]", _msrc179
    )
    _ai_ver179 = _ai_ver179_m.group(1) if _ai_ver179_m else None
    _site_ver179 = _site_ver179_m.group(1) if _site_ver179_m else None
    _ok179 = (
        _ai_ver179 is not None
        and _site_ver179 is not None
        and _ai_ver179 == _site_ver179
    )
    check(
        _ok179,
        f"Check 179: ai:version={_ai_ver179!r} == main.js SITE_CONFIG.VERSION={_site_ver179!r}",
        (f"Check 179: ai:version drift: ai:version={_ai_ver179!r} / "
         f"SITE_CONFIG.VERSION={_site_ver179!r} — AI crawler に旧 version を信じさせる。"
         "index.html ai:version を SITE_CONFIG.VERSION と揃えよ"
         if _ai_ver179 and _site_ver179 else
         f"Check 179: ai:version / SITE_CONFIG.VERSION 抽出不可 "
         f"(ai:version={_ai_ver179} / SITE_CONFIG.VERSION={_site_ver179})"),
        blocking=True,
    )
else:
    check(False, "Check 179: index.html + main.js present",
          "Check 179: index.html または main.js が無い", blocking=True)

# ── 180. <meta name=ai:last-modified> matches main.js SITE_CONFIG.LAST_UPDATED (BLOCKING) ─
# index.html の `<meta name="ai:last-modified">` content と main.js
# SITE_CONFIG.LAST_UPDATED が byte-identical であることを BLOCKING 強制。drift は
# SILENT に AI crawler の freshness signal を破壊し、recency-weighted retrieval に
# stale-view または不当に新しい view を見せうる。Check 179 (ai:version) の timestamp 軸版。
_idx180 = ROOT / "index.html"
_main180 = ROOT / "main.js"
if _idx180.exists() and _main180.exists():
    _isrc180 = _idx180.read_text(encoding="utf-8")
    _msrc180 = _main180.read_text(encoding="utf-8")
    _ai_lm180_m = re.search(
        r'<meta\s+name=["\']ai:last-modified["\']\s+content=["\']([^"\']+)["\']', _isrc180
    )
    _site_lm180_m = re.search(
        r"LAST_UPDATED:\s*['\"]([^'\"]+)['\"]", _msrc180
    )
    _ai_lm180 = _ai_lm180_m.group(1) if _ai_lm180_m else None
    _site_lm180 = _site_lm180_m.group(1) if _site_lm180_m else None
    _ok180 = (
        _ai_lm180 is not None
        and _site_lm180 is not None
        and _ai_lm180 == _site_lm180
    )
    check(
        _ok180,
        f"Check 180: ai:last-modified={_ai_lm180!r} == main.js SITE_CONFIG.LAST_UPDATED={_site_lm180!r}",
        (f"Check 180: ai:last-modified drift: ai:last-modified={_ai_lm180!r} / "
         f"SITE_CONFIG.LAST_UPDATED={_site_lm180!r} — AI crawler の freshness 信号が "
         "deploy 実時刻から desync。index.html ai:last-modified を SITE_CONFIG.LAST_UPDATED と揃えよ"
         if _ai_lm180 and _site_lm180 else
         f"Check 180: ai:last-modified / SITE_CONFIG.LAST_UPDATED 抽出不可 "
         f"(ai:last-modified={_ai_lm180} / SITE_CONFIG.LAST_UPDATED={_site_lm180})"),
        blocking=True,
    )
else:
    check(False, "Check 180: index.html + main.js present",
          "Check 180: index.html または main.js が無い", blocking=True)

# ── 181. main.js SITE_CONFIG.LAST_UPDATED is strict ISO-8601 (BLOCKING) ────────
# main.js SITE_CONFIG.LAST_UPDATED が `YYYY-MM-DD` strict ISO-8601 で実在カレンダー日付
# であることを BLOCKING 強制。free-form / locale-specific format ('2026/05/31',
# '5/31/26' 等) は Check 180 (byte-identical) を素通りし ai:last-modified に伝播するが、
# AI/SEO crawler は ISO-8601 期待ゆえ freshness signal を drop or 誤 parse する。
# 中心 (SITE_CONFIG) で format を縛り downstream coherence (Check 91/180) が自動継承。
from datetime import date as _date181
_main181 = ROOT / "main.js"
if _main181.exists():
    _msrc181 = _main181.read_text(encoding="utf-8")
    _lu181_m = re.search(r"LAST_UPDATED:\s*['\"]([^'\"]+)['\"]", _msrc181)
    _lu181 = _lu181_m.group(1) if _lu181_m else None
    _iso_ok181 = False
    _parse_err181 = None
    if _lu181 and re.match(r"^\d{4}-\d{2}-\d{2}$", _lu181):
        try:
            _y, _m, _d = _lu181.split("-")
            _date181(int(_y), int(_m), int(_d))
            _iso_ok181 = True
        except (ValueError, TypeError) as _e:
            _parse_err181 = str(_e)
    check(
        _iso_ok181,
        f"Check 181: SITE_CONFIG.LAST_UPDATED={_lu181!r} は ISO-8601 (YYYY-MM-DD) かつ実在日付",
        (f"Check 181: SITE_CONFIG.LAST_UPDATED={_lu181!r} が ISO-8601 (YYYY-MM-DD) 形式または実在日付でない "
         f"({_parse_err181 or 'regex mismatch'}) — ai:last-modified に伝播し AI/SEO crawler が "
         "freshness signal を drop / 誤 parse する。'YYYY-MM-DD' (例 '2026-05-31') 形式に揃えよ"
         if _lu181 else
         "Check 181: SITE_CONFIG.LAST_UPDATED が抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 181: main.js present",
          "Check 181: main.js が無い", blocking=True)

# ── 182. ai:* meta URL endpoints resolve to actual repo files (BLOCKING) ──────
# index.html の `<meta name="ai:context">`, `<meta name="ai:entrypoint">`,
# `<meta name="ai:aio-manifest">` content URL が canonical URL prefix を strip した
# repo-relative path で実在 file に resolve することを BLOCKING 強制。Check 171 は
# prefix のみ検証で、prefix 後の path drift (例 llms-full.txt → llms-context.txt
# rename + meta 未更新) は素通り→AI crawler が 404 で discovery 崩壊。Check 163/164
# (icon/og:image resolves) の ai:* meta 軸版。
_idx182 = ROOT / "index.html"
if _idx182.exists():
    _isrc182 = _idx182.read_text(encoding="utf-8")
    _canon182_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc182
    )
    _canon182 = _canon182_m.group(1) if _canon182_m else None
    _ai_meta_names182 = ["ai:context", "ai:entrypoint", "ai:aio-manifest"]
    _dangling182: list[str] = []
    _extracted182: list[tuple[str, str]] = []
    for _name in _ai_meta_names182:
        _m = re.search(
            rf'<meta\s+name=["\']{re.escape(_name)}["\']\s+content=["\']([^"\']+)["\']',
            _isrc182,
        )
        if not _m:
            _dangling182.append(f"{_name}=<missing>")
            continue
        _url = _m.group(1)
        _extracted182.append((_name, _url))
        if _canon182 and _url.startswith(_canon182):
            _rel = _url[len(_canon182):]
        elif _canon182:
            # Try without trailing slash
            _cs = _canon182.rstrip("/") + "/"
            if _url.startswith(_cs):
                _rel = _url[len(_cs):]
            else:
                _dangling182.append(f"{_name}={_url} (canonical prefix 不一致)")
                continue
        else:
            _dangling182.append(f"{_name}={_url} (canonical 抽出不可)")
            continue
        _target = ROOT / _rel.lstrip("/")
        if not _target.exists():
            _dangling182.append(f"{_name}={_url} → {_rel} (file 不在)")
    _ok182 = (
        _canon182 is not None
        and len(_extracted182) == len(_ai_meta_names182)
        and not _dangling182
    )
    check(
        _ok182,
        f"Check 182: ai:* meta URL 3 endpoint 全て実 file に resolve "
        f"({', '.join(n for n, _ in _extracted182)})",
        (f"Check 182: ai:* meta URL endpoint 不整合: "
         f"{'; '.join(_dangling182)} — AI crawler が fetch して 404 discovery 崩壊。"
         "ai:context / ai:entrypoint / ai:aio-manifest content URL を canonical 配下の "
         "実在 file に揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 182: index.html present",
          "Check 182: index.html が無い", blocking=True)

# ── 183. sitemap.xml <lastmod> values are strict ISO-8601 YYYY-MM-DD (BLOCKING) ─
# sitemap.xml の全 `<lastmod>` 要素値が strict `YYYY-MM-DD` regex + 実在カレンダー
# 日付であることを BLOCKING 強制。W3C Datetime / sitemap protocol は liberal format
# 許容 (YYYY-MM-DDThh:mm:ss / YYYY/MM/DD 等) だが locale-specific 形式は crawler の
# parser を silent に壊す。Check 65/181 の sitemap 軸版。
from datetime import date as _date183
_sm183 = ROOT / "sitemap.xml"
if _sm183.exists():
    _smsrc183 = _sm183.read_text(encoding="utf-8")
    _lastmods183 = re.findall(r"<lastmod>([^<]+)</lastmod>", _smsrc183)
    _bad183: list[str] = []
    for _v in _lastmods183:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", _v):
            _bad183.append(f"{_v!r} (format)")
            continue
        try:
            _y, _m, _d = _v.split("-")
            _date183(int(_y), int(_m), int(_d))
        except (ValueError, TypeError) as _e:
            _bad183.append(f"{_v!r} ({_e})")
    _ok183 = len(_lastmods183) > 0 and not _bad183
    check(
        _ok183,
        f"Check 183: sitemap.xml <lastmod> {len(_lastmods183)} 件全て ISO-8601 (YYYY-MM-DD) かつ実在日付",
        (f"Check 183: sitemap.xml <lastmod> 不正値: {'; '.join(_bad183)} — "
         "crawler date parser を silent に壊す。strict YYYY-MM-DD に揃えよ"
         if _bad183 else
         "Check 183: sitemap.xml に <lastmod> 0 件 — vacuous-gate"),
        blocking=True,
    )
else:
    check(False, "Check 183: sitemap.xml present",
          "Check 183: sitemap.xml が無い", blocking=True)

# ── 184. sw.js AIO_FILES paths resolve to actual repo files (BLOCKING) ────────
# sw.js の `AIO_FILES = [...]` 配列内文字列を抽出し、index.html canonical URL の
# pathname (例 /portfolio/) を strip した repo-relative path で実在 file に resolve
# することを BLOCKING 強制。Check 160 (pathname 第 1 segment 整合) は素通る path
# tail drift (例 /portfolio/llms.txt → /portfolio/llms-entry.txt rename + sw.js
# 未更新) を捕捉し SW の SWR 404 silent fail を防ぐ。Check 182 (ai:* meta 解決)
# の SW 軸版。
_sw184 = ROOT / "sw.js"
_idx184 = ROOT / "index.html"
if _sw184.exists() and _idx184.exists():
    _swsrc184 = _sw184.read_text(encoding="utf-8")
    _isrc184 = _idx184.read_text(encoding="utf-8")
    _canon184_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc184
    )
    _canon_path184 = ""
    if _canon184_m:
        from urllib.parse import urlparse as _urlparse184
        _canon_path184 = _urlparse184(_canon184_m.group(1)).path  # e.g. "/portfolio/"
    _aio_files184_m = re.search(
        r"const\s+AIO_FILES\s*=\s*\[([^\]]+)\]", _swsrc184
    )
    _aio_paths184: list[str] = []
    if _aio_files184_m:
        _aio_paths184 = re.findall(r"['\"]([^'\"]+)['\"]", _aio_files184_m.group(1))
    _dangling184: list[str] = []
    for _p in _aio_paths184:
        if _canon_path184 and _p.startswith(_canon_path184):
            _rel = _p[len(_canon_path184):]
        else:
            _rel = _p.lstrip("/")
        _target = ROOT / _rel
        if not _target.exists():
            _dangling184.append(f"{_p} → {_rel} (file 不在)")
    _ok184 = (
        _canon_path184 != ""
        and len(_aio_paths184) > 0
        and not _dangling184
    )
    check(
        _ok184,
        f"Check 184: sw.js AIO_FILES {len(_aio_paths184)} 件全て実 file に resolve "
        f"(canonical path '{_canon_path184}' を strip)",
        (f"Check 184: sw.js AIO_FILES 不整合: {'; '.join(_dangling184)} — "
         "SW が rename 後 endpoint を SWR で fetch して silent 404。AIO_FILES の path tail を canonical 配下の "
         "実在 file に揃えよ"
         if _dangling184 else
         "Check 184: sw.js AIO_FILES 抽出不可 / canonical pathname 抽出不可 / 0 件 — vacuous-gate"),
        blocking=True,
    )
else:
    check(False, "Check 184: sw.js + index.html present",
          "Check 184: sw.js または index.html が無い", blocking=True)

# ── 185. Canonical URL uses HTTPS scheme (BLOCKING) ────────────────────────────
# index.html `<link rel="canonical">` href が `https://` で始まることを BLOCKING
# 強制。`http://` drift は SILENT に SEO / security signal を劣化させる
# (browser の "Not Secure" 警告 / crawler が HTTPS variant と別 origin と認識し
# entity 同一性を split / Mixed Content block で sub-resource silent 失敗)。
# Check 149 は 3 surface 一致を保証するが 3 surface 同時 HTTP 化を素通る scheme
# 自体の anchor。
_idx185 = ROOT / "index.html"
if _idx185.exists():
    _isrc185 = _idx185.read_text(encoding="utf-8")
    _canon185_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc185
    )
    _canon185 = _canon185_m.group(1) if _canon185_m else None
    _ok185 = _canon185 is not None and _canon185.startswith("https://")
    check(
        _ok185,
        f"Check 185: canonical URL は HTTPS scheme ({_canon185!r})",
        (f"Check 185: canonical URL が HTTPS でない: {_canon185!r} — "
         "browser 'Not Secure' 警告 / crawler entity split / Mixed Content block。"
         "`https://` 始まりに揃えよ"
         if _canon185 else
         "Check 185: canonical URL 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 185: index.html present",
          "Check 185: index.html が無い", blocking=True)

# ── 186. <meta name=author> contains canonical entity identifiers (BLOCKING) ──
# index.html `<meta name="author">` content が canonical entity name 2 件
# ("Yuta Yokoi" + "横井雄太") を共に含むことを BLOCKING 強制。drift は SILENT に
# HTML 層 author signal を entity identity から desync させ generic SEO/HTML
# crawler (= author meta を読む層) が別 entity を見る。Check 173 (js/identity.js
# AUTHOR) / Check 172 (manifest entity name variants) の HTML <meta name=author>
# surface 版。
_idx186 = ROOT / "index.html"
if _idx186.exists():
    _isrc186 = _idx186.read_text(encoding="utf-8")
    _author186_m = re.search(
        r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']', _isrc186
    )
    _author186 = _author186_m.group(1) if _author186_m else None
    _required186 = ["Yuta Yokoi", "横井雄太"]
    _missing186 = [n for n in _required186 if _author186 and n not in _author186] if _author186 else _required186
    _ok186 = _author186 is not None and not _missing186
    check(
        _ok186,
        f"Check 186: <meta name=author> に canonical entity name 全件含む ({_author186!r})",
        (f"Check 186: <meta name=author>={_author186!r} に必須名 {_missing186} 欠落 — "
         "HTML 層 author signal が entity identity から desync。CLAUDE.md §1 canonical name "
         "('Yuta Yokoi' + '横井雄太') を共に含めよ"
         if _author186 else
         "Check 186: <meta name=author> meta が抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 186: index.html present",
          "Check 186: index.html が無い", blocking=True)

# ── 187. og:locale language sub-tag matches <html lang> (BLOCKING) ────────────
# index.html `<meta property="og:locale">` の language sub-tag (例 ja_JP → ja)
# が `<html lang>` 属性 (例 ja) と一致することを BLOCKING 強制。drift は SILENT に
# OG crawler (LinkedIn/Slack/Facebook unfurl) と browser/SEO crawler へ別言語
# signal を送り、preview card が page と別の audience へ localize される。
# Check 152 (lang ↔ JSON-LD inLanguage) の og:locale 軸版。
_idx187 = ROOT / "index.html"
if _idx187.exists():
    _isrc187 = _idx187.read_text(encoding="utf-8")
    _lang187_m = re.search(r'<html\s+[^>]*lang=["\']([^"\']+)["\']', _isrc187)
    _ogl187_m = re.search(
        r'<meta\s+property=["\']og:locale["\']\s+content=["\']([^"\']+)["\']', _isrc187
    )
    _lang187 = _lang187_m.group(1) if _lang187_m else None
    _ogl187 = _ogl187_m.group(1) if _ogl187_m else None
    # og:locale の language sub-tag (underscore 区切りの先頭)
    _ogl_lang187 = _ogl187.split("_")[0] if _ogl187 else None
    _ok187 = (
        _lang187 is not None
        and _ogl_lang187 is not None
        and _lang187 == _ogl_lang187
    )
    check(
        _ok187,
        f"Check 187: og:locale={_ogl187!r} (lang={_ogl_lang187!r}) == <html lang>={_lang187!r}",
        (f"Check 187: og:locale language drift: og:locale={_ogl187!r} (lang={_ogl_lang187!r}) / "
         f"<html lang>={_lang187!r} — OG crawler が page と別 audience へ localize。"
         "og:locale の language sub-tag を <html lang> と揃えよ"
         if _lang187 and _ogl187 else
         f"Check 187: og:locale / <html lang> 抽出不可 "
         f"(og:locale={_ogl187} / html lang={_lang187})"),
        blocking=True,
    )
else:
    check(False, "Check 187: index.html present",
          "Check 187: index.html が無い", blocking=True)

# ── 188. robots.txt Sitemap URL resolves to actual repo file (BLOCKING) ───────
# robots.txt の `Sitemap:` directive URL が canonical URL pathname を strip した
# repo-relative path で実在 file に resolve することを BLOCKING 強制。Check 63 は
# origin 整合のみで path tail drift (sitemap.xml → sitemap-v2.xml rename + robots
# 未更新) を素通る。crawler (Googlebot 等) は sitemap pointer を 404 で skip し
# sitemap が宣言する全 URL を index しない。Check 182/184 の robots.txt 軸版。
_rb188 = ROOT / "robots.txt"
_idx188 = ROOT / "index.html"
if _rb188.exists() and _idx188.exists():
    _rbsrc188 = _rb188.read_text(encoding="utf-8")
    _isrc188 = _idx188.read_text(encoding="utf-8")
    _canon188_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc188
    )
    _canon_path188 = ""
    if _canon188_m:
        from urllib.parse import urlparse as _urlparse188
        _canon_path188 = _urlparse188(_canon188_m.group(1)).path  # e.g. "/portfolio/"
    _sitemap188_urls = re.findall(r"(?im)^\s*Sitemap:\s*(\S+)", _rbsrc188)
    _dangling188: list[str] = []
    for _u in _sitemap188_urls:
        from urllib.parse import urlparse as _up
        _pth = _up(_u).path
        if _canon_path188 and _pth.startswith(_canon_path188):
            _rel = _pth[len(_canon_path188):]
        else:
            _rel = _pth.lstrip("/")
        _target = ROOT / _rel
        if not _target.exists():
            _dangling188.append(f"{_u} → {_rel} (file 不在)")
    _ok188 = len(_sitemap188_urls) > 0 and not _dangling188
    check(
        _ok188,
        f"Check 188: robots.txt Sitemap: {len(_sitemap188_urls)} 件全て実 file に resolve",
        (f"Check 188: robots.txt Sitemap: 不整合: {'; '.join(_dangling188)} — "
         "crawler が sitemap pointer を 404 で skip し sitemap 宣言 URL を index しない。"
         "robots.txt Sitemap: directive を canonical 配下の実在 file に揃えよ"
         if _dangling188 else
         "Check 188: robots.txt に Sitemap: directive 0 件 — vacuous-gate"),
        blocking=True,
    )
else:
    check(False, "Check 188: robots.txt + index.html present",
          "Check 188: robots.txt または index.html が無い", blocking=True)

# ── 189. <meta name=robots> does not contain noindex / none (BLOCKING) ────────
# index.html `<meta name="robots">` content が `noindex` / `none` を含まないことを
# BLOCKING 強制 (negative invariant)。silent な noindex drift は全 search engine
# (Google/Bing/DuckDuckGo + これを backend にする AI search) からのサイト全 deindex
# = AIO discovery 致命傷で、browser/console/behavior e2e に non-visible。Check 161
# (robots.txt full-site disallow guard) の HTML meta robots 軸版。
_idx189 = ROOT / "index.html"
if _idx189.exists():
    _isrc189 = _idx189.read_text(encoding="utf-8")
    _robots189_m = re.search(
        r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']', _isrc189
    )
    _robots189 = _robots189_m.group(1).lower() if _robots189_m else None
    _forbidden189 = ["noindex", "none"]
    _hits189 = [tok for tok in _forbidden189 if _robots189 and tok in _robots189] if _robots189 else []
    _ok189 = _robots189 is not None and not _hits189
    check(
        _ok189,
        f"Check 189: <meta name=robots>={_robots189!r} に noindex/none 不在 (index 許容)",
        (f"Check 189: <meta name=robots>={_robots189!r} に禁止 token {_hits189} 検出 — "
         "サイト全 deindex (Google/Bing + AI search) で AIO discovery 致命傷。"
         "noindex/none を除去せよ"
         if _hits189 else
         "Check 189: <meta name=robots> 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 189: index.html present",
          "Check 189: index.html が無い", blocking=True)

# ── 190. .nojekyll file presence (GitHub Pages Jekyll bypass) (BLOCKING) ──────
# repo root の `.nojekyll` file 存在を BLOCKING 強制。GitHub Pages は本 file が
# 無いと Jekyll 処理を稼働させ、`_` 始まりの file/directory (例
# `docs/files/_template.md`、`_assets/`) を silent に skip する。本 site は
# underscore-prefix path を含むため本 file 欠落は invisible 破壊 (homepage は
# 描画されるが特定 path が 404 化)。presence-only (file は空でも OK)。
_nj190 = ROOT / ".nojekyll"
_ok190 = _nj190.exists() and _nj190.is_file()
check(
    _ok190,
    "Check 190: .nojekyll file presence (GitHub Pages Jekyll bypass)",
    "Check 190: .nojekyll file が repo root に無い — GitHub Pages が Jekyll 処理を "
    "稼働させ _-prefix path (例 _template.md / _assets/) が silent に 404 化。"
    "`touch .nojekyll` で空 file を作成し commit せよ",
    blocking=True,
)

# ── 191. CNAME file absence (canonical URL is github.io subdomain) (BLOCKING) ─
# repo root に `CNAME` file が存在しないことを BLOCKING 強制 (negative invariant)。
# canonical URL (yutapr0117-design.github.io/portfolio/) は GitHub Pages subdomain
# ゆえ CNAME 追加は silent に deployment を custom domain へ redirect する
# (未所有 → 全 site 404 / 所有未設定 → AIO entity canonical URL ↔ 実 URL 分裂で
# URL coherence Check が cascade 崩壊)。Check 190 (.nojekyll) と並ぶ GitHub Pages
# canonical deployment baseline。
_cname191 = ROOT / "CNAME"
_ok191 = not _cname191.exists()
check(
    _ok191,
    "Check 191: CNAME file 不在 (canonical URL は github.io subdomain)",
    "Check 191: CNAME file が repo root に存在 — GitHub Pages が custom domain へ "
    "deployment を redirect し canonical URL (yutapr0117-design.github.io/portfolio/) と "
    "分裂。custom domain 採用は AIO entity canonical URL の全 surface 同期更新を伴うため "
    "本 Check は意図的に CNAME を禁止。CNAME を削除せよ",
    blocking=True,
)

# ── 192. JSON-LD Person url matches canonical URL (BLOCKING) ──────────────────
# index.html 静的 JSON-LD の Person block の `url` property が canonical URL
# (`<link rel="canonical">` href) と一致することを BLOCKING 強制。drift は SILENT に
# entity の declared homepage を canonical page から desync させ AI/social crawler
# の entity-to-page linking を破壊。Check 176 (@id own-origin canonical prefix) の
# `url` property 軸版。
_idx192 = ROOT / "index.html"
if _idx192.exists():
    _isrc192 = _idx192.read_text(encoding="utf-8")
    _canon192_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc192
    )
    _canon192 = _canon192_m.group(1) if _canon192_m else None
    # Person block: find `"@type": "Person"` then collect within block the first url
    # Person block scope: from `"@type": "Person"` to the next `"@type":` (or
    # end of file). Within that scope we look for a `"url":` at the SAME
    # indentation as `"@type":` (Person's own property, not a nested sub-block).
    _person_blocks192 = []
    _type_positions192 = [m.start() for m in re.finditer(r'"@type":', _isrc192)]
    for _m in re.finditer(r'"@type":\s*"Person"', _isrc192):
        _start = _m.start()
        # find next @type position after this Person
        _next = next((p for p in _type_positions192 if p > _start), len(_isrc192))
        _scope = _isrc192[_start:_next]
        # detect Person's own indentation: the spaces before `"@type":` on its line
        _line_start = _isrc192.rfind("\n", 0, _start) + 1
        _indent = _isrc192[_line_start:_start]  # spaces (or tabs) before `"@type":`
        # match `\n<indent>"url": "..."` (same-indent sibling, not nested)
        _u = re.search(
            r'\n' + re.escape(_indent) + r'"url":\s*"([^"]+)"', _scope
        )
        if _u:
            _person_blocks192.append(_u.group(1))
    _drifts192 = [u for u in _person_blocks192 if _canon192 and u != _canon192]
    _ok192 = (
        _canon192 is not None
        and len(_person_blocks192) > 0
        and not _drifts192
    )
    check(
        _ok192,
        f"Check 192: JSON-LD Person.url {len(_person_blocks192)} 件全て canonical URL と一致 ({_canon192!r})",
        (f"Check 192: JSON-LD Person.url drift: {_drifts192!r} ≠ canonical={_canon192!r} — "
         "AI crawler の entity-to-page linking 破壊。Person.url を canonical URL と揃えよ"
         if _drifts192 else
         "Check 192: JSON-LD Person block or canonical 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 192: index.html present",
          "Check 192: index.html が無い", blocking=True)

# ── 193. JSON-LD WebSite url matches canonical URL (BLOCKING) ─────────────────
# index.html 静的 JSON-LD の WebSite block の `url` property が canonical URL
# と一致することを BLOCKING 強制。drift は SILENT に WebSite entity の declared
# URL を canonical page から desync し JSON-LD WebSite-to-page anchor 破壊 +
# Search Console "About this result" enrichment 混乱。Check 192 (Person.url)
# の WebSite 軸版。同じ sibling-indent 抽出で nested url を skip。
_idx193 = ROOT / "index.html"
if _idx193.exists():
    _isrc193 = _idx193.read_text(encoding="utf-8")
    _canon193_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc193
    )
    _canon193 = _canon193_m.group(1) if _canon193_m else None
    _site_blocks193 = []
    _type_positions193 = [m.start() for m in re.finditer(r'"@type":', _isrc193)]
    for _m in re.finditer(r'"@type":\s*"WebSite"', _isrc193):
        _start = _m.start()
        _next = next((p for p in _type_positions193 if p > _start), len(_isrc193))
        _scope = _isrc193[_start:_next]
        _line_start = _isrc193.rfind("\n", 0, _start) + 1
        _indent = _isrc193[_line_start:_start]
        _u = re.search(r'\n' + re.escape(_indent) + r'"url":\s*"([^"]+)"', _scope)
        if _u:
            _site_blocks193.append(_u.group(1))
    _drifts193 = [u for u in _site_blocks193 if _canon193 and u != _canon193]
    _ok193 = (
        _canon193 is not None
        and len(_site_blocks193) > 0
        and not _drifts193
    )
    check(
        _ok193,
        f"Check 193: JSON-LD WebSite.url {len(_site_blocks193)} 件全て canonical URL と一致 ({_canon193!r})",
        (f"Check 193: JSON-LD WebSite.url drift: {_drifts193!r} ≠ canonical={_canon193!r} — "
         "WebSite entity ↔ canonical page anchor 破壊。WebSite.url を canonical URL と揃えよ"
         if _drifts193 else
         "Check 193: JSON-LD WebSite block or canonical 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 193: index.html present",
          "Check 193: index.html が無い", blocking=True)

# ── 194. JSON-LD WebPage url matches canonical URL (BLOCKING) ─────────────────
# index.html 静的 JSON-LD の WebPage block の `url` property が canonical URL と
# 一致することを BLOCKING 強制。drift は SILENT に page entity の declared URL を
# canonical page から desync し AI/search-engine の page-to-canonical 解決を
# 破壊。Check 192/193 と並ぶ Person/WebSite/WebPage URL coherence triangle 完成。
_idx194 = ROOT / "index.html"
if _idx194.exists():
    _isrc194 = _idx194.read_text(encoding="utf-8")
    _canon194_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc194
    )
    _canon194 = _canon194_m.group(1) if _canon194_m else None
    _page_blocks194 = []
    _type_positions194 = [m.start() for m in re.finditer(r'"@type":', _isrc194)]
    for _m in re.finditer(r'"@type":\s*"WebPage"', _isrc194):
        _start = _m.start()
        _next = next((p for p in _type_positions194 if p > _start), len(_isrc194))
        _scope = _isrc194[_start:_next]
        _line_start = _isrc194.rfind("\n", 0, _start) + 1
        _indent = _isrc194[_line_start:_start]
        _u = re.search(r'\n' + re.escape(_indent) + r'"url":\s*"([^"]+)"', _scope)
        if _u:
            _page_blocks194.append(_u.group(1))
    _drifts194 = [u for u in _page_blocks194 if _canon194 and u != _canon194]
    _ok194 = (
        _canon194 is not None
        and len(_page_blocks194) > 0
        and not _drifts194
    )
    check(
        _ok194,
        f"Check 194: JSON-LD WebPage.url {len(_page_blocks194)} 件全て canonical URL と一致 ({_canon194!r})",
        (f"Check 194: JSON-LD WebPage.url drift: {_drifts194!r} ≠ canonical={_canon194!r} — "
         "page entity ↔ canonical page 解決破壊。WebPage.url を canonical URL と揃えよ"
         if _drifts194 else
         "Check 194: JSON-LD WebPage block or canonical 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 194: index.html present",
          "Check 194: index.html が無い", blocking=True)

# ── 195. JSON-LD Person alternateName contains canonical variants (BLOCKING) ──
# index.html 静的 JSON-LD の primary Person block の `alternateName` array が
# CLAUDE.md §1 canonical name variants ("横井雄太" + "Yokoi Yuta") を共に含む
# ことを BLOCKING 強制。drift は SILENT に AI entity-matching を弱体化
# (Google/AI search で 横井雄太 / Yokoi Yuta query が本 Person entity に anchor
# しない)。Check 172 (manifest entity.name_alt) / 173 (identity.js AUTHOR) の
# JSON-LD Person.alternateName 軸版。
_idx195 = ROOT / "index.html"
if _idx195.exists():
    _isrc195 = _idx195.read_text(encoding="utf-8")
    _required195 = ["横井雄太", "Yokoi Yuta"]
    _person_alt195 = []
    _type_positions195 = [m.start() for m in re.finditer(r'"@type":', _isrc195)]
    for _m in re.finditer(r'"@type":\s*"Person"', _isrc195):
        _start = _m.start()
        _next = next((p for p in _type_positions195 if p > _start), len(_isrc195))
        _scope = _isrc195[_start:_next]
        _line_start = _isrc195.rfind("\n", 0, _start) + 1
        _indent = _isrc195[_line_start:_start]
        # match `\n<indent>"alternateName": [ ... ]` (multi-line array literal)
        _arr = re.search(
            r'\n' + re.escape(_indent) + r'"alternateName":\s*\[([^\]]*)\]', _scope
        )
        if _arr:
            _names = re.findall(r'"([^"]+)"', _arr.group(1))
            _person_alt195.append(_names)
    # check primary (first) Person.alternateName covers required variants
    _primary195 = _person_alt195[0] if _person_alt195 else []
    _missing195 = [n for n in _required195 if n not in _primary195]
    _ok195 = len(_person_alt195) > 0 and not _missing195
    check(
        _ok195,
        f"Check 195: primary Person.alternateName が canonical variants {_required195} を網羅 "
        f"({len(_primary195)} entries)",
        (f"Check 195: primary Person.alternateName に必須 variant {_missing195} 欠落 "
         f"(現 alternateName={_primary195!r}) — AI entity matching を弱体化。"
         "JSON-LD Person.alternateName array に必須 variant を追加せよ"
         if _person_alt195 else
         "Check 195: JSON-LD primary Person block alternateName 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 195: index.html present",
          "Check 195: index.html が無い", blocking=True)

# ── 196. JSON-LD Organization (nkgr.co.jp) name = 株式会社日本経営 (BLOCKING) ─
# index.html 静的 JSON-LD の `@id` が nkgr.co.jp/#organization を含む Organization
# block の `name` が "株式会社日本経営" (CLAUDE.md §1 canonical affiliation 名) と
# 一致することを BLOCKING 強制。drift は SILENT に JSON-LD Organization entity を
# canonical affiliation 宣言 (Check 81-85 で multi-surface 強制) から desync させる。
# 本 Check は affiliation-name coherence mesh を JSON-LD surface まで拡張。
_idx196 = ROOT / "index.html"
if _idx196.exists():
    _isrc196 = _idx196.read_text(encoding="utf-8")
    # find Organization block with @id containing nkgr.co.jp/#organization
    _org196_m = re.search(
        r'"@type":\s*"Organization"[^{]*?"@id":\s*"[^"]*nkgr\.co\.jp[^"]*#organization"',
        _isrc196,
        re.DOTALL,
    )
    if not _org196_m:
        # try the other ordering: @id then @type
        _org196_m = re.search(
            r'"@id":\s*"[^"]*nkgr\.co\.jp[^"]*#organization"[^{]*?"@type":\s*"Organization"',
            _isrc196,
            re.DOTALL,
        )
    _org_name196 = None
    if _org196_m:
        # scope from match start onwards ~600 chars to find name
        _scope = _isrc196[_org196_m.start():_org196_m.start() + 600]
        _n = re.search(r'"name":\s*"([^"]+)"', _scope)
        if _n:
            _org_name196 = _n.group(1)
    _expected196 = "株式会社日本経営"
    _ok196 = _org_name196 == _expected196
    check(
        _ok196,
        f"Check 196: JSON-LD Organization (nkgr.co.jp).name = {_expected196!r}",
        (f"Check 196: JSON-LD Organization (nkgr.co.jp).name = {_org_name196!r} ≠ "
         f"{_expected196!r} — affiliation-name coherence (Check 81-85 と Multi-surface) "
         "から JSON-LD surface が drift。CLAUDE.md §1 canonical affiliation 名に揃えよ"
         if _org_name196 else
         "Check 196: JSON-LD Organization (nkgr.co.jp) block / name 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 196: index.html present",
          "Check 196: index.html が無い", blocking=True)

# ── 197. JSON-LD Organization (nkgr.co.jp) url = https://nkgr.co.jp/ (BLOCKING) ─
# index.html 静的 JSON-LD の Organization block (Check 196 と同 block) の `url`
# property が "https://nkgr.co.jp/" (CLAUDE.md §1 canonical Organization URL) と
# 一致することを BLOCKING 強制。drift は SILENT に AI/social crawler を別 home
# へ誘導し employee→employer URL 解決を破壊。Check 196 (name 軸) の URL 軸版。
_idx197 = ROOT / "index.html"
if _idx197.exists():
    _isrc197 = _idx197.read_text(encoding="utf-8")
    # locate the canonical nkgr Organization block: @type=Organization + @id=
    # nkgr.co.jp/#organization + has both name and url (not the worksFor stub
    # which only has @id reference). Use Check 196's pattern (4-line block
    # signature) to anchor on the full block.
    _org197_m = re.search(
        r'"@id":\s*"https://nkgr\.co\.jp/#organization",\s*\n\s*"name":\s*"株式会社日本経営"',
        _isrc197,
    )
    _org_url197 = None
    if _org197_m:
        _scope = _isrc197[_org197_m.start():_org197_m.start() + 800]
        _u = re.search(r'"url":\s*"([^"]+)"', _scope)
        if _u:
            _org_url197 = _u.group(1)
    _expected197 = "https://nkgr.co.jp/"
    _ok197 = _org_url197 == _expected197
    check(
        _ok197,
        f"Check 197: JSON-LD Organization (nkgr.co.jp).url = {_expected197!r}",
        (f"Check 197: JSON-LD Organization (nkgr.co.jp).url = {_org_url197!r} ≠ "
         f"{_expected197!r} — AI/social crawler が別 Organization home へ誘導。"
         "CLAUDE.md §1 canonical Organization URL に揃えよ"
         if _org_url197 else
         "Check 197: JSON-LD Organization (nkgr.co.jp) url 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 197: index.html present",
          "Check 197: index.html が無い", blocking=True)

# ── 198. JSON-LD Person jobTitle contains canonical role markers (BLOCKING) ───
# index.html 静的 JSON-LD の primary Person block の `jobTitle` string が
# CLAUDE.md §1 canonical role markers ("IT Consultant" + "KERNEL Framework
# Designer") を共に含むことを BLOCKING 強制。drift は SILENT に AI/search-engine
# entity panel 上の professional role 宣言を弱体化。Check 169 (manifest entity.role)
# の JSON-LD Person.jobTitle 軸版。
_idx198 = ROOT / "index.html"
if _idx198.exists():
    _isrc198 = _idx198.read_text(encoding="utf-8")
    # locate primary Person block by `"@type": "Person"` then look for jobTitle
    # within scope (Person block can be ~3KB; jobTitle is sibling-indent).
    _person198_m = re.search(r'"@type":\s*"Person"', _isrc198)
    _jobtitle198 = None
    if _person198_m:
        _line_start = _isrc198.rfind("\n", 0, _person198_m.start()) + 1
        _indent = _isrc198[_line_start:_person198_m.start()]
        # find next "@type": (next entity boundary)
        _all_types = [m.start() for m in re.finditer(r'"@type":', _isrc198)]
        _next = next((p for p in _all_types if p > _person198_m.start()), len(_isrc198))
        _scope = _isrc198[_person198_m.start():_next]
        _jt = re.search(
            r'\n' + re.escape(_indent) + r'"jobTitle":\s*"([^"]+)"', _scope
        )
        if _jt:
            _jobtitle198 = _jt.group(1)
    _required198 = ["IT Consultant", "KERNEL Framework Designer"]
    _missing198 = [m for m in _required198 if _jobtitle198 and m not in _jobtitle198] if _jobtitle198 else _required198
    _ok198 = _jobtitle198 is not None and not _missing198
    check(
        _ok198,
        f"Check 198: primary Person.jobTitle が canonical role markers {_required198} を網羅",
        (f"Check 198: primary Person.jobTitle に必須 marker {_missing198} 欠落 "
         f"(現 jobTitle={_jobtitle198!r}) — AI/search entity panel の role 宣言を弱体化。"
         "CLAUDE.md §1 canonical role markers を jobTitle に含めよ"
         if _jobtitle198 else
         "Check 198: primary Person.jobTitle 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 198: index.html present",
          "Check 198: index.html が無い", blocking=True)

# ── 199. JSON-LD Person knowsAbout contains technical anchors (BLOCKING) ──────
# index.html 静的 JSON-LD の primary Person block の `knowsAbout` array が
# unique 技術 positioning anchor ("KERNEL Framework" + "Vanilla JavaScript SPA")
# を共に含むことを BLOCKING 強制。drift は SILENT に AI search discovery
# (KERNEL Framework / Vanilla JavaScript SPA AI query) を弱体化。knowsAbout は
# Knowledge Panel topics と expert-finder system の feed source。
_idx199 = ROOT / "index.html"
if _idx199.exists():
    _isrc199 = _idx199.read_text(encoding="utf-8")
    _person199_m = re.search(r'"@type":\s*"Person"', _isrc199)
    _know_topics199 = []
    if _person199_m:
        _line_start = _isrc199.rfind("\n", 0, _person199_m.start()) + 1
        _indent = _isrc199[_line_start:_person199_m.start()]
        # scope to the NEXT primary Person block (not nested @type entries
        # like Article sameAs items which share the Person block scope).
        _all_persons = [m.start() for m in re.finditer(r'"@type":\s*"Person"', _isrc199)]
        _next = next((p for p in _all_persons if p > _person199_m.start()), len(_isrc199))
        _scope = _isrc199[_person199_m.start():_next]
        # knowsAbout array starts at sibling indent and contains string entries
        _kw = re.search(
            r'\n' + re.escape(_indent) + r'"knowsAbout":\s*\[([^\]]*)\]', _scope
        )
        if _kw:
            _know_topics199 = re.findall(r'"([^"]+)"', _kw.group(1))
    _required199 = ["KERNEL Framework", "Vanilla JavaScript SPA"]
    _missing199 = [t for t in _required199 if t not in _know_topics199]
    _ok199 = len(_know_topics199) > 0 and not _missing199
    check(
        _ok199,
        f"Check 199: primary Person.knowsAbout が technical anchors {_required199} を網羅 "
        f"({len(_know_topics199)} topics)",
        (f"Check 199: primary Person.knowsAbout に必須 anchor {_missing199} 欠落 "
         f"(現 knowsAbout={_know_topics199!r}) — AI search Knowledge Panel での "
         "expert-topic 紐付けが弱体化。canonical 技術 anchor を knowsAbout に含めよ"
         if _know_topics199 else
         "Check 199: primary Person.knowsAbout 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 199: index.html present",
          "Check 199: index.html が無い", blocking=True)

# ── 200. JSON-LD Person @id derives from canonical URL (BLOCKING) ─────────────
# index.html 静的 JSON-LD の primary Person block の `@id` が canonical URL +
# "#person" と一致することを BLOCKING 強制。drift は SILENT に JSON-LD entity
# graph を分断 (secondary Person references が string-equality で primary @id を
# 引くため primary だけ drift すると孤立 node を生む)。Check 176 (own-origin
# canonical prefix) の Person @id 完全一致軸版。
_idx200 = ROOT / "index.html"
if _idx200.exists():
    _isrc200 = _idx200.read_text(encoding="utf-8")
    _canon200_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc200
    )
    _canon200 = _canon200_m.group(1) if _canon200_m else None
    _person200_m = re.search(r'"@type":\s*"Person"', _isrc200)
    _person_id200 = None
    if _person200_m:
        # @id should be within ~200 chars after @type for primary Person block
        _scope = _isrc200[_person200_m.start():_person200_m.start() + 400]
        _id = re.search(r'"@id":\s*"([^"]+)"', _scope)
        if _id:
            _person_id200 = _id.group(1)
    _expected200 = (_canon200 + "#person") if _canon200 else None
    _ok200 = (
        _canon200 is not None
        and _person_id200 is not None
        and _person_id200 == _expected200
    )
    check(
        _ok200,
        f"Check 200: primary Person.@id = canonical+#person ({_expected200!r})",
        (f"Check 200: primary Person.@id drift: @id={_person_id200!r} ≠ "
         f"canonical+'#person'={_expected200!r} — JSON-LD entity graph 分断 "
         "(secondary Person references が primary @id を引けない)。"
         "primary Person.@id を canonical URL + '#person' に揃えよ"
         if _person_id200 and _canon200 else
         f"Check 200: canonical URL or primary Person.@id 抽出不可 "
         f"(canonical={_canon200} / Person.@id={_person_id200})"),
        blocking=True,
    )
else:
    check(False, "Check 200: index.html present",
          "Check 200: index.html が無い", blocking=True)

# ── 201. JSON-LD WebSite/WebPage @id derive from canonical URL (BLOCKING) ─────
# index.html 静的 JSON-LD の primary WebSite block の `@id` が canonical URL +
# "#website" と一致、primary WebPage block の `@id` が canonical URL +
# "#webpage" と一致することを BLOCKING 強制。drift は Check 200 同様 entity
# graph 分断 (isPartOf/mainEntity が dead anchor を指す)。Person/WebSite/WebPage
# @id anchor triangle 完成。
_idx201 = ROOT / "index.html"
if _idx201.exists():
    _isrc201 = _idx201.read_text(encoding="utf-8")
    _canon201_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc201
    )
    _canon201 = _canon201_m.group(1) if _canon201_m else None
    def _extract_id201(_type_label):
        _m = re.search(rf'"@type":\s*"{_type_label}"', _isrc201)
        if not _m:
            return None
        _scope = _isrc201[_m.start():_m.start() + 400]
        _id_m = re.search(r'"@id":\s*"([^"]+)"', _scope)
        return _id_m.group(1) if _id_m else None
    _site_id201 = _extract_id201("WebSite")
    _page_id201 = _extract_id201("WebPage")
    _expected_site201 = (_canon201 + "#website") if _canon201 else None
    _expected_page201 = (_canon201 + "#webpage") if _canon201 else None
    _drifts201 = []
    if _site_id201 != _expected_site201:
        _drifts201.append(f"WebSite.@id={_site_id201!r} ≠ {_expected_site201!r}")
    if _page_id201 != _expected_page201:
        _drifts201.append(f"WebPage.@id={_page_id201!r} ≠ {_expected_page201!r}")
    _ok201 = _canon201 is not None and not _drifts201
    check(
        _ok201,
        f"Check 201: WebSite/WebPage @id 両方とも canonical 派生 ({_expected_site201!r} / {_expected_page201!r})",
        (f"Check 201: JSON-LD WebSite/WebPage @id drift: {'; '.join(_drifts201)} — "
         "entity graph 分断 (isPartOf / mainEntity の dead anchor)。canonical URL + "
         "'#website'/'#webpage' に揃えよ"
         if _drifts201 else
         "Check 201: canonical URL 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 201: index.html present",
          "Check 201: index.html が無い", blocking=True)

# ── 202. Canonical URL pathname ends with `/` (BLOCKING) ──────────────────────
# index.html `<link rel="canonical">` href の pathname が `/` で終わることを
# BLOCKING 強制。trailing slash の喪失は Check 153/164/166/171/182/184/188 が
# 暗黙に依存する prefix 契約を破壊し、startswith は通るが repo-relative path
# stripping が壊れる。
from urllib.parse import urlparse as _urlparse202
_idx202 = ROOT / "index.html"
if _idx202.exists():
    _isrc202 = _idx202.read_text(encoding="utf-8")
    _canon202_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc202
    )
    _canon202 = _canon202_m.group(1) if _canon202_m else None
    _canon202_path = _urlparse202(_canon202).path if _canon202 else ""
    _ok202 = bool(_canon202_path) and _canon202_path.endswith("/")
    check(
        _ok202,
        f"Check 202: canonical URL pathname が `/` で終わる ({_canon202_path!r})",
        (f"Check 202: canonical URL pathname={_canon202_path!r} が trailing slash 無し — "
         "Check 153/164/166/171/182/184/188 の prefix-strip 契約を破壊。"
         "canonical URL を `/portfolio/` のように `/` で終わらせよ"
         if _canon202 else
         "Check 202: canonical URL 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 202: index.html present",
          "Check 202: index.html が無い", blocking=True)

# ── 203. JSON-LD Person givenName/familyName canonical decomposition (BLOCKING) ─
# index.html 静的 JSON-LD の primary Person block の `givenName` が "雄太"・
# `familyName` が "横井" であることを BLOCKING 強制 (CLAUDE.md §1 canonical
# 日本語名 decomposition)。drift は SILENT に Schema.org-aware AI/SEO crawler
# へ誤名前要素を送り Knowledge Panel name display を破壊。Check 195 (alternateName)
# の structured name-decomposition 軸版。
_idx203 = ROOT / "index.html"
if _idx203.exists():
    _isrc203 = _idx203.read_text(encoding="utf-8")
    _person203_m = re.search(r'"@type":\s*"Person"', _isrc203)
    _given203 = None
    _family203 = None
    if _person203_m:
        _line_start = _isrc203.rfind("\n", 0, _person203_m.start()) + 1
        _indent = _isrc203[_line_start:_person203_m.start()]
        _all_persons = [m.start() for m in re.finditer(r'"@type":\s*"Person"', _isrc203)]
        _next = next((p for p in _all_persons if p > _person203_m.start()), len(_isrc203))
        _scope = _isrc203[_person203_m.start():_next]
        _g = re.search(r'\n' + re.escape(_indent) + r'"givenName":\s*"([^"]+)"', _scope)
        _f = re.search(r'\n' + re.escape(_indent) + r'"familyName":\s*"([^"]+)"', _scope)
        _given203 = _g.group(1) if _g else None
        _family203 = _f.group(1) if _f else None
    _expected_g203 = "雄太"
    _expected_f203 = "横井"
    _ok203 = _given203 == _expected_g203 and _family203 == _expected_f203
    check(
        _ok203,
        f"Check 203: primary Person givenName={_given203!r} / familyName={_family203!r} canonical 一致",
        (f"Check 203: primary Person name decomposition drift: "
         f"givenName={_given203!r} (expected {_expected_g203!r}) / "
         f"familyName={_family203!r} (expected {_expected_f203!r}) — "
         "Schema.org 構造化名要素が canonical CLAUDE.md §1 から desync。"
         "JSON-LD givenName/familyName を canonical 値に揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 203: index.html present",
          "Check 203: index.html が無い", blocking=True)

# ── 204. JSON-LD WebSite name contains site brand markers (BLOCKING) ──────────
# index.html 静的 JSON-LD の primary WebSite block の `name` string が site
# brand marker ("yuta" + "AI-Driven PM") を共に含むことを BLOCKING 強制。
# drift は SILENT に WebSite-level brand signal を canonical title (Check 66)
# から desync させ AI/SEO crawler の site identity 認識を弱体化。Check 156
# (og:site_name) の JSON-LD WebSite.name 軸版。
_idx204 = ROOT / "index.html"
if _idx204.exists():
    _isrc204 = _idx204.read_text(encoding="utf-8")
    _site204_m = re.search(r'"@type":\s*"WebSite"', _isrc204)
    _site_name204 = None
    if _site204_m:
        _line_start = _isrc204.rfind("\n", 0, _site204_m.start()) + 1
        _indent = _isrc204[_line_start:_site204_m.start()]
        _all_sites = [m.start() for m in re.finditer(r'"@type":\s*"WebSite"', _isrc204)]
        _next = next((p for p in _all_sites if p > _site204_m.start()), len(_isrc204))
        _scope = _isrc204[_site204_m.start():_next]
        _n = re.search(r'\n' + re.escape(_indent) + r'"name":\s*"([^"]+)"', _scope)
        _site_name204 = _n.group(1) if _n else None
    _required204 = ["yuta", "AI-Driven PM"]
    _missing204 = [m for m in _required204 if _site_name204 and m not in _site_name204] if _site_name204 else _required204
    _ok204 = _site_name204 is not None and not _missing204
    check(
        _ok204,
        f"Check 204: primary WebSite.name が brand markers {_required204} 全て含む ({_site_name204!r})",
        (f"Check 204: primary WebSite.name に必須 brand marker {_missing204} 欠落 "
         f"(現 name={_site_name204!r}) — WebSite-level brand signal が canonical title "
         "から desync。'yuta' + 'AI-Driven PM' を含む形に揃えよ"
         if _site_name204 else
         "Check 204: primary WebSite.name 抽出不可"),
        blocking=True,
    )
else:
    check(False, "Check 204: index.html present",
          "Check 204: index.html が無い", blocking=True)

# ── 205. JSON-LD url fields all use HTTPS (BLOCKING) ──────────────────────────
# index.html 静的 JSON-LD 内の全 `"url": "<URL>"` の値が `https://` で始まる
# ことを BLOCKING 強制 (negative invariant)。drift は SILENT に AI/SEO crawler の
# URL signal を downgrade (Mixed Content block / search insecure penalty /
# AI crawler が http vs https を別 origin と認識)。Check 185 (canonical link
# HTTPS) の JSON-LD 全 entity の url field 軸版。
_idx205 = ROOT / "index.html"
if _idx205.exists():
    _isrc205 = _idx205.read_text(encoding="utf-8")
    # find all "url": "<value>" inside JSON-LD blocks (within <script
    # type="application/ld+json">...</script>). simplest: scan whole file.
    _all_urls205 = re.findall(r'"url":\s*"([^"]+)"', _isrc205)
    _http205 = [u for u in _all_urls205 if u.startswith("http://")]
    _ok205 = len(_all_urls205) > 0 and not _http205
    check(
        _ok205,
        f"Check 205: JSON-LD url field {len(_all_urls205)} 件全て https://",
        (f"Check 205: JSON-LD url field に http:// scheme drift: {_http205!r} — "
         "AI/SEO crawler の URL signal 劣化 (Mixed Content / scheme split)。"
         "JSON-LD url を全て https:// に揃えよ"
         if _http205 else
         "Check 205: JSON-LD url field 0 件 — vacuous-gate"),
        blocking=True,
    )
else:
    check(False, "Check 205: index.html present",
          "Check 205: index.html が無い", blocking=True)

# ── 206. JSON-LD @id URI fields all use HTTPS (BLOCKING) ──────────────────────
# index.html 静的 JSON-LD 内の全 `"@id": "<URI>"` の値が `https://` で始まる
# ことを BLOCKING 強制 (URN/other scheme は本 site で未使用)。drift は SILENT に
# entity graph を分断 (string-equality で参照される @id が http vs https で別
# entity 扱いになる)。Check 205 (url HTTPS) の @id 軸版・Check 176 (own-origin
# canonical prefix) の external-origin (nkgr.co.jp 等) 補完。
_idx206 = ROOT / "index.html"
if _idx206.exists():
    _isrc206 = _idx206.read_text(encoding="utf-8")
    _all_ids206 = re.findall(r'"@id":\s*"([^"]+)"', _isrc206)
    _http206 = [u for u in _all_ids206 if u.startswith("http://")]
    _ok206 = len(_all_ids206) > 0 and not _http206
    check(
        _ok206,
        f"Check 206: JSON-LD @id field {len(_all_ids206)} 件全て https://",
        (f"Check 206: JSON-LD @id field に http:// scheme drift: {_http206!r} — "
         "entity graph 分断 (string-equality 参照で http vs https が別 entity 扱い)。"
         "JSON-LD @id を全て https:// に揃えよ"
         if _http206 else
         "Check 206: JSON-LD @id field 0 件 — vacuous-gate"),
        blocking=True,
    )
else:
    check(False, "Check 206: index.html present",
          "Check 206: index.html が無い", blocking=True)

# ── 207. index.html external src/href attributes all use HTTPS (BLOCKING) ─────
# index.html の `src="<URL>"` / `href="<URL>"` で absolute URL (scheme 付き) の
# 全てが `https://` で始まることを BLOCKING 強制 (negative invariant)。drift は
# SILENT に Mixed Content blocking で sub-resource load 失敗 (production console
# error 抑制化で気付きにくい)。Check 205/206 (JSON-LD url/@id HTTPS) の HTML
# 属性 axis 版。
_idx207 = ROOT / "index.html"
if _idx207.exists():
    _isrc207 = _idx207.read_text(encoding="utf-8")
    # Extract src=/href= values where value starts with a scheme (e.g.
    # https?:// or //) — only flag http:// (relative paths and data: URIs
    # are exempt).
    _all_attrs207 = re.findall(
        r'(?:src|href)\s*=\s*["\'](http://[^"\']+)["\']', _isrc207
    )
    _ok207 = len(_all_attrs207) == 0
    check(
        _ok207,
        "Check 207: index.html src=/href= 属性に http:// 不在 (Mixed Content guard)",
        (f"Check 207: index.html src=/href= 属性に http:// scheme: {_all_attrs207!r} — "
         "browser Mixed Content blocking で sub-resource silent load 失敗。"
         "全 absolute URL を https:// に揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 207: index.html present",
          "Check 207: index.html が無い", blocking=True)

# ── 208. JSON-LD date fields are strict ISO-8601 YYYY-MM-DD (BLOCKING) ────────
# index.html 静的 JSON-LD 内の全 `"datePublished"`/`"dateModified"`/`"dateCreated"`
# 値が strict `YYYY-MM-DD` regex かつ実在カレンダー日付であることを BLOCKING 強制。
# drift は SILENT に Schema.org / Search Console の recency-weighted ranking 用
# freshness signal を corruption (locale 形式は parse 失敗 or 誤 parse)。Check 183
# (sitemap lastmod ISO-8601) の JSON-LD date 軸版。
from datetime import date as _date208
_idx208 = ROOT / "index.html"
if _idx208.exists():
    _isrc208 = _idx208.read_text(encoding="utf-8")
    _date_fields208 = ["datePublished", "dateModified", "dateCreated"]
    _dates208 = []
    for _fld in _date_fields208:
        for _m in re.finditer(rf'"{_fld}":\s*"([^"]+)"', _isrc208):
            _dates208.append((_fld, _m.group(1)))
    _bad208: list[str] = []
    for _fld, _v in _dates208:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", _v):
            _bad208.append(f"{_fld}={_v!r} (format)")
            continue
        try:
            _y, _mo, _d = _v.split("-")
            _date208(int(_y), int(_mo), int(_d))
        except (ValueError, TypeError) as _e:
            _bad208.append(f"{_fld}={_v!r} ({_e})")
    _ok208 = len(_dates208) > 0 and not _bad208
    check(
        _ok208,
        f"Check 208: JSON-LD date field {len(_dates208)} 件全て ISO-8601 (YYYY-MM-DD) かつ実在日付",
        (f"Check 208: JSON-LD date field 不正値: {'; '.join(_bad208)} — "
         "Schema.org freshness signal 破壊。strict YYYY-MM-DD に揃えよ"
         if _bad208 else
         "Check 208: JSON-LD date field 0 件 — vacuous-gate"),
        blocking=True,
    )
else:
    check(False, "Check 208: index.html present",
          "Check 208: index.html が無い", blocking=True)

# ── 209. JSON-LD potentialAction target shares canonical URL prefix (BLOCKING) ─
# index.html 静的 JSON-LD 内の全 `potentialAction` block の `target` URL が
# canonical URL prefix で始まることを BLOCKING 強制。drift は SILENT に AI/voice
# assistant の action を間違った page (404 等) へ誘導。Check 153/171 の
# potentialAction.target 軸版。
_idx209 = ROOT / "index.html"
if _idx209.exists():
    _isrc209 = _idx209.read_text(encoding="utf-8")
    _canon209_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc209
    )
    _canon209 = _canon209_m.group(1) if _canon209_m else None
    # find each potentialAction block scope (from `"potentialAction":` to next
    # closing `}` at the same indent — approx via lookahead of ~600 chars).
    _drifts209: list[str] = []
    _target_count209 = 0
    for _m in re.finditer(r'"potentialAction":', _isrc209):
        _scope = _isrc209[_m.start():_m.start() + 1500]
        for _t in re.finditer(r'"target":\s*(?:\[([^\]]*)\]|"([^"]+)")', _scope):
            if _t.group(1) is not None:
                # array form: extract each quoted URL
                for _u in re.findall(r'"([^"]+)"', _t.group(1)):
                    _target_count209 += 1
                    if _canon209 and not _u.startswith(_canon209):
                        _drifts209.append(f"target={_u!r}")
            else:
                _u = _t.group(2)
                _target_count209 += 1
                if _canon209 and not _u.startswith(_canon209):
                    _drifts209.append(f"target={_u!r}")
            break  # only first target per potentialAction block
    _ok209 = (
        _canon209 is not None
        and _target_count209 > 0
        and not _drifts209
    )
    check(
        _ok209,
        f"Check 209: potentialAction.target {_target_count209} 件全て canonical prefix {_canon209!r} で始まる",
        (f"Check 209: potentialAction.target drift: {_drifts209!r} ≠ canonical prefix "
         f"{_canon209!r} — AI/voice assistant action が wrong page 誘導 (404)。"
         "target URL を canonical 配下に揃えよ"
         if _drifts209 else
         "Check 209: canonical / potentialAction.target 抽出不可 / 0 件"),
        blocking=True,
    )
else:
    check(False, "Check 209: index.html present",
          "Check 209: index.html が無い", blocking=True)

# ── 210. manifest.webmanifest start_url / scope == canonical pathname (BLOCKING) ─
# index.html `<link rel=canonical>` href の pathname (例 /portfolio/) と
# manifest.webmanifest の start_url / scope が一致することを BLOCKING 強制。drift は
# SILENT に PWA install が canonical URL とは別の URL を home に持つことになり、
# entity authority が二分される (AI/search は canonical を entity 識別子とする)。
from urllib.parse import urlparse as _urlparse210
_idx210 = ROOT / "index.html"
_mani210 = ROOT / "manifest.webmanifest"
if _idx210.exists() and _mani210.exists():
    _isrc210 = _idx210.read_text(encoding="utf-8")
    _canon210_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc210
    )
    _canon210 = _canon210_m.group(1) if _canon210_m else None
    _canon_path210 = _urlparse210(_canon210).path if _canon210 else None
    try:
        _mdata210 = json.loads(_mani210.read_text(encoding="utf-8"))
    except json.JSONDecodeError as _e:
        _mdata210 = None
        _parse_err210: str | None = str(_e)
    else:
        _parse_err210 = None
    _start210 = _mdata210.get("start_url") if isinstance(_mdata210, dict) else None
    _scope210 = _mdata210.get("scope") if isinstance(_mdata210, dict) else None
    _drifts210: list[str] = []
    if _canon_path210 is None:
        _drifts210.append("canonical pathname 抽出不可")
    if _parse_err210:
        _drifts210.append(f"manifest JSON parse 失敗: {_parse_err210}")
    if _start210 is None:
        _drifts210.append("start_url 欠落")
    elif _canon_path210 and _start210 != _canon_path210:
        _drifts210.append(f"start_url={_start210!r} != canonical pathname={_canon_path210!r}")
    if _scope210 is None:
        _drifts210.append("scope 欠落")
    elif _canon_path210 and _scope210 != _canon_path210:
        _drifts210.append(f"scope={_scope210!r} != canonical pathname={_canon_path210!r}")
    _ok210 = not _drifts210
    check(
        _ok210,
        f"Check 210: manifest.webmanifest start_url={_start210!r} / scope={_scope210!r} == canonical pathname={_canon_path210!r}",
        (f"Check 210: manifest drift: {_drifts210!r} — PWA install が canonical URL "
         "と異なる URL を home にし entity authority が二分。manifest.webmanifest の "
         "start_url / scope を canonical pathname (例 /portfolio/) に揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 210: index.html + manifest.webmanifest present",
          "Check 210: index.html もしくは manifest.webmanifest が無い", blocking=True)

# ── 211. JSON-LD contentUrl / thumbnailUrl share canonical URL prefix (BLOCKING) ─
# index.html 静的 JSON-LD 内の全 `contentUrl` / `thumbnailUrl` 値が canonical URL
# prefix で始まることを BLOCKING 強制。drift は SILENT に AI/SEO crawler へ
# non-canonical な asset URL を流し authority を二分。Check 153/171/209 と同
# canonical-prefix family の JSON-LD media-asset 軸版。
_idx211 = ROOT / "index.html"
if _idx211.exists():
    _isrc211 = _idx211.read_text(encoding="utf-8")
    _canon211_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc211
    )
    _canon211 = _canon211_m.group(1) if _canon211_m else None
    _url_fields211 = ["contentUrl", "thumbnailUrl"]
    _urls211: list[tuple[str, str]] = []
    for _fld in _url_fields211:
        for _m in re.finditer(rf'"{_fld}":\s*"([^"]+)"', _isrc211):
            _urls211.append((_fld, _m.group(1)))
    _drifts211: list[str] = []
    if _canon211:
        for _fld, _v in _urls211:
            if not _v.startswith(_canon211):
                _drifts211.append(f"{_fld}={_v!r}")
    _ok211 = (
        _canon211 is not None
        and len(_urls211) > 0
        and not _drifts211
    )
    check(
        _ok211,
        f"Check 211: JSON-LD contentUrl/thumbnailUrl {len(_urls211)} 件全て canonical prefix {_canon211!r} で始まる",
        (f"Check 211: JSON-LD media-asset URL drift: {_drifts211!r} ≠ canonical "
         f"prefix {_canon211!r} — AI/SEO crawler が non-canonical asset URL を取得し "
         "entity authority が二分。contentUrl / thumbnailUrl を canonical 配下に揃えよ"
         if _drifts211 else
         "Check 211: canonical / contentUrl/thumbnailUrl 抽出不可 / 0 件"),
        blocking=True,
    )
else:
    check(False, "Check 211: index.html present",
          "Check 211: index.html が無い", blocking=True)

# ── 212. manifest.webmanifest icons src canonical pathname + 実在 (BLOCKING) ───
# manifest.webmanifest の全 `icons[].src` が canonical URL pathname (例 /portfolio/)
# で始まること + pathname を strip して repo root へ map した path が実在することを
# BLOCKING 強制。drift は SILENT に PWA install が icon を 404 で取得失敗。
from urllib.parse import urlparse as _urlparse212
_idx212 = ROOT / "index.html"
_mani212 = ROOT / "manifest.webmanifest"
if _idx212.exists() and _mani212.exists():
    _isrc212 = _idx212.read_text(encoding="utf-8")
    _canon212_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc212
    )
    _canon212 = _canon212_m.group(1) if _canon212_m else None
    _canon_path212 = _urlparse212(_canon212).path if _canon212 else None
    try:
        _mdata212 = json.loads(_mani212.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        _mdata212 = None
    _icons212 = (
        _mdata212.get("icons", []) if isinstance(_mdata212, dict) else []
    )
    _icon_srcs212 = [
        _ic.get("src") for _ic in _icons212
        if isinstance(_ic, dict) and isinstance(_ic.get("src"), str)
    ]
    _drifts212: list[str] = []
    if not _canon_path212:
        _drifts212.append("canonical pathname 抽出不可")
    if not _icon_srcs212:
        _drifts212.append("icons[].src 0 件")
    for _src in _icon_srcs212:
        if _canon_path212 and not _src.startswith(_canon_path212):
            _drifts212.append(f"src={_src!r} canonical pathname {_canon_path212!r} 不一致")
            continue
        if _canon_path212:
            _rel = _src[len(_canon_path212):]
            _f = ROOT / _rel
            if not _f.exists():
                _drifts212.append(f"src={_src!r} → {_rel!r} がリポジトリに無い")
    _ok212 = not _drifts212
    check(
        _ok212,
        f"Check 212: manifest icons[].src {len(_icon_srcs212)} 件全て canonical pathname {_canon_path212!r} prefix かつ実在",
        (f"Check 212: manifest icons drift: {_drifts212!r} — PWA install が "
         "icon を 404 で取得失敗。icons[].src を canonical pathname + 実在 file へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 212: index.html + manifest.webmanifest present",
          "Check 212: index.html もしくは manifest.webmanifest が無い", blocking=True)

# ── 213. <link rel=icon/apple-touch-icon> href canonical pathname (BLOCKING) ──
# index.html の <link rel="icon"> / <link rel="apple-touch-icon"> の href
# (non-data: のみ) が canonical URL pathname (例 /portfolio/) で始まることを
# BLOCKING 強制。drift は SILENT に production GitHub Pages で 404。
from urllib.parse import urlparse as _urlparse213
_idx213 = ROOT / "index.html"
if _idx213.exists():
    _isrc213 = _idx213.read_text(encoding="utf-8")
    _canon213_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc213
    )
    _canon213 = _canon213_m.group(1) if _canon213_m else None
    _canon_path213 = _urlparse213(_canon213).path if _canon213 else None
    _hrefs213: list[tuple[str, str]] = []
    for _m in re.finditer(
        r'<link\s+rel=["\'](icon|apple-touch-icon)["\'][^>]*\shref=["\']([^"\']+)["\']',
        _isrc213,
    ):
        _hrefs213.append((_m.group(1), _m.group(2)))
    # also handle type=...; rel between attributes
    for _m in re.finditer(
        r'<link\s+rel=["\'](icon|apple-touch-icon)["\'][^>]*?\stype=["\'][^"\']+["\'][^>]*?\shref=["\']([^"\']+)["\']',
        _isrc213,
    ):
        if (_m.group(1), _m.group(2)) not in _hrefs213:
            _hrefs213.append((_m.group(1), _m.group(2)))
    _drifts213: list[str] = []
    if not _canon_path213:
        _drifts213.append("canonical pathname 抽出不可")
    _non_data213 = [(_r, _h) for _r, _h in _hrefs213 if not _h.startswith("data:")]
    if not _non_data213:
        _drifts213.append("非 data: な <link rel=icon/apple-touch-icon> 0 件")
    for _r, _h in _non_data213:
        if _canon_path213 and not _h.startswith(_canon_path213):
            _drifts213.append(f"<link rel={_r}> href={_h!r} canonical pathname {_canon_path213!r} 不一致")
    _ok213 = not _drifts213
    check(
        _ok213,
        f"Check 213: <link rel=icon/apple-touch-icon> non-data: href {len(_non_data213)} 件全て canonical pathname {_canon_path213!r} prefix",
        (f"Check 213: <link rel=icon/apple-touch-icon> href drift: {_drifts213!r} — "
         "production GitHub Pages で 404 化。canonical pathname prefix へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 213: index.html present",
          "Check 213: index.html が無い", blocking=True)

# ── 214. JSON-LD sameAs URLs all HTTPS (BLOCKING) ─────────────────────────────
# index.html 静的 JSON-LD 内の全 `sameAs` array の URL が `https://` で始まることを
# BLOCKING 強制。drift は SILENT に AI/SEO の authenticity-grade を下げる
# (mixed-content / 認証低下)。Check 206 (@id HTTPS) / Check 207 (HTML src/href HTTPS)
# の sameAs external-link 軸版。
_idx214 = ROOT / "index.html"
if _idx214.exists():
    _isrc214 = _idx214.read_text(encoding="utf-8")
    _same_arrays214 = re.findall(r'"sameAs":\s*\[([^\]]*)\]', _isrc214)
    _urls214: list[str] = []
    for _arr in _same_arrays214:
        for _u in re.findall(r'"([^"]+)"', _arr):
            _urls214.append(_u)
    _bad214 = [u for u in _urls214 if not u.startswith("https://")]
    _ok214 = len(_urls214) > 0 and not _bad214
    check(
        _ok214,
        f"Check 214: JSON-LD sameAs URL {len(_urls214)} 件全て HTTPS",
        (f"Check 214: JSON-LD sameAs に non-HTTPS URL: {_bad214!r} — "
         "AI/SEO authenticity-grade 劣化。https:// へ揃えよ"
         if _bad214 else
         "Check 214: JSON-LD sameAs URL 抽出不可 / 0 件"),
        blocking=True,
    )
else:
    check(False, "Check 214: index.html present",
          "Check 214: index.html が無い", blocking=True)

# ── 215. ai:last-modified + SITE_CONFIG.LAST_UPDATED strict ISO-8601 (BLOCKING) ─
# index.html `<meta name="ai:last-modified">` content と main.js
# SITE_CONFIG.LAST_UPDATED が strict ISO-8601 (YYYY-MM-DD regex + 実在カレンダー日付)
# であることを BLOCKING 強制。Check 180 は両者の byte-equality を見るが、両方が
# 同時に非 ISO format へ drift する可能性は別 invariant。format drift は SILENT に
# AI/SEO crawler の recency-weighted retrieval を corruption (parse 失敗 / 誤 parse)。
from datetime import date as _date215
_idx215 = ROOT / "index.html"
_main215 = ROOT / "main.js"
if _idx215.exists() and _main215.exists():
    _isrc215 = _idx215.read_text(encoding="utf-8")
    _msrc215 = _main215.read_text(encoding="utf-8")
    _ai_lm215_m = re.search(
        r'<meta\s+name=["\']ai:last-modified["\']\s+content=["\']([^"\']+)["\']', _isrc215
    )
    _site_lm215_m = re.search(
        r"LAST_UPDATED:\s*['\"]([^'\"]+)['\"]", _msrc215
    )
    _ai_lm215 = _ai_lm215_m.group(1) if _ai_lm215_m else None
    _site_lm215 = _site_lm215_m.group(1) if _site_lm215_m else None
    _bad215: list[str] = []
    for _label, _v in (("ai:last-modified", _ai_lm215), ("SITE_CONFIG.LAST_UPDATED", _site_lm215)):
        if _v is None:
            _bad215.append(f"{_label}=抽出不可")
            continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", _v):
            _bad215.append(f"{_label}={_v!r} (format)")
            continue
        try:
            _y, _mo, _d = _v.split("-")
            _date215(int(_y), int(_mo), int(_d))
        except (ValueError, TypeError) as _e:
            _bad215.append(f"{_label}={_v!r} ({_e})")
    _ok215 = not _bad215
    check(
        _ok215,
        f"Check 215: ai:last-modified={_ai_lm215!r} / SITE_CONFIG.LAST_UPDATED={_site_lm215!r} 共に strict ISO-8601 YYYY-MM-DD",
        (f"Check 215: ISO-8601 drift: {_bad215!r} — AI/SEO recency 信号が "
         "parse 失敗 / 誤 parse に corruption。strict YYYY-MM-DD へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 215: index.html + main.js present",
          "Check 215: index.html もしくは main.js が無い", blocking=True)

# ── 216. JSON-LD @id cross-references resolve (referential integrity) (BLOCKING) ─
# index.html 静的 JSON-LD 内の参照系 property (author/about/isPartOf/mainEntity/
# creator/reviewedBy/publisher/primaryImageOfPage) の `{"@id": "..."}` 参照が、
# 同じ graph 内のどこかで `@type` + `@id` を持つ node により定義されていることを
# BLOCKING 強制。drift は SILENT に entity graph を断片化 — AI/知識グラフ consumer
# が dead anchor を踏み Person/WebSite/WebPage/Organization 主張の linkage が壊れる。
_REF_PROPS216 = {
    "author", "about", "isPartOf", "mainEntity", "creator",
    "reviewedBy", "publisher", "primaryImageOfPage",
}
_idx216 = ROOT / "index.html"
if _idx216.exists():
    _isrc216 = _idx216.read_text(encoding="utf-8")
    _blocks216 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc216,
        flags=re.DOTALL,
    )
    _defined_ids216: set[str] = set()
    _ref_ids216: list[tuple[str, str]] = []
    def _walk216(node: object, parent_key: str | None = None) -> None:
        if isinstance(node, dict):
            _is_def = "@type" in node and "@id" in node and isinstance(node.get("@id"), str)
            if _is_def:
                _defined_ids216.add(node["@id"])
            # reference: object containing ONLY @id (or @id + minor) appearing under ref-prop
            if (
                parent_key in _REF_PROPS216
                and "@id" in node
                and "@type" not in node
                and isinstance(node.get("@id"), str)
            ):
                _ref_ids216.append((parent_key, node["@id"]))
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk216(item, k)
                else:
                    _walk216(v, k)
        elif isinstance(node, list):
            for item in node:
                _walk216(item, parent_key)
    for _blk in _blocks216:
        try:
            _data216 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk216(_data216)
    _dangling216 = [
        f"{_prop}:{_rid}" for _prop, _rid in _ref_ids216
        if _rid not in _defined_ids216
    ]
    _ok216 = len(_ref_ids216) > 0 and not _dangling216
    check(
        _ok216,
        f"Check 216: JSON-LD 参照 @id {len(_ref_ids216)} 件全て graph 内 defined @id ({len(_defined_ids216)} 個) に解決",
        (f"Check 216: dangling @id 参照: {_dangling216!r} — entity graph が断片化し "
         "AI/知識グラフが dead anchor を踏む。参照先 node を JSON-LD 内に定義するか参照を訂正せよ"
         if _dangling216 else
         "Check 216: JSON-LD 参照 @id 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 216: index.html present",
          "Check 216: index.html が無い", blocking=True)

# ── 217. JSON-LD @id definitions are unique within each @graph (BLOCKING) ─────
# index.html 静的 JSON-LD の各 `<script type=application/ld+json>` block 内の
# top-level `@graph` 配列で、`@type` + `@id` を持つ defining node が同一 @id を
# 重複宣言しないことを BLOCKING 強制 (block を跨いだ context-redundant な Person
# 再定義は許容)。同一 graph 内の重複は SILENT に AI/知識グラフ consumer の参照解決を
# 非決定化。Check 216 (referential integrity) の sibling。
_idx217 = ROOT / "index.html"
if _idx217.exists():
    _isrc217 = _idx217.read_text(encoding="utf-8")
    _blocks217 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc217,
        flags=re.DOTALL,
    )
    from collections import Counter as _Counter217
    _all_dupes217: list[str] = []
    _total_ids217 = 0
    for _bi, _blk in enumerate(_blocks217):
        try:
            _data217 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        # top-level @graph 配列の最上位 element だけ確認 (nested embedded entities は
        # context-redundant とみなし許容)
        _graph217 = _data217.get("@graph") if isinstance(_data217, dict) else None
        if not isinstance(_graph217, list):
            continue
        _ids = []
        for _node in _graph217:
            if (
                isinstance(_node, dict)
                and "@type" in _node
                and isinstance(_node.get("@id"), str)
            ):
                _ids.append(_node["@id"])
        _total_ids217 += len(_ids)
        for _id, _n in _Counter217(_ids).items():
            if _n > 1:
                _all_dupes217.append(f"block{_bi}:{_id}×{_n}")
    _ok217 = _total_ids217 > 0 and not _all_dupes217
    check(
        _ok217,
        f"Check 217: JSON-LD @graph top-level defining @id {_total_ids217} 件 全て block 内 unique",
        (f"Check 217: 同一 @graph 内重複 @id: {_all_dupes217!r} — AI/知識グラフが "
         "参照を非決定的に解決。同一 block 内では @id を unique へ揃えよ"
         if _all_dupes217 else
         "Check 217: JSON-LD @graph top-level defining @id 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 217: index.html present",
          "Check 217: index.html が無い", blocking=True)

# ── 218. JSON-LD datePublished <= dateModified per node (BLOCKING) ────────────
# index.html 静的 JSON-LD で datePublished + dateModified を両方持つ node の
# datePublished <= dateModified を BLOCKING 強制。drift は SILENT に AI/SEO crawler
# が "publish 前に modify された" 矛盾信号を取得し recency/trust が破壊。Check 208
# (ISO-8601 format) の date 順序 semantic 軸版。
from datetime import date as _date218
_idx218 = ROOT / "index.html"
if _idx218.exists():
    _isrc218 = _idx218.read_text(encoding="utf-8")
    _blocks218 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc218,
        flags=re.DOTALL,
    )
    _violations218: list[str] = []
    _checked_pairs218 = 0
    def _walk218(node: object, path: str) -> None:
        global _checked_pairs218
        if isinstance(node, dict):
            _dp = node.get("datePublished")
            _dm = node.get("dateModified")
            if isinstance(_dp, str) and isinstance(_dm, str):
                try:
                    _dp_d = _date218.fromisoformat(_dp[:10])
                    _dm_d = _date218.fromisoformat(_dm[:10])
                    _checked_pairs218 += 1
                    if _dp_d > _dm_d:
                        _violations218.append(
                            f"{path}: datePublished={_dp!r} > dateModified={_dm!r}"
                        )
                except ValueError:
                    pass  # Check 208 が format violation を担当
            for k, v in node.items():
                _walk218(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk218(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks218):
        try:
            _data218 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk218(_data218, f"block{_bi}")
    _ok218 = _checked_pairs218 > 0 and not _violations218
    check(
        _ok218,
        f"Check 218: JSON-LD datePublished <= dateModified — {_checked_pairs218} 件全て OK",
        (f"Check 218: 順序違反: {_violations218!r} — AI/SEO crawler が 'publish 前に "
         "modify' 矛盾信号を取得し recency/trust 破壊。datePublished <= dateModified を満たすよう揃えよ"
         if _violations218 else
         "Check 218: datePublished+dateModified 両備の node 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 218: index.html present",
          "Check 218: index.html が無い", blocking=True)

# ── 219. aio-manifest.json paths ⊆ check_aio_digests.py MANIFEST_PATH_TO_LOCAL (BLOCKING) ─
# aio-manifest.json の `source_of_truth` / `supporting_evidence` /
# `observational_evidence` の全 `path` が check_aio_digests.py の
# `MANIFEST_PATH_TO_LOCAL` dict の key に登録されていることを BLOCKING 強制。
# 未登録 path は digest 検証されず、aio-guardian が新 evidence を manifest へ追加
# しても check_aio_digests に登録忘れがあれば silent に digest gap が生じる。
_mani219 = ROOT / ".well-known" / "aio-manifest.json"
_chk_aio219 = ROOT / ".github" / "scripts" / "check_aio_digests.py"
if _mani219.exists() and _chk_aio219.exists():
    try:
        _mdata219 = json.loads(_mani219.read_text(encoding="utf-8"))
    except json.JSONDecodeError as _e:
        _mdata219 = None
        _err219: str | None = str(_e)
    else:
        _err219 = None
    _declared219: list[str] = []
    if isinstance(_mdata219, dict):
        for _sec in ("source_of_truth", "supporting_evidence", "observational_evidence"):
            _entries = _mdata219.get(_sec, [])
            if isinstance(_entries, list):
                for _e in _entries:
                    if isinstance(_e, dict) and isinstance(_e.get("path"), str):
                        _declared219.append(_e["path"])
    _chksrc219 = _chk_aio219.read_text(encoding="utf-8")
    # MANIFEST_PATH_TO_LOCAL 内の key 文字列を抽出 (key の literal "..."" のみ)
    _map_block219_m = re.search(
        r"MANIFEST_PATH_TO_LOCAL:[^=]*=\s*\{(.*?)\}", _chksrc219, flags=re.DOTALL
    )
    _registered219: set[str] = set()
    if _map_block219_m:
        for _km in re.finditer(r'^\s*"([^"]+)":', _map_block219_m.group(1), flags=re.M):
            _registered219.add(_km.group(1))
    _missing219 = [p for p in _declared219 if p not in _registered219]
    _ok219 = (
        _err219 is None
        and len(_declared219) > 0
        and bool(_registered219)
        and not _missing219
    )
    check(
        _ok219,
        f"Check 219: aio-manifest declared paths ({len(_declared219)} 件) 全て check_aio_digests MANIFEST_PATH_TO_LOCAL ({len(_registered219)} 件) に登録",
        (f"Check 219: 未登録 path: {_missing219!r}"
         f" / manifest parse error: {_err219!r}"
         " — check_aio_digests.py で digest 検証されず silent gap。"
         "MANIFEST_PATH_TO_LOCAL に追加せよ"),
        blocking=True,
    )
else:
    check(False, "Check 219: aio-manifest.json + check_aio_digests.py present",
          "Check 219: aio-manifest.json もしくは check_aio_digests.py が無い", blocking=True)

# ── 220. manifest.webmanifest lang == <html lang> (BLOCKING) ──────────────────
# manifest.webmanifest `lang` field と index.html `<html lang>` attribute が
# strict 一致することを BLOCKING 強制。drift は SILENT に PWA install で OS/screen
# reader/AI/SEO consumer に異なる言語信号を流す。Check 152 (<html lang> ↔
# JSON-LD inLanguage) / Check 187 (og:locale ↔ <html lang>) の manifest install 軸版。
_idx220 = ROOT / "index.html"
_mani220 = ROOT / "manifest.webmanifest"
if _idx220.exists() and _mani220.exists():
    _isrc220 = _idx220.read_text(encoding="utf-8")
    _html_lang220_m = re.search(r'<html\s+lang=["\']([^"\']+)["\']', _isrc220)
    _html_lang220 = _html_lang220_m.group(1) if _html_lang220_m else None
    try:
        _mdata220 = json.loads(_mani220.read_text(encoding="utf-8"))
    except json.JSONDecodeError as _e220:
        _mdata220 = None
    _mani_lang220 = _mdata220.get("lang") if isinstance(_mdata220, dict) else None
    _ok220 = (
        _html_lang220 is not None
        and _mani_lang220 is not None
        and _html_lang220 == _mani_lang220
    )
    check(
        _ok220,
        f"Check 220: manifest.lang={_mani_lang220!r} == <html lang>={_html_lang220!r}",
        (f"Check 220: language drift: manifest.lang={_mani_lang220!r}, "
         f"<html lang>={_html_lang220!r} — PWA install と HTML render で言語信号が "
         "split。manifest.lang を <html lang> と同一値へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 220: index.html + manifest.webmanifest present",
          "Check 220: index.html もしくは manifest.webmanifest が無い", blocking=True)

# ── 221. JSON-LD image / primaryImageOfPage refs resolve to ImageObject (BLOCKING) ─
# index.html 静的 JSON-LD で `image` / `primaryImageOfPage` の `{"@id":...}` 参照が、
# 同 graph 内で `@type == "ImageObject"` の node に解決することを BLOCKING 強制。
# Check 216 (referential integrity) に「参照先 @type が ImageObject」の type-safety を追加。
# drift は SILENT に AI/SEO consumer が non-image entity を image slot で取得し、
# image-card rendering / OG preview / 知識グラフ image extraction を破壊。
_idx221 = ROOT / "index.html"
if _idx221.exists():
    _isrc221 = _idx221.read_text(encoding="utf-8")
    _blocks221 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc221,
        flags=re.DOTALL,
    )
    _IMAGE_REF_PROPS221 = {"image", "primaryImageOfPage"}
    _typeof221: dict[str, str] = {}
    _img_refs221: list[tuple[str, str]] = []
    def _walk221(node: object, parent_key: str | None = None) -> None:
        if isinstance(node, dict):
            _t = node.get("@type")
            _id = node.get("@id")
            if isinstance(_t, str) and isinstance(_id, str):
                _typeof221[_id] = _t
            if (
                parent_key in _IMAGE_REF_PROPS221
                and isinstance(_id, str)
                and "@type" not in node
            ):
                _img_refs221.append((parent_key, _id))
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk221(item, k)
                else:
                    _walk221(v, k)
        elif isinstance(node, list):
            for item in node:
                _walk221(item, parent_key)
    for _blk in _blocks221:
        try:
            _data221 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk221(_data221)
    _wrong_type221: list[str] = []
    for _prop, _rid in _img_refs221:
        _resolved_type = _typeof221.get(_rid)
        if _resolved_type != "ImageObject":
            _wrong_type221.append(f"{_prop}@id={_rid}: type={_resolved_type!r}")
    _ok221 = len(_img_refs221) > 0 and not _wrong_type221
    check(
        _ok221,
        f"Check 221: JSON-LD image/primaryImageOfPage refs {len(_img_refs221)} 件全て ImageObject @type へ解決",
        (f"Check 221: type 不一致 image refs: {_wrong_type221!r} — AI/SEO が "
         "non-image entity を image slot で取得し card rendering 破壊。"
         "参照先 node の @type を ImageObject へ揃えるか refs を訂正せよ"
         if _wrong_type221 else
         "Check 221: image/primaryImageOfPage refs 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 221: index.html present",
          "Check 221: index.html が無い", blocking=True)

# ── 222. JSON-LD author/creator/reviewedBy/copyrightHolder/employee refs Person|Organization (BLOCKING) ─
# index.html 静的 JSON-LD で `author` / `creator` / `reviewedBy` /
# `copyrightHolder` / `employee` の `{"@id":...}` 参照が、同 graph 内で
# `@type in {Person, Organization}` の node に解決することを BLOCKING 強制。
# Check 221 (image-slot type safety) の agent-slot 軸版。drift は SILENT に
# AI/SEO consumer が著者帰属を image や website へ誤帰属し knowledge-graph 攻撃。
_AGENT_REF_PROPS222 = {
    "author", "creator", "reviewedBy", "copyrightHolder", "employee",
}
_AGENT_OK_TYPES222 = {"Person", "Organization"}
_idx222 = ROOT / "index.html"
if _idx222.exists():
    _isrc222 = _idx222.read_text(encoding="utf-8")
    _blocks222 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc222,
        flags=re.DOTALL,
    )
    _typeof222: dict[str, str] = {}
    _agent_refs222: list[tuple[str, str]] = []
    def _walk222(node: object, parent_key: str | None = None) -> None:
        if isinstance(node, dict):
            _t = node.get("@type")
            _id = node.get("@id")
            if isinstance(_t, str) and isinstance(_id, str):
                _typeof222[_id] = _t
            if (
                parent_key in _AGENT_REF_PROPS222
                and isinstance(_id, str)
                and "@type" not in node
            ):
                _agent_refs222.append((parent_key, _id))
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk222(item, k)
                else:
                    _walk222(v, k)
        elif isinstance(node, list):
            for item in node:
                _walk222(item, parent_key)
    for _blk in _blocks222:
        try:
            _data222 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk222(_data222)
    _wrong_type222: list[str] = []
    for _prop, _rid in _agent_refs222:
        _resolved_type = _typeof222.get(_rid)
        if _resolved_type not in _AGENT_OK_TYPES222:
            _wrong_type222.append(f"{_prop}@id={_rid}: type={_resolved_type!r}")
    _ok222 = len(_agent_refs222) > 0 and not _wrong_type222
    check(
        _ok222,
        f"Check 222: JSON-LD agent-slot refs {len(_agent_refs222)} 件全て Person|Organization へ解決",
        (f"Check 222: type 不一致 agent refs: {_wrong_type222!r} — AI/SEO で "
         "著者帰属が non-agent entity に誤帰属し knowledge-graph 破壊。"
         "参照先 node の @type を Person|Organization へ揃えるか refs を訂正せよ"
         if _wrong_type222 else
         "Check 222: agent-slot refs 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 222: index.html present",
          "Check 222: index.html が無い", blocking=True)

# ── 223. JSON-LD isPartOf refs resolve to WebSite|WebPage|CreativeWork (BLOCKING) ─
# index.html 静的 JSON-LD で `isPartOf` の `{"@id":...}` 参照が、同 graph 内で
# `@type in {WebSite, WebPage, CreativeWork}` の node に解決することを BLOCKING 強制。
# Check 221 (image-slot) / Check 222 (agent-slot) の isPartOf 構造軸版。
_ISPARTOF_OK_TYPES223 = {"WebSite", "WebPage", "CreativeWork"}
_idx223 = ROOT / "index.html"
if _idx223.exists():
    _isrc223 = _idx223.read_text(encoding="utf-8")
    _blocks223 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc223,
        flags=re.DOTALL,
    )
    _typeof223: dict[str, str] = {}
    _ip_refs223: list[str] = []
    def _walk223(node: object, parent_key: str | None = None) -> None:
        if isinstance(node, dict):
            _t = node.get("@type")
            _id = node.get("@id")
            if isinstance(_t, str) and isinstance(_id, str):
                _typeof223[_id] = _t
            if (
                parent_key == "isPartOf"
                and isinstance(_id, str)
                and "@type" not in node
            ):
                _ip_refs223.append(_id)
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk223(item, k)
                else:
                    _walk223(v, k)
        elif isinstance(node, list):
            for item in node:
                _walk223(item, parent_key)
    for _blk in _blocks223:
        try:
            _data223 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk223(_data223)
    _wrong_type223: list[str] = []
    for _rid in _ip_refs223:
        _resolved_type = _typeof223.get(_rid)
        if _resolved_type not in _ISPARTOF_OK_TYPES223:
            _wrong_type223.append(f"isPartOf@id={_rid}: type={_resolved_type!r}")
    _ok223 = len(_ip_refs223) > 0 and not _wrong_type223
    check(
        _ok223,
        f"Check 223: JSON-LD isPartOf refs {len(_ip_refs223)} 件全て WebSite|WebPage|CreativeWork へ解決",
        (f"Check 223: type 不一致 isPartOf refs: {_wrong_type223!r} — AI/SEO が "
         "page/article を非構造 entity へ contain させ階層が破壊。"
         "参照先 node の @type を WebSite|WebPage|CreativeWork へ揃えるか refs を訂正せよ"
         if _wrong_type223 else
         "Check 223: isPartOf refs 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 223: index.html present",
          "Check 223: index.html が無い", blocking=True)

# ── 224. <meta name=description> content length in [30, 300] (BLOCKING) ───────
# index.html `<meta name="description">` content の character length が
# SEO-sane band [30, 300] であることを BLOCKING 強制。<30 = SERP snippet preview
# 抑制 (短すぎ抽出不能) / >300 = 静かに truncate (...)。Check 154 (presence) を
# 補完する length sanity 軸。
_idx224 = ROOT / "index.html"
if _idx224.exists():
    _isrc224 = _idx224.read_text(encoding="utf-8")
    _desc224_m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', _isrc224
    )
    _desc224 = _desc224_m.group(1) if _desc224_m else None
    _len224 = len(_desc224) if isinstance(_desc224, str) else 0
    _ok224 = _desc224 is not None and 30 <= _len224 <= 300
    check(
        _ok224,
        f"Check 224: <meta name=description> length={_len224} (SEO-sane band [30, 300])",
        (f"Check 224: description length={_len224} (band [30, 300] 違反) — "
         f"{'抽出不能で SERP snippet 抑制' if _len224 < 30 else '300 超えで SERP 末尾 truncate'}。"
         "description 長を band 内へ調整せよ"
         if _desc224 is not None else
         "Check 224: <meta name=description> が無い"),
        blocking=True,
    )
else:
    check(False, "Check 224: index.html present",
          "Check 224: index.html が無い", blocking=True)

# ── 225. <title> content length in [10, 70] (BLOCKING) ────────────────────────
# index.html <title> content の character length が [10, 70] に収まることを
# BLOCKING 強制。<10 = sparse 過ぎ SERP 表示不適 / >70 = SERP で末尾 truncate。
# Check 66 (canonical 名 presence) を補完する length sanity 軸。
_idx225 = ROOT / "index.html"
if _idx225.exists():
    _isrc225 = _idx225.read_text(encoding="utf-8")
    _title225_m = re.search(r"<title>([^<]+)</title>", _isrc225)
    _title225 = _title225_m.group(1) if _title225_m else None
    _len225 = len(_title225) if isinstance(_title225, str) else 0
    _ok225 = _title225 is not None and 10 <= _len225 <= 70
    check(
        _ok225,
        f"Check 225: <title> length={_len225} (SEO-sane band [10, 70])",
        (f"Check 225: title length={_len225} (band [10, 70] 違反) — "
         f"{'sparse 過ぎ SERP 表示不適' if _len225 < 10 else '70 超えで SERP 末尾 truncate'}。"
         "title 長を band 内へ調整せよ"
         if _title225 is not None else
         "Check 225: <title> が無い"),
        blocking=True,
    )
else:
    check(False, "Check 225: index.html present",
          "Check 225: index.html が無い", blocking=True)

# ── 226. og:title [10, 90] + og:description [30, 250] length (BLOCKING) ───────
# index.html `og:title` length [10, 90] / `og:description` length [30, 250] を
# BLOCKING 強制。Facebook/LinkedIn/Slack/Discord の social card preview で
# 短すぎ表示抑制 / 長すぎ silent truncate を阻止。Check 155 (og↔twitter byte-id)
# によって twitter card にも同時適用。Check 224/225 の Open Graph 軸版。
_idx226 = ROOT / "index.html"
if _idx226.exists():
    _isrc226 = _idx226.read_text(encoding="utf-8")
    _og_t226 = re.search(
        r'<meta\s+property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', _isrc226
    )
    _og_d226 = re.search(
        r'<meta\s+property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']', _isrc226
    )
    _bad226: list[str] = []
    if _og_t226:
        _lt = len(_og_t226.group(1))
        if not (10 <= _lt <= 90):
            _bad226.append(f"og:title length={_lt} (band [10, 90] 違反)")
    else:
        _bad226.append("og:title 抽出不可")
    if _og_d226:
        _ld = len(_og_d226.group(1))
        if not (30 <= _ld <= 250):
            _bad226.append(f"og:description length={_ld} (band [30, 250] 違反)")
    else:
        _bad226.append("og:description 抽出不可")
    _ok226 = not _bad226
    check(
        _ok226,
        f"Check 226: og:title length={len(_og_t226.group(1)) if _og_t226 else 0} / "
        f"og:description length={len(_og_d226.group(1)) if _og_d226 else 0} 共に SEO-sane band 内",
        (f"Check 226: og length 違反: {_bad226!r} — "
         "social card preview が短すぎ抑制 / 長すぎ silent truncate。band 内へ調整せよ"),
        blocking=True,
    )
else:
    check(False, "Check 226: index.html present",
          "Check 226: index.html が無い", blocking=True)

# ── 227. JSON-LD Person name == canonical entity name (BLOCKING) ──────────────
# index.html 静的 JSON-LD の全 `"@type": "Person"` node の `name` が
# canonical entity identifier ("Yuta Yokoi" / "横井雄太" / "Yokoi Yuta") の
# いずれかに一致することを BLOCKING 強制。drift は SILENT に AI/SEO の entity
# identity を block 跨ぎで断片化。
_CANONICAL_PERSON_NAMES227 = {"Yuta Yokoi", "横井雄太", "Yokoi Yuta"}
_idx227 = ROOT / "index.html"
if _idx227.exists():
    _isrc227 = _idx227.read_text(encoding="utf-8")
    _blocks227 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc227,
        flags=re.DOTALL,
    )
    _names227: list[str] = []
    def _walk227(node: object) -> None:
        if isinstance(node, dict):
            if node.get("@type") == "Person" and isinstance(node.get("name"), str):
                _names227.append(node["name"])
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk227(item)
                else:
                    _walk227(v)
        elif isinstance(node, list):
            for item in node:
                _walk227(item)
    for _blk in _blocks227:
        try:
            _data227 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk227(_data227)
    _bad227 = [n for n in _names227 if n not in _CANONICAL_PERSON_NAMES227]
    _ok227 = len(_names227) > 0 and not _bad227
    check(
        _ok227,
        f"Check 227: JSON-LD Person.name {len(_names227)} 件全て canonical 名 ('Yuta Yokoi'/'横井雄太'/'Yokoi Yuta') に一致",
        (f"Check 227: 非 canonical Person.name: {_bad227!r} — AI/SEO entity identity "
         "が断片化。canonical 名へ揃えよ"
         if _bad227 else
         "Check 227: Person.name 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 227: index.html present",
          "Check 227: index.html が無い", blocking=True)

# ── 228. sitemap.xml <changefreq> values are spec-valid (BLOCKING) ────────────
# sitemap.xml 全 `<changefreq>` 要素の content が Sitemap Protocol 規定の 7 値
# (always/hourly/daily/weekly/monthly/yearly/never) のいずれかであることを
# BLOCKING 強制。drift (typo / 不正値) は SILENT に crawler が freshness hint を
# 無視 → recrawl scheduling が劣化。
_VALID_CHANGEFREQ228 = {
    "always", "hourly", "daily", "weekly", "monthly", "yearly", "never",
}
_sitemap228 = ROOT / "sitemap.xml"
if _sitemap228.exists():
    _ssrc228 = _sitemap228.read_text(encoding="utf-8")
    _freqs228 = re.findall(r"<changefreq>([^<]+)</changefreq>", _ssrc228)
    _bad228 = [f for f in _freqs228 if f not in _VALID_CHANGEFREQ228]
    _ok228 = len(_freqs228) > 0 and not _bad228
    check(
        _ok228,
        f"Check 228: sitemap.xml changefreq {len(_freqs228)} 件全て spec-valid 値",
        (f"Check 228: spec 外 changefreq: {_bad228!r} — crawler が freshness hint "
         "を無視。Sitemap Protocol 規定値 ({always|hourly|daily|weekly|monthly|yearly|never}) へ揃えよ"
         if _bad228 else
         "Check 228: sitemap.xml <changefreq> 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 228: sitemap.xml present",
          "Check 228: sitemap.xml が無い", blocking=True)

# ── 229. sitemap.xml <priority> values in [0.0, 1.0] (BLOCKING) ───────────────
# sitemap.xml 全 `<priority>` 要素の content が float [0.0, 1.0] にあることを
# BLOCKING 強制。drift (1.5 / "high" / 負値) は spec 違反で crawler が silent に
# default 0.5 へ fallback → priority hint 喪失。Check 228 (changefreq) の priority 軸。
_sitemap229 = ROOT / "sitemap.xml"
if _sitemap229.exists():
    _ssrc229 = _sitemap229.read_text(encoding="utf-8")
    _prios229 = re.findall(r"<priority>([^<]+)</priority>", _ssrc229)
    _bad229: list[str] = []
    for _p in _prios229:
        try:
            _v = float(_p)
        except ValueError:
            _bad229.append(f"{_p!r} (not float)")
            continue
        if not (0.0 <= _v <= 1.0):
            _bad229.append(f"{_p!r} (out of [0.0, 1.0])")
    _ok229 = len(_prios229) > 0 and not _bad229
    check(
        _ok229,
        f"Check 229: sitemap.xml priority {len(_prios229)} 件全て float in [0.0, 1.0]",
        (f"Check 229: spec 外 priority: {_bad229!r} — crawler が default 0.5 へ "
         "fallback し priority hint 喪失。spec 規定 float [0.0, 1.0] へ揃えよ"
         if _bad229 else
         "Check 229: sitemap.xml <priority> 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 229: sitemap.xml present",
          "Check 229: sitemap.xml が無い", blocking=True)

# ── 230. sitemap.xml ちょうど 1 <url> が <priority>1.0</priority> 且つ canonical (BLOCKING) ─
# sitemap.xml の `<priority>1.0</priority>` が含まれる <url> が ちょうど 1 件で、
# その <loc> が canonical URL と一致することを BLOCKING 強制。drift (priority=1.0
# が複数 / non-canonical) は SILENT に「primary entry point」signal を分散させ
# canonical authority を希釈。
_sitemap230 = ROOT / "sitemap.xml"
_idx230 = ROOT / "index.html"
if _sitemap230.exists() and _idx230.exists():
    _ssrc230 = _sitemap230.read_text(encoding="utf-8")
    _isrc230 = _idx230.read_text(encoding="utf-8")
    _canon230_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc230
    )
    _canon230 = _canon230_m.group(1) if _canon230_m else None
    # 各 <url> block を抽出
    _url_blocks230 = re.findall(r"<url>(.*?)</url>", _ssrc230, flags=re.DOTALL)
    _p1_locs230: list[str] = []
    for _ub in _url_blocks230:
        if re.search(r"<priority>\s*1\.0\s*</priority>", _ub):
            _loc_m = re.search(r"<loc>([^<]+)</loc>", _ub)
            if _loc_m:
                _p1_locs230.append(_loc_m.group(1))
    _violations230: list[str] = []
    if _canon230 is None:
        _violations230.append("canonical URL 抽出不可")
    if len(_p1_locs230) != 1:
        _violations230.append(f"priority=1.0 count={len(_p1_locs230)} (expected 1)")
    elif _canon230 and _p1_locs230[0] != _canon230:
        _violations230.append(f"priority=1.0 loc={_p1_locs230[0]!r} != canonical={_canon230!r}")
    _ok230 = not _violations230
    check(
        _ok230,
        f"Check 230: sitemap.xml priority=1.0 が 1 件で canonical URL ({_canon230!r}) に一致",
        (f"Check 230: 違反: {_violations230!r} — 「primary entry point」signal が "
         "分散し canonical authority 希釈。priority=1.0 は canonical homepage 1 件のみへ"),
        blocking=True,
    )
else:
    check(False, "Check 230: sitemap.xml + index.html present",
          "Check 230: sitemap.xml もしくは index.html が無い", blocking=True)

# ── 231. main.js SITE_CONFIG.ROLE_TITLE == canonical role (BLOCKING) ──────────
# main.js SITE_CONFIG.ROLE_TITLE が canonical entity role 3 値 ("AI-Driven PM" /
# "IT Consultant" / "KERNEL Framework Designer") のいずれかに一致することを
# BLOCKING 強制。drift は SILENT に SPA renderer 出力 (title / meta) で entity を誤表現。
_CANONICAL_ROLES231 = {
    "AI-Driven PM", "IT Consultant", "KERNEL Framework Designer",
}
_main231 = ROOT / "main.js"
if _main231.exists():
    _msrc231 = _main231.read_text(encoding="utf-8")
    _role231_m = re.search(r"ROLE_TITLE:\s*['\"]([^'\"]+)['\"]", _msrc231)
    _role231 = _role231_m.group(1) if _role231_m else None
    _ok231 = _role231 is not None and _role231 in _CANONICAL_ROLES231
    check(
        _ok231,
        f"Check 231: SITE_CONFIG.ROLE_TITLE={_role231!r} が canonical role に一致",
        (f"Check 231: SITE_CONFIG.ROLE_TITLE={_role231!r} 非 canonical — "
         "SPA renderer 出力 (title/meta) で entity 役割が誤表現。"
         "{'AI-Driven PM','IT Consultant','KERNEL Framework Designer'} のいずれかへ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 231: main.js present",
          "Check 231: main.js が無い", blocking=True)

# ── 232. <meta name=ai:*> content URLs all HTTPS (BLOCKING) ───────────────────
# index.html `<meta name="ai:...">` content attribute の absolute URL (scheme 付き)
# が全て `https://` で始まることを BLOCKING 強制 (negative invariant)。drift は
# SILENT に AIO routing layer を downgrade し AI crawler が Mixed Content blocking。
_idx232 = ROOT / "index.html"
if _idx232.exists():
    _isrc232 = _idx232.read_text(encoding="utf-8")
    _ai_urls232 = re.findall(
        r'<meta\s+name=["\']ai:[^"\']+["\'][^>]*content=["\'](http://[^"\']+)["\']',
        _isrc232,
    )
    _ok232 = len(_ai_urls232) == 0
    check(
        _ok232,
        "Check 232: <meta name=ai:*> content に http:// 不在 (AIO routing HTTPS guard)",
        (f"Check 232: <meta name=ai:*> content に http:// URL: {_ai_urls232!r} — "
         "AI crawler が Mixed Content blocking で AIO routing 喪失。https:// に揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 232: index.html present",
          "Check 232: index.html が無い", blocking=True)

# ── 233. <meta name=asset:*> content URLs all HTTPS (BLOCKING) ────────────────
# index.html `<meta name="asset:*">` content attribute の absolute URL (scheme 付き)
# が全て `https://` で始まることを BLOCKING 強制 (negative invariant)。Check 232
# (ai:* content HTTPS) の asset:* axis 版。drift は SILENT に AI/SEO crawler が
# asset を Mixed Content blocking で fetch 失敗し authenticity-grade 劣化。
_idx233 = ROOT / "index.html"
if _idx233.exists():
    _isrc233 = _idx233.read_text(encoding="utf-8")
    _asset_urls233 = re.findall(
        r'<meta\s+name=["\']asset:[^"\']+["\'][^>]*content=["\'](http://[^"\']+)["\']',
        _isrc233,
    )
    _ok233 = len(_asset_urls233) == 0
    check(
        _ok233,
        "Check 233: <meta name=asset:*> content に http:// 不在 (AIO asset HTTPS guard)",
        (f"Check 233: <meta name=asset:*> content に http:// URL: {_asset_urls233!r} — "
         "AI/SEO crawler が Mixed Content blocking で asset fetch 失敗、authenticity 劣化。"
         "https:// に揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 233: index.html present",
          "Check 233: index.html が無い", blocking=True)

# ── 234. <meta name=asset:*> content URLs (absolute) share canonical prefix (BLOCKING) ─
# index.html `<meta name="asset:*">` content attribute の absolute URL (http(s):// で
# 始まる値) が canonical URL prefix で始まることを BLOCKING 強制。drift は SILENT に
# AI/SEO へ non-canonical asset URL を流し entity authority を二分。Check 171
# (ai:* canonical prefix) の asset:* 軸版。
_idx234 = ROOT / "index.html"
if _idx234.exists():
    _isrc234 = _idx234.read_text(encoding="utf-8")
    _canon234_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc234
    )
    _canon234 = _canon234_m.group(1) if _canon234_m else None
    _asset_urls234 = re.findall(
        r'<meta\s+name=["\']asset:[^"\']+["\'][^>]*content=["\'](https?://[^"\']+)["\']',
        _isrc234,
    )
    _drifts234: list[str] = []
    if _canon234 is None:
        _drifts234.append("canonical URL 抽出不可")
    if not _asset_urls234:
        _drifts234.append("asset:* 絶対 URL 0 件 — vacuous-fail")
    for _u in _asset_urls234:
        if _canon234 and not _u.startswith(_canon234):
            _drifts234.append(f"asset URL={_u!r} canonical prefix 不一致")
    _ok234 = not _drifts234
    check(
        _ok234,
        f"Check 234: <meta name=asset:*> 絶対 URL {len(_asset_urls234)} 件全て canonical prefix {_canon234!r} で始まる",
        (f"Check 234: drift: {_drifts234!r} — AI/SEO crawler が non-canonical asset を "
         "正規扱いし entity authority 二分。canonical prefix に揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 234: index.html present",
          "Check 234: index.html が無い", blocking=True)

# ── 235. JSON-LD Article/TechArticle with @id has headline+author+datePublished (BLOCKING) ─
# index.html 静的 JSON-LD で `@type in {Article, TechArticle}` かつ `@id` を持つ
# (full definition) node が Schema.org 必須 field (headline + author +
# datePublished) を持つことを BLOCKING 強制。@id 無し (subjectOf/citation の
# 外部 URL 参照) は self-description でないため exempt。drift は Google rich-result
# 失格 + AI search Article snippet 劣化。
_REQUIRED_ARTICLE_FIELDS235 = ("headline", "author", "datePublished")
_idx235 = ROOT / "index.html"
if _idx235.exists():
    _isrc235 = _idx235.read_text(encoding="utf-8")
    _blocks235 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc235,
        flags=re.DOTALL,
    )
    _violations235: list[str] = []
    _full_count235 = 0
    def _walk235(node: object, path: str) -> None:
        global _full_count235
        if isinstance(node, dict):
            _t = node.get("@type")
            if isinstance(_t, str) and _t in ("Article", "TechArticle") and "@id" in node:
                _full_count235 += 1
                _missing = [f for f in _REQUIRED_ARTICLE_FIELDS235 if f not in node]
                if _missing:
                    _violations235.append(f"{path} {_t}@id={node.get('@id')!r}: missing {_missing!r}")
            for k, v in node.items():
                _walk235(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk235(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks235):
        try:
            _data235 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk235(_data235, f"block{_bi}")
    _ok235 = _full_count235 > 0 and not _violations235
    check(
        _ok235,
        f"Check 235: Article/TechArticle full def ({_full_count235} 件) 全て headline+author+datePublished を持つ",
        (f"Check 235: 必須 field 欠落: {_violations235!r} — Google rich-result 失格 + "
         "AI search Article snippet 劣化。Schema.org 必須 field を追加せよ"
         if _violations235 else
         "Check 235: @id 付き Article/TechArticle 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 235: index.html present",
          "Check 235: index.html が無い", blocking=True)

# ── 236. aio-manifest.json generated_at + start_date strict format (BLOCKING) ─
# aio-manifest.json `generated_at` が RFC 3339 (YYYY-MM-DDTHH:MM:SSZ) で
# `entity.affiliation.start_date` が YYYY-MM-DD で実在 datetime/date であることを
# BLOCKING 強制。Check 93 (last_metadata_update format) の generated_at +
# start_date 軸補完。drift は SILENT に recency / 雇用 timeline 信号を corruption。
from datetime import date as _date236, datetime as _dt236
_man236 = ROOT / ".well-known" / "aio-manifest.json"
if _man236.exists():
    try:
        _md236 = json.loads(_man236.read_text(encoding="utf-8"))
    except json.JSONDecodeError as _e236:
        _md236 = None
    _bad236: list[str] = []
    if isinstance(_md236, dict):
        _gen236 = _md236.get("generated_at")
        if not isinstance(_gen236, str):
            _bad236.append(f"generated_at 欠落 / 非 string ({_gen236!r})")
        elif not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", _gen236):
            _bad236.append(f"generated_at={_gen236!r} (format)")
        else:
            try:
                _dt236.strptime(_gen236, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError as _e:
                _bad236.append(f"generated_at={_gen236!r} ({_e})")
        _sd236 = (
            _md236.get("entity", {}).get("affiliation", {}).get("start_date")
            if isinstance(_md236.get("entity"), dict) else None
        )
        if not isinstance(_sd236, str):
            _bad236.append(f"affiliation.start_date 欠落 / 非 string ({_sd236!r})")
        elif not re.match(r"^\d{4}-\d{2}-\d{2}$", _sd236):
            _bad236.append(f"affiliation.start_date={_sd236!r} (format)")
        else:
            try:
                _y, _mo, _d = _sd236.split("-")
                _date236(int(_y), int(_mo), int(_d))
            except (ValueError, TypeError) as _e:
                _bad236.append(f"affiliation.start_date={_sd236!r} ({_e})")
    else:
        _bad236.append("aio-manifest parse 失敗")
    _ok236 = not _bad236
    check(
        _ok236,
        f"Check 236: aio-manifest generated_at + affiliation.start_date 共に strict ISO format",
        (f"Check 236: 違反: {_bad236!r} — recency/雇用 timeline 信号 corruption。"
         "strict ISO format へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 236: aio-manifest.json present",
          "Check 236: aio-manifest.json が無い", blocking=True)

# ── 237. js/*.js leaf modules have ZERO ESM imports (BLOCKING) ────────────────
# js/*.js (および js/quiz/*.js) の全 leaf module が top-level `import` を
# 一切持たないことを BLOCKING 強制 (negative invariant)。main.js のみが orchestrator。
# leaf 間 import = 循環依存の入口・hidden coupling・bundling 複雑化 (C1 違反入口)。
import glob as _glob237
_leaf_paths237 = (
    _glob237.glob(str(ROOT / "js" / "*.js"))
    + _glob237.glob(str(ROOT / "js" / "quiz" / "*.js"))
)
_offenders237: list[str] = []
for _lp in _leaf_paths237:
    try:
        _lsrc = open(_lp, encoding="utf-8").read()
    except (FileNotFoundError, PermissionError):
        continue
    # Strip block comments to avoid false-positive on `import` inside comments
    _stripped = re.sub(r"/\*.*?\*/", "", _lsrc, flags=re.DOTALL)
    _stripped = re.sub(r"^\s*//.*$", "", _stripped, flags=re.M)
    # top-level import statements: `import ... from '...'` or `import '...'`
    if re.search(r"(?:^|\n)\s*import\s+", _stripped):
        _offenders237.append(str(Path(_lp).relative_to(ROOT)))
_ok237 = len(_leaf_paths237) > 0 and not _offenders237
check(
    _ok237,
    f"Check 237: js/ leaf modules {len(_leaf_paths237)} 件全て import 文 0 (zero coupling)",
    (f"Check 237: import 文を持つ leaf module: {_offenders237!r} — "
     "leaf↔leaf coupling で循環依存の入口を作る。main.js 経由のみで orchestrate せよ"
     if _offenders237 else
     "Check 237: leaf module 0 件 — vacuous-fail"),
    blocking=True,
)

# ── 238. HTML head singleton tags appear exactly once (BLOCKING) ──────────────
# index.html の head 内 singleton tag (title / link rel=canonical /
# meta name=description / meta property=og:url / meta property=og:title) が
# それぞれちょうど 1 件で存在することを BLOCKING 強制。複数 instance は SILENT
# に browser/crawler が「first」「last」を非決定的に選び canonical signal を希釈。
_idx238 = ROOT / "index.html"
if _idx238.exists():
    _isrc238 = _idx238.read_text(encoding="utf-8")
    _patterns238 = [
        ("<title>", r"<title>[^<]+</title>"),
        ('<link rel="canonical">', r'<link\s+rel=["\']canonical["\']'),
        ('<meta name="description">', r'<meta\s+name=["\']description["\']'),
        ('<meta property="og:url">', r'<meta\s+property=["\']og:url["\']'),
        ('<meta property="og:title">', r'<meta\s+property=["\']og:title["\']'),
    ]
    _bad238: list[str] = []
    for _label, _pat in _patterns238:
        _n = len(re.findall(_pat, _isrc238))
        if _n != 1:
            _bad238.append(f"{_label} count={_n} (expected 1)")
    _ok238 = not _bad238
    check(
        _ok238,
        f"Check 238: HTML head singleton tags 全て exactly 1 件",
        (f"Check 238: singleton 違反: {_bad238!r} — browser/crawler が非決定的に "
         "選択し canonical signal が希釈。各 head singleton tag を exactly 1 件へ整理"),
        blocking=True,
    )
else:
    check(False, "Check 238: index.html present",
          "Check 238: index.html が無い", blocking=True)

# ── 239. Shipped JS no eval / Function call (BLOCKING) ────────────────────────
# main.js + sw.js + js/**/*.js + root scripts (aio-guard/theme-init/karte-init/
# error-suppressor) に `eval(` / `new Function(` / `Function(` 呼び出しが無いことを
# BLOCKING 強制 (negative invariant)。drift で CSP の 'unsafe-eval' を要求し
# 既存 CSP (Check 115) が reject し runtime 破壊。
_eval_targets239: list[Path] = []
for _p in [ROOT / "main.js", ROOT / "sw.js", ROOT / "aio-guard.js",
           ROOT / "theme-init.js", ROOT / "karte-init.js",
           ROOT / "error-suppressor.js"]:
    if _p.exists():
        _eval_targets239.append(_p)
_eval_targets239 += [Path(p) for p in _glob237.glob(str(ROOT / "js" / "*.js"))]
_eval_targets239 += [Path(p) for p in _glob237.glob(str(ROOT / "js" / "quiz" / "*.js"))]
_offenders239: list[str] = []
_eval_pat239 = re.compile(r"(?:^|[^a-zA-Z0-9_$.])(eval\s*\(|new\s+Function\s*\(|(?<![a-zA-Z0-9_$.])Function\s*\()")
for _p in _eval_targets239:
    try:
        _src = _p.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        continue
    # Strip /* ... */ comments and // ... comments to avoid false-positive on
    # documentation mentions of eval/Function.
    _stripped = re.sub(r"/\*.*?\*/", "", _src, flags=re.DOTALL)
    _stripped = re.sub(r"//[^\n]*", "", _stripped)
    # Also strip string literals (single/double/template) to avoid catching
    # `"eval("` 等 documentation in strings.
    _stripped = re.sub(r"'(?:\\.|[^'\\])*'", "''", _stripped)
    _stripped = re.sub(r'"(?:\\.|[^"\\])*"', '""', _stripped)
    _stripped = re.sub(r"`(?:\\.|[^`\\])*`", "``", _stripped)
    if _eval_pat239.search(_stripped):
        _offenders239.append(str(Path(_p).relative_to(ROOT)))
_ok239 = len(_eval_targets239) > 0 and not _offenders239
check(
    _ok239,
    f"Check 239: shipped JS ({len(_eval_targets239)} 件) に eval/new Function 呼び出し 0",
    (f"Check 239: eval/Function 呼び出しを含む shipped JS: {_offenders239!r} — "
     "CSP 'unsafe-eval' を要求し runtime 破壊 (Check 115 が reject)。除去せよ"
     if _offenders239 else
     "Check 239: shipped JS 0 件 — vacuous-fail"),
    blocking=True,
)

# ── 240. Shipped JS no setTimeout/setInterval string first arg (BLOCKING) ─────
# main.js + sw.js + js/**/*.js + root scripts に setTimeout('...', ...) /
# setInterval('...', ...) のような string 第 1 引数 (eval-equivalent) が無いことを
# BLOCKING 強制 (negative invariant)。Check 239 の timer-callback 軸補完。
_offenders240: list[str] = []
_timer_pat240 = re.compile(r"set(?:Timeout|Interval)\s*\(\s*['\"`]")
for _p in _eval_targets239:  # reuse Check 239 target list
    try:
        _src = _p.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        continue
    _stripped = re.sub(r"/\*.*?\*/", "", _src, flags=re.DOTALL)
    _stripped = re.sub(r"//[^\n]*", "", _stripped)
    if _timer_pat240.search(_stripped):
        _offenders240.append(str(Path(_p).relative_to(ROOT)))
_ok240 = len(_eval_targets239) > 0 and not _offenders240
check(
    _ok240,
    f"Check 240: shipped JS ({len(_eval_targets239)} 件) に setTimeout/setInterval 文字列第 1 引数 0",
    (f"Check 240: 文字列引数 timer を含む shipped JS: {_offenders240!r} — "
     "eval-equivalent semantics で CSP 'unsafe-eval' 要求。第 1 引数を関数に揃えよ"
     if _offenders240 else
     "Check 240: shipped JS 0 件 — vacuous-fail"),
    blocking=True,
)

# ── 241. Shipped JS no document.write / document.writeln (BLOCKING) ───────────
# main.js + sw.js + js/**/*.js + root scripts に `document.write(` /
# `document.writeln(` 呼び出しが 0 であることを BLOCKING 強制 (negative invariant)。
# legacy API: deprecated / HTML5 parser sniff 破壊 / XSS vector / browser intervention 対象。
_offenders241: list[str] = []
_docwrite_pat241 = re.compile(r"document\s*\.\s*write(?:ln)?\s*\(")
for _p in _eval_targets239:  # reuse target list
    try:
        _src = _p.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        continue
    _stripped = re.sub(r"/\*.*?\*/", "", _src, flags=re.DOTALL)
    _stripped = re.sub(r"//[^\n]*", "", _stripped)
    _stripped = re.sub(r"'(?:\\.|[^'\\])*'", "''", _stripped)
    _stripped = re.sub(r'"(?:\\.|[^"\\])*"', '""', _stripped)
    _stripped = re.sub(r"`(?:\\.|[^`\\])*`", "``", _stripped)
    if _docwrite_pat241.search(_stripped):
        _offenders241.append(str(Path(_p).relative_to(ROOT)))
_ok241 = len(_eval_targets239) > 0 and not _offenders241
check(
    _ok241,
    f"Check 241: shipped JS ({len(_eval_targets239)} 件) に document.write/writeln 呼び出し 0",
    (f"Check 241: document.write を含む shipped JS: {_offenders241!r} — "
     "deprecated/HTML5 parser sniff 破壊/XSS vector。createElement+appendChild に置換せよ"
     if _offenders241 else
     "Check 241: shipped JS 0 件 — vacuous-fail"),
    blocking=True,
)

# ── 242. index.html inline on*= handlers are restricted to allowlist (BLOCKING) ─
# index.html の全 `on*="..."` 属性 (HTML comment 外) が CSP unsafe-hashes で
# whitelist された 1 パターン `onload="this.media='all'"` のみであることを
# BLOCKING 強制。drift は CSP script-src を bypass する XSS entry vector。
_ALLOWED_INLINE_HANDLERS242 = {"onload=\"this.media='all'\""}
_idx242 = ROOT / "index.html"
if _idx242.exists():
    _isrc242 = _idx242.read_text(encoding="utf-8")
    _stripped242 = re.sub(r"<!--.*?-->", "", _isrc242, flags=re.DOTALL)
    _handlers242 = re.findall(r'\bon[a-z]+\s*=\s*"[^"]*"', _stripped242)
    _bad242 = [h for h in _handlers242 if h not in _ALLOWED_INLINE_HANDLERS242]
    _ok242 = len(_handlers242) > 0 and not _bad242
    check(
        _ok242,
        f"Check 242: index.html inline on*= handlers {len(_handlers242)} 件全て allowlist 内",
        (f"Check 242: allowlist 外 inline handler: {_bad242!r} — CSP script-src "
         "bypass の XSS vector。allowlist は onload=\"this.media='all'\" のみ"
         if _bad242 else
         "Check 242: inline handler 0 件 — vacuous-fail (font async load の期待値は 2 件)"),
        blocking=True,
    )
else:
    check(False, "Check 242: index.html present",
          "Check 242: index.html が無い", blocking=True)

# ── 243. SITE_CONFIG.LAST_UPDATED + ai:last-modified NOT future (BLOCKING) ────
# main.js SITE_CONFIG.LAST_UPDATED と <meta name="ai:last-modified"> content が
# 共に today より未来でないことを BLOCKING 強制。Check 36 (sitemap lastmod 未来
# WARNING) と異なり本サイトは pre-schedule しない設計のため BLOCKING。
from datetime import date as _date243
_main243 = ROOT / "main.js"
_idx243 = ROOT / "index.html"
if _main243.exists() and _idx243.exists():
    _msrc243 = _main243.read_text(encoding="utf-8")
    _isrc243 = _idx243.read_text(encoding="utf-8")
    _site243_m = re.search(r"LAST_UPDATED:\s*['\"]([^'\"]+)['\"]", _msrc243)
    _ai_lm243_m = re.search(
        r'<meta\s+name=["\']ai:last-modified["\']\s+content=["\']([^"\']+)["\']', _isrc243
    )
    _site243 = _site243_m.group(1) if _site243_m else None
    _ai_lm243 = _ai_lm243_m.group(1) if _ai_lm243_m else None
    _today243 = _date243.today()
    _futures243: list[str] = []
    for _label, _v in (("SITE_CONFIG.LAST_UPDATED", _site243), ("ai:last-modified", _ai_lm243)):
        if not isinstance(_v, str):
            _futures243.append(f"{_label}=抽出不可")
            continue
        try:
            _d = _date243.fromisoformat(_v[:10])
        except ValueError:
            # Check 215 が format を担う。本 check は format violation で fail せず skip。
            continue
        if _d > _today243:
            _futures243.append(f"{_label}={_v!r} (today={_today243.isoformat()} より未来)")
    _ok243 = not _futures243
    check(
        _ok243,
        f"Check 243: SITE_CONFIG.LAST_UPDATED + ai:last-modified 共に today ({_today243.isoformat()}) 以前",
        (f"Check 243: 未来日 detected: {_futures243!r} — AI/SEO recency が "
         "「未来から来た content」と誤認し ranking corruption。today 以下へ修正"),
        blocking=True,
    )
else:
    check(False, "Check 243: main.js + index.html present",
          "Check 243: main.js もしくは index.html が無い", blocking=True)

# ── 244. JSON-LD @graph 全 top-level node has @type (BLOCKING) ────────────────
# index.html の各 JSON-LD <script> block の top-level `@graph` 配列の全 element に
# 非空 `@type` がある (anonymous node 不在) ことを BLOCKING 強制。drift で AI/SEO
# が無 type node を無視し Schema.org graph traversal 不能。
_idx244 = ROOT / "index.html"
if _idx244.exists():
    _isrc244 = _idx244.read_text(encoding="utf-8")
    _blocks244 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc244,
        flags=re.DOTALL,
    )
    _violations244: list[str] = []
    _total244 = 0
    for _bi, _blk in enumerate(_blocks244):
        try:
            _data244 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _g244 = _data244.get("@graph") if isinstance(_data244, dict) else None
        if not isinstance(_g244, list):
            continue
        for _j, _n in enumerate(_g244):
            _total244 += 1
            if not isinstance(_n, dict) or not isinstance(_n.get("@type"), str) or not _n.get("@type"):
                _violations244.append(f"block{_bi}.@graph[{_j}] missing/empty @type")
    _ok244 = _total244 > 0 and not _violations244
    check(
        _ok244,
        f"Check 244: JSON-LD @graph top-level node {_total244} 件全て @type 保有",
        (f"Check 244: @type 不在 node: {_violations244!r} — AI/SEO 無視されて "
         "Schema.org graph traversal 破壊。各 top-level node に @type を付与せよ"
         if _violations244 else
         "Check 244: @graph top-level node 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 244: index.html present",
          "Check 244: index.html が無い", blocking=True)

# ── 245. JSON-LD FAQPage mainEntity Q&A structure validity (BLOCKING) ─────────
# index.html JSON-LD の全 FAQPage node の `mainEntity` 配列が Schema.org Q&A 構造
# (Question + name + acceptedAnswer(Answer + text)) を満たすことを BLOCKING 強制。
# drift は SILENT に Google FAQ rich-result 失格 + AI search FAQ ingestion 破壊。
_idx245 = ROOT / "index.html"
if _idx245.exists():
    _isrc245 = _idx245.read_text(encoding="utf-8")
    _blocks245 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc245,
        flags=re.DOTALL,
    )
    _violations245: list[str] = []
    _q_count245 = 0
    def _walk245(node: object, path: str) -> None:
        global _q_count245
        if isinstance(node, dict):
            if node.get("@type") == "FAQPage":
                _me = node.get("mainEntity")
                if not isinstance(_me, list) or not _me:
                    _violations245.append(f"{path}: FAQPage.mainEntity 欠落/空")
                else:
                    for _i, _q in enumerate(_me):
                        _q_count245 += 1
                        if not isinstance(_q, dict):
                            _violations245.append(f"{path}.mainEntity[{_i}] non-dict")
                            continue
                        if _q.get("@type") != "Question":
                            _violations245.append(f"{path}.mainEntity[{_i}] @type != Question")
                        _n = _q.get("name")
                        if not isinstance(_n, str) or not _n.strip():
                            _violations245.append(f"{path}.mainEntity[{_i}] name 欠落/空")
                        _a = _q.get("acceptedAnswer")
                        if not isinstance(_a, dict):
                            _violations245.append(f"{path}.mainEntity[{_i}] acceptedAnswer 欠落")
                        else:
                            if _a.get("@type") != "Answer":
                                _violations245.append(f"{path}.mainEntity[{_i}].acceptedAnswer @type != Answer")
                            _t = _a.get("text")
                            if not isinstance(_t, str) or not _t.strip():
                                _violations245.append(f"{path}.mainEntity[{_i}].acceptedAnswer.text 欠落/空")
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk245(item, f"{path}.{k}")
                else:
                    _walk245(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk245(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks245):
        try:
            _data245 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk245(_data245, f"block{_bi}")
    _ok245 = _q_count245 > 0 and not _violations245
    check(
        _ok245,
        f"Check 245: FAQPage mainEntity Q&A {_q_count245} 件全て Schema.org 構造正",
        (f"Check 245: 違反: {_violations245!r} — Google FAQ rich-result 失格 + "
         "AI FAQ ingestion 破壊。Question+name+acceptedAnswer(Answer+text) 構造へ揃えよ"
         if _violations245 else
         "Check 245: FAQPage mainEntity Q 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 245: index.html present",
          "Check 245: index.html が無い", blocking=True)

# ── 246. JSON-LD BreadcrumbList itemListElement Schema.org 構造 (BLOCKING) ────
# index.html JSON-LD 全 BreadcrumbList の `itemListElement` 配列が ListItem +
# position(int) + name(非空 str) + item(URL/string) を満たすことを BLOCKING 強制。
# drift で Google breadcrumb rich-result + AI site-structure ingestion 破壊。
_idx246 = ROOT / "index.html"
if _idx246.exists():
    _isrc246 = _idx246.read_text(encoding="utf-8")
    _blocks246 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc246,
        flags=re.DOTALL,
    )
    _violations246: list[str] = []
    _items_count246 = 0
    def _walk246(node: object, path: str) -> None:
        global _items_count246
        if isinstance(node, dict):
            if node.get("@type") == "BreadcrumbList":
                _ile = node.get("itemListElement")
                if not isinstance(_ile, list) or not _ile:
                    _violations246.append(f"{path}: itemListElement 欠落/空")
                else:
                    for _i, _it in enumerate(_ile):
                        _items_count246 += 1
                        if not isinstance(_it, dict):
                            _violations246.append(f"{path}.itemListElement[{_i}] non-dict")
                            continue
                        if _it.get("@type") != "ListItem":
                            _violations246.append(f"{path}.itemListElement[{_i}] @type != ListItem")
                        if not isinstance(_it.get("position"), int):
                            _violations246.append(f"{path}.itemListElement[{_i}] position not int")
                        _n = _it.get("name")
                        if not isinstance(_n, str) or not _n.strip():
                            _violations246.append(f"{path}.itemListElement[{_i}] name 欠落/空")
                        if "item" not in _it:
                            _violations246.append(f"{path}.itemListElement[{_i}] item 欠落")
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk246(item, f"{path}.{k}")
                else:
                    _walk246(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk246(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks246):
        try:
            _data246 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk246(_data246, f"block{_bi}")
    _ok246 = _items_count246 > 0 and not _violations246
    check(
        _ok246,
        f"Check 246: BreadcrumbList itemListElement {_items_count246} 件全て Schema.org 構造正",
        (f"Check 246: 違反: {_violations246!r} — Google breadcrumb rich-result 失格 "
         "+ AI site-structure ingestion 破壊。ListItem+position+name+item へ揃えよ"
         if _violations246 else
         "Check 246: BreadcrumbList items 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 246: index.html present",
          "Check 246: index.html が無い", blocking=True)

# ── 247. JSON-LD ImageObject/AudioObject/VideoObject 必須 fields (BLOCKING) ───
# index.html JSON-LD で `@type in {ImageObject, AudioObject, VideoObject}` の
# node が `name` AND (`contentUrl` OR `url`) を持つことを BLOCKING 強制。drift で
# Google Image/Audio rich-result 失格 + AI/SEO entity-asset linkage 破壊。
_MEDIA_TYPES247 = {"ImageObject", "AudioObject", "VideoObject"}
_idx247 = ROOT / "index.html"
if _idx247.exists():
    _isrc247 = _idx247.read_text(encoding="utf-8")
    _blocks247 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc247,
        flags=re.DOTALL,
    )
    _violations247: list[str] = []
    _media_count247 = 0
    def _walk247(node: object, path: str) -> None:
        global _media_count247
        if isinstance(node, dict):
            _t = node.get("@type")
            if isinstance(_t, str) and _t in _MEDIA_TYPES247:
                _media_count247 += 1
                _missing = []
                if not isinstance(node.get("name"), str) or not node.get("name", "").strip():
                    _missing.append("name")
                if "contentUrl" not in node and "url" not in node:
                    _missing.append("contentUrl|url")
                if _missing:
                    _violations247.append(f"{path} {_t}: missing {_missing!r}")
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk247(item, f"{path}.{k}")
                else:
                    _walk247(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk247(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks247):
        try:
            _data247 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk247(_data247, f"block{_bi}")
    _ok247 = _media_count247 > 0 and not _violations247
    check(
        _ok247,
        f"Check 247: MediaObject {_media_count247} 件全て name + contentUrl|url 保有",
        (f"Check 247: 違反: {_violations247!r} — Google Image/Audio rich-result 失格 "
         "+ AI/SEO entity-asset linkage 破壊。name + contentUrl|url を揃えよ"
         if _violations247 else
         "Check 247: MediaObject 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 247: index.html present",
          "Check 247: index.html が無い", blocking=True)

# ── 248. <meta charset> value is utf-8 (case-insensitive) (BLOCKING) ──────────
# index.html `<meta charset="...">` の値が utf-8 (case-insensitive) であることを
# BLOCKING 強制。drift で Japanese mojibake → canonical entity 名表示破壊。
# Check 157 は presence、Check 248 は value canonicality 軸。
_idx248 = ROOT / "index.html"
if _idx248.exists():
    _isrc248 = _idx248.read_text(encoding="utf-8")
    _cm248 = re.search(r'<meta\s+charset\s*=\s*["\']?([^"\'\s>]+)', _isrc248, re.IGNORECASE)
    _cv248 = _cm248.group(1) if _cm248 else None
    _ok248 = isinstance(_cv248, str) and _cv248.lower() == "utf-8"
    check(
        _ok248,
        f"Check 248: <meta charset>={_cv248!r} == utf-8 (case-insensitive)",
        (f"Check 248: charset 値違反: {_cv248!r} — Japanese mojibake で canonical "
         "entity 名表示破壊。utf-8 (case-insensitive) へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 248: index.html present",
          "Check 248: index.html が無い", blocking=True)

# ── 249. <meta name=viewport> content has mobile baseline (BLOCKING) ──────────
# index.html `<meta name="viewport">` content が `width=device-width` AND
# `initial-scale=1` を含むことを BLOCKING 強制。drift で mobile rendering 破壊
# (zoom 固定 / content cropped)。Check 157 (presence) の value 軸補完。
_idx249 = ROOT / "index.html"
if _idx249.exists():
    _isrc249 = _idx249.read_text(encoding="utf-8")
    _vm249 = re.search(
        r'<meta\s+name=["\']viewport["\'][^>]*content=["\']([^"\']+)["\']', _isrc249
    )
    _vv249 = _vm249.group(1) if _vm249 else None
    _missing249: list[str] = []
    if not isinstance(_vv249, str):
        _missing249.append("viewport 抽出不可")
    else:
        if "width=device-width" not in _vv249:
            _missing249.append("width=device-width 不在")
        if not re.search(r"initial-scale\s*=\s*1(\.0+)?\b", _vv249):
            _missing249.append("initial-scale=1 不在")
    _ok249 = not _missing249
    check(
        _ok249,
        f"Check 249: <meta name=viewport> content has mobile baseline ({_vv249!r})",
        (f"Check 249: viewport content 違反: {_missing249!r} — mobile rendering 破壊"
         " (zoom 固定/content cropped)。width=device-width + initial-scale=1 を付与"),
        blocking=True,
    )
else:
    check(False, "Check 249: index.html present",
          "Check 249: index.html が無い", blocking=True)

# ── 250. <html lang> value is BCP-47 valid (BLOCKING) ─────────────────────────
# index.html `<html lang="...">` 値が BCP-47 regex に一致することを BLOCKING 強制。
# Check 152/187/220 (inter-surface 一致) を補完する syntactic 軸。
_idx250 = ROOT / "index.html"
if _idx250.exists():
    _isrc250 = _idx250.read_text(encoding="utf-8")
    _hl250_m = re.search(r'<html\s+lang=["\']([^"\']+)["\']', _isrc250)
    _hl250 = _hl250_m.group(1) if _hl250_m else None
    _bcp47_re250 = re.compile(r"^[a-zA-Z]{2,3}(?:-[a-zA-Z0-9]{1,8})*$")
    _ok250 = isinstance(_hl250, str) and bool(_bcp47_re250.match(_hl250))
    check(
        _ok250,
        f"Check 250: <html lang>={_hl250!r} is BCP-47 valid",
        (f"Check 250: <html lang>={_hl250!r} 非 BCP-47 — browser 言語選択 / screen reader / "
         "AI/SEO 言語信号 silent 破壊。BCP-47 (例 'ja' / 'ja-JP' / 'en-US') へ訂正"),
        blocking=True,
    )
else:
    check(False, "Check 250: index.html present",
          "Check 250: index.html が無い", blocking=True)

# ── 251. JSON-LD potentialAction has required @type + target (BLOCKING) ───────
# index.html JSON-LD の全 `potentialAction` block が `@type` (Schema.org Action
# subclass) AND `target` を持つことを BLOCKING 強制。drift で AI/voice assistant の
# action invocation 破壊。Check 209 (target canonical prefix) の required-fields 軸。
_idx251 = ROOT / "index.html"
if _idx251.exists():
    _isrc251 = _idx251.read_text(encoding="utf-8")
    _blocks251 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc251,
        flags=re.DOTALL,
    )
    _violations251: list[str] = []
    _pa_count251 = 0
    def _walk251(node: object, path: str) -> None:
        global _pa_count251
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "potentialAction":
                    if isinstance(v, dict):
                        _pa_count251 += 1
                        if not isinstance(v.get("@type"), str) or not v.get("@type", "").strip():
                            _violations251.append(f"{path}.potentialAction @type 欠落/空")
                        if "target" not in v:
                            _violations251.append(f"{path}.potentialAction target 欠落")
                    elif isinstance(v, list):
                        for _i, _it in enumerate(v):
                            _pa_count251 += 1
                            if not isinstance(_it, dict):
                                _violations251.append(f"{path}.potentialAction[{_i}] non-dict")
                                continue
                            if not isinstance(_it.get("@type"), str) or not _it.get("@type", "").strip():
                                _violations251.append(f"{path}.potentialAction[{_i}] @type 欠落/空")
                            if "target" not in _it:
                                _violations251.append(f"{path}.potentialAction[{_i}] target 欠落")
                if isinstance(v, list):
                    for item in v:
                        _walk251(item, f"{path}.{k}")
                else:
                    _walk251(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk251(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks251):
        try:
            _data251 = json.loads(_blk)
        except json.JSONDecodeError:
            continue
        _walk251(_data251, f"block{_bi}")
    _ok251 = _pa_count251 > 0 and not _violations251
    check(
        _ok251,
        f"Check 251: potentialAction {_pa_count251} block 全て @type + target 保有",
        (f"Check 251: 違反: {_violations251!r} — AI/voice assistant action invocation 破壊。"
         "@type (Schema.org Action subclass) + target を付与せよ"
         if _violations251 else
         "Check 251: potentialAction 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 251: index.html present",
          "Check 251: index.html が無い", blocking=True)

# ── 252. sw.js registers install + activate + fetch handlers (BLOCKING) ───────
# sw.js が install / activate / fetch 3 event handler を全て登録することを
# BLOCKING 強制。silent 欠落で SW lifecycle 破壊 (precache 不能 / cleanup 不能 /
# offline+SWR 不能)。Check 19 (CACHE_NAME version) の SW handler presence 軸。
_sw252 = ROOT / "sw.js"
if _sw252.exists():
    _ssrc252 = _sw252.read_text(encoding="utf-8")
    _required_evts252 = ["install", "activate", "fetch"]
    _missing252: list[str] = []
    for _e in _required_evts252:
        _pat = re.compile(
            r'(?:self|globalThis)\s*\.\s*addEventListener\s*\(\s*[\'"]' + re.escape(_e) + r'[\'"]'
        )
        if not _pat.search(_ssrc252):
            _missing252.append(_e)
    _ok252 = not _missing252
    check(
        _ok252,
        f"Check 252: sw.js registers {_required_evts252!r} handlers (all 3)",
        (f"Check 252: missing SW handlers: {_missing252!r} — SW lifecycle 破壊 "
         "(precache/cleanup/offline 不能)。self.addEventListener で 3 event 全登録"),
        blocking=True,
    )
else:
    check(False, "Check 252: sw.js present",
          "Check 252: sw.js が無い", blocking=True)

# ── 253. main.js calls navigator.serviceWorker.register('./sw.js' (BLOCKING) ──
# main.js が `navigator.serviceWorker.register('./sw.js'` を呼ぶことを BLOCKING
# 強制。silent 欠落で sw.js handler は存在しても install されず offline+SWR 機能
# 全停止。Check 252 (handler presence) の register call-site 軸。
_main253 = ROOT / "main.js"
if _main253.exists():
    _msrc253 = _main253.read_text(encoding="utf-8")
    _has253 = re.search(
        r"navigator\s*\.\s*serviceWorker\s*\.\s*register\s*\(\s*['\"]\./sw\.js['\"]",
        _msrc253,
    ) is not None
    check(
        _has253,
        "Check 253: main.js が navigator.serviceWorker.register('./sw.js'...) を呼ぶ",
        ("Check 253: main.js に navigator.serviceWorker.register('./sw.js') 呼び出しが無い — "
         "sw.js handlers (Check 252) は存在しても install されず offline+SWR 停止。"
         "main.js の SW 登録 call-site を復元せよ"),
        blocking=True,
    )
else:
    check(False, "Check 253: main.js present",
          "Check 253: main.js が無い", blocking=True)

# ── 254. .well-known/index.json skill name uniqueness + digest format (BLOCKING) ─
# .well-known/index.json の skills[] 各 entry の name が非空+block 内 unique で、
# digest が `sha-256:<64-hex>` regex に一致することを BLOCKING 強制。Check 5
# (byte-identical mirror) の schema structural validity 軸。
_widx254 = ROOT / ".well-known" / "index.json"
if _widx254.exists():
    try:
        _wd254 = json.loads(_widx254.read_text(encoding="utf-8"))
    except json.JSONDecodeError as _e254:
        _wd254 = None
    _skills254 = _wd254.get("skills", []) if isinstance(_wd254, dict) else []
    _bad254: list[str] = []
    _names254: list[str] = []
    _digest_re254 = re.compile(r"^sha-256:[0-9a-f]{64}$")
    for _i, _s in enumerate(_skills254):
        if not isinstance(_s, dict):
            _bad254.append(f"skills[{_i}]: non-dict")
            continue
        _nm = _s.get("name")
        if not isinstance(_nm, str) or not _nm.strip():
            _bad254.append(f"skills[{_i}]: name 欠落/空")
        else:
            _names254.append(_nm)
        _dg = _s.get("digest")
        if not isinstance(_dg, str) or not _digest_re254.match(_dg):
            _bad254.append(f"skills[{_i}].digest={_dg!r} format 不正 (sha-256:<64-hex>)")
    from collections import Counter as _Counter254
    _dupes254 = [n for n, c in _Counter254(_names254).items() if c > 1]
    if _dupes254:
        _bad254.append(f"name 重複: {_dupes254!r}")
    _ok254 = len(_skills254) > 0 and not _bad254
    check(
        _ok254,
        f"Check 254: .well-known/index.json skills ({len(_skills254)} 件) 全て name 一意 + digest 形式正",
        (f"Check 254: 違反: {_bad254!r} — agent-skills discovery 破壊。"
         "name 一意 + digest=sha-256:<64-hex> へ整理"
         if _bad254 else
         "Check 254: .well-known/index.json skills 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 254: .well-known/index.json present",
          "Check 254: .well-known/index.json が無い", blocking=True)

# ── 255. index.html starts with <!DOCTYPE html> (HTML5 declaration) (BLOCKING) ─
# index.html が `<!DOCTYPE html>` (case-insensitive, leading BOM/whitespace 無視)
# で始まることを BLOCKING 強制。drift で browser quirks mode 発火 → CSS box model
# 退行 / line-height drift / layout 破壊。Check 157 の document-mode declaration 軸。
_idx255 = ROOT / "index.html"
if _idx255.exists():
    _isrc255 = _idx255.read_text(encoding="utf-8")
    _head255 = _isrc255.lstrip("﻿").lstrip()
    _ok255 = bool(re.match(r"<!DOCTYPE\s+html\s*>", _head255, re.IGNORECASE))
    check(
        _ok255,
        "Check 255: index.html starts with <!DOCTYPE html> (HTML5)",
        ("Check 255: index.html が <!DOCTYPE html> で始まらない — browser quirks "
         "mode 発火で CSS box model 退行・layout 破壊。先頭に <!DOCTYPE html> を配置"),
        blocking=True,
    )
else:
    check(False, "Check 255: index.html present",
          "Check 255: index.html が無い", blocking=True)

# ── 256. primary WebPage has dateModified + inLanguage + isPartOf (BLOCKING) ──
# index.html 静的 JSON-LD の primary WebPage node (@id == canonical+#webpage) が
# `dateModified` + `inLanguage` + `isPartOf` を持つことを BLOCKING 強制。drift で
# recency/language/hierarchy 信号 silent 喪失。Check 235 の primary WebPage 軸版。
_idx256 = ROOT / "index.html"
if _idx256.exists():
    _isrc256 = _idx256.read_text(encoding="utf-8")
    _canon256_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc256
    )
    _canon256 = _canon256_m.group(1) if _canon256_m else None
    _expected_wid256 = (_canon256 or "") + "#webpage"
    _blocks256 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc256,
        flags=re.DOTALL,
    )
    _primary_wp256 = None
    def _walk256(node: object) -> None:
        global _primary_wp256
        if isinstance(node, dict):
            if node.get("@type") == "WebPage" and node.get("@id") == _expected_wid256:
                _primary_wp256 = node
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk256(item)
                else:
                    _walk256(v)
        elif isinstance(node, list):
            for item in node:
                _walk256(item)
    for _blk in _blocks256:
        try:
            _walk256(json.loads(_blk))
        except json.JSONDecodeError:
            continue
    _missing256: list[str] = []
    if _primary_wp256 is None:
        _missing256.append(f"primary WebPage @id={_expected_wid256!r} 不在")
    else:
        if not isinstance(_primary_wp256.get("dateModified"), str):
            _missing256.append("dateModified 欠落")
        if not isinstance(_primary_wp256.get("inLanguage"), str):
            _missing256.append("inLanguage 欠落")
        if not isinstance(_primary_wp256.get("isPartOf"), (dict, str)):
            _missing256.append("isPartOf 欠落")
    _ok256 = not _missing256
    check(
        _ok256,
        f"Check 256: primary WebPage ({_expected_wid256}) has dateModified + inLanguage + isPartOf",
        (f"Check 256: 違反: {_missing256!r} — recency/language/hierarchy 信号喪失。"
         "primary WebPage に 3 field を揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 256: index.html present",
          "Check 256: index.html が無い", blocking=True)

# ── 257. primary Person 必須 5 fields (BLOCKING) ──────────────────────────────
# index.html 静的 JSON-LD の primary Person node (@id == canonical+#person) が
# jobTitle (str) / image (dict|str) / sameAs (list) / worksFor (dict|str) /
# description (str) 全 5 field を持つことを BLOCKING 強制。drift で entity-rich
# profile data 喪失 → knowledge-graph card 縮小。Check 256 の primary Person 軸版。
_idx257 = ROOT / "index.html"
if _idx257.exists():
    _isrc257 = _idx257.read_text(encoding="utf-8")
    _canon257_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc257
    )
    _canon257 = _canon257_m.group(1) if _canon257_m else None
    _expected_pid257 = (_canon257 or "") + "#person"
    _blocks257 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc257,
        flags=re.DOTALL,
    )
    _primary_p257 = None
    def _walk257(node: object) -> None:
        global _primary_p257
        if isinstance(node, dict):
            if node.get("@type") == "Person" and node.get("@id") == _expected_pid257 and _primary_p257 is None:
                _primary_p257 = node
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk257(item)
                else:
                    _walk257(v)
        elif isinstance(node, list):
            for item in node:
                _walk257(item)
    for _blk in _blocks257:
        try:
            _walk257(json.loads(_blk))
        except json.JSONDecodeError:
            continue
    _missing257: list[str] = []
    if _primary_p257 is None:
        _missing257.append(f"primary Person @id={_expected_pid257!r} 不在")
    else:
        _str_fields = ("jobTitle", "description")
        for _f in _str_fields:
            if not isinstance(_primary_p257.get(_f), str) or not _primary_p257[_f].strip():
                _missing257.append(f"{_f} 欠落/空")
        if not isinstance(_primary_p257.get("image"), (dict, str)):
            _missing257.append("image 欠落")
        if not isinstance(_primary_p257.get("sameAs"), list) or not _primary_p257["sameAs"]:
            _missing257.append("sameAs 欠落/空 list")
        if not isinstance(_primary_p257.get("worksFor"), (dict, str)):
            _missing257.append("worksFor 欠落")
    _ok257 = not _missing257
    check(
        _ok257,
        f"Check 257: primary Person ({_expected_pid257}) has 5 required fields",
        (f"Check 257: 違反: {_missing257!r} — entity-rich profile 喪失で knowledge-graph "
         "card 縮小。primary Person に 5 field を揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 257: index.html present",
          "Check 257: index.html が無い", blocking=True)

# ── 258. primary WebSite has inLanguage + potentialAction (BLOCKING) ──────────
# index.html 静的 JSON-LD の primary WebSite node (@id == canonical+#website) が
# inLanguage (str) + potentialAction (dict|list) を持つことを BLOCKING 強制。
# drift で site-level 言語信号 + AI/voice action descriptor 喪失。Check 256/257
# の primary WebSite 軸版。
_idx258 = ROOT / "index.html"
if _idx258.exists():
    _isrc258 = _idx258.read_text(encoding="utf-8")
    _canon258_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc258
    )
    _canon258 = _canon258_m.group(1) if _canon258_m else None
    _expected_wid258 = (_canon258 or "") + "#website"
    _blocks258 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc258,
        flags=re.DOTALL,
    )
    _primary_ws258 = None
    def _walk258(node: object) -> None:
        global _primary_ws258
        if isinstance(node, dict):
            if node.get("@type") == "WebSite" and node.get("@id") == _expected_wid258 and _primary_ws258 is None:
                _primary_ws258 = node
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk258(item)
                else:
                    _walk258(v)
        elif isinstance(node, list):
            for item in node:
                _walk258(item)
    for _blk in _blocks258:
        try:
            _walk258(json.loads(_blk))
        except json.JSONDecodeError:
            continue
    _missing258: list[str] = []
    if _primary_ws258 is None:
        _missing258.append(f"primary WebSite @id={_expected_wid258!r} 不在")
    else:
        if not isinstance(_primary_ws258.get("inLanguage"), str):
            _missing258.append("inLanguage 欠落")
        if not isinstance(_primary_ws258.get("potentialAction"), (dict, list)):
            _missing258.append("potentialAction 欠落")
    _ok258 = not _missing258
    check(
        _ok258,
        f"Check 258: primary WebSite ({_expected_wid258}) has inLanguage + potentialAction",
        (f"Check 258: 違反: {_missing258!r} — site-level 言語 / action descriptor 喪失。"
         "primary WebSite に 2 field を揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 258: index.html present",
          "Check 258: index.html が無い", blocking=True)

# ── 259. primary Organization (nkgr.co.jp) 必須 5 fields (BLOCKING) ──────────
# index.html JSON-LD の primary Organization node
# (@id == "https://nkgr.co.jp/#organization") が name + url + alternateName +
# description + employee 5 field を持つことを BLOCKING 強制。drift で employer-rich
# data 喪失 → knowledge-graph Organization card 縮小。Check 257 の Organization 軸版。
_PRIMARY_ORG_ID259 = "https://nkgr.co.jp/#organization"
_idx259 = ROOT / "index.html"
if _idx259.exists():
    _isrc259 = _idx259.read_text(encoding="utf-8")
    _blocks259 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc259,
        flags=re.DOTALL,
    )
    _primary_org259 = None
    def _walk259(node: object) -> None:
        global _primary_org259
        if isinstance(node, dict):
            if (
                node.get("@type") == "Organization"
                and node.get("@id") == _PRIMARY_ORG_ID259
                and _primary_org259 is None
            ):
                _primary_org259 = node
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk259(item)
                else:
                    _walk259(v)
        elif isinstance(node, list):
            for item in node:
                _walk259(item)
    for _blk in _blocks259:
        try:
            _walk259(json.loads(_blk))
        except json.JSONDecodeError:
            continue
    _missing259: list[str] = []
    if _primary_org259 is None:
        _missing259.append(f"primary Organization @id={_PRIMARY_ORG_ID259!r} 不在")
    else:
        for _f in ("name", "url", "description"):
            if not isinstance(_primary_org259.get(_f), str) or not _primary_org259[_f].strip():
                _missing259.append(f"{_f} 欠落/空")
        if not isinstance(_primary_org259.get("alternateName"), list) or not _primary_org259["alternateName"]:
            _missing259.append("alternateName 欠落/空 list")
        if not isinstance(_primary_org259.get("employee"), (dict, list, str)):
            _missing259.append("employee 欠落")
    _ok259 = not _missing259
    check(
        _ok259,
        f"Check 259: primary Organization ({_PRIMARY_ORG_ID259}) has 5 required fields",
        (f"Check 259: 違反: {_missing259!r} — employer-rich data 喪失 → "
         "knowledge-graph Organization card 縮小。primary Organization に 5 field を揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 259: index.html present",
          "Check 259: index.html が無い", blocking=True)

# ── 260. primary hero ImageObject 必須 4 fields (BLOCKING) ────────────────────
# index.html JSON-LD の primary hero ImageObject node (@id == canonical+#hero-image)
# が caption (非空 str) + width (numeric-parsable) + height (numeric-parsable) +
# encodingFormat (非空 str) を持つことを BLOCKING 強制。drift で Google Image
# rich-result + CWV LCP preload + accessibility 劣化。Check 247 の hero-image 軸版。
_idx260 = ROOT / "index.html"
if _idx260.exists():
    _isrc260 = _idx260.read_text(encoding="utf-8")
    _canon260_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc260
    )
    _canon260 = _canon260_m.group(1) if _canon260_m else None
    _expected_hid260 = (_canon260 or "") + "#hero-image"
    _blocks260 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc260,
        flags=re.DOTALL,
    )
    _primary_hero260 = None
    def _walk260(node: object) -> None:
        global _primary_hero260
        if isinstance(node, dict):
            if (
                node.get("@type") == "ImageObject"
                and node.get("@id") == _expected_hid260
                and _primary_hero260 is None
            ):
                _primary_hero260 = node
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk260(item)
                else:
                    _walk260(v)
        elif isinstance(node, list):
            for item in node:
                _walk260(item)
    for _blk in _blocks260:
        try:
            _walk260(json.loads(_blk))
        except json.JSONDecodeError:
            continue
    _missing260: list[str] = []
    if _primary_hero260 is None:
        _missing260.append(f"primary hero ImageObject @id={_expected_hid260!r} 不在")
    else:
        for _f in ("caption", "encodingFormat"):
            if not isinstance(_primary_hero260.get(_f), str) or not _primary_hero260[_f].strip():
                _missing260.append(f"{_f} 欠落/空")
        for _f in ("width", "height"):
            _v = _primary_hero260.get(_f)
            try:
                if isinstance(_v, str):
                    int(_v)
                elif isinstance(_v, int):
                    pass
                else:
                    raise ValueError("not numeric")
            except (TypeError, ValueError):
                _missing260.append(f"{_f}={_v!r} 非 numeric/欠落")
    _ok260 = not _missing260
    check(
        _ok260,
        f"Check 260: primary hero ImageObject has caption + width + height + encodingFormat",
        (f"Check 260: 違反: {_missing260!r} — Google Image rich-result + CWV LCP + "
         "accessibility 劣化。caption(str) + width/height(numeric) + encodingFormat(str) を揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 260: index.html present",
          "Check 260: index.html が無い", blocking=True)

# ── 261. primary BGM AudioObject 必須 fields (BLOCKING) ───────────────────────
# index.html JSON-LD の primary BGM AudioObject (@id == canonical+#portfolio-bgm)
# が encodingFormat (str) + creator (dict|str) を持つことを BLOCKING 強制。drift で
# AI search audio classification + attribution 喪失。Check 260 の audio 軸版。
_idx261 = ROOT / "index.html"
if _idx261.exists():
    _isrc261 = _idx261.read_text(encoding="utf-8")
    _canon261_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc261
    )
    _canon261 = _canon261_m.group(1) if _canon261_m else None
    _expected_bid261 = (_canon261 or "") + "#portfolio-bgm"
    _blocks261 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc261,
        flags=re.DOTALL,
    )
    _primary_bgm261 = None
    def _walk261(node: object) -> None:
        global _primary_bgm261
        if isinstance(node, dict):
            if (
                node.get("@type") == "AudioObject"
                and node.get("@id") == _expected_bid261
                and _primary_bgm261 is None
            ):
                _primary_bgm261 = node
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk261(item)
                else:
                    _walk261(v)
        elif isinstance(node, list):
            for item in node:
                _walk261(item)
    for _blk in _blocks261:
        try:
            _walk261(json.loads(_blk))
        except json.JSONDecodeError:
            continue
    _missing261: list[str] = []
    if _primary_bgm261 is None:
        _missing261.append(f"primary BGM AudioObject @id={_expected_bid261!r} 不在")
    else:
        if not isinstance(_primary_bgm261.get("encodingFormat"), str) or not _primary_bgm261["encodingFormat"].strip():
            _missing261.append("encodingFormat 欠落/空")
        if not isinstance(_primary_bgm261.get("creator"), (dict, str)):
            _missing261.append("creator 欠落")
    _ok261 = not _missing261
    check(
        _ok261,
        f"Check 261: primary BGM AudioObject ({_expected_bid261}) has encodingFormat + creator",
        (f"Check 261: 違反: {_missing261!r} — AI search audio classification + "
         "attribution 喪失。encodingFormat (str) + creator (dict/str) を揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 261: index.html present",
          "Check 261: index.html が無い", blocking=True)

# ── 262. Shipped JS no console.log calls (BLOCKING) ───────────────────────────
# main.js + sw.js + js/**/*.js + root scripts に `console.log(` 呼び出しが 0
# であることを BLOCKING 強制 (negative invariant)。console.error/warn/info/debug は
# 許可 (production observability)、log は debug-statement leak の anti-pattern。
_offenders262: list[str] = []
_log_pat262 = re.compile(r"\bconsole\s*\.\s*log\s*\(")
for _p in _eval_targets239:  # reuse Check 239 target list (31 file)
    try:
        _src = _p.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        continue
    _stripped = re.sub(r"/\*.*?\*/", "", _src, flags=re.DOTALL)
    _stripped = re.sub(r"//[^\n]*", "", _stripped)
    _stripped = re.sub(r"'(?:\\.|[^'\\])*'", "''", _stripped)
    _stripped = re.sub(r'"(?:\\.|[^"\\])*"', '""', _stripped)
    _stripped = re.sub(r"`(?:\\.|[^`\\])*`", "``", _stripped)
    if _log_pat262.search(_stripped):
        _offenders262.append(str(Path(_p).relative_to(ROOT)))
_ok262 = len(_eval_targets239) > 0 and not _offenders262
check(
    _ok262,
    f"Check 262: shipped JS ({len(_eval_targets239)} 件) に console.log 呼び出し 0",
    (f"Check 262: console.log を含む shipped JS: {_offenders262!r} — "
     "production debug-statement leak。console.error/warn/info/debug を使うか除去せよ"
     if _offenders262 else
     "Check 262: shipped JS 0 件 — vacuous-fail"),
    blocking=True,
)

# ── 263. Shipped JS no debugger; statement + no alert( call (BLOCKING) ────────
# main.js + sw.js + js/**/*.js + root scripts に `debugger;` statement と
# `alert(` 呼び出しが共に 0 であることを BLOCKING 強制 (negative invariant)。
# 共に dev-debug-only pattern。confirm() は意図的に許可 (削除確認 UX)。
_offenders263: list[tuple[str, str]] = []
_dbg_pat263 = re.compile(r"\bdebugger\s*;|\balert\s*\(")
for _p in _eval_targets239:  # reuse Check 239 target list
    try:
        _src = _p.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        continue
    _stripped = re.sub(r"/\*.*?\*/", "", _src, flags=re.DOTALL)
    _stripped = re.sub(r"//[^\n]*", "", _stripped)
    _stripped = re.sub(r"'(?:\\.|[^'\\])*'", "''", _stripped)
    _stripped = re.sub(r'"(?:\\.|[^"\\])*"', '""', _stripped)
    _stripped = re.sub(r"`(?:\\.|[^`\\])*`", "``", _stripped)
    _m = _dbg_pat263.search(_stripped)
    if _m:
        _offenders263.append((str(Path(_p).relative_to(ROOT)), _m.group(0)))
_ok263 = len(_eval_targets239) > 0 and not _offenders263
check(
    _ok263,
    f"Check 263: shipped JS ({len(_eval_targets239)} 件) に debugger; / alert( 0",
    (f"Check 263: dev-debug pattern を含む shipped JS: {_offenders263!r} — "
     "debugger; / alert( は production UX-break。除去せよ (confirm() は許可)"
     if _offenders263 else
     "Check 263: shipped JS 0 件 — vacuous-fail"),
    blocking=True,
)

# ── 264. Shipped JS comments no TODO/FIXME/HACK/XXX (BLOCKING) ────────────────
# main.js + sw.js + js/**/*.js + root scripts の comment 内に dev-cruft marker
# (TODO/FIXME/HACK/XXX, word-boundary, case-sensitive) が無いことを BLOCKING 強制。
# string literal の "TODO" 等は exempt (e.g. user-facing app 名)。
_offenders264: list[tuple[str, str]] = []
_cruft_pat264 = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
for _p in _eval_targets239:  # reuse Check 239 target list (31 file)
    try:
        _src = _p.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        continue
    # Strip string/template literals first to avoid false-positive on
    # user-facing strings containing "TODO" (e.g. app name "クイックTODO").
    _stripped = re.sub(r"'(?:\\.|[^'\\])*'", "''", _src)
    _stripped = re.sub(r'"(?:\\.|[^"\\])*"', '""', _stripped)
    _stripped = re.sub(r"`(?:\\.|[^`\\])*`", "``", _stripped)
    # Collect only comment regions (// ... and /* ... */).
    _comments: list[str] = []
    for _m in re.finditer(r"/\*.*?\*/", _stripped, flags=re.DOTALL):
        _comments.append(_m.group(0))
    for _m in re.finditer(r"//[^\n]*", _stripped):
        _comments.append(_m.group(0))
    for _c in _comments:
        _m2 = _cruft_pat264.search(_c)
        if _m2:
            _offenders264.append((str(Path(_p).relative_to(ROOT)), _m2.group(0)))
            break
_ok264 = len(_eval_targets239) > 0 and not _offenders264
check(
    _ok264,
    f"Check 264: shipped JS comments ({len(_eval_targets239)} 件) に TODO/FIXME/HACK/XXX 0",
    (f"Check 264: dev-cruft marker を含む shipped JS comment: {_offenders264!r} — "
     "incomplete dev-time note leak。task 化して comment は除去せよ"
     if _offenders264 else
     "Check 264: shipped JS 0 件 — vacuous-fail"),
    blocking=True,
)

# ── 265. Shipped JS strict equality (no `==` / `!=`) (BLOCKING) ───────────────
# main.js + sw.js + js/**/*.js + root scripts に loose equality (`==` / `!=`)
# 演算子が無いことを BLOCKING 強制 (negative invariant)。strict (===/!==) のみ。
# string literal / comment 内の `==` 等は exempt。
_offenders265: list[str] = []
# `==` and `!=` not preceded by =/!/</> and not followed by =
_loose_pat265 = re.compile(r"(?<![=!<>])==(?!=)|(?<![=!<>])!=(?!=)")
for _p in _eval_targets239:  # reuse Check 239 target list
    try:
        _src = _p.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        continue
    _stripped = re.sub(r"/\*.*?\*/", "", _src, flags=re.DOTALL)
    _stripped = re.sub(r"//[^\n]*", "", _stripped)
    _stripped = re.sub(r"'(?:\\.|[^'\\])*'", "''", _stripped)
    _stripped = re.sub(r'"(?:\\.|[^"\\])*"', '""', _stripped)
    _stripped = re.sub(r"`(?:\\.|[^`\\])*`", "``", _stripped)
    if _loose_pat265.search(_stripped):
        _offenders265.append(str(Path(_p).relative_to(ROOT)))
_ok265 = len(_eval_targets239) > 0 and not _offenders265
check(
    _ok265,
    f"Check 265: shipped JS ({len(_eval_targets239)} 件) に loose equality (==/!=) 0",
    (f"Check 265: loose equality を含む shipped JS: {_offenders265!r} — "
     "type coercion bugs の温床。===/!== へ変更"
     if _offenders265 else
     "Check 265: shipped JS 0 件 — vacuous-fail"),
    blocking=True,
)

# ── 266. JSON-LD entity description length in [20, 1000] (BLOCKING) ───────────
# index.html JSON-LD で Person/Organization/ImageObject/CreativeWork node の
# description 値長が [20, 1000] character 内であることを BLOCKING 強制。
# 下限以下: too brief / 上限以上: copy-paste over-long。Check 224 の JSON-LD 軸版。
_DESC_TYPES266 = {"Person", "Organization", "ImageObject", "CreativeWork"}
_idx266 = ROOT / "index.html"
if _idx266.exists():
    _isrc266 = _idx266.read_text(encoding="utf-8")
    _blocks266 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc266,
        flags=re.DOTALL,
    )
    _violations266: list[str] = []
    _checked266 = 0
    def _walk266(node: object, path: str) -> None:
        global _checked266
        if isinstance(node, dict):
            _t = node.get("@type")
            _d = node.get("description")
            if isinstance(_t, str) and _t in _DESC_TYPES266 and isinstance(_d, str):
                _checked266 += 1
                _ln = len(_d)
                if not (20 <= _ln <= 1000):
                    _violations266.append(f"{path} {_t}: description len={_ln} (band [20, 1000] 違反)")
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk266(item, f"{path}.{k}")
                else:
                    _walk266(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk266(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks266):
        try:
            _walk266(json.loads(_blk), f"block{_bi}")
        except json.JSONDecodeError:
            continue
    _ok266 = _checked266 > 0 and not _violations266
    check(
        _ok266,
        f"Check 266: JSON-LD entity description ({_checked266} 件) 全て [20, 1000] 内",
        (f"Check 266: 違反: {_violations266!r} — too brief で AI/SEO 入力不足 / "
         "too long で copy-paste 過剰。20〜1000 char へ調整せよ"
         if _violations266 else
         "Check 266: description 付き entity 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 266: index.html present",
          "Check 266: index.html が無い", blocking=True)

# ── 267. JSON-LD entity name length in [3, 200] (BLOCKING) ────────────────────
# index.html JSON-LD で @id + name 両備の entity (Person/Organization/Image/
# WebSite/WebPage/TechArticle/CreativeWork/AudioObject) の name 値長が
# [3, 200] 内であることを BLOCKING 強制。Check 266 の entity name 軸版。
_NAME_TYPES267 = {"Person", "Organization", "ImageObject", "WebSite", "WebPage",
                   "TechArticle", "CreativeWork", "AudioObject"}
_idx267 = ROOT / "index.html"
if _idx267.exists():
    _isrc267 = _idx267.read_text(encoding="utf-8")
    _blocks267 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc267,
        flags=re.DOTALL,
    )
    _violations267: list[str] = []
    _checked267 = 0
    def _walk267(node: object, path: str) -> None:
        global _checked267
        if isinstance(node, dict):
            _t = node.get("@type")
            _n = node.get("name")
            if (
                isinstance(_t, str) and _t in _NAME_TYPES267
                and node.get("@id") and isinstance(_n, str)
            ):
                _checked267 += 1
                _ln = len(_n)
                if not (3 <= _ln <= 200):
                    _violations267.append(f"{path} {_t}: name len={_ln} value={_n[:30]!r}")
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk267(item, f"{path}.{k}")
                else:
                    _walk267(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk267(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks267):
        try:
            _walk267(json.loads(_blk), f"block{_bi}")
        except json.JSONDecodeError:
            continue
    _ok267 = _checked267 > 0 and not _violations267
    check(
        _ok267,
        f"Check 267: JSON-LD entity name ({_checked267} 件) 全て [3, 200] 内",
        (f"Check 267: 違反: {_violations267!r} — <3=stub / >200=copy-paste over-long。"
         "[3, 200] へ調整"
         if _violations267 else
         "Check 267: name 付き entity 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 267: index.html present",
          "Check 267: index.html が無い", blocking=True)

# ── 268. JSON-LD Article/TechArticle headline length in [10, 110] (BLOCKING) ──
# index.html JSON-LD Article/TechArticle node の headline 値長が [10, 110] 内
# (Schema.org / Google Article rich-result spec) であることを BLOCKING 強制。
# Check 235 (Article 必須 fields) の headline length 軸版。
_HEADLINE_TYPES268 = {"Article", "TechArticle", "NewsArticle", "BlogPosting"}
_idx268 = ROOT / "index.html"
if _idx268.exists():
    _isrc268 = _idx268.read_text(encoding="utf-8")
    _blocks268 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc268,
        flags=re.DOTALL,
    )
    _violations268: list[str] = []
    _checked268 = 0
    def _walk268(node: object, path: str) -> None:
        global _checked268
        if isinstance(node, dict):
            _t = node.get("@type")
            _h = node.get("headline")
            if isinstance(_t, str) and _t in _HEADLINE_TYPES268 and isinstance(_h, str):
                _checked268 += 1
                _ln = len(_h)
                if not (10 <= _ln <= 110):
                    _violations268.append(f"{path} {_t}: headline len={_ln}")
            for k, v in node.items():
                if isinstance(v, list):
                    for item in v:
                        _walk268(item, f"{path}.{k}")
                else:
                    _walk268(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk268(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks268):
        try:
            _walk268(json.loads(_blk), f"block{_bi}")
        except json.JSONDecodeError:
            continue
    _ok268 = _checked268 > 0 and not _violations268
    check(
        _ok268,
        f"Check 268: Article/TechArticle headline ({_checked268} 件) 全て [10, 110] 内",
        (f"Check 268: 違反: {_violations268!r} — Google rich-result card truncate "
         "or sparse。Schema.org spec の <= 110 char に揃えよ"
         if _violations268 else
         "Check 268: headline 付き Article 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 268: index.html present",
          "Check 268: index.html が無い", blocking=True)

# ── 269. canonical binary asset size budget (BLOCKING) ────────────────────────
# canonical hero.webp <= 200_000 bytes AND BGM.mp3 <= 1_000_000 bytes を
# BLOCKING 強制 (CWV LCP / mobile bandwidth budget)。Check 120 (JS byte weight)
# の binary asset 軸版。
_HERO_WEBP269 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
_BGM_MP3_269 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"
_BUDGETS269 = [
    (_HERO_WEBP269, 200_000, "hero.webp"),
    (_BGM_MP3_269, 1_000_000, "BGM.mp3"),
]
_violations269: list[str] = []
for _p, _budget, _label in _BUDGETS269:
    if not _p.exists():
        _violations269.append(f"{_label} ({_p.name}) 不在")
        continue
    _sz = _p.stat().st_size
    if _sz > _budget:
        _violations269.append(f"{_label}={_sz} bytes (budget {_budget})")
_ok269 = not _violations269
check(
    _ok269,
    f"Check 269: canonical binary assets ({len(_BUDGETS269)} 件) all within byte budget",
    (f"Check 269: 違反: {_violations269!r} — CWV LCP / mobile bandwidth 劣化。"
     "binary を再圧縮 or budget を上げる contract 更新"),
    blocking=True,
)

# ── 270. canonical text asset byte budget (BLOCKING) ──────────────────────────
# style.css <= 100_000 bytes AND index.html <= 200_000 bytes を BLOCKING 強制。
# Check 120 (JS) / 269 (binary) の text asset 軸版。
_BUDGETS270 = [
    (ROOT / "style.css", 100_000, "style.css"),
    (ROOT / "index.html", 200_000, "index.html"),
]
_violations270: list[str] = []
for _p, _budget, _label in _BUDGETS270:
    if not _p.exists():
        _violations270.append(f"{_label} ({_p.name}) 不在")
        continue
    _sz = _p.stat().st_size
    if _sz > _budget:
        _violations270.append(f"{_label}={_sz} bytes (budget {_budget})")
_ok270 = not _violations270
check(
    _ok270,
    f"Check 270: canonical text assets ({len(_BUDGETS270)} 件) all within byte budget",
    (f"Check 270: 違反: {_violations270!r} — silent file bloat 検出。"
     "dead-code 削除 or budget を上げる contract 更新"),
    blocking=True,
)

# ── 271. root JS byte budget (BLOCKING) ───────────────────────────────────────
# main.js <= 100_000 / sw.js <= 20_000 / 4 root scripts each <= 10_000 bytes を
# BLOCKING 強制。silent script bloat による parse/execute time 増大を阻止。
# Check 120 (JS 総 weight) の per-file 軸版。
_BUDGETS271 = [
    (ROOT / "main.js", 100_000, "main.js"),
    (ROOT / "sw.js", 20_000, "sw.js"),
    (ROOT / "aio-guard.js", 10_000, "aio-guard.js"),
    (ROOT / "theme-init.js", 10_000, "theme-init.js"),
    (ROOT / "karte-init.js", 10_000, "karte-init.js"),
    (ROOT / "error-suppressor.js", 10_000, "error-suppressor.js"),
]
_violations271: list[str] = []
for _p, _budget, _label in _BUDGETS271:
    if not _p.exists():
        _violations271.append(f"{_label} 不在")
        continue
    _sz = _p.stat().st_size
    if _sz > _budget:
        _violations271.append(f"{_label}={_sz} bytes (budget {_budget})")
_ok271 = not _violations271
check(
    _ok271,
    f"Check 271: root JS ({len(_BUDGETS271)} 件) all within per-file byte budget",
    (f"Check 271: 違反: {_violations271!r} — silent script bloat 検出。"
     "dead-code 削除 or budget を上げる contract 更新"),
    blocking=True,
)

# ── 272. js/*.js leaf module byte budget (BLOCKING) ───────────────────────────
# js/**/*.js の全 leaf module が 100_000 bytes 以下であることを BLOCKING 強制。
# Stage 5 factory 抽出の物理分割 goal を silent bloat から防衛。Check 271 の
# leaf 軸版。
_LEAF_BUDGET272 = 100_000
_leaf_paths272 = (
    _glob237.glob(str(ROOT / "js" / "*.js"))
    + _glob237.glob(str(ROOT / "js" / "quiz" / "*.js"))
)
_violations272: list[str] = []
for _lp in _leaf_paths272:
    _p = Path(_lp)
    _sz = _p.stat().st_size
    if _sz > _LEAF_BUDGET272:
        _violations272.append(f"{_p.relative_to(ROOT)}={_sz} bytes (budget {_LEAF_BUDGET272})")
_ok272 = len(_leaf_paths272) > 0 and not _violations272
check(
    _ok272,
    f"Check 272: js leaf modules ({len(_leaf_paths272)} 件) all <= {_LEAF_BUDGET272} bytes",
    (f"Check 272: 違反: {_violations272!r} — leaf bloat で Stage 5 分割 goal 崩壊。"
     "更に細分化 or budget contract 更新"
     if _violations272 else
     "Check 272: leaf module 0 件 — vacuous-fail"),
    blocking=True,
)

# ── 273. JSON-LD dates NOT in future (BLOCKING) ───────────────────────────────
# index.html JSON-LD の全 `datePublished` / `dateModified` / `dateCreated` 値が
# today 以下であることを BLOCKING 強制。Check 243 (SITE_CONFIG/ai:last-modified
# not future) の JSON-LD date 軸版。
from datetime import date as _date273
_idx273 = ROOT / "index.html"
if _idx273.exists():
    _isrc273 = _idx273.read_text(encoding="utf-8")
    _today273 = _date273.today()
    _date_fields273 = ("datePublished", "dateModified", "dateCreated")
    _blocks273 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc273,
        flags=re.DOTALL,
    )
    _futures273: list[str] = []
    _total_dates273 = 0
    def _walk273(node: object, path: str) -> None:
        global _total_dates273
        if isinstance(node, dict):
            for _f in _date_fields273:
                _v = node.get(_f)
                if isinstance(_v, str):
                    _total_dates273 += 1
                    try:
                        _d = _date273.fromisoformat(_v[:10])
                    except ValueError:
                        continue  # Check 208 が format を担う
                    if _d > _today273:
                        _futures273.append(f"{path}.{_f}={_v!r}")
            for k, v in node.items():
                _walk273(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk273(item, f"{path}[{i}]")
    for _bi, _blk in enumerate(_blocks273):
        try:
            _walk273(json.loads(_blk), f"block{_bi}")
        except json.JSONDecodeError:
            continue
    _ok273 = _total_dates273 > 0 and not _futures273
    check(
        _ok273,
        f"Check 273: JSON-LD date ({_total_dates273} 件) 全て today ({_today273.isoformat()}) 以前",
        (f"Check 273: 未来日 detected: {_futures273!r} — AI/SEO recency 誤認 / "
         "ranking corruption。today 以下へ修正"),
        blocking=True,
    )
else:
    check(False, "Check 273: index.html present",
          "Check 273: index.html が無い", blocking=True)

# ── 274. aio-manifest entity.name == primary Person.name (JSON-LD) (BLOCKING) ─
# .well-known/aio-manifest.json の entity.name が index.html JSON-LD の primary
# Person node (@id == canonical+#person) の name と strict 一致することを BLOCKING
# 強制。Check 172 (name variants combined) の direct-equality 軸版。
_mani274 = ROOT / ".well-known" / "aio-manifest.json"
_idx274 = ROOT / "index.html"
if _mani274.exists() and _idx274.exists():
    try:
        _mdata274 = json.loads(_mani274.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        _mdata274 = None
    _entity_name274 = None
    if isinstance(_mdata274, dict):
        _entity_name274 = _mdata274.get("entity", {}).get("name")
    _isrc274 = _idx274.read_text(encoding="utf-8")
    _canon274_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc274
    )
    _canon274 = _canon274_m.group(1) if _canon274_m else None
    _expected_pid274 = (_canon274 or "") + "#person"
    _blocks274 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc274,
        flags=re.DOTALL,
    )
    _primary_pname274 = None
    def _walk274(node: object) -> None:
        global _primary_pname274
        if isinstance(node, dict):
            if (
                node.get("@type") == "Person"
                and node.get("@id") == _expected_pid274
                and _primary_pname274 is None
                and isinstance(node.get("name"), str)
            ):
                _primary_pname274 = node["name"]
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk274(item)
                else:
                    _walk274(v)
        elif isinstance(node, list):
            for item in node:
                _walk274(item)
    for _blk in _blocks274:
        try:
            _walk274(json.loads(_blk))
        except json.JSONDecodeError:
            continue
    _ok274 = (
        isinstance(_entity_name274, str)
        and isinstance(_primary_pname274, str)
        and _entity_name274 == _primary_pname274
    )
    check(
        _ok274,
        f"Check 274: aio-manifest entity.name={_entity_name274!r} == primary Person.name={_primary_pname274!r}",
        (f"Check 274: name drift: aio-manifest.entity.name={_entity_name274!r}, "
         f"JSON-LD primary Person.name={_primary_pname274!r} — entity identity split。"
         "両者を同一 canonical name へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 274: aio-manifest.json + index.html present",
          "Check 274: aio-manifest.json もしくは index.html が無い", blocking=True)

# ── 275. aio-manifest affiliation.organization_name == JSON-LD Org.name (BLOCKING) ─
# .well-known/aio-manifest.json の entity.affiliation.organization_name が
# index.html JSON-LD primary Organization node (@id ==
# https://nkgr.co.jp/#organization) の name と strict 一致することを BLOCKING 強制。
# Check 274 の Organization 軸版。
_PRIMARY_ORG_ID275 = "https://nkgr.co.jp/#organization"
_mani275 = ROOT / ".well-known" / "aio-manifest.json"
_idx275 = ROOT / "index.html"
if _mani275.exists() and _idx275.exists():
    try:
        _mdata275 = json.loads(_mani275.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        _mdata275 = None
    _aff_org275 = None
    if isinstance(_mdata275, dict):
        _aff_org275 = (
            _mdata275.get("entity", {}).get("affiliation", {}).get("organization_name")
        )
    _isrc275 = _idx275.read_text(encoding="utf-8")
    _blocks275 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc275,
        flags=re.DOTALL,
    )
    _primary_org_name275 = None
    def _walk275(node: object) -> None:
        global _primary_org_name275
        if isinstance(node, dict):
            if (
                node.get("@type") == "Organization"
                and node.get("@id") == _PRIMARY_ORG_ID275
                and _primary_org_name275 is None
                and isinstance(node.get("name"), str)
            ):
                _primary_org_name275 = node["name"]
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk275(item)
                else:
                    _walk275(v)
        elif isinstance(node, list):
            for item in node:
                _walk275(item)
    for _blk in _blocks275:
        try:
            _walk275(json.loads(_blk))
        except json.JSONDecodeError:
            continue
    _ok275 = (
        isinstance(_aff_org275, str)
        and isinstance(_primary_org_name275, str)
        and _aff_org275 == _primary_org_name275
    )
    check(
        _ok275,
        f"Check 275: aio-manifest affiliation.organization_name={_aff_org275!r} == JSON-LD Organization.name={_primary_org_name275!r}",
        (f"Check 275: Organization name drift: aio-manifest={_aff_org275!r} / "
         f"JSON-LD={_primary_org_name275!r} — employer identity split。両者を同一値へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 275: aio-manifest.json + index.html present",
          "Check 275: aio-manifest.json もしくは index.html が無い", blocking=True)

# ── 276. aio-manifest affiliation.organization_url == JSON-LD Org.url (BLOCKING) ─
# .well-known/aio-manifest.json の entity.affiliation.organization_url が
# index.html JSON-LD primary Organization (@id == https://nkgr.co.jp/#organization)
# の url と strict 一致することを BLOCKING 強制。Check 275 の url 軸版。
_PRIMARY_ORG_ID276 = "https://nkgr.co.jp/#organization"
_mani276 = ROOT / ".well-known" / "aio-manifest.json"
_idx276 = ROOT / "index.html"
if _mani276.exists() and _idx276.exists():
    try:
        _mdata276 = json.loads(_mani276.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        _mdata276 = None
    _aff_url276 = None
    if isinstance(_mdata276, dict):
        _aff_url276 = (
            _mdata276.get("entity", {}).get("affiliation", {}).get("organization_url")
        )
    _isrc276 = _idx276.read_text(encoding="utf-8")
    _blocks276 = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        _isrc276,
        flags=re.DOTALL,
    )
    _primary_org_url276 = None
    def _walk276(node: object) -> None:
        global _primary_org_url276
        if isinstance(node, dict):
            if (
                node.get("@type") == "Organization"
                and node.get("@id") == _PRIMARY_ORG_ID276
                and _primary_org_url276 is None
                and isinstance(node.get("url"), str)
            ):
                _primary_org_url276 = node["url"]
            for v in node.values():
                if isinstance(v, list):
                    for item in v:
                        _walk276(item)
                else:
                    _walk276(v)
        elif isinstance(node, list):
            for item in node:
                _walk276(item)
    for _blk in _blocks276:
        try:
            _walk276(json.loads(_blk))
        except json.JSONDecodeError:
            continue
    _ok276 = (
        isinstance(_aff_url276, str)
        and isinstance(_primary_org_url276, str)
        and _aff_url276 == _primary_org_url276
    )
    check(
        _ok276,
        f"Check 276: aio-manifest affiliation.organization_url={_aff_url276!r} == JSON-LD Organization.url={_primary_org_url276!r}",
        (f"Check 276: Organization url drift: aio-manifest={_aff_url276!r} / "
         f"JSON-LD={_primary_org_url276!r} — canonical URL split。両者を同一値へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 276: aio-manifest.json + index.html present",
          "Check 276: aio-manifest.json もしくは index.html が無い", blocking=True)

# ── 277. aio-manifest entity.authoritative_context == canonical+llms-full.txt (BLOCKING) ─
# .well-known/aio-manifest.json の entity.authoritative_context 値が
# canonical URL + "llms-full.txt" に一致することを BLOCKING 強制。
_mani277 = ROOT / ".well-known" / "aio-manifest.json"
_idx277 = ROOT / "index.html"
if _mani277.exists() and _idx277.exists():
    try:
        _mdata277 = json.loads(_mani277.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        _mdata277 = None
    _auth_ctx277 = None
    if isinstance(_mdata277, dict):
        _auth_ctx277 = _mdata277.get("entity", {}).get("authoritative_context")
    _isrc277 = _idx277.read_text(encoding="utf-8")
    _canon277_m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc277
    )
    _canon277 = _canon277_m.group(1) if _canon277_m else None
    _expected277 = (_canon277 or "") + "llms-full.txt"
    _ok277 = (
        isinstance(_auth_ctx277, str)
        and _auth_ctx277 == _expected277
    )
    check(
        _ok277,
        f"Check 277: aio-manifest entity.authoritative_context={_auth_ctx277!r} == canonical+llms-full.txt={_expected277!r}",
        (f"Check 277: authoritative_context drift: aio-manifest={_auth_ctx277!r} / "
         f"expected={_expected277!r} — AI/agent authoritative-context ingestion 誤 route"),
        blocking=True,
    )
else:
    check(False, "Check 277: aio-manifest.json + index.html present",
          "Check 277: aio-manifest.json もしくは index.html が無い", blocking=True)

# ── 278. sitemap.xml all <loc> URLs use HTTPS (BLOCKING) ──────────────────────
# sitemap.xml の全 <loc> URL が `https://` で始まることを BLOCKING 強制 (negative
# invariant: http:// 0)。drift で crawler が非 secure transport で URL を取得。
_sitemap278 = ROOT / "sitemap.xml"
if _sitemap278.exists():
    _ssrc278 = _sitemap278.read_text(encoding="utf-8")
    _locs278 = re.findall(r"<loc>([^<]+)</loc>", _ssrc278)
    _bad278 = [u for u in _locs278 if u.startswith("http://")]
    _ok278 = len(_locs278) > 0 and not _bad278
    check(
        _ok278,
        f"Check 278: sitemap.xml <loc> URLs {len(_locs278)} 件全て HTTPS",
        (f"Check 278: sitemap.xml に non-HTTPS <loc>: {_bad278!r} — crawler が "
         "insecure transport で fetch。https:// に揃えよ"
         if _bad278 else
         "Check 278: sitemap.xml <loc> 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 278: sitemap.xml present",
          "Check 278: sitemap.xml が無い", blocking=True)

# ── 279. robots.txt Sitemap: directive URL HTTPS (BLOCKING) ───────────────────
# robots.txt の全 `Sitemap:` directive の URL が `https://` で始まることを
# BLOCKING 強制。Check 278 の robots.txt sitemap-directive 軸版。
_robots279 = ROOT / "robots.txt"
if _robots279.exists():
    _rsrc279 = _robots279.read_text(encoding="utf-8")
    _smaps279 = re.findall(r"^Sitemap:\s*(\S+)", _rsrc279, flags=re.MULTILINE)
    _bad279 = [u for u in _smaps279 if u.startswith("http://")]
    _ok279 = len(_smaps279) > 0 and not _bad279
    check(
        _ok279,
        f"Check 279: robots.txt Sitemap: URL {len(_smaps279)} 件全て HTTPS",
        (f"Check 279: robots.txt に non-HTTPS Sitemap: {_bad279!r} — crawler が "
         "insecure transport で sitemap fetch。https:// に揃えよ"
         if _bad279 else
         "Check 279: robots.txt Sitemap: 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 279: robots.txt present",
          "Check 279: robots.txt が無い", blocking=True)

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
