"""
checks_structural.py — structural parse / CI wiring / tooling integrity checks
(extracted from check_repository_consistency.py — check.py split track・category E).

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/errors/warnings (同一参照・exec 不使用).
NOTE: Check 47/56/57/61 (_modules47 js-leaf source-of-truth を共有する coupled cluster) は
Phase 6 で checks_esm.py へ一括抽出済 (このモジュールとは別ファイル)。

Check inventory (Check 45 enforces sync with the `# \u2500\u2500 N.` sections in run()):
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
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    warnings = ctx.warnings
    read = ctx.read
    extract = ctx.extract

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
