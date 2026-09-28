---
file: LICENSES/ACD-1.0.review-doctrine.md
audience: OSI license-discuss / license-review participants, licence reviewers, 監査人
last-updated: 2026-09-27
canonical-ref: LICENSES/ACD-1.0.review-precedents.md (他の提出に何が起きたかの記録) / LICENSES/ACD-1.0.against.md
---

# リストで論じられた法理を、ACD-1.0 の特定の条へ当てたもの

**`ACD-1.0.review-precedents.md` から 2026-09-25 に切り出した。引き金は advisory 予算だが、
割る線は行数ではなく主題で選んだ。**

**残した側（`review-precedents.md`）は「他の提出に何が起きたか」の記録** ——
撤回・却下・承認・改名・理事会の議決。**こちら（本 file）は「リスト上の法理を、我々の特定の条に
当てるとどうなるか」** —— §6.3 / §10.4 と OSD 5 / 学習のための複製と TDM 例外 / §8 と §5。

**節番号は変えていない**ので、既存の `§1.84` / `§1.100` / `§1.101` / `§1.109` という参照は
番号としてはそのまま解決する。**file 名を添えている参照は本 file へ向け直した。**

**この分け方の限界**: 「顛末」と「法理」は排他ではない —— たとえば §1.57（Unlicense への veto）は
顛末でありながら、その論拠が ACD の条文になっている。**境界は読み手の用途で引いてあり、
論理的に排他な分類ではない。** 迷ったら両方見る。

## 1.84 委員長が OpenMDW に当てている原理を、我々の §6.3 に当てると刺さる（2026-09-15）

**§1.88 と同じスレッドの読み。** 2026-09-10〜09-14 の争点は**終了条項**であり、
**ACD には終了が無い**（§10.1 / §10.4）ので**表面は当たらない**。
**だが委員長が使っている原理は、条項の種類に依存していない。**

> **You're putting the burden on the potentially wronged party to limit their choices rather than
> on the licensor to avoid wrongful conduct.** … You are also assuming the licensee has knowledge
> that will allow them to make an informed choice, **but that's not the reality**. The OpenMDW-1.1
> licensee is asked to agree to the license **without having any knowledge about whether it
> infringes**
> —— Pamela Chestek 氏（Licensing Committee 委員長）、`license-review` 2026-09-11

### 🔴 この原理が当たる場所が、ACD に 1 つだけある

**§6.3 は、ACD 全体でただ一つ、「第三者がした行為」に対して働くと述べる条項である。**

> Where a Reservation has been made in respect of the Work, **whether by the Dedicator or by
> another person**, and whether before or after this Dedication was applied, the Dedicator
> **withdraws it and disclaims reliance on it, to the fullest extent the Dedicator is able**.

**実測して確かめた**: 第三者に触れる他の条項は、いずれも **Dedicator 自身の行為**しか縛らない ——
§5.1 と §8.6 は *"not to authorise or assist **any other person** to assert"*（Dedicator の不作為）、
§8.2 は報復条項の不在、§2.7 は**及ばないことの宣言**。
**「他人がしたことを取り消す」と述べるのは §6.3 だけである。**

**委員長の 2 つの問いを、そのまま当てる。**

1. **負担は誰に置かれているか。** 第三者は、自分の Reservation が「撤回された」と書かれた文書を
   読む。**その撤回が自分に届いていないことを知る負担は、その第三者にある。**
2. **読み手は判断に足る知識を持っているか。** 受領者は、目の前の Work に他人の Reservation が
   付いていたかどうかも、Dedicator が *"able"* だったかどうかも**知り得ない**。
   ***"to the fullest extent the Dedicator is able"* は、読んだ時点では何も確定させない限定である。**

### 我々の答えと、その答えの弱いところ

**答えはある。** §2.7 が instrument 全体を「Dedicator が持つ権利」に縛り、
§6.2 の末文が *"does not purport to defeat a Reservation made by another rightsholder"* と述べ、
§6.3 の *"to the fullest extent the Dedicator is able"* がその限定を条文内で繰り返している。
**法的には、届かない撤回は届かない。**

**弱いところは、それが読み手の作業になることである。** 3 条（§2.7 / §6.2 / §6.3）を
**この順で読んだ人にしか成立しない**。**そして #99 が既に記録しているとおり、読み順は我々が
決められない。** 委員長の言い方を借りれば、**我々は「届かないと分かるはずだ」という前提で
負担を読み手に置いている。**

### この節が establish しないこと

**委員長は ACD-1.0 について何も述べていない。** これは**他者の提出に当てている原理を、
我々が自分に当てた結果**であって、指摘を受けたのではない。
**そして逆側**: 原理が当たることと、**それが OSD 違反であること**は別である ——
§6.3 は条件でも制限でもなく、**誰の自由も減らしていない**（減らしうるのは第三者の Reservation の
効力だけで、それは届かない）。**「刺さる」と「不承認の理由になる」を混ぜない。**

### 🔴 この節の初版は「1.1 で直すかどうかは未決」と書いた。**草案を開かずに書いた。**

**1.1 草案の §6.3 は、既にこれを条文内で閉じている**（**前日 2026-09-14** に、
外部レビューを受けて入れた）:

> *"Where the Reservation is another rightsholder's, made in exercise of rights of their own, the
> **Dedicator has no power to withdraw it and this Section does not purport to give one**;
> the disclaimer of reliance operates in every case (Section 2.7)."*

**したがって残るのは 1.0 についてだけ**であり、1.0 は凍結中なので**直さず記録する**。

**それでもこの節に価値がある理由は 2 つ。** (1) **前日の修正は「狭めよ」という処方への
対案として入れた**もので、*なぜ*入れる価値があったのかは書いていなかった ——
**委員長の原理が、その理由を外から名指しする**（負担を、知り得ない側に置いていた）。
(2) **1.0 の側は依然として読み順に依存している**ことが、これで明確になった。

**⚠ そして本日 9 度目の同じ失敗である。** 「未決」と書く前に草案を開いていない ——
**しかもその草案は、前日に自分が編集した file である。**
`BLIND-SPOTS.md` が *「近いものほど確認が省かれる」* と記録している当のことをした。


## 1.100 OSD 5 に広い読みが持ち出された —— そして ACD には当たらない理由が、同時に費用でもある（2026-09-16 / 09-18）

**取得**: `license-review` 2026-09 のアーカイブ（取得時刻 2026-09-19T16:55Z）。

