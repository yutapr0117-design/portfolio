---
file: LICENSES/ACD-1.0.comparison.md
audience: ai, human (提出者), 監査人, 採用検討者, 第三者全般
last-updated: 2026-09-05
canonical-ref: LICENSES/ACD-1.0.txt (凍結中の本文・唯一の権威) / docs/architecture/acd-license-rationale.md (§2 に無条件系との比較と 0BSD/Apache 逐条差分) / LICENSES/ACD-1.0.review-responses.md (総論の想定問答・索引)
---

# ACD-1.0 — ライセンス族ごとの比較（「なぜ既存のあれではないのか」への答え）

```
本書の役割 : 「X で足りるのでは」への答えを**族ごと**に置く
既にある比較 : docs/architecture/acd-license-rationale.md §2
             —— 無条件系 (CC0 / Unlicense / MIT-0 / 0BSD / WTFPL / PDDL) と
                Apache-2.0・MIT/BSD・CC-BY との 6 列比較、および
                0BSD / Apache-2.0 との**逐条差分**
本書が足すもの : そこで扱っていない 4 族 —— **copyleft 系 / AI 用途制限系 /
                source-available 系 / データ系** と、族をまたぐ判断基準
本書の性質 : 非規範。齟齬があれば本文が勝つ
```

## 0. なぜ族ごとに分けるのか

「なぜ新しいライセンスが要るのか」への答えは、相手が**どの族を念頭に置いているか**で変わる。

- 無条件系を念頭に置く人 → 「条件ゼロなら 0BSD で足りるのでは」
- copyleft を念頭に置く人 → 「なぜ共有を要求しないのか」（**価値観の問い**）
- AI 用途制限系を念頭に置く人 → 「AI に触れるライセンスは制限のためのものでは」（**誤読**）
- source-available を念頭に置く人 → 「これも open source ではない類か」（**分類の誤り**）
- データ系を念頭に置く人 → 「データなら ODbL / CDLA では」

**同じ答えを繰り返すと噛み合わない。** 族ごとに答えを用意する。

---

## 1. 無条件系 —— **最も近い承認済みライセンスとの比較（この文書の主題）**

OSI が新規ライセンスの提出者に求めるのは、**最も近い承認済みライセンスとの比較**である。
以下がその節にあたる。他の族（copyleft / AI 用途制限 / source-available / データ）は、
承認済みではないか、そもそも「条件を課さない」という性質を共有しないので、比較としては
副次的である。**この節が最も厚くあるべきで、以前はここが最も薄かった。**

> **English:**
>
> **The nearest OSI-approved licences.** MIT-0 and 0BSD are the closest by effect: both are
> permissive grants with the notice condition removed, so like ACD-1.0 they ask nothing of a
> recipient. The Unlicense is the closest by *form*: it is a public domain dedication with a
> fallback grant, approved in 2020 on a legacy request. CC0 is the closest by *intent* but is
> not approved — Creative Commons withdrew it from review in 2012 over its express exclusion
> of patent rights.
>
> | | Conditions on You | Express patent grant | ML / TDM addressed | Reservation signals | Rights may not subsist | Moral rights | Binds successors |
> |---|---|---|---|---|---|---|---|
> | **MIT-0** | none | no | no | no | no | no | no |
> | **0BSD** | none | no | no | no | no | no | no |
> | **Unlicense** | none | no (silent) | no | no | dedication form only | no | no |
> | **CC0** (not approved) | none | **expressly excluded** | no | no | dedication form only | waived where possible | no |
> | **Apache-2.0** | notice, NOTICE file | yes, limited to claims necessarily infringed | no | no | no | no | no |
> | **ACD-1.0** | none | yes, reaching computational use, models and outputs (§8.4) | yes, affirmatively (§6) | expressly declines to make one (§6.2) | §9 makes permissions independent of subsistence | §12.1 waiver, §12.2 covenant where waiver is impossible | §2.8, §12.4 |
>
> **What ACD-1.0 adds, stated as narrowly as it can be.** Four things, and only four: a patent
> grant that follows the work into training and inference; an affirmative statement about
> machine learning and text-and-data-mining, including a refusal to make a reservation; a
> construction that does not assume any right subsists in the first place; and provisions that
> follow the rights when they change hands. Everything else it shares with MIT-0 and 0BSD.
>
> **When the approved alternatives are the better choice — which is most of the time.** If the
> work is ordinary software, if the author holds no patents, if no text-and-data-mining opt-out
> regime is in play, and if authorship is not in doubt, then **MIT-0 or 0BSD is the better
> licence**, and this submission says so plainly. They are shorter, they are approved, licence
> scanners recognise them, and a reader's legal team has seen them before. ACD-1.0 earns its
> existence only in the narrow band where those four assumptions fail together — which is where
> this repository sits, and which is not where most projects sit.
>
> **The cost of another entry in this category, in the terms the list itself uses.** On
> 2026-08-07 a solo author brought another public-domain-equivalent instrument to
> `license-discuss`. Rob Landley's reply put the category argument in a frame this document had
> not used: public-domain-equivalent licences are, on his understanding, **the only fungible
> category** — they do not require the licence text to be carried into derived works, so code
> from differently-licensed sources combines without listing each and without "the stuttering
> problem" — and 0BSD is in that category, in wide use, and authored under by Google, Microsoft
> and Facebook. His question to the newcomer was *"could you explain why you're doing another
> one?"* (individual capacity, not an OSI position).
>
> **ACD-1.0 is fungible in exactly that sense, and this is checkable rather than argued.** §10.2
> states a recipient need not give attribution or reproduce any notice; §4.3 and §10.1 attach no
> condition of any kind. So the two costs a new licence usually imposes — compatibility analysis
> and notice bookkeeping — are near zero here, in both directions: code under ACD-1.0 combines
> into a 0BSD project and the reverse, with nothing to track. **That is the honest answer to
> "why another one": not that it is better in the category, but that the category's cost of
> admitting an entry is unusually low**, and the three subjects above are absent from the
> incumbent.
>
> **It cuts against us as well, and the same sentence carries both edges.** If combining is free
> and nothing must be carried, then an author who wants ACD-1.0's four properties for *their own*
> work is well served, but a *downstream* project gains little from the licence's presence in the
> world that it could not obtain by asking that author directly. Fungibility lowers the cost of
> another entry; it does not by itself create a benefit. And low lock-in works the same way for
> the adopter: **anyone who later regrets choosing ACD-1.0 can relicense outward freely**, which
> makes adopting it cheap to reverse — a reason to be less worried about the choice, and equally
> a reason the choice matters less than a steward would like it to.
>
> **The proliferation question is therefore not "is ACD-1.0 different?"** — it demonstrably is,
> in the four respects above. It is "**is that difference worth another licence in the world?**"
> That is a judgement for the list, and the honest position is that the answer is not obviously
> yes. What can be said is that the gap is real, that no approved licence closes it, and that
> combining approved licences does not close it either (§5.5 addresses the CC0-plus-patent-pledge
> construction directly).

