#!/usr/bin/env python3
"""file-size-budget.md §2 の「実測行数」列のうち、Check 424 が赤くする行だけを実測へ直す。

    npm run sync-sizes

この列は行が隣り合うので、別の file を直した PR どうしが git の上で衝突する (2026-11-06 に 1 日 3 回)。
`LICENSES/` の文書は 3 セッションが毎日書くので ±50 行の幅を許し、幅の中ではこの列に触らない。
上限の判定は Check 52 / 365 が実物の行数で行うので、この幅は上限を緩めない。
衝突したら main の表を取り直してから回す: `git checkout origin/main -- docs/architecture/file-size-budget.md`
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit("sync_size_table.py requires Python 3.10+ (Check 104)")

ROOT = Path(__file__).resolve().parents[2]
TABLE = ROOT / "docs" / "architecture" / "file-size-budget.md"
ROW = re.compile(r"^(\|\s*`([^`]+)`\s*\|\s*)([\d,]+)(\s*\|)", re.M)


def allowed_drift(path: str) -> int:
    """表の値と実測の差として許す行数。Check 424 と共有する単一の定義。"""
    return 50 if path.startswith("LICENSES/") else 0


def measured(path: Path) -> int:
    return len(path.read_text(encoding="utf-8", errors="replace").split("\n")) - 1


def main() -> int:
    def fix(m: re.Match) -> str:
        p = ROOT / m.group(2)
        if not p.exists():
            return m.group(0)
        rec, real = int(m.group(3).replace(",", "")), measured(p)
        if abs(rec - real) <= allowed_drift(m.group(2)):
            return m.group(0)
        print(f"{m.group(2)}: {rec} -> {real}")
        return f"{m.group(1)}{real}{m.group(4)}"

    src = TABLE.read_text(encoding="utf-8")
    TABLE.write_text(ROW.sub(fix, src), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
