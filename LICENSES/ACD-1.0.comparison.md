---
file: LICENSES/ACD-1.0.comparison.md
audience: ai, human (提出者), 監査人, 採用検討者, 第三者全般
last-updated: 2026-08-27
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
> **The proliferation question is therefore not "is ACD-1.0 different?"** — it demonstrably is,
> in the four respects above. It is "**is that difference worth another licence in the world?**"
> That is a judgement for the list, and the honest position is that the answer is not obviously
> yes. What can be said is that the gap is real, that no approved licence closes it, and that
> combining approved licences does not close it either (§5.5 addresses the CC0-plus-patent-pledge
> construction directly).

---

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
