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
