---
file: LICENSES/rounds/2017-04-license-review-pd-type-submissions-observed-1of2.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-28
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.review-doctrine.md §1.129 / LICENSES/ACD-1.0.against.md
---

# LICENSES/rounds/2017-04-license-review-pd-type-submissions-observed-1of2.txt

## What

**我々の類型（公有化の献呈 / PD 等価）の提出 2 スレッド、全 10 通**の第 1 部（全 2 部）（2026-09-28 取得）。
**我々宛ではなく、ACD-1.0 についてでもない。**

| | スレッド | 通数 |
| :-- | :-- | :-- |
| (A) | *"For approval, by license steward, a license recognizing public domain derivation"*（2010-04-11）| **1**（返信ゼロ）|
| (B) | *"Proposal for OSI Approval track: Modified MIT License for Public Domain software"*（2017-04-13〜05-30）| **9** |

## Why

**`license-review` の全期間 census（199 か月・2026-09-28 実行）は、我々の類型に見えるスレッドを
27 件挙げる。そのうちドシエが一度も言及していなかったのがこの 2 件である。**

**(B) が重い理由は 2 つある。** **(1) 最初の実質的な返信が、Rob Landley 氏が後に我々へ向けた
のと同じ問い**である —— Richard Fontana 氏 *"Are you aware of the Free Public License 1.0.0,
also known as the Zero-Clause BSD license? … **Do you see anything distinctive about your
license relative to FPL/0BSD?**"*。**(2) McCoy Smith 氏が、公有化の献呈が測られる試験を
言葉にしている** —— *"Have you confirmed that that statement is **legally effective to result in
a dedication to the public domain**? … **the wording they use in CC0 is much more comprehensive**
… The language you use is **quite brief**"*。

**(A) は、我々の類型の提出が返信ゼロで終わった実例**である（#109 / #117 の基準率の、
類型を絞った側の 1 点）。

## How

月次 mbox を**ブラウザ相当の UA** で取得し、件名で 2 スレッドを header ごと無改変で切り出した
（**選別ではなくスレッド全体**）。

## Constraints

- **無改変で保存する**（`rounds/README.md`）。
- **観測（`-observed`）であって受領ではない。**
- **⚠ 帰属に注意。** (B) の *"Three things: 1) The FPL does not indicate an intent of Public
  Domain…"* は**提出者の文**であり、McCoy 氏の言葉は `>>…<<` で囲まれた部分である。
  **引用符を剥がして読むと取り違える。**

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。

## Audience-specific notes

- **AI（実装者）**: **(B) の試験は当てれば答えが出る** ——`review-doctrine.md` §1.129 が
  ACD §3 と CC0 §2 を語数と要素で突き合わせている。**当てた結果は 5 要素中 4 つが被覆・1 つが未対応**で、
  **その 1 つを register へ立てた。**
- **監査人**: 取得日は本文冒頭。同じ URL を同じ UA で取れば再現できる。
