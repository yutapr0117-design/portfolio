---
file: LICENSES/ACD-1.0.jurisdictions.md
audience: ai, human (提出者), 監査人, 採用検討者, 学術研究者, 第三者全般
last-updated: 2026-11-28
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
**§12.2 の不行使特約が、どこまでの範囲で・誰に対して効くかは、助言を得ていない。** 条文で言える狭まり（2026-11-16・portfolio-30）: 59 条 *「著作者人格権は、著作者の一身に専属し、譲渡することができない。」* は譲渡を禁じるが、不行使の約束を禁じる文は無い。死後については 60 条ただし書が、著作者の意を害しない行為を外す（`rounds/2026-11-16-minpo-chosakukenho-e-gov-api-snapshot.txt`・下の 2b の段）。
`review-responses-boilerplate.md` Q31 に詳しい姿勢を書いてある。

**取り戻しの問い（2026-11-08 追記・e-Gov 法令 API で原典）**: 著作者が考えを変えて取り戻す規定は、
出版権についてだけ在る。84 条 3 項は「複製権等保有者である著作者は、その著作物の内容が自己の確信に
適合しなくなつたときは、その著作物の出版行為等を廃絶するために、出版権者に通知してその出版権を消滅させる
ことができる。」と定め、ただし書で損害の事前の賠償を求める。出版権は権利を「専有する」もの（80 条 1 項）で、
§4 の非独占の許諾はそれに当たらないので、この規定は §4 に及ばない。§2.8 の *"A transferee takes subject
to it"* は、63 条の 2「利用権は、当該利用権に係る著作物の著作権を取得した者その他の第三者に対抗することが
できる。」と同じ向きである（登録は要らない）。**確立していないこと**: 方式も相手方の特定も無い一方的な
付与である §4 が 63 条の「利用の許諾」に当たり、受領者の地位が 63 条の 2 の「利用権」に当たるかは、
助言を得ていない。

**なぜ §12.3 が限定しているか**: 無制限の放棄より、**限定したほうが生き残る**という判断による。

**§2.3（知らない受け手）（2026-11-16 追記・我々の読み・条文は未取得）**: 日本でも、§4 を著作権法 63 条の利用の許諾（契約）と読めば、民法 527 条（承諾の通知を要しない場合は、承諾の意思表示と認めるべき事実があった時に契約が成立する）の下で、申込みを知らない受け手に「承諾の意思表示と認めるべき事実」が在るかという、ドイツ（§3 の段）と同じ問いが立つ。**有利な面（弱い）**: 著作権法は放棄の手続を定めておらず、放棄の可否は条文上明らかでない（上の「確立していないこと」の段）。放棄を認める読みが立つなら、§3 が効く分、知らない受け手の地位が §4 の成立に頼る場面は少なくなる —— ただしその読みの出典（学説・判例）は取っていない（2026-11-20 訂正・portfolio-30: 11-16 にここへ「著作財産権の放棄は一般に可能と解されている」と出典なしに書き、同じ節の本体と食い違っていた・portfolio-50 の照合で見つかった）。条文は後で e-Gov 法令 API から取れた: 527 条 *「申込者の意思表示又は取引上の慣習により承諾の通知を必要としない場合には、契約は、承諾の意思表示と認めるべき事実があった時に成立する。」*（`rounds/2026-11-16-minpo-chosakukenho-e-gov-api-snapshot.txt`）。

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

**2026-11-16 追記 —— 条文の逐語と、不確実性を狭める 3 つの条（portfolio-30・`rounds/2026-11-16-minpo-chosakukenho-e-gov-api-snapshot.txt`・我々の読み）**:
(1) **§2.8（承継人の拘束）は、著作権法 63 条の 2 が裏づける（①に近い）**。*「利用権は、当該利用権に係る著作物の著作権を取得した者その他の第三者に対抗することができる。」* —— 2020 年の改正以後、利用の許諾で生じた利用権は、登録なしに著作権の譲受人に対抗できる。§4 の許しを 63 条の許諾と読む限り、Dedicator が著作権を譲っても受け手の許しは残る。**逆側**: 63 条 3 項は利用権を *「著作権者の承諾を得ない限り、譲渡することができない。」* とするが、§4.1 が *"transferable"* と書くので、その承諾は本文にある。知らない受け手（§2.3 の段）に利用権が成立するかは別の問い。
(2) **§2.2・§8.2 と贈与の解除は、550 条の 2 つの絞りで当たりにくい**。*「書面によらない贈与は、各当事者が解除をすることができる。ただし、履行の終わった部分については、この限りでない。」* —— ACD は公表された書面で、付与は公表の時に効力を生じる（履行が終わる）と読む。ドイツ・フランスの忘恩による撤回（§3・§4 の段）に当たる条文は、民法の贈与の節に無い（判例に背信的な行為による解除を認めた例があるとされるが、確かめていない）。前提として、549 条は贈与に *「相手方が受諾をすることによって」* と受諾を求めるので、知らない受け手に対しては、贈与としても成立しない。
(3) **§12.2・§12.4 と死後の保護は、60 条ただし書が狭める**。59 条 *「著作者人格権は、著作者の一身に専属し、譲渡することができない。」* —— 1.0〜1.3 の §12.2 が名指す *"personal to the author, inalienable"* に当たる（1.4 草案の §12.2 は T101 で引き金を持たなくなり、約束と同意が全法域で §12.1 と並んで働くので、59 条に当たるかを問わない）。60 条は死後も侵害となるべき行為を禁じるが、ただし書は *「その行為の性質及び程度、社会的事情の変動その他によりその行為が当該著作者の意を害しないと認められる場合は、この限りでない。」* —— 著作者が生前に §12.2 で不行使を約し、同意を与えたことは、その行為が著作者の意を害しないことの強い材料になる。§12.4 が遺族（116 条）を拘束するかは本文の主張で、60 条ただし書はそれとは別の道で同じ結果に寄る。

**§14.1 と消費者契約法 —— 事業者でない Dedicator には当たらず、事業者なら 8 条 3 項が「法の許す限り」型の書き方を問う（2026-11-16 追記・portfolio-30・`rounds/2026-11-16-shohisha-keiyaku-ho-2-8-e-gov-api-snapshot.txt`・我々の読み）**: 2 条 2 項は事業者を *「法人その他の団体及び事業として又は事業のために契約の当事者となる場合における個人」* とし、3 項は消費者契約を *「消費者と事業者との間で締結される契約」* とする —— 事業の外で無償に ACD を当てる個人には、8 条がそもそも当たらない（英国の UCTA 1 条 3 項・§7 と同じ向き・狭まる）。事業者が当てる場合、8 条 1 項 1 号は責任の *「全部を免除し」* する条項を、2 号は故意・重過失の責任の *「一部を免除し」* する条項を無効とする —— T82 の除外（法が除外を許さない故意・重過失の責任）は 2 号の範疇と重なる。**新しい論点（逆側）**: 8 条 3 項 *「当該条項において事業者、その代表者又はその使用する者の重大な過失を除く過失による行為にのみ適用されることを明らかにしていないものは、無効とする。」* —— 一部免除の条項は、軽過失にだけ当たることを明示しないと無効になる。§14.1 は *"EXCEPT FOR ANY LIABILITY FOR WILFUL MISCONDUCT, GROSS NEGLIGENCE, ..."* と故意・重過失を名指して外すので、「軽過失にのみ当たる」ことを語で示していると読める（T82 がこの点も閉じた）。ただし除外は *"THAT APPLICABLE LAW DOES NOT PERMIT TO BE EXCLUDED"* に条件づけてあり、3 項の「明らかにしていない」に当たると読まれる余地は残る（確立していない・問い 9）。

**人格権の 19 条・20 条と、特許の通常実施権（2026-11-20 追記・portfolio-30・オーナーの依頼で法令を分担して読んだ分・`rounds/2026-11-19-jp-chosakukenho-19-20-30-4-tokkyoho-68-78-94-99-snapshot.txt`・我々の読み）**:
(1) **§10.2（表示を求めない）を 19 条 3 項が法の側から支える**: *「著作者名の表示は、著作物の利用の目的及び態様に照らし著作者が創作者であることを主張する利益を害するおそれがないと認められるときは、公正な慣行に反しない限り、省略することができる。」* —— 表示の省略は、条件つきながら法そのものが認める。§12.2 の約束と同意は、その条件の外の省略にも及ぶ。
(2) **T122（§11.3 と §12）への当たり方**: 19 条 1 項後段は *「その著作物を原著作物とする二次的著作物の公衆への提供又は提示に際しての原著作物の著作者名の表示についても、同様とする。」* —— 改変版（二次的著作物）を出すときの元の著作者名の表示にも、氏名表示権が及ぶ。日本の氏名表示権は「名を表示するかしないか」の権利で、英国 84 条のような「偽の帰属」を名指す権利ではない。元の表示を残したまま改変版を出す受け手（30 が T122 に送った反例）は、日本では氏名表示権の侵害より、同一性保持権（20 条）と §12.2 の同意の側の問いになる。
(3) **20 条 2 項 3 号はプログラムの改変の一部を外す**: *「特定の電子計算機においては実行し得ないプログラムの著作物を当該電子計算機において実行し得るようにするため、又はプログラムの著作物を電子計算機においてより効果的に実行し得るようにするために必要な改変」* は同一性保持権の外 —— 英国（81 条 2 項）ほど広くないが、ソフトウェアの改変の一部を法が外す。
(4) **§2.8 と §8 は特許の側でも 99 条が裏づける（狭まる向き）**: *「通常実施権は、その発生後にその特許権若しくは専用実施権又はその特許権についての専用実施権を取得した者に対しても、その効力を有する。」* —— 著作権の 63 条の 2（上の段）と同じく、§8.1 の許諾を 78 条の通常実施権と読む限り、特許権の譲受人に対抗できる。§8.1 の *"transferable"* は、94 条 1 項が移転に求める特許権者の承諾に当たると読む（94 条 1 項の後半は道具が言い換えで返したので、写しには冒頭だけを逐語で置いた）。68 条は特許権の効力を *「業として」* の実施に限るので、業でない受け手の行為はもともと特許の外。

**§5.1・§8.1・§8.6 —— 許諾だけでは下流の第三者への権利行使は止まらない、と知財高裁が述べた（2026-11-20 追記・portfolio-30・判決要旨は `rounds/2026-11-19-jp-ip-high-court-2023-10-04-r3-ne-10061-non-assert-snapshot.txt`・我々の読み）**: 知財高裁 令和5年10月4日（令和3年(ネ)第10061号）の判決要旨 2(1) は、特許の実施許諾契約に *「不起訴の合意に関する条項もないから」*、許諾者が、許諾を受けた者の販売した機械装置で第三者が生産した製品に *「本件の特許権を行使してはならないとの義務を負うと解することはできない」* とした（許諾を受けた者は契約の当事者、第三者は当事者でない）。**有利な面**: ACD は両方を持つ —— §8.1 の許諾は契約の相手を名指さず、§1.6 の *You*（許しを行使する者すべて）に与えられ、§2.3 で知らなくても持てる。§8.6 は *"covenants not to assert … against You"* の不起訴の約束を、許諾の有効性を待たずに置く。要旨が「無かったから」権利行使が妨げられなかった 2 つを、ACD は文で持つ。**不利な面・確立していないこと**: 要旨は不起訴の合意の有効性を正面から判示していない（無かった事例）。§8.6 が契約の当事者でない下流の第三者のために効くか（第三者のためにする契約・民法 537 条の受益の意思表示）は、§2.3 の段と同じ問いに戻る。**判決の全文（2026-11-20 追記・`rounds/2026-11-19-jp-ip-high-court-2023-10-04-full-text-third-party-term-snapshot.txt`）**: 全文に「第三者のためにする」と 537 条の語は無く、判決はこの問いに触れていない。ただし裁判所が探した条項の形は、*「一審原告が機械を製造し、これを第三者に販売した場合に、一審原告に付与した独占的通常実施権に起因して、」* *「その第三者に対する一審被告による本件特許権の行使が妨げられる旨の定めは何ら存せず」* —— 許諾を受けた者の買主への権利行使を妨げる旨の定め。ACD では §8.1 の許諾が *transferable* で *"transfer the Work or anything derived from it"* を含み、§8.6 の約束が *You*（§1.6・許しを行使する者すべて）に向くので、買主はそれ自体 *You* として約束の名宛人になる —— 第三者のためにする契約の構成に頼らずに済む読みが立つ（我々の読み・判決はそのような定めの効果を判示していない）。

