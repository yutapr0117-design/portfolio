---
file: LICENSES/ACD-1.0.review-outcomes.md
audience: OSI license-discuss / license-review participants, licence reviewers, 監査人
last-updated: 2026-09-27
canonical-ref: LICENSES/ACD-1.0.review-precedents.md (提出そのものの読み) / LICENSES/ACD-1.0.board-decisions.md (理事会議事録の分析) / LICENSES/ACD-1.0.against.md
---

# OSI 側が何をしたか、何を述べたか —— 議決・運用・承認後の扱い・留め置き

**`ACD-1.0.review-precedents.md` から 2026-09-27 に切り出した。引き金は Check 365 の 1,000 行上限だが、
割る線は行数ではなく主題で選んだ。**

**残した側（`review-precedents.md`）は「提出そのものの読み」** ——
その instrument が何を試み、リストが条文に何と言ったか。
**こちら（本 file）は「OSI 側が何をしたか・何を述べたか」** ——
理事会の議決とその理由、委員長の手続き運用、承認後にどう扱われるか、そして決まらない場合。

**`board-decisions.md` との違い**: あちらは**議事録という一次資料**からの分析、
ここは**メーリングリスト上に現れた OSI 側の言動**である。**同じ決定を両方から見ることがある。**

**節番号は変えていない**ので、既存の `§1.88` / `§1.108` / `§1.116` / `§1.118` という参照は
番号としてそのまま解決する。**file 名を添えている参照は向け直した。**

**この分け方の限界**: 提出の読みと OSI 側の言動は排他ではない ——
たとえば §1.108 は「Mulan の提出の読み」でもある。**境界は読み手の用途で引いてあり、
論理的に排他な分類ではない。**

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


## 1.116 理事会は準拠法条項を「必要でも望ましくもない」と述べて承認した —— そして弁護士が起草しても 11 か月・3 版かかった（2026-09-27）

一次資料は `rounds/2022-04-license-review-open-logistics-license-observed-*.txt`（106 通・15 部）。
**Open Logistics License**（Apache-2.0 を欧州法へ適合させたもの）は 2022-04 に提出され、
**2023-03-19 の理事会で承認**された（special purpose category）。

### 理事会が、承認の文言のなかで準拠法について立場を述べている

Pamela Chestek 氏 2023-03-18 ——

> *"The Board of the Open Source Initiative approved the Open Logistics License version 1.3 as an
> Open Source Initiative Certified license in the special purpose category of licenses at its
> March 19, 2023 meeting. **The Board did so with the comment that it does not believe that choice
> of law provisions are necessary or advisable in open source licenses.**"*

**ACD-1.0 §15.7 は準拠法も法廷地も置いていない。**
**ドシエはこれまで、その不在を「費用」としてだけ記録してきた** ——
`submission-reference.md` §4 は *"a plaintiff chooses the venue, and neither party can predict
which law governs"* と書き、2026-09-20 の外部レビューはこれを
*"the instrument's greatest systemic defect"* と呼んだ（`against.md` #170）。
**費用は消えないが、理事会自身の選好はこちら側に在る** ——
**置かないことが、置くことより不利だという証拠は無く、理事会は逆を述べている。**

**⚠ 過大に読まない。** 理事会が述べたのは *"necessary or advisable"* であって、
**「不在が有利に働く」とは言っていない。** §15.7 が抱える固有の問題（#23 が指摘した
「depeçage を宣言で作ろうとしている」読み）は、この発言では何も解決しない。

### 法律事務所が起草に同伴しても、承認まで 11 か月・3 版かかった

提出文自身が述べている —— *"The entire process of discussing and drafting the license was
accompanied by **BHO Legal, a German law firm specialized in IT law** ... The license was
subsequently **reviewed and approved by several in-house lawyers**."*

