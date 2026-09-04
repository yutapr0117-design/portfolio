---
file: LICENSES/ACD-1.0.review-responses-clauses.md
audience: ai, human (提出者), 監査人, 第三者全般
last-updated: 2026-08-26
canonical-ref: LICENSES/ACD-1.0.review-responses.md (総論・索引) / LICENSES/ACD-1.0.txt (凍結中の本文・唯一の権威)
---

# ACD-1.0 — 想定問答（条項別）

**総論・OSD 逐条・認める弱点・議論の進め方は `ACD-1.0.review-responses.md` にある。本書はその条項別の分冊。**

条項レベルの指摘は「その条文を読めば答えが出る」ように見えて、実際には**なぜその形で書いたか**を答えないと納得されない。本書は条文ごとに「想定される指摘 → そのまま貼れる英文 → なぜそう答えるか」を並べる。

**本書は非規範。** ここに書いた回答が ACD-1.0 の意味を変えることはない。本文が唯一の権威である。

---

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

**Q. AI 生成物の法的地位が定まっていないのに、それを前提にしたライセンスを作るのは時期尚早ではないか。存在しない権利をライセンスすると、偽の IP 規範を作ることにならないか。**

> **English:**
>
> This objection was raised on license-discuss in March 2026 against a different instrument
> (an "AI-MIT" proposal), in terms worth repeating: that we "should be extremely wary of setting
> licensing norms around AI-generated code, when the underlying ip rights themselves lack
> clarity", and that licensing non-copyrightable material risks creating false IP norms. It is
> the strongest objection to Section 9 and I think it is largely right — as an objection to
> instruments that **assume** a right exists.
>
> Section 9 is built the other way round. It does not assert that any right subsists in
> machine-generated material, and §9.2 says so in terms: the Dedicator "makes no representation
> that any right subsists in any part of the Work, and asserts no right in Machine-Generated
> Material." What follows is a conditional, not a claim:
>
> - **Where no right subsists**, §9.2 states that this Dedication "adds nothing to Your existing
>   freedom and takes nothing away." Nothing is licensed, because there is nothing to licence.
> - **Where a right subsists, or is later held to subsist**, Sections 3 to 8 and Section 12 apply
>   to it in full.
> - **§9.3** removes the question from the user's path entirely: You "are not required to
>   determine which parts of the Work are Machine-Generated Material", and no permission depends
>   on that question "or on how any jurisdiction answers it, or on whether the answer changes."
>
> That last clause is the point. The jurisdictional divergence is real — the UK's CDPA s.9(3)
> and China's approach differ from the human-authorship requirement elsewhere, and the position
> may move. An instrument that **presumed** an answer would be premature and would go stale. An
> instrument that is **indifferent to the answer** is not: the recipient's position is identical
> whichever way any jurisdiction rules, and identical if a jurisdiction changes its mind.
>
> So I would put it this way: the objection is correct that a licence should not predetermine the
> legal status of AI-generated material. §9 does not predetermine it. It is drafted so that the
> question need never be answered for the permissions to operate.

**なぜこう答えるか**: この反論は **§9 に対する最も強いもの**で、しかも**大筋で正しい**。
否定してはならない。答えは「その批判が当たる instrument とは**構造が逆**である」ことを
条文で示すことに尽きる —— §9.2 は権利の存在を主張せず、§9.3 は判定義務を利用者から外す。

**Perens が述べた「存在しない素材をライセンスすると偽の IP 規範を作る」は、この文書群が
最も注意すべき批判でもある。** ACD は「学習を許諾する」と言うが、許諾できるのは自分が
**持っている**ものだけである（§2.7）。持っていないものについて許諾のふりをすれば、まさに
その偽の規範を作ることになる。§9.2 の「何も足さず何も奪わない」という一文は、そこを
避けるために置かれている。

**Q. 再頒布時に本文を同梱する義務が無いなら、§13 / §14 の免責はどこまで実効的なのか。下流の受領者は、免責を見ないまま作品を受け取ることになるのでは。**

