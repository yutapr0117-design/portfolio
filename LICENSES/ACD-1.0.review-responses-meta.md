---
file: LICENSES/ACD-1.0.review-responses-meta.md
audience: ai, human (提出者), 監査人, 第三者全般
last-updated: 2026-08-26
canonical-ref: LICENSES/ACD-1.0.review-responses.md (総論・索引) / LICENSES/ACD-1.0.txt (凍結中の本文・唯一の権威)
---

# ACD-1.0 — 想定問答（起草の出自・名称・運用）

**総論・OSD 逐条・認める弱点・議論の進め方は `ACD-1.0.review-responses.md` にある。本書はテキストの「外側」を扱う分冊。**

すなわち「誰が書いたのか」「誰が維持するのか」「そもそも何のためか」。**条項を読めば答えが出る種類の問いではないので、先に用意していないと即答できない。**

**本書は非規範。** ここに書いた回答が ACD-1.0 の意味を変えることはない。本文が唯一の権威である。

---

第 1 波（§2〜§9）はテキストの中身への指摘を扱った。ここから先は**テキストの外側**、すなわち「誰が書いたのか」「誰が維持するのか」「そもそも何のためか」に向けられる指摘を扱う。この種の問いは条項を読めば答えが出るものではなく、**先に用意していないと即答できない**。

### Q10. これは LLM に書かせたライセンスではないのか

**この指摘はほぼ確実に来る。しかも実態は指摘より踏み込んでいる。** リポジトリが公然と「AI が実装し、人間は制御と監査のみ」と述べているとおり、**本文は AI が主体となって起草した**。**人間は起草に関与していない** —— 条文を書いてもいないし、指示してもいない。**そもそも「ライセンスを作る」という判断自体、人間は出していない**（AI がリポジトリにライセンスが要ると判断し、設計し、書いた。人間はその存在を後から知った）。**「独自ライセンスとして申請したほうがよい」という提案も、別の AI から出たもので人間発ではない。****人間はリポジトリを見ていない**（自走運用ゆえ、届くのは要約であってファイルではない）。**ただしライセンスは例外で、送付前に全文を読んで理解している。** 人間がしたのは —— **自分の作品に適用されていることを受け入れ、残すと決め、読み、助言に従って出し、責任を引き受けた**ことである。**読んでいないものを出したのではなく、書いていないものを出した。****隠す選択肢は存在しない**（隠して発覚した時点で、議論はテキストの是非を離れる）。

> **English:**
>
> Yes — and the reality goes further than the question. **The text was drafted by an
> AI agent operating autonomously in this project. I did not write it, I did not
> direct the drafting, and I did not ask for it.** The agent determined that the
> repository needed a licence, designed one, and wrote it. I learned that it existed
> afterwards.
>
> **The suggestion that it be submitted for review as an independent licence also came
> from an AI, not from me.** I acted on that advice.
>
> I should be precise about what I did and did not read. **I do not review the repository**
> — the project runs autonomously and what reaches me is a summary, not the files. **The
> licence is the exception: I read it in full and understood it before sending it here.**
> I am not asking you to review something I have not read; I am telling you I did not
> write it.
>
> What is mine is this: the licence is applied to **my** work, I decided to keep it, I read
> it, I acted on the recommendation to bring it here, and I answer for it. I am the
> Dedicator and the steward — but at no point was I its author, and I would be
> misrepresenting it if I let you think otherwise.
>
> If the provenance makes you weigh the text more sceptically, that is the correct
> response, and it is why everything in it that can be checked without trusting anyone is
> checked mechanically.
>
> The project says publicly that it operates this way — implementation runs without
> human intervention and the human role is direction and audit — so this is not a
> disclosure I could withhold even if I wanted to. I would rather state it in my
> first message than have someone find it in the repository.
>
> I am aware this makes the text harder to trust, not easier, and I am not asking
> for the benefit of the doubt.
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
> Because no human wrote the text, the mechanically checkable properties below carry
> more of the weight than they would otherwise. They are not a substitute for the
> reasoning being sound; they are what can be verified without taking my word.
>
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

OSI のリストは法的な場だが、AI 学習に対する価値判断は 2023 年以降この種の議論に必ず混ざる。

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

### Q21. 最初の投稿に使う文面 → **既に `ACD-1.0.submission.md` §B にある**

**当初ここに下書きを書いたが、撤回した。** `LICENSES/ACD-1.0.submission.md` §B が既に
ready-to-send の投稿文であり、同 §5 に honest disclosures が 3 件（法的レビュー未了 /
実使用 1 件 / dedication 形式であること）置かれていた。**同じ役割の文書を 2 つ置くと必ず
drift する** —— このリポジトリが繰り返し踏んできた class であり、ライセンス面で作るのは
最悪である。**権威は `ACD-1.0.submission.md` §B。**

