---
file: LICENSES/ACD-1.0.review-responses.md
audience: ai, human (提出者), 監査人, 第三者全般
last-updated: 2026-08-26
canonical-ref: LICENSES/ACD-1.0.txt (凍結中の本文) / LICENSES/ACD-1.0.submission.md (提出パケット) / LICENSES/READY-TO-SUBMIT.md (提出判断) / LICENSES/FROZEN.md (凍結宣言) / docs/architecture/acd-license-rationale.md (設計根拠)
---

# ACD-1.0 — OSI license-review 想定問答ドシエ

```
Status        : OSI license-review (公開レビュー) へ投稿済み・結果待ち
                ※ OSI の「正式承認申請」でも SPDX License List 提出でもない
本文の状態    : 凍結中 (LICENSES/FROZEN.md の存在が凍結を意味し Check 453 が sha256 で強制)
本書の位置づけ : 非規範。ライセンス本文の一部ではない。回答の下書きであって、
                ここに書いたことが ACD-1.0 の意味を変えることはない
```

## 0. この文書の使い方

OSI の `license-review` は**公開のメーリングリスト上の議論**であり、審査というより「読者が本気で読んで穴を突く場」である。したがって必要なのは *弁明* ではなく **「その指摘は正しい / 正しくない、根拠はこれ」を短く返せる準備**である。

本書は次の形で並べてある。

- **想定される指摘**（日本語・一行）
- **そのまま貼れる英文の回答**（引用ブロック）
- **なぜこう答えるか**（日本語・回答の裏にある判断）

英文をそのまま貼れる形にしてあるのは、リストの言語が英語だからであって、翻訳の手間を惜しむためではない。**回答は必ず読んでから貼ること。** 議論の流れによっては「答えない」「認める」ほうが正しい場面がある（§5 参照）。

### 3 つの原則

1. **認めるべき指摘は即座に認める。** license-review で最も心証を損なうのは、弱点を指摘されたときに言い繕うことである。本ドシエには「認める」と書いた項目が実際にある（§4）。
2. **本文は凍結中なので、その場で直さない。** 妥当な指摘を受けたときの正しい返答は「その指摘は正しい。ACD-1.1 でこう直す」であり、審査中に差し替えることではない。審査側が見ているテキストと公開されているテキストが食い違うのが最悪である。
3. **保証しない。** 「承認されるはずだ」と述べない。求めているのはレビュー結果であって同意ではない。

---

## 1. 前提の確認 —— この提出が何であって何でないか

| | 実態 |
|---|---|
| 出したもの | OSI **license-review** への投稿（公開議論の開始） |
| 出していないもの | OSI の正式承認申請 / SPDX License List への収録申請 |
| SPDX を見送った理由 | SPDX は「相当程度の実使用」を求める。現在の使用実績は本リポジトリ 1 件で、その条件を満たしていない。**満たしていないものを出さない**のが誠実である |
| いま欲しいもの | 起草では解消できない論点（dedication 型の是非・§12 の各国法での効き方・§8.4 の射程）について、**第三者の目による判断** |

**この区別は最初の投稿で明示したほうがよい。** 「approval を求めているのか discussion を求めているのか」はリストで頻繁に確認される点であり、先に述べておくと以後のやり取りが噛み合う。

> **English (use in the opening message if not already stated):**
>
> To be clear about what I am asking for: I am seeking review and criticism, not
> a fast path to approval. I have deliberately not submitted this to the SPDX
> License List, because SPDX asks for substantial real-world use and this text
> currently has exactly one user — my own project. I would rather be told that
> the instrument is unnecessary, or that a particular section does not work,
> than have it listed on the strength of nobody having read it closely.

---

## 2. 最重要の 3 問（ここで負けたら他は読まれない）

### Q1. なぜ新しいライセンスが要るのか（license proliferation）

> **English:**
>
> The short answer is that three properties I needed are not available together
> in any approved licence, and two of them are not available at all.
>
> 1. **An affirmative permission for machine learning and TDM, coupled with an
>    express statement that no reservation is made.** Several jurisdictions now
>    key TDM exceptions to whether the rightsholder has *reserved* the right
>    (the EU DSM Directive Article 4(3) opt-out, and the machine-readable
>    reservation protocols now being built on top of it). A permissive licence
>    grants copyright permissions but says nothing about reservation, so a
>    downstream system that checks for a reservation signal has to guess.
>    ACD-1.0 Section 6.2 states the absence of a reservation as a term of the
>    instrument itself.
> 2. **A patent grant in a public-domain-style instrument.** CC0 is the closest
>    existing instrument in form, and CC0 Section 4(a) expressly does *not*
>    grant patent rights. That exclusion was the centre of the 2012 discussion
>    on this list, and it is precisely the gap Section 8 fills.
> 3. **A workable position on machine-generated material.** Where authorship
>    itself is uncertain (and it is uncertain, differently, in the US, the EU,
>    the UK and Japan), a licence that presupposes a subsisting copyright leaves
>    the user to guess. Section 9 removes the question from the user's path
>    without asserting an answer to it.
>
> I would genuinely rather be shown an existing licence that does all three. If
> one exists, I will use it and withdraw this.

**なぜこう答えるか**: proliferation の指摘に対する唯一有効な返しは「**既存で埋まらない具体的な穴**を挙げること」であり、「私のプロジェクトに合うから」は答えにならない。そして最後の一文（既存で埋まるなら撤回する）は形式的な謙遜ではなく、**実際にそうすべき**である。撤回できると言える提出者は、そう言えない提出者より真剣に読まれる。

### Q2. CC0 は撤回された。なぜこれは違うのか

