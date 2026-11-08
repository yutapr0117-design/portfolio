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
