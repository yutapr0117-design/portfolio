---
file: LICENSES/ACD-1.0.submission.md
audience: OSI license-discuss / license-review participants, SPDX submitters, the human who sends the message
last-updated: 2026-11-23
canonical-ref: LICENSES/ACD-1.0.txt (the text being submitted) / LICENSES/REVIEWERS.md (English entry point) / LICENSES/ACD-1.0.against.md (the adverse case)
---

# ACD — submission materials (English; facts for the owner, not text to paste)

> **What this file is.** The facts and fields the owner needs in order to submit the
> Autonomous Commons Dedication — now ACD-1.4 — to OSI License Review and to the SPDX
> License List, written in the language those bodies use. **The owner writes and sends the
> messages in his own words** (B14, gate 0 of `REVISION-PROTOCOL.md`); since decision 3b of
> the five (2026-11-23) this file no longer holds a message to paste.
>
<!-- SUBMISSION-TARGET: ACD-1.4 -->
<!--
  **この packet がどの版を提出対象にしているかを宣言する単一ソース。** 値は `ACD-<版>`。
  **Check 472 が、提出側の文書に現れる `§N.M` 引用のすべてが、この版の条文に実在することを
  BLOCKING で強制する。**

  なぜ要るか: **条番号は版をまたいで保存されない。** 1.0 の §15.5 / §15.7 / §15.8 は
  1.1 以降に存在せず、§16.4〜§16.6 は意味が違う。**提出対象を切り替えた瞬間に、
  提出物が「何も述べていない条」へ審査者を送る**ことになる ——`against.md` #144 で
  一度踏んだ class そのもの（自分のライセンスを 5 か所で誤引用し、2 か所は審査者を
  別の条へ送っていた）。**確定手順 (§0.13) はこの再写像を列挙していなかった。**

  切り替え方: **ここを `ACD-1.2` に変えれば、残りは CI が指す。**
-->

> **Status of the licence itself:** the version submitted is `LICENSES/ACD-1.4.txt`; the version posted to `license-discuss` was `LICENSES/ACD-1.0.txt`. The rationale, the
> gap analysis, the clause-level comparison with the closest OSI-approved licences, and
> the honest weaknesses are in `docs/architecture/acd-license-rationale.md` (Japanese).
>
> **Do not send anything from this file until `LICENSES/READY-TO-SUBMIT.md` exists.**
> Its absence means the text is still being improved and is not yet at a standard where
> a review verdict would be worth having.

---

## Status as of 2026-08-26

| | |
|---|---|
| **Sent** | **OSI `license-discuss`** — posted, awaiting reaction. This is OSI's *general discussion* list, **not the venue for an approval request**. The steward posted there to find out whether the instrument should exist at all, before asking anyone to approve it. |
| **Not sent** | **OSI `license-review`** — the venue that actually starts an approval request. **Section B below is written for that step and has not been sent.** |
| **Not sent** | SPDX License List. SPDX asks for substantial real-world use; this text has one user. **Not meeting the condition is the reason, not the ordering** — section C below stays unsent until that changes. |
| **Text** | Frozen. `LICENSES/FROZEN.md` records the freeze and CI pins the sha256 of the three submitted artefacts. A sound criticism received during review is answered with *"that is right, and ACD-1.1 will do X"* — not by editing the text under review. |

**Section E below lists disclosures that section B does not contain.** They apply to whatever
is posted, including the license-discuss thread that is already open.

Anticipated objections and prepared answers (50 worked entries plus a table of 9 short answers, across four files) are in
`LICENSES/ACD-1.0.review-responses.md` and its `-clauses` / `-meta` / `-boilerplate` companions.

A clause-by-clause reference covering **all 82 clauses** — what each one is for, and what
breaks without it — is in `LICENSES/ACD-1.0.clause-reference.md`. If a reviewer cites a
section number, that file answers it directly.

**What actually gets said on the list is recorded in `LICENSES/ACD-1.0.discussion-log.md`.**
That file is the bridge to the next step: the review submission cites it so that the earlier
discussion is visibly accounted for rather than repeated.

---

## A. Facts you will be asked for (both bodies)

