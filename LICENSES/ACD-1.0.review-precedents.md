---
file: LICENSES/ACD-1.0.review-precedents.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-09-09
canonical-ref: LICENSES/ACD-1.0.comparison.md (条項レベルの比較はこちら) / LICENSES/PEER-REVIEW-WATCH.md (手続きの観測) / LICENSES/AS-OF.md (日付つきの外部事実)
---

# 審査の記録から読み取ったこと —— ACD-1.0 に当たる指摘と、当たらない指摘

**この文書は `ACD-1.0.comparison.md` から 2026-09-08 に切り出した。** 節番号は変えていない
（切り出し時点で `§1.45`〜`§1.50`、現在は下の目次のとおり）ので、既存の参照はそのまま解決する。

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


## 1.49 人格権 —— リストの日本人参加者が 2024 年から押している論点で、§12 はその答えである

**ACD-1.0 §12 は、ドシエの中で「なぜこんな条項があるのか」が最も説明を要する節だった。**
アーカイブを人格権で走査したところ（2026-09-08）、**この論点はリスト上で 2024 年から
繰り返し提起されており、しかも提起しているのは日本の参加者である**ことが分かった。

### 何が言われているか（原文・発言者・日付）

**Shuji Sado 氏（2024-09・`license-review`）** —— Blue Oak Model License について:

> In March, I pointed out that the Blue Oak Model License does not consider moral rights.
> **The consensus in this thread was that, for software programs, not considering moral rights is
> not an issue in most jurisdictions worldwide, but it can be a problem in East Asian countries,
> particularly in Japan.**

> …after discussions with multiple legal department members who hold law degrees, it was determined
> that **in Japan, the Blue Oak License retains moral rights with the authors, posing a risk that
> usage could be stopped at any time. This cannot be considered an Open Source Data license.**

> In the case of the Apache 2.0 License, it explicitly states "copyright license," but it also
> grants irrevocable permission for acts such as reproduction, distribution, and modification.
> **This is interpreted as a declaration that moral rights will not be exercised.**

> I recently learned that **Japan applies moral rights most strictly among countries**.

**Carlo Piana 氏（2023-11）—— 反対の見方**:

> On the moral rights, mind that **these are not licensable**, so anything the license says one way
> or the other, nothing changes. I take the opinion that moral rights are probably not relevant in
> software as they are in creative…

**別の参加者（2023-11・Blue Oak を論じて）**:

> **The CC0 mechanism (promise not to exercise or assert any remaining rights) seems much clearer.**

### §12 がそれぞれにどう答えるか

| 論点 | ACD-1.0 |
|---|---|
| 日本では人格権が著作権と別個で、**最も厳格に**運用される。触れないライセンスは「いつでも利用を止められる」risk を残す | **§12 が正面から扱う唯一の節である。** §12.1 が放棄可能な範囲で放棄し、§12.2 が**放棄不能な法域では不行使の合意**を置く |
| 人格権は **licensable ではない**（Piana 氏）ので、条項は無意味ではないか | **§12.2 は許諾ではなく covenant（不行使の合意）である。** 「譲渡・放棄できない権利」でも「行使しないと約束する」ことはできる、という区別に依っている。Piana 氏の指摘は**放棄構成（§12.1）にだけ当たり、covenant 構成（§12.2）には当たらない** |
| CC0 の「残る権利を行使しないと約束する」機構のほうが明確だ | **§12.2 はその機構である**（§5 の covenant not to assert と同じ設計）|
| Apache-2.0 は「不可逆の許諾」を人格権不行使の宣言と**解釈で**読ませている | **ACD-1.0 は解釈に依存しない** —— §12 が明文で述べる。**日本法の下で最も強い形は、解釈ではなく明文である** |
| 人格権は**著者の死後も存続**し、遺族や公的機関が行使しうる | **§12.4 がそこまで縛る**（承継人・相続人・遺言執行者・死後に行使しうる者）。**この節の存在理由は「最も長く残る risk」である**と条文自身が述べている |
| 人格権が守る「氏名表示を偽られない利益」まで放棄させるのか | **§12.5 が明示的に留保する**（§11.3 の虚偽表示は covenant の外）。**放棄しない部分を書いてある** |

