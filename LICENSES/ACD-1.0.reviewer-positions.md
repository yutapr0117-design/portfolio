---
file: LICENSES/ACD-1.0.reviewer-positions.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-09-09
canonical-ref: LICENSES/ACD-1.0.review-precedents.md (提出ごとの記録) / LICENSES/ACD-1.0.objection-map.md (1 表の要約) / LICENSES/ACD-1.0.against.md
---

# 審査者は、この主題について何と言っているか —— 主題ごとの記録

**`ACD-1.0.review-precedents.md` から 2026-09-09 に切り出した。節番号は変えていない**ので
既存の `§1.4x` / `§1.5x` / `§1.6x` 参照はそのまま解決する。

**境界は「何についての記録か」である。** 向こうは「**この提出はどう扱われたか**」（1 つの提出の
顛末）、本書は「**審査者はこの主題について何と言っているか**」（複数の提出を横断する主題）。

**読み方の規律は同じ** —— 原文を引き、発言者と日付を書き、**その読みが establish しないことを
併記する**。有利な材料も落とさない。

---

## 1.49 人格権 —— リストの日本人参加者が 2024 年から押している論点で、§12 はその答えである

**ACD-1.0 §12 は、ドシエの中で「なぜこんな条項があるのか」が最も説明を要する節だった。**
アーカイブを人格権で走査したところ（2026-09-08）、**この論点はリスト上で 2024 年から
繰り返し提起されており、しかも提起しているのは日本の参加者である**ことが分かった。

### 何が言われているか（原文・発言者・日付）

**Shuji Sado 氏（2024-09・`license-review`）** —— Blue Oak Model License について:

> In March, I pointed out that the Blue Oak Model License does not consider moral rights.
> **The consensus in this thread was that, for software programs, not considering moral rights is
> not an issue in most jurisdictions worldwide, but it can be a problem in East Asian countries,
> particularly in Japan.**

> …after discussions with multiple legal department members who hold law degrees, it was determined
> that **in Japan, the Blue Oak License retains moral rights with the authors, posing a risk that
> usage could be stopped at any time. This cannot be considered an Open Source Data license.**

> In the case of the Apache 2.0 License, it explicitly states "copyright license," but it also
> grants irrevocable permission for acts such as reproduction, distribution, and modification.
> **This is interpreted as a declaration that moral rights will not be exercised.**

> I recently learned that **Japan applies moral rights most strictly among countries**.

**Carlo Piana 氏（2023-11）—— 反対の見方**:

> On the moral rights, mind that **these are not licensable**, so anything the license says one way
> or the other, nothing changes. I take the opinion that moral rights are probably not relevant in
> software as they are in creative…

**別の参加者（2023-11・Blue Oak を論じて）**:

> **The CC0 mechanism (promise not to exercise or assert any remaining rights) seems much clearer.**

### §12 がそれぞれにどう答えるか

| 論点 | ACD-1.0 |
|---|---|
| 日本では人格権が著作権と別個で、**最も厳格に**運用される。触れないライセンスは「いつでも利用を止められる」risk を残す | **§12 が正面から扱う唯一の節である。** §12.1 が放棄可能な範囲で放棄し、§12.2 が**放棄不能な法域では不行使の合意**を置く |
| 人格権は **licensable ではない**（Piana 氏）ので、条項は無意味ではないか | **§12.2 は許諾ではなく covenant（不行使の合意）である。** 「譲渡・放棄できない権利」でも「行使しないと約束する」ことはできる、という区別に依っている。Piana 氏の指摘は**放棄構成（§12.1）にだけ当たり、covenant 構成（§12.2）には当たらない** |
| CC0 の「残る権利を行使しないと約束する」機構のほうが明確だ | **§12.2 はその機構である**（§5 の covenant not to assert と同じ設計）|
| Apache-2.0 は「不可逆の許諾」を人格権不行使の宣言と**解釈で**読ませている | **ACD-1.0 は解釈に依存しない** —— §12 が明文で述べる。**日本法の下で最も強い形は、解釈ではなく明文である** |
| 人格権は**著者の死後も存続**し、遺族や公的機関が行使しうる | **§12.4 がそこまで縛る**（承継人・相続人・遺言執行者・死後に行使しうる者）。**この節の存在理由は「最も長く残る risk」である**と条文自身が述べている |
| 人格権が守る「氏名表示を偽られない利益」まで放棄させるのか | **§12.5 が明示的に留保する**（§11.3 の虚偽表示は covenant の外）。**放棄しない部分を書いてある** |

### 我々にとっての意味

1. **§12 は思弁ではなく、リスト上の実際の未解決論点への回答である。** しかも
   **提起者は日本の参加者で、Dedicator も日本にいる。**
2. **不利な側も同じ強さで書く**（`against.md` #104）—— Piana 氏の「人格権は licensable でない」は
   §12.1 への有効な批判であり、**§12 全体が無意味だと読まれる余地がある**。答えは
   「§12.2 は許諾ではなく covenant」だが、**それは条文を読ませて初めて通る答え**である。
3. Sado 氏の基準（人格権を扱わないものは「Open Source Data license とは言えない」）は**高い**。
   ACD-1.0 はその基準の正しい側に立つが、**基準が存在すること自体は覚えておく**。

---

## 1.50 「著作権だけでは足りない」—— #102 と正面から対立する 3 つの発言

