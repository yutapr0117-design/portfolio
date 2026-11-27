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

## 1.218 放棄し、放棄できない所では行使しないと約束し、虚偽の著者表示だけは除き、可分にする —— 人格権について Sado 氏と Perens 氏が示した形（PUWL・2025）（2026-11-15・2026-11-27 に帰属を訂正）

"[DISCUSS] PUWL v1.0"（`license-discuss` 2025-10・`rounds/2025-10-license-discuss-puwl-moral-rights-observed.txt` に 4 通）。単独の作者が出した public-domain 型のライセンスの草案で、人格権の扱いが論じられた。ドシエは PUWL を「crayon license」の例として引いていたが（`review-labels.md`）、人格権の条の形について決める側が示した案は引いていなかった。portfolio-1c の §12.4 の依頼で探した。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Contributor waives and agrees not to assert any moral rights (including rights of attribution, integrity, and disclosure) in the Work and Contributions. Where such waiver is not permitted, each Licensor and Contributor irrevocably covenants not to assert such rights and consents to all acts that would otherwise infringe them, including modification, combination, and omission of attribution, provided there is no false attribution of authorship. This provision is severable and survives to the extent enforceable in any jurisdiction."*、*"in Japanese software practice, a pure "waiver" rarely bites on its own."* | Shuji Sado 氏 2025-10-17（Open Source Group Japan の代表。*"Hi Bruce-san, Pamela-san, Thanks for your thoughtful “belt-and-suspenders” take on moral rights"* と 2 人宛てに書いたが、その形を出したのは下の行の Perens 氏で、Chestek 氏は放棄だけで足りるとした側） | **有利な面（B8・強い）。** 1.4 草案の §12 は同じ構造を持つ: §12.1 *"waives and agrees not to assert Moral Rights"*、§12.2 放棄できない法域では *"covenants not to exercise Moral Rights in the Work against You"*、§12.5 は虚偽の著者表示（§11.3）を約束の外に置き、§12.6 は可分（§15.2）。日本の実務を知る審査者の 1 人が、ACD の型と同じ形を自分から提案した。**差は 1 つ**: Sado 氏の案は *"consents to all acts that would otherwise infringe them"* という同意を持ち、ACD の §12.2 は約束だけで同意を書かない（試作の候補として portfolio-1c へ渡した。同意の理由は Sado 氏の通に書かれていない・下の逆側） |
| *"How about waiving all claims and promising not to assert moral or other rights in a lawsuit? Belt and suspenders :-)"* と *"Ah, but then we have severability."*（どちらも Perens 氏の同じ通。Chestek 氏の *"why not just say that the author waives all claims and leave it at that?"* と *"The phrase "to the fullest extent permitted by applicable law" is surplusage too; it goes without saying that's the extent to which it can be enforced."* への返信） | Bruce Perens 氏 2025-10-06（2025 年の役はドシエで確かめていない） | 放棄と不行使の約束を重ね、可分の条で支える形を、Perens 氏が示した。§12.1・§12.2・§12.6 の重ね方と同じ。**Chestek 氏は逆の側** —— 放棄だけで足り、限定の句は余計とした（下の逆側） |
| フランスの規定を引いて *"It is perpetual, inalienable and indefeasible. On the author's death it can be transmitted to his heirs. The exercise of this right can be transferred to a third person by testamentary disposition."* | Perens 氏 2025-10-06 | §12.4 は約束が *"heirs, personal representatives, and any person entitled to exercise or enforce Moral Rights in the Work after the Dedicator's death"* を *"to the fullest extent the law permits the Dedicator to bind them"* 縛ると書く。相続人と遺言で行使を受けた人の両方を名指す点で、Perens 氏の引いた規定の形に当たる |
| *"An affirmative grant would be a significant difference from cc0."*（特許について） | Perens 氏 2025-10-06 | **有利な面（B10）。** 特許の積極的な許諾が CC0 との大きな違いになると、Perens 氏が 2025 年に書いた（役は確かめていない）。ACD の §8 はそれを持つ |
| *"I would also like to see an explanation of how all the other licenses that attempt to achieve this fail, and how this license has remedied their flaws."* | Pamela Chestek 氏 2025-10-06 | **B10 の要求。** 既存の試みがどう失敗し、新しいものがどう直したかの説明を求めた。`REVIEWERS.md` の "In one screen" と `submission-reference.md` の比較がこの形に答える |

**読み。** 2025 年 10 月に 2 人の審査者（Sado 氏・Perens 氏）が人格権の条に示した形（放棄＋放棄できない所での不行使の約束＋虚偽の著者表示の除外＋可分）は、ACD の §12 の構造と一致する。日本法を知る Sado 氏が自分から同じ形を書いたことは、§12 を「範囲を広げすぎ」（B8 の一方の読み）ではなく「放棄だけでは効かない法域への備え」として読ませる材料になる。

**逆側。** **同じ会話の Chestek 氏は簡素な側に立った**（2026-11-27 に帰属を訂正 —— 初稿は Perens 氏の「放棄＋約束」の文を Chestek 氏のものとし、「2 人の決める側が支持した」と書いていた。有利な向きに盛った誤りで、d7 が帰属の照合で見つけた）。同氏は放棄だけで足り、「適用法の許す最大限で」の限定の句は余計だとした（`review-readings-7.md` §1.481 の「限定句の繰り返し」の行と同じ通）。ACD の §12 は放棄・約束・同意・可分を重ねるので、この簡素さの側の問い（重ねる理由は何か）が当たる。Sado 氏の案は Contributor と Licensor を名指し、同意を含む。ACD の §12 は Dedicator の約束だけで、同意の語を持たない。**同意の出所について**: Sado 氏の通が日本の実務について述べるのは *"Where "natural persons" are the authors, practice relies on non-assertion covenants rather than blanket waivers."* と *"the broad permission to modify and create derivatives often functions in effect as a non-assertion of integrity-type claims"* で、同意が同一性保持権に効くとは書いていない。同意は案の文に在るだけで、その理由は通の中に無い。「同意を足せば約束より強い」は我々の推測で、日本の文献にも法律家にも当てていない（`QUESTIONS-FOR-COUNSEL.md` の候補）。また、PUWL そのものは「crayon license」と呼ばれた単独の草案で、決める側が示した形は PUWL を直すための助言であり、承認の基準ではない。B8 のもう一方の読み（人格権の条は mission creep）は、この会話では論じられていない。

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

**逆側。** Phipps 氏の点検は「どれかにしか通らない」ことを問題の印とするので、FSF や Debian の側で ACD が通らないと分かれば、それ自体が不利な材料になる（ACD は §3 の放棄を持つ。FSF と Debian が放棄の型をソフトウェアについてどう扱ってきたかは、このドシエでは出典に当てていない —— 最初は「Debian と FSF は CC0 をソフトウェアに勧めない立場を取ってきた」と書いたが、出典が無く、少なくとも Debian の部分は疑わしいと portfolio-30 に指摘され、2026-11-15 に取り下げた。FSF の側の理由が CC0 の特許の除外なら、特許を許諾する ACD には当たらない可能性もある。どちらも確かめるまでは読みに使わない。**2026-11-16 に確かめた**: FSF の license-list は CC0 をソフトウェアに勧めない理由を特許の明示の除外に置き、Debian Wiki は CC0 型の献呈をソースがあれば DFSG を満たしうるとしていた（`rounds/2026-11-16-fsf-license-list-and-debian-dfsg-public-domain-snapshot.txt`・WebFetch の逐語の片）。取り下げた文は、Debian について誤り、FSF について理由を欠いていた）。点検をすれば結果が記録に残る。Berkus 氏の文は L0-R（使用を条件にする型）への文で、ACD のような条件の無い型の審査が同じく長くなるかは分からない。

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

## 1.235 MPL 2.0 の起草者は OSI と同時に FSF にも一覧への掲載を求めた、Perens 氏は追加の許可を本文の外に置き本文を不変にせよと書いた（"MPL 2 section 11"・2010-11）（2026-11-15）

"MPL 2 section 11"（`license-review` 2010-11〜12・49 通）を通読し、2 通を置いた（`rounds/2010-11-license-review-mpl2-s11-villa-fsf-too-observed.txt`・`rounds/2010-11-license-review-mpl2-s11-perens-invariant-observed.txt`）。会話の大半は MPL 2.0 の草案の GPL との互換の通知と、強いコピーレフトが米国の著作権法で成り立つかの議論で、条件を置かない ACD には当たらない。当たるのは次の 2 通である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Just as we're asking OSI, we're also asking FSF to be on their lists of Libre and compatible licenses, and have spoken with them to that end."* | Luis Villa 氏 2010-11-22（Mozilla の側から、MPL 2.0 の目標の説明として） | **手順の先例。** 承認された主要なライセンスの起草者が、OSI と FSF の両方に同時に当たり、FSF とは話を済ませていた。§1.229 の Phipps 氏の事前点検（OSI・FSF・Debian の全部に通るか）を、提出者が実際に行った例である。`OSI-APPROVAL-PLAN.md` が未使用の経路としている FSF の見解は、提出と並べて求められてきた |
| *"Adding permissions to use under different licenses is always the right of the copyright holder, and can be stated /outside of the Mozilla license./ And IMO should be."* / *"I submit that Mozilla would be doing the community a service if they were to make their license invariant."* | Bruce Perens 氏 2010-11-22（MPL の変種が承認済みの中に多すぎる、と同じ通で） | **有利な面。** ACD の §16.4（1.0 でも §16.4）は、改変した本文を "Autonomous Commons Dedication" の名と "ACD-" の識別子の下で配ることを Steward の新版のほかは許さず、*"each name and identifier in this family continues to denote one fixed text"* と書く。名と本文を 1 対 1 に保つ形で、Perens 氏の「ライセンスを不変に」に合う。ACD は条件を置かないので、追加の許可を本文の外に置く必要もそもそも生じない |

**読み。** 2010 年の MPL 2.0 の審査は、FSF の見解を OSI の審査と並べて求めることが、主要な提出者の通常の手順だったことを示す。ACD の §16.4 の不変性は、変種の増殖を嫌う審査者の線に合う。

**逆側。** Mozilla は大きな組織で、FSF と事前に話せる立場にあった。個人の提出者が同じ経路を取れるかは別の問題で、FSF に当たって否定的な見解が出れば、それは記録に残る（§1.229 の逆側）。また ACD は 1.0 から 1.4 まで版を重ねており、Perens 氏の「変種が多すぎる」は、名の下の不変性とは別に、同じ家族の版の数として読まれうる（`against.md` #320 の「3 か月足らずで 5 つの本文」と合わせて読む）。

**この節が establish しないこと。** FSF が MPL 2.0 をどう扱ったかは、この会話では確かめていない。FSF が ACD をどう見るかも確かめていない。

## 1.236 特定の相手に届けることを条件にしたライセンスは、その相手が消えると使えなくなるので OSD に合わない —— ACD は誰にも何も届けさせない（netX Public License・2010-10）（2026-11-15）

"For Approval: The netX Public Lisense (in plain text)"（`license-review` 2010-10〜11・27 通）を通読し、3 通を置いた（`rounds/2010-10-license-review-netx-phipps-unreachable-observed.txt`・`rounds/2010-10-license-review-netx-perens-website-observed.txt`・`rounds/2010-10-license-review-netx-perens-approved-license-observed.txt`）。ドシエは 2010-12-01 の委員長の報告の 1 文（*"The requirement to submit changes directly to the licensor is a technology-specific term"*・`review-readings.md` §1.192 の表）だけを持っていた。netX は改変を許諾者のサイトへ上げることを条件にしていた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Any requirement that a specifically identified entity (e.g. the original author) must receive notification in any form (including a code submission) in order for the license conditions to be satisfied creates an onerous accumulating burden on downstream participants and additionally may invalidate the license grant if the entity becomes unreachable or ceases to exist."* / *"I believe this burden unreasonably restricts the freedoms of anyone but the copyright holder and would therefore constitute a failure to satisfy the OSD."* | Simon Phipps 氏 2010-10-31（*"I believe this represents the prior conclusions of OSI in the matter"* と同じ通で） | **有利な面。** ACD は誰にも何も届けさせない（§10.1・1.0 でも §10.1）。許諾は Dedicator に連絡が付くかに依らず、取り消せない（§2.2）。Phipps 氏が OSD 違反とした形を、ACD は持たない |
| *"And licenses that have been predicated on a particular upload site have previously been rejected. The language must continue the license once the web site goes away, as they so often do."* | Bruce Perens 氏 2010-10-06 | **有利な面。** ACD の §16.2（1.0 でも §16.2）は、識別子や名前の参照があれば *"the terms apply in full whether or not a copy of this text accompanies the work"* と書く。§16.1 の通知は本文の場所（`Full text: <location of this file>`）を書かせるが、その場所が消えても条件の効力は変わらない |
| *"Thus, I must stress: The very best thing you could do for the Open Source developer community would be to find an already-approved license to use."* | Bruce Perens 氏 2010-10-30（新しいライセンスは、承認済みと似たことをしながら開発者の法的な負担と組み合わせの問題を増やすので、一般に疑いの目で見る、と同じ通で） | **不利な面（B10）。** 承認済みのものを使え、という定型の応答で、§1.217 の Blue Oak への同じ人の文（2024）と同じ線である。ACD は承認済みに無い効果を主張して答える（B10 の G1） |

**読み。** netX は改変を特定のサイトへ上げることを条件にして、OSD に合わないとされた。理由は、特定の相手やサイトに依る条件は、相手が消えると許諾を使えなくするからである。ACD は利用者に何も課さず、本文の場所が消えても条件の効力が変わらない形に書いてある。

**逆側。** ACD の §2.6（1.0 でも §2.6）は、別段を述べた素材を示すことを Dedicator に約束させる。利用者に課すものではないが、「誰かが何かをしなければならない」文が本文にあることは、netX の型を探す審査者の目に留まりうる（§2.6 は *"imposes nothing upon You"* と書いて答えている）。Perens 氏の「承認済みのものを使え」は、効果の差（G1）が読まれなければ、そのまま ACD に当たる。

**この節が establish しないこと。** netX の審査の帰結（却下か取り下げか）は、この会話の中では確かめていない。

## 1.237 承認すれば使われるようになると提出者は信じるが、問題は承認の欠如ではなく関心の欠如だ —— Perens 氏の「承認の妖精の粉」（"Support for SSPL v2"・2018-12）（2026-11-15）

"Support for SSPL v2"（`license-review` 2018-12・16 通と、`license-discuss` へ移した 1 通）を通読し、1 通を置いた（`rounds/2018-12-license-review-sspl-support-perens-fairy-dust-observed.txt`）。会話はクラウドの事業者に条件を課すライセンスを支持する事業者の声と、それへの反論で、条件を置かない ACD には大半が当たらない。当たるのは次の 1 通である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The problem is generally that the license is *not *sufficiently compelling to build a community, and the submitter believes it will magically become so if OSI sprinkles approval fairy dust upon it."* / *"So, IMO the problem for some of the proposed licenses is not a lack of OSI's approval, but a lack of interest."* | Bruce Perens 氏 2018-12-18 | **不利な面（B2）。** 採用が少ないライセンスの提出者は、承認が採用を生むと期待している、という見方である。ACD の実使用は 1 リポジトリで（B2）、承認の前に関心を示せていない。審査者がこの線で ACD を読めば、「承認を採用の手段にしようとしている」と見える |
| *"Having been adopted by a wider community than Debian, this is extended to mean that everybody can run Open Source software for any purpose and should not have to hire a lawyer just to run it. Which seems to have a very broad buy-in."* | Bruce Perens 氏 2018-12-18（同じ通） | **有利な面。** ACD は何の条件も課さず（§10.1・1.0 でも §10.1）、受諾も要らない（§2.3）。「動かすために法律家を雇わなくてよい」を、使う人だけでなく配る人と改変する人にまで及ぼした形である（§1.229 の同じ人の 2017 年の文と同じ線） |

**読み。** Perens 氏は、承認を採用の代わりにしようとする提出を疑う。ACD の B2 はこの疑いの的になりうる。一方で、ACD の中身（何も課さない）は、同じ通で Perens 氏が広い支持を得ていると書いた「目的を問わず、法律家なしに動かせる」に合う。

**逆側。** Perens 氏の文は、クラウドの事業者に条件を課したい事業者の提出（SSPL とその支持者）への文で、承認が欲しい理由が事業上の利益だった。ACD の提出の理由は事業上の利益ではない（`against.md` #161 は「AI の自走の実験」と書く）が、承認を求める理由が採用ではない、とも言い切れない。B2 の解除の条件（`board-decisions.md` §2c の関心の表明）を承認の前に満たすことが、この疑いへのいちばん直接の答えになる。

**この節が establish しないこと。** Perens 氏の見方が委員会の基準になったかは確かめていない（B2 には「使用は承認の基準ではない」という委員会の文が 3 本ある）。

## 1.238 承認は「一語も変えない」本文に対するもので、他人の名を消して自分の名を入れれば承認は及ばない —— だから型板にすべきだ、と委員長は書いた（IWL・2008-05〜06）（2026-11-15）

"Approval of IWL - Consolidated Response"（`license-review` 2008-05〜06・27 通）を通読し、3 通を置いた（`rounds/2008-05-license-review-iwl-nelson-not-one-word-observed.txt`・`rounds/2008-05-license-review-iwl-nelson-existing-license-observed.txt`・`rounds/2008-05-license-review-iwl-perens-bigger-issues-observed.txt`）。Open Kernel Labs が Sleepycat License を元に作った IWL の審査で、本題は API の向こうのプログラムまで条件を及ぼす条（1(c)(ii)）が OSD 6 と 9 に反するかだった。条件を置かない ACD には本題は当たらない。当たるのは次の 3 通である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"We've always taken the position that a license cannot be modified in any way (not one word).  We've always acted as if the license steward's published copy is the official copy, and that we are not empowered to change their license.  But I think that indeed, we should make templates of all of *our* copies of the licenses."* | Russ Nelson 氏 2008-05-29（同じ日の別の通では、他人の名を消して自分の名を入れることはできない、とも書いた） | **有利な面。** ACD の本文は特定の人や組織の名を持たず、"Dedicator" と "the Steward" を一般の語で定める。§16.3（1.0 でも §16.3）は *"This Dedication may be applied by anyone"* と書き、一語も変えずに誰でも自分の作品に当てられる。Nelson 氏が承認済みの本文に欠けているとした型板の性質を、ACD は最初から持つ |
| *"It's definitely NOT a good idea to seek OSD compliance by starting with an existing license.  Our understanding of what is required by the OSD has changed over the years, and the community has come to realize that more Open Source licenses are not a good thing."* | Russ Nelson 氏 2008-05-29（承認済みに近いものを元に最小の変更で作った、という提出者への返答） | **両面。** 既存のライセンスを元にすれば適合する、という考えを退けた文で、ACD が既存の文を写していないことは不利ではない。一方で「ライセンスが増えるのは良くない」は B10 の定型の不利な面である |
| *"I don't think anyone has bothered to focus on smaller issues of the license after seeing that the bigger ones would keep it from passing. These will have to be addressed once the larger problems are fixed."* | Bruce Perens 氏 2008-05-27（論点は 1 つの条だけか、という提出者の問いへ） | **見込みの材料。** 審査者は通らない理由を 1 つ見つけると小さな問題を見るのをやめる。最初の審査で指摘が少ないことは、残りが無いことを意味しない。ACD の審査で大きな論点（B4・B10）が片付いた後に、細部の指摘が新しく来ることを見込んでおく |

