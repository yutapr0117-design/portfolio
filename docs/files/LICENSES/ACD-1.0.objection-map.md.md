---
file: LICENSES/ACD-1.0.objection-map.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-09-09
canonical-ref: LICENSES/ACD-1.0.review-precedents.md / LICENSES/ACD-1.0.against.md / LICENSES/REVIEWERS.md
---

# LICENSES/ACD-1.0.objection-map.md

## What

**直近 24 か月に `license-review` / `license-discuss` で出た反論を全部並べ、ACD-1.0 に当たるかを
1 表にした文書。** 当たるものを先に置き、当たらないものには**条文で確かめた理由**を付ける。
出典は全て公開アーカイブで、発言者と日付を書く。

## Why

**審査者が最初に知りたいのは「どの既知の反論がこの提出に当たるか」である。** それを
900 行の precedent 記録の末尾に置くのは、`against.md` #6（長さ）に対して我々ができる
数少ない実務的な対処を捨てることになる。**1 ページで読めることがこの文書の機能である。**

## How

- 2026-09-09 に `ACD-1.0.review-precedents.md` から切り出した（同 file が advisory を越えた）
- **節番号 §1.62 は変えていない**ので既存の参照は解決する
- 各行は `#N`（不利な事実）と `§1.x`（原文と読み）へ二重に紐づく

## Constraints

- **「当たらない」は我々の読みであって審査者の判断ではない**、と文書自身が明記している
- **反論は組み合わさる**（長い + 採用 1 件 + 弁護士が読んでいない）。表は個別にしか答えない
- 網羅ではない。読んだ窓は `PEER-REVIEW-WATCH.md` にある

## Change impact

行を足したら `review-precedents.md` の該当節と `against.md` の `#N` も同じ commit で。
Check 460 face (k) が `#N` / `E<n>` の解決性を強制する。

## Audience-specific notes

- **審査者**: ここから読める。原文は `review-precedents.md`、不利な事実の本体は `against.md`
- **後任 AI**: **この表を「我々は正しい」の一覧に育てるな。** 当たるものを先に置く順序は規約であり、
  当たらない側だけが伸びていたら、それは読み方が偏っている兆候である
