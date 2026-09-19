---
file: LICENSES/ACD-1.0.jurisdictions.md
audience: ai, human (提出者), 監査人, 採用検討者, 学術研究者, 第三者全般
last-updated: 2026-09-05
canonical-ref: LICENSES/ACD-1.0.txt (凍結中の本文・唯一の権威) / LICENSES/ACD-1.0.clause-reference.md (逐条リファレンス) / LICENSES/ACD-1.0.review-responses-clauses.md (§31 に日本法の論点)
---

# ACD-1.0 — 法域別に「どこが問いになるか」

```
本書の性質 : **答えではなく、問いの所在と本文の手当ての地図**である
            弁護士の確認を経ていない (READY-TO-SUBMIT.md「残る弱点」1)
書き方     : 各法域について「問い」「本文の手当て (条番号)」「確立していないこと」の 3 段
禁じ手     : **断定しない。** 助言を得ていない領域で法理を断定するのは、
            review-responses-meta.md Q10 が警告する
            「confidently invented doctrine」の実演にほかならない
```

## 0. なぜこの文書があるのか

「あなたの国では効くかもしれないが、うちの国では効かないのでは」は、公有化型の instrument に
**必ず**向けられる。そのとき有効なのは、法理を語ることではなく **「その問いは認識していて、
本文のここで手当てしてある」と条番号で示すこと**である。

**手当てがあることと、それが有効であることは別**である。本書は前者しか主張しない。

## 1. 全法域に共通する構造（これが答えの土台）

どの法域の話であっても、答えの骨格は同じである。

| 層 | 条項 | 効かなかったときに何が残るか |
|---|---|---|
| 放棄（public domain 化）| §3.1 / §3.2 | §3.3（waiver として扱う）→ それも駄目なら §15.4 で**その法域に限り**切り離す |
| ライセンス | §4.1〜§4.3 | **§3 の成否に依存しない**（§4.4）。通常のライセンス法理で立つ |
| 不行使の約束 | §5.1〜§5.3 | 契約・禁反言の一般法理。承継人にも及ぶ（§5.3）|
| 特許 | §8.1 / §8.4 | ライセンスが無効なら §8.6 が**同じ範囲の不行使の約束**へ切り替わる |
| 人格権 | §12.1 | 放棄不能なら §12.2 が**不行使の約束**へ切り替わる |

**§2.4 が「§3・§4・§5・§6 は互いに独立」と定めているのが要**である。段階的なフォールバック
（まず §3、駄目なら §4）ではないので、**利用者はどの層が効いているかを判定しなくてよい**
（§4.4 が明示）。

> **English (use when asked "does this work in my country?"):**
>
> The honest answer is that I do not know how each jurisdiction will treat Section 3, and the
> instrument is built so that You do not have to know either. Sections 3, 4, 5 and 6 are
> independent (Section 2.4); Section 4 is granted without waiting for Section 3 to fail
> (Section 4.4); Section 5 is a covenant that survives an attack on either; Section 15.4
> severs a failed provision **as to that jurisdiction only**. So the question "is abandonment
> effective here?" changes which layer is doing the work, not whether You may use the Work.

---

## 2. 日本（**Dedicator（適用者）の所在地**・必ず問われる）

**問い**: 著作権を放棄できるのか。人格権は放棄できるのか。

**本文の手当て**: §3.3（放棄が不可でも waiver として扱う）/ §4.4（§3 に依存しないライセンス）/
§12.1（可能な範囲で放棄）→ §12.2（不能なら不行使の約束）/ §12.3（**この Work に限定**）/
§12.4（承継人）。

**確立していないこと**: 著作権法は放棄の手続を定めておらず、放棄の可否は条文上明らかではない。
人格権については 59 条が一身専属と定めており、放棄は認められないとするのが一般的な理解である。
**§12.2 の不行使特約が、どこまでの範囲で・誰に対して効くかは、助言を得ていない。**
`review-responses-clauses.md` §31 に詳しい姿勢を書いてある。

**なぜ §12.3 が限定しているか**: 無制限の放棄より、**限定したほうが生き残る**という判断による。

