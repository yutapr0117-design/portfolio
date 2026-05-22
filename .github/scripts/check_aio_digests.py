"""
check_aio_digests.py — AIO digest consistency CI check

Verifies:
  1. .well-known/index.json and .well-known/agent-skills/index.json are byte-identical.
  2. Each skill's digest matches the SHA-256 of the corresponding local file.
  3. .well-known/aio-manifest.json sha256 fields match the SHA-256 of each local file
     in source_of_truth, supporting_evidence, and observational_evidence sections.
     (generated_at and manifest_version fields are not checked — updated by CI.)

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

MANIFEST_FILE = ROOT / ".well-known" / "aio-manifest.json"

URL_TO_LOCAL = {
    "https://yutapr0117-design.github.io/portfolio/llms-full.txt": ROOT / "llms-full.txt",
    "https://yutapr0117-design.github.io/portfolio/AI2AI.md": ROOT / "AI2AI.md",
}

# aio-manifest path → local file (relative to repo root)
MANIFEST_PATH_TO_LOCAL: dict[str, Path] = {
    "llms.txt":       ROOT / "llms.txt",
    "llms-full.txt":  ROOT / "llms-full.txt",
    "AI2AI.md":       ROOT / "AI2AI.md",
    "yuta-yokoi-ai-pm-orchestration-system.webp":
        ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp",
    "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3":
        ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3",
    # supporting_evidence
    "Claude2Claude.md":
        ROOT / "Claude2Claude.md",
    "ChatGPT2ChatGPT.md":
        ROOT / "ChatGPT2ChatGPT.md",
    "docs/evidence/ai-pioneer-identity-review.md":
        ROOT / "docs" / "evidence" / "ai-pioneer-identity-review.md",
    # observational_evidence
    "docs/evidence/aio-monitoring-log.json":
        ROOT / "docs" / "evidence" / "aio-monitoring-log.json",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_index_files() -> tuple[bool, list[str]]:
    """index.json byte-identity + skill digest verification."""
    errors: list[str] = []
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
        return False, errors

    raw = [p.read_bytes() for p in INDEX_FILES]
    if raw[0] != raw[1]:
        return False, [
            ".well-known/index.json and .well-known/agent-skills/index.json are NOT byte-identical"
        ]

    ok = True
    for skill in payloads[0].get("skills", []):
        url = skill.get("url", "")
        digest = skill.get("digest", "")
        local = URL_TO_LOCAL.get(url)

        if not local:
            errors.append(f"unknown skill URL (no local mapping): {url}")
            ok = False
            continue
        if not local.exists():
            errors.append(f"local file not found for {url}: {local.relative_to(ROOT)}")
            ok = False
            continue

        expected = "sha-256:" + sha256_file(local)
        if digest != expected:
            errors.append(
                f"digest mismatch for {url}\n"
                f"  expected : {expected}\n"
                f"  in file  : {digest}"
            )
            ok = False
        else:
            print(f"OK (index): {url}")

    return ok, errors


def check_manifest_section(data: dict, section_key: str) -> tuple[bool, list[str]]:
    """Verify sha256 fields in a manifest section (source_of_truth or supporting_evidence)."""
    errors: list[str] = []
    ok = True

    for entry in data.get(section_key, []):
        path_key = entry.get("path", "")
        recorded = entry.get("sha256", "")
        local = MANIFEST_PATH_TO_LOCAL.get(path_key)

        if not local:
            errors.append(f"aio-manifest [{section_key}]: unknown path '{path_key}' — no local mapping")
            ok = False
            continue
        if not local.exists():
            errors.append(f"aio-manifest [{section_key}]: local file not found for '{path_key}'")
            ok = False
            continue

        expected = sha256_file(local)
        if recorded != expected:
            errors.append(
                f"aio-manifest sha256 mismatch [{section_key}] for '{path_key}'\n"
                f"  expected : {expected}\n"
                f"  in file  : {recorded}"
            )
            ok = False
        else:
            print(f"OK (manifest/{section_key}): {path_key}")

    return ok, errors


def check_manifest() -> tuple[bool, list[str]]:
    """aio-manifest.json sha256 field verification for source_of_truth and supporting_evidence."""
    errors: list[str] = []

    if not MANIFEST_FILE.exists():
        return False, [f"Missing required file: {MANIFEST_FILE.relative_to(ROOT)}"]

    try:
        data = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return False, [f"JSON parse error in aio-manifest.json: {e}"]

    ok = True
    for section in ("source_of_truth", "supporting_evidence", "observational_evidence"):
        section_ok, section_errors = check_manifest_section(data, section)
        if not section_ok:
            errors.extend(section_errors)
            ok = False

    return ok, errors


def main() -> int:
    all_ok = True

    ok, errors = check_index_files()
    if not ok:
        for e in errors:
            print(f"ERROR: {e}")
        all_ok = False

    ok, errors = check_manifest()
    if not ok:
        for e in errors:
            print(f"ERROR: {e}")
        all_ok = False

    if not all_ok:
        return 1

    print("AIO digest check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
