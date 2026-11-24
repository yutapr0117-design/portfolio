---
file: LICENSES/ACD-1.5-CLARITY-TRIAL.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.5-CHANGELIST.md (採否の規則「方針」と、採った変更の記録先) / LICENSES/ACD-1.5-DRAFT.txt (試作の対象・この file は草案を上書きしない) / LICENSES/ACD-1.4-THIRD-CLARITY-TRIAL.md (1.4 の試作の 3 冊目・§15.54 が 1.5 の候補の始まり)
---

# ACD-1.5 草案の試作

1.4 は 2026-11-23 に確定・凍結した。1.5 の草案に入れる変更の試作をここに書く。草案を上書きせず、試作ごとに Before / After、欠陥、逆側、測定（`measure_clause_overlap.py --compare`・`measure_clause_clarity.py`）、反例、採否を書く。**採否は `ACD-1.5-CHANGELIST.md` の「方針」の規則で決める** —— 各変更は閉じる errata / SELF-AUDIT の番号か、消す読みの分岐（`ACD-1.4-UNIQUE-READING.md` の行）を書く。例外は、読みを変えずに文を分けるか語を減らす変更だけ。

試作の番号は 1.4 の T1〜T134 に続けて **T135 から**（版をまたいで番号を重ねない）。節番号はこの file の中で §1 から。1.4 の試作の記録（`ACD-1.4-CLARITY-TRIAL.md`・`ACD-1.4-SECOND-CLARITY-TRIAL.md`・`ACD-1.4-THIRD-CLARITY-TRIAL.md`）は移さない。THIRD §15.54（文の長さ・S1〜S3）は 1.5 の候補として THIRD に残し、採るときはここに節を立てる。S3 は §4（T137）、S1・S2 は §8（T140・T141）で決め、THIRD §15.54 の 1.5 の候補はどれも採らないで終わった（2026-11-24）。

## 1. T135 —— §11.4 第 2 文の網羅の言い切りを、黙示の排除に置き換える（−15 語・2026-11-23・案 5e・案 (c) は portfolio-cd）

**種**: `ACD-1.1-SELF-AUDIT.md` §3zd。§11.4 第 2 文 *"It reaches nothing else, save that the covenants in Section 5 are promises about the Dedicator's own conduct and are not limited by this sentence."* は、及ぶものを網羅すると言い切り、但し書きで §5 の約束だけを外す。この形が同じ型を 3 度生んだ —— E44（§16 は文書としての本文に及ぶ・1.4 草案で閉じた）、§2.5 の約束（2f の最終の通読・UNIQUE-READING の「§11.4 第 2 文の除外」の行・§11.1 第 2 文で閉じて一意）、T124 の §5.2 の回避の授権と放棄（約束でないので但し書きの外・SELF-AUDIT §3zd）。

| 案 | After（第 2 文） | 語 | 閉じるもの | 残るもの |
| :-- | :-- | --: | :-- | :-- |
| (a) | *"It reaches nothing else, save that Section 5 is not limited by this sentence."* | −11 | T124 | 網羅の言い切り（§2.5 の型は §11.1 第 2 文の読みで支え続ける）|
| (b) | （第 2 文を外す）| −25 | 3 件の型 | **黙示の許諾の排除が消える**（下の反例）|
| **(c)** | *"It gives nothing by implication beyond what its words give."*（2 巡目で動詞を *grants* から *gives* へ・下）| −15 | 3 件の型 | 黙示の許諾と黙示の約束の排除 |

**測定**（`measure_clause_overlap.py --compare`・1.5 草案の確定直後の形に当てた・2026-11-23）: 3 案とも、条 80 のまま、先行詞の無い指示語 0、許可の声が増えた条 0、そろえ残し 0、新しく入った全称の句 0、外向きの依拠 0。外した文に依拠する記録は 7（against-2 #279・errata E71・SELF-AUDIT L861・CHANGELIST-REVIEWS の 1 行・UNIQUE-READING の §5.2(b) / §11.1 / §11.4 の 3 行）—— どれも 1.4 の文を引く記録で、採るときに「1.5 で置き換えた」の注を足す。(c) の代名詞 *It* / *its* の先行詞は、直前の文の *"This Dedication, in respect of the Work"* から動かない。§5.2(d) の *"Section 11.4 is unaffected"* と §1.5 の *"which Section 11.4 addresses"* は第 3 文（許しを与えない）を指すので残る。

**反例（portfolio-cd・2026-11-23）**: (b) を退ける —— 1.4 の本文で黙示の許諾を外しているのは *"It reaches nothing else"* の 1 文だけで、*implied* / *estoppel* / *no other licence* の類いは §13 の保証の否認の *IMPLIED* を除いて 0 件（grep）。この文を外すと、§15.1（広い読みが勝つ）と組み合わさって、§4 の *use* の許諾から、§8.4 の限定の外の Dedicator の特許について、米国の黙示の特許許諾の議論に足場を与える。B7 は §8.4 の限定を B10 との意図した取引として守っているので、(b) は B7 の釣り合いを黙って動かす。

**(c) の逆側**: (i) *estoppel* を書かないのは §2.5（Dedicator が *estopped*）との混同を避けるためだが、そのぶん禁反言による許諾の排除は明示されない。(ii) 法が黙示の許諾や消尽を強行的に与える法域では、文で外せない（どの案でも同じ）。(iii) 第 1 文は網羅の主張を失い、「及ぶものの例示」に読まれうる。(iv) *"what its words give"* は、§2.5 の約束や §5.2 の授権のような「与える」でない文の扱いを読み手に委ねる —— ただしそれらは明示の語なので、黙示の排除の外に在る（cd）。(v) 1.4 の §15.6 の、許諾を受け手に不利に狭く読む規則を外す文 と衝突しないか —— (c) は語の外の黙示を外す文で、§15.1 も *"that its words allow"* の中の読みなので、同じ線に立つ、と読む（5e）。(vi) 第 3 文の *"It grants no permission under the law of data protection …"* と並び、*It grants nothing … / It grants no permission …* の 2 文が続く —— 前者は量、後者は種類を限るので重ならない、と読む。

