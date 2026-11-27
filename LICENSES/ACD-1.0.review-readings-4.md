---
file: LICENSES/ACD-1.0.review-readings-4.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-11-15
reachable-via: ACD-1.0.review-readings.md
canonical-ref: LICENSES/ACD-1.0.review-readings.md / LICENSES/ACD-1.0.review-readings-2.md / LICENSES/READ-THREADS.txt / LICENSES/AS-OF.md
---

# 未読のスレッドを読んだ記録（節 1.350 から・2004〜2005 のスレッド）

2026-11-15、オーナーの依頼「未読の OSI スレッドを 5 人で無くして、反映して」で、census の未読 285 本を年の帯で 5 人に分けた（30 の割り振り・2f の書き場所の案）。この文書は 2004〜2005 に始まるスレッドの記録で、節番号は 1.350 から使う（帯を分けたので、番号は文書をまたいで重ならない・Check 500 が重複を止める）。書き方は `ACD-1.0.review-readings-2.md` と同じである: 原文を引き、発言者と日付を書き、ACD への当たり方と逆側を同じ表に置き、最後に「この節が establish しないこと」を書く。論点の無い会話は節を作らず、`record_read.py --log-only` で読了だけを記録する。

## 1.350 承認されなかった OVPL —— 最初の開発者だけが受け取る還元は OSD 5 の差別とされ、特別な権利そのものは差別とされなかった（2005）（2026-11-15）

"OVPL summary"（2005-09・53 通）、"OVPL vote results"（2005-11）、"OVPL and the OSI Board on Thursday"（2005-08）、"Two new licenses - OVPL & OVLPL"（2005-04）。OVPL は CDDL を下敷きに、寄与者が最初の開発者に寄与を再許諾する義務（grant-back）を足した提出で、理事会は 2005-11-11 に承認しないと決めた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The grant-back creates a situation that discriminates against parties who wish to make their own distribution of OVPL-licensed code."*、*"This, we adjudge, violates the "No Discrimination against persons or groups of persons" term of the Open Source Definition."* | Russell Nelson 氏 2005-11-11（理事会の決定の告知） | **§16.4 の Steward 例外への最も近い先例（区別できる）。** 否決の理由は、最初の開発者だけが**寄与されたコード**を受け取る還元の義務である。ACD の例外は、Steward だけが名前の下で新しい版を出せるという**本文の名前**についての区別で、Work の頒布にも寄与にも何も課さない（§16.6 *"no one in respect of the Work"*）。理事会の線は「自分の頒布をしたい人を差別する」ことに引かれており、ACD はその人に何も求めない |
| *"I agree that such differences in rights is not discrimination under the OSD. Many of the existing licenses are not perfectly recipricol."* | Mark Radcliffe 氏 2005-09-14（後の OSI の法律顧問） | **有利な面。** 最初の開発者と他の受け手の権利の差そのものは差別ではない、という読み |
| *"under today's OSD, I've told others privately, the OVPL should be approved."*、*"I've also told people privately that I don't like such special privileges in open source licenses. I prefer equal reciprocity."* | Lawrence Rosen 氏 2005-09-14 | 両面。OSD の文言では特別な権利は通るとし、同時に好まないと述べる。理事会は結局否決した —— 委員の私見と決定は別である |
| *"An additional rights grant is not discriminatory under OSD #5 if the parties to whom the rights are NOT granted are still getting sufficient rights for it to otherwise be considered an Open Source license."* | Bruce Perens 氏 2005-04-11 | **有利な面（OSD 5 の試験の形）。** §16.4 の例外を受けない者（Steward 以外）も、Work について全部の許諾を持つ（§4・§10.1）。名前の下で新しい版を出す権利が無いだけである |
| *"What if we made a mistake *then*?  Should we be required to make the same mistake forever on?  As a guiding principle I must reject this."* | Nelson 氏 2005-11-12（QPL の前例を挙げた提出者への返信） | 前例は理事会を縛らない —— Piana 氏 2024 の *"but license x does the same"* と同じ線が 2005 年に既に在った（`REVIEWERS.md` の有利な記録の表の前置き） |
| *"It's approvable as far as I can see.  However we also have license proliferation issues to worry about."*、*"If we continue to increase the number of approved licenses, they WILL do this."* | Nelson 氏 2005-08-19 | **不利な面（B10・B2）。** 承認できる提出でも、増殖を理由に審査を保留した実例。大企業が「この一覧から選べ」と言い出すという見立て |

