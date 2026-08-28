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
