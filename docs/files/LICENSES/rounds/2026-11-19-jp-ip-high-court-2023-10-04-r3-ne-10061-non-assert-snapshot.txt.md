---
file: LICENSES/rounds/2026-11-19-jp-ip-high-court-2023-10-04-r3-ne-10061-non-assert-snapshot.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-19
canonical-ref: LICENSES/rounds/README.md (置き方の規約)
---

# LICENSES/rounds/2026-11-19-jp-ip-high-court-2023-10-04-r3-ne-10061-non-assert-snapshot.txt

## What

知的財産高等裁判所 令和5年10月4日判決 令和3年(ネ)第10061号（判決要旨） の 知財高裁 令和5年10月4日 令和3年(ネ)第10061号 判決要旨 2(1), 知財高裁 令和5年10月4日 令和3年(ネ)第10061号 判決要旨 2(3) を 2026-11-19 に WebFetch で取得した結果（portfolio-30）。バイト単位の写しではない。

## Why

§18 の §5.1 の「日: 不起訴の合意は判例法で条文は無い（未取得）」を狭めるため。courts.go.jp の判例検索（不起訴の合意・18 件）で、特許の実施許諾と不起訴の合意を扱う知財高裁の判決が見つかった。§8.1・§8.6 の下流の第三者への届き方にも当たる。（当てる 1.4 草案の条: §5.1, §8.1, §8.6）

## How

各条を 1 度ずつ取得し、道具が逐語で返した片だけを置いた（`add_law_snapshot.py`）。ヘッダに取得の日時 (UTC)・URL・取得した条・本文の sha256 を書いてある。

## Constraints

写しは道具を通ったもので、片と片の間に語が無いとは保証しない。法源は ACD を扱っていない。本文を直さない（`rounds/README.md`）。

## Change impact

この写しを引く節（§18 の行・jurisdictions）を直すときは、引用が本文に在るかを確かめる。版が改められたら取り直して新しい日付の写しを置く。

## Audience-specific notes

- **監査人**: ヘッダの URL を開き、片を原文に当てて確かめられる。