### 2a. 30 条の 4 —— 例外は広い。だが**但書がある**（2026-09-19 に原典で確認）

**e-Gov の法令 API から取得した本文**（`345AC0000000048`）:

> **第三十条の四** 著作物は、次に掲げる場合その他の当該著作物に表現された思想又は感情を自ら
> 享受し又は他人に享受させることを目的としない場合には、その必要と認められる限度において、
> いずれの方法によるかを問わず、利用することができる。**ただし、当該著作物の種類及び用途並びに
> 当該利用の態様に照らし著作権者の利益を不当に害することとなる場合は、この限りでない。**
> …　二　**情報解析**（多数の著作物その他の大量の情報から、当該情報を構成する言語、音、影像
> その他の要素に係る情報を抽出し、比較、分類その他の解析を行うことをいう。）の用に供する場合

**日本の例外は非営利に限られない。** その意味で **§6 の追加価値は、EU や英国より小さく見える** ——
**そこまでは我々に不利な事実である**（`review-corpus.md` にも同趣旨が書いてある）。

**しかし但書がある。** 「著作権者の利益を不当に害する」かどうかは**当てはめの問題**で、
**学習用に販売されているデータセットのような事例をめぐって議論が続いている。**
**権利者本人の明示の許諾があれば、その当てはめを争う必要が無くなる。**

**つまり日本における §6 の価値は「例外が無いから要る」ではなく、
「例外はあるが条件付きで、その条件の当てはめを消せる」である。** ——**主張を弱い方へ言い直す。**

**⚠ 但書とは別に、*入口*の条件も当てはめである（2026-09-20 に外部レビューが指摘し、原典で確かめた）。**
30 条の 4 の本文は **「享受し又は他人に享受させることを目的としない場合」**に限って許す。
**享受目的が併存する利用**（学習と同時に鑑賞・提供の目的を持つ場合）や、
**学習データに類似する出力を意図的に得る利用**では、**そもそも入口の条件を満たさない**と
論じられうる ——**但書（「利益を不当に害する」）に進む前に落ちる経路がもう 1 本ある。**
**§6 の価値はここでも同じ形である** ——**権利者本人の明示の許諾は、この入口の当てはめも消す。**
**⚠ ただしこれは我々の読みではなく、条文の構造から言えることに限る** ——
**どの利用が「享受目的の併存」に当たるかの実務は、我々は測っていない。**

### 2b. 59 条と 60 条 —— §12.2 と §12.4 に、それぞれ対応する条文がある

> **第五十九条** 著作者人格権は、著作者の一身に専属し、譲渡することができない。
> **第六十条** 著作物を公衆に提供し、又は提示する者は、**その著作物の著作者が存しなくなつた後に
> おいても**、著作者が存しているとしたならばその著作者人格権の侵害となるべき行為をしてはならない。

**59 条は「譲渡できない」と述べる。** 放棄の可否は条文が直接答えておらず、
**実務は不行使特約（＝約束）で扱う** ——**これが §12.2 の形そのものである。**

**60 条は §12.4 の日本における referent である。** §12.4 は
*"any person entitled to exercise or enforce Moral Rights in the Work after the Dedicator's death"*
まで拘束すると述べており、**60 条（および 116 条の遺族による請求）が、まさにその「死後に行使しうる者」を
作っている。** **§12.4 は抽象的な用心ではなく、名前のある制度に対応している。**

---

## 3. ドイツ（公有化否定の代表例として必ず引かれる）

**問い**: 著作権は譲渡も放棄もできないのではないか。作者が考えを変えたら取り戻せるのでは。

**本文の手当て**: §3.3 / §4.4（§3 が効かなくても**通常のライセンス**が残る）/ §2.2（撤回不能の
意思表明）/ §2.5（**信頼が目的であり、方式や約因の欠如を理由に無効を主張しない**＝禁反言）/
§15.4（その法域に限り切り離す）。

**確立していないこと**: 著作権の完全な放棄が認められないという理解は広く共有されているが、
**不行使の約束や撤回不能のライセンスがどこまで拘束するかは、助言を得ていない。**

