---
file: LICENSES/AS-OF.md
audience: OSI license-discuss / license-review participants, licence reviewers
last-updated: 2026-09-05
canonical-ref: LICENSES/FROZEN.md (freeze + venue, single source) / LICENSES/ACD-1.0.against.md / LICENSES/PEER-REVIEW-WATCH.md
---

# Facts that can change, and when they were last checked

Most of this directory describes a text that is frozen and does not move. **A small number of
statements describe the world outside it, and those go stale.** They are collected here with the
date each was last verified, so that a reader in six months knows which claims to re-check rather
than having to guess.

**If a date below is old and the claim matters to your reading, treat the claim as unverified.**
The dossier is written to be checked, not believed, and that applies to its own currency.

## Status of this submission

| Fact | As of | Value | How to re-check |
|---|---|---|---|
| Where it has been submitted | **2026-09-05** | `license-discuss` only. Nothing to `license-review`. Nothing to SPDX | `FROZEN.md` VENUE-DATA is the single source; CI enforces every other file against it (Check 458) |
| Responses received | **2026-09-06** | None — **verified at the primary source** | The public `license-discuss` archive for 2026-08 and 2026-09 was read directly: our post appears once (2026-08-26 17:17) and nothing follows it under that subject. Until this date the claim rested on the owner's report; it now rests on the archive. **The same archive shows the list answering a structurally comparable post six times within about ten hours** (`against.md` #83), so the silence is not a quiet list |
| Messages we have sent | **2026-09-06** | Two, by the owner's report; **one confirmed in the archive** | The 2026-08-26 post is in the public archive and kept verbatim at `rounds/2026-08-26-license-discuss-sent.txt` (5,778 words). The owner reports sending a **second, topic-focused message on 2026-09-06**; it has not yet appeared in the archive, so its text is not in `rounds/` and nothing here characterises its contents. **It is recorded because the owner stated it, not because we have seen it** |
| Public review tracker (`LicenseAtlas`) | **2026-09-06** | Exists, machine-readable, **does not list ACD-1.0** | `https://morningd.github.io/license.atlas/data/tracker.json` — built from the `license-review` and `license-discuss` archives, announced on the list 2026-08-28, endorsed there by Richard Fontana. Its `meta` reports **252 submissions**: approved 89, rejected 42, withdrawn 14, pending 12, superseded 3, legacy 33, discussion 59. **We have not read its source and have not verified how it classifies**, so these are its counts, not ours. Absence of ACD-1.0 is `against.md` #86 |
| Whether silence on the list carries a signal | **2026-09-06** | **Not reliably, in either direction** | Against reading it as neutral: a structurally comparable `license-discuss` post drew six replies in about ten hours (#83). Against reading it as negative: Max Mehl, whose submission the board **approved**, wrote *"It would have been great to get a feedback as a reply to the review request"* — **approval with no reply in the thread**. Both are from the 2026-08 archives |
| `license-discuss` is not the approval venue | **2026-09-06** | Confirmed, quoted at source | McCoy Smith on the list, 2026-08-04, three weeks before our post: *"this list 'license-discuss' is for discussion of licenses, not for getting licenses approved. That list is 'license-review.'"* Until now this directory asserted the distinction; it is now cited. **Individual capacity, not an OSI ruling** — but it is the maintainer-side statement of how the two lists are used |
| Subject-line convention for a submission | **2026-09-06** | `For Approval: <name>` on `license-review`; `For Discussion: <name>` on `license-discuss` | Measured across the archives held: 103 messages under `For Approval: OpenMDW License Agreement`, plus `Request for Legacy Approval of PHP License 3.01`, `CeCILL license V2.1 for Approval`, `For Discussion: GNU Affero General Public License`. **`submission.md` §B.0 already specifies `For Approval: Autonomous Commons Dedication 1.0 (ACD-1.0)`** — checked and correct, and now correct *for a recorded reason* rather than by chance |
| Text frozen | **2026-09-05** | Yes; three files pinned | `grep -E "^[0-9a-f]{64}  " LICENSES/FROZEN.md \| shasum -a 256 -c` → 3× OK |

## Facts about the licence's standing

| Fact | As of | Value | How to re-check |
|---|---|---|---|
| SPDX registration | **2026-09-05** | Not registered; `LicenseRef-ACD-1.0` is the conforming form | SPDX License List |
| OSI approval | **2026-09-05** | Not approved | OSI approved-licence list |
| Adopters | **2026-09-05** | One: this repository | Any public search; we do not track adoption and would not know of others |
| No AI-specific licence has been OSI-approved | **2026-09-04** | True at that date | OSI approved-licence list — **this is the claim most likely to change**, and if it does, `against.md` #33 improves rather than breaks |

## Facts about other instruments

These are observations of other people's submissions and are the fastest-moving statements here.
`PEER-REVIEW-WATCH.md` holds the detail and the plan for each outcome.

| Fact | As of | Value |
|---|---|---|
| OpenMDW-1.1 | **2026-09-04** | First submission, still open; the August 2026 thread ran to roughly 90 messages among about a dozen participants |
| ModelGo MG0-2.0 / MG-BY-2.0 | **2026-09-04** | Third resubmission (Dec 2025); the author's follow-ups of Jan, May and Jul 2026 had gone unanswered |
| Incumbent stewards' AI response | **2026-09-04** | FSF working on criteria for free ML applications, no GPLv4 announced; ASF publishing generative-tooling guidance, no licence amendment announced; CC0 unchanged since 2012 |
| **The CC0 review record (2012)** | **2026-09-06 · read at source, including the withdrawal** | The objections, Bruce Perens' objection to the abandonment-plus-fallback structure, **and Creative Commons' own withdrawal message (2012-02-24)** are all quoted from license-review 2012-02. The withdrawal names exactly two grounds — estoppel and "on notice" — and states that the patent carve-out came from the **scientific data community** | license-review archive, 2012-February |
| **The Unlicense approval record (2020)** | **2026-09-06 · read at source** | License Review Committee recommendation, June 2020: the document is "poorly drafted"; it is "an attempt to dedicate a work to the public domain (**which, taken alone, would not be approved as an open source license**) but it also has wording commonly used for license grants"; the lawyers who opined, **"both US and non-US"**, agreed it "would most likely be interpreted as a license and that the license met the OSD"; placed in **Special Purpose** over the submitter's request for the popular category | license-review archive, 2020-June. **This is the primary source for #2, #3 and #7** — previously all three rested on secondary characterisation |
| **BOS Public License v1.3** | **2026-09-06 · full text read in the archive** | MIT plus two file-preservation conditions (`UPSTREAM.txt`, `CREDITS.txt`), applying **strictly to public source-code distribution, not to binaries**. Submitted 2026-09-05 by Luis Harz. Its notice reads `Copyright (c) 2026 [Your Name or Organization]` — **it carries a placeholder**, which is the property `submission.md` §4b claims ACD-1.0 does not need | license-review archive, 2026-September |
| **Clause citations to other licences** | **2026-09-06 · the substantive ones verified at source** | The dossier characterises four clauses of other instruments, and all four were read at their canonical source and match: **Apache-2.0 §3** is "Grant of Patent License" and does terminate the patent licence on litigation alleging the Work infringes; **Apache-2.0 §6** is "Trademarks" and grants no permission to use the licensor's marks; **CC0 §4(a)** reads "No trademark or patent rights held by Affirmer are waived, abandoned, surrendered, licensed or otherwise affected by this document"; **GPLv3 §3** is "Protecting Users' Legal Rights From Anti-Circumvention Law". The dossier **quotes none of them verbatim** — every quotation attributed to an outside source is from a mailing-list discussion. Remaining mentions of other licences are generic or are references to ACD-1.0's own sections | Re-read at the canonical source if a new version of any of the four appears |
| **The Open Source Definition (the ten criteria)** | **2026-09-06 · read at source** | Criteria 4, 6, 7, 9 and 10 were compared word for word against how this dossier renders them. **No misquotation and no mischaracterisation.** One phrasing was tightened: #27 cited OSD 4 as context for §16.4's name provision, which invites the reading that §16.4 needs OSD 4's shelter — it does not, because §16.4 is not a term of the Work (§10.5, §16.6) | https://opensource.org/osd — re-read if the OSD text is ever revised |
| **OSAID (Open Source AI Definition) v1.0** | **2026-09-06 · read at source** | All three required components are conditioned on OSI approval, verbatim: *"Data Information shall be made available under OSI-approved terms"*, *"Code shall be made available under OSI-approved licenses"*, *"Parameters shall be made available under OSI-approved terms"*. **So an AI system cannot be OSAID-conformant while its data information, code or parameters are released under ACD-1.0 — until ACD-1.0 is approved.** The wording asymmetry ("terms" for two components, "licenses" for one) is noted and **not resolved here** | https://opensource.org/ai/open-source-ai-definition — re-read if a v1.1 appears |

## What is deliberately not here

**Nothing about the text itself.** The licence is frozen and CI pins its digest, so statements
about what it says do not need an as-of date — they need the digest check above. Mixing the two
would suggest the text might have moved when it has not.

**No predictions.** How long review takes, whether approval is likely, what the incumbents will
do next. `submission.md` §4a gives the two comparable submissions and notes they point opposite
ways; that is as far as the evidence goes.
