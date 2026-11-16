---
file: .github/scripts/count_b_topics.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/ACD-OSI-BOTTLENECKS.md / LICENSES/REFLECTION-BACKFILL.md / .github/scripts/census_decision_statements.py (DECIDERS)
---

# .github/scripts/count_b_topics.py

## What

読んだ節（LICENSES/*.md の `## 1.N`）が B1〜B15 のどれに当たったかを、会話の年代ごとに数える。節の表の最後の列
（ACD への当たり方）・末尾の反映の欄・REFLECTION-BACKFILL の行の B# を節ごとに集め、表の「誰が」の列が決める側
（census の DECIDERS）の行の B# を別に数える。`--by-year`・`--sections B10`。

## Why

未読 0・全節反映（提出のゲート 6c）を満たした 2026-11-16、5 人で「審査で最初に問われる順」を数で決め、入口の答えの順に
使う（30 の依頼・1c の段取り案）。手で数えると数え方が人ごとに割れるので、1 つの道具に置く。

## How

対象の節は Check 501b と同じ集合（comparison・REVISION-PROTOCOL・CHANGELIST・REFLECTION-BACKFILL を除く）。年代は見出しの
括弧の年、無ければ本文の最初の年、それも無ければ「不明」。同じ節で同じ B# は 1 回だけ数える。

## Constraints

- **我々の記録の中での頻度であって、審査の問いの頻度ではない。** 節は我々が選んで読んだ会話の記録で、census の候補の選び方と
  読む順の偏りがそのまま入る。入口の順に使うときは、その限定を同じ場所に書く。

## Change impact

- 節の表の列の並び（最後の列が ACD への当たり方）を変えると、数える列がずれる。

## Audience-specific notes

- **AI / 後任**: B の数の増減を「審査がそれを重く見る」と読まない。決める側の行の数のほうが、審査に近い。
