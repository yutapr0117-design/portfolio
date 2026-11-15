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
