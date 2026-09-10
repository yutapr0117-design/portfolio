---
file: LICENSES/ACD-1.0.review-precedents.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-09-09
canonical-ref: LICENSES/ACD-1.0.comparison.md (条項レベルの比較はこちら) / LICENSES/PEER-REVIEW-WATCH.md (手続きの観測) / LICENSES/AS-OF.md (日付つきの外部事実)
---

# 他の提出がどう扱われたか —— 提出ごとの記録

**この文書は `ACD-1.0.comparison.md` から 2026-09-08 に切り出し、2026-09-09 にさらに二分した。**
節番号は一度も変えていないので、既存の `§1.4x` / `§1.5x` 参照はすべて解決する。

**二分の境界は「何についての記録か」である。**

- **本書 = 提出ごとの記録**（§1.45〜§1.48 / §1.51 / §1.53 / §1.54 / §1.57 / §1.63）——
  「**この提出はどう扱われたか**」。1 つの提出の顛末を追う。
- **[`ACD-1.0.reviewer-positions.md`](ACD-1.0.reviewer-positions.md) = 主題ごとの記録**
  （§1.49 / §1.50 / §1.52 / §1.55 / §1.56 / §1.58〜§1.61）——
  「**審査者はこの主題について何と言っているか**」。複数の提出を横断する。

**新しい節はどちらかに足す。** 迷ったら「1 つの提出の話か、1 つの主題の話か」で決める。

**何のための文書か**: `comparison.md` は「既存ライセンスのどれを選ぶべきか」を条項で比べる。
こちらは **`license-review` / `license-discuss` の記録を読んで、ACD-1.0 が実際に何を言われるかを
先に知る**ための文書である。**原文を引き、発言者と日付を書き、その読みが establish しないことを
併記する**（`PEER-REVIEW-WATCH.md` の読み方の規律と同じ）。

**取得と読み方の手順は `PEER-REVIEW-WATCH.md` §3.9 にある。**

---

## 1.45 最も近い同時代の比較対象 —— AI-MIT / AIAL-1.0（2026-03・提出の翌日に撤回）

**2026-09-06 に一次資料で読んだ。** `license-review` と `license-discuss` の 2026-03 に計 36 通ある。
提出者は **AI 生成コードのための permissive ライセンス**として出し、動機は ACD-1.0 §9 とほぼ同じ
——「既存ライセンスは人間の著者を前提に書かれており、AI 生成コードについて**存在しないかもしれない
著作権と人間の著作者性を含意してしまう**」。**提出は 2026-03-12、撤回は 03-19。**

**なぜ止まったかを、条ごとに我々へ当てる。** 以下は「我々の方が優れている」という主張ではなく、
**3 つの反論がこの本文では発火しない**という条文上の対応である。

| AI-MIT / AIAL への反論（発言者・原文） | ACD-1.0 の該当 | なぜ発火しないか |
|---|---|---|
| **佐渡秀治氏**（Open Source Group Japan 会長）: 透明性条項が再頒布だけでなく *"use as input for further AI training"* でも発火する → **OSD #10**。帰属要求は **OSD #3・#7**。そして —— *"it is not clear how **conditions derived from copyright can be imposed in a stable way on code for which copyright may not exist at all**"* | **§10.1** | **条件を一切課さない。** 課す条件が無いので、「存在しないかもしれない権利に由来する条件」という不安定さが生じる余地が無い |
| **Joshua Gay 氏**: *"overreading Thaler v. Perlmutter"* —— 「完全に AI 生成」と表示された file を**そのままパブリックドメインと扱える**という前提は、現行法が支えるより強い | **§9.2** | **権利の存否について一切表明しない。**「存在しないなら本 Dedication は何も足さず何も奪わない／**存在する、あるいは後に存在すると判断されるなら** §3〜§8 と §12 が全面適用」と両方向に書いてある |
| **Josh Berkus 氏**（OSI）: 実プロジェクトは AI 生成・AI 補助・人間著述・他 OSS 由来の file が混在し、履歴を通じて改変される。ファイル単位の帰属モデルは *"targets only brand-new projects created from scratch and never modified again"* | **§9.3** | **どの部分が機械生成かを判定する必要が無い。** *"No permission granted here depends on that question, or on how any jurisdiction answers it, or on whether the answer changes."* |

**この読みが establish しないこと。** AI-MIT が止まったことは ACD-1.0 が通ることを意味しない。
同じスレッドで佐渡氏は *"this proposal should receive **legal review before** the community debates
whether it should be approved"* とも述べており、**これは我々にこそ当たる**（#1・#2）。Berkus 氏の
「名称が MIT の商標に触れる」も我々には無関係だが、それは我々の設計の功績ではなく命名の偶然である。

**ただし方向の違いは実体である。** 2024 年以降に来た AI 時代の instrument は、観測できた範囲では
**いずれも条件を足す方向**（透明性義務・帰属・利用制限・出力への notice）で、そこが争点になっている。
**ACD-1.0 は逆方向に振り切った唯一の提出である** —— 条件をすべて取り去り、権利の存否を判定しなくても
成立するように書いてある。**同じ問いに対する反対向きの賭けであって、同じ賭けの次の 1 件ではない。**

**その鏡像も同じ場所に書く。** 「逆方向に振り切った唯一の提出」は、裏返すと **その方向を誰も
検証していない**ということでもある。**採用が 1 件しかない以上、実地で確かめられてもいない**（#4）。

**⚠ ここには最初、誤った鏡像を書いた（2026-09-06 に同日中に是正）。** 初版は「条件を取り去るだけで
足りるなら 0BSD と MIT-0 が既にある。よって差別化は §6・§8.4・§9 の 3 主題だけにかかる」と述べたが、
**結論も含意も誤りである。** 正しい分析は**この同じ文書の §1.35** に既にあった。

