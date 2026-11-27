---
file: LICENSES/FAQ.md
audience: 採用検討者, 法務, ai, human (提出者), 監査人, 第三者全般
last-updated: 2026-11-26
canonical-ref: LICENSES/ACD-1.4.txt (このリポジトリが適用する確定版・答えはこの本文に当てる) / LICENSES/ADOPTING.md (採用の手順) / LICENSES/ACD-1.0.comparison.md (族ごとの比較) / LICENSES/ACD-1.0.jurisdictions.md (法域別の問い)
---

# ACD — 実務 FAQ（使う人・法務・観察者向け・ACD-1.4 に当てて）

```
本書の役割 : レビュアではなく **実際に使うかもしれない人**の疑問に答える
本書の性質 : 非規範。齟齬があれば本文が勝つ。法的助言ではない
当てる版   : ACD-1.4（root の LICENSE が名指し、ADOPTING.md が勧める確定版）
関連       : 逐条は clause-reference / 族比較は comparison / 法域は jurisdictions /
            レビューの想定問答は review-responses{,-clauses,-meta}
```

---

> **版について（2026-11-26・議題 13）**: この FAQ は 2026-11-26 まで `ACD-1.0.faq.md` の名で ACD-1.0 に向けて書かれ、1.4 との差を各問の注で足していた。勧める版と説明する版が違うことは採用者を迷わせる（B2）ので、名を版に依らない `FAQ.md` に替え、答えを ACD-1.4 の本文に当てて書き直した。条番号は特に断らない限り ACD-1.4 のもの（1.0 と 1.4 は 16 節の骨組みが同じで、多くの番号が一致する）。**1.0〜1.3 で答えが違う所は、各問の末の「前の版」に書く。** OSI の `license-discuss` へ投稿した本文は ACD-1.0 で、条番号の対応は `REVIEWERS.md` の "Which text you are looking at" にある。

## A. 使う側の疑問

### A1. 自分の作品に使ってよいか

> **English:** Yes, without asking, if you hold rights in it. Section 16.3 says that the
> Dedication may be applied by anyone, *"to any material in which they hold or may hold rights
> of their own"*, without permission from, notice to, or any relationship with its authors.
> Section 16.1 gives a notice form, and Section 16.2 says that the identifier, an SPDX tag, or a
> reference by name and version is sufficient notice.

**先に確認すること**: **あなたがその作品の権利を持っているか**。職務著作や譲渡で雇用主が権利を持つ場合、あなたは適用できる立場にない（**A20** 参照）。共同で作ったものなら **A13** も見ること。

**適用の仕方**: §16.1 の書式の通知を作品に添える。全文の同梱は不要で、§16.2 のとおり、識別子 `ACD-1.4`、`SPDX-License-Identifier: ACD-1.4` か `LicenseRef-ACD-1.4` の tag、または**名前と版**による言及で通知として足りる。**名前だけでは足りない**。

*前の版*: 1.0 の §16.3 は *"to any work"* で、権利を持つかを言わなかった（1.1 から限った・errata E2）。名前だけで通知として足りたのは 1.0〜1.2 で、1.3 から版を要する（errata E38）。

### A2. 通知や帰属表示を残す必要はあるか

> **English:** No. Section 10.2 says in terms that You need not give attribution, reproduce any
> notice, state that the Work was modified, make source available, license anything under this
> Dedication or any other terms, **retain this file**, or inform anyone of anything.

**README に「引用してください」と書いてあった場合も同じ**である。§10.3 が、Dedicator の依頼・希望は、どこでどう述べられても依頼であって条件ではなく、義務を作らず、従わなくても違反でなく、どの許諾も限らず終わらせない、と述べている。

### A3. 改変して再配布するとき、何をすればよいか

> **English:** Nothing is required. You may distribute the Work and any adaptation or
> collection containing it under **any terms You choose**, including terms that impose
> conditions on Your own recipients and terms incompatible with this Dedication (Section 4.5).
> You need not mark changes (Section 10.2).

ただし §4.6 が、**あなたが付けた条件は「あなたが与えるもの」を規律するだけ**で、受領者と本 Dedication の関係を切らないと定めている。受領者は自分の権利として §1.6 の "You" になる。**あなた自身がその素材の Dedicator でもある**とき（自分の寄与を含めて配るときなど）は、§4.5 の末文のとおり、§5 が禁じることをその素材に課すことはできない。

### A4. 商用利用・軍事利用・その他の用途制限はあるか

> **English:** None. Section 4.3 excludes conditions on field of use, on *"the identity,
> character, size, revenue, or purpose of the user"*, on the scale of use, and on any
> restriction as to persons, groups, technologies, endeavours, or jurisdictions. Section 6.1
> permits Computational Use for any purpose. There is no acceptable-use policy and no scale
> threshold.

### A5. GPL / Apache のプロジェクトに取り込めるか

> **English:** Yes. Because there is no condition to satisfy (Section 10.1), the Work can be
> combined with material under any licence, and the combination can be distributed under that
> licence's terms (Section 4.5). Nothing flows back from this instrument to constrain the
> combined work.

**逆向き**（ACD の作品に GPL のコードを混ぜる）は**別の話**である。混ぜた相手の条件はその相手のライセンスが決めるので、**GPL コードを取り込めば結果物は GPL の条件に従う**。本 Dedication は §2.7 のとおり **Dedicator が持つ権利にしか及ばない**。

### A6. 特許を持っている。適用してよいか

> **English:** Only if You are willing to license them. Section 8.1 grants a licence under every
> patent claim You own or control that acts in respect of the Work or anything derived from it
> would infringe, where the infringement is caused by subject matter contained in the Work as
> You made it available. Section 8.4 grants a licence for Computational Use and for models and
> outputs, reaching a claim only where the infringing feature results, in whole or in part, from
> the content of the Work. Section 8.3 says nothing reserves a claim those Sections reach. If You
> are not willing to do that, this is the wrong instrument.

**これは適用者側の判断であって、利用者側の心配ではない。** 利用者から見れば §8.5 のとおり「Dedicator が所有または支配する請求項にしか及ばない」ので、第三者特許の risk は別に残る（§13.2 が非侵害を保証しないと明言）。**支配**は §8.5 が定義する（義務に反さず支払いも生まずに許諾できる請求項だけ）。**所有する請求項にはこの条件が掛からない**ので、既に独占実施権を出した請求項も許諾する（errata E91・**A32**）。寄与者の請求項のうち、寄与と元のプロジェクトの組み合わせで初めて侵害するものに届くかは読みが割れる（errata E95）。

*前の版*: 1.0 の §8.4 は因果の限定を持たず、モデル・出力に関わる請求項に広く届いた（1.1〜1.3 は 2 通りに読める・`against.md` #282）。「支配」の定義は 1.4 から（errata E39）。

### A7. データセットやモデルに使えるか

> **English:** Yes. Section 1.3 defines the Work as the material to which the Dedicator has
> applied the Dedication, in any medium and in any form, including data and metadata as well as
> source and object code. Section 7 addresses the sui generis database right, and Section 7.2
> permits repeated and systematic extraction and re-utilisation of the whole or any substantial
> part of the contents, so far as the Dedicator's Covered Rights are concerned.

### A8. 学習に使ってよいか。学習して作ったモデルや出力は自由か

> **English:** Yes to both, as far as the Dedicator's rights go. Section 6.1 permits Computational
> Use for any purpose; Section 6.2 says the Dedicator makes no Reservation; Section 6.4 says that,
> to the fullest extent the law permits, no enforceable claim arises against You, under this
> Dedication or under any Covered Right of the Dedicator, in respect of a model, parameter set,
> weight, embedding, output or other data resulting from Computational Use of the Work, and that
> You owe nothing under this Dedication in respect of any of them. Section 8.4 grants the
> corresponding patent licence, reaching a claim where the infringing feature results, in whole
> or in part, from the content of the Work.

**届かないもの**: 他の権利者の権利（§2.7）、個人データ・肖像の法（§11.4・**A28**）、他の権利者が自分の権利について置いた opt-out（§6.2 の末・**A29**）。