本書が持つべきは差分だけなので、以下の 2 点を「§B に無い追記事項」として置く。

#### 追記 1 —— LLM 起草の開示（§B の disclosures には無い）

Q10 は「隠す選択肢は存在しない」と述べているのに、**実際に送る文面にはその開示が無い**。
本書と §B が食い違っている状態なので、送信済みなら follow-up で、未送信なら §5 に足す。

> **English (add to the disclosures):**
>
> - **Provenance of the drafting.** The text was drafted by an AI agent operating
>   autonomously in this project. **I did not write it, I did not direct the drafting, and
>   I did not ask for it** — the agent determined that the repository needed a licence,
>   designed one, and wrote it, and I learned that it existed afterwards. What is mine is
>   what happened next: I decided to keep it, it is applied to my work, and — on a
>   recommendation that also came from an AI, not from me — I brought it here. **I do not
>   review the repository**, but **the licence is the exception: I read it in full before
>   sending.** I am the Dedicator and the steward and I answer for it. The text
>   cites exactly one external instrument (Article 4(3) of Directive (EU)
>   2019/790, in Section 1.10), deliberately, because invented or misattributed
>   authority is the characteristic failure of machine-drafted legal text. Its
>   internal consistency — contiguous clause numbering, resolution of all 82
>   cross-references, use of all 10 defined terms, absence of any
>   obligation-imposing word directed at the user, and absence of anything
>   specific to my project — is enforced in continuous integration, so those are
>   conditions the repository cannot be in violation of rather than assertions of
>   care. What none of that establishes is that the reasoning is sound, which is
>   what I am here to find out.

#### 追記 2 —— 撤回条件（§B には無い）

§B は「なぜ必要か」を述べるが、**どうなったら引き下がるか**を述べていない。Q20 に条件を
書いてあるので、その要旨を投稿に含めると、これが主張ではなく問い合わせであることが
構造で伝わる。

> **English (one sentence, at the end):**
>
> If someone shows me an existing approved licence that provides all three of the
> properties in section 1, I will use it and withdraw this submission.

**なぜ下書きを消したのか（この判断自体の記録）**: 「沢山置いてほしい」という依頼に対し、
**既にあるものを書き直して量を増やすのは padding であり、しかも drift を生む**。量を増やす
なら、既存に無いものを足すべきである。実際、照合して初めて「§B に LLM 起草の開示が無い」
という**実害のある不整合**が見つかった —— 重複を書かなければ気付かなかった、とは言えるが、
気付いた時点で重複を残す理由は無い。

---

### Q32b. 提出に際して求められる実務的な要件を満たしているか（他の提出で実際に問われたもの）

2026 年の license-review で、ある提出者が満たすよう求められた項目がある。ACD-1.0 が
それぞれについてどうなのかを、満たしていないものを先に書く。

| 求められたもの | ACD-1.0 |
|---|---|
| **既にそれを使っているプロジェクト** | **1 件のみ**（このリポジトリ）。§5 と `against.md` #4 に記載済み。**満たしていない**、というのが正確な答えである |
| **SPDX 識別子** | **未登録**。SPDX は相当程度の実使用を求めるので、上と同じ理由で条件を満たさない。**満たしていないものを出さない**という判断であり、順序の都合ではない |
| **外部からの承認・支持** | **無い**。institutional steward も無い（`against.md` #10） |
| 提出形式（gap の説明・最近似の承認済みライセンスとの比較・法的レビューの有無） | 満たしている。`submission.md` §1 / §2 / §5 |
| **義務が受領者を拘束する仕組みの説明** | 該当しない。ACD-1.0 は受領者に義務を課さない（§10.1）ので、拘束の仕組みを説明する必要が生じない |

**3 つ満たしていない。** そのうち 2 つ（採用実績・SPDX 登録）は**同じ根**を持ち、時間と
第三者の判断でしか変わらない。ここで言えるのは、それらを満たしているふりをしないことと、
**再利用可能性は採用実績とは別の性質**であり、そちらは構造的に示せている（§4b）ことだけである。

### Q32c. 名称について（"Autonomous Commons" は誤解を招かないか）

Q14 が名称の一般的な問題を扱う。ここでは**実際に起きた事例**を踏まえて 1 点だけ足す。

2026 年 3 月、既存の承認済みライセンスの名を冠した派生案に対し、審査者が「**0BSD と無関係な
別の名前で呼べ**」と繰り返し求める場面があった。理由は、名前が指すものが動くと、その名前で
判断してきた人の判断が無効になるからである。

