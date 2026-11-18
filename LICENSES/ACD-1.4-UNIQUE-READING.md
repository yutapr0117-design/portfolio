---
file: LICENSES/ACD-1.4-UNIQUE-READING.md
audience: 次のセッションの実装者（一次読者）/ 監査人 / 法律家
last-updated: 2026-11-18
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt / .github/scripts/measure_legal_uncertainty.py（section19 が行を数える）/ LICENSES/ACD-1.4-THIRD-CLARITY-TRIAL.md（§18 の法の側）
---

# 1.4 草案の法的解釈を一意に定める —— 各条の「最も強い別の読み」

THIRD（`ACD-1.4-THIRD-CLARITY-TRIAL.md`）にあった第 19 節を 2026-11-18 にこの file へ移した（本文は無改変・見出しの番号はそのまま）。各帯の人は**自分の小節の中に**行を足す（末尾に足さない —— 5 人が同じ末尾に足して衝突が続いたので分けた）。行の形と数え方は `LICENSES/LEGAL-UNCERTAINTY.md` と `measure_legal_uncertainty.py` の section19()。

## 19. 法的解釈を一意に定める —— 各条の「最も強い別の読み」を 1 つ書き、立つなら語で消す（2026-11-18〜・オーナーの依頼）

**依頼**: オーナー 2026-11-18「ACD-1.4-DRAFT.txt の法的解釈が一意に定まるように「５人」で連携しながら続けてください」。**§18 との分け**: §18 は法の側の不確かさ（どの法域で効くか）を扱った。§19 は **本文の語が 2 通り以上に読める所** を扱う。**方法**（portfolio-2f の案で 5 人が決めた）: 各条の最も強い別の読みを 1 つ書き、立たない → 一意（閉じている条を根拠に名指す）、立つ → 1c の試作（Tnn・【反例待ち】）で語を消す、法の側に依る → 既存の問い・§18 の ③。探す手がかりの型: 先行詞・修飾の掛かり先・量化・or・including・定義語の混用・時点・主語・否定の範囲。**行の形**: `- §x.y | 別の読み: … | 一意 / 試作 Tnn / 法の側 | 根拠: …`。**小節**: 19.1 = §1〜§4（1c）、19.2 = §5〜§7（30）、19.3 = §8〜§10（50）、19.4 = §11〜§13（2f）、19.5 = §14〜§16（9b）。各自、自分の小節を見出しごと足す（番号順に並べる）。

### 19.1 §1〜§4（portfolio-1c・main の 1.4 草案・T96 の前）

