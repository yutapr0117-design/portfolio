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