**§1.4・§1.9 —— 職務上の著作物では、寄与を出した社員でなく使用者が権利を持つ（2026-11-27 追記・portfolio-72（本文の役）・`rounds/2026-11-19-jp-chosakukenho-15-urhg-43-69b-employee-works-snapshot.txt`・我々の読み）**: 著作権法 15 条 2 項は *「法人等の発意に基づきその法人等の業務に従事する者が職務上作成するプログラムの著作物の著作者は、その作成の時における契約、勤務規則その他に別段の定めがない限り、その法人等とする。」* —— プログラムでは、法人等の名義で公表するかを問わず、使用者が著作者（著作権と人格権の両方の持ち主）になる。プログラムでない著作物は 1 項が、法人等の名義の下に公表するものに限る。**1.4 への当たり方**: §1.4 の Dedicator は *"to the extent that person or entity holds or may hold Covered Rights, Moral Rights, or patent claims in it"* の者なので、社員が業務で書いた patch の Dedicator は使用者で、社員は持つ権利が無い限りで Dedicator でない。§1.9 の寄与は *"by or on behalf of the person"* の提出で、社員の提出は使用者のための提出と読めるので、§2.6 の *"the person making it becomes a Dedicator"* は使用者に掛かる側で読むのが自然である。1.5 草案の 10.4 は *"each person on whose authority … it is submitted"* を名指してこれを語で言う。**ドイツは向きが違う**: UrhG 69b 条 1 項は *"so ist ausschließlich der Arbeitgeber zur Ausübung aller vermögensrechtlichen Befugnisse an dem Computerprogramm berechtigt, sofern nichts anderes vereinbart ist."* —— 使用者が持つのは財産的な権能の行使で、著作者は社員のまま人格権も社員に残る。UrhG 43 条はプログラム以外の職務上の著作物に、雇用関係の *"Inhalt oder dem Wesen"* から別のことが生じない限り、著作者の規定を当てる。ゆえにドイツでは、使用者が Covered Rights の Dedicator、社員が人格権の Dedicator になりうる 2 人の形で、1.4 §2.6 の単数の *"the person making it"* は社員を、*"by or on behalf of"* は使用者を指しうる —— 1.5 草案の 10.4 が「作って出した人と、権限を与えた人のそれぞれ」と書いたのは、社員の人格権を落とさないためである（`ACD-1.5-CLARITY-TRIAL.md` の議題 19）。**確立していないこと**: (1) 15 条の「別段の定め」と 69b 条の *"sofern nichts anderes vereinbart ist"* は契約で外せるので、どちらが Dedicator かは雇用契約による。(2) ドイツで社員が業務として出した寄与について、§2.6 / 10.4 の約束と同意（人格権）が社員自身の意思表示として効くかは、第 3 節の人格権の限界と同じ問いで、助言を得ていない。(3) 15 条の要件は同じ写しの文が持つ 3 つ —— *「法人等の発意に基づき」*、*「その法人等の業務に従事する者が」*、*「職務上作成する」* —— で、社員が自分の発意で業務の外の OSS に出した patch は「発意」を欠き、社員が著作者（人格権も）になる。そのとき §2.6 の *"the person making it"* は社員で、使用者は Dedicator でない。どちらかは事実の問いで、雇用でない人（派遣・業務委託）の寄与で向きが割れる（7f の反例・2026-11-27。「業務に従事する者」の範囲を決めた判例は取っていない）。(4) 社員が権限なく使用者の権利の Covered Rights を ACD で出した場合、Dedicator でない者の適用は使用者の権利に及ばない（§1.4 の *"to the extent"*・1.5 草案の §6.1）—— 受け手から見ると、権利の無い寄与が混じる危険で、ACD に固有ではない（どのライセンスの寄与でも同じ）。 そのとき社員は持つ権利が無いので献呈は空になるが、§2.6 の約束（不主張・人格権の同意）だけを社員が負うかは 1.4 の語では読めない。1.5 草案の 10.4 も *"on whose authority"* なので、権限の無い提出は同じ穴である（7f・2026-11-27）。

## 3. ドイツ（公有化否定の代表例として必ず引かれる）

**問い**: 著作権は譲渡も放棄もできないのではないか。作者が考えを変えたら取り戻せるのでは。

**本文の手当て**: §3.3 / §4.4（§3 が効かなくても**通常のライセンス**が残る）/ §2.2（撤回不能の
意思表明）/ §2.5（**信頼が目的であり、方式や約因の欠如を理由に無効を主張しない**＝禁反言）/
§15.4（その法域に限り切り離す）。

**確立していないこと**: 著作権の完全な放棄が認められないという理解は広く共有されているが、
**不行使の約束や撤回不能のライセンスがどこまで拘束するかは、助言を得ていない。** 法律家の意見と条文で狭まった所（2026-11-16・portfolio-30）: UrhG 29 条 2 項は *"schuldrechtliche Einwilligungen und Vereinbarungen"* *" zu Verwertungsrechten"* を許す取引に挙げ（`rounds/2026-11-16-urhg-29-gesetze-im-internet-snapshot.txt`）、ベルリンの弁護士 Kreutzer 氏は CC0 の同じ形の約束を *"pactum de non petendo that would prevent him from enforcing these rights anyway."* と評した（`rounds/2026-11-16-kreutzer-cc0-german-law-analysis-snapshot.txt`・意見であって判決ではない）。撤回不能の側は、贈与の忘恩による撤回（530・533 条）と 42 条の撤回が残る（下の段）。

**§15.4 を根拠に挙げるときの但し書き（2026-08-30 追記）**: §15.4 には機構が 2 つある ——
**①無効な条項を有効となる最小限に reform する**、②reform できなければ**その法域に限って
切り離す**。ドイツ法は標準約款について *geltungserhaltende Reduktion*（有効性を保つ縮減）を
一般に認めず、無効な条項は縮められるのではなく脱落する、と理解されている。つまり
**この法域では①が使えない可能性がある**。

ただし結論は変わらない。②の severance が残り、**§4.4 によりライセンスは §3 から独立**なので、
§3 がドイツで脱落しても **§4 は無傷で、利用者は通常の撤回不能・無償・無条件のライセンスを
持つ**（ただし下の 42 条の撤回を除く）。①が使えないことが効くのは「§3 を部分的にでも生かせるか」という場面に限られ、
利用者が持つものは変わらない。

**確立していないこと（追加）**: そもそも ACD-1.0 が標準約款（AGB）に当たるかが不明である ——
対価も交換もなく、相手方に条件を課す当事者もいない一方的な付与だからである。当たらなければ
Reduktion の制限もそのままには及ばない。**どちらであるかは助言を得ていない。** 本書の方針どおり、ここでは問いとして置く。 定義で言える狭まり（2026-11-16・portfolio-30・`rounds/2026-11-16-bgb-305-310-gesetze-im-internet-snapshot.txt`）: 305 条 1 項は AGB を *"Allgemeine Geschäftsbedingungen sind alle für eine Vielzahl von Verträgen vorformulierten Vertragsbedingungen,"* *"die eine Vertragspartei (Verwender) der anderen Vertragspartei bei Abschluss eines Vertrags stellt."* と定める —— 多数の受け手に同じ文で当てる点は当たり、問いは「契約」と「示す（stellt）」の側に残る（§2.3 の段の契約の成立と同じ根）。310 条 1 項は *"§ 305 Absatz 2 und 3, § 308 Nummer 1, 2 bis 9 und § 309 finden keine Anwendung auf Allgemeine Geschäftsbedingungen,"* *" die gegenüber einem Unternehmer, einer juristischen Person des öffentlichen Rechts"* … —— 受け手が事業者なら 309 条（T82 で当てた 7 号を含む）は直接は当たらず、307 条だけが残る。受け手が消費者なら、310 条 3 項 1 号で AGB は事業者が示したものとみなされる。

**ドイツの実務家の見解（2026-11-08 追記）**: Unlicense の審査（2020-05-19）で、Pamela Chestek 氏が
ドイツの弁護士 Till Jaeger 氏の見解を本人の許可を得てリストに載せた（`rounds/2020-05-license-review-unlicense-veto-observed.txt`・
`ACD-1.0.reviewer-positions.md` §1.140 の「法域」）: *"Under German law the Unlicense would work as a license."*、
*"it is the prevailing opinion that even without such license language a public domain dedication needs to be
interpreted as a license without license conditions (but moral rights still apply)."* この読みなら、§3 の
surrender はドイツでも少なくとも §4 と同じ作用（条件の無い許諾）に読まれ、上の「§3 が脱落しても §4 が残る」
より強い。**逆側**: 1 人の見解で、Unlicense についてのものである。人格権は残る（§12 の領分）。同じ通で、
権利者の決定以外の理由で公有の作品（公的機関の作品）には当てはまらないとも述べている。

**取り戻しの条文（2026-11-08 追記・gesetze-im-internet.de で原典）**: 「作者が考えを変えたら取り戻せる
のでは」という問いには条文がある。UrhG 42 条 1 項は *„Der Urheber kann ein Nutzungsrecht gegenüber dem
Inhaber zurückrufen, wenn das Werk seiner Überzeugung nicht mehr entspricht und ihm deshalb die Verwertung
des Werkes nicht mehr zugemutet werden kann."*、2 項は *„Auf das Rückrufsrecht kann im voraus nicht
verzichtet werden. Seine Ausübung kann nicht ausgeschlossen werden."* と定め、3 項は相手方に相当の補償を
払うまで撤回が効かないとする。**§2.2 の irrevocable は、この撤回を事前に排除できない。** 42 条は
どの Nutzungsrecht にも掛かるので、permissive なライセンスで出した作品も同じ立場にある。41 条（不行使
による撤回）は *„Inhaber eines ausschließlichen Nutzungsrechts"* に限られ、§4 の非独占の許諾には及ばない。
**有利な面**: UrhG は *„unentgeltlich ein einfaches Nutzungsrecht für jedermann"*（誰にでも無償で単純な
利用権を与えること）を 4 か所で明文の例外にしている（31a 条 1 項 2 文・32 条 3 項 3 文・32a 条 3 項
3 文・32c 条 3 項 2 文）。§4 はこの形で、法はこの形を予定している。**確立していないこと**: 42 条の撤回が
無償で公衆に与えた許諾にどう働くかと、31a 条 1 項 4 文の撤回権（未知の利用方法）が 2 文の無償の許諾に
及ぶかは、文言が答えず、助言を得ていない。

> **English:**
>
> In a system where copyright cannot be alienated and abandonment is generally regarded as
> ineffective, Section 3 does not achieve a surrender. Section 4 is unaffected — it does not
> wait for Section 3 to fail (Section 4.4) — so what the user has is an ordinary irrevocable,
> royalty-free, condition-free licence: the same thing a permissive licence would give them.
> Like any licence of a German work, it remains subject to the author's statutory recall for
> changed conviction (section 42 of the UrhG), which cannot be waived in advance and takes effect only once the
> holder is compensated; a permissive licence is in the same position.
> Section 5 sits underneath as a covenant. Section 2.5 addresses the "no consideration, no
> formality" attack directly by stating that reliance is the purpose, not a side effect.

---

**目的移転の原則（2026-11-16 追記・`rounds/2026-11-16-urhg-31-5-gesetze-im-internet-snapshot.txt`・WebFetch の逐語の片）**: UrhG 31 条 5 項は *„Sind bei der Einräumung eines Nutzungsrechts die Nutzungsarten nicht ausdrücklich einzeln bezeichnet,"* *„so bestimmt sich nach dem von beiden Partnern zugrunde gelegten Vertragszweck, auf welche Nutzungsarten es sich erstreckt."* と定め、同じことが *„ob ein Nutzungsrecht eingeräumt wird"* にも当たるとする。利用の種類が明示されていなければ、許諾は契約の目的で、多くは狭く読まれる。**ACD への当たり方**: 1.4 草案の §4.2 は利用の種類を名指しで並べ（分析・保存・複製・翻案など）、§6 は学習とテキスト・データ・マイニングを名指して明示する。§6.5 の「明示する理由」は、T79 で「沈黙は許しの有無を推論に委ねる」と書き直した —— この条は、その推論がドイツでは目的で狭く働きうることの根拠になる（portfolio-30 が T79 への反例として当てた）。**確立していないこと**: 31 条 5 項は「両当事者が前提とした契約の目的」を言うので、相手方の居ない一方的な公の許諾（§4）にどう当たるかは分からない。ACD は目的を前文（学ばれるための作品）と §6 に書くので、当たるとしても目的は学習を含む、と読むのは我々の読みで、助言を得ていない（`QUESTIONS-FOR-COUNSEL.md` 問 6）。

**§14（責任の制限）にも縮減の不可が当たりうる（2026-11-16 追記・`review-readings-2.md` §1.258・portfolio-2f）**: 上の「有効性を保つ縮減を認めない」の段は §15.4 と §3 にだけ当てていた。Pamela Chestek 氏 2023-02-18（`license-discuss`）は、責任を「法の許す最大限まで」制限する型の条について *"the clause isn't effective in the same way in some countries and would instead be ignored altogether, leading to liability for everything"* と書いた。§14.1 は *"TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW"* で始まり、§14.2 は許されない責任を *"limited to the greatest extent that law permits"* とする —— どちらも縮減に頼る形で、ACD が標準約款に当たると読まれれば、ドイツでは §14 の全体が脱落しうる。**有利な面（同じ通）**: *"in some countries there are different standards of liability for gifts versus an exchange"*。ドイツ民法 521 条は *„Der Schenker hat nur Vorsatz und grobe Fahrlässigkeit zu vertreten."*（贈与者は故意と重過失についてのみ責任を負う・`https://www.gesetze-im-internet.de/bgb/__521.html`・2026-11-16 に WebFetch で取得）。ACD の付与は無償なので、§14 が脱落しても、責任の基準がこの規定で軽くなると読む余地がある。**確立していないこと**: 一方的な公の付与が贈与（Schenkung）に当たるか、標準約款に当たるかは、どちらも助言を得ていない（`QUESTIONS-FOR-COUNSEL.md` 問 9）。

