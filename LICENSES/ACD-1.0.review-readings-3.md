---
file: LICENSES/ACD-1.0.review-readings-3.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-11-15
reachable-via: ACD-1.0.review-readings.md
canonical-ref: LICENSES/ACD-1.0.review-readings.md / LICENSES/ACD-1.0.review-readings-2.md / LICENSES/READ-THREADS.txt / LICENSES/AS-OF.md
---

# 未読のスレッドを読んだ記録（節 1.300 から・1999〜2001 のスレッド）

2026-11-15、オーナーの依頼「未読の OSI スレッドを 5 人で無くして、反映して」で、census の未読 285 本を年の帯で 5 人に分けた（30 の割り振り・2f の書き場所の案）。この文書は 1999〜2001 に始まるスレッドの記録で、節番号は 1.300 から使う（帯を分けたので、番号は文書をまたいで重ならない・Check 500 が重複を止める）。書き方は `ACD-1.0.review-readings-2.md` と同じである: 原文を引き、発言者と日付を書き、ACD への当たり方と逆側を同じ表に置き、最後に「この節が establish しないこと」を書く。論点の無い会話は節を作らず、`record_read.py --log-only` で読了だけを記録する。

**読み方。** 50 本の会話それぞれから、census が決める側として数える差出人の通を全文で、その他の通を冒頭だけ抜き出して読んだ（決める側の通 142 KB）。論点の無い会話（雑談・個別の質問・運営の連絡）は `READ-THREADS-LOG.md` に読了だけを記録した。論点のある 6 つを下の節に置いた。引用はアーカイブ（`~/osi-archive-cache`・全 508 か月の写し）の本文で、`rounds/` には置いていない。**1999〜2001 年の決める側は、いまの委員会と人も規則も違う**ので、どの節も「その時代の記録」として読む。

## 1.300 公有の宣言で著作権を手放せるか —— 1999 年の Perens 氏と 2001 年の Rosen 氏は逆を言った（B4・§3 と §4）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"If you place on your work the notice "I place this work in the public domain", you abandon your copyright rights entirely. You literally no longer have a copyright on that work at all."* | Bruce Perens 氏 1999-11-15（`license-discuss`・"Can you alter the MIT license?"） | **有利な面（§3）。** 当時の決める側の 1 人は、公有の宣言を著作権の放棄として効くものと読んだ |
| *"Nobody can "do away" with their copyright "by providing a notice that places the work in the public domain." Please don't perpetuate this myth."*、*"You have to wait for the statutory time for the work to enter the public domain."*、*"And suppose you later retract your abandonment? What's to prevent that? What's to reassure someone using your "abandoned" software that you won't later retract? Is your word "abandoned" merely a loose way of saying "I license everyone to use"?"*、*"My suggestion is, use software that comes with a reasonable license."* | Lawrence Rosen 氏 2001-06-21（当時の OSI の事務局長・法律家・"Copyright & License Questions"） | **不利な面（§3）と、§4 が答える面。** 公有の宣言で著作権は手放せない、撤回を防ぐものは何か、と法律家が書いた。ACD は §3 の放棄が効かない場合に備えて §4 で独立の許諾を与え（§4.4）、§2.2 で撤回不能と述べる —— Rosen 氏の 3 つの問い（放棄は効くか・撤回できるか・実は許諾ではないか）に、本文の側で別々に答える形である |

**読み。** 放棄が効くかについて、決める側の 2 人が 2 年の間に逆を言った。ACD の §3＋§4 の二段構え（B4）は、この割れを前提にした形である。Rosen 氏の「撤回を防ぐものは何か」は、`against.md` #324（条件の無い許諾は撤回できるという 2000 年の議論）と同じ根の問いで、ACD の答えは §2.2・§2.5（禁反言）・§4.1 の *irrevocable* である。

**逆側。** Rosen 氏の文は米国法についての当時の見解で、法域を超えた答えではない。同じ日に John Cowan 氏（当時は決める側ではない）が返した —— *"No, one can't. But I don't see why an author cannot abandon their Title 17 rights explicitly, just as any other property right can be abandoned explicitly."*（通知の文だけでは手放せないが、明示の放棄はできる、という読みで、§3 の形に近い）。§4 が独立に働くことは Rosen 氏の 3 つ目の問い（それは許諾ではないか）を認める形でもあり、§3 だけで足りるとは ACD も主張していない。

