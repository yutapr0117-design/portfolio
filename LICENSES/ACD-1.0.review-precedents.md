---
file: LICENSES/ACD-1.0.review-precedents.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-09-25
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
| **Josh Berkus 氏**（OSI）: 実プロジェクトは AI 生成・AI 補助・人間著述・他 OSS 由来の file が混在し、履歴を通じて改変される。ファイル単位の帰属モデルは *"targets only brand-new projects which are created from scratch and never modified again"* | **§9.3** | **どの部分が機械生成かを判定する必要が無い。** *"No permission granted here depends on that question, or on how any jurisdiction answers it, or on whether the answer changes."* |

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
| **Piana（同日 18:29・上の続き）**: *"I have nothing against using a **PD dedication and a license by way of backstop** where PD does not really exists [sic] in the fullest… **I actually advise to use both**"* | **これは指摘ではなく支持である。** §3（献呈）と §4（許諾）の対は、この審査者が**自ら勧める**構造そのもの。「dedication *taken alone* は承認されない」という 2020 年の勧告に対する我々の答え（§4.4）と同じ向き |
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

### 結果（**2026-09-13 に理事会議事録で訂正した**）

**この節は 2026-09-07 に「提出者は取り下げていない（2025-08-28 時点でスレッドは自然に終息）」と
書いた。アーカイブだけを見れば、それは正しい。** だが**帰結はアーカイブには現れていなかった** ——
**2025-12-19 の理事会議事録に、委員会が MIT-I を取り下げたと記録されている**
（*"The committee has withdrawn the NIST Software License (Legacy) and **the Irrevocable MIT
License**"*・逐語は `rounds/2026-09-13-osi-board-meeting-minutes-2025-06-to-2026-06.txt`）。

**したがって帰結は「自然終息」ではなく「委員会による取り下げ」である。**
提出は 2025-07、議論は 2025-08 に止まり、**取り下げは 4 か月後**に、リストではなく理事会で記録された。

**ここから出る一般形のほうが、この 1 件より重い。**
**リスト上の沈黙は、帰結が無いことを意味しない。** 手続きは別の場所で進み、別の場所に記録される。
**我々は「返信ゼロ」を数えてきた**（#109 / #117）が、**返信ゼロのスレッドの帰結を、
我々はどこからも読んでいなかった。** **`license-review` のアーカイブは議論の記録であって、
決定の記録ではない**（`ACD-1.0.board-decisions.md`）。

**なお「取り下げ」は「否決」ではない。** 同じ議事録は NIST Software License を取り下げたと述べ、
**その NIST は 2026-02-20 に承認されている** ——**取り下げは終端ではなく、経路である。**

**承認されていない**（2026-09-13 時点の公開記録で）。
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

## 1.88 承認は取り消せない —— そしてその事実を、承認する側が自分で述べている（2026-09-15 に取得）

**逐語は `rounds/2026-09-14-license-review-openmdw-thread-observed.txt`**（OpenMDW スレッドの
観測。**我々宛ではなく ACD-1.0 についてでもない** ——register に効く 2 文があるので記録する）。

**(A) Richard Fontana 氏・2026-09-11**（配送された本体を保存。引用の中だけではない）:

> The OSI does not currently have a process for de-listing licenses, and I wouldn't put
> OFL-1.1 at the top of the list if it did because there are actually worse licenses on
> the OSI-approved list, but it would be on the list.

**(B) Carlo Piana 氏・2026-09-14**（de-listing の是非を持ち出した参加者への返信）:

> It's a hell of an important issue and whichever decision would bring unintended
> consequences. We have discussed internally many times and for the time being we
> defaulted to not take any action, even though revising ALL the approved licenses
> (which we have done recently), some approved licenses, fortunately some seldom if at
> all used, leave licensing experts scratching their heads as to how the heck...

#### 何が確立し、何が確立しないか

**確立する 3 点:**

1. **承認は事実上取り消せない。** de-listing の手続きは**無く**、作る議論は内部で何度も行われて
   **「当面は何もしない」**に落ち着いている。
2. **承認済みリストには、専門家が首をかしげる起草のライセンスが実在する** ——
   そう述べているのは**承認する側の人間**である。
3. **委員会は最近、承認済みライセンスを全件見直した。**

**確立しないこと**: どのライセンスのことか / それが**新規提出の基準に影響するか**。
**両氏とも ACD-1.0 について何も述べていない。**

#### 🟢 我々に有利な読み

**起草の粗さは、承認の絶対的な障壁ではない**（#6 / B3）。**承認済みリストにその実例が在ると
承認する側が認めている。** これは我々の推論ではなく、**リスト上の発言**である。