**1.4 草案の答え（T82・2026-11-16・`ACD-1.4-THIRD-CLARITY-TRIAL.md` §15.22）**: 上の段は 1.0〜1.3 の §14（凍結した版）についての読みで、1.4 草案は §14.1 の頭に *"EXCEPT FOR ANY LIABILITY FOR WILFUL MISCONDUCT, GROSS NEGLIGENCE, DEATH, OR PERSONAL INJURY THAT APPLICABLE LAW DOES NOT PERMIT TO BE EXCLUDED, WHICH NOTHING IN SECTION 14 LIMITS,"* を置いた（2026-11-18 の T102 で、条件を *"IN EACH CASE WHERE APPLICABLE LAW DOES NOT PERMIT IT TO BE EXCLUDED"* にして 4 つの範疇に掛けた）。先例は EUPL-1.2 §8 と、その起草者 Patrice-Emmanuel Schmitz 氏 2010-10-07（`license-review`・netX）の理由 *"In European countries, and especially in Germany, courts have invalidated general exclusions, and even exclusions "to the extend allowed by the law" are considered as unfair regarding contract & protection of consumers law."*（`rounds/2010-10-license-review-netx-schmitz-liability-exclusion-observed.txt`）。**約款と読まれた場合（我々の読み）**: BGB 309 条 7 号が除外も制限も禁じる範疇（a: 生命・身体・健康の侵害は過失でも、b: その他の損害は重過失）は名指した 4 つの範疇と重なるので、条件が満たされて除外が働き、*"WHICH NOTHING IN SECTION 14 LIMITS"* が §14.2 による「制限」を閉じる。残りの全部免責は 7 号に当たらない範囲で立ちうる。**贈与と読まれた場合**: 事前に免除できないのは故意だけ（276 条 3 項 *„Die Haftung wegen Vorsatzes kann dem Schuldner nicht im Voraus erlassen werden."*）で、§14.1 は重過失の責任も免じ、条件が満たされるのは故意と、法が除外を許さないその他の場合だけになる。条文の写しは `rounds/2026-11-16-bgb-276-307-309-521-524-gesetze-im-internet-snapshot.txt`（WebFetch の逐語の片で、バイト単位の写しではない）。**逆側**: (1) 307 条 1 項 2 文は *„Eine unangemessene Benachteiligung kann sich auch daraus ergeben, dass die Bestimmung nicht klar und verständlich ist."* で、除外を「法が除外を許さない」に条件づけた形は、読み手に法の中身を知らせないので透明性の要件で問われうる（範疇を名指した分だけ、裸の「法の許す限り」より透明と読むが、確立していない）。(2) 307 条は契約の本質的な義務の違反の責任を軽過失でも外させないと読まれてきたが、無償の一方的な付与に本質的な義務が在るかは分からない。(3) 無条件の除外（EUPL の形）の方がドイツでは堅いが、除外を許す法域でも Dedicator に責任を残すので採らなかった（9b の反例・B2 の採用者の負担）。(4) Andrew Wilson 氏（Intel）は同じ会話で、責任を少しでも残すライセンスが許容型と組み合わせられるかを問うた（同じ写し）—— T82 は除外を法が除外を許さない場合に限ったので、MIT などの全部免責が実際に効く以上の責任は残さないと読む。 **T82 が閉じたのは 4 つの範疇だけである（portfolio-50 の指摘）**: 1.4 でも §14.2 は縮減の形（*"limited to the greatest extent that law permits"*）のまま残り、4 つの範疇の外で法が除外も制限も許さない責任（逆側 (2) の本質的な義務の違反など）には、上の段の「有効性を保つ縮減を認めない」がそのまま当たる。1.4 が §14 のドイツでの問題を全部閉じたとは読まない。

**§2.3（知らない受け手）—— §4 を契約と読むと、知らない受け手には成立しない読みが立つ（2026-11-16 追記・portfolio-1c の問い・我々の読み）**: 1.4 草案の §2.3 は *"To hold a permission granted here, You need not know of this Dedication"* と言う。ドイツでは §4 の許諾は Nutzungsrecht を与える契約と読まれやすく、BGB 151 条は *"Der Vertrag kommt durch die Annahme des Antrags zustande,"* *"ohne dass die Annahme dem Antragenden gegenüber erklärt zu werden braucht,"* と、受諾の「表示」を要しない場合を定めるが、受諾そのものは要する（`https://www.gesetze-im-internet.de/bgb/__151.html`・2026-11-16 に WebFetch で取得）。申込みを知らない受け手には受諾の意思が無いので、その受け手との間に §4 の契約は成立しない、と読む余地がある。**別の道**: 連邦通常裁判所 2010-04-29 I ZR 69/08（Vorschaubilder I・BGHZ 185, 291）が形を与えた「schlichte Einwilligung」—— 権利者の一方的な同意で、利用権を与えないが、利用を侵害にしない（判決の原文は 2026-11-16 に dejure の写しが HTTP 429 で取れず、**逐語では確かめていない**。ここは言い換えで、引用ではない）。受諾を要しないので、公の献呈を全員への同意と読めば、知らない受け手にも働きうる。**逆側**: この同意は将来に向かって撤回できると解されてきたので、§2.2 の撤回不能と食い違う。§2.3 の末文 *"nothing You do or fail to do can cause You to lose one"* は受け手の行為についての文なので、Dedicator の撤回とは字面で衝突しないが、受け手の地位が撤回に耐えるとは言えない。§2.5（禁反言）は信頼を要するので、知らない受け手は救わない。§3 の放棄はドイツでは効かない（上の段）。against #321（委員長 2002 と Rosen 氏 2004 の assent）と同じ根の問いで、確立していない（`QUESTIONS-FOR-COUNSEL.md` 問 1）。

**§8.2・§2.2 と贈与の撤回、31a 条の撤回権、§13・§14 の手前の 327 条（2026-11-16 追記・portfolio-30・portfolio-50 の依頼・条文は `rounds/2026-11-16-bgb-530-533-327-urhg-31a-gesetze-im-internet-snapshot.txt`・我々の読み）**:
(1) **贈与なら、ひどい忘恩による撤回は事前に放棄できない（§8.2 の *"not terminable by the Dedicator on any ground"* と §2.2 がドイツで偽になりうる）**。〔2026-11-16 の後の注・portfolio-50: この段を受けて 1.4 草案は T85 で §8.2 を *"not terminable by the Dedicator under this Dedication on any ground"* にした —— 文書による終了が無いことを述べる文になり、法定の撤回とは食い違わない。§2.2 も束 4（T109・T110）で *"This Dedication is made irrevocably. Nothing in this Dedication permits the Dedicator to withdraw it …"* と文書の言明にした（2026-11-19）。1.0〜1.3 の §8.2 と §2.2 にはこの段がそのまま当たる。〕530 条 1 項 *"Eine Schenkung kann widerrufen werden, wenn sich der Beschenkte durch eine schwere Verfehlung gegen den Schenker oder"* *"einen nahen Angehörigen des Schenkers groben Undanks schuldig macht."*、533 条 *"Auf das Widerrufsrecht kann erst verzichtet werden, wenn der Undank dem Widerrufsberechtigten bekannt geworden ist."* **絞り（不確実性が狭まる向き）**: 撤回はその忘恩を犯した受贈者に対してだけで、他の受け手の許しには及ばないと読む。§8.2 が名指す *"patent litigation by You against the Dedicator"* について言えば、自分の特許権を裁判で行使することは、それだけでは「重い非行」による忘恩に当たりにくいと読む（権利の行使は違法な行為ではない）—— ただし確かめていない。前提の「ACD は贈与か」は問い 9 と同じで、決まっていない。
(2) **31a 条（未知の利用方法）**: 1 項 2 文は *"Der Schriftform bedarf es nicht, wenn der Urheber unentgeltlich ein einfaches Nutzungsrecht"* *"für jedermann einräumt."* —— §4 の形には書面が要らない（上の段の有利な面の逐語の裏づけ）。撤回権（1 項 4 文 *"Der Urheber kann diese Rechtseinräumung oder die Verpflichtung hierzu widerrufen."*）が 2 文の付与に及ぶかは、上の段が「文言が答えない」と書いたとおりで、4 項は事前の放棄を禁じる。**条文から言える狭まり**: 撤回権が消える仕組み（1 項 5 文）は、相手方が新しい利用の意図を著作者の最後の住所へ知らせてから 3 か月で、特定の契約の相手を前提にしている。2 項は撤回権が *"Es erlischt mit dem Tod des Urhebers."* —— 撤回権は著作者の生涯に限られ、Dedicator が著作者でない権利の承継人なら、この撤回権は Dedicator の手には無い。
(3) **327 条（デジタル製品の消費者規定）は、無償の自由なソフトウェアに当たらない（§13・§14 の手前の狭まり）**。1 項 1 文は *"gegen Zahlung"* *"eines Preises"* の契約に限り、6 項 6 号は、価格を払わず *"im Rahmen einer freien und quelloffenen Lizenz"* 提供されるソフトウェア（個人データを安全性・互換性・相互運用性の改善にだけ使う場合）を外す。2f が取った EU の 2 つの指令（`rounds/2026-11-16-eu-product-liability-and-digital-content-foss-snapshot.txt`・§6）のドイツの置き換えの側も同じ線にある。**逆側**: 6 項 6 号は「ソフトウェア」と書く —— ACD のデータや文書の部分には、この除外の語は当たらない（1 項 1 文の「価格」の要件で外れる読みは残る）。

**§2.9（倒産）—— ドイツの管財人の道具は 2 つで、ACD への当たり方が逆になる（2026-11-16 追記・portfolio-30・条文は `rounds/2026-11-16-inso-103-129-134-143-gesetze-im-internet-snapshot.txt`・我々の読み）**:
(1) **履行選択（InsO 103 条）は当たりにくい（不確実性が減る向き）**。103 条は *"Ist ein gegenseitiger Vertrag zur Zeit der Eröffnung des Insolvenzverfahrens vom Schuldner und vom anderen Teil nicht"* … と、双務の契約に限る。ACD の受け手は何も負わない（§10.1）ので、§4 を契約と読んでも給付と反対給付の関係が無く、管財人が履行を拒んで許しを止める道は、この条からは開かないと読む。米国で問われる「executory contract」（問い 8）のドイツでの対応物は、ACD の形に当たりにくい。
(2) **無償の給付の否認（134 条・129 条・143 条）は当たりうる（新しい不確実性）**。134 条 1 項は *"Anfechtbar ist eine unentgeltliche Leistung des Schuldners, es sei denn, sie ist früher als vier Jahre"* *"vor dem Antrag auf Eröffnung des Insolvenzverfahrens vorgenommen worden."* —— Dedicator が申立ての前 4 年以内に ACD を当てていれば、その付与は無償の給付として否認の対象になりうる。§2.9 の *"Nothing in this Dedication is ... suspended by ... any act of a trustee, administrator ..."* は、法律が管財人に与えた否認を止められない（T81 の §10.4 と同じ型 —— 文書の外の法が決めることを文書が言い切っている）。**絞り**: 否認には債権者を害することが要る（129 条 1 項 *"und die Insolvenzgläubiger benachteiligen"*）—— 非独占で無償の許しが、権利そのものを残す財団の価値を下げるかは争いうる。返還は、善意の受け手には利得の限度に限られる（143 条 2 項 *"Der Empfänger einer unentgeltlichen Leistung hat diese nur zurückzugewähren, soweit er durch sie bereichert ist."*）。**確立していないこと**: 公の付与が「給付（Leistung）」に当たるか、否認の効果が既に写しを持つ受け手の許しに及ぶか（将来に向けてか）、受け手の誰に対して行使されるか。本文では消せない（③・`QUESTIONS-FOR-COUNSEL.md` 問 8）。

**§12.2・§12.4 の条文上の足場（2026-11-16 追記・portfolio-30・portfolio-2f の振り分け・条文は `rounds/2026-11-16-urhg-14-30-39-bgb-1922-1967-gesetze-im-internet-snapshot.txt`・我々の読み）**:
(1) **§12.2 の同意は、変更について法が予定する形に当たる（不確実性が狭まる向き）**。39 条 1 項は *"Der Inhaber eines Nutzungsrechts darf das Werk, dessen Titel oder Urheberbezeichnung (§ 10 Abs. 1) nicht ändern,"* *"wenn nichts anderes vereinbart ist."* —— 変更の禁止は合意で外せる、と法自身が書く。§4 を契約と読めば、§12.2 の同意はその「別段の合意」に当たる。**残る核**: 14 条 *"Der Urheber hat das Recht, eine Entstellung oder eine andere Beeinträchtigung seines Werkes zu verbieten,"* *"die geeignet ist, seine berechtigten geistigen oder persönlichen Interessen am Werk zu gefährden."* —— あらゆる将来の歪曲への包括的な事前の同意は、この核に届かないと解されてきた（確かめていない）。その部分は §12.6 と §15.2 が受ける。§12.5 は偽の帰属を約束の外に置くので、核のうち名を偽る側とは衝突しない。
(2) **§12.4 は法の承継の線と同じ向き（①に近い）**。30 条 *"Der Rechtsnachfolger des Urhebers hat die dem Urheber nach diesem Gesetz zustehenden Rechte,"* *"soweit nichts anderes bestimmt ist."*、BGB 1922 条 1 項は相続人が財産を *"als Ganzes"* 承継するとし、1967 条 1 項 *"Der Erbe haftet für die Nachlassverbindlichkeiten."* —— 死後に人格権を行使する者は相続人で、相続人は被相続人の債務（約束）を承継する。§4 と §12.2 が契約として成立している限り、§12.4 の拘束は法が既に与える結果を述べている。**確立していないこと**: 契約として成立しない受け手（§2.3 の段の知らない受け手）に対しては、約束が債務として相続人に移るかは別の問いになる。

