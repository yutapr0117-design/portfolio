---
file: LICENSES/REVIEWERS.md
audience: OSI license-discuss / license-review participants, licence reviewers, anyone arriving from the mailing list
last-updated: 2026-11-07
canonical-ref: LICENSES/ACD-1.0.txt (the text posted) / LICENSES/ACD-1.3.txt (the frozen successor this repository applies since 2026-10-25) / LICENSES/FROZEN.md (freeze + venue, single source) / LICENSES/rounds/2026-08-26-license-discuss-sent.txt (what was actually sent) / LICENSES/ACD-1.0.submission.md (the packet prepared for license-review)
---

# Reviewing ACD — start here

## The short path, and what it costs you

**You are a volunteer. Nothing here is required reading.** Measured 2026-11-09, the analysis in
this directory — everything except `rounds/` — is **407,629 words**, **83 times the licence**, and
more than that in fact, because Japanese is not space-delimited. `rounds/` holds the primary
sources verbatim so that every quotation can be checked against what was actually sent; **nobody
is asked to read it.** The whole of it exists so that a claim we make can be checked, **not so
that it must be**. *(Re-measure: `git ls-files -z LICENSES ':!LICENSES/rounds' | xargs -0 cat | wc -w`.)*

**If you read three things you have checked the parts that decide the question:**

| | words | why |
| :-- | --: | :-- |
| [`ACD-1.0.txt`](ACD-1.0.txt) | **4,896** | the licence. Nothing outside it fixes it |
| the two facts **#1 and #4** in [`ACD-1.0.against.md`](ACD-1.0.against.md) | ~220 | **no lawyer has read this text**, and **the only project using it is the author's**. These are the strongest points against it. Neither is one of the eight published criteria, and the Licensing Committee's chair has called legal review *"not a blocker"*, but a reviewer may weigh both |
| [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md) | **4,326** | every objection we found on these lists in 24 months, and whether it lands. The first table is the part that counts |

**≈ 9,443 words** *(`wc -w`, 2026-11-11.)* **What you give up by stopping there**: the clause-by-clause reasoning, the
jurisdiction analysis, and the archive measurements — **all of which are evidence for claims,
not claims themselves.** The four commands below check the licence text without trusting any
of it.

---

This page is in English because the discussion is. Most of the supporting analysis in this
directory is written in Japanese; this page tells you what each document contains so you can
decide what is worth translating, and gives you the commands to check the claims yourself.

## In one screen

- **What it is.** A dedication of copyright and neighbouring rights to the public, **plus a
  licence granted independently of it** (§4.4), for works meant to be learned from.
- **Why it should be approved.** OSI's own FAQ gives two reasons a public-domain dedication falls
  short: it is *"still not a license"*, and CC0's *"most serious"* concern was its patent exclusion.
  An article on OSI's site named the fix in 2017: *"disclaim ownership for the jurisdictions where
  that is possible, and then grant a copyright license"*. ACD has both parts (§3, §4), its licence
  applying everywhere, and grants patents (§8). It imposes no condition (§10.1), so one of the two
  grounds on which submissions fail has nothing to attach to. Each of the eight published criteria has an answer in the
  text (below), and it fills a gap the approved list leaves open.
- **The gap it claims, in one sentence.** **No OSI-approved instrument grants all three of these
  at once**: (i) a **patent licence that survives the transformation of the work into a model** and
  its outputs; (ii) **no condition on you at all**; and (iii) a grant that expressly reaches
  **non-copyright rights in data** — the EU sui generis database right and its own verbs,
  *extraction* and *re-utilisation*.
  **(i) and (ii) differ in effect; (iii) differs in what is stated, not in what an
  unrestricted permission may already reach.**
- **Measured over the whole approved list.** Of the **141 licences
  SPDX marks OSI-approved and not deprecated, exactly three impose no condition on the licensee** —
  **0BSD, MIT-0 and the Unlicense** — and **none of those three contains the word *patent* at
  all**. Seven extend a patent grant beyond the work itself, and **all seven carry a condition**
  ([`ACD-1.0.gap-measurements.md`](ACD-1.0.gap-measurements.md) §1.97, §1.133).
- **What this does not claim.** That existing licences forbid training: a licence that allows
  everything allows training, and MIT's *"deal in the Software without restriction"* may well
  reach these rights too. §6.1, §7 and §9 state expressly what a broad permission may already
  give, so **they are not grounds of uniqueness** (§1.134).
- **Nearest approved licences.** Closest in effect to the Unlicense, MIT-0 and 0BSD (and to CC0,
  which is **not** OSI-approved), and in patent terms to UPL-1.0, BlueOak-1.0.0 and
  BSD-2-Clause-Patent, which already combine a permissive grant with an express patent grant under
  one notice condition — **against those three it adds less**: the difference is that condition, not
  the patent grant ([`submission-reference.md`](ACD-1.0.submission-reference.md) §2).
- **The two weaknesses, first.** **No lawyer has read it**, and **it has one adopter — this
  repository**. Neither is repaired here. Neither is a published criterion: the chair called legal
  review *"not a blocker"*, and a Committee rationale (2020) calls non-use *"not a basis for
  rejection that the OSI has applied in the past"*.
- **Anyone can adopt it.** No project names, and nothing in the text to edit.
- **If you read one more thing**, read [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md):
  every objection raised on the lists, and whether it lands.

## Which text you are looking at

**There are four frozen texts, and they are frozen for different reasons.** *(2026-10-29: this table said "two" and named 1.0 as the applied licence after 1.2 and 1.3 had been frozen; corrected.)*

