---
file: LICENSES/ACD-OSI-BOTTLENECKS-B10.md
audience: 次のセッションの実装者（一次読者）/ OSI license-review participants / 監査人
last-updated: 2026-11-15
reachable-via: ACD-OSI-BOTTLENECKS-EXTERNAL.md
canonical-ref: LICENSES/ACD-OSI-BOTTLENECKS.md (索引・分類・集計はあちらが canonical) / LICENSES/ACD-OSI-BOTTLENECKS-EXTERNAL.md (切り出し元・他の外部依存の項目) / LICENSES/ACD-1.0.gap-measurements.md
---

# OSI Approval Bottleneck Register —— B10（gap が本当に残っているか）

`ACD-OSI-BOTTLENECKS-EXTERNAL.md` が 821 行で advisory（800）を越え、B10 がそのうち 284 行を占め、いま最も足している節だったので、
2026-11-15 に B10 を丸ごとこの file へ移した（30 の提案・9b が移した）。本文は移す前と 1 字も変えていない。B10 の追記はここへ書く。

## B10 —— gap が本当に残っているか（最重要・OSI 判断依存）

**2026-09-10 の測定（第 1 の枝は確かめられる）**: **承認済み 149 件の本文をすべて取得して数えた**
（SPDX 3.28.0・取得失敗 0）——`machine learning` **0 件** / `text and data mining` **0 件** /
`machine-generated` **0 件** / `train` 系 **1 件**（`Frameworx-1.0`・無関係な用法）/
`model` **16 件**（実見したものは *"product model"* / *"Blue Oak **Model** License"* /
*"open source **model**"* で、**機械学習のモデルではない**）。

**これが establish すること**: **どの承認済みライセンスも、これらの主題を明示的には扱っていない。**
**establish しないこと**: **機械学習が許諾されていないこと** ——permissive ライセンスは
「すべての利用」を許すことで暗黙に許している。**我々が擁護できる主張は「明示の有無」と
「沈黙が未解決に残すもの」（留保機構・モデルと出力に及ぶ特許・そもそも著作権が生じるか）であり、
それは §6.5 が述べていることそのものである。**

**第 2・第 3 の枝も同日に測った**: **92 / 149 が特許に言及する**が、`output` を含む 30 件のうち
**主要 10 件では `output` が `patent` の 250 字以内に一度も現れない**（GPL 系の *"output from
running the Program"* は**著作権の話であって特許ではない**）。**`subsist` は 149 件中 0 件** ——
**権利が「生じているか」という語彙を使う承認済みライセンスは 1 つも無い。**
**establish しないこと**: 解釈上 output に及ばないこと。**測れるのは語の不在であって、効果は裁判所が決める。**

**残る枝は依然として OSI の判断である** ——**gap が在ることと、その gap が新しいライセンスを
承認するに足ることは別**であり、後者は測れない。

**gap を担う条項は 3 つに絞られる**（B3 の測定より）——
**§6**（ML / TDM の明示的許諾と Reservation の否認）/ **§8.4**（特許がモデル・出力に及ぶ）/
**§9**（機械生成物に権利が存するか否かと無関係に許諾が成立する）。

**この 3 つが 3 つである理由は、歴史である**（2026-09-16 追記・`comparison.md` §1.3）——
**既存の無条件系は「AI について寛容」なのではなく「AI について沈黙している」。** AI が利用形態でなかった時代に書かれたので、沈黙に費用が無かった。**変わったのは、3 つの問い（利用形態 / 生成物 / 権利の存否）が帰結を持つようになったこと**で、§6 / §8.4 / §9 はその 3 つに 1 つずつ対応している。
**⚠ そして最強の反論も同じ枠から出る** —— *「全部渡す」許諾は既に 3 つとも覆っているのだから、明示は長さだけを足す*。**これは #84 と B3 の合わせ技で、この枠はそれを打ち negate しない。****争点を「どれだけ許すか」から「その許諾が、行動する側に読めるか」へ移すだけである**（§6.5）。
**読めることに価値を認めない審査者に対しては、3 軸は冗長へ畳まれる。それが、この議論が実際に負ける形である。**

**この 3 つを削ると、ACD-1.0 は 0BSD / Unlicense に収束する** ——**そして承認基準 7（*"The license must fill a gap that currently existing licenses do not fill"*・`review-rules.md` §1.70）を満たさなくなる。**
*（2026-09-15 訂正: ここは長く、**どの文書にも存在しない節番号**を「の失敗」として引いていた。意図は復元できないので、番号ではなく**何が失敗するのか**を書いた。Check 471 (e) が検出。**訂正の注記に、訂正した当の記法を書き写さないこと** ——本日 3 度目の自己マッチである。）*
**逆にこの 3 つ以外はすべて削減候補である。**

**判断が OSI 側にある部分**: 「この 3 つは既存の承認済みライセンスで代替できないか」。
**現時点で我々が示せるのは、6 本（MIT / MIT-0 / 0BSD / Apache-2.0 / CC0 / Unlicense）の
どれもこの 3 つを同時には持たない、という事実まで**である。

### 2026-11-03 再検証 —— 語句ではなく法的作用で当て直した。**新規欠陥なし**

オーナーが渡した外部 AI の見解（指示ではない）を受けて、3 人の判断で、25 が**ドシエを読まずに** 1.4 草案の条文を承認済みの最近傍 10 本（0BSD / MIT / UPL / BSD-2-Clause-Patent / BlueOak / CERN-OHL-P / Apache-2.0 / EUPL / Unlicense / WordNet）の原文へ当て、bb がドシエ側の既存の反論と回答を棚卸しして突き合わせた。

| 条 | 最近傍に対する**作用** |
|---|---|
| §6.1 学習の許諾 | **新しくない**（0BSD・BlueOak の包括許諾が既に覆う。§6.5 自身がそう述べる）|
| §6.2 / §6.3 / §5.2(b) | **新しい** —— Dedicator 自身の留保の否認・依拠の放棄・付随条件を課さない約束。範囲は Dedicator 自身の行為に限られる |
| §6.4 | MIT の notice 条件がモデルに及ぶかという不確実性を除く。0BSD に対しては明示だけ |
| §7 データベース権 | **明示としては新しい。作用としては**、MIT / 0BSD の無限定の許可（著作権に限られていない）が及ぶ読みを**反証できない**（2026-11-04 訂正・下の「原典による立証」H2。旧文は「新しい —— 承認済みの許諾は copyright と patent に限られる」）|
| §8.1 | BSD-2-Clause-Patent / UPL / BlueOak と作用は同じ。差は条件の有無だけ（#241 (2)）|
| §8.4 | **明示としては新しい**（モデル・出力を名指す）。**請求項の範囲の差（§8.1 型の内容の限定を外した点）は立証できない** —— CERN-OHL-P の *"necessarily infringed by exercising rights under the Covered Source"* は、学習を権利の行使と読めば、1.1〜1.3 の §8.4 の *"only claims whose infringement depends upon the use of the Work"* とほぼ同じ形になる（ACD-1.4 は *"reaches a claim only where the feature that infringes it results, in whole or in part, from the content of the Work"* で、侵害する特徴の単位で限る。どちらも Work との因果で限る点は同じ・2026-11-24 に 1.4 の語へ当て直した）。**作用として立つのは「作品を超える対象への特許許諾 ∧ 条件も終了も無い」の組み合わせ**（2026-11-04 訂正・下の「原典による立証」G1）。費用は #16 |
| §9 | 付与としての作用は無く、宣言（主張しない）にとどまる |
| §12 | permissive に対しては新しいが、EUPL に先例（#241 (3)）|

