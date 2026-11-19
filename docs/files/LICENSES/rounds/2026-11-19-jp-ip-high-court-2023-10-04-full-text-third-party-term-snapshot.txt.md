---
file: LICENSES/rounds/2026-11-19-jp-ip-high-court-2023-10-04-full-text-third-party-term-snapshot.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-19
canonical-ref: LICENSES/rounds/README.md (置き方の規約)
---

# LICENSES/rounds/2026-11-19-jp-ip-high-court-2023-10-04-full-text-third-party-term-snapshot.txt

## What

知的財産高等裁判所 令和5年10月4日判決 令和3年(ネ)第10061号（判決全文） の 知財高裁 令和5年10月4日 令和3年(ネ)第10061号 判決全文 第4 当裁判所の判断 2(1)（43〜44 頁） を 2026-11-19 に WebFetch で取得した結果（portfolio-30）。バイト単位の写しではない。

## Why

50 の依頼（問い 5 の第 4 の問い）: 判決が、不起訴の合意を第三者のために置けたかに触れているかを全文で確かめる。触れていない（537 条・第三者のためにする契約の語は無い）が、裁判所が探した条項の形は『許諾を受けた者が売った第三者への権利行使が妨げられる旨の定め』だった。（当てる 1.4 草案の条: §5.1, §8.1, §8.6）

## How

各条を 1 度ずつ取得し、道具が逐語で返した片だけを置いた（`add_law_snapshot.py`）。ヘッダに取得の日時 (UTC)・URL・取得した条・本文の sha256 を書いてある。

## Constraints

写しは道具を通ったもので、片と片の間に語が無いとは保証しない。法源は ACD を扱っていない。本文を直さない（`rounds/README.md`）。

## Change impact

この写しを引く節（§18 の行・jurisdictions）を直すときは、引用が本文に在るかを確かめる。版が改められたら取り直して新しい日付の写しを置く。

## Audience-specific notes

- **監査人**: ヘッダの URL を開き、片を原文に当てて確かめられる。
