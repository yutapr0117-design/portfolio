---
file: LICENSES/ACD-1.0.submission.md
audience: OSI license-discuss / license-review participants, SPDX submitters, the human who sends the message
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.txt (the text being submitted) / LICENSES/REVIEWERS.md (English entry point) / LICENSES/ACD-1.0.against.md (the adverse case)
---

# ACD-1.0 — submission packets (English, ready to paste)

> **What this file is.** Everything a human needs in order to submit the Autonomous
> Commons Dedication 1.0 to the SPDX License List and to OSI License Review, written in
> the language those bodies use, so that the human-only step is *send*, not *compose*.
>
<!-- SUBMISSION-TARGET: ACD-1.0 -->
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

> **Status of the licence itself:** see `LICENSES/ACD-1.0.txt`. The rationale, the
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

Anticipated objections and prepared answers (47 worked entries plus a table of 8 short answers, across three files) are in
`LICENSES/ACD-1.0.review-responses.md` and its `-clauses` / `-meta` companions.

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
| Full name | Autonomous Commons Dedication 1.0 |
| Short identifier | `ACD-1.0` |
| Licence steward | Yuta Yokoi (横井雄太) |
| Canonical text | **Attached to the message as plain text.** OSI's process asks for "a copy of the license as an attachment in simple text format", and a reviewer's first response to a 2026 submission that gave only a repository link was *"we need a version that isn't subject to dynamic changes to evaluate"*. The published copy is at `https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt`, and **a reviewer can confirm the attachment is that text**: `LICENSES/FROZEN.md` pins its SHA-256 and `grep -E "^[0-9a-f]{64}  " LICENSES/FROZEN.md \| shasum -a 256 -c` checks it |
| SPDX XML | `https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.spdx.xml` |
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
Version:                        1.0
Short Identifier:               ACD-1.0
Copyleft:                       No
Legacy or New:                  New License
Drafted By Lawyer:              No
Approved or Used by Projects:   One — the submitter's own repository
License URL:                    https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt
Steward:                        Yuta Yokoi (横井雄太)
SPDX Identifier:                Not registered (LicenseRef-ACD-1.0 is the conforming form)
ScanCode Identifier:            None
Third-party Endorsement:        None (no Debian, FSF or Fedora review)
Proposed Tags:                  None
```

**Two of those lines are the ones a reviewer will stop on**, and they are stated without
softening: no lawyer drafted or reviewed it (#1), and the only project using it is the
submitter's own (#4).

### A.1 Affirmative statement of OSD compliance

OSI's process requires the submitter to "affirmatively state that the license complies with the
Open Source Definition". **Stated plainly: I affirm that ACD-1.0 complies with the Open Source
Definition.** The criterion-by-criterion analysis is in §3, and **§3b sets out, for each of the ten
criteria, where a reviewer could still argue the opposite** — the affirmation is not offered in
place of that, and nothing in §3b is withdrawn by making it.


---

## B. OSI License Review — ready-to-send message (**not yet sent**)

> **This is the approval-request step, and it has not been taken.** What is currently open is a
> thread on `license-discuss`. Send this only when the decision is to actually request approval.
>
> **Before sending, add a paragraph about the license-discuss thread.** The usual order is
> discuss → review, and a submission that arrives without referring to the earlier thread
> reads as though the earlier thread never happened — which costs credibility before anyone
> has evaluated the text. Pick three points from `LICENSES/ACD-1.0.discussion-log.md`
> (strongest objection / what was conceded / what changed) and use the template in section 3
> of that file. **If something raised there is still unanswered, say so** — hiding it fails
> the moment the person who raised it is also on license-review.

> **⚠ 2026-09-11 追加 —— 上の指示は「指摘が届いた」場合の形しか持っていない。** 「最も強い反論 /
> 認めたこと / 変えたこと」を 3 点選べという指示は、**選ぶ材料があることを前提にしている**。
> **沈黙のまま出す経路がある**（`REVISION-PROTOCOL.md` §3.6 分岐 B・オーナー 2026-09-11）。
> **その場合にこの指示へ従おうとすると、無いものを作文する場所になる** —— 提出文のうち
> **最も嘘が混入しやすい一段落**が、まさにここである。**そこで沈黙版を先に書いておく。**
>
> **沈黙版（そのまま貼れる形。送る日に日付と「返信ゼロ」を測り直すこと）:**
>
> > **On the earlier license-discuss thread.** ACD-1.0 was posted to `license-discuss` on
> > 26 August 2026, to ask for pre-review before requesting approval. A second and narrower
> > message followed on 6 September 2026, putting one question about the relationship between
> > Sections 3 and 4. **Neither has drawn a reply in the public archive as of <DATE>.**
> > I do not read that silence as agreement. Replies on that list arrive on their own
> > schedule, and a measurable share of threads there receive none at all.
> > **The differences between the text discussed there and the text submitted here are
> > therefore not responses to comments. They are defects I found in my own text**, and each
> > one is listed, with what was changed and why, in the errata record linked below.
> > **Defects that are still unrepaired are listed as unrepaired.**
>
> **この段落で守ること**: **(1)** 沈黙を支持と読ませない（`against.md` #109 —— 返信ゼロは
> 珍しくない）。**(2)** 「指摘を反映した」と書かない —— **1.1 草案が閉じている 12 件は
> 全件が自己発見の errata で、言われて直したものは 1 件も無い**。**(3)** 未修理を未修理と書く。
> **(4)** 貼れば §B.0 の語数が約 110 語増える —— **申告語数を測り直す**（確定手順の (3)）。
> **返信が届いていたら、この沈黙版は使わず上の元の指示に従う。**

Send to `license-review@opensource.org` (subscribe first). OSI asks submitters to state
the rationale, to distinguish the licence from the closest approved one, to address the
Open Source Definition, and to say where the licence is used.

---

### B.0 The message as it should actually be sent (**1505 words**, measured 2026-09-25)

> **どの版を出すのか（2026-09-11 追加）。** **オーナー確認済みの計画は「discuss で受けたものを
> 取り込んだ改訂版を `license-review` へ出す」である**（`REVIEWERS.md` の Status）。
> **したがって提出対象は 1.0 ではなく、確定した次版になる。** 本 §B.0 の header block と URL は
> **まだ 1.0 を指している** ——**それが誤りなのではなく、次版が確定していないからである。**
> **確定させるのに必要なのは 3 手だけ**: **(1)** `ACD-1.1.txt` を `ACD-1.1.txt` として確定し
> `FROZEN.md` の FREEZE-DATA に行を足す（置き換えない）/ **(2)** `generate_spdx_license_xml.py` で
> XML を生成する（**Check 445a が本文からの再生成と byte 一致を強制するので、手で書く余地は無い**）/
> **(3)** 本 §B.0 の header block・URL・語数申告を新版へ向ける（**Check 444 が cross-surface の
> 一致を強制するので、片側だけ直すと落ちる**）。**そして §4c の数値を再導出する** ——
> 条数は **82 → 77** に変わり、clause pointer 数は新しい `machine.json` から数え直しになる。
> **(4) 版に紐づく Check の対象を新版へ向ける。** **Check 460 face (n) は §4c を `ACD-1.0.txt` と
> `ACD-1.0.machine.json` に対して照合し、Check 468 / 468d は `ACD-1.1.txt` を見ている** ——
> **確定の瞬間に、前者は古い版を、後者は消えた file を指す。**
> **CI が最も止まってほしくない日に止まるので、ここは確定作業の一部として先に書いておく。**
> **(5) 新版をこのリポジトリへ適用する。** **適用しなければ、提出する版の利用者は 0 件になる。**
> 現在 ACD-1.0 は root `LICENSE` を含む約 10 面（`llms.txt` / `llms-full.txt` /
> `llms_well-known.txt` / `.well-known/*` / `index.html` の JSON-LD / `robots.txt` /
> `sitemap.xml` / README バッジ）で宣言され、**Check 444 が cross-surface 一致を強制**している。
> **1.0 の本文は動かない** —— 凍結は**本文の byte についての約束**であって、リポジトリが
> どの版を適用するかの約束ではない。**B2（実使用 1 件）は我々の 2 大弱点の一つであり、
> 経路の変更でそれを 1 → 0 にしてはならない。** AIO 編集なので `aio-guardian` を通し
> digest を再生成する（C6）。
>
> **どれも AI が実行できるが、「確定させる」判断はオーナーのものである。**

> **🛑 送る前に読む（2026-09-09 追加）。** OSI Moderators が同日、両リストへ
> **「AI が全部または大半を書いたと疑われる投稿は拒否する」**と投稿し、両リストが
> **「AI が自律的に参加しライセンスを起草する proof-of-concept」**に使われていると述べた
> （逐語は `rounds/2026-09-09-license-{discuss,review}-osi-moderators-observed.txt`・
> 分析は `ACD-1.0.against.md` #119 と `ACD-OSI-BOTTLENECKS.md` B14）。
> **§B.0 は AI 起草の文面である。この状態で送ることは、その通知が名指しした行為に当たりうる。**
> **次に何を送るか、そもそも送るかはオーナーの判断であり、AI はそれを代行しない。**
> **開示（§E.1）を薄めて回避してはならない。**

**Why this section exists.** Everything below §B.0 — §1 through §5 — runs to **7,500 words**. The
list's code of conduct asks for "concise and low-volume" and that was restated in the August 2026
review (`REVISION-PROTOCOL.md` §3.7). **A 7,500-word opening post contradicts the design this
dossier is built on**, which is that the repository holds the depth so the message can be short.
§1–§5 are not deleted: they are the reference material the short message points at, and they are
where a reviewer who asks a specific question is sent. **Send §B.0. Do not paste §1–§5.**

**Length, stated rather than rounded.** 577 words when written on 2026-09-06; **660** after two
additions the same day; **685** on 2026-09-07, when the enforcement sentence was changed to say what
each CI check actually establishes (`against.md` #95); **768** when the OSD affirmation was made
specific to criteria 3, 5, 6 and 9 as the review-process page requires (#97) — **that one is not
optional**, because on 2026-09-07 a reviewer publicly declined to comment on another submission at
all until its missing required information was supplied; **788** when the "why now" paragraph was
corrected, because it had said no submission before 2024 concerned machine learning and the archive
shows two in 2023 (#103); **858** on 2026-09-08, when the structure paragraph gained the thing that
most directly answers *"why another public-domain-equivalent?"* — that §4.4 states in text the
argument which had to be argued on this list to save the Unlicense in 2020
(`review-precedents.md` §1.57); **971** on 2026-09-09, when a second gap was added to the same
paragraph — moral rights, which the chairman of Open Source Group Japan argued on this list in 2024
leaves licences that speak only of copyright unable to guarantee modification in Japan
(`review-precedents.md` §1.59).; **1,048** on 2026-09-10, when the gap paragraph stopped asserting that no approved licence does these things and started **stating the measurement** —— all 149 OSI-approved texts searched, four strings at zero （**+77 語。長さは B3 の争点であり、足すたびに理由を書く**）

**And 1,098 on 2026-09-11**, when the gap paragraph gained **a one-sentence form before the detail**. The reason is a precedent rather than a preference: **the only new licence approved in 33 months whose submitter was an individual** — the OSC License, a lawyer submitting for the city of Solingen — **stated its gap in one sentence** (*"the versatile MIT license does not contain a limitation of liability that is effective under German law"*) and reached a decision in three months (`review-corpus.md` §1.68). **Ours named three areas before it named one.**

**And 1,456 on 2026-09-25**, when a subject-matter paragraph was added. **The first draft of it ran
223 words and was cut to 94 before it was kept.** The reason is this section's own design: the
repository holds the depth so the message can be short, and a 223-word pre-emption written into the
message would have worsened **the one bottleneck with two recorded instances of a reviewer not
engaging at all** (`ACD-OSI-BOTTLENECKS.md` B3). **The full treatment went to the reference instead**
(`ACD-1.0.submission-reference.md` §3d). **Naming an objection before the reviewer finds it is worth
words; explaining it at length in the opening message is not.**

**And 1,505 the same day**, when the OSD affirmation gained **OSD 1 and OSD 7**. The review-process
page asks for 3, 5, 6 and 9, and those were there; **the archive shows 1 and 7 are the criteria a
patent objection is actually raised under** (`review-doctrine.md` §1.112). **Naming a criterion we
meet costs 49 words and removes a place the reviewer has to go looking.**

**Why that last addition earns its words.** *"Why another public-domain-equivalent?"* is the opening
move in this category — Rob Landley put it as fungibility (#84), David Woolley put it to the
UPD 1.5.2 author, Carlo Piana has put it as proliferation — and until 2026-09-09 the only answer in
the message was about the Unlicense. **The 0BSD form of the question had no answer at all**, which
is the form Landley actually asked. It now has one, and it is sourced to this list rather than to us.

**Two defects in this paragraph were found on 2026-09-09 and are recorded rather than quietly
swapped.** A clause about #103 had been stranded in the wrong sentence by an earlier edit, and the
summary of the 2026-09-06 additions still described *"why now"* as claiming **no ML-substantive
submission before 2024** — **the very claim #103 corrected in the message itself.** The message was
right and its own changelog was wrong. **An account of our corrections that is itself uncorrected is
the same failure as a stale count**, and it is worse here, because this is the paragraph a reader
consults to find out what we fixed.

**The instrument, stated with the number.** Whitespace-separated tokens from the `**Subject:**` line
to the sign-off, fenced metadata block included, counted by `re.findall(r'\S+', ...)`. **This was
written down on 2026-09-09 because it had never been**: recomputing the earlier figures showed the
method matters by tens of words depending on where the count starts and whether the fenced block is
included. **A number without its instrument is the failure recorded at #87**, and this dossier had
been carrying six of them.

**If it grows again, the number here moves with it** — a heading that rounds its own length to a
friendlier figure is the failure this dossier spent 2026-09-06 finding in itself.

---

**Subject:** For Approval: Autonomous Commons Dedication 1.0 (ACD-1.0)

Dear License Review Committee,

I am submitting the **Autonomous Commons Dedication 1.0 (ACD-1.0)** for approval. The text is
attached as plain text; it is also published at
`https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt`, and the attachment can be
checked against it — the SHA-256 is pinned in `LICENSES/FROZEN.md` and verified by CI, so the text
cannot drift during review.

```
License Name:                   Autonomous Commons Dedication
Version:                        1.0
Short Identifier:               ACD-1.0
Copyleft:                       No
Legacy or New:                  New License
Drafted By Lawyer:              No
Approved or Used by Projects:   One — my own repository
Steward:                        Yuta Yokoi (横井雄太), yuta.yokoi.r@gmail.com
Submitter:                      The same person, in his own capacity
SPDX / ScanCode Identifier:     None (LicenseRef-ACD-1.0 is the conforming form)
Third-party Endorsement:        None (no Debian, FSF or Fedora review)
Proposed Tags:                  None
```

**I affirm that ACD-1.0 complies with the Open Source Definition**, and specifically that it meets
**OSD 3** (§4.2 permits modification and derivative works; §10.1 attaches no condition to
distributing them; and §16.3 lets anyone apply this text to a work in which they hold rights, so a
derived work may be distributed **under these same terms**), **OSD 5 and OSD 6** (§4.3 states the licence is not conditioned on who You are
or what You use the Work for, so no person, group or field of endeavour is excluded), and **OSD 9**
(§5.2(b) and §2.3 confine the instrument to this Work, so nothing is required of other software
distributed alongside it). I add **OSD 1 and OSD 7**, because the archive shows those are the
criteria under which a patent objection is actually raised: §8 grants a patent licence on the same
terms to everyone who receives the Work, so nothing further has to be executed by a downstream
recipient. A criterion-by-criterion analysis of all ten is in the repository, and so
is a companion section setting out, for each, **where a reviewer could argue the opposite**.

**The gap.** In one sentence: the approved licences that impose no conditions say nothing about
machine learning, and the machine-learning licences brought to this list have so far added
conditions; ACD-1.0 is the intersection — no condition of any kind (§10.1), and explicit about
training, models and outputs (§6, §8.4, §9). **In detail**, ACD-1.0 is written for works meant
to be learned from. It does three things no
approved licence does together: it expressly permits machine learning and text-and-data-mining and
declines to make any reservation (§6); it grants a patent licence that reaches models and outputs
of computational use (§8.4); and it makes the recipient's permissions independent of whether
copyright subsists in machine-generated material at all (§9). **That claim is measurable, and I
measured it**: across all 149 OSI-approved texts (SPDX List 3.28.0, fetched 2026-09-10) the strings
"machine learning", "text and data mining", "machine-generated" and "subsist" occur **zero** times.
Absence of the words is not absence of effect — a permissive licence allows training by allowing
everything — but it is what leaves §6, §8.4 and §9 open. The command is in the repository.

**Why now, since the objection is reasonable.** Licences for machine learning have been brought to
this list since at least April 2023 — the Restricted Artificial Intelligence License, withdrawn four
days after submission, and the Open Constitution License later that year — and the rate has risen
sharply since 2025. **None has been approved.** I do not claim the timing makes this licence
necessary. I offer it against the fair objection that if the question were real, someone would have
raised it long ago: it has been raised, repeatedly, and has not yet been answered.

**And why this one is shaped differently.** The AI-era submissions so far add conditions —
transparency duties, attribution, notice on outputs — and that is where they have run into OSD 3,
7 and 10. ACD-1.0 goes the other way: it imposes no condition at all (§10.1), and it makes no
representation about whether copyright subsists in machine-generated material (§9.2), so a
recipient never has to decide that question. It is the opposite bet on the same problem.

**A disagreement I should name rather than let you find.** On the ModelGo thread the chair wrote
that mentioning model Output at all creates *"ambiguity about the legal status of the output"* and
is *"not worth including"* (15 December 2025). ACD-1.0 mentions it anyway, in §6.4, for the reason
§6.5 gives: silence has proved ambiguous, and a permission an automated system cannot determine is
no permission at all. That is a deliberate trade-off, not an oversight.

**On the scope of the patent grant.** §8.1 reaches claims infringed by subject matter contained in
the Work as made available by the Dedicator. That is the limitation this list has itself described
as acceptable — Pamela Chestek's formulation in February 2025, and the phrasing Bruce Perens called
*"the proper language"* in April 2024. I mention it because a non-lawyer's drafting is otherwise
hard for you to check: the wording was fixed on 23 August 2026, before this project had read either
message, and the repository's history shows that.

**Subject matter, which I raise because a 2023 decision turned on it.** The Mulan Open Works
Licenses were declined as open culture licences rather than for any Open Source Definition failure,
and the rationale quoted their own list of covered works. ACD-1.0's §1.2 lists "audiovisual
material" beside source and object code. I have not narrowed it, because datasets and model weights
are the non-code material the gap is about; the overlap, and the committee's own line between a
licence tied to software and one unrelated to it, are set out in the reference (§3d).

**Nearest approved licences.** It is closest in effect to the Unlicense, MIT-0, 0BSD and CC0, and
closest in patent machinery to Apache-2.0. The full comparison — **including where those are the
better choice, which is most of the time** — is in the repository.

**Structure, since it matters for reviewability.** §3 surrenders the Covered Rights and §4 grants a
licence over the same rights **independently of §3** (§4.4): §4 does not wait for §3 to fail, and a
recipient never has to decide which operated. The Committee's 2020 recommendation on the Unlicense
records that a dedication *taken alone* would not be approved; ACD-1.0 is not taken alone.

**Why that matters, and why another public-domain-equivalent.** The 2020 veto against the Unlicense
was that it was *"very much not clear"*. What answered it was the argument that, even if the
dedication were ineffective, the enumerated permissions would still operate. **That argument is not
in the Unlicense's text — it had to be made on this list.** §4.4 states it, so no recipient and no
court has to reach it.

**And a second gap, named on this list rather than by me.** In March 2024 the chairman of Open
Source Group Japan argued here that a licence speaking only of copyright — Blue Oak was the
example, but 0BSD and MIT-0 read the same way — is *"not open source, at least not in Japan"*,
because the right of integrity reaches software there and can be used to stop modification. §12
answers that with a waiver where waiver is possible and, where it is not, a covenant not to
exercise, binding heirs. **No lawyer has checked whether it works. What I claim is only that the
incumbents do not attempt it.**

**Legal review: none.** No lawyer has drafted or read it. I state that plainly rather than let it
be discovered. What can be shown without counsel is mechanical, and is checked in CI on every
pull request and on every push to the main branch: contiguous clause numbering, resolution of every internal cross-reference, use of every
defined term, absence of the obligation-imposing constructions I enumerate, absence of the
project-specific elements I enumerate — names, URLs, placeholder text — and pure-ASCII text.
**Each is a floor rather than a proof**: an enumeration catches the forms it lists.

**Provenance.** I decided to have a licence of my own and said it should aim at external approval;
I gave the goal and the top-level direction, and did not write a legal specification or supply a
list of legal requirements. An AI agent generated the concrete legal design and the text and
developed it further under my standing delegation. The name ACD-1.0, the generalised instrument
and this packet took shape during that delegated work, and I came to know their concrete state
afterwards. I read the text in full and understood it before relying on it. I am the Dedicator and
steward and I answer for it; I did not write its clauses.

**Everything else, including the case against approving it.** The repository carries an adverse
list — written by me, adverse items first, with the two entries that have no answer at the top —
along with known defects in the text, the jurisdictional questions, and worked answers to the
objections I expect. Start at `LICENSES/REVIEWERS.md`. I would rather you found those there than
had to extract them from me.

Thank you for your time.

Yuta Yokoi

---

### B.1 Reference material behind the message (**not for pasting**)

**Moved 2026-09-09 to [`ACD-1.0.submission-reference.md`](ACD-1.0.submission-reference.md).**
§1〜§5 はそこに在り、**節番号は変えていない**ので `submission-reference.md §4c` のような既存の参照は
本書ではなく参考資料の同じ節へ解決する。

**分けた理由は 2 つ。** 読み手が違う ——**この文書は送る人が読み、参考資料は審査者が読む**。
そして**同居している限り「§1〜§5 を貼るな」という警告が必要**であり、警告は分割で不要になる。
規模もある（分割前 976 行・advisory 950）。

## C. SPDX License List — ready-to-paste request

Submit via https://tools.spdx.org/app/submit_new_license/ (preferred) or the
`spdx/license-list-XML` new-license-request issue template.

- **Full name:** Autonomous Commons Dedication 1.0
- **Short identifier requested:** `ACD-1.0`
- **OSI approved:** No. Not submitted to OSI License Review either — only discussed on license-discuss
- **Licence text URL:** https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt
- **SPDX XML:** `LICENSES/ACD-1.0.spdx.xml` in the repository below, generated from the
  text by `npm run spdx-xml` and kept in sync by a blocking CI check, so the submitted
  markup cannot drift from the published text.
- **Evidence of use:** https://github.com/yutapr0117-design/portfolio — the licence covers
  the whole repository (source, documentation, data, and media assets) and is declared in
  `LICENSE`, in `link rel="license"`, in the JSON-LD `license` property of every
  CreativeWork node, in `sitemap.xml`, in `.well-known/aio-manifest.json`, and in the
  `llms.txt` family, each of which is checked in CI.
- **Not a duplicate:** it is not a variant of any listed licence. A clause-level comparison
  with 0BSD (closest on "zero conditions") and Apache-2.0 (closest on "express patent
  licence") is given in section B.2 above.
- **Steward commitment:** I am the steward. Once `ACD-1.0` is on the list I will not modify
  the text that the identifier denotes. Any later improvement will be issued as a distinct
  version (`ACD-1.1`, `ACD-2.0`) with its own identifier. Section 16.4 of the text itself
  forbids distributing a modified text under the same name or identifier.

---

## D. Before sending — checklist for the human

1. `LICENSES/READY-TO-SUBMIT.md` exists (it is written only when the text is judged ready).
2. The published copies resolve:
   `curl -sI https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt`
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