*前の版*: 1.0 の §8.4 は因果の限定を持たなかった（**A6** の「前の版」）。

### A9. 作者が気を変えたら / 亡くなったら / 会社が破産したら

> **English:** Section 2.2 makes the Dedication irrevocable. Section 2.5 states that reliance is
> its purpose and that the Dedicator will not argue that it is revocable or ineffective for want of
> consideration or formality. Section 2.8 binds successors, assigns, heirs, personal
> representatives and transferees, to the fullest extent the law permits. Section 2.9 says that
> nothing in the Dedication is, under its terms, conditioned on, suspended by, or revived by an
> insolvency or similar proceeding, and treats an officer in one as a transferee.

**どこまで拘束できるかは法域による**（`ACD-1.0.jurisdictions.md` 参照）。条文は「法が許す限り」と書いており、**拘束できると断言はしていない**。米国では 17 U.S.C. §203 が 35 年後に許諾の撤回を許しうる（**A27**）。

*前の版*: 1.0 の §2.8 は拘束する条を §3・§4・§6・§8 と列挙し、§2.5 の禁反言が列の外にあった（errata E49）。1.0 の §2.9 は *"fully performed"* として「未履行でない」と言い切っていた（1.1 で外れた・errata E5・E30）。

### A10. SPDX 識別子が無い。ツールにどう書けばよいか

**これは現時点の実務上の最大の不便である。** ACD は SPDX License List に**未登録**（実使用が薄いため意図的に見送っている・B11）なので、SPDX ドキュメントでは **`LicenseRef-` を付けた形**で参照する。本文がそれを自分で言う。

> **English:** ACD is not on the SPDX License List. Section 16.1's notice form says
> *"SPDX-License-Identifier: ACD-1.4 (LicenseRef-ACD-1.4 while not on the SPDX License List)"*,
> and Section 16.2 accepts either tag as sufficient notice. In an SPDX document, use
> `LicenseRef-ACD-1.4` and supply the full text in `ExtractedLicensingInfo` (or your tool's
> equivalent). The tag is a notice form the Dedication defines; it is not a claim that the
> identifier is registered.

*前の版*: 1.0〜1.3 の §16.1 は `SPDX-License-Identifier: ACD-1.0`（各版の番号）だけを示し、`LicenseRef-` の形は本文に無かった。識別子は適用する版の番号で書く。

### A11. 依存関係スキャナが「未知のライセンス」と言う

想定内である。未登録の識別子はスキャナのデータベースに無い。実務的には次のいずれかになる。

1. `LicenseRef-ACD-1.4` として手動登録し、全文を添える（A10）
2. 組織のポリシー上「無条件・特許許諾あり」に相当する分類（例: public domain / permissive
   with patent grant）へ手動でマップする
3. **判断できないなら使わない** —— それは正当な選択であり、こちらから止める理由は無い

> **English:** If your tooling cannot classify it and your policy requires a listed licence,
> the correct answer is to wait. Declining is better than adopting something your process
> cannot account for.

### A13. 既存プロジェクトを ACD へ移行できるか

**「自分が全ての権利を持っているか」で答えが変わる。**

> **English:** If you hold all the rights, yes — Section 16.3 lets anyone apply this, without
> permission, to material in which they hold rights of their own. If other people have contributed, you cannot relicense their
> contributions unilaterally. You need either their agreement, or a prior licence that
> already permits what you are about to do (a permissive licence generally lets you
> sublicense; a copyleft one generally does not let you drop its conditions).
>
> Two things are worth saying plainly:
>
> - **Applying this does not reach past distributions.** Copies already released under the
>   old licence stay under it. Recipients keep what they were given.
> - **Applying this is irrevocable** (Section 2.2), and Section 2.5 says the Dedicator will
>   not later argue otherwise. If you are not certain, do not apply it yet.

**§2.6 が助けになる場面**: 今後の貢献については、貢献者が別段の意思表示をしない限り
本 Dedication の下で提出されたものとして扱われ、**そのために CLA のような別文書は要らない**。*（2026-11-24 訂正: 旧文は「別文書を要求できない」と書いていた。それは 1.0 と 1.1 の答えである —— その §2.6 は *"none may be required of them as a condition of the Contribution being accepted"* と書く (in ACD-1.0 and ACD-1.1)。1.2 からこの句は無く「要らない」と言うだけで、1.4 の §2.6 は *"Whether the Dedicator asks a contributor for anything else is a matter of project governance and is not addressed here."* と明示する。寄与について CLA を求めることは統治の問題である。CLA の義務の目的語は Work ではなく貢献者自身の寄与で、Dedicator が受け入れる見返りでもある（§2.6 の末文は、Dedicator が何も受け入れる義務を負わないと述べる）。**ただし端が 2 つ §5.2(b) の約束に反する**: (a) CLA が貢献者の Work の使い方を縛る条項（フォークしない、改変物を Dedicator にだけ許諾する、競合に使わない など）を持つとき、(b) 署名を Work の写しやリポジトリの入手の条件にするとき（§5.2(b) の *"access condition, click-through, registration requirement"*）。portfolio-5e の読み）。**逆側**: §2.6 の *"not addressed here"* の *here* は、本文の用法（*"a permission granted here"* など）では「この Dedication」と読むのが自然で、そう読むと Dedication 全体が CLA を扱わないと言い、(a)(b) の端と緊張する。それでも (a)(b) は §5.2(b) が自分の語で扱う Work についての義務と入手の条件で、*anything else* は寄与について求めるものなので、端は §5.2(b) に残る（両方の読みが残るなら §15.1 が §5.2(b) の及ぶ読みを選ぶ・`ACD-1.4-UNIQUE-READING.md` の §2.6 の CLA の行）。当初の「我々は『§2.6』と読む」は用法に合わなかったので改めた）*
ただしこれは**将来の貢献**についての規律であって、**過去の貢献を遡って変えるものではない**。

**貢献を受ける側の実務**: §2.6 の *"unless they state otherwise"* は記録を残さない。Apache-2.0 §5 も同じ形（*"Unless You explicitly state otherwise"*）で、承認済みの先例があるので本文は変えない。違いは費用で、ACD の放棄は寄与者にとって取り消せない。**別段の意思が述べられた貢献は、merge しないのが最も簡単である。**

### A14. 輸出規制・制裁法との関係は

> **English:** This instrument grants intellectual-property permissions and nothing else.
> Export control, sanctions, and similar public-law obligations are not the Dedicator's to
> grant or to waive. Section 11.4 states the shape of that limit: the Dedication, in respect of
> the Work, reaches Covered Rights, the patent claims Section 8 reaches, and Moral Rights to the
> extent stated in Section 12; *"It reaches nothing else, save that the covenants in Section 5
> are promises about the Dedicator's own conduct and are not limited by this sentence."*
>
> Because the licence imposes no condition (Section 10.1), it adds no export-related term of
> its own. It also removes none of your obligations under the law that applies to you.

**「無条件」は「法的義務が消える」という意味ではない。** §2.7・§11.4・§13.2 が一貫して**「Dedicator が持っているものしか渡せない」**と述べており、公法上の義務はその外側にある。

*前の版*: 1.0 の §11.4 は *"It reaches nothing else."* を無限定で述べ、§16（本文という文書）にも掛かって読めた（errata E44・1.4 で *in respect of the Work* を前置）。§5 の約束の但し書きは 1.4 から（SELF-AUDIT §3zd が残る食い違いを記録）。

### A15. 公共調達・組織のポリシーで「OSI 承認済み」が要件になっている

**その場合は使えない。** ACD は**どの版も OSI 承認を受けていない**（1.0 を `license-discuss` へ投稿した段階で、承認申請の窓口である `license-review` へは未提出）。

> **English:** If your policy requires an OSI-approved licence, ACD does not qualify today, and
> nobody should argue otherwise on its behalf. The current status is recorded in
> `LICENSES/FROZEN.md`. Waiting, or using an approved licence, is better than spending your own
> credibility on an unapproved one.