> **English:**
>
> CC0 was withdrawn from this list by Creative Commons in 2012. As I read the
> archive, the objection that mattered was not "dedications are bad" in the
> abstract but a concrete one: CC0 Section 4(a) states that no patent rights are
> waived, abandoned, surrendered, licensed or otherwise affected. An instrument
> that hands over copyright while expressly preserving patents can leave a user
> worse off than a permissive licence, because the user has no notice that the
> patent risk was carved out.
>
> ACD-1.0 takes the opposite position in Section 8: a patent licence is granted,
> on the same no-condition footing as everything else, and Section 8.3 says
> expressly that nothing in the instrument reserves or preserves any patent
> claim. Section 8.4 extends the grant to models, parameters and outputs,
> because Section 1.5 excludes patents from "Covered Rights" and I did not want
> the copyright-side permission for computational use in Section 6 to be
> undercut by a patent-side gap.
>
> If the committee's position is that the *form* is the problem regardless of
> the patent point, I would like to hear that stated, because it is decisive for
> whether this text should exist at all.

**なぜこう答えるか**: CC0 の件は**必ず**出る。ここで「CC0 とは違う」と抽象的に言うと相手にされない。**撤回の実際の争点（§4(a) の特許除外）を正確に述べ、自分の §8 がその一点への回答であること**を示すのが唯一の筋である。そして最後の一文で「形式自体が問題なら、それを言ってほしい」と**負けを引き受ける用意**を見せる。これは §7 の弱点 4「公有化型は歴史的に難しい」に対する正面からの姿勢である。

### Q3. 献呈（dedication）は「ライセンス」なのか。OSI が扱う対象か

> **English:**
>
> ACD-1.0 is deliberately built as three independent footings for the same
> outcome, not as a dedication with a licence bolted on:
>
> - Section 3 surrenders the rights, where surrender is possible.
> - Section 4 grants a licence, **independently** of Section 3 and without
>   waiting for Section 3 to fail (Section 4.4). It is not a fallback that has
>   to be triggered.
> - Section 5 is a covenant not to assert, which operates even if both of the
>   above are held ineffective somewhere.
>
> Section 2.4 states that Sections 3, 4, 5 and 6 are independent of one another.
> So whatever a given jurisdiction thinks of abandonment of copyright — and
> Germany and much of the civil-law world think very little of it — there is an
> operative licence grant on the page that a court can enforce on ordinary
> licence principles.
>
> If the committee's view is that OSI should evaluate only the Section 4 licence
> and disregard Sections 3 and 5, that is a reading the text can bear, and I
> would accept it.

**なぜこう答えるか**: 「dedication は各国法で効かないことがある」は**正しい指摘**であり、否定してはならない。答えは「効かない場合に備えて**独立の**ライセンス条項が同じページにある」であり、これは実際にそう起草されている（§2.4 / §4.4）。最後の譲歩（§4 だけ見てくれてよい）は、審査の焦点を**確実に評価可能な部分**へ寄せる実利がある。

---

## 3. Open Source Definition 逐条

OSD への適合は提出者が**自分から**述べるべきものである。以下は 10 条それぞれについて、根拠条項を指した形。

> **English (paste as a block if asked for an OSD walkthrough):**
>
> **1. Free redistribution.** The licence in Section 4.1 is worldwide,
> royalty-free, non-exclusive and irrevocable, and Section 4.3 attaches no
> condition to it. Section 4.5 states the consequence for redistribution: You may
> distribute the Work, and any adaptation or collection containing it, **under
> any terms You choose**, including terms incompatible with these, and nothing
> requires those terms to reproduce this text. Selling is therefore permitted and
> no royalty is payable to the Dedicator.
>
> **2. Source code.** The instrument imposes no obligation of any kind
> (Section 10.1) and in particular does not require source to be made available
> (Section 10.2) — but neither does it restrict it. Applied to software, the
> Work as distributed by the Dedicator is the source. Nothing in the text
> permits distribution in obfuscated form only, because nothing in the text
> conditions anything.
>
> **3. Derived works.** Section 4.2 includes the rights to reproduce, adapt,
> modify and distribute; Section 4.3 attaches no condition, so derivatives may
> be distributed under any terms the distributor chooses.
>
> **4. Integrity of the author's source code.** No requirement to mark changes
> is imposed (Section 10.2). This criterion permits, but does not require, such
> a term.
>
> **5. No discrimination against persons or groups.** "You" is defined in
> Section 1.4 as any person or entity exercising permissions; no class is
> excluded anywhere in the text.
>
> **6. No discrimination against fields of endeavour.** Section 4.1 is granted
> for any purpose; Section 6.1 states expressly that computational use is
> permitted for any purpose. There is no non-commercial, non-military,
> ethical-use or AI-related carve-out. **The AI provisions of Section 6 are
> permissions, not restrictions** — this is the point I most expect to be
> misread, given that most licences mentioning AI in the last three years have
> been restrictive ones.
>
> **7. Distribution of licence.** Section 2.3: the Dedication takes effect
> without any act of acceptance; Section 16.2: an SPDX identifier or a reference
> by name is sufficient notice. Rights attach to the recipient without any
> further instrument.
>
> **8. Licence must not be specific to a product.** The text speaks only of
> "the Work", "the Dedicator" and "You". Section 16.3 states that it may be
> applied by anyone, to any work. My own project's application of it is a
> separate file (`LICENSE`), not part of the text. This separation is enforced
> mechanically in my repository, so that the text cannot acquire
> project-specific content by accident.
>
> **9. Licence must not restrict other software.** Section 4.5 expressly covers
> "any adaptation or collection containing" the Work and disclaims any obligation
> on You in respect of Your recipients. No term reaches other software distributed
> alongside it, and Section 4.6 confirms that terms You add govern only what You
> give.
>
> **10. Licence must be technology-neutral.** No term depends on a technology,
> interface or medium. Section 2.3 requires no click-through or other act of
> assent.

