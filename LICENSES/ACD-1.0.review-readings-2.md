---
file: LICENSES/ACD-1.0.review-readings-2.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-11-15
reachable-via: ACD-1.0.review-readings.md
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
| *"Most FOSS licenses nowadays are not -- and need not be -- sublicenseable. They are directly licenses between a Licensor and a Licensee. That avoids all the confusing contractual rules about contract privity."* | Rosen 氏 2016-01-21（BSD+Patent の審査） | 直接の許諾が privity の問題を避ける、という読み。ACD は 1.4 草案の §1.6・§4.6 で直接の許諾を持つ（§1.208）。§5.3 の受益者の条は、直接の許諾が及ばない約束（訴えない約束）を下流へ届かせるための層で、Rosen 氏の言う「避けた問題」を約束の側で引き受けている |
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

## 1.226 改変した本文には名前を変えさせる、Steward の役割は譲れる —— 承認済みの MPL 2.0 §10.3 と CPL・EPL の形、名前の保護は商標の仕事という見方（1999〜2011）（2026-11-15）

portfolio-1c の依頼（1.4 草案の §16.4 の名前と識別子の規律、§16.5 の Steward の定義に、承認済みの先例と審査者の文を当てる）で、全期間の決める側の通を探した。`rounds/1999-to-2010-license-discuss-licence-name-and-steward-assignment-observed.txt` に 4 通。

| 発言・文 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| MPL 2.0 §10.3 *"If you create software not governed by this License, and you want to create a new license for such software, you may create and use a modified version of this License if you rename the license and remove any references to the name of the license steward (except to note that such modified license differs from this License)."*（Luis Villa 氏が 2010〜2011 に `license-review` で提出し、承認された本文。アーカイブの月 2011-August・2011-December） | Mozilla（Villa 氏の提出） | **有利な面（§16.4）。** 改変した本文に名前を変えさせる条は、承認済みのライセンスに在る。1.4 草案の §16.4 は改変した本文を *"Autonomous Commons Dedication"* を含む名や *"ACD-"* に数字が続く識別子で、大文字小文字を問わず頒布することを禁じる。**逆側**: ACD は MPL より広い（名前を含む任意の名・大小を問わない）。この広げ方を論じた決める側の通は見つからなかった |
| *"If you've modified the Artistic license, you should probably not call it "ARTISTIC" at all, so that you avoid confusion with the unmodified Artistic license."* | Bruce Perens 氏 1999-09-23 | 改変した本文に元の名を使うなという、名前の規律の早い例。混同を避けるという理由は §16.4 の *"so that each name and identifier in this family continues to denote one fixed text"* と同じ向き |
| *"One more time, let me explain that OSI protects its certification marks by trademark law, not copyright licenses, and you should consider doing the same to protect the name of your product."* | Lawrence E. Rosen 氏 2002-10-08 | **不利な面になりうる。** 名前は商標法で守り、著作権のライセンスで守るものではない、という見方である（対象は製品の名で、ライセンスの名ではない）。ACD の §16.4 は名前の規律をライセンスの本文（文書としての扱い・§16.6）に置く。MPL 2.0 も同じく本文に置いているので承認の妨げにはなっていないが、Rosen 氏の型の審査者には「商標の仕事を本文でしている」と見えうる |
| CPL-1.0 *"IBM is the initial Agreement Steward. IBM may assign the responsibility to serve as the Agreement Steward to a suitable separate entity."*（Fontana 氏が引用）、Artistic 2.0 への提案 *""License Steward" means The Perl Foundation or its assignee under clause 15"*（Cowan 氏が CPL から借りて提案） | Richard Fontana 氏 2010-09-06・John Cowan 氏 2007-03-14 | **有利な面（§16.5・B12）。** Steward の役割を別の者へ譲れる形は、承認済みの CPL-1.0（と同型の EPL-1.0）に在り、決める側の 1 人が別の提出にその形を勧めた。1.4 草案の §16.5 は Steward を *"the person or entity to whom that role was last assigned by the person or entity then holding that role"* と定め、譲渡の形を持つ |

**読み。** §16.4 と §16.5 の形は、どちらも承認済みのライセンスに先例が在る（MPL 2.0 §10.3・CPL-1.0 と EPL-1.0）。ACD はそれより広く書いている点（名前を含む任意の名、大小を問わない）だけが先例の外で、その広げ方を審査者が論じた記録は無い。

**逆側。** 先例の MPL・CPL・EPL の Steward は大きな組織（Mozilla・IBM・Eclipse）で、ACD の Steward は個人である（B12）。譲渡の形が在っても、譲る相手がいるかは別の問いである。Rosen 氏の「名前は商標で守る」は、名前の規律を本文に置くこと自体への疑問として当たりうる。

**この節が establish しないこと。** MPL 2.0 §10.3 の承認の過程でこの条が論じられたかは読んでいない。CPL・EPL の Steward の条が承認の理由に挙がったかも確かめていない。

