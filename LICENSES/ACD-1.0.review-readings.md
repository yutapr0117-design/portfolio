---
file: LICENSES/ACD-1.0.review-readings.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-11-09
canonical-ref: LICENSES/ACD-1.0.reviewer-positions.md (主題ごとの記録) / LICENSES/ACD-1.0.gap-measurements.md (差の測定) / LICENSES/ACD-1.0.against.md
---

# 未読のスレッドと審査の帰結を読んだ記録（§1.164 以降）

`ACD-1.0.reviewer-positions.md`（§1.155〜§1.159）と `ACD-1.0.gap-measurements.md`（§1.154・§1.160〜§1.163）が予算の 900 行に近づいたので、2026-11-09 から新しい節をここに置く。**既存の節は動かしていない**ので、他の文書の `§1.1xx` の参照はそのまま元の文書で解決する。§1.xx は `ACD-1.0.*.md` の共有の採番で、この文書は §1.164 から続ける。

どの節も、原文を引き、発言者と日付を書き、ACD への当たり方と逆側を同じ表に置き、最後に「この節が establish しないこと」を書く。引用の原文は `rounds/` に置く。

## 1.164 CC0 の審査で、決める側が特許について述べたこと（記録に無かった段落）（2012-02）（2026-11-09）

`rounds/2012-02-license-review-cc0-submission-patent-statements-observed.txt`。§1.138 は審査の本体を読んだが、ここに置く段落は引いていなかった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I suspect, or at least would like to think, that if Creative Commons were drafting CC0 today, knowing that CC0 would be enthusiastically applied to software as well as to nonsoftware content, those two words "or patent" might not be in the document, and something else might be there in its place"* | Richard Fontana 氏 2012-02-18 | CC0 から "or patent" を外し、別のものを置く形への期待。ACD の §8 はその場所に明示の許諾を置く。同じ日に同氏は *"I've encouraged use of CC0 by Red Hat developers for certain things (such as sample code or other kinds of relatively small pieces of code)"* とも書いた |
| *"Requiring an explicit patent grant in new licenses /might/ be over-reaching. Being sensitive about disclaimers of patent grants and their potential to harm developers is probably appropriate."* | Bruce Perens 氏 2012-02-17 | 明示の許諾は要件ではないが、除外は害になりうる、という線。ACD は要件の側ではなく、除外をしない側に立つ（§8.3） |
| *"We decided long ago that patents -- or any other screwy laws one country or another might invent -- are beyond the remit of OSI to worry about."* | Russ Nelson 氏 2012-02-17 | 逆側。特許は OSI の判断の外、という立場（#233 の対称性と同じ人）。同じ審査で委員会の報告は 4(a)（特許の除外）を理由に不承認を勧めた（*"Recommend disapprove"*・§1.138） |
| 承認済みライセンスを「patent」の語の有無で分けて調べ、*"So we're sort of approaching CC0 territory but aren't squarely in it, with existing OSI-approved licenses, as far as I can tell."* | Karl Fogel 氏 2012-02-18 | 特許を明示に除く承認済みの先例が無かったという調べ。ACD はその逆側（明示の許諾）に立つ |
| BSD・MIT・CC0 では特許の許諾は黙示で、*"there is possibly an unfortunate assumption by some here that implied patent licenses are enforceable in all jurisdictions"* | Lawrence Rosen 氏 2012-02-20 | 黙示の許諾に頼らず明示する理由。§8.3 の *"A dedication that gives away copyright while withholding patent rights leaves the recipient exposed"* と同じ向き |
| CC0 が付けられる作品について *"artistic works can be infringing of machine, process, and composition patents"* | Bruce Perens 氏 2012-02-20 | ソフトウェアでない作品にも特許が掛かる、という見方。ACD の §8 はデータや文書の Work にも及ぶ（B15 の主題の広さと同じ向き） |

**読み。** CC0 の審査では、明示の許諾を要件にする声（DiBona 氏 2012-03・§1.138）と、特許は OSI の判断の外とする声（Nelson 氏）の間に、「要件ではないが除外は害」という線（Perens 氏）と、「今なら除外の語は無いだろう」という見方（Fontana 氏）があった。ACD の §8 は除外の代わりに明示の許諾を置く形で、この線の上に立つ。

**この節が establish しないこと。** どれも個人の発言で、CC0 の審査の帰結は CC の取り下げである。Fontana 氏の期待は CC0 についてのもので、ACD の §8.4（モデルと出力）までは述べていない。

## 1.165 著作権の無いものに特許だけを許諾するとき —— オープンソースと両立する条件（2002・2005）（2026-11-09）

`rounds/2002-to-2005-license-discuss-standalone-patent-licences-observed.txt`。どれも Lawrence Rosen 氏の発言。

| 発言 | ACD への当たり方 |
| :-- | :-- |
| *"if the only thing that is being contributed is a patent without any copyrightable subject matter, then a standalone patent license would be needed. But that patent license must be compatible with open source. It cannot impose conditions that are incompatible with open source."*（2005-01-11） | ACD の §8 は §3・§4 に依存せずに働き（§2.4・§8.6）、権利の無い Machine-Generated Material にも特許の許諾が届く（§9.2）。条件を 1 つも持たない（§8.2・§10.1）ので、この線の内側にある |
| *"To be compatible with open source, the patent license must at least extend to the creation of conforming implementations, and it must not forbid non-conforming implementations."*（2005-01-14） | 標準の文脈での最小の線。§8.1 は *"the Work or anything derived from it"* に及び、派生物を禁じない |
| W3C の特許方針の議論で、許諾を標準の実装に限る案について *"Open source representatives were almost alone in lobbying for a patent license of unlimited scope."*、OSL と AFL の許諾は特定の実装に結ばれず *"are broader than the W3C patent grant."*（2002-11-21） | オープンソースの側は範囲の広い特許の許諾を求めていた、という記録。§8.4 の伸びの向きと合う。逆側: 同じ通は *"In most cases this field of use limitation will have little practical effect."* とも述べ、特許を持つ側の多くは限定を求めた（B7） |

**この節が establish しないこと。** どれも 2002 年と 2005 年の個人の発言で、OSI の決定ではない。標準の特許方針の文脈で述べられたもので、ACD のような献呈を論じたものではない。

## 1.166 新しい概念を持つライセンスを、弁護士が起草して出し、2 か月半後に提出者が自分で止めた —— Tidepool の審査（2013-10〜12）（2026-11-09）

`rounds/2013-10-to-12-license-review-tidepool-health-data-observed-1of2.txt` と `-2of2.txt`（13 通）。非営利の Tidepool Project が、1 型糖尿病の機器のデータを扱うソフトウェアのために出したライセンスで、提出者は *"The Tidepool license is permissive as to source code, and "copyleft" as to the open data requirement."* と書いた。ソフトウェアを使って健康データを集める者に、そのデータを本人へ開くことを求める条件を持つ。委員長の 2013-10-09 の報告は *"Discussion is ongoing and active."*・*"No recommendation at this time."* だった。2013-12-19 に提出者は、コードの大半を BSD-2-Clause で、一部を GPLv2 で出すと書き、ライセンスは GitHub で練り続け *"when we feel we have achieved a reasonable consensus on the Tidepool License and attained OSI compliance"* に移すとした。`license-review` の 2013-11〜2014-12 には、この後の議論も決定も無い（件名に残る報告の題を除く）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The license was drafted by Heather Meeker of Greenberg Traurig, who also participated in the creation of the Mozilla licenses."*（提出文の "Legal Review" の節） | Howard Look 氏（提出者）2013-10-05 | B1。弁護士の起草は提出文に節を立てて書かれ、それでも 2 か月半で提出者が止めた。UPL（`gap-measurements.md` §1.154）と並んで、弁護士の関与が承認を決めなかった例になる。**逆側**: 止めた理由は審査の否定ではなく、提出者自身の *"getting a new open source license right is hard - especially one with novel concepts such as the Tidepool License."*（2013-12-19）で、コードの公開を待てなかったことが大きい |
| *"These are a combination of policy issues and textual interpretation (where the main relevant texts are this license and the OSD)."*・*"Not sure how much more useful lawyers qua lawyers are, in general, for things like this."* 同じ通に Rosen 氏が *"+1."* | Richard Fontana 氏 2013-10-11、Lawrence Rosen 氏 2013-10-13 | B1。Berkus 氏の *"That's a lawyer question, really; the license certainly looks open source from a developer perspective."*（2013-10-10、OSD に適合し独自かという問いについて）への返事で、OSD 適合の問いは政策と文言の解釈だとした。2017 年の同氏の発言（`reviewer-positions.md` §1.156）と同じ向きで、4 年早い。**逆側**: 同じ通は *"Lawyers may be able to provide some insight, especially regarding how the license itself is likely to be interpreted in practice."* とも書く。ACD の新しい条項（§8.4、§7、§12）が実務でどう読まれるかは、まさにこの範囲で、我々はそれを持っていない |
| *"its provisions are fairly easy to understand, and it does not appear to duplicate any existing license."* | Josh Berkus 氏（開発者として）2013-10-05 | B10・B13。開発者の側の基準は、読みやすさと既存のものと重ならないことだった。ACD の差は B10 の行が条文で立証している。**逆側**: ACD は 4,896 語で（B3）、読みやすさのほうは Tidepool より不利である |
| *"Completely unrelated to approval, have you thought of simply calling it the Health Data Software License?"* | Josh Berkus 氏 2013-10-05 | B6。steward の名を外した一般的な名前を勧めたが、本人が承認とは関係ないと断っている。Behlendorf 氏も *"Same reason we've tried to avoid vendor-specific licenses."*（2013-10-07）と書いた。ACD の名前は steward の名を含まない。**逆側**: 名前は承認の基準として述べられていないので、有利にも数えない |
| *"asking whether there are new kinds of rights worthy of protecting with the same kinds of nuances and range that we've managed with protecting access to source code and the rights to modify."* | Brian Behlendorf 氏 2013-10-07 | B10。新しい種類の権利を扱うライセンスを歓迎した発言。**逆側（同じ通）**: *"it'd be great to avoid a proliferation of licenses with the same terms only because someone decided their personal data use cases weren't primarily"* 健康 —— 分野の名だけで分かれる同じ条件のライセンスは proliferation と読まれる。ACD を「AI 向けの CC0」と読む人には、この懸念がそのまま当たる。ACD の差は分野の名ではなく、条項の働き（§8 の特許、§7 のデータベース権、§9 の Machine-Generated Material）で立てる必要がある（#316） |
| *"Despite what the OSD literally says or doesn't say, there is an expectation in open source that there is some large zone of software user privacy"*・*"The key idea is that open source licenses are supposed to be highly unburdensome"* | Richard Fontana 氏 2013-10-07 | 書かれていない基準の 1 つ（#248 の一覧と同じ種類）。Tidepool の条件は内部の使用にも及ぶので、この基準に当たった。Cowan 氏も機械可読の形を求める部分に *"In any case, this is a technology restriction which looks to me to violate OSD #10."*（2013-10-06）と書いた。ACD は使用にも頒布にも条件を置かない（§10.1）ので、どちらにも当たらない。**逆側**: これは条件を持つライセンスへの基準で、条件が無いことを利点として述べたものではない |
| *"Given that you have decided to dual-license your software under GPLv3 (an OSI-approved license) and this new license, why are you seeking OSI approval for the new license?"* | Richard Fontana 氏 2013-10-06 | B10。承認がなぜ要るのかを、審査する側が提出者に問うた。提出者は 2013-10-24 に、繰り返し受けた懸念の 1 つとして *"3) Concern about us offering a new license at all"* を挙げた。ACD も同じ問い（なぜ既存のものと特許の許諾の組み合わせではないか）を受ける。**逆側**: Fontana 氏の問いは二重許諾を前提にしたもので、ACD は二重許諾ではない |
| *"They are the experts on privacy of electronic information and the licensing of non-software."*・*"Most of us are not also on those lists so please let us know if they recommend your license."* | Lawrence Rosen 氏 2013-10-13 | B15。ソフトウェアでないものの許諾について、審査に近い人が Creative Commons と EFF のリストを専門の場として挙げた。ACD の §1.2 は data と audiovisual material を含む。**逆側**: これは健康データの扱いに条件を課すライセンスへの発言で、OSI がソフトウェアでないものを含むライセンスを審査しないという意味ではない（data files を主題に明記したライセンスの承認は 2 度ある・`review-outcomes.md` §1.119） |
| *"I believe that because this license is coming from NASA, it should be held to a relatively high standard. I think there is a natural bias in favor of approval of the license (because of NASA's prominence, technological and cultural, as a US government agency, and because OSI has certified a predecessor license)."* | Richard Fontana 氏 2013-10-31（同じ報告のスレッドで、NOSA 2.0 について） | B12・B2。steward が著名だと承認へ自然に偏る、と審査する側の人が認め、だから高い基準で見ると述べた。ACD には著名さも先行の承認も無いので、この偏りは働かない。**逆側（有利）**: 同じ文は著名さを補正すべきだという立場で、著名でない提出者を不利に扱えとは言っていない。NOSA 2.0 は著名さがあっても 3 年半決まらなかった（`review-outcomes.md` §1.118・#317） |

**読み。** Tidepool の審査で論点になったのは、ほぼ全部が「使う者に課す条件」（データを開く義務、その形、期間、研究の例外、内部の使用）だった。ACD の新しさは条件ではなく、許諾の範囲（§8・§7・§9）にある。だから Tidepool で効いた反対の多くは ACD に当たらない。当たるのは、弁護士の関与（B1）、新しいライセンスを出すこと自体への懸念（B10）、分野の名で分かれるライセンスへの懸念（B10）、ソフトウェアでないものの専門の場（B15）、steward の著名さ（B12）の 5 つである。**有利な面**: 提出者が止めたのは審査の否定によるものではなく、待つ間コードを公開できなかったからである。ACD は 1.3 をこのリポジトリに適用したまま審査を待てるので、この理由で止まることは無い。**不利な面**: 提出者が止めた時点で、提出したライセンスで出したコードは無く、利用は既存の承認済みライセンスへ移った。新しいライセンスの利用が 1 件のまま審査が長引くのは、B2 の形と同じである。

**この節が establish しないこと。** どの発言も個人のもので、OSI の決定ではない。Tidepool は承認も不承認もされず、提出者が自分で止めた。委員長の報告は勧告をしていない。Tidepool のライセンスは条件を持ち、ACD は持たないので、Tidepool の帰結から ACD の帰結は導けない。弁護士の起草が承認を決めなかったことは、弁護士の関与が不要だということを意味しない。

## 1.167 委員長が「差は小さく価値も限られる」と書いたライセンスを、OSD 適合を理由に承認へ勧めた —— MirOS Licence（2008-07〜09）（2026-11-09）

`rounds/2008-07-to-09-license-review-miros-licence-approval-observed.txt`（8 通）。2008-07 の Nelson 氏の 2 通（*"not improvement *enough*"* と 2 つの学派）は `rounds/1999-to-2026-license-lists-unread-threads-cited-observed-4of5.txt` に在り、#302 が引いている。

**経過。** Thorsten Glaser 氏は 2008-07-05 に MirOS Licence を出し直した。提出文は自分のライセンスを *"clearly not a licence most people would want to use"* と書き、利用を「大きいプロジェクト 1 つと小さいもの 2〜3」とした。委員長の Russ Nelson 氏は 7 月に、既存のライセンスへ移るよう求め、2008-07-13 には *"Approve your license? LOTS and LOTS of people have told us not to do that. Basically, you're out-voted."* と書いた。同じ通は *"Even the entire license review committee's opinion doesn't necessarily carry the day."*・*"The MirOS License will go before the board for a vote."* とも書く。2 か月後、同じ委員長の報告（2008-09-07）は次のとおりだった —— *"The license is obviously OSD compliant, but it is Yet Another academic license of limited difference and limited value. I've asked him to use an existing academic license, but he refuses."*、そして *"Recommend: approval"*。理事会の 2008-09-10 の議事録は、RTEMS と UJIL についての修正を付けて報告を受け入れたと記録し、MirOS については、OSD に適合するので承認すべきだが、独自のことをしていないので推奨のライセンスにはならない、という趣旨を書く（https://opensource.org/meeting-minutes/minutes20080910/ を 2026-11-09 に要約する道具で読んだ。逐語の写しは置いていない）。OSI のライセンス一覧の API（`opensource.org_api_licenses.json`・2026-10-27 取得）は MirOS の承認日を 20080910 とする。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The license is obviously OSD compliant, but it is Yet Another academic license of limited difference and limited value."*・*"Recommend: approval"* | Russ Nelson 氏（委員長）2008-09-07 | B10。差が小さく、提出者が既存のライセンスへの移行を断っても、OSD に適合することで承認が勧められた。**逆側**: 議事録の趣旨は「承認するが推奨はしない」で、2017 年の「承認して目立つ一覧には載せない」（#315）と同じ形である。同じ委員長は同じ年の 2008-05 に、MIT/X11 に近い別のライセンスに *"Recommend: rejection for similarity"* を出している（#302）。どこからが「似すぎ」かの線は、読んだ記録には無い |
| *"Approve your license? LOTS and LOTS of people have told us not to do that. Basically, you're out-voted."* | Russ Nelson 氏 2008-07-13 | B2・B10。7 月のリストの反対は、9 月の帰結を決めなかった。**逆側**: 7 月から 9 月の間に何が変わったかは、読んだ記録には書かれていない。2 か月後の勧告を「反対があっても通る」の一般則として読むことはできない |
| *"it is in active use, and because some platforms (such as BerliOS/Sourceforge/...) discriminate against licences that are not OSI approved"*、同じ人が 2008-07-09 に *"weak argumentation base here"* | Thorsten Glaser 氏（提出者）2008-07-08 | B2。利用の少なさと論拠の弱さを提出者自身が認めた提出が承認された。ACD の提出文も不利な事実を自分から述べる。**逆側**: MirOS には MirOS Project の開発者と外部の利用者があった。ACD の利用は本リポジトリ 1 件である |
| *"only used in code copyrighted by you"*、別の通で *"but I'd like to hear some stronger statement from actual European developers before I consider that a 'sufficient' reason for a new license."* | Ernest Prabhakar 氏（理事）2008-07-09、2008-07-10 | B2・B10。理事の問いは、legacy でない新しいライセンスに十分な理由があるか、だった。ACD はまさに「steward の作品にだけ使われている新しいライセンス」の位置にある。**有利な面**: 同じ位置の MirOS は 2 か月後に承認された |
| *"which has the interesting side-effect that the MirOS Licence also conforms to the Open Knowledge Definition (at least I think)"*（"software" の代わりに "work" の語を使ったことについて） | Thorsten Glaser 氏 2008-07-05 | B15。ソフトウェアに限らない "work" を対象に書かれたと提出文が述べたライセンスが承認された。読んだ範囲では、この点への反対は無い。data files を明記したライセンスの承認 2 件（`review-outcomes.md` §1.119）に並ぶ。**逆側**: MirOS は BSD 型の短い許諾で、ACD の §1.2 のようにソフトウェアでないものを列挙してはいない。2023 年の理事会の判断（B15）は 15 年後である |
| *"Anything multiply licensed, where at least one license is OSI-compliant, is obviously open source."* | John Cowan 氏 2008-09-07（同じ報告の RTEMS についての返信、`license-discuss`） | B4。Cowan 氏が述べたのは受領者が選ぶ二重許諾（どれか 1 つ）で、§2.4 は足場を重ねて働かせる（全部が同時に）ので、この言葉はそのままでは当たらない。ACD でも同じ結論（§4 が単独で OSD に適合すれば、§3 と §5 が並んでもオープンでなくならない）になるのは、§10.1 によってどの足場も You に条件を課さず、重ねても自由が減らないからである（2026-11-09、portfolio-aa の指摘で支えの主語を Cowan 氏から §10.1 へ移した）。**逆側**: 足場の一方が条件を持つ組には、この読みは当たらない。Cowan 氏の発言は個人のものである |

