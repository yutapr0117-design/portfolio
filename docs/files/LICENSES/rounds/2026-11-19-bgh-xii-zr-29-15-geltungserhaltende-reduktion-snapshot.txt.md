---
file: LICENSES/rounds/2026-11-19-bgh-xii-zr-29-15-geltungserhaltende-reduktion-snapshot.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-19
canonical-ref: LICENSES/rounds/README.md (置き方の規約)
---

# LICENSES/rounds/2026-11-19-bgh-xii-zr-29-15-geltungserhaltende-reduktion-snapshot.txt

## What

Bundesgerichtshof, Urteil vom 6. April 2016, XII ZR 29/15 (as published by gesetze.co — a secondary publisher; the official collection is bundesgerichtshof.de) の XII ZR 29/15 を 2026-11-19 に WebFetch で取得した結果（portfolio-9b）。バイト単位の写しではない。

## Why

THIRD §18.5 の §14.2 の行が「効力維持的縮減の禁止の BGH の判例は未取得」と書いていた法源。約款の無効な条項を、許される限度まで縮めて生かすことはしない（BGB 306 条 2 項と合わせ、§14.2 の「法の許す限りに制限する」と §15.2 の「必要最小限に改める」が、約款と読まれたドイツでは働かない側の根拠）（当てる 1.4 草案の条: §14.2, §15.2）

## How

各条を 1 度ずつ取得し、道具が逐語で返した片だけを置いた（`add_law_snapshot.py`）。ヘッダに取得の日時 (UTC)・URL・取得した条・本文の sha256 を書いてある。

## Constraints

写しは道具を通ったもので、片と片の間に語が無いとは保証しない。法源は ACD を扱っていない。本文を直さない（`rounds/README.md`）。

## Change impact

この写しを引く節（§18 の行・jurisdictions）を直すときは、引用が本文に在るかを確かめる。版が改められたら取り直して新しい日付の写しを置く。

## Audience-specific notes

- **監査人**: ヘッダの URL を開き、片を原文に当てて確かめられる。