**読み。** 2008 年の委員長は、承認済みの本文が型板でないことを問題と見て、名の付け替えに承認は及ばないと書いた。ACD は名を持たない型板の形で書いてあり、この点では審査者の望む形に合う。

**逆側。** Nelson 氏の「一語も変えない」は、§16.4（名と識別子の下で本文を変えさせない）の考えと同じだが、ACD はその規則を本文の中に置いている（`against.md` #27 は §16.4 が「条件は課さない」という通知の文と食い違うと読んだ）。Behlendorf 氏は同じ日に、名を変えた承認済みのライセンスも承認済みと扱ってきたと反論しており、2008 年の運用は一つに定まっていない。Perens 氏の文は、我々の提出に最初の指摘が少なくても安心できないことを意味する。

**この節が establish しないこと。** OSI がその後に承認済みの本文を型板にしたかは確かめていない。IWL の帰結は、この会話の範囲では確かめていない。

## 1.239 承認済みの AAL の作者は法律家ではないと OSI のサイトが書いている、使われなくなった承認済みライセンスは廃止が論じられた、公開されたライセンスの名は共同体のものだと Berkus 氏は書いた（"Thoughts on AAL and OSS vs FOSS"・2020-03）（2026-11-15）

"Thoughts on AAL and OSS vs FOSS"（`license-discuss` 2020-03〜04・33 通）を通読し、3 通を置いた（`rounds/2020-03-license-discuss-aal-*-observed.txt`）。Attribution Assurance License（AAL・承認済み・`gap-census.md` の 141 本に在る）を使う事業者が、バッジの表示を残す 2.0 版を求めた会話である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The author, who is not an attorney, places this license template into the public domain along with a complete disclaimer of any warranty or responsibility for its content or legal efficacy."* | McCoy Smith 氏 2020-03-30 が OSI のサイトの AAL の説明を引いた（同じ通に *"Note that the dedication of the license to the public domain means that a 2.0 version could be written by anyone."*） | **有利な面（B1）。** 承認済みのライセンスの中に、作者が自ら法律家でないと述べ、OSI のサイトがそれを載せているものがある。法律家が起草していないことは、それだけで承認を妨げてこなかった |
| *"Yeah, that was the first thing I looked at when I remarked that the license didn't have significant use anymore."* | Josh Berkus 氏 2020-03-30（作者自身が今は Apache-2.0 を使っている、という Fontana 氏の指摘を受けて。Smith 氏は同じ日に、作者に任意の廃止を持ちかけてはどうかと書いた） | **不利な面（B2）。** 承認の後も、使われなくなったライセンスは廃止が論じられる。実使用が 1 リポジトリの ACD は、承認されてもこの議論の的になりうる（`against.md` の B2 の「承認の後にも費用は残る」と同じ線） |
| *"Why? I don't see how an original license author has any moral right to the name. Once the license is released, it belongs to the whole community."* | Josh Berkus 氏 2020-03-31（2.0 版を作るのに元の作者の許しは要らない、という流れで） | **逆側（§16.4・§16.5）。** ACD の §16.4（1.0 でも §16.4）は、"Autonomous Commons Dedication" の名と "ACD-" の識別子の下で新しい版を出せるのを Steward（§16.5）に限る。Berkus 氏の見方では、名は公開された時点で共同体のものになる。ただし AAL の作者は型板を公有に置いており、ACD の本文は名の扱いを本文の中で定めている。GPL と MPL も steward が版を出す形で承認されている |

**読み。** AAL は、法律家でない作者が書いたライセンスが承認され、OSI がその事実を公表してきた例である。B1 の「法律家の目が通っていない」は、それだけで承認を止めた記録になっていない。一方で、使われなくなった承認済みのライセンスは、承認の後に廃止の議論を受けた。

**逆側。** AAL の承認は古い時期のもので（この会話の時点で既に「もはや大きく使われていない」）、その後の審査は法律家の目を探すようになった記録がある（B1 の Berkus 氏 2020・Piana 氏 2024）。Berkus 氏の「名は共同体のもの」は、§16.4 の Steward の規則が審査で問われうることを意味する。AAL の作者が型板を公有に置いたことは、ACD の本文自身の扱い（§16.4 は改変した本文を別の名でなら配れると書く）と比べて読む必要がある。

**この節が establish しないこと。** AAL が承認された年と、そのときの審査の記録は確かめていない。AAL 2.0 が出されたか、AAL が廃止されたかは、この会話の範囲では分からない。

## 1.240 OSL と AFL は 1 人の起草者が何度も版を重ね、その多くが承認された —— 作者は後に旧版を勧めないとしたが、「FOSS の許諾は永遠」なので既に配った物は変わらない（"Issue on licenses pages"・2013-11）（2026-11-15）

"Issue on licenses pages"（`license-discuss` 2013-11・4 通）を通読し、2 通を置いた（`rounds/2013-11-license-discuss-osl-afl-rosen-iterations-observed.txt`・`rounds/2013-11-license-discuss-osl-afl-rosen-forever-observed.txt`）。OSL 1.1・2.0 と AFL 1.0・1.1・1.2・2.1 が OSI のサイトから見えなくなっている、承認されたはずだ、という Engel Nyst 氏の問いに、起草者の Lawrence Rosen 氏が答えた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Not only were they approved, they were originally written at the behest of the same OSI board of directors that approved those early licenses."* / *"As you can tell, we went through several iterations."* | Lawrence Rosen 氏 2013-11-26 | **有利な面（版の数・`against.md` #320）。** 1 人の起草者のライセンスが、版を重ねながら複数の版で承認された。ACD が 1.0 から 1.4 まで版を重ねていることは、それだけで承認の妨げになった前例を持たない |
| *"As I understand it, however, FOSS licensing is forever, so deprecation wasn't supposed to mean any licensing changes to FOSS software that had already been distributed voluntarily under those licenses."* | Lawrence Rosen 氏 2013-11-27（旧版を勧めないとしたのは作者の意向で、OSI のサイトから消すことではなかった、と同じ通で） | **有利な面。** 版を改めても既に配った物の許諾は変わらない、という考えで、ACD の §2.2（1.0 でも §2.2・取り消せない）と、このリポジトリの `LICENSE` が書く *"Everything those versions gave away stays given away"*（2026-11-23 までは "Everything ACD-1.0 gave away …"・1.4 の適用で直った語）と同じ線である |

**読み。** 版を重ねることそのものは、承認の記録の上では異例でない。OSL と AFL は、理事会の求めに応じて 1 人の起草者が書き直しを重ね、複数の版が承認された。旧版を勧めなくなっても、既に配った物の許諾は残る。

**逆側。** Rosen 氏は法律家で、OSL と AFL の初期の版は理事会の求めで書かれた。ACD は法律家でない者の起草で（B1）、理事会の求めで書いたものではない。また OSL と AFL の版の改めは数年にわたり、ACD は 3 か月足らずで 5 つの本文を出している（`against.md` #320 の Kuhn 氏 2018 は、35 日での置き換えを手続きの問題とした）。版の数ではなく、版を改める速さが問われうる点は、この先例では答えられない。

**この節が establish しないこと。** OSL と AFL のどの版がいつ承認されたかは、この会話の範囲では確かめていない（Engel Nyst 氏は「承認されたはず」と書き、Rosen 氏が承認を認めた）。

## 1.241 OSD に文字どおり合っても OSI が承認するとは考えられないライセンスがある、既にそうなら条は要らず、そうでないなら条は悪い（OSET Public License の「国家安全保障と公益」の条・2015-09）（2026-11-15）

"-- National Security and Public Policy (3.5B and 4)"（`license-review` 2015-09・16 通）を通読し、2 通を置いた（`rounds/2015-09-license-review-oset-ns-fontana-inconceivable-observed.txt`・`rounds/2015-09-license-review-oset-ns-berkus-not-needed-observed.txt`）。OSET Public License の審査は §1.179 で読んであり、政府の側に有利な条（3.5B と 4）が一部の利用者に特権を与える、という論点と委員会の帰結（条を元の MPL 2.0 の形へ戻すよう求めた）はそこに在る。不平等を組み込む先例を作るのは愚かだ、という Simon Phipps 氏の文は、2015-10-13 の委員会報告が引いている（`rounds/2015-10-13-license-review-fontana-committee-report-fpl-observed.txt`）。この節は、§1.179 が読まなかった 2 通を足す。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Actually, I think such a license could be demonstrably OSD-conformant (or, to make this easier, conformant to the similar-in-spirit Free Software Definition of the FSF). But it is inconceivable that the OSI would approve such a license, and it might, and maybe does, expose some inadequacy in the Open Source Definition or some overly-literal interpretations of it."* | Richard Fontana 氏 2015-09-17（一部の者に他の貢献者より多くの権利を与えるライセンスについて） | **期待（審査は OSD の文言より広い）。** OSD に文字どおり合うことは、承認の十分条件ではない。§1.230 の Smith 氏 2018（運用は OSD の文言より厳しい）と同じ線である。ACD の OSD 逐条（`submission-osd.md`）が文字どおりの適合を示しても、審査はそれだけで終わらない。ACD が全員に同じ許諾を与えること（§2・§4）は、Fontana 氏が「承認するとは考えられない」とした非対称を持たない |
| *"Precisely. If governments already have immunity, the clause is not needed; if they don't, then the clause is bad. Either way, it is not something OSI should be endorsing."* | Josh Berkus 氏 2015-09-17（政府は既に著作権の請求で限られた救済しか受けない、という John Cowan 氏の指摘を受けて） | **審査者の攻め方の型。** 法が既にそうしているなら条は要らず、していないなら条は害になる、という二択で条を退ける。この型は、法の状態を述べ直すだけの条に当たる。ACD は法域ごとに効力が違う点に備える条を多く持つ（§3.3 の放棄が効かない法域での許諾、§12 の人格権など）。それらは「法が既にそうしているか」が法域で違うから要る、と答えられるが、答えを用意しておく必要がある |

**読み。** 2015 年の審査は、OSD の文字どおりの適合だけでは承認に足りないことと、要らない条や特権を与える条を二択で退けることを示した。ACD は特権を持たないので前者の非対称には当たらない。後者の型は、ACD の法域ごとの備えの条に向けられうる。

**逆側。** Berkus 氏の二択は、特権を与える条（OSET の政府への例外）に向けたもので、何も与えない説明の条には「害になる」の側が当たらない。その場合に残るのは「要らない」の側で、それは本文の長さの費用（1.4 草案の語数の議論）として現れる。Fontana 氏の文は、我々の OSD 逐条を軽く見る理由にもなりうる。逐条が示すのは必要条件であって十分条件ではない、と提出の文書が自分で書いているかは確かめていない。

**この節が establish しないこと。** OSET Public License の最終的な帰結は §1.179 の範囲で、この節は扱わない。ACD のどの条が Berkus 氏の二択の「要らない」側に読まれうるかは、条ごとには数えていない。

## 1.242 「取り消せない」と本文に書いても、それは自分への約束にすぎない —— Cowan 氏 2003 は無償の許諾の撤回を論じた（"Language question"・2003-05）（2026-11-15）

census の候補の外で、話題の語（撤回・放棄）に当たる未読の会話の 1 本（`license-discuss` 2003-05・18 通）を通読し、3 通を置いた（`rounds/2003-05-license-discuss-language-question-cowan-{irrevocable,promise,corporation}-observed.txt`）。著作権の承継とオープンソースの許諾の関係を問う会話である。撤回の可否はドシエで厚く扱われている（`QUESTIONS-FOR-COUNSEL.md` の問 (i)、Rosen 氏 2003 の *"Probably a new licensee with notice of the revocation can't obtain a license."*）。この節は、同じ年の別の人の文を足す。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"It's *far* from clear that the licenses you have already granted are somehow irrevocable.  I'd be interested to know under what theory you think they are."* / *"Even if we suppose that existing licensees (those who have already copied or distributed) are grandfathered, I see no possibility that new licensees can come into existence based on a grant that the grantor (or his successor in title) has explicitly revoked."* | John Cowan 氏 2003-05-07（*"IANAL, TINLA"* と断っている） | **逆側（§2.2・§2.5）。** 既に受け取った者は守られるとしても、撤回の後に初めて作品に出会う者は許諾を得られない、という見方で、問 (i) の狭い形（撤回を知った後に初めて出会う者）と同じ問いである |
| *"All that is, is a promise to yourself, and it's not binding, any more than your publishing a promise never to tell a lie is.  You may look bad if you break it, but there can't be any legal liability."* | John Cowan 氏 2003-05-08（本文が許諾を取り消せないと明記している、という提出者の返答へ） | **逆側（§2.2）。** ACD の §2.2（1.0 でも §2.2）は *"This Dedication is irrevocable."* と書く。Cowan 氏の見方では、その一文だけでは拘束しない。ACD はこれに §2.5（1.0 でも §2.5・他者の依拠を目的とし、撤回を主張しないと約束し、法が認める範囲で禁反言に服する）と §3.1（権利の放棄）を重ねて答えている |
| *"Furthermore, if the author transfers the copyright to a corporation whose chartered purpose is to maintain the license, then the corporation would be unable to revoke it through lack of appropriate powers."* | John Cowan 氏 2003-05-07 | **B12 の材料。** 撤回を防ぐ一つの形として、許諾の維持を目的とする法人へ著作権を移すことを挙げた。ACD は Dedicator が個人でありうる形で、この形を取っていない |

**読み。** 2003 年の議論は、「取り消せない」という本文の一文の効力を疑い、撤回の後に初めて出会う者の扱いを問題にした。ACD はこの疑いを見越して、§2.2 の一文だけでなく、§2.5 の約束と禁反言、§3.1 の放棄を重ねている。

**逆側。** Cowan 氏は法律家でないと断っており、これは決める側の判断ではない。一方で、問 (i) の Rosen 氏 2003（法律家）も同じ向きのことを書いており、二人の見方は一致する。§2.5 の禁反言について、Rosen 氏は 2004 年に、約束的禁反言は契約の法理で GPL のような単純な許諾には関係が無いと書いた（`against.md` #236）。ACD の重ねた答えがどの法域で効くかは、法律家の問いのまま残る。

**この節が establish しないこと。** 撤回の可否の法的な評価はしていない。

**追記（2026-11-15・同じ論点の 2015 年の記録）**: "Companies that encourage license violations"（`license-discuss` 2015-09）で、Lawrence Rosen 氏の通に引用された John Cowan 氏の文（Outlook 形式の引用で、`>` の付かない行に在る）は *"Since the right of an owner to revoke a bare license is inherent, it must be a promise not to exercise that right, and on what meeting of the minds, what consideration is that promise founded? Looks like a nudum pactum to me."*、Rosen 氏の答えは *"John, an open source license is not a nudum pactum. Consideration abounds in FOSS."* だった（`rounds/2015-09-license-discuss-violations-rosen-consideration-abounds-observed.txt`）。Rosen 氏の答えは、ライセンスの条件を対価と見る線で、何の条件も課さない ACD（§10.1）には移らない。`against-2.md` #324 が 2000 年と 2005 年の記録で同じことを書いており、これは 3 つ目の記録である。

**反映**: B12（法人に移せば取り消せない、という形・30 へ）/ B4 の撤回の論点の補強（`QUESTIONS-FOR-COUNSEL.md` の問 (i)・撤回の後に初めて出会う者・30 へ）。本文は変えない（§2.2・§2.5・§3.1 を重ねた答えが既に在る）。

## 1.243 「公有のライセンス」というものは無い、それは放棄の試みと代わりの許諾の組み合わせだ —— ACD の §3 と §4 の形そのもの（"Public domain license - Public Domain Customized"・2014-12〜2015-01）（2026-11-15）

census の候補の外で、話題の語に当たる未読の会話の 1 本（`license-discuss`・2 通）を通読し、1 通を置いた（`rounds/2015-01-license-discuss-pd-customized-woolley-no-pd-licence-observed.txt`）。公有に置きつつ特許の許諾も明示したい、という問いへの返答である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"There is no such thing as a public domain licence.  The documents are combinations of an attempt to abandon copyright, meaning you can't licence, and a, fallback, licence that attempts to give away as many rights as possible, even though you still own the copyright and moral rights."* | David Woolley 氏 2015-01-07 | **B4 の両面。** ACD は §3（1.0 でも §3・権利の放棄）と §4（1.0 でも §4・放棄が効かない範囲での許諾）を並べる。Woolley 氏の言う「放棄の試みと代わりの許諾の組み合わせ」は、この形を普通の型として描いている。同時に、放棄が成功すれば許諾するものが無い、という内側の緊張も指している |
| *"In most countries, including the UK, an attempt to abandon copyright will fail; if you want to put something in the public domain, you must die and then wait 70 years.  Many question whether anyone except the federal government can abandon it in the USA."* | David Woolley 氏 2015-01-07 | **逆側（§3）。** 放棄は多くの法域で効かない、という見方である。ACD の §3.3（1.0 でも §3.3・権利を手放すこと（surrender）は認めないが waive は認める法域では、Dedicator が waive する）と §4 の許諾は、この場合に備える。ACD は放棄が効くことに頼らない |

**読み。** 「放棄＋代わりの許諾」の形は、承認されなかった CC0 の審査（2012・提出は取り下げ・`review-precedents.md`）でも論じられた型で、承認済みでは Unlicense（献呈と列挙された許諾・2020）が同じ型に近い。Woolley 氏はそれを当然のように描いた。ACD の §3 と §4 の並存（B4）は、この型に属する。**訂正（2026-11-15・portfolio-30 の当て直し）**: 最初は「承認済みの CC0 の審査」と書いていた。CC0 は OSI に承認されていない（`board-decisions.md` §2f）。有利な側に寄った事実の誤りだった。

**逆側。** Woolley 氏は決める側の人ではない。「公有のライセンスというものは無い」という言い方は、ACD を「公有に置くもの」と紹介すると反論を呼ぶことを示す。ACD の入口が ACD を何と呼んでいるか（dedication と licence の両方の語を使う）は、この線で確かめる価値がある。

**この節が establish しないこと。** 放棄が各法域で効くかの評価はしていない（`jurisdictions.md` の範囲）。

**反映**: B4（§3 と §4 の並存の両面・30 へ）/ 入口（`SUBMISSION-MATERIALS.md` §1 の表の後の「ACD の呼び方」の段・public domain licence と呼ぶ所は grep で 0 件、残る曖昧さは散文の *the licence* が全体と §4 の両方を指すこと・portfolio-50 が 2026-11-16 に点検した）。本文は変えない。

## 1.244 「OSI に承認されることが、あなたにとってなぜ大事なのか」—— Phipps 氏が提出者に直接尋ねた（ViraTrace・2020-12）（2026-11-15）

census の候補の外の未読の会話の 1 本（"License-review Digest, Vol 97, Issue 8"・`license-review` 2020-12・3 通）を通読し、1 通を置いた（`rounds/2020-12-license-review-viratrace-phipps-why-approval-observed.txt`）。ViraTrace のライセンスの審査の一部で、同じ提出の他の通は `rounds/2020-12-license-review-viratrace-gdpr-observed-*` に在る。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I have to agree with Eric here - it seems likely you will have to choose between OSI approval and the protections you seek for your interests through these terms. Please can you succinctly explain why having your license be approved by OSI is important to you?"* | Simon Phipps 氏 2020-12-11 | **期待（提出の動機）。** 審査者は提出者に、承認がなぜ大事かを直接尋ねることがある。`against.md` #161 は、提出の理由が審査の入力になりうるとした（Fontana 氏 2019 など）。ACD の提出でも同じ問いが来うるので、答えを先に持っておく |

