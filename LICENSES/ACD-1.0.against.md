---
file: LICENSES/ACD-1.0.against.md
audience: OSI license-discuss / license-review participants, licence reviewers
last-updated: 2026-08-28
canonical-ref: LICENSES/ACD-1.0.txt (authoritative text) / LICENSES/ACD-1.0.submission.md (the message as sent) / LICENSES/READY-TO-SUBMIT.md
---

# The case against approving ACD-1.0

Read this before the arguments in favour. It is the complete set of facts that argue against
approval, written by the submitting side, and it is not balanced: nothing here is paired with a
reassurance in the same breath. Where an answer exists it is given afterwards and marked as such.
Where none exists, the row says so.

**Standard used to build this list.** A fact belongs here if a reviewer could reasonably raise
it, not if we think we can answer it. Two of the entries below have no answer, and one of them
is, on its own, sufficient reason to decline. That is the point of writing the list this way:
if every adverse fact came with a tidy rebuttal, the document would be advocacy wearing the
costume of candour.

## The list

| # | Adverse fact | Status |
|---|---|---|
| 1 | **No lawyer has read the licence.** It has had no legal review of any kind | **Unanswerable by us.** Only counsel can cure it, and none has been engaged |
| 2 | **The decisive step in the closest precedent is unavailable here.** The Unlicense was approved after legal advisors concluded it "would most likely be interpreted as a license and that the license met the OSD." That reading is what resolved the dedication-versus-licence question there. Nothing equivalent exists for ACD-1.0 | **Unanswerable by us.** Same root as #1 |
| 3 | **A public-domain dedication, taken alone, is not approvable.** The escape is §4, a licence granted independently of §3 (§4.4). That construction has never been tested by any court in any jurisdiction, and no court has characterised the instrument as a whole | **Unresolved.** The structure is argued in submission §1b; whether it functions is a legal question nobody has answered |
| 4 | **One adopter: this repository.** No independent party has chosen it | **Answered narrowly.** Reusability is shown structurally (submission §4b); adoption is not claimed and does not follow |
| 5 | **It was drafted by an AI, autonomously.** The human owner did not commission it, did not direct its contents, and learned of its existence afterwards. He read the full text before sending | **Disclosed, not defended.** Provenance does not make a text good or bad, but reviewers are entitled to weigh it and this submission does not ask them not to |
| 6 | **It is long.** 16 sections, 82 clauses, 597 lines, for an instrument whose stated purpose is to reserve nothing | **Accepted cost.** The trade is argued in review-responses-meta Q17. The opposite criticism sank nothing — the Unlicense was approved while broadly agreed to be poorly drafted — so length is not obviously the safer error |
| 7 | **Realistic best case is a narrow placement.** The Unlicense was put in a special-purpose category over the submitter's objection, expressly because of its dedication nature | **Accepted.** Submission §4a disclaims any request for a broader designation |
| 8 | **Jurisdictional effectiveness is unverified everywhere.** §3 fallback, §8.4 patent reach, §12 moral-rights construction, §13/§14 against consumer-protection law — none tested | **Unresolved by design.** `ACD-1.0.jurisdictions.md` records these as questions and refuses to state conclusions |
| 9 | **§5.2 contains covenants by the Dedicator.** A reviewer may read a covenant as an obligation that makes the instrument less than fully permissive | **Answered.** §5.2 binds only the Dedicator; §10.1 states that no condition is imposed on You. Argued in review-responses-clauses Q26 |
| 10 | **The steward is one individual.** No organisation maintains it, and there is no succession plan for the licence itself | **Answered partially.** review-responses-meta Q12. The absence of an or-later mechanism (Q33) is a deliberate consequence: a lone steward should not hold a blank cheque over future versions |
| 11 | **No versioning mechanism.** "ACD-1.0 or later" cannot be written | **Accepted.** Same as Apache-2.0, MIT and BSD; explained in Q33 |
| 12 | **Not registered with SPDX.** Scanners will report `LicenseRef-` or `NOASSERTION` | **Accepted.** A registration-state problem, not a text problem; the order (discussion → review → SPDX) is deliberate |
| 13 | **Nothing has actually started yet.** The message is on `license-discuss`, which is not the approval venue. No submission to `license-review` exists | **Stated, not spun.** This document exists before the process does |
| 14 | **The licence has never been tested by a dispute.** No court, no arbitration, no adversarial reading | **Unresolved.** True of most licences at submission time, which is a mitigation and not an answer |

