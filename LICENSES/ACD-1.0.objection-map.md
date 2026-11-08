---
file: LICENSES/ACD-1.0.objection-map.md
audience: OSI license-review / license-discuss participants, licence reviewers, auditors
last-updated: 2026-11-07
canonical-ref: LICENSES/ACD-1.0.review-precedents.md (the original text and our reading of each objection) / LICENSES/ACD-1.0.against.md (the adverse record) / LICENSES/REVIEWERS.md (the entry page)
---

# Which known objections land on ACD

## 1.62 The objections we found, and whether each one lands

**This page is not here to show that we are right.** A reviewer's first question is which known
objections apply to this submission and which do not, so the ones that land come first.

**Sources.** Everything is from the public `license-review` / `license-discuss` archives, with
speaker and date, except the Board minutes in the second table. **It is a floor, not a census**: we listed every subject line, read the threads
that matched, and kept objections that bear on a public-domain-equivalent or AI-facing instrument.
The main table covers the last 24 months. Objections can have been missed; the OpenMDW thread alone
ran to 86 messages in 2026-08, and we did not break all of them down. **"Does not land" is our
reading, not a reviewer's finding.**

**Numbers.** Clause numbers are those of ACD-1.0, the text posted to `license-discuss`, unless a
version is named. `#N` is an entry in [`ACD-1.0.against.md`](ACD-1.0.against.md); `§1.x` is a section
of the dossier, in Japanese unless it says otherwise.

### Objections that land