**これは採用者を減らす記述であり、意図的である。** 承認されていないものを「実質的に同等だ」と言わせるのは、こちらの都合で相手の信用を使わせることになる。

### A16. SBOM にはどう記載すればよいか

**A10（SPDX 識別子が無い問題）の実務面である。** SBOM（SPDX / CycloneDX いずれの形式でも）は
ライセンスを識別子で持つので、**未登録の識別子はそのまま書けない**。

> **English:** Record it as a user-defined licence entry — `LicenseRef-ACD-1.4` in SPDX terms —
> and attach the full text, which is short enough to embed. Do **not** map it to a
> superficially similar listed identifier (CC0, 0BSD, Unlicense) just to make the tool quiet:
> those differ on patents, which is the one place where the difference has teeth (Section 8.3).

**「似ているから」で既存識別子に丸めないこと。** とくに CC0 は**特許を明示的に除外**して
おり（§8.3 が拒絶する結果そのもの）、丸めると SBOM が**実態と逆のことを記録する**。

### A17. fork / vendoring / ミラーは自由か

> **English:** Yes, and nothing is required. Section 4.5 permits distribution of the Work and
> any adaptation under any terms You choose; Section 10.2 says You need not retain this file,
> reproduce any notice, or state that the Work was modified. Vendoring into a monorepo,
> mirroring, and forking are all ordinary uses.

**ただし §4.6** —— あなたが付けた条件は「あなたが与えるもの」を規律するだけで、
**受領者と本 Dedication の関係を切らない**。fork を閉じた条件で配っても、元の Work に
ついては受領者が自分の権利として §1.6 の "You" になる。

### A18. 名称や識別子は商標登録されているのか

**されていない。** §11.1 は「商標・サービスマーク・商号・ロゴ・氏名の権利を与えない」と述べるが、これは**存在する商標を留保する**条項であって、**商標を主張する**条項ではない。

> **English:** No trademark is claimed or registered. What keeps "ACD-1.4" pointing at one
> fixed text is **not** trademark law but Section 16.4: the text may be copied verbatim by
> anyone, and a modified text may not be distributed under any name containing "Autonomous
> Commons Dedication" or any identifier containing "ACD-" followed by a digit, except by the
> Steward (Section 16.5) for a new version under a number no earlier text has borne. A modified
> text may circulate freely — under a different name. Section 16.6 says these rules govern the
> text as a document and bind no one in respect of the Work.

**なぜ商標ではなく条文で守るのか**: 商標は登録・維持・行使のコストを steward に課し、**§13.3 が保守義務を負わないと述べているのと整合しない**。§16.4 なら、守る主体が消えても条文としての意味は残る。

*前の版*: 1.0〜1.3 の §16.4 は、その版の名と識別子だけを守り、Steward の定義（§16.5）が無かった。

### A19. ACD の版を「廃止」できるのか

**適用済みの作品については、できない。** §2.2 が撤回不能と定め、§2.5 が「後から無効だと主張しない」と述べている。**すでに配られたものは戻らない。**

> **English:** Deprecation, if it ever happens, can only mean "stop recommending it for new
> works". It cannot mean withdrawal: Section 2.2 is irrevocable and Section 2.5 forecloses the
> argument that it was not. Under Section 16.4 each name and identifier continues to denote one
> fixed text, so a successor is a new version under a new identifier, not a replacement of this
> one; a notice that names ACD-1.4 keeps naming ACD-1.4.

**これは cost として認めている**（想定問答 boilerplate 分冊 Q32）。後から静かに直せない代わりに、**識別子が指すものが動かない**という性質を得ている。

### A20. 会社員が業務で書いたコードに適用してよいか（職務著作）

**これは「適用してよいか」ではなく「あなたが権利を持っているか」の問題である。** そして
**実務で最も多い取り違え**でもある。

> **English:** Section 1.4 defines the Dedicator as each person or entity applying this
> Dedication **"to the extent that person or entity holds or may hold Covered Rights, Moral
> Rights, or patent claims in it"**, and Section 16.3 lets anyone apply it to material in which
> they hold or may hold rights of their own.
> If your employer holds the rights — through a work-for-hire rule, an employment agreement,
> or an assignment — then you are not the person who can apply this, and applying it does not
> transfer anything you do not have (Section 2.7).
>
> The instrument does not warn you about this and cannot: Section 13.2 disclaims any warranty
> that the Dedicator holds any right in the Work. **Check before you apply it, not after.**

**§2.2 が撤回不能である以上、間違って適用しても取り消せない**（少なくとも、こちらから
取り消す手段は用意していない）。**A13（移行）と同じ確認が要る。**

*前の版*: 1.0〜1.2 の Dedicator の定義は *"Covered Rights in it"* だけで、人格権と特許の請求項だけを持つ人を数えなかった（1.3 から・errata E35）。

### A21. FRAND 宣言している特許を持っている場合、§8 と衝突しないか

> **English:** Section 8.1 grants a licence under patent claims the Dedicator **owns or
> controls**, and Section 8.5 says that Sections 8.1 to 8.4 reach only such claims. Section 8.5
> defines control: a claim is controlled *"if, and only if, at the time in question, the
> Dedicator has the right to grant these licences under it without breaching an obligation to,
> or incurring a payment to, another person"*. A claim the Dedicator **owns** is granted without
> that test, so a claim already licensed exclusively, or committed to a standards body, is
> still granted as far as the Dedicator can grant it (errata E91, examined and left as it is).
>
> This states the structure rather than the conclusion, because how a prior commitment interacts
> with a later unconditional grant is exactly the kind of question no lawyer has looked at
> (`ACD-1.0.jurisdictions.md` §10).

**構造だけ述べて結論を述べていない**のは、`jurisdictions.md` と同じ姿勢による。**助言を得ていない領域で断定しない。** FRAND の約束を持つ請求項を持つなら、適用する前に約束の相手と自分の法務に確かめること（**A32**）。

*前の版*: 1.0〜1.3 は「支配」を定義しなかった（errata E39）。

### A12. 法務に説明するとき、何を見せればよいか

| 訊かれること | 見せる場所 |
|---|---|
| 条件はあるか | 本文 §10.1 / §10.2 / §4.3 |
| 特許はどうなるか | 本文 §8.1 / §8.4 / §8.5 |
| 何を保証しているか | 本文 §13.1 / §13.2（**4 つとも否定**している） |
| 我々の法域で効くか | `ACD-1.0.jurisdictions.md`（**結論は書いていない**と明記） |
| 既存ライセンスとの違い | `ACD-1.0.comparison.md` / `acd-license-rationale.md` §2 |
| 条項ごとの意図 | `ACD-1.4.clause-reference.md`（1.4 の 80 条・1.0 の版は `ACD-1.0.clause-reference.md`） |
| 弱点 | `READY-TO-SUBMIT.md`「残る弱点」/ 想定問答 §4 |

**弱点の場所を先に示すこと。** 法務が自分で見つけると、その後の説明が全部疑われる。

---

### A22. コード以外（画像・音声・埋め込みメタデータ）も対象か。第三者の資産はどうなるか

**このリポジトリが同梱している資産は、すべて ACD-1.4 の対象である。** §1.3 の "Work" は
source / object / documentation に加えて **data / metadata / audiovisual** を明示的に含む定義
なので、コードと非コードで扱いが分かれることはない。実測（2026-08-27）で追跡対象の資産は
4 件だけである。

| 資産 | 扱い |
|---|---|
| `yuta-yokoi-ai-pm-orchestration-system.webp` | 対象。**XMP に埋め込まれた AIO メタデータも Work の一部**（§1.3 が metadata を含む） |
| `yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3` | 対象。ID3 の埋め込みフィールドも同様 |
| `icon.svg` | 対象 |
| `e2e/.../homepage-baseline-chromium-linux.png` | 対象（テストの基準画像） |

**埋め込みメタデータを「別扱い」にしない**のは意図的である。AIO 層は「同じ主張がどの面でも
一致していること」で成立しており、本文だけ自由でメタデータだけ許諾が違う、という状態は
その主張自体を壊す。剥がす・書き換える・別の作品へ移すことも自由で、条件は課さない
（§10 / §11 が「条件ではない」と繰り返すとおり）。