| | |
| :-- | :-- |
| [`ACD-1.0.txt`](ACD-1.0.txt) | **The text posted to `license-discuss` on 2026-08-26.** Frozen since 2026-08-24 so that the text under discussion does not move. This repository applied it until 2026-10-25. |
| [`ACD-1.1.txt`](ACD-1.1.txt) | **The successor, frozen 2026-09-17.** When it was frozen it closed nineteen of the twenty-one defects then recorded in [`ACD-1.0.errata.md`](ACD-1.0.errata.md); the list has kept growing since, and each entry says which version addresses it. It has **not** been submitted to `license-review` and is **not** applied to this repository. |
| [`ACD-1.2.txt`](ACD-1.2.txt) | **The second successor, frozen 2026-10-17.** Its own header says what it is. It has **not** been submitted to `license-review` and is **not** applied to this repository. |
| [`ACD-1.3.txt`](ACD-1.3.txt) | **ACD-1.3, the third successor, frozen 2026-10-25, and the licence this repository applies from that date** (the root `LICENSE` says so). It has **not** been submitted to `license-review`. |

**Work on the next version happens in [`ACD-1.4-DRAFT.txt`](ACD-1.4-DRAFT.txt)**, so no
frozen text moves while it is being discussed. All four are pinned by SHA-256 in
[`FROZEN.md`](FROZEN.md) and checked in CI; the command to verify that is below.

**Clause numbers do not transfer cleanly between 1.0 and its successors, and this matters when you read the
analysis below, which is written against 1.0.** Measured, not assumed:

- **§2 to §14 — every clause number means the same thing in both texts.** The citations on
  this page (§4.4, §6, §8.4, §9, §10.1) are therefore good for either.
- **§1's definitions were reordered, so four of them changed number.** Matched by defined term:
  1.0's §1.2 *Work* is 1.2's §1.3, §1.3 *Dedicator* is §1.4, §1.4 *You* is §1.6, and §1.6 *Moral
  Rights* is §1.2. **The numbers all exist in both, so nothing dangles — they simply mean
  different things.**
- **§15 and §16 were shortened and renumbered.** 1.0's §15.7 and §15.8 are 1.2's §15.3 and
  §15.4; 1.0's §15.2 has no counterpart in 1.1 but its three rules of construction were
  restored at 1.2's §15.5 (errata E24); **1.0's §15.3 likewise has no counterpart in 1.1 and
  is restored word for word at 1.2's §15.6** (errata E25); 1.0's §16.5 (translations) was
  absorbed into 1.2's §16.4, and **1.2's §16.5 is a different clause — the definition of the
  Steward**.
  **A citation to §1, §15 or §16 has to name the version.** The full map, citation by citation,
  is in [`ACD-1.2-CHANGELIST.md`](ACD-1.2-CHANGELIST.md).

## Status

**Posted to `license-discuss` and received. No responses in the archive when last read, 2026-11-11 01:17 UTC.** (The October archives of both lists were unchanged; the November archive pages returned 404, which says nothing either way about posts — see `OSI-EVENTS-2026-10.md`.) That list is for general
discussion — it is **not** the approval venue. Nothing has been submitted to `license-review`,
and nothing has been submitted to SPDX. SPDX asks for substantial real-world use, this work has
one adopter, and we are not submitting something that does not meet the stated bar.