**McCoy Smith 氏（Licensing Committee）が ModelGo Attribution 2.0 の終了条項に、
これまでこのリストで読んだことのない角度を当てた。** 条文は終了の引き金を
*"if You initiate any legal action "against the Licensor" alleging that the Licensed Materials
and/or Derivative Materials infringe any patent worldwide"* と書いている。氏はこう述べた:

> That means a patent assertion against a *Licensee* (someone who has received and is using
> the licensed code, but has not granted any license too it) does not trigger termination of
> the license. This puts Licensors & Licensees in different positions vis a vis patent
> assertions, and therefore arguably violates OSD 5

**そして 4 つの既承認ライセンスを並べ、引き金が*当事者*ではなく*著作物*に向いていることを示した**
——Apache-2.0 *"against any entity … alleging that the Work or a Contribution … constitutes direct or
contributory patent infringement"* / MPL-2.0 *"against any entity by asserting a patent infringement
claim … alleging that a Contributor Version directly or indirectly infringes any patent"* /
EPL-2.0 / GPL-3.0。

**09-18 に steward（Duan 氏）は譲らなかった**:

> OSD 5 says the license must not discriminate against any person or group of persons. Here,
> Licensor is a role in the license, not a person.

**我々にとっての意味を、有利・不利の両方で書く。**

**有利（構造的に当たらない）**: **ACD には終了規定が一切無い。** §10.4 が
*"No permission granted by this Dedication terminates for any reason. This Dedication, in respect
of the Work, contains no termination provision and no revival provision, because it contains
nothing that You could breach."* と述べ、§8.2 が特許許諾を終了不能としている。
**引き金が無いので、引き金の向きを問う指摘は起動しない。**
**同じ形の確認はこれで 3 例目**（2025-03 / 2026-08 / 本件）——**リストが労力を割いている論点集合と
ACD の表面集合が交わらない**（#101 の再現）。

**不利（同じ 1 つの事実である）**: **その免疫は、#174 が費用として記録した「特許報復の不在」と同一の事実**である。
エコシステムが報復条項を置いたのには理由があり、ACD はその防御手段を持たない。
**「指摘されない」と「その設計が良い」は別**であり、ここで得ているのは前者だけである。

**不利（我々の OSD 逐条の当て方）**: **氏の読みは OSD 5 を「人・集団」ではなく「役割の非対称」まで広げている。**
我々の OSD 5 の当て方（`submission-reference.md` §3 / §3b）は**狭い読みしか当てていない**
——`against.md` #179。**⚠ ただし広い読みは確立していない**: 氏自身が *"arguably"* と書き、
steward が正面から争っており、委員会の裁定でも理事会の決定でもない。
**確立するのは「そういう読みがリスト上に現れた」ことだけである。**


## 1.101 リストは「学習のための複製がそもそも侵害か」を未決として論じている —— そして TDM 例外を名指ししている（2026-09-10〜14）

**取得**: `license-review` 2026-09（取得時刻 2026-09-19T16:55Z）。**OpenMDW の終了条項をめぐる
スレッドで、議論は「著作権の主張を引き金に許諾を切ってよいか」へ移った。**
**我々宛でも ACD-1.0 についてでもない。**

**Pamela Chestek 氏（Licensing Committee 委員長・2026-09-10）**:

> What I find distinguishable about a termination of the copyright license versus the patent
> license is that copyright infringement doesn't happen by accident. There is no copyright
> infringement without deliberate, knowing copying.

**Luis Villa 氏（同日）が正面から否定し、根拠に法域の例外を 2 つ名指しした**:

> This conflates two different things: copying is always intentional, but not all copying is
> copyright infringement. There are very clear good-faith arguments (under both the EU's TDM
> exception and US fair use) that the sorts of copying we're mostly talking about here are not
> copyright infringement.

**Josh Berkus 氏（2026-09-11 / 09-14）は「事故による侵害的複製」の実例を列挙し、
その中に生成 AI を入れている**:

> Speaking as a software developer, accidental infringing copying happens all the time.

> - Stack overflow - GenAI & Autocomplete - Copying code from a private project to a public one,
> forgetting where you got it in the first place …

**Richard Fontana 氏（2026-09-11）は、FOSS が「不正」と見なしてこなかった行為を罰する条項の危うさを述べた**
（API の再実装を例に）。**Michael Dolan 氏（2026-09-14・OpenMDW steward）は束ね方の論点で答えている。**

### ACD-1.0 に効く点

**(1) B10 の 1 本目に、リスト側からの裏付けが付く。** 我々は §6 の gap を
「既存の承認済みライセンスはこの主題に沈黙している」という**語の不在**で示してきた。
**このスレッドは、沈黙が残す当の問い ——学習のための複製が侵害にあたるのか——
を、審査する側自身が未決として論じ、EU の TDM 例外を名指ししていることを示す。**
**同じ問いを、同じ週に、ドイツの控訴審が UrhG 44b 条 / UrhG 60d 条で決めている**（`jurisdictions.md` §9a (9)）。
**「沈黙が未解決に残すもの」は仮定ではない。**

**(2) §2.7 が答えている懸念が、実例つきで述べられた。** Berkus 氏の一覧は
「付与者が、自分の持っていない権利を渡したつもりになる」経路の列挙である。
**ACD §2.7 は *"reaches only rights the Dedicator holds"* と述べ、§1.3（1.1 以降は §1.4）は
Dedicator を *"to the extent that person or entity holds or may hold Covered Rights"* で定義する。**
**先回りではない** ——同じ懸念に既に答えている、というだけである。

### establish しないこと

- **これは ACD-1.0 についての議論ではない。** OpenMDW の終了条項についてであり、
  **ACD には終了条項が無い**（§10.4）ので、争点そのものは当たらない。
- **リストがこの種の明示を望んでいる証拠ではない。** Villa 氏自身が
  *"maybe you don't agree with those arguments (I move back and forth myself a lot of the time!)"*
  と書いている ——**未決であることの証拠であって、答えの証拠ではない。**
- **個人の資格での発言である。** 委員長の発言も含め、委員会の裁定でも理事会の決定でもない。

## 1.109 2006 年の 2 スレッドが、特許についての 3 段目と、Unlicense 先例への依拠を同時に出した（2026-09-25）

一次資料は `rounds/2006-07-license-discuss-broad-institute-bipl-observed-*.txt`（28 通）と
`rounds/2006-11-license-discuss-biological-open-source-observed-*.txt`（11 通）。
**どちらも件名フィルタでは拾えず、recall テストで初めて出た**（`against.md` #240）。