**§15.4 を根拠に挙げるときの但し書き（2026-08-30 追記）**: §15.4 には機構が 2 つある ——
**①無効な条項を有効となる最小限に reform する**、②reform できなければ**その法域に限って
切り離す**。ドイツ法は標準約款について *geltungserhaltende Reduktion*（有効性を保つ縮減）を
一般に認めず、無効な条項は縮められるのではなく脱落する、と理解されている。つまり
**この法域では①が使えない可能性がある**。

ただし結論は変わらない。②の severance が残り、**§4.4 によりライセンスは §3 から独立**なので、
§3 がドイツで脱落しても **§4 は無傷で、利用者は通常の撤回不能・無償・無条件のライセンスを
持つ**。①が使えないことが効くのは「§3 を部分的にでも生かせるか」という場面に限られ、
利用者が持つものは変わらない。

**確立していないこと（追加）**: そもそも ACD-1.0 が標準約款（AGB）に当たるかが不明である ——
対価も交換もなく、相手方に条件を課す当事者もいない一方的な付与だからである。当たらなければ
Reduktion の制限もそのままには及ばない。**どちらであるかは助言を得ていない。**
本書の方針どおり、ここでは問いとして置く。

> **English:**
>
> In a system where copyright cannot be alienated and abandonment is generally regarded as
> ineffective, Section 3 does not achieve a surrender. Section 4 is unaffected — it does not
> wait for Section 3 to fail (Section 4.4) — so what the user has is an ordinary irrevocable,
> royalty-free, condition-free licence: the same thing a permissive licence would give them.
> Section 5 sits underneath as a covenant. Section 2.5 addresses the "no consideration, no
> formality" attack directly by stating that reliance is the purpose, not a side effect.

---

## 4. フランス（人格権が最も強い）

**問い**: 人格権は永久・不可譲・時効にかからないのではないか。

**本文の手当て**: §12.1 →（放棄不能なら）§12.2 の不行使の約束 / §12.3（Work 限定）/
§12.4（死後に行使しうる者まで）/ §12.5（**虚偽の帰属に対抗する利益は残す**）/ §12.6（可分）。

**確立していないこと**: 不行使の約束が人格権について有効かは争いがありうる。**§12.5 で
虚偽帰属への対抗利益を残しているのは、全部を捨てさせない設計だが、それで足りるかは
助言を得ていない。**

---

## 5. 米国

**問い**: 著作権法に放棄の手続が無いのに、public domain に置けるのか。倒産したらどうなるか。

**本文の手当て**: §4.4（ライセンスが独立）/ §2.5（禁反言）/ **§2.9（履行完了＝未履行双務契約では
ない）** / §2.8（管財人は「譲受人」に当たると明示）。

**§2.9 の位置づけ**: 未履行双務契約であれば管財人による解除の対象になりうるため、
**11 U.S.C. §365(n) のような保護規定に頼る構図**になる。§2.9 は「適用時点で履行が完了して
おり継続債務が無い」と述べることで、その構図に入らないことを主張する。

**確立していないこと**: **裁判所が実際に non-executory と認めるかは保証できない。**
§2.9 の文言はその主張であって、判断ではない。

### 5a. 法定の終了権（17 U.S.C. §203）—— 「irrevocable」は、米国の §4 については statute に負ける

**2026-09-19 に原典で確認した**（`https://www.law.cornell.edu/uscode/text/17/203`）。
条文はこう定める:

> *"the exclusive or nonexclusive **grant of a transfer or license** of copyright or of any right
> under a copyright, **executed by the author** … otherwise than by will, is subject to
> termination …"*（§203(a)）
> *"Termination of the grant may be effected **notwithstanding any agreement to the contrary** …"*（§203(a)(5)）

**帰結を隠さずに書く。** §4 は **licence** であり、**§203 はそれに届く。**
**§2.2 と §4.1 の *"irrevocable"* は、米国で著作者本人（またはその承継者）が 35 年後に行う
法定の終了を止められない** ——*"notwithstanding any agreement to the contrary"* がそう述べている。
**本文の語がどれほど強くても、この点では statute が勝つ。**