**反例の 2 巡目（portfolio-cd・2026-11-23）**: (1) *"what its words give"* の *give* は、ACD 自身の語の使い方で許諾より広い —— 約束（§8.6 *"This covenant is given on the same footing"*）、同意（§12.2 *"The covenant and the consent are given for every jurisdiction"*）、否認（§6.3 *"the disclaimer of reliance is given in every case"*）、前文の *"Each is given on its own terms"*、§11.1 の *"what any other Section of this Dedication gives"*。だから §5 の約束・§5.2 の授権・§12.2 の同意は「語が与えるもの」に入り、害は無い。**新しい反例**: そのため動詞の *grants* が目的語の *give* より狭く、黙示の許諾は外すが黙示の約束（行為から推定される不行使の約束など）は外さない → 動詞を *gives* にした（語数は同じ。逆側: *give* が 2 度続き、文体が硬い）。(2) 第 1 文が例示に読まれても、止まり先は 5 つ残る —— 第 3 文（データ保護・プライバシー等・他人の権利）、§11.1（商標・名）、§1.5 の除外の列（特許・商標・人格権・データ保護は Covered Rights の外）、第 1 文と §1.5 の *in respect of the Work* / *in the Work*（ほかの著作物へ伸びない）、§12.3（人格権の約束は他の作品へ及ばない）。残る隙は Dedicator の契約上の権利（配布サイトの利用規約など）だが、それは §5.2 の約束が自分の語で扱う。

**反例の 3 巡目（portfolio-cd・2026-11-23）**: 止める反例なし。(1) *It* と *its words* は第 1 文の *This Dedication* を受ける。(2) 法が与える黙示の許諾（米国の legal estoppel・特許の消尽）は文で外せず、外せるのは Dedication が黙示に与えるものだけ —— 旧文の *"reaches nothing else"* と同じ射程で、§8.4 の限定（B7）を広げも狭めもしない。(3) ドイツの目的移転の原則（UrhG 31 条 5 項）は、§4.1 が *"all Covered Rights"* を明示で許すので黙示に頼る場面が残らない。(4) §11.4 末文の、及ぶ範囲の限界を述べると言う語 は、第 3 文が限界を述べ続けるので真のまま。**逆側 (vii)**: *"gives nothing by implication beyond what its words give"* は、本文の外の Dedicator の言動（「学習に自由に使ってよい」という公の発言など）から受け手が得る禁反言の防御まで、完全合意条項（entire agreement）のように締め出すと読まれる余地がある。主語は Dedication なので、Dedication の外の言動が与えるものには及ばない、と読むのが自然で、§2.5 も本文の内から禁反言を支える —— この文は「本文が黙示に与えるもの」を限る文であって、完全合意条項ではない、と読む（法律家への問いの材料）。

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
| 条件か非条件かの曖昧さは、どちらかへ明確な語で解け（Carlo Piana 氏 2024-10・Accountable Resolver の審査・*"I would therefore suggest to resolve the possible controversial interpretation with clearer wording in either direction"*）。対して Turner 氏 2020-12-27 は、条件の形で書いて次の文で引っ込める形を *"invites abuse"* とした | §16.4 末文 *"Both provisos are conditions upon distributing the text, not upon any use of the Work (Section 10.5)."*（cd が Turner 氏の型に見えうると指摘）| 変えない —— 2 つの但し書き（訳と再符号化の表示）が条件である対象（本文の頒布）と、条件でない対象（Work の利用）を 1 文で分ける文で、Piana 氏の「どちらかへ明確に」に答える形。条件を言ってから打ち消すのではない。但し書きは本文の名と識別子についてだけで、使用や使用者を名指さないので、非条件の宣言でも内容で OSD 5・6 に当たる型（Smith 氏 2020-02）にも当たらない（採掘は portfolio-d7） |
| 念押しの明確化は混乱を生む（Chestek 氏 2020-12-26・OIN・*"or even used for commercial purposes"* について *"the attempted clarification only creates confusion"*）| §6.1 *"for any purpose, whether or not commercial"* | 立たない —— Chestek 氏が問うたのは *or even* が商用を例外のように響かせる形で、*whether or not commercial* は両方を同じ重さで言う。承認済みの Unlicense も *"for any purpose, commercial or non-commercial"* と書く。**逆側**: *for any purpose* だけで足りるので、3 語は B3 の費用で、閉じる分岐は無い（削る案は方針の例外「読みを変えずに語を減らす」に当たるが、計算利用の条で商用を明示する読み手の便を失う） |
| 同じことを違う語で書くと、挑む側が違いを探す（Chestek 氏 2022-07-04・当ては portfolio-cd・2026-11-23）| 「法が許す限り」の言い回し 5 種 —— (a) *"to the fullest extent the law permits"*（§2.8・§5.2 の授権・§5.3・§6.4・§12.4）、(b) *"to the fullest extent permitted by the law of each jurisdiction"*（§3.1・§12.1）、(c) *"TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW"*（§14.1）、(d) *"to the greatest extent that law permits"*（§14.2・*that law* は直前の *applicable law*）、(e) *"to the fullest extent the Dedicator is able"*（§6.3・別の概念） | 分岐なし —— (b) は放棄と献呈を法域ごとに働かせる意図した区別、(c)(d) は責任の制限の定型とその後半、(e) は他人の留保を撤回する力の限度で別の概念。違いを探されうるのは (a) の *the law*（どの法か）と (b) の対だが、§15.3（準拠法も法廷地も定めない）と並べれば (a) も各法域の法と読むのが自然。(d) の *greatest* を *fullest* に揃えても 0 語で効果は変わらないが、errata も読みの分岐も書けないので方針の規則 1 で入らない。法律家への問いの候補: (a) の *the law* は §15.3 の下で各法域の法と読まれるか |
| 許容型・献呈型に版の引き上げ条項（*or any later version*・新しい版の条）を求めるか（種は 5e・採掘は portfolio-d7・2026-11-23）| ACD は引き上げ条項を持たない（受け手は版を上げる必要が無く、Dedicator が新しい版を当てる）| 探して無かった —— 全 508 か月・全差出人で *permissive / BSD / MIT / public domain / CC0 / dedication* と *or later / upgrade clause / new versions of the license* が同じ文に在る通は 4 通で、決める側は 0。最も近いのは不在を支える Piana 氏 2025-05-29（Tiwaz・*"a legitimate choice and I won't fuss about it"*・`ACD-OSI-BOTTLENECKS.md`）。試作に起こさない |
| Steward の死亡・解散のとき役は誰に移るか（種は 5e・採掘は portfolio-d7・2026-11-23）| §16.5 は承継を述べない（空席なら新しい版が出ないだけで、本文は固定のまま）| 探して無かった —— 全差出人で *steward* と *dies / dead / bankrupt / out of business / defunct / dissolved / orphan / disappear / ceases to exist / successor* が同じ文に在る通は 0。近い Rosen 氏 2012-10-05 は死んだ Steward の本文を OSI が配る案で承継の論ではなく、2006-11-15 の *goes bankrupt or disappears* は Work の licensor の話（ACD では §2.8 が承継人を拘束する）。試作に起こさない |

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

