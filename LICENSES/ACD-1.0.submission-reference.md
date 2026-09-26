---
file: LICENSES/ACD-1.0.submission-reference.md
audience: OSI license-review participants / licence reviewers / 監査人 / 次のセッションの実装者
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.submission.md (送る文面は §B.0。**これを貼らない**) / LICENSES/ACD-1.0.against.md / LICENSES/AS-OF.md
---

# ACD-1.0 — 提出文の背後にある参考資料（**貼らない**）

**2026-09-09 に `ACD-1.0.submission.md` から切り出した。** 節番号は変えていない
（`§1`〜`§5`）ので、既存の `submission.md §4c` 等の参照は**本書の同じ節へ解決する**。

**なぜ分けたか。** `submission.md` は「**何を送るか**」（§A の要求情報・§B.0 の本文・
§C の SPDX 用文面・§D の送信前チェック・§E の追加開示）で、読み手は**送る人**である。
本書は「**送ったあとに、審査者が具体的な質問をしたときに指し示す先**」で、読み手は**審査者**で
ある。**同じ文書に置くと、送る人が貼ってはいけないものを貼る危険が残る** ——
`submission.md` §B.0 は 3 度にわたり「§1〜§5 を貼るな」と書いていたが、
それは**同居している限り必要な警告**だった。分けたので、その危険は構造的に消える。

**規模の理由もある**: 分割前の `submission.md` は 976 行で advisory (950) を越えていた。
**BLOCKING (1000) に当たってから動くのでは遅い**（`file-size-budget.md` の二層設計）。

---

### B.1a 送り状の代替形（短い header 版・参考）

**Subject:** For Approval: Autonomous Commons Dedication 1.0 (ACD-1.0)

Dear License Review Committee,

I am submitting the **Autonomous Commons Dedication 1.0 (ACD-1.0)** for approval.

**Text:** https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt
**Steward:** Yuta Yokoi
**In use by:** https://github.com/yutapr0117-design/portfolio (the entire repository,
including source, documentation, data and media assets)
**Proposed proliferation category:** I do not ask for a "popular / widely used"
designation. I submit it as a new licence and accept whatever category the committee
considers appropriate on the evidence of use.

---

### 1. Why a new licence is necessary

ACD-1.0 is written for works that are *meant to be learned from* by machines. Three
questions decide whether such a work is safe to build on, and the licences in common use
answer none of them:

1. **Machine learning and text-and-data mining.** Permissive licences are silent.
   Silence is not refusal — Article 4(3) of Directive (EU) 2019/790 requires an *express*
   reservation — but silence is not something an automated consumer can rely on either.
   The question is unsettled in most jurisdictions, and where a reservation mechanism
   exists it can be operated by parties *other than the licensor* (a host, a platform, an
   aggregator) through signals attached to the work. A consumer reading only the licence
   cannot tell. ACD-1.0 Section 6 answers directly: Computational Use is expressly
   permitted (6.1); the licensor makes no reservation and declines to make one (6.2); any
   reservation attached to the work is withdrawn so far as the licensor's own rights reach
   (6.3, bounded by 2.7); and no model, parameter set, weight, embedding or output is
   encumbered (6.4).

2. **Patents.** Public-domain-style instruments have withheld patent rights. That is the
   very clause on which CC0 did not complete OSI review, and the committee's concern at
   the time was that approving it would weaken, not strengthen, the position of users of
   software so released. ACD-1.0 Section 8 grants an express patent licence, states that
   it is subject to no condition and not terminable (8.2), rejects any reading that would
   reserve patent rights (8.3), and **grants a further licence, in its own right, over
   Computational Use and over any model, parameter set, weight, embedding or output
   resulting from it (8.4)**. Section 8.4 is deliberately a grant and not a clarification:
   whether a trained model is "the Work" or a derivative of it is unresolved, and a
   provision that merely avoided doubt would be read down together with the reading it was
   written to correct. Section 8.5 states the limits of the grant honestly, and Section 8.6 adds a
   covenant not to assert, for any jurisdiction in which the patent licence itself is held
   ineffective. Copyright is protected three times over in this instrument (surrender,
   licence, covenant); Section 8.6 gives the patent grant the second footing it would
   otherwise lack, in the manner Section 12.2 uses for moral rights.

3. **Machine-generated material.** It is unsettled whether copyright subsists in it at
   all. Section 9 makes the recipient's permissions independent of that question: the
   licensor asserts no right in such material, the recipient is not required to determine
   which parts are machine-generated, and if a right is later held to subsist, Sections 3
   to 8 and Section 12 apply to it in full.

### 1a. Two other AI-native instruments are already before this list

Stated here because the gap argument above is weaker if it is read as "nobody else is working
on this," which was never true and is not claimed.

**OpenMDW-1.1** (Linux Foundation) and **ModelGo v2** (MG0-2.0 and MG-BY-2.0, National
University of Singapore) are in review. Both are drafted for machine learning model materials:
OpenMDW's subject matter is "one or more machine learning models (including architecture and
parameters); and all related artifacts (including associated data, documentation and software)";
ModelGo's is the Model plus Complementary Materials, with pretraining datasets expressly outside
scope.

**They answer a different question, and for their question they are better.** Theirs is *how do
I license a model?* If that is the question, OpenMDW is the better instrument today — it names
the artefacts a model release consists of, it has an institutional steward, and it has been
through counsel. ACD-1.0's question is *how do I release any work so that machine processing of
it is unencumbered?*, and it reaches models only because a model is a work.

