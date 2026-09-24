---
file: LICENSES/rounds/2026-08-28-license-review-villa-volume-etiquette-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-22
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.review-venue.md §1.99 / LICENSES/ACD-1.0.against.md #208 / LICENSES/ACD-OSI-BOTTLENECKS-EXTERNAL.md (B14)
---

# LICENSES/rounds/2026-08-28-license-review-villa-volume-etiquette-observed.txt

## What

**`license-review` の OpenMDW 審査スレッド中、Luis Villa 氏の 1 通を逐語で保存したもの**
（2026-08-28・2026-09-22 にキャッシュから切り出し）。**我々宛ではなく、ACD-1.0 に
ついてでもない。**

> *"the list's code of conduct has, since it was first written, asked people to respect each
> other's precious time by being concise and low-volume. The people we most need on this list
> are those whose time is very precious."*

**引用されている Rob Landley 氏の本文も、配送された形のまま残してある。**

## Why

**B14（moderator 通知）が引いたのと同じ CoC 条項が、その 12 日前に、AI とは無関係に、
人間の参加者へ向けて引かれているから。** 通知は *"this behavior goes against the
**\"Respect time and attention\"** from our Code of Conduct"* と述べる。

**我々は既に「現行 CoC の実質は簡潔さで、AI への言及は 1 語も無い」を条文で確かめていた。
これは、その条項が実際に list 上で発動した記録である** ——条文が在ることと、社会的に
強制されていることは別の事実で、**後者の一次資料をこれまで持っていなかった。**

**⚠ 同じ 1 通が逆側にも働く。** *"the word count is going to be high"* は**議論の volume**を
正当化しており、**ライセンス本文の語数（B3）ではない。混ぜてはならない**
（`against.md` #116 が記録した誤りと同じ形）。当たるのは `review-corpus.md` §1.80 の
**提出メールの長さ**の軸である。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-August.txt`
を**ブラウザ相当の UA** で取得した既存キャッシュから、該当 1 通を無改変で切り出した
（header ごと保存）。**見つけ方は件名の全数列挙**（2026-08 / 09 で 15 スレッド・155 通）で、
**この 1 通は件名にライセンスの語を 1 つも含まないので、語で探す限り出てこない。**

## Constraints

- **無改変で保存する。** このディレクトリで byte を変えることは規約違反である。
- **観測（`-observed`）であって受領ではない。**
- **Villa 氏は OSI の役員でも moderator でもない** ——本文末尾の定型文が
  *"opinions … are those of the sender and not necessarily those of the Open Source Initiative"*
  と述べている。**OSI の立場として引いてはならない。**
- **volume の指摘だけを切り出さない。** 同じ文脈には、Villa 氏が「他の人に任せる」と
  述べた人身攻撃の問題が併存する。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫も同じ commit で（**Check 465**）。
- 引用を運ぶときは、**この file の逐語と照合してから書く。**

## Audience-specific notes

- **AI（実装者）**: **件名が手続き的に見えるスレッドを開く**こと ——#206 はこのスレッドの
  8 月分 85 通を読みながら、この 1 通を件名だけで飛ばしていた。
- **監査人**: 取得元と日付は本文冒頭にある。同じ URL を同じ UA で取れば再現できる。
- **第三者**: 有利な半分（規範は AI 用ではない）と不利な半分（長さへの要求は明示されている）を
  同じ場所に置いてある。
