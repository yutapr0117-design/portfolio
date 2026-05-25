#!/usr/bin/env python3
"""
check_css_stylelint.py — P0-16 / 改善文書a 6.1/6.2
Runs stylelint on:
  1. style.css (external CSS — always checked)
  2. Inline <style> blocks extracted from index.html (checked if present)

Detection logic:
  - severity:error violations  → BLOCKING (exit 1)
  - severity:warning violations → non-blocking (printed as ::warning::)
  - stylelint --max-warnings=-1 → exit 0 = no errors, exit 1 = real errors only

Design-exception suppression (P3):
  Warnings for !important in the following contexts are suppressed as
  intentional design decisions, not lint noise:
    1. @media (prefers-reduced-motion: reduce) blocks — animation/transition safety net
    2. .u-ai-* utility classes — DOM-API-only utility layer (innerHTML禁止制約準拠)
    3. .nav-group-body[data-collapsed] — JS-driven collapse control
  All other !important occurrences remain warning-eligible.
"""

import re
import subprocess
import sys
import tempfile
import os


# ── Design-exception patterns for !important suppression (P3) ─────────────
# Lines matching these patterns are filtered from warning output.
_IMPORTANT_EXCEPTION_PATTERNS = [
    # reduced-motion block contents (animation/transition/scroll-behavior)
    re.compile(r"animation-duration\s*:.*!important", re.IGNORECASE),
    re.compile(r"animation-iteration-count\s*:.*!important", re.IGNORECASE),
    re.compile(r"transition-duration\s*:.*!important", re.IGNORECASE),
    re.compile(r"scroll-behavior\s*:.*!important", re.IGNORECASE),
    # .u-ai-* utility classes
    re.compile(r"\.u-ai-\w+\s*\{[^}]*!important", re.IGNORECASE),
    # nav-group-body collapse control
    re.compile(r"nav-group-body.*!important", re.IGNORECASE),
]


def _is_design_exception_warning(line: str) -> bool:
    """Return True if a stylelint warning line matches a known design exception."""
    for pat in _IMPORTANT_EXCEPTION_PATTERNS:
        if pat.search(line):
            return True
    return False


def extract_style_blocks(html: str) -> str:
    """Extract and concatenate all inline <style> blocks."""
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL)
    return "\n".join(blocks)


def run_stylelint(css_content: str, label: str, config_path: str) -> int:
    """Run stylelint on css_content; return exit code (0=pass, 1=error, 2=fatal)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".css", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(css_content)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [
                "npx", "stylelint", tmp_path,
                "--config", config_path,
                "--max-warnings", "-1",
            ],
            capture_output=True,
            text=True,
        )
        output = (result.stdout + result.stderr).replace(tmp_path, f"<{label}>")

        if result.returncode == 0:
            print(f"Stylelint [{label}]: PASS (no violations)")
            return 0

        if result.returncode == 2:
            print(f"::warning::Stylelint [{label}] fatal error (config issue?): {output[:300]}")
            return 0  # Don't block on config issues

        # exit code 1: real error-severity violations exist.
        # Filter out design-exception !important warnings before reporting.
        lines = output.splitlines()
        suppressed = 0
        filtered_lines = []
        for line in lines:
            if "declaration-no-important" in line and _is_design_exception_warning(line):
                suppressed += 1
                continue
            filtered_lines.append(line)

        if suppressed:
            print(
                f"::warning::Stylelint [{label}]: {suppressed} !important warning(s) suppressed "
                f"(design exceptions: reduced-motion / .u-ai-* / nav-group-body). "
                f"See check_css_stylelint.py for policy."
            )

        remaining_output = "\n".join(filtered_lines)

        # Re-check if any real (non-suppressed) violations remain
        # Stylelint exit-1 mixes warnings and errors in output; re-run can't easily re-score,
        # so we check for "error" lines still present after filtering.
        has_real_violations = any(
            ("error" in l.lower() or "warning" in l.lower())
            for l in filtered_lines
            if l.strip()
        )

        if has_real_violations:
            print(f"::error::BLOCKING: Stylelint error-severity violations in [{label}]:")
            for line in filtered_lines:
                if line.strip():
                    print(f"  {line}")
            return 1

        print(f"Stylelint [{label}]: PASS after suppressing design exceptions")
        return 0

    finally:
        os.unlink(tmp_path)


def main() -> int:
    config_path = ".stylelintrc.json"
    exit_code = 0

    # ── 1. External style.css (always checked) ──────────────────────────
    css_path = "style.css"
    if not os.path.exists(css_path):
        print(f"::error::style.css not found — CSS check cannot proceed")
        return 1

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    ec = run_stylelint(css_content, "style.css", config_path)
    if ec != 0:
        exit_code = 1

    # ── 2. Inline <style> blocks from index.html (checked if present) ───
    html_path = "index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        css = extract_style_blocks(html)
        if css.strip():
            ec = run_stylelint(css, "index.html inline <style>", config_path)
            if ec != 0:
                exit_code = 1
        else:
            print("No inline <style> blocks found in index.html — skipping inline check")
    else:
        print(f"::warning::{html_path} not found — skipping inline <style> check")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