**反例（portfolio-cd・2026-11-23）**: (1) 文脈がもう限っている —— 第 1 段落の主題文は *"The legal tools in common use were drafted for a world …"* で、*"That assumption now fails in three places at once"* に続く 3 つの言明（機械生成物・許容型の沈黙・献呈の特許）は、どれもその道具についての言明と読むのが自然である。全称の読みは文を段落から切り出したときにだけ立つ。(2) 同じ型の 2 文目 —— *"Permissive licences are silent on whether a work may be used to train a model"* も切り出せば全称になる（承認済み 141 本については gap 測定 `ACD-1.0.gap-measurements.md` §1.97 が支える。審査に出た提出文では OpenMDW 1.1 は学習を名指さず、ModelGo 2.0 は定義でモデルからの学習（蒸留）を名指す部分的な反例で、承認されておらず普及もしていない —— d7 が提出文で確かめた。最初は確かめる前に「反例がある」と書き、2026-11-23 に訂正した）。T139 が 3 文目だけに *in common use* を足すと、足していない 2 文目は全称だという対比の読みが生まれる（語を 1 か所だけそろえると対比が立つ型）。(3) 直すなら限定を 1 度で 3 文に掛ける形（*"In the tools in common use, that assumption now fails in three places at once"*・+5 語前後）だが、前文は作用せず、*in common use* も実務についての言明として残るので、閉じる分岐が小さい。

**採否**: **採らない**（2026-11-23・5e と cd）。errata E88 に 2 文目も入れ、「文脈（第 1 段落の主題文）が限っている。切り出した読みにだけ当たる」として直さないと決めた。**逆側**: 「直さない」は E6・E87 に続き 3 件目になる。1 文だけを引く審査者には、その文は偽に見える。

## 8. T140・T141 —— THIRD §15.54 の残りの 2 つ（S1 §5.1 第 2 文・S2 §5.2 の回避の授権）を分ける（+7 / +5 語・2026-11-24・起草 5e・**どちらも採らない**）

**方針の欄**: 規則 1 の例外（読みを変えずに文を分け、45 語超の文が減るもの）に当たるかを測った。どちらも errata の番号も `ACD-1.4-UNIQUE-READING.md` の分岐も持たない（§5.1 第 2 文の行は 2 つとも「一意」で、除外の列が *claim* に掛かることは 1.4 の SECOND の T39 が決めている）ので、例外に当たらなければ入れられない。

**T140（S1）**: §5.1 第 2 文（91 語）を *"… a use of the Work that this Dedication permits or purports to permit. This further covenant does not extend to a claim for patent infringement (Section 8), under trademark rights or rights in a name (Section 11.1), for a false statement or representation (Section 11.3), or for a payment You agreed to make for providing a copy or for a service that is not permission to use the Work."* へ（42 語と 56 語・+7 語）。THIRD の案（*That covenant*）が持っていた「第 1 文の約束にも除外が掛かる」読みは、*This further covenant* が第 2 文の *"further covenants"* を名指すことで閉じる。**それでも 2 文目が 56 語で、45 語超の文は 1 つのまま減らない** —— 除外の 4 項は §5.2(b)・§5.2(d) の除外と語をそろえてあり（1.4 の SECOND §14.1・T112・T39。`ACD-1.4-CHANGELIST.md` の「§5.1 / §5.2(d)」の行）、ここだけ縮めると対の差が新しく生じる。

**T141（S2）**: §5.2 の回避の授権（77 語）の *"…, and waives any power …"* を *"To the same extent, the Dedicator waives any power under a law concerning such circumvention to forbid that circumvention."* として分ける（63 語と 19 語・+5 語）。**前半が 63 語で、45 語超の文は減らない**（THIRD の見込み「前半は 59 語」は 4 語ずれていた）。

**採否**: **どちらも採らない**（5e）。例外の条件は「45 語超の文が減る」ことで、どちらも減らさず語だけを足す。**逆側**: (i) T140 は、除外の列が *claim* に掛かることを構文で示すので、T39 が読みで決めた点を文の形でも決める利点がある —— だがそれは分岐を消す変更ではなく（分岐は「一意」）、規則 1 の本則にも当たらない。(ii) 45 語超の割合（14.7%）は 1.0 の 10.3% より高いまま残る。下げるには列挙の文（§8.1・§8.4 の行為の列、§1.2・§1.5・§1.7・§1.10 の定義、§4.2・§4.3）に手を入れるしかなく、それは語を足さずには分けられない（THIRD §15.54 の結び・B3 と引き換え）。**反例（portfolio-cd・2026-11-24）**: なし。(1) 第 2 文は *"The Dedicator further covenants …"* で始まるので、*This further covenant* の *further* はその文の約束だけを名指す。(2) 仮に第 1 文まで掛かると読んでも、除外の 4 項（特許・商標と名前・虚偽の言明・合意した支払い）はどれも Covered Right ではない（§1.5 の定義、§11.4 が特許の請求項と Moral Rights を別に数える）ので、第 1 文から何も外れない。閉じるのは THIRD の案（*That covenant*）が分けたときに生む読みで、1.4 の 1 文の形には元からその分岐が無い。**逆側**（文体）: *This further* と限定詞が 2 つ並ぶ形は契約文ではやや珍しい。

## 9. T142 —— §8.4 の因果の文に、重複原因でも足りることを 1 文で足す（+14 語・2026-11-24・種は 5e が cd の gap ② の読みに当てた反例・**法律家への問い 2 (h2) の答えまで保留**）

**方針の欄**: 規則 1 の本則 —— 消す読みの分岐は `ACD-1.4-UNIQUE-READING.md` の「§8.4 (4 巡目・but-for)」の行。errata の番号は無い（1.0〜1.3 の末文は別の形で反事実を問うていたので、1.0 から在る文の欠陥ではない）。

**Before**（1.5 草案 §8.4 の末尾）: *"… a feature that the Work teaches or embodies is taken so to result. That is a question of causation and not of quantity: no threshold of how much of the Work was used is imposed."*

**After**: *"… no threshold of how much of the Work was used is imposed. A feature so results even if it would also have resulted without the Work."*

**測定**（`--compare`・1.5 草案）: 条 80、§8.4 は 184 → 198 語（+14）、草案 5,864 → 5,878 語。足した文は 14 語の独立の文で、45 語超の文は増えない。先行詞の無い指示語 0（*it* は *A feature*）、そろえ残し 0、全称 0、`--guard` の 468r・468d・冒頭の理由の句はどれも 0。外向きの依拠 1（`ACD-1.0.review-responses-clauses.md` の、特許の除外の理由を §8.4 の文に置く答え —— 足す文で狭まる読みは無いが、1.5 を出すなら見直す）。