| Objection | Source | Where it lands on ACD | Record |
|---|---|---|---|
| *"you'd likely need to have the help of a lawyer. **Waivers/disclaimers of IP rights are quite complex**"* | McCoy Smith, `license-discuss` 2026-08-07 | **No legal review.** The only answer is that this is true and we do not have one | #5 / #79 / §1.52 |
| *"**why you're doing another one?**"* (public-domain equivalents are the one fungible class, and 0BSD exists) | Rob Landley, same list 2026-08-07 | **The reason to add one more.** Our partial answers are a patent grant that goes beyond the work with no condition and no termination (§1.133), moral rights (§1.59), and that §4.5 creates no dead end, the Board's test for SimPL in 2007 | #84 / §1.59 |
| *"A patent grant with zero attribution seems equivalent to abandoning the patent."* / *"It's not the goal of the OSI to have licenses for every possible combination of conditions"* | Rob Landley; Josh Berkus, same list 2026-10-14, on 0BSD-P | **§8 + §10.2 is that combination**, though neither message addresses ACD. The chain-of-custody cost is real and we admit it. To Berkus's question, what specific use needs this, we can describe one: a work published to be learned from, as this repository is, where a notice condition has no settled way through training. We cannot show a second, and no adopter yet exercises the patent half. Recent permissive approvals (0BSD, BSD-2-Clause-Patent, MIT-0, OSC) each differ from a neighbour by one point, but all four reuse an existing text (`ACD-1.0.gap-measurements.md` §1.137) | #276 |
| *"a license of this complexity needs to be drafted by a professional"* | Pamela Chestek, `license-review` 2026-04-14, on Project Tick GPL; McCoy Smith 2025-10-26 and Shuji Sado 2026-03-14 said the same of other submissions | **No legal review**, in the form members now put it. The process page requires disclosure, not a lawyer | #291 / §1.140 |
| *"Looks like AI slop to me and is clearly not OSD-compliant from the description"* | Pamela Chestek, `license-review` 2025-08-14, on AFN-License | **How an AI-drafted text may be received.** Her reason also names the OSD. ACD says how it was drafted and asks to be read as text | #292 / §1.140 |
| *"a flood of thought exercise licenses"* | Carlo Piana, `license-review` 2025-08-18 | **One adopter.** He says use is not a requirement but must be weighed before review starts | #294 / §1.140 |
| *"the addition of aspirational language in legal text"* | Carlo Piana, `license-review` 2026-01-16 | **Reasons inside clauses.** The preamble is labelled non-operative. §8.2 to §8.4 state reasons in operative text | #295 / §1.140 |
| *"**It is excessively wordy** and proscriptive… no one other than you will ever use this license"* | Pamela Chestek, same list 2026-06-23 | **Length and adoption.** The short route through this directory helps with the first. **One adopter does not move** | #6 / §1.60 |
| *"**Which is it, a dedication to the public domain or a license? You can't have it both ways.**"* | Pamela Chestek, same list 2025-10-16 | **The §3 + §4 + §4.4 structure itself.** §11.3 anticipates it, but the answer takes four clauses. The substance of her criticism is reserving rights one by one, so the comparison is with what approved licences place in the same position: BSD-3-Clause's third clause is a condition and Apache-2.0 §6 a limit of reach (§1.7) An article on OSI's site named these two parts in 2017: *"disclaim ownership for the jurisdictions where that is possible, and then grant a copyright license that has the same practical effect"*. It is one author's article, not a decision | #110 / #118 / §1.61 / §1.7 |
| **Moral-rights clause called "mission creep"** | Pamela Chestek, same list 2026-06-23 | **§12**, the clause §1.59 counts as a gap in the incumbents | #6 / §1.59 / §1.60 |
| *"**these are not licensable**, so anything the license says one way or the other, nothing changes"* (moral rights) | Carlo Piana, `license-review` 2023-11 | **Lands on the §12.1 waiver.** The §12.2 covenant not to exercise does not fall to the same objection | #104 |
| *"**it is an issue as to whether a license of this scope would gain significant uptake at least from patent holders**"* | McCoy Smith, `license-review` 2025-05-14 | **§8.1 + §8.4 + no retaliation.** Not an OSD problem, but it bears on SPDX's real-use condition | #107 / §1.58 |
| *"three different things with one document"* | Pamela Chestek, `license-discuss` 2026-03-29 | **The 16-section structure**, although each section acts on the same Work | #105 |
| **One instrument should carry one right** (a summary, not a quotation) | Rob Landley | **§3 to §12 cover several kinds of right.** This pulls against #105, and reordering cannot satisfy both | #102 |
| *"there is **no requirement for a court to consider statements outside the four corners of** the license itself… **you can't count on FAQs** to prevent an unintended interpretation"* | Pamela Chestek, `license-review` 2026-09-01 | **The shape of this whole dossier.** Text outside the licence is at most evidence of intent. The answer is not to write more; §4.4 is one case of putting the point in the clause | #124 |
| *"**it's not worth including Output at all** in the license"* (mentioning it creates a negative implication and ambiguity) | Pamela Chestek, same list 2025-12-15 | **§6.4, a deliberate design.** The same message says *"I wouldn't reject the license for that reason"* | #133 |
| **How do you know what the covered work is?** (the central question of a month's review; this is a summary, not a quotation, and the wording is #134's) | Richard Fontana, same list 2026-08-16 | **§1.2 (the act of applying fixes the Work) + §2.7 + the Dedicator's undertaking to identify.** Only partly answered | #134 |
| *"probably going to be parsed in court as a **dedication to the public domain rather than a contract**. There is thus **some question of how binding the terms could be on the grantor**"* | Bruce Perens, `license-discuss` 2024-04-06 | **The three promises the Dedicator makes on top of §3.** Same root as "which is it" above | #135 |
| *"The OSI **does not currently have a process for de-listing** licenses"* | Richard Fontana, `license-review` 2026-09-11 (and Carlo Piana 2026-09-14) | **The cost side of our answer to #84.** "Adding one to this class costs little" became "costs little and cannot be undone" | #146 |
| *"putting the **burden on the potentially wronged party**… assuming the licensee **has knowledge**… **that's not the reality**"* | Pamela Chestek, same list 2026-09-11 | **§6.3**, the one clause said to operate on third parties' acts. **Closed from ACD-1.1**; 1.0 stays frozen | #147 |
| **OSD 5 read as far as asymmetry of roles** (we had applied it only to discrimination against persons and groups) | McCoy Smith, same list 2026-09-16 | **The Steward exception in §16.4.** On the wide reading there is a difference, and all we can say is that this standard does not govern it. **We have not refuted it** | #179 / §3b-i |
| *"**structurally put the licensor in a more favored position** than any licensee"* (a published criterion) / *"**That is the discrimination**"* | Pamela Chestek, with McCoy Smith, same list 2026-09-20 to 22, on ModelGo | Said of a termination trigger limited to suits against the Licensor. ACD terminates nothing, but **§13 and §14 protect the Dedicator**, and the criterion has not been applied to them | #265 / §1.123 |
| *"any terms applying to contributors should be in individual projects' contributor documentation and governance, and have no place in an OSS license"* | Josh Berkus, `license-discuss` 2025-12-08 | **§2.6 is such a clause.** Pamela Chestek answered in the same thread: *"I am in favor of an express statement in the license and agree that the statement should be inbound=outbound"*. §2.6 is inbound=outbound and leaves the rest to project governance. It also makes a contributor a Dedicator, which asks more than the usual clause | #286 |
| *"The lawyers on this list who reviewed that provision found it legally dubious"*, on terms that apply with no copy of the licence present | Josh Berkus, `license-review` 2015-10-13, on the Free Public License | **§16.2 says this outright.** The OSI took outside counsel and approved that licence, and whether §16.2 works is a question for a lawyer | #287 |
| *"significant problems in the first few paragraphs, indicating that undoubtedly the drafting problems were throughout"*, and *"this is not a task for the layperson."* | Pamela Chestek, `license-review` 2026-02-23, on OSCL | **The opening of ACD is read hardest.** A defect in §1 counts for the whole text | #303 |
| *"**flawed in its basic conception**"*: *"a single license that applies to everything"* | Richard Fontana, same list 2026-09-11, on OpenMDW | **§1.2 also puts many kinds of material under one text.** The harm he names needs a clause that some of the material cannot justify; ACD's material-specific clauses only remove duties or add permissions (§1.125). That is our reading, and the steward's defence he was answering is not a committee finding. The chair said in 2024 that the area *"needs room to develop"*, which may not happen if OSI dictates *"whether that is a single license for all components or separate licenses"*. His objection is later | #266 / §1.125 |
| Traditional licences are *"appropriate even in situations where copyrightability is relatively dubious"* | Richard Fontana, `license-discuss` 2026-04-06 | **§9's reason for being.** We agree that §9 adds no effect, and it is not a ground of uniqueness (§1.134) | #211 / §1.134 |

