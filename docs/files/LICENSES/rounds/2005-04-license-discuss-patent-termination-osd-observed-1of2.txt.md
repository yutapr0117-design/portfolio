---
file: LICENSES/rounds/2005-04-license-discuss-patent-termination-osd-observed-1of2.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #236
---

# LICENSES/rounds/2005-04-license-discuss-patent-termination-osd-observed-1of2.txt

## What

**Proposed new OSD item - patent termination**（`license-discuss`・2005-04）の観測保存（1of2）。
**我々宛ではなく、ACD-1.0 についてでもない。**

## Why

**Perens 氏「BSD には黙示の特許許諾が在る —— 自分の特許を体現するソフトを使用許諾つきで頒布すれば、その特許について estoppel を与えたことになる」**、Garrett 氏「OSD はそもそも特許許諾を要求していない」。**特許 gap の重みに直接当たる。**

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

- **監査人**: 本 file は **703 行**。スレッド全体は複数部に分かれることがある。
- **第三者**: **他人の議論の観測**であって、ACD-1.0 への応答ではない。