- **§6 と §8.4 は「改訂で埋まる側」**である。§1.35 は 7 つの差のうち 4 つ（ML/TDM の許諾・不留保の
  言明・モデルと出力に届く特許・データベース権）を **既存が条項を足せば消える差**として明示している。
  差別化の根拠をそこに置くのは、**最も脆い足場を選ぶこと**になる。
- **0BSD と MIT-0 は近い代替物ではない。** §1.35 の結論は「既存が改訂した場合、ACD-1.0 の差は
  **権利の存在を前提としないこと**と**誰にも条件を課さないこと**の 2 つに縮む」であり、
  **前者が 0BSD / MIT-0 との根本的な違い**である。両者は条件を外した *著作権者による許諾* であって、
  **権利が存在することを前提としている**。ACD-1.0 は §9.2 で「いかなる権利も subsist するとは
  表明しない」と述べ、一段手前から始まる。§1.35 の言葉では「**その前提を組み替えることは改訂ではなく、
  別の instrument である**」。**機械生成物という、まさに前提が崩れる場面での差**であり、
  AI-MIT を止めた佐渡氏の指摘（存在しないかもしれない権利に由来する条件）が刺さらないのもここに拠る。
- **条件の不在についてだけは、初版の狭い指摘が成り立つ** —— **0BSD / MIT-0 との比較に限れば**
  条件の不在は共有された性質であって差別化ではない。ただしそれは、§1.35 が挙げるもう一方の差
  （前提の不在）が効いていることを何ら弱めない。

**この誤りの形は記録に値する。** 直前の commit で「不利と有利は鏡写しで同時に存在する」と原理を
書き、**その同じ commit の中で、不利方向へ過剰修正した鏡像を作った**。#87 初版と同じ形である。
そして**正しい分析は編集中のファイルの 100 行上にあった** —— 失敗したのは分析ではなく、
**自分が書き込もうとしている文書を読まなかったこと**である。

### 「OSD の枠組みがこの種の instrument を受け付けないのでは」——測ると逆だった

上の読みには反対解釈がありうる ——「止まっているのは条件のせいではなく、**OSD の枠組み自体が
この種の instrument を受け付けないから**」。これが正しければ、条件を取り去った ACD-1.0 も同じ壁に
当たる。**だが、それなら往復が生じないはずである。** 枠組みが拒む形は実際に観測できていて、
それは**審査以前にモデレータが差し戻す**姿をしている（2026-08-07 の UPD 1.5.2 提出者が
`license-review` で受けた扱いがそれで、`license-discuss` へ回された）。

**トラッカーの 252 件で往復の深さを測ると、AI 時代の 6 件は拒まれるどころか最も手厚く議論されている。**

| | timeline（記録された往復） | 参加者 |
|---|---|---|
| **AI 時代の 6 件** | 中央値 **22** | 中央値 **10** |
| 残り 246 件 | 中央値 7 | 中央値 4 |

内訳は ModelGo v2 が **119 往復 / 14 名**、OpenMDW 1.1 が **103 / 19**、AI-MIT が
**撤回までの 1 週間で 35 / 14**（OSI 理事・各国 OSG 会長を含む）。**典型的な提出の約 3 倍の往復と
2.5 倍の参加者**である。

**したがって「枠組みが受け付けない」という読みは、記録が支持しない。** 受け付けない形は短い
スレッドと少ない参加者、あるいは審査以前の差し戻しとして現れる。実際に起きているのはその逆で、
**この主題は `license-review` でいま最も濃く議論されている領域**である。

**片側にしない。** 濃い議論は同時に**濃い精査**であり、争点が多いことは通りやすさを意味しない
（AI-MIT は 35 往復のあと撤回された）。言えるのは「**争われている**」であって「**拒まれている**」
ではない、という区別だけである。

---

## 1.46 我々の類型が実際に審査された唯一の近例 —— PBZC v2.0（2024-12 提出 → 2025-01 撤回）

**Public Benefit Zero Copyright License v2.0**（Wayne Thornton 氏）は、**公有化の献呈**として
`license-review` に出され、17 通・約 5 週間の審査を経て**撤回**された。**我々の類型が実際に
審査された、直近で唯一の例である**（2026-09-07 にアーカイブで読了）。

**なぜ #87 の一覧に無かったか**: #87 はトラッカーの**名称検索**で類型を数えた。PBZC は名称に
public domain / dedication / waiver / CC0 / Unlicense / 0BSD のいずれも含まない。#87 は
「name matching is a floor, not a census」と**自分で書いておきながら、2 度目の走査をしなかった**
（`against.md` #99）。

### 何が問題にされ、それが ACD-1.0 に当たるか

