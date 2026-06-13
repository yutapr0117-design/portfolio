"""
_lib_io.py — Pure I/O helpers extracted from check_repository_consistency.py

これらは Check 番号体系の外にある純関数の helper 群で、check-repository-
consistency-map.md §4 で予告された「helper-first 抽出」の第一歩。Check 45
(self-integrity) は番号付きセクションのみを対象とするため、ここに helper を
sibling file 化しても自己整合は壊さない。

設計指針:
- 純関数のみ (副作用なし)。`errors` / `warnings` への append は呼出側責務。
- `Path` ベース。文字列 path も受けるが内部で Path 化。
- 全関数は標準ライブラリのみで実装 (boring-technology 原則)。
- sibling import (`from _lib_io import ...`) で読めるよう、`.github/scripts/`
  直下に配置。sys.path 操作は不要 (Python は実行スクリプトのディレクトリを
  自動 import path に含めるため、check_repository_consistency.py からの sibling
  import が解決される)。
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def read(path: str | Path, root: Path | None = None) -> str:
    """テキストファイルを UTF-8 で読み出す。root 指定時は相対 path として resolve."""
    p = (root / path) if (root and not Path(path).is_absolute()) else Path(path)
    return p.read_text(encoding="utf-8")


def read_bytes(path: str | Path, root: Path | None = None) -> bytes:
    """バイナリファイルを読み出す。root 指定時は相対 path として resolve."""
    p = (root / path) if (root and not Path(path).is_absolute()) else Path(path)
    return p.read_bytes()


def extract(pattern: str, text: str) -> str | None:
    """text から正規表現 pattern の最初のキャプチャを返す。マッチ無しは None."""
    m = re.search(pattern, text)
    return m.group(1) if m else None


def csp_sri_hash(content: str) -> str:
    """CSP `sha256-...` directive 用の hash 文字列を生成。

    inline <script>/<style> の content から CSP nonce/hash 許可リスト用の
    `'sha256-<base64>'` 形式 (prefix 込み) で返す (元 `_csp_sri_hash` を public
    API として export — prefix 込みの方が既存呼出側の API と互換)。
    """
    import base64

    digest = hashlib.sha256(content.encode("utf-8")).digest()
    return "sha256-" + base64.b64encode(digest).decode("ascii")


def now_iso8601() -> str:
    """現在 UTC を ISO-8601 形式で返す (秒精度・末尾 Z)。

    binary metadata の derived-value 系日付フィールド (xmp:ModifyDate /
    xmp:MetadataDate / MP3 TXXX AIO:MetadataLastModified / aio-manifest.json
    last_metadata_update) の真値生成に使用する。C6 「derived value 自動更新」
    例外条項 (A 案) の中央 helper。
    """
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def update_webp_xmp_dates(path: Path, iso_now: str) -> bool:
    """WebP XMP 内の `xmp:ModifyDate` と `xmp:MetadataDate` を `iso_now` に更新する。

    両 field が無い場合は xmp: namespace ブロックに追加する。RIFF 構造を保持し、
    chunk size を再計算する。冪等 (既に同じ値なら no-op)。返り値: 変更があったか。

    7 案 (xmp:MetadataDate 追加) と B 案 (binary 編集 tool に日付更新責務) の
    共通 helper として使用する。
    """
    import re
    import struct

    data = path.read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise RuntimeError(f"{path}: not a WebP file")
    xmp_pos = data.find(b"XMP ")
    if xmp_pos < 0:
        raise RuntimeError(f"{path}: XMP chunk not found")
    xmp_size = struct.unpack("<I", data[xmp_pos + 4 : xmp_pos + 8])[0]
    xmp_payload = data[xmp_pos + 8 : xmp_pos + 8 + xmp_size]
    xmp_text = xmp_payload.decode("utf-8")

    changed = False
    # xmp:ModifyDate を update or 追加
    if "<xmp:ModifyDate>" in xmp_text:
        new_text = re.sub(
            r"<xmp:ModifyDate>[^<]*</xmp:ModifyDate>",
            f"<xmp:ModifyDate>{iso_now}</xmp:ModifyDate>",
            xmp_text,
        )
        if new_text != xmp_text:
            changed = True
            xmp_text = new_text
    else:
        # xmp namespace ブロックに追加 (存在しない場合は新規 Description block)
        if "xmlns:xmp='http://ns.adobe.com/xap/1.0/'" in xmp_text:
            xmp_text = xmp_text.replace(
                "xmlns:xmp='http://ns.adobe.com/xap/1.0/'>",
                f"xmlns:xmp='http://ns.adobe.com/xap/1.0/'>\n  <xmp:ModifyDate>{iso_now}</xmp:ModifyDate>",
                1,
            )
            changed = True

    # xmp:MetadataDate を update or 追加 (7 案)
    if "<xmp:MetadataDate>" in xmp_text:
        new_text = re.sub(
            r"<xmp:MetadataDate>[^<]*</xmp:MetadataDate>",
            f"<xmp:MetadataDate>{iso_now}</xmp:MetadataDate>",
            xmp_text,
        )
        if new_text != xmp_text:
            changed = True
            xmp_text = new_text
    else:
        if "<xmp:ModifyDate>" in xmp_text:
            xmp_text = xmp_text.replace(
                "<xmp:ModifyDate>",
                f"<xmp:MetadataDate>{iso_now}</xmp:MetadataDate>\n  <xmp:ModifyDate>",
                1,
            )
            changed = True

    if not changed:
        return False

    new_xmp_payload = xmp_text.encode("utf-8")
    new_xmp_size = len(new_xmp_payload)
    new_xmp_chunk = (
        b"XMP "
        + struct.pack("<I", new_xmp_size)
        + new_xmp_payload
        + (b"\x00" if new_xmp_size % 2 else b"")
    )
    old_padded_size = xmp_size + (xmp_size % 2)
    old_chunk_total = 8 + old_padded_size
    new_data = data[:xmp_pos] + new_xmp_chunk + data[xmp_pos + old_chunk_total :]
    new_riff_size = len(new_data) - 8
    new_data = b"RIFF" + struct.pack("<I", new_riff_size) + new_data[8:]
    path.write_bytes(new_data)
    return True


def update_mp3_metadata_date(path: Path, iso_now: str) -> bool:
    """MP3 ID3v2.4 tag に TXXX `AIO:MetadataLastModified` frame を追加 or 更新する。

    既存 frame があれば in-place 更新、無ければ tag 末尾に append。tag_size の
    synchsafe encoding を厳密に維持する。冪等。返り値: 変更があったか。
    """
    data = path.read_bytes()
    if data[:3] != b"ID3" or data[3] != 4:
        raise RuntimeError(f"{path}: not an ID3v2.4 file")
    tag_size = ((data[6] & 0x7F) << 21) | ((data[7] & 0x7F) << 14) | ((data[8] & 0x7F) << 7) | (data[9] & 0x7F)
    body = data[10 : 10 + tag_size]

    new_value = iso_now.encode("utf-8")
    desc = b"AIO:MetadataLastModified"
    encoding = b"\x03"  # UTF-8
    new_body_frame = encoding + desc + b"\x00" + new_value

    # 既存 frame を探す
    needle = b"AIO:MetadataLastModified\x00"
    idx = body.find(needle)
    if idx >= 0:
        # frame header は 10 bytes 前にある: "TXXX" + size(4) + flags(2)
        frame_header_pos = idx - 1 - 10  # encoding byte 分も戻す
        # frame header の TXXX を確認
        if body[frame_header_pos : frame_header_pos + 4] == b"TXXX":
            # 既存 frame size を読む
            old_size_bytes = body[frame_header_pos + 4 : frame_header_pos + 8]
            old_size = (
                ((old_size_bytes[0] & 0x7F) << 21)
                | ((old_size_bytes[1] & 0x7F) << 14)
                | ((old_size_bytes[2] & 0x7F) << 7)
                | (old_size_bytes[3] & 0x7F)
            )
            old_frame_total = 10 + old_size
            # 新しい frame 構築
            new_size = len(new_body_frame)
            new_size_bytes = bytes(
                [(new_size >> 21) & 0x7F, (new_size >> 14) & 0x7F, (new_size >> 7) & 0x7F, new_size & 0x7F]
            )
            new_frame = b"TXXX" + new_size_bytes + b"\x00\x00" + new_body_frame
            old_frame_data = body[frame_header_pos + 10 : frame_header_pos + 10 + old_size]
            if old_frame_data == new_body_frame:
                return False
            new_body = body[:frame_header_pos] + new_frame + body[frame_header_pos + old_frame_total :]
        else:
            return False
    else:
        # 末尾 padding (NUL) を除去して append
        stripped = body.rstrip(b"\x00")
        new_size = len(new_body_frame)
        new_size_bytes = bytes(
            [(new_size >> 21) & 0x7F, (new_size >> 14) & 0x7F, (new_size >> 7) & 0x7F, new_size & 0x7F]
        )
        new_frame = b"TXXX" + new_size_bytes + b"\x00\x00" + new_body_frame
        new_body = stripped + new_frame

    # tag_size を維持しつつ padding 調整
    target_size = max(tag_size, len(new_body) + 64)
    new_body = new_body + b"\x00" * (target_size - len(new_body))
    new_size_synchsafe = bytes(
        [(target_size >> 21) & 0x7F, (target_size >> 14) & 0x7F, (target_size >> 7) & 0x7F, target_size & 0x7F]
    )
    new_header = data[:6] + new_size_synchsafe
    new_data = new_header + new_body + data[10 + tag_size :]
    path.write_bytes(new_data)
    return True
