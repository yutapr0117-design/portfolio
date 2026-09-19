---
file: .github/scripts/measure_citation_drift.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-19
canonical-ref: LICENSES/ACD-1.2-CHANGELIST.md (条項の対応表) / LICENSES/ACD-1.0.submission.md (SUBMISSION-TARGET) / .github/scripts/checks_license_dossier.py (Check 472)
---

# .github/scripts/measure_citation_drift.py

## What

**提出側の文書が引く条が、版をまたいで意味を変えていないかを測る道具。**
条番号ごとに 2 つの版の本文を比べ、**消えた / 番号は在るが本文が変わった / 実質同一**に分ける。
**定義の写像は番号ではなく定義語（`"X" means`）で引く。**

## Why

**Check 472 は「引いた条が提出対象の版に*存在するか*」しか見ない。**
**存在するのに意味が違う場合を、それは捕まえられない。**

2026-09-19 の実測で、**§1 の定義は並べ替えで番号が入れ替わっていた** ——
`§1.4`（*You* のつもりで引いている）は次版では *Dedicator* を指す。**番号は在るので 472 は通る。**
**その朝に書いた対応表は「§1 は番号を動かしていない」と述べており、誤りだった** ——
**比べたのが「番号の集合」で、動いたのは「中身」だったから。**

## How

- 対象は提出側の 4 面（`submission.md` / `submission-reference.md` / `REVIEWERS.md` / `objection-map.md`）
- 本文は 80 本のダッシュで冒頭の説明部を切り、`difflib` の一致度で分類（0.97 超を実質同一）
- **定義は語で照合**する ——番号で推測すると**並べ替えの向きを間違える**

## Constraints

- **Check にしない。** 「意味が変わった」の閾値は判断であり、**正当な改訂まで RED にする**
  （E4 が §6.4 の文言を直したような場合）。**道具として手で回し、出た一覧を人が当たる。**
- 公開アーカイブの取得は不要（リポジトリ内で完結する）

## Change impact

**版を確定させる日に必ず 1 回回す**（`ACD-1.1-CHANGELIST.md` §0.13 の確定手順）。
**出力の「別の条」印（一致度 0.15 未満）は、引用を書き換えないかぎり必ず誤りになる。**

## Audience-specific notes

- **審査者**: 我々が提出前に自分の引用を機械で当て直していることの証跡である
- **後任 AI**: **「番号が同じ」を「同じことを指す」と読まないこと。** それがこの道具の存在理由である