**読み。** 2005 年の理事会は、最初の開発者が他より多くを持つこと自体ではなく、**他の受け手が自分の頒布をする自由に負担をかける**ことで線を引いた。§16.4 の例外は本文の名前の扱いで、Work についての誰の自由にも負担をかけないので、この線の手前にある。

**逆側。** 審査者は「1 人だけが持つ権利」という形の類似で OVPL を思い出しうる。区別は §16.6 を読めば立つが、読まれる前に「これは OVPL の還元とは違う」と言う場所が要る（`submission-osd.md` §3b-i の OSD 5 の段）。また Rosen 氏の「好まない」は、委員の私見として今も現れうる。

**この節が establish しないこと。** 理事会の議事録は読んでいない（告知の通だけ）。§16.4 の例外が OSD 5 に適うことを、この記録は保証しない。

**反映**: `ACD-1.0.submission-osd.md` §3b-i（OSD 5 の段）に OVPL の否決との区別を 1 段（50）。Nelson 氏 2005-08 の増殖による保留は register の B10（30 へ渡した）。

## 1.351 「死んだ」ライセンスの整理と、再利用できるライセンスという分類（2004-12）（2026-11-15）

"pruning "dead" licenses"（`license-discuss` 2004-12・33 通）。当時の license approval committee の委員長（2005-02 に第三者から OSI の新しい会長と呼ばれた）Nelson 氏が、使われなくなったライセンスの認証を外すことを提案した。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"A "dead" license is one which is no longer used for any projects."* | Nelson 氏 2004-12-13 | **不利な面（B2）。** 使用が無いことを、承認を外す理由として論じた記録 |
| *"What purpose does a license serve if nobody uses it?"* | Nelson 氏 2004-12-14 | **不利な面（B2）。** 採用者が 1 件の ACD に、審査者が同じ問いを向けうる |
| *"There's a whole bunch of requirements to gain certification which are outside the OSD."* | Nelson 氏 2004-12-14 | 不利な面。承認の要件は OSD の外にもあるという、license approval committee の委員長の発言（`submission-osd.md` 冒頭の Nelson 氏 2009 と同じ線） |
| *"From this perspective, I would vote for categorizing licenses into "Active" vs "Legacy". I would also support an additional annotation of "Reusable" to indicate licenses which people should consider for (b)."* | Ernest Prabhakar 氏 2004-12-14 | **有利な面。** 「自分のコードを出す人が選ぶ」再利用できるライセンスという分類。ACD は誰でも本文を変えずに適用できるように書いてある（§16.3）ので、この分類に入る |

**読み。** 2004 年の整理の議論は、使用を承認の維持の条件として論じたが、決定には至らなかった。後の 2005 年の増殖委員会につながる。

**逆側。** 使用の問いは 2020 年の理由書で「基準ではない」とされた（`review-readings.md` §1.201）が、2004 年の理事長の問いの形（何のためにあるのか）は、今も審査者の最初の問いとして来る（§1.222）。

**この節が establish しないこと。** どのライセンスが実際に外されたかは扱わない。

**反映**: register の B2 に Nelson 氏 2004-12 の 2 文（30 へ渡した）。入口と材料は §1.222 の行（使うと表明するプロジェクト・何を達成したいか）で既に答えているので、足すものは無い。

## 1.352 本文の書き方 —— 目的に足るだけの長さ、注釈は論評にしない、1 語でも変えれば別のライセンス、書いた語がそれ自体で立つ（2004〜2005）（2026-11-15）

いくつかの会話から、本文の書き方について決める側が述べたことを集めた。