### 特許: 沈黙は許され、除外は致命的で、明示は実務の標準である

**1 段目（沈黙）の 5 人目。** 提出者側弁護士 Karin Rivard 氏（MIT）2006-07-14 ——
*"The requirements for OSI certification **do not include a requirement** that the originator of the
software offer a license to originator owned patents."* **この点への反論はスレッドに無い** ——
Rosen 氏の反論は「不適合だ」ではなく「賢明でない」だった。

**3 段目（明示が標準）。** Lawrence Rosen 氏 2006-07-14 ——
*"many people hope that the old BSD- and MIT-style licenses have 'implicit patent licenses,' but
that's **a thin reed** from which to build a basket that's to hold valuable software. **All modern,
professionally-written open source licenses, including the proposed new GPLv3, contain explicit
patent grants**."*

**これは #236 の 4 人（黙示の許諾で足りるという読み）に対する、名前のある反対である。**
**ただし「§8 が要求されている」ことにはしない** —— 3 段の構造は `against.md` #238。

**同じ Rosen 氏が、covenant not to assert を勧めてもいる** ——
*"MIT ought to **covenant that the University itself will never assert its patents against open
source software**."* **ACD-1.0 §5 はその形である**（Piana 氏の「PD 献呈 + 許諾のバックストップ」
§1.52 に続く、2 件目の「我々が採った構造をリストの権威が自ら勧めた」記録）。

### Unlicense 先例への依拠に当たる一文

David Dillard 氏 2006-07-14 —— *"You're correct that previously approved licenses have done (or not
done) things that MIT is repeating ... Keep in mind that **as experience grows people learn that
mistakes have been made** and try not to repeat them. I think it's safe to say that **there are some
previously approved licenses that would not be approved if submitted today**."*

**当たるのは、先例を合否の予測に使うときだけである。** 我々が Unlicense を引く用途は
「承認されたのだから我々も通る」ではなく「**献呈 + 許諾の併置という形が審査対象になりうる**」
ことを示すためで（`submission-reference.md` §1b）、その用途には当たらない。
**だが我々自身が Unlicense を「起草が粗いと広く合意されつつ承認された」と書いており、
それはまさに Dillard 氏が名指しした種類の承認である。**

### 採用実績（bottleneck B2）の 2006 年の姿

John Cowan 氏 —— *"**We are reluctant to go through the effort of approving licenses which no one
but the drafter of the license will ever make use of.**"*
**20 年前から同じ文で述べられている**（2025-07-18 の理事会がこれを「否決ではなく *not approved*
のまま留め置く」に精密化した —— `board-decisions.md` §2a）。

### そして §8.4 に真っ向から当たる proliferation

Rosen 氏 2006-11-15（BiOS スレッド）—— *"**I don't think there's much enthusiasm to come up with yet
another way to say these things about patents.**"*

**答えは 1 つしかない** —— 既存の特許許諾条項は *"the Work and Derivative Works"* で止まり、
**学習済みモデルと出力に届かない**。届かないことを示せなければ、§8.4 は
「特許について言う、もう一つの言い方」である。**この主張は本ドシエに既に在るが、
反対の形に名前がついたのは 2026-09-25 が初めてである。**

## 1.111 OSD の起草者本人が「OSD は著作権・人格権・特許を区別しない」と述べている —— MXM Public License（2009・不承認）（2026-09-25）

一次資料は `rounds/2009-04-license-review-mxm-public-license-observed-*.txt`（59 通・4 部）。
**提出したのは Carlo Piana 氏で、ISO/IEC の MPEG Working Group を代理している。**
**そして氏が 2023 年に、我々の論点の先例として自分のこの提出を名指ししている** ——
*"we have in the past discussed many times (see discussion of CC0 or **the MXM license** or the
W3C license) pure copyright licenses excluding all other rights"*（`against.md` #238）。

### 何が提出されたか

MPL を改変し、**特許条項を外した**もの。提出文はその理由を隠していない ——
*"none of the contributors would have accepted to encapsulate their patents in a FOSS license
without the ability to ask for a license separately from the copyright."*

### 起草者本人の発言（本節の中心）

Bruce Perens 氏 2009-04-14 ——

> *"I am the creator of the Open Source Definition, and thus can shed some light on the parts that
> might be seen as ambiguous. ... **The OSD does not distinguish between copyright, moral rights,
> patents, contract restriction, or any other means of restricting what someone can do with
> software. It applies equally to all of those.** And thus I believe that your proposed license,
> by making explicit that patent rights are not granted for a large class of binary derivatives of
> the program, violates **most of the OSD rules, not just rule number 7**."*

**これは `against.md` #236 が集めた「OSD は明示的な特許許諾を要求していない」という 4〜6 人の
読みに対する、最も強い反対である** ——しかも**その文書を書いた本人**から出ている。

**同じ趣旨を、別の人が別の角度から述べている。** Matthew Flaschen 氏 2009-04-08 ——
*"No provision of the OSD **explicitly** requires any specific grant of intellectual property.
There is no mention of copyright, patent, or trademark in the OSD. **So saying, the OSD doesn't
require patent grants makes no sense. It doesn't require copyright license grants explicitly
either.** In practice, **both** copyright and patent rights must be granted in order to ensure the
actions listed in the OSD are possible."*

**この形の反論は、#236 の読みを「誤り」とは言わず「無意味」と言う** ——
**OSD は著作権についても明示していないのだから、「明示していない ⇒ 要求していない」は
どの権利についても成り立たない。**

### どの条で切られたか —— OSD 7

Russ Nelson 氏（当時 OSI）—— *"This license **obviously does not comply with the Open Source
Definition's term #7**, Distribution of License."*
Chuck Swiger 氏 —— OSD 7 の *"without the need for execution of an additional license by those
parties"* を引き、*"suggests that the contributors don't really intend to open-source their stuff
in the first place."* Lawrence Rosen 氏 —— *"the MXM Public License doesn't pass the OSD test."*

**ACD-1.0 には当たらない** —— §8 が明示的に許諾し、§10.1 が条件を付けず、
§8.2 が *"subject to no condition"* と述べる。**だが「どの条で切られるか」を知っているのと
知らないのとでは、答え方が違う。**

### CC0 を止めた "on notice" の議論は、2012 年ではなく 2009 年に始まっている

