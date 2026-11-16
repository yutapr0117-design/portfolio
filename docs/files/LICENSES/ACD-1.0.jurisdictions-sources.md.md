---
file: LICENSES/ACD-1.0.jurisdictions-sources.md
audience: ai, human (提出者), 監査人, 採用検討者, 学術研究者, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/ACD-1.0.jurisdictions.md (元の文書)
---

# LICENSES/ACD-1.0.jurisdictions-sources.md

## What

`ACD-1.0.jurisdictions.md` の §9（2026-09-20 の敵対的レビューが名前を挙げた法源・判例の一覧）と §9a（そのうち 8 件を原典で読んだ記録と、その後の追加）を、元の番号のまま置いた文書。

## Why

法域ごとの読みに一次の法源（条文と判決の逐語）を足し続けると、元の文書が 1,000 行の上限（Check 365）に届く。§9 と §9a は一まとまりの記録（外から届いた法源とその読み）なので、まとめて分けた（2026-11-16・portfolio-30）。

## How

本文は移す前と同じで、見出しの番号（9・9a と (1)〜(11)）もこの文書が持つ。元の文書には、§ を前に置いた指しだけを残した（見出しが番号を名乗らないように）。他の文書の、元の文書の §9a (N) を指していた参照は、同じ PR でこの文書を指すよう書き換えた。

## Constraints

法的助言ではない。元の文書の §10（この文書の限界）がこの文書にも当たる。

## Change impact

`measure_legal_uncertainty.py`（9b）は `ACD-1.0.jurisdictions*.md` を読むので、この文書の「確立していないこと」の段も数える（分けた時点でこの文書の該当の段は 0）。参照の解決は Check 471 が見る。

## Audience-specific notes

- **監査人**: 移す前の本文は、この文書を足した commit の親の `ACD-1.0.jurisdictions.md` に在る。