**読み。** #302 は MirOS を「OSD に適合しても承認しない」の系譜に入れて引いていたが、MirOS は承認された。7 月の反対の記録と、9 月の勧告と、承認日は、別のスレッドと別の文書に分かれていた。議論の記録に帰結は無い（`reviewer-positions.md` §1.142 と同じ教訓）。2008 年の委員会は、差の小ささも、提出者が既存のライセンスを断ったことも、利用の少なさも理由にせず、OSD への適合で承認を勧め、推奨はしなかった。ACD の提出が狙えるのは、少なくともこの形である。

**この節が establish しないこと。** 2008 年の委員会の運用で、2025 年の理事会の文（B2 の「留め置き」）より 17 年前である。議事録は要約する道具で読んだもので、逐語の照合をしていない。7 月から 9 月の間に勧告が変わった理由は記録に見つからない。MirOS は BSD 型の短い許諾で、ACD の長さ（B3）や特許の許諾（B7）は問われていない。

## 1.168 委員長は「OSD に適合するものは全部承認」がリストの声だとして 3 つの基準の撤回を求め、理事に退けられた —— 2005-09 の委員会報告と理事会の対応（2026-11-09）

`rounds/2005-09-license-discuss-committee-report-three-criteria-observed.txt`（9 通）。同じ日の理事会の議事録の側は `board-decisions.md` の 8.7 節が引いている。ここに置くのは、リストの側の記録である。

**経過。** 理事会は 2005 年 3 月に、新しいライセンスに 3 つの基準（readable・reusable・unique）を足した。委員長の Russell Nelson 氏は 2005-09-08 の報告で、OVPL にこの基準を当てようとして支持が無かったと書き、*"The license-discuss membership has spoken loudly and clearly that we should approve all licenses that comply with the OSD."*・*"Thus, we should withdraw those criteria and if we're serious about them, set about modifying the Open Source Definition."* と理事会に求めた。同じ日に理事の Eric S. Raymond 氏が *"The license-discuss membership doesn't make policy. The Board does."*・*"Those criteria were approved after due deliberation by the Board for good strategic reasons."* と返し、Mark Radcliffe 氏も *"the OSI board must make these decisions. We have done so and should follow the decision until we decide that it is incorrect."* と同意した。2005-09-12 の改訂版の報告は、撤回の提案を消して *"The three criteria (readable, reusable and unique) that the board passed and published in March got accidentally deleted in August."*・*"Most license-discuss members seem to believe that that place is in the OSD. There is not a consensus on this, though."* と書いた。

| 発言・決定 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| ACE License について *"The ACE License is a hard case because it's duplicative, not very readable and not reusable."*、決定は *"Status: deferred by the OSI board 9/12 to ask"* 再許諾できるか。OVPL は *"Recommend: deferral if you want to wait to see what Simon and Alex's negotiations produce in the way of changes to the CDDL."* のとおり保留（*"We voted to defer approval with a note"*） | Russell Nelson 氏（委員長）による理事会の対応の報告 2005-09-12、2005-09-13 | B10・B2。3 つの基準を最初に当てた日、重複を指摘された 2 本は却下ではなく保留になった。`board-decisions.md` の 8.7 節は「20 年かけて、追加テストは承認しないまま置く根拠として形を得た」と書いたが、その形は最初の適用の日から在った。**逆側**: 同じ日に Open-Realty License は *"Comments: Not a reusable license."* と書かれ、*"Recommend: rejection because of a lack of clarity of which license"* で却下された。却下の形式上の理由は、どちらの版を承認するかが不明なことである |
| *"They stepped all over my notion that readability extended across multiple licenses. You were right, I was wrong."* | Russell Nelson 氏 2005-09-13 | B3・B13。委員長は *"readable in context with other licenses; that is, if you make a derivative work from another license, you minimize the changes."*（2005-09-09）と読み、提出者は本文そのものの読みやすさと読んだ。理事会は後者を採った。ACD の読みやすさは、既存のライセンスとの差の小ささではなく、本文そのもので量られる。本文に残した理由の文は、解釈の材料として効果を運ぶものに限っている（例: §8.4 の "This is a grant in its own right and not a clarification" は狭く読む解釈への指示）。純粋な動機の文は 1.4 草案で外した（−135 語・#295）。擁護できるのは「残した理由の文は効果を運ぶ」までで、読みやすさを上げるとまでは言えない（portfolio-aa の 2026-11-10 の読み）。**逆側**: 本文そのもので量るなら、4,896 語（B3）はそのまま不利に働く |
| reusable について *"Can't name individual parties. Have to use generic terms like"* Licensor | Russell Nelson 氏 2005-09-14 | ACD は当事者を "Dedicator" と "You" で書き、1.0 は個人を名指さない。1.4 草案の §16.5 も "the Steward" を一般的に定める。2026-11-10 に portfolio-aa が 1.4 草案の本文で個人・会社・商標の名を語で探し、当たったのは法令の名（§1.10）、識別子の慣行の名（SPDX）、ライセンス自身の名前の 3 種だけだった。**逆側**: これは委員長の説明で、理事会の決定文ではない。記述子（machine.json）の steward 欄と、確定版の冒頭の作業記録は個人を名指す。記述子は本文ではないので、この基準の外である |
| *"Since it's no longer about conformance to a fairly objective specification, you really should stop referring to it as a"* certification mark | Brian Behlendorf 氏 2005-09-09 | B10。基準がウェブサイトに無かったことへの指摘。書かれていない基準の問題（`board-decisions.md` の 8.8 節にある 2013 年、2025 年の理事会の「process ページで伝える」）は 20 年前から在る。**逆側**: 個人の発言で、理事会は同じ月に基準を元の場所へ戻すとした |
| *"The license-discuss membership doesn't make policy. The Board does."* | Eric S. Raymond 氏（理事）2005-09-08 | B14 と discuss の位置。リストの多数の意見は理事会の方針を拘束しない。ACD が discuss で得た反応（あるいは沈黙）も、それだけで帰結を決めない。**有利な面**: 委員長自身がリストの多数を「OSD に適合するものは全部承認」と読んでおり、2025-07-18 の理事会の *"a license should be rejected only if it violates the OSD"*（`board-decisions.md` §2）は、却下についてはその読みに追いついている |

**読み。** 2005 年 9 月の 1 週間に、20 年後の論点が全部出ている。リストの多数は OSD への適合だけで足りると言い、理事会は方針は理事会が決めると言い、実際の審査では、重複を指摘されたライセンスを却下せずに保留した。ACD にとって大事なのは 3 つ目である。保留は 2025 年に始まった新しい運用ではない。重複の指摘に対する、最初からの扱い方である。

**この節が establish しないこと。** 2005 年の委員会と理事会の運用で、後の委員会がこの基準をどう扱ったかは別の節（`board-decisions.md` の 8.7 節・8.8 節）による。reusable と readable の中身は委員長の説明で、理事会の決定文として逐語で残っているのは議事録の側だけである。OVPL のその後の帰結は、この節では追っていない。

## 1.169 2 つの短い枝 —— 委員会の合意と理事会、1 つの道具で覆う需要、データベース権、提出者の名前（2009-01、2012-02）（2026-11-10）

`rounds/2009-to-2012-license-review-cc0-process-and-tgppl-branches-observed.txt`（4 通）と、委員長の通を含む `rounds/2012-01-to-04-license-review-cc0-cited-observed-2of2.txt`。どちらも rounds に 1 通だけ置かれていて読了に数えていなかった枝で、2026-11-10 に全部読んだ（`READ-THREADS.txt` を読了の単一の一覧にする切り替えの判定の途中）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Ideally, it rubber-stamps the consensus of this committee. If there are deep divisions here, the Board is unlikely to approve the license."* | Karl Fogel 氏（委員長）2012-02-22、CC0 の審査の手続きを問われて | B14・B2。帰結を左右するのは `license-review` での合意で、深い対立が残れば承認されにくい。ACD は discuss でまだ反応を得ていないので、review で対立が出たときに解けるかが帰結を決める。**逆側**: 同じ通で、同氏は CC0 の価値を *"It's not that CC0 is a software license already applied to lots of programs"* と、利用の多さではなく公有化への問いに答える道具として述べた（B2 の読みには有利） |
| *"There are often not sharp divisions between software, code snippets and scripts, documentation, data files, figures, etc in scientific work"*、続けて *"Currently recognized OSI licenses do not appear applicable for these heterogeneous"* 成果物 | Carl Boettiger 氏 2012-02-22 | B15。ソフトウェアとデータと文書を 1 つの道具で覆う需要を、OSI の承認の理由として述べた利用者の声。ACD の §1.2 の列挙は同じ需要に当たる。**逆側**: CC0 は承認されずに取り下げられた（`review-precedents.md` §1.138）。この需要は承認の帰結を変えなかった |
| *"Most free software, open source and free culture licenses do not consider database rights."* | Kuno Woudt 氏 2012-02-24 | B9。CC0 の価値の 1 つとして EU のデータベース権を扱うことを挙げた。ACD の §7 は同じ穴を受け持つ。**逆側**: 個人の発言で、CC0 の帰結（特許の除外による取り下げ）には効かなかった |
| *"One of the filters for frivolity is whether someone submits the license using a pseudonym, or their real name."*、これに Perens 氏が *"The board has total freedom to reject the license, and they should."* と返し、提出者ではなく提出物を見るべきだと述べた | Russ Nelson 氏 2009-01-24、Bruce Perens 氏 2009-01-24 | B14。提出者の名前が審査の扱いに使われた記録。ACD はオーナーが本名で出し、起草の経緯（AI が大半を書いた）も開示している。**逆側**: 審査する人が提出物でなく提出者を見ることがある、という記録でもある。B14 の moderator の宣言（AI が大半を書いた投稿を拒否する）は、その現在の形である |

**この節が establish しないこと。** どれも個人の発言で、OSI の決定ではない。Fogel 氏の「理事会は委員会の合意を追認する」は 2012 年の運用の説明である。

## 1.170 3 つの基準の元の文言 —— 立証の責任は提出者にある、と書かれていた（2005-03）（2026-11-10）

`rounds/2005-03-license-discuss-three-proposed-osd-terms-observed.txt`（11 通・スレッドは全 76 通）。§1.168 の 2005 年 9 月の報告が *"passed and published in March"* と書いた基準の、元の提案である。委員長の Russell Nelson 氏は 2005-03-02 に、OSD に 3 つの条項を足すと提案した。リストの多くは「OSD ではなく承認の手続きに置くべき」と答え、理事会は OSD を変えずに、承認の基準として通した（§1.168）。

| 提案の文言・発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| 11（non-duplicative）: *"That is, it is up to the submitter to demonstrate that the license solves a problem not sufficiently addressed by an existing certified license."* | Russell Nelson 氏（委員長）2005-03-02 | B10。立証の責任は提出者にある。ACD の提出文が先に差を示すのは、この形に合う（register の B10 の行は、承認済み 141 本で達成できない効果を条文で示した）。**逆側**: 同じ委員長は *"They're judgement calls."*・*"The first term alone gives us the discretion to say"* とも書いた（2005-03-03）。示しても、足りるかは審査する側の判断である |
| 12（clearly written）: *"OSI may deny certification to licenses which, though technically correct and OSD-compliant, are so obscure and complicated that an intelligent layperson cannot be assured of knowing his or her rights and liabilities after reading it."*・*"The burden of engineering this clarity falls on the submitter."* | 同 | B3・B13。基準は語数ではなく、読んだ人が自分の権利と責任を知れるかである。ACD は §10.1 で条件が無いことを 1 文で述べ、§16.1 の通知の書式が要点を数行で述べる。**逆側**: 4,896 語を読み通さないと「何も課されない」を確かめられない、という反論は残る。Alex Bligh 氏は *"It is rather easier to right a license which is entirely permissive (or for that matter entirely restrictive) than one which says some things are allowed under some conditions, but not under others."*（2005-03-07）と書いた。条件の無いライセンスの長さは、条件の複雑さで説明できない |
| *"judge-friendliness trumps programmer-friendliness"* | John Cowan 氏 2005-03-02 | B3 の逆側（有利）。短さより、裁判所で読まれたときの確かさを優先するという立場。ACD の長さの多くは、狭く読まれる読みを先に閉じる文である。**逆側**: 個人の発言で、12 の文言（素人が読める）とは向きが違う |
| *"It's not even 100% clear that dedications to the public domain are actually effective."* | John Cowan 氏 2005-03-02 | B4・B5。公有化の宣言が効くかに 2005 年から疑いがあった。ACD が §3 の放棄に §4 の許諾を重ねる理由の 1 つに当たる。**逆側**: 同じ疑いは、公有化を中心に置くライセンスそのものへの疑いにも使える |
| 13（reusable）: *"As the sole exception, the license may name its owner and steward."* | Russell Nelson 氏 2005-03-02 | 本文が名指してよいのは owner と steward だけ。ACD の本文は個人を名指さない（§1.168）。この基準は満たす |
| *"Certification should not be so subjective - it will only lead to long, drawn out arguments over whether something is detrimental or not, or duplicative or not, and make it difficult to defend a decision as more than a value judgement."* | Brian Behlendorf 氏 2005-03-03 | B10 の有利な面。重複の判定が主観に寄ることへの反対。同じ日に David A. Wheeler 氏は *"there's a rough working consensus that the OSI should continue to accept OSS licenses that meet the current OSD, and not change the current OSD."* と要約し、推奨の小さな一覧を別に作る案を挙げた。これが後の「承認して、目立つ一覧には載せない」（§1.167、#315）の元の形である。**逆側**: 理事会はそれでも基準を通した（§1.168） |
| *"This seems like an administrative detail, not a principle of the open source movement."*・*"I'd prefer to redefine OSI Certification to add these constraints, rather than burden the OSD per se with them."* | Joel West 氏 2005-03-02、Ernest Prabhakar 氏 2005-03-02 | 3 つの基準は OSD の外に置かれた。2025 年の理事会が却下を OSD 違反に限った文（`board-decisions.md` §2）と、この置き方は合う。**逆側**: OSD の外に置かれた基準は、却下ではなく留め置きの根拠として働き続けている（§1.168） |

**読み。** 3 つの基準は、最初から「提出者が立証する」形で書かれていた。ACD の提出文が差と読みやすさの根拠を先に出すのは、この形への答えになる。同時に、リストの大勢は 2005 年に、OSD に適合すれば承認し、推奨は別の一覧で扱う、と述べていた。ACD が狙える帰結（承認・推奨なし）は、この大勢の形でもある。

**この節が establish しないこと。** 提案の文言は委員長の案で、理事会が通した文言そのものではない（理事会の側は `board-decisions.md` の 8.7 節）。読みやすさの基準に語数の線は書かれていない。

## 1.171 2007 年 7 月の委員会報告とその枝 —— ハードウェアの範囲、承認して効果を見る、後継の版の審査、誰にでも同じ手続き、擁護できる提出者（2007-07〜08）（2026-11-11）

`rounds/2007-07-to-08-license-discuss-committee-report-and-approval-process-observed.txt`（6 通）。報告のスレッド（63 通の大半は GPLv3 と LGPLv3 の互換性の議論）と、手続きをめぐる枝 "what *is* the approval process?"（36 通）を読んだ。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| Open Source Hardware License について *"No consensus on license-discuss that OSI should be in the business of Open Source Hardware."*・*"Is this a direction that OSI should go in? And, even if we do, is a license particular to hardware needed?"* | Russ Nelson 氏（委員長）2007-07-23 | B15。ソフトウェアでないものを OSI が扱うかが、2007 年に問いとして出た。**2026-11-11 訂正**: 旧文は「2007 年から問いのままだった」と書いたが、理事会は 2 か月後の 2007-09-06 に *"Status: The board encourages more discussion, as Open Source Hardware falls within the remit of the Open Source Initiative."* と答えていた（§1.173）。**逆側（有利）**: 委員会は 2021 年に CERN-OHL について *"written such that they can be used for software"* という基準を述べて承認に進んだ（register の B15・`board-decisions.md` §2e）。ACD はソフトウェアに使える形で書かれている |
| CPAL について *"My personal recommendation (as a board member, not the chair) is to approve the license and see if it achieves the Open Source effect."*・*"If such a licensed software does not achieve the Open Source effect, it will put the issue to rest."* | 同 | B2・B10。新しい要件（帰属表示）を持つライセンスを、使われ方で確かめるために承認する、という立場。CPAL は承認された。**逆側**: 委員長としてではなく個人の勧告で、CPAL には Socialtext という提出元の組織があった。ACD の新しさは要件ではなく許諾の範囲で、「効果を見る」の対象が違う |
| *"does not mean that it should be given an automatic approval."*・*"In fact, the GPLv3 is quite different from GPLv2 and deserves a standard review."* | Mark Radcliffe 氏（OSI の General Counsel）2007-07-30 | 版の扱い。承認は版から版へ受け継がれない。ACD はどの版も承認されていないので、どの版を出しても通常の審査になる。出す版を申請の日の最新版にする計画（`OSI-APPROVAL-PLAN.md` §4）は、この扱いと食い違わない。**逆側**: Chuck Swiger 氏は同じ枝で、承認済みライセンスの新しい版には詳しい法的分析が *"has generally not been needed."* と書いた。ACD にはその近道が無い |
| *"No, the problem there is that we require everyone to follow the process, even the best of friends. If we didn't, we would (very reasonably) be accused of cronyism."* | Russ Nelson 氏 2007-08-03 | B12。手続きは誰にでも同じに当てる、という委員長の説明（#317 の「著名さへの偏り」の逆側）。**逆側**: 手続きが同じでも、判断の重みは同じとは限らない（#317） |
| *"You need to find someone who is capable of doing so, as you will not be able to champion the licence through the approvals process unless you understand it inside out."*・*"There is also a preference that the person submitting be able to change it in response to feedback"* | David Woolley 氏 2007-07-31 | B14・B1。審査を通すには、提出者がライセンスを隅々まで理解して擁護できる必要がある。ACD は AI が起草し、提出と返信はオーナーが自分の言葉で行う（B14）。#318 として記録した。**有利な面**: 後半の「指摘に応じて変えられる」は ACD の steward が満たす（1.1〜1.4 の改訂） |
| *"the need for a legal analysis to be included with a submitted licence assumes that such analysis is new and not previously available to license discuss."* | Rishab Aiyer Ghosh 氏（理事）2007-08-01 | B1。2007 年には法的分析が提出の要件で、理事はその趣旨を「新しい分析を出すこと」と読んだ。この要件は同じ年の 12 月に外れた（`review-rules.md` §1.141）。ACD の提出文は分析を求められないが、理由と逆側の記録はこの趣旨に近い |

**この節が establish しないこと。** どれも 2007 年の個人の発言か委員長の報告で、理事会の決定文ではない。CPAL の承認の理由は、この報告の勧告からは確かめていない。

## 1.172 2009 年 9 月の委員会報告 —— 答えられなかった問い、足りない議論、採用者を待つ、擁護する弁護士（2009-09〜11）（2026-11-11）

