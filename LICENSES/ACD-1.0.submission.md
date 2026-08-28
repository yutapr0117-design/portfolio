# ACD-1.0 — submission packets (English, ready to paste)

> **What this file is.** Everything a human needs in order to submit the Autonomous
> Commons Dedication 1.0 to the SPDX License List and to OSI License Review, written in
> the language those bodies use, so that the human-only step is *send*, not *compose*.
>
> **Status of the licence itself:** see `LICENSES/ACD-1.0.txt`. The rationale, the
> gap analysis, the clause-level comparison with the closest OSI-approved licences, and
> the honest weaknesses are in `docs/architecture/acd-license-rationale.md` (Japanese).
>
> **Do not send anything from this file until `LICENSES/READY-TO-SUBMIT.md` exists.**
> Its absence means the text is still being improved and is not yet at a standard where
> a review verdict would be worth having.

---

## Status as of 2026-08-26

| | |
|---|---|
| **Sent** | **OSI `license-discuss`** — posted, awaiting reaction. This is OSI's *general discussion* list, **not the venue for an approval request**. The steward posted there to find out whether the instrument should exist at all, before asking anyone to approve it. |
| **Not sent** | **OSI `license-review`** — the venue that actually starts an approval request. **Section B below is written for that step and has not been sent.** |
| **Not sent** | SPDX License List. SPDX asks for substantial real-world use; this text has one user. **Not meeting the condition is the reason, not the ordering** — section C below stays unsent until that changes. |
| **Text** | Frozen. `LICENSES/FROZEN.md` records the freeze and CI pins the sha256 of the three submitted artefacts. A sound criticism received during review is answered with *"that is right, and ACD-1.1 will do X"* — not by editing the text under review. |

**Section E below lists disclosures that section B does not contain.** They apply to whatever
is posted, including the license-discuss thread that is already open.

Anticipated objections and prepared answers (40 worked entries plus a table of 8 short answers, across three files) are in
`LICENSES/ACD-1.0.review-responses.md` and its `-clauses` / `-meta` companions.

A clause-by-clause reference covering **all 82 clauses** — what each one is for, and what
breaks without it — is in `LICENSES/ACD-1.0.clause-reference.md`. If a reviewer cites a
section number, that file answers it directly.

**What actually gets said on the list is recorded in `LICENSES/ACD-1.0.discussion-log.md`.**
That file is the bridge to the next step: the review submission cites it so that the earlier
discussion is visibly accounted for rather than repeated.

---

## A. Facts you will be asked for (both bodies)

| Field | Value |
|---|---|
| Full name | Autonomous Commons Dedication 1.0 |
| Short identifier | `ACD-1.0` |
| Licence steward | Yuta Yokoi (横井雄太) |
| Canonical text | `https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt` |
| SPDX XML | `https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.spdx.xml` |
| Project using it | `https://yutapr0117-design.github.io/portfolio/` (source: `https://github.com/yutapr0117-design/portfolio`) |
| OSI-approved | Not yet (this submission) |
| Reusable by others | Yes — Section 16.3 states it is not specific to any project, person, organisation, jurisdiction, or field |

---

## B. OSI License Review — ready-to-send message (**not yet sent**)

> **This is the approval-request step, and it has not been taken.** What is currently open is a
> thread on `license-discuss`. Send this only when the decision is to actually request approval.
>
> **Before sending, add a paragraph about the license-discuss thread.** The usual order is
> discuss → review, and a submission that arrives without referring to the earlier thread
> reads as though the earlier thread never happened — which costs credibility before anyone
> has evaluated the text. Pick three points from `LICENSES/ACD-1.0.discussion-log.md`
> (strongest objection / what was conceded / what changed) and use the template in section 3
> of that file. **If something raised there is still unanswered, say so** — hiding it fails
> the moment the person who raised it is also on license-review.

Send to `license-review@opensource.org` (subscribe first). OSI asks submitters to state
the rationale, to distinguish the licence from the closest approved one, to address the
Open Source Definition, and to say where the licence is used.

---

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