| 指摘（発言者・日付は原文どおり） | ACD-1.0 |
|---|---|
| **Carlo Piana（2024-12-18）**: 献呈と**コピーレフト**が同居しており *"one cannot really calculate the effect of the license in different jurisdictions"* | **当たらない。** ACD-1.0 にコピーレフトは無く、§10.1 が条件を一切課さない |
| **Piana（同日 18:29・上の続き）**: *"I have nothing against using a **PD dedication and a license by way of backstop** where PD does not really exist in the fullest… **I actually advise to use both**"* | **これは指摘ではなく支持である。** §3（献呈）と §4（許諾）の対は、この審査者が**自ら勧める**構造そのもの。「dedication *taken alone* は承認されない」という 2020 年の勧告に対する我々の答え（§4.4）と同じ向き |
| **McCoy Smith（2024-12-18）**: 対を持つこと自体は *"not necessarily fatal"*。ただし CC0 は「PD が可能な法域では完全な献呈、それ以外では制限のない極めて寛容な許諾」と**明確に**書いており、PBZC はそうなっていない | **§4.4 がまさにその明確さを書いている** —— §4 は §3 とは独立に付与され、**§3 が無効であることに依存しない**。受領者はどちらが作用したかを判断しなくてよい |
| **McCoy（同）**: PD 法域では公有・それ以外ではコピーレフト、という構造は *"likely violates OSD 5 as it discriminates against people in non-public domain dedication jurisdictions"* | **当たらない、が答えを書いておく必要がある**（`against.md` #100）。**PBZC は実体的な結果が法域で変わる**（公有 vs コピーレフト）。ACD-1.0 で法域により変わるのは §12 の**機構**（放棄が可能な法域では放棄・不能な法域では本著作物に限定した不行使の合意）だけで、**受領者が得るものは §4 により同一**である。§10.4 により何も終了せず、§4.4 により §3 の有効性を判断する必要も無い |
| **McCoy（12:52）**: *"public domain is a concept that exists as part of international copyright law… **You can't just rewrite in a way you like**"* | **当たらない。** ACD-1.0 は公有の定義を書き換えない。§3 は放棄の意思表示であり、§9.2 は機械生成物に著作権が生じるか否かについて**何も表明しない**（表明しないことが要点） |
| **Lukas Atkinson（2024-12-18）**: Unlicense を模した条文への批判。*"The Unlicense is not a particularly well-drafted license or PD dedication, and should not serve as a model… **That it was eventually OSI-approved has more to do with its widespread use in some circles**"* | **当たらない（我々は Unlicense の条文を模していない）。しかも #87 の独立した裏付けである** —— Unlicense の承認が普及によるものだ、というのは我々自身が不利な事実として書いていることで、それが**リストの常連から 2024 年に独立に述べられている** |
| **Atkinson（同）**: *"I would be very happy if new licenses/dedications/devices in the 'PD dedication' or 'PD equivalent' category **make use of this wealth of prior discussions (well over a decade)** and avoid running into the same problems"* | **これは我々への要求そのものであり、既に満たしている。** 2012-01〜04 と 2020-03〜06 の議論を原典で読み、`submission-reference.md` §1b と本書 §1.4 に反映してある（`PEER-REVIEW-WATCH.md` §3.9） |
| **Piana**: *"it seems to deliver a grant only for copyright and not under every right that encumbers the free use of the software"* | **当たらない。** §2.2 の Covered Rights は著作権と隣接権を含み、§7 が sui generis データベース権、§8 が特許、§12 が人格権を個別に扱う |

### この 1 件から取れる最も重要な事実

**Pamela Chestek 氏（OSI Licensing Committee 委員長・肩書を明示した発言）、2024-12-18**:

> To be clear, **we do not require review by a lawyer, only recommend it. That is not a blocker.**

これは Piana 氏の「OSI requires prior review by a lawyer」への訂正で、**Piana 氏自身が同日
"I stand corrected re: Pam's message on requiring legal review, bad choice of words on my side."
と撤回している**。

**我々の最大の不利な事実（#5 / #79・法的レビュー不在）に対する、最も強い反証材料である。**
**ただし過大に読まない** —— *recommend* は残るし、Piana 氏の当初の反応が示すとおり、
審査者はそれを重く扱いうる。**「要件ではない」は「軽い」ではない。**

---

## 1.47 撤回不能性が単独で審査された唯一の例 —— MIT-I（2025-07 提出・18 通）

**Irrevocable MIT License (MIT-I)** は「MIT を撤回不能にする」という**一点だけ**を扱う提出で、
18 通の議論を受けた。**ACD-1.0 の中核性質（§4.1 の irrevocable・perpetual / §8.1 / §10.4「何も
終了しない」）が、単独の論点として審査された唯一の記録である**（2026-09-07 にアーカイブで読了）。

### ACD-1.0 に有利に働く 2 つの発言

**McCoy Smith（2025-08-14）**:
> **Making a license irrevocable is fine, and many OSI licenses do that** (for example, Apache 2.0)

**Pamela Chestek（2025-08-15）**:
> I hadn't noticed before that the grant in the MIT license isn't perpetual or irrevocable. …
> **all that really would need to be done is insert the words "perpetual" and "irrevocable" in the
> grant language.**
> I believe the standard MIT license is terminable, since it doesn't say it's irrevocable.

**ACD-1.0 §4.1 は逐語でそうなっている** —— *"worldwide, royalty-free, non-exclusive, **irrevocable,
perpetual**, sublicensable, and transferable licence"*。§8.1 の特許許諾も同じ語を持ち、§10.4 が
「いかなる理由でも終了しない・復活条項も無い」と述べる。**委員長が「最小限これをすればよい」と
述べたことを、本文が既に満たしている。**

### 同じスレッドから来る、我々への警告

**McCoy Smith（同日）**:
> The statement that the "copyright holder(s) may not ... **modify** ... this version of the
> Software" **violates OSD 3**. … If what is intended is that **the terms of the license** may not
> be modified, t[hen say so]

**§16.4 は「本文を改変した形を `ACD-1.0` の識別子の下で頒布すること」を禁じている。**
対象は**著作物ではなく文書**であり、§10.5 と §16.6 がそれを明示するが、**この審査者は
「modify してはならない」という語形に反応して OSD 3 を持ち出している**。
`against.md` #101 として記録した —— **指摘は 1 行で出せて、答えは §10.5 → §16.6 → §16.4 の
読み順を辿る必要がある**。#100 と同じ非対称である。