**読み。** 承認を求める理由は、審査者が明示に尋ねる問いである。ACD の場合、その答えは提出者（オーナー）の言葉で書かれる必要がある（B14）。

**逆側。** Phipps 氏の問いは、利益を守る条項と OSI の承認が両立しない提出に向けたもので、条件を置かない ACD とは場面が違う。ただし ACD の提出は「AI の自走の実験」と結びついて読まれうるので（#161・§1.233）、問われる可能性はむしろ高い。

**この節が establish しないこと。** ACD の提出で何と答えるべきかは、この節では決めない（オーナーの言葉の線）。

**反映**: against #161（提出の理由が審査の入力になる・その補強・30 へ）/ 入口（「承認がなぜ大事か」に答える用意を `OSI-APPROVAL-PLAN.md` に置く・答えはオーナーの言葉で B14 の下・50 へ）。

## 1.245 「なぜ CC0 を使わないのか」—— CC0 が長いのは世界中で確実に手放すためで、承認されないのは特許のためだ（"Svoboda for Approval"・2012-05）（2026-11-15）

`license-review` 2012-05 の会話（24 通）を通読し、5 通を置いた（`rounds/2012-05-license-review-svoboda-*-observed.txt`）。個人が WTFPL に似た短い公有の文を出し、どの法域でも公有に置きたいと述べた提出である。ACD と同じく、作品を公有に置く単独の起草者の提出で、審査者の返しは ACD にそのまま来うる。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Why not use CC0?"* | Richard Fontana 氏 2012-05-21 | **B10 の定型の問い。** 公有に置きたい提出者に、承認済みでない CC0 を勧めた。ACD は同じ問いに、CC0 が持たない特許の許諾と TDM の明示（B10 の G1）で答えることになる |
| *"It's only not OSI approved because it doesn't do what it can't do, and what people think it should do -- solve the problem of patents. It's only too long because that's what is needed to reliably disclaim copyright world-wide ... and failing that, it's a license that comes as close as possible to public domain. If the Creative Commons thought "This work has no copyright" was sufficient, they would have used it, no?"* | Russ Nelson 氏 2012-05-21（CC0 は承認されておらず長すぎる、という提出者の返答へ） | **有利な面（長さと構造・B10）。** 世界中で確実に手放すには長さが要り、それが効かなければ公有に限りなく近い許諾になる、という CC0 の構造（放棄と代わりの許諾・§1.243）を、長さの理由として擁護した。CC0 が承認されない理由を特許に置いた点は、ACD と CC0 の差に関わる（ただし 2012 年の CC0 の審査で実際に問題になったのは、特許の許諾が無いことではなく、特許を明示に除外する条（4(a)）だった。ACD が「埋める」と書けるのは、特許の許諾を持つという形の面だけである・2026-11-15 に portfolio-30 の指摘で直した） |
| *"If you must do this, at least state the problem you're trying to address that isn't already addressed by an OSI license. Heck, I'd argue that step should be a mandatory prerequisite for _any_ new license submission at this point."* | Tom Callaway 氏 2012-05-21（Fedora） | **期待（B10）。** 既存で解けない問題を述べることは、翌年には承認の規則の「新しいライセンスの理由」として明文になっている（§1.246）。ACD の提出は、この問いに最初の一画面で答える必要がある |
| *"The fact that "Public Domain" means so many different things in so many different jurisdictions should tip you off that what you want to do is not trivial. CC-0 (aside from its patent issues) makes an admirable attempt to "workaround" this fact to achieve extremely permissive end-results when it is not possible to abandon copyright. If there was an "easy" way to universally place works in the Public Domain (for all meanings of PD), it would already have been done. The fact that CC-0 is long is because it is thorough."* | Tom Callaway 氏 2012-05-21 | **有利な面（長さ）と期待。** 公有に置く文が長いことは、徹底していることの印として読まれた。ACD の長さ（1.4 草案の語数の議論）にとって、「短くすべき」とは逆向きの、審査者の側の文である |
| *"That sort of thing would qualify as a "crayon license"."* | Bruce Perens 氏 2012-05-21（短い公有の文について） | **逆側（B1）。** 短く、法律家の手を経ない公有の文は、crayon license と呼ばれた。ACD は短くはないが、単独の起草者の文である点で同じ型に見られうる |

**読み。** 公有に置く単独の提出に、審査者は「なぜ CC0 ではないのか」「何の問題を解くのか」を返し、CC0 の長さと構造を「必要だから」「徹底しているから」と擁護した。ACD は CC0 と同じ放棄と代わりの許諾の構造に、CC0 が欠く特許の許諾を足した形で、この審査の線の上では「CC0 の承認を妨げた点を埋めたもの」として説明できる。

**逆側。** 2012 年の Nelson 氏の「承認されないのは特許のため」は、CC0 の提出（2012-02）が取り下げられた事情の一つの見方で、委員会の判断の文ではない。Callaway 氏は Fedora の立場で書いており、OSI の決める側ではない。ACD の長さは「徹底」として読まれうるが、CC0 よりずっと長い。CC0 1.0 の全文は 998 語、1.4 草案は前文から END OF TERMS まで 5,561 語（T72 の後）で、約 5.6 倍である（どちらも Python の `split()` で 2026-11-15 に数えた。CC0 の本文は npm の `mdn-data` が同梱する LICENSE の写し（116 行）で数えた。写しはアーカイブにも OSI の一覧にも無く、外部の取得は今回行っていない・portfolio-30 の指摘で数えた）。Callaway 氏の「長いのは徹底しているから」が CC0 の長さを擁護したものなので、その 5.6 倍の長さにまで同じ擁護が及ぶとは言えない。

**この節が establish しないこと。** Svoboda の提出の帰結（取り下げか放置か）は確かめていない。

**反映**: B10（G1 の説明に「CC0 の承認を妨げた特許の点を埋める」を足す候補・30 へ）/ 入口（最初の一画面で「既存で解けない問題」に答えているかの点検・50 へ）/ 入口（`SUBMISSION-MATERIALS.md` の長さの行。1c は「閾値のために語を削らない」を維持し、長さは入口の一画面で先に認める、と 2026-11-16 に判断した。CC0 との比（約 5.6 倍）を同じ行に置く提案を 50 へ送った）。

## 1.246 2013 年の承認の規則 —— 確定前に出す、新しいライセンスの理由、最も近い承認済みとの比較、法的な分析、増殖の区分（"Akshar License 1.0 Final Draft"・2013-05）（2026-11-15）

`license-discuss` 2013-05 の会話（8 通）を通読し、2 通を置いた（`rounds/2013-05-license-discuss-akshar-{fogel-discourage,villa-approval-rules}-observed.txt`）。Apache-2.0 に近い新しいライセンスの事前の相談である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"We generally very strongly discourage the creation of new open source licenses.  There are too many already, and each new license increases the burden on developers and legal departments.  There should be a convincing reason why no existing license will even come close to serving your purposes before you try creating a new license, IMHO."* | Karl Fogel 氏 2013-05-03（提出の動機を尋ねた同じ通で） | **B10 の定型。** 新しいライセンスへの基本の姿勢で、2008 年の Nelson 氏（§1.238）、2010 年の Perens 氏（§1.236）と同じ線 |
| *"1. Submit before final, whenever possible, to allow for revisions based on feedback"* / *"**2. Clearly state rationale for a new license**"* / *"**3. Compare to and contrast with the most similar OSI-approved license(s)**"* / *"4. Provide results of any legal analysis available"* / *"**5. Recommend which license proliferation category is appropriate**"* | Luis Villa 氏 2013-05-07（承認の規則の頁を示して） | **手順の材料（規則の過去の版）。** 2013 年の規則は、確定の前に出して意見で改訂できるようにすることを第一に挙げた。ACD は版を確定して凍結し、指摘は次の版で直す手順を取る（`REVISION-PROTOCOL.md`）。審査に出す版は凍結されるが、次の版で改訂できるので、「意見で改訂できる」という趣旨とは食い違わない。2〜5 は現行の提出の文書（`submission-reference.md` の増殖の区分の推薦など）が答えている |

**読み。** 2013 年の規則の 5 項目のうち、2・3・5 は太字で示され、提出の必須として扱われていた。ACD の提出の文書はこの 3 つに答える形を持つ。1 の「確定前に出す」は、ACD が `license-discuss` に先に出した経路（2026-08）と、次の版で改訂する手順に合う。

**逆側。** 4 の「法的な分析の結果」は、ACD には出せるものが無い（B1）。また、規則の 1 を「審査中の本文を直接直す」と読む審査者には、凍結して次の版で直す手順は遅く見えうる（§1.230 の C-FSL で、指摘が改訂版で扱われないことが延期の理由になった）。

**この節が establish しないこと。** 2013 年の規則が現行の規則とどう違うかの全文の比較はしていない（`review-rules.md` の範囲）。

**反映**: 入口（`SUBMISSION-MATERIALS.md` の「2013 年の規則の 5 項目との対照」の段と、§1 の表に足した「増殖の区分」の行・portfolio-50 が 2026-11-16 に足した）/ B1（規則の 4 に出せるものが無いことの記録・30 へ）。
## 1.247 表記だけの改訂でも、改訂版は「OSI 承認済み」と呼べない —— 承認は 1 つの本文に付く（MirOS Licence の表記の変更・2013-09）（2026-11-15）

"Suggested MirOS Licence wording change: editorial or substantial?"（`license-review` 2013-09・4 通）を通読し、2 通を置いた（`rounds/2013-09-license-review-miros-{fontana-editorial-not-approved,villa-roughly-right}-observed.txt`）。承認済みの MirOS Licence の作者が、ハイフンでの改行を避けるために語順を少し入れ替える変更は「表記の変更」で版を改めずに済むか、と尋ねた会話である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"My personal view is that this revised version should not be characterized as an OSI-approved license, even if the revisions here are justifiably considered 'merely editorial'. You could say it's very similar to an OSI-approved license, and point out the degree of similarity."* | Richard Fontana 氏 2013-09-10 | **手順の材料（承認の後の版）。** 承認は一語単位で 1 つの本文に付き、表記だけの改訂でも新しい本文は承認済みではない。ACD の §16.4（1.0 でも §16.4）が「名と識別子は 1 つの固定した本文を指し続ける」と書くのは、この運用に合う。同時に、承認の後に ACD の版を改めれば、その版は改めて審査を要する |
| *"I think that's roughly right, though I'm open to alternative points of view. (I'd make an exception for cases where there is no "standard" license (i.e., the BSDs/MITs) where clarifying the default text we present can be a useful service to the community and doesn't make life substantially more difficult for those trying to handle the number of licenses out there.)"* | Luis Villa 氏 2013-09-11 | **同じ向き。** 例外は「標準の本文」の無い BSD・MIT に限られ、ACD には当たらない |

**読み。** 承認は特定の本文に付き、版を改めれば承認は引き継がれない。ACD が 1.0 から 1.4 まで版を重ねてきたことは、承認の後には「版ごとに審査」という費用に変わる。

**逆側。** 承認を受けた版で版の改めを止めれば、この費用は生じない。ただし欠陥が見つかったときに直せない（直せば未承認の版になる）。ACD の手順（凍結して次の版で直す）は、承認の後にはそのまま「次の版も出す」ことになり、`against.md` #320（短い間の版の多さ）の費用と重なる。

**この節が establish しないこと。** OSI が承認済みの本文の誤字の訂正をどう扱ってきたかの全体は確かめていない。

**反映**: 入口（`OSI-APPROVAL-PLAN.md` の段 11「承認後」に、承認は 1 つの本文に付き版を改めた本文は承認済みと呼べないこと・portfolio-50 が 2026-11-16 に足した）/ against #320（承認の後にも版の多さが費用になる・30 が足した）。

## 1.248 指摘に本文で答えず「FAQ で説明する」と先送りした提出への評価は「meh」だった（ESA-PL・2018-05）（2026-11-15）

"ESA-PL Weak 2.3"（`license-review` 2018-03〜05・4 通）を通読し、1 通を置いた（`rounds/2018-05-license-review-esa-pl-perens-faq-not-text-observed.txt`）。欧州宇宙機関のライセンスの審査である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Your responses offer to correct an obvious error in the license and punt all of the other issues, offering to clarify them in a FAQ rather than to go back to the lawyers for more drafting."* / *"So, because of this reluctance to go back to the lawyers, I'd have to say that my opinion so far is "meh". I don't strongly reject approval of the license, but neither do I see a need to speak in its favor."* | Bruce Perens 氏 2018-05-07 | **不利な面の候補（本文の外で答えること）。** 指摘に本文の改訂でなく説明の文書で答えると、審査者は支持しない。ACD は条文の論点の多くに、本文を変えずに逐条の説明や想定問答（`ACD-1.0.review-responses.md` など）で答える判断をしてきた（たとえば §1.232 の §2.6、§1.238 の型板、§1.239 の §16.4）。審査で同じ形を取れば、Perens 氏の「meh」の線に読まれうる |

**読み。** 審査者が求めるのは本文での答えで、外の文書での説明は、本文を直す手間を避けたものと読まれうる。ACD の「本文を変えない」判断は、どれも「本文が既にその読みを持つ」ことを理由にしてきたが、審査ではその理由を本文の文言で示す必要がある。

**逆側。** 本文が既に答えている論点を、さらに本文に書き足すのは語数の費用になる（§1.241 の Berkus 氏の二択の「要らない」側）。Perens 氏の文は、明らかな誤りを含む本文について、その他の論点を全部先送りした応答に向けたもので、本文が答えていることを示す説明まで否定してはいない。

**この節が establish しないこと。** ACD の「本文を変えない」判断のうち、どれが審査で「先送り」と読まれうるかは数えていない。

**反映**: 1c 種（「本文を変えない」判断の一覧に、その読みを本文のどの文言が持つかを並べる点検・1c へ）/ 入口（`SUBMISSION-MATERIALS.md` §2 の冒頭「答えは本文の語を引いて書く」・portfolio-50 が 2026-11-16 に点検し、50 問のうち条番号と逐語 18・条番号だけ 23・どちらも無い 9 と数えた）。

## 1.249 「Autonomous」を名に持つ先行のライセンス —— 後の CAL の前身「Autonomous Agent License」（2019-01）（2026-11-15）

"Developing a new open source license"（`license-discuss` 2019-01・7 通）を通読し、2 通を置いた（`rounds/2019-01-license-discuss-autonomous-agent-license-{lindberg,perens}-observed.txt`）。Van Lindberg 氏が Holo のために作っていた強いコピーレフトのライセンスの事前の告知で、その告知（Holo の文）が "Autonomous Agent License" と呼んでいた。Bruce Perens 氏はその文を自分の通に貼って条項を批判した。この提出は後に Cryptographic Autonomy License（CAL・2020 承認）として審査された（`rounds/2019-04-license-review-cal-approval-observed-*`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Unlike other current open source licenses, the Autonomous Agent License will require software that implements a compatible API or publicly performs the API to also be open source."* | Holo の告知の文（Bruce Perens 氏 2019-01-31 の通に「this part:」として貼られたもの。引用符も `>` も無いので、通の差出人の文と取り違えやすい） | **名の記録（B6・`against.md` #161）。** 「Autonomous」を名に持つライセンスが、ACD より前に審査の場に出ていた。名は提出者の側が付けたもの |
| *"So, unfortunately I really have to recommend in the strongest way that a license incorporating that term not be approved."* | Bruce Perens 氏 2019-01-31 | **批判の向き。** 条項（API の実装への条件）に向けたもので、名には向いていない |

**読み。** ACD の名の「Autonomous」は、審査の場で初めての語ではない。先行のライセンスは、名ではなく条項で批判され、名を変えて（Cryptographic Autonomy License）承認された。

**逆側。** 名が変わった理由はこの会話の範囲では分からない。名の変更が審査の指摘によるものなら、#161 の Kuhn 氏の「名がその主題に唯一ふさわしいライセンスに見せる」の線と重なりうる。ACD の名が先行の名と混同されうるかも確かめていない。

**この節が establish しないこと。** Autonomous Agent License から CAL への改名の理由。

**反映**: B6（「Autonomous」を名に持つ先行のライセンスの記録・30 へ）。

## 1.250 「著作権の拡張は、ライセンスの強制に役立つ場合でもオープンソースに悪い」—— Perens 氏の原則（"Open Source and the extension of copyright"・2019-01）（2026-11-15）

`license-discuss` 2019-01 の会話（2 通）を通読し、1 通を置いた（`rounds/2019-01-license-discuss-extension-of-copyright-perens-observed.txt`）。オープンハードウェアのライセンスが、機能的で著作権の及ばない回路図の実装まで覆おうとすることへの批判である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"In addition, I think there's a principle here. Extension of copyright is bad for Open Source, even if it helps us enforce our licenses more effectively. It will always work against us to a greater extent that it can be put to work for us."* | Bruce Perens 氏 2019-01-31 | **点検の材料（データ・モデル・著作権以外の権利）。** ACD はデータ、モデルの重み、著作権以外の権利（データベース権・特許など）を許諾の範囲に含める。その書き方が「そこに権利がある」と主張するように読まれれば、Perens 氏の原則に当たる。ACD の §2.7（1.0 でも §2.7）は *"This Dedication reaches only rights the Dedicator holds, now or in future."* と書き、権利があるかどうかを主張しない形を取っている |

**読み。** ACD は権利を与える文書で、権利の範囲を広げて強制する文書ではない。§2.7 は、権利が無いところに権利を主張しない形をとっており、Perens 氏の原則に合う。

**逆側。** 許諾の範囲にデータやモデルを名指すこと自体が、「それらに権利がある」という前提を置いているように読まれうる。とくに §6（TDM と機械学習）と §1.3（Work の定義）の書き方は、Perens 氏の役の審査者がまず突く所になる（模擬委員会の点検の対象）。

**この節が establish しないこと。** ACD の各条が権利の存在を前提しているかの条ごとの点検はしていない。

**反映**: THIRD（`ACD-1.4-THIRD-CLARITY-TRIAL.md` の 16.4 節・模擬委員会の Perens 氏の役で点検した。§6.4 の "Whether a right subsists in any such thing is not decided here and does not need to be." と §2.7・§6.1 が答えており、本文は変えない。逐条の §6.4 の行へは 1c が足す）。

## 1.251 法的な文書に「拘束しない部分」は無い、前文は意図の解釈に使われる —— ACD の前文は「informative」と書くが、それでも読まれる（"Invariant manifestos …"・2020-12）（2026-11-15）

