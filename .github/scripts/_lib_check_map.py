"""_lib_check_map.py — Check の地図 (check-repository-consistency-map.md) の file の一覧と、全 file の本文。

**なぜ在るか (2026-11-16・9b)**: 地図は 393 KB でバイトの advisory (380 KB・Check 495) を越え、上限 (500 KB) へ近づいている。
大半は Check の行の表 (371 KB) で、散文の節を移しても足りないので、いつか行を 2 つ目の file へ分ける。その日に行を読む Check
(64 の番号の一意・105 の地図と実装の一対一・478 の所在の列) が 2 つ目を黙って見落とさないよう、file の一覧をここだけに置く
(against.md を分けたときの AGAINST_FILES と同じ形)。**分けた日は CHECK_MAP_FILES に 2 つ目を足す**。

**分ける日の予行 (2026-11-16)**: 使い捨ての worktree でカテゴリ F の表を `check-repository-consistency-map-2.md` へ移し、一覧に
足して consistency を回すと、64・105・478 は緑のまま (2 つ目を読む) で、RED は新しい file に付きものの 2 つだけだった ——
(1) docs/files の mirror (108)、(2) 行数の表 (424・`npm run sync-sizes`)。ほかに、`.github/scripts/checks_canon_config.py` の
Check 109 の生きた文書の一覧と BYTE-BUDGET-DATA に 2 つ目の行を足す。動かした行に anchor を持つ mutation の "file" も付け替える。
"""
from pathlib import Path

CHECK_MAP_FILES = ("docs/architecture/check-repository-consistency-map.md",)


def check_map_paths(root: Path) -> list[Path]:
    """地図の file を順に (在るものだけ)。"""
    return [root / f for f in CHECK_MAP_FILES if (root / f).exists()]


def check_map_text(root: Path) -> str:
    """地図の全 file の本文をつないだもの (無ければ空)。"""
    return "\n".join(p.read_text(encoding="utf-8") for p in check_map_paths(root))