### 我々にとっての意味

1. **§12 は思弁ではなく、リスト上の実際の未解決論点への回答である。** しかも
   **提起者は日本の参加者で、Dedicator も日本にいる。**
2. **不利な側も同じ強さで書く**（`against.md` #104）—— Piana 氏の「人格権は licensable でない」は
   §12.1 への有効な批判であり、**§12 全体が無意味だと読まれる余地がある**。答えは
   「§12.2 は許諾ではなく covenant」だが、**それは条文を読ませて初めて通る答え**である。
3. Sado 氏の基準（人格権を扱わないものは「Open Source Data license とは言えない」）は**高い**。
   ACD-1.0 はその基準の正しい側に立つが、**基準が存在すること自体は覚えておく**。


## 1.50 「著作権だけでは足りない」—— #102 と正面から対立する 3 つの発言

#102（Rob Landley 氏「一つの instrument に一つの権利。特許を許諾したいなら**別のライセンスを
並べろ**」）は、我々の構造への最も直接的な反論である。**同じアーカイブに、逆向きの発言が
3 つある**（2026-09-08 に走査して発見）。

**Pamela Chestek 氏（2025-03・ModelGo 審査・当時 OSI Licensing Committee）**:
> 2.5(a) — you have **reserved rights that may be needed for someone to exercise the full grant
> required for an open source license**, in particular because you expressly aren't granting rights
> in database. **One theory for the protection of models is database rights, so you might have
> unintentionally withheld the right to reproduce the Model.**

**Carlo Piana 氏（2023-01）**:
> The only rights the license mentions are under Copyright … There is **no mention of other
> controlled rights necessary to use of the software, such as database rights or patents**.
> Suppose I am a patent holder of a work of mine and I license said work under this license.
> **Can I later go after my licensees under the patent regime**…?

**Carlo Piana 氏（2023-07）**:
> …**pure copyright licenses excluding all other rights**, therefore at least the non-patent
> licenses **do not meet the OSD**, since they expressly carve out patents

### 何が対立しているのか

| Landley 氏（#102） | Chestek 氏・Piana 氏 |
|---|---|
| 権利の種類ごとに**別の instrument** を並べよ。0BSD は著作権だけのライセンスである | 著作権だけに届く許諾は、**受領者が実際に必要とする権利を留保してしまう**。とくに**モデルはデータベース権で保護されうる**ので、それを許諾しないと**モデルを複製する権利を意図せず withheld している** |

**両者は「別々に扱え」と「1 つの文書に入れろ」で対立しているのではない。**
Landley 氏が言っているのは**文書を分けろ**であり、Chestek 氏・Piana 氏が言っているのは
**取りこぼすな**である。**ACD-1.0 は両方を満たす形になっている** ——

- **取りこぼさない**: §1.5 の Covered Rights が著作権・実演・放送録音・**sui generis データベース権**
  を含み、**§7 がデータベース権を独立に扱い**、§8 が特許、§12 が人格権を扱う。
- **混ぜない**: §1.5 は特許・商標・人格権を **Covered Rights から明示的に除外**して、
  それぞれ §8 / §11 / §12 へ送る。**種類ごとに節が分かれている。**

**残る争点は 1 つだけ**: 「別々」は**別の文書**でなければならないか、**別の節**でよいか。
Apache-2.0 は 1 文書で著作権と特許（§3）を扱って承認されている。**この 1 点に絞れば議論は短い。**

### ACD にとっての含意（有利・ただし条件つき）

**AI モデルにデータベース権が効きうる、という指摘は、我々の §7 が存在する理由そのものである。**
しかも指摘者は Licensing Committee の委員長で、**別の AI ライセンス提出者に対して
「モデルの複製権を意図せず留保している」と述べた**。ACD-1.0 はその失敗をしていない。

