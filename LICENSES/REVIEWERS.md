---
file: LICENSES/REVIEWERS.md
audience: OSI license-discuss / license-review participants, licence reviewers, anyone arriving from the mailing list
last-updated: 2026-11-27
clause-numbers: ACD-1.4
canonical-ref: LICENSES/ACD-1.0.txt (the text posted) / LICENSES/ACD-1.4.txt (the frozen successor this repository applies since 2026-11-23) / LICENSES/FROZEN.md (freeze + venue, single source) / LICENSES/rounds/2026-08-26-license-discuss-sent.txt (what was actually sent) / LICENSES/ACD-1.0.submission.md (the packet prepared for license-review)
---

# Reviewing ACD — start here

## The short path, and what it costs you

**You are a volunteer. Nothing here is required reading.** Measured 2026-11-26, the analysis in
this directory — everything except `rounds/` — is **659,644 words**, **112 times the licence**, and
more than that in fact, because Japanese is not space-delimited. `rounds/` holds the primary
sources verbatim so that every quotation can be checked against what was actually sent; **nobody
is asked to read it.** The whole of it exists so that a claim we make can be checked, **not so
that it must be**. *(Re-measure: `git ls-files -z LICENSES ':!LICENSES/rounds' | xargs -0 cat | python3 -c "import sys; print(len(sys.stdin.read().split()))"`. `wc -w` gives about 2% more, because it splits the Japanese text differently.)*

**If you read three things, you will have checked the parts that decide the question:**

| | words | why |
| :-- | --: | :-- |
| [`ACD-1.4.txt`](ACD-1.4.txt) | **5,879** | the licence: the version this repository applies and the one that would be submitted. Nothing outside it fixes it. [`ACD-1.0.txt`](ACD-1.0.txt) (4,896 words) is the text posted to `license-discuss` on 2026-08-26 and the base of [`REDLINE-1.0-TO-1.4.txt`](REDLINE-1.0-TO-1.4.txt), which shows every changed word |
| the two facts **#1 and #4** in [`ACD-1.0.against.md`](ACD-1.0.against.md) | ~220 | **no lawyer has read this text**, and **the only project using it is the author's**. These are the strongest points against it. Neither is one of the eight published criteria, and the Licensing Committee's chair has called legal review *"not a blocker"*, but a reviewer may weigh both |
| [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md) | **5,808** | every objection we found on these lists in 24 months, and whether it lands. The first table is the part that counts |

**≈ 11,905 words** *(`wc -w`, 2026-11-27.)* **What you give up by stopping there**: the clause-by-clause reasoning, the
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
  that is possible, and then grant a copyright license"*. ACD has both parts (§3, §4), with a licence that
  applies everywhere, and grants patents (§8). It imposes no condition (§10.1), so a condition, a
  field-of-use limit or discrimination — one of the two grounds on which submissions fail — has nothing
  to attach to. Each published criterion has an answer below.
- **The gap it claims, in one sentence.** **No OSI-approved instrument grants all three of these
  at once**: (i) a **patent licence that survives the transformation of the work into a model** and
  its outputs; (ii) **no condition on you at all**; and (iii) a grant that expressly reaches
  **non-copyright rights in data** — the EU sui generis database right and its own verbs,
  *extraction* and *re-utilisation*.
  **(i) and (ii) differ in effect; (iii) differs in what is stated, not in what an
  unrestricted permission may already reach.**
- **Measured over the whole approved list.** Of the **141 licences
  SPDX marks OSI-approved and not deprecated, exactly three impose no condition on the licensee** —
  **0BSD, MIT-0 and the Unlicense** — and **none of those three contains the word** *patent*. Seven extend a patent grant beyond the work itself, and **all seven carry a condition**
  ([`ACD-1.0.gap-measurements.md`](ACD-1.0.gap-measurements.md) §1.97, §1.133).
- **What this does not claim:** that existing licences forbid training. MIT's *"deal in the
  Software without restriction"* may well reach these rights. §6.1, §7 and §9 state expressly what a broad permission may already
  give, so **they are not grounds of uniqueness** (§1.134).
- **Nearest approved licences.** Closest in effect to the Unlicense, MIT-0 and 0BSD (and to CC0,
  which is **not** OSI-approved), and in patent terms to UPL-1.0, BlueOak-1.0.0 and
  BSD-2-Clause-Patent, which already combine a permissive grant with an express patent grant under
  one notice condition — **against those three it adds less**: the one difference established is that
  ACD has no such condition ([`gap-measurements.md`](ACD-1.0.gap-measurements.md) §1.133).
- **The three weaknesses, first.** **No lawyer has read it**; **it has one adopter — this
  repository**; and **it is long**: its terms run longer than GPL-3.0's, a length a Committee
  member has held, with other faults, against another licence. None is repaired here. The first two are not published
  criteria: the chair called legal review *"not a blocker"*, and a Committee rationale (2020) calls
  non-use *"not a basis for rejection that the OSI has applied in the past"*.
- **Anyone can adopt it.** It names no project and needs no editing.
- **If you read one more thing**, read [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md).

## The new language, next to the nearest approved text