**それでも v1.1 → v1.2 → v1.3 と 2 度書き直され、106 通を要した。**
**B1（法的レビューが無い）にとっての意味は 2 つで、向きが逆である。**
**不利**: 弁護士が付いていてなお 3 版を要したのだから、**付いていない我々が一発で通る見込みは薄い。**
**有利**: **法的レビューは審査を短くしない** ——**「弁護士が居れば通る」でも「居なければ止まる」でもなく、
どちらの側でもリストは条文を読んで直させる。**

### vanity の判定基準が、2 段で述べられている

Bradley M. Kuhn 氏 2022-12-23 ——

> *"If a license submitter cannot make a clear and compelling case as to why their license serves a
> ***widespread* need for many different FOSS communities**, *and* explain how that need is
> **wholly unserved by all existing FOSS licenses** — then the license is almost surely just a
> vanity license. ... They come to OSI for its endorsement and **to build their own licensing
> credibility upon a foundation of OSI's credibility**. OSI-approval should always include the
> question ... **whether the license is in service to a broader FOSS community beyond the
> organization submitting it**."*

**これは B6（vanity）と B10（gap）を 1 つの連言にしたものである。**
**我々の答えは提出パケット §4b（本文に固有名詞ゼロ・採用に本文編集が不要）と gap census だが、
Kuhn 氏の基準は「提出者専用でないこと」より強い** ——**"widespread need" を求めている。**
**採用実績 1 件（B2）では、その語に届かない。**

### 開発者からの feedback が集まらない、という観察

Josh Berkus 氏 2022-12-23 —— *"developer feedback on this license is limited; **its entire reason
for existence depends on legal interpretation**, and I have nothing to contribute to that.
My one request is: ... somewhere this license needs **a FAQ that explains in developer
(non-lawyer) terms when I would want to use it**, in preference to the standard APL, and why."*

**ACD-1.0 も存在理由の大半が法的解釈である。** FAQ は既にある（`ACD-1.0.faq.md`）が、
**「いつ、なぜ、既存のどれの代わりに使うのか」を開発者の言葉で答える面としては読まれていない。**

### 改訂の手続きが、委員長の運用として記録されている

Pamela Chestek 氏 2023-01-21 —— *"**We will consider version 1.2 withdrawn and this a
resubmission.** The Decision Date for it will be 30 days after submission"*、
根拠として承認ページを引用 —— *"'Decision Date' ... (a) **60 days after a license is initially
submitted** ... and (b) **30 days after submission of a revised version**"*。

**`REVISION-PROTOCOL.md` §2 が記録している「審査中は変更せず、取り下げて新版を出す」は、
委員長が実際にそう運用した記録として裏づけられる** ——**改訂は取り下げと再提出として扱われ、
時計は 30 日で引き直される。**

## 1.118 「留め置き」の最長記録は 3 年半 —— そして公有化に著作権ライセンスを当てる危険と、§3+§4 を並置する理由が、同じ束に在る（2026-09-27）

一次資料は `rounds/2013-06-license-review-nosa-2-0-limbo-observed-*.txt`（225 通・23 部）。
**NASA Open Source Agreement 2.0** は 2013-06 に提出され、**2017 年 1 月の時点でまだ決まっていない。**

### 限定状態は、実在し、長い

当時の委員長 Richard Fontana 氏 2017-01-05 ——

> *"As some know, NOSA 2.0 has been **languishing in a limbo review state for an extremely long
> time**. In my opinion, NOSA 2.0 is, in its current form, **an overly complex and badly drafted
> license**. ... I also believed for a long time that **it was contrary to de facto OSI policy to
> reject a license outright**, as opposed to gently directing [submitters elsewhere]."*

**#139 が理事会の議事録から見つけた「第 3 の帰結」（承認でも否決でもない）は、
ここでは 3 年半の実時間として現れている。**
**`AS-OF.md` の「提出から決定まで中央値 101 日」は、決まった場合の値である** ——
**この束は、その分布の外に何があるかを示す。**