**9 月 20 日以降にこの節が引いていなかった記録**（いずれも既に `against.md` に在り、ここでは指し先だけを置く）: #211（Fontana 氏「既存のライセンスで足りる」——gap 3）/ #233（CC0 スレッドの最強の反論）/ #241（承認済み 141 本の census が主張を 4 点狭めた —— **§8.4 について言えるのは「モデルを名指す承認済みは無い」まで**）/ #264（CAL-1.0）/ #269（**gap は存在理由であると同時に、果たしているかを測られる基準**・`[OPEN]`）/ #276（帰属ゼロ + 明示特許の組み合わせへの反対・(f) の vanity テストは我々には閉じられない）。

**残余（いずれも外部判断で、この増分では減らせない）**: (1) 作用として新しいのは §6.2 / §6.3 / §5.2(b)（限定つき）と §8.4 + §8.2 の組み合わせ（2026-11-04 に原典で立証・§7 と「§8.4 の内容限定の除去」は同日に外した）で、**それが承認基準 7 の「gap」に足りるか**は OSI の判断 / (2) 新しくない部分（§6.1 / §6.4 / §9）の価値は「確実性・読めること」で、**読めることに価値を認めない審査者には冗長へ畳まれる**（上の「最強の反論」そのもの）/ (3) #276 (f) と #255 の前半（具体的な用途を示せ）は採用の捏造なしには答えられない。**この再検証が減らした OSI 側の未解決は 0 件で、ドシエ側で直したのは説明 1 件**（`submission-reference.md` の「§8.4 の新しさは名指しだけ」→ 内容限定の除去も、25 が担当）。

### 2026-11-04 原典による立証 —— 既存ライセンスでは達成できない効果は、少なくとも 1 件あるか（差の狭さは `gap-measurements.md` §1.137）
**条文の対置・141 本の分割の証明・場面ごとの効果・Before/After・OSI 基準との対応は `ACD-1.0.gap-measurements.md` §1.133。** **オーナーが渡した外部 AI の見解（指示ではない・2026-11-04 にオーナーが明言）が置いた成功条件**: 既存ライセンスでは達成できない ACD 固有の法的効果を、**少なくとも 1 件、比較対象の原典と具体的条文で**裏付ける。できなければ未達と書く。 **分担**: 敵対仮説と B15 は bb・比較対象の条文の逐語照合は 5a（SPDX 原文 141 本・1.4 草案・`rounds/`・21 件中 20 件一致、残る 1 件は引用符の形で修正済み）・条文の対置は 25。

#### 敵対仮説（「既存ライセンスでも実現できる」）と反証
**比較対象の原文は SPDX `license-list-data` から取得した**（`generate_gap_census.py --fetch`・141/141・2026-11-04）。逐語の照合は 5a。

**G1. §8.4 —— 計算的利用から生じたモデル・出力の製造・使用・販売・輸入に及ぶ、無条件・終了なしの特許許諾**

| 敵対仮説 | 比較対象の条文（原文）| 反証 | 判定 |
|---|---|---|---|
| H1-a: BlueOak で足りる | *"Each contributor licenses you to do everything with this software that would otherwise infringe any patent claims they can license or become able to license."* | 対象は「このソフトウェアで行うこと」。学習という行為は覆うが、**できたモデルをその後に使う・売る行為は、ソフトウェアで行うことではない**。加えて *"The rules of this license are both obligations under that agreement and conditions to your license"*（Acceptance）・*"your license ends immediately"*（Excuse）—— 条件と終了がある。ACD §8.2 は *"subject to no condition and are not terminable"* | **反証できた**（⚠ *with this software* を「ソフトウェアを用いて作ったものについても」と広く読む余地は残る —— 残余リスク）|
| H1-b: CERN-OHL-P の Products で足りる（**敵対側の最強の筋** —— 5a）| §1.4 *"'Product' means any device, component, work or physical object … arising from the use, application or processing of Covered Source"* / §6.1 *"patent license to Make, have Made, use, offer to sell, sell, import, and otherwise transfer the Covered Source and Products, where such licence applies only to those patent claims … necessarily infringed by exercising rights under the Covered Source as Conveyed by that Licensor"* / §6.1 *"irrevocable (except as stated in this section 6, or where terminated by the Licensor for cause)"* / §6.2 *"If You institute patent litigation … any rights granted to You under this Licence shall terminate"* / §4 *"You may Make Products, and/or Convey them, provided that You ensure that the recipient of the Product has access to any Notices"* | **請求項の範囲では反証できない** —— ACD §8.4 は 1.1〜1.3 で *"This Section reaches only claims whose infringement depends upon the use of the Work"* と、ACD-1.4 で *"reaches a claim only where the feature that infringes it results, in whole or in part, from the content of the Work"* と限っており、学習を「Covered Source の下での権利の行使」と読めば、CERN の *necessarily infringed by exercising rights under the Covered Source* とほぼ同じ形の限定になる（**下書きの初版は「元の資料が実施しない請求項まで及ぶ」と書いたが、言い過ぎだった**）。**反証できるのは条件と終了の側**: モデルが Product なら、それを渡すたびに §4 の通知の条件が掛かり、特許許諾は §6.2（特許訴訟）と *"for cause"* で終わりうる。ACD では、モデル・出力について何も負わず（§6.4 *"You owe nothing under this Dedication in respect of any of them"*・§10.1。1.0〜1.3 の語は *"under this Dedication"* を持たなかった —— 2026-11-24 に 1.4 の本文へ当て直した）、特許許諾は *"subject to no condition and are not terminable by the Dedicator under this Dedication on any ground"*（§8.2・T85 の後の文） | **条件と終了の側でのみ反証できた** |
| H1-c: UPL で足りる | *"… patent rights … covering either (i) the unmodified Software … or (ii) the Larger Works (as defined below) … (b) any piece of software and/or hardware listed in the lrgrwrks.txt file"* | Larger Works は **事前に列挙されたもの**で、しかも *"each a “Larger Work” to which the Software is contributed"* —— **ソフトウェアが組み込まれる先**として定義されている。学習で生じたモデルはソフトウェアを組み込まないので、**列挙しても Larger Work に当たらない**（5a の問い「事前に列挙すれば代替できるか」への答え）。加えて通知の条件 *"This license is subject to the following condition"* | **反証できた** |
| H1-d: Apache-2.0 / BSD-2-Clause-Patent で足りる | Apache: *"necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Work"* / BSD-2-Clause-Patent: *"necessarily infringed by: (a) their Contribution …"*・*"The patent license shall not apply to any other combinations which include the Contribution."* | 請求項は Contribution（と Work との組み合わせ）に限られる。モデルは Contribution でも Work でもない | **反証できた** |
| H1-e: 0BSD / MIT / MIT-0 / Unlicense で足りる（黙示の許諾）| 特許の語を持たない（census） | 黙示の許諾（estoppel）は、リスト上でも論じられるが（#236 / #238）、**及ぶとしてもそのソフトウェアの使用**についてで、そこから生じたモデルの使用・販売にまで及ぶという読みの根拠は条文に無い | **反証できた**（黙示の許諾の範囲は裁判所が決める）|
| H1-f: 承認済みライセンス + 別の特許の誓約で足りる | —（ライセンスではない）| 経路は在る（Landley 氏 #276 (e)・`comparison.md` §5.5）。**ただしそれは「既存ライセンスで」ではない** —— OSI が比べるのはライセンスの条文で、誓約は Work と一緒に移らず、条件・期間・撤回可能性が誓約ごとに違う | **この仮説は「ライセンスでは」を外したときにだけ成り立つ**（既存ライセンスでは達成できない、という主張の範囲を書く）|

