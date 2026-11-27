---
file: LICENSES/ACD-1.0.review-readings-5.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-11-15
reachable-via: ACD-1.0.review-readings.md
canonical-ref: LICENSES/ACD-1.0.review-readings.md / LICENSES/ACD-1.0.review-readings-2.md / LICENSES/READ-THREADS.txt / LICENSES/AS-OF.md
---

# 未読のスレッドを読んだ記録（節 1.400 から・2006〜2008 のスレッド）

2026-11-15、オーナーの依頼「未読の OSI スレッドを 5 人で無くして、反映して」で、census の未読 285 本を年の帯で 5 人に分けた（30 の割り振り・2f の書き場所の案）。この文書は 2006〜2008 に始まるスレッドの記録で、節番号は 1.400 から使う（帯を分けたので、番号は文書をまたいで重ならない・Check 500 が重複を止める）。書き方は `ACD-1.0.review-readings-2.md` と同じである: 原文を引き、発言者と日付を書き、ACD への当たり方と逆側を同じ表に置き、最後に「この節が establish しないこと」を書く。論点の無い会話は節を作らず、`record_read.py --log-only` で読了だけを記録する。

**2006〜2008 の 51 本の読み方（portfolio-1c）**: 決める側（`census_decision_statements.py` の DECIDERS）の通を全部取り出し、ACD の条に関わる語（特許・献呈・公有・人格権・表示・終了・保証・Steward・商標・データベース・放棄・約束・撤回・再許諾・識別子・版・承認・却下・重複・条件ほか）を含む文を拾い、語に掛からなかった会話は決める側の通を全文で読んだ。論点のあった会話は前後の通を原文で読み、引いた文が本人の文かを `rounds/` の原文で確かめた —— 1 件（2006-05 の「今または将来の請求項」の文）は McCoy Smith 氏の通に Outlook 形式（*"-----Original Message-----"* の下に `>` の無い本文）で引用された David A. Temeles 氏の文で、決める側の文ではなかったので外した。道具の `own_text` は `>` の行しか外さないので、この形の引用は本人の文に見える。

## 1.400 見知らぬ者どうしの間に約束は成り立つか、契約なしに保証を否認できるか —— Nelson 氏（2007〜2008）（2026-11-15）

"(OT) - NOT A Major Blow to Copyleft Theory"（`license-discuss` 2008-02・`rounds/2008-02-license-discuss-nelson-covenant-strangers-observed.txt`）と "EULA and Modifed BSD"（`license-discuss` 2007-12・`rounds/2007-12-license-discuss-nelson-warranty-contract-observed.txt`）。どちらも当時の OSI の License Committee の委員長だった Russ Nelson 氏の通。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"A covenant exists only within the context of a license.  And, a covenant is a solemn promise.  Does a judge seriously expect that a covenant, bound with seal and oath, exists between an open source licensor and licensee, who have never communicated with each other and when the latter is unknown to the former?"*（2008-02-08）| Nelson 氏 | 文脈は Jacobsen v. Katzer の地裁判決で、疑っているのは**受領者の約束**（配布の条件を約束と読む読み）である。ACD の §5・§8.6 は **Dedicator の約束**で向きが違う。ただし「会ったことのない者の間に約束が成り立つか」という疑いの型は、§5.3 の受益者の構成にそのまま当たる。**有利な面**: ACD は約束だけに頼らない。§3（放棄）と §4（許諾）は約束と独立に働き（§2.4、§5.3 末文 *"Sections 3 and 4 operate in their favour independently of this Section"*）、§5.3 は依拠を *"to the extent a jurisdiction gives effect to such reliance"* に限る。Nelson 氏の疑いは、約束を唯一の足場にしない理由として読める |
| *"You \*do\* need to make sure that a contract is formed in order to disclaim warranty.  (As an aside, the GPL isn't a contract, so how can it effectively disclaim warranty?)"*（2007-12-10）| Nelson 氏 | §13（保証の否認）と §14（責任の制限）は、受諾を要しない（§2.3）献呈の中にある。契約が成り立たない法域では、否認が効くかが問われうる。GPL と同じ問いで、ACD に固有ではない |

