---
file: LICENSES/ACD-1.0.review-readings-6.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-11-15
reachable-via: ACD-1.0.review-readings.md
canonical-ref: LICENSES/ACD-1.0.review-readings.md / LICENSES/ACD-1.0.review-readings-2.md / LICENSES/READ-THREADS.txt / LICENSES/AS-OF.md
---

# 未読のスレッドを読んだ記録（節 1.450 から・2002〜2003 と 2009〜2010 のスレッド）

2026-11-15、オーナーの依頼「未読の OSI スレッドを 5 人で無くして、反映して」で、census の未読 285 本を年の帯で 5 人に分けた（30 の割り振り・2f の書き場所の案）。この文書は 2002〜2003 と 2009〜2010 に始まるスレッドの記録で、節番号は 1.450 から使う（帯を分けたので、番号は文書をまたいで重ならない・Check 500 が重複を止める）。書き方は `ACD-1.0.review-readings-2.md` と同じである: 原文を引き、発言者と日付を書き、ACD への当たり方と逆側を同じ表に置き、最後に「この節が establish しないこと」を書く。論点の無い会話は節を作らず、`record_read.py --log-only` で読了だけを記録する。

## 1.450 ライセンスについて書いた物は、前文でも別の解説でも、条文の解釈に使われる —— だから最良の本文を書いて、あとは黙れ、と Nelson 氏は書いた（"Static v. Dynamic Linking -- redux"・2002-03）（2026-11-15）

"Static v. Dynamic Linking -- redux"（`license-discuss` 2002-03・13 通）を通読し、1 通を置いた（`rounds/2002-03-license-discuss-static-dynamic-nelson-interpret-observed.txt`）。静的リンクと動的リンクのどちらが二次的著作物を作るかを Lawrence Rosen 氏が論じた会話で、裁判官が意図をどう読むかに話が移った。Russell Nelson 氏は当時の理事で、同じ年の別の会話で「今日の理事会でこの件を出す」と書いている（"OpenE License"・2002-02-27）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"In a lawsuit, the judge will interpret the license to try to divine your intention. That is why anything you write in or about a license -- even if it's "just" a preamble and postamble, or in a separate commentary -- is used to interpret the terms of the license."* | Russell Nelson 氏 2002-03-16（同じ通の冒頭で *"Again, I must stress that this is not based on experience, but instead on learning."* と断っている） | **不利な面（B13・`against.md` #124 の逆側）。** #124 は Pamela Chestek 氏 2026-09-01 の、本文の外の文を裁判所が考慮する義務は無い、という文を引き（逐語は #124 に在る）、ドシエの説明は本文の曖昧さを直さない、と記録した。Nelson 氏の読みはその反対の向きで、本文の外に書いた物も意図を探る材料になる。**2 つは両立する**: 外の説明は本文を直す力を約束されず（Chestek 氏）、しかも読まれうる（Nelson 氏）。ACD のドシエは本文の約 100 倍の語数があり（`REVIEWERS.md` 冒頭の実測・2026-11-15）、`against.md` は ACD の文の不利な読みを自分で書いている。裁判官がそれを Dedicator の意図として読むと、我々が「こう読まれうる」と書いた不利な読みが、意図の証拠として働く向きがある |
| *"That's why you do best to write the best license you can, and then shut up about it."* | Russell Nelson 氏 2002-03-16 | **不利な面（B3・B13）。** ACD の本文は §6.5・§8.2・§8.3 で理由を述べ、ドシエは本文の約 100 倍ある（同じ実測）。「黙れ」の反対側に立っている |

**読み。** 2002 年の理事は、ライセンスについて書いた物は（本文の外の解説も）意図を探る材料として使われる、と書いた。2026 年の元委員長は、本文の外の説明を裁判所が考慮する義務は無い、と書いた。決める側の 2 人の読みは向きが逆で、どちらも「外の説明で本文の曖昧さを直す」ことは当てにできない、という点で一致する。

**逆側。** Nelson 氏は法律家ではなく、自分で「経験ではなく学んだこと」と断っている。ACD の本文（1.4 草案）は §15.1 で、読みが分かれるときは受け手に多く与える読みが勝つと定め、§15.6 で起草者に不利に解する原則と付与を狭く解する原則の両方を外している。ドシエの不利な読みが意図の証拠として持ち出されても、本文の §15.1 がその向きを受け手に有利な側へ倒す。ただし §15.1 が裁判所を拘束するかは、それ自体が本文の外の法の問いで、ここでは決まらない（B1）。

