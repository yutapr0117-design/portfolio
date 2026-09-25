---
file: LICENSES/ACD-1.0.review-responses-clauses.md
audience: ai, human (提出者), 監査人, 第三者全般
last-updated: 2026-09-20
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

**Q. §6.2 が扱っているのは仮想の問題ではないのか（誰が signal を置いたかなど、実際に争われるのか）。**

> **English:**
>
> It has been litigated, and the two things Section 6.2 turns on were the two
> things the court had to decide. On 10 December 2025 the Hanseatisches
> Oberlandesgericht dismissed the appeal in the *Kneschke v. LAION* line of
> cases (Az. 5 U 104/24). According to the court's own press release, the
> reservation had been placed not by the photographer but by the picture agency
> he used, and the court held that such a reservation *"auch ihm als
> Rechtsinhaber zugerechnet werden"* must — it is attributed to the rightsholder.
> It then held that the reservation nonetheless failed because it did not have
> *"die gesetzlich vorgesehene Form (Maschinenlesbarkeit)"*, the form the statute
> requires. Section 6.2 addresses both: it declines to read a signal attached to
> the Work as a Reservation whoever placed it, and it does so whether or not the
> signal is machine-readable — which is wider than UrhG 44b 条 3 項, since that
> provision only reaches machine-readable reservations.
>
> **Three qualifications belong in the same answer.** The decision is **not
> final**: the Senat admitted a Revision to the Bundesgerichtshof. What I have
> read is the **court's press release, not the judgment** — the release says an
> anonymised full text can be requested, and I have not requested it. And the
> same court held that the dataset's creation was **independently justified as
> scientific research** under UrhG 60d 条, notwithstanding that commercial
> providers could use the dataset; where that limitation applies, a reservation
> is beside the point, so Section 6's marginal value in Germany is smaller for
> research institutions than this answer might otherwise suggest.

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

#### §6.4 を、原理ではなく **license-review の記録** から論じる（2026-09-06 に一次資料で確認）

これまで §6.4（「Computational Use から派生した model / parameter set / weight / embedding /
output は、この Dedication によっても Dedicator のいかなる Covered Right によっても encumber
されない」）は**原理から**論じてきた。**同じ結論を、このリストの記録そのものから論じられる。**

2025-03、ModelGo の初期草案が出力へ notice を要求していた件について、`license-review` で
次のやりとりがある（**アーカイブ本文から直接引いた。提出者による後の要約ではない**）:

> **Moming Duan**（提出者・2025-03-03）: "I am also considering whether we could narrow this
> clause so that it only applies when distributing a collection of outputs, requiring disclosure
> of the info of original model and its license."
>
> **Simon Phipps**（*in a personal capacity* と明記・同日）:
> "That sounds like **a restriction or condition on mere use. That would not be open source.**"
>
> **Richard Fontana**（同日）: "This would be akin to **putting an editor under a license that
> required any file created with the editor to have an attribution notice.**" さらに前例に触れて
> いる —— "I am reminded of the Kyle Mitchell license that was submitted several years ago …
> it attempted to extend copyleft to the output of a program … **I recall that the general
> sentiment on this list was against approval.**"
>
> **Moming Duan**（同日）: "Correct. As Pamela pointed out, the current clause **somewhat
> oversteps**, as not all users will use the output to train a new model."

要件はその後**削除された**（提出者が 2026-09-04 の返信でそう述べており、現行テキストにも無い）。

**何が示されたのか。** 「出力に義務を掛けると mere use への条件になる」は我々が構成した理論では
なく、**このリストで議論され、複数の参加者が同じ結論に達し、条文が実際に削除された軸**である。
しかも Fontana 氏の記憶によれば、**出力へ copyleft を及ぼそうとした先行提出も同じ方向で退けられて
いる**（撤回されたため裁定には至っていない）。§6.4 はこの軸に対して**構造的に安全な側**にいる ——
出力に何も掛けないので、掛かるかどうかを検討する必要が生じない。

**この論拠の限界も書いておく。**

  - **どれも OSI の裁定ではない。** Phipps 氏は "in a personal capacity" と明記しており、
    ModelGo の削除は**提出者の判断**、Kyle Mitchell の件は**撤回**であって決定ではない。
    「リストの一般的な傾向」までしか言えない。
  - **問われたのは *notice* 要件である。** ACD-1.0 はいかなる要件も持たないので同じ轍を踏み
    ようがないが、それは設計の巧みさではなく**何も課さないことの帰結**にすぎない。
  - **この記録は §6.4 を支持するだけである。** §9（機械生成物に権利が存在すると前提しない）や
    §4.4（§3 と独立の許諾）といった、**本 instrument に固有の争点には何も述べていない。**

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