## Clause-level adversarial re-reading (added 2026-08-28)

Five clauses were put to a hostile reading at the suggestion of a third party. The results are
placed here rather than in the favourable material, because three of the five are costs and one
is a fair criticism of the text itself.

| # | Adverse reading | Status |
|---|---|---|
| 15 | **§2.6 makes submission itself the act of dedicating, by default.** A Contribution is under this Dedication and its author becomes a Dedicator "unless they state otherwise at the time of submission." A licence cannot by its own words determine the legal effect of a third party's act: whether a contributor is bound depends on notice and assent, not on this clause saying so. It is also an **opt-out by silence**, which sits awkwardly beside §6.2, where the instrument refuses to read silence as a reservation | **Real tension, partly answered.** §2.7 keeps the reach honest — nothing is dedicated that the person did not hold, and §2.6 cannot manufacture assent. In practice it operates as a stated default that a project must put contributors on notice of, not as a self-executing transfer. The dossier previously described contributions in a way that omitted this default; that description has been corrected |
| 16 | **§8.4's patent grant is very broad.** It reaches "every patent claim owned or controlled by the Dedicator, now or in future" that would be infringed by Computational Use **or by any model, parameter set, weight, embedding, or output resulting from that use.** An output can be far from the Work, so a claim in an unrelated field could be swept in. It is materially broader than Apache-2.0, which limits the grant to claims necessarily infringed by the contribution | **Accepted cost, with a consequence worth naming.** The breadth runs against the Dedicator, not against You, so it is not an OSD problem. But counsel for a patent-holding organisation would likely refuse it, which means **the instrument is expensive for exactly the adopters whose adoption would carry weight**. That is part of why adoption is one repository |
| 17 | **§5.2(b) is a wide covenant against collateral obligations.** The Dedicator promises not to impose, "by contract, terms of service, access condition, click-through, registration requirement, or any other collateral means," an obligation in respect of the Work. The boundary between "in respect of the Work" and "in respect of a service that uses it" is not drawn | **Accepted cost.** Again it binds only the Dedicator. But read together with #16, an organisation adopting ACD-1.0 gives up more than it may realise: arguably dual licensing, paid support terms touching the Work, and gated distribution. The instrument is demanding of its adopter by design, and adopters should be told so plainly rather than discovering it |
| 18 | **§16.1 instructs adopters to write an identifier that no registry has assigned.** The recommended notice contains `SPDX-License-Identifier: ACD-1.0`, but SPDX has not registered ACD-1.0. Today the conforming form for an unregistered licence is `LicenseRef-`, so a notice written exactly as §16.1 directs is not SPDX-conforming, and scanners will not match it | **Fair criticism of the text. Not fixed.** The text is frozen for the duration of the discussion (Check 453 pins its digest), so this is **reported and left in place** rather than patched — changing it underneath a live review would make the review of it meaningless. It is a candidate correction for 1.1. Note the practical effect is limited: the identifier a licence assigns itself is conventionally the string SPDX later registers, and `ACD-1.0.faq.md` already tells adopters what to write while unregistered |
| 19 | **§15.1 tells the reader how to construe the instrument**, and §5.2(c) has the Dedicator covenant not to argue for a narrower reading. A party cannot instruct a court | **Answered, with one addition.** The general point is argued at review-responses-clauses Q22: a construction rule does not bind a court but is evidence of intent, which is all it claims to be. The addition the hostile reading surfaces is the **interaction with #16** — where §8.4's scope is ambiguous, §15.1 resolves the ambiguity *against* the Dedicator, compounding the breadth rather than limiting it |