**この節が establish しないこと。** どちらの読みが正しいかは扱わない（法律家への問い 1）。

**反映**: B4（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B4 の節・Rosen 氏の 3 つの問いと §3・§2.2・§4.4 の答えの対応）。不利な面は against #324 と同じ根なので行は立てない。

## 1.301 2001 年の事務局長が挙げた審査の優先度 6 項 —— いまの委員会の最初の問いと同じ形が、25 年前に在った（B10・B2・B1・B13）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Is the license sufficiently different from one of the licenses already approved that we shouldn't simply encourage the submitter to use another already-approved license?"*、*"Is the proposed license likely to be used by a sufficiently large part of the community that it merits priority consideration?"*、*"Is the license well written and legally sound?"*、*"Has the submitter described the license in license-disucss with sufficient clarity that the community and the OSI board can understand why it is needed?"*、*"Has the community at large expressed its interest in the license by responding with meaningful comments (pro or con) on license-discuss?"* | Lawrence Rosen 氏 2001-01-19（"Cherry-picking license proposals"・本人は「自分の提案」と断っている・綴りは原文のまま） | **見込み。** 差（B10）・使用（B2）・起草の質（B1）・必要性の説明の明確さ（B13）・共同体の関心（B2）—— 2026 年の委員会が最初に訊く問い（`review-readings-2.md` §1.222）と同じ並びが、優先度の基準として既に在った |
| *"Some of the licenses ARE innovative, and it's not clear that we can reject the ones which aren't so innovative given that they comply with the open source definition."* | Russell Nelson 氏 2001-08-05（当時の理事・"approved licenses web page not being updated"） | **有利な面（B10）。** 新しさが無くても OSD に合えば退けられるか分からない、という当時の理事の立場 |
| *"OSI approves licenses if and only if the license is consistent with the provisions of the published Open Source Definition."*、*"Aspects of licenses that are not related to specific OSD provisions are irrelevant to the approval process"* | Rosen 氏 2001-09-26（"click, click, boom"） | **有利な面（当時の基準）。** 承認は OSD への適合だけで決まる、とした |

**読み。** 2001 年の記録は、承認の可否（OSD への適合だけ）と審査の優先度（差・使用・質・明確さ・関心）を分けていた。ACD の B10・B2・B1・B13 は、いまの委員会では承認の前の問いとして来るが、25 年前には「どれから審査するか」の基準だった。

**逆側。** 2001 年の「OSD への適合だけ」は、その後の運用（OSET 2015 の「文字どおり合っても承認されないものがある」・§1.241、2026 年の起草の質による却下・`board-decisions.md` §4a）で狭まっている。古い基準を有利な材料として引くなら、それが今の基準ではないことを同じ文で言う。

**この節が establish しないこと。** Rosen 氏の 6 項は本人の提案で、理事会が採った規則ではない。

**反映**: B10（`ACD-OSI-BOTTLENECKS-B10.md`・Nelson 氏 2001 の「新しさが無くても OSD に合えば退けられない」と、その後に狭まったこと）。

## 1.302 ライセンスの本文は名前を持つ文書として守られる —— GPL の改変を退け、名前を抜いた型板を求め、差分での提出を歓迎した（B6・§16.3・§16.4）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"For better or worse, the GPL is a document copyrighted by the Free Software Foundation and they have not granted permission to make derivative works."*、*"Please either use the GPL as written, adopt another approved license, or write your own license (which we will be glad to consider for approval)."* | Russell Nelson 氏 2001-11-07（"CMGPL licence"） | **有利な面（§16.4）。** ライセンスの本文を著作物として扱い、改変して同じ名で出すことを退けた。ACD の §16.4 はこの規律を本文に書いている |
| *"take the major licenses (GPL, Artistic, BSD, MPL, APSL) and genericize them - abstract all the project-specific or company-specific information into the equivalent of a header file, and allow that header file to be tweaked per-project while the licenses themselves would be entirely static and devoid of any branding."* | Brian Behlendorf 氏 1999-04-14（当時の理事・"Get ready...."） | **有利な面（B6・§16.3）。** 名前と固有名詞を抜いた不変の型板を求めた。ACD は本文に固有名詞を持たず、§16.3 で誰でも 1 語も変えずに当てられる |
| *"We've already said that changing names on a license doesn't affect OSD conformance"*、*"Patches provided in "diff" format against other OSI-approved licenses are always appreciated."* | Behlendorf 氏 2000-09-11（"License List -- as of 9-11-00"） | **手順の材料。** 承認済みとの差分での提出を歓迎した —— 2026 年の Sado 氏の「redline か innovations only の抜粋」（`against.md` #325）の 26 年前の形 |