- §1.3（1.0 では §1.2） | 別の読み: *"any collection or compilation of these"* の *these* が、列挙した種類でなく素材一般を指し、Work の外の素材との集合物まで Work になる | 一意 | 根拠: *these* は直前の列挙を受け、Work は *"the material to which the Dedicator has applied this Dedication"* に限られる（§2.7・§16.2 の適用の範囲。E61 で *in whole or in part* を外した）
- §1.4 第 1 文 | 別の読み: *"holds or may hold … in it"* の *it* が Dedication を指す | 一意 | 根拠: Dedication に権利を持つ読みは意味を成さず、§1.5 の *"in the Work"* と揃う
- §1.6 第 3 文 | 別の読み: *"on whose behalf it acts"* の *it* が permission を指す | 一意 | 根拠: §1.6 の同じ文 —— *acts* の主語は同じ節の *an automated system*
- §1.7 | 別の読み: 列挙の後ろの *"resulting from that processing"* が最後の *other data* だけに掛かる（last antecedent rule）—— どのモデルの作成・頒布・使用も Computational Use になる | 試作 T96 で入った | 根拠: §1.7 は *"other data that results from that processing"*（関係節が *any* の束ねる名詞の束に付く）、§6.4・§8.4 は *"in each case resulting from"*（30 の反例で §1.7 だけ形を変えた・§15.31）
- §2.2 第 2 文 | 別の読み: *"any copy of the Work that has been made available"* の *that has been made available* が *Work* でなく *copy* に掛かり、Dedicator がまだ頒布していない写しには後から条件を付けられる | 一意 | 根拠: どちらの掛かり方でも、頒布された写しには条件を付けられない。*Work* に掛ける読みの方が受け手に多く与えるので、§15.1 *"the reading that grants more to You prevails"* がそれを選ぶ
- §2.3 第 2 文 | 別の読み: *"cause You to lose one"* の *one* が *act* を指す | 一意 | 根拠: §2.3 の同じ文 *"To hold a permission granted here"* の *permission* を受ける
- §2.8 第 2 文 | 別の読み: *"takes subject to it to that extent"* の *that extent* が第 1 文の *"to the fullest extent the law permits"* 以外（Dedicator の持つ権利の範囲）を指す | 一意 | 根拠: §2.8 第 1 文の唯一の *extent*（*"to the fullest extent the law permits"*・T59 で足した語）
- §2.9 第 2 文 | 別の読み: *"Such an officer"* が第 1 文の officer の一部だけを指す | 一意 | 根拠: §2.9 第 1 文 —— *such* はその列挙全体（*trustee, administrator, receiver, liquidator, or equivalent officer*）を受ける
- §3.1 | 別の読み: *"to the fullest extent permitted by the law of each jurisdiction"* が後半の *"places the Work in the public domain"* にも掛かり、公有にする法域を限らない | 一意 | 根拠: §3.1 の後半が自分の限定 *"in each jurisdiction that gives effect to such an act"* を持つ
- §4.2 | 別の読み: *"any adaptation of it"* の *it* が licence を指す | 一意 | 根拠: §4.2 の同じ列挙の目的語 *the Work* を受ける
- §4.5 第 1 文 | 別の読み: *"terms that are incompatible with these"* の *these* が、この Dedication の条項でなく、直前の *terms* や *conditions upon Your own recipients* を指す | 試作 T97 | 根拠: *"incompatible with this Dedication"*（+1）で先行詞を語に置く
- §4.6 第 2 文 | 別の読み: *"Terms You add govern what You give"* が、You の加えた条件が Dedicator の約束（§5.3 の受益者）まで狭めると読む | 一意 | 根拠: §4.6 第 2 文の後半 *"they do not narrow what the Dedicator has already given in respect of the Work"*

**結果**: §1〜§4 の立つ別の読みは 2 つ（§1.7 は T96・§4.5 は T97）。ほかの 10 行は他の条（§15.1・§1.5・§2.7・§16.2）か同じ文の語が一方に閉じている。

### 19.2 §5〜§7（portfolio-30・main の 1.4 草案・T95 の後）

