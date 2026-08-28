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
| 3 | **A public-domain dedication, taken alone, is not approvable.** The escape is §3's fallback licence, which has never been tested by any court in any jurisdiction | **Unresolved.** The structure is argued in submission §1b; whether it functions is a legal question nobody has answered |
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

**What this exercise changed.** One dossier statement was wrong and has been corrected (#15).
One criticism of the text is accepted as fair and left unrepaired because the text is frozen
(#18). Two are costs that were understated and are now stated (#16, #17). None of the five was
dismissed.

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

- If the list's view is that §3's fallback does not make this a licence, then it is not a
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
