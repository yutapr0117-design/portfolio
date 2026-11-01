#!/usr/bin/env python3
"""mutation_samples_common.py — 共有パス定数 (ROOT / CHECK) for mutation_samples*.py

mutation_samples.py / mutation_samples_archive.py が共通で参照する ROOT / CHECK を
単一定義する小モジュール (循環 import 回避 + 重複排除)。データもロジックも持たない。
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / ".github" / "scripts" / "check_repository_consistency.py"

# 作業中の草案 (pointer でない ACD-*-DRAFT.txt がちょうど 1 つ)。Check 468 と同じ規則で導出する。
# 版番号を決め打ちした mutation は、版を確定した日に的を外す (2026-10-26 の週次 probe で 468i が
# SURVIVED)。草案を指す mutation はこの 3 つから組み立てる。定まらなければ存在しない名前になり、
# Check 362 (anchor 解決) が RED にする。
def _current_draft():
    cands = [p for p in sorted((ROOT / "LICENSES").glob("ACD-*-DRAFT.txt"))
             if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]]
    return cands[0] if len(cands) == 1 else ROOT / "LICENSES" / "ACD-UNRESOLVED-DRAFT.txt"


CURRENT_DRAFT = _current_draft()
_m = re.match(r"ACD-(\d+)\.(\d+)-DRAFT\.txt$", CURRENT_DRAFT.name)
CURRENT_DRAFT_VER = f"{_m.group(1)}.{_m.group(2)}" if _m else "0.0"
PREVIOUS_VER = f"{_m.group(1)}.{int(_m.group(2)) - 1}" if _m and int(_m.group(2)) > 0 else "0.0"