**効果**: *so results* が直前の文の *"results, in whole or in part, from the content of the Work"* を受け、因果の基準が but-for ではなく寄与であることを本文で決める。Work が教えも体現もしない特徴でも、Work の内容が一部でも寄与していれば、他のデータだけでも同じ特徴が生じたかどうかを問わない。

**逆側**: (i) 語を足す（B3・+14）。(ii) 寄与の基準は、Work の寄与が小さい特徴まで §8.4 に入れる —— ただしそれは *"no threshold of how much of the Work was used is imposed"* が既に言っていることで、足す文は量ではなく反事実の問いだけを外す。(iii) 採用者の特許の負担（B7）は広い側に寄る。(iv) 法律家への問い 2 (h2) の答えを待たずに本文を動かすことになる —— 答えが「寄与で足りると読むのが普通」なら、この文は要らない（重複の文になる）。(v) *would also have resulted without the Work* は、それ自体が仮定の問いを名指すので、「その仮定を立てて調べてよい」と読まれる余地を作らないか（否定の文脈だが、反例の担当に当ててほしい点）。

**反例（portfolio-cd・2026-11-24）**: (a) *so results* の受け先に反例が 1 つ —— 直前の 2 文のうち *so* を持つのはみなし規定の *"taken so to result"* なので、足す文は「みなされた特徴（Work が教えるか具える特徴）は、Work が無くても生じたとしても結果である」と、みなしの範囲に限って読める。閉じたいのはみなしの外の特徴（教えも具えもしないが寄与した特徴）なので、その読みでは文が目的の場面に届かない。採るなら *so* を使わず *"A feature results from the content of the Work even if it would also have resulted without it."*（+18 語）と主語を言い直す。(b) 仮定を名指すこと自体の害は小さい（*even if* は反事実の答えを無関係にする形で、調べてよいとは言わない）。別の逆側が 2 つ: (i) 事実上の寄与（その M の特徴が実際に Work から一部でも生じたか）の立証は ML では不透明なままで、文は重複原因の法的な扱いを決めるだけで争点を「寄与の有無」へ移すにすぎない。(ii) *in part* と量の閾値の無さに重ねると、学習データに Work を少しでも含んだモデルの、他のデータだけでも生じた特徴まで特許許諾が届く —— 範囲が広がる向きの変更で、`against.md` #16 と B7 の費用が増える（gap の主張には有利、採用には不利）。(c) 分岐は法の側にしかなく、*in part* がそれを既に退けると読むのが自然なので、法律家の答えが「寄与で足りる」なら重複の文になる。(b)(ii) の広がりは条文の範囲の判断であって読みの整理ではないので、法律家の答えなしに動かすのは規則 1 に当たらない。

**採否**: **いまは採らず、法律家への問い 2 (h2) の答えまで候補として置く**（合議の議題 9・5/0/0・2026-11-24）。**答えが来て採るときは、上の After（+14 語・*so results*）ではなく、主語を言い直した形を入れる**: *"A feature results from the content of the Work even if it would also have resulted without it."*（+18 語）。**採るときの費用**: 範囲が広がる向きの変更で、学習データに Work を少しでも含んだモデルの、他のデータだけでも生じた特徴まで特許許諾が届く —— `against.md` #16 と B7（特許を持つ組織が採りにくい）の費用が増える（gap の主張には有利、採用には不利）。**逆側**: 答えが来るまで、but-for の読みの余地は本文（§8.4 の *"a question of causation"*）に残る —— UNIQUE-READING の法の側の行と問い 2 (h2) がそれを開示している。**方針が働いた例**: 規則 1 の本則（分岐を消す）に見えた変更が、実際は範囲を広げる判断を含んでいたことを、反例が切り分けた。

## 10. T143 —— §4.5 第 2 文の *Nothing here* を *Nothing in Section 4.5* へ（+2 語・2026-11-24・起草 5e・**反例待ち**）

**方針の欄**: 規則 1 の本則 —— 消す読みの分岐は `ACD-1.4-UNIQUE-READING.md` の「§4.5 第 2 文 (here)」の行。種は §2.6 の CLA の行で本文の *here* の用法を数えたこと（*here* はほぼ Dedication 全体を指す）。

**Before**: *"Nothing here limits what those terms may be, requires them to reproduce this text, or places any obligation on You in respect of Your recipients."*

**After**: *"Nothing in Section 4.5 limits what those terms may be, requires them to reproduce this text, or places any obligation on You in respect of Your recipients."*

**測定**（`--compare`・1.5 草案）: §4.5 は 89 → 91 語（+2）。先行詞の無い指示語 0 / 0、そろえ残し 0、全称 0、外した文に依拠する外向きの箇所 0。45 語超の文は増えない。

**効果**: *here* を本文の用法どおり Dedication 全体と読むと、「Dedication のどこも You の条件を限らない」が §5.2(b) と同じ条の末文（Dedicator でもある配布者は §5 が禁じるものを課せない）に食い違う。*in Section 4.5* はその文の届く範囲を §4.5 の許しに限り、末文と並べて読める。Dedication 全体として You に条件を課さないことは §10.1・§10.2 が自分の文で言っているので、狭めて失うものは無い。

**逆側**: (i) 効果は変わらない —— 末文と §10.1 の *"other than in Your capacity as a Dedicator"* が既に決めている（UNIQUE-READING の行は「一意」に近い）。文の上の食い違いを消すだけの +2 語は B3 に逆らう。(ii) *here* は本文に 11 か所あり、ここだけ名指しへ替えると、残りの *here* が Dedication 全体を指すことが対比で強まる —— それは用法どおりなので害は無いと見るが、§6.4 *"not decided here"*・§8.2 *"expressed here"* が §6.4・§8.2 だけを指すつもりで書かれていたなら、意味が広がって読まれる（どちらも Dedication 全体と読んでも偽にならないことは確かめた）。**反例をお願いしたい点（cd）**: 狭めることで、Dedicator でない You について何かが失われないか。

**反例（portfolio-59・2026-11-24）**: なし。Dedicator でない You が失うものは無い —— §10.1 と、§10.2 の *license anything under this Dedication or any other terms* / *retain this file* が同じことを言う。「在り物 + Section N」は §2.6・§11.1・§10.5 と同じ型。**効果は上の記録より大きい**: *here* を Dedication 全体と読むと、§16.4（改変した本文を ACD の名で配ることの制限）とも食い違い、そこは末文ではなく §10.5 を経ないと解けない。