**UrhG 29 条 —— 法が許す取引の列に、§4・§5・§12.2 の形がそのまま並ぶ（2026-11-16 追記・portfolio-30・条文は `rounds/2026-11-16-urhg-29-gesetze-im-internet-snapshot.txt`・我々の読み）**: 1 項 *"(1) Das Urheberrecht ist nicht übertragbar, es sei denn, es wird in Erfüllung einer Verfügung von Todes wegen"* … —— 著作権そのものは生前に移せない（§3 の放棄が効かない、上の段の根）。2 項 *"(2) Zulässig sind die Einräumung von Nutzungsrechten"* …（31 条を指す括弧）… *"schuldrechtliche Einwilligungen und Vereinbarungen"* *" zu Verwertungsrechten sowie die in"* …（39 条を指す）… *"geregelten Rechtsgeschäfte über Urheberpersönlichkeitsrechte."*（条番号の括弧は Check 471 が本ドシエの節と取り違えるので省いた。全文は写しに在る） —— 法が許すと名指す 4 つの形は、ACD の 4 つの層に当たる: 利用権の付与（§4）、債権的な同意（§12.2 の consent と、§2.3 の段の schlichte Einwilligung の近く）、利用権についての合意（§5 の不行使の約束）、39 条の人格権についての取引（§12.2・上の §12.2 の段）。**不確実性が狭まる向き**: §3 が効かない法域の代表であるドイツで、§4・§5・§12.2 の形が法の列に在ることが、条文で言える。**残ること**: 「債権的な」同意と合意は契約として成立して初めて働くので、知らない受け手（§2.3 の段）と、包括的な事前の同意の限界（14 条の段）は、この条では閉じない。

**同じ構造（放棄・許諾・不行使の約束）を、ドイツの弁護士が既に読んでいる —— 上の段の「我々の読み」の 3 つが、公開された法律家の意見で裏づけられる（2026-11-16 追記・portfolio-30・portfolio-2f が取得・`rounds/2026-11-16-kreutzer-cc0-german-law-analysis-snapshot.txt`）**: Till Kreutzer 氏（ベルリンの弁護士・2011 年頃・CC0 のドイツ法上の分析・McCoy Smith 氏が 2020 年の Unlicense の審査で引いた）。
(1) **§3 は効かない（上の段と同じ）**: *"A waiver of the author's right as such is not valid under German copyright law."* —— 根は UrhG 29 条 1 項（上の段の写し）。
(2) **§4 の形は効く（狭まる向き）**: *"The bottom line is that the CC0 license fallback is – according to my opinion – legally effective."*、さらに *"public domain licenses (which"* *"cannot be interpreted as a waiver of rights under the German copyright, see above) are reinterpreted as"* *"unconditional, unlimited, non-exclusive (i.e. public) licenses"* が学説の通説だと書く —— 許諾の条が無くても公の許諾に読み替えられる。ACD の §4 は fallback でなく独立に立つ（§4.4）が、この読み替えの通説は同じ向きに働く。
(3) **§5 の不行使の約束は有効（狭まる向き・§2.3 の段と §18.2 の §5.1 の ③ の一部を閉じる）**: *"pactum de non petendo that would prevent him from enforcing these rights anyway."*（*"valid and legally binding"* と評する）。29 条 2 項が許す *"Vereinbarungen"* の形に、弁護士の意見が当てはめた。
(4) **§12.2 の包括的な同意の限界（上の §12.2 の段の「確かめていない」を一部埋める）**: *"According to the prevailing opinion among the German commentators global and unrestricted disclaimers"* *"about moral rights positions are invalid."* —— 包括的・無制限の人格権の放棄は通説で無効。その効果がライセンス全体に及ぶかを述べる続きの文は、取り出しの窓の外で取れていない。§12.2 は放棄でなく約束と同意で、§12.3 が the Work に限るので「無制限」より狭いが、当たるかは確立していない。
**逆側**: 1 人の弁護士の 2011 年頃の意見で、判決でも制定法でもない。2021 年の UrhG の改正（DSM 指令の置き換え）の後に読み直された記録は見ていない。ACD の §4.4 は fallback でない点で CC0 と構造が違う。

**§14.2・§15.2 と BGB 306 条 —— 約款と読まれた場合、無効な条項は縮められず、法律の規定が代わる（2026-11-18 追記・portfolio-30・portfolio-9b の台帳の依頼・条文は `rounds/2026-11-18-bgb-306-gesetze-im-internet-snapshot.txt`・我々の読み）**: 306 条 2 項 *"(2) Soweit die Bestimmungen nicht Vertragsbestandteil geworden oder unwirksam sind, richtet sich der Inhalt"* *" des Vertrags nach den gesetzlichen Vorschriften."* —— 無効な約款の条項の代わりは法律の規定で、条項を有効な限度まで縮めて残すのではない（その縮減の禁止は連邦通常裁判所の判例で、判決は取得していない）。**§15.2 への当たり方（狭まる向き）**: §15.2 の第 2 文（改められなければその法域で切り離し、残りは効く）は、306 条 1 項 *"(1) Sind Allgemeine Geschäftsbedingungen ganz oder teilweise nicht Vertragsbestandteil geworden oder"* *" unwirksam, so bleibt der Vertrag im Übrigen wirksam."* と同じ向きで、法律が既に与える結果を述べている。第 1 文（改め）は約款には当たらず、306 条 2 項が代わる。**§14.2 への当たり方**: *"limited to the greatest extent that law permits"* は縮減の形で、約款と読まれれば効かず、責任は法律の規定に戻る —— 贈与と読まれれば BGB 521 条（故意と重過失のみ・上の段）、そうでなければ一般の規定。T82 の除外は、外す範疇を名指しているので、この縮減に頼らない。**確立していないこと**: ACD が約款か（305 条 1 項・上の段）。306 条 3 項（契約の残りに拘束されることが一方にとって酷なら契約全体が無効）が、無償の付与で働く場面は考えにくいと読むが、確かめていない。

## 4. フランス（人格権が最も強い）

**問い**: 人格権は永久・不可譲・時効にかからないのではないか。

**本文の手当て**: §12.1 →（放棄不能なら）§12.2 の不行使の約束 / §12.3（Work 限定）/
§12.4（死後に行使しうる者まで）/ §12.5（**虚偽の帰属に対抗する利益は残す**）/ §12.6（可分）。

**確立していないこと**: 不行使の約束が人格権について有効かは争いがありうる。**§12.5 で 虚偽帰属への対抗利益を残しているのは、全部を捨てさせない設計だが、それで足りるかは 助言を得ていない。** 条文で言える所（2026-11-16・portfolio-30）: 知的財産法典の第 L121-1 条は *"L'auteur jouit du droit au respect de son nom, de sa qualité et de son oeuvre."* —— 名前の尊重は権利の 3 つの柱の 1 つとして名指されており、§12.5 が残す偽の帰属への対抗は、その柱の 1 つにそのまま当たる。残る 2 つ（qualité と oeuvre）は §12.2 の約束と同意の下に在り、ソフトウェアでは L121-7 が法の側で狭める（上の段）。条文の写しは `rounds/2026-11-16-cpi-l121-1-l121-7-legifrance-snapshot.txt`。

**撤回の条文（2026-11-08 追記・Légifrance で原典）**: フランスには人格権としての撤回権がある。
L121-4 は *« Nonobstant la cession de son droit d'exploitation, l'auteur, même postérieurement à la
publication de son oeuvre, jouit d'un droit de repentir ou de retrait vis-à-vis du cessionnaire. »* と
定め、行使には相手方への事前の補償を要する。**ソフトウェアは外れる**: L121-7 は *« Sauf stipulation
contraire plus favorable à l'auteur d'un logiciel, celui-ci ne peut : »* と始まり、その 2° が
*« Exercer son droit de repentir ou de retrait. »* である。**データセットや文書の Work には L121-4 が
残る**ので、§2.2 の irrevocable はそこで無条件には立たない。**有利な面**: L122-7-1（2006 年創設）は
*« L'auteur est libre de mettre ses oeuvres gratuitement à la disposition du public »* と、無償で公衆に
提供する自由を明文で認める。**確立していないこと**: 無償・非独占で誰にでも与えた許諾の受領者が
L121-4 の *cessionnaire* に当たるか。L121-4 の本文は、取得の道具が断片で返したものを繋いだもので、
1 か所の句読点が欠けている（25 が 2026-11-08 に取得）。

---

**§8.2・§2.2 と贈与の撤回 —— フランスでは撤回の事由が法律で限られ、§8.2 が偽になる範囲は狭い（2026-11-16 追記・portfolio-30・portfolio-50 の依頼・条文は `rounds/2026-11-16-code-civil-931-953-955-957-960-legifrance-snapshot.txt`・我々の読み）**: 民法典 953 条は、生存者間の贈与の撤回を *"pour cause d'inexécution des conditions sous lesquelles elle"* *"aura été faite, pour cause d'ingratitude, et pour cause de survenance d'enfants."* の 3 つに限る。ACD に当てると: (i) 条件の不履行 —— ACD は条件を課さない（§10.1）ので当たらない。(ii) 忘恩 —— 955 条が 3 つの場合（*"1° Si le donataire a attenté à la vie du donateur ;"*、*"2° S'il s'est rendu coupable envers lui de sévices, délits ou injures graves ;"*、*"3° S'il lui refuse des aliments."*）に限る。§8.2 が名指す受け手の特許の訴訟はどれにも当たらない。当たりうるのは、受け手が Dedicator に重い犯罪などを犯した場合で、その受け手に対してだけ、1 年以内に（957 条）。(iii) 子の出生 —— 960 条は *"si l'acte de donation le prévoit"* に限る。ACD は定めないので当たらない。**前提がさらに狭める**: 931 条は *"Tous actes portant donation entre vifs seront passés devant notaires dans la forme ordinaire des contrats ;"* *"et il en restera minute, sous peine de nullité."* —— 公証の無い ACD は、方式の上では生存者間の贈与として成立しにくい。判例が方式を求めない手渡しの贈与（don manuel）や間接の贈与に当たるかは、確かめていない。**結論の向き**: ドイツ（§3 の段・530 条は「重い非行」と開いた語）よりフランスの方が、§8.2 の言い切りが偽になる範囲は狭い。**逆側**: 「重い犯罪」に当たる行為をした受け手に対しては、贈与と読まれる限り、§8.2 の *"on any ground"* は偽になる。

**§12.2・§12.4 と CPI L121-1・L121-7（2026-11-16 追記・portfolio-30・portfolio-2f の振り分け・条文は `rounds/2026-11-16-cpi-l121-1-l121-7-legifrance-snapshot.txt`・我々の読み）**:
(1) **フランスは 1.0〜1.3 の §12.2 の「inalienable」の法域に当たる**（1.4 草案の §12.2 は T101 で引き金を持たず全法域で働くので、当たるかを問わない）。L121-1 は *"Il est perpétuel, inaliénable et imprescriptible."* —— §12.1 の放棄は当たらず、§12.2 の不行使の約束と同意が働く側になる。**残る不確実性**: 一般的で事前の、将来のあらゆる改変への同意が、尊重を求める権利（*"droit au respect de son nom, de sa qualité et de son oeuvre"*）の核に届くかは、ドイツの 14 条と同じく確立していない。届かない部分は §12.6 と §15.2 が受ける。
(2) **ソフトウェアでは法律そのものが狭めている（不確実性が狭まる向き）**。L121-7 は *"Sauf stipulation contraire plus favorable à l'auteur d'un logiciel, celui-ci ne peut :"* *"1° S'opposer à la modification du logiciel par le cessionnaire des droits mentionnés au 2° de l'article L. 122-6,"* *" lorsqu'elle n'est préjudiciable ni à son honneur ni à sa réputation ;"* —— ソフトウェアの著作者は、名誉や声望を害さない改変に反対できない。§12.2 の約束は、ソフトウェアについては法が既に与える結果と同じ向きにある。**逆側**: 1° は「権利の譲受人（cessionnaire）」の改変についての文で、非独占の公衆への許諾の受け手が cessionnaire に当たるかは確かめていない。名誉や声望を害する改変は、法がなお著作者に残す。
(3) **§12.4 と相続人**: L121-1 は *"Il est transmissible à cause de mort aux héritiers de l'auteur."*、*"L'exercice peut être conféré à un tiers en vertu de dispositions testamentaires."* —— 死後に権利を行使するのは相続人か遺言で指定された者で、§12.4 が名指す *"any person entitled to exercise or enforce Moral Rights in the Work after the Dedicator's death"* はこの 2 つに当たる。相続人が被相続人の生前の約束に拘束されるかは、権利が一身専属であることとの関係で確立していない（日本の 60 条ただし書のような、著作者の意思に寄せる明文は、取得した条には無い）。

**§15.4（英語が正文）とトゥーボン法（2026-11-18 追記・portfolio-30・portfolio-9b の台帳の依頼・条文は `rounds/2026-11-18-loi-toubon-94-665-art-2-5-legifrance-snapshot.txt`・我々の読み）**: 5 条は、公法人か公役務を担う私人が当事者の契約について *"Quels qu'en soient l'objet et les formes, les contrats auxquels une personne morale de droit public ou une personne privée"* *"exécutant une mission de service public sont parties sont rédigés en langue française."* とする —— フランスの公的機関が ACD を当てる、または受け取る場面では、英語だけの本文はこの条に当たりうる。2 条は財・製品・役務の *"la désignation, l'offre, la présentation, le mode d'emploi"* と保証の条件にフランス語を求める。**狭まる向き**: 5 条は公法人と公役務の当事者に限られ、私人どうしには及ばない。2 条は製品や役務の表示と保証についての条で、無償の公の許諾がそれに当たるかは疑わしく、当たっても 1.4 草案の §15.4（1.0 の §15.8）は翻訳を禁じていない（*"A translation is for convenience only"*）—— フランス語の翻訳を添えれば 2 条の要求は満たしうる。**確立していないこと**: 5 条の場面で、英語を正文とする §15.4 そのものが効くか（翻訳が正文と食い違ったときにどちらが勝つか）。もう 1 つは採用者の側の問い（portfolio-9b の指摘・2026-11-18）: ACD を当てた製品や役務をフランスの消費者へ出す採用者にとって、2 条の *"la description de l'étendue"* *"et des conditions de garantie d'un bien, d'un produit ou d'un service"* に、§13 の保証の否認が当たるか —— 当たるなら、その採用者はフランス語の訳を添える必要があり、それは採用者の義務で、Dedication が受け手に課す条件ではない（§10.1）。`ADOPTING.md` に書くかは 50 の判断。

