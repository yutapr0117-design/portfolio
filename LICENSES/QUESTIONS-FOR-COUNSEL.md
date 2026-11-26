---
file: LICENSES/QUESTIONS-FOR-COUNSEL.md
audience: a lawyer asked to read ACD, or reading it on license-review / license-discuss; the steward, when asking one
last-updated: 2026-11-25
canonical-ref: LICENSES/ACD-1.4.txt (the latest fixed text, applied to this repository) / LICENSES/ACD-1.5-DRAFT.txt (the successor draft) / LICENSES/ACD-1.0.jurisdictions.md (where we think each question sits, by jurisdiction) / LICENSES/ACD-OSI-BOTTLENECKS-EXTERNAL.md (B1)
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

**Which text.** Clause numbers are those of **ACD-1.4** (`ACD-1.4.txt`, fixed on 2026-11-23, 80 clauses), which is the version this repository applies. ACD-1.2 and ACD-1.3 use the same numbers. **ACD-1.0, the version posted to license-discuss, numbers some clauses
differently** (the definitions were reordered and Section 15 shifted); the mapping is in
`ACD-1.2-CHANGELIST.md`.

**Who wrote this page.** An AI model (Claude), working in this repository under the steward's
delegation, from the repository's own analysis. The licence text was drafted the same way; the
steward read ACD-1.0 in full before posting it. Neither has been reviewed by a lawyer.

---

## 1. Can a surrender and a licence of the same rights stand side by side? (§2.3, §3, §4, §4.4)