**条件つきである理由**: これは「§7 があってよかった」を示すが、**§7 の書き方が正しいことは
示さない**。データベース権は EU 由来の制度で、法域ごとに存否も範囲も違う。
§7 の妥当性そのものは依然として法的レビューを受けていない（#5 / #79）。

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

## 1.52 「弁護士が要る」への実務的な答えは、審査そのものである

§1.51 の McCoy 氏の発言（この類型で弁護士なしは *"isn't likely to result in something functional"*）は
**我々に反論の材料が無い**指摘だった。**だが同じアーカイブに、その指摘の実務的な帰結が書いてある。**

**Carlo Piana 氏（2024-12・PBZC 審査）**:
> OSI requires prior review by a lawyer because there are things that a layman very likely cannot
> consider, not just to enrich lawyers (**who mostly do this job pro bono, as we are doing now**).

**Carlo Piana 氏（2024-09・別の提出者へ）**:
> I second the opinion that you should probably withdraw the submission and consider the valuable
> advice you have been provided with (**for free**).

**Josh Berkus 氏（2025-07・BOS の提出者へ・OSI Board Member として）**:
> We are approaching 2 months from the submission of this license, **our usual interval for
> examination**. You've received some critical feedback from **our volunteer attorneys**. Do you
> plan to revise the license submission, or keep it as it is?

### 読み取れること 3 点

1. **このリストの審査者は、pro bono で働く弁護士たちである。**（Piana 氏の "as we are doing now" は
   自分自身を含めた記述である。）**単独・無資金の起草者が条文に弁護士の目を通す実務的な経路は、
   提出することそのものである。** McCoy 氏の指摘への答えは「反論」ではなく**「その通りであり、
   だからこそ提出する」**である。
2. **ただしこれは「弁護士が起草した」とは違う。** 受けられるのは**起草の代行ではなく批評**で、
   しかも**提出後**にしか来ない。`submission.md` §B.0 が法的レビューの不在を先に述べるのは、
   この順序を偽らないためである。
3. **審査の標準的な間隔は約 2 か月**で、その時点で **「改訂するのか、このまま行くのか」を
   聞かれる**。オーナー方針（届いた議論を全部取り込んで改訂版を出す）は、
   **この問いに対する答えとして既に用意されている**（`REVISION-PROTOCOL.md` §1〜§2）。
   **聞かれてから考えるのではなく、聞かれる前から決めてある**ことがこの track の設計である。

**この節が establish しないこと**: pro bono の批評を受けられることは、**批評が好意的である
ことを意味しない**（§1.51 の McCoy 氏の発言自体がその批評である）。また、
**批評を受ける前提は「要求情報を満たした提出」**であって、満たしていなければ
コメントは付かない（#97・Piana 氏 2026-09 / McCoy 氏 2024-10・2026-03 の 3 例）。

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

## 1.55 非ソフトウェア資産と AI エージェントの「スキル」—— 我々が実際に配っているもの（2026-04）

ACD-1.0 は**リポジトリ全体**（ソース・文書・データ・メディア資産、そして
`.well-known/` の **Agent Skills**）に適用されている。**その適用形態そのものが議論された
スレッドがある**（`license-discuss` 2026-04・Moming Duan 氏の問題提起）。

**問い**: スキル（AI コーディング支援への指示セット）に明示的なライセンスは要るのか。
そもそも著作物なのか。米国著作権局は「プロンプトだけでは十分な人的支配を与えない」と結論して
いるのではないか。従来の OSS ライセンスは適切なのか。

**Richard Fontana 氏（Red Hat・2026-04-06）の回答が 3 点とも我々に効く**:

> "Instructions" **can be copyrightable works**. I think at least some skills files are likely
> copyrightable.

> The document does not state that. Rather, it says that **prompts alone do not provide sufficient
> human control over AI-generated *outputs*** to confer human authorship and thus copyrightability
> **over the outputs**. It references [Part 2] that appears to endorse the view … that
> **sufficiently creative prompts may be copyrightable**.

> it's already the case that **open source software licenses are extensively used for non-software
> material** in open source project repositories. My general view is that **traditional open source
> software licenses are completely appropriate** for association with such material if they are
> copyrightable.

### 我々にとっての意味

