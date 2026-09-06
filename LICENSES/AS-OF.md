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
| Responses received | **2026-09-05** | None | `ACD-1.0.discussion-log.md` — an empty log means nothing has arrived, and silence is recorded as an entry rather than as absence |
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
| **The Unlicense approval record (2020)** | **2026-09-06 · read at source** | License Review Committee recommendation, June 2020: the document is "poorly drafted"; it is "an attempt to dedicate a work to the public domain (**which, taken alone, would not be approved as an open source license**) but it also has wording commonly used for license grants"; the lawyers who opined, **"both US and non-US"**, agreed it "would most likely be interpreted as a license and that the license met the OSD"; placed in **Special Purpose** over the submitter's request for the popular category | license-review archive, 2020-June. **This is the primary source for #2, #3 and #7** — previously all three rested on secondary characterisation |
| **BOS Public License v1.3** | **2026-09-06 · full text read in the archive** | MIT plus two file-preservation conditions (`UPSTREAM.txt`, `CREDITS.txt`), applying **strictly to public source-code distribution, not to binaries**. Submitted 2026-09-05 by Luis Harz. Its notice reads `Copyright (c) 2026 [Your Name or Organization]` — **it carries a placeholder**, which is the property `submission.md` §4b claims ACD-1.0 does not need | license-review archive, 2026-September |
| **Clause citations to other licences** | **2026-09-06 · characterised, not quoted; sources not fetched here** | The dossier cites **15** clauses of other instruments (Apache-2.0 §3 and §6, CC0 §4(a), GPLv3 §3, and others) and **quotes none of them verbatim** — every quotation attributed to an outside source is from a mailing-list discussion, not from a licence text. The characterisations match the widely-known content of those clauses, **but were not checked against the source texts in this environment** | Open each licence at its canonical source and read the cited section. **A section number plus a topic is cheap to check and expensive to get wrong** — reviewers on this list know Apache-2.0 and CC0 better than they know anything we wrote |
| **OSAID (Open Source AI Definition) v1.0** | **2026-09-06 · read at source** | All three required components are conditioned on OSI approval, verbatim: *"Data Information shall be made available under OSI-approved terms"*, *"Code shall be made available under OSI-approved licenses"*, *"Parameters shall be made available under OSI-approved terms"*. **So an AI system cannot be OSAID-conformant while its data information, code or parameters are released under ACD-1.0 — until ACD-1.0 is approved.** The wording asymmetry ("terms" for two components, "licenses" for one) is noted and **not resolved here** | https://opensource.org/ai/open-source-ai-definition — re-read if a v1.1 appears |

## What is deliberately not here

**Nothing about the text itself.** The licence is frozen and CI pins its digest, so statements
about what it says do not need an as-of date — they need the digest check above. Mixing the two
would suggest the text might have moved when it has not.

**No predictions.** How long review takes, whether approval is likely, what the incumbents will
do next. `submission.md` §4a gives the two comparable submissions and notes they point opposite
ways; that is as far as the evidence goes.
