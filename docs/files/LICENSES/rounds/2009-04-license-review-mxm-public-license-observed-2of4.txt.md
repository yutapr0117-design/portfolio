---
file: LICENSES/rounds/2009-04-license-review-mxm-public-license-observed-2of4.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #244
---

# LICENSES/rounds/2009-04-license-review-mxm-public-license-observed-2of4.txt

## What

**MXM Public License の承認審査**（`license-review` / `license-discuss`・2009 年 4 月・全 59 通）の
**2/4 部**。**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**Carlo Piana 氏が 2023 年に、我々の論点（特許を除外した著作権のみのライセンス）の先例として
名指しした 3 件のうちの 1 件である** —— *"see discussion of CC0 or **the MXM license** or the
W3C license"*。**そして氏自身がこの提出者だった。**

**最も重いのは、OSD の起草者本人の発言がここに在ること** —— Bruce Perens 氏 2009-04-14:
*"The OSD does not distinguish between copyright, **moral rights**, patents, contract restriction,
or any other means of restricting what someone can do with software. **It applies equally to all of
those.**"* **これは「OSD は特許許諾を要求していない」という読み（#236）に対する、
起草者からの最も強い反対である**（#244）。**同じ 1 文が人格権にも及んでおり、§12 に当たる**（#245）。

## How

`https://lists.opensource.org/pipermail/license-{review,discuss}_lists.opensource.org/2009-April.txt`
から**ブラウザ相当の UA** で取得（2026-09-25）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **4 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **2012 年に同じ件名で続いた分は保存していない** —— 実体は CC0 のスレッドで、
  既に `2012-03-license-review-cc0-osd-patents-observed-*.txt` に在る（重複を作らない）。
- **ここに分析を書かない**（規約 2）。読みは `ACD-1.0.review-doctrine.md` §1.111 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: 2009 年分のみ。2012 年の続きは上記 CC0 の file に在る。
- **第三者**: これは他人の提出についての議論であって、ACD-1.0 への応答ではない。
