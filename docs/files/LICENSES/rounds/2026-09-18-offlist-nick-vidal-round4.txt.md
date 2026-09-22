---
file: LICENSES/rounds/2026-09-18-offlist-nick-vidal-round4.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-23
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #214 / LICENSES/ACD-1.0.against.md #215 / LICENSES/ACD-OSI-BOTTLENECKS-EXTERNAL.md (B14) / LICENSES/rounds/2026-09-15-offlist-nick-vidal-round3.txt
---

# LICENSES/rounds/2026-09-18-offlist-nick-vidal-round4.txt


> **🔴 2026-09-23: この file の本文は撤去された。**
> steward の指示により、**第三者（OSI moderator）の off-list 私信の全文を公開リポジトリに置かない**
> 方針を実装した（`against.md` #217）。**やり取りが在ったこと・日付・向きは残してある**
> ——それを消すと接触量を実態より小さく見せることになり、`rounds/` が防ぐために在る失敗そのものになる（#89）。
> **⚠ git 履歴には残っている。** 履歴の書き換えはこのリポジトリでは行わない。
> **⚠ 費用**: この本文に依拠していた逐語引用は、**リポジトリ内では検証できなくなった。**

## What

**moderator（Nick Vidal 氏）との off-list のやり取り、4 巡目**（2026-09-18・全 4 通）。
2026-09-23 に steward が渡した引き継ぎ文書の §7 を、そのまま保存したもの。
**その §7 は、2026-09-18 に Gmail 現物から逐語転記したものだと当の文書が述べている。**

| 時刻（JST） | 向き | 要点 |
| :-- | :-- | :-- |
| 09-17 22:42 | steward → list | **この投稿が拒否された** |
| 09-18 01:41 | steward → list owner | *"content of this specific message, or … my current moderation status"* のどちらかを問う。*"I wrote this particular message myself rather than having AI draft it"* |
| 09-18 13:09 | Nick Vidal → steward | **我々が `LICENSE` に載せている開示文を引いて**方針を再説。CoC の *"Respect time and attention"*。*"restrain yourself from using AI to generate licenses and posts"* |
| 09-18 15:23 | steward → Nick Vidal | *"I am the designer of ACD."* と、OSI への制度質問 |

**問い（内容か、moderation status か）には答えが返っていない。**

## Why

**3 つを変えるから**（`against.md` #215）。

1. **拒否された投稿の数を、我々は過少に書いていた。** 記録していたのは
   **`license-review` の 2 通**だけで、**`license-discuss` 側の拒否はどこにも無かった。**
2. **引き金は我々自身の公開文である。** moderator が警告の根拠として引いたのは、
   `LICENSE` に載せている開示文そのもの ——**`against.md` #66 は、その文が*無かった*ことを
   欠陥として記録した entry である。**
3. **人間が自分で書いた投稿が、それでも掛かった。**

**そして #214 の一次資料でもある** —— steward の 09-18 の返答が、我々の公開する来歴と
食い違う当の文である。

## How

steward がローカルから共有。**§7 だけを取り出し、本文は 1 バイトも変えていない**（規約 1）。
先頭に受領ヘッダと**証拠力の限界**を置いた（規約 3）。

**⚠ 引き継ぎ文書の残りは steward 自身の戦略評価であり、このリポジトリが公開するものではない。
取り出したのは §7 だけである。**

## Constraints

- **無改変で保存する。**
- **これは我々が取得したものではなく、steward が渡した転記である。**
  **off-list である以上、定義によりアーカイブと突き合わせられない。**
  **それが証拠力のすべてで、他の 3 つの off-list file と同じ規則である。**
- **moderator の行為は OSI の決定ではない**（`board-decisions.md`・B14 が 2026-09-10 から保つ読み）。
- **「問いに答えなかった」と「取り違えた」を混ぜない。** 記録が示すのは前者だけである。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫も同じ commit で（**Check 465**）。
- **「アーカイブに我々の投稿が無い」と書くときは、`license-review` の 2 通に加えて
  `license-discuss` の 1 通も拒否されていることを併記する。**

## Audience-specific notes

- **AI（実装者）**: **開示が引き金になった**という事実と、**開示が無かったことを欠陥として
  記録した #66** は、**1 つの決定の両端である。両方 register に置く。**
- **監査人**: 日時は分単位で本文にある。**ただし一次アーカイブでは確認できない**（off-list）。
- **第三者**: 我々に不利な材料である。**だから逐語で置いてある。**
