---
file: .github/scripts/errata_faces.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-23
canonical-ref: LICENSES/ACD-1.0.errata.md (errata の一次記録) / .github/scripts/sync_stated_counts.py (件数の同期)
---

# .github/scripts/errata_faces.py

## What

errata を 1 件足した (または状態を変えた) ときに、consistency を 1 回回して、その E 番号を名指す誤りと errata の件数の誤りだけを、面ごとに「どこに・何を・誰が (道具か人か)」の形で並べる。何も書き換えない (`--apply-counts` で件数だけ `sync_stated_counts.py --apply` に揃えさせる)。

## Why

2026-11-23 に 5e が E87 を足したとき、Check 464・468 (Still open)・460 (v) と件数・469・498 (a) / (j) が別々の面を求め、読み分けに往復が要った。

## How (usage)

```sh
python3 .github/scripts/errata_faces.py E88
python3 .github/scripts/errata_faces.py E88 --apply-counts
```

## Constraints

errata の行 (`ACD-1.0.errata.md` の表) は先に人が書く。処置の文 (草案冒頭の Still open・errata 冒頭の英文・確定した版の CHANGELIST の英文) は判断なので、場所と形だけを示す。面の印は誤りの文の語に依るので、Check の文言を変えたら FACES を直す (当たらない誤りは `[?]` として全文を出す)。

## Change impact

面を足す Check ができたら FACES に行を足す。

## Audience-specific notes

- **本文担当**: 「Still open in this draft:」の句は本文担当が書く。