### 結果

提出者は議論の後に取り下げていない（2025-08-28 時点でスレッドは自然に終息）。**承認されていない。**
だが**この提出が失敗した理由は撤回不能性ではない** —— McCoy 氏と Chestek 氏の指摘は
「新しい段落のほとんどが surplusage・循環・悪手」であり、**撤回不能性そのものは "fine" と
明言されている**。ACD-1.0 は撤回不能性を**独立した売りとして提出しない**（§4.1 の一語である）
ので、この論点で争う理由が無い。

---

## 1.48 0BSD に条件を足した提出 —— Modified 0BSD (Maintenance-Required)（2026-03・12 通・却下）

#87 はこれを「条件を足しているので比較対象ではない」として**中身を読まなかった**。
だが**却下の理由**は、我々に効く材料を 3 つ含んでいた（2026-09-07 にアーカイブで読了）。

### 1. 要求情報が無ければ、議論は始まらない —— **2 例目**

**McCoy Smith（2026-03-17）**:
> In order for this license to be considered for approval, **you need to answer all the questions
> set forth in the process for approval**, found here: https://opensource.org/licenses/review-process

2026-09-07 の Carlo Piana 氏（BOS 宛・`against.md` #97）と**同じ反応が、別の審査者から半年前に
出ている**。**これはひとりの流儀ではなく、不完全な提出に対するリストの標準的な第一反応である。**
`submission.md` §B.0 が 11 項目を満たしていることの重みが上がった。

### 2. 「一つの instrument に一つの権利」という立場 —— **我々への生きた反論**

**Rob Landley 氏（0BSD の作者）**:
> **Copyrights, trademarks, patents, trade secrets are all DIFFERENT THINGS.** They are different
> areas of law.
> 0BSD is JUST a copyright license. **If you want to license patents, put a patent license
> alongside it.** If you want to mess with trademarks, add a trademark license alongside it.

**ACD-1.0 は 1 つの文書で著作権・隣接権・データベース権・特許・商標・人格権をすべて扱う。**
この立場を機械的に当てれば、ACD-1.0 は「混ぜている」ことになる（`against.md` #102）。

**答えは §1.5 にある** —— Covered Rights は「著作権・実演・放送録音・sui generis データベース権」
であり、**特許（§8）・商標および名称（§11）・人格権（§12）を明示的に除外して、それぞれ独自の節へ
送っている**。つまり ACD-1.0 は Landley 氏の要求（別々に扱え）を**文書内の別々の節として**
実装している。争点は「別々に扱え」ではなく「**別々の文書でなければならないか**」であり、
**Apache-2.0 が 1 つの文書で著作権と特許（§3）を扱って承認されている**ことが先例になる。

**この反論は軽くない。** Landley 氏は #84（「PD 等価は代替可能なのに、なぜもう 1 つ？」）の
発言者でもあり、**我々の類型について既に 2 つの独立した疑問を公に述べている唯一の人物**である。

### 3. 積極的義務は「現物での対価」に見える —— 我々の設計の裏付け

**Carlo Piana 氏（2026-03-18）**:
> It remains **a positive obligation on which the license is conditioned** … In my view, this is
> **not substantially different from requiring a fee or royalty** for commercial distribution.
> Consequently, it appears to conflict with #1, as the fee or royalty is **in kind**

**§10.1 が条件を一切課さない**ことの外部からの裏付けである。**積極的義務は、それが金銭でなくても
対価として読まれうる。** ACD-1.0 にはその表面が無い。

**結果**: Pamela Chestek 氏が *"IMO this license should be rejected … It is nonsensical."* と述べ、
承認されていない。

---

## 1.51 構造上いちばん近い兄弟 —— UPD 1.5.2（2026-08・`license-discuss`・我々の 19 日前）

**Universal Public Domain License 1.5.2** は、**献呈 + 許諾フォールバック / 単独著者 / 法的レビュー
なし / 2026 年**という、**ACD-1.0 と外形が最も一致する提出**である（本文は `license-discuss`
2026-08 のアーカイブに全文が載っている）。提出者自身が *"solely at my free time **no legal review
has been made**, but i have tried my best"* と書いている。**約 10 時間で 6 通の応答**があった（#83）。

**その 6 通が何を言ったか**（2026-09-08 に原文で読了）。

| 指摘（発言者） | ACD-1.0 |
|---|---|
| **David Woolley 氏**: *"**What alleged defect in CC0 are you claiming to address?**"* | **同じ問いが我々にも来る。** #84（Landley 氏「PD 等価は代替可能。なぜもう 1 つ？」）と Piana 氏の proliferation（#97）に続く**3 例目**で、**この類型の開口一番の問い**である。答えは §6（TDM を積極的に許諾）/ §8.4（モデルと出力に届く特許許諾）/ §9（機械生成物の権利存否に依存しない）—— `submission.md` §B.0 の「The gap」段落がそれ |
| **McCoy Smith 氏**: 「grant」が**対象と無関係なものまで含めて全知的財産権を放棄している | **当たらない。** §1.5 の Covered Rights は **the Work における**権利に限られ、§2.7 が Dedicator の保有する権利に射程を閉じる。**過大な放棄はこの類型の名指しされた失敗モードである** |
| **subham mahesh 氏**: **商標まで放棄している**のは意味をなさない。通常のライセンスは「商標の使用許諾を与えない」と述べるだけ | **当たらない。ACD-1.0 は放棄していない** —— §11.1 は「商標および名称にいかなる権利も与えない」と述べる形で、**まさにここで推奨されている書き方**である |
| **Rob Landley 氏**: PD 等価は **fungible**（代替可能）な唯一の類型で、0BSD がある | #84 の原典。`comparison.md` §1 が両刃で扱っている |