Richard Fontana 氏 2009-04-08 —— *"this license clearly **puts the user on notice** that he/she may
need to pay patent royalties to the copyright licensor for exercising rights that OSI-approved
licences are supposed to provide."*

**`comparison.md` §1.4 は、この反対を 2012 年の CC0 撤回理由として記録している。
3 年早い同じ形が、同じリストに在った** ——**反対は CC0 に固有ではなく、類型に付いている。**

### 起草者が示した「OSD に適合する代案」は、条件付きの特許許諾だった

Perens 氏 —— *"You could, however, construct a license that is 1) fully compliant with the OSD and
2) **grants patent rights only for derivative works under that license**, and 3) spoils the
potential revenue stream from non-commercially-licensed derivatives as much as it can.
For example, **a patent grant that applies only to software under the AGPL3 license** ..."*

**⚠ これは `review-outcomes.md` §1.108 と #235 の読みに緊張を与える。**
そこでは **Intel の 2001 年 BSD+Patent が「GPL 系 OS に条件づけた特許許諾」を理由に OSD 3 / 6 / 8 で
争われ、無条件にした 2016 年版が承認された**と記録した。
**ここでは OSD の起草者が、ライセンスに条件づけた特許許諾を「OSD に完全に適合する」と述べている。**
**両立しないわけではない**（2001 年に争われたのは *特定の OS 実装* への条件づけで、
Perens 氏の案は *そのライセンスの下の派生物* への条件づけである）。
**だが「無条件だから通った」と単純化してはならない。**
**ACD-1.0 §8.2 が無条件であることは、依然として安全側の選択である。**

### この節が establish しないこと

**MXM は理事会の議決に至っていない** —— 記録に在るのはリスト上の評価と、
**提出者自身による 2012 年の総括**（*"as MXM is a copyright-only license, and **this is why, in my
recollection, it failed to be approved**"*・保存先は `2012-03-license-review-cc0-osd-patents-observed-*.txt`）
である。**「不承認」と書くときは、この出典が提出者本人の回想であることを併記する。**

## 1.112 特許について沈黙したライセンスは、反対を記録に残したまま承認されている —— W3C（2017）（2026-09-25）

一次資料は `rounds/1999-2024-license-review-w3c-software-license-observed-*.txt`（72 通・7 部）。
**Piana 氏が 2023 年に名指しした 3 件（CC0 / MXM / W3C）の最後の 1 件であり、
3 件のうち唯一「承認された」ものである。**

### 提出者は「著作権のみ」だと明言している

Wendy Seltzer 氏（W3C 顧問弁護士）2017-08-09 ——
*"**This is a copyright-only license. It makes no statement about the presence or absence of patent
claims covering the licensed works.** Copyright and patent are distinct regimes, so I don't believe
there's ambiguity in offering one without discussing the other."*

### 反対は記録され、承認は止まらなかった

Carlo Piana 氏 2017-08-11 —— *"If different rights insist on software, the owner of those rights
who purports to give permission **must** give those permission under all the rights she may have,
or the openness test would miserably fail. ... **A license which only gives copyright licenses but
refuses to do so for patents is not an open source license in my and many others' opinion.**"*

**しかし氏は保留を求めていない** —— 2017-08-16 *"I have acknowledged that the issue is of minimal
importance in the context of this particular license ... and **I have not asked to withhold
approval**. However, I still keep the point ... that the issue **whether an open source license can
openly exclude patent rights from the grants and still be called 'open source' must be resolved**."*

Nigel Tzeng 氏 —— *"**there is no red line for patents in the OSD.** Either get the necessary
consensus to change the OSD or **stop debating this in every single Open Source license submission
and holding them up**."* Lawrence Rosen 氏 —— *"This W3C copyright license is **the wrong
battlefield** to argue about patents ... OSI should please approve it."*

**Richard Fontana 氏が 2017-10-26 に承認を勧告し、2017-11-29 に承認された。**

### なぜこれが #238 の 3 段構造を強めるのか

**#238 は「沈黙は許され、明示的な除外は致命的で、明示的な許諾が実務の標準」と書いた。
1 段目の根拠はそれまで「発言」だけだった。ここには承認がある** ——
**同じ反対者（Piana 氏）が、沈黙には保留を求めず（W3C・2017）、
明示的な除外には OSD 違反だと述べている（MXM・2009 / MulanOWL・2023）。**
**1 人の中で線が引かれており、線の位置は「沈黙 / 除外」の境目にある。**

**⚠ ただし Piana 氏の 2017 年の文は「未解決だ」と言っている。**
**「沈黙は許される」は、争わないという運用であって、決着した規則ではない。**

### 特許の除外が持ち出される条は、時期によって違う

**OSD 7**（Nelson 氏 / Swiger 氏 / Rosen 氏・2009・MXM）/ **"most of the OSD rules"**
（Perens 氏・2009・§1.111）/ **OSD 1**（McCoy Smith 氏・2024・W3C の IP disclaimer 条項について
*"would allow this license to include disclaimers that would make it violative of OSD 1"*）。

**ACD-1.0 はどれにも当たらない** —— §8 が明示的に許諾し、§8.2 が *"subject to no condition"*、
§10.1 が条件を付けない。**だが提出文は OSD 3 / 5 / 6 / 9 しか名指ししていなかった**
（review-process ページが求める 4 つ）。**記録上、特許まわりの反対が実際に持ち出される条は
OSD 1 と OSD 7 である** ——**満たしている条を名指ししない理由が無いので、1 文足した**
（`submission.md` §B.0）。

### 25 年分を束ねたので、別の時代の事実も 1 つ入っている

**2001 年、W3C の提出は 19 か月放置されていた**（2000-01 提出 → 2001-08 時点で未処理）。
Russ Nelson 氏の答え —— *"Why isn't it approved? Because we got hideously backlogged. ...
**if you want it approved, and you've submitted it and haven't heard from us, resubmit it.**"*

**⚠ これを我々の沈黙への処方として読んではならない。** 2001 年の運用には moderation が無く、
**我々の場合は moderator が「ACD-1.0 に関する further submissions の前に直接返信せよ」と
求め、その後も投稿が通っていない**（B14 / `ACD-OSI-BOTTLENECKS-POSTING.md`）。
**「再提出せよ」という処方が在ることと、我々がいま再提出できることは別である。**

## 1.114 「使用の制限は OSD に無い」—— リストが自分でそう言い、正確な形まで出している（2026-09-26）

