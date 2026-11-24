---
file: LICENSES/ACD-1.5-CLAUSE-REFERENCE-DRAFT.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.5-DRAFT.txt / LICENSES/ACD-1.4.clause-reference.md / LICENSES/CLAUSE-MAP-1.4-1.5.tsv
---

# LICENSES/ACD-1.5-CLAUSE-REFERENCE-DRAFT.md

## What

縮約した 1.5 草案（10 節 52 条）の逐条の下書き。条ごとに「1.4 のどの条から来たか」「何を定めるか」「なぜ必要か / 1.4 との差・逆側」を 1 行で書く。

## Why

条番号が 1.4 と全部違うので、1.4 の逐条と入口の条番号が草案と食い違う。凍結の前に条ごとの行を揃えておく（議題 16 の後の付け替え）。

## How

草案から条番号を抜き出して 52 条と一致することを機械で確かめ、1.4 の条の列を `CLAUSE-MAP-1.4-1.5.tsv` と突き合わせた（2026-11-24）。由来の errata と試作の経緯は 1.4 の逐条の行が持ち、ここでは繰り返さない。

## Constraints

- 本文が勝つ。齟齬があれば本文に合わせてこの file を直す。
- 法的効果を確立したものとして書かない。

## Change impact

- 草案の条文を変える commit では、その条の行を同じ commit で直す。

## Audience-specific notes

- **ai**: 条文を変えたら、この file の行と `CLAUSE-MAP-1.4-1.5.tsv` を同じ commit で直す。
- **human (新卒)**: 1.4 の条番号しか分からないときは 2 列目で引く。
- **監査人**: 由来の errata は `ACD-1.4.clause-reference.md` の対応する行から辿る。
- **第三者全般**: 読みの記録であって、法律家の判断ではない。
