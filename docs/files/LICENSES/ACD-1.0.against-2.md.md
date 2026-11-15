---
file: LICENSES/ACD-1.0.against-2.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/ACD-1.0.against.md / LICENSES/REVIEWERS.md
---

# LICENSES/ACD-1.0.against-2.md

## What

不利な事実の register（`ACD-1.0.against.md`）の**続き**。#223 から後の行を持ち、新しい行はこの file の末尾へ足す。
番号は 1 冊目から続き、状態の記法・行の閉じ方・総括の文（「grown from 14 entries to N」など）は 1 冊目に在る。

## Why

1 冊目がバイトの予算（Check 495・advisory 800 KB / ceiling 1,000 KB）を越えたので、2026-11-15 に分けた。
**伸びている表（#223〜）を出した**（30 の判断）—— 静的な表（#82〜#222）を出すと 1 冊目が新しい行でまた伸び、
同じ日がもう一度来る。分けた後は 1 冊目が約 534 KB で止まり、この file だけが伸びる。

## How

register の file の一覧は `.github/scripts/_lib_dossier.py` の `AGAINST_FILES` だけが持つ。数える側（460 (e)/(f)/(g)・
474・491・`sync_stated_counts.py`）は `against_text()` で 2 冊を合わせて読む。分ける日の予行と作業の一覧は同じ file の
docstring に在る。

## Constraints

- 行の番号は変えない。語も変えない（分けた commit は行を動かしただけ）。
- 不利な事実を後から**減らさない**。反論できるようになっても行は消さず、status を動かす（1 冊目と同じ）。

## Change impact

- 行を足すと 460 (e)/(g)・474・491 の数が動く。総括の数は `sync_stated_counts.py --apply` が 2 冊を合わせて書き直す。
- この file を別の名へ動かすときは `AGAINST_FILES` と、この file に anchor を持つ mutation（474 の 2 件）の "file" も直す。

## Audience-specific notes

- **審査者**: 1 冊目の冒頭（状態の記法）を先に読む。この file は表の続きだけを持つ。
- **AI / 後任**: 新しい不利な事実はこの file の末尾へ。1 冊目の表に行を足さない（1 冊目がまた予算へ伸びる）。
