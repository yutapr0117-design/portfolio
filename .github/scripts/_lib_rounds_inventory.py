"""_lib_rounds_inventory.py — `LICENSES/rounds/` の在庫表 (年の帯ごとの分冊) を読み書きする共通の部品。

**なぜ在るか (2026-11-23・d7 の依頼・fc)**: 在庫表は `rounds/README.md` の「## いまの状態」に 1 枚で在り、採掘で
受領文を 1 日 20 通ほど足すので README が 803 行になり、Check 454 (危険域の未登録) に当たった。数週で Check 365
(1,000 行・BLOCKING) に届く。そこで表を年の帯ごとの分冊 `rounds/INVENTORY-<帯>.md` へ移した。表を読む・書く道具と
Check (465・add_round・add_law_snapshot・prepare_version_freeze の拒否の stub) が同じ帯の規則を持つよう、ここに 1 つだけ置く
(2 か所に持つと食い違う)。帯の境は行の数でなく年で決める (行を足しても帯が動かない)。

行の形は `| <日付> | <venue or 出所> | <相手 / 向き> | <中身> |`。日付は `YYYY`・`YYYY-MM`・`YYYY-MM-DD`・`YYYY〜YYYY` などで
始まり、先頭の 4 桁の年で帯を決める。
"""
from __future__ import annotations

import re
from pathlib import Path

# (最初の年, 最後の年, file 名)。最後の帯は終わりを持たない
BANDS = (("1999", "2012", "INVENTORY-1999-2012.md"), ("2013", "2019", "INVENTORY-2013-2019.md"),
         ("2020", "9999", "INVENTORY-2020-onward.md"))
HEADER = "| 日付 | venue | 相手 / 向き | 中身 |\n|---|---|---|---|\n"
ROW = re.compile(r"^\| (\d{4})[^|]*\|.*$", re.M)


def inventory_files(rounds: Path) -> list[Path]:
    return [rounds / name for _a, _b, name in BANDS]


def is_inventory(name: str) -> bool:
    """在庫の文書 (README と分冊) か。rounds/ の受領文の数から外す。"""
    return name == "README.md" or any(name == n for _a, _b, n in BANDS)


def band_file(rounds: Path, date: str) -> Path:
    year = date[:4]
    return next(rounds / n for a, b, n in BANDS if a <= year <= b)


def rows(text: str) -> list[str]:
    """分冊の本文から在庫表の行 (見出しと区切りを除く) を取る。"""
    return [ln for ln in text.splitlines() if ln.startswith("| ") and not ln.startswith("| 日付 |") and not ln.startswith("|---")]


def all_text(rounds: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in inventory_files(rounds) if p.exists())


def insert_row(rounds: Path, key: str, row: str, date_re: str = r"\d{4}-\d{2}(?:-\d{2})?", write: bool = True) -> tuple[Path, int]:
    """key (YYYY-MM か YYYY-MM-DD) の帯の分冊へ、日付の位置で row を差し込む。返り値は (分冊, 差し込んだ行の 1 つ前の行番号)。"""
    path = band_file(rounds, key)
    text = path.read_text(encoding="utf-8")
    found = list(re.finditer(rf"^\| ({date_re})[^|]*\|.*$", text, re.M))
    before = [r for r in found if r.group(1) <= key]
    if before:
        at = max(before, key=lambda r: r.group(1)).end()
    elif found:
        at = found[0].start() - 1
    else:
        at = text.index(HEADER) + len(HEADER) - 1
    if write:
        path.write_text(text[:at] + "\n" + row + text[at:], encoding="utf-8")
    return path, text[:at].count("\n") + 1
