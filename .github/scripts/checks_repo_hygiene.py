"""
checks_repo_hygiene.py — repository hygiene / doc-dating / artifact / lock-sync checks
(extracted from check_repository_consistency.py — check.py split track・category "repo hygiene").

Non-contiguous cluster of Checks 31/32/33/34/35/36/38/39/40/41: Claude2Claude ↔ AI2AI record (31),
index.html JSON-LD valid (32), Zenn slug set (33), per-file doc dating (34・WARNING), robots↔sitemap
(35), sitemap no-future-date (36・WARNING), package.json↔lock sync (38), sitemap loc→committed file
(39), CSS lint path hygiene (40), AIO monitoring-log↔manifest atomic-commit (41). Check 37 (no
generated/cache artifacts tracked) is NOT included — it is the PRODUCER of the module-level
`_member_paths` / `_repo_member_paths` shared with later monolith consumers, a producer/consumer
coupling left in the monolith. Each Check here reads its own target files directly; no shared-var
coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  31. Claude2Claude.md references AI2AI.md's current max Session Record
  32. index.html application/ld+json blocks are valid JSON (BLOCKING)
  33. Zenn featuring layers share the canonical article slug set + PRIMARY (BLOCKING)
  34. doc Last-Updated equals its sitemap <lastmod> — honest dating (WARNING)
  35. robots.txt advertises a Sitemap: directive resolving to sitemap.xml (BLOCKING)
  36. sitemap.xml has no future-dated <lastmod> (WARNING)
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
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract

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