**2026-11-15 に足した —— G1 の特許の面の出典: CC0 の審査で決める側が述べたこと（`review-readings.md` §1.164・`review-readings-2.md` §1.245・portfolio-2f）。** Richard Fontana 氏 2012-02-18 は、CC0 を今起草するなら *"those two words "or patent" might not be in the document, and something else might be there in its place"* と書き、Bruce Perens 氏 2012-02-17 は *"Requiring an explicit patent grant in new licenses /might/ be over-reaching. Being sensitive about disclaimers of patent grants and their potential to harm developers is probably appropriate."* と書いた。Russ Nelson 氏 2012-05-21 は Svoboda の審査で *"It's only not OSI approved because it doesn't do what it can't do, and what people think it should do -- solve the problem of patents."* と述べた。ACD の §8 は、CC0 の 4(a) が除外を置いた場所に明示の許諾を置く。**逆側**: (i) どれも個人の発言で、委員会が理由としたのは除外の文（4(a)）であって許諾の不在ではない（Chestek 氏 2023-08-10・`review-outcomes.md`・against-2）。(ii) Perens 氏は明示の許諾を要件にすることを「行き過ぎかもしれない」と書いた —— ACD の §8 が要件を満たすための条ではなく、除外をしない形の 1 つにすぎないことを示す。(iii) CC0 は Creative Commons が取り下げたので、特許の点を埋めれば承認されたかは分からない。

**2026-11-16 に足した —— G1 の形を、CC0 の審査中に Perens 氏が提案していた（`gap-measurements.md` §1.150・古い節の反映）。** Bruce Perens 氏 2012-02-19（Fontana 氏と同意見だと述べて）*"CC should be asked to add language to CC0: an explicit permission to make use of patent claims necessary to use the software in the form that was dedicated or licensed. This should apply to both public domain, and the fallback license."* ACD の §8 は §3 と §4 のどちらにも依らずに立つ（§2.4・§8.6）ので、この形に当たる。**逆側**: 提案の範囲は「献呈された形のまま使うのに要る請求項」までで、§8.4 はそれを越える（#305）。Russ Nelson 氏は同じ日に、罠を仕掛ける者は特許を別の法人に持たせる、と書いた —— §8.5 は関連会社の特許に届かない（#310）。

**G1 の結論: 少なくとも 1 件、立証できた —— 立つのは 2 つの性質の組み合わせとしてである。** **(i) 作品・寄与を超える対象への特許許諾**を持つのは、census の分類（`generate_gap_census.py`・SPDX `8791eda`・2026-10-28・取得 2026-11-04）で S2 / S3 の **7 本**（BlueOak-1.0.0 / CERN-OHL-P / S / W-2.0 / EUPL-1.1 / EUPL-1.2 / UPL-1.0）で、**7 本すべてが原文で明示された条件を持ち**（BlueOak *"You must ensure that everyone who gets a copy … also gets the text of this license"*・CERN-OHL-P *"provided that You: a) retain Notices"*・CERN-OHL-S / W *"provided that on Conveyance of any such Source, or any associated Product You treat …"*・EUPL *"must include a copy of such notices and a copy of the Licence with every copy"*・UPL *"This license is subject to the following condition"*）、**UPL 以外の 6 本は終了の定めも持つ**（BlueOak *"your license ends immediately"*・CERN *"terminated by the Licensor for cause"* / *"shall terminate as of the date such process is initiated"*・EUPL *"will terminate automatically upon any breach"*）。**よって 141 本のうち、(i) と (ii) 条件も終了も無いこと を同時に持つものは 0 本で、ACD §8.4 + §8.2 は両方を持つ**（5a が全数で機械的に確認）。**再現と固定**: この 0 本は `python3 .github/scripts/generate_gap_census.py --fetch` のあと `python3 .github/scripts/measure_patent_reach.py` で、条件と終了の文の逐語つきで出し直せる（5a・PR 2407）。効果を運ぶ句（§8.4 の 2 句と §8.2）は Check 468u が草案の中で固定する（PR 2405）。**限界**: S1 の 58 本が本当にモデル・出力に届かないかは census の分類（人が読んだ判定）に依拠しており、裁判所の解釈ではない。**請求項の範囲そのものの差は立証できない**（1.1〜1.3 の §8.4 の *"only claims whose infringement depends upon the use of the Work"*、ACD-1.4 の *"reaches a claim only where the feature that infringes it results, in whole or in part, from the content of the Work"* と、CERN の限定は、どれも因果で限るほぼ同じ形）。**⚠ 費用（同じ重さで）**: この広さと無条件は #16（特許を持つ組織は受け入れにくい）と #276（帰属ゼロ + 特許許諾は「特許の放棄に等しい」）の当の原因で、**gap であると同時に採用を下げる理由**（B7）でもある。 **そして組み合わせで立つこと自体に反論が在る** —— Berkus 氏 *"It's not the goal of the OSI to have licenses for every possible combination of conditions"*（#276）。答えの範囲は `ACD-1.0.gap-measurements.md` §1.133「確立しないこと」6。 **同日後半の独立の再検証で 3 点動いた**（§1.133「独立の再検証」）: 母集団は OSI の頁だけに在る 8 本を足しても結論不変 / 既存ライセンスの組み合わせでは出ないが、別個の誓約では出る（gap は「不可能」ではなく「審査済みの 1 本に無い」）/ **§8.4 末文に 2 読みがあり、モデルの販売に届く範囲は解釈に依存する**。B15 との緊張は未解消で、条文比較・解釈・OSI 判断の 3 つに分けて置いた。

**G2. §7 —— sui generis のデータベース権の抽出・再利用の許可**

