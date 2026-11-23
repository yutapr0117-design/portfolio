---
file: LICENSES/ACD-1.5-CLARITY-TRIAL.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-23
canonical-ref: LICENSES/ACD-1.5-CHANGELIST.md (採否の規則「方針」と、採った変更の記録先) / LICENSES/ACD-1.5-DRAFT.txt (試作の対象・この file は草案を上書きしない) / LICENSES/ACD-1.4-THIRD-CLARITY-TRIAL.md (1.4 の試作の 3 冊目・§15.54 が 1.5 の候補の始まり)
---

# ACD-1.5 草案の試作

1.4 は 2026-11-23 に確定・凍結した。1.5 の草案に入れる変更の試作をここに書く。草案を上書きせず、試作ごとに Before / After、欠陥、逆側、測定（`measure_clause_overlap.py --compare`・`measure_clause_clarity.py`）、反例、採否を書く。**採否は `ACD-1.5-CHANGELIST.md` の「方針」の規則で決める** —— 各変更は閉じる errata / SELF-AUDIT の番号か、消す読みの分岐（`ACD-1.4-UNIQUE-READING.md` の行）を書く。例外は、読みを変えずに文を分けるか語を減らす変更だけ。

試作の番号は 1.4 の T1〜T134 に続けて **T135 から**（版をまたいで番号を重ねない）。節番号はこの file の中で §1 から。1.4 の試作の記録（`ACD-1.4-CLARITY-TRIAL.md`・`ACD-1.4-SECOND-CLARITY-TRIAL.md`・`ACD-1.4-THIRD-CLARITY-TRIAL.md`）は移さない。THIRD §15.54（文の長さ・S1〜S3）は 1.5 の候補として THIRD に残し、採るときはここに節を立てる。

## 1. T135 —— §11.4 第 2 文の網羅の言い切りを、黙示の排除に置き換える（−15 語・2026-11-23・案 5e・案 (c) は portfolio-cd）

**種**: `ACD-1.1-SELF-AUDIT.md` §3zd。§11.4 第 2 文 *"It reaches nothing else, save that the covenants in Section 5 are promises about the Dedicator's own conduct and are not limited by this sentence."* は、及ぶものを網羅すると言い切り、但し書きで §5 の約束だけを外す。この形が同じ型を 3 度生んだ —— E44（§16 は文書としての本文に及ぶ・1.4 草案で閉じた）、§2.5 の約束（2f の最終の通読・UNIQUE-READING の「§11.4 第 2 文の除外」の行・§11.1 第 2 文で閉じて一意）、T124 の §5.2 の回避の授権と放棄（約束でないので但し書きの外・SELF-AUDIT §3zd）。

| 案 | After（第 2 文） | 語 | 閉じるもの | 残るもの |
| :-- | :-- | --: | :-- | :-- |
| (a) | *"It reaches nothing else, save that Section 5 is not limited by this sentence."* | −11 | T124 | 網羅の言い切り（§2.5 の型は §11.1 第 2 文の読みで支え続ける）|
| (b) | （第 2 文を外す）| −25 | 3 件の型 | **黙示の許諾の排除が消える**（下の反例）|
| **(c)** | *"It gives nothing by implication beyond what its words give."*（2 巡目で動詞を *grants* から *gives* へ・下）| −15 | 3 件の型 | 黙示の許諾と黙示の約束の排除 |

**測定**（`measure_clause_overlap.py --compare`・1.5 草案の確定直後の形に当てた・2026-11-23）: 3 案とも、条 80 のまま、先行詞の無い指示語 0、許可の声が増えた条 0、そろえ残し 0、新しく入った全称の句 0、外向きの依拠 0。外した文に依拠する記録は 7（against-2 #279・errata E71・SELF-AUDIT L861・CHANGELIST-REVIEWS の 1 行・UNIQUE-READING の §5.2(b) / §11.1 / §11.4 の 3 行）—— どれも 1.4 の文を引く記録で、採るときに「1.5 で置き換えた」の注を足す。(c) の代名詞 *It* / *its* の先行詞は、直前の文の *"This Dedication, in respect of the Work"* から動かない。§5.2(d) の *"Section 11.4 is unaffected"* と §1.5 の *"which Section 11.4 addresses"* は第 3 文（許しを与えない）を指すので残る。