**一方、同梱していない第三者の資産には及ばない。これは制限ではなく、及ぼしようがないという
事実である。** 具体的には Web フォント（`fonts.googleapis.com` / `fonts.gstatic.com` から
実行時に読み込む）で、**リポジトリには 1 バイトも入っていない**。したがって ACD が
それらの権利を許諾することはあり得ず、利用者は提供元の条件に従う。逆に言えば、この
リポジトリを丸ごと複製しても第三者資産の権利問題は発生しない —— 複製しているのは
「そこへの参照」だけだからである。

**確かめ方**: `git ls-files` で追跡対象の資産を数え、`index.html` の外部参照ホストを見れば、
同梱されているものと参照しているだけのものは 1 分で切り分けられる。ライセンスの主張を
信じる必要はなく、**実測で確認できる**形にしてある。

### A23. 派生物に別のライセンスを付けてよいか。逆に、他人の貢献はどう扱われるか

**付けてよい。制限は無い。** ACD は権利を留保しないので、派生物へ GPL でも Apache-2.0 でも
プロプライエタリでも、好きな条件を付けられる。copyleft のような「同じ条件で配れ」という
要求は存在しない（§10 / §11 が「条件ではない」と繰り返すのはこのため）。

ただし正確に言うと、**あなたが付けたライセンスが及ぶのはあなたの寄与部分だけ**である。
元の部分は ACD のまま誰でも自由に使える —— あなたが派生物に条件を付けても、
**上流のテキストから直接受け取る人の自由は減らない**（§4.6）。これは ACD に限らず、
留保しない型の instrument に共通する帰結である。

**逆方向（他人がこのリポジトリへ貢献する場合）。** CLA も DCO も要求していない。**ただし
「何も定まっていない」わけではない** —— §2.6 は、Contribution は**この Dedication の下で提出
されたものとし、提出者はその Contribution について Dedicator になる。ただし提出時に別段の
表示をした場合を除く**、と定める。つまり**既定は献呈で、外れたい人は提出時にそう言う**。
別途の証書や合意は要らない。CLA を求めるかはプロジェクトの統治の問題である（A13）。**Contribution に当たらないもの**も §1.9 が決める: 議論のためだけに送ったもの、提出者が Contribution でないと印したものは外れ、Contribution は Dedicator か、この Dedication の通知とともに Work を提供するリポジトリ・forum への提出に限る。

*前の版*: 受入の条件として別文書を要求してはならなかったのは 1.0 と 1.1 だけで、1.2 からはその句が無い。§1.9 の「通知とともに Work を提供する場」の限定と、印による除外は 1.4 から。

この既定の限界も書いておく。**ライセンスが自分の文言で第三者の行為の法的効果を決めることは
できない** —— 貢献者が拘束されるかは、その人が知らされていたか・提出をどう評価するかに
かかり、§2.6 がそう書いているからではない。しかも「黙っていたら献呈」という opt-out 構造は、
§6.2 が「沈黙を留保と読まない」と述べているのと**向きが逆**である（この緊張は
`ACD-1.0.against.md` #15 に不利な事実として記録した）。実務上は「プロジェクトが貢献者に
周知すべき既定」であって、自動的に成立する権利移転ではない。

そして
**ACD が適用されるのは適用者が権利を持つ部分だけ**なので、第三者の寄与を取り込んだ場合、
その部分についてまで「権利を留保しない」と宣言できるわけではない（§2.7 が他の権利者の
留保に触れないと述べるとおり）。

**現時点でこの区別が問題にならない理由**も述べておく。このリポジトリの実装コードは
**すべて AI が生成し、人間はコードを 1 行も書いていない**（C5）。外部からの pull request は
受け入れていないので、取り込まれた第三者の著作物は存在しない。将来受け入れるなら、
その時点で「どの部分が誰の寄与か」を記録する必要が生じる —— **いま無いから書いていない
のではなく、いま無いことを確かめたうえで書いていない**。

### A24. 「無保証・免責」は、消費者保護法のある国でも本当に効くのか

**全部そのまま効くとは限らない。そう書いてある。** §14.1 は故意・重過失・死亡・人身傷害の責任を、適用法が排除を認めない場合に限って先に除き、残りを "TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW" と条件を付けて免責する。§14.2 は「適用法が排除を認めない責任は、その法が認める最大限まで制限され、§14 の残りは効き続ける」と述べ、さらに、§2.5・§5・§8.6・§12.2 の約束に反して請求を主張し権利を行使した Dedicator の責任を限らない（§13.1 の無保証はこの句をどの版でも持たない —— 2026-11-24 に本文に当てて訂正。旧文は §13.1 も持つと書いていた）。
**効かない可能性を否認していない**のがこの条項群の設計である。

具体的に何が制限されうるか。

| 法域 | 制限されうる部分 |
|---|---|
| 日本 | 消費者契約法 8 条は、事業者の債務不履行・不法行為による損害賠償責任を**全部免除する**条項を無効とする（一部免除は故意・重過失で無効）。**ただし前提として「消費者契約」＝事業者と消費者の契約である必要がある** |
| EU | 不公正条項指令（93/13/EEC）が消費者契約の不当条項を拘束力なしとする。人身損害の責任排除は多くの国で無効 |
| ドイツ | BGB §309 が約款による責任排除を強く制限し、故意・重過失は免責できない |
| 米国 | UCC §2-316 の下でも "AS IS" は広く有効だが、州によっては consequential damages の排除が unconscionable とされうる |

**ただし ACD の場面では、そもそも「消費者契約」に当たらないことが多い。** これは
献呈（dedication）であって、対価も申込・承諾もない。受領者は何も支払わず、何の約束もして
いない（§2.3 は受け入れの行為を要らないとし、§10.1 は受領者に条件も義務も課さない）。消費者保護法の多くは
**事業者と消費者の間の契約**を対象にするので、対価なしの一方的な献呈がその枠に入るかは
法域ごとに別途の判断になる。**「入らないから安心」とは書かない** —— 判断できないことを
断定しないのが、この文書群の方針である。

**同じ理由が、逆の向きにも働く（2026-11-12 に足した）。** 献呈が契約でないことは、消費者保護法が当たらない理由になりうる一方で、免責そのものが受領者を縛らない理由にもなりうる。受け入れの行為を求めない形（§2.3・1.0 から同じ）について、OSI の委員長は 2002 年に *"From what various legal scholars tell me, a non-contractual license (such as the GPL) cannot cause you to give up your warranty rights. Only a contract can do that."* と書き、同じ年に Rod Dixon 氏（署名に J.D., LL.M.）は同意の表示が無いことを理由に条項を争いやすいと述べ、2015 年に Lawrence Rosen 氏は *"Indeed, some courts will NOT enforce a license that has NOT been seen and approved by the licensee."* と書いた（`review-readings.md` §1.180・§1.190、`against.md` #321）。**免責は受け入れを要らない形で書かれていて、効き方は法域による** —— これがこの問いへの正確な答えである。**逆側**: GPL をはじめ同意を求めない承認済みライセンスも保証を否認しており、ACD だけの問題ではない。受け入れの手順を求めることは OSD 10 が退けている。

**利用者にとっての実務的な帰結は 1 つだけ。** 無保証条項がどこまで効くかに関わらず、
**この作品は無保証で提供されている**。重要な用途に使うなら、自分で検証する。それは
ライセンスの文言ではなく、他人が書いたものを使うこと自体の性質である。

**逆に、Dedicator にとっての帰結。** 一部の法域で免責が制限されても、§14.2 により条項全体が
倒れるのではなく、その責任だけが法の認める範囲に戻る。これは §15 の可分性（severability）と
同じ考え方で、**一部が効かない法域でも instrument 全体は生き残る**ように組んである。

### A25. 研究・教育で使いたい。引用は要るのか、論文やデータセットに含めてよいか

**ライセンス上は何も要らない。ただし学術の作法は別の体系である。** ここを混ぜると誤る。