`rounds/2009-09-to-11-license-review-committee-report-and-falcon-observed.txt`（6 通）。報告は 5 本すべてに承認を勧めなかった。理由は、反対の多数（MXM）、二重許諾で足りる（Signatured-GPL）、問いに答えが無かった（36 Open Software License）、既存の BSD で足りる（Azure）、議論の不足（Falcon）である。スレッドの後半（2009-11）は Falcon の審査の続きになった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| 36 Open Software License について *"Comments: Bruce had questions, which didn't get answered."*、勧告は *"Recommend: no approval"* | Russ Nelson 氏（委員長）2009-09-01 | B14。審査で出た問いに答えが無いことが、そのまま不承認の勧告の理由になった。#318 の「オーナーが自分の言葉で答えられるか」は、記録の上で帰結に直結する。**逆側**: 答えれば足りるという記録ではない |
| Falcon について *"Recommend: discussion has been insufficient to justify approval at this time."* | 同 | B14・B2。議論の量の不足が、勧告を保留にする理由として書かれた。ACD の 1.0 は discuss で返信を得ていない（AS-OF）。review で議論が起きなければ、同じ形になりうる。**逆側**: Falcon には GPL に足した帰属表示の要件があり、OSD への適合の問いが残っていた。ACD は条件を持たない |
| *"I believe it is wiser to wait until the need is made clear by having many adopters of this language."*・*"Yet Another License needs to be understood in its totality."* | Russ Nelson 氏 2009-09-02 | B2。必要が採用者で示されるまで待つ、という委員長の立場（#161 の 2020 年の Fontana 氏、#312 の 2014 年の Berkus 氏と同じ向きで、さらに古い）。**逆側**: 同じ委員長は前年に、採用の少ない MirOS に承認を勧めた（§1.167）。採用を待つかは、差の大きさで決まる判断に見える |
| *"I submit that for OSI to approve a license, there should be an attorney willing to stand up for it and either explain why its terms or necessary or repair them."* | Bruce Perens 氏 2009-11-16 | B1。#309（同氏 2019 年）の 10 年前に、同じ要件が述べられていた。#309 に足した。**逆側**: Falcon の提出者は、3 人の弁護士が書いて署名した分析を添えていたと答えた（*"The license is presented together with a well-respected attorney relation."*）。それでも同氏の結論は *"Not convinced it's necessary or worth the cost in license proliferation, as existing licenses perform a very similar service."* で、弁護士の分析は帰結を決めなかった（Tidepool・§1.166、UPL・`gap-measurements.md` §1.154 に続く 3 件目） |
| *"I would tend to argue the other way around: open source defines a set of freedoms to which business models must adapt."* | Michael Tiemann 氏 2009-09-02（`opensource.org` の宛先から） | 提出者が「事業の形に必要」と述べたことへの返答。ACD の提出は事業の必要を理由にしない（#161 の逆側）。**逆側**: ACD の提出の理由（ポートフォリオの実験・AI による起草）は、別の形で審査の入力になりうる（#161・B14） |

**2026-11-11 追記（Falcon の最終の勧告）**: 2009 年 12 月分の委員会報告（2009-11-27）は、Falcon について *"Clearly OSD-compatible but"* と同じ説明を繰り返したうえで、勧告を *"Recommend: Not different enough from the LGPL to warrant approval."* とした（`rounds/2004-to-2009-license-lists-ecl-and-committee-report-december-2009-observed.txt`）。9 月の「議論が足りない」は、OSD に適合すると認めたうえで「差が足りない」へ移った。#302 の系譜（OSD に適合しても承認しない）の 2009 年の例である。

**この節が establish しないこと。** 委員長の勧告と個人の発言で、理事会の決定文ではない。5 本の帰結（理事会が勧告どおり決めたか）は、この節では議事録に当てていない。Tiemann 氏の役職は、この通の署名からは確かめていない（宛先が `opensource.org` であることだけを書いた）。

## 1.173 理事会は 2007 年に、オープンソースハードウェアを OSI の範囲に入るとした —— 2007 年 8 月の委員会報告と理事会の対応（2026-11-11）

`rounds/2007-09-license-discuss-committee-report-august-and-board-remit-observed.txt`（4 通）。母数の動きで読まずに外れていた件名を、2026-11-11 に読んだ。§1.171 の 7 月の報告の続きである。

| 発言・決定 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| 委員会: *"Recommend: Discussion has stalled. The board needs to direct license discuss -- is this a direction the organization should move in?"*、理事会: *"Status: The board encourages more discussion, as Open Source Hardware falls within the remit of the Open Source Initiative."* | Russ Nelson 氏（委員長）2007-09-04、理事会の対応の報告 2007-09-06 | B15 の有利な面。ソフトウェアでないもの（ハードウェア）が OSI の範囲に入る、と理事会が述べた記録。ACD の §1.2 がソフトウェアでないものを含むこと自体は、2007 年の理事会の答えの内にある。**逆側**: 「範囲に入る」は議論を促す答えで、承認ではない。2023 年に理事会はソフトウェアでないものを主題にした審査を不承認とし（register の B15）、2021 年の委員会は「ソフトウェアに使える形で書かれているか」を基準にした（`board-decisions.md` §2e）。範囲は 2007 年より後に狭く引き直されている |
| *"I think one thing that would be helpful is for the board to consider the current open source licenses and to evaluate which ones would be usable for hardware projects. GPL, MIT, BSD all seem OK to me for hardware."* | Jamey Hicks 氏（提出者）2007-09-13 | B10 の逆側。新しい分野でも、まず既存のライセンスで足りるかを見る、という提出者自身の結論（提出者のプロジェクトは MIT を選んだ）。ACD の「AI の成果物には既存のもので足りない」という主張は、同じ問いに条文で答える必要がある（register の B10・#316） |
| *"Second was the growing realization within the organization that there were too many licenses with too few and too minor differences, and too many licenses granted simply because it was as easy as asking."*・*"Instead, we've imposed requirements which reduce our workload in analyzing licenses."* | Russ Nelson 氏 2007-09-09 | B10・B3。承認を難しくした理由は、差の小さいライセンスの多さと、審査の手間だった。ACD の長さ（B3）は審査の手間を増やす向きにある。**有利な面**: 同じ通は、お金を取る案を退けた理由に *"First, because some of the most interesting licenses were going to come from people like you without a monetary incentive for getting the license approved."* を挙げた。個人の提出は、承認の手続きが想定した提出者の内にある |
| GPLv3 と LGPLv3 の承認の告知: *"Due to the dramatic differences between and viable communities around both the GPLv3 family and the GPLv2 family of licenses, we will not be marking GPLv2 and LGPLv2 as redundant"* | 理事会の対応の報告 2007-09-06 | 版の扱い（§1.171 の Radcliffe 氏と同じ月）。後継の版が承認されても、前の版は使う共同体が在る限り冗長とされない。ACD はどの版も承認されていないので、当たるのは「前の版をどう扱うか」の先例としてだけである |

**2026-11-11 追記（食い違う記録）**: 1 年後の 2008-11-04、Bruce Perens 氏は SIL Open Font License の審査で *"OSI refused to consider the Open Hardware License because they felt their task should be limited to software."* と書いた（§1.175）。理事会が 2007-09 に「範囲に入る」と答えたことと、その後ハードウェアのライセンスを扱わなかったことの両方が、記録に在る。どちらの文が当時の運用を表していたかは、議事録に当てていない。

**この節が establish しないこと。** 理事会の対応は委員長が委員会へ返した報告の文で、議事録の文ではない。オープンソースハードウェアのライセンスが当時承認されたかは、この節では追っていない（Perens 氏の 2008 年の記述は「扱わなかった」と述べる）。

## 1.174 多くの大学が使うと表明した提出も、使用を制限する条件で一度止まった —— Educational Community License（2004）（2026-11-11）

`rounds/2004-to-2009-license-lists-ecl-and-committee-report-december-2009-observed.txt`（ECL の 4 通）。Sakai Project と Open Source Portfolio Initiative の役員が 2004-06-07 に出した。提出文は、複数の大学と企業が使うことに合意したと列挙し、*"Other universities and projects have indicated their interest in using the license if it receives OSI certification."* と書いた。2004-08-30 に委員長の Russell Nelson 氏は、使用への制限を理由に *"So, no go."* と返した。OSI の一覧の API（`opensource.org_api_licenses.json`・2026-10-27 取得）は ECL-1.0 と ECL-2.0 の承認日をどちらも 20070606 とし、2.0 の提出を 2007-05 とする。2004 年の提出から承認まで 3 年かかった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Other universities and projects have indicated their interest in using the license if it receives OSI certification."* | Bradley C. Wheeler 氏（提出者）2004-06-07 | B2。承認されたら使うという表明を、提出文に並べた例（2025 年の委員会が留め置きを解く条件として挙げた「使う、または関心を表明する」と同じ形・AS-OF）。ACD にはこの表明が無い（窓口は `.github/ISSUE_TEMPLATE/acd-use.yml`・AI は投稿しない）。**逆側**: 表明があっても、2004 年の提出は止まった。表明は承認の十分条件ではない |
| *"We don't approve licenses that put restrictions on use. Copyright law doesn't allow you to restrict the use to which someone puts a copy that they have lawfully received. Only a contract can do that."* | Russell Nelson 氏（委員長）2004-08-30 | 有利な面。使用を制限する条件や、同意を求める契約の形が止められた。ACD は使用に条件を置かず（§10.1）、受け入れの行為を要らないとする（§2.3）。**逆側**: これは ECL の条件への判断で、ACD のような献呈を論じたものではない |
| *"So I think that a "permission to use" under copyright law is necessary in EU member states."* | Arnoud Engelfriet 氏 2004-08-30 | ACD の §4.2 が *"use"* を許諾の列挙の最初に置く理由の支え。EU ではプログラムを動かすことが複製に当たり、使用の許諾が要る、という読み。**逆側**: 個人の発言で、プログラムについての指令の話である。データや文書の Work には別の問いがある |
| *"I have to ask: Did you look at the original Apache license?"* | Ernest Prabhakar 氏 2004-06-07 | B10。新しいライセンスに審査者がまず問うのは、既存のもので足りないか、である。ACD への同じ問いの答えは、register の B10 の行と meta Q37 |

**この節が establish しないこと。** 2004 年の審査と 2007 年の承認の間に何が変わったかは、この節では読んでいない（2.0 の審査のスレッドは別に在る）。Engelfriet 氏の読みは個人のもので、法律家の判断としては数えない。

## 1.175 フォントのライセンスは、フォントをソフトウェアとして扱う読みのもとで承認された —— SIL Open Font License 1.1（2008-11〜2009-04）（2026-11-11）

`rounds/2008-11-license-review-sil-open-font-license-observed.txt`（5 通・スレッドは全 51 通）。SIL International の Nicolas Spalinger 氏が 2008-11-05 に出した。審査の大半は Perens 氏の文言への批判（文書に埋め込んだフォントを取り出せば制限を外せる、など）と、提出者の答えだった。理事会は 2009-04-01 に承認した（`board-decisions.md` の 8.9 節。同氏の懸念について *"we've never used likelihood of achieving the author's goals as a criteria for license approval"*）。OSI の一覧の API は、同じ日に IPA Font License の承認も記録している。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"OSI refused to consider the Open Hardware License because they felt their task should be limited to software."* | Bruce Perens 氏 2008-11-04 | B15 の不利な面。2008 年の時点で、OSI の範囲はソフトウェアに限る、という運用の記述。理事会が 2007-09 に述べた「範囲に入る」（§1.173）と食い違う |
| *"Outline fonts are only copyrightable at all (in the U.S., at least) because the hints they contain are in some sense software"*、提出者は Fonts are *"software and copyrightable as such in various jurisdictions."* | John Cowan 氏 2008-11-05、Nicolas Spalinger 氏 2008-11-06 | B15。フォントのライセンスは、フォントがソフトウェアだという読みのもとで審査され、承認された。2021 年の委員会の基準（ソフトウェアに使える形で書かれているか・`board-decisions.md` §2e）と同じ向きである。**ACD に当てると不利な面が強い**: ACD の §1.2 が含む data・audiovisual material は、ソフトウェアとして扱う読みが立ちにくい。OFL の承認は、ソフトウェアでないものを扱うライセンスの先例としては弱い。**有利な面**: ACD 自身はソフトウェアに使える形で書かれていて（source code、object code を列挙する）、この基準には当たる |
| *"This doesn't prevent OSI approval."* | Bruce Perens 氏 2008-11-08 | B10・B1。文言で目的を達せないという強い批判をした本人が、それは承認を妨げないと書いた。理事会の「作者の目的を達するかは承認の基準にしてこなかった」（8.9 節）と同じ向きである。**逆側**: 同氏は同じスレッドで、法的レビューを経ないライセンスを出すことに強く反対した（#309 の系譜） |
| *"Sometimes open source advocates believe they can revise copyright law by crafting special words in their licenses. That doesn't work."* | Lawrence Rosen 氏 2008-11-10 | ACD の §6.5・§9.2・§6.4 のような、法の状態について述べる文への警告。ACD はこれらの文で法を変えると称さず、権利が在るかを決めないと書く（§6.4 の *"is not decided here"* の向き）。**逆側**: 法の状態に触れる文を持つこと自体が、Rosen 氏の言う誤解を生む余地を持つ（条項別の想定問答の §6 の Perens 氏の問いと同じ根） |

**この節が establish しないこと。** OFL の承認の理由は議事録の 1 文と、この審査の発言から読んだもので、承認の告知の文は読んでいない。フォントがソフトウェアかは法域で違い、この節は決めない。Perens 氏の「OSI が拒んだ」という記述を、議事録で確かめていない。

## 1.176 権利は総称でなく名指す、正本の言語は 1 つにする —— CeCILL v2.1 の審査（2012）（2026-11-11）

`rounds/2012-04-to-05-license-review-cecill-2-1-observed.txt`（3 通・スレッドは全 19 通）。CEA・CNRS・Inria が 2012-02-27 に出した。2005 年の 2.0 は *"rejection because of unclear source distribution language"*（§1.168）で、2013 年に委員長が「増殖の報告に反するように感じられた」と述べている（`board-decisions.md` の 8.8 節）。2.1 の帰結は、この節の末尾の 2026-11-11 の追記が理事会の議事録で追った。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"If two of the three main items usually understood under the term are excluded, it would be better not to use the term at all and to be clear what you're talking about."*（"intellectual property" の語について） | Simon Phipps 氏 2012-04-06 | 有利な面。ACD は "intellectual property" の総称を使わず（1.0 と 1.4 草案に 0 回）、§1.5 の Covered Rights で権利を列挙し、特許は §8、商標は §11.1 で別に扱う。**逆側**: 列挙は長さ（B3）の一因で、"any right of similar effect" のような受け皿の語は、総称と同じ曖昧さを一部持つ |
| *"The court must use whatever mechanisms it normally uses to resolve ambiguity"*（2 つの言語の本文が共に正本のとき） | John Cowan 氏 2012-04-02 | 有利な面。CeCILL は仏語と英語の両方を正本とし、食い違いを裁判所に委ねる形だった。ACD は英語だけを正本とし、翻訳は便宜とする（1.0 の §15.8、1.4 草案の §15.4）。2 つの正本の食い違いという問いを持たない。**逆側**: 英語を母語としない法域の受領者には、正本が読めない負担が残る（`jurisdictions.md`） |
| *"Can we assume that your software license objectives are the same as those of W3C? If so, can you use the W3C licenses and not create a new one"* | Lawrence Rosen 氏 2012-05-19 | B10。ここでも最初の問いは既存のもので足りないか、だった（§1.174 の Prabhakar 氏と同じ型）。ACD の答えは register の B10 の行と meta Q37 |

**この節が establish しないこと。** 個人の発言で、CeCILL v2.1 の承認の理由ではない。

**2026-11-11 の追記 —— 2.1 の帰結: 提出から約 14 か月で承認された。** `rounds/2013-03-license-review-cecill-2-1-restart-observed.txt`（2 通）と、理事会の議事録の写し（opensource.org・2026-10-17 取得・`board-decisions.md` の 8.8 節が同じ 2013-05-01 の版を引く）。

| いつ | 記録 | ACD への当たり方 |
| :-- | :-- | :-- |
| 2010-11-03 | 理事会の議事録: 提出者が理事に状況を尋ね、以前の懸念を受け取って *"his legal team would look into it and prepare a new submission to the OSI."* | 提出の前に、以前の懸念を手にして作り直した。ACD の errata と版の扱いと同じ形 |
| 2012-04-04 | 理事会の議事録（委員長 Fogel 氏の報告）: *"CeCILL 2.1 in review; have responded to submitters with questions, am awaiting answers."* | 審査の中で、提出者への問いと答えの往復が続いた |
| 2013-03-05 | 新しい委員長の Villa 氏が list で再開: *"as far as I can see in my archives no one raised specific issues of non-compliance with the OSD."* と書き、*"I was aware of their submission when I took over the chair, and still dropped the ball."* と謝った。前の委員長の Fogel 氏も翌日に謝った | 不利な面（時間）。弁護士が起草し 3 つの公的機関が出した提出でも、委員会の手が回らず 1 年止まった。再開は提出者が改めて問い合わせたことによる。#257（NOSA 2.0 の 3 年半）と並ぶ記録。**有利な面**: 再開の基準は「OSD に適合しないという具体的な指摘が在るか」だった |
| 2013-03-06 | 理事会の議事録: 委員長が承認を提案し、別の理事が先に委員会の報告を出すよう求めた（*"first like to see the publication of a license committee report, as had been done in the past"*） | 承認の前に、list が正式に意見を言える報告を置く手順が求められた |
| 2013-03-06（list） | 委員長の報告（`rounds/2013-03-license-review-committee-reports-observed.txt`）: *"[After an absence of some time, the board has asked me to resurrect the formal license committee reports. This is the first one. Comments and suggestions on format, content, etc. are welcome.]"*、CeCILL 2.1 について *"Several clarifying questions were asked, indicating the license had been read, but no list members challenged the OSD compliance of the license itself."*、*"If anybody disagrees with my assessment of the list's comments or conclusions, please say so within the next week."* | 理事が求めた報告は、list に異議の期間（1 週間）を置く形で出た。推薦の理由は「読まれたうえで、OSD への適合に誰も異を唱えなかった」こと。いまの手順の「委員長の推薦を list に写して理事会へ」の前身である |
| 2013-03-28 | 次の報告: CeCILL 2.1 は *"Recommendation: Board should approve."*。同じ報告で、個人が起草した MOSL は OSD 9 への異議を理由に *"Recommendation: Not accept at this time."* | 同じ報告の中で、公的機関の提出は承認へ、個人の起草は「いまは受けない」へ分かれた。分けたのは起草者の属性ではなく、OSD 9 への具体的な異議が在ったかどうかである |
| 2013-05-01 | 理事会の議事録: *"It has been reviewed and discussed on the license-review mailing list and found to be compliant with the OSD."*、増殖の報告に反するように感じられたが成文の規則が無い（`board-decisions.md` の 8.8 節）。Phipps 氏は *"CeCILL was not duplicative when it was first introduced. It was the only license that was enforceable in French courts."* と述べ、*"Villa made a motion to approve the CeCILL 2.1 license. Phipps seconded. Motion passed by general consent."* | 有利な面。増殖の懸念が在っても、OSD への適合と、出たときに重複していなかったこと（特定の法廷で効くという固有の理由）で承認された。**逆側**: CeCILL の固有の理由は法域で、ACD の差（特許の側・B10）とは種類が違う。分類は決まらないまま承認された |

**同じ報告の別の提出 —— 個人の起草者への勧め。** MOSL の起草者に、Gervase Markham 氏は 2013-03-28 に *"Perhaps it would be wise to do license design using a) software which tracks changes, and b) on a site where you can also post your design goals? We seem to be re-inventing parts of the BSD Protection License and parts of the GPL here."* と書いた。ACD は git で変更を追い、設計の目的と理由を `docs/architecture/acd-license-rationale.md` と各版の CHANGELIST（`ACD-1.4-CHANGELIST.md` など）に置いている —— 勧められた形と合う有利な面である。**逆側**: 同じ文の後半（既存のライセンスの部分を作り直している）は、ACD の B10 の問いと同じ向きである。

**この追記が establish しないこと。** 議事録は要約の記録で、発言の逐語ではない。承認の理由は議事録に書かれたものに限り、ほかの理事の考えは分からない。CeCILL 2.1 が承認後にどれだけ使われたかは確かめていない。

## 1.177 「OSD に適合するものを全部か、良いものだけか」—— 委員長の問いと、理事が述べた 3 つの基準の使い方（2005-09）（2026-11-11）