## 1.227 権利が移っても、倒産しても、約束は残る —— OWFa の 3 つの条を Rosen 氏が示した（2013）（2026-11-15）

"Open Source Eventually License Development"（`license-discuss` 2013-08・`rounds/2013-08-license-discuss-owfa-successors-bankruptcy-observed.txt` に 1 通）。portfolio-1c の依頼（1.4 草案の §2.8 で、権利が移った後も許諾が残ることを本文で述べた先例）の探索で見つけた。決める側の通に 17 U.S.C. §205(e) を論じたものは無かったが、同じ問いに法律家が起草の形で答えた通が在った。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| Eben Moglen 氏の「ライセンスは倒産などで終わりうる」に対し、OWFa の条を引いて *"the Open Web Foundation Agreement ("OWFa") deals directly with the fact that copyrights and patents can change ownership (voluntarily or involuntarily)"*、3.1.3 *"Notwithstanding the personal nature of my promise, this promise is intended to be binding on any future owner, assignee or exclusive licensee who has been given the right to enforce any Granted Claims against third parties."* | Lawrence Rosen 氏 2013-08-18 | **有利な面（§2.8・起草の先例）。** 権利が移った後も約束を将来の所有者・譲受人に及ぼす形は、法律家（Rosen 氏）が起草した文書に在る。1.4 草案の §2.8 は *"binds the Dedicator's successors, assigns, heirs, and personal representatives, and any person to whom a Covered Right or a patent claim in the Work is transferred"* と書き、同じ形である |
| 3.1.4 *"Solely for purposes of Section 365(n) of Title 11, United States Bankruptcy Code and any equivalent law in any foreign jurisdiction, this promise will be treated as if it were a license and you may elect to retain your rights under this promise if I … as a debtor in possession, or a bankruptcy trustee, reject this non-assert."* | Rosen 氏 2013-08-18（OWFa の引用） | **有利な面と差（§2.9）。** 倒産で約束が止まらない形の先例。1.4 草案の §2.9 は「倒産・管財などで止まらず、管財人は §2.8 の譲受人に当たる」と一般の語で書き、365(n) を名指さない。OWFa は約束（non-assert）を許諾として扱うと書いて 365(n) の保護に入れている。ACD の §5 の約束（訴えない約束）に同じ扱いを書くかは、試作の候補になりうる（portfolio-1c へ） |
| 6 *"I agree that I will not intentionally take or willfully assist any third party to take any action for the purpose of circumventing my obligations under this CLA."*、*"Could a court invalidate this license? Yes, it would have the authority to do so. Is that likely? No."* | Rosen 氏 2013-08-18（OWFa の引用と本人の評価） | §5.1 の *"not to authorise or assist any other person to assert"* と同じ向き。Rosen 氏は裁判所が無効にしうることを認めつつ、ありそうにないとした |

**読み。** ACD の §2.8・§2.9・§5.1 の 3 つの形は、2013 年に法律家が起草した OWFa の 3.1.3・3.1.4・6 とほぼ同じ並びである。ACD は法律家の確認を持たない（B1）が、同じ問題に法律家が出した答えの形をなぞっている、と言える。

**逆側。** OWFa は仕様への貢献のための合意（CLA に近い文書）で、OSI が承認したライセンスではない。承認の先例ではなく起草の先例である。また OWFa は 365(n) を名指して約束を許諾として扱い、ACD はそれを書かない ——ACD の §2.9 の一般の語が米国の倒産手続きで同じ効果を持つかは、法律家に当てていない（`QUESTIONS-FOR-COUNSEL.md` の候補）。

**この節が establish しないこと。** Moglen 氏の主張の全体と、会話の帰結は読んでいない。決める側の通に §205(e) の議論が無かったことは、語の照合による。

## 1.228 不透明でも善意だから通したのは誤りだった、関心を持つ人を紹介してほしい —— License Zero Reciprocal の審査の後で（2018）（2026-11-15）

