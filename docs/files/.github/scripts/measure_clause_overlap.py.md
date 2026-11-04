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
- 比較では、先行詞の無い指示語（those / these / that / such + Section(s) / provision(s) …）の Before / After も出す。同じ条の中で、それより前に条番号が無ければ宙に浮いている（2026-11-04、§2.8 の理由の文だけを外した私の試算版で末文の "those Sections" が先行詞を失ったのを、25 が読んで見つけた —— 道具は見ていなかった）

## Why

2026-11-04、オーナーが共有した別の AI の見解（B3 / B13 —— 法的な明瞭さ・解釈の負荷を、許諾の範囲・主体・効果を保ったまま、重複と読みの分岐を減らして下げる）を材料に 3 人が判断して進めた検証の分担のうち（課題設定は別の AI のもので、オーナーの指示ではない）、5a の受け持ち（KPI を機械で数える / 試作への反例探しの起点を作る）。人の目は「同じ働きを言い直している」箇所を拾うが、拾い漏れを数えられない —— この道具はその**対照**である。

## How

```
python3 .github/scripts/measure_clause_overlap.py LICENSES/ACD-1.4-DRAFT.txt
python3 .github/scripts/measure_clause_overlap.py --min 8 LICENSES/ACD-1.4-DRAFT.txt
python3 .github/scripts/measure_clause_overlap.py --compare LICENSES/ACD-1.4-DRAFT.txt <試作>
python3 .github/scripts/measure_clause_overlap.py --guard <試作>          # 468u の目印（効果を運ぶ句）が残っているか
python3 .github/scripts/measure_clause_overlap.py --uses <草案> Work "Computational Use"   # 定義語を使う条と回数
```

比較では、内容が変わった条を参照している箇所（`Section N.M`）も全件を文脈つきで出し、参照先の内容を述べる形（前後に purpose / states / explains / why など）に ⚠ を付ける。文を外すと、その文を「理由」や「目的」として指していた参照が宙に浮く（2026-11-04、F3 の T3 で §9.4 "Section 11.3 explains why …" が、外す候補の理由の文そのものを指していると分かった）。括弧の指し先も中身に依拠しうるので、全件を読む前提。

`--guard` の目印の一覧は `checks_license_draft.py` の `EFFECT_MARKERS_468U` だけに置き、Check 468u と同じものを読む（2 か所に持つと食い違う）。`--uses` は、定義を狭める試作（例: B15 の検証で §1.3 の "Work" を狭める）の前に、到達範囲が変わりうる条を一覧にする。

族は「同じ言い回しを共有する条の集合」で数える。条を言い回しで結んだ連結成分も参考に出すが、汎用の言い回しが数珠つなぎにする（1.4 草案では 37 条が 1 つになる）ので族の数には使わない。

## Constraints

- **測っていないもの: 法的効果。** 語の一致は同じ働きの証拠ではなく、語の消失は効果の消失の証拠ではない。出すのは「人が読んで確かめるべき箇所の一覧」まで。
- 効果を運ぶ語の語彙は網羅ではない。ここに無い語の消失は拾わない。
- 品詞は見ない。許諾の動詞の語が名詞として使われる形（直前が the / these / those / its / any / every / each / a）は数えないが、それ以外の名詞用法は数えてしまう（2026-11-04 に §2.8 の試算で「the grants themselves」を動詞と数えた誤検出から足した）。
- 語数は条の本文だけで、見出しや冒頭の変更一覧を含まない（草案が冒頭で申告する語数とは別の数）。

## Change impact

- 草案の条の書式（2 空白 + `N.M`）が変わると条を切れなくなる。

## Audience-specific notes

- **AI**: 試作が出たら比較モードを回し、減った「効果を運ぶ語」を反例探しの起点として渡す。数字は Before / After の両方を同じ道具で出す（片方だけ別の数え方にしない）。