`rounds/2005-09-license-discuss-license-proliferation-observed.txt`（5 通）。件名 "License Proliferation" の議論（2005-08〜09・2 か月で 106 通）は、増殖を扱う委員会ができた時期のもので、§1.168（同じ月の委員会報告）と §1.170（3 月の基準の提案）の間を埋める。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Does OSI certify all licenses that comply with the OSD?"* か *"Does OSI certify all good licenses that comply with the OSD?"*、*"In other words, do we take into account the interests of the community?"* | Russell Nelson 氏（委員長）2005-09-01 | B10 の根の問い。2005 年に委員長自身が答えを決めていなかった。2025 年の理事会は却下を OSD 違反に限ると述べた（`board-decisions.md` §2）が、留め置きでは後者（良いものだけ）の運用が続いている（§1.168） |
| *"As I've told you often before, my opinion has always been that OSI should approve licenses that comply with the OSD. Period."*・*"But don't keep moving the goal posts when licenses try to cross into the end zone."*・良さ・必要性・法的な適切さについて *"Those needn't be conditions for approval."* | Lawrence Rosen 氏 2005-09-01 | 有利な面。OSD への適合だけで承認し、必要性は教育で扱う、という立場（2017 年にも同氏は拒む理由を新しさの欠如と OSD 不適合に限ると述べた・`reviewer-positions.md` §1.156）。**逆側**: 個人の立場で、同じ月に理事会は基準を戻した |
| *"ii) They are supplemental to the OSD."*・*"iii) We expect license-discuss to apply them when doing evaluations. The Board will consider them when making final approve/reject decidions."*・*"iv) The rationale for these new criteria is simply that we need to avoid junk licenses. At a time when we're trying to cut down even on the number of non-junk licenses in use, we have to be more strict about what we allow in."* | Eric S. Raymond 氏（理事）2005-09-24 | B10・B3・B13 の不利な面。3 つの基準（readable・reusable・unique）は OSD の補足として、リストが評価に当て、理事会が最終判断で考慮する、と理事が述べた。「使われている良いライセンスの数さえ減らそうとしている時期に、入れるものには厳しくする」。ACD の長さ（B3）と差（B10）は、この基準に当たる |
| *"simply using "number of projects that use the license" as the criterion is not the best approach - it simply shows what's trendy. The test of a license is surely how many people are willing to participate in the project that's licensed under it, both as developers and as deployers."* | Simon Phipps 氏 2005-09-02（当時は Sun の所属） | B2。使っているプロジェクトの数を基準にすることへの反対（2018 年には OSI President として署名している・#274）。**逆側**: 同氏の代わりの試験（そのライセンスのプロジェクトに参加する人の数）でも、ACD は 1 リポジトリで、参加者はほぼ居ない |
| *"My understanding is that we cannot be arbitrary. We can change our reasons for approval over time, but not over parties asking for approval."* | Russell Nelson 氏 2005-09-04 | B12。理由は時とともに変えられるが、申請者ごとには変えられない（§1.171 の「仲間うちでも同じ手続き」と同じ向き）。**逆側**: 「時とともに変えられる」ので、2005 年の基準も 2025 年の運用も、提出の日の運用とは限らない |

**この節が establish しないこと。** 理事の Raymond 氏の文は理事会の方針の説明で、議事録の文ではない（議事録の側は `board-decisions.md` の 8.7 節）。Phipps 氏の役職は 2005 年のものとして書いた。

## 1.178 「OSD に適合するものを承認しない方針は、正式に定めたことがない」—— 2012 年の理事の理解と、それと食い違う記録（2026-11-11）

`rounds/2012-06-license-discuss-licensing-pages-proposal-observed.txt`（4 通）。理事の Luis Villa 氏が 2012-06 に、承認済みライセンスのページの見せ方を変える提案を出した。分類（「人気がある・広く使われている」の一覧）は変えない、という提案だった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I'm not sure I agree 100% with the substance of the second sentence, as (to the best of my knowledge) OSI has never formally laid out a policy or criteria by which something could be OSD-compliant but not approved and placed into at least"* どこかの分類に | Luis Villa 氏（理事）2012-06-09 | B10・B2 の有利な面。理事の理解では、OSD に適合するのに承認されず、どの分類にも置かれない、という方針は正式に定められていなかった。翌年の議事録で同氏は *"we have no written rules about non-proliferation"* と述べている（`board-decisions.md` の 8.8 節）。**逆側（記録と食い違う）**: 同氏は "to the best of my knowledge" と留保している。実際には、2005 年の Wonka（差が小さく承認しない）、2008-05 の *"Recommend: rejection for similarity"*、2009 年の Falcon の *"Not different enough from the LGPL to warrant approval."* が在る（#302・§1.172）。正式な方針が無くても、勧告の運用は在った。2025 年の理事会の留め置きは、その運用の現在の形である |
| *"3) The Board believes that it substantially duplicates an existing license."*（オープンソースだが承認されない理由として *"1) It has not been submitted for certification in proper form."*・*"2) The Board considers it a vanity license."* と並べた） | John Cowan 氏 2012-06-07 | Villa 氏の上の通が答えていた相手。リストの古参の理解では、重複は承認されない理由の 1 つだった。Villa 氏の「正式な方針は無い」と、この理解と、#302 の勧告の記録の 3 つが並ぶ。ACD に当たるのは 3 番目で、差は条文で示す（register の B10・meta Q37） |
| *"It is not perfect, but it is long-settled, and will not be revised until many months (more likely years) of work have been done."*（人気の一覧について） | Luis Villa 氏 2012-06-04 | 分類の一覧は、決めたあと長く手を入れられなかった（Phipps 氏 2020 の「保守されず古くなった」・meta Q37 と同じ観察）。ACD が分類を名乗らない理由の支え |
| *"As long as that list remains, I will object. It is inaccurate, incomplete, misleading, subject to cronyism and personal bias by members of the OSI board of directors, and does not reflect the actual importance or uses of those licenses."* | Lawrence Rosen 氏 2012-06-04 | B2。人気や使われ方の一覧を、承認や推奨の根拠にすることへの強い反対。**逆側**: 個人の発言で、一覧は残った |

**2026-11-12 の追記 —— 同じ年の 4 月、ライセンスのページを短い一覧へ導く案。** `rounds/2012-04-license-discuss-licenses-landing-page-observed.txt`（4 通・件名が "BSD, MIT" に変わった枝と合わせて全 45 通）。Karl Fogel 氏は *"Historically, we haven't tried to steer newcomers toward choosing the most popular / widely-recognized licenses, probably because we thought it more important to remain neutral among all OSI-approved licenses."* と書き、新しく来た人を短い一覧へ導くページを提案した。Luis Villa 氏は許容型の筆頭について *"Apache fills the same purpose[1] (permissive license) while being better drafted and properly handling patents."* と書いた —— **B10 の特許の側の有利な面**: 特許を正しく扱うことを、一覧の先頭に置く理由とした記録（`gap-measurements.md` §1.144 の Cowan 氏 2014 より 2 年早い）。Lawrence Rosen 氏は *"I would probably recommend to someone who doesn't really care about his copyright other than to give it away to use CC0 or the BSD license."* と書いた —— 献呈の型を勧める弁護士の文（有利な面）。同氏は同じ通で、OSI が利用者の事情を知らずに勧めることには反対した。John Cowan 氏は *"All that matters, finally, is an argument good enough to convince 7 out of 12 OSI board members; in practice, probably fewer."* と書いた。**逆側**: 一覧の先頭に置かれることと承認は別で、ACD が承認されても短い一覧に入るわけではない（§1.185・#322）。

**この節が establish しないこと。** Villa 氏の文は留保つきの個人の理解で、OSI の方針の文ではない。2012 年の運用の全体は、この節では数えていない。

## 1.179 審査の仕事は 4 つの問い —— OSD、独自で正当な条項、法的な健全さ、大きく持続するプロジェクト（OSET Public License・2015）（2026-11-11）

`rounds/2015-09-to-11-license-review-oset-public-license-observed.txt`（6 通）。Open Source Election Technology Foundation の依頼で Heather Meeker 氏が 2015-09-01 に出した、MPL 2.0 を元にした選挙の技術のためのライセンス。委員会は政府に有利な条項（§4）を MPL 2.0 の元の形へ戻すよう求め、本文から財団の名を外して再利用できる形にしたあと、2015-11-12 に *"The OSI has approved the OSET Foundation Public License version 2.1."* と告げた。2 か月半で、弁護士が起草し財団が出した提出である（同じ弁護士が起草した Tidepool は、提出者が自分で止めた・§1.166）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Our job is to decide: a) does the OSET license meet the letter and spirit of the OSD? b) does it contain unique and valid provisions, such that no existing license is sufficient? c) is it legally sound? d) is it going to be used by a significant and sustained project?"* | Josh Berkus 氏（委員会）2015-09-10 | B10・B1・B2 の不利な面。審査の仕事を 4 つの問いで述べた。ACD は (a) を満たすと主張でき、(b) は register の B10 が条文で示す。(c) は法的なレビューを受けていない（B1）。**(d) には答えられない** —— 本リポジトリ 1 件で、大きく持続するプロジェクトは無い。#312（同氏 2014「使う意思の無いライセンスには反対」）に足した。**逆側**: 個人の言い方で、委員会の規則の文ではない。同氏は翌日 *"It is NOT OUR BUSINESS to tell an OSS project that they should have a different license"* とも書いた |
| *"I don't think we've been consistently enforcing the 'recommend a proliferation category' requirement at the outset, but would you agree this license ought to be classified as 'special purpose'?"* | Richard Fontana 氏 2015-09-03 | 分類の扱い。提出者が分類を勧める手続きは一貫して当てられていなかった（meta Q37 の「分類は名乗らない」と同じ観察）。委員会の側から特別な目的の分類を示した |
| *"Given the concerns expressed here about the OSET Public License privileging one class of licensees, we ask that the OSET Foundation revise the OSET Public License to revert section 4 to the corresponding ancestral version of that section in MPL 2.0."* | Richard Fontana 氏（委員会として）2015-10-14 | 受領者の一部（政府）を有利にする条項は戻すよう求められた。ACD は受領者を区別しない（§1.4 の "You"、§10.1）。有利な面 |
| 提出者の名を本文から外す提案: *"That way, the text of the license will be "templatized" for use by others."* | Heather Meeker 氏 2015-11-04 | reusable の基準が 2015 年にも運用で当てられた例（§1.168・§1.170）。ACD の本文は個人も組織も名指さない（§1.168 の行） |

**読み。** OSET の審査は、弁護士の起草、財団の後ろ盾、具体的なプロジェクト（TrustTheVote）を持つ提出が、条項の修正と名の外しを経て 2 か月半で承認された例である。ACD が持たないのは (c) と (d) で、どちらも提出の前に記録の上で変えられない。

**この節が establish しないこと。** Berkus 氏の 4 つの問いは個人の言い方で、承認の理由として理事会が述べた文ではない。OSET の承認の議事録は読んでいない。

## 1.180 契約でないライセンスは、受領者に保証の権利を放棄させられるか —— 2002 年の委員長の懸念と反論（2026-11-11）

`rounds/2002-08-license-discuss-legal-soundness-observed.txt`（4 通・スレッドは全 88 通）。委員長の Russell Nelson 氏が 2002-08 に、理事会の決定（AFL の承認と、クリックラップを求めるライセンスの扱い）を報告して始めた議論。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"From what various legal scholars tell me, a non-contractual license (such as the GPL) cannot cause you to give up your warranty rights. Only a contract can do that."* | Russell Nelson 氏（委員長）2002-08-02 | §2.3・§13・§14 の不利な面。ACD は受け入れの行為を要らない献呈で（§2.3）、契約を作らない。この読みが立つ法域では、§13 の保証の否認と §14 の責任の制限は、受領者を縛らないかもしれない。#321 として記録した。費用を負うのは受領者ではなく Dedicator で、採用者を遠ざける向き（B2） |
| *"IMO it's not all that germane to warranty disclaimer, and I'm not buying the chain of extrapolation that leads from this case to the conclusion that click-wrap might be necessary."* | Bruce Perens 氏 2002-08-03 | 逆側。委員長が根拠にした判決は保証の否認には関係が薄い、という反論。GPL をはじめ、同意を求めない承認済みライセンスは、いまも保証を否認している |
| *"At the July OSI board meeting last week, we approved the Academic Free License (think MIT/BSD/X11/Apache with a patent grant)"* | Russell Nelson 氏 2002-08-02 | B10 の参考。寛容なライセンスに特許の許諾を足したものは 2002 年に承認されている（AFL は通知の条件を持つ）。register の B10 が測った差（明示の特許許諾 ∧ 無条件）は、この型に条件の無さを足したところにある |
| *"One of the benefits of the OSI Certified certification mark is that users of such certified software can be assured that the licenses are OSD compliant without having to read and understand the entire license."* | Lawrence E. Rosen 氏 2002-08-14 | B13 の逆側。承認の印は、利用者が本文を全部読まずに済むためのもの、という見方。ACD の長さ（B3）の費用の一部は、承認されれば利用者の側では小さくなる。**逆側**: 審査する側は全部を読む |

**2026-11-12 の追記 —— 同じ年の 10 月、click-wrap の議論（2002）。** `rounds/2002-10-license-discuss-click-wrap-observed.txt`（3 通・スレッドは全 11 通）。Rod Dixon 氏（署名に J.D., LL.M.）は、同意を形づくる手順はライセンスを出す側の利益だと書き、*"many on this list seem to have no aversion to the warranty disclaimer, which, if enforceable in a particular state, is not exactly user-friendly."* と続けた。同じスレッドの最後で同氏は *"If there were no clickwrap or if you lived in Russ' world, you might have a better argument challenging the license (browser-wrap) on the basis that there is no manifestation of mutual assent."* と書いた。**不利な面**: 同意を求めない形（ACD の §2.3）は、相互の同意の表示が無いことを理由に条項を争われる余地を残す —— #321 の向きを、法律家の肩書きを持つ人が述べた記録である。**逆側**: Nelson 氏は同じ日に *"I guess I just can't believe that so many sober people take click-wrap so seriously."* と click-wrap の効き目そのものを疑い、OSD は後に特定の受け入れの手順を求めることを退けた（OSD 10）。同意の手順を足すことは ACD の設計（§2.3）と OSD の両方に反する。

**この節が establish しないこと。** 2002 年の個人の発言と委員長の報告で、法律家の判断ではない（Nelson 氏は「法学者から聞いた」と書いている）。保証の否認が契約なしに効くかは法域の問いで、この節は決めない。
**2026-11-12 の追記 —— 同じ 10 月、委員長が OSD に「使用と改変を制限しない」を足そうとした（2002）。** "a proposed change to the OSD"（`license-discuss` 2002-10〜11・74 通・`rounds/2002-10-license-discuss-proposed-osd-change-use-and-click-wrap-observed.txt` に 11 通）。Russell Nelson 氏（委員長）は、次の木曜の理事会に 1 つの条を出すと書いた —— *"A license may not restrict use or modification of a lawfully obtained copy of a work."* 議論はすぐ、クリックラップ（受け入れの手順）と、契約が無くても免責が効くかへ移った。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I know that you need a contract to disclaim warranties, but I'm not sure that it's necessary to disclaim a warranty on a gift."*、*"At the end of the day, Larry, the community doesn't want to use software for which it has to contract to use."* | Russell Nelson 氏（委員長）2002-10-26 | 有利な向き。ACD は契約を作らない贈与の形（§2.3）で、委員長はその形の免責が効く余地を探していた。8 月の同氏の文（上の表の 1 行目）は「契約でなければ保証を放棄させられない」だったので、2 か月で「贈与なら要らないかもしれない」へ動いている。どちらも見通しで、法の判断ではない |
| *"if there's no contract, there cannot possibly be any restrictions."* | Nelson 氏 2002-10-30 | ACD は受領者に制限を課さない（§10.1）ので、契約が無いことで失う制限が無い。失いうるのは免責の効き方だけである（#321） |
| *"I will ALWAYS recommend to my clients that they use such notices for their software, and that they require their sublicensees to use such notices."*、*"the courts are clear about the importance of such notices for contract formation."* | Lawrence E. Rosen 氏 2002-10-26 | **不利な面。** list の弁護士が、受け入れの手順を契約の成立に要るものとして勧めた。ACD は受け入れを求めない（§2.3）。11 月にも同氏は *"we ought to use enforceable contracts when we license our software."* と書いた（#321 の追記） |
| *"I doubt that any lawyer would advise support of this change to the OSD, if it pertains to the clickwrap issue."*、*"Calling an open source license a gift is nice semantics, but I am unsure what else that description gets us..."* | Rod Dixon 氏（Rutgers の法学の客員助教授と署名）2002-10-26 | 不利な面。贈与と呼んでも、違反に対する救済は他のライセンスと同じだろう、という見通し。ACD は違反しうる条件を持たないので救済の問いは小さいが、免責の側の問いは残る |
| *"contracts involving mere use (as opposed to a copyright-holder right such as modification) are a Very Bad Thing."*、*"You could very well claim that you did not know the terms, because you had no notice of them."* | John Cowan 氏 2002-10-26・27 | 両方の面。使うだけのための契約は悪い、という ACD の §2.3 と同じ向きの文と、通知を受けなかった人は条件を知らなかったと言える、という #321 の側の文 |
| *"Unless there is a structure that under current law gives some confidence that the disclaimers and limitations in particular will be enforced, there is a real disincentive for many entities to make software available on an open source basis."*、*"may not be enforced by many courts in many cases."* | Karen Williams 氏 2002-10-30（sybase.com から、自社の提出について） | **不利な面で、#321 の 4 例目。** 提出した会社の側の人が（署名に肩書きは無く、*"In my opinion, the current legal reality"* と書いた文を法の見通しとして読む）、同意の明確な表示を求めない構造は多くの裁判所で執行されないかもしれず、免責が効く見込みが無ければ公開をためらう主体が多い、と書いた。ACD を採るかを決める組織の法務が同じ読みをすれば、採用を遠ざける（B2）。同氏は、承認済みの IBM Public License などが使用を受け入れの条件にしていることも挙げた。ACD はそれもしない |
| *"consent is for the product liability clauses in the licenses, not the copyright grants."* | Mahesh T Pai 氏 2002-11-01 | 不利な面。同意が要るのは許諾ではなく責任の条だ、という区別。ACD の許諾は同意を要らないが、§13 と §14 はこの区別の後ろ側に在る |
| *"Some of us would like to see people who give away software relieved of all liability by law.  The trick is to get this to be true in all possible jurisdictions"* | Cowan 氏 2002-11-02 | 法域の問い。ACD の §14 は「法が許す限り」の形で、法がそれを許すかは法域による（`jurisdictions.md`） |

**読み。** 2002 年 10 月の議論は、受け入れを求めない形の費用（#321）を、委員長と list の弁護士が正面から争った記録である。委員長は贈与の形を守る側、弁護士は契約を作る側に立った。ACD は前者の形をとり、費用は免責の効き方に出る。のちの OSD 10（技術の中立）の理由書はクリックラップを要件にすることを退けた（`submission-osd.md` の OSD 10 の行）が、それは受け入れの手順を求めてはならないという側の決定で、受け入れなしの免責が効くという決定ではない。

**この追記が establish しないこと。** Nelson 氏の案が理事会でどう扱われたかは、このスレッドには無い。いまの OSD に同じ文は無い（ドシエの OSD の写しに *"lawfully obtained copy"* は現れない）。Sybase のライセンスの審査そのもの（別のスレッド）は読んでいない。

