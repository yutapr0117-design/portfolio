"""
checks_csp_hashes.py — inline-script CSP hash verification (7b/7c)
(extracted from check_repository_consistency.py — check.py split track・category "CSP hashes"・
ctx-enrich module).

Verifies that the SHA-256 content hashes for inline <script> blocks in index.html are
present in the CSP script-src header. Content is hashed from the live DOM source, so
this catches BOTH a removed hash AND content edited without recomputing the hash.

Dependencies:
- ctx.html    (index.html content, pre-loaded by monolith)
- ctx.check, ctx.warnings
- Standard library: re, hashlib, base64 (via _lib_io.csp_sri_hash helper)

Executed at Check 7b's original position in list order. Self-integrity: aggregated by
_aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105 span this file).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  7b. inline suppressor <script> hash present in CSP script-src
  7c. inline speculation-rules <script type="speculationrules"> hash present in CSP script-src
"""
import re

from _lib_io import csp_sri_hash as _lib_csp_sri_hash


def run(ctx):
    check = ctx.check
    html = ctx.html
    warnings = ctx.warnings

    # ── 7b. inline suppressor CSP hash ───────────────────────────────────────────
    # Strip HTML comments first: comments may contain literal <script>...</script> strings
    # (e.g. the CSP architecture note documents the speculationrules tag), which would
    # otherwise corrupt regex-based extraction. The browser never hashes comment text.
    _html_nc = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

    _plain_scripts = re.findall(r"<script>(.*?)</script>", _html_nc, re.DOTALL)
    _sup_content = next((s for s in _plain_scripts if "unhandledrejection" in s), None)
    if _sup_content is not None:
        _sup_hash = _lib_csp_sri_hash(_sup_content)
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

    # ── 7c. inline speculation-rules CSP hash ────────────────────────────────────
    _m_spec = re.search(r'<script type="speculationrules">(.*?)</script>', _html_nc, re.DOTALL)
    if _m_spec is not None:
        _spec_hash = _lib_csp_sri_hash(_m_spec.group(1))
        check(
            f"'{_spec_hash}'" in html,
            f"index.html CSP authorizes inline speculation rules (content hash {_spec_hash})",
            f"index.html CSP does NOT authorize inline speculation rules — computed {_spec_hash} "
            f"is absent from script-src. Chrome will block prerender with "
            f'"Applying inline speculation rules violates ... script-src". '
            f"Add '{_spec_hash}' to script-src (recompute if the JSON was edited).",
        )
    else:
        warnings.append("index.html: speculationrules block not found — Check 7c skipped")
