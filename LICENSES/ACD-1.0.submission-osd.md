---
file: LICENSES/ACD-1.0.submission-osd.md
audience: OSI license-review participants / licence reviewers / 監査人 / 次のセッションの実装者
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.submission-reference.md (切り出し元・§1〜§2 / §4〜§5) / LICENSES/ACD-1.0.submission.md (送る文面は §B.0。**これを貼らない**)
---

# ACD-1.0 — 提出参考資料のうち OSD の節（§3 / §3b / §3c / §3d・**貼らない**）

**`ACD-1.0.submission-reference.md` から 2026-09-25 に切り出した**（899 行で advisory 900 の 1 行手前に達したため・
予算表が事前に宣言していた分割計画どおり）。**節番号は動かしていない。** 切り出し元には各節の案内見出しを残してあるので、
既存の `submission-reference.md §3b` などの参照は案内を経てここへ着く。
**本文中の裸の `§4c` / `§2` などは、切り出し元（`submission-reference.md`）の節を指す。**

**なぜこの節だけか**: ここは「審査者が OSD の話をしに来たとき」という単一の用途で読まれ、
他の節（なぜ新しいライセンスが要るか・既存との差・開示）とは読み手が分かれる。

### 3. Open Source Definition conformance

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
  answered the first limb only.