`license-discuss` 2020-12 の会話（3 通・census の会話の始まり 2020-12-27）を通読し、2 通を置いた（`rounds/2020-12-license-discuss-invariant-manifestos-{chestek-no-non-binding,atkinson-preamble}-observed.txt`）。プロジェクトの価値を述べる変更不可の宣言をライセンスに添える案への返答である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"It is a misperception to think that there is any "non-binding" part of a legal document. Everything in there is there for a reason (or should be). There may be parts that don't describe an action, but contract interpretation often involves determining the intent of the parties. This is often the role of the recitals."*（同じ通で、GPLv2 の前文の意図の文は曖昧な条を利用者の自由の側に読むよう指示する、と続ける） | Pamela Chestek 氏 2020-12-28（個人のアドレスから） | **両面（ACD の前文）。** 1.4 草案の前文は *"PREAMBLE (informative; not part of the operative terms)"* と見出しを付け、*"Sections 1 to 16 are the operative terms. This preamble is not, and nothing in it qualifies them."* で終わる（1.0 にも同じ見出しの前文が在る）。Chestek 氏の線では、それでも前文は意図の判断に使われる。有利な面は、前文の *"This Dedication is written for works that are meant to be learned from."* が、曖昧な条を学ぶ側・受け手の側に読む方向に働くことである。逆側は、前文の他の道具への評価（*"silent or hostile"*）も意図の一部として読まれることである（この語は 2026-11-15 に portfolio-1c が T72 で *"leave a gap"* に変えた・`ACD-1.4-THIRD-CLARITY-TRIAL.md` §15.8） |
| *"The GPL's preamble provides a non-legalese summary of the effect of the license, and explains the intent of the license."* / *"a much more neutral tone would have worked as well."*（間で、GPL の前文は価値を述べ強い語（threatened・surrender）を使っており、許される範囲の境の半ばまで来ている、と書く。原文の引用符とダッシュは写しで文字化けしているので、その部分は逐語で引かない） | Lukas Atkinson 氏 2020-12-27 | **点検の材料（前文の調子）。** 審査に近い参加者は、前文の調子を「許される範囲」の物差しで測る。ACD の前文の *"the existing tools are silent or hostile"* は、他のライセンスへの評価を含む強い語で、同じ物差しに掛かりうる |

**読み。** ACD の前文を「informative」と明示しても、解釈では意図を示す文として読まれる。前文の意図（学ばれるための作品）は ACD に有利に働くが、他の道具への強い評価の語は、その分だけ審査の物差しに掛かる。

**逆側。** Chestek 氏の文は契約の解釈の一般論で、許諾（ライセンス）が契約として読まれない法域では前文の役割は違いうる。「nothing in it qualifies them」は、前文が条の範囲を狭めも広げもしないという ACD の意図を述べており、意図の判断に使われること自体とは矛盾しない。

**この節が establish しないこと。** ACD の前文のどの語が「強すぎる」と読まれうるかの点検はしていない。同じ線の記録として、`ACD-1.0.review-readings-6.md` §1.450（Nelson 氏 2002「前文も別の解説も条文の解釈に使われる」）と `against.md` #124 の「逆向きの危険」の段を併せて読む。

**反映**: 1c THIRD §15.8（T72・PR 3249 で前文の "silent or hostile" を "leave a gap" へ変えた。前文の意図の文 "written for works that are meant to be learned from" は残した）→ T73（`ACD-1.4-THIRD-CLARITY-TRIAL.md` の 15.9 節）で "where that assumption fails" へ再び改めた（"leave a gap" は B10 で問われる当の語で、前文が当然のように述べると答えの先取りに読まれうるため）。

## 1.252 米国では、ソフトウェアに法的に認められる人格権は無い（"exploring the attachment between the author and the code"・2020-02〜03）（2026-11-15）

`license-discuss` 2020-02〜03 の会話（11 通）を通読し、1 通を置いた（`rounds/2020-03-license-discuss-author-attachment-chestek-moral-right-observed.txt`）。作者と自分のコードの心理的な結びつきを問う会話である。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"There is no legally cognizable moral right in software in the US."* | Pamela Chestek 氏 2020-03-01（個人のアドレスから） | **§12 の範囲の確認。** ACD の §12（1.0 でも §12・人格権の放棄と不行使）は、米国では及ぶ対象がほとんど無い。§12 が効くのは、人格権を認める法域（日本・EU など）である。条が「米国では要らない」と読まれることは、§1.241 の Berkus 氏の二択の「要らない」側に当たるが、法域で違うから要る、という答えが立つ |

**読み。** ソフトウェアについては、§12 は人格権を持つ法域の作者が ACD を使うために要る条で、米国の審査者には要らない条に見えうる。**ただし Work はソフトウェアに限らない**（§1.3 は視聴覚の素材も含む）。米国にも視覚芸術の作品の人格権（17 U.S.C. §106A・VARA）があり、その放棄には署名した書面が要る。§12.1 の放棄はその方式を満たさない（`against.md` #152 が「米国で直接効く 2 つの規定」の 1 つとして記録している）。Chestek 氏の文は *"in software"* と限っているので、文そのものは正しい。**訂正（2026-11-15・portfolio-30 の当て直し）**: 最初は「米国では §12 の及ぶ対象がほとんど無い」と書き、Work をソフトウェアに限った読みで有利に寄せていた。

**逆側。** 同じ会話で Chestek 氏は、ソフトウェアの作者は作品への強い所有の感覚を持たないことが多い（機能的だから）という個人の経験を書いている。ACD が人格権を重く扱うことは、ソフトウェアの実務からは過剰に見えうる。

**この節が establish しないこと。** 各法域でソフトウェアに人格権がどう及ぶかの評価はしていない（`jurisdictions.md` の範囲）。

**反映**: 1c 種（§12 が「法域で違うから要る」ことを逐条の §12 の行で示しているかの点検・THIRD §15.6 の掃引の対象・1c へ）。

## 1.253 「論点なし」とした会話を全文で当て直して拾った 4 点 —— 公の許諾は取り消せないものとして扱われてきた、無条件の許諾は献呈と取られうる、CC0 は FSF と共にソフトウェアに推奨された（2011）、提出者は 3 つを立証する（2026-11-16）