| 敵対仮説 | 条文 | 反証 | 判定 |
|---|---|---|---|
| H2: MIT / 0BSD の無限定の許可が及ぶ | MIT *"to deal in the Software without restriction"*・0BSD *"Permission to use, copy, modify, and/or distribute this software for any purpose"* —— どちらも許可を著作権に限っていない | 141 本に *sui generis* / *database right* の語は 0（census）。**だが MIT・0BSD の許可は著作権に限られていないので、データベース権に及ぶ読みは成り立つ** | **反証できない** —— **独自 gap の根拠から外す**。ACD §7 の効果は「明示による確実性」として扱う |

**G3. §6.2 —— Dedicator 自身の機械可読な合図を Reservation と読まない**

| 敵対仮説 | 反証 | 判定 |
|---|---|---|
| H3: どの許諾も、許諾が働く限り TDM の留保とは無関係なので足りる | その通り —— 留保（DSM 指令 4 条 3 項）が効くのは**例外**についてで、ライセンスの許可は別の経路である。§6.2 が効果を持つのは、**受領者がライセンスではなく例外に依って使う場面か、許諾が無効とされた場面**だけ | **一部だけ反証できる**（その場面では既存ライセンスに対応する文が無い・Kneschke v. LAION が「機械可読な留保」の帰属を問題にした）—— 独自 gap としては**限定つき** |

**G4. §12 —— 人格権の放棄と、放棄できない法域での不行使の約束・承継人の拘束**

| 敵対仮説 | 条文 | 反証 | 判定 |
|---|---|---|---|
| H4: EUPL で足りる | EUPL-1.2 *"In the countries where moral rights apply, the Licensor waives his right to exercise his moral right to the extent allowed by law"* | 「行使する権利の放棄」は不行使と同じ働きをする。ACD が足すのは**相手方（受領者と下流）の明示と、承継人・死後の行使者の拘束（§12.4）**だけで、後者が効くかは法域による | **ほぼ反証できない** —— 独自 gap の根拠から外し、「EUPL の形に、相手方と承継人を足したもの」と書く |

**除外したもの**: §9（機械生成物）は付与ではなく宣言 / §3 + §4 の独立は Unlicense も献呈と許可を並べている —— どちらも「既存では達成できない法的効果」の根拠にしない。

#### B15（主題適格）とのトレードオフ
**G1 を強めても B15 は悪化しない、と判断する。** 理由: §8.4 の対象は**Work（ソフトウェア）の計算的利用と、その結果**で、モデルのパラメータそのものを許諾の対象に加えるものではない。Chestek 氏の境界 *"cross over into data … when tied to software"* の内側にある。 **⚠ 逆側**: (i) Fontana 氏は *"the OSI contemplates that things other than OSI-approved licenses might be suitable for model parameters"* と述べており、§8.4 がモデルを名指すこと自体が「モデルについてのライセンス」と読まれる余地がある。(ii) **1.4 で §1.3 に「機械学習モデルのパラメータ・重み・設定」を足したこと**（CHANGELIST §1.3 行）は、Work の形としてモデルを名指すので、**こちらは B15 を自分から出す側**に働く（25 が逆側として記録済み）。**G1 の根拠は §8.4 で足り、§1.3 の追加には依らない** —— B10 を立てるのに B15 を悪化させる変更は要らない。

### 2026-11-15 —— 委員会の問いは「既存のライセンスで」ではなく「既存＋追加の許諾で」だった（H1-g・against #325）

**きっかけ**: Shuji Sado 氏 2026-01-24（`license-review`・Project Tick v2 への返信）*"Before a full OSD review, it would help to provide either a redline against GPLv3/AGPLv3 or a short "innovations only" excerpt, along with a brief explanation of why existing OSI-approved licenses plus additional permissions/exceptions or guidance cannot achieve the same goals."*（`review-readings.md` §1.205・portfolio-2f）。上の 2026-11-04 の立証は H1-f（承認済みライセンス＋別の特許の誓約）を「ライセンスでは、を外したときにだけ成り立つ」として退けた。**誓約は Work と一緒に移らないが、追加の許諾（例外）はライセンスの通知と一緒に移る**ので、H1-f の反証はこの形には届かない。

| 敵対仮説 | 反証の試み | 判定 |
|---|---|---|
| **H1-g: 0BSD に追加の許諾（§8.1・§8.4・§8.2 の形の特許許諾）を足せば G1 は足りる** | 追加の許諾は許諾を足す文なので、モデル・出力に及び、条件も終了も無い特許許諾を書ける。0BSD の *"for any purpose"* は計算的利用に及び、§6.2・§6.3 の合図の扱いは通知（ガイダンス）で述べられる。足すのに要る語は G1 だけなら §8.1・§8.2・§8.4 の作用の文で約 150〜400 語（どこまで写すかで変わる・語数は数えていない見積もり）| **反証できない。** G1 は「既存のライセンスでは」作れないが、「既存＋追加の許諾では」作れる |
| H1-g′: §3・§5・§12 も追加できる | 文書としては足せる。ただし §3 を足すと許諾ではなく献呈の文になり、OSI の FAQ が審査の対象外とする公有化の側に入る。§5・§12 は G2〜G4 の判定どおり、既存の文（EUPL など）が近い作用を持つ | **反証できない**（量が増えるだけ）|

**この問いへの答えの形（書けること・書けないこと）**:
- **書けない**: 「§8.4 の射程は追加の許諾では作れない」。追加の許諾にはどんな射程の特許許諾も書ける（portfolio-1c の最初の見立てを 30 が退けた・2026-11-15）。
- **書ける (1) 先例**: BSD-2-Clause-Patent は「BSD-2＋明示の特許許諾」を 1 本の新しいライセンスとして出し、2017-04-05 に承認された（`gap-measurements.md` §1.137 の追記・against #235）。提出文は *"a simple permissive license that is compatible with the GNU General Public License (GPL), version 2, but which also has an express patent grant included"* で、スレッドに「BSD-2＋別の例外にせよ」という投稿は見つからない（2016-01 と 2017 の `license-review` の件名に BSD+Patent を持つ投稿を *addendum / rider / separate patent / patent pledge / instead of a new license / just use* で grep・引用行を除く・2026-11-15）。ただし承認の理由は GPLv2 との両立で、ACD の理由とは違う（#235）。
- **書ける (2) 識別子**: *"0BSD WITH <新しい例外>"* も、例外を SPDX の例外一覧に載せなければ走査器に読まれず、B11 の費用は消えない。例外の文そのものも審査されない法的な文で、B1 を小さな文へ移すだけである。
- **書ける (3) 量**: ACD の残り（§3・§5・§12・§9・§2）は G2〜G4 と「除外したもの」で独自 gap の根拠にしていない部分で、それを含めて 1 本にするかは差の主張ではなく形の選択である、と認める。

**⚠ 逆側**: (i) 2026 年の委員会がこの問いを立てているので、2016 年の先例は「当時は問われなかった」以上の意味を持たないかもしれない。(ii) (2) の「B1 を小さな文へ移す」は、小さな文の方が審査しやすいと読まれれば、かえって既存＋例外を勧める理由になる（B3・B13）。(iii) 宛先は GPL を写した互恵型の草案で、例外の型は GPL の linking exception を念頭に置いている。許容型の土台に特許の許諾を例外として足す形が実務で受け入れられるかは、この立証の外にある。