**同じ追記の前段（2002-08）—— 許される制限を列挙する案。** 10 月の案の 2 か月前、委員長の Nelson 氏は "A new "use" clause in the OSD"（`license-discuss` 2002-08・12 通・`rounds/2002-08-license-discuss-osd-use-clause-observed.txt` に 4 通）で、許される制限だけを列挙する形の条を、OSD の 11 番目の条として出していた —— *"A license must not restrict the use or modification of the software in any way except the following: it may disclaim warranties, it may grant limited patent use rights, it may specify arbitration, it may suspend use rights if the user sues for patent infringement, and it may prohibit modifications which remove legal information."* 理由は *"There's nothing in the OSD that clearly prohibits restrictions on use."* だった。Lawrence Rosen 氏は列挙でなく一般の形（使用の権利を制限しない）を、Brian Behlendorf 氏は OSD を広げること自体への疑いを書いた。**ACD への当たり方**: ACD は列挙された 5 つの制限のどれも使用の制限として持たない（保証の否認 §13 は制限でなく否認、特許の許諾 §8 は終了しない・§8.2、仲裁も報復の終了も持たない）ので、この最も狭い案の下でも当たらない。**逆側**: 今の OSD に同じ条は無い。ACD に有利な基準が在ることを示すのではなく、最も厳しい案でも ACD が通ることを示すだけである。

## 1.181 承認は受け入れの床であって、下流の一覧ではない —— "why standard licenses"（2014）と Apache の第三者ライセンス方針（2015）（2026-11-11）

`rounds/2014-04-license-discuss-why-standard-licenses-observed.txt`（4 通・スレッドは全 25 通）と `rounds/2015-05-and-08-license-discuss-apache-third-party-policy-observed.txt`（7 通・2 本のスレッドは全 31 通と 11 通）。前者は Luis Villa 氏が 2014-04-27 に、標準的なライセンスを使う理由を説明する文が FAQ にもサイトにも無いとして、FAQ の下書きを示して始めた議論。後者は Lawrence Rosen 氏が、Apache Software Foundation（ASF）が第三者のライセンスを A・B・X に分けて受け入れる方針を、OSI に任せる形へ変えるよう提案した議論で、ASF の legal-discuss から cross-post された。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"OSI approval signifies to me that a license meets minimum standards of acceptability, minimum standards of conformance to FLOSS norms"* | Richard Fontana 氏 2014-04-28 | 有利な面。承認は受け入れられる最低の基準を満たすことの印で、推薦ではない、という読み。ACD が求めているのはこの床である。**逆側**: 同じ通で *"But only some OSI-approved licenses go further and inspire for me the kind of trust and confidence spoken of in Luis's draft FAQ entry."* と続け、承認されても使う側の信頼は別に要る、と書いた |
| *"The fact that it was approved by the OSI is very important but it does not transform the Attribution Assurance License into something that is "standard" in a common-sense sense."* | Richard Fontana 氏 2014-04-28 | B2 の不利な面。ACD は承認されても、既知の系列に属さない一本の承認済みライセンスになる。#322 に記録した |
| *"I'm not quarreling with OSI's attempt to get everyone to use approved licenses, but I have long challenged your attempts to steer people toward some subset of those licenses."* | Lawrence Rosen 氏 2014-04-28 | 有利な面。承認済みのものの一部へ人を寄せることへの異議。§1.177 の「全部か、良いものだけか」と同じ線で、承認の判断は OSD への適合で行う、という立場（§1.178 の Villa 氏 2012 と並ぶ）。**逆側**: 個人の発言で、FAQ の下書き自体は標準的なライセンスを使う理由を述べるものだった（FAQ に入ったかは確かめていない） |
| *"Same with "ALL other" OSI-approved licenses since each package would have to be reviewed as to whether it would be okay."* | Nigel H. Tzeng 氏（利用者の組織）2015-05-28 | B2 の不利な面。利用者の組織は、見慣れた組み合わせの外にある承認済みライセンスを、パッケージごとに審査する。承認は下流の審査を省かせない。#322 |
| *"OSI *might* be able to determine what we legally can do (though I doubt that), but they have not a clue (no disrespect) what our *policy* is as well as the background and rationale behind that policy."* | Jim Jagielski 氏 2015-05-26 | 下流の一覧は各組織の方針で決まる、という立場。Ross Gardler 氏も同日 *"The OSI is not qualified to make judgments on ASF cultural mission."* と書いた |
| *"Even though I am outside GC for OSI, I think that these issues are critical to ASF and should remain a decision made by ASF."* | Mark Radcliffe 氏 2015-05-27 | 同じ立場を、OSI の外部の general counsel と自ら書いた人が述べた。OSI の承認と、財団がどのライセンスを受け入れるかは別の決定である |
| *"It's hard to see why this Apache-specific discussion is being redirected to OSI's mailing list and I suggest we end the conversation unless there is a specific and well-defined question for us to answer."* | Simon Phipps 氏（opensource.org のアドレスから）2015-05-29 | OSI の側も、一つの財団の受け入れの方針を決める場ではない、とした |
| *"Enforcing compliance with licenses and copyright law requires legal review even for FOSS licenses that Apache lists in Category A."* | Lawrence Rosen 氏 2015-08-22 | 逆側。一覧に載っていても、遵守には法的な確認が要る、という見方。一覧は審査を消すのではなく、審査の入口を決めるものである |

**いまの ASF の一覧（2026-11-11 に WebFetch で読んだ要約・逐語ではない）。** `https://www.apache.org/legal/resolved.html` は、受け入れの基準を OSD への適合に置き（OSI の承認の語は使っていない）、Unlicense と 0BSD を Category A に挙げ、CC0 を public domain と同様に扱うものとして挙げる。一覧に無い場合の一般の規則は書いておらず、問いは Legal Affairs Committee（legal-discuss か JIRA）へ出す。**有利な面**: 献呈の型そのものは、少なくとも一つの大きな財団の一覧で既に受け入れられている。基準が OSD への適合なので、ACD の論じ方（OSD の逐条）はそのまま使える。**逆側**: ACD はどの一覧にも無く、載るかは各組織が決める。0BSD の作者は、CC0 や MIT-0 が企業の法務で押し返しを受けたと証言している（`ACD-OSI-BOTTLENECKS.md` の B6 の 2026-11-08 の注）。

**読み。** 承認が示すのは受け入れの床で、そこから使われるまでには各組織の一覧と審査がある。ACD の B2（採用者 1）は承認の前の問いで、この節が足すのは承認の後にも同じ費用が残ることである。承認の判断そのものには当たらない。

**この節が establish しないこと。** 2014 年と 2015 年の個人の発言で、OSI の規則の文ではない。Villa 氏の FAQ の下書きが公開されたか、Phipps 氏の 2015-05 の役職は確かめていない。ASF の現行の一覧は WebFetch の要約で読んだので、逐語の照合はしていない。ASF が ACD をどう扱うかは、この節は何も言わない。

## 1.182 理事会は何を却下するか —— 2007 年の分類の採択と "License Proliferation Dissatisfaction"（2026-11-11）

`rounds/2007-04-license-discuss-license-proliferation-dissatisfaction-observed.txt`（5 通・スレッドは全 22 通）。ライセンス増殖の委員会を共同で率いた Russ Nelson 氏が 2007-04-22 に、理事会が委員会の報告を承認し分類を支持したと告げ、分類で下位に置かれた AFL と OSL の作者 Lawrence Rosen 氏の異議に答えた議論。分類は承認の可否ではなく、承認済みのライセンスの並べ方である（分類が承認の category であることは `review-corpus.md` と `review-outcomes.md` が扱う）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"we do our best to reject licenses that (1) have obvious legal problems, and (2) do not have such an overwhelming community of use that the community itself becomes a legal force."* | Michael Tiemann 氏 2007-04-24（理事会の判断を "we" で述べた） | B1 と B2 が 1 つの文で働く形。却下されるのは、明らかな法的な問題を持ち、かつ使う共同体がそれを補うほど大きくないライセンスである。ACD は (2) を必ず満たす（採用者 1）ので、却下されるかは (1) だけで決まり、(1) を誰も法律家として確かめていない（B1）。#323 として記録した。**逆側**: 「明らかな」問題に限った文で、法的なレビューが無いことそのものを理由にしてはいない。2007 年の一人の発言で、規則の文ではない。翌年の MirOS は、共同体の大きさを問われず OSD への適合で承認へ勧められた（§1.167） |
| *"At one point it was proposed that we really should try to winnow the field to 3-4 licenses, tops--reciprocal, liberal, and one or two others. We did not take such a drastic approach after looking in more detail at the wide range of licenses and communities using those licenses."* | Michael Tiemann 氏 2007-04-24 | 有利な面。理事会は承認済みのライセンスを数本へ絞る案を検討し、採らなかった。Andrew C. Oliver 氏は同じスレッドで、承認の手続きそのものを閉じ、承認済みのものだけをオープンソースと宣言する案を出した。手続きは閉じられず、承認はその後も続いた |
| *"They want a license that solves a particular legal problem, and for them, I would advise that they follow their attorney's advice, not the advice of the OSI, which has more to do with policy, economics, advocacy, and the like."* | Michael Tiemann 氏 2007-04-24 | 有利な面。人気が判断の軸でない利用者が居ることを、理事会の側が認めた。ACD の gap（B10）は、特定の問題を解くライセンスとして論じる形と合う。**逆側**: 同じ文は、その利用者は自分の弁護士に従え、とも言っている。ACD を選ぶ利用者には弁護士の読みが要り、ACD はそれを持たない（B1） |
| *"If he can get the numbers up on his license, then we will certainly consider moving his license(s)s to the "Strong Communities" category."* | Russ Nelson 氏 2007-04-22 | 分類は使われ方に従って動く、という約束。承認された後に低い分類に置かれても、そこに固定されない。同じ通で *"We did not consider it practical to recommend licences that are rarely used, however sound their legal drafting may be."* とも書いた。法的な起草の良さは推薦の理由にならない |
| *"Isn't the position that new licenses are disrecommended (by definition, licenses that start out as "less popular"), also a position against improvement and change?"* | Brian Behlendorf 氏 2007-04-23 | 有利な面の批判。新しいライセンスは定義上「人気が無い」ところから始まる。**逆側**: 批判であって、分類の方針は変わらなかった。Rosen 氏は *"Remember, I wrote the bylaws and know what OSI's mission was supposed to be. "Ranking for popularity" was never a part of it."* と書いた |

**読み。** 2007 年の分類は、承認の基準ではなく推薦の基準として人気を使った。理事会の側は、承認済みを数本へ絞る案も、承認を閉じる案も採らなかった。一方で、却下の基準を述べた Tiemann 氏の文は、使われていないライセンスには法的な問題を補うものが無いことを示す。ACD にとって、承認の判断は本文の法的な健全さに寄り、それを確かめた法律家は居ない。

**この節が establish しないこと。** Tiemann 氏の文は 2007 年の一人の発言で、理事会の決定文ではない（同氏の 2007-04 の役職は、この通の署名からは確かめていない）。「明らかな法的な問題」が ACD に在るかは、この節は何も言わない。分類の制度はその後も変わっており、いまの分類の運用は `board-decisions.md` が扱う。

## 1.183 個人の起草者に示された順序 —— gap と概念を先に、最後に弁護士（The Libre Source License・2019）（2026-11-11）

`rounds/2019-08-license-discuss-libre-source-license-observed.txt`（4 通・スレッドは全 52 通）。Moritz Maxeiner 氏が個人で起草し、Contribution Public License から Libre Source License へ名を変えて 2019-08-08 に再び出した下書きへの返信。同氏の投稿は全 508 か月の写しで 2019-08 の `license-discuss` だけに在り、`license-review` への提出は無い（2026-11-11 に送り手と件名で grep）。前の名のスレッドで Lukas Atkinson 氏が特許の許諾の無さを指摘した 1 通は `reviewer-positions.md` に在る。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"You really should be working with a legal person on this if you're serious about it; there are a lot of basic drafting issues and language inconsistencies in all the drafts you have presented so far on this mailing list."* | McCoy Smith 氏 2019-08-08 | B1 の不利な面。法律家の無い個人の起草への、同じ年の 2 つ目の指摘（#262 の Perens 氏 2019-05 に足した）。同じ通で *"I'm not sure I see a reason for anyone to spend the time given these issues seem to persist as your drafts continue to evolve."* —— 下書きが変わり続けることが、読む理由を減らすと述べた（#320 に足した） |
| *"Outline the gaps you are seeing in existing OSI approved licenses vs what your goals are."* に始まる 3 段と、最後の *"After that, I'm afraid, you'd likely need to hire a lawyer, if you want a license that meets your goals, meets the OSD, and is drafted according to good legal standards."* | McCoy Smith 氏 2019-08-08 | 起草の順序の勧め: 既存のライセンスとの gap を述べる → 埋め方を条文でなく概念で述べる → gap が在るか、OSD に適合するライセンスで目標が満たせるかへの反応を見る → 弁護士。ACD は gap の主張（B10）を持ち、提出の材料は gap の行から始まる（`SUBMISSION-MATERIALS.md`）。**逆側**: ACD は条文を先に出し、5 つの版を重ねた。最後の段（弁護士）は無い（B1） |
| *"My opinion is different, I think everything you have done and asked for is appropriate for this list."* | Pamela Chestek 氏 2019-08-08 | 有利な面。下書きを list に出して意見を求めることは、この list に適切だ、という立場。同じ通で *"So I'm not sure it's the best way to go about drafting a license. But it has been a good demonstration of how difficult it is to write a good, solid license."* とも書いた |
| *"I'll refrain from posting further updates on the LSL itself for a while and rethink my approach."* | Moritz Maxeiner 氏 2019-08-08 | 帰結。起草者は投稿を止め、提出へは進まなかった |

**読み。** list の人が示した順序は、gap と概念を先に置き、条文と弁護士を最後に置く。ACD の提出の材料はこの順序の前半と合う（gap から述べる）。合わないのは、条文が先に在って版を重ねたことと、最後の段が無いことである。Chestek 氏は list に下書きを出すこと自体を適切とした。

**この節が establish しないこと。** 2019 年の個人の発言で、OSI の規則の文ではない。Smith 氏と Chestek 氏の 2019-08 の役職は、これらの通の署名からは確かめていない。Maxeiner 氏が投稿を止めた理由がこの 2 通だけかは、この節は言わない。

## 1.184 献呈と許諾を 1 つに持つ文書は、審査するなら全体を —— CC0 を招く前の議論（2012-01）（2026-11-11）

`rounds/2012-01-license-review-invite-cc0-observed.txt`（5 通・両 list で 23 通）。Karl Fogel 氏が 2012-01-03 に `license-review` で、Creative Commons に CC0 の提出を招くことに反対はあるかと問うた議論（*"Does anyone here on the license review committee think that inviting Creative Commons to submit the CC0 Dedication for OSI approval is a bad idea, and if so, why?"*）。招いた後の審査本体は `review-precedents.md` §1.138 が読んでいて、意向調査は 13 対 8 で反対、反対の 13 人は全員が特許を理由に含めた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I see no problem with approving it as a whole: the combination of a copyright disclaimer with a copyright license is a copyright license."* | John Cowan 氏 2012-01-03 | B4 の有利な面。放棄と許諾の組み合わせは、全体として 1 つの著作権のライセンスだ、という読み。ACD の §3 と §4 の並存は、この読みならそのまま審査の対象になる。同じ通で *"software licensed under CC0 is open source, period."* |
| *"I don't think it would make sense for OSI to review a portion of an integral legal document like CC0. Either review for certification/approval the whole thing or not at all."* | Richard Fontana 氏 2012-01-04 | B4 の両面。fallback の部分だけを審査する道は無く、§3 の献呈を含む全体が審査される。ACD の提出は §4 だけを見てくれとは言えない。**逆側（有利）**: 全体を一体の文書として審査し、全体を承認しうる、という前提でもある |
| *"I think submitting the licence fallback of CC0 for review as an Open Source licence is a very good idea. (This is distinct.)"* | Thorsten Glaser 氏 2012-01-03 | B4 の不利な面。同じ通で、全体を見たうえで、著作権が無いと述べる部分は著作権のライセンスとして認証しない、という立場を続けて書いた（原文はアーカイブで引用符が化けているので、ここでは要約で書く）。ACD の §3 は認証の外に置かれうる |
| *"But let's remember what 99.9% of people are going to understand if we approve this license: "OSI says CC0 is an open source license"."* | Karl Fogel 氏 2012-01-03 | 承認が外からどう読まれるか。献呈を含む文書を承認すれば、ある程度「OSI は公有を open source と言っている」と受け取られる、と同じ通で書いた。ACD の承認も、§3 の献呈ごと「OSI が認めた」と読まれる。**逆側**: 同じ通で、新しい混乱が今の混乱より良いかもしれない（*"IMHO it might well be"*）とも書いた |

**読み。** CC0 の審査が特許で止まる前に、委員会の側は構造（放棄と許諾を 1 つに持つ文書）を審査できるかを論じていた。全体として 1 つのライセンスだという読み（Cowan 氏）と、一体の文書は全体を審査するか、しないかだという立場（Fontana 氏）が出て、どちらも審査そのものを退けていない。放棄の部分を認証から外す立場（Glaser 氏）も在った。BOTTLENECKS の B4 の「意向調査で構造を理由にした人はいない」は意向調査の記録として動かないが、提出の前には構造への留保が在った。

**この節が establish しないこと。** 個人の発言で、OSI の決定ではない。Fogel 氏と Fontana 氏の 2012-01 の役職は、これらの通の署名からは確かめていない。Glaser 氏の文の後半はアーカイブの文字化けのため逐語で引いていない。

**2026-11-11 の追記 —— 1 か月後、利用者が承認を求めたスレッド（2012-02）。** `rounds/2012-02-license-review-osi-recognition-cc0-observed.txt`（7 通・全 17 通）。Carl Boettiger 氏が CC0 を承認の候補として出し、Creative Commons が自分で出すのを待つことになった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"What practical problem do you consider this licence (in truth, a professed public domain declaration with a failsafe fallback to a simple permissive licence) to solve that is not already solved by MIT License or Fair License?"* | Rick Moen 氏 2012-02-02 | B10 の不利な面。ACD と同じ型に、既存の許容型で解けていない何を解くのかが最初に問われた。同じ日に同氏は *"A bit perverse and nothing I'd recommend anyone use, but every bit as open source as the endless variety of other simple permissive licence variants."* とも書いた —— 適合は認め、勧めない。ACD の答えは帰属の無さではなく特許の側に在る（B10、`gap-measurements.md` §1.146 の 2015 年の行と同じ） |
| *"CC0 was explicitly created to solve the license challenges I have (applying equally well to data and code, not burdening the user with deciding what's substantial, and being appropriately vetted by legal experts)."* | Carl Boettiger 氏（利用者）2012-02-02 | B1 の不利な面。利用者が既製の文書を選ぶ理由の一つに、法律家に吟味されていることを挙げた。ACD はそれを持たない。**逆側**: 同じ文が挙げるデータとコードの両方に当たること（ACD の §1.2）は、ACD が答える側の性質である |
| *"Many people would stay clear off a work with such a notice."* | Thorsten Glaser 氏 2012-02-02 | 有利な面。既存のライセンスに「同梱の要件を放棄する」と自分で書き足せばよいという勧め（Moen 氏）に対し、その場の注記は人を遠ざける、と述べた。標準の文書が要る理由の一つ |
| *"The normal objection is that a random submitter can't negotiate with the OSI for changes if they are wanted."* | John Cowan 氏 2012-02-02 | B12 と B14 の参考。普通の反対は、起草した側でない提出者は変更の交渉ができないことだ、と述べた。ACD は steward のオーナーが自分で出し、版を改めて応じられる。**逆側**: 本文を書いたのは AI で、交渉に応じる語はオーナーのものになる（B14） |
| *"After all, the requirement that the originator of a license be the one to submit it is not a hard requirement, it's just a tradition that we've kept because it's a good filter."* | Karl Fogel 氏 2012-02-02 | 起草した本人が出すのは厳格な要件ではなく、濾し器としての慣行だ、という説明。同じ通で、CC0 は増殖の費用を払ってでも評価に値すると書いた（*"despite the license proliferation cost"*） |