**Where their coverage exceeds ours.** OpenMDW licenses **trade secret rights** expressly;
ACD-1.0's Covered Rights (§1.5) do not reach them. For weights protected by confidentiality
rather than copyright, that is a gap on our side. (Whether licensing a trade secret has legal
effect was itself questioned in OpenMDW's review, so the point is contested, not settled.)

**Where ours differs.** ACD-1.0 imposes no condition at all, where OpenMDW requires the agreement
and notices to be retained and MG-BY requires attribution and a modification notice. ACD-1.0 has
no patent retaliation, where OpenMDW and MG-BY terminate on suit — deliberate, since a
termination trigger is a condition, but many reviewers regard defensive termination as a feature.
And ModelGo **excludes** models derived by distillation or synthetic data generation from its
Derivative Materials, where ACD-1.0 §8.4 grants toward "any model, parameter set, weight,
embedding, or output" of Computational Use. That last axis is where the three are genuinely in
tension rather than merely adjacent.

**The proliferation question this raises.** Not "is ACD-1.0 different from OpenMDW and ModelGo"
— it is, in subject matter and in conditions. It is whether the adjacent question is worth a
separate instrument when two others are already in flight for the neighbouring one. That is a
judgement for the list. `ACD-1.0.comparison.md` §1.5 sets out the full comparison, and
`ACD-1.0.against.md` #28–#31 record what this comparison costs our case.

### 1c. Section 6 is a statement about my own rights, not a policy position

Raised here because the same ground is being contested in another review as this is written, and
because the distinction is easy to lose.

A participant in the OpenMDW review put the difficulty plainly: the training-data question "is
the center of the whole open source ai definition debate and IMO won't be solved by a license but
needs to be solved at the policy level," and a licence review should not be "encumbered by policy
discussions." That is a fair warning, and §6 of this instrument is exactly where it could apply.

**It does not, and the text is drafted so that it does not.** §6 says nothing about what anyone
else may reserve, what any legislature should do, or how fair use and the EU text-and-data-mining
exception ought to be reconciled. It says what **this Dedicator** does with **this Dedicator's**
rights:

- §6.2 is limited on its face to "the Covered Rights and patent claims of the Dedicator" — the
  Dedicator makes no reservation and declines to make one.
- §2.7 confines the whole instrument to rights the Dedicator holds, and disclaims any
  representation that the material is otherwise unencumbered.
- §6.3 reaches reservations by others only to the extent the Dedicator "is able", which §2.7
  already bounds.
- §6.5 concedes the point that §6 is declaratory of §3–§5 rather than an independent enlargement.

**Why state it at all, if it is declaratory?** Because in a regime where an opt-out is exercised
by signalling, silence is not neutral — a work with no signal invites the argument that a
reservation may exist. Saying "no reservation is made, and none will be" removes that argument
for this work, without asserting anything about the regime itself.

**What this submission is therefore not asking the list to decide.** Whether TDM opt-out regimes
are good policy. Whether training on lawfully accessible material should require permission.
Whether the Open Source AI Definition should require open training data. None of those is
necessary to decide whether an instrument that reserves nothing meets the Open Source Definition.

### 1d. What the text says about its own subject matter, measured

The jurisdictional question in §1a — whether this list reviews licences for works that are not
software — is usually argued from intent. It can also be measured, and the measurement cuts
against us more sharply than the argument does.

**The operative text does not describe itself as a software licence.**

| Term | Occurrences in the whole text |
|---|---|
| "program" | **0** |
| "executable" | **0** |
| "software" | **2**, both in the explanatory preamble and in §8.3's reasoning; **none in an operative grant or condition** |
| "source code" / "object code" | 1 each, inside §1.2's list of what a Work may be, alongside documentation, data, metadata and audiovisual material |

**Read against ACD-1.0, this is a liability.** If the criterion is that OSI reviews software
licences, an instrument whose operative provisions never mention software is further from that
line than one that does. §1.2 places source code in a list where it is one item among six. A
reviewer inclined to draw the line strictly has the text on their side, and I am not going to
argue that "any Work" quietly means "software".

**Read the other way, it is what makes the instrument coherent.** A licence that says "software"
in its grants has to be stretched to cover a dataset, a set of weights, or a documentation
corpus — and stretching is where the ambiguities that this whole review process exists to catch
come from. §1.7's "Computational Use" is defined over the Work, not over programs, so §6.1 and
§8.4 apply identically to code and to a corpus with no clause doing double duty.

**What this does not resolve.** Whether the OSD, written for software, is the right instrument
to judge this by. That question is live in another review as this is written (§1a), and it will
not be settled by pointing at word counts in either direction. What the counts do settle is that
the question is not marginal here: **this is not a software licence with data provisions bolted
on, and it does not read as one.**

### 1e. Why one document, and what would have to be true for that to be wrong

A structural objection has been put to another AI-era submitter on this list, and read from a
table of contents it is the shape of ACD-1.0. Pamela Chestek, `license-discuss` 2026-03-29:

> *"It seems that you are trying to do **three different things with one document**: (1) create
> a system for identifying the provenance of code, (2) apply a license and (3) optionally state
> that someone is waiving a claim to copyright they might have. I don't see any reason why
> purpose (1) is tied to purposes (2) and (3)… **Doing (2), and (3) optionally in the same
> document, is unnecessarily complicating things.**"*

ACD-1.0 has a dedication (§3), a licence (§4), a covenant not to assert (§5), express permission
for text and data mining (§6), database rights (§7), patents (§8), a statement about
machine-generated material (§9), moral rights (§12), and rules governing the document itself
(§16). **That is a long list, and the objection is not answered by saying the list is long for
good reasons.** It is answered, if at all, by what kind of thing each item is.

**The distinction I am relying on is between a purpose and a right.** What the objection names
is a *provenance-identification system* — an informational mechanism that is not a grant, not a
waiver, not a covenant, and which could be attached to any licence or to none. Bundling it with
legal operations ties two things that need not travel together, and a reader has to decide which
of them a given sentence belongs to.

**Every section listed above is a legal operation on the same Work.** §3 surrenders, §4 grants,
§5 covenants, §6 permits, §7 and §8 and §12 do the same over a different right, and §9 states
what is not represented. There is one subject matter throughout — the Work identified in §1.2 —
and one section per kind of right in it. **The nearest thing here to a declaration is §9.2, and
it is a refusal to represent rather than an information system**: it tells a recipient that no
claim is made about whether rights subsist in machine-generated material, which is a statement
about the grant's own reach.

**What would make this answer wrong.** If any section could be lifted out and applied to a
different work, or to no work, without changing what the others do, then it is a separate purpose
and belongs in a separate document. I do not think any of them can be, but that is the test, and
it is the reviewer's to apply rather than mine to assert.

**⚠ Two objections in this family pull in opposite directions, and I cannot satisfy both.** Rob
Landley has argued on this list that one instrument should carry one kind of right, which would
mean splitting §§3–8 apart. Chestek's objection is that unrelated purposes should not be bundled.
Elsewhere Piana and Chestek have both warned against leaving rights out, which is an argument for
keeping them together. **A submission cannot satisfy all three by rearranging the same material.
It can only say which principle it follows and why.** ACD-1.0 follows: one Work, one document,
one section per kind of right in that Work, and no non-legal purposes.

### 1b. Whether an instrument of this kind is reviewable at all

This question comes before the others, so it is answered first.

**The OSI's stated position is that a public-domain dedication, taken alone, is not an open
source licence.** That position is not a technicality to be argued around; it is the reason the
form of this instrument was chosen rather than a bare waiver. If ACD-1.0 were only a dedication,
the correct outcome would be that it falls outside what this list reviews.

**It is not only a dedication, and the licence half is not a fallback.** §3 is the surrender and
waiver. §4 is a licence grant, and §4.4 says in terms that it "is granted independently of
Section 3 and does not depend on Section 3 being ineffective" — where §3 works, §4 "is redundant
but not void, and it remains available to be relied upon by You," and "You are not required to
determine whether Section 3 is effective in any jurisdiction."

That construction is stronger than a fallback, and the difference matters to this question. A
fallback invites the argument that the licence exists only if and when a court first finds the
dedication ineffective — leaving open who decides, under which law, and what the recipient may
rely on meanwhile. §4.1 grants outright: worldwide, royalty-free, irrevocable, perpetual,
sublicensable, "subject to no condition of any kind" (§4.3). In every jurisdiction the recipient
holds a licence on its own terms, and holds it without having to resolve anything about §3.

**There is precedent for reviewing exactly this hybrid.** The Unlicense — an attempt at a public
domain dedication that also uses licence-grant wording — was submitted in March 2020 and
approved by the board in June 2020, and the discussion turned on that dual nature rather than
treating the dedication half as disqualifying. The archives are public and worth reading against
this submission:
<https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2020-June/004890.html>

**Two arguments from that review carry directly onto this text, and I would rather name them
than wait for them.**

*"This is not a license."* A reviewer took the position that the Unlicense "falls on the side of
'this is not a license'", on the ground that it lacks a clear expression of intent to convey
rights. The counter offered there was that its operative sentence — anyone is free to copy,
modify, publish, use, compile, sell, or distribute — functions as a grant whatever the label,
and that the BSD licence does not use the words "grant" or "permission" either. ACD-1.0 is on
firmer ground here than the Unlicense was, and not because it is better drafted: §4.1 says
"The Dedicator grants You a … licence", and §4.4 states that this grant is independent of the
dedication and does not depend on it failing. Where the Unlicense had to argue that a permission
was a grant, this text says so.

*"No requirement to include the licence on redistribution — how effective is the disclaimer?"*
This one lands, and lands harder here than there: §10.2 says expressly that You need not retain
the file or reproduce any notice. The permissions are unaffected (§1.4, §4.1 and §2.3 make the
grant run to each recipient directly, which is how MIT-0 and 0BSD operate), but a warranty
disclaimer asserted against someone who never saw it is weaker than one that travelled with the
work. **The loss falls on the Dedicator, not on the recipient**, which is why it is disclosed
here rather than argued away in the conformance section. `ACD-1.0.review-responses-clauses.md`
sets it out at length.

The committee's own words are worth quoting, because they state the doctrine and the escape from
it in one sentence: the Unlicense "is an attempt to dedicate a work to the public domain (which,
taken alone, would not be approved as an open source license) but it also has wording commonly
used for license grants."