## 5. 米国

**問い**: 著作権法に放棄の手続が無いのに、public domain に置けるのか。倒産したらどうなるか。

**本文の手当て**: §4.4（ライセンスが独立）/ §2.5（禁反言）/ §2.9 / §2.8（管財人は「譲受人」に当たると明示）。**版の注（2026-11-16）**: 1.0 の §2.9 は「適用の時点で履行が完了し、継続する義務が無いので未履行双務契約ではない」と分類まで言い切ったが、その分類と結果の言い切りは欠陥として外した（errata E5・E30）。1.4 草案の §2.9 は、倒産の手続や管財人の行為を条件にしないことと、管財人が §2.8 の移転先であることだけを述べる。

**§2.9 の位置づけ**: 未履行双務契約であれば管財人が拒絶しうるので、11 U.S.C. §365(n) のような保護規定に頼る構図になる。**2019 年の最高裁判決がこの構図を狭めた**（2026-11-16・portfolio-2f が取得・`rounds/2026-11-16-us-bankruptcy-tempnology-and-365n-snapshot.txt`）: *Mission Product Holdings v. Tempnology* は *"Rejection of a contract—any contract—in bankruptcy operates not as a rescission but as a breach"*、*"Such an act cannot rescind rights that the contract previously granted"* と判示した。米国では、(i) 受領者に義務の無い ACD の許諾は「双方に履行が残る」契約に当たらないと読め（我々の読み・判決は ACD のような付与を扱っていない）、(ii) 当たっても拒絶は与えた権利を消さない —— §365(n) の選択に頼らずに。

**確立していないこと**: (i) の分類を裁判所が採るか。国境を越える場合の *Jaffé v. Samsung* の衡量（#178。判決は事案の事実と 4 日の証拠調べに依って、§1522(a) の衡量で §365(n) を米国の特許の受け手に及ぼした破産裁判所の裁量を是認し、§1506 の公序の例外がその衡量を締め出さないとした —— 一般の規則ではなく裁量の判断で、特許の許諾について、Tempnology（2019）より前の判断・`rounds/2026-11-19-us-jaffe-v-samsung-4th-cir-2013-snapshot.txt`）。米国の外では、ドイツの倒産法を 30 が読んだ（§3 の §2.9 の段・`rounds/2026-11-16-inso-103-129-134-143-gesetze-im-internet-snapshot.txt`）: 管財人の履行選択（103 条）は、受け手が何も負わないので当たりにくいが、無償の給付の否認（134 条）は申立ての前 4 年の内の付与に当たりうる —— 米国と違い、ドイツでは「与えた権利は消えない」とまでは言えない（2026-11-16 に予定の書き方から結果へ書き換えた・portfolio-50）。

**§8 と §2.8 —— 特許の移転と、ドイツの承継保護・米国の登録（2026-11-20 追記・portfolio-50・条文は `rounds/2026-11-20-patent-usc-patg-berne-trips-snapshot.txt`・我々の読み）**: ドイツ PatG 15 条 3 項 *"Ein Rechtsübergang oder die Erteilung einer Lizenz berührt nicht Lizenzen, die Dritten vorher erteilt worden sind."* —— §8.1・§8.4 の許諾は、後に特許を譲り受けた者に対しても残る（§2.8 が言うことを法が既にする）。米国 35 U.S.C. 261 条は *"An interest that constitutes an assignment, grant or conveyance shall be void as against any subsequent purchaser"* *"or mortgagee for a valuable consideration, without notice, unless it is recorded in the Patent and Trademark Office"* —— 公への非独占の許諾がこの *interest* に当たるかは判例を読んでいない（**確立していないこと**・問い 1 (j)）。侵害の行為は 271 条 (a) が *makes, uses, offers to sell, or sells* と *imports* を挙げ、§8.1・§8.4 の列挙（T94）はそれを含む。条約の側では、TRIPS 28 条 1 項 (b) が方法の特許を *"the product obtained directly by that process"* に及ぼし、特許の学習方法で直接得たモデルも §8.4 の語の内に在る。

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

**本文の手当ては §15.4 である**（1.1 / 1.2 草案では §15.2。無効なら当該法域についてのみ改釈・可分）。
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

### 5c. リスト自身が同じ条文を「心配すべき橋」と呼び、同じスレッドで献呈の効果も述べている（2026-09-27 追加）

**5a は §203 を statute から見つけた。** 2026-09-27 に `license-discuss` の
"Can copyrights be abandoned to the public domain?"（2012-08・全 34 通・
`rounds/2012-08-license-discuss-copyright-abandonment-observed-1of3.txt` ほか）を読むと、
**同じ条文が、リスト上で実務弁護士の口から名指しされている。**

**🔴 不利 —— §203 は「リストが知っている危険」である。**

Lawrence Rosen 氏（オープンソース法の実務家）は、人格権の危険を論じる当時の
License Committee 委員長 Russ Nelson 氏に対してこう返している:

> *"If you want to worry about copyright law, **consider 17 USC 203**. [1] Tell me what you
> experience as you drive over that bridge...."*（2012-08-18）

Nelson 氏の返事は *"I'll tell you in 35 years."* ——**35 年という期間を、両者とも正確に
理解したうえでの応酬である。**

**5a の評価は変わらない**（§4 は licence なので §203 に届き、§15.4 / 次版 §15.2 が縮退を受ける）。
**変わるのは位置づけだけである** —— **これは我々が文献から掘り出した理屈ではなく、
リストの住人が「本当に心配すべきもの」として名前で呼んでいる条文**である。
**審査で持ち出される可能性は、その分だけ高い。**

**🟢 有利 —— 放棄の可否が不確かでも、明確な献呈は効果を持つ（§2.5 の外からの裏づけ）**

Tom Callaway 氏（当時 Fedora の法務窓口）は、Red Hat Legal との検討結果としてこう述べている:

> *"if someone is **explicitly and clearly abandoning** their copyright on a work (as in CC-0,
> for example), treating that work in good faith as being in the public domain presented a
> **very minimal amount of risk**, especially since **such a declaration, were it to go to
> trial, would likely limit the effectiveness of the copyright 'holder' suing for
> infringement**."*（2012-08-14）
>
> *"We're **not attempting to pronounce that public domain declarations are legally possible
> everywhere**, but we are saying that … where there is **clear intent** from a copyright
> holder for unrestricted permissions on works, we feel it is safe for us to treat them as if
> they were in the public domain."*（同 08-14）

**これは ACD-1.0 §2.5（estoppel）が本文の中で述べていることの、外からの裏づけである** ——
**「放棄が有効か」を決めなくても、明確な意思表示は、後から翻す側の立場を弱める。**
**しかも述べているのは、承認済みライセンスを大量に扱う頒布者の側**であり、
**採用を判断する実務者が実際に使っている物差しでもある。**

**⚠ 逆側 3 つ。** **(1)** Callaway 氏は *"very minimal"* であって *"none"* とは言っていない。
**(2)** 述べているのは Fedora / Red Hat の**採用判断**であって、**OSI の承認基準ではない。**
**(3)** 2012 年の発言で、**§203 の 35 年は当時まだ誰にとっても将来の話だった**
（1978 年以降の grant が最初に終了可能になるのは 2013 年以降）。

**2026-11-12 の追記 —— 同じ点は 2007 年に、*perpetual* の語について述べられていた。** "Question on OSD #5"（`license-discuss` 2007-11・54 通・`rounds/2007-11-license-discuss-question-on-osd-5-perpetual-observed.txt` に 3 通）で、John Cowan 氏は Rick Moen 氏が挙げた 3 つの試験について *"since the GPLv2 nowhere says it is perpetual (nor can any U.S. copyright license be truly perpetual given the provisions in U.S. law for license recapture), it obviously violates the second test you mention"* と書いた（2007-11-27）。ACD の §4.1 と §8.1 は *"irrevocable, perpetual"* と書くので、この括弧の中の文は ACD の *perpetual* の語にそのまま当たる（*irrevocable* の側は 5a が扱う）。5a の読み（§4 は合衆国では §203 に服し、§15 が縮退を受ける）と同じで、新しい不利な事実ではない。**逆側**: Cowan 氏は同じスレッドで自分を法律家でないと書いており（*"IANAL"*・2007-11-22）、文は試験の当てはめについての傍論である。同じスレッドで Arnoud Engelfriet 氏（欧州の弁理士と署名）は、ライセンスの外の NDA について *"the software still is BSD. I just can't distribute it."* と書いた（2007-11-24）。ACD の外で受領者が結ぶ約束は ACD を変えない、という §10.1 の読みと同じ向きである。

**同じ追記の逆側（2003）**: list の弁護士は 4 年早く、*perpetual* の語を残すべきだと書いていた。Lawrence E. Rosen 氏は OSL の期間の語について *"I hope that parties contracting under the Open Software License (OSL, www.rosenlaw.com/osl2.0.html) really mean "perpetual" as "until the end of time."  The fact that copyright law provides an escape mechanism to protect against unequal bargaining power at the beginning of a copyright term shouldn't prevent parties from saying "perpetual" when they honestly, sincerely, presently intend it to be forever."* と書き、*"Since the 35-year option-to-terminate rule (17 U.S.C. 203) doesn't even apply to a work made for hire, is it practical to worry about it in most software licenses?"* と問うた（`license-discuss` 2003-08-27・`rounds/2003-08-license-discuss-osl-perpetual-and-section-203-observed.txt`）。同じ会話で Ian Lance Taylor 氏は、著作権が切れると OSL も切れることを *"actually a drawback, not a benefit"* と書いた。ACD の *perpetual* は、Rosen 氏の言う「今の意図」の表明として読める。**逆側の逆側**: 職務著作に §203 が及ばないのは雇用者の側の著作物で、個人が書いて ACD を当てた著作物には及ぶ。AI が生成した素材の著作者が誰かという問い（B14・`jurisdictions.md` の別の節）とは別である。Rosen 氏の文は 2003 年の実務家の見通しで、判断ではない。

### 5b. 人格権（17 U.S.C. §106A・VARA）—— §12.1 は米国では形式要件を満たさない。だから §12.2 がある

**2026-09-19 に原典で確認した**（`https://www.law.cornell.edu/uscode/text/17/106A`）:

> *"The rights conferred by subsection (a) **may not be transferred**, but those rights may be waived
> if the author **expressly agrees to such waiver in a written instrument signed by the author**.
> Such instrument shall **specifically identify the work, and uses of that work**, to which the
> waiver applies …"*（§106A(e)(1)。**2026-11-01 に冒頭の 1 句を補った** —— 旧版は *"those rights
> may be waived"* から引いており、下の結論が依拠する当の句を落としていた）

**§12.1 の放棄は、この形式を満たさない。** リポジトリに置かれた LICENSE file は
**著作者が署名した書面ではなく**、**用途を特定してもいない。**
**したがって米国では §12.1 は放棄として成立しないと考えるのが素直である。**

**それは設計どおりである** ——§12.2 が *"Where the law of a jurisdiction provides that Moral Rights
are personal to the author, **inalienable**, or incapable of waiver, Section 12.1 does not apply …
and instead the Dedicator covenants not to exercise"* と述べており、**covenant には形式要件が無い。**

**⚠ 当たっているのは 3 つの語のうち *inalienable* である（2026-11-01 訂正）。** 旧版はここで
*"incapable of waiver"* を引いていたが、**VARA の権利は署名書面があれば放棄できる**ので、
その語には当たらない。§12.2 を発動させるのは §106A(e)(1) 冒頭の *"may not be transferred"*
（譲渡できない＝inalienable）である。**結論は変わらない** —— 3 語は「or」で並んでいるので
1 つ当たれば足りる —— が、**根拠に引く語を取り違えると、「放棄できるのだから §12.2 は働かない」
という反論にそのまま道を開く。** **1.4 草案（T101・2026-11-19）は引き金を無くし、§12.2 の約束と同意を全法域で §12.1 と並べたので、この語の取り違えの道は本文から消えた。** 1.4 草案の §12 を VARA と英国 CDPA に当てた検討（2026-11-01・
`ACD-1.4-CHANGELIST.md`）が気付いた。

**⚠ ただし射程を誇張しない。** **VARA が及ぶのは *works of visual art* だけ**であり、その定義は
絵画・素描・版画・彫刻・展示目的の限定部数の写真に限られ、**映画その他の audiovisual work は
定義から明文で除かれている。** **ソフトウェアは対象外である。**
**したがって ACD の典型的な対象物について、VARA はそもそもほとんど発動しない** ——
**この節は「米国には人格権の問題がある」ではなく、「あるとしても §12.2 が受け止める形になっている」
ことを示すためにある。**

**⚠ そして §12.2 自体の有効性は別問題である。** 形式要件が無いことと、
**covenant が裁判所で執行されることは同じではない。** ここは外部の法律意見が要る（register B1）。

---

### 5d. list の法学の教員は 2000 年に、放棄の抗弁が 1976 年法の下で生きているかを疑った（2026-11-12 追加）