"Consensus on L0-R"（`license-review` 2018-06・14 通・`rounds/2018-06-license-review-l0r-cowan-rpl-observed.txt` と `rounds/2018-06-license-review-l0r-perens-interest-observed.txt` に 1 通ずつ）。法律家の Kyle Mitchell 氏が単独で提出した License Zero Reciprocal（L0-R）の審査が止まった後の会話で、通単位の未引用の会話の上位に出た。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I believe that RPL's certification was wrongly decided, although it is probably too late to reverse it now. I remember thinking at the time that the license was very hard to understand (I don't find it so now, particularly), but that it meant well and we probably should approve it despite its opacity. I wish now that I'd made more fuss then."* | John Cowan 氏 2018-06-20 | **不利な面（B3・B13）。** 分かりにくくても善意なら通す、という過去の判断を、通した側の 1 人が誤りだったと書いた。決める側は不透明さに過去より厳しくなっている、と読める。ACD の長さと理由の文の多さ（B3）は「分かりにくい」の側に読まれうる。2016 年の Fontana 氏の「読めなければ適合しないと推定する」（§1.209）、2026 年の理事会の Project Tick の否決（§1.205）と同じ向き |
| *"However, when I asked you to introduce me to someone who was interested in the license, no names were forthcoming. So, I have to believe this is only theoretical."* | Bruce Perens 氏 2018-06-19 | **不利な面（B2）。** 審査者の 1 人が、提出者に「関心を持つ人を紹介して」と頼み、名前が出なかったので「理論上のもの」と見た。ACD も今は関心の表明を示せない。2026 年の Piana 氏の「使う、または使うと表明するプロジェクトはあるか」（§1.222）と同じ問いの形で、オーナーが関心の表明を集める窓口（`.github/ISSUE_TEMPLATE/acd-use.yml`）の意味がここにも在る |

**読み。** 2018 年の 2 人の文は、B3 と B2 を決める側の経験から裏づける。分かりにくいライセンスを善意で通した後悔（Cowan 氏）と、関心を持つ人を示せない提出を「理論上」と見る目（Perens 氏）である。

**逆側。** Cowan 氏が「今は分かりにくくない」とも書いているとおり、分かりにくさは読み手の慣れで変わる。ACD の理由の文は分かりやすさのために置いているが、長さとして数えられる。Perens 氏の問いは L0-R（使用を制限する独自の型）への問いで、委員会の理由書は使用を基準にしていない（§1.201・§1.223）。

**この節が establish しないこと。** L0-R の審査の帰結（提出者が実質的に取り下げた・2019-01 の要約）はこの節では読んでいない。

## 1.229 承認済みに無いことをするライセンスの審査は速くも一致もしない、使うだけの人に法的な負担を課さない、OSI・FSF・Debian の全部に通るかを先に問う —— License Zero Reciprocal の審査（2017）（2026-11-15）

"For Approval: License Zero Reciprocal Public License"（`license-review` 2017-09〜11）と、そこから分かれた "resolving ambiguities in OSD"（2017-10）から 3 通（`rounds/2017-11-license-review-l0r-berkus-novel-not-fast-observed.txt`・`rounds/2017-10-license-review-l0r-perens-no-legal-load-observed.txt`・`rounds/2017-10-license-review-l0r-phipps-preflight-observed.txt`）。法律家の Kyle Mitchell 氏が単独で出した新しいライセンスの審査で、通単位の未引用の会話の上位に出た。§1.228（同じ提出の 2018 年の後日談）の前段である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"You are submitting for approval a license which does several things which no license previously approved by the OSI does. If you thought that reviewing such a license was going to be either fast or straightforwards, or that committee members would be unanimous in our evaluation of criteria or recommendations, then I'm sorry."* | Josh Berkus 氏 2017-11-13 | **見込みの材料（B10 の裏面）。** 承認済みに無い効果を主張するライセンスの審査は、速くも簡単でもなく、委員の評価も割れる、と理事の 1 人が書いた。ACD は B10 で「承認済みのどれにも無い効果」を主張するので、その主張が強いほど審査は長く、意見が割れると見込むのが正確である（`OSI-APPROVAL-PLAN.md` の時間の見込み） |
| *"With regard to *simple users,* those who make use of the Open Source software and do not modify or redistribute it, there should be as close to *no legal load* as possible. We need to be cognizant that many of these users are individuals and very small businesses that can't reasonably assume any legal load at all."* | Bruce Perens 氏 2017-10-24（OSD が書いていないが承認の過程で見るべきこととして） | **有利な面。** ACD は使うだけの人に何も課さず（§10.1）、知らなくても許諾を持つ（§2.3）。Perens 氏の「法的な負担を限りなく 0 に」を、使う人だけでなく配る人・改変する人にまで及ぼした形である。§1.199 の同じ人の「ライセンスを読まなくても動かせる」と同じ線 |
| *"Seems to me any license that is approved by only one of {OSI, FSF, Debian} is an indicator of an unaddressed issue. So, simply as an exercise of reflection, asking if one's license will be approved by all is a great pre-flight check."* | Simon Phipps 氏 2017-10-25 | **手順の材料。** OSI・FSF・Debian の全部に通るかを、提出の前の点検として問え、という当時の理事の勧めである。`OSI-APPROVAL-PLAN.md` は Debian・FSF・Fedora の見解を「関連情報」として挙げ、未使用の経路としている。提出の前にこの点検を自分で行い、結果を提出に書くことは、Phipps 氏の勧めの形に合う |

**読み。** 2017 年の 3 人の文は、ACD の提出に 3 つの見込みと準備を与える。新しい効果を主張するほど審査は長く割れる（Berkus 氏）、使う人に負担を課さないことは決める側の価値に合う（Perens 氏）、FSF・Debian の見解を先に確かめるのは良い点検（Phipps 氏）。

