---
file: .github/scripts/_lib_rounds_inventory.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-23
canonical-ref: LICENSES/rounds/README.md (在庫の入口) / LICENSES/rounds/INVENTORY-*.md (分冊)
---

# .github/scripts/_lib_rounds_inventory.py

## What

`LICENSES/rounds/` の在庫表（年の帯ごとの分冊 `INVENTORY-1999-2012.md` / `INVENTORY-2013-2019.md` / `INVENTORY-2020-onward.md`）を読み書きする小さな module。

- `BANDS` —— (最初の年, 最後の年, file 名)。帯は年で決まる。
- `inventory_files(rounds)` / `is_inventory(name)` / `band_file(rounds, date)` —— 分冊の一覧、在庫の文書か、日付の帯の分冊。
- `rows(text)` / `all_text(rounds)` —— 表の行、全分冊の本文。
- `insert_row(rounds, key, row, date_re, write)` —— 日付の位置へ 1 行差し込む。

## Why

2026-11-23 に在庫表を README から年の帯の分冊へ移した（README が 803 行）。表を読む・書く 4 か所（Check 465・`add_round.py`・`add_law_snapshot.py`・`prepare_version_freeze.py` の拒否の stub）が同じ帯の規則を持つよう、1 か所だけに置く。

## How (usage)

```python
from _lib_rounds_inventory import insert_row
insert_row(ROUNDS, "2008-03", "| 2008-03 | `license-review` | … | `….txt` |", date_re=r"\d{4}-\d{2}")
```

## Constraints

帯の規則はここにだけ書く（Check 465 と 3 つの道具が読む）。帯の境は行の数でなく年で決める。

## Change impact

帯を変えるときは分冊の行を移し、Check 465 の帯の外の行の照合が緑になることを確かめる。

## Audience-specific notes

- **実装者**: 新しい帯を足すときは `BANDS` の最後の帯を閉じ、新しい分冊と mirror と LICENSES/README.md の索引の行を足す。