| したいこと | ライセンス上 | 補足 |
|---|---|---|
| 論文中で引用・図示する | 許諾不要 | 引用の可否を判断するのに許可を取る必要がない |
| 学習用データセットに含める | **明示的に許諾**（§6） | TDM の留保をしておらず、機械学習を積極的に許している |
| 授業教材として配る・改変する | 許諾不要 | 教育目的かどうかで扱いが変わることはない（用途制限が無いため） |
| 成果物（モデル・論文・派生コード）に条件が及ぶか | **及ばない**（§6.4） | 出力が本作品の許諾に縛られない |
| 出典を書く | **義務ではない**（§10.2） | 歓迎はする。書くなら canonical URL と `SPDX-License-Identifier: ACD-1.4`（適用された版の番号） |

**「帰属不要」は「引用しなくてよい」を意味しない。** 引用の要否を決めるのは著作権法や
ライセンスではなく、**所属機関と学術分野の規範**である。出典を示さずに他人の成果を自分の
ものとして提示すれば、ライセンスに違反していなくても剽窃（plagiarism）になりうる。
ACD は前者を放棄しているだけで、後者には触れていないし、触れられない。

**逆に、ライセンスが放棄していない唯一のこと**も述べておく。§11.3 は「私が書いた」「私が
推奨している」という**虚偽の表示**を禁じるが、これはライセンスが課した条件ではなく、
虚偽表示がそれ自体として成立するという確認である（§11.3 *"This Dedication does not make a false statement true."*）。ACD が何を許諾しようと独立に成り立つ。

**再現性のために**: この作品を研究対象にするなら、参照すべきは特定のコミットである。
リポジトリは全履歴が公開されており、`LICENSES/FROZEN.md` の存在と Check 453 が
**`FREEZE-DATA` に列挙された凍結ファイルすべての sha256 を pin している**ので、「いつ時点のテキストを見たか」は
機械的に確定できる。主張を信じる必要がなく、確かめられる形にしてあるのは他の面と同じ。

### A26. 権利者が複数いる作品（共同著作物・多数の貢献者）に適用できるか

**適用できるが、届くのは適用した人が持つ権利までである。** §2.7 が明示している ——
「この Dedication は Dedicator が保有する権利にのみ及ぶ。作品が他人の権利のある素材を
取り込んでいる場合、この Dedication はその権利に影響せず、影響させようともせず、その素材が
負担を負っていないという表明でもない」。§13.2 が対応する無保証を述べる。

**適用する側の実務。** §1.4 の Dedicator は「この Dedication を適用する各人または各主体」
なので、**複数人がそれぞれ適用できる**。§1.4 は、Dedicator が複数いるとき各人について別々に働き、1 人の適用が効かなくても他の人の適用に影響しないと述べる。多人数の作品で全体を自由にしたいなら、
**権利者全員が適用する**必要がある。一部だけが適用した状態は「その人の持ち分については
自由」という中途半端な状態で、受領者から見ると使えるかどうかが判断できない。

**受け取る側が確かめること。** リポジトリが「全貢献者が適用している」と述べているか、
述べていないなら誰が適用したのかを見る。ACD はそれを保証しない —— **保証しないことを
§2.7 と §13.2 で正面から書いている**のであって、書き忘れているのではない。

**法域による差がある（結論は書かない）。** 日本の著作権法 65 条は共同著作物の権利行使に
共有者全員の合意を求める。ドイツのように共同著作の持分処分に制約を置く法域もある。
つまり「1 人が単独で全体を献呈できるか」は法域ごとの問いで、ここでは答えない
（`ACD-1.0.jurisdictions.md` が結論ではなく問いを置いているのと同じ姿勢）。

**このリポジトリの場合は単純である。** 実装コードはすべて AI が生成し、人間はコードを
1 行も書いていない。外部からの pull request は受け入れておらず、取り込まれた第三者の
著作物は存在しない（A23 と同じ事実）。したがって権利者は 1 人で、上の複雑さはここでは
発生しない —— **他所で適用する人には発生しうる**ので、この節がある。

### A27. 適用した人が亡くなったら／会社が売却・破産したら、受け取った許諾はどうなるか

**変わらない。そう書いてある。** §2.8 は *"This Dedication, in respect of the Work, binds"* と、Dedication 全体で **Dedicator の承継人・譲受人・相続人・遺言執行者**、および Covered Right や §8 が届く特許請求項の移転先を、法の許す最大限まで拘束すると述べる。移転先は *"takes subject to it to that extent, Section 6 included"* —— Reservation（学習の opt-out）を置いて取り戻すこともできない。§15.5 は *"person"* が法人を含むと定めるので、会社が売却されて権利を受け取る法人も移転先である。

*前の版*: 1.0〜1.3 の §2.8 は拘束する条を §3・§4・§6・§8 と列挙し、§7.2（データベースの抽出の許可）と §2.5（禁反言）を名指していなかった（errata E46・E49）。*person* が法人を含む規定も無かった（errata E58）。1.4 は列挙をやめ、§15.5 を足した。

**破産・管財人。** §2.9 は、この Dedication のどれも、その条項の上で倒産手続や管財人の行為を条件にせず、それによって止まりも戻りもしないと述べ、管財人を §2.8 の移転先とする。未履行双務契約に当たるかは法廷地の倒産法が決め、本文は決めない（1.0 の §2.9 は *"fully performed"*・*"and so is not executory"* と分類まで言い切っていたが、欠陥として外した・errata E5・E30）。どちらの側にも継続的な
義務を残さない構造は、管財人が「履行を拒絶してライセンスを終わらせる」筋道に乗りにくくする
ことを狙っている。米国では 2019 年の最高裁判決（*Mission Product Holdings v. Tempnology*）が、倒産での
拒絶は解除ではなく違反として働き、すでに与えた権利を消さないと判示したので、問いは狭まった
（`ACD-1.0.jurisdictions.md` §5）。米国の外については、**それで足りるかは我々には判断できず、法律家の確認は無い**
（`QUESTIONS-FOR-COUNSEL.md` 問 8・米国倒産法 §365(n) の保護が国をまたぐ事件で衡量に
なった *Jaffé v. Samsung* を含む）。

**それでも残る限界を書く。** 人格権（§12）は法域によって**相続され、放棄も譲渡もできない**
とされる。フランスのように人格権が強い法域では、相続人が氏名表示や同一性保持を主張する
可能性そのものは条文で消せない。§12 は放棄可能な法域では放棄し、不可能な法域では
**本作品に限定した不行使の合意**という二段構えを取るが、**それが相続人に対してどこまで効くか
は法域ごとの問い**である。ここでは答えない（`ACD-1.0.jurisdictions.md` の姿勢と同じ）。

**受け取る側にとっての実務的な帰結。** 権利者が変わったからといって、既に受け取った permission
を確かめ直す必要はない。確かめる意味があるのは「そもそも適用時点で Dedicator がその権利を
持っていたか」で、それは §2.7（保有する権利にのみ及ぶ）と §13.2（無保証）の話であり、
承継とは別の論点である。

### A28. 個人データを含む作品に適用したい／そういう作品を学習に使いたい。何を確かめればよいか

**このライセンスは、その問いに答えられない。答えられないことを条文が明示している。**
§11.4 は、Work が個人データや人の肖像・音声・実演を含む場合、「それらの法が要求する許諾は
Dedicator が与えうるものではなく、本 Dedication はそれを与えようともしない」と述べる。
§11.4 は他人（Dedicator 以外の人）について言う。Dedicator 本人のデータでも、データ保護法上の同意は撤回できるので、このライセンスが処理の根拠にならないことは変わらない。Dedicator 本人の privacy・publicity・personality の権利は、Dedicator が §5.2(d) で許された利用に対して主張しない（虚偽の表示を除く）。

*前の版*: 1.0 の §11.4 は本人が写っている場合も「与えられない」と言い、言い過ぎだった（errata E43・1.4 で他人に限った）。本人の人格的な権利を主張しない約束（§5.2(d)）は 1.2 から（errata E31）。

