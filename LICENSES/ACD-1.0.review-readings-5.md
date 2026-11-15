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

"(OT) - NOT A Major Blow to Copyleft Theory"（`license-discuss` 2008-02・`rounds/2008-02-license-discuss-nelson-covenant-strangers-observed.txt`）と "EULA and Modifed BSD"（`license-discuss` 2007-12・`rounds/2007-12-license-discuss-nelson-warranty-contract-observed.txt`）。どちらも当時の OSI の会長だった Russ Nelson 氏の通。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"A covenant exists only within the context of a license.  And, a covenant is a solemn promise.  Does a judge seriously expect that a covenant, bound with seal and oath, exists between an open source licensor and licensee, who have never communicated with each other and when the latter is unknown to the former?"*（2008-02-08）| Nelson 氏 | 文脈は Jacobsen v. Katzer の地裁判決で、疑っているのは**受領者の約束**（配布の条件を約束と読む読み）である。ACD の §5・§8.6 は **Dedicator の約束**で向きが違う。ただし「会ったことのない者の間に約束が成り立つか」という疑いの型は、§5.3 の受益者の構成にそのまま当たる。**有利な面**: ACD は約束だけに頼らない。§3（放棄）と §4（許諾）は約束と独立に働き（§2.4、§5.3 末文 *"Sections 3 and 4 operate in their favour independently of this Section"*）、§5.3 は依拠を *"to the extent a jurisdiction gives effect to such reliance"* に限る。Nelson 氏の疑いは、約束を唯一の足場にしない理由として読める |
| *"You \*do\* need to make sure that a contract is formed in order to disclaim warranty.  (As an aside, the GPL isn't a contract, so how can it effectively disclaim warranty?)"*（2007-12-10）| Nelson 氏 | §13（保証の否認）と §14（責任の制限）は、受諾を要しない（§2.3）献呈の中にある。契約が成り立たない法域では、否認が効くかが問われうる。GPL と同じ問いで、ACD に固有ではない |

**逆側**: (1) Nelson 氏は *"IANAL; take the following with a grain of salt."* と断っている（2007-12-10）。2008-02 の通も法律家の意見ではない。(2) 保証の否認の効き方は法律家への問いの範囲で、ACD の本文では閉じられない（§13 は無償の献呈で、売買の黙示の保証が生じる場面かどうかが先に問われる）。portfolio-30 に、法律家への問いに足すかを渡した。

**この節が establish しないこと**: 2007〜2008 年の個人の見解で、委員会や理事会の判断ではない。約束が見知らぬ者の間に成り立つかは法域で違い、Nelson 氏の疑いが今の審査者に共有されているかは確かめていない。

**反映**: 逐条リファレンスの §5.3 と §13.1 の行に不利な材料として（本文は変えない —— ACD は約束だけに頼らず §3・§4 を独立に立てる）。保証の否認は法律家への問い 1 (f) の裏づけとして portfolio-30 が足す。register の B4・B5（約束と放棄の構成）へ（30）。

## 1.401 表示は保存より偽らないことが芯、ライセンスに商標の許諾を入れない —— Tiemann 氏と Rosen 氏（2006〜2008）（2026-11-15）

"For Approval: Generic Attribution Provision"（`license-discuss` 2006-11・`rounds/2006-11-license-discuss-tiemann-attribution-misrepresented-observed.txt`）、"Followup on Exhibit B licences"（`license-discuss` 2007-03・`rounds/2007-03-license-discuss-rosen-no-trademark-licence-observed.txt`）。同じ時期の "Policy for attribution"（2006-07）と "The Rails Wheels licencing system and Open Source"（2008-09）も同じ論点で、引用は前の 2 通にとどめた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"In Red Hat's case, the operative aspect of attribution is not that it be preserved, but that it not be misrepresented, which OSD #4 covers."*、*"I think it is very interesting to consider whether and how attribution should be preserved, but as a means to protect the integrity of authorship, not as a mechanism to exert a proprietary control point that the open source model and philosophy forbids."*（2006-11-29）| Tiemann 氏（当時の OSI の会長）| **有利**。ACD は表示を求めず（§10.2・§10.3）、偽らないことだけを献呈の外に置く（§11.3）。Tiemann 氏が「芯」とした形と同じである |
| *"An open source license cannot (should not!) contain a trademark license."*（2007-03-06）| Rosen 氏 | **有利**。§11.1 は *"This Dedication grants no right in any trademark, service mark, trade name, logo, or personal name of the Dedicator or of any other person."* と商標の許諾を持たない |

**逆側**: 2006〜2007 年の議論は、表示を UI に求めるライセンス（badgeware）が承認できるかの論争で、表示を求めないライセンスを論じたものではない。§16.4 は名前の下での改変した本文の頒布を制限するが、これは文書の名についての規律（§16.6）で、Rosen 氏の言う商標の許諾ではない —— ただし審査者が §16.4 を商標の代わりと読む余地は残る（`review-readings-2.md` §1.226 の Rosen 氏 2002 と同じ点）。