2f は帯の会話を、決める側の通を先頭の 220〜300 字で切った抜き出しで読み、35 本を「新しい論点は無い」とした。portfolio-30 が同じ会話の 1 つ（2020-08 の BSD の変種）から、切った先に在った Rosen 氏の文を拾った（portfolio-30 の PR 3273 で `review-readings-3.md` に足す節）ので、「論点なし」とした 75 本を切らずに全文で ACD の論点の語に当て直した。新しく拾ったのは次の 4 通で、rounds に置いた（`rounds/2004-03-license-discuss-must-read-cowan-irrevocable-expectation-observed.txt`・`rounds/2000-03-license-discuss-rms-position-cowan-unconditional-dedication-observed.txt`・`rounds/2011-08-license-discuss-dual-licence-linksvayer-cc0-fsf-observed.txt`・`rounds/2013-11-license-review-sfsl-berkus-burden-three-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The FLOSS world has always treated its public licenses as irrevocable, though it tolerates new versions being issued under incompatible or even proprietary licenses. Anyone who tries to revoke a public license outright with retroactive force is acting against community expectations"* | John Cowan 氏 2004-03-15（SCO の件で、他者が依拠していれば撤回は禁反言で止められる、と同じ通で続ける） | **有利な面（§2.2・§2.5）。** 共同体の期待と依拠を撤回の歯止めとする線で、ACD の §2.5（1.0 でも §2.5・他者の依拠を目的とし、法が認める範囲で禁反言に服する）の考え方そのものである。同じ人の 2003 年の疑い（§1.242）と並べると、Cowan 氏は「本文の一文では拘束しないが、依拠と期待が歯止めになる」と読んでいたことになる |
| *"An *unconditional* public license like "Anyone may copy, distribute, publicly perform, and make derivative works, without restriction" might be taken as a dedication to the public domain. But the various free licenses are conditional"* | John Cowan 氏 2000-03-28 | **両面（B4・`against-2.md` #324）。** 何の条件も課さない許諾は献呈と取られうる。ACD は自ら献呈と名乗るので、この読みと食い違わない。一方で、条件付きのライセンスが対価を通じて撤回に耐えるという線（#324）には乗らない |
| *"The exception that proves the rule is the CC0 public domain dedication, which is GPL-compatible and with the FSF we recently recommended for software if public domain is the intention."* | Mike Linksvayer 氏 2011-08-08（Creative Commons の側から書いており、"we" は CC を指す。CC はソフトウェアに CC ライセンスを勧めない、という流れで） | **FSF の扱いの手がかり。** 2011 年に CC と FSF は、公有を望む場合のソフトウェアに CC0 を推奨した、と CC の側が述べた。§1.229 で出典が無いとして取り下げた「FSF の扱い」について、一次資料の手がかりになる。ただし FSF 自身の文ではない |
| *"As a new license proposer, the burden is on you to prove to a majority of the OSI board that your license is: - open source - legally valid - needed"* / *"And note that we haven't even begun the non-proliferation arguments yet, which will also be substantial."* | Josh Berkus 氏 2013-11-07 | **基準（B1・B10）。** 立証の責任は提出者にあり、その中身は「オープンソースであること・法的に有効であること・必要であること」の 3 つで、増殖の議論はその後に来る。2015 年の 4 つの問い（§1.179）と同じ線で、「法的に有効」は B1（法的レビューが無い）、「必要」は B10 に当たる |

**読み。** 切った抜き出しで「論点なし」とした会話にも、ACD に当たる文が残っていた。撤回について、Cowan 氏は 2003 年には本文の一文の効力を疑い、2004 年には共同体の期待と依拠を歯止めとした。ACD の §2.2 と §2.5 の重ね方は、この両方に答える形である。

**逆側。** Cowan 氏も Berkus 氏も、文を書いた時点で決める側の役にあったかは、この節では確かめていない（Berkus 氏は "the burden is on you to prove to a majority of the OSI board" と、理事会の側から書いている）。Linksvayer 氏の文は CC の側の報告で、FSF がその後に CC0 の特許の除外をどう扱ったか（2022 年の Fedora の変更など）は別の問いである。FSF の現在の見解は、FSF の一次資料に当てるまで読みに使わない。

**この節が establish しないこと。** 当て直しは語で当てたもので、語に当たらない読み落としは残りうる（測り方の限界）。

**反映**: B1・B10（Berkus 氏 2013 の 3 つの立証の責任・30 へ）/ against #324（Cowan 氏 2000 の無条件の許諾と献呈・2004 の期待と依拠・30 へ）/ 入口と B10（FSF の一次資料は 2026-11-16 にオーナーの許可で取得した: `rounds/2026-11-16-fsf-license-list-and-debian-dfsg-public-domain-snapshot.txt`。FSF は CC0 をソフトウェアに勧めない理由を *"as CC0 has a term expressly stating it does not grant you"* *"any patent licenses."* と特許の明示の除外に置き、献呈と代わりの許諾の組み合わせ（Unlicense）は GPL と両立するとする。Debian Wiki は CC0 型の献呈をソースがあれば DFSG を満たしうるとする。特許を明示に許諾する ACD には FSF の理由は当たらないが、FSF も Debian も ACD を評価していない。**逆側（同じ写しの 0BSD の項）**: FSF は表示の保存を求めないライセンス（0BSD・Expat0）を、GPL と両立する自由なライセンスと認めつつ *"We recommend that developers choose a license that clearly requires preserving notices for their own works"* *"because of the confusion and antisocial effect that is the result of the 0BSD License."* と勧めない。ACD も表示を求めない（§10.2）ので、FSF の目ではこの線に入りうる・30 へ）。

## 1.254 承認の投票の前に、既存の団体と重なる略称を変えるよう求めた理事 —— 「ACD」の略称は確かめていなかった（OIN License・2020-12）。リストの参加者は相談すべき法律家の代わりを務めない（2020-10）（2026-11-16）

census の決める側の一覧（DECIDERS）に、OSI の公の宛名で書いていた 3 人（Jim Jagielski 氏・Patrick Masson 氏・VM (Vicky) Brasseur 氏）が入っておらず、足して回すと未読が 4 本出た（portfolio-9b に DECIDERS への追加を頼んだ）。4 本を読み、2 本から 3 通を置いた（`rounds/2020-12-license-review-oin-{berkus-acronym,brasseur-spdx-identifier}-observed.txt`・`rounds/2020-10-license-review-digest95-brasseur-consult-lawyer-observed.txt`）。残る 2 本（2017-01 Groups/Communities・2019-08 GPL-3.0's anti-DRM tivoization clause）は新しい論点が無かった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Aside from the required wording changes, the other major issue with this license is the short name of the license itself, which seems like a pretty clear trademark infringement in my non-lawyer eyes."* / *"Since this license is unaffiliated with that organization (unless I've missed something), even were it otherwise acceptable I'd request a change of license acronym before voting to approve it."* | Josh Berkus 氏 2020-12-27（略称「OIN」が Open Invention Network と重なることについて） | **点検の材料（B6・名前）。** 承認の投票の前に、既存の団体と重なる略称を変えるよう求めた。ACD の略称「ACD」と識別子「ACD-1.x」が既存の団体や商標と重ならないかは、ドシエで確かめていなかった。**2026-11-16 に確かめた範囲**: 画像ソフトの ACDSee の会社名は "ACD Systems International Inc."（acdsee.com のフッター *"© Copyright 1993 -  ACD Systems International Inc."*・同日に取得）で、「ACD」を名に持つソフトウェアの会社が実在する。「ACD」が商標として登録されているか、どの範囲で登録されているかは確かめていない |
| *"The license was also submitted to SPDX for inclusion in its list. Earlier today the team changed the proposed license identifier to avoid potential confusion with Open Invention Network"* | VM (Vicky) Brasseur 氏 2020-12-28（2018〜2020 年に OSI の宛名でも書いていた） | **点検の材料（B6・B11）。** SPDX の側も、既存の団体との混同を避けるために識別子を変えた。ACD を SPDX に出すとき（B11）にも同じ点検が来うる |
| *"However, before doing moving the conversation to license-discuss, I advise you take the recommendation of several list members and consult a lawyer experienced in license drafting to have them review and rework the document first. The members of license-discuss are unlikely to be happy with playing the role of the lawyer you should be consulting instead. ;-)"* | VM (Vicky) Brasseur 氏 2020-10-20 | **不利な面（B1）。** リストは法律家の代わりにならない、という線で、`review-readings-2.md` §1.233 の Chestek 氏 2020（「review は本物のライセンスに限る」）・§1.234 の Perens 氏と同じ向き。ACD が `license-discuss` に出した 1.0 の議論も、法律家の目の無い文書として同じ物差しで見られうる |

**読み。** 略称が既存の団体や商標と重なることは、2020 年の審査で承認の投票の前に直すべき点として扱われた。ACD の名前の点検（B6）は、これまで「Autonomous」の語（§1.249）と名の主張（#112）を見てきたが、略称「ACD」の衝突は見ていなかった。

**逆側。** OIN の件は、ライセンスの略称が同じ分野（オープンソースの特許）で長く活動する団体の名と同じだった例で、「ACD」と画像ソフトの会社の名は分野が違う。Berkus 氏は自分の目を *"non-lawyer eyes"* と断っている。商標の衝突が実際にあるかは、登録の調査（法律家の問い）を経ないと分からない。略称を変える費用は大きく（識別子、§16.4 の名の規則、既に配った版）、確かめずに変える理由にはならない。

**この節が establish しないこと。** 「ACD」の商標の登録の有無と範囲。ACD の名前が審査で問われるかどうか。

**反映**: B6（略称「ACD」の衝突は against の新しい行にせず B6 の段に置いた。先例の引き金は同じ分野でのはっきりした衝突で、ACD には記録の範囲で同じ分野の衝突が無い。ACD Systems の実在と商標の検索が未了であることを明記・portfolio-30）/ B11（SPDX の側の識別子の変更）/ against #1（Brasseur 氏の「提出前に法律家に見てもらう」という期待）/ 入口（法律家への問いに「ACD」の商標の調査を足すかの判断・`QUESTIONS-FOR-COUNSEL.md`・50 へ）。

## 1.255 新しいライセンスを書く前に、既存のどれも合わない理由をリストに説明せよ（2003）。承認済みのほとんどは法的な助言を受けて書かれた（2004）。長さは確かさの代価でもある（2004）（2026-11-16）

Ian Lance Taylor 氏（`ian at airs.com`・両リストで 232 通）の発言した会話のうち、census の候補の外の 31 本を 5 人で分けた（portfolio-9b の分担）。portfolio-2f は 2002〜2004 年の 15 本を通読した。各通を切らずに ACD の論点の語（献呈・取り消し・特許・増殖・法律家・承認・長さ）で当て直してから記録した。4 本から 4 通を置いた（`rounds/2003-07-license-discuss-license-idea-taylor-first-step-observed.txt`・`rounds/2004-02-license-discuss-{simple-permissive-taylor-length-soundness,non-lawyers-taylor-legal-advice,non-lawyers-rousskov-100-page}-observed.txt`）。残る 11 本は、GPL の派生物の範囲や再頒布の制限の相談で、ACD に当たる新しい論点は無かった。**Taylor 氏が OSI の理事や委員だったという一次の記録は見つかっていない**（portfolio-50 の判断で DECIDERS には足さない）ので、ここでは常連の参加者の発言として読む。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"If you can't use an existing license, then your first step should not be to write a license, but instead to write to the list and explain clearly why no existing license will work for your situation."* 続けて、リストの答えは 3 つ —— *"1) actually, license X satisfies your needs; or 2) you're right, there is no current license for your needs, but what you want to do would be OSI approved, so go ahead and write a license; or 3) ... because what you want to do would not be OSI approved."* | Ian Lance Taylor 氏 2003-07-16（"license idea"） | **B10 の手順の材料。** ACD は「既存のどれも合わない理由」を `ACD-OSI-BOTTLENECKS-B10.md`（G1）に書いている。**逆側**: ACD は理由を先に問わず、本文を書いてから 1.0 を `license-discuss` に出した。その問いへの返信は無い（`REVIEWERS.md`）ので、リストの答え 1)〜3) のどれも得ていない |
| *"I don't see how it serves the purposes of the OSI to approve a license which is intended to be identical to an existing license merely because programmers can't read."* / *"for people who want something like the MIT license, I recommend the Academic Free License, which is rather more likely to be legally sound. However, for that very reason, it is much longer."* | Ian Lance Taylor 氏 2004-02-08（"For Approval: Simple Permissive License"） | **B3 の両面。** 長さが法的な確かさの代価になりうる、という参加者の読みで、ACD の長さ（B3）を擁護する向きに使える。同じ提出は、委員会が「既存と同じ効果は改善ではない」として退けた（`board-decisions.md` の 2004 年の表）。**逆側**: Taylor 氏の文で長さを正当化したのは、法律家（Rosen 氏）が起草した AFL の長さである。ACD の長さは法律家が起草した結果ではない（B1） |
| *"Also, note that most of the OSI approved licenses were in fact written with the benefit of legal advice, including the GPL."* | Ian Lance Taylor 氏 2004-02-13（"Inappropriate postings from non-lawyers"） | **不利な面（B1）。** 承認済みのライセンスの起草に法的な助言が伴うのが普通だった、という 2004 年の観察。`review-rules.md` §1.141（法律家の分析は 2007 年 12 月まで提出の要件）と同じ向き |
| *"For example, open source software with new 100 page legal license attached has fewer chances succeeding in real world, no matter how many lawyers are happy about that license."* | Alex Rousskov 氏 2004-02-13（同じ会話） | **不利な面（B3・B2）。** 長さは法律家の満足と別に、使う人を遠ざける。ACD の本文は 1.4 草案で 5,000 語を超える（`ACD-1.4-DRAFT.txt` の `This draft:` の行）。**逆側**: Rousskov 氏は同じ通で、使う人の必要と法の必要の「釣り合い」を求めており、短さだけを求めてはいない |

**読み。** 2003〜2004 年のリストの常連は、新しいライセンスの前に「既存のどれも合わない理由」を問い、長さを確かさの代価と認めつつ、使う人への費用としても数えていた。ACD の答えの場所はどれも既に在る（B10 の G1、B3 の長さの説明、B1 の法律家への問い）。

**逆側。** どれも委員会の決定ではなく、参加者の発言である。Taylor 氏の役は確かめられていない。2004 年の承認の手続き（法律家の分析を求めていた時期）は、提出の日の手続きとは違う。

**この節が establish しないこと。** 審査者が提出の日に「既存のどれも合わない理由」を先に問うかどうか。長さが ACD の確かさを上げているかどうか（法律家の目を経ていないので、それは測れない）。

**反映**: B10（「書く前にリストに理由を尋ねよ」と、ACD が本文を先に書いて出した逆側の 1 文・portfolio-30）/ B3（長さを確かさの代価とする Taylor 氏の読みと Rousskov 氏の逆の文を対で置き、どちらも法律家の起草を前提にするので ACD には半分しか当たらない、と書く・portfolio-30）/ B1 は足さない（承認済みの多くが法律家の助言を経たという同じ向きの文が、B1 と against #1 に既に厚く在るので、足すと padding になる・portfolio-30 の判断）。

## 1.256 CC0 は献呈が効かない所で働く許諾を持つので「法的に隙が無い」、その代わりに長い（Moen 氏 2015）。ソフトウェアに CC0 が承認されなかった理由は特許の除外（Ingo 氏 2017）（2026-11-16）

Henrik Ingo 氏（`henrik.ingo at avoinelama.fi`・両リストで 203 通）を census の決める側の一覧に足すと、未読が 8 本出る（2026-11-16 の試算・一時の写しで回した）。Ingo 氏が OSI の理事だったかは一次の記録で確かめていない（portfolio-50 に確かめを頼む）ので、Taylor 氏（§1.255）と同じく候補の外として 8 本を通読した。2 本から 4 通を置いた（`rounds/2015-10-license-discuss-bsd3-{moen-cc0-airtight,woolley-pd-europe}-observed.txt`・`rounds/2017-11-license-discuss-cc0-request-{ingo,morrison-patent}-observed.txt`）。残る 6 本（2012 The alphabetical list・2015 PHP License v3.01 comments・2016 malicious derivatives・2019 CAL Beta 3・2020 On dual-licensing・2020 Extending copyleft）は、ACD に当たる新しい論点が無かった（CAL Beta 3 の Ingo 氏の評は CAL の審査の記録に既に厚い）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"OTOH, Creative Commons CC0 is highly permissive and legally airtight because it includes well-drafted permissive licence that applies in any jurisdiction where its primary PD dedication clauses fail to have the intended legal effect. (On the gripping hand, this causes its full text to be lengthy.)"* / 同じ通で *"Like most recent licences that aim to be more minimal than MIT/X11 License and Fair License (both OSI Certified, BTW), Unlicense suffers fatal drafting errors, such that it should _not_ be recommended to anyone."* | Rick Moen 氏 2015-10-02（"BSD 3-clause and copyright notices"） | **有利な面（B4・B3）。** 献呈と許諾を並べる形を、献呈の効かない法域への備えとして「隙が無い」と評し、その長さを同じ理由の代価とした。ACD の §3 と §4 の並びはこの形の系譜に在る。**ただし ACD は CC0 と同じではない**: CC0 の許諾は献呈が効かない所で働く（fallback）が、ACD の §4.4 は *"not as a fallback for it: it takes effect whether or not Section 3 does"* と書き、受領者に §3 が効くかの判断を求めない。Moen 氏の評は fallback の形に向いたもので、独立の許諾にそのまま当たるかは分からない（`QUESTIONS-FOR-COUNSEL.md` の問い 1 の「献呈と許諾は並んで立つか」がこの点） |
| *"Public domain dedication is impossible in Europe. There is some doubt as whether it is even possible in the USA. The nearest you would get is something like CC0, which attempts to disclaim as much IPR as it is possible to disclaim."* | David Woolley 氏 2015-10-02（同じ会話） | **不利な面（B8・法域）と、§4 の理由。** 献呈そのものが効かない法域が在る、という参加者の読み。ACD の §3.3（放棄だけを許す法域では放棄する）と §4（独立の許諾）は、この読みに備える条である。**逆側**: 「不可能」は参加者の断定で、法域ごとの検討ではない（`jurisdictions.md` が法域ごとの撤回権を持つ） |
| *"But for software I think there's no justification to not pick an OSI approved license. (Conversely, CC licenses are primarily designed for copyrighted works that are not software code.)"* / *"Many reviewers voiced an opinion that explicitly reserving the right to sue your users for patent infringment is clearly not compatible with the Open Source Definition."* / *"Technically then, it's never been decided whether CC0 is open source or not, but it is not OSI approved."* | Henrik Ingo 氏 2017-11-10（"I've been asked to license my open source project CC0"） | **両面。** CC0 が承認されなかった理由を特許の除外とする読みで、`rounds/2026-11-16-fsf-license-list-and-debian-dfsg-public-domain-snapshot.txt` の FSF の理由と同じ向き。ACD の §8 は CC0 が除外を置いた所に許諾を置くので、この理由は ACD に当たらない。**逆側**: 「ソフトウェアには承認済みのライセンスを」は、新しい道具を出すこと自体への逆風（B10）で、ソフトウェア以外の著作物を覆う ACD の §1.3 は、CC の側の道具と同じ需要に当たる（B15） |
| *"With CC0, I would suggest striking the patent provision or incorporating a patent grant from contributors in some manner."* | Christopher Sean Morrison 氏 2017-11-07（同じ会話） | **有利な面（§8）。** CC0 を使う人への処方として、特許の条を消すか特許の許諾を組み込め、と書いた。ACD の §8 は後者の形を取る。**逆側**: 同じ会話で Nigel Tzeng 氏は、自分のコードが使う特許を持たないなら特許の条は意味を持たない、と書き（要約・アーカイブの写しでは引用符の文字が化けているので逐語で引かない）、特許の差が実際に効く場面は狭いと読んだ |

**読み。** 2015〜2017 年のリストの参加者は、献呈と許諾を並べる形を「隙が無い」と評し、CC0 の欠点を特許の除外に絞っていた。ACD はどちらの点でも CC0 の欠点を避ける側に在る。

**逆側。** どれも参加者の発言で、委員会の決定ではない。Moen 氏が 2015 年に「致命的な起草の誤り」と評した Unlicense は、2020 年に承認された（`review-precedents.md`）—— 参加者の起草の評が承認の帰結を決めるわけではない。ACD の §4 は fallback でないので、Moen 氏の評の前提（献呈が効かない所で許諾が働く）とは形が違う。

**この節が establish しないこと。** 献呈と独立の許諾を並べる形が、fallback の形と同じく「隙が無い」と審査者に読まれるか。ACD の長さが CC0 と同じ理由で受け入れられるか（CC0 は 998 語、ACD の 1.4 草案は 5,546 語・`review-readings-2.md` §1.245）。

**反映**: B4（献呈と許諾を並べる形への有利な評と、ACD の §4.4 が fallback でないので評がそのまま当たらないこと・30 へ）/ B3（長さを「隙の無さ」の代価とする評・§1.255 の Taylor 氏の読みと同じ向き・30 へ）/ B8（献呈は欧州で不可能という参加者の読み・30 へ）/ 入口（CC0 が承認されなかった理由を特許の除外とする読みが、FSF の理由と並ぶ・50 へ）。

## 1.257 Mulan OWL の不承認の前に、Smith 氏（のちに理事）は「ソフトウェアにも内容にも使えるライセンスを退ける理由は無い」と書いていた（2023）。「より良いライセンスを作るのは弁護士資格を持つ人の仕事」（Perens 氏 2022）（2026-11-16）

census は、ドシエに多く引かれた会話を「候補の外」に置く。その会話の中に、決める側の通でドシエが 1 文も引いていない通（8 語連鎖が無い 40 語以上の通）が 218 会話・1,277 通ある（`census_decision_statements.py threads` の `unquoted-decider` の出力・2026-11-16）。2024〜2026 年の `license-review` の分は `review-readings.md` §1.211 の前後で読んだ。portfolio-2f は 2021〜2023 年の分（136 通・29 会話のうち、件名で写しから取り出せた 65 通）を、各通を切らずに論点の語で点数づけし、点の付いた通をすべて全文で読んだ。2 つの会話から 4 通を置いた（`rounds/2023-08-license-review-mulan-owl-{smith-content-patent,berkus-content-criteria}-observed.txt`・`rounds/2022-12-license-discuss-retro-disapprove-{perens-bar,smith-drafting}-observed.txt`）。ほかの通（3D Slicer の審査の手続き、AFL の旧版の扱い、承認済みの一覧の整理、OSD の定義の議論）は、ACD に当たる新しい論点が無かった。**引いていない通は 71 通残る**（件名の書き換えで写しから取り出せなかった通・機械層の道具で取り出せれば読む）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"FWIW, I agree that licenses that disclaim patent grants are not approvable. That's the lesson of CC."* / *"There's an underlying issue within that about whether a license that doesn't disclaim patent licenses but doesn't articulate any express patent license is approvable (at least, going forward) which probably also should be addressed"* | McCoy Smith 氏 2023-08-15（Mulan OWL の審査） | **有利な面（§8）。** 特許の否認が承認を妨げる、という線を Smith 氏が「CC の教訓」として述べた。ACD の §8 は明示の許諾を置くので、否認の型にも沈黙の型にも当たらない。沈黙の型の扱いが未決であること（`against-2.md` #246 の W3C の承認）とも合う |
| *"I'm not sure I agree that a "content" license is not approvable."* / *"I think if OSI is going to limit itself to only "software" licenses, it need to make that policy decision and make it clear, and perhaps articulate how one distinguishes between a "software" (or "primarily software") and a "non-software" (or "primarily non-software") license"* / *"absent that I see no reason why it shouldn't be approved if it could be used with software equally with content."* | McCoy Smith 氏 2023-08-15（同じ通） | **有利な面（B15）。** ソフトウェアにも内容にも等しく使えるライセンスは退ける理由が無い、という Smith 氏の読みで、ACD の §1.3 の列挙（ソフトウェアとそれ以外）に直接当たる。Fair License と CERN OHL を、ソフトウェアに限らない承認済みの例として挙げた。**逆側（重い）**: この通の 1 か月後、理事会は Mulan OWL を *"as open culture licenses, are not appropriate for OSI approval"* として不承認にした（`against-2.md` #237）。Smith 氏の読みは採られなかった |
| *"I'm not ready to take on OSI developing a process and criteria for approving content licenses this year.  I do think it's something we should consider for the future ... in fact, should have done years ago ... but it's also going to be a ginormous effort for someone."* | Josh Berkus 氏 2023-08-11（同じ会話・委員長 Chestek 氏の「これらは承認の対象として適切でない、で合意があるか」への答え） | **不利な面（B15）。** 内容のライセンスを承認する基準は無く、作るのは大きな作業だ、という Berkus 氏の答え。ACD がソフトウェア以外を覆う部分は、基準の無い所で審査される |
| *"1. There has to be a better license first. Which might unfortunately mean making it sometimes, and tolerating yet another license. Making it is for someone admitted to the Bar to do."* | Bruce Perens 氏 2022-12-14（"Retroactively disapproving licenses"・SIL Open Font License を例に） | **両面（B10・B1）。** 新しいライセンスを足すことを「より良いものが要るなら許す」と認めつつ、作り手を弁護士資格を持つ人に限った。ACD は前者に当たりうるが、後者には当たらない（B1）。`review-readings-2.md` §1.255 の Taylor 氏 2004「承認済みのほとんどは法的な助言を受けて書かれた」と同じ向き |
| *"I also think that there are other factors, beyond OSI conformance, that can, and should, go into license approval (for example, a license is so poorly or ambiguously drafted that it can create problems for users, or -- for example -- it explicitly omits certain rights -- like patent -- that can result in them being non-open)."* | McCoy Smith 氏 2022-12-14（同じ会話） | **両面（B3・§8）。** 起草のあいまいさを OSD の外の承認の要素とする Smith 氏の読み。1.4 草案の明確さの試作（`ACD-1.4-CLARITY-TRIAL.md` から THIRD まで）はこの要素に答える側に在り、§8 は「特許を明示に外す」型に当たらない |

**読み。** 2022〜2023 年の決める側の人の通は、ACD の 2 つの特徴（明示の特許の許諾、ソフトウェアと内容を共に覆うこと）のどちらにも、それを支える文を持っていた。ただし後者は、同じ審査で理事会が採らなかった読みである。

**逆側。** Smith 氏の当時の役（委員か）は確かめていない（ドシエは「後に Licensing Committee」「2026-02 頃〜・理事」と書く）。Smith 氏の B15 の読みは不承認の決定に負けている。Berkus 氏の通は、ソフトウェア以外を覆うことの審査に基準が無いことを示す。Perens 氏の通は、新しいライセンスの作り手に弁護士資格を求める。

**この節が establish しないこと。** 理事会が「ソフトウェアにも等しく使える」ライセンスを Mulan OWL と別に扱うか。決定の文は *"as open culture licenses"* で、ソフトウェアに使えるかには触れていない。

**反映**: B15（Smith 氏 2023 の「ソフトウェアにも内容にも等しく使えるなら退ける理由が無い」を採られなかった読みとして置き、1 か月後の理事会の不承認（#237）と Berkus 氏の「基準は未整備」を同じ段の逆側にする・portfolio-30）/ B1 は足さない（Perens 氏 2022「作るのは弁護士資格を持つ人の仕事」と同じ向きの文が B1 に既に厚い・portfolio-30 の判断）/ 入口（特許の否認は承認できないという「CC の教訓」の Smith 氏の文を、ACD の §8 の説明に使えるか・50 へ）。

## 1.258 「法の許す限り」の句は、国によっては縮められずに句ごと無視される（Chestek 氏 2023）—— §14 の形に当たる。「法律家のボランティアの助けを得て出し直せ」（Perens 氏 2019）（2026-11-16）

`review-readings-2.md` §1.257 の続き。portfolio-9b が unquoted-decider の各通に写しの file 名と Message-ID を足した（PR 3419）ので、件名に依らず通を引けるようになった。portfolio-2f の分担（2017〜2020 年の 486 通と、2021〜2023 年の §1.257 で引けなかった 71 通・計 568 通・72 会話）を同じ手順で点数づけした（9b は 1999〜2016 年）。CAL の 3 本の審査（186 通）はドシエが最も厚く読んだ審査なので後に回し、残りから点の付いた通を全文で読んだ。3 通を置いた（`rounds/2023-02-license-discuss-unless-required-chestek-unwaivable-observed.txt`・`rounds/2017-02-license-discuss-arl-osl-rosen-non-lawyer-funnel-observed.txt`・`rounds/2019-03-license-review-whonix-perens-lawyer-volunteer-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"Your premise that all liabilities can be waived is not correct."* / *"What can be waived varies from jurisdiction to jurisdiction, but I believe it's fairly universal that one cannot waive liability for intentional wrongs."* / *"My understanding is that the clause isn't effective in the same way in some countries and would instead be ignored altogether, leading to liability for everything, not just the unwaivable claims."* / *"I also understand that in some countries there are different standards of liability for gifts versus an exchange that benefits both parties."* | Pamela Chestek 氏 2023-02-18（"Reconsidering the "unless required by applicable law" clause"・個人として） | **不利な面（§14・B8）。** ACD の §14.1 は *"TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW"* で、§14.2 は *"Where applicable law does not permit the exclusion or limitation of a liability, that liability is limited to the greatest extent that law permits"* —— Chestek 氏が「国によっては効かない」とした型そのものである。句が無視される国では §14 の全体が落ち、§14.2 の縮減も働かない読みが立つ。`jurisdictions.md` のドイツの節は、縮減（*geltungserhaltende Reduktion*）が使えない可能性を §15.4 と §3 について検討したが、§14 には当てていなかった。**有利な面**: 同じ通の最後の文は、無償の贈与と交換とで責任の基準が違う国があると言う。ACD は対価も条件も持たない一方的な付与なので、贈与の側の基準に当たりうる（どの国でどうなるかは確かめていない） |
| *"I don't immediately see any non-compliance with the OSD. However, there is another good reason why I feel the license should be rejected."* / *"Foregoing the legal review was excusable long ago, indeed the OSD had no legal review because no lawyer would help us. Today we have folks like Kyle and Van on this list who have given of their time and are properly admitted to the Bar. I thus suggest that you actually get a lawyer volunteer to help you, and resubmit after that."* | Bruce Perens 氏 2019-03-15（GPL-3+-with-whonix-additional-terms の審査） | **B1 の潰し方の材料。** 法的レビューの無い提出に対し、退けるだけでなく「リストの法律家のボランティアの助けを得て出し直せ」と道を示した。オーナーの行為 3（法律家に読んでもらうよう頼む）の、決める側の人が名指した経路の 1 つである。同じ日の "The per se license constructor"（`reviewer-positions.md`）は同じ考えの一般形で、ドシエに既に在る。**逆側**: 名の挙がった 2 人の法律家が今も手伝うかは分からない。Perens 氏は同じ文で「OSD に不適合は見えない」と言いながら退けるべきとした —— OSD 適合は ACD の十分条件にならない（`against.md` #130） |
| *"Their behavior in funneling their license to this public list via a non-lawyer is insulting to those of us on this list who are lawyers and who well understand the law of copyright and open source. They are also insulting the non-lawyers on this list who know more about open source licenses than most lawyers in your government agency apparently do. Please ask them to talk to us as professionals."* | Lawrence Rosen 氏 2017-02-27（ARL OSL・米陸軍研究所の法律家が非法律家の職員を通して出したことについて） | **参考（B14）。** 起草した者が表に出ず、別の人を通してリストと話す形への反発。ACD は起草の大半が AI であることを開示し、オーナーが自分の言葉で話す（B14 のゲート 0）。ARL は「背後に法律家がいるのに出てこない」形で、ACD は「背後に法律家がいない」形なので、同じではない。ただし「誰が書き、誰が答えられるのか」を審査者が問う、という点は共通する |

**T82 の後（2026-11-16 追記）**: portfolio-1c は T82 で §14.1 の冒頭に *"EXCEPT FOR ANY LIABILITY FOR WILFUL MISCONDUCT, GROSS NEGLIGENCE, DEATH, OR PERSONAL INJURY THAT APPLICABLE LAW DOES NOT PERMIT TO BE EXCLUDED, WHICH NOTHING IN SECTION 14 LIMITS"* を足した。上の表の §14 の記述は T82 の前の文である。T82 は、Chestek 氏が同じ通で述べた「法域ごとに、なお負う責任を名指す」形（*"jurisdiction-specific licenses that specifically name what the licensor will still be liable for"*）に近づく。ただし *"TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW"* と §14.2 の縮減は残っており、句を無視する法域で §14 の残りが働くかは、なお問い 9 の問いである。

**読み。** 2017〜2023 年のドシエが引いていない決める側の通は、§14 の型に向けた具体的な不利な読み（Chestek 氏 2023）と、B1 の具体的な潰し方（Perens 氏 2019）を持っていた。

**逆側。** Chestek 氏は「個人として」書き、「理解している」の形で述べた。どの国で句が無視されるかは名指していない。

**この節が establish しないこと。** §14 がどの国で落ちるか。ACD が贈与の基準に当たるか。

**反映**: B8 の着地は `ACD-1.0.jurisdictions.md` §3（ドイツ）の「§14 にも縮減の不可が当たりうる」の段（portfolio-30）/ 入口（`QUESTIONS-FOR-COUNSEL.md` 問い 9 の §14 の段 —— 句を無視する法域で §14 が残るか、贈与の責任の基準（BGB 521 条）に当たるか・portfolio-30。portfolio-50 の同じ中身の (c) は重複として落とした）/ B1 の潰し方は `OSI-APPROVAL-PLAN.md` のオーナーの行為 3 に Perens 氏 2019 の勧め（portfolio-50）/ 1c（§14.2 の語を見直すかの判断を送った）。

