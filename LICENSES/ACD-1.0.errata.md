---
file: LICENSES/ACD-1.0.errata.md
audience: OSI license-discuss / license-review participants, licence reviewers, a future 1.1 drafter
last-updated: 2026-08-30
canonical-ref: LICENSES/ACD-1.0.txt (frozen text) / LICENSES/FROZEN.md (freeze + digests) / LICENSES/ACD-1.0.against.md (the full adverse case)
---

# Known defects in ACD-1.0, and why none of them is fixed

Six items are recorded: five imprecisions and one open drafting question. **All five are unrepaired, deliberately.** This
page exists so that the list is public before anyone else compiles it, and so that "the text is
frozen" reads as a discipline rather than as a way of not answering.

## Why nothing is fixed

The text is frozen for the duration of the `license-discuss` thread, and CI pins the SHA-256 of
`ACD-1.0.txt`, `ACD-1.0.spdx.xml` and `ACD-1.0.machine.json` (Check 453) so that an accidental
edit fails the build. Editing wording underneath a live discussion would mean reviewers were
reading one text and commenting on another — their review would be of something that no longer
exists. A defect found now is therefore **reported and left in place**.

Verify the freeze rather than taking it on trust:

```sh
grep -E "^[0-9a-f]{64}  " LICENSES/FROZEN.md | shasum -a 256 -c   # expect 3× OK
```

## The list

| # | Clause | What is imprecise | What 1.1 would do | Severity |
|---|---|---|---|---|
| E1 | **§16.1** | The recommended notice instructs adopters to write `SPDX-License-Identifier: ACD-1.0`. SPDX has not assigned that identifier; the conforming form for an unregistered licence is `LicenseRef-`. A notice written exactly as directed is not SPDX-conforming | Either use the `LicenseRef-` form until registration, or say in the clause that the bare identifier presumes registration | **Highest.** It is the one place where the text instructs a reader to do something incorrect |
| E2 | **§16.3** | "may be applied by anyone, to any work, without permission from ... its authors" is broader than the point it exists to make. §2.7 keeps the effect honest, but the sentence invites applying the notice to works one does not own, and the party harmed is the **downstream recipient** who relies on the signal | Add "in which they hold rights", which preserves the reusability point (submission §4b depends on this clause) and drops the invitation | High |
| E3 | **§16.1 notice wording** (and the same sentence carried into `ACD-1.0.machine.json`'s `notice` field, so the fix touches two frozen files) | The notice says "no conditions are imposed" without §10.1's qualifier "in respect of the Work". §16.4 does restrict redistributing the licence *text* under its name, so the shorthand reads as contradicted three lines later | Carry the qualifier into the notice | Medium — the text is consistent; only the summary is loose |
| E4 | **§6.4** | "No model ... is encumbered by this Dedication or by any Covered Right of the Dedicator" states the result in a form that can be read as denying that any right subsists, rather than as saying no enforceable claim remains. §6.5 makes §6 declaratory of §3–§5, so the operative effect is right | Say "no enforceable claim arises" | Medium |
| E6 | **§8.4** | The grant reaches claims infringed by "any model, parameter set, weight, embedding, or output" resulting from Computational Use, and deliberately drops §8.1's proviso limiting infringement to subject matter contained in the Work. Whether it needs to reach *outputs* as well as the *use of the Work in training* is an open drafting question — the narrower form might close the same gap at lower cost to patent-holding adopters | Consider splitting the grant: claims infringed by computational use of the Work, and separately claims infringed by the resulting model, so an adopter can see which is which | **Open question, not a defect.** The current text is coherent and its breadth is stated; what is unresolved is whether a narrower form would do the same work |
| E5 | **§2.9** | "and so is not executory" asserts a classification that a forum's insolvency law determines, not the document. The clause does give the supporting facts first — no continuing obligation on either side — which is the strongest thing a text can do | State the facts and stop; let the conclusion follow | Low — form, not substance |

## What the machine-readable layer got right

The two machine-readable artefacts are frozen alongside the text, so they were audited rather
than corrected. They came out **cleaner than the human-facing notice**:

- `ACD-1.0.machine.json` records `osiApproved: false` and `spdxListed: false`, is marked
  `NON-OPERATIVE` with the text prevailing, and its `notice` field **omits** the SPDX identifier
  line — so E1 does not propagate there. E3 does, and that is now noted in the row above.
- `ACD-1.0.spdx.xml` records `isOsiApproved="false"`.
- Every one of the **29** `clause` pointers in the descriptor resolves to a clause that exists
  and is about the subject claimed. Verify it by cross-checking the `clause` fields against
  `ACD-1.0.txt`; the result is 29/29.

That asymmetry is itself the lesson for 1.1: the machine-readable files say "not approved, not
listed" in the same breath as the identifier, and the human notice does not. **The notice should
borrow the honesty of the descriptor**, not the other way round.

## What is *not* on this list

No defect has been found that changes what a recipient may do. Every entry above is a matter of
precision, scope of wording, or the form in which a conclusion is stated. If a defect of the
first kind is found, it goes here immediately and the honest response may be to withdraw rather
than to patch — `ACD-1.0.submission.md` §E.2 and `ACD-1.0.against.md` record the conditions.

Two of these were found by a third party's adversarial reading and three by auditing the
dossier's own citations against the text. Neither route was exhaustive. **If you find a sixth,
that is a failure of our review and not of yours** — say so on the list and it will be added
here rather than argued with.

## When the freeze lifts

On the day the freeze is lifted — that is, when the discussion closes and the owner says so — the
correct order is: apply E1 first (it is the only one that misdirects a reader), re-measure every
property recorded in `ACD-1.0.submission.md` §4c, regenerate the digests in `FROZEN.md`, and
record in `ACD-1.0.discussion-log.md` which changes were driven by which feedback. A property
verified once is not a property that stays true.
