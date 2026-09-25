---
file: LICENSES/rounds/2016-01-license-review-bsd-plus-patent-approval-observed-1of10.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #235
---

# LICENSES/rounds/2016-01-license-review-bsd-plus-patent-approval-observed-1of10.txt

## What

**`BSD-2-Clause-Patent` の承認審査**（`license-review`・2016 年 1 月・全 68 通）の **1/10 部**。
**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**permissive なライセンスに明示的特許許諾を足したものを OSI が承認した近い先例の 1 つ**で（同じ形の承認済みは他に UPL-1.0 と BlueOak-1.0.0 がある —— `ACD-1.0.gap-census.md`。**審査スレッドで承認理由まで読めるのはこの 1 本**）、
**我々の特許 gap にとって最も近い承認済みの隣人**である。

**テキストの census（`ACD-1.0.gap-census.md`）は「その条文が在る」ことは示すが、
「なぜ承認されたか」は示さない。** このスレッドには提出者が書いた承認理由が逐語で在る ——
*"the desire of certain organizations to have a simple permissive license that is compatible
with the GNU General Public License (GPL), version 2, but which also has an express patent
grant included"*。**これは我々の理由とは違う**（我々のは公有化型 + AI/TDM）。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2016-January.txt`
から**ブラウザ相当の UA** で取得。**抽出は件名で厳密に行った** ——
本文中の語で拾うと別スレッド 4 通（`AFL/OSL/NOSL 3.0` ほか）が混入する。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- 分割は Check 365（1,000 行）のため・**メッセージ境界**で切ってある。
- **ここに分析を書かない**（規約 2）。読みは `against.md` #235 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけ。そのときは書き換えず別 file に置く。

## Audience-specific notes

- **監査人**: 本 1/10 部は **584 行**。全体は 68 通で、10 部すべてを読む。
- **第三者**: **他人の提出についての議論**であって、ACD-1.0 への応答ではない。
