---
file: .github/scripts/measure_descriptor_carryover.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-01
canonical-ref: LICENSES/ACD-1.4-CHANGELIST.md (E10 の項・記述子の作り方) / .github/scripts/checks_license_surfaces.py (Check 451d / 451e)
---

# .github/scripts/measure_descriptor_carryover.py

## What

**前版の機械可読記述子（`ACD-<版>.machine.json`）が `clause` で引く条のうち、新版で本文が変わった条を列挙する道具。**
条ごとに「新版に在るか」「本文が同じか」と、変わっていれば一致度（difflib の ratio）を出す。

## Why

新しい版の記述子は前版を下敷きに作る。**番号が同じでも内容が変わった条をそのまま持ち越すと、記述子が条文と食い違う**
（Check 451d は条の存在しか見ない）。2026-11-01 に 1.3 → 1.4 を手で当てて 4 条が該当した（portfolio-25 の依頼で道具化）。
道具で回すと、引かれている 23 条すべてを比べて **5 条**（§4.2 / §4.3 / §8.1 / §8.4 / §16.4）が出た —— §16.4 は同日に
外部レビューを受けて直した条で、手作業の後に変わったもの。

## How

```sh
python3 .github/scripts/measure_descriptor_carryover.py          # 最新の記述子の版 → 現行草案（どちらも導出）
python3 .github/scripts/measure_descriptor_carryover.py 1.3 1.4  # 版を指定
```

## Constraints

- **Check ではない**。変わった条の事実を述べ直すかは判断である。
- 本文は区切り線（`-` × 80）より後。一致度 0.5 未満は「別の条になっている可能性」として印を付ける。

## Change impact

記述子の形（`clause` の key 名）を変えたら `cited()` も合わせる。

## Audience-specific notes

- **AI**: 新しい版の記述子を作る直前に回し、出た条ごとに前版の事実を本文に当て直す（451e の §6 / §8 / §9 要求と合わせて）。
