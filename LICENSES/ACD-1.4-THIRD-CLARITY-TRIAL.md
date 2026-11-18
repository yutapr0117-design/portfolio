---
file: LICENSES/ACD-1.4-THIRD-CLARITY-TRIAL.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-15
canonical-ref: LICENSES/ACD-1.4-CLARITY-TRIAL.md (§1〜§9・規則はそちらに従う) / LICENSES/ACD-1.4-SECOND-CLARITY-TRIAL.md (§10〜§14) / LICENSES/ACD-1.4-DRAFT.txt (試作の対象・この file は草案を上書きしない) / LICENSES/ACD-1.4-CHANGELIST.md (採用した変更の記録先)
---

# ACD-1.4 草案の明瞭性の試作（3 冊目）—— §15 から

`ACD-1.4-SECOND-CLARITY-TRIAL.md` が 1,000 行の BLOCKING（Check 365）に届いたので（2026-11-15・1,002 行）、2 冊目と同じく
節の単位で分けた。節番号は続き番号で §15 から始める。規則（草案を上書きしない・採用の条件 2 つ・分担）は 1 冊目の冒頭に従う。
§1〜§9 は `ACD-1.4-CLARITY-TRIAL.md`、§10〜§14 は `ACD-1.4-SECOND-CLARITY-TRIAL.md` に残してある。ドシエはそれらを
「SECOND-CLARITY-TRIAL.md §14.N」の形で引いているので、移さない。

試作を採る commit の手順は 2 冊目の §14 と同じ（`measure_clause_overlap.py --compare / --guard / --sync` で測り、草案を直し、
`sync_stated_counts.py --apply` で語数から導出する数を書き直し、冒頭の箇条・束の表・CHANGELIST の主表を手で直す）。
Check 468y は 2 冊目とこの file の両方の「変えない」「退けた」の節を読む。

**この file で足した規則（2026-11-15）**: (1) 2 冊目は 1,000 行の上限（Check 365）の手前なので、§10〜§14 の節への訂正や逆側の追記も、2 冊目には足さず、この file に「§14.N への追記」として書く。(2) 本文に特定の名（組織名・URL・人名）を足す案は退ける —— 承認は一語も変えない本文に対するもので、承認済みの写しは型板として使われる（Nelson 氏 2008・`review-readings-2.md` §1.238）。§16.3（誰でも適用でき、特定のプロジェクトや人に結ばれない）と §16.4 の名の規則も同じ考えに立つ。いま本文に在る固有の名は *Autonomous Commons Dedication* と識別子だけで、§16.1 の雛形の *<location of this file>* は差し込みの印である。(4) 明晰さの試作の根拠: 読めないライセンスは適合しないと推定される —— Fontana 氏 *"It is not really possible to assess as-is, other than to conservatively assume that it's not OSD-conformant."*（`license-review` 2016-06-07・`review-readings.md` §1.209）、Piana 氏「公開のライセンスは作者の意図から離れて単独で読めなければならない」（同日）。2026 年の理事会の *"Poor drafting"* と同じ基準が 10 年前に在った。(3) 一般形（*every other provision* など）を足すときは、自分の条が主語にしているものと、受領者のために働かない条（§13・§14・§16）を量化が巻き込まないかを読む（§15.5）。

## 15. 2026-11-15 からの試作（5 人体制）

### 15.1 T67: §12.2 に Dedicator の同意を足す（+25 語・採った・2026-11-15）

**見つけた経緯**: portfolio-2f が §12.4（人格権の承継）に当てる審査記録を探し、`license-discuss` の PUWL の会話で Sado 氏が日本の事情を踏まえて示した条を見つけた（2025-10-17・`review-readings-2.md` §1.218）: *"… each Licensor and Contributor irrevocably covenants not to assert such rights and consents to all acts that would otherwise infringe them, including modification, combination, and omission of attribution, provided there is no false attribution of authorship. This provision is severable"*。§12.1 / §12.2 / §12.5 / §12.6 とほぼ同じ構造で、差は **同意（consent）** だけだった。Sado 氏は後に委員会の側で `license-review` に書く人だが、この通は個人の提案で、PUWL は審査に出ていない（portfolio-30 が確かめた）。

**Before（§12.2 の第 1 文の後）**: *"… against You or against any person who receives the Work from You, directly or indirectly. You are not required to determine …"*

**After**: *"… directly or indirectly. The Dedicator also consents to any act by You or by any such person that would otherwise infringe those rights. You are not required to determine …"*。§12.4 は *"The covenant and the consent in Section 12.2 bind …"*、§12.5 は *"Neither the covenant nor the consent in Section 12.2 extends to conduct falling within Section 11.3, so the interest that Moral Rights protect against false attribution survives both."*

**欠陥ではなく効果を足す理由**: §12.2 が働くのは人格権を放棄できない法域で、そこで不行使の約束は契約の効果にとどまる。日本の著作権法 20 条 1 項は「意に反して」の改変を侵害とし、同意があれば侵害そのものが成り立たないと読める。英国の CDPA s.87(1) も *"It is not an infringement … to do any act to which the person entitled to the right has consented"* と定める。死後の保護（日本 60 条）も「著作者の意を害しない」場合を除くので、生前の同意は遺族の差止め（116 条）に約束より直接に効く、と読める（portfolio-50）。1.0〜1.3 に欠陥があったのではないので、errata にも SELF-AUDIT にも入れない。

**反例と形（portfolio-50）**: (1) 同意は約束と同じ文に *"and consents to …"* と足すのでなく、別の文にした。包括的な事前同意を無効とする法域で裁判所が同意だけを外すとき、§15.2 の切り分けが文の単位で効き、約束を巻き込まない。(2) 最初の案の *"of theirs"* は先行詞（*You or … any person*）の数が揺れるので、*"by You or by any such person"* にした。(3) *"those rights"* は §12.2 の約束の文の、Work についての人格権を受けるので、同意は Work についての人格権に限られ、§12.3 の限定と同じ範囲になる。

**⚠ 逆側**: (1) **同意が約束より強く効くという読みは我々のもの**である。Sado 氏の通は、日本の実務は自然人が著者のとき包括的な放棄でなく不行使の約束に頼る、と書くだけで、同意が効く理由は書いていない（portfolio-2f）。文献にも法律家にも当てていない —— 法律家への問いに足すよう portfolio-30 に頼んだ。(2) 日本 113 条 11 項（名誉声望を害する利用）と、予見できない程度の改変には、包括的な事前同意が及ばないという読みがある（50）。だから同意は約束を置き換えず並べる。(3) +29 語（§12.3・§2.4 を含む）で、GPL-3.0 より題名から短い余裕は 69 語から 40 語になる。(4) 同意は §2.4 の *"every other grant, permission, and covenant"* に名指されていない。*permission* と読めば独立は §2.4 でも支えられるが、名指していないので争う余地はある（50）。

**反例で足した 2 か所（portfolio-9b・portfolio-30）**: (a) §12.4・§12.5 は約束と同意の両方を名指したのに §12.3 だけが約束を限っていたので、対比で「同意は他の著作物に及ぶ」と読む余地が立つ（語を 1 か所だけそろえると対比が立つ型）。§12.3 を *"The covenant and the consent in Section 12.2 are limited to the Work. They extend …"*（+3）。(b) §2.4 は独立を *"every other grant, permission, and covenant"* の 3 つの種類で述べ、同意の名が無い。*also* が約束の文に結ぶので、同意が約束に従属し、約束が契約として効かない法域で同意も落ちる —— T67 の目的とちょうど逆の読みになる（30）。§2.4 を *"every other grant, permission, consent, and covenant"*（+1）。逆側: 同意は *permission* の一種と読むのが普通で、§1.6・§4.6 は *permission* を総称に使う。ただし区別を立てた文の中に名前が無いことは響く（T51 と同じ理屈）。

**測定（portfolio-9b・最初の形）**: `--compare` は条 +0・語 +25・重複 69 → 69・族 51・先行詞の無い指示語 0 / 0・許可の声が増えた条 0。`--guard` は 468u 17 件の欠け 0・468r 0 / 0。§12.2 の *any such person* は直前の文の *any person who receives the Work from You* を指す。外した語に依拠する外向きの記録は `against.md` #118（§12.5 の旧文 *"survives it"*）で、1.4 を出す版にする日に書き換える。

**§15.1 への追記（2026-11-16）**: §12.3 の *"they are given in respect of a work that the Dedicator has chosen to place in the commons for the purpose stated in Section 6"* は、1 冊目の試作で「目的の文が約束の有効性を助けるか狭めるかは法律家への問い 3 (c) の領分」として残した句である（`ACD-1.4-CLARITY-TRIAL.md` の §12.3 の行）。T67 で §12.3 の主語を *"The covenant and the consent"* にしたので、この目的の句は同意にも掛かる。包括的な事前の同意が目的に照らして狭く読まれうるなら、学ばれることと関係の無い通常の改変が同意の外と読まれうる —— 狭める側の重みが T67 で増した（理由の文が範囲を狭める E78・E85 と同じ型の、法律家の判断に委ねる側の残り）。「目的で狭く読まれうる」は我々の読みで、どの法域でも確かめていない。本文は変えず、portfolio-30 が `QUESTIONS-FOR-COUNSEL.md` 問 3 (c) の 2 つ目の点として訊いた（この句は同意を学ばれることに資する行為に限るか、限るなら句を外すと約束の有効性を損なうか）。

### 15.2 §2.9 と OWFa の「約束を倒産法の目的では許諾として扱う」（変えない・2026-11-15）

**材料（portfolio-2f・`review-readings-2.md` §1.227）**: Rosen 氏は Moglen 氏の「ライセンスは倒産で終わりうる」に、OWFa の 3 つの条で答えた（`license-discuss` 2013-08-18）。3.1.3 *"Notwithstanding the personal nature of my promise, this promise is intended to be binding on any future owner, assignee or exclusive licensee who has been given the right to enforce any Granted Claims against third parties."*、3.1.4 *"Solely for purposes of Section 365(n) of Title 11, United States Bankruptcy Code and any equivalent law in any foreign jurisdiction, this promise will be treated as if it were a license and you may elect to retain your rights under this promise if I … reject this non-assert."*、6（義務を迂回する行為を取らず、第三者にも手伝わない）。ACD の §2.8・§2.9・§5.1 とほぼ同じ並びで、法律家が起草した先例である（承認の先例ではない）。候補は、§2.9 に「この Dedication の約束（§5・§8.6・§12.2）は、許諾者の倒産で許諾を受けた者を守る法の目的では許諾として扱う」型の 1 文を足すこと（20〜25 語）。

**変えない理由**: (a) §2.9 は、倒産で何も *"conditioned on, suspended by, or revived by"* されないと述べるだけで、法的な結果を言い切らない形に直してある（errata E5・E30）。「許諾として扱う」は、本文が法の分類を自分で決める文で、E23・E79 と同じ型（本文が制定法より強い主張をする）になる。OWFa 3.1.4 は 365(n) を名指して限っているが、ACD は特定の法を名指さない形を通しており、名指さずに「許諾として扱う」と書くと、どの法域のどの法に当たるかが読めなくなる。(b) 効くかどうかは法廷地の倒産法が決める —— 法律家への問い 8 の芯（*Jaffé v. Samsung* のように 365(n) の保護が衡量で決まる）そのもので、文を足しても答えは変わらない。(c) 語数（GPL-3.0 との余裕は 40 語）。

**⚠ 逆側**: (1) 法律家が起草した OWFa が、まさにこの場面に「許諾として扱う」を置いている。ACD の約束（§5・§8.6・§12.2）は、米国では不行使の約束が許諾と同じに扱われるのが普通だが、他の法域で約束が 365(n) 相当の保護から外れる読みは残る。(2) 3.1.3 の「約束は将来の権利者を縛る」は §2.8（*to that extent*・T59）と §5.3 が持ち、6 の「迂回しない」は §5.1・§5.2(d) の *"not to authorise or assist any other person"* が持つ —— 並びは揃っている。(3) 譲渡の後も非独占の許諾が残ることを決める側が論じた通は無いが、OWFa 3.1.3 は起草の先例として T59 の記録に足せる。OWFa 3.1.4 の形が §2.9 を助けるか、本文が法の分類を決める形として害になるかは、法律家への問い 8 に足した（portfolio-30）。

### 15.3 T68: §5.2(a) 第 2 肢の回避規制の射程（試作・退けた・2026-11-15）

**見つけた経緯（portfolio-50）**: T64 の逆側 (4)（§14.36・Dedicator 自身のサーバの防御の回避にも回避法を使えない）は、逆側として残ったまま語を検討していなかった。芯は §5.2(a) 第 2 肢の *"any law concerning the circumvention of such measures"* の射程で、配布サーバの関門（proof-of-work、レート制限、認証）を破られたときに援用する法は、著作権の回避規制（DMCA §1201、InfoSoc 指令 6 条）だけでなく、不正アクセスの法（CFAA、日本の不正アクセス禁止法）も「関門の回避に関する法」と読める。そう読むと、自分のサーバを攻撃された Dedicator が不正アクセスの法まで放棄したことになり、自前で配る採用者（B2 で最も欲しい層）には重い。1.0 から同じ語。

**試した形と、退けた理由**:

| 形 | 語数 | 退けた理由 |
| :-- | --: | :-- |
| 法の目的で切る: *"… any law that protects such measures as a means of protecting rights in the Work"*（1c の初案）| +7 | (1) 営業上の利益を守る目的で DRM の回避を禁じる法（日本の不正競争防止法 2 条 1 項 17・18 号）が外に出て Dedicator の手に戻り、旧文が放棄していたものを狭める —— 差を読む人には「放棄を狭めた」と読まれる。(2) §3 の放棄が効いて権利が無い法域では「守る権利」が無いので第 2 肢が空になる（portfolio-50）。(3) 不正競争防止法は回避の道具を作って配る受領者に向く法で、外に出ると Dedicator がそれを You に向けられるようになる（portfolio-30）|
| 許された行為による回避に限る（GPL-3.0 §3 型）| +10 前後 | 配布サーバの関門を越えて写しを取ることも「複製＝許された行為」に入るので、サーバの防御の回避に対して何も残らない読みになり、問題を閉じない |
| 旧文を保ち、不正アクセスの法を除く: *"…, other than a law against unauthorised access to a computer system"*（50 の代案）| +9 | 除外で残した不正アクセスの法を、PoW やレート制限を越えて写しを取ったクローラに向けると、§6 の「機械が学べる」に対する脅しとして働く。それを §5.1 第 2 文（*"any claim … for a use of the Work that this Dedication permits"*）が塞ぐかは、サーバに接近することが Work の *use* に当たるかに依り、語から決まらない（50）|

**結論（変えない）**: どの形でも、境界（Dedicator が自分のシステムを守る法と、Work の利用の自由を守るために放棄する法の線）は、§14.36 の逆側 (4) と同じ所に残る。1.3 の語は不正アクセスの法まで放棄すると読める余地を持つが、狭めるどの形も別の穴を開けるので、語を変えずに法律家への問いに回した（portfolio-30 に依頼）。30 の反例 (iv): T64 と組むと、Dedicator はボット対策を置き、それを破るクローラを不正アクセスの法で訴えうる。§6 の目的は写しが別の手段で手に入ることでしか保たれず、本文はそれを求めない —— T64 の撤退線（`REVISION-PROTOCOL.md` §3.8 の *"where a copy … remains obtainable"*）と同じ点で、これも同じ問いに含めた。

**⚠ 逆側**: 語を変えないので、採用者が「自分のサーバを攻撃されても不正アクセスの法を使えない」と読む余地は残る。答えは本文ではなく `ADOPTING.md`（50 が持つ）に「§5.2(a) が放棄するのは回避の法を You に向けることで、計算機への不正なアクセスを止める法がそれに含まれるかは法律家への問いとして開いている」と書く形になる。

### 15.4 T69: §2.6 の識別を §16.2 の仕組みで果たせると書く（+9 語・採った・2026-11-15）

**見つけた経緯（portfolio-30 の候補）**: §2.6 は、寄与から外れる素材を Work に入れる Dedicator が *"identify it in a form that accompanies the Work, so that a person or an automated system reading the Work can determine what this Dedication does not cover"* と約束するが、どう識別するかを言わない。審査の側の語では、Piana 氏が *"In source code there are standards like SPDX and REUSE and that one is the (machine readable) way"* と書いた（2025-07-18・`review-readings.md` §1.203）。

**Before**: *"… will identify it in a form that accompanies the Work, so that …"* **After**: *"… will identify it in a form that accompanies the Work, as a notice may identify material under Section 16.2, so that …"*（最初に採った *"as a notice may under Section 16.2"* は動詞を省き、*identify* と *accompany* のどちらを補うかで割れ、*may* が許可の声に数えられたので、同じ日に *identify material* を書いた・portfolio-9b の測定・+2 語）

**最初の案と反例（portfolio-50）**: 最初は *"such as an SPDX expression or a REUSE file"*（+9 語・*license* の綴りは 468o とぶつかるので *SPDX license expression* は避けた）とした。50 の反例: (1) SPDX のライセンス式（*"LicenseRef-ACD-1.4 AND MIT"*）はパッケージの単位では「どのライセンスが混ざっているか」しか言わず、どのファイルが MIT かを言わない。例に挙げると、式を 1 つ書けば約束を果たしたと読ませる。(2) SPDX / REUSE を名指すと、*ejusdem generis* でソースのメタデータの類に読まれ、データセットのカードの YAML の license 欄が外されたと読める。(3) 実務家への問い 5 は「どの標準か」を尋ねていて、名指す形はその答えの前に標準を選ぶ。§16.2 は、注記がどの素材に掛かるかを、語・ファイル内の注記の位置・他の素材を指すファイル名・範囲を区切る印で決める語と、狭い注記が他の条件へ割り当てた素材にはこの Dedication を適用しないという規則を既に持つ。§2.6 の識別はその仕組みで果たせるので、それを指す。

**⚠ 逆側**: §16.2 を指す形は抽象的で、実務の読み手には SPDX / REUSE の名の方が速く伝わる —— 標準の名は `ADOPTING.md` に例として置く（50 に依頼）。+9 語で、GPL-3.0 との余裕は 40 語から 31 語になる。

**審査記録（portfolio-2f・引用行を除く本文への正規表現の当て・弱い不在）**: 承認済みの CAL-1.0 は適用の文で *"SPDX-License-Identifier: CAL-1.0"* の札を名指している（委員会報告 2020-02-09・`rounds/2019-04-license-review-cal-approval-observed-52of61.txt`）。ACD の §16.2 も同じ札を名指すので、§16.2 を指す形はそれを含む。告知の形を本文で固定したライセンスは機械可読の慣行と衝突しうる、という指摘があり（Crane 氏 2021-09・AFL と REUSE / SPDX）、§2.6 が形を §16.2 の仕組みへ開くのはその衝突を避ける向きである。「標準を本文に書くと古びる」型の正面の異議は見つからなかった。審査者は SPDX の構文の正確さまで見る（Fontana 氏 2020-02-07）—— 本文に式の例を書かなかったことは、その費用も避ける。

### 15.5 T70: §5.3 末文の足場の列挙（試作・採ってから同日に戻した・退けた・2026-11-15）

**見つけた経緯**: portfolio-30 が T66（§14.44・errata E83）の逆側に記録していた。T66 で §5.3 の主語に §8.6（特許の約束）を入れた後も、末文 *"Sections 3 and 4 operate in their favour independently of this Section"* は著作権の足場（§3 の放棄・§4 の許諾）しか名指さない。特許の約束の受益者について、§8.1・§8.4 の許諾が §5.3 と独立に働くことを言わないので、「§8.6 には §8.1・§8.4 が独立に働かない」と裏読みされうる —— T67 の §12.3・§2.4 と同じ「そろえ残し」の型（主語を「A」から「A and B」へ増やしたとき、A だけを名指す文が残る）。

**Before**: *"Sections 3 and 4 operate in their favour independently of this Section."* **After**: *"Every provision of this Dedication other than those covenants operates in their favour independently of this Section."*（同日に再改: 最初に採った *"Every other provision …"* は、*other* が「§5.3 以外」なので §5.3 自身の主語の約束まで含み、第 1 文の限定 *"to the extent a jurisdiction gives effect to such reliance"* を空にする読みが立った・portfolio-50。最初の案 *"Sections 3, 4, 8.1, and 8.4 operate …"* は、受け手のために独立に働く他の足場 —— §6.1・§7.2 の許可、§12.1 の放棄、§12.2 の同意、§9 —— が列挙に無いことを新しい対比にした・portfolio-50。50 の一般形 *"Sections 3 and 4, and every other grant, permission, waiver, and consent in this Dedication, operate …"* は +11 語で、*waiver* が §3 の *surrender* を呼び替えると読まれうるので、列挙をやめた短い形にした。一般形は §16 のような文書の規律まで「受け手のために働く」と述べる形になるが、害は無いと読む）

**⚠ 逆側**: §8.6 第 2 文（*"does not wait for either licence to be held ineffective"*）と §2.4（独立の一般則）が許諾と約束の独立を既に述べているので、欠陥は弱い。30 は最初「逆側の記録で足りる」と読み、私も T66 では変えなかった。採ったのは、9b の「そろえ残し」の検出が T66 の時点では無く、同じ型を T67 で 2 か所直した後で、残す理由が語数だけになったからである。+5 語で、GPL-3.0 との余裕は 31 語から 26 語になる（`split()` で数えた —— 最初は +3 と書き、Check 468n が箇条の申告と本文の差の食い違いで捕まえた）。

**一般形（T70 から）**: 列挙を一般形（*every other provision*）に替えるとき、*other* が外すのは自分の条だけで、自分の条が主語にしているものは外さない。同じ条の中で、主語にしたものについて限定を置き（第 1 文の *"to the extent a jurisdiction gives effect to such reliance"*）、続けて「それ以外のすべて」が独立に働くと言うなら、主語にしたものを語で外す。T67・T70 で 3 回続いた「そろえ残し」を、一般形で避けようとして起きた —— 列挙を増やせば名指さないものとの対比が立ち、一般形にすれば自分を含める。どちらを選んでも、主語と目的語の重なりを読む。

**戻した（2026-11-15・同日）**: 採った形 *"Every provision of this Dedication other than those covenants operates …"* に portfolio-30 が反例を当てた: (1) §13（保証の否認）と §14（責任の制限）は受領者のために働く条ではなく、審査者が §14 を指して「すべての条が受領者のために働く」を偽と言える。(2) §16.4 も受領者のための条ではない。(3) §5.3 自身も「その約束以外」に入り、自己言及になる。30 の代案（*"The surrender in Section 3, and every grant, permission, and consent …"*）は §12.1 の放棄を落とし、列挙の型の問題を繰り返す。文を外す形も試したが、1.1 はこの文を「第 1 文の限定（*"to the extent a jurisdiction gives effect to such reliance"*）が穴に読まれないよう、逃げ道を同じ条に置く」ために足しており（`ACD-1.1-CHANGELIST.md`）、`against.md` #327 もこの文を有利な材料として引く —— 外せばその判断を覆し、差を読む人に「独立をやめた」と読ませる。**3 つの形がどれも別の欠陥を生んだので、末文は 1.3 の語に戻し、T70 は退けた**。§8.6 の約束について §8.1・§8.4 が独立に働くことは、§8.6 第 2 文（*"does not wait for either licence to be held ineffective"*）と §2.4 が述べる。T66 の逆側（§5.3 末文は §8 を名指さない）はそのまま残る。**一般形の教訓は上のとおりで、もう 1 つ足す: 弱い対比を閉じるために語を変えると、より強い欠陥を作ることがある。30 は最初に「逆側の記録で足りる」と読んでいた —— その読みが正しかった。**


### 15.6 法の状態や限界を述べ直す条を「要らない／害」の二択に当てた（変えない・2026-11-15）

**レンズ（portfolio-2f・`review-readings-2.md` §1.241）**: Berkus 氏は OSET の政府への例外の条について *"If governments already have immunity, the clause is not needed; if they don't, then the clause is bad. Either way, it is not something OSI should be endorsing."* と書いた（`license-review` 2015-09-17）。法の状態を述べ直す条を「既にそうなら要らない／そうでないなら害」で退ける型である。Berkus 氏が論じたのは特権を与える条で、ACD の条ではない —— **ここでは型を借りた**。法の状態や限界を述べ直す ACD の条を全部当て、「法域で違うから要る」「要らない（語数の費用）」「害（特権・判定を課す）」に分けた。