#102（Rob Landley 氏「一つの instrument に一つの権利。特許を許諾したいなら**別のライセンスを
並べろ**」）は、我々の構造への最も直接的な反論である。**同じアーカイブに、逆向きの発言が
3 つある**（2026-09-08 に走査して発見）。

**Pamela Chestek 氏（2025-03・ModelGo 審査・当時 OSI Licensing Committee）**:
> 2.5(a) — you have **reserved rights that may be needed for someone to exercise the full grant
> required for an open source license**, in particular because you expressly aren't granting rights
> in database. **One theory for the protection of models is database rights, so you might have
> unintentionally withheld the right to reproduce the Model.**

**Carlo Piana 氏（2023-01）**:
> The only rights the license mentions are under Copyright … There is **no mention of other
> controlled rights necessary to use of the software, such as database rights or patents**.
> Suppose I am a patent holder of a work of mine and I license said work under this license.
> **Can I later go after my licensees under the patent regime**…?

**Carlo Piana 氏（2023-07）**:
> …**pure copyright licenses excluding all other rights**, therefore at least the non-patent
> licenses **do not meet the OSD**, since they expressly carve out patents

### 何が対立しているのか

| Landley 氏（#102） | Chestek 氏・Piana 氏 |
|---|---|
| 権利の種類ごとに**別の instrument** を並べよ。0BSD は著作権だけのライセンスである | 著作権だけに届く許諾は、**受領者が実際に必要とする権利を留保してしまう**。とくに**モデルはデータベース権で保護されうる**ので、それを許諾しないと**モデルを複製する権利を意図せず withheld している** |

**両者は「別々に扱え」と「1 つの文書に入れろ」で対立しているのではない。**
Landley 氏が言っているのは**文書を分けろ**であり、Chestek 氏・Piana 氏が言っているのは
**取りこぼすな**である。**ACD-1.0 は両方を満たす形になっている** ——

- **取りこぼさない**: §1.5 の Covered Rights が著作権・実演・放送録音・**sui generis データベース権**
  を含み、**§7 がデータベース権を独立に扱い**、§8 が特許、§12 が人格権を扱う。
- **混ぜない**: §1.5 は特許・商標・人格権を **Covered Rights から明示的に除外**して、
  それぞれ §8 / §11 / §12 へ送る。**種類ごとに節が分かれている。**

**残る争点は 1 つだけ**: 「別々」は**別の文書**でなければならないか、**別の節**でよいか。
Apache-2.0 は 1 文書で著作権と特許（§3）を扱って承認されている。**この 1 点に絞れば議論は短い。**

### ACD にとっての含意（有利・ただし条件つき）

**AI モデルにデータベース権が効きうる、という指摘は、我々の §7 が存在する理由そのものである。**
しかも指摘者は Licensing Committee の委員長で、**別の AI ライセンス提出者に対して
「モデルの複製権を意図せず留保している」と述べた**。ACD-1.0 はその失敗をしていない。

**条件つきである理由**: これは「§7 があってよかった」を示すが、**§7 の書き方が正しいことは
示さない**。データベース権は EU 由来の制度で、法域ごとに存否も範囲も違う。
§7 の妥当性そのものは依然として法的レビューを受けていない（#5 / #79）。

---

## 1.52 「弁護士が要る」への実務的な答えは、審査そのものである

§1.51 の McCoy 氏の発言（この類型で弁護士なしは *"isn't likely to result in something functional"*）は
**我々に反論の材料が無い**指摘だった。**だが同じアーカイブに、その指摘の実務的な帰結が書いてある。**

**Carlo Piana 氏（2024-12・PBZC 審査）**:
> OSI requires prior review by a lawyer because there are things that a layman very likely cannot
> consider, not just to enrich lawyers (**who mostly do this job pro bono, as we are doing now**).

**Carlo Piana 氏（2024-09・別の提出者へ）**:
> I second the opinion that you should probably withdraw the submission and consider the valuable
> advice you have been provided with (**for free**).

**Josh Berkus 氏（2025-07・BOS の提出者へ・OSI Board Member として）**:
> We are approaching 2 months from the submission of this license, **our usual interval for
> examination**. You've received some critical feedback from **our volunteer attorneys**. Do you
> plan to revise the license submission, or keep it as it is?

### 読み取れること 3 点

1. **このリストの審査者は、pro bono で働く弁護士たちである。**（Piana 氏の "as we are doing now" は
   自分自身を含めた記述である。）**単独・無資金の起草者が条文に弁護士の目を通す実務的な経路は、
   提出することそのものである。** McCoy 氏の指摘への答えは「反論」ではなく**「その通りであり、
   だからこそ提出する」**である。
2. **ただしこれは「弁護士が起草した」とは違う。** 受けられるのは**起草の代行ではなく批評**で、
   しかも**提出後**にしか来ない。`submission.md` §B.0 が法的レビューの不在を先に述べるのは、
   この順序を偽らないためである。
3. **審査の標準的な間隔は約 2 か月**で、その時点で **「改訂するのか、このまま行くのか」を
   聞かれる**。オーナー方針（届いた議論を全部取り込んで改訂版を出す）は、
   **この問いに対する答えとして既に用意されている**（`REVISION-PROTOCOL.md` §1〜§2）。
   **聞かれてから考えるのではなく、聞かれる前から決めてある**ことがこの track の設計である。