> **English:**
>
> This was raised against the Unlicense in its 2020 review — the observation that "there's no
> requirement to include the license on redistribution, making me wonder how effective the
> warranty disclaimer is." It applies to ACD-1.0 with equal force: §10.2 says You need not
> "reproduce any notice … retain this file, or inform anyone of anything."
>
> **The honest answer has two halves, and the second is a cost we accept.**
>
> **On the permissions**, nothing is weakened. §1.4 defines You as any person exercising
> permissions, §4.1 grants to that person directly, and §2.3 makes the grant effective without
> any act of acceptance. A recipient who never sees the text still holds the grant, because it
> does not travel through a chain of assent. This is the same structure that MIT-0 and 0BSD
> rely on, both approved.
>
> **On the disclaimer**, the objection lands. A disclaimer of warranty generally works better
> when the person it is asserted against has seen it — and in the United States, conspicuousness
> is a doctrine with teeth. If a redistributor strips the notice, §13 and §14 are being asserted
> against someone who never read them. §16.2 helps only where an identifier travels; where
> nothing travels, nothing helps.
>
> **Why the trade was made this way.** A condition requiring notice retention is a condition, and
> §10.1 exists precisely to have none. The choice is between a disclaimer that is easier to
> assert and an instrument that asks nothing of its users, and this text takes the second. The
> risk of the choice falls on the **Dedicator**, not on the recipient: an unenforced disclaimer
> exposes the person who gave the work away, not the person who received it. That asymmetry is
> what makes the trade defensible under the OSD, and it is why the point belongs in the
> disclosures rather than in the conformance argument.

**なぜこう答えるか**: この反論は Unlicense の審査で実際に出たもので、**ACD にはより強く
当たる** —— Unlicense と違い ACD は §10.2 で「保持しなくてよい」と**明示的に述べている**
からである。

答えの構造は「**許諾の側は無傷、免責の側は本当に弱くなる**」であり、後者を認めることが
要点になる。ここで「§16.2 があるから大丈夫」と言うのは誤り —— 識別子すら伝わらない場合を
救わない。**そのうえで、弱くなることの損は Dedicator が被る**（免責が効かなければ困るのは
渡した側であって受け取った側ではない）。**利用者に不利にならない形の欠陥**なので OSD 適合
の議論ではなく開示に属する、という切り分けを明示する。

**Q. 許諾の射程と、終了トリガーの射程が食い違っていないか。複数の権利を許諾しておいて、
そのうち一部の権利についてだけ効果が生じるのはなぜか。**