- §5.1 第 1 文 | 別の読み: *"in respect of any use of the Work"* の *use* を狭い意味（使用だけで、複製・頒布・改変を含まない）に読み、約束が複製や頒布の権利の主張に及ばない | 一意 | 根拠: *use* は定義されていないが、§15.1 が *"the reading that grants more to You prevails"* と受け手に多く与える読みを選ばせ、同じ文の *"any Covered Right"* が複製・頒布の権利を含む。
- §5.1 第 2 文 | 別の読み: 例外の *"for a payment You agreed to make"* が、第三者への支払いの約束を根拠に Dedicator が請求を立てることを許す | 一意 | 根拠: §5.1 第 2 文の主語。約束は Dedicator 自身の請求の主張についての文で（*"The Dedicator further covenants not to assert against You"*）、第三者への支払いの請求権を Dedicator は持たない。例外は Dedicator 自身が当事者の支払いに限って働く。
- §5.2 末段 | 別の読み: Dedicator が自分の素材（例: 自分のモデル）に Work の写しを含め、その素材の利用条件で中の写しまで縛るとき、条件は *"the terms or measures the Dedicator applies to that material"* として §5 の外に在り、§5.2(b) は当たらない（最後の文 *"A copy of the Work … remains the Work"* は写しが Work であることを言うだけで、条件が §5 の内に入るとは言わない） | 試作 T98 | 根拠: 最後の文の目的（T91・同梱した写しは Work のまま）は読み A（条件はその写しには及ばず §5.2(b) が禁じる）を示すが、語は「素材に当てた条件」を丸ごと外に出しており、写しへの効き目を閉じていない。案: 最後の文の後に *"and Section 5 reaches those terms and measures so far as they apply to it"*（+12 語）か、外に出す文を *"…applies to that material, other than so far as they apply to a copy of the Work it contains,"* とする。逆側: SaaS の規約（写しを渡さない）は、前の文が外に置いたままで、この案はそこへ戻さない。
- §5.3 | 別の読み: 末文 *"Sections 3 and 4 operate in their favour independently of Section 5.3"* の *their* が §2.8 の者（拘束される側）を指す | 一意 | 根拠: 直前の文の主語は約束、*relied upon by You and by anyone who receives the Work from You* が受益者で、§3・§4 は受け手に働く条なので、*their* は受益者を指す読みしか意味をなさない。
- §6.1 | 別の読み: *"by any person or automated system"* が、自動の仕組みそのものを許しの持ち主にする | 一意 | 根拠: §1.6 が、自動の仕組みが行使した許しはその背後の人と運用者に与えられると定める。
- §6.2 | 別の読み: *"whoever placed it there"* が、他の権利者が置いた留保まで留保でないと読ませる | 一意 | 根拠: §6.2 第 2 文と §2.7。同じ文が *"So far as the Covered Rights and patent claims of the Dedicator are concerned"* と範囲を Dedicator の権利に限り、次の文が *"does not purport to defeat a Reservation made by another rightsholder"* と明示する。
- §6.4 | 別の読み: 学習データに Work と他人の作品が混ざったモデルは、*"resulting from Computational Use of the Work"* に当たらない（Work だけから生じたものに限る） | 一意 | 根拠: §6.4 第 1 文と §2.7。文は *"under this Dedication or under any Covered Right of the Dedicator"* の請求に限るので、他人の作品が混ざっても、Dedicator の権利の側の結果は変わらない。混ざったモデルについての他人の権利は、もともとこの文の外。
- §6.5 | 別の読み: §6.1 の *"expressly permitted"* が §3〜§5・§8 から独立した許しで、§4 が効かない法域でも §6 だけで許しが立つ | 一意（読み A: §6 は宣言的） | 根拠: §6.5 自身が *"Section 6 states expressly what Sections 3 to 5 and 8 would in any event permit"* と述べる。逆側: §4 が効かない法域で §6.1 が独自の許しとして読まれることを、この文は封じる —— 受け手に少なく与える読みを本文が選んでいる。§15.1 との関係は、§6.5 の明示が優先すると読む。
- §7.1 | 別の読み: *"Sections 3 to 6 apply to it"* が §8（特許）を外すことに意味があり、データベース権について特許の許諾は働かない | 一意 | 根拠: データベース権は特許とは別の権利で、§8 はもともと特許の請求項にしか届かない。外しているのではなく、当たる条を挙げている。
- §7.2 | 別の読み: *"without limit and without condition"* が、Dedicator 以外の者のデータベース権まで許す | 一意 | 根拠: §2.7。同じ文が *"so far as the Covered Rights of the Dedicator are concerned (Section 2.7)"* と限る。

**§19.2 の結果**: 10 行のうち、立つ別の読みは 1 つ（§5.2 末段・1c の T98）。§6.5 は一意だが、受け手に少なく与える側に本文が定めていることを逆側に記録した。


### 19.3 §8〜§10（portfolio-50・main の 1.4 草案・T95 の後・2026-11-18）