**反例（portfolio-cd・2026-11-23）**: (b) を退ける —— 1.4 の本文で黙示の許諾を外しているのは *"It reaches nothing else"* の 1 文だけで、*implied* / *estoppel* / *no other licence* の類いは §13 の保証の否認の *IMPLIED* を除いて 0 件（grep）。この文を外すと、§15.1（広い読みが勝つ）と組み合わさって、§4 の *use* の許諾から、§8.4 の限定の外の Dedicator の特許について、米国の黙示の特許許諾の議論に足場を与える。B7 は §8.4 の限定を B10 との意図した取引として守っているので、(b) は B7 の釣り合いを黙って動かす。

**(c) の逆側**: (i) *estoppel* を書かないのは §2.5（Dedicator が *estopped*）との混同を避けるためだが、そのぶん禁反言による許諾の排除は明示されない。(ii) 法が黙示の許諾や消尽を強行的に与える法域では、文で外せない（どの案でも同じ）。(iii) 第 1 文は網羅の主張を失い、「及ぶものの例示」に読まれうる。(iv) *"what its words give"* は、§2.5 の約束や §5.2 の授権のような「与える」でない文の扱いを読み手に委ねる —— ただしそれらは明示の語なので、黙示の排除の外に在る（cd）。(v) §15.6 *"no rule that construes a grant narrowly against the grantee"* と衝突しないか —— (c) は語の外の黙示を外す文で、§15.1 も *"that its words allow"* の中の読みなので、同じ線に立つ、と読む（5e）。(vi) 第 3 文の *"It grants no permission under the law of data protection …"* と並び、*It grants nothing … / It grants no permission …* の 2 文が続く —— 前者は量、後者は種類を限るので重ならない、と読む。

**反例の 2 巡目（portfolio-cd・2026-11-23）**: (1) *"what its words give"* の *give* は、ACD 自身の語の使い方で許諾より広い —— 約束（§8.6 *"This covenant is given on the same footing"*）、同意（§12.2 *"The covenant and the consent are given for every jurisdiction"*）、否認（§6.3 *"the disclaimer of reliance is given in every case"*）、前文の *"Each is given on its own terms"*、§11.1 の *"what any other Section of this Dedication gives"*。だから §5 の約束・§5.2 の授権・§12.2 の同意は「語が与えるもの」に入り、害は無い。**新しい反例**: そのため動詞の *grants* が目的語の *give* より狭く、黙示の許諾は外すが黙示の約束（行為から推定される不行使の約束など）は外さない → 動詞を *gives* にした（語数は同じ。逆側: *give* が 2 度続き、文体が硬い）。(2) 第 1 文が例示に読まれても、止まり先は 5 つ残る —— 第 3 文（データ保護・プライバシー等・他人の権利）、§11.1（商標・名）、§1.5 の除外の列（特許・商標・人格権・データ保護は Covered Rights の外）、第 1 文と §1.5 の *in respect of the Work* / *in the Work*（ほかの著作物へ伸びない）、§12.3（人格権の約束は他の作品へ及ばない）。残る隙は Dedicator の契約上の権利（配布サイトの利用規約など）だが、それは §5.2 の約束が自分の語で扱う。

**反例の 3 巡目（portfolio-cd・2026-11-23）**: 止める反例なし。(1) *It* と *its words* は第 1 文の *This Dedication* を受ける。(2) 法が与える黙示の許諾（米国の legal estoppel・特許の消尽）は文で外せず、外せるのは Dedication が黙示に与えるものだけ —— 旧文の *"reaches nothing else"* と同じ射程で、§8.4 の限定（B7）を広げも狭めもしない。(3) ドイツの目的移転の原則（UrhG 31 条 5 項）は、§4.1 が *"all Covered Rights"* を明示で許すので黙示に頼る場面が残らない。(4) §11.4 末文の *"states a limit of the Dedication's reach"* は、第 3 文が限界を述べ続けるので真のまま。**逆側 (vii)**: *"gives nothing by implication beyond what its words give"* は、本文の外の Dedicator の言動（「学習に自由に使ってよい」という公の発言など）から受け手が得る禁反言の防御まで、完全合意条項（entire agreement）のように締め出すと読まれる余地がある。主語は Dedication なので、Dedication の外の言動が与えるものには及ばない、と読むのが自然で、§2.5 も本文の内から禁反言を支える —— この文は「本文が黙示に与えるもの」を限る文であって、完全合意条項ではない、と読む（法律家への問いの材料）。