**Nigel Tzeng 氏はこれを手続きの問題として扱い、**
*"I would ask that the review process be amended that **licenses automatically go to an up or down
vote within 6 months of submission**"* と求めている。**その改正は行われていない。**

### 何が却下を正当化するか —— 元理事の整理

Luis Villa 氏 2017-01-09 ——

> *"I think rejection is perfectly appropriate for licenses that obviously violate the OSD or other
> ***clear, written, (ideally) objective* OSI policies**. However, **the OSD is frequently ambiguous
> or vague (e.g., patent grant?), other rules are completely unwritten (e.g., quality standards),
> and others were never actually adopted as rules (e.g., non-proliferation report)**."*

**そして実務の姿** —— *"my sense was that, except in egregious cases, **being poorly written and/or
duplicative was sufficient to delay and push for improvements, but not (ultimately) to block**"*。

**これは B3（長さ）・B6（vanity）・#84（重複）にとって、有利と不利が 1 文に同居している。**
**有利**: 起草の粗さと重複は、**遅延の理由ではあっても阻止の理由ではない**（元理事の実務感覚）。
**不利**: **遅延の実例が NOSA 2.0 の 3 年半である。** 採用ゼロの単独 steward にとって、
**3 年半の留め置きは否決より悪い**（時計は進み、B2 は改善せず、凍結は解けない）。
**そして氏は「特許許諾」を OSD が曖昧な例として名指ししている** ——
**#238 が「沈黙は許されるのは運用であって規則ではない」と書いた当のことである。**

### 公有化に著作権ライセンスを当てることの法的危険

Cem Karan 氏（米陸軍研究所）2017-08-28、同所の弁護士の分析として ——
**17 U.S.C. §506(c)**（*"Any person who, **with fraudulent intent, places on any article a notice of
copyright** or words of the same purport **that such person knows to be false** ..."*）を引き、
**著作権が存在しない著作物に著作権ライセンスを当てることが copyfraud にあたりうる**と述べている。

**ACD-1.0 の答えは §2.7 である** —— **Dedicator が保持する権利にしか及ばない。**
**§3 も §4 も「存在する限りにおいて」しか作用しないので、存在しない権利を主張する構造になっていない。**
**この危険を名指しした一次資料を、ドシエは持っていなかった。**

### そして §3 と §4 を並置する理由が、同じスレッドに在る

Thorsten Glaser 氏 2017-08-28 —— *"How is their position if the works are in the Public Domain
**only in the USA**? Their own copyright FAQ says that **even US government work may be
copyright-protected e.g. in Germany**. So, in the end, **we need a copyright licence period**."*

**これは ACD-1.0 §4.4 の設計理由そのものである** ——
*"granted independently of Section 3 and does not depend on Section 3 being ineffective"*。
**公有化が或る法域で効かない可能性があるから許諾を並べる、という判断を、
2017 年に別の人が別の文脈で同じ結論として述べている。**
**⚠ ただし氏が述べたのは「だから著作権ライセンスが要る」までで、
「献呈と許諾を並置せよ」ではない。** **並置の設計は我々のもので、裏づけは半分である。**

## 1.119 OSI は「data files」を主題に明記したライセンスを 2 度承認している —— そして「一般化」と「空欄つき本文」で通った先例が在る（2026-09-27）

一次資料は `rounds/2017-11-license-review-unicode-data-files-observed-*.txt`（16 通・3 部）。

### 承認は 2 度

**(1) 2018-09-03**、Richard Fontana 氏 —— *"The OSI board approved, for **Legacy Approval**, the
**Unicode Data Files and Software License** ... to be associated with the proliferation category
**'Licenses that are redundant with more popular licenses'**."*

**(2) 2023-11-28**、Pamela Chestek 氏 —— *"The **Unicode License v3** was approved as an OSI
Certified License in the **Special Purpose category** of licenses at its Board meeting on November
17, 2023. **The previous version of the license will be marked as superseded.**"*