## 1.259 「OSI は『分からない』と言い続け、承認の印なしに使わせて様子を見る選択肢が要る」（Kuhn 氏 2020・CAL の審査）—— 2025 年に理事会が「重複かつ未使用」に限って似た形を採った（2026-11-16）

`review-readings-2.md` §1.258 で後に回した CAL の 3 つの審査の、ドシエが引いていない決める側の通（188 通・Perens 氏 76・Chestek 氏 46・Berkus 氏 19 ほか）を、同じ手順で点数づけし、点の付いた通を全文で読んだ。3 通はどれも `rounds/2019-04-license-review-cal-approval-observed-*.txt` に既に逐語で在り（20・35・49 of 61）、分析の文書が引いていなかった。新しい rounds は置かない。ほかの通は API の著作権への copyleft、公衆への実演の語、商標の扱いなど CAL に固有の論点で、ACD に当たる新しい点は無かった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"As I said in 2018 during SS Public License evaluation, the process works great for "minor tweak", highly permissive FOSS licenses that have appeared in the wild and need urgent attention."* / *"I think there has to be an option (in the general case, not only for this particular license) for the OSI to say "we don't know" indefinitely and encourage the drafting authority to begin using the new license without the OSI-approved label and see what happens."* | Bradley M. Kuhn 氏 2020-01-04（CAL Beta 4・`rounds/2019-04-license-review-cal-approval-observed-49of61.txt`） | **両面（B2・B10）。** 審査の手順は「世に出て使われている、小さな手直しの許容的なライセンス」に向き、新しく書かれた広い射程のライセンスには向かない、という読み。ACD は許容的だが、新しく書かれ、世で使われていない（B2）。同時に、否決でも承認でもない「分からない・まず使ってみよ」という帰結を提案した。License Committee は 2025-07-18 に理事会へ *"should the LC reject a license proposal that is valid but is not in use anywhere?"* と問い、理事会は *"a license should be rejected only if it violates the OSD. But a license could stay in a status where it is not approved if it is duplicative and not used by a project."* と答えた（`board-decisions.md` §2・`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B2 の「否決ではない帰結」の段）。Kuhn 氏の提案は一般の選択肢としては採られていないが、「重複かつ未使用」の場合に限った第 3 の状態として、似た形が 5 年後の理事会の答えになった（portfolio-30 の指摘で直した）。**逆側**: その第 3 の状態は「重複かつ」が条件で、ACD が重複に当たらないと示せれば（B10）当たらず、示せなければ「未使用」（B2）と合わせて当たる。Kuhn 氏は当時の理事でも委員でもない（決める側の一覧には入っている） |
| *"The FSF authorized a third-party fork for experimentation when the idea was new in 2002 -- precisely because the FSF (as a license steward dedicated to software freedom) was cautious about expanding copyleft requirements in novel directions."* | Bradley M. Kuhn 氏 2019-08-28（CAL Beta 2・同 35 of 61） | **B2 の材料。** 新しい考えのライセンスが、承認や採用の前に何年も実地で試された先例（Affero GPL）。ACD の新しい部分（モデルと出力への伸び・§6・§8.4）は試されていない。**逆側**: これは copyleft の義務を広げる場合の話で、義務を課さない ACD に「慎重さ」の理由がそのまま当たるかは分からない |
| *"The license is being held to a standard for universal applicability of terms of art that I am not aware has been applied to Open Source licenses before."* | Bruce Perens 氏 2019-06-28（CAL・同 20 of 61・CAL の "public performance" が米国法の語だという指摘について） | **有利な面（B8）。** 1 つの法域の語に頼ることが審査で問われた。ACD の §4.2 は *"publicly display, publicly perform, communicate to the public"* と米国の語とベルヌ条約・欧州の語を並べ、§1.2 で Moral Rights を、§7 で sui generis database rights を自分で定義する。Perens 氏は同じ通で、この基準は以前は当てられていなかった、とも書いた —— 審査の基準が上がっているという読みで、ACD の長さ（B3）の一部はこの基準に答えるためのものである |

**読み。** CAL の審査の、ドシエが引いていない決める側の通は、B2 について「否決ではない帰結」の早い形（Kuhn 氏 2020）を持っていた。

**逆側。** 2025 年の理事会の答えは「重複かつ未使用」に限っており、Kuhn 氏の一般の提案（新しく書かれた広い射程のライセンスを、承認も否決もせずに使わせる）とは範囲が違う。

**この節が establish しないこと。** 2025 年の第 3 の状態が、重複に当たらないが未使用のライセンスにも使われるか。

**反映**: B2（「否決ではない帰結」の段に、Kuhn 氏 2020 の文を、2025 年の理事会の答えの 5 年前の形として 1 文・portfolio-30）/ 1c（§4.2 が複数の法域の語を並べることが、CAL の審査で問われた「1 つの法域の語」の問いに答える形であること —— 逐条の §4.2 の行の材料・portfolio-30 の振り分け）。

## 1.260 撤回不能を明記することは「少し冗長」—— 撤回の実例は無い（Berkus 氏 2025・MIT-I）。AI には一般化に使える実践がまだ無い（Maffulli 氏 2024）（2026-11-16）

census の unquoted-decider（候補の外の会話の、ドシエが 1 文も引いていない決める側の通）の 2024〜2026 年分 170 通（`license-review` 124・`license-discuss` 46）を、2026-11-16 の main で回し直して Message-ID で引き、論点の語で点数づけして、ACD の論点に近い会話（AI への審査の手順の適応・MIT-I・新しいライセンスの事前の相談 など）を全文で読んだ。`review-readings.md` §1.211 の前後で読んだ 2024〜2026 年の `license-review` の 74 通の後に、ドシエが増えて引用が変わった分と `license-discuss` の分が加わっている。3 通を置いた（`rounds/2025-08-license-review-mit-i-berkus-irrevocable-redundant-observed.txt`・`rounds/2024-09-license-review-ai-process-{maffulli-no-practice,berkus-list-separately}-observed.txt`）。Perens 氏 2024-10 の「ある種の関門が要る」は `review-venue.md` に、AI への審査の適応のスレッドの委員長の答えは `board-decisions.md` に既に在る。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"It's one thing to say that the license is not revokable on already distributed copies of the software.  I think it's a bit redundant for the reasons Pam gives; even if the license is theoretically revokable, unless the revokation is automatic for reasons already documented in the license itself you're going to have a hard time actually carrying it out.  As far as I know, nobody has ever tried to do this; even with the various relicensings of database software, nobody has tried to claw back the old versions."* | Josh Berkus 氏 2025-08-15（MIT-I の審査） | **逆側（§2.2・§4.1・§10.4・B10）。** `review-precedents.md` §1.47 は、委員長が MIT に「perpetual と irrevocable の語を入れればよい」と述べたことを、ACD の §4.1 が既に満たす有利な面として読んだ。同じ審査で Berkus 氏は、撤回不能の明記そのものを「少し冗長」とし、撤回の実例は無いと書いた。ACD の本文は "irrevocable" の語を §2.2（*"This Dedication is irrevocable"*）・§3.1・§4.1・§8.1 の 4 か所に持ち、§10.4 が許しが終了しないことを別に述べる —— 新しさ（B10）や長さ（B3）の説明に撤回不能を挙げると、「実際には問題になっていない点に語を費やしている」と読まれうる。**有利な面**: Berkus 氏は撤回不能を誤りとは言っておらず、`jurisdictions.md` の法定の撤回権（UrhG 42 条ほか）は、ライセンスの撤回とは別の、作者の側の撤回の道で、実例が無いのはライセンスの撤回についてである |
| *"I see the temptation to jump to this conclusion but I recommend everybody to remember that the OSD looks easy to interpret today only because it's 26 years old. Also, when it came out there were hundreds of software packages already using its principles."* / *"For AI we don't have any of that, there isn't a body of widely-agreed-upon "free as in freedom" work we can look at, there is no practice of openness, therefore there are no examples we can use to generalize"* | Stefano Maffulli 氏（事務局長）2024-09-12（"Adapting the license-review process to AI"） | **両面（B10・B15・B2）。** AI の領域には一般化に使える実践が無い、という事務局長の読み。ACD のモデルと出力への伸び（§6・§8.4）は、審査者が比べる先例の無い所に在る —— 新しさの根拠にもなり、比べる物差しが無いという不利にもなる。OSD 自体が「既に何百もの実践があった」ことで解釈しやすくなった、という読みは、B2（実使用が 1 件）の重さを裏から支える |
| *"Finally, I think we'll want to list approved documents which are not software licenses separately on the website from the software licenses."* | Josh Berkus 氏 2024-09-09（同じ会話） | **参考（B15）。** ソフトウェアのライセンスでない承認済みの文書を別に並べる、という案。ACD のようにソフトウェアとそれ以外を共に覆う文書が、どちらの一覧に入るのかは、この案の下で問われうる |

**読み。** 2024〜2026 年の、ドシエが引いていない決める側の通は、ACD の撤回不能の強調に向けた逆側（Berkus 氏 2025）を持っていた。§1.47 の有利な読みは、同じ審査の別の通と対で置く必要がある。

**逆側。** Berkus 氏の通は、MIT-I の「公の置き場から外してはならない」という別の義務への批判が主で、撤回不能の明記を退けてはいない。Maffulli 氏の通は OSAID（AI の定義）の文脈で、ライセンスの審査の基準を述べたものではない。

**この節が establish しないこと。** 審査者が ACD の撤回不能の 4 か所の語と §10.4 を冗長と読むかどうか。

**反映**: B10 の着地は `review-precedents.md` §1.47 の有利な読みの後の逆側の段（Berkus 氏 2025・結論が変わらない理由として批判の主は MIT-I の別の義務・portfolio-30）/ B15（Maffulli 氏 2024 と Berkus 氏 2024 の非ソフトウェアの一覧の案・portfolio-30）/ B3（撤回不能の繰り返しの段。4 か所は別々の権利 —— 献呈 §2.2・放棄 §3.1・著作権の許諾 §4.1・特許の許諾 §8.1 —— に付くので、まとめると読みが割れうる、を逆側に・portfolio-30）/ 1c（語数を減らす候補になるかの判断を送った）。

## 1.261 受諾が無ければ bare license（Rosen 氏 2005）、大陸法に bare license の概念は要らない（Engelfriet 氏 2007）、明示に外したライセンスは禁反言に頼れない（Piana 氏 2012）—— §2.3・§2.5 の撤回不能の足場を、リストの法律家の文に当てる（2026-11-16）

