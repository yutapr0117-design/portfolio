---
file: LICENSES/ACD-1.0.review-readings-2.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-11-15
canonical-ref: LICENSES/ACD-1.0.review-readings.md (§1.164〜§1.217) / LICENSES/ACD-1.0.reviewer-positions.md / LICENSES/ACD-1.0.against.md
---

# 未読のスレッドと審査の帰結を読んだ記録（§1.218 以降）

`ACD-1.0.review-readings.md`（§1.164〜§1.217）が 1,000 行（Check 365）に届いたので、2026-11-15 から新しい節をここに置く。**既存の節は動かしていない**ので、他の文書が `review-readings.md` を名指して引く §1.164〜§1.217 の参照はそのまま元の文書で解決する。§1.xx は `ACD-1.0.*.md` の共有の採番で、この文書は §1.218 から続ける。

書き方は元の文書と同じである。どの節も、原文を引き、発言者と日付を書き、ACD への当たり方と逆側を同じ表に置き、最後に「この節が establish しないこと」を書く。引用の原文は `rounds/` に置く。

## 1.218 放棄し、放棄できない所では行使しないと約束し、虚偽の著者表示だけは除き、可分にする —— 人格権について Sado 氏・Chestek 氏・Perens 氏が示した形（PUWL・2025）（2026-11-15）

"[DISCUSS] PUWL v1.0"（`license-discuss` 2025-10・`rounds/2025-10-license-discuss-puwl-moral-rights-observed.txt` に 4 通）。単独の作者が出した public-domain 型のライセンスの草案で、人格権の扱いが論じられた。ドシエは PUWL を「crayon license」の例として引いていたが（`review-labels.md`）、人格権の条の形について決める側が示した案は引いていなかった。portfolio-1c の §12.4 の依頼で探した。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Contributor waives and agrees not to assert any moral rights (including rights of attribution, integrity, and disclosure) in the Work and Contributions. Where such waiver is not permitted, each Licensor and Contributor irrevocably covenants not to assert such rights and consents to all acts that would otherwise infringe them, including modification, combination, and omission of attribution, provided there is no false attribution of authorship. This provision is severable and survives to the extent enforceable in any jurisdiction."*、*"in Japanese software practice, a pure "waiver" rarely bites on its own."* | Shuji Sado 氏 2025-10-17（Open Source Group Japan の代表。Chestek 氏・Perens 氏の "belt-and-suspenders" を受けて） | **有利な面（B8・強い）。** 1.4 草案の §12 は同じ構造を持つ: §12.1 *"waives and agrees not to assert Moral Rights"*、§12.2 放棄できない法域では *"covenants not to exercise Moral Rights in the Work against You"*、§12.5 は虚偽の著者表示（§11.3）を約束の外に置き、§12.6 は可分（§15.2）。日本の実務を知る審査者の 1 人が、ACD の型と同じ形を自分から提案した。**差は 1 つ**: Sado 氏の案は *"consents to all acts that would otherwise infringe them"* という同意を持ち、ACD の §12.2 は約束だけで同意を書かない（試作の候補として portfolio-1c へ渡した。同意の理由は Sado 氏の通に書かれていない・下の逆側） |
| *"How about waiving all claims and promising not to assert moral or other rights in a lawsuit? Belt and suspenders :-)"*（Chestek 氏）への返信で *"Ah, but then we have severability."* | Bruce Perens 氏 2025-10-06 | 放棄と不行使の約束を重ね、可分の条で支える形を、2 人の決める側が支持した。§12.1・§12.2・§12.6 の重ね方と同じ |
| フランスの規定を引いて *"It is perpetual, inalienable and indefeasible. On the author's death it can be transmitted to his heirs. The exercise of this right can be transferred to a third person by testamentary disposition."* | Perens 氏 2025-10-06 | §12.4 は約束が *"heirs, personal representatives, and any person entitled to exercise or enforce Moral Rights in the Work after the Dedicator's death"* を *"to the fullest extent the law permits the Dedicator to bind them"* 縛ると書く。相続人と遺言で行使を受けた人の両方を名指す点で、Perens 氏の引いた規定の形に当たる |
| *"An affirmative grant would be a significant difference from cc0."*（特許について） | Perens 氏 2025-10-06 | **有利な面（B10）。** 特許の積極的な許諾が CC0 との大きな違いになると、決める側の 1 人が 2025 年に書いた。ACD の §8 はそれを持つ |
| *"I would also like to see an explanation of how all the other licenses that attempt to achieve this fail, and how this license has remedied their flaws."* | Pamela Chestek 氏 2025-10-06 | **B10 の要求。** 既存の試みがどう失敗し、新しいものがどう直したかの説明を求めた。`REVIEWERS.md` の "In one screen" と `submission-reference.md` の比較がこの形に答える |