**読み。** 本文を名前の付いた不変の文書として扱い、改変は別の名前で出す、という規律（§16.4）と、名前を抜いた型板（§16.3）は、どちらも最初の数年の決める側の言葉に在った。

**逆側。** Behlendorf 氏の型板の提案は承認済みのライセンスを整理する案で、新しいライセンスの承認の基準ではない。Nelson 氏の文は FSF との関係で述べたもので、名前の保護一般の規則としては述べていない。

**この節が establish しないこと。** 型板の提案がその後に実行されたかは扱わない。

**反映**: B6（`ACD-OSI-BOTTLENECKS.md` の B6 の節・名前を持つ本文の規律と型板・差分での提出）。

## 1.303 帰属を外せることは、当時の理事にとって「悪いこと」だった（§10.2 の費用）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Since the BSD and Apache license are so permissive in respects to redistribution of derivatives, it's entirely possible for a redistributor to remove all attribution in the codebase."*、*"So most would never be aware that the software they are using has an upstream source. I would consider this a bad thing."* | Brian Behlendorf 氏 1999-09-03（"advertising clauses"） | **不利な面（§10.2）。** 上流の出所が分からなくなることを、当時の理事は悪いことと書いた。ACD は §10.2 で帰属も通知も求めない |
| *"Giving credit is an inexpensive way of spread the benefits of participation in an open source project, and costs the current developers essentially nothing."* | Behlendorf 氏 2001-03-20（"Apache vs. BSD licenses"） | 同じ向き。帰属を求めることの費用は小さい、と書いた |

**読み。** `against.md` #41・#326 と §3e（FSF の 0BSD への注意）が記録した「表示を外せることの費用」は、1999 年の理事の言葉にも在る。

**逆側。** Behlendorf 氏は Apache の立場から書いており、帰属を求めないライセンスの承認を否定してはいない。帰属を求めない 0BSD・MIT-0・Unlicense は後に承認され、委員会は 2015 年と 2020 年にその性質を中身で受け入れた（#326）。

**この節が establish しないこと。** 当時の理事会が帰属の要求を承認の条件と考えた記録は、この 2 通からは出ない。

**反映**: against #326 に 1 文（同じ根なので新しい行は立てない・帰属を外せることの費用を 1999 年の理事が書いていた）。

## 1.304 OSD そのものも法律家の手を経ていない、法的な意味の無い依頼はなぜ要るのか（B1・§10.3）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Of course, a big problem with the OSD is that it talks about legal requirements, and yet was not touched by a lawyer before being cast into stone."* | Russell Nelson 氏 2001-09-26（"Section 2 source distribution terms"） | **B1 の両側。** 審査の基準である OSD 自身が法律家の手を経ていないと、当時の理事が書いた。法律家の関与の無いことが本文の起草だけの問題ではない、という材料だが、同じ通で同氏は書き直すなら法律の経験のある人がすべきだと続けている |
| *"If the request is no legal meaning, why do you need your license approved? If the request indeed has legal import, what problem is it solving?"* | Nelson 氏 2001-11-14（"Wonka Public Licence"・ライセンスに依頼の文を入れた提出へ） | **型（§10.3）。** 法的な意味の無い依頼の文を本文に入れることへの二択の問い（`ACD-1.4-THIRD-CLARITY-TRIAL.md` §15.6 が 2015 年の形で当てた型の 2001 年の形）。ACD の §10.3 は Dedicator の依頼が条件でないことを述べる条で、依頼そのものを本文に入れてはいない |
| *"I think it's possible to create any number of licenses that violate the spirit of the OSD while following the letter."*、*"It still makes a _wonderful_ manifesto, its success speaks for that. But to apply it blindly would be foolhardy."* | Bruce Perens 氏 2001-11-13（"Fails OSD #1."） | **見込み。** 文字どおり合っても精神に反するライセンスがある、という読み（OSET 2015・`review-readings-2.md` §1.241 と同じ線の 14 年前の形） |

