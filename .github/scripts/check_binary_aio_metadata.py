"""
check_binary_aio_metadata.py — Binary AIO metadata integrity CI check (BLOCKING)

Verifies that AIO-critical metadata is present in binary assets:

WebP:
  - RIFF / WEBP magic bytes
  - XMP chunk presence
  - XMP content contains required AIO terms

MP3:
  - ID3v2.4 header presence
  - Required TXXX and COMM frame presence (detected via raw byte search)

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

# Required AIO terms in WebP XMP chunk
WEBP_XMP_REQUIRED = [
    b"CanonicalURL",
    b"EntityName",
    b"llms-full.txt",
    b"Yuta Yokoi",
    b"\xe6\xa8\xaa\xe4\xba\x95\xe9\x9b\x84\xe5\xa4\xaa",  # 横井雄太 UTF-8
]

# Required ID3 frame identifiers or TXXX description bytes in MP3
MP3_ID3_REQUIRED = [
    b"AIO:CanonicalURL",
    b"AIO:EntityName",
    b"AIO:AuthoritativeContext",
    b"AIO Context",
    b"PairedImageAsset",
]


def check_webp(path: Path) -> list[str]:
    errors = []
    data = path.read_bytes()

    # RIFF / WEBP magic
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        errors.append(f"WebP: missing RIFF/WEBP magic bytes in {path.name}")
        return errors  # Cannot proceed without valid container

    # Find XMP chunk
    xmp_data = None
    i = 12
    while i + 8 <= len(data):
        chunk_id = data[i:i+4]
        chunk_size = struct.unpack_from("<I", data, i+4)[0]
        if chunk_id == b"XMP ":
            xmp_data = data[i+8:i+8+chunk_size]
            break
        # Chunks are padded to even byte boundaries
        i += 8 + chunk_size + (chunk_size % 2)

    if xmp_data is None:
        errors.append(f"WebP: XMP chunk NOT FOUND in {path.name} — AIO metadata lost")
        return errors

    for term in WEBP_XMP_REQUIRED:
        if term not in xmp_data:
            readable = term.decode("utf-8", errors="replace")
            errors.append(f"WebP XMP: required AIO term missing: {readable!r}")

    return errors


def check_mp3(path: Path) -> list[str]:
    errors = []
    data = path.read_bytes()

    # ID3 header: "ID3" + major version byte (>= 4 for v2.4)
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