**読み。** 2025 年 10 月に 3 人の審査者が人格権の条に示した形（放棄＋放棄できない所での不行使の約束＋虚偽の著者表示の除外＋可分）は、ACD の §12 の構造と一致する。日本法を知る Sado 氏が自分から同じ形を書いたことは、§12 を「範囲を広げすぎ」（B8 の一方の読み）ではなく「放棄だけでは効かない法域への備え」として読ませる材料になる。

**逆側。** Sado 氏の案は Contributor と Licensor を名指し、同意を含む。ACD の §12 は Dedicator の約束だけで、同意の語を持たない。**同意の出所について**: Sado 氏の通が日本の実務について述べるのは *"Where "natural persons" are the authors, practice relies on non-assertion covenants rather than blanket waivers."* と *"the broad permission to modify and create derivatives often functions in effect as a non-assertion of integrity-type claims"* で、同意が同一性保持権に効くとは書いていない。同意は案の文に在るだけで、その理由は通の中に無い。「同意を足せば約束より強い」は我々の推測で、日本の文献にも法律家にも当てていない（`QUESTIONS-FOR-COUNSEL.md` の候補）。また、PUWL そのものは「crayon license」と呼ばれた単独の草案で、決める側が示した形は PUWL を直すための助言であり、承認の基準ではない。B8 のもう一方の読み（人格権の条は mission creep）は、この会話では論じられていない。

**この節が establish しないこと。** 日本法とフランス法の内容は審査者の文の引用で、我々の法的な読みではない（`ACD-1.0.jurisdictions.md`）。

## 1.219 受け手が約束に依拠できると書くこと —— 承認済みの「受益者」の条は向きが逆で、審査者は「知らない受益者」と privity を問うた（2014〜2018）（2026-11-15）

portfolio-1c（T66・§5.3 の受益者に §8.6 を入れるか）と portfolio-30（SELF-AUDIT の「約束の依拠」の候補）の依頼で、全期間の決める側の通を *"third-party beneficiary"*・*"intended beneficiary"*・*"covenant not to"*・*"non-assert"*・*"privity"* で探した（63 通）。`rounds/2014-to-2018-license-review-third-party-beneficiary-privity-observed.txt` に 3 通。1.4 草案の §5.3 は、Dedicator の約束を *"may be relied upon by You and by anyone who receives the Work from You, directly or indirectly, as an intended beneficiary, to the extent a jurisdiction gives effect to such reliance"* と書く。

**承認済みのライセンスの「受益者」の条は、ACD と向きが逆だった。** CAL-1.0（2020 承認）は *"either the Licensor or a Recipient (as an intended third-party beneficiary) may enforce the terms and conditions of this License against You via specific performance"*、NOSA 1.3 は政府を受益者にする ——どちらも licensee に条件を守らせるための受益者である。CERN-OHL-2（2021 承認）§8.6 は逆に *"third party beneficiary rights are specifically excluded"*。下流の受け手が licensor の約束に依拠できると明示した承認済みの文は、この探し方では見つからなかった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Are you suggesting that there can be oblivious third party beneficiaries (under contract law!) of a software license who get their rights from infringers (under copyright law!)?"* | Lawrence Rosen 氏 2014-09-16（UPL の審査） | **不利な面（§5.3 と §2.3 の組み合わせ）。** ACD は受け手が Dedication を知らなくても許諾を持つとし（§2.3）、受け手を約束の受益者にする（§5.3）。「知らない受益者」が契約法の上で成り立つかを、2014 年の審査者が疑問として出している。ACD の §5.3 は *"to the extent a jurisdiction gives effect to such reliance"* と限り、§3 と §4 は §5.3 と独立に働く（最後の文）ので、受益者の構成が崩れても許諾は残る |
| *"Most FOSS licenses nowadays are not -- and need not be -- sublicenseable. They are directly licenses between a Licensor and a Licensee. That avoids all the confusing contractual rules about contract privity."* | Rosen 氏 2016-01-21（BSD+Patent の審査） | 直接の許諾が privity の問題を避ける、という読み。ACD は §1.6・§4.6 で直接の許諾を持つ（§1.208）。§5.3 の受益者の条は、直接の許諾が及ばない約束（訴えない約束）を下流へ届かせるための層で、Rosen 氏の言う「避けた問題」を約束の側で引き受けている |
| *"You might be missing that "third-party beneficiary" has a special meaning in contract law."*（NOSA 2.0 の政府を受益者にする条に） | Bruce Perens 氏 2018-03-02 | 受益者の語は契約法の特別な意味を持ち、審査者はその効果を問う。ACD の §5.3 は受益者が「依拠できる」ことだけを言い、受益者に何かを強制させる条ではない |