---

## 1.3 「既存の大型ライセンスが AI 対応すれば済むのでは」

**proliferation の反論として最も強い形**である。新しい instrument が要るかを問う代わりに、
**待てば済むのではないか**を問う。事実を確かめてから答える。

> **English:**
>
> **What the stewards of the incumbent licences are actually doing (checked 2026-09).**
>
> | Steward | What they have done about AI | What they have not done |
> |---|---|---|
> | FSF | Announced work on **criteria for free machine learning applications**, taking the position that an ML application is not free unless its training data and processing scripts also respect the four freedoms; published analysis of code-generation tooling | **No announced GPLv4**, and no timeline. The GPL family's forward mechanism is the "or later" clause, which routes future terms through a version that does not yet exist |
> | ASF | Published **generative-tooling guidance** for its projects, describing it as rapidly evolving; funded a Responsible AI initiative | **No announced amendment to the Apache License** for training or TDM |
> | Creative Commons | Explored signalling approaches for AI preferences | CC0 remains as it was in 2012; the withdrawal was never reversed (§1.4) |
>
> **The pattern is consistent, and it is the answer to this objection.** The incumbent stewards
> are addressing AI through **criteria, guidance and policy** rather than through licence text.
> That is a defensible choice — arguably the better one for a steward with a large installed
> base, since amending a licence in wide use imposes migration costs on everyone using it.
>
> **But it means the licence text stays silent, and silence is not neutral in a regime where an
> opt-out is exercised by signalling.** A work under Apache-2.0 today says nothing about
> text-and-data mining, nothing about whether a reservation has been made, and nothing about
> whether the grant reaches a trained model. Those questions are answered by policy documents
> that do not travel with the work, or not answered at all.
>
> **The honest shape of the argument, stated with the concession first.** If GPLv4 or a revised
> Apache License were announced tomorrow with TDM and model-output terms, the case for ACD-1.0
> would be materially weaker — not eliminated, since neither would address material whose
> authorship may not subsist (§9), but weaker. **Nothing in this submission depends on the
> incumbents staying silent for ever.** What it depends on is that a work released today needs an
> answer today, and that "wait for the next version of a licence whose next version has not been
> announced" is not an answer a publisher can act on.
>
> **What would falsify this section.** A concrete announcement from any of the three stewards of
> licence-text changes addressing training, TDM reservation, or model outputs. If that happens,
> this section should be rewritten rather than defended, and `PEER-REVIEW-WATCH.md` records the
> obligation to check.

## 1.35 取り込んだ後も残る差は何か（差別化とその代償）

§1.3 は「待てば済むのでは」に答えた。**ここは別の問いに答える** —— **既存ライセンスが
AI 条項を実際に取り込んだとして、そのとき何が残るのか。** 「根本が異なる」と述べるだけでは
主張であって説明ではないので、**条項を追加すれば埋まる差**と**追加では埋まらない差**を分ける。