## 11. T144・T145 —— 縛られる者として Dedicator だけを名指す 2 つの文を、§2.8 が縛る者まで届かせる（−6 / +7 語・2026-11-24・種は portfolio-59 と 0d）

**方針の欄**: 規則 1 の本則 —— `ACD-1.1-SELF-AUDIT.md` §3ze（1.4 の T121・T120 が持ち込んだ欠陥）。欠陥の全体と重さはそこに書いた。

| 試作 | 条 | Before | After | 語 |
| :-- | :-- | :-- | :-- | --: |
| T144 | §4.5 末文 | *"Section 4.5 does not permit a person to impose what Section 5 forbids on material as to which that person is a Dedicator."* | *"Section 4.5 does not permit a person to impose what Section 5 forbids that person to impose."* | −6 |
| T145 | §10.1 | *"… upon You in respect of the Work, other than in Your capacity as a Dedicator."* | *"… other than in Your capacity as a Dedicator or as a person Section 2.8 names."* | +7 |

**測定**（T143・T144・T145 をまとめて `--compare`）: 条 80、本文 +3 語（§4.5 は 89 → 85、§10.1 は 24 → 31）、先行詞の無い指示語 0 / 0、許可の声 +0、そろえ残し 0、全称 0。外した文に依拠する外向きの箇所 3（逐条の 4.5、`SUBMISSION-MATERIALS.md` の OSD 3・OSD 9 の行 —— どれも 1.4 の文を 1.4 として引く）。

**退けた案（T144 の案 B）**: *"… to impose on any material what Section 5 forbids that person to impose on it."*（22 語）。素材ごとの射程を文の中に残すが、§1.3・§1.4 の *severally* と §2.6 の *as to that Contribution* が既に決めているので、語だけが増える。

**逆側**: (i) T144 は「自分が Dedicator である素材だけ」の明示を落とす。寄与者が Work 全体の EULA を禁じられると読む余地は、§1.3（その Dedicator が適用した素材が Work）と §2.6 が閉じる。(ii) T145 は §10.1 の「受け手に何も課さない」に 2 つ目の例外の語を足す —— 買い手の法務が「うちは譲受人に当たるのか」を読むことになる。課されるのは §2.8 が既に課しているものだけで、Work の受け手としての行為には何も掛からない。

## 12. T146 —— 同じ効果を、1 度ずつ述べる形に書き直す（縮約の再起草・2026-11-24・起草 0d・合議の議題 12）

**方針の欄**: 規則 1 の例外（同じことの述べ直しを外す）を、文ごとではなく本文の構造に当てる。消す errata や分岐の番号を 1 つに絞れないので、合議（議題 12）で採否を決める。

**種**: B3 と B13。1.4 は題名から 5,879 語で GPL-3.0 より長い。`ACD-OSI-BOTTLENECKS.md` の B3 の節は「削る」案だけを測り（306 語・機構部の圧縮で約 360 語）、3,888 語に届かないので「縮められるが答えきれない」と結んでいた。測っていなかったのは、同じ型を何度も述べる構造そのものを 1 度に畳む道である。5 人とも 1.5 草案を初めて読む日に、3f が初見読みの議題を、0d が再起草を、同じ時刻に出した。

**なぜ「短い」でなく「2 度言わない」か**（採掘は portfolio-6c・節は `ACD-1.0.review-readings-7.md` の §1.479 以降）: Chestek 氏（委員・元委員長）2026-01-24 *"anytime you say things twice, unless they are exactly the same, you created the potential for two different interpretations"*。同じ人は 2026-02 に説明の文が問題を増やすとも書いた。逆側: McCoy Smith 氏（委員長）2019-05-11 は、複雑さそのものは却下の理由にならないと書いた（*"Complexity qua complexity is … not"*）。

**同じことを何度述べていたか（1.4）と、縮約でどこに 1 度書いたか**:

| 1.4 で繰り返していた文 | 1.4 の条 | 縮約の条 |
| :-- | :-- | :-- |
| 「どれが有効かを判定しなくてよい・許しはそれに依らない」 | §4.4・§8.6・§12.2（と §2.4 の独立） | 2.7（機械生成か否かの事実の問いは 3.2） |
| 「条件でない・§10.1 は影響を受けない」 | §10.5・§11.1・§11.3・§11.4・§16.4・§16.6 | 6.5 と 10.7 |
| 「承継人・譲受人を縛る・法が許す最大限」 | §2.8・§5.3・§12.4 | 7.2（最大限は 2.7） |
| 計算の利用の許しと成果物 | §1.7・§6.1・§6.4・§6.5・§8.4 | 1.8・1.9・2.2・2.3(b)・2.5(a)・4.1 |
| 許諾の形容詞の列 | §4.1・§8.1 | 2.4 |
| 特許の支配の条件 | §8.5 | 1.7（定義の側） |

1.4 の 80 条がどこへ行ったかは `CLAUSE-MAP-1.4-1.5.tsv` が持つ。上の表の右の列は 1.5 草案の条番号である。

**測定**（題名から・`measure_clause_clarity.py` の `body` と `sentences`）:

| | 1.4 | 述べ直し（固定 37） |
| :-- | --: | --: |
| 語（題名から） | 5,879 | 3,168 |
| 条 | 80 | 50 |
| 45 語超の文 | 28 / 191（14.7%） | 4 / 144（2.8%） |
| 最長の文（語） | 93 | 51 |

**回帰試験**（固定 9 から固定 37 まで・2026-11-24）: 番号を固定した本文に、閉じた欠陥と一意の読みの行を分担で当て、行ごとに「閉じたまま / 対象が消えた / 開いた」を付けた。分担は errata E1〜E29 = portfolio-59、E30〜E58 = 6c、E59〜E88 = 3f、SELF-AUDIT §3e〜§3zd = df、UNIQUE-READING の行は条で 4 人。**開いたもの（どれも直してから次の番号に固定した）**: E13（定義が後の定義語を先に使う）、E34（信頼は目的・禁反言）、E39（*if, and only if*）、E42・E45（約束が許諾の有効に依る語）、E51、E52、E62、E74、E75、E80、E83 の型、E30・T89（*under its terms*）、T45・T57（Steward の番号）、T96（*in each case*）、T102・T126（責任の例外が無条件になる）、T115（*exercise*）、T117（waiver が期間に掛からない）、T129（可分性の言い切り）、§3u(2)（*rights of their own*）、§3zd の型（及びの網羅の言い切りが 1 度戻った）、§1.4(d)・E35（権利を持たない適用者）、通知が *only* Reservation のとき。**手続きの教訓（6c）**: E35 は固定 10 で「閉じたまま」と判定した後、固定 17 で入った語で開いていた。固定した後に動いた条は、判定した人が当て直すまで閉と数えない。固定どうしの条の差を機械で出し、動いた条に当たる行だけ当て直した（固定 34）。**この列が示すこと**: 短くする書き直しは、閉じた欠陥を 20 件以上の単位で開け直す。番号を固定して全件を当て直さなければ、どれも緑のまま入っていた。