`license-discuss` 2000 年 8 月の "The different between GPL and non-license"（8 通・`rounds/2000-08-license-discuss-gpl-and-non-license-observed.txt`）。上の **問い**（著作権法に放棄の手続が無いのに、public domain に置けるのか）を、法学の教員が list で直接扱った、読んだ中で最も古い記録である。Rod Dixon 氏は同じ年の通に *"Visiting Assistant Professor of Law"*（Rutgers University Law School - Camden）と署名している。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| 公有に置くかを著作権者は選べない（原文は *choice* を強調）—— *"as to whether to put/transfer/cede a work to the public domain."*、*"The public domain status of a work operates as a matter of law."* | Rod Dixon 氏 2000-08-10 | **不利な面。** 公有は法の作用で生じる状態で、著作権者が選んで置けるものではない、という立場。ACD の §3 はまさにその選択の宣言である |
| *"The continued vitality of the defense of abandonment is in serious doubt except for, perhaps, copyright disputes occurring under the pre-1976 Copyright Act"*、訴えないことで権利を手放すことはできても（原文は *abandon* を強調）*"this is not the same as public domain."* | Dixon 氏 2000-08-10 | **不利な面。** 放棄が働くのは 1909 年法の下の争いぐらいで、いまの法の下では、訴えないことで放棄に近いことはできても公有にはならない、という見通し。ここで疑われているのは侵害訴訟で被告が持ち出す放棄の抗弁で、§3 の献呈の宣言とは場面が違う。だが §3 が受領者を守るのは、著作権者が訴えたときに受領者が §3 の放棄を持ち出す場面なので、抗弁が疑われるなら §3 も合衆国では同じ疑いを受けうる（2026-11-12 に portfolio-aa の指摘で一段を足した） |
| *"There is nothing within the US copyright statute which prevents an author or copyrightholder from ceding rights to a work."* | Karsten M. Self 氏 2000-08-10 | 逆側。制定法に禁じる規定は無い、という反論。同氏は法律家でない（*"I claim no authority in this area"*） |
| *"the U.S. Copyright office accepts and registers affidavits by the author of a work that the author has abandoned copyright. That suggests that the defense of abandonment is still possible."* | John Cowan 氏 2000-08-10 | 逆側。著作権局が放棄の宣誓書を受け付けて登録している、という事実からの推論。Dixon 氏はその後の通で、訴えを起こすこと自体が放棄の意思の主張を弱めると答えた |
| *"I believe there are doctrines under contract law -- estoppal, possibly -- which act as a bar from granting broad rights to something at one point in time then reversing yourself later."* | Self 氏 2000-08-10 | ACD の §2.5 と同じ向きの手当て。同氏は自分に権威が無いと書いた |

**読み。** Dixon 氏の見通しが正しければ、§3 は合衆国では働かず、受領者を支えるのは §4 の許諾と §5 の約束である。ACD が §3 と §4 を並べ、§4.4 で §4 を §3 から独立させているのはこのためで、B4 と B5 の答えはこの不利な読みを前提にしている。**ただしそれは §4 と §5 が働くことを示さない** —— §4 は合衆国では 203 条の終了権に服し（5a）、対価の無い許諾が撤回されうるか（`against.md` #324・`QUESTIONS-FOR-COUNSEL.md` 問 1 (i)）、署名の無い許諾が後の譲受人に優先するか（問 1 (j)）が残る。

**この節が establish しないこと。** 2000 年の 1 人の法学の教員の見通しで、判例でも OSI の判断でもない。Dixon 氏が挙げた理由（1976 年法で公表と表示の方式が要らなくなったこと、訴えることが放棄の意思と矛盾すること）は、その後の判例に当てていない。Cowan 氏が挙げた CNI の 1994 年の投稿は開いていない。同じ月の "Abandonment" での同氏の文（公有に入った作品はそこに留まる）は、公有に入れば戻らないという別の点で、§3 が効くかどうかとは別である（`review-readings.md` §1.191）。

**§1.9 —— 米国の職務著作でも寄与の権利は使用者に帰属する（2026-11-27 追記・portfolio-72・`rounds/2026-11-19-us-17-usc-101-wmfh-106-201-snapshot.txt`・我々の読み）**: 17 U.S.C. §101 は職務著作を *"a work prepared by an employee within the scope of his or her employment"* と定め、§201(b) は *"In the case of a work made for hire, the employer or other person for whom the work was prepared"* … *"is considered the author for purposes of this title, and, unless the parties have expressly agreed"* … *"otherwise in a written instrument signed by them, owns all of the rights comprised in the copyright."* と言う。**1.4 への当たり方**: 社員が職務で出した寄与の権利は使用者のもので、§1.9 の *"by or on behalf of the person"* の提出として使用者が Dedicator になる読みは日本の 15 条（第 2 節の段）と同じ向きである。委託の著作物（§101 の (2)）は列の類型で、かつ署名した書面の合意があるときだけ職務著作になるので、外部の請負人が出した寄与は普通は請負人自身の権利で、§2.6 / 1.5 草案 10.4 の「作って出した人」が Dedicator になる。**確立していないこと**: 社員の寄与が *"within the scope of his or her employment"* か（業務外の時間に書いた OSS への寄与）は事実の問いで、ACD の文では決まらない —— 10.4 が「作って出した人」と「権限を与えた人」の両方を名指すのは、どちらが持っていても献呈が効く形にするためで、この問いに答えるものではない。

**§2.9 —— 倒産法の「知的財産」の定義に、ACD が与えるものの 2 つが入り、1 つが入らない（2026-11-27 追記・portfolio-72・`rounds/2026-11-19-us-11-usc-101-35a-intellectual-property-snapshot.txt`・我々の読み）**: 11 U.S.C. §101(35A) は *"The term “intellectual property” means—"* として *"(A) trade secret; (B) invention, process, design, or plant protected under title 35; (C) patent application;"* *"(D) plant variety; (E) work of authorship protected under title 17; or"* *"(F) mask work protected under chapter 9 of title 17;"* を挙げ、*"to the extent protected by applicable nonbankruptcy law."* で閉じる。**1.4 への当たり方**: §4（著作権の許諾）は (E)、§8（特許の許諾）は (B) と (C) に当たるので、§365(n) の保護の対象を決めるこの定義の内にある（§365(n) の本文と *Tempnology* は上の §2.9 の位置づけの段と `rounds/2026-11-16-us-bankruptcy-tempnology-and-365n-snapshot.txt`）。列に無いのは商標と sui generis のデータベース権で、ACD は商標を与えない（§11.1・1.5 草案 6.2）ので前者は欠けない。データベース権は米国に在る権利ではないので、米国の倒産の手続で問われない。§2.9 は保護の規定に頼る前に、倒産の手続や管財人の行為を条件にしないことを述べ、管財人を §2.8 の移転先とする —— 定義の内に在ることは、§2.9 の文が効かない場合の受け皿が在ることを示すにとどまる。**確立していないこと**: (1) *"to the extent protected by applicable nonbankruptcy law"* は、§3 の放棄が効いて公有になった部分には保護すべき権利が残らないことを示す —— 放棄が効けば拒絶の対象が無く、効かなければ §4 の許諾が (E) として残る、という 2 段の読みは我々のもので、裁判所の確認は無い。(2) **定義の内でも、§365(n) が働くのは未履行の契約を拒絶したときである**（7f の反例・2026-11-27）。*Tempnology* が引く定義は *"performance remains due to some extent on both sides"*（上の段の写し）で、受け手に義務の無い ACD（§10.1）は未履行でないと読む側が強い —— そうなら拒絶そのものが当たらず、(35A) の内か外かは働かない（受け手に有利な向き）。ただし未履行でないと言い切った 1.0 §2.9 の文は errata E5・E30 で外した欠陥で、Dedicator の側の約束（§5・§8.6）を未履行の義務と見る裁判所はありうる。定義の内に在ることは、その場合の受け皿にとどまる。(3) (A) の営業秘密は ACD が与えない（Covered Rights に名指さない）が、1.4 §5.1 第 2 文と 1.5 草案 2.5(d) の一般の約束は受け手への営業秘密の請求に届く（`ACD-1.5-CLARITY-TRIAL.md` §15）—— 約束が §365(n) の「知的財産の許諾」に当たるかは確かめていない。

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

- **§1.2 の Work は *audiovisual material* を含む**（1.1 / 1.2 草案では §1.3）。 映画や録音物へ適用されれば射程に入りうる。
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

**§13・§14 —— 2 つの EU 指令は、無償の自由なソフトウェアを先に外している（2026-11-16 追記・portfolio-2f が取得・`rounds/2026-11-16-eu-product-liability-and-digital-content-foss-snapshot.txt`）**: 製造物責任指令 2024/2853 の第 2 条 2 項は、商業活動の外で開発・供給される自由でオープンソースのソフトウェアに適用しない。デジタルコンテンツ指令 2019/770 の第 3 条 5 項 (f) も、価格も限られた目的以外の個人データも無い FOSS を外す。無償の Dedicator は、§13・§14 が効くかを問う前に、2 つの指令の外にいる。ドイツの置き換えの側は §3 の段（BGB 327 条 6 項 6 号）。**逆側**: 会社が商業活動の過程で ACD を当てれば 2024/2853 が適用され、同指令の第 15 条により、§14 は製造物責任を契約で制限・排除できない。ACD のデータや文書の部分が指令の「ソフトウェア」に当たるかは、指令から決まらない。

**§1.5 —— 報道出版者の権利（DSM 指令 15 条）は Covered Rights の「似た権利」に入り、記事の著者の権利は残る（2026-11-27 追記・portfolio-72・`rounds/2026-11-19-eu-dsm-2019-790-art-15-snapshot.txt`・我々の読み）**: 15 条 1 項は加盟国に *"publishers of press publications established in a Member State"* へ *"for the online use of their press publications by information society service providers"* の権利を与えさせ、2 項は *"The rights provided for in paragraph 1 shall leave intact and shall in no way affect any rights provided"* … *"for in Union law to authors and other rightholders, in respect of the works and other subject matter incorporated"* … *"in a press publication."* と言う。**1.4 への当たり方**: §1.5 の Covered Rights は *"rights in performances, broadcast and recording rights, sui generis database rights, rights against unfair extraction, and any right of similar effect"* を挙げ、報道出版者の権利は著作権の隣接の権利として *"any right of similar effect"* に入ると読む（1.5 草案 1.6 は *"any similar right"*）。出版者が ACD を当てれば、出版者のこの権利は §3 と §4 で手放され、情報社会サービスの提供者への請求は §5.1 が止める（模型の学習のための取得がこの権利の及ぶ「online use」に当たるかは各国の実装で、ここでは言わない・7f）。2 項により、記事に入った著者の著作権は出版者の献呈で動かない —— §1.4 の *"to the extent that person or entity holds or may hold Covered Rights, Moral Rights, or patent claims in it"* と同じ限りで、出版者の献呈は著者の権利に及ばない（1.5 草案の §6.1 の *"affects no right held by a person other than the Dedicator"*）。**逆側・確立していないこと**: (1) 15 条の権利は加盟国の法で実装され、名と範囲が国ごとに違う（ドイツの Presseverleger の権利など・写しは指令だけ）ので、「似た権利」に入るかは国の実装の語で決まる。(2) 写しは 15 条の 1 項と 2 項だけで、権利の期間・私的利用や hyperlink や短い抜粋の例外・著者への収入の分配を定める他の項は取っていない —— 出版者が献呈して収入が無くなるとき、著者の分配の請求（出版者に対する・ACD の外の契約の問い）と食い違いうるかは、その項を取ってから読む（7f の反例・2026-11-27・出版者が採用をためらう事情なら B2 の側）。(3) 受け手から見ると、出版者の ACD は記事の著者の権利を外さないので、著者が別に許諾していない記事を使う人は著作権の側の許しを別に要する —— ACD の通知が記事全体を覆うように見える危険で、§1.4 の限りと 1.5 草案の §6.1 の *"is no representation that the Work is free of such rights"* が受ける。

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

**§14.1（T82 の後）と UCTA —— 規制は事業上の責任に限られる（2026-11-16 追記・portfolio-30・条文は `rounds/2026-11-16-ucta-1977-s1-s2-legislation-gov-uk-snapshot.txt`・我々の読み）**: UCTA 1 条 3 項は、2〜7 条を *" only to business liability, that is liability for breach of obligations or duties arising—"* *"(a)from things done or to be done by a person in the course of a business (whether his own business or another's); or"* に限る。事業の外で無償に ACD を当てる個人の Dedicator には、2 条の規制がそもそも当たらない（不確実性が狭まる向き）。事業として当てる場合は 2 条 1 項 *"exclude or restrict his liability for death or personal injury resulting from negligence."* が当たり、2 項は他の損害の過失の責任の除外を合理性の要件に服させる。T82 の除外（法が除外を許さない死亡・人身の責任）は 1 項と同じ向きで、*"WHICH NOTHING IN SECTION 14 LIMITS"* が 1 項の「制限（restrict）」の禁止にも合う。**確立していないこと**: 2 項の合理性の要件を、無償の公の付与の免責が満たすか（費用を取らないことは合理性の側に働くと読むが、確かめていない）。消費者への通知は 2 条 4 項で消費者権利法 2015 の側に移る（`rounds/2026-11-16-consumer-rights-act-2015-s2-s61-s65-legislation-gov-uk-snapshot.txt`）。その Part 2 は *"This Part applies to a contract between a trader and a consumer."* と、通知については *"(b)purports to exclude or restrict a trader's liability to a consumer."* に限り、trader は *"a person acting for purposes relating to that person's trade, business, craft or profession,"* —— UCTA と同じく、事業の外の個人の Dedicator には当たらない。事業者が当てる場合は 65 条 1 項 *"A trader cannot by a term of a consumer contract or by a consumer notice exclude or restrict liability for death or"* *"personal injury resulting from negligence."* が当たり、T82 の除外と同じ向きにある。

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