**読み。** 承認済みのライセンスが受益者の語を使うのは licensee に守らせる側で、ACD は受け手を守る側で使う。この向きは新しく、承認済みの先例が無い。審査者の疑問（知らない受益者、契約法の特別な意味）は ACD に当たりうるが、§5.3 は効果を法域に委ね、許諾（§3・§4）を受益者の構成から切り離している。

**逆側。** 先例が無いことは B10 の「新しい効果」の側に数えられるが、法律家の確かめの無い新しい構成でもある（B1）。§5.3 に §8.6 の約束を入れる T66 は、この新しい構成を特許の約束にも広げる。Rosen 氏の「知らない受益者」の疑問は、広げるほど当たる面が増える。

**この節が establish しないこと。** 63 通のうち決める側が受益者の向き（守る側か守らせる側か）を区別して論じた通は見つからなかった。探し方は語の照合で、言い換えた通は拾っていない。

## 1.220 直した版の出し方と差分の示し方 —— 新しいスレッドで、1 つの完全な文書で、変更は番号つきの一覧で（2018〜2026）（2026-11-15）

portfolio-50 の依頼（`REVISION-PROTOCOL.md` の 3.6 節の 6b で 1.4 を `license-discuss` に置くときの形、`SUBMISSION-MATERIALS.md` の「添えるもの」）で、2016 年以降の決める側の通を redline・差分・出し直し・新しいスレッド・変更の要約の語で探した（162 件の当たり）。`rounds/2023-to-2025-license-review-revised-versions-and-diffs-observed.txt` に 3 通。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"To avoid further delays, can you please start a new thread for the revised edition?"* | Josh Berkus 氏 2025-12-08（ModelGo の 2 度目の出し直し） | **形の指示。** 直した版は、前の版の会話への返信ではなく新しいスレッドで出す。1.4 を `license-discuss` に置くなら、1.0 の 2026-08-26 の投稿への返信でなく、新しい件名で出す形になる |
| *"we much have the complete, correct version to be approved as one document. It is too confusing and the recordkeeping too difficult to have multiple documents that are supposed to represent a single license."*、*"That is one reason we much have in our records the exact version of what is to be approved, so others will have an immutable source of truth about the actual license text that was approved."* | Pamela Chestek 氏 2025-02-10（委員長・Mulan PSL v2） | **形の要件。** 差分（redline）だけでなく、完全な本文を 1 つの文書で出す。差分は添えるもので、本文の代わりにならない。ACD の凍結（`FROZEN.md`）と版ごとの 1 ファイルは「変わらない本文」の求めと同じ向き（有利） |
| *"The license submitter summarized the changes as follows: 1. …"*（提出者が番号つきで書いた変更の一覧を、委員会の理由書がそのまま引いた） | Chestek 氏 2023-11-12（委員会の理由書・Unicode License v3） | **有利な先例。** 旧版の後継を出すとき、提出者が変更を番号つきの短い一覧で示すと、委員会の理由書にその一覧がそのまま入った。ACD の 1.4 草案の冒頭の変更一覧（errata の番号と語数つき）は同じ形で、1.0 → 1.4 の差として出せる |