### そして、我々の最大の弱点についての最も鋭い発言

**McCoy Smith 氏（2026-08-07・同スレッド）**:

> Although you say you've "tried your best" without the use of a lawyer, I think if you want to
> propose something that has **any chance of being useable, and approvable**, you'd likely need to
> have the help of a lawyer. **Waivers/disclaimers of IP rights are quite complex, particularly
> given international laws in that regard, and trying to do this on your own isn't likely to result
> in something functional.**

**これは「法的レビューは要件ではない」（Chestek 氏・Berkus 氏・Piana 氏の撤回）と矛盾しない。
だが同じ強さで読まれなければならない。** 委員長と理事が述べたのは**手続き上の要件ではない**
ことであり、McCoy 氏が述べているのは **この類型に限れば実質的にほぼ必要**だということである。
**しかも対象は「waivers/disclaimers of IP rights」で、ACD-1.0 の §3 / §12 / §13 / §14 がまさにそれ。**

**我々の側の反応は「反論する」ではない**（反論できる材料が無い）。
`submission.md` §B.0 は法的レビューの不在を**自分から先に述べ**、§4c が
「弁護士なしで機械的に確かめられること」を列挙する構成になっている。**その構成は正しいが、
McCoy 氏のこの発言は「機械的に確かめられること」の外側にあるものを名指ししている。**
`against.md` #5 / #79 はこの発言で**弱まるのではなく鋭くなる**。

---

## 1.53 PUWL —— 「撤回不能」と「自動終了」を同居させると、献呈ではなくなる（2026-01）

**P-EADCA Universal Waiver License (PUWL)** は `license-discuss` に出された waiver 型の草案。
**Pamela Chestek 氏の返答は 3 行で、しかも致命的だった**（2026-01-27）:

> How can you both "***irrevocably* releases it for unrestricted worldwide use by anyone, for any
> purpose**" and also "**terminate automatically**" against "any party that initiates or threatens
> patent litigation"?
> **This is a license, not a dedication to the public domain.**

**特許報復条項を足した瞬間に、その instrument は献呈ではなくなる。**

**ACD-1.0 はこの矛盾を構造的に持てない** —— §8.2 が
*"This Dedication contains no patent retaliation provision, and **its absence is deliberate**"* と
明言し、§10.4 が「いかなる理由でも終了しない・復活条項も無い」と述べる。**「意図的な不在」と
書いてあるのは、まさにこの指摘を先回りするためである。**

**これで「条件を足すと献呈が壊れる」は 4 例目**（PBZC=コピーレフト混在 / AI-MIT=透明性条件 /
Modified 0BSD=保守義務 / PUWL=特許報復）。**4 件とも承認されていない。**

---

## 1.54 AIAL v2（旧 AI-MIT）—— 「1 つの文書で 3 つのことをやろうとしている」

AI-MIT は 2026-03 に撤回されたあと、**AIAL v2 として `license-discuss` で議論が続いた**
（`comparison.md` §1.45 は撤回までしか記録していなかった）。

**Pamela Chestek 氏（2026-03-29）**:
> It seems that you are trying to do **three different things with one document**: (1) create a
> system for identifying the **provenance** of code, (2) apply a **license** and (3) optionally state
> that someone is **waiving a claim to copyright** they might have. I don't see any reason why
> purpose (1) is tied to purposes (2) and (3)… **Doing (2), and (3) optionally in the same document,
> is unnecessarily complicating things.**

**この批判は ACD-1.0 にも向けられうる**（`against.md` #105）。ACD は献呈（§3）・許諾（§4）・
不行使の合意（§5）・TDM の言明（§6）・データベース権（§7）・特許（§8）・機械生成物についての
言明（§9）・人格権（§12）・文書についての規則（§16）を 1 文書に持つ。

**ただし Chestek 氏が束ねるなと言ったのは「来歴の識別システム」という*非法的・情報的*な目的**で
あり、**ACD の各節はすべて同一の Work についての法的機構**である。最も近いのは §9 だが、
**§9.2 は「表明しない」という法的態度**であって情報システムではない。**この区別は主張できるが、
主張しなければ通らない。**

**Bruce Perens 氏（2026-03-19・同スレッド）—— 我々に有利な形で効く警告**:
> our community, in general, greatly **over-estimate the power of licenses and are unaware of the
> limits of copyright** … They are surprised when companies blithely ignore their overestimations …
> And of course they are liable to be **let down in court** if they try to en[force it]

**ACD-1.0 は逆をやっている** —— §9.2 は機械生成物に著作権が生じるか否かについて**何も表明せず**、
§13.2 は「いかなる権利が存在することも保証しない」と大文字で述べる。**過大評価の反対側に立つ
設計であることは、この警告に照らして初めて説明しやすくなる。**

**Stefano Maffulli 氏（2026-03-30）**: *"multiple things you're trying to achieve and **not all of
them (if any) can be solved with a copyright license**"* —— AI 学習への選好の signalling は
ライセンスでは解けない、という指摘。**ACD-1.0 は §6.2 で TDM の留保を*しない*と述べており、
signalling をライセンスでやろうとしていない**（`research-application-policy.md` §3C が
IETF AIPREF を採らない理由と同じ向き）。

---

## 1.57 Unlicense への「veto」（2020-04〜06・49 通）—— 否決の論拠と、それを条文にした ACD

**Lukas Atkinson 氏は PBZC の審査（2024-12）で、我々の類型の新規提出者にこう求めた** ——
*"I would be very happy if new licenses/dedications/devices in the 'PD dedication' or 'PD
equivalent' category **make use of this wealth of prior discussions (well over a decade)** and
avoid running into the same problems."*

