#!/usr/bin/env python3
"""
extract_js_for_eslint.py — 改善文書a 3.2
Extracts inline JS blocks from index.html and writes them to /tmp/_eslint_check.js
for ESLint to consume. Runs as a standalone script to avoid YAML/Python
quoting conflicts entirely.
"""

import re
import sys
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


def main() -> int:
    output_path = "/tmp/_eslint_check.js"
    html_path = "index.html"

    if not os.path.exists(html_path):
        print(f"::error::File not found: {html_path}")
        return 1

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    blocks = extract_js_blocks(html)
    combined = "\n;\n".join(blocks)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(combined)

    print(f"Extracted {len(blocks)} JS blocks ({len(combined)} chars) to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