各条で、語の構造から立つ最も強い別の読みを 1 つずつ書いた。「一意」は他の語か他の条が既にその読みを閉じているもの（根拠にその条を名指す）、「試作」は語を変えれば 1 つに定まるもの、「法の側」は語では定まらず §18 の ③ に送るもの。

- §8.1 | 別の読み: *"now or in future"* が *"owned or controlled"* でなく *"that those acts would infringe"*（侵害の時点）に掛かる | 一意 | 根拠: §8.5 が *"patent claims the Dedicator owns or controls, now or in future"* と、同じ句を保有の側に置いて繰り返す
- §8.1 | 別の読み: *"where the infringement is caused by subject matter contained in the Work as made available by the Dedicator"* が許諾の「条件」で、§8.2 の *"subject to no condition"* と食い違う | 一意 | 根拠: §10.1 の *"condition … upon You"* は受け手に課すものを言い、この句は届く請求の範囲（何が侵害の原因か）を言う。§8.3 も *"reach a patent claim only as to the acts they describe"* と範囲の語で受ける
- §8.2 | 別の読み: *"by You"* が *"participation in patent litigation"* だけに掛かり、*"commencement of"* は誰が始めても当たる | 一意 | 根拠: どちらの読みでも終了の事由にならない（*"on any ground"*）ので、読みが割れても効果は同じ
- §8.3 | 別の読み: 第 2 文 *"Nothing in this Dedication reserves, preserves, or leaves unaffected any patent claim they reach"* が、届いた請求を（第 1 文の行為に限らず）全体として残さないと言い、第 1 文 *"only as to the acts they describe"* と食い違う | **試作 T99（1c・【反例待ち】）** | 根拠: 第 2 文に行為の限定が無い。案: *"… leaves unaffected, as to those acts, any patent claim they reach."*（+4）。逆側: 第 1 文を読めば限定は明らかだという読みも立つが、2 つの文が別々に引かれると第 2 文だけが広く読まれる
- §8.4 | 別の読み: *"resulting from Computational Use of the Work"* が *"other data"* だけに掛かり（直前の先行詞の規則）、*"any model"* はどのモデルでも許諾に入る | 試作 T96 で入った（*"in each case resulting from"*・PR 3610） | 根拠: 1c の最初の当たり（§1.7・§6.4・§8.4 の同じ列挙）。§8.4 の第 6 文 *"reaches a claim only where the feature that infringes it results … from the content of the Work"* が因果で絞るので、特許の届く範囲はどちらの読みでも Work に由来する特徴に限られる —— 割れるのは「許される行為」の側
- §8.4 | 別の読み: *"Section 8.1 alone governs a feature added to the Work, by whatever means"* の *"by whatever means"* が *"governs"* に掛かる、または §8.1 が足された特徴に許諾を与えると読む | 一意 | 根拠: §8.1 の但し書き（*"caused by subject matter contained in the Work as made available by the Dedicator"*）が、足された特徴による侵害を §8.1 の外に置く。この文は「§8.4 がそれを拾わない」と言うだけ
- §8.5 | 別の読み: *"at the time in question"* が行為の時点を指し、Dedicator が行為の後に取得した請求は、その行為については届かない | 一意（効果の側） | 根拠: §8.6 の約束が *"not to assert … the patent claims that Sections 8.1 and 8.4 reach, in respect of any act that those Sections describe"* と主張の時点で働くので、後に取得した請求で過去の行為を訴えることはどちらの読みでも約束に反する。時点の語そのものは E60 が「各時点で読む」と閉じた
- §8.6 | 別の読み: *"either licence"* が §8.1・§8.4 でなく §4.1 と §8 を指す | 一意 | 根拠: 同じ文の主語が *"Sections 8.1 and 8.4"* の請求で、*"either"* は 2 つのうちの一方
- §9.2 | 別の読み: *"asserts no right in Machine-Generated Material"* が、Dedicator 以外の者の権利も主張されないと言う | 一意 | 根拠: 主語が *"The Dedicator"* で、§2.7 が届く範囲を Dedicator の権利に閉じる
- §9.2 | 別の読み: 末文 *"Where a right that this Dedication reaches subsists, or is later held to subsist, this Dedication applies to it"* の *"it"* が *"a right"* でなく Work を指す | 一意 | 根拠: 単数の先行詞は *"a right"* だけで、Work はこの文に出ない
- §10.1 | 別の読み: *"in respect of the Work"* が、モデル・出力について条件を課す余地を残す | 一意 | 根拠: §6.4 *"You owe nothing under this Dedication in respect of any of them"* がモデル・出力の側を閉じる
- §10.3 | 別の読み: *"Under this Dedication"* が文頭に在るので、Dedicator が別の契約で同じ要望を条件にしたとき、それも「条件ではない」と読む | 一意 | 根拠: 文頭の句は「この Dedication の下では」と範囲を限り、別の契約の効果を言わない。§5.2(b) が、別の手段で義務を課さない約束を Dedicator に負わせる側を受け持つ
- §10.4 | 別の読み: *"No permission granted by this Dedication terminates under it, for any reason"* の *"it"* が *"permission"* を指す | 一意 | 根拠: 第 2 文が *"This Dedication … contains no termination provision"* と同じ主語で受ける

