---
file: LICENSES/REVIEWERS.md
audience: OSI license-discuss / license-review participants, licence reviewers, anyone arriving from the mailing list
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.txt (the text posted, and the one this repository applies) / LICENSES/ACD-1.1.txt (the frozen successor) / LICENSES/FROZEN.md (freeze + venue, single source) / LICENSES/rounds/2026-08-26-license-discuss-sent.txt (what was actually sent) / LICENSES/ACD-1.0.submission.md (the packet prepared for license-review)
---

# Reviewing ACD — start here

## The short path, and what it costs you

**You are a volunteer. Nothing here is required reading.** Measured 2026-09-24, this directory
is **295,277 words** — **60 times the licence** — and that figure *understates* it: it splits on
whitespace, and much of the directory is Japanese, which is not space-delimited (a further
~359,000 Japanese characters are not counted as words at all). The whole of it exists so that a
claim we make can be checked, **not so that it must be**. *(The count grows with every entry;
it was 251,824 two days earlier. To re-measure: `git ls-files -z LICENSES | xargs -0 cat | wc -w` —
the `-z` matters, because three file names are Japanese and the plain form silently skips them.)*

**If you read three things you have checked the parts that decide the question:**

| | words | why |
| :-- | --: | :-- |
| [`ACD-1.0.txt`](ACD-1.0.txt) | **4,896** | the licence. Nothing outside it fixes it |
| the two facts at the top of [`ACD-1.0.against.md`](ACD-1.0.against.md) | ~400 | **no lawyer has read this text**, and **the only project using it is the author's**. Either is a sufficient reason to decline |
| [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md) | **949** | every objection we found on these lists in 24 months, and whether it lands |

**≈ 6,250 words.** **What you give up by stopping there**: the clause-by-clause reasoning, the
jurisdiction analysis, and the archive measurements — **all of which are evidence for claims,
not claims themselves.** The four commands below check the licence text without trusting any
of it.

---

This page is in English because the discussion is. Most of the supporting analysis in this
directory is written in Japanese; this page tells you what each document contains so you can
decide what is worth translating, and gives you the commands to check the claims yourself.

## In one screen

