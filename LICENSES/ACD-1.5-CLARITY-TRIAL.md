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

**採否**: 未決（(c) を採る向きで、5 人の判断を待つ）。規則 1 の欄には SELF-AUDIT §3zd を書く。採るなら、`CHANGES-ACD-1.5.txt` に 1 行、`ACD-1.5-CHANGELIST.md` の表に 1 行、草案冒頭の語数を `sync_stated_counts.py --apply` で直す。

## 2. 決める側の文から作った点検の観点を 1.4 の本文に当てた（2026-11-23・観点は portfolio-d7 の採掘・当ては 5e）

| 観点（出典） | 1.4 の本文 | 結果 |
| :-- | :-- | :-- |
| 定義は *means* で書き、違う語は違う意味と読まれる（Chestek 氏 2025-07-19・委員長）| §1.1〜§1.10 はすべて *means* | 満たす |
| 許可は *permission* として書き、受動態で書かない（Perens 氏 1999-06-16・07-13）| 許可の文の受動態は 16 文。主たる許諾で許す者が書かれていないのは §6.1 *"Computational Use of the Work is expressly permitted"* だけ | 立たない —— THIRD §15.45 の 9 巡目が行為者を文脈（Dedicator）で一つに決め、§6 が独立の足場か宣言的かは T108 と UNIQUE-READING の §6.5 の行で閉じている。能動にする案（*"The Dedicator expressly permits Computational Use of the Work, …"*・+1 語）は分岐を閉じず、文を分けず語も減らさないので、方針の規則 1 で入らない |
| 同じことを別の文で言い直すと解釈が割れる（Rosen 氏 2002-08-01）| 「§16 は Work の利用への条件でない」が 4 か所、「限界であって条件でない」が 2 か所 | 当てた —— `ACD-1.4-CLARITY-TRIAL.md` §4.1（F2 の試作 (b)）で、どれも条件か否かの曖昧さをその場で閉じる働きを持つと読んで不採用。Chestek 氏・Rosen 氏 2021-06-09（3D Slicer: ある句が許諾の条件かが問われた）は残す側の根拠 |
| 否認は目立つ形で（Smith 氏 2025-12-05）| §13.1・§13.2・§14.1 は大文字 | 満たす |
| *term* は期間の合意と読まれ、一部の法域で解約できる（Piana 氏 2025-02-24）| §3.2 *"for the full term for which the Covered Rights would otherwise subsist"*（権利の存続期間）、§1.10 *"contractual term"*、§2.2 *"further term, condition, or restriction"* | 反例の担当（portfolio-cd）へ —— §3.2 の *term* は権利の存続期間で合意の期間ではない、と読むが、§2.2 の撤回不能と組み合わせて当てる |

## 3. T136 —— §4.1 と §8.1 の *perpetual* を、権利の存続期間に結ぶ（+17 / +35 語・2026-11-23・種は portfolio-cd・起草 5e）

**種**: Carlo Piana 氏 2025-02-24（`license-review`・ModelGo Zero）は、期間の定めの無い合意は一部の法域で相当の予告により解約できると書いた（本人は *"not probably something relevant to the approval"* と前置きした）。cd が原文を読み、ACD-1.4 でそれに一番近いのは §3.2 の *term*（権利の存続期間で、合意の期間ではない）ではなく、§4.1 と §8.1 の *"irrevocable, perpetual"* だと当てた。期間の定めの無いことをそのまま名乗る語である。EU 法の下で起草された EUPL は *"for the duration of copyright vested in the Original Work"*（`license-review` 2008-03 に出た本文）、CC0 の予備の許諾は *"for the maximum duration provided by applicable law or treaty (including future time extensions)"*（`license-discuss` 2024-04 に引かれた本文）と書き、どちらも *perpetual* を使わない（どちらもアーカイブの写しで原文に当てた・2026-11-23）。

**消す読みの分岐**: §4.1 の許諾は期間の定めの無い許諾で、期間の定めの無い約束を当事者が予告で解約できるとする法域では Dedicator の予告で終わる —— 対して、権利が存続する間という期間の定めのある許諾である。§2.2（撤回不能）と §10.4（*"No permission granted by this Dedication terminates under it"*）は文書の中の仕組みを述べる文で（T81 の *under it*）、法が当事者に与える解約の権利を外せない。大陸法の面（フランス民法の期間の定めの無い約束の条など）は**我々の読みで、原典の写しは未取得** —— Légifrance は 2026-11-23 の自動取得を 403 で拒んだ。

| 案 | §4.1 の After | §8.1 の After | 語 |
| :-- | :-- | :-- | --: |
| (A) §3.2 の形 | *"… irrevocable, sublicensable, and transferable licence, for the full term of each Covered Right, including any extension, restoration, or revival of term, to exercise …"* | *"… irrevocable, sublicensable, and transferable licence, for the full term of each patent claim under which it is granted, including any extension or restoration of that term, to make, …"* | +15 / +20 |
| (B) 短い形 | *"… licence, for as long as the rights it covers subsist, to exercise …"* | *"… licence, for as long as the patent claims it covers subsist, to make, …"* | +8 / +9 |

**逆側**: (i) Apache-2.0 は *"perpetual, worldwide, … irrevocable"* で承認済みで、イタリアを含む欧州で広く使われている —— 実務で解約の争いが起きた記録を我々は持たない。(ii) Rosen 氏 2003-08-27 は *perpetual* を「今の意図の表明」として擁護した（`jurisdictions.md` 5a の 2003 の段）。外すと、その意図の表明を失う。(iii) Piana 氏の指摘は 1 人の法律家の自国の読みで、承認に関係しないと本人が書いた。(iv) B3 に逆らう（(A) で +35 語・(B) で +17 語）。(v) (B) の *"for as long as … subsist"* は、権利が一度消えて回復した場合（期間の回復）に許諾が戻るかを語で決めない —— (A) はそれを §3.2 と同じ語で閉じるが長い。(vi) 期間を権利の存続に結んでも、それが期間の定めのある約束と扱われるかは法域の判断で、文で決められない（法律家への問い）。(vii) 米国の読み手には「なぜ perpetual を外したか」の説明が要り、外したこと自体が狭めたと読まれうる（`SUBMISSION-MATERIALS.md` の「差だけを読む人が「狭めた・条件を足した」と読みうる箇所と、その 1 行の注」の表に足す対象）。

**採否**: 未決。不利な事実としては portfolio-cd が `against.md` に記録する（cd が番号を取った）。規則 1 の欄には上の「消す読みの分岐」を書く。採るなら §8.4 は *"on the terms of Section 8.1"* で同じ期間を受ける。