**なぜこう答えるか**: OSD 6 が最大の誤読ポイントである。近年 license-review に来る「AI を扱うライセンス」の大半は**制限**（学習禁止・用途制限）であり、レビュアはその前提で読み始める。**「§6 は許諾であって制限ではない」を OSD 6 の項で先に言う**のが最も効く。OSD 8 については「本文とプロジェクトへの適用宣言が別ファイルであり、それが機械強制されている」という事実が強い（Check 441 の「プロジェクト固有要素ゼロ」）。

---

## 4. 認める項目（先に自分から述べる）

**この節は防御ではない。** 指摘される前に自分から出すべき弱点である。提出パケットの "Honest disclosures" と整合させること。

### A1. 法的レビューを受けていない

> **English:**
>
> No lawyer has reviewed this text. I say that first because it changes how the
> rest should be read. The drafting is my own, checked mechanically against the
> published criteria rather than against professional judgement. Section 12
> (moral rights) is the place where that matters most, because it turns on
> Japanese law — Article 59 of the Japanese Copyright Act makes moral rights
> personal to the author and inalienable — and on how a court would treat a
> covenant not to exercise them. I would value a correction there more than
> anywhere else in the document.

### A2. 実使用が 1 件しかない

> **English:**
>
> One project uses this: mine. I have not sought adopters, and I would rather
> say that plainly than present a single repository as an ecosystem. This is
> also why I have not gone to SPDX, which asks for substantial use. If the
> committee's view is that a licence with one user should not be reviewed at
> all until that changes, that is a reasonable position and I will accept it.

### A3. 長い

> **English:**
>
> At roughly 600 lines this is long for what it does, and length is a real cost:
> it is read less carefully, and every extra sentence is a place for an
> inconsistency to hide. My reason for the length is that most of it is not
> operative text but *stated reasoning* — Sections 8.3, 9.4, 11.4 and 12.4 each
> explain why they exist, because the failure mode I was drafting against is a
> future reader (including an automated one) drawing the wrong inference from
> silence. I accept that this is a trade-off and that reasonable people weigh it
> the other way. If the committee prefers a text with the explanations stripped
> to a companion document, that is a straightforward change for a 1.1.

### A4. §6 は copyright ライセンスとして冗長ではないか

> **English:**
>
> Partly, yes, and Section 6.5 says so on its face: it states expressly what
> Sections 3 to 5 would in any event achieve. I kept it for two reasons that I
> think survive the redundancy objection, but I acknowledge it is a judgement
> call.
>
> First, the EU DSM Article 4(3) opt-out is not a copyright permission question
> but a *reservation* question, and silence is doing work there that a grant
> does not do. Second, the readers I care most about are automated, and a
> statement that has to be inferred from the absence of a restriction is
> materially harder to act on than one that is present as text.

**なぜこの 4 つを先に出すか**: license-review では、提出者が弱点を隠していると判明した時点で議論が「テキストの是非」から「提出者の信頼性」に移り、そうなると回復しない。A1〜A4 はいずれも**調べれば分かる**（法的レビューの有無は書いてある、使用実績は GitHub を見れば分かる、行数は数えれば分かる）。**自分から言えば誠実さの証拠になり、言われてから認めれば失点になる**、というだけの違いである。

---

## 5. 条項別の想定問答

### §2 SCOPE AND EFFECT

**Q. §2.2「irrevocable」と言うが、各国法で本当に撤回不能か。**

> **English:**
>
> Section 2.2 states the Dedicator's position; it does not claim to override a
> jurisdiction that provides an inalienable withdrawal right (Germany's
> Rückrufsrecht wegen gewandelter Überzeugung, for instance). That is what
> Section 15.4 is for: a provision held unenforceable in a jurisdiction is
> reformed to the minimum extent necessary there and severed as to that
> jurisdiction only. In practice a user's protection against a change of heart
> is the layering, not the word "irrevocable" — Section 5 is a covenant not to
> assert, which is enforceable on ordinary contract or estoppel grounds in most
> systems even where the surrender in Section 3 is not.

**Q. §2.8 が承継人を拘束すると書いているが、そんなことができるのか。**

> **English:**
>
> Only "to the fullest extent the law permits the Dedicator to bind them" —
> Section 12.4 uses the same formula. The clause is doing two things. It states
> the Dedicator's intent, which matters for construction under Section 15.1, and
> it puts a successor on notice, which is what makes an estoppel argument
> available to a user who relied. It is not an assertion that a bankruptcy
> trustee is bound in every system. Section 2.8's stated concern with insolvency
> is there because that is the most common route by which rights reach someone
> who never made the promise.

### §6 MACHINE LEARNING, TDM

**Q. §6.2「no Reservation」は、他人が付けた留保まで無効化する主張ではないのか（OSD 上も越権では）。**

> **English:**
>
> It is not, and an earlier draft of mine did over-claim here — this was
> corrected before submission. Section 6.2 states that *the Dedicator* makes no
> reservation. Section 6.3 addresses a reservation made by someone else, and it
> does so only in the register Section 2.7 allows: the Dedication reaches only
> rights the Dedicator holds. Where a third party's reservation attaches to
> material inside the Work, that reservation is not the Dedicator's to disclaim,
> and Section 11.4 says so in terms for the adjacent case of personal data.

**Q. §6.4「モデルも出力も縛られない」——自分が持っていない権利について何を言っているのか。**