**逆側。** Phipps 氏の点検は「どれかにしか通らない」ことを問題の印とするので、FSF や Debian の側で ACD が通らないと分かれば、それ自体が不利な材料になる（ACD は §3 の放棄を持つ。FSF と Debian が放棄の型をソフトウェアについてどう扱ってきたかは、このドシエでは出典に当てていない —— 最初は「Debian と FSF は CC0 をソフトウェアに勧めない立場を取ってきた」と書いたが、出典が無く、少なくとも Debian の部分は疑わしいと portfolio-30 に指摘され、2026-11-15 に取り下げた。FSF の側の理由が CC0 の特許の除外なら、特許を許諾する ACD には当たらない可能性もある。どちらも確かめるまでは読みに使わない）。点検をすれば結果が記録に残る。Berkus 氏の文は L0-R（使用を条件にする型）への文で、ACD のような条件の無い型の審査が同じく長くなるかは分からない。

**この節が establish しないこと。** FSF・Debian が ACD をどう見るかは確かめていない。L0-R の審査の帰結は §1.228 の範囲で、この節は扱わない。

## 1.230 指摘に改訂版で答えない提出は判断を延ばされ、著者に代わって理事が論点を集めた —— 先例の主張は通らず、承認は一般の利用のためにある（C-FSL・2018〜2019）（2026-11-15）

"For Approval: Convertible Free Software License"（`license-review` 2018-09〜2019-03・v1.1 から v1.4 まで）から、まだ置いていなかった 5 通のうち 4 通（`rounds/2018-10-license-review-cfsl-phipps-postponed-observed.txt`・`rounds/2018-10-license-review-cfsl-phipps-open-issues-observed.txt`・`rounds/2018-09-license-review-cfsl-smith-interpretive-history-observed.txt`・`rounds/2019-01-license-review-cfsl-phipps-general-use-observed.txt`）。同じ提出の「承認を保留する」の 2 通は 2026-09-28 に `rounds/2018-12-license-review-withhold-approval-observed.txt` へ置き、`against.md` #274 で読んである。この節はその前後である。帰結は Richard Fontana 氏 2019-03-14 の告知で、v1.4 を *"in accordance with the consensus view of the community as expressed on this list, and because further constructive revision of the license to cause it to conform to the OSD does not seem likely"* として却下した（`rounds/2019-03-license-review-cfsl-fontana-rejected-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Since the discussion is still in progress, and since there are so many comments indicating problems -- including drafting issues and multiple conflicts with the OSD -- that have so far not been addressed in a revised version, the Board has postponed any decision on this license for another month. For the avoidance of doubt, no license is OSI Approved until the Board has stated that it is so."* | Simon Phipps 氏 2018-10-15（理事会の決定の報告） | **手順の材料。** 指摘が改訂版で扱われていることが、理事会が判断へ進む条件として働いた。`REVISION-PROTOCOL.md` の「受けた指摘を改訂版に取り込む」手順は、この運用に合う形である |
| *"For the list's convenience, and in the absence of similar diligence by the author, I have attempted to accumulate the open issues."* / *"I believe a minimum of a revised license with the drafting issues addressed will be required to progress"* | Simon Phipps 氏 2018-10-15 | **有利な面と期待。** 理事は、未解決の論点を集めて一覧にすることを著者に期待される「勤勉さ」として扱った。ACD は欠陥を errata に、反論を `ACD-1.0.objection-map.md` に、不利な事実を `against.md` に自分で集めている。審査で同じことを求められたとき、すでに一覧を持っている |
| *"the practice around applying those definitions is more rigorous than the wording of the definitions themselves, which leads to submitters who rely much more on the words of the OSD than the interpretive history."* | McCoy Smith 氏 2018-09-26（「承認済みのライセンスも同じことをしているから、先例で却下できない」という提出者の応答が繰り返されることへ） | **不利な面（先例の重み）。** 「承認済みの X も同じことをする」は、この 1 年で何度も出て否定的に受け取られた応答の型として名指しされた。ACD の文書は CC0・Unlicense・0BSD などの先例に依る箇所を持つ。先例は「論点が既に論じられた」ことを示す材料にはなるが、それだけで通る論拠としては書かない |
| *"It may be worth reminding some folk that we approve licenses for general use. It should be possible for many users of the code to simply proceed knowing that a level playing field of rights delivering the four freedoms are ensured by OSI approved licenses."* | Simon Phipps 氏 2019-01-14（四つの自由は評価の前提だ、と同じ通で） | **有利な面。** C-FSL は「原著者」の集団に他の貢献者より強い権利を残したので、対等でないと読まれた（Piana 氏・Perens 氏）。ACD は全員に同じ許諾を与え（§2・§4）、他の人の改変や貢献について Dedicator に特権を残さない。「対等な権利」の基準に、型として合う |