**この追記が establish しないこと。** 個人の発言で、OSI の決定ではない。Boettiger 氏が後に CC0 以外を選んだかは確かめていない。

## 1.185 採用の入口としてのライセンス選択サイト —— choosealicense.com の公開と、「無名には理由がある」（2013）（2026-11-11）

`rounds/2013-07-and-08-license-discuss-choosealicense-observed.txt`（5 通・スレッドは全 49 通）。GitHub が 2013-07 に公開したライセンス選択サイトを、Karl Fogel 氏が OSI の FAQ から案内するかを問うた議論（*"We may want to consider linking to it from OSI's FAQ, but it would be great to get people's opinions first."*）。8 月には選択サイトの偏りと、増殖の何が悪いかの議論になった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Historically OSI has shyed away from such things because they involve recommending licenses without being lawyers, and also suggest that some licenses are more useful than others."* | John Cowan 氏 2013-07-15 | OSI 自身は、どのライセンスを使うべきかを勧める場に立ってこなかった。採用の入口は OSI の外に在る（`review-readings.md` §1.181 の下流の一覧と同じ形）。**逆側**: 勧めないことは、承認を推薦と読ませない有利な面でもある |
| *"It is fairly obvious that the GitHub site's presentation of what licenses it recommends, and why, is politically biased"* | Richard Fontana 氏 2013-08-17 | 選択サイトは中立ではない。同じ通で、要約は不正確になりやすく、案内するなら多くの選択サイトを強い注意書きつきで、と書いた |
| *"So you would like people to read and comprehend, we'll say conservatively the 11 "Popular Licenses," and find one that has the major substantive aspects they want but that also does not have any aspect that could use some tweaking for their own business model -- say, for example, a delayed release date of source code, which will mean they will write another license, or find another obscure license that does what they want but is obscure for a reason."* | Pamela Chestek 氏 2013-08-19 | B2 の不利な面。無名のライセンスは理由があって無名だ、という読み。#289（同氏 2019「使われていないことは欠陥の証拠かもしれない」）の 6 年前の形で、#289 に足した。同じ通で、選択サイトは主な性質の要約で採用を決めさせるものだと書いた —— ACD の主な性質が短い要約に収まるかは B13 の問いである |
| *"It isn't that MORE licenses are necessarily bad. Instead, say that the proliferation of BAD (or "me-too" or "un-templated" or "legally questionable") licenses is bad."* | Lawrence Rosen 氏 2013-08-20 | 両面。増殖で悪いのは数ではなく質だ、という立場（有利）。挙げた 3 つの悪さのうち、ACD は「型に合わない」（既存の言い回しを借りない・#184）と「法的に疑わしい」と読まれうる（法律家の読みが無い・B1）。同じ通で、良し悪しは依頼人の必要によるので、この list のほとんど誰も（自分も）見分けられない、とも書いた |

**いまの choosealicense.com（2026-11-11 に WebFetch で読んだ要約・逐語ではない）。** 比較の表（`/appendix/`）は 47 本を挙げ、献呈の型の Unlicense、CC0、0BSD、MIT-0 を含む。OSI が承認していない WTFPL も載っている。ACD は無い。**有利な面**: 献呈の型そのものは、採用の主な入口に既に在る。載るかどうかは OSI の承認と同じ基準ではない。**逆側**: ACD はこの入口に無く、承認されても載るわけではない（#322 に足した）。

**この節が establish しないこと。** 2013 年の個人の発言で、OSI の決定ではない。choosealicense.com が何を基準に載せるかは確かめていない。表は WebFetch の要約で読んだので、逐語の照合はしていない。

## 1.186 弁護士は要るか、で list の弁護士 2 人が反対を向いた —— 承認済みライセンスの小さな変種の FAQ（2013）（2026-11-11）

`rounds/2013-03-license-discuss-slight-variations-lawyer-observed.txt`（4 通・スレッドは全 10 通）。委員長の Luis Villa 氏が、承認済みライセンスの 1〜2 語違いの変種は承認済みか、という FAQ の下書きを提案し、Karl Fogel 氏が答えの文案に弁護士の確認を入れた（*"if you have a competent lawyer review the variation and you conclude that it is minor and could not possibly have any legal signifance"*）。そこから弁護士の要否の応酬になった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The idea that you would need a lawyer, competent or otherwise, to be involved in such review, though personally appealing from a guild-aggrandizement standpoint, seems highly dubious, and probably sends the wrong message."* | Richard Fontana 氏 2013-03-07 | B1 の有利な面（狭い）。弁護士である本人が、確認に弁護士が要るという考えは疑わしく、間違った合図を送ると述べた。委員長の Villa 氏は *"Agreed."* と答えた。**逆側**: 話は承認済みライセンスの小さな変種の確認で、新しいライセンスの起草ではない |
| *"we should declare that it is really foolish to entrust your copyrighted works to amateur legal efforts."* | Lawrence Rosen 氏 2013-03-07 | B1 の不利な面。素人の法的な試みに著作物を預けるのは愚かだと宣言すべきだ、と述べ、Jacobsen の件（#262 の Perens 氏と同じ例）を挙げて *"Let's not encourage the same mistakes in future licenses."* と続けた。ACD は法律家の読みを持たない新しいライセンスで、この文が向く先そのものである |
| *"I really don't want submissions of every 1-2 word variation in a license, which this wording would seem to encourage (whether or not filtered through a lawyer)."* | Luis Villa 氏（委員長）2013-03-07 | 審査の負担への関心。弁護士を通したかどうかに関わらず、細かい変種の提出を増やしたくない、という委員長の立場。ACD は変種ではないが、審査の手が限られていることは §1.176 の追記（CeCILL の 1 年の停止）と同じ向きである |

**読み。** 弁護士の要否について、list の弁護士は 1 つの声ではない。Fontana 氏は小さな変種の確認に弁護士を求めることを退け、Rosen 氏は素人の起草そのものを退けた。ACD に当たるのは後者の向きで、前者は承認済みのものの扱いに限った話である。2007 年に提出の手順から法律家の分析の要件が外れたこと（`review-rules.md` §1.141）と並べて読む。

**この節が establish しないこと。** 2013 年の個人の発言で、OSI の規則の文ではない。FAQ の答えがどう公開されたかは確かめていない。

## 1.187 list の沈黙は読んだ印ではなく、理事会は前もって判断を示さない —— 2017 年 1 月の委員会報告（2026-11-12）

`rounds/2017-01-and-02-license-review-committee-report-observed.txt`（4 通・会話は全 19 通）。委員長の Richard Fontana 氏が 2017-01-08 に、2015-10 以後に出されて決まっていないライセンスと NOSA 2.0 の推薦を書いた報告と、その後の議論。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"My guess is that most people subscribing to and reading this list have not attempted to read the license and have no particular opinion about it."* | Richard Fontana 氏（委員長）2017-01-09 | 両面。list の沈黙は支持でも反対でもなく、読まれていないことの印だ、という委員長自身の読み。ACD の `license-discuss` への投稿に返信が無いことを、支持と読ませない（`REVIEWERS.md` の Status の書き方）のと同じ向きである。同じ通で *"The 'Recommendations' here are just my own recommendations."* とも書いた |
| *"At the last OSI board meeting, the OSI decided not to hold a vote on NOSA 2.0, and instead requested that I prepare a document providing my comments about the license."* | Richard Fontana 氏 2017-01-23 | 委員長が却下を勧めても、理事会は採決しないことがある。#257（NOSA 2.0 の留め置き）の 2017 年の段の一次の記録である |
| *"I think the current Board is not inclined to give the equivalent of "advisory opinions" on the OSD, for better or worse. It is probably better to get clarity on this issue through actual submission of a license embodying some sort of license asymmetry."* | Richard Fontana 氏 2017-02-08 | 不利な面。理事会は OSD の解釈について前もって判断を示さず、はっきりさせるには実際に提出するのがよい、という委員長の見立て。ACD の `license-discuss` への投稿は審査の前の意見を求めたもので、判断は審査に出してからでないと得られない向きである（`REVISION-PROTOCOL.md` §3.6 の分岐 B）。**逆側**: 2017 年の一人の見立てで、議論の場（discuss）で指摘を受けて直すこと自体を否定してはいない |

**この節が establish しないこと。** 委員長の個人の推薦と見立てで、理事会の決定文ではない。2017 年以後に理事会が助言的な判断を示したことがあるかは、この節では確かめていない。同じ "advisory opinions" の語は、2018〜19 年の審査の手順の議論の rounds（`rounds/2018-to-2019-license-discuss-review-process-cited-observed.txt`）にも在る。

## 1.188 数十万の利用者を挙げても退けられた提出 —— ZENTAO Public License（2016）（2026-11-12）

`rounds/2016-06-license-review-zentao-public-license-observed.txt`（5 通・2016-06 の 2 つの会話 "ZENTAO PUBLIC LICENSE For Approval" と "Approval request for ZENTAO PUBLIC LICENSE" で全 61 通、1 通は 2017-01 の委員会報告の会話から）。中国の会社が 2016-06-05 に、自社の製品の画面に出所の表示を残すことを求めるライセンス（badgeware）を出した。正本は中国語だった。委員長の 2017-01 の報告（`review-readings.md` §1.187 の rounds）の推薦は *"Comments: Submission did not fully follow approval requirements. Substantive discussion focused on the badgeware issue; some suggested that legacy approval might be a more appropriate path."*、*"Recommendation: Reject."* だった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"This is a private Google Docs link, which is not accessible to us. If you expect us to evaluate the license, please attach it to email as a text file."*、同じ通で *"Do you have approved English versions of your documents? While we can use translation tools, we've found that they aren't adequate for licensing."* | Josh Berkus 氏 2016-06-06 | 提出の形。本文は文字のファイルとして添付する。英語の正本が無いと審査の手が止まる。ACD は英語だけを正本とし（1.4 草案の §15.4）、本文は `.txt` で在る —— 有利な面。同じ通の問い（*"What other licenses did you consider, and why were they found not to be adequate?"*）は B10 の問いと同じである |
| *"But more to the point, OSI has historically not accepted badgeware licenses like this, because they don't allow for the possibility of reuse of parts (especially small parts) of the software in new contexts where "texts, images, and links" are no longer relevant."* | John Cowan 氏 2016-06-06 | 出所の表示を残させる条件は、部品の再利用を妨げるとして退けられてきた。ACD は帰属の義務を持たない（§10.1）—— 有利な面。**逆側**: 帰属の無さは gap ではない（B10・`gap-measurements.md` §1.146 の追記） |
| *"ZPL has been applied in three of our products and approved by hundreds of thousands users of ours."* | 提出者 2016-06-23 | B2 の逆側の例。数十万の利用者を挙げた提出でも、OSD への疑義と提出の形の不備で退けられた。使われていることは承認の十分な条件ではない |
| *"Can we get a Chinese reader to review the Chinese version, since it's the authoritative version?"* | Josh Berkus 氏 2016-06-24 | 正本が英語でないと、その言語を読める審査者を探すところから始まる。2017-01 の報告への返信で同氏は *"Also, the license's main langauage is Chinese, and needs to be reviewed in that language, which I think stalled us."* と書いた（原文ママ・2017-01-09）。ACD の英語の正本は、この費用を持たない |

**2026-11-12 の追記 —— 英語以外の正本の扱い（EUPL v1.2・2017）。** `rounds/2017-05-and-07-license-review-eupl-1-2-observed.txt`（2 通）。Simon Phipps 氏は International の分類について *"That categorisation was created for licenses submitted in languages other than English, as it triggers a process that allows the list and board to reasonably review the license."* と書き（2017-05-30）、委員長の Richard Fontana 氏は 2017-07-13 に *"The OSI has approved EUPL v1.2."*、*"As with EUPL 1.1, the approval extends to all the official language versions of the license."* と告げた。英語以外の正本を持つライセンスにも審査の道は在り、全ての言語の版に承認が及ぶ例である。ACD は英語だけを正本とするので、この分類の手続きを要しない。

**この節が establish しないこと。** 却下の理由は委員長の推薦の文に限り、理事会の決定文は読んでいない。ZENTAO がその後に別の形で出されたかは確かめていない。

## 1.189 プライバシーの条件を利用に課すと退けられる —— Twente License（2019）（2026-11-12）

`rounds/2019-02-license-review-twente-license-observed.txt`（4 通・スレッドは全 19 通）。MIT に、派生物が利用者の同意なく個人の情報を集めないことなどの条件を足したライセンスが 2019-02-05 に出され、同日から OSD 6 に反するという返信が続き、提出者は却下を受け入れた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The OSI board is the entity that issues rejection, but they listen to this group. Sorry, I concur this violates OSD #6."* | Bruce Perens 氏 2019-02-05 | 利用の目的や分野で条件を課すライセンスは OSD 6 に反する、という読み。ACD は利用に条件を課さない（§10.1） |
| 人権とプライバシーは *"as expressed in the text of a license, are matters of opinion, so a developer/distributor cannot know if they have violated the license or not, pending litigation."* | Josh Berkus 氏 2019-02-05 | 条件が意見の問題だと、利用者は守れているかを知れない、という具体的な理由。ACD の §11.3（虚偽の表示）と §11.4（プライバシー等の権利）は条件ではなく到達の限界として書かれ、*"it is not a condition upon You, and Section 10.1 is unaffected by it"* と明記する（1.4 草案）—— 有利な面 |
| *"Open source MUST be allowed to do illegal things. It is not up to the copyright owners to perform law enforcement."* | Carlo Piana 氏 2019-02-06 | 法を守ることをライセンスの条件にするな、という立場。ACD は違法な利用を禁じる条を持たない。**逆側**: §11.3 は虚偽の表示を Dedication の外に置き、§5.2(d) はプライバシー等の不主張から虚偽の言明を除く —— 条件ではないと書いていても、読み手が「法の執行」に近いと読む余地は残る |
| Twente は利用を規制しようとしていて、*"not just the copying and modification of the software."*（原文は *use* を強調） | Lukas Atkinson 氏 2019-02-06 | 著作権の外の「利用」を規制することへの異議。ACD は利用を規制しない。**逆側**: ACD は §5 で Dedicator 自身の行為（技術的手段・契約による条件の付加）を縛る —— 規制の向きが Dedicator で、利用者ではないことを提出の材料で言う必要がある |

**読み。** Twente は「条件として課す」ことで退けられた。ACD はプライバシーと虚偽の表示を、許諾の範囲の限界として書き、利用者への条件ではないと明記している。この書き分けが、Twente と同じ読みを避ける理由である。

**この節が establish しないこと。** 個人の発言で、理事会の決定文ではない（提出者が却下を受け入れたので、理事会が判断したかは確かめていない）。ACD の書き分けが OSI の審査で同じように読まれるかは、この節は言わない。

## 1.190 誰も賛成しなければ 3 週間で「却下」、本文を添えずに配ることへの懸念 —— Non-Coercive Copyleft Licence（2015）（2026-11-12）

`rounds/2015-07-and-08-license-review-nccl-observed.txt`（4 通・スレッドは全 38 通）。Tim Makarios 氏が 2015-07-20 に、CC0 に近いが派生物を同じ条件で配らせるライセンス（本人の言い方では "CC-0-SA" に近いもの）を個人で出した。ACD は同じ条件で配らせる条を持たないので、コピーレフトの論点は当たらない。当たるのは次の 3 点である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| NCCL は、ライセンスを添えずに配ることを勧める（原文は *encourages* を強調）初めての提出だ —— *"distributors to distribute the code without the license attached."*、*"Disributing a copy of the license with the software isn't just about protecting the rights of the original author; it's about protecting the users, but informing them of their rights under the license."*（原文ママ） | Josh Berkus 氏 2015-07-31 | 両面。ACD の §16.2 は識別子だけで足りる通知とし、本文が添えられていなくても条項が全部当たると書く。受領者に義務を課さないので、NCCL の「知らずに条件に縛られる」害は起きない（有利）。**逆側**: 受領者が自分の権利を知らされない、という Berkus 氏の後半の懸念は、条件の有無に関わらず当たる —— 途中で通知が落とされれば、受け取った人は与えられた許諾を知らない |
| *"Indeed, some courts will NOT enforce a license that has NOT been seen and approved by the licensee."* | Lawrence Rosen 氏 2015-07-31 | 不利な面。#321（同意を求めない形の免責は効かないかもしれない）の 3 例目として #321 に足した。逆側は §1.180 の追記と同じ（受け入れの手順を求めることは OSD 10 が退けた） |
| *"Nobody on this committee has spoken in favor of it. Therefore, I believe "rejected" is the correct status."*（2015-08-07）、同じ日に *"I don't believe that "30 days" is intended as some kind of guaranteed minimum."*、*"Really, this is up to the Chair, though."* | Josh Berkus 氏 2015-08-07 | 審査の時間の逆の端。提出から 18 日で、委員会で誰も賛成しないことを理由に「却下」と述べられた。個人の起草で、反対は 4 人だった。§1.187 の 2017 年の委員長（list の沈黙は読まれていない印）と並べると、「賛成が無い」の扱いは人と年で違う。同氏は決めるのは委員長だとも書いた |

**読み。** NCCL は CC0 と同じ方向（権利を手放す）とコピーレフトを 1 つにしようとして、両立しないと読まれた。ACD はコピーレフトを持たず、この矛盾は無い。ACD に残るのは、本文を添えない配り方を許すことの両面（義務が無いので害は無いが、権利を知らされない受領者が出る）と、同意を求めない形の費用（#321）と、誰も賛成しないときに早く閉じられうることである。

**この節が establish しないこと。** Berkus 氏の「却下」は委員会の一人の判断で、委員長の推薦や理事会の決定文は読んでいない。NCCL がその後どうなったかは確かめていない。

## 1.191 条件の無い許諾は撤回できるか、譲渡の後も続くか —— cphack と GPL（2000）（2026-11-12）