**4 巡目 —— 決める側の文で当て直した（portfolio-d7 の採掘・2026-11-23。引用はアーカイブの写しで原文に当てた）**:

- **反例（重い）**: Pamela Chestek 氏 2022-07（委員長・`license-review`・Open Logistics License）は、OLL の *"Under no circumstances will anything in this Section 3 be construed as granting, by implication, estoppel or otherwise, a license to any patent …"* に *"What is this sentence designed to do? The grant clause defines the grant … It's not necessary to say that there is no grant of what is not granted."* と問うた。T135 の新しい文も、置き換えた旧文（1.0 から在る *"It reaches nothing else"*）も、この型（与えないものを与えないと言う文）に在る。
- **反例（中）**: Bruce Perens 氏 2012-02（CC0 の審査）は、献呈では黙示の特許許諾（禁反言）が立ちにくい、と読んだ。§8 が届かない請求項について、BSD や MIT なら立ちうる黙示の許諾まで、ACD は文で外すと読まれうる。
- **支え**: 承認済みのライセンスが同じ型の文を持つ —— BSD+Patent（2017 承認）*"Except as expressly stated above, no rights or licenses from any copyright holder or contributor is granted under this license, whether expressly, by implication, estoppel or otherwise."*、EPL-2.0 の同じ型の文。

**読み**: Chestek 氏の問いと Perens 氏の読みは、T135 の前の文にも同じく当たる。旧文は「及ぶのは列挙したものだけ」と言い切ることで、黙示の許諾を外していたからである（cd の 3 巡目の (2): 射程は同じ）。だから T135 はこの点を悪くしていない。黙示の排除を BSD+Patent・EPL-2.0 と同じ型の 1 文に寄せ、−15 語で網羅の言い切りが生んだ型（E44・§2.5・T124）を閉じた。**逆側**: 委員長の問いに正面から答えるなら、黙示の排除の文そのものを外す道（試作 §1 の (b)）がある。だが cd の反例のとおり、1.4 でこの働きを持つのはこの 1 文だけで、外すと §8.4 の限定（B7）の外の特許へ黙示の議論の足場を与える。委員長の *"What is this sentence designed to do?"* には、「§8.4 が意図して限った特許の許諾を、黙示によって広げさせないため」と答える。この答えは入口（`REVIEWERS.md` の §8 の説明）に置く候補である（cd へ）。

**採否**: **採った**（2026-11-23・(c) の *gives* の形・−15 語・草案 5,879 → 5,864 語）。`CHANGES-ACD-1.5.txt` に 1 行、`ACD-1.5-CHANGELIST.md` の表に 1 行、草案冒頭の状態の行を「1.4 と同一」から「一覧の変更を除いて 1.4 の本文」へ。規則 1 の欄には SELF-AUDIT §3zd を書く。採るなら、`CHANGES-ACD-1.5.txt` に 1 行、`ACD-1.5-CHANGELIST.md` の表に 1 行、草案冒頭の語数を `sync_stated_counts.py --apply` で直す。

## 2. 決める側の文から作った点検の観点を 1.4 の本文に当てた（2026-11-23・観点は portfolio-d7 の採掘・当ては 5e）

