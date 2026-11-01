---
file: LICENSES/QUESTIONS-FOR-COUNSEL.md
audience: a lawyer asked to read ACD, or reading it on license-review / license-discuss; the steward, when asking one
last-updated: 2026-11-02
canonical-ref: LICENSES/ACD-1.3.txt (the latest fixed text, applied to this repository) / LICENSES/ACD-1.4-DRAFT.txt (the successor draft) / LICENSES/ACD-1.0.jurisdictions.md (where we think each question sits, by jurisdiction) / LICENSES/ACD-OSI-BOTTLENECKS-EXTERNAL.md (B1)
---

# Questions for counsel

**ACD has had no legal review.** The review record asks for one again and again, and one
reviewer joined it in a single sentence to the other thing ACD lacks (register B1: *"submitted
licenses should have either received legal review or at least non-negligible use. This license
has neither"*). Nothing in this repository can supply it. This page exists to make one review cheap: it lists, in order of
consequence, the questions on which a lawyer's reading would most change the text — for each,
the clause, what it is meant to do, our own reading, and why we doubt that reading.

**What this page is not.** It is not legal advice to anyone. It does not ask for an opinion on
Open Source Definition conformance, which is OSI's question rather than a lawyer's. It is not a
summary of the dossier. Any one question can be answered without reading the others.

**Which text.** Clause numbers are those of **ACD-1.3** (`ACD-1.3.txt`, fixed on 2026-10-25,
80 clauses), which is the version this repository applies. ACD-1.2 and the successor draft
ACD-1.4 use the same numbers; the draft differs only by the changes its header lists. **ACD-1.0, the version posted to license-discuss, numbers some clauses
differently** (the definitions were reordered and Section 15 shifted); the mapping is in
`ACD-1.2-CHANGELIST.md`.

**Who wrote this page.** An AI model (Claude), working in this repository under the steward's
delegation, from the repository's own analysis. The licence text was drafted the same way; the
steward read ACD-1.0 in full before posting it. Neither has been reviewed by a lawyer.

---

## 1. Can a surrender and a licence of the same rights stand side by side? (§3, §4, §4.4)

**The clauses.** §3.1 surrenders all Covered Rights and places the Work in the public domain
*"in each jurisdiction that gives effect to such an act"*; §3.3 waives where surrender is not
possible. §4.1 licenses the same rights *"for any purpose whatsoever"*, and §4.4 says the licence
*"is granted independently of Section 3, and not as a fallback for it: it takes effect whether
or not Section 3 does."*

**Meant to do.** Give the recipient a footing that does not depend on whether the surrender works
in a given jurisdiction, without making the licence conditional on the surrender failing — CC0's
fallback licence leaves the recipient to decide whether the waiver failed.

**Our reading.** Where the surrender is effective, nothing is left to license and §4 is harmless;
where it is not, §4 operates.

**Why we doubt it.** (a) A reviewer has asked of a similar instrument, *"Which is it, a dedication
to the public domain or a license?"*; a court construing an instrument that both abandons and
licenses a right may read one in the light of the other. (b) In the United States §4 is a licence
executed by the author and so, on our reading of 17 U.S.C. §203, terminable after 35 years
*"notwithstanding any agreement to the contrary"*; abandonment is neither a transfer nor a licence,
but whether copyright can be abandoned at all is unsettled (`jurisdictions.md` §5a). (c) In
Germany, where copyright cannot be transferred or waived, §3 may do nothing and everything rests
on §4 and §5.

**An answer would change** whether the text keeps three footings (register B4) and how §4.4 says
"independent".

## 2. Does the patent licence reach what it is meant to reach? (§8.1, §8.4, §8.6)

**The clauses.** §8.1 licenses *"every patent claim owned or controlled by the Dedicator, now or
in future"* infringed by making, using, selling or importing the Work or a derivative, *"where the
infringement is caused by subject matter contained in the Work as made available"*. §8.4 licenses
claims infringed by Computational Use or by making or using *"any model, parameter set, weight,
embedding, or output resulting from that use"*, limited to claims *"whose infringement depends upon
the use of the Work"* — *"a question of causation and not of quantity"*. §8.2 makes both
unconditional and non-terminable; §8.6 adds a covenant not to assert. In ACD-1.3 the covenant
arises where a licence is held ineffective; the 1.4 draft makes it operate alongside the licences
in every jurisdiction (2026-11-01), because a covenant that arises only on a holding does not
exist when the claim that produces the holding is first asserted. The 1.4 draft also ties the covenant's
reach to "any act that those Sections describe"; 1.3 says "any use of the Work or of anything
resulting from Computational Use of it", and in a patent covenant "use" may name only one of the
acts (making, selling, importing) that §8.1 and §8.4 license (errata E45).

**Meant to do.** Close the gap on which CC0 stopped at OSI (patent rights expressly withheld), and
reach trained models and outputs, which no approved licence names (`gap-census.md`).

**Our reading.** "Controlled" bears its ordinary meaning (the power to license), and the causation
limit is definite enough to apply.

**Why we doubt it.** (a) "Controlled" is undefined in ACD-1.3; GPL-3.0 and MPL-2.0 define their
equivalents. The 1.4 draft now defines it in §8.5 (a claim the Dedicator can license, at the time
in question, without breaching an obligation to or paying another person; errata E39) — whether
that definition is the right one is part of the question.
(b) A causal limit with no threshold may be read as too indefinite to operate, or as reaching any
model that has once processed the Work. (c) We have not examined how an unconditional,
non-terminable patent licence to the public interacts with the Dedicator's other patent licensing.
(d) Whether the §8.6 covenant survives where the licence is held ineffective, or falls with it, and
whether a covenant given alongside the licence (the 1.4 form) is treated differently from one that
arises only on a holding (the 1.3 form). (e) Whether "use" in a covenant not to assert patent claims is read as
the statutory act of using only, which is the reading the 1.4 change assumes and guards against.

**An answer would change** the wording of §8.4 (register B7; errata E6 and E15).

## 3. Are the moral-rights covenants enforceable where waiver is not? (§12.1 to §12.5)

**The clauses.** §12.1 waives Moral Rights to the extent the law permits. §12.2 replaces the waiver,
where moral rights are inalienable, with a covenant not to exercise them against You. §12.3 limits
the covenant to the Work. §12.4 binds successors and *"any person entitled to exercise or enforce
Moral Rights in the Work after the Dedicator's death"*. §12.5 keeps false attribution outside the
covenant.

**Meant to do.** Remove the integrity right as an obstacle to modifying the Work, in the form that
Japanese practice already uses (a covenant not to exercise rights that Article 59 of the Copyright
Act makes inalienable), without reaching other works.

**Why we doubt it.** (a) Whether a covenant given to the public at large, rather than to a known
counterparty, is enforceable in Japan, Germany or France. (b) Whether §12.4 can bind persons who,
after the author's death, act in their own right (Japan, Articles 60 and 116). (c) Whether a court
would treat a covenant this broad as contrary to public order even though §12.3 confines it.
(d) Whether any jurisdiction treats Moral Rights as transferable yet requires a formality, such as
a signed writing, for a waiver. There §12.2's covenant would not operate, since its trigger is that
the rights are personal, inalienable, or incapable of waiver, while §12.1's waiver, given without a
signature, may fail for want of form. The United States (17 U.S.C. §106A(e)(1)) and the United
Kingdom (CDPA s.94) make the rights non-transferable, so §12.2 applies there; we know of no
jurisdiction in the gap, which is why the text was not changed (2026-11-01).

**An answer would change** §12.2 and §12.4, the clauses on which the dossier most wants correction
(`jurisdictions.md` §10).

## 4. Does a contribution fall under the Dedication by default? (§2.6, §1.9)

**The clause.** *"A Contribution is submitted under this Dedication, and the person making it
becomes a Dedicator as to that Contribution, unless they state otherwise at the time of
submission."* A Contribution is material *"intentionally"* submitted for inclusion.

**Why we doubt it.** A surrender or waiver of copyright usually needs clear evidence of intent;
an intent to contribute is not obviously an intent to surrender. Inbound-equals-outbound works
for licences such as Apache-2.0 (§5), but a public-domain surrender may need more than a default.

**An answer would change** whether §2.6 should require an affirmative statement, at a cost to
projects that accept contributions informally.

## 5. How far does the covenant against "any claim or cause of action" reach? (§5.1, §11)

**The clause.** §5.1 covenants not to assert *"any claim or cause of action, whether now known or
unknown, arising from or relating to a use of the Work that this Dedication permits"*. §11.1
grants no trademark right; §11.3 places misrepresentation of authorship or endorsement outside
the Dedication's reach; §11.4 states that the §5 covenants are not limited by its own sentence on
reach.

**Our reading.** Trademark and passing-off claims survive, because the conduct they address is
the misrepresentation §11.3 excludes, which is not "a use … that this Dedication permits"
(recorded as examined in `ACD-1.3-CHANGELIST.md`).

**Why we doubt it.** The reading needs three clauses read together, and "relating to" is broad.
If a court read §5.1 as releasing trademark claims against distributions of the Work, a Dedicator
with a mark could be said to have licensed it without control.

**An answer would change** whether §5.1 should say expressly that Section 11 is unaffected.

## 6. Do the text-and-data-mining declarations do anything? (§6.2, §6.3)

**The clauses.** §6.2: the Dedicator *"makes no Reservation … and expressly declines to make
one"*, and no signal associated with the Work is to be read as a Reservation *"so far as the
Covered Rights and patent claims of the Dedicator are concerned"*. §6.3: the Dedicator withdraws
any Reservation *"to the fullest extent the Dedicator is able"*, and disclaims reliance on any.

**Why we doubt it.** Under Article 4(3) of Directive (EU) 2019/790 a reservation is the
rightsholder's statutory act. Whether a rightsholder can bind itself in advance never to make one,
and whether a reservation placed by a host or platform (not a rightsholder) has any effect for the
purpose of the exception, are questions on which a German appellate court has ruled in a case
about the same exception (HansOLG 5 U 104/24; `jurisdictions.md` §9a(9)) — we have read the
court's own announcement, not the judgment.

## 7. What follows from naming no governing law and no forum? (§15.3)

**The clause.** *"This Dedication specifies no governing law and no forum. It is intended to
operate under the law of each jurisdiction in which the Work is used."*

**Why we doubt it.** OSI's board, approving another licence, said *"it does not believe that
choice of law provisions are necessary or advisable in open source licenses"* (`against.md`
#254), which supports the omission; but a recipient sued abroad has no clause to point to, and
the dossier records that as a cost it has not answered (#23, #170).

## 8. Does the Dedication survive the Dedicator's insolvency? (§2.9)

**The clause.** Nothing in the Dedication is conditioned on, suspended by, or revived by an
insolvency proceeding, and an insolvency officer is a transferee bound under §2.8.

**Why we doubt it.** Whether a trustee can reject the licence as an executory contract is for the
forum's insolvency law, and *Jaffé v. Samsung* (4th Cir. 2013) shows that protection under
11 U.S.C. §365(n) can turn on a balancing in a cross-border case. The text no longer asserts the
result (errata E5, E30); whether its structure — no obligation on the licensee — keeps it outside
"executory" is what we cannot judge.

## 9. Does the limitation of liability reach a breach of the Dedicator's own covenants? (§14.1, §5, §8.6, §12.2)

**The clauses.** §14.1: the Dedicator *"is not liable to You or to any other person, on any legal
theory, for any … loss or damage arising out of this Dedication or the use of the Work"*. §5.1,
§8.6 and §12.2 are promises by the Dedicator not to assert claims against You, and §5.3 lets You
and later recipients rely on them as intended beneficiaries.

**Our reading.** The covenants work chiefly as a defence: a recipient sued in breach of one points
to it, and the claim fails. Damages for the breach are secondary, and §14.2 keeps whatever
liability a jurisdiction does not allow to be excluded, which in many includes deliberate breach.

**Why we doubt it.** Read literally, "arising out of this Dedication" includes a breach of the
Dedication's own promises, so a recipient put to the cost of defending a suit the Dedicator
promised not to bring may have no claim for that cost. GPL-3.0 §16 limits liability for damages
*"arising out of the use or inability to use the program"*, which does not reach the licensor's
own breach; ACD's wording is wider. We found this by setting §14.1 beside the covenants, which
share no term with it (`ACD-1.4-CHANGELIST.md`, the pre-finalisation checks).

**An answer would change** whether §14.1 should exclude liability only for the use of the Work, as
GPL-3.0 does, or say that it does not limit the covenants.

---

## How to answer

In any form, on a list or privately. **Public answers are recorded word for word** in
`LICENSES/rounds/`. **Private correspondence is not published**: only its date, its direction and a
pointer to where the analysis uses it are recorded (`rounds/README.md`). Correction of any reading
on this page is the most useful answer; agreement is the next most useful, because it moves B1.
Nothing here asks a reader to take on any obligation, and a short answer to one question is worth
more to us than a long one to all nine.
