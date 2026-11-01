---
file: LICENSES/ACD-1.4-ADVERSARIAL-TRIAGE.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-01
canonical-ref: LICENSES/ACD-1.0.against.md (#279) / LICENSES/ACD-1.4-CHANGELIST.md
---

# LICENSES/ACD-1.4-ADVERSARIAL-TRIAGE.md

## What

**2026-11-01 にオーナーが転送した、別の AI による ACD-1.4 草案の敵対的監査（A01〜J20）を、
現行の条文と既存ドシエに 1 件ずつ当てた仕分け表。** 各行は報告書の要点・担当・分類（既知-修正済 /
既知-回答済（法的残余）/ 取引 / 新規→修正 / 新規→記録 / 外部 / 対象外）と根拠を持つ。

## Why

外から届いた大量の指摘は、既知のものを「新規」と数えて水増しするか、未読のまま「対応済み」と
括るかのどちらかに崩れやすい。**1 件ずつ根拠に当て、どこに既に答えがあるかを指す**ことで、
重複処理も取りこぼしも行単位で見えるようにした。

## How

3 セッションで分担する（条文 = 25 / ドシエ = bb / 機械層とシナリオ = 5a）。条文の修正は 25 だけが
行い、採否と理由は `ACD-1.4-CHANGELIST.md` に書く。5a が他の 2 人の行から抜き取って当て直す。

## Constraints

- **報告書の本文は置かない**（第三者の文書。要点は各行の短題に写した）。
- **AI によるレビューを提出要件の「法的レビュー」に数えない。**
- 凍結版（1.0〜1.3）の本文は変えない。

## Change impact

行を「新規→修正」にしたら、`ACD-1.4-CHANGELIST.md` と（1.0 からの欠陥なら）errata を同じ PR で揃える。

## Audience-specific notes

- **監査人**: 各行の根拠は既存の記録（`against.md` の番号・errata の E 番号・`QUESTIONS-FOR-COUNSEL.md` の問い）を指す。