| 観点（出典） | 1.4 の本文 | 結果 |
| :-- | :-- | :-- |
| 定義は *means* で書き、違う語は違う意味と読まれる（Chestek 氏 2025-07-19・委員長）| §1.1〜§1.10 はすべて *means* | 満たす |
| 許可は *permission* として書き、受動態で書かない（Perens 氏 1999-06-16・07-13）| 許可の文の受動態は 16 文。主たる許諾で許す者が書かれていないのは §6.1 *"Computational Use of the Work is expressly permitted"* だけ | 立たない —— THIRD §15.45 の 9 巡目が行為者を文脈（Dedicator）で一つに決め、§6 が独立の足場か宣言的かは T108 と UNIQUE-READING の §6.5 の行で閉じている。能動にする案（*"The Dedicator expressly permits Computational Use of the Work, …"*・+1 語）は分岐を閉じず、文を分けず語も減らさないので、方針の規則 1 で入らない |
| 同じことを別の文で言い直すと解釈が割れる（Rosen 氏 2002-08-01）| 「§16 は Work の利用への条件でない」が 4 か所、「限界であって条件でない」が 2 か所 | 当てた —— `ACD-1.4-CLARITY-TRIAL.md` §4.1（F2 の試作 (b)）で、どれも条件か否かの曖昧さをその場で閉じる働きを持つと読んで不採用。Chestek 氏・Rosen 氏 2021-06-09（3D Slicer: ある句が許諾の条件かが問われた）は残す側の根拠 |
| 否認は目立つ形で（Smith 氏 2025-12-05）| §13.1・§13.2・§14.1 は大文字 | 満たす |
| *term* は期間の合意と読まれ、一部の法域で解約できる（Piana 氏 2025-02-24）| §3.2 *"for the full term for which the Covered Rights would otherwise subsist"*（権利の存続期間）、§1.10 *"contractual term"*、§2.2 *"further term, condition, or restriction"* | 反例の担当（portfolio-cd）へ —— §3.2 の *term* は権利の存続期間で合意の期間ではない、と読むが、§2.2 の撤回不能と組み合わせて当てる |

## 3. T136 —— §4.1 と §8.1 の *perpetual* を、権利の存続期間に結ぶ（+17 / +35 語・2026-11-23・種は portfolio-cd・起草 5e・**採らない**）

**種**: Carlo Piana 氏 2025-02-24（`license-review`・ModelGo Zero）は、期間の定めの無い合意は一部の法域で相当の予告により解約できると書いた（本人は *"not probably something relevant to the approval"* と前置きした）。cd が原文を読み、ACD-1.4 でそれに一番近いのは §3.2 の *term*（権利の存続期間で、合意の期間ではない）ではなく、§4.1 と §8.1 の *"irrevocable, perpetual"* だと当てた。期間の定めの無いことをそのまま名乗る語である。EU 法の下で起草された EUPL は *"for the duration of copyright vested in the Original Work"*（`license-review` 2008-03 に出た本文）、CC0 の予備の許諾は *"for the maximum duration provided by applicable law or treaty (including future time extensions)"*（`license-discuss` 2024-04 に引かれた本文）と書き、どちらも *perpetual* を使わない（どちらもアーカイブの写しで原文に当てた・2026-11-23）。

**消す読みの分岐**: §4.1 の許諾は期間の定めの無い許諾で、期間の定めの無い約束を当事者が予告で解約できるとする法域では Dedicator の予告で終わる —— 対して、権利が存続する間という期間の定めのある許諾である。§2.2（撤回不能）と §10.4（*"No permission granted by this Dedication terminates under it"*）は文書の中の仕組みを述べる文で（T81 の *under it*）、法が当事者に与える解約の権利を外せない。大陸法の面（フランス民法の期間の定めの無い約束の条など）は**我々の読みで、原典の写しは未取得** —— Légifrance は 2026-11-23 の自動取得を 403 で拒んだ。

| 案 | §4.1 の After | §8.1 の After | 語 |
| :-- | :-- | :-- | --: |
| (A) §3.2 の形 | *"… irrevocable, sublicensable, and transferable licence, for the full term of each Covered Right, including any extension, restoration, or revival of term, to exercise …"* | *"… irrevocable, sublicensable, and transferable licence, for the full term of each patent claim under which it is granted, including any extension or restoration of that term, to make, …"* | +15 / +20 |
| (B) 短い形 | *"… licence, for as long as the rights it covers subsist, to exercise …"* | *"… licence, for as long as the patent claims it covers subsist, to make, …"* | +8 / +9 |

**逆側**: (i) Apache-2.0 は *"perpetual, worldwide, … irrevocable"* で承認済みで、イタリアを含む欧州で広く使われている —— 実務で解約の争いが起きた記録を我々は持たない。(ii) Rosen 氏 2003-08-27 は *perpetual* を「今の意図の表明」として擁護した（`jurisdictions.md` 5a の 2003 の段）。外すと、その意図の表明を失う。(iii) Piana 氏の指摘は 1 人の法律家の自国の読みで、承認に関係しないと本人が書いた。(iv) B3 に逆らう（(A) で +35 語・(B) で +17 語）。(v) (B) の *"for as long as … subsist"* は、権利が一度消えて回復した場合（期間の回復）に許諾が戻るかを語で決めない —— (A) はそれを §3.2 と同じ語で閉じるが長い。(vi) 期間を権利の存続に結んでも、それが期間の定めのある約束と扱われるかは法域の判断で、文で決められない（法律家への問い）。(vii) 米国の読み手には「なぜ perpetual を外したか」の説明が要り、外したこと自体が狭めたと読まれうる（`SUBMISSION-MATERIALS.md` の「差だけを読む人が「狭めた・条件を足した」と読みうる箇所と、その 1 行の注」の表に足す対象）。