**したがって、確かめるべきことは 2 段に分かれる。**

| 段 | 何を確かめるか | どこで答えが出るか |
|---|---|---|
| **1 段目: 適用者の権利** | Dedicator が持つ著作権・DB 権・特許について、学習を含む一切の利用が自由か | **本ライセンスで完結する**（§6.1 / §6.4 / §8.4）。追加の確認は要らない |
| **2 段目: 第三者の権利** | 個人データ・肖像・音声・実演について、必要な法的根拠があるか | **本ライセンスの外**。GDPR や各国法、契約、同意の有無で決まる |

**なぜ 2 段目を引き受けないのか。** 引き受けられないからである。データ保護法上の適法性は
**処理する側の目的と根拠**で決まり、素材の提供者が事前に付与できる性質のものではない
（GDPR の下では法的根拠は管理者が自ら特定する）。**「学習してよい」と書いてある素材が、
その処理を適法にすることはない。** これを曖昧にする instrument は、利用者に**実際には
存在しない安心**を与えることになる。

**適用する側への実務的な帰結。** 個人データを含む作品に ACD を適用するのは自由だが、
**それによって受領者の処理が適法になるわけではない**。適用者にできる有用なことは、
ライセンスの文言を強めることではなく、**素材の性質を記述すること** —— どのような
データが含まれるか、どこから来たか、どのような同意や法的根拠のもとで集めたか。
それは本ライセンスが要求する義務ではない（§10.1 は何も要求しない）が、
**受領者が 2 段目を評価するために必要な唯一の材料**である。

**使う側への実務的な帰結。** 1 段目は本ライセンスを読めば済み、**2 段目は誰が何と言おうと
自分で評価する必要がある**。§13.2 が「使用が他者の権利を侵害しないことを保証しない」と
明示するのは、この境界を曖昧にしないためである。

**この節が言っていないこと。** 個人データを含む作品を学習に使ってよいかどうか。それは
法域と目的と根拠によって決まり、**ライセンスの読み方では決まらない**。

### A29. 作品に第三者が付けた「学習禁止」シグナルは、このライセンスで無効になるのか

**ならない。§6.3 が「撤回する」と書いているのは、Dedicator が撤回できる Reservation についてだけである。**

条文は 2 つの作用を持ち、**効く範囲が違う。**

| 作用 | 誰の Reservation に効くか |
|---|---|
| **撤回（withdraw）** | **Dedicator が撤回する権限を持つものだけ。** 例: 配布者として自分で付けた metadata、hosting 側の既定 robots directive のうち自分で外せるもの |
| **依拠しない宣言（disclaim reliance）** | **誰が付けたものについても成り立つ。** Dedicator は「その signal を根拠に権利主張しない」と述べているだけで、他人の権利には触れていない |

**したがって、第三者が自分の権利の行使として付けた Reservation に、ACD は触れない**（それが法の上で有効かは、その権利者と法域の法が決める）。
§6.2 の末文が *"does not purport to defeat a Reservation made by another rightsholder"* と述べ、
§2.7 が instrument 全体を「Dedicator が持つ権利」に縛っている。**届かない撤回は、届かない。**

§6.3 自身も、他の権利者が自分の権利の行使として置いた Reservation については *"the Dedicator has no power to withdraw it and Section 6.3 does not purport to give one"* と述べる。

*前の版*: 1.0 ではこの答えが 3 条（§2.7 → §6.2 → §6.3）に分かれ、1 条だけ読んだ人には「他人の signal まで剥がす」と読めた。§6.3 の「撤回する力が無い」の文は 1.1 から（`ACD-1.1-CHANGELIST.md` §1・2026-09-14）。

**利用者にとっての実務的な帰結**: **ACD の作品を学習に使う前に、第三者の Reservation が
付いていないかは自分で確かめる必要がある。** このライセンスはそれを肩代わりしない ——
§13.2（無保証）と §2.7（保有する権利にのみ及ぶ）が、その限界を条文で述べている。

### A30. 適用した本人が、同じ作品を別のライセンス（GPL・商用ライセンス等）でも配ってよいか

**配ってよい。ただし、その別ライセンスは ACD を狭めない。** 本人（Dedicator）も、作品を
受け取って配る側としては「You」に当たり、§4.5 により好きな条件で頒布できる。一方 §2.2 は、
Dedicator が既に公開した写しについて「さらなる条件・制限を課すこと」を禁じ、§5.2(b) は
契約・利用規約・クリックスルー等の付随手段で、ACD が課さない義務を Work に課すことを禁じる。

**両者は次のように噛み合う。**

| 配るもの | 本人が付けた別ライセンスの効き方 |
|---|---|
| **ACD を適用した Work そのもの** | **受領者は ACD の下でも使える。** 別ライセンスの条件は、本人の権利によって Work を縛ることができない（§2.2 / §5.2(b)） |
| **本人が新たに書き足した部分**（ACD を適用していないもの） | **別ライセンスがそのまま効く。** その部分は「Work」ではない（§1.3 は Work を「Dedicator が適用した素材」と定義する） |

**つまり二重頒布（dual distribution）は普通にできるが、商用ライセンスを買わせて ACD 部分の
利用を制限することはできない。** 有償で売れるのは、ACD を適用していない付加部分・保守・
保証・サポートである。§5.1 と §5.2(b) は *"a payment You agreed to make for providing a copy or for a service that is not permission to use the Work"* を除く —— 写しや保守・サポートの代金は取れるが、許しそのものを「サービス」と名づけた代金は取れない。

*前の版*: 1.2 と 1.3 の §5.1 第 2 肢は、この代金の請求まで主張しないと読める語だった。1.4 草案は *"a payment You agreed to make"* を例外に足し、T118 でそれを写しとサービスの代金に限って §5.2(b) にも置いた。

**⚠ この答えの大半は §4.5 の中には書かれていない**（§4.5 の末文が「§5 が禁じることを Dedicator である素材に課せない」と述べるほかは、§2.2・§5.2(b)・§1.3 に分かれている）。
2026-11-01 に外部の敵対的レビューがこの読みを問い（`ACD-1.0.against.md` #279）、
次版の草案に相互参照を足すことも検討したが、**答えは本文全体で既に出ており、足す語は
長さ（register B3）に対する費用になる**ので、本文は変えずにこの FAQ で答えることにした
（`ACD-1.4-CHANGELIST.md`「外部の AI による敵対的レビューを当てた結果（2026-11-01）」節）。
**審査者が同じ問いを立てうることは変わらない** —— 1 条だけ読む読者のために、ここに書く。

### A31. モデルの重みを営業秘密として守ってきた。ACD を付けて公開すると、営業秘密はどうなるのか

**ACD は営業秘密を名指して許諾していない。ただし受け手に営業秘密を主張しない約束は届く。そして公開した時点で、秘密は事実として失われる。**

- **許諾の面**: §1.5 の Covered Rights は著作権・実演・放送・データベース権・不正な抽出に対する権利と
  「同様の効果を持つ権利」を挙げ、**営業秘密を名指していない**。それが「同様の効果を持つ権利」に
  含まれるかは本文が決めておらず、法域による（`ACD-1.0.against.md` #31・OpenMDW は明示的に含める）。
  §11.4 は、ACD が及ぶのは Covered Rights・§8 の特許・§12 の人格権だと述べ、同じ文で *"save that the covenants in
  Section 5 are promises about the Dedicator's own conduct and are not limited by this sentence"* と §5 の約束を外す
  （2026-11-27 訂正: この行は後半を落とし「だけ」と書いていた）。**§1.5 の第 1 文は開いた類である**:
  *"every right that the Dedicator holds or may come to hold in the Work … however arising, including …"* で、
  列は例示なので、営業秘密が第 1 文の内と読む側も立つ（`ACD-1.5-UNIQUE-READING.md` の §1.6 第 1 文の行・
  1.5 草案でも同じ）。