### Statements from outside that window that decide this submission

Older, or not from the lists, but each one goes to whether ACD can be approved.

| Statement | Source | Why it matters here | Record |
|---|---|---|---|
| *"OSI really does need to trust the license steward when an upgrade clause is in play"* | Bradley Kuhn, `license-review` 2018-11-22, on SSPL | **ACD has no upgrade clause**, and a new version does not reach a work already dedicated. Rosen answered the same distrust of one person with section 16 of AFL and OSL, which §16.4 resembles. Kuhn also says OSI should consider *"who the license steward is"*, and no successor is named | #10 / B12 |
| *"a license could stay in a status where it is **not approved** if it is duplicative and not used by a project"* | OSI Board minutes, 2025-07-18, and the Committee's hold on Tiwaz, 2025-09-11: *"a close variant of an existing license"* with *"no demonstrated uses or planned uses"* | **The outcome to prepare for, and it is not a rejection.** The two parts are joined by *and*, and the hold lifts if *"one or more projects begin using this license or express an interest in doing so"*. ACD is not a variant of an existing text, and the patent combination in the first table answers "duplicative". It has one use, this repository, which is the steward's own. The OSC License was approved on use its submitter's client had planned, but Piana in 2026 (*"not having an active project"*) points the other way. Non-use alone has not been a ground: the Committee wrote in its rationale for MIT-0 (2020) that it is *"not a basis for rejection that the OSI has applied in the past"* | #84 / #285 / B2 |
| *"we recommend that you always apply an approved Open Source license to software you are releasing, rather than try to waive copyright altogether"*, and a licence *"enables the protection of attribution"* | OSI's FAQ, last modified 2025-01-21 | **§3 does try to waive copyright, and §10.2 gives up attribution.** Our answer is that §4 applies a licence independently of §3. The same FAQ is the strongest record in our favour on the licence and on patents (`REVIEWERS.md`) | §4.4 |
| *"**The lawyers who opined on the issue, both US and non-US, agreed** that the document would most likely be interpreted as a license and that the license met the OSD."* | Committee rationale for the Unlicense, 2020 | **Our one dedication-plus-licence precedent crossed the line with what we lack** | #270 |
| *"as open culture licenses, are **not appropriate for OSI approval**"*, naming *"an audiovisual work"* among the subject matter | License Committee recommendation on the Mulan licences; Board decision 2023-09-15 | **§1.2 lists audiovisual material, but it opens with source code and object code.** The Committee stated a test for CERN-OHL in 2021: *"they are written such that they can be used for software, so they are appropriate for the OSI's review"*, though software was not their primary use. In 2024 OSI's Executive Director said review may reach *"non-software artifacts like datasets, documentation, and model parameters"*. Mulan's definition had no software in it. ACD's list is wider than CERN's, and the list cannot be narrowed without losing non-code assets | #237 / B15 |
| *"**widespread** need for many different FOSS communities"* and *"wholly unserved by all existing FOSS licenses"* | Bradley M. Kuhn, 2022-12-23 | **A two-part test for a vanity licence.** The census answers the second part. One adopter does not answer the first | #255 |
| *"it is an active disservice to the programmers of the world"*, *"please get a lawyer to write a license for you"* | Bruce Perens, 2019-05-28 | **§16.3 invites anyone to adopt ACD**, and the harm he names falls on adopters. Disclosure does not remove that | #262 |
| *"There are reasons beyond OSD conformance why we might not want to approve the license."* | Russ Nelson, OSI President, 2009-02-17 | **Conformance is a floor.** Meeting every listed criterion does not oblige approval | #263 |
| *"A patent license is antithetical to a public domain declaration."*, and *"to whom would any waiver of patent rights apply then?"* | Russ Nelson and Karl Fogel, `license-review` 2012-02-18, on CC0 | **The form ACD takes.** §8.1 goes straight from the Dedicator to You, depends on no copyright licence (§2.4), and does not travel with a copy or a notice (§2.3, §10.2). It reaches what is derived from the Work, not what someone reinvents. No review has tested this form | #288 / §1.138 |
| *"excessive vagueness, problems of comprehensibility, inconsistency across provisions"* | Richard Fontana, in the thread on a Committee report, 2014-06-30 | **Faults that can stop a licence outside the OSD.** Our errata record all three in ACD, and he names the submitter most exposed: *"a non-lawyer with no affiliation with a prestigious institution"* | #293 / §1.140 |
| *"It is only because a FOSS license imposes conditions that it may be enforceable by the parties."* | Lawrence Rosen, `license-discuss` 2011-04-18 | **§10.1 imposes none.** There is nothing for the Dedicator to enforce, and the Board approved 0BSD, *"a license with no conditions"*, in 2015 | #307 |
| *"I'd really like to see a real patent attorney work on this question."* | Josh Berkus, `license-review` 2016-01-14, on the licence now BSD-2-Clause-Patent | **§8 was drafted without a lawyer**, and that licence was drafted by one | #308 |
| *"The license review process is not for workshopping a license, it is for a go/no-go on a license."* | Pamela Chestek as chair, `license-review` 2023-08-22 | **Comments on a submission do not replace review before it.** The text has to be finished first | #298 |
| *"make different statements about that subject matter. Why did you add them?"* | Pamela Chestek, `license-discuss` 2019-08-05 | **§3, §4 and §5 overlap by design.** Their legal effects differ, and §2.4 states how they stand together | #299 |
| *"There has to be a real problem (material ongoing harm) to warrant incurring these costs."* | Roland Turner, `license-review` 2021-02-14 | **The gap is a measurement of texts.** The harm we can show is Fedora's 2022 decision on CC0 | #301 |
| *"Without access to the license, recipients won't know that they have this right."* | Lukas Atkinson, `license-review` 2021-02-11 | **§10.1 asks for no notice**, and §2.3 does not need the recipient to know. 0BSD has the same property | #306 |
| *"I almost feel like you wrote three different licenses here and combined them into one."* | Richard Fontana, 2014-04-13 | **§3, §4 and §5 say the same thing three ways by design.** Three such pairs did disagree (E42 to E44); the 1.4 draft closes them | #280 |