| 発言 | 誰が・どこで | ACD への当たり方 |
| :-- | :-- | :-- |
| *"A license should be long enough to accomplish your goals, but no longer."* | Prabhakar 氏 2004-03-03（"Help with license decision for "cluster" of similar projects"） | **B3。** ACD は長い（`ACD-OSI-BOTTLENECKS.md` B3）。1.4 で理由の文を外したのはこの向き |
| *"Some of them seem more like commentary than clarification"*、*"I think it would be worthwhile for you to find a friendly English collaborator to work on the wording"* | Prabhakar 氏 2004-03-16（LAB Public License の提出） | **B13・B1。** 本文の中の論評を嫌い、母語話者の協力を勧めた。1.4 は理由の文を外した（T54 ほか）。英語の母語話者が読んでいないことは ACD にも当たる（§1.211 の Berkus 氏 2025 と同じ線） |
| *"My initial read of this license is that yes, it does satisfy the letter of the OSD, so that's a Good Thing.  But the larger question that I must always ask is: if/when it becomes used by multiple third parties, what problems can it solve that other OSI-approved licenses don't solve."* | Michael Tiemann 氏 2004-04-15（Adaptive Public License） | **B10。** OSD の文言を満たしても、既存のライセンスで解けない何を解くかを問う。ACD の答えは `REVIEWERS.md` の "The new language" の表 |
| *"I suspect the problem is that the optional modules make life easier for the *licensor*, but painfully confusing for the *licensee*."* | Prabhakar 氏 2004-04-16（同） | **有利な面。** ACD には選択の項目が無い（採用者は本文を編集しない） |
| *"You cannot change a single word of a license without losing approval."* | Nelson 氏 2005-11-01（Educational Community License） | **有利な面（§16.4）。** 本文の 1 語が承認の単位であるという理事の言葉。§16.4 が名前の下で改変した本文を配ることを止めるのは、この同一性を守るため |
| *"Please note that most Open Source licenses are themselves not subject to modification without the consent of the author of the licenses."* | Brian Behlendorf 氏 2004-11-07（"Definition of open source"） | **有利な面（§16.4）。** ライセンスの本文そのものを改変不可にすることは、承認済みの多くが既にしている |
| *"I'm not the sole interpreter of the meaning even of my own words. No attorney is."*、*"The specific words we wrote in our licenses will stand on their own."* | Rosen 氏 2005-04（"A prototype License Wizard up and running"） | **有利な面。** ドシエや想定問答は本文の意味を決めない（各文書が「非規範」と書く）、前文は作用しない（前文の末尾）、という ACD の作りと同じ考え |
| *"If the rules are simple and the licenses few in number, I believe, we're much more likely to grow a large commons of free and open source software."* | Rosen 氏 2005-02（"Best base license to pick?"） | **不利な面（B10）。** 新しいライセンスを足すこと自体の費用 |
| *"What specific business needs were you pursuing that could not be addressed by existing licenses?"*、*"Please, do *not* call your license MPL.  That name's already taken."* | Prabhakar 氏 2005-10-06（MindTree Public License の提出） | B10 と B6。名前の重複を問うた例。ACD の名前と識別子は既存と重ならない（`ACD-OSI-BOTTLENECKS.md` B6） |
| *"If all you've ever done is talk about your license on license-discuss, it will never be approved."* | Nelson 氏 2004-11-03（"certification mark for "mirbsdksh"?"） | **段 6b を支える。** `license-discuss` での議論は提出ではない。計画は discuss に 30 日置いたあと `license-review` へ出す（`OSI-APPROVAL-PLAN.md` §4） |

**読み。** 2004〜2005 年の決める側は、本文を短く、論評を入れず、1 語の同一性を承認の単位とし、本文の外の説明は本文を縛らないと考えた。ACD の 1.4 の方向（理由の文を外す・本文を変えずに使う・§16.4）はこれと同じ向きにある。

**逆側。** 同じ人たちは、新しいライセンスを足すこと自体を費用とみなした（Rosen 氏・Tiemann 氏）。ACD が「同じ向き」であることは、それが新しく足される理由にはならない。

**この節が establish しないこと。** どの提出が承認されたかは扱わない（APL は後に承認、LAB と MindTree の帰結はここでは見ていない）。

**反映**: `OSI-APPROVAL-PLAN.md` 段 6b の根拠に Nelson 氏 2004-11 の文（50）。§16.4 の 2 つの有利な文（Nelson 氏 2005-11・Behlendorf 氏 2004-11）は `submission-osd.md` §3b-i の同じ段へ（50）。B3・B13 は 1.4 の向き（理由の文を外した）で既に答えており、本文への種は無い。

## 1.353 寄与の既定、同意、法令の注記、通知を読む人 —— §2.3・§2.6・§10.2 に当たる 2004〜2005 年の発言（2026-11-15）