**文脈なしの読み手**（3f と 59 が固定 14・17・24・26 を、ドシエも記録も見せずに本文だけ渡した agent の読み —— **人の審査ではない**。役は敵対的な審査者・企業の特許担当・企業法務・非母語の保守者ほか）: OSD 10 項に反するものは無いという答えが続き、求められたのは基準 3（曖昧さ）の改訂だった。採ったもの: 通知を写しただけの人が Dedicator にならない 1 文（10.2）、3.1 の *in respect of the Work*、5.4 を *do not reach* の形に、4.1〜4.3 の外側で EULA が丸ごと違反にならない自己執行の文（5.4(e)）、*directly or indirectly*（1.8・多段の生成）、寄与者にとっての Work（1.3）、実演家の人格権（1.5）、2.5 の柱書の「Dedicator が持つもの」への限定（他人の請求の証言まで止めない）。

**採らなかった案と理由**: (i) *a claim for unauthorised access* を 5.4 で外す —— Dedicator のサイトに置いた Work を集めた人への不正アクセスの請求が戻り、機械学習の許しを裏口で狭める。サーバへの侵入そのものは 2.5(d) の *by reason of its being a use of the Work* で外れている。(ii) 特許の定義を *licensable* の型（Apache-2.0・MPL-2.0）へ —— 従業者発明の対価（独 ArbnErfG・日本特許法 35 条）が *incurring a payment* に当たり、自社の請求項が丸ごと抜ける。一度入れて戻した（固定 23〜27）。(iii) 10.4 の表示の約束を *included on other terms* まで広げる —— 第三者の依存物すべてに掛かる。(iv) 7.2(a) の承継人を「譲り受けた権利について」に限る —— 権利でない約束（5.1・5.2）から承継人が外れる。特許だけを 1.7 の末で限った。(v) 営業秘密を Covered Rights の例示に足す —— 1.4 に無い放棄なので別の試作に分けた。

**残した種**（1.4 と同じ扱いで、今回は変えない）: 実行は *automated processing* に当たるか、社内の非公開の fork への寄与、コードを配る hosted service と 5.4(e)、却下された寄与。

**決める側の文を当てた結果**（6c・原文照合・節は `ACD-1.0.review-readings-7.md`）: Chestek 氏 2026-01-24（前文は説明の場所でない・番号の無い段落を置かない・定義は見つけやすく）、2025-10（Orivex・*as delivered by the Licensor* の型）、2025-03（MGB・*under any theory*）、Smith 氏 2026-01-03（curl・*sublicense* を落とさない）、2025-01-22（Berne と米国法の動詞）、2025-12（免責は目立つ形で）を条に入れた。*sublicensable* は Chestek 氏 2025-10 が外せ、Smith 氏 2026-01 が落とすなと割れたので残した。

**逆側**: (i) 条番号がすべて変わる —— 外向きの逐条・索引・記述子の引用が新しい番号を要る（1.4 は凍結のまま、提出対象も変えない）。(ii) 1.4 で「その場で述べる」と決めたもの（E26・E7、`ACD-1.4-CLARITY-TRIAL.md` §4.1・§4.2）を 1 か所へ寄せる。1 条だけを読む読者には答えが 1 段遠くなる。(iii) 80 条の一意の読みの台帳（`ACD-1.4-UNIQUE-READING.md`）を新しい条に当て直す費用。(iv) 理由の文を外したので、審査者の問いに本文の言葉で答える場所が減る（四隅の原則）。(v) 版が増え（B13）、改訂が控えている版を出すのかという問い（Nelson 氏 2005）が、出す版を決めるまで残る。

## 13. T147〜 の列 —— 述べ直しを載せた後の試作（2026-11-24・議題 16 の後）

固定 37 を載せた後に出た案を、重さの順に並べる。1 つずつ反例 → 測定 → 採決で決める。語はこの節で決めない。

| 試作 | 条 | 案 | 種 | 逆側 |
| :-- | :-- | :-- | :-- | :-- |
| T147 | 1.11 / 10.4 | 案 A: 1.11 の末に *"and states no other terms for such material"*。案 B: 10.4 の *"unless one of them states otherwise"* を *"unless one of them, or the place it is submitted to, states other terms for it"* へ | SELF-AUDIT §3zg（ACD の通知つきの素材を取り込んだ別ライセンスのリポジトリへの patch で、書いた人が知らずに Dedicator になる・6c と 59） | A は寄与の定義から外れるので 10.4 の表示の約束が取り込んだ人に掛かる。B は、CLA を別に求める ACD のプロジェクトで寄与者が Dedicator にならない読みを足す |
| T148 | 5.4(a) | *"or anything done under rights in a trademark or a name"* を *"or rights in a trademark or a name, exercised as such"* へ | 6c（ロゴを埋めた Work の頒布に「商標の条件」で署名と支払いを求める形が 5.1 の外に出る）・59（T147 で比べる価値はある、立たないとも） | *as such* は裁判所が読む語 |
| T149 | 7.2(b) | *"is transferred"* を *"is transferred or exclusively licensed after this Dedication is applied"* へ | 6c | 独占的許諾を受けた人は権利者でないので縛れない法域がある（2.7 と 7.2 の *to the fullest extent* が受ける） |
| T150 | 1.4・2.4・2.6・7.4 | You に「Work、Work から派生した物、Result を受け取る人」を入れ、3 か所の列を外す | 59（短くなる） | 5.x の約束の相手が広がる。受け取っただけで使わない人も You になる |
| T151 | 2.5(d)・5.4(e)・6.5・7.1 | 二重の語（*subject to Section 5.4*、*That is so even where …*、6.5 第 1 文、*irrevocably*）を外す | 59（「2 度言わない」） | 2.5(d) の案内が無いと例外が見えない |
| T152 | 2.5(d) | 適用の前に結んだ契約の請求は 1.4 より弱く覆われる（df） | df | 前の契約の受け手を広げる向き |
| T153 | 1.6 | 除外に有体物の所有権 | 6c の読み手（弱い） | 語を足す |
| T154 | 1.6 | 営業秘密の例示 | 3f・6c（Chestek 氏 2024-10） | 1.4 に無い放棄で、採用者の怖さを足す |
| T155 | 1.8・1.9・10.4・5.4(e) | 実行は *automated processing* か、社内の非公開の fork、コードを配る hosted service、却下された寄与 | 読み手（1.4 と同じ扱い） | 変えると範囲が動く |

