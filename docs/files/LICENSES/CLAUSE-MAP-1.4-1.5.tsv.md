---
file: LICENSES/CLAUSE-MAP-1.4-1.5.tsv
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.5-DRAFT.txt (草案の本文) / LICENSES/ACD-1.5-CHANGELIST.md (各変更の理由・日本語)
---

# LICENSES/CLAUSE-MAP-1.4-1.5.tsv

## What

ACD-1.4 の条（§5.2 の項と番号の無い段を含む）が、1.5 草案のどの条へ行ったかの対応表。タブ区切りで、1 列目が 1.4 の条、2 列目が
1.5 草案の条（空白区切りで複数・引き継がないものは —）、3 列目が日本語の注（同じ / 広げた / 外した、と理由）。

## Why

1.5 草案は 1.4 を述べ直し、条番号をすべて変えた（合議の議題 12・15・16、`ACD-1.5-CLARITY-TRIAL.md` §12）。1.4 の番号で書いた
文書（逐条・索引・想定問答・register）を 1.5 へ移すときに、番号を記憶でなく表で移すために置く。

## How

行を足すときは、1.4 の条を 1 列目に 1 度だけ書く。意味が動く所は `ACD-1.5-CHANGELIST.md` の「T146 で意味が動く所」の節が持つので、
ここの注は短く書く。

## Constraints

2 列目の番号は 1.5 草案に実在すること。

## Change impact

草案の条番号を動かしたら、この表を同じ commit で直す。1.5 を確定した後は、外向きの面の番号の移しに使う。

## Audience-specific notes

- **監査人**: 「外した」と書いた行が、`CHANGES-ACD-1.5.txt` の一覧にも在ることを確かめる。