| 発言 | 誰が・どこで | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Unless You explicitly state otherwise, any Contribution intentionally submitted for inclusion in the Work by You to the Licensor shall be under the terms and conditions of this License, without any additional terms or conditions."*（Apache-2.0 §5 の引用）、*"It makes implicit what our separate Contributor Agreement makes explicit"* | Behlendorf 氏 2005-07-11・12（"OSI-approved license that assigns contributor copyright to me"） | **有利な面（§2.6・§1.9）。** 寄与を既定でそのライセンスの下に置く条は、承認済みの Apache-2.0 が持つ。ACD §2.6 は同じ構造で、寄与者が別段を述べれば外れる |
| *"Nobody should rely on an unsigned copyright assignment, especially one that's buried in an unsigned open source license."* | Rosen 氏 2005-07（"OVPL - wrap-up of objections"） | **逆側（§2.6・§3）。** ACD §2.6 は譲渡ではなく寄与者自身の適用だが、署名なしの放棄（§3）が法域によって書面の要件に当たるかは法律家の問いである（`QUESTIONS-FOR-COUNSEL.md`） |
| *"In the meantime, and in the absence of clear law or clear precedent, it is still wise for open source licensors to obtain explicit manifestations of assent to their licenses."* | Rosen 氏 2004-05-11（"Browsewrap Agreements"） | **逆側（§2.3）。** ACD は受諾の行為を求めない。Rosen 氏は 2005-08 にも、OSL と AFL は同意が整うまで契約ではなく bare license だと書いた。ACD は条件を課さないので契約に頼らない作りだが、免責が契約なしにどこまで効くかは `against.md` #321 のとおり開いている |
| *"We can't require you to violate the law, but we can require you to not include your country's laws in your license.  And we do."* | Nelson 氏 2005-03-28（"restricting the use of open source software"） | **有利な面。** ACD は法令遵守の条も、特定の国の法も本文に置かない（§15.3） |
| *"Why impose notice burdens on folks who (when asked) will have nothing to hide, especially when almost nobody cares to read the notices anyway?"* | Rosen 氏 2005-09（"OSL 3.0: informing licensees of their rights"） | 両面（§10.2）。通知の保持を求めないことの理由になりうるが、同じ会話で他の参加者は「通知が無いと受け手が権利を知れない」と反論した（`against.md` #326・#328 と同じ論点） |

**読み。** §2.6 の寄与の既定には承認済みの先例（Apache-2.0 §5）がある。同意と署名については、2004〜2005 年の OSI の法律顧問が「明示の同意を取れ」「署名の無い譲渡に頼るな」と述べており、これは ACD の §2.3 と §3 の不利な側の記録として残る。

**逆側。** Rosen 氏の同意の助言は条件を課すライセンス（OSL）についてで、条件の無い ACD には「守らせる条件が無いので契約の効力に頼らない」という答えがある。それでも、この答えが確かめられているわけではない（B1）。

**この節が establish しないこと。** 署名なしの放棄の効力は、どの法域についても確かめていない。

**反映**: 入口 —— Apache-2.0 §5 の先例は `SUBMISSION-MATERIALS.md` §1b の §2.6 の段へ（50）。署名なしの放棄が書面の要件に当たるかは `QUESTIONS-FOR-COUNSEL.md` の問いとして 30 へ渡した。同意の助言（Rosen 氏 2004・2005）は `against.md` #321 の追記として 30 へ渡した。

## 1.354 FSF のライセンス一覧の一次資料 —— Unlicense は「献呈＋許諾」の形で GPL と両立する自由ソフトウェアのライセンスに載り、CC0 は特許の除外でソフトウェアに勧められず、0BSD は通知を外せることで「antisocial」とされる（2026-11-16）

`https://www.gnu.org/licenses/license-list.html` を 2026-11-16 に取得した（オーナーの許可・同日。curl はこの環境の権限で止まり、WebFetch で取った。**WebFetch は要約の層を通るので、下の逐語は原文の頁で当て直してから外向きの文書に引く**。頁は最終更新日を表示していない）。**照合（同日）**: portfolio-2f が別に WebFetch で取った写し（`rounds/2026-11-16-fsf-license-list-and-debian-dfsg-public-domain-snapshot.txt`・120 字ごとに分けた逐語）と、この節の FSF の引用 13 件を突き合わせた。10 件は写しにそのまま在り、3 件は写しが文を分けた所をまたぐだけで、語は一致した。2 つの独立した取得が同じ語を返したことは、要約の層が語を変えていない傍証になるが、どちらも byte の写しではない。2f の §1.253（FSF への自己点検）と `against-2.md` #328（Phipps 氏 2017 の「OSI・FSF・Debian のどれか 1 つだけの承認は未解決の問題の印」）の材料。