**この節が establish しないこと**: pro bono の批評を受けられることは、**批評が好意的である
ことを意味しない**（§1.51 の McCoy 氏の発言自体がその批評である）。また、
**批評を受ける前提は「要求情報を満たした提出」**であって、満たしていなければ
コメントは付かない（#97・Piana 氏 2026-09 / McCoy 氏 2024-10・2026-03 の 3 例）。

---

## 1.55 非ソフトウェア資産と AI エージェントの「スキル」—— 我々が実際に配っているもの（2026-04）

ACD-1.0 は**リポジトリ全体**（ソース・文書・データ・メディア資産、そして
`.well-known/` の **Agent Skills**）に適用されている。**その適用形態そのものが議論された
スレッドがある**（`license-discuss` 2026-04・Moming Duan 氏の問題提起）。

**問い**: スキル（AI コーディング支援への指示セット）に明示的なライセンスは要るのか。
そもそも著作物なのか。米国著作権局は「プロンプトだけでは十分な人的支配を与えない」と結論して
いるのではないか。従来の OSS ライセンスは適切なのか。

**Richard Fontana 氏（Red Hat・2026-04-06）の回答が 3 点とも我々に効く**:

> "Instructions" **can be copyrightable works**. I think at least some skills files are likely
> copyrightable.

> The document does not state that. Rather, it says that **prompts alone do not provide sufficient
> human control over AI-generated *outputs*** to confer human authorship and thus copyrightability
> **over the outputs**. It references [Part 2] that appears to endorse the view … that
> **sufficiently creative prompts may be copyrightable**.

> it's already the case that **open source software licenses are extensively used for non-software
> material** in open source project repositories. My general view is that **traditional open source
> software licenses are completely appropriate** for association with such material if they are
> copyrightable.

### 我々にとっての意味

1. **「ソフトウェア用のライセンスを非ソフトウェア資産に当てている」ことは、この場では異常では
   ない。** Fontana 氏が *"extensively used"* かつ *"completely appropriate"* と述べている。
   **ただし Carlo Piana 氏（2023-07）は逆に近いことを述べている** —— *"the only non-software
   specific licenses we approve are those bearing a total waiver of any right so that the work
   becomes nearly public domain"*。**両方を記録する** —— そして**その「total waiver に近いもの」は
   ACD-1.0 の形そのもの**なので、2 つの見解は我々については同じ結論へ収束する。
2. **§9 が navigate している区別を、この場の第一人者が正確に述べている** ——
   **プロンプトは著作物たりうる / そこから生成された出力は人的著作性を欠きうる**、は別の命題である。
   **§9.2 が「表明しない」のは、この区別が未確定だからであって、不勉強だからではない。**
   **よくある誤読（「著作権局はプロンプトは著作物でないと言った」）を、Fontana 氏がその場で
   訂正している** —— 我々もその誤読を繰り返してはならない。
3. **我々が配っている Agent Skills は、この議論の対象そのものである。** ACD-1.0 を
   リポジトリ全体に当てるという選択は、**この論点に対する 1 つの答え**になっている
   （スキルが著作物なら許諾が及び、著作物でないなら許諾は無害である —— §2.7 が
   「Dedicator が保有する権利」に射程を閉じているので、**どちらでも壊れない**）。

---

## 1.56 我々の投稿の 1 つ前のメッセージが、我々のやっていることを標準化していた（2026-08-25）

**アーカイブ上、我々の 2026-08-26 の投稿の直前にあるのは Matija Šuklje 氏のこのメッセージである**
（同じリスト・前日）。**クライアントサイドの JavaScript / CSS に著作権とライセンス情報を
どう載せるか**について、*"after several workshops and iterations, **a bunch of us finally agreed
to a solution**"* として 4 段の手順を示している:

1. **REUSE.software のベストプラクティスを適用する**（他の言語と同じように）
2. **SBOM（SPDX / CycloneDX）か attribution file を、好きなツールで生成する**
3. **その file/page を `<head>` の `<link rel="license" href="">` で指す**
4. **web UI にも `<a rel="license" href="">` で提示する**

### 我々が満たしているもの / いないもの（2026-09-08 実測）

| 手順 | 本リポジトリ |
|---|---|
| 3. `<head>` の `<link rel="license">` | **満たす** —— `grep -n 'rel="license"' index.html`（Check 444a が BLOCKING で強制）|
| 4. UI 内の `<a rel="license">` | **満たす** —— `js/components.js` の sidebar/drawer 共通部（`rel="license noopener noreferrer"`）|
| 1. REUSE のファイル単位ヘッダ | **満たさない** —— shipped の HTML / CSS / JS に `SPDX-License-Identifier` ヘッダは **1 つも無い**（`against.md` #106）|
| 2. SBOM / attribution file | **問題自体がほぼ生じない** —— C1（Boring Technology・外部フレームワークとライブラリ **ゼロ**）により、**配信物に第三者コードが含まれていない**。この手順が解こうとしている「束ねられた minified ライブラリのライセンス情報が失われる」問題が、この配信物には存在しない |

### 3 つの観察

1. **手順 4 は 2026-09-06 に #85 として独立に実装した。** その時点でこのスレッドは読んでいない。
   **「機械にだけ伝えて人間に伝えていなかった」という自分の発見が、10 日前にリスト上で
   合意されていた解決策と一致した。** —— 収束は嬉しいが、**先に読んでいれば 10 日早かった。**
2. **手順 2 が我々に当たらないのは、アーキテクチャの選択（C1）の帰結である。**
   これは「やらなくてよい」ではなく「**問題が生じない構造にしてある**」という主張なので、
   **主張として書いておく必要がある**（黙っていると「SBOM が無い」とだけ見える）。