**この節が establish しないこと。** 2002 年の米国で、ライセンスの外の解説が実際に解釈に使われた判決を、この会話は挙げていない。ACD のドシエが解釈に使われた事例は無い（ACD を争った訴訟は無い）。

**反映**: against #124（逆側の補強 —— 外の説明は直す力を約束されず、しかも読まれうる・30 へ）/ B13（ドシエの不利な読みが意図の証拠として働く向き・`QUESTIONS-FOR-COUNSEL.md` に問いとして足す候補・30 へ）。本文は変えない（1.4 草案の §15.1・§15.6 が既にその向きを扱う）。

## 1.451 「コピーを持っているなら、それで何をしてもよい」と OSD は言うべきだった —— 使用に条件を付けるライセンスを、理事は意図して承認したことが無いと書いた（"Advertising Clauses in Licenses"・2002-01〜02、"NCSA Open Source License"・2002-01）（2026-11-15）

"Advertising Clauses in Licenses"（`license-discuss` 2002-01〜02・39 通）と "NCSA Open Source License"（`license-discuss` 2002-01・19 通）を通読し、3 通を置いた（`rounds/2002-02-license-discuss-advertising-nelson-use-observed.txt`・`rounds/2002-01-license-discuss-advertising-perens-run-observed.txt`・`rounds/2002-01-license-discuss-ncsa-rosen-no-opinion-observed.txt`）。広告条項（バッジウェア）を OSD がどう扱うかの会話で、Bruce Perens 氏が OSD に「使用への負担」を禁じる文を足すことを提案した。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"One of the goals of the OSD was to have software that the user could run without having to read the license or take any special action."* | Bruce Perens 氏 2002-01-20（OSD の起草者） | **有利な面（B10）。** ACD の §10.1〜§10.4 は、受け手に条件・義務・制限を課さず、何も知らせなくてよいと定める。OSD の起草者が述べた目標を、条件を持つライセンスより文字どおりに満たす |
| *"Unfortunately, the OSD is not very well written. For example, it says nothing about use, so multiple parties have tried to say "Yeah, you can copy this software, but in order to use it, you have to license it from us." We squashed them using #7 (fortunately!), but the OSD really ought to say "If you have a copy of this software, you can do anything you want with it.""* | Russell Nelson 氏 2002-02-13（当時の理事） | **有利な面（B10・B4）。** ACD の §3 と §6.1 は、コピーを持つ者が何をしてもよいことを、使用を含めて書いている。理事が「OSD が言うべきだった」とした文の形に、ACD の本文は近い |
| *"The OSI board of directors approves licenses if they are consistent with the OSD. The board renders no opinion about the validity or enforceability of specific clauses in specific licenses."* | Lawrence Rosen 氏 2002-01-20（当時の OSI の法律顧問） | **有利な面と不利な面（B1）。** 承認は OSD との整合で決まり、条項の有効性の意見ではない —— B1（法的レビューが無い）は承認の基準そのものではない、という読みを支える。ただし同時に、承認は ACD の §3 や §4 が各国で有効だとは言わない。審査者が有効性を論じないなら、ACD の有効性の問いは承認の後も残る |

**読み。** 2002 年の決める側の 3 人は、使用に条件を付けないことを OSD の目標（Perens 氏）、OSD に書かれるべきだった原則（Nelson 氏）として述べ、承認は条項の有効性の意見ではない（Rosen 氏）とした。ACD の「条件を一切課さない」設計は、この 3 つの文と同じ向きにある。

**逆側。** 同じ会話で Nelson 氏は *"We've never intentionally approved use-restricted licenses before."* と書いたが（"OSD modification regarding what license can require of user"・2002-03-16）、それは条件を持つライセンスの話で、条件を持たないライセンスが承認に有利だとは言っていない。条件が無いことは OSD の下限を越えるだけで、B10（既存の許容的なライセンスで足りるのでは、という問い）には答えない —— MIT や 0BSD も使用に条件を付けない。また Rosen 氏の文は 2002 年の理事会の運用で、2026 年の Licensing Committee が条項の有効性を論じる例（`against.md` #124 など）とは時代が違う。