| 条 | 分け方 | 理由 |
| :-- | :-- | :-- |
| §2.7 第 1 文（*"reaches only rights the Dedicator holds"*）| 要る | 他人の権利に及ばないことは法の通りだが、§6.2（*"bounded by Section 2.7"*）・§11.4 などが参照する範囲の定めとして働く。外すと参照先を失う |
| §9.2 第 2 文（権利が無ければ何も足さず何も取らない）| 要る | 機械生成物について権利が在ると主張していない（*copyfraud* と読まれない）ことを述べる。権利が在るかは法域で違う |
| §9.4（出所の事実は否認しない）| 要る | 1 冊目の試作の理由の文のレンズ（`ACD-1.4-CLARITY-TRIAL.md` の表）で検討して残した。§9 を人の指示の事実まで否認したと読ませないため |
| §10.4 の *because*（違反しうるものが無いから終了規定が無い）| 要る | 1 冊目の試作 §4.4 で検討して採らなかった。外すと「違反しうるものが見つかれば終了できる」の反対解釈が具体的に立つ |
| §11.2（名を指して述べることは影響を受けない）| 要る | 商標の法の名指しの使用を述べ直すだけに見えるが、Dedicator の氏名についての許可でもあり、氏名の権利は法域で違う |
| §11.3 第 1 文（*"This Dedication does not make a false statement true."*）| 要る | 法の通りの言明に見えるが、§5.1 と §5.2(d) の除外 *"for a false statement or representation (Section 11.3)"* の *false statement* の語は §11.3 ではこの文にしか無い。外すと参照先が語を失う |
| §13.3（保守・更新の義務を負わない）| 要る | 黙示の義務の有無は法域で違う |

**結果**: 削る候補は 0。「要らない」に分けられる条は無く、どの条も参照先か、法域で違う点か、反対解釈を閉じる働きを持っていた。「害」に分けられる条（特権を与え、判定を課す）も無い。

**⚠ 逆側**: 型を借りただけで、審査者がこれらの条を論じた記録は無い。§11.3 第 1 文は、§5.1 の語の参照先という理由で残したので、§5.1 の除外の語を *"a representation Section 11.3 describes"* に替えれば外せる —— ただしその形は T21（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.7）で *false statement* へ広げた経緯を戻すことになる。

### 15.7 T71: §8.3 の理由の文と規則を外す（−40 語・採った・2026-11-15）

**見つけた経緯（portfolio-30 の再提起・errata E85）**: §8.3 の第 3 文 *"A dedication that gives away copyright while withholding patent rights leaves the recipient exposed, because software cannot be practised without practising whatever patent claims it embodies."* は *software* を名指す。§1.3 の Work はデータ・文書・視聴覚資料を含むので、目的で読む人は第 4 文 *"Any reading of this Dedication that would produce that result is to be rejected."* をソフトウェアの Work に限りうる —— E78（§8.4 の理由の文が許諾を狭く読ませた・T54）と同じ型。1 冊目の試作の CE8 が既にこの残余を記録していた（`ACD-1.4-CLARITY-TRIAL.md`）。そこで試した「結果を書き込む形」（*"Any reading … that gives away a Covered Right while withholding a patent right is to be rejected"*）は、§8.4 が意図して許諾しない請求項まで退けるべき読みにして不成立だった。

**Before**: *"Sections 8.1 and 8.4 reach a patent claim only as to the acts they describe. Nothing in this Dedication reserves, preserves, or leaves unaffected any patent claim they reach. A dedication that gives away copyright … whatever patent claims it embodies. Any reading of this Dedication that would produce that result is to be rejected."* **After**: 最初の 2 文だけ。

**最初の形と反例**: 最初は第 2 文に *"and any reading to the contrary is to be rejected"* を結ぶ形（−30 語）とし、規則の対象を *"any patent claim they reach"* に結んで CE8 の失敗を避けた。portfolio-50 の反例: その規則は作用の文に「反対の読みは退ける」を付けるだけの同語反復で、何も足さない。曖昧なときの向き（受け手が無防備になる読みを退ける）は §15.1（*"the reading that grants more to You prevails"*）が持つ。portfolio-30 は *"the contrary"* の先は 1 つに決まると確かめた。

**⚠ 逆側**: (1) 旧い第 4 文は、届く範囲（*reach*）を狭く読む読みも「受け手を晒す結果」として退けていた。外した後、範囲の争いは §15.1 だけに頼り、§15.1 は *in respect of the Work* に限られるので、§8.4 のモデルと出力の請求項が「Work について」かを争う余地がある（30）—— ただし旧文の規則も *software* の理由に結んでいて、モデルと出力を名指していなかった（50）。(2) §8 全体の目的（著作権を渡して特許を留保すると受け手が晒される）を審査者に一目で示す説明力は、本文の作用の条からは消える。前文（*"… both leave the recipient of software exposed"*）に残る（30）。(3) 外向きの文書 5 つが 1.0 の文として引くので、切り替えの日の表に行を置いた。(4) −40 語で、GPL-3.0 より題名から短い余裕は 31 語から 71 語になる。B3 への作用は結果で、理由ではない。

### 15.8 T72: 前文の *"silent or hostile"* を *"leave a gap"* へ（−1 語・採った・2026-11-15）

**見つけた経緯（portfolio-2f・`review-readings-2.md` §1.251）**: Chestek 氏は *"It is a misperception to think that there is any "non-binding" part of a legal document."*（2020-12-28）と書いた —— 前文が自分を *"informative; not part of the operative terms"* と述べても、意図の判断に読まれる。Atkinson 氏 2020 は GPL の前文を「中立な調子でも足りた」と評した。ACD の前文の *"the three places where the existing tools are silent or hostile"* の *hostile* は、既存のライセンスへの強い評価語で、前文の第 1 段落が述べる 3 つ（未決・沈黙・特許の留保か沈黙）のどれも「敵対」ではない。

**Before**: *"… it speaks in the three places where the existing tools are silent or hostile: machine learning, patents, and machine authorship."* **After**: *"… where the existing tools leave a gap: machine learning, patents, and machine authorship."*

**⚠ 逆側**: (1) *gap* は B10 で我々が論じ、審査者が問う当の語で、前文がそれを当然のように述べると B10 の答えを先取りしていると読まれうる。中立の語の候補（*"where the existing tools say little"*）もあるが、特許を明示に留保する道具（CC0）を「言わない」とは言えないので、3 つを覆う語として *gap* を採った。(2) 前文の有利な面（*"written for works that are meant to be learned from"* が曖昧な条を受け手の側に読ませる）は変えない。(3) 2f の種の (2)（「本文を変えない」判断を、その読みを持つ本文の語と並べる）は、§14.x と §15.x の「変えない」節が既にその形（変えない理由に本文の語を引く）を持つので、別の表は作らない。

### 15.9 T73: 前文の三つの場所を「その前提が崩れる所」と呼ぶ（−3 語・採った・2026-11-16）

**見つけた経緯（portfolio-30 の T72 への反例）**: T72 で採った *"where the existing tools leave a gap"* は、前文の第 1 段落が道具を限って述べた正確な文を、限定の無い「既存の道具」一般の断定に広げていた。第 1 段落は、機械が作った素材の権利は未決（道具の話ではない）、*"Permissive licences are silent on whether a work may be used to train a model"*、*"dedications to the public domain either withhold patent rights expressly or say nothing about them at all"* と、場所ごとに道具を限っている。特許の許諾を持つ Apache-2.0・Blue Oak・UPL も既存の道具なので、審査者が B10（H1-g）を問うとき、前文が「特許について既存の道具に穴がある」と一般に言い切る形になる。

**Before**: *"… it speaks in the three places where the existing tools leave a gap: machine learning, patents, and machine authorship."* **After**: *"… where that assumption fails: machine learning, patents, and machine authorship."*

**30 の案から変えた点**: 30 は *"where those tools leave a gap"*（−1 語）を挙げ、逆側として *those* が第 1 段落の *"The legal tools in common use"*（一般）まで広がれば効かないこと、機械による著作の場所では第 1 段落が道具を名指していないことを書いた。*"that assumption"* は第 1 段落の *"That assumption now fails in three places at once"* を受けるので、3 つの場所がそのまま一致し、道具の良し悪しを何も言わない。

**⚠ 逆側**: (1) 前文は非作用で、効くのは審査者が前文を意図の証拠として読むとき（Chestek 氏 2020・`review-readings-2.md` §1.251）だけ。(2) 2 回続けて同じ文を直した（T72・T73）—— 審査中の改訂を嫌う審査者（Berkus 氏 2018）の目には、確定の前の草案の中のことなので当たらないが、投稿の差には最後の形だけが出る。(3) 前文が「既存では足りない」と言わなくなったので、B10 の主張は入口と提出の材料が受け持つ。

### 15.10 定義語を承認済みの語と照らした —— 独特に読まれる語はどれか（変えない・2026-11-16）

**訂正の記録**: Dedicator の行は 2 度直した。初めは「Licensor にすると §3 の放棄と食い違う」（ACD も §4・§8 で許諾するので不正確）、次は「許諾は放棄の予備で CC0 と同じ構造」（§4.4 の *"not as a fallback"* に反する・portfolio-50 の指摘）。いまの行は §4.4 の語に当てて書いた。

**種（portfolio-50・模擬委員会の Fontana 氏の節）**: Fontana 氏は Open Innovation License を *"a highly and uninterestingly permissive FOSS license and it just happens to be written in a highly odd and idiosyncratic style"* と評した（2020-12-28）。定義はあっても語が独特に読まれると、理解の費用（B13）が増える。30 の頻度表の読みでは、25 年出続けた問い（B10・B1・B2・B13・B3）のうち、本文の語で答えられるのは B13 だけである。ACD の定義語 11 個を、承認済みのライセンスと法令の語に照らした（使われる回数は 2026-11-16 の草案で数えた）。

| 定義語 | 回数 | 最も近い承認済み・法令の語 | 読み |
| :-- | --: | :-- | :-- |
| Work | 80 | Apache-2.0 の *Work* | 同じ語 |
| You | 48 | Apache-2.0 の *You* | 同じ語 |
| Contribution | 6 | Apache-2.0 の *Contribution* | 同じ語（定義は ACD の場に合わせてある）|
| Moral Rights | 9 | CC0 の *moral rights*・ベルヌ条約 6 条の 2 | 同じ語 |
| the Steward | 4 | EPL の *Agreement Steward*・MPL の *license steward* | 同じ語（`review-readings-2.md` §1.226 の先例）|
| Reservation | 7 | EU 指令 2019/790 の 4 条 3 項の *reserved … in an appropriate manner* | 法令の語に結ぶ |
| Dedicator | 77 | CC0 の *Affirmer*・Apache-2.0 の *Licensor* | **ACD に独特**。Dedicator は権利を放棄し（§3）、それとは独立に許諾もし（§4・§4.4 *"granted independently of Section 3, and not as a fallback for it"*）、特許も許諾する（§8）—— *Licensor* は 2 つ目の役だけを名指す。CC0 の *Affirmer* も放棄を名に持つ語だが、CC0 の許諾は放棄の予備で、ACD の許諾は予備ではない（この違いは ACD の差の要の 1 つ） |
| Covered Rights | 9 | CC0 の *Copyright and Related Rights*・MPL の *Covered Software* | ACD に独特だが、*Covered* は MPL と同じ型 |
| Computational Use | 5 | 承認済みに無い | **前文の 3 つの場所（機械学習）に対応する新しい語** |
| Machine-Generated Material | 4 | 承認済みに無い | **前文の 3 つの場所（機械による著作）に対応する新しい語** |
| Dedication | — | CC0 の *dedication*（本文中の語）| ほぼ同じ語 |

**結果（変えない）**: 11 個のうち 6 個は承認済みのライセンスか法令と同じ語、1 個（*Dedication*）はほぼ同じ語で、*Covered Rights* は MPL と同じ型である。独特なのは *Dedicator* と、前文が名指す場所に対応する 2 つの新しい語（*Computational Use*・*Machine-Generated Material*）—— 後の 2 つは、ACD が既存に無いと主張する効果（B10）そのものを名指す語で、承認済みの語に置き換えると、何が新しいかを本文が言えなくなる。*Dedicator* は 77 回使われ、置き換えの候補（*Licensor*）は、放棄と独立の許諾を併せ持つ役（§3・§4.4・§8）のうち許諾だけを名指す。審査者の理解の費用は、本文ではなく入口の 1 行（定義語と承認済みの語の対応）で下げる —— portfolio-50 に `REVIEWERS.md` への 1 行を依頼した。

**⚠ 逆側**: (1) Fontana 氏の評は文体全体（*style*）についてで、定義語だけではない。ACD の長さと文の形（B3）は、この表では測っていない。(2) 「同じ語」と書いた語も、定義の中身は承認済みのものと違う（例えば *Contribution* は §1.9 で場を名指す）—— 同じ語が別の意味で使われると、かえって誤読を招きうる。(3) 置き換えないので、1.3 との差（redline）には何も出ない。

### 15.11 同じ問題を扱う部分どうしの語の揺れを掃いた —— Fontana 氏 2014 の *subtle contradictions*（変えない・2026-11-16）

**種（portfolio-30・頻度表の読み）**: 25 年出続けた問いのうち本文の語で答えられるのは B13 で、その試作の種として、Fontana 氏 2014 が挙げた「同じ問題を扱う部分どうしの subtle contradictions」がある（模擬委員会 §16.3）。1.4 草案の第 1 条から *END OF TERMS* までを 2 つの方法で機械的に掃いた: (a) 3 項以上の列挙で、項の 3 つ以上が重なり、残りが違う組、(b) 同じ相手を指す句（*person* / *person or entity*、*Covered Rights* と *patent claims* の組）の数え上げ。

| 見つけた揺れ | 読み | 扱い |
| :-- | :-- | :-- |
| §1.10 の *Reservation* の列挙 *"any act, notice, marking, metadata, protocol element, header, machine-readable signal, contractual term, or other measure"* と、§6.2 の *"no notice, marking, metadata, protocol element, header, robots directive, or other signal associated with the Work is to be read as a Reservation"* —— §6.2 は *machine-readable signal* と *contractual term* を持たず、*robots directive* を足す（1.0 から）| 2 つの経路の分担で、矛盾ではない。§6.2 は「信号を留保と読まない」経路で、Work に付いた信号だけを対象にする（*robots directive* は *machine-readable signal* の一種で、*other signal* が残りを拾う）。契約の条項は信号ではなく、Dedicator が結んだものは §6.3 が撤回し、他の権利者が自分の権利で結んだものは §6.3 第 2 文が力の外とする。権利者でない人の契約（ホスティングの利用規約など）は、§1.10 が Reservation を *"by which a rightsholder purports to reserve"* に限るので、そもそも Reservation に当たらない。§6.2 に *contractual term* を足すと、Dedicator が結んでいない契約の条項まで「留保と読まない」と宣言することになり、§2.7 の境界（他人の権利と約束に触れない）を越える。**より強い理由（portfolio-50 の反例の結果）**: Dedicator 自身の利用規約の TDM 禁止は、3 層で既に閉じている —— §6.2 第 1 文 *"The Dedicator makes no Reservation in respect of the Work and expressly declines to make one"* は形を問わず契約の条項も含み（第 2 文の列挙は信号の読み方の補いで、第 1 文を狭めない）、§6.3 の撤回は自分の契約上の権利では *"to the fullest extent the Dedicator is able"* で止まらず、§5.2(b) は *terms of service* による義務を課さないと約す（§5.3 で受領者が頼れる）。足すと第 1 文と重なる（B3） | 変えない |
| *person or entity*（9 回）と *person* だけ（11 回以上）| 定義が *person or entity* と書き、拘束する条が *person* と書くと、明示したものだけを含む読みで会社が外れる（§5.1・§8.6 の *"any other person"*、§6.3 の *"by another person"* など）| E58 で閉じた: §15.5 *"\"person\" includes an entity"* |
| §1.7 と §6.4 の *"model, parameter set, weight, embedding, or output resulting"* | 同じ列挙（§1.7 は *any* を前に置くだけ）| 揺れなし |

**結果（変えない）**: 機械の掃引で見つかった揺れは 2 つで、1 つは経路の分担として説明でき、1 つは既に閉じていた。

**⚠ 逆側**: (0) TDM と名乗らず「自動のアクセス・scraping を禁ずる」とだけ書いた server の利用規約は、「Work について」の義務か「server について」の条件かで §5.2(b) の当たり方が割れ、§5.2(a) は自分の server に技術的手段を置くことを許す。その規約で写しを得た人に契約や不正アクセスの法で向かう道が残りうるのは、`QUESTIONS-FOR-COUNSEL.md` が既に挙げた問い（*"any law concerning the circumvention"* が computer-misuse law まで放棄させるか）と同じ面で、本文を変える指摘にはしない（portfolio-50）。(1) この掃引は語の列挙と句の数え上げだけで、Fontana 氏が指した「同じ問題を扱う部分」—— 例えば §3・§4・§5 の 3 つの層が同じ行為を別の語で許すか —— の意味の矛盾は測っていない。それは 1 冊目からの試作（T1〜T73）と模擬委員会が条ごとに読んできた側に在る。(2) §6.2 と §1.10 の差は、審査者には説明なしでは揺れに見える。逐条の §6.2 の行に分担を書いた。

### 15.12 T74 —— §5.3 の承継の列挙を §2.8 へ寄せる（採った・−17 語・2026-11-16）

**種**: §15.11 の逆側 (1) で残した「意味の側」—— §3・§4・§5 の 3 層が同じことを別の語で言っていないかを読んだ。§5.3 は約束（§5.1・§5.2・§8.6）について *"bind the Dedicator's successors, assigns, heirs, and personal representatives, to the fullest extent the law permits the Dedicator to bind them"* と承継の列挙を持つ。1.4 の §2.8 は *"This Dedication, in respect of the Work, binds the Dedicator's successors, assigns, heirs, and personal representatives, and any person to whom a Covered Right or a patent claim in the Work is transferred, to the fullest extent the law permits"*（E49 で列挙から「This Dedication」へ）。

**欠陥（揺れ）**: §5.3 の列挙は §2.8 に何も足さず、§2.8 より短い（特許の譲受人を名指さない）うえに限度の語が違う。特定の規定が一般の規定に勝つ読みでは、特許を買った者は §8.6 の不行使の約束に縛られないと主張される余地がある。1.4 では §2.8 の末文 *"Neither Section 5.3 nor Section 12.4 narrows this Section."* がこれを止めていた（SELF-AUDIT 692 行の型）—— 揺れの元と、その防ぎの文が両方本文にあった。

Before（§5.3 第 1 文の前半）: The covenants in Sections 5.1, 5.2, and 8.6 bind the Dedicator's successors, assigns, heirs, and personal representatives, to the fullest extent the law permits the Dedicator to bind them, and may be relied upon …

After: The covenants in Sections 5.1, 5.2, and 8.6 bind those whom Section 2.8 binds, and may be relied upon …

§2.8 の末文: *"Neither Section 5.3 nor Section 12.4 narrows this Section."* → *"Section 12.4 does not narrow this Section."*

**採った理由**: 列挙が 1 つになり、§5 を読む人にも承継が §2.8 を名指して見える。§2.8 の防ぎの文は §12.4 の分だけ残る（§12.4 は死後に人格権を行使できる者を足すので、列挙を残す）。`measure_clause_overlap.py --compare` は §5.3 で *dedicator 2→0 / successors / assigns / heirs 1→0* を出し、外した語は §2.8 に全部残る。

**⚠ 逆側**: (1) §5.3 だけを読む人は、誰が拘束されるかを §2.8 で読む必要がある（参照 1 つ）。(2) §5.3 の *"the law permits the Dedicator to bind them"* は、約束が承継人を縛れるかが法域で違うことを、約束の側で言っていた。§2.8 の *"the law permits"* はそれを含むが、語は一般になる。SELF-AUDIT の E（*"to the fullest extent the law permits"* の法域差・起草では閉じられない）は T74 で閉じない。(3) 1.0〜1.3 の §5.3 を引く外向きの文は、1.4 の §5.3 の語と違う（`QUESTION-INDEX.md` の「§2.8 and §12.4 bind successors」は 1.4 でもそのまま正しい）。

**反例の担当へ（50・30）**: (a) §8.6 の約束を受けた後に特許を譲り受けた者が、§2.8 の *"any person to whom … a patent claim in the Work is transferred"* と §5.3 の *"those whom Section 2.8 binds"* の組で縛られない読みが残るか。(b) §4.6 の *"on the terms Section 5.3 states"* が、承継の列挙を失った §5.3 から何か落とすか。 **反例の結果**: §15.13 の冒頭（portfolio-50）—— (a) は当たった（範囲まで借りる読み）ので T75 で *names* にした。(b) は落ちるもの無し。続く §15.14（portfolio-30）で、T75 が限度を落としたことが当たり、T76 で限度を揃えた。

### 15.13 T75 —— T74 の §5.3 を「人だけを借りる」語へ、§2.8 の特許の譲受人の語と §12.4 を揃える（採った・−1 語・2026-11-16）

**反例（portfolio-50・§15.12 の (a)〜(c)）**: (a) 人の集合は変わらない（§2.8 も *assigns* を挙げる）。当たるのは範囲の側で、§2.8 は *"This Dedication, in respect of the Work, binds …"* なので、T74 の §5.3 *"bind those whom Section 2.8 binds"* は「§2.8 が縛る限りで（*in respect of the Work*）」と読む余地を持つ。§8.6 の約束は §8.4 の行為（Work の Computational Use から生じたモデル・重み・出力の製造・使用・販売）に及び、モデルについての行為が *in respect of the Work* かは争いうる。§15.1 の「広く読む」も T43 以後は *in respect of the Work* の下なので、受領者に有利に解く規則が無い —— **T74 は約束の範囲を狭める読みを新しく生んでいた**。(b) §4.6 の *"on the terms Section 5.3 states"* が借りるのは頼れる人と頼り方で、落ちるもの無し。(c) §2.8 の *"a patent claim in the Work"* は §8.1・§8.4 の請求項の語（行為で定める）と揃わない。

**直したもの**: §5.3 *"bind the persons Section 2.8 names"*（*names* は人だけを借り、範囲は約束の側に残る・0 語）。§2.8 *"a Covered Right, or a patent claim that Section 8 reaches, is transferred"*（+1・挿入句にして *Section 8 reaches* が *Covered Right* に掛かる読みを避けた。草案の他の場所の *"the patent claims Section 8 reaches"* と同じ語）。§12.4 *"bind the persons Section 2.8 names and any person entitled to exercise or enforce Moral Rights in the Work after the Dedicator's death"*（−2・承継人の列挙を §2.8 の 1 か所にした）。

**教訓**: 定義を他の条に預ける語は、何を預けるか（人か、範囲か）を動詞で決める —— *binds* は効果を指し、*names* は人を指す。T74 の検証で `--compare` は §5.3 の主体の語が消えたことを示したが、範囲の語が借りられることは示さなかった（語の増減では見えない種類）。

**⚠ 逆側**: (1) §12.4 の限度 *"to the fullest extent the law permits the Dedicator to bind them"* は残るので、§2.8 の末文 *"Section 12.4 does not narrow this Section."* は要る（468u の目印）。(2) §2.8 の挿入句は読みの負担を 1 つ足す。(3) *names* は §2.8 の文の中の *any person to whom … is transferred* も含むが、これは名指しではなく記述なので、*names* を「固有名で挙げる」と狭く読む余地は残る（*the persons Section 2.8 lists* でも同じ問いが立つ）。

### 15.14 T76 —— §5.3・§12.4 の限度を §2.8 と同じ語に、§2.8 の末文を外す（採った・−5 語・2026-11-16）