- **What it is.** A dedication of copyright and neighbouring rights to the public, **plus a
  licence granted independently of it** (§4.4), for works meant to be learned from. One file,
  16 sections, no placeholders in the clauses (the one blank, in §16.1's notice template, goes
  in the adopter's own notice).
- **The gap it claims, in one sentence.** **No OSI-approved instrument grants all three of these
  at once**: (i) a grant that expressly reaches **non-copyright rights in data** — the EU sui generis
  database right and its own verbs, *extraction* and *re-utilisation*; (ii) a **patent licence that
  survives the transformation of the work into a model** and its outputs; and (iii) **no condition
  on you at all**. Two of the three exist in several places; the three together do not.
  **Measured over the whole approved list rather than over comparators we chose**: of the
  **141 licences SPDX marks OSI-approved and not deprecated, exactly three impose no condition
  on the licensee** — **0BSD, MIT-0 and the Unlicense** — and **none of those three contains the
  word *patent* at all**, while the Unlicense limits itself in terms to *"any and all
  **copyright** interest"*. The census, its method, and the two places where an English-keyword
  count got it wrong (a German text and a French one) are in
  [`ACD-1.0.gap-measurements.md`](ACD-1.0.gap-measurements.md) §1.97.
  **This is checkable from the grant clauses themselves**, not from what the texts omit:
  Apache-2.0 §2 calls itself a *"copyright license"* and its §3 patent grant is bounded by *"the
  Work"*; 0BSD and the Unlicense enumerate copyright verbs (the Unlicense dedicates *"copyright
  interest"* in terms); CAL-1.0 §3.1(a) **does** reach *"non-patent intellectual property laws of
  any jurisdiction"* — but it is conditioned on its §4, and its patent grant expressly excludes
  claims infringed only *"by combination"*. The clause-by-clause comparison is
  [`ACD-1.0.gap-measurements.md`](ACD-1.0.gap-measurements.md) §1.96.
  **What this does not claim**: MIT's *"deal in the Software without restriction"* may well reach
  those rights by implication. The argument is that it is **left to interpretation**, and §6.5 of
  this text holds that a permission an automated system cannot determine is, for a work meant to be
  learned from, no permission at all. **That is a design argument, not a legal opinion.**
- **The same gap, in detail.** No approved licence does these three together: expressly permits machine
  learning and text-and-data-mining and makes no reservation (§6); grants a patent licence that
  reaches **models and outputs** of computational use (§8.4); and makes your permissions
  independent of whether copyright subsists in machine-generated material at all (§9).
- **Nearest approved licences.** Closest in effect to the Unlicense, MIT-0 and 0BSD (and to CC0,
  which is **not** OSI-approved); closest in patent machinery to Apache-2.0. What it adds to each
  is the three items above. **Against three it adds less**: UPL-1.0, BlueOak-1.0.0 and
  BSD-2-Clause-Patent already combine a permissive grant with an express patent grant under one
  notice condition — there the difference is that condition, not the patent grant
  ([`submission-reference.md`](ACD-1.0.submission-reference.md) §2).
- **The two weaknesses, first.** **No lawyer has read it**, and **it has one adopter — this
  repository**. Both are stated at length below and neither is repaired anywhere in this directory.
- **Anyone can adopt it.** Zero project names, no placeholders in the clauses (only §16.1's notice template has a blank, filled in the adopter's own notice), no editing of the licence text required — the
  commands to check that are below.
- **If you read one more thing**, read [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md):
  every objection raised on the lists, which ones land, and the clause that answers each.

## Which text you are looking at

**There are two frozen texts, and they are frozen for different reasons.**

| | |
| :-- | :-- |
| [`ACD-1.0.txt`](ACD-1.0.txt) | **The text posted to `license-discuss` on 2026-08-26, and the licence this repository applies.** Frozen since 2026-08-24 so that the text under discussion does not move. |
| [`ACD-1.1.txt`](ACD-1.1.txt) | **The successor, frozen 2026-09-17.** When it was frozen it closed nineteen of the twenty-one defects then recorded in [`ACD-1.0.errata.md`](ACD-1.0.errata.md); the list has kept growing since, and each entry says which version addresses it. It has **not** been submitted to `license-review` and is **not** applied to this repository. |

**Work on the next version happens in [`ACD-1.2-DRAFT.txt`](ACD-1.2-DRAFT.txt)**, so neither
frozen text moves while it is being discussed. Both are pinned by SHA-256 in
[`FROZEN.md`](FROZEN.md) and checked in CI; the command to verify that is below.

**Clause numbers do not transfer cleanly between the two, and this matters when you read the
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

**Posting resumed 2026-09-17, when the owner sent a short ACD-1.1 discussion request in his own words.** What follows is the history that stopped it, and it has not been withdrawn. **On 2026-09-09** the OSI Moderators posted to both lists that they *"will reject posts where we suspect that an AI has been responsible for all or most of a message"* and that the lists *"are being used as a proof-of-concept to demonstrate that an AI system can autonomously engage and even draft an open source license for review"*. **No name is given in the notice. What we can say is narrower and stronger: two days before it, on 2026-09-07, a moderator put the same question to us directly and by name** — five questions about whether an AI drafts our messages, whether anything posts autonomously, whether ACD-1.0 was AI-drafted, whether testing autonomous participation is an objective, and whether the steward takes responsibility. **The steward answered all five and we have published the exchange verbatim** (`rounds/2026-09-07-offlist-nick-vidal-moderator-exchange.txt`; it is off-list, so it is not in the public archive and you cannot verify it there). **The moderator asked that we reply before any further ACD-1.0 submission; that reply has been sent, and no response to it has arrived.** **We do not assert that the public notice is about us alone** — but the description fits this project, whose licence was drafted by an AI agent (disclosed in `ACD-1.0.submission.md` §E.1 since before the frozen text was posted). **Nothing was sent to either list between 2026-09-09 and 2026-09-17, when the owner decided**, and he is in a direct, off-list exchange with the moderator personally about it — **the policy decision belongs to OSI as an organisation and is not that exchange** (his statement, 2026-09-09; it will be published verbatim in `rounds/` when it concludes). **He states that the human decides the direction and that he checks and sends the messages himself** — the notice rejects posts made *"without careful review from the author"*, and that is the line it draws. The verbatim notices are in `rounds/`; the analysis is `against.md` #119 and `ACD-OSI-BOTTLENECKS.md` B14. **We are not reducing the disclosure in response.**

**Posted to `license-discuss` and received. No responses yet.** That list is for general
discussion — it is **not** the approval venue. Nothing has been submitted to `license-review`,
and nothing has been submitted to SPDX.

**ACD-1.1 was frozen on 2026-09-17** (`ACD-1.1.txt`, pinned by SHA-256 in `FROZEN.md` and
verified in CI). When frozen it closed nineteen of the twenty-one defects then recorded in ACD-1.0.
**The owner sent it to `license-discuss` the same day, and that message was rejected by moderation**
(`ACD-1.0.against.md` #215), so the list has not yet received this text; **work on the next version happens in `ACD-1.2-DRAFT.txt`,
so the text under discussion does not move.** **ACD-1.0 remains frozen and remains the licence
this repository applies** — freezing a text is a promise about its bytes, not a statement about
which version a project uses, and the two facts are deliberately kept apart here.

**How it came to be on this list.** **No submission to license-review has been made, and the text
now frozen is not what will be submitted there.** The sequence — post to license-discuss, collect
what the list says, fold it into a revised version, and submit **that** to license-review — is the
plan the owner has held from the outset, and it does not end at one submission: review comments
feed a further revision, repeated as needed. **This paragraph is corrected as of 2026-09-09**; it
previously said the ordering "reflects OSI's guidance rather than foresight on our part", which
understated the owner's own plan, and before that it overstated it. **The correction rests on the
owner's direct confirmation, not on inference from the repository**, which is why it is dated and
marked. What is our own decision is the SPDX timing: SPDX asks for substantial
real-world use, this work has one adopter, and we are not submitting something that does not
meet the stated bar.

**A successor exists and is not in force.** `LICENSES/ACD-1.1.txt` was frozen on 2026-09-17 and says what it is in its own first line — **"FROZEN TEXT. NOT SUBMITTED FOR APPROVAL. NOT APPLIED TO THIS REPOSITORY."** — and work on the version after it happens in `LICENSES/ACD-1.2-DRAFT.txt`, whose first line says **NOT IN FORCE, NOT SUBMITTED, NOT APPLIED**. They are mentioned here because you would find them anyway, and because the alternative reading — that we are quietly revising the text under discussion — is the one thing they must not be mistaken for. **Clause numbers differ from 1.0 in §1 (the definitions were reordered) and in §15–§16** — the measured map is under "Clause numbers do not transfer cleanly" above — so a citation to 1.0 must use the 1.0 text. **⚠ ACD-1.1's own header says the numbers differ only "after Section 15"; that is incomplete, and because the text is frozen it stays so (`ACD-1.1-SELF-AUDIT.md` §3n).** A CI check requires the draft to keep declaring what it is.

The text is **frozen** while this is open. `LICENSES/FROZEN.md` exists to say so, and
**Check 453 in CI pins the SHA-256 of five files** — the three submitted ones
(`ACD-1.0.txt`, `ACD-1.0.spdx.xml`, `ACD-1.0.machine.json`) and the two that carry the
**frozen successor** (`ACD-1.1.txt`, `ACD-1.1.machine.json`), which is **not in force,
not submitted for approval and not applied** — so that an accidental edit fails the build rather than
silently changing the text you are reading. If you find a defect in the text, it will be **reported, not quietly
patched** — changing the wording underneath a live discussion would make your review of it
meaningless.

## The case, and the strongest thing against each part of it

Nothing here is new; it is the argument from
[`ACD-1.0.submission.md`](ACD-1.0.submission.md) §1–§4 compressed, with the best counter to each
line placed beside it rather than further down. **The adverse case is the longer document and it
is the one to read first** — this is only a map of where the argument runs.

**Start with what cannot be answered.** No lawyer has read this licence, and none has been
engaged ([`against.md`](ACD-1.0.against.md) #1). The step that resolved the closest precedent —
legal advisors concluding the Unlicense "would most likely be interpreted as a license and that
the license met the OSD" — has no counterpart here (#2). **And the precedent has not been
repeated**: searching the public review tracker's 252 records for this family returns one approval —
the Unlicense, 2020, on a legacy basis we cannot use — and one contemporary attempt, still
unresolved, whose author was told on this list that a waiver of this kind needs a lawyer (#87).
**Those three are stated first because they are the three we cannot fix.**

| The claim | The strongest thing against it |
|---|---|
| **The gap is real**: no approved licence expressly permits training and text-and-data-mining, grants patents reaching models and outputs, and declines to presume that rights subsist in machine-generated material (§6, §8.4, §9) | **Four of the seven distinguishing features close if the incumbents amend** — and we say which four ([`comparison.md`](ACD-1.0.comparison.md) §1.35). The case then rests on the remaining three. **And the patent limb holds only as "names models"**: CERN-OHL-P-2.0 grants patents over *Products* — *"any … work … arising from the … processing of Covered Source"* — which can be read to reach a trained model ([`submission-reference.md`](ACD-1.0.submission-reference.md) §2, [`gap-census.md`](ACD-1.0.gap-census.md)) |
| **It is reviewable**: §3 surrenders, §4 grants a licence *independently* (§4.4), so a reader never has to decide whether the surrender worked | **No court has characterised this construction**, in any jurisdiction (#3), and **no submission of this shape has been approved since 2020** (#87). A dedication taken alone is not approvable, and the escape is untested |
| **It imposes nothing**: §10.1 and §4.3 attach no condition, so no obligation can fire in any delivery mode — the failure that condition-bearing instruments meet in hosted deployment | **The same structure weakens the warranty disclaimer** (#41) and forecloses defensive patent termination (#46). Both costs fall on the adopter, and both are deliberate |
| **Anyone can adopt it**: zero project names, no placeholders in the clauses (one blank in §16.1's notice template), no editing of the licence text required — verifiable with the commands below | **One adopter: this repository** (#4). Reusability is a structural property; adoption is a social one, and only the first is shown |

## What to open first

> ⚠ **This heading said "The three things you probably want first" until 2026-09-09; the table
> below has eight rows.** A number written into a heading stops matching the moment a row is
> added, and this is the page a reviewer is asked to trust. The convention used elsewhere in this
> directory is to **enumerate rather than count**, and it is now used here.

**Reading order, stated because the table has eight rows and two of them used to claim to be first.** If you have ten minutes: the objection map, then the licence. If you are deciding: add what was actually sent, and the errata. **The case against is the full record and the longest document in this directory** — it is where the objection map points, not a substitute for it. Nothing in it is summarised away anywhere else, and **nothing in it will be shortened**: this directory treats a shrinking adverse list as erasure rather than improvement (`REVISION-PROTOCOL.md` §2).

| | File | Note |
|---|---|---|
| **What is blocking approval** | [`ACD-OSI-BOTTLENECKS.md`](ACD-OSI-BOTTLENECKS.md) | **The register.** Fourteen items, each with why it is an approval problem, what is fact and what is inference, the smallest resolution, what would be lost, and who can move it — **four are marked highest severity, and none of them is repaired by editing the licence**: no legal review (B1) and one adopter (B2) advance only by submitting and by time; whether the gap justifies a new licence is OSI's call (B10); and the moderators' notice about AI-written posts is being handled by the owner directly (B14). Its summary line is derived from the table by a CI check, so it cannot quietly understate what is left |
| **Which known objections land** | [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md) | **One table.** Every objection **we have found** in the `license-review` / `license-discuss` archives of the last two years **that bears on a public-domain-equivalent or AI-facing instrument** — found by a subject census plus reading the threads that matched, which is **a floor, not a census of every objection ever raised** (#87). Whether each applies to ACD-1.0, and — for the ones that do not — the clause that answers it. **Objections that land are listed first** |
| The licence itself | [`ACD-1.0.txt`](ACD-1.0.txt) | 597 lines, 16 sections. Plain ASCII, no placeholders in the clauses (one in §16.1's notice template) |
| **What was actually sent** | [`rounds/2026-08-26-license-discuss-sent.txt`](rounds/2026-08-26-license-discuss-sent.txt) | The `license-discuss` post of 2026-08-26, verbatim from the public archive. 5,778 words |
| The packet prepared for `license-review` | [`ACD-1.0.submission.md`](ACD-1.0.submission.md) | English, **not yet sent anywhere**. Gap statement, comparison, OSD conformance, disclosures, and what is deliberately absent |
| **Looking for a specific answer** | [`QUESTION-INDEX.md`](QUESTION-INDEX.md) | 346 worked entries, indexed by the question rather than the filename |
| **The case against** | [`ACD-1.0.against.md`](ACD-1.0.against.md) | **The complete record, and the largest document here — six times the length of the licence.** All 249 adverse facts, written by us. Two have no answer; one of those is on its own a sufficient reason to decline |
| **Which facts have gone stale** | [`AS-OF.md`](AS-OF.md) | Every claim about the outside world, with the date it was last verified |
| **Known defects in the text** | [`ACD-1.0.errata.md`](ACD-1.0.errata.md) | 34 known imprecisions, all unrepaired while the freeze holds, with what 1.1 would do |
| Known weaknesses, longer form | [`READY-TO-SUBMIT.md`](READY-TO-SUBMIT.md) | Stated by us, before you have to find them |

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
# the two digests must be identical; as of 2026-09-07 both are
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

# Verify that the text you are reading is the text that is pinned      → 5× OK
grep -E "^[0-9a-f]{64}  " LICENSES/FROZEN.md | shasum -a 256 -c
```

The last one is the important one. `LICENSES/FROZEN.md` records the digests in the same format
`shasum` emits, so the check is a single pipe with no trust in anything this repository says
about itself: if the licence text had been altered since the discussion began, that line would
print `FAILED` instead of `OK`. It currently prints `OK` for all five files.

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

**The documents a reviewer is most likely to want are already in English**: the adverse case, the
errata, this page, the question index, the submission packet, and both of the anticipated-response
files that deal with clauses and with comparison. What is Japanese is mostly the clause-by-clause
reference and the jurisdiction map.

If something you need is only in Japanese and matters to your review, say so on the list and it
will be translated. Nothing here is withheld — the language is an artefact of who wrote it, not
a choice about who should read it.

### The rest of the directory, in one line each

The table above is where to start. It is not the inventory, and until 2026-09-20 this page did
not mention the following files at all — including the register of what we believe stands
between this instrument and approval, which is the most self-critical thing here.

| File | Language | What is in it |
|---|---|---|
| [`ACD-OSI-BOTTLENECKS.md`](ACD-OSI-BOTTLENECKS.md) | Japanese | **The register of what we think blocks approval** — fourteen entries with severity, who can move each, and none marked resolved |
| [`ACD-OSI-BOTTLENECKS-EXTERNAL.md`](ACD-OSI-BOTTLENECKS-EXTERNAL.md) | Japanese | The entries whose answer is not ours to give (legal review, adoption, the gap question, the moderator decision) |
| [`ACD-1.0.review-precedents.md`](ACD-1.0.review-precedents.md) | Japanese, quoting English verbatim | What this list has actually done to submissions of our shape, read from the archives |
| [`ACD-1.0.review-corpus.md`](ACD-1.0.review-corpus.md) | Japanese, quoting English verbatim | Measurements over the archives as a whole, as distinct from readings of single threads |
| [`ACD-1.0.review-rules.md`](ACD-1.0.review-rules.md) | Japanese, quoting English verbatim | The OSI's own published pages, read at source and applied criterion by criterion |
| [`ACD-1.0.board-decisions.md`](ACD-1.0.board-decisions.md) | Japanese, quoting English verbatim | The board's published minutes — where decisions are recorded, which the mailing list does not record |
| [`ACD-1.0.reviewer-positions.md`](ACD-1.0.reviewer-positions.md) / [`ACD-1.0.review-labels.md`](ACD-1.0.review-labels.md) | Japanese | Positions taken by named participants, and the labels this list uses for licences like this one |
| [`AUDIT-LEDGER.md`](AUDIT-LEDGER.md) | Japanese | How each class of claim in this dossier was verified, with the counts and the residue |
| [`BLIND-SPOTS.md`](BLIND-SPOTS.md) | Japanese | The dimensions we have used to look for our own defects, and the ones we have not |
| [`PEER-REVIEW-WATCH.md`](PEER-REVIEW-WATCH.md) | Japanese | Contemporary instruments under review, and what we would change if each is approved, rejected, revised or stalls |
| [`ACD-1.1-CHANGELIST.md`](ACD-1.1-CHANGELIST.md) / [`ACD-1.2-CHANGELIST.md`](ACD-1.2-CHANGELIST.md) | Japanese | What each successor draft changes, and why, one erratum at a time |
| [`ACD-1.1-SELF-AUDIT.md`](ACD-1.1-SELF-AUDIT.md) | Japanese | Defects the successor drafts introduce themselves |
| [`ACD-1.0.dig-2026-09.md`](ACD-1.0.dig-2026-09.md) | Japanese | The record of one archive excavation, kept because the method is reusable |

## What is not being asked for

Approval would mean the licence conforms to the Open Source Definition. It would not mean it is
recommended, popular or preferred. This submission makes no claim to those, and the honest
position is the narrow one.
