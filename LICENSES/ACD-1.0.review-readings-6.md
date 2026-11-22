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

**2026-11-16 の当て直し（全文で読み直した）。** 最初の読みは決める側の通を 220 語で切っていた（30 と 2f が見つけた穴の一般形・§1.456 の冒頭）。全文で読み直すと、逆側に頼った §15.1 そのものに当たる問いが 2003 年に在った —— 同じ Rosen 氏が、契約でないと名乗る著作権の許諾の解釈の文が受け手を縛るかを問うている（§1.456）。

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

**2026-11-16 の当て直し（全文で読み直した）。** 最初の読みは決める側の通を 220 語で切り、長い会話の前半を見ていなかった。全文で読むと、この節の有利な読みには、同じ会話の中に逆側が 2 つ在った。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"It is very tempting to ask for the OSD to say "no requirements connected with use, whatsoever". But I don't believe that's what we should do."* | Bruce Perens 氏 2002-03-13（OSD の改定を任された最初の通・`rounds/2002-03-license-discuss-osd-modification-perens-not-no-use-observed.txt`） | **逆側（B10）。** 同じ OSD の起草者は、使用への要件を一切禁じることには反対した（GPL の将来の版や、免責の補償を求める条を認めるため）。この節の 1 行目「ライセンスを読まずに使える」は目標であって、「使用に要件を付けないこと」を OSD の原則にせよという主張ではない |
| *"The individuals and communities who create free and open source software deserve to receive credit for their contributions."* / *"All-in-all, I praise the advertising clause and encourage it to be used."* | Lawrence Rosen 氏 2002-01-20（同じ会話の最初の通・`rounds/2002-01-license-discuss-advertising-rosen-praise-observed.txt`） | **不利な面（`against.md` #277 の先例）。** 当時の OSI の法律顧問は、帰属表示を求める条を称えた。ACD の §10.2 は帰属表示を求めない。「条件が無いこと」は、決める側にとって無条件に良いことではなかった |
| *"Right now, people can by and large ignore open source licenses *unless* they intend to modify *and* redistribute. That's an awfully nice aspect that would be a shame to lose."* | Brian Behlendorf 氏 2002-08-06（当時の理事・`rounds/2002-08-license-discuss-click-through-behlendorf-ignore-observed.txt`） | **有利な面（B10）。** 利用者がライセンスを気にせずに使えることを、理事が手放したくない良さとして書いた。ACD は改変して再配布する者にも何も求めないので、この良さをさらに広げる |

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
| *"to prevent the use of his or her name as the author of any work which he or she did not create;"* | Lawrence Rosen 氏 2002-10-03（人格権として守るべきものの 2 つ目に挙げた） | **有利な面（B8）。** ACD の 1.4 草案は §11.3 で、作っていない作品を Dedicator が書いたと偽ることを、この文書が届く範囲の外に置き（1.0〜1.3 は理由を *"it was never the Dedicator's to permit"* と述べた。2026-11-16 の T77 で 1.4 草案はこの理由の文を外し、*"This Dedication does not make a false statement true"* と範囲の外であることの述べ方は残した）、§12.5 で人格権の放棄と不行使の約束がそこへ及ばないとする。Rosen 氏が挙げた 2 つ目の利益を、ACD は放棄の外に残している |
| *"Do we really want to go down such a path in open source licenses, opening up a whole pandora's box of litigation about what constitutes "honor or reputation" in the sofware arena?"* | Lawrence Rosen 氏 2002-10-03 | **両面（B8）。** 有利な面: ACD は名誉と声望を守る条を置かず、人格権を放棄し、放棄できない所では行使しないと約束する（1.4 草案の §12.1・§12.2）。Rosen 氏が避けたがった訴訟の箱を、ACD は開けない向きにある。不利な面: B8 は同じ §12 を「gap」とも「mission creep」とも呼ばれた記録を持ち、ライセンスが人格権を扱うこと自体を、2002 年の法律顧問は問いとして立てた —— 扱わない方がよいという読みも、この問いから出る |

**読み。** 2002 年の OSI の法律顧問は、人格権をオープンソースのライセンスで守る道に慎重で、名誉と声望の訴訟を避けたいと書いた。同時に、作っていない作品に名前を使われない利益は、守るべきものとして挙げた。ACD の 1.4 草案は、前者を放棄と不行使の約束で閉じ、後者を §11.3 と §12.5 で放棄の外に残す。2 つの扱いが、Rosen 氏の問いの 2 つの側にそれぞれ当たる。

**逆側。** Rosen 氏の問いは、ライセンスで人格権を *守る* 条（著者の側）についてで、ACD の §12 は人格権を *放棄する* 条（受け手の側）である。向きが逆の条について、同じ慎重さが当たるとは限らない。また Rosen 氏は自分で *"I actually know very little about the law pertaining to moral rights in other countries."* と書いており、放棄できない法域での不行使の約束（§12.2）の効きは、この通からは何も言えない（B1・B8）。

**この節が establish しないこと。** OSI がこの後、人格権について方針を定めたかは、この会話の範囲では確かめていない。

**反映**: B8（2002 年の法律顧問の問い —— 名誉と声望の訴訟を避ける向きと、偽の著者表示を守る向きの両方が ACD の 1.4 草案の §12 と §11.3 に当たる・逆側は「守る条」と「放棄する条」の向きの違い・30 へ）。本文は変えない。

