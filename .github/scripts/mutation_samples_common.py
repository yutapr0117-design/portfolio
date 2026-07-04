#!/usr/bin/env python3
"""mutation_samples_common.py — 共有パス定数 (ROOT / CHECK) for mutation_samples*.py

mutation_samples.py / mutation_samples_archive.py が共通で参照する ROOT / CHECK を
単一定義する小モジュール (循環 import 回避 + 重複排除)。データもロジックも持たない。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / ".github" / "scripts" / "check_repository_consistency.py"