オーナーの依頼（2026-11-16「ACD-1.4-DRAFT.txt の法的解釈の不確実性を 5 人で減らし続けて」）の portfolio-2f の受け持ち（リストの法律家の発言を条ごとに当てる・portfolio-30 の重ね）。直前に置いた米国の 2 つの法源 —— 撤回不能を対価に結びつけた Asset Marketing v. Gagnon（2008・`rounds/2026-11-16-us-asset-marketing-v-gagnon-consideration-snapshot.txt`）と、約束的禁反言のリステイトメント 90 条 1 項（`rounds/2026-11-16-us-restatement-90-promissory-estoppel-snapshot.txt`）—— の間を、リストの法律家の文で埋める。アーカイブの写しで、法律家の差出人（Rosen・Fontana・Chestek・Welch・Smith・Piana・Radcliffe・Kuhn・Engelfriet ほか）の通を "promissory estoppel"・"bare license"・"revocable"・"gratuitous license"・"nudum pactum" で当てた 14 通のうち、ドシエに 8 語連鎖の無い 11 通を読み、4 通を置いた（`rounds/2012-03-license-review-mxm-cc0-piana-agnostic-estoppel-observed.txt`・`rounds/2005-08-license-discuss-bare-licenses-rosen-assent-observed.txt`・`rounds/2007-08-license-discuss-copyleft-blow-engelfriet-civil-law-observed.txt`・`rounds/2020-01-license-review-mulan-psl-smith-party-bare-license-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The OSL and AFL are \*worded\* to be unilateral contracts rather than bilateral contracts. But they are not contracts until the formalities of contract formation (particularl assent) are completed. Until then they are bare licenses. I have argued before that contracts have additional enforcement options than bare licenses."* | Lawrence Rosen 氏 2005-08-25（"Contracts vs. bare licenses"） | **§2.3 の帰結（米国）。** ACD の §2.3 は *"This Dedication takes effect without any act of acceptance by You"* —— 受諾の手続きを置かないので、Rosen 氏の線では米国で ACD は契約ではなく bare license である。Gagnon は撤回不能を対価（契約）に結びつけたので、ACD の撤回不能は契約の道からは立たず、§2.5 の禁反言（リステイトメント 90 条）が足場になる。**これで米国の撤回不能の問いは 1 本の線に狭まる**: bare license（§2.3・Rosen 氏）→ 対価の道は無い（Gagnon）→ §2.5 がリステイトメント 90 条の要件を満たすか（実際の信頼と不正義は事実の問い） |
| *"As a civil lawyer, the main problem for me is that even the simplest interaction between the parties creates a contract."* / *"I don't think I \*need\* the concept of a bare license in civil law. If it's not a contract, then usually it's something like an easement."* | Arnoud Engelfriet 氏 2007-08-27（オランダの特許弁理士・"(OT) - Major Blow to Copyleft Theory"） | **大陸法の側（独・仏・日は portfolio-30）。** 大陸法では、受諾の手続きが無くても行為から契約が成り立ちうるので、ACD の撤回不能は契約として支えられる読みが立つ。同時に、契約なら贈与の撤回（独 BGB 530 条・仏 民法典 953 条 —— `ACD-1.4-THIRD-CLARITY-TRIAL.md` §18.3 の §8.2 の行）が当たりうる。米国と大陸法で、撤回不能の足場が違う（禁反言 / 契約） |
| *"At least the hyperpermissive licenses don't say anything, so you can rely on promissory estoppel, /contra se venire/ or all other legal theories. But the agnostic ones -- and I put both MXM and CC0 in that category -- are in this more dangerous, as you cannot construe against what it's clearly spelt out."* | Carlo Piana 氏 2012-03-05（"MXM compared to CC0"・特許について） | **有利な面（§8・§2.5）。** 沈黙のライセンスは禁反言に頼れるが、特許を明示に外した MXM・CC0 は「明記されたことに反して」解釈できない。ACD は特許を明示に許諾し（§8.1）、禁反言を明示に置く（§2.5）ので、Piana 氏の言う「不可知の」型に当たらず、禁反言を明記された側に置いている。**逆側**: Piana 氏の文は特許の沈黙と除外についてで、撤回不能を禁反言で支えることの効き目を述べてはいない |
| （逐語は引かない —— 写しで引用符が "?" に化けている）bare license として書かれた文書で "party" の語を使うと、双方に拘束力のある義務を作ろうとしていると読まれうる、契約として読ませたいなら受領者の義務を明らかにせよ | McCoy Smith 氏 2020-01-01（Mulan PSL V1 の審査・同じ文が後の Chestek 氏の通に印なしで引かれている） | **有利な面（語の選び方）。** ACD の 1.4 草案は "party" の語を本文で使わない（Dedicator と You だけ）。bare license の読みと語が食い違うことを避けている |

**読み。** リストの法律家の文を当てると、米国の撤回不能の問い（`QUESTIONS-FOR-COUNSEL.md` 問い 1 の一部）は、「§2.3 で ACD は bare license → 対価の道は無い → §2.5 がリステイトメント 90 条を満たすか」の 1 本の線に狭まる。大陸法では足場が契約に移り、代わりに贈与の撤回が問いになる。

**逆側。** Rosen 氏の「bare license」は米国の学説の 1 つで、オープンソースのライセンスを契約と読む判決（Jacobsen v. Katzer の後の読みなど）もある。契約と読まれれば対価の問い（条件の無い ACD に対価は在るか）が戻る。Engelfriet 氏は「usually」と書き、オランダ法を念頭に置く。どの文も ACD を扱っていない。

**この節が establish しないこと。** §2.5 の禁反言が米国の裁判所で撤回を実際に止めるか。大陸法で ACD が贈与と読まれるか。

**反映**: 入口（法律家への問い 1 に「米国では §2.3 → bare license → §2.5 とリステイトメント 90 条」の線を、出典と共に・50 へ）/ 1c（THIRD §18.1 の §2.2・§2.3・§2.5 の行に、この線と 4 つの法源を）/ B4（撤回不能の足場が米国と大陸法で違うこと・30 へ）。

## 1.262 「起草者は準拠法の条項を入れないでほしい」（Piana 氏 2022）—— §15.3 が準拠法も法廷地も名指さないことへの、決める側の人とライセンスの steward の理由。逆側は「省けば受け手の法域へ行く、というのは魔法か」（Rosen 氏 2022）（2026-11-18）

オーナーの依頼（2026-11-16「法的解釈の不確実性を 5 人で減らし続けて」）の portfolio-2f の受け持ち（リストの法律家の発言を条ごとに当てる）。`QUESTIONS-FOR-COUNSEL.md` 問い 7（§15.3）は、理事会の 1 文（*"it does not believe that choice of law provisions are necessary or advisable in open source licenses"*・`against.md` #254）だけを省くことの支えに挙げていた。同じ論点を論じた 2022-12 の `license-review` の会話（Open Logistics License の審査から分かれた・件名 "in opposition of 'choice of law' provisions in FOSS licenses"）は、決める側の人の通 12 通がドシエのどの分析にも引かれていなかった（逐語は `rounds/2022-04-license-review-open-logistics-license-observed-10of15.txt`〜`12of15` に既に在る）。

| 発言 | 誰が | §15.3 への当たり方 |
| :-- | :-- | :-- |
| *"Another notable license dropping it for good is Creative Commons (v3 -> v4)"* / *"I strongly invite drafters NOT to include choice-of-law provisions in their licenses."* | Carlo Piana 氏 2022-12-14（`rounds/…-10of15.txt`） | **有利な面。** 決める側の人が、準拠法の条項を入れないよう起草者に求めた。CC も 4.0 で外した。§15.3 の省き方と同じ向き |
| 準拠法の条項が嫌われる実務上の理由として、多くの法律家が嫌う（EPL-1.0 は準拠法の条項のために米国寄りと見られ、避けられた）と、多くの法律家が読まない、の 2 つを挙げた（`rounds/…-10of15.txt` の 204〜205 行） | Mike Milinkovich 氏 2022-12-13（Eclipse の EPL の steward・当時 OSI の宛名） | **有利な面。** 準拠法を選ぶことが利用の妨げになった steward の経験。ACD の利用者が法域の偏りを感じない形 |
| 準拠法の条項は、選ばれた法域に不慣れな参加者に偏りを生み、FOSS のライセンスは同じ文で世界中に働き、全ての法域を等しく扱うべきだ、という理由の列挙 | Bradley M. Kuhn 氏 2022-12-12（アーカイブの写し・`license-review` 2022-12） | **有利な面。** §15.3 が法域を選ばない理由と同じ |
| *"Does anyone on here believe that omitting a "choice of law" provision entirely from a software license will necessarily result in the license being sent to the licensee's jurisdiction for court enforcement?"* / *"How does that default work? Is it magic?"*（写しでは引用符が "?" に化けている） | Lawrence Rosen 氏 2022-12-17（`rounds/…-12of15.txt`・OSL の起草者で、OSL は許諾者の所在地の法を名指す） | **逆側。** 省けば受け手の法域で裁かれる、とは限らない。`rounds/2026-11-16-eu-tdm-and-conflict-of-laws-snapshot.txt` のローマ I 第 4 条 2 項（選択が無ければ特徴的な給付をする当事者の常居所地）は、契約の側では許諾者（Dedicator）の法を指す —— Rosen 氏の問いの向きを EU の条が裏づける。侵害の側はローマ II 第 8 条で保護が求められる国の法で、合意では動かない |

**読み。** §15.3 の省き方は、理事会（#254）に加え、決める側の人（Piana 氏）と steward（Milinkovich 氏）と常連（Kuhn 氏）の理由で支えられる。残る費用（受け手が外国で訴えられたとき、指す条項が無い・契約の側は Dedicator の法へ向く）は、Rosen 氏の問いとローマ I が同じ所を指しており、問い 7 の 1.4 草案の段（T92 の後）が既に問うている。

**逆側。** 準拠法の条項を持つ承認済みのライセンスは多い（OSL 3.0・MPL 2.0 の法廷地・CAL 7.2 —— 同じ会話の Chestek 氏・Fontana 氏の列挙）。省くことは承認の要件ではなく、好みの線である。

**この節が establish しないこと。** 外国で訴えられた受け手にとって、名指しが無いことが不利に働くか。

**反映**: 入口（問い 7 の "Why we doubt it" の理事会の 1 文に、Piana 氏・Milinkovich 氏の理由と Rosen 氏の逆側を並べるか・50 へ）/ B8（準拠法を選ばないことの支えと費用・30 へ）。

## 1.263 「正本は 1 つにすべきだ」（Piana 氏 2019）—— Mulan PSL の提出者は v2 で「食い違えば中国語版が優先する」を足し、承認された。§15.4（英語を正本とする）と同じ形（2026-11-18）

オーナーの依頼（2026-11-16「法的解釈の不確実性を 5 人で減らし続けて」）の portfolio-2f の受け持ち（リストの法律家の発言を条ごとに当てる）。1.4 草案の §15.4 は *"English is the authoritative language of this Dedication. A translation is for convenience only; in the event of conflict, this English text prevails."* —— この条を論じた審査の文は、ドシエの分析に無かった（`review-readings.md` の Berkus 氏 2016 の ZenTao の 1 行「正本が中国語なら中国語の読み手に見てもらえるか」だけ）。Mulan PSL の審査（`license-review` 2019-12〜2020）から 3 通を置いた（`rounds/2019-12-license-review-mulan-psl-{piana-one-authoritative-version,piana-translation-glitch,v2-chinese-prevails}-observed.txt`）。

| 発言 | 誰が | §15.4 への当たり方 |
| :-- | :-- | :-- |
| *"Frankly, I see little merit in creating confusion by using two languages on equal footing."* と、GPL の族が英語だけを正本と決めたことに同意し、どちらが正本かがライセンスの中に書かれていなければ地域の裁判所に委ねられる、と書いた | Carlo Piana 氏 2019-12-03 | **有利な面。** 正本を 1 つに決める §15.4 の形を、決める側の人が求めた |
| *"**One** version should be authoritative, IMHO. Which one, that's up to the author of the license to decide."* と、訳の不具合で 2 つの版が大きく違い、第三者がそれを組み合わせると、同じ名で法的な帰結の違うライセンスが並ぶ、という例 | Carlo Piana 氏 2019-12-06 | **有利な面。** どの言語を正本にするかは著者の選択とした —— ACD が英語を選ぶことは、この線で問われない |
| v1 の中国語版と英語版の食い違いが主な懸念だったので、v2 で「食い違いがあれば中国語版が優先する」という文を条に足した、Piana・Berkus・Phipps・Chestek の諸氏の示唆に感謝する | Zhou Minghui 氏（提出者）2019-12-30 | **先例。** 正本を 1 つにする文は、審査の指摘に応えて提出の版に足され、Mulan PSL は 2020 年に承認された（`board-decisions.md` の理由書の段）。§15.4 の形は、審査が求めて承認に至った形と同じ |

**読み。** §15.4 が英語を正本とし訳を便宜とする形は、決める側の人が求め、提出者がそれに応えて承認に至った先例と同じ形で、この条の解釈の不確実性（どの版が効くか）は、条の文が自分で決めている。

**逆側。** 正本が英語であることは、英語以外の法域の裁判所が英語の文を読むことを前提にする。訳が便宜にすぎないと言っても、地域の裁判所が自国語の訳を参照することまで止められるとは限らない（Piana 氏も「地域の裁判所に委ねられる」のは正本を書かない場合として述べた）。

**この節が establish しないこと。** 英語を正本とする条が、各法域の裁判所で訳より優先して扱われるか。

**反映**: 1c（`ACD-1.4-THIRD-CLARITY-TRIAL.md` §18.5 の §15.4 の行の支え —— 審査が正本を 1 つにすることを求め、Mulan PSL v2 が足して承認された・9b の帯）/ 入口（§15.4 の説明に、審査が求めた形であることを添えるか・50 へ）。

## 1.264 §15.2（改めと切り離し）は承認済みの CAL 7.6 と同じ型で、切り離しを法域に限る点で狭い。「オープンソースのライセンスへの切り離しの攻撃は起きていない」（Perens 氏 2018）、「切り離しで利用者に写しの破棄を求めるのは苛酷」（Rosen 氏 2002）（2026-11-18）

オーナーの依頼（2026-11-16「法的解釈の不確実性を 5 人で減らし続けて」）の portfolio-2f の受け持ち（リストの法律家の発言を条ごとに当てる）。1.4 草案の §15.2 は *"If a provision of this Dedication is held invalid or unenforceable in a jurisdiction, it is to be reformed to the minimum extent necessary to make it valid and enforceable there while preserving its purpose. If it cannot be reformed, it is severed as to that jurisdiction only, and the remainder continues in full force everywhere."*。アーカイブの写しで法律家と決める側の人の通を "severab" で当て、ドシエに引かれていない 3 通を置いた（`rounds/2018-06-license-review-nosa-perens-no-severability-attack-observed.txt`・`rounds/2002-08-license-discuss-rpsl-rosen-severability-harsh-observed.txt`・`rounds/2020-02-license-review-cal-chestek-text-severability-7-6-observed.txt`）。

| 発言 | 誰が | §15.2 への当たり方 |
| :-- | :-- | :-- |
| *"If any provision of this License is held to be unenforceable, such provision shall be reformed only to the extent necessary to make it enforceable. Any invalid or unenforceable portion will be interpreted to the effect and intent of the original portion. If such a construction is not possible, the invalid or unenforceable portion will be severed from this License but the rest of this License will remain in full force"* | Cryptographic Autonomy License の 7.6（Pamela Chestek 氏 2020-02-09 の通が引いた CAL の文・CAL 1.0 は 2020 年に承認） | **先例（同じ型・2 点の違い）。** 必要な限りで改め、できなければ切り離して残りを保つ —— §15.2 の 2 段（改め → 切り離し）と同じ型。違いは 2 つ: (1) CAL は *"severed from this License"* と法域を限らずに切り離すが、1.4 草案の §15.2（1.3 までの §15.4）は *"severed as to that jurisdiction only, and the remainder continues in full force everywhere"* とその法域に限る —— ACD の方が狭く、他の法域では条項が生きる。(2) 改めの基準は、CAL が *"interpreted to the effect and intent of the original portion"*、§15.2 が *"while preserving its purpose"* で、近いが語が違う（portfolio-30 の反例で直した）。**限り**: 引かれた文が承認された版の 7.6 と一字一句同じかは確かめていない |
| *"And yet we haven't had a severability attack on an Open Source license that I am aware of."* | Bruce Perens 氏 2018-06-20（NOSA 2.0 の審査・公有の部分の問題は全てのオープンソースのプログラムに及ぶ、という文の後） | **参考。** 2018 年までに、切り離しを争点にしたオープンソースのライセンスへの攻撃は知られていない、という決める側の人の観察 |
| *"The severability provision in 13.5(b) is a little harsh. If a court rules against you, I could understand your halting any further distribution or licensing of the Original Code. But to require your users to discontinue any use and destroy all copies is quite draconian."* | Lawrence Rosen 氏 2002-08-05（RealNetworks の RPSL の事前の議論） | **有利な対比。** 切り離しの条が利用者に使用の停止や写しの破棄を求める形は苛酷とされた。§15.2 は無効な条項をその法域についてだけ切り離し、残りを全ての所で保つので、利用者に何も求めない |

**読み。** §15.2 は承認済みの CAL 7.6 と同じ型で（切り離しを法域に限る点で狭い）、リストの法律家が苛酷とした形（切り離しが利用者の側に義務を生む）を避けている。

**逆側。** 改め（reformation）は、縮減を認めない法域では使えない読みが立つ（`against.md` #25・`jurisdictions.md` のドイツの節）—— ドイツの縮減の不可は標準約款（AGB）についての規則で、ACD が AGB と読まれた場合だけの問い（BGB 305 条 1 項の AGB の定義と、310 条で事業者の受け手には 309 条が当たらないこと・`rounds/2026-11-16-bgb-305-310-gesetze-im-internet-snapshot.txt`・ACD が AGB かは確立していない）。その場合は §15.2 の第 2 文（その法域に限った切り離し）が働く。Perens 氏の観察は 2018 年までの、知る限りのもの。

**この節が establish しないこと。** 各法域の裁判所が §15.2 の改めの指示に従うか。

**反映**: 1c（`ACD-1.4-THIRD-CLARITY-TRIAL.md` §18.5 の §15.2 の行の支え —— 承認済みの CAL 7.6 と同じ型で、切り離しを法域に限る点で狭い・9b の帯）/ 入口（§15.2 の説明に CAL 7.6 との同じ型と違いを添えるか・50 へ）。

## 1.265 「作成者に不利な解釈の規則は、法域で違い、当たらないこともある」（Piana 氏 2017）—— §15.6 が法の解釈の規則を外し、§15.1 が受け手に有利な読みを本文で定める理由（2026-11-18）

オーナーの依頼（2026-11-16「法的解釈の不確実性を 5 人で減らし続けて」）の portfolio-2f の受け持ち（リストの法律家の発言を条ごとに当てる）。1.4 草案の §15.1 は *"This Dedication, in respect of the Work, is to be construed so as to give the widest permission and the least obligation upon You that its words allow, and so that, where a provision is capable of more than one reading, the reading that grants more to You prevails."* —— 受け手に有利な読みを、法の規則に任せず本文で定める。§15.6 は *"No rule of construction that resolves ambiguity against the drafter applies to this Dedication, and no rule that construes a grant narrowly against the grantee applies to it."* と、両向きの法の解釈の規則を外す。アーカイブの写しで法律家と決める側の人の通を "contra proferentem" と「起草者に不利に解釈」の語で当て、ドシエに無い 1 通を置いた（`rounds/2017-08-license-review-w3c-piana-contra-proferentem-observed.txt`）。起草者に不利に解釈する規則を外す条が承認済みのライセンスの定型であること（MPL 1.1 系・CDDL・CPAL、MPL 2.0 は貢献者の側だけに狭めた）は、`review-responses-boilerplate.md` の §15.6 の段に既に在る。

| 発言 | 誰が | §15.1 への当たり方 |
| :-- | :-- | :-- |
| *"a license might be interpreted beyond the intentions of the drafter and sometimes also not against her interests; in many laws there is a \*contra proferentem\* rule, but that may be recessive or non applicable, and anyway being based on contractual law, \*the rule itself\* would largely vary, never mind \*its concrete application\*."* | Carlo Piana 氏 2017-08-09（W3C Software and Document License の審査・特許を明示しないことの危うさについて） | **有利な面（§15.6 と §15.1 の組の理由）。** 作成者に不利な解釈の規則は、法域で違い、劣後するか当たらないことがある —— 法の規則に任せると、受け手に有利な読みが法域ごとに変わる。§15.6 が法域ごとの規則を外し、§15.1 が受け手に有利な読みを本文で定めるので、この揺れを文書の側で消す |

**読み。** §15.6 と §15.1 の組は、Piana 氏が「法域で違い、当たらないこともある」とした規則を外し、同じ向き（受け手に有利）の解釈の指示を本文に置く。規則を外す側は承認済みの定型（MPL 1.1 系ほか）で、本文が解釈の向きを自分で定める側が ACD の加えた部分である。

**逆側。** 本文の解釈の指示が、法域の解釈の規則（強行的な消費者法の解釈の規則など）より優先するかは、法域に依る。`review-responses-boilerplate.md` の §15.6 の段が書くとおり、規則を外す条は「起草者が保護規則から逃げている」と読まれうる —— §15.1 が同じ向きの読みを本文で残すことは、その読みへの答えになる。ACD の §15.1 は Dedicator にとって最も不利な読みを選ぶ指示で、受け手の側からこれを争う動機は乏しいが、Dedicator の承継人が争う場面は残る。

**この節が establish しないこと。** §15.1 の解釈の指示を各法域の裁判所が採るか。

**反映**: 1c（`ACD-1.4-THIRD-CLARITY-TRIAL.md` §18.5 の §15.1・§15.6 の行の支え —— 法の規則の揺れを本文で消す・9b の帯）/ 入口（`review-responses-boilerplate.md` の §15.6 の段に、Piana 氏の指摘を「外す理由」として添えるか・50 へ）。

## 1.266 「"may not" は読み違えられやすい、"must not" と書け」（Cowan 氏 2001・2003）—— 審査で実際に 2 通りの読みを指摘された語が、1.4 草案の §2.2 と §16.4 に在る（2026-11-18）

オーナーの依頼（2026-11-18「ACD-1.4-DRAFT.txt の法的解釈が一意に定まるように 5 人で連携しながら」）の portfolio-2f の受け持ち（審査者が他のライセンスの同じ語を実際に 2 通りに読んだ例を集め、ACD の同じ語に当てる）。アーカイブの写しで、決める側の人と法律家の通のうち「曖昧・読み違え・2 通りに読める」を述べた段の近くで引用符に入った語を、1.4 草案の本文と突き合わせた。草案の本文に在る語で、審査者が読み違えの恐れを名指したのは "may not" だけだった（"for any purpose" を「広すぎる」とした通は提出者 Hruska 氏の文で、審査者の文ではなかった）。2 通を置いた（`rounds/2001-02-license-discuss-osd-wording-cowan-may-not-must-not-observed.txt`・`rounds/2003-09-license-discuss-ossal-cowan-may-not-misreading-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I think you are absolutely right, and "may not" should be changed to "must not" everywhere. As evidence that "may not" means "must not" in this document, however, consider clause 6."* | John Cowan 氏 2001-02-16（"Wording in Open Source Definition"・OSD 自身の語について） | **割れの型。** "may not" は禁止（must not）とも、可能性（might not）とも読める。Cowan 氏は、同じ文書の中の対の文（一般の原則が "must not"、例が "may not"）から、その文書では禁止の意味だと読めると示した —— 文書の中の別の文が読みを閉じる、の型 |
| *"It would be better to word this "must not" rather than "may not", which latter is subject to misreading."* | John Cowan 氏 2003-09-25（Open Source Software Alliance License の審査） | **同じ型の 2 度目。** 審査で提出の文に対し、"may not" を "must not" に替えるよう求めた |

**1.4 草案の "may not"**: 本文に 2 か所あり、意図する意味が違う（portfolio-30 の反例で直した。最初の版は 2 か所とも禁止の読みが意図と書いていた）。
- §2.2 *"The Dedicator may not withdraw it, and may not impose any further term, condition, or restriction"*（1c の帯）: 意図は「力が無い」（撤回しても効かない）で、第 1 文 *"This Dedication is irrevocable."* の言い換え。Cowan 氏の勧めどおり "must not" にすると禁止の読みになり、「撤回は効くが約束に反する」という別の読みを作る —— T81 などで閉じてきた「法の効果の言い切りと義務の混同」の逆向き。直すなら、草案の §6.3 が他の権利者の留保について既に使う「力が無い」の言い方（§6.3 の "the Dedicator has no power to withdraw it"）と同じ形か "cannot withdraw it" の形で、法定の撤回（独 42 条・仏 L121-4・贈与の撤回）との関係（"under this Dedication" を添えるか）は 1c の判断。
- §16.4 *"A modified text may not be distributed under any name"*（9b の帯）: 意図は頒布の禁止で、Cowan 氏どおり "must not" が合う（±0 語）。§16.6 が Work の条件ではないと述べるので、受け手の Work の利用には及ばない。

**逆側。** 法の起草の慣行では "may not" は禁止として広く通る。"must not" に替えることは語数が増えず（±0）、別の読みを消すが、既に読みが閉じている §2.2 では語を変える利点は小さい。

**この節が establish しないこと。** 審査で ACD の "may not" が実際に問われるか。

**反映**: 1c（THIRD §19.1 の §2.2 の行 —— 意図は「力が無い」で、"must not" にすると禁止の読みを作る。第 1 文が力の無さに閉じるか、"has no power" の形にするかの判断）/ 9b（THIRD §19.5 の §16.4 の行 —— 意図は禁止で、"must not" の試作の種・±0 語）。

## 1.267 審査者が他のライセンスで名指した語の割れ —— 定義されない大文字の語（Piana 氏 2017）、否認の主語と許諾の主語の不揃い（Piana 氏 2025）、定義されない語は普通の意味で読まれる（Cowan 氏 2018）、語の使い方の不一致（Smith 氏 2025）。1.4 草案の同じ型を当てた（2026-11-19）

オーナーの依頼（2026-11-18・19「ACD-1.4-DRAFT.txt の法的解釈が一意に定まるように 5 人で連携しながら」）の portfolio-2f の受け持ち（審査者が他のライセンスで実際に指摘した語の割れを集め、ACD の同じ型に当てる・portfolio-30 の 3 巡目の型 (1) 名づけで外れる (2) 同じ語が条ごとに違う範囲）。アーカイブの写しで、決める側の人と法律家の通を「定義されない語・大文字・語の使い方の不一致・違う意味で使う」の語で当て、ドシエに引かれていない通のうち型の分かる 4 通を置いた（`rounds/2017-07-license-review-hooyami-piana-capitalised-undefined-observed.txt`・`rounds/2025-12-license-review-qmdeve-piana-authors-contributors-observed.txt`・`rounds/2018-10-license-review-sspl-cowan-functionality-undefined-observed.txt`・`rounds/2025-09-license-review-mgb-smith-inconsistent-terminology-observed.txt`）。