**T147 の検討（0d）**: 場面は、B の別ライセンスのリポジトリが A の ACD の通知つきのファイルを含み、C がそのファイルへ B 宛てに patch を送る形である。ファイルごとに条件を示すリポジトリ（REUSE の型）では、そのファイルへの patch は普通そのファイルの条件で出すと読まれ、GitHub の利用規約の inbound = outbound も同じ向きなので、C が ACD の下で出したと扱うこと自体は不意打ちではない。不意打ちになるのは、リポジトリが**寄与についての条件**を別に書いているときである。案 A（1.11 の末）は、ルートに別の LICENSE が在るだけで寄与の定義から外れうる。採るなら案 B を寄与の条件に絞る形: 10.4 *"… becomes a Dedicator as to it, unless one of them states otherwise when it is submitted, or the place it is submitted to states other terms for such submissions."*（+9 語）。**逆側**: CLA や別の寄与の条件を求める ACD のプロジェクトでは、寄与者が Dedicator にならず、寄与の特許は CLA が与えるものに限られる（10.4 の表示の約束が受ける）。

**T148 の検討（0d）**: *anything done under* は広いが、商標の条件を別に求めることは承認済みのライセンスの下でも起きる（59）。著作権と特許の許しは 2.2 と 2.3 に在り、5.4(a) が外すのは 5.1 の「課さない」だけなので、縮まない。*exercised as such* は解釈の語を 1 つ足して分岐を 1 つ減らす形で、釣り合わない。**採らない案を推す。**

**T149 の検討（0d）**: 独占的許諾を受けた人が自分の名で訴えられる法域（米国ほか）では、譲り受けていないその人を 7.2(b) が名指さない。2.5 の柱書（*that another person holds through the Dedicator*）は Dedicator がその人を助けることを止めるだけで、その人自身は縛らない。案: *"any person to whom a Covered Right, or a Patent Claim that Section 2.3 reaches, is later transferred or exclusively licensed"*（+4 語）。*later* は適用の前に譲り受けた人を縛ると書かない。**逆側**: 独占的許諾を受けた人は、許諾の契約の外の約束に縛られないと争える（*to the fullest extent the law permits* が受ける）。1.4 §2.8 は *transferred* だけなので、広げる向きである。

**議題 17 の決定**（2026-11-24・反例は 59・6c・df・3f）: **T147 は採る** —— 語は *"or is submitted to a repository or forum that puts such submissions under other terms instead"* で、10.4 でなく 1.11 の除外の列へ置いた（10.4 の文が 57 語になるため）。*states other terms* の形は、場所の一般規約の上乗せの許諾（GitHub の規約・CLA）まで当たり、普通の寄与が外れる（59・6c が別々に挙げた）。**T148 は採らない**（*as such* は解釈の語が増えるだけ）。**T149 は採る**（*is later transferred or exclusively licensed*）。逆側: 分野限りで独占的に許諾した相手も縛る向きで、B7 の費用が少し増える。適用の前に譲った相手は 2.5 の *holds through the Dedicator* の側に残る（df）。**T157・T158 は採る**（6.2 *"Section 6.2 does not restrict stating truthfully …"*、6.3 *"accompanied or was contained in the Work"* —— 1.4 の T100・T123 への回復・3f の台帳）。**T156**（1.7 末の除外を 7.2 の側へ移す案・3f）**は採らない**: 存続会社が地位を包括承継する合併では「the Dedicator owns」の側に買い手の元の特許が入り、7.2 の文では止まらない（59）。7.2(c) の死後に人格権を行使する人の地位は法律が直接に与えることがあり、その権利まで外れて 7.2(c) が空になる（6c）。**T159 は採る**（59 の台帳 §2）: 2.5(d) の *"This also includes a claim under a right of privacy …"* は、Work の使用と関わらない請求まで約束に入れると読める。1 文に結んだ（*whether by reason of … or under a right of …* —— *or under* だけでは *any other claim* に直接掛かる・6c）。**T161・T162 は採る**（6c の台帳 §9・§10・1.4 への回復）: 9.2 に *or unenforceable*（1.4 §15.2）、10.5 を、名を含む名で配ってはならないの形に（1.4 §16.4。肯定の形は、名の無い抜粋に名を付けることを求めると読める）。

**縮約で 1.4 の語に戻った所の機械の一覧**（df・使い捨ての道具・1.1〜1.4 の CHANGELIST と試作 3 冊の Before / After 200 対を 3 語の連なりで当てた）: 戻っていたのは T60（5.4(e) の it）・T100・T123 で、この束で直した。T69（10.4 の識別の形を 10.2 の通知と同じでよいと言う句）と T40（4.4 の *wherever expressed*）は弱く、足すと限定が増えるだけなので足さない。**限界**: 対で書いていない試作は見えない。

**議題 18 の束**（2026-11-24・議題 17 と 1 本にした）: T160（59・6c が 2 回当て直した形: 1.3 の末 *"Succeeding the Dedicator, or being named in Section 7.2, makes no person a Dedicator as to anything that person holds otherwise than from the Dedicator."* —— 肯定形は管財人や相続人に Dedicator の地位を与え、否定形は権利を 1 つ譲り受けた人の自分の寄与の献呈まで消した）、T163（4.2 *"This Dedication limits no permission by …"* —— 「制限されない」という法の効果の断定をやめる・df）、T164（3.1 に *header, robots directive* を戻す・59 —— 審査者と自動の仕組みが探す語）、T165（2.6 *"the Dedicator's Moral Rights"*・3f の二度目の読み）。

**1.4 と草案の 2 本だけを、ドシエを見せない独立の読み手に比べさせた結果**（6c・議題 18）: 記録の無い落ちが 11 件出た。重いもの —— (A1) 6.5 の *"Except as Section 6.3 states"* が、6.3 の「届く外」を通して 2.2 の許諾まで減らすと読め、虚偽の表示が許諾の条件に見えた（1.4 §11.1 第 2 文は例外を持たない）。(A2) 10.5 に、改変した本文を作り別の名で配る許しが無かった（1.4 §16.4）。(A3・A4) 8.2 の無制限の責任が広がっていた。(A5) 2.5(b) が支配だけの特許に届かなかった。(A6) 5.4(e) から *rights in material* が落ちていた。直した形は議題 18 の束に在る。**この読みが示すこと**: 回帰（閉じた欠陥の行を当てる）は「開いた欠陥」を見つけるが、欠陥と記録されていない効果の落ちは見つけない。2 本を条ごとに比べる読みは別の役である（凍結の門に足す案・6c 起草・df 実装）。