1. **「ソフトウェア用のライセンスを非ソフトウェア資産に当てている」ことは、この場では異常では
   ない。** Fontana 氏が *"extensively used"* かつ *"completely appropriate"* と述べている。
   **ただし Carlo Piana 氏（2023-07）は逆に近いことを述べている** —— *"the only non-software
   specific licenses we approve are those bearing a total waiver of any right so that the work
   becomes nearly public domain"*。**両方を記録する** —— そして**その「total waiver に近いもの」は
   ACD-1.0 の形そのもの**なので、2 つの見解は我々については同じ結論へ収束する。
2. **§9 が navigate している区別を、この場の第一人者が正確に述べている** ——
   **プロンプトは著作物たりうる / そこから生成された出力は人的著作性を欠きうる**、は別の命題である。
   **§9.2 が「表明しない」のは、この区別が未確定だからであって、不勉強だからではない。**
   **よくある誤読（「著作権局はプロンプトは著作物でないと言った」）を、Fontana 氏がその場で
   訂正している** —— 我々もその誤読を繰り返してはならない。
3. **我々が配っている Agent Skills は、この議論の対象そのものである。** ACD-1.0 を
   リポジトリ全体に当てるという選択は、**この論点に対する 1 つの答え**になっている
   （スキルが著作物なら許諾が及び、著作物でないなら許諾は無害である —— §2.7 が
   「Dedicator が保有する権利」に射程を閉じているので、**どちらでも壊れない**）。

## 1.56 我々の投稿の 1 つ前のメッセージが、我々のやっていることを標準化していた（2026-08-25）

**アーカイブ上、我々の 2026-08-26 の投稿の直前にあるのは Matija Šuklje 氏のこのメッセージである**
（同じリスト・前日）。**クライアントサイドの JavaScript / CSS に著作権とライセンス情報を
どう載せるか**について、*"after several workshops and iterations, **a bunch of us finally agreed
to a solution**"* として 4 段の手順を示している:

1. **REUSE.software のベストプラクティスを適用する**（他の言語と同じように）
2. **SBOM（SPDX / CycloneDX）か attribution file を、好きなツールで生成する**
3. **その file/page を `<head>` の `<link rel="license" href="">` で指す**
4. **web UI にも `<a rel="license" href="">` で提示する**

### 我々が満たしているもの / いないもの（2026-09-08 実測）

| 手順 | 本リポジトリ |
|---|---|
| 3. `<head>` の `<link rel="license">` | **満たす** —— `index.html:403`（Check 444a が BLOCKING で強制）|
| 4. UI 内の `<a rel="license">` | **満たす** —— `js/components.js` の sidebar/drawer 共通部（`rel="license noopener noreferrer"`）|
| 1. REUSE のファイル単位ヘッダ | **満たさない** —— shipped の HTML / CSS / JS に `SPDX-License-Identifier` ヘッダは **1 つも無い**（`against.md` #106）|
| 2. SBOM / attribution file | **問題自体がほぼ生じない** —— C1（Boring Technology・外部フレームワークとライブラリ **ゼロ**）により、**配信物に第三者コードが含まれていない**。この手順が解こうとしている「束ねられた minified ライブラリのライセンス情報が失われる」問題が、この配信物には存在しない |

### 3 つの観察

1. **手順 4 は 2026-09-06 に #85 として独立に実装した。** その時点でこのスレッドは読んでいない。
   **「機械にだけ伝えて人間に伝えていなかった」という自分の発見が、10 日前にリスト上で
   合意されていた解決策と一致した。** —— 収束は嬉しいが、**先に読んでいれば 10 日早かった。**
2. **手順 2 が我々に当たらないのは、アーキテクチャの選択（C1）の帰結である。**
   これは「やらなくてよい」ではなく「**問題が生じない構造にしてある**」という主張なので、
   **主張として書いておく必要がある**（黙っていると「SBOM が無い」とだけ見える）。