**Four differences from that precedent, all of which cut against this submission and are stated
here rather than left to be discovered.**

1. **The Unlicense was submitted as a request for *legacy* approval** — the thread is titled
   *"Request for legacy approval: The Unlicense"* — and it was already in widespread use by many
   unaffiliated parties, which is weight the text alone might not have carried. ACD-1.0 has one
   adopter and cannot borrow that argument. It has to stand on the text. **What the record does
   not show is the basis the board actually used**: the OSI's own licence list categorises the
   Unlicense as `special-purpose`, not as legacy (the category exists and holds other licences),
   and the board minutes for that decision are linked to a wiki that no longer serves them.
2. **The Unlicense was approved despite broad agreement that it is poorly drafted.** ACD-1.0
   errs in the opposite direction: 16 sections and 82 clauses, which will draw the opposite
   criticism — that it is too long for what it does (answered at length in
   `ACD-1.0.review-responses-meta.md` Q17). That trade was made deliberately. Where the
   Unlicense's brevity left questions to be resolved by argument, this text tries to answer them
   in the text, and pays for it in length.

3. **That approval rested on legal advice.** The License Review Committee's recommendation reads,
   in full on the point (read at source in the license-review archive, 2026-09-06):

   > "It is an attempt to dedicate a work to the public domain (**which, taken alone, would not be
   > approved as an open source license**) but it also has wording commonly used for license
   > grants. There was some discussion about the legal effectiveness of the document, in particular
   > how it would operate in a jurisdiction where one cannot dedicate a work to the public domain.
   > **The lawyers who opined on the issue, both US and non-US, agreed that the document would most
   > likely be interpreted as a license and that the license met the OSD.** It is therefore
   > recommended for approval."

   Two things follow, and they cut in opposite directions. The parenthesis is **the Committee's own
   statement of the rule this submission must clear** — a dedication taken alone is not approvable
   — and ACD-1.0's answer to it is structural: §4 is a licence granted independently of §3 and does
   not wait for §3 to fail (§4.4), so the instrument is not "taken alone" as a dedication. But the
   sentence that resolved the Unlicense is **legal opinion, from more than one lawyer, across
   jurisdictions**, and that is precisely what this submission cannot replicate: no lawyer has read
   ACD-1.0 (§5, §4c). Where the Unlicense had counsel's reading to settle the
   dedication-versus-licence question, this submission has only the structure of the text and
   whatever reading the list gives it.
4. **It was not placed in a general category.** The committee recommended the Unlicense be placed
   in the "Special Purpose" category "because of its intended nature as a dedication to the public
   domain," and **rejected** the submitter's request for the "Popular and Widely-Used or With
   Strong Communities" category. If ACD-1.0 were approved, a comparable narrow placement is the
   realistic expectation, not a general endorsement — which is consistent with §4a above, where
   this submission disclaims any request for such designations. (OSI's category names have since
   been revised; the point is the narrowness, not the label.)

**What follows if the hybrid framing is rejected.** If the list's view is that §4's independent
grant does not make this a licence, then the honest conclusion is that ACD-1.0 is not a candidate for OSI
approval in its present form, and the response will be to say so rather than to redraft under
pressure. `ACD-1.0.submission.md` §E.2 already records what would cause the submission to be
withdrawn; this is one of those conditions.

### 2. How ACD-1.0 differs from the closest OSI-approved licences

**The gap, in one sentence, stated so that it can be falsified.** No OSI-approved instrument
grants all three of these at once: **(i)** a grant that expressly reaches **non-copyright rights
in data** — in the EU the sui generis database right, whose own verbs are *extraction* and
*re-utilisation*; **(ii)** a **patent licence that survives the transformation of the work into a
model** and the outputs of that model; and **(iii)** **no condition on the licensee at all**.
**Two of the three exist in several approved licences. The three together do not.** This is
checkable from the grant clauses themselves rather than from what the texts omit, and the
clause-by-clause reading is in `ACD-1.0.gap-measurements.md` §1.96.

**What this does not claim.** MIT's *"deal in the Software without restriction"* may well reach
those rights by implication; this submission does not argue that it does not. It argues that the
question is **left to interpretation**, and that for a work meant to be learned from — read by
systems that cannot litigate an implication — an express grant and an implied one are not the
same thing. That is a design argument, not a legal opinion, and no legal opinion has been
obtained (§5).

**Closest on "zero conditions": 0BSD.** 0BSD grants permission to *use, copy, modify and
distribute this software*. ACD-1.0 shares that zero-condition character and differs in
seven respects, each of which is operative rather than stylistic:

| | 0BSD | ACD-1.0 |
|---|---|---|
| Subject matter | "software" | any Work: source, object, documentation, **data, metadata, audiovisual material**, and compilations (1.2) |
| Patents | silent | 8.1–8.5, with 8.4 granting separately over Computational Use and its outputs |
| ML / TDM | silent | 6.1–6.5 |
| Sui generis database right | silent | 7.1–7.2 (extraction and re-utilisation of a substantial part, repeatedly and systematically) |
| Moral rights | silent | 12.1–12.6: waiver, and in jurisdictions where moral rights cannot be waived, a covenant not to exercise them **limited to the Work** and binding successors |
| Machine-generated material | silent | 9.1–9.4 |
| Irrevocability / successors | silent | 2.2, 2.5 (reliance and estoppel), 2.8 (Sections 3, 4, 6 and 8 bind successors and transferees), 2.9 (not executory; unaffected by insolvency and by the acts of a trustee) |

**On the moral-rights row, against us**: 0BSD is silent, but the approved EUPL-1.1 and 1.2 are
not — *"In the countries where moral rights apply, the Licensor waives his right to exercise his
moral right to the extent allowed by law"*. The structure of Section 12 (waive where possible,
do not exercise where not) therefore has an approved precedent; what Section 12 adds is naming
whom the covenant protects (12.2) and binding successors (12.4). EUPL is the only approved
licence of 141 that mentions moral rights ([`ACD-1.0.gap-census.md`](ACD-1.0.gap-census.md)).

The enumerated acts also differ: 0BSD's four verbs do not cover sublicensing, communication
to the public, public performance or display, rental, or adaptation, which ACD-1.0 Section
4.2 lists expressly for civil-law jurisdictions where those are distinct exploitation
rights.

*Would 0BSD plus a separate patent grant do?* No. A separate instrument does not travel
with the work, and a downstream recipient has no assurance it exists. The point of Section
6.5 — that a permission an automated system cannot determine is, for a work meant to be
learned from, no permission at all — applies to patents as much as to training.

**Closest on "express patent licence": Apache-2.0.** Apache-2.0 conditions its grant on
notice retention, change notices and NOTICE propagation; ACD-1.0 imposes no condition
(4.3, 10.1). Apache-2.0 terminates the patent licence on patent litigation; ACD-1.0
contains no retaliation provision and says so expressly (8.2). Apache-2.0's patent grant
reaches "the Work and Derivative Works"; whether a *trained model* is either is unresolved,
and Section 8.4 is written precisely to close that — as an independent grant, so that it
does not fall with the reading of Section 8.1 it was written to survive.

