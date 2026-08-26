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
  456. **`if __name__ == "__main__":` より後で def/class を定義しない** (BLOCKING):
       ガード本体は `sys.exit(main())` の形で **その場で実行される**ので、後ろに置いた
       関数はスクリプト実行時にはまだ束縛されていない。import すると定義されるため、
       **import 経由のテストでは動くのに CLI では NameError** という最悪の非対称になる。
       実測 (2026-08-26): `rotate_mutation_samples.py` の `_wire_new_archive` がこの位置に
       あり、「受け皿が埋まったら次を起こす」という docstring が宣伝している機能が
       **`npm run rotate-mutations` からは一度も動いたことがなかった** (サンドボックスで
       CLI 実行し `NameError: name '_wire_new_archive' is not defined` を実測)。
       しかも失敗するのは受け皿が満杯になった瞬間 —— **最も助けが要るときにだけ**壊れる。
       導入時の走査で誤検出 0 件 (13 file がガードを持ち、違反 0)。(BLOCKING)
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

    # ── 456. __main__ ガードより後に def/class を置かない (BLOCKING) ──────────────────
    # ガード本体 (`sys.exit(main())`) はその場で実行されるので、後ろの def はまだ束縛されて
    # いない。**import 経由では動くのに CLI では NameError** という非対称を生む。
    # 実測 (2026-08-26): rotate_mutation_samples.py の _wire_new_archive がこの位置にあり、
    # docstring が宣伝する「受け皿が埋まったら次を起こす」機能が CLI からは一度も動いて
    # いなかった (サンドボックス実行で NameError を実測)。受け皿が満杯になった瞬間 =
    # **最も助けが要るときにだけ**壊れる形だった。
    import subprocess as _sp456
    try:
        _ls456 = _sp456.run(["git", "ls-files", ".github/scripts"], cwd=str(ROOT),
                            capture_output=True, text=True, check=True)
        _bad456 = []
        for _rel456 in (ln.strip() for ln in _ls456.stdout.splitlines() if ln.strip().endswith(".py")):
            _p456 = ROOT / _rel456
            if not _p456.is_file():
                continue
            _src456 = _p456.read_text(encoding="utf-8", errors="replace")
            _m456 = re.search(r'^if __name__ == ["\']__main__["\']:', _src456, re.M)
            if not _m456:
                continue
            _defs456 = re.findall(r"^(?:def|class)\s+(\w+)", _src456[_m456.end():], re.M)
            if _defs456:
                _bad456.append(f"{_rel456}: {', '.join(_defs456[:3])}")
        check(
            not _bad456,
            "Check 456: __main__ ガードより後に def/class を置いていない (CLI 実行時の NameError 防止)",
            (f"Check 456: {len(_bad456)} file が `if __name__ == \"__main__\":` より後で def/class を"
             f" 定義している: {_bad456[:3]}。ガード本体はその場で実行されるため、後ろの定義は"
             " **スクリプト実行時にはまだ束縛されていない**。import すると定義されるので"
             " **import 経由のテストでは動くのに CLI では NameError** になる。ガードより前へ移せ"),
            blocking=True,
        )
    except (OSError, _sp456.CalledProcessError) as _e456:
        warnings.append(f"Check 456: 走査に失敗 ({_e456}) — __main__ ガード位置の検査を skip")