3. **手順 1 は素直に未達である。** ドシエは機械可読なライセンス宣言を強みとして述べている
   （6 面の cross-surface coherence を Check 444 が強制）が、**REUSE は「面」ではなく
   「ファイル単位」の標準**で、そちらは 1 つも無い。**強みを主張している領域の、名指しできる欠落。**

---

## 1.58 「OSD 違反ではないが、採用されるかは別問題」—— 特許条項の広さが uptake を下げるという指摘

**ACD-1.0 §8 が最も広い形を取っている当のことについて、審査者が名指しで懸念を述べた記録がある。**
これは我々が**差別化として提示している箇所**（§8.4）に当たるので、同じ強さで書く。

### 原文（McCoy Smith 氏・`license-review` 2026-05-14・ModelGo 宛）

> Finally, the termination provision for patent assertions applies to Derivative Works. There's a
> long-standing debate about whether that sort of termination is overbroad… One of the reasons why
> the newer, popular licenses articulate their defensive termination/suspension clauses more
> narrowly than this is because of the concern that **patent holders would be reluctant to grant an
> open-ended patent license to downstream licensees**. **I don't think that's an OSD violation, but
> it is an issue as to whether a license of this scope would gain significant uptake at least from
> patent holders.**

**同じ人物が 2026-09-07 の CALL FOR COMMENTS で、これを 4 問中 2 問に組み直している** ——
Q3（終了が Licensor にしか向かない非対称は OSD 5 の問題か / 特許主張が著作権の許諾まで終わらせてよいか）と
Q4（引き金が Derivative Materials にまで及ぶのは広すぎないか。*"Most of the OSI-approved licenses
that have patent assertion termination clauses limit them to assertions against the licensed work,
not subsequent derivatives."*）。**1 年 4 か月にわたって同じ論点が生きている。**

### ACD-1.0 に当たるか —— 二段に分けて答える

**当たらない部分（形式）**: ACD-1.0 には**特許報復条項が存在しない**。§8.2 は
*"This Dedication contains no patent retaliation provision, and its absence is deliberate."* と
明言し、§10.4 は何も終了しない。**Q3・Q4 が問うている条項が無いので、その問いは当たらない。**

**当たる部分（実質）**: McCoy 氏の懸念の中身は終了条項そのものではなく、
**「特許権者は、下流の受領者へ開放的な特許許諾を与えたがらない」**である。
その尺度で見ると **ACD-1.0 は ModelGo より広い** ——

| | ModelGo Attribution 2.0 | ACD-1.0 |
|---|---|---|
| 特許許諾の範囲 | Licensed Materials とその派生 | Work とその派生（§8.1）**＋ 訓練済みモデル・パラメータ・出力**（§8.4）|
| 取り戻す手段 | 特許主張があれば終了できる | **無い**（§8.2 が明示的に無条件・終了不能と述べる）|

**つまり我々は、McCoy 氏が「uptake を下げる」と述べた方向の極限に立っている。**
差別化として提示している §8.4 は、**その尺度では最も採用されにくい形**である。

### これが establish すること / しないこと

- **establish する**: 承認の障害ではない。McCoy 氏自身が *"I don't think that's an OSD violation"*
  と述べている。**OSD 適合と採用可能性は別の軸である。**
- **establish しない**: 「だから ACD-1.0 は採用されない」。彼が述べたのは**特許権者からの**
  採用についてである。同じスレッドで Moming Duan 氏が反対側を書いている ——
  *"patent holders are likely to be larger companies with the resources to file for patents and
  obtain legal advice on their IP rights. Would such patent holders be likely to use a template
  license, or would they have a bespoke license?"*（2026-05-15）。
  **この反論は ACD-1.0 にもそのまま当たる。**

### なぜこれを不利な事実として記録するか（#107）

**SPDX は「相当程度の実使用」を要求し、我々の実績は 1 件である**（`READY-TO-SUBMIT.md`
「残る弱点」2）。uptake を下げる設計は、**OSI の承認では問題にならないが SPDX の条件では
直接効く**。**我々がいちばん弱い軸に、我々がいちばん強いと主張している条項が乗っている。**

### 同じ発言の中に、我々にとって有利な実測もある

McCoy 氏は同じメッセージの直前で、特許許諾の**動詞の列挙**についてこう述べている ——
*"I understand there are precedents from prior licenses (BSD is the best example) for not fully
articulating all of these rights, but **I think that precedent shouldn't be used to allow for
incompletely written licenses now.**"*

**ACD-1.0 §8.1 は 6 つすべてを列挙している** —— *making, having made, using, offering to sell,
selling, importing, or otherwise transferring*。§8.4 も同じ列挙を繰り返す。
**この指摘は当たらない**（`AS-OF.md` に日付つきで記録した）。**有利な実測を落とすと、
不利な一覧は「不利に間違える圧力」の下で偏る**（`BLIND-SPOTS.md`「引き継ぎで失われるのは
事実ではなく枠」(1)）。

---

---

## 1.59 §12 の穴は「日本では」だけではない —— 法域の分岐と、#84 への接続（§1.49 の続き）