### Objections that do not land (checked against the text)

| Objection | Source | Why it does not land |
|---|---|---|
| *"OSI doesn't approve **partial licenses or add-ons to existing licenses**"* | McCoy Smith, `license-discuss` 2026-08-03 | ACD is a complete, free-standing document (`ACD-1.0.txt` alone: 16 sections, 82 clauses) |
| Clauses that treat commercial and non-commercial use differently | Henrik Ingo, same list 2026-08-05, and others. Bruce Perens explained OSD 6's origin there on 2026-08-06 (the Berkeley SPICE clause on South African police) | **§4.3**: the licence is not conditioned on who you are or what you do with the Work |
| **Giving up trademarks too** | subham mahesh, same list 2026-08-07 | **§1.5** excludes trademarks from Covered Rights and **§11.1** grants no trademark right |
| **Automatic termination on a patent suit** (OSD 5, an over-broad trigger) | Pamela Chestek 2025-10-16; McCoy Smith 2026-09-07 (Q3, Q4) | **§8.2**: *"contains no patent retaliation provision, and its absence is deliberate"*. McCoy Smith's article on OSI's blog (2025-12-04) speaks of express grants *"with or without defensive termination provisions"*. This has a cost; see the note below |
| **A clause forbidding unlawful use** (a reservation) | Pamela Chestek 2025-10-16 | Not in the text (`unlawful` / `illegal`: 0 occurrences, measured 2026-09-09) |
| **"Irrevocable" beside automatic termination** | Pamela Chestek, `license-review` 2026-01 (PUWL) | **§10.4** terminates nothing, and §4.1 is irrevocable and perpetual |
| **Wording borrowed from existing licences** | Lukas Atkinson and McCoy Smith, on other submissions | No shared 8-word run with MIT, MIT-0, 0BSD, Apache-2.0, CC0 or the Unlicense (§4c gives the method and a control) |
| **A model has no source code to open, so Freedoms 1 and 3 fail** | John Colagioia, `license-review` 2026-08-29 | ACD is not a model licence. Its subject is the Work, and §9.2 makes no representation about machine-generated material |
| **Not open without the training data** (*"or any other license with similar flaws"*) | Preston Maness, same list 2026-09-08 | As above. ACD never claims that a given model is open |
| **Duties to label or disclose outputs** (where AI-era submissions stopped on OSD 3, 7 and 10) | The AI-MIT, RAIL and FMLL threads | **§10.1**: no condition of any kind |

