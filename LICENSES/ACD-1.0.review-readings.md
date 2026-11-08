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
