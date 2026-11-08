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
| *"Anything multiply licensed, where at least one license is OSI-compliant, is obviously open source."* | John Cowan 氏 2008-09-07（同じ報告の RTEMS についての返信、`license-discuss`） | B4。ACD の §4 の許諾が単独で OSD に適合すれば、§3 と §5 が並んでいても、オープンソースでなくなることはない、という読みの支え。**逆側**: Cowan 氏が述べたのは受領者が選ぶ二重許諾で、ACD の §2.4 の足場は選ぶものではなく重なって働く。個人の発言である |

**読み。** #302 は MirOS を「OSD に適合しても承認しない」の系譜に入れて引いていたが、MirOS は承認された。7 月の反対の記録と、9 月の勧告と、承認日は、別のスレッドと別の文書に分かれていた。議論の記録に帰結は無い（`reviewer-positions.md` §1.142 と同じ教訓）。2008 年の委員会は、差の小ささも、提出者が既存のライセンスを断ったことも、利用の少なさも理由にせず、OSD への適合で承認を勧め、推奨はしなかった。ACD の提出が狙えるのは、少なくともこの形である。

**この節が establish しないこと。** 2008 年の委員会の運用で、2025 年の理事会の文（B2 の「留め置き」）より 17 年前である。議事録は要約する道具で読んだもので、逐語の照合をしていない。7 月から 9 月の間に勧告が変わった理由は記録に見つからない。MirOS は BSD 型の短い許諾で、ACD の長さ（B3）や特許の許諾（B7）は問われていない。