一次資料は `rounds/2004-09-license-discuss-academic-citing-license-observed-*.txt`（36 通・3 部）と
`rounds/2001-06-license-discuss-qmail-osd4-observed-*.txt`（21 通・2 部）。

### OSD には「使用を制限してはならない」と書いていない

2004 年、科学ソフトの作者が「このプログラムを使った論文は特定の論文を引用すること」という
条件を付けたいと相談した。Evan Prodromou 氏の答え ——
*"as the copyright holder, you have limited rights to tell people how they can use your software. ...
**Why isn't it part of the OSD, you may ask? I'm not sure.** My guess is that it was assumed that
since copyright holders don't have the right to tell people how to use their software, that
shouldn't show up in licenses anyways."*

**そして同じ人が、数日後に自分の言い方を正している** ——
*"It's a mistake on my part to use the imprecise short phrase 'no restrictions on use'.
**It'd be more accurate to say 'no restrictions on use not covered by copyright law.'**"*

**ACD-1.0 にとっての意味は 2 つある。**
**(1)** §10.1 は**どんな条件も付けない**ので、この線のどちら側かを判定する必要がない。
**(2)** §1.5 の Covered Rights は *"rights in performances"* を**明示的に含んでいる** ——
同じスレッドで Moen 氏と Poole 氏が「プログラムの実行は public performance か」で決着せず
（Moen 氏「米国著作権法の performance rights は音楽・photoplay 等に限られ software には及ばない」/
Poole 氏「WIPO 著作権条約は computer programs を literary works として保護し、Berne は
literary works の public recitation を留保している」）、**Rosen 氏が実務的な答えを出している**
—— *"If you want to 'perform' software, **the OSL expressly allows it just as it expressly allows
'use'**, so there's no need to worry about whether it is a performance or a use."*
**ACD-1.0 は §3・§4 が Covered Rights 全体を対象にし、その定義が performances を名指しするので、
同じ「心配しなくてよい」側に立っている。**

### 2004 年にも「OSD には適合する。だが承認はしない」が出ている

Stephen North 氏 —— *"Though I'm not a fan of this proposal, **doesn't it conform to the Open
Source Definition?**"* 提出者の返し —— *"Oh yes, someone please say '**It conforms to the OSD.
Nevertheless, we won't approve it as it restricts the use.**'"*

**#248（OSD 適合は十分条件ではない）の、13 年早い同じ形である。**

### 条件は「あるかないか」ではなく「どこまで厳しくできるか」で見られている

2001 年の qmail スレッド。Behlendorf 氏 *"Every license has a list of conditions attached to those
rights they grant, even the BSD/MIT licenses."* に対し、John Cowan 氏 ——
*"a claim that 'X must allow Y' is satisfied by a statement by X that 'Y is allowed under
conditions Z' **can't be true in general, since the conditions Z can be arbitrarily restrictive**."*

**ACD-1.0 §10.1 は条件を 1 つも持たないので、この議論の対象にならない。**
**これは「強い」からではなく「議論の前提である条件が存在しない」からである** ——
**§10.1 の価値は、争点を作らないことにある。**

### OSD 3 の後半は、実際に判定の決め手として使われている

Rick Moen 氏 2001-06-07 —— *"**OSD clause #3, immediately preceding, strikes me as disambiguating
this.** ... Although a copy of qmail compiled from modified source is a derived work, **it may not
be distributed under the same terms as the original** (as clause #3 says must be true for OSD
compliance)."*

**我々が 2026-09-13 に §16.3 で埋めたのは、この後半である**（`against.md` の「OSD 3 の後半に
答えていなかった」件）。**25 年前の実例が、その後半が飾りではないことを示している。**

## 1.117 データ保護法にライセンサーは登場しない —— §1.5 がデータ保護を Covered Rights に含めない理由が、外から裏づく（2026-09-27）

一次資料は `rounds/2020-12-license-review-viratrace-gdpr-observed-*.txt`（35 通・6 部）。
ViraTrace Public Source License（COVID 接触追跡・2020-12）は「GDPR / HIPAA 準拠のために
ライセンスで下流を制御する」ことを目的として提出され、OSD 違反を複数指摘された。
**委員長が議論を `license-discuss` へ移し、「GDPR とライセンス条項の交点」という一般論になった。**

### 実務家の一文

Roland Turner 氏（Chief Privacy Officer・2020-12-11）——

> *"It is my understanding that **data protection law in most jurisdictions is about the legal
> obligations of organisations in control of personal data** both with respect to that data and to
> people that it relates to (and often to regulators), and legal/contractual obligations of other
> organisations **processing that data on their behalf**; **software licensors are not part of the
> picture**."*

**ACD-1.0 §1.5 は Covered Rights に著作権・実演・放送録音・sui generis データベース権・
不公正抽出に対する権利を挙げ、データ保護・privacy・publicity・personality を挙げていない。**
**§11.4 は *"It reaches nothing else. It grants no permission ..."* と述べる。**
**これは欠落ではなく、権利の種類の違いである、という読みをこの一文が支える** ——
**ライセンサーとしての地位は、データ保護法が規律する地位（controller / processor）ではない。**

**⚠ そのまま安心しない。** Turner 氏が述べているのは **licensor qua licensor** についてであり、
**ACD が対象にする Work にはデータセットが含まれうる**（§1.2 の列挙）。
**個人データを含む Work を公開する者は controller になりうる** ——
**そのとき義務は ACD の外で発生し、ACD は何も与えず何も免除しない。**
**この区別を提出文で述べていない**（errata が「列挙に無い」と記録しているだけ）。

### 「規制準拠のためにライセンスが要る」は、この場では通らなかった

Brian Behlendorf 氏 —— *"**boutique licenses are not required for either GDPR or HIPAA
compliance**"*。Lukas Atkinson 氏 —— 下流の製品にまで同じ水準を課すことは
*"clearly has a **discriminatory effect** (e.g. when considering use in jurisdictions where neither
GDPR nor HIPAA applies)"*。

**ACD-1.0 には当たらない** —— **§10.1 は何の条件も課さず、下流に何も要求しない。**
**だが「規制が動機なら新しいライセンスが要る」という形の主張は、この場で否定されている**ことは
覚えておく価値がある ——**我々の gap の一部（TDM の留保・学習の許諾）は規制に隣接する。**
**我々の主張は「規制準拠のために要る」ではなく「既存の許諾が機械に読めない」である**
（§6.5）。**この違いを崩さないこと。**