> **⚠ この節は当初「本セッションで最も重い発見」として書かれた。それは誤りだった。**
> **§1.49 が同じ論点を 2026-09-08 に既に記録している** —— Shuji Sado 氏が Blue Oak について
> *"in Japan, the Blue Oak License retains moral rights with the authors, posing a risk that usage
> could be stopped at any time"* と述べた `license-review` 2024-09 の投稿、Piana 氏の反対、
> §12 の各条への対応表まで在る。**新しい引用を 1 つ見つけたことを、新しい論点を見つけたことと
> 取り違えた。** 節は残すが、**§1.49 との差分だけを述べる形に書き直した**（2026-09-09）。

**§1.49 に対して本節が足すのは 3 つである。**

### (1) 発端は 2024-03 の `license-discuss` で、根拠は条文である

§1.49 が引くのは 2024-09 の `license-review` 投稿だが、**議論はその半年前に別のリストで
始まっている**。Sado 氏・`license-discuss` 2024-03-13 / 03-14 / 03-23:

> In Japan, copyright, which is a property right, and moral rights are separated… The BlueOak
> license clearly states "copyright," but this would probably be interpreted in Japan as **not
> including moral rights**.

> Japanese law recognizes the right of identity preservation **even for software**… Article 20(1)
> The author of a work has the right to preserve the integrity of that work… Usually, in Japan,
> contracts related to intellectual property rights always include a clause stating that
> **"the author shall not exercise moral rights."**

> To summarize the discussion so far, **the Blue Oak license is not open source, at least not in
> Japan.**

**§12.2 はその「行使しない旨の合意」そのものである。** §1.49 は「covenant である」と述べたが、
**それが日本の実務上の標準形だという裏づけは無かった。** ここで付いた。
**同じ人物が 2025-10-17 に、放棄一般についても同じことを述べている** ——
*"practice relies on **non-assertion covenants rather than blanket waivers**… a pure 'waiver'
rarely bites on its own."*

### (2) 法域の分岐 —— これは §1.49 に無い

**同じスレッドで、穴が普遍的でないことが示されている。**

| 法域 | 同一性保持権はソフトウェアに及ぶか | 出所 |
|---|---|---|
| 日本 | **及ぶ**（著作権法 20 条 1 項・例外は 20 条 2 項 3 号）| Sado 氏 2024-03-14 |
| 韓国・台湾 | **及ぶ**（構造が同じと同氏が調査）| Sado 氏 2024-03-15 |
| 英国 | **及ばない**（CDPA 1988 s.81 がプログラムを除外）| David Woolley 氏 2024-03-14 |
| スロベニア（および大陸欧州の多く）| **及ばない**（同一性保持権は software に適用されないと明記）| Matija Šuklje 氏 2024-03-13 |

**§12 が埋める穴は法域固有である。** 「どこでも incumbent が壊れている」ではない。

### (3) #84 への接続 —— これも §1.49 に無い

§1.49 は §12 を「リスト上の未解決論点への回答」として位置づけた。**本節はそれを
「なぜ 0BSD が在るのにもう 1 つ作るのか」（#84・Rob Landley 氏）への答えとして使う。**
#84 に対してこれまで書けたのは「1 件足す費用が低い」＋不在の 3 主題
（学習と TDM / モデルと出力に及ぶ特許 / 機械生成物）だけで、**人格権はその一覧に無かった。**
0BSD も MIT-0 も Unlicense も人格権に触れないので、**上表の左半分の法域では、
incumbent は「著作者がいつでも改変を止められる」状態を残している。**

### establish しないこと

- **リストはこの結論を採用していない。** Pamela Chestek 氏は同スレッドで
  *"Wouldn't the same criticism hold true for all the other licenses too?"* と返している ——
  **そのとおりで、だから差分になる**が、「では新しいライセンスが要る」への同意ではない。
- **§12.2 が日本法の下で機能するかは、弁護士が確かめていない**（弱点 1）。
  Sado 氏が述べたのは「実務がそうしている」であって「この文言で足りる」ではない。
- **#104 は消えない。** Piana 氏の *"these are not licensable"* は §12.1 に当たる。

---

## 1.60 委員長が 3 か月前に「長さ」を承認しない理由として述べている —— そして我々はその数を測っていなかった

**Linkumori Free License への Pamela Chestek 氏の返信**（`license-discuss` 2026-06-23）。
**Licensing Committee 委員長**であり、`license-review` の審査を主導している人物である。

> That said, your license seems to be undergoing substantial **mission creep**. You originally said
> it was to address the problem of attribution in a web-based context, but now you have added
> **moral rights**, a secondary license clause, and I don't know what else. **It is now 3888 words,
> longer than the GPLv3. It is excessively wordy and proscriptive. These qualities mean that no one
> other than you will ever use this license, so it does not seem to be a good candidate for
> approval.**

**この 1 段落に、我々に当たるものが 3 つある。**

1. **長さそのものが「承認の候補として良くない」理由として述べられている。** #6 はこれまで
   我々自身の懸念として書かれていた。**委員長の発言として、しかも数つきで存在する。**
2. **人格権条項の追加が mission creep の例として名指しされている** —— §1.59 で我々が
   「incumbent に無い穴」として評価した当のものである。**同じ条項が、片方から見れば差別化で、
   片方から見れば肥大である。**
3. **推論の形**: 冗長 ∧ 命令的 → **他の誰も使わない** → 承認の候補として良くない。
   **最後の 2 つは我々にも当たる**（採用実績 1 件・#2）。

### そこで数を測った（2026-09-09）

