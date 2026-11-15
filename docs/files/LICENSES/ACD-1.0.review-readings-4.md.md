---
file: LICENSES/ACD-1.0.review-readings-4.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/ACD-1.0.review-readings.md / LICENSES/AS-OF.md
---

# LICENSES/ACD-1.0.review-readings-4.md

## What

未読の OSI スレッドのうち 2004〜2005 に始まるものを読んだ記録（節 1.350 から）。書き手は portfolio-50（2026-11-15 の割り振り）。

## Why

2026-11-15 にオーナーが「未読の OSI スレッドを 5 人で無くして、反映して」と依頼した。5 人が同じ文書に並行して書くと
衝突し、1 つの文書が 1,000 行（Check 365）へ伸びるので、年の帯ごとに書き場所と節番号の帯を分けた。

## How

節の形は `review-readings-2.md` と同じ。読了は `record_read.py`（論点の無い会話は `--log-only`・`--start` は census の
会話の始まりの日付で、違えば道具が止まる）。register・against・errata に効く点は読んだ人が自分で書く（against の新しい行は
`against-2.md` の末尾へ）。本文への種は 1c へ送る。

## Constraints

- 節番号は 節 1.350 からの帯の中で使う。他の帯と重なると Check 500 が RED にする。
- 逐語の引用は `rounds/` か入口の manifest で解決できる形で置く（Check 472n / 476）。

## Change impact

- 節を足しても他の文書の数は動かない。読了の数（AS-OF・READ-THREADS）は `record_read.py` が直す。

## Audience-specific notes

- **審査者**: `REVIEWERS.md` → `review-readings.md` の末尾から辿る。
- **AI / 後任**: 帯の外の番号を使わない。1,000 行に近づいたら次の file へ分ける。
