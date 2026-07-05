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
  7.  index.html CSP meta appears before inline suppressor script (error-suppressor inlined)
  7b. index.html CSP authorizes inline suppressor (hash recomputed from live content)
  7c. index.html CSP authorizes inline speculation rules (hash recomputed from live content)
  9.  sitemap.xml is valid XML
  10. All .github/scripts/*.py parse without syntax errors
  11. aio_monitoring.py summary dict contains 'enabled_engines' and 'total_cited_count'
  12. No stale "72回/72回以上" in current-description files (history lines exempt)
  13. "70超" appears only in history/log context
  14. v1→v74 canonical declaration present in index.html or AI2AI.md
  15. Project Pages robots/.well-known constraint documented (llms-full.txt / AI2AI.md / README.md)
  17. ai:last-modified (index.html) == SITE_CONFIG.LAST_UPDATED (main.js)
  18. sitemap.xml root <lastmod> == ai:last-modified (per-URL lastmod policy)
  19. sw.js CACHE_NAME version == ai:version
  21. llms alias files Last-Updated are in sync
  22. AI2AI.md Session Record headers are in ascending order
  23. .github/workflows/*.yml and dependabot.yml parse without YAML syntax errors
  24. llms-full.txt Last-Updated is within 7 days of AI2AI.md and >= v75-v78 floor
  25. aio-monitoring-log.json has an evidence_policy key (attempt_log_only honesty)
  26. aio-manifest.json archive role #1-#N matches AI2AI-archive.md max Session Record
  27. llms-full.txt has no stale C1–C6 in current-constraint context (should be C1–C7)
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
  72. ESLint baseline absolute-ceiling contract: file-size-budget.md の
      `<!-- ESLINT-BASELINE-DATA <N> -->` ブロックが記録する warning 数 baseline N が、
      sanity ceiling (200) を超えないことを機械強制する。Check 60 (ADVISORY 監視) を BLOCKING
      化した姉妹 Check で、baseline 値が極端に大きい drift も同時に検出する。Plan A の
      「絶対防衛線」を main.js / sw.js の AIDK Kernel 保護領域に手を入れることなく達成する
      設計。baseline marker が消失している場合も BLOCKING で fail。(BLOCKING)
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
  141. Default-project slug & id uniqueness: store.js defaultProjects (the hardcoded proj("pNN","slug",…)
       seed list) must have unique ids AND unique slugs. ProjectDetailPage resolves a project via
       find(p.slug === slug) and returns the FIRST match, so a duplicate slug silently makes the later
       project's detail page unreachable (the #154 class). User-added projects get a runtime slug-suffix
       dedup in addProjectManual, but the hardcoded defaults have NO such protection — a future data edit
       introducing a duplicate slug/id would ship a silently-unreachable project. This Check parses the
       proj(...) seed entries and asserts both id-set and slug-set are collision-free. (BLOCKING)
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
  201. JSON-LD WebSite/WebPage `@id` derive from canonical URL: in index.html
       JSON-LD, the primary WebSite block's `@id` must equal canonical URL +
       "#website" and the primary WebPage block's `@id` must equal canonical
       URL + "#webpage". Drift would fragment the entity graph in the same
       way Check 200 catches for Person — secondary `isPartOf:{"@id":...
       #website}` and `mainEntity:{"@id":...#webpage}` references would
       point to dead anchors. Completes the Person/WebSite/WebPage @id
       anchor triangle that started in Check 200. (BLOCKING)
  215. `<meta name="ai:last-modified">` and SITE_CONFIG.LAST_UPDATED are
       strict ISO-8601 YYYY-MM-DD (format + real calendar date): both date
       sources (the ai:* AIO meta and the main.js SITE_CONFIG constant)
       must match a strict `^\d{4}-\d{2}-\d{2}$` regex AND parse as a real
       calendar date. Check 180 enforces byte-equality between the two but
       both could silently drift together to a non-ISO format (e.g.
       `2026/06/30` or `2026-13-01`) corrupting recency signals. Sibling of
       Check 208 (JSON-LD date ISO-8601) for the ai:* / SITE_CONFIG date
       surface. (BLOCKING)

  236. aio-manifest.json `generated_at` is strict RFC 3339 datetime AND
       affiliation `start_date` is strict YYYY-MM-DD: the `generated_at`
       top-level field must match `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`
       and `entity.affiliation.start_date` must match `^\d{4}-\d{2}-\d{2}$`
       AND parse as a real calendar date/time. Sibling of Check 93
       (last_metadata_update format) for the generated_at + start_date
       fields. Drift would silently corrupt recency / employment-timeline
       signals consumed by AI/SEO. (BLOCKING)

  238. HTML head singleton tags each appear exactly once: index.html must
       contain exactly 1 of each of `<title>`, `<link rel="canonical">`,
       `<meta name="description">`, `<meta property="og:url">`,
       `<meta property="og:title">`. Multiple instances are SILENT class
       drift — browsers/crawlers pick "first" or "last" non-deterministically
       and the duplicate dilutes the canonical entity signal. Sibling of
       Check 17/180 (date sync) for the head singleton uniqueness axis.
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

  304. All `<meta name="theme-color">` values are 6-digit hex colors:
       every `<meta name="theme-color">` content in index.html MUST match
       `^#[0-9a-fA-F]{6}$`. Drift = mobile browser chrome color falls
       back to default (loses brand cohesion). Sibling of Check 174
       (theme-color literals in style.css) for the theme-color value-
       format axis. (BLOCKING)

  305. `<meta name="theme-color">` has both light AND dark media
       variants: index.html MUST contain one theme-color for
       `media="(prefers-color-scheme: light)"` AND one for
       `media="(prefers-color-scheme: dark)"`. Drift silently makes
       mobile browser chrome color inconsistent between OS-level
       light/dark modes. Sibling of Check 304 (theme-color hex format)
       for the theme-color media-coverage axis. (BLOCKING)

  307. sitemap.xml opens with XML declaration + closes with `</urlset>`:
       sitemap.xml MUST start with `<?xml version="1.0" encoding="UTF-8"?>`
       and end with `</urlset>` (trailing whitespace allowed). Drift =
       structurally malformed sitemap parses as invalid → crawler drops
       entire sitemap. Sibling of Check 306 (index.html structural
       closure) for the sitemap.xml structural axis. (BLOCKING)

  308. sitemap.xml `<urlset>` declares both sitemap + image namespaces:
       the sitemap.xml `<urlset>` opening tag MUST declare both
       `xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"` AND
       `xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"`.
       Drift = `<image:image>` blocks parsed as unknown → Google Image
       sitemap coverage collapses. Sibling of Check 297 (canonical entry
       image:image) for the sitemap.xml namespace-declaration axis.
       (BLOCKING)

  309. .well-known/aio-manifest.json all URLs use HTTPS: the manifest
       JSON MUST NOT contain any `http://` URL (negative invariant).
       Drift silently downgrades AIO discovery transport security.
       Sibling of Check 232/233/234 (ai:* / asset:* HTTPS) for the
       aio-manifest.json HTTPS axis. (BLOCKING)

  338. `<meta property="og:image:width">` / `og:image:height` declared
       values MUST equal the ACTUAL pixel dimensions of the hero WebP
       (parsed directly from the VP8X/VP8/VP8L chunk header — no external
       library). Drift = the hero image is re-exported at a different
       resolution but the meta tags are not updated; social-card
       consumers that trust the declared dimensions render the card with
       a wrong aspect ratio (letterboxing / cropping) or reject the image.
       Check 298 verifies the values are positive integers but not that
       they match reality. Sibling of Check 298 (og:image dims positive
       int) / Check 337 (magic bytes) for the hero-image dimension-truth
       axis. (BLOCKING)

  339. Every JSON-LD `ImageObject` for the hero WebP that declares
       `width` / `height` MUST match the ACTUAL pixel dimensions of the
       hero WebP file. Drift = the image is re-exported at a new
       resolution and og:image (Check 338) gets updated but the JSON-LD
       ImageObject width/height stays stale — AI crawlers / knowledge
       graphs then ingest a wrong dimension for the entity's primary
       image. (This Check was born from a real drift found 2026-07-04:
       JSON-LD declared 1200x630 while the file was 1536x1024, corrected
       under C6 orchestrator approval.) Sibling of Check 338 (og:image
       dims == actual) for the JSON-LD ImageObject dimension-truth axis.
       (BLOCKING)

  340. Every JSON-LD `ImageObject` / `AudioObject` `encodingFormat` MIME
       for the hero WebP / BGM MP3 MUST match the ACTUAL binary format
       (webp→`image/webp`, mp3→`audio/mpeg`, from magic bytes). Drift =
       the JSON-LD declares a MIME (`image/png`, `audio/wav`) that
       disagrees with the real bytes — AI crawlers ingest a wrong
       content-type for the entity's primary media, and consumers that
       trust the declared MIME mis-decode. Check 337 verifies the magic
       bytes match the extension; this closes the JSON-LD MIME leg of the
       same truth. Sibling of Check 337 (magic bytes) / Check 339 (JSON-LD
       dims) for the binary-asset declaration-truth axis. (BLOCKING)

  348. Both BLOCKING gate workflows (`architecture-validation.yml` and
       `playwright-regression.yml`) MUST declare a `pull_request` trigger
       targeting the `main` branch in their `on:` block. This completes
       the meta-guard family: Check 346/347 verify the gates are INVOKED
       and BLOCKING, but a workflow whose `pull_request:` trigger is
       removed simply never runs on PRs — the `run:` step is present yet
       never executes, so PRs merge un-gated while CI shows no failure
       (there is nothing to fail). Sibling of Check 346 (consistency
       invocation) / Check 347 (behavior invocation) for the
       CI-triggers-the-guard axis. (BLOCKING)

  349. `icon.svg` (the favicon / PWA icon, declared `type="image/svg+xml"`
       in both index.html `<link rel="icon">` and manifest.webmanifest)
       MUST actually be a well-formed SVG: its content starts with `<?xml`
       or `<svg` (after optional BOM/whitespace) AND contains a `</svg>`
       close tag AND the `xmlns="http://www.w3.org/2000/svg"` namespace.
       Drift = a non-SVG file saved as `icon.svg` (a PNG, a truncated
       export); the declared `image/svg+xml` MIME lies, browsers reject
       the favicon (generic globe) and the PWA install icon fails.
       Sibling of Check 337 (hero/BGM magic bytes) for the icon-asset
       format-integrity axis. (BLOCKING)

  350. The inline event-handler `onload="this.media='all'"` (the async
       font-loading trick) MUST have its exact-content SHA-256 hash
       present in the CSP `script-src` (authorized via `'unsafe-hashes'`).
       Check 7b/7c cover the two inline `<script>` blocks; this covers the
       third CSP hash — the inline handler. Drift = editing the handler
       value (e.g. `this.media='screen'`) without recomputing the CSP
       hash makes Chrome BLOCK the handler, so the print-media stylesheet
       never flips to `all` and the fonts never load (FOUC / wrong font),
       silently. Computed from live handler content (not a constant), so
       both a removed hash and an edited-without-rehash handler are
       caught. Sibling of Check 7b (suppressor hash) / Check 7c
       (speculation-rules hash) / Check 242 (handler allowlist) for the
       inline-CSP-hash integrity axis. (BLOCKING)

  360. Every `<meta name="asset:*:canonical">` content URL (currently
       `asset:image:canonical` → hero WebP, `asset:audio:canonical` → BGM
       MP3) MUST resolve (after stripping the canonical prefix) to an
       existing local file. Check 234 verifies these URLs share the
       canonical prefix but NOT that they point at a real file — so a
       rename that updates the filename in the URL while leaving the
       prefix intact stays green under 234 yet declares an AIO canonical
       asset that 404s. AI crawlers that fetch the declared canonical
       asset get a dead link, corrupting the entity's asset authority.
       Sibling of Check 234 (asset:* canonical prefix) / Check 164
       (og:image resolves) for the AIO-asset-canonical resolution axis.
       (BLOCKING)

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
    ROOT / ".github" / "scripts" / "checks_maintainability.py",  # split: maintainability/test-health/file-size
    ROOT / ".github" / "scripts" / "checks_structural.py",  # split: structural / CI wiring / tooling (48-51)
    ROOT / ".github" / "scripts" / "checks_esm.py",  # split: ESM contract cluster (47/56/57/61)
    ROOT / ".github" / "scripts" / "checks_tooling.py",  # split: dev-tooling/.claude config cluster (74-80)
    ROOT / ".github" / "scripts" / "checks_entity.py",  # split: entity/Organization cross-surface cluster (81-90)
    ROOT / ".github" / "scripts" / "checks_docs_mirror.py",  # split: docs/files mirror-doc governance (96-99)
    ROOT / ".github" / "scripts" / "checks_aio_derived.py",  # split: AIO C6 derived-value & date tooling (91-95)
    ROOT / ".github" / "scripts" / "checks_app_route.py",  # split: app-route whitelist coherence-mesh (136-140)
    ROOT / ".github" / "scripts" / "checks_ci_supply.py",  # split: CI/workflow coverage & supply-chain (142-145)
    ROOT / ".github" / "scripts" / "checks_behavioral.py",  # split: shipped-JS behavioral regression guards (128-131)
    ROOT / ".github" / "scripts" / "checks_shipped_structure.py",  # split: shipped-JS structural coherence & byte budget (118-120)
    ROOT / ".github" / "scripts" / "checks_wiring.py",  # split: shipped-asset & AIO wiring/discoverability (132-134)
    ROOT / ".github" / "scripts" / "checks_aio_entity.py",  # split: AIO manifest entity-field & identity coherence (167-173)
    ROOT / ".github" / "scripts" / "checks_seo_coherence.py",  # split: AIO/SEO URL-canonical-format coherence (273-302)
    ROOT / ".github" / "scripts" / "checks_sitemap_manifest.py",  # split: 311-320
    ROOT / ".github" / "scripts" / "checks_html_standards.py",  # split: 324-337
    ROOT / ".github" / "scripts" / "checks_jsonld_entity.py",  # split: 191-200
    ROOT / ".github" / "scripts" / "checks_jsonld_meta.py",  # split: 221-235
    ROOT / ".github" / "scripts" / "checks_meta_url.py",  # split: 175-180
    ROOT / ".github" / "scripts" / "checks_canonical_https.py",  # split: 202-214
    ROOT / ".github" / "scripts" / "checks_shipped_hygiene.py",  # split: 242-249
    ROOT / ".github" / "scripts" / "checks_jsonld_primary.py",  # split: 256-261
    ROOT / ".github" / "scripts" / "checks_jsonld_refs.py",  # split: 216-219
    ROOT / ".github" / "scripts" / "checks_sw_pwa.py",  # split: 251-254
    ROOT / ".github" / "scripts" / "checks_csp_security.py",  # split: 351-355
    ROOT / ".github" / "scripts" / "checks_ci_verify.py",  # split: 345-347
    ROOT / ".github" / "scripts" / "checks_meta_validity.py",  # split: 341-343
    ROOT / ".github" / "scripts" / "checks_asset_resolve.py",  # split: 357-359
    ROOT / ".github" / "scripts" / "checks_html.py",  # split: index.html document/meta baseline & lang coherence (8/20/115/152/187/220/250/255/303/306・ctx-enrich html)
    ROOT / ".github" / "scripts" / "checks_css.py",  # split: style.css / CSS contract (6/73/101/103/135/174/321-323/344/356・ctx-enrich style)
    ROOT / ".github" / "scripts" / "checks_shipped_static.py",  # split: shipped-JS static analysis + byte budgets (237/239-241/262-265/269-272/310)
    ROOT / ".github" / "scripts" / "checks_e2e_infra.py",  # split: e2e/Playwright test-infra hygiene (110/111/114/116/117)
]


def _aggregate_check_numbers():
    """(inventory_nums, section_nums) sorted, aggregated across CHECK_SOURCE_FILES.

    inventory_nums = `  N. ` lines in each file's module docstring (first triple-quoted block).
    section_nums   = the `# <box-drawing> N.` section-header numbers in each file's body.
    Self-integrity Checks 45/70/105 use this so the bijection spans every split check module.
    NOTE: leading whitespace is tolerated on the section header so an extracted module can keep
    its `# ── N.` headers inside `def run(ctx):` (indented) — see checks_maintainability.py.
    """
    _sec_re = re.compile(r'^\s*#\s*──\s*(\d+)\.', re.MULTILINE)
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


# ── Shared check context for extracted check modules (Phase 1 check.py split) ──
# checks_maintainability.run(_ctx) 等の抽出 module に「monolith と同一の」check()/errors/warnings/
# ROOT/read 等を明示注入する。errors/warnings は同一 list オブジェクトを参照で渡すため、抽出 module の
# check() 呼び出しも同じ errors/warnings に append する = 挙動 byte-equivalent。exec() を使わず module-
# global 結合も無いので #253 が指摘した net-negative (自由変数の静的解決不能・未定義グローバル参照) を回避。
import types as _types
_ctx = _types.SimpleNamespace(
    ROOT=ROOT, check=check, read=read, read_bytes=read_bytes,
    extract=extract, errors=errors, warnings=warnings,
)


# ── Load files ──────────────────────────────────────────────────────────────
html       = read("index.html")
ai2ai      = read("AI2AI.md")
mainjs     = read("main.js")
style      = read("style.css")
aio_mon    = read(".github/scripts/aio_monitoring.py")

mcp_data   = json.loads(read(".well-known/mcp.json"))

# ── ctx enrichment for split modules that read shared global content (check.py split track) ──
# split-out checks_* modules that need the pre-loaded style.css (etc.) content unpack it from ctx
# (avoids re-reading). Added AFTER the globals load so the value already exists on _ctx. Only the
# content actually consumed by an extracted module is attached here — extend as further glob-
# dependent categories (html / mainjs / ai2ai / mcp_data) are split out in later phases.
_ctx.style = style
_ctx.html = html

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

# ── 6/73/101/103/135/174/321-323/344/356. style.css / CSS contract → checks_css.py ──
# (check.py split track・first ctx-enrich module。style glob を _ctx.style 経由で消費。forced-colors/HCM/
#  prefers-contrast a11y(101/103)/theme-color(174)/a11y-CWV attr(73)/@import·inline·@layer(321-323/344)/
#  Google-Fonts CSP(356)/token baseline(6/135)。非連続・style 以外の cross-section 結合なし。6 位置で
#  list 順連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_css as _checks_css
_checks_css.run(_ctx)

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

# ── 8/20/115/152/187/220/250/255/303/306. index.html document/meta baseline & lang coherence → checks_html.py ──
# (check.py split track・ctx-enrich module。html glob を _ctx.html 経由で消費。security meta(8/115)/
#  og:image dims(20)/<html lang> coherence(152/187/220/250)/doc structure(255/306)/data-attr(303)。
#  Check 7 は _lib_io.csp_sri_hash helper 依存ゆえ除外。8 位置で list 順連続実行。CHECK_SOURCE_FILES 登録。)
import checks_html as _checks_html
_checks_html.run(_ctx)

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
            # 肥大化解消でページが js/<name>-page.js へ分離されたため、featuring layer
            # (Zenn slug) を含みうる全ページ leaf を集約に含める (HomePage→home-page.js 等)。
            for _aux33 in (_p33, ROOT / "js" / "components.js",
                           ROOT / "js" / "home-page.js",
                           ROOT / "js" / "ai-knowhow-page.js"):
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

# ── 47 / 56 / 57 / 61. main.js ⇄ js/ leaf-module ESM contract & factory coherence → checks_esm.py ──
# (check.py split track・category "ESM contract". These four Checks share the `_modules47`
#  leaf-module source-of-truth list + `_main_src47` (main.js source); extracting the list together
#  with all its consumers (47 import/export bijection・56 factory params・57 modulepreload set・61
#  factory docstring) resolves the coupling that kept them in the monolith through Phase 5. Executed
#  at 47's original position; 56/57/61 now run adjacent to 47 rather than interleaved with 53-60 —
#  order-independent since each Check only appends to the shared errors/warnings. CHECK_SOURCE_FILES
#  registration makes self-integrity 45/70/105 aggregate across this module.)
import checks_esm as _checks_esm
_checks_esm.run(_ctx)

# ── 48-51. structural / CI wiring / tooling checks → checks_structural.py ──────
# (check.py split track. 元の実行位置=47 の後・53 の前を保持して ctx で呼ぶ。CHECK_SOURCE_FILES 登録で
#  自己整合 Check 45/70/105 が横断集約。48-51 は _NN 接尾辞 local + file fresh read の self-contained cluster。
#  47/56/57/61 (_modules47 共有クラスタ) は checks_esm.py へ抽出済 (直上)。)
import checks_structural as _checks_structural
_checks_structural.run(_ctx)

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

# ── 74-80. dev-tooling / .claude config-file integrity checks → checks_tooling.py ──
# (check.py split track・category "dev-tooling/.claude config". _lib_io helper API (74) /
#  incident README inventory (75) / .claude settings baseline (76) / commands (77) / agents (78)
#  frontmatter / .mcp.json parsability (79) / skills SKILL.md frontmatter (80). Contiguous
#  self-contained cluster — each Check reads its own target file directly (no global content dep),
#  so no ctx enrich needed. 元の実行位置 (73 の後・81 の前) を保持。CHECK_SOURCE_FILES 登録で
#  自己整合 Check 45/70/105 が横断集約。)
import checks_tooling as _checks_tooling
_checks_tooling.run(_ctx)


# ── 81-90. AIO entity / employer-Organization cross-surface coherence → checks_entity.py ──
# (check.py split track・category "entity/Organization". WebP XMP (81) / MP3 ID3 (82) binary
#  Organization fields / aio-manifest affiliation (83) + entity full-set (86) / README (84) /
#  Claude2Claude (85) Organization mention / CLAUDE.md cold-start entity (87) / LICENSE (88) /
#  governance-file presence (89) / .claude entity (90). Contiguous self-contained cluster —
#  READ-ONLY presence assertions reading their own target files directly (no global content dep,
#  no C6 edit). 元の実行位置 (80 の後・91 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_entity as _checks_entity
_checks_entity.run(_ctx)


# ── 91-95. AIO C6 derived-value & date-sync tooling integrity → checks_aio_derived.py ──
# (check.py split track・category "AIO derived-value". binary date freshness (91) / C6 canon
#  presence (92) / manifest last_metadata_update (93) / update_aio tools integrity (94) /
#  _lib_io date helpers (95). Contiguous self-contained cluster — READ-ONLY assertions reading
#  their own files directly (no global content dep, no C6 edit). 元の実行位置 (90 の後・96 の前)
#  を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_aio_derived as _checks_aio_derived
_checks_aio_derived.run(_ctx)


# ── 96-99. docs/files 1-to-1 mirror-doc governance → checks_docs_mirror.py ──
# (check.py split track・category "docs-mirror". shipped-code 1-to-1 docs bijection (96) /
#  frontmatter integrity (97) / 5-axis section presence (98) / README + _template presence (99).
#  Contiguous self-contained cluster reading docs/files/** directly (no global content dep).
#  Check 108 (full tracked-files bijection) は非連続ゆえ monolith 残置。元の実行位置 (95 の後・
#  100 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_docs_mirror as _checks_docs_mirror
_checks_docs_mirror.run(_ctx)


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

# ── 110/111/114/116/117. e2e / Playwright test-infra hygiene → checks_e2e_infra.py ──
# (check.py split track・category "e2e/test-infra". A11Y_ROUTES↔ALL_ROUTES (110) / no-networkidle
#  (111) / no-.only (114) / reuseExistingServer=false (116) / screenshot tolerance ceiling (117)。
#  非連続クラスタ (112 IME / 113 canon / 115 CSP は monolith 残置)。各 Check は e2e spec /
#  playwright.config を自前 read_text (no global content dep)。110 位置で連続実行 (order-independent)。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_e2e_infra as _checks_e2e_infra
_checks_e2e_infra.run(_ctx)

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

# ── 118-120. shipped-JS structural coherence & byte budget → checks_shipped_structure.py ──
# (check.py split track・category "shipped structure". PAGE_META route coverage (118) / factory
#  docstring dependency coherence (119) / shipped JS+CSS byte-weight budget (120)。連続 self-
#  contained クラスタ (free-var 分析で外部 _var ゼロ確認)・自前 read_text (no global content dep)。
#  元の実行位置 (117 の後・121 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_shipped_structure as _checks_shipped_structure
_checks_shipped_structure.run(_ctx)


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
# NOTE (肥大化解消 2026-07-04): 運用モデル記述は ai-knowhow ページ内容にあり、そのページは
# js/components.js から js/ai-knowhow-page.js へ分離された。marker の実在場所が移動しただけで
# 「サイトに現運用モデル記述あり」invariant は不変ゆえ、両ファイルの union を scan する。
_comp123_files = [ROOT / "js" / "components.js", ROOT / "js" / "ai-knowhow-page.js"]
_comp123_t = "".join(
    _f.read_text(encoding="utf-8") for _f in _comp123_files if _f.exists()
)
_site_ok123 = ("現在の運用モデル" in _comp123_t) and ("Claude Code" in _comp123_t) and ("自走" in _comp123_t)
check(
    _site_ok123,
    "Check 123a: site (js/components.js ∪ ai-knowhow-page.js) が現運用モデル (現在の運用モデル + Claude Code + 自走) を保持 (site↔canon coherence)",
    "Check 123a: site 層 (components.js / ai-knowhow-page.js) から現運用モデルの記述が失われた — 「対話型 Claude」だけの旧記述へ "
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

# ── 128-131. shipped-JS behavioral regression guards → checks_behavioral.py ──
# (check.py split track・category "behavioral guards". command-palette↔router coherence (128) /
#  topbar data-action double-fire (129) / live-input oninput focus-loss (130) / sw
#  decodeURIComponent try/catch (131)。連続 self-contained クラスタ — 各 Check は shipped-JS
#  (js/*.js / main.js / sw.js) を自前 read_text (no global content dep)。元の実行位置 (127 の後・
#  132 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_behavioral as _checks_behavioral
_checks_behavioral.run(_ctx)


# ── 132-134. shipped-asset & AIO wiring / discoverability → checks_wiring.py ──
# (check.py split track・category "wiring/discovery". AIO evidence↔sitemap discoverability (132) /
#  aio-guard.js script wiring (133) / root-script wiring completeness (134)。連続 self-contained
#  クラスタ (free-var ゼロ確認)・自前 read_text (no global content dep)。135 (stylesheet wiring) は
#  global style 依存ゆえ monolith 残置。元の実行位置 (131 の後・135 の前) を保持。CHECK_SOURCE_FILES 登録。)
import checks_wiring as _checks_wiring
_checks_wiring.run(_ctx)


# ── 136-140. app-route whitelist coherence-mesh → checks_app_route.py ──
# (check.py split track・category "app-route mesh". js/router.js の app whitelist を single
#  source of truth に、demoRoute (136) / main.js render switch (137) / Sidebar app-nav (138) /
#  AppsPage app index (139) / Settings demo selector (140) の全 producer/consumer 整合を強制。
#  連続 self-contained クラスタ — 各 Check は対象 file を自前 read_text (no global content dep)。
#  元の実行位置 (135 の後・141 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_app_route as _checks_app_route
_checks_app_route.run(_ctx)


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

# ── 142-145. CI / workflow-coverage & supply-chain hardening → checks_ci_supply.py ──
# (check.py split track・category "CI/supply-chain". Playwright e2e gate covers its toolchain
#  (142) / auto-digest workflow covers every digested manifest file (143) / digest-regen tool
#  file-map == manifest (144) / GitHub Actions full-SHA pin (145). Contiguous self-contained
#  cluster reading workflow YAML / tool / manifest directly (no global content dep). 元の実行
#  位置 (141 の後・146 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_ci_supply as _checks_ci_supply
_checks_ci_supply.run(_ctx)


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

# ── 167-173. AIO manifest entity-field & identity coherence → checks_aio_entity.py ──
# (check.py split track・category "AIO entity coherence". aio-monitoring schedule (167) /
#  entity.architecture C1/C2/C3 (168) / entity.role (169) / disambiguation (170) / ai:* meta
#  canonical prefix (171) / entity name variants (172) / identity.js AUTHOR values (173)。連続
#  self-contained クラスタ (annotation-aware free-var 分析でゼロ確認・READ-ONLY・no global content dep)。
#  元の実行位置 (166 の後・174 の前) を保持。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_aio_entity as _checks_aio_entity
_checks_aio_entity.run(_ctx)


# ── 175-180. index.html meta/asset URL resolution & AIO routing coherence checks (175-180) → checks_meta_url.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_meta_url as _checks_meta_url
_checks_meta_url.run(_ctx)


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

# ── 191-200. JSON-LD Person/WebSite/WebPage/Organization canonical entity coherence checks (191-200) → checks_jsonld_entity.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_jsonld_entity as _checks_jsonld_entity
_checks_jsonld_entity.run(_ctx)


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

# ── 202-214. canonical URL, HTTPS-only & manifest/icon path coherence checks (202-214) → checks_canonical_https.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_canonical_https as _checks_canonical_https
_checks_canonical_https.run(_ctx)


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

# ── 216-219. JSON-LD referential integrity checks — @id refs resolve / @id unique / datePublished<=dateModified / manifest paths (216-219) → checks_jsonld_refs.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 1 箇所。)
import checks_jsonld_refs as _checks_jsonld_refs
_checks_jsonld_refs.run(_ctx)


# ── 221-235. JSON-LD ref-type + meta length + sitemap value coherence checks (221-235) → checks_jsonld_meta.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 1 箇所。)
import checks_jsonld_meta as _checks_jsonld_meta
_checks_jsonld_meta.run(_ctx)


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

# ── 237/239/240/241/262-265/269-272/310. shipped-JS static analysis + byte budgets → checks_shipped_static.py ──
# (check.py split track. shipped-JS lint(237/239-241/262-265)+ byte budgets(269-272)+ total weight(310)。
#  非連続 tightly-coupled unit・共有: glob import(_glob237)/_eval_targets239 list/_HERO_WEBP269·_BGM_MP3_269。
#  310 は 269 の binary path を消費するため同梱(部分 slice は 2 度 crash)。238/266-268 は非使用で残置。
#  237 位置で list 順に連続実行。CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。)
import checks_shipped_static as _checks_shipped_static
_checks_shipped_static.run(_ctx)

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

# ── 242-249. shipped-JS/HTML security & hygiene checks — eval/setTimeout-string/document.write/console/loose-eq etc. (242-249) → checks_shipped_hygiene.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 3 箇所。)
import checks_shipped_hygiene as _checks_shipped_hygiene
_checks_shipped_hygiene.run(_ctx)


# ── 251-254. service-worker & PWA registration + potentialAction structure checks (251-254) → checks_sw_pwa.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 1 箇所。)
import checks_sw_pwa as _checks_sw_pwa
_checks_sw_pwa.run(_ctx)


# ── 256-261. JSON-LD primary-node required-field completeness checks — WebPage/Person/WebSite/Org/hero/BGM (256-261) → checks_jsonld_primary.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 6 箇所。)
import checks_jsonld_primary as _checks_jsonld_primary
_checks_jsonld_primary.run(_ctx)


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

# ── 273-302. AIO/SEO cross-surface URL, canonical & format coherence → checks_seo_coherence.py ──
# (check.py split track・category "SEO/URL coherence". canonical URL / HTTPS-only / manifest↔JSON-LD
#  entity equality / strict format (VERSION/CACHE_NAME/manifest_version) / og/twitter/meta coherence の
#  30 Check。連続 self-contained (annotation+def-aware free-var 分析でゼロ確認・READ-ONLY)。nested walker の
#  section-local accumulator は module-level の global を run() 内で nonlocal に機械変換 (意味等価)。
#  元の実行位置 (272 の後・303 の前) を保持。CHECK_SOURCE_FILES 登録で横断集約。)
import checks_seo_coherence as _checks_seo_coherence
_checks_seo_coherence.run(_ctx)


# ── 304. <meta name=theme-color> content values are 6-digit hex (BLOCKING) ────
# index.html の全 `<meta name="theme-color">` content が `^#[0-9a-fA-F]{6}$`
# regex に一致することを BLOCKING 強制。Check 174 (style.css literal) の
# value-format 軸版。
_idx304 = ROOT / "index.html"
if _idx304.exists():
    _isrc304 = _idx304.read_text(encoding="utf-8")
    _tc_vals304 = re.findall(
        r'<meta\s+name=["\']theme-color["\'][^>]*content=["\']([^"\']+)["\']',
        _isrc304,
    )
    _bad304 = [v for v in _tc_vals304 if not re.match(r"^#[0-9a-fA-F]{6}$", v)]
    _ok304 = len(_tc_vals304) > 0 and not _bad304
    check(
        _ok304,
        f"Check 304: <meta name=theme-color> {len(_tc_vals304)} 件全て 6-digit hex",
        (f"Check 304: 非 hex theme-color: {_bad304!r} — mobile browser chrome color "
         "が default fallback。#XXXXXX 形式へ揃えよ"
         if _bad304 else
         "Check 304: <meta name=theme-color> 0 件 — vacuous-fail"),
        blocking=True,
    )
else:
    check(False, "Check 304: index.html present",
          "Check 304: index.html が無い", blocking=True)

# ── 305. <meta name=theme-color> covers both light + dark media (BLOCKING) ────
# index.html に `<meta name=theme-color media="(prefers-color-scheme: light)">`
# AND `<meta name=theme-color media="(prefers-color-scheme: dark)">` 両方が
# 存在することを BLOCKING 強制。Check 304 の media-coverage 軸版。
_idx305 = ROOT / "index.html"
if _idx305.exists():
    _isrc305 = _idx305.read_text(encoding="utf-8")
    _tc_light305 = re.search(
        r'<meta\s+name=["\']theme-color["\'][^>]*media=["\']\(prefers-color-scheme:\s*light\)["\']',
        _isrc305,
    )
    _tc_dark305 = re.search(
        r'<meta\s+name=["\']theme-color["\'][^>]*media=["\']\(prefers-color-scheme:\s*dark\)["\']',
        _isrc305,
    )
    _missing305 = []
    if not _tc_light305:
        _missing305.append("theme-color for light media")
    if not _tc_dark305:
        _missing305.append("theme-color for dark media")
    _ok305 = not _missing305
    check(
        _ok305,
        f"Check 305: theme-color has both light + dark media variants",
        (f"Check 305: 欠落: {_missing305!r} — mobile browser chrome color が "
         "OS-level light/dark mode 遷移で inconsistent。両 media variant を追加"),
        blocking=True,
    )
else:
    check(False, "Check 305: index.html present",
          "Check 305: index.html が無い", blocking=True)

# ── 307. sitemap.xml opens with XML decl + closes with </urlset> (BLOCKING) ───
# sitemap.xml が `<?xml version="1.0" encoding="UTF-8"?>` で始まり `</urlset>`
# で終わることを BLOCKING 強制。Check 306 (index.html structural closure) の
# sitemap.xml structural axis 版。
_sitemap307 = ROOT / "sitemap.xml"
if _sitemap307.exists():
    _ssrc307 = _sitemap307.read_text(encoding="utf-8")
    _bad307: list[str] = []
    if not _ssrc307.lstrip().startswith('<?xml version="1.0" encoding="UTF-8"?>'):
        _bad307.append("XML declaration 欠落/drift")
    if not _ssrc307.rstrip().endswith("</urlset>"):
        _bad307.append("</urlset> closing 欠落")
    _ok307 = not _bad307
    check(
        _ok307,
        "Check 307: sitemap.xml opens with XML decl + closes with </urlset>",
        (f"Check 307: 違反: {_bad307!r} — sitemap.xml structural malformation。"
         "crawler 全 sitemap drop リスク"),
        blocking=True,
    )
else:
    check(False, "Check 307: sitemap.xml present",
          "Check 307: sitemap.xml が無い", blocking=True)

# ── 308. sitemap.xml <urlset> declares both namespaces (BLOCKING) ─────────────
# sitemap.xml の <urlset> tag が sitemap + image 両方の xmlns 宣言を含むことを
# BLOCKING 強制。Check 297 (canonical entry <image:image>) の namespace 軸版。
_sitemap308 = ROOT / "sitemap.xml"
if _sitemap308.exists():
    _ssrc308 = _sitemap308.read_text(encoding="utf-8")
    _required_ns308 = [
        ('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', "sitemap 0.9"),
        ('xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"', "image 1.1"),
    ]
    _urlset308_m = re.search(r"<urlset\s+[^>]*>", _ssrc308, flags=re.DOTALL)
    _urlset308 = _urlset308_m.group(0) if _urlset308_m else ""
    _missing308 = [_label for _pat, _label in _required_ns308 if _pat not in _urlset308]
    _ok308 = not _missing308 and bool(_urlset308_m)
    check(
        _ok308,
        f"Check 308: sitemap.xml <urlset> declares both sitemap + image namespaces",
        (f"Check 308: 欠落 xmlns: {_missing308!r} — <image:image> block が unknown "
         "parse で Google Image sitemap coverage 崩壊"),
        blocking=True,
    )
else:
    check(False, "Check 308: sitemap.xml present",
          "Check 308: sitemap.xml が無い", blocking=True)

# ── 309. aio-manifest.json all URLs HTTPS (BLOCKING) ──────────────────────────
# .well-known/aio-manifest.json に `http://` URL が 0 であることを BLOCKING 強制
# (negative invariant)。Check 232/233/234 の aio-manifest.json HTTPS 軸版。
_mani309 = ROOT / ".well-known" / "aio-manifest.json"
if _mani309.exists():
    _msrc309 = _mani309.read_text(encoding="utf-8")
    _http_urls309 = re.findall(r'"(http://[^"]+)"', _msrc309)
    _ok309 = len(_http_urls309) == 0
    check(
        _ok309,
        "Check 309: aio-manifest.json に http:// URL 不在 (HTTPS-only)",
        (f"Check 309: aio-manifest.json に http:// URL: {_http_urls309!r} — "
         "AIO discovery transport が insecure に downgrade。全 URL を https:// へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 309: aio-manifest.json present",
          "Check 309: aio-manifest.json が無い", blocking=True)

# ── 311-320. sitemap & manifest format/validity coherence checks (311-320) → checks_sitemap_manifest.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_sitemap_manifest as _checks_sitemap_manifest
_checks_sitemap_manifest.run(_ctx)


# ── 324-337. index.html standards/safety hygiene + webmanifest + asset integrity checks (324-337) → checks_html_standards.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_html_standards as _checks_html_standards
_checks_html_standards.run(_ctx)


# ── 338. og:image:width/height == actual hero WebP dimensions (BLOCKING) ─────
def _parse_webp_dims338(_path):
    """外部ライブラリ不要で WebP の pixel 寸法を先頭 chunk から parse。"""
    _b = _path.read_bytes()[:40]
    if _b[0:4] != b"RIFF" or _b[8:12] != b"WEBP":
        return None
    _fourcc = _b[12:16]
    if _fourcc == b"VP8X":
        _w = 1 + int.from_bytes(_b[24:27], "little")
        _h = 1 + int.from_bytes(_b[27:30], "little")
        return (_w, _h)
    if _fourcc == b"VP8 ":
        _w = int.from_bytes(_b[26:28], "little") & 0x3FFF
        _h = int.from_bytes(_b[28:30], "little") & 0x3FFF
        return (_w, _h)
    if _fourcc == b"VP8L":
        _bits = int.from_bytes(_b[21:25], "little")
        _w = (_bits & 0x3FFF) + 1
        _h = ((_bits >> 14) & 0x3FFF) + 1
        return (_w, _h)
    return None

_webp338 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
_html338 = ROOT / "index.html"
if _webp338.is_file() and _html338.is_file():
    _dims338 = _parse_webp_dims338(_webp338)
    _hs338 = re.sub(r"<!--.*?-->", "", _html338.read_text(encoding="utf-8"),
                    flags=re.DOTALL)
    _mw338 = re.search(
        r'<meta\s+property="og:image:width"\s+content="(\d+)"', _hs338)
    _mh338 = re.search(
        r'<meta\s+property="og:image:height"\s+content="(\d+)"', _hs338)
    _declared_w338 = int(_mw338.group(1)) if _mw338 else None
    _declared_h338 = int(_mh338.group(1)) if _mh338 else None
    _problems338: list[str] = []
    if _dims338 is None:
        _problems338.append("hero WebP 寸法を parse できない (未対応 chunk)")
    elif _declared_w338 is None or _declared_h338 is None:
        _problems338.append("og:image:width / og:image:height meta が欠落")
    else:
        _aw338, _ah338 = _dims338
        if (_aw338, _ah338) != (_declared_w338, _declared_h338):
            _problems338.append(
                f"宣言 {_declared_w338}x{_declared_h338} != 実寸 {_aw338}x{_ah338}")
    check(
        not _problems338,
        f"Check 338: og:image:width/height が実 hero WebP 実寸と一致 ({_dims338})",
        (f"Check 338: og:image 寸法 drift: {_problems338!r} — "
         "hero 再エクスポートで実寸が変わったのに meta 未更新。social-card が "
         "誤 aspect ratio (letterbox/crop) or reject。meta を実寸へ同期せよ"),
        blocking=True,
    )
else:
    check(False, "Check 338: hero WebP + index.html present",
          "Check 338: hero WebP または index.html が無い", blocking=True)

# ── 339. JSON-LD hero ImageObject width/height == actual WebP dims (BLOCKING) ─
_webp339 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
_html339 = ROOT / "index.html"
if _webp339.is_file() and _html339.is_file():
    _dims339 = _parse_webp_dims338(_webp339)
    _hero_name339 = "yuta-yokoi-ai-pm-orchestration-system.webp"
    _problems339: list[str] = []
    _checked339 = 0
    if _dims339 is None:
        _problems339.append("hero WebP 寸法を parse できない")
    else:
        _aw339, _ah339 = _dims339
        for _m in re.finditer(
                r'<script type="application/ld\+json">(.*?)</script>',
                _html339.read_text(encoding="utf-8"), re.DOTALL):
            try:
                _ld339 = json.loads(_m.group(1))
            except json.JSONDecodeError:
                continue

            def _walk339(_o):
                global _checked339
                if isinstance(_o, dict):
                    if (_o.get("@type") == "ImageObject"
                            and _hero_name339 in str(_o.get("contentUrl", ""))
                            and ("width" in _o or "height" in _o)):
                        _w = str(_o.get("width", ""))
                        _h = str(_o.get("height", ""))
                        _checked339 += 1
                        if _w and _w != str(_aw339):
                            _problems339.append(
                                f"@id={_o.get('@id','?')} width={_w!r} != 実寸 {_aw339}")
                        if _h and _h != str(_ah339):
                            _problems339.append(
                                f"@id={_o.get('@id','?')} height={_h!r} != 実寸 {_ah339}")
                    for _v in _o.values():
                        _walk339(_v)
                elif isinstance(_o, list):
                    for _v in _o:
                        _walk339(_v)
            _walk339(_ld339)
    check(
        not _problems339,
        f"Check 339: JSON-LD hero ImageObject 寸法 ({_checked339} 件) が実 WebP 実寸 {_dims339} と一致",
        (f"Check 339: JSON-LD ImageObject 寸法 drift: {_problems339!r} — "
         "hero 再エクスポートで実寸が変わったのに JSON-LD が stale。AI crawler / "
         "knowledge graph が誤寸法を ingest。JSON-LD を実寸へ同期せよ (C6 semantic ゆえ "
         "orchestrator 承認経由)"),
        blocking=True,
    )
else:
    check(False, "Check 339: hero WebP + index.html present",
          "Check 339: hero WebP または index.html が無い", blocking=True)

# ── 340. JSON-LD encodingFormat MIME == actual binary format (BLOCKING) ──────
_webp340 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
_mp3_340 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"
_html340 = ROOT / "index.html"
if _html340.is_file():
    # 実バイナリの magic-byte 由来の期待 MIME を確定
    _expected_mime340: dict[str, str] = {}
    if _webp340.is_file():
        _wb = _webp340.read_bytes()[:12]
        if _wb[0:4] == b"RIFF" and _wb[8:12] == b"WEBP":
            _expected_mime340[_webp340.name] = "image/webp"
    if _mp3_340.is_file():
        _mb = _mp3_340.read_bytes()[:3]
        if _mb[0:3] == b"ID3" or (len(_mb) >= 2 and _mb[0] == 0xFF
                                  and (_mb[1] & 0xE0) == 0xE0):
            _expected_mime340[_mp3_340.name] = "audio/mpeg"
    _problems340: list[str] = []
    _checked340 = 0
    for _m in re.finditer(
            r'<script type="application/ld\+json">(.*?)</script>',
            _html340.read_text(encoding="utf-8"), re.DOTALL):
        try:
            _ld340 = json.loads(_m.group(1))
        except json.JSONDecodeError:
            continue

        def _walk340(_o):
            global _checked340
            if isinstance(_o, dict):
                if (_o.get("@type") in ("ImageObject", "AudioObject")
                        and "encodingFormat" in _o):
                    _url = str(_o.get("contentUrl", "") or _o.get("url", ""))
                    for _fname, _mime in _expected_mime340.items():
                        if _fname in _url:
                            _checked340 += 1
                            _declared = str(_o.get("encodingFormat", ""))
                            if _declared != _mime:
                                _problems340.append(
                                    f"@id={_o.get('@id','?')} encodingFormat="
                                    f"{_declared!r} != 実 format {_mime!r} ({_fname})")
                for _v in _o.values():
                    _walk340(_v)
            elif isinstance(_o, list):
                for _v in _o:
                    _walk340(_v)
        _walk340(_ld340)
    _ok340 = (not _problems340) and _checked340 > 0
    check(
        _ok340,
        f"Check 340: JSON-LD encodingFormat MIME ({_checked340} 件) が実 binary format と一致",
        (f"Check 340: encodingFormat MIME drift: {_problems340!r} — "
         "JSON-LD が実バイナリと異なる MIME を宣言。AI crawler が誤 content-type を "
         "ingest / 宣言 MIME を信じる consumer が mis-decode。実 format へ同期せよ "
         "(C6 semantic ゆえ orchestrator 承認経由)"),
        blocking=True,
    )
else:
    check(False, "Check 340: index.html present",
          "Check 340: index.html が無い", blocking=True)

# ── 341-343. og/twitter meta non-empty + robots safety + .well-known JSON validity checks (341-343) → checks_meta_validity.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_meta_validity as _checks_meta_validity
_checks_meta_validity.run(_ctx)


# ── 345-347. CI verification-chain wiring checks — verify layers / consistency guard / behavior e2e gate (345-347) → checks_ci_verify.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_ci_verify as _checks_ci_verify
_checks_ci_verify.run(_ctx)


# ── 348. Both gate workflows trigger on pull_request → main (BLOCKING) ───────
# meta-guard (trigger 層): 346/347 は invocation を守るが、pull_request トリガが
# 消えると workflow が PR で発火せず run: step は存在するのに実行されない。
def _has_pr_main_trigger348(_path):
    if not _path.is_file():
        return None
    _src = _path.read_text(encoding="utf-8")
    # `on:` ブロックを次の top-level key (行頭非空白 + `:`) まで切り出す
    _m = re.search(r"(?ms)^on:\s*\n(.*?)(?=^\S)", _src)
    if not _m:
        # `on:` が inline (on: [push, pull_request]) の可能性
        _inline = re.search(r"(?m)^on:\s*(.+)$", _src)
        _block = _inline.group(1) if _inline else ""
    else:
        _block = _m.group(1)
    _has_pr = "pull_request" in _block
    _has_main = '"main"' in _block or "'main'" in _block or re.search(r"\bmain\b", _block)
    return bool(_has_pr and _has_main)

_wf348 = {
    "architecture-validation.yml": ROOT / ".github" / "workflows" / "architecture-validation.yml",
    "playwright-regression.yml": ROOT / ".github" / "workflows" / "playwright-regression.yml",
}
_bad348: list[str] = []
for _name348, _p348 in _wf348.items():
    _res348 = _has_pr_main_trigger348(_p348)
    if _res348 is None:
        _bad348.append(f"{_name348} が存在しない")
    elif not _res348:
        _bad348.append(f"{_name348} に pull_request→main トリガが無い")
_ok348 = not _bad348
check(
    _ok348,
    "Check 348: 両 gate workflow が pull_request→main トリガを宣言",
    (f"Check 348: gate trigger drift: {_bad348!r} — "
     "pull_request トリガが消えると workflow が PR で発火せず run: step が "
     "存在しても実行されない (PR が un-gated で merge)。on: に "
     "pull_request: branches: [main] を復元せよ"),
    blocking=True,
)

# ── 349. icon.svg is a well-formed SVG (BLOCKING) ────────────────────────────
_icon349 = ROOT / "icon.svg"
if _icon349.is_file():
    _isvg349 = _icon349.read_text(encoding="utf-8", errors="replace")
    _head349 = _isvg349.lstrip("﻿ \t\r\n")
    _problems349: list[str] = []
    if not (_head349.startswith("<?xml") or _head349.startswith("<svg")):
        _problems349.append(f"先頭が <?xml/<svg でない (head={_head349[:30]!r})")
    if "<svg" not in _isvg349:
        _problems349.append("<svg 要素が無い")
    if "</svg>" not in _isvg349:
        _problems349.append("</svg> close tag が無い")
    if 'xmlns="http://www.w3.org/2000/svg"' not in _isvg349:
        _problems349.append("SVG namespace 宣言が無い")
    _ok349 = not _problems349
    check(
        _ok349,
        "Check 349: icon.svg が well-formed SVG (declared image/svg+xml と実体一致)",
        (f"Check 349: icon.svg format 違反: {_problems349!r} — "
         "declared type=\"image/svg+xml\" が実体と食い違い、browser が favicon を "
         "reject (generic globe) / PWA install icon 失敗。正規 SVG へ差し戻せ"),
        blocking=True,
    )
else:
    check(False, "Check 349: icon.svg present",
          "Check 349: icon.svg が無い", blocking=True)

# ── 350. inline onload handler CSP hash present + matches content (BLOCKING) ──
# Check 7b/7c は 2 つの inline <script> block を被覆。本 Check は 3 つ目の CSP
# hash = inline event handler `this.media='all'` を被覆。handler を編集して
# hash を再計算しないと Chrome が block しフォント非同期ロードが silent 破綻。
_idx350 = ROOT / "index.html"
if _idx350.is_file():
    _h350 = _idx350.read_text(encoding="utf-8")
    _h350_nc = re.sub(r"<!--.*?-->", "", _h350, flags=re.DOTALL)
    # font async-load handler の onload 属性値を実体から抽出
    _m350 = re.search(r"onload=\"(this\.media='[^']*')\"", _h350_nc)
    if _m350 is not None:
        _handler_content350 = _m350.group(1)
        _handler_hash350 = _lib_csp_sri_hash(_handler_content350)
        check(
            f"'{_handler_hash350}'" in _h350,
            f"Check 350: CSP が inline handler {_handler_content350!r} を authorize (content hash {_handler_hash350})",
            (f"Check 350: CSP が inline handler {_handler_content350!r} を authorize しない — "
             f"computed {_handler_hash350} が script-src に不在。handler を編集して CSP hash を "
             "再計算し忘れると Chrome が block しフォント非同期ロードが破綻 (FOUC)。"
             f"'{_handler_hash350}' を script-src へ追加せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 350: inline onload handler present",
              "Check 350: index.html に onload=\"this.media='...'\" handler が無い "
              "(font async-load pattern の期待値)", blocking=True)
else:
    check(False, "Check 350: index.html present",
          "Check 350: index.html が無い", blocking=True)

# ── 351-355. shipped-JS security + CSP script authorization checks — sitemap loc / innerHTML fail-closed / DOMParser absence / script-src+connect-src host authz (351-355) → checks_csp_security.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_csp_security as _checks_csp_security
_checks_csp_security.run(_ctx)


# ── 357-359. shipped-asset resolution wiring checks — preload href / sitemap image:loc + og:image / BGM audio (357-359) → checks_asset_resolve.py ──
# (check.py split track. 連続 self-contained クラスタ・自前 read_text・READ-ONLY。元の実行位置を保持。
#  CHECK_SOURCE_FILES 登録で 45/70/105 横断集約。global→nonlocal 変換 0 箇所。)
import checks_asset_resolve as _checks_asset_resolve
_checks_asset_resolve.run(_ctx)


# ── 360. asset:*:canonical meta URLs resolve to real files (BLOCKING) ────────
# Check 234 は canonical prefix を守るが実 file 解決は未検証。rename で
# canonical-prefixed だが 404 な AIO canonical asset を declare しうる gap を封じる。
_idx360 = ROOT / "index.html"
if _idx360.is_file():
    _h360 = re.sub(r"<!--.*?-->", "", _idx360.read_text(encoding="utf-8"), flags=re.DOTALL)
    _asset_canon360 = re.findall(
        r'<meta\s+name="(asset:[^"]*canonical)"\s+content="(https://[^"]+)"', _h360)
    _missing360: list[str] = []
    for _name, _url in _asset_canon360:
        _rel = _url
        for _pfx in ("https://yutapr0117-design.github.io/portfolio/",
                     "/portfolio/", "./", "/"):
            if _rel.startswith(_pfx):
                _rel = _rel[len(_pfx):]
                break
        if not (ROOT / _rel).is_file():
            _missing360.append(f"{_name} → {_url} (file 解決せず)")
    _ok360 = (not _missing360) and len(_asset_canon360) > 0
    check(
        _ok360,
        f"Check 360: asset:*:canonical meta {len(_asset_canon360)} 件すべて実 file に解決",
        (f"Check 360: asset canonical が file 解決しない: {_missing360!r} — "
         "canonical prefix (Check 234) は通るが実 file が無い = AI crawler が fetch すると "
         "dead link で entity の asset authority が壊れる。実 file へ揃えよ"),
        blocking=True,
    )
else:
    check(False, "Check 360: index.html present",
          "Check 360: index.html が無い", blocking=True)

# ── 361-364. maintainability/test-health checks → checks_maintainability.py ──
# (extracted Phase 1 PoC. Registered in CHECK_SOURCE_FILES so self-integrity Checks 45/70/105
#  aggregate its inventory + sections. Runs here — same position/order as before — via ctx.)
import checks_maintainability as _checks_maintainability
_checks_maintainability.run(_ctx)

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
