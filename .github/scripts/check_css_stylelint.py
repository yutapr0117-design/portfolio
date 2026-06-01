#!/usr/bin/env python3
"""
check_css_stylelint.py — P0-10 / 改善文書 3.10
                          + P0-01 (v80+ Phase 2 CI-hygiene increment #3)
Runs stylelint on:
  1. style.css (external CSS — always checked)
  2. Inline <style> blocks extracted from index.html (checked if present)

Detection logic (改善文書 3.10):
  - Uses --formatter json for reliable severity parsing
  - severity:error violations  → BLOCKING (exit 1)
  - severity:warning violations → non-blocking (printed as ::warning::)
  - stylelint execution failure / config errors → distinct category (not silently non-blocking)

Execution-path hygiene (P0-01, decision-v80-phase2-ci-hygiene-3):
  Phase 2-A introduced package.json / package-lock.json / `npm ci`, so the
  stylelint binary is now installed locally under node_modules/.bin. This
  script therefore PREFERS that local binary and only falls back to `npx`
  when node_modules is absent (e.g. a local checkout that skipped `npm ci`).
  Rationale: `npx` may resolve stylelint through the npm cache or the network,
  which makes the result depend on cache/network/permission state — a source
  of non-reproducible runs and, worse, of false-green CI (a config or
  execution error that silently exits 0).

  To kill that false-green, execution/config failures are escalated to
  BLOCKING (exit 1) whenever stylelint is *expected* to run cleanly. That
  condition is captured by the `strict` predicate:
      strict = used_local_binary OR CI
  - used_local_binary is True  → the binary is installed, so any failure to
    run it (bad config, parse error, non-JSON output, unexpected exit code)
    is a real defect, regardless of where we run.
  - CI is True (env CI / GITHUB_ACTIONS) → on a runner we always demand a
    clean run; an npx-fallback failure there is blocking too.
  - Only the local-without-node_modules case (strict False) degrades
    gracefully: the failure is reported as a note and exits 0, so a developer
    who simply forgot `npm ci` is not hard-blocked locally.

Design-exception suppression:
  Warnings for !important in the following contexts are suppressed as
  intentional design decisions, not lint noise:
    1. @media (prefers-reduced-motion: reduce) blocks
    2. .u-ai-* utility classes (DOM-API-only utility layer)
    3. .nav-group-body[data-collapsed] — JS-driven collapse control
"""

import json
import re
import subprocess
import sys
import tempfile
import os
from pathlib import Path


# Repo root, resolved from this script's location (…/.github/scripts/<this>),
# so the local-binary lookup is correct no matter what the current working
# directory is. (File arguments below stay relative to CWD, preserving the
# pre-existing behaviour of `npm run lint:css`, which runs from the repo root.)
ROOT = Path(__file__).resolve().parents[2]

# CI detection: GitHub Actions sets both, but we accept the generic CI flag too
# so any CI provider triggers strict mode.
CI_MODE = bool(os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"))


def resolve_stylelint_cmd():
    """Return (cmd_prefix, used_local).

    Prefers node_modules/.bin/stylelint (installed by `npm ci`); falls back to
    `npx stylelint` only when that local binary is absent. `used_local` feeds
    the `strict` escalation described in the module docstring.
    """
    local_bin = ROOT / "node_modules" / ".bin" / "stylelint"
    if local_bin.exists():
        return [str(local_bin)], True
    return ["npx", "stylelint"], False


_IMPORTANT_EXCEPTION_PATTERNS = [
    re.compile(r"animation-duration\s*:.*!important", re.IGNORECASE),
    re.compile(r"animation-iteration-count\s*:.*!important", re.IGNORECASE),
    re.compile(r"transition-duration\s*:.*!important", re.IGNORECASE),
    re.compile(r"scroll-behavior\s*:.*!important", re.IGNORECASE),
    re.compile(r"\.u-ai-\w+\s*\{[^}]*!important", re.IGNORECASE),
    re.compile(r"nav-group-body.*!important", re.IGNORECASE),
]


def _is_design_exception(rule: str, text: str) -> bool:
    if rule != "declaration-no-important":
        return False
    for pat in _IMPORTANT_EXCEPTION_PATTERNS:
        if pat.search(text):
            return True
    return False


def extract_style_blocks(html: str) -> str:
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL)
    return "\n".join(blocks)