**この節を書くまで、我々は ACD-1.0 の語数を一度も測っていなかった。**
#6 は「16 節 / 82 項 / 597 行」とだけ述べていた ——**審査者が使う単位（語数）ではない。**

| | 全文 | 本体（前文・付録を除く） |
|---|---|---|
| GPL-3.0 | **5,644** | **4,617** |
| **ACD-1.0** | **4,896** | **4,574** |
| Linkumori（委員長が「GPLv3 より長い」と述べたもの） | 3,888（本人申告） | — |

**ACD-1.0 は GPLv3 より長くない。** 本体で **43 語短く**、全文で **748 語短い**。

**そして委員長の比較は、我々が測れるどの測り方でも成り立たない** ——
3,888 は GPLv3 の本体 4,617 より短く、全文 5,644 より短い。
**これを「委員長が間違えた」と使ってはならない。** 別の数え方（節の一部だけ、あるいは別の版）を
していた可能性があり、**我々は本人の測り方を知らない**。記録するのは我々の測定であって、
彼女の誤りではない。

### この発見が両刃である理由

**有利**: 長さの反論に対して、初めて**測った数**で答えられる。しかも
「GPLv3 と同程度」は、この文脈で最も分かりやすい基準である。

**不利**: 彼女の批判の核は数ではない。*"excessively wordy **and proscriptive**"* → *"no one other
than you will ever use this license"* である。**ACD-1.0 は proscriptive ではない**（§10.1 が
条件を一切課さない・§4.3）が、**「他の誰も使わない」は採用 1 件の我々により強く当たる**。
**数で反論して、推論の残り半分に答えないのは、いちばん都合のよい半分だけ取ることになる。**

---

---

## 1.61 「献呈なのかライセンスなのか、どちらかにせよ」—— 委員長が我々の中核構造に当たる言葉を書いている（2025-10）

**ACD-1.0 の中核は §3（献呈）と §4（許諾）を並置し、§4.4 で「独立に付与される」と述べる構造で
ある。** その構造に**そのまま当たる文**が、`license-discuss` に 11 か月前から在った。

### 原文（Pamela Chestek 氏・`license-discuss` 2025-10-16・PUWL v1.0 宛）

> **Which is it, a dedication to the public domain or a license? You can't have it both ways.**
> A dedication to the public domain is a full release of any and all rights, but a license is a
> way to exercise some control. You say that you want to have a dedication to the public, with
> various fallback positions if the law doesn't allow it, **but then you are nevertheless trying to
> retain some rights**

彼女が「留保」として名指ししたのは **4 つ**である ——
(a) 虚偽の著作者主張を認めない条項 / (b) 違法な利用を許さない条項 /
(c) 特許訴訟による自動終了 / (d) 責任の否認。そして:

> These provisions are **retention of rights**, contrary to the statement that the author is
> releasing all rights whatsoever in the work… You can only enforce them if you are **maintaining
> ownership of some rights** in the work… **The document is internally contradictory.**

### ACD-1.0 を 4 点に当てる（条文を読んで確かめた・2026-09-09）

| 彼女が挙げた留保 | ACD-1.0 |
|---|---|
| (b) 違法な利用を許さない条項 | **無い**（`grep -i 'unlawful\|illegal'` で 0 件）|
| (c) 特許訴訟による終了 | **無い。** §8.2 が *"contains no patent retaliation provision, and its absence is deliberate"* |
| (d) 責任の否認 | **有る**（§13 / §14）。**ただし承認済みライセンスはすべて持つ**ので、この項目は我々を他と区別しない |
| (a) 虚偽の著作者主張 | **有る** —— §11.3 と §12.5。**ここが当たる** |

**「all rights whatsoever を放棄する」という第一文は、*operative な条文には* 無い。**
§3.1 が surrender するのは **Covered Rights** という定義された集合で、§1.5 が特許・商標・人格権を
そこから除き、§2.7 が一般的な限界を述べる。

> **⚠ 2026-09-09 に、この段落は不十分だと分かった（#114）。** 条文だけを見て
> 「定義によって回避されている」と書いたが、**PREAMBLE は見ていなかった。**
> 前文は *"It **gives everything away**, once, without conditions"* と述べており、
> **これは Chestek 氏が突いた形そのものである。** 訂正の詳細は §1.65。

**§11.3 は、この反論を予期して書かれている** ——
*"This Section states a **limit of the Dedication's reach**; it is **not a condition upon You**,
and Section 10.1 is unaffected by it."* つまり「留保した権利を行使する」のではなく
「そもそも Dedicator のものではなかったから許可のしようがない」という形にしてある
（*"it was never the Dedicator's to permit"*）。§11.4 が privacy / publicity / データ保護について
同じことをする。

### それでも不利な事実として記録する理由（#110）

**反論は 1 文、答えは 4 条である。** *"You can't have it both ways."* に答えるには
§11.3 の最終文・§10.1・§1.5・§2.7 を読ませる必要がある。
**#100 / #101 / #104 と同じ非対称**で、この非対称そのものが不利である。

**さらに悪いのは、彼女が挙げた 4 つのうち我々に当たる 1 つが、我々自身の言葉と衝突すること。**
ドシエは ACD-1.0 を「**何も留保しない instrument**」と繰り返し述べてきた（#6 の書き出しがそれ
である）。**§11.3 と §12.5 は、少なくとも表面上は留保に見える。** 我々の説明は正しいと考えるが、
**「留保していない」と一言で述べる書き方は、この反論に対して最も弱い形**である。

