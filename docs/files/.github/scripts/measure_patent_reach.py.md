---
file: .github/scripts/measure_patent_reach.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-06
canonical-ref: LICENSES/ACD-1.0.gap-measurements.md (§1.133・B10 の立証) / LICENSES/ACD-1.0.gap-census.md (範囲の分類) / .github/scripts/generate_gap_census.py (原文の取得)
---

# .github/scripts/measure_patent_reach.py

## What

B10 の立証（`gap-measurements.md` §1.133）——「OSI 承認済み・非 deprecated の全ライセンスのうち、作品を超える対象への特許許諾と、条件の不在を同時に持つものは 0 本」——を、審査者が自分で再現するための道具。gap-census の全数表から特許許諾の範囲が作品を超える（`S2` / `S3`）本を拾い、それぞれの SPDX 原文から条件と終了の文を逐語で出し、両立する本の数を数える。

## Why

測れると言う主張には、実際に走るコマンドを添える（`measure_gap_claim.py` が在るのと同じ理由・#122 / #123 の族）。§1.133 は ACD に固有の効果として立証できた唯一のもので、その 0 を読み手が確かめる手段が無ければ、主張は「我々が数えた」から先へ進まない。

## How

```
python3 .github/scripts/generate_gap_census.py --fetch   # SPDX の原文を取得（ネットワーク要・一度だけ）
python3 .github/scripts/generate_gap_census.py --check   # census が取得した原文から再現するか
python3 .github/scripts/measure_patent_reach.py
```

2026-11-04 の実行（SPDX 8791eda・2026-10-28）: 作品を超える特許許諾は 7 本（BlueOak / CERN-OHL-P・S・W / EUPL-1.1・1.2 / UPL）、7 本すべてに条件、UPL 以外の 6 本に終了の定め、両立する本は 0 本。

`--express`（2026-11-04）は、明示の特許許諾を持つ全本（census の「明示」列）の条件の文を逐語で出す。主張は「範囲 ∧ 無条件 ∧ 終了なし」の連言なので、全本が条件を持つなら範囲の分類（読みの判定）に依拠せずに同じ結論が出る。実測 65 本すべてに義務の文があり、見つかった文は人が 1 本ずつ読んで確かめた。**ただし多くの条件は頒布のときにしか発動しない** —— Work を配らず学習だけする受領者には発動しないので、この結論は「条文に条件が在る」ことまでで、「その受領者に条件が掛かる」ことではない。

## Constraints

- **分類（S1 / S2 / S3）は census の読みの判定で、この道具は検証しない。** S1 の本が実はモデルに届くと読めるなら、結論は変わりうる（§1.133「確立しないこと 2」）。
- 条件・終了の検出は正規表現で、見つけた文を示すまで。見つからないことは「無い」の証明ではない。条件は notice 等の具体的な義務を優先して探す（汎用の "you must" を先にすると BlueOak の受諾の文を拾った）。
- 法的な効果も、OSI の判断も測らない。
- **全数が揃わなければ結論を出さない**（2026-11-06・別の AI の patch の指摘をオーナーが渡した）。原文の欠落、取得の失敗、取得時の sha256 との不一致、census の sha256 との不一致のどれでも exit 2 で止まる。それまでは欠けた本を黙って飛ばし、最後の 0 が完全に見えた。Check 489b が空のキャッシュで確かめる。**SPDX の一覧が census の後に動くと止まる**ので、そのときは `generate_gap_census.py` で census を作り直す。

## Change impact

- census の表の列（範囲の列が 5 番目）が変わると、拾う本を誤る。

## Audience-specific notes

- **審査者**: 上の 3 行で、主張の 0 を自分の環境で出し直せる。