#### 🔴 そして同じ 2 文の、より強い不利な読み

**取り消せないからこそ、入口が固くなる。** 誤った承認のコストが**永久**であり、
しかも**最近になって全件を見直した結果として不満が残っている**なら、
**委員会が「もう一つ首をかしげるものを足す」ことに慎重になる理由は増える。**

**この読みは #84（なぜもう一つ PD 等価を）と B2（採用 1 件）に直接乗る** ——
Landley 氏の問いは「代替可能な類型に 1 件足す費用」を問うており、
**その費用が「取り消せない」なら、答えるべき費用は我々が見積もっていたより高い。**
`comparison.md` §1 の「この類型に 1 件足す費用が低い」という答えは、
**「費用が低い」ではなく「費用は低いが取り返しがつかない」へ書き換わる。**

**どちらが勝つかは我々には決められない。両方を register に載せる。**

## 1.105 日本発の提出を初めて開いた —— 止めたのは本文ではなく翻訳の証明だった（2026-09-22）

**きっかけはオーナーの指摘**（*「世界中で議論するのに、日本人不在はおかしい」*）。
**⚠ 当初これを「推論」と書いたのは誤りで、本人が同じ時間に訂正した** ——
*「私は私でレビューしてるから、日本人が居るのは知ってたよ」*。**本人はアーカイブを自分で読んでおり、
知っていた。** **我々がしたのは数えることだけである** ——`license-review` / `license-discuss` のアーカイブ 314 file・
差出人 633 人を数えると、**日本の参加者が実在する**: 佐渡秀治氏 38 通（**ドシエが既に 9 file で引用**）、
**Yutaka MATSUBARA 氏 25 通（`ertl.jp`・名古屋大 ERTL）——ドシエでの言及 0 件**、ほか 2 名。

**MATSUBARA 氏の 25 通のうち 23 通が 1 つのスレッドだった**:
**「For Legacy Approval: TOPPERS License」（2015-06-10 〜 2015-11-04・全 50 通）。**
**当時これを「記録に在る唯一の日本発の提出」と書いた。⚠ それは誤りだった（2026-09-25 に訂正・`against.md` #242）** ——**2009 年の IPA Font License v1.0 が在り、しかも承認されている**（§1.110）。**誤った原因は探し方にある** —— この節は**差出人のドメインから日本の参加者を数えて**辿り着いており、**提出名の側から数えると別の 1 件が出た。**

### 何が起きたか

- 提出は **legacy approval** 目的。ライセンスは**日本語版と英語版**を持つ。
- **理事たちは前向きだった** —— Josh Berkus 氏 *"I am +1 to approve as a legacy license"*、
  提出者側の要約でも *"the English-language version ... worthy of OSI legacy approval"*。
- **止めたのは翻訳の証明である。** Richard Fontana 氏:
  *"We'd prefer to have an affidavit from a **professional translation service**. I realize that
  might be a little odd in this case, but the nature of this case also calls for **some extra care
  on our part**."* ——提出者が提案した「計算機科学と OSS に詳しい弁護士による検証」は**採られなかった**。
- 同じスレッドに **"International License category"** の語が在り、
  *"err on the side of strictness concerning the certified translation requirement,
  at least until we get more experience with the International License category"* と述べられている。
- **スレッドは 2015-11-04 で止まっている。**
  **⚠ 最初にこう書いたとき、corpus には 2016 年が丸ごと欠けていた** ——2015 と 2017 は在り、**続きが在るなら在る場所だけが穴だった**。**同日に 2016 年の両リストを取得して 測り直した**: 21 か月を取得（3 か月は月次 file 自体が存在せず 404）、**TOPPERS の言及は 0 件**。**「止まっている」は、いま 2015〜2016 を通して測った上での主張である。**

### ⚠ 確立しないこと

**却下されたとは書けない。** 止まっただけで、**取り下げたのか、リスト外へ移ったのか、
立ち消えたのかはアーカイブからは決まらない**（#91 / #139 と同じ形）。
OSI のライセンス API（126 件・**網羅ではない**）にも SPDX にも TOPPERS は無いが、
**不在は決定の証拠ではない。**

### ACD-1.0 に効くところ

1. **§15.8 は英語を正文と定め、§16.4 は翻訳の頒布を同じ名称・識別子の下で許している。**
   **OSI には、非英語版が在るライセンスに *professional translation service の宣誓供述書* を
   求めた実例が在る。** 日本語版の ACD が §16.4 の許す形で配られたとき、この先例が当たる。
2. **手続きが門番である**（§1.75 と同じ結論が、別の年・別の国・別の類型で再現した）——
   **5 か月・24 通を投じた提出者が、本文の評価ではなく証明の要件で止まっている。**