**本文の手当ては §15.2 である**（無効なら当該法域についてのみ改釈・可分）。
**つまり文書が「誤っている」のではなく、当該法域で当該条が縮む、という構造になっている。**

**そして、ここで三重構造が初めて冗長でなくなる。**

| 条 | §203 に対して |
| :-- | :-- |
| **§4（ライセンス）** | **届く。** 終了されうる |
| **§3（放棄・献呈）** | **§203 の語は *"transfer or license"* である。放棄はそのどちらでもない**（権利を移すのではなく消す）——**条文の文言上は届かない** |
| **§5（不主張の約束）** | **grant ではない。** §203(b) が復帰させるのは *"all rights … that were covered by the terminated grants"* であって covenant ではない |

**⚠ この表が establish しないこと**: **米国法上の著作権放棄は判例法の領域で、確立した手続が無い**
（この文書の §5 冒頭の問いがまさにそれ）。**「§3 は §203 に届かないから安全」ではなく、
「§3 が有効なら §203 の射程外にある」**である ——**二重の不確実性が直列につながっている。**
**§5 の生存も同様に未確定**で、*"agreement to the contrary"* と読まれれば同じ運命になりうる。

**言えるのはここまで**: **§3 / §4 / §5 が並置されていることは、§203 に対しては
「同じことを 3 回言っている」ではなく「効き方の違う 3 つを置いている」。**

### 5b. 人格権（17 U.S.C. §106A・VARA）—— §12.1 は米国では形式要件を満たさない。だから §12.2 がある

**2026-09-19 に原典で確認した**（`https://www.law.cornell.edu/uscode/text/17/106A`）:

> *"those rights may be waived if the author **expressly agrees to such waiver in a written
> instrument signed by the author**. Such instrument shall **specifically identify the work, and
> uses of that work**, to which the waiver applies …"*（§106A(e)(1)）

**§12.1 の放棄は、この形式を満たさない。** リポジトリに置かれた LICENSE file は
**著作者が署名した書面ではなく**、**用途を特定してもいない。**
**したがって米国では §12.1 は放棄として成立しないと考えるのが素直である。**

**それは設計どおりである** ——§12.2 が *"Where the law of a jurisdiction provides that Moral Rights
are … incapable of waiver, Section 12.1 does not apply … and instead the Dedicator covenants not
to exercise"* と述べており、**covenant には形式要件が無い。**

**⚠ ただし射程を誇張しない。** **VARA が及ぶのは *works of visual art* だけ**であり、その定義は
絵画・素描・版画・彫刻・展示目的の限定部数の写真に限られ、**映画その他の audiovisual work は
定義から明文で除かれている。** **ソフトウェアは対象外である。**
**したがって ACD の典型的な対象物について、VARA はそもそもほとんど発動しない** ——
**この節は「米国には人格権の問題がある」ではなく、「あるとしても §12.2 が受け止める形になっている」
ことを示すためにある。**

**⚠ そして §12.2 自体の有効性は別問題である。** 形式要件が無いことと、
**covenant が裁判所で執行されることは同じではない。** ここは外部の法律意見が要る（register B1）。

---

## 6. EU（TDM と DB 権）

**問い**: TDM の opt-out はどうなっているのか。データベース権は。

**本文の手当て**: §1.10（**Reservation の定義が DSM 指令 4 条 3 項を名指しする** ——
本文が引用する唯一の外部法令）/ §6.2（**留保しない**と明言）/ §6.3（他者の留保には触れない）/
§7.1（DB 権も Covered Right）/ §7.2（**extraction / re-utilisation** の語で反復的・体系的な
利用を許す）。

**なぜ §6.2 が要るのか**: 4 条 3 項の opt-out は「**留保したか**」で決まる。許諾の言明だけでは
「留保していない」ことの表明にならない —— **沈黙が意味を持つ領域**だからである。

