---
file: LICENSES/QUESTIONS-FOR-PRACTITIONERS.md
audience: a person who builds machine-learning systems, asked to read ACD's machine-learning clauses; the steward, when asking one
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.5-DRAFT.txt (the successor draft) / LICENSES/ACD-1.4.txt (the latest fixed text, applied to this repository) / LICENSES/QUESTIONS-FOR-COUNSEL.md (the same page for a lawyer)
---

# Questions for machine-learning practitioners

**The review record asks for this reader by name.** When the OSI reviewed the first licence
written for models, a board member wrote: *"while I am an AI/ML user I am not an AI/ML system
developer, and we probably need some feedback from someone with that expertise"*, and asked for
*"someone who works in-depth on building AI systems to comment on the following clauses to see if
they are likely to be sufficiently clear and effective"* (Josh Berkus, `license-review`,
2025-02-25, on ModelGo). ACD has more clauses of that kind than ModelGo did, and no practitioner
has read them. Our own reading of them (`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.13, five roles from
ML practice) was done by the same AI model that drafted them, which is not the review that was
asked for.

This page lists five questions, each answerable on its own, about whether the words match what
practitioners actually do. It does not ask whether ACD is a good licence, or whether it conforms
to the Open Source Definition; those are the OSI's questions. It asks whether a person who builds
these systems would recognise their own acts in the words.

**Which text.** Clause numbers and quotations are ACD-1.4's (fixed on 2026-11-23; "the 1.4 draft" below
is that text before it was fixed, and the quotations were checked against the fixed text on 2026-11-24).
The 1.5 draft restates the same clauses under new numbers, and four of the five questions stay open there:

| Question | ACD-1.4 | 1.5 draft | What changed |
| :-- | :-- | :-- | :-- |
| 1 | §1.7, §15.5 | 1.9, 1.12 | Nothing in the list of uses; the example acts are fewer. |
| 2 | §1.7, §6.4, §8.4 | §1.8 | One definition, *Result*, with *"directly or indirectly"*; a copy of the Work is not a Result. |
| 3 | §8.4 | §2.3 (b) | The causal test is gone: the licence reaches a feature the Work teaches or embodies, that is extracted from its content, or that is learned from it, alone or together with other material, *"however much or little of the Work was used"*. **Would you find it easier or harder to say whether a feature was learned from a dataset than whether it results from it?** |
| 4 | §6.2, §6.3 | §3.1 | The list of signals is shorter: *"notice, metadata, protocol element, header, robots directive, or other signal"*. It no longer names markings. **Would you read those as outside it?** |
| 5 | §2.6 | §10.4 | The promise is the same and still names no standard. |

**Who wrote this page.** An AI model (Claude), working in this repository under the steward's
delegation. The licence text was drafted the same way.

---

## 1. Does the list of acts cover a real pipeline? (§1.7)

§1.7 defines *Computational Use* as *"any automated processing of the Work"*, with examples
including use of the Work *"as input to train, fine-tune, evaluate, align, distil, or otherwise
develop a machine learning model"*.

**Our reading.** The general words come first and the list only illustrates them, so an act that
is not named (retrieval at inference time, generating synthetic data from the Work, building a
vector index, an agent reading the Work as a tool result) is still covered.

**Why we doubt it.** A reader looking for their own act in the list and not finding it may take
the list as the boundary. **The 1.4 draft answers that reading:** §15.5 says that "including" and "in
particular" *"introduce examples and do not limit what precedes them"*, so the list is not the boundary in
the text. **The question:** which acts in your pipelines would you not recognise
in these words, and would you rely on the general words for them?

## 2. Do the five nouns name every artefact you produce? (§1.7, §6.4, §8.4)

In ACD-1.3 three clauses use the same closed list: *"model, parameter set, weight, embedding, or
output"*.
§6.4 says no claim arises in respect of them; §8.4 grants a patent licence for them.

**Why we doubt it.** A reviewer has already warned that *"the vocabulary for AI is fluid and
constantly changing"* (Pamela Chestek, 2025-12-06, `reviewer-positions.md` §1.159). Adapters
(LoRA weights), quantised or merged checkpoints, a key-value cache, a vector index, a reward
model, an agent's tool configuration, or a dataset distilled from model outputs may or may not
be one of the five. **The question:** which artefacts would you put outside all five, and is
there a word that would cover them without reaching things that are not artefacts of processing?

**The 1.4 draft answers this part (trial T95).** The list in §1.7, §6.4 and §8.4 now ends *"output, or
other data"*, so every artefact above that is data is named, while a physical product made from an
output is left out on purpose, because §8.4 would otherwise grant a patent licence to manufacture it.
*"artefact"* was tried first and dropped for that reason. **What remains:** is there an artefact of
processing in your work that is neither data nor an output?

## 3. Can anyone tell whether a model's feature "results from" the Work? (§8.4)

§8.4 reaches a patent claim *"only where the feature that infringes it results, in whole or in
part, from the content of the Work; a feature that the Work teaches or embodies is taken so to
result"*, and says *"That is a question of causation and not of quantity: no threshold of how much of
the Work was used is imposed."* (ACD-1.3 gave the reason in the text: *"since You could not determine
whether one had been crossed"*; the 1.4 draft dropped it in trial T80.)

**Why we doubt it.** The clause drops a quantity test, which a user cannot measure, and uses a causal
test instead. Whether a capability of a trained model results from one document in its
training data may be no easier to establish. **The question:** in your experience, can a model
builder, or a court with expert help, decide that a feature results from particular training
content? If not, does the second half (*"teaches or embodies"*) do the work on its own?

## 4. Which signals would your crawler or loader read as an opt-out? (§6.2, §6.3)

§6.2 says that *"no notice, marking, metadata, protocol element, header, robots directive, or
other signal associated with the Work is to be read as a Reservation"*, so far as the Dedicator's
rights are concerned, and §6.3 withdraws one the Dedicator made.

**The question:** which signals do your systems actually read (robots.txt and its AI-specific
user agents, `ai.txt`, TDMRep, licence fields in a model card or dataset card, C2PA assertions,
HTTP headers), and when a work carries both this Dedication and such a signal, would your system
see the Dedication at all? If it would not, the clause speaks to a court but not to the machine
it is written for (§6.5: *"a permission that an automated system cannot determine is … no
permission at all"*).

## 5. What form would let a loader find the material this Dedication does not cover? (§2.6)

§2.6 asks a Dedicator who includes excluded material to identify it *"so that a person or an
automated system reading the Work can determine what this Dedication does not cover"*. It does
not say how.

**The question:** what would a dataset or model loader you use actually read — an SPDX
expression per file, a REUSE `.license` file, a field in a dataset card, a manifest — and should
the text name one, or is naming none the right choice because the formats change?

---

## How to answer

Any of the five, in any length. Public answers on `license-discuss` are recorded verbatim in
`rounds/`; a private answer is recorded only as a dated stub (`rounds/README.md`), and nothing
from it is quoted. An answer that a clause does not match practice goes to the draft as a trial
(`ACD-1.4-SECOND-CLARITY-TRIAL.md`) with the answer as its source, and, if the frozen text has the
same words, to `ACD-1.0.errata.md`.