**この節が establish しないこと。** Perens 氏が提案した OSD の追加の文が採られたかは、この会話の範囲では確かめていない。

**反映**: B10（有利な面 —— 決める側が 2002 年に「使用に条件を付けない」を OSD の目標と原則として述べた・逆側は MIT と 0BSD も同じ・30 へ）/ B1（Rosen 氏 2002 —— 承認は条項の有効性の意見ではない・有利と不利の両面・30 へ）/ 入口（「条件を一切課さない」の説明に OSD の起草者の目標を引く候補・50 へ）。本文は変えない。

## 1.452 議論が止んだことは承認を意味しない、議論の参加者はボランティアだ —— そして冗長なライセンスでも、勧めに反して求めるなら承認する、と同じ理事が書いた（eNetwizard のライセンス・2002-10）（2026-11-15）

"Moral Rights"（`license-discuss` 2002-10・9 通を通読）と "Modified Artistic License (eNetwizard Content Application Server)"（`license-discuss` 2002-10・4 通を通読）は、同じ提出（Robert Samuel White 氏のライセンス）の承認をめぐる会話である。3 通を置いた（`rounds/2002-10-license-discuss-moral-rights-nelson-volunteers-observed.txt`・`rounds/2002-10-license-discuss-enetwizard-nelson-redundant-observed.txt`・`rounds/2002-10-license-discuss-moral-rights-rosen-attorney-observed.txt`）。提出者は `license-discuss` で指摘を受けて直し、指摘が止んだので承認されると考えていた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Here's the problem: Robert worked with the people on license-discuss to fix the problems in his license. He thought that, when they stopped suggesting changes, that that meant that his license would be approved. The people on license-discuss are volunteers. Their contributions are valuable and valued. Unfortunately, you can't beat up volunteers to get them to contribute more."* | Russell Nelson 氏 2002-10-07（当時の理事） | **ACD の沈黙の読みへの先例（`against.md` #109・#228）。** ACD は 2026-08-26 に `license-discuss` へ出し、アーカイブに返信は無い。我々は「沈黙を支持と読ませない」と決めている（`REVISION-PROTOCOL.md` §3.6 分岐 B）。2002 年の理事が、議論が止んだことを承認と読んだ提出者を、その誤りとして名指した記録で、我々の決めごとと同じ向きにある。**不利な面も同じ文に在る**: 議論の参加者はボランティアで、議論を引き出すことはできない —— 沈黙が続くことは提出者には変えられない |
| *"Is not having your name on the license sufficient reason for us to approve a redundant license?"* | Russell Nelson 氏 2002-10-07 | **不利な面（B10・B2）。** 既存のライセンスで得られないものが「自分の名前」だけなら、冗長なライセンスだ、という問い。ACD が答えるべき問いは、既存のどのライセンスでも得られないものは何か、である（B10 の表がその答えの試み） |
| *"How is the world served by Yet Another Not Very Different License? The answer: it isn't."* / *"I'd really, really like you to consider using an existing license. Consider it *hard*. If, in the end, against best advice, you want your own license approved, you'll get it."* | Russell Nelson 氏 2002-10-03 | **両面（B10）。** 不利な面: 冗長さへの強い反対。有利な面: それでも 2002 年の運用では、OSD に合えば、勧めに反しても承認した。**逆側**: 2026 年の委員会は冗長さ（proliferation）を却下の理由に挙げうる（`against.md` に在る 2026-09-24 の議事録の 4 本の却下）。2002 年の「求めるなら承認する」は、今の基準ではない |
| *"We've all said many times that, if RSW's license is OSD-compatible, it will be approved. I do recommend, however, that RSW seek an attorney's advice. I recommend that to everyone who wants to "roll his own" license."* | Lawrence Rosen 氏 2002-10-06（当時の OSI の法律顧問・事務局長） | **両面（B1）。** 承認の基準は OSD で、弁護士の助言は勧めであって条件ではない（有利）。ただし決める側の法律家は、自作のライセンスを出す全員に弁護士の助言を勧めた（不利 —— ACD は受けていない） |

**読み。** 2002 年の決める側は、(1) 議論が止んだことは承認を意味しないと書き、(2) 冗長なライセンスに強く反対しながら、OSD に合えば承認するのが運用だと書き、(3) 弁護士の助言を条件ではなく勧めとした。(1) は ACD の沈黙の読みと同じ向きで、(3) は B1 の「要件ではない」の読みを支える。