**What will be submitted is a later version, not 1.0.** The sequence — post to `license-discuss`,
collect what the list says, fold it into a revised version, submit **that** to `license-review`,
and repeat on the review comments — is the plan the owner has held from the outset (his direct
confirmation, 2026-09-09). The owner sent ACD-1.1 to `license-discuss` on 2026-09-17, and **that
message was rejected by moderation** (`ACD-1.0.against.md` #215), so the list has not received
that text. Work on the next version happens in `ACD-1.4-DRAFT.txt`, so no frozen text moves.
Freezing a text is a promise about its bytes, not a statement about which version a project uses.

**AI drafting and the lists.** On 2026-09-09 the OSI Moderators posted to both lists that they
*"will reject posts where we suspect that an AI has been responsible for all or most of a
message"* and that the lists *"are being used as a proof-of-concept to demonstrate that an AI
system can autonomously engage and even draft an open source license for review"*. No name is
given. **Two days earlier a moderator had put the same question to us directly and by name, in
five questions, and the steward answered all five the same day**; the correspondence continued
off-list. A third party's private mail does not belong in a public repository, so `rounds/`
records those exchanges as dated stubs only (`rounds/README.md`, exception section; `against.md`
#217). **We do not assert that the notice is about us alone**, but the description fits this
project, whose licence was drafted by an AI agent (disclosed in `ACD-1.0.submission.md` §E.1
since before the text was posted). Nothing was sent to either list between 2026-09-09 and
2026-09-17, when posting resumed with a short ACD-1.1 discussion request in the owner's own words.
**He states that the human decides the direction and that he checks and sends the messages
himself** — the notice rejects posts made *"without careful review from the author"*, and that is
the line it draws. **The policy decision belongs to OSI as an organisation.** The verbatim notices
are in `rounds/`; the analysis is `against.md` #119 and `ACD-OSI-BOTTLENECKS.md` B14. **We are not
reducing the disclosure in response.**

The text is **frozen** while this is open. `LICENSES/FROZEN.md` exists to say so, and
**Check 453 in CI pins the SHA-256 of nine files** — the three submitted ones
(`ACD-1.0.txt`, `ACD-1.0.spdx.xml`, `ACD-1.0.machine.json`) and two for each of the
**frozen successors** (`ACD-1.1.txt`, `ACD-1.1.machine.json`, `ACD-1.2.txt`, `ACD-1.2.machine.json`, `ACD-1.3.txt`, `ACD-1.3.machine.json`), none of them
submitted for approval (ACD-1.3 is the one this repository applies) — so that an accidental edit fails the build rather than
silently changing the text you are reading. If you find a defect in the text, it will be **reported, not quietly
patched** — changing the wording underneath a live discussion would make your review of it
meaningless.

## The case, and the strongest thing against each part of it

Nothing here is new; it is the argument from
[`ACD-1.0.submission-reference.md`](ACD-1.0.submission-reference.md) §1–§4 compressed, with the best counter to each
line placed beside it rather than further down. **The adverse record is the longer document, and
nothing in it is summarised away** — this is only a map of where the argument runs.

| The claim | The strongest thing against it |
|---|---|
| **The gap is real**: no approved licence does all three of the things stated in "In one screen" above — grant patents that name models and outputs (§8.4), impose no condition (§10.1), and reach the sui generis database right with its own verbs (§7.2). On top of these it states expressly what others leave unsaid about training and text-and-data-mining (§6), and it declines to presume that rights subsist in machine-generated material (§9) — which grants nothing new today, but is one of the three differences the next column says an amendment of the incumbents cannot close. Each limb alone has neighbours, as the next column says | **Four of the seven distinguishing features close if the incumbents amend** — and we say which four ([`comparison.md`](ACD-1.0.comparison.md) §1.35). The case then rests on the remaining three. **And the patent limb is narrower than it sounds**: CERN-OHL-P-2.0 grants patents over *Products* — *"any … work … arising from the … processing of Covered Source"* — which can be read to reach a trained model ([`submission-reference.md`](ACD-1.0.submission-reference.md) §2, [`gap-census.md`](ACD-1.0.gap-census.md)). What remains is naming the artefact, and the combination: that reach with no condition and no termination, which no approved licence has (CERN-OHL-P-2.0 conditions conveying a Product in §4 and can end in §6.2; [`gap-measurements.md`](ACD-1.0.gap-measurements.md) §1.133). **We do not claim a difference in claim scope**: CERN-OHL-P-2.0 §6.1 grants claims *"necessarily infringed by exercising rights under the Covered Source as Conveyed"*, and if that includes making and using Products it is close to the limit §8.4 has carried since 1.1 (in 1.1 to 1.3: *"only claims whose infringement depends upon the use of the Work"*; the 1.4 draft rewrites that limit, #282). A combination is also what Josh Berkus answered on this list with *"It's not the goal of the OSI to have licenses for every possible combination of conditions"* (#276, said of another proposal), and that breadth is a cost (#16). **In legal effect, much of the first and third limbs is statement rather than new permission**: §6.1 states what permissive licences already allow (§6.5 says so itself), and §9 asserts no right rather than granting one. What §6 adds in effect is §6.2–§6.3, on the Dedicator's own reservations |
| **It is reviewable**: §3 surrenders, §4 grants a licence *independently* (§4.4), so a reader never has to decide whether the surrender worked | **No court has characterised this construction**, in any jurisdiction (#3), and **no submission of this shape has been approved since 2020** (#87). A dedication taken alone is not approvable, and the escape is untested |
| **It imposes nothing**: §10.1 and §4.3 attach no condition, so no obligation can fire in any delivery mode — the failure that condition-bearing instruments meet in hosted deployment | **The same structure weakens the warranty disclaimer** (#41) and forecloses defensive patent termination (#46). Both costs fall on the adopter, and both are deliberate |
| **Anyone can adopt it**: zero project names, no placeholders in the clauses (one blank in §16.1's notice template), no editing of the licence text required — verifiable with the commands below | **One adopter: this repository** (#4). Reusability is a structural property; adoption is a social one, and only the first is shown |

**The published standard for new licences, item by item.** Each line is our answer. Whether it is
enough is yours to judge.

| The standard asks | ACD's answer |
|---|---|
| *"reusable"*, by any licensor *"without changing the terms"* | §16.1 and §16.3: no project names, and the one blank goes in the adopter's own notice |
| No terms that *"structurally put the licensor in a more favored position"* | §10.1 puts no condition on You, and the promises run from the Dedicator (§5, §8.6, §12). §13 and §14 do protect the Dedicator, as approved licences do, and §16.4 reserves new versions to the Steward; we have not refuted the wide reading of that (#265, #179) |
| Ambiguity *"must not have a material effect"* | As to the Work, §15.1 sends a doubtful provision to the reading that grants more to You |
| *"grammatically and syntactically clear"* | Yours to judge. It was not drafted by a lawyer |
| *"Every possible variation"* of its application must meet the OSD | An adopter edits no term and chooses no option; only the form of the notice varies (§10.1, §16.1) |
| *"possible to comply with the license on submission"* | There is nothing to comply with (§10.1) |
| *"fill a gap that currently existing licenses do not fill"* | §8.4 and §8.2: see "In one screen" above |
| *"complete license"* | One file, no external references, no overlay |

**What the record already says in its favour.** These are quoted from the lists, the Committee's
rationale documents, the Board's minutes and OSI's site. None of them binds anyone: *"Approval of a license with the same or similar terms in the
past does not bind the OSI"*, and a list message is its author's own view.

| On this point | What was said | Where it meets ACD |
|---|---|---|
| A dedication alone, and CC0 | OSI's FAQ (last modified 2025-01-21): *"even where it is clear what it means, it's still not a license"*; on CC0, *"The most serious of the concerns raised had to do with the effects of clause 4(a)"*, the patent exclusion. | §4 is a licence and §8 grants patents. The same FAQ says *"rather than try to waive copyright altogether"*, which is §3, and values attribution, which §10.2 gives up |
| What gets reviewed in a dedication | Lawrence Rosen, 2011-04-18, on CC0: *"OSI could analyze CC0 for its license fallback terms, but not as a public domain dedication."* Richard Fontana, 2011-09-07: *"OSI's main business has been certifying particular legal documents, and there simply is no standard one in the sphere that's been considered (justifiably or not) "public domain"."* | §4 is a licence on its own footing (§4.4), so there is a licence to review. The same message calls CC0's silence on patents troubling, which §8 answers |
| Patents | Josh Berkus, on OSI's blog, 2023-10-03: *"provisions like patent grants have been shown to be necessary"*. McCoy Smith, a Licensing Committee member, on OSI's blog, 2025-12-04: CC0 is *"perhaps the best example of a comprehensive effort to dedicate content to the public domain"*, but its patent disclaimer raised concerns; *"well-crafted explicit patent license grants in Open Source licenses (with or without defensive termination provisions) go a long way to reducing the risks"* Bruce Perens, as OSI's standards chair, 2018-11-09: *"We assert that the OSD terms apply to patents as well as copyright."* | §8 is an express grant and §8.2 has no defensive termination. The same article calls Apache-2.0's clause *"a form of mutual patent peace"*, Berkus goes on *"We've also learned the value of non-proliferation"*, and neither is a decision |
| A patent grant beyond the work | Lawrence Rosen, 2014-04-15, in the UPL review: no provision of the OSD requires a patent licence *"broader than for the specific software work licensed by its copyright license"*; licences that reach further do so *"to be more generous than the OSD requires."* The Board approved UPL, whose grant also reaches listed *"Larger Works"*, on 2015-02-04: *"Board agreed the UPL is OSD compliant"* | So §8.4's reach to models is neither required nor barred. Richard Fontana said UPL's breadth *"goes way beyond to the opposite extreme"*, and before approval its grant was narrowed to the unmodified Software and the listed works. Henrik Ingo named *"the surprise element"* for contributors (#313). In the Blue Oak review, approved in 2024, Carlo Piana answered the same worry: *"those holding a patent portfolio and not wishing to dilute it in a non-copyleft license understand the consequences of using such license"* |
| Surrender plus licence | An article on OSI's site, 2017: *"A solution would be"* to *"disclaim ownership for the jurisdictions where that is possible, and then grant a copyright license that has the same practical effect"*; CC0 stalled *"during a complex discussion about patent rights"* | §3 and §4 are those two parts, §4 is not limited to those jurisdictions (§4.4), and §8 grants patents. The article is one author's, not a decision, and ends by recommending MIT |
| Liability, in the public domain | The same FAQ: *"we don't know how or whether the author would be protected from liability for software released into the public domain"* | §13 and §14 |
| Liability, in a dedication | McCoy Smith, 2016-08-16, of CC0: *"I believe that to be an effective waiver of liability, despite the fact that there is not copyright rights being conveyed."* | §13 and §14. Richard Fontana read CC0 differently in 2017: *"CC0 does not have a limitation of liability provision as far as I can tell"*; ACD has both a warranty disclaimer and a limitation |
| Why CC0 stopped | Board minutes, 2012-03-07: *"Recommend disapprove, due to clause 4a"*. A straw poll that month went 13 to 8 against approval; all 13 gave the patent exclusion among their reasons and none gave the structure of waiver plus licence (our count, `rounds/2012-03-license-review-cc0-straw-poll-observed-1of2.txt`). One of the 13, Chris DiBona: *"I don't think that any new licenses should be approved unless they include patent clauses"*. Richard Fontana, who raised the point, 2019: *"I was not troubled by the idea of approval of CC0 as such."* Fedora dropped CC0 for code in 2022 and still allows the Unlicense: *"licenses that preclude any form of patent licensing or patent forbearance cannot be considered FOSS"* (Fontana, as LWN quotes him). During the review Lawrence Rosen, 2012-02: *"There is nothing we have identified about the CC0 license that comes close to violating any of the provisions of the OSD."* | §8 replaces the exclusion with a grant. No review has tested that form. Russ Nelson objected to it (`ACD-1.0.objection-map.md`), CC0's academic users wanted the exclusion (*"the patent exception is important to them"*), and the replacement Fontana recommended, MIT-0, says nothing of patents (#290) |
| The word "dedication" | Karl Fogel, 2012-01-02: *"The fact that one is called a "license" and the other is called a "dedication" does not lessen their essential similarity"*, and of such promises, *"Those sorts of promises are what the OSI evaluates and sometimes approves."* | The name. He adds: *"We could decide, for other reasons, not to evaluate any PD dedications."* |
| No conditions | Board minutes, 2015-10-14, on the licence now called 0BSD, approved 8 to 0: *"a license with no conditions"*, *"Cannot be argued to violate OSD"*. Richard Fontana, 2015-11-12: *"the OSI obtained outside legal counsel concerning the legal and policy issues raised by 'ultra-permissive' licenses"* | §10.1, including no notice. The same minutes ask *"is it really going to be used?"*. The advice is not public, so we cannot say it was favourable or that it reaches ACD |
| A dedication with a licence beside it | Carlo Piana, 2024-12-18: *"I have nothing against using a PD dedication and a license by way of backstop"*, *"I actually advise to use both in the admittedly rare case I am asked."* McCoy Smith, same day: having both is *"not necessarily fatal"* if the relation is stated clearly | §3 and §4, and §4.4 states the relation |
| A dedication with a patent promise | Karl Fogel, 2014-05-04: *"maybe we wouldn't certify PD itself for software works, but would certify PD *when accompanied by* a particular patent non-assertion text"*, adding *"it's more complex than that"*. Bruce Perens, 2012-02-26, on what a public-domain text would need: *"a public domain declaration coupled with a covenant not-to-sue that extends to the patent claims of the dedicator that are necessary to utilize the work as it was dedicated. And a warranty disclaimer to protect the donor."* Gervase Markham, 2017-02-28: *"if the scheme had a patent grant accompanying the CC-0 license, that might solve both of these issues in one go and lead to something very, very good."* McCoy Smith, 2016-08-16: *"[although CC0 with a plug-in patent grant might work....]"* Richard Fontana, writing from opensource.org, 2016-12-13: *"If the US government standardizes on some particular explicit patent language to use with CC0 I would welcome OSI review of that."* | §3 with §8.6, and §13. Perens began by doubting any *"benefit"* over BSD and ended *"It ends up not being shorter nor simpler."* His patent scope stops at the work, and §8.4 goes further (#300, #305). Smith added in 2017 that his plug-in *"isn't OSI approved (nor would it likely ever be as it's not an independent license)"*; ACD is one text |
| Every path | Russ Nelson, 2009-05-28: *"all the possible paths through the license terminate in acceptable terms under the OSD"*. John Cowan answered with a path ending *"Otherwise: no license."* | §4.4: whether or not §3 takes effect, the §4 licence stands, so no path ends without one. Said of discrimination under OSD 5 |
| The need | Christopher Sean Morrison, 2017-10-26: *"so many federal agencies moving into open source, commensurately searching the legal landscape for something close to public domain yet still addressing indemnification and contributor patent grants"*. A talk hosted on OSI's site, 2025, on existing licences and training data: *"Unclear how attribution requirements transfer through the AI training lifecycle"*. Clark C. Evans, in the review of CC0, 2012-02-25: *"an instrument that is succinct, covers patents as well as copyrights, is both a dedication and fallback doesn't exist."* | §3, §2.6 and §8, and §10.2 asks for no attribution. These are stated needs, not adoptions. Morrison goes on: *"All leading to proliferation"*, the talk says *"A one-size-fits-all approach may not work"*, and ACD is not succinct. Mark Radcliffe, as OSI's outside General Counsel, 2016: *"the drafting of a new "open source" license requires strong reasons."* (#314) |
| Burdens on the licensee | Pamela Chestek, 2025-03-02, on ModelGo: *"Imposing too many burdens and obligations on the licensee means that benefits of the open source ecosystem won't be realized."* The same day, in her personal capacity: licences impose requirements *"only to the extent they assure that the licensor receives the benefit that is their motive for putting software under an open source license and to protect the licensor from harm"*. Carlo Piana, 2025-03-03: *"The output of a program (and of an AI system/model alike) should not be subject matter controlled by the maker of them."* | §10.1 imposes none, and §6.4 leaves outputs free |
| One steward | Bradley Kuhn, 2018: *"OSI really does need to trust the license steward when an upgrade clause is in play"*. Lawrence Rosen, 2012, on distrust of him personally: section 16 of AFL and OSL *"declared authorship but disclaimed control over changes"* | ACD has no upgrade clause, and §16.4 has the same shape as that section 16. The steward keeps new versions under the name, and no successor is named |
| Use | The Committee's rationale for MIT-0, which the Board approved in 2020: *"this is not a basis for rejection that the OSI has applied in the past (and the OSI has historically approved newly drafted licenses not yet in use)"*. For Jam, 2021: *"to date, OSI has not used the number of projects adopting a license as a factor"*. Richard Fontana's report on 0BSD, 2015: *"Approval, or else OSI to adopt some formal maturity/real-world-use factor"*; the Board approved it 8 to 0 | All speak of the past, and 0BSD reused an existing text. Chestek in 2026: *"less inclined to approve a license that doesn't have a track record"*, and the later records join non-use to duplication. Josh Berkus, 2020: *"technically OSS but not really needed"* (#294), and in 2014, on UPL: *"I'm going to vote against any licence which the submitter doesn't intend to actually use to distribute software"*. The Board's minute approving UPL names *"Oracle intends to release software soon"* (#312) |
| Subject matter | The Committee's rationale for CERN-OHL, 2021: *"Although software is not the primary use case for the license ... they are written such that they can be used for software, so they are appropriate for the OSI's review"*. Stefano Maffulli, OSI's Executive Director, 2024-09-01: documents *"may apply, not just to copyrighted software, but to non-software artifacts like datasets, documentation, and model parameters"* | §1.2 opens with source code and object code, and the Mulan definition refused in 2023 had no software in it. §1.2 is wider than CERN's scope, and the statement predates that refusal |
| New instruments for AI | Pamela Chestek as chair, 2024-09-10: *"it is going to take some creativity"*, *"This area needs room to develop, which may not happen if the OSI dictates what it believes the correct approach is, including whether that is a single license for all components or separate licenses for different components"*, and documents *"may assure the necessary rights through the use of legal mechanisms other than a license"* | §3, §4 and §1.2. Said of OSAID terms in 2024, and Richard Fontana's later objection to a single instrument stands |
| Refusal | The Board, 2025-07-18: *"a license should be rejected only if it violates the OSD"* | It has not been said to violate the OSD. The same minutes allow a licence to stay unapproved (see `ACD-1.0.objection-map.md`). The one such hold on record, on Tiwaz in 2025, lifts when *"one or more projects begin using this license or express an interest in doing so"* |
| Legal review | Pamela Chestek as chair, 2024-12-18: *"we do not require review by a lawyer, only recommend it. That is not a blocker."* Carlo Piana, who had written the opposite that morning, withdrew it the same day: *"bad choice of words on my side"*. Richard Fontana, 2013: *"the OSI will be rewarding the represented and punishing the unrepresented"*. McCoy Smith, a lawyer, 2019-03-15: *"Drafting or review by a lawyer is no guarantee of quality"*. The process once required it, *"The analysis should come from a licensed practitioner of the law in your country."*, until it was *"dramatically revised"* in December 2007, and today it asks for a description (`ACD-1.0.review-rules.md` §1.141, in Japanese) | It is still our largest weakness, and the Unlicense did pass with lawyers' agreement. Members keep asking submitters for one. Chestek, 2026-04-14: *"a license of this complexity needs to be drafted by a professional"* (#291). At least 24 new licences went in saying they had no review, and one is on the list (#297). The review *"is not for workshopping a license"* (#298) |
| No governing-law clause | The Board, approving the Open Logistics License in 2023: *"it does not believe that choice of law provisions are necessary or advisable in open source licenses"* | §15.7 names no law (§15.3 from 1.1) |
| Proliferation | Board minutes, 2007-11-07, on SimPL, which allows relicensing under the GPL: *"it does not create a licensing dead-end and thus does not exacerbate the negative aspects of licensing proliferation"*. Scott Peterson of HP, 2005-04: separate pools of code are *"an impediment that is not created by proliferation of non-copyleft licenses."* | §4.5: the Work may go out under any terms. One decision, nineteen years ago. Peterson's message goes on: *"Proliferation of long licenses creates more complexity than proliferation of short licenses."* |
| Vanity | The Board, 2007: *"does not give that argument much weight as long as the license is reusable"*. Pamela Chestek as chair, 2023-01-27, of the working group behind today's criteria: *"There are some "unwritten rules" that we discussed but didn't adopt, like the "no vanity license" philosophy."* | §16.3, and the commands below. The word is still used (`ACD-1.0.objection-map.md`) |
| AI and ML | The Board, 2025-07-18: *"When licenses aimed at AI/ML projects are approved"*, and such a licence is reviewed against the OSD and the standard criteria. OSI's page of questions on the Open Source AI Definition, on parameters: *"They may be free by nature, or a license or other legal instrument may be required"*, and *"we require an explicit assertion"* that they are free | ACD is reviewed on those terms, and it gives that assertion without assuming a right subsists (§9.2, §16.3). OSAID is not the approval standard. Pamela Chestek, in a 2025 review of a model licence: *"the attempt to control Output at all is not justified because it's not limited to derivative works"*; §6.4 attaches nothing to outputs. She also warned that *"the vocabulary for AI is fluid and constantly changing"*, and §8.4 names its objects in a closed list |

**What we cannot fix.** No lawyer has read this licence, and none has been
engaged ([`against.md`](ACD-1.0.against.md) #1). The step that resolved the closest precedent —
legal advisors concluding the Unlicense "would most likely be interpreted as a license and that
the license met the OSD" — has no counterpart here (#2). **And the precedent has not been
repeated**: searching the public review tracker's 252 records for this family returns one approval —
the Unlicense, 2020, on a legacy basis we cannot use — and one contemporary attempt, still
unresolved, whose author was told on this list that a waiver of this kind needs a lawyer (#87).
**Those are the three things we cannot fix, and we state them here rather than leave them to be found.**

## What to open first

**Reading order.** If you have ten minutes: the objection map, then the licence. If you are deciding: add what was actually sent, and the errata. **The case against is the full record and the longest document in this directory** — it is where the objection map points, not a substitute for it. Nothing in it is summarised away anywhere else, and **nothing in it will be shortened**: this directory treats a shrinking adverse list as erasure rather than improvement (`REVISION-PROTOCOL.md` §2).

| | File | Note |
|---|---|---|
| **What is blocking approval** | [`ACD-OSI-BOTTLENECKS.md`](ACD-OSI-BOTTLENECKS.md) | **The register. Mostly Japanese; it opens with a full index in English.** Each item says why it is an approval problem, what is fact and what is inference, the smallest resolution, what would be lost, and who can move it — **four are marked highest severity, and none of them is repaired by editing the licence**: no legal review (B1) and one adopter (B2) advance only by submitting and by time; whether the gap justifies a new licence is OSI's call (B10); and the moderators' notice about AI-written posts is for OSI as an organisation to decide (B14). Its summary line is derived from the table by a CI check, so it cannot quietly understate what is left |
| **Which known objections land** | [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md) | **In English.** Every objection **we have found** in the `license-review` / `license-discuss` archives of the last two years **that bears on a public-domain-equivalent or AI-facing instrument**, plus the older statements that decide this submission — found by a subject census plus reading the threads that matched, which is **a floor, not a census of every objection ever raised** (#87). Whether each applies to ACD-1.0, and — for the ones that do not — the clause that answers it. **Objections that land are listed first** |
| The licence itself | [`ACD-1.0.txt`](ACD-1.0.txt) | 597 lines, 16 sections. Plain ASCII, no placeholders in the clauses (one in §16.1's notice template) |
| **What was actually sent** | [`rounds/2026-08-26-license-discuss-sent.txt`](rounds/2026-08-26-license-discuss-sent.txt) | The `license-discuss` post of 2026-08-26, verbatim from the public archive. 5,778 words |
| The packet prepared for `license-review` | [`ACD-1.0.submission.md`](ACD-1.0.submission.md) | English, **not yet sent anywhere**. Gap statement, comparison, OSD conformance, disclosures, and what is deliberately absent |
| **Looking for a specific answer** | [`QUESTION-INDEX.md`](QUESTION-INDEX.md) | 425 worked entries, indexed by the question rather than the filename |
| **The case against** | [`ACD-1.0.against.md`](ACD-1.0.against.md) | **The complete record, and the largest document here — about twenty times the length of the licence.** All 319 adverse facts, written by us. Two have no answer |
| **Which facts have gone stale** | [`AS-OF.md`](AS-OF.md) | Every claim about the outside world, with the date it was last verified |
| **What we would ask a lawyer** | [`QUESTIONS-FOR-COUNSEL.md`](QUESTIONS-FOR-COUNSEL.md) | ACD has had no legal review. Nine questions on which a lawyer's reading would most change the text, ranked by consequence, each answerable on its own |
| **Known defects in the text** | [`ACD-1.0.errata.md`](ACD-1.0.errata.md) | 77 known imprecisions, all unrepaired in 1.0 while the freeze holds, with what the successor does (the Status column is authoritative) |
| Known weaknesses, longer form | [`READY-TO-SUBMIT.md`](READY-TO-SUBMIT.md) | **Mostly Japanese.** Stated by us, before you have to find them |

## Disclosures you should not have to dig for

- **No lawyer was involved.** The licence has had no legal review.
- **The goal was the owner's; the concrete legal design and the text are an AI's.** He decided
  to have a licence of his own and said it should aim at external approval; he gave the goal and
  the top-level direction, and **did not write a legal specification or supply a list of legal
  requirements**. An AI agent generated the concrete legal design and the text and developed it
  further under a standing delegation. **The name ACD-1.0, the generalised instrument and the
  submission material took shape during that delegated work, and he came to know their concrete
  state afterwards.** He read the full text and understood it before sending it. He is the
  Dedicator and the steward and answers for it; **he did not write its clauses**
  (`submission.md` §E.1).
- **One adopter: this repository.** That is the only real-world use.
- These are stated at length in `ACD-1.0.submission-reference.md` §5 and §E.1, not buried.

## Checking the claims yourself

Every structural claim in the submission is meant to be verifiable in one command. A few:

**These commands assume you have the repository.** One line gets it, and nothing here needs a
build or a network beyond that:

```sh
git clone --depth 1 https://github.com/yutapr0117-design/portfolio && cd portfolio
```

**If you only have the attachment from the mailing list, use this instead** — it needs no clone,
and it is the check that matters, because it compares *the bytes you were sent* against the
pinned value rather than against anything this repository asserts about itself:

```sh
shasum -a 256 ACD-1.0.txt
curl -s https://yutapr0117-design.github.io/portfolio/LICENSES/FROZEN.md \
  | grep -E '^[0-9a-f]{64}  LICENSES/ACD-1\.0\.txt$'
# the two digests must be identical; as of 2026-11-02 (first run 2026-09-07) both are
# 924e6a90d05cbc5dd8a400b4e892d7f323581c281d585d55a093d65a997b2d8a
```

```sh
# No project, author, domain or URL appears in the licence body      → expect 0
grep -icE "yokoi|portfolio|github|https?://" LICENSES/ACD-1.0.txt

# Placeholders: only §16.1's notice template, which the adopter fills in
# their own notice — the licence text itself needs no editing            → expect 1
grep -cE "<[^>]+>|\[year\]|\[name\]|YYYY" LICENSES/ACD-1.0.txt

# Section count                                                       → expect 16
grep -cE "^[0-9]+\. [A-Z]" LICENSES/ACD-1.0.txt

# Verify that the text you are reading is the text that is pinned      → 9× OK
grep -E "^[0-9a-f]{64}  " LICENSES/FROZEN.md | shasum -a 256 -c
```

The last one is the important one. `LICENSES/FROZEN.md` records the digests in the same format
`shasum` emits, so the check is a single pipe with no trust in anything this repository says
about itself: if the licence text had been altered since the discussion began, that line would
print `FAILED` instead of `OK`. It currently prints `OK` for all nine files (re-run 2026-11-02, together with the three counts above: 0, 1 and 16).

**The strongest claim can be checked too, and this one needs a network** and Python 3.10 or later:

```sh
python3 .github/scripts/generate_gap_census.py --fetch   # the texts of the approved licences
python3 .github/scripts/measure_patent_reach.py          # the conditions and terminations, quoted
```

The result line reads `# Patent grant reaching beyond the work with no condition found: 0 []`, and the
tool exits 0. A counterexample prints `REVIEW REQUIRED` and exits 1; an incomplete set of texts exits 2. The
tool quotes the condition or termination in each licence it counts; **which licences reach beyond
the work is the census's reading, not something the tool verifies**
([`ACD-1.0.gap-census.md`](ACD-1.0.gap-census.md)). If the SPDX list has moved since the census was
made, the tool stops rather than report a partial count, and the census has to be rebuilt first.

The repository's own CI enforces the rest: that the licence is declared identically across every
published surface, that the counts these documents quote match reality, and that the frozen files
are unchanged. Those are Checks 444, 460 and 453 respectively; `npm run verify` runs them.

## Map of the supporting documents, and which language each is actually in

**Measured, not assumed** (2026-09-05, by counting Japanese vs Latin characters). The earlier
version of this page called all of these "the Japanese documents", which was wrong for four of
them and would have sent a reviewer away from material they can read.

| File | Language | What is in it |
|---|---|---|
| [`ACD-1.0.comparison.md`](ACD-1.0.comparison.md) | **English** | Why the nearest licences do not fit, by family (Unlicense, 0BSD/MIT-0, Apache-2.0, MPL — all OSI-approved — and CC0, which is not) |
| [`ACD-1.0.clause-reference.md`](ACD-1.0.clause-reference.md) | Japanese | All 82 clauses, one line each, with what each is for |
| [`ACD-1.0.jurisdictions.md`](ACD-1.0.jurisdictions.md) | Japanese | Where the questions differ by jurisdiction (JP, DE, FR, US, EU, UK). **Questions, not conclusions** — no legal opinion is offered |
| [`ACD-1.0.faq.md`](ACD-1.0.faq.md) | Mixed; each answer has an English block | Practical questions from the adopter's side (SPDX notation, scanners, explaining it to a legal team, academic use, consumer-law limits) |
| [`ACD-1.0.review-responses.md`](ACD-1.0.review-responses.md) | Mixed; **every answer is given in English**, with Japanese notes on why it is phrased that way | Anticipated objections: the four weaknesses stated first, then OSD clause by clause |
| [`ACD-1.0.review-responses-clauses.md`](ACD-1.0.review-responses-clauses.md) | **English** | Anticipated objections at the clause level |
| [`ACD-1.0.review-responses-boilerplate.md`](ACD-1.0.review-responses-boilerplate.md) | **English** | Anticipated objections to the boilerplate and construction provisions — whether a court will give them the effect they claim |
| [`ACD-1.0.review-responses-meta.md`](ACD-1.0.review-responses-meta.md) | Mixed; answers in English | Objections about the instrument's provenance, name, stewardship, versioning and machine-readability |
| [`ACD-1.0.discussion-log.md`](ACD-1.0.discussion-log.md) | Japanese | Reserved for **actual** feedback once it arrives. Deliberately not filled with guesses |

**The documents a reviewer is most likely to want are already in English**: the objection map, the
adverse case, the errata, this page, the question index, the submission packet, and both of the
anticipated-response files that deal with clauses and with comparison. What is Japanese is mostly
the clause-by-clause reference, the jurisdiction map, the analysis in the register, and
`READY-TO-SUBMIT.md`.

If something you need is only in Japanese and matters to your review, say so on the list and it
will be translated. Nothing here is withheld — the language is an artefact of who wrote it, not
a choice about who should read it.

### The rest of the directory, in one line each

The table above is where to start. It is not the inventory, and until 2026-09-20 this page did
not mention the following files at all — including the register of what we believe stands
between this instrument and approval, which is the most self-critical thing here.

| File | Language | What is in it |
|---|---|---|
| [`ACD-OSI-BOTTLENECKS.md`](ACD-OSI-BOTTLENECKS.md) | Japanese | **The register of what we think blocks approval** — fifteen entries with severity, who can move each, and none marked resolved |
| [`ACD-OSI-BOTTLENECKS-EXTERNAL.md`](ACD-OSI-BOTTLENECKS-EXTERNAL.md) | Japanese | The entries whose answer is not ours to give (legal review, adoption, the gap question, the moderator decision) |
| [`ACD-1.0.review-precedents.md`](ACD-1.0.review-precedents.md) | Japanese, quoting English verbatim | What this list has actually done to submissions of our shape, read from the archives |
| [`ACD-1.0.review-corpus.md`](ACD-1.0.review-corpus.md) | Japanese, quoting English verbatim | Measurements over the archives as a whole, as distinct from readings of single threads |
| [`ACD-1.0.review-rules.md`](ACD-1.0.review-rules.md) | Japanese, quoting English verbatim | The OSI's own published pages, read at source and applied criterion by criterion |
| [`ACD-1.0.board-decisions.md`](ACD-1.0.board-decisions.md) | Japanese, quoting English verbatim | The board's published minutes — where decisions are recorded, which the mailing list does not record |
| [`ACD-1.0.reviewer-positions.md`](ACD-1.0.reviewer-positions.md) / [`ACD-1.0.review-labels.md`](ACD-1.0.review-labels.md) | Japanese | Positions taken by named participants, and the labels this list uses for licences like this one |
| [`AUDIT-LEDGER.md`](AUDIT-LEDGER.md) | Japanese | How each class of claim in this dossier was verified, with the counts and the residue |
| [`BLIND-SPOTS.md`](BLIND-SPOTS.md) | Japanese | The dimensions we have used to look for our own defects, and the ones we have not |
| [`PEER-REVIEW-WATCH.md`](PEER-REVIEW-WATCH.md) | Japanese | Contemporary instruments under review, and what we would change if each is approved, rejected, revised or stalls |
| [`ACD-1.1-CHANGELIST.md`](ACD-1.1-CHANGELIST.md) / [`ACD-1.2-CHANGELIST.md`](ACD-1.2-CHANGELIST.md) / [`ACD-1.3-CHANGELIST.md`](ACD-1.3-CHANGELIST.md) / [`ACD-1.4-CHANGELIST.md`](ACD-1.4-CHANGELIST.md) | Japanese | What each successor changes, and why, one erratum at a time (1.4 is the current draft) |
| [`ACD-1.1-SELF-AUDIT.md`](ACD-1.1-SELF-AUDIT.md) | Japanese | Defects the successor drafts introduce themselves |
| [`ACD-1.4-ADVERSARIAL-TRIAGE.md`](ACD-1.4-ADVERSARIAL-TRIAGE.md) | Japanese | An external adversarial audit of the 1.4 draft (172 points, supplied 2026-11-01), triaged one row at a time: what was already known, what is a deliberate trade, what needs counsel, and what was new and repaired in the draft. **An AI-written review, not a legal review** |
| [`ACD-1.0.dig-2026-09.md`](ACD-1.0.dig-2026-09.md) | Japanese | The record of one archive excavation, kept because the method is reusable |

## What is not being asked for

Approval would mean the licence conforms to the Open Source Definition. It would not mean it is
recommended, popular or preferred. This submission makes no claim to those, and the honest
position is the narrow one.