**読み。** C-FSL の審査は、指摘を受けた提出が改訂版を出さないと判断が延び、最後は「OSD に合う改訂が出そうにない」ことを理由に却下された。理事が求めたのは、論点の一覧と、それに答える改訂版である。ACD の側には一覧があり、全員に同じ権利を与える型である。

**逆側。** 一覧を持っていることは、指摘に答えた改訂版を出したことではない。審査で出る指摘に答える改訂は、その時点で作るしかない（凍結した本文は直さず次版で直す、という我々の手順は、審査の途中では「改訂版がまだ無い」と見える時間を作りうる）。Smith 氏の文は、我々の比較の文書（`ACD-1.0.comparison.md`）が先例に頼るほど弱く読まれうることを示す。C-FSL は単独の著者で作文の質が問題にされた提出で、ACD の B1（単独の起草者）と同じ面を持つ。

**この節が establish しないこと。** 2018 年の「1 か月延ばす」運用が今も同じかは確かめていない（2019 年以降の process の変更は `ACD-1.0.review-rules.md` の範囲）。ACD の比較の文書のどの文が「先例だけで通る」型になっているかは数えていない。

## 1.231 本文で機械可読の形式を名指すこと —— 承認された本文は SPDX の札を名指した、本文の URL は古びた、告知の形を固定すると REUSE と衝突した、OSI は識別子ではなくライセンスを承認する（2026-11-15）

portfolio-1c の T69（1.4 草案の §2.6 に、除外する素材を示す形の例として "such as an SPDX expression or a REUSE file" を書く案・1.0 でも §2.6）への当て。測り方: 写しの全月（2010 年以降）の、引用行を除いた本文に `SPDX-License-Identifier|reuse.software|REUSE (spec|file)|本文の中の SPDX` を正規表現で当てた。会話を 1 本ずつ通読したのではないので、「見つからない」は弱い不在である。新しく置いた 3 通は `rounds/2024-03-license-discuss-ecl-stale-link-ombredanne-observed.txt`・`rounds/2021-09-license-discuss-afl-reuse-crane-observed.txt`・`rounds/2024-08-license-discuss-gplv2-spdx-fontana-observed.txt`。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| 承認された本文の冒頭: *"This Cryptographic Autonomy License (the "License") applies to any Work whose owner has marked it with any of the following notices: "Licensed under the Cryptographic Autonomy License version 1.0," or "SPDX-License-Identifier: CAL-1.0," or ..."* | 委員会報告 2020-02-09 の Exhibit A（Pamela Chestek 氏・`rounds/2019-04-license-review-cal-approval-observed-52of61.txt`）。理事会は 2020-02-14 に 8-0（棄権 1）で承認 | **有利な面（先例）。** 承認済みの本文が、条文の中で SPDX の札を適用の印として名指している。ACD の §16.2（1.0 でも §16.2）が `SPDX-License-Identifier` の札を十分な告知とするのと同じ型で、審査でこの名指しそのものへの異議は見つからなかった |
| *"In the prefatory material, "with Combined-Works-Exception" should be "WITH ..." (the SPDX operator, or whatever the proper term is, is capitalized)."* | Richard Fontana 氏 2020-02-07（CAL の審査・`rounds/2019-04-license-review-cal-approval-observed-51of61.txt`） | **期待。** 審査者は本文の中の SPDX の構文の正確さまで見る。§2.6 に "SPDX expression" と書くなら、例に出す式の構文（`WITH`・`AND` の大文字、`LicenseRef-` の形）を正確にする |
| *"or even better, bypass the URL entirely and use an SPDX-License-Identifier: ECL-2.0 tag."* | Philippe Ombredanne 氏 2024-03-20（ECL-2.0 の付録の URL が死んだので本文を直してよいか、という問いへ。本文を直すと checksum で照合する道具を欺くので悪手、と同じ通で） | **両面。** 本文に外部の場所を書くと古びる、の実例である。処方は SPDX の札で、古びたのは URL のほうだった。ただし SPDX も外部の団体で、名指した形式の側が変わる危険は 0 ではない |
| *"Unfortunately, it seems as though the wording of the AFL precludes its use with REUSE and SPDX license identifiers, so the script is under MIT-0 in any case :)"* | Sebastian Crane 氏 2021-09-08 | **有利な面。** 告知の形を本文で固定したライセンスは、機械可読の慣行と衝突しうる。§2.6 と §16.2 が SPDX の札や式、REUSE の file でも足りると開くのは、この衝突を避ける向きである |
| *"OSI does not approve, or up till now hasn't approved, SPDX identifiers as such, but rather the actual licenses they refer to"* / *"I've certainly noticed some confusion about the difference between an actual license and the SPDX identifier that might represent it."* | Richard Fontana 氏 2024-08-09（"Not speaking for the OSI" と断っている） | **逆側。** 承認の対象は本文で、識別子は SPDX が別に割り当てる。ACD の §16.1 と §16.2 は `ACD-1.4` という識別子を本文の中で先に名指し、一覧に載るまでは `LicenseRef-ACD-1.4` と書く。SPDX が別の識別子を割り当てれば、本文の名指しと一覧が食い違う |