**逆側。** (2) の「求めるなら承認する」は 2002 年の運用で、いまの委員会は冗長さを理由に却下しうる。ACD に有利な先例として引くなら、時代の違いを同じ場所に書く必要がある。(1) は我々の決めごとを支えるが、沈黙を変える手段を与えない —— 議論の参加者に議論を求めることはできない、とまで書かれている。

**この節が establish しないこと。** eNetwizard のライセンスが最終的に承認されたかは、この 2 つの会話の範囲では確かめていない。

**反映**: against #109（沈黙の読み・決める側の 2002 年の先例を足す・30 へ）/ B10（冗長さへの反対と、2002 年の「求めるなら承認する」・時代の違いを逆側に・30 へ）/ B1（弁護士の助言は勧めで条件ではない・同時に全員に勧めた・30 へ）。本文は変えない。

## 1.453 ソフトウェアの人格権をライセンスで守ると「名誉と声望」をめぐる訴訟の箱を開けるのでは、と OSI の法律顧問が問うた —— ACD は放棄し、偽の著者表示だけを外に置く（"Moral Rights"・2002-10）（2026-11-15）

同じ "Moral Rights"（`license-discuss` 2002-10）から、Lawrence Rosen 氏の最初の通を置いた（`rounds/2002-10-license-discuss-moral-rights-rosen-question-observed.txt`）。著者の「芸術的な管理」を求める 2 つのプロジェクトの声を受け、人格権を OSD に合う形でどう扱うかを、提出者と Bruce Perens 氏らに問うた通である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"to prevent the use of his or her name as the author of any work which he or she did not create;"* | Lawrence Rosen 氏 2002-10-03（人格権として守るべきものの 2 つ目に挙げた） | **有利な面（B8）。** ACD の 1.4 草案は §11.3 で、作っていない作品を Dedicator が書いたと偽ることを、この文書が許せる範囲の外に置き（*"it was never the Dedicator's to permit"*）、§12.5 で人格権の放棄と不行使の約束がそこへ及ばないとする。Rosen 氏が挙げた 2 つ目の利益を、ACD は放棄の外に残している |
| *"Do we really want to go down such a path in open source licenses, opening up a whole pandora's box of litigation about what constitutes "honor or reputation" in the sofware arena?"* | Lawrence Rosen 氏 2002-10-03 | **両面（B8）。** 有利な面: ACD は名誉と声望を守る条を置かず、人格権を放棄し、放棄できない所では行使しないと約束する（1.4 草案の §12.1・§12.2）。Rosen 氏が避けたがった訴訟の箱を、ACD は開けない向きにある。不利な面: B8 は同じ §12 を「gap」とも「mission creep」とも呼ばれた記録を持ち、ライセンスが人格権を扱うこと自体を、2002 年の法律顧問は問いとして立てた —— 扱わない方がよいという読みも、この問いから出る |

**読み。** 2002 年の OSI の法律顧問は、人格権をオープンソースのライセンスで守る道に慎重で、名誉と声望の訴訟を避けたいと書いた。同時に、作っていない作品に名前を使われない利益は、守るべきものとして挙げた。ACD の 1.4 草案は、前者を放棄と不行使の約束で閉じ、後者を §11.3 と §12.5 で放棄の外に残す。2 つの扱いが、Rosen 氏の問いの 2 つの側にそれぞれ当たる。

**逆側。** Rosen 氏の問いは、ライセンスで人格権を *守る* 条（著者の側）についてで、ACD の §12 は人格権を *放棄する* 条（受け手の側）である。向きが逆の条について、同じ慎重さが当たるとは限らない。また Rosen 氏は自分で *"I actually know very little about the law pertaining to moral rights in other countries."* と書いており、放棄できない法域での不行使の約束（§12.2）の効きは、この通からは何も言えない（B1・B8）。

**この節が establish しないこと。** OSI がこの後、人格権について方針を定めたかは、この会話の範囲では確かめていない。

**反映**: B8（2002 年の法律顧問の問い —— 名誉と声望の訴訟を避ける向きと、偽の著者表示を守る向きの両方が ACD の 1.4 草案の §12 と §11.3 に当たる・逆側は「守る条」と「放棄する条」の向きの違い・30 へ）。本文は変えない。