> **English:**
>
> Section 6.4 is a statement about what this instrument does, not a grant over
> rights the Dedicator lacks. Its function is to foreclose a specific bad
> inference: that permitting training implies some residual claim over what the
> training produces. Several recent licence-like documents assert exactly that,
> so silence on the point is not neutral any more. Read together with Section
> 8.4, the effect is that a person who trains on the Work does not need to reason
> about whether the Dedicator retained a hook into their model.

### §8 PATENTS

**Q. 特許報復条項（defensive termination）がない。Apache-2.0 §3 を持たないのは弱点では。**

> **English:**
>
> This is a real design choice and I will defend it rather than concede it.
> Apache-2.0's Section 3 terminates the patent licence if the licensee sues.
> Termination is a condition, and the whole architecture of this instrument is
> that there are no conditions and nothing that can be breached (Section 10.4).
> Adding retaliation would give the user something to lose, which is exactly what
> Section 10 removes.
>
> I recognise the cost: ACD-1.0 gives up the defensive benefit that Apache-2.0's
> users get. Someone who wants that benefit should use Apache-2.0, and I would
> say so to them. What I did not want was an instrument that is described as
> unconditional and then turns out to have one condition hidden in the patent
> section.

**Q. §8.4 はモデル・重み・出力にまで特許ライセンスを及ぼすと言うが、前例がない。**

> **English:**
>
> I am not aware of a precedent either, and I would be glad to be shown one. The
> reasoning is in Section 8.4's own text: Section 1.5 excludes patents from
> "Covered Rights", so Section 6.4 by itself leaves computational use permitted
> as a matter of copyright while leaving a patent-shaped hole in the same place.
> Section 8.3 rejects the reading that anything is reserved, so an instrument
> that left that hole would contradict itself.
>
> The scope limit is Section 8.5: like every other grant here, it reaches only
> claims the Dedicator can license (Section 2.7). It is not a warranty of
> non-infringement — Section 13.2 states in terms that the Dedicator does not
> warrant "that use of the Work does not infringe the rights of any other
> person".

### §9 MACHINE-GENERATED MATERIAL

**Q. 「権利が存在するか分からない」と書くのは利用者を不安にさせるだけでは。**

> **English:**
>
> The alternative is worse. A licence that presupposes a subsisting copyright,
> applied to material that may have none, tells the user something that might not
> be true, and the user still has to work out what happens if it is not.
> Section 9.3 is the operative part: You are not required to determine which
> parts are machine-generated, and no permission depends on that question, or on
> how any jurisdiction answers it, or on whether the answer changes. The
> uncertainty exists in the world; Section 9 keeps it off the user's path
> instead of pretending it away.

### §10 / §11 —— 「条件ではない」と繰り返すのはなぜか

**Q. §11.3（虚偽の endorsement 表示）は実質的な制限ではないのか。OSD 6 に触れないか。**

> **English:**
>
> Section 11.3 does not restrict anything, and it is drafted to make that
> unmistakable: "This Section states a limit of the Dedication's reach; it is not
> a condition upon You, and Section 10.1 is unaffected by it."
>
> Falsely representing that I authored or endorsed something is actionable, where
> it is actionable, under trademark, passing-off, unfair-competition or
> personality law — none of which are mine to license away. Saying so is not
> imposing a term; it is declining to mislead the reader about how far the
> instrument goes. Apache-2.0 Section 6 does the same job for trademarks, and
> Section 11.2 preserves nominative use expressly so that the clause cannot be
> read as suppressing truthful statements about provenance.

**Q. §10.3「attribution の依頼は条件ではない」——では依頼に意味はあるのか。**

> **English:**
>
> It has social meaning and no legal effect, and Section 10.3 says which is
> which. The reason for stating it that bluntly is that "please cite me" in a
> README, sitting next to a licence, is routinely read as a term. If I want
> credit and do not get it, that is a disappointment, not a breach — and a user
> should be able to determine that from the licence rather than from my
> temperament.

### §12 MORAL RIGHTS

**Q. 日本法では人格権は放棄できない。§12.1 は空文ではないか。**

> **English:**
>
> In Japan, yes: Article 59 makes moral rights personal to the author and not
> transferable, and the prevailing view is that they cannot be waived outright.
> That is why Section 12.1 is expressed "to the fullest extent permitted by the
> law of each jurisdiction" and why Section 12.2 supplies a covenant not to
> exercise them wherever waiver is unavailable. A covenant not to exercise is the
> mechanism Japanese practice actually uses (fukōshi tokuyaku), and it is what
> commercial agreements there rely on.
>
> Section 12.3 keeps the covenant limited to this Work, so it is not a general
> renunciation of the author's personality rights — that limitation is
> deliberate, because an unlimited one would be more likely to be struck down,
> not less.
>
> This is the section where I would most welcome correction, and I have flagged
> it as unreviewed by counsel.

**Q. §12.4 が遺族・遺言執行者まで拘束すると言うのは無理では。**

> **English:**
>
> Again "to the fullest extent the law permits the Dedicator to bind them". Many
> systems let relatives or a public authority enforce moral rights after death,
> so a covenant binding only the living author would leave the longest-lived risk
> open — Section 12.4 says exactly that as its reason. Whether it binds is a
> question of each jurisdiction's succession law, and the clause does not pretend
> otherwise. Its reliable effect is notice and construction, not conquest.

### §15 / §16

**Q. §15.7 で準拠法を定めないのは欠陥では。**

> **English:**
>
> A choice-of-law clause in a unilateral grant that takes effect without
> acceptance (Section 2.3) would be asserting a term the recipient never agreed
> to, and would invite the argument that acceptance was needed after all.
> Section 15.7 therefore says the instrument is intended to operate under the law
> of each jurisdiction in which the Work is used, according to that law. That is
> also how CC0 and the Unlicense behave in practice. Section 15.4 handles the
> consequence — per-jurisdiction reformation and severance.