**主題は名前に書いてある** ——*Data Files and Software*。
**B15（主題適格）にとって、フォント（`review-precedents.md` §1.110）に続く 2 つ目の counterweight。**
**2023 年の Mulan 不承認（*"open culture licenses are outside the purview"*）と並べると、
線は「コードか否か」ではなく、Chestek 氏の言う *"tied to software"* に引かれていることが
2 例で見える。** **⚠ それでも線の位置は分からない** —— Unicode のデータは
**ソフトウェアが消費する技術的データ**で、§1.2 が名指しする *"audiovisual material"* とは距離がある。

### 「一般化」を目的として明記した提出が、承認されている

McCoy Smith 氏 2023-08-23（Unicode Consortium を代理して）—— 改訂の目的として
*"to address certain suboptimal terms in the license, and **to genericize it so that it may be used
by entities other than the Unicode Consortium**"*。

**提出パケット §4b（本文に固有名詞ゼロ・採用に本文編集が不要）は、
「一般化されていること」を承認に向けた美点として述べている。**
**ここにそれを目的として掲げて通った先例が在る。**

### 空欄のある本文が、そのまま承認対象になっている

同じ提出文 —— *"note that that copy is slightly different than the copy submitted for approval,
in that it contains a Unicode copyright notice with relevant years; **for the text submitted for
approval by OSI, the copyright notice and years have been indicated as 'fill in the blanks.'**"*
Fontana 氏も 2017 年に同じ方向を示している —— *"the appropriate thing to do ... would be to
**templatize the date** (as has been done with certain OSI-approved licenses)"*。

**ACD-1.0 §16.1 の notice 雛形には 1 欄の空欄が在り、
提出パケット §4b はそれを「唯一の例外」として明示している**（2026-09-24 訂正）。
**その例外が異例ではないことの先例である。**

### 名前の条項がどこまで及ぶか —— 2 人の読みが割れている

Bruce Perens 氏 2017-11-29 —— *"the name of a copyright holder shall not be used in advertising ...
If we consider that 'Unicode' alone is also the protected name of the copyright holder, this would
appear to **prohibit anyone from stating in advertising that their product is compatible with
Unicode**. Certainly this is not what you want."* ——ただし *"I would not ask to block it upon that
point"*。
Richard Fontana 氏 —— *"**I did not read it as a blanket prohibition** on mentioning 'Unicode' in
an advertisement. I see it as equivalent to the ... 3-clause BSD"* の endorsement 条項。

**ACD-1.0 §11 は名称と商標を扱い、唯一撤回していない制限が
「entity 名で endorsement を偽装すること」である。**
**この往復は、その種の条項が「広すぎる」と読まれうることと、
それでも BSD-3 と同等なら通ることの、両方を示している。**

### 手続きの再確認

*"Decision date: due no later than the first Board meeting after October 23, 2023"*
（2023-08-23 提出の 60 日後）——**§1.116 で見た運用と同じ。**

## 1.120 英語としての不可解さは、実際に書かれた否決理由である —— そして「弁護士を雇え」の最も鋭い形が記録に在る（2026-09-27）

一次資料は `rounds/2022-03-license-review-yateam-not-approved-observed-*.txt`（9 通・5 部）と
`rounds/2019-05-license-review-master-console-withdrawn-observed-*.txt`（15 通・2 部）。

### 否決の Rationale Document、逐語

YATeam Public License v1（2022-03 提出 → **2023-09-15 の理事会で不承認**）——

> *"Resolved that it is the opinion of the OSI that the YATeam Public License Version 1 **does not
> conform to the OSD and assure software freedom** and the license is therefore not approved."*
>
> Rationale Document: *"This license is an attempt to create a license where the licensor can
> choose what options to invoke. However, in Section 4 the license allows adding restrictions that
> do not comply with the OSD ... **Unless a license meets the OSD in every possible iteration, it
> cannot be approved as an open source license.** **The license is also unintelligible in the
> English language version.**"*

