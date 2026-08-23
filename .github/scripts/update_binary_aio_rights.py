#!/usr/bin/env python3
"""
update_binary_aio_rights.py — one-shot tool

binary AIO layer (WebP XMP / MP3 ID3v2.4) の**権利表示**を ACD-1.0 へ揃え、あわせて
MP3 の malformed な COMM frame を修復する。

実行: python3 .github/scripts/update_binary_aio_rights.py

## なぜ必要か

1. **権利表示の面ごとの食い違い (C6)**
   2026-08-23 に LICENSE を独自ライセンス ACD-1.0 (権利留保ゼロ) へ移行したが、
   binary 内の権利表示は `All rights reserved` のままだった。XMP/ID3 を読む機械は
   **公開層から矛盾した権利情報を受け取る**。C6 が守るのは「面ごとに食い違わせない」ことなので、
   これは是正対象。

2. **🔴 MP3 の malformed COMM frame により 5 frame が到達不能だった**
   `COMM` frame (offset 6540) の size 欄が **実データより 3 バイト大きい** (宣言 2396 / 実体 2393)。
   ID3v2.4 の frame は連結されているので、size が実体とずれると **以降の walk が破綻する**。
   実測: 厳密な reader は offset 8946 で不正な frame id `b'X\\x00\\x00\\x00'` を読んで停止し、
   **それ以降の 5 frame が一切読めなかった**:

       TXXX:AIO:Organization
       TXXX:AIO:OrganizationURL
       TXXX:AIO:OrganizationRole
       TXXX:AIO:OrganizationStartDate
       TXXX:AIO:MetadataLastModified   ← Check 91 が存在と同期を BLOCKING 強制している当の field

   つまり PR #49 で入れた「Organization 情報を cross-surface に反映」は、**MP3 面では一度も
   標準リーダーに届いていなかった**。さらに Check 91 は「必ず存在せよ」と機械強制しているのに、
   その field は誰にも読めない位置にあった —— #929 (WebMCP の幻セレクタ) / #930 (route 追従
   JSON-LD) と同じ「**宣言はあるが実態が伴わない**」class の binary 面。

## 設計 — オフセットを動かさない

malformed な frame があるので、**frame を parse して tag を組み直す方式は使わない**
(組み直すと壊れた COMM のデータを落とすか、さらに破損させる)。本 tool の 2 つの編集は
どちらも **byte 長を変えない in-place 編集**で、file size もその他すべての frame の
offset も変わらない:

  - COMM size 欄 (4 bytes) を synchsafe(2393) へ書き換える
  - TCOP のテキストを **同一バイト長 (52 bytes)** の新しい文言へ置き換える

WebP 側は XMP が text なので、既存 `update_binary_aio_organization.py` と同じく
RIFF chunk を再計算して置換する (この経路は Check 337 が検証済)。

## 冪等

いずれも「既に適用済みなら何もしない」。日付フィールドは C6 の A1 派生値例外に従い
`_lib_io` の helper で同期する (Check 91 が同一 commit での同期を機械強制)。
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _lib_io import now_iso8601, update_webp_xmp_dates, update_mp3_metadata_date  # noqa: E402

WEBP = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
MP3 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"

# 権利表示の新しい文言。ACD-1.0 は権利を留保しないので "All rights reserved" は事実に反する。
OLD_RIGHTS_WEBP = ("Copyright (C) 2026 Yuta Yokoi (横井雄太). All rights reserved. "
                   "Canonical: https://yutapr0117-design.github.io/portfolio/")
NEW_RIGHTS_WEBP = ("2026 Yuta Yokoi (横井雄太). Released under the Autonomous Commons Dedication 1.0 "
                   "(ACD-1.0): no rights reserved, no conditions imposed, machine learning expressly "
                   "permitted. Canonical: https://yutapr0117-design.github.io/portfolio/")

# MP3 TCOP は **同一バイト長 (52) ** でなければならない (offset を動かさないため)。
OLD_TCOP = "2026 Yuta Yokoi (横井雄太). All rights reserved."
NEW_TCOP = "2026 Yuta Yokoi (横井雄太). ACD-1.0 (no rights)."


def _synchsafe(n: int) -> bytes:
    return bytes([(n >> 21) & 0x7F, (n >> 14) & 0x7F, (n >> 7) & 0x7F, n & 0x7F])


def _read_synchsafe(b: bytes) -> int:
    return ((b[0] & 0x7F) << 21) | ((b[1] & 0x7F) << 14) | ((b[2] & 0x7F) << 7) | (b[3] & 0x7F)


def readable_frame_count(data: bytes) -> int:
    """厳密な ID3 reader が読める frame 数。malformed frame で停止する挙動を再現する。"""
    end = 10 + _read_synchsafe(data[6:10])
    pos, n = 10, 0
    while pos + 10 <= end:
        fid = data[pos:pos + 4]
        if fid[:1] == b"\x00":
            break
        if not all(48 <= c <= 57 or 65 <= c <= 90 for c in fid):
            break
        n += 1
        pos += 10 + _read_synchsafe(data[pos + 4:pos + 8])
    return n


def repair_malformed_frame(path: Path) -> bool:
    """walk を破綻させている frame の size 欄を実データ長へ直す (4 bytes の in-place 編集)。

    **frame 種別で探してはならない** —— この file には COMM が 5 個あり、malformed なのは
    最後の 1 つだけ。初版は `data.find(b"COMM")` で先頭の COMM を掴み、たまたま
    「size は実データと一致」と報告して**修復を行わずに成功したふりをした**。
    正しくは **walk が実際に破綻する位置**から犯人を特定する。
    """
    data = bytearray(path.read_bytes())
    end = 10 + _read_synchsafe(bytes(data[6:10]))
    pos, prev = 10, None
    while pos + 10 <= end:
        fid = bytes(data[pos:pos + 4])
        if fid[:1] == b"\x00":
            print("MP3: walk は padding まで到達 — malformed frame なし (skip)")
            return False
        if not all(48 <= c <= 57 or 65 <= c <= 90 for c in fid):
            break
        prev = (fid.decode(), pos, _read_synchsafe(bytes(data[pos + 4:pos + 8])))
        pos += 10 + prev[2]
    else:
        print("MP3: walk は tag 末尾まで到達 — malformed frame なし (skip)")
        return False
    if prev is None:
        raise RuntimeError("MP3: 先頭 frame から不正 — 手動調査が必要")

    name, fpos, declared = prev
    # 真の終端 = 破綻位置の前後で最初に valid な frame id が始まる位置
    true_end = None
    for cand in range(pos - 8, min(pos + 9, end - 4)):
        fid = bytes(data[cand:cand + 4])
        if cand > fpos + 10 and all(48 <= c <= 57 or 65 <= c <= 90 for c in fid):
            true_end = cand
            break
    if true_end is None:
        raise RuntimeError(f"MP3: {name}@{fpos} の真の終端を特定できない — 手動調査が必要")
    true_size = true_end - (fpos + 10)
    if declared == true_size:
        print("MP3: size は既に実データと一致 — skip")
        return False
    comm = fpos
    before = readable_frame_count(bytes(data))
    data[comm + 4:comm + 8] = _synchsafe(true_size)
    after = readable_frame_count(bytes(data))
    if after <= before:
        raise RuntimeError(f"MP3: 修復したのに読める frame が増えていない ({before} -> {after}) — 中断")
    path.write_bytes(bytes(data))
    print(f"MP3 {name}@{fpos}: size {declared} -> {true_size} (実データ長へ是正)。"
          f"読める frame {before} -> {after}。file size 不変")
    return True


def update_mp3_tcop(path: Path) -> bool:
    """TCOP のテキストを同一バイト長で置換する。長さが変わる場合は中断する。"""
    data = bytearray(path.read_bytes())
    old, new = OLD_TCOP.encode("utf-8"), NEW_TCOP.encode("utf-8")
    if len(old) != len(new):
        raise RuntimeError(f"TCOP: byte 長が違う (old={len(old)} new={len(new)}) — "
                           f"offset を動かさない前提が崩れるので中断")
    i = data.find(old)
    if i < 0:
        if data.find(new) >= 0:
            print("MP3 TCOP: 既に ACD-1.0 表記 — skip")
            return False
        raise RuntimeError("TCOP: 想定した旧文言が見つからない")
    size_before = len(data)
    data[i:i + len(old)] = new
    assert len(data) == size_before, "file size が変わった"
    path.write_bytes(bytes(data))
    print(f"MP3 TCOP: 権利表示を ACD-1.0 へ ({len(new)} bytes 同長置換)。file size 不変")
    return True


def update_webp_rights(path: Path) -> bool:
    """WebP XMP の dc:rights を書き換える (RIFF chunk を再計算)。"""
    data = path.read_bytes()
    assert data[:4] == b"RIFF" and data[8:12] == b"WEBP", "not a WebP file"
    xmp_pos = data.find(b"XMP ")
    if xmp_pos < 0:
        raise RuntimeError("XMP chunk not found")
    xmp_size = struct.unpack("<I", data[xmp_pos + 4:xmp_pos + 8])[0]
    xmp_text = data[xmp_pos + 8:xmp_pos + 8 + xmp_size].decode("utf-8")

    if NEW_RIGHTS_WEBP in xmp_text:
        print("WebP dc:rights: 既に ACD-1.0 表記 — skip")
        return False
    if OLD_RIGHTS_WEBP not in xmp_text:
        raise RuntimeError("WebP dc:rights: 想定した旧文言が見つからない")

    new_text = xmp_text.replace(OLD_RIGHTS_WEBP, NEW_RIGHTS_WEBP, 1)
    payload = new_text.encode("utf-8")
    chunk = b"XMP " + struct.pack("<I", len(payload)) + payload + (b"\x00" if len(payload) % 2 else b"")
    old_total = 8 + xmp_size + (xmp_size % 2)
    new_data = data[:xmp_pos] + chunk + data[xmp_pos + old_total:]
    new_data = b"RIFF" + struct.pack("<I", len(new_data) - 8) + new_data[8:]
    path.write_bytes(new_data)
    print(f"WebP dc:rights: 権利表示を ACD-1.0 へ ({len(data)} -> {len(new_data)} bytes)")
    return True


def main() -> int:
    changed = False
    changed |= repair_malformed_frame(MP3)
    changed |= update_mp3_tcop(MP3)
    changed |= update_webp_rights(WEBP)

    if changed:
        # C6 A1 派生値: semantic 編集に伴う日付フィールドを同一 commit で同期する (Check 91)
        iso = now_iso8601()
        update_webp_xmp_dates(WEBP, iso)
        update_mp3_metadata_date(MP3, iso)
        print(f"derived dates synced to {iso}")
        print("\n次に `python3 .github/scripts/update_aio_digests.py` を実行して digest を再生成すること")
    else:
        print("変更なし (冪等)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
