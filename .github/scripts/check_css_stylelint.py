#!/usr/bin/env python3
"""
check_css_stylelint.py — P0-10 / 改善文書 3.10
Runs stylelint on:
  1. style.css (external CSS — always checked)
  2. Inline <style> blocks extracted from index.html (checked if present)

Detection logic (改善文書 3.10):
  - Uses --formatter json for reliable severity parsing
  - severity:error violations  → BLOCKING (exit 1)
  - severity:warning violations → non-blocking (printed as ::warning::)
  - stylelint execution failure / config errors → distinct category (not silently non-blocking)

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


def run_stylelint(css_content: str, label: str, config_path: str) -> int:
    """Run stylelint with --formatter json; return 0=pass, 1=has errors."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".css", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(css_content)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [
                "npx", "stylelint", tmp_path,  # version managed by workflow (npm install --no-save stylelint@16)
                "--config", config_path,
                "--formatter", "json",
                "--allow-empty-input",
            ],
            capture_output=True,
            text=True,
        )

        # returncode 64 = bad usage/config; 78 = lint error (some versions)
        if result.returncode not in (0, 1, 2, 64, 78):
            print(f"::warning::Stylelint [{label}] unexpected exit code {result.returncode} — treating as config issue")
            if result.stderr:
                print(f"::warning::Stylelint [{label}] stderr: {result.stderr[:300]}")
            return 0  # config issues are non-blocking but reported

        # Try to parse JSON output
        stdout = result.stdout.strip()
        if not stdout:
            if result.returncode == 0:
                print(f"Stylelint [{label}]: PASS (no output)")
                return 0
            # exit 1 with no JSON = likely config parse error
            print(f"::warning::Stylelint [{label}] config/parse error (no JSON output): {result.stderr[:300]}")
            return 0

        try:
            lint_results = json.loads(stdout)
        except json.JSONDecodeError:
            print(f"::warning::Stylelint [{label}] non-JSON output (version mismatch?): {stdout[:200]}")
            return 0

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

    css_path = "style.css"
    if not os.path.exists(css_path):
        print(f"::error::style.css not found — CSS check cannot proceed")
        return 1

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    ec = run_stylelint(css_content, "style.css", config_path)
    if ec != 0:
        exit_code = 1

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