**2026-09-25 訂正**: 旧回答は *"I am not aware of a precedent either"* で始まっていた。同日の全数 census（`ACD-1.0.gap-census.md` / `against.md` #241）で CERN-OHL-P-2.0 の Products への特許許諾が見つかり、**自分たちの記録を知っている相手に対して偽になっていた**ので、部分的な先例を先に名指しする形へ改めた。

> **English:**
>
> There is a partial one, and I should name it. CERN-OHL-P-2.0 grants a patent
> licence over "Products", defined to include any work "arising from the use,
> application or processing of Covered Source", which can be read to reach a
> trained model. It does not name models, parameters or outputs, and conveying
> a Product carries a notice obligation (its Section 4). So what is new in
> Section 8.4 is naming them, and doing so without a condition — not the idea
> that a patent grant can follow what is made from the work. The
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

**Q. §8.4 は §8.1 の「作品に含まれる主題に起因する場合」という但し書きを意図的に外している。つまり作品と無関係なクレームまで及ぶのではないか。**

> **English:**
>
> The observation is correct and the clause says so itself: "The proviso in Section 8.1 as to
> subject matter contained in the Work is deliberately absent from this Section: a model is not
> subject matter contained in the Work, so importing that proviso would restore the exposure this
> Section exists to remove."
>
> **So the reach is genuinely wider, and here is what actually bounds it.** Two limits remain and
> a third does not exist:
>
> - **Ownership.** §8.5 applies §2.7: only claims "the Dedicator owns or controls". A claim held
>   by anyone else is untouched, whatever its subject matter.
> - **Causation.** The claim must be one "that would be infringed by Computational Use of the
>   Work" or by making, using or transferring a model or output "resulting from that use". A
>   patent that has nothing to do with processing this Work, or with anything produced by
>   processing it, is not within the words.
> - **What is gone:** the requirement that the infringement trace to subject matter *contained
>   in the Work*. That is the deliberate widening. A claim reading on a training technique, or on
>   a property of the resulting model, is reachable even though the technique is not in the Work.
>
> **This is the price of the design, and I would rather state it than let it be discovered.** A
> Dedicator with a patent portfolio who applies ACD-1.0 to a dataset may be licensing claims that
> read on downstream model-building, not merely on the dataset. `ACD-1.0.against.md` #16 records
> this as a cost: an organisation that wants to keep its patents cannot use this instrument.
>
> **Why the narrower drafting was rejected.** Keeping the proviso would mean the patent grant
> stops at the Work while §6 permits computational use of it — the exact split §8.3 says must be
> rejected, because a permission that is safe under copyright and exposed under patent is not a
> permission anyone can rely on. Narrowing §8.4 would be coherent drafting for a different
> instrument; for this one it would reintroduce the hole the section exists to close.
>
> **The remaining honest gap.** A reviewer may say the widening is broader than necessary — that
> the section could reach claims infringed by the *use of the Work in training* without also
> reaching claims infringed by *any output*. That is a real drafting question and I do not have a
> conclusive answer to it. It is recorded as a 1.1 candidate in `ACD-1.0.errata.md` rather than
> defended here.

**なぜこの問答を足すか**: 既存の Q は「**なぜ §8.4 が必要か**」を述べていたが、**攻撃面は
そこではない** —— §8.4 が §8.1 の但し書きを**明示的に外している**ことである。条文が自分で
「deliberately absent」と書いているので、審査者は必ずそこを読む。

**必要性の説明は、射程の説明の代わりにならない。** 何が残る制限で（保有・因果）、何が
消えた制限か（作品に含まれる主題への遡及）を分けて述べ、**その広さが誰にとってのコストか**
（特許を持つ採用者）を名指しする。そのうえで**答えを持たない部分**（出力にまで及ぶ必要が
本当にあるか）は 1.1 候補として残し、ここで弁護しない。

**Q. 「Work の使用に起因する」という因果の限定は、具体的な場面で何を答えるのか。判定基準が定義されていない。**