**逆側**: (1) Nelson 氏は *"IANAL; take the following with a grain of salt."* と断っている（2007-12-10）。2008-02 の通も法律家の意見ではない。(2) 保証の否認の効き方は法律家への問いの範囲で、ACD の本文では閉じられない（§13 は無償の献呈で、売買の黙示の保証が生じる場面かどうかが先に問われる）。portfolio-30 に、法律家への問いに足すかを渡した。

**この節が establish しないこと**: 2007〜2008 年の個人の見解で、委員会や理事会の判断ではない。約束が見知らぬ者の間に成り立つかは法域で違い、Nelson 氏の疑いが今の審査者に共有されているかは確かめていない。

**反映**: 1c（逐条リファレンスの §5.3 と §13.1 の行に不利な材料として・本文は変えない —— ACD は約束だけに頼らず §3・§4 を独立に立てる）。B4・B5 と法律家への問い 1 (f)（30）。保証の否認は法律家への問い 1 (f) の裏づけとして portfolio-30 が足す。register の B4・B5（約束と放棄の構成）へ（30）。

## 1.401 表示は保存より偽らないことが芯、ライセンスに商標の許諾を入れない —— Tiemann 氏と Rosen 氏（2006〜2008）（2026-11-15）

"For Approval: Generic Attribution Provision"（`license-discuss` 2006-11・`rounds/2006-11-license-discuss-tiemann-attribution-misrepresented-observed.txt`）、"Followup on Exhibit B licences"（`license-discuss` 2007-03・`rounds/2007-03-license-discuss-rosen-no-trademark-licence-observed.txt`）。同じ時期の "Policy for attribution"（2006-07）と "The Rails Wheels licencing system and Open Source"（2008-09）も同じ論点で、引用は前の 2 通にとどめた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"In Red Hat's case, the operative aspect of attribution is not that it be preserved, but that it not be misrepresented, which OSD #4 covers."*、*"I think it is very interesting to consider whether and how attribution should be preserved, but as a means to protect the integrity of authorship, not as a mechanism to exert a proprietary control point that the open source model and philosophy forbids."*（2006-11-29）| Tiemann 氏（当時の OSI の会長）| **有利**。ACD は表示を求めず（§10.2・§10.3）、偽らないことだけを献呈の外に置く（§11.3）。Tiemann 氏が「芯」とした形と同じである |
| *"An open source license cannot (should not!) contain a trademark license."*（2007-03-06）| Rosen 氏 | **有利**。§11.1 は *"This Dedication grants no right in any trademark, service mark, trade name, logo, or personal name of the Dedicator or of any other person."* と商標の許諾を持たない |

**逆側**: 2006〜2007 年の議論は、表示を UI に求めるライセンス（badgeware）が承認できるかの論争で、表示を求めないライセンスを論じたものではない。§16.4 は名前の下での改変した本文の頒布を制限するが、これは文書の名についての規律（§16.6）で、Rosen 氏の言う商標の許諾ではない —— ただし審査者が §16.4 を商標の代わりと読む余地は残る（`review-readings-2.md` §1.226 の Rosen 氏 2002 と同じ点）。

**この節が establish しないこと**: Tiemann 氏の文は Red Hat の立場として書かれている。OSD 4 の読みとして委員会が確認したものではない。

**反映**: 1c（逐条リファレンスの §11.1・§11.3 の行に有利な材料として・本文は変えない）。入口（REVIEWERS）で §11 を説明するときの材料。

## 1.402 承認はどれも費用を課す、承認の指針は独自性の証明、or later は範囲外 —— Nelson 氏・Rosen 氏・Tiemann 氏（2007）（2026-11-15）

