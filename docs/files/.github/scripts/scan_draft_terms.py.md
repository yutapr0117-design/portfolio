---
file: .github/scripts/scan_draft_terms.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt / LICENSES/ACD-1.4-THIRD-CLARITY-TRIAL.md / .github/scripts/measure_clause_overlap.py
---

# .github/scripts/scan_draft_terms.py

## What

草案の条どうしの語の揺れを掃引し、読む候補を出す。(a) ほぼ同じ 3 項以上の列挙の 1 項以上の違い、(b) 同じ条を指す句の言い方の
揺れ、(c) 他の条の定義を借りる語（names = 人 / reaches・describes・governs = 範囲 / to the extent Section N = 限度 / binds = 拘束の
相手）を指し先ごとに並べ、同じ指し先から違う種類を借りていれば ⚠。

## Why

THIRD の §15.11・§15.12 は語の揺れを人の目で見つけ、T74〜T76 は定義を借りる語の食い違い（人・範囲・限度）を 1 か所ずつ直した。
草案全体を同じ型で掃引する道具が無かった（1c の依頼・2026-11-16）。1.3 に当てると、T74〜T76 が 1.4 で直した承継人の列挙の揺れ
（§2.8・§5.3・§12.4）を (a) が拾う —— 道具が捕まえるべき型を過去の本文で確かめた。

## How

条は measure_clause_overlap.clauses() で読む。列挙は「x, y, and z」の形、借りる語は「… Section N reaches / names / binds / governs」
と「to the extent Section N」。

## Constraints

- **候補であって欠陥の証拠ではない。** 語が違っても同じ働きのことがあり（単数と複数）、同じ語でも働きが違うことがある。効果は人が読む。

## Change impact

- 本文の条の形（`  N.M  …`）が変わると、measure_clause_overlap と同じく読み方が変わる。

## Audience-specific notes

- **AI / 後任**: 試作の前後で回して差を見る（新しく出た候補が、その試作が持ち込んだ揺れ）。

- **(d) 英米の綴りの混在（2026-11-16）**: 綴りの対（wilful / willful・authorise / authorize・endeavour / endeavor など 16 組）のうち、草案に両方がある語を出す。草案と 1.0・1.3 は英国綴りで揃っていて 0 件。いまの草案の authorise を 1 か所だけ authorize に変えた写しで ⚠ が出ることを確かめた。license / licence は名詞（licence）と動詞（license）を分けられないので数えない。
