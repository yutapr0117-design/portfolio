---
file: LICENSES/QUESTIONS-FOR-COUNSEL.md
audience: a lawyer asked to read ACD, or reading it on license-review / license-discuss; the steward, when asking one
last-updated: 2026-11-11
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
on §4 and §5. (d) Covered Rights include rights the Dedicator *"may come to hold … now or in
future"* (§1.5), and in the 1.4 draft Moral Rights include rights conferred by law *"now or in
future"* (§1.2, errata E50). Whether a surrender, waiver or licence of a right not yet held takes
effect when the right arises, or needs a further act then, is a question of each forum's law
that the text cannot answer for itself. (e) In the 1.4 draft a one-line tag can apply the
Dedication (§16.1, §16.2). Whether so short a mark shows the intention an abandonment needs is
open; if it does not, §3 may fail there while §4 stands, which is what §4.4 is for. (f) OSI's FAQ
says *"we don't know how or whether the author would be protected from liability for software
released into the public domain"*. The concern is old: Lawrence Rosen, answering a request to list
public-domain dedications in 2003, wrote *"please consider using a regular open source license that
contains a disclaimer of warranty. The Public Domain Dedication does not deal with such issues
because it is not a license."* (`rounds/2003-03-license-discuss-public-domain-on-the-list-observed.txt`).
Where §3 is effective nothing is left to license, so what do §13 and §14 rest on there? (g) §10.2 lets a copy travel with no notice, and in the 1.4 draft §2.3 says
You need not know of the Dedication. Where a licence is read as a contract, can a person who has
never seen the text hold it, or does such a person rest on §3 and §5 alone and, for patents, on §8.6
alone? (h) Some statutes let an author take a grant back whatever the grant says, which (b) asks
for the United States. In Germany UrhG section 42(1) provides *"Der Urheber kann ein Nutzungsrecht
gegenüber dem Inhaber zurückrufen"* where the work no longer reflects the author's convictions;
section 42(2) says *"Auf das Rückrufsrecht kann im voraus nicht verzichtet werden."*; section 42(3) requires
the author to compensate the holder, at least for its expenses. UrhG
section 31a(1) lets the author revoke a grant of rights for types of use unknown when it was made, which
§4.2's *"by any means now known or later devised"* is; the same paragraph excuses from written form
a grant made *"unentgeltlich ein einfaches Nutzungsrecht für jedermann"* (free, non-exclusive, to
everyone), which is ACD's form, and its words do not say whether the revocation right reaches such
a grant. In France CPI L121-4 gives the author a *"droit de repentir ou de retrait vis-à-vis du
cessionnaire"* against prior indemnity, but by L121-7 the author of software, *"Sauf stipulation
contraire plus favorable à l'auteur d'un logiciel"*, cannot *"Exercer son droit de repentir ou de
retrait."* In Japan the Copyright Act's recall for a change of conviction (Article 84(3)) ends a
出版権, an exclusive right to publish, and its words do not reach a non-exclusive licence. Our
reading: these statutes reach every OSI-approved licence alike, §2.2 cannot contract out of them,
and §15.2 confines their effect to the jurisdiction concerned. We do not know whether section 42 reaches a
free non-exclusive licence offered to everyone; whether section 31a(1)'s revocation right reaches a grant
that its second sentence excuses from written form; whether a recipient under ACD is a
*cessionnaire* for L121-4; whether the documentation and data that §1.3 includes in the Work are
*logiciel* for L121-7; or whether §5's covenant not to assert would be read as excluding the exercise
of a recall, which section 42(2) forbids. (Statute text fetched on 2026-11-08 from gesetze-im-internet.de,
Légifrance LEGIARTI000006278894 and LEGIARTI000006278899, and the e-Gov law API.)

**An answer would change** whether the text keeps three footings (register B4) and how §4.4 says
"independent". An answer to (b) or (h) would change what the dossier says rather than the text: no
wording contracts out of a statute that forbids it.

## 2. Does the patent licence reach what it is meant to reach? (§8.1, §8.4, §8.6)

