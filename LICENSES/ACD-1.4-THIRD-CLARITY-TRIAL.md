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

**この file で足した規則（2026-11-15）**: (1) 2 冊目は 1,000 行の上限（Check 365）の手前なので、§10〜§14 の節への訂正や逆側の追記も、2 冊目には足さず、この file に「§14.N への追記」として書く。(2) 本文に特定の名（組織名・URL・人名）を足す案は退ける —— 承認は一語も変えない本文に対するもので、承認済みの写しは型板として使われる（Nelson 氏 2008・`review-readings-2.md` §1.238）。§16.3（誰でも適用でき、特定のプロジェクトや人に結ばれない）と §16.4 の名の規則も同じ考えに立つ。いま本文に在る固有の名は *Autonomous Commons Dedication* と識別子だけで、§16.1 の雛形の *<location of this file>* は差し込みの印である。(3) 一般形（*every other provision* など）を足すときは、自分の条が主語にしているものと、受領者のために働かない条（§13・§14・§16）を量化が巻き込まないかを読む（§15.5）。

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

**§15.7（T71）への追記（portfolio-30）**: 理由を作用の条に置くと Chestek 氏 2026-01-24 *"The unnumbered parts appear to be explanatory material, so I question whether they belong in the agreement at all."* と Piana 氏の線（説明は本文に入れない）に当たり、前文に置くと前文は自ら *"informative; not part of the operative terms"* と述べるので、`against.md` #124 の線では効力を持たない。どちらも同じ審査者の文に当たるので「理由をどこに置くか」に正解は無く、T71 は理由が範囲を狭める読みを許す害（E85）を除く方を選んだ。
