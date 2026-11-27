---
file: LICENSES/ACD-OSI-BOTTLENECKS.md
audience: 次のセッションの実装者（一次読者）/ OSI license-review participants / 監査人
last-updated: 2026-11-26
canonical-ref: LICENSES/ACD-1.0.against.md (不利な事実の本体) / LICENSES/ACD-1.0.errata.md (本文の既知欠陥) / LICENSES/AS-OF.md (外部事実と検証日) / LICENSES/ACD-1.0.objection-map.md (反論の当否)
---

# OSI Approval Bottleneck Register

**この文書が唯一の canonical なボトルネック一覧である。** 他の文書はここを参照し、
同じ問題を独立に管理しない。

**目的は欠陥を数えることではない。** 目的は **OSI Approved への到達を阻害する要因を除去し、
残る不可制御要因を減らすこと**である。不利な事実（`against.md`）は**入力**であって、
ここに載るのは**承認確率に効くもの**だけである。

## English index for reviewers

**The analysis below is mostly in Japanese, so this table is the whole register in English.** "Who can
move it" names who has to act. The status is our own reading, not OSI's. Section numbers are those of
ACD-1.4, the version that would be submitted; where 1.0 numbers a clause differently, its number follows
in parentheses.

| ID | The problem | Severity | Where it stands | Who can move it |
|---|---|---|---|---|
| B1 | No legal review | Highest | Nothing here supplies it. It is not a requirement: the process asked for an analysis by a licensed practitioner until December 2007 and then dropped it (`review-rules.md` §1.141). Members keep asking submitters for one (#291), and the review is *"not for workshopping a license"* (#298). Other side: a reviewer who later sat on the Board reads the disclosure item as more than that: McCoy Smith, 2024-01-29, *"which is a requirement of submission"*, adding that posting a licence to the list for its lawyers to review does not count; the chair's answer that year was *"we do not require review by a lawyer, only recommend it."* (Pamela Chestek, 2024-12-18). In a talk published 2026-11-24 the chair of the License Committee, McCoy Smith, said that using an AI is at the moment no substitute for using a lawyer to write a licence (#333); the two main reasons for rejection he gave are about the text, not its author. Of at least 24 new licences submitted with no review, one is on the list (#297). The questions a lawyer would need are in `QUESTIONS-FOR-COUNSEL.md`. On 2026-11-26 (`review-readings-7.md` §1.490): Pamela Chestek (2025-10-26), on a submission full of defects, wrote that fixing all its problems *"is not a task that a layperson can competently do without professional assistance"*, agreed it *"needs the input of a licensing professional before the OSI reviews it again"*, and urged withdrawing to reconsider *"whether this license is necessary at all"*. Not about ACD by name, but it bears on a text drafted by models with no lawyer's eyes. Other side: one submission's opinion, not a rule; the reason given was the number of defects, not the drafting tool — though the need for professional help to fix them applies to ACD as it stands. On 2026-11-26 (`review-readings-7.md` §1.491, on the review of the four licences rejected 2026-09-24, #335): Pamela Chestek (2026-01-24) called one licence *\"a good example of why it is highly unlikely that a license not written by a lawyer can be approved\"*; Bruce Perens (2026-01-25) stopped reading a submission whose author said no lawyer was used; Carlo Piana (2026-05-04) read a text as having had no lawyer's eyes; Chestek (2026-06-08) wrote that legal documents carry drafting conventions and rules of interpretation. Other side: the same person wrote *\"not a blocker\"* on 2024-12-18, and the four rejections turned on the quality of the drafting and the shape of the response (no response, or rebuttal without revision), not on the absence of a lawyer. On 2026-11-26 (`review-readings-7.md` §1.494): McCoy Smith, as chair (2026-03-17), quoted the submission page's item on legal review and asked a submitter to say whether any lawyer was involved; before he became chair (2025-12-22), after seeing a drafting error in another submission, he wrote that any future submission would need to show that a legal review had been done, and by whom. ACD cannot show that one was done; answering "none" in its disclosure is not the answer that sentence looks for. Carlo Piana, a Board member (2026-03-18), recommended a competent lawyer before reviewers spend their time. Other side: each was about one submission, the 2025-12 sentence is hedged ("I think") and tied to that submission's error, no rule makes review a requirement, and the 2026-03 request was to fill in the item, which ACD does. Remaining work: re-read the current review-process page (an attempt to fetch it from this session on 2026-11-23 was refused for permissions; the fetch is done from the Mac side). On 2026-11-27 (#336, `review-readings-7.md` §1.495): McCoy Smith, months before he became chair (2025-10-02, replying to the drafter of PUWL), in the reply that granted the gap, advised against drafting it oneself. Other side: a personal reply, not a rule. | The owner, by engaging one |
| B2 | One adopter: this repository | Highest | We can improve discoverability. We cannot produce adoption, and will not claim any. Non-use alone has not been a ground (Committee rationale, 2020 and 2021). The one hold on record (Tiwaz, 2025-09-11) lifts if one project uses the licence or expresses interest. Approval would not by itself put ACD on an adopter's list of accepted licences or on a licence chooser, where the dedication type is already present (#322) Other side: a Committee member counted a substantiated use case among the criteria he applied to a new licence (Josh Berkus, 2017-10-24); and the chair, asked about adopters' policies and not about approval, described a licence with only its drafter behind it as having no community, adding that a single project may do (2026-11-24, #333). On 2026-11-26 (`review-readings-7.md` §1.490): Pamela Chestek (2025-10-26) opened on a defect-heavy submission by citing the submission guide's adoption item: *"Is this license in use? If not, who is your intended user?"* Other side: a question, not a ground for refusal; the same letter asks *"whether this license is necessary at all"* (B10) at its close. On 2026-11-27 (#336, `review-readings-7.md` §1.495): McCoy Smith, months before he became chair (2025-10-02, replying to the drafter of PUWL) named Creative Commons as the maker for that gap, which reads as preferring a large maker behind such an instrument. Other side: a personal reply, phrased as a question ("CC0-2.0?"). | Third parties; the owner can ask |
| B3 | Length: ACD-1.4 has 5,879 words, 16 sections, 80 clauses (1.0 had 4,896 words and 82 clauses) | High | Longer than GPL-3.0 both in full (5,644) and in the operative text, and its sentences are longer than 1.0's (`against.md` #6, #329). Cutting sentences could not answer it; on 2026-11-24 the 1.5 draft was rewritten to say each thing once. When adopted as the draft it had 3,168 words, 10 sections and 50 clauses, with 4 of 144 sentences over 45 words (ACD-1.4: 28 of 191); it has changed since: measured 2026-11-25, the draft (n8) has 3,479 words, 10 sections and 52 clauses, with 9 of 151 sentences over 45 words (6.0%; longest 58 words); the list of places where the meaning moved is in `ACD-1.5-CHANGELIST.md`. The draft is not frozen and is not the submission target. Other side: it was rewritten in one day by AI models, no lawyer and no third party has read it, every clause number changed, and Bruce Perens wrote in 2017 that a licence that is merely shorter would be a disservice to approve. On 2026-11-26 (`review-readings-7.md` §1.490): Pamela Chestek (2025-10-26) wrote of a submission *"You have many sections that are unnecessary, circular, or redundant"*, and of a grant split across four sections, *"I don't understand why the copyright grant is broken up into four sections"*. ACD-1.4 repeats *"need not determine"* in §4.4, §8.6 and §12.2 (the §1.481 pattern — it applies). Permission language also sits in §6.1 (Computational Use) and §7.2 (databases), which could read as the same pattern — but §3, §4 and §5 are a waiver, a licence and a promise, different workings, and §6.1 and §7.2 state explanations within §4's scope (*"so far as the Covered Rights …"*), so the licence's scope is not split (the 1.5 draft gathers the Covered Rights licence in 2.2). On 2026-11-26 (`review-readings-7.md` §1.491, the patterns of criticism in the review of the four licences rejected 2026-09-24): a missing grant, a name written in, the range of recipients, and a collapsed grant section do not apply to 1.4. What applies are four Low patterns — the words for a changed work in two forms (errata E94), *made available* not saying to whom the provision is made (the register), headings and numbering (a contribution clause in §2, an unnumbered paragraph in §5.2), and the repeated listing of models and outputs (next to E47; in 1.4 the words agree and only repeat in three places. 1.5 gathers them in the single definition of Result). Other side: we did the matching; there is no guarantee a reviewer counts the same way. On 2026-11-26 (`review-readings-7.md` §1.493): a search of deciders' messages since 2019 found no acceptance of a rewrite that only shortened a licence without changing its effect; one 2026 rewrite was called a poor attempt at rewriting MIT, and the plain-language licence that was accepted (Blue Oak, 2024) was written by lawyers and added a patent grant. So length is not offered as a reason to approve. Other side: the 1.5 draft is the same steward's next version, not a rewrite of someone else's licence, and lists 31 differences in effect; Blue Oak's lawyers are what ACD lacks (B1). | Us, in part |
| B4 | The §3 surrender beside the §4 licence | High | Tested as a possible structural refusal, and that was rejected. An article on OSI's site named the two parts as the solution in 2017. In the 2012 straw poll on CC0 all 13 votes against named patents and none named the structure, though one reviewer objected to the form that year. What OSI reviews is the licence part: *"OSI could analyze CC0 for its license fallback terms, but not as a public domain dedication"* (Lawrence Rosen, 2011; the same line in 2003, `gap-measurements.md` §1.143, §1.146). The judgment is OSI's Other side: after the WTFPL was refused in 2009, the chair objected that a licence giving the licensees every permission does nothing to protect the licensor, and ACD's §10.1 gives every permission too (Russ Nelson, 2009-03-19). | OSI |
| B5 | The legal account in §4.4 | Medium | The drafting defect closed in 1.1. The design question stays open | OSI |
| B6 | The name | Medium | Decided on 2026-10-24: no rename Other side: all 58 licence names we found that use "Commons" come from Creative Commons or the ODC, and "Dedication" names only half of what the text does (measured for the decision of 2026-10-24). | Decided |
| B7 | §8.4's patent reach may lower uptake | Medium | A one-way trade with B10. Both mitigations are structurally closed. On features added later, deciders have refused both ends: a licence that loses the patent grant *"the moment a change is made to the software"* (Pamela Chestek, 2025-09-19) and one that grants *"any patent affecting the software regardless of modifications"* (Josh Berkus, 2019-12-06); ACD-1.4 §8.4 stands between, since §8.1 alone governs a feature added to the Work (`review-readings-7.md` §1.486). Deciders have measured reach mainly by the word *embodied* (Lawrence Rosen, 2002 and 2016; Josh Berkus, 2016), and words against a broad grant are on record: *"in use of the licensed copyrighted property, and no more"* (Bruce Perens, 2025-11-12) and *"with no boundaries as to scope"* (McCoy Smith, 2018-09-26). ACD-1.4 §8.4's *"results, in whole or in part, from the content of the Work"* is broader than that main word, and we found no approved clause with the same wording (`review-readings-7.md` §1.485). Other side: a modifier has to be able to tell whether the grant covers them (Josh Berkus, 2014-04-15), and a causal test on a trained model is hard to apply; Pamela Chestek (2025-03-13) treats not suing users of an unmodified version on any theory as the minimum line, and combination language exists in approved BSD+Patent. On 2026-11-26 (`review-readings-7.md` §1.490): Pamela Chestek (2025-10-26) called a submission whose contributor patent grant was narrower than the licensor's and did not reach derivatives a non-free licence: *"The lack of necessary scope in the Contributor patent grant, in my opinion, makes this a non-free license."* ACD's contributors become Dedicators as to their contributions, and §8.1 reaches *"the Work or anything derived from it"*, so the shape matches (in our favour). Other side: §8.1 is limited to what is *"caused by subject matter contained in the Work"*, and if a contributor's Work is read as only the contribution, a claim first infringed by the combination of the contribution with the original Work could read as outside (Apache-2.0 names it: *"by combination of their Contribution(s) with the Work"*). The 1.5 draft 2.3(a) names the combination and closes it; recorded as errata E95 on 2026-11-26. | OSI |
| B8 | §12 moral rights | Medium | The same clause has been called a gap and mission creep. Both are recorded | A lawyer |
| B9 | §7 database right | Low | Checked and kept | Decided |
| B10 | Is the remaining gap enough for a new licence? | Highest | One effect stands on the text of all 141 approved licences: a patent grant beyond the work with no condition and no termination. John Cowan observed in 2014: *"We may not be in the business of approving licenses without patent grants any more"* (`gap-measurements.md` §1.144). Reach past the work has been approved once, to works the licensor lists: UPL in 2015, after Lawrence Rosen said such reach is *"more generous than the OSD requires"* (`gap-measurements.md` §1.154). No one close to the decision has supported a reach to a model or its output (#305). The same shape without that patent grant, a public-domain dedication with a fallback that asks for no attribution, was put to the lists in 2012 and 2015. One reply asked what it solved that the MIT License or the Fair License did not; the other said there were more than enough such licences (`review-readings.md` §1.184, `gap-measurements.md` §1.146). Whether that is enough is OSI's call. In ACD's favour on the patent half: a Committee member read an express withholding of patent rights as contrary to OSD 7, *"The withholding of a patent license means that an additional patent license must be executed."* (Pamela Chestek, 2023-08-15, on the Mulan licences); §8 grants directly. A director, in his own capacity, has since said the same of an express denial: *"So I think for that reason alone this one violates OSD 1 & 7."* (McCoy Smith, 2025-11-03, on TERO-GL; `review-readings-7.md` §1.479). Both spoke of an express withholding or denial, as in CC0, not of licences silent on patents, Mulan was declined for its subject matter (B15), and Josh Berkus, in the same thread as Smith, called a licence that merely leaves patents out allowable (2025-11-03), so this supports the patent grant, and the gap as against CC0 (which withholds patents expressly; the Committee named that clause, 4(a), when CC0 was not approved in 2012, `board-decisions.md`), but not the gap as against 0BSD, MIT-0 or the Unlicense, which are silent on patents. Other side: a new identifier costs reviewers and licence tooling even where a difference exists (Carlo Piana, 2025-07-18). On 2026-11-27 (#336, `review-readings-7.md` §1.495): McCoy Smith, months before he became chair (2025-10-02, replying to the drafter of PUWL), said there was room for a CC0 without the disclaimer of patent rights, which is the gap ACD claims. Other side: in the same reply he advised against drafting it oneself and named Creative Commons as the body that should (B1, B2, B12); it was a personal reply, not a rule. | OSI |
| B11 | SPDX and REUSE naming | Low | Deliberately not submitted yet. A compliance data service has said it handles LicenseRef identifiers, not only approved licences (2026-11-26, not checked verbatim), so an adopter's `LicenseRef-ACD-1.4` can reach the tools. Other side: reaching the tools is neither adoption nor approval, and the SPDX list's condition of substantial use is unchanged | OSI, then SPDX |
| B12 | One steward, and succession | Low | The recorded worry is control, and ACD has no upgrade clause. No successor is named Other side: if the Steward dies or dissolves without assigning the role, the text does not say who may issue new versions (§16.5). On 2026-11-27 (#336, `review-readings-7.md` §1.495): McCoy Smith, months before he became chair (2025-10-02, replying to the drafter of PUWL) named Creative Commons as the maker, which reads as preferring an established large steward to a new small one. Other side: he was not discussing how many stewards a licence should have. | The owner, and someone willing |
| B13 | The cost of understanding this submission | High | Continuing. It is the only real relief for B3 Other side: most changes made for precision add words, so relief here is paid for in B3, and reviewers meet each new draft expecting the same misconceptions (Bruce Perens, 2025-12-03). On 2026-11-27 (`review-readings-7.md` §1.497): Carlo Piana (2025-02-20, replying on MGB 1.0) wrote that licences must work under any relevant jurisdiction and that arguing a text works the same way in a particular jurisdiction is not a good defence. So the entry leads with the form that does not depend on jurisdiction (§4.4, §12.2) and keeps the per-country readings as material for questions. Other side: he wrote about another submission; that ACD names no governing law is supported by the then chair (2025-02-14). | Us |
| B14 | The moderators' notice on AI-written posts | Highest | The decision is OSI's. At least three posts were rejected by moderation Other side: three members of the Licensing Committee said in March 2026 that an AI having drafted a licence does not bear on how it operates. | OSI, the owner |
| B15 | Subject matter: §1.3's list (§1.2 in 1.0) touches a reason the Board gave in 2023 | High | The Committee stated a test in 2021 (CERN-OHL): licences *"written such that they can be used for software"* are appropriate for review. ACD meets it on its face. In 2024 OSI's Executive Director said review may reach datasets and model parameters. §1.3 is wider than CERN's, and the judgment is OSI's Other side: a current reviewer asks whether a licence reaching beyond software can be judged by software standards (Carlo Piana, 2026-08-31), and naming non-software material is where that question starts. | OSI |

## 2026-09-11 の掘削で確定したこと（この節は結論だけ。逐語は `review-corpus.md` §1.67〜§1.70a）

**この日、`license-review` の 2024-01〜2026-09（33 か月・804 通・111 スレッド）を取得し、
基準・規則・結果の 3 層を一次資料で押さえた。register の各項目はこれを前提に読む。**

1. **承認の基準は 8 条あり、原典に書いてある。** `review-process` の "Standard for new licenses"。
   **7 条は我々の側で確かめられ、いずれも通る** ——再利用可能性（前半）/ licensor 優遇なし /
   曖昧性の実質的影響（§15.1・§15.3）/ 適用の変化幅 / **提出時点で遵守可能（義務ゼロなので自明）** /
   完全なテキスト（外部参照 0）/ **gap を埋めること**。**8 条目（明晰さ）だけが判断の余地を残す。**
2. **その明晰さの代理指標（文長）は比較群の中ほどにあり、出す版の値は 1.0 より悪い**（§1.70a / §1.70b・**三度の訂正を経ている**）——
   `measure_clause_clarity.py --fetch`（方法は道具の docstring・比較群は SPDX の Apache-2.0 / MPL-2.0 / EPL-2.0 / OSL-3.0 / CDDL-1.0）で
   2026-11-23 に測ると、**1.4 の本文は平均文長 28.9（6 本中 4 番目に短い）/ 45 語超の割合 14.7%（6 本中 4 番目に低い）/
   最長文 93 語（2 番目に短い）**。1.0 は 26.0 / 10.3% / 81 語で、平均は同じく 4 番目、45 語超は 2 番目に低かった
   （CDDL-1.0 の 10.2 だけが低い）。1.3 は 27.5 / 11.9% / 81 語。**出す版の文は、議論に出した版の文より長い**（`against-2.md` #329）。
   **⚠ 2026-11-23 訂正**: 旧文は見出しを「代理指標では良い側にある」とし、*「平均文長 26.0（7 本中 3 番目に短い）/
   45 語超の割合 10.3%（最小）」* と述べていた。これは 1.0 を 09-14 の比較で測った数で、09-28 の再実行
   （`submission-reference.md` の文長の行）で 1.0 自身が平均 4 番目・45 語超 2 番目に動いていたのに、ここは直っていなかった
   （portfolio-5e の測定で見つけた）。**逆側**: 文の短さは明晰さではない（道具の docstring）。1.4 で長くなった文は読みの分岐を
   閉じる限定を足したものが多く、分けると掛かり先が新しい分岐を生みうる。従属語 2 つ以上の長文の割合は 1.3 の 63.6% から
   1.4 の 60.7% へ下がった。
   **⚠ 2026-09-14 に 2 つ取り下げた**: *「最長文は 6 本中で最短」*（再実行では OSL-3.0 の 76 語が
   ACD の 81 語より短く、**順位が方法に依存する**）と *「従属節を 2 つ以上積んだ長文は 0 件」*
   （**その列の定義がどこにも記録されておらず再実行できない**。方法を書いた指標では 61.1% で
   結論が逆向きになる）。**したがって *「解析の負荷という意味では最も軽い」* は register から外した。**
   **これが動かさないもの: B1（弁護士レビュー無し）は 1 ミリも動かない。**
3. **gap は「あれば良いもの」ではなく要件だった**（基準 7）。**B10 の位置づけが上がる。**
4. **委員長（当時）・委員・理事が述べた「承認しない／受け入れる」規則は 5 件**（§1.67・**2026-09-21 に「委員会が」から狭めた**・#188）。**4 件は当たらないか
   一致する。1 件（*"OSI requires prior review by a lawyer"* ・Piana 氏）は B1 に不利で、
   B1 の欄に逐語で置いた。** **⚠ 2026-11-06 訂正: その 1 件は本人が同じ日に撤回している** —— *"I stand corrected re: Pam's message on requiring legal review, bad choice of words on my side."*（2024-12-18 18:29・`rounds/2024-12-18-license-review-piana-correction-observed.txt`）。**B1 に不利な 1 件として数えていたのは誤りだった。** **⚠ 2026-09-22 に根拠を差し替えた（#186）** ——旧文は
   「個人の資格だから軽い」と読んでいたが、process ページは *"Board members and employees of OSI
   may participate in license review **in their individual capacity**"* と定めており、
   **その断り書きは理事が参加するときの印である。Piana 氏は OSI 理事**（2025-06〜2026-06 の名簿 12 回）。
   **disposition は変わらない**が、支えるのは我々の推論ではなく公表規則 ——
   *"**no one person, including a Board member, has the authority to approve or reject a license**"*。
5. **結果の分布**（§1.68・§1.69・**同日に自己訂正した**）: 決議 11 件 + 告知で、**承認 4・否決 8**。
   **承認 4 件はいずれも既存テキストである**（MIT-CMU / Los Alamos BSD-3 Variant /
   OSC License v1 = MIT + ドイツ法対応 1 段落 / BSD-3-Clause-Open-MPI）——**新規の道具は 1 件も無い。**
   **我々の輪郭は否決側に一致する**（`against.md` #128）。
6. **否決の理由は 2 束** ——**条件・利用制限・差別**（§10.1 により構造上あたらない）と
   **起草の粗さ・解釈問題**（当たりうる唯一の束）。
7. **「重複」は承認の category である**（MIT-CMU は *"Redundant with More Popular"* として承認）——
   **#84「なぜもう一つ PD 等価を？」への、我々の推論ではない答え。**
8. **⚠ 上の全部に掛かる天井が 2 つある**（`against.md` #130）:
   *"Their consensus that a license does not ensure software freedom may … be the justification for
   rejecting a license **even where they cannot identify a specific aspect of the OSD or the approval
   guidelines … that is not met**"* と、*"**Approval of a license with the same or similar terms in
   the past does not bind the OSI**"*。**必要条件はいくら積んでも十分条件にならない。**

## 解消可能性の分類

`1` 文言修正 / `2` 条項削除 / `3` 条項縮小 / `4` 条項統合 / `5` 構造変更 /
`6` 名称・識別子変更 / `7` 提出方法変更 / `8` 法律家レビュー / `9` 外部証拠・第三者利用 /
`10` OSI 判断依存 / `11` 解消方法不明 / `12` 構造的に両立不能の可能性

**`11` と `12` を最優先で探索する。** 軽微な修正可能事項を大量に見つけても安心しない。
**1 件の構造的問題は 100 件の軽微 errata より重い。**

## 索引（2026-09-09 に現物と一次資料から再構築）

| ID | 問題 | 重大度 | 分類 | status | 人間 | 弁護士 | OSI |
|---|---|---|---|---|---|---|---|
| **B1** | 法的レビューが無い | **最高** | 8 | **提出の産物**（「待ち」ではない・§B1+B2）| ○ **2026-11-15（法律の論点で数えられる声）**: Unlicense の承認の議論で、Josh Berkus 氏 2020-05-13 は *"We're considering accepting the Unlicense on the basis that more than one attorney has said that they have no objections to it, and no attorney has objected. Despite the enthusiasm of your arguments, you are not an attorney, yet your arguments rest on legal grounds."* と書いた（`license-review`・`review-readings.md` §1.214）。**法律の論点で決める側が数えたのは法律家の声で、非法律家の法的な議論ではなかった。** ACD のドシエの法的な読み（`jurisdictions.md`・`QUESTIONS-FOR-COUNSEL.md` の「我々の読み」）は、この基準では数えられない側にある。**逆側**: 文は反対者の議論を退けた場面のもので、提出側に法律家が要るかは問われていない。Unlicense の承認の決め手が法律家の意見だったことは against #270 が既に持つ。 ○ **2026-11-15（審査者が最初に探すもの）**: Carlo Piana 氏 2024-09-05（ADVPL）*"I doubt a lawyer has laid their eyes on this text and I can't find any such indication"*、*"does not fully comply with the submission guidelines"*（`review-readings.md` §1.212）。同じ人は 3 か月後（2024-12-18）に、法律家のレビューを要件とした語を *"bad choice of words"* と撤回した（REVIEWERS の Legal review の行）。**撤回で規則の読みは正されたが、審査者が本文を読む前に法律家の目の形跡を探すという行動は残る。** ACD の提出文は「法律家は起草もレビューもしていない」と先に書いているので（`submission.md` §A.0）、探させる前に答えている。○ **2026-11-15（法律家と別の外部の読み手 2 種）**: 委員会は ML の条に **AI システムを作る実務家**の読みを求め、**英語を母語とする編集者**の通読も求めた —— Josh Berkus 氏 2025-02-25（`license-review`・ModelGo）*"we probably need some feedback from someone with that expertise"*、*"you should have an editor who is a native English speaker review them as there are many typos and grammatical issues."*（`review-readings.md` §1.210）。どちらも法律家のレビューとは別の項目で、依頼はオーナーの行為である（B14）。実務家への問いは `QUESTIONS-FOR-PRACTITIONERS.md` に用意した。**逆側**: ACD の本文は AI が英語で起草しており、誤字と文法の指摘が ModelGo ほど出る形ではないと読むが、母語話者が読んだ記録は無い。 ○ **2026-11-15（理事会）**: 2026-05 の委任の最初の行使で、委員会は 4 本を理事会の議決なしに却下し、4 本とも第 1 の理由は *"Poor drafting"*、2 本は *"argument without revision"* だった（2026-09-24 の議事録・`board-decisions.md` §4a）。**B1（法律家の関与が無い）と B3（長さ）は、理事会の議論を待たない却下の経路で効く。** 指摘に説明（`review-responses*.md`）だけを返し直した版を出さなければ、記録の上では却下された 2 本と同じ形になる。**逆側**: 4 本はどれも応答しないか直さなかった提出で、ACD は errata・試作・次版の草案という「直す」記録を公開で持つ。却下された形を避けることは我々の側で選べる。○ **2026-11-15（2 件目・不利な面）**: 2026 年の現役の参加者が、法律家を使わない起草を利用者への害と書いた —— Bruce Perens 氏 2026-01-23（`license-discuss`・Project Tick の草案）*"Failure to make use of an attorney is in general a harmful action to developer who use the license, since it would be prone to fail in unanticipated ways, making them incapable of enforcing their copyrights, and subject to various sorts of liability. Making the language suitable for acceptance is probably a year's work, with some expense, don't take it lightly."*（`review-readings.md` §1.205）。挙げた害のうち「著作権を行使できなくなる」は条件を持たない ACD には当たらず、「責任を負う」は当たる（against #41）。同じ草案はその後 `license-review` に出され、理事会は 2026-02-20 に *"ambiguities in drafting"* を理由に否決した（`board-decisions.md`）。2026-04-14 の再提出には委員長が *"a license of this complexity needs to be drafted by a professional"* と返した（against #291 が既に持つ）。**規則としては求めないが、複雑なライセンスには専門家の起草を求める**という形で、B1 は B3（長さ）と結び付いている。**逆側**: 宛先は GPL を写した互恵型の草案（約 7,800 語・portfolio-2f の数え）で、ACD はそれより短い。ただし「complexity」は語数だけでは測られない。○ **2026-11-15**: PPPL BSD-3 の提出者は本文に *"The license has not been through legal review."* と自分で書き（`license-review` 2025-07-09）、2025-07 と 2025-10 のスレッドで、この文を引用の外で論じた投稿は無かった（件名に PPPL を持つ投稿を *legal review / lawyer / counsel / attorney* で grep・2026-11-15・`~/osi-archive-cache`）。ただしこの提出は既存の LBNL の BSD-3 と名前だけが違うことが論点になり、理事会は既存の文を一般化する方を採った（Josh Berkus 氏 2025-10-22 *"That genericization update is happening soon, the Board just voted to authorize it."*）。**沈黙は「レビューが要らない」の証拠ではなく、別の理由で行き先が決まったことの記録である**（`review-readings.md` §1.203・portfolio-2f）。○ **2026-11-08**: UPL（2015）は社外の法律家も見たと書いた提出でも独立の審査を求められ、出された記録の無いまま承認された（`gap-measurements.md` §1.154）。Fontana 氏 2017 は法律家の関与を品質の印としにくいと述べた（`reviewer-positions.md` §1.156）。 **2026-11-23（`review-readings-6.md` §1.459・portfolio-d7・不利な面）**: 委員長の Russ Nelson 氏 2004-11-26（German Free Software License）*"You really should have a native English speaking lawyer review this license."*（`rounds/2004-11-license-discuss-gfsl-nelson-native-english-lawyer-observed.txt`）—— 英語を母語としない起草者に、英語を母語とする法律家のレビューを求めた。ACD の起草者は日本語を母語とし、法律家のレビューは無い。同じ向きで、Fontana 氏 2015-09-02（TOPPERS）は日本で書かれたライセンスに日本語の公式の版を尋ねた（ACD は英語だけで起草し、公式の訳を持たない（1.4 の §15.4）ので、答えは「無い」）。**逆側**: どちらも 1 人の審査者の勧めで、承認の要件として書かれた文ではない（Piana 氏の「法律家の事前レビュー」の文は 2024-12-18 に本人が撤回した・上の項目 4）。 **2026-11-23（`review-readings-6.md` §1.462・portfolio-d7・不利な面・重い）**: いまの審査者が、法律家のレビューを提出の要件と読んでいる。McCoy Smith 氏 2024-01-29（SADL・2025 年の通では理事として署名）*"I don't see any indication (which is a requirement of submission <https://opensource.org/licenses/review-process/> ) that this was reviewed by a lawyer"*、*"(and I don't think submitting it to the list in the hope that the lawyers on the list will do the legal review ought to count)"*（`rounds/2024-01-license-discuss-sadl-smith-legal-review-requirement-observed.txt`）。Carlo Piana 氏 2024-10-10（Berkeley Artistic License）も *"All in all the license does not seem to have been checked by a lawyer, nor that there is any mention of a legal review. Could you please clarify?"*。ACD は `license-discuss` に意見を求める形で出しており、Smith 氏の後半の文はその形に当たる。**逆側**: 手順の語は 2007 年 12 月に「法律家の分析を出す」から「受けたレビューを述べる」へ動き（`review-rules.md` §1.141）、2023 年からのページの語は *"Describe any legal review the license has been through"* である。Smith 氏が「要件」と呼んだのは、この開示の項目と読める。委員長の Chestek 氏は 2024-12-18 に *"we do not require review by a lawyer, only recommend it. That is not a blocker."* と書いた。**2026-11-25（委員長の講演・2026-11-24 掲載）**: McCoy Smith 氏は、AI の利用はいまのところ弁護士の代わりにならないと述べた（名指しではないが ACD の来歴に当たる・抜粋で未照合・#333・§1.488）。同じ講演の却下の主因 2 つ（定義に合わない・不明瞭な起草）は書き手でなく本文を見る。 **2026-11-26（§1.490・Chestek 氏 2025-10-26・委員・元委員長）**: 欠陥の多い提出に *"In my opinion, fixing all the problems with this license is not a task that a layperson can competently do without professional assistance."*、その前に *"I agree with McCoy that this license needs the input of a licensing professional before the OSI reviews it again."*、取り下げて *"whether this license is necessary at all"* から考え直し、法律家の助けを得るよう勧めた。ACD の来歴（モデルが起草・法律家の目なし）に、名指しではないが当たる。**逆側**: 1 つの提出への意見で規則ではない。勧めた理由は欠陥の多さ（同じ通の *"many small problems … in addition to the big ones"*）と、それを専門の助けなしに直せないことで、起草の道具（人か AI か）は理由に挙げていない —— ただし直す人に専門の助けが要るという向きは、法律家の目の無い ACD にそのまま当たる。 **2026-11-26（§1.491・2026-09-24 に却下された 4 本の審査・#335）**: Chestek 氏 2026-01-24 *"This license is a good example of why it is highly unlikely that a license not written by a lawyer can be approved."*、Perens 氏 2026-01-25（法律家を使わないと述べた提出者について読むのをやめた）、Piana 氏 2026-05-04（法律家の目が無いと読める本文）、Chestek 氏 2026-06-08（法律文書には起草の慣習と解釈の規則が在る）。**逆側**: 同じ人が 2024-12-18 に *"not a blocker"* と書き、4 本の却下の理由は起草の質と応答の形（応答なし・直さず反論）で、法律家の不在ではない。 **2026-11-26（§1.494）**: いまの委員長 McCoy Smith 氏は、委員長として 2026-03-17 に手順ページの項目 *"Describe any legal review the license has been through, including whether it was drafted by a lawyer."* を引き、提出者に法律家が関わったかを書けと求めた。委員長になる前の 2025-12-22 には、起草の誤りを見た提出へ *"I think any future submission would need to indicate a legal review has been done, and by whom, in view of this."* と書いた —— 求めたのは「レビューが**済んだ**こと」を示すことで、ACD は示せない（開示で「無い」と答えることは、この文が望む答えではない）。Piana 氏（理事）2026-03-18 は審査者の時間を使う前に competent lawyer を勧め、Chestek 氏（当時の委員長）2024-10-05 は承認の見込みを熟練した法律家の仕事に結びつけた。起草の欠陥を errata として公開していること（件数は errata の冒頭）は、2025-12 の文の引き金（起草の誤りを見た後）に当たりうる —— 多くは 1.4 の草案までに閉じ、1.4 に残るのは E87〜E95 ほかで多くは Low だが、審査者はそれを法律家の目が無いことの表れとも、欠陥を隠さない運用とも読める（§1.494 の読みと同じ）。**逆側**: どれも個別の提出への文で、2025-12 の文は *"I think"* と *"in view of this"*（その提出の誤りを見た後）に限られ、規則として要件にした文は見つからない。2026-03-17 が求めたのは項目を書くことで、ACD は書いている。**残る作業**: いまの review-process のページの語を取り直す（2026-11-23 にこのセッションから取ろうとして権限で拒否された。外部の取得は Mac の組が行う）。 **2026-11-27（Smith 氏 2025-10-02（`license-discuss`・PUWL の起草者への返事・のちの委員長・#336・§1.495））**: gap を認めた同じ返事で *"I wouldn't counsel you try to do this yourself. It's something I think that CC should do (CC0-2.0?)"* —— 個人の起草を勧めない。**逆側**: 当時は委員長でなく、起草者への個人の返事で規則ではない。 | ○ | — |
| **B2** | 実使用が 1 リポジトリのみ | **最高** | 9 | 解消可能・未実施（discoverability のみ制御可）。**2026-11-15: 「使用は承認の基準ではない」は、決める側の 3 つの独立の文に支えられる** —— 委員長の Richard Fontana 氏 2015-10-13 の委員会報告 *"OSI has approved thought-experiment licenses before (e.g. the SimPL) as well as licenses that were not used prior to OSI approval (e.g. the UPL)."*（推薦は *"Approval, or else OSI to adopt some formal maturity/real-world-use factor"* で、理事会は翌日 8 対 0 で承認し、使用の要素を採らなかった）、MIT-0（2020）と Jam（2021）の理由書（portfolio-2f の依頼 (3) の答え）。**逆側**: 当時の会長 Michael Tiemann 氏 2007-07-05 *"is there a body of code now covered by the licenses? Although it's a bit of chicken-and-egg, sometimes it's nice to have some code that will become "open source" when a license is approved, rather than just another entry in a too-long list"*（GPLv3 の提出時）—— 基準ではないが、望ましいとされてきた。 **2026-11-15: 決める側の 1 人は、採用されない新しいライセンスを承認の費用として数えている** —— Bruce Perens 氏 2024-03-15（`license-discuss`）は、法律家 3 人が書いた Blue Oak（2019 承認）について *"its main effect was to increase the number of OSI-approved licenses and the combinatorial problem"*、*"This is something that I think OSI should keep in mind regarding the license approval process. Even the submitters we could grade as most competent have licenses fall flat"* と書いた（`review-readings.md` §1.217・portfolio-2f）。「採用は承認の基準ではない」（MIT-0 / Jam の理由書）という有利な面と食い違う、委員の考えとして置く。**逆側**: Blue Oak は承認済みと同じ効果を別の文で書いたもので、ACD は既存に無い効果（B10 の G1）を主張する。ただし差が読まれなければ同じ型に見え、B10 の H1-g（既存＋追加の許諾で G1 も作れる）はその差を小さくする。 **2026-11-11: 承認の後にも B2 の費用は形を変えて残る** —— 利用者の組織は承認済みのライセンスでもパッケージごとに審査し（Tzeng 氏 2015）、財団は受け入れの一覧を自分の決定とした（Radcliffe 氏 2015）（`review-readings.md` §1.181・#322）。採用の主な入口であるライセンス選択サイト（choosealicense.com）は献呈の型（Unlicense・CC0・0BSD・MIT-0）を載せ、ACD は無い（WebFetch の要約・§1.185）。Chestek 氏 2013 *"find another obscure license that does what they want but is obscure for a reason"*（#289 の追記）。**逆側**: 承認は受け入れの床で（Fontana 氏 2014 *"minimum standards of acceptability"*）、献呈の型は ASF の一覧と選択サイトの両方に既に在る。**2026-11-09: MirOS（2008）は、提出者が「大きいプロジェクト 1 つと小さいもの 2〜3」と書いた利用で、理事の *"only used in code copyrighted by you"* という問いを受けたまま、2 か月後に承認された（承認日 2008-09-10・`review-readings.md` §1.167）。逆側: MirOS の利用は ACD の 1 件より多く、2025 年の理事会の文より 17 年前の運用である。****2026-09-13 追記: 帰結は否決ではなく「承認しないまま留め置かれる」**（理事会 2025-07-18・#84 と連言）。**2026-11-04 確認**: GitHub のコード検索（*"Autonomous Commons Dedication"*・上限 100 件）で現れるリポジトリは本リポジトリ 1 つだけ（45 ファイル）—— **独立した第三者の採用は公開情報で確認できない**（検索が見るのは GitHub が索引した範囲だけ）| — **2026-11-08**: 利用を承認の理由に挙げた記録が増えた —— UPL を承認した理事会の議事録（2015-02-04）は *"Oracle intends to release software soon"* を挙げ、審査では Berkus 氏が提出者の利用の予定を、Villa 氏が anchor tenant を求めた（#312）。Blue Oak は 5 年の使用の後に出された（`reviewer-positions.md` §1.158）。逆側: Fontana 氏 2014 は利用の予定の無い提出を退けないと述べ、Villa 氏 2017 の案は OSD を満たせば承認して目立つ一覧に載せない形だった（#315・§1.156）。 **2026-11-23（`review-readings-6.md` §1.462・portfolio-d7）**: Piana 氏 2025-05-28（Tiwaz License）*"I am personally not impressed by the idea that someone offers a new license not for using it as copyright holder, but just to offer a new variant or license in case some projects wanted and have been advised to adopt it. Until there is some appetite by actual projects, submitting it appears to be nothing but an intellectual exercise, not meeting the bar for eliciting the attention of OSI and approve it."*（`rounds/2025-05-license-review-tiwaz-piana-intellectual-exercise-observed.txt`）。**有利な面**: ACD はオーナーが著作権者として自分の著作物（このリポジトリ）に適用して使っており、前半の「著作権者として使わずに出す」には当たらない。**不利な面**: 後半の「実際のプロジェクトの関心」は 1 件で、B2 そのものに当たる。 **2026-11-23（`review-readings-6.md` §1.464・portfolio-d7・不利な面・重い）**: 委員の Josh Berkus 氏 2017-10-24 は、新しいライセンスを量る基準の 4 つ目に *"Has a substantiated use case"* を挙げ、同じ週に別の提出者へ *"can you explain what the first project you have in mind for this license is?"*、理由として *"this committee doesn't want to approve a license with no confirmed users."* と書いた。**逆側**: ACD の最初のプロジェクトはこのリポジトリで、オーナーが著作権者として使っている。MIT-0 の理由書は *"the OSI has historically approved newly drafted licenses not yet in use"* と書き、FPL（いまの 0BSD）は使用の無いまま 8 対 0 で承認された（`board-decisions.md` §8.6）。 **2026-11-26（§1.490）**: Chestek 氏 2025-10-26 は欠陥の多い提出への最初の点に、提出の案内の採用の項を引いて *"Is this license in use? If not, who is your intended user?"* と問うた。**逆側**: 問いであって却下の理由ではなく、同じ通は *"whether this license is necessary at all"*（B10）を結びで問う。 **2026-11-27（#336・§1.495）**: のちの委員長は gap の作り手に Creative Commons を挙げた（Smith 氏 2025-10-02）—— 背後に大きな作り手が居る形を良しとする読みで、作り手が起草者 1 人の ACD に不利。**逆側**: 個人の返事で規則ではなく、*"(CC0-2.0?)"* は疑問の形。 | — | ○ |
| **B3** | 長さ 4,896 語 / 16 節 82 項（**確定した ACD-1.4 は題名から 5,879 語で GPL-3.0 より 235 語長く、条文では 925 語長い**）| **高** | 3 / 4 | **2026-11-11: 出す版の 1.4 草案は 5,658 語（題名から）・5,320 語（第 1 条から）で、GPL-3.0（5,644・4,617）より長い。1.0 で答えにしていた「GPLv3 より短い」は提出する版に当てはまらない（portfolio-aa の測定・#6）。** **2026-11-12: T54 が §8.4 の理由の文（105 語）を外し、題名からは 5,553 語で GPL-3.0（5,644）より 91 語短くなった。条文では、第 1 条から *END OF TERMS* の手前までが 5,212 語で、同じ数え方の GPL-3.0（4,617）より 595 語長い（`SUBMISSION-MATERIALS.md` §2 の長さの行）。上の 11-11 の 5,320 は *END OF TERMS* の行を含めた数え方で、それにそろえると 5,215。題名からの数が下回ったのは、§8.4 の理由の文が許諾を狭く読む分岐を生む欠陥（errata E78）を閉じた結果で、閾値のために削ったのではない。条文の数では「GPLv3 より短い」は当てはまらないままである。** **同日、T56 が §8.6 の *alongside them*（2 語）を外し、題名から 5,551 語・第 1 条から 5,210 語（同じ数え方）になった。T57〜T59（長い文を分け、§2.8 を限りに結ぶ）で +1 語、題名から 5,552 語・第 1 条から 5,211 語。T60（§5.2 末文の it を名指し）で +3 語、題名から 5,555 語・第 1 条から 5,214 語。2026-11-15 の T61（§5.2(b) の it を名指し）と T62（§16.4 を Steward が出した新しい版に及ぼす・errata E80）で +18 語、題名から 5,573 語・第 1 条から 5,232 語。GPL-3.0 より題名からは 71 語短く、条文では 615 語長い。同日の T64（§5.2(a) の *apply, or* を外す・errata E82）で −2 語、題名から 5,571 語・第 1 条から 5,230 語。T65（§2.2 の後付けの制限を配った写しで何をするかに掛ける）で +3 語、題名から 5,574 語・第 1 条から 5,233 語。** **縮められるが答えきれない**（実測 306 語・機構部を削っても 3,888 語に届かない）。**2026-11-07: CC0 の審査で、放棄と許諾と特許を持つ道具は *"a 10-15 line"* の短さで求められていた**（Evans 氏 2012・§1.138）。**2026-09-20 追記: この bottleneck が実際に決定を生んだ例が出た** ——2017 秋の理事会は NOSA 2.0 について *"in view of the length, complexity, and ambiguities … conformance … cannot be assured"* として**承認も却下もしない**決議を採った（#183）。2026-11-04: 1.4 草案で読みの分岐を 4 件減らしたが結論は不変（下の B3 節） **2026-11-26（§1.490・Chestek 氏 2025-10-26）**: *"You have many sections that are unnecessary, circular, or redundant."* と、許諾を 4 つの節に割った提出に *"I don't understand why the copyright grant is broken up into four sections"*。ACD-1.4 は「判定しなくてよい」を §4.4・§8.6・§12.2 で繰り返す（§1.481 の型・当たる）。許しの文は §4 のほかに §6.1（Computational Use）と §7.2（データベース）に在り、同じ型と読まれうる —— ただし §3・§4・§5 は放棄・許諾・約束の別の働きで、§6.1 と §7.2 は *"so far as the Covered Rights …"* と §4 の範囲の中で述べる説明なので、許諾の範囲は割れていない（1.5 の草案は Covered Rights の許諾を 2.2 に集めた）。 **2026-11-26（§1.491・2026-09-24 の 4 本の審査の指摘の型）**: 許諾の欠け・名の書き込み・受け手の範囲・許諾の節の崩れは 1.4 に当たらない。当たるのは Low の 4 型 —— 改変物の語が 2 通り（errata E94）、*made available* が誰に向けた提供かを言わない（台帳）、見出しと番号（§2 に寄与の条・§5.2 の番号の無い段落）、モデル・出力の列挙の繰り返し（E47 の隣・1.4 では語は揃っていて 3 か所で繰り返すだけ。1.5 は Result の定義 1 か所にまとめた）。**逆側**: 型を当てたのは我々で、審査者が同じ数え方をする保証は無い。| — | — | — |
| **B4** | §3 献呈と §4 許諾の並存 | **高** | 10 | **OSI 判断依存**（12 候補として検証し否定）。**2026-11-15（有利な面）**: Unlicense の承認の議論で、Pamela Chestek 氏 2020-05-17 は撤回の危険を他のライセンスと量的に違わないと見て、*"Here we have a very clear statement from the copyright owner that they have no intention of exercising copyright rights in the work."*、*"this clear statement would be a pretty high hurdle to get over"* と書いた（§1.214）。権利を行使しない意思の明確さが撤回の危険への答えとされた。ACD は同じ意思を §2.2（撤回不能）・§3（放棄）・§4（独立の許諾）・§10.4（終了しない）で Unlicense より多くの語で述べる。**逆側**: Chestek 氏の読みは、米国法で放棄として扱われることを前提にした段（*"Assuming this would be treated as an abandonment under US law"*）で、法域を超えた答えではない。語が多いことは B3 と引き換えでもある。 **2026-11-07: CC0 の審査本体を読んだ。2012 年の意向調査は 13 対 8 で反対だったが、−1 の 13 人は全員が特許を理由に含め、構造を理由にした人はいない**（`review-precedents.md` §1.138）。**⚠ 同じ審査に、特許の許諾を公有化の宣言に結びつける形そのものへの反対が 1 人ある（#288）。****2026-11-11 追記: 提出の前の議論（2012-01）には構造への留保が在った** —— Cowan 氏は放棄と許諾の組み合わせを 1 つのライセンスと読み、Fontana 氏は一体の文書は全体を審査するか、しないかだと述べ（どちらも審査を退けていない）、Glaser 氏は放棄の部分を著作権のライセンスとして認証しない立場だった（`review-readings.md` §1.184）。意向調査の記録は動かない。**2026-11-07: OSI のサイトの記事（2017）が、放棄と許諾の 2 部構成を *"A solution would be"* と述べていた**（`board-decisions.md` §2f。決定ではない）。**2026-11-06 追記: OSI の FAQ が、公有化は *"still not a license"* で審査の対象にならないと述べ、§4 が要る理由は OSI の文で言える。同じ FAQ の *"rather than try to waive copyright altogether"* は §3 に当たる**。**2026-09-20 追記: 献呈だけの instrument が「著者は自分で献呈できる」という理由で却下された実例（WTFPL・2009-03-04）が理事会記録に在り、同じ 4 行に「ヨーロッパに public domain は無い」という §4 の存在理由も並んでいる**（#182） **2026-11-23（`review-readings-6.md` §1.459・portfolio-d7）**: WTFPL の不承認の後、委員長の Nelson 氏 2009-03-19 はライセンスにできることを 3 つ挙げた（保証の否認・商標の使用を認めないこと・条項を一定に保たせること）。ACD-1.4 は前の 2 つを持つ（§13・§11.1）。3 つ目にあたる §16.4 は、名を変えた改変を許す点で WTFPL と同じ型である。一方で、名と識別子の族の側は WTFPL より強く固定している（*"continues to denote one fixed text"*）。3 つ目が「同じ名の条項が変わらないこと」を指すなら、ACD は満たす側に在る。「受け手に条項を保たせること」を指すなら、§10.2 があるので持たない。原文からはどちらとも決まらない（`board-decisions.md` §8.1）。予備の許諾（§4）の理由の側には 3 つの文が在る: Lawrence Rosen 氏 2001-01-23（当時 OSI の法律顧問）*"So software that is "public domain" (to use your term) is not certifiable."*（認証の対象は許諾の下で配られるもので、献呈ではない）、Michlmayr 氏 2009-03-16（パブリックドメインに置けない欧州では、同じ効果のライセンスが要る）、Rosen 氏 2016-07-22（米国で公有の著作にも、外国のためにライセンスを重ねよ）。**逆側**: Nelson 氏の同じ通の *"This license does nothing to protect the licensor, and gives the licensees all permissions."* は ACD にもそのまま当たる（§10.1）。Rosen 氏 2016 が勧めたのは既存の Apache 2.0 で、新しいライセンスではない（B10）。献呈の部分が OSI の評価の外に在る、とも読める。| — | — | ○ |
| **B5** | §4.4 の法的説明の正確性 | 中 | 1 / 5 | **起草は閉じ、設計の問いだけ外部**（E11 は 2026-09-14 に 1.1 で閉じた —— 過大な 1 文を削除し 1.1 / 1.2 草案に 0 件。steward が自ら出した問いの設計側（読み A）は未回答・1.0 には文が残る。**2026-09-28 訂正**）| — | — | ○ |
| **B6** | 名称 "Autonomous Commons Dedication" | 中 | 6 | **決定済み（2026-10-24）: 改名しない**（測定: 識別子は空き・"Commons" 58/58 が CC・ODC / "Dedication" は半分しか言っていない。理由と逆側は §B6）| — **2026-11-08**: 1.4 草案は §16.4 の名前の保護を「名前を含む名前」にも及ぼした（errata E76・T44）。「1 つの名前が 1 つの本文を指す」という改名しない判断の前提が、語で守られる。 | — | — |
| **B7** | §8.4 の特許射程が uptake を下げる | 中 | 3 | **B10 との一方向の取引**（緩和策 2 つは構造上ふさがっている）。**2026-11-06**: 1.4 草案は §5.1 と §8.3 が §8.4 の限定を素通りする読みを閉じ、費用を限定の内へ戻した。費用の一覧は `gap-measurements.md` §1.136 **2026-11-08**: 広さが承認を止めた記録は無い —— UPL（2015）と Blue Oak（2024）は広い特許許諾のまま承認され、Piana 氏 2023 は特許を持つ側が結果を理解すればよいと述べた。費用は採用の側に出る: 学術医療機関は Apache-2.0 すら避け（2024・#311）、寄与者への警告が 2014 年と 2023 年に出ている（#313）。 **2026-11-24（`review-readings-7.md` §1.486・6c）**: 後から足された特徴について、決める側は 2 つの端を拒んできた —— 改変した瞬間に許諾が消える形（Chestek 氏 2025-09-19 *"the moment a change is made to the software"*・Piana 氏 2025-09-22）と、改変に関わらず白紙の形（Berkus 氏 2019-12-06）。ACD-1.4 §8.4 の *"Section 8.1 alone governs a feature added to the Work, by whatever means."* はその間に在る。1.5 の草案（n8・2.3(b)）はこの文を替えた —— Work の中身から *学ばれた*（単独または他の素材と合わせて）か *抜き出された* か、Work が教え具える特徴に届き、Work と他の素材から学んだ特徴を fork に足す場面と、Work の教えることと他の文の教えることを組み合わせた特徴では 1.4 より広く（Berkus 氏の端へ寄る）、一部だけ因果の特徴と、評価・選択だけに使った場合では狭い（`CHANGES-ACD-1.5.txt` の 6・承知で受け入れた・議題 24・32）。**逆側**: Berkus 氏 2014-04-15 は、改変する人が許諾に入るかを知れなければ許諾の意味が無いと書いた —— 学習したモデルの因果の基準は、広いか狭いかとは別に、改変する人が判じにくい。 **2026-11-25（§1.484・§1.485・6c）**: 決める側が射程を量った語は *embodied* が主で（Rosen 氏 2002・2016、Berkus 氏 2016）、広い許諾への不利な文が在る —— Perens 氏 2025-11-12 *"in use of the licensed copyrighted property, and no more"*（必然的に侵害する請求項まで、の意）、Smith 氏 2018-09-26 *"with no boundaries as to scope"*（C-FSL）。ACD-1.4 §8.4 の *"results, in whole or in part, from the content of the Work"* はその主の語より広く、承認済みの条に同じ語は見つからない。**逆側**: Chestek 氏 2025-03-13 は未改変の版の利用者をどの理論でも訴えさせないことを最低線とし、因果の語は承認済みの BSD+Patent に組合せについて在る。 **2026-11-26（§1.490・Chestek 氏 2025-10-26）**: 寄与者の特許許諾が Licensor より狭く派生物に届かない提出に、*"The lack of necessary scope in the Contributor patent grant, in my opinion, makes this a non-free license."*。ACD の寄与者は寄与について Dedicator になり、§8.1 は *"the Work or anything derived from it"* に届くので、型はそろう（有利）。**逆側**: §8.1 は *"caused by subject matter contained in the Work"* に限り、寄与者の Work が寄与だけだと読めば、寄与と元の Work の組み合わせで初めて侵害する請求項は外と読まれうる（Apache-2.0 は *"by combination of their Contribution(s) with the Work"* と名指す。1.5 の草案 2.3(a) が組み合わせを名指して閉じる。errata E95 として 2026-11-26 に記録）。 | — | — | ○ |
| **B8** | §12 人格権（licensable でない / mission creep）| 中 | 3 / 4 / 8 | **分岐を記録済み**（同じ条項が gap とも creep とも呼ばれている）| — | ○ | — |
| **B9** | §7 データベース権の必要性 | 低 | 2 | **検証済み・保持**（§7.2 は行為の語で独立に働く）| — | — | — |
| **B10** | **新規ライセンスを承認するだけの gap が残っているか** | **最高** | 10 | **2026-11-15（§9・有利な面）**: 理事の Josh Berkus 氏 2026-03-13/15（AI-MIT）は、AI 生成か否かをプロジェクト全体で 1 度述べる形では部分を写す人がどの権利が当たるか分からない、と書いた（*"if you want to copy a single module from this project, you don't know what copyright applies."*・§1.212）。ACD-1.4 の §9.3 は *"You are not required to determine which parts of the Work are Machine-Generated Material"* で、許諾がその問いに依らないので、この問いを生まない。§9 は G1〜G4 の独自 gap の根拠にしていない（宣言であって付与ではない）が、決める側が問うた形の空白を持たないことは言える。 **2026-11-15: 審査の側は gap の問いを「既存の承認済みライセンスに追加の許諾・例外・ガイダンスを足しても同じことができない理由」の形で、提出の前に求めている** —— Shuji Sado 氏 2026-01-24（`license-review`・Project Tick v2 への返信）*"Before a full OSD review, it would help to provide either a redline against GPLv3/AGPLv3 or a short "innovations only" excerpt, along with a brief explanation of why existing OSI-approved licenses plus additional permissions/exceptions or guidance cannot achieve the same goals."*（`review-readings.md` §1.205）。ACD の提出物はこの形の答えを持たない（`SUBMISSION-MATERIALS.md`・`submission.md`・`REVIEWERS.md` を *innovation / redline / additional permission* で grep して 0 件・against #325）。**この形で当て直すと、2026-11-04 に立証した唯一の差 G1（§8.4）も「既存＋追加の許諾」では作れる**（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` B10 の H1-g）。書ける答えは先例（BSD-2-Clause-Patent は「BSD-2＋特許許諾」を 1 本で出して承認された・#235）と識別子の費用（例外も SPDX 登録が要る）で、「付け足しでは作れない」は書けない。**逆側**: 宛先は GPL を写した互恵型の草案で、「既存＋例外」は GPL の linking exception の型を念頭に置いた問いである。許容型の土台（0BSD）に特許の許諾を例外として足す形が実務で通るかは別の問いになる。 **2026-11-15: 重複の基準は「名前のほかに違いが在るか」で、識別子を増やす費用は違いが在っても掛かる** —— Carlo Piana 氏 2025-07-18（`license-review`・PPPL BSD-3）*"giving it a different name when it's actually the same license, creates unnecessary friction, clogs the namespace and creates a lot of issues in automated license compatibility resolution, especially if it's given a separate SPDX identifier."*（`review-readings.md` §1.203）。ACD は名前のほかの違い（特許・ML・機械の著作）を示せるので、この文の主たる対象ではない。**逆側**: 文の後半（名前空間と自動の互換判定の費用）は違いが在っても新しい識別子に掛かる費用で、B11 と同じ側にある。違いを示すだけでは払えない。 **2026-11-11: ACD と同じ型（公有化の献呈と、帰属を求めない許容型の fallback）は 2012 年と 2015 年に list に出ていて、どちらも既存の許容型で足りると答えられた** —— Rick Moen 氏 2012-02-02 *"What practical problem do you consider this licence (in truth, a professed public domain declaration with a failsafe fallback to a simple permissive licence) to solve that is not already solved by MIT License or Fair License?"*（同じ日に OSD への適合は認めた・`review-readings.md` §1.184）、Mark Radcliffe 氏 2015-10-21 *"I think that we have more than enough licenses with these characteristics."*（0BSD の承認の 1 週間後・`gap-measurements.md` §1.146 の追記・#314）。帰属の無さと献呈の型は gap にならず、ACD の差は下の特許の側でしか言えない、という B10 の線と同じ向きである。**逆側**: どちらも特許の許諾を持たない文への答えで、ACD の特許の差には当たっていない。 **2026-11-09: 2008 年の委員長は MirOS を *"Yet Another academic license of limited difference and limited value"* と書き、提出者が既存のライセンスへの移行を断ったうえで、OSD 適合を理由に *"Recommend: approval"* とした。理事会は報告を受け入れ、承認されたが推奨はされなかった（`review-readings.md` §1.167・#302 の逆側）。同じ委員長は同じ年に、MIT/X11 に近い別のライセンスに類似を理由とする却下を勧めており、線は記録に無い。** **2026-11-07: Fedora は 2022 年に CC0 をコードから外し、公有化の形は外していない。代わりに勧められた MIT-0 は特許に触れない（`gap-measurements.md` §1.139・#290）。** **OSI 判断依存**（2026-11-04: 既存の承認済み 141 本では達成できない効果を**少なくとも 1 件、原典の条文で立証** —— §8.4 + §8.2「作品を超える対象への特許許諾 ∧ 条件も終了も無い」を同時に持つものは 0 本。**gap が承認に足りるかは依然 OSI の判断**・EXTERNAL の B10 節。**同日後半の再検証: 条文比較で立つのは「明示の特許許諾 ∧ 無条件 = OSI の全テキストで 0 本」で、モデルの販売への届き方は §8.4 末文の読みに依存する** —— `ACD-1.0.gap-measurements.md` §1.133。**2026-11-06**: 行為の類型で当て直し、差が立つのはモデルの販売と出力の利用だと絞った（§1.135）。最強の反論は受益者の少なさ（#284・§1.136）） **2026-11-27（Smith 氏 2025-10-02（`license-discuss`・PUWL の起草者への返事・のちの委員長・#336・§1.495））**: *"I've always thought there was room for a CC-0 less the disclaimer of patent rights."* —— ACD の gap（献呈型で特許を留保しない形）を、決める側の人が自分から名指した。**逆側**: 同じ返事の次の文で個人の起草を勧めず、作り手に CC を挙げた（B1・B2・B12）。個人の返事で規則ではない。 | — | — | ○ |
| **B11** | SPDX 未登録 / REUSE 命名（#108）| 低 | 承認で消える | **意図的に未実施**（所在を動かさない・#106 は承認後も残る）。**2026-11-07: SPDX の基準は 2026-10-27 に書き直された。*"only by the license drafter"* は実使用に数えず、OSI 承認と Fedora / Debian の受け入れが審査なしの経路である（#296）** **2026-11-26**: ClearlyDefined（オープンソースの compliance 用のライセンス情報の集約）は、LicenseRef の識別子も扱い、OSI 承認のライセンスに限らないと述べた（OSI のブログ・2026-11-26 掲載の講演・逐語は未照合）。`LicenseRef-ACD-1.4` を書いた採用者のメタデータは、SPDX の一覧に無くても道具に乗りうる。**逆側**: 道具に乗ることは採用でも承認でもなく、SPDX の一覧に載る条件（相当の使用）は変わらない。話者は OSI の決める側ではない。| — | — | ○ |
| **B12** | steward が 1 人 / 承継 | 低 | 9 | **リストが恐れたのは支配で、ACD に upgrade 条項は無い。承継先は未定**（2026-11-07 に 11 から移した）| ○ **2026-11-15**: 1.0〜1.3 のまま役割を譲渡すると、新しい Steward が出した版を第三者が配ることは、旧版の §16.4 の語では「Steward による」配布に当たらない（旧版の本文の著作権は譲渡人に残る・errata E80）。1.4 草案は例外で出た版に §16.4 をそのまま及ぼす文で閉じた（T62）。承継の線を定めるだけでは足りず、**譲渡の後に誰が何を配れるか**まで本文が答える必要があった。**逆側**: 役割の譲渡は一度も起きておらず、1 人が全版の権利を持つ限り各版の §16.4 が救う。○ **2026-11-08**: 1.4 草案の §16.5 は、譲渡の後の Steward を最後に譲り受けた者に限る（T45）。継承の線が 1 本に定まり、1 回の譲渡で複数の者を共同の Steward にすることもできる（§15.5）。Steward が譲渡しないまま死亡・解散した場合は、本文は答えない。 **2026-11-23（`review-readings-6.md` §1.468・portfolio-d7・有利な面）**: or-later を持たないことは、決める側が問題にしてきた形の外に在る —— 移行の強制（Nelson 氏 2004）、更新が要件を足すこと（Perens 氏 2008）、正式な版を決める権威が要ること（Berkus 氏 2024）。逆側と詳細は against #11。 **2026-11-27（#336・§1.495・3f）**: のちの委員長が gap の作り手に Creative Commons を挙げたこと（Smith 氏 2025-10-02）は、新しい小さな steward より既存の大きな steward を良しとする読みになり、B12 に不利に効く。**逆側**: 個人の返事で、steward の数を論じた文ではない。 | — | — |
| **B13** | reviewer の理解コスト | 高 | 1 / 3 | **継続対象**（B3 の結論により、長さへの唯一の実効的緩和）。**2026-11-15: 語の精確さは、審査で量られる品質である** —— Carlo Piana 氏 2025-12-10（CingXaero）*"use of appropriate and precise wording is a quality issue that can be taken into account"*（§1.212）。2026-09-24 の却下 4 本の第 1 の理由が *"Poor drafting"* だったこと（B1・`board-decisions.md` §4a）と同じ向きの文で、理解の費用は語数だけでなく語の精確さでも量られる。**逆側**: ACD の試作の記録（SECOND-CLARITY-TRIAL）は、精確さのために語を足した変更が多く、B3（長さ）と引き換えになっている。**2026-11-15: 審査者が新しい草案を読む初期値は「また同じ誤解」である** —— Bruce Perens 氏 2025-12-03（`license-discuss`・TRPL のスレッド）*"We get approached with essentially the same misconceptions, behind different drafts, about once a month."*（`review-readings.md` §1.202）。理解の費用は ACD の語数だけで決まらず、最初の段落で「よくある誤解の型ではない」と示せるかにも掛かる。同じ人は 2026-01-21 に別の草案へ *"you have not shown what language achieves those goals and how it is different from existing licenses like GPL. You should do that in detail, because this thing is big enough that I don't want to spend hours decoding it and differentiating it from GPL"* と書いた（§1.205）—— 理解の費用を下げる手段は、既存との差を条ごとに示す文書である（ACD では `comparison.md`）。**逆側**: 同じ文の前半で Perens 氏は *"including, but not limited to"* を自分も必ず使うと述べており、慎重な語を足す起草を退けてはいない。また TRPL は互恵型の草案で、ACD の型（献呈と許容型の許諾）への言葉ではない。 **2026-11-27（§1.497・準拠法と法域の条）**: Piana 氏 2025-02-20（MGB 1.0 への返事）は *"these licenses must be designed to work under any relevant jurisdiction"* と書き、続けて *"Nitpicking that under a particular jurisdiction the language would be equivalent or work the same way is not necessarily a good defense of the license."* と述べた。**入口の書き方への意味**: ドシエの法域ごとの答え（`ACD-1.0.jurisdictions.md` の日本・ドイツ・フランス）を「この法域でも同じに働く」という防御として前に出すと、この文の言う弱い防御に当たる。前に出すのは「どの法域でも働き、どこで効くかを利用者が判断しなくてよい」形（1.4 の §4.4・§12.2）で、法域ごとの読みは問われたときの材料に留める。**逆側**: 他の提出（MGB 1.0）への返事で、ACD についての文ではない。準拠法の条を持たないこと自体は、Chestek 氏 2025-02-14（当時の委員長）と Piana 氏 2024-10-15（私人として）の文が有利に支える。| — | — | — |
| **B14** | **AI 起草の投稿は拒否すると両リストの moderator が宣言した（2026-09-09）** | **最高** | 新設 | **規制判断は OSI（組織）**（AI には解けない）。**2026-11-15: 審査で問われたときに答えるのも、書いた本人であるべきとされている** —— 当時の委員長の Pamela Chestek 氏 2020-02-28（`license-discuss`）*"the people who wrote the license are ideally the ones explaining it to the license-review list because they know the ins and outs. We've had proxies participate in the past and it doesn't go well."*（`review-readings-2.md` §1.221・portfolio-2f）。B14 の線（送る文はオーナーが自分の言葉で書く）は投稿の文面についてだったが、この文は**審査の問いへの答え**まで同じ人に求める。AI が答えを書いてオーナーが送れば、審査の側からは代理人の形に見えうる。ACD の本文は AI が起草したので「書いた本人」が誰かという問い自体が立つ（B14 と B1 の結び目）。**逆側**: 同じ文は「書いた本人」を理想として述べ、要件にはしていない。ACD ではオーナーが起草を依頼し、条文の採否の記録（試作・反例・CHANGELIST）は公開で、答えの材料はオーナーが読める形で在る。 **2026-11-11: 本文を AI が書いたこと自体は、委員会の 3 人が 2026-03 に問題にしないと答えていた** —— Chestek 氏 *"Why does that matter to how the license operates?"*、Fontana 氏 *"I'm not sure the possibility that any part of this license is AI-generated matters though."*、Berkus 氏 *"There is no requirement that the license be copyrightable."*（AI-MIT の審査・`review-responses-meta.md` Q36）。B14 の moderator の宣言は投稿の文面についてで、本文の起草についてではない。**2026-11-15: 委員長自身が AI で作った比較を `license-review` に出していた** —— Pamela Chestek 氏 2026-04-11（Project Tick v2）*"Here is an AI-generated comparison to the AGPLv3 that might be helpful."*（`review-readings.md` §1.206・portfolio-2f）。審査の側は AI の出力を審査の道具として使い、そうと名乗って出している。**逆側**: これは審査者の道具であって提出者の投稿ではなく、moderator の宣言（提出者と参加者の投稿の文面）を変えない。我々に効くのは「AI を使ったことを名乗る」形が審査の側でも普通だという点だけである。逆側: 起草したモデルの会社と利害の関係は残る（#319）。**2026-09-28 訂正（旧文「オーナーは Nick 氏個人とリスト外で対応中」は 09-10 時点の現在形のまま残っていた）**: 発信は 2026-09-17 に再開（状態の単一ソースは `FROZEN.md` の `POSTING-STATUS`）、**少なくとも 3 通が moderation で拒否**（#136 / #215 / #222）、リスト外の往復は `rounds/` に 09-07 / 09-13 / 09-15 / 09-17〜18 の記録がある（本文は撤回済みの stub・#217）。**それ以後の状態は我々からは分からない** ——「対応中」とも「終わった」とも書かない | ○ | — | ○ |
| **B15** | **主題適格 —— §1.2 の列挙が、2023 年に理事会が不承認とした当の理由に触れている** | **高** | 10 | **OSI 判断依存**。**2026-11-15: 2026 年の現役の委員が、ソフトウェアでないものに及ぶライセンスを「ソフトウェアなら受け入れられるか」だけで量らないと書いた** —— Carlo Piana 氏 2026-08-31（`license-review`・OpenMDW・暫定の立場と明記）*"we cannot just simply apply the "would this be acceptable for software" test."*、*"I am really wary of porting the same reasoning we apply to software to an entirely new and broader category of artifacts."*（`review-readings.md` §1.211）。2021 年の基準（ソフトウェアに使える形で書かれている）を文面で満たすという有利な読みの隣に置く。**逆側**: 同じ審査で Richard Fontana 氏 2026-08-16 は、ソフトウェアとモデルの素材の両方に当てるライセンスの提出を *"completely appropriate"* とした。Piana 氏が問うたのは量る基準で、対象は制限がソフトウェアの外へ及ぶライセンスだった。ACD は何も制限しないので、「ソフトウェアの基準で量れない」理由は弱い。それでも、ソフトウェアでないものを名指すことが入口になる点は残る。 **2026-11-11: 理事会は 2007-09-06 に *"Open Source Hardware falls within the remit of the Open Source Initiative"* と述べていた（`review-readings.md` §1.173）。ソフトウェアでないものを範囲に入れた記録で、その後の 2021 年の基準と 2023 年の不承認は、範囲を狭く引き直した側の記録になる。** **同日追記: Perens 氏は 2008-11 に *"OSI refused to consider the Open Hardware License because they felt their task should be limited to software."* と書き、フォントのライセンス（OFL・2009 承認）はフォントをソフトウェアとして扱う読みのもとで審査された（`review-readings.md` §1.175）。OFL は、ソフトウェアでないものを扱うライセンスの先例としては弱い。** **2026-11-09: MirOS（2008 承認）の提出文は "software" の代わりに "work" の語を使い、Open Knowledge Definition にも適合するはずだと書いた。読んだ範囲でこの点への反対は無い（`review-readings.md` §1.167）。逆側: MirOS はソフトウェアでないものを列挙していない。** **2026-11-07: 委員会は 2021 年に審査対象の基準を述べていた** —— *"written such that they can be used for software"*（CERN-OHL・`board-decisions.md` §2e）。事務局長は 2024 年に、審査はデータセットとパラメータの文書にも及ぶと述べた（§2g）。ACD はこれに本文で答える。本文を変えて解く手は無い（列挙の語を落としても範囲は変わらず、範囲を縮めると非コード資産を失う・#237・`gap-measurements.md` §1.134。2026-11-04: 1.4 が §1.3 と §9.1 で自分で足したパラメータの名指しは戻した —— 範囲・B10 は不変・`ACD-1.4-CLARITY-TRIAL.md` §7）| — | — | ○ |

**深い分析の所在**: **B1 + B2 / B4 / B5 / B7 / B11 / B15** は [`ACD-OSI-BOTTLENECKS-EXTERNAL.md`](ACD-OSI-BOTTLENECKS-EXTERNAL.md) に在る（**外の答えに依存する項目**）。**B10 は [`ACD-OSI-BOTTLENECKS-B10.md`](ACD-OSI-BOTTLENECKS-B10.md)**（2026-11-15 に EXTERNAL から丸ごと移した・EXTERNAL が advisory を越え、B10 が最大でいちばん足している節だったため）。**B14 だけは [`ACD-OSI-BOTTLENECKS-POSTING.md`](ACD-OSI-BOTTLENECKS-POSTING.md)** ——**instrument の中身ではなく、そもそも投稿できるかという手続きの問題**だから（2026-09-25 に主題で分離）。**B3 / B6 / B8 / B9 / B12 / B13** はこの file の下。**索引・分類・集計は分離していない。**

**集計（表から導出・Check 460 (m) が照合する）**: 主要 15 / 解消済み 0 /
**OSI の判断が要る 8** / **弁護士が要る 2** / **人間が要る 3** / **構造的拒否候補 0**。
「解消済み」は status 欄が「**解消済み**」で始まる行の数で、「構造的拒否候補」は分類の列に `12` を持つ行の数である。項目を閉じるときは status をその語で始める（2026-11-08・Check 498 (e) が同じ数え方で照合する）。

> **⚠ この行は 2026-09-10 に直した。** 直前まで「**OSI 判断依存 3**（B4・B10・B11 の一部）」と
> 書いてあり、**実際に ○ が付いている行は 6 つ**だった（B4 / B5 / B7 / B10 / B11 / B14）。
> **項目を足すたびに列は増えるのに、集計行は最初に書いた数のまま動かなかった。**
> **しかも過少申告である** —— `All N adverse facts` が 118 に対し 14 と書いてあったのと
> **同じ向きの誤り**（#58）。**自分の状態について書いた文は、いま真か。**
> 以後は **Check 460 (m)** が表から導出して照合する。

---

> **⚠ 2026-09-14: 各項目の深い分析のうち、「外の答えを待つもの」を分離した。**
> **索引・分類・集計はここに残る** —— **「この文書が唯一の canonical なボトルネック一覧である」は、
> 一覧＝上の表のことなので、その性質は保たれている。**
> **分離先**: [`ACD-OSI-BOTTLENECKS-EXTERNAL.md`](ACD-OSI-BOTTLENECKS-EXTERNAL.md)
> —— **B1 + B2 / B4 / B5 / B7 / B10 / B11 / B14**（弁護士・第三者の採用・OSI の判断・moderator の
> 決定に依存するもの）。**この file に残るのは、我々の作業で動かせるもの** ——B3 / B6 / B8 / B9 / B12 / B13。
>
> **⚠ 分割線は、前日に測らずに書いた線とは違う。** 2026-09-13 に
> 「次に鳴ったら**索引+status** と **深い分析**で割る」と書いてあったが、**実測すると 85 / 871** で
> **受け皿が即座に再び鳴る**。**測ってから「行為主体で割る」へ変えた（370 / 586）。**
> **見積もりは、現物を測るまで自分に都合よく外れる** ——分割線も例外ではない。

## B6 —— 名称。**識別子は空いている。問題は「Commons」と「Dedication」の 2 語である**

**2026-11-07 に足した**: 「dedication」という語について、CC0 の提出の前に Karl Fogel 氏が述べている（2012-01-02）—— *"Those sorts of promises are what the OSI evaluates and sometimes approves."*、*"I just don't think we should decide that on the basis of nominalism."* 同じ文に *"We could decide, for other reasons, not to evaluate any PD dedications."* も在る（`review-precedents.md` §1.138）。

**2026-11-08 に足した —— 名前は採用の側にも効く。** 0BSD の作者 Rob Landley 氏は、公有化に等しいライセンスに BSD 系の名前を付けた理由を *"In terms of decision making, "4 clause, 3 clause, 2 clause, zero clause BSD" tends to get rubber stamped. Despite other public domain equivalent licenses such as CC0 or MIT-0 having significant pushback from the same departments (when proposed independently)."* と述べ、*"there was explicit marketing strategy in my attempt to make a public domain equivalent license palatable to a broader population, and that strategy was working."* と書いた（`license-discuss` 2021-04・`rounds/2021-04-license-discuss-0bsd-naming-strategy-observed.txt`）。"Autonomous Commons Dedication" は既知の系列に属さない名前なので、企業の法務で同じ押し返しを受けうる（B2 の採用の側）。**逆側**: 審査は本文で決まる（Piana 氏 2018 *"A license must be approved for its text, not for its context"*・`reviewer-positions.md` §1.140）。Landley 氏の証言は一人の作者の経験で、法務の判断を測ったものではない。2026-10-24 の改名しない判断は変えない。

**#112 が記録したとおり、我々は数週間テキストを敵対的に読みながら、
「名前そのもの」を一度も検査していなかった。** 0BSD の改名は `license-review` で 54 通を要している。

**⚠ この測定は新しくない。** `AS-OF.md` に **2026-09-09 付**で同じ測定が既に在り、
**しかもそちらの方が詳しい**（最近似は `CAL-1.0` "Cryptographic Autonomy License" で語幹のみ共有、
という事実をこちらは持っていなかった）。**本節が足したのは disposition であって測定ではない。**
**「初めて検査した」と書きかけて、grep して取り下げた** —— #88 / #92 と同じ形
（**「X はどこにも無い」と書く前に X を grep する**）。

**測定（SPDX License List 3.28.0・727 件・`AS-OF.md` 2026-09-09 / 本増分で 2026-09-10 に再確認）**

| 検査 | 結果 |
|---|---|
| `ACD` で始まる識別子 | **0 件。空いている** |
| 名称に "Autonomous" を含むもの | **0 件** |
| 名称に **"Commons"** を含むもの | **58 件 —— 内訳は Creative Commons 55 / Open Data Commons 3。例外なし** |
| 名称に "Dedication" を含むもの | 2 件（`CC-PDDC` / **`PDDL-1.0` = *"Public Domain **Dedication & License**"***）—— **ただしどちらも OSI 承認ではない**。**命名の先例ではあるが、承認の先例ではない** |

**そこから出る 2 点**

1. **"Commons" は、この名前空間では事実上 2 つの組織のハウスマークである**（58 件すべて）。
   **商標の主張は誰もしていないし、我々も §11 で商標を持ち出さない。**
   だが**審査者が「Commons 系列の一員」と読む余地**はあり、
   **名前は merits として争われる**（#112）。
2. **"Dedication" だけの名前は、この instrument の半分しか言っていない。**
   本体は**献呈（§3）と、それとは独立に付与される許諾（§4・§4.4）**である。
   **Chestek 氏（委員・元委員長）の *"Which is it, a dedication to the public domain or a license?"*（#110）は、
   名前そのものによって強められている。**
   **そして同じ表に、その解き方が載っている** —— PDDL は
   ***"Public Domain Dedication & License"*** と名乗る。
   **ただし PDDL は OSI 承認ではない。使えるのは「名前でその対を表す前例が在る」ことまでで、
   「その対が承認された」ことではない。**

**最小の解消方法**: **1.0 は改名しない。** 凍結中であり、この名前で既に投稿され、
識別子は `machine.json` / `spdx.xml` / `FROZEN.md` / Check 441・453 に pin されている。
**successor 候補として、両方の半分を名前に持たせる案を記録する。**

**変更によって失うもの**: 改名は**継続性を失う** —— 既に公開した名前・識別子・digest・
`rounds/` の投稿本文がすべて旧名を指す。**#108（REUSE の命名要件）とも二重に絡む。**

**副作用・新たな反論**: 名前を変えれば「中身が変わった」と読まれる。
**逆に変えなければ、"Which is it" に対して名前が反証材料であり続ける。**
**どちらも実在する費用であり、片方だけを書かない。**

**外部確認**: 不要（測定は完了）。**status: 1.0 は改名しない。識別子の穴（E14）は 1.1 草案で閉じた** ——`ACD-N` / `ACD-N.N` の族へ保護を広げてある（**2026-11-01 追記**: その形は `ACD-1.4.1` のような 3 段の版番号を外していた。1.4 草案は「`ACD-` に数字が続く識別子」へ広げ、Steward の例外も新しい版番号と識別子に限った —— `ACD-1.0.errata.md` E14・`ACD-1.4-ADVERSARIAL-TRIAGE.md` の H-01 / H-17）。**名前そのもの（"Commons" / "Dedication"）は草案でも変えていない** ——**改名が継続性を失うという費用は、識別子の穴を塞いでも消えない**からである。

**2026-10-24 決定（AI・オーナーの委任による）—— 1.3 でも、承認まで改名しない。**
オーナー明言（同日）「OSI通過の為の何かで私の裁可が必要なものは無いよ」を受け、それまで「オーナーの判断待ち」と
されていたこの項目を AI が決めた。

**改名しない理由（3 つ）**:
1. **記録の継続性。** 1.0 はこの名前で `license-discuss` に投稿され、`rounds/`・機械可読面・digest・`FROZEN.md` が
   すべてこの名前を指す。**最初の `license-review` の直前に名前を変えると「中身が変わった」と読まれ、記録が 2 つに割れる。**
2. **"Which is it" に答えるのは名前ではなく本文である。** §4.1 は Langley 氏の試験（*"Licensor grants X rights"*）に
   通る許諾の動詞を持ち、§4.4 が許諾を §3 から独立させている（#270）。**Unlicense は名前に "license" を否定する語を
   持ったまま、承認されている** ——category は名前ではなく献呈という性質で決まった（*"Special Purpose"*）。
3. **名前の議論は高くつく。** 0BSD の改名は 54 通を要した（#112）。**新しい名前は、提出の瞬間に名前そのものの
   merits の議論を新しく開く。**

**逆側（改名しないことの費用・同じ重さで）**:
- **"Dedication" は半分しか言っていない**ので、名前を見ただけで Chestek 氏（委員・元委員長）の *"Which is it"* の枠に
  入れられうる（#110）。
- **"Commons" は CC / ODC の系列と読まれうる。** CC0 は特許の扱いで OSI の審査から撤回されたので、その連想は
  我々に不利に働きうる（ただしその特許の点こそ ACD が CC0 と違うところでもある）。
- **承認後は改名できない。** 改名が安いのは今だけである。

**それでも決定が保たれる理由**: 改名しない費用は**枠の費用**で、提出文と本文（§4.1 / §4.4）で答えられる。
改名する費用は**記録の継続性と新しい議論**の費用で、本文では答えられない。**見直す条件**: `license-review` で
審査者が名前そのものに merits の異議を述べたら、後継版で改名する（そのときの費用は今と同程度）。

**2026-09-10 追記（敵対的な利用者の視点で読んで出た）**: **§16.4 の保護は名前と識別子で非対称である。**
名前 *"Autonomous Commons Dedication"* は版を含まない形で書かれているので後続版にも及ぶが、
**識別子は `ACD-1.0` だけ**なので、**第三者が改変版を `ACD-1.1` として頒布しても条文には当たらない。**
**我々自身が 1.1 を予定しているため実務的な空きである**（`errata.md` **E14**）。
**承認されれば SPDX が識別子を固定するので、この穴は B11 と同じく承認で縮む。**

---


**2026-11-15 に足した —— 名前が 1 つの本文を指すことを、決める側が良いこととして求めた記録。** Bruce Perens 氏 2010-11（`license-review`・MPL 2.0 の審査）*"I submit that Mozilla would be doing the community a service if they were to make their license invariant."*（`review-readings-2.md` §1.235・portfolio-2f）。ACD の §16.4（1.0 でも §16.4）は、名前と識別子が 1 つの本文を指し続けるように、改変した本文をその名の下で配ることを禁じる —— Perens 氏の求めた不変の形である。**逆側**: ACD は 1.0 から 1.3 まで 4 つの本文を確定し、1.4 を作っている（`against.md` #320）。1 つの名前の下の版の数そのものが、不変を求める読み手には別の問いになりうる。


**2026-11-15 に足した（2 つ目）—— 名前を Steward に結ぶことの両側。** **有利な面**: 当時の委員長 Russ Nelson 氏 2008-05-29（`license-review`・IWL の審査）*"We've always taken the position that a license cannot be modified in any way (not one word). We've always acted as if the license steward's published copy is the official copy, and that we are not empowered to change their license."*（`review-readings-2.md` §1.238）—— Steward が公表した写しを正とする運用で、§16.4・§16.5 の形である。同じ通で同氏は、承認した写しを型板にすべきだとも書いた。ACD は本文に固有名詞を持たず、§16.3 で誰でも 1 語も変えずに当てられるので、その型板の形をしている。**不利な面**: Josh Berkus 氏 2020-03（`license-discuss`・"Thoughts on AAL and OSS vs FOSS"）*"I don't see how an original license author has any moral right to the name. Once the license is released, it belongs to the whole community."*（§1.239）—— Steward だけが名前の下で新しい版を出せる規則（§16.4）は、この立場からは問われうる。**逆側**: GPL と MPL は Steward が新しい版を出す形のまま承認されてきた。Berkus 氏の文は廃止の議論の中の 1 人の立場で、規則ではない。

**2026-11-15 に足した（3 つ目）—— 名前を持つ本文の規律は最初の数年から在った（`review-readings-3.md` §1.302）。** Russell Nelson 氏 2001-11-07（GPL の改変版の提出へ）*"Please either use the GPL as written, adopt another approved license, or write your own license (which we will be glad to consider for approval)."*、Brian Behlendorf 氏 1999-04-14 は名前と固有名詞を抜いた不変の型板を求め（*"genericize them"*）、2000-09-11 には *"changing names on a license doesn't affect OSD conformance"* と書いた。§16.3（誰でも 1 語も変えずに当てられる）と §16.4（改変した本文は別の名で）の形である。**逆側**: どれも承認済みのライセンスの整理か、他人の本文の改変についての文で、新しいライセンスの名前の選び方（「Commons」「Dedication」の 2 語）には答えない。

**2026-11-15 に足した（4 つ目）—— 名前を持たない型板は、2003 年には運用として述べられていた（`review-readings-3.md` §1.306）。** Russell Nelson 氏 2003-04-23 *"For example, the Zope Public License contains the name of the Zope Corporation within it. If you want to use it, you need to create a derivative license, which in most cases will earn a rubber stamp."* ACD は本文に固有名詞を持たないので、この派生の手間が無い。**逆側**: 名前を変えただけの派生が通りやすい、という話で、新しいライセンスの名前（「Commons」「Dedication」）の審査には答えない。

**2026-11-15 に足した（5 つ目）—— 「Autonomous」を名に持つ先行のライセンスが在った（`review-readings-2.md` §1.249・portfolio-2f）。** 2019-01 に Holo のために準備されたライセンスは、告知の文で "Autonomous Agent License" と呼ばれ（Bruce Perens 氏の通に引かれた形でアーカイブに残る）、のちに Cryptographic Autonomy License（CAL）として 2020 年に承認された。Perens 氏の批判は条項（API の実装への条件）に向けられ、名には向いていない。**逆側**: 改名の理由は記録の範囲では分からない。ACD の名がこの先行の名と混同されうるかも確かめていない。

**2026-11-16 に足した（6 つ目）—— 派生に別の名を求めることは「自由」と両立する、と当時の理事が書いた（`review-readings-3.md` §1.312）。** Brian Behlendorf 氏 2001-03-20 *"I don't see asking someone to choose a different name for a derivative work as not qualifying as "free" as the FSF defines it."* §16.4（改変した本文は別の名で）を支える。**逆側**: Apache の製品名の条件について書いたもので、ライセンスの本文の名前の条ではない。

**2026-11-16 に足した（7 つ目）—— 略称の衝突は、承認の投票の前に直すべき点として挙げられたことがある。ドシエはこの点検をしていなかった（portfolio-2f が見つけ、30 が当てた）。** Josh Berkus 氏 2020-12-27（`license-review`・OIN License）は、略称「OIN」がオープンソースの分野の Open Invention Network と重なることを *"seems like a pretty clear trademark infringement in my non-lawyer eyes"* とし、*"even were it otherwise acceptable I'd request a change of license acronym before voting to approve it."* と書いた。提出者は同じ日に略称を改め、SPDX の側も混同を避けて識別子を変えた（B11 の段）。**ACD について**: 上の段の「識別子は空いている」は SPDX の識別子（ACD-1.x）の話で、略称「ACD」が他の組織や製品と重なるかは確かめていなかった。ソフトウェアの会社 ACD Systems International Inc.（ACDSee）が実在する（2f が会社の頁で確かめた・2026-11-16）。オープンソースのライセンスや特許の分野で「ACD」を名乗る組織は、ドシエの記録の範囲では見つかっていない。**商標の登録の有無と範囲は確かめていない**（開いた項目）。**逆側**: 先例の引き金は同じ分野でのはっきりした衝突で、Berkus 氏は法律家でない目と断っている。分野の違う会社名との重なりが同じ扱いを受けるかは分からない。略称を変える費用は大きい（識別子・通知・文書の全面）。

## B8 —— §12 人格権。**同じ条項が「gap」と「mission creep」の両方で名指しされている**

**この項目が難しいのは、賛否が割れているからではなく、賛否が同じ条項の別の面を見ているからである。**

**不利な側（3 件・いずれも一次資料）**

| 発言 | どこに当たるか |
|---|---|
| Carlo Piana 氏 *"these are **not licensable**, so anything the license says one way or the other, nothing changes"*（`license-review` 2023-11・#104）| **§12.1（放棄）に当たる。** ただし §12.2（不行使の合意）は**約束**であって許諾ではないので、同じ反論では倒れない |
| Pamela Chestek 氏が人格権条項の追加を **"mission creep"** と名指し（`license-discuss` 2026-06-23・#6）| **§12 全体に当たる。** 「ライセンスは著作権を扱うもので、人格権まで手を伸ばすのは範囲外だ」という筋 |
| **法域による非対称**（#118・2026-09-09 に自分で発見）| **§12.5 に当たる。** 虚偽の帰属に対抗する利益は、放棄が有効な法域では放棄され、**放棄不能な法域でだけ残る** ——「一貫していない」と読まれうる |

**有利な側（1 件・そして重い）**

Shuji Sado 氏（Open Source Group Japan 会長）は 2024-03 に、**著作権だけを述べるライセンス**は
—— Blue Oak を例に、0BSD と MIT-0 も同じ読みだとして ——
***"not open source, at least not in Japan"*** と論じている（§1.59）。**理由は同一性保持権が
日本ではソフトウェアに及び、改変を止めるのに使えるからである。**

**2026-11-07 追記 —— 同じ Chestek 氏の、逆向きの 2 通が在る。** 2021-02-20（本人の資格で・Ritchey）: *"Maybe your intention is to allow all permitted uses under
copyright law. But what about patent law? What about moral rights?"* 許諾が述べない権利は *"we are left only to guess"* と続く。
2024-09-09（`license-review`）: *"We consider patent rights specifically, and we have recently discussed moral rights. I believe there is sufficient expertise on the committee to
evaluate non-copyright provisions."* どちらも §12 を支持した文ではなく、2026 年の *"mission creep"* のほうが新しい。言えるのは、委員長が人格権を審査の外とは述べていないことである。

**つまり同じ §12 が、一方では「範囲外」と呼ばれ、他方では「これが無いと OSD 3 を
満たさない法域がある」と論じられている。** どちらも `license-discuss` / `license-review` 上の発言である。

**分岐（決めるのは我々ではない）**

| もし審査者が採るなら | §12 に起きること | 我々に残るもの |
|---|---|---|
| 「人格権は licensable でない」（Piana 氏）| §12.1 は無害だが**空**になる | **§12.2 は残る**（不行使の約束。ACD-1.4 は別の文で同意も持つ・T67）。ただし約束と同意が人格権について有効かは別途争われる |
| 「mission creep」（Chestek 氏）| §12 を削れという圧力 | **Sado 氏の論点が答えになる** ——削れば、日本で改変が止まりうる |
| 「法域で結果が変わるのは不整合」（#118）| §12.5 の書き直し | **1.1 には入らず、1.2 草案で扱った**（errata **E26**: §12.2 が *"You are not required to determine which of Section 12.1 and this Section applies … and nothing permitted by this Dedication depends on that question"* と述べ、非対称を条文の側から説明する。**§12.5 自体は書き直していない**。**2026-09-28 訂正**: 旧文は「1.1 候補として `errata.md` に記録済み」だったが、errata に §12.5 の項目は無く、指し先が実在しなかった）|

**最小の解消方法（分類 1・提示の変更）**: **§12 を「人格権も扱う」ではなく
「改変の自由を、著作権だけでは保証できない法域で保証するための条項」として提示する。**
**mission creep への答えは、範囲の弁明ではなく OSD 3 との接続である。**

**変更によって失うもの**: 無し（提示の変更のみ）。**条文は凍結中で触らない。**

**残る gap**: **§12 が有効かどうかは、我々には決められない。**
§12.2 は「不行使の約束」（ACD-1.4 では、それに加えて別の文の「同意」）であって、**それが人格権について各法域で有効かは弁護士の領域**である（同意については `QUESTIONS-FOR-COUNSEL.md` 問 3 (e)）
（B1 と同じ壁）。**「無効かもしれない」と書いてある条項を、有効であるかのように書かない。**

**外部確認**: **必要**（B1 と同じ）。**status: 分岐を記録済み・提示のみ調整可。**

---

**2026-11-16〜17 に足した —— §12.2 の約束と同意の足場を、4 法域の条文と 1 人の弁護士の意見で狭めた（portfolio-30・法源は `rounds/`・我々の読み）。** B8 の「gap か mission creep か」は審査者の評価の問いで、条文では決まらない。ここで狭まったのは、その下にある「§12.2 は効くのか」の側である。
(1) **4 法域とも、人格権を譲渡できない・放棄できないと定め、1.0〜1.3 の §12.2 が働く側になる**（1.4 草案は T101 で §12.2 の引き金を無くし、約束と同意を *"given for every jurisdiction, whether or not Section 12.1 has effect there"* と §12.1 に並べたので、1.4 ではこの分けは要らない・2026-11-19 追記）: 日本の著作権法 59 条、フランスの CPI L121-1（*"Il est perpétuel, inaliénable et imprescriptible."*）、ドイツの UrhG 29 条 1 項（著作権そのものが移せない）、英国の CDPA 87 条 2 項（放棄には署名ある書面が要る）。
(2) **4 法域とも、約束や同意の形を法の側が予定している**: ドイツの UrhG 39 条 1 項（変更の禁止は *"wenn nichts anderes vereinbart ist"*）と 29 条 2 項（39 条の人格権の取引を許す）、英国の CDPA 87 条 1 項（同意した行為は侵害でない）と 4 項（署名の無い放棄にも契約と禁反言の一般法が働く・人格権の章に限る）、フランスの L121-7（ソフトウェアの著作者は名誉や声望を害さない改変に反対できない）、日本の 60 条ただし書（死後の保護は著作者の意を害しない行為に及ばない）。
(3) **残る核は同じ形で 4 法域に在る**: 包括的・無制限の事前の同意は、名誉や声望を害する改変・歪曲には届かないと読まれる —— ドイツの UrhG 14 条と Kreutzer 氏の *"global and unrestricted disclaimers"* *"about moral rights positions are invalid."*（通説として）、フランスの L121-7 の *"préjudiciable ni à son honneur ni à sa réputation"* の除外。§12.3（the Work に限る）と §12.5（偽の帰属は約束の外）は「無制限」より狭いが、届かない部分は §12.6 と §15.2 が受ける。
**逆側**: 法律家の審査ではない。Kreutzer 氏は 1 人の弁護士の 2011 年頃の意見で、判決ではない。日本の不行使特約は実務の形で、効く範囲を判例で確かめていない。B8 の評価の問い（この条を「必要」と見るか「行き過ぎ」と見るか）は、どの法源でも答えられない。

**2026-11-20 に足した —— ソフトウェアに限ると、「gap か mission creep か」の答えが法域で割れる（portfolio-30・条文は `rounds/2026-11-20-cdpa-1988-s9-s78-s79-s81-s84-s94-legislation-gov-uk-snapshot.txt` と `rounds/2026-11-19-jp-chosakukenho-19-20-30-4-tokkyoho-68-78-94-99-snapshot.txt`・我々の読み）。** 英国の CDPA は、氏名表示権を *"(a) a computer program"* に与えず（79 条 2 項）、同一性保持権も *"The right does not apply to a computer program or to any computer-generated work."*（81 条 2 項）とする —— 英国のコードには §12.1 と §12.2 が手放す相手の大半がもともと無く、残るのは偽の帰属を受けない権利（84 条）だけで、それは §12.5 が §12 の外に置く。**英国のコードについては、§12 は mission creep の側に近い**（害は無いが、働く場面がほとんど無い）。日本は逆で、同一性保持権はプログラムにも及び、外れるのは 20 条 2 項 3 号の *「特定の電子計算機においては実行し得ないプログラムの著作物を当該電子計算機において実行し得るようにするため、又はプログラムの著作物を電子計算機においてより効果的に実行し得るようにするために必要な改変」* だけ —— Sado 氏の *"not open source, at least not in Japan"*（上）は、この狭い除外の外の改変（機能の追加・削除）を指す読みで成り立つ。**日本のコードについては、§12 は gap を埋める側に在る。** ドイツは 69b 条が財産権の行使を雇用者に置くが人格権は従業者に残り、フランスは L121-7 がソフトウェアの改変への反対を名誉と声望の侵害に限る（ドイツの条文は `rounds/2026-11-19-jp-chosakukenho-15-urhg-43-69b-employee-works-snapshot.txt`）。**有利な面**: 同じ §12 が、人格権の強い法域では gap を埋め、弱い法域では害なく空になる —— 1 つの文で両方の評価に答える形で、法域ごとに条を分けずに済む。**逆側**: 審査者が英国や米国の目で読めば §12 は余分に見え、B3（長さ）の費用だけが残る。どちらに見えるかは読み手の法域で決まり、我々には決められない。

## B9 —— §7 データベース権。「未検証・削除候補」だったので、検証した。**削除しない**

**検証したこと**: §7 は 67 語 2 項。**§1.5（Covered Rights の定義）が既に
*"sui generis database rights"* と *"rights against unfair extraction"* を含んでいる**ので、
**§7 は丸ごと重複ではないか**を確かめた。

| 項 | 語数 | 判定 |
|---|---:|---|
| **§7.1**（DB 権は Covered Right であり §3〜§6 が適用される）| 24 | **重複である。** §1.5 が権利を含み、§3〜§6 は Covered Rights 全体に働く。*"To the extent … subsists"* も §1.5 の *"whether or not presently subsisting"* と同じ |
| **§7.2**（全部または実質的部分を、反復的・組織的に、無制限・無条件に抽出し再利用してよい）| 43 | **重複ではない。削除しない** |

**⚠ 逆側（2026-09-15 追記・種類 8 の掃引で出た）。** **この節の見出しは「削除しない」と述べるが、同じ節の表は §7.1 を「重複である」と述べている。** 見出しが表より広い。
**保持の費用は 24 語** ——**B3（長さ）の測定に直接乗る量であり、しかも「重複」は *"excessively wordy"* という既出の批判が名指ししうる形そのものである。**
**それでも保持する理由**（明示しておく）: §7.1 は §1.5 と §3〜§6 の関係を**その場で読める形**にしており、**削れば読み手は 3 条を辿ることになる**（#99 の読み順問題と同じ）。**24 語はその対価である。**
**この判断は再検討しうる** —— B3 の削減候補一覧（`ACD-1.1-CHANGELIST.md`）に **§7.1 は入っていない**ので、**入れるかどうかは次版を確定するときの判断**である。**「削除しない」はここでは §7.2 についてだけ確定している。**

**§7.2 が独立に働く理由**: sui generis 権は **行為の語**（抽出 / 再利用 / 実質的部分 /
反復的かつ組織的）で定義されており、**一般的な許諾文が同じ行為に届くかは自明ではない。**
とくに *"repeatedly and systematically"* は、**些少部分の反復抽出を禁じる側の規律**に
正面から当たる語である。**学習用データセットの構築は、まさにこの行為の形をしている。**

**さらに、これは委員長が「モデルを保護しうる理論の一つ」として挙げた当の権利である**
（`reviewer-positions.md`）。**削るのは、審査者が名指しした論点から条文を引くことになる。**

**変更によって失うもの**: §7.1 を落とせば 24 語（本体の 0.5%）。**B3 の結論
（機構部を削っても届かない）を踏まえると、この 24 語のために「EU の審査者が
見出しから中身へ入ったとき、まず権利の帰属が書いてある」構造を崩す価値は無い。**

**結論: §7 は削除しない。§7.1 は successor で 1 文に圧縮する余地があるが、優先度は低い。**
**表の status を「未検証（削除候補）」から「検証済み・保持」へ変える。**

**外部確認**: 不要。**status: 検証済み。**

---

## B13 —— 理解コスト。B3 の結論により、これが長さへの唯一の実効的な緩和になった

**位置づけの変更（2026-09-09）**: B3 は「縮められるが答えきれない」と結論した（§2.8）。
**したがって長さへの実効的な緩和は本文の外にしか無く、それが B13 である。**
表の impact 高は据え置き、**status を「部分的に解消済み」から「継続対象」へ変える。**

**測定（2026-09-09・語オフセット）**

| 面 | 規模（**2026-09-09 実測**）| 審査者が必要な答えに到達するまで |
|---|---:|---|
| 送る文面 `submission.md` §B.0 | **972 語** | gap 24% / 最近似 49% / 法的レビュー 8% / 提出者専用でないこと 85% |
| 入口 `REVIEWERS.md` | 2,402 語 | **改善前: gap 35% / 最近似 30% / 法的レビュー 29%** → **改善後: 5% / 8% / 9%** |
| `objection-map.md` | 653 語 | 1 つの表 |
| `against.md` | 29,586 語 | 完全な記録（#120 で経路を直した）|

**この表は 2026-09-09 の測定である。** **数え方は macOS の `wc -w`（UTF-8）で、記録に書いていなかった**（2026-11-02 に各 file の当日の git 版で再現して特定）。英語だけの `REVIEWERS.md` は空白区切りでも同じ値になるが、**日本語を含む 2 つは数え方で値が割れる** —— `objection-map.md`（09-09 23:44 の版）は `wc -w` 653・空白区切り 634・ASCII 文字を含む語 367、`against.md`（09-09 23:54 の版）は 29,586・29,583・28,563。比べるときは同じ数え方で数え直すこと。 §B.0 はその後 1,362 語（2026-09-24）に伸びた。現在値は §B.0 の見出しを読むこと（Check 460 (p)）。
**🔴 2026-09-24 に測り直した入口ページ**: `REVIEWERS.md` は **2,402 → 4,353 語（+81%）** に伸び、冒頭へ "The short path" と "Which text you are looking at" が足された結果、**"In one screen" は 4% → 15% の位置へ押し下げられ**、gap への到達は **5.7% → 16.2%**、最近似への到達は **8.4% → 24.8%** に悪化していた（上の「改善後」は、その後の追記で黙って崩れていた）。**"In one screen" を "Which text" の前へ移した**（引く条 §4.4 / §6 / §8.4 / §9 はどちらの版でも同じ番号なので、版の対応表より先に読んでも意味が変わらない）。移動後は **In one screen 6.9% / gap 8.2% / 最近似 16.8%**。2 つの弱点は "The short path" の表で **約 3%** に在る。**⚠ 逆側: 4% には戻っていない** —— 冒頭の "The short path"（読む量の見積もりと、止めたときに失うもの）は審査者の時間を節約するための節で、削らない。**入口が伸びるのは開示を足すたびに起きるので、次に入口へ節を足すときは "In one screen" より前に置かないこと。**

**🔴 2026-11-06 に測り直した入口ページ**: `REVIEWERS.md` は **4,353 → 5,370 語（+23%）** に伸びていた。"In one screen" は 641 語で 1 画面ではなくなり、Status は 1,159 語で、審査者が主張へ着く前に経緯の段落を読む形だった。中身も 11-04 の結論からずれていて、*"The same gap, in detail"* が §6 / §8.4 / §9 を「同じ gap」と名乗り、§1.134 が独自性の根拠から外した §6.1 と §9 を含む別の 3 項目を挙げていた。直して **4,411 語**、"In one screen" は 7 割（**先頭から 375 語の位置**）、最近似への到達は **886 → 666 語**、Status は 524 語にした。経緯の細部は B14 と `against.md` に既に在るものだけを外し、開示は減らしていない。**2 度目の退行である**（1 度目は 09-24）——**追記のたびに伸びるのは入口ページの性質で、1 度直しても止まらない。**

**🔴 2026-11-06: 勧めた文書が、勧めた相手に読めなかった。** `REVIEWERS.md` は英語の審査者へ「3 つ読めば足りる」と案内し、その 1 つが `objection-map.md` だが、**表の 30 行中 28 行に日本語が入っていた**（案内の 827 語は ASCII を含む語だけの数で、日本語の分を数えていなかった）。"short path" の 3 分の 1 が審査者に読めない状態で、2026-09-09 から続いていた。本文を英語へ書き直し、09-22 以降に抜けていた反論（#211 / #265 / #266 / #276）と、窓の外でも判断を左右する 6 件（#237 / #255 / #262 / #263 / #270 / #280）を足した。Landley 氏の行の答えは §1.133 の結論へ改め、「GPLv3 より 43 語短い」は相手がしていない比較なので外した（#116）。**短い道は 5,950 語から約 7,450 語へ増えた** —— 語数が増えたのではなく、数えていなかった分が見えた。

**2026-11-07**: 決める側の文書から足した記録で、短い経路は約 7,550 語から約 8,050 語へ伸びた（`objection-map.md` 2,451 → 2,938 語）。最初の画面は 500 語の上限を保った。**記録を足すほど B13 の費用は上がる**ので、次に足すときは同じ行の説明を削れないかを先に見る。

**2026-11-24 に測り直した入口ページ（空白区切りの語・main の版）**: 11-06 の 5,518 語から **11,703 語**（合議の記録の議題 14 の値）まで伸びていたのを、発言の表と「1.4 が自分の語で述べなくなった理由」の節を `REVIEWERS-RECORD.md` へ移して **7,819 語**にした（文は書き換えていない・3f の PR 4075）。"In one screen" の位置は **440 語目**（Check 472d の上限 450 の手前）、Status は 2,801 語目から、The case は 3,391 語目から、Disclosures は 5,885 語目から始まる。**逆側**: (1) 2 つの file を合わせると 11,870 語で、読む総量は減っていない —— 減ったのは入口で読む量だけである。(2) 発言の表の不利な側は 1 click 遠くなった（Disclosures と "The three weaknesses, first" は入口に残る）。(3) "The new language" の節（938 語目から約 1,160 語）は、提出する版が 1.4 のあいだの条の引用で、次の版が確定すれば短くなる見込みだが、まだ測っていない。**3 度目の退行である**（09-24・11-06 に続く）。

**2026-11-06 後半**: 有利な記録の表（OSI の FAQ・理事会の議事録・審査者の発言）と基準 8 条の表を足し、`REVIEWERS.md` は 5,518 語へ戻った。**増えた大半は後ろの "The case" の節で、"In one screen" の位置は 375 → 391 語、最近似への到達は 666 → 758 語へ少し伸びた**（承認されるべき理由を先に足した分）。Check 472d / 472g が先頭の 2 節を守り、それより後ろは守らない。

**やったこと**: 入口ページの冒頭に **"In one screen"** を置いた ——**何であるか / 主張する gap /
最近似の承認済みライセンス / 2 つの弱点 / 提出者専用でないこと / 次に読む 1 件**。
**弱点（法的レビュー無し・採用 1 件）を、主張より前ではなく同じ画面に置いた** ——
後ろに置けば「見つけさせる」形になる。

**なぜ改善前は 30% だったのか（自作の退行）**: **B14 の停止告知を Status に足したのは同じ日の
自分である。** 状態の説明が増えた分だけ、主張と弱点が下へ押し出された。
**#120 と同じ族 ——最後に書かれ、最初に読まれるページ。**

**2026-09-10 追記 —— B13 には天井がある。** Chestek 氏（委員・元委員長）は 2026-09-01 に、条文の外にある説明について
*"you can't count on FAQs to prevent an unintended interpretation"* と述べ、
**「四隅の外」の記述は intention の証拠にしかならないとした**（#124）。
**短い入口は読まれる確率を上げるが、それ以上は上げない ——審査は四隅で決まる。**
したがって **B13 の投資は「読まれる確率」までで頭打ちであり、答えは条文の中に置くしかない**
（§4.4 がその唯一の実例）。

**⚠ ただし四隅の原則が当たる範囲を、広く取りすぎないこと。**
**この原則は「条文がどう解釈されるか」に当たる。「OSI が承認すべきか」には当たらない。**
後者は委員会への議論であり、**ドシエこそが正しい容れ物である。**

**当たる 9 件を手で分類した（2026-09-10・grep ではなく読んで）**

| 反論 | 答えの在り処 | 種別 |
|---|---|---|
| 献呈と許諾の並置（#110）| **§3 / §4 / §4.4 / §11.3** | **条文内・構成の問題** |
| 人格権は licensable でない（#104）| **§12.1 と §12.2 の二段構え**（ACD-1.4 の §12.2 は約束と同意の 2 つの文） | **条文内・構成の問題** |
| 特許射程が uptake を下げる（#107）| **§8.1 / §8.4 / §8.2（報復ゼロ）** | **条文内・構成の問題** |
| mission creep（#6）| **§12 は条文内**だが、必要性の論拠（日本の同一性保持権）は散文 | 混在 |
| なぜもう一つ（#84）| **§12 は条文内**だが、「類型に 1 件足す費用」の議論は散文 | 混在 |
| 弁護士が要る（#5 / #79）| **条文では答えられない** ——事実の欠落である | 承認政策 |
| 長すぎる（#6）| 語数と比較は散文（§4c）| 承認政策 |
| 1 文書に 3 つのこと（#105）| 構成の説明は散文 | 承認政策 |
| 一つの instrument に一つの権利（#102）| 同上・しかも #105 と逆を向く | 承認政策 |

**読み方**: **構成の問題 3 件は条文内で答えており、四隅の基準を満たす。**
**混在 2 件は、条文が「何をするか」は述べているが「なぜそれが要るか」は述べていない** ——
**そして「なぜ」は解釈の対象ではないので、散文で足りる。**
**承認政策 4 件は、条文に書いても解決しない**（むしろ B3 の長さを悪化させる）。

**したがって successor で条文へ移すべきものは、実は多くない。**
**#124 を「全部を条文へ入れろ」と読むのは過剰修正である。**

**この節が establish しないこと**: **理解コストを下げても、長さそのものは変わらない。**
Chestek 氏が engage しなかった 2 例は**ライセンス本文**の語数で述べられている（#116）。
**短い入口は「読んでもらえる確率」を上げるだけで、「長い」という評価を消さない。**

**外部確認**: 不要（AI だけで前進可能）。**status: 継続対象。**

---

**2026-11-15 に足した —— 不透明さを善意で通した判断を、通した側の 1 人が後で誤りとした。** John Cowan 氏 2018-06-20（`license-review`・L0-R の審査）*"I believe that RPL's certification was wrongly decided, although it is probably too late to reverse it now. I remember thinking at the time that the license was very hard to understand (I don't find it so now, particularly), but that it meant well and we probably should approve it despite its opacity. I wish now that I'd made more fuss then."*（`review-readings-2.md` §1.228・portfolio-2f）。「意図は良いが読みにくい」本文を通した過去を、決める側が悔いた記録で、理解の費用は善意では払えないことを示す。2026-09-24 の却下の第 1 の理由が *"Poor drafting"* だったこと（B1・`board-decisions.md` §4a）と同じ向きである。**逆側**: 同じ文の括弧書き（今はそれほど難しくない）は、読みにくさが慣れで変わることも言っている。RPL は使用に条件を課す型で、何も課さない ACD とは読みの重さが違う。


**2026-11-23 に足した —— 前文の形は、審査の側が勧めた形に在る（5e の読み・`~/osi-archive-cache/license-review-2020-December.txt` の OIN License の会話）。** Roland Turner 氏 2020-12-27: *"The usual way to handle this in the construction of legal instruments is to shift statements of principle into a preamble, either a section specifically headed Preamble (e.g. Gnu licenses) or"* recitals で、*"Either is fine"*、*"Without this relationship, a court is going to have real trouble discerning the intentions of the parties."* 委員長だった Russ Nelson 氏も同じ日に *"If it's not a restriction, it does not belong in the license. It might go into a preamble, but it should be phrased in the form of encouragement, not agreement."*。ACD の前文は見出しで作用の条から分かれ、*"Sections 1 to 16 are the operative terms. This preamble is not, and nothing in it qualifies them."* で閉じる —— Turner 氏の勧めた形で、理由を条から外して前文へ移した 1.4 の作業（入口の "Reasons ACD-1.4 no longer gives in its own words"）も同じ線に在る。**逆側**: (i) 前文の第 1 段は出典の無い経験の言明（承認済みのライセンスは学習について沈黙する、など）を持つ。(ii) Nelson 氏の「約束でなく奨励の形で」に照らすと、前文の *"It gives away, once and without conditions"* は約束の形に近い。(iii) Turner 氏の同じ通は *"explicitly wording in the fashion of a license condition and then rowing it back in the following paragraph invites abuse"* と続く。ACD の「Section N … is not a condition upon You」の文は条件を言ってから引っ込める形ではないが、§16.4 の末文のように条件の語と打ち消しの語が 1 文に並ぶものは、読み手によってはその型に見える（1.5 の点検の候補・5e へ送った）。

## B3 —— 長さ。測定が解消経路を示した

**なぜ承認上の問題か（事実）**: Chestek 氏が長さを理由に engage しなかった記録が **2 件**ある（2024-10 は委員長として・2026-06 は委員として） ——
*"approximately 4500 words … **I have not read these licenses in detail**"*（2024-10-05）と
*"3888 words … **excessively wordy** … not a good candidate for approval"*（2026-06-23）。
**ACD-1.0 は 4,896 語**（本体 4,574）で、**両方より長い**。

**測定（本体 4,574 語・2026-09-09）**

| 区分 | 語数 | 割合 |
|---|---|---|
| **gap 部**（§6 ML/TDM 282・§8 特許 583・§9 機械生成物 176）| **1,041** | **23%** |
| **machinery 部**（§1 575・§2 558・§13 108・§14 98・§15 328・§16 356）| **2,023** | **44%** |
| その他（§3 §4 §5 §7 §10 §11 §12）| 1,510 | 33% |

**最小の解消方法（分類 2 / 3 / 4・gap 損失ゼロ）**

| 対象 | 語数 | 削れる理由 |
|---|---|---|
| §2.9 | 111 | *"not executory"* は forum が決める分類（**E5 が既に記録**）。事実だけ述べて結論を落とす |
| §15.2 / §15.3 / §15.5 / §15.6 | 168 | 単複・contra proferentem・沈黙・代理否認。**MIT / 0BSD は 1 つも持たない** |
| **§16.4 + §16.5** | **165** | 文書自体の再頒布制限と翻訳例外。**落とすと E2 / E3 / E12 と #108 隣接も同時に縮む** |
| §1.10 "Reservation" の inline 化 | ≈40 | 使用箇所は §6.2 / §6.3 のみ |
| §2.5 の圧縮 | ≈45 | estoppel は §2.2 の irrevocable と重複が大きい |

**合計 ≈529 語（本体の 12%）。** ← **2026-09-09 に実際に置換文を起草して数え直した結果、正しくは 306 語（6.7%）である**（内訳と起草文は `ACD-1.1-CHANGELIST.md` §2.6）。**見積もりは 42% 外れていた** —— 節の大きさを削減量として数えたためで、§2.9 は事実を残すので 56、§15.5 は統合なので 57、§16.4+§16.5 は書き足すので 45、**§1.10 の inline 化は撤回**（"Reservation" は §2 でも使われており、74 語の列挙を3 箇所へ展開すれば長くなる）。

**そしてこれで足りないことが分かった** —— 改定後は全体で約 4,590 語で、**Chestek 氏が engage しなかった 2 例（3,888 / 約 4,500）をどちらも下回らない**。**B3 は「無駄を削る」問題ではない。** そして **(b) 構造変更（説明的な節を附属文書へ出す）も成立しない** ——測って否定した（`ACD-1.1-CHANGELIST.md` §2.7）。**附属文書は審査対象ではないので移せるのは「争われても条文で答える必要がないもの」だけ**だが、引用密度が最も低い 4 節（§14 責任制限 / §13 無保証 / §5 不行使の合意 / §15 解釈・可分性）は**どれも移せない**（無保証条項の不在は permissive ライセンスとして成立しない／§5 は §3 が無効な場合の受け皿で§4.4 と対の中核主張／§15.4 は他条が名指しで参照）。

**残る道は (c) 本文内での圧縮のみで、対象は §1 + §2 + §15 + §16 = 1,797 語（本体の 39%）。**
**3,888 語を下回るにはこれを半分以下にする必要があり、gap を損なわずに可能かは未実証。**
**実際に最大の定義 3 件を書き直して測った（§2.8）—— 228 → 182 語＝ 20%、意味の変化なし。**
**その率を機構部 1,797 語すべてに外挿しても約 360 語**（外挿であって測定ではない）で、
§2.6 の 306 語と合わせて **4,896 → 約 4,230 語。3,888 語には届かない。**

**2026-09-10 夜・実物で確かめた**（**語数はその後の errata 修正で動いた** —— 権威は草案自身の宣言と Check 468。2026-09-11 実測 **4,866 語**）: 1.1 草案は **4,742 語・77 条**（1.0 は 4,896 語・82 条）で、
**正味 −154 語（3.1%）にしかならなかった。** 内訳は **機構部で −302**、
**正確さのために +148**（E12 の notice の限定 +18 / E16 の opt-out 可視化 +55 /
E15 の因果の限定 +75）。**削減の半分が、欠陥を閉じる語で相殺された。**

**そこから出る、B3 についての最も重要な事実**: **長さは正確さと直接競合する。**
**「短くする」を目標にすると、閉じるべき欠陥を閉じない方向へ圧力がかかる。**
我々は**正確さを選んだ**（言い過ぎを削るのに語が要るなら、語を足す）。
**したがって B3 は successor でも解消されない。**

**🔴 2026-09-24 追記（上の 4,742 / 4,866 は凍結前の途中値だった）**: **凍結された 1.1 は 5,051 語・78 条で、1.0（4,896 語）より +155 語（+3.2%）長い。** 1.2 草案は**その時点で** 5,299 語・80 条（+403 語・+8.2%）だった。**草案は伸びるので現在値は草案冒頭の申告を読むこと**（Check 468c が実測と照合する・2026-09-26 時点は 5,335 語）。1.1 は凍結 pin が実測と一致させている。**この節は「1.1 で −154 語」までしか書いておらず、successor が 1.0 より短いと読める状態で止まっていた。** **結論（縮められるが答えきれない）は変わらない。変わったのは向きで、successor は実際には長くなり、長さは正確さと競合するという上の事実を実物が裏づけた。**

**2026-11-04 追記 —— 語数ではなく読みの分岐を対象に、1.4 草案で試した（`ACD-1.4-CLARITY-TRIAL.md`）。** 採用したのは −157 語（§2.8・§12.4 の理由の文 −79 / §13.2 への案内と §11.4 の理由の文ほか −63 / §1.3 と §9.1 のパラメータの名指し −15）で、本文が自分で作っていた反対解釈の分岐が 3 件と、§4.6 の指示語の分岐が 1 件消えた。草案全体は 1.3 の 5,443 語より短くなった（現在値は草案冒頭の申告が権威）。
**⚠ 逆側**: 理由の文 9 件のうち 6 件は残した。§6.5 前半と §8.4 は審査者向けの文書が本文の言葉として引いており、§11.3 は §9.4 が指す理由そのもので、§8.3 は操作条項の指示語の先である。**理由の文は反対解釈の種であると同時に、我々の答えの置き場でもある** ——四隅の原則（#124）のもとでは、外すと答えが本文の外へ出る。**−157 語は本文の約 3% で、下の結論は変わらない。**

**🔴 2026-11-24 —— 下の結論は「削る」案だけを測ったもので、「同じことを 1 度ずつ述べ直す」案を測っていなかった（6c の指摘・§1.480）。** 1.5 草案（T146・`ACD-1.5-CLARITY-TRIAL.md` §12）は、1.4 の 80 条を 50 条にまとめ直して、載せた日に **3,168 語**（その後の束で動いた。現在値は草案の道具が測る）（題名から・空白区切り。第 1 条から *END OF TERMS* の手前までは 3,157 語）になった。GPL-3.0（5,644・4,617）より題名から 2,476 語、条文で 1,460 語短く、Chestek 氏が 2026-06 に長さを理由に挙げた 3,888 語も下回る。45 語超の文は 1.4 の 28 / 191 から 4 / 144、最長の文は 93 から 51 語（`measure_clause_clarity.py`）。意味が動いた所は `ACD-1.5-CHANGELIST.md` の「T146 で意味が動く所」に 1 行ずつ在る。

**効く理由は短さでなく「2 度言わない」こと**（Chestek 氏 2026-01-24・§1.481）で、提出文で短さを承認の理由に立てない —— Perens 氏 2017-10-23 は、同じ効果で短いだけのライセンスの承認を *"an active disservice to the community"* と書いた。 **2026-11-26（§1.493）**: 2019 年以降の決める側の通を書き直しの語で拾うと、効果を変えずに短くしただけの書き直しを受け入れた文は見つからず、2026 年に見た書き直しは *"a poor attempt at rewriting the MIT license"* と呼ばれた（Chestek 氏 2026-03-29・AIAL v2）。受け入れられた平易な書き直しの Blue Oak（2024 承認）は、法律家が書き、特許の許諾という機能を足していた（Villa 氏 2023-11）。**逆側**: 1.5 は他人のライセンスの書き直しでなく同じ steward の次の版で、OSI は版の更新を受け入れてきた（MPL 2.0・EPL 2.0）。1.5 は効果の差を 31 項、公開の一覧に挙げており、「効果を変えずに短くしただけ」ではない（その分、効果の差の記録を問われる）。**逆側の逆**: Blue Oak の受け入れの条件（法律家が書いた）は ACD に無い（B1）。

**逆側**: (1) 凍結していない。提出対象は ACD-1.4 のままで、1.4 については下の結論が立つ。(2) AI のモデルが 1 日で書き直した本文で、法律家も第三者も読んでいない。文脈なしの読みは agent のもので、人の審査ではない。(3) 2 か月の敵対的な検査を受けた 1.4 の文を置き換えた —— 回帰試験は開いた欠陥を 20 件あまり見つけて直したが、見つけられなかったものが無いことは示さない。(4) 理由の文を外したので、審査者の問いに本文の言葉で答える場所が減った。(5) McCoy Smith 氏 2019-05-11 は、複雑さそのものは却下の理由でなく、曖昧さを生む単純さは理由になると書いた。長さが答えになるかは、曖昧さが増えていないときだけである。

**2026-11-24 までの結論（削る案について・提出対象の 1.4 に当たる）: B3 は「解消できる項目」ではなく「縮められるが答えきれない項目」である。**
gap 部 1,041 語を削れば届くが、**それは B10（新規性の根拠が残っているか・最高位）を
悪化させるので取引として成立しない。** **残る緩和は本文の外にある短い入口だけ**で、
2026-09-09 の実測では送る文面 972 語 / 入口ページ約 1,900 語（**同日の B13 の表は 2,402 語で、git の同日版も 2,402 語。約 1,900 は誤り**）/ objection-map 653 語（`wc -w`・空白区切りなら 634。数え方は B13 の表の注）＝
**審査者が最初に触れる面は本文の 1/5 だった。**
**⚠ 2026-09-24: 送る文面は 1,362 語になった**（+40%・現在値の権威は `submission.md` §B.0 の見出しで、Check 460 (p) が実測と照合する）。増えた分は来歴と弱点の開示であって削れる無駄ではないが、**唯一の実効的な緩和である短い入口が、本文の 1/5 から 28% へ伸びている。**
**successor 候補の置換文は 7 件・約 350 語・gap 損失ゼロ**（§2.6 + §2.8）。

**より大きな再設計**: §1 の定義 10 件のうち `Contribution`（§2.6 のみ）と
`Machine-Generated Material`（§9 のみ）を使用箇所へ inline すると更に ≈100 語。
**ただし §1 は前方参照が 3 件ある（E13）ので、並べ替えと同時に行う。**

**変更によって失うもの**: §15.2〜§15.6 は「争われたときの防御」であって「許諾の内容」ではない。
**失うのは防御であって gap ではない。** §16.4 を落とすと**識別子が固定テキストを指す保証**が
消える —— これは §16.4 の目的そのものなので、**代替（凍結 + 公開 digest）で置き換えられるかを
検討してから決める。**

**変更後も残る gap**: §6 / §8.4 / §9 は 1 語も触らない。**23% がそのまま残る。**

**副作用・新たな反論**: 短くすると「防御が薄い」と読まれうる。ただし
**MIT・0BSD・Unlicense はいずれもこの種の防御を持たずに承認されている**ので、
**先例のある方向への移動である。**

**外部確認**: 不要（AI だけで前進可能）。**status: successor candidate 化済み** ——条項ごとの判定は `ACD-1.1-CHANGELIST.md` §2.5。

**⚠ 見積もりを 1 件撤回した。** 当初「§16.4 + §16.5 を落として 165 語」としたが、§11 の問い（**これが無いと何が壊れるか**）を当てると **§16.4 は登録されるまでの橋**だと分かった ——MIT / 0BSD / Unlicense が同じ条項を持たないのは **SPDX と OSI がテキストを固定しているから**で、**ACD-1.0 はまだどちらにも載っていない**。**削除ではなく §16.5 を §16.4 へ統合**し、節約は 165 → **≈85 語**。**総計 ≈529 語は据え置き**（他候補の内訳で吸収）。

---

**2026-11-16 に足した —— 長さを確かさの代価とする読みと、その逆（`review-readings-2.md` §1.255・portfolio-2f・どちらも参加者の発言）。** Ian Lance Taylor 氏 2004-02（`license-discuss`）は AFL について *"rather more likely to be legally sound. However, for that very reason, it is much longer."* と書き、同じ月に Alex Rousskov 氏は *"new 100 page legal license attached has fewer chances succeeding in real world, no matter how many lawyers are happy"* と書いた。**ACD への当たり方は半分**: Taylor 氏の読みは、長さが法律家の起草から来る確かさの代価だという前提に立つ。ACD は法律家の起草ではない（B1）ので、長さを確かさの印として引くことはできない。Rousskov 氏の側（長いものは実際には使われにくい）は、そのまま当たる（B2）。**同じ向きの 2 つ目の記録は、構造が長さを生むと言う**: Rick Moen 氏 2015-10-02（`license-discuss`・`review-readings-2.md` §1.256）は CC0 を、献呈が効かない法域で働く許諾を含むので確かだと評し、*"(On the gripping hand, this causes its full text to be lengthy.)"* と添えた。こちらは法律家の起草を前提にせず、献呈＋許諾という構造が長さを生むと言うので、§3＋§4＋§5 を並べる ACD にはより当たる。**逆側**: 構造が長さの理由になっても、ACD は CC0 の約 5.6 倍で（長さの行）、構造だけでは説明しきれない。

**2026-11-16 に足した —— 複雑さを理由に却下すべきだった、という委員会側の振り返り（`review-readings-6.md` §1.458・portfolio-9b）。** Richard Fontana 氏 2016-08-20（`license-discuss`・opensource.org のアドレスから・NOSA 2.0）*"Possibly, in retrospect, the better approach with NOSA 2.0 would have been to outright reject it as being way too complex with a number of likely or actual fatal problems."* **理由は連言である**（複雑すぎる、かつ致命的な問題を多く持つ）—— Chestek 氏の長さの文（#116）と同じく、片方だけを取らない。ACD の長さは前者に当たり、後者は B1（法律家の審査が無い）の側の問いになる。**逆側**: 逆向きの評も記録に在る —— Nelson 氏 2008-01 の委員会報告 *"Rosen suggests that this license is worthless because it is too simple."*（Boost について）。短すぎても長すぎても批判されうる。

**2026-11-23 に足した —— 新しいライセンスに求められる明確さの水準と、法が既に定めることを条に書くことへの問い（`review-readings-6.md` §1.459・portfolio-d7）。** Josh Berkus 氏 2015-06-12（`license-review`・TOPPERS）*"If this were not a legacy license, I would push to replace that with the phrase "one of the following two conditions" just to make it completely clear.  Given that it is legacy (and thus, already in use with that wording), I think a framing paragraph on the OSI page is sufficent."* —— 使われてきた旧来のライセンスには語のぎこちなさを許し、新しいライセンスには「完全に明確」を求めた。ACD は新しく、使用も 1 件なので、高い側の基準が当たる（B2・B13）。Karl Fogel 氏 2014-06-30（NASA の審査の委員会報告）*"In general, I worry about building trademark-law-type provisions into licenses that are really about copyright"* —— ACD-1.4 の §11.3 と §11.4 は、法が既に定める限界（偽りの表示・他人の権利）を条で述べており、告知の形であっても「要るのか」が長さの論点として向く。**逆側**: Brian Behlendorf 氏 2004-09-28 は、Apache が商標の文を禁止から告知（*"nothing gives you the right to use"*）に変えた後、*"So far, we have not noticed a change in behavior of licensees due to the change of license"* と書いた。ACD-1.4 の §11.1 はその告知の形に在る。Perens 氏 2010-04-05 の *"The ultimate purpose of a license is to guide the judge in his or her ruling."* は、条を足して読みの分岐を閉じる作業を支える側に在る（ただし、裁判所の目で読んだのは法律家ではない・B1）。

**2026-11-23 に足した —— 「効果の無い語は置くな」と「条件か否かを書け」は同じ人の文で、ACD の説明の文はその間に在る（`review-readings-6.md` §1.461・portfolio-d7）。** Pamela Chestek 氏 2020-12-26（OIN License）*"If the words aren't meant to have any effect, they shouldn't be there."* —— ACD-1.4 は条の効果を述べ直す文を多く持つ（§11.3・§11.4 の *"states a limit of the Dedication's reach; it is not a condition upon You"*、§16.4 の *"Both provisos are conditions upon distributing the text, not upon any use of the Work"*）。**逆側**: 同じ人が翌年の 2021-06-09（3D Slicer）に問うたのは *"The question was whether the phrase in the 3D license is a condition on the copyright grant or not."* で、条件でなければ書いておけ、という向きである。Lawrence Rosen 氏も同じ日に *"In my license, intentionally, only the licensor makes promises!"* と書き、AFL / OSL は条件でない文を条件でないと明記した。ACD の述べ直しの文は、条件か否かを決める働きを持つときは置き、持たないときは置かない —— この基準で条ごとに当てるのは 1.5 の試作の候補である（5e へ送った）。上の Berkus 氏 2015 と同じ線を、Richard Fontana 氏 2019-05-17（LBNL BSD の旧来の承認）は明文で書いた: *"I believe we have higher standards around open-ish license drafting quality today than we had ~15 years ago"* —— ACD は新しいライセンスとして、高い側の基準で読まれる。

**2026-11-16 に足した —— 撤回不能を繰り返して述べることは「少し冗長」と読まれうる（`review-readings-2.md` §1.260）。** Josh Berkus 氏 2025-08-15 の MIT-I への文（全文と逆側は `review-precedents.md` §1.47）。ACD は撤回不能を §2.2・§3.1・§4.1・§8.1 の語と §10.4 で述べる。語数を減らす候補になるかは 1c の判断（2f の振り分け）。**逆側**: 4 か所はそれぞれ別の権利（献呈・放棄・著作権の許諾・特許の許諾）に付いていて、1 か所にまとめると、どの権利が撤回不能かの読みが割れうる。

**2026-11-18 に足した —— 法的な不確実性を減らし、読みを一意にする試作は、語を足して買う（portfolio-30・数は草案の冒頭の *"This draft:"* の語数 —— `sync_stated_counts.py` が実測で揃える —— を commit ごとに読んだ）。** 2026-11-16 の T81 の前の草案は 5520 語、2026-11-18 の main（T96 の後）は 5623 語で、2 日の試作（T81〜T96）で +103 語。各試作の増減（その commit の前後の草案の冒頭の語数の差・2026-11-18 に測った）: 足した側 —— T82（§14.1・法が除外を許さない故意・重過失・人身の責任の除外・反例での直しを含め +29）、T90 と T91（§5.1 の不当利得、§5.2 末段の同梱した写し・2 巡を含め合わせて +30）、T94（§8.1・§8.4・4 法域の特許法の行為の語・+6 —— 申出を裸の *offer* にして短くした）。削った側 —— T92 と T93（§15.3 の第 2 文を外す −21 と、§5 の「許すと称する」+8 で、合わせて −13）、T80（§8.4 の閾値の理由・−12）。束 1（T97〜T99・+20）は反例待ちで、この数に入っていない。**読み**: 語の多くは「法域ごとに違う法の語に名指しで当てる」か「割れる読みを 1 つに閉じる」ために足され、どれも CHANGELIST の行が理由と逆側を持つ。B3 の上の段（Moen 氏 2015 の「構造が長さを生む」）と同じ向きで、確かさの費用として説明できる。**逆側（重い）**: 長さそのものが審査者の負担で（Fontana 氏 2016 の「複雑すぎる」・上の段）、+103 語は 1.3 → 1.4 の差（5443 → 5623・+180）の半分を超える。一意化の試作が足した語が、新しい割れを持ち込むこともある（T96 の §1.7 は 30 の反例で直した）—— 足す前に、閉じる読みが本当に立つかを反例で当てる手順が、長さの側の歯止めになっている。

## B12 —— class 9（2026-11-07 に 11 から移した）

**steward が 1 人**で、承継の仕組みが無い。**設計変更では解けない**（条文を直しても steward は
増えない）。分類 9（外部証拠）に見えるが、**採用を増やすためにライセンスを歪めない**という
方針に照らすと、**現時点で我々が取れる行動が無い**ため 11 とする。
**採用が自然に増えたときに 9 へ移る。**

**⚠ 2026-09-17 ——「解消方法不明」は、束をほどかずに出した結論だった。**
この項目は **2 つの別の事実**を束ねていた: **(a) steward が 1 人であること**（世界についての事実）と
**(b) 承継の仕組みが無いこと**（**文書についての事実**）。**(b) は条文で扱える。**
1.1 草案の §16.5 が *"the Steward"* を機能で定義し、**その役割が譲渡されうることを条文に置いた**
（先例は EPL-2.0 —— *"may assign the responsibility to serve as the Agreement Steward to a suitable
separate entity"*・SPDX の canonical text で逐語確認）。

**分類は 11 のままにする。** 残っているのは **(a)** で、そこは条文では動かない ——
**「半分が条文の問題だった」を「解消した」と読み替えない。** 承継が*可能*であることと、
**承継先が実在すること**は別であり、後者はいま存在しない。

**⚠ 2026-11-07 ——「解消方法不明」も、出典より不利に書いていた。分類を 9 へ移す。**
残っていた (a) を一次資料へ当てると、リストが恐れてきたのは人数ではなく**支配**だった。

- **信頼が要る場面は名指しされている。** Bradley Kuhn 氏（`license-review` 2018-11-22・SSPL の審査）:
  *"Brendan's comments caused me to realize that OSI really does need to trust the license steward when an
  upgrade clause is in play."* ACD に upgrade 条項は無い。§16.2 は版を名指し、§16.4 は各名前と識別子を 1 つの固定テキストに結ぶので、
  受領者は steward を信頼しなくても固定の本文に依拠でき、新しい版は既に献呈された著作物へ届かない。
- **個人への不信は実際に述べられ、解かれている。** Lawrence Rosen 氏の回想（`license-discuss` 2012-10-03）:
  *"Nobody trusted that I personally (or my heirs) would forever have the good of the community at heart. I agreed
  with them. That was my incentive to write section 16 of those licenses, which declared authorship but disclaimed
  control over changes."* その §16 は、改変を別の名前でなら許し、名前を独占し、既存の著作物の再許諾を封じる形で、
  ACD §16.4 と同じ構造である。AFL-3.0 / OSL-3.0 / NPOSL-3.0 は今も承認済みの一覧に在り、
  本文は *"Copyright © 2005 Lawrence Rosen"* と述べ、本人は 2016 年に *"this license steward (me!)"* と書いている。
- **steward を持たないことも普通である。** 141 本の本文を測ると、*license steward* / *agreement steward* の語を持つものは
  8 本である（語の検索なので床）。Richard Fontana 氏（`license-discuss` 2019-05-31）:
  *"MIT is not the license steward of the MIT license -- there is no license steward"*。
- **連絡の取れない steward の下でも、承認は残っている（2026-11-11 に足した）。** Russell Nelson 氏は 2006-03-11 に *"These licenses are ones for whom we have no good steward contact."* と書き、承認済みの 12 本を挙げた（`license-discuss`・`rounds/2006-03-license-discuss-looking-for-license-stewards-observed.txt`）。そのうち 11 本（BSD-3-Clause・EFL-1.0・EFL-2.0・Frameworx-1.0・Motosoto・Naumen・NGPL・QPL-1.0・RSCPL・VSL-1.0・Zlib）は、2026-11-04 に SPDX の `isOsiApproved` で数えた 141 本（`gap-census.md`）に今も在る。CVW だけが無く、理由は確かめていない。**逆側**: これは承認の後の連絡先の話で、承認の時に steward を見るという Kuhn 氏の見解は動かない。141 本は SPDX の印で、OSI の一覧そのものではない。
- **上の版を外す選択も退けられていない。** Piana 氏（`license-review` 2025-05-29・Tiwaz）:
  *"a legitimate choice and I won't fuss about it. There are different views on this kind of provisions."*

**逆側を同じ重さで書く。**

- **steward が誰かは見られる。** 同じ Kuhn 氏の同じ 1 通: *"I \*do\* think OSI should consider who the license steward is
  and what their motivations are as part of the license approval process."* 氏の見解であって OSI の声明ではないが、
  upgrade 条項に限っていない。
- **版を動かせない設計には費用がある。** Rob Landley 氏（`license-review` 2025-07-19）:
  *"Given that the law tends to change every few years even in individual jurisdictions, walling that option off for
  anything nontrivial seems a bit weird."* Brendan Hickey 氏（同 2019-01）: *"Use a well known open license with an upgrade
  clause if you're concerned about novel legal developments."* ACD の答えは新しい版と再適用で、すでに配られた著作物には届かない。
- **Rosen 氏は弁護士で、回想は 1 人の記憶である。** 同じ解き方が個人の非弁護士にも効くとは言えない。
  Piana 氏は「個人であること」を理由に下げないでほしいという提出者への返信で、審査の延期を勧めている（2026-06-19）。
- **§16.4 は Steward に新しい版の権利を残す。** OSL の §16 との差は 2 点で、OSL は改変ライセンスに OSI の承認なしで
  open source と言うなと足し、ACD は Steward の版の出し方を書く。役割の非対称は `submission-osd.md` §3b-i に在る。
- **承継先は実在しない。** §16.5 は譲渡を許すが、譲渡の前に steward が欠ければ、本文では役割は空く（§2.8 の承継人は Work についての文で、§16.6 が §16.4 / §16.5 を Work の条項から外す）。一般の承継法が別の結果を与えるかは未確認である。その場合に止まるのは
  その名前での新しい版だけで、著作物の許諾は何も変わらない（§10.4）。別の名前での改変も止まらない。

**分類を 9 に移す理由。** 解き方は分かっている —— 引き受ける人を見つけて §16.5 で指名することである。
必要なのは第三者の同意で、それは分類 9 の形である。**steward が 1 人である事実は変わっていない。**
**「解き方が分かった」を「解けた」と読まない。**

**一般形**: **1 つの項目を確かめて、項目が指す集合について結論していた。**
`BLIND-SPOTS.md` が「集合の 1 つを確かめて集合について結論した」と呼んでいる形の、register 側の実例である。

---


**2026-11-15 に足した —— 許可が特定の主体に連絡が取れることに依れば、その主体が消えたとき許可も危うくなる、と理事が書いた。** Simon Phipps 氏 2010-10（`license-review`・netX の審査）*"Any requirement that a specifically identified entity (e.g. the original author) must receive notification in any form (including a code submission) in order for the license conditions to be satisfied creates an onerous accumulating burden"*、*"may invalidate the license grant if the entity becomes unreachable or ceases to exist"*、*"would therefore constitute a failure to satisfy the OSD"*（*"I believe this represents the prior conclusions of OSI in the matter"* とも・`review-readings-2.md` §1.236・portfolio-2f）。**B12 の有利な面**: ACD の許可は Dedicator にも Steward にも連絡が取れることに依らない（§2.3・§10.1・§10.2）。Steward が要るのは §16.4 の、本文を名前の下で改変して配ることの扱いだけで、Steward が消えても Work の利用者の許可は何も変わらない（§16.6）。**逆側**: Steward が消えれば新しい版を出す者がいなくなる（承継先が未定のまま）。それは Work の許可の問題ではなく、ライセンスの本文の保守の問題である。同じ審査で Bruce Perens 氏は提出者に承認済みのものを探すよう勧めた —— B10 の同じ線の文は 2010 年まで遡る。

**2026-11-15 —— 2f の §1.242 で B12 の材料として挙がったものを当てた。判断は動かない。** John Cowan 氏 2003-05-07 *"if the author transfers the copyright to a corporation whose chartered purpose is to maintain the license, then the corporation would be unable to revoke it through lack of appropriate powers."* —— これは著作権者（Dedicator）の撤回を防ぐ形で、steward の承継（この項目）ではない。ACD はこの形を取らず、撤回には §2.2・§2.5・§3.1 で答える（`QUESTIONS-FOR-COUNSEL.md` 問 1 (i)）。**逆側**: 個人の Dedicator の撤回を構造で防ぐ手段が ACD に無いことは、この形と比べると見える。それは B12 ではなく問 1 (i) の側の論点である。

## 更新規約

- 新しい問題は**必ずこの表へ入れ、分類を付ける**。分類が付かないものはボトルネックではなく
  `against.md` の不利な事実に留める。
- **詳細分析**（なぜ承認上の問題か / 事実・推論・予測の別 / 最小の解消方法 / より大きな再設計 /
  失うもの / 残る gap / 副作用 / 新たな反論 / 外部確認の要否）は当該項目の節に書く。表は索引。
- **revision のたびに集計を比較する。** 減っていなければ revision 自体を疑う。