**The clauses.** In ACD-1.3, §8.1 licenses *"every patent claim owned or controlled by the Dedicator, now or
in future"* infringed by making, using, selling or importing the Work or a derivative, *"where the
infringement is caused by subject matter contained in the Work as made available"*. §8.4 licenses
claims infringed by Computational Use or by making or using *"any model, parameter set, weight,
embedding, or output resulting from that use"*, limited to claims *"whose infringement depends upon
the use of the Work"* — *"a question of causation and not of quantity"*. The 1.4 draft replaces
that limit (2026-11-04): a claim is reached only where *"the feature that infringes it results, in
whole or in part, from the content of the Work"*, and *"a feature that the Work teaches or embodies is
taken so to result"*. §8.2 makes both unconditional and non-terminable; §8.6 adds a covenant not to assert. In ACD-1.3 the covenant
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
model that has once processed the Work; the 1.4 wording tests the infringing feature rather than the
model, and a licensee must show that the feature came from the Work or that the Work teaches it. (c) We have not examined how an unconditional,
non-terminable patent licence to the public interacts with the Dedicator's other patent licensing.
One form of that interaction was raised against CC0 in 2012: Bruce Perens wrote that a party that
*"has licensed a patent and dedicates the software exercising that patent is obligated to help the
licensee of the patent to prosecute the party using the software"*
(`rounds/2012-03-license-review-cc0-straw-poll-observed-1of2.txt`). For ACD the question is whether
§8.6's promise *"not to authorise or assist any other person to assert"* the claims meets an earlier
duty owed to an exclusive licensee, and whether that licensee can sue a recipient regardless.
(d) Whether the §8.6 covenant survives where the licence is held ineffective, or falls with it, and
whether a covenant given alongside the licence (the 1.4 form) is treated differently from one that
arises only on a holding (the 1.3 form). (e) Whether "use" in a covenant not to assert patent claims is read as
the statutory act of using only, which is the reading the 1.4 change assumes and guards against.

(f) In the 1.4 draft §8.4 says the proviso on subject matter contained in the Work is deliberately
absent, then limits the grant to a feature resulting from the content of the Work. We read §8.1 as
testing what the Work contains and §8.4 as testing where a feature of a model or output came from.
A reader may instead see one limit taken away and the same limit put back.

(g) In ACD-1.3 the acts sit in a relative clause that selects the claims, so the licence reads as a
licence under the claim. The 1.4 draft (2026-11-07) makes the acts the object: *"licence to make,
have made, use, offer to sell, sell, import, and otherwise practise or transfer the Work or anything
derived from it"*, and §8.4 follows it. Does that list leave out an act a national law names, such
as export and lending (Japan, Patent Act Art. 2(3)) or possession (Germany, PatG §9)? We added
*"otherwise practise"* so that it should not, and we have not tested the phrase.
(h) The 1.4 draft adds to §8.4 *"Section 8.1 alone governs a feature added to the Work, by whatever
means."* Does it hold the line between a feature added to the Work and a feature of a model or
output, including where the Work is itself a model?
(i) §8.1 reaches claims *"owned or controlled by the Dedicator"*, and §8.5 defines *controlled* as the
Dedicator's own right to license. A claim held by the Dedicator's affiliate is not reached. Apache-2.0
reaches it, because its *"Legal Entity"* includes entities under common control; UPL-1.0, BlueOak-1.0.0
and BSD-2-Clause-Patent do not. We left ACD on the narrower side, because a Dedication cannot bind a
company that has not applied it (§2.7), and a claim transferred to an affiliate after application is
bound by §2.8. Is the remaining gap (a claim the affiliate already holds) a defect a reviewer would
press, and if so, is a covenant by the Dedicator not to cause an affiliate to assert it effective?

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

## 5. How far does the covenant against "any claim or cause of action" reach? (§5.1, §5.2(d), §11)

**The clause.** In ACD-1.3 §5.1 covenants not to assert *"any claim or cause of action, whether now
known or unknown, arising from or relating to a use of the Work that this Dedication permits"*.
The 1.4 draft reads *"any claim or cause of action, whether now known or unknown, for a use of the
Work that this Dedication permits, other than for patent infringement (Section 8), under trademark
rights or rights in a name (Section 11.1), for a false statement or representation (Section 11.3), or
for a payment You agreed to make"*. §5.2(d) carries only one of those exceptions, the one for a false
statement or representation (Section 11.3). §11.1 grants no trademark right; §11.3 places
misrepresentation of authorship or endorsement outside the Dedication's reach; §11.4 states that the §5 covenants are not limited by its own sentence on reach.

