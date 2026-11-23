---
file: LICENSES/rounds/INVENTORY-1999-2012.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-23
canonical-ref: LICENSES/rounds/README.md (置き方の規約と分冊の一覧) / .github/scripts/_lib_rounds_inventory.py (帯の規則)
---

# LICENSES/rounds/INVENTORY-1999-2012.md

## What

`LICENSES/rounds/` に置いた受領文・観測・スナップショットの在庫表のうち、日付が 1999〜2012 年の行。列は日付・venue（出所）・相手 / 向き・中身（file 名）。

## Why

在庫表は `rounds/README.md` の「いまの状態」に 1 枚で在り、採掘で 1 日 20 通ほど増えるので 2026-11-23 に 803 行になった（Check 454・数週で Check 365 の 1,000 行）。年の帯で分けたので、行を足しても帯は動かない。

## How (usage)

`add_round.py` と `add_law_snapshot.py` が日付の位置へ行を差し込む（`_lib_rounds_inventory.insert_row`）。手で足すときも日付の帯の分冊へ置く。

## Constraints

行は日付の帯の分冊にだけ置く（帯の外の行は Check 465 が RED にする）。受領文の本文はここに書かない（`rounds/` の写しが持つ）。

## Change impact

Check 465 が、rounds/ の受領文の数と全分冊の行の数、帯の外の日付の行、README が分冊を名指すことを照らす。

## Audience-specific notes

- **監査人**: 行の file 名から `rounds/` の写しを開き、元のアーカイブの月に当てて確かめられる。
