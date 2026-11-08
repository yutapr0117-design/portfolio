---
file: LICENSES/ACD-1.4-CLAUSE-REFERENCE-DRAFT.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-08
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt / LICENSES/ACD-1.0.clause-reference.md / LICENSES/ACD-1.4-CHANGELIST.md
---

# LICENSES/ACD-1.4-CLAUSE-REFERENCE-DRAFT.md

## What

1.4 草案の逐条リファレンスの下書き。草案の各条について「何を定めるか」と「なぜ必要か / 無いとどうなるか」を 1 行ずつ書き、1.0 と番号が違う条には 1.0 の番号を添える。

## Why

`ACD-1.0.clause-reference.md` は 1.0 の番号と中身で書かれている。提出の版が 1.4 になると、入口が紹介する逐条が提出する本文と食い違う。Check 460(c) はその申告を `ACD-1.0.txt` と照合するので、機械はこの食い違いを見ない。そこで草案の段階で 1.4 について書き直しておく。

## How

節ごとに書き手と、1.4 の本文に当てる照合役を置いた workflow で作り、そのあと portfolio-00 が挙げた「1.0 の表から引き継ぐと誤る説明」を該当する節に当てた。引用は草案の本文に逐語で在ることを機械で確かめた。

## Constraints

- 本文が勝つ。齟齬があれば本文に合わせてこの file を直す。
- 法的効果を確立したものとして書かない。記録が開いた問いとするものは開いたまま書く。
- 1.0 の逐条リファレンスは凍結版の説明として残し、こちらで上書きしない。

## Change impact

- 草案の条文を変える commit では、その条の行を同じ commit で直す。
- 提出の版を 1.4 に切り替える日に、入口（submission.md・REVIEWERS.md・README.md・QUESTION-INDEX.md）の逐条への案内をこの file（確定後の名前）へ向ける（`ACD-1.4-CHANGELIST.md` の切り替えの日の表）。

## Audience-specific notes

- **ai**: 条文を変えたら、この file の該当する行と「（1.0 の §x.y）」の対応を確かめる。
- **human (新卒)**: 条番号が分かっているときは、本文の前にこの表を引くと条の目的が先に分かる。
- **監査人**: 各行の errata と T の番号から、変更の理由の一次記録へたどれる。
- **第三者全般**: 読みの記録であって、法律家の判断ではない。