**読み。** 本文の中で SPDX の札を名指すことには承認済みの先例（CAL-1.0）があり、審査は名指しを咎めず、構文の正確さを求めた。告知の形を本文で固定すると機械可読の慣行と衝突しうる（AFL）ので、形式を例示しつつ限定しない T69 の書き方（"such as"）は、衝突を避ける側にある。

**逆側。** 例示した形式は本文の外の団体の管理下にあり、古びることも名前が変わることもある（Ombredanne 氏の URL、Fontana 氏の識別子と本文の区別）。REUSE を本文で名指した承認済みの例は見つからなかった（AI-MIT-1.0 の提出者が 2026-03 の改訂で REUSE の per-file header を採ると書いたが、未承認で、審査の反応は確かめていない）。"such as" の例示は要件ではないと読まれるのが自然だが、例示が古びたときに本文が古く見えることは残る。

**この節が establish しないこと。** CAL-1.0 の本文が名指した 2 つ目の札（`CAL-1.0-With-Exception`）が、SPDX の一覧で実際に割り当てられた識別子と一致しているかは確かめていない（一致していなければ、本文が先に名指した識別子が一覧と食い違った実例になる。SPDX の一覧は外部の取得が要る）。「標準を本文に書くと古びる」という正面の異議は、この測り方では見つからなかった。

## 1.232 貢献の条項を執行できる根拠は「外向きのライセンスを受諾したこと」だと Chestek 氏は書いた —— ACD は受諾を要しないので、その根拠は移らず、移るのは Smith 氏の「提出する行為が同意の表示」である（"Contributor Clauses in Licenses"・2025-12）（2026-11-15）

`against.md` #286 が Berkus 氏と Chestek 氏の 2 文を引いた会話（`license-discuss` 2025-12-08〜09・21 通）を通読し、6 通を rounds に置いた（`rounds/2025-12-license-discuss-contributor-clauses-*-observed.txt`）。#286 は「貢献の条項はライセンスに場所が無い」という異議とその潰し方を書いた。この節は、潰し方の一つ（Chestek 氏の明示の inbound=outbound）が ACD にどこまで移るかを読む。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"1. Unless enforced by some other mechanism (CLA, repository TOS, etc.), it is not automatically true that contributions are under the license in the first place;"* / *"2. A license cannot reasonably contain the full multiple-page-long set of the various things that a contributor should comply with, leaving us with a very arbitrary selection."* | Josh Berkus 氏 2025-12-08（会話の最初の通） | **2 つ目には §2.6 が答えている。** §2.6（1.0 でも §2.6）は貢献者に求める「それ以外のこと」を *"a matter of project governance and is not addressed here"* として本文の外に置く。恣意的な選び方を本文に持ち込まない。1 つ目は下の Chestek 氏と Smith 氏の往復が扱う |
| *"It doesn't violate the OSD, no.  But it also has zero effect.  It's a no-op."* / *"No text contained within the license can enforce that my PR is under that license."* | Josh Berkus 氏 2025-12-08 | **異議の芯。** 効果が無いという異議で、OSD の問題ではない。同じ人が翌日 *"In neither case is there an OSD violation *unless* the contributor clauses specifically create an asymmetry."* と書いた |
| *"The bigger problem with these combined outbound license+inbound cla documents is they often attempt to impose non-reciprocal conditions"* / *"That makes the license discriminatory."* | McCoy Smith 氏 2025-12-08 | **有利な面。** 問題は非相互の形である。§2.6 の貢献者は全員に同じものを与え、維持者に特別な権利は残らない（#286 の判断と同じ） |
| *"I am in favor of an express statement in the license and agree that the statement should be inbound=outbound."* / *"Since I accepted the project license, I therefore agreed to the terms for my contribution and the CLA within the license is enforceable against me as a contributor."* / *"If an express grant isn't enforceable against a contributor, then the implied grant is even less likely to be enforceable against them."* | Pamela Chestek 氏 2025-12-08（黙示の許諾は狭く解され、米国第 9 巡回区の判例も揺れる、と同じ通で） | **有利な面と、ACD に移らない根拠。** 明示の inbound=outbound に賛成する理由（黙示より確か）は ACD にも当たる。しかし執行の根拠として挙げたのは「貢献者は外向きのライセンスを受諾した」ことである。ACD の §2.3（1.0 でも §2.3）は *"This Dedication takes effect without any act of acceptance by You."* と書き、利用者に受諾を求めない。受諾が無ければ、Chestek 氏の経路は ACD には通らない |
| *"If you're concern is manifestation of assent, the act of submitting a contribution and requesting it be accepted would be the manifestation."* | McCoy Smith 氏 2025-12-08 | **ACD に移る根拠。** 同意の表示を受諾ではなく提出する行為に置く読みで、§2.6 が *"unless they state otherwise at the time of submission"* と提出の時点に結びつけている形に合う |