- **約束の面（有利）**: §5.1 第 2 文 *"any claim or cause of action, whether now known or unknown, that treats as
  wrongful, or as without legal basis, a use of the Work that this Dedication permits or purports to permit"* は、
  受け手の使用を営業秘密の不正使用とする Dedicator の請求にも届く（列挙された例外 —— 特許・商標と名・虚偽の言明・
  合意した支払い —— のどれでもない）。この一般の約束は 1.2 から在り、1.0・1.1 には無い。**逆側**: 約束は許諾でない
  （Chestek 氏 2024-10-05 は別の草案に「営業秘密の権利を与えない」ことを OSD の問題と書いた・`against.md` #31）。
  Dedicator が第三者（秘密を盗んだ人・元の雇用者）に持つ権利は残る。営業秘密が第 1 文の内と読まれると、
  §3 の放棄が第三者への権利まで手放したと読まれる危険もある。
- **事実の面**: 営業秘密の保護は秘密であることに依存するので、重みを誰でも取得できる形で公開すれば、
  **許諾の有無にかかわらず**秘密としての保護は残らない。ACD を付けても付けなくても同じである。

**したがって「ACD を付けたから営業秘密を手放した」でも「営業秘密は ACD の外だから守られている」でもない。**
守りたい秘密があるなら、公開しないことだけが手段である。逆に、第三者の営業秘密を含むデータで
学習したモデルを公開する場合、その第三者に対する責任（契約・不正競争）は ACD の外に残る（§2.7 / §13.2）。

2026-11-01 の外部監査（`ACD-1.4-ADVERSARIAL-TRIAGE.md` の J-18・B-06）が、「AI 完全フリー」という
見え方がこの境界を隠すと指摘したので、使う側の問いとしてここに置いた。

### A32. 特許を持っている。その方法を説明した文書に ACD を付けてよいか

**付けてよいが、その方法の特許を手放すことに近い。** ACD-1.4 の §8.4 は、Work が教える特徴について、学習から生じたモデルと出力に特許許諾を及ぼす。

- **何が起きるか**: 誰かがあなたの文書でモデルを学習し、そのモデルが方法を実施するコードを出力すれば、その出力についてあなたの請求項は許諾されている。文書そのものは方法を実施しないので §8.1 は発火しないが、§8.4 は発火する。**小さなモデルを経由するだけで足りる。**
- **止められるか**: 止められない。§8.2 は条件も終了も置かないので、許諾の範囲を後から狭めることも、特許訴訟で報復することもできない。
- **どうすればよいか**: その方法の特許を保ちたいなら、説明文書に ACD を付けない。**特許を持つ組織が文書に適用する前に確かめるべき最大の点である**（`against.md` #16 / #282・register B7）。
- **版**: 1.0 の §8.4 は因果の限定を持たず、もっと広い。1.1〜1.3 は読みが割れている（#282）。

**これは法律の助言ではない。** 法的レビューは受けていない。

### A33. ACD のファイルのタグを残したまま手を入れた。自分の改変分まで ACD になるのか

> **English:** Keeping a tag that was already there is not applying the Dedication, on our reading.
> Section 16.1 speaks of placing a notice in order to apply it, and Section 1.4 (1.0: Section 1.3)
> makes a Dedicator of the person applying it. You are free to keep or remove the tag (Section 10.2).
> If your changes are under other terms, say so next to the tag. No court has tested this.

**なぜ問うか**: §3 は取り消せず §8 は終了しないので、誤って成立したときの費用が他のライセンスより重い。SPDX のタグは REUSE などの道具が既定で残すので、起きやすい。ACD-1.4 からタグだけでも適用になるので（§16.1・`ACD-1.1-SELF-AUDIT.md` §3v）、この線がタグにも引かれる。

- **読みの根拠**: §16.1 は *"To apply this Dedication, place a notice"* で、目的の語と「置く」行為の語を持つ。残すことはどちらにも当たらない。
- **どうすればよいか**: 改変分を別の条件で出すなら、タグの隣にそう書く。書かないと次の読み手には区別できない。
- **⚠ 逆側**: これは読みであって判決ではない。残したまま配ったことを適用の表示と見る余地はある。
- **本文の外の話**: 改変者の表示に依拠した受領者の主張（黙示の許諾や estoppel）は ACD の外の一般法の問題である。§2.5 は Dedicator 本人の行為にしか掛からない。

**これは法律の助言ではない。** 法的レビューは受けていない。

### A34. 自分の作品の一部（例: `corpus/`）だけは学習に使わせたくない。opt-out の通知を置けば ACD から外れるか

> **English (ACD-1.4):** No. To keep material out of the Dedication, assign it to other terms: a notice that names another licence, or that reserves all rights. A notice that only reserves text and data mining or training (an Article 4(3) DSM opt-out, a robots or "noai" signal) assigns nothing to other terms (Section 16.2), and Section 6.2 does not read it as a Reservation. Material already released under the Dedication cannot be taken back (Section 2.2).