### 2026-11-15 —— 新しい効果を主張するほど、審査は長く割れる（L0-R・2017）

当時の委員の Josh Berkus 氏は、法律家が単独で出した新しいライセンスの審査で、提出者に *"a license which does several things which no license previously approved by the OSI does. If you thought that reviewing such a license was going to be either fast or straightforwards, or that committee members would be unanimous in our evaluation of criteria or recommendations, then I'm sorry."* と書いた（`license-review` 2017-11-13・`review-readings-2.md` §1.229・portfolio-2f）。**B10 で gap を強く言えるほど、審査の時間と割れ方は大きくなる** —— gap の主張は承認されるべき理由であると同時に、審査を長くする理由でもある。同じ審査で Bruce Perens 氏は *"those who make use of the Open Source software and do not modify or redistribute it, there should be as close to *no legal load* as possible"* と書いた（2017-10-24）。ACD は使う人に何も課さない（§10.1・§2.3）ので、新しさの側で時間がかかっても、決める側が掲げる価値の側では争点を作らない。

同じ線の文は 2008 年にも在る —— 当時の委員長 Russ Nelson 氏 2008-05-29 *"the community has come to realize that more Open Source licenses are not a good thing."*（§1.238）。**逆側**: L0-R は使用を条件にする型で、Berkus 氏の文が割れを予告した中身（条件の新しさ）は ACD に無い。ACD の新しさは許諾と約束の範囲（§8.4・§5・§6）で、割れるとすれば H1-g（既存＋追加の許諾で足りるか）の側である。

### 2026-11-15 —— 2001 年には「新しさが無くても OSD に合えば退けられない」と書かれていた（`review-readings-3.md` §1.301）

当時の理事 Russell Nelson 氏 2001-08-05 *"Some of the licenses ARE innovative, and it's not clear that we can reject the ones which aren't so innovative given that they comply with the open source definition."*、事務局長 Lawrence Rosen 氏 2001-09-26 *"OSI approves licenses if and only if the license is consistent with the provisions of the published Open Source Definition."*。同じ年に Rosen 氏は、審査の優先度として差・使用・起草の質・必要性の説明の明確さ・共同体の関心を挙げた（2001-01-19・本人の提案）。**逆側**: これは今の基準ではない。2008 年の委員長（上の Nelson 氏の同じ人）は *"more Open Source licenses are not a good thing"* と書き、委員会は後に差を問うようになった。古い基準を有利に引くなら、それが今の基準でないことを同じ文で言う —— 現役の委員の Pamela Chestek 氏は 2019-07 に *"I disagree with your framing that every license must be approved unless we can point to a specific rule broken."* と書き、Richard Fontana 氏は 2026-08-28 にその由来を、新奇な条項を持つライセンスは OSD の特定の条に反すると名指せない限り承認を強いられる、という起草者の主張への対応だと説明した（`reviewer-positions.md` の「一般的な規則の移り変わり」・`board-decisions.md` §2h）。2001 年の記録が示すのは、差の問いが承認の可否ではなく優先度として始まった、という経過だけである。

### 2026-11-15 —— 承認できる提出を、増殖を理由に保留した実例（OVPL・2005・`review-readings-4.md` §1.350・portfolio-50）

Russell Nelson 氏 2005-08-19（2005-02-09 に第三者から OSI の新しい会長と呼ばれた・`license-discuss` 2005-02。2005-08 に会長だったかは確かめていない） *"It's approvable as far as I can see. However we also have license proliferation issues to worry about."* —— OSD に合うと認めたうえで、増殖を理由に別の道（CDDL への改善の取り込み）を求めた。B10 の「差は承認の可否ではなく優先度として始まった」（上の 2001 年の段）は、2005 年には可否の手前で働いていた。**逆側**: 同じ通で同氏は *"This is just my opinion, and I can be talked out of it."* と書き、処方は「CDDL の改善は CDDL へ入れよ」だった。ACD は既存のライセンスの派生ではないので、処方はそのまま当たらない。当たるのは「増殖は OSD への適合と別に問われる」という点である。

### 2026-11-15 —— OSD の起草者と当時の理事が述べた目標を、ACD は文字どおりに満たす（`review-readings-6.md` §1.451・portfolio-9b）

Bruce Perens 氏 2002-01-20 *"One of the goals of the OSD was to have software that the user could run without having to read the license or take any special action."*、Russell Nelson 氏 2002 は、OSD は *"If you have a copy of this software, you can do anything you want with it."* と言うべきだったと書いた。ACD の §10.1〜§10.4 は、受け手に条件も義務も課さず、何も知らせなくてよいと定める。**逆側**: MIT と 0BSD も同じ目標をほぼ満たすので、これは B10 の問い（既存のライセンスで足りないのは何か）には答えない。有利な材料として使えるのは、「条件を持たない形は OSD の目標に沿う」という点だけである。 **2026-11-16 に足した逆側（9b の全文での当て直し・`review-readings-6.md` §1.451）**: 同じ Perens 氏は 2002-03-13 に *"It is very tempting to ask for the OSD to say "no requirements connected with use, whatsoever". But I don't believe that's what we should do."* と書き、使用に要件を一切置かないことを OSD の原則にするのには反対した。Lawrence Rosen 氏は 2002-01-20 に帰属表示を求める条を *"All-in-all, I praise the advertising clause and encourage it to be used."* と称えた。「条件が無いこと」は、決める側にとって無条件の美点ではなかった —— 上の目標の文は「読まずに使える」ことの目標で、条件の無さを原則とする主張ではない。

### 2026-11-15 —— 2005 年の委員長も「OSD に合うものを全部か、良いものだけか」を決めていなかった（`review-readings.md` §1.177・portfolio-2f）

Russell Nelson 氏 2005-09-01 *"Does OSI certify all licenses that comply with the OSD?"* と *"Does OSI certify all good licenses that comply with the OSD?"* を並べ、*"In other words, do we take into account the interests of the community?"* と問うた。Lawrence Rosen 氏は同じ日に *"my opinion has always been that OSI should approve licenses that comply with the OSD. Period."* と答え、理事の Eric S. Raymond 氏は同じ月に、3 つの基準（読める・再利用できる・重複しない）を *"supplemental to the OSD"* とし、*"we have to be more strict about what we allow in."* と書いた。上の 2001 年の段（新しさが無くても退けられない）から 2005 年のこの段を経て、差の問いは「優先度」から「承認の前の問い」へ移った。**逆側**: Raymond 氏の文は方針の説明で、理事会の議決の文ではない。Nelson 氏 2005-09-04 *"We can change our reasons for approval over time, but not over parties asking for approval."* —— 基準は時とともに変わるので、2005 年の基準も提出の日の運用とは限らない。

### 2026-11-15 —— 2013 年の議論は、新しいライセンスの問いを「OSD に合うか」と「既存の全てと十分に違うか」に置いた（`review-readings-2.md` §1.223・9b が反映）