**§12.2 が発動する根拠は s.94 である**（*"The rights conferred by Chapter IV (moral rights) are
**not assignable**."*・2026-11-01 に原典で確認）—— 英国の人格権は署名書面で放棄できるので
*"incapable of waiver"* には当たらず、当たるのは *"inalienable"* である（§5b の米国と同じ形）。

**§12.2 の不行使の約束は、この consent の形に写る。**
**米国（VARA）と同じ構図だが、英国のほうが着地が良い** ——**明文の consent 経路がある。**

**⚠ 確立しないこと**: §12.1 / §12.2 が英国法上 consent と評価されるかは**我々の読みであって
助言ではない**（register B1）。s.87(3) は waiver が *"subject to revocation"* とされうるとも定めており、
**撤回可能性の議論はここでは扱わない。**

---


**§2.8・§12.2・§2.5 と CDPA 87 条 3 項 4 項・90 条 4 項（2026-11-16 追記・portfolio-30・条文は `rounds/2026-11-16-cdpa-1988-s87-s90-legislation-gov-uk-snapshot.txt`・我々の読み）**:
(1) **§2.8（譲受人の拘束）は 90 条 4 項が裏づける（狭まる向き）**。*"A licence granted by a copyright owner is binding on every successor in title to his interest in the copyright,"* *"except a purchaser in good faith for valuable consideration and without notice (actual or constructive) of the licence"* —— 英国では許諾は承継人を法律で拘束し、外れるのは許諾を知らず、知りえなかった有償の善意の買主だけ。ACD は公開され、§16.2 の識別子が写しに付くので、「擬制された知（constructive notice）」の無い買主は考えにくいと読む（確かめていない）。§4 の許しが 90 条 4 項の licence に当たる限り、日本の 63 条の 2（§2b）と同じく、§2.8 は法が既にすることを述べる。
(2) **§12.2 は 87 条 4 項の下に在る（狭まる向き）**。*"(4)Nothing in this Chapter shall be construed as excluding the operation of the general law of contract or estoppel"* *"in relation to an informal waiver or other transaction in relation to any of the rights mentioned in subsection (1)."* —— 署名の無い放棄（§12.1 が 87 条 2 項に届かない場合）でも、人格権の取引には契約と禁反言の一般法が働くと法自身が書く。§12.2 の約束と同意は、まさにこの道。87 条 3 項 (a) は放棄が *"to works generally, and may relate to existing"* *"or future works"* に及びうるとし、包括的な形を法が予定している（§12.3 は ACD の約束を the Work に限るので、それより狭い）。**範囲の限り（2026-11-17 に直した・portfolio-30 自身の誤りの是正）**: 87 条は第 4 章（人格権）の条で、4 項の *"Nothing in this Chapter"* は人格権の取引についてだけ言える。§2.5（Dedication 全体の撤回の主張を止める）の対象は主に経済的な権利なので、87 条 4 項は §2.5 の足場にならない。英国での §2.5 の足場は判例法の約束的禁反言だけで、制定法の裏づけは無い。その禁反言が請求の根拠にならないことは、控訴院の Harvey v Dunbar Assets（2017）第 62 段落が *"it cannot alone confer positive rights on the promisee"* *"(often expressed by saying that the doctrine operates as a shield and not as a sword)"* と述べる（`rounds/2026-11-17-harvey-v-dunbar-2017-ewca-civ-60-promissory-estoppel-snapshot.txt`・保証の事件で、一般論として引く・2026-11-17 に Find Case Law から取得）。§2.5 は Dedicator の主張を止める盾として書いてあるので、剣にならないことはその働きを削らない（portfolio-2f の読み）。逆側: 盾は Dedicator の主張を止めるだけで、撤回の効力そのものを消すとは限らない。

**§12（人格権）と CDPA の人格権の章 —— ソフトウェアには表示と改変の権利が当たらず、残るのは偽の帰属の権利だけ（2026-11-20 追記・portfolio-30・オーナーの依頼で法令を分担して読んだ分・条文は `rounds/2026-11-20-cdpa-1988-s9-s78-s79-s81-s84-s94-legislation-gov-uk-snapshot.txt`・我々の読み）**:
(1) **表示と改変の権利はプログラムとコンピュータ生成物に当たらない（§12 の問いが法律の段階で大きく狭まる）**。79 条 2 項は表示の権利（77 条）について *"The right does not apply in relation to the following descriptions of work—"* *"(a) a computer program;"* … *"(c) any computer-generated work."*、81 条 2 項は改変に異議を述べる権利（80 条）について *"The right does not apply to a computer program or to any computer-generated work."* —— ソフトウェアの Work には、英国ではこの 2 つの人格権がもともと無く、§12.1 の放棄も §12.2 の約束も当たる先が無い。さらに 78 条 1 項は、表示の権利は *"unless the right has been asserted"* の限りで侵害されないとし、主張には署名ある書面などを要する（2 項）—— ACD はこれを主張しない。
(2) **残るのは偽の帰属の権利（84 条）で、プログラムの例外が無い**。84 条 1 項 *"(a)not to have a literary, dramatic, musical or artistic work falsely attributed to him as author, and"* —— プログラムは言語の著作物に当たるので、Dedicator は改変版を自分の作として出されることに、この権利で向かえる。2 項は偽の帰属の付いた写しを *"issues to the public"* する者、5 項は事業の過程でそれを持ち・扱う者を侵害者とする。
(3) **T122 の向きへの当たり方**: 英国のソフトウェアでは、人格権のうち実際に残るのは 84 条だけで、それは §11.3（偽の表示は Dedication の外）が守ろうとする利益と同じ —— (A)（§12.1 の放棄が 84 条にも及ぶ）なら、ソフトウェアについて英国で残る唯一の人格権を放棄させることになり、(B)（84 条は残す）なら §11.3 と揃う。加えて、87 条 2 項は放棄に署名ある書面を求めるので、署名の無い ACD の §12.1 は英国では放棄として働かず（87 条 4 項の契約・禁反言の道は残る・上の段）、(A) が実際に英国で手放させる力も弱い。
(4) **9 条 3 項**: コンピュータ生成物の著作者は *"the person by whom the arrangements necessary for the creation of the work are undertaken"*（§7a の段と同じ）—— コンピュータ生成物には 79 条・81 条の例外があるので、機械生成物（§1.8・§9）について英国で人格権が問題になる場面は、84 条の偽の帰属に限られる。
**確立していないこと**: 1.4 草案の §12 は「Moral Rights」を §1.2 で広く定めるので、英国のどの権利に当たるかは本文の語ではなく法が決める（上の読みは法の側の結論で、裁判所の確認は無い）。データや文書など、プログラムでない Work には 77 条・80 条が当たり、そこでは §12 の問いはそのまま残る。

**§7（データベース権）と §6（TDM）—— 英国のデータベース権は 1997 年の規則に在り、§7.2 と同じ線を法が引く（2026-11-20 追記・portfolio-30・オーナーの依頼で法令を分担して読んだ分・条文は `rounds/2026-11-19-uk-database-regulations-1997-cdpa-29a-snapshot.txt`・我々の読み）**:
(1) **置き場所**: 英国の独自データベース権は CDPA ではなく Copyright and Rights in Databases Regulations 1997 に在る —— 13 条 1 項 *"A property right ("database right") subsists, in accordance with this Part, in a database if there has been a substantial"* *"investment in obtaining, verifying or presenting the contents of the database."*、2 項は著作物であるか否かを問わない。オーナーが貼った外の AI のまとめは「CDPA がデータベース権を定める」と書いていたが、条文はこの規則（照合は 50 が 1 か所に記録する）。
(2) **§7.2 と規則の線が揃う（狭まる向き）**: 16 条 1 項は *"extracts or re-utilises all or a substantial part of the contents"* を侵害とし、2 項は *"the repeated and systematic extraction or re-utilisation of insubstantial"* *"parts of the contents of a database may amount to the extraction or re-utilisation of a substantial part of those contents."* —— §7.2 の *"the whole or any substantial part … repeatedly and systematically"* は、侵害となりうる行為をちょうど覆う。19 条 1 項は適法な利用者が実質的でない部分を *"for any purpose"* 抽出・再利用できるとし、2 項はそれを妨げる契約の条項を無効にする —— EU の DB 指令 8 条・15 条（`rounds/2026-11-16-eu-database-directive-snapshot.txt`）と同じ形。
(3) **§6 と CDPA 29A 条**: 29A 条 1 項の TDM の例外は *"for the sole purpose of research for a non-commercial purpose"* に限られ、*"(b) the copy is accompanied by a sufficient acknowledgement"* を求める（§7c の段と同じ）。5 項は、例外が許す複製を妨げる契約の条項を *"unenforceable"* とする。ACD の §6.1 は目的を問わず条件も付けずに計算の利用を許すので、英国の例外より広く、例外に頼る必要が無い。

**§5.2(a) と T124（回避の授権と放棄）—— 英国の技術的手段の条は、守る対象を「著作権者が許していない行為」に限る（2026-11-20 追記・portfolio-30・portfolio-50 と 2f の §1.269 の依頼・条文は `rounds/2026-11-19-cdpa-1988-s296-s296za-s296zf-snapshot.txt`・我々の読み）**: 296ZF 条 3 項 (a) は保護を *"the prevention or restriction of acts that are not authorised by the copyright owner"* *" of that work and are restricted by copyright"* と定め、1 項は技術的手段を *"other than a computer program"* の著作物に限る。プログラムの側は 296 条で、6 項は技術的手段を *"intended to prevent or restrict acts that are not authorised by the copyright owner of that computer program"* とし、1 項 (b) は手段を扱う者を *"knowing or having reason to believe that it will be used to make infringing copies"* の場合に限る。**読み（狭まる向き）**: ACD の §4 は著作権が制限する行為を全部許すので、許された行為を妨げる手段は、英国では著作物でもプログラムでも法律が守る「技術的手段」の保護に当たらない —— 2f が EU の指令 2001/29 6 条 3 項で示した読み（§1.269）と同じ形。ACD の下で作る写しは侵害の写しでないので、296 条の手段の取引の規制も働きにくい。T124 の授権と放棄は、この読みを本文の側から確かめる。**確立していないこと**: 手段が Work の許された行為と許されていない行為（例: 他人の素材と混ざった部分）の両方を妨げるときの扱い。

**§5.1 と §2.5 —— ACD は英国の捺印証書（deed）にならない（2026-11-20 追記・portfolio-30・条文は `rounds/2026-11-19-uk-lpmpa-1989-s1-deeds-snapshot.txt`・我々の読み）**: Law of Property (Miscellaneous Provisions) Act 1989 1 条 2 項は、文書が deed であるには *"it makes it clear on its face that it is intended to be a deed"* と *"it is validly executed as a deed"* の両方を求め、3 項は個人の有効な作成を *"(i)by him in the presence of a witness who attests the signature"*（または指図による署名と 2 人の証人）と *"(b)it is delivered as a deed"* に限る。ACD は自らを deed と名乗らず、証人の証明も交付も無い公開の文書なので、英国で deed として効くことはない。**読み**: 英国では、§5 の約束を約因の無い一方的な約束として強制する道（deed）は閉じている。§5 は、受け手の行為に対価が在ると読める場合の契約、§2.5 の禁反言（約束による禁反言は英国では抗弁としてだけ働く —— 控訴院 Harvey v Dunbar Assets [2017] EWCA Civ 60 の第 62 段落 *"it cannot alone confer positive rights on the promisee"* *"(often expressed by saying that the doctrine operates as a shield and not as a sword)"*・`rounds/2026-11-17-harvey-v-dunbar-2017-ewca-civ-60-promissory-estoppel-snapshot.txt`。2026-11-20 訂正: 先に「判例は未取得」と書いたが、30 自身が 11-17 にこの写しを置いていた・2f の指摘）、そして §3 の放棄・§4 の許諾の側で働く。**逆側（狭まる向きではない）**: §5 の約束を Dedicator に対して積極的に強制する（訴えて履行させる）道は、英国では弱い。**確立していないこと**: 公開の許諾の受け手の行為（複製・配布）が約因になるか（約因の判例は未取得）。