**Q. §16.4 は本文の改変を禁じている。ライセンス文書自体が自由でないのは矛盾では。**

> **English:**
>
> Section 16.6 draws the line: Sections 16.4 and 16.5 govern *this text as a
> document*, and Section 10.5 states that nothing in Section 16 is a condition on
> Your use of the Work. This is the same arrangement as the GPL, the Apache
> Licence and MPL, all of which are distributable verbatim only. The reason is
> identical: if "ACD-1.0" could name a modified text, the identifier would stop
> carrying information, and Section 16.2 makes the identifier alone sufficient
> notice. Section 16.5 exempts translations, and Section 15.8 keeps English
> authoritative so that a translation cannot change the terms.

---

## 6. 既存ライセンスとの差分（比較表を求められたとき）

> **English:**
>
> | | Patent grant | ML/TDM stated | Reservation disclaimed | Machine-generated material | Conditions |
> |---|---|---|---|---|---|
> | CC0-1.0 | **No** (Sec. 4(a) expressly excludes) | No | No | No | None |
> | Unlicense | Not addressed | No | No | No | None |
> | 0BSD / MIT-0 | Not addressed | No | No | No | None |
> | MIT / BSD-2 | Not addressed | No | No | No | Notice |
> | Apache-2.0 | Yes, limited to the Work and Derivative Works | No | No | No | Notice, NOTICE file, change marking |
> | ACD-1.0 | Yes, extended to models, parameters and outputs (Sec. 8.4) | Yes (Sec. 6.1) | Yes (Sec. 6.2) | Yes (Sec. 9) | **None** (Sec. 10.1) |
>
> The row that matters is the first: no approved instrument in the
> public-domain-dedication family grants patents, and no permissive licence with
> a patent grant is condition-free.

**なぜこの形か**: 比較表は**自分に不利な列を含めないと信用されない**。Apache-2.0 の「条件」列（NOTICE ほか）は Apache の弱点ではなく設計であり、そう扱うこと。ACD-1.0 の列で「None」と書ける代償が Q「特許報復条項がない」であることは §5 で認めてある。

---

## 7. 出そうで出ない質問への備え（短答で足りるもの）

| 想定される指摘 | 短答（英文で述べる要点） |
|---|---|
| GPL 互換か | Condition-free なので GPLv2/v3 いずれにも取り込める。ACD-1.0 の側から何も要求しないため互換性の問題が生じる余地がない |
| 誰が steward か | 起草者本人。§16.4 により ACD-1.0 のテキストは不変で、改訂は 1.1 以降の別バージョンとして行う（`FROZEN.md` と CI がこれを機械強制している） |
| どのカテゴリでの承認を求めるか | カテゴリの割当は委員会の判断に委ねる。特定のカテゴリを主張しない |
| 機械可読記述子（JSON）の位置づけ | 非規範。本文が唯一の権威。記述子が本文と食い違えば本文が勝ち、CI（Check 451）が食い違いを BLOCKING で検出する |
| なぜ ASCII 限定か | 転記・メール・古いツールでの毀損を避けるため。CI（Check 441）が純 ASCII を強制する |
| 名称の由来 | Autonomous（本リポジトリの運用モデル）/ Commons（条件ゼロで共有領域に置く）/ Dedication（許諾ではなく献呈という法的形式）。2026-08-23 時点で SPDX License List・OSI 承認一覧のいずれにも同名・類似識別子が無いことを確認済み（`acd-license-rationale.md` §6） |
| 実装（コード）は誰が書いたか | 本リポジトリは AI が実装し人間が設計・監査する体制で運用している。ライセンス本文もその過程で起草された。**この事実を隠さない**（§9 の存在理由と直結する） |
| 撤回する用意はあるか | ある。Q1 の最後の一文がその表明である |

---

## 8. 議論の進め方（回答内容ではなく態度の話）

1. **聞かれたことに答える。** license-review で最も嫌われるのは、指摘に答えず別の長所を語ることである。
2. **一度に全部貼らない。** 本ドシエは長いが、リストに投げるのは**その回に問われた項目だけ**にする。全文投下は読まれない。
3. **「その指摘は正しい」を惜しまない。** §4 の 4 項目はいつでも認めてよい。認めても失うものが無いように書いてある。
4. **本文を審査中に直さない。** 妥当な指摘は「1.1 でこうする」と述べて記録する。直したくなったら `FROZEN.md` を消したくなるが、それは**審査側が見ているテキストとの乖離**を作る行為である（Check 453 が機械的に止める）。
5. **沈黙も返答である。** 数日で反応が無いのは普通で、催促しない。OSI の決定は初回投稿から概ね 60 日かかる。
6. **敵対的な読みに感謝する。** 本ドシエの想定問答の多くは、起草時に「敵対的承継人 / 被告側弁護士 / 翻訳者 / 機械」のレンズで自分に対して行った攻撃の再演であり、外部から同じことをしてもらえるのは得である。

---

## 9. レビューで指摘されたら 1.1 で直す候補（現時点の自己評価）

**これは「直す」という約束ではない。** 指摘を受けたときに即答できるよう、あらかじめ棚卸ししたもの。

| 箇所 | 直す方向 | いま直さない理由 |
|---|---|---|
| 全体の長さ | 説明部分を companion document へ分離し、本文を operative text だけにする | 凍結中。かつ「説明を本文に置く」判断自体がレビュー対象なので、結果を見てから動くべき |
| §6 の冗長性 | §6.5 を残して §6.1〜6.4 を圧縮 | 同上。EU DSM の opt-out 実務が今後どう固まるかで正解が変わる |
| §12 | 日本法の専門家確認を経て、covenant の文言を実務の定型に寄せる | 助言を得ていない段階で定型に寄せると、**根拠なく正しく見えるテキスト**になる |
| §8.4 | 「model, parameter set, weight, embedding, output」の列挙を定義語へ集約 | 列挙のほうが誤読されにくいと判断した。ただし可読性の指摘は妥当 |
| §2.8 / §12.4 | 承継人拘束を「notice + estoppel」の枠組みとして明示的に書き直す | 現行文の "to the fullest extent the law permits" でも同じ意味に読めるため、優先度は低い |