**2 つ在る。**
**(1) *"in every possible iteration"*** —— **選択肢を持つライセンスは、すべての組合せで OSD を
満たさなければならない。** **ACD-1.0 には選択肢が無い**（§10.1 は条件を 1 つも持たない）ので
**構造上あたらない** ——**これは「強い」からではなく「取りうる形が 1 つしかない」からである。**
**(2) *"unintelligible in the English language version"*** ——
**英語としての不可解さが、Rationale Document に書かれた否決理由の一つである。**
**B3（長さ）と B13（理解コスト）の、最も鋭い形。**
**⚠ ACD-1.0 の英語は「不可解」ではないが、それを我々が判定することはできない。**
`review-corpus.md` の代理指標（平均文長 27.3・最長 85 語・従属節 2 つ以上の長文 0 件）は
**読みやすさの代理であって、審査者の心証ではない。**

### 二言語の扱い —— 2 人が別々の理由で同じ結論に至っている

Russell Nelson 氏 —— 中国語が正文で英語が訳、という構造は *"untenable"*。
*"The proper way is '**I cut the cake, you pick the piece**.' ... YATeam allows the defendant to
choose whichever language version they want."*
Pamela Chestek 氏 —— *"I believe it's also true that **some countries won't respect the choice of
version stated in the license** and will only enforce the local language no matter what the license
says about it. So perhaps the lesson is only that **translations shouldn't be part of the formal
agreement**."*

**ACD-1.0 §15.8 は英語を正文と定め、翻訳を本文の一部にしていない。**
**ドシエの大半は日本語だが、それは instrument の外に在る**（`REVIEWERS.md` が英語の入口）。
**この構図は、上の「教訓」をそのまま満たしている。**

### 「弁護士を雇え」の最も鋭い形

Bruce Perens 氏 2019-05-28、Master-Console の提出者に向けて ——

> *"It's obviously not the product of a lawyer. I have previously worked on the case **Jacobsen v.
> Katzer**, in which an Open Source developer paid **tens of thousands of dollars in losses and
> five years of hardship in court** because he relied on the Artistic License ... rather than a
> license from an attorney. These licenses are very unlikely to do what you expect when a judge
> goes to parse them — which is the only purpose of a license. Thus, **it is an active disservice
> to the programmers of the world** to present them with a license which is unlikely to work as
> they expect in court, and is likely to cause them damages. **So, please get a lawyer to write a
> license for you.**"*

**B1 の最も強い表現である** ——**害は「承認されないこと」ではなく、
それを採用した第三者が被る損害として述べられている。**
**ACD-1.0 は §16.3 と README で「誰でも使ってよい」と積極的に招いている。**
**その招きに対して、この一文は正面から当たる。**
**我々の既存の対処**（提出パケット §5 で法的レビューの不在を最初に述べ、
`LICENSE` にも来歴と不在を書いた・#67）**は、開示であって反論ではない。**
**⚠ 事実の訂正**: 氏は *"Artistic License Zero"* と書いているが、
Jacobsen v. Katzer で争われたのは **Artistic License** である。

### 委員長が示した経路は、我々がいま辿っている経路そのものである

Pamela Chestek 氏 2019-05-27 —— *"I suggest that you **withdraw the license for now** ...
I would also suggest **starting a thread on license-discuss** about the concepts that you would
like to employ, to get feedback on whether they would be acceptable for an approved license.
**If after discussion it appears that the OSI might approve a license of the type you propose**,
you can get assistance with conveying the concepts more clearly in a legal document and
**resubmitting the revised version**."*

**`REVIEWERS.md` の Status が述べる我々の計画（discuss → 指摘を取り込む → review へ）は、
委員長が別の提出者に示した経路と同じ形である。** **⚠ ただし向きが違う** ——
あちらは*提出したものを取り下げて* discuss へ行けという指示で、**我々は discuss から始めている。**

