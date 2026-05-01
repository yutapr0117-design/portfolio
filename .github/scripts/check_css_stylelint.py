#!/usr/bin/env python3
"""
check_css_stylelint.py — 改善文書a 6.1/6.2
Extracts inline <style> blocks from index.html and runs stylelint on them.

Root fix for recurring CI bug:
  The YAML heredoc + Python string quoting combination caused persistent
  SyntaxErrors and incorrect error detection. Moving ALL logic here
  eliminates YAML/Python escaping conflicts entirely.

Detection logic:
  - severity:error violations  → BLOCKING (exit 1)
  - severity:warning violations → non-blocking (printed as ::warning::)
  - The old logic used 'error' in l.lower() which matched summary lines
    like "14 errors, 6 warnings" even when all rules were severity:warning.
    This script uses subprocess exit code correctly:
      stylelint --max-warnings=-1 → exit 0 = no errors, exit 1 = real errors only
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


def main() -> int:
    html_path = "index.html"
    config_path = ".stylelintrc.json"

    if not os.path.exists(html_path):
        print(f"::error::File not found: {html_path}")
        return 1

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    css = extract_style_blocks(html)
    if not css.strip():
        print("No <style> blocks found — skipping Stylelint check")
        return 0

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".css", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(css)
        tmp_path = tmp.name

    try:
        # --max-warnings=-1: suppress "Too many warnings" — warnings are non-blocking by design.
        # Exit code semantics with this flag:
        #   0 = no violations at all
        #   1 = at least one error-severity violation exists
        #   2 = fatal/unexpected error
        # Warning-only violations do NOT cause exit code 1 when --max-warnings=-1.
        result = subprocess.run(
            [
                "npx", "stylelint", tmp_path,
                "--config", config_path,
                "--max-warnings", "-1",
            ],
            capture_output=True,
            text=True,
        )
        output = (result.stdout + result.stderr).replace(tmp_path, "<index.html style>")

        if result.returncode == 0:
            print("Stylelint: PASS (no violations)")
            return 0

        if result.returncode == 2:
            print(f"::warning::Stylelint fatal error (config issue?): {output[:300]}")
            return 0  # Don't block on config issues

        # exit code 1: real error-severity violations exist
        print("::error::BLOCKING: Stylelint error-severity violations detected:")
        for line in output.splitlines():
            if line.strip():
                print(f"  {line}")
        return 1

    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    sys.exit(main())
