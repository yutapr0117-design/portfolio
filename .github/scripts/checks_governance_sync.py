"""
checks_governance_sync.py — AIO / AI2AI / llms freshness & session-record governance sync checks
(extracted from check_repository_consistency.py — check.py split track・category "governance sync").

Contiguous cluster of Checks 21-27: llms alias Last-Updated sync (21), AI2AI Session Record ordering
(22), workflow/dependabot YAML syntax (23), llms-full freshness vs AI2AI (24), aio-monitoring-log
evidence_policy key (25), AI2AI-archive max session record == manifest role (26), llms-full no stale
C1-C6 in current-description (27). Each Check reads its own target files directly; no global-content
or cross-section var coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  21. llms alias files Last-Updated are in sync
  22. AI2AI.md Session Record headers are in ascending order
  23. .github/workflows/*.yml and dependabot.yml parse without YAML syntax errors
  24. llms-full.txt Last-Updated is within 7 days of AI2AI.md and >= v75-v78 floor
  25. aio-monitoring-log.json has an evidence_policy key (attempt_log_only honesty)
  26. aio-manifest.json archive role #1-#N matches AI2AI-archive.md max Session Record
  27. llms-full.txt has no stale C1–C6 in current-constraint context (should be C1–C7)
  436. 規範層 (docs/architecture/) に「オーナー裁可待ち」型の defer 理由が残らない: canon
       (AI2AI.md STEP 3 / CLAUDE.md §7) は 2026-08-18 に「**オーナー裁可が要る項目なんか一切
       無い**」「C5 は『人間がコードを書かない』の意であって設計判断を defer する根拠ではない」
       「**「裁可待ち」という作業カテゴリは存在しない**」と明記した。しかし canon を直しても、
       **その canon を根拠に書かれた下流の規範文書は自動では直らない**。実際 2026-08-20 の
       棚卸しで research-application-policy.md が「適用条件: オーナーが配色変更を裁可した時」
       を現行ガイダンスとして保持しており、しかもその項目は既に #1158 で解決済みだった ——
       読み手は**否定された規則を持ち帰る**。scope を `docs/architecture/` (規範層) に限るのは、
       `docs/incident-artifacts/` が**性質上の歴史記録**で、そこへ注記を強制すると履歴を
       濁す圧力になるため (#977 の「書き換えれば履歴を偽る」判断と同じ線引き)。
       否定・超越を明示する行 (SUPERSEDED / 否定された / 存在しない 等) は違反にしない。 (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract
    warnings = ctx.warnings

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

    # ── 436. 規範層に「オーナー裁可待ち」型の defer 理由を残さない (BLOCKING) ────────
    # canon を直しても、その canon を根拠に書かれた**下流の規範文書は自動では直らない**。
    # 2026-08-20 の棚卸しで research-application-policy.md が「適用条件: オーナーが配色変更を
    # 裁可した時」を現行ガイダンスとして保持しており、しかもその項目は #1158 で解決済みだった。
    # 歴史記録 (docs/incident-artifacts/) は対象外 —— そこへ注記を強制すると履歴を濁す。
    _DEFER436 = ("裁可待ち", "裁可した時", "裁可を待", "C5（人間）の領域", "C5 (人間) の領域")
    _OK436 = ("SUPERSEDED", "否定された", "存在しない", "読み違い", "解決済み", "誤りだった")
    _viol436 = []
    for _f in sorted((ROOT / "docs" / "architecture").glob("*.md")):
        for _n, _line in enumerate(_f.read_text(encoding="utf-8").splitlines(), 1):
            if any(_p in _line for _p in _DEFER436) and not any(_o in _line for _o in _OK436):
                _viol436.append(f"{_f.name}:{_n}")
    check(
        not _viol436,
        f"Check 436: 規範層 docs/architecture/ に「裁可待ち」型の defer 理由が無い",
        (f"Check 436: 規範層に canon が否定した defer 理由が残っている: {_viol436[:5]}。"
         "canon (AI2AI.md STEP 3 / CLAUDE.md §7) は「オーナー裁可が要る項目なんか一切無い」"
         "「C5 は『人間がコードを書かない』の意」「『裁可待ち』という作業カテゴリは存在しない」"
         "と明記している。規範文書に残ると**読み手が否定された規則を持ち帰る**。"
         "解決済みなら SUPERSEDED / 解決済み を、記録として残すなら『否定された』等を同じ行に"
         "書いて超越を明示せよ (歴史記録の docs/incident-artifacts/ は対象外)"),
        blocking=True,
    )
