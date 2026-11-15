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

