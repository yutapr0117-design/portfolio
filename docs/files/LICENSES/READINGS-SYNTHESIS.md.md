---
file: LICENSES/READINGS-SYNTHESIS.md
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/REFLECTION-BACKFILL.md / LICENSES/REVISION-PROTOCOL.md
---

# LICENSES/READINGS-SYNTHESIS.md

## What

未読の OSI スレッドを 5 人で 0 にした後に、読みの節 244 の反映先を集め直し、条文（1.4 草案）・register（B と against と errata）・入口（提出の文書）のそれぞれに読みが何をもたらしたかを 1 か所で示す文書。

## Why

オーナーの前提「未読があり、未反映のまま本申請は出せない。全て読んで反映してこそ、出せる品質になる」に、記録の側から答えるため。節ごとの反映の欄と表は散らばっているので、本申請の判断の前に全体を見る面が要る。

## How

節の末尾の「反映:」の行（無ければ `REFLECTION-BACKFILL.md` の行）を集め、行き先の文の語で条文・register・入口に分けて数えた。B ごとの頻度は `count_b_topics.py` の出力を写した。

## Constraints

数は我々が読んだ会話の記録の中での頻度で、審査で問われる頻度ではない。分類は語による機械的なもので、行き先がその点をどれだけ扱ったかの質は測っていない。

## Change impact

節を足したり反映の欄を書き換えたりすると数が変わる。本申請の確定の日に数え直す。
## Audience-specific notes

- **監査人**: 各行の反映先の文書で、その節の番号を grep すれば確かめられる。