**反例の 2 巡目（portfolio-cd・2026-11-23）—— 採らない理由が 2 つ増えた**: (viii) **回復の穴は (B) だけでなく、*perpetual* を外すこと自体の費用である。** §4.1 は *"all Covered Rights"*（§1.5 *"now or in future … whether or not presently subsisting"*）を *perpetual* で許すので、権利が一度消えて回復しても（米国の 17 U.S.C. §104A の回復、EU の保護期間の調和で復活した権利、特許の期間の回復や SPC）許諾は語の上で途切れない。(B) はそこに空白の読みを生み、(A) は §3.2 と同じ語で閉じるが、1 語で済んでいたことを +35 語で作り直すだけである。(ix) **期間に結んでも、期間の無い権利が残る。** Covered Rights は *"rights against unfair extraction"* と *"any right of similar effect"* を含み、不正競争の側の権利には法定の存続期間が無く、sui generis のデータベース権は相当の投資のたびに新しい期間が始まる。だから (A) でも (B) でも、消そうとした読みの分岐（期間の定めの無い許諾として予告で解約できる）は閉じきれない。EUPL の *"for the duration of copyright"* が成り立つのは EUPL が著作権だけを許す文書だからで、Covered Rights が著作権より広い ACD には同じ語を移せない。(x) (A) の +35 語は、1.5 で T135 が得た −15 の 2 倍を戻す変更で、しかも (ix) のとおり分岐を閉じきれない。

**採否**: **採らない**（2026-11-23・5e と cd）。規則 1 の欄に書いた分岐を、どの案も閉じきれないため。法律家への問いとして `QUESTIONS-FOR-COUNSEL.md` の問い 1 に (k) を足した（期間の定めの無い許諾は予告で解約できるとする法域で §4.1・§8.1 が服するか、服するなら存続期間の無い Covered Rights を含む ACD で EUPL の形が効くか）。不利な事実としては portfolio-cd が `against.md` に記録し、潰し方を「T136 は採らず、法律家への問いへ」とする。規則 1 の欄には上の「消す読みの分岐」を書く。採るなら §8.4 は *"on the terms of Section 8.1"* で同じ期間を受ける。

## 4. T137 —— §5.2 末段の 68 語の文を、サービスの文を先にして分ける（+10 語・2026-11-23・THIRD §15.54 の S3・**採らない**）

**方針の欄**: 規則 1 の例外（読みを変えずに文を分け、45 語超の文が減るもの）として当てた。測定（1.5 草案・`measure_clause_clarity.py`）: 191 → 192 文、45 語超 28 → 27、+10 語（34 語と 44 語の 2 文）。`--compare`: 先行詞の無い指示語 0、*Nor does it reach* の *it* は *Section 5*、外向きの依拠 1（`QUESTIONS-FOR-COUNSEL.md` の問い 5 の第 3 の問いが *"ACD-1.4 says …"* と 1.4 を引く —— 1.4 の引用としては真のまま）、468r・468d の目印は欠けない。

**限定句と名指しの語の表**（portfolio-cd の条件）:

| 元の文の語 | 元の掛かり先 | 分けた後の掛かり先 | 同じか |
| :-- | :-- | :-- | :-- |
| *other than the Work* | 素材 | 第 2 文の素材 | 同じ |
| *that the Dedicator itself makes or makes available* | 素材 | 第 2 文の素材 | 同じ |
| *without providing a copy of the Work* | サービス | 第 1 文のサービス | 同じ |
| *even where using that material is a Computational Use of the Work* | 文末で全体に掛かりうるが、語は素材を名指す | 第 2 文の素材 | 同じ |
| 次の文の **those terms**（*"Section 5 reaches those terms to the extent they restrict what may be done with that copy"*） | *"the terms or measures the Dedicator applies to that material or to the use of a service …"* —— 素材の条件とサービスの条件の両方 | 最も近い *terms* は第 2 文の素材の条件だけ | **狭まる** |