"Communication skills"（`license-discuss` 2007-11・`rounds/2007-11-license-discuss-nelson-every-licence-a-cost-observed.txt`）、"AFL 3.0"（`license-discuss` 2007-04・`rounds/2007-04-license-discuss-rosen-uniqueness-observed.txt`）、"When to evaluate dual licenses"（`license-discuss` 2007-12・`rounds/2007-12-license-discuss-tiemann-or-later-scope-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Every license we approve imposes a cost on all software distributors,"*（2007-11-15・同じ通は Simplified BSD と FreeBSD の両方を承認する意味は無いと続ける）| Nelson 氏（当時の License Committee の委員長）| **不利（B2・B10）**。新しいライセンスはそれだけで費用であり、既存と同じ効果なら承認の理由が無い。ACD は既存に無い効果（B10 の G1）を示す必要がある |
| *"One of the guiding principles in recent years for OSI's approval of open source licenses has been the demonstration of uniqueness."*（2007-04-04）| Rosen 氏 | 同じ向きの基準で、**ACD が答えるべき問い**。答えは B10（既存の承認済み 141 本に無い効果）にある |
| *"I would agree that "GPLv2 or later" is outside our scope, because we cannot predict whether future versions of the GPL will be OSD-compliant or not."*（2007-12-15）| Tiemann 氏 | **有利**。ACD は「or later」の条を持たない（新しい版は §16.4・§16.5 の Steward が新しい名と識別子で出し、前の版の適用は §2.2 で変わらない）。審査は提出された 1 つの本文に対して閉じる |

**逆側**: (1) 2007 年の基準は、その後の委員会の理由書（`board-decisions.md`）で言い換えられている。「独自性」は Rosen 氏の観察で、規則として書かれたものではない。(2) Nelson 氏の「費用」の文は、Simplified BSD と FreeBSD の重複についての文で、新しい効果を持つライセンスに同じ重さで当たるとは限らない。

**この節が establish しないこと**: 3 つとも 2007 年の個人の発言で、今の委員会の基準ではない。

**反映**: B10・B2（承認の費用と独自性）・B12（or later の不在）（portfolio-30 が受ける）。逐条リファレンスの §16.5 の行に Tiemann 氏の or later の文を有利な材料として（本文は変えない）。

## 1.403 論点の無かった会話（2006〜2008・48 本）（2026-11-15）

残りの会話は、ACD の条や register に当たる論点を持たなかった。主な型は次のとおりで、件名は `READ-THREADS-LOG.md` に記録した: GPL の使い方の質問（"Question Regarding GPL"・"GPL issue at my work place"・"distributing GPL libreries"・"Question about the GPL v3"・"LGPL 2.1 + GPL 3 = problems?"）、表示を UI に求めるライセンスの論争（"APL license - What about the enforced logos?"・"InfoWorld: Pentaho opens up further"・"SocialText license discussion"・"Followup on Exhibit B licences" の他の通・"For Approval: Common Public Attribution License (CPAL)"）、OSI の運営（"Call for Votes: New OSI-Editors List"・"Noise filter"・"a plea"・"license categories"・"Censure / Removal Re: Affero Licence/AGPL"・"OSI Logo - Terms of Use"）、Jacobsen v. Katzer の論評（"Major Blow to Copyleft Theory"・"encforceability of Open Source Licences"・"SFLC will love the 7th Circuit"）、ほかの個別の質問。**2 点だけ記録する**: (1) IETF の寄与の方針について Rosen 氏は *"Of course a contributor can't give patent rights it doesn't own. BUT IT CAN GIVE IETF PATENT RIGHTS IT DOES OWN!"* と書いた（2007-01-19・"IETF IP Contribution Policy"）—— §2.7・§8.5（持つ・支配する請求項だけに及ぶ）と同じ線で、寄与者が特許を許諾する §2.6 の形（寄与者も Dedicator になる）を支える。(2) BIPL の審査で McCoy Smith 氏は、最初の開発者が特許を許諾せず後の寄与者だけが許諾する非対称を問題にした（2006-05-11・"License Discussion for the Broad Institute Public License (BIPL)"）—— ACD は寄与者を Dedicator にし（§2.6）、同じ §8 の許諾を負わせるので、非対称は無い。どちらも短い文なので `rounds/` には置かず、アーカイブの月を引く。

**反映**: 1c（論点の 2 点は逐条リファレンスの §2.6・§8.5 の行へ・本文は変えない。残りの会話は論点が無い）。

## 1.404 本気のライセンスなら法律家の審査を経る、起草の質と OSD への適合は別に問う —— Perens 氏・Piana 氏（2009）（2026-11-15）

2009〜2010 の 15 本は portfolio-9b の帯で、portfolio-1c が引き受けた（9b は 2002〜2003 を読む）。"Serious Open Source (SOS) License -- Injunctive Relief clause"（`license-review` 2009-03・`rounds/2009-03-license-review-perens-serious-licence-legal-review-observed.txt`）と "Legacy Approval - BlackBox Component Builder Open Source License"（`license-review` 2009-11・`rounds/2009-11-license-review-piana-blackbox-drafting-vs-osd-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"A really Serious License would have proper legal review by at least one qualified attorney. Can you get that? I'd like to hear from your attorney a credible explanation regarding the effectiveness of this language."*（2009-03-14・同じ人の次の通は *"What I asked you for was to have YOUR license reviewed by a lawyer."* と続け、*"I don't believe it is supportive of Open Source developers for anyone to submit a license that has not had legal review, because those developers may be hurt when the license fails to work as expected in court."* と書いた・2009-03-15）| Perens 氏 | **不利（B1）**。ACD は法律家の審査を経ていない。2007 年 12 月に提出の要件から法律家の分析が外れた後（`review-rules.md` §1.141）も、審査者の側には「本気なら法律家」の期待が残っていたことを示す |
| *"Clearly those who have written it have a slack understanding of copyright and the concept of derivatives. I agree: stay away from this license because of the lack of predictability of the outcome of applying it to your software. Having said that, I don't see overly evident reasons why this should not qualify according to the OSD."*（2009-11-03）| Piana 氏 | 2009 年の Piana 氏は、起草の質への評価（使うな）と OSD への適合（不適合の明らかな理由は無い）を分けた。2026 年の委員会は *"Poor drafting"* を第 1 の理由として却下している（`board-decisions.md` §4a）—— **起草の質が適合の外の助言から却下の理由へ移った**ことの、時代の差の記録になる。ACD にとっては、OSD に合うだけでは足りず、起草の質（B1・B13）が却下に直結しうる |