### そして、我々にとって最も不愉快な一文

Richard Fontana 氏 2019-05-27 —— *"My first thought was that this license was written in a
non-English language and **run through a machine translator without subsequent human review**."*

**ACD-1.0 の本文は AI が生成した英語である**（§E.1 で開示している）。
**もし英語が機械的に見えれば、これがその反応である。**
**開示していることは、そう読まれないことを意味しない。**

### 手続きの実測（3 例目）

*"Decision date: due no later than the first Board meeting after 21 May 2022"* に対し、
**理事会の議決は 2023-09-15**（**約 16 か月遅い**）。
Mulan の 207 日（§1.108）、NOSA 2.0 の 3 年半（§1.118）に続く 3 例目 ——
**公表された決定期限は上限として機能していない。**

## 1.121 「OSD 適合は十分条件ではない」の理由 —— 商標を一貫して行使する義務がある、と当時の会長が述べている（2026-09-27）

一次資料は `rounds/2008-12-license-review-tgppl-trademark-rule-observed-*.txt`（134 通・8 部）。
Transitive Grace Period Public Licence（2008-12 提出）は**承認されていない。**

### #248 の原理に、理由が付いた

Russ Nelson 氏（当時 OSI 会長）2009-02-17、提出者が「60 日のレビューで OSD 非適合という
指摘は誰からも出ていない」と述べたのに対し ——

> *"The license review process is **more what you'd call 'guidelines' than actual rules**.
> The review takes as long as it takes."*
>
> *"**There are reasons beyond OSD conformance why we might not want to approve the license.
> Why? Because we have a trademark to preserve.** If you can figure out some way to **comply with
> the OSD in a way that does not achieve the desired open source effect**, which endangers the
> meaning of OSI-Approved trademark, **then we MUST deny your license OSI approval (trademark law
> gives us no choice).**"*
>
> *"**Somebody has to decide what OSD conformance means. It's us.**"*
>
> *"we've given the plank to smart-asses before who thought that **strict OSD compliance (which
> technically doesn't even require that you SHIP SOURCE CODE) was sufficient**."*

**#248 は「OSD 適合は必要条件であって十分条件ではない」を 3 人の発言で記録した。
ここにはその理由が在る** ——**商標は一貫して行使しなければ保護を失うので、
「形式的には適合するが効果を達成しない」ライセンスを承認することは、
OSI にとって選択の余地のない拒否事由になる。**

**これは #248 の Villa 氏の *"political game"* という言い方より正確である** ——
**恣意ではなく、商標という法的資産の保全から来ている。**

### ACD-1.0 にとって何を意味するか

**我々の提出パケットは「逐条で OSD を満たす」を中心に据えている**
（`submission-osd.md` の 10 条逐条と、§3b の反対側）。
**この一文は、その中心が十分条件ではないことを、理由つきで述べている。**

**我々が答えられるのは「効果を達成するか」の側だけである** ——
**§10.1 は条件を 1 つも持たないので、「形式的には適合するが効果を達成しない」という
構造を取りようがない。** **抜け道は条件の中にしか作れず、条件が無いからである。**

**⚠ だが Nelson 氏が挙げた例は条件の抜け道ではない** ——
*"a license which permitted distribution of all the source code you didn't get"* は
**許諾の形をした空洞**で、**条件ゼロでも作りうる**。
**ACD-1.0 が空洞でないことは、§4.2 が改変と派生物を許し、§10.1 が条件を付けないことから
言えるが、それは我々の読みである。**

### そして、ここでも限定状態が語られている

Nelson 氏 —— *"**It's possible that years of experience with this license may be needed before it
can be approved.**"* **TGPPL は承認されていない**（提出から 17 年）。
**§1.118（NOSA 2.0 の 3 年半）、§1.120（YATeam の 16 か月遅れ）に続く 3 例目で、
こちらは「決まらないまま」である。**

### 併せて記録する —— 条件を緩める側の変更に承認は要らない

