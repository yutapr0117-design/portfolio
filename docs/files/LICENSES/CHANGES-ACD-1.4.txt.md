---
file: LICENSES/CHANGES-ACD-1.4.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-20
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt (草案の本文と状態) / LICENSES/ACD-1.4-CHANGELIST.md (各変更の理由・日本語)
---

# LICENSES/CHANGES-ACD-1.4.txt

## What

1.4 草案の ACD-1.3 からの変更の一覧（英文・80 桁）。1 変更 1 箇条で、何を変えたか・閉じた errata の番号・語数の増減
（"(+N words.)"）を書き、末尾の要約の行に「ACD-1.3: N words, M clauses. This draft: N words, M clauses.」を置く。

## Why

2026-11-20 まで草案の冒頭（区切りの線より上）に在った。試作のたびに伸び、草案が Check 365 の 1,000 行に当たり続けた（11-20 だけで
3 回詰めた・1c）。確定の日に一覧は版の本文から外れる（凍結の対象は本文）ので、草案の外へ出しても失うものは「1 ファイルで読める」
ことだけで、草案の冒頭が名を指す（案 A・1c と 9b の合意）。名を `ACD-*.txt` の形にしないのは、版の本文を探す glob（11 か所）に
当たらないため。

## How

Check と道具は `_lib_draft_counts.with_changes()` を通して、この一覧を草案の冒頭のもとの位置（状態の箇条の後・「Still open in this
draft」の前）へ戻した文として読む。だから 468n（箇条ごとの語数）・468b（一覧が引く文が本文に在る）・468i（errata の番号）・
468f・498 (k)・502 は、移す前と同じ文を読む。試作を採る人（1c）は、このファイルに箇条を足す。

## Constraints

80 桁・ASCII（草案と同じ規則を 468 が見る）。一覧を読む mutation は `mutation_samples_common.CURRENT_CHANGES` を file にする。

## Change impact

版を確定するとき（prepare_version_freeze）、次版の一覧は草案の冒頭に戻して作られる —— 次版でも外へ出すなら、同じ手順でこのファイルの
次版を作る。

## Audience-specific notes

- **監査人**: 草案（ACD-1.4-DRAFT.txt）の冒頭がこのファイルの名を書いている。