**読み。** 2001 年の決める側は、OSD が法の文ではないこと、精神と文字の差、本文に法的な意味の無い文を置くことへの問いを、すでに述べていた。

**逆側。** Nelson 氏の「OSD は法律家の手を経ていない」は、だから起草に法律家は要らない、という意味ではなく、書き直すなら法律家が要る、という意味である（同じ通）。B1 の有利な材料としては使えない。

**この節が establish しないこと。** これらは 2001 年の個人の発言で、今の委員会の規則ではない。

**反映**: B1（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B1 の節・OSD 自体も法律家の手を経ていないが、書き直すなら法律家が要る、の両側）。

## 1.305 OSI が認証するのはソフトウェアで、文書ではない（2001）—— 範囲の広さへの最も古い記録と、許諾の動詞をそろえよという法律家の注文（B15・§4.2）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"OSI certifies software, not documentation, as open source. There are various documentation licenses out there. We're not decided on whether we want to certify documentation."* | Russell Nelson 氏 2001-09（"Section 2 source distribution terms"） | **不利な面（B15）。** ソフトウェアでないものへの認証を、当時の理事は決めていなかった。ACD は §1.2 でモデル・データ・文書にも及ぶ |
| *"OSI *certifies* software. OSI *approves* licenses. This is a legally significant distinction."* | Lawrence Rosen 氏 2001-09-26（"click, click, boom"・§1.301 と同じ通） | **見込み（B15）。** 承認の対象はライセンスで、認証の対象はソフトウェアだと分けた。ソフトウェアに使えるライセンスなら、他のものにも及ぶことは承認の可否と別の問いになりうる |
| *"The word "modifications" has legal significance under copyright law. It is one example of what is considered a "derivative work.""*、*"I believe that lawyers should say "derivative work" when they mean both a modification and a translation. Otherwise the license is ambiguous."* | Rosen 氏 2001-12-07（"Does "modification" include translation to another HLL?"） | **有利な面（§4.2）。** 1.4 草案の §4.2 は *"adapt, translate, modify, create derivative and collective works from"* と、翻訳・改変・二次的著作物を全部並べており、この注文に当たらない |