**採らない理由**: 分けると *those terms* の先行詞からサービスの条件が落ち、Dedicator が API の利用規約などで、受け手が素材の中に持つ Work の写しの扱いを縛る場面が §5 の外に出る読みが立つ。直す語（*those terms* → *"the terms that the two preceding sentences describe"*）を足すと +16 語で、45 語超の文を 1 つ減らすための費用として重い。**逆側**: サービスは写しを渡さずに Work を動かすものなので、サービスの条件が「その写し」を縛る場面は狭い、と読む余地もある —— だがその読みに頼るなら、分ける前の文のほうが確かである。**方針が働いた例**: cd が足した「限定句と名指しの語を表で示す」条件が、語を足さない分割に見えた変更の狭まりを捕まえた。

## 5. T138 —— §5.2(b) に、偽りの言明をしない義務だけを除外として足す（+14 語・2026-11-23・errata E87・起草 5e・**採らない**）

**種**: errata E87。§5.1・§5.2(b)・§5.2(d) の除外の列を並べた（SELF-AUDIT §3zd の一般形「後から入った変更が別の条の列を古くする」の当て直し）。

| 条 | 除外 |
| :-- | :-- |
| §5.1 第 2 文 | 特許（§8）・商標と名（§11.1）・偽りの言明と表示（§11.3）・合意した支払い |
| §5.2(b) | 商標と名（§11.1・T104）・合意した支払い（T112・T118）—— **偽りの言明と表示が無い** |
| §5.2(d) | 偽りの言明と表示（§11.3）|

§5.2(b) は Dedicator が *"impose by contract, terms of service, … an obligation in respect of the Work that this Dedication does not itself impose"* をしないと約束する。偽りの帰属や推奨をしない義務は本 Dedication が課さない（§11.3 *"not a condition upon You"*）ので、利用規約の「当方が書いた・推奨したと示さないこと」の 1 行が約束に反すると読める。1.0〜1.3 は §5.1 も除外を持たなかったので 2 つの条は揃っていたが、1.4 が §5.1 にだけ偽りの言明の除外を足して非対称になった。

**After**（§5.2(b) の末尾）: *"… an obligation in respect of the Work that this Dedication does not itself impose, **other than an obligation not to make a false statement or representation (Section 11.3)**, and this Dedication imposes none (Section 10.1);"*（+14 語）。

**測定**（`--compare`・1.5 草案）: 条 80、指示語 0、許可の声 +0、そろえ残し 0、全称 0、外向きの依拠 0（記録 1: errata E81 が 1.0〜1.3 の文を引く）。45 語超の文は 28 のまま（(b) は列の中の項で、道具は §5.2 の頭から (d) までを 1 文に数えない）。

**限定句の表**: §5.2(b) に足す句は *an obligation* を名指し、*not to make* の否定の形に限る —— 改変した版に印を付ける義務（§10.2 が要らないと言う）のような**積極の義務**は入らない。§5.2(b) の *"in respect of the Work"* と *"that this Dedication does not itself impose"* の掛かり先は変わらない。

**逆側**: (i) 契約上の義務は、偽りの表示の法だけでは得られない救済（契約違反の損害）を Dedicator に足す。(ii) §5.2(b) は、利用規約が裏口から条件を足すのを止める唯一の条で、除外を足すたびに狭まる。(iii) (b) の頭に既に *"other than under trademark rights … or for a payment …"* が在り、同じ項に *other than* が 2 度出る（頭は約束からの除外、末尾は義務からの除外）。(iv) 同じことを法が既に禁じているので、契約で重ねる必要は無い、と読む審査者もいる（Fogel 氏 2014-06-30 *"I worry about building trademark-law-type provisions into licenses that are really about copyright"*・`review-readings-6.md` §1.459）。(v) 変えない場合の費用は、採用者が標準の利用規約を写して知らずに約束を破ること —— 本文でなく採用者向けの案内（ADOPTING.md）で知らせる道もある。