**The clauses.** §3.1 surrenders all Covered Rights and places the Work in the public domain
*"in each jurisdiction that gives effect to such an act"*; §3.3 waives where surrender is not
possible. §4.1 licenses the same rights *"for any purpose whatsoever"*, and §4.4 says the licence
*"is granted independently of Section 3, and not as a fallback for it: it is granted whether
or not Section 3 is effective."*

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
future"* (§1.5), and in ACD-1.4 Moral Rights include rights conferred by law *"now or in
future"* (§1.2, errata E50). Whether a surrender, waiver or licence of a right not yet held takes
effect when the right arises, or needs a further act then, is a question of each forum's law
that the text cannot answer for itself. (e) In ACD-1.4 a one-line tag can apply the
Dedication (§16.1, §16.2). Whether so short a mark shows the intention an abandonment needs is
open; if it does not, §3 may fail there while §4 stands, which is what §4.4 is for. (f) OSI's FAQ
says *"we don't know how or whether the author would be protected from liability for software
released into the public domain"*. The concern is old: Lawrence Rosen, answering a request to list
public-domain dedications in 2003, wrote *"please consider using a regular open source license that
contains a disclaimer of warranty. The Public Domain Dedication does not deal with such issues
because it is not a license."* (`rounds/2003-03-license-discuss-public-domain-on-the-list-observed.txt`).
Where §3 is effective nothing is left to license, so what do §13 and §14 rest on there? (g) §10.2 lets a copy travel with no notice, and in ACD-1.4 §2.3 says
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
(i) §2.5 states that others' reliance is the purpose of the Dedication, and that the Dedicator will not
assert that it is revocable or ineffective for want of consideration or formality, *"and is estopped
from doing so to the extent the law of any jurisdiction gives that principle effect"*. Lawrence Rosen
wrote in 2004 that *"Promissory estoppel is a contract doctrine that has nothing to do with a bare
license like the GPL."* (`against.md` #236). Where a court treats the Dedication as a bare licence and
does not apply estoppel, what protects a recipient against revocation for want of consideration: the
words *"irrevocable"* and *"perpetual"* in §4.1, the covenants in §5, or nothing?
The same lawyer wrote in 2003, a day after advising *"Grant an irrevocable license."*, that
*"Probably a new licensee with notice of the revocation can't obtain a license."*, and another
participant (not a lawyer, by his own account) put it as *"no harm, no estoppel."*
(`gap-measurements.md` §1.146). So a narrower form of the question is whether §2.5, §4.1 or §5
protects a person who first meets the Work after the Dedicator has purported to revoke it, and has
notice of that. John Cowan (not a lawyer, by his own account) wrote in the same year of a licence that declared
itself irrevocable: *"All that is, is a promise to yourself, and it's not binding, any more than your
publishing a promise never to tell a lie is."* (`review-readings-2.md` §1.242). That is the view under
which §2.2 alone would do nothing, and §2.5 and §3.1 are what the text adds to it.
In the United States the authorities we have read narrow (i) to one line. Rosen wrote in 2005 that
licences *"are not contracts until the formalities of contract formation"* are completed, *"Until then
they are bare licenses."* (`rounds/2005-08-license-discuss-bare-licenses-rosen-assent-observed.txt`);
§2.3 asks for no acceptance, so on that view the Dedication is a bare licence there. The Ninth Circuit
tied irrevocability to payment: *"because AMS paid consid-eration, this license is irrevocable"*
(*Asset Marketing Systems v. Gagnon*, 2008, as the copy hyphenates it;
`rounds/2026-11-16-us-asset-marketing-v-gagnon-consideration-snapshot.txt`). That leaves promissory
estoppel, which section 90(1) of the Restatement (Second) of Contracts states as *"A promise which the promisor should
reasonably expect to induce action or forbearance on the part of the"* promisee or a third person, and
which does so, binding *"if injustice can be avoided"* only by enforcement
(`rounds/2026-11-16-us-restatement-90-promissory-estoppel-snapshot.txt`, as quoted by state courts).
§2.5's *"intending that others rely on it"* speaks to the first element on the face of the text; actual
reliance and injustice are facts of each case, and Rosen's 2004 view above denies that the doctrine
reaches a bare licence at all. So the open part is whether section 90 reaches a bare licence, and the facts.
In England and Wales the doctrine is narrower and, on our reading, fits what §2.5 asks of it. The Court of Appeal said
that promissory estoppel *"cannot alone confer positive rights on the promisee"*, *"(often expressed by
saying that the doctrine operates as a shield and not as a sword)"* (*Harvey v Dunbar Assets*, 2017, a
case on a guarantee; `rounds/2026-11-17-harvey-v-dunbar-2017-ewca-civ-60-promissory-estoppel-snapshot.txt`).
§2.5 needs only the shield: a recipient sued by a Dedicator who says the Dedication is revocable answers
with the estoppel. Whether an English court applies it to a promise made to the public, and on what
reliance, is the open part there. Nor, on our reading, can the Dedication bind as a deed in England and Wales: the Law of
Property (Miscellaneous Provisions) Act 1989, section 1(2), requires that an instrument *"makes it clear on
its face that it is intended to be a deed"* and *"is validly executed as a deed"*, which for an individual
means a signature attested by a witness and delivery (`rounds/2026-11-19-uk-lpmpa-1989-s1-deeds-snapshot.txt`).
A published dedication is neither, so a gratuitous promise in it is enforced there, if at all, as a contract
where the recipient gives something in return, or through the estoppel above.
On whether a gratuitous licence can be irrevocable at all, Mummery LJ in the Court of Appeal in *Fisher v
Brooker* (2008) said of a copyright licence that *"It may be for a consideration or gratuitous, exclusive or non-exclusive,
revocable or irrevocable"* (paragraph 34(2); Sir Paul Kennedy agreed with Mummery LJ *"for the reasons he has given"*, paragraph
141). Against that, David Richards J, who partly dissented on a different point (acquiescence and
laches), said of a licence presumed from conduct that *"Such a presumed licence is prima facie revocable on reasonable notice."*
(paragraph 120; `rounds/2026-11-19-uk-fisher-v-brooker-2008-ewca-civ-287-gratuitous-licence-snapshot.txt`).
He added that *"The licence is revocable unless the defendant has acted to his detriment such that revocation
would be unconscionable."* (paragraph 136; `rounds/2026-11-19-uk-fisher-v-brooker-2008-paras-136-141-snapshot.txt`):
on that view what stops revocation of an implied gratuitous licence is reliance to the licensee's detriment, which is
what §2.5 invites, and a recipient who has not relied would have no footing in §2.5 against revocation.
The House of Lords ([2009] UKHL 41) allowed the claimant's appeal and restored the declaration that the
implied licence had been revoked; we have its outcome only as a later judgment summarises it: *"The claimant’s
appeal to the House of Lords was allowed and the second and third declarations"* *"made by the judge at first
instance were restored."*, quoting Lord Hope, *"it would be a very strong thing, in the absence of a
proprietary estoppel, to deny him the opportunity of"* *"exercising his right of property in his own share of
the copyright."* (`rounds/2026-11-19-uk-noel-redding-v-sony-2026-fisher-v-brooker-hl-snapshot.txt`). So the
majority of the Court of Appeal was reversed on the point decided there, laches and estoppel, not on the
general statement in paragraph 34(2). On our reading, formation is the smaller question in England: infringement is an act done *"without the licence of the copyright owner"*, with no element of the licensee's knowledge or acceptance (CDPA section 16(2)), and section 92(1) asks for writing and a signature only of an *"exclusive licence"* (`rounds/2026-11-19-cdpa-1988-s16-s92-licence-snapshot.txt`). A recipient who has never heard of the Dedication (§2.3) therefore plausibly holds the licence, and the question moves to revocation, where that recipient, having relied on nothing, has no footing in §2.5. The revocation holdings above concern a licence presumed from conduct. The Dedication is an
express licence that calls itself irrevocable. Does an English court treat an express gratuitous licence to
the public as irrevocable on its words, or, as with the presumed licence, as revocable unless an estoppel
(which §2.5 invites) stops it?
(j) A transfer after the Dedication. Under 17 U.S.C. section 205(e), a nonexclusive licence prevails over a
conflicting transfer of copyright ownership only if it is evidenced by a written instrument signed by
the owner of the rights licensed or the owner's agent, and was taken before the transfer was executed,
or in good faith before the transfer was recorded and without notice of it (text read on 2026-11-12 at
the Legal Information Institute; we have not read a case that applies it to a public licence). Nobody
signs the Dedication for each recipient, and §2.8 says that it binds any person to whom a Covered Right
is transferred *"to the fullest extent the law permits"*. Its second sentence said, without that limit,
that a transferee takes subject to it; since 2026-11-12 ACD-1.4 says *"A transferee takes subject
to it to that extent, Section 6 included."*, so that the text claims no more than the statute may allow
(`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.32, T59; errata E79). In the United States, does a recipient's
licence under §4 prevail over a later assignee of the copyright, and does it matter whether §3 has
already taken effect, leaving nothing to transfer?
In Japan the statute answers for a licence. Copyright Act Article 63-2 reads:
*"利用権は、当該利用権に係る著作物の著作権を取得した者その他の第三者に対抗することができる。"*
A right of use may be asserted against a person who later acquires the copyright, with no registration
(`rounds/2026-11-16-minpo-chosakukenho-e-gov-api-snapshot.txt`), so §2.8 states what Japanese law already does if §4 is a grant of a right of use
under Article 63. Whether it is one is the question of §1 above.
In the United Kingdom, CDPA section 90(4) makes a copyright owner's licence binding on every successor in
title *"except a purchaser in good faith for valuable consideration and without notice (actual or
constructive) of the licence"* (`rounds/2026-11-16-cdpa-1988-s87-s90-legislation-gov-uk-snapshot.txt`).
A Dedication published with the Work makes notice likely, but a purchaser who never saw it is the case
§2.8's *"to the fullest extent the law permits"* leaves to the law. For patents in Germany the statute
answers outright: PatG section 15(3), *"Ein Rechtsübergang oder die Erteilung einer Lizenz berührt nicht
Lizenzen, die Dritten vorher erteilt worden sind."* (a transfer or a licence does not affect licences
granted to third parties before it; `rounds/2026-11-20-patent-usc-patg-berne-trips-snapshot.txt`), so §8's licences bind a later owner of
the patent there. In the United States, 35 U.S.C. section 261 voids an unrecorded *"assignment, grant or
conveyance"* against a later purchaser without notice; whether a non-exclusive licence given to the
public is such an interest we have not read a case on.

A further question concerns the recipient who never saw the Dedication. In ACD-1.4, §2.3 says
*"To hold a permission granted here, You need not know of this Dedication"*, which matters because §10.2
lets a copy travel with no notice. Where §4 is read as a contract, German civil code section 151 dispenses
only with declaring acceptance to the offeror (*"ohne dass die Annahme dem Antragenden gegenüber erklärt zu
werden braucht"*), and a person who does not know of an offer cannot accept it; Japan's civil code
article 527 raises the same question. Does such a recipient hold the §4 permission? If not, does the
public dedication still work as a unilateral consent of the kind the German Federal Court of Justice
recognised in 2010 (I ZR 69/08, *Vorschaubilder I*), and if so, can the Dedicator revoke that consent
despite §2.2? (`jurisdictions.md` §2 and §3; `against-2.md` #321.)

(k) A licence of no fixed duration (added 2026-11-23). §4.1 and §8.1 grant an *"irrevocable, perpetual"* licence.
A list participant who is a lawyer wrote on `license-review` (2025-02-24, on another submission) that in some
jurisdictions an agreement of no fixed duration can be ended on reasonable notice, while saying it was probably
not relevant to approval. Does such a rule reach the licence in §4.1 or §8.1 in Italy or France, despite
*"irrevocable"* and §2.2? If it does, would tying the term to the life of the rights, as EUPL does with
*"for the duration of copyright vested in the Original Work"*, help a text whose Covered Rights also include
rights with no fixed statutory term (rights against unfair extraction) and sui generis database rights, whose
term can begin again with new investment? We drafted that change for the next version and did not adopt it
(`ACD-1.5-CLARITY-TRIAL.md` §3, T136): the single word *"perpetual"* also carries the licence across a right that
lapses and is restored, which a term tied to subsistence would interrupt. We have not read the French or
Italian provisions in an official copy (Légifrance refused automated retrieval on 2026-11-23), so the premise
is the list participant's statement, not our reading of the statute.

**What a German attorney has written about the closest instrument (added 2026-11-16).** Till Kreutzer's
analysis of CC0 under German law (c. 2011, cited on `license-review` in 2020) narrows (c). He wrote that
the waiver is ineffective there (*"the waiver in sec. 2 of the CC0 is not legally effective under German
copyright law"*), that the fallback licence is effective, and that even without one *"public domain
licenses ... are reinterpreted as unconditional, unlimited, non-exclusive (i.e. public) licenses"* in the
prevailing opinion of scholars. He read the non-assertion as *"a valid and binding assurance to desist
from taking legal actions"* (`rounds/2026-11-16-kreutzer-cc0-german-law-analysis-snapshot.txt`). On that view §3 does
nothing in Germany, as (c) supposes, but §4 and §5 carry the Dedication there, and §4.4 does not depend on
a reinterpretation. It is one attorney's opinion on CC0, not a decision, and the extract breaks off where
he turns to moral rights, so §12 is not covered by it.

**An answer would change** whether the text keeps three footings (register B4) and how §4.4 says
"independent". An answer to (b) or (h) would change what the dossier says rather than the text: no
wording contracts out of a statute that forbids it. An answer to (i) would change whether §2.5 needs
anything beyond §4.1 and §5, or whether the dossier must say that it has no answer. An answer to (j) would change whether
the guidance for adopters should suggest a signed statement, which nothing in the text asks for. An answer to (k)
would change whether a later version ties the term of §4.1 and §8.1 to the life of the rights it can name.

## 2. Does the patent licence reach what it is meant to reach? (§8.1, §8.4, §8.6)

**The clauses.** In ACD-1.3, §8.1 licenses *"every patent claim owned or controlled by the Dedicator, now or
in future"* infringed by making, using, selling or importing the Work or a derivative, *"where the
infringement is caused by subject matter contained in the Work as made available"*. §8.4 licenses
claims (in ACD-1.3) infringed by Computational Use or by making or using *"any model, parameter set, weight,
embedding, or output resulting from that use"*, limited to claims *"whose infringement depends upon
the use of the Work"* — *"a question of causation and not of quantity"*. ACD-1.4 replaces
that limit (2026-11-04): a claim is reached only where *"the feature that infringes it results, in
whole or in part, from the content of the Work"*, and *"a feature that the Work teaches or embodies is
taken so to result"*. §8.2 makes both unconditional and non-terminable; §8.6 adds a covenant not to assert. In ACD-1.3 the covenant
arises where a licence is held ineffective; ACD-1.4 gives it for every jurisdiction without
waiting for a licence to be held ineffective (2026-11-01; since T86 it says *"it is given for every
jurisdiction"*, not that it operates there), because a covenant that arises only on a holding does not
exist when the claim that produces the holding is first asserted. ACD-1.4 also ties the covenant's
reach to "any act that those Sections describe"; ACD-1.3 says "any use of the Work or of anything
resulting from Computational Use of it", and in a patent covenant "use" may name only one of the
acts (making, selling, importing) that §8.1 and §8.4 license (errata E45).

**Meant to do.** Close the gap on which CC0 stopped at OSI (patent rights expressly withheld), and
reach trained models and outputs, which no approved licence names (`gap-census.md`).

**Our reading.** "Controlled" bears its ordinary meaning (the power to license), and the causation
limit is definite enough to apply.

**Why we doubt it.** (a) "Controlled" is undefined in ACD-1.3; GPL-3.0 and MPL-2.0 define their
equivalents. ACD-1.4 now defines it in §8.5 (a claim the Dedicator can license, at the time
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

(f) In ACD-1.4 §8.4 says the proviso on subject matter contained in the Work is deliberately
absent, then limits the grant to a feature resulting from the content of the Work. We read §8.1 as
testing what the Work contains and §8.4 as testing where a feature of a model or output came from.
A reader may instead see one limit taken away and the same limit put back.

(g) In ACD-1.3 the acts sit in a relative clause that selects the claims, so the licence reads as a
licence under the claim. ACD-1.4 of 2026-11-07 made the acts the object: *"licence to make,
have made, use, offer to sell, sell, import, and otherwise practise or transfer the Work or anything
derived from it"*, and §8.4 followed it. Did that list leave out an act a national law names, such
as export and lending (Japan, Patent Act Art. 2(3)) or possession (Germany, PatG §9)? We had added
*"otherwise practise"* so that it should not, and we have not tested the phrase. **ACD-1.4 answers this part (trial T94).** The list now reads *"make,
have made, use, offer, sell, lend, lease, import, export, keep, possess, and otherwise practise or transfer
the Work or anything derived from it"*, in §8.1 and in §8.4, so the acts that Japanese, German and United
Kingdom patent law name are in the words. *"offer"* replaces *"offer to sell"* because those laws also
count an offer to use a patented method; it is wider than the *"offer to sell"* of 35 U.S.C. §271(a) and
of Apache-2.0 §3. *"otherwise practise"* stays for any act a law names that the list still misses.
For a process patent, TRIPS Article 28.1(b) extends the owner's right to *"the product obtained directly
by that process"* (`rounds/2026-11-20-patent-usc-patg-berne-trips-snapshot.txt`); §8.4's list of acts reaches a model or output that
results from Computational Use, so a model that is the direct product of a patented training method is
within the words.
(h) ACD-1.4 adds to §8.4 *"Section 8.1 alone governs a feature added to the Work, by whatever
means."* Does it hold the line between a feature added to the Work and a feature of a model or
output, including where the Work is itself a model?
(h2) *(added 2026-11-24, from a counterexample by portfolio-5e)* §8.4 says the limit is *"a question of causation and not of quantity"*. Where causation is tested by asking whether the result would have occurred without the cause, a Dedicator could argue that a feature of a model, produced both by the Work and, sufficiently, by other training data, would have arisen without the Work and so does not *"result … from the content of the Work"*. That would bring back, case by case, the question *"would this have happened without the Work?"* that ACD-1.1 to 1.3 asked in words. We read *"in whole or in part"* as making a partial contribution enough, and the words *"a feature that the Work teaches or embodies is taken so to result"* as shutting the question out for a feature the Work teaches or embodies; what remains is a feature the Work neither teaches nor embodies but contributed to, where other data would also have produced it. Is that how a court applying a but-for test would read the clause, and does any jurisdiction treat a contribution "in part" differently?
(i) §8.1 reaches claims *"owned or controlled by the Dedicator"*, and §8.5 defines *controlled* as the
Dedicator's own right to license. A claim held by the Dedicator's affiliate is not reached. Apache-2.0
reaches it, because its *"Legal Entity"* includes entities under common control; UPL-1.0, BlueOak-1.0.0
and BSD-2-Clause-Patent do not. We left ACD on the narrower side, because a Dedication cannot bind a
company that has not applied it (§2.7), and a claim transferred to an affiliate after application is
bound by §2.8. Is the remaining gap (a claim the affiliate already holds) a defect a reviewer would
press, and if so, is a covenant by the Dedicator not to cause an affiliate to assert it effective?

**A Japanese decision on the gap §8.6 fills (added 2026-11-20).** The IP High Court (4 October 2023,
Reiwa 3 (ne) 10061, patent licence) held that a licensor could assert its patent against products a third
party made with machines the licensee had sold, because the licence had no non-assertion clause:
*「不起訴の合意に関する条項もないから、」* and *「本件の特許権を行使してはならないとの義務を負うと解することはできない。」*
(the court's own summary, not the full judgment;
`rounds/2026-11-19-jp-ip-high-court-2023-10-04-r3-ne-10061-non-assert-snapshot.txt`). ACD has what that
licence lacked: a covenant not to assert (§8.6) and a grant that names no counterparty (§1.6, §2.3). The court
did not hold that such a covenant would have worked, and whether a person who is not party to it can rely on
it in Japan (civil code article 537, the beneficiary's declaration) is the fourth question under question 5.

**An answer would change** the wording of §8.4 (register B7; errata E6 and E15).

## 3. Are the moral-rights covenants enforceable where waiver is not? (§12.1 to §12.5)

**The clauses.** §12.1 waives Moral Rights to the extent the law permits. In ACD-1.3 §12.2 replaces the
waiver, where moral rights are inalienable, with a covenant not to exercise them against You. ACD-1.4
adds, in a sentence of its own, the Dedicator's consent to the acts the rights would otherwise forbid ((e)
below), and since trial T101 gives the covenant and the consent *"for every jurisdiction, whether or not
Section 12.1 has effect there"*, with no trigger. §12.3 limits the covenant to the Work. §12.4 binds successors and *"any person entitled to exercise or enforce
Moral Rights in the Work after the Dedicator's death"*. §12.5 keeps false attribution outside the
covenant.

**Meant to do.** Remove the integrity right as an obstacle to modifying the Work, in the form that
Japanese practice already uses (a covenant not to exercise rights that Article 59 of the Copyright
Act makes inalienable), without reaching other works. The treaty floor is narrower than §12: Berne
Article 6bis(1) gives the right *"to claim authorship of the work and to object to any distortion,"*
*"mutilation or other modification of, or other derogatory action in relation to, the said work,"* only
where it *"would be prejudicial to his honor or reputation"* (`rounds/2026-11-20-patent-usc-patg-berne-trips-snapshot.txt`); several
national laws reach further, which is why §12 does not rest on the treaty's limit.

**Why we doubt it.** (a) Whether a covenant given to the public at large, rather than to a known
counterparty, is enforceable in Japan, Germany or France. For Germany, Till Kreutzer wrote of CC0 that
broad waivers of moral rights are invalid in the prevailing opinion, but *"The effect, however, is not
that the license itself is void."*; the author could still, for example, *"prohibit distortions of his
work"* (`rounds/2026-11-16-kreutzer-cc0-german-law-analysis-snapshot.txt`). On that view what fails is the reach of §12, not
the licence, and the part that stays with the author is the core against distortion (UrhG section 14).
(b) Whether §12.4 can bind persons who,
after the author's death, act in their own right (Japan, Articles 60 and 116). (c) Whether a court
would treat a covenant this broad as contrary to public order even though §12.3 confines it. A second
point under (c): in ACD-1.3, and in ACD-1.4 before trial T103, §12.3 ended by saying that the covenant and the consent
*"are given in respect of a work that the Dedicator has chosen to place in the commons for the purpose
stated in Section 6"*. That clause
was kept to support the covenant's validity; since ACD-1.4 added a consent (T67), it also reaches
the consent. A blanket consent given in advance may be read narrowly by the purpose it states (that is our
reading, not one we have confirmed for any jurisdiction). Does the clause confine the consent to acts that
serve §6's purpose, being learned from, so that an ordinary modification unrelated to learning falls outside
it? If it does, would removing the clause weaken the covenant it was meant to support? **ACD-1.4
narrows this part (trial T103).** §12.3 now reads *"they are given in respect of the Work, which the
Dedicator has chosen to place in the commons for the purpose stated in Section 6"*: the purpose is set
in a non-restrictive clause about why the Dedicator placed the Work, not about which acts the consent
covers, so the reading that confines the consent to acts serving §6 is weaker. Whether a court in a
jurisdiction that reads advance consents narrowly would still use the purpose that way is the open part.
(d) Whether any jurisdiction treats Moral Rights as transferable yet requires a formality, such as
a signed writing, for a waiver. There §12.2's covenant would not operate, since its trigger is that
the rights are personal, inalienable, or incapable of waiver, while §12.1's waiver, given without a
signature, may fail for want of form. The United States (17 U.S.C. §106A(e)(1)) and the United
Kingdom (CDPA s.94) make the rights non-transferable, so §12.2 applies there; we know of no
jurisdiction in the gap, which is why the text was not changed (2026-11-01).
ACD-1.4 (trial T101, 2026-11-19) now gives §12.2's covenant and consent *"for every
jurisdiction, whether or not Section 12.1 has effect there"*, so the gap no longer arises in
ACD-1.4; the question stands for 1.0 to 1.3.
(e) **Consent as well as a covenant.** Where moral rights cannot be waived, does a blanket advance
consent in the licence text to acts that would otherwise infringe them (modification, omission of
the author's name) operate separately from a covenant not to exercise them? In Japan the integrity
right is infringed by alteration "against the author's will" (Article 20(1)), which reads as if
consent removes the infringement rather than the remedy; the United Kingdom provides that the rights
are not infringed by an act to which the person entitled has consented (CDPA s.87(1)). A waiver there
must be an instrument in writing signed by the person giving up the right (s.87(2)), which a published
dedication is not, but s.87(4) keeps *"the general law of contract or estoppel"* for *"an informal
waiver"* (`rounds/2026-11-16-cdpa-1988-s87-s90-legislation-gov-uk-snapshot.txt`), so §12.1 and §12.2 rest
in the United Kingdom on consent, contract or estoppel rather than on a statutory waiver. If that is
right, consent reaches what a covenant may not: persons who are not party to the covenant, and the
protection after death (Japan, Article 60). If it is wrong, or if courts refuse a consent given in
advance to unspecified acts (and Article 113(11), on acts prejudicial to honour or reputation, is
not a right that consent obviously reaches), does adding consent words do harm, for instance by
inviting the reading that the covenant alone was not meant to suffice? ACD-1.4 adds such a consent
(`ACD-1.4-THIRD-CLARITY-TRIAL.md` §15.1, T67); the reading above is ours, not a list participant's.

**An answer would change** §12.2 and §12.4, the clauses on which the dossier most wants correction
(`jurisdictions.md` §10), and whether §12.3 keeps its last clause (the second point under (c)).

## 4. Does a contribution fall under the Dedication by default? (§2.6, §1.9)

**The clause.** *"A Contribution is submitted under this Dedication, and the person making it
becomes a Dedicator as to that Contribution, unless they state otherwise at the time of
submission."* A Contribution is material *"intentionally"* submitted for inclusion.

**Why we doubt it.** A surrender or waiver of copyright usually needs clear evidence of intent;
an intent to contribute is not obviously an intent to surrender. Inbound-equals-outbound works
for licences such as Apache-2.0 (§5), but a public-domain surrender may need more than a default.

A second question runs the other way. *"Unless they state otherwise"* names no addressee, so a
contributor can opt out by telling someone who is not a Dedicator. No Dedicator then knows, and the
undertaking in §2.6 to identify such material does not bite. We considered requiring the statement
to be made *"in the submission or to the Dedicator to whom it is submitted"* and did not adopt it
(`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.27, T53): it would treat an express refusal as ineffective
because it reached the wrong person, and we do not know whether a court would do that.