**議題 19 の束**（2026-11-24・固定は h3）: 6c が 1.4 と草案の 2 本だけを独立の読み手に比べさせる読みを 4 回まわした。直す点は 11 → 13 → 7 → 6、内訳は「1.4 から落ちた」が 6 → 9 → 5 → 0、「前の束の直しが作った」が 5 → 4 → 2 → 6。4 回目は HIGH が 0 で、6 点すべてが前の束の直しが作ったものだった。**方針**（3f）: 後者が前者を上回ったら、語を足さず 1.4 の語へ戻す側で直す。大きく直したもの —— 5.4 の一律の例外を条ごとに分けた（5.4 = 2.5(d)・5.1、5.5 = 2.5(d)・5.1・5.2、5.6 = 5.5 の限界。一律の列は技術的手段の約束に支払い・商標の例外を掛けていた・OSD 10）、5.6（5.5 は、自分の素材の条件が写しを縛ることを許さない・1.4 §5.2 末文の効果。自己執行の形も試したが、条件の効力の言い切りになるので戻した）、10.2（通知を写す・記録する・適用のためでなく言及することは適用でない）、10.4（作って出した人と、権限を与えた人のそれぞれ・社員の人格権を落とさない）、6.5 を 1.4 §11.1 の形へ、6.3 末（帰属の省略と通知の保持は *under this Dedication* の虚偽の表示でない）。**採らなかったもの**: データ保護の法の請求を 2.5(d) の例に足す案 —— 1.4 §5.1 の一般の文が字面で拾っていただけで、名指すと「GDPR の権利を前もって放棄させる」と最初に読まれる（3f・59）。狭めたことは `CHANGES-ACD-1.5.txt` の 9 に書いた。T166（5.4(a) の *a name* が publicity の約束まで外す・59）は *", other than under a right of privacy, publicity, or personality"* で入れた。

**議題 21**（3f の最終の読み手 2 体目から・どちらも与えるものを動かす）: (A) 2.3(b) を *"where the Work teaches or embodies the infringing feature, however much or little of the Work was used"* の 1 文にして因果と末文を外す案は、**退けた** —— データセットが請求項の方法を教えも具えもせず、学習したモデルの特徴がその中身から生じる場面（59 の心電図・df の診断の画像）が許諾の外に出て、gap の芯（B10）に穴が開く。*"learned from the Work by processing it"* を足す案（3f）も、学習でない成果物（変換・索引・圧縮の出力）を落とすので次の試作へ（T167）。代わりに末文を *"A feature that a modified version of the Work has, and that the Work itself did not teach or embody, is governed by paragraph (a) alone, by whatever means it was added."* に（59）—— 学習したモデルは改変版でないので、因果の文と逆の答えが出なくなる。(B) 5.4(e)（サイトの一般規約の除外）は、*"other than a registration or acceptance required in order to obtain a copy of the Work"* を付けて採る（59 の条件・登録の壁は 5.1 の内のまま）。**材料**（6c・原文照合）: 具現の語に寄る側 —— Rosen 氏 2002-07-28 *"The grant extends only to claims that are embodied in the Original Work."*、Berkus 氏 2016-01-19（BSD+Patent の審査で読めるかを問うた）。広い射程への不利な側 —— Smith 氏 2018-09-26 *"a unbounded patent license to the distributor's entire portfolio with no boundaries as to scope"*、同 2025-05（ModelGo）。承認済みの中で、出力について「一部でも」の因果を使ったものは見つからない（6c）。

**議題 22（T167・2.3(b)）の経過**: 議題 21 で (A) を退けた後、`O4`（*teaches or embodies, or … learned, extracted, or inferred from its content by processing it*・末文なし）、`O5`（*inferred* を外す）、`i1`（*in whole or in part* を足す）を順に当てた。`O4` は、模型に足させた新しい特徴が *inferred* と読まれて E66 が開く（6c）。`O5` は、Work と他のデータを合わせて初めて学べる特徴が割れる（6c・errata の番号は無い場面）。`i1` は、Work の A に agent が B を足した組み合わせの請求項が、A の分だけで入って E66 が開く（59）。ここで 0d・59・6c は「1 文では同時に閉じない」として元の 2 文に戻す側に傾いたが、3f が作者を伏せて元の 2 文と `O5` を読み手に比べさせると、元の 2 文は「判らない」（小さな部品が corpus に入っただけ）と逆の答え（微調整と蒸留）を出した。読み手の案に 3f が寄せた `Z`（*whether alone or together with other material* と、処理したことだけでは足りないとする 1 文）を、59 が *together* を学習にだけ掛ける語順（`Z′`）に直し、6c がコンマで切れた修飾が 3 つの枝全部に掛かる読みを見つけて *"learned from its content by processing it alone or together with other material"* へ区切りを直して採った。**逆側**: learned / extracted は決める側に使用例の無い語（6c・§1.485）。学んだ関係から作った化合物と、実行の出力は 9.1 に頼る。agent が Work と「B を書いた別の文書」を両方読んで A+B を書いたときは学習の枝に入ると言え、合わせて学ぶ場面と 1 文で分けられない（6c）—— Dedicator が多く与える向きで残る（B7）。承知で狭めた分は「意味が動く所」の 6 に書いた。**議題 23**: 1.4 と草案を比べた 6 回目の読みの K1〜K4（HIGH 0・MEDIUM 3）。K2 は、登録の壁つきで写しを渡す service（6c）と、JS 1 本を配るだけで例外が落ちる service（文脈の無い読み手 4 人）を、5.5(b) の *other than as to a copy of the Work that the service provides*（3f）で分けた。製品の download 前の同意を 5.1 違反に戻す形（j1）は 59 の反例で退けた。10.2 は *identifies or accompanied* も試し、compile した製品と NOTICE 置き場の LICENSE が外れるので（59）*applies to* にした。

**残る種**: T152（適用の前の契約）、T153（有体物の所有）、T154（営業秘密）、T155（読み手の 4 つ）、6.5 の *except as Section 6.3 states* を残すか、1.11 の *such submissions*。番号は T167 から 0d が払い出す。