**その "wealth" の中心が、2020 年の Unlicense legacy 承認に対する veto スレッド（49 通）である。**
ドシエは §3.9 でこの窓を「読了」としていたが、取り出していたのは **2 つの結論だけ**だった
（「dedication *taken alone* は承認されない」「lawyers both US and non-US が一致した」）。
**論拠そのものは読んでいなかった**（2026-09-08 に読了）。

### veto 側の論拠（Thorsten Glaser 氏）

> It is very much not clear, and we have rejected licences with less ambiguous reading.
> **No, it does not meet the definition of "licence".**

> it's not just about what a court would think, it's just as much about **promising to my (as a
> distributor) downstreams that the stuff I take from upstream is under a good licence**.
> This one is clearly not good and almost certainly not a licence.

> [「訴えられない」に対し] **Wrong, at least for the part of the world not USA.**

### 承認へ至った側の論拠（Pamela Chestek 氏）

> Even though the person using this document … may be mistaken about the concept of public domain,
> **the intent of the grantor is very clear** … For this document to not meet the definition of
> "open source," a court would have to say that there is no such thing as "public domain" in the
> jurisdiction … **the court will then have to ignore what the person thinks it means as clearly
> described in the document, reaching a conclusion that the document is entirely meaningless**…
> That is not something that would happen in a US court.

> a court might hold that, **in the absence of an effective dedication to the public domain, a user
> would not have a defense to a claim of infringement based on the clear statement of the uses the
> author has identified in the document as permitted**.

**McCoy Smith 氏**:
> And (d) the assertion that this passage … **is not a license. Because if that's true, MIT and BSD
> are also not licenses.**

### ここが ACD-1.0 にとって決定的である

**Unlicense を承認へ運んだ論拠は「献呈が無効でも、列挙された許諾が許諾として働く」である。**
そしてそれは **Unlicense の条文に書かれていない** —— 弁護士がその読みを**論証した**のである。

**ACD-1.0 §4.4 はそれを条文にしている** ——
§4 の許諾は **§3 とは独立に付与され、§3 が無効であることに依存しない**。
つまり **受領者も裁判所も、§3 の有効性を判断する必要がない。**

**veto の中心は「不明確である」だった。§4.4 はその不明確さそのものを取り除いている。**
これは「なぜもう 1 つ PD 等価が要るのか」（#84 / #97 / §1.51）への、**最も具体的な答え**である ——
**前のものは弁護士が論証しなければならなかったことを、こちらは書いてある。**

### 不利な側（同じ強さで）

**Glaser 氏の「頒布者の下流への約束」論は、§4.4 では完全には解けない。** §4.4 は
「受領者は §3 の有効性を判断しなくてよい」を与えるが、**再頒布者が下流に対して負う説明の
負担**は、instrument が新しいぶんむしろ重い（0BSD や MIT なら名前だけで通る）。
**#84 の「代替可能性」と同じ根**であり、`comparison.md` §1 が両刃で扱っている。

**そして「Wrong, at least for the part of the world not USA」は今も生きている。**
Chestek 氏の擁護は明示的に **US の裁判所**についてのものだった。§12 / §15.4 / §4.4 の
多段構成はそこへの対処だが、**法的レビューを経ていない**（#5 / #79 / §1.51）。


---

---

## 1.63 名前そのものが審査対象である —— 0BSD の改名スレッド（2018-10・54 通）

**我々は「なぜもう 1 つ作るのか」（#84）を 0BSD との比較で何度も論じてきたが、
0BSD が OSI で経験した唯一の審査は承認ではなく「改名」だった。** そして、その 54 通は
**ライセンスの名前が実際に議論の対象になる**ことを示している。

### 何が起きたか

同一のテキストが **Free Public License 1.0.0** と **Zero Clause BSD (0BSD)** の 2 つの名前を
持ち、OSI のページは前者を正式名として掲げつつ *"There is a license that is identical to the Free
Public License 1.0.0 called the Zero Clause BSD License."* と注記していた。Rob Landley 氏が
改名を求め、**承認後の改名は OSI にとって前例が無かった**（Richard Fontana 氏・2018-10-15:
*"As far as I know this would be the first time the OSI has changed the reference name of an
OSI-approved license, post-approval."*）。

**名前は merits で争われた。**

> **Josh Berkus 氏**: I'm still not keen on calling anything "BSD" that has no historical
> relationship to Berkeley… **We should not be in the business of approving license names that
> deceive users. -1 from me.**

> **Simon Phipps 氏**: I share this concern. **BSD is not related to the license author's trademark**
> as far as I am aware.

> **Richard Fontana 氏**: one problem with the "Zero Clause BSD" name is that **the license is not
> textually based on any version of the BSD license** — rather, it is an alteration of the ISC
> license… **I do not think it's OSI's job to help with adoption of particular licenses.**

最終的に rough consensus で改名され、Berkus 氏は棄権した（*"Not going to stand in the way of
rough consensus… Abstain."*）。手続きの記録として: **Simon Phipps 氏（当時 OSI President）**
*"the Board will vote on it when consensus emerges and the discussion quiesces."*

### ACD-1.0 に効く 3 点

**(1) 名前は審査される。** ドシエは条文を隅々まで敵対的に読んできたが、
**「Autonomous Commons Dedication」という名前そのものを一度も検査していなかった**（#112）。