`license-discuss` 2000 年 3 月の "Wired Article on the GPL"（3〜4 月・43 通）から 15 通と、同じ年の 8 月の "Public Domain and liability"（13 通）から 2 通、"Abandonment"（2 通）から 1 通（`rounds/2000-03-license-discuss-gpl-revocation-cphack-observed.txt` と `rounds/2000-08-license-discuss-public-domain-liability-and-abandonment-observed.txt`）。cphack の著作者 2 人は、プログラムを GPL の下で配った後に著作権を Mattel の側へ譲渡し、譲受人が配布を止めようとした。そこから、GPL は撤回できるか、譲渡の後も続くか、条件が対価になるかが論じられた。発言者のほとんどは法律家でないと自分で書いている。法律家の肩書きで書いたのは Rod Dixon 氏（J.D., LL.M.）だけである。読んだ記録の中で、撤回と譲渡と対価の問いを list が扱った最も古い記録で、ACD の §2.2（撤回しない）、§2.8（譲受人も拘束される）、§4.1（撤回できない許諾）と、条件を課さない設計（§10.1）に当たる。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"A. Is revocation by M possible?"* | W. Yip 氏 2000-03-30 | 問い。譲渡の前に GPL で配られた作品の配布を、譲受人が止められるか |
| *"By releasing under the GPL, the original authors surrendered their right to control GPL-compatible copying.  Having surrendered that right, the original authors are not able to transfer it."* | Chip Salzenberg 氏 2000-03-29（*"[IANAL]"*）。翌日には *"the license adheres to the code, not the author."* | 有利な向き。許諾した分の権利は譲渡で取り戻せない。ACD の §2.8 の *"A transferee takes subject to it"* と同じ向きである |
| *"A nonexclusive license, whether recorded or not, prevails over a conflicting transfer of copyright ownership if the license is evidenced by a written instrument signed by the owner of the rights licensed"* | Ken Arromdee 氏 2000-03-29（Slashdot に引かれた合衆国法典 17 編 205 条 (e) の写しを引いた） | **不利な面で、ドシエに無かった。** 合衆国では、非独占の許諾が後の譲渡に優先するのは、権利者が署名した書面で示されるときである。ACD は署名を求めず、Dedicator が通知を置くだけである。§2.8 は法が許す限り譲受人を拘束すると書くが、署名の無い通知がこの書面に当たるかには答えていない。署名を持たない承認済みのライセンスにも同じ問いが当たるので ACD だけの問題ではないが、§2.8 は譲受人について明示の主張をしている。引用はリストに引かれた写しの写しで、その逐語は条文に当てていない。portfolio-aa が同じ日に LII で条文を確かめ、要件を `QUESTIONS-FOR-COUNSEL.md` 問 1 (j) に言い換えで置いた。`against.md` #152 の追記 |
| *"I think it safe to assume that in absence of a 'written instrument' a license is exhausted by the act of copyright transfer."*、*"a purchaser, particularly a bona fide one, may not know anything about the licenses attached to a copyright which he is purchasing, and thus deserves protection"* | W. Yip 氏 2000-03-30 | 不利な面。署名の無い許諾は bare licence で、譲渡で尽きる、という読み。善意の譲受人を守る側の理由も書いた。Richard Watts 氏は同じ日に、英国法から見れば条文に優先を否定する語は無い、と答えた |
| *"Licenses are personal, in general, and a license that isn't a contract (a bare permission) can be freely revoked by the licensor"*、*"If the copyright owner revokes the permissions, you are probably out of luck."*、*"You can rely on that permission unless you know or should have known that it has been revoked."* | John Cowan 氏 2000-03-30・31 | 不利な面。2003 年の Rosen 氏の *"Probably a new licensee with notice of the revocation can't obtain a license."*（`gap-measurements.md` §1.146 の追記）と同じ形で、3 年早い。`QUESTIONS-FOR-COUNSEL.md` 問 1 (i) が尋ねる「何も無い」の側である |
| *"That CAN'T be right. If it is right, we need a quick revision to the GPL to fix this problem."* | Justin Wells 氏 2000-03-30 | 有利な向き。撤回できないことを本文に書く必要は、2000 年に使う側から言われていた。ACD は §2.2 と §4.1 でそれを書く。書くことで撤回が止まるかは、Cowan 氏の文と QFC 問 1 (i) の問いに残る |
| *"there's always the possibility of a court ruling that recipients of GPL software are providing consideration, so it's a contract."*、*"If you distribute a binary, the consideration might be that you distribute the source."* | Ken Arromdee 氏 2000-03-30（IANAL）。Richard Watts 氏も翌日、ソースを配る義務を対価と読んで考えを改めた（*"I changed my mind"*） | **不利な面で、新しい。** GPL では、受領者の側の条件（ソースを配ること）が対価になり、契約として撤回を防ぐ道が論じられた。ACD は You に条件を課さない（§10.1）ので、この道を持たない。`against.md` #324 |
| *"By requiring that source code be shared, it helps us achieve goal #1."*、*"By requiring that we be credited on derivative works, it helps us establish our reputation and achieve goal #2."* | Justin Wells 氏 2000-03-31 | 同じ向きの不利な面。対価の候補として挙げられたのは、ソースを共有させる要件と、派生物に名前を載せさせる要件の 2 つで、どちらも受領者に課す条件である。ACD は条件を課さず、帰属も求めない。同じ日に Chip Salzenberg 氏は、自由なソフトウェアが増えることは著作者の価値観では対価になる、と書いた。W. Yip 氏（英国の法学生と自分で書いた）は、英国法では対価は主観で決まらないと答えた |
| *"Shaky."* | Cowan 氏 2000-03-31（Watts 氏の議論に） | 逆側。条件を対価と読むこと自体も確かではなく、GPL の側の道も開いたままだった。2004 年に Rosen 氏は約束的禁反言は bare licence に関わらないと書いた（`review-responses-clauses.md` §2） |
| *"even if you place a disclaimer on the software, someone could legally distribute your software without the disclaimer"* と *"They specifically state "redistribution must include this license", with the disclaimer in the license."* | Blake Cretney 氏と Brian Behlendorf 氏 2000-08-07（"Public Domain and liability"） | `against.md` #41（免責の文が作品について行かない）の、読んだ中で最も古い記録。承認済みの許容型は、許諾の文を付けて配ることを条件にして免責を運ぶ。ACD は条件を持たないので運ばない |
| *"Generalized attempts to *push* works into the public domain by unrecorded dedications do not serve the public interest well."*、*"once a work *enters* the public domain, it stays there."* | Rod Dixon 氏（J.D., LL.M.）2000-08-10（"Abandonment"） | 両方の面。登録の無い宣言で公有化しようとすることは、公有かどうかを判断する手間を利用者に負わせる、と法律家の肩書きで述べた。ACD の §3 はその宣言で、§4.4 は §3 が効くかどうかに依らずに許諾を立てる（B5）。後半の文は、効いた公有化は撤回できないという、§3 に有利な向きの文である |

**読み。** 2000 年の議論は、撤回できるかを 2 つの道で答えようとした —— 撤回できないと本文に書くこと（Wells 氏）と、条件を対価にして契約にすること（Arromdee 氏・Watts 氏）。ACD は前者を取り、後者を設計として持たない。条件を課さないことは ACD の中心で、変えない（変えれば ACD でなくなる）。だからここに書くのは、その設計の費用である。同じ費用は、条件を課さない承認済みの 0BSD・MIT-0・Unlicense も負っている。205 条 (e) の問いは、署名を持たない承認済みのライセンスすべてに当たるが、§2.8 が譲受人について明示の主張をしている分、ACD には答える必要がある。

**この節が establish しないこと。** 2000 年の個人の発言で、ほとんどが法律家でない人の見通しである。cphack の件が裁判所でどう扱われたかは、このスレッドには無い。同じスレッドの David Johnson 氏と Mark Wielaard 氏は、GPL の表示は 1 ファイルの 1 行だけで、本文の主な文書は *"you can do whatever you want with it"* と書いていたと述べた。205 条 (e) の list の写しの逐語は条文に当てていない（要件は portfolio-aa が LII で確かめた）。スレッドの残りの 28 通（4 月の書庫の 7 通のうち 2 通は保険を例にした対価の話、5 通は合衆国法典 17 編 117 条と RAM への複製の話。3 月の残りは、件の事実、GPL を受け入れるとは何か、UCITA、電子署名で許諾を運ぶ案、英国法の対価の説明）と "Public Domain and liability" の残りの 11 通（政府の著作物、州の著作権、FOIA）は、ACD に当たる新しい材料を持たない。

**2026-11-12 の追記 —— 5 年後に同じ問いへ同じ答えが出た。** "When can licenses be revoked?"（`license-discuss` 2005-09・10 通・`rounds/2005-09-license-discuss-when-can-licenses-be-revoked-observed.txt` に 5 通）。Ben Tilly 氏は、相続人が撤回できない理由を尋ねられて答えられず、*"many popular licenses (eg GPL, BSD) are not contracts."* と書いた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I thought only licenses given without consideration were revocable at will - most licenses open-source include obligations upon the licensee and are thus not without consideration, and so cannot be revoked at will"* | Alex Bligh 氏 2005-09-07 | 2000 年の Arromdee 氏と同じ道で、受領者の義務が対価になって撤回を防ぐ。ACD は受領者に義務を課さないので、この道を持たない（`against.md` #324） |
| *"there would have to be an obligation upon the licensee. Any obligation on the licensee is thus likely to count, including the acceptance of liability limitation."* | Bligh 氏 2005-09-09 | 不利な面で、#324 の範囲を確かめる文。対価の候補に免責を受け入れることまで挙げた。ACD は §13 と §14 で免責を置くが、受け入れを求めない（§2.3・#321）ので、この候補も弱い |
| *"He may have much more difficulty finding others who agree that open source licenses can simply be terminated by notifying licensees."*、*"I'm not aware of any copyright holders who then took the extra, drastic step of informing licensees that their open source license had been revoked."* | Andy Wilson 氏 2005-09-07（Intel・法律家でないと書いた） | 有利な向き。撤回を通知した例を知らない、という実務の観察。2000 年の cphack も、配布を止めようとした例であって、許諾の撤回が裁判所で認められた記録はこのスレッドにも無い |
| *"an open source copyright license, once given, might be revokable.  However when it may be revoked is fairly unclear, and is likely to vary by jurisdiction."* | Tilly 氏 2005-09-09 | まとめ。Bligh 氏は *"You are correct that it is unclear"* と答えた。法域で変わる、という点は QFC 問 1 (i) と同じ場所に在る |

**この追記が establish しないこと。** opensourcelaw.biz の宛先から書いた Brendan Scott 氏の 2 通は、アーカイブに添付として除かれた形でしか無く、読めていない。Bligh 氏が挙げた英国の判例（Hurst v. Picture Theatres）は当たっていない。

**2026-11-12 の追記 —— 2011 年、撤回できないと書くことが GPL 3.0 の答えだったと述べられた。** "GPL revokability"（`license-discuss` 2011-05・5 通・`rounds/2011-05-license-discuss-gpl-revokability-observed.txt` に 3 通）。Ron Teitelbaum 氏は、Groklaw の 2006 年の記事を *"as an explanation as to why irrevocable was added to v3."* と挙げ、GPL で出したものを後で撤回できるかを尋ねた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"GPL v. 3.0 provides that it is irrevocable during the term of the copyright so long as the licensee is in compliance with the license."* | nvalaw.com の宛先から、弁護士と名乗って（*"IAALBNYL"*）書いた人 2011-05-10（名前はアーカイブに無い） | 有利な向き。撤回できないことを本文に書くことは、GPL の次の版が採った答えだった。ACD は §2.2 と §4.1 で同じことを書き、条件が無いので「守る限り」の限定も無い |
| *"The answer re GPL v 2.0 and 1.0, as unsatisfying as it may seem, is it depends upon the specific facts and the applicable jurisdiction's law."*、*"The GPL is a non-exclusive license subject to interpretation and enforcement under contract law and the related equitable concepts just like any other software license"* | 同じ人 | 両方の面。撤回について黙っている版の答えは事実と法域による。ACD は黙っていないが、書いたことが効くかも法域による（QFC 問 1 (i)）。契約法と衡平法の両方で読む、という立場では、ACD は契約法の側の道（受領者の義務を対価にすること）を持たず（#324）、衡平法の側（§2.5 の禁反言）に頼る |
| *"Until someone really try it in court, the debate will not be settled."* | Cinly Ooi 氏 2011-05-10（IANAL と書いた） | 2000 年・2003 年・2005 年と同じ結び。11 年たっても、list の上で撤回の問いは裁判で試されていなかった |

**この追記が establish しないこと。** 弁護士と名乗った人の名前と資格は確かめていない。Groklaw の記事は開いていない。GPL 3.0 の本文の該当の文は、リポジトリに写しが無いので、ここでは本文に当てずこの人の要約として置いた。

**2026-11-12 の追記 —— 同じ週に「ライセンスは契約か」も答えが分かれていた。** "Licenses versus contracts"（`license-discuss` 2000-03・5 通・`rounds/2000-03-license-discuss-licenses-versus-contracts-observed.txt` に 3 通）。cphack の議論の前日に、David Johnson 氏がライセンスと契約の違いを尋ねた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Simply stated, a license is a contract."*、*"A transfer and a license are both contracts, but they are very different."* | Rod Dixon 氏（J.D., LL.M.）2000-03-29 | ライセンスを契約とみる側。契約なら成り立つのに対価が要り、ACD は受領者の義務を対価として挙げられない（#324） |
| *"Thus a copyright license such as "You have the right to make up to five verbatim copies of this message and send them to your friends" is a bare license which happens to be in writing.  It is not the subject matter of any contract."* | John Cowan 氏 2000-03-29 | 許可とみる側。W. Yip 氏も同じ日に、許可と契約は *"two distinct legal concepts, which regrettably are known to overlap"* と書いた。許可なら対価は要らないが、翌日の Cowan 氏の文のとおり撤回されうる（上の表）。どちらの見方でも、ACD が頼るのは対価ではなく §2.5 の信頼と §4.1 の語で、その効き方が開いていること（QFC 問 1 (i)）は変わらない |

**この追記が establish しないこと。** 法律家の肩書きで書いたのは Dixon 氏だけで、Cowan 氏と Yip 氏の文は説明であって法の判断ではない。

## 1.192 2008〜2010 年の委員会報告 —— 条件を放棄しても承認は外れない、簡単な方がよいとは限らない、何でもしてよい式は望む効果を持たない（2026-11-12）

委員長の Russ Nelson 氏の委員会報告 3 本（`license-review` 2008-11-11・2010-06-01・2010-12-01）と、2012-03 の `license-discuss` の "license committee"（`rounds/2008-to-2012-license-lists-committee-reports-observed.txt`・10 通）。2004 年の報告（`board-decisions.md` 8.11 節）と同じ形で、ライセンスごとに勧告と理由を書く。portfolio-9b の「決める側・未読」の一覧（PR 2937）から読んだ。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I think that this committee should ask the board to agree that if a licensor using an open source license waives any conditions imposed by the license, their license is automatically approved."*、*"Not being a lawyer, I don't know if that idea achieves the effect desired: giving a user more freedom doesn't remove OSI approval."* | Russ Nelson 氏（委員長）2008-11-17 | **有利な向き。** 承認済みのライセンスの条件を全部放棄しても承認は外れない、という委員長の案。条件を課さない ACD（§10.1）は、その帰結の形をしている。**逆側**: 案であって、理事会が採った記録はこのスレッドに無く、委員長自身が法律家でないと書いた。同じ通で、新しいライセンスは Jacobsen の判決に語を合わせよという Rosen 氏の助言を *"wise"* とした（条件を持つことで執行できる、という #307 の側の話） |
| *"Bruce, Matthew, and I have been trying to convince them that an open source license is not the right tool to do this."* → *"Recommend: rejection"*（UOML License 1.2）。2008-11-13 に委員長は *"The board did indeed approve the MirOS License."* と書き、UOML の却下も伝えた | 委員長 2008-11-11・13 | UOML は、規格に適合する実装にだけ使わせる制限で却下された（`AS-OF.md` の UOML の記録と同じ）。ACD はこの種の制限を持たない。MirOS は 2004 年の勧告（8.11 節）から 4 年後に承認された |
| *"Commentators are uniformly dubious of the value of this license.  Simpler isn't necessarily better when it comes to legal documents."*（KLLSD License・提出者は Apache を *"too wordy"* とした） | 委員長 2010-06-01 | B3 の両面。短くすること自体は価値と数えられない —— 2004 年の WSOSL への *"shortness is not an improvement"* と同じ線である。ACD の長さ（B3）は短さで補えないが、長さそのものも理由にされていない |
| *"Bruce suggests that a lawyer be involved."*（BSD+1 License）と、提出者の *"I can't afford a lawyer to help me, and I apologize for submitting it without having a lawyer check it first."*（名の無いライセンス） | 委員長 2010-06-01 と Joel Rees 氏 2010-06-02 | B1 の不利な面。法律家を入れるよう勧められた提出と、法律家を雇えないと詫びた単独の提出者が同じ報告に並ぶ。後者は名を付けるまで審査の表から外れた（2010-12 に本人が了承）。ACD も法律家の読みを持たない |
| *"Cowan says it won't work. So doe Perens. DiBona is even more dismissive.  Not likely to have the desired effect."* → *"send back for further revision"*（Do Whatever You Want To With It Public License） | 委員長 2010-12-01 | **不利な面。** 何でもしてよい式の短いライセンスが、望む効果を持たないとして差し戻された。2009 年の WTFPL の却下（`board-decisions.md` 8.1 節）と同じ類型である。ACD はこの類型の目的（何でも許す）を共有するので、審査者がこの類型と並べて読む恐れがある。**逆側**: ACD は条ごとに効果を書いた長い文書で、差し戻しの理由（効かない）に対しては §3・§4・§5 の 3 つの足場で答えている |
| *"The requirement to submit changes directly to the licensor is a technology-specific term"*（netX・OSD 10 に反するとされた）、*"Indemnity is too broad"*（CodeIgniter） | 委員長 2010-12-01 | ACD は変更の提出も補償も求めない |
| *"And the point is that OSI can't even bring itself to dis-approve the "crayon" licenses."* と、*"OSI, unlike FSF, has always been seen as a neutral fact-finder."* | Bruce Perens 氏と John Cowan 氏 2012-03-09 | 2004 年の増殖の委員会の後の評価。McCoy Smith 氏は、2006 年の報告が自発的な非推奨をあまり生まず、2006 年以後に足された数は少なく見える、と書き、Mike Milinkovich 氏は、その報告の具体的な結果として Common Public License が Eclipse Public License に替えられて非推奨になったことを挙げた。素人の起草への list の言葉（*crayon*）は `against.md` #158 に在る |

**読み。** 2008〜2010 年の報告は、2004 年と同じ線を保っている —— 門は OSD への適合で、短さや新しさの主張だけでは足りず、効かない条項は差し戻される。ACD に有利なのは、条件を放棄しても承認は外れないという委員長の案と、使用を制限する条件を持たないこと。不利なのは、法律家を入れるよう勧める文と、何でもしてよい式の類型の差し戻しである。

**この節が establish しないこと。** 報告はどれも委員長の勧告で、2010 年の 2 本の理事会の議決はこのスレッドに無い。2008-11 の委員長の案が採られた記録は読んでいない。2012 年の発言は個人の評価である。

## 1.193 弁護士に曖昧さを指摘され、提出者が認め、本文を変えずに承認された —— Microsoft Community License と Reciprocal License（2005・2007）（2026-11-12）

`license-discuss` の 3 つのスレッド: 2005-12 の "For Approval: Microsoft Community License"（10 通・John Cowan 氏が出した。Microsoft 自身の提出ではない）、2007-08 の同名のスレッド（16 通・Microsoft の Jon Rosenberg 氏が出した）、2007-10 の "For Approval: Microsoft Reciprocal License"（9 通）。13 通を `rounds/2005-12-to-2007-10-license-discuss-ms-cl-and-ms-rl-observed.txt` に置いた。portfolio-9b の「決める側・未読」の一覧から読んだ。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"When software under multiple licenses is combined into one .zip or .tar file, must that entire file be under the MS-CL? File-based software licenses are subject to confusion on that point. Not that this would affect its compliance with OSD at all, it just possibly turns a reasonable reciprocity requirement into a very dangerous one."* | Lawrence Rosen 氏 2007-08-10 | 通知や条件がどの素材に及ぶかという問いは、ACD では §16.2 の *"the material it accompanies"* に当たる（`ACD-1.4-SECOND-CLARITY-TRIAL.md` T23・T26・T28）。Rosen 氏はそれを OSD の問いではなく、配る人にとっての危険の問いとして出した |
| *"I think MSCL is clearly OSD-compliant, but the file-based rule is over-simplistic, and can result in ambiguities like this."* | Matthew Flaschen 氏 2007-08-10 | 同じ切り分け。適合と、語の質とを分けて述べている |
| *"We are looking into various ways that the ambiguity can be addressed, but please know that the intent of the language was not to cause one software program that is licensed under a particular license, to be subject to the terms of the MCL, merely because the two are both contained in the same .zip, or similar type of file."* | Jon Rosenberg 氏（提出者）2007-08-10 | 提出者は曖昧さを認め、意図を list に書いた |
| *"This license contains the same terms as the previously submitted Microsoft Community License, but has been renamed for greater clarity"* | Rosenberg 氏 2007-10-02 | **有利な向き。** 出し直した本文は、3(A)（*"For any file you distribute that contains code from the software …"*）を含め、8 月の本文と 1 語も変わっていない（2 つの提出文の *"This license governs use"* から末尾の免責までの 467 語を語ごとに比べた。題名は比べていない）。Flaschen 氏は *"I still support approval of this license."* と書き、OSI の一覧の API（`opensource.org_api_licenses.json`・2026-10-27 取得）は MS-RL の提出日を 20071003、承認日を 20071010 とする |
| *"I was under the impression that the Ms-RL abbreviation refers to the Microsoft Reference License"* | Mike Strobel 氏 2007-10-10 | 略称が既存の別の文書と重なるという指摘。承認は止めなかった。ACD の名と識別子の問いは B6 |
| *"Let's give Microsoft a chance to submit these licenses on its own.  I think that the general principle should be that authors have preference over third parties when it comes to submitting licenses."*、*"Perhaps they have revisions to make?  If so, then approving draft licenses would be a serious wrongo."* | Russell Nelson 氏 2005-12-11 | 2 つの面。起草者が出すのが原則という線は、ACD では起草者が出す側なので当たらない。改訂が控えている版を承認するのは誤りだという線は、1.0 を `license-discuss` に出したまま 1.4 を作っている ACD に当たる。出す版を申請の日に確定する最新版とした計画（`OSI-APPROVAL-PLAN.md` §4）はこの線と同じ向きである |
| *"In order for the terms to be listed on the OSI website the copyright holder must necessarily be involved"*、*"anyone using the license must themselves have the right to copy the license."*、*"The copyright holder ought to be proposing the license for approval and stating an intention to use."* | Brendan Scott 氏 2005-12-11 | ACD は本文を写して配ることを誰にでも許す（§16.4）ので、2 つ目の問いには本文が答える。3 つ目の「使う意図」は B2 の側で、ACD の利用はこのリポジトリ 1 件である |