**§2.2 と §4.1 —— 英国の無償の許諾の撤回（2026-11-20 追記・portfolio-30・判決の写しは `rounds/2026-11-19-uk-fisher-v-brooker-2008-ewca-civ-287-gratuitous-licence-snapshot.txt`・我々の読み）**: 控訴院 Fisher v Brooker [2008] EWCA Civ 287 で Mummery LJ は、著作権の許諾は *"It can be implied from conduct."* *"It may be for a consideration or gratuitous, exclusive or non-exclusive, revocable or irrevocable, of limited duration"* と述べた（第 34 段落 (2)）。一部反対の David Richards J は、黙認から法が推定する無償の許諾について *"Such a presumed licence is prima facie revocable on reasonable notice."*（第 120 段落）と述べた。**有利な面**: 前者は、無償であることと撤回不能であることを並べて挙げ、両立を語の上で排除しない。後者は推定された許諾についての言明で、撤回不能と書いた明示の許諾についてではない。**不利な面**: 英国で無償の許諾を撤回不能にするものは、約因か deed（上の LP(MP)A 1989 の段で ACD は deed にならない）か禁反言で、禁反言は抗弁としてだけ働く（Harvey v Dunbar）。ACD の §2.2 の撤回不能は、英国では §2.5 の禁反言と、受け手の信頼に頼る。**判決の後半（2026-11-20 追記・`rounds/2026-11-19-uk-fisher-v-brooker-2008-paras-136-141-snapshot.txt`）**: 多数は Mummery LJ と Sir Paul Kennedy（第 141 段落 *"I agree with Lord Justice Mummery that this appeal should be allowed to the extent that he has indicated"*）。一部反対の David Richards J は第 136 段落で *"The licence is revocable unless the defendant has acted to his detriment such that revocation would be unconscionable."* と述べ、第 138 段落で *"nothing less than estoppel could terminate the right to revoke the implied licence."* とまとめた —— 黙示の無償の許諾について、撤回を止めるのは受け手の不利益に基づく禁反言だけ、という読み。ACD の §2.5 は、まさにその信頼と不利益を足場にする（狭まる向き: §2.5 の役が英国で明確になる。広がる向き: 不利益を被っていない受け手には、英国では撤回を止める足場が §2.5 からは出ない）。**上告審の結論（2026-11-20 追記・後の判決の要約で・`rounds/2026-11-19-uk-noel-redding-v-sony-2026-fisher-v-brooker-hl-snapshot.txt`）**: 上告審の本体は parliament.uk が 403、Find Case Law が 404 で取れない。高等法院 Noel Redding Estate v Sony [2026] EWHC 983 (Ch) は第 580 段落で、上告が認められ第 1 審の第 2・第 3 の宣言（共有と、黙示の許諾の撤回）が戻されたと記録し、第 581 段落で Lord Hope の文 *"But it would be a very strong thing, in the absence of a proprietary estoppel, to deny him the opportunity of"* *"exercising his right of property in his own share of the copyright."* を引く。**読み（不利な側に寄る）**: 上告審は控訴院の多数ではなく第 1 審と一部反対の側に立ち、黙認から推定された無償の許諾は撤回でき、撤回を止めるのは禁反言だけ、という結果になった。ACD への当たり方: 推定の許諾についての結論で、撤回不能を書いた明示の許諾（§2.2）についてではない。ただ英国で無償の許諾の撤回を止める足場が禁反言（§2.5）と信頼に在ることは、上告審の結論とも合う。**確立していないこと**: 上告審の本体の逐語（後の判決の引用を経た文だけを持つ）と、明示の無償の撤回不能の許諾についての英国の判例。

**§2.3（知らない受け手）と §4.1 —— 英国では侵害の要件が「著作権者の licence なしに」で、非独占の許諾は方式を要しない（2026-11-20 追記・portfolio-30・条文は `rounds/2026-11-19-cdpa-1988-s16-s92-licence-snapshot.txt`・我々の読み）**: 16 条 2 項 *"(2)Copyright in a work is infringed by a person who without the licence of the copyright owner does, or"* *"authorises another to do, any of the acts restricted by the copyright."* —— 侵害かどうかは、行為が著作権者の licence の内に在るかで決まり、条文は受け手が licence を知っていることも受諾したことも要件にしない。書面と署名を求めるのは 92 条 1 項の独占的許諾（*"a licence in writing signed by or on behalf of the copyright owner"*）だけで、非独占の許諾は口頭でも行為からでもよい（Fisher v Brooker 控訴院 34 段落 (2) *"It can be implied from conduct."*・上の段）。**有利な面（狭まる向き）**: 英国では §4.1 を bare licence（契約でない許し）と読めるので、ドイツや日本（§3・§2 の段）で立つ「受諾が無ければ契約が成立しない」という問いが、侵害の成否について立ちにくい —— 知らない受け手の行為も、著作権者が与えた licence の内なら侵害でない。**不利な面・確立していないこと**: bare licence は撤回できると読まれる（Fisher v Brooker の上告審の結論・上の段）ので、§2.3 の地位は英国で「撤回されるまで」になりうる —— 止めるのは §2.5 の禁反言と信頼で、知らない受け手は信頼していないので §2.5 からは足場が出ない（§2.3 と §2.5 の組み合わせの弱点）。受け手が知らないことを要件にしない読みは条文の語からの我々の読みで、判例を取っていない。
## 8. その他の法域

個別に扱っていない法域については、**§1 の構造がそのまま答え**になる。§15.4 が「無効な条項は
その法域に限り切り離す」と定めているので、**未知の法域があること自体は設計に織り込まれている**。

---

**§ 9（外から届いた、未読の法源）と § 9a（その原典の読み）は、2026-11-16 に `ACD-1.0.jurisdictions-sources.md` へ移した**（本文は同じ・番号もそちらが持つ）。法域ごとの読みに一次の法源を足し続けると、この文書が 1,000 行の上限（Check 365）に届くため。


---

## 9. オーストラリア

<!-- この節番号は、2026-11-16 に §9／§9a の出典が `ACD-1.0.jurisdictions-sources.md` へ移されたときに空いた番号を再利用している。§10 以下は繰り上げていない（他の文書が `jurisdictions.md` §10 を指しているため）。 -->

**問い** — オーストラリアでは、著作権の放棄（献呈）に法的な手続がなく、位置付けはコモンロー上も不確かである。さらに人格権は放棄できないうえ、2026 年の連邦裁判所の判断で包括的な事前の放棄（waiver）は無効とされた。ACD の献呈と人格権の放棄・同意の条項は、オーストラリアではどこまで効くか。

**本文の手当て** — 1.4 §3.1 は著作権を放棄し、§3.3 は献呈が認められない場合に §4.1 の包括的ライセンスへ落ちる。§12.1 は人格権を放棄し、§12.2 は同意と不侵害の誓約を置く。§15.2 は、ある条項が無効とされた場合にその条項を最小限に修正し、修正できなければその法域についてのみ切り離して残りを存続させる。オーストラリアでは、献呈の有効性そのものが不確かであるため、§4.1 のフォールバックと §15.2 の分離可能性が、献呈の成否に左右されない実効の柱になる。人格権については、§12.1 の放棄が効かない見込みが強く、§12.2 の同意も特定の行為に向けたものでなければならず、包括的な事前同意は効かないため、§12.2 の誓約（不侵害の約束）の方が実効の柱になる。

### 9a. 原典

- *Copyright Act 1968* (Cth), Compilation No. 65（2026 年 4 月 2 日施行）、Authorised Version C2026C00138。以下の引用は `rounds/2026-11-28-au-copyright-act-1968-s33-s40-s195am-s195an-s195awa-s195ax-s196-s197-snapshot.txt` に写しを置いた（同ファイルの冒頭の注意書きを参照）。
- Greenleaf & Li, "China's Copyright Public Domain: A Comparison with Australia" (2017) 27(3) *Australian Intellectual Property Journal* 147（2.6 節「Public domain dedications」）。
- *McCallum v Projector Films Pty Ltd* [2026] FCA 173（連邦裁判所、Shariff J、責任判断）——**判決本文は未読**。以下の要旨は、Johnson Winter Slattery、Piper Alderman、Clayton Utz の各法律事務所の解説と、*Journal of Intellectual Property Law & Practice* (2026) 21(8) 522 の要旨で確認した。判決本文の取得と照合は残課題である。

### 9b. 献呈

オーストラリアには、著作権の放棄（relinquishment）のための法令上の手続がない。Greenleaf & Li は「There is no statutory procedure for the relinquishing of copyright in Australia, where the position is uncertain at common law, and further complicated by moral rights provisions.」と述べている（同論文 2.6 節）。著作権は s 196(1) で譲渡可能な財産権とされ、譲渡は s 196(3) で署名のある書面を要する。将来の著作権の譲渡も s 197(1) で署名のある合意を要する。譲渡が書面を要するのに対し、放棄の方式や効力について法は沈黙しており、コモンロー上も確立していない。**確立していないこと** — オーストラリア法のもとで §3.1 の献呈が著作権の消滅として効くかは確立していない（§3、§4、§16）。献呈が効かない場合に §4.1 の包括的ライセンスが発動することは条文上の設計だが、そのライセンスが献呈者の後継者（successor in title）を拘束するかは、s 196(4) が「著作権の所有者が付与したライセンス」を前提としており、献呈が効かない場合のフォールバック・ライセンスがその前提を満たすかが未検証であるため、確立していない（§3、§4、§16）。Creative Commons Australia は、CC0 がオーストラリアで有効である可能性が高いと考えているが、確定的な司法判断はないと Greenleaf & Li は記している（同論文 2.6 節）。ACD の場合も同じく、献呈の有効性を断定できない。出典は `rounds/2026-11-28-au-copyright-act-1968-s33-s40-s195am-s195an-s195awa-s195ax-s196-s197-snapshot.txt`。

### 9c. 人格権

オーストラリアの人格権（Part IX）は、帰属権、虚偽帰属に対する権利、同一性保持権の三つである（Greenleaf & Li、同論文 2.6 節、脚注 84）。人格権は譲渡できない——s 195AN(3) は人格権が「譲渡、遺言、又は法律の作用による承継によって移転しない」と定める。放棄の規定はなく、侵害に対する同意だけが認められる（同論文の脚注 84 は当時の番号で s 195AW を引く。現行の Compilation No. 65 では s 195AWA に当たる）。同意は s 195AWA(2) で書面を要し、s 195AWA(3) は「特定の行為又は不作為」又は「特定の種類の行為又は不作為」と「特定の著作物」を特定しなければ効力を生じないと定める。包括的な事前同意は効かない。*McCallum* [2026] FCA 173 は、包括的な人格権の放棄を直接に判断した初めてのオーストラリアの判決である。Shariff J は、契約条項 6.2（「The Director waives all moral or other similar rights in respect of the Documentary or the Development Materials that the Director may be entitled to under the laws of any jurisdiction throughout the world in perpetuity.」）は有効な同意に当たらないとした。Part IX の文言・文脈・目的は、包括的な放棄を支持しない。同意は、特定の行為に向けられ、情報を得たうえでのものでなければならない。この問いは `QUESTIONS-FOR-COUNSEL.md` 質問 3(e)「Consent as well as a covenant」でも立てられている。**確立していないこと** — オーストラリアで §12.1 の放棄が効くかは、*McCallum* により否定的な見込みが強いが、控訴審の判断はまだなく、確立していない（§12）。§12.2 の同意が s 195AWA(3) の「特定の行為」の要件を満たすかも確立していない（§12）。ライセンス本文の同意は、特定の行為を指定していないため、s 195AWA(3) の要件を満たさない見込みである。したがってオーストラリアでは、§12.2 の誓約（献呈者が人格権の侵害を主張しないという約束）が、放棄や同意よりも実効の柱になる。ただし誓約自体が人格権の侵害の主張をどこまで封じるかは、*McCallum* の射程外であり確立していない（§12）。出典は `rounds/2026-11-28-au-copyright-act-1968-s33-s40-s195am-s195an-s195awa-s195ax-s196-s197-snapshot.txt`。

### 9d. テキスト・データ・マイニング

オーストラリアには、テキスト・データ・マイニング（TDM）のための一般的な例外がない。フェア・ディーリングは列挙された目的に限られる（研究・学習のための s 40、批評・評論のための s 41、パロディ・風刺のための s 41A、報道のための s 42 等）。米国のような一般的なフェアユースもない。生産性委員会（Productivity Commission）は 2025 年 8 月 5 日の中間報告書で TDM 例外の導入を提案したが、2025 年 10 月 26 日に司法長官（Michelle Rowland）は政府として導入しないと発表した。生産性委員会の最終報告書（2025 年 12 月 19 日）は、直ちに導入せず 3 年間の監視を勧めた。著作権と AI に関する参照グループ（Copyright and AI Reference Group）は、2026 年も有償の集合的ライセンスについて協議を続けている。**確立していないこと** — オーストラリアで、学習用データの複製が s 40 の研究・学習のフェア・ディーリングに当たるかは確立していない（§6）。s 40 は目的と性格、著作物の性質、合理的な期間内に通常の商業価格で入手できるか、潜在的な市場への影響、複製部分の量と実質性を考慮する（s 40(2)）。学習のための大量複製がこの枠に収まるかは、未検証である（§6）。出典は `rounds/2026-11-28-au-copyright-act-1968-s33-s40-s195am-s195an-s195awa-s195ax-s196-s197-snapshot.txt`。

### 9e. データベース権

オーストラリアには、EU のような独自の（sui generis）データベース権がない。オーストラリア著作権協議会（Australian Copyright Council）のファクトシート G066v14（2023 年 4 月）は、「No specific law exists in Australia protecting databases. Databases may only be protected if they fall under general copyright law.」と述べる。*IceTV v Nine Network* [2009] HCA 14 は、オーストラリア法にはデータベース指令に相当するものがないとした。したがって、データベース権を定める ACD の条項は、オーストラリアでは権利そのものが存在しないため、著作権の側面でのみ意味を持つ。

## 10. この文書の限界（先に自分から述べる）

1. **弁護士の確認を経ていない。** 本書は条文と公開された一般的理解の対応づけであり、
   法的助言ではない。
2. **各法域の記述は「問いの所在」であって結論ではない。** 「確立していないこと」の節を
   各所に置いてあるのはそのためである。
3. **法は動く。** 本書は 2026-08-27 に、DSM 指令 4 条 3 項のほかは条文番号を挙げない方針で書き始めた。
   その後、原典で読んだ条文を番号と逐語で引くようになった（2026-09-19 以降の 2a・6a・7a、2026-11-16 の
   各法域の段）。逐語は `rounds/` の写しに置き、写しの見出しに取得の日と方法（多くは WebFetch の片で、
   byte の写しではない）を書いてある。番号を挙げた分だけ正確さの保証が要るので、引く前に写しで確かめる。
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