### 有利な側も同じ強さで

**この 1 通は、ACD-1.0 が回避している設計上の失敗を 3 つ名指ししている** ——
違法利用条項 / 特許報復 / 全面放棄の宣言と個別留保の同居。
**§8.2 が「不在は意図的である」と本文に書いてある理由**が、ここに実例として存在する。
`comparison.md` §1.53（PUWL の「撤回不能」と「自動終了」の同居）と同じスレッドの、より深い層である。


---

---

## 1.64 「法的レビューも実使用も無い」を**接続詞で**言われた記録（2021-02・Ritchey Permissive License v11）

**ドシエは「弁護士が読んでいない」（#5 / #79）と「採用が 1 件」（#2）を別々の不利な事実として
持ってきた。** リスト上では、この 2 つは **1 文の中で結ばれて**承認しない理由として述べられている。

### 原文（Lukas Atkinson 氏・`license-review` 2021-02-14）

> I would ask the Board to not approve this license: it leads to unnecessary license
> proliferation, and likely fails to provide sufficient software freedom.
>
> On a meta-level, the submission of this license makes a strong argument that **submitted licenses
> should have either received legal review or at least non-negligible use. This license has
> neither**: not even the license author seems to have published any works/material under this
> license…

**ACD-1.0 はその 2 つの条件について、片方は満たさず、もう片方は 1 リポジトリである。**
（Ritchey 氏との差は、我々は**実際に自分の全リポジトリへ適用している**点だけである。）

### 「良い性質があるから」は先に潰されている

提出者が「法的レビューはライセンスが持ちうる多くの性質の 1 つに過ぎず、本ライセンスは
他の質を持ち込む」と述べたのに対し、**McCoy Smith 氏（2021-02-15）**:

> licenses are legal instruments, and **OSI approval is a mechanism that presents approved licenses
> to the community as having value as a legal instrument.** Under your theory, a submitted license
> that is unquestionably legally invalid should nevertheless be approved if it has good ideas in it
> or the submitter feels strongly about it…

**これは §4c（「弁護士が読んでいないことに対置する機械的検証」）へ直接向く警告である。**
§4c は「代替にはならない」と明記してあるが、**明記してあることと、そう読まれることは別**である。

**Josh Berkus 氏（2021-02-14）**はさらに直接的だった:

> Given this statement, why would we take this license submission seriously? This is like
> submitting a PR to someone else's repository with the commit message "I didn't do any tests or
> use any linting tools". **That's an automatic rejection in most OSS projects I know.**

**Russell Nelson 氏（2021-02-22）**: *"Programmers writing legal documents are like programmers
creating user interfaces. **Don't. Just don't.** You have skills, and you're smart, but nobody is
skilled at everything."*

### 反対側 —— 同じ強さで

**§1.52 が記録しているとおり、リストには逆向きの発言もある。**
Pamela Chestek 氏（PBZC 審査 2024-12）は法的レビューを *"recommended"* であって
*"not a blocker"* と述べ、Josh Berkus 氏自身も 2025-05 に同趣旨を述べている。
**つまり「必須ではない」は制度の言明、「無いなら承認しない」は参加者の議論であり、
両方がこのリストに在る。** 我々が選べるのは**どちらを引くか**ではなく、**両方あることを
先に書くか**だけである。

### 当たらないもの（同じスレッドから 3 件・条文で確認）

| Ritchey 提出への指摘 | ACD-1.0 |
|---|---|
| *"permission to do anything **lawful**"* が OSD 違反になりうる。Carlo Piana 氏: *"it's **no business of a license** to limit use of software to what is lawful"* | **合法性への言及が本文に無い**（`unlawful` / `illegal` の出現 0 件・#110 で実測済み）|
| 裁判管轄条項（*"only occur in the courts of British Columbia"*）—— McCoy 氏「**間接的に差別的**でありうる」/ Berkus 氏「**国家の禁輸で違反しうるライセンスは OSD 5 違反**というのがこの団体の方針だった」| **§15.7** —— *"This Dedication specifies **no governing law and no forum**."* |
| 「この素材はこのライセンスの下に留まらなければならない」が copyleft 義務と読まれた | **§10.1** が条件を一切課さず、**§4.5** が「条件が無いので再頒布は自由」と明言する |

### 我々にとっての意味

**objection-map.md の「この表の限界」2（**反論は組み合わさる**）に、名前と日付が付いた。**
個別に答えられる 3 つ（長さ・採用・弁護士）が、**1 文にまとめられた形**で 2021 年から
存在している。**答えを 3 つ用意しておくことと、束ねられた 1 文に答えられることは別である。**

---

## 1.65 前文が「everything を渡す」と述べ、条文が 4 か所で渡していない —— 自分の主張の訂正（#114）

**§1.61 で「Chestek 氏が突いた形（全部放棄と言いながら留保する）は ACD-1.0 には無い」と書いた。
条文を読んで書いた。前文を読んでいなかった。**

### 事実

**PREAMBLE（第 2 段落）**:

> This Dedication is written for works that are meant to be learned from.
> **It gives everything away, once, without conditions**, and it speaks in the three places where
> the existing tools are silent or hostile: machine learning, patents, and machine authorship.

**そして条文は、4 か所で「everything」ではないと述べている。**