新しいライセンスの承認を「まず `license-discuss`、問いは OSD と十分な差、形式の不備は門前で戻す」に寄せ、使用の数を要件にする案は鶏と卵として退けた議論である。B10 の問い（既存で足りるか）は、この 2 つ目の問いそのものである。**逆側**: 同じ会話の基準率は厳しく、2012〜13 年の新しいライセンスは既存の新版を除いて全部退けられた（Berkus 氏の数え方・我々は数え直していない）。

### 2026-11-15 —— 効果が重複するライセンスの例外は「判例の新しい展開」と「明白な法的欠陥」だ、と Perens 氏が書いた（2018・`review-readings-2.md` §1.224・9b が反映）

差の言い方をこの 2 つの例外の語に合わせれば、審査者が既に持っている枠で B10 を読める。**逆側**: 例外は判例（case law）と書かれていて、ACD が依る EU 指令の留保は立法である。また Perens 氏の注意書きは OSI の規則ではない（本人が断っている）。

### 2026-11-16 —— 許可型の変種の増殖に、元の事務局長が「もう断るべき」と書いた（`review-readings-3.md` §1.311）

Lawrence Rosen 氏 2020-08-18（`license-discuss`）は、承認済みの BSD 型のライセンスが増えていることを *"ludicrous"* と呼び、*"OSI should simply refuse to do it anymore!"* と書いた。Josh Berkus 氏は 2020-08-21 に *"For such a short license, BSD has an awful lot of variations."* と添えた。ACD は条件の無い許可型の文書として、0BSD・MIT-0・Unlicense と同じ棚に置かれうるので、差が認められなければこの線に当たる。**逆側**: 文は同じ効果の言い換え（BSD の変種）に向けたもので、G1 の差が立てば当たらない。同じ Rosen 氏が 2005 年には「OSD に合えば承認すべき」と書いており（上の 2005 年の段）、2020 年の文は Rosen 氏個人の立場が動いた記録である（2020 年の同氏は OSI の役職に無く、委員会や理事会の運用が変わったことは示さない）。文は、Nelson 氏の付け替えの提案（無承諾の付け替えは法に反する、が通の主題）に反対する通の中で *"Although I do agree that ..."* と付け加えた一文である。Berkus 氏の文は *"Gotta be the bikeshed problem."* と続く軽い一言で、重くは使わない。

### 2026-11-16 —— 2013 年の理事は、立証の責任を提出者に置き、「必要であること」をその 3 つ目に挙げた（`review-readings-2.md` §1.253・portfolio-2f）

Josh Berkus 氏 2013-11-07（`license-review`）*"As a new license proposer, the burden is on you to prove to a majority of the OSI board that your license is: - open source - legally valid - needed"*、続けて *"And note that we haven't even begun the non-proliferation arguments yet, which will also be substantial."* 2015 年の同氏の 4 つの問い（`review-readings.md` §1.179）と同じ線で、「必要であること」は B10 の問いを提出者の立証の責任として述べている。**逆側**: 1 人の理事の言い方で、理事会の規則の文ではない。「増殖の議論はその後」とあるので、差の立証が通っても次の問いが残る。

### 2026-11-16 —— 明示の特許許諾が無ければ強く反対する、共同体にとっての必要を説明せよ（`gap-measurements.md` §1.149・古い節の反映）

Lawrence Rosen 氏 2018-12-13 *"if a license now is proposed without an express patent grant, I'd object to it vociferously"*（ACD の §8 は明示の許諾で、この線に合う）。Henrik Ingo 氏 2019-05 *"The OSI process is as much about policy as it is about technically applying the OSD rules correctly."*、新しいライセンスの提出者は *"fail to even attempt to explain how the new license is necessary or beneficial for the open source community as a whole."* —— B10 の答え（G1）は、提出者の都合ではなく共同体の利益として書く必要がある。**逆側**: どちらも個人の発言で、OSI の決定ではない。Luis Villa 氏 2019-06 がすぐ退けられる類型に挙げた *"incoherently written"* は、B3・B13 の側の危険として残る。

### 2026-11-16 —— ACD に最も近い型の直近の提出に、要点が見えないと書かれた（PUWL・Fontana 氏 2025-10-01）

Richard Fontana 氏は PUWL（公有化の放棄・責任の否認・代わりの許諾を 1 つにした提出）に *"I think the rationale you give for the license is fine, but I don't see the point of the license itself. As far as I can tell you are just combining a bunch of existing highly permissive permission grants"* と書いた（portfolio-50 が模擬委員会のアーカイブの当て方で拾った・against #110 の段）。B10 の問いが、同じ型にそのまま向けられた記録である。**逆側**: PUWL は既存の文（CC0・Unlicense など）を、どれが当たるかを言わずに並べた文書で、ACD は自前の文で書かれ、G1 の効果を主張する。審査者がその差を、同じ結論に達する前に見るかどうかは、入口（最初の一画面）が受け持つ。

### 2026-11-16 —— 「本文を書く前に、既存のどれも使えない理由をリストに書け」（`review-readings-2.md` §1.255・参加者の発言）

Ian Lance Taylor 氏 2003-07-16（`license-discuss`）*"If you can't use an existing license, then your first step should not be to write a license, but instead to write to the list and explain clearly why no existing license will work"*。**逆側（ACD に不利な順序）**: ACD は G1 に理由を書いたが、リストに尋ねる前に本文を書き、1.0 を出した（2026-08-26）。**有利な面**: 1.0 は `license-review` ではなく `license-discuss` に出し、理由（gap）を最初の投稿に添えた。Taylor 氏は決める側の記録の無い参加者で、規則ではない。

### 2026-11-16 —— 「違反しようのないライセンスは存在する理由が無い」（2009 の委員長）と、「増殖への扉は、それだけでは却下の理由ではない」（2011）（`review-readings-6.md` §1.458・portfolio-9b）

不利な側: Russ Nelson 氏 2009-03-14 の WTFPL への理由（全文と ACD の答えは `board-decisions.md` §8.1）。有利な側: Karl Fogel 氏 2011-12-15（`license-review`・MPL 2.0）*"Agree with Bruce that the clause that opens the door to license proliferation is not in itself grounds for rejection."*（同じ通で *"We should of course still do everything we can to stop proliferation!"* と添える）。**逆側**: Fogel 氏の文は MPL 2.0 の版の更新の条についてで、新しいライセンスそのものの増殖を許す文ではない。

### 2026-11-23 —— 「OSD に無い理由で却下するのも務め」（Perens 氏 2009）と、「単純な許容型にも、既存より改善になる点が無い」（Chestek 氏 2020）（`review-readings-6.md` §1.460・portfolio-d7・`review-readings-6.md` §1.461・portfolio-d7）

