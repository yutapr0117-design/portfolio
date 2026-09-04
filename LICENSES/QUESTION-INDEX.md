---
file: LICENSES/QUESTION-INDEX.md
audience: OSI license-discuss / license-review participants, licence reviewers
last-updated: 2026-09-04
canonical-ref: LICENSES/REVIEWERS.md (entry point) / LICENSES/ACD-1.0.against.md (the adverse case) / LICENSES/ACD-1.0.txt (authoritative text)
---

# If you were going to ask — where the answer already is

There are 130 worked entries across this directory. This page exists so that you do not have to
find them by guessing which filename they are in. **It is organised by the question, not by the
document.**

If your question is not here, that is our omission and worth saying on the list.

## The ones most likely to come first

| Question | Where |
|---|---|
| If nobody has to keep the notice, is your warranty disclaimer worth anything? | **Weaker, yes — and the loss is ours.** `review-responses-clauses.md` §15/§16; `submission.md` §1b. Permissions are unaffected; the disclaimer is |
| Isn't this "not a licence" at all? | `submission.md` §1b — the argument made against the Unlicense in 2020. §4.1 says "grants You a licence" in terms, which is more than the Unlicense had to work with |
| Isn't a public domain dedication outside what OSI reviews? | `submission.md` §1b — with the Unlicense precedent and the two ways it cuts against us |
| So this is a dedication with a licence bolted on as a fallback? | **No.** §4 is granted independently of §3 and does not wait for it to fail (§4.4). `clause-reference.md` §4.4 row; `review-responses.md` §2 |
| Has a lawyer read it? | **No.** `submission.md` §5 and §4c; `against.md` #1 — it is the weakest point and is stated without hedging |
| Who wrote it? | An AI, autonomously, under a standing delegation. The owner did not commission it and learned of it afterwards; he read the full text before sending. `submission.md` §E.1; `against.md` #5 |
| How many people use it? | **One repository.** `submission.md` §5; `against.md` #4. Reusability is shown structurally in §4b — a different property from adoption |
| CC0 was stopped by OSI — why would this be different? | `comparison.md` §1.4 — the 2012 objection was the **patent carve-out** (weakening estoppel; putting users on notice), and §2.5 and §8.3 are built against exactly those two. **It does not follow that this clears the bar CC0 did not** |
| Why not just use MIT-0, 0BSD, CC0 or Apache-2.0? | `comparison.md` §1 — including **when those are the better choice**, which is most of the time |
| Doesn't OpenMDW or ModelGo already do this? | `comparison.md` §1.5 — adjacent, not the same question; and where they are better than this one. `against.md` #28, #31 |
| Suppose they do add AI terms — what is left? | `comparison.md` §1.35 — **four of six distinguishing features would close**; two would not (it does not presume a right exists; it imposes no condition). With the costs of that structure listed beside them |
| Won't GPL or Apache just add AI terms in their next version? | `comparison.md` §1.3 — **checked**: FSF and ASF are responding through criteria and guidance, not licence text, and no GPLv4 is announced. **If that changes, the section gets rewritten, not defended** |
| Is this just licence proliferation? | The honest answer is that it is not obviously not. `comparison.md` §1 closing; `against.md` #28, #33 |

## Conformance

| Question | Where |
|---|---|
| Does it meet each OSD criterion? | `submission.md` §3 — all ten, individually |
| Where is each criterion arguable? | `submission.md` §3b — the counter-argument for all ten, written by us. **OSD 7 is the one we expect to be litigated** |
| You grant over several kinds of right — do you react to litigation over all of them? | **There is nothing to react with.** §10.4 terminates nothing; §8.2 says the absence is deliberate. `review-responses-clauses.md` §15/§16; the cost is `against.md` #16, #46 |
| How would your conditions work for a hosted API where nothing is transferred? | **There are no conditions to work.** §10.1 / §4.3; §16's conditions bind the licence text only (§10.5, §16.6). `against.md` #47 |
| Does §5.2's anti-DRM covenant restrict the user? | No — it binds the Dedicator. `review-responses-clauses.md` Q26 |
| Does §16.4's name restriction breach OSD 4? | No — §10.1 is limited to conditions "in respect of the Work"; §16.4 governs the licence text. `against.md` #27; the loose shorthand is errata E3 |
| §11 says no trademark right, but §16 makes the name carry meaning — which is it? | **Both, and §10.5 / §16.6 are the join.** §16's conditions bind the licence text, not the Work. `clause-reference.md` — the six clauses that disclaim being conditions form one mesh |
| Does §11.3 (no false attribution) discriminate? | No — it states a limit of reach, and says so in terms. `clause-reference.md` §11.3 row |

## The text itself