3. **我々に最も近い「国」の先例**であり、**steward は日本人で、ドシエの大半は日本語である。**

### ⚠ 逆側

**これは我々に不利な材料ではない。** ACD-1.0 は**英語で書かれ、日本語版は存在せず、
§15.8 が英語を正文と定めている** ——**翻訳証明の要件は、いま我々には発火しない。**
**発火するのは「日本語版を配ったとき」だけ**であり、それは §16.4 が許すが、我々はしていない。
**先例を知らずに日本語版を出すことが危険だった**のであって、現状が危険だったのではない。


## 1.108 理事会が実際に不承認にした、我々の時代でいちばん近い審査 —— 理由は OSD ではなく主題だった（2026-09-25）

**Mulan Open Works Licenses（MulanOWL BY / BY-SA / BY-PL / BY-PL-SA）**。
提出 2023-02-20、**理事会の議決 2023-09-15、結論は不承認**。
一次資料は `rounds/2023-02-license-review-mulanowl-open-works-observed-*.txt`（14 通・11 部）。

**このスレッドは、件名に主題語を 1 つも含まないので、我々の census には一度も現れなかった**
（`against.md` #240 —— 件名がライセンスの名前でできているから）。

### 勧告文は OSD 違反を 1 つも挙げていない

> *"Resolved that it is the opinion of the OSI that the licenses, **as open culture licenses, are
> not appropriate for OSI approval**."*
>
> Reasons for withholding approval: The subject matter of licenses is "intellectual achievement
> protected by copyright law that is licensed under This License, including but not limited to a
> written work, a musical work, a fine art work, an architecture work, a photographic work, **an
> audiovisual work**, a graphic work, and a model work." Because of the differences in the purposes
> and goals of these different (albeit related) areas, **open culture licenses are outside the
> purview of the Open Source Initiative.**

**ACD-1.0 §1.2 の列挙は "audiovisual material" を含む**（`against.md` #237・bottleneck B15）。

### 境界は委員会自身が引いている

Pamela Chestek 氏（License Committee 委員長）2023-08-10 ——
*"the OSI is not in the practice of approving licenses that are not software-specific. ...
Sometimes an OSI license will **cross over into data or hardware when tied to software**, but not a
license altogether unrelated to software."*

Carlo Piana 氏 2023-07-05 —— *"In general, all the licenses should be rejected for not being
(Open Source) software licenses."* Josh Berkus 氏 2023-03-01 —— *"OSI has not previously approved
content licenses ... it would be an **organizational policy change** and therefore not a routine
license approval."*

### 同じスレッドが、CC0 について我々が持っていなかった第 2 の出典を与える

Chestek 氏 2023-08-10 —— *"Two of the licenses ... are not likely to be approved because they
**expressly state that they do not grant a patent license**. **This is the reason that the CC-0
license is not an OSI-approved license** ... although **it has not been definitively decided due to
Creative Commons' withdrawal of the license from consideration**."*
Piana 氏 —— *"pure copyright licenses excluding all other rights ... **do not meet the OSD**, since
they **expressly carve out patents** from the scope of the license."*
**`comparison.md` §1.4 へ還元済み。**

### 手続きについて 2 つ

**(1) 複数本の同時提出は審査を難しくする**、と委員長が明言している ——
*"It is also difficult to manage the approval process when **more than one license is submitted at
a time**."* **ACD は 1 本なので当たらないが、1.x 系列を同時に出す誘惑への答えになる。**

**(2) 公表された決定期限は守られていない。** 勧告文自身が *"Decision date: due no later than the
first Board meeting after **April 20, 2023**"* と述べ、**実際の議決は 2023-09-15**（提出から 207 日）。
委員長は *"I apologize for not processing these licenses sooner, time slipped away from me."* と書いている。
**`AS-OF.md` の所要日数（実測中央値 101 日）は「決まった場合」の値であり、期限は上限ではない。**

### この節が establish しないこと

**「我々が不適格だ」とは述べていない。** §1.2 は source code / object code から始まり、
PREAMBLE の第 1 文は *"Software and the works that surround it"* で、適用先はソフトウェアの
リポジトリである。**上の carve-out は ACD の形をそのまま述べている** ——
**だがそれは我々の読みであって委員会の判断ではない。**


## 1.110 日本発の提出は 2 件あり、通った方には弁護士が付いていた —— IPA Font License（2009・承認）（2026-09-25）

一次資料は `rounds/2009-02-license-review-ipa-font-license-observed-*.txt`（41 通・3 部）。
**§1.105 が「唯一」と書いたのを撤回する根拠でもある**（`against.md` #242）。

