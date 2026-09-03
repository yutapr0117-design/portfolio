---
file: LICENSES/REVIEWERS.md
audience: OSI license-discuss / license-review participants, licence reviewers, anyone arriving from the mailing list
last-updated: 2026-08-27
canonical-ref: LICENSES/ACD-1.0.txt (authoritative text) / LICENSES/FROZEN.md (freeze + venue, single source) / LICENSES/ACD-1.0.submission.md (the message as sent)
---

# Reviewing ACD-1.0 — start here

This page is in English because the discussion is. Most of the supporting analysis in this
directory is written in Japanese; this page tells you what each document contains so you can
decide what is worth translating, and gives you the commands to check the claims yourself.

## Status

**Posted to `license-discuss` and received. No responses yet.** That list is for general
discussion — it is **not** the approval venue. Nothing has been submitted to `license-review`,
and nothing has been submitted to SPDX.

**How it came to be on this list.** **No submission to license-review has been made.** When the
owner moved to seek approval, the guidance from OSI was that a licence of this kind goes to
license-discuss first, and that is what was done — the discussion post is the only thing that
has been submitted anywhere. So discussion did come first, but the ordering reflects OSI's
guidance rather than foresight on our part, and this page previously described it as a
deliberate choice of ours. What is our own decision is the SPDX timing: SPDX asks for substantial
real-world use, this work has one adopter, and we are not submitting something that does not
meet the stated bar.

The text is **frozen** while this is open. `LICENSES/FROZEN.md` exists to say so, and
**Check 453 in CI pins the SHA-256 of three files** (`ACD-1.0.txt`, `ACD-1.0.spdx.xml`,
`ACD-1.0.machine.json`) so that an accidental edit fails the build rather than silently changing
the text you are reading. If you find a defect in the text, it will be **reported, not quietly
patched** — changing the wording underneath a live discussion would make your review of it
meaningless.

## The three things you probably want first

| | File | Note |
|---|---|---|
| The licence itself | [`ACD-1.0.txt`](ACD-1.0.txt) | 597 lines, 16 sections. Plain ASCII, no placeholders |
| The message as sent | [`ACD-1.0.submission.md`](ACD-1.0.submission.md) | English. Gap statement, comparison, OSD conformance, disclosures, and what is deliberately absent |
| **Looking for a specific answer** | [`QUESTION-INDEX.md`](QUESTION-INDEX.md) | 118 worked entries, indexed by the question rather than the filename |
| **The case against** | [`ACD-1.0.against.md`](ACD-1.0.against.md) | **Read this first.** All 14 adverse facts, written by us. Two have no answer; one of those is on its own a sufficient reason to decline |
| **Known defects in the text** | [`ACD-1.0.errata.md`](ACD-1.0.errata.md) | Five imprecisions, all unrepaired while the freeze holds, with what 1.1 would do |
| Known weaknesses, longer form | [`READY-TO-SUBMIT.md`](READY-TO-SUBMIT.md) | Stated by us, before you have to find them |

## Disclosures you should not have to dig for

- **No lawyer was involved.** The licence has had no legal review.
- **The drafting was done by an AI**, autonomously, under a standing delegation. The human
  owner did not ask for a licence to be written, did not direct its contents, and learned of its
  existence afterwards. He read the full text before sending it.
- **One adopter: this repository.** That is the only real-world use.
- These are stated at length in `ACD-1.0.submission.md` §5 and §E.1, not buried.

## Checking the claims yourself

Every structural claim in the submission is meant to be verifiable in one command. A few:

```sh
# No project, author, domain or URL appears in the licence body      → expect 0
grep -icE "yokoi|portfolio|github|https?://" LICENSES/ACD-1.0.txt

# No placeholder or replaceable text (so adoption needs no editing)  → expect 0
grep -cE "<[a-z]+>|\[year\]|\[name\]|YYYY" LICENSES/ACD-1.0.txt

# Section count                                                       → expect 16
grep -cE "^[0-9]+\. [A-Z]" LICENSES/ACD-1.0.txt

# Verify that the text you are reading is the text that is pinned      → 3× OK
grep -E "^[0-9a-f]{64}  " LICENSES/FROZEN.md | shasum -a 256 -c
```

The last one is the important one. `LICENSES/FROZEN.md` records the digests in the same format
`shasum` emits, so the check is a single pipe with no trust in anything this repository says
about itself: if the licence text had been altered since the discussion began, that line would
print `FAILED` instead of `OK`. It currently prints `OK` for all three files.

The repository's own CI enforces the rest: that the licence is declared identically across every
published surface, that the counts these documents quote match reality, and that the frozen files
are unchanged. Those are Checks 444, 460 and 453 respectively; `npm run verify` runs them.

## Map of the Japanese documents

| File | What is in it |
|---|---|
| [`ACD-1.0.comparison.md`](ACD-1.0.comparison.md) | Why the nearest approved licences do not fit, by family (CC0, Unlicense, 0BSD/MIT-0, Apache-2.0, MPL) |
| [`ACD-1.0.clause-reference.md`](ACD-1.0.clause-reference.md) | All 82 clauses, one line each, with what each is for |
| [`ACD-1.0.jurisdictions.md`](ACD-1.0.jurisdictions.md) | Where the questions differ by jurisdiction (JP, DE, FR, US, EU, UK). **Questions, not conclusions** — no legal opinion is offered |
| [`ACD-1.0.faq.md`](ACD-1.0.faq.md) | Practical questions from the adopter's side (SPDX notation, scanners, explaining it to a legal team, academic use, consumer-law limits) |
| [`ACD-1.0.review-responses.md`](ACD-1.0.review-responses.md) | Anticipated objections: the four weaknesses stated first, then OSD clause by clause |
| [`ACD-1.0.review-responses-clauses.md`](ACD-1.0.review-responses-clauses.md) | Anticipated objections at the clause level |
| [`ACD-1.0.review-responses-meta.md`](ACD-1.0.review-responses-meta.md) | Objections about the instrument's provenance, name, stewardship, versioning and machine-readability |
| [`ACD-1.0.discussion-log.md`](ACD-1.0.discussion-log.md) | Reserved for **actual** feedback once it arrives. Deliberately not filled with guesses |

If something you need is only in Japanese and matters to your review, say so on the list and it
will be translated. Nothing here is withheld — the language is an artefact of who wrote it, not
a choice about who should read it.

## What is not being asked for

Approval would mean the licence conforms to the Open Source Definition. It would not mean it is
recommended, popular or preferred. This submission makes no claim to those, and the honest
position is the narrow one.