A third question is about form. Lawrence Rosen wrote in 2005, of a licence that took an assignment of
copyright from contributors, *"Nobody should rely on an unsigned copyright assignment, especially one
that's buried in an unsigned open source license."* (`review-readings-4.md` §1.353). §2.6 makes a
contributor a Dedicator without a signature, and §3 surrenders rights without one. Under 17 U.S.C.
section 204(a) a transfer of copyright ownership needs a signed writing; a non-exclusive licence does not.
Is a surrender under §3, or a contributor's dedication under §2.6, a "transfer" for that purpose, or for
the equivalent rule in other jurisdictions? Our reading is that a surrender transfers nothing to anyone
and that §4 in any case needs no writing, but Rosen's remark was about a transfer to a project, which
ACD does not take, and we have not found a case on an unsigned surrender.

A fourth question is what a notice does when the person who carries it did not mean to apply it. §16.2 of
1.0 to 1.3 says that where a work *"is accompanied by the identifier"* the terms apply in full; ACD-1.4
speaks of *"A notice a Dedicator places"*, but a Dedicator is a person *"applying this Dedication"*. A
distributor that keeps a file's tag, a notices file, and a software bill of materials all carry the
identifier next to other material (errata E90). Would a court find that such a person surrendered rights or
licensed patents, or would the law on declarations of intent, mistake, or agency answer it before the
text does? The converse matters as much: if carrying a notice never applies it, can a recipient rely on a tag?

