"""_lib_dossier.py — ドシエの不利な事実の register (against) を読む場所を 1 か所にする。

against.md はバイトの予算 (Check 495) に近づいており、BLOCKING の手前で #N の番号を続けたまま 2 つ目の file へ分ける
(portfolio-00 と portfolio-9b の合意・2026-11-12)。その日に読み手を何か所も直さずに済むよう、file の一覧をここだけに置く。
分けた日は AGAINST_FILES に 2 つ目の file 名を足す (番号の範囲は file の順)。
"""
from pathlib import Path

AGAINST_FILES = ("ACD-1.0.against.md",)


def against_paths(licenses_dir: Path) -> list[Path]:
    """register の file を順に (在るものだけ)。"""
    return [licenses_dir / n for n in AGAINST_FILES if (licenses_dir / n).exists()]


def against_text(licenses_dir: Path) -> str:
    """register の全 file の本文をつないだもの (無ければ空)。"""
    return "\n".join(p.read_text(encoding="utf-8") for p in against_paths(licenses_dir))


def is_against(name: str) -> bool:
    """file 名が register の file か。"""
    return name in AGAINST_FILES