*"It would probably be better for you to put up the language you think is innovative and we can
discuss those pieces."* (Bruce Perens, `license-discuss`, 2026-01-21, to the author of another
licence.) Here it is. The left column quotes **ACD-1.4**
([`ACD-1.4.txt`](ACD-1.4.txt)), the latest frozen text and the version we intend to submit; the middle column
quotes the nearest OSI-approved text we found.

| ACD-1.4 | Nearest approved text | The difference |
| :-- | :-- | :-- |
| §8.4: *"grants You a licence on the terms of Section 8.1 to put the Work to Computational Use and to make, have made, use, offer, sell, lend, lease, import, export, keep, possess, and otherwise practise or transfer any model, parameter set, weight, embedding, output, or other data, in each case resulting from Computational Use of the Work"* | UPL-1.0, one of the seven approved licences whose patent grant reaches beyond the work ([`gap-measurements.md`](ACD-1.0.gap-measurements.md) §1.133), extends it to *"(ii) the Larger Works (as defined below)"*: *"(b) any piece of software and/or hardware listed in the lrgrwrks.txt file if one is included with the Software"* | UPL reaches beyond the work only to what is **listed in advance** in a file shipped with it. A model trained on the work later cannot be listed. UPL also carries a notice condition |
| §10.1 of ACD-1.4: *"This Dedication imposes no condition, obligation, restriction, or requirement upon You in respect of the Work, other than in Your capacity as a Dedicator."* The closing words keep the promises a contributor makes as a Dedicator (§2.6, §5); none of them is a condition on using the Work | 0BSD: *"Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted."* | **Nothing, in this sentence alone** — 0BSD is as unconditional. What is new is the pairing with the patent grant above: none of the three approved licences without a condition contains the word *patent* (§1.97) |
| §7.2: *"You may extract and re-utilise the whole or any substantial part of the contents of the Work, repeatedly and systematically, without limit and without condition"* | **None that we found** names this right. CC0 1.0, which is **not** OSI-approved, lists *"database rights (such as those arising under Directive 96/9/EC"* among the rights it waives | A difference in what is **stated**, not necessarily in effect: an unrestricted permission may already reach this right. ACD-1.4 uses the Directive's own verbs. The right exists in the EU and the UK; Japan and the United States protect a database only as a creative compilation, so there §7 has nothing to reach and copyright in the compilation falls to §§3–6 |

**The defined terms.** *Work*, *You* and *Contribution* are Apache-2.0's words; *Moral Rights* is
one of CC0's listed rights; *the Steward* follows EPL's *Agreement Steward*; *Reservation* is tied to Article 4(3) of
Directive (EU) 2019/790. *Dedicator* plays the part of CC0's *Affirmer*: it surrenders rights (§3) and also licenses
them (§4, granted independently and not as a fallback) and its patents (§8). *Licensor* would
name only the second role. *Dedication* is CC0's
word. *Covered Rights* is ours: MPL's *Covered* names software, ours names the rights, so that one
term reaches copyright, neighbouring and database rights together. *Computational Use* and
*Machine-Generated Material* are new, and name what ACD adds.

**Why a new licence at all.** Bruce Perens wrote to submitters in 2018, as his own view and not
an OSI rule, that licences *"duplicative of other licenses in their effect should not be accepted
any longer, unless it's to meet new developments in case law or solve an obvious legal deficit."*
ACD's claim is that it is not duplicative (the table above); these two exceptions are a second
line, not the claim itself. The deficit is the one OSI's FAQ calls CC0's most
serious concern: a dedication that withholds patents (§8). The development is training on works
and the reservations made against it: in December 2025 the Hamburg Higher Regional Court held,
according to its press release, that an image agency's reservation against text and data mining
could be attributed to the rightsholder but failed for want of a machine-readable form (*Kneschke
v. LAION*), which is the question §6.2 settles for the Dedicator (`ACD-1.0.jurisdictions.md`
§9a). Against this: the reservation itself comes from legislation, not case law, and we have read
the court's press release, not the judgment; §10.1 alone duplicates 0BSD in effect; and the same
message says *"If you have not made use of an attorney in drafting your license, you are very
unlikely to understand how the courts would actually execute your license."* No lawyer drafted
this one.

**One definition a reader may misread.** In ACD-1.4, §1.7 defines *Computational Use* to include
*"the making, distribution, and use of any model, parameter set, weight, embedding, output, or other
data, in each case resulting from that processing"* (ACD-1.0 to 1.3 end the list at *"or output"*). That defines acts so that §6.1 can permit them; it does not say outputs are
derivative works. §6.4 of ACD-1.4: *"You owe nothing under this Dedication in respect of any of them"*, and
*"Whether a right subsists in any such thing is not decided here and does not need to be."* A
licence that deems outputs derivative and puts its terms on them (TRPL, `license-discuss`
2025-12) runs the other way.