> **English:**
>
> ### Differences an amendment closes
>
> These are the ones that would disappear if Apache-2.0 or the GPL added AI terms tomorrow, and
> it is worth saying so plainly rather than claiming a permanence they do not have.
>
> | Difference | Why an amendment closes it |
> |---|---|
> | Express permission for training and TDM | A clause can say this. Nothing structural prevents it |
> | A statement that no TDM reservation is made | Same |
> | Patent grant extending to models and outputs | Apache-2.0 already has the machinery; extending its scope is a drafting change |
> | Database rights addressed | A clause can enumerate them |
>
> **Four of ACD-1.0's seven distinguishing features are of this kind.** If the incumbents move,
> the case for this instrument narrows to the remaining three — and the honest position is that
> those three carry the argument, not the seven.
>
> *(Corrected 2026-09-06. This section said "six" and "the remaining two" while enumerating
> four below one heading and three below the other. Both numbers were written in the same
> commit as the list they miscount, so this was wrong when written rather than gone stale —
> the third instance of that failure found in this dossier on one day. The arithmetic is now
> derived from the two lists on every CI run.)*
>
> ### Differences an amendment does not close
>
> These follow from **where a licence starts**, not from what it contains.
>
> **1. A licence that presumes a right cannot be amended into one that does not.**
> Apache-2.0, MIT and the GPL all begin from a grant by a copyright holder. That is their
> operative premise: rights exist, and the holder permits certain uses of them. ACD-1.0 begins
> one step earlier — §9.2 makes no representation that any right subsists, and states that where
> none does, the instrument "adds nothing to Your existing freedom and takes nothing away";
> §9.3 removes from the user any duty to determine which parts are machine-generated, and makes
> no permission depend on "how any jurisdiction answers it, or on whether the answer changes."
>
> An AI clause bolted onto a conventional licence still inherits the premise. Applied to material
> whose authorship may not subsist, it grants permissions under rights that may not be there —
> which is precisely the "false IP norms" criticism levelled at AI-specific licences on
> license-discuss in March 2026. **Restructuring around that premise is not an amendment; it is a
> different instrument.**
>
> **2. "Conditions plus an exception" is not the same thing as no conditions.**
> The incumbents are condition-bearing by design — attribution, notice retention, source
> disclosure, reciprocity. An AI amendment would most naturally take the form of *permission to
> train, subject to the existing conditions*. That is a coherent and probably good design. It is
> not this one: §4.3 attaches no condition of any kind and §10.1 says so for the whole
> instrument, so **there is no condition for a machine to satisfy, and therefore nothing for a
> compliance step to check.**
>
> **3. Computational use is defined once, at the top, rather than added at the edge.**
> §1.7 defines Computational Use to include reproduction, extraction, normalisation, indexing,
> retrieval, analysis and TDM, *and* training, fine-tuning, evaluation, alignment and
> distillation, *and* the making, distribution and use of any resulting model, weights,
> embeddings or outputs. Because it is a defined term, §6.1 permits all of it in one sentence and
> §8.4 follows it into patents. An amendment adds a clause; a definition changes what every other
> clause is about.
>
> ### What this costs
>
> Structural difference is not free, and the costs are the mirror image of the advantages.
>
> - **No conditions means no attribution and no notice retention** — which some publishers want,
>   and which makes the warranty disclaimer weaker in practice (`against.md` #41).
> - **No patent retaliation** (§8.2, expressly) — OpenMDW and MG-BY both terminate on suit, and
>   many reviewers regard defensive termination as a feature.
> - **A patent grant this broad is expensive for a patent holder** — an organisation that wants
>   to keep its patents cannot use this instrument (`against.md` #16).
> - **Unfamiliarity.** Apache-2.0 with an AI clause is a document every legal team has already
>   read. This is not, and that is a real adoption cost, not a rhetorical one.
> - **No steward, no adoption, no legal review** (`against.md` #1, #4, #10).
>
> **The narrow claim.** If the incumbents amend, ACD-1.0's distinctiveness reduces to two things:
> **it does not presume that a right exists, and it imposes no condition on anyone.** Whether
> those two are worth a separate instrument is the proliferation question, and this document
> does not claim the answer is obvious.

## 1.38 「なぜ新しいライセンスが要るのか」に、審査者が実際に使っている経験則（2026-07・一次資料）

`license-review` で 2026-07 に審査された新規提出に対し、Carlo Piana 氏がこう書いている
（**要約ではなくアーカイブ本文**）:

> "I am not even sure what shortcoming this license intends to cure compared to the hundreds of
> already existing non copyleft MIT-style licenses. … the idea to create a new type of condition …
> **creates additional friction in the compliance process** — which is already a nightmare for a
> medium-sized embedded software project. Therefore I urge license submitter to introduce one only
> where there is a strong rationale. **As a rule of the thumb, if in more than 25 years nobody
> thought of it, most likely it is not a perceived problem, unless something new has come around
> (see the SaaS model, or extensive AI model usage, etc.).**"

**この経験則は 2 つの部分からできており、ACD-1.0 に対して逆向きに働く。**

**(1) 「25 年誰も思いつかなかったなら、たぶん問題ではない —— *何か新しいことが起きていない限り*」。**
氏が挙げた例の 1 つが **"extensive AI model usage"** である。ACD-1.0 の §1 の gap 主張は、
まさに「機械学習と機械による著作が新しい事情である」というものなので、**審査者が明示した
テストの、名指しされた例に当たる**。

**ただしこれは*カテゴリ*についての支持であって、*この instrument* についてではない。**
「AI が新しい事情である」と「ACD-1.0 がその事情に必要な instrument である」は別の命題で、
後者は §1.35 が扱っている（**7 つのうち 4 つは既存が改訂すれば閉じる**）。**1 参加者の
rule of thumb であって規則でもない。**

**(2) 「新しい *条件* を作ると compliance の摩擦が増える」。** こちらは**この instrument には
当たらない** —— ACD-1.0 は条件を 1 つも課さない（§10.1 / §4.3）。氏が懸念しているのは
「条項を増やすと確認作業が増える」ことで、**確認すべきことがゼロの instrument は、
その懸念の対象外**である。

**逆に、この経験則が我々に突きつけるものもある。** 氏の最初の問いは
「**hundreds of already existing MIT-style licenses に比べて、何の欠点を治すのか**」だった。
それは `against.md` #28 / #33（proliferation）と同じ問いで、**この節の存在理由そのもの**である。
`comparison.md` §1 全体がその答えであり、**§1.35 はその答えのうち「改訂で消える部分」を
自分から先に切り出している。**

## 1.4 CC0 —— 同型で唯一 OSI で止まった先例（2012）

**ACD-1.0 に最も近い先例は CC0 であり、その顛末はこの提出にとって最も重要な事実である。**
同じ dedication 型で、同じく「権利を留保しない」ことを目指し、**OSI の審査で止まった**。
2012-02 のアーカイブを一次資料として読み、争点を正確に把握した。

> **English:**
>
> **What actually stopped it.** Creative Commons withdrew CC0 from OSI review in February 2012.
> The unresolved objection was not the dedication form — it was the patent language. Two
> distinct criticisms were made of the clause placing patents out of scope: that it **weakens
> equitable estoppel defences against patents**, and that it **heightens risk by putting a user
> "on notice" of patent exposure** in the associated code. CC explained that removing the text
> would require a new version, which they lacked the bandwidth to produce while CC 4.0 was in
> progress; the withdrawal was therefore procedural in form and substantive in cause.
>
> **Both criticisms are addressed in ACD-1.0's structure, and not by accident.**
>
> | The 2012 objection to CC0 | ACD-1.0 |
> |---|---|
> | The patent carve-out **weakens estoppel defences** | §2.5 builds estoppel deliberately: the Dedicator declares that reliance "is the purpose of this Dedication and not merely a foreseeable consequence of it", will not assert the instrument is "revocable, unsupported, or otherwise ineffective for want of consideration or formality", and "is estopped from doing so to the extent the law of any jurisdiction gives that principle effect." Where CC0's language was said to erode the defence, §2.5 is drafted to supply it |
> | The carve-out **puts users on notice** of patent risk, raising exposure | There is no carve-out to give notice of. §8.1 grants a patent licence; §8.4 extends it to computational use, models and outputs; §8.3 states in terms that nothing "reserves, preserves, or leaves unaffected any patent right of the Dedicator", because "a dedication that gives away copyright while withholding patent" leaves the recipient exposed |
> | Fixing it would require a new version CC could not then produce | Not applicable — ACD-1.0 was drafted with §8 in place from the first published version |
>
> **A third objection, found on re-reading the archive in 2026-09, is the one this instrument was
> built against.** Bruce Perens, 2012-02-18:
>
> > "CC0 is an abandonment of rights, and then a backup license that would be considered
> > acquiescence, **but which is only in consideration *if your rights were not abandoned*.**
> > So, I am reading this as **either an abandonment of rights OR acquiescence, but not both**."
>
> That is an objection to the **fallback** shape: a licence whose operation is conditioned on the
> dedication having failed. **ACD-1.0 §4.4 is written so that the objection does not reach it** ——
> the licence "is granted independently of Section 3 and does not depend on Section 3 being
> ineffective", and where §3 is effective §4 is "redundant but not void" and remains available.
> A recipient never has to decide which of the two operated, which is precisely the decision
> Perens was pointing at.
>
> **This also explains why `against.md` #24 mattered more than a wording slip.** That entry
> corrected our own documents for describing §3 as having a "fallback licence" —— i.e. for
> describing ACD-1.0 as having **exactly the structure objected to here**. The error did not
> merely misdescribe a clause; it handed a reviewer the 2012 objection, against an instrument
> drafted to avoid it.
>
> **The withdrawal itself, verbatim (found 2026-09-06).** Christopher Allan Webber, Creative
> Commons, license-review, 2012-02-24:
>
> > "We've discussed this internally, and unfortunately we agree that it's best to **withdraw CC0
> > from the OSI review process at this time.** There have been several issues raised around the
> > language declaring patents out of scope in the tool (**that they weaken equitable estoppel
> > defenses against patents or that they heighten risk by putting someone "on notice" about
> > patent risks in the associated code**)."
>
> **That confirms this section's account of the cause, in the withdrawing party's own words** ——
> the two criticisms named above are the two named there, and no other ground is given.
>
> **It also adds a fact this section did not have: why the carve-out existed at all.**
>
> > "The patent language that exists comes out of conversations with the **scientific data
> > community**, whom were a large target of adoption for the tool. This community felt strongly
> > that there was a need to clearly waive something into the public domain **without also waiving
> > patents in the process**."
>
> So the carve-out was **a deliberate accommodation of a named constituency**, not an oversight.
> That matters for how ACD-1.0's opposite choice should be read: §8.3 states that a dedication
> giving away copyright while withholding patents "leaves the recipient exposed, because software
> cannot be practised without practising whatever patent claims it embodies". **That is a
> considered disagreement with a position someone held for a reason** —— and the reason was that
> the tool's target adopters were publishing data, not software. ACD-1.0 is written for works
> meant to be learned from, which includes both, and it resolves the tension the other way.
> **A reviewer is entitled to think the scientific-data community was right**; what this section
> claims is only that the choice was made knowingly.

> **What this does not mean.** It does not mean ACD-1.0 clears the bar CC0 did not. CC0's
> patent problem was one objection among several, the dedication-form question remains live
> (§1b), and CC0 had adoption and an institutional steward that this instrument does not. What
> it means is narrower and worth stating precisely: **the specific defect that ended the closest
> comparable review is one this text was built to avoid**, and the avoidance is visible in the
> clauses rather than asserted in the covering message.
>
> **The uncomfortable half.** CC0's patent silence was requested by the scientific data
> community, who wanted to place material in the public domain **without** waiving patents. That
> is a real constituency with a real preference, and ACD-1.0 does the opposite: §8 grants, and
> §8.3 refuses the reservation outright. An adopter who holds patents and wants to keep them
> cannot use ACD-1.0, and that cost is recorded as `against.md` #16.

## 1.45 最も近い同時代の比較対象 —— AI-MIT / AIAL-1.0（2026-03・提出の翌日に撤回）

**2026-09-06 に一次資料で読んだ。** `license-review` と `license-discuss` の 2026-03 に計 36 通ある。
提出者は **AI 生成コードのための permissive ライセンス**として出し、動機は ACD-1.0 §9 とほぼ同じ
——「既存ライセンスは人間の著者を前提に書かれており、AI 生成コードについて**存在しないかもしれない
著作権と人間の著作者性を含意してしまう**」。**提出は 2026-03-12、撤回は 03-19。**

**なぜ止まったかを、条ごとに我々へ当てる。** 以下は「我々の方が優れている」という主張ではなく、
**3 つの反論がこの本文では発火しない**という条文上の対応である。

| AI-MIT / AIAL への反論（発言者・原文） | ACD-1.0 の該当 | なぜ発火しないか |
|---|---|---|
| **佐渡秀治氏**（Open Source Group Japan 会長）: 透明性条項が再頒布だけでなく *"use as input for further AI training"* でも発火する → **OSD #10**。帰属要求は **OSD #3・#7**。そして —— *"it is not clear how **conditions derived from copyright can be imposed in a stable way on code for which copyright may not exist at all**"* | **§10.1** | **条件を一切課さない。** 課す条件が無いので、「存在しないかもしれない権利に由来する条件」という不安定さが生じる余地が無い |
| **Joshua Gay 氏**: *"overreading Thaler v. Perlmutter"* —— 「完全に AI 生成」と表示された file を**そのままパブリックドメインと扱える**という前提は、現行法が支えるより強い | **§9.2** | **権利の存否について一切表明しない。**「存在しないなら本 Dedication は何も足さず何も奪わない／**存在する、あるいは後に存在すると判断されるなら** §3〜§8 と §12 が全面適用」と両方向に書いてある |
| **Josh Berkus 氏**（OSI）: 実プロジェクトは AI 生成・AI 補助・人間著述・他 OSS 由来の file が混在し、履歴を通じて改変される。ファイル単位の帰属モデルは *"targets only brand-new projects created from scratch and never modified again"* | **§9.3** | **どの部分が機械生成かを判定する必要が無い。** *"No permission granted here depends on that question, or on how any jurisdiction answers it, or on whether the answer changes."* |

**この読みが establish しないこと。** AI-MIT が止まったことは ACD-1.0 が通ることを意味しない。
同じスレッドで佐渡氏は *"this proposal should receive **legal review before** the community debates
whether it should be approved"* とも述べており、**これは我々にこそ当たる**（#1・#2）。Berkus 氏の
「名称が MIT の商標に触れる」も我々には無関係だが、それは我々の設計の功績ではなく命名の偶然である。

**ただし方向の違いは実体である。** 2024 年以降に来た AI 時代の instrument は、観測できた範囲では
**いずれも条件を足す方向**（透明性義務・帰属・利用制限・出力への notice）で、そこが争点になっている。
**ACD-1.0 は逆方向に振り切った唯一の提出である** —— 条件をすべて取り去り、権利の存否を判定しなくても
成立するように書いてある。**同じ問いに対する反対向きの賭けであって、同じ賭けの次の 1 件ではない。**

**その鏡像も同じ場所に書く。** 「逆方向に振り切った唯一の提出」は、裏返すと **その方向を誰も
検証していない**ということでもある。**採用が 1 件しかない以上、実地で確かめられてもいない**（#4）。

**⚠ ここには最初、誤った鏡像を書いた（2026-09-06 に同日中に是正）。** 初版は「条件を取り去るだけで
足りるなら 0BSD と MIT-0 が既にある。よって差別化は §6・§8.4・§9 の 3 主題だけにかかる」と述べたが、
**結論も含意も誤りである。** 正しい分析は**この同じ文書の §1.35** に既にあった。

- **§6 と §8.4 は「改訂で埋まる側」**である。§1.35 は 7 つの差のうち 4 つ（ML/TDM の許諾・不留保の
  言明・モデルと出力に届く特許・データベース権）を **既存が条項を足せば消える差**として明示している。
  差別化の根拠をそこに置くのは、**最も脆い足場を選ぶこと**になる。
- **0BSD と MIT-0 は近い代替物ではない。** §1.35 の結論は「既存が改訂した場合、ACD-1.0 の差は
  **権利の存在を前提としないこと**と**誰にも条件を課さないこと**の 2 つに縮む」であり、
  **前者が 0BSD / MIT-0 との根本的な違い**である。両者は条件を外した *著作権者による許諾* であって、
  **権利が存在することを前提としている**。ACD-1.0 は §9.2 で「いかなる権利も subsist するとは
  表明しない」と述べ、一段手前から始まる。§1.35 の言葉では「**その前提を組み替えることは改訂ではなく、
  別の instrument である**」。**機械生成物という、まさに前提が崩れる場面での差**であり、
  AI-MIT を止めた佐渡氏の指摘（存在しないかもしれない権利に由来する条件）が刺さらないのもここに拠る。
- **条件の不在についてだけは、初版の狭い指摘が成り立つ** —— **0BSD / MIT-0 との比較に限れば**
  条件の不在は共有された性質であって差別化ではない。ただしそれは、§1.35 が挙げるもう一方の差
  （前提の不在）が効いていることを何ら弱めない。

**この誤りの形は記録に値する。** 直前の commit で「不利と有利は鏡写しで同時に存在する」と原理を
書き、**その同じ commit の中で、不利方向へ過剰修正した鏡像を作った**。#87 初版と同じ形である。
そして**正しい分析は編集中のファイルの 100 行上にあった** —— 失敗したのは分析ではなく、
**自分が書き込もうとしている文書を読まなかったこと**である。

### 「OSD の枠組みがこの種の instrument を受け付けないのでは」——測ると逆だった

上の読みには反対解釈がありうる ——「止まっているのは条件のせいではなく、**OSD の枠組み自体が
この種の instrument を受け付けないから**」。これが正しければ、条件を取り去った ACD-1.0 も同じ壁に
当たる。**だが、それなら往復が生じないはずである。** 枠組みが拒む形は実際に観測できていて、
それは**審査以前にモデレータが差し戻す**姿をしている（2026-08-07 の UPD 1.5.2 提出者が
`license-review` で受けた扱いがそれで、`license-discuss` へ回された）。

**トラッカーの 252 件で往復の深さを測ると、AI 時代の 6 件は拒まれるどころか最も手厚く議論されている。**

| | timeline（記録された往復） | 参加者 |
|---|---|---|
| **AI 時代の 6 件** | 中央値 **22** | 中央値 **10** |
| 残り 246 件 | 中央値 7 | 中央値 4 |

内訳は ModelGo v2 が **119 往復 / 14 名**、OpenMDW 1.1 が **103 / 19**、AI-MIT が
**撤回までの 1 週間で 35 / 14**（OSI 理事・各国 OSG 会長を含む）。**典型的な提出の約 3 倍の往復と
2.5 倍の参加者**である。

**したがって「枠組みが受け付けない」という読みは、記録が支持しない。** 受け付けない形は短い
スレッドと少ない参加者、あるいは審査以前の差し戻しとして現れる。実際に起きているのはその逆で、
**この主題は `license-review` でいま最も濃く議論されている領域**である。

**片側にしない。** 濃い議論は同時に**濃い精査**であり、争点が多いことは通りやすさを意味しない
（AI-MIT は 35 往復のあと撤回された）。言えるのは「**争われている**」であって「**拒まれている**」
ではない、という区別だけである。

## 1.46 我々の類型が実際に審査された唯一の近例 —— PBZC v2.0（2024-12 提出 → 2025-01 撤回）

**Public Benefit Zero Copyright License v2.0**（Wayne Thornton 氏）は、**公有化の献呈**として
`license-review` に出され、17 通・約 5 週間の審査を経て**撤回**された。**我々の類型が実際に
審査された、直近で唯一の例である**（2026-09-07 にアーカイブで読了）。

**なぜ #87 の一覧に無かったか**: #87 はトラッカーの**名称検索**で類型を数えた。PBZC は名称に
public domain / dedication / waiver / CC0 / Unlicense / 0BSD のいずれも含まない。#87 は
「name matching is a floor, not a census」と**自分で書いておきながら、2 度目の走査をしなかった**
（`against.md` #99）。

### 何が問題にされ、それが ACD-1.0 に当たるか

| 指摘（発言者・日付は原文どおり） | ACD-1.0 |
|---|---|
| **Carlo Piana（2024-12-18）**: 献呈と**コピーレフト**が同居しており *"one cannot really calculate the effect of the license in different jurisdictions"* | **当たらない。** ACD-1.0 にコピーレフトは無く、§10.1 が条件を一切課さない |
| **Piana（同日 18:29・上の続き）**: *"I have nothing against using a **PD dedication and a license by way of backstop** where PD does not really exist in the fullest… **I actually advise to use both**"* | **これは指摘ではなく支持である。** §3（献呈）と §4（許諾）の対は、この審査者が**自ら勧める**構造そのもの。「dedication *taken alone* は承認されない」という 2020 年の勧告に対する我々の答え（§4.4）と同じ向き |
| **McCoy Smith（2024-12-18）**: 対を持つこと自体は *"not necessarily fatal"*。ただし CC0 は「PD が可能な法域では完全な献呈、それ以外では制限のない極めて寛容な許諾」と**明確に**書いており、PBZC はそうなっていない | **§4.4 がまさにその明確さを書いている** —— §4 は §3 とは独立に付与され、**§3 が無効であることに依存しない**。受領者はどちらが作用したかを判断しなくてよい |
| **McCoy（同）**: PD 法域では公有・それ以外ではコピーレフト、という構造は *"likely violates OSD 5 as it discriminates against people in non-public domain dedication jurisdictions"* | **当たらない、が答えを書いておく必要がある**（`against.md` #100）。**PBZC は実体的な結果が法域で変わる**（公有 vs コピーレフト）。ACD-1.0 で法域により変わるのは §12 の**機構**（放棄が可能な法域では放棄・不能な法域では本著作物に限定した不行使の合意）だけで、**受領者が得るものは §4 により同一**である。§10.4 により何も終了せず、§4.4 により §3 の有効性を判断する必要も無い |
| **McCoy（12:52）**: *"public domain is a concept that exists as part of international copyright law… **You can't just rewrite in a way you like**"* | **当たらない。** ACD-1.0 は公有の定義を書き換えない。§3 は放棄の意思表示であり、§9.2 は機械生成物に著作権が生じるか否かについて**何も表明しない**（表明しないことが要点） |
| **Lukas Atkinson（2024-12-18）**: Unlicense を模した条文への批判。*"The Unlicense is not a particularly well-drafted license or PD dedication, and should not serve as a model… **That it was eventually OSI-approved has more to do with its widespread use in some circles**"* | **当たらない（我々は Unlicense の条文を模していない）。しかも #87 の独立した裏付けである** —— Unlicense の承認が普及によるものだ、というのは我々自身が不利な事実として書いていることで、それが**リストの常連から 2024 年に独立に述べられている** |
| **Atkinson（同）**: *"I would be very happy if new licenses/dedications/devices in the 'PD dedication' or 'PD equivalent' category **make use of this wealth of prior discussions (well over a decade)** and avoid running into the same problems"* | **これは我々への要求そのものであり、既に満たしている。** 2012-01〜04 と 2020-03〜06 の議論を原典で読み、`submission.md` §1b と本書 §1.4 に反映してある（`PEER-REVIEW-WATCH.md` §3.9） |
| **Piana**: *"it seems to deliver a grant only for copyright and not under every right that encumbers the free use of the software"* | **当たらない。** §2.2 の Covered Rights は著作権と隣接権を含み、§7 が sui generis データベース権、§8 が特許、§12 が人格権を個別に扱う |

### この 1 件から取れる最も重要な事実

**Pamela Chestek 氏（OSI Licensing Committee 委員長・肩書を明示した発言）、2024-12-18**:

> To be clear, **we do not require review by a lawyer, only recommend it. That is not a blocker.**

これは Piana 氏の「OSI requires prior review by a lawyer」への訂正で、**Piana 氏自身が同日
"I stand corrected re: Pam's message on requiring legal review, bad choice of words on my side."
と撤回している**。

**我々の最大の不利な事実（#5 / #79・法的レビュー不在）に対する、最も強い反証材料である。**
**ただし過大に読まない** —— *recommend* は残るし、Piana 氏の当初の反応が示すとおり、
審査者はそれを重く扱いうる。**「要件ではない」は「軽い」ではない。**


## 1.47 撤回不能性が単独で審査された唯一の例 —— MIT-I（2025-07 提出・18 通）

**Irrevocable MIT License (MIT-I)** は「MIT を撤回不能にする」という**一点だけ**を扱う提出で、
18 通の議論を受けた。**ACD-1.0 の中核性質（§4.1 の irrevocable・perpetual / §8.1 / §10.4「何も
終了しない」）が、単独の論点として審査された唯一の記録である**（2026-09-07 にアーカイブで読了）。

### ACD-1.0 に有利に働く 2 つの発言

**McCoy Smith（2025-08-14）**:
> **Making a license irrevocable is fine, and many OSI licenses do that** (for example, Apache 2.0)

**Pamela Chestek（2025-08-15）**:
> I hadn't noticed before that the grant in the MIT license isn't perpetual or irrevocable. …
> **all that really would need to be done is insert the words "perpetual" and "irrevocable" in the
> grant language.**
> I believe the standard MIT license is terminable, since it doesn't say it's irrevocable.

**ACD-1.0 §4.1 は逐語でそうなっている** —— *"worldwide, royalty-free, non-exclusive, **irrevocable,
perpetual**, sublicensable, and transferable licence"*。§8.1 の特許許諾も同じ語を持ち、§10.4 が
「いかなる理由でも終了しない・復活条項も無い」と述べる。**委員長が「最小限これをすればよい」と
述べたことを、本文が既に満たしている。**

### 同じスレッドから来る、我々への警告

**McCoy Smith（同日）**:
> The statement that the "copyright holder(s) may not ... **modify** ... this version of the
> Software" **violates OSD 3**. … If what is intended is that **the terms of the license** may not
> be modified, t[hen say so]

**§16.4 は「本文を改変した形を `ACD-1.0` の識別子の下で頒布すること」を禁じている。**
対象は**著作物ではなく文書**であり、§10.5 と §16.6 がそれを明示するが、**この審査者は
「modify してはならない」という語形に反応して OSD 3 を持ち出している**。
`against.md` #101 として記録した —— **指摘は 1 行で出せて、答えは §10.5 → §16.6 → §16.4 の
読み順を辿る必要がある**。#100 と同じ非対称である。

### 結果

提出者は議論の後に取り下げていない（2025-08-28 時点でスレッドは自然に終息）。**承認されていない。**
だが**この提出が失敗した理由は撤回不能性ではない** —— McCoy 氏と Chestek 氏の指摘は
「新しい段落のほとんどが surplusage・循環・悪手」であり、**撤回不能性そのものは "fine" と
明言されている**。ACD-1.0 は撤回不能性を**独立した売りとして提出しない**（§4.1 の一語である）
ので、この論点で争う理由が無い。


## 1.5 AI-native な同時代 instrument（OSI 審査中・2026-09 時点）

**ACD-1.0 は、OSI の前にある唯一の AI-native instrument ではない。** 2026-09 時点で
**OpenMDW-1.1**（Linux Foundation 起草）と **ModelGo v2**（MG0-2.0 / MG-BY-2.0・
シンガポール国立大学）が license-review に係属している。proliferation の問いは、この節を
書く前は抽象的だったが、いまは**具体的な競合が 2 つある**状態で問われる。

> **English:**
>
> **What each is for.** OpenMDW and ModelGo answer *"how do I license a machine learning
> model?"* Both define their subject matter as model artefacts: OpenMDW's "Model Materials"
> are "one or more machine learning models (including architecture and parameters); and all
> related artifacts (including associated data, documentation and software)"; ModelGo's
> "Licensed Materials" are the Model plus Complementary Materials, with pretraining datasets
> expressly outside scope. ACD-1.0 answers a different question — *"how do I release any work
> so that machine processing of it is unencumbered?"* — and reaches models only because a model
> is a work like any other.
>
> | | OpenMDW-1.1 | MG0-2.0 | MG-BY-2.0 | ACD-1.0 |
> |---|---|---|---|---|
> | Subject matter | Model Materials (model + data + docs + software) | Model + Complementary Materials; **pretraining data excluded** | same as MG0 | any Work; data, metadata, audiovisual named (§1.2) |
> | Copyright | yes | yes | yes | §3 surrender, §4 licence |
> | Patent | yes, incl. indirect infringement | yes | termination clause; grant not stated in the same terms | §8.1, and §8.4 reaching models and outputs |
> | Database rights | yes | yes | yes | §7 (sui generis + unfair extraction) |
> | **Trade secret** | **yes, expressly** | not named | not named | **not covered** — §1.5 lists copyright, performance, broadcast, database, unfair extraction, "any right of similar effect", and excludes patents, trademarks, moral rights |
> | Conditions on You | **retain agreement + notices** | trademark/publicity consent | **attribution + modification notice + retained notices**; trademark/publicity consent | none (§10.1) |
> | Patent retaliation | **terminates on suit** | — | **terminates on suit** | **none, expressly** (§8.2) |
> | Outputs | no restrictions or obligations | disclaimed | disclaimed | §6.4 unencumbered; §8.4 patent grant follows outputs |
> | Distilled / synthetic-data models | not addressed | **excluded from Derivative Materials** | excluded | not carved out; §8.4 reaches "any model, parameter set, weight, embedding, or output" |
>
> **Where they are better than ACD-1.0, stated plainly.**
>
> 1. **For releasing a model, OpenMDW is the better fit.** It names the artefacts a model
>    release actually consists of, it is drafted by the Linux Foundation, and it has been through
>    counsel. ACD-1.0 covers the same material only by generality. If the question is "what
>    licence do I put on my weights", the honest answer today is OpenMDW, not ACD-1.0.
> 2. **OpenMDW covers trade secret rights and ACD-1.0 does not.** For model weights — where
>    protection may rest on confidentiality rather than copyright — that is a real gap on our
>    side. (Whether licensing a trade secret has legal meaning was itself questioned in OpenMDW's
>    review, so the advantage is contested rather than settled.)
> 3. **Both have institutional stewards.** ACD-1.0 has one individual (adverse fact #10).
>
> **Where ACD-1.0 differs, and it is not only in its favour.**
>
> 1. **ACD-1.0 imposes no condition at all.** OpenMDW requires the agreement and notices to be
>    retained; MG-BY requires attribution and a modification notice. Whether "no condition" is
>    better depends on the adopter, not on the instrument.
> 2. **ACD-1.0 has no patent retaliation.** OpenMDW and MG-BY terminate on suit. ACD-1.0 §8.2
>    declines that expressly. This is a deliberate difference — a termination trigger is a
>    condition — but many reviewers regard defensive termination as a feature.
> 3. **ModelGo carves distilled and synthetic-data-derived models out of Derivative Materials;
>    ACD-1.0 grants toward them.** §8.4 reaches "any model, parameter set, weight, embedding, or
>    output" of Computational Use. On this axis ACD-1.0 is the more permissive instrument, and
>    it is the axis where the three are genuinely in tension rather than merely different.
> 4. **ModelGo restricts referring to the Licensor for publicity without prior written consent.**
>    ACD-1.0 grants no trademark right (§11.1) but imposes no such restriction.
>
> **Do they compete?** Partly. They overlap where the Work is a model and the question is
> licensing its artefacts — there OpenMDW is purpose-built and ACD-1.0 is general. They do not
> overlap where the Work is not a model: OpenMDW and ModelGo have nothing to say about a
> documentation set, a dataset released on its own, a metadata layer, or material whose
> authorship is uncertain, and ACD-1.0's §9 is addressed to exactly that last case. The three
> are best read as answering adjacent questions, and **that is an argument for ACD-1.0 existing
> only if the adjacent question is worth a separate instrument** — which §1 of this document
> says is true in a narrow band and false outside it.

## 2. Copyleft 系（GPL / AGPL / LGPL / MPL / EUPL）

**これは価値観の問いである。** 「なぜ共有を要求しないのか」に技術的な答えを返すと噛み合わない。

> **English:**
>
> I am not arguing that copyleft is wrong. I am saying it does not fit what this particular
> work is for.
>
> - **GPL-2.0 / GPL-3.0** require that derivative works be distributed under the same terms
>   and that source be made available. **AGPL-3.0** extends that to network use. Those are
>   conditions, and this instrument is built on having none (Section 10.1) — not because
>   conditions are bad, but because the work exists to be absorbed by systems that cannot
>   accept terms (Section 1.4 speaks of automated actors, Section 2.3 removes acceptance).
>   A model trained on a corpus cannot "distribute the corresponding source".
> - **LGPL** and **MPL-2.0** are weaker but still conditional: MPL is file-level copyleft with
>   a patent grant and **patent retaliation**. Section 8.2 explains why retaliation is
>   deliberately absent here.
> - **EUPL-1.2** is a copyleft licence published in the official EU languages, all equally
>   authentic, with a compatibility list for other copyleft licences. Its multilingual design
>   is a genuinely good idea and Section 16.5 borrows the spirit — translations may circulate
>   under the same name — but Section 15.8 keeps English authoritative rather than making
>   every language equally binding, because a licence that imposes no condition has far less
>   to lose from a translation dispute than one that does.
>
> **What ACD-1.0 gives up by not being copyleft:** a downstream user may take the work,
> improve it, and share nothing back. That is a real cost and I accept it. Section 4.5 says
> so plainly — You may redistribute under terms incompatible with these.

**なぜこう答えるか**: copyleft 支持者に対して「条件は悪」と言うと議論が価値観の衝突になる。**「あなたの選択が誤りだとは言っていない。この作品には合わないだけだ」**と述べ、**失うもの（還元されない）を自分から認める**のが唯一噛み合う形である。EUPL の多言語設計を褒めているのは追従ではなく、§16.5 が実際にその方向を採っているからである。

---

## 3. AI 用途制限系（RAIL / OpenRAIL / Llama / Gemma / BigScience）

**ここが最も誤読されやすい。** 近年「AI に言及するライセンス」の大半は**制限**であり、レビュアはその前提で読み始める。

> **English:**
>
> ACD-1.0 points in the opposite direction from the RAIL family, and I want to be explicit
> about it because the surface similarity ("a licence that talks about machine learning")
> hides an inversion.
>
> - **RAIL / OpenRAIL** licences impose **use-based restrictions**: enumerated behavioural
>   prohibitions that flow down to derivatives. Whatever their merits, they are not
>   OSD-conformant, because OSD 6 forbids discrimination against fields of endeavour.
> - **Llama Community License** and similar model licences add an acceptable-use policy and,
>   in Llama's case, a scale threshold above which a separate licence must be negotiated.
>   That is a restriction on persons and on scale.
> - **BigScience BLOOM RAIL** likewise enumerates prohibited uses.
>
> ACD-1.0 has **no** enumerated prohibitions, no acceptable-use policy, and no scale
> threshold. Section 6.1 permits computational use **for any purpose**; Section 4.3 excludes
> conditions on "field of use" and on "the identity, character, or purpose of the user" in
> terms. Section 6 exists to *remove* doubt about permission, not to add limits.
>
> If the committee's instinct on seeing "machine learning" in a licence is "here comes
> another use restriction", I would rather that instinct be corrected in the first paragraph
> than at the end of a long thread.

**なぜこう答えるか**: **表面の類似（AI に言及する）が反転を隠している**。この誤読は放置すると OSD 6 の議論全体を汚染するので、§3 の OSD 逐条でも先回りしているが、族比較としても独立に置く。「その直感は正しいが、この文書には当てはまらない」と述べるのが最短。

---

## 4. Source-available 系（BUSL / SSPL / Elastic / PolyForm）

> **English:**
>
> These are not comparable and I mention them only because the phrase "not a standard
> licence" sometimes pulls them into the conversation.
>
> **BUSL-1.1** restricts production use until a change date, after which the work converts to
> an open licence. **SSPL** requires the source of the entire service stack. **Elastic
> License 2.0** forbids providing the work as a managed service. **PolyForm** is a family of
> deliberately non-open licences.
>
> Every one of them adds restrictions relative to a permissive licence. ACD-1.0 removes them
> —— it has no condition at all (Section 10.1), no termination (Section 10.4), and no
> field-of-use limit (Section 4.3). The two directions could not be further apart, and I
> would not want ACD-1.0 grouped with them merely because both are non-standard.

**なぜこう答えるか**: 「独自ライセンス」という語が source-available 系を連想させることがある。**方向が正反対である**ことを一度言えば済むので、短く置く。

---

## 5. データ系（ODbL / CDLA / PDDL / CC-BY-SA）

> **English:**
>
> The Work here is not only software (Section 1.2 includes data, metadata and audiovisual
> material), so data licences are a fair comparison.
>
> - **ODbL** is share-alike for databases: derived databases must be offered under ODbL. That
>   is a condition.
> - **CDLA-Permissive-2.0** is close in spirit — permissive, data-oriented — but is silent on
>   patents, on TDM reservation, and on machine-generated material. **CDLA-Sharing** adds a
>   share-alike condition.
> - **PDDL-1.0** is a dedication for data and is the closest data-side analogue, but like CC0
>   it does not grant patents and says nothing about reservation.
> - **CC-BY-SA-4.0** conditions on attribution and share-alike.
>
> Section 7 exists precisely because the sui generis database right is a *different* right
> with its own vocabulary (extraction, re-utilisation). A licence that covers copyright and
> is silent on the database right leaves a European user unsure whether systematic extraction
> is permitted.

**なぜこう答えるか**: Work がソフトウェアに限られないので、**データ族を無視すると「そこは考えていない」と見なされる**。§7 の存在理由がそのまま答えになる。

---

## 5.5 「CC0 と特許誓約を組み合わせればよいのでは」

**これは最も鋭い代替案**であり、Q13（CC0 + Apache-2.0）とは別に扱う価値がある。

> **English:** This is the strongest alternative I have been offered, and it is not obviously
> wrong. CC0 gives away copyright; a separate patent pledge — a defensive-patent arrangement,
> a membership in a patent non-aggression community, or a unilateral written pledge — could
> in principle supply what CC0 Section 4(a) withholds.
>
> Three structural differences made me not take that route.
>
> 1. **Two instruments, and the user must find both.** A licence travels with the work; a
>    pledge published elsewhere does not. A recipient three hops downstream sees CC0 and has
>    no way to know a pledge exists, or whether it still does. Section 8 is in the same file
>    as Section 3, and Section 16.2 makes the identifier alone sufficient notice for both.
> 2. **The pledge's own terms are separate.** Scope, duration, revocability, and who may rely
>    on it are decided by the pledge, not by the licence, and they differ between arrangements.
>    A user evaluating risk has to read and reconcile two documents written by different
>    people for different purposes.
> 3. **Neither reaches models and outputs.** Section 8.4 exists because Covered Rights exclude
>    patents (Section 1.5), so a copyright-side permission for computational use leaves a
>    patent-shaped hole over models, weights and outputs. A general patent pledge aimed at
>    software implementations does not obviously close that hole, and I did not want to rely
>    on it doing so by implication.
>
> If someone shows me a pledge that travels with the work, is unconditional, and reaches
> outputs, then CC0 plus that pledge would do what this does, and I would use it.

**なぜこう答えるか**: **「二文書に分かれること」が構造的な差**であり、優劣の主張ではない。
最後の一文は Q1 と同じ姿勢（**既存で埋まるなら使う**）を、この代替案に対しても具体的な条件
つきで述べている。

---

## 6. 族をまたぐ判断基準（読み手が自分で当てはめられる形）

> **English:**
>
> If you are deciding whether ACD-1.0 is the right choice, three questions settle it:
>
> 1. **Do you want anything back?** If yes — attribution, source, share-alike — do not use
>    this. Use a permissive licence with a notice condition, or a copyleft licence. ACD-1.0
>    asks for nothing and Section 10.3 says that a request is not a condition.
> 2. **Do you want to restrict any use?** If yes — non-commercial, non-military, no-AI, no
>    managed service — do not use this. Section 4.3 forecloses every such condition, and a
>    licence cannot both be unconditional and carve out a use.
> 3. **Do you hold patents that read on the work?** If yes and you are not willing to license
>    them, do not use this. Section 8.3 rejects any reading that preserves them.
>
> If all three answers are "no", the remaining question is whether an existing unconditional
> licence already covers your case. If your work is software only, and you do not care about
> patents, TDM reservation, or machine-generated authorship, **0BSD is simpler and I would
> recommend it over this**.

**なぜこの節を置くか**: 採用検討者への誠実さであり、同時に**「自分のライセンスを売り込んでいない」ことの証拠**になる。**条件が合うなら 0BSD を薦める**と書けることが、proliferation の指摘に対する最も強い姿勢である。

---

## 7. この比較で意図的に扱っていないもの

| 扱っていないもの | 理由 |
|---|---|
| 各ライセンスの**条文の正確な引用** | 引用は誤りが混入しやすく、本書の主張は**構造の違い**にあって字句の差ではない。字句が必要なら一次資料を見るべきである |
| OSI 承認の有無の一覧 | 時点依存で腐る。**承認一覧は OSI の公開ページが一次資料**であり、ここに写すと drift する |
| バージョン差（GPL-2 と GPL-3 の詳細等） | 本書の論点（条件の有無・方向）はバージョンを跨いで同じ |
| 「どちらが優れているか」 | 比較の目的は**別物であることの説明**であって優劣ではない |

**扱わない理由を書いておくのは、抜けではなく判断であることを示すため**である。

---

**Lost?** [`QUESTION-INDEX.md`](QUESTION-INDEX.md) indexes every worked entry in this directory by
the question it answers. [`AS-OF.md`](AS-OF.md) lists which claims about the outside world were
verified when. [`ACD-1.0.against.md`](ACD-1.0.against.md) is the case against approving this.
