#!/usr/bin/env python3
"""
update_binary_aio_organization.py — one-shot tool

WebP XMP と MP3 ID3v2.4 に「株式会社日本経営」Organization 情報を追加する。
既存 JSON-LD / llms.txt / aio-manifest.json と整合する形で、binary AIO layer に
散在欠落していた所属組織情報を補完する。

実行: python3 .github/scripts/update_binary_aio_organization.py

設計:
- WebP: 既存 RIFF 構造を保持しつつ 'XMP ' chunk の payload を rewrite。
  既存の <rdf:Description xmlns:aio='...'> ブロックに Organization* field を追加。
- MP3:  既存 ID3v2.4 tag を読み、TXXX frame を 4 件追加 (Organization name/URL/Role/StartDate)。
  既存 TXXX:AIO:* との命名整合性を保つ。
- 冪等: 既に追加済みなら再追加しない。
- ID3 synchsafe encoding を厳密に維持。
"""

from __future__ import annotations

import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

WEBP = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
MP3 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"

ORG_NAME_JA = "株式会社日本経営"
ORG_NAME_EN = "Nihon Keiei / Japan Management Co., Ltd."
ORG_URL = "https://nkgr.co.jp/"
ORG_ROLE = "シェアデータベース事業部 主幹（課長格）"
ORG_START = "2026-06-11"


# ── WebP XMP rewriter ──────────────────────────────────────────────────────────

def update_webp(path: Path) -> bool:
    data = path.read_bytes()
    assert data[:4] == b"RIFF" and data[8:12] == b"WEBP", "not a WebP file"

    # XMP chunk locate
    xmp_pos = data.find(b"XMP ")
    if xmp_pos < 0:
        raise RuntimeError("XMP chunk not found")
    xmp_size = struct.unpack("<I", data[xmp_pos + 4 : xmp_pos + 8])[0]
    xmp_payload = data[xmp_pos + 8 : xmp_pos + 8 + xmp_size]
    xmp_text = xmp_payload.decode("utf-8")

    # 冪等チェック
    if "aio:OrganizationName" in xmp_text and ORG_NAME_JA in xmp_text:
        print("WebP XMP: Organization fields already present — skipping")
        return False

    # 既存 aio: namespace ブロックを発見し、その閉じ </rdf:Description> の直前へ追記する
    aio_block_start = xmp_text.find("xmlns:aio='https://yutapr0117-design.github.io/portfolio/aio-schema/1.0/'")
    if aio_block_start < 0:
        raise RuntimeError("aio namespace block not found in XMP")
    # この Description の閉じタグを探す
    desc_close = xmp_text.find("</rdf:Description>", aio_block_start)
    if desc_close < 0:
        raise RuntimeError("</rdf:Description> not found after aio: namespace block")

    # 挿入する Organization fields
    new_fields = (
        f"  <aio:OrganizationName>{ORG_NAME_JA} ({ORG_NAME_EN})</aio:OrganizationName>\n"
        f"  <aio:OrganizationURL>{ORG_URL}</aio:OrganizationURL>\n"
        f"  <aio:OrganizationRole>{ORG_ROLE}</aio:OrganizationRole>\n"
        f"  <aio:OrganizationStartDate>{ORG_START}</aio:OrganizationStartDate>\n "
    )

    new_xmp_text = xmp_text[:desc_close] + new_fields + xmp_text[desc_close:]
    new_xmp_payload = new_xmp_text.encode("utf-8")

    # padding 末尾の whitespace 領域 (元 XMP には拡張余白がある) を活用するため、
    # 長さを既存と同じ payload size に近づける必要はない (RIFF chunk size を再計算するため可変)。
    # WebP RIFF は chunk size を 4-byte LE で持つ。chunk が odd-size の場合 1 byte の padding。
    new_xmp_size = len(new_xmp_payload)
    new_xmp_chunk = (
        b"XMP "
        + struct.pack("<I", new_xmp_size)
        + new_xmp_payload
        + (b"\x00" if new_xmp_size % 2 else b"")
    )

    # 既存 XMP chunk の terminator (padding) も考慮した置換
    old_padded_size = xmp_size + (xmp_size % 2)
    old_chunk_total = 8 + old_padded_size  # header (8) + payload + padding

    new_data = data[:xmp_pos] + new_xmp_chunk + data[xmp_pos + old_chunk_total :]

    # RIFF top-level size を更新
    new_riff_size = len(new_data) - 8
    new_data = b"RIFF" + struct.pack("<I", new_riff_size) + new_data[8:]

    path.write_bytes(new_data)
    print(f"WebP XMP: updated — size {len(data)} -> {len(new_data)} bytes")
    return True