**同じ探索から、形について 3 つ（原文はアーカイブの月）。** (1) McCoy Smith 氏 2023-08-30（Unicode v3）は添付つきの通が一部の購読者に届かなかったとして再送し、*"I'm not including the attachments which might be the cause of the problem. If anyone is interested in a redline contact me directly."* と書いた ——添付は配信を妨げうる。ACD の 2026-09 の投稿が moderation で落とされた件（`FROZEN.md`）とは理由が別だが、添付に頼らず本文とリンクで示す方が届く。(2) Smith 氏 2026-09-07（ModelGo）は 2 つの版の redline を自分で作り、GitHub に置いてリンクで示した ——審査者自身が差分をリンクで配っている。(3) 2018-12 の委員会報告の要約（Lukas Atkinson 氏 2019-01-07）は SSPL について *"discussion will continue on the revised version"* と書いた ——直した版は審査の続きとして扱われた。

**読み。** 決める側が直した版に求めた形は、新しいスレッド（Berkus 氏）、1 つの完全な本文（Chestek 氏）、変更の短い一覧（Unicode の理由書）、添付でなくリンク（Smith 氏）である。ACD が 1.4 を `license-discuss` に置くなら、件名を新しくし、本文の全文を 1 ファイルで示し、1.0 からの変更を番号つきの一覧で添え、redline はリンクで置く形が、これらの先例に合う。

**逆側。** これらは `license-review` の提出（審査の続き）での形で、`license-discuss` の意見募集でどう受け取られるかは別の問いである。また、1.0 → 1.4 の変更は errata の数だけで数十件あり、Unicode の一覧（数件）とは量が違う。量が多い一覧は、それ自体が「審査の途中で大きく書き直した」（`against.md` #249 の費用）と読まれうる。AI の関与の開示への決める側の反応（portfolio-50 の依頼 (2)）は、2023 年以降の通で、開示した提出に決める側が答えた例を見つけられなかった（moderator の告知・`against.md` #292 の "AI slop"・§1.206 の Chestek 氏自身の AI の比較だけ）。

**この節が establish しないこと。** 探索は語の照合で、言い換えた通は拾っていない。どの形が承認の確率に効くかは示していない。

## 1.221 書いた本人が説明し、直す意思を示す —— 「代理人はうまくいかなかった」「受け入れるか否かなら否」（Chestek 氏 2020）と、3 年後の「審査は直す場ではない」（2023）（2026-11-15）

"Resources to discourage governments from bespoke licenses?"（`license-discuss` 2020-02〜03・`rounds/2020-02-license-discuss-authors-explain-not-proxies-observed.txt` に 1 通）。米陸軍研究所の担当者が、政府の法律家は匿名のまま提出したいと述べたのに、当時の委員長が答えた。2024〜2026 年の照合で決める側の未引用の通に出た会話の 1 つ。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The licenses are discussed publicly, so the people who wrote the license are ideally the ones explaining it to the license-review list because they know the ins and outs. We've had proxies participate in the past and it doesn't go well."* | Pamela Chestek 氏 2020-02-28（License Review Committee の委員長） | **不利な面（B14・B1）。** 審査で説明するのは書いた本人が望ましく、代理人はうまくいかなかった、という委員長の経験である。ACD の本文は AI が起草し、人間（オーナー）が設計と判断を担った。list で問われたとき、条の「ins and outs」を自分の言葉で答えるのはオーナーで、AI が答えの文を書いて送れば代理人の形になり、moderator の告知（B14）にも当たる。オーナーが自分で説明できる範囲が、審査で答えられる範囲になる |
| *"There also needs to be some willingness to modify the license based on feedback. The license may last to perpetuity, so it needs to be really well written. If it's presented to license-review as "take it or leave it," the outcome for a newly written license is likely going to be "leave it.""* | Chestek 氏 2020-02-28 | **両面。** 直す意思が要る。ACD は凍結した版を審査中に変えない（`FROZEN.md`）が、欠陥は errata に記録して次の版で直し、1.1〜1.4 と版を重ねてきた。直す意思はこの記録で示せる（有利）。だが「凍結しているので直さない」とだけ読まれれば「受け入れるか否か」の形に見える（不利）。2026 年の Chestek 氏は、提出した文は変えられず取り下げと再提出になると書いた（§1.206）——直す意思は、審査中の本文の変更ではなく、版の出し直しで示す形が今の手順に合う |
| *"The anonymous lawyers should think of the license-review process as a really great tool for improving their work product. … so that the ultimately approved license is much higher quality than the originally submitted license."* | Chestek 氏 2020-02-28 | **時点の違いに注意。** 2020 年の委員長は審査を本文を良くする道具と見ていた。同じ人が 2023-08-22 に *"The license review process is not for workshopping a license, it is for a go/no-go on a license."* と書いた（`against.md` #298）。審査の役割の読みは 3 年で「直す場」から「可否の場」へ移っている。ACD の手順（`license-discuss` で固めてから `license-review` へ・§1.206 の 30 日）は後者に合わせた形である |