**反例（portfolio-30・T75 の merge の後に届いた）**: T75 の §5.3 *"bind the persons Section 2.8 names"* は人だけを借り、§2.8 の限度 *"to the fullest extent the law permits"* を借りない。3 つの約束が承継人・譲受人を限度なしに縛ると断定する形で、1.0 の §5.3 が持ち 1.1 で E17 が直した欠陥を戻していた。30 の案は (A) *"to the extent Section 2.8 binds them"*（+6）と (B) §5.3 から承継の句を外す（−6・30 の推し）。

**50 の応答**: (A) も (B) も §2.8 の範囲 *"in respect of the Work"* を借り、50 の (a)（§8.4 のモデルについての約束が譲受人を縛るか）を戻す。50 の案 (C) は、人を借り、限度を §2.8 と同じ語で自分で持ち、範囲を約束の側に置く。

**採った形**: (C) から *"as to everything those covenants reach"* を除いたもの —— 約束が人を縛るとき、縛る範囲は約束の文そのものが決めるので、範囲の句は何も足さない。さらに §12.4 の限度 *"the law permits the Dedicator to bind them"* も同じ語にした。人（§2.8 から借りる）と限度（同じ語）が 1 つになれば、どの条も §2.8 を狭められないので、§2.8 の末文 *"Section 12.4 does not narrow this Section."* の働きは構造で満たされ、外した。

| 条 | Before（T75） | After（T76） | 語 |
| :-- | :-- | :-- | --: |
| §5.3 | *"bind the persons Section 2.8 names, and may be relied upon"* | *"bind the persons Section 2.8 names, to the fullest extent the law permits, and may be relied upon"* | +7 |
| §12.4 | *"… after the Dedicator's death, to the fullest extent the law permits the Dedicator to bind them."* | *"… after the Dedicator's death, to the fullest extent the law permits."* | −5 |
| §2.8 | 末文 *"Section 12.4 does not narrow this Section."* | （外した）| −7 |

**機械層**: 468u の目印を §5.3 の *"bind the persons Section 2.8 names, to the fullest extent the law permits"* と §12.4 の *"after the Dedicator's death, to the fullest extent the law permits."* に替え、§2.8 の末文の目印を外した。mutation は §12.4 の限度を旧い語へ戻す形にした（手で RED を確かめた）。

**教訓**: T74〜T76 は 1 日に §5.3 の語を 3 度変えた。T74 は範囲を借り（50）、T75 は限度を落とした（30）—— どちらも、語の増減を見る `--compare` には出ない種類で、反例の担当の読みでしか出なかった。**定義を他の条に預ける改めは、merge の前に反例を 1 巡当てる**（T74・T75 は CI の緑で merge し、反例はその後に届いた）。

**⚠ 逆側**: (1) §12.4 の *"the Dedicator to bind them"* は、死後の行使者を Dedicator の約束で縛れるかを法が決める、と明示していた。新しい語も同じ意味だが、明示は減る。(2) §2.8 の末文を外すと、将来どこかの条が別の限度で承継を語れば、狭める読みが戻る —— 468u の目印が §5.3・§12.4 の語を守るが、新しい条は守らない。(3) SELF-AUDIT の E（*"to the fullest extent the law permits"* の法域差・起草では閉じられない）は T76 でも閉じない。

### 15.15 語の揺れの道具（scan_draft_terms.py）の最初の結果を読んだ（変えない・2026-11-16）

portfolio-9b が §15.11〜§15.14 の型を道具にした（`scan_draft_terms.py`・2026-11-16）。T76 の後の草案で、(a) ほぼ同じ列挙の違いは 0 件、(b) 同じ指し先の言い方の揺れは 2 件、(c) 他の条の定義を借りる語は 8 つの指し先に分かれた。

| 道具の出力 | 読み | 扱い |
| :-- | :-- | :-- |
| (b) *"a patent claim that Section 8 reaches"*（§2.8）/ *"the patent claims Section 8 reaches"*（§6.1・§11.4）| 冠詞と数と関係詞 *that* の有無だけで、指し先は同じ。§2.8 の *that* は T75 で挿入句にしたときに、*Covered Right* に *Section 8 reaches* が掛かる読みを避けるために置いた | 変えない |
| (b) *"Sections 8.1 and 8.4 reach"*（§8.3）/ *"the patent claims that Sections 8.1 and 8.4 reach"*（§8.6）| §8.3 の *reach* は文の動詞（*"Sections 8.1 and 8.4 reach a patent claim only as to …"*）で、指し先を名指す句ではない。§8 全体（§2.8・§6.1・§11.4 の *Section 8 reaches*）と §8.1・§8.4（§8.6）の違いは、§8 の請求項が §8.1 と §8.4 の 2 つから成るので、集合は同じ | 変えない |
| (c) §2.8 を借りる 2 か所（§5.3・§12.4）がどちらも「人」 | T74〜T76 の結果がそのまま出ている —— 範囲と限度は借りない | 揃っている |
| (c) §15.1 を借りる §2.4 *"Section 15.1 governs"* が「範囲」 | §2.4 の 3 つの足場の読みを §15.1 に委ねる文で、§15.1 は *in respect of the Work* の下にある。§2.4 の約束（Dedicator の側）に §15.1 が効くかは §17.4（50）が答えた | 変えない |

**⚠ 逆側**: 道具は語の形を拾うので、T74 の欠陥（*binds* が範囲まで借りる）のような**動詞が運ぶ借り方**を、(c) の「借りる種類」の推定が正しく分けられるかは、T74 の形に当てて確かめていない —— 9b へ、T74 の文（*"bind those whom Section 2.8 binds"*）を入れたとき (c) が「範囲」か「拘束の相手」を出すかを確かめてほしいと頼んだ。

### 15.16 §11.3 の理由の文を、T54・T71 の線で当て直した（変えない・2026-11-16）

**種**: 模擬委員会の Chestek 氏の行（§16.2）は「条の中の理由の文は残る」とした。§15.1 の追記で数えた作用の条の理由の文 11 のうち、§11.3 の *"because it was never the Dedicator's to permit"* は 1 冊目の試作 T3（`ACD-1.4-CLARITY-TRIAL.md` §8.1）で「§9.4 *"Section 11.3 explains why a false claim of authorship is not something this Dedication is able to permit"* が指すので残す」とした。その後 T54（§8.4）と T71（§8.3）は「理由の文が狭く読む分岐を作るなら外す」という線を採ったので、同じ線で当て直した。

**分岐が立つか**: T3 の記録が挙げた反対解釈は「Dedicator が許せる場合（自分の名の使用）には範囲内」である。§11.3 第 2 文は *"when that is not the case"* に限られるので、Dedicator が実際に作者である・支持している場合は初めから外である。Dedicator が他人に「支持を表明してよい」と許した場合は、その表明は許した範囲で真になり、*"when that is not the case"* に当たらない。Dedicator が許しうるのに虚偽のままの表明は、語の上で組み立てられない —— **反対解釈の分岐は、§11.3 自身の *when that is not the case* で閉じている**。T54・T71 の理由の文は、結論より狭い前提（§8.4 の「モデルは Work の主題ではない」、§8.3 の「ソフトウェアは請求項を実施せずに使えない」）を置いたので分岐を作った。§11.3 の理由は結論と同じ広さである。

**結果（変えない）**: T3 の判断（§9.4 が指す説明を残す）は、T71 の線で当て直しても変わらない。

**⚠ 逆側**: (1) *"never the Dedicator's to permit"* は法の命題として争いうる —— 自分の名の使用は Dedicator が許せる（パブリシティ）。ただし許せば表明は真になるので、作用は変わらない。命題の正しさを審査者が問う余地は残る（Chestek 氏の「説明は合意に入れない」の線・against #295）。(2) 理由の文を残すことは、B3 の長さで −8 語を見送ることである。

### 15.17 T77 —— §11.3 の理由の文を外す（採った・−18 語・2026-11-16・§15.16 の読みを覆した）

**反例の結果**（portfolio-30・§15.16 への反例・§11.3 と §9.4）: §15.16 は「Dedicator が許しうるのに虚偽のままの表明は組み立てられない」としたが、*authored* は許しても真にならない。英国 CDPA s.84（偽の帰属）の権利は表示された本人のもので、s.87(1) *"It is not an infringement of any of the rights conferred by this Chapter to do any act to which the person entitled to the right has consented."* により本人の同意で侵害でなくなる（`QUESTIONS-FOR-COUNSEL.md` 問 3 (e)）。理由の文 *"because it was never the Dedicator's to permit"* は法の命題として一部の場合に誤りで、*"when that is not the case"* は分岐を閉じない。**§15.16 の結論は誤りだった。**

**直したもの**: §11.3 の理由の文を外し（−8）、§9.4 を *"Section 11.3 governs a false claim of authorship"* に（−10）。30 の案 (B)（*"because permission does not make it true"*）は第 1 文 *"This Dedication does not make a false statement true"* と同じ命題の繰り返しになるので採らなかった。

**⚠ 逆側**: §9.4 は「なぜ」の説明を失う。§11.3 の作用は「Dedication の届く範囲の外」という Dedicator の選択として残り、Dedicator が別に同意を与えることは妨げない。**反例待ち**（50・30）。

### 15.18 T77 の目（理由が一部の場合に偽か）で、残りの理由の文を当てた（変えない・2026-11-16）

T77 は、理由の文が結論より狭いだけでなく、**一部の場合に法の命題として偽**になりうることを見つけた（作者の表示と英国 CDPA s.84・s.87(1)）。同じ目で、作用の条に残る理由・目的の文（§15.1 の追記で数えた 11 のうち、T77 で外した §11.3・§9.4 と、法律家に委ねた §12.3 を除くもの）を当てた。

| 条 | 理由・目的の文 | 偽になる場合があるか | 扱い |
| :-- | :-- | :-- | :-- |
| §10.4 | *"because it contains nothing that You could breach"* | §10.1 の *in respect of the Work* の下では真（§16.4 の本文の制限は Work についてではない）。反対解釈は第 1 文 *"No permission granted by this Dedication terminates for any reason"* が閉じる（1 冊目の F3・§4.4）| 変えない |
| §6.5 第 1 文 | *"Section 6 states expressly what Sections 3 to 5 and 8 would in any event permit"* | 特許の面は E36 で *and 8* を足して真にした。§6.3 の留保の撤回は許可ではないが、許諾がある以上、撤回は許しの範囲を変えない。§6.1 が独立の力を失う読みは CE13 で通過 | 変えない |
| §6.5 第 2 文 | *"silence on this subject has proved ambiguous in practice"* と *"a permission that an automated system cannot determine is … no permission at all"* | 前者は経験の言明で、法の命題ではない。後者は規範の言明で、§2.6・§8.4 から 3 か所で引かれる（1 冊目の CE11）| 変えない |
| §1.6（1.0 では §1.4） | *"so that no permission fails for want of a legal person to hold it"* | 目的の句で、命題を言わない | 変えない |
| §2.5 | *"intending that others rely on it … that reliance is the purpose of this Dedication and not merely a foreseeable consequence of it"* | Dedicator の意図の表明で、Dedicator 自身について真 | 変えない |

**結果**: T77 のほかに、法の命題として偽になる理由の文は見つからなかった。**⚠ 逆側**: 法の命題か否かの判断は我々の読みで、法律家の確認は無い（B1）。§6.5 の「沈黙が曖昧だった」は経験の言明として出典を問われうる（1 冊目の T1 は外す案を検討し、§2.6・§8.4 が指すのは後半なので前半を外す案は CE14 で不成立）。

### 15.19 T79 —— §6.5 の出典の無い経験の言明を、分析の言明に替える（+4 語・2026-11-16）

**種**: §15.18 で §6.5 第 2 文前半 *"silence on this subject has proved ambiguous in practice"* を「経験の言明で、出典を問われうる」とした。portfolio-50 がドシエを当て、出典が無いと確かめた —— 在るのは承認済み 141 本に ML・TDM の語が 0 件という沈黙の測定（`gap-measurements.md` §1.97・§1.133）で、それは「沈黙している」の証拠であって「実務で曖昧だった」の証拠ではない。逆向きの記録（Villa 氏の *"very clear good-faith arguments"*・against #132、Chestek 氏の #133）もある。

Before: *"It is stated expressly because silence on this subject has proved ambiguous in practice, and because …"* / After: *"It is stated expressly because silence on this subject leaves it to be inferred whether this is permitted, and because …"*

**理由**: 本文が出典の無い経験の言明を持つのは、T77 と同じ型の弱点である（審査者が「本当か」と問えば、本文の外に答えが無い）。新しい語は分析の言明で、沈黙すれば許しの有無は推論に委ねられる、という構造だけから真である（許しが在るとも無いとも前提しない）。後半の *"a permission that an automated system cannot determine"* へも繋がる —— 推論に委ねられた許しは、自動の仕組みには判定できない。1 冊目の T1 は前半を外す案で、外向きの引用のため CE14 で不成立だった。T79 は外さずに替えるので、§2.6・§8.4 が §6.5 を指す 3 か所（後半を指す）は変わらない。

**機械層**: 468r は前半の句を「過去の観察（偽にならない）」の除外として持っていた。新しい語には状態の語が無いので除外を外し、mutation は §6.4 の除外の句（*"not decided here"*）へ移した。

**⚠ 逆側**: (1) 新しい語は沈黙の害を弱く言う —— 旧い語は「争いになった」と言い、新しい語は「推論に委ねる」と言うだけで、推論が争われうることは言わない。(2) 1.0〜1.3 の文を引く外向きの記録は 1.4 では語が違う。(3) 出典が見つかれば（読みの側・2f・30）、旧い語に戻す選択もありうる。

**反例の担当へ（50・30）** **反例の結果**: 30 —— (a) は立たない（§6.5 第 1 文が、明示が無くても §3〜§5・§8 から許しが立つと言う）。**(b) は立つ**: ドイツ UrhG 31 条 5 項（目的移転の原則・Zweckübertragungsregel）は、利用の種類が個別に明示されていなければ、権利の及ぶ利用を契約の目的で決める（30 の読み・条文の写しは手元に無い）。この下で沈黙は許しを狭く読む方向に働くので、許しが在ることを前提にした *"leaves permission to be inferred"* は偽に読める。30 の案 *"leaves it to be inferred whether this is permitted"*（+4・許しの有無を推論に委ね、前提を置かない）を採った。副産物: 31 条 5 項は、§6 と §4.2 が利用の種類を名指しで並べる理由を法の側から与える（出典の在る理由）—— 逐条の §6.5 の行と法律家への問い 6 に足す（問い 6 は 30）。登録した問い: (a) *"leaves permission to be inferred"* が、§6 の明示が無い場合に許しが**無い**と読む余地を作るか（推し量れなければ許しは無い、という反対解釈）。(b) 「推し量る」が法の命題として偽になる場合（沈黙が許しの否定と読まれる法域・契約の解釈の規則）があるか。

### 15.20 T80 —— §8.4 の閾値を置かない理由の句を外す（−12 語・2026-11-16）

**種**: T77・T79 の型（理由の文が一部の場合・法域で偽）を、作用の動詞を持たない記述の文 35 に当てた（作用の動詞の無い文を機械で抜き、目で読んだ）。偽になりうるのは §8.4 末文 *"no threshold of how much of the Work was used is imposed, since You could not determine whether one had been crossed (Section 6.5)"* だけだった。You は学習する者を含み（§1.6）、自分の集めたデータで学習・微調整する者は Work をどれだけ使ったかを知りうる。

Before: *"since You could not determine whether one had been crossed"* / After: *"since You could not always determine whether one had been crossed"*

**理由**: 理由が真になる。偽の場合に「判定できる者には閾値が戻る」と読む分岐（T54 の型）は、前提が真になることで立ちにくくなる。§6.5 への参照（1 冊目の T1 が数えた 3 か所の 1 つ）は変わらない。

**⚠ 逆側**: (1) 「いつもは判定できない」は、判定できる者には閾値があってもよい、と読む余地を語の上で残す —— 結論 *"no threshold … is imposed"* は無条件だが、理由が場合分けを示唆する。(2) 理由の句ごと外す案（−9 語・*"(Section 6.5)"* の参照を失う）と比べてほしい。外すと §6.5 の後半を指す 3 か所が 2 か所になり、1 冊目の T1・CE11 の判断の前提が変わる。

**反例の担当へ（50・30）** **反例の結果**: 50 —— (a) は立つ: *always* は理由を真にするが、理由の句が「判定できない場合のための免除」と読まれると、判定できる者（自分のデータで微調整する者）について「理由が尽きれば規則も尽きる」の筋で閾値を持ち込む足場になる。T71 で閉じた E85（理由が範囲を狭める読み）と同じ型を新しく作る。(b) 句ごと外すと作用の句だけが残り、どの場合でも真で、狭める足場が無い。§6.5 後半の理由は §8.4 の閾値の有無を決めていないので、失うのは説明だけ（逐条の §8.4 の行へ移した）。(c) because / since / so that の句を機械で全部拾い、見落としなし。**→ 句ごと外す形に替えた（−12 語）**。登録した問い: (a) *always* が「判定できる者には閾値」の読みを作るか、(b) 外す案の方が当たる面が狭いか、(c) ほかの 34 の記述の文に、法域や場合で偽になるものを見落としていないか（35 の一覧は §15.18 と合わせて読む）。

### 15.21 T81 —— §10.4 第 1 文を文書の中の終了に絞る（+2 語・2026-11-16・【反例待ち】）

**種（portfolio-50・T80 の (c) の後半）**: §9〜§16 の記述の文 45 を「どの法域でも真か」で当て、§10.4 第 1 文 *"No permission granted by this Dedication terminates for any reason."* が当たった。米国では §4 の licence に 17 U.S.C. §203 の終了権が *"notwithstanding any agreement to the contrary"* で届く（`jurisdictions.md` §5a・法律家への問い 1）ので、35 年後に著作者が終了通知を出せば許しは終わりうる。文が法の命題として言い切っているので、一部の法域で偽になる。

Before: *"No permission granted by this Dedication terminates for any reason."* / After: *"No permission granted by this Dedication terminates under it, for any reason."*

**理由**: ドシエは既に「§10.4 は文書についての文で、外部の出来事まで生き残ると約束するライセンスは無い（§13.2 が免責）」と答えていた（`QUESTION-INDEX.md` の §8.2 と §10.4 の行）。本文の語をその答えに合わせた。第 2 文 *"contains no termination provision and no revival provision"* は文書の中身の言明で、もとから真。

**⚠ 逆側**: (1) *under it* は「法による終了は在る」と本文が自分で示す読みを作る —— ただし `ADOPTING.md` が §203 を名指すので、隠す利益は無い（50）。(2) §2.2 *"This Dedication is irrevocable."* も同じ問いを持ちうるが、*irrevocable* は Apache-2.0 など承認済みのライセンスが使う慣用の語で、法定の終了権に負けることは前提として読まれる —— *"for any reason"* のような言い切りを持たないので、変えない。(3) 50 の案のもう 1 つ *"Nothing in this Dedication terminates a permission granted by it, for any reason."*（+3）は、主語を文書にする点で同じ。短い方を採った。

**反例の担当へ（30・50）** **反例の結果**: 50 —— (a) 立たない: §8.2 は Dedicator の力の否定、§10.4 は文書の中の終了の事由の否定で、別の命題。§8.2 は特許の licence で §203 は著作権の grant だけに届くので、§8.2 の言い切りは米国でも真。(b) 立たない: §2.2 *"The Dedicator may not withdraw it, and may not impose any further term, condition, or restriction"* と §5.2(b) が閉じる。逆側: 旧文は「契約でない許しは許諾者が自由に撤回できる」読み（Cowan 氏 2000・objection-map の *"a bare permission can be freely revoked by the licensor"* の行）にも本文の言葉で答えていたが、*under it* の後はその答えを §2.2（撤回しない）と §2.5（禁反言）が持つ —— §10.4 から抜けるのは重複で、失う答えは無い。 **1 冊目の記録との関係**: `ACD-1.4-CLARITY-TRIAL.md` の §4.4（F3）と CE9 は、§10.4 第 2 文の *because* の反対解釈（違反しうるものが見つかれば終了できる）を「第 1 文 *"No permission granted by this Dedication terminates for any reason"* が無条件なので立たない」で閉じた。T81 の後の第 1 文も、文書の中の終了の事由については *"for any reason"* のまま無条件なので、その結論は保たれる（引用の語だけが 1.4 の本文から外れる・portfolio-50）。登録した問い: (a) *under it* が、§8.2 の *"not terminable by the Dedicator on any ground"* と食い違う読みを作るか、(b) Dedicator が別の文書（例えば別の契約）で許しを終わらせうると読む余地を作るか（§2.2 の撤回不能と §5 の約束が閉じると読む）。

### 15.22 T82 —— §14.1 の全部免責に、外せない責任の除外を先に置く（+29 語・2026-11-16）

**種（portfolio-2f・§1.258）**: Chestek 氏 2023-02-18（個人として）*"My understanding is that the clause isn't effective in the same way in some countries and would instead be ignored altogether, leading to liability for everything, not just the unwaivable claims."* —— §14.1 の *"TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW"* はこの型で、縮減を認めない法域では §14 全体が落ちる読みが立つ。`jurisdictions.md` は縮減を §15.4（1.0 の番号）と §3 にだけ当て、§14 には当てていなかった。

**先例（アーカイブ）**: EUPL の起草者 Schmitz 氏 2010-10-07（`license-review` "For Approval: The netX Public Lisense"）*"In European countries, and especially in Germany, courts have invalidated general exclusions, and even exclusions "to the extend allowed by the law" are considered as unfair regarding contract & protection of consumers law. This is the reason why the OSI-approved European Union Public License … does not exclude liability in case of wilful misconduct … and in case of damages to natural persons"*。EUPL-1.2 §8 *"Except in the cases of wilful misconduct or damages directly caused to natural persons"*。

Before: *"TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW, THE DEDICATOR IS NOT LIABLE …"* / After: *"EXCEPT FOR LIABILITY FOR WILFUL MISCONDUCT OR GROSS NEGLIGENCE, OR FOR DEATH OR PERSONAL INJURY, WHICH NOTHING IN SECTION 14 LIMITS, AND TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW, THE DEDICATOR IS NOT LIABLE …"*

**語の選び方**: 30 の予告への答え —— ドイツ BGB 309 条 7 号は a（生命・身体・健康の侵害は単なる過失でも）と b（その他の損害の重過失）を約款で外せない（30 が条文を取得）。初めの案（故意と死亡・身体の傷害）は b を覆わず、約款と読まれれば §14.1 は縮減されずに全体が落ちる。重過失を入れた。贈与と読まれれば 521 条で贈与者はもともと故意と重過失にしか責任を負わないので、失うものは無い。EUPL の *"damages directly caused to natural persons"* は個人へのあらゆる直接損害と読めるので、英国 UCTA s.2(1) の語（死亡・身体の傷害）に絞った。

**⚠ 逆側**: (1) +22 語（B3）。(2) 全部免責の承認済みのライセンス（MIT・BSD）より免責が狭く見え、採用者が「責任が残る」と受け取りうる —— ただし残るのは、どの法域でも外せないか外しにくい責任だけで、Apache-2.0 §8 も *"(such as deliberate and grossly negligent acts)"* を名指す。(3) §14.2（法が許す最大の範囲に限る）は残し、ほかの外せない責任（消費者法など）を受ける。(4) §13（無保証）には同じ問いが立ちにくい（贈与なら 524 条で悪意の隠蔽だけ・30 の読み）ので変えない。(5) 日本の消費者契約法 8 条（故意・重過失の全部免責は無効）にも当たる形になる（`jurisdictions.md` の行）。

