---
file: LICENSES/ACD-1.0.errata.md
audience: OSI license-discuss / license-review participants, licence reviewers, a future 1.1 drafter
last-updated: 2026-09-05
canonical-ref: LICENSES/ACD-1.0.txt (frozen text) / LICENSES/FROZEN.md (freeze + digests) / LICENSES/ACD-1.0.against.md (the full adverse case)
---

# Known defects in ACD-1.0, and why none of them is fixed

**Thirteen items are recorded, and all thirteen are unrepaired, deliberately.** ⚠ **Until 2026-09-09 this
sentence said "Seven items … five imprecisions … All five are unrepaired" while the table below held
ten.** The correction is recorded rather than swapped in silently, because **a page whose purpose is
to list our known defects was understating how many we know** — the same direction of error, and the
same worst direction, as `against.md` #58. The count is now derived from the table and checked in CI
(Check 460 face (l)). This
page exists so that the list is public before anyone else compiles it, and so that "the text is
frozen" reads as a discipline rather than as a way of not answering.

## Why nothing is fixed

The text is frozen for the duration of the `license-discuss` thread, and CI pins the SHA-256 of
`ACD-1.0.txt`, `ACD-1.0.spdx.xml` and `ACD-1.0.machine.json` (Check 453) so that an accidental
edit fails the build. Editing wording underneath a live discussion would mean reviewers were
reading one text and commenting on another — their review would be of something that no longer
exists. A defect found now is therefore **reported and left in place**.

Verify the freeze rather than taking it on trust:

```sh
grep -E "^[0-9a-f]{64}  " LICENSES/FROZEN.md | shasum -a 256 -c   # expect 3× OK
```

## The list