**読み。** 2020 年の委員長は、書いた本人が説明し、直す意思を示すことを求めた。2023 年以降は、直すのは `license-discuss` と版の出し直しの側で、`license-review` は可否の場になった。ACD はこの移り変わりの後の手順に合わせている（凍結・errata・次の版）。残る問いは「書いた本人」で、ACD ではそれがオーナーであり、オーナーが審査の問いに自分の言葉で答えられることが、代理人の形を避ける条件になる。

**逆側。** 「書いた本人」を「設計と判断をした人」と読めばオーナーは本人だが、「本文の語を書いた人」と読めば AI である。後者の読みで審査者が問えば、ACD は代理人の形に見える（`ACD-OSI-BOTTLENECKS.md` B14）。開示はこの点を隠さないが、開示が懸念を消すとは限らない（§1.220 で開示への決める側の反応の例は見つからなかった）。

**この節が establish しないこと。** 2020 年の文は匿名の政府の法律家についてで、AI の関与についてではない。「代理人」の範囲に AI の起草が入るかは、決める側の誰も述べていない。

## 1.222 2026 年の新しい提出が最初に受ける問い —— 元のライセンスと何が違うか、使う（使うと表明する）プロジェクトはあるか、手順の項目は揃っているか（2026）（2026-11-15）

2026 年の `license-review` の 2 つの提出に付いた決める側の通（`rounds/2026-03-to-04-license-review-first-questions-observed.txt` に 2 通）。どちらも 2024〜2026 年の照合で決める側の未引用の通に出た。ACD を `license-review` に出したときに最初に来る問いの、今の形の実例として置く。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Other than translating the ISC text and changing the license name, is there is any difference from the originating license? Would you please discuss the substantive changes, if any?"*、*"Also, is there any project actually using or signalling it will be using the license if/when approved?"*、*"Finally, have you checked all the boxes in https://opensource.org/licenses/review-process, is there an part missing other than than the two queries above?"* | Carlo Piana 氏 2026-04-17（委員・ISC を基にしたロシア語のライセンスの提出への最初の返信） | **最初の 3 つの問いの実例。** (1) 元のライセンスとの実質的な差（ACD は「承認済みのどれとも違う効果」を `REVIEWERS.md` の "In one screen" と §1.205〜§1.206 の逐語の比較で答える）、(2) 使う、または使うと表明しているプロジェクト（ACD はこのリポジトリ 1 件・B2。「表明する」も数えると書いてあるので、オーナーが関心の表明を集める窓口〔`.github/ISSUE_TEMPLATE/acd-use.yml`〕の意味がここに在る）、(3) 審査手順の項目の充足（`SUBMISSION-MATERIALS.md`・REVISION-PROTOCOL の表の 8） |
| *"I don't understand what you're expecting to accomplish with this license."*、*"Licenses aren't tools for social engineering. If you're trying to build a commercially and technically successful community, clever license terms aren't going to do that for you."* | Josh Berkus 氏 2026-03-17（理事・Modified 0BSD への返信。Chestek 氏が同日 *"IMO this license should be rejected for the reasons that Josh gives."*） | **目的の問い。** 何を達成したいかを最初に問われ、ライセンスは社会的な目的の道具ではないと言われた。ACD の目的（学ばれるための作品に、確かめなくてよい許諾を与える・§6.5）は条件で人を動かすものではないが、「何を達成したいか」に 1 文で答えられる形が要る（`REVIEWERS.md` の "In one screen" の最初の行） |