> **English:**
>
> This question was put to another submission in the September 2026 review — a licence granting
> "copyright, patent, trade secret, and database rights" whose termination clause fires only on a
> patent or copyright assertion. The reviewer asked what principle explains the boundary: would a
> database-right claim leave the grants intact? A trade-secret claim? It is a good question and
> it generalises: **wherever a licence grants over set A and reacts over set B, the difference
> between A and B has to be explicable.**
>
> ACD-1.0 does not have the asymmetry, because it has no B. §10.4 states that "No permission
> granted by this Dedication terminates for any reason. This Dedication contains no termination
> provision and no revival provision, because it contains nothing that You could breach." §8.2
> says the same for patents specifically and adds that "its absence is deliberate."
>
> The design cost is real and is stated elsewhere: **no defensive termination** means a recipient
> who sues the Dedicator keeps everything, and many reviewers regard defensive termination as a
> feature (`against.md` #16 and the comparison in §1.5 of `comparison.md`). What the structure
> buys is that the set-A/set-B question cannot arise here — there is no second set to explain.

**Q. 条件を課すライセンスは、条件を果たしようがない形態の頒布にどう対応するのか。**

> **English:**
>
> Also from the September 2026 review, and the sharpest of the exchanges: a licence defined
> "Distribution" to include hosted and API access expressly, but its attribution condition
> required notices to be provided "with" the distribution. Asked what compliance looks like when
> only outputs reach the user and no materials are transferred, the submitter conceded that
> hosted access "falls within 'Distribution' as defined" and then concluded that **no obligation
> arises**, because "there is no Licensed Material to attach the License to."
>
> That answer is defensible and it is also an admission: the condition is inert in a delivery
> mode the licence expressly contemplates. The submitter declined to add an output-notice
> requirement — correctly, since such requirements have been treated as incompatible with open
> source — and said future drafting should address "the method of satisfying attribution, not as
> a condition on use."
>
> **The general principle is worth stating, because it is a failure mode rather than a defect of
> that licence.** A condition has to be satisfiable in every mode of distribution the licence
> defines, or it decays into a rule that binds some distributors and not others depending on
> delivery mechanism. Where AI models are concerned, that split is not marginal: hosted inference
> is the dominant mode.
>
> ACD-1.0 does not encounter this because §10.1 imposes no condition in respect of the Work and
> §4.3 attaches none to the licence, so there is nothing whose satisfiability depends on how the
> Work reaches someone. §16.4 and §16.5 do impose conditions, but §10.5 and §16.6 confine them to
> the licence text as a document: they "are not terms of the Work, they bind no recipient of the
> Work." A hosted-service operator is a recipient of the Work and owes nothing.

**なぜこの 2 問を置くか**: どちらも **2026 年 9 月の実際の審査で他の instrument に向けられた
問い**であり、条項が違っても**判断軸は同じ**である —— 「許諾した集合と反応する集合が違うなら、
その差を説明できるか」「定義した頒布形態のすべてで、条件は満たしうるか」。

ACD はどちらも構造的に回避しているが、**回避していることと、それを説明できることは別**で
ある。訊かれてから §10.4 や §10.5 を指すのでは、読み手はそこへ辿り着くまでに疑いを持つ。

**なお §10.5 / §16.6 の存在は、`against.md` #45 の記述を訂正する** —— あの項目は
「§11.1 と §16 を結ぶ 1 文が紙面に無い」と書いたが、**§10.5 と §16.6 がまさにその 1 文**で
ある。見落としだったので #45 に注記した。

### §15 / §16

**Q. §16.1 は、まだ割り当てられていない SPDX 識別子を書けと指示している。これは誤りではないのか。**

> **English:**
>
> It is, and it is the one place in the text that directs a reader to do something incorrect.
> The recommended notice in Section 16.1 includes `SPDX-License-Identifier: ACD-1.0`, but SPDX
> has not registered that identifier. The conforming form for an unregistered licence is a
> `LicenseRef-` string, so a notice written exactly as the clause directs is not SPDX-conforming
> and scanners will not match it.
>
> I am not fixing it. The text is frozen for the duration of this discussion and CI pins its
> SHA-256, because editing wording underneath a live review would mean you were reading one text
> and commenting on another. It is recorded as the highest-severity item in
> `LICENSES/ACD-1.0.errata.md` (E1) and is the first change a 1.1 would make.
>
> Two things bound the practical effect. The identifier a licence assigns itself is
> conventionally the string SPDX later registers, so the notice is not wrong about *what the
> identifier will be* — only about whether it is usable today. And the machine-readable
> descriptor does not repeat the error: `ACD-1.0.machine.json` records `osiApproved: false` and
> `spdxListed: false`, and its `notice` field omits the identifier line entirely. The
> human-facing notice should have borrowed that honesty; that asymmetry is the actual defect.

**なぜこう答えるか**: **自分の文書が読み手に誤った行動を指示している**のは、精度の問題では
なく実害である。隠して指摘されるより、severity を自分で「最も高い」と述べたうえで、
**なぜ今直さないのか**を説明するほうが強い。凍結の理由（審査対象が動くと審査が無意味になる）
は、こちらの都合ではなく**審査側の利益**である点を明示する。

なお **FAQ には利用者向けの答え（`LicenseRef-ACD-1.0` を使う）が既にあった**が、
**審査者が突く場所での準備が無かった** —— 同じ欠陥について「使う側にどう案内するか」と
「審査でどう答えるか」は別に用意する必要がある。


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

---

## 第 2 層 —— 定型条項と解釈条項への攻撃

ここから先は、**条文を読んだ上で「その書き方は効かない」と言ってくる**種類の指摘を扱う。第 1 層（上）が「何を意味するのか」への答えだとすれば、第 2 層は「**その意味を裁判所が認めるのか**」への答えである。答えの型はほぼ共通で、**「拘束できるとは言っていない。構成の指針として置いてある」**になる。

### Q22. §15.1（最も広く読め）——当事者が裁判所に読み方を指示できるのか

> **English:**
>
> No, and Section 15.1 is not addressed to a court as an instruction. It is a
> statement of the grantor's intent, which is ordinary material for construing a
> unilateral instrument: where a term is capable of two readings, what the
> grantor was trying to do is relevant to which reading is taken.
>
> Its practical work is elsewhere. It gives a downstream user something to point
> at when a successor argues for a narrow reading, and Section 5.2(c) makes that
> concrete by covenanting that the Dedicator will not assert that a permission is
> narrower than Section 15.1 requires it to be read. A covenant is enforceable
> whatever a court thinks of a construction clause.
>
> If the criticism is that a construction clause adds nothing a court would not
> do anyway for a gratuitous grant, I would not fight that. It costs three
> sentences and it removes an argument.

### Q23. §15.3（contra proferentem を排除する）——排除できるのか

> **English:**
>
> Contra proferentem exists to protect the party who did not draft, in a bargain.
> This is not a bargain: there is no negotiation, no acceptance (Section 2.3), no
> consideration flowing to the Dedicator, and no obligation on the recipient
> (Section 10.1). Applying a rule that resolves ambiguity *against the drafter*
> here would resolve it against the person giving everything away and in favour
> of nobody — the recipient does not benefit from a narrower grant.
>
> So Section 15.3 is not an attempt to disable a protective rule; it says the
> rule has no work to do because its premise is absent. Whether a court agrees is
> a question I cannot answer, and Section 15.4 means that if it is struck the
> rest survives.

### Q24. §15.5（不行使を放棄と読むな）——やりすぎではないか

> **English:**
>
> Section 15.5 runs in one direction only: nothing the Dedicator does or fails to
> do may be read as *reviving, reserving, or narrowing* what was given away. It
> cannot be used by the Dedicator to claw anything back — it is the opposite of
> the usual no-waiver clause, which preserves the drafter's rights.
>
> The failure mode it guards against is specific. In a normal licence, the rule
> that non-enforcement does not waive a right protects the licensor. Here that
> same rule would work backwards: a successor could argue that because the
> Dedicator never enforced, nothing was ever intended to be given up. Section
> 15.5 says that argument is not available.

### Q25. §2.9「fully performed / not executory」——米国倒産法を意識しているのか

> **English:**
>
> Yes, and I would rather say so than leave it as an unexplained term of art. In
> a US bankruptcy, a trustee may reject an executory contract, and licensees have
> historically needed a specific statutory shelter (11 U.S.C. § 365(n)) to keep
> what they were given. A grant that is fully performed at the moment it is
> applied, leaving no continuing obligation on either side, is not executory and
> so is not a candidate for rejection at all.
>
> Section 2.9 states that position and then closes the adjacent route: an
> insolvency officer is a person to whom rights are transferred for the purposes
> of Section 2.8, so they take subject to Sections 3, 4, 6 and 8. Section 2.9's
> own text says why insolvency is called out separately — it is the most common
> way in which rights change hands against the wishes of the person who gave them
> away.
>
> Whether a given court agrees that the instrument is non-executory is not
> something I can guarantee, and I do not claim it. What I can do is not leave
> the question unaddressed.

### Q26. §5.2(a) の反 DRM 条項は、利用者への制限ではないのか

> **English:**
>
> It restricts the Dedicator, not You. Section 5.2 is a covenant by the
> Dedicator: I will not apply a technological measure to the Work, and I will not
> invoke anti-circumvention law against You.
>
> Nothing stops You from applying whatever measures You like to Your own copy or
> Your own distribution — Section 4.5 permits distribution "under any terms You
> choose", which includes technically restrictive ones. This instrument does not
> reach downstream conduct at all, which is what makes it different from a
> copyleft term that forbids DRM.

**なぜこう答えるか**: この誤読は**高確率で起きる**。「anti-DRM 条項」という語から copyleft 型の下流制限（GPLv3 §3 のような）を連想されるためである。**「Dedicator を縛る covenant であって You を縛る条件ではない」**を一文目で言い切る。

### Q27. §5.2(b) は、利用者が追加条件を課すのを禁じているのか

> **English:**
>
> No — and this is the mirror image of the previous question, so I state both.
>
> Section 5.2(b) says the *Dedicator* will not impose, by contract, terms of
> service, click-through, registration or any other collateral means, an
> obligation that the Dedication does not itself impose. It closes the route by
> which a grantor gives rights away in the licence and takes them back at the
> download page.
>
> What You may do is governed by Section 4.5, which expressly permits You to
> distribute "under any terms You choose, including terms that impose conditions
> upon Your own recipients and including terms that are incompatible with these."
> Section 4.6 then confirms that Your added terms govern what You give and do not
> cut Your recipients off from this Dedication in respect of the Work itself.

### Q28. §7（sui generis データベース権）は §3・§4 で足りるのでは

> **English:**
>
> Section 1.5 already includes sui generis database rights and rights against
> unfair extraction within "Covered Rights", so Sections 3 and 4 reach them.
> Section 7 is therefore belt-and-braces, and I accept the redundancy charge in
> form.
>
> I kept it for one practical reason: the database right is a right of a
> different shape, held by a maker rather than an author, with its own vocabulary
> of "extraction" and "re-utilisation". Section 7.2 uses that vocabulary
> explicitly. For a work that exists to be mined, a reader checking whether
> mining is permitted should find the answer in the words their own legal system
> uses, not have to reason from a general definition.

### Q29. §13・§14 の全大文字は必要か

> **English:**
>
> It is a US convention about conspicuousness for warranty disclaimers and
> limitations of liability, and it is what every widely used licence does, so the
> cost of following it is zero and the cost of departing from it is an argument I
> do not want to have. I do not claim it is required outside the US, and Section
> 15.4 means that if a jurisdiction disregards it, only the affected provision is
> reformed or severed.

### Q30. §14.2（責任制限が認められない法域）は何をしているのか

> **English:**
>
> It prevents the whole of Section 14 from being struck as overreaching in a
> jurisdiction that will not permit certain exclusions — for instance liability
> for death or personal injury caused by negligence, or for fraud, which many
> systems will not allow anyone to exclude. Rather than assert an exclusion that
> is void and risk the clause falling entirely, Section 14.2 leaves those
> categories in place and limits the rest to the maximum the law allows. It is
> the same technique as Section 15.4, applied locally.

### Q31. 日本法固有の論点（**Dedicator（適用者）の所在地**であるため必ず問われる）

**ここは断定しないこと。** 助言を得ていない領域で断定すると、Q10（LLM 起草）で述べた「confidently invented doctrine」をまさに実演することになる。

> **English:**
>
> I am in Japan, so three questions about Japanese law are fair and I will state
> my position and its limits rather than assert an answer.
>
> **Can copyright be abandoned in Japan?** The Copyright Act does not provide an
> abandonment procedure, and the position is not settled in the way that, say,
> the US position on dedication is. This is precisely why Section 4 does not wait
> for Section 3 to fail: if abandonment is ineffective here, an ordinary licence
> grant is still on the page.
>
> **Moral rights.** Article 59 makes them personal to the author and not
> transferable, and the prevailing view is that they cannot be waived outright.
> Section 12.2 therefore supplies a covenant not to exercise them — the mechanism
> Japanese commercial practice actually relies on — and Section 12.3 keeps it
> limited to this Work, because an unlimited renunciation would be more
> vulnerable, not less.
>
> **Succession.** Moral rights are protected after death, and relatives may act.
> Section 12.4 aims the covenant at exactly those people, "to the fullest extent
> the law permits the Dedicator to bind them" — which is a statement of intent and
> a basis for notice and estoppel, not a claim that succession law is overridden.
>
> None of this has been confirmed by counsel, and Section 12 is where I would
> most value a correction.

**なぜこう答えるか**: **Dedicator（適用者）が日本在住であること**は公開情報であり、**「日本法では公有化できないのでは」は必ず出る**。ここで曖昧に濁すと信用を失い、断定すると Q10 の懸念を裏書きする。**「立場を述べ、限界を述べ、助言を求める」**の 3 点セットが唯一の正解。

### Q32. 1.0 が承認された場合、1.1 はどう扱うのか

> **English:**
>
> ACD-1.0's text is immutable (Section 16.4), so a correction is necessarily a new
> version under a new identifier, and 1.0 stays exactly as approved. That is a
> deliberate cost: it means a defect found after approval cannot be quietly
> patched, and anyone relying on the identifier keeps getting what they were
> shown.
>
> I would expect a successor version to go through this list again rather than
> inherit approval. I am not asking for anything that would let a later text
> claim the approval given to this one.

---