**§19.3 の結果**: 13 行のうち、立つ別の読みは 2 つ —— §8.3 第 2 文（1c の T99・【反例待ち】）と §8.4 の列挙の後の修飾（T96 で入った）。一意 11、法の側 0。

### 19.4 §11〜§13（portfolio-2f・main の 1.4 草案）

試作の種 2 つは 1c が T100・T101 の番号を付けた（T96 の merge の後の束で【反例待ち】として出す見込み・portfolio-1c 2026-11-18）。

- §11.1 | 別の読み: 第 2 文 "Nothing in Section 11 reduces what any other Section of this Dedication gives" に反し、§11.4 の "It reaches nothing else" が §5 の約束を狭める | 一意 | 根拠: §11.4 自身が "save that the covenants in Section 5 are promises about the Dedicator's own conduct and are not limited by this sentence" と閉じている
- §11.2 | 別の読み: §11.2 の "You may name the Dedicator for that purpose" は、§11.1 が否定した Dedicator の人の名についての権利を与えており、2 つの文が食い違う | 試作 T100 | 根拠: 案は §11.2 の第 1 文を "Nominative reference is not a use of a right in a name, and is unaffected." にする（§11.1 を保ち、§11.2 を付与と読ませない・portfolio-1c が採る見込み）。逆側: "Except as Section 11.2 states," を §11.1 に足す案は §11.2 を例外＝付与と読ませるので採らない
- §11.3 | 別の読み: 虚偽の帰属（Dedicator が改変版を書いた・推奨したと表すこと）をすれば許しを失う（条件として読む） | 一意 | 根拠: §11.3 の第 3 文 "it is not a condition upon You" と §10.1
- §11.3(a) | 別の読み: 改変した Work に元の作者の表示を残すことが、Dedicator が改変版を書いたと「表す」ことに当たる | 法の側 | 根拠: 表示を残すことが虚偽の表示に当たるかは各法域の不正表示の法が決める（文書はそれを "outside what this Dedication reaches" と述べるだけ）→ 問い 5（§5.1・§5.2(d)・§11 の約束の射程）
- §11.4 | 別の読み: 貢献者（§2.6 で Dedicator になる人）の権利は "any right held by a person other than the Dedicator" に当たり、許されない | 一意 | 根拠: 1.4 草案の §1.4（1.3 までの §1.3）の "this Dedication operates severally as to each"（Dedicator はそれぞれで、各自の部分について Dedicator である）と §2.6 の "becomes a Dedicator as to that Contribution"
- §12.1 | 別の読み: "To the fullest extent permitted by the law of each jurisdiction" が、放棄そのものではなく放棄の範囲だけを法に委ね、法が放棄を許さない法域でも一部の放棄が残る | 一意 | 根拠: §12.2 がその法域では §12.1 を外して約束と同意に替えると定め、§12.2 の最後の文が受け手に判定を求めない
- §12.2 | 別の読み: 引き金 "personal to the author, inalienable, or incapable of waiver" の "inalienable" が、譲渡はできないが放棄はできる法域（英国 CDPA 87 条・米国 17 U.S.C. §106A(e) "may not be transferred, but ... may be waived"）でも §12.1 を外し、法が許す放棄を捨てて約束と同意だけにする | 試作 T101 | 根拠: 最初の案（"and instead" → "and in addition"・±0）は、同じ文の "Section 12.1 does not apply in that jurisdiction" が残るので「何に加えるか」が無く、自分と食い違う（portfolio-30 の反例）。30 が勧める案は引き金から "inalienable" を外し "personal to the author or incapable of waiver" にする（−2 語）—— 譲渡できないが放棄できる法域では §12.1 がそのまま働き、§12.2 は放棄できない法域だけに当たり、§12.2 の最後の文と合う。逆側: "personal to the author" が英米の「譲渡できない」を拾う読み（ただし CDPA 87 条 2 項は放棄を明文で許すので "incapable of waiver" でない法域として §12.1 が当たる）。法源は rounds/2026-11-16-us-ucc-vara-and-eu-trademark-snapshot.txt の [5]
- §12.3 | 別の読み: 末尾の "for the purpose stated in Section 6" が、§12.2 の同意を §6 の目的（学習と計算の利用）の行為に限る | 法の側 | 根拠: 目的の句が同意の範囲を狭めるかは同意の解釈の法に依る → 問い 3 (c)（`ACD-1.4-THIRD-CLARITY-TRIAL.md` §15.1 の追記・portfolio-30）
- §12.5 | 別の読み: 作者の表示を省くこと（偽りの帰属でない）も §11.3 に当たり、§12.2 の同意から外れる | 一意 | 根拠: §11.3 は "Representing that the Dedicator authored, endorsed, approved, sponsored, or is associated with a work, when that is not the case" で、表示の省略を含まない。§12.2 の同意は "any act ... that would otherwise infringe those rights" を覆う
- §12.6 | 別の読み: §12.2 が一部で無効になると、§12.1 が復活してその法域で働く | 一意 | 根拠: §12.6 は §15.2 を当て "the invalidity affects no other Section" と述べ、§12.2 の第 1 文が §12.1 をその法域で外している（復活の語は無い）
- §13.1 | 別の読み: "WITHOUT WARRANTY OR CONDITION OF ANY KIND" の "CONDITION" が、受け手への条件（§10.1）を指す | 一意 | 根拠: "INCLUDING WITHOUT LIMITATION ANY WARRANTY OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, FITNESS ..." の列挙が保証の文脈に閉じ、"CONDITION" は英国法の黙示の condition（保証の一種）を指す。受け手への条件は §10.1 が別に扱う
- §13.2 | 別の読み: "THAT ANY SECTION OF THIS DEDICATION IS EFFECTIVE IN ANY JURISDICTION" を否認することで、Dedication 全体の効力を Dedicator が争える | 一意 | 根拠: §13.2 は保証の否認で、効力の主張ではない。§2.5 が Dedicator に "not to assert that this Dedication is revocable or ineffective" を約束させ、禁反言を置く
- §13.3 | 別の読み: "no duty to ... continue to make the Work available" が §2.2 の撤回不能に反し、提供の停止で許しが終わる | 一意 | 根拠: §13.3 は提供の義務の否定で、許しの終了ではない。§10.4 が "No permission granted by this Dedication terminates under it" と閉じる

