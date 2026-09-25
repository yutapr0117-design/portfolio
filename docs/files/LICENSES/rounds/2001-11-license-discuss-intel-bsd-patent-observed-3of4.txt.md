---
file: LICENSES/rounds/2001-11-license-discuss-intel-bsd-patent-observed-3of4.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #236
---

# LICENSES/rounds/2001-11-license-discuss-intel-bsd-patent-observed-3of4.txt

## What

**Intel's proposed BSD + Patent License**（`license-discuss`・2001-11）の観測保存（3of4）。
**我々宛ではなく、ACD-1.0 についてでもない。**

## Why

**特許許諾を GPL の OS に条件づけた 2001 年版が OSD 3 / 6 / 8 で争われ、承認されなかった。** 2016 年の無条件版は承認されている（`2016-01-...` を参照）。**ACD §8.2 が無条件・終了不能である理由に当たる。**

## How

`https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/` から
**ブラウザ相当の UA** で取得し、**折り返しを畳んだ `Subject:` で厳密に抽出**した
（本文中の語で拾うと別スレッドが混入する —— #235 で実際に踏んだ）。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- 分割がある場合は Check 365（1,000 行）のためで、**メッセージ境界**で切ってある。
- **ここに分析を書かない**（規約 2）。読みは `against.md` #236 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけ。そのときは書き換えず別 file に置く。

## Audience-specific notes

- **監査人**: 本 file は **678 行**。スレッド全体は複数部に分かれることがある。
- **第三者**: **他人の議論の観測**であって、ACD-1.0 への応答ではない。
