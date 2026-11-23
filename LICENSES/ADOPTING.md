---
file: LICENSES/ADOPTING.md
audience: anyone thinking of applying ACD to their own work
last-updated: 2026-11-23
canonical-ref: LICENSE (names the version this repository applies) / LICENSES/ACD-1.0.faq.md (the adopter's questions in full) / LICENSES/ACD-1.0.comparison.md (the alternatives) / LICENSES/ACD-1.0.against.md (the adverse record)
---

# Before you apply ACD to your own work

**Read this first. It is short, and you should treat the decision as final.** ACD is written so that anyone
can apply it to any work without asking us. For most projects an approved licence is the better
choice. Section numbers below are the same in every version unless the page says otherwise.

## What you cannot get back

- **The text gives you no way to take it back.** Nothing in it lets you end the surrender in §3 or
  the licence in §4.1, and what you have given stays given (§2.2). In the United States, 17 U.S.C.
  §203 may still reach the licence ([`ACD-1.0.jurisdictions.md`](ACD-1.0.jurisdictions.md) §5a).
  If the law treats the act as a gift, Germany lets a donor revoke it against a recipient guilty of
  gross ingratitude, a right that cannot be waived in advance; France allows revocation only in three
  serious cases its civil code lists, and requires a gift to be notarised (§3 of the same file). Japan
  lets a gift not made in writing be cancelled except for what has already been delivered; we read the
  published text as a writing ([`QUESTIONS-FOR-COUNSEL.md`](QUESTIONS-FOR-COUNSEL.md) question 9). Either
  way it reaches that recipient only, and no lawyer has checked how it applies here.
- **You give up credit.** Nobody has to keep your name or any notice (§10.2).
- **You give up more patent rights than most licences ask.** The patent licence has no condition
  and you cannot terminate it (§8.2), and it reaches models and outputs that result from using the
  work (§8.4). If you hold a patent on a method your work explains, read
  [FAQ A32](ACD-1.0.faq.md) before you apply it.
- **You cannot answer a patent suit by ending the suer's rights.** Retaliation clauses are absent,
  and a competitor can take the work and still sue you (`ACD-1.0.against.md` #174).
- **If you serve copies from your own server, read §5.2 first.** In 1.0 to 1.3 you covenant not to
  *apply* any technological measure that restricts access to the work. Read on its words, that reaches a
  rate limit, a proof-of-work check or a crawler block on your own download server (errata
  [E82](ACD-1.0.errata.md)). ACD-1.4, fixed on 2026-11-23, drops *apply*: you may put such measures on
  your server and promise only not to assert rights in them or use anti-circumvention law against
  people who get round them. It also authorises anyone to get round a measure that you apply to a copy
  of the work, in a use the Dedication permits, and waives any power such a law gives you to forbid that
  (§5.2, the paragraph after (d)). A measure on your server can slow people down, but as far as your own
  rights go it cannot stop them. If you apply 1.0 to 1.3, the safer course is still to let a host you do
  not operate serve the copies (`ACD-1.0.against.md` #171 reads a host's own measures as outside the covenant). In
  every version the covenant reaches *"any law concerning the circumvention of such measures"*;
  whether that includes the law against unauthorised access to a computer, if someone gets round
  your server's defences, is open and is one of our questions for a lawyer
  ([`QUESTIONS-FOR-COUNSEL.md`](QUESTIONS-FOR-COUNSEL.md)).
- **If you also run the work as a service, your terms cannot restrict a copy of it that reaches your users.**
  In ACD-1.4, §5 leaves alone your rights in other material you make, and the terms of a service through
  which you run the work without handing out a copy. But where such material contains a copy of the work
  or of part of it, §5 reaches your terms to the extent they restrict what may be done with that copy
  (§5.2, final paragraph); we read a service's output as such material. Who may use the service, and a
  payment for it, stay yours (§5.2(b)). 1.0 to 1.3 have no such carve-out: their §5.2(b) bars any
  obligation in respect of the work imposed by terms of service, without exception for a service.
- **Check your site's terms of service before you apply it.** In every version, §5.2(b) is a promise not to
  impose, by contract or terms of service, any obligation in respect of the work that the Dedication does
  not impose itself, except under your trademarks or name and for a payment. A clause such as "do not imply
  that we endorse you" is within that exception only if it rests on your name or marks; a bare "do not
  misrepresent the work" is not, and would break the promise as to the work (errata
  [E87](ACD-1.0.errata.md)). You do not need such a clause: the law against false statements and false
  endorsement still applies, and the Dedication leaves it alone (§5.1, §11.3). We decided not to change
  the text, because the line it draws is that the law stays and no new contractual obligation is added.

## What nobody can tell you yet

- **No lawyer has read this text**, and no court has tested it. If it matters to you, take advice.
- **It is not OSI-approved** and not on the SPDX License List, so scanners may call it unknown
  ([FAQ A11](ACD-1.0.faq.md)).
- **No independent project is known to use it.** You would not have anyone else's experience to
  rely on.

## When something else is better

- **Your work is ordinary software, you hold no patents, no text-and-data-mining opt-out is in play,
  and authorship is not in doubt**: 0BSD or MIT-0. They are shorter and approved, and scanners
  recognise them.
- **You want an express patent grant and can accept one notice condition**: BlueOak-1.0.0,
  UPL-1.0 or BSD-2-Clause-Patent.
- **You want changes to stay open**: a copyleft licence.

[`ACD-1.0.comparison.md`](ACD-1.0.comparison.md) gives the reasons. ACD earns its place only in the
narrow band where those assumptions fail together.

## How to apply it

1. **Check that you hold the rights.** Your employer may hold them ([FAQ A20](ACD-1.0.faq.md)).
   If other people contributed, read [FAQ A13](ACD-1.0.faq.md).
2. **Copy the text unchanged.** Use the version named in this repository's root
   [`LICENSE`](../LICENSE), which is the latest fixed version we apply ourselves. The header above
   the dividing line describes this repository's file and is not part of the Dedication (§1.1), so
   your copy may leave it out.
3. **Add the notice** from §16.1 of that text, with the location of your copy.
4. **Mark anything the Dedication does not cover.** If your work includes material under other
   terms, §2.6 has you identify it in a form that travels with the work, so that a person or a
   program can tell what is excluded. The text names no standard; forms that say *which* material
   is excluded include a per-file `SPDX-License-Identifier`, REUSE's `.license` files or
   `REUSE.toml`, and the `license` field of a dataset or model card naming the files it covers. A
   single licence expression for a whole package says which licences are mixed in, not where.

**If you only mention ACD, say so.** In your own work, the identifier (`ACD-1.4`), an SPDX tag, or
the name with its version can be read as a notice that applies the text to the material it
accompanies (Section 16 of the 1.4 draft, on notices). A README that names ACD only to compare it with other licences should name it without
a version, or say in the same sentence that the work is not under it. Section 16 speaks of a notice that
a Dedicator places, so an article or a comparison table about other people's work does not apply
ACD to that work; that is our reading, and no lawyer has checked it.

There is nothing to register, and you do not need to tell us.

**If you use it or plan to, and are willing to say so publicly,
[this form](https://github.com/yutapr0117-design/portfolio/issues/new?template=acd-use.yml) helps.** Use by a project is the
one thing the steward cannot supply. OSI's committee has said of another licence that one project
using it or expressing interest would lift a hold. Say so only if it is true.

**This page is not legal advice.** It was written by an AI model (Claude, an Anthropic model)
working under the steward's delegation. The licence text was drafted the same way, to a goal the steward set, and he read
ACD-1.0 in full before posting it. Neither has been reviewed by a lawyer.