**確立していないこと**: 機械可読な留保の様式やその解釈は各国実装・実務の形成途上である。
§1.10 は「機械可読な信号・プロトコル要素・ヘッダ」を広く含む書き方にしてあるが、**将来の
標準に自動的に追随するとは主張していない**。

---

### 6a. 放棄できない報酬請求権 —— §3.2 が名指しで surrender すると書いているもの（2026-09-19 に原典で確認）

**§3.2 は surrender の射程をこう述べる**: *"includes any right to **compensation, remuneration,
levy, or royalty** arising from any use of the Work."*
**EU にはそれを放棄できないと定める条文がある。**

**Directive 2006/115/EC（貸与権・公貸権）第 5 条「Unwaivable right to equitable remuneration」**:

> *"1. Where an author or performer has transferred or assigned his rental right concerning a
> **phonogram or an original or copy of a film** to a phonogram or film producer, that author or
> performer **shall retain the right to obtain an equitable remuneration for the rental**.
> 2. **The right to obtain an equitable remuneration for rental cannot be waived by authors or
> performers.**"*

**同第 6 条（公貸権）**: 加盟国は貸与の排他権を制限できるが *"**provided that at least authors
obtain a remuneration for such lending**"*。

### なぜ ACD に当たりうるのか

- **§1.3 の Work は *audiovisual material* を含む。** 映画や録音物へ適用されれば射程に入りうる。
- **§4.2 は *lend, rent* を明示的に許諾している。**
- **§3.2 は報酬請求権を surrender の対象として名指ししている。**

### それでも利用者の立場は変わらない —— 3 つの理由

1. **§3.2 は §3.1 の射程を述べる文であり、§3.1 は *"to the fullest extent permitted by the law of
   each jurisdiction"* を持つ。** 放棄できない法域では**その分だけ縮む。本文は不可能を主張していない。**
2. **報酬は多くの場合、利用者ではなく機器の製造者・輸入者や図書館制度から徴収機構を通じて支払われる。**
   **放棄できない報酬請求権が残っても、それは You に対する義務にならない。**
3. **第 5 条の要件は「producer への rental right の譲渡」**である。ACD は producer への譲渡ではなく
   万人への放棄・許諾なので、**そのまま当てはまるかは自明でない。**

### ⚠ それでも記録する理由

**§3.2 を単独で読むと絶対的に見える。** E19 / E21 で直したのと同じ形である ——
**ただし §3.2 は *"The surrender in Section 3.1 is made …"* と明示的に §3.1 へ錨を下ろしているので、
本掃引が定めた規則（錨がある条は clean）に従い、本文は変えない。**
**変えるのは、この事実が我々の側から先に述べられているかどうかである。**

**⚠ 確立しないこと**: 各国の実装は一様でない（ドイツは著作権法 27 条が貸与・公貸に報酬請求権を置くなど、
指令より踏み込む例がある）。**本書はどの国内法がどこまで及ぶかを判断しない。**
**私的複製の補償金は別の指令に由来するが、本書では原典を当てていないので触れない。**

---

## 7. 英国

**問い**: 人格権の扱いが他の欧州法域と違うのでは。**機械生成著作物に条文があるのでは**。

**本文の手当て**: §12.1（英国では放棄が可能とされているので §12.1 が直接働きうる）/
§9.1〜§9.3（**機械生成物の権利の存否を利用者の経路から外す**）。

**ここが英国固有で重要**: 英国著作権法は **computer-generated works** について明文を持つ
（著作者を「創作に必要な手配をした者」とする趣旨の規定）。つまり**他の多くの法域と違い、
権利が存在しうる**。§9.2 は「存在しなければ何も足さず何も奪わない／**存在すれば §3〜§8 と
§12 が全面適用される**」と両方向を書いてあるので、この違いで利用者の立場は変わらない。

**確立していないこと**: 当該規定の適用範囲・存続期間の扱い・生成 AI への当てはめは議論が
続いている。**本書はその議論に立ち入らない。**

### 7a. 原典（2026-09-19 に legislation.gov.uk で確認）

