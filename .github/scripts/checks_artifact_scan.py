"""
checks_artifact_scan.py — generated/cache artifact tracking guard (37)
(extracted from check_repository_consistency.py — check.py split track・category "artifact scan"・
ctx-enrich module).

Verifies that no generated/cache artifacts (node_modules, __pycache__, *.pyc, test-results,
playwright-report, blob-report, .DS_Store, …) are tracked in the repository.

.gitignore prevents *new* accidental staging, but it does NOT detect artifacts that are
already tracked, nor ones that slipped into a distributed ZIP. This check makes
re-introduction a hard CI failure. It judges *repository membership*, so the source of truth
is `git ls-files` (already computed by the monolith's setup into `ctx._member_paths`).

Dependencies:
- ctx._member_paths  (list of repo-relative POSIX paths, pre-computed by monolith setup)
- ctx.check
- Module-local FORBIDDEN_* constants mirror the monolith definitions — kept in sync via
  Check 45/70/105 self-integrity and the fact that both sets are declared together. The
  constants are duplicated here because they must be identical and are stable; the
  check itself catches any drift when the test suite is run.

Executed at Check 37's original position in list order. Self-integrity: aggregated by
_aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105 span this file).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  37. No generated/cache artifacts are tracked in the repository (BLOCKING)
"""

_FORBIDDEN_PATH_PARTS = {
    "__pycache__",
    "node_modules",
    "test-results",
    "playwright-report",
    "blob-report",
    ".pytest_cache",
}
_FORBIDDEN_NAMES = {
    ".DS_Store",
    "Thumbs.db",
    "npm-debug.log",
}
_FORBIDDEN_SUFFIXES = (".pyc", ".pyo")


def run(ctx):
    check = ctx.check
    member_paths = ctx._member_paths

    # ── 37. No generated/cache artifacts are tracked in the repository (BLOCKING) ──
    _artifact_hits = []
    for _p in member_paths:
        _name = _p.rsplit("/", 1)[-1]
        if set(_p.split("/")) & _FORBIDDEN_PATH_PARTS:
            _artifact_hits.append(_p)
        elif _name in _FORBIDDEN_NAMES:
            _artifact_hits.append(_p)
        elif _p.endswith(_FORBIDDEN_SUFFIXES):
            _artifact_hits.append(_p)

    check(
        not _artifact_hits,
        f"Check 37: no generated/cache artifacts tracked in repository (scanned {len(member_paths)} paths)",
        "Check 37: generated/cache artifact(s) present in repository tree — remove from Git and "
        "keep them in .gitignore: " + ", ".join(sorted(_artifact_hits)[:10])
        + (" …" if len(_artifact_hits) > 10 else ""),
        blocking=True,
    )
