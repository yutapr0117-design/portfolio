---
file: LICENSES/ACD-1.0.gap-census.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.comparison.md / LICENSES/ACD-OSI-BOTTLENECKS.md
---

# LICENSES/ACD-1.0.gap-census.md

## What

**ACD-1.0 が埋めると主張する 3 つの gap**（(a) AI 学習 / TDM の明示許諾、(b) 公有等価ツールでの明示特許許諾、
(c) 許諾が学習済みモデル・パラメータ・出力に及ぶこと）を、**OSI 承認済みで非 deprecated の 141 本すべて**に
1 本ずつ当てた表と、その結論・逆側の記録。

## Why

gap 論は「既存は X を持たない」という全称の主張で、**比較対象を選ぶのが我々である限り検証にならない**。
`comparison.md` §1.97 は同じ 141 本で「条件の有無」を数えたが、**gap そのものを 1 本ずつ当てた表は無かった**。
全数で当てると、**有利な結論（(a)・(c) で名指しする本は 0）と同時に、不利な材料**
（許容型 ＋ 明示特許は既に在る / 作品から作った物へ特許を及ぼす CERN-OHL / 出力を外に置く GPL 系）が出る。

## How

- SPDX `license-list-data` の `licenses.json`（版数は本文に記載）で集合を決め、各 text を取得して sha256 を記録
- 語の出現を正規表現で数え、**0 でない命中はすべて文脈を読んで判定**（誤命中は本文の節に列挙）
- 特許許諾の有無と範囲は**人が読んで分類**した（判定基準は本文）
- **本文中の件数は全て表を数えて生成**しており、手で書いていない

## Constraints

- 本文・表は生成物だが、**生成スクリプトはリポジトリに置いていない**（取得物 141 本が repo 外のため）。
  再現は本文の「方法」節の正規表現と版数で行う
- **凍結中の本文（ACD-1.0 / 1.1）・`against.md`・bottleneck register・errata・1.2 草案には触れていない**。
  ここからの還元は各所有者の判断に委ねる（本文末尾の「拾う側へ」）
- Check 459 が索引（`LICENSES/README.md`）からの到達性を、Check 461c が `last-updated` を強制

## Change impact

SPDX の承認済み集合が変わったら（新規承認・deprecated 化）、**表を作り直す**。
表の数を手で直すと、表と文の数が食い違う。

## Audience-specific notes

- **審査者・第三者**: 「拾う側へ」の英文 1 文は**逆側の 1 文と対で**使う前提で書いてある
- **次の AI**: gap を主張する文を書く前にここを読む。**(b) は連言でしか立たない**ことを落とさない