### 「OSD には書かれていないが内在する」を、委員がもう一度述べている

McCoy Smith 氏 2020-12-10 —— *"definition of 'Deploy' includes internal only use. This violates
**Freedom Zero**, which I believe is, and have argued before is, **inherently, part of the OSD**.
Given this question has come up more than once recently, **might it be time for OSI to clarify
this point?**"*

**#248（Cowan 氏 / Perens 氏 / Villa 氏）と #251（Prodromou 氏）に続く 5 人目で、
Licensing Committee の委員である。** **そして氏自身が「明確化すべきでは」と問うている** ——
**書かれていない基準が在ることは、内部でも認識されている。**

## 1.123 公表されている新規ライセンスの基準「licensor を構造的に優位に置く条項を持たない」が、実際に条項へ当てられた —— ModelGo Attribution 2.0（2026-09-20〜22）（2026-09-27）

**⚠ まず訂正から。この節の初版は「適用された実例を 1 つも持っていなかった」と書いたが、それは誤りである。**
**2026-09-24 に別セッションが同じ適用を `review-rules.md` 行 2 へ記録していた**（オーナーが渡した
アーカイブ経由）。**書く前に grep していれば分かった** —— 本ドシエが何度も記録している当の失敗で、
**近いものほど確認が省かれる**（`against.md` #92）。

**この節が足すのは、結論ではなく導出である。** 行 2 は**結論**（当たらない）と**結末**（提出者が翌日
条項を改めた）と **§16.4 の露出**を記録している。**逐語の経緯も、下の逆側 4 つも、そこには無い。**
2026-09-16〜09-24 の FINAL CALL にそれが在る（逐語は
`rounds/2026-09-24-license-review-modelgo-final-call-observed-{1,2,3}of3.txt`）。

**経緯は 3 手である。**

**(1) McCoy Smith 氏（2026-09-16）が OSD 5 として立てた。** ModelGo の終了条項は
*"if You initiate any legal action **against the Licensor** alleging that the Licensed Materials
and/or Derivative Materials infringe any patent worldwide"* と書く。氏は「Licensor は許諾する
権利者だけを指すので、**Licensee に対する特許主張では終了しない**」と読み、
*"This puts Licensors & Licensees in **different positions** vis a vis patent assertions, and
therefore **arguably violates OSD 5**"* と述べた。**対照として、Apache-2.0 / MPL-2.0 / EPL-2.0 /
GPL-3.0 はいずれも引き金を *"any entity"*（＝当事者ではなく**対象著作物**）に置いていることを
逐語で並べている。**

**(2) steward は「Licensor は役割であって人ではない」と答え、現行文言の維持を求めた。**

**(3) 委員長 Pamela Chestek 氏（2026-09-20 / 09-22）が、その答えを退けた。**
まず当事者を 4 類型（Licensor / 非頒布の利用者 A / 頒布する利用者 B / 特許権者 C）に分解し、
C が A や B を訴えても終了しないことを示して *"**That is the discrimination**"* と書く。
そのうえで **09-22 に基準を名指しした**:

> *"I also note that the one of the requirements for new licenses is "The license does not have
> terms that **structurally put the licensor in a more favored position than any licensee**."
> **This does put the licensor in a more favored position than a licensee.**"*

### ACD はこの基準にどう当たるか

**当たらない。理由は「条件が 1 つも無い」ことに尽きる。**
§10.1 が条件を置かず、§10.4 が終了を置かないので、**終了しうる地位を持つ当事者の類型が
そもそも存在しない**。ACD の構造は **Dedicator が一方的に与え、受領者に何も要求しない**
（§3 の献呈 / §4 の無条件並行付与 / §8 の特許許諾はいずれも一方向）。
**基準が禁じるのは licensor が*優位*に立つことであり、ACD で非対称なのは Dedicator が
*不利*に立つ向きである。**

### ⚠ 逆側（3 つ・同じ音量で書く）

**(a) §13 / §14 は Dedicator の側を守る。** 無保証と責任制限は Dedicator にだけ利益がある。
**委員長の適用は*権利*の非対称に向いており免責条項には届いていないが、それは沈黙であって
判断ではない**（承認済み 141 本すべてが同種の条項を持つことは**「皆やっている」型の弁護**で、
本ドシエが他所では信用しない形である）。

**(b) 「意図的だ」という答えは事態を悪くする。** 委員長は steward の説明に対し
*"Your response is **quite troubling to me**. I read it as saying that the disparate treatment …
is **intentional**"* と応じた。**ACD-1.0 §8.2 は特許報復の不在を *"deliberate"* と明記している。**
向きは逆（ACD が意図的に手放しているのは *licensor を守る*機構の方）だが、
**「意図的である」は適合の問いへの答えにならない**という一般形はそのまま我々に当たる。

**(c) 自分の instrument を承認済みライセンスから構造で区別する主張は退けられうる。**
委員長は *"**All licenses are "single grantor,"** Apache included"* と、steward の区別立てを
正面から否定した。**提出パケットが ACD の構造的な新しさを述べる箇所は、この読みに耐える
必要がある。**

**(d) そして、我々にも licensor 側の留保が 1 つある** —— **1.1 / 1.2 草案の §16.4 は、改変した
テキストを同じ名前・識別子で頒布することを Steward にだけ許す。** §16.6 が「本著作物の条件ではなく
受領者を拘束しない」と定める**文書の版管理**についての留保で、利用者の権利は狭めない。
**だが基準の文言に対して読まれうる箇所であり、`review-rules.md` 行 2 と `against.md` #221 が
2026-09-24 から記録していた。本節の初版はそれを落としていた** ——**免責（(a)）より先に挙がるべき
項目で、こちらのほうが基準の文言に近い。**

### この節が establish しないこと

**ModelGo の帰結はまだ出ていない**（2026-09-24 に steward が GitHub のテキストを更新した
段階で、**大学サーバー上の複製は古いまま**だと自ら述べている）。
**「当たらない」と確かめられることは、ACD が承認されることを意味しない**（`board-decisions.md`
の 2 つの天井 —— *"even where they cannot identify a specific aspect of the OSD"* と
*"prior approval … does not bind"* —— は動かない）。

## 1.125 「1 本で全部を覆う」への批判を、ACD の条へ 1 つずつ当て直した —— 当たらないが、理由は「束ねていない」ことではない（2026-09-27）