**逆側**: Perens 氏の通は、wtfpl.user と名乗る提出者の、差止めの同意を事前に受領者に求める条についてで、ACD のような条件の無いライセンスについてではない。Piana 氏は 2009 年には委員会の側ではなかった（記録上は `[OSI]` の付いた差出人）。

**この節が establish しないこと**: 2009 年の個人の発言で、今の委員会の基準ではない。

**反映**: B1（法律家の審査が無い）と B13（理解の費用）へ（portfolio-30 が受ける）。1c（本文は変えない —— 法律家の審査は本文の語では作れない）。

## 1.405 オープンデータの定義を OSI が作ろうとした、ライセンスは一方的な付与 —— Nelson 氏・Mathur 氏（2010）（2026-11-15）

"Open Data Definition at OSCON"（`license-discuss` 2010-06・`rounds/2010-06-license-discuss-nelson-open-data-definition-observed.txt`）と "GPL Issue"（`license-discuss` 2010-09）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I'm running a BOF at OSCON on Wednesday night at 7PM, with the declared purpose of writing an Open Source Definition for Open Data. Safe enough to say that the OSD has been quite successful in laying out a set of criteria for what is, and what is not, Open Source. I think we can and should do the same thing for Open Data."*（2010-06-29・同じ日に *"the point of this exercise is not to create something from scratch, but instead for OSI to take a position on open data backed up by community input"*）| Nelson 氏（当時の理事） | **B15 に有利な材料**。2010 年の OSI の側に、データについて OSI が立場を取るべきだという考えがあった。Villa 氏は同じ日に opendefinition.org を挙げ、焦点は開かれたサービスだと返した |
| *"Regardless of legal precedence or lack thereof, a software licence is not a bilateral or multilateral agreement -- it is a unilateral grant of privileges from the licensor to the licensee. There cannot be a contract between two parties, at least one of whom is unaware of the other's existence"*（2010-09-22）| Raj Mathur 氏 | §2.3（受諾を要しない）と同じ線。§1.400 の Nelson 氏 2008（見知らぬ者の間に約束は成り立つか）と組で読む —— ACD は許諾と放棄を一方的に与え、約束はその上に重ねる形で、どちらの読みにも足場を残す |