- **OSD 4 (Integrity of the author's source code).** No restriction is imposed. Section
  16.4 concerns the text of the licence *as a document*, not the licensed work; Sections
  10.5 and 16.5 state this expressly.
- **OSD 5 (No discrimination against persons or groups)** and **OSD 6 (No discrimination
  against fields of endeavour).** Section 4.3 states that the licence is conditioned on no
  restriction as to persons, groups, technologies, endeavours or jurisdictions, and on no
  field of use.
- **OSD 5 (No discrimination against persons or groups).** §4.3 states the licence is not
  conditioned "on the identity, character, or purpose of the user, or on any restriction as to
  persons, groups, technologies, endeavours, or jurisdictions." §2.3 adds that the grant takes
  effect without any act of acceptance, so there is no gate at which a person could be excluded.
- **OSD 6 (No discrimination against fields of endeavour).** The same sentence of §4.3 excludes
  conditioning "on field of use." §6 goes further in one direction only — it names machine
  learning and text-and-data-mining expressly in order to **permit** them, not to single them out
  for a condition.
- **OSD 7 (Distribution of licence).** Section 2.3 makes the licence effective without any
  act of acceptance; Section 16.2 makes an identifier or SPDX tag sufficient notice, so
  rights attach to every recipient without further action.
- **OSD 8 (Licence must not be specific to a product).** Section 16.3.
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
| **OSD 2** Source code | The instrument never requires source to be available. §10.2 says You "need not ... make source available" | OSD 2 bars a licence from **obstructing** source distribution and requires the preferred form when a program is distributed under it; §4.2 grants distribution "in source form, in object form, or in any other form." Permissive licences are approved on this basis |
| **OSD 3** Derived works | — | §4.2 grants adaptation, modification and derivative works expressly, and §4.3 attaches no condition to them |
| **OSD 4** Integrity of the author's source code | §16.4 forbids distributing **the licence text** in modified form under the name or identifier. A reviewer skimming may read that as a restriction on the Work | It is not: §10.1 is limited to conditions "in respect of the Work," and §16.4 governs the licence text only. The provision is the same name-integrity term GPL and Apache-2.0 carry for their own texts. The looseness is in the notice wording, recorded as errata E3 |
| **OSD 5** Persons or groups | §11.3 withholds one thing — falsely representing the Dedicator's authorship or endorsement | §11.3 says in terms that it "states a limit of the Dedication's reach; it is not a condition upon You, and Section 10.1 is unaffected by it." Misrepresentation was never the Dedicator's to permit, so withholding it discriminates against no one. **A wider reading of OSD 5 is live on the list**: on 2026-09-16 McCoy Smith argued that a termination trigger firing only on claims "against the Licensor" "puts Licensors & Licensees in different positions vis a vis patent assertions, and therefore arguably violates OSD 5". **This instrument has no trigger to point in either direction** — §10.4 states that no permission "terminates for any reason" and that it "contains no termination provision and no revival provision", and §8.2 makes the patent licence non-terminable. **The wider reading is not established** (its author wrote "arguably" and the steward contested it), and we record our own exposure to it at `against.md` #179 |
| **OSD 6** Fields of endeavour | §6 names machine learning and TDM specifically. Naming a field at all can look like singling it out | The naming is entirely permissive: §6 grants and disclaims reservation. §4.3 excludes conditioning on field of use. A grant aimed at a field is not a restriction on it |
| **OSD 7** Distribution of licence | **The sharpest one.** §10.2 says You need not "reproduce any notice ... retain this file, or inform anyone of anything," and §4.5 adds that nothing requires Your terms to reproduce this text. A downstream recipient may therefore never see that the Work is under ACD-1.0 | The criterion is about rights applying without an additional licence, not about notice. §1.4 defines You as **any** person exercising permissions, §4.1 grants to You directly, and §2.3 makes the grant effective "without any act of acceptance." Every recipient holds the grant from the Dedicator, not through a chain. **Precedent is squarely on point:** MIT-0 and 0BSD are approved and likewise require no notice retention. The practical gap — a recipient who does not know what they hold — is real and is recorded as adverse fact #20 rather than argued away |
| **OSD 8** Not specific to a product | §16.3's wording is broader than needed (errata E2) | §16.3 states the instrument "is not specific to any project, person, organisation, jurisdiction, or field of endeavour," and the structural evidence is in §4b: no project name, no URL, no placeholder in the clauses (the one blank is in §16.1's notice template, filled in the adopter's own notice), no edit to the licence text required to adopt |
| **OSD 9** Must not restrict other software | §5.2(b) is a wide covenant about collateral obligations, and §4.5 speaks to what You may add | Both point away from restricting other software: §5.2 binds the **Dedicator**, and §4.5 expressly permits Your other terms to be "incompatible with these." Nothing conditions the licensing of anything distributed alongside the Work |

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

| **OSD 10** Technology-neutral | §2.3 forbids click-through, but §6 is written around a particular technology | §2.3 is the operative provision for OSD 10 and it removes the acceptance ritual entirely. §6's subject matter is technological; its **effect** is a grant with no technological predicate |

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
| **§5.2** | The Dedicator covenants not to apply or invoke technological measures or laws against You, not to impose collateral conditions, and not to argue for a narrow construction | **The asymmetry runs against the grantor and in favour of every recipient equally.** No recipient is placed in a different position from any other, and the party disadvantaged is the one making the grant |
| **§11.3** | Withholds permission to misrepresent the Dedicator's authorship or endorsement | **Applies identically to every recipient.** It is a limit of reach, not a condition (§10.1 is unaffected), and what it withholds was never the Dedicator's to permit |
| **§12.2** | The Dedicator covenants not to exercise Moral Rights against You or against anyone who receives the Work from You | **Runs one way only, in the recipient's favour, and reaches downstream recipients as well.** Nobody is worse off than anybody else |
| **§16.4** | A modified licence text may not be distributed under the name "Autonomous Commons Dedication" or under the identifier "ACD-1.0". **ACD-1.0 makes no exception for any party** | **Applies identically to every distributor of the text, the steward included.** The role-based difference this row once conceded is in the **successor**, not in 1.0: ACD-1.1 and the 1.2 draft add *"except by the Steward"* to close errata E14 — see below |

**On §16.4**, three things are true at once. It concerns **the licence text as a document, not
the Work**: §10.5 and §16.6 say so in terms, so it places no person in a different position with
respect to the licensed work, which is what OSD 5 governs. It is **the same name-integrity term
that approved licences carry for their own texts**, so a reading of OSD 5 that condemned it would
condemn a large part of the approved list with it. And OSD 4 **expressly contemplates** name
restrictions of this shape. **In ACD-1.0 there is no role-based difference at all**: §16.4 closes
the name and the identifier to every distributor alike. **What remains, and we state it rather
than resolve it, belongs to the successor**: to close errata E14 (1.0 protects the name in general
but only the one identifier `ACD-1.0`), ACD-1.1 and the 1.2 draft protect the whole `ACD-N` /
`ACD-N.N` family and let **the Steward alone** issue a modified text under it. That is a
role-based difference on the face of the document, and a reviewer taking the wide reading at full
strength is entitled to ask about it. Our answer there is the subject-matter limit, not a denial
that the difference exists. *(Corrected 2026-09-24: this paragraph and the row above had
attributed 1.1's Steward exception to ACD-1.0, whose §16.4 has none — `against.md` #160.)*

**⚠ And the converse.** Under the wide reading this instrument is *unusually* well placed in the
vulnerable place — it has no termination provision at all (§10.4: no permission
"terminates for any reason") and a non-terminable patent licence (§8.2), so there is no trigger
whose direction could be asymmetric. **But that immunity and a recorded weakness are the same
fact**: the absence of patent retaliation is listed as a cost at `against.md` #174. Being
unreachable by an objection is not the same as having made the better choice.

### 3c. The OSI's own list of common reasons for rejection, item by item

**Source, read 2026-09-07**: `https://opensource.org/licenses/common-reasons-for-rejection-of-licenses`,
linked from the review-process page. It names five patterns. Each is answered from the text.

| Reason OSI publishes | ACD-1.0 |
|---|---|
| **"An express statement that no patent license is granted"** — fails OSD 6, 7 and 8; a licence that says nothing about patents *may* be acceptable if the grant can be read as implied | **The opposite.** §8.1 grants an express, irrevocable, worldwide patent licence, and §8.4 extends it to computational use, models and outputs. §8.2 states there is no retaliation provision and that its absence is deliberate. **This is also the clearest external support for §8 existing at all**: the OSI treats patent silence as a risk to be read around, so a dedication-shaped instrument that stayed silent would be relying on an implication |
| **Badgeware** — requiring a trademark to be displayed; fails OSD 3 and 10 | **Not present.** §10.2 states You need not give attribution or reproduce any notice. §11.1 grants no trademark rights and §11.2 disclaims any requirement to use a name |
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

**The overlap, stated before it is found.** ACD-1.0 §1.2: *"'Work' means the material to which the
Dedicator has applied this Dedication, in whole or in part, in any medium and in any form,
including source code, object code, documentation, data, metadata, **audiovisual material**, and
any collection or compilation of these."* One of the words the 2023 rationale names appears in our
definition.

**Where the committee itself drew the line.** Pamela Chestek, chairing the License Committee, on
10 August 2023: *"the OSI is not in the practice of approving licenses that are not
software-specific. ... Sometimes an OSI license will **cross over into data or hardware when tied
to software**, but not a license altogether unrelated to software."* Carlo Piana, 5 July 2023:
*"In general, all the licenses should be rejected for not being (Open Source) software licenses."*
Josh Berkus, 1 March 2023: *"OSI has not previously approved content licenses ... it would be an
organizational policy change and therefore not a routine license approval."*

**Why we say this falls on the near side of that line, and what is our reading rather than theirs.**
The Mulan definition contains no software at all; §1.2 begins with source code and object code, the
preamble's first sentence is *"Software and the works that surround it"*, and the work the
instrument is applied to is a software repository. Chestek's carve-out — a licence that crosses
over into data *when tied to software* — describes that shape. **But that is our reading of her
sentence, not a ruling, and the risk is not structural: it is that §1.2, read on its own, is hard
to distinguish from the definition that was declined.**

**Why we have not narrowed §1.2, stated as a cost rather than a defence.** The gap this instrument
claims is about material that is trained on and produced by machines: datasets, model weights and
outputs are exactly the non-code assets in that enumeration. Removing *"audiovisual material"* to
look more software-specific would make the licence read better to a reviewer and cover less of what
it exists to cover. **We would rather carry the objection than narrow the instrument to avoid it.**
**The cost is real and is not cured by saying so:** a reviewer may conclude, as the Board did in
2023, that the subject matter places the instrument outside the OSI's purview, and nothing in this
section prevents that conclusion.
