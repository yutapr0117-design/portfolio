"""
checks_structural_ci.py — kernel/canary structural integrity + CI lint-coupling checks
(extracted from check_repository_consistency.py — check.py split track・category "structural/CI").

Non-contiguous cluster of Checks 43/44/46/53/54/55/58/60: main.js AIDK Isolated Kernel structural
integrity (43), AIO provenance canary token cross-surface (44), package.json lint scripts JS-set
coverage (46), index.html modulepreload href resolution (53), ESLint ↔ @eslint/js major coupling
(54・defines `_major54` reused by 55), CI lint-target authoritative coupling (55), e2e ALL_ROUTES ↔
main.js switch set equality (58). Each Check
reads its own target files directly. NOTE: Check 45 (self-documentation bijection) is the
self-integrity aggregator — it MUST stay in the monolith. Checks 59+72 (file-size-budget / ESLint
absolute-ceiling) are a separate producer/consumer pair (`_bsrc59`/`_budget59`) left in the monolith.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
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
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract
    warnings = ctx.warnings

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
    # ALL_ROUTES は e2e spec のテーマ別分割 (2026-07-07) で security-proxy.spec.js に移動したため、
    # e2e/*.spec.js 全体を連結して照合する。
    _specs58 = sorted((ROOT / "e2e").glob("*.spec.js"))
    _main58 = ROOT / "main.js"
    if _specs58 and _main58.exists():
        _ssrc58 = "\n".join(p.read_text(encoding="utf-8") for p in _specs58)
        _msrc58 = _main58.read_text(encoding="utf-8")
        # ALL_ROUTES = [ { hash: '#/<name>', name: '<name>' }, ... ]
        # 全 spec 連結ソースから ALL_ROUTES ブロックだけを切り出してから name を抽出する
        # (他 spec の getByRole({ name: '...' }) 等を誤って route 名として拾わないため)。
        _allm58 = re.search(r"const ALL_ROUTES\s*=\s*\[(.*?)\];", _ssrc58, re.DOTALL)
        _allblk58 = _allm58.group(1) if _allm58 else ""
        _e2e_routes58 = set(re.findall(r"name:\s*'([a-z][a-z0-9-]*)'", _allblk58))
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
        warnings.append("Check 58: e2e/*.spec.js or main.js not found — route set check skipped")
