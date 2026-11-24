---
file: LICENSES/ACD-1.0.submission-osd.md
audience: OSI license-review participants / licence reviewers / 監査人 / 次のセッションの実装者
last-updated: 2026-11-23
clause-numbers: ACD-1.4
reachable-via: ACD-1.0.submission-reference.md
canonical-ref: LICENSES/ACD-1.0.submission-reference.md (切り出し元・§1〜§2 / §4〜§5) / LICENSES/ACD-1.0.submission.md (送る文面は §B.0。**これを貼らない**)
---

# ACD-1.0 — 提出参考資料のうち OSD の節（§3 / §3b / §3c / §3d・**貼らない**）

**2026-11-23（5 人の合議・議題 3）: 提出対象を ACD-1.4 へ切り替えた。** 条の中身を現在形で述べる行（OSD 5・OSD 7 の項、表の §5.2・§12.2・§16.4、§3d の Work の定義）は ACD-1.4 の語と番号で書き直し、1.0 の番号が違う所は括弧で添えた。1.0 について書いた日付つきの訂正と記録は書き換えていない。1.4 で変わった条への OSD 1〜10 の当て直しは `ACD-1.4-THIRD-CLARITY-TRIAL.md` §15.52（立つもの 0）。

**`ACD-1.0.submission-reference.md` から 2026-09-25 に切り出した**（899 行で advisory 900 の 1 行手前に達したため・
予算表が事前に宣言していた分割計画どおり）。**節番号は動かしていない。** 切り出し元には各節の案内見出しを残してあるので、
既存の `submission-reference.md §3b` などの参照は案内を経てここへ着く。
**本文中の裸の `§4c` / `§2` などは、切り出し元（`submission-reference.md`）の節を指す。**

**なぜこの節だけか**: ここは「審査者が OSD の話をしに来たとき」という単一の用途で読まれ、
他の節（なぜ新しいライセンスが要るか・既存との差・開示）とは読み手が分かれる。

### 3. Open Source Definition conformance

**Stated first, because the archive says it should be.** Conformance with the Definition is the
floor of this process and not the whole of it. Russ Nelson, then president, put the reason on the
list in 2009: *"There are reasons beyond OSD conformance why we might not want to approve the
license. Why? Because we have a trademark to preserve. If you can figure out some way to comply
with the OSD in a way that does not achieve the desired open source effect ... then we MUST deny
your license OSI approval."* I am not offering the clause-by-clause analysis below as a
sufficient condition, and the question I take to be live is the one behind it: whether this
instrument achieves the effect, not merely the form. **My answer is that it has no conditions at
all (Section 10.1), so it has nowhere to put a discrepancy between form and effect** — the
evasions that provision guards against live inside conditions, and there are none here. That is
an argument, not a proof, and it is the part of this submission I would most like you to test.

ACD-1.0 imposes no conditions at all, so conformance is straightforward. Addressing the
criteria the committee asks submitters to speak to directly:

- **OSD 1 (Free redistribution).** Section 4.2 permits distribution and sale by any means;
  Section 4.3 attaches no condition, including no royalty.
- **OSD 2 (Source code).** The licence permits distribution in source form, object form,
  or any other form (4.2), and imposes no obstacle to providing source.
- **OSD 3 (Derived works).** Section 4.2 permits modification and derivative works;
  Section 4.3 forbids any reciprocal-licensing condition; and Section 4.5 states the
  consequence positively — the Work and any adaptation or collection containing it may be
  distributed under any terms the recipient chooses, **including terms incompatible with
  these**, with nothing reaching through to their recipients. A recipient may therefore
  place the Work inside a copyleft project without friction. **The criterion's second limb
  is met expressly as well**: OSD 3 requires that derived works be allowed *"to be distributed
  **under the same terms as the license of the original software**"*, and §16.3 permits anyone
  to apply this text to a work in which they hold rights — so a derivative may carry ACD-1.0
  itself. **Checked word for word against the source on 2026-09-13**; the earlier rendering
  answered the first limb only. Those who decide have read the second limb as a permission the licence must give, not a term it must
  impose: Russ Nelson, 2004-09-21, *"#3 says explicitly that a license has to allow redistribution under the same terms as the license of the original software."*;
  and Bruce Perens, 2022-09-19, that the OSD does not require a licence to permit *all* modifications
  (`ACD-1.0.review-readings-7.md` §1.477). In ACD-1.4, §16.3 reaches the parts in which the modifier holds
  rights, and §4.6 keeps the original parts under the original Dedication.