**読み。** 2026 年の新しい提出への最初の返信は、差・使用・手順の 3 点と、目的の 1 点を問うた。ACD の入口はこの 4 点に答える場所を持つが、(2) の使用だけは「このリポジトリ 1 件」以外の答えを持たない。Piana 氏の問いは「使うと表明している」プロジェクトも数えるので、承認の前に関心の表明を集めることは、問いの形そのものに合う。

**逆側。** 2 つの提出はどちらも退けられた側（ISC の翻訳はほぼ同じ文、Modified 0BSD は Chestek 氏が否決を勧めた）で、最初の問いが同じでも ACD の扱いが同じになるとは限らない。使用の問いは、委員会の理由書が「基準ではない」とした問い（§1.201、MIT-0・Jam）を委員が最初に訊いていることを示し、規則と実際の問いの順の間にずれがある（B2）。

**この節が establish しないこと。** 2 つの提出の帰結は扱わない。Piana 氏の 3 つの問いが毎回同じ形で来るかは、この 1 通からは分からない。

## 1.223 多段階の承認、まず license-discuss、問いは「OSD に合うか」と「既存の全てと十分に違うか」—— 2013 年の「起草の質と手順」の議論（2026-11-15）

"License drafting quality and process"（`license-review` 2013-04〜06・32 通・決める側の未引用の通 7 通・`rounds/2013-06-license-review-drafting-quality-and-process-observed.txt` に 5 通）。census の会話の一覧にも READ-THREADS にも行が無く、ドシエは同じ会話の Berkus 氏の *"it happens afterwards"*（法律家のレビューは提出の前か後か）と Fontana 氏の「支持者が複数いる」提案だけを引いていた。portfolio-9b が census に入れた通単位の面で見つけた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I think there would be significant non-proliferation benefit to having a multi-stage approval process for new licenses, an important part of which could be license-discuss."*、問いは *"(1) does the license fit the OSD? (2) is it sufficiently different from all existing licenses?"* | Josh Berkus 氏 2013-06-05 | **手順と問いの形。** 新しいライセンスは `license-discuss` を含む多段階で、問いは OSD への適合と既存の全てとの十分な差の 2 つ、と 2013 年に書かれた。2026 年の Chestek 氏の「`license-discuss` に 30 日」（§1.206）と Piana 氏の最初の問い（§1.222）は、この形の続きに見える。ACD の入口は (1) を `submission-osd.md`、(2) を "In one screen" で答える |
| *"Requiring evidence of 100+ projects using a proposed license will have the same chilling effect against further reform and evolution of open source licensing. There is a bit of a chicken/egg problem, as the absence of OSI approval may significantly deter projects *independent of the steward* from choosing the new license."* | Richard Fontana 氏 2013-06-06 | **有利な面（B2）。** 使用の数を要件にすると新しいライセンスを止めてしまい、承認が無いこと自体が採用を妨げる、という鶏と卵の指摘である。2015 年の同じ人の委員会報告（使用の要素を採らずに承認・§1.216）と同じ線で、B2 の「使用は基準でない」の支えが 2013 年まで遡る |
| *"it is quite possible to submit a license that complies with all our formal requirements without improving the overall ecosystem, and we have no formal way to say no to those."* | Luis Villa 氏 2013-06-06 | **不利な面（B10）。** 形式の要件を満たしても生態系を良くしないライセンスを断る手段が無い、という当時の委員の不満である。2025 年の理事会の「留め置き」の形（`board-decisions.md`）は、この不満への後年の答えと読める |
| *"the only licenses we've approved in the last year were new versions of old approved licenses. Every other proposed license we've seen has been rejected as either (a) not OSD-compliant, or (b) very poorly conceived and written, or (c) wholly duplicative of an existing license."* | Berkus 氏 2013-06-12 | **不利な面（基準率）。** 2012〜13 年に新しく書かれたライセンスは、既存の新版を除いてすべて退けられ、理由は OSD 不適合・起草の質・重複の 3 つだった。ACD が当たりうるのは (b)（B1・B3・B13）と (c)（B10） |
| *"To be clear, this is now official policy. Submissions to license-review that aren't quite compliant with the submissions policy will be politely rejected until you come back with a better one."* | Villa 氏 2013-06-13 | 提出の形式（必要な情報）を満たさない提出は内容を見る前に退ける、が 2013 年に方針になった。ACD の `SUBMISSION-MATERIALS.md` と REVISION-PROTOCOL の表の 8 がこれに当たる |

