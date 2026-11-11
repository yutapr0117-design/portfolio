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