**逆側**: Nelson 氏の BOF の後に OSI がオープンデータの定義を採った記録は、このスレッドには無い。データを OSI の範囲に入れることは、2023 年の Mulan の不承認の理由と向きが逆である（B15）。Mathur 氏の文は法律家の意見ではない。同じスレッドで Smith 氏は Jacobsen v. Katzer の控訴審の判決を *"Pretty leading case"* と挙げている。

**この節が establish しないこと**: 2010 年の個人の発言で、OSI の方針ではない。

**反映**: B15（データとソフトウェアの外の素材）へ（portfolio-30 が受ける）。1c（逐条の §2.3 の行に Mathur 氏の文を、本文は変えない）。

## 1.406 2009〜2010 の残りの会話（11 本）（2026-11-15）

WTFPL の承認の請求（"WTFPL approval, please?"・2009-02）は、Nelson 氏が承認しない理由（名前を変えないと改変できない）を述べた後、Michlmayr 氏に指摘されて *"Duh. Yes. Indeed."* と認めており、OSD 上の理由は残っていない。Nelson 氏は同じ通で、このライセンスを使うことを勧めないとも書いた（語の品位について）。同じ提出者の SOS の通で Perens 氏は *"Nothing associated with "wtf" is likely to be consdiered serious."* と書いた（2009-03-14）—— **名前は審査者の受け取り方に効く**（B6 の材料。ACD の名前は真面目に読まれる形）。残りは使い方の質問（"How do I choose a licence"・"combining software under different licenses"・"GPL with the Classpath exception"・"GNU GPL vs. source code fees"・"Licensing question"・"ARToolKit"・"question about AGPLv3, OSLv3, the keyword 'communicate'"・"What does "new" mean in Section 1.9 (b) of the MPL v 1.1.?"）、告知（"DISA to open source administrative software"）、雇用主から権利の放棄の書面を取ること（"Freeing my code... need some guidance"・Tiemann 氏 2009-01-15 —— §1.4 の Dedicator が権利を持つことの実務で、`ADOPTING.md` の材料）で、ACD の条に当たる論点は無い。

**反映**: B6（名前の受け取り方）へ（portfolio-30）。入口（`ADOPTING.md` の雇用主の権利の確認・portfolio-50）。残りの会話は論点が無い。

## 1.407 準拠法は書くか何も書かないか、新しいライセンスは混乱を増やす —— Phipps 氏・Smith 氏・DiBona 氏（2007）、プラグインの例外（2022）（2026-11-15）

