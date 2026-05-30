#!/usr/bin/env python3
"""
check_repository_consistency.py — P0-23 / Cross-file consistency check (BLOCKING)

Verifies that key version, date, and structural invariants hold across the repository.

Checks performed:
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
  23. .github/workflows/*.yml and dependabot.yml parse without YAML syntax errors

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

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []
warnings: list[str] = []


def check(condition: bool, msg_ok: str, msg_fail: str, blocking: bool = True) -> None:
    if condition:
        print(f"OK: {msg_ok}")
    else:
        tag = "ERROR" if blocking else "WARNING"
        print(f"{tag}: {msg_fail}")
        (errors if blocking else warnings).append(msg_fail)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_bytes(path: str) -> bytes:
    return (ROOT / path).read_bytes()


def extract(pattern: str, text: str) -> str | None:
    m = re.search(pattern, text)
    return m.group(1) if m else None


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
    return "sha256-" + base64.b64encode(
        hashlib.sha256(content.encode("utf-8")).digest()
    ).decode()

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

    for _ln28, _line28 in enumerate(_spec_lines_28, 1):
        # A top-level test() definition starts at column 0
        if _re_spec28.match(r"^test\s*\(", _line28):
            if _test_start_depth_28 is not None:
                _nesting_errors_28.append(
                    f"line {_ln28}: test() opened while previous test() "
                    f"(started at brace-depth {_test_start_depth_28}) is not yet closed"
                )
            _test_start_depth_28 = _brace_depth_28  # record depth *before* this line

        # Naive brace counting (works for this file; strings do not contain unbalanced braces)
        _brace_depth_28 += _line28.count("{") - _line28.count("}")

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