**Why not an approved licence plus an additional permission?** Shuji Sado asked a submitter in
2026 for *"a brief explanation of why existing OSI-approved licenses plus additional
permissions/exceptions or guidance cannot achieve the same goals"*. For the patent grant, the
honest answer is that they could: an additional permission can grant a patent licence of any
reach, §8.4's included, and 0BSD plus a few hundred words would carry the first row of the table
above. What that would not remove: an identifier such as *0BSD WITH* an exception is read by
scanners only once the exception is on SPDX's list, so the cost of a new name stays; and the
exception would itself be new, unreviewed legal text. The approved precedent went the other way:
BSD-2-Clause-Patent was submitted as *"a simple permissive license that is compatible with the
GNU General Public License (GPL), version 2, but which also has an express patent grant
included"* and approved in 2017 as a licence of its own; we found no post in that thread asking
for BSD-2-Clause plus an exception instead (its stated reason was GPLv2 compatibility, which is
not ours). The rest of ACD — the surrender (§3), the covenants (§5), moral rights (§12) — is not
what the gap claim rests on; putting it in one instrument is a choice of form, not a claim of
difference. The question is being asked now, and a 2017 precedent may weigh less than it; and a short exception is easier to review than a long licence, which argues the other way.
([`ACD-OSI-BOTTLENECKS-EXTERNAL.md`](ACD-OSI-BOTTLENECKS-EXTERNAL.md) B10, H1-g.)


## Which text you are looking at

**There are five frozen texts, and they are frozen for different reasons.** *(2026-10-29: this table said "two" and named 1.0 as the applied licence after 1.2 and 1.3 had been frozen; corrected.)*

| | |
| :-- | :-- |
| [`ACD-1.0.txt`](ACD-1.0.txt) | **The text posted to `license-discuss` on 2026-08-26.** Frozen since 2026-08-24 so that the text under discussion does not move. This repository applied it until 2026-10-25. Every word changed since is in [`REDLINE-1.0-TO-1.4.txt`](REDLINE-1.0-TO-1.4.txt). |
| [`ACD-1.1.txt`](ACD-1.1.txt) | **The successor, frozen 2026-09-17.** When it was frozen it closed nineteen of the twenty-one defects then recorded in [`ACD-1.0.errata.md`](ACD-1.0.errata.md); the list has kept growing since, and each entry says which version addresses it. It has **not** been submitted to `license-review` and is **not** applied to this repository. |
| [`ACD-1.2.txt`](ACD-1.2.txt) | **The second successor, frozen 2026-10-17.** Its own header says what it is. It has **not** been submitted to `license-review` and is **not** applied to this repository. |
| [`ACD-1.3.txt`](ACD-1.3.txt) | **ACD-1.3, the third successor, frozen 2026-10-25.** This repository applied it from that date until 2026-11-23. It has **not** been submitted to `license-review`. |
| [`ACD-1.4.txt`](ACD-1.4.txt) | **ACD-1.4, the fourth successor, frozen 2026-11-23, and the licence this repository applies from that date** (the root `LICENSE` says so). It is the version this dossier prepares for submission (the submission target since 2026-11-23); it has **not** been submitted to `license-review`, and as of 2026-11-23 it had not been posted to any list (postings are recorded in [`FROZEN.md`](FROZEN.md)). What changed from 1.3, clause by clause, is in [`CHANGES-ACD-1.4.txt`](CHANGES-ACD-1.4.txt). |

**No frozen text moves.** A defect found in a frozen text is recorded (in the errata, or in the self-audit when a
successor introduced it) and repaired only in a later version. **If ACD-1.4 is submitted, it will not be changed while it is under review:** a later version would come only by withdrawing 1.4 and resubmitting, after the review comments have been gathered so that the changes come together — the review-process page's rule that a licence cannot be changed while it is being considered, as Pamela Chestek applied it to another submitter on `license-review`, 2026-03-15 (`ACD-1.0.review-readings-6.md` §1.471). All five are pinned by SHA-256 in
[`FROZEN.md`](FROZEN.md) and checked in CI; the command to verify that is below.

**Why each version changed, in English.** 1.0 → 1.1: the header of [`ACD-1.1.txt`](ACD-1.1.txt) and the entries of
[`ACD-1.0.errata.md`](ACD-1.0.errata.md) it closed (each entry names the version that addresses it); the reasoning
beyond that is only in Japanese (`ACD-1.1-CHANGELIST.md`, `ACD-1.1-SELF-AUDIT.md`). 1.1 → 1.2, 1.2 → 1.3 and 1.3 → 1.4:
the English change list each draft carried, kept word for word in the appendix of `ACD-1.2-CHANGELIST.md`,
`ACD-1.3-CHANGELIST.md` and `ACD-1.4-CHANGELIST.md` (the section headed "付録: 確定時点の草案ヘッダ（逐語）"), and for 1.4
also [`CHANGES-ACD-1.4.txt`](CHANGES-ACD-1.4.txt). Every word changed from 1.0: [`REDLINE-1.0-TO-1.4.txt`](REDLINE-1.0-TO-1.4.txt).

**Clause numbers do not transfer cleanly between 1.0 and its successors, and this matters when you read the
analysis in this directory, much of which was written against 1.0; this page cites ACD-1.4.** Measured, not assumed:

- **§2 to §14 — every clause number names the same subject in both texts, but several of those clauses were
  substantially rewritten**, among them §2.2, §2.6, §2.8, §2.9, §5.3, §8.4, §8.6, §12.2 and §14.2. A sentence quoted from
  one version is therefore no evidence of the other; [`REDLINE-1.0-TO-1.4.txt`](REDLINE-1.0-TO-1.4.txt) shows each change.
- **§1's definitions were reordered, so four of them changed number.** Matched by defined term:
  1.0's §1.2 *Work* is 1.2's §1.3, §1.3 *Dedicator* is §1.4, §1.4 *You* is §1.6, and §1.6 *Moral
  Rights* is §1.2. **The numbers all exist in both, so nothing dangles — they simply mean
  different things.**
- **§15 and §16 were shortened and renumbered.** 1.0's Sections 15.7 and 15.8 are 1.2's §15.3 and
  §15.4; 1.0's §15.2 has no counterpart in 1.1 but its three rules of construction were
  restored at 1.2's §15.5 (errata E24); **1.0's §15.3 likewise has no counterpart in 1.1 and
  is restored word for word at 1.2's §15.6** (errata E25); 1.0's §16.5 (translations) was
  absorbed into 1.2's §16.4, and **1.2's §16.5 is a different clause — the definition of the
  Steward**.
  **A citation to §1, §15 or §16 has to name the version.** The full map, citation by citation,
  is in [`ACD-1.2-CHANGELIST.md`](ACD-1.2-CHANGELIST.md).

## Status

**Posted to `license-discuss` and received. No responses in the archive when last read, 2026-11-27 00:01 UTC.** (The October archives of both lists were unchanged; the November archives held three messages on `license-discuss` and one on `license-review`, all on other subjects (the last a reminder about the PSF-2.0 submission of 2026-09-09) — see `OSI-EVENTS-2026-10.md`.) That list is for general
discussion — it is **not** the approval venue. Nothing has been submitted to `license-review`,
and nothing has been submitted to SPDX. SPDX asks for substantial real-world use, this work has
one adopter, and we are not submitting something that does not meet the stated bar.