**`against.md` #266 が要求した作業である。** §1.78 (a) は「束ねの OSD 9 は ACD に当たらない」と
書いたが、**根拠を 1 行で済ませていた**。Fontana 氏の 2026-09-11 の本体
（`rounds/2026-09-14-license-review-openmdw-thread-observed.txt`）を読み直すと、
**批判の形は「束ねること」ではない。**

> *"The **asserted policy justification** for copyright-triggered termination **has no relevance
> to latex2html.py**, and yet it is **swept in improperly** by this termination provision. …
> OpenMDW-1.1 is **flawed in its basic conception**, as a consequence of the termination
> provision. **Its whole raison d'être is to have a single license that applies to everything.**"*

**一般形はこうである** ——
**(i) instrument が異種の素材を 1 語に束ね、(ii) その中に「一部の素材にしか正当化が及ばない
条項」があると、(iii) 束ねがその条項を正当化の及ばない素材まで運ぶ。**
OpenMDW では (ii) が**終了**で、運ばれた先は「事前学習済みの重みとは無関係な Python script」だった。

### ACD の条へ 1 つずつ当てる

**(i) は ACD にも当たる。** §1.2 は source code / object code / documentation / data /
metadata / audiovisual material を 1 語に束ねる。

**(ii) が当たらない。** 素材ごとに正当化が違う条は ACD にもあるが、**その全部が
「義務を外す」か「許諾を足す」側にしか働かない**:

| 条 | 正当化が及ぶ素材 | 及ばない素材に運ばれると何が起きるか |
| :-- | :-- | :-- |
| §6（機械生成物・出力） | AI の出力 | **何も起きない。** §6.4 は *"You owe nothing in respect of any of them"* ——**外す側**である |
| §7（データベース権） | データ集合 | **空振りする。** sui generis 権が生じない素材では対象が無い |
| §9（機械生成著作物の権利の存否） | 機械生成物 | **空振りする。** 不確実性を除く条で、義務を作らない |
| §12（人格権） | 著作物 | **Dedicator 側が更に手放すだけ。** 受領者は何も失わない |
| §8（特許） | 全素材 | **素材固有ではない**（Apache-2.0 も Work 全体に及ぶ・Dolan 氏 2026-09-14） |

**したがって (iii) が起こらない。** ACD が束ねて運ぶのは**許諾だけ**で、
**受領者から何かを取り上げる条が 1 つも無い**（§10.1 が条件を、§10.4 が終了を置かない）。
**批判は「不利益が正当化の外へ運ばれること」を問題にしているので、運ぶ不利益が無ければ成立しない。**

**⚠ 「束ねているから安全」ではない。安全なのは「不利益が無いから」である。**
§1.78 (a) の一行の根拠は正しかったが、**正しい理由を述べていなかった** ——
「終了が無い」は結論であって、**なぜそれで十分かは上の表を書くまで示されていなかった。**

### ⚠ 逆側 3 つ

**(a) 過剰に広い*許諾*は、別の種類の欠陥になりうる。** 持っていない権利について献呈すること
（§2.7 が Dedicator 自身の権利に限り、§2.6 が第三者素材の特定を Dedicator の義務とする）。
**Berkus 氏が同日に挙げた 8 経路**（*"GenAI & Autocomplete"* を含む・偶発的な混入は常時起きる）
は、**束ねが運ぶのが不利益ではなく*リスク*である**ことを示す。**これが実際の残余で、#134 そのものである。**

**(b) Fontana 氏は OSAID を引いて、素材の種類で線を引いている** ——
*"the OSI contemplates that things other than OSI-approved licenses might be suitable for
**model parameters**, but **that does not apply to code or model architecture materials**"*。
**B15（主題適格）に直接効く**: パラメータ側については「そもそも OSI 承認ライセンスの仕事ではない
かもしれない」という読みが、審査者の側から出ている。

**(c) そして B15 の counterweight の 1 つが、同じ 1 通で弱められている。**
`against.md` #237 は「OSI はフォント（IPA）とデータを名に持つライセンス（Unicode）を承認している」
を counterweight に使っているが、**Fontana 氏は OFL-1.1 を名指しで *"wrongly approved"* と述べ、
自分が 17 年前にその承認を後押ししたことを謝罪している**。
**承認されたという事実は残るが、先例としての重さは、承認する側の 1 人がそう言っている分だけ軽い。**
**有利な読みの反証を同じ段落で探した結果であり、探さなければ出なかった。**

## 1.127 「提出されたライセンスは、OSD だけでなく*その約束*に照らしても評価される」—— Ms-PL 審査（2007）で当時の OSI 会長が述べた評価関数（2026-09-27）

**#243 の census が挙げた最大の未読スレッド**（"For Approval: Microsoft Permissive License"・
331 通・2005-12〜2007-10）から、**決める側の 26 通**を規則を明記して読んだ
（逐語は `rounds/2007-09-license-discuss-ms-pl-decision-makers-observed-1of3.txt` ほか 3 部）。
**優先順位を通数ではなく「決める側が何を述べたか」で決めた**のは #243 の潰し方に従ったものである。

### 🔴 不利な側 —— gap は存在理由であると同時に、測られる基準にもなる

Michael Tiemann 氏（当時の OSI 会長・2007-09-26）:

> *"I do believe that **if a license is submitted with promise X, then we should evaluate
> promise X as well as the OSD**. If the only promise of the license is 'we meet the minimum
> terms of the OSD, and nothing more', then we should not hold it to a higher standard.
> **This is my personal opinion, not a defined board policy**, but I think others use a
> similar evaluation function."*

**ACD は OSD の最低限だけを約束してはいない。** PREAMBLE と §6.5 は**機械が判定できる許諾**を、
§3 + §4 は**公有化と等価な地位を、§3 の有効性に依存せずに**、§8.4 は**学習済みモデルと出力まで
届く特許許諾**を約束する。**ドシエはこれらを「なぜ既存で埋まらないか（基準 7）」の側からだけ
書いてきた** —— **それが同時に「我々が満たしているか測られる項目」でもある、とはどこにも書いて
いなかった**（`against.md` #269）。

**同じスレッドに、その評価が実際に働いた例がある** —— Tiemann 氏は、ある承認済みライセンスが
*"GPL with training wheels"* を名乗った以上 **GPL 互換でなければ「約束したことをしていない」**
ので、互換性が確認できて初めて承認した、と述べている。**約束の内容そのものが合否の一部になった。**