**An answer would change** whether §2.6 should require an affirmative statement, at a cost to
projects that accept contributions informally, whether the opt-out needs an addressee, whether adopters
should be told to keep a signed statement from contributors, and whether the rule on notices needs words
about intention.

## 5. How far does the covenant against "any claim or cause of action" reach? (§5.1, §5.2(d), §11)

**The clause.** In ACD-1.3 §5.1 covenants not to assert *"any claim or cause of action, whether now
known or unknown, arising from or relating to a use of the Work that this Dedication permits"*.
ACD-1.4 reads *"any claim or cause of action, whether now known or unknown, that treats as
wrongful, or as without legal basis, a use of the Work that this Dedication permits or purports to
permit, other than for patent infringement (Section 8), under trademark rights or rights in a name
(Section 11.1), for a false statement or representation (Section 11.3), or for a payment You agreed
to make for providing a copy or for a service that is not permission to use the Work"*. §5.2(d) carries
only one of those exceptions, the one for a false statement or representation (Section 11.3). §11.1
grants no trademark right; §11.3 places misrepresentation of authorship or endorsement outside the
Dedication's reach; §11.4 states that the §5 covenants are not limited by its own sentence on reach.

**Our reading.** Until 2026-11-16 ACD-1.4 said *"for a use"*, and trial T90 put this reading into
the words. The covenant keeps the claims that attack the use itself: those that treat it as wrongful,
such as unfair competition, and those that treat it as without legal basis, such as unjust enrichment
(German civil code section 812, Japan's civil code article 703). It leaves out a claim that only
accompanies a use, such as an injury
caused by a machine You run. A claim against selling a trained model stays in, because §1.7 makes
that sale a Computational Use and so a use of the Work.

**Why we doubt it.** In 1.3 we read trademark claims as surviving because the conduct is the
misrepresentation §11.3 excludes (`ACD-1.3-CHANGELIST.md`). That reading does not hold on the
words: §5.2(d) uses the same *"use of the Work that this Dedication permits"* for rights §11.4 does
not grant, and a fork that keeps the name and logo need not represent anything. A Dedicator with a
mark could then be said to have licensed it without control, so ACD-1.4 says it in words.
The words now draw the line we describe; how a court reads *"treats as wrongful, or as without legal
basis"*, which no approved licence uses, we have not tested. The exception does not name data
protection, because §5.2(d) was written to stop a Dedicator's own personal rights from defeating a
permitted use (errata E31).

ACD-1.4 also excepts a payment You agreed to make (2026-11-07; since trial T118, a payment *"for
providing a copy or for a service that is not permission to use the Work"*, and §5.2(b) carries the same
exception, so that calling a permission a service does not bring a fee for it inside the exception) and
patent
infringement (2026-11-06): in 1.2 and 1.3 the words can be read to bar a patent claim that §8.4 does not
license, because the use is permitted as to the Covered Rights.

A second question sits between §10.2 and §11.3. §10.2 says You need not *"state that the Work was
modified"*; §11.3 keeps outside the Dedication *"Representing that the Dedicator authored, endorsed,
approved, sponsored, or is associated with a work, when that is not the case"*. A person who alters a
file and leaves the Dedicator's original authorship line in it, without saying it was altered, may be
read as representing that the Dedicator authored the altered file. On one reading the Dedicator did
write it, in part, so nothing false is represented; on the other the altered whole is not what the
Dedicator wrote. We did not widen §11.3 to name an altered work presented as unaltered, because that
would turn §10.2 into a condition in practice (`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.18, T41). Which
reading a court would take, and whether an author's claim for this survives in a jurisdiction where
§12.2 applies (§12.5 keeps false attribution outside the covenant), we cannot say. **ACD-1.4
answers the first part (trial T123).** §11.3 now adds *"Retaining a notice that accompanied or was
contained in the Work is not such a representation."*, so leaving the original authorship line in an
altered file is not within §11.3, and since trial T122 §12.5 keeps only §11.3 conduct outside the waiver,
the covenant and the consent. A new statement that the altered file is the unaltered original is not
retaining and stays within §11.3. Whether a court applying a statute such as the United Kingdom's CDPA
section 84 reads retention the same way is the open part.

A third question sits at the end of §5.2. ACD-1.4 says *"Section 5 does not reach the Dedicator's
rights in material, other than the Work, that the Dedicator itself makes or makes available, or the
terms or measures the Dedicator applies to that material"*. Suppose a Dedicator ships the Work only inside its own
installer, under a click-through and a licence key that forbid extracting the bundled components. We
read the copy inside the installer as still the Work (§2.1: *"every separable part of it"*), so the terms
stay inside §5.2(b), and the key stays inside §5.2(a) as far as asserting rights in respect of it goes
(since T64 ACD-1.4 no longer forbids applying a measure, only asserting rights in respect of one
or invoking the law of circumvention against You). If a court treated the installer as one
piece of "other material", the exclusion would reach terms that in fact restrict the Work
(`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.26). **ACD-1.4 closes this part (trial T91).** §5.2 now ends
*"A copy of the Work, or of part of it, contained in that material remains the Work, or that part of
it."*, so the installer's terms cannot
reach the bundled copy through the exclusion. The cost is that a Dedicator who ships the Work inside
its own product must keep the product's terms off that copy.

The fourth question is who may rely on these covenants. §5.3 says they *"may be relied upon by You
and by anyone who receives the Work from You, directly or indirectly, as an intended beneficiary, to the
extent a jurisdiction gives effect to such reliance"*, and ACD-1.4 extends that sentence to the
patent covenant of §8.6 (T66). Approved licences use third-party-beneficiary language the other way
round, to let someone enforce the licence against the licensee (CAL-1.0, NOSA 1.3), and a reviewer has
asked whether *"there can be oblivious third party beneficiaries (under contract law!)"* (Lawrence Rosen,
2014). ACD's recipients need not know of the Dedication (§2.3). Can a person who never saw the text rely
on a promise made to the public as an intended beneficiary, in the United States and in a civil-law
jurisdiction, and does it matter that the promise is a covenant not to sue rather than a duty to perform
(`ACD-1.0.against.md` #327)? Pamela Chestek, signing from her law practice in 2024, put the
ordinary rule this way: *"Only the licensor can enforce the contract (unless the license has a third party
beneficiary, in which case the third party can enforce it only insofar as that party's interest is
impacted)."* If that rule applies, a recipient could hold the Dedicator to §5 only as to the recipient's own
use, which is all §5.3 asks for; whether it applies to a promise that is not part of a contract is the question.
For the patent covenant there may be a shorter route. In the 2023 IP High Court case under question 2, the
court looked for, and did not find, a term that the licensor's right against the licensee's buyers was
barred: *「一審原告が機械を製造し、これを第三者に販売した場合に、一審原告に付与した独占的通常実施権に起因して、」*
*「その第三者に対する一審被告による本件特許権の行使が妨げられる旨の定めは何ら存せず」*
(`rounds/2026-11-19-jp-ip-high-court-2023-10-04-full-text-third-party-term-snapshot.txt`; the judgment does
not mention civil code article 537). In ACD a buyer is not a third party to §8.6: the covenant runs to *You*,
and §1.6 makes You anyone who exercises a permission granted here, so a buyer who uses or sells the product is
itself a promisee. That is our reading; the court decided a case with no such term. If it holds, the
beneficiary route of article 537 is not needed for §8.6, and the question narrows to recipients who exercise
no permission at all.

The fifth question is about the second limb of §5.2(a). The Dedicator covenants not to *"invoke
against You any law concerning the circumvention of such measures"*, where the measures are those
that restrict access to or use of the Work. The limb was written against DRM, that is, against the
anti-circumvention rules of copyright law (17 U.S.C. §1201, Article 6 of Directive 2001/29/EC and
their national forms). Since T64 ACD-1.4 lets the Dedicator apply a measure, such as a
proof-of-work challenge, a rate limit or an authentication step on its own download server. Does
*"any law concerning the circumvention"* also make the Dedicator give up computer-misuse law (the
Computer Fraud and Abuse Act, Japan's Act on the Prohibition of Unauthorized Computer Access) against
a person who defeats that measure to take copies? If it does, are there words that leave the
Dedicator the law that protects its computers without returning to it any law that protects the
measure as a restriction on the Work? A trial that limited the limb to laws protecting measures *"as
a means of protecting rights in the Work"* (T68) was not taken: it would also have returned unfair-
competition protection of technological measures (Japan's Unfair Competition Prevention Act) to the
Dedicator, and would have left the limb empty where the surrender in §3 takes effect. The answer
cuts both ways. If the limb does not reach computer-misuse law, a Dedicator may put a bot challenge in
front of its server and use that law against a crawler that defeats it; the purpose of §6 (a work
meant to be learned from) is then kept only if copies remain obtainable by other means, and the text
does not require that they do. Trial T124 sharpens the line without answering it: §5.2 now also says
that the Dedicator *"authorises the circumvention of any technological measure that is applied at any time
by or on behalf of the Dedicator to a copy of the Work"* in a permitted use, and waives any power under a law
concerning such circumvention to forbid it. A measure on the Dedicator's own server is not applied to a copy,
so neither the authorisation nor the waiver reaches it, and the question above stays where it was for those
measures; for a measure applied to a copy, the authorisation is the Dedicator's own act and does not depend on
how a court reads *"any law concerning the circumvention"*.

A sixth question was what *"a use of the Work that this Dedication permits"* means where the permission
fails. In a jurisdiction where §4 does not take effect, is the use still one the Dedication permits, so
that §5.1 still bars the claim, or only one the text says it permits? We read §15.1, which asks for the
reading that gives *"the widest permission and the least obligation upon You"*, as choosing the first,
so that the covenant stands on its own footing, as §2.4 says. If a court takes the second, §5.1
falls with §4 in exactly the place it is meant to hold (`ACD-1.4-THIRD-CLARITY-TRIAL.md` §15.27, from
portfolio-30). **ACD-1.4 answers it (trial T93):** §5.1 and §5.2(d) now say *"a use of the Work
that this Dedication permits or purports to permit"*, so the covenant holds where §4 does not take
effect.

A seventh question is where the covenant stops when the harm is not the use of rights but what was done
with a tool. Suppose a Dedicator releases a network scanner under ACD-1.4 and someone uses it to break into
the Dedicator's own server. §4.1 permits use *"for any purpose whatsoever"*, so the use is one *"that this
Dedication permits or purports to permit"*, and a claim for the break-in treats that use as wrongful. None of
the four exceptions fits. Our reading above leaves out a claim that only accompanies a use; on the words, the
break-in is the use. Germany does not let liability for intent be excluded in advance (civil code section
276(3)), and other laws have similar rules, so the covenant may fail there; does it fail only for the
deliberate act, or does a court read the whole limb down? The same point touches §5.2(d): if the Work is an
image generator, a false image of the Dedicator made with it is a *"use of the Work"*, and §5.2(d) is not
tied to a likeness the Work contains, as CC0's waiver is (*"depicted in a Work"*). Both are recorded as
defects of 1.2 to 1.4 (`ACD-1.1-SELF-AUDIT.md` §3zf and §3zh, in Japanese); the 1.5 draft limits both to
a claim made by reason of the use being a use, or of what the Work contains (Section 2.5(d) of the draft). It is not fixed.

**An answer would change** whether §5.1's *"treats as wrongful, or as without legal basis"* is the right wording,
and whether data protection needs its own exception. An answer to the seventh would change whether adopters who
release security or generative tools under ACD-1.4 should be told to wait for a later version. An answer to the second question would change whether §11.3 needs the altered-work case in words.
The third is settled in ACD-1.4 by T91. The sixth is settled in ACD-1.4 by T93. An answer to the fourth would change whether §5.3 should keep the words *intended beneficiary*, and whether T66 should have extended them to §8.6. An answer to the fifth would change whether the second limb of §5.2(a) needs a carve-out for computer-misuse law.

## 6. Do the text-and-data-mining declarations do anything? (§6.2, §6.3)

**The clauses.** §6.2: the Dedicator *"makes no Reservation … and expressly declines to make
one"*, and no signal associated with the Work is to be read as a Reservation *"so far as the
Covered Rights and patent claims of the Dedicator are concerned"*. §6.3: the Dedicator withdraws
any Reservation *"to the fullest extent the Dedicator is able"*, and disclaims reliance on any.

**Why we doubt it.** Under Article 4(3) of Directive (EU) 2019/790 a reservation is the
rightsholder's statutory act. Whether a rightsholder can bind itself in advance never to make one,
and whether a reservation placed by a host or platform (not a rightsholder) has any effect for the
purpose of the exception, are questions on which a German appellate court has ruled in a case
about the same exception (HansOLG 5 U 104/24; `jurisdictions-sources.md` §9a(9)) — we have read the
court's own announcement, not the judgment.

ACD-1.4 adds a rule on the Dedicator's own notices (§16.2, 2026-11-10): *"a notice that is
only a Reservation assigns nothing to other terms (Section 6.2)"*. It is meant to stop an opt-out
notice the Dedicator places from taking that material out of the Work. If a court treats such a
notice as the Dedicator's statutory reservation all the same, §16.2 and the statute point different
ways for that material, and §6.3's withdrawal is what has to carry it.

A second question runs underneath §6 as a whole. Under German law a grant of rights whose kinds of use
are not expressly named is read by the purpose of the contract (UrhG section 31(5): *„so bestimmt sich nach dem
von beiden Partnern zugrunde gelegten Vertragszweck, auf welche Nutzungsarten es sich erstreckt."*, `rounds/2026-11-16-urhg-31-5-gesetze-im-internet-snapshot.txt`).
§4.2 and §6 name the uses expressly, and §6.5 now gives as its reason that silence *"leaves it to be inferred
whether this is permitted"*. Does section 31(5) apply to a unilateral grant to the public, where there is no
counterparty whose purpose can be read? If it does, is the purpose the Work's stated one (the preamble's
*"works that are meant to be learned from"* and §6), and does the express list in §4.2 and §6 take the grant outside
the rule altogether?

**What the law already settles in the European Union (added 2026-11-16).** The reservation in Article
4(3) of Directive (EU) 2019/790 is a condition of the exception in Article 4(1), not of a licence, and
recital 18 says *"Rightholders should remain able to license"* the uses that fall outside the exception
(`rounds/2026-11-16-eu-tdm-and-conflict-of-laws-snapshot.txt`, read through a fetch tool). Our reading:
a reservation closes the exception route only, so where §4 and §6.1 operate as a licence they do not
depend on whether a Reservation exists, and the question narrows to the case where a recipient relies on
the exception alone, for example where the licence is held ineffective.

**An answer would change** whether §6.2 and §6.3 can stay as statements of the Dedicator's own
position, and whether the §16.2 rule does what it is meant to do or should be dropped; an answer to the second
would say whether §6 is needed in Germany or only stated.

## 7. What follows from naming no governing law and no forum? (§15.3)

**The clause.** In ACD-1.3: *"This Dedication specifies no governing law and no forum. It is intended to
operate under the law of each jurisdiction in which the Work is used, according to that law."* ACD-1.4
(trial T92) keeps only the first sentence: *"This Dedication specifies no governing law and no
forum."*

**Why we doubt it.** OSI's board, approving another licence, said *"it does not believe that
choice of law provisions are necessary or advisable in open source licenses"* (`against.md`
#254), which supports the omission; but a recipient sued abroad has no clause to point to, and
the dossier records that as a cost: #23 is answered only in part, and #170 lists national rules a
forum could apply against several clauses.

The board's sentence is not alone. In the December 2022 thread on choice of law, Carlo Piana wrote *"I
strongly invite drafters NOT to include choice-of-law provisions in their licenses."*, noting *"Another
notable license dropping it for good is Creative Commons (v3 -> v4)"*, and Mike Milinkovich, steward of
the EPL, recalled lawyers who *"found the EPL-1.0 USA-centric because of its choice of law provision"*
and avoided it (`rounds/2022-04-license-review-open-logistics-license-observed-10of15.txt` and `-12of15.txt`,
the second as Lawrence Rosen quoted it). Rosen answered by asking whether omitting the clause sends the
licence to the licensee's law at all. In the European Union the paragraph below answers in two parts:
infringement follows the country for which protection is claimed, and the contract side, if any, the
Dedicator's.

**What the law already settles in the European Union (added 2026-11-16).** For infringement, the law is
that of the country for which protection is claimed: Rome II, Article 8(1), *"shall be the law of the
country for which protection is claimed"*, and Article 8(3), *"may not be derogated from by an
agreement pursuant to Article 14"*. Naming no governing law therefore gives up nothing on the
infringement side. On the contract side, if the Dedication is a contract at all, Rome I, Article 4(2)
points to the law of the country *"where the party required to effect the characteristic performance of
the contract has his habitual residence"*; for a grant, that is the Dedicator
(`rounds/2026-11-16-eu-tdm-and-conflict-of-laws-snapshot.txt`). Whether it is a contract is not settled by
these texts. Outside the European Union the same rule for protection comes from the Berne Convention,
Article 5(2): *"the extent of protection, as well as the means of redress afforded to the author to
protect his rights, shall be governed exclusively by the laws of the country where protection is
claimed."* (`rounds/2026-11-20-patent-usc-patg-berne-trips-snapshot.txt`).

**ACD-1.4 answers the first part (trial T92).** #23 read the second sentence as a declaration
about conflict of laws that a forum need not follow, and the law above shows it did no work on the
infringement side, so ACD-1.4 removed it. One consequence follows: that sentence was the only words
that could be read as an implied choice of each place of use, so without it, on the contract side,
Rome I Article 4(2) points to the Dedicator's habitual residence. Is that a cost to a recipient sued
abroad, or does it make the contract side easier to predict?

**The phrase "the law" in other clauses (added 2026-11-23).** Five places limit an effect *"to the fullest
extent the law permits"* (§2.8, the paragraph of §5.2 after (d), §5.3, §6.4, §12.4); two say *"permitted by the law of each
jurisdiction"* (§3.1, §12.1); §14 speaks of *"applicable law"*. With no governing law named, we read "the law" in the five as
the law of whichever jurisdiction is applied, which is what the other two forms say. Could a court read it instead as one law,
for example the Dedicator's by Rome I Article 4(2) on the contract side? A reviewer has warned that wording one idea two ways
*"invites challengers to find some distinction between the two"* (Pamela Chestek, `license-review` 2022-07-04).

**An answer would change** whether the dossier should tell adopters that the contract side may follow
the Dedicator's law. It would also change whether the five clauses should say *"the law of each jurisdiction"*, as §3.1 and §12.1 do. Whether §15.3 keeps its second sentence is settled in ACD-1.4 by T92.

## 8. Does the Dedication survive the Dedicator's insolvency? (§2.9)

**The clause.** Nothing in the Dedication is conditioned on, suspended by, or revived by an
insolvency proceeding, and an insolvency officer is a transferee bound under §2.8. What the officer
is bound to differs by version: in ACD-1.3, §2.8 binds Sections 3, 4, 6 and 8, so the covenants in
§5 reach transferees only through §5.3's narrower list, and §7.2 and §2.5 are left out (errata E46,
E49). ACD-1.4 binds the whole Dedication as it concerns the Work and states that §5.3 and
§12.4 do not narrow §2.8 (2026-11-02).

**Why we doubt it.** Whether a trustee can reject the licence as an executory contract is for the
forum's insolvency law, and *Jaffé v. Samsung* (4th Cir. 2013) shows that protection under
11 U.S.C. §365(n) can turn on a balancing in a cross-border case. The text no longer asserts the
result (errata E5, E30); whether its structure — no obligation on the licensee — keeps it outside
"executory" is what we cannot judge.

**What the law already settles in the United States (added 2026-11-16).** The Supreme Court held in
*Mission Product Holdings v. Tempnology* (2019) that *"Rejection of a contract—any contract—in bankruptcy
operates not as a rescission but as a breach"*, that *"Such an act cannot rescind rights that the
contract previously granted"*, and that *"the counterparty retains the rights it has received under
the agreement"*; the opinion uses the definition that a contract is executory if *"performance remains
due to some extent on both sides"* (`rounds/2026-11-16-us-bankruptcy-tempnology-and-365n-snapshot.txt`,
read through a fetch tool and not a byte copy). So in the United States the question narrows to two
steps: whether a licence that puts no obligation on the licensee is executory at all (our reading is
that it is not; the Court did not decide a case like this), and, if it is, rejection still leaves the
rights already granted, without relying on §365(n). The same reasoning reaches the covenants if they
are "any contract", which narrows the second question below to jurisdictions other than the United
States. What remains open is the law of those jurisdictions (Germany is being read under §103 of the
Insolvency Code) and the cross-border balancing of *Jaffé v. Samsung*.

**An answer would change** whether §2.9 needs more than ACD-1.4 gives it, and how the dossier
answers #178 (`jurisdictions-sources.md` §9a (10), on Qimonda).
In *Jaffé v. Samsung* the result took a four-day evidentiary hearing and a discretionary
balancing (#178). The opinion says so in terms: *"relying on the particular facts of this case and the
extensive record developed during the four- day evidentiary hearing, we also conclude that the bankruptcy
court reasonably exercised its discretion in balancing the interests of the licensees against the interests
of the debtor"*; it held that §1506's public-policy exception does not foreclose that balancing under §1522,
and it noted that §103 of the German Insolvency Code, unlike §365, *"does not specifically address
intellectual property licenses"* (`rounds/2026-11-19-us-jaffe-v-samsung-4th-cir-2013-snapshot.txt`, text extracted from the court's PDF; the
case was about patent licences under Chapter 15 and was decided before *Tempnology*). The protection §365(n) gives reaches the licence of copyright as well as of patents: 11 U.S.C. §101(35A) defines *"intellectual property"* to include *"(E) work of authorship protected under title 17"* and *"(B) invention, process, design, or plant protected under title 35"*, and not trademarks (`rounds/2026-11-19-us-11-usc-101-35a-intellectual-property-snapshot.txt`). So the core of the question is whether §2.9's statement that nothing in the
Dedication is *"suspended by, or revived by"* such a proceeding or an officer's act would be read
the same way under another jurisdiction's insolvency law.

A second question is about the covenants. §365(n) protects a licensee; ACD's §5 covenants (and the
patent covenant of §8.6) are promises not to sue, not licences. A drafting precedent exists for
exactly this gap: the Open Web Foundation Agreement 1.0, drafted by lawyers, says in 3.1.4
*"Solely for purposes of Section 365(n) of Title 11, United States Bankruptcy Code and any
equivalent law in any foreign jurisdiction, this promise will be treated as if it were a license"*
(quoted by Lawrence Rosen on `license-discuss`, 2013-08-18). If a covenant might fall outside
§365(n)-type protection where a licence would not, would a sentence of that kind in §2.9 help? And
would it harm, by appearing to decide a legal classification that the text otherwise leaves to the
law (the same objection that led us to remove sentences asserting legal results, errata E23 and
E79)? ACD-1.4 does not add such a sentence, for that second reason
(`ACD-1.4-THIRD-CLARITY-TRIAL.md` §15.2).
For patents in the United States the gap narrows: the Federal Circuit held that *"a non-exclusive
patent license is equivalent to a covenant not to sue"* (*TransCore v. Electronic Transaction
Consultants*, 2009; `rounds/2026-11-16-us-transcore-covenant-equals-license-snapshot.txt`), so the patent
covenant of §8.6 and the licences of §8.1 and §8.4 should fare alike there, and after *Tempnology* (above)
rejection leaves either in place. The case is about patent exhaustion; whether the same line reaches the
copyright covenants of §5 we have not found.