3. **手順 1 は素直に未達である。** ドシエは機械可読なライセンス宣言を強みとして述べている
   （6 面の cross-surface coherence を Check 444 が強制）が、**REUSE は「面」ではなく
   「ファイル単位」の標準**で、そちらは 1 つも無い。**強みを主張している領域の、名指しできる欠落。**

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

## 1.58 「OSD 違反ではないが、採用されるかは別問題」—— 特許条項の広さが uptake を下げるという指摘

**ACD-1.0 §8 が最も広い形を取っている当のことについて、審査者が名指しで懸念を述べた記録がある。**
これは我々が**差別化として提示している箇所**（§8.4）に当たるので、同じ強さで書く。

### 原文（McCoy Smith 氏・`license-review` 2026-05-14・ModelGo 宛）

> Finally, the termination provision for patent assertions applies to Derivative Works. There's a
> long-standing debate about whether that sort of termination is overbroad… One of the reasons why
> the newer, popular licenses articulate their defensive termination/suspension clauses more
> narrowly than this is because of the concern that **patent holders would be reluctant to grant an
> open-ended patent license to downstream licensees**. **I don't think that's an OSD violation, but
> it is an issue as to whether a license of this scope would gain significant uptake at least from
> patent holders.**

**同じ人物が 2026-09-07 の CALL FOR COMMENTS で、これを 4 問中 2 問に組み直している** ——
Q3（終了が Licensor にしか向かない非対称は OSD 5 の問題か / 特許主張が著作権の許諾まで終わらせてよいか）と
Q4（引き金が Derivative Materials にまで及ぶのは広すぎないか。*"Most of the OSI-approved licenses
that have patent assertion termination clauses limit them to assertions against the licensed work,
not subsequent derivatives."*）。**1 年 4 か月にわたって同じ論点が生きている。**

### ACD-1.0 に当たるか —— 二段に分けて答える

**当たらない部分（形式）**: ACD-1.0 には**特許報復条項が存在しない**。§8.2 は
*"This Dedication contains no patent retaliation provision, and its absence is deliberate."* と
明言し、§10.4 は何も終了しない。**Q3・Q4 が問うている条項が無いので、その問いは当たらない。**

**当たる部分（実質）**: McCoy 氏の懸念の中身は終了条項そのものではなく、
**「特許権者は、下流の受領者へ開放的な特許許諾を与えたがらない」**である。
その尺度で見ると **ACD-1.0 は ModelGo より広い** ——

| | ModelGo Attribution 2.0 | ACD-1.0 |
|---|---|---|
| 特許許諾の範囲 | Licensed Materials とその派生 | Work とその派生（§8.1）**＋ 訓練済みモデル・パラメータ・出力**（§8.4）|
| 取り戻す手段 | 特許主張があれば終了できる | **無い**（§8.2 が明示的に無条件・終了不能と述べる）|

**つまり我々は、McCoy 氏が「uptake を下げる」と述べた方向の極限に立っている。**
差別化として提示している §8.4 は、**その尺度では最も採用されにくい形**である。

### これが establish すること / しないこと

- **establish する**: 承認の障害ではない。McCoy 氏自身が *"I don't think that's an OSD violation"*
  と述べている。**OSD 適合と採用可能性は別の軸である。**
- **establish しない**: 「だから ACD-1.0 は採用されない」。彼が述べたのは**特許権者からの**
  採用についてである。同じスレッドで Moming Duan 氏が反対側を書いている ——
  *"patent holders are likely to be larger companies with the resources to file for patents and
  obtain legal advice on their IP rights. Would such patent holders be likely to use a template
  license, or would they have a bespoke license?"*（2026-05-15）。
  **この反論は ACD-1.0 にもそのまま当たる。**

### なぜこれを不利な事実として記録するか（#107）

**SPDX は「相当程度の実使用」を要求し、我々の実績は 1 件である**（`READY-TO-SUBMIT.md`
「残る弱点」2）。uptake を下げる設計は、**OSI の承認では問題にならないが SPDX の条件では
直接効く**。**我々がいちばん弱い軸に、我々がいちばん強いと主張している条項が乗っている。**

### 同じ発言の中に、我々にとって有利な実測もある

