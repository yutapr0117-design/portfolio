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
  28. e2e/*.spec.js has no test() nested inside another test() (+ 'No Trusted Types' test present)
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
  424. file-size-budget.md §2 表の「実測行数」列が実測 (`wc -l`) と一致することを機械強制
       する。§2 は人間可読な要約で、機械可読な真値は §4 BUDGET-DATA (Check 52/71 がパース)
       ゆえ、§2 の数値は「一致は人間レビューで保つ」とだけ書かれ **誰も検証していなかった**。
       実測すると 62 行中 44 行が stale (最大 366 行ズレ) で、列見出しが「実測行数」と
       名乗りながら 71% が実測でない状態だった。cold-start の読者はこの表で headroom を
       判断するため、間違った数値は無いより悪い。CLAUDE.md §7 の教訓「『生じないように』は
       doc/convention でなく Check で機械強制せよ」の未適用箇所。(BLOCKING)
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
  365. Capstone: every git-tracked text file (excluding the design-constraint
       A group: style.css / index.html / main.js; AIO/C6 layer:
       llms-full.txt / llms.txt / llms_well-known.txt; npm lockfile:
       package-lock.json; bot-managed append logs: aio-monitoring-log.json /
       aio-monitoring-log-archive.json (weekly bot appends ~95 lines/entry and
       cannot be bounded without rotation — excluded as pure evidence logs);
       pure-data subtrees: js/quiz/*.js / .well-known/**; binary extensions:
       png/jpg/webp/mp3 etc.; e2e snapshot dirs) MUST be ≤1,000 lines.
       This is the top-level bloat gate complementing the per-surface guards
       (Check 363 for js/*.js, Check 52 ADVISORY, JS-LEAF-CEILING BLOCKING).
       check.py split (→920 lines), e2e spec split (→max 647 lines), and
       B-track trim (AI2AI.md→951, ChatGPT2ChatGPT.md→970) had to complete
       before this gate could first pass (achieved 2026-07-08). Implemented
       via `git ls-files` so only committed files are scanned — no untracked
       or gitignored noise. Prevents any future increment from silently
       re-bloating any doc, check module, workflow, or e2e spec beyond the
       threshold. (BLOCKING)
  385. checks_*.py error-path ctx.warnings/ctx.errors unpack: every split check module
       (`.github/scripts/checks_*.py`) that uses a BARE `warnings.append(...)` / `errors.append(...)`
       (an error/skip path, e.g. "target file not found — check skipped") MUST also unpack
       `warnings = ctx.warnings` / `errors = ctx.errors` in its `run(ctx)`. The shared warnings/errors
       lists live on `ctx`; a module that appends to a bare `warnings`/`errors` name WITHOUT unpacking
       raises `NameError` the moment that path executes (a target file is missing, PyYAML is absent,
       etc.), crashing the ENTIRE consistency script with a traceback instead of emitting the intended
       graceful warning. The bug is dormant while all files/deps are present (the error branch never
       runs) so it survives normal verify — a latent crash. Discovered when deleting `.github/
       dependabot.yml` made Check 68 raise NameError instead of skipping (5 modules had the missing
       unpack: aio_config/governance_sync/repo_hygiene/structural_ci lacked warnings, misc_governance
       lacked errors). This Check parses each module for bare append + missing unpack. (BLOCKING)
  398. consistency の ADVISORY warning 本文出力: `check_repository_consistency.py` の Result block
       は `warnings` を反復し各本文を `::warning::{w}` (GitHub Actions annotation) 形式で印字し
       なければならない。従来は errors 側だけが `::error::{e}` で本文を列挙し、warnings 側は
       `passed with N warning(s)` と件数のみを出して本文を捨てていた (「1 ケースだけ処理・他を
       忘れる」asymmetry)。ADVISORY Check は 56 箇所・13 module に及び、drift を検出しても本文が
       出ないためローカル実行でも CI ログでも「どの invariant が緩んでいるか」を読めず、対処の
       起点が存在しない — 読めない advisory は実質 vacuous な助言層で、BLOCKING でない Check 群
       (52 予算 / 60 ESLint baseline / 121 STATUS 鮮度 等) の早期警告価値がゼロになる。検証は
       loop 変数名に束縛して行う (`for w in warnings:` → `print(f"...::warning::{w}")`)。literal
       の有無だけを見るとループと無関係な固定文字列で vacuous に PASS しうるため。Check 385
       (advisory/error パスの latent crash 防止) と対で「助言層が実際に機能する」軸を守る。(BLOCKING)
  408. e2e spec budget registration: every `e2e/*.spec.js` must be registered in
       docs/architecture/file-size-budget.md (§2 table + §4 BUDGET-DATA). Without an entry the only
       thing guarding a spec's size is Check 365's hard 1,000-line BLOCKING ceiling, so a file grows
       silently and then blocks a PR with no prior warning — measured on 2026-08-09, when
       apps-settings.spec.js hit the ceiling in TWO consecutive cycles (1,032 then 1,021 lines) while
       apps-task.spec.js sat 28 lines below it. Registering them makes Check 52 emit an ADVISORY
       first (a two-layer design: advisory warning → blocking ceiling), and Check 398 now prints
       advisory bodies so that warning actually reaches the operator. This is the e2e face of
       Check 361 (js leaf registration). (BLOCKING)
  400. monolith の module-level parse fail-soft: `check_repository_consistency.py` の module 直下
       (indent 0) に try/except 非保護の `json.loads(...)` / `yaml.safe_load(...)` があってはならない。
       対象 file が壊れた瞬間に traceback で **suite 全体** が停止し、その破損を検出するために書かれた
       Check 自身を含む全 Check が未実行のまま skip される。exit 1 ゆえ merge は止まるが、(a) 診断が
       Python の traceback で actionable でなく (b) crash 地点以降の Check が一切走らないため他の
       drift を全て masking する — Check としては死んでいる。実測 (mutation-probe の catch 帰属を
       正した直後に検出): `.well-known/mcp.json` に構文エラーを入れると module-level の
       `mcp_data = json.loads(read(...))` が JSONDecodeError を送出し、まさにこの破損を検出する
       Check 343 が一度も走らなかった。fail-soft な既定値 (空 dict 等) へ degrade させ、専任 Check に
       診断させること。Check 385 (split module の error パス NameError) の global 面。(BLOCKING)
  413. runbook §9 tracked-file baseline freshness (ADVISORY): `total-check-runbook.md` §9 is the face
       CLAUDE.md declares to be the SOURCE OF TRUTH for numbers ("if §7's numbers drift, §9 wins").
       Yet several of its measured baselines have no machine enforcement, and the runbook itself
       admits they "can drift while verify stays green (it actually drifted 243→567 over time)".
       Re-measuring on 2026-08-10 found exactly that: tracked-file total 490→502 and non-docs/files
       source 244→250. A document that CLAIMS to be the truth and silently goes stale is the worst
       case, because readers trust it instead of re-measuring. This Check surfaces the divergence.
       ADVISORY rather than BLOCKING because these values legitimately move whenever a file is added,
       and forcing every PR to touch the runbook would be pure churn (the advisory-warning +
       separate-hard-gate two-layer design of Check 60). Tolerance is an ABSOLUTE 5 files: the first
       attempt used ±3%, which would NOT have caught the very 12-file drift that motivated this Check
       — a gate whose threshold sits above its own motivating failure is worthless, so it was
       measured and tightened. The `OK:` line count in §9 is deliberately OUT of scope: it is not
       knowable from inside the same run (it is only final once the run ends), an honest limit of
       self-measurement rather than an oversight. (ADVISORY)
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

    # ── 28. P0-02: e2e/*.spec.js — no test() nested inside another test() ─
    # spec テーマ別分割 (2026-07-07) 後は e2e/*.spec.js 全体を走査する。'No Trusted Types' テストは
    # security-proxy.spec.js に移動したため presence 判定も全 spec 横断で行う。
    _specs_28 = sorted((ROOT / "e2e").glob("*.spec.js"))
    if _specs_28:
        # Verify the 'No Trusted Types' test exists at all (across all spec files)
        _has_ttt = any(
            "No Trusted Types or CSP violations in console" in _sp28.read_text(encoding="utf-8")
            for _sp28 in _specs_28
        )
        check(
            _has_ttt,
            "e2e/*.spec.js: 'No Trusted Types or CSP violations in console' test exists",
            "e2e/*.spec.js: 'No Trusted Types or CSP violations in console' test is missing",
        )

        # Detect test() nested inside another test() by tracking brace depth (per file).
        # Only top-level test() calls (column 0, matching ^test\() are tracked as test-openers.
        # Parameterised tests inside a for-loop are indented and do NOT match ^test\(,
        # so they are intentionally excluded from this check.
        import re as _re_spec28
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

        for _sp28 in _specs_28:
            _spec_lines_28 = _sp28.read_text(encoding="utf-8").splitlines()
            _brace_depth_28 = 0
            _test_start_depth_28 = None   # None = not currently inside a top-level test()
            for _ln28, _line28 in enumerate(_spec_lines_28, 1):
                _code28 = _strip_js_literals_28(_line28)
                # A top-level test() definition starts at column 0 (元行で判定: 列 0 固定ゆえ strip 不要)
                if _re_spec28.match(r"^test\s*\(", _line28):
                    if _test_start_depth_28 is not None:
                        _nesting_errors_28.append(
                            f"{_sp28.name}:{_ln28}: test() opened while previous test() "
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
            f"e2e/*.spec.js ({len(_specs_28)}): all test() definitions are top-level (no nesting detected)",
            "e2e/*.spec.js: nested test() detected — " + "; ".join(_nesting_errors_28[:3]),
        )
    else:
        warnings.append("P0-02: e2e/*.spec.js not found — test-nesting check skipped")

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

    # ── 424. file-size-budget.md §2 表の実測行数が実測と一致 (BLOCKING) ────────────
    # §2 は人間可読な要約で、機械可読な真値は §4 BUDGET-DATA (Check 52/71 がパース) である。
    # そのため §2 の数値は長らく「一致は人間レビューで保つ」とだけ書かれ、誰も検証して
    # いなかった。実測したところ 62 行中 44 行が stale (最大 366 行ズレ) で、列見出しが
    # 「実測行数」と名乗りながら 71% が実測でない状態だった。表を読んで headroom を判断する
    # cold-start の読者にとって、間違った数値は無いより悪い。人間レビュー任せをやめて機械強制する。
    _budget424 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget424.exists():
        _src424 = _budget424.read_text(encoding="utf-8")
        _stale424 = []
        _checked424 = 0
        for _m424 in re.finditer(r"^\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| `", _src424, re.M):
            _p424 = ROOT / _m424.group(1)
            if not _p424.exists():
                continue  # 存在検証は Check 71 の担当
            _actual424 = len(_p424.read_text(encoding="utf-8", errors="replace").split("\n")) - 1
            _rec424 = int(_m424.group(2).replace(",", ""))
            _checked424 += 1
            if _rec424 != _actual424:
                _stale424.append(f"{_m424.group(1)}: 表={_rec424} 実測={_actual424}")
        check(
            not _stale424 and _checked424 > 0,
            f"Check 424: file-size-budget.md §2 表の実測行数 {_checked424} 件が実測と一致",
            f"Check 424: §2 表の実測行数が実測とズレている: {_stale424[:8]}"
            + (f" (他 {len(_stale424) - 8} 件)" if len(_stale424) > 8 else "")
            + "。行数を変えたファイルは §2 表の「実測行数」列も同じ commit で更新せよ "
            f"(§4 BUDGET-DATA は予算値なので変更不要)",
        )
    else:
        warnings.append("Check 424: file-size-budget.md not found — §2 line-count sync check skipped")

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

    # ── 365. Capstone: 全非 A 追跡テキストファイル ≤1,000 行 (BLOCKING) ─────────────
    # AI 無限改善自走の持続可能性を守る Capstone。「肥大化を生じないように」する最上位 gate。
    # check.py 分割 (920行) + e2e spec 分割 (max 647行) + B-track trim (AI2AI.md 951行・
    # ChatGPT2ChatGPT.md 970行) が完了した 2026-07-08 に初めて全ファイルで通過できるようになった。
    # git ls-files で committed files のみスキャン（untracked / .gitignore 対象は除外）。
    import subprocess as _sp365
    _a_names = frozenset([
        "style.css", "index.html", "main.js",       # design-constraint A group
        "llms-full.txt", "llms.txt", "llms_well-known.txt",  # AIO/C6（orchestrator 承認必須）
        "package-lock.json",                         # npm 自動生成 lockfile（手動編集対象外）
        # bot-managed append logs: weekly aio-monitoring.yml が ~95 行/エントリで追記する
        # 純粋な evidence ログ。人間が手動編集する文書ではなく log-rotation なしの append-only
        # ゆえ「1,000 行ハードゲート」の対象外とする。
        "aio-monitoring-log.json",
        "aio-monitoring-log-archive.json",
    ])
    _bin_exts = frozenset([
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
        ".mp3", ".woff", ".woff2", ".ttf", ".eot", ".gz", ".zip",
    ])
    _excl_pfx = ("js/quiz/", ".well-known/", "e2e/portfolio.spec.js-snapshots/")
    _CEIL365 = 1000
    try:
        _ls365 = _sp365.run(
            ["git", "ls-files"], cwd=str(ROOT), capture_output=True, text=True, check=True
        )
        _tracked365 = [ln.strip() for ln in _ls365.stdout.splitlines() if ln.strip()]
        _over365 = []
        for _rel in _tracked365:
            _p365 = ROOT / _rel
            if not _p365.is_file():
                continue
            if _p365.name in _a_names or _p365.suffix in _bin_exts:
                continue
            if any(_rel.startswith(pfx) for pfx in _excl_pfx):
                continue
            try:
                _n365 = len(_p365.read_text(encoding="utf-8", errors="replace").splitlines())
            except OSError:
                continue
            if _n365 > _CEIL365:
                _over365.append(f"{_rel} ({_n365}行)")
        check(
            not _over365,
            f"Check 365: 全非 A 追跡テキストファイル ≤{_CEIL365} 行 (capstone BLOCKING)",
            f"Check 365: {len(_over365)} ファイルが {_CEIL365} 行超。肥大化解消後に merge せよ: "
            + ", ".join(_over365[:5]),
            blocking=True,
        )
    except Exception as _e365:
        warnings.append(f"Check 365: git ls-files 実行失敗 — capstone skipped ({_e365})")

    # ── 385. checks_*.py error-path ctx.warnings/ctx.errors unpack (BLOCKING) ─────
    # 分割 check module が bare `warnings.append` / `errors.append` を error/skip パスで使うのに
    # `warnings = ctx.warnings` / `errors = ctx.errors` を run(ctx) で unpack していないと、その
    # パス到達時 (target file 不在 / PyYAML 不在 等) に NameError で consistency script 全体が
    # traceback で crash する (全ファイル/依存が揃う通常 verify では error 枝が走らず休眠する latent
    # crash)。dependabot.yml 削除で Check 68 が NameError 化した実バグの systematize (5 module 修正)。
    _scripts_dir385 = ROOT / ".github" / "scripts"
    _bad385 = []
    if _scripts_dir385.exists():
        for _mp385 in sorted(_scripts_dir385.glob("checks_*.py")):
            _msrc385 = _mp385.read_text(encoding="utf-8")
            # bare `warnings.append(` / `errors.append(` を **行頭 (indent のみ)** で検出する。
            # 行頭アンカーにより (a) `ctx.warnings.append(` (行頭が ctx.) と (b) f-string / コメント内の
            # "bare errors.append without ..." のような文字列言及 (行頭が別トークン) を除外する
            # — この Check 自身の説明文中の "errors.append" 言及で self-false-positive しない。
            _bare_w385 = re.search(r"^\s*warnings\.append\(", _msrc385, re.M)
            _bare_e385 = re.search(r"^\s*errors\.append\(", _msrc385, re.M)
            _unpack_w385 = re.search(r"^\s*warnings\s*=\s*ctx\.warnings", _msrc385, re.M)
            _unpack_e385 = re.search(r"^\s*errors\s*=\s*ctx\.errors", _msrc385, re.M)
            if _bare_w385 and not _unpack_w385:
                _bad385.append(f"{_mp385.name}: bare warnings.append without `warnings = ctx.warnings`")
            if _bare_e385 and not _unpack_e385:
                _bad385.append(f"{_mp385.name}: bare errors.append without `errors = ctx.errors`")
    check(
        not _bad385,
        f"Check 385: all checks_*.py modules unpack ctx.warnings/ctx.errors before bare append ({len(_bad385)} offenders)",
        f"Check 385: {_bad385[:6]} — module が bare `warnings.append(...)` / `errors.append(...)` を "
        "error/skip パスで使うのに run(ctx) で `warnings = ctx.warnings` / `errors = ctx.errors` を "
        "unpack していない。その枝が走ると NameError で consistency script 全体が crash する (通常は "
        "全ファイル/依存が揃うため休眠)。`extract = ctx.extract` の直後に不足 unpack を追加せよ",
    )

    # ── 408. e2e spec の予算登録 (BLOCKING) ────────────────────────────────────────
    # e2e/*.spec.js は Check 365 の 1,000 行 BLOCKING 上限だけが効いており、**超過するまで一切の
    # 予告が無かった**。実測 (2026-08-09): apps-settings.spec.js で 2 サイクル連続 BLOCKING を踏み
    # (1,032 行 → 1,021 行)、apps-task.spec.js は上限まで残り 28 行だった。file-size-budget.md の
    # BUDGET-DATA へ登録すれば Check 52 が advisory で先に警告する二層になる (Check 398 で advisory
    # 本文が読めるようになったため警告が実際に届く)。新しい spec が登録漏れで早期警告網の外へ
    # 出るのを防ぐ (Check 361 = js leaf 面の e2e 版)。
    _budget408 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    _e2e_dir408 = ROOT / "e2e"
    if _budget408.exists() and _e2e_dir408.is_dir():
        _bsrc408 = _budget408.read_text(encoding="utf-8")
        _specs408 = sorted(f"e2e/{p408.name}" for p408 in _e2e_dir408.glob("*.spec.js"))
        _missing408 = [p408 for p408 in _specs408
                       if not re.search(r"^" + re.escape(p408) + r"\s*\|", _bsrc408, re.M)]
        check(
            bool(_specs408) and not _missing408,
            f"Check 408: 全 {len(_specs408)} 個の e2e spec が file-size-budget.md の BUDGET-DATA に登録済 (早期警告網)",
            f"Check 408: BUDGET-DATA 未登録の e2e spec: {_missing408} — 未登録だと Check 52 の advisory が効かず "
            "Check 365 の 1,000 行 BLOCKING に予告なく当たる (実測: apps-settings.spec.js で 2 サイクル連続発生)。"
            "docs/architecture/file-size-budget.md の §2 表と §4 BUDGET-DATA へ追加せよ",
            blocking=True,
        )
    else:
        check(False, "Check 408: file-size-budget.md and e2e/ present",
              "Check 408: file-size-budget.md または e2e/ が無い — e2e spec の予算登録を検証できない", blocking=True)

    # ── 398. consistency の ADVISORY warning 本文出力 (BLOCKING) ───────────────────
    # check_repository_consistency.py の Result block は errors 側を `::error::{e}` で本文列挙する
    # のに、warnings 側は件数だけを印字し本文を捨てていた (asymmetry)。ADVISORY Check (56 箇所・
    # 13 module) が drift を検出しても "passed with N warning(s)" としか出ず、ローカルでも CI ログ
    # でも「どの invariant が緩んでいるか」が読めない = 読めない advisory は実質 vacuous な助言層。
    # warning 本文を `::warning::` (GitHub Actions annotation) で列挙することを構造強制する。
    _cons398 = ROOT / ".github" / "scripts" / "check_repository_consistency.py"
    _src398 = _cons398.read_text(encoding="utf-8") if _cons398.exists() else ""
    _loop398 = re.search(r"^\s*for\s+(\w+)\s+in\s+warnings\s*:\s*$", _src398, re.M)
    _emit398 = False
    if _loop398:
        # loop 変数名に束縛して検証する (`for w in warnings:` → `print(f"...::warning::{w}")`)。
        # literal 有無だけを見ると、ループと無関係な固定文字列で vacuous に PASS しうる。
        _var398 = _loop398.group(1)
        _tail398 = _src398[_loop398.end():]
        _emit398 = bool(re.search(
            r'^\s*print\(f?"[^"]*::warning::\{' + re.escape(_var398) + r'\}', _tail398, re.M))
    check(
        bool(_src398) and bool(_loop398) and _emit398,
        "Check 398: consistency の ADVISORY warning 本文が ::warning:: annotation で列挙出力される",
        "Check 398: check_repository_consistency.py の Result block が warnings を反復して本文を "
        "`::warning::{w}` 形式で印字していない。件数のみの出力では ADVISORY Check が drift を検出しても "
        "どの invariant が緩んだか読めず (ローカル/CI ログ双方)、advisory 層が実質 vacuous になる。"
        "errors 側の `::error::{e}` 列挙と対称に `for w in warnings: print(f\"  ::warning::{w}\")` を保て",
    )

    # ── 400. monolith の module-level parse は fail-soft (BLOCKING) ────────────────
    # check_repository_consistency.py の module 直下 (indent 0) で生 `json.loads(...)` を実行すると、
    # 対象 file が壊れた瞬間に traceback で suite 全体が停止し、その失敗を検出するために書かれた
    # Check 自身を含む全 Check が未実行のまま skip される (exit 1 で merge は止まるが診断は actionable
    # でなく、crash 地点以降の drift を全て masking する)。実測: .well-known/mcp.json に構文エラーを
    # 入れる mutation で Check 343 は一度も走らず traceback で停止していた。try/except で fail-soft へ
    # degrade させ、専任 Check に actionable な診断を出させること。Check 385 (split module の error
    # パス NameError) の global 面。
    _mono400 = ROOT / ".github" / "scripts" / "check_repository_consistency.py"
    _src400 = _mono400.read_text(encoding="utf-8") if _mono400.exists() else ""
    # indent 0 の代入行のみを検出する (try 本体は 4-space indent ゆえ除外される)。
    _bare400 = re.findall(r"^\w+\s*=\s*(?:json\.loads|yaml\.safe_load)\(", _src400, re.M)
    check(
        bool(_src400) and not _bare400,
        f"Check 400: monolith の module-level parse が fail-soft ({len(_bare400)} unguarded)",
        f"Check 400: check_repository_consistency.py の module 直下に try/except 非保護の "
        f"`json.loads(...)` / `yaml.safe_load(...)` が {len(_bare400)} 件ある。対象 file が壊れた瞬間に "
        "traceback で suite 全体が停止し、その破損を検出するはずの Check 自身を含む全 Check が未実行の "
        "まま skip される (診断は actionable でなく、以降の drift を全て masking する)。try/except で "
        "fail-soft な既定値へ degrade させ、専任 Check に診断させよ",
    )

    # ── 413. runbook §9 の tracked-file baseline 鮮度 (ADVISORY) ───────────────────
    # `docs/architecture/total-check-runbook.md` §9 は CLAUDE.md が「数値の真値」と宣言する面で、
    # §7 の数値が drift したときも §9 を正とする、と canon に書かれている。だが §9 の実測値には
    # 機械強制が無いものがあり、runbook 自身が「verify 緑のまま drift しうる volatile baseline
    # (実際 243→567 まで長期 drift していた)」と認めている。実際 2026-08-10 の再測定で
    # 追跡ファイル総数 490→502 / 非 docs/files source 244→250 の drift を検出した。
    # **真値を名乗る doc が黙って古くなる**のが最も害が大きい (読み手は再測定せず信じる) ため、
    # 乖離を ADVISORY で可視化する。BLOCKING にしないのは、この値は file を 1 つ足すたびに動く
    # 正当な volatile 値であり、全 PR に runbook 更新を強制すると churn になるから (Check 60 と
    # 同じ「advisory 早期警告 + 別レイヤーの hard gate」二層設計の advisory 側)。
    # 許容は **絶対 5 件**。当初 ±3% にしたが、それでは今回検出した 12 件の drift (490→502) を
    # 見逃す設定であり、**動機となった drift を捕捉できない Check は無意味** (自作 gate の
    # 非 vacuity を実測して発見)。5 件なら 1 セッション内の数件追加は黙認しつつ、放置された
    # 乖離は必ず警告になる。
    import subprocess as _sp413
    _runbook413 = ROOT / "docs" / "architecture" / "total-check-runbook.md"
    if _runbook413.exists():
        _rb413 = _runbook413.read_text(encoding="utf-8")
        _m_total413 = re.search(r"\|\s*追跡ファイル総数\s*\|\s*\*\*(\d+)\*\*", _rb413)
        _m_src413 = re.search(r"source file が \*\*(\d+)\*\*", _rb413)
        try:
            _files413 = [ln for ln in _sp413.run(
                ["git", "ls-files"], cwd=str(ROOT), capture_output=True, text=True, check=True
            ).stdout.splitlines() if ln.strip()]
        except Exception:  # noqa: BLE001 — git 不在環境では検証をスキップ (ADVISORY ゆえ fail-soft)
            _files413 = []
        if _files413 and _m_total413 and _m_src413:
            _actual_total413 = len(_files413)
            _actual_src413 = len([f for f in _files413 if not f.startswith("docs/files/")])
            _rec_total413 = int(_m_total413.group(1))
            _rec_src413 = int(_m_src413.group(1))
            _drift413 = []
            for _label413, _rec413, _act413 in (
                ("追跡ファイル総数", _rec_total413, _actual_total413),
                ("非 docs/files source", _rec_src413, _actual_src413),
            ):
                if abs(_act413 - _rec413) > 5:
                    _drift413.append(f"{_label413}: 記載 {_rec413} vs 実測 {_act413}")
            check(
                not _drift413,
                f"Check 413 (ADVISORY): runbook §9 の tracked-file baseline が実測と整合 "
                f"(総数 {_actual_total413} / 非 docs/files source {_actual_src413})",
                f"Check 413 (ADVISORY): runbook §9 の baseline が実測から乖離 — {' / '.join(_drift413)}。"
                "§9 は CLAUDE.md が「数値の真値」と宣言する面であり、古い値は読み手を誤らせる。"
                "再測定して §9 を同期せよ (権威 = `git ls-files | wc -l`)",
                blocking=False,
            )
        else:
            check(True, "Check 413 (ADVISORY): tracked-file baseline の検証をスキップ (git 不在または §9 の記載形式変更)",
                  "", blocking=False)

        # 413b — §9 の内訳が**それ自身の足し算**として整合していること (BLOCKING)。
        # 413 は 6 個ある数値のうち 2 個 (総数・source) しか git と突き合わせないため、行が
        # **内部で矛盾していても緑**になる。実際 2026-08-22 時点で本行は「総数 530 / source 264 /
        # mirror 250 / = 490」と **3 通りの総数を同時に主張**していた (264+250+2 は 516 で、
        # 490 でも 530 でもない)。真値を名乗る面が自分自身と食い違っているのは、古いより悪い
        # (読み手はどれを信じればよいか判断できない)。
        # これは絶対値に依存しない**純粋な算術不変条件**なので、volatile な baseline であっても
        # BLOCKING にできる — file を足せば全部の数が一緒に動くだけで、和の性質は常に成り立つ。
        # 逆に「1 つだけ更新して他を忘れる」という現実の drift 経路をちょうど捕まえる。
        # (Check 60 と同じ「ADVISORY 早期警告 + BLOCKING hard gate」二層設計の hard gate 側。)
        _m_mirror413 = re.search(r"mirror が \*\*(\d+)\*\*", _rb413)
        _m_sum413 = re.search(r"_template\.md` の \*\*(\d+)\*\* = \*\*(\d+)\*\*", _rb413)
        if _m_total413 and _m_src413 and _m_mirror413 and _m_sum413:
            _t413 = int(_m_total413.group(1))
            _parts413 = (int(_m_src413.group(1)), int(_m_mirror413.group(1)), int(_m_sum413.group(1)))
            _stated413 = int(_m_sum413.group(2))
            check(
                sum(_parts413) == _t413 == _stated413,
                f"Check 413b: runbook §9 の内訳が算術的に整合 "
                f"({' + '.join(str(_p) for _p in _parts413)} = {_t413})",
                f"Check 413b: runbook §9 の内訳が自分自身と矛盾している — "
                f"内訳 {' + '.join(str(_p) for _p in _parts413)} = {sum(_parts413)} / "
                f"行頭の総数 = {_t413} / 行末が主張する合計 = {_stated413}。"
                "§9 は CLAUDE.md が「数値の真値」と宣言する面であり、"
                "**複数の総数を同時に主張する行は古い値より有害** (読み手がどれを信じるか決められない)。"
                "1 つの数値を更新したら同じ行の残りも同一 commit で揃えよ",
                blocking=True,
            )
        else:
            check(False, "",
                  "Check 413b: runbook §9 の内訳を parse できない — "
                  "「source file が **N**」「mirror が **N**」「`_template.md` の **N** = **N**」の"
                  "記載形式を保つこと (形式を変えるならこの Check の正規表現も同一 commit で更新せよ)",
                  blocking=True)