## 1.454 OSI は法律の観点からライセンスを評価しない、承認を法的な祝福と扱うな、と OSI の法律顧問が書いた —— 同じ会話で、議論の多いライセンスに注意を早く向ける案が出た（"time frame between request for approval and acknowledgement of request?"・2002-11）（2026-11-15）

"time frame between request for approval and acknowledgement of request?"（`license-discuss` 2002-11・9 通を通読）を読み、3 通を置いた（`rounds/2002-11-license-discuss-time-frame-rosen-no-legal-blessing-observed.txt`・`rounds/2002-11-license-discuss-time-frame-rosen-buzz-observed.txt`・`rounds/2002-11-license-discuss-time-frame-nelson-pre-vet-observed.txt`）。提出者が、承認の請求への受領の知らせが来るまでの時間を尋ねた会話である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"please everyone remember that OSI does not evaluate licenses from a legal perspective. Some licenses are written by lawyers and others are not. Only your own lawyer can evaluate a license for you. So don't treat approval by OSI as if there is a legal blessing upon the license."* | Lawrence Rosen 氏 2002-11-21（署名は "General Counsel, OSI"） | **両面（B1）。** 有利な面: 承認は法律の評価ではなく、法律家が書いたライセンスもそうでないものもある —— 法的レビューの不在（B1）は、承認の基準の外にある、という読みを支える。不利な面: 同じ文が、承認は利用者に法的な保証を与えないと言う。ACD を採る人が「OSI が承認したから法的に安全だ」と読むことはできず、B2（利用者）の側の費用は承認の後も残る |
| *"Should we go with the "squeeky wheel" process: The license that gets the most conversation and comment ("buzz") on license-discuss gets expedited attention from the OSI board?"* | Lawrence Rosen 氏 2002-11-20（理事会が戦略の問題に追われ、承認が止まっていると書いた同じ通で） | **不利な面（`against.md` #109・§1.452）。** 議論の多さで注意の順を決める案で、2002 年の運用の案である。ACD の `license-discuss` への投稿には返信が無く、この案の下では後回しになる側に立つ |
| *"The problem with license submittals is that I try to pre-vet them, so that the license-discuss people don't have to waste their time with licenses that are obviously unacceptable."* | Russell Nelson 氏 2002-11-20（当時の理事） | **観測（手続き）。** 2002 年には、理事が提出を list へ回す前に下見した。いまの手続き（`license-review` への提出と委員会の審査）とは違う。ACD の手続きの読みには、いまの process ページが効く（`REVISION-PROTOCOL.md`） |

**読み。** 2002 年の OSI の法律顧問は、承認は法律の評価ではないと書いた。これは B1 の「法的レビューは要件ではない」を支え、同時に「承認は利用者に法的な保証を与えない」を述べる。同じ会話で、議論の多いライセンスを先に見る案が出ており、沈黙の続く ACD には不利な向きの運用の案である。

**逆側。** Rosen 氏の文は 2002 年の運用で、いまの Licensing Committee は条項の効き方を論じることがある（`against.md` #124 など）。「法律の観点から評価しない」がいまも同じかは、この会話からは言えない。「squeaky wheel」は案で、採られたかはこの会話の範囲では確かめていない。

**この節が establish しないこと。** この会話の提出者のライセンスが承認されたかは確かめていない。

**反映**: B1（2002 年の法律顧問「承認は法律の評価ではない・法的な祝福と扱うな」—— 要件ではないことの支えと、利用者の側の費用が残ることの両面・30 へ）/ against #109（議論の多さで注意を向ける 2002 年の案 —— 沈黙の費用の補強・30 へ）。本文は変えない。

## 1.455 法的には要らないと思うが念のため、使用の許可を明文で足した —— 承認された OSL 1.1 の起草者が書いた。同じ起草者は、前文は自分の言葉の解釈に聞こえるので書かないとした（"Right to Use"・2002-10、"Approval Requested for AFL 1.2 and OSL 1.1"・2002-11）（2026-11-15）

"Right to Use"（`license-discuss` 2002-10・10 通・決める側の通と最初の通を読んだ）と "Approval Requested for AFL 1.2 and OSL 1.1"（`license-discuss` 2002-11・27 通・決める側の通と最初の通を読んだ）から 3 通を置いた（`rounds/2002-10-license-discuss-right-to-use-rosen-observed.txt`・`rounds/2002-11-license-discuss-afl-osl-rosen-no-preamble-observed.txt`・`rounds/2002-11-license-discuss-afl-osl-rosen-country-neutral-observed.txt`）。Lawrence Rosen 氏が自分の起草した OSL と AFL の改訂版を出し、承認を求めた会話である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I don't actually believe that this provision is legally necessary in many jurisdictions but, just in case, I wanted to express the understanding of the open source community about the *use* of software."* | Lawrence Rosen 氏 2002-10-29（OSL 1.1 に "Right to Use" の条を足したと告げた通） | **有利な面（B13・B3）。** ACD の 1.4 草案の §6.5 は *"Section 6 states expressly what Sections 3 to 5 and 8 would in any event permit."* と書き、他の条が既に許すことを明文で言い直している。法律家の起草者が、要らないと思う条を念のため足した記録で、言い直しそのものは異例ではない。ACD の長さ（B3）の一部は、この種の明文化である |
| *"I'm reluctant to write a preamble, as such, because it might sound too much like interpreting my own words."* | Lawrence Rosen 氏 2002-11-06 | **不利な面（§1.450・`against.md` #124・B13）。** 同じ起草者は、ライセンスの外に自分の解釈を書くことを避けた。ACD は本文の §6.5・§8.2・§8.3 で理由を述べ、ドシエで自分の本文の読みを大量に書いている。§1.450 の Nelson 氏 2002（外の解説も解釈に使われる）と同じ根の、起草者の側の慎重さである |
| *"Almost every license on the OSI approved list specifies a US jurisdiction. The OSL is specifically intended to be country neutral in that respect."* | Lawrence Rosen 氏 2002-11-06 | **有利な面（B10 の周辺）。** ACD の 1.4 草案の §15.3 は準拠法と裁判地を定めない。2002 年の法律顧問は、米国の裁判地を定めない国に中立なライセンスを意図して書いた。ACD の §15.3 はその線にある。**逆側**: 同じ会話で Rosen 氏は、OSL の下では許諾者が裁判地を決め、利用者は許諾者の所在で権利を求められる、と書いており（2002-11-06・2002-11-17 の通）、「定めない」とは違う。ACD の「定めない」が国に中立と読まれるかは、この会話からは言えない |