Lawrence Rosen 氏 2008-12-14 —— *"So long as the Licensor **waives a condition** of the OSL 3.0
license that otherwise burdens the licensee, **no formal OSI approval should be needed**. ...
**Note that you cannot use a waiver to *add a burden* on a licensee. That would require a new
license and OSI approval.**"*

**ACD-1.0 は条件を 1 つも持たないので、この非対称の「緩める側」の極にある。**
**⚠ ただし氏が述べているのは既存ライセンスへの waiver についてで、
新しい instrument が要らないという話ではない** ——**#84 と #253 の proliferation はそのまま残る。**

## 1.122 委員長は反対意見を繰り返し条文と OSD へ差し戻す —— #263 と対で読むべき、審査の実際の形（2026-09-27）

一次資料は `rounds/2019-04-license-review-cal-approval-observed-*.txt`（585 通・61 部）。
**アーカイブ中で最大の提出スレッド**で、**2020-02-14 の理事会で承認された**
（**賛成 8・反対 0・棄権 1・欠席 2**）。

### ドシエは本文を分析し、審査を読んでいなかった

`gap-measurements.md` は **CAL-1.0 の条文**を我々の gap 主張に当て、
*"CAL-1.0 §3.1(a) は非特許 IP 全般に及び database 権にも届く"* と結論している
（#150 が「最も近い承認済みライセンスを提出パケットが論じていない」と記録した当のもの）。
**しかしその審査 585 通は一度も開いていなかった。**
**「言及 ≠ 読了」** ——**census が名前で数えたとき「未言及」と出なかったので、
読んだつもりになっていた。**

### 委員長の扱い方

Pamela Chestek 氏は、反対意見に対して繰り返し同じ問いを返している（2020-02-12）——

> *"I'm still in the dark. **Can you explain what OSD is not met and where you find that in the
> license?** If it's a meta-OSD problem, like forced disclosure of data that is not yours to have,
> **can you explain it in layperson's terms?** If you believe that the license is not appropriate
> for certain types of uses or certain types of software architecture, **can you explain how that
> violates the OSD?**"*

Josh Berkus 氏も同じ線を引いている —— *"**The fact that a license is useless in certain contexts
does not make it an invalid license.** I challenge you to find any of our approved licenses that is
useful to everyone everywhere under every circumstance."* /
*"it sounds like **you don't have specific objections to the actual text of this license**, but do
have discussion you want to take to license-discuss."*

**#263（会長 Nelson 氏の「OSD 適合は十分条件ではない・商標のため MUST deny」）と、
この差し戻しは矛盾しない。2 つで審査の形になっている** ——
**通常の運用では、反対は条文と OSD に接続しなければ効かない。
接続できない反対を理由に拒否する権限は在るが、それは予備の力として語られている。**

**ACD-1.0 にとっての意味**: **我々の逐条作業（`submission-osd.md`）は、
委員長が反対者に求めているものと同じ土俵に在る。**
**⚠ ただし #263 の天井は消えない** ——**土俵に乗ることと勝つことは別である。**

### late objection は再開理由にならない

承認の告知 —— *"The Board discussed the additional emails sent **after the License Committee made
its recommendation** to the Board and **found that they did not raise issues not previously
considered**."*
**勧告後に届いた反対は、新しい論点でなければ再開を生まない。**
**§1.116（Open Logistics）で見た「改訂は取り下げと再提出として扱う」と合わせると、
時計の進め方が読める。**

### 弁護士 + 長期、の 3 例目

CAL は弁護士（Van Lindberg 氏）が起草し、**beta 1 から beta 4 まで 4 版・約 11 か月**を要した。
**§1.116（Open Logistics・法律事務所同伴・3 版・11 か月）、§1.110（IPA Font・弁護士・2 版）に続く。**
**法的レビューは審査を短くしない** ——**それは #255 で記録した通りで、ここが 3 例目である。**