| Field | Value |
|---|---|
| Full name | Autonomous Commons Dedication 1.4 |
| Short identifier | `ACD-1.4` |
| Licence steward | Yuta Yokoi (横井雄太) |
| Canonical text | **Attached to the message as plain text.** OSI's process asks for "a copy of the license as an attachment in simple text format", and a reviewer's first response to a 2026 submission that gave only a repository link was *"we need a version that isn't subject to dynamic changes to evaluate"*. The published copy is at `https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.4.txt`, and **a reviewer can confirm the attachment is that text**: `LICENSES/FROZEN.md` pins its SHA-256 and `grep -E "^[0-9a-f]{64}  " LICENSES/FROZEN.md \| shasum -a 256 -c` checks it |
| SPDX XML | `https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.4.spdx.xml` |
| Project using it | `https://yutapr0117-design.github.io/portfolio/` (source: `https://github.com/yutapr0117-design/portfolio`) |
| OSI-approved | Not yet (this submission) |
| Reusable by others | Yes — Section 16.3 states it is not specific to any project, person, organisation, jurisdiction, or field |
| Submission category | **New License.** OSI's process defines a *Legacy License* as one "in use for at least five years by more than twenty projects maintained by different unrelated entities". ACD-1.0 meets none of the three: it was drafted in 2026, has one adopter, and that adopter is the steward. **This is the harder track and it is the correct one** (§4a) |
| SPDX identifier | **Not registered.** `LicenseRef-ACD-1.0` is the conforming expression until it is (errata E1) |
| ScanCode identifier | **None.** No ScanCode LicenseDB entry has been requested or created. Recorded here because OSI's process asks for "unique identifiers from other projects (SPDX, ScanCode)" and the honest answer to both is that there are none yet |
| Proposed tags | **None proposed.** OSI's process invites the submitter to "identify any proposed tags". This submission proposes none and accepts whatever the committee considers appropriate, which is the same position taken on category in §4a — **a submission with one adopter is not in a position to ask for a designation** |

---

### A.0 The header block, in the form this list is used to seeing

Submissions to `license-review` typically open with a short labelled block. Reproducing that shape
costs nothing and spares a reviewer from hunting for the same facts in prose. **Filled in honestly,
including where the answer is the weak one:**

```
License Name:                   Autonomous Commons Dedication
Version:                        1.4
Short Identifier:               ACD-1.4
Copyleft:                       No
Legacy or New:                  New License
Drafted By Lawyer:              No
Approved or Used by Projects:   One — the submitter's own repository
License URL:                    https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.4.txt
Steward:                        Yuta Yokoi (横井雄太)
SPDX Identifier:                Not registered (LicenseRef-ACD-1.0 is the conforming form)
ScanCode Identifier:            None
Third-party Endorsement:        None (no Debian, FSF or Fedora review)
Proposed Tags:                  None
```

