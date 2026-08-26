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

Anticipated objections and prepared answers (38 worked entries plus a table of 8 short answers, across three files) are in
`LICENSES/ACD-1.0.review-responses.md` and its `-clauses` / `-meta` companions.

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

- **Provenance of the drafting.** The text was drafted with a large language model under
  my direction, in a project that states publicly that this is how it operates. I mention
  it before anyone finds it in the repository. The text cites exactly one external
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