**読み。** Berkus 氏の異議は OSD の問題ではなく「効果が無い」という問題で、非対称を作らなければ OSD 違反ではないと本人が書いた。§2.6 は対称で、恣意的な条件を本文の外に置く。効果について、明示の条項が黙示より確かだという Chestek 氏の論は ACD にも当たるが、彼女が執行の根拠にした受諾は ACD には無い。ACD の §2.6 を支えるのは Smith 氏の「提出という行為」で、本文もすでに提出の時点に結びつけている。

**逆側。** 受諾を要しない設計（§2.3）は利用者に有利だが、貢献の条項の執行の根拠を一つ減らす。提出を同意の表示と読むのは Smith 氏の一通で、どの法域で通るかは確かめていない。Berkus 氏の例（文書の文法の直し、翻訳、デザイン、依存の版の更新）のうち、Chestek 氏は依存の更新を著作物でないと退け、文書の直しは派生物だと答えたが、ライセンスを受諾せずに貢献する人がいることは否定しなかった。§2.6 の「受諾が無くても提出で結びつく」は、この隙間を埋める向きだが、埋まるかは法律家の問いである（`QUESTIONS-FOR-COUNSEL.md` の問 4）。

**この節が establish しないこと。** 提出が同意の表示になるかの法的な評価はしていない。Chestek 氏と Berkus 氏の 2025-12-09 の往復（独占的なライセンスで手にした版から貢献する人）は、帰結が会話の中で定まっていないので、読みに使っていない。

## 1.233 委員長は「license-review は本物のライセンスに限る、思考実験は license-discuss で」と書いた（2020）—— 5 年前の委員長は「思考実験のライセンスも承認した」と書いている。ACD は適用された本文だが、適用先は自らを実験と呼ぶ（2026-11-15）

"What should fit in a FOSS license?"（`license-discuss` 2020-03・19 通）を通読し、1 通を置いた（`rounds/2020-03-license-discuss-what-fits-chestek-thought-experiments-observed.txt`）。会話の大半は倫理的な条件をライセンスに入れるかの意見で、ACD には当たらない（ACD は条件を置かない）。当たるのは、次の 1 通と、B2 が既に引く 2015 年の委員会報告との対照である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"No, you shouldn't. License-review is a burdensome process for the OSI and the list participants, so it should be limited to real licenses, not thought experiments. License-discuss is for thought experiments."* | Pamela Chestek 氏 2020-03-09（License Review Committee の委員長として署名）。考えを本物のライセンスの文に起こし、皆にとって面白い演習として `license-review` に通してみようか、と書いた Christopher Lemmer Webber 氏への返答（Webber 氏の文は Chestek 氏の通の引用行に在る） | **手順の材料と不利な面の候補。** 委員長は、演習として作った文を `license-review` に出すことを退けた。ACD を `license-review` に出すときに問われうるのは、ACD が「本物のライセンス」か「演習」かである |
| *"OSI has approved thought-experiment licenses before (e.g. the SimPL) as well as licenses that were not used prior to OSI approval (e.g. the UPL)."* | Richard Fontana 氏 2015-10-13（委員長として、Free Public License の委員会報告・`rounds/2015-10-13-license-review-fontana-committee-report-fpl-observed.txt`・B2 が既に引く） | **有利な面（承認の記録）。** 思考実験として書かれたライセンスも承認されてきた。ただし Chestek 氏の文は承認の可否ではなく、`license-review` に出してよいかについてで、5 年後の委員長の運用である |

**読み。** 2 人の委員長の文は食い違うように見えるが、問いが違う。Fontana 氏は「承認されたライセンスの中に思考実験もあった」と書き、Chestek 氏は「演習として審査に出すな」と書いた。ACD は演習として書いたのではなく、このリポジトリに適用されている（`LICENSE` は 1.3 を適用し、*"The dedication used here was written for this repository and is offered for general use by anyone"* と書く）。審査の対象として「本物のライセンス」である、という主張は立つ。

**逆側。** 適用先のリポジトリは、`LICENSE` 自身が *"This repository is a public experiment in AI orchestration"* と書き、README も「experiment」と書く。ライセンスの本文と提出の文書（`submission.md`・`REVIEWERS.md`）には「experiment」の語は無いが（2026-11-15 に grep で 0 件）、リポジトリを開いた審査者は「実験の一部として作られたライセンス」と読みうる。OSI の moderators が 2026-09-09 にこのリストを *"proof-of-concept"* に使われていると書いたこと（`against.md` #161・B14）と重なると、Chestek 氏の「思考実験」の線に読まれる危険がある。実使用が 1 リポジトリだけであること（B2）も、この読みを強める。