McCoy 氏は同じメッセージの直前で、特許許諾の**動詞の列挙**についてこう述べている ——
*"I understand there are precedents from prior licenses (BSD is the best example) for not fully
articulating all of these rights, but **I think that precedent shouldn't be used to allow for
incompletely written licenses now.**"*

**ACD-1.0 §8.1 は 6 つすべてを列挙している** —— *making, having made, using, offering to sell,
selling, importing, or otherwise transferring*。§8.4 も同じ列挙を繰り返す。
**この指摘は当たらない**（`AS-OF.md` に日付つきで記録した）。**有利な実測を落とすと、
不利な一覧は「不利に間違える圧力」の下で偏る**（`BLIND-SPOTS.md`「引き継ぎで失われるのは
事実ではなく枠」(1)）。

---

## 1.59 §12 の穴は「日本では」だけではない —— 法域の分岐と、#84 への接続（§1.49 の続き）

> **⚠ この節は当初「本セッションで最も重い発見」として書かれた。それは誤りだった。**
> **§1.49 が同じ論点を 2026-09-08 に既に記録している** —— Shuji Sado 氏が Blue Oak について
> *"in Japan, the Blue Oak License retains moral rights with the authors, posing a risk that usage
> could be stopped at any time"* と述べた `license-review` 2024-09 の投稿、Piana 氏の反対、
> §12 の各条への対応表まで在る。**新しい引用を 1 つ見つけたことを、新しい論点を見つけたことと
> 取り違えた。** 節は残すが、**§1.49 との差分だけを述べる形に書き直した**（2026-09-09）。

**§1.49 に対して本節が足すのは 3 つである。**

### (1) 発端は 2024-03 の `license-discuss` で、根拠は条文である

§1.49 が引くのは 2024-09 の `license-review` 投稿だが、**議論はその半年前に別のリストで
始まっている**。Sado 氏・`license-discuss` 2024-03-13 / 03-14 / 03-23:

> In Japan, copyright, which is a property right, and moral rights are separated… The BlueOak
> license clearly states "copyright," but this would probably be interpreted in Japan as **not
> including moral rights**.

> Japanese law recognizes the right of identity preservation **even for software**… Article 20(1)
> The author of a work has the right to preserve the integrity of that work… Usually, in Japan,
> contracts related to intellectual property rights always include a clause stating that
> **"the author shall not exercise moral rights."**

> To summarize the discussion so far, **the Blue Oak license is not open source, at least not in
> Japan.**

**§12.2 はその「行使しない旨の合意」そのものである。** §1.49 は「covenant である」と述べたが、
**それが日本の実務上の標準形だという裏づけは無かった。** ここで付いた。
**同じ人物が 2025-10-17 に、放棄一般についても同じことを述べている** ——
*"practice relies on **non-assertion covenants rather than blanket waivers**… a pure 'waiver'
rarely bites on its own."*

### (2) 法域の分岐 —— これは §1.49 に無い

**同じスレッドで、穴が普遍的でないことが示されている。**

| 法域 | 同一性保持権はソフトウェアに及ぶか | 出所 |
|---|---|---|
| 日本 | **及ぶ**（著作権法 20 条 1 項・例外は 20 条 2 項 3 号）| Sado 氏 2024-03-14 |
| 韓国・台湾 | **及ぶ**（構造が同じと同氏が調査）| Sado 氏 2024-03-15 |
| 英国 | **及ばない**（CDPA 1988 s.81 がプログラムを除外）| David Woolley 氏 2024-03-14 |
| スロベニア（および大陸欧州の多く）| **及ばない**（同一性保持権は software に適用されないと明記）| Matija Šuklje 氏 2024-03-13 |

**§12 が埋める穴は法域固有である。** 「どこでも incumbent が壊れている」ではない。

### (3) #84 への接続 —— これも §1.49 に無い