| 審査者が名指した型 | 誰が | 1.4 草案に当てた結果 |
| :-- | :-- | :-- |
| *"I also note that you have inserted an explicit patent license with capitalized terms like "Contributor" or "You", but those terms are not defined elsewhere."* | Carlo Piana 氏 2017-07-27（Hooyami License） | **当たらない。** 草案の本文の大文字の語を機械で拾い、定義の文（*"... means"*）と突き合わせた: 大文字で使われる語は Dedication・Moral Rights・Work・Dedicator・Covered Rights・You（Your）・Computational Use・Machine-Generated Material・Contribution・Reservation・the Steward で、すべて §1 か §16.5 で定義されている（ほかに大文字で現れるのは §16.1 の告知の文の中の名前だけ） |
| *"This comes to relevance since the disclaimer of liability refers to Authors or Copyright holders (not sure capitalized, since it's all caps). I am not sure if Authors includes Contributors"* | Carlo Piana 氏 2025-12-01（QmDeve License） | **当たらない。** §13 と §14 の否認と制限の主語は "THE DEDICATOR" で、許しの主語も "the Dedicator"。§2.6 が貢献者を "a Dedicator as to that Contribution" にするので、否認の主語に貢献者が入るかの割れは起きない（§1.4 の "operates severally as to each" と合わせて） |
| *"While we are at it, the use of "functionality" is extremely problematic. Since it is not a defined term, it must be read in its ordinary sense in connection with computers"* | John Cowan 氏 2018-10-18（SSPL） | **当たりうる（50 の帯へ）。** 草案の作用の条で、定義されずに範囲を決める語として §8.4 の "feature"（*"Section 8.1 alone governs a feature added to the Work"*・*"the feature that infringes it"*）が在る。普通の意味の「機能・特徴」で読むと、特許の請求項を侵害するのは製品や方法であって 1 つの特徴ではない、という点と噛み合わず、「特徴の 1 つが Work から来れば足りる」か「侵害する組み合わせの全体が Work から来ることを要する」かが割れうる |
| *"inconsistent use of terminology (Definition of "Source Form" and "Object Form" is different than in Apache, but body of license uses the formulation of Apache"* | McCoy Smith 氏 2025-09-22（MGB 1.0） | **当たらない（記録）。** 草案は "source code, object code"（§1.3・素材の種類）と "in source form, in object form, or in any other form"（§4.2・許しの及ぶ形）を使い分け、どちらも定義語ではない普通の語で、役が違う |

**読み。** 審査者が他のライセンスで名指した型のうち、1.4 草案に当たりうるのは「定義されない語が作用の条で範囲を決める」型（§8.4 の feature）だけだった。大文字の語の未定義と、否認と許諾の主語の不揃いは、草案には無い。

**逆側。** 機械で拾ったのは大文字の語だけで、小文字の普通の語が条ごとに違う範囲で使われる型（30 の型 (2)）は、語ごとに読む必要がある（9b の `scan_draft_ambiguity.py` の型 (a) が定義語の小文字を拾う）。

**この節が establish しないこと。** §8.4 の "feature" の 2 つの読みのどちらが審査で採られるか。

**反映**: 1c・50（UNIQUE-READING §19.3 の §8.4 の行 —— "feature" が定義されない語として範囲を決める点を、別の読みとして 2 巡目の行に・50 の帯）。

## 1.268 米国の著作権法と特許法、EU の DSM 指令の一次資料を 1.4 草案に当てた —— 新しく効くのは 17 U.S.C. §203(b)(1)（終了の後も残る派生物）、§101 と §204(a)（非独占の許諾に署名した書面は要らない）、35 U.S.C. §271(a)（侵害するのは発明であって特徴ではない・§8.4 の feature）の 3 つ（2026-11-19）

オーナーの提案（2026-11-19・1.4 草案が拠る法令の一次資料を 5 人で分担して読む。貼られた別の AI の一覧は材料で結論ではない）の portfolio-2f の受け持ち（米国と EU）。読む前に `rounds/` と `jurisdictions.md` を grep し、既に在るもの（DSM 4 条と前文 18・DB 指令 7・8・15 条・VARA 106A 条 (e)(1)・17 U.S.C. §205(e)）を除いて取った。写しは `rounds/2026-11-19-us-title-17-35-and-dsm-2-3-7-snapshot.txt`（WebFetch の逐語の片で、バイト単位の写しではない。§203 の 3 つの文字列と DSM 2 条 2 号・7 条 1 項は 2 度目の取得で確かめた）。

| 法源（写しの番号） | 当てた 1.4 草案の条 | 結果 |
| :-- | :-- | :-- |
| 17 U.S.C. §203(b)(1) *"A derivative work prepared under authority of the grant before its termination may continue to be utilized under the terms of the grant after its termination, but this privilege does not extend to the preparation after the termination of other derivative works"*（[9]） | §4.1 の licence（`jurisdictions.md` の §203 の表は「§4 に届く。終了されうる」とだけ書く） | **新しい（有利と不利の両方）。** 著作者が 35 年後に §4 の licence を終了しても、終了の前に作られた派生物は許諾の条件のまま使い続けられる。逆に、終了の後に新しい派生物を作る許しは §4 からは来ない（残るのは §3 と §5 の足場で、`jurisdictions.md` の表のとおり不確実が直列につながる）。派生物に当たらない写しの扱いは (b)(1) は言わない |
| 17 U.S.C. §101 *"but not including a nonexclusive license"*（[1]）と §204(a) *"is not valid unless an instrument of conveyance, or a note or memorandum of the transfer, is in writing and signed by the owner of the rights conveyed"*（[10]） | §4.1 *"non-exclusive"*。ACD は署名しない文書として当てられる | **新しい（有利）。** §4.1 の licence は「著作権の移転」に当たらないので、§204(a) の署名した書面の要件は掛からない。**逆側**: 後の移転に対する優先（§205(e)）は署名した書面を要する（`errata.md` に在る）、視覚芸術の人格権の放棄も同じ（VARA 106A 条 (e)(1)・`rounds/2026-11-16-us-ucc-vara-and-eu-trademark-snapshot.txt`）。§203(a) の *"executed by the author"* が署名の無い付与に当たるかは制定法の文からは決まらない（法の側） |
| 35 U.S.C. §271(a) *"whoever without authority makes, uses, offers to sell, or sells any patented invention … or imports into the United States any patented invention … infringes the patent"*（[13]） | §8.4 *"the feature that infringes it"*、§8.1 の動詞 | **新しい（§8.4 の feature の種を強める）。** 制定法の上で侵害するのは *"patented invention"*（請求項の全体）であって 1 つの特徴ではない。§1.267 で 50 へ送った「特徴の 1 つが Work から来れば足りるか、侵害する組み合わせの全体を要するか」の割れは、§8.4 の語が侵害の主語を特徴に置いたことから来る。§8.1 の動詞（make, have made, use, offer, sell, … import）は §271(a) の 5 つの行為を全て覆い、*offer* は *offers to sell* より広いので、当たらない |
| 35 U.S.C. §261 の最後の段 *"shall be void as against any subsequent purchaser … unless it is recorded"*（[12]） | §8 の約束と許諾が特許の譲受人に及ぶか | **当たらない（法の側のまま）。** 登録の要件が掛かるのは *"assignment, grant or conveyance"* で、直前の段の *grant* は独占の権利の付与を指す。非独占の許諾が後の譲受人を拘束するかは制定法の文からは決まらず判例法の側 |
| DSM 指令 2 条 2 号 *"'text and data mining' means any automated analytical technique aimed at analysing text and data in digital form in order to generate information"*（[15]） | §1.7 と §1.10 の定義されない語 *"text and data mining"* | **当たらない（一意）。** EU では ACD の *text and data mining* がこの定義に当てて読まれうるが、§1.7 は TDM を *"any automated processing of the Work"* の例の 1 つに置き、§1.10 は *"permission for text and data mining or for the use of a work in developing a machine learning model"* と学習を別に挙げる。学習が 2 条 2 号の TDM に入るかの争いは、ACD の範囲を割らない |
| DSM 指令 7 条 1 項 *"Any contractual provision contrary to the exceptions provided for in Articles 3, 5 and 6 shall be unenforceable."*（[17]） | §6.2・§6.3（Reservation を置かない・取り消す） | **当たらない（記録）。** 4 条（商業の TDM）は 7 条 1 項に挙がらないので、権利者は契約や留保で 4 条の例外を外せる —— だから §1.10 は *"contractual term"* を Reservation に含め、§6.3 は Dedicator が置いた留保を *"to the fullest extent the Dedicator is able"* で取り消す。3 条（研究機関の TDM）はもともと契約で外せないので、ACD の許しと重なるだけ |
| 17 U.S.C. §107（[2]）・DB 指令 9 条（[19]）・§201(d)（[3][4]） | ACD の許しの外の例外、権利の分割 | **当たらない。** フェアユースと DB の例外は ACD と独立に働く。§201(d)(2) が権利を分けて持たせるので、Dedicator が一部の権利しか持たない場合に ACD が及ぶのは持つ分だけ —— §13 が権原を保証しないことと整合する |

**読み。** 米国と EU の一次資料のうち、1.4 草案の読みを動かすのは §271(a)（§8.4 の feature の割れの根）だけで、§203(b)(1) と §101・§204(a) は法の側の記述（`jurisdictions.md` の §203 の表と THIRD §18 の米国の行）を正確にする材料である。

**逆側。** 写しは法典の文で、判例（§203 の "executed" の解釈、非独占の特許の許諾の承継、TDM の定義の範囲）を取っていない。§203(b)(1) が派生物を残すのは「許諾の条件のまま」なので、§4.1 の licence が終了した後にその条件が何を意味するかは読みが要る。

**この節が establish しないこと。** ACD の §4 の licence が §203 の *"executed by the author"* に当たるか。学習済みのモデルが §203(b)(1) の派生物に当たるか。

**反映**: 50・1c（§8.4 の feature —— §1.267 の種に §271(a) の根を足す・UNIQUE-READING §19.3）、30（`jurisdictions.md` の §203 の表の §4 の行に §203(b)(1) の残るもの、§204(a) の書面の要件が掛からないこと）。

## 1.269 回避と管理情報の法の授権の置き場所 —— 米国は回避の定義（17 U.S.C. §1201(a)(3)(A)）に、EU は技術的手段の定義（指令 2001/29/EC 6 条 3 項）に置く。T124 の範囲の句が下流の頒布者の手段を外しても、EU では手段の地位を 6 条 3 項が決める（2026-11-19）

オーナーの提案（2026-11-19・関連法令の一次資料を 5 人で分担して読む）の portfolio-2f の受け持ち（米国と EU）。T124（§5.2(a) に回避の授権と力の放棄を足す試作・§19.2 の行）の法源として、17 U.S.C. §1202・§1203 と指令 2001/29/EC 6 条・7 条を取った（`rounds/2026-11-19-us-17-usc-1202-1203-snapshot.txt`・`rounds/2026-11-19-eu-infosoc-2001-29-art-6-7-snapshot.txt`。EU の文は legislation.gov.uk の英国保持版で、EU の採択時の文は道具が読めなかった。6 条の 3 つの文字列は 2 度目の取得で確かめた）。§1201 は portfolio-9b の写し（`rounds/2026-11-19-us-17-usc-203-1201-snapshot.txt`）。

| 法源 | 授権がどこに在るか | T124 と 1.4 草案への当て |
| :-- | :-- | :-- |
| 17 U.S.C. §1201(a)(3)(A) *"without the authority of the copyright owner"*、(a)(3)(B) *"with the authority of the copyright owner"* | **回避の定義**と、手段が「実効的に管理する」ことの定義の両方 | 受け手 B が §4.1 の licence（*"for any purpose whatsoever"*）の下で Work に掛けた手段は、(a)(3)(B) の *with the authority of the copyright owner* を満たしうるので保護される手段になりうる。そのうえで C の回避が「権限なし」かは Dedicator の授権で決まる —— **米国では T124 の範囲の句（50 の案: Dedicator が掛けた手段か、Dedicator のために掛けられた手段）が B の手段の扱いを実際に決める** |
| 指令 2001/29/EC 6 条 3 項 *"designed to prevent or restrict acts, in respect of works or other subject-matter, which are not authorised by the rightholder"* | **手段の定義** | §4.1 は Covered Rights の全ての行為を誰にでも許すので、Work の写しに掛けた手段が妨げる行為は、Dedicator の権利については *not authorised* ではない —— その手段は、Dedicator の権利について 6 条 3 項の *technological measures* に当たらないと読める。**EU では T124 の範囲の句が B の手段を外しても、B の手段の保護は 6 条 3 項の定義の側で決まり、T124 はそれを変えない**。逆に読み (i)（§3 が効かない場合に第三者の前で回避が権限なしのまま）は、EU では §4.1 だけで既に狭い |
| 17 U.S.C. §1202(b) *"without the authority of the copyright owner or the law"*・末尾 *"knowing … that it will induce, enable, facilitate, or conceal an infringement"*、指令 7 条 1 項 *"knowingly performing without authority"* | 管理情報の除去・改変の禁止 | `jurisdictions-sources.md` (5) の読み（§10.2 *"You need not give attribution, reproduce any notice"* が授権を与える）と整合。加えて §1202(b) は侵害を招く・隠すことの知を要し、§4.1 が全ての利用を許すので隠す侵害が無い。**新しい割れは無い**。作者の名を偽る改変は §11.3（偽の言明）の側 |
| 17 U.S.C. §1203(a) *"Any person injured by a violation of section 1201 or 1202 may bring a civil action"* | 原告の範囲 | §19.2 の T124 の行が引く *any person injured* の出典（行の出典の欠けを埋めた） |

**読み。** 授権の置き場所が米国と EU で違う。米国では「誰の手段か」と「回避が授権されたか」を T124 の語が決め、EU では §4.1 の許しが手段の定義の側に効く。T124 の範囲の句の効き目は、米国に向けた設計として説明できる。

**逆側。** (1) B が Work の上に自分の権利（自分の改変の著作権、データベース権）を持つとき、その権利についての行為は B が許していないので、EU でも B の手段はその範囲で 6 条 3 項の手段に当たる。(2) 6 条 3 項の読み（許された行為を妨げる手段はその権利について手段でない）は我々の文言の読みで、EU 司法裁判所の判断（技術的手段の比例性を論じた判決）を取っていない。(3) 写しは英国保持版で、EU の採択時の文と一致するとは確かめていない。

**この節が establish しないこと。** §4.1 の licence が米国の §1201(a)(3)(B) の *with the authority of the copyright owner* を B に与えると裁判所が読むか。EU で許された行為を妨げる手段が保護されないという読みが判例で採られているか。

**反映**: 1c・50（T124 の行の根拠に「範囲の句は米国に向けた設計、EU では 6 条 3 項が決める」を足す・`ACD-1.4-UNIQUE-READING.md` §19.2）、THIRD §18 の §5.2 の行（写しの名を結んだ）。

## 1.270 職務著作を §2.6・§1.9・§2.2 に当てた —— 米国では雇用者が著作者なので、貢献を献呈の下に入れるのは「誰の提出か」、終了権は職務著作に無い（2026-11-20）

オーナーの提案（2026-11-19・関連法令を 5 人で分担して読む）の portfolio-2f の受け持ち（米国）。17 U.S.C. §101 の職務著作の定義・§106・§201(a)(b) を取った（`rounds/` の `us-17-usc-101-wmfh-106-201` の写し・WebFetch の逐語の片）。30 の 3 巡目の型 (3)「役が入れ替わる」を、提出する人と権利を持つ人が別になる場面に当てた。

| 法源 | 当てた条 | 結果 |
| :-- | :-- | :-- |
| §101 *"a work prepared by an employee within the scope of his or her employment"*・§201(b) *"the employer or other person for whom the work was prepared is considered the author … and … owns all of the rights comprised in the copyright"* | §2.6 第 1 文 *"the person making it becomes a Dedicator as to that Contribution"*、§1.9、§1.4、§2.7 | **読みは本文の語で一意、残りは法の側。** 従業者が雇用の中で書いて出した貢献の権利は雇用者に在り、従業者は §1.4 の限度で何の Dedicator にもならない。献呈が及ぶのは、§1.9 *"made by or on behalf of the person"* の下で雇用者が提出した者と読める場合 —— 提出の手を動かした人ではなく本人を受ける語は本文に在る。従業者の提出が雇用者を拘束するか（代理の成否）は法の側で、THIRD §18 の §2.6 の行へ |
| §203(a) *"any work other than a work made for hire"*（2026-11-19 の写し） | §2.2・§4.1 | **有利（記録）。** 雇用者が職務著作の Work を献呈したとき、§203 の終了権はそもそも無い。`jurisdictions.md` の §203 の表（§4 に届く）は、著作者が自然人の場合の記述 |
| §101 の定義 (2) の *"if the parties expressly agree in a written instrument signed by them"* | §2.6 第 4 文 *"This Dedication requires no separate instrument"* | **当たらない。** 委託の著作物を職務著作にする書面は当事者の間の権利の帰属の問いで、ACD の下に貢献を入れる行為の方式ではない |

**逆側。** (1) 雇用者が貢献を知らない場合（従業者が勝手に出した）、§1.9 の *on behalf of* は立たず、貢献は誰の献呈の下にも無いまま Work に入る —— §2.6 の識別の約束は Dedicator（企画の側）が、Contribution でない素材を *"includes … or causes it to be included"* したときにだけ掛かり、Dedicator は外れたことを知らないと識別できない。§13 は権原を保証しない。(2) 米国の外では、雇用の中の著作物の帰属は国ごとに違い（日本の著作権法 15 条の職務著作、ドイツ UrhG 43 条は著作者を従業者に残す）、この節はそれらを取っていない。

**この節が establish しないこと。** 従業者の提出が雇用者の代理に当たると裁判所が読むか。

**反映**: `ACD-1.4-UNIQUE-READING.md` §19.1 の末尾の §2.6 第 1 文の行（3 巡目）、THIRD §18 の §2.6 第 1 文と §2.2 第 1 文の行（写しを結んだ）。30・1c へ: 日本の職務著作（15 条）とドイツ（43 条）を、30 の日本の分担と 9b の取得で。

## 1.271 PSF-2.0 の提出は 72 日、`license-review` で返事を受けていない —— 採用の実績を背にした提出の待ちの観測（2026-11-22）

`license-review` の 2026 年 11 月の写し（11-21 23:37 UTC に写しへ置かれた・portfolio-50 の日次の取得の記録は同じ時刻に「11 月は 404」と書いていて食い違う —— 50 へ知らせた）に 1 通: Max Mehl 氏 2026-11-20 *"There has not been any feedback on the license submission of PSF-2.0 so far, see the post below. Is there anything the community can do to facilitate the process?"*（`rounds/2026-11-license-review-psf-submission-no-feedback-ping-observed.txt`）。提出は 2026-09-09（`rounds/2026-09-09-license-review-psf-submission-observed.txt`・`AS-OF.md` の "What a submission to `license-review` looks like when the submitter can rely on adoption" の行）で、09-28 に同じ人が *"with no replies so far"* と書き（`rounds/2026-09-28-license-review-python-licenses-followup-observed.txt`）、11-20 までの 72 日、提出のスレッドに返事は無い（9 月〜11 月の写しの件名で数えた）。

**読み。** 承認済みの Python-2.0.1 の構成部分で、3 つのプロジェクトの採用を挙げた提出でも、`license-review` は 2 か月半返事をしないことがある。ACD の提出の計画が「出せば審査が始まる」と前提しているなら、その前提は観測と合わない —— 待ちの長さは、本文の出来と独立に起こりうる。

**逆側。** (1) 沈黙は却下でも反対でもない —— PSF-2.0 は争点の少ない、既に承認された構成の一部で、審査者が「論じることが無い」と読んでいる可能性もある（その場合の沈黙は ACD のような新しい型には当たらない）。(2) 2026 年の審査者の人数と、同じ時期の他の提出への返事の速さは数えていない。(3) 返事の無さの理由を述べた通は、写しに無い。

**この節が establish しないこと。** ACD を出したときの待ちの長さ。PSF-2.0 が無視されているのか、順番を待っているのか。

**反映**: 入口 —— 50（OSI-EVENTS の 11-21 の行と REVIEWERS の Status の「`license-review` の 11 月は 404」を、この 1 通に合わせて直す）、30（`OSI-APPROVAL-PLAN.md` の提出の段の待ちの前提に、この観測を逆側として）。
