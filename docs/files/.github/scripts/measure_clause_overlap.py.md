---
file: .github/scripts/measure_clause_overlap.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-04
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt (測る対象) / LICENSES/ACD-OSI-BOTTLENECKS.md (B3 / B13)
---

# .github/scripts/measure_clause_overlap.py

## What

ACD の草案と試作文について、条の重複と「効果を運ぶ語」の差分を数える道具。

- 単体: 条（`  N.M  …` の形）ごとの語数・全体の語数、条をまたいで 6 語以上一致する言い回しの全数（条の組・語数・本文）、言い回しごとの族
- `--compare BEFORE AFTER`: 条ごとの語数の差と、効果を運ぶ語（主体 / 許諾の動詞 / 範囲 / 除外・限定 / 条件・時点）の出現回数の増減

## Why

2026-11-04、オーナーの依頼「B3 / B13（法的な明瞭さ・解釈の負荷）を、許諾の範囲・主体・効果を保ったまま、重複と読みの分岐を減らして改善する」に対する 3 人の分担のうち、5a の受け持ち（KPI を機械で数える / 試作への反例探しの起点を作る）。人の目は「同じ働きを言い直している」箇所を拾うが、拾い漏れを数えられない —— この道具はその**対照**である。

## How

```
python3 .github/scripts/measure_clause_overlap.py LICENSES/ACD-1.4-DRAFT.txt
python3 .github/scripts/measure_clause_overlap.py --min 8 LICENSES/ACD-1.4-DRAFT.txt
python3 .github/scripts/measure_clause_overlap.py --compare LICENSES/ACD-1.4-DRAFT.txt <試作>
```

族は「同じ言い回しを共有する条の集合」で数える。条を言い回しで結んだ連結成分も参考に出すが、汎用の言い回しが数珠つなぎにする（1.4 草案では 37 条が 1 つになる）ので族の数には使わない。

## Constraints

- **測っていないもの: 法的効果。** 語の一致は同じ働きの証拠ではなく、語の消失は効果の消失の証拠ではない。出すのは「人が読んで確かめるべき箇所の一覧」まで。
- 効果を運ぶ語の語彙は網羅ではない。ここに無い語の消失は拾わない。
- 語数は条の本文だけで、見出しや冒頭の変更一覧を含まない（草案が冒頭で申告する語数とは別の数）。

## Change impact

- 草案の条の書式（2 空白 + `N.M`）が変わると条を切れなくなる。

## Audience-specific notes

- **AI**: 試作が出たら比較モードを回し、減った「効果を運ぶ語」を反例探しの起点として渡す。数字は Before / After の両方を同じ道具で出す（片方だけ別の数え方にしない）。
