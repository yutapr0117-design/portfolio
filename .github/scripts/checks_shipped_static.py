"""
checks_shipped_static.py — shipped-JS static-analysis lint + asset byte-budget checks
(extracted from check_repository_consistency.py — check.py split track・category "shipped static analysis").

Non-contiguous cluster of Checks 237/239/240/241/262/263/264/265/269/270/271/272/310 that statically
scan the shipped JS/assets. They form ONE tightly-coupled unit sharing three cluster-internal values,
all moved together: `import glob as _glob237` (declared in 237, used by 239/271/272), `_eval_targets239`
(the shipped-JS file+content list, built in 239, reused by 240/241/262-265), and `_HERO_WEBP269`/
`_BGM_MP3_269` (binary asset paths defined in 269, consumed by the total-weight Check 310). Check 310
is intentionally pulled in here (though numerically distant) because it consumes 269's paths — a
reverse coupling that a naive 237-272 slice would break (verified: two partial-slice attempts crashed
via the safety net's NameError before this full-set extraction). 238 (HTML head singletons) and 266-268
(JSON-LD length) are interleaved but use none of these, so they stay in the monolith. Executed at Check
237's position in list order so glob / _eval_targets239 / hero+bgm paths bind before their consumers.
No global content dependency.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), byte-equivalent.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
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

  310. Total shipped byte weight <= 2_000_000 bytes: sum of index.html +
       style.css + all root JS (main/sw/4 root scripts) + all leaf JS
       (js/**/*.js) + hero.webp + BGM.mp3 MUST be within the shipping
       total budget. Drift = per-file budget checks (269/270/271/272)
       stay green but the total silently balloons past the 2 MB mobile
       cell-network target. Sibling of Check 269/270/271/272 for the
       total shipped weight axis. (BLOCKING)

"""
import re
import json
from pathlib import Path


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

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

    # ── 310. Total shipped byte weight <= 2_000_000 bytes (BLOCKING) ──────────────
    # 全 shipped asset (index.html + style.css + all root JS + all leaf JS + hero.webp
    # + BGM.mp3) の合計 byte size が 2_000_000 以下であることを BLOCKING 強制。
    # Check 269/270/271/272 (per-file budget) の total 軸版。
    _TOTAL_BUDGET310 = 2_000_000
    _shipped_files310 = [
        ROOT / "index.html", ROOT / "style.css",
        ROOT / "main.js", ROOT / "sw.js",
        ROOT / "aio-guard.js", ROOT / "theme-init.js",
        ROOT / "karte-init.js", ROOT / "error-suppressor.js",
        _HERO_WEBP269, _BGM_MP3_269,
    ]
    _shipped_files310 += [Path(_p) for _p in _glob237.glob(str(ROOT / "js" / "*.js"))]
    _shipped_files310 += [Path(_p) for _p in _glob237.glob(str(ROOT / "js" / "quiz" / "*.js"))]
    _total_size310 = 0
    _missing310: list[str] = []
    for _p in _shipped_files310:
        if not _p.exists():
            _missing310.append(str(_p.relative_to(ROOT)))
            continue
        _total_size310 += _p.stat().st_size
    _ok310 = not _missing310 and _total_size310 <= _TOTAL_BUDGET310
    check(
        _ok310,
        f"Check 310: total shipped weight = {_total_size310} bytes (budget {_TOTAL_BUDGET310})",
        (f"Check 310: 違反: total={_total_size310} > budget {_TOTAL_BUDGET310} bytes / "
         f"missing files={_missing310!r} — mobile cell-network 圧迫。dead-code 削除 or "
         "budget contract 更新"),
        blocking=True,
    )