**反例の担当へ（30・50）** **反例の結果**: 30 —— **(c) は立つ**: §14.2 *"Where applicable law does not permit the exclusion or limitation of a liability, that liability is limited to the greatest extent that law permits"* は、§14.1 が除外から外した責任（まさに法が除外も制限も許さない責任）を「法の許す最大限まで制限する」と読め、309 条 7 号は *"ein Ausschluss oder eine Begrenzung der Haftung"*（除外も制限も）を禁じるので、§14.2 の側から同じ問題が戻る。30 の案 *"WHICH NOTHING IN SECTION 14 LIMITS,"*（+6）を除外の句に足した —— 除外の句の中で完結し、§14.2 は「その他の責任」の縮減の文として残る。(b) 立たない（AND で並ぶ 2 つの句で、除外は「法の許す限り」の下に入らない。足した句が除外の独立をさらに明示する）。(a) 低い（Apache-2.0 §8 が先例・輪郭の争いは除外された責任の側にだけ生じる。逆側: 州で gross negligence と recklessness の境が違う）。**9b —— 除外が無条件**: 法がその責任の除外を許す法域でも Dedicator に責任を残し、承認済みの先例（Apache-2.0 §8 *"unless required by applicable law (such as deliberate and grossly negligent acts)"*、MPL-2.0 §7 *"to the extent applicable law prohibits such limitation"*）はどれも法に条件を掛けている。採用者（B2）にとって MIT より重い責任が残るのは害なので、除外を *"THAT APPLICABLE LAW DOES NOT PERMIT TO BE EXCLUDED"* に条件づけた（+7）。範疇（故意・重過失・死亡・身体の傷害）は名指したままなので、ドイツの裁判所から見て除外の範囲は読める（Schmitz 氏の言う「法の許す限り」だけの全部免責とは違う）。**逆側**: 条件は「どの責任が外せないか」を法に委ねるので、透明性の要件（50 の (2)）の問いは残る —— EUPL の無条件の形の方がドイツでは堅い。採用者の負う責任（米国）とドイツでの堅さの取引で、前者を取った。綴り: *wilful* は草案の英国綴り（licence・authorise など）と揃う（9b）。**30 の 2 巡目（条件づけた形）**: 採ってよい。(a) 約款と読まれる場合、309 条 7 号が禁じる範疇（a: 生命・身体・健康は軽過失でも、b: その他の損害は重過失）は名指した 4 つと重なり、条件が満たされて除外が働き、残りの全部免責は 7 号に当たらない範囲で立つ。贈与と読まれる場合は、事前に外せないのは故意だけ（276 条 3 項）なので、§14.1 は重過失も免じ、贈与者の責任は故意だけになる（521 条より有利）。残る危険は 307 条 1 項 2 文の透明性の要件 —— 範疇を名指すので裸の *soweit gesetzlich zulässig* よりは透明と読むが確かではない（問い 9・30）。(b) 上限を許す責任の上限の放棄は、狭い 4 つの範疇で、無償の Dedicator が失うものは小さい。日本の消費者契約法 8 条 1 項 2 号とも整合する。 **9b の追加の問い（merge の後）**: §14.2 *"Where applicable law does not permit the exclusion or limitation of a liability, that liability is limited to the greatest extent that law permits"* は、文の上では §14.1 が除いた責任も拾い、法が除外は禁じても上限は許す責任について、§14.1 と逆を言う、と読めるか。**1c の判断（変えない）**: §14.1 の句 *"WHICH NOTHING IN SECTION 14 LIMITS"* は §14 全体を名指すので §14.2 を含む —— 特別の規定が一般の規定に勝つという解釈に頼らず、語で §14.2 を外している。§14.2 に *"Subject to Section 14.1's exception"* を足す形（+5）は同じことを 2 度言う。50 —— 30 の (c) に同意。透明性の要件で §14.2 そのものが効力を失う読みは本文で閉じられないので、法律家への問い 9 (c) に「約款と読まれた場合」を足す（50）。残る点（試作にしない）: ドイツの 307 条の判例（本質的な義務の違反の責任は軽過失でも外せない）—— 無償の一方的な付与に本質的な義務が在るかは法律家への問い 9。登録した問い: (a) *GROSS NEGLIGENCE* の語が、コモン・ローの法域で輪郭の争いを生むか（米国の州で gross negligence の定義が違う）、(b) 除外と *"TO THE FULLEST EXTENT"* の順で、除外が「法が許す限り」の下に入ると読まれないか、(c) §14.2 と重なる部分の整理。

### 15.23 §2.3 の受諾の言い切りと、"irrevocable" の 4 か所（どちらも変えない・2026-11-16）

**§2.3（「どの法域でも真か」の続き）**: *"This Dedication takes effect without any act of acceptance by You. To hold a permission granted here, You need not know of this Dedication …"* は法の効果を言い切る形で、§4 を契約と読む法域では、申込みを知らない受け手に受諾の意思が無いので許諾が成立しないと読む余地がある —— ドイツ BGB 151 条は受諾の表示を要しないだけで受諾そのものは要し（portfolio-30 が条文を取得）、日本の民法 527 条も承諾の意思表示と認めるべき事実を要する。**変えない理由（30 の読み）**: (1) 危険は条文ではなく法の側にあり、"takes effect" を Dedicator の要求の言明（*"The Dedicator requires no act of acceptance"*）に絞っても、知らない受け手の地位は変わらない —— §2.5（禁反言）は信頼を要するので知らない受け手には効かず、§15.2（reform）は成立しない契約を成立させない。(2) 絞ると B10 の gap の主張と入口の文（`review-responses-clauses.md` の *"the same structure that MIT-0 and 0BSD rely on"*）を弱めるだけである。(3) T81 との違い: §10.4 は外部の法（17 U.S.C. §203）が明らかに否定する命題を言い切っていた。§2.3 の *"You need not know"* は、文書が課す条件の文（この Dedication は知ることを条件にしない）として読める。ドイツには一方的な同意（schlichte Einwilligung・BGH 2010-04-29 I ZR 69/08・判決の原文はまだ取得できていない）という別の道があり、受諾を要しない —— ただし将来に向かって撤回できると読まれ、§2.2 と食い違う。法域の読みは 30 が `jurisdictions.md` と法律家への問いに書き、against #321 から指す。**逆側**: 審査者が「文書が法の効果を言い切っている」と読む可能性は残り、その場合の答えは上の「条件の文」の読みである。

**"irrevocable" の 4 か所（portfolio-2f・2026-11-16 の読み）**: Berkus 氏 2025-08-15（MIT-I の審査）は、既に頒布された写しについて撤回できないと明記することを *"a bit redundant"* とした。1.4 草案は *irrevocable* を §2.2（*"This Dedication is irrevocable."*）・§3.1・§4.1・§8.1 に持つ。**変えない理由**: §2.2 は Dedication 全体の性質、§3.1 は放棄の行為、§4.1 と §8.1 は許諾の性質を述べ、役割が違う。同じ審査で委員長は *perpetual* と *irrevocable* の語を許諾の語として求めており（`review-precedents.md` §1.47）、§4.1・§8.1 から語を外すとその最小限を外れる読みが立つ。**逆側**: 4 か所の繰り返しは長さ（B3）の一部で、Berkus 氏の「冗長」の評に当たる。

### 15.24 T83 —— §14 が Dedicator 自身の約束の違反を免責しないと明示する（+27 語・2026-11-16）

**依頼**: オーナー 2026-11-16「ACD-1.4-DRAFT.txt の法的解釈の不確実性を『５人』で減らし続けてください」。分担は 9b の案（9b が解釈の割れる型の一覧を道具で出し、1c が試作、30 が反例、50 が問いへ移す、2f が先例）に、30 の 3 分類（(A) 本文の曖昧さは語で、(B) 法の不確かさは一次の法源か「どちらの読みでも同じ結果」の形で、(C) 法律家にしか決められないものは問いを狭めて）を重ねる。1c は、法律家への問いのうち**起草で答えが決まる部分**から始める。

**種（`QUESTIONS-FOR-COUNSEL.md` 問 9 (a)）**: §14.1 *"… LOSS OR DAMAGE ARISING OUT OF THIS DEDICATION OR THE USE OF THE WORK"* は、文字どおりには Dedicator 自身の約束（§5・§8.6・§12.2）の違反まで免責する。約束を破って受け手を訴えた Dedicator に、受け手の防御の費用を負わせられないと読める。問いの記録は「答えがあれば、§14.1 を使用の免責に絞るか、約束を制限しないと言うかが変わる」と書く —— 法が決めるのでなく、起草の選択で決まる。

After（§14.2 の末）: *"Section 14 does not limit the Dedicator's liability for asserting a claim, or exercising a right, in breach of a covenant in Section 5, 8.6, or 12.2."*

**語の選び方**: GPL-3.0 §16 の形（*"arising out of the use or inability to use the program"*）に絞る案は、約束に反した訴えも「Work の使用から生じた」と読めるので、不確実性が残る。明示する方を採った。§14.1 の大文字の文には置かず §14.2 に置いたのは、§14.1 の除外（T82）と並べると 1 文が長くなりすぎるため。

**どの問いが消えるか**: 問 9 (a) は消える（本文が答える）。問 9 (b)（誰が守られるか）と、T82 の後の透明性の問いは残る。

**⚠ 逆側**: (1) Dedicator は自分の約束の違反について責任を負う。例えば自動の削除要請や、Work についての利用規約の強制（§5.2(b)）が約束に反すれば、損害の責任が生じうる —— ただし約束は Dedicator 自身の行為で、避けられる。(2) 採用者の顧問は、全部免責の承認済みのライセンス（約束を持たない MIT など）より責任が広いと受け取りうる。(3) +20 語（B3）。(4) §12.2 の同意（T67）は約束ではないので、この文に入らない —— 同意を「撤回」して訴えることは §2.2 と §12.2 の約束が受ける。

**反例の担当へ（30・50）** **反例の結果**: 50 —— (a) 故意・重過失の除外と重なる部分はどちらも「制限しない」で食い違わない。(b) §5.3 の受益者への責任も「Dedicator の責任」に入り、§5.3 の目的に合う。(c) 免責しないことは責任を作らないので §2.5 の性質を変えない。**当たった点**: §5.2(b)（利用規約・アクセス条件で義務を課さない）は、Dedicator が配布に使うホスティングの規約やダウンロードのログインで気づかずに破りうるので、その損害を一切制限しないと採用者の負担が MIT より重く読める（B2）。**→ *asserting a claim* に絞った（+3）**: 主張の形の約束（§5.1・§5.2(a)(c)(d)・§8.6・§12.2）は入り、§5.2(b) だけが外れる。§5.2(b) の違反は、§5.3 の受益者が抗弁として頼れば足りる。30 —— (a) 約束が契約として成立すれば BGB 280 条・民法 415 条の損害賠償が立ち、成立しない場面では文は空になるが約束は抗弁として働くので害は無い。(b) *asserting* は §5.1・§8.6 の約束と同じ動詞で、警告状や DMCA の notice も含むと読む（米国で訴答の語として狭く読まれても、約束と一緒に動くのでずれない）。**(c) は立った**: §12.2 は *exercise* の約束で、フランスの撤回権・修正権（CPI L121-4）のように請求を立てない行使は *asserting a claim* に当たらない → *"or exercising a right"* を足した（+4）。条件 *"in breach of a covenant"* が範囲を約束に縛るので、§5・§8.6 の側で余分になる害は無い。登録した問い: (a) 約束の違反の責任が、§14.1 の除外（故意・重過失）と重なるときの順序、(b) §5.3 の受益者（後の受け手）にもこの文が及ぶか（*"the Dedicator's liability"* に宛先が無いので、受益者に対する責任も含むと読む）、(c) 約束の違反を「免責しない」ことが、約束を契約と読ませる向きに働き、契約でない約束としての性質（§2.5 の禁反言）と食い違うか。

### 15.25 T84〜T88 —— 法の効力の言い切りと、2 通りに読める指し方を、語で 1 つに定める（+6 語・2026-11-16）

§18 の ②（語を変えれば法域に依らなくできる）と、portfolio-9b の `scan_draft_ambiguity.py` が出した語の揺れから、同じ型の 5 つを 1 つの PR にした（反例を一度に当てられるように）。

| 試作 | 条 | Before → After | 消える／狭まる不確実性 | 語 |
| :-- | :-- | :-- | :-- | --: |
| T84 | §2.6 第 4 文 | *"No separate instrument, assignment, or agreement is needed …"* → *"This Dedication requires no separate instrument, assignment, or agreement …"* | 書面と権利ごとの明示を求める法域（CPI L131-2・L131-3）で旧文が偽になる読み（§18.1）。法が書面を求めるかは言わなくなる | 0 |
| T85 | §8.2 | *"not terminable by the Dedicator on any ground"* → *"… under this Dedication on any ground"* | 贈与と読まれたときの法定の撤回（BGB 530 条・533 条、民法典 953 条・955 条）で旧文が偽になる読み（§18.3・portfolio-50）。T81 と同じ型 | +3 |
| T86 | §8.6 | *"it operates in every jurisdiction"* → *"it is given for every jurisdiction"* | 対価の無い約束が効かない法域で、効力の言い切りが偽になる読み（§18.3・50）。文の役は範囲 | +1 |
| T87 | §2.6・§5.3・§6.2・§6.3・§8.4（2 か所）・§11.3・§11.4・§12.2 | *"this Section"* → *"Section 8.4"* など条番号 | 小項の中の *this Section* が節全体（*"Section 8"* の書き方）とも読める揺れ。§8.4 の *"deliberately absent from this Section"* は §8 と読むと §8.1 に但し書きが在るので偽になる（9b の (h)）| 0 |
| T88 | §14.2・§2.5 | 例外の列 *"Section 5, 8.6, or 12.2"* → *"Section 2.5, 5, 8.6, or 12.2"*、§2.5 *"will not assert"* → *"covenants not to assert"*（30 の (d)）| §2.5 の Dedicator の約束（撤回や無効を主張しない）が T83 の列から漏れ、その違反の責任を §14.1 がまだ外す読み（9b の (k)）| +2 |

**機械層**: 468u の §8.2 の目印（B10 の立証 `gap-measurements.md` §1.133 が依拠する句）と、§8.2・§8.4 の mutation の anchor を新しい語へ移した。errata E42 の引用は *as adopted on* の形にした。

**⚠ 逆側**: (1) T84・T85・T86 は、法が書面を求めない・撤回を許さない・約束を効かせる法域では、旧い文の方が受け手に強く告げていた —— 新しい文は文書の言明に留まり、法の効果は法に任せる。(2) T85 の *under this Dedication* は、法定の終了の事由が在ることを本文が自分で示す。(3) T87 で条の中で自分を番号で呼ぶのは読みにくい（§16.4 は T62 から同じ書き方）。

**反例の担当へ（30・50）** **反例の結果**: 50 —— 反例なし（§14.2 の列は §5.2(b) の「課す」だけの違反を外し、その規約で訴えたときは入る）。取り残しとして §2.9 の *"suspended by, or revived by … any act of a trustee"*（InsO 134 条の否認に負けうる）を次の束へ。30 —— (a)(b)(c) 立たない（§5.3 末文の旧 *this Section* は節 5 全体とも読めたが、§3・§4 は §5 を引かないので害は無い）。**(d) は立った**: §2.5 は自分を covenant と呼ばず、*a covenant in Section 2.5* が §2.5 の中に covenant を探させ、禁反言まで含むと読まれる。§2.5 を *"covenants not to assert"* にして動詞を揃えた（+1）。登録した問い: (a) T84 の *requires no* が、提出者に別の手続きを求めないことの約束（§2.6 第 1 文の既定）を弱めるか、(b) T86 の *is given for* が、§2.4 の独立の足場の読み（第 2 の足場）を弱めるか、(c) T87 の 9 か所のうち、節全体を指していたものが無いか（§6.2 *"Section 6.2 is bounded by Section 2.7"* など、どれも自分の小項を指すと読んだ）、(d) T88 の §2.5 は *"will not assert"* の約束と禁反言の 2 つを持つ —— *a covenant in Section 2.5* が禁反言まで含むと読まれる害があるか。

### 15.26 T89 —— §2.9 を文書の中の効果に絞る（+3 語・2026-11-16・【反例待ち】）

**種**: portfolio-50 と 30 が §18 の ② として送り、T84〜T88 の束から取り残した（50 の 1 巡の指摘）。§2.9 *"Nothing in this Dedication is conditioned on, suspended by, or revived by an insolvency … or by any act of a trustee …"* は、倒産手続と管財人の行為の**効果**まで言い切る。管財人が無償の処分を否認できる法域（ドイツ InsO 134 条・30 が条文を取得）では偽になりうる —— T81 と同じ型。

After: *"Nothing in this Dedication is, under its terms, conditioned on, suspended by, or revived by an insolvency …"*

**消える／狭まる不確実性**: ドイツで旧文が偽になる読み（§18.1 の §2.9 の行）。否認されうるかは法の側に残り、問 8 が持つ。米国では Tempnology（2019）で拒絶は解除ではなく既に与えた権利は残る（2f）ので、旧文は米国ではほぼ真だった。

**⚠ 逆側**: (1) *under its terms* は、法による停止・否認が在ることを本文が自分で示す。(2) 第 2 文（管財人を §2.8 の譲受人として扱う）は変えないので、管財人が §2.8 の拘束を受けるかは法が決める（問 8）。

**反例の担当へ（30・50）**: (a) *under its terms* が、*conditioned on* の部分（文書の条件の言明・もとから真）まで弱めると読まれるか、(b) 第 2 文の *"Such an officer is a person to whom rights are transferred"* も効果の言い切り（管財人が譲受人に当たるかは法が決める）で、同じ型か。

### 15.27 T90・T91 —— 法律家への問い 5 のうち起草で決まる 2 つ（+30 語・2026-11-16）

| 試作 | 条 | Before → After | 消える／狭まる問い |
| :-- | :-- | :-- | :-- |
| T90 | §5.1 第 2 文 | *"any claim or cause of action, whether now known or unknown, for a use of the Work that this Dedication permits"* → *"… that treats as wrongful, or as without legal basis, a use of the Work that this Dedication permits"* | 問 5 の本体: 記録は「*for* が、使用そのものを違法とする請求（不当利得・不正競争）を入れ、使用に付随するだけの請求（動かした機械による傷害）を外す、という線を引くかは試していない」と書く。我々の読みを語で定めた —— 問 5 の本体は狭まる（線は語で引かれ、その語が法でどう読まれるかが残る）|
| T91 | §5.2 末段 | 末に *"A copy of the Work, or of part of it, contained in that material remains the Work, or that part of it."* | 問 5 の第 3 の小問: Work を同梱したインストーラーとクリックスルーとライセンスキーを、裁判所が 1 つの「他の素材」と扱えば、除外が Work を制限する規約まで届く。§2.1 の *every separable part* だけに頼らず、語で閉じた —— 小問は消える |

**468u の目印**: §5.1 の *"other than for patent infringement"* は残る（T90 は *for a use* だけを替えた）。§5.2 の *"other than the Work, that the Dedicator itself makes or makes available"* の行は動かしていない（mutation の anchor）。

**⚠ 逆側**: (1) *treats as wrongful* は新しい語で、承認済みのライセンスに先例が無い。*for* は短いが線を引かない。(2) T91 は、Dedicator が自分の製品やインストーラーの中の Work の写しにも §5 の約束（§5.2(b) の規約で義務を課さない）を負うことを言い切る —— 製品の中に Work を同梱する採用者は、製品の規約が Work の部分に及ばないよう書く必要がある。(3) +15 語（B3）。

**反例の担当へ（30・50）** **反例の結果**: 50 —— **(a) は立った**: 不当利得は使用を違法とせず「法律上の原因が無い」と言う請求（BGB 812 条 1 項 1 文の 2 つ目の場合 *ohne rechtlichen Grund*・民法 703 条「法律上の原因なく」）で、*treats as wrongful* だけでは残すつもりの請求が外れる → *"or as without legal basis"* を足した（+5）。50 のもう 1 案 *"depends on … being unauthorised"* は、許諾の不在に依らない不正競争（模倣）の請求を外すので採らなかった。(b) Dedicator 自身の改変: 改変しない写しは T91 で Work、改変した部分は他の素材、改変されずに残る部分は §2.1 で Work —— 反例なし。(c) SaaS: 末段第 1 文は写しを渡さない場面だけを除くので、T91 は SaaS の規約へ戻らない —— 反例なし。30（2 巡目・条文は rounds に）—— (a) *legal ground* は通じるが、英語の不当利得の文献で据わるのは *without legal basis*（英国の議論は Rechtsgrund をそう訳す）→ 替えた（0 語）。(b) 日本の 703 条は直訳、フランス 1303-1 条は「正当化されない」を「義務の履行も無償の意思も無い」と定義し *legal basis* の範囲に入る —— **しかも 1303-1 条は損失者の無償の意思から生じた利得を明文で不当でないとするので、Dedication が効く所では不当利得の請求は法律の要件の段階で立たない**。T90 の追加が効くのは許しが成立しない所（約束が最後の受け皿になる所）に限られ、そこでこそ要る。**(c) は立った（弱い）**: 一部だけを同梱した場合に *copy of the Work* と言えるかが開く → *"A copy of the Work, or of part of it, contained in that material remains the Work, or that part of it."*（+9）。**残る問い（逆側・法律家へ）**: 許しが成立しない法域で、その使用はなお *"a use of the Work that this Dedication permits"* か —— *permits* を「文書が許すと述べる」と読めば約束は働き、「法的に有効に許している」と読めば受け皿が要る場面で約束が外れる。§15.1（受け手に多く与える読み）は前者を選ぶ、が 30 の読み。(d) 読みの記録: Dedicator 自身のモデルが Work を逐語で含むなら、その逐語は Work の写しで、モデルの規約はその部分に掛からない（§6 の設計と合う向き）。登録した問い: (a) *treats as wrongful* が、損害の請求（使用が違法だと主張せず、損害だけを求める形）を外すと読まれる道が無いか、(b) T91 で「Work の写し」と「Work を変えたもの（Dedicator 自身の改変）」の境 —— Dedicator が自分で改変した写しは Work か、他の素材か、(c) T91 が §5.2(b) を、Dedicator の SaaS の規約（Work の写しを渡さない場面）にまで戻すと読まれないか（*"without providing a copy of the Work"* の場面は写しが無いので当たらない、と読む）。

### 15.28 T92・T93 —— 準拠法の第 2 文を外し、約束が許しの効否に依らないと語で言う（−13 語・2026-11-16）

| 試作 | 条 | Before → After | 消える／狭まる問い |
| :-- | :-- | :-- | :-- |
| T92 | §15.3（1.0 では §15.7） | 第 2 文 *"It is intended to operate under the law of each jurisdiction in which the Work is used, according to that law."* を外す（−21） | 問 7: 第 1 文 *"specifies no governing law"* と第 2 文（使用地の法を指すように読める）が食い違い、契約の側で Rome I 3 条の黙示の選択と読まれる余地があった。侵害の側は Rome II 8 条 1 項・3 項が保護国法を合意で外せない形で決めていて、第 2 文は何も足さない（`QUESTIONS-FOR-COUNSEL.md` 問 7 の 2026-11-16 の段が引く EU の法源・`rounds/2026-11-16-eu-tdm-and-conflict-of-laws-snapshot.txt`。Brussels I bis の読みは条文未取得の我々の読み）。問いの記録は「働かないなら外せる」と書く —— 問 7 の「第 2 文を残すか」は消える。契約と読まれた場合の準拠法（Rome I 4 条 2 項）は残る |
| T93 | §5.1・§5.2(d) | *"a use of the Work that this Dedication permits"* → *"… permits or purports to permit"*（2 か所・+8） | 問 5 の第 6 の問い（30 が出し 50 が置いた）: 許しが成立しない法域で、その使用はなお「この Dedication が許す使用」か。*permits* を「法的に有効に許す」と読めば、約束が最後の受け皿になる場面で約束が外れる。語で答えた —— 問いは消える |

**語の選び方（T93）**: *describes as permitted* は「列挙して述べたものだけ」と狭く読まれうる。*permits or purports to permit* は、有効な許しと、効かない法域の許しの両方を含む。§4.4・§8.6・§12.2 の「足場は互いに依らない」と揃う。

**⚠ 逆側**: (1) T92: 第 2 文は「各法域の法で働くことを意図する」と Dedicator の意図を告げていた。50 の 1 巡の記録: 第 2 文は Rome I 3 条 1 項の黙示の（法域ごとに分けた）選択と読まれうる唯一の文で、外すと選択が無いことがはっきりし、契約の側は 4 条 2 項で Dedicator の常居所地の法になる（オーナーなら日本法）。侵害の側は Rome II 8 条 3 項で変わらない。契約の側の法が利用地から Dedicator の地へ移るのは、受け手には予測しやすく、法域ごとの効き方の差は §15 の他の条が受ける —— 不利と言い切れない。外すと、契約と読まれた場合の準拠法は Rome I 4 条 2 項の既定（Dedicator の常居所地）に任される —— 受け手には遠い法になりうる。ただし第 2 文があっても、それが選択として認められるかは不確かだった。(2) T93: *purports* は「称する」の語で、許しが効かない場面があることを本文が自分で示す。(3) §5.2(d) は Dedicator 自身の私権（プライバシー・パブリシティ）の不行使で、*purports to permit* は「Dedication が許すと称する使用」—— 私権は §11.4 が許さない（Dedication の外）ので、*permits* の範囲は §4 の使用で、*purports* で広がらないと読む。