A third question is German. German insolvency law gives the administrator two tools. The election not to
perform (InsO section 103) is limited to a mutual contract (*"Ist ein gegenseitiger Vertrag"*), and ACD asks
nothing of the recipient, so we read it as not reaching the Dedication. The other tool is avoidance of a
gratuitous performance: *"Anfechtbar ist eine unentgeltliche Leistung des Schuldners, es sei denn, sie ist
früher als vier Jahre"* *"vor dem Antrag auf Eröffnung des Insolvenzverfahrens vorgenommen worden."*
(section 134(1)). Avoidance requires prejudice to creditors (section 129(1)), and a recipient in good faith
returns only what still enriches it (section 143(2)). Is applying ACD a gratuitous performance that an
administrator can avoid if the Dedicator becomes insolvent within four years? If so, does avoidance reach the
permissions of recipients who already hold copies, or only future use? §2.9 cannot prevent this, because the
statute gives the administrator the power (`jurisdictions.md` §3; the statutory text is in
`rounds/2026-11-16-inso-103-129-134-143-gesetze-im-internet-snapshot.txt`).

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

**ACD-1.4 answers this part (trials T83 and T88).** §14.2 now ends *"Section 14 does not limit the
Dedicator's liability for asserting a claim, or exercising a right, in breach of a covenant in Section 2.5,
5, 8.6, or 12.2"*. A recipient put to the cost of a suit the Dedicator promised not to bring keeps the
claim for it. A breach that consists only of imposing terms (§5.2(b)) is outside that sentence until the
Dedicator sues on them. What stays open for counsel is (b) below and the questions about the T82 exception.

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

