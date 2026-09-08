---
file: LICENSES/ACD-1.0.review-precedents.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-08
canonical-ref: LICENSES/ACD-1.0.comparison.md (条項レベルの比較) / LICENSES/PEER-REVIEW-WATCH.md (手続きの観測) / LICENSES/AS-OF.md
---

# LICENSES/ACD-1.0.review-precedents.md

## What

`license-review` / `license-discuss` のアーカイブを読んで、**ACD-1.0 に当たる指摘と当たらない
指摘**を逐条で整理した文書。§1.45（AI-MIT）/ §1.46（PBZC）/ §1.47（MIT-I）/ §1.48（Modified 0BSD）/
§1.49（人格権）/ §1.50（著作権だけでは足りない）。

## Why

`ACD-1.0.comparison.md` から 2026-09-08 に切り出した。**読者も用途も違う** —— `comparison.md` は
「既存ライセンスのどれを選ぶべきか」を条項で比べる文書で、本書は「**この提出は実際に何を
言われるか**」を先に知るための文書である。同じ file に置き続けると、advisory 予算（900 行）を
越えた時点で **分けるか黙らせるかの二択**になる。予算はそのために在る。

**節番号は変えていない。** `§1.45`〜`§1.50` を指す既存の参照（`against.md` / `AS-OF.md` /
`PEER-REVIEW-WATCH.md` / `QUESTION-INDEX.md` / `CLAUDE.md`）はすべてそのまま解決する ——
**分割で参照を壊さない最も安い方法は、番号を動かさないことである。**

## How

- 原文を引き、**発言者と日付を書く**。提出者による後の要約で代用しない
- **その読みが establish しないこと**を同じ場所に書く（個人資格の発言は OSI の裁定ではない）
- **有利な材料も落とさない**（#70: 擁護している側こそ古くなる）
- 取得手順は `PEER-REVIEW-WATCH.md` §3.9

## Constraints

- ACD-1.0 本文は凍結中（Check 453）。本書は本文ではないので凍結対象外
- Check 108（mirror 1 対 1）/ Check 459（索引からの到達性）/ Check 461c（last-updated）が縛る
- **逐語引用は逐語のまま**。引用の忠実性は `BLIND-SPOTS.md` の「逐語引用の忠実性」次元で検査済み

## Change impact

新しいスレッドを読んだら節を足す。**節番号は追記のみで、既存番号を動かさない**（参照が壊れる）。
900 行を越えたら、`comparison.md` と同じ判断 —— 分けるか、分けない理由を書く。

## Audience-specific notes

- **審査者**: あなたが出しそうな指摘の多くは、ここに既に書いてある（当たらない理由も含めて）
- **後任 AI**: この文書は「隣人のスレッドは審査者が何を論じるかを教える」の産物である。
  **新しい提出が現れたら読んで足す** —— `PEER-REVIEW-WATCH.md` の全数調査表が入口