> **s.9(3)** *"In the case of a literary, dramatic, musical or artistic work which is
> **computer-generated**, the author shall be taken to be **the person by whom the arrangements
> necessary for the creation of the work are undertaken**."*
> **s.178** *"**computer-generated**, in relation to a work, means that the work is generated by
> computer in circumstances such that **there is no human author of the work**."*

**英国は「人間の著作者がいない」ことを前提にしたうえで、著作者を擬制する。**

### 7b. 同じ材料が、英国では権利を持ち、米国では持たない —— これが §9 の存在理由である

**米国著作権局は 2025 年の報告で、純粋な AI 生成物それ自体には人間の著作者性が無く
著作権適格が無いとの立場を示している**（`review-corpus.md`）。**英国は s.9(3) で著作者を擬制する。**

**つまり同一の機械生成材料が、一方の法域では権利の対象で、他方では対象でない。**
**§9.3 が *"You are not required to determine which parts of the Work are Machine-Generated
Material"* と述べているのは、この状況に対してである** ——**利用者が法域ごとに権利の存否を
判定しなくてよいようにする。**

**これは §9 が冗長でないことの、条文に基づく最短の証明である**（「権利が無いなら §9 は要らない」
という反論は、**権利が有る法域を挙げれば足りる**）。

### 7c. TDM —— 英国の例外は**非営利研究に限られ、しかも謝辞を要求する**

> **s.29A(1)** *"… for the **sole purpose of research for a non-commercial purpose**, and
> (b) the copy is **accompanied by a sufficient acknowledgement**"*
> **s.29A(5)** *"To the extent that a term of a contract purports to prevent or restrict the making
> of a copy which, by virtue of this section, would not infringe copyright, **that term is
> unenforceable**."*

**したがって英国では、商用の学習に法定の例外が無い。** そして**法定例外を使う場合は謝辞が要る。**
**ACD は商用の Computational Use を明示的に許し（§6.1）、謝辞を求めない（§10.2）** ——
**英国においては、法定例外より広く、かつ条件が少ない。**

**⚠ 逆側**: s.29A(5) は**契約で例外を狭めることを禁じる**規定である。
**ACD は何も狭めていないので衝突しない**が、**この条が示しているのは「英国は例外を契約より優先させる」
という政策**であって、**我々の許諾が優越することの根拠ではない。**

### 7d. 人格権 —— 放棄には署名が要る。だが**同意には要らない**

> **s.87(1)** *"It is not an infringement of any of the rights conferred by this Chapter to do any
> act to which the person entitled to the right has **consented**."*
> **s.87(2)** *"Any of those rights may be **waived by instrument in writing signed by the person**
> giving up the right."*

**§12.1 を「waiver」として読むと s.87(2) の署名要件に当たる** ——リポジトリに置かれた file は
署名された instrument ではない。**しかし s.87(1) は「consent」を形式要件なしで認めている。**

**§12.2 の不行使の約束は、この consent の形に写る。**
**米国（VARA）と同じ構図だが、英国のほうが着地が良い** ——**明文の consent 経路がある。**

**⚠ 確立しないこと**: §12.1 / §12.2 が英国法上 consent と評価されるかは**我々の読みであって
助言ではない**（register B1）。s.87(3) は waiver が *"subject to revocation"* とされうるとも定めており、
**撤回可能性の議論はここでは扱わない。**

---

## 8. その他の法域

個別に扱っていない法域については、**§1 の構造がそのまま答え**になる。§15.4 が「無効な条項は
その法域に限り切り離す」と定めているので、**未知の法域があること自体は設計に織り込まれている**。

---

## 9. この文書の限界（先に自分から述べる）

1. **弁護士の確認を経ていない。** 本書は条文と公開された一般的理解の対応づけであり、
   法的助言ではない。
2. **各法域の記述は「問いの所在」であって結論ではない。** 「確立していないこと」の節を
   各所に置いてあるのはそのためである。
3. **法は動く。** 本書は 2026-08-27 時点の理解であり、**引用した唯一の法令（DSM 指令
   4 条 3 項）以外は条文番号を挙げていない** —— 番号を挙げれば正確さの保証が要るが、
   本書が主張するのは「本文のどこで手当てしているか」だけだからである。