**反例（portfolio-cd・2026-11-23）**: (A) **法か契約か** —— §5.1 の除外は、Dedicator が「法が既に与える請求」（詐称・不正競争・虚偽の推奨）を主張できる、という除外で、§11.3 も「Dedication はそこに及ばない」と言うだけで法の側を残す。§5.2(b) は「Dedication が課さない義務を契約・利用規約で新しく課さない」約束で、守っているのは新しい義務の経路を作らないこと。この線で読めば 2 つの条は同じ向きで一貫している。T138 は契約の経路を開け、しかも開ける先は「偽りの言明または表示」という輪郭のあいまいな範囲で、何が表示に当たるかを Dedicator が書く利用規約の側が決めることになる —— §10.1 の「受け手に何も課さない」に、契約で課せる義務の型が 1 つ増える。(B) 推奨を装わない条項の多くは名か商標を使うので、(b) の頭の除外（*"under trademark rights or rights in a name"*）が既に覆う。T138 が効くのは名を使わない偽りの表示だけで、その場合も §5.1 と §11.3 により法の請求は残る —— 利用規約の 1 行が約束違反になっても、Dedicator が失うのは契約上の二重の救済だけ。(C) E87 の番号は書けるが、(A) のとおり欠陥とは言い切れず、+14 語は閉じた欠陥でなく開けた経路に払う語になる。

**採否**: **採らない**（2026-11-23・5e と cd）。E87 は「検証して直さないと決めた」（E6 と同じ扱い）とし、採用者には `ADOPTING.md` で「利用規約に推奨を装わない条項を入れるなら名か商標に結びつけること。名を使わない偽りの表示には、契約でなく法で対する（§5.1・§11.3）」と知らせる（cd）。**逆側**: 「直さない」が E6 に続いて 2 件目になる。標準の利用規約をそのまま使う採用者は、ADOPTING を読まない限り違反に気づかず、§5.3 の受益者の主張の種になりうる。

## 6. 前文（326 語）を本文から外す案 —— 試作に起こさず退ける（2026-11-23・5e）

**種**: Pamela Chestek 氏 2020-12-26（`license-review`・OIN License）*"I've marked up the license to omit non-operative language below. If the words aren't meant to have any effect, they shouldn't be there. The only thing that can happen is that the words will be used in ways that create unintended consequences, so it's best just not to have them at all."*（採掘は portfolio-d7・`review-readings-6.md` §1.461）。ACD の前文は自分を *"informative; not part of the operative terms"* と言う 326 語で、外せば題名からの語数は 5,864 から約 5,538 へ下がる（B3）。

**退ける理由 —— 同じスレッドの審査者が、主張の文を前文へ移せと勧めていた**（どれもアーカイブの写し `license-review` 2020-12 で原文に当てた）:

- Roland Turner 氏 2020-12-27（同じ OIN のスレッド）: *"The usual way to handle this in the construction of legal instruments is to shift statements of principle into a preamble, either a section specifically headed Preamble (e.g. Gnu licenses) or more traditionally a section starting with the word "whereas" which contains a series of statements of belief (recitals). Either is fine"*、*"Without this relationship, a court is going to have real trouble discerning the intentions of the parties."*
- Russ Nelson 氏 2020-12-27（同じ OIN のスレッド）: *"If it's not a restriction, it does not belong in the license. It might go into a preamble, but it should be phrased in the form of encouragement, not agreement."*
- Chestek 氏が外せと言ったのは、OIN の本文で *"The context of this license includes"* の段落が *includes* によって作用の範囲に入りうる位置にあり、隣の段落が非作用と定義されていた —— 作用か否かが読み手に決められない語である（同じ通の続き *"You have created a document that is unclear"*）。ACD の前文は見出しで作用の条から分けられ、最後の文 *"This preamble is not, and nothing in it qualifies them."* と §1.1 の *"comprising Sections 1 to 16"* が、作用しないことを本文の側からも決める（UNIQUE-READING の §1.1 の行）。