A second question is whether §14 survives at all where a court will not cut a limitation down to what
the law allows. Pamela Chestek wrote in 2023 of clauses of this form that *"the clause isn't effective in
the same way in some countries and would instead be ignored altogether, leading to liability for
everything"*. §14.1 and §14.2 both rely on being cut down (*"TO THE FULLEST EXTENT PERMITTED"*, *"limited
to the greatest extent that law permits"*). In the same message she noted that *"in some countries there
are different standards of liability for gifts versus an exchange"*; German civil code section 521 limits a
donor's liability to intent and gross negligence. Is a dedication like this one standard terms whose
limitation falls away entirely, or a gift whose donor is liable only for intent and gross negligence, or
neither (`jurisdictions.md` §3)?

If it is a gift, the same characterisation brings a donor's revocation for gross ingratitude, which in
Germany cannot be waived in advance (German civil code sections 530 and 533). France allows revocation
only in the three cases of article 955 of its civil code (an attempt on the donor's life, serious
cruelty, offences or insults, or refusal of maintenance), and article 931 requires a gift to be made
before a notary on pain of nullity, so an un-notarised dedication is unlikely to be a gift there; whether
French law bars an advance waiver we have not checked. Our reading narrows it further: revocation would
reach only the recipient guilty of the ingratitude, not other recipients, and enforcing one's own patent
in court is not in itself a serious wrong (`jurisdictions.md` §3). In Japan, civil code article 550 lets
either party cancel a gift not made in writing, *"ただし、履行の終わった部分については、この限りでない。"*
(except for the part already performed;
`rounds/2026-11-16-minpo-chosakukenho-e-gov-api-snapshot.txt`); our reading is that a published text
applied to a Work is a writing and that a copy already received is a part performed, but we have not
read a case on a public licence. Article 550 does not say what form the writing takes, and we have not read
the cases that set the test (to whom the writing is addressed, how clearly it shows the intent to give).
Article 549 also makes a gift take effect when the other party accepts, so a grant to the public may not
be a gift at all, and then article 550 does not arise. On either reading, article 550 would not undo
what a recipient already holds; neither reading is settled. Is that reading right, and could revocation reach the patent licence
of §8? ACD-1.4 (T85) now says that the licences are not terminable *"under this Dedication"* on
any ground, so the text no longer speaks for what the law may allow.