**(2) 名前が「どちらか一方」を宣言している。** #110 で記録したとおり、委員長は
*"Which is it, a dedication to the public domain or a license? You can't have it both ways."*
と問う。**我々の名前は "Dedication" と言い切っている** —— 一方 §4 は licence であり、
§4.4 は独立の許諾だと述べる。**反論が来る前に、名前の側で片方に賭けてしまっている。**

**(3) 名前を変える余地が構造的に無い。** §16.4 が名前と識別子を「1 つの固定テキストを指す」
ものとして本文の側から縛り、Check 453 がその本文を pin する。**改名は別の instrument を作ること
と同じ**である。0BSD は承認**後**に改名できたが、それは前例が無く rough consensus を要した。

### 「Commons」と「Dedication」—— 主張ではなく実測（SPDX License List 3.28.0・2026-09-09）

2018 年にリストが反対した形は「**その名前が想起させるものと、実際の由来が一致していない**」で
あった（BSD の名を持つが ISC 由来のテキスト）。**では我々の名前は何を想起させるのか。**
**主張せずに数えた** —— SPDX License List の **727 件**（うち OSI 承認 149 件）を機械で走査した。

| 実測 | 結果 |
|---|---|
| 名前に **"Commons"** を含む | **58 件。内訳は Creative Commons **55**、Open Data Commons **3**。**それ以外は 0 件** |
| 名前に **"Dedication"** を含む | **2 件のみ** —— `CC-PDDC`（Creative Commons Public Domain Dedication and Certification）と `PDDL-1.0`（Open Data Commons Public Domain Dedication & License）。**どちらも OSI 承認ではない** |
| 識別子 `ACD-1.0` / `ACD` / `LicenseRef-ACD-1.0` | **いずれも未使用**（OSI の review-process が求める *"unique name"* を、識別子の側では満たす）|
| 名前の衝突 | 無し。最も近いのは `CAL-1.0`「Cryptographic **Autonom**y License」で、語幹を共有するだけである |

**この 4 行が言うこと。**

1. **"Commons" はこのリストでは一般語として使われていない。** 58 件すべてが 2 つの組織
   （Creative Commons / Open Data Commons）の名前である。**"commons" が
   "tragedy of the commons" のように CC より古い一般語であることは事実だが、
   *SPDX の名前空間では* 例外なく組織標識として使われている** —— この区別を落とすと、
   自分に都合よく読むことになる。**これは #112 の懸念を、主張から実測へ変える。**
2. **`PDDL-1.0` は "Public Domain **Dedication & License**" と名乗っている。**
   委員長が *"You can't have it both ways"* と言った当の組み合わせを、**名前の中で明示している
   既存の instrument が在る**（#110 / #1.61）。**先例が無いわけではない。**
3. **ただしその 2 件はどちらも OSI 承認ではない。** *"Dedication" を名前に持つ OSI 承認
   ライセンスは 0 件である。* **ここには読み方の但し書きが要る** —— CC0 の SPDX 名は
   「Creative Commons Zero v1.0 Universal」で "Dedication" を含まないが、**中身は献呈である**。
   つまりこの 0 件は**命名の慣行の反映**でもあり、承認可能性そのものの指標ではない。
4. **識別子は空いている。** #108（REUSE 適合名 `LicenseRef-ACD-1.0`）が指す名前も未使用である。

**なお言えないまま**: 「Commons」が商標上の問題かどうか。**判断には弁護士が要る**（弱点 1）。
**近いことと問題であることは別**である。ここで増えたのは、**近さが実測になった**ことだけである。

---

## 1.66 同じ日に、同じ窓口へ、正反対の形の提出が出た —— PSF-2.0（2026-09-09）

**比較できるのは形だけだが、その形が我々の弱点と正面から対応している。**

### 何が出されたか

**Max Mehl 氏**が `license-review` へ **PSF-2.0**（Python Software Foundation License 2.0）を
提出した。**約 270 語**。構成は ——

| 含まれるもの | 含まれないもの |
|---|---|
| 名称と SPDX 識別子 | **OSD の逐条的な言明** |
| 本文の text part 添付 | **提案する tag** |
| steward の特定（**本人ではなく代理**。PSF に資力が無いと明記）| **法的レビューの有無** |
| **採用実績 3 プロジェクト**（Jython / cx_Freeze / PDFeXpress）| **既存で埋まらない gap** |
| 既承認ライセンス（Python-2.0.1）との関係 | **最近似の承認済ライセンスとの比較** |

そして *"I hope to have provided **all required information**"* と書いている。

### 我々にとっての意味 —— 2 通りに読めて、両方書く

**(1) 形の完全さでは我々が上回る。** #97 で足した項目（OSD 3/5/6/9 の名指し / ScanCode 識別子 /
提案 tag）は、**同日の、直前の提出が承認された経験者の提出には無い**。
**我々のパケットは、今日この窓口に出された提出より完全である。**

**(2) だが完全さの尺度は類型で違う。** PSF-2.0 は数十年使われ、既承認ライセンスの構成要素で
ある。**gap / 比較 / 法的レビューの問いは、そもそも生じない。** 彼が依っているのは
**採用実績**と**先例**で、**我々にはどちらも無い**（#2 / #113）。

**この 2 つを並べると、リストを通る道が 2 本あることが見える。**

| 道 | 依るもの | 我々 |
|---|---|---|
| A | **テキストが正しいこと** | **これしか使えない** |
| B | **既に使われていること** | 採用 1 件 —— 使えない |

**#113（「法的レビューか、相当の実使用か、どちらか」）はこの構造の言い換えである。**
Mehl 氏は B で通り、我々は A で通すしかない ——**そして A は、B より遅く、より厳しく読まれる。**

### establish しないこと