| 項目（頁の見出し・anchor） | FSF の文 | ACD への当たり方 |
| :-- | :-- | :-- |
| The Unlicense（*GPL-Compatible Free Software Licenses*・`#Unlicense`） | *"The Unlicense is a public domain dedication."*、*"A work released under the Unlicense is dedicated to the public domain to the fullest extent permitted by law,"* *"and also comes with an additional lax license that helps cover any cases where the dedication is inadequate."* | **有利な面（B4）。** FSF は「献呈＋許諾」の形のものを、ソフトウェアのライセンスの節に GPL と両立するものとして載せている。ACD の §3 と §4 の並存は同じ型に属する。ただし Unlicense の許諾は献呈の補い（*"helps cover any cases where the dedication is inadequate"*）として描かれ、ACD の §4.4（献呈と独立・fallback でない）の形は FSF が評していない |
| CC0 1.0（*Licenses for Works of Practical Use besides Software and Documentation*・`#CC0`） | *"If you want to release your non-software work to the public domain, we recommend you use CC0."*、*"For works of software it is not recommended, as CC0 has a term expressly stating it does not grant you any patent licenses."*、*"If the developer is refusing users patent licenses, the program is in effect a trap for users and users should avoid the program."* | **有利な面（G1・§8）。** FSF がソフトウェアに CC0 を勧めない理由は特許の除外ただ 1 つで、ACD は特許を明示に許諾する（§8.1・§8.4）。OSI の CC0 の審査で反対が集まった点（`review-precedents.md` §1.138）と同じ所を、FSF も理由にしている |
| Zero-clause BSD（*GPL-Compatible Free Software Licenses*・`#Zero-BSD`） | *"if the copyright notice or license notice is removed from the program, it is not possible to safely rely on the license"* *"and users might even face liability."*、*"We recommend that developers choose a license that clearly requires preserving notices for their own works"* *"because of the confusion and antisocial effect that is the result of the 0BSD License."* | **不利な面（#328）。** ACD の §10.2 は *"You need not give attribution, reproduce any notice, … retain this file, or inform anyone of anything"* で、0BSD と同じ性質を明示の語で持つ。FSF は 0BSD を GPL と両立する自由ソフトウェアのライセンスとして載せたまま、自分の作品には勧めないと書く。ACD が FSF に出されれば、同じ評が付くと読むのが自然である |
| Expat No Attribution（`#Expat0`・MIT-0 にあたる） | *"Our comments about the Zero-clause BSD license apply to this license."* | 同上。OSI が 2020 年に承認した MIT-0 にも同じ評が付いている —— FSF のこの評は OSI の承認を妨げなかった |
| Public domain（`#PublicDomain`） | *"Being in the public domain is not a license; rather, it means the material is not copyrighted and no license is needed."* | OSI の FAQ の *"still not a license"* と同じ向き。ACD は §4 で許諾を持つので、献呈だけのものではない |

**読み。** FSF の一覧は ACD の 3 つの部分にそれぞれ当たる。献呈と許諾の組（Unlicense）は自由ソフトウェアのライセンスとして載り、特許の明示（CC0 との差）は FSF がソフトウェアに求める点に合う。不利なのは §10.2 の通知を外せる性質で、FSF は 0BSD と MIT-0 にこれを理由に「自分の作品には勧めない」と書いた。Phipps 氏の pre-flight（#328）に当てると、ACD は FSF の自由ソフトウェアの定義を満たす側に読まれうるが、勧められない側に置かれる見込みが高い。

**逆側。** (1) FSF の「勧めない」は自由ソフトウェアでないという判断ではなく、0BSD も MIT-0 も GPL と両立するものとして一覧に在る。Phipps 氏の試験は「承認される（approved）」かを問うので、勧めないことは不承認ではない。(2) OSI は FSF のこの評の後も MIT-0 を承認した（2020）。(3) ACD を FSF に出したことは無く、上はすべて我々が他の文書の評を当てた読みである。