**読み。** 承認された OSL 1.1 の起草者（法律家・当時の OSI の法律顧問）は、要らないと思う使用の許可を念のため明文で足し、同時に、前文で自分の言葉を解釈することは避けた。ACD は前者（§6.5 の明文化）と同じ向きにあり、後者（解説を書かない）とは逆の向きにある。

**逆側。** Rosen 氏の「念のため」の条は 1 文で、ACD の §6 は 5 つの項（1.4 草案）である。明文化の量は比べられていない。また、前文を書かないことを選んだのは起草者自身の判断で、OSI の基準ではない。

**この節が establish しないこと。** AFL 1.2 と OSL 1.1 がこの会話の後に承認されたかは、この会話の範囲では確かめていない（§1.240 は OSL と AFL の複数の版が承認されたと Rosen 氏 2013 が書いたことを記録している）。

**反映**: B13（承認されたライセンスの起草者が、要らないと思う条を念のため明文で足した —— §6.5 の明文化の先例・30 へ）/ against #124（同じ起草者が、前文で自分の言葉を解釈することを避けた —— §1.450 と同じ根・30 へ）/ 1c（§15.3 の「定めない」と OSL の「国に中立」の違いを、逐条の §15.3 の逆側に足す候補）。本文は変えない。

## 1.456 ライセンスの本当の読み手は法律家だ、だから著作権法の語を使う —— そして、契約でないと名乗る著作権の許諾の解釈の文が受け手を縛れるか、と同じ起草者が問うた（2002-11・2003-01）（2026-11-16）