**読み。** 2013 年の議論は、新しいライセンスの承認の形を「まず `license-discuss`、問いは OSD と十分な差、形式の不備は門前で戻す」に寄せ、使用の数を要件にする案は鶏と卵として退けた。今の手順（2026 年の 30 日、最初の問い、形式の要件）はこの線の上に在る。ACD の手順（`license-discuss` に 1.0 を置き、版を出し直し、入口で差を示す）は、この形に合っている。

**逆側。** 同じ会話の基準率は厳しい: 2012〜13 年の新しいライセンスは既存の新版を除いて全部退けられた。理由の (b) 起草の質と (c) 重複は、ACD の B1・B3・B13 と B10 にそのまま当たる。Villa 氏の「断る手段が無い」は、後に理事会が留め置きの形で手段を持ったことで解けており、その手段は ACD にも使われうる。

**この節が establish しないこと。** 2013 年の Berkus 氏の多段階の案が正式な手順になったかは、この会話からは分からない。基準率は 2012〜13 年の 1 年の Berkus 氏の数え方で、我々は数え直していない。

## 1.224 効果が重複するライセンスは、判例の新しい展開に応じるか明白な法的欠陥を解く場合を除いて受け入れない —— Perens 氏の「提出者への注意書き」（2018）（2026-11-15）

"Some notes for license submitters"（`license-review` 2018-06・`rounds/2018-06-license-review-perens-notes-for-submitters-observed.txt` に 1 通）。ドシエは同じ会話の Allison Randal 氏の「法が変わるのでライセンスも変わる必要がある」を §1.195 で引いていたが、会話の起点になった Perens 氏の注意書きは引いていなかった。Perens 氏は冒頭で *"These are not OSI rules"* と断っている。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"licenses that are duplicative of other licenses in their effect should not be accepted any longer, unless it's to meet new developments in case law or solve an obvious legal deficit."* | Bruce Perens 氏 2018-06-12 | **有利な面（B10・基準の形）。** 重複の例外を 2 つ名指している ——判例（法）の新しい展開に応じること、明白な法的欠陥を解くこと。ACD の差の主張は、この 2 つの形で言える: 機械学習と TDM をめぐる法の新しい展開（EU の Art. 4(3) の留保・§6）、承認されなかった CC0 の明白な欠陥（特許の除外・§8）。§1.195 の Randal 氏の同じ日の文（法が変わるのでライセンスも変わる）と組で、「法の変化と欠陥に応じる新しいライセンス」の居場所を 2 人の決める側が認めている |
| *"A license is a sort of program designed to be executed by the courts. If you have not made use of an attorney in drafting your license, you are very unlikely to understand how the courts would actually execute your license."* | Perens 氏 2018-06-12 | **不利な面（B1）。** §1.205（2026）・§1.213（2012）と同じ人の同じ向きの文で、2012・2018・2026 年と一貫している |
| *"If your license doesn't consider the broader developer community and its needs, it's difficult to see why OSI should approve it."*、*"A whole category of licenses has been submitted to push the boundaries of Open Source beyond what was intended in the writing of the Open Source Definition."* | Perens 氏 2018-06-12 | ACD は何も制限せず、提出する組織の都合で受け手を縛らないので、「境界を押し広げる」類型（使用の制限・事業の方法）には入らない（有利）。受け手の側の必要（確かめずに学習に使える）を目的に書いている（§6.5） |

**読み。** 2018 年の Perens 氏は、新しいライセンスを原則として要らないとしつつ、例外を「法の新しい展開」と「明白な法的欠陥」に置いた。ACD の差の言い方を、この 2 つの例外の語に合わせて書けば、審査者が既に持っている枠で読める。

**逆側。** 例外は「判例の新しい展開」（case law）と書かれていて、ACD が依る EU 指令の留保は判例ではなく立法である。機械学習の著作権をめぐる判例はまだ固まっていない（§1.211 の Smith 氏・Villa 氏）。また Perens 氏は同じ通で法律家の関与を前提にしており、例外に当たるかを判断するのも法律家の読みだと考えている。