**What will be submitted is a later version, not 1.0.** The sequence — post to `license-discuss`,
collect what the list says, fold it into a revised version, submit **that** to `license-review`,
and repeat on the review comments — is the plan the owner has held from the outset (his direct
confirmation, 2026-09-09). The owner sent ACD-1.1 to `license-discuss` on 2026-09-17, and **that
message was rejected by moderation** (`ACD-1.0.against.md` #215), so the list has not received
that text. **The version to be submitted will itself go to `license-discuss` first, for at least
30 days, before anything goes to `license-review`**, as Pamela Chestek advised another submitter
in January 2026. No frozen text moves while this is open.
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
**Check 453 in CI pins the SHA-256 of twelve files** (`FREEZE-DATA` in `FROZEN.md`:
each frozen text and descriptor, and the SPDX XML of 1.0 and 1.4), none of them
submitted for approval (ACD-1.4 is the one this repository applies) — so that an accidental edit fails the build rather than
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
| **The gap is real**: no approved licence does all three of the things stated in "In one screen" above — grant patents that name models and outputs (§8.4), impose no condition (§10.1), and reach the sui generis database right with its own verbs (§7.2). On top of these it states expressly what others leave unsaid about training and text-and-data-mining (§6), and it declines to presume that rights subsist in machine-generated material (§9) — which grants nothing new today, but is one of the three differences the next column says an amendment of the incumbents cannot close. Each limb alone has neighbours, as the next column says | **Four of the seven distinguishing features close if the incumbents amend** — and we say which four ([`comparison.md`](ACD-1.0.comparison.md) §1.35). The case then rests on the remaining three. **And the patent limb is narrower than it sounds**: CERN-OHL-P-2.0 grants patents over *Products* — *"any … work … arising from the … processing of Covered Source"* — which can be read to reach a trained model ([`submission-reference.md`](ACD-1.0.submission-reference.md) §2, [`gap-census.md`](ACD-1.0.gap-census.md)). What remains is naming the artefact, and the combination: that reach with no condition and no termination, which no approved licence has (CERN-OHL-P-2.0 conditions conveying a Product in §4 and can end in §6.2; [`gap-measurements.md`](ACD-1.0.gap-measurements.md) §1.133). **We do not claim a difference in claim scope**: CERN-OHL-P-2.0 §6.1 grants claims *"necessarily infringed by exercising rights under the Covered Source as Conveyed"*, and if that includes making and using Products it is close to the limit §8.4 has carried since 1.1 (in 1.1 to 1.3: *"only claims whose infringement depends upon the use of the Work"*; ACD-1.4 rewrites that limit, #282). A combination is also what Josh Berkus answered on this list with *"It's not the goal of the OSI to have licenses for every possible combination of conditions"* (#276, said of another proposal), and that breadth is a cost (#16). **In legal effect, much of the first and third limbs is statement rather than new permission**: §6.1 states what permissive licences already allow (§6.5 says so itself), and §9 asserts no right rather than granting one. What §6 adds in effect is §6.2–§6.3, on the Dedicator's own reservations. **The shape has been asked about before**: in 2012 Rick Moen asked what a public-domain declaration with a permissive fallback solves *"that is not already solved by MIT License or Fair License?"*, and in 2015 Mark Radcliffe answered another proposal of that shape *"I think that we have more than enough licenses with these characteristics."* Neither text licensed patents (the 2012 one was CC0, which excludes them expressly), so our answer to both is the patent limb, not the absence of attribution ([`review-readings.md`](ACD-1.0.review-readings.md) §1.184, [`gap-measurements.md`](ACD-1.0.gap-measurements.md) §1.146) |
| **It is reviewable**: §3 surrenders, §4 grants a licence *independently* (§4.4), so a reader never has to decide whether the surrender worked | **No court has characterised this construction**, in any jurisdiction (#3), and **no submission of this shape has been approved since 2020** (#87). A dedication taken alone is not approvable, and the escape is untested. In 2000 a law teacher on this list wrote that *"The continued vitality of the defense of abandonment is in serious doubt except for, perhaps, copyright disputes occurring under the pre-1976 Copyright Act"* (`ACD-1.0.jurisdictions.md` §5d), which reaches §3 in the United States. And because ACD sets no condition, a recipient has no condition met to point to as consideration if the licence is attacked as a revocable bare permission (#324); ACD relies on reliance (§2.5) instead, and reliance protects only those who relied |
| **It imposes nothing on a recipient**: §10.1 and §4.3 attach no condition, so no obligation can fire in any delivery mode — the failure that condition-bearing instruments meet in hosted deployment | **The same structure weakens the warranty disclaimer** (#41) and forecloses defensive patent termination (#46). Both costs fall on the adopter, and both are deliberate |
| **Anyone can adopt it**: zero project names, no placeholders in the clauses (one blank in §16.1's notice template), no editing of the licence text required — verifiable with the commands below | **One adopter: this repository** (#4). Reusability is a structural property; adoption is a social one, and only the first is shown |
| **It has a use case**: a work made to be learned from by AI needs, at once, an express permission for computational use (§6.1, §6.2), a patent licence that reaches the models and outputs made from it (§8.4), and a licence that does not depend on whether any right subsists in machine-generated material (§9.2, §9.3). OSI's own page on parameters asks for *"an explicit assertion"* (the AI and ML row below) | **The use case is not substantiated.** Josh Berkus, as a Committee member, 2017-10-24, listed the criteria he applied to a new licence, the fourth being *"Has a substantiated use case"*; Richard Fontana added *"Is sufficiently clear and understandable"* the same evening (`ACD-1.0.review-readings-6.md` §1.464). The one use shown is the author's own repository, and the form that invites other projects to say they use or want it (`.github/ISSUE_TEMPLATE/acd-use.yml`) has had no response (#4, B2). In the same week he asked another submitter *"can you explain what the first project you have in mind for this license is?"*, because *"this committee doesn't want to approve a license with no confirmed users."* What is missing is not an explanation of the use but evidence of it. Against that: the first project is this repository, and the Committee's rationale for MIT-0 says OSI *"has historically approved newly drafted licenses not yet in use"* (the Use row below) |

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

**The complete adverse record** is [`ACD-1.0.against.md`](ACD-1.0.against.md); the objections that land
come first in [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md). What the record already says in
ACD's favour, point by point with the speaker and the date, and the reasons that earlier versions gave
in their own words and ACD-1.4 does not, are on their own page:
[`REVIEWERS-RECORD.md`](REVIEWERS-RECORD.md). Nothing there binds anyone, and you can decide without it.

**What we cannot fix.** No lawyer has read this licence, and none has been
engaged ([`against.md`](ACD-1.0.against.md) #1). The step that resolved the closest precedent —
legal advisors concluding the Unlicense "would most likely be interpreted as a license and that
the license met the OSD" — has no counterpart here (#2). **And the precedent has not been
repeated**: searching the public review tracker's 252 records for this family returns one approval —
the Unlicense, 2020, on a legacy basis we cannot use — and one contemporary attempt, still
unresolved, whose author was told on this list that a waiver of this kind needs a lawyer (#87).
**Those are the three things we cannot fix, and we state them here rather than leave them to be found.**

**What we did instead, and what it is not.** We read the statutes, and the few decisions we could
obtain, that ACD-1.4 relies on in the United States, the United Kingdom, Germany, France and
Japan, with Canada for moral rights, the EU directives on text and data mining, databases and
technological measures, and the Berne Convention and TRIPS, kept each text in `rounds/`, and wrote
under each question in
[`QUESTIONS-FOR-COUNSEL.md`](QUESTIONS-FOR-COUNSEL.md) what the law already settles and what it
leaves open. Where a reading turned on our own words, the text was changed instead, before ACD-1.4 was fixed. This narrows the
questions a lawyer would be asked. It is not legal review, and it does not answer #1 or #2.
For every clause of ACD-1.4 we also wrote down at least the strongest other reading its words
allow (a modifier after a list, a pronoun without an antecedent, an exception present in one covenant
and missing from its twin, a sentence that asserts a legal effect rather than what the document does).
Readings that stood were closed in the text; readings that did not stand are recorded with the clause
that closes them; the few that only the law can settle went to the questions for counsel
([`ACD-1.4-UNIQUE-READING.md`](ACD-1.4-UNIQUE-READING.md)). We do not claim to have found every
reading: a second pass found new ones. That a reading does not stand is our judgment, not a lawyer's.

## What to open first

**Reading order.** If you have ten minutes: the table under *The new language* above (what is new, next to the nearest approved text), the objection map, then the licence. If you are deciding: add what was actually sent, and the errata. **The case against is the full record and the longest document in this directory** — it is where the objection map points, not a substitute for it. Nothing in it is summarised away anywhere else, and **nothing in it will be shortened**: this directory treats a shrinking adverse list as erasure rather than improvement (`REVISION-PROTOCOL.md` §2).

| | File | Note |
|---|---|---|
| **What is blocking approval** | [`ACD-OSI-BOTTLENECKS.md`](ACD-OSI-BOTTLENECKS.md) | **The register. Mostly Japanese; it opens with a full index in English.** Each item says why it is an approval problem, what is fact and what is inference, the smallest resolution, what would be lost, and who can move it — **four are marked highest severity, and none of them is repaired by editing the licence**: no legal review (B1) and one adopter (B2) advance only by submitting and by time; whether the gap justifies a new licence is OSI's call (B10); and the moderators' notice about AI-written posts is for OSI as an organisation to decide (B14). Its summary line is derived from the table by a CI check, so it cannot quietly understate what is left |
| **Which known objections land** | [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md) | **In English.** Every objection **we have found** in the `license-review` / `license-discuss` archives of the last two years **that bears on a public-domain-equivalent or AI-facing instrument**, plus the older statements that decide this submission — found by a subject census plus reading the threads that matched, which is **a floor, not a census of every objection ever raised** (#87). Whether each applies to ACD, cited by the clause numbers of ACD-1.4 (the readings were first made against 1.0, and the rows on clauses rewritten since were read again against 1.4 on 2026-11-24), and — for the ones that do not — the clause that answers it. **Objections that land are listed first** |
| The licence itself | [`ACD-1.4.txt`](ACD-1.4.txt) | 701 lines, 16 sections. Plain ASCII, no placeholders in the clauses (one in §16.1's notice template). The text posted to the list is [`ACD-1.0.txt`](ACD-1.0.txt) (597 lines); [`REDLINE-1.0-TO-1.4.txt`](REDLINE-1.0-TO-1.4.txt) shows the changes |
| **What was actually sent** | [`rounds/2026-08-26-license-discuss-sent.txt`](rounds/2026-08-26-license-discuss-sent.txt) | The `license-discuss` post of 2026-08-26, verbatim from the public archive. 5,778 words |
| The packet prepared for `license-review` | [`ACD-1.0.submission.md`](ACD-1.0.submission.md) | English, **not yet sent anywhere**. Gap statement, comparison, OSD conformance, disclosures, and what is deliberately absent |
| **Looking for a specific answer** | [`QUESTION-INDEX.md`](QUESTION-INDEX.md) | 449 worked entries, indexed by the question rather than the filename |
| **The case against** | [`ACD-1.0.against.md`](ACD-1.0.against.md) | **The complete record, and the largest document here — about twenty times the length of the licence.** All 337 adverse facts, written by us. Two have no answer |
| **Which facts have gone stale** | [`AS-OF.md`](AS-OF.md) | Every claim about the outside world, with the date it was last verified |
| **What we would ask a lawyer** | [`QUESTIONS-FOR-COUNSEL.md`](QUESTIONS-FOR-COUNSEL.md) | ACD has had no legal review. Ten questions on which a lawyer's reading would most change the text, ranked by consequence, each answerable on its own |
| **What we would ask someone who builds ML systems** | [`QUESTIONS-FOR-PRACTITIONERS.md`](QUESTIONS-FOR-PRACTITIONERS.md) | The review record asks for this reader by name. Five questions on whether the machine-learning clauses (§1.7, §6.2, §6.3, §6.4, §8.4, §2.6) match a real pipeline, each answerable on its own |
| **Known defects in the text** | [`ACD-1.0.errata.md`](ACD-1.0.errata.md); for defects that a successor introduced, [`ACD-1.1-SELF-AUDIT.md`](ACD-1.1-SELF-AUDIT.md) (Japanese) | A frozen text is not repaired either: a defect in a sentence that 1.0 also has is recorded in the errata, one that a successor introduced is recorded in the self-audit, and a later version repairs both. The first defect recorded in the frozen ACD-1.4 is self-audit §3zd (2026-11-23): §11.4's second sentence says the Dedication reaches nothing beyond the Covered Rights, the §8 patent claims and Moral Rights, save for the covenants in Section 5, but the authorisation and waiver as to technological measures that 1.4 added to §5.2 are not covenants. §11.1 (second sentence) and §15.1 keep that sentence from narrowing anything a recipient has. Low; the self-audit entry records how a later version closes it. Nine more, in sentences 1.0 also has, were recorded after it and stand in ACD-1.4 unrepaired, each with its reasons: errata E87 to E95 (§5.2(b), the preamble, §8.1, §8.1 and §8.4, §16.2, §1.2, §1.4, §4.2, and §8.1 with §2.6). Why the sentence is there at all, and the case against it: `ACD-1.0.review-responses-clauses.md` §10 / §11. 94 known imprecisions, all unrepaired in 1.0 while the freeze holds, with what the successor does (the Status column is authoritative) |
| Known weaknesses, longer form | [`READY-TO-SUBMIT.md`](READY-TO-SUBMIT.md) | **Mostly Japanese.** Stated by us, before you have to find them |

## Disclosures you should not have to dig for

- **No lawyer was involved.** The licence has had no legal review. McCoy Smith, chair of OSI's
  License Committee, said in a talk OSI's blog published on 2026-11-24 that using an AI is at the
  moment no substitute for using a lawyer to write a licence (our paraphrase of an automatic
  transcript, not checked byte for byte; `ACD-1.0.against.md` #333).
- **The goal was the owner's; the concrete legal design and the text are an AI's.** He decided
  to have a licence of his own and said it should aim at external approval; he gave the goal and
  the top-level direction, and **did not write a legal specification or supply a list of legal
  requirements**. An AI agent (Claude, an Anthropic model, run through Claude Code) generated the
  concrete legal design and the text and developed it further under a standing delegation. The
  model's maker trains models, and §6.4 and §8.4 favour those who do; we name it so that you can
  read those clauses with that in mind (`ACD-1.0.against.md` #319). **The name ACD-1.0, the generalised instrument and the
  submission material took shape during that delegated work, and he came to know their concrete
  state afterwards.** He read the full text of ACD-1.0 and understood it before posting it on 2026-08-26. Whether he has read ACD-1.4 in full — the version that would be submitted — is for him to state when he submits it; this page does not state it for him. He is the
  Dedicator and the steward and answers for it; **he did not write its clauses**
  (`submission.md` §E.1).
- **Who answers your questions.** The owner, in his own words; the AI that drafted the text does
  not post. Pamela Chestek, 2020-02-28: *"the people who wrote the license are ideally the ones
  explaining it to the license-review list because they know the ins and outs. We've had proxies
  participate in the past and it doesn't go well."* By that measure the answer to who wrote it is
  unusual here: he commissioned the text, publishes it and answers for it as its steward, but did
  not write the clauses, so he answers from the record rather than from having drafted it. Her word
  was *ideally*; it is not a requirement. What he answers from is the public record of
  every drafting decision, each with its reasons and the case against it (the change list, the
  trial drafts, the errata and `ACD-1.0.against.md`), and he decides what changes in answer to a
  question. We state this here so that you can weigh it before the first question, not after.
- **One adopter: this repository.** That is the only real-world use. The repository calls itself a public
  experiment in AI orchestration; the licence is not a text written for discussion but the terms
  the repository's contents are released under today (ACD-1.4, applied 2026-11-23), and it is
  written so that anyone can apply it unchanged.
- These are stated at length in `ACD-1.0.submission-reference.md` §5 and `ACD-1.0.submission.md` §E.1, not buried.

## Checking the claims yourself

Every structural claim in the submission is meant to be verifiable in one command. A few:

**These commands assume you have the repository.** One line gets it, and nothing here needs a
build or a network beyond that:

```sh
git clone --depth 1 https://github.com/yutapr0117-design/portfolio && cd portfolio
```

**If you only have the attachment from the mailing list, use this instead** — it needs no clone,
and it is the check that matters, because it compares *the bytes you were sent* against the
pinned file rather than against anything this repository asserts about itself. The attachment is
the part of `ACD-1.4.txt` below the line of 80 hyphens: the lines above it describe the file, and
the file itself says they are not part of the Dedication and that a copy may leave them out
(decision 4 of the five, `ACD-1.0.submission.md` §A, Canonical text). So it has its own digest,
derived from the pinned file:

```sh
shasum -a 256 <the attachment>
# expect ce76f3ab337c367741a6a1cea237657d371a3a193b43aa9fd2d34fdcfa8b962f
curl -s https://yutapr0117-design.github.io/portfolio/LICENSES/FROZEN.md \
  | grep -E '^[0-9a-f]{64}  LICENSES/ACD-1\.4\.txt$'
# the pinned digest of the whole file: 6792e804486e59082b84fce663d2bc24c22d72720c6d1bab8af43a90c9e3b615
curl -s https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.4.txt | shasum -a 256
# must equal the pinned digest above
curl -s https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.4.txt \
  | sed '1,/^-\{80\}$/d' | shasum -a 256
# must equal the digest of the attachment (as of 2026-11-24, both values computed from the pinned file)
```

```sh
# No project, author, domain or URL appears in the licence body      → expect 0
grep -icE "yokoi|portfolio|github|https?://" LICENSES/ACD-1.4.txt

# Placeholders: only §16.1's notice template, which the adopter fills in
# their own notice — the licence text itself needs no editing            → expect 1
grep -cE "<[^>]+>|\[year\]|\[name\]|YYYY" LICENSES/ACD-1.4.txt

# Section count                                                       → expect 16
grep -cE "^[0-9]+\. [A-Z]" LICENSES/ACD-1.4.txt

# Verify that the text you are reading is the text that is pinned      → 12× OK
grep -E "^[0-9a-f]{64}  " LICENSES/FROZEN.md | shasum -a 256 -c
```

The last one is the important one. `LICENSES/FROZEN.md` records the digests in the same format
`shasum` emits, so the check is a single pipe with no trust in anything this repository says
about itself: if the licence text had been altered since the discussion began, that line would
print `FAILED` instead of `OK`. It currently prints `OK` for all twelve files (re-run 2026-11-23, together with the three counts above: 0, 1 and 16).

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
| [`ACD-1.0.clause-reference.md`](ACD-1.0.clause-reference.md) / [`ACD-1.4.clause-reference.md`](ACD-1.4.clause-reference.md) | Japanese | All 82 clauses of 1.0, and all 80 of ACD-1.4, one line each, with what each is for. In English, for ACD-1.4: [`CHANGES-ACD-1.4.txt`](CHANGES-ACD-1.4.txt) (what changed from 1.3, clause by clause) and "The new language, next to the nearest approved text" above |
| [`ACD-1.0.jurisdictions.md`](ACD-1.0.jurisdictions.md) | Japanese | Where the questions differ by jurisdiction (JP, DE, FR, US, EU, UK). **Questions, not conclusions** — no legal opinion is offered |
| [`FAQ.md`](FAQ.md) | Mixed; each answer has an English block | Practical questions from the adopter's side (SPDX notation, scanners, explaining it to a legal team, academic use, consumer-law limits) |
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
| [`ACD-1.0.review-precedents.md`](ACD-1.0.review-precedents.md) | Japanese, quoting English verbatim | What this list has actually done to submissions of our shape, read from the archives. Two parts were split out by subject: [`ACD-1.0.review-doctrine.md`](ACD-1.0.review-doctrine.md) (doctrine argued on the lists, applied to particular ACD clauses) and [`ACD-1.0.review-outcomes.md`](ACD-1.0.review-outcomes.md) (what OSI did and said: votes, practice, handling after approval, holding back) — both Japanese, quoting the archive in English. |
| [`ACD-1.0.review-corpus.md`](ACD-1.0.review-corpus.md) | Japanese, quoting English verbatim | Measurements over the archives as a whole, as distinct from readings of single threads |
| [`ACD-1.0.review-rules.md`](ACD-1.0.review-rules.md) | Japanese, quoting English verbatim | The OSI's own published pages, read at source and applied criterion by criterion |
| [`ACD-1.0.board-decisions.md`](ACD-1.0.board-decisions.md) | Japanese, quoting English verbatim | The board's published minutes — where decisions are recorded, which the mailing list does not record |
| [`ACD-1.0.reviewer-positions.md`](ACD-1.0.reviewer-positions.md) / [`ACD-1.0.review-labels.md`](ACD-1.0.review-labels.md) | Japanese | Positions taken by named participants, and the labels this list uses for licences like this one |
| [`AUDIT-LEDGER.md`](AUDIT-LEDGER.md) | Japanese | How each class of claim in this dossier was verified, with the counts and the residue |
| [`BLIND-SPOTS.md`](BLIND-SPOTS.md) | Japanese | The dimensions we have used to look for our own defects, and the ones we have not |
| [`PEER-REVIEW-WATCH.md`](PEER-REVIEW-WATCH.md) | Japanese | Contemporary instruments under review, and what we would change if each is approved, rejected, revised or stalls |
| [`ACD-1.1-CHANGELIST.md`](ACD-1.1-CHANGELIST.md) / [`ACD-1.2-CHANGELIST.md`](ACD-1.2-CHANGELIST.md) / [`ACD-1.3-CHANGELIST.md`](ACD-1.3-CHANGELIST.md) / [`ACD-1.4-CHANGELIST.md`](ACD-1.4-CHANGELIST.md) / [`ACD-1.5-CHANGELIST.md`](ACD-1.5-CHANGELIST.md) | Japanese | What each successor changes, and why, one erratum at a time |
| [`ACD-1.1-SELF-AUDIT.md`](ACD-1.1-SELF-AUDIT.md) | Japanese | Defects the successor drafts introduce themselves |
| [`ACD-1.4-ADVERSARIAL-TRIAGE.md`](ACD-1.4-ADVERSARIAL-TRIAGE.md) | Japanese | An external adversarial audit of the 1.4 draft (172 points, supplied 2026-11-01), triaged one row at a time: what was already known, what is a deliberate trade, what needs counsel, and what was new and repaired in the draft. **An AI-written review, not a legal review** |
| [`ACD-1.0.dig-2026-09.md`](ACD-1.0.dig-2026-09.md) | Japanese | The record of one archive excavation, kept because the method is reusable |

## What is not being asked for

Approval would mean the licence conforms to the Open Source Definition. It would not mean it is
recommended, popular or preferred. This submission makes no claim to those, and the honest
position is the narrow one.