(4) T92（9b の読み）: §15.3 から第 2 文を外すと、「法の許す限り」型の文（§2.8・§3.1・§9.2 など）がどの法を指すかを本文の中で受ける文が無くなり、法の選択は抵触法に任される —— ただし第 2 文は意図の表明で抵触法を変えなかったので、効果は同じ。

**反例の担当へ（30・50）** **反例の結果**: 30（法律家の確認なし・EU の法源は 2f の帯）—— (a) 立たない: 第 1 文は「選ばない」の言明として足りる。Rome I 3 条 1 項は契約の一部についての選択を認めるので、旧第 2 文は部分ごとの選択と読まれる余地があり、外せばその読みは消える。契約と読まれた場合の 4 条 2 項（Dedicator の常居所地）の費用はもともと在った。事業者の Dedicator と消費者の受け手なら 6 条が受け手の常居所地の強行規定を残す。(b) 立たない: §11.1 *"grants no right"*・§11.4 *"does not purport to give it"* が自分で「称さない」ことを言うので、*purports to permit* が §11 へ約束を広げる道は本文が閉じている（逆側: §15.1 が *purports* に掛かると範囲が広がる余地 —— Dedicator 自身の約束なので受け手の害にはならない）。(c) 立たない: *no forum* は Brussels I bis 25 条の合意管轄が無いと言うだけで、一般の管轄はそのまま働く。登録した問い: (a) T92 の後、§15.3 が 1 文だけで、Rome I の下で「準拠法を選ばない」意思表示として足りるか、(b) T93 の *purports to permit* が、Dedication が許さないもの（§11 の商標・私権）まで「許すと称する」と読まれて約束が広がる道が無いか、(c) 第 1 文の *"no forum"* が Brussels I bis の下で何をするか。

### 15.29 T94 —— 特許の行為の列挙に、主要な法域の法の語を足す（+6 語・2026-11-16）

**種**: 法律家への問い 2 (g)。§8.1・§8.4 の *"make, have made, use, offer to sell, sell, import, and otherwise practise or transfer"* は、日本の特許法 2 条 3 項（貸渡し・輸出）、ドイツ PatG 9 条（所持）、英国 Patents Act 1977 60 条 1 項 (a)（*keeps*）の行為を *otherwise practise* に頼り、記録は「試していない」と書く。

After（2 か所）: *"make, have made, use, offer, sell, lend, lease, import, export, keep, possess, and otherwise practise or transfer"*（*offer to … transfer* は 9b の反例: 英国 s.60(1)(a) の *offers to dispose of*）

**消える／狭まる問い**: 問 2 (g) は、名指した 4 つの行為については消え、残りを *otherwise practise* が受けるかの問いに狭まる。

**先の反例（portfolio-50・予告への答え）**: (1) 列挙は挙げた物以外を外す読みを招く —— *keep*（英国）を足した。(2) *possess* は PatG 9 条では「挙げた目的のため」の所持で、目的なしの所持に許諾が要る読みを本文が認めることにはならない。許諾は広く与える側なので、余計な行為を挙げても受け手は損をしない。

**⚠ 逆側**: (1) 列挙はそれでも尽きない（日本の *展示* は *譲渡等の申出* の一部）。(1b) 裸の *offer* は、米国 35 U.S.C. §271(a) と Apache-2.0 §3 の *offer to sell* より広い —— 審査者が承認済みの語との差を問えば、理由は英・独・仏の「使用の申出」（50）。目的語は列挙の後の *the Work or anything derived from it*・*any model … resulting from Computational Use* が決め、§8.5 が請求を Dedicator の持つものに閉じるので、Dedicator の想定外の負担は増えない。**反例の結果**: 30・50 とも反例なし（50: §8.6 の *any act that those Sections describe* は新しい列挙をそのまま受ける）。(2) +8 語（B3）。(3) §8.1 と §8.4 の列挙の並行（同じ語で同じ効果）は保った。

**反例の担当へ（30・50）** **反例の結果**: 30（4 法域の条文は rounds に）—— (a) 立たない: *keep*（英 s.60(1)(a)）と *possess*（独 9 条 *besitzen*・仏 L613-3 *la détention*）は法域ごとに別の語で、両方を挙げると各法域の語に名指しで当たる。**(b) は立った**: 日本の「貸渡し」は有償・無償を問わないが、英語の *lend* は無償の貸与を指す → *lease* を足した（+1）。(c) 立たない: *export* は行為の名で、§2.7 は請求項の範囲を限る文。(d) 列挙に無い語: 仏 L613-3 の *le transbordement* と日本の「電気通信回線を通じた提供」は *otherwise practise or transfer* に入ると読める —— ソフトウェアの特許ではネット経由の提供が中心の行為になるので、名指すかは語数との取引（*provide over a network*・+4）で、今回は見送る。(e) 立たない: 申出の *transfer* と末の *transfer* は同じもの（譲渡）を指す。ただし (b) を採るなら申出の側も *lease* を含めないと、日本の「貸渡しの申出」が名指しから落ちる → *offer to sell, lease, or transfer* にした。9b —— 英 s.60(1)(a) の *offers to dispose of* → 初めは *offer to … transfer*、30 の法源への当てで、英・独（*anzubieten*）・仏（*l'offre*）とも申出を売る申出に限らず、方法の発明の「使用の申出」も数えると分かり、**申出を *offer* だけにした**（−5 語ずつ・申出の対象の列挙が要らなくなる）。仏 L613-3 の *le transbordement*（積み替え）は *otherwise practise or transfer* に任せて見送った。登録した問い: (a) *keep* と *possess* の重なり（英国の *keeps* は所持の一種）を両方挙げる害、(b) *lend* が日本の 2 条 3 項の *貸渡し* に当たるか（有償・無償を問わない語として）、(c) *export* が §2.7（Dedicator の持つ請求項だけ）と食い違わないか。

## 16. 模擬委員会 —— 記録に立場が厚く残る審査者の目で 1.4 草案を通読する（2026-11-15〜）

**仕組み**: オーナーの依頼（「5 人で話し合って、より良い案をガンガン実行して」）を受けて、portfolio-1c が出し 5 人で決めた。記録に立場が厚く残る 5 人の審査者を 1 人ずつ受け持ち（30 = Chestek 氏、50 = Fontana 氏、2f = Perens 氏、9b = Smith 氏、1c = Villa 氏）、その人の過去の文だけを根拠に、その人の目で 1.4 草案を頭から通読して「どこを突くか」を条番号つきで出す。根拠の無い推測は書かない（必ずその人の文を引く）。各節は表（基準と出典 | 当たる条 | 扱い済みの場所 | 残る点）と、条を変える指摘（試作の種）を持つ。**0 件でも表を残す** —— 審査者の基準を網羅して当てた記録になる。**この節が establish しないこと**: 模擬であって、その人が実際にそう言うことを意味しない。

### 16.1 Villa 氏の基準を 1.4 草案に当てた（portfolio-1c・条を変える指摘 0 件）

| 基準と出典 | 当たる条 | 扱い済みの場所 | 残る点 |
| :-- | :-- | :-- | :-- |
| 却下は OSD に明らかに反するものと明文の方針に限るのが適切だが、実務では *"being poorly written and/or duplicative was sufficient"*。OSD は特許などで曖昧（2019 頃の整理・`reviewer-positions.md`）| 全体（起草の質）・§8 | 1.4 の試作 T34〜T71 と errata E39〜E85 は起草の質を直した記録。§8 は特許を明示する | 長さ（B3）と、法律家の関与が無いこと（B1）は残る |
| *"Apache fills the same purpose[1] (permissive license) while being better drafted and properly handling patents."*（`review-readings.md` §1.178 の追記）| §8・B10 | B10（既存に無い効果）と `comparison.md` が Apache-2.0 との差を述べる | 「Apache-2.0 で足りないか」は B10 の H1-g と同じ問いで、量の問いとして答える（`SUBMISSION-MATERIALS.md` §0d） |
| *"If you/your community/your project have not already conducted a review of the basic license, this isn't the place to get that done."*（2013-11-17）| 提出の手順 | 段 6b（list に 30 日）と法律家への問いの文書 | B1（法律家の審査が無い）は残る |
| *"it's impossible to prove the negative"*（B2 の文脈）| 採用 | B2 の記述がこの発言を伏せていないことを確かめた（register） | 採用の数（B2）は変わらない |
| TDM 例外と米国の fair use について *"very clear good-faith arguments"*（2026-09-10・`against.md` #132）| §6 | §6.5 が §6 を明示する理由を述べ、§6.2・§6.3 は留保をしないことで例外が働く条件を保つ（portfolio-2f の読み・`against.md` #132 の欄） | 「例外で足りるのに §6 は長い」と読まれる余地（B3） |
| GPL-3.0 §3 は WIPO 条約の回避の権利を行使したい人を差別すると arguably 読める（`license-review` 2018-11・SSPL の審査・portfolio-2f が T64 の材料として挙げた弱い文で、ドシエの節には置いていない）| §5.2(a)（T64）| T64 は GPL-3.0 §3 型を採ったが、ACD の §5.2(a) は Dedicator 自身の約束で、受領者や第三者に何も課さない —— 差別の問いは、他人に放棄を課す GPL の形にしか当たらない | なし |

**結果**: 条を変える指摘は 0 件。Villa 氏の基準は、起草の質（直した記録がある）、既存との差（B10）、事前の審査（B1）、採用（B2）に集まり、どれも register の側の問いで、1.4 の本文の語では閉じられない。

**アーカイブからの補い（2026-11-16）**: 上の表は、ドシエに引かれた文だけから書いていた。portfolio-2f がアーカイブの Villa 氏の通 331 通から論点の語に当たる 62 通を読んで 5 つの候補を挙げ、portfolio-1c が原文に当てた 3 つを rounds/ に置いた。

| 発言 | 当たる条 | 読み | 残る点 |
| :-- | :-- | :-- | :-- |
| *"MPL 2.0's defensive clause terminates copyright grants specifically because the patent grant is often such a toothless remedy."*、*"A major software company (and frequent patent litigator) told us that they'd never ship MPL 2 software because of that, which we counted as a win."*（`license-review` 2026-08-14・OpenMDW 1.1・`rounds/2026-08-license-review-openmdw-villa-mpl2-defensive-clause-observed.txt`）| §8.2・§10.4 | **不利な面**。MPL 2.0 の起草側が、防御の終了を著作権の許諾に掛けるのは意図した設計だと述べた。ACD は終了を持たない（§10.4）ので、Dedicator を訴えた人も全ての許可を保つ（`against.md` #46 の費用）。2 つ目の文の「勝ち」も、まず不利に効く —— 承認済みの起草者は特許の訴訟者を遠ざけたかったのに、ACD は誰も遠ざけない（portfolio-30 の読み・#46 の欄）。**逆側**: 逆側として使えるのは文の中の事実だけで、防御条項は大きな事業者の採用を実際に止めた。どちらが重いかは審査者の判断である。ACD は報復の条を持たず、1.4 の §8.2 はそれを方針でなく構造（§10.1 が条件を認めない）から導く —— *"the absence follows from the structure of this Dedication rather than from a policy preference expressed here"*。採用の阻害を避けるのは結果であって、本文が述べる理由ではない| 本文は変えない。§10.4 に終了を入れると、ACD の差の要（条件も終了も無い・§10）が消える。#46 の欄に足すかは register の担当（portfolio-30）へ |
| *"our existing licenses are maybe not as global as we'd like to pretend; feels like that has implications for future license approvals (and maybe CAL)"*（`license-discuss` 2019-07-02・`rounds/2019-07-license-discuss-how-global-villa-2019-observed.txt`）| §15.3・§3.3・§12 | **有利な面**。既存のライセンスが法域の違いを扱いきれていないことを、元理事が将来の承認の問いとして挙げた。ACD は法域ごとに放棄が効かない場合の備え（§3.3・§4）、人格権の不行使と同意（§12）、裁判地を選ばない規則（§15.3）を持つ | Villa 氏は含意が何であるべきかは分からないと書いている。支持ではなく、問いが在ることの記録 |
| *"The software industry has a completely different economic and technological infrastructure than it did when OSI was founded and when most of these licenses were written. … It is not healthy that the OSI's license selection (and possibly the OSD) have not followed suit."*（`license-review` 2018-06-19・`rounds/2018-06-license-review-submitter-notes-villa-industry-changed-observed.txt`）| §6・§9・B10 | **有利な面**。新しい事情（ACD では機械学習と機械による著作）に応じるライセンスの居場所を、元理事が求めた。ACD の前文は *"the three places where that assumption fails"* を名指す | 2018 年の文で、機械学習を名指していない。B10 の「既存で足りないか」に答えるのは量の側（`SUBMISSION-MATERIALS.md` §0d）で、この文は居場所が在りうることだけを示す |

**補いの結果**: 条を変える指摘は 0 件のまま。2f の残り 2 つ（BSD+Patent の相互参照の誤りの指摘・2018-10 の審査の場への評価）は原文に当てていない —— 前者は ACD の相互参照の errata の線（E-series）で既に機械が照合し（Check 471）、後者は B1 の逆側に使うかを慎重に決める必要があるので、register の担当に渡す。

**§15.7（T71）への追記（portfolio-30）**: 理由を作用の条に置くと Chestek 氏 2026-01-24 *"The unnumbered parts appear to be explanatory material, so I question whether they belong in the agreement at all."* と Piana 氏の線（説明は本文に入れない）に当たり、前文に置くと前文は自ら *"informative; not part of the operative terms"* と述べるので、`against.md` #124 の線では効力を持たない。どちらも同じ審査者の文に当たるので「理由をどこに置くか」に正解は無く、T71 は理由が範囲を狭める読みを許す害（E85）を除く方を選んだ。

### 16.2 Chestek 氏の基準を 1.4 草案に当てた（portfolio-30・条を変える指摘 0 件）

| 基準と出典 | 当たる条 | 扱い済みの場所 | 残る点 |
| :-- | :-- | :-- | :-- |
| *"Which is it, a dedication to the public domain or a license?"*（2025-10-16） | §3・§4・§4.4 | against #110・#112、B4 | OSI の判断に依る（B4 は class 10）。並存は必要だが疑われないとは言えない |
| 出力に触れると逆の含意が生じる（2025-12-15・ModelGo） | §1.8・§6・§8.4 | against #133 | G1 は出力を名指すことに依る。名指さなければ G1 を失う —— 取引 |
| 翻訳を正式な合意に入れない | §15.4・§16.4 の但し書き | against #261 | 残る |
| *"longer than the GPLv3"* | 全体 | against #6・#116、B3・B13 | 長さは残る（B13 が唯一の緩和） |
| *"That is the discrimination"*（当事者の類型化） | §5.2 | against #265 | 扱い済み |
| 足した許諾は混乱を足す（2019-08-05） | §8・§6 | against #299 | 扱い済み |
| 使われないことは欠点の証拠でありうる（2019-06-04） | — | against #289、B2 | 採用は 1 件のまま |
| データへの越境は *"when tied to software"* | §1.2 | against #237、B15 | OSI の判断に依る |
| 許諾を権利の列挙で定義しない（2026-04-18） | §4.2 | `reviewer-positions.md` §1.140 の「当たらないと確かめたもの」（§4.1 が全部を与え §4.2 は例示） | 当たらない |
| 番号の無い説明の部分は合意に入れない（2026-01-24） | 前文 | against #295 | 前文は *"informative; not part of the operative terms"* と述べる。条の中の理由の文は残る |
| 法の選択の条は必要でも望ましくもない（理事会の付言） | §15.3（置かない） | `REVIEWERS.md`、against-2 | 有利 |
| *"a license of this complexity needs to be drafted by a professional"*（2026-04-14） | 全体 | against-2、B1 | 残る（B1） |
| *"The license may last to perpetuity, so it needs to be really well written."* | 全体 | `reviewer-positions.md` | 残る（B1） |
| 本文の外の説明は本文を直せない（2026-09-01） | ドシエ全体 | against #124 | 答えは本文に置く |
| *"not for workshopping a license"*（2023-08-22） | 手続き | against-2、B1 | 確定した版で出す |
| *"Why does that matter to how the license operates?"* | §6.2・§6.3・§10.3 | `SUBMISSION-MATERIALS.md`、THIRD §15.6 | 扱い済み |
| *"Catch-22"*（実績が無いと承認しにくい） | — | B2 | 残る |
| 代理人による説明はうまくいかない（2020-02-28） | 手続き | B14 | **オーナー本人が答える必要がある** |
| *"Looks like AI slop"*（2025-08-14） | 手続き | against #292、B14 | **オーナー本人が答える必要がある**（開示を薄めない） |
| 特許の許諾を持たないライセンスは認めない（2026-02-20）・除いてよいのは新しい侵害だけ（2025-09-19） | §8.1・§8.4 | `SUBMISSION-MATERIALS.md` の表、`reviewer-positions.md` | 有利。§8.1 の組み合わせの侵害の読みは問 2 |
| 規則に反すると名指せない限り承認、という見方に反対（2019-07） | — | B10（2001 年の段の逆側） | 差の問いは残る |
| 権利を行使しない意図の明確な表明（2020-05-17・Unlicense） | §2.2・§2.5・§3 | B4 の行 | 有利 |
| 範囲の広いライセンスは「ソフトウェアだけのライセンス」として通読する（2023-08-15・CERN-OHL） | §6・§7・§8.4・§1.5・§11.4 | B15（2026-11-15・同じ通読を 1.4 に当てた） | 新しい欠陥は無い。「個人データ」の語は限界の文として本文に残る |
| サービスや個人情報はソフトウェアだけのライセンスにふさわしくない（2024-10-05・個人の立場） | §1.5・§11.4 | B15 | 同上（試作の種になりうる） |
| 営業秘密を許諾しないことは OSD に合わないと見られるだろう／公開されたコードに営業秘密がありうるか（2024-10-05） | §1.5（営業秘密を挙げない） | against #31 | 黙っている形が両方の読みに耐える、と読む |
| 第三者受益者は自分の利益に関わる範囲でだけ執行できる（2024-02-06） | §5.3・§8.6 | `QUESTIONS-FOR-COUNSEL.md` 問 5 | §5.3 が求めるのはその範囲だけ。契約でない約束に及ぶかは問いのまま |
| 支持が無い版の承認の見込みは低い（2020-12-28・委員長） | 手続き | B2 | 返信は 0 件のまま（B2・B14） |

**結果**: 条を変える指摘は 0 件。同氏の基準は、OSI の判断に依る項目（献呈と許諾の並存・データへの越境）、構造上残る項目（長さ・採用・法律家の関与・永続ゆえの起草の質）、オーナー本人にしかできない項目（代理人による説明への懸念・AI の提出）に集まる。後者 2 つは、提出の材料に「質問にはオーナー本人が答える」と書く根拠になる（B14）。

