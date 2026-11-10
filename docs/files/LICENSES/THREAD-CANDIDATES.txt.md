---
file: LICENSES/THREAD-CANDIDATES.txt
audience: ai, 監査人
last-updated: 2026-11-11
canonical-ref: LICENSES/AS-OF.md（「未読スレッドの残り」の行）/ LICENSES/READ-THREADS.txt / .github/scripts/census_decision_statements.py
---

# LICENSES/THREAD-CANDIDATES.txt

## What

AS-OF の「未読スレッドの残り」の母数になる候補のスレッドの件名の一覧（1 行 1 件名・最初の通の日付つき）。候補は、決める側の発言があり（3 通以上・決める側の語 120 以上）、候補になった時点でドシエの 8 語の連なりが 8 回未満しか現れなかったスレッドである。

## Why

道具（`census_decision_statements.py threads`）は候補を「いまのドシエの語」で選んでいたので、ドシエに語が足されると、読んでいないスレッドも候補から外れ、未読の数が読まずに減っていた（2026-11-10 に 2 本: ZENTAO の承認依頼と 2007 年 8 月の委員会報告が、§1.171 の語で外れた）。一度候補になったスレッドをこの一覧に置き、道具は「いまの候補 ∪ この一覧 ∪ READ-THREADS」を母数にする。

## How

`census_decision_statements.py threads <out.json> --pin` が、一覧に無い新しい候補を日付順に足す。2026-11-11 の最初の一覧は、2026-11-09 の母数 778（その日の候補 776 と、外れた 2 本）で作った。

## Constraints

一度候補になったら外さない。未読から外れるのは `READ-THREADS.txt` に足したときだけ。道具の出力の「いまの語では候補でないが一覧に在る（N 件・うち未読 M 件）」で、母数の動きが「読んだから」か「語が増えたから」かを区別できる。

## Change impact

`AS-OF.md` の「未読スレッドの残り」の数（Check 498 (h) が和を見る）と、道具の `threads` の出力がこの file を数える。

## Audience-specific notes

- **監査人**: 各行の件名は公開アーカイブの月で引ける。候補の選び方は道具の `threads` にある。