**Our reading.** "For a use" keeps the claims that attack the use itself, such as unjust enrichment
and unfair competition, and leaves out a claim that only accompanies a use, such as an injury
caused by a machine You run. A claim against selling a trained model stays in, because §1.7 makes
that sale a Computational Use and so a use of the Work.

**Why we doubt it.** In 1.3 we read trademark claims as surviving because the conduct is the
misrepresentation §11.3 excludes (`ACD-1.3-CHANGELIST.md`). That reading does not hold on the
words: §5.2(d) uses the same *"use of the Work that this Dedication permits"* for rights §11.4 does
not grant, and a fork that keeps the name and logo need not represent anything. A Dedicator with a
mark could then be said to have licensed it without control, so the 1.4 draft says it in words.
We have not tested whether "for" draws the line we describe, and the exception does not name data
protection, because §5.2(d) was written to stop a Dedicator's own personal rights from defeating a
permitted use (errata E31).

The 1.4 draft also excepts a payment You agreed to make (2026-11-07) and patent infringement
(2026-11-06): in 1.2 and 1.3 the words can be read to bar a patent claim that §8.4 does not license,
because the use is permitted as to the Covered Rights.

A second question sits between §10.2 and §11.3. §10.2 says You need not *"state that the Work was
modified"*; §11.3 keeps outside the Dedication *"Representing that the Dedicator authored, endorsed,
approved, sponsored, or is associated with a work, when that is not the case"*. A person who alters a
file and leaves the Dedicator's original authorship line in it, without saying it was altered, may be
read as representing that the Dedicator authored the altered file. On one reading the Dedicator did
write it, in part, so nothing false is represented; on the other the altered whole is not what the
Dedicator wrote. We did not widen §11.3 to name an altered work presented as unaltered, because that
would turn §10.2 into a condition in practice (`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.18, T41). Which
reading a court would take, and whether an author's claim for this survives in a jurisdiction where
§12.2 applies (§12.5 keeps false attribution outside the covenant), we cannot say.

**An answer would change** whether "for" is the right word, and whether data protection needs its
own exception. An answer to the second question would change whether §11.3 needs the altered-work case in words.

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

The 1.4 draft adds a rule on the Dedicator's own notices (§16.2, 2026-11-10): *"a notice that is
only a Reservation assigns nothing to other terms (Section 6.2)"*. It is meant to stop an opt-out
notice the Dedicator places from taking that material out of the Work. If a court treats such a
notice as the Dedicator's statutory reservation all the same, §16.2 and the statute point different
ways for that material, and §6.3's withdrawal is what has to carry it.

**An answer would change** whether §6.2 and §6.3 can stay as statements of the Dedicator's own
position, and whether the §16.2 rule does what it is meant to do or should be dropped.

## 7. What follows from naming no governing law and no forum? (§15.3)

**The clause.** *"This Dedication specifies no governing law and no forum. It is intended to
operate under the law of each jurisdiction in which the Work is used."*

**Why we doubt it.** OSI's board, approving another licence, said *"it does not believe that
choice of law provisions are necessary or advisable in open source licenses"* (`against.md`
#254), which supports the omission; but a recipient sued abroad has no clause to point to, and
the dossier records that as a cost: #23 is answered only in part, and #170 lists national rules a
forum could apply against several clauses.

**An answer would change** whether the second sentence of §15.3 stays. #23 reads *"It is intended to
operate under the law of each jurisdiction in which the Work is used, according to that law"* as a
declaration about conflict of laws that a forum need not follow; if it does no work, it can go.

## 8. Does the Dedication survive the Dedicator's insolvency? (§2.9)

**The clause.** Nothing in the Dedication is conditioned on, suspended by, or revived by an
insolvency proceeding, and an insolvency officer is a transferee bound under §2.8. What the officer
is bound to differs by version: in ACD-1.3, §2.8 binds Sections 3, 4, 6 and 8, so the covenants in
§5 reach transferees only through §5.3's narrower list, and §7.2 and §2.5 are left out (errata E46,
E49). The 1.4 draft binds the whole Dedication as it concerns the Work and states that §5.3 and
§12.4 do not narrow §2.8 (2026-11-02).

**Why we doubt it.** Whether a trustee can reject the licence as an executory contract is for the
forum's insolvency law, and *Jaffé v. Samsung* (4th Cir. 2013) shows that protection under
11 U.S.C. §365(n) can turn on a balancing in a cross-border case. The text no longer asserts the
result (errata E5, E30); whether its structure — no obligation on the licensee — keeps it outside
"executory" is what we cannot judge.

**An answer would change** whether §2.9 needs more than the 1.4 draft gives it, and how the dossier
answers #178 (`jurisdictions.md` §9a (10), on Qimonda).
In *Jaffé v. Samsung* the result took a four-day evidentiary hearing and a discretionary
balancing (#178), so the core of the question is whether §2.9's statement that nothing in the
Dedication is *"suspended by, or revived by"* such a proceeding or an officer's act would be read
the same way under another jurisdiction's insolvency law.

## 9. Does the limitation of liability reach a breach of the Dedicator's own covenants? (§14.1, §5, §8.6, §12.2)

**The clauses.** §14.1, set in capitals as conspicuous: the Dedicator *"IS NOT LIABLE TO YOU OR TO
ANY OTHER PERSON, ON ANY LEGAL THEORY, FOR ANY … LOSS OR DAMAGE ARISING OUT OF THIS DEDICATION OR
THE USE OF THE WORK"*. §5.1,
§8.6 and §12.2 are promises by the Dedicator not to assert claims against You, and §5.3 lets You
and later recipients rely on them as intended beneficiaries.

**Our reading.** The covenants work chiefly as a defence: a recipient sued in breach of one points
to it, and the claim fails. Damages for the breach are secondary, and §14.2 keeps whatever
liability a jurisdiction does not allow to be excluded, which in many includes deliberate breach.

**Why we doubt it.** Read literally, "ARISING OUT OF THIS DEDICATION" includes a breach of the
Dedication's own promises, so a recipient put to the cost of defending a suit the Dedicator
promised not to bring may have no claim for that cost. GPL-3.0 §16 limits liability for damages
*"arising out of the use or inability to use the program"*, which does not reach the licensor's
own breach; ACD's wording is wider. Apache-2.0 §8 is as wide on this point (*"arising as a result
of this License or out of the use or inability to use the Work"*), so the wording has an approved
precedent, but Apache-2.0 gives no covenant for it to reach, and it excepts what applicable law
requires, naming *"deliberate and grossly negligent acts"*. We found this by setting §14.1 beside
the covenants, which share no term with it (`ACD-1.4-CHANGELIST.md`, the pre-finalisation checks).

(b) A second question about the same clause concerns whom it protects. §1.4 defines the Dedicator
*"to the extent that person or entity holds or may hold Covered Rights, Moral Rights, or patent claims
in it"*. A maintainer who distributes a Work containing contributors' code, third-party material, or
machine-generated parts in which no right subsists holds no right in those parts. Does §14.1 protect
that maintainer against a loss caused by such a part? Our reading is that it does: §13.2 disclaims any
warranty *"THAT THE DEDICATOR HOLDS ANY RIGHT IN IT"*, so the text uses "the Dedicator" for the person
who applied the Dedication whether or not that person holds a right, and §1.4's limit governs what is
dedicated, not who is protected. Apache-2.0 §8 reaches the same result in its own words by making the
subject *"any Contributor"*, defined to include the Licensor. We did not change the text: a wording that
named the parts without rights produced a sentence about a Dedicator who, for those parts, is not one
(`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.19).

**An answer would change** whether §14.1 should exclude liability only for the use of the Work, as
GPL-3.0 does, or say that it does not limit the covenants. An answer to (b) would change whether §14.1 needs its own subject.

---

## How to answer

In any form, on a list or privately. **Public answers are recorded word for word** in
`LICENSES/rounds/`. **Private correspondence is not published**: only its date, its direction and a
pointer to where the analysis uses it are recorded (`rounds/README.md`). Correction of any reading
on this page is the most useful answer; agreement is the next most useful, because it moves B1.
Nothing here asks a reader to take on any obligation, and a short answer to one question is worth
more to us than a long one to all nine.