ACD-1.4 (trials T82 and T102) now opens §14.1 with *"EXCEPT FOR ANY LIABILITY FOR WILFUL MISCONDUCT,
GROSS NEGLIGENCE, DEATH, OR PERSONAL INJURY, IN EACH CASE WHERE APPLICABLE LAW DOES NOT PERMIT IT TO BE
EXCLUDED, WHICH NOTHING IN SECTION 14 LIMITS,"*, following EUPL-1.2 §8. Our reading is that this keeps the exclusion standing in Germany
if the Dedication is standard terms, because the excepted categories match those that German civil code
section 309 no. 7 protects. Section 309 reaches only a recipient who is a consumer: section 310(1) says
that section 309 does not apply to standard terms *"die gegenüber einem Unternehmer, einer juristischen
Person des öffentlichen Rechts"* are used (`rounds/2026-11-16-bgb-305-310-gesetze-im-internet-snapshot.txt`),
so against a business recipient only section 307 applies. Two points we cannot settle. Does tying the exception to what "applicable law does
not permit" meet the transparency requirement of section 307(1), second sentence? And does EUPL's unconditional
form, which leaves the licensor liable for these categories even where the law would let them be excluded,
stand better, at the cost of more liability for adopters elsewhere? The texts we rely on are in
`rounds/2026-11-16-bgb-276-307-309-521-524-gesetze-im-internet-snapshot.txt`.

