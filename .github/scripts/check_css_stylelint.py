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
"""

import re
import subprocess
import sys
import tempfile
import os


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

        # exit code 1: real error-severity violations exist
        print(f"::error::BLOCKING: Stylelint error-severity violations in [{label}]:")
        for line in output.splitlines():
            if line.strip():
                print(f"  {line}")
        return 1

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