9b の帯の 31 本を、決める側の通を 170〜220 語で切って読んでいたことが分かった（30 の確認の依頼・2026-11-16）。切れていた決める側の通と最初の通は 39 通、出力の末尾しか見ていなかった長い会話が 5 本あった。全文で読み直し、§1.450・§1.451 に当て直しの段を足し、新しい論点をこの節に置いた。2 通を置いた（`rounds/2002-11-license-discuss-afl-osl-rosen-real-reader-observed.txt`・`rounds/2003-01-license-discuss-derivative-work-rosen-interpretive-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"But the real reader of an open source license is another lawyer who is going to advise his client what that word means."* / *"I'm using language from the Copyright Act on purpose."* | Lawrence Rosen 氏 2002-11-06（OSL 1.1 と AFL 1.2 の承認を求めた会話・同じ通の追伸で *"The license has been submitted to several companies' attorneys for review"* と書いた） | **不利な面（B1・B13）。** 承認された OSL の起草者は、読み手を法律家と置き、法令の語を意図して使い、複数の企業の弁護士の審査も経た。ACD は "Covered Rights" などの自前の定義語で書かれ、弁護士の審査を経ていない。**逆側**: 同じ起草者は「承認は法的な祝福ではない」とも書いた（§1.454）—— 法律家の起草は承認の要件ではない |
| *"But when a license purports NOT to be a contract and intends to be interpreted in the same way worldwide under copyright law alone, then I don't understand how you can go beyond what that law provides."* / *"How can a licensee be bound to interpretive language in a *mere* copyright license?"* | Lawrence Rosen 氏 2003-01-14（GPL の "work based on the Program" の読みをめぐる会話） | **不利な面（§1.450 の逆側への問い・B1）。** §1.450 は、ドシエの不利な読みが意図の証拠として持ち出されても、1.4 草案の §15.1（受け手に多く与える読みが勝つ）と §15.6 がその向きを倒す、と書いた。Rosen 氏の問いは、その種の解釈の文が契約でない許諾の中で効くかに向いている。**逆側**: Rosen 氏の問いは *受け手を* 解釈の文で縛ることについてで、ACD の §15.1 は Dedicator の側を縛る向き（受け手に多く与える）である。許諾者が自分に不利な読みを自分で約束する形は、受け手に義務を負わせる形とは違う。どちらが効くかは法の問いで、ここでは決まらない（B1） |
| *"In particular, your claim that your license is not a contract is legal hogwash."* | Lawrence Rosen 氏 2002-10-27（BXAPL の提出者への返信・同じ通で、改変者に著作権の譲渡を課す条は受け入れられないと書いた・`rounds/2002-10-license-discuss-bxapl-rosen-not-a-contract-observed.txt`・2f の全文の当て直しで拾った） | **両面（`against.md` #321・B1）。** 有利な面: BXAPL は義務（著作権の譲渡）を課しながら「契約でない」と名乗った。ACD は義務を課さず、自らを契約でないとも名乗らない（1.4 草案の §2.3 は受諾が要らないと述べるだけ）。批判の的は「契約なしの義務」で、「義務の無い許諾」ではない。不利な面: 法的性質についての言い切りは、法律家が最初に突く場所である。ACD の入口には、法律家の確認の無い法的性質の言い切りが在る（`ACD-1.0.faq.md` の未履行双務契約の行・50 が限定を見る） |

**読み。** 2002〜2003 年の OSI の法律顧問は、ライセンスを法律家に読まれる文書として書き、契約でない許諾の解釈の文の効きを疑った。ACD は自前の定義語で書かれ、§15 の解釈の規則に頼る部分がある。どちらも B1 の「法律家の読み」の問いに戻る。

**逆側。** 同じ起草者は、法律家の起草が承認の要件ではないこと（§1.454）と、要らないと思う条を念のため明文で足すこと（§1.455）も書いた。ACD の §15.1 が受け手を縛らず Dedicator を縛る向きであることは、Rosen 氏の問いの的を外れる読みを支える。

**この節が establish しないこと。** Rosen 氏の問いに裁判所がどう答えたかは、この会話からは分からない。ACD の §15.1 が効くかは確かめていない（B1）。

**反映**: B1（承認されたライセンスの起草者は読み手を法律家と置き、企業の弁護士の審査を経た・30 へ）/ B13（自前の定義語と法令の語・1c へ種）/ against #124（§1.450 の逆側が頼る §15.1 に、契約でない許諾の解釈の文の効きという問いが当たる・30 へ）/ against #321（BXAPL の「契約でないという主張は戯言」—— 30 が PR 3336 で入れた・入口の法的性質の言い切りは 50 へ）。本文は変えない。


## 1.457 受け手が実行してよいと OSD が明記していればもっと安心だ —— 理事の「適法に受け取ったコピーは使うのが自由だ」を引いた参加者の通（"Subscription/Service Fees - OSD Intent"・2001-03）（2026-11-16）

census の外の 31 本（Ian Lance Taylor 氏が多く書いた会話・Taylor 氏は OSI の役を一次資料で確かめられていないので DECIDERS に入れていない・50 の判断）のうち、9b が 1999〜2001 の 14 本を全文で読んだ。13 本は GPL・LGPL の一般論で、ACD に当たる新しい論点は無かった（READ-THREADS-LOG）。この節は残る 1 本で、2 通を置いた（`rounds/2001-03-license-discuss-subscription-fees-taylor-nelson-quote-observed.txt`・`rounds/2001-03-license-discuss-subscription-fees-taylor-run-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"If you have legally received a copy of a program (and OSD #1 guarantees the right of the person giving you a copy to do so), you are free to use it or not, as you wish. Copyright law only restricts copying. You could only restrict the activities of a *recipient* if you could require them to execute a license, but OSD #7 prohibits that."* | Russell Nelson 氏（当時の理事）の文を、Ian Lance Taylor 氏が 2001-03-28 の通で引いた（*"Russ Nelson (who is on the OSI board) said this"*。元の通は未特定） | **有利な面（B10・§1.451 と同じ線）。** 理事は、受け手の使用を縛る手段が OSD の下では無いと書いた。ACD は使用を縛らず、1.4 草案の §3・§4・§6.1 で使用の許可を明文で述べる |
| *"I myself am uncertain, which is why I would be happier if the OSD had an explicit statement that a recipient of a program was permitted to run it."* | Ian Lance Taylor 氏 2001-03-28（決める側とは確かめられていない参加者） | **有利な面（B13・§1.455 と同じ線）。** 使用の許可を明文で書くことへの求めは、承認された OSL の起草者（§1.455）だけでなく、参加者の側にも在った。ACD の §6.5 の「他の条が既に許すことを明文で言い直す」理由と同じ向き |

**読み。** 2001 年の list で、受け手が使ってよいことは OSD から導けるが明文ではない、という不安が書かれ、理事の「使用を縛る手段は無い」が引かれた。ACD はそれを明文で書く側に在る。

**逆側。** Taylor 氏は決める側と確かめられていないので、この節の重みは §1.451・§1.455 より低い。Nelson 氏の文は Taylor 氏の引用で、元の通をこの節では特定していない。明文化は長さ（B3）の費用を持つ。

**この節が establish しないこと。** OSD が後に実行の明文を足したかは、この会話からは分からない。

**反映**: B10（§1.451 の有利な面の補強 —— 理事の「使用を縛る手段は無い」を参加者が引いた・重みは低い・30 へ）/ B13（§6.5 の明文化の求めは参加者の側にも在った・1c へ種）。本文は変えない。

## 1.458 違反のしようが無いライセンスは存在理由が無く、OSI が承認する理由も無い —— WTFPL の不承認のときの委員長の理由（2009）。同じ委員長は 1 年前、バイナリで表示を求めない Boost の承認を勧めていた（2008）（2026-11-16）