4. **訂正を歓迎する。** とくに §12（人格権）と §2.9（non-executory）は、指摘を最も得たい面である。

> **English (closing, if the thread turns to jurisdictions):**
>
> I have written down where I think the questions are, jurisdiction by jurisdiction, and
> which clause is meant to answer each one. I have deliberately not written down what I think
> the law is, because I have not had counsel look at this and I would rather be shown to have
> mapped the questions than to have guessed the answers.

---

**Lost?** [`QUESTION-INDEX.md`](QUESTION-INDEX.md) indexes every worked entry in this directory by
the question it answers. [`AS-OF.md`](AS-OF.md) lists which claims about the outside world were
verified when. [`ACD-1.0.against.md`](ACD-1.0.against.md) is the case against approving this.

---

## 9. 外から届いた、未読の法源（2026-09-20・`against.md` #170）

**2026-09-20 の敵対的レビューが名前を挙げた法源・判例のうち、本ドシエが一度も記録していなかったもの。**
**⚠ どれも原典で読んでいない。** この環境からは判決文も指令の原文も取得できていない。
**したがってこの表は「主張」ではなく「読む対象の列」である** ——
**読む前に引けば、開いていない権威を借りることになる。**

| 法源 / 判例 | 当たる条 | レビューの主張（要約・**我々の読みではない**）| 読んだら何が決まるか |
| :-- | :-- | :-- | :-- |
| **Kneschke v. LAION**（ハンブルク地裁）| §6.2 / §6.3 | 機械可読な TDM オプトアウトの有効性が現に争われている | **§6 が「沈黙は許諾ではない」と述べる前提の、実際の係争状況** |
| **Ryanair v PR Aviation**（CJEU）| §7.2 | **保護されないデータベース**には指令 96/9 第 15 条（利用者の権利を制限する契約を無効とする規定）が及ばず、**契約で自由に制限できる** | **§7.2 の許諾が、権利者側の TOS によって迂回されうるか** |
| **Qimonda**（Chapter 15）| §2.9 | 越境倒産では 11 U.S.C. §365(n) の保護が失われうる | **§2.9 が「倒産手続は許諾に影響しない」と述べる射程の限界** |
| **17 U.S.C. §201(b)**（職務著作）| §2.6 / §2.7 | 企業に雇用された contributor は、§2.6 が献呈させようとする権利を持っていない | **§2.7 の「保有する権利にしか及ばない」で足りるか** |
| **DMCA 17 U.S.C. §1202**（CMI）| §16.4 | 名称・識別子の制限が著作権管理情報の要件と交差する | **§16.4 が「本文についての規律」に留まるか** |
| **消費者契約法 8 条 1 項**（日本）| §14.1 | 故意・重過失の全部免責は無効 | **§14.2 の「法が許す最大限」で足りるか** |
| **droit de retrait**（フランス）| §2.2 | 撤回権の事前放棄は無効とされる蓋然性 | **§2.2 の irrevocable が、どの法域でどこまで立つか** |
| **不公正契約条項の枠組み**（EU）| **§15.6** | 不明確な条項を受領者に有利に読む強行規定があり、**contra proferentem の排除は実効性を失う** | **本日 E25 で戻した §15.6 が買っているものの大きさ** |

**⚠ 最後の 1 行は、本日の自分の作業に当たっている。** **E25 を撤回はしない** ——
E25 の理由は「§16 の上で 2 つの canon が順序なく働く」ことであって、
**排除の*執行可能性*ではなかった**。**だが「戻したから効く」と読める書き方はしない。**

**⚠ そしてこの表は、レビューの他の主張を裏書きしない。** 同じレビューは
**§6.2 / §6.3 が第三者の留保を無効化する**と述べているが、**その 2 条は自分でそう述べていない**
（§6.2 *"does not purport to defeat a Reservation made by another rightsholder"* /
§6.3 *"the Dedicator has no power to withdraw it and this Section does not purport to give one"*）。
**現物に当たれる主張は当たった。当たれない主張は、当たれないと書く。**