未読の最後の分。"Politics-Free Licence ;)"（`license-discuss` 2007-06・候補が 821 本から 824 本へ増えたときに入った 2006〜2008 の帯の 1 本）と "Question about AGPLv3 with a Plugin Exception"（`license-discuss` 2022-08・どの帯にも入っていなかった 1 本）。原文は `rounds/2007-06-license-discuss-phipps-choice-of-law-namespace-observed.txt`・`rounds/2007-06-license-discuss-phipps-fixed-law-or-none-observed.txt`・`rounds/2007-06-license-discuss-dibona-every-new-licence-confusion-observed.txt`。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"It seems to me that if you want maximum uptake on an open source license, you'd leave out jurisdiction and venue clauses."*（2007-06-28）| McCoy Smith 氏 | **有利**。§15.3（1.0 では §15.7）は *"This Dedication specifies no governing law and no forum."* と、どちらも置かない |
| 準拠法を *"a "namespace" declaration helping interpretation of the language of the license"* と見て入れる方に共感する（2007-06-28）。翌日 *"Thus, I assert that /either/ there should be a fixed statement of the system of law assumed by the license, or none at all. Encouraging the language of the license to be variably interpreted unsettles lots of people"*（2007-06-29・同じ通は、多くの法律家に磨かれていないライセンスほど想定した法体系を書くのが賢いとも書く）。前日の Chuck Swiger 氏への返事では *"If we don't know what system of law is assumed in the interpretation of the license, or if it varies from use to use, I believe the community uncertainty it produces is worse, not better."*（2007-06-28・`rounds/2007-06-license-discuss-phipps-law-varying-by-use-observed.txt`・portfolio-2f が挙げた）同じ 06-29 の通の末尾は *"I do feel that more people will be more happy with a license that makes no attempt to choose a venue."* | Simon Phipps 氏 | **両面**（裁判地を選ばないことは Phipps 氏も支える）。§15.3（1.0 では §15.7）第 1 文は Phipps 氏の二択の「何も書かない」側に合う。第 2 文 *"It is intended to operate under the law of each jurisdiction in which the Work is used, according to that law."* は、Phipps 氏が人を不安にするとした「法域ごとに違う読み」を自分から述べる文にも読める。ACD は法律家に磨かれていない（B1）ので、Phipps 氏の基準では「想定した法体系を書く」側が勧められる |
| *"Every new license osi approves as subscribing to the osd adds to the confusion and difficulty that new developers and companies face when using open source and worse yet means yet another largely incompatible potential pool of code."*（2007-06-28）| Chris DiBona 氏 | **不利（B10・B2）**。§1.402 の Nelson 氏 2007 と同じ向き。ACD は条件が無く、どのライセンスの下のコードとも組めるので「非互換の池」には当たりにくいが、新しいライセンスの費用そのものは残る |
| *"Licenses can, and should, clearly state when an API is meant to be a connector to another work which can be under a different license and is not to be considered derivative. … We don't want to win in court about this sort of thing. We want to never go to court."*（2022-08-16）| Bruce Perens 氏 | B13（明瞭さ）と同じ向きの一般の規範。ACD は条件を持たないので、派生物の境界を問う場面が無い |

**逆側**: Phipps 氏の二択は、準拠法を選ぶライセンスの起草者への助言で、選ばないことを述べ直す文が「違う読みを促す」かは、同氏が論じていない。第 2 文は法律家への問い 7（*"What follows from naming no governing law and no forum?"*）が、残すかどうかを既に訊いている。

**この節が establish しないこと**: 2007 年と 2022 年の個人の発言で、委員会の基準ではない。

**反映**: 1c（逐条の §15.3 の行に Smith 氏と Phipps 氏の両面を・本文は変えない —— 第 2 文を残すかは法律家への問い 7 の答えを待つ）。B10・B2（DiBona 氏・portfolio-30）。法律家への問い 7 に Phipps 氏の二択を材料として（portfolio-30）。

**読み直し（2026-11-16）**: portfolio-2f と portfolio-30 が、決める側の通を先頭の数百字で切って読んでいた穴を見つけた（`review-readings-3.md` §1.312）。portfolio-1c も同じ穴を持っていた —— 2009〜2010 の 15 本と §1.407 の 2 本は各通の先頭 850 字、2006〜2008 のうち語に掛からなかった 9 本は 700 字で切っていた（2006〜2008 の残りは全文から語で拾ったので切っていない）。切られた 20 通の後ろを全文で読み直し、2 文を足した: Perens 氏 2009-03-15 の法律家の審査の文（§1.404・B1 を強める）と、Phipps 氏 2007-06-29 の裁判地の文（§1.407・§15.3 第 1 文の支え）。ほかの 18 通の後ろは署名、引用された質問の本文、告知の続きで、論点を足さなかった。