**Closest on "reaches beyond copyright": CAL-1.0.** This is the comparison a reviewer who knows
the approved list will reach for, and it is the one that most narrows the claim above.
CAL-1.0 §3.1(a) grants permission to *"take any action with the Work that would infringe the
**non-patent intellectual property laws of any jurisdiction** to which You are subject"* — which
does reach a sui generis database right, expressly and without naming it. **So it is not true
that no approved licence reaches these rights.** (Nor is it true that none treats a database as licensed material:
WordNet grants *"Permission to use, copy, modify and distribute this software and database"*,
though it names no right beyond that list; a full-text scan of the 141 approved licences finds
`sui generis` and `database right` in none —
[`ACD-1.0.gap-census.md`](ACD-1.0.gap-census.md).) Two differences remain, and they are the ones
that matter here. First, CAL-1.0 §3.1 opens *"Conditioned on compliance with section 4"*, and
§4 carries attribution, source-availability and Recipient-Data obligations; ACD-1.0 imposes no
condition of any kind (4.3, 10.1). Second, CAL-1.0 §3.2(a) states that the Licensor *"does not
grant any patent license for claims that are only infringed due to … the combination of the
Work as provided by Licensor, directly or indirectly, with any other component"* — a trained
model is such a combination, so the patent grant stops before the artefact ACD-1.0 Section 8.4
is written to reach.

**Closest on "a patent grant that reaches things made from the work": CERN-OHL-P-2.0**
(and its S and W variants, which share the definition). **This is the comparison that most
narrows the claim that no approved licence carries a patent grant past the work itself, and
until 2026-09-25 this dossier had not made it.** CERN-OHL-P-2.0 §6.1 grants a patent licence
*"to Make, have Made, use, offer to sell, sell, import, and otherwise transfer the Covered
Source **and Products**"*, and §1.4 defines a Product as *"any device, component, **work** or
physical object, whether in finished or intermediate form, arising from the use, application
or **processing** of Covered Source"*. **A reviewer can fairly read a model trained on Covered
Source as such a Product**, and nothing in the text excludes that reading. **So "no approved
licence grants patents that reach a trained model" should not be asserted. What can be
asserted is narrower**: no approved licence *names* models, parameters or outputs (census,
[`ACD-1.0.gap-census.md`](ACD-1.0.gap-census.md)). The remaining differences are the same kind
as with CAL-1.0. First, conveying a Product is conditioned: CERN-OHL-P-2.0 §4 permits it
*"provided that You ensure that the recipient of the Product has access to any Notices
applicable to the Product"* — a notice obligation that would travel with a model — whereas
ACD-1.0 imposes none (4.3, 10.1). Second, §6.2 terminates all rights on patent litigation
alleging that the Covered Source *or a Product* infringes; ACD-1.0 has no retaliation
provision (8.2). **Third, and against us**: CERN-OHL was drafted for hardware, where "things
made from the source" is the central case, so its authors had already solved in general terms
the structural problem Section 8.4 solves for one artefact. **Section 8.4's novelty is naming
the artefact, not the idea of a grant that follows what is made.**

**Closest on "permissive, one condition, express patent grant": UPL-1.0, BlueOak-1.0.0 and
BSD-2-Clause-Patent.** **This is the question a reviewer is most likely to ask first — "why
not one of these?" — and until 2026-09-25 this section did not answer it.** All three are
approved, all three grant patents expressly, and each carries exactly one kind of condition:

| | Condition | Patent grant reaches | Also |
|---|---|---|---|
| **UPL-1.0** | *"The above copyright notice and either this complete permission notice or at a minimum a reference to the UPL must be included in all copies or substantial portions of the Software."* | the unmodified Software, and the *"Larger Work(s)"* **listed in `lrgrwrks.txt`** | licensed material is *"software, associated documentation and/or **data**"* |
| **BlueOak-1.0.0** | *"You must ensure that everyone who gets a copy of any part of this software from you … also gets the text of this license or a link"*, with a 30-day cure (*Excuse*) | *"everything with this software that would otherwise infringe any patent claims they can license or become able to license"* | *"No contributor can revoke this license."* |
| **BSD-2-Clause-Patent** | retention of the notice in source and binary redistributions (clauses 1–2) | Contributions alone, or in the combination they were added to *"at the time the Contribution is added"*; *"shall not apply to any other combinations"* | |