- **「短くてよい」の証拠ではない。** 彼が短く書けるのは、**長く説明すべきことが無いから**である。
- **彼の提出が承認される保証も無い**（本節は形の観測であって結果の予測ではない）。
- **同日という一致は偶然である。** 1 件の同時代例から傾向を読まない（#109 の教訓）。

## 1.67 委員会が実際に述べた「承認しない／受け入れる」規則の全数（2024-01〜2026-09）と、ACD-1.0 の当たり方

**方法**: `license-review` の 2024-01〜2026-09（33 か月・804 通・111 スレッド）を取得し、
**引用行を除いた本文**から `OSI will/does not approve` / `OSI will accept` / `OSI requires` /
`cannot be approved` の形を全数抽出した。**名称検索ではなく形の全数列挙である**（#87 / #99 の
「名前で数えると母集団を数えたことにならない」を避けるため）。**得られたのは 5 件**で、
うち 4 件は Licensing Committee 委員長（Pamela Chestek 氏）の発言である。

| # | 述べられた規則（逐語） | 出典 | ACD-1.0 の位置 |
|---|---|---|---|
| R1 | *"OSI **requires prior review by a lawyer** because there are things that a layman very likely cannot consider, not just to enrich lawyers (who mostly do this job **pro bono**, as we are doing now)"* | Carlo Piana 氏・2024-12-18・PBZC スレッド。**"in his own capacity" と自ら明記している** | **⚠ 我々に不利で、しかも既存の記述と食い違う。** B1 は委員長の *"recommended … not a blocker"*（同じ 2024-12 の PBZC スレッド）と Berkus 理事の同趣旨（2025-05）に依っている —— **同一スレッドの中で、2 人の OSI 関係者が期待値を別の言葉で述べている。** 我々の disposition は変えない（委員長は委員会として述べ、Piana 氏は個人の資格と明記している）が、**この逐語を B1 の隣に置かずに「recommended だ」とだけ書くのは、有利な側だけを引くことである** |
| R2 | *"OSI will not approve licenses that are **not self-contained** because of the high likelihood that the added content will not comply with the OSD or OSAID"* | Chestek 氏・2025-02-14・MGB 1.0（annex を許す構造への指摘） | **通る。実測: ACD-1.0 本文に外部参照は 0 件**（`http` / `annex` / `available at` / `incorporated by reference` のいずれも 0）。**付属文書も、後から差し替わる余地もない** |
| R3 | *"The OSI **will not approve a license that attempts to describe which claims are licensed and which are not by what type of rights the user is exercising** - they must be allowed to exercise them all"* | Chestek 氏・2025-02-14・MGB 1.0。MGB は特許許諾を「再現・派生に必要な範囲」に限っており、**ソフトウェアを実行するだけの人に許諾が届かない**ため OSD 6 違反と判断された | **当たらない。** §8.1 の限定は**行使する権利の種類**ではなく **Work との関係**である —— *"every patent claim … that would be infringed by making, having made, **using**, offering to sell, selling, importing, or otherwise transferring the Work"*。**"using" が入っているので、実行するだけの受領者にも届く**（MGB が落ちた当の点） |
| R4 | *"The OSI **will accept** a patent grant that is limited to only the claims that are **necessarily infringed by the patentee's contribution** (alone or in combination with the preexisting software) and temporally limited to only what was granted at the time of the contribution"* | 同上（R3 の直後・**受け入れる形を名指しした唯一の発言**） | **この形に一致する。** §8.1 末尾は *"where the infringement is caused by subject matter contained in the Work as made available by the Dedicator"* ——**寄与によって必然的に侵害される請求項に限る**という同じ限定である。**ただし ACD は時点による限定を置いていない**（*"now or in future"*）—— これは受け入れ条件より**広い**方向の差であり、狭い方向の差ではない |
| R5 | *"OSI will not approve licenses where the **title refers to a particular person, entity or software** or that have them 'hard coded' into the license (see **'Standard for New Licenses' para. 1**)"* | Chestek 氏・2026-04-18・CNPL-1.0（名称に "CompanioNation" を含むことへの指摘） | **通る。** 名称に人・団体・ソフトウェアの名は無く、**本文の固有名詞は 0 件・置換テキストも 0 件**（`submission.md` §4b の実測）。**B6 が扱っているのは別の懸念**（"Commons" が CC/ODC の house mark と衝突しうること）で、**この規則そのものには当たらない** |

**同じ 2026-04-18 の CNPL への指摘には、規則の形をとっていないがもう 1 つ重要な点がある**:
*"The license does not grant all the rights under copyright, at least under US law. US law also
includes the right to **publicly perform and publicly display** … it is also **better practice not
to define the grant by enumerating specific rights**, since those may be country-specific."*
**ACD-1.0 はこの指摘の両方に対して逆側に立っている** —— §4.1 は列挙ではなく
*"all Covered Rights in the Work for any purpose whatsoever"* という**範囲による許諾**で、
§4.2 は *"includes, **without limitation**"* と明示したうえで
**"publicly display, publicly perform" を実際に含んでいる**。

**この節が意味すること（過大に読まないための注記）**: **R2 / R3 / R5 に「当たらない」ことは、
承認されることを意味しない。** これらは**失格の形**であって合格の条件ではなく、我々の 2 大弱点
（B1 法的レビュー・B2 実使用）はここでは 1 つも解消していない。**それでも記録する理由は 2 つ**
——**(a)** これまでドシエは「我々は OSD に適合すると考える」という**自分の推論**を積んでおり、
**委員会が実際に口にした規則に対して当てた記録が無かった**。**(b)** R1 は不利であり、
**探して見つかったのが有利な 4 件だけだったのではないことを、同じ表の中で示す必要がある。**