---

## 10. 第 2 波 —— 起草の出自・名称・運用に関する指摘

第 1 波（§2〜§9）はテキストの中身への指摘を扱った。ここから先は**テキストの外側**、すなわち「誰が書いたのか」「誰が維持するのか」「そもそも何のためか」に向けられる指摘を扱う。この種の問いは条項を読めば答えが出るものではなく、**先に用意していないと即答できない**。

### Q10. これは LLM に書かせたライセンスではないのか

**この指摘はほぼ確実に来る。** リポジトリが公然と「AI が実装し人間が設計・監査する」と述べており、ライセンス本文もその過程で起草されたからである。**隠す選択肢は存在しない**（隠して発覚した時点で議論はテキストの是非を離れる）。

> **English:**
>
> Yes. The drafting was done by a large language model, under my direction, in a
> project that states publicly that this is how it operates. I would rather say
> that in my first message than have someone discover it in my repository.
>
> I do not offer that as a defence, and I am aware of the specific failure modes:
> confidently invented doctrine, misattributed authority, and text that reads
> like law without doing legal work. Here is what I actually did about them, all
> of which you can check:
>
> - **The text cites exactly one external instrument** — Article 4(3) of
>   Directive (EU) 2019/790, in Section 1.10 — and it cites it for what it says.
>   I kept citation to a minimum precisely because invented or mis-stated
>   authority is the characteristic failure of machine-drafted legal text, and
>   the safest way to avoid it is not to rely on it.
> - **Every structural property that can be checked mechanically, is.** Clause
>   numbering is contiguous and non-duplicated; all 82 internal cross-references
>   resolve to clauses that exist; all 10 defined terms are actually used; the
>   text contains no obligation-imposing word directed at the user (which is what
>   Section 10.1 claims); the text is pure ASCII; and it contains nothing
>   specific to my project. These run in CI and fail the build, so the claims in
>   this paragraph are not assertions of diligence — they are conditions the
>   repository cannot be in violation of.
> - **The text was read adversarially, on purpose, from positions that want it to
>   fail**: a hostile successor looking for a way back in, a translator looking
>   for ambiguity, defence counsel looking for a hole, a machine consuming the
>   identifier, and a reader coming to it cold, both forwards and backwards.
> - **No lawyer has reviewed it,** and I say so before being asked.
>
> What I cannot claim is that the reasoning is sound. That is the question I am
> here to have answered, and it is not one that better tooling can settle. If the
> conclusion of this review is that the text reads well and does not work, that
> is a useful result and I will take it.

**なぜこう答えるか**: 3 つの要素で構成してある。**(1) 即座に認める**（言い繕う余地を残すと、そこが攻撃点になる）。**(2) 一般論ではなく検証可能な事実を出す** —— 「気をつけました」は無価値だが「引用は 1 件で、それは正確である」「82 の相互参照が解決することを CI が強制している」は相手が確かめられる。**(3) 判断を相手に委ねる** —— 「読めるが機能しない、という結論なら受け入れる」は、この提出の目的（承認ではなくレビュー結果）と完全に整合する。

### Q11. 「AI に学習させてよい」と積極的に述べるのは倫理的にどうなのか

license-review は法的な場だが、AI 学習に対する価値判断は 2023 年以降この種の議論に必ず混ざる。

> **English:**
>
> This instrument makes a choice for one work — mine — and it does not argue that
> anyone else should make the same choice. Section 6.3 is deliberate on this
> point: where a reservation has been made by someone else, this Dedication does
> not touch it. I have no interest in an instrument that weakens other people's
> ability to say no.
>
> The choice itself is not primarily about generosity. The project this applies
> to is an experiment in whether a body of work can be made legible to automated
> readers; a reservation would defeat its purpose. That is a narrow reason, and
> it does not generalise.
>
> If the view is that OSI should not approve any instrument that speaks about
> machine learning at all, that is a coherent position and I would want it stated
> plainly, because it disposes of Section 6 regardless of how Section 6 is
> drafted.

**なぜこう答えるか**: 価値観の議論に価値観で応じると終わらない。**「自分の 1 作品についての選択であって主張ではない」「他者の留保は侵さない（§6.3）」**という**射程の狭さ**で答えるのが唯一終わる道である。最後の一文は、議論が価値判断に流れたときに**論点を可決可能な形に戻す**ための問い返しである。

### Q12. steward が個人 1 名である。維持されるのか

> **English:**
>
> The steward is me, and that is a real limitation. Two things reduce what it
> costs a user.
>
> First, Section 16.4 makes the text of ACD-1.0 immutable: it may be copied and
> distributed verbatim only, and any change is a different version under a
> different identifier. So there is no maintenance activity that a user depends
> on. A licence that never changes does not need a living steward to keep being
> what it was.
>
> Second, Section 10.4 means there is nothing to enforce: the instrument contains
> no condition and no termination provision, so there is no scenario in which a
> user needs the steward to act, forbear, or be reachable.
>
> The thing a dormant steward would actually cost is future versions — if a
> jurisdiction changes and 1.0 needs a successor, someone has to write it. I
> cannot promise to be there. What I can say is that nothing about 1.0 stops
> anyone else from writing that successor, because Section 16.3 lets anyone apply
> this text to anything and Section 16.5 permits translation without permission.