**外れない。素材を ACD から外すには、その素材を別の条件へ割り当てる。DSM 指令 4 条 3 項の opt-out だけでは外れない。** この答えは **確定した ACD-1.4 の文**についてのもの（2026-11-23 に凍結した本文で引用を確かめた）（§16.2 の第 3 文と、2026-11-10 に足した *"a notice that is only a Reservation assigns nothing to other terms (Section 6.2)"*・`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.24 の T52）。

- **外す方法**: その素材の隣に、別のライセンスを名指す通知か、すべての権利を留保する表示を置く（§16.2 の「狭い通知」）。学習だけを禁じたいなら、そのための別の条件を書いた通知が要る。
- **外れない通知**: TDM や学習の留保だけを述べる通知、robots の指示、"noai" の meta、ホスティングが既定で付ける信号。どれも「他の条件への割り当て」ではなく、§6.2 はそれを Reservation として読まない。§6.3 は Dedicator 自身が後から置いた Reservation も撤回する。
- **なぜこう決めたか**: 留保だけの通知で素材が外れると読めると、サイト全体に置いた robots の AI 拒否まで「狭い通知」になり、§6 の約束が通知 1 つで外れる。自動化システムが判定できない許可は許可でない、という §6.5 の理由にも反する。
- **1.0 では**: 1.0 には「狭い通知」の文が無い。ACD-1.0 の通知が `corpus/` を含む素材に付いていれば、`corpus/` は Work で、そこに置いた opt-out は §6.2 により Reservation と読まれず、§6.3 により撤回される。通知の範囲を `corpus/` の外に限っても、§1.2 の *"in whole or in part"* により素材全体が Work と読まれうる（errata E61・1.4 草案で外した）。1.0 で `corpus/` を確実に外すには、範囲を限るだけでなく、`corpus/` が別の条件に属することを明示する（他のライセンスを名指すか、すべての権利の留保を置く）。E61 自体は害が確実だとは言っていない（*"to which"* と表示の範囲は逆を指す）ので、ここも「読まれうる」に留める（portfolio-aa の指摘で 2026-11-10 に足した）。
- **⚠ 逆側**: opt-out だけで外れると思って置いた Dedicator には、学習への献呈が取り消せない形で起きる（§2.2）。EU の Dedicator は opt-out を「外す標準の手段」と考えがちなので、この罠は現実にありうる。この項はその緩和のために置いている。
- **一度出した素材は戻らない**: 後から別の条件の通知を置いても、既に ACD で出した素材は戻らない（§2.2）。受領者からは、どちらの通知が先かが見えにくいことがある。

**これは法律の助言ではない。** 法的レビューは受けていない。

## B. プロセスの疑問

### B1. いまどの段階か

`LICENSES/FROZEN.md` の `VENUE-DATA` marker が**単一ソース**である（Check 458 が 5 ファイルとの整合を BLOCKING で強制）。**ACD-1.0 を OSI `license-discuss`（一般的な議論リスト）へ投稿した**ところまでで、承認申請の窓口である `license-review` へも、SPDX へも出していない。**承認の手続きはまだ何も始まっていない。**

- **出す版**: 2026-11-23 の合議（議題 3）で、提出対象を確定した **ACD-1.4** に切り替えた（`ACD-1.0.submission.md` の `SUBMISSION-TARGET`）。ただし 1.4 の新しい語をオーナーが `license-discuss` へ自分の言葉で出し、少なくとも 30 日置くまで、提出の門は開かない。
- **このリポジトリが適用しているのも ACD-1.4**（root の `LICENSE`）。1.1〜1.4 はどれも確定・凍結した版で、どれも承認されていない。
- **「反応待ち」は「届いている」を意味しない。** 我々の投稿のうち**少なくとも 3 通**が moderation で拒否され、リストに届いていない（`ACD-1.0.against.md` #215・発信状態の単一ソースは `FROZEN.md` の `POSTING-STATUS`）。

### B2. OSI が却下したら / 反応が無かったら

**却下は結果であって失敗ではない。** 想定問答 meta 分冊 Q20 に**撤回すべき条件を事前に**
書いてある（既存 1 本で 3 つの gap が埋まると示された / dedication 形式を扱わないと述べられた /
§4 が独立の許諾として機能しないと指摘され反論できなかった / 実使用 1 件では対象外と述べられた）。

**反応が無かった場合も事実として記録する** —— `ACD-1.0.discussion-log.md` が空のままなら
「スレッドは反応を得られなかった」と書くのが正しく、起きなかった議論を匂わせるより良い。
**ただし「反応が無かった」と「届かなかった」は別の事実である**（2026-09-27 追記）—— moderation で拒否された
投稿について「反応を得られなかった」と書くと、リストが読んで黙ったかのように読める。拒否が分かっている投稿は
**拒否された**と書き、届いたか分からない投稿は**分からない**と書く（アーカイブを取得できなかった日も同じ）。

### B3. SPDX にはいつ出すのか

**実使用が増えてから。** SPDX は「相当程度の実使用」を求めるが、現在の使用実績は本リポジトリ
1 件である。**満たしていないものを出さない**という判断であって、順序の都合ではない。

### B4. 次の版はいつ作るのか

**直すべき欠陥が記録されたとき、次版の草案で直す。確定した版は直さない。** 版を確定するたびに本文を凍結し（`FROZEN.md`・Check 453 が sha256 で pin する）、見つけた欠陥は `ACD-1.0.errata.md`（1.0 にも在る文）か `ACD-1.1-SELF-AUDIT.md`（後の版が持ち込んだ文）に記録して、次版の草案で直す。いまの作業場は `LICENSES/README.md` の「次版の草案」行が名指す（版が動くたびにここが古くならないように、ここには書かない）。審査中に審査側が見ているテキストを差し替えないためである。

**いま ACD-1.4 を適用してよいか**: **よい。** §16.2 により、識別子か名前と版で参照していれば本文の写しが付いていなくても terms は完全に適用される。次の版が確定しても**あなたの notice は壊れない** —— §16.4 は各名と識別子が 1 つの固定テキストを指し続けるようにし、新しい版は新しい識別子を持つ。**移りたければ notice の識別子を変えるだけでよく、移らない自由もある**（ただし既に出した素材は §2.2 により戻らない）。

**後から静かにパッチを当てられない**のは意図的な cost である（想定問答 boilerplate 分冊 Q32）。**§16.4 は改変そのものを禁じてもいない** —— 別の名前でなら頒布してよい。

*前の版*: 1.0 の §16.4 は `ACD-1.0` しか名指さず、第三者が改変版を `ACD-1.1` の名で頒布することを 1.0 の文言は止めなかった（errata E14・1.1 で閉じた）。1.4 は「`ACD-` に数字が続く識別子」全体と Steward（§16.5）へ広げた。

### B5. 誰に連絡すればよいか

**何について連絡したいかで、相手が違う。**

| 連絡したいこと | 相手 |
|---|---|
| **ある作品**（その作品の権利・来歴・含まれる第三者素材） | **その作品の Dedicator（適用した人）**。このリポジトリの作品なら横井雄太、他の人が ACD を適用した作品ならその人である |
| **ライセンス本文そのもの**（誤り・次版・識別子） | **ライセンスの steward** —— `ACD-1.0.submission.md` §A の *Licence steward* 行（横井雄太）。ACD-1.4 の §16.5 は *"the Steward"* を、その名前と識別子でこの本文を最初に公開した者、または役を譲られた者と定義している |

**⚠ 2026-11-01 訂正**: この節は「steward は Dedicator（適用者）本人」「§A に連絡先の欄がある」と
述べていたが、**2 つとも不正確だった**。steward と Dedicator は、このリポジトリでは同じ人だが
**一般には別人**であり（他の人が ACD を適用した作品について、本文の steward に尋ねても答えは無い）、
§A にあるのは steward の**名前**であって連絡先の欄ではない（個人の連絡先は公開リポジトリに置かない）。

**どちらにも義務は無い。** §13.3 のとおり Dedicator は保守・更新・修正・サポート・防御の義務を負わず、
§10.4 により**終了規定が無い**ので、利用者が誰かの行動を必要とする場面は無い。

---

## C. リポジトリのどこを見れば何が分かるか

| 知りたいこと | 見る場所 |
|---|---|
| **条文そのもの**（唯一の権威・このリポジトリが適用する版） | `LICENSES/ACD-1.4.txt`（`license-discuss` へ投稿した版は `LICENSES/ACD-1.0.txt`） |
| 条項ごとの意図 | `LICENSES/ACD-1.4.clause-reference.md`（80 条）/ `LICENSES/ACD-1.0.clause-reference.md`（1.0 の 82 条） |
| 「X で足りるのでは」への答え | `LICENSES/ACD-1.0.comparison.md` / `docs/architecture/acd-license-rationale.md` §2 |
| 法域ごとの問い | `LICENSES/ACD-1.0.jurisdictions.md` |
| レビューで来るであろう指摘 | `LICENSES/ACD-1.0.review-responses.md`（+ `-clauses` / `-meta`） |
| **実際に来た指摘** | `LICENSES/ACD-1.0.discussion-log.md` |
| 使う側の実務 | **本書** |
| 設計根拠と申請ドシエ | `docs/architecture/acd-license-rationale.md` |
| 提出パケット（英文・**送る版は §B.0 の確定手順を経る**。何を・いつ送るかは AI が決め、送る行為と文面の語はオーナー） | `LICENSES/ACD-1.0.submission.md` |
| 提出判断と**残る弱点** | `LICENSES/READY-TO-SUBMIT.md` |
| 凍結の状態と投稿先の単一ソース | `LICENSES/FROZEN.md` |
| 確定・凍結済みの後継版（未提出・未適用） | `LICENSES/ACD-1.1.txt` |
| 確定・凍結済みの後継版 1.2（2026-10-17・未提出・未適用） | `LICENSES/ACD-1.2.txt` / `LICENSES/ACD-1.2-CHANGELIST.md` |
| 確定・凍結済みの後継版 1.3（2026-10-25・未提出・2026-11-23 まで適用） | `LICENSES/ACD-1.3.txt` / `LICENSES/ACD-1.3-CHANGELIST.md` |
| 確定・凍結済みの後継版 1.4（2026-11-23・未提出・このリポジトリに適用中） | `LICENSES/ACD-1.4.txt` / `LICENSES/ACD-1.4-CHANGELIST.md` |
| 次版の草案（作業場・版が動いたら `LICENSES/README.md` の「次版の草案」行が権威） | `LICENSES/ACD-1.5-DRAFT.txt` / `LICENSES/ACD-1.5-CHANGELIST.md` |
| 機械可読な記述子 | `LICENSES/ACD-1.4.machine.json` / `LICENSES/ACD-1.4.spdx.xml`（1.0 の版は `ACD-1.0.machine.json` / `ACD-1.0.spdx.xml`） |

**ここに無い疑問が出たら、それはこの一覧の欠落である。** 追記すること。

---

**Lost?** [`QUESTION-INDEX.md`](QUESTION-INDEX.md) indexes every worked entry in this directory by
the question it answers. [`AS-OF.md`](AS-OF.md) lists which claims about the outside world were
verified when. [`ACD-1.0.against.md`](ACD-1.0.against.md) is the case against approving this.