§1.49 は §12 を「リスト上の未解決論点への回答」として位置づけた。**本節はそれを
「なぜ 0BSD が在るのにもう 1 つ作るのか」（#84・Rob Landley 氏）への答えとして使う。**
#84 に対してこれまで書けたのは「1 件足す費用が低い」＋不在の 3 主題
（学習と TDM / モデルと出力に及ぶ特許 / 機械生成物）だけで、**人格権はその一覧に無かった。**
0BSD も MIT-0 も Unlicense も人格権に触れないので、**上表の左半分の法域では、
incumbent は「著作者がいつでも改変を止められる」状態を残している。**

### establish しないこと

- **リストはこの結論を採用していない。** Pamela Chestek 氏は同スレッドで
  *"Wouldn't the same criticism hold true for all the other licenses too?"* と返している ——
  **そのとおりで、だから差分になる**が、「では新しいライセンスが要る」への同意ではない。
- **§12.2 が日本法の下で機能するかは、弁護士が確かめていない**（弱点 1）。
  Sado 氏が述べたのは「実務がそうしている」であって「この文言で足りる」ではない。
- **#104 は消えない。** Piana 氏の *"these are not licensable"* は §12.1 に当たる。

## 1.60 委員長が 3 か月前に「長さ」を承認しない理由として述べている —— そして我々はその数を測っていなかった

**Linkumori Free License への Pamela Chestek 氏の返信**（`license-discuss` 2026-06-23）。
**Licensing Committee 委員長**であり、`license-review` の審査を主導している人物である。

> That said, your license seems to be undergoing substantial **mission creep**. You originally said
> it was to address the problem of attribution in a web-based context, but now you have added
> **moral rights**, a secondary license clause, and I don't know what else. **It is now 3888 words,
> longer than the GPLv3. It is excessively wordy and proscriptive. These qualities mean that no one
> other than you will ever use this license, so it does not seem to be a good candidate for
> approval.**

**この 1 段落に、我々に当たるものが 3 つある。**

1. **長さそのものが「承認の候補として良くない」理由として述べられている。** #6 はこれまで
   我々自身の懸念として書かれていた。**委員長の発言として、しかも数つきで存在する。**
2. **人格権条項の追加が mission creep の例として名指しされている** —— §1.59 で我々が
   「incumbent に無い穴」として評価した当のものである。**同じ条項が、片方から見れば差別化で、
   片方から見れば肥大である。**
3. **推論の形**: 冗長 ∧ 命令的 → **他の誰も使わない** → 承認の候補として良くない。
   **最後の 2 つは我々にも当たる**（採用実績 1 件・#2）。

### そこで数を測った（2026-09-09）

**この節を書くまで、我々は ACD-1.0 の語数を一度も測っていなかった。**
#6 は「16 節 / 82 項 / 597 行」とだけ述べていた ——**審査者が使う単位（語数）ではない。**

| | 全文 | 本体（前文・付録を除く） |
|---|---|---|
| GPL-3.0 | **5,644** | **4,617** |
| **ACD-1.0** | **4,896** | **4,574** |
| Linkumori（委員長が「GPLv3 より長い」と述べたもの） | 3,888（本人申告） | — |

**ACD-1.0 は GPLv3 より長くない。** 本体で **43 語短く**、全文で **748 語短い**。

**そして委員長の比較は、我々が測れるどの測り方でも成り立たない** ——
3,888 は GPLv3 の本体 4,617 より短く、全文 5,644 より短い。
**これを「委員長が間違えた」と使ってはならない。** 別の数え方（節の一部だけ、あるいは別の版）を
していた可能性があり、**我々は本人の測り方を知らない**。記録するのは我々の測定であって、
彼女の誤りではない。

### この発見が両刃である理由

**有利**: 長さの反論に対して、初めて**測った数**で答えられる。しかも
「GPLv3 と同程度」は、この文脈で最も分かりやすい基準である。

**不利**: 彼女の批判の核は数ではない。*"excessively wordy **and proscriptive**"* → *"no one other
than you will ever use this license"* である。**ACD-1.0 は proscriptive ではない**（§10.1 が
条件を一切課さない・§4.3）が、**「他の誰も使わない」は採用 1 件の我々により強く当たる**。
**数で反論して、推論の残り半分に答えないのは、いちばん都合のよい半分だけ取ることになる。**