census の `unquoted-decider`（候補の外の会話のうち、決める側の通でドシエが 1 文も引いていない通・`census_decision_statements.py threads`）の 1999〜2016 年分 484 通を、9b が読んだ（2017〜2023 年は portfolio-2f・§1.257）。手順は §1.257 と同じで、各通を切らずに論点の語で点数づけし、点の付いた通を上から全文で読んだ（5 点以上 171 通のうち上位 100 通。通は写しの file 名と Message-ID で引き、484 通すべてを引けた・PR 3419）。8 通を `rounds/` に置いた。下の表のほか、IPA Font（2009・Perens 氏と Tiemann 氏がフォントの source と binary の区別を論じた）と Open Source Hardware License（2007・取り下げ）は B15 の材料として読み、新しい論点は無かった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The only (ONLY) reason to write a license rather than putting your software into the public domain is because you plan to sue at least one of your users eventually."* / *"The WTFPL is impossible to violate"* … *"Thus, it is a license with no reason to exist, and a license which the OSI has no reason to approve."* | Russ Nelson 氏 2009-03-14（委員長・WTFPL の審査・`rounds/2009-03-license-review-wtfpl-nelson-no-reason-to-exist-observed.txt`） | **不利な面（B4・B10）。** ACD は §10.1 で受け手に条件を課さない。この基準では ACD も「違反のしようが無い」ので、存在理由が問われる。`board-decisions.md` §8.1 の WTFPL の不承認（*"It's no different from dedication to the public domain"*）の、委員長自身の言葉での理由である |
| Boost について *"The license is closest to the MIT license, but gives the additional release from needing to include the copyright notice in binaries."* / *"Recommend: Approval"*。同じ報告で別の提出に *"Rosen suggests that this license is worthless because it is too simple."* | Nelson 氏 2008-01-09（委員長の委員会報告・`rounds/2008-01-license-discuss-committee-report-nelson-boost-observed.txt`） | **有利な面（§10.2・#326）。** 表示の義務を MIT から外したライセンスを、同じ委員長が承認へ勧めた。ACD の §10.2 はすべての形で表示を求めない。外したのはバイナリの表示だけなので、ACD ほど遠くはない。**両面（B3）**: 短すぎることも欠点として挙がった |
| *"the discernable record of purported provenance and copyright ownership in most open source codebases is generally inaccurate and gets decreasingly accurate over time. I don't actually think this is a problem, in practice"* | Richard Fontana 氏 2015-10-13（委員長・FPL 1.0.0（0BSD）の報告への Moen 氏の異議への答え・`rounds/2015-10-license-review-committee-report-fontana-provenance-observed.txt`） | **有利な面（§10.2・#326 の補強）。** `review-readings.md` §1.216 の報告の続きで、写しから出所が消えることを問題としない理由を述べた |
| *"Conforming to the OSD is a necessary but not sufficient condition."* / 「好きにしてよい」が文字どおりなら *"it offers nothing over public domain"*、国際的な同等物が要るなら CC0 | Ernest Prabhakar 氏 2009-03-31（理事会オブザーバーと署名・`rounds/2009-04-license-review-committee-report-prabhakar-net-benefit-observed.txt`） | **不利な面（B10・B4）。** 承認は共同体への利益で量られ、考慮は *"proliferation, validity, and comprehensibility"* だと書いた。ACD には「CC0 で足りるのでは」が向く |
| *"the world does not have an intrinsic need for any more open source licenses"* / 求めるのは *"a license that is visibly better than any other license"* | Nelson 氏 2004-12-01（German Free Software License・`rounds/2004-12-license-discuss-gfsl-nelson-intrinsic-need-observed.txt`） | **不利な面（B10）。** 新しいライセンスは既存より目に見えて良いことを示す側に負担がある |
| *"These days I believe the OSI Board is also interested in reasons why a proposed license is a good idea in addition to meeting the OSD."* | Simon Phipps 氏 2008-12-15（TGPPL・後の理事と会長。2008 年の役は確かめていない・`rounds/2008-12-license-review-tgppl-phipps-reasons-beyond-osd-observed.txt`） | **不利な面（B10）。** OSD への適合の外に、なぜ良い考えかの理由が要る |
| MPL 2.0 について、増殖への扉を開く条項は *"not in itself grounds for rejection"* | Karl Fogel 氏 2011-12-15（理事会へ勧告を送ると書いた・`rounds/2011-12-license-review-mpl2-fogel-proliferation-not-grounds-observed.txt`） | **有利な面（B10）。** 増殖のおそれは、それだけでは却下の理由にならない |
| NOSA 2.0 は振り返れば *"outright reject it as being way too complex with a number of likely or actual fatal problems"* が良かった / 直した版は *"generally been prepared by the license steward rather than that task being taken on by the OSI itself"* | Fontana 氏 2016-08-20（ARL OSL の会話・`rounds/2016-08-license-discuss-arl-fontana-nosa-too-complex-observed.txt`） | **不利な面（B3）・両面（B1）。** 複雑さそのものが却下の理由になりうる（`board-decisions.md` §8.2 の NOSA 2.0 の決議と同じ向き）。直すのは提出者の仕事で、OSI は起草を引き受けない |

**読み。** 2004〜2016 年の決める側の通は、新しいライセンスに「OSD への適合の外の理由」を求めた（Nelson 氏・Prabhakar 氏・Phipps 氏）。最も鋭いのは Nelson 氏の WTFPL への理由で、条件を課さないこと自体を存在理由の欠如と読んだ。ACD の中心の設計（§10.1）にそのまま当たる。

