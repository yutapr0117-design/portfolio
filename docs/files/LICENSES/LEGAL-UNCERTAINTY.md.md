---
file: LICENSES/LEGAL-UNCERTAINTY.md
audience: ai, human (新卒), 監査人, 法律家
last-updated: 2026-11-16
canonical-ref: .github/scripts/measure_legal_uncertainty.py
---

# LICENSES/LEGAL-UNCERTAINTY.md

## What

法的解釈の不確実性の台帳: 数え方、THIRD の第 18 節 の記録の行の形、2026-11-16 の基準線（BASELINE-DATA）。

## Why

オーナーの依頼（2026-11-16）で、不確実性を減らし続ける進み具合を数で言うため。

## How

数は `measure_legal_uncertainty.py` が出し、ここには書き写さない。基準線は `--pin` が BASELINE-DATA に書く。

## Constraints

基準線を書き換えるのは 5 人が決めた日だけ。

## Change impact

THIRD の第 18 節 の行の形を変えるときは、道具の ROW の正規表現と同じ commit で。

## Audience-specific notes

- **法律家**: 問いの一覧は `QUESTIONS-FOR-COUNSEL.md`。この台帳はその数え方であって、問いの中身ではない。