**集め方**: 上の 22 行はドシエに既に在る同氏の文から、下の 5 行はアーカイブの同氏の通 586 通のうち、60 語以上でドシエが 1 文も引いていなかった 35 通を読んで足した（2026-11-15・register への反映は PR 3232）。同氏の確かめ方（範囲の広いライセンスをソフトウェアだけのライセンスとして通読する・2023-08）を 1.4 草案に当てた結果は `ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B15 の節に在る。

**逆側**: 同氏の文はどれも他の提出についてのもので、ACD に当てたのは我々である。60 語に満たない通と、ドシエが一部を引いている通の残りの文は読んでいない。

### 16.3 Fontana 氏の基準を 1.4 草案に当てた（portfolio-50・条を変える指摘 0 件）

| 基準と出典 | 当たる条 | 扱い済みの場所 | 残る点 |
| :-- | :-- | :-- | :-- |
| *"I almost feel like you wrote three different licenses here and combined them into one."*、同じ通で、同じ問題を扱う部分どうしの *"subtle contradictions"* を懸念（2014-04-13） | §3・§4・§5 | `objection-map.md`（3 つの足場は意図した設計）、`ACD-1.4-CHANGELIST.md` の *"subtle contradictions"* の行、§4.4（献呈が無効でも許諾が立つ） | **最も当たりやすい点。** 足場どうしの食い違いは 1.4 の試作で探し続けたが、無いことは示せない（B3・B13） |
| *"We should not be quick to approve new licenses that seem to have problematically-drafted provisions even if the problems are not mentioned in the OSD (e.g., excessive vagueness, problems of comprehensibility, inconsistency across provisions)."*（2014-06-30） | 全体 | `SUBMISSION-MATERIALS.md` §1c の基準 3・4、試作 T34 以降と errata | 理解の費用（B3・B13）。判断は審査者のもの |
| 「名指せる規則に反しない限り承認」という主張の由来を、*"Artful license drafters were arguing that the OSI was compelled to approve any license with some sort of novel controversial provision if a clear conflict with a specific OSD provision could not be identified."* と説明（2026-08-28） | — | B10 | OSD 適合だけでは足りない、という同氏の線は残る（16.2 の 2019-07 の行と同じ） |
| *"the waste-of-time licenses are most often just the work of one developer acting in isolation"*（2013-05-30）、*"some credible showing that there's more than one person who supports the submission"*（2013-06-05） | 手続き | B2、`OSI-APPROVAL-PLAN.md`、窓口 `acd-use.yml` | **ACD はこの形に当たる。** 支持の表明は 0 件のまま（尋ねるのはオーナーの行為） |
| 有利: *"access to good legal advice will be unrealistic to many developers, and yet they seem to me to have as much a right to draft new purportedly open source licenses"*（2013-04-07）、*"it is hard to make the case that involvement of an attorney is a likely indicator of higher quality"* | 全体 | `reviewer-positions.md`（B1 の逆の記録） | 法律家の不在そのものを退ける理由にしない立場。ただし同じ人が起草の質は問う（上の 2014 の行） |
| 有利: *"There is a bit of a chicken/egg problem, as the absence of OSI approval may significantly deter projects *independent of the steward* from choosing the new license."*（2013-06-06）、*"OSI has approved thought-experiment licenses before (e.g. the SimPL) as well as licenses that were not used prior to OSI approval (e.g. the UPL)."*（2015-10-13・委員長として） | — | `reviewer-positions.md`、`review-readings-2.md` | 2015 年の文は、演習として作った文を `license-review` に出すことを退けた文脈に在る。ACD は「本物のライセンスか演習か」を問われうる（#161） |
| *"may have taken the wrong path very early on by developing a process that encouraged submission of novel, community-untested licenses"*（2020-01-04） | 手続き | `review-labels.md`、#161 | ACD は community-untested の典型（B2） |
| 機械翻訳を疑い *"run through a machine translator without subsequent human review"*（2019-05-27） | 全体（英語の質） | `review-outcomes.md`、B14 | 本文は AI が書いた英語で、英語の母語話者の法律家の目は通っていない（B1） |
| 有利: *"I'm not sure the possibility that any part of this license is AI-generated matters though."*（2026-03・AI-MIT の審査） | — | `review-responses-meta.md` Q36、`SUBMISSION-MATERIALS.md` | 問いは本文の著作権の有無についてで、AI 起草の提出を読むかどうかではない |
| *"I support granting legacy approval for the Unlicense. I wouldn't necessarily support approval for the regular (non-legacy) category, which arguably entails a more stringent form of review based on various criteria."*（2020-03-29） | 全体 | `against-2.md` | **ACD に legacy の道は無い。** Unlicense が通った基準より厳しい審査を受ける。先例への寄りかかりはこの差を越えない（#239） |
| Fedora で CC0 の代わりを問われ *"I have typically been recommending MIT No Attribution (SPDX: MIT-0)"*（2022-07-23・Fedora legal） | B10 | `against-2.md`、`ADOPTING.md`（MIT-0 を先に勧める） | 「MIT-0 で足りないか」は B10 の問いそのもの。差は特許・ML の明示・権利の存否を問わないこと |
| *"licenses that preclude any form of patent licensing or patent forbearance cannot be considered FOSS"*（Fedora がコードへの CC0 を外したとき（2022）に LWN が引いた同氏の文・原文の日付と場所は未確認）、CC0 について *"I was not troubled by the idea of approval of CC0 as such."*（2019-05）、CC0 への懸念は *"not about lack of explicit patent language (which is characteristic of many OSI-approved licenses)"* で、特許を明示に除く 1 文だった（2016-12-13） | §8.1・§8.4・§3 | `REVIEWERS.md` | 有利。§8 は許諾を明示し、反対が集まった CC0 の特許の除外を持たない |
| *"Either review for certification/approval the whole thing or not at all."*（2012-01-04・CC0） | §3・§4 | B4、`review-readings.md` | §4 だけを見てくれとは言えず、§3 の献呈を含む全体が審査される |
| UPL の許諾の広さを *"goes way beyond to the opposite extreme"* と読み、承認の前に許諾は改変前の Software と挙げた作品へ狭められた（2015） | §8.4 | `REVIEWERS.md`、`SUBMISSION-MATERIALS.md` | **§8.4 はモデルと出力へ伸びる**。1.4 草案は侵害する特徴が Work の内容から生じる範囲に限ったが、広さを問う読みは残る（B7・B10） |
| モデルのパラメータには承認済み以外のライセンスもありうるが *"that does not apply to code or model architecture materials"* | §1.3・§6 | `ACD-1.4-CHANGELIST.md`（§1.3 の重みの列挙を外した行）、B15 | 扱い済み。§1.3 は重みを名指さない |
| 有利（個人の見解）: オープンソースのライセンスは *"extensively used for non-software material in open source project repositories"* で *"completely appropriate"*（2026-04-06） | §1.3（data・audiovisual） | `ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B15、`against.md` #211 | 委員会の立場ではない |
| *"OSI does not approve, or up till now hasn't approved, SPDX identifiers as such, but rather the actual licenses they refer to"*（2024-08-09・個人の立場） | §16.1 の SPDX の行 | `ACD-OSI-BOTTLENECKS-EXTERNAL.md` | 扱い済み（識別子は SPDX が割り当てる） |
| 通知の年は *"templatize the date"*（2017） | §16.1 | `review-outcomes.md`、提出パケット §4b | 扱い済み（雛形の空欄は所在の 1 欄だけ） |
| clickwrap と OSD 10（2026-03-20・CNRI） | §2.3 | `SUBMISSION-MATERIALS.md` §1c の OSD 10 の行（`review-readings.md` §1.204） | 有利 |
| どの素材が covered work かを問う（`against.md` #134・アーカイブに逐語の 1 文は無く、要旨） | §1.3・§2.6・§16.2 | #134、T69（§2.6 の識別を §16.2 の形で果たす） | 扱い済み |
| **PUWL に**: *"I think the rationale you give for the license is fine, but I don't see the point of the license itself. As far as I can tell you are just combining a bunch of existing highly permissive permission grants, so OSI would have to end up examining each of them other than the Unlicense which has already been approved."*（2025-10-01・`license-discuss`） | 全体・§3・§4・§8 | B10、B4 | **同じ型の提出への直近の文で、ACD に最も近い。** ACD は既存の許諾を寄せ集めず自分の語で書いたが、「献呈と許諾と特許を 1 つにした、要点は何か」という問いの形はそのまま当たる。答えは B10 の 3 つの効果（`REVIEWERS.md` の "In one screen"）で、同氏がそれを足りると読むかは分からない |
| OpenMDW に: *"I don't think the OSI should be classifying this as an "AI license" and adopting some new, presumably looser, standard of approval for it based on that classification."*、コードにも使えるので *"plain old software license"* として働く（2026-08-28） | §1.3・§6 | B15（Chestek 氏の CERN-OHL の通読と同じ線） | ACD もコードに使えるので、ソフトウェアのライセンスとして通常の基準で読まれる。緩い基準を求めない、と先に述べておく材料 |
| OpenMDW の防御的な終了を OSD 5/6 と OSD 9 に当て、特許の主張で別の物の許諾まで終わる形に *"are there any limits to how *unrelated* A and B can be?"*（2026-08-15・08-29） | §10.4・§8.2 | `against.md` #174（終了の条が無い費用） | 有利。ACD は終了の条を持たないので、この 2 つの問いは立たない |
| *"this seems like it's probably intended to be a highly and uninterestingly permissive FOSS license and it just happens to be written in a highly odd and idiosyncratic style"*（2020-12-28・Open Innovation License） | 定義（§1.4 Dedicator・§1.7 Computational Use・Reservation） | B13、`REVIEWERS.md` の新しい語と承認済みの文の表（`review-readings.md` §1.198） | ACD の新しい語は定義を持つが、許容型の目的に対して語が独特だと読まれる余地は残る。**試作の種（1c へ）**: 承認済みの語で言える定義語を数え、置き換えられるものがあるか |
| *"Far better than focusing on so-called "crayon" and thought-experiment licenses, which until relatively recently characterized a lot of the submissions to license-review."*（2020-02-25）、GPLv3 の追加条項の提出に *"what you've submitted isn't in actual use anywhere"*（2019-03-17） | 手続き | B2、`against.md` #158（crayon） | 実使用は提出者の 1 件だけ（B2） |
| 有利: *"I can imagine ways in which we could have made these points ever clearer (at the cost of making the license twice or more as long and more complex)"*（2007-11-13・GPLv3 について） | 全体 | B3 | 明確さと長さの取引を起草者として述べた文。ACD は明確さの側を選んだ（B3 の説明と同じ）が、同氏がその取引を ACD で是とするかは別 |

**結果**: 条を変える指摘は 0 件。同氏の基準は、起草の構造（3 つの足場の食い違い・起草の質）、手続き（単独の起草者・community-untested・legacy でない厳しい審査）、既存で足りるか（MIT-0・UPL の広さ）に集まる。本文の語で閉じられるものは 1.4 までに閉じてあり、残るのは B2・B3・B10・B13 の側の問いである。審査で最初に来やすいのは、PUWL への 2025 年の文（既存の許諾を束ねただけなら要点は何か）と、1 行目（3 つのライセンスを 1 つにした）と、§8.4 の広さ（UPL）の 3 つと読む。試作の種は 1 つ（独特な定義語を承認済みの語へ置き換えられるか・1c へ）。

**集め方**: 前の 20 行は、ドシエに既に引かれている同氏の文を、帰属が同氏と確かめられるものだけ集めた。後の 6 行は、portfolio-30 の道具（差出人で通を集め、引用の行を外した本人の文がドシエに 70 字の頭で 1 つも一致しない通を出す）でアーカイブの同氏の通 558 通から 60 語以上の 220 通を出し、ACD に関わる語（公有・献呈・CC0・特許・増殖・起草・承認・モデルなど）を多く含む上位 22 通を読んで足した（2026-11-16）。ドシエだけから集めると、ドシエが扱った文しか当たらず「0 件」が作りから決まる（30 の指摘）。

**逆側**: 同氏の文はどれも他の提出についてのもので、ACD に当てたのは我々である。2015〜2020 年の文の一部は委員長や理事としての文で、2024 年以後の一部は「OSI を代表しない」と断った個人の文で、重みが違う。220 通のうち読んだのは 22 通で、残りの 198 通は語の数の少ない順に読んでいない。

### 16.4 Perens 氏の基準を 1.4 草案に当てた（portfolio-2f・条を変える指摘 0 件）

Perens 氏の文は 1999〜2024 年にわたり、ドシエの中で最も多く引かれている審査者の 1 人である。決める側の役に無い時期の文も多いが、OSD の起草者として審査の場で重く読まれる。下の表は、その文だけを根拠に、1.4 草案の頭から終わりまでを Perens 氏の目で通読した結果である。

**集め方（2026-11-16 に足した・portfolio-30 の当て直しを受けて）**: 最初はドシエに在る Perens 氏の文だけから集めた。ドシエに在る文だけで当てると、ドシエが既に扱った基準しか出てこないので、アーカイブの写しの全月で Perens 氏の通 1,139 通を拾い、ACD の論点の語（公有・献呈・特許の許諾・法律家・増殖・重複・crayon など）に当たる 308 通のうち、ドシエに 40 字の窓で見つからない 137 通を読んだ。新しく行に足したのは 2 つ（下の表の最後の 2 行）で、どちらも条を変える指摘ではなかった。語に当たらない通は読んでいない。

| 基準と出典 | 当たる条 | 扱い済みの場所 | 残る点 |
| :-- | :-- | :-- | :-- |
| 使うだけの人には *"as close to *no legal load* as possible"*（2017-10・`review-readings-2.md` §1.229）、誰でも何の目的でも *"should not have to hire a lawyer just to run it"*（2018-12・`review-readings-2.md` §1.237） | §2.3・§10.1・§10.2 | §2.3 は受諾を要さず、§10.1 は何の条件も課さない。使う人に法的な負担は無い | 無し。むしろ有利な面（配る人・改変する人にも負担が無い） |
| *"Extension of copyright is bad for Open Source, even if it helps us enforce our licenses more effectively."*（2019-01・`review-readings-2.md` §1.250） | §1.3・§6.1・§6.4・§7・§2.7 | §2.7 は *"reaches only rights the Dedicator holds"*。§6.1 は Covered Rights の範囲に限る。§6.4 はモデルや出力について *"Whether a right subsists in any such thing is not decided here and does not need to be."* と書き、権利の存在を主張しない。§1.3 はデータや視聴覚の素材を Work に数えるが、そこに権利があるとは述べない | 無し。§7（データベースの sui generis の権利）は既に在る法の権利を手放す条で、拡張ではない |
| *"The language must continue the license once the web site goes away, as they so often do."*（2010-10・netX・`review-readings-2.md` §1.236） | §16.1・§16.2 | §16.2 は *"the terms apply in full whether or not a copy of this text accompanies the work"*。§16.1 の `<location of this file>` が消えても条件は効く | 無し |
| *"I submit that Mozilla would be doing the community a service if they were to make their license invariant."*（2010-11・`review-readings-2.md` §1.235） | §16.4・§16.5 | §16.4 は名と識別子の下で本文を変えさせず、各名と識別子が 1 つの固定した本文を指し続ける | 版の数そのもの（1.0〜1.4）は不変性とは別に読まれうる（`against-2.md` #320） |
| *"Requiring an explicit patent grant in new licenses /might/ be over-reaching. Being sensitive about disclaimers of patent grants and their potential to harm developers is probably appropriate."*（2012-02・CC0 の審査・`review-readings.md` §1.164） | §8.1・§8.4 | §8 は特許を除外せず、明示に許諾する。Perens 氏が害を見た「除外」の形を持たない | 明示の許諾は要件ではない、という同じ文の前半は、§8 が承認に必要だとは言えないことを示す（B10 の G1 の重さの問いで、本文の問いではない） |
| *"licenses that are duplicative of other licenses in their effect should not be accepted any longer, unless it's to meet new developments in case law or solve an obvious legal deficit."*（2018-06・`review-readings-2.md` §1.224）、*"find an already-approved license to use"*（2010・`review-readings-2.md` §1.236）、Blue Oak について *"its main effect was to increase the number of OSI-approved licenses and the combinatorial problem"*（2024・`review-readings.md` §1.217） | 全体（B10） | B10 の G1（承認済みに無い効果）と、§1.224 の 2 つの例外（法の新しい展開＝§6、明白な欠陥＝CC0 の特許の除外と §8） | B10 は register の問いで、本文の語では閉じられない |
| *"A license is a sort of program designed to be executed by the courts. If you have not made use of an attorney in drafting your license, you are very unlikely to understand how the courts would actually execute your license."*（2018-06・`review-readings-2.md` §1.224）、*"It isn't the least bit difficult to diagnose when no lawyer was involved in drafting a license."*（2013-03・`review-readings-2.md` §1.234）、短い公有の文は *"crayon license"*（2012-05・`review-readings-2.md` §1.245） | 全体（B1） | 入口が「法律家が読んでいない」ことを 5 か所で先に言い切る（portfolio-50 の確認）。`QUESTIONS-FOR-COUNSEL.md` が法律家への問いを条ごとに置く | B1 は残る。Perens 氏の目では、本文から法律家の不在が「すぐ分かる」所がまず突かれる |
| 指摘に本文でなく FAQ で答える応答への評価は *"meh"*（2018-05・ESA-PL・`review-readings-2.md` §1.248） | 「本文を変えない」と判断した条（§2.6・§16.4 など） | 本文を変えない判断は、その読みを本文のどの語が持つかを引いて理由にしている（この文書の 15.8 節） | 審査で同じ形を取るとき、答えを本文の語で示すこと（手順の問い） |
| *"I don't think anyone has bothered to focus on smaller issues of the license after seeing that the bigger ones would keep it from passing."*（2008-05・IWL・`review-readings-2.md` §1.238） | 全体 | `REVISION-PROTOCOL.md` の 3.8 節（細部の指摘の 2 波目の見込み・portfolio-30） | 最初の指摘が少なくても、細部の指摘は後から来る |
| 標準の団体が API の実装を禁じうる条項は承認しないよう強く勧める（2019-01・`review-readings-2.md` §1.249） | 無し | ACD は使用や実装に条件を置かない（§10.1） | 無し |
| CC0 に特許と商標の許諾を足した「True Zero License」（2024）に、特許の許諾は *"necessarily practiced in the work as issued by the grantor"* に限るべきだとし、*"It is probably going to be parsed in court as a dedication to the public domain rather than a contract. There is thus some question of how binding the terms could be on the grantor."*（2024-04-06・`ACD-1.0.review-corpus.md` §1.79） | §8.1・§8.4・§3〜§5・§2.5 | §8.1 は *"caused by subject matter contained in the Work as made available by the Dedicator"* で同じ種類の限定を持つ（§8.4 はモデルのために意図して外す・#305）。拘束の疑いには、献呈（§3）・許諾（§4・§8）・不行使の約束（§5）の 3 つの足場と §2.5 の禁反言で答える（review-corpus §1.79 の読み） | ACD の型に最も近い先例で、同じ人の目では「献呈の中の約束は許諾者を拘束するか」がまず突かれる。答えが効くかは法律家への問い（`QUESTIONS-FOR-COUNSEL.md` の問 (i)）のまま |
| *"As far as I am aware, where the previous OSI board has worst "screwed up" has been in accepting crayon licenses that can be harmful to the community"*、*"The OSD would not, on its own, have stopped this regardless of the literal-ness of the reading."*（2018-12-13・`rounds/2018-12-license-discuss-decision-process-perens-crayon-ofl-observed.txt`） | 全体（B1） | 入口が法律家の不在を先に言い切る | Perens 氏にとって法律家の手を経ない文書は、OSD の適合と別に承認の失敗の種類で、B1 は OSD の逐条では答えられない |

**結果**: 条を変える指摘は 0 件。Perens 氏の目で突かれるのは、本文の語ではなく、B1（法律家の不在）と B10（既存と重複しないか）と B2（採用）で、どれも register の側の問いである。本文に向く基準（使う人の負担、著作権の拡張、サイトに依らない効力、本文の不変、特許の除外）は、1.4 草案がそれぞれ §2.3・§10.1、§2.7・§6.4、§16.2、§16.4、§8 で既に満たしている。

**逆側**: 「満たしている」は Perens 氏の過去の文に当てた結果で、Perens 氏が 1.4 草案を実際に読めば別の点を突きうる（模擬の限界）。とくに長さ（1.4 草案は CC0 の約 5.6 倍・`review-readings-2.md` §1.245）は、Perens 氏の文には直接の基準が無いが、*"crayon license"* の逆の極として「長すぎて読めない」と読まれる余地を残す（B3・B13）。

### 16.5 Smith 氏の基準を 1.4 草案に当てた（portfolio-50・9b の受け持ちを引き継いだ・条を変える指摘 0 件）

| 基準と出典 | 当たる条 | 扱い済みの場所 | 残る点 |
| :-- | :-- | :-- | :-- |
| 提出の手順の問いに全部答える: *"you need to answer all the questions set forth in the process for approval"*（2026-03-17）、Blue Oak に Rationale・Distinguish・Legal review・Proliferation category を挙げ *"I think any review of this license should be suspended at least until those questions are answered."*（2022-03-20）、ADVPL に *"Describe what gap not filled by currently existing licenses that the new license will fill."* を名指し（2024-09-05） | 手続き | `ACD-1.0.submission.md`、`SUBMISSION-MATERIALS.md` §1 | 答えは用意してある。Legal review の答えは「無い」で、それは B1 として残る |
| 法律家: *"this license really needs to go through a legal review before submission/resubmission."*（2025-10-26）、*"trying to do this on your own isn't likely to result in something functional"*。有利な側: *"Drafting or review by a lawyer is no guarantee of quality"*（2019-03-15）、審査した法律家は匿名でなく名を出すべき（2020-08-25・Vaccine License の「専門家が書いたが審査は公開できない」に） | 全体 | B1、`against-2.md`、`REVIEWERS.md` | **残る（B1）**。ACD は「法律家は読んでいない」と書くので、匿名の審査を主張する形には当たらない |
| 献呈と許諾の同居: *"I sort of feel like it is not necessarily fatal to have the two concepts together in a single "license," but CC-0 makes it clearer that it operates in the way above -- complete dedication to public without restriction in places where that can be done, otherwise extremely permissive license without restrictions"*、法域で献呈と copyleft が入れ替わる形は *"likely violates OSD 5"*（2024-12-18・PBZC）、*"I think everyone acknowledges that a pure public domain dedication without a backstop is problematic"*（2020-05-15） | §3・§4・§4.4・§12.2 | B4、`review-precedents.md` §1.46 | 有利。§4 の許諾は §3 と独立に、どの法域でも同じ形で立つ（§4.4）ので、法域で条件が入れ替わる形に当たらない。CC0 との差は、許諾が献呈の失敗を条件にしないこと（*"not as a fallback"*） |
| **PUWL に**: *"it seems to be a concatenation of a bunch of different highly-permissive ("-0") licenses or other public domain dedications, without any indication of whether all, or the one the licensee chooses, applies."*（2025-10-01） | §3・§4・§5・§4.4 | 1.4 草案の前文（3 つは互いの fallback でなく、1 つだけに頼ってよい）と §4.4 | 有利。どれが働くかを本文が述べる。作用の条では §4.4（§4 は §3 と独立）と §5.3 の末尾（*"Sections 3 and 4 operate in their favour independently of this Section."*）が述べ、3 つ全部が互いの fallback でないことを 1 か所で述べるのは *informative* の前文である |
| CC0 の献呈の語を範に: *"the wording they use in CC0 is much more comprehensive in the language it uses (in Sec. 2)"*、CC0 は *"perhaps the best example of a comprehensive effort to dedicate content to the public domain"*（2025-12-04） | §3 | `ACD-1.2-CHANGELIST.md` | 扱い済み |
| 撤回不能: *"Making a license irrevocable is fine, and many OSI licenses do that (for example, Apache 2.0)."* | §2.2 | `AS-OF.md` | 有利 |
| 特許: 権利を明示に外すライセンスは *"can result in them being non-open"*（2022-12-14）、CC0 の特許の除外は OSD 7 に反しうる（2025-12・OSI ブログ）、BSD+Patent と UPL の特許の許諾の射程を、何を基準に測るかで比べた（2017-03-30） | §8.1・§8.4 | `REVIEWERS.md`、`SUBMISSION-MATERIALS.md` §1c の OSD 7 の行 | 有利（特許を明示に許す）。**ただし同氏は射程の測り方を条ごとに比べる人で、§8.4 の「Work の内容から生じる」という因果の基準は、Apache 型（寄与とその組み合わせ）とも UPL 型（挙げた作品）とも違う新しい測り方である**（B7） |
| *"I think that precedent shouldn't be used to allow for incompletely written licenses"*（2026-05-14）、承認済みの OSD に反するライセンスが *"can be used as precedent for new license submitters as to why their non-OSD compliant licenses must also be approved"*（2019-06-03） | §4.2・全体 | `AS-OF.md`、#239 | ACD は許諾の行為を列挙する。先例への寄りかかりは同氏の線で限られる（#239） |
| *"preambles can be construed as not part of the license"*（2025-10-26） | 前文 | `reviewer-positions.md`、#124 | 前文は自ら *informative* と述べる。上の PUWL の行のとおり、3 つの足場の関係を 1 か所で述べるのは前文で、作用の条は §4.4 と §5.3 の末尾に分けて述べる。**1c の補い（2026-11-16）**: 作用の条にも 1 か所ある —— §2.4 *"Sections 3, 4, 5, and 6 are independent of one another … none is conditioned on another being effective or on another's failure. Where more than one operates, they operate cumulatively"*。前文が契約の一部と読まれなくても、足場の関係は §2.4 が作用の条として持つ。§4.4 と §5.3 の末尾はその個別の確認である |
| 本文の変更を禁じる文は OSD 3 に反する（2025-08-14） | §16.4 | #101、#179 | §16.4 は本文テキストの名前の制約で Work の条件ではない（§16.6）。Steward の例外に同氏の広い読みが届く点は論破していない（#179） |
| 起草の手入れ: MGB に、閉じていない引用符・括弧、定義語と本文の語の食い違い（定義は *Model Materials*、本文は *Models*）を挙げた（2025-09-22） | 全体 | —（**この節で測った**） | **1.4 草案の第 1 条から END OF TERMS までで、定義語の表記ゆれは 0**（2026-11-16・portfolio-50 が語ごとに大小文字を無視して数えた）。小文字の *machine-generated material*・*reservation*・*dedication* は前文だけ、小文字の *work* は定義の前の一般の語（*a work*・*any work*）だけだった。同じ範囲で括弧は開き 25・閉じ 25、二重引用符は 42 で偶数（数えただけで、対応の位置は見ていない・これを見る Check は無い） |
| 許諾される物の定義は汎用でよい（GPLv3 の *"any copyrightable work"*・Apache-2.0 の *"the work of authorship"* と並べて・2026-08-29・OpenMDW） | §1.3 | B15 | 有利。§1.3 も適用された素材という汎用の形 |
| source に触れない提出は OSD 2 に反しうる（2020-10-16・Anti-IP） | §4.2 | `SUBMISSION-MATERIALS.md` §1c の OSD 2 の行 | 有利（§4.2 は source の形の頒布を許す） |
| 公有の素材にも免責は効く: *"I believe that to be an effective waiver of liability, despite the fact that there is not copyright rights being conveyed."*（2016-08-16） | §13・§14 | `REVIEWERS.md` | 有利 |
| 既存と重なるものを「より使われるライセンスと重複する」の分類に置く提案（2020-03-05・PHP） | — | B10 | 承認されても分類で重複と読まれうる（B10） |
| pre-review の場: *"if you want people to give comments before you submit for approval, this is the correct mailing list"*（2024-09-30） | 手続き | #117 | 有利（`license-discuss` を先に使った） |

**結果**: 条を変える指摘は 0 件。同氏の基準は、手続き（問いに全部答える・法律家）、構造（献呈と許諾の同居・どれが働くかの明示）、特許の射程の測り方、起草の手入れに集まる。献呈と許諾の同居は §4.4 で、汎用の定義・source・免責・撤回不能は本文で有利に答えている。起草の手入れは、この節で定義語の表記ゆれを数えて 0 と確かめた。**審査で来やすいのは、§8.4 の射程の測り方（新しい因果の基準）**と読む。3 つの足場の関係を 1 か所で述べるのが前文だけであることは、前文を合意の外と読む同氏の文（2025-10-26）と組み合わさりうるが、作用の条（§4.4・§5.3 の末尾）が分けて述べているので、条を変える指摘にはしない。

**集め方**: ドシエに引かれている同氏の文に加え、portfolio-30 の道具でアーカイブの同氏の通 458 通から、ドシエが 1 文も引いていない 60 語以上の 99 通を出し、ACD に関わる語の多い上位 16 通を読んだ（2026-11-16）。PBZC（2024-12-18）・PUWL（2025-10-01）・特許の射程（2017-03-30）・起草の手入れ（2025-09-22）・汎用の定義（2026-08-29）・Anti-IP（2020-10-16）・pre-review の重複分類（2020-03-05）はこちらから足した。