**この節が establish しないこと。** FSF が ACD をどう評するか。WebFetch の要約の層を通った逐語が、原文と 1 字ずつ一致すること。

**反映**: against #328（FSF の一次資料を 2026-11-16 に取り直した・逐語の置き換えは 30 へ）/ 入口（`OSI-APPROVAL-PLAN.md` の第三者の見解を得る経路の段に、FSF の一覧が ACD の 3 つの部分に当たる形を足す・50）。

## 1.355 承認は OSD への適合だけでなく共同体の益も見るべきだという声と、見慣れないライセンスは取り残されるが新しい機能で選ばれることも原理的にはある、という観察（"Proposal: criteria for license approval"・2005-09）（2026-11-16）

census の候補の外の会話（Ian Lance Taylor 氏の通を含む 31 本・9b の一覧）のうち 50 の分の 1 本。5 通を全文で読んだ（`read_thread.py`・上限で切った通 0）。Taylor 氏が OSI の理事だったかは opensource.org の頁でも写しでも確かめられなかった（2026-11-16・50）ので、決める側としては扱わない。

| 発言 | 誰が・いつ | ACD への当たり方 |
| :-- | :-- | :-- |
| *"applications should be told whether their license is approved, or whether it has been rejected (and if so what criteria it breaches and why). Where rejection is for a minor reason that would be remedied by an obvious drafting change, the words of this drafting change should be passed on."* と、承認を OSD と公表された手続きだけで判断せよという提案 | Alex Bligh 氏 2005-09-01（OVPL の審査の最中・3 人が +1） | 手続きの材料。提出者の側の要求で、OSI の規則にはならなかった。ACD の手続きの文書（`REVISION-PROTOCOL.md`）は、指摘に本文で答えて改訂する形を取る |
| *"I've generally argued that the OSI should not just blindly approve licenses which meet the requirements of the OSD, but should consider whether those licenses will help or hurt the community."* | Ian Lance Taylor 氏 2005-09-01 | B10 の側。OSD の適合は床で、共同体への益が問われうるという線（`against-2.md` #248 の 3 人と同じ向き）。ACD の答えは B10 の 3 つの効果と、条件を課さないので互換を壊さないこと（同じ通の反 GPL のライセンスの例は、他のライセンスとの組み合わせを禁じる形で、ACD はその反対） |
| *"An less extraordinary software package under an unusual license is simply doomed to be left behind--it will perhaps included in distros, but it will not attract wide attention or contributions, or be integrated into other packages."* | 同 | **不利な面（B2）。** 採用は、ライセンスでなくソフトウェアの力が運ぶという見方で、ACD を使う作品は提出者のリポジトリ 1 件だけである |
| *"It is possible in principle for a new license to be sufficiently interesting that people will adopt it in preference to the existing licenses because of new features that it has, even if it is not attached to any interesting software.  The only cases so far where I think this may actually happen are the AFL and the OSL."* | 同 | **有利な面（B10・B2）。** 機能で選ばれる新しいライセンスは原理的にありうるが稀だ、という観察。ACD が名指す機能（モデルと出力に届く特許・条件の無さ・機械学習の明示）は、この「機能で選ばれる」側の賭けである。逆側: 同氏は同じ文で、その例を 2 本しか挙げていない |

2 本目の "OPEN Source"（2005-11・11 通）も全文で読んだ。帰属と対価への一般論（OSD 1 の説明）で、ACD に当たる新しい論点は無い（Taylor 氏の 4 通は自由ソフトウェアの起こりの説明）。

**読み。** 2005 年の list には、承認を OSD だけで決めよという声と、共同体への益も見よという声が並んでいた（§1.198 の Behlendorf 氏と Nelson 氏の対立と同じ時期）。ACD にとって不利なのは「見慣れないライセンスは取り残される」の観察で、有利なのは「新しい機能で選ばれることもありうる」の観察である。

**逆側。** Taylor 氏の文は一参加者の見解で、決める側の文ではない。共同体への益を承認の基準にする案は、その後の OSI の規則の文（`review-rules.md`）にそのままの形では入っていない。

**この節が establish しないこと。** Taylor 氏が理事だったかどうか。

**反映**: B2・B10（採用はソフトウェアが運ぶという観察と、機能で選ばれる新しいライセンスの稀さ・30 へ）。