**読み**: 前文は Turner 氏が勧めた形（GPL の *Preamble* の型）に在り、Chestek 氏の文が向いた形（作用の段落に混ざった非作用の語）には無い。外すと、なぜ 3 つの足場を並べるかの説明が本文から消える（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.25 は、§8.6 の説明を外した T20 の後、その説明を前文が持つとして前文第 3 段落を残した）。**逆側**: (i) 前文の第 1 段落は、承認済みのライセンスと献呈の現状についての経験の言明（*"Permissive licences are silent on whether a work may be used to train a model"*・*"dedications to the public domain either withhold patent rights expressly or say nothing about them at all"*）を持ち、審査者が出典を問いうる —— 前文に置いても、本文に経験の主張を持つ費用は残る（T79 が §6.5 で出典の無い経験の言明を分析の言明へ替えたのと同じ型）。(ii) Nelson 氏の *"phrased in the form of encouragement, not agreement"* に照らすと、前文の *"It gives away, once and without conditions, every right it reaches"* は約束の形に近い。どちらも試作の種として残す（第 1 段落の経験の言明に出典を付けるか、分析の言明に替えるか）。

**この節の位置**: 方針の規則 1 の例外（読みを変えずに語を減らす）に形の上では当たるが、上の審査者の文が「外さない」側の根拠になるので、試作に起こさない。前文の語を減らす候補は、逆側 (i) の第 1 段落の言明に限って当て直す。

## 7. T139 —— 前文の「献呈は特許を留保するか沈黙する」を、広く使われている献呈に限る（+3 語・2026-11-23・errata E88・種は portfolio-d7・**採らない**）

**種**: errata E88。前文第 1 段落の *"And dedications to the public domain either withhold patent rights expressly or say nothing about them at all, and both leave the recipient of software exposed."* は全称で、特許を扱う献呈が `license-discuss` で論じられていた —— Engel Nyst 氏 2013-08-24 *"Custom Dedication: Open Source is a modified CC0 that addresses the patent rights issue."*（アーカイブの写しで原文に当てた）、Joe Kua 氏 2014-12-04 の同じ道具についての問い（`review-readings-2.md` §1.243 が Woolley 氏の返信を読んでいる）。ACD 自身も特許を許諾する献呈である。§6 で退けた前文の逆側 (i)（第 1 段落の経験の言明）が、反例の出る形で当たった。

**After**: *"And dedications to the public domain **in common use** either withhold patent rights expressly or say nothing about them at all, …"*（+3 語・題名からの数。`measure_clause_overlap.py` は作用の条だけを数えるので差 0）。段落の第 2 文 *"The legal tools in common use were drafted …"* と同じ限定にそろえる。

**測定**（`--compare`）: 条 80、作用の条の語 ±0、指示語 0、外向きの依拠 0（記録 2: errata E85・E88 が 1.0〜1.4 の文を引く）。

**逆側**: (i) *in common use* もまた実務についての言明で、ドシエは使用を測っていない —— 念頭に置くのは CC0（4(a) で特許を留保）と Unlicense（沈黙）。(ii) 前文は作用しない（*"nothing in it qualifies them"*）ので、直さなくても受け手の得るものは変わらない。費用は「審査者が反例を 1 つ知っていれば偽と言える文」を本文に持つこと。(iii) 前文の語を増やすのは、§6 で「前文を外す」案を退けた理由（原理の表明の置き場）とは別の向きの費用で、+3 語は B3 に逆らう。

**反例（portfolio-cd・2026-11-23）**: (1) 文脈がもう限っている —— 第 1 段落の主題文は *"The legal tools in common use were drafted for a world …"* で、*"That assumption now fails in three places at once"* に続く 3 つの言明（機械生成物・許容型の沈黙・献呈の特許）は、どれもその道具についての言明と読むのが自然である。全称の読みは文を段落から切り出したときにだけ立つ。(2) 同じ型の 2 文目 —— *"Permissive licences are silent on whether a work may be used to train a model"* も切り出せば全称で、学習を名指す AI 向けのライセンスという反例がある。T139 が 3 文目だけに *in common use* を足すと、足していない 2 文目は全称だという対比の読みが生まれる（語を 1 か所だけそろえると対比が立つ型）。(3) 直すなら限定を 1 度で 3 文に掛ける形（*"In the tools in common use, that assumption now fails in three places at once"*・+5 語前後）だが、前文は作用せず、*in common use* も実務についての言明として残るので、閉じる分岐が小さい。

**採否**: **採らない**（2026-11-23・5e と cd）。errata E88 に 2 文目も入れ、「文脈（第 1 段落の主題文）が限っている。切り出した読みにだけ当たる」として直さないと決めた。**逆側**: 「直さない」は E6・E87 に続き 3 件目になる。1 文だけを引く審査者には、その文は偽に見える。