| Question | Where |
|---|---|
| Is there any condition anywhere in this instrument? | **One, and the text names it itself.** §16.5 conditions *distributing a translation of the licence text* on identifying it as a translation — and says in terms that this is not a condition on any use of the Work (§10.5). `clause-reference.md` |
| Why is the same protection expressed three different ways? | Deliberate layering: surrender (§3), licence (§4), covenant (§5) — and §8.6 gives patents the second footing, §12.2 does the same for moral rights. `clause-reference.md` |
| What does each of the 82 clauses do? | `clause-reference.md` — one row per clause, checked against the text (82/82) |
| Are there known defects? | **Five.** `errata.md` — with severity, what 1.1 would do, and why none is fixed |
| §16.1 tells adopters to write an unregistered SPDX identifier | **Correct, and it is the highest-severity item.** `errata.md` E1; `review-responses-clauses.md` §15/§16 |
| §2.9 declares its own insolvency classification | `against.md` #21 — facts before the conclusion is right; asserting the conclusion is not |
| §6.4 says outputs are "not encumbered" in absolute form | `against.md` #22 — §6.5 makes §6 declaratory, so the effect is right and the phrasing is loose |
| §8.4's patent grant looks very broad | It is, and that is a cost to adopters with patents. `against.md` #16 |
| §16.3 invites applying the notice to anyone's work | `against.md` #20; errata E2 — §2.7 bounds the effect, but the wording is wider than needed |
| Isn't it premature to licence AI-generated material when its legal status is unsettled? | `review-responses-clauses.md` §15/§16 — the strongest objection to §9, and largely right **against instruments that assume a right exists**. §9 is built the other way round |
| Do you meet the practical submission requirements (existing users, SPDX id, endorsements)? | **Three of them, no.** `review-responses-meta.md` Q32b — stated as not met rather than argued around |
| Is the name misleading? | `review-responses-meta.md` Q14 and Q32c — no existing licence's name or identifier is used, and §16.4 applies the same rule to this one |
| Why is it 16 sections and 82 clauses? | `review-responses-meta.md` Q17 — an accepted cost, argued against the opposite failure |

## Machine learning, TDM, patents, data

| Question | Where |
|---|---|
| Is §6 a policy position about AI training? | **No** — it is a statement about the Dedicator's own rights. `submission.md` §1c |
| Does it purport to defeat someone else's TDM reservation? | No. §6.2 is limited to the Dedicator's rights; §6.3 handles others' within §2.7. `review-responses-clauses.md` §6 |
| Does it license trade secrets? | **No** — §1.5 does not reach them. OpenMDW does. `against.md` #31 |
| What about sui generis database rights? | §7, in the Database Directive's own vocabulary. `clause-reference.md` §7 rows |
| Does it reach models, weights and outputs? | Yes — §8.4 for patents, §6.4 for encumbrance. `comparison.md` §1.5 |
| Does it carve out distillation? | **No**, unlike ModelGo. `comparison.md` §1.5 — the one axis where the three are in real tension |

## Jurisdictions and effect

| Question | Where |
|---|---|
| What happens where abandonment is ineffective? | `jurisdictions.md` — questions, not conclusions, by jurisdiction |
| Germany specifically? | `jurisdictions.md` §3 — including that §15.4's reformation may not be available there, and why the outcome holds anyway |
| Moral rights in France? | `jurisdictions.md` §4; §12.1/§12.2 are a two-step, not a single waiver |
| Does it warrant that it works? | **No** — §13.2 says so expressly. `against.md` #26 |
| What if the Dedicator dies, or the rights are sold? | §2.8 and §12.4 bind successors. `faq.md` A27 |
| Consumer-protection law? | `faq.md` A24 — some of §13/§14 may not survive contact with it, and §14.2 anticipates that |

## Using it

| Question | Where |
|---|---|
| How do I apply it? | §16.1 — but see errata E1 for the SPDX line |
| How do I write it in an SBOM while unregistered? | `faq.md` A10, A16 — `LicenseRef-ACD-1.0` |
| Can I relicense derivatives under anything? | Yes. `faq.md` A23 — and what that does *not* change upstream |
| Multiple rightsholders? | `faq.md` A26 — each applies for what they hold; §2.7 keeps it honest |
| Research and teaching? | `faq.md` A25 — nothing required, but licence terms are not citation norms |
| Images, audio, embedded metadata? | `faq.md` A22 — all in scope; fonts loaded from elsewhere are not |

## Process

| Question | Where |
|---|---|
| What has actually been submitted, and where? | `REVIEWERS.md` — discussion only; nothing to license-review, nothing to SPDX |
| Why discussion first? | OSI's guidance, not our foresight. `discussion-log.md` §3.5 — including that we described this wrongly once |
| What happens when feedback arrives? | `REVISION-PROTOCOL.md` — verbatim archive, then decomposition; **1.0 is never mutated** |
| What would make you withdraw? | `submission.md` §E.2; `against.md` closing section |
| How long do you expect this to take? | We do not set a figure. `submission.md` §4a — the two comparable submissions point opposite ways |