### 19.5 §14〜§16（portfolio-9b・main の 1.4 草案）

入力: `scan_draft_ambiguity.py --split` の 9b の帯（10 件）と、§14 の 2 つの条を並べて読んだ結果。§15.1（受け手に多く与える読みが勝つ）は受け手に与えるものについての割れを閉じるが、Dedicator の責任の範囲や文書の規律（§16）の割れは閉じない —— この帯の割れの多くはそちら側にある。

- §14.1 | 別の読み: "LIABILITY FOR WILFUL MISCONDUCT, GROSS NEGLIGENCE, DEATH, OR PERSONAL INJURY THAT APPLICABLE LAW DOES NOT PERMIT TO BE EXCLUDED" の "THAT …" が最後の "PERSONAL INJURY" だけに掛かると読むと、故意・重過失・死亡の責任は法が除外を許しても除外されない（T82 が狙った「法に条件づける」が 3 つの範疇で外れる） | 試作 T102 | 根拠: 1c の案は T96 と揃えた "… OR PERSONAL INJURY, IN EACH CASE WHERE APPLICABLE LAW DOES NOT PERMIT IT TO BE EXCLUDED, WHICH NOTHING IN SECTION 14 LIMITS" —— 修飾が 4 つの範疇のどれにも掛かることを語で示す。9b の "SUCH AS" の案（4 つを例示にする）は、外せない責任すべてを除外に入れて §14.2 の働く先を無くすので採らない（1c の判断）。逆側: いまの語順でも "LIABILITY … THAT" と読むのが自然
- §14.1 | 別の読み: 法が除外を許さないが制限は許す責任について、§14.1 の "WHICH NOTHING IN SECTION 14 LIMITS" は「§14 のどれも制限しない」、§14.2 第 1 文 "that liability is limited to the greatest extent that law permits" は「法の許す限り制限する」と読める | 一意 | 根拠: §14.1 の "WHICH NOTHING IN SECTION 14 LIMITS" が §14.2 を名指しで含む（§15.22 で「変えない」と決め、30 も同意・1c）。逆側: 名指しで含むことは、2 つの文が同じ責任に掛かる場面で §14.1 が勝つと読ませるが、§14.2 の文そのものはその場面を除かない
- §14.1 | 別の読み: "SPECIAL LOSS OR DAMAGE ARISING OUT OF THIS DEDICATION OR THE USE OF THE WORK" の "ARISING OUT OF …" が最後の "SPECIAL" だけに掛かる | 一意 | 根拠: §14.1 —— "LOSS OR DAMAGE" が名詞で、形容詞の列（DIRECT … SPECIAL）はどれもその名詞に掛かるので、修飾は名詞句の全体に掛かる
- §15.1 | 別の読み: "its words" の "its" が "the Work" を指す | 一意 | 根拠: §15.1 —— 文の主語が "This Dedication" で、"its words" はその Dedication の語（"is to be construed so as to give … that its words allow"）
- §16.2 | 別の読み: "the material it identifies" の "it" が "this Dedication" を指す | 一意 | 根拠: §16.2 —— 主語の "A notice a Dedicator places" を受け、"whether by its words, by its place in a comment within a file …" と通知の性質が続く
- §16.4 | 別の読み: "may be distributed under the name and the identifier if it is identified as a translation" の "it" が "the name" / "the identifier" を指す | 一意 | 根拠: §16.4 —— 文の主語が "A translation" で、"identified as a translation" は翻訳についてしか意味をなさない
- §16.5 | 別の読み: "the name and the identifier it bears" の "it" が "the identifier" を指す | 一意 | 根拠: §16.5 —— "first published this text under the name and the identifier it bears" で、名と識別子を帯びるのは "this text"
- §16.4 | 別の読み: "A modified text may not be distributed under any name that contains …" の "may not" を可能性（配られないかもしれない）と読む | 一意 | 根拠: 同じ条の直前の文 *"what is restricted is distributing one"* が禁止と述べ、末文 *"Both provisos are conditions upon distributing the text"* が条件と呼ぶので、禁止の読みに閉じる（2f の §1.266・Cowan 氏の「may not は読み違えられやすい」を当てた）
