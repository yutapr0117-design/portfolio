#!/usr/bin/env python3
"""
check_js_syntax.py — 改善文書a 3.1
Extracts inline JS blocks from index.html and checks each for syntax errors
using `node --check`. Runs as a standalone script to avoid YAML/Python
quoting conflicts entirely.

Design decision (root fix):
  This project is Boring Technology (Vanilla JS, no TypeScript).
  Running tsc strict-mode on concatenated inline HTML scripts causes:
    1. Third-party minified blocks (KARTE etc.) trigger false errors
    2. Valid DOM patterns (Node.hasAttribute &&, EventTarget.closest) are
       flagged due to tsc type-narrowing — these are NOT real bugs
    3. MutationObserver NodeList typing is a tsc-only issue, not a runtime bug
  Solution: syntax-only check via `node --check` catches real breakage
  (SyntaxError, unexpected token etc.) without false positives.
  Type-level bug detection is fully delegated to ESLint (Step 24).
"""

import re
import sys
import subprocess
import tempfile
import os


def extract_js_blocks(html: str) -> list[str]:
    """Extract inline JS blocks, excluding third-party minified and non-JS types."""
    raw_pairs = re.findall(r"<script([^>]*)>(.*?)</script>", html, re.DOTALL | re.IGNORECASE)
    js_blocks = []
    for attrs, body in raw_pairs:
        a = attrs.lower()

        # Exclude external scripts
        if "src=" in a:
            continue

        # Exclude third-party minified single-line blocks (e.g. KARTE: !function(...){...})
        stripped = body.strip()
        if stripped.startswith("!function") and "\n" not in stripped:
            print(f"Skipped minified third-party block: {stripped[:60]}...")
            continue

        # Exclude non-JS types (application/ld+json, importmap, etc.)
        m = re.search(r'type\s*=\s*["\x27]([^"\x27]*)["\x27]', a, re.IGNORECASE)
        if m:
            t = m.group(1).strip()
            if t and t not in ("text/javascript", "module"):
                continue

        js_blocks.append(body)

    return js_blocks


def check_block(block: str, index: int) -> list[str]:
    """Run node --check on a single JS block. Returns list of error lines."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".js", delete=False, encoding="utf-8"
    ) as tf:
        tf.write(block)
        tf_path = tf.name

    try:
        result = subprocess.run(
            ["node", "--check", tf_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # Replace temp path with readable label
            err = result.stderr.replace(tf_path, f"<inline-block-{index+1}>")
            return [err.strip()]
        return []
    finally:
        os.unlink(tf_path)


def main() -> int:
    html_path = "index.html"
    if not os.path.exists(html_path):
        print(f"::error::File not found: {html_path}")
        return 1

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    blocks = extract_js_blocks(html)
    print(f"Checking {len(blocks)} JS blocks with node --check...")

    all_errors = []
    for i, block in enumerate(blocks):
        errs = check_block(block, i)
        if errs:
            for e in errs:
                print(f"::error::BLOCKING: Syntax error in inline JS block {i+1}:\n{e}")
            all_errors.extend(errs)

    if all_errors:
        print(f"::error::BLOCKING: {len(all_errors)} JS block(s) have syntax errors. Fix before merging.")
        return 1

    print(f"node --check: ALL {len(blocks)} blocks PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