> **English:**
>
> The criticism is right that the text states a test and does not define it, and the honest
> answer is case by case. Six situations, worked. **Where the answer differs between 1.0 and the
> 1.1 draft I say so, because 1.0 does not contain the causation sentence at all.**
>
> - **A model trained on the Work, then run for inference.** Covered. The model is one
>   "resulting from that use", and Section 8.4 licenses claims infringed by the "use" of such a
>   model, not only by its transfer.
> - **Operating a service rather than distributing anything.** Covered, and by the same word.
>   The enumerated acts are "making, having made, **use**, offering for sale, sale, importation,
>   or other transfer". A hosted service uses the model. Nothing turns on distribution.
> - **The use of the Work is not a necessary condition of the infringement.** Not covered under
>   1.1, which reaches "only claims whose infringement **depends upon** the use of the Work".
>   **Under 1.0 this is unresolved**: the only limiter there is "resulting from that use", which
>   reads as factual causation and does not ask whether the infringement depended on it.
> - **An identical model obtainable without the Work at all.** **This is where 1.0 and 1.1 give
>   different answers, and it is the sharpest example of what the 1.1 sentence does.** Under 1.1
>   the claim does not depend on the Work, so it is outside. Under 1.0 the model in fact resulted
>   from the use, so on the words it is inside even though the Work was dispensable.
> - **The Work's use supplies one element of a claim.** Covered on the natural reading:
>   infringement is of the claim as a whole, and if the Work's use supplies an element the
>   infringement depends on it. I am not aware of an argument the other way that the text supports.
> - **An embedding derived from the Work, used as input to a second model.** **Unresolved, and I
>   will not pretend otherwise.** The embedding results from the use; whether the second model
>   does is a question about how far down a chain "resulting from" runs, and neither version
>   answers it. This is the weakest point in the section and it is recorded rather than argued.
>
> **What this shows about the design.** Five of the six turn on words already in the section —
> "use", "resulting from", "depends upon" — and the sixth is a genuine gap. **The section is
> broad by intent and the boundary is doing real work in at least two of these cases**, which is
> the answer to the charge that the reach is unlimited. It is not the answer to the charge that
> the test is undefined, and I do not claim it is.

**なぜこの問答を足すか**: **§8.4 の「広さ」は既に 2 問で扱っているが、境界の作例が 1 つも無かった。**
外部レビュー（2026-09-14・`ACD-1.0.discussion-log.md` ラウンド 0 #3）が 6 つの場面を挙げ、
**「因果と量の区別は述べているが、因果の判定基準自体は定義していない」**と指摘した。
**指摘は正しい。定義できないなら、せめて当てて見せる。**

**作ってみて分かったことが 2 つある。** **(1) 6 件中 5 件は条文の語（"use" / "resulting from" /
"depends upon"）で答えが出る** ——**「射程は無限」という読みへの反論は、抽象論ではなく作例で示せる。**
**(2) 4 件目（Work 無しでも同一のモデルに到達できる場合）で 1.0 と 1.1 の答えが割れる** ——
**1.0 には因果の文が無く、"resulting from that use" は事実的因果として読める**ので、
**Work が不可欠でなくても射程に入る。** E15 で 1.1 に足した 1 文が、**実際に何をしているか**が
この 1 件で目に見える。**提出するのが 1.0 なら、この差は先に述べておくほうがよい。**

**6 件目は答えを持っていない**（連鎖の深さ）。**持っていないと書く。**

**Q. §8.2 は「Dedicator によって終了させられない」と限定するのに、§10.4 は「いかなる理由でも終了しない」と限定していない。どちらが本当なのか。**

> **English:**
>
> Both, and the difference is not accidental — but the text does not explain it, so it is worth
> setting out.
>
> §10.4 is the general statement: "No permission granted by this Dedication terminates for any
> reason. This Dedication contains no termination provision and no revival provision, because it
> contains nothing that You could breach." That is unqualified because it is a statement about
> **the document**: there is no clause anywhere that ends a permission, so nothing in the
> instrument can terminate one.
>
> §8.2 addresses a different worry. Patent grants in widely-used licences commonly *are*
> terminable — Apache-2.0 §3 ends the patent licence on the filing of a patent claim — so a
> reader arriving at §8 expects to find a retaliation provision and needs to be told, in that
> place, that there is none. Saying "not terminable **by the Dedicator** on any ground, including
> the commencement of … patent litigation" names the actor the reader is worried about.
>
> **Why the narrower wording is the honest one.** No licence can promise that a permission
> survives every external event: a court can hold a provision ineffective, a statute can change,
> a jurisdiction may not give effect to part of the instrument. §10.4 says the *document*
> terminates nothing; §8.2 says the *Dedicator* cannot terminate. Neither claims that no
> external force could ever disturb a permission, and §13.2 disclaims exactly that warranty —
> it does not warrant "that any Section of this Dedication is effective in any jurisdiction".
>
> If a reviewer reads §10.4 as promising more than that, the answer is that it does not, and the
> narrower §8.2 is the better guide to what is actually being undertaken.

