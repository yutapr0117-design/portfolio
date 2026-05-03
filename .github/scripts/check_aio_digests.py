"""
check_aio_digests.py — AIO digest consistency CI check

Verifies:
  1. .well-known/index.json and .well-known/agent-skills/index.json are byte-identical.
  2. Each skill's digest matches the SHA-256 of the corresponding local file.

Exit codes:
  0 — all checks passed
  1 — any check failed (CI blocking)
"""

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]

INDEX_FILES = [
    ROOT / ".well-known" / "index.json",
    ROOT / ".well-known" / "agent-skills" / "index.json",
]

URL_TO_LOCAL = {
    "https://yutapr0117-design.github.io/portfolio/llms-full.txt": ROOT / "llms-full.txt",
    "https://yutapr0117-design.github.io/portfolio/AI2AI.md": ROOT / "AI2AI.md",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors = []

    # Load both index files
    payloads = []
    for p in INDEX_FILES:
        if not p.exists():
            errors.append(f"Missing required file: {p.relative_to(ROOT)}")
            continue
        try:
            payloads.append(json.loads(p.read_text(encoding="utf-8")))
        except json.JSONDecodeError as e:
            errors.append(f"JSON parse error in {p.relative_to(ROOT)}: {e}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    # Check byte-identity
    raw = [p.read_bytes() for p in INDEX_FILES]
    if raw[0] != raw[1]:
        print("ERROR: .well-known/index.json and .well-known/agent-skills/index.json are NOT byte-identical")
        return 1

    # Check each skill digest
    failed = False
    for skill in payloads[0].get("skills", []):
        url = skill.get("url", "")
        digest = skill.get("digest", "")
        local = URL_TO_LOCAL.get(url)

        if not local:
            print(f"ERROR: unknown skill URL (no local mapping): {url}")
            failed = True
            continue

        if not local.exists():
            print(f"ERROR: local file not found for {url}: {local.relative_to(ROOT)}")
            failed = True
            continue

        expected = "sha-256:" + sha256_file(local)
        if digest != expected:
            print(f"ERROR: digest mismatch for {url}")
            print(f"  expected : {expected}")
            print(f"  in file  : {digest}")
            failed = True
        else:
            print(f"OK: {url}")

    if failed:
        return 1

    print("AIO digest check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
