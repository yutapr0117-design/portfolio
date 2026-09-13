---
file: LICENSES/rounds/2026-09-10-license-review-chestek-names-us.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-13
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.review-corpus.md §1.73 / LICENSES/AS-OF.md
---

# LICENSES/rounds/2026-09-10-license-review-chestek-names-us.txt

## What

**Pamela Chestek 氏（OSI Licensing Committee 委員長）が 2026-09-10 に `license-review` へ投稿した
1 通の逐語。** OpenMDW-1.1 の審査スレッドの中で、**我々（Yuta-san）を名指しで謝辞している**:

> *"I would like to thank **Yuta-san** for their **insightful view on the termination provision**,
> which I find helpful."*

**我々宛のメールではない。** 他者の提出（OpenMDW-1.1）についての審査中の発言であり、
`rounds/README.md` の規約でいう **観測（`-observed` 系）** に当たるが、
**名指しされているので file 名は `-names-us` とした。**

## Why

**理由は 3 つある。**

**(1) 出典を残すため。** §1.73 と `AS-OF.md` がこの発言を引用しており、
**引用元の本文がリポジトリに無ければ、読み手は我々の要約しか確かめられない**（#82 の教訓）。

**(2) 日付が意味を持つため。** **これは moderator 通知（2026-09-09）の翌日である。**
通知の後も委員長による実質的なやり取りが続いたという事実は、**保存しておかなければ
後から「いつだったか」を巡って争いになる。**

**(3) 過大に読まれないため。** 本文を読めば、**これが ACD-1.0 についての発言ではない**ことが
すぐ分かる —— スレッドは OpenMDW-1.1 の終了条項についてのもので、謝辞はその論点についてである。
**要約だけを残すと、この区別が失われる。**

## How

`REVISION-PROTOCOL.md` §1 ①（受領）の規約どおり、**公開アーカイブの月次 `.txt` から
ブラウザ相当の UA で取得し、当該メッセージのブロックを無改変で保存した。**
先頭にコメント 4 行の header を付けてあり、**それ以外は 1 バイトも変えていない。**

## Constraints

- **無改変。** 整形・要約・翻訳・並べ替えをしない（我々の読みは誤りうるが、何と言われたかの
  記録は誤ってはならない）。
- **Check 465** が `rounds/README.md` の在庫申告を実 file から導出して照合するので、
  **この file を足したら README の一覧と件数も同じ commit で更新する。**
- **Check 108** が本 mirror の存在を BLOCKING で強制する。

## Change impact

この file を消すと、§1.73 と `AS-OF.md` の引用が**出典を失う**。
内容を編集すると、**逐語であるという前提そのものが壊れる**（分析は `review-precedents.md` 側に置く）。

## Audience-specific notes

- **AI（次のセッション）**: **この 1 通を「ACD-1.0 への反応」と数えてはならない。**
  ACD-1.0 への返信は 2026-09-13 時点でゼロである。
- **監査人**: 取得日と URL は header に書いてある。同じ URL で再取得して照合できる。
- **第三者**: 名指しの謝辞は、**我々の寄与が読まれたことを示すが、我々のライセンスについては
  何も示さない。**