---

## 1.61 「献呈なのかライセンスなのか、どちらかにせよ」—— 委員長が我々の中核構造に当たる言葉を書いている（2025-10）

**ACD-1.0 の中核は §3（献呈）と §4（許諾）を並置し、§4.4 で「独立に付与される」と述べる構造で
ある。** その構造に**そのまま当たる文**が、`license-discuss` に 11 か月前から在った。

### 原文（Pamela Chestek 氏・`license-discuss` 2025-10-16・PUWL v1.0 宛）

> **Which is it, a dedication to the public domain or a license? You can't have it both ways.**
> A dedication to the public domain is a full release of any and all rights, but a license is a
> way to exercise some control. You say that you want to have a dedication to the public, with
> various fallback positions if the law doesn't allow it, **but then you are nevertheless trying to
> retain some rights**

彼女が「留保」として名指ししたのは **4 つ**である ——
(a) 虚偽の著作者主張を認めない条項 / (b) 違法な利用を許さない条項 /
(c) 特許訴訟による自動終了 / (d) 責任の否認。そして:

> These provisions are **retention of rights**, contrary to the statement that the author is
> releasing all rights whatsoever in the work… You can only enforce them if you are **maintaining
> ownership of some rights** in the work… **The document is internally contradictory.**

### ACD-1.0 を 4 点に当てる（条文を読んで確かめた・2026-09-09）

| 彼女が挙げた留保 | ACD-1.0 |
|---|---|
| (b) 違法な利用を許さない条項 | **無い**（`grep -i 'unlawful\|illegal'` で 0 件）|
| (c) 特許訴訟による終了 | **無い。** §8.2 が *"contains no patent retaliation provision, and its absence is deliberate"* |
| (d) 責任の否認 | **有る**（§13 / §14）。**ただし承認済みライセンスはすべて持つ**ので、この項目は我々を他と区別しない |
| (a) 虚偽の著作者主張 | **有る** —— §11.3 と §12.5。**ここが当たる** |

**そして「all rights whatsoever を放棄する」という第一文が、そもそも ACD-1.0 に無い。**
§3.1 が surrender するのは **Covered Rights** という定義された集合で、§1.5 が特許・商標・人格権を
そこから除き、§2.7 が一般的な限界を述べる。**彼女が突いた「全部放棄と言いながら留保している」
という形は、定義によって回避されている。**

**§11.3 は、この反論を予期して書かれている** ——
*"This Section states a **limit of the Dedication's reach**; it is **not a condition upon You**,
and Section 10.1 is unaffected by it."* つまり「留保した権利を行使する」のではなく
「そもそも Dedicator のものではなかったから許可のしようがない」という形にしてある
（*"it was never the Dedicator's to permit"*）。§11.4 が privacy / publicity / データ保護について
同じことをする。

### それでも不利な事実として記録する理由（#110）

**反論は 1 文、答えは 4 条である。** *"You can't have it both ways."* に答えるには
§11.3 の最終文・§10.1・§1.5・§2.7 を読ませる必要がある。
**#100 / #101 / #104 と同じ非対称**で、この非対称そのものが不利である。

**さらに悪いのは、彼女が挙げた 4 つのうち我々に当たる 1 つが、我々自身の言葉と衝突すること。**
ドシエは ACD-1.0 を「**何も留保しない instrument**」と繰り返し述べてきた（#6 の書き出しがそれ
である）。**§11.3 と §12.5 は、少なくとも表面上は留保に見える。** 我々の説明は正しいと考えるが、
**「留保していない」と一言で述べる書き方は、この反論に対して最も弱い形**である。

### 有利な側も同じ強さで

**この 1 通は、ACD-1.0 が回避している設計上の失敗を 3 つ名指ししている** ——
違法利用条項 / 特許報復 / 全面放棄の宣言と個別留保の同居。
**§8.2 が「不在は意図的である」と本文に書いてある理由**が、ここに実例として存在する。
`comparison.md` §1.53（PUWL の「撤回不能」と「自動終了」の同居）と同じスレッドの、より深い層である。

