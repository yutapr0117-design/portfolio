#!/usr/bin/env python3
"""build_private_phrase_hashes.py — 私信の本文を repo に書かず、語の連なりの hash だけを登録する。

**なぜ在るか。** 第三者との private off-list correspondence は本文を公開しない
(`LICENSES/rounds/README.md` の例外節)。それでも引用が分析の文書へ残っていた例があり、手の掃引は
mirror doc を直して元の script を見落とした (2026-11-07)。Check 492 が hash の一覧を読み、語の連なりが
tree へ戻ると RED にする。一覧から本文は読めない。

**やること**: 渡された file の 8 語の連なりの hash を一覧へ足す。公開の一次資料と今の tree に在る連なりは
足さない。steward 本人の文と公開の通知の文が RED にならないようにするためである。

使い方 (本文は repo の外に置く):
    DOSSIER_ARCHIVE_CACHE=<cache> python3 .github/scripts/build_private_phrase_hashes.py <file> [...]
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

from verify_dossier_quotations import load_sources, norm

ROOT = Path(__file__).resolve().parents[2]
HASHES = ".github/scripts/private_phrase_hashes.txt"
WIDTH = 8
TEXT = (".md", ".txt", ".json", ".html", ".js", ".yml", ".py")


def phrase_key(words: list[str]) -> str:
    return hashlib.blake2b(" ".join(words).encode("utf-8"), digest_size=6).hexdigest()


def keys_of(text: str) -> set[str]:
    words = norm(text).split()
    return {phrase_key(words[i:i + WIDTH]) for i in range(len(words) - WIDTH + 1)}


def read_hashes(root: Path) -> set[str]:
    lines = (root / HASHES).read_text(encoding="utf-8").splitlines()
    return {h for line in lines if not line.startswith("#") for h in line.split()}


def scanned_files(root: Path) -> list[str]:
    """tree のうち見る file。公開リストの逐語の保存は見ない (私信の stub は見る)。"""
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=root, check=True, text=True, capture_output=True).stdout.split("\0")
    return [f for f in tracked if f.endswith(TEXT) and f != HASHES
            and (not f.startswith("LICENSES/rounds/") or "offlist" in f)]


def tree_hits(root: Path, hashes: set[str]) -> dict[str, int]:
    """語の連なりが一覧に当たった file と件数。本文は返さない。"""
    hits = {}
    for f in scanned_files(root):
        found = keys_of((root / f).read_text(encoding="utf-8", errors="replace")) & hashes
        if found:
            hits[f] = len(found)
    return hits


def main() -> int:
    sources = [Path(p).read_text(encoding="utf-8", errors="replace") for p in sys.argv[1:]]
    if not sources:
        sys.exit(__doc__)
    new = set().union(*(keys_of(t) for t in sources))
    public = keys_of(load_sources(str(ROOT)))
    for f in scanned_files(ROOT):
        public |= keys_of((ROOT / f).read_text(encoding="utf-8", errors="replace"))
    merged = sorted(read_hashes(ROOT) | (new - public))
    head = [ln for ln in (ROOT / HASHES).read_text(encoding="utf-8").splitlines() if ln.startswith("#")]
    rows = [" ".join(merged[i:i + 8]) for i in range(0, len(merged), 8)]
    (ROOT / HASHES).write_text("\n".join(head + rows) + "\n", encoding="utf-8")
    print(f"連なり {len(new)} 件のうち公開か tree に在る {len(new & public)} 件を除き、一覧は {len(merged)} 件になった")
    return 0


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10 or later is required")
    sys.exit(main())