**Two of those lines are the ones a reviewer will stop on**, and they are stated without
softening: no lawyer drafted or reviewed it (#1), and the only project using it is the
submitter's own (#4).

### A.1 Affirmation of OSD compliance — the owner's to make

OSI's process requires the submitter to "affirmatively state that the license complies with the
Open Source Definition", naming OSD 3, 5, 6 and 9 in particular. **The affirmation is the owner's
to make, in his own words** (decision 3b of the five, extended to this section on 2026-11-23); the
clauses behind it, criterion by criterion, are in §B.0 section 3, and
[`ACD-1.0.submission-osd.md`](ACD-1.0.submission-osd.md) sets out, for each of the ten criteria,
**where a reviewer could still argue the opposite** — the affirmation is not offered in place of that.


---

## B. OSI License Review — material for the owner's message (**not yet sent**)

> **This is the approval-request step, and it has not been taken.** Send a message only when the
> decision is to request approval, to `license-review@opensource.org` (subscribe first). OSI asks
> submitters to state the rationale, to distinguish the licence from the closest approved one, to
> address the Open Source Definition, and to say where the licence is used —
> the facts for each are below.

> **🛑 送る前に読む（2026-09-09 追加・2026-11-23 に材料の形へ書き直した）。** OSI Moderators が同日、両リストへ
> **「AI が全部または大半を書いたと疑われる投稿は拒否する」**と投稿し、両リストが
> **「AI が自律的に参加しライセンスを起草する proof-of-concept」**に使われていると述べた
> （逐語は `rounds/2026-09-09-license-{discuss,review}-osi-moderators-observed.txt`・
> 分析は `ACD-1.0.against.md` #119 と `ACD-OSI-BOTTLENECKS.md` B14）。
> **§B.0 は AI が書いた材料である。箇条を文に組んで写して送れば、その通知が名指しした行為に当たりうる。**
> 次に何を・いつ送るかは AI が決めて理由とともに記録するが、送る行為と文面の語はオーナーであり、AI はそれを代行しない。
> **開示（§E.1・§B.0 の 1）を薄めて回避してはならない。**

> **書く人への注（日本語・送る文ではない）。** (1) 沈黙を支持と読ませない（`against.md` #109）。
> (2) 「list の指摘を反映した」と書かない —— 1.0 から 1.4 への変更の由来は送る日に errata で数え直す。
> (3) 未修理を未修理と書く（errata の開いている行）。(4) この下の箇条は AI が書いた材料で、文面ではない。
> 2026-11-23 までここに在った「沈黙版（そのまま貼れる形）」の段落と §B.0 の手紙は、どちらも AI が書いた
> 送る文で、議題 3b（C′・5/0/0）で外した。commit `87c52107474d` の本 file に記録として残る。

---

### B.0 Facts for the owner's message (**1,634 words**, measured 2026-11-23 from the line after this heading to §B.1; **material, not a message to send**)

> **This is not a message.** It is a list of facts and sources, drafted by an AI, for the owner to draw on when he writes his own message to `license-review` in his own words (B14, gate 0 of `REVISION-PROTOCOL.md`). It has no greeting, no first-person sentences and no signature, on purpose. Decision 3b of the five (2026-11-23, 5/0/0) replaced the letter that stood here; that letter, drafted for ACD-1.0, is kept as a record in the history of this file at commit `87c52107474d` and is not to be sent.

**1. Disclosures that belong at the top of any message**

- No lawyer has drafted or reviewed ACD-1.4, or any earlier version.
- One project applies it: this repository (`https://github.com/yutapr0117-design/portfolio`).
- The licence text and the material in this directory were drafted by an AI agent under the owner's standing delegation; the owner set the goal and the direction and did not write the clauses. The owner read ACD-1.0 in full before posting it on 2026-08-26; whether to say the same of ACD-1.4 is for the owner to state.
- The other side, on the record: Richard Fontana, 2026-03-15, *"I'm not sure the possibility that any part of this license is AI-generated matters though."*; Josh Berkus, 2026-03-17, *"There is no requirement that the license be copyrightable."* The list moderators announced on 2026-09-09 that posts suspected of being written wholly or mostly by AI would be rejected (`review-responses-meta.md`).

**2. What OSI's review-process page asks a submission to contain — one line each, with the fact for ACD-1.4**

| OSI asks for | Fact for ACD-1.4 |
| :-- | :-- |
| Subject line | The list uses the form For Approval: followed by the licence name and version; here, Autonomous Commons Dedication 1.4 (ACD-1.4) |
| The licence text, attached as plain text | The part of `LICENSES/ACD-1.4.txt` below the line of 80 hyphens, which the file's own header names as the end of its description (*"Everything above the line below describes this file. It is not part of the Dedication (Section 1.1), and a copy may leave it out."*): 674 lines, 5,879 words, SHA-256 `ce76f3ab337c367741a6a1cea237657d371a3a193b43aa9fd2d34fdcfa8b962f`. Reproduce with `sed '1,/^-\{80\}$/d' LICENSES/ACD-1.4.txt \| shasum -a 256`. The fixed file itself is at `https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.4.txt` (fixed on 2026-11-23, SHA-256 `6792e804486e59082b84fce663d2bc24c22d72720c6d1bab8af43a90c9e3b615`, pinned in `LICENSES/FROZEN.md` and checked in CI); the attachment leaves out only its header (decision 4 of the five) |
| License name and version | Autonomous Commons Dedication, version 1.4 |
| Legacy or new | New |
| An affirmation, in the submitter's own words, that the licence complies with the Open Source Definition, naming OSD 3, 5, 6 and 9 | The clauses behind it are in section 3 below; the affirmation itself is the owner's to make |
| Any legal review, including whether a lawyer drafted it | None. No lawyer has drafted or reviewed any version |
| Projects that use it | One — `https://github.com/yutapr0117-design/portfolio` |
| Steward and contact | The owner (name and e-mail address as published on the repository) |
| Review by Debian, the FSF or Fedora | None |
| SPDX or ScanCode identifier | None; `LicenseRef-ACD-1.4` is the conforming form until it is listed. SPDX XML: `LICENSES/ACD-1.4.spdx.xml` (fixed with the text) |
| Proposed tags | None |
| The gap it fills (rationale) | Section 4 below |
| The nearest approved licence, and how this differs | Section 4 below |
| Where a reviewer can check the claims | `https://github.com/yutapr0117-design/portfolio/blob/main/LICENSES/REVIEWERS.md` |

Also useful to state: the difference from the text posted to `license-discuss` — ACD-1.0 → ACD-1.4, clause by clause, `LICENSES/REDLINE-1.0-TO-1.4.txt` (generated by `make_redline.py`; regenerate on the day of sending) — and the length: 5,879 words and 80 clauses (1.0: 4,896 words, 82 clauses); the operative terms run longer than GPL-3.0's.

**3. Open Source Definition, the criteria most likely to be raised**

- OSD 3: §4.2 grants adaptation, modification and derivative works expressly; §4.3 attaches no condition to them; §4.5 lets them be distributed *"under any terms You choose"*.
- OSD 5 and 6: §4.3 says the licence is not conditioned on who the user is or on the purpose of use.
- OSD 9: §4.3 and §10.1 impose no requirement on anything distributed with the Work.
- OSD 1: §4.1 grants a royalty-free licence; §4.2 includes distributing, selling and sublicensing; §4.3 attaches no condition.
- OSD 7: every recipient holds the grant from the Dedicator directly, with no further licence and no act of acceptance — §1.6 makes You any person exercising a permission, §4.1 grants to You, §2.3 needs no acceptance, and §4.6 says that terms a distributor adds do not cut recipients off. §8 grants the patent licence on the same footing.
- All ten, each with the strongest argument the other way: `ACD-1.0.submission-osd.md`.

**4. The gap, and how it was measured**

- What differs in effect is one combination: a patent licence that reaches models and outputs of computational use (§8.4), with no condition (§10.1) and no termination (§8.2).
- Of the 141 OSI-approved texts on SPDX List 3.29.0 (deprecated identifiers excluded), the three with no condition on the licensee — 0BSD, MIT-0, the Unlicense — never use the word *patent*, and all seven whose patent grant reaches beyond the work carry a condition (`ACD-1.0.gap-measurements.md` §1.97, §1.133).
- §6, §7 and §9 state what a broad permission may already give; they are not grounds of uniqueness. None of the 141 names machine learning or text and data mining.
- Nearest approach: CERN-OHL-P-2.0's patent licence (its §6.1) reaches Products, and its §1.4 defines a Product as what arises *"from the use, application or processing of Covered Source"*, which can be read to reach a model. It does not name models, and it has conditions (`ACD-OSI-BOTTLENECKS-B10.md`, `ACD-1.0.gap-measurements.md`).
- Nearest approved licences: in effect, the Unlicense, MIT-0 and 0BSD (and CC0, which is not approved); in patent terms, UPL-1.0, BlueOak-1.0.0 and BSD-2-Clause-Patent, each differing by one kind of condition.

**5. History on these lists**

- Licences for machine learning have been brought to the lists since at least April 2023 (the Restricted Artificial Intelligence License, withdrawn four days after submission; the Open Constitution License later that year). As of 2026-11-23 none is listed as approved; ModelGo and OpenMDW were before the Committee in 2026-09 (re-check the approved list on the day).
- Those submissions added conditions; the Restricted Artificial Intelligence License, for example, restricts uses.
- ACD-1.4 imposes no condition on You in respect of the Work (§10.1).

**6. Points a reviewer is likely to raise, with the record**

- Output: Pamela Chestek (2025-12-15, ModelGo) wrote that mentioning model output creates *"ambiguity about the legal status of the output"* and is *"not worth including"*. ACD-1.4 keeps §6.4; §6.5 gives the reason: silence *"leaves it to be inferred whether this is permitted"*, and a permission an automated system cannot determine is no permission.
- Patent scope: §8.1 reaches claims infringed by *"subject matter contained in the Work as made available by the Dedicator"* — the same kind of limitation the list has described as acceptable (Chestek, 2025-02; Perens, 2024-04), not the same words. The wording dates from 2026-08-23, before either message had been read (repository history).
- Subject matter: the Mulan Open Works Licenses were declined in 2023 on their list of covered works. §1.3 of ACD-1.4 lists audiovisual material beside source and object code; the Committee's 2021 rationale on CERN-OHL found licences not primarily for software *"appropriate for the OSI's review"* because *"they can be used for software"*.
- Structure: §3 surrenders the Covered Rights and §4 licenses the same rights independently (§4.4), so no recipient has to decide which operated. An article on OSI's site in 2017 proposed this shape; the Committee's 2020 recommendation on the Unlicense records that a dedication taken alone would not be approved.
- Moral rights: on 2024-03-23 (`license-discuss`, "Question about Blue Oak License") the chairman of Open Source Group Japan, Shuji Sado, wrote that *"the Blue Oak license is not open source, at least not in Japan. It is possible for an author to exercise author's moral rights to stop third parties from modifying the program."* — a permissive licence that grants patents but does not address moral rights. ACD-1.4 waives moral rights where the law permits (§12.1) and, for every jurisdiction, gives a covenant not to exercise them and a consent (§12.2), binding successors and anyone entitled after the Dedicator's death (§12.4). No lawyer has checked whether this works.
- Demand: Bradley Kuhn (2022) asked submitters to show a widespread need and that it is wholly unserved. The second limb is what the measurement above addresses; the first cannot be shown with one adopter.

**7. What is checked mechanically, on every pull request**

- Contiguous clause numbering, resolution of every internal cross-reference, use of every defined term, absence of the enumerated obligation-imposing and project-specific constructions, pure-ASCII text. Each is a floor rather than a proof.

**8. The earlier `license-discuss` thread (re-measure on the day)**

- ACD-1.0 was posted on 2026-08-26, and a narrower question on 2026-09-06; as of the last check (`REVIEWERS.md`, Status) neither had a reply in the public archive. A short request to discuss ACD-1.1, sent on 2026-09-17, was rejected in moderation (`LICENSES/FROZEN.md`, POSTING-NOTE; `ACD-1.0.against.md` #215), and at least three of the project's posts in all were rejected. **No version after 1.0 has reached the list.**
- Note for the writer, not a statement to send: do not present the silence as agreement (`ACD-1.0.against.md` #109).
- The changes from 1.0 to 1.4 are mostly defects found in the project's own review, some found by reviewers outside the list, and one a question put to the list and not answered: re-count by origin from `ACD-1.0.errata.md` on the day.
- Where the case against approval is collected, adverse items first: `LICENSES/REVIEWERS.md`.

---

### B.1 Reference material behind the message (**not for pasting**)

**Moved 2026-09-09 to [`ACD-1.0.submission-reference.md`](ACD-1.0.submission-reference.md).**
§1〜§5 はそこに在り、**節番号は変えていない**ので `submission-reference.md §4c` のような既存の参照は
本書ではなく参考資料の同じ節へ解決する。

**分けた理由は 2 つ。** 読み手が違う ——**この文書は送る人が読み、参考資料は審査者が読む**。
そして**同居している限り「§1〜§5 を貼るな」という警告が必要**であり、警告は分割で不要になる。
規模もある（分割前 976 行・advisory 950）。

## C. SPDX License List — the fields of the request

Submit via https://tools.spdx.org/app/submit_new_license/ (preferred) or the
`spdx/license-list-XML` new-license-request issue template. The owner writes the request;
the fields below are the facts it needs (decision 3b of the five, 2026-11-23, extended to this
section). Evidence of use, the comparison with listed licences and the steward's position are
in §B.0.

| Field | Value |
| :-- | :-- |
| Full name | Autonomous Commons Dedication 1.4 |
| Short identifier requested | `ACD-1.4` |
| Licence text URL | https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.4.txt |
| SPDX XML | `LICENSES/ACD-1.4.spdx.xml`, fixed with the text on 2026-11-23 and generated from it (`npm run spdx-xml -- --version 1.4`); a blocking CI check keeps the markup byte-identical to the regenerated output |

---

## D. Before sending — checklist for the human

1. `LICENSES/READY-TO-SUBMIT.md` exists (it is written only when the text is judged ready).
2. The published copies resolve:
   `curl -sI https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.4.txt`
3. `npm run verify` exits 0 (this proves the XML matches the text, the cross-references
   resolve, and every declaration surface agrees).
4. Subscribe to `license-review@opensource.org` before posting; the list rejects mail from
   non-subscribers.
5. **Confirm the message actually reached the list**, by finding it in the public archive —
   not by finding it in your sent folder. `https://lists.opensource.org/pipermail/license-review_lists.opensource.org/<YYYY>-<Month>.txt`,
   fetched with a browser user-agent. **This step exists because two of our substantive
   messages to `license-review` were rejected in moderation and never appeared** (`against.md`
   #128). **From the list's side, "could not send" and "did not answer" look identical**, and
   the board minutes record two submissions withdrawn for *"lack of communication with their
   submitters"* alone, with the committee holding delegated authority since 2026-05-22 to
   reject an unresponsive submitter without a board vote (`ACD-1.0.board-decisions.md` §4).
   **A submission that is not delivered is worse than one not sent**: the clock runs and the
   silence is attributed to us.
6. **Decision timing: read the rule, not the folklore.** The published rule is 60 days from
   first submission, or 30 days from a revised version but never earlier than 60 days from the
   original; the Licensing Committee has separately described *"two months from your final
   submission"*. **These do not say the same thing** and we cannot tell which governs
   (`review-rules.md` §1.82). **Measured time-to-decision, where a decision was reached at
   all, has a median of 101 days** (§1.72) — and *"not approved"* without a decision is a
   status the board has said it may leave a licence in (`board-decisions.md` §2).
7. **Fold in the license-discuss summary** (section 3 of `LICENSES/ACD-1.0.discussion-log.md`).
   Three points, not the whole log. If the log is empty, say the thread drew no response —
   that is also a fact about the licence, and stating it is better than implying a debate
   that did not happen.
8. **Re-read section E** of this file. Its disclosures apply to whatever is posted, and the
   provenance one (E.1) is the disclosure most likely to be discovered independently.
9. **The version you are submitting has been on `license-discuss` for at least 30 days.**
   Pamela Chestek advised another submitter in January 2026 to allow *"at least 30 days for
   feedback on license-discuss before submitting to license-review"*, in the same message as a
   *"hard "no""* (`review-readings.md` §1.206). Only 1.0 has reached the list so far. Give the
   date the submitted version (or its difference from 1.0) appeared in the public archive, and
   point to the section of the draft's header that lists the changes made since that posting (`OSI-APPROVAL-PLAN.md` §4, step 6b). If the posting was rejected in
   moderation, say so rather than counting the days from the attempt.
10. **No thread in the archive's list of candidates is left unread, and every reading has been
    acted on.** Re-run the census on an archive fetched that day: the unread count must be 0.
    Every reading must record where its finding went, or why nowhere, with none left "to be
    decided" (sections from 1.242 on, in a closing line; earlier ones, in a table still being
    built) (`REVISION-PROTOCOL.md` §3.6, row 6c). The owner set this on 2026-11-15: a
    submission sent while threads remain unread or unreflected is not of the quality to send.

---

## E. Addendum (2026-08-26) — disclosures that section B does not contain

Section B was written before the text was frozen and before the anticipated-objection
dossier existed. Reviewing the two against each other surfaced one disclosure that the
dossier argues is mandatory and that section B did not make.

**The hedge this addendum was written under has since been resolved, and the instruction it
gave has been carried out (2026-09-06).** It said "Section B is not rewritten here, because it
may already have been sent — or fold it into section 5 if section B has not gone out yet."
Section B has *not* gone out: what is open is a thread on `license-discuss`, nothing has been
submitted to `license-review`, and CI enforces that statement against a single source
(Check 458). So the condition for folding was satisfied and **E.1 now also appears, in shorter
form, inside section 5 — the part that would actually be sent.**

**Why that mattered.** Left as it was, the message a reviewer receives would not have said that
the licence was drafted autonomously by an AI, while the repository's own adverse list calls
that something "reviewers are entitled to weigh" (#5). A disclosure that lives only where the
reader has to go looking is not the same as a disclosure. This addendum is kept rather than
deleted, because how the omission was found and closed is itself part of the record.

### E.0 Which list this is on

If the thread is on `license-discuss`, say so plainly, and say what you want from it:

> I have posted this to license-discuss rather than license-review on purpose. I am not
> asking for approval yet. I would like to know whether this instrument is necessary at
> all, and where it is wrong, before taking anyone's time with a formal request.

### E.1 Provenance of the drafting

- **Provenance of the drafting.** Another AI told me that creating a custom licence was
  possible; **I then said that I wanted a licence of my own and that it should aim at external
  approval.** I did not write a legal specification and I did not supply a list of legal
  requirements: **I gave the goal and the top-level direction**, and the AI generated the
  concrete legal design and the text and developed it further under the standing delegation this
  repository runs on. **The name ACD-1.0, the generalised instrument, the submission packet and
  the review apparatus took shape during that delegated work, and I came to know their concrete
  state afterwards.** It is applied to **my** work. **I do not review the repository**; what
  reaches me is a summary, not the files. **The licence is the exception: I read it in full and
  understood it before sending.** I am the Dedicator and the steward and I answer for it;
  **I did not write its clauses.** The project states publicly that it
  operates this way — the human role is direction and audit, not implementation. The text cites exactly one external
  instrument (Article 4(3) of Directive (EU) 2019/790, in Section 1.10), deliberately,
  because invented or misattributed authority is the characteristic failure of
  machine-drafted legal text. Its internal consistency — contiguous clause numbering,
  resolution of all 82 cross-references, use of all 10 defined terms, absence of any
  obligation-imposing word directed at the user, and absence of anything specific to my
  project — is enforced in continuous integration, so those are conditions the repository
  cannot be in violation of rather than assertions of care. What none of that establishes
  is that the reasoning is sound, which is what I am here to find out.

> **送る文ではない注記（2026-11-11）。** 起草に使ったモデルの名前（Anthropic の Claude。
> Claude Code で動かした）と、名前を出す理由（モデルの作り手はモデルを訓練し、§6.4 と §8.4
> はそうする者に有利に働く）は、`REVIEWERS.md` の Disclosures と `SUBMISSION-MATERIALS.md`
> §1 に在る（`ACD-1.0.against.md` #319）。上の E.1 は AI が書いた材料であって、送る本文は
> オーナーの言葉で書く。そこでモデルの名前を述べるかはオーナーが決める（B14）。述べない場合も
> 上の 2 か所の開示は残るので、入口から辿る読み手には届く。

### E.2 What would cause the submission to be withdrawn

Section B explains why the licence is necessary but does not say what would end the
matter. Stating it makes clear that this is an enquiry rather than an advocacy exercise.

- If someone shows me an existing approved licence that provides all three of the
  properties in section 1, I will use it and withdraw this submission.

The fuller set of withdrawal criteria — decided in advance, so that the decision is not
made in the heat of a thread — is in `LICENSES/ACD-1.0.review-responses-meta.md`.

---

**Lost?** [`QUESTION-INDEX.md`](QUESTION-INDEX.md) indexes every worked entry in this directory by
the question it answers. [`AS-OF.md`](AS-OF.md) lists which claims about the outside world were
verified when. [`ACD-1.0.against.md`](ACD-1.0.against.md) is the case against approving this.