**この節が establish しないこと。** 2026 年の委員会が Chestek 氏の 2020 年の運用を引き継いでいるかは確かめていない。ACD を「本物のライセンス」と示す材料として、適用の事実のほかに何が要るか（他のプロジェクトの使用、B2）は、この節では扱わない。

## 1.234 承認を取り下げる理由として、法律家なしに書かれたことは挙げられ、そして退けられた —— OSD の解釈は法律家と非法律家が等しくでき、起草の質の評価は主観的だ（"what would de-listing of licenses look like?"・2013-03）（2026-11-15）

`license-discuss` 2013-03 の会話（18 通）を通読し、5 通を置いた（`rounds/2013-03-license-discuss-delisting-*-observed.txt`・Fontana 氏の *"approved "in haste""* は `delisting-villa-opener` の引用行に在る）。発端は Richard Fontana 氏が Frameworx License を *"approved "in haste""* と書き、取り下げの手続きがあれば見直しを勧める、と述べたことで、Luis Villa 氏がその手続きの形を尋ねた。ドシエは 2026 年の *"The OSI does not currently have a process for de-listing"*（`review-outcomes.md`・against #146 / #209）を持つが、取り下げの理由を何に置くかを論じたこの会話は読んでいなかった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"1. They are ambiguous or likely to perform in court in unexpected ways, should they ever be litigated. ... These would be the "crayon" licenses, mostly, those written without legal counsel."* / *"3. They are both redundant /and /rarely used."* | Bruce Perens 氏 2013-03-06（取り下げの理由として 3 つを挙げた。2 つ目は OSD に合わず誤って承認されたもの） | **不利な面（B1・B2）。** 法律家なしに書かれたことと、重複して使われないことを、承認を取り下げる理由に挙げた。ACD は法的レビューを受けておらず（B1）、実使用は 1 リポジトリ（B2） |
| *"It isn't the least bit difficult to diagnose when no lawyer was involved in drafting a license."* | Bruce Perens 氏 2013-03-06（Villa 氏の「評価は難しい」への返答） | **不利な面（B1）。** 法律家が関わったかは本文から読み取れる、という見方である。ACD は起草の経緯を開示している（B14）ので、読み取られる前に書いてある |
| *"In my view, Bruce's justification 2 is the only justification: the license does not comply with the OSD and was accepted in error."* / *"my view is that the OSD should be the basis for an argument for delisting, and you don't need to be, or to get, a lawyer to interpret the OSD (more precisely, lawyers and non-lawyers are equally competent to interpret the OSD)."* | Richard Fontana 氏 2013-03-07 | **有利な面（B1）。** Perens 氏の 1 つ目（法律家なしの起草）と 3 つ目（重複と不使用）を、取り下げの理由として退けた。理由は OSD に置くべきで、OSD の解釈に法律家は要らない、と書いた。ACD の OSD 逐条（`submission-osd.md`）は、この基準では法律家でなくても行える作業である |
| *"That said, as Richard pointed out, this is an extremely difficult issue to evaluate. It is inherently subjective, and a matter requiring expertise. Given that, I see  no evidence that OSI (or anyone) could perform it in a reasonable, objective, efficient manner, so I'm not very interested in pursuing it."* | Luis Villa 氏 2013-03-06 | **有利な面（B1）。** 起草の質の評価は主観的で、OSI が客観的に行えるとは思えない、と書いた。審査の基準が起草の質そのものに置かれないことの、決める側に近い人の文である |

**読み。** 2013 年の会話は、法律家なしに書かれたことを取り下げの理由に挙げる人（Perens 氏）と、それを退けて OSD だけを理由とする人（Fontana 氏・Villa 氏）に分かれた。後者の線では、ACD の審査で問われるのは OSD への適合で、起草者が法律家かではない。

**逆側。** 会話は取り下げについてで、承認の基準についてではない。承認の審査では、法律家の目が通ったかを審査者が最初に探す記録がある（B1 の Piana 氏 2024、Berkus 氏 2020 の「法律家の声を数える」）。Fontana 氏自身が同じ会話の発端で Frameworx を *"approved "in haste""* と書いており、急いだ承認を悔やむ記録は、新しい単独起草のライセンスの審査を慎重にする向きに働く。Perens 氏の「診断は易しい」は、ACD の本文が法律家の書き方に見えない箇所があれば、それが最初に読まれることを意味する。

**この節が establish しないこと。** 2013 年の Fontana 氏・Villa 氏の文が、その後の承認の審査の運用になったかは確かめていない。Frameworx が取り下げられたかは、この会話では分からない。