**この節が establish しないこと。** Perens 氏の注意書きは OSI の規則ではない（本人が断っている）。2018 年以降、この 2 つの例外が委員会の理由書で使われたかは確かめていない。

## 1.225 個々の部分に権利が在るかに関わらず作品全体に許諾する、プログラムの一部は機械の仕事 —— NOSA 2.0 をめぐる Perens 氏と Cowan 氏（2018）（2026-11-15）

"NOSA 2.0 and Government licensing"（`license-review` 2018-06・`rounds/2018-06-license-review-nosa-whole-work-machine-portions-observed.txt` に 2 通）。NASA の独自ライセンス（NOSA 2.0）は、理事会が 2017 年に長さ・複雑さ・曖昧さを理由に承認も却下もできないとした（`against.md` #183）。その後の会話で、政府の作品が米国でパブリックドメインであることをどう扱うかが論じられた。通単位の未引用の会話を ACD の語の濃さで並べた最上位だった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"There is also the matter that much of the work in computer programs is not an original work or authorship (for example, some of it is the work of a machine) and thus can not be copyrighted. These portions are in the public domain."*、*"We take care of this in our licenses by granting permissions on the entire work, whether or not we actually have rights to grant on any particular part. And yet there has been no attack of an Open Source license on a severability basis that I know of. NASA can do the same thing, and grant permissions regarding the entire work. Or alternatively they can actually dedicate the public domain works to the public domain, removing the ambiguity of where they are and are not public domain."* | Bruce Perens 氏 2018-06-20 | **有利な面（§9・強い）。** 2018 年の決める側の 1 人が、プログラムの一部は機械の仕事で著作物でないと名指し、その扱い方を「部分ごとに権利が在るかに関わらず作品全体に許諾する」「または放棄して曖昧さを除く」と書いた。1.4 草案の §9 はまさにこの形で、§9.2 は権利が無い部分には何も足さず何も取らないとし、§9.3 は受け手がどの部分が機械の生成かを決めなくてよいとし、§3 は放棄、§4 は作品全体への許諾である。§1.207（米国政府の作品・Smith 氏）と同じ線の、機械の仕事を明示した版 |
| *"U.S. government-created software … is in the public domain in the U.S. only. In all other jurisdictions, it is fully protected by U.S. and foreign copyright. So a license is required to cover the remaining 98% of the planet, and this license has to be a single integrated instrument, not the disjunction of two potentially severable licenses."* | John Cowan 氏 2018-06-20 | **両面（B4）。** 有利: 一方の法域で権利が無くても他では在り、許諾が要るという形は、ACD が §3 と §4 を並べる理由と同じ。注意: Cowan 氏は「1 つに統合された文書」であって「切り離しうる 2 つのライセンスの並び」でないことを求めた。ACD は 1 つの文書だが、§2.4 は §3・§4・§5・§6 を互いに独立させ、§4.4 は許諾を放棄から独立させる。独立を「切り離しうる並び」と読む審査者には B4（放棄と許諾が並ぶ構造）の懸念に見えうる。ACD の答えは、独立は「一方が倒れても他方が立つ」ためで、受け手から見て 1 つの文書の 1 つの効果だということ |

**読み。** 2018 年の 2 人は、権利の無い部分（政府の作品・機械の仕事・機能的な部分）を含む作品の扱い方を 2 つ示した。作品全体に許諾する（Perens 氏）か、放棄して曖昧さを除く（同）か、そして許諾は 1 つの統合された文書で（Cowan 氏）。ACD は両方を 1 つの文書に持つ。

**逆側。** Perens 氏は「または」と書いた ——全体への許諾か放棄かの一方で足りる、という読みもでき、両方を持つ ACD は余分と見られうる（B3）。Cowan 氏の「切り離しうる 2 つの並びでなく」は、ACD の §2.4 の独立の書き方への疑問として当たりうる。NOSA 2.0 自体は長さと複雑さで止まった（#183）ので、この会話の 2 人の形を持っていても長さの問題は別に残る。

**この節が establish しないこと。** Perens 氏の「機械の仕事」は 2018 年の文で、今の生成 AI を念頭に置いたものではない。「切り離しうる」が §2.4 の独立を指すかは、Cowan 氏は述べていない（NOSA の文脈）。