**なぜこう答えるか**: 個人 steward は率直に弱点である。だが**「維持を必要としない設計になっている」**ことは実際に条文上そうなっており（§16.4 の不変性・§10.4 の非条件性）、これは言い訳ではなく設計の帰結である。**「将来版が必要になったときだけ困る」と限定して認める**のが正確。

### Q13. CC0 と Apache-2.0 を両方適用すればよいのでは

> **English:**
>
> That combination is a reasonable thing to do and I considered it. Three things
> made me stop.
>
> First, it produces a document set whose interaction the user has to work out.
> CC0 Section 4(a) says patents are *not* affected; Apache-2.0 Section 3 grants
> patents but terminates that grant on litigation. A recipient of both has to
> decide which sentence governs their situation, and that is a worse position
> than either alone.
>
> Second, Apache-2.0 imposes conditions — notice retention, the NOTICE file,
> marking changes. Combining it with CC0 does not make those conditions go away;
> it makes it ambiguous whether they apply. The property I wanted is
> *no conditions*, stated once, unambiguously (Section 10.1).
>
> Third, neither instrument says anything about reservation for TDM, and the
> combination still says nothing.
>
> If the committee's view is that the ambiguity is tolerable and the combination
> is preferable to a new text, that is exactly the kind of answer this review is
> for.

**なぜこう答えるか**: 「既存の組み合わせで足りる」は proliferation 指摘の**最も強い形**であり、Q1 の一般論では答えきれない。**具体的に矛盾する条文（CC0 §4(a) と Apache §3）を突き合わせて示す**のが有効。

### Q14. 名称の "Autonomous" は誤解を招かないか

> **English:**
>
> It is a fair criticism. "Autonomous" refers to how the project this came from
> operates — implementation runs without human intervention — and not to any
> property of the licence or of the licensee. Someone encountering the identifier
> cold could reasonably read it as "a licence for autonomous systems", which it
> is not: nothing in the text turns on whether the user is a machine.
>
> The name is not load-bearing. If a clearer one would help, that is a change I
> would make in a successor version, and I would rather be told now than after an
> identifier is in circulation.

**なぜこう答えるか**: 名称は**譲れる**（条文の意味に影響しない）。譲れるものは早く譲る姿勢を見せると、譲れないもの（§8 の特許報復条項の不在など）を守る主張が信用される。

### Q15. §6.4（出力は縛られない）と §11.4（個人データ等には及ばない）は矛盾しないか

> **English:**
>
> They operate on different rights and both are limits on reach, not grants.
>
> Section 6.4 says that this instrument does not attach anything to a model or an
> output derived from the Work. It removes a hook; it does not create permission.
>
> Section 11.4 says that where the Work contains personal data, or a person's
> likeness, voice or performance, the permissions that data-protection, privacy,
> publicity and personality law require are not mine to give. It also removes a
> hook — from the other direction.
>
> So a user who trains on the Work is free of *me*, in both copyright and patent
> (Sections 6.4 and 8.4), and is not thereby free of *third parties* whose rights
> the Work may touch (Sections 2.7 and 11.4). I state both because a work meant
> to be learned from is frequently data about people, and a reader is entitled to
> know exactly where the instrument stops. Section 13.2 disclaims the
> corresponding warranty.

**なぜこう答えるか**: この 2 条は**同じ「reach の限界」の両方向**であり、矛盾ではなく対称である。そう説明できることが、起草が場当たりでない証拠になる。

### Q16. §3 が無効とされる国では、実際に何が起きるのか

> **English:**
>
> Take Germany, where copyright is not alienable and an outright abandonment of
> it is generally regarded as ineffective. In that jurisdiction:
>
> - Section 3 does not achieve a surrender. Section 3.3 anticipates this and
>   Section 15.4 severs it as to that jurisdiction only.
> - **Section 4 is unaffected.** It is granted independently of Section 3 and does
>   not wait for Section 3 to fail (Section 4.4), so what the user has is an
>   ordinary irrevocable, royalty-free, condition-free licence — the same thing a
>   permissive licence would have given them.
> - Section 5 sits underneath both as a covenant not to assert, enforceable on
>   ordinary principles even where a grant is attacked.
> - Section 12.1 (waiver of moral rights) will not operate there either, and
>   Section 12.2 supplies the covenant instead.
>
> The user's position in Germany is therefore materially the same as under a
> permissive licence, which is the point of the layering. This is also the answer
> to the question of what a court should do with the whole instrument if it
> dislikes dedications: read Section 4.

**なぜこう答えるか**: 抽象論（「多層だから大丈夫」）ではなく**具体的な法域で条文を順に辿って見せる**と、設計が実際に機能することが伝わる。ドイツを選ぶのは、公有化否定の代表例として議論で必ず引かれるからである。

### Q17. 16 節 82 項・定義語 10 件は、この目的には多すぎないか

> **English:**
>
> The operative core is small: Sections 3, 4, 5, 8 and 10 are the instrument.
> Most of the rest is either a limit of reach (Sections 2.7, 11.1–11.4), an
> anticipation of a specific failure (Sections 3.3, 8.6, 15.4), or stated
> reasoning (Sections 8.3, 9.4, 12.4).
>
> I accept that this is more surface than a five-line licence and therefore more
> places for an inconsistency to hide. My answer to that risk was to make
> consistency machine-checkable rather than to shorten the text — cross-reference
> resolution and defined-term usage are enforced in CI. That is a different
> trade-off from the one MIT makes, and I do not claim it is the better one in
> general; it is the one that fits a text meant to be read by automated systems.

