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

- 比較では、**外した語に依拠するドシエの箇所**も出す（`LICENSES/*.md`。`rounds/` と CHANGELIST / CLARITY-TRIAL / ADVERSARIAL-TRIAGE の作業記録は除く）。本文の中の参照だけを見ると、§6.5 の前半を外す試作 h1 は通るが、提出文 `submission.md` §B.0 はまさにその前半を根拠に *"for the reason §6.5 gives"* と引いていた（2026-11-04、bb の提案・25 が同意）。審査者向けの文書（submission* / review-responses* / clause-reference / faq / comparison / against / REVIEWERS / SUBMISSION-MATERIALS / READY-TO-SUBMIT / README）は「その版を対象にするなら書き換えが要る」として、errata / BLIND-SPOTS* / SELF-AUDIT / discussion-log / review-corpus などの記録は「当時の本文を引く」として分けて出す（記録を書き換えると履歴を偽る）。`against.md` はファイル単位で外向き: 入口が審査者に読ませる全ラウンド通しの一覧で、版を付けない現在形の行は出す版が変わると偽になる。日付の有無で行を分けると、日付を含む #133 を落とす

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

- 文書をまたぐ照合は、外した **5 語の連なり**（空白・大小・引用符と `*` `_` を正規化）と、理由を本文に帰す形（"§N.N gives" / "Section N.N's own text" / "§N.N 自身が述べ" 等）だけを見る。**言い換えは拾わない** —— `faq.md` A8 の *"because Covered Rights exclude patents"* は構造を自分の言葉で述べるだけで、理由の文を外しても真のままなので、拾わないのが正しい。
- 照合する句は 2 段: 変更後の本文の**どこにも**無い句は常に出し、その条からは消えたが他の条や PREAMBLE に残る句は**行がその条番号を名指すときだけ**出す。段を分けたのは実測による —— 文単位では残った後半まで拾って 29 件中ほぼ全部が誤検出、本文全体だけで差し引くと試作 f の誤検出 8 件は消えたが `clause-reference.md` の 8.4 行（本物の依拠・句は他の条にも在る）を落とした。偶然 5 語が一致するだけの行（試作 e で `review-responses-clauses.md` の §15.7 の説明が §2.8 の句と一致）は残るので、出た行は全件を読む。
- 5 語の連なりは文の中だけで作る。文をまたぐと、文末に語を足しただけの試作 i（§2.7）で "holds. Where" の連なりが「外した」と数えられ、語を足す案の対照が誤検出になった。
- ドシエの条番号は 1.0 の番号で書かれていることがある（1.0 §1.2 = 1.4 §1.3 など）。番号の形の一致は「版の条番号に注意」として出す。

## Change impact

- 草案の条の書式（2 空白 + `N.M`）が変わると条を切れなくなる。

## Audience-specific notes

- **AI**: 試作が出たら比較モードを回し、減った「効果を運ぶ語」を反例探しの起点として渡す。数字は Before / After の両方を同じ道具で出す（片方だけ別の数え方にしない）。
