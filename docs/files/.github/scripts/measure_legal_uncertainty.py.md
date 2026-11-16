---
file: .github/scripts/measure_legal_uncertainty.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/LEGAL-UNCERTAINTY.md
---

# .github/scripts/measure_legal_uncertainty.py

## What

法的解釈の不確実性の台帳を数える道具。草案の節ごとに、法律家への問い（Q）・実務家への問い（P）・jurisdictions の「確立していないこと」（J）・開いている errata（E）・THIRD の第 18 節 の記録の行（R と ①②③・狭まった）を数え、`LICENSES/LEGAL-UNCERTAINTY.md` の基準線からの増減を出す。

## Why

オーナーの依頼（2026-11-16）「ACD-1.4-DRAFT.txt の法的解釈の不確実性を『５人』で減らし続けてください」。5 人で決めた台帳（2f の案に 30 と 50 が重ねた）の、9b の持ち分。

## How

`python3 .github/scripts/measure_legal_uncertainty.py`（表）・`--pin`（今日の数を基準線にする）。2026-11-16 の基準線: Q 16・P 7・J 21・E 1、計 45（節ごとに数えるので、2 つの節を名指す問いは 2）。第 18 節の記録の行は `- §N.M | 命題: … | ①/②/③ | 状態: … | 法源: rounds/…` の形だけを読む。

## Constraints

「出典あり」の行の法源の file が無ければ ⚠ を出して終了コード 1。数が減ることは不確実性が減ったことの必要条件で、十分条件ではない（台帳の「establish しないこと」）。

## Change impact

問いの見出しの形（`## N. … (§…)`）や jurisdictions の「**確立していないこと**」の印を変えると数が変わる。

## Audience-specific notes

- **AI / 後任**: 基準線は 5 人が決めた日だけ `--pin` で書き換える。