**なぜこの問答を足すか**: 本文の自己言及的な主張 9 件を機械的に検証した副産物である。
9 件はすべて真だった（「無い」と述べた条項は実際にどこにも無い）が、**同じ事柄を 2 箇所で
述べていて限定語だけが違う**箇所が 1 つ見つかった。

**同じことを 2 度述べる文書では、限定語の差が意味を持つ。** 審査者は必ず狭いほうを読んで
「では広いほうは何なのか」と問う。**説明できるなら書いておく、説明できないなら直す** ——
今回は説明できるので書いた（片方は文書についての言明、片方は行為者についての言明）。

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

#### §11.4 が答えている、いま生きている原理的な反対（2026-08・一次資料）

OpenMDW-1.1 の審査で、著作権侵害の主張を終了の引き金にすることへ、次の反対が出ている
（アーカイブ本文より）:

> "The reason for treating patent and copyright infringement differently is that **copyright
> infringement requires copying**. That means that there was a volitional act … on the part of the
> licensor, and the license gives them **blanket immunity** for that act. … So what you are
> proposing is that **a completely non-culpable party has to give up a claim** against what might
> be a deliberate, intentional, unlawful act… This seems to me to be **antithetical to open source
> principles** — open source developers get exploited enough without being exploited by their own
> community. If the model provider believes their deliberate use of someone else's copyrighted
> work is non-infringing they should be **willing to defend the claim, not absolve themselves of
> liability through contract**."

**主張されている原理は 2 つある**: (a) ライセンスは、**落ち度のない第三者に請求権を放棄させて
はならない**。(b) 提供者は、**契約によって自らの責任を免れてはならない**。

**ACD-1.0 はどちらの形も持たない。** 終了の引き金が無いので (a) の構造が作れず、
そして **§11.4 が (a) を明文で否定している** ——「本 Dedication は Covered Rights、§8 が述べる
特許クレーム、§12 の範囲の Moral Rights に及ぶ。**それ以外には及ばない。**…
**Dedicator 以外の者が保持する権利の下では、いかなる許諾も与えない**」。§11.4 は元来
**個人データや第三者の権利**のために書かれた条項だが、**「他人の請求権に触れない」という同じ
性質**が、この反対の中心にある心配をそのまま外している。

**(b) については、正直に線を引く。** ACD-1.0 も §13 / §14 で warranty と liability を否認して
おり、**それは「契約による免責」の一種である**。氏の批判が向いているのは「**第三者の請求権を
消す**」形であって、「自分は保証しないと述べる」形ではない —— 後者はほぼすべての OSI 承認済み
ライセンスが持つ。**両者を混ぜて「我々は該当しない」と言わないために、ここに書き分けておく。**

**この記録は ACD-1.0 が何かを満たすことの証明ではない。** 誰も ACD-1.0 について述べていない。
ここにあるのは、**いま審査の場で主張されている原理**と、**その原理に対して本文のどの条項が
働くか**の対応づけだけである。

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

## 第 2 層 —— 定型条項と解釈条項への攻撃（別冊）

**Q22〜Q33 は [`ACD-1.0.review-responses-boilerplate.md`](ACD-1.0.review-responses-boilerplate.md) にある。**
「条文を読んだ上で、その書き方は効かないと言ってくる」種類の指摘——構成の指針（§15.1）、
contra proferentem の排除（§15.3）、不行使の扱い（§15.5）、倒産（§2.9）、反 DRM（§5.2(a)）、
追加条件（§5.2(b)）、データベース権（§7）、全大文字（§13・§14）、法域固有の論点、
1.0 承認後の 1.1 の扱い、機械を "You" に含める理由——を扱う。**番号は動かしていない。**