**読み。** B15（主題適格）の論点は 2001 年に既に在り、当時は決めていなかった。Rosen 氏の区別（ライセンスを承認し、ソフトウェアを認証する）は、2021 年の CERN-OHL の理由書の「ソフトウェアに使えるように書かれているので承認できる」（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` B15）と同じ線の、20 年前の形である。

**逆側。** Nelson 氏の文は決めていないと言っているだけで、受け入れるとも書いていない。Rosen 氏の区別も、ソフトウェア以外に及ぶライセンスを承認するとは述べていない。同じ会話で Nelson 氏は、ソースのための定義と、ソースから機械的に作られた派生物の頒布のための定義の、2 つの OSD が要ると書いた（2001-10-03・要約） —— モデルのように機械的に作られた物を、ソースと同じ定義で量ることに当時の理事も迷っていた。

**この節が establish しないこと。** ソフトウェア以外を含むライセンスを OSI が承認するかは扱わない（B15 は OSI 判断依存のまま）。

**反映**: B15（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B15 の節・ソフトウェアを認証しライセンスを承認する、という 2001 年の区別と、決めていなかった事実）。§4.2 は語がそろっているので 1.4 草案は変えない。

## 1.306 License Approval Committee は、license-discuss そのものとして始まった —— 決め方は rough consensus、承認の権限は理事会だけ（"License Approval Committee"・2003-04）（2026-11-15）

2026-11-15 に 9b の帯から引き受けた 2003 年の 16 本（portfolio-30）の 1 本。決める側の通を全文、他の通を冒頭で読んだ。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Part of this change gives license-discuss more authority. You're being deputized to serve as the License Approval Committee. License approval requests now go directly to you."* | Russell Nelson 氏 2003-04-23 | **経過（B13・B14）。** 審査の委員会は、このリストの購読者として始まった。ACD が 1.0 を出した `license-discuss` は、2003 年には審査そのものの場だった |
| *"Just to be clear, the OSI Board of Directors has sole authority to approve or disapprove licenses. That is essential to retain our certification mark."*、*"The License Approval Committee recommends only."* | Lawrence Rosen 氏 2003-04-23 | **経過。** 勧告と承認を分けた。いまの委員会の勧告と理事会の議決の形の起点 |
| *"Rough consensus. Like the IETF uses."* | Nelson 氏 2003-04-23（勧告をどう決めるかへの答え） | **見込み（B2）。** 勧告は賛否の数ではなく大まかな合意で決める、とした |
| *"For example, the Zope Public License contains the name of the Zope Corporation within it. If you want to use it, you need to create a derivative license, which in most cases will earn a rubber stamp."* | Nelson 氏 2003-04-23 | **有利な面（B6・§16.3）。** 本文に会社名を持つライセンスは、他人が使うには派生のライセンスを作る必要があった。ACD は本文に固有名詞を持たず、§16.3 で誰でも 1 語も変えずに当てられる |

**読み。** 委員会は、`license-discuss` の購読者に勧告を任せる形で始まり、承認は理事会に残された。§1.302 の「名前を抜いた型板」（1999）と同じ線が、2003 年には「名前を変えた派生はほぼ自動で通る」という運用として述べられている。

**逆側。** 2003 年の委員会はリストそのもので、いまの委員会（任命された委員と委員長）とは形が違う。「rough consensus」はいまの規則の文ではない。Zope の例は、名前を変えただけの派生が通りやすいことを言っているのであって、新しいライセンスの審査の基準ではない。

**この節が establish しないこと。** 2003 年の手続きの改定の全文（Nelson 氏が示したページ）は読んでいない。

**反映**: B6（`ACD-OSI-BOTTLENECKS.md` の B6 の節・名前を持たない型板が 2003 年には運用として述べられていた）。

## 1.307 誰も意見を書かないとき、委員長は自分から求め、1 人の賛成で承認を勧めた（"is it just summertime?"・2003-07、"please discuss EU DataGrid"・2003-09）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Are these licenses obviously open source? It would be helpful if someone other than myself would say so."* | Russell Nelson 氏 2003-07-09（2 つの提出に返信が無いことについて） | **見込み（B2・分岐 B）。** 返信の無さを、委員長は「明らかだから黙っている」とも「読まれていない」とも決めず、言葉にしてほしいと求めた |
| *"This license has been sitting around for over a month, and nobody has said anything. Maybe it's because it's obviously open source, but as committee members, I'd like to hear it explicitly from your mouths (or keyboards rather) to report back to the board."* | Nelson 氏 2003-09-26 | 同じ向き。1 か月の沈黙の後に、委員長が意見を求めた |
| *"Thanks, Ernie. I'm going to recommend that the board approve it."* | Nelson 氏 2003-10-10（1 人が「OSD との衝突は見えない」と返した後） | **有利な面（2003 年の運用）。** 沈黙の後の 1 通の賛成で、承認の勧告に進んだ |

**読み。** 2003 年の委員長は、沈黙を賛成とも反対とも読まず、明示の言葉を求めた。`review-readings.md` §1.187（2017 年の委員長: list の沈黙は読んだ印ではない）と同じ線の、14 年前の運用である。

**逆側。** 2003 年の EU DataGrid は、修正 BSD に近い短いライセンスで、委員長自身が中身を説明して求めた。ACD のように長く新しい形のライセンスが、1 通の賛成で勧告に進むとは読めない。いまの委員会は、支持の無い版の見込みを低く見る（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B2 の節・Chestek 氏 2020）。

**この節が establish しないこと。** 2003-07 の 2 つの提出がその後どうなったかは確かめていない。

**反映**: B2（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B2 の節）/ 入口（`REVISION-PROTOCOL.md` の分岐 B に 1 段・沈黙のときに決める側が明示の言葉を求めた先例）。

## 1.308 「perpetual」と書いても米国では 35 年後に終了しうる、だから明示する —— 当時の OSI の general counsel（"from advogato, open source licenses revokable?"・2003-01）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Because of the very confusion that is reflected in the discussion you referred to, my two new licenses (the Open Software License and the Academic Free License) make "perpetual" grants. I believe in being explicit."* | Lawrence Rosen 氏 2003-01-25 | **有利な面（§4.1・§2.2）。** 撤回の不安に、許諾を perpetual と明示して答えた。ACD の §4.1 は *irrevocable, perpetual* と書き、§2.2 は撤回できないと述べる |
| *"Note that, for public policy reasons, under the Copyright Act all licenses are terminable "at any time during a period of five years beginning at the end of thirty-five years from the date of execution of the grant...." 17 U.S.C. 203(a)(3). This is true even if the license states that it is "perpetual.""* | Rosen 氏 2003-01-25 | **不利な面（#152）。** 本文の *perpetual* は、米国の終了権を越えられない、とリストの上で法律家が述べた記録 |
| *"I think licenses should be written so as to be subject to both copyright law and contract law. Fuzziness in licenses is bad."* | Rosen 氏 2003-01-26 | **不利な面（#321）。** 著作権法と契約法の両方に服するように書け、とした。ACD は受諾を求めず、契約を作らない（§2.3） |

**読み。** 撤回の可否について、2003 年の法律家は「明示する」ことと「法定の終了権は越えられない」ことを同じ通で述べた。ACD の §2.2・§4.1 は前者の形で、後者は `against.md` #152 と `jurisdictions.md` が扱う。

**逆側。** 203 条の終了権は、作者の生前の許諾についての米国の規定で、ACD の §3 の放棄（許諾ではない）に及ぶかは別の問いである。Rosen 氏の「契約法にも服するように」は、ACD の設計（条件を持たず受諾を求めない）とは逆の向きで、§5 の約束を契約なしに立たせる ACD の形は、この線では弱く見える。

**この節が establish しないこと。** 203 条が ACD のどの部分に及ぶかの法的な評価はしていない（`QUESTIONS-FOR-COUNSEL.md` 問 1）。

**反映**: against #152（203 条の終了権をリストの上で法律家が述べていた）/ against #321（契約法にも服するように書け）。

## 1.309 OSI に出すのと同時に FSF にも送った、終了の条項は使う人の拒否で外された（"Termination for Patent Action"・2003-09）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I did send a copy of the license to FSF at the same time as I submitted the license to the OSI board for its approval."* | Lawrence Rosen 氏 2003-09-27（AFL 2.0 について） | **手順の先例（#328）。** OSI への提出と並べて FSF に送った。`review-readings-2.md` §1.235 の Mozilla（2010）より 7 年早い |
| *"Actually, the new AFL version 2.0 (...) doesn't contain that mutual defense clause because some key folks really hated it and refused to use any license that contained it."* | Rosen 氏 2003-09-27（URL は省いた） | **有利な面（#46 の逆側）。** 広い特許の報復の条項は、使う人が拒んだので外された。ACD は報復の条項を持たない（§8.2） |
| *"The theory behind this clause is that you need to consider carefully before you sue an open source licensor for patent infringement."* | Rosen 氏 2003-09-28 | **不利な面（#46）。** 残した狭い終了の条項の理由。ACD はこの抑止も持たない |

**読み。** 起草者が OSI と FSF の両方に並べて出すことは、2003 年にも行われていた。報復の条項の範囲は、採用者の拒否で狭められた。

**逆側。** Rosen 氏は広い条項を外して狭い条項を残した。条項を持たないことを支持したのではない。FSF に写しを送ったことは、FSF が何を答えたかを示さない。

**この節が establish しないこと。** FSF が AFL 2.0 について何を述べたかは読んでいない。

**反映**: against #328（FSF に並べて送った 2003 年の先例）/ against #46（報復の条項の範囲は採用者の拒否で狭められた）。

## 1.310 管轄を指定する、商標の名指しは自由 —— §15.3 と §11.2 に当たる 2003 年の法律家の文（"Licensing Model: Joint Copyright Assignments"・2003-04、"Open source and trademarks"・2003-07）（2026-11-15）

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Yes, that term is complex, and U.S. law may be different from that of other countries. I try to solve that jurisdiction problem by specifying a jurisdiction in all my licenses."* | Lawrence Rosen 氏 2003-04-15（「二次的著作物」の語が国で違うことについて） | **不利な面（§15.3）。** ACD は準拠法も管轄も指定しない。当時の法律家は、語の意味の国ごとの違いを、管轄の指定で解こうとした |
| *"Anyone is free to use a trademark by way of comparison ("Jello pudding tastes better than Royal pudding") or to make truthful statements about a product ("this Nokia telephone works on the AT&T Wireless network")."* | Rosen 氏 2003-07-06 | **有利な面（§11.2・§11.3）。** 真実の名指しは自由で、出所を偽る使い方だけが侵害になる。ACD の §11.2（名指しは妨げない）と §11.3（偽りは及ばない）と同じ線 |

**読み。** 準拠法について、2003 年の法律家は指定する側に立った。ACD の §15.3 は指定しない側に立つ。

**逆側。** 理事会は後に、準拠法の条について *"The Board did so with the comment that it does not believe that choice of law provisions are necessary or advisable in open source licenses."* と付言した（Pamela Chestek 氏が `license-review` 2023-03 に伝えた Open Logistics License 1.3 の承認・`rounds/2022-04-license-review-open-logistics-license-observed-15of15.txt`。`REVIEWERS.md`・against-2。2026-11-26 に直した: 初めは原文に無い並び *"not necessary or advisable"* を引用符の中に書いていた）。いまの決める側の線は ACD の側にある。Rosen 氏の通は、指定しないことの費用（語の意味が国ごとに割れる）を名指していて、その費用は残る。

**この節が establish しないこと。** 管轄を指定しないことが、どの国の裁判所でどう扱われるかは扱わない（`QUESTIONS-FOR-COUNSEL.md` 問 7）。

**反映**: against #254 に 1 文（準拠法の条を置かないことの費用を、2003 年の法律家が名指していた）。新しい行は立てない。

## 1.311 「承認済みの BSD 型のライセンスが増え続けるのは馬鹿げている、OSI はもう断るべきだ」—— 2020 年の Rosen 氏（"A modest proposal to reduce the number of BSD licenses"・2020-08）（2026-11-16）

この会話の読了は portfolio-2f が記録した（PR 3270・新しい論点は無いとして読了の記録だけ）。portfolio-30 も同じ時に決める側の通を読み、Rosen 氏の 1 通がドシエのどこにも引かれていない不利な面だったので、この節を立てた（2f と重なって読んだ。読了の数には 2f の記録だけを数える）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| 承認済みの BSD 型のライセンスが増えていることは *"ludicrous"* で、*"OSI should simply refuse to do it anymore!"*（原文の引用符は写しで文字化けしているので、その部分は逐語で引かない） | Lawrence Rosen 氏 2020-08-18（OSI の役職に無い時期。Nelson 氏の付け替えの提案に反対する通の中で *"Although I do agree that ..."* と付け加えた一文） | **不利な面（B10）。** 条件の少ない許可型のライセンスが似たまま増えることに、OSI はもう承認を出すべきでない、とした。ACD は条件の無い許可型の文書で、0BSD・MIT-0・Unlicense と同じ棚に置かれうる |
| *"For such a short license, BSD has an awful lot of variations."* | Josh Berkus 氏 2020-08-21（*"Gotta be the bikeshed problem."* と続く軽い一言） | 同じ向き（B10）だが、重くは使わない |
| 似た BSD 型の 2 つのうち片方へ寄せる再許諾の試みを提案し、法に反すると認めたうえで *"The question is what harm is created and what benefit is created, not whether a law exists or not."* と書いた | Russell Nelson 氏 2020-08-17・19 | 経過（B10）。元の理事も、似たライセンスの数を減らす方へ動いた |

**読み。** 2020 年に、元の事務局長が付け加えの一文で、似た許可型のライセンスを承認し続けることに反対した。B10 の不利な面（「既存で足りるのに増やすな」）の、許可型に絞った形である。

**逆側。** Rosen 氏の文は BSD の変種（同じ効果の言い換え）についてで、新しい効果を持つ文書を断れとは言っていない。ACD の差の主張（`ACD-OSI-BOTTLENECKS-B10.md` の G1）は「効果が違う」ことに立つので、この文がそのまま当たるのは、差が認められなかった場合である。Rosen 氏は 2005 年に「OSD に合えば承認すべき」と書いており（`review-readings.md` §1.177）、2020 年のこの文はその立場から動いた記録でもある。

**この節が establish しないこと。** 提案された再許諾がその後に行われたかは確かめていない。

**反映**: B10（`ACD-OSI-BOTTLENECKS-B10.md`・許可型の変種の増殖に、元の事務局長が「もう断るべき」と書いた）。

## 1.312 決める側の通を全文で当て直した —— 2,500 字で切っていた 12 通から、§8.5 と §16.4 に当たる 2 文（1999・2001）（2026-11-16）

2f が自分の抜き出しの穴（決める側の通を先頭の数百字で切っていた）を見つけて全文で当て直したのを受けて（2f の PR 3280）、portfolio-30 も 1.300〜1.305 を書いたときの抜き出しを測った。1999〜2001 年の 50 本では、決める側の通を 2,500 字で切っていて、12 通が切られていた。そのうち 5 通はライセンスの本文の転送（"A new open source license"・IBM Public License・3dfx・LPPL・ADPL）で、残りの 7 通を全文で読み直した。2003 年の 16 本（`read_thread.py --deciders-only`・上限 600 語）では、切れたのは 1 通の末尾 12 語だけだった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"what developers want, and what they (incorrectly) think they have under other licenses, is code that is patent-free. Sorry, it doesn't work like that; any software, under any license, can come under a claim of patent infringement by a patent holder"* | Brian Behlendorf 氏 1999-04-19（APSL 1.1 の意見募集の会話） | **有利な面（§8.5）。** ライセンスは第三者の特許から受け手を守れない、とした。ACD の §8.5 は、§8 が Dedicator の持つ請求項にしか及ばず、第三者の請求項を侵害しないことの表明でも保証でもない、と書く |
| *"I think this is unfortunate, as in a digital environment, your good name is your only asset, and protecting it shouldn't be hard. I don't see asking someone to choose a different name for a derivative work as not qualifying as "free" as the FSF defines it."* | Brian Behlendorf 氏 2001-03-20（"Apache vs. BSD licenses"） | **有利な面（§16.4・B6）。** 派生物に別の名を選ばせることは自由と両立する、とした。ACD の §16.4 は、改変したライセンスの本文を同じ名で配ることだけを妨げ、Work には何も求めない（§10.5） |

**読み。** 切られていた部分に、ACD の結論を変えるものは無かった。拾えた 2 文は、どちらも既に本文が持つ形（§8.5・§16.4）を、当時の理事の言葉で支える。

**逆側。** Behlendorf 氏 2001 は Apache の名前（製品名に「Apache」を使わせない条件）について書いており、ACD の §16.4 はライセンスの本文の名前についての条で、対象が違う。名前を守ることへの共感としてだけ読む。切られていた 12 通のうち、ライセンスの本文の転送の 5 通は意見を含まないので読み直していない。他の帯の抜き出しの上限は、それぞれの読み手が確かめる（2026-11-16 に全員へ知らせた）。

**この節が establish しないこと。** 50 本の決める側でない通は、冒頭 500 字で読んだままである。

**反映**: B6（`ACD-OSI-BOTTLENECKS.md` の B6 の節・派生に別の名を求めることは自由と両立する）。§8.5 の側は本文が既に持つので、register には行を立てない。