**What this concedes, stated first.** (i) **BlueOak's patent grant is not limited by activity**:
training a model on the software is something done *"with this software"*, so the act of
training is covered in terms — the difference from Section 8.4 is whether the grant also follows
the resulting model once it is used apart from the software, which BlueOak does not say.
(ii) **UPL already names data as licensed material and already lets a licensor extend the patent
grant to named downstream works** — a licensor could list a model in `lrgrwrks.txt`. The
difference is that UPL makes that the licensor's per-work act, where Section 8.4 makes it the
default for every recipient. (iii) **The remaining difference on every row is the condition.**
ACD-1.0 has none (4.3, 10.1), and that is the whole of the case against these three — not the
patent grant, which they already have. **A reviewer who thinks a single notice condition is not
a burden worth a new licence has answered the question against us, and that is a fair answer**
(see [`ACD-1.0.board-decisions.md`](ACD-1.0.board-decisions.md) on *"duplicative"*, and #84 on fungibility).

### 3. Open Source Definition conformance → [`ACD-1.0.submission-osd.md`](ACD-1.0.submission-osd.md)

**この節は 2026-09-25 に `ACD-1.0.submission-osd.md` へ移した**（節番号はそのまま）。

### 3b. Where a reviewer could still argue, criterion by criterion → [`ACD-1.0.submission-osd.md`](ACD-1.0.submission-osd.md)

**この節は 2026-09-25 に `ACD-1.0.submission-osd.md` へ移した**（節番号はそのまま）。

### 3c. The OSI's own list of common reasons for rejection, item by item → [`ACD-1.0.submission-osd.md`](ACD-1.0.submission-osd.md)

**この節は 2026-09-25 に `ACD-1.0.submission-osd.md` へ移した**（節番号はそのまま）。

### 3d. Subject matter: why this is a software licence and where the overlap with an open-culture licence lies → [`ACD-1.0.submission-osd.md`](ACD-1.0.submission-osd.md)

**この節は 2026-09-25 に `ACD-1.0.submission-osd.md` へ移した**（節番号はそのまま）。

### 4. What is deliberately absent

Omissions are design decisions too, and the committee will ask about several of them.

**Each entry below now states what the absence costs, not only why it was chosen** (added
2026-09-20). Until then every item carried the favourable half alone, which was found by
auditing our own record after an adversarial reading pointed at one of them (`against.md`
#174). **An omission that only ever appears as a strength is being argued rather than
disclosed**, and this list is the wrong place to argue.

- **No patent retaliation.** A grant that ends when the licensee litigates is a grant with
  a condition. Section 8.2 says the absence is deliberate so that it is not mistaken for an
  oversight. **Cost:** retaliation is the standard deterrent in Apache-2.0 §3 and GPLv3 §10,
  and this instrument has no substitute for it — a competitor may take everything and sue
  anyway. **The accurate statement is that Section 10.1 makes retaliation impossible here,
  not that retaliation is undesirable** (`against.md` #174).
- **No attribution requirement.** Attribution is a real wish, so Section 10.3 separates the
  wish from the obligation: any request the licensor makes, however phrased and wherever
  expressed, is a request and not a condition; not observing it is not a breach and narrows
  no permission. **Cost:** nothing carries provenance downstream. A recipient may strip every
  trace of origin lawfully, so the chain that lets a later reader find the source is broken by
  design, and the licence offers no answer to origin-laundering.
- **No field-of-use restriction of any kind**, including the "ethical" restrictions now in
  circulation. Section 4.3 forecloses them expressly (OSD 6). **Cost:** a Dedicator who later
  objects to a particular use has no recourse under this instrument, and adopters who want
  such limits cannot get them here. **OSD 6 requires this; the cost is still real.**
- **No choice of law or forum.** Section 15.7. Naming one jurisdiction would disadvantage
  recipients everywhere else. **Cost:** a plaintiff chooses the venue, and neither party can
  predict which law governs before a dispute begins. An adversarial reading of 2026-09-20
  called this the instrument's greatest systemic defect; **the dossier answers it
  (`review-responses-clauses.md`) but the text does not.**
- **No anti-DRM condition on the licensee.** A licence that imposes nothing cannot impose
  this either. The same protection is achieved from the other side: Section 5.2(a) is a
  covenant by the *licensor* not to apply technological measures to the Work or to invoke
  anti-circumvention law against You. **Cost:** downstream is unconstrained — a recipient may
  wrap the Work in access controls, and a measure applied by a distribution platform is
  outside the covenant entirely (`against.md` #171). **The Work stays free; copies of it need
  not.**
- **No barrier to translation.** Section 16.4 fixes the text that the name denotes, but
  Section 16.5 makes a translation an express exception: it may carry the name and the
  identifier so long as it is identified as a translation and states that the English text
  prevails. A rule that kept translations out would have put Section 16.4 at odds with
  Section 15.8 and would have kept the licence away from readers who do not read English.
  **Cost:** a translation may drift in meaning while carrying the same name and identifier.
  Section 15.8 makes English authoritative, but **a reader who relies on the translation is
  misled in fact even where the text is right in law.**
- **No trademark licence.** Section 11.1. Trademarks identify origin, and an unconditional
  grant would mislead. Section 11.2 preserves truthful nominative reference. **Cost:** an
  adopter cannot use the Dedicator's marks to signal what they have adopted, and the notice
  in Section 16.1 named this carve-out while passing over the wider one in Section 11.4 until
  errata E29 (`against.md` #173).
- **No provenance or disclosure requirement for AI output.** Section 6.4 says outputs are
  unencumbered; requiring their labelling would contradict the licence's central purpose.
  **Cost:** it sits against the direction transparency regulation is moving, and a reviewer
  may read it as the licence declining a duty the law is about to impose. **The answer is that
  a licence condition and a statutory duty are different instruments — but the tension is
  real, and it is not resolved by pointing at OSD 6.**

### 4a. Which track this submission is on, and what it does not ask for

**This is a new licence, not a legacy one.** The review process distinguishes the two: a legacy
licence is one already in widespread use for several years by a number of unaffiliated entities;
everything else is a new licence. ACD-1.0 has one adopter and was published in 2026, so it is
unambiguously in the new-licence track and is expected to answer the questions that track asks:

| What the track asks | Where it is answered |
|---|---|
| What gap do existing licences not fill, compared with the most similar approved licence(s)? | §1 and §2 of this message; clause-level comparison in `ACD-1.0.comparison.md` |
| What legal review has it had, and was it drafted by a lawyer? | §5 and §E.1 — **no legal review, not drafted by a lawyer**, stated without hedging |
| Can others use it, or is it usable only by the submitter? | §4b below, with commands that verify each claim |

**What is not being asked for.** Approval would place ACD-1.0 in the set of licences that meet
the Open Source Definition. It would not make it recommended, popular, or preferred; those are
separate designations driven by adoption data, and this submission makes no claim to them.
Saying so up front is not modesty — conflating "conforms to the OSD" with "should be widely
used" is a common way for a submission to overreach, and the honest position is the narrower one.

**Timeline expectations are the reviewers', not mine, and the two comparable submissions do not
point the same way.** The process describes a decision on the order of two months. The two
AI-specific licences actually in review show a wider spread than that figure, in both directions:

- **ModelGo** was submitted in February 2025, reached a third resubmission in December 2025, and
  its author's follow-ups in January, May and July 2026 have gone unanswered.
- **OpenMDW-1.1** is still on its first submission, and its August 2026 thread alone runs to some
  48 messages among about a dozen participants — substantive engagement rather than silence,
  with several of the submitter's explanations reported as resolving the concerns raised.

Either pattern is possible here. This submission sets no deadline, asks for no expedited
handling, **will not read silence as a verdict**, and does not treat repeated revision as
failure — ModelGo's three rounds are what "improve and resubmit" looks like when it is working. If the
outcome is rejection, §E.2 already states what would cause the licence to be withdrawn rather
than re-argued.

### 4b. That the licence is not usable only by me

OSI's review process asks a submitter to show that a new licence is **not uniquely usable only
by the submitter**. Two kinds of evidence are offered: what the text structurally is, and who
else would plausibly reach for it.

**Structural evidence (verifiable in one command each).**

| Property | How to check | Result |
|---|---|---|
| No project, author, domain or URL appears in the licence body | `grep -icE "yokoi\|portfolio\|github\|https?://" LICENSES/ACD-1.0.txt` | **0** |
| No placeholder or replaceable text in the operative clauses (`<year>`, `[name]`, templates) | `grep -cE "<[^>]+>\|\[year\]\|\[name\]\|YYYY" LICENSES/ACD-1.0.txt` | **1** — the only hit is §16.1's recommended-notice template *"Full text: &lt;location of this file&gt;"*, a blank the adopter fills in **their own notice**, not in the licence; the licence text itself is never edited. *(Corrected 2026-09-24: this row used `<[a-z]+>`, which cannot match a multi-word placeholder, and reported **0**. Our own `spdx.xml` marks that blank as an `<alt>` variable.)* |
| Defined terms are generic role names, not identities | `"Work"`, `"You"`, `"Your"`, `"Dedicator"`, `"Contribution"`, `"Dedication"`, `"Reservation"` | 7 terms, none naming a person or project |
| The application declaration is a separate file | `LICENSE` carries `SPDX-License-Identifier` and a path; `LICENSES/ACD-1.0.txt` is the generic instrument | Applied **by reference**, never by editing |

The practical consequence: adopting ACD-1.0 requires **no edit to the licence text at all**. That
is a stronger form of reusability than licences that must be filled in with a name and a year,
and it is why the text is byte-identical for every adopter.

**Who else would reach for it, and why the nearest approved licences do not fit.**

| Adopter | Why not the nearest OSI-approved option |
|---|---|
| A research group publishing a corpus intended to be trained on | MIT-0 / 0BSD / Unlicense are silent on text-and-data-mining and on the EU sui generis database right. Silence is not permission where an opt-out regime exists; ACD-1.0 §6 affirmatively permits and makes no reservation |
| A standards body publishing a reference implementation | The public-domain-like effect is wanted **together with** a patent grant. CC0's exclusion of patents is precisely what stopped it at OSI; ACD-1.0 §8 grants, and §8.4 reaches the trained model and its outputs |
| A publisher of machine-generated artefacts | MIT/BSD assume a copyright exists to license. Where authorship may not subsist at all, that assumption is the problem; ACD-1.0 §9 makes the permissions independent of whether any right subsists |
| A public-sector or civic-data publisher in a jurisdiction where waiver is ineffective | A bare dedication can fail outright in such jurisdictions. ACD-1.0 §3 falls back rather than failing |
| Anyone shipping assets with embedded metadata (images, audio, models) | The status of embedded metadata is usually left unstated. ACD-1.0 §1.2 includes data, metadata and audiovisual material in the defined Work |

None of these depend on anything about my project. Each is a gap that exists for the adopter
regardless of who drafted the instrument.

**A falsifiable test.** Copy `LICENSES/ACD-1.0.txt` into any unrelated repository, add a
`LICENSE` file containing `SPDX-License-Identifier: ACD-1.0` and a pointer to the text, and the
adoption is complete. If any step required editing the licence body, the claim in this section
would be false. It does not.

**What this section does not claim.** It does not claim adoption. Actual use is one repository,
mine, and that limitation is stated plainly in §5 below. Reusability and adoption are different
properties, and the requirement here is the former.

**What this property is called on these lists, and the one criterion the successor does not clear.** The
OSI's own License Proliferation Report names a category of *"Non-reusable licenses"* —
*"licenses in this group are **specific to their authors and cannot be reused by others**. Many,
but not all, of these licenses fall into the category of **vanity licenses**"* — a definition
quoted on `license-discuss` by three participants independently in 2020 (Fontana, 2020-03-31;
Smith and Rosen, 2020-04-01). On the same list in 2019, Marc Jones proposed four things a
reusable licence should not do (2019-02-11). Measured against them:

| What Jones proposed excluding | ACD-1.0 |
|---|---|
| *"hard code a specific person/company as being the licensor and the code base being licensed"* | **Clear** — §16.3; the first grep above returns 0 and the second finds only the adopter's own notice blank in §16.1 |
| *"hard code the licensor being in an **unreasonably privileged position**"* | **Clear in ACD-1.0, at the cost of errata E14; not clear from 1.1 on. See below** |
| *"required significant changes or modifications to the license text to be used by others"* | **Clear** — adoption requires no edit at all |
| *"if only the company sponsoring the license is capable of **complying**"* | **Clear, and this is the strongest of the four** — §10.1 imposes no condition, so there is no one who can fail to comply |

**Why ACD-1.0 clears it, and what that costs — stated here rather than left to be found.**
ACD-1.0's §16.4 forbids distributing a *modified text* under the name "Autonomous Commons
Dedication" or under the identifier "ACD-1.0", and it makes **no exception for anyone**: the
steward is bound exactly as every other distributor of the text is. No party holds a privilege
written into the text, so the criterion is clear. **The cost is errata E14**: 1.0 protects the
name in general but only the one identifier `ACD-1.0`, so a modified text can circulate as
`ACD-1.1` or `ACD-2.0` as long as it avoids the name.

**The successor closes E14 and thereby fails this criterion.** ACD-1.1 and the 1.2 draft protect
the whole `ACD-N` / `ACD-N.N` family and let a modified text be distributed under it
*"except by the Steward"*, a role their §16.5 defines as whoever first published the text under
that name. That is a privilege held by one party and **written into the licence itself**. Three
things bound it, and none of them makes it disappear. First, the successor's §16.6 places
§16.4 and §16.5 outside the terms of the Work: they bind no recipient of a work — but Jones's
criterion is about the text, and carries no such limit. Second, a steward is ordinary; Apache,
Mozilla and the FSF each have one. What is unusual is writing it into the text rather than
operating it outside, which MIT, 0BSD and the Unlicense do by naming no steward at all. Third,
it is there for a reason that expires: an identifier family has to keep denoting fixed texts,
and until a registry performs that function the text is the only place it can be performed.

So the honest statement is that **family-wide identifier stability and the absence of in-text
privilege cannot both be had: ACD-1.0 has the second and pays for it with E14, and the successor
chose the first**. A reviewer may prefer either. What would not be honest is to answer the
point by quoting §16.6, as though the criterion had a limit it does not have — or to present the
successor's privilege as a property of the text under review. *(Corrected 2026-09-24: this
section had attributed 1.1's Steward exception to ACD-1.0 — `against.md` #160.)*

**And the label is removed by an explanation, not by the text.** On `license-review`
(2023-01-18) Bradley M. Kuhn declined to withdraw the word from another submission in these
terms: *"absent that explanation, this really does still look like a vanity license to me at
the moment"* — the explanation being why someone would need this licence instead of an existing
one. That question is answered in §1 and §2 above; the answer here is only that it is the same
question.

### 4c. What was verified mechanically, since it was not verified legally

No lawyer has read this. That is stated plainly in §5 and it is the weakest point of the
submission. It cannot be repaired by asserting confidence, so what follows is the opposite: the
narrow set of properties that **can** be established without counsel, each with the command that
establishes it. None of these substitute for legal review. They only mean that the failures a
machine can find are not present.

| Property | Command | Result |
|---|---|---|
| Every defined term is actually defined, in one place | `grep -nE '^\s+1\.[0-9]+\s+"' LICENSES/ACD-1.0.txt` | 10 terms, all in §1.1–§1.10 |
| No defined term is dead (each is used outside its own definition) | count occurrences of each term outside the clause that defines it | 10/10 used; the lowest is **3**, shared by `Contribution` and `Machine-Generated Material` |
| Section numbering is contiguous with no gaps | `grep -cE '^[0-9]+\. [A-Z]' LICENSES/ACD-1.0.txt` | 16 sections, numbered 1–16 |
| Internal cross-references all resolve to a clause that exists | enforced in CI (Check 441b) | no dangling `§N.M` |
| The text is pure ASCII | byte scan for values > 137 | **0** non-ASCII bytes |
| **Every promise §B.0 makes about the repository resolves** | 2026-09-10 に手で掃引 —— 「in the repository」型の 4 つ（OSD 逐条 / 反対の読み方の対 / 比較 / 不利な事実の一覧）、本文の URL、backtick で名指しした 2 path（`FROZEN.md` / `REVIEWERS.md`）| **全部在る。****1 件は同日に自分で作って同日に直した** ——「The command is in the repository」と書いた時点で `measure_gap_claim.py` は無かった。**Check は作らない**: 失敗したのは path ではなく散文の約束で、backtick path を検査する gate はこの class を捕まえない ——**捕まえない gate は名前だけの gate** |
| **The gap claim in §B.0 is reproducible** | `python3 .github/scripts/measure_gap_claim.py` —— SPDX の `isOsiApproved` 全件の本文を取得して主題語を数える | **149 件・4 語すべて 0 件、`output` が `patent` の 250 字以内に現れるものも 0 件**（2026-09-10・SPDX 3.28.0）。**2026-09-25 に 3.29.0 で再実行: 154 件（うち deprecated ID 13）・同じくすべて 0 件。** **⚠ この欄は 2026-09-19 に 149 → 150 → 151 と誤って書き換わっていた** —— 不利な事実の件数（#150 / #151）を更新した一括の数値更新が、たまたま同じ値だった承認済みライセンスの本数まで押し上げた（下の借用ゼロの行も同じ）。**script 自身が「語の不在は効果の不在ではない」を印字する** |
| **Every capitalised term used as if it were defined is defined — or is covered by the number clause** | scan every capitalised word-run that is not sentence-initial, subtract the ten §1 terms, and read what is left | **clean.** The residue is `Covered Right` (the singular of a defined plural, which **§15.2** expressly provides for), the literal `SPDX-License-Identifier` tag, and ordinary prose. **This is the defect that sank the Zeppelin Public License** — the Committee's rationale reads *"A 'contribution' is not defined, which means it might not be a derivative work … which would violate OSD 9"* (`review-corpus.md` §1.69) |
| **The sentence-length profile is at the short end of the approved range, and no long sentence stacks conditions** | split at `. ; :` before a capital **or a clause number**, count whitespace tokens per sentence, and run the same instrument over the SPDX `licenseText` of Apache-2.0, MPL-2.0, EPL-2.0, OSL-3.0 and CDDL-1.0 | mean **27.3** (only CDDL-1.0 is shorter), **longest sentence 85 words — the shortest of the six** (EPL-2.0: 195), **11.7%** of sentences exceed 45 words (the lowest but for CDDL-1.0 at 11.6%), and **none of them stacks two or more subordinate clauses** (Apache-2.0: 18.2%, EPL-2.0: 21.4%). **The first version of this row said the opposite** because the splitter did not recognise a clause number as a sentence start and merged our clauses (`review-rules.md` §1.70a). **Short sentences are not clarity**: errors specific to a non-native drafter do not appear in this measurement at all |
| **No condition is placed on the output of a model** | read §6.4 and §9.2–§9.3, and check the text for any obligation attaching to output | **none.** §6.4: *"You owe nothing in respect of any of them. Nothing in this Dedication requires You to license, disclose, or attribute any such thing."* **The Licensing Committee chair has stated on this list that putting conditions on model output violates OSD 9 where the output is not a derivative work** (2025-12-05); ACD-1.0 is on the opposite side of that line (`review-corpus.md` §1.74). **This removes a disqualifier; it is not a reason to approve** |
| **The patent grant uses the limitation this list has described as acceptable, and the wording predates our reading of those messages** | compare §8.1's closing words with Chestek (`license-review`, 2025-02-14) and Perens (`license-discuss`, 2024-04-06); then `git log -S'as made available by the Dedicator' -- LICENSES/ACD-1.0.txt` and `git log --diff-filter=A -- LICENSES/rounds/` | **match**, and **2026-08-23 vs 2026-09-06** — the clause was fixed two weeks before this project stored any list archive. **What this does not claim**: the drafter is an AI whose training includes licence literature, so this shows the wording predates **our reading of these messages**, not that it was reached in ignorance of such formulations (`review-corpus.md` §1.79) |
| The authoritative language is stated in the text itself | `grep -n "authoritative language" LICENSES/ACD-1.0.txt` | §15.8 — English governs; translations are convenience only |
| No project-specific or replaceable text | see §4b | 0, and 1 in the notice template only (§16.1) |
| **The warranty disclaimer and liability limitation are conspicuous** | `grep -n '^ *1[34]\.' LICENSES/ACD-1.0.txt` and read the case of the text | **§13.1, §13.2 and §14.1 are entirely upper-case.** This follows the convention McCoy Smith described on this list (2025-05-28): MPL-2.0 highlights those paragraphs in yellow to meet the US UCC requirement that such disclaimers be *conspicuous*, and plain-text renderings substitute capitals or rules of asterisks. §13.3 (no duty to maintain) and §14.2 (savings clause) are not capitalised because they are not themselves disclaimers. Measured 2026-09-08 |
| **No clause text is borrowed from an existing licence** | word-normalise both texts (lower-case, strip punctuation) and intersect their 8-word runs | **Re-run on 2026-09-14 against all 149 OSI-approved licence texts, fetched from the SPDX License List rather than from web pages.** **ACD-1.0 shares seven distinct 8-word runs in total**, and every one of them is a standard formula rather than clause text: *"even if advised of the possibility of such"* and two neighbouring windows of the same liability sentence (37 licences), *"(be) reformed to the minimum extent necessary to make"* (8), *"grants you a worldwide royalty free non exclusive"* (6). **With MIT, MIT-0, 0BSD, Apache-2.0 and the Unlicense the intersection is empty**, and the longest shared run with any of them is seven words — *"for any purpose commercial or non commercial"*, once, with the Unlicense. **Control**: MIT ∩ MIT-0 = 124 runs, MIT ∩ Unlicense = 59, so the method detects borrowing where borrowing exists. **The earlier measurement (2026-09-07) reported the same zero and the same seven-word run, but a control of 555 and 485** — it used the six licences' published web pages, and **its own caveat predicted that page furniture inflates the control and cannot deflate the zero. Re-running from clean texts confirms the caveat in both direction and magnitude.** CC0-1.0 is absent from this run because **it is not on the OSI-approved list**; it remains a relevant comparator and was tested in the 2026-09-07 measurement |
| **The definition graph has no vicious circularity, and its forward references are named** | build the dependency graph of the ten §1 definitions (each definition against every other defined term) and look for cycles and for references to terms defined later | **One mutual pair and three forward references, all stated rather than denied.** The pair is **"Work" ⇄ "Dedicator"** — §1.2 defines the Work as *"the material to which **the Dedicator** has applied this Dedication"* and §1.3 defines the Dedicator as *"each person or entity **applying this Dedication to the Work**"*. **It is not vicious**, because both are anchored to an act outside the definitions — the placing of the notice under §16.1 — so the pair is fixed by something a reader can observe rather than by the definitions alone. **This is the ordinary shape**; MIT and Apache-2.0 tie their "Work" and licensor terms the same way. **The three forward references are §1.2→§1.3, §1.3→§1.5 and §1.5→§1.6.** A reader going strictly top-down meets a term three times before it is defined. **No reordering removes all three**, because the mutual pair guarantees at least one; §1 could be ordered to leave only that one. **Recorded, not repaired — the text is frozen** |
| **The drafting constructions this list has objected to are absent** | **read by hand with grep**, 2026-09-09: probe the text for each construction a `license-review` or `license-discuss` participant has raised against a submission | **`shall` 0 · `must` 0** (Bruce Perens, 2024-10: *"The word 'SHALL' must not be used in a license"* — though McCoy Smith disagreed on the same thread, so this is not settled practice); **`and/or` 0** (Pamela Chestek raised the *"collectively" vs "and/or"* ambiguity on ModelGo, 2025-03); **`hereby`/`herein`/`hereof` 0**; **`notwithstanding` 0**; **`deemed` 0**; **no "best efforts" or "reasonable efforts"**, and **no use of "reasonable" as a standard at all**; **no "including but not limited to"**; **no governing-law or venue clause** (§15.7 says so expressly — McCoy Smith calls such clauses *"indirectly discriminatory"*, Josh Berkus says a licence breakable by a national embargo fails OSD 5); **no capitalised term used as if defined but missing from §1** (all ten are defined and all ten are used — Check 441c enforces the converse). The only reference to an external legal source is §15.2's interpretation rule — *"a reference to a law includes that law as amended, replaced, or re-enacted"* — which makes the text **more** durable rather than dependent on a moving document. **Caveat, the same one that governs every enumeration here: this catches the constructions it lists.** It is a floor, not a proof, and the list was assembled from what reviewers have actually objected to, not from a drafting manual |
| Every clause pointer in the machine-readable descriptor **resolves** | Check 451a parses `ACD-1.0.machine.json` and requires each `clause` value to name a clause that exists in the text | **33 / 33**, machine-checked on every pull request and every push to `main` |
| Every clause pointer **also supports the claim it is attached to** | **read by hand**, 2026-09-09: each boolean and each `outOfScope` entry compared against the wording of the clause it cites | **33 / 33.** **This row previously said "resolves and matches its subject" with only the existence check behind it** — resolution is mechanical, agreement of meaning is not, and the two were reported as one. The same audit on `clause-reference.md`'s 82 rows found **three** mismatches (`against.md` #34–#36), so a clean result here was not a foregone conclusion. **Repeat the pass if the descriptor changes; nothing enforces it** |
| Every clause in the text has a row in the clause-by-clause reference, and every row a clause | cross-check `ACD-1.0.clause-reference.md` against the text | **82 / 82**, no gaps either way |
| Each row's description was read against its clause | manual pass over all 82, 2026-09-04 | **3 mismatches found and corrected** (against.md #34–#36) |
| The adverse list is numbered without gaps or duplicates, and every cross-reference between the dossier documents resolves | count `#N` entries; check each `#N` and `EN` citation against the lists | **249 entries, 1–249, no gaps; all citations resolve** |
| Every defect called a "1.1 candidate" anywhere has an entry in the errata to point at | cross-check declarations against `errata.md` | **one was missing and has been added (E7)** |
| Every negative self-claim the text makes about itself is true | extract each "contains no / imposes no / grants no / reaches nothing / specifies no" statement and search the whole text for the thing denied | **9 claims, 9 true** — each denied term appears only inside the clause doing the denying |
| Subordination claims are consistent: every "is subject to / bounded by Section N" points at a clause that exists and is a general principle | read the full text and follow each cross-reference | **2 found, both pointing at §2.7**, which is the general limitation clause |
| The six clauses disclaiming condition-status cross-reference into one mesh centred on §10.1 | trace §4.6, §10.3, §10.5, §11.3, §11.4, §16.6 | consistent; documented in `clause-reference.md` |
| **How long the text is, in the unit a reviewer uses** | `wc -w LICENSES/ACD-1.0.txt`, and the same over GPL-3.0 from gnu.org, counting the operative text of each | **4,896 words in full; 4,574 in the operative text** (clause 1 to the end). **GPL-3.0 is 5,644 and 4,617** by the same method (operative = `TERMS AND CONDITIONS` to `END OF TERMS AND CONDITIONS`). So ACD-1.0 is **43 words shorter than GPLv3's operative text and 748 shorter overall**; for scale, Apache-2.0 is 1,581 and MPL-2.0 2,435. **This row exists because length has been given on this list as a reason not to approve a licence**, and until 2026-09-09 we had described this text only in sections, clauses and lines. **It answers the number and not the whole argument**: the objection as stated was *wordy and proscriptive, therefore no one else will use it*, and only the first half is measurable. ACD-1.0 imposes no conditions (§10.1), but its adoption is one repository |
| **No condition is imposed on You — measured over a deontic vocabulary wide enough to survive the reviewer's own grep** | **22 terms** swept over the full text with context, 2026-09-22: `shall`, `must`, `required to`, `obliged`, `obligation`, `provided that`, `on condition`, `only if`, `subject to`, `may not`, `agree to`, `undertake to`, `covenant to`, `in exchange`, `in consideration`, `conditioned on`, `so long as`, `unless you`, `failure to`, `is required`, `requirement`, `condition` | **`shall` 0, `must` 0. Every one of the ~45 remaining occurrences is a negation of a condition, a limit on the Dedicator, or a description of a different instrument** — read individually, not pattern-matched. **Why this row exists**: the published mitigation had been *"`shall` and `must` appear zero times"*, which is true and narrow; **a reviewer greps `condition` and gets more than forty hits.** The four that need a second's thought are §8.5 (*"subject to Section 2.7"* — a limit on the grant's reach, and §11.3 / §11.4 say in terms that a limit of reach is not a condition), §4.5 (You **may** impose conditions on Your own recipients), §5.2(b) (a list of what the **Dedicator** may not impose) and the preamble's description of a fallback design ACD-1.0 rejects. **The frozen text is unchanged; only the measurement is wider.** **What CI already enforced, and what this adds**: `Check 441d` (BLOCKING) tests seven patterns — `You must`, `You shall`, `You may not`, `You are required`, `provided that`, `on condition`, `You agree`. **This sweep adds the twelve it does not look for**, among them `subject to`, `only if`, `conditioned on`, `so long as` and the bare `must`. **The same seven now also guard the successor draft (Check 468g), which had no such guard.** |
| The machine-readable layer does not overstate its status | `grep -o 'isOsiApproved="[a-z]*"' LICENSES/ACD-1.0.spdx.xml` and the `osiApproved` / `spdxListed` fields | all **false** |

**Re-derived again on 2026-09-10: the five mechanically derivable rows all reproduce (10 terms, 82 clauses, 16 contiguous sections, 0 non-ASCII bytes, 33 / 33 clause pointers), and **Check 460 (n) now compares them with the artefacts on every pull request**, so this table can no longer drift silently. The hand-read rows are deliberately left outside that check — a machine must not certify what it cannot read. **Every row above was re-derived from the artefacts on 2026-09-06, and three were wrong.** The
entry count was stale; the clause-pointer count and the defined-term minimum were wrong when
written, since both of their inputs are frozen and could not have drifted. They are corrected
here and are now checked on every CI run against the artefacts themselves rather than against a
remembered number. A fourth was nearly reported in error: counting the negative self-claims with
a looser pattern than the one this table names gives 10 or 11 rather than 9, because "contains
nothing" contains the string "contains no". **Under the five phrase forms this row actually
lists, the count is 9 and the row is correct** — which is the reason the counting rule is now
stated in each row rather than left to the reader.

**Why this is worth stating rather than skipping.** Drafting defects that reviewers routinely
catch in new licences are disproportionately of the mechanical kind: a term used but never
defined, a definition left over from an earlier draft, a cross-reference to a clause that was
renumbered, a section that says "as set out below" with nothing below it. Those are exactly the
faults a machine can rule out, and ruling them out is not nothing — it means the review time you
spend can go to substance instead of bookkeeping.

**What it does not establish.** Whether §4's independent grant is given effect in a
jurisdiction that rejects waiver, and how a court there characterises the instrument as a whole. Whether §8.4's patent grant reaches what it says it reaches.
Whether §12's moral-rights construction is effective in France. Whether §13/§14 survive contact
with consumer-protection law. Every one of those is a legal question, none of them is answered
here, and `ACD-1.0.jurisdictions.md` deliberately records them as **questions rather than
conclusions**.

**Stability of these results.** The text is frozen for the duration of this discussion and CI
pins the SHA-256 of the three licence files (Check 453), so the properties above hold for exactly
the text under discussion. If the freeze is lifted, they must be re-measured — a property
verified once is not a property that stays true.

### 5. Honest disclosures

- **Legal review.** The text has not been reviewed by counsel. I state this plainly rather
  than let the committee discover it. Section 12 in particular depends on the position of
  moral rights under Japanese law (Copyright Act Articles 59 and 60), and I would welcome
  the committee's scrutiny of the two-step structure I have used there.
- **Evidence of use.** At the time of submission the licence is applied to one substantial
  repository. I make no claim of wider adoption.
- **Provenance of the drafting.** Another AI told me that creating a custom licence was
  possible; **I then said that I wanted a licence of my own and that it should aim at external
  approval.** I did not write a legal specification and I did not supply a list of legal
  requirements: **I gave the goal and the top-level direction**, and the AI generated the
  concrete legal design and the text and developed it further under the standing delegation this
  repository runs on. **The name ACD-1.0, the generalised instrument, the submission packet and
  the review apparatus took shape during that delegated work, and I came to know their concrete
  state afterwards.** It is applied to **my** work. **I do not review the repository**; what
  reaches me is a summary, not the files. **The licence is the exception: I read it in full and
  understood it before sending.** I am the Dedicator and the steward and I answer for it;
  **I did not write its clauses.** The text cites exactly one external instrument
  (Article 4(3) of Directive (EU) 2019/790, in Section 1.10), deliberately, because invented or
  misattributed authority is the characteristic failure of machine-drafted legal text. Its
  internal consistency — contiguous numbering, resolution of every cross-reference, use of all
  ten defined terms, no obligation-imposing word directed at the user, nothing specific to my
  project — is enforced in continuous integration, so those are conditions the repository cannot
  be in violation of rather than assertions of care. **What none of that establishes is that the
  reasoning is sound**, which is what I am here to find out. A fuller statement is in section E.1.
- **Form.** The instrument is styled a *dedication* and contains a public-domain dedication
  (Section 3). I am aware of the committee's history with dedication-shaped instruments.
  Section 4 is a licence granted **independently** of Section 3 and expressly does not
  depend on Section 3 being ineffective (2.4, 4.4). Where Section 3 operates, Section 4 is
  redundant but not void and remains available to be relied upon. The licence is therefore
  a licence in its own right, and is what I ask the committee to review.

Thank you for your time.

Yuta Yokoi

---