The committee's own words are worth quoting, because they state the doctrine and the escape from
it in one sentence: the Unlicense "is an attempt to dedicate a work to the public domain (which,
taken alone, would not be approved as an open source license) but it also has wording commonly
used for license grants."

**Four differences from that precedent, all of which cut against this submission and are stated
here rather than left to be discovered.**

1. **The Unlicense entered by a request for *legacy* approval** — it was already in widespread
   use by many unaffiliated parties, and that adoption carried weight the text alone might not
   have. ACD-1.0 has one adopter and cannot borrow that argument. It has to stand on the text.
2. **The Unlicense was approved despite broad agreement that it is poorly drafted.** ACD-1.0
   errs in the opposite direction: 16 sections and 82 clauses, which will draw the opposite
   criticism — that it is too long for what it does (answered at length in
   `ACD-1.0.review-responses-meta.md` Q17). That trade was made deliberately. Where the
   Unlicense's brevity left questions to be resolved by argument, this text tries to answer them
   in the text, and pays for it in length.

3. **That approval rested on legal advice.** The committee recorded that legal advisors
   concluded the document "would most likely be interpreted as a license and that the license met
   the OSD." That is the decisive step, and it is precisely the step this submission cannot
   replicate: no lawyer has read ACD-1.0 (§5, §4c). Where the Unlicense had counsel's reading to
   resolve the dedication-versus-licence question, this submission has only the structure of the
   text and whatever reading the list gives it.
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

### 3. Open Source Definition conformance

ACD-1.0 imposes no conditions at all, so conformance is straightforward. Addressing the
criteria the committee asks submitters to speak to directly:

- **OSD 1 (Free redistribution).** Section 4.2 permits distribution and sale by any means;
  Section 4.3 attaches no condition, including no royalty.
- **OSD 2 (Source code).** The licence permits distribution in source form, object form,
  or any other form (4.2), and imposes no obstacle to providing source.
- **OSD 3 (Derived works).** Section 4.2 permits modification and derivative works;
  Section 4.3 forbids any reciprocal-licensing condition; and Section 4.5 states the
  consequence positively — the Work and any adaptation or collection containing it may be
  distributed under any terms the recipient chooses, **including terms incompatible with
  these**, with nothing reaching through to their recipients. A recipient may therefore
  place the Work inside a copyleft project without friction.