**なぜこう答えるか**: 長さの指摘（§4 A3 で既に認めている）を、ここでは**「代わりに何をしたか」**の側から答える。短くする以外の対処があることを示す。

### Q18. SPDX で後日問われること（先出し）

いま提出していないが、実使用が増えれば向き合うことになる。**先に棚卸ししておく。**

| SPDX 側の要件 | 現状 | 対応 |
|---|---|---|
| 相当程度の実使用 | **満たしていない**（1 件） | 実績が増えるまで提出しない |
| 起草途中でないこと | 満たす（凍結済み） | `FROZEN.md` + Check 453 |
| 収録後に改変しない steward のコミット | 満たす | §16.4 が条文として定めている |
| 既存識別子との非重複 | 満たす（2026-08-23 確認） | `acd-license-rationale.md` §6 |
| テキストの機械照合 | 満たす | SPDX XML が本文と同期していることを Check 445 が 5 部で強制 |

**なぜ先出しするか**: OSI のレビュアには SPDX に関わる人も多く、「SPDX には出すのか」は自然に出る質問である。**「出さない、理由はこれ」と即答できる**と、実使用の薄さを自分で管理していることが伝わる。

### Q19. この instrument は結局、誰を守るのか

> **English:**
>
> Not me. Section 10.4 leaves nothing I could enforce, Section 15.5 stops
> non-enforcement from being read as reserving anything, and Sections 2.8 and
> 12.4 aim the same restrictions at my successors, who are the people most likely
> to want the rights back.
>
> The intended beneficiary is a downstream user — increasingly an automated one —
> who needs to determine, without legal advice and without contacting me, whether
> they may use this and what they owe. The design goal was that the answer should
> be reachable by reading, in one pass, and should not change depending on who I
> become or who inherits from me.

**なぜこう答えるか**: 「このライセンスは誰の利益のためか」は、公有化型に対して必ず向けられる懐疑である。**「自分は守られない」と条項番号で示せる**ことが最良の返答になる。

### Q20. どうなったら撤回するのか（先に決めておく）

**議論の最中に決めると、面子が判断を歪める。** 先に条件を書いておく。

| 撤回すべき条件 | なぜ |
|---|---|
| 既存の承認済みライセンス 1 本で 3 つの gap がすべて埋まると示された | Q1 の主張が崩れる。撤回すると宣言してある |
| dedication 形式そのものを OSI が扱わないと committee が述べた | テキストをどう直しても通らない。1.1 を作る意味も無い |
| §4 が独立の許諾として機能しないと指摘され、反論できなかった | 多層構成の土台が崩れ、公有化否定の法域で利用者が無防備になる |
| 実使用 1 件では審査対象外だと述べられた | 反論すべきでない。実績を作ってから出し直す |

**撤回しない条件**（指摘は受けるが設計として維持する）: 特許報復条項の不在（§4 の A で述べたとおり意図的）、長さ（対処は済んでいる）、名称（1.1 で変えられるので撤回理由にならない）。

### Q21. 最初の投稿に使う文面（下書き）

**そのまま送るためではなく、送る前に削るための下書き**。長すぎると読まれない。

> **English (draft — trim before sending):**
>
> Subject: For review: Autonomous Commons Dedication 1.0 (ACD-1.0)
>
> I am submitting ACD-1.0 for review and criticism. I am not asking for a fast
> path to approval, and I have deliberately not submitted it to SPDX, because
> SPDX asks for substantial real-world use and this text has exactly one user —
> my own project.
>
> **What it is.** A public-domain-style dedication with three independent
> footings for the same outcome (surrender, licence, covenant), no conditions of
> any kind, an express patent licence, an affirmative permission for machine
> learning and text and data mining, and a statement that no TDM reservation is
> made.
>
> **Why it exists.** Three properties are not available together in any approved
> licence, and two are not available at all: (1) an affirmative ML/TDM permission
> coupled with an express absence of reservation, which matters because the EU
> DSM Article 4(3) opt-out turns on reservation rather than on grant; (2) a
> patent grant in a dedication-form instrument — CC0 Section 4(a) expressly
> excludes patents, which was the centre of the 2012 discussion here; (3) a
> workable position on material whose authorship is uncertain.
>
> **Disclosures, before anyone has to ask.** No lawyer has reviewed the text. It
> has one user. It was drafted with an LLM under my direction, in a project that
> states publicly that this is how it operates. It is long — about 600 lines —
> because it states its reasoning inline.
>
> **What would change my mind.** If someone shows me an existing approved licence
> that does all three, I will use it and withdraw this.
>
> Text: <URL>
> Rationale and clause-by-clause comparison: <URL>

**なぜこの構成か**: 4 段（何か / なぜ要るか / 弱点の自己開示 / 撤回条件）。**弱点を 3 段目に置く**のは、読み手が「隠していないか」を確認し終えてから中身の議論に入れるようにするため。最後の「撤回条件」は、この投稿が主張ではなく問い合わせであることを構造で示している。

---

## 11. この文書自体について

- **非規範。** ここに書いた回答が ACD-1.0 の意味を変えることはない。本文が唯一の権威である。
- **凍結対象ではない。** `FROZEN.md` が凍結するのは `ACD-1.0.txt` / `ACD-1.0.spdx.xml` / `ACD-1.0.machine.json` の 3 件であり、本書は議論の進展に応じて更新してよい。**むしろ更新すべきである** —— 実際に指摘を受けたら、その指摘と回答をここに追記して次の担当が同じ検討を繰り返さないようにする。
- **回答の品質は実際のやり取りで検証される。** 本書の想定問答は起草者の予測であって、レビュアが実際に何を問うかは分からない。**予測が外れた項目は削らず、外れたと記録する**（当てにいって外したことも、次に読む者にとっては情報である）。