def run_stylelint(
    css_content: str,
    label: str,
    config_path: str,
    cmd_prefix: list,
    strict: bool,
) -> int:
    """Run stylelint with --formatter json; return 0=pass, 1=has errors.

    cmd_prefix: either [<local-binary>] or ["npx", "stylelint"] (see
        resolve_stylelint_cmd).
    strict: when True, execution/config failures that previously exited 0
        silently are escalated to BLOCKING (return 1). See module docstring
        for the `strict = used_local OR CI` rationale.
    """
    # Helper: a config/execution failure (NOT a lint violation). Under strict
    # mode these become blocking; otherwise we keep the historical graceful
    # behaviour (report + exit 0) so a local run without `npm ci` is not
    # hard-blocked.
    def _exec_failure(message: str) -> int:
        severity = "error" if strict else "warning"
        suffix = "" if strict else " (non-blocking: local run without node_modules)"
        print(f"::{severity}::Stylelint [{label}] {message}{suffix}")
        return 1 if strict else 0

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".css", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(css_content)
        tmp_path = tmp.name

    try:
        try:
            result = subprocess.run(
                [
                    *cmd_prefix, tmp_path,  # binary resolved by resolve_stylelint_cmd(): local node_modules/.bin/stylelint preferred, npx fallback
                    "--config", config_path,
                    "--formatter", "json",
                    "--allow-empty-input",
                ],
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            # Neither the local binary nor npx is invocable. Under strict mode
            # (CI, or local binary that vanished mid-run) this is a hard fail.
            return _exec_failure("could not be executed (stylelint not found on PATH and no local binary)")

        # returncode 64 = bad usage/config; 78 = lint error (some versions)
        if result.returncode not in (0, 1, 2, 64, 78):
            detail = f"unexpected exit code {result.returncode}"
            if result.stderr:
                detail += f" — stderr: {result.stderr[:300]}"
            return _exec_failure(detail)

        # Try to parse JSON output
        stdout = result.stdout.strip()
        if not stdout:
            if result.returncode == 0:
                print(f"Stylelint [{label}]: PASS (no output)")
                return 0
            # exit 1 with no JSON = likely config parse error
            return _exec_failure(f"config/parse error (no JSON output): {result.stderr[:300]}")

        try:
            lint_results = json.loads(stdout)
        except json.JSONDecodeError:
            return _exec_failure(f"non-JSON output (version mismatch?): {stdout[:200]}")

        error_count = 0
        warning_count = 0
        suppressed_count = 0

        for file_result in lint_results:
            for warning in file_result.get("warnings", []):
                rule = warning.get("rule", "")
                severity = warning.get("severity", "warning")
                text = warning.get("text", "")
                line = warning.get("line", "?")
                col = warning.get("column", "?")

                if _is_design_exception(rule, text):
                    suppressed_count += 1
                    continue

                location = f"{label}:{line}:{col}"
                if severity == "error":
                    error_count += 1
                    print(f"::error::Stylelint error [{location}] {rule}: {text}")
                else:
                    warning_count += 1
                    print(f"::warning::Stylelint warning [{location}] {rule}: {text}")

        if suppressed_count:
            print(
                f"::warning::Stylelint [{label}]: {suppressed_count} !important warning(s) suppressed "
                f"(design exceptions: reduced-motion / .u-ai-* / nav-group-body)."
            )

        if error_count == 0 and warning_count == 0 and suppressed_count == 0:
            print(f"Stylelint [{label}]: PASS (no violations)")
        elif error_count == 0:
            print(f"Stylelint [{label}]: PASS ({warning_count} warning(s), {suppressed_count} suppressed)")
        else:
            print(f"::error::BLOCKING: Stylelint [{label}]: {error_count} error(s), {warning_count} warning(s)")
            return 1

        return 0

    finally:
        os.unlink(tmp_path)


def main() -> int:
    config_path = ".stylelintrc.json"
    exit_code = 0

    # Resolve the execution path once, up front, and announce it. This single
    # decision (local binary vs npx) plus CI_MODE determines `strict`, which is
    # then applied uniformly to every stylelint invocation below.
    cmd_prefix, used_local = resolve_stylelint_cmd()
    strict = used_local or CI_MODE
    runner = "node_modules/.bin/stylelint (local)" if used_local else "npx stylelint (fallback)"
    mode = "strict (failures BLOCKING)" if strict else "lenient (local, no node_modules)"
    print(f"CSS lint runner: {runner} — {mode}; CI={CI_MODE}")
    if not used_local and CI_MODE:
        # On a runner the local binary should always exist after `npm ci`; its
        # absence is itself suspicious, so surface it (still strict-blocking).
        print("::warning::Local stylelint binary not found in CI — falling back to npx (check `npm ci` step).")

    css_path = "style.css"
    if not os.path.exists(css_path):
        print(f"::error::style.css not found — CSS check cannot proceed")
        return 1

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    ec = run_stylelint(css_content, "style.css", config_path, cmd_prefix, strict)
    if ec != 0:
        exit_code = 1

    html_path = "index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        css = extract_style_blocks(html)
        if css.strip():
            ec = run_stylelint(css, "index.html inline <style>", config_path, cmd_prefix, strict)
            if ec != 0:
                exit_code = 1
        else:
            print("No inline <style> blocks found in index.html — skipping inline check")
    else:
        print(f"::warning::{html_path} not found — skipping inline <style> check")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