不利な側: Bruce Perens 氏 2009-02-17（`license-review`・TGPPL・`rounds/2008-12-license-review-tgppl-trademark-rule-observed-4of8.txt` の中に引用の形で在る）*"Other licenses are poorly written, self-contradictory, or impractical. Those aren't in the OSD either, but it's OSI's duty to reject them rather than inflict them on the user community."* —— OSD の起草者が、OSD の外の理由（起草の質・実用性）での却下を務めとした。Pamela Chestek 氏 2020-12-26（OIN License・`rounds/2020-12-license-review-oin-chestek-non-operative-words-observed.txt`）*"I see no benefit to this license even if you adopted all my suggestions; there are many well-accepted, commonly used permissive licenses and I don't see this one as ever reaching a point where it is an improvement on them."* —— 条件の少ない許容型の新しいライセンスに、当時の委員長が「直しても既存より良くならない」と書いた。B10 の問いそのもので、ACD が既存との差を示す責任を重くする。**逆側**: OIN License は特定の団体の目的のために書かれた許容型で、Chestek 氏はその文書について書いた。ACD は gap の 3 本（G1〜G3）を条ごとに名指して述べており、少なくとも G1 は承認済みのライセンスの census に当てて立てた（上の「G1 の結論」）ので、「既存より改善の点が無い」には条ごとに答える材料がある。Perens 氏の 3 つの理由は、どれも起草の質の問いで、B3・B13 の側で答える。

### 2026-11-23 —— 「より良い否認は、新しいライセンスの価値の代わりにならない」（2014・`review-readings-6.md` §1.459・portfolio-d7）

不利な側: Carlo Piana 氏 2014-03-12（`license-review`・Public Software License・`rounds/2014-03-license-review-psl-piana-disclaimer-not-a-proxy-observed.txt`）*"I don't see "better liability disclaimer" a good proxy to assess the worthiness of a new license in terms of non-proliferation."*、同じ会話で Richard Fontana 氏 *"I know of no specific reason (other than desire for elegance) why one could not simply supplement the form disclaimers with additional ones."* ACD が既存との差を述べるときに §13 の否認や §14 の責任の制限を挙げても、増殖に見合う価値の証拠にはならない。**逆側**: ACD の gap の 3 本（G1 §8.4・G2 §7・G3 §6.2）は否認に依っていないので、この文が崩す主張は今のドシエには無い。重さが足されるのは、差の説明に否認を混ぜたときだけである。

### 2026-09-20 追記 —— gap の 1 本目に、**決着した裁判例が付いた**

**§6 が扱う問いは仮想ではない。** ハンブルク上級地方裁判所 第 5 民事部は 2025-12-10 に
*Kneschke v. LAION* の控訴を棄却し（Az. 5 U 104/24）、**(a) 画像エージェンシーが置いた利用留保は
権利者に帰属させられる**が、**(b) それは機械可読の形式を欠いていたので効かなかった**と判断した
（`jurisdictions-sources.md` §9a (9)）。**§6.2 が扱うのはその 2 点そのもの**で、
**しかも UrhG 44b 条 3 項より広い**（機械可読な signal であっても Dedicator の側では
Reservation と読まないと述べている）。

**これが B10 に対して足すもの**: gap の 3 本のうち **§6 については、「明示が無いこと」が
現実の帰結を持つことを、名前のある裁判所が名前のある条文で示した**。
**「沈黙が未解決に残すもの」は仮定ではない**、という 1 段だけ強くなる。

**⚠ そして同じ判決が、同じ本数だけ弱める。** 控訴審は **UrhG 60d 条**（学術研究）でも
正当化されるとしており、**その法域では研究目的の TDM は留保の有無に関係なく通る**。
**決着した事件がある唯一の法域で、§6 の追加価値は研究機関に対しては小さい。**
**さらに確定していない**（BGH への Revision 許可）——**審査中に覆りうる holding を引くことになる。**
**そして我々が読んだのは判決ではなく裁判所の press release である**（全文は請求可能・未請求）。

---

### 第 3 ラウンド（2026-09-15）—— moderator が 3 つを求めた

**逐語は `rounds/2026-09-15-offlist-nick-vidal-round3.txt`**（リスト外・steward 提供）。
2026-09-14 に steward が長文で全体像を説明し、身元証拠として履歴書・職務経歴書を添付した。
その返信で moderator が求めたのは 3 つ。

1. **Code of Conduct の *"Respect time and attention"* との整合を説明すること。**
2. **メールの長さと密度を、他の人間の投稿と比べて示すこと。**
3. **公開通知の一文を理解しているか、そして現在のワークフローが実際にそれを満たすか、
   満たすならどう満たすかを具体的に説明すること。**

#### (2) は測れる問いなので測った

**結果は `review-corpus.md` §1.85**（両リスト 3 か月・192 通・37 名・道具は
`measure_list_verbosity.py`）。**先に不利な側を書く。**

- **我々が書いた散文の中央値は、他の参加者の 3.6 倍**（683 語 対 188 語）。
- **6 通すべてが 69〜95 パーセンタイル。短い投稿が 1 通も無い。**
- **2026-08-26 の ACD 投稿は、この 3 か月で届いた本文が最長の 1 通**（5,778 語）。

**有利な側も同じ測定から出る。**

- **密度では濃くない** —— 1 文 22.0 語（他 23.0）/ 1 段落 21.5 語（他 34.5）。
  **文も段落も他より短い。「長い」と「密である」は別の性質で、我々は前者だけに当たる。**
- **`license-review` へ送った 3 通は、届いた量で 37.6 / 47.8 / 53.8 パーセンタイル** ——**中位以下。**
- **総量は 7 位 / 37 名**（全投稿の 3.1% / 全散文語数の 6.4%）。上位 6 名は 9〜26 通を投じている。

**🟢 そして、直せる欠陥が 1 つ見つかった。** process ページは
*"Submit a copy of the license **as an attachment** in simple text format"* と書いている。
**我々は条文を本文へ貼り付けた。** 従っていれば、最長の 1 通は **5,778 語 → 867 語**だった。
**これは弁明ではなく、向こうの手続きに根拠のある具体的な是正である。**

#### (3) は測れない —— そして、素直に読むと満たしていない

**通知の一文は 2 つの節から成る。**

> We do not allow posts generated by AI **without careful review from the author**
> **and** will reject posts where we **suspect that an AI has been responsible for all or most of
> a message**.

**前半には例外がある（著者による careful review）。後半には無い。**
**素直に読めば、後半は「文言の大半を AI が作った投稿」を、review の有無にかかわらず拒否対象とする。**

**steward の 2026-09-07 の回答は、その状態を自分から述べている** ——
*"The initial drafts are generally generated by AI. I review them, and if I consider the content
appropriate, I send them as written."*

**したがって、素直な読みでは現在のワークフローは後半を満たさない。**
**これを「満たしている」と述べる文面を作ってはならない。**

**⚠ 逆側も同じ重さで書く。** 後半を**文言**ではなく**帰責**の意味に読む余地はある:

- **前半の例外が意味を持つのは、後半が「文言を AI が作った」より狭いときだけ**である。
  広く読むと、**AI が起草した投稿はすべて後半に当たり、前半の例外は一度も働かない。**
- **moderator 自身が 2026-09-07 に同じ区別を書いている** ——
  **説明責任を負う人を AI が補助すること**と、**AI が独立に長い法的議論を生成すること、
  または開示なしにリストを実験の場にすること**を分けている
  （私信なので要約）。
