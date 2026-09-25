---
file: LICENSES/ACD-1.0.gap-measurements.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.comparison.md / LICENSES/ACD-1.0.gap-census.md
---

# LICENSES/ACD-1.0.gap-measurements.md

## What

ACD-1.0 の gap の主張（「既存の承認済みライセンスは X を持たない」）を、**既存ライセンスの本文に当てて測った 3 節**。
§1.96（grant 条項を逐語で当てた）/ §1.97（承認済み 141 本の全数で「条件の有無」を数えた）/
§1.104（既存ライセンスについての我々の主張 6 件を本文に当てた）。

## Why

切り出し元の `comparison.md` が 893 行で advisory（900）の手前に達した。切り出し元は「条項で比べる」文書、
移した 3 節は「gap の主張が本文に当てて成り立つかを測った」記録で、用途が違う。同じ用途の全数表
`ACD-1.0.gap-census.md` と読み手が重なる。

## How

- 節番号は `§1.xx` の共有採番のまま動かしていない（Check 471(f) がファイルをまたいだ重複を禁じる）
- 切り出し元には番号で始まらない案内の節を残した（案内が見出し番号を持つと 471(f) の重複になる）
- 文書を名指した参照（`comparison.md` §1.97 等 9 箇所）はこのファイルへ張り替えた

## Constraints

- Check 459 が索引（`LICENSES/README.md`）からの到達性を、Check 461c が `last-updated` を強制
- 外部の本文はリポジトリに無い。再現は各節の方法の記述で行う

## Change impact

gap の主張を書き換えるときは、ここと `gap-census.md` を両方当て直す。

## Audience-specific notes

- **審査者**: 各節に「逆側」がある —— 不在は効果の不在ではない、の但し書きを読み落とさないこと
