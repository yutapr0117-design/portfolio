"""
checks_maintainability.py — maintainability / test-health governance checks
(extracted from check_repository_consistency.py — Phase 1 PoC of the check.py split).

Self-integrity: this module's checks are aggregated by _aggregate_check_numbers() in the
monolith via CHECK_SOURCE_FILES, so Checks 45/70/105 (docstring inventory ↔ `# ── N.`
section ↔ check-map ↔ runbook §9 bijection) span this file too. `run(ctx)` receives a
context object exposing the shared check() / ROOT / errors / warnings, so the extracted
checks stay behavior-identical (same errors/warnings list objects, no exec, no module-global
coupling — the #253 "net-negative" concern is avoided by explicit ctx injection, not exec()).

Check inventory (kept in sync with the `# \u2500\u2500 N.` sections in run() below; Check 45 enforces):
  16. e2e/portfolio.spec.js screenshot test has a baseline-skip guard
  42. docs/ artifact placement & naming hygiene: (42a) every file directly under
      docs/incident-artifacts/ matches an allowed naming pattern (decision-*.md /
      improvement-notes-*.md / *.yml / README.md); (42b) no decision-*.md or
      improvement-notes-*.md file lives outside docs/incident-artifacts/. Turns the
      placement convention documented in docs/README.md into an enforced invariant
      (artifact-placement governance increment). (BLOCKING)
  28. e2e/portfolio.spec.js has no test() nested inside another test()
  29. Playwright baseline-generation linkage intact (snapshot workflow <-> spec env signal)
  30. v80+ maintainability anchor docs present (repository-maintainability-map / main-js-extraction-map)
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
  71. file-size-budget.md BUDGET-DATA path existence: docs/architecture/file-size-budget.md
      §4 BUDGET-DATA に列挙された各エントリのパスが実在ファイルを指すことを機械強制する。
      BUDGET-DATA は Check 52 (ADVISORY 行数予算) の真値だが、ファイル rename / 削除後に
      BUDGET-DATA から行を消し忘れると Check 52 が「存在しないファイル」を黙ってスキップし、
      削除後の monitoring drift が見えなくなる。本 Check は「BUDGET-DATA に登録された path は
      全て実在する」を BLOCKING で保証する。(BLOCKING)
  361. Every shipped JS leaf module (`js/*.js` ∪ `js/quiz/*.js`) MUST be
       registered in docs/architecture/file-size-budget.md §4 BUDGET-DATA
       with a line budget. Check 71 guarantees registered⟹exists; this is
       the symmetric exists⟹registered, so together they bijection the
       js-leaf surface against BUDGET-DATA. Without it a new leaf module
       (e.g. a js/<x>-page.js born from a bloat-reduction extraction) stays
       silently unbudgeted, escaping the Check 52 advisory and able to grow
       unbounded — the exact gap file-size-budget.md §5 flagged as a
       deferred extension. Machine-enforces the owner-accepted 1,000-line
       threshold discipline (keep bloat from recurring). (BLOCKING)
  362. Every mutation in mutation_samples.py (MUTATIONS ∪ E2E_MUTATIONS)
       MUST have its `find` anchor resolve in its target `file`. The
       mutation-probe / -e2e runners are NOT invoked by any CI workflow
       (completeness verification is manual), so a leaf extraction or
       refactor that moves/removes the anchored code leaves the anchor
       silently orphaned until someone runs the probe by hand — quietly
       hollowing out the completeness-critic's net. Real example: #558
       moved PomodoroPage js/apps.js → js/pomodoro-page.js and orphaned
       the pomodoro E2E mutation anchor. This lifts anchor integrity into
       the BLOCKING verify gate so refactors must keep mutation_samples.py
       in sync. (BLOCKING)
  363. No shipped JS *logic* leaf module (`js/*.js`, non-recursive) may
       exceed the hard line ceiling declared by the JS-LEAF-CEILING marker
       in docs/architecture/file-size-budget.md (currently 1,000). This is
       the BLOCKING enforcement of the owner-accepted 1,000-line bloat
       threshold: whereas Check 52 (BUDGET-DATA) is an ADVISORY per-file
       loose budget that only warns, this is a hard gate that fails the
       build so an over-threshold logic leaf must be split before merge —
       the same two-layer design as Check 60 (advisory early-warning layer
       + BLOCKING hard-gate layer). Scope excludes js/quiz/*.js (pure quiz
       data, where content growth is valuable, observed only by advisory)
       and main.js (protected kernel, not under js/, guarded by Check 43 /
       strong-advisory). Machine-enforces "keep bloat from arising" for the
       behavior-code surface, protecting the AI self-improvement loop that
       unbounded logic-leaf growth would threaten. (BLOCKING)
  364. store.js's ingestion normalizers (validateAndNormalize /
       normalizeAppsData / normalizeProject) MUST NOT use the
       `(X || []).<throwing-array-method>` idiom. They are total functions
       over untrusted external data (import / cross-tab / snapshot / load)
       and must never throw on a non-array input. `(X || [])` fails to
       replace a non-array *truthy* value (a string / number / object), so
       the following .filter/.map/.forEach/.some/.reduce throws a TypeError
       and every ingestion path FatalPage-crashes — #568 (ai/pomodoro
       history), #572 (project tech/tags/links), #573 (task.tags) were the
       real bugs of this class. The safe form is `(Array.isArray(X) ? X :
       [])`. This lifts the per-instance fixes into a structural guard so
       the class cannot be silently reintroduced. (BLOCKING)
"""
import re