**逆側**: 同氏の文はどれも他の提出についてのもので、ACD に当てたのは我々である。99 通のうち読んだのは 16 通。同氏は委員会の報告者として書く通（*"on behalf of the Licensing Committee"*）と個人として書く通があり、上の表は区別していない。

## 17. SECOND に先に登録されたまま答えの無かった反例への答え（2026-11-16〜）

`list_open_items.py` が、`ACD-1.4-SECOND-CLARITY-TRIAL.md` の「先に登録する反例（bb へ）」のうち「**反例の結果**」の段を持たないものを 8 件出した。SECOND は 2026-11-16 に閉じたので、答えはここに書き、SECOND の節の番号で名指す。分担は 50 が 4 件（§14.15・§14.20・§14.22・§14.23）、30 が 4 件。当てた本文は、2026-11-16 の main の 1.4 草案（T76 の後）。

### 17.1 SECOND §14.15（T34・§9.2）への反例（portfolio-50）

**反例の結果**（SECOND §14.15 の先に登録する反例）: **当たらない（4 点とも）。** いまの §9.2 は第 3 文の列挙を持たず、*"Where a right that this Dedication reaches subsists, or is later held to subsist, this Dedication applies to it."* と述べる。
(a) *"a right that this Dedication reaches"* が受領者に「reach するか」の判定を求める読みは、§9.3 の *"No permission granted here depends on that question"* に当たって立たない —— §9.2 の第 3 文は Dedicator の側の適用を述べ、受領者の行為を条件にしない。
(b) 旧文の *"in full"* はもう無い。「適用する」は §12 を含む各条をその語のとおりに適用することで、§12 の *"to the extent stated"* の限定を外す読みは立たない。
(c) 後に権利が生じた部分には、文書全体（§2.2 の撤回不能を含む）が適用される。旧文が §2 を挙げなかった欠けは、列挙を外したことで消えた。
(d) §14.15 の (A)（列挙が §5 を権利のある場合の側に置く）は、列挙が無いので立たない。§9.2 の第 2 文 *"adds nothing … as to that right and takes nothing away"* は「その権利について」に限られ、§5.2(b) の約束（Dedicator 自身の行為）を消さない。(B)（免責が権利の無い部分に及ばない）は、§13.2 の *"DOES NOT WARRANT THAT ANY RIGHT SUBSISTS IN THE WORK"* と、免責が受領者の自由を「奪う」ものでないことから立たない。
**逆側**: (d) の (B) は弱い読みとして残りうる —— 権利の無い部分について免責がどの法に依って立つかは、法律家への問い 9（§14.1）の側にある。

### 17.2 SECOND §14.20（T46・§16.4 の大小文字）への反例（portfolio-50）

**反例の結果**（SECOND §14.20 の先に登録する反例）: **当たらない（3 点とも）。** いまの §16.4 は *"under any identifier that contains "ACD-", regardless of case, followed by a digit"*。
(a) *regardless of case* は読点で挟まれて *"ACD-"* に掛かり、数字には大小が無いので、数字の書式まで広げる読みは意味を持たない。
(b) 翻訳の文は *"may be distributed under the name and the identifier if it is identified as a translation"* で、照合の大小とは別の許しなので食い違わない。
(c) 縛られるのは「この文書の改変した本文」を配ることだけで（§16.4 の *"A modified text may not be distributed under …"*）、*ACD-* を名に含む別のライセンスやプロジェクトの本文は、ACD の本文の改変でない限り縛られない。§16.6 は *"They are not terms of the Work, they bind no one in respect of the Work"* と述べる。
**逆側**: 「改変した本文」かどうかの境（ACD を下敷きに大きく書き換えた別のライセンス）は語で決まらず、名に *ACD-* と数字を含めたい書き手には、その境が費用になる。

### 17.3 SECOND §14.22（T48〜T50）への反例（portfolio-50）

**反例の結果**（SECOND §14.22 の先に登録する反例）: **(a)(b) は当たらない。(c) は書き方の問いで、試作の種にしない。**
(a) §5 の末尾の外しは *"the use of a service through which the Dedicator runs the Work for others without providing a copy of the Work"* に限られる。写しを受け取った人への約束は外れない。同じサービスが写しの取得も許すなら、それは写しを提供しているので外しの外である。
(b) *a former Steward* は §16.5 の定義（最初に公表した者か、その役を譲り受けた者）の過去の保有者で、役を持たずに版を出した者（違反者を含む）は Steward でなかったので含まれない。
(c) 2 つの *regardless of case* を 1 つにまとめると、どちらの句に掛かるかの読みが新しく生じる。いまの形（それぞれの句の直後）は長いが、掛かり先が 1 つに決まる。
**逆側**: (a) で、サービスの利用規約が写しの取得の条件を兼ねる形（ダウンロードにログインと規約への同意を求める）は、写しを提供しているので §5.2(b) の内に在る —— Dedicator がこの形を取れば約束に反する。外しの境を Dedicator に読み違えられる余地はある。

### 17.4 SECOND §14.23（T51・§15.1 を許可に絞る）への反例（portfolio-50）

**反例の結果**（SECOND §14.23 の先に登録する反例）: **(a)(b) は当たらない。(c) は 1 つ残る。** いまの §15.1 は *"This Dedication, in respect of the Work, is to be construed so as to give the widest permission and the least obligation upon You that its words allow, and so that, where a provision is capable of more than one reading, the reading that grants more to You prevails."*
(a) §5 の約束は *"in respect of the Work"*（§5.2 の柱書き）で、約束を広く読むことは受領者に「より多くを与える」読みなので、§15.1 は §5 の範囲の読みに効く。§2.4 も *"Section 15.1 governs their construction"* と述べる。
(b) §2.4 の 3 つの足場の読みは §2.4 の最後の文がそのまま §15.1 に結ぶので、影響しない。
(c) **残る点**: *"grants more to You"* の *grants* は、免責（§13・§14）の読みが分かれたときに、受領者に有利な（免責を狭くする）読みまで含むかを決めない。許可と義務の側では向きが 1 つに決まるが、免責は Dedicator を守る条で、どちらが「より多くを与える」かが語から決まらない。E20 と E75 が §15.1 の 2 つの文の射程を *in respect of the Work* に置いた後も、この点は扱っていない。
**逆側**: 免責の読みを受領者に有利へ倒す規則を本文に足すと、承認済みのライセンスが持つ免責の型（`SUBMISSION-MATERIALS.md` §1c の基準 2 の行・#265）から外れ、かえって審査者に「免責が効かないかもしれない」と読ませる。試作の種にするかは 1c が決める（50 は「変えない」を勧める）。

**1c の判断（2026-11-16・変えない）**: (c) の空白は §15.6（1.0 では §15.3）が意図して残している。§15.6 は *"No rule of construction that resolves ambiguity against the drafter applies to this Dedication"* と述べ、起草者に不利に解く既定の規則（免責の読みを受領者に有利へ倒す普通の道）を外す。§15.1 の *"grants more to You"* は許可と義務の向きを決め、免責（§13・§14）の向きは決めない —— 2 つを合わせると、免責の読みが分かれたときは、どちらへも倒す規則が無く、裁判所の通常の解釈に委ねられる。これは承認済みのライセンスの免責と同じ状態で（ほとんどは解釈の規則を持たない）、50 の逆側の理由（受領者に有利へ倒す規則を足すと、免責が効かないと読ませる）とも合う。**逆側**: §15.6 が起草者に不利な解釈を外すことは、免責について Dedicator に有利に働く。受領者から見れば、普通のライセンスなら使える既定の規則が 1 つ無い。§15.6 の目的は許可を狭く読ませないことで（第 2 の句）、第 1 の句が免責にも及ぶのは副作用として記録する。


### 17.5 SECOND §10.1（T5・§16.1 のタグだけの適用）への反例（portfolio-30）

**反例の結果**（SECOND §10.1 の先に登録する反例 (a)〜(e)）: **4 点は当たらない。(a) に残る点が 1 つ。** (b) 依存物の同梱ディレクトリのタグ: §16.2 は *"A notice a Dedicator places"* に限り、第三者が置いたタグは Dedicator の通知ではない。§2.7 が Dedicator の持つ権利に閉じるので、同梱物には及ばない。(c) 従業員が雇用主のコードにタグを付ける: §1.4 の Dedicator の定義は、適用する者を、その者が持つか持ちうる Covered Rights の範囲に限るので、権利を持たない者の適用は雇用主の権利に及ばない（代理の権限の問いは本文の外）。(d) `docs/` だけのタグ: §16.2 の *"applies this Dedication to the material it identifies ... or, where it identifies none, to the material it accompanies"* が範囲を決める。(e) 語順: §16.1 の *"in a form Section 16.2 names or in substantially the following form"* は 2 つを並べた選択で、通知文が推奨にすぎないとは読めない。**残る点 (a)**: README が比較のために「ACD-1.4」を挙げるだけでも、§16.2 の *"a reference to this Dedication by name and version"* の形には当たる。§16.1 の適用は *"place a notice with the Work"* で、*notice* は定義されていないので、比較の言及を「通知」と読む余地は語の上では残る。条件を告げない言及を通知と読むのは不自然で、実害は小さいと読む。試作にするなら、§16.2 の第 1 文の頭を「A notice that a Dedicator places to apply this Dedication」に寄せる形が候補（+5 語前後）。B3 の費用と比べて、30 は試作にしない側に傾く。

**1c の判断（2026-11-16・変えない）**: 試作の形は §16.2 第 2 文 *"A notice a Dedicator places applies this Dedication to the material it identifies"* を *"A notice a Dedicator places to apply this Dedication applies it to the material it identifies"* にするもので、+3 語になる。採らない理由は語数より強いものが 1 つある —— *to apply* は適用の**意図**を通知の要件にし、受け手（と自動の判定）は、識別子が在ることに加えて、置いた人の意図を判断しなければならなくなる。§6.5 が述べる「自動の仕組みが判定できない許可は、学ばれるための作品にとって許可ではない」に逆らう向きで、SPDX のタグを機械が読む場面で、意図の争いの余地を新しく作る。比較の言及の側は、§16.1 が *"To apply this Dedication, place a notice with the Work"* と適用の行為を定め、§16.2 第 1 文が *"a work to which a Dedicator has applied this Dedication"* を前提にするので、条件を告げない言及を通知と読むのは不自然な読みのままである（30 の読み）。**逆側**: 比較の言及が通知と読まれた場合の害は、Dedicator が意図しない作品へ撤回不能の献呈が及ぶことで、起きれば重い（E61 と同じ向き）。そのため、`ADOPTING.md` の側で「比較のために ACD を名指すときは、識別子（`ACD-1.4`）も名前と版の組も §16.2 が十分な通知とする形なので避け、版を付けずに名前で書くか、同じ文でその作品に適用していないと述べる」と案内する方が当たる面が狭い —— 案内の文は入口の担当（portfolio-50）へ渡す。

### 17.6 SECOND §10.2（T6・§6.4 の "(Section 9)" を外す）への反例（portfolio-30）

**反例の結果**: **当たらない（2 点とも）。** (a) いまの §6.4 は *"Whether a right subsists in any such thing is not decided here and does not need to be."* と自分の文で決めないことを述べ、§9 を根拠に要さない。§9.2 は別に *"makes no representation that any right subsists in any part of the Work"* と述べる。(b) 出力が Dedicator の Work に取り込まれた場合は、§9.1（Work は Machine-Generated Material を含みうる）と §9.2・§9.3 が受け持ち、§6.4 の括弧が無くても案内は §9 の見出しから届く。

### 17.7 SECOND §10.3（T7・§15.1 の "upon You"）への反例（portfolio-30）

**反例の結果**: **当たらない（2 点とも）。** (a) §15.1 の第 2 の句 *"the reading that grants more to You prevails"* は *"upon You"* と独立に働き、受け手に多く与える読みは Dedicator の側を重くする向きでも勝つ。*"upon You"* は第 1 の句の「義務を最小に」の宛先を受け手に定めるだけで、第 2 の句の射程を狭めない（`against.md` #124 の 2026-11-16 の段が、§15.1 は Dedicator の側を縛る向きだと書いたのと合う）。(b) §16.4 は文書についての制約で、§15.1 は *"This Dedication, in respect of the Work, is to be construed"* と、Work についての解釈に限られる（E20）ので当たらない。

### 17.8 SECOND §14.24（T52・§16.2 の狭い通知と §6.2 の留保）への反例（portfolio-30）

**反例の結果**: **当たらない（3 点とも）。** いまの §16.2 は *"a notice that is only a Reservation assigns nothing to other terms (Section 6.2)"* と書く。(a) 撤回不能の向き: TDM だけを外したい Dedicator は、opt-out の通知では外せず、素材を別の条件へ明示に割り当てる必要がある。これは §6.2 の *"expressly declines to make one"* を Dedicator が自分で適用した結果で、本文から読める。E61 が避けた向き（Dedicator の知らないうちに献呈が広がる）とは違い、Dedicator が §6.2 を読めば分かる。(b) 「TDM と再配布を禁じる」のような通知は *only* に当たらず、狭い通知として素材を Work の外に置く。それは Dedicator が献呈の範囲を選ぶことで、受け手から何かを取る抜け道ではない。外された素材は献呈されておらず、通知がそう告げている。(c) 第三者が置いた留保は §16.2 の *"A notice a Dedicator places"* に当たらないので狭い通知にならず、§6.3 が *"Where the Reservation is another rightsholder's ... the Dedicator has no power to withdraw it"* と扱う。

## 18. 法的解釈の不確実性を減らす —— 各条が頼る法の命題を、米・英・独・仏・日に当てる（2026-11-16〜・オーナーの依頼）

**依頼**: オーナー 2026-11-16「ACD-1.4-DRAFT.txt の法的解釈の不確実性を「５人」で減らし続けてください」。**方法**（5 人で決めた）: 各条について (a) 頼っている法の命題を書き出し、(b) 米・英・独・仏・日で真か・争いうるか・偽かを当て、(c) ① どこでも真 → 記録だけ、② 語を変えれば法域に依らなくできる → 試作の種（1c へ・【反例待ち】）、③ 語では消せない → 法律家への問いか `ACD-1.0.jurisdictions.md` の「確立していないこと」へ。一次の法源は 2f（米国・EU）と 30（独・英・仏・日）が取り、取れないものは「我々の読み」と書く。**小節**: 18.1 = §1〜§4（1c）、18.2 = §5〜§7（30）、18.3 = §8〜§10（50）、18.4 = §11〜§13（2f）、18.5 = §14〜§16（9b）。

### 18.1 §1〜§4（portfolio-1c・main の 1.4 草案）

| 条 | 頼っている法の命題 | 当て | 分け |
| :-- | :-- | :-- | :-- |
| §1.4 | 複数の Dedicator の行為は各自に別々に働く（*"operates severally"*）| Dedicator 自身の意思表示の範囲の言明で、法の命題を言わない | ① |
| §1.6 | 自動の仕組みが行使した許しは、その背後の人と運用者に与えられる | 許諾の宛先を Dedicator が決める文で、自動の仕組みが法的な主体になれるかは問わない形 | ① |
| §2.2 第 1 文 | *"This Dedication is irrevocable."* —— 献呈は撤回できない | ドイツ UrhG 42 条（確信の変更による撤回）・フランス CPI L121-4（撤回・悔悟の権利）、米国 17 U.S.C. §203 の終了権は法定で、事前に放棄できない。さらに無償の付与が贈与と読まれれば、ドイツ BGB 530 条（ひどい忘恩による撤回・533 条で事前の放棄不可）とフランス民法典 953 条・955 条が残る（portfolio-50 の持ち越し・条文は 30 が取得）。*irrevocable* は承認済みのライセンス（Apache-2.0 など）も使う慣用の語で、法定の撤回権に負けることは前提として読まれる。第 2 文 *"The Dedicator may not withdraw it"* は Dedicator 自身の約束で、約束としては真 | ③（UrhG 42 条・CPI L121-4・§203 は `jurisdictions.md` に在る。贈与の撤回は 30 が足した）。**米国の出典（不利な側・2f）**: Asset Marketing v. Gagnon（第 9 巡回区・2008）*"because AMS paid consid-eration, this license is irrevocable"* —— 撤回不能の理由を対価に置くので、対価の無い ACD の *irrevocable* は語だけからは立たず、米国で撤回を止めるのは §2.5（禁反言）と §5 の約束の側になる（判決は対価の無い許諾を撤回できるとは判示していない・反対の読みは推論・`rounds/2026-11-16-us-asset-marketing-v-gagnon-consideration-snapshot.txt`）|
| §2.3 | 受諾が無くても許しが立つ | §4 を契約と読む法域（BGB 151 条・民法 527 条）では、知らない受け手に許諾が成立しない読みがある（§15.23）。米国の側（2f）: 受諾が無ければ bare license（Rosen 氏 2005・`rounds/2005-08-license-discuss-bare-licenses-rosen-assent-observed.txt`）、§2.5 の禁反言の足場は Restatement (Second) of Contracts の section 90（`rounds/2026-11-16-us-restatement-90-promissory-estoppel-snapshot.txt`）| ③（30 が `jurisdictions.md` と問い 1 に書いた）・出典あり |
| §2.5 | 約因・方式の欠如を理由に無効を主張しない（禁反言）| *"to the extent the law of any jurisdiction gives that principle effect"* と法に条件づけた形で、どの法域でも真 | ① |
| §2.6 第 1 文 | 提出は既定で献呈の下に入り、提出者は Dedicator になる | 提出を同意と読めるかは法が決める（問 4）。米国の側（2f）: 非独占の許諾は書面を要さず黙示でもよく、意思は提出の時の客観的な行為で決まり、署名の無い文書も意思の証拠になる —— ACD の告知のある企画へ出す行為は、少なくとも黙示の非独占の許諾の意思を示す（Asset Marketing v. Gagnon [5]〜[7]・`rounds/2026-11-16-us-asset-marketing-v-gagnon-consideration-snapshot.txt`）。逆側: 黙示の許諾が運ぶのは使う許しで、§3 の放棄や §5 の約束まで黙示で運ぶとは言えない | ③ —— 法律家への問い 4・出典あり |
| §2.6 第 4 文 | *"No separate instrument, assignment, or agreement is needed to place a Contribution under this Dedication."* —— 書面や別の合意は法的に要らない | 受け身の *is needed* が法の命題として読め、書面や権利ごとの明示を要する法域（フランス CPI L131-2・L131-3 は著作者の権利の移転に書面と権利ごとの明示を求める）では偽になりうる。ACD は権利を移転しないので当たりにくいが、提出者の権利を Work へ献呈させる形は移転に近く読まれうる | **②** → **T84 で入った（2026-11-16）**: *"This Dedication requires no separate instrument, assignment, or agreement to place a Contribution under it."*（0 語）—— 文書自身の要求の言明になり、法が別に書面を求めるかは言わない |
| §2.7 | Dedicator の持つ権利だけに届く | 範囲を限る起草の言明 | ① |
| §2.8 | 承継人・譲受人を拘束する | *"to the fullest extent the law permits"* と法に条件づけた形。拘束の範囲の法域差は起草では閉じない（SELF-AUDIT の E）| ①（範囲の差は ③）|
| §2.9 | 倒産の手続は献呈に影響せず、管財人は譲受人として扱う | 米国: Tempnology（2019）は拒絶を解除でなく違反とし、既に与えた権利は残るとした。executory は *"performance remains due to some extent on both sides"* で、受け手に義務の無い ACD の licence は当たりにくい（2f が法源を rounds に置く）。ドイツ InsO 103 条の選択権が及ぶかは問 8 | 米国は ①（法源つき）。ドイツは **②** → **T89**（*"under its terms"* で文書の中の効果に絞る・管財人の否認 InsO 134 条は法の側に残る・`rounds/2026-11-16-inso-103-129-134-143-gesetze-im-internet-snapshot.txt`）|
| §3.1・§3.3 | 放棄・waiver | *"to the fullest extent permitted by the law of each jurisdiction"*・*"where the law … permits it to be waived"* と法に条件づけた形 | ① |
| §3.2 | 放棄は報酬請求権（補償・報酬・徴収・使用料）を含む | §3.1 の「法の許す限り」の下に入る。ドイツの法定報酬請求権（UrhG 63a 条など）は事前に放棄できないが、条件づけた形なので文は偽にならない | ①（法の限りで空になる部分がある）|
| §4.1 | 譲渡可能・再許諾可能 | ドイツ UrhG 34 条・35 条は譲渡・再許諾に著作者の同意を要するが、許諾の語自体がその同意になる | ① 。*irrevocable, perpetual* の米国での効力は §2.2 の行の Gagnon（2008）と同じ根 |
| §4.2 | *"by any means now known or later devised"* | ドイツ UrhG 31a 条は未知の利用方法の許諾に書面を求めるが、誰にでも無償で単純な利用権を与える場合を除く、というのが我々の読み（条文の確認を 30 に頼む）。フランス CPI L131-6 は予見できない利用形態の明示と利益配分を求め、無償の公衆への許諾（L122-7-1）に及ぶかは我々の読みでは決まらない | ドイツは ①（条文待ち）、フランスは ③ |
| §4.3〜§4.6 | 条件の無さ・独立・下流の扱い | 起草の言明で、法の命題を言わない（§4.4 の *"takes effect whether or not Section 3 does"* は §3 に依存しないことの言明）| ① |

**結果**: §1〜§4 の ② は 1 つ（§2.6 第 4 文・T84 の種）。③ は 5 つ（§2.2・§2.3・§2.6 第 1 文・§2.9 のドイツ・§4.2 のフランス）で、どれも `jurisdictions.md` か法律家への問いに在るか、30・2f が書いている。


### 18.2 §5〜§7（§5 は portfolio-30、§6・§7 は portfolio-2f・main の 1.4 草案）

§5〜§7 は portfolio-30 の帯。§6 と §7 は EU の法源が主なので portfolio-2f が行を書き、独・英・仏・日の当ては 30 が同じ行の命題の括弧に足す（台帳が 1 条 1 行で数えるため）。§5 の行は 30 がこの段落の直後に置く。

- §5.1 | 命題: Dedicator が「許された使用を違法とし、または法律上の原因を欠くとする請求」を主張しないという約束が、約束として効く（独: UrhG 29 条 2 項が *"schuldrechtliche Einwilligungen und Vereinbarungen"* *" zu Verwertungsrechten"* を許す取引に挙げ、約束の形を法が予定する。T90 の *"without legal ground"* は BGB 812 条・民法 703 条に当たり、仏 1303-1 条は無償の意思から生じた利得を不当でないと明文で外す。英: 約因の無い約束は捺印証書でなければ契約として強制できないと読む（判例は未取得）—— 英国では契約より抗弁と §2.5 の禁反言として働く。日: 不起訴の合意は判例法で条文は無い（未取得）。独の弁護士 Kreutzer 氏（2011 年頃・CC0 の分析）は CC0 の同じ形の約束を *"pactum de non petendo"* として *"valid and legally binding"* と評した —— 独の強制の可否は意見で狭まった（判決ではない）。範囲の語は T90 の後で閉じ、強制の可否は契約の成立に依る → 問い 5） | ③ | 状態: 出典あり | 法源: rounds/2026-11-16-urhg-29-gesetze-im-internet-snapshot.txt・rounds/2026-11-16-unjust-enrichment-bgb-812-minpo-703-code-civil-1303-snapshot.txt・rounds/2026-11-16-kreutzer-cc0-german-law-analysis-snapshot.txt
- §5.2 | 命題: Dedicator は利用規約・技術的手段などで Work に条件を足さない（範囲は §5.2 の末段と T91 で起草が閉じた。強制の可否は §5.1 と同じ根 → 問い 5） | ③ | 状態: 出典あり | 法源: rounds/2026-11-16-urhg-29-gesetze-im-internet-snapshot.txt
- §5.3 | 命題: 下流の受け手が約束を intended beneficiary として頼れる（日: 民法 537 条 2 項は第三者が契約の時に特定していなくてもよいとし、3 項の受益の意思表示は受け手が約束を抗弁として持ち出すことに当たると読む。英: Contracts (Rights of Third Parties) Act 1999 s.1(1)(b) と (3) の階層での特定が §5.3 の形に合う。独: BGB 328 条 1 項。どれも契約の成立が前提で、英国では約因が無いので Act が当たらない読みが強い。*"to the extent a jurisdiction gives effect to such reliance"* と条件づけた形なので文は偽にならない → 問い 1） | ③ | 状態: 出典あり | 法源: rounds/2026-11-16-third-party-beneficiary-minpo-537-crtpa-1999-bgb-328-snapshot.txt