**逆側。** Nelson 氏の基準は、その後の承認で方針にならなかった。理事会は 2015 年に FPL 1.0.0（0BSD）を *"Essentially the same as the WTFPL license"* と言われながら 8 対 0 で承認し（`board-decisions.md` §8.6）、2020 年に MIT-0 も承認した。どちらも違反のしようが無い。同じ Nelson 氏は 2008 年に、表示を求めない Boost を承認へ勧めていた。Fogel 氏は増殖のおそれだけでは却下しないと書いた。ただし Prabhakar 氏の「CC0 で足りるのでは」は、ACD がなぜ CC0 でないかを示す側の負担として残る（B10 の差の主張）。

**この節が establish しないこと。** Nelson 氏の理由が 2009 年の理事会の決定の理由と同じだったか（決定の文は「パブリックドメインへの献呈と違わない」）。Prabhakar 氏の通がどのライセンスの審査か（件名は委員会報告への返信）。Phipps 氏の 2008 年の役。

**反映**: B10（Nelson 氏 2004・Prabhakar 氏 2009・Phipps 氏 2008 の「適合の外の理由」を不利な側に、Fogel 氏 2011 を有利な側に・30 へ）/ B4（Nelson 氏 2009 の WTFPL の理由を `board-decisions.md` §8.1 の決定の文の隣に置くか・逆側の 0BSD と MIT-0 と同じ段に・30 へ）/ B3（Fontana 氏 2016 の「複雑すぎるので却下が良かった」と、Nelson 氏 2008 の報告の「短すぎて無価値」を同じ段に・30 へ）/ 入口（§10.2 の説明に Boost の承認の勧めと Fontana 氏の出所の文を足せるか・#326 の行・50 へ）。本文は変えない。


## 1.459 準拠法を定めさせない方がよい（Perens 氏 2008）、誰でも使えるライセンスを推してきた（Nelson 氏 2004）、商標は「権利を与えない」の告知の形で足りた（Behlendorf 氏 2004）—— ACD-1.4 の §15.3・§16.3・§11.1 の形に当たる。WTFPL の不承認の委員長の理由には、ライセンスにできる 3 つのことが並んでいた（Nelson 氏 2009-03-19）（2026-11-23）