**読み。** 1 つのライセンスについて、list の弁護士が曖昧さを指摘し、別の参加者が同じ点を「OSD に適合するが単純すぎる」と述べ、提出者が曖昧さを認めた。それでも本文は変わらず、2 か月後に承認された。2017 年の Rick Moen 氏が挙げた書かれていない理由の 1 つ（*"unjustifiably opaque or ambiguous in its wording"*・`against.md` #248）は、少なくともこの時点では、OSD に関わらない曖昧さに対して承認を止める形では働いていない。

**逆側。** 提出者は Microsoft で、曖昧さは 1 つの条の 1 つの場面に限られ、提出者は意図を list に書いた。ACD の起草者は単独で、法律家の読みを持たず（B1）、§16.2 はすでにこの場面を語で扱っている。2007 年の扱いは、曖昧さが残っても通ったことを示すが、ACD の語の質が問われないことは示さない。

**この節が establish しないこと。** 理事会がこの曖昧さを議論したかは、このスレッドには無い。提出者が曖昧さを認めたうえで本文を 1 語も変えなかったことについて、審査者が変えないことを許したのか、問題にしなかったのかは記録から決まらない（portfolio-aa の指摘）。2011 年に Russ Nelson 氏は、承認済みの語でも今は承認できないことがあると書いた（`against.md` #239 の追記）ので、この記録を今の審査の予測には使わない。API の `approved` 欄は MS-RL と MS-PL のどちらも false を返すが、承認日の欄は埋まっている。この食い違いの理由は確かめていない。2005-12 のスレッドは、Cowan 氏が Nelson 氏に *"I defer to your vast expertise."* と返して終わる。これを取り下げと読むかは、この 1 文からは決まらない。

## 1.194 OSD 2 はライセンスでなく配られる物について述べる —— 2007 年の問いと答え（2026-11-12）

"inconsistency in OSD- software (#2) v. licenses/rights (every other plank)"（`license-discuss` 2007-07〜08・6 通・`rounds/2007-07-license-discuss-osd-2-inconsistency-observed.txt` に 2 通）。portfolio-9b の「決める側の文書の形」の一覧から読んだ。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"section 2 of the OSD is inconsistent with the rest of the document, since it speaks of qualities of specific software, rather than rights or qualities of a generic license."* | Luis Villa 氏 2007-07-31 | ライセンスの審査で OSD 2 をどう当てるかの問い |
| *"OSD #2 is more direct:  "Must be available in source form".  This is not inconsistency, though it is lack of parallelism."*、*"This prevents the claim that some opaque block of binary bits is Open Source because you have attached the BSD or similar permissive license to it."* | John Cowan 氏 2007-08-01 | **2 つの面。** 有利な面: ライセンスとしての ACD は OSD 2 を妨げない（`submission-osd.md` の OSD 2 の行。§4.2 は source の形での配布を許す）。不利な面: ACD を学習済みモデルの重みに付けて配っても、重みが「不透明なバイナリ」と読まれれば、ライセンスを付けただけでは open source にならない。これは ACD の本文の欠陥ではなく、配られる物の側の問いである（B15） |

**読み。** OSD 2 は、ライセンスが source の配布を妨げないかと、配られる物が source の形で手に入るかの 2 つを含む。ACD の審査で問われるのは前者で、ACD は満たす。後者は ACD を何に付けるかで決まり、重みの preferred form が何かは OSI の Open Source AI Definition の側の論点である。

**逆側。** 審査者が ACD の §6（学習と出力）を読んで、ライセンスが重みの配布を前提にしていると見れば、後者の問いをライセンスの審査に持ち込みうる。その場合の答えは、ACD は source の提供を求めも妨げもしない（§10.2 は *"make source available"* を求めないと書く）、というところまでで、重みが open source かは答えない。

**この節が establish しないこと。** 2007 年の 2 人の文で、OSI の判断ではない。Villa 氏の改訂案が採られたかは、このスレッドには無い。

## 1.195 理事会の側の 2018 年の 2 つの文 —— 変更を求めるのは OSD に反するときと、OSD に適うか曖昧なとき。新しいライセンスは独自の価値を問われる（2026-11-12）

"moving to an issue tracker"（`license-review` 2018-06・32 通・`rounds/2018-06-license-review-board-change-requests-and-unique-value-observed.txt` に 5 通）。portfolio-9b の「途中に決める側」の一覧（DECISION_EVENT で絞った 12 本）から読んだ。Allison Randal 氏は `opensource.org` の宛先から書いている。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"There are two general situations where the board requests or suggests changes to a license: - The text submitted does not comply with the OSD, so we can't approve it - The text submitted is ambiguous, and while it might comply with the OSD, it also might not, and so we can't approve it"* | Allison Randal 氏 2018-06-19 | **基準の文。** 曖昧さが承認を止めるのは、OSD に適うかどうかが曖昧なときである。2007 年の MS-RL（§1.193）で、OSD に関わらない曖昧さが承認を止めなかったことと食い違わない。ACD の語の質の問い（B13）のうち、承認を止めうるのは OSD に触れる部分（§5.2 の禁止、§11 の除外、§16.4 の名前の制限）だと読める |
| *"the ultimate responsibility of the board is to determine whether a license satisfies the OSD. So, we aren't just considering the opinions expressed on the list, we're also evaluating those opinions against a defined standard."* | Randal 氏 2018-06-19 | 有利な向き。list の意見は OSD という基準に当てて評価される。2025 年の理事会の文（`board-decisions.md` §2）と同じ線である |
| *"I'm a firm supporter of the license proliferation position that the OSI adopted over a decade ago, and we do continue to consider whether a new license is offering unique value."*、*"the law that open source licenses are built on keeps changing, so over time open source licenses will need to evolve to cope with a legal environment that the current licenses couldn't anticipate."* | Randal 氏 2018-06-19 | **両方の面。** 不利な面: 新しいライセンスは独自の価値を問われる（B10）。有利な面: 既存のライセンスが想定できなかった法の変化に応じることは、独自の価値の理由として理事の口から挙がっている。ACD が独自の価値として挙げるのは、機械学習と TDM の許諾、モデルと出力への特許許諾である（`comparison.md`） |
| *"There are actually only three useful licenses, a gift-style, a sharing-with-rules-style, and something in between."*、*"All else is embellishment."*、*"The license reviewers aren't waiting to be surprised by some worthy innovation in Open Source licensing. No such thing is coming"* | Bruce Perens 氏 2018-06-19 | **不利な面。** ACD は贈与の型に入り、その型には承認済みのもの（0BSD、MIT-0、Unlicense など）が在る。ACD の追加は飾りだと読まれうる。同じ日に Perens 氏は *"OK, so not just whether it passes the OSD but whether it provides any unique value, too."* と、Randal 氏の文を受けて書いた |

**読み。** 2018 年の理事会の側の文は 2 つの基準を述べる。1 つは OSD への適合で、曖昧さもこの基準に当てて扱われる。もう 1 つは独自の価値（増殖の方針）である。ACD の承認に向けた主張は、前者では語の明確さ、後者では既存のライセンスが想定できなかった法の変化（機械学習と TDM）への対応に置くことになる。Perens 氏の文は後者を正面から否定する立場で、ACD はその立場の審査者を説得する材料を持たない（贈与の型の飾りと読まれるか、新しい問いへの答えと読まれるかは、読み手が機械学習の許諾を新しい問いと見るかで決まる）。

**逆側。** Randal 氏の「法の変化に応じる」は、既存のライセンスの新しい版を想定した文で、新しい起草者の新しいライセンスを想定したものとは読めない。Perens 氏の「三つしかない」は 2018 年の個人の見解で、その後も新しいライセンスは承認されている（Blue Oak・2024、`reviewer-positions.md` の Blue Oak の節）。

**この節が establish しないこと。** Randal 氏の文はその時点の理事の説明で、規則の文書ではない。このスレッドは決める側の通（Randal 氏、Luis Villa 氏、Perens 氏、Chris Lamb 氏など）に絞って読んだ。他の通は読んでいない。

## 1.196 単独の非法律家の提出に、同じ審査者が 2026 年 6 月に書いたこと —— The Mutualist License（2026）（2026-11-12）

"The Mutualist License (MutuaL) v1.2"（`license-review` 2026-06・5 通・`rounds/2026-06-license-review-mutual-drafting-and-canons-observed.txt` に 3 通）。ACD を `license-discuss` に出す 2 か月前の、`license-review` への新しいライセンスの提出である。提出者の Kat Suricata 氏は、法律家でない読み手のための平易な言葉を目的に掲げ、見出しを「Generosity」「Clarity」「Foresight」のように付けた。portfolio-9b の「途中に決める側」の一覧から読んだ。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"A principle of contract law is that, when interpreting legal instruments, every word is necessary and meaningful and not "mere surplusage.""* | Pamela Chestek 氏 2026-06-08 | **不利な面。** ACD は確認のための重ね書き（§10.2 の列挙、§4.3 の「条件にしないもの」の列挙など）を持つ。語に全部意味があるとする原則の下では、列挙に無いものは外れると読まれうる |
| *"Not numbering paragraphs is a nightmare."*、*"What does "break copyright" mean?"* | Chestek 氏 2026-06-08 | ACD は条に番号を持ち、許諾は著作権法の語（reproduce, adapt, distribute 等）で書く。この 2 点は当たらない |
| *"Canons of contract interpretation do not save the day. They aren't invoked unless the language is unclear, so even having to invoke them means there is a chance that the legal conclusion about the meaning will not be what you intended."*、*"Using substitutes for well-known and well-understood terms of art is an invitation to misinterpretation."* | Chestek 氏 2026-06-09 | **不利な面。** ACD の §15.1（受領者に多く与える読みが勝つ）と §15.6 は解釈の規則を本文に持つ。この文の下では、規則を書くことは語の明確さの代わりにならない。`review-responses-boilerplate.md` Q22 の答え（意図の表明であって裁判所への指示ではない）は、この形の異議に直接は当たらない |
| *"you need domain expertise in this specific area reviewing your stuff or the real world will immediately pop your clever new idea"* | Rob Landley 氏 2026-06-08 | B1 そのもの。ACD も法律家の読みを持たない |
| *"It's not the writing style that is the problem, it is the inexactness with which it is done that is the problem."*、*"In my opinion this license is too poorly drafted to assure that will happen."* | Chestek 氏 2026-06-09 | 審査の基準の文。平易な文体は問題にされず（Blue Oak を例に挙げた）、問題は語の不正確さだと書いた |

**読み。** これは ACD と同じ形の提出（単独、法律家でない、新しいライセンス）への、ACD の投稿の直前の審査の記録で、書いたのは Pamela Chestek 氏である（同氏の過去の文は `against.md` に多く在る）。基準は文体ではなく語の正確さで、解釈の規則はそれを補わない、と明言された。ACD の §15 は規則を持つので、この基準に当てて読まれる。

**逆側。** ACD の列挙は、*"includes, without limitation"*（§4.2）や *"In particular"*（§4.3・§10.2）で例示であることを本文で示し、§15.5 が列挙を例示と定めるので、列挙に無いものは外れるという読みは弱い（ただし §15.5 も本文の中の規則なので、下の解釈の規則の逆側を同じく持つ）。ACD は MutuaL が指摘された点の多く（番号の無い段落、見出しの言い換え、*break copyright* のような法の語の置き換え）を持たない。定義語（Covered Rights、Computational Use など）は term of art の置き換えではなく、本文で定義を与えている。Chestek 氏の結論は MutuaL の本文についてのもので、ACD について述べたものではない。

**portfolio-aa の答えの形（2026-11-12）。** 本文は語で分岐を閉じる作業を、記録つきで続けている（`ACD-1.4-SECOND-CLARITY-TRIAL.md` の試作。同じ日の T56・T60 は代名詞の分岐を語で閉じた）。§15.1・§15.5・§15.6 は、語で閉じきれない場面の最後の受け皿で、語の代わりではない。この答えの逆側は Chestek 氏の文そのもの（受け皿が要る時点で、意図と違う結論の危険がある）と、ACD が長く、新しい定義語を持つことである。

**この節が establish しないこと。** MutuaL の審査の帰結は、このスレッドの 5 通には無い（2026-06-09 の通で終わる）。Chestek 氏の文は個人の見解で、委員会の判断ではない。§15.1 と §15.6 を外すかどうかの判断は、portfolio-aa の試作の手順に委ねた。

## 1.197 2019〜2020 年の 2 つの会話 —— 意図は明確に、ただし曖昧で広すぎる語でなく。list の通は moderation で落とされることがある（2026-11-12）

"Intimacy in open source (SSPL and AGPL)"（`license-discuss` 2019-01・34 通）と "Ethical open source licensing - Dual Licensing for Justice"（`license-discuss` 2020-02〜03・28 通）。どちらも決める側の通に絞って読んだ。4 通を `rounds/2019-01-to-2020-03-license-discuss-intent-precision-and-moderation-observed.txt` に置いた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The INTENT of the license must be clear, but not with words or phrases that are vague and too broad. They should say precisely what they mean"* | Lawrence Rosen 氏 2019-01-22 | §1.196 の Chestek 氏の基準と同じ線。ACD の §6（学習と出力）と §8.4 の語の広さが、この基準で読まれる |
| *"the ethical license proposals are fundamentally irreconcilable with the non-discrimination values in the OSD."* | Pamela Chestek 氏 2020-02-26 | 有利な向き。ACD は使い道や使う人を制限しない（§4.3）。倫理的な制限を持つ AI のライセンス（RAIL など）と ACD が分かれる点である（`comparison.md`） |
| *"Once we say that a license is OSD-compliant, anybody can distribute software under that license and say that it's open source."* | Russell Nelson 氏 2020-03-08 | 承認の効き目の文。承認されたライセンスの下の配布は open source と名乗れる。ACD が承認されれば、ACD を付けたモデルの重みも「open source のライセンスの下」と名乗れるようになり、`review-readings.md` §1.194 の OSD 2 の問い（重みが source の形か）が、承認の後の論点として残る |
| *"I would like to point out that the OSI rejected the email ESR sent that Gil quoted (which I have removed) and it did not get published to the list. It would be helpful if everyone could make sure when replying they aren't inadvertently subverting the moderation process."* | Pamela Chestek 氏（License Review Committee の委員長と署名）2020-02-26 | B14 の背景。list の個々の通が moderation で落とされることは 2020 年にも在り、それは OSI の創設に関わった人の通にも及んだ。我々の投稿のうち少なくとも 3 通が moderation で拒否されたこと（B14）は、この運用の中で起きている |

**読み。** 2019 年の Rosen 氏の文は、2026 年の Chestek 氏の基準（§1.196）の前に同じことを述べている。2020 年の 2 つの文は、ACD の有利な点（使い道を制限しない）と、承認の後に残る問い（承認されたライセンスを付けた物は open source と名乗れる）を示す。

**逆側。** 2020 年の moderation は、特定の個人の通の内容についての判断である。2026-09-09 の moderator の告知は、AI が大半を書いた投稿という種類についての方針で、同じ運用の延長と読むか、新しい方針と読むかは、この記録からは決まらない。

**この節が establish しないこと。** どちらの会話も、ライセンスの承認の審査ではない。Nelson 氏の文は、倫理的なソフトウェアの定義（ESD）への反論の中の一文である。

## 1.198 承認済みの語をそのまま使えば読む費用が下がる —— OVPL（2005）で委員長が求めた逐語の再利用と、それへの理事の反対（2026-11-12）

"Change ot topic, back to OVPL"（`license-discuss` 2005-08・65 通・決める側の通に絞って読んだ・`rounds/2005-08-license-discuss-ovpl-verbatim-reuse-observed.txt` に 6 通）。Open Vendor Public License は CDDL を下敷きにした提出で、委員長の Russell Nelson 氏は、CDDL への改善を OVPL から外し、CDDL の番号を保つよう求めた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"A license is written once and read many times. But a license is not read out of context."*、*"If you can read and understand a term in one license, and then see that the term is identically present in another license, that greatly reduces the cost of understanding that license. I'm asking for verbatim code reuse."* | Russell Nelson 氏（委員長）2005-08-29 | **不利な面（B13）。** ACD の多くの条は、承認済みのライセンスの語をそのまま使わず、新しく書いている。読む人は ACD の語を既知の語に当てて理解できず、読む費用が上がる。**逆側**: ACD も一部は承認済みの語の型を使う（§1.9 と §2.6 は Apache-2.0 §5 の *"intentionally submitted for inclusion in the Work"* の型。同じスレッドで Behlendorf 氏がこの §5 を引いている、§3.1 の留保は CC0 の型）。全部を逐語にできないのは、承認済みの本文に無い対象（学習、モデル、出力）を扱うからである |
| *"Admission of past mistakes is no reason to make new ones."* | Nelson 氏 2005-08-29 | `against.md` #239 と同じ線。承認済みに似た条が在ることは新しい条の理由にならない |
| *"I disagree with requirements for certification that go beyond conformance to the letter and spirit of OSD."*、*"Approve it and put it directly, immediately on your "not recommended" list if OSI wants to pass judgement on its quality."* | Brian Behlendorf 氏 2005-08-24・29 | **有利な面。** 承認は OSD への適合で決め、質の判断は承認の後の分類で示せばよい、という理事の立場。2025 年の理事会の文（`board-decisions.md` §2）と同じ向きで、20 年前から在った |
| *"That's the risk we take pushing back against license proliferation. We've been taking it for years"* | Nelson 氏 2005-08-30 | Behlendorf 氏の「OSD に適うのに認証しなければ陰謀説が出る」への答え。委員長は増殖への抵抗の費用を受け入れていた |

**読み。** 2005 年の委員長と理事は、承認の門を OSD だけに置くか、増殖への抵抗（逐語の再利用を求めることを含む）まで広げるかで分かれていた。ACD が新しく書いた語は、前者では問題にならず、後者では読む費用として数えられる。

**この節が establish しないこと。** OVPL の帰結はこの節では追っていない（`review-readings.md` の 3 基準の節と `board-decisions.md` を参照）。Nelson 氏の逐語の再利用の要求は、下敷きのライセンスが在る提出（CDDL の派生）についての文で、下敷きを持たない ACD に同じ形で当たるとは限らない。