# ── MP3 ID3v2.4 TXXX rewriter ──────────────────────────────────────────────────

def _synchsafe(n: int) -> bytes:
    """4-byte synchsafe (7-bit per byte) integer encoding."""
    return bytes([(n >> 21) & 0x7F, (n >> 14) & 0x7F, (n >> 7) & 0x7F, n & 0x7F])


def _read_synchsafe(b: bytes) -> int:
    return ((b[0] & 0x7F) << 21) | ((b[1] & 0x7F) << 14) | ((b[2] & 0x7F) << 7) | (b[3] & 0x7F)


def _txxx_frame(description: str, value: str) -> bytes:
    """ID3v2.4 TXXX frame: 1-byte encoding + description \\x00 + value."""
    encoding = b"\x03"  # UTF-8
    body = encoding + description.encode("utf-8") + b"\x00" + value.encode("utf-8")
    header = b"TXXX" + _synchsafe(len(body)) + b"\x00\x00"  # flags 2 bytes
    return header + body


def update_mp3(path: Path) -> bool:
    data = path.read_bytes()
    assert data[:3] == b"ID3" and data[3] == 4, "not an ID3v2.4 file"

    tag_size = _read_synchsafe(data[6:10])
    tag_end = 10 + tag_size  # exclusive
    body = data[10:tag_end]

    # 冪等チェック (TXXX:AIO:Organization が既に存在するか)
    if b"AIO:Organization" in body:
        print("MP3 ID3: AIO:Organization TXXX already present — skipping")
        return False

    new_frames = (
        _txxx_frame("AIO:Organization", f"{ORG_NAME_JA} ({ORG_NAME_EN})")
        + _txxx_frame("AIO:OrganizationURL", ORG_URL)
        + _txxx_frame("AIO:OrganizationRole", ORG_ROLE)
        + _txxx_frame("AIO:OrganizationStartDate", ORG_START)
    )

    # 既存 body の末尾 padding (NUL bytes) を取り除いてから新 frame を append、
    # その後、適切な padding を確保する。
    stripped = body.rstrip(b"\x00")
    new_body = stripped + new_frames
    # ID3v2.4 tag size は frame total。padding は任意。元と同サイズ以上に維持し
    # MPEG frame の位置をずらさないため、既存 tag_size + 追加分でサイズ拡張する。
    target_size = max(tag_size, len(new_body) + 256)  # 256 byte 余裕
    new_body = new_body + b"\x00" * (target_size - len(new_body))

    new_header = data[:6] + _synchsafe(target_size)
    new_data = new_header + new_body + data[tag_end:]

    path.write_bytes(new_data)
    print(f"MP3 ID3: updated — tag_size {tag_size} -> {target_size}, file {len(data)} -> {len(new_data)} bytes")
    return True


if __name__ == "__main__":
    print("== WebP XMP ==")
    update_webp(WEBP)
    print("== MP3 ID3 ==")
    update_mp3(MP3)
    print()
    print("Done. Next steps:")
    print("  1. python3 .github/scripts/update_aio_digests.py  # sha256 連鎖更新")
    print("  2. python3 .github/scripts/check_aio_digests.py    # 検証")
    print("  3. python3 .github/scripts/check_binary_aio_metadata.py")
