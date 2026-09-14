---
file: LICENSES/rounds/2026-09-14-license-review-openmdw-thread-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-15
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.review-corpus.md §1.82 / LICENSES/ACD-1.0.against.md #146 / LICENSES/ACD-1.0.comparison.md §1
---

# LICENSES/rounds/2026-09-14-license-review-openmdw-thread-observed.txt

## What

**`license-review` の OpenMDW-1.1 スレッドから、2 通を逐語で保存したもの**（2026-09-15 取得）。
**我々宛ではなく、ACD-1.0 についてでもない。** 保存したのは、この 2 通が
**承認の取り消し可能性について、承認する側の発言を含む**からである。

| | 発言者 / 日付 | 要点 |
| :-- | :-- | :-- |
| (A) | **Carlo Piana 氏** 2026-09-14 | de-listing の是非を持ち出した参加者に対し、議論を打ち切る返信。*"revising **ALL** the approved licenses (which we have done recently), some approved licenses … leave licensing experts **scratching their heads**"* |
| (B) | **Richard Fontana 氏** 2026-09-11 | *"The OSI does not currently have a process for **de-listing** licenses … there are actually **worse licenses on the OSI-approved list**"* |

**(B) は配送された本体を保存してある**（(A) の引用の中だけではない）。
**引用の中にしか残っていない文と、配送された文は別物である** ——同じ規律で
`against.md` #91 を書いた。

## Why

**#84（「0BSD が在るのに、なぜもう一つ PD 等価を出すのか」）への我々の答えの前提を変えるから。**

その答えは `comparison.md` §1 にあり、*「この類型に 1 件足す費用が低い」* と述べていた。
**費用が低いことと、取り返しがつかないことは両立する。** de-listing の手続きが無く、
作る議論が「当面は何もしない」に落ち着いており、**しかも委員会が最近 全件を見直して
一部に不満が残っているなら、もう一つ足すことに慎重になる理由は増える。**

**同じ 2 文には有利な読みもある**: **承認済みリストには、専門家が首をかしげる起草の
ライセンスが実在する** ——そう述べているのは**承認する側の人間**であり、我々の推論ではない。
**起草の粗さは承認の絶対的な障壁ではない**（#6 / B3）。

**どちらが勝つかは我々には決められないので、両方を register に載せてある。**

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt`
を**ブラウザ相当の UA** で取得し、該当 2 通を無改変で切り出した（header ごと保存）。
ファイル冒頭に**取得日・取得元・「我々宛ではない」ことの明示**を置いてある。

## Constraints

- **無改変で保存する。** このディレクトリで byte を変えることは規約違反である
  （`rounds/README.md`）。
- **観測（`-observed`）であって受領ではない。** 向きを取り違えると、
  **「我々に対して言われたこと」の量を誤って多く見せる。**
- **どちらの発言も ACD-1.0 に言及していない。** 沈黙の反証にも、承認の見込みの証拠にも
  使ってはならない。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で
  （**Check 465** が照合する）。
- 引用を他の文書へ運ぶときは、**この file の逐語と照合してから書く**。

## Audience-specific notes

- **AI（実装者）**: この file の 2 文は**両刃**である。片側だけを引いて使わないこと。
- **監査人**: 取得日は本文冒頭に書いてある。**同じ URL を同じ UA で取れば再現できる。**
- **第三者**: アーカイブは公開されており、読み手は自分で取れる。