### 誰が出したか

**2009-02-04、`mhmjapan.com` の Yuko Noguchi 氏 —— 森・濱田松本法律事務所の弁護士**が、
**独立行政法人情報処理推進機構（IPA）を代理して**提出している ——
*"On behalf of The Information-Technology Promotion Agency, Japan ("IPA"), we would like to submit
'IPA Font License v1.0' for OSI approval."*

**B1 にとっての意味は率直である。** 日本発の提出は 2 件あり、
**弁護士が付いた方（IPA Font・2009）は承認され、付かなかった方（TOPPERS・2015）は
翻訳の証明で止まった**（§1.105）。**n=2 なので因果は言えない。だが並べれば見える。**

### 何が論点になり、どう決着したか

初版は **difference file（差分ファイル）方式** —— 派生フォントは「元のフォント + 差分」でしか
配布できない —— を採っていた。**Perens 氏が OSD 2 で切った** ——
*"a step required to translate the program into a usable form ... must not take place until after
distribution. Thus it doesn't permit distribution of the compiled form, and doesn't pass OSD #2."*

**提出者は 1 か月で本文を 2 度書き直し、3 月 4 日に difference file の要求を全部落とした。**
Perens 氏 *"Please convey to your colleagues my appreciation for the excellent way they have
listened and responded to the objections."* Tiemann 氏 *"I hereby add my own affirmation that this
license appears to meet the criteria of the OSD in letter and in spirit."*

**⚠ これを「審査中は書き直してよい」と読んではならない。** 2009 年の運用であり、
**2026 年の process ページは「審査中は変更せず、取り下げて新版を出せ」と明文で述べている**
（`REVISION-PROTOCOL.md` §2）。**読めるのは「指摘に応じて落とした」という*姿勢*の方である。**

### 再利用の見込みが無いことは、却下ではなく分類で処理された

Chuck Swiger 氏 2009-03-27 —— *"the license seems to be fully OSD-compliant. It would be more
universal if 'Article 5 (Governing Law)' section could be removed, but as this license seems to be
fairly specific to IPA anyway, that might be a moot concern: regardless, **I would recommend
approval and placing it into the 'Non-reusable licenses' category**."*

**B2（採用実績 1 件）にとって、これは 2 つのことを同時に述べている。**
**有利**: 再利用の見込みが無いことは、**承認しない理由ではなく、収容先の問題として扱われた。**
**不利**: **その収容先は降格である。** ACD-1.0 は §16.3 と提出パケット §4b で
**「提出者専用ではない」ことを積極的に主張している**ので、この扱いは我々が求めるものではない。
**そして 2009 年の category 体系は現在のものと違う** ——現在の分類は
`review-labels.md` が扱っている。

### 主題適格（B15）にとっての逆側

**OSI はフォントのライセンスを承認している。** 主題は source code でも object code でもなく
**書体**だが、Cowan 氏がこう述べている ——
*"In the U.S., the appearance of a font is what is not copyrightable, nor is a straight
representation of the font ... **A vector font, however, is considered program code and therefore
copyrightable**."*

**線は「コードか否か」ではなく、「プログラムとして扱えるか / ソフトウェアに結びついているか」に
引かれている。** これは B15 にとって有利な材料である ——
2023 年の Mulan 不承認（*"open culture licenses are outside the purview"*）と並べると、
**フォント（承認）と文化的著作物（不承認）の間のどこかに線がある**ことが分かる。
**⚠ ただし線の位置は分からない。** そして **ACD-1.0 §1.2 が名指しする "audiovisual material" は、
フォントより Mulan の列挙に近い語である。**

### 2025 年の後日談 —— 同じ件名に 16 年後の 4 通が繋がっている

2025-09、IPA Font License で配布された MJ 明朝の WOFF 変換版に対し、
権利を承継した CITPC が配布停止を求めた件が `license-discuss` に持ち込まれた
（*"questions have arisen within the Japanese-speaking open-source community about whether the IPA
Font License fundamentally meets the definition of open source"*）。
**Shuji Sado 氏（Open Source Group Japan 会長）が答えている** ——
*"I don't see this episode as bearing on whether the IPA Font License v1.0 is 'Open Source.'
It looks like an **operational compliance issue** around redistribution conditions, **not a
challenge to the license's status**."*

**ドシエは佐渡氏を 9 file で引用しながら、このスレッドを引いていなかった。**
**承認は取り消せない**（§1.88）という事実と、**承認後に「本当に open source か」と問われうる**
という事実は両立する ——**そしてその問いに答えたのは OSI ではなく、その言語圏の当事者だった。**