In the United Kingdom the question narrows. Sections 2 to 7 of the Unfair Contract Terms Act 1977 apply
*"only to business liability"* (section 1(3)), so a Dedicator who applies ACD outside a business is
not reached by them. Where a business applies it, section 2(1) forbids excluding liability *"for death or
personal injury resulting from negligence"*, which the T82 exception already leaves standing, and section
2(2) lets other negligence be excluded only *"in so far as the term or notice satisfies the requirement of
reasonableness"* (`rounds/2026-11-16-ucta-1977-s1-s2-legislation-gov-uk-snapshot.txt`). Whether §14.1 is
reasonable for a gratuitous grant is the open part.

In Japan the Consumer Contract Act reaches only a contract between a consumer and a business (Article
2(3)), so an individual who applies ACD outside a business is not reached by it either. Where a business
applies it, Article 8(3) adds a test of wording: a clause that partly excludes liability is void if it
does not make clear that it applies only to negligence other than gross negligence:
*「当該条項において事業者、その代表者又はその使用する者の重大な過失を除く過失による行為にのみ適用されることを明らかにしていないものは、無効とする。」*
(`rounds/2026-11-16-shohisha-keiyaku-ho-2-8-e-gov-api-snapshot.txt`). The T82 exception names wilful
misconduct and gross negligence, which reads as making that clear, but it excepts them only where
applicable law does not permit their exclusion. Does a conditional exception of that kind meet
Article 8(3), or must §14.1 except gross negligence without the condition, as EUPL-1.2 §8 does
(`jurisdictions.md`, the paragraph on §14.1 and the Consumer Contract Act)?

**An answer would change** the wording of the T82 exception, if it fails the German transparency requirement,
the United Kingdom's reasonableness test, or Article 8(3) of Japan's Consumer Contract Act. Whether §14 should say that it does not limit the covenants
is settled in ACD-1.4 by T83. An answer to (b) would change whether §14.1 needs its own subject.


## 10. Does the name or the short identifier collide with a mark in use? (§16.4, B6)

**The clause.** §16.4 ties the name *Autonomous Commons Dedication* and the identifier *ACD-*
followed by a version number to one fixed text, and restricts distributing a modified text under
either. The short form used everywhere, including in this repository's notices, is *ACD*.

**Why we doubt it.** We checked that SPDX has no identifier beginning *ACD-* (B6), but not whether
*ACD* is a registered or used mark. A software company, ACD Systems International Inc. (ACDSee),
uses it (`ACD-OSI-BOTTLENECKS.md` B6, 2026-11-16). On another submission a board member asked for
a new acronym before voting because the short name was also an organisation's name in the same
field: Josh Berkus, 2020-12-27, *"Were it otherwise acceptable I'd request a change of license
acronym before voting to approve it."* (`review-readings-2.md` §1.254). He spoke as a
non-lawyer, and that clash was in the same field; whether a mark held by a company outside open
source licensing matters is what we cannot judge.

**An answer would change** whether the identifier should change before the version to be submitted
is fixed. Changing it later costs every notice, the SPDX request and the documents; changing it
before the version is fixed costs only the draft and the dossier.

---

## How to answer

In any form, on a list or privately. **Public answers are recorded word for word** in
`LICENSES/rounds/`. **Private correspondence is not published**: only its date, its direction and a
pointer to where the analysis uses it are recorded (`rounds/README.md`). Correction of any reading
on this page is the most useful answer; agreement is the next most useful, because it moves B1.
Nothing here asks a reader to take on any obligation, and a short answer to one question is worth
more to us than a long one to all ten.