- **OSD 4 (Integrity of the author's source code).** No restriction is imposed. Section
  16.4 concerns the text of the licence *as a document*, not the licensed work; Sections
  10.5 and 16.6 state this expressly. *(Corrected 2026-11-01: this said "10.5 and 16.5"; in
  ACD-1.0 §16.5 is the translation rule and §16.6 is the clause that says §16.4 and §16.5 are not
  terms of the Work. In 1.1 and later the same clause is §16.6 as well.)*
- **OSD 5 (No discrimination against persons or groups).** §4.3 states the licence is not
  conditioned "on the identity, character, size, revenue, or purpose of the user, on the scale of use or the number of users served, or on any restriction as to
  persons, groups, technologies, endeavours, or jurisdictions." §2.3 adds that the grant takes
  effect without any act of acceptance, so there is no gate at which a person could be excluded.
- **OSD 6 (No discrimination against fields of endeavour).** The same sentence of §4.3 excludes
  conditioning "on field of use." §6 goes further in one direction only — it names machine
  learning and text-and-data-mining expressly in order to **permit** them, not to single them out
  for a condition.
- **OSD 7 (Distribution of licence).** Section 2.3 makes the licence effective without any
  act of acceptance, and Section 4.6 makes each person who exercises a permission You in
  their own right, so rights attach to every recipient without further action. Section 16.2
  makes an identifier or SPDX tag sufficient notice.
- **OSD 8 (Licence must not be specific to a product).** The Work is the material the Dedication
  was applied to, not a distribution (§1.2 in 1.0, §1.3 from 1.1). Section 2.1 applies it to the
  Work as a whole and to every separable part of it, and Section 4.6 makes each person who
  receives it You in their own right, so the rights do not depend on the Work staying in any
  particular distribution. Section 16.3 adds that the text itself is not specific to any project. *(Corrected 2026-11-06: this line cited only §16.3, which speaks of
  the instrument, not of the rights in a program.)*
- **OSD 9 (Licence must not restrict other software).** Sections 4.3 and 10.1 impose no
  requirement on anything distributed alongside the Work.
- **OSD 10 (Licence must be technology-neutral).** Section 2.3 requires no click-through
  or other individual act of assent; Section 5.2(b) forbids imposing one by collateral
  means.

### 3b. Where a reviewer could still argue, criterion by criterion

The list above says why each criterion is met. This one says where the meeting is arguable, so
that the two are read together rather than one being discovered after the other.

| Criterion | The argument against | Why it is nonetheless met |
|---|---|---|
| **OSD 1** Free redistribution | §4.5 lets You redistribute "under any terms You choose, including terms that impose conditions upon Your own recipients." A reviewer may ask whether an instrument that permits proprietary relicensing satisfies a criterion about free redistribution | It does, and this is settled: every permissive approved licence allows it. OSD 1 constrains what the **licence** may require, not what a redistributor may add |
| **OSD 2** Source code | The instrument never requires source to be available. §10.2 says You "need not ... make source available" | OSD 2 bars a licence from **obstructing** source distribution and requires the preferred form when a program is distributed under it; §4.2 grants distribution "in source form, in object form, or in any other form." Permissive licences are approved on this basis. That §4.2 names source matters: McCoy Smith, 2020-10-16, said of a short dedication that *"it doesn't anywhere discuss source code (which would seem to violate OSD 2)"* (`review-readings-7.md` §1.479); his next sentence, *"I'd say this is one that really needs a lawyer's involvement"*, is against us (B1). Lawrence Rosen, 2008-09-27, separated the two questions: a distributor who withholds source is not offering open source, whatever its licence says |
| **OSD 3** Derived works | — | §4.2 grants adaptation, modification and derivative works expressly, and §4.3 attaches no condition to them. The second limb (distribution *"under the same terms as the license of the original software"*) is met by §4.5 and §16.3 (§16.3 for the parts in which the modifier holds rights; §4.6 keeps the original parts under the original Dedication), as the paragraph above shows |
| **OSD 4** Integrity of the author's source code | §16.4 forbids distributing **the licence text** in modified form under the name or identifier. A reviewer skimming may read that as a restriction on the Work | It is not: §10.1 is limited to conditions "in respect of the Work," and §16.4 governs the licence text only. The provision is the same name-integrity term GPL and Apache-2.0 carry for their own texts. The looseness is in the notice wording, recorded as errata E3 |
| **OSD 5** Persons or groups | §11.3 places one thing outside the Dedication's reach — a false representation that the Dedicator authored, endorsed or is associated with a work | §11.3 says in terms that it "states a limit of the Dedication's reach; it is not a condition upon You, and Section 10.1 is unaffected by it." A false representation stays false whatever the Dedicator permits, and the limit falls on everyone alike, so it discriminates against no one. (Until 2026-11-16 this line said that misrepresentation was never the Dedicator's to permit. That is wrong for a false claim of authorship: in the United Kingdom the right not to have a work falsely attributed belongs to the person named (CDPA s.84) and is not infringed by an act that person has consented to (s.87(1)); trial T77, proposed the same day, drops the same reason from the 1.4 draft's §11.3.) **A wider reading of OSD 5 is live on the list**: on 2026-09-16 McCoy Smith argued that a termination trigger firing only on claims "against the Licensor" "puts Licensors & Licensees in different positions vis a vis patent assertions, and therefore arguably violates OSD 5". **This instrument has no trigger to point in either direction** — §10.4 states that no permission "terminates under it, for any reason" and that the Dedication "contains no termination provision and no revival provision", and §8.2 makes the patent licence non-terminable. **The wider reading is not established** (its author wrote "arguably" and the steward contested it), and we record our own exposure to it at `against.md` #179 |
| **OSD 6** Fields of endeavour | §6 names machine learning and TDM specifically. Naming a field at all can look like singling it out | The naming is entirely permissive: §6 grants and disclaims reservation. §4.3 excludes conditioning on field of use. A grant aimed at a field is not a restriction on it |
| **OSD 7** Distribution of licence | **The sharpest one.** §10.2 says You need not "reproduce any notice ... retain this file, or inform anyone of anything," and §4.5 adds that nothing requires Your terms to reproduce this text. A downstream recipient may therefore never see that the Work is under ACD | The criterion is about rights applying without an additional licence, not about notice. Its drafter gave the reason as *"The license must be automatic, no signature required."* (Bruce Perens, 2000-11-02, `ACD-1.0.review-readings-7.md` §1.478). §1.6 (§1.4 in 1.0) defines You as **any** person exercising permissions, §4.1 grants to You directly, and §2.3 makes the grant effective "without any act of acceptance." Every recipient holds the grant from the Dedicator, not through a chain. **Precedent is squarely on point:** MIT-0 and 0BSD are approved and likewise require no notice retention. The practical gap — a recipient who does not know what they hold — is real and is recorded as adverse fact #20 rather than argued away |
| **OSD 8** Not specific to a product | §16.3's wording is broader than needed (errata E2) | §16.3 states the instrument "is not specific to any project, person, organisation, jurisdiction, or field of endeavour," and the structural evidence is in §4b: no project name, no URL, no placeholder in the clauses (the one blank is in §16.1's notice template, filled in the adopter's own notice), no edit to the licence text required to adopt |
| **OSD 9** Must not restrict other software | §5.2(b) is a wide covenant about collateral obligations, and §4.5 speaks to what You may add | Both point away from restricting other software: §5.2 binds the **Dedicator**, and §4.5 expressly permits Your other terms to be "incompatible with this Dedication." Nothing conditions the licensing of anything distributed alongside the Work |

**A live reading of OSD 9 that bears on this submission (read at source, license-review 2026-08).**
In the OpenMDW review a participant argued that OSD 9 reaches further than the "same medium"
example: *"I don't think it's much of a stretch to think of **defensive termination provisions as
'restrictions'**"*, anchoring that in the history where Apache-2.0's patent-termination clause was
treated as a source of GPLv2 incompatibility, and in OSD 9's role in the SSPL discussion.

**Two things follow, and only the first is ours to claim.** ACD-1.0 has no termination of any kind
(§10.4) and no patent retaliation (§8.2, expressly), so **whatever that reading decides, this
instrument has nothing in the class being argued about**. That is not a virtue claimed after the
fact —— it is the same design choice recorded as a **cost** in `against.md` #46, where a recipient
who sues the Dedicator keeps every permission. The second thing is what we must not say: **this
does not establish that ACD-1.0 satisfies OSD 9.** Our OSD 9 exposure, if any, is elsewhere ——
§5.2's covenants and §16.4's restrictions on redistributing the licence text —— and it is argued in
the row above on its own terms. **The reading quoted here is one participant's position in a live
thread, not a settled rule**, and it is recorded because a submission that ignores how the criterion
is currently being argued is answering a question nobody is asking.

| Criterion | The argument against | Why it is nonetheless met |
|---|---|---|
| **OSD 10** Technology-neutral | §2.3 forbids click-through, but §6 is written around a particular technology | §2.3 is the operative provision for OSD 10 and it removes the acceptance ritual entirely. §6's subject matter is technological; its **effect** is a grant with no technological predicate. Removing the ritual is what OSD 10 asks for; whether a warranty disclaimer binds a recipient who never assented is a separate question, and OSD 10 does not answer it (`ACD-1.0.against.md` #321). On the lists, the OSD 10 question put to an AI licence by a participant who is not on the Committee concerned a condition triggered by training: Shuji Sado, chairman of Open Source Group Japan, `license-review` 2026-03-14, *"AIAL-1.0 at least raises a substantial question under OSD #10, because its Transparency clause is triggered not only by redistribution, but also by use as input for further AI training."* (`ACD-1.0.review-readings-6.md` §1.473; it carries the weight of a participant, not of the Committee, whose one such record we found is on another point). §6 names training only to permit it, and §10.1 attaches no condition to it. Against that: OSD 10 says *"No provision of the license"*, not "no condition", so a reviewer may still ask whether a clause that names a technology at all is predicated on it |

**The one that would actually be litigated on the list is OSD 7**, and not because the criterion
fails — it does not — but because ACD-1.0 goes further than most approved licences in releasing
the recipient from any obligation to carry the notice forward. That choice is deliberate (§10.2),
it has approved precedent, and its cost is stated as an adverse fact rather than defended.

#### 3b-i. The wide reading of OSD 5, applied

A criterion is a text, and the people who vote are still arguing about how wide some of them
are. On 2026-09-16 McCoy Smith read OSD 5 as reaching **asymmetry between roles**, not only
discrimination between persons and groups: a termination trigger firing only on claims
"against the Licensor" "puts Licensors & Licensees in different positions vis a vis patent
assertions, and therefore arguably violates OSD 5". The reading is contested — its author wrote
"arguably", the steward of the instrument in question answered that "Licensor is a role in the
license, not a person", and no committee or board has ruled on it. We had applied OSD 5 only in
its narrow sense, so we have now applied the wide one as well.

| Asymmetric provision | What it does one way | Under the wide reading |
| :-- | :-- | :-- |
| **§5.2** | The Dedicator covenants not to assert rights in technological measures or invoke anti-circumvention law against You (and authorises circumvention in a use the Dedication permits), not to impose collateral obligations, not to argue for a narrow construction, and not to assert its own rights of privacy, publicity or personality against a permitted use | **The asymmetry runs against the grantor and in favour of every recipient equally.** No recipient is placed in a different position from any other, and the party disadvantaged is the one making the grant |
| **§11.3** | Places a false representation of the Dedicator's authorship, endorsement or association outside the Dedication's reach | **Applies identically to every recipient.** It is a limit of reach, not a condition (§10.1 is unaffected); the Dedication does not make a false statement true |
| **§12.2** | The Dedicator covenants not to exercise, or authorise or assist anyone to exercise, Moral Rights in the Work against You or anyone who receives the Work from You, and consents to acts that would otherwise infringe them, in every jurisdiction | **Runs one way only, in the recipient's favour, and reaches downstream recipients as well.** Nobody is worse off than anybody else |
| **§16.4** | A modified licence text may not be distributed under any name containing "Autonomous Commons Dedication" or any identifier containing "ACD-" followed by a digit, except by the Steward, whose exception reaches only a new version under a number that no earlier text has borne | **The one role-based difference, and it concerns the licence text as a document, not the Work** (§10.5, §16.6). The Steward may issue new versions, in the shape of GPL-3.0 §14; no one may make an existing identifier denote a different text, and no distributor of the Work is touched. ACD-1.0 had no Steward exception; it entered in 1.1 to close errata E14 (see below) |

**On §16.4**, three things are true at once. It concerns **the licence text as a document, not
the Work**: §10.5 and §16.6 say so in terms, so it places no person in a different position with
respect to the licensed work, which is what OSD 5 governs. It is **the same name-integrity term
that approved licences carry for their own texts**, so a reading of OSD 5 that condemned it would
condemn a large part of the approved list with it. OSD 4 contemplates name restrictions of a
similar shape for a different subject, the modified **software**: a licence may require derived
works to carry a different name or version number. §16.4 names the licence **text**, which OSD 4
does not address; Bruce Perens, 2019-08-23, read the sentence narrowly: *"The last sentence of OSD #4
is specific to trademark and branding."* We cite OSD 4 for the idea, not as authority for §16.4
(`review-readings-7.md` §1.479; corrected 2026-11-24 — this sentence had said that OSD 4 "expressly
contemplates" restrictions of this shape). **In ACD-1.0 there is no role-based difference at all**: §16.4 closes
the name and the identifier to every distributor alike. **What remains, and we state it rather
than resolve it, belongs to the successor**: to close errata E14 (1.0 protects the name in general
but only the one identifier `ACD-1.0`), ACD-1.1, ACD-1.2, ACD-1.3 and ACD-1.4 (all frozen; this repository applies ACD-1.4 since 2026-11-23) protect the whole `ACD-N` /
`ACD-N.N` family and let **the Steward alone** issue a modified text under it. *(2026-11-01: this sentence named only "ACD-1.1 and the 1.2 draft"; 1.2 and 1.3 have since been frozen with §16.4 and §16.5 unchanged, and 1.3 is the version applied here, so the Steward exception is now in the licence this repository uses.)* *(Later on 2026-11-01: the 1.4 draft now protects any identifier that begins with "ACD-" followed by a digit, and lets the Steward distribute a modified text under the name and such an identifier "only as a new version under a version number and identifier that no earlier text has borne". *(2026-11-02: the draft now adds ", other than a draft identified as such" after "no earlier text", because a successor drafted in public under its own number could otherwise never be finalised under it; a text labelled as a draft is the one text that may share a final version's identifier.)* The privilege that remains in 1.4 is the power to issue new versions, the shape of GPL-3.0 §14 ("The Free Software Foundation may publish revised and/or new versions"); it no longer includes changing what an existing identifier denotes, which 1.1 to 1.3 did not rule out. The criterion still applies to what remains.)* That is a *(2026-11-12: the 1.4 draft has changed again since the notes above. In the 1.4 draft, the name and the identifier are tested by "contains", regardless of case ("any name that contains "Autonomous Commons Dedication"" and "any identifier that contains "ACD-", regardless of case, followed by a digit"). In the 1.4 draft, the earlier texts that block a version number are those "the Steward or a former Steward has published". In the 1.4 draft, the limit on the Steward's exception is its own sentence, "That exception reaches only a new version under a version number and identifier that no earlier text … has borne". The wording that counts is the one in `ACD-1.4.txt` §16.4; these notes describe it only as it stood on their dates.)*
role-based difference on the face of the document, and a reviewer taking the wide reading at full
strength is entitled to ask about it. Our answer there is the subject-matter limit, not a denial
that the difference exists. *(Corrected 2026-09-24: this paragraph and the row above had
attributed 1.1's Steward exception to ACD-1.0, whose §16.4 has none — `against.md` #160.)*

**The closest decided case is the OVPL, and it draws the line where the Steward exception stays
clear.** The board declined the OVPL on 2005-11-11 because its grant-back to the initial developer
*"creates a situation that discriminates against parties who wish to make their own distribution
of OVPL-licensed code"* (Russell Nelson's announcement). The same year, Mark Radcliffe wrote that
*"such differences in rights is not discrimination under the OSD"*, and Bruce Perens put the test
as whether *"the parties to whom the rights are NOT granted are still getting sufficient rights for
it to otherwise be considered an Open Source license."* The Steward exception burdens nobody's
distribution of the Work and asks nothing of contributors (§16.6); it concerns only who may issue
a new text under the name. Two remarks from the same years support keeping the text fixed at all:
*"You cannot change a single word of a license without losing approval"* (Nelson, 2005-11-01) and
*"most Open Source licenses are themselves not subject to modification without the consent of the
author of the licenses"* (Brian Behlendorf, 2004-11-07). Against this: a reviewer may recall the
OVPL from the shape alone, "one party holds a right others do not", and Lawrence Rosen, who thought
the OVPL approvable, also wrote *"I don't like such special privileges in open source licenses"*
(`ACD-1.0.review-readings-4.md` §1.350, §1.352).

**⚠ And the converse.** Under the wide reading this instrument is *unusually* well placed in the
vulnerable place — it has no termination provision at all (§10.4: no permission
"terminates under it, for any reason") and a non-terminable patent licence (§8.2), so there is no trigger
whose direction could be asymmetric. **But that immunity and a recorded weakness are the same
fact**: the absence of patent retaliation is listed as a cost at `against.md` #174. Being
unreachable by an objection is not the same as having made the better choice.

### 3c. The OSI's own list of common reasons for rejection, item by item

**Source, read 2026-09-07**: `https://opensource.org/licenses/common-reasons-for-rejection-of-licenses`,
linked from the review-process page. It names five patterns. Each is answered from the text.

| Reason OSI publishes | ACD-1.0 |
|---|---|
| **"An express statement that no patent license is granted"** — fails OSD 6, 7 and 8; a licence that says nothing about patents *may* be acceptable if the grant can be read as implied | **The opposite.** §8.1 grants an express, irrevocable, worldwide patent licence, and §8.4 extends it to computational use, models and outputs. §8.2 states there is no retaliation provision and that its absence is deliberate. **This is also the clearest external support for §8 existing at all**: the OSI treats patent silence as a risk to be read around, so a dedication-shaped instrument that stayed silent would be relying on an implication |
| **Badgeware** — requiring a trademark to be displayed; fails OSD 3 and 10 | **Not present.** §10.2 states You need not give attribution or reproduce any notice. §11.1 grants no trademark rights, and §11.2 lets You name the Dedicator truthfully without requiring it *(2026-11-02: this cell said §11.2 "disclaims any requirement to use a name"; §11.2 permits naming, and the absence of any requirement is §10.2's)* |
| **Non-commercial and ethical clauses** — restrict where, why and how; fails OSD 6 | **Not present.** §4.3 states the licence is not conditioned on who You are or what You use the Work for. §10.1 imposes no condition of any kind |
| **Conditional licensing** — "variable outcomes like BUSL that delay availability of full software freedom"; SISSL-style condition-selected *approved* licences have been approved | **Not present, and the nearby-sounding structure is different.** §3 (dedication) and §4 (licence) are not alternatives selected by a condition: §4.4 grants §4 **independently of §3 and not in dependence on §3 being ineffective**, so both operate and the recipient never determines which applies. Nothing becomes available later or expires: §10.4 states no permission terminates for any reason and there is no revival provision. **A reviewer may still raise this** — the answer is that BUSL varies *over time* and SISSL varies *by condition*, whereas ACD-1.0 varies in neither dimension |
| **Phone-home provisions** — require interaction with a specific organisation, website or API; fails OSD 5, sometimes 8 and 10 | **Not present.** There is no interaction requirement of any kind; §10.1 and §10.2 exclude the category |

**Why this section exists.** Until 2026-09-07 this dossier had never read this page, although it is
two clicks from the process page a reviewer cited that morning and is 1,822 characters long
(`against.md` #98). Four of the five are clean by construction — an instrument that imposes no
conditions cannot impose *those* conditions — but **the first is not a negative result at all**: it
is the OSI stating that saying nothing about patents is a risk, which is the case for §8.

### 3d. Subject matter: why this is a software licence and where the overlap with an open-culture licence lies

**The decision this answers.** On 15 September 2023 the OSI Board declined the four Mulan Open
Works Licenses. The recommendation carried to the Board did not find any Open Source Definition
failure. It reads: *"Resolved that it is the opinion of the OSI that the licenses, **as open
culture licenses, are not appropriate for OSI approval**."* The rationale quotes the licences'
own definition — *"a written work, a musical work, a fine art work, an architecture work, a
photographic work, **an audiovisual work**, a graphic work, and a model work"* — and concludes
that *"open culture licenses are outside the purview of the Open Source Initiative."*

**The overlap, stated before it is found.** ACD-1.4 §1.3 (§1.2 in 1.0): *"'Work' means the material to which the
Dedicator has applied this Dedication, in any medium and in any form,
including source code, object code, documentation, data, metadata, **audiovisual material**, and
any collection or compilation of these."* (1.0 also had *"in whole or in part"*, removed in 1.4 to close errata E61.) One of the words the 2023 rationale names appears in our
definition.

**Where the committee itself drew the line.** Pamela Chestek, chairing the License Committee, on
10 August 2023: *"the OSI is not in the practice of approving licenses that are not
software-specific. ... Sometimes an OSI license will **cross over into data or hardware when tied
to software**, but not a license altogether unrelated to software."* Carlo Piana, 5 July 2023:
*"In general, all the licenses should be rejected for not being (Open Source) software licenses."*
Josh Berkus, 1 March 2023: *"OSI has not previously approved content licenses ... it would be an
organizational policy change and therefore not a routine license approval."*

**Why we say this falls on the near side of that line, and what is our reading rather than theirs.**
The Mulan definition contains no software at all; §1.3 begins with source code and object code, the
preamble's first sentence is *"Software and the works that surround it"*, and the work the
instrument is applied to is a software repository. Chestek's carve-out — a licence that crosses
over into data *when tied to software* — describes that shape. **But that is our reading of her
sentence, not a ruling, and the risk is not structural: it is that §1.3, read on its own, is hard
to distinguish from the definition that was declined.**

**Why we have not narrowed §1.3, stated as a cost rather than a defence.** The gap this instrument
claims is about material that is trained on and produced by machines: datasets, model weights and
outputs are exactly the non-code assets in that enumeration. Removing *"audiovisual material"* to
look more software-specific would make the licence read better to a reviewer and cover less of what
it exists to cover. **We would rather carry the objection than narrow the instrument to avoid it.**
**The cost is real and is not cured by saying so:** a reviewer may conclude, as the Board did in
2023, that the subject matter places the instrument outside the OSI's purview, and nothing in this
section prevents that conclusion.

**The Committee has stated a test (added 2026-11-07).** Its rationale for CERN-OHL in 2021 reads:
*"Although software is not the primary use case for the license, and the licenses include some unusual
terminology that make the licenses more difficult to interpret, they are written such that they can be
used for software, so they are appropriate for the OSI's review."* §1.3 opens with source code and object
code, and this text is applied to a software repository, so ACD meets that test on its face. The Mulan
definition had no software in it, so the two records do not conflict. Three limits: §1.3 is wider than
CERN's *"designs that includes both hardware and software"*, the statement predates the 2023 refusal, and
being appropriate for review is not approval.

**OSI's Executive Director went further in 2024**: such documents *"may apply, not just to copyrighted software,
but to non-software artifacts like datasets, documentation, and model parameters"*, and the chair of the Committee
said *"the documents may assure the necessary rights through the use of legal mechanisms other than a license"*
(`license-review`, 2024-09-01 and 2024-09-10). That was said of OSAID terms, and it is not a published rule.

### 3e. Pre-flight: would the FSF and Debian accept it as well? (2026-11-15)

**Why this section exists.** Simon Phipps, then on the OSI board, `license-review` 2017-10-25: *"Seems to me
any license that is approved by only one of {OSI, FSF, Debian} is an indicator of an unaddressed issue. So,
simply as an exercise of reflection, asking if one's license will be approved by all is a great pre-flight
check."* (`review-readings-2.md` §1.229). Neither the FSF nor Debian has looked at ACD. **What follows is our
own reading of ACD-1.4 against their published tests, not their assessment**, and it should be
weighed as such. Clause numbers are those of ACD-1.4. The table was first written on the 1.4 draft on 2026-11-15 and 16; on 2026-11-23 every clause and quotation it cites was checked again against the frozen text and holds there. The FSF's positions are taken from its licence list
(`https://www.gnu.org/licenses/license-list.html`, read on 2026-11-15 and again on 2026-11-16 with the owner's
permission to fetch from gnu.org). The entries for CC0, the Unlicense and *Public Domain*, and the Debian Wiki's public-domain note, are quoted below from `rounds/2026-11-16-fsf-license-list-and-debian-dfsg-public-domain-snapshot.txt` (portfolio-2f): the fetch tool's verbatim quotes, not a byte copy of the page, and to be re-fetched before anything relies on the exact wording. The 0BSD and Expat0 (MIT-0) entries were added to the same file later the same day and are quoted from it too.

| Test | What it asks | ACD-1.4 |
|---|---|---|
| FSF freedom 0 | Run the program for any purpose | §4.1 *"for any purpose whatsoever"*; §4.3 excludes conditions on field of use and on the user |
| FSF freedoms 1 and 3 | Study and change it; distribute changed versions; access to source is a precondition | §4.2 includes study, adaptation and distribution *"in source form, in object form, or in any other form"*. ACD does not require anyone to provide source (§10.2), which the FSF accepts in permissive licences |
| FSF freedom 2 | Redistribute copies | §4.2, §4.5 |
| FSF: the stated reason it does not recommend CC0 for software | The list: *"For works of software it is not recommended, as CC0 has a term expressly stating it does not grant you"* *"any patent licenses."*, and *"If the developer is refusing users patent licenses, the program is in effect a trap for users"* | **Does not apply.** §8.1 and §8.4 grant patent licences and §8.6 adds a covenant |
| FSF: what it says of 0BSD | The list: *"but if the copyright notice or license notice is removed from the program,"* *"it is not possible to safely rely on the license and users might even face liability."*, and *"We recommend that developers choose a license that clearly requires preserving notices for their own works"* *"because of the confusion and antisocial effect that is the result of the 0BSD License."* Of MIT-0: *"Our comments about the Zero-clause BSD license apply to this license."* The same entry also says 0BSD *"can operate as a free software license compatible with the GNU GPL,"* | **Applies to ACD as much as to 0BSD.** §10.2 lets a recipient drop every notice. §2.3 holds that a recipient has every permission without knowing of the Dedication, and §16.2 makes an identifier sufficient notice, but neither helps a recipient who received a copy with nothing on it to show where it came from (`against.md` #41, #326) |
| FSF: what "public domain" is | *"Being in the public domain is not a license; rather, it means the material is not copyrighted and no license is needed."* The list files CC0 and the Unlicense as public domain dedications that each add a fallback licence (the Unlicense's *"additional lax license that helps cover any cases where the dedication is inadequate"*) | **Same structure as ACD.** §3 surrenders, and §4 grants a licence that stands without §3 (§4.4), which is what the FSF's entries for CC0 and the Unlicense describe as a dedication with a fallback |
| FSF: GPL compatibility | No condition that the GPL forbids adding | ACD imposes no condition (§10.1), and §4.5 lets a distributor apply any terms, including the GPL |
| DFSG 1–3 | Free redistribution; source; derived works under the same terms allowed | §4.2, §4.5; no condition is imposed, so nothing prevents derived works under any terms |
| DFSG 4 | Integrity of the author's source code (a licence may require patches) | ACD requires nothing; the only restriction is on distributing a modified **licence text** under its name (§16.4), which §16.6 keeps away from the Work, as the GPL's own text restriction is |
| DFSG 5–6 | No discrimination against persons, groups or fields | §4.3 |
| DFSG 7 | Rights apply to all to whom the program is redistributed | §1.6, §2.3, §4.6 |
| DFSG 8 | Not specific to Debian | §16.3 |
| DFSG 9 | Must not contaminate other software | No condition reaches other works; §12.3 confines the moral-rights covenant and consent to the Work |
| Debian practice (desert island, dissident, tentacles-of-evil tests) | No obligation to send changes, to identify oneself, or that can be altered by a licensor later | §10.1 and §10.2 impose nothing; §2.2 makes the Dedication irrevocable and bars later terms on copies made available |

**Where we expect a question rather than a refusal.** (1) The FSF discourages new licences that duplicate
existing ones; whether it would treat ACD as a new licence or as a public-domain dedication with a patent grant
is not ours to predict (`ACD-OSI-BOTTLENECKS-B10.md` H1-g). (2) Debian's reviewers have asked of dedications
whether the surrender works where the author's country does not recognise it; ACD answers with §4 (an
independent licence, §4.4), the same answer CC0 gives with its fallback licence. The Debian Wiki's licence page says *"Generally, a CC0-style PD dedication is viewed as sufficient for all jurisdictions, and can satisfy the DFSG "* *"if source is available."* (`rounds/2026-11-16-fsf-license-list-and-debian-dfsg-public-domain-snapshot.txt`); it is a wiki FAQ, not Debian's policy text, and it does not name ACD. (3) §6.2 and §6.3, on
reservations for text and data mining, have no counterpart in either test and would be read as statements, not
conditions.

**⚠ Converse.** The pre-flight cuts against us if it is run by them rather than by us: Phipps's test treats a
licence approved by only one of the three as a sign of trouble, and if the FSF or Debian were to reach a
different answer on any row above, that answer would itself be an adverse fact (`against.md` #328). A
self-assessment is also the kind of statement that a reviewer may discount as the drafter's view of its own
text.

**The step after a self-assessment is to ask them.** Mozilla did so when it submitted MPL 2.0: Luis Villa,
for Mozilla, `license-review` 2010-11, *"Just as we're asking OSI, we're also asking FSF to be on
their lists of Libre and compatible licenses, and have spoken with them to that end."* (`review-readings-2.md`
§1.235). Asking the FSF's licensing team and `debian-legal` in parallel answers the discount above with their
view rather than ours. Under the moderators' notice (register B14) the owner, not the AI, would send those
questions.

**Added 2026-11-16 — a lead to the FSF's own record, not the FSF's words.** Mike Linksvayer, writing for Creative Commons on `license-discuss` 2011-08-08: *"The exception that proves the rule is the CC0 public domain dedication, which is GPL-compatible and with the FSF we recently recommended for software if public domain is the intention."* (`review-readings-2.md` §1.253, portfolio-2f). This is CC reporting a joint recommendation; the FSF's own statement of 2011, and what it said later about CC0's patent exclusion, are still to be read from FSF sources before the self-check above relies on them. **Checked against the list on 2026-11-16**: the FSF's current entry for CC0 says (in the fetch tool's summary, not word for word) that it does not recommend CC0 for software because CC0 expressly grants no patent licences. If the 2011 joint recommendation happened as Creative Commons described it, the FSF's position has since moved on CC0 for software, and the reason it gives is the one ACD's §8 answers.