**§5 の読み（portfolio-30）。** §5 の ② は 0（T90・T91 で語の側は閉じた）。③ は 1 つの根にまとまる —— **ACD が契約として成立するか**（§2.3 の知らない受け手、英国の約因、日独の第三者のための契約の前提）。問い 1 と問い 5 の本体で、起草では消せない。

- §6.1 | 命題: TDM と学習の利用を、法定の例外とは別に許諾で許せる（DSM 指令 前文 18 は、権利者が例外の外の利用を許諾できると述べる） | ① | 状態: 出典あり | 法源: rounds/2026-11-16-eu-tdm-and-conflict-of-laws-snapshot.txt
- §6.2 | 命題: Dedicator が留保をしないと宣言し、自分の権利について、どの信号も留保と読まないと定められる（DSM 指令 第 4 条 3 項の留保は権利者の行為で、オンラインでは機械可読の方法が「適切」—— 宣言は条と同じ向きだが、Dedicator が後に置いた機械可読の信号が留保と読まれるかは、HansOLG 5 U 104/24 の判決文を取るまで残る → 問い 6） | ③ | 状態: 出典あり | 法源: rounds/2026-11-16-eu-tdm-and-conflict-of-laws-snapshot.txt
- §6.3 | 命題: Dedicator は自分の留保を撤回でき、他の権利者の留保は撤回できない（第 4 条 3 項は留保を "their rightholders" の行為とする —— 後半は条と同じ。前半の撤回の効力は条の文からは決まらない → 問い 6） | ③ | 状態: 出典あり | 法源: rounds/2026-11-16-eu-tdm-and-conflict-of-laws-snapshot.txt
- §6.4 | 命題: Dedicator の権利の下では、学習の結果のモデルと出力について請求が生じない（Dedicator 自身の権利についての言明で、法の命題に頼らない。モデルに権利が在るかは決めない） | ① | 状態: 出典なし
- §6.5 | 命題: 明示の理由の言明 | ① | 状態: 出典なし
- §7.1 | 命題: sui generis のデータベース権は許諾できる（DB 指令 第 7 条 3 項 "may be transferred, assigned or granted under contractual licence"）。放棄（§3 の surrender）ができるかは指令の文に無い → 問い 1 | ③ | 状態: 出典あり | 法源: rounds/2026-11-16-eu-database-directive-snapshot.txt
- §7.2 | 命題: 作成者は全部か実質的な部分の抽出と再利用を、反復・系統的なものも含めて許せる（第 7 条 1 項は作成者の「防ぐ」権利、5 項は反復・系統的な抽出を防ぐ範囲に含める —— どちらも作成者の権利の範囲で、3 項により許諾できる。第 15 条は適法な利用者の権利（第 8 条）を狭める契約の条項を無効とするが、§7.2 は広げる側なので当たらない。米国にはこの権利が無い） | ① | 状態: 出典あり | 法源: rounds/2026-11-16-eu-database-directive-snapshot.txt

**読み。** §6.1 と §7.2 は EU の条の文と同じ向きで、狭まった。§6.2・§6.3 の残りは、Dedicator 自身が後に置く信号と撤回の効力で、問い 6 の側（ドイツの控訴審の判決文が鍵・30 へ）。§7.1 の残りは sui generis 権の放棄の可否で、問い 1 の側。

**逆側。** 指令は加盟国の置き換えを要し、国内法の文は取っていない。§6.1 の「例外とは別に許諾で許せる」は前文の文で、条の文ではない。

### 18.3 §8〜§10（portfolio-50・main の 1.4 草案・T83 の前）

| 条 | 頼っている法の命題 | 当て（我々の読み・法源は未取得のものは 30 / 2f へ） | 分類 |
| :-- | :-- | :-- | :-- |
| §8.2 *"are not terminable by the Dedicator on any ground"* | 対価の無い特許の許諾を、許諾者が後から終わらせられない | **独・仏で偽になりうる**: 無償の付与が贈与と読まれれば、受贈者のひどい忘恩を理由とする贈与の撤回（独 BGB 530 条・仏 民法典 953 条・955 条）が法定の終了の事由として残り、契約で事前に放棄できない（独 533 条）。米・英では対価の無い許諾は撤回可能と読まれうるが、§2.5（禁反言）と §8.6（約束）が別の足場になる。T81（§10.4 と米国 §203）と同じ型 —— 文が「どの事由でも終わらない」という法の命題になっている | **② —— T84〜T88 で入った**（T85・§15.25）。案は *"are not terminable by the Dedicator under this Dedication on any ground"*（+3）か、T81 と同じ *"under it"*。逆側: 法定の撤回を自分から名指さない形でも、受け手に「法による終了は在る」と気づかせる。§2.2 *"This Dedication is irrevocable"* も同じ命題を持つが §1〜§4 の帯（1c）なので 18.1 で当てる |
| §8.6 *"it operates in every jurisdiction"* | 約束がどの法域でも効力を持つ | 「効く」は法の命題で、対価の無い約束が契約として効かない法域（英米の consideration）や方式を要する法域では偽になりうる。文の役は「許諾が無効と判断されるのを待たずに働く」で、範囲の言明である | **② —— T84〜T88 で入った**（T86・§15.25）。案は *"it is given for every jurisdiction"*（語数 ±0）—— 効力でなく範囲を述べる。逆側: 「given」は効くかを述べないので、§8.6 の役（第 2 の足場）が弱く読まれうる。効くかは問い 2 の側に残る |
| §8.1 *"irrevocable, perpetual"* | 無償の特許の許諾が撤回できない | 上の §8.2 と同じ根。§8.1 の形容詞は許諾の性質の宣言で、終了の事由についての文ではない | **③** 問い 1・2 の側（法律家）。§8.2 を②で直せば、§8.1 は宣言として残せる |
| §8.4 *"a feature that the Work teaches or embodies is taken so to result"* | 当事者が因果を「みなす」ことができる | 許諾の範囲を当事者が定めるのは契約・一方的な許諾のどちらでも許諾者の自由で、法の命題ではない。因果の判定の実務は実務家への問い 3 | ① |
| §8.5 *"controlled … if, and only if"* | 定義 | 法の命題でない | ① |
| §9.2 第 3 文 *"Where a right … is later held to subsist, this Dedication applies to it"* | 後に認められる権利（新しい権利・未知の利用の種類）に、いまの付与が及ぶ | 独では未知の利用の種類についての契約は書面を要し撤回できる（UrhG 31a 条 1 項）が、**誰にでも無償で単純な利用権を与える場合は書面を要しない**（同条 1 項 2 文・いわゆる Linux 条項）—— ACD の §4 はこの形に当たると読む。日本・英米に同種の制限は見つからない（我々の読み） | ①（出典を 30 へ: UrhG 31a 条 1 項 2 文の条文） |
| §9.1・§9.3・§9.4 | 事実の言明と、受け手に判定を求めないことの宣言 | 法の命題でない | ① |
| §10.1〜§10.3 | 文書が受け手に条件を課さないことの言明 | 文書の中身についての言明で、どの法域でも真 | ① |
| §10.4 第 1 文（T81 の後）・第 2 文 | 文書の中に終了と復活の条項が無い | 文書の中身についての言明 | ① |
| §10.5 | §16 は文書についての条で Work についてではない | 同上 | ① |

**結果**: ② が 2 つ（§8.2 の「どの事由でも終わらない」、§8.6 の「どの法域でも効く」）、③ が 1 つ（§8.1 の撤回不能の効力・問い 1・2 に既に在る）、残りは ①。②の 2 つは T81 と同じ型で、文書が自分の外の法の効力を言い切っている。**1c へ**: 試作の種として 2 つ。**30 へ**: BGB 530・533 条と仏 民法典 953・955 条、UrhG 31a 条 1 項 2 文の条文の取得。**⚠ 逆側**: 贈与の撤回の当てはまりは、一方的な公の付与が贈与に当たるか（30 の §3 の段・問い 9）に依り、当たらなければ §8.2 の文は独・仏でも偽にならない。②の直しは、当たる場合の害を消す保険である。

### 18.4 §11〜§13（portfolio-2f・main の 1.4 草案・米国と EU の法源つき）

行の形は portfolio-9b の台帳（`measure_legal_uncertainty.py`）が読む形。独・英・仏・日の当ては portfolio-30 の法源を待つので、行の末尾に「30 へ」と書いた。

- §11.1 | 命題: 著作権と特許の許諾は、商標・商号・人の名の権利を与えない（文は付与しないことの言明で、法の命題に頼らない） | ① | 状態: 出典なし
- §11.2 | 命題: Work を真実に名指し、出所として Dedicator を名指す使用は、商標の効力の外にある | ① | 状態: 出典あり | 法源: rounds/2026-11-16-us-ucc-vara-and-eu-trademark-snapshot.txt
- §11.3 | 命題: 文書は虚偽の表示を許せない（文は文書の及ぶ範囲の限りの言明で、法の命題に頼らない） | ① | 状態: 出典なし
- §11.4 | 命題: Dedicator は他人の個人データ・肖像・声についての許しを与えられない（個人データの同意は本人のもの） | ① | 状態: 出典なし
- §12.1 | 命題: 人格権は、法の許す限りで放棄できる（米国: VARA の権利は視覚芸術の作品だけに在り、放棄は作品と利用を特定した署名ある書面を要する → 問い 3） | ③ | 状態: 出典あり | 法源: rounds/2026-11-16-us-ucc-vara-and-eu-trademark-snapshot.txt
- §12.2 | 命題: 譲渡できない・放棄できない人格権について、不行使の約束と同意は効く（米国: VARA の権利は "may not be transferred" で §12.2 の "inalienable" に当たり、§12.2 の側が働く。約束が §106A(e) の方式なしに効くかは判決を取っていない。独: UrhG 39 条 1 項が変更の禁止を「別段の合意が無ければ」とし、同意はその合意に当たる・残る核は 14 条。仏: CPI L121-1 で inalienable、L121-7 がソフトウェアの改変について法の側で狭める・残る核は尊重の権利。日: 59 条で譲渡不能、実務は不行使特約・portfolio-30 → 問い 3） | ③ | 状態: 出典あり | 法源: rounds/2026-11-16-us-ucc-vara-and-eu-trademark-snapshot.txt・rounds/2026-11-16-urhg-14-30-39-bgb-1922-1967-gesetze-im-internet-snapshot.txt・rounds/2026-11-16-cpi-l121-1-l121-7-legifrance-snapshot.txt
- §12.4 | 命題: 約束と同意は承継人と死後の権利の行使者を拘束する（独: UrhG 30 条で死後の権利は承継人に、BGB 1922 条・1967 条で相続人は被相続人の債務を負うので、約束が契約として成立する限り法と同じ向き。日: 60 条・116 条が対応し、60 条ただし書が著作者の意に寄せる（jurisdictions §2b）。仏: L121-1 で相続人と遺言の指定者が行使する・生前の約束への拘束は確立していない・portfolio-30） | ③ | 状態: 出典あり | 法源: rounds/2026-11-16-urhg-14-30-39-bgb-1922-1967-gesetze-im-internet-snapshot.txt・rounds/2026-11-16-cpi-l121-1-l121-7-legifrance-snapshot.txt
- §13.1 | 命題: "AS IS" の否認は黙示の保証を外す（米国: UCC §2-316 は商品性に触れ、書面なら目立つ形を求める —— §13.1 は大文字で、MERCHANTABILITY と FITNESS FOR A PARTICULAR PURPOSE と "AS IS" を持つ。EU: 商業活動の外の無償の FOSS は製造物責任指令とデジタルコンテンツ指令の外。商業活動の過程の供給なら製造物責任は契約で外せない） | ① | 状態: 出典あり | 法源: rounds/2026-11-16-eu-product-liability-and-digital-content-foss-snapshot.txt
- §13.2 | 命題: 権原と非侵害の保証を外せる（米国: UCC §2-312(2) は特定の語か事情を求める —— §13.2 は "DOES NOT WARRANT … THAT THE DEDICATOR HOLDS ANY RIGHT IN IT" と特定して述べる） | ① | 状態: 出典あり | 法源: rounds/2026-11-16-us-ucc-vara-and-eu-trademark-snapshot.txt
- §13.3 | 命題: Dedicator は保守・更新・提供の継続の義務を負わない（文書の中身の言明。EU のサイバーレジリエンス法の義務が無償の Dedicator に及ぶかは取っていない） | ① | 状態: 出典なし

**読み。** 米国と EU の側で、§11〜§13 に語で直す ② は無かった。狭まったのは 5 行で、§13.1・§13.2 は米国の UCC の要件を本文が満たし（UCC が無償の公の付与に当たるかは別の問い）、EU では商業活動の外の無償の供給はそもそも 2 つの指令の外に在る。§12 の米国の不確実性は、VARA が視覚芸術の作品（絵画・彫刻・署名した 200 部までの版など）にしか権利を与えないので、ソフトウェアとデータについてはほぼ消え、視覚芸術の作品に ACD を当てる場合に限って、§12.2 の約束が §106A(e) の方式なしに効くかが残る。

**逆側。** UCC は物品の売買のモデル法で、無償のライセンスに当たらない読みが有力なら、§13.1 が UCC の要件を満たすことは重みを持たない（害も無い）。EU の除外は「商業活動の外」に限られ、会社が業として ACD を当てれば製造物責任は §14 でも外せない（第 15 条）。§11.2 の EU の法源は商標規則で、加盟国の商標法と不正競争の法は取っていない。

**この節が establish しないこと。** §12.2 の約束と同意が、独・仏・日で効くか（30 の法源を待つ）。VARA の権利の不行使の約束が §106A(e) の方式なしに効くか。

### 18.5 §14〜§16（portfolio-9b・main の 1.4 草案・T83 の前）

入力: `scan_draft_ambiguity.py --law` の 9b の帯（6 条・13 句）と `scan_draft_ambiguity.py` の (d)・(k)。法源の取得は 30（独・英・仏・日）と 2f（米国・EU）へ渡す。

| 条 | 頼っている法の命題 | 当て（我々の読み・法源が rounds/ に無いものは未取得） | 分類 |
| :-- | :-- | :-- | :-- |
| §14.1 *"THAT APPLICABLE LAW DOES NOT PERMIT TO BE EXCLUDED … TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW"* | 無償で付与する者は、法が除外を許す範囲で責任を除外できる | 文は法に条件づけて自分を限るので、文の言明はどの法域でも真。独: 故意の責任は事前に免除できない（276 条 3 項）、約款なら 309 条 7 号、贈与と読めば責任は故意・重過失に限られる（521 条）—— rounds/2026-11-16-bgb-276-307-309-521-524-gesetze-im-internet-snapshot.txt。英: 過失による死亡・身体の傷害は除外できない（UCTA 2 条 1 項・rounds/2026-11-16-ucta-1977-s1-s2-legislation-gov-uk-snapshot.txt・30 の取得）。日: 消費者契約なら消費者契約法 8 条（未取得）。米: 消費財の人身の損害についての責任の制限は一応の不当性を推定され、商業上の損失の制限はそうでない（UCC §2-719(3)・rounds/2026-11-16-us-ucc-vara-and-eu-trademark-snapshot.txt の [8]・2f が 2026-11-17 に取得）。EU: 製造物責任指令の責任は契約で除外も制限もできない（第 15 条・rounds/2026-11-16-eu-product-liability-and-digital-content-foss-snapshot.txt の [3]）。どれも文の「法が許さない責任は除く」に入る。**逆側**: UCC が無償の公の付与に当たるか、指令が商業活動の外の無償の頒布に及ぶかは別の問いで（§18.4 の §13 と同じ）、当たらなければこれらの法源はこの条に働かない | ① |
| §14.1 *"ARISING OUT OF THIS DEDICATION OR THE USE OF THE WORK"* | 免責の射程が Dedicator 自身の約束（§5・§8.6・§12.2 ほか）の違反に及ぶか | 法でなく起草の選択で決まる（問い 9 (a)）。`scan_draft_ambiguity.py` の (k) が、外していない約束の条 13 を挙げる | **②** T83〜T88 で入った（§14.2 の例外に §5・§8.6・§12.2 を T83 で、§2.5 を T88 で）。Check 468ab が、この型が戻ると止める |
| §14.2 *"that liability is limited to the greatest extent that law permits"* | 除外できない責任について、条項を法の許す限りに縮めて生かせる | 独: 約款の無効な条項は縮めて生かさず、法律の規定が代わる（306 条 2 項 *"richtet sich der Inhalt des Vertrags nach den gesetzlichen Vorschriften"*・rounds/2026-11-18-bgb-306-gesetze-im-internet-snapshot.txt・30 の取得。効力維持的縮減の禁止の BGH の判例は未取得）。§14.2 の「法の許す限りに制限する」はこの禁止に当たりうる。英米は可分を広く認める。語で減らせる部分（除外の対象を初めから法の許す形で名指す）は T82 で済んだ | **③** jurisdictions のドイツの段へ（30） |
| §15.1 *"the reading that grants more to You prevails"* | 文書が解釈の規則を自分で定められる | 独の約款の不明確条項の規則（305c 条 2 項・未取得）と EU 不公正条項指令 93/13 の 5 条（未取得）は、どちらも受け手（消費者）に有利に読む規則で、§15.1 と向きが同じ。規則が強行的でも結果は変わらない | ① |
| §15.2 *"reformed to the minimum extent necessary … severed as to that jurisdiction only"* | 裁判所が無効な条項を書き直す（無理なら切り離す） | 独: 第 2 文（切り離し・残りは効く）は 306 条 1 項 *"so bleibt der Vertrag im Übrigen wirksam"* と同じ向き、第 1 文（最小限に改める）は約款なら当たらず 306 条 2 項（法律の規定が代わる）—— rounds/2026-11-18-bgb-306-gesetze-im-internet-snapshot.txt（30 の取得・30 の読み）。英: 裁判所は書き直さず削るだけ（blue pencil）。米: 州で分かれる。「書き直す」部分は法域の規則で、語では決められない。「切り離す」部分はどこでも働く | **③** jurisdictions のドイツの段へ（§14.2 と同じ段・30） |
| §15.3 *"no governing law"* | 準拠法を書かなくても、各法域の抵触法が使用地の法を選ぶ | 問い 7 に在る。EU: ローマ I 規則 4 条（契約）とローマ II 規則 8 条（知的財産の侵害は保護国の法・3 項は当事者の合意で外せない）—— rounds/2026-11-16-eu-tdm-and-conflict-of-laws-snapshot.txt（2f の取得）。侵害の側は文書が何を書いても保護国の法になり、§15.3 が法を名指さないことは侵害の準拠法を変えない。契約の側は、ACD が契約に当たるか（問い 1）とローマ I 4 条の特徴的な給付の読みに依る。ベルヌ条約 5 条 2 項は未取得 | **③** 法律家（問い 7） |
| §15.4 *"the authoritative language"* | 言語の優先の定めが効く | 審査の側: 正本を 1 つに定める条は承認の妨げにならず、むしろ求められた —— Mulan PSL の審査で Piana 氏が *"One version should be authoritative"* と求め、v2 が正本の条を足して 2020 年に承認された（rounds/2019-12-license-review-mulan-psl-piana-one-authoritative-version-observed.txt・rounds/2019-12-license-review-mulan-psl-v2-chinese-prevails-observed.txt・2f の取得・§1.263）。法の側: 仏 トゥーボン法（1994-665）の 5 条は、公法人と公役務を担う者が当事者の契約に限って仏語を求め、私人どうしには及ばない（30 の読み）。ただし 2 条は、財・製品・役務の *"l'offre, la présentation, le mode d'emploi ou d'utilisation, la description de l'étendue et des conditions de garantie"* に仏語を求める —— ACD を適用した製品をフランスの消費者へ出す採用者にとって、§13 の保証の否認が「保証の条件の記述」に当たるかは別の問い（rounds/2026-11-18-loi-toubon-94-665-art-2-5-legifrance-snapshot.txt・30 の取得）。**逆側**: 正本の条があっても、地域の裁判所が自国語の訳を参照することまでは止められない | **③** jurisdictions のフランスの段へ（30）—— 審査の側は狭まった（Mulan PSL）、法の側（トゥーボン法）は残る |
| §15.5 *"person" includes an entity* | 文書の定義の規則が効く | 定義の規則は一般に効く。ただし本文が "person or entity" を §1.4・§1.6・§16.5 の 8 か所で重ねて書くので、「person だけの所は entity を含まない」の反対解釈を招く（`scan_draft_ambiguity.py` の (d)）。語で消せる | ① —— §15.5 の明示の規則が「明示したものだけを含む」の推定に勝つ（1c の判断・2026-11-16）。定義の中の "or entity" は §15.5 を読む前の読み手への明示として働き、22 の文書が引く 1.0 の語とも揃う。**逆側**: 重ね書きを外せば 16 語減り、推定の余地そのものが消える（見送った）|
| §15.6 *"No rule of construction that resolves ambiguity against the drafter applies"* | 作成者に不利に読む規則を排除できる | 独 305c 条 2 項と指令 93/13 の 5 条は排除できない場面がある（未取得）。ただし ACD ではその規則の向き（受け手に有利）が §15.1 と同じなので、排除が効かなくても結果は変わらない | ① |
| §16.2 *"that is sufficient notice of these terms, and the terms apply in full"* | 識別子だけで条件が受け手に及ぶ | ACD は受け手に条件を課さない（§10.1）ので、受け手を縛る合意の成立は要らない。通知の十分性は許諾が受け手に届くかだけの問いで、届かないときに受け手が負う不利は無い | ① |
| §16.3・§16.6 | 文書の利用の許しと、§16.4・§16.5 が Work の条件でないことの言明 | 文書の中身についての言明 | ① |
| §16.4 *"A modified text may not be distributed under any name that contains …"* | 文書の著作権で、改変した文書の頒布の名を制限できる | 審査の側: 承認済みのライセンスが本文の改変そのものを禁じる先例が在る —— GPL-3.0 の頭 *"Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed."*（rounds/2026-11-18-gpl-3-0-header-spdx-snapshot.txt・SPDX の license-list-data・2f の取得）。§16.4 は改変そのものを禁じず、名と識別子での頒布だけを縛るので、より弱い形。法の側: 名そのものは著作権で守られない。制限は改変した文書の頒布の許しの範囲として働く（文書の著作権の範囲内）。名と識別子が使われている標章と重ならないかは問い 10 | **③** 法律家（問い 10）—— 審査の側の先例は在る（GPL-3.0）、名で縛れるかの法の根拠（文書の著作権か商標か）は残る |
| §16.5 *"the Steward"* | 役の譲渡で Steward の地位が移る | 文書の中の定義で、法の命題でない | ① |

**結果**: ② が 1 つ（§14.1 の射程・T83 と T88）、③ が 5 つ（§14.2・§15.2 の効力維持的縮減の禁止、§15.3 の準拠法、§15.4 のトゥーボン法、§16.4 の名）、残りは ①。**1c へ**: ② の 1 つ（§14.1・T83 で入り、§2.5 は T88）。§15.5 の重ね書きは 1c の判断で ① に替えた（2026-11-16）。**30 へ**: 独 305c 条 2 項・306 条 2 項と効力維持的縮減の禁止の判例、英 UCTA 2 条 1 項、仏トゥーボン法、日 消費者契約法 8 条の取得。**2f へ**: 指令 93/13 の 5 条、ローマ I 規則 4 条、ローマ II 規則 8 条、ベルヌ条約 5 条 2 項。**⚠ 逆側**: §14.2 と §15.2 の ③ は、ACD が約款に当たるか（問い 9）に依り、当たらなければドイツの禁止は及ばない。① の多くは「文が法に条件づけて自分を限る」ことに頼っていて、その形はどの法域でも真だが、受け手が実際に得る保護の大きさは法域で違う。