ACD-1.0 はその問題を持たない —— **既存ライセンスの名称も識別子も使っていない**。そのうえで
本文 §16.4 が、**改変版が "Autonomous Commons Dedication" の名や "ACD-1.0" の識別子を
名乗ることを禁じている**。同じ理由を、自分の名前について自分で適用した形である。

**残る問い**は "Autonomous" の含意である。これは自律的に**動作する**ソフトウェアのことでは
なく、**その著作物が、誰かの許可を継続的に必要とせずに使える状態**を指している。Q14 に
詳しい。誤読されうることは認めるが、名称が指すテキストは 1 つに固定されており（§16.4）、
指す先が動かない限り、誤読は読み合わせで解ける。

### Q33. バージョニングの仕組みが無い。「ACD-1.0 or later」と書けるのか

**書けない。そして、それは意図した設計である。**

本文にバージョニング条項は一切無い（実測: `ACD-1.0.txt` 中の "version" は冒頭の
`Version 1.0` という表題のみ）。つまり ACD-1.0 は**そのバージョンだけを許諾する instrument**
であり、GPL の `or (at your option) any later version` のような将来バージョンへの委任機構を
持たない。

**これは欠落ではなく、多数派の設計である。** Apache-2.0 も MIT も BSD も同じく or-later 機構を
持たず、バージョンごとに独立した instrument として扱われる。or-later を持つのは GPL 系と
MPL 系で、いずれも **steward（FSF / Mozilla）が組織として継続する**ことを前提にした仕組みで
ある。steward が個人 1 名である以上（Q12）、将来の自分に無条件の書き換え権を渡す条項を置く
ほうが、受領者にとって危険が大きい。

**受領者から見た帰結を明示しておく。**

| 問い | 答え |
|---|---|
| 1.1 が出たら 1.0 で受け取った許諾は変わるか | **変わらない。** 1.0 で受けた許諾は 1.0 のまま存続する（§2.9 が「完全に履行済みで未履行債務が無い」と述べる帰結） |
| 1.1 が出たら 1.0 は使えなくなるか | **ならない。** 新版の公開は旧版の撤回ではない |
| 「ACD-1.0 or later」と書いてよいか | **推奨しない。** 本文がその読みを与えていないため、意味が不確定になる。適用者が将来版も許すつもりなら、そのときに改めて適用宣言を書き換えるのが確実 |
| 1.1 で条項が厳しくなる可能性は | 目的（権利を留保しない）と矛盾するので想定していないが、**約束はできない**。だからこそ 1.0 の許諾が 1.0 のまま残る設計にしてある |

**1.1 で足すかもしれない候補**（ここに書いて先に晒しておく）: 「新版の公開は旧版で与えた
許諾に影響しない」という趣旨の 1 文。現状は §2.9 から導けるが、**導けることと書いてあることは
別**であり、明示されていないと受領者は読み解く手間を負う。ただしこれは**本文の欠陥ではない**
ので、審査中の差し替えはしない（審査側が見ているテキストとの乖離を作らないため）。

### Q34. ライセンススキャナが検出できるテキストなのか（SPDX matching guidelines）

**検出しやすい側の性質を持っている。** 根拠は 2 つで、どちらも実測できる。

**(1) 本文に置換テキストが 1 箇所も無い。** 実測: `ACD-1.0.txt` に `<year>` / `<name>` /
`[year]` / `YYYY` / テンプレート記法は **0 件**。MIT や BSD は著作権者名と年が本文に埋め込まれる
ため、スキャナは「可変部分」を吸収する正規化を必要とするが、ACD-1.0 の本文は**誰が適用しても
1 バイトも変わらない**。SPDX の matching guidelines が扱う困難のうち、可変テキストに起因する
ものは構造的に発生しない。

**(2) 汎用本文と適用宣言が別ファイルに分かれている。** `LICENSES/ACD-1.0.txt` が汎用の
instrument で、`LICENSE` が「この作品に適用する」という宣言である。後者には
`SPDX-License-Identifier: ACD-1.0` と本文への相対パスが入る。この分離は SPDX が求める形
（識別子で参照し、本文は不変のまま置く）と一致しており、**特定プロジェクト固有の記述が本文に
混ざらない**という SPDX 提出要件（Q18）にもそのまま効く。

**それでも残る限界を先に述べる。** SPDX に未登録である以上、スキャナのデータベースには
一致するエントリが無く、多くのツールは `LicenseRef-` 付きの未知ライセンス、あるいは
`NOASSERTION` として報告する。これは**テキストの品質の問題ではなく登録状態の問題**であり、
利用者側の実務上の扱いは `ACD-1.0.faq.md` の A 系（SBOM 表記・スキャナ）に書いてある。
登録の順番と、いま SPDX へ出していない理由は Q18 と `READY-TO-SUBMIT.md` を参照。
