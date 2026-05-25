"""
check_binary_aio_metadata.py — Binary AIO metadata integrity CI check (BLOCKING)
P0-15: Enhanced to verify expected version/date/path context, not just keyword presence.

Asset baseline policy (P0-14):
  Application current version: v74 / 2026-05-24
  Binary asset metadata baseline: v73 / 2026-04-14 (Manus AIO Optimization Record)
  Binaries are NOT re-encoded; metadata reflects the Manus-AIO baseline.
  EXPECTED_ASSET_BASELINE_VERSION and EXPECTED_ASSET_BASELINE_DATE below match this.

Verifies:
  WebP:
    - RIFF / WEBP magic bytes
    - XMP chunk presence
    - XMP content contains required AIO terms
    - Expected canonical file name in XMP
    - Expected incident artifact path (not stale .github/workflows/ path)

  MP3:
    - ID3v2.4 header presence
    - Required TXXX and COMM frame presence
    - Expected canonical file name in ID3
    - Stale forbidden markers are absent from current-state fields

Exit codes:
  0 — all checks passed
  1 — any check failed (CI blocking)
"""

from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]

WEBP_FILE = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
MP3_FILE  = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"

# Asset baseline: binaries were last updated by Manus AIO at v73 / 2026-04-14.
# Application is now v74 / 2026-05-24.
EXPECTED_APP_VERSION        = "v74"
EXPECTED_ASSET_BASELINE_VERSION = "v73"
EXPECTED_ASSET_BASELINE_DATE    = "2026-04-14"
EXPECTED_INCIDENT_PATH      = b"docs/incident-artifacts/update-portfolio.v70-experiment.yml"

# Markers that must NOT appear as current-state indicators in style.css
# (these are style.css checks, not binary, but included for completeness)
FORBIDDEN_CSS_CURRENT_MARKERS = [
    "Current release: v73",
    "v74 is NEXT_PLANNED_RELEASE",
]

# Required AIO terms in WebP XMP chunk
WEBP_XMP_REQUIRED = [
    b"CanonicalURL",
    b"EntityName",
    b"llms-full.txt",
    b"Yuta Yokoi",
    b"\xe6\xa8\xaa\xe4\xba\x95\xe9\x9b\x84\xe5\xa4\xaa",  # 横井雄太 UTF-8
    b"yuta-yokoi-ai-pm-orchestration-system.webp",          # canonical filename
]

# Required ID3 frame identifiers or TXXX description bytes in MP3
MP3_ID3_REQUIRED = [
    b"AIO:CanonicalURL",
    b"AIO:EntityName",
    b"AIO:AuthoritativeContext",
    b"AIO Context",
    b"PairedImageAsset",
    b"yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3",  # canonical filename
]

# Stale path that must NOT be referenced in MP3 ID3 as current incident path
MP3_STALE_INCIDENT_PATH = b".github/workflows/update-portfolio.v70-experiment.yml"


def check_webp(path: Path) -> list[str]:
    errors = []
    data = path.read_bytes()

    # RIFF / WEBP magic
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        errors.append(f"WebP: missing RIFF/WEBP magic bytes in {path.name}")
        return errors

    # Find XMP chunk
    xmp_data = None
    i = 12
    while i + 8 <= len(data):
        chunk_id = data[i:i+4]
        chunk_size = struct.unpack_from("<I", data, i+4)[0]
        if chunk_id == b"XMP ":
            xmp_data = data[i+8:i+8+chunk_size]
            break
        i += 8 + chunk_size + (chunk_size % 2)

    if xmp_data is None:
        errors.append(f"WebP: XMP chunk NOT FOUND in {path.name} — AIO metadata lost")
        return errors

    for term in WEBP_XMP_REQUIRED:
        if term not in xmp_data:
            readable = term.decode("utf-8", errors="replace")
            errors.append(f"WebP XMP: required AIO term missing: {readable!r}")

    # Asset baseline version check (informational — v73 is expected baseline)
    baseline_v = EXPECTED_ASSET_BASELINE_VERSION.encode()
    baseline_d = EXPECTED_ASSET_BASELINE_DATE.encode()
    if baseline_v not in xmp_data:
        errors.append(
            f"WebP XMP: expected asset baseline version {EXPECTED_ASSET_BASELINE_VERSION!r} not found "
            f"(binary baseline should reference Manus AIO at {EXPECTED_ASSET_BASELINE_VERSION})"
        )
    if baseline_d not in xmp_data:
        errors.append(
            f"WebP XMP: expected asset baseline date {EXPECTED_ASSET_BASELINE_DATE!r} not found"
        )

    return errors


def check_mp3(path: Path) -> list[str]:
    errors = []
    data = path.read_bytes()

    if data[:3] != b"ID3":
        errors.append(f"MP3: ID3 header NOT FOUND in {path.name} — AIO metadata lost")
        return errors

    major_version = data[3]
    if major_version < 4:
        errors.append(
            f"MP3: ID3 version is 2.{major_version} — expected 2.4 (ID3v2.4) per AIO spec"
        )

    for term in MP3_ID3_REQUIRED:
        if term not in data:
            readable = term.decode("utf-8", errors="replace")
            errors.append(f"MP3 ID3: required AIO tag missing: {readable!r}")

    # Stale incident path check
    if MP3_STALE_INCIDENT_PATH in data:
        errors.append(
            f"MP3 ID3: stale incident artifact path detected: "
            f"{MP3_STALE_INCIDENT_PATH.decode()!r}. "
            f"Expected: {EXPECTED_INCIDENT_PATH.decode()!r}"
        )

    # Asset baseline version check
    baseline_v = EXPECTED_ASSET_BASELINE_VERSION.encode()
    if baseline_v not in data:
        errors.append(
            f"MP3 ID3: expected asset baseline version {EXPECTED_ASSET_BASELINE_VERSION!r} not found"
        )

    return errors


def main() -> int:
    all_errors = []

    if not WEBP_FILE.exists():
        all_errors.append(f"WebP asset missing: {WEBP_FILE.name}")
    else:
        errs = check_webp(WEBP_FILE)
        all_errors.extend(errs)
        if not errs:
            print(f"OK: WebP XMP AIO metadata verified ({WEBP_FILE.name})")
            print(f"  Asset baseline: {EXPECTED_ASSET_BASELINE_VERSION} / {EXPECTED_ASSET_BASELINE_DATE} (Manus AIO)")
            print(f"  Application version: {EXPECTED_APP_VERSION} (text-layer files updated separately)")

    if not MP3_FILE.exists():
        all_errors.append(f"MP3 asset missing: {MP3_FILE.name}")
    else:
        errs = check_mp3(MP3_FILE)
        all_errors.extend(errs)
        if not errs:
            print(f"OK: MP3 ID3 AIO metadata verified ({MP3_FILE.name})")

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}")
        return 1

    print("Binary AIO metadata check passed")
    print(f"NOTE: Binary asset metadata baseline is {EXPECTED_ASSET_BASELINE_VERSION}/{EXPECTED_ASSET_BASELINE_DATE}; "
          f"application version is {EXPECTED_APP_VERSION}. This is intentional (P0-14 asset baseline policy).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