| 渡していないもの | 条文 |
|---|---|
| 商標・サービスマーク・商号・ロゴ・人名 | **§11.1** *"grants no right in any trademark…"* |
| データ保護・プライバシー・パブリシティ・人格の権利 | **§11.4** *"It reaches nothing else… any permission those laws require is not the Dedicator's to give"* |
| 虚偽の著作者主張 | **§11.3** *"Representing that the Dedicator authored, endorsed… is outside what this Dedication reaches"* |
| Dedicator が保有していない権利一般 | **§2.7** |

**Chestek 氏が PUWL について書いたのは、まさにこの形である**（`rounds/` 参照）——
*"These provisions are **retention of rights**, contrary to the statement that the author is
releasing all rights whatsoever… **The document is internally contradictory.**"*

### 反論できる材料（誇張せずに）

1. **前文は自分が非 operative だと宣言している。** 見出しが
   *"PREAMBLE (informative; not part of the operative terms)"* であり、末尾が
   *"Sections 1 to 16 are the operative terms. This preamble is not, and **nothing in it qualifies
   them.**"* である。**PUWL にはこの標識が無かった。**
2. **"without conditions" の側は正確である**（§10.1）。不正確なのは "everything" だけである。
3. **§11.3 と §11.4 は「留保」ではなく「reach の限界」として書かれている** ——
   *"it was never the Dedicator's to permit"*。**Dedicator が持っていないものは渡せない**、
   というのは全部渡すことと矛盾しない。**この読みが通れば "everything" は正しい**
   ——「Dedicator が持っている everything」の意味で。
4. **§11.1（商標）だけは、その読みでは救えない。** 商標は Dedicator が**持っている**権利であり、
   §1.5 が意図的に Covered Rights から外している。**ここは正真正銘の留保である**
   （ただし `against.md` の記録どおり、**商標を渡さないのは全承認済みライセンスの標準**である）。

### 何を学んだか

**「条文にはこう書いてある」で反論を退けるとき、条文の外にある文を数えていない。**
前文・§16.1 の推奨 notice・`machine.json` の `notice` フィールド・提出文 §B.0 ——
**審査者が読むのはそれらも含めた文書全体**である。#110 の答えを書いたとき、
**4 つのうち 1 つしか見ていなかった。**

これは #111（文ではなく論点を grep せよ）と同じ族の、**面の側**の失敗である。
一般形: **自分の instrument について何かを主張するときは、その主張が及ぶ面をすべて列挙してから
確かめる。** 面は条文だけではない。

---

## 1.67 `license-discuss` を pre-review として使った唯一の先例（2024-09〜10・15 通）

**我々と同じ使い方をしたスレッドが 1 つだけ見つかった。** 提出者は
*"Complying to https://opensource.org/licenses/review-process process, I wish to invite everyone
here to **discuss and pre-review** my newly drafted open-source licenses … **before submitting to
license-review**"* と書いて始めている。

### venue の設計が、否定形ではなく肯定形で述べられている

**McCoy Smith 氏・2024-09-30（同日）**:

> So, if you want this to be reviewed and approved, "license-discuss" is not the right mail list to
> do that. However, **if you want people to give comments before you submit for approval, this is
> the correct mailing list.**

**ドシエがこれまで持っていたのは否定形だけ**だった（「`license-discuss` は承認の窓口ではない」・
2026-08-04）。**肯定形の一次資料はこれが最初**である。**我々の venue 選択は、設計どおりの使い方
である。**

### そして pre-review は、機能するときは速く機能する

同日に McCoy 氏、翌日に Josh Berkus 氏と Pamela Chestek 氏、Bruce Perens 氏、Aaron Williamson 氏。
**15 通。** 条項の具体的な欠陥（特許・営業秘密の不許諾が承認を妨げる）まで踏み込んでいる。

### 我々に当たる 3 つ

**(1) 長さ —— 委員長が「読んでいない」と述べた記録の 2 例目（#116）。**

> **Pamela Chestek 氏・2024-10-05**: I have **not read these licenses in detail** because they are
> **extremely long, approximately 4500 words**, appear from the definitions alone to have way more
> detail than a typical open source license, and **are not understandable**…

**ACD-1.0 は 4,896 語である**（§1.60 の実測）。**彼女が詳細に読まなかったものより長い。**
**ただし理由は連言で述べられている**（長い ∧ 典型より詳細 ∧ 理解できない）ので、
**長さだけを取り出して引くのは相手の理由を歪める。**

**(2) 非弁護士の起草 —— 名前のついた歴史的事例。**

> **Bruce Perens 氏・2024-10-01**: I was expert witness in the appeal of one of the first Open
> Source license cases, which resulted from **Larry Wall drafting the Artistic License 1.0 without
> the knowledge of a legal professional**, resulting in the lower court…

そして 10-05 に *"**there should be some sort of gateway**"* と述べている。
**#113（法的レビューか実使用か）に、最も具体的な形を与える発言である。**

**(3) "shall" —— 当たらない。**

> **Bruce Perens 氏**: The word "SHALL" **must not** be used in a license. Please replace all
> occurrences of "SHALL" with "MUST"…

**ACD-1.0 の "shall" は 0 件、"must" も 0 件である**（実測 2026-09-09）。
条件を課さない instrument なので**義務語がそもそも要らない** —— §10.1 の帰結であり、
Check 441d が列挙した構文の不在を BLOCKING で守っている。
**なお McCoy 氏はこの点で Perens 氏に完全には同意していない**（*"it is one of those things that
is so ingrained in legal drafting that we'll likely never be rid of it"*）—— **リストは一枚岩ではない。**
