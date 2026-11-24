---
file: LICENSES/ACD-1.0.review-readings-7.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.0.review-readings.md / LICENSES/AS-OF.md
---

# LICENSES/ACD-1.0.review-readings-7.md

## What

採掘の記録の続き（節 1.476 から）。書き手は採掘の役（portfolio-d7）。`ACD-1.0.review-readings-6.md` の続き。

## Why

readings-6 が BYTE-BUDGET の上限（200,000 B）の手前（180,647 B・2026-11-24）に来たので、肥大化の規律（BLOCKING の手前で処理する）に従って次の file に分けた。

## How

節の形は `review-readings-2.md` と同じ。読了は `record_read.py`（論点の無い会話は `--log-only`・`--start` は census の
会話の始まりの日付で、違えば道具が止まる）。register・against・errata に効く点は読んだ人が自分で書く（against の新しい行は
`against-2.md` の末尾へ）。本文への種は 1c へ送る。

## Constraints

- 節番号は readings-6 の続き（節 1.476 から）。他の文書と重なると Check 500 が RED にする。
- 逐語の引用は `rounds/` か入口の manifest で解決できる形で置く（Check 472n / 476）。

## Change impact

- 節を足しても他の文書の数は動かない。読了の数（AS-OF・READ-THREADS）は `record_read.py` が直す。

## Audience-specific notes

- **審査者**: `REVIEWERS.md` → `review-readings.md` の末尾から辿る。
- **AI / 後任**: 帯の外の番号を使わない。1,000 行に近づいたら次の file へ分ける。