§1.458 の続き。9b は census の `unquoted-decider` の 1999〜2016 年分 476 通（2026-11-23 の実行。§1.458 の時点は 484 通）のうち、論点の語に当たる 171 通の上位 100 通を読んだ。portfolio-d7（採掘の役）は、同じ `B_TOPICS` の語の当たりの数で 171 通を並べ直し、9b が読んだ上位の外の 78 通（当たりが 1 回の通。順位の境の同点を含めるため 71 通より多く取った）を、写しの file 名と Message-ID で引いて全文で読んだ。写しは 2026-11-23 00:35 JST に `fetch_osi_watch.py --to-cache` で今月と先月を取り直したもので、census は 828 本のうち 828 本を読了・未読 0 のまま（11-22 の写しから byte は変わっていない）。6 通を `rounds/` に置いた。当たりが 0 回の通（305 通）は読んでいない。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Would it be approvable? No.  It serves no purpose.  Yes, a license CAN be used to disclaim warranty, but this one does not.  Yes, a license CAN be used to deny use of a trademark, but this one does not.  Yes, a license can require that you keep its terms constant, but this one does not."* / *"This license does nothing to protect the licensor, and gives the licensees all permissions."* | Russ Nelson 氏 2009-03-19（委員長・WTFPL の不承認の後・`rounds/2009-03-license-review-wtfpl-nelson-three-things-a-license-can-do-observed.txt`） | **両面（B4）。** §1.458 の 03-14 の通（「違反のしようが無いライセンスは存在理由が無い」）より具体的な理由で、ライセンスにできることを 3 つ挙げた。ACD-1.4 は 2 つを持つ —— 保証の否認（§13・責任の制限は §14）と、商標の権利を与えないこと（§11.1）。3 つ目（条項を一定に保つ）は、改変した文をその名で配ってはならないとする §16.4 で、WTFPL と同じ「名を変えれば改変してよい」の型である。**逆側**: 「受け手にすべての許可を与える」は ACD にもそのまま当たり（§10.1）、Nelson 氏の結論の半分は残る |
| *"the WTFPL was written in Europe where you don't seem to be able to put something into the public domain.  So you need a license that effectively does the same."* | Martin Michlmayr 氏 2009-03-16（同じ会話・census の決める側の一覧に入る。2009 年の役は確かめていない） | **有利な面（B4）。** パブリックドメインに置けない法域のために、同じ効果のライセンスが要る —— ACD が §4 で予備の許諾を置く理由と同じ。ただし 2009 年の理事会は WTFPL を承認しなかった |
| *"So software that is "public domain" (to use your term) is not certifiable.  This is not intended as a value judgment, merely as a description of what our certification mark is used for."* | Lawrence Rosen 氏 2001-01-23（当時 OSI の法律顧問・`rounds/2001-01-license-discuss-ipl-rosen-public-domain-not-certifiable-observed.txt`） | **両面（B4）。** 承認と認証は、承認されたライセンスの下で配られるソフトウェアに付く。献呈だけでは対象にならず、ACD が承認の対象になりうるのは §4 の予備の許諾があるからだ、という読みを支える。逆に、献呈の部分は OSI の評価の外に在る、とも読める |
| *"It is true that this public domain result doesn't apply outside the U.S. But if you apply a valid open source license to it"* | Rosen 氏 2016-07-22（ARL の提案） | **有利な面（B4）。** 米国でパブリックドメインになる政府の著作に、外国のためにオープンソースのライセンスを重ねよ —— 献呈と予備の許諾を重ねる ACD と同じ形の助言。ただし Rosen 氏が勧めたのは既存の Apache 2.0 で、新しいライセンスではない（B10） |
| *"OSI can not practically get into the business of evaluation of national law, it would be better to require that licenses do not specify choice of law."* | Bruce Perens 氏 2008-03-16（EUPL の審査・`rounds/2008-03-license-review-eupl-perens-no-choice-of-law-observed.txt`） | **有利な面（ACD-1.4 の §15.3）。** ACD-1.4 は *"specifies no governing law and no forum"*。§1.455 の反映に書いた OSL の「国に中立」との違いの逆側に、審査者の側から「定めない」を求めた文が在る。**逆側**: 同じ会話で Nelson 氏は 2008-03-15 に「準拠法は法域の選択にすぎず、無ければ法律家はどの法の下の文書かを知らずに書くことになる」と書いた（要約）。審査者の間で割れている |
| *"That's why we've pushed hard for licenses which may be reused by anybody.  On the other hand, if somebody insists on a license which cannot be reused, we'll approve it reluctantly."* | Nelson 氏 2004-06-11 / *"reference to a specific project ought to be omitted, otherwise the license would practically be limited to a single use -- a one-way free ticket to proliferation."* Carlo Piana 氏 2015-07-02（TOPPERS の審査） | **有利な面（ACD-1.4 の §16.3・B10）。** ACD-1.4 は *"It is not specific to any project, person, organisation, jurisdiction, or field of endeavour"*。特定のプロジェクトに縛られたライセンスは増殖の種と読まれたが、ACD はその形ではない |
| *"In the 1.0 license, it was phrased as "you must not use our marks".  In an attempt to bring us closer to being compatible with the GPL and LGPL, we changed this in 1.1 to "nothing gives you the right to use".  Thus it was changed from an "additional restriction" as defined by the GPL (and thus incompatible) to a more passive informational notification."* / *"So far, we have not noticed a change in behavior of licensees due to the change of license"* | Brian Behlendorf 氏 2004-09-28（census の決める側の一覧に入る・Apache の経験・`rounds/2004-09-license-discuss-closed-standard-behlendorf-nothing-gives-right-to-marks-observed.txt`） | **有利な面（ACD-1.4 の §11.1・§11.3）。** ACD-1.4 の §11.1 は *"grants no right in any trademark"*、§11.3 は *"it is not a condition upon You"* —— 禁止ではなく告知の形で、Behlendorf 氏が追加の制限にならないとした側に在る。Rosen 氏 2003-03-11 も AFL の同じ形を *"a reminder rather than an order"* と書いた（"Compatibility of the AFL with the GPL"）。告知の形にしても濫用は増えなかった、という実務の観察も付く |
| *"In general, I worry about building trademark-law-type provisions into licenses that are really about copyright"* | Karl Fogel 氏 2014-06-30（NASA の審査の委員会報告・法令が既に禁じることを条に繰り返す必要があるか、と問うた） | **不利な面（B3）。** §11.3 と §11.4 は、法が既に定める限界（偽りの表示・他人の人格権とデータ保護）を条で述べる。告知の形であっても「要るのか」という問いは向く（長さの論点） |
| *"I don't see "better liability disclaimer" a good proxy to assess the worthiness of a new license in terms of non-proliferation."* | Piana 氏 2014-03-12（Public Software License の審査・`rounds/2014-03-license-review-psl-piana-disclaimer-not-a-proxy-observed.txt`） / *"I know of no specific reason (other than desire for elegance) why one could not simply supplement the form disclaimers with additional ones."* Richard Fontana 氏 2014-03-12（同じ会話） | **不利な面（B10）。** 否認は法域に依存する道具で、より良い否認は新しいライセンスの価値の代わりにならない。ACD が既存との差を述べるときに §13 の否認を挙げても重みは無い。差の主張は §8（特許）・§12（人格権）・§3（献呈の構造）に置く |
| *"You really should have a native English speaking lawyer review this license."* / *"if one language license says that you are free to do something, but the other says that you are not, then you are free to do it."* | Nelson 氏 2004-11-26（German Free Software License・`rounds/2004-11-license-discuss-gfsl-nelson-native-english-lawyer-observed.txt`） | **不利な面（B1）・両面（ACD-1.4 の §15.4）。** 英語を母語としない起草者に、英語を母語とする法律家のレビューを求めた。ACD の起草者は日本語を母語とし、法律家のレビューは無い（B1）。言語の食い違いには「自由な側が勝つ」を勧めた。ACD-1.4 の §15.4 は「英語の文が勝つ」で、§15.1 の「受け手に多く与える読みが勝つ」は英語の文の中の読みにだけ掛かる。訳を頼りにした受け手が、訳の方が広いときに守られない形で、次の版の候補になる |
| *"You said that the license was authored by lawyers in Japan. Does the license exist in an official Japanese language form?"* | Fontana 氏 2015-09-02（TOPPERS の審査・広すぎる免責の語が日本語の法律の語の写しではないかと問うた） | **両面（B1）。** 日本で書かれたライセンスに、審査者は日本語の公式の版と語の対応を尋ねた。ACD は英語で起草し、日本語の公式の版を持たない（ACD-1.4 の §15.4）ので、その問いには「無い」と答えられる。ただし、起草者の母語が英語でないことへの注意そのものは向く |
| *"to reject a licence because it is also available in other languages, however, is to say that open source should only be used and distributed by people who understand (and whose lawyers understand and work with) english."* | Rishab Ghosh 氏 2008-03-16（理事として・EUPL の審査） | **有利な面（ACD-1.4 の §16.4 の訳の扱い）。** 訳を持つことは却下の理由にしない、と理事が書いた。ACD-1.4 は訳を名と識別子で配ることを許し、英語の文が勝つと書かせる |
| *"If this were not a legacy license, I would push to replace that with the phrase "one of the following two conditions" just to make it completely clear.  Given that it is legacy (and thus, already in use with that wording), I think a framing paragraph on the OSI page is sufficent."* | Josh Berkus 氏 2015-06-12（TOPPERS の審査） | **不利な面（B3・B2）。** 既に使われている旧来のライセンスには語のぎこちなさを許し、新しいライセンスには「完全に明確に」を求める。ACD は新しく、利用の実績も 1 件なので、明確さの基準は高い側で当たる |
| *"The ultimate purpose of a license is to guide the judge in his or her ruling. If it works for programmers and not for the judge, it doesn't really work."* | Perens 氏 2010-04-05（BSD+1 の審査） | **両面（B1・B3）。** ACD-1.4 の明確さの試作（`ACD-1.4-CLARITY-TRIAL.md` から THIRD まで）は、読み手を裁判所に置く方向の作業で、この基準に答える側に在る。ただし、裁判所の目で読んだのは法律家ではない（B1） |
| *"since the steward of those licenses didn't ask for OSI approval, it did not make much sense to conduct a review and/or approval."* | Mike Milinkovich 氏 2007-07-05（GPLv3 の提出の会話・Microsoft のライセンスを第三者が出した時の扱いを引いた） | **有利な面（B12）。** 審査は steward が求めて行う、という先例の読み（問いの形で書かれた）。ACD の提出は steward であるオーナーが行うので、この型には当たらない |