- **OSD 4 (Integrity of the author's source code).** No restriction is imposed. Section
  16.4 concerns the text of the licence *as a document*, not the licensed work; Sections
  10.5 and 16.5 state this expressly.
- **OSD 5 (No discrimination against persons or groups)** and **OSD 6 (No discrimination
  against fields of endeavour).** Section 4.3 states that the licence is conditioned on no
  restriction as to persons, groups, technologies, endeavours or jurisdictions, and on no
  field of use.
- **OSD 7 (Distribution of licence).** Section 2.3 makes the licence effective without any
  act of acceptance; Section 16.2 makes an identifier or SPDX tag sufficient notice, so
  rights attach to every recipient without further action.
- **OSD 8 (Licence must not be specific to a product).** Section 16.3.
- **OSD 9 (Licence must not restrict other software).** Sections 4.3 and 10.1 impose no
  requirement on anything distributed alongside the Work.
- **OSD 10 (Licence must be technology-neutral).** Section 2.3 requires no click-through
  or other individual act of assent; Section 5.2(b) forbids imposing one by collateral
  means.

### 4. What is deliberately absent

Omissions are design decisions too, and the committee will ask about several of them.

- **No patent retaliation.** A grant that ends when the licensee litigates is a grant with
  a condition. Section 8.2 says the absence is deliberate so that it is not mistaken for an
  oversight.
- **No attribution requirement.** Attribution is a real wish, so Section 10.3 separates the
  wish from the obligation: any request the licensor makes, however phrased and wherever
  expressed, is a request and not a condition; not observing it is not a breach and narrows
  no permission.
- **No field-of-use restriction of any kind**, including the "ethical" restrictions now in
  circulation. Section 4.3 forecloses them expressly (OSD 6).
- **No choice of law or forum.** Section 15.7. Naming one jurisdiction would disadvantage
  recipients everywhere else.
- **No anti-DRM condition on the licensee.** A licence that imposes nothing cannot impose
  this either. The same protection is achieved from the other side: Section 5.2(a) is a
  covenant by the *licensor* not to apply technological measures to the Work or to invoke
  anti-circumvention law against You.
- **No barrier to translation.** Section 16.4 fixes the text that the name denotes, but
  Section 16.5 makes a translation an express exception: it may carry the name and the
  identifier so long as it is identified as a translation and states that the English text
  prevails. A rule that kept translations out would have put Section 16.4 at odds with
  Section 15.8 and would have kept the licence away from readers who do not read English.
- **No trademark licence.** Section 11.1. Trademarks identify origin, and an unconditional
  grant would mislead. Section 11.2 preserves truthful nominative reference.
- **No provenance or disclosure requirement for AI output.** Section 6.4 says outputs are
  unencumbered; requiring their labelling would contradict the licence's central purpose.

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

**Timeline expectations are the reviewers', not mine.** The process describes review on the order
of two months; this submission sets no deadline and asks for no expedited handling. If the
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
| No placeholder or replaceable text (`<year>`, `[name]`, templates) | `grep -cE "<[a-z]+>\|\[year\]\|\[name\]\|YYYY" LICENSES/ACD-1.0.txt` | **0** |
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

### 4c. What was verified mechanically, since it was not verified legally

No lawyer has read this. That is stated plainly in §5 and it is the weakest point of the
submission. It cannot be repaired by asserting confidence, so what follows is the opposite: the
narrow set of properties that **can** be established without counsel, each with the command that
establishes it. None of these substitute for legal review. They only mean that the failures a
machine can find are not present.

| Property | Command | Result |
|---|---|---|
| Every defined term is actually defined, in one place | `grep -nE '^\s+1\.[0-9]+\s+"' LICENSES/ACD-1.0.txt` | 10 terms, all in §1.1–§1.10 |
| No defined term is dead (each is used outside its own definition) | count occurrences of each term outside quotes | 10/10 used; lowest is `Contribution` at 4 |
| Section numbering is contiguous with no gaps | `grep -cE '^[0-9]+\. [A-Z]' LICENSES/ACD-1.0.txt` | 16 sections, numbered 1–16 |
| Internal cross-references all resolve to a clause that exists | enforced in CI (Check 441b) | no dangling `§N.M` |
| The text is pure ASCII | byte scan for values > 127 | **0** non-ASCII bytes |
| The authoritative language is stated in the text itself | `grep -n "authoritative language" LICENSES/ACD-1.0.txt` | §15.8 — English governs; translations are convenience only |
| No project-specific or replaceable text | see §4b | 0 and 0 |

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
- **Form.** The instrument is styled a *dedication* and contains a public-domain dedication
  (Section 3). I am aware of the committee's history with dedication-shaped instruments.
  Section 4 is a licence granted **independently** of Section 3 and expressly does not
  depend on Section 3 being ineffective (2.4, 4.4). Where Section 3 operates, Section 4 is
  redundant but not void and remains available to be relied upon. The licence is therefore
  a licence in its own right, and is what I ask the committee to review.

Thank you for your time.

Yuta Yokoi

---

## C. SPDX License List — ready-to-paste request

Submit via https://tools.spdx.org/app/submit_new_license/ (preferred) or the
`spdx/license-list-XML` new-license-request issue template.

- **Full name:** Autonomous Commons Dedication 1.0
- **Short identifier requested:** `ACD-1.0`
- **OSI approved:** No. Not submitted to OSI License Review either — only discussed on license-discuss
- **Licence text URL:** https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt
- **SPDX XML:** `LICENSES/ACD-1.0.spdx.xml` in the repository below, generated from the
  text by `npm run spdx-xml` and kept in sync by a blocking CI check, so the submitted
  markup cannot drift from the published text.
- **Evidence of use:** https://github.com/yutapr0117-design/portfolio — the licence covers
  the whole repository (source, documentation, data, and media assets) and is declared in
  `LICENSE`, in `link rel="license"`, in the JSON-LD `license` property of every
  CreativeWork node, in `sitemap.xml`, in `.well-known/aio-manifest.json`, and in the
  `llms.txt` family, each of which is checked in CI.
- **Not a duplicate:** it is not a variant of any listed licence. A clause-level comparison
  with 0BSD (closest on "zero conditions") and Apache-2.0 (closest on "express patent
  licence") is given in section B.2 above.
- **Steward commitment:** I am the steward. Once `ACD-1.0` is on the list I will not modify
  the text that the identifier denotes. Any later improvement will be issued as a distinct
  version (`ACD-1.1`, `ACD-2.0`) with its own identifier. Section 16.4 of the text itself
  forbids distributing a modified text under the same name or identifier.

---

## D. Before sending — checklist for the human

1. `LICENSES/READY-TO-SUBMIT.md` exists (it is written only when the text is judged ready).
2. The published copies resolve:
   `curl -sI https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt`
3. `npm run verify` exits 0 (this proves the XML matches the text, the cross-references
   resolve, and every declaration surface agrees).
4. Subscribe to `license-review@opensource.org` before posting; the list rejects mail from
   non-subscribers.
5. Expect roughly 60 days to a decision from first posting.
6. **Fold in the license-discuss summary** (section 3 of `LICENSES/ACD-1.0.discussion-log.md`).
   Three points, not the whole log. If the log is empty, say the thread drew no response —
   that is also a fact about the licence, and stating it is better than implying a debate
   that did not happen.
7. **Re-read section E** of this file. Its disclosures apply to whatever is posted, and the
   provenance one (E.1) is the disclosure most likely to be discovered independently.

---

## E. Addendum (2026-08-26) — disclosures that section B does not contain

Section B was written before the text was frozen and before the anticipated-objection
dossier existed. Reviewing the two against each other surfaced one disclosure that the
dossier argues is mandatory and that section B does not make. **Section B is not rewritten
here, because it may already have been sent.** Add the following in a follow-up message,
or fold it into section 5 if section B has not gone out yet.

### E.0 Which list this is on

If the thread is on `license-discuss`, say so plainly, and say what you want from it:

> I have posted this to license-discuss rather than license-review on purpose. I am not
> asking for approval yet. I would like to know whether this instrument is necessary at
> all, and where it is wrong, before taking anyone's time with a formal request.

### E.1 Provenance of the drafting

- **Provenance of the drafting.** The text was drafted by an AI agent operating
  autonomously in this project. **I did not write it, I did not direct the drafting, and
  I did not ask for it** — the agent determined that the repository needed a licence,
  designed one, and wrote it, and I learned that it existed afterwards. What is mine is
  what happened next: I decided to keep it, it is applied to **my** work, and — on a
  recommendation that also came from an AI, not from me — I brought it here. **I do not
  review the repository**; what reaches me is a summary, not the files. **The licence is the
  exception: I read it in full and understood it before sending.** I am the Dedicator and the
  steward and I answer for it, but at no point was I its author. The project states publicly that it
  operates this way — the human role is direction and audit, not implementation. The text cites exactly one external
  instrument (Article 4(3) of Directive (EU) 2019/790, in Section 1.10), deliberately,
  because invented or misattributed authority is the characteristic failure of
  machine-drafted legal text. Its internal consistency — contiguous clause numbering,
  resolution of all 82 cross-references, use of all 10 defined terms, absence of any
  obligation-imposing word directed at the user, and absence of anything specific to my
  project — is enforced in continuous integration, so those are conditions the repository
  cannot be in violation of rather than assertions of care. What none of that establishes
  is that the reasoning is sound, which is what I am here to find out.

### E.2 What would cause the submission to be withdrawn

Section B explains why the licence is necessary but does not say what would end the
matter. Stating it makes clear that this is an enquiry rather than an advocacy exercise.

- If someone shows me an existing approved licence that provides all three of the
  properties in section 1, I will use it and withdraw this submission.

The fuller set of withdrawal criteria — decided in advance, so that the decision is not
made in the heat of a thread — is in `LICENSES/ACD-1.0.review-responses-meta.md`.