**この節が establish しないこと**: Tiemann 氏の文は Red Hat の立場として書かれている。OSD 4 の読みとして委員会が確認したものではない。

**反映**: 逐条リファレンスの §11.1・§11.3 の行に有利な材料として（本文は変えない）。入口（REVIEWERS）で §11 を説明するときの材料。

## 1.402 承認はどれも費用を課す、承認の指針は独自性の証明、or later は範囲外 —— Nelson 氏・Rosen 氏・Tiemann 氏（2007）（2026-11-15）

"Communication skills"（`license-discuss` 2007-11・`rounds/2007-11-license-discuss-nelson-every-licence-a-cost-observed.txt`）、"AFL 3.0"（`license-discuss` 2007-04・`rounds/2007-04-license-discuss-rosen-uniqueness-observed.txt`）、"When to evaluate dual licenses"（`license-discuss` 2007-12・`rounds/2007-12-license-discuss-tiemann-or-later-scope-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Every license we approve imposes a cost on all software distributors,"*（2007-11-15・同じ通は Simplified BSD と FreeBSD の両方を承認する意味は無いと続ける）| Nelson 氏（当時の会長）| **不利（B2・B10）**。新しいライセンスはそれだけで費用であり、既存と同じ効果なら承認の理由が無い。ACD は既存に無い効果（B10 の G1）を示す必要がある |
| *"One of the guiding principles in recent years for OSI's approval of open source licenses has been the demonstration of uniqueness."*（2007-04-04）| Rosen 氏 | 同じ向きの基準で、**ACD が答えるべき問い**。答えは B10（既存の承認済み 141 本に無い効果）にある |
| *"I would agree that "GPLv2 or later" is outside our scope, because we cannot predict whether future versions of the GPL will be OSD-compliant or not."*（2007-12-15）| Tiemann 氏 | **有利**。ACD は「or later」の条を持たない（新しい版は §16.4・§16.5 の Steward が新しい名と識別子で出し、前の版の適用は §2.2 で変わらない）。審査は提出された 1 つの本文に対して閉じる |

**逆側**: (1) 2007 年の基準は、その後の委員会の理由書（`board-decisions.md`）で言い換えられている。「独自性」は Rosen 氏の観察で、規則として書かれたものではない。(2) Nelson 氏の「費用」の文は、Simplified BSD と FreeBSD の重複についての文で、新しい効果を持つライセンスに同じ重さで当たるとは限らない。

**この節が establish しないこと**: 3 つとも 2007 年の個人の発言で、今の委員会の基準ではない。

**反映**: register の B10・B2（承認の費用と独自性）と B12（or later の不在）へ（portfolio-30 が受ける）。逐条リファレンスの §16.5 の行に Tiemann 氏の or later の文を有利な材料として（本文は変えない）。

## 1.403 論点の無かった会話（2006〜2008・48 本）（2026-11-15）

残りの会話は、ACD の条や register に当たる論点を持たなかった。主な型は次のとおりで、件名は `READ-THREADS-LOG.md` に記録した: GPL の使い方の質問（"Question Regarding GPL"・"GPL issue at my work place"・"distributing GPL libreries"・"Question about the GPL v3"・"LGPL 2.1 + GPL 3 = problems?"）、表示を UI に求めるライセンスの論争（"APL license - What about the enforced logos?"・"InfoWorld: Pentaho opens up further"・"SocialText license discussion"・"Followup on Exhibit B licences" の他の通・"For Approval: Common Public Attribution License (CPAL)"）、OSI の運営（"Call for Votes: New OSI-Editors List"・"Noise filter"・"a plea"・"license categories"・"Censure / Removal Re: Affero Licence/AGPL"・"OSI Logo - Terms of Use"）、Jacobsen v. Katzer の論評（"Major Blow to Copyleft Theory"・"encforceability of Open Source Licences"・"SFLC will love the 7th Circuit"）、ほかの個別の質問。**2 点だけ記録する**: (1) IETF の寄与の方針について Rosen 氏は *"Of course a contributor can't give patent rights it doesn't own. BUT IT CAN GIVE IETF PATENT RIGHTS IT DOES OWN!"* と書いた（2007-01-19・"IETF IP Contribution Policy"）—— §2.7・§8.5（持つ・支配する請求項だけに及ぶ）と同じ線で、寄与者が特許を許諾する §2.6 の形（寄与者も Dedicator になる）を支える。(2) BIPL の審査で McCoy Smith 氏は、最初の開発者が特許を許諾せず後の寄与者だけが許諾する非対称を問題にした（2006-05-11・"License Discussion for the Broad Institute Public License (BIPL)"）—— ACD は寄与者を Dedicator にし（§2.6）、同じ §8 の許諾を負わせるので、非対称は無い。どちらも短い文なので `rounds/` には置かず、アーカイブの月を引く。

**反映**: 論点の 2 点は逐条リファレンスの §2.6・§8.5 の行へ（本文は変えない）。残りは無し（論点が無い）。