**読み。** ドシエが 1 文も引いていなかった 2001〜2016 年の決める側の通には、ACD-1.4 の後半の条（§11・§15・§16）の形に直接当たる文が在った。準拠法を定めないこと（Perens 氏）、誰でも使えること（Nelson 氏・Piana 氏）、商標を告知の形で外すこと（Behlendorf 氏・Rosen 氏）は、どれも ACD-1.4 が既に取っている形で、審査者の側から求められていた。WTFPL の不承認の委員長の理由（Nelson 氏 03-19）は、ライセンスにできることとして保証の否認と商標の否定を挙げ、ACD はその 2 つを持つ。

**逆側。** 有利な文の多くは、承認の基準として採られた文ではなく、一人の審査者の意見である。準拠法については同じ会話で Nelson 氏が逆を書いた。WTFPL の理由の後半（「受け手にすべての許可を与える」、同じ通の続きの「パブリックドメインそのものだ」）は ACD にもそのまま当たり、2009 年の理事会は WTFPL を承認しなかった（`board-decisions.md` §8.1）。不利な文 —— 英語を母語とする法律家のレビュー（Nelson 氏 2004）、新しいライセンスに高い明確さ（Berkus 氏 2015）、否認は価値の代わりにならない（Piana 氏 2014）—— は、B1・B3・B10 のどれも動かさず、重さを足す。

**この節が establish しないこと。** Michlmayr 氏の 2009 年の役。Nelson 氏 03-19 の 3 つの「できること」が理事会の決定の理由と同じだったか（決定の文は「パブリックドメインへの献呈と違わない」）。Perens 氏の「準拠法を定めさせない」が、その後の審査で求められたか（2008 年以降の承認に準拠法を持つものは在る）。当たりが 0 回の 305 通に、ACD に当たる文が無いこと。

**反映**: B4（Nelson 氏 2009-03-19 の 3 つの「できること」と、ACD が 2 つを持ち 3 つ目は WTFPL と同じ型であることを `board-decisions.md` §8.1 の §1.458 の段の隣に・Rosen 氏 2001 の「パブリックドメインは認証の対象にならない」と Michlmayr 氏 2009・Rosen 氏 2016 を予備の許諾の理由の側に・cd へ）/ B10（Piana 氏と Fontana 氏 2014 の「より良い否認は価値の代わりにならない」を差の主張の不利な側に・cd へ）/ B1（Nelson 氏 2004 の英語を母語とする法律家のレビューを不利な側に・cd へ）/ B3（Berkus 氏 2015 の新旧の明確さの基準、Fogel 氏 2014 の商標法の型の条への懸念を不利な側に・cd へ）/ 入口（§15.3 の説明に Perens 氏 2008 を、§11.1 の説明に Behlendorf 氏 2004 を、§16.3 の説明に Nelson 氏 2004 と Piana 氏 2015 を足せるか・逆側の Nelson 氏 2008-03-15 を同じ段に・6d へ）/ 1c（§15.4 の「英語の文が勝つ」に、訳と英語が食い違うときは受け手に多く与える側が勝つ、を足す案 —— Nelson 氏 2004 の勧め。ACD-1.4 の確定の後の次の版の候補で、確定を止めない・5e へ）。本文は変えない。