- **2026-09-09 の公開通知も、外国語で legalese を理解し応答するための AI 利用を
  *"appropriate"* と明示している。**

**しかし読みを決めるのは moderator であり、我々ではない。**
**安全側の想定は素直な読みのほうである。**

#### この局面で AI がやってはならないこと（既存 3 点に 1 つ足す）

4. **この往復への返信を起草しないこと。** 問い (3) は「あなたのメールを AI が書いているか」で
   あり、**その返信を AI が書けば、答えそのものが答えを裏切る。**
   **本リポジトリが出すのは材料まで** —— 測定・条文の読み・選択肢 —— **であり、文面は steward が書く。**
   **これは謙譲ではなく、この 1 通に限っては、AI が書いた文面が内容を偽ることになるからである。**

#### 選択肢（すべて steward の判断・AI は選ばない）

| | 中身 | 費用 |
|---|---|---|
| **(a)** | **ワークフローを変える** —— リストへ送る文面は本人が書き、AI の関与を翻訳・読解に限る（**通知が *appropriate* と呼んでいる範囲**）| 速度が落ちる。**後半の節を素直な読みでも満たす唯一の道** |
| **(b)** | **後半の節が前半の例外を共有するのかを、moderator に率直に聞く** | 聞くこと自体は誠実だが、**答えが「しない」なら (a) か (c) へ戻る** |
| **(c)** | **リストへの投稿をやめる** | **B1（弁護士レビュー）の解消経路も閉じる**（審査者は pro bono の弁護士であり、提出が条文を彼らの論評の場に置く経路である・#274）|

**⚠ (b) を「時間を稼ぐ手」として使わないこと。** 聞いている間も投稿はできず、
**聞いたこと自体が「素直な読みでは満たしていないと自覚している」ことの表明**になる。
**それは正直だが、無料ではない。**

#### 返信は送られた（2026-09-15・steward が自分で書いた）

**逐語は `rounds/2026-09-15-offlist-nick-vidal-round3-sent.txt`。**
**本リポジトリは文面を起草していない** —— 出したのは測定と条文の読みと選択肢までで、
**「この往復への返信を起草しない」は守られた。**

**同じ道具で測ると 271 語 / 1 文 18.1 語 / 62.4 パーセンタイル**（我々のそれまでの中央値 683）。
**「長い」と言われた問いに、短い文で答えている** ——主張ではなく実演になっている。

**返信が確定させたこと 3 点。**

1. **不利な数を自分から先に出した**（683 対 188）。密度の反論は**その後ろ**に置かれている。
2. **欠陥を自分で名指しし、直し方まで述べた**（貼り付け → 添付）。
   **process ページを引いて「向こうの規則に従っていなかっただけ」と見せる形は取っていない** ——
   引けば正しさは増えるが、非を認める度合いは減る。
3. **素直な読みを自分に当て、*"so I will change my approach"* と先に述べた**うえで、
   **有利な読みを自分から主張していない**（*"I do not wish to speculate on the moderators'
   intentions"*）。

**⚠ そして、返信が作った 2 つの負債。**

- **`not fully comply` の "fully" が、唯一の緩衝語である。** 素直な読みなら「完全に満たさない」で
  あって「十分には満たさない」ではない。**緩衝の無いことが強みの文面に、1 語だけ緩衝がある。**
- **「今後は短くする」は測れる約束になった。** アーカイブは公開で、
  `measure_list_verbosity.py` が次の数字を出す。**提出本体には下限がある**
  （gap 説明・比較・要求項目）ので、**「添付にする・送り状は短くする」という*行為*の約束は
  守れるが、「短くする」という*結果*の約束は引用されうる。**

**⚠ 置いてきた材料（忘れたのではない）。** 問いは「他の**人間**の投稿と比べて」だったが、
返信は**総量の比較を出していない** —— `license-review` の 3 通が届いた量で中位以下
（37.6 / 47.8 / 53.8）であることと、**総量が 37 名中 7 位・全投稿の 3.1%** であること。
***"Respect time and attention"* は本来 1 通あたりより総量の話**なので、最も的に当たる数字だった。
**それでも落としたのは妥当である** ——「短さ」を問われた返信で数字を足せば、それ自体が矛盾する。
**次に同じ問いが来たら、この 2 つが未使用の材料として在る。**

#### したがって、分岐 (a) と (b) は両方とも生きている

**返信は (b)（読みを聞く）を取りつつ、答えが素直な読みなら (a) へ移ると*先に宣言した*。**
**つまり (a) の中身は、聞かれる前に決まっていなければならない。**
**これは「待ち」ではなく、いま手を動かせる作業である** ——
**次の作業は (a) の棚卸し**（リストへ送る文面について、AI の関与をどこまでに限るか / 翻訳と読解は
通知が *appropriate* と呼んでいる範囲 / 測定とその提示はどちら側か）。
**決めるのは steward だが、選択肢を並べるのは本リポジトリの仕事である。**

#### ⚠ 測ったが、答えには使わない材料（2026-09-15）

**moderator は我々の他ライセンス審査が本物かを問うた。** その行動がリストで普通かどうかを
測った結果が `review-venue.md` §1.89 にある（**19 年の提出者 82 人中 53 人＝65% が、
自分の提出以外のスレッドにも投稿している**）。

**この数を返信に使ってはならない。** 理由は 3 つで、どれも独立に効く:

1. **問われたのは行動の分布ではなく、我々の意図である。** 分布で答えるのは**問いのすり替え**になる。
2. **頻度は動機について何も言わない。**「普通の行動だ」は「本物だ」ではない。
3. **我々はその母集団に入っていない** ——我々の提出は `license-discuss` に在り、
   測ったのは `license-review` の提出者である。**比較できるのは pattern であって membership ではない。**

**では何のために測ったのか。** **我々自身が「異常なことをしている」と誤って自己評価しないため**である
（#131 の「誤りは我々が悪く見える向きに偏る」の予防）。**register の内部向けの数であって、
外へ出す材料ではない。**

**2026-11-25 に足した —— 出力に条件を課さないことの支えと、出力へ広げた特許の費用（`review-readings-7.md` §1.485・§1.487・6c）。** 出力に条件を付けることについて、決める側の文は支える側に揃っている: Pamela Chestek 氏 2025-05-17 *"you are imposing a obligation that runs with the output, which has never been acceptable in an open source license."*（ModelGo）、Carlo Piana 氏 2025-05-14 *"I think that imposing anything on the output of the model is against the OSD as it is a restriction on the use of the licensed subject matter."*。ACD-1.4 は *Computational Use* の中に作成と使用を入れ、条件を課さない（§10.1・§6.4）。特許を出力へ広げたことは、広さの側では不利な語（B7 の Perens 氏 2025・Smith 氏 2018）に当たり、G1 の gap はその広さを買っている。**逆側**: Chestek 氏 2025-12-03 は出力の制限が自動的に OSD 6 に当たるとは言わない、どの文も条件を課す側への異議で、課さない文を求めたものではない、*embodied* に限る承認済みの型（AFL・OSL）は出力を想定していない —— 出力に届く許諾が求められた記録も、退けられた記録も無い。
