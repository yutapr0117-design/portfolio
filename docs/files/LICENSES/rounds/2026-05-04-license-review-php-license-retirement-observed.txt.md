---
file: LICENSES/rounds/2026-05-04-license-review-php-license-retirement-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-22
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #209 / LICENSES/ACD-1.0.against.md #146 / LICENSES/ACD-1.0.comparison.md §1
---

# LICENSES/rounds/2026-05-04-license-review-php-license-retirement-observed.txt

## What

**`license-review` の「PHP ライセンスの自主的な retire」スレッド全 4 通を逐語で保存したもの**
（2026-05-04・2026-09-22 に切り出し）。**我々宛ではなく、ACD-1.0 についてでもない。**

| 発言者 | 要点 |
| :-- | :-- |
| **Ben Ramsey 氏**（PHP Group を代表して）| *"I am submitting notice of the **voluntary retirement of the PHP License 3.01**"*。3.0 も superseded として同時に retire。**"the process for voluntary retirement isn't described on the OSI website"** |
| **Nick Vidal 氏**（OSI）| 同じ時間帯に *"I really appreciate the effort to move this forward"*。OSI の月次ニュースレターにも載せる |
| **McCoy Smith 氏**（Licensing Committee）| *"Kudos to the PHP community!"* |

**誰も「そういう手続きは無い」とは述べていない。誰も反対していない。
そして誰も、手続きを示していない。**

## Why

**`against.md` #146 が *"An approval cannot be undone"* と書いていたから。**
その根拠は Fontana 氏の *"The OSI does not currently have a process for de-listing licenses"*
（2026-09-11）である。**この 4 通は、その 4 か月前に承認が実際に巻き戻された記録である。**

**de-listing と retirement は別の行為である** —— 前者は OSI が steward の意に反して外すこと、
後者は steward 自身が申し出ること。**#146 は 2 つを括っており、その括りは我々に不利な向きに
働いていた** ——#84 への答え（`comparison.md` §1「この類型に 1 件足す費用は低い」）は、
**足したものをどれだけ戻せるかに依存する。**

**⚠ 有利な読みなので、狭く書く。** n = 1。手続きは公表されていない。
retire は「承認されなかったこと」にはならない。**そして steward が生きていることが要る**
——ACD の steward は個人 1 名で承継計画が無い（#10）。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-May.txt`
を**ブラウザ相当の UA** で取得した既存キャッシュから、該当 4 通を無改変で切り出した。

**見つけ方は「読む単位をスレッドから発言者へ変えた」こと** —— B14 の中心人物である
Nick Vidal 氏の 2026 年の投稿を全数列挙したところ **11 通**あり、**我々が読んでいたのは
2026-09-09 の 1 通だけ**だった。

## Constraints

- **無改変で保存する。**
- **観測（`-observed`）であって受領ではない。**
- **retire を「承認の取り消し」と書かない。** 承認された事実も記録も残る。
- **n = 1 を一般則として引かない。** 提出者自身が手続きの不在を述べており、
  **誰もそれに答えていない。**

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫も同じ commit で（**Check 465**）。
- **#146 の見出しはこの file により限定された。** 両方を同時に読むこと。

## Audience-specific notes

- **AI（実装者）**: **有利な発見ほど、逆側を同じ段落で探す**（`always_pair_the_converse`）。
  この entry の逆側は 4 つ書いてある。
- **監査人**: 取得元と日付は本文冒頭。同じ URL を同じ UA で取れば再現できる。
- **第三者**: 我々に有利な材料である。**だからこそ確立する範囲を狭く書いてある。**