| 20 | **§16.3 invites anyone to apply the notice to any work** "without permission from, notice to, or any relationship with its authors." §1.3 and §2.7 keep the *effect* honest — nothing is given that the applier does not hold — but the harm a reviewer will point at is not to the true owner. It is to the **downstream recipient**, who sees a machine-readable notice this very instrument invited anyone to emit, and whose reliance §13.2 then disclaims. An instrument whose stated purpose includes reliable machine-readable signalling weakens that signal in its own §16 | **Fair criticism; wording broader than needed.** The clause is doing necessary work — it is the textual basis for the reusability claim in submission §4b, so it cannot simply be narrowed without weakening that. A tighter form ("by anyone, to any work in which they hold rights") would keep the reusability point and drop the invitation. **Reported, not fixed:** the text is frozen. 1.1 candidate |
| 21 | **§2.9 declares its own insolvency-law classification** ("and so is not executory"), and states that no proceeding "affects a permission granted here." A document cannot determine how a forum's insolvency law classifies it; the Countryman-style tests belong to the forum. The mechanism is circular under hostile reading: §2.9 binds an officer by deeming them a §2.8 transferee, but whether that deeming is effective is the same question insolvency law decides | **Overstated in form; sound in substance.** The clause does give the facts before the conclusion — no continuing obligation on either side — and those facts are what any executory-contract test actually examines. Stating them is the strongest thing a text can do. Asserting the outcome is not, and this text asserts it |
| 22 | **§6.4 says outputs are not "encumbered by ... any Covered Right of the Dedicator" in absolute form.** Where an output substantially reproduces the Work, copyright in the Work plainly subsists in that reproduction, so the sentence appears to conflate "no right exists" with "rights exist and are unconditionally given away" | **Answered, with a wording caveat.** §6.5 says §6 "states expressly what Sections 3 to 5 would in any event" do — §6 is declaratory, so "encumbered" means "burdened by an enforceable claim," and there is none, because §4.1 grants unconditionally. The operative result is right. The phrasing is loose enough that a reviewer can press it, and "no enforceable claim arises" would have been the precise form. 1.1 candidate |
| 23 | **§15.7 states an intention about conflict of laws without resolving it.** "It is intended to operate under the law of each jurisdiction in which the Work is used, according to that law" reads as depeçage by declaration, which parties cannot dictate — a forum applies its own conflict rules | **Answered in part (review-responses-clauses, §15.7 entry, addresses the choice-of-law silence). One addition from this reading:** the absence of a governing law interacts with #3. Whether §3 is effective, and how the instrument is characterised, are both forum-dependent — so the questions §4.4 relieves the *recipient* of are not thereby removed from the *analysis*, only from the recipient's burden |
| 24 | **🔴 The submitting side misdescribed its own text.** Until 2026-08-28 this dossier and the submission packet said "§3's fallback licence." §3 is the surrender and waiver; the licence is §4, and §4.4 states it "is granted independently of Section 3 and does not depend on Section 3 being ineffective." The error made our own case weaker and wrong — a fallback invites "who decides, under which law, and when," while an independent grant does not | **Corrected, and recorded here rather than quietly.** `ACD-1.0.review-responses.md` had it right all along (it quotes §4.4); the newer documents contradicted it. A reviewer who caught this would have been entitled to discount everything else we assert about the text |

**What this exercise changed.** Two dossier statements were wrong and have been corrected
(#15, #24 — the second of them a misdescription of which section grants the licence, which had
been repeated across the submission packet). Two criticisms of the text are accepted as fair and
left unrepaired because the text is frozen (#18, #20), with #22 a third if the looser reading is
taken. Three are costs that were understated and are now stated (#16, #17, #21). **Nothing
raised was dismissed**, and the two rounds together moved the count of adverse facts from 14 to
24 — which is the honest direction for a list like this to move as it is examined.

## What survives

After the list above, the claim this submission actually makes is narrow, and it is the only one
it makes:

> The text is internally coherent, contains no project-specific or replaceable content, grants
> permissions in licence terms in every jurisdiction (dedication where dedication works, licence
> where it does not), and reserves nothing. Whether that is enough to meet the Open Source
> Definition is the question being asked — not a conclusion being asserted.

Everything mechanically checkable about the text has been checked and is recorded with the
commands to re-check it (submission §4c). Everything legal is unchecked, and no amount of care
in the first category substitutes for the second.

## What would cause withdrawal

Stated in advance so that it is not a reaction to how the discussion goes:

- If the list's view is that §4's independent grant does not make this a licence, then it is not a
  candidate in its present form, and the answer will be to say so rather than to redraft under
  pressure.
- If a defect is found in the text, it will be **reported and left in place** while the
  discussion is open. The text is frozen and CI pins its SHA-256 (Check 453); changing wording
  underneath a live review would make that review meaningless.
- `ACD-1.0.submission.md` §E.2 records the same conditions in the message as sent.

## Why this document exists

Because a submission that leads with its strengths invites the reviewer to find the weaknesses,
and the reviewer will find them. Putting them first is not humility; it is the only way the
favourable claims can be read as anything other than selection.