**⚠ 逆側 3 つ。** **(1)** 本人が *"my personal opinion, not a defined board policy"* と明記している。
**(2)** 2007 年の会長の発言であり、2026 年の委員会が同じ関数を使う保証は無い。
**(3)** **同じ規則は有利にも働く** —— 最低限しか約束しないものを高い基準で測ってはならない、
という半分は、**過剰な要求から提出者を守る向き**でもある。

### 🟢 有利な側 —— vanity の異議には「再利用できるか」で答える

Russ Nelson 氏（License Committee 委員長として、2007-09-06 の論点要約）:

> *"Ross Mayfield suggests that the name implies that it's a vanity license -- but **the OSI
> board does not give that argument much weight as long as the license is reusable**. We allow
> people to give and take credit in the name of the software, so applying the same principle
> to licenses seems appropriate."*

**提出パケット §4b はこの項目に正面から答えている** —— 本文の固有名詞 0・条項の置換テキスト 0
（§16.1 の notice 雛形の 1 欄を除く）・採用に本文編集が 1 箇所も要らない・利用者類型 5 つ。
**vanity をめぐる我々の既存の材料は Kuhn 氏の 2 段テスト（*"widespread need"* ∧ *"wholly
unserved"*）で、前半に我々は答えられない**（#255）。**本節はそれとは別の、より古く、
かつ我々が満たせる定式である。**

**⚠ 逆側 3 つ。** **(1)** *"not much weight"* は「無視する」ではない。
**(2)** 2007 年の理事会であり、Kuhn 氏の定式は後年のものである ——**新しいほうが後で述べられた**。
**(3)** Ms-PL の背後には Microsoft があり、**再利用可能性だけが通した要因ではない。**

### 🟡 そして #268 の機構が、別の年・別の議長で再現している

Nelson 氏は名称への異議にこう答えている ——
*"Will the name mislead anybody? **Not after this discussion, it won't.**"*

**#268 は CAL（曖昧さを容れて承認）と Project Tick GPL（曖昧さを理由に否決）の対から、
「曖昧さ自体ではなく、議論で解けないことが致命である」を引き出した。**
**本節はその機構の、2007 年・別の議長による独立した 2 例目である** ——
**異議は議論を通ることで無害化される、と述べているのは我々ではなく決める側である。**
**そして議論を通るには、議論の場に居なければならない（B14）。**

### この節が establish しないこと

**Ms-PL は承認された**が、**それは我々の類型の先例ではない**（許容型・企業 steward・採用は
その時点で既に広い）。**本節が establish するのは 2 つの*規則の言い方*だけ**で、
**どちらも、当てはめた結果を保証しない。**

## 1.128 依拠している先例に逆らった側を読んだ —— 反対は「テキストが通るか落ちるかの試験」の形で述べられており、ACD-1.0 はそれに通る（2026-09-27）

**Unlicense は本ドシエが依拠している唯一の「献呈 + 許諾」型の承認先例**である。
**その理由書は `AS-OF.md` が逐語で持っていたが、逆らった側の議論は持っていなかった**
（`veto against Unlicense`・2020-05-16〜06-03・全 17 通を
`rounds/2020-05-license-review-unlicense-veto-observed.txt` に保存）。

### 反対は試験の形で述べられている

Stuart Langley 氏（実務弁護士・自らそう名乗っている）:

> *"Unlicense falls on the side of '**this is not a license**' to me largely because I read the
> second paragraph as **a description of what the author thinks public domain means, not a
> clear intent to convey rights**."*
>
> *"I would never advise a client to sign a commercial license that did not have
> **conventional, well-trodden language of license such as 'Licensor grants X rights....'**"*

**これは意見ではなく、当てれば答えが出る試験である。** 当てた結果:

| | |
| :-- | :-- |
| **ACD-1.0 §4.1** | *"**The Dedicator grants You** a worldwide, royalty-free, non-exclusive, irrevocable, perpetual, sublicensable, and transferable licence to exercise all Covered Rights in the Work for any purpose whatsoever."* |
| **§8.1 / §8.4**（特許）| 同じ動詞 —— *"The Dedicator grants You …"* / *"The Dedicator further grants You …"* |
| 本文中の `grant` 系の語 | **12 箇所**（実測） |

**Unlicense が落ちたと言われた当の点で、ACD-1.0 は落ちない。**
しかも **§4.4 は許諾が §3 の有効性に依存しないと明言する**ので、
**「献呈の意思の記述」と読まれる余地は、Unlicense より構造的に狭い。**

### ⚠ 逆側 4 つ —— この試験に通ることは、承認の予測ではない

**(1) 同じ反対者が、別の要素も挙げている** —— *"risk perception is relative and **wide use
without any problems is a big factor** in getting comfortable with any particular wording"*。
**そちらに我々は答えられない**（B2・採用 1 件）。

**(2) 反対は承認を止めなかった** —— Unlicense は 2020-06-12 の理事会で承認され、
**Langley 氏は最後まで *"I still will advise against using software encumbered with the
Unlicense"* と述べている。****有力な反対が残ったまま承認は通る**（有利）が、
**同じことは「我々に有利な意見が残っても否決は通る」を意味する**（不利）。

**(3) 承認を運んだのは弁護士たちの一致であって、テキストの形だけではない** ——
委員会の理由書は *"**The lawyers who opined on the issue, both US and non-US, agreed** that
the document would most likely be interpreted as a license and that the license met the OSD"*
と述べる。**B1（法的レビュー不在）に対する最も鋭い形がここにある** ——
**我々が依拠する先例は、まさに我々が欠いているものによって線を越えた。**
そして**その一致はリスト上の議論で生まれた**ので、**#268 の機構の 3 例目**でもある
（CAL 2020 / Ms-PL 2007 に続く）——**議論の場に居られないこと（B14）の費用がまた 1 段上がる。**

**(4) category は提出者の希望どおりにならなかった** —— 提出者は
*"Popular and Widely-Used or With Strong Communities"* を求めたが、委員会は
*"**because of its intended nature as a dedication to the public domain**, that it be placed
in the '**Special Purpose**' category"* と勧告した。**献呈という性質そのものが category を
決めている**ので、**ACD も同じ扱いを受けうる**と見ておくべきである（CAL は *"Uncategorized"*）。

### この節が establish しないこと

**「試験に通る」は「承認される」ではない。** Langley 氏の試験は**彼の**試験であり、
委員会の基準ではない。**確立するのは 1 点だけ** —— **Unlicense に向けられた最も具体的な
起草上の異議は、ACD-1.0 の条文には当たらない。**