**The cost of no retaliation.** The row above records only the reviewers' concern. Retaliation clauses
exist for a reason: Apache-2.0 §3 and GPLv3 §10 end a recipient's licence if it sues, which deters
patent attacks. §8.2 gives up that deterrent, so a competitor can absorb the technology and still sue
the Dedicator (#174). §10.1 allows no condition, so such a clause cannot be placed here. **We leave it
out because we cannot have it, not because leaving it out is better** (register B7).

### Limits of this page

1. **"Does not land" is our reading.** We do not decide where a reviewer aims a word, and *AI* in
   particular can call up the three AI-related rows above by reflex.
2. **Objections combine.** "Long", "one adopter" and "no lawyer" can each be answered and still add up
   to one inference, and Pamela Chestek has combined them that way. Lukas Atkinson joined two of them
   in one sentence on 2021-02-14: *"submitted licenses should have either received **legal review** or
   at least **non-negligible use**. This license has **neither**"* (#113, §1.64). **The tables answer
   row by row. They do not answer that sentence.** The nearest answer is later and from the Committee: *"to
   date, OSI has not used the number of projects adopting a license as a factor"* (Jam rationale, 2021-09-12).
3. **It is not exhaustive.** The windows we read are listed in `PEER-REVIEW-WATCH.md` §3.9.
4. **Nothing updates this page automatically.** An entry added to `ACD-1.0.against.md` does not reach
   it. It went stale twice (#196, and again until 2026-11-06), and it last caught up at #308.