| # | Clause | What is imprecise | What 1.1 would do | Severity |
|---|---|---|---|---|
| E1 | **§16.1** | The recommended notice instructs adopters to write `SPDX-License-Identifier: ACD-1.0`. SPDX has not assigned that identifier; the conforming form for an unregistered licence is `LicenseRef-`. A notice written exactly as directed is not SPDX-conforming | Either use the `LicenseRef-` form until registration, or say in the clause that the bare identifier presumes registration | **Highest.** It is the one place where the text instructs a reader to do something incorrect |
| E2 | **§16.3** | "may be applied by anyone, to any work, without permission from ... its authors" is broader than the point it exists to make. §2.7 keeps the effect honest, but the sentence invites applying the notice to works one does not own, and the party harmed is the **downstream recipient** who relies on the signal | Add "in which they hold rights", which preserves the reusability point (submission §4b depends on this clause) and drops the invitation | High |
| E3 | **§16.1 notice wording** (and the same sentence carried into `ACD-1.0.machine.json`'s `notice` field, so the fix touches two frozen files) | The notice says "no conditions are imposed" without §10.1's qualifier "in respect of the Work". §16.4 does restrict redistributing the licence *text* under its name, so the shorthand reads as contradicted three lines later | Carry the qualifier into the notice | Medium — the text is consistent; only the summary is loose |
| E4 | **§6.4** | "No model ... is encumbered by this Dedication or by any Covered Right of the Dedicator" states the result in a form that can be read as denying that any right subsists, rather than as saying no enforceable claim remains. §6.5 makes §6 declaratory of §3–§5, so the operative effect is right | Say "no enforceable claim arises" | Medium |
| E8 | **§16.4 and machine-readable re-encoding** | §16.4 permits copying the text verbatim and forbids distributing it "in modified form under the name ... or under the identifier 'ACD-1.0'"; §16.5 carves out translations and nothing else. `ACD-1.0.spdx.xml` — the artifact SPDX registration requires — carries `licenseId="ACD-1.0"` and the full name, and is **not verbatim**: every clause is reflowed into a `<p>` element with the line breaks and indentation of the fixed text removed, and the standard-header element carries an `<alt match=".+">` substitution point. On a strict reading the registration path requires producing what §16.4 prohibits; on a sensible reading a re-encoding is not a modification. **The text does not say which** | Say in §16.4 that a rendering preserving the words in a different encoding (registry XML, structured metadata) is not a modified text, on the same footing as §16.5's translation | **Medium-high — the only entry here that touches the submission path itself.** Nothing about the Work changes; what is unresolved is whether the licence permits the form in which registries must carry it. §6.5 — a permission an automated system cannot determine is not a permission — is the strongest reason this should have been stated rather than inferred |
| E6 | **§8.4** | The grant reaches claims infringed by "any model, parameter set, weight, embedding, or output" resulting from Computational Use, and deliberately drops §8.1's proviso limiting infringement to subject matter contained in the Work. Whether it needs to reach *outputs* as well as the *use of the Work in training* is an open drafting question — the narrower form might close the same gap at lower cost to patent-holding adopters | Consider splitting the grant: claims infringed by computational use of the Work, and separately claims infringed by the resulting model, so an adopter can see which is which | **Open question, not a defect.** The current text is coherent and its breadth is stated; what is unresolved is whether a narrower form would do the same work |
| E7 | **§11.1 と §16 の読み順** | §11.1 states that no right is granted in any trademark or name; §16.2 then makes the name and identifier carry legal effect, and §16.4 regulates their use. The reconciliation exists — §10.5 and §16.6 confine §16 to the licence text as a document — but it sits between the two, so a reader who meets §11.1 first can reasonably think §16 asks for something §11 withheld | Add a cross-reference in §11.1 pointing at §10.5, so the resolution is available at the point the apparent conflict arises | **Low — a reading-order problem, not a substantive one.** Nothing about what anyone may do changes. It is here because `against.md` #45 called it a 1.1 candidate and the candidate had no entry to point at |
| E9 | **§10.4, second sentence — scope** | Every neighbouring clause in the no-condition mesh is qualified: §10.1 says "in respect of the Work"; §10.5, §11.3 and §11.4 each say a clause is "not a condition upon Your use of the Work"; §16.6 says §16.4–16.5 "bind no recipient of the Work". §10.4's second sentence is not: it says flatly that the Dedication "contains nothing that You could breach". But "You" is defined at §1.4 as **any person or entity exercising permissions under this Dedication**, §16.4 grants a permission over the text, and §16.5 states in terms that its proviso **is** "a condition upon distributing the translated text" | Qualify the sentence as its six neighbours are — "nothing that You could breach in respect of the Work" | **Low, and narrow.** Nothing about what anyone may do with the Work changes. It is the one unqualified sentence in a mesh that is qualified everywhere else, and a reviewer following the **defined term** rather than the section arrives at it |
| E10 | **`ACD-1.0.machine.json` — the one restriction is the one thing not described** | The descriptor's `reservationsAndLimits` names six things the instrument does *not* do (TDM reservation, patent retaliation, field-of-use restriction, termination, trademark grant, governing law). **All six are absences.** The one thing the document actually restricts — redistributing the licence *text* in modified form under its name or identifier (§16.4), with the translation proviso (§16.5) — has no key, while the *permission* side of §16 does (`reusableByAnyone` → §16.3). A consumer built on the descriptor concludes the document restricts nothing at all; that is true of the Work and false of the text. The file's own last line, "Any adopter may copy this file verbatim", **is §16.4 applied to itself, stated as a permission rather than as a limit** | Add a `textRedistribution` entry under `reservationsAndLimits` citing §16.4 and §16.5, so the descriptor carries §16's limit as well as §16's permission | **Low–medium, and narrow.** No user of the Work is misled about their own obligations (§16.4 binds no recipient — §16.6), and scanners rarely model restrictions on a licence text at all. It is here because §6.5's reasoning cuts both ways: **a restriction an automated system cannot determine is one it will breach without knowing.** `machine.json` is pinned by Check 453, so this cannot be corrected while the freeze holds |
| E5 | **§2.9** | "and so is not executory" asserts a classification that a forum's insolvency law determines, not the document. The clause does give the supporting facts first — no continuing obligation on either side — which is the strongest thing a text can do | State the facts and stop; let the conclusion follow | Low — form, not substance |
| E11 | **§4.4, second sentence — whether it describes the successful-dedication case accurately** | The sentence reads *"Where Section 3 is effective, this Section is redundant but not void, and it remains available to be relied upon by You."* **Two readings are possible and the steward put both to `license-discuss` on 2026-09-06.** *Reading A*: §4.1 is a present, unconditional grant whose existence never depended on §3 failing, so where §3 succeeds the grant is merely redundant and the prior independent grant is not invalidated. *Reading B*: the grant is independent, **but once a Covered Right has actually been surrendered there is no longer an exclusive right for a licence to operate on**, so saying the licence "remains available to be relied upon" over that right may be inaccurate. **The recipient-facing result is identical under both** — if the right is gone permission is unnecessary, if it remains §4.1 supplies it — **so this is about whether §4.4 describes the legal route correctly, not about whether anyone is free.** | Two possibilities, and which one applies is exactly what was asked on the list: **(1) architectural** — a dedication and an unconditional present licence should not be structured as independent concurrent footings at all; or **(2) drafting** — the architecture is sound and §4.4 simply claims too much about continued operation over rights that no longer exist, in which case the fix is to state the independence and stop. **Not decided here.** The steward said in terms that if the present wording is already coherent he would rather leave the fixed text alone than revise it unnecessarily | **Open.** This is the only entry raised by the steward on the list rather than found in-house, and the only one whose disposition waits on an answer from outside |
| E12 | **§16.1 の推奨 notice、同じ 1 文の前半 —— "No rights are reserved"** | E3 は同じ文の**後半**（*"no conditions are imposed"* に §10.1 の限定「in respect of the Work」が無い）を記録した。**前半は見ていなかった。** *"No rights are reserved"* にも対応する限定が無い —— **§11.1 は商標・サービスマーク・商号・ロゴ・人名についていかなる権利も与えない**（これらは Dedicator が現に保有する権利である）し、§11.4 はデータ保護・プライバシー・パブリシティについて何も与えない。**厳密に読めば「Covered Rights は何も留保されていない」であり §1.5 がその集合を定義するので、条文としては整合している**が、**notice は定義を持って行かない。** 同じ文言は `ACD-1.0.machine.json` の `notice` フィールドと、適用宣言 `LICENSE` の 4 行目にも在る —— **operative 条項・機械可読層・利用者が最初に読む面の 3 つ**で、前文（#114）より重い位置である | E3 と同じ —— **限定を notice へ持って行く。** 「Covered Rights は留保されていない」と書けば §11.1 と両立する。**手本は同じリポジトリの中に在る**: 適用宣言 `LICENSE` は同じことを *"nothing here is withheld from anyone: **no approval is required, from anyone, for any use**"* と書き、**コロンで「使用について」と限定している**。さらに虚偽の推奨については別段落で *"not as a restriction placed on you, but because **no licence can make a false statement true**"* と説明している。**同じリポジトリが、片方の面では正確に書き、もう片方では要約している** | **Open。** #115。**E3 を見つけた時に同じ文の前半を見なかったこと自体が、この errata の中身より重要である** |
| E13 | **§1 の並び順 —— 定義が 3 回、後で定義される語を使う** | §1.2 が §1.3 の "Dedicator" を、§1.3 が §1.5 の "Covered Rights" を、§1.5 が §1.6 の "Moral Rights" を使う。**上から順に読む読者は、定義される前の語に 3 回出会う。** 内容は正しく、Check 441c が「定義語はすべて使われている」を強制しているが、**読む順は誰も見ていない**（#101 が §16 で記録したのと同じ族）。**"Work" と "Dedicator" は相互定義**だが、両者とも §16.1 の notice を置くという**定義の外にある行為**に錨を下ろしているので悪循環ではない（MIT / Apache-2.0 も同じ形）| **並べ替えで 3 件のうち 2 件は消せる**（"Moral Rights" と "Covered Rights" を先に置く）。**相互定義の 1 件は原理的に消せない**ので、そこは残す。あるいは §1 の冒頭に「定義は相互に参照する。順に読む必要はない」の 1 文を置く | **Open。** 実害は読みやすさに限られ、意味は変わらない |

## What the machine-readable layer got right

The two machine-readable artefacts are frozen alongside the text, so they were audited rather
than corrected. They came out **cleaner than the human-facing notice**:

- `ACD-1.0.machine.json` records `osiApproved: false` and `spdxListed: false`, is marked
  `NON-OPERATIVE` with the text prevailing, and its `notice` field **omits** the SPDX identifier
  line — so E1 does not propagate there. E3 does, and that is now noted in the row above.
- `ACD-1.0.spdx.xml` records `isOsiApproved="false"`.
- Every one of the **29** `clause` pointers in the descriptor resolves to a clause that exists
  and is about the subject claimed. Verify it by cross-checking the `clause` fields against
  `ACD-1.0.txt`; the result is 29/29.

That asymmetry is itself the lesson for 1.1: the machine-readable files say "not approved, not
listed" in the same breath as the identifier, and the human notice does not. **The notice should
borrow the honesty of the descriptor**, not the other way round.

## What is *not* on this list

No defect has been found that changes what a recipient may do. Every entry above is a matter of
precision, scope of wording, or the form in which a conclusion is stated. If a defect of the
first kind is found, it goes here immediately and the honest response may be to withdraw rather
than to patch — `ACD-1.0.submission.md` §E.2 and `ACD-1.0.against.md` record the conditions.

Two of these were found by a third party's adversarial reading and three by auditing the
dossier's own citations against the text. Neither route was exhaustive. **If you find a sixth,
that is a failure of our review and not of yours** — say so on the list and it will be added
here rather than argued with.

## When the freeze lifts

On the day the freeze is lifted — that is, when the discussion closes and the owner says so — the
correct order is: apply E1 first (it is the only one that misdirects a reader), re-measure every
property recorded in `ACD-1.0.submission-reference.md` §4c, regenerate the digests in `FROZEN.md`, and
record in `ACD-1.0.discussion-log.md` which changes were driven by which feedback. A property
verified once is not a property that stays true.

---

**Lost?** [`QUESTION-INDEX.md`](QUESTION-INDEX.md) indexes every worked entry in this directory by
the question it answers. [`AS-OF.md`](AS-OF.md) lists which claims about the outside world were
verified when. [`ACD-1.0.against.md`](ACD-1.0.against.md) is the case against approving this.