def run(ctx):
    """Execute this module's checks against the shared context.

    ctx exposes: ROOT (Path), check (callable), warnings (list), errors (list),
    read/read_bytes/extract (helpers). Extracted checks use the same objects the
    monolith uses, so appends land in the same errors/warnings lists.
    """
    ROOT = ctx.ROOT
    check = ctx.check
    warnings = ctx.warnings

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

    # ── 361. shipped JS leaf-module BUDGET-DATA registration coverage (BLOCKING) ──
    # 全 shipped JS leaf module (js/*.js ∪ js/quiz/*.js) が file-size-budget.md §4
    # BUDGET-DATA に行数予算として登録されていることを機械強制する。Check 71 が
    # 「BUDGET-DATA に登録された path は実在する」(registered ⟹ exists) を保証するのに対し、
    # 本 Check はその対称「shipped JS が存在する ⟹ 登録済み」(exists ⟹ registered) を担い、
    # 両者で js leaf module 面の bijection を成す。これが無いと新規 leaf module (bloat-reduction
    # の抽出で生まれる js/<x>-page.js など) が BUDGET-DATA に登録されないまま silent に
    # 「行数予算なし」になり、Check 52 advisory の網から外れて無制限に成長し得る
    # (file-size-budget.md §5 が deferred 拡張候補として認識していた gap)。owner 受諾の
    # 1,000 行しきい値 (bloat を「生じないように」する規律) を機械強制へ昇華する Check。
    _budget361 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget361.exists():
        _bsrc361 = _budget361.read_text(encoding="utf-8")
        _bblock361 = re.search(r"<!--\s*BUDGET-DATA(.*?)-->", _bsrc361, re.DOTALL)
        _registered361: set[str] = set()
        if _bblock361:
            for _line361 in _bblock361.group(1).strip().split("\n"):
                _line361 = _line361.strip()
                if not _line361 or _line361.startswith("#"):
                    continue
                _parts361 = [p.strip() for p in _line361.split("|")]
                if len(_parts361) >= 3:
                    _registered361.add(_parts361[0])
        _shipped361 = sorted(
            p.relative_to(ROOT).as_posix()
            for p in list((ROOT / "js").glob("*.js")) + list((ROOT / "js" / "quiz").glob("*.js"))
        )
        _unregistered361 = [p for p in _shipped361 if p not in _registered361]
        check(
            not _unregistered361 and len(_shipped361) > 0,
            f"Check 361: all {len(_shipped361)} shipped JS leaf modules (js/*.js ∪ js/quiz/*.js) "
            "are registered in file-size-budget.md §4 BUDGET-DATA",
            f"Check 361: shipped JS leaf module(s) missing from §4 BUDGET-DATA: {_unregistered361}. "
            "新 leaf モジュールは file-size-budget.md §2 表 + §4 BUDGET-DATA に行数予算を登録せよ "
            "(Check 52 silent-unbudgeted 防止 / bloat を「生じないように」する 1,000 行しきい値の機械強制)",
        )
    else:
        warnings.append("Check 361: file-size-budget.md not found — JS budget coverage skipped")

    # ── 362. mutation_samples find-anchor resolution (BLOCKING) ───────────────────
    # mutation_samples.py の全 mutation (MUTATIONS ∪ E2E_MUTATIONS) の `find` anchor が対象 file に
    # 実在することを機械強制する。mutation-probe / mutation-probe-e2e は CI workflow から呼ばれない
    # (完全性検証は手動実行) ため、leaf 抽出やリファクタで anchor の対象コードが別 file へ移動/消滅
    # しても、手動で probe を回すまで anchor は silent に orphan 化し、completeness-critic (安全網の
    # 安全網) の網が知らぬ間に穴だらけになる。実例: #558 で PomodoroPage を js/apps.js →
    # js/pomodoro-page.js へ分離した際、pomodoro E2E mutation の anchor が apps.js から消え orphan 化
    # した (mutation-probe --e2e を手動実行して初めて発覚)。本 Check は anchor 整合性を verify 時の
    # BLOCKING gate へ引き上げ、抽出/リファクタ時に mutation_samples.py の追従を強制する。
    try:
        import importlib as _importlib362
        _ms362 = _importlib362.import_module("mutation_samples")
        _orphans362: list[str] = []
        for _lst362, _lbl362 in ((_ms362.MUTATIONS, "MUTATIONS"), (_ms362.E2E_MUTATIONS, "E2E_MUTATIONS")):
            for _m362 in _lst362:
                _f362 = _m362["file"]
                try:
                    _txt362 = _f362.read_text(encoding="utf-8")
                except OSError:
                    _orphans362.append(f"[{_lbl362}] {_m362['name'][:55]} → file 不在: {_f362}")
                    continue
                if _m362["find"] not in _txt362:
                    _orphans362.append(f"[{_lbl362}] {_m362['name'][:55]} → find-anchor 不在 in {_f362.name}")
        check(
            not _orphans362,
            f"Check 362: all {len(_ms362.MUTATIONS) + len(_ms362.E2E_MUTATIONS)} mutation find-anchors "
            "(MUTATIONS ∪ E2E_MUTATIONS) resolve in their target files",
            f"Check 362: orphaned mutation find-anchor(s): {_orphans362[:5]}. "
            "リファクタ/抽出で anchor の対象コードが別 file へ移動/消滅した — mutation_samples.py の該当 "
            "file/find を現行コードへ追従させよ (mutation-probe は CI 非実行ゆえ本 Check が anchor 整合を守る)",
        )
    except ImportError as _e362:
        warnings.append(f"Check 362: mutation_samples import failed ({_e362}) — anchor resolution skipped")

    # ── 363. shipped JS logic-leaf hard line ceiling (BLOCKING) ───────────────────
    # shipped JS *ロジック* leaf module (js/*.js・非再帰) の行数が JS-LEAF-CEILING marker
    # (file-size-budget.md) の宣言するハード上限 (現行 1,000) を越えないことを機械強制する。
    # Check 52 (BUDGET-DATA) が per-file の loose な ADVISORY 予算で「緩やかに観測」(超過は warning のみ)
    # するのに対し、本 Check は owner 受諾の 1,000 行しきい値を BLOCKING gate として強制し、越えた
    # ロジック leaf は merge 前に分割させる (Check 60 と同型の advisory 早期警告層 + BLOCKING ハード
    # ゲート層の二層設計)。スコープは js/*.js 直下のロジック leaf のみ: js/quiz/*.js (純データ・設問追加は
    # 価値ある成長ゆえ advisory 観測に委ねる) と main.js (保護 kernel・js/ 直下でない・Check 43 で別途保護)
    # は除外する。肥大化放置が脅かす「AI 無限改善自走」を behavior-code 面で守る「生じないように」の機械化。
    _budget363 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget363.exists():
        _bsrc363 = _budget363.read_text(encoding="utf-8")
        _m363 = re.search(r"<!--\s*JS-LEAF-CEILING\s+(\d+)\s*-->", _bsrc363)
        if _m363:
            _ceiling363 = int(_m363.group(1))
            _over363: list[str] = []
            for _p363 in sorted((ROOT / "js").glob("*.js")):
                _n363 = len(_p363.read_text(encoding="utf-8").splitlines())
                if _n363 > _ceiling363:
                    _over363.append(f"{_p363.relative_to(ROOT).as_posix()} ({_n363} > {_ceiling363})")
            check(
                not _over363,
                f"Check 363: all shipped JS logic leaves (js/*.js) are within the "
                f"{_ceiling363}-line hard ceiling (JS-LEAF-CEILING)",
                f"Check 363: js/*.js logic leaf(s) exceed the {_ceiling363}-line hard ceiling: {_over363}. "
                "owner 受諾の 1,000 行しきい値超過 — factory pattern で葉モジュールへ分割してから merge せよ "
                "(肥大化を『生じないように』する BLOCKING 防止層。恒久的に越えるべき正当理由があれば "
                "file-size-budget.md の JS-LEAF-CEILING marker を rationale 付きで owner 裁可のもと引き上げる)",
            )
        else:
            warnings.append("Check 363: JS-LEAF-CEILING marker not found in file-size-budget.md — ceiling check skipped")
    else:
        warnings.append("Check 363: file-size-budget.md not found — JS leaf ceiling skipped")

    # ── 364. store.js ingestion normalizer array-op safety (BLOCKING) ─────────────
    # store.js の正規化子 (validateAndNormalize / normalizeAppsData / normalizeProject) は import /
    # cross-tab / snapshot / load から来る untrusted な外部データを正規化する総関数で、非配列を渡されても
    # throw してはならない。`(X || []).<array-method>` idiom は X が非配列の *truthy* 値 (文字列/数値/
    # オブジェクト) だと `|| []` が置換せず、後続の throwing array-method (filter/map/forEach/some/reduce...) が
    # `TypeError: ... is not a function` を投げ、全 ingestion 経路が FatalPage crash する。#568 (ai/pomodoro
    # history) / #572 (project tech/tags/links) / #573 (task.tags) が同一 class の実バグ。安全形は
    # `(Array.isArray(X) ? X : [])`。本 Check は per-instance の fix を「idiom 再混入の構造防止」へ昇華する
    # (肥大化 Check 363 と同じ「解消したら再発も防ぐ」規律の ingestion-safety 版)。
    _store364 = ROOT / "js" / "store.js"
    if _store364.exists():
        _ssrc364 = _store364.read_text(encoding="utf-8")
        # `<property-access> || []) . <throwing array-method>` を検出 (slice は文字列でも throw しないため除外)。
        # 直前を `\w` (識別子/プロパティアクセス末尾) に限定することで、`str.match(...) || []` のような
        # method-call 結果 (`)` で終わる・match は Array|null 契約ゆえ安全) を false-positive にしない。
        # 危険なのは `raw.tech || []` 等の untrusted プロパティアクセスが非配列 truthy を返す場合のみ。
        _unsafe364 = re.findall(
            r"\w\s*\|\|\s*\[\]\s*\)\s*\.\s*(filter|map|forEach|some|every|reduce|flatMap|find|findIndex)\b",
            _ssrc364,
        )
        check(
            not _unsafe364,
            "Check 364: store.js の正規化子に unsafe `(X || []).<throwing array-method>` idiom が無い "
            "(ingestion-crash class の構造防止)",
            f"Check 364: store.js に unsafe idiom `(X || []).<throwing array-method>` が {len(_unsafe364)} 件 "
            f"({sorted(set(_unsafe364))})。非配列 truthy 入力で TypeError を投げ ingestion 全経路が FatalPage "
            "crash する (#568/#572/#573 class)。`(Array.isArray(X) ? X : [])` へ書き換えよ",
        )
    else:
        warnings.append("Check 364: js/store.js not found — ingestion normalizer safety skipped")
