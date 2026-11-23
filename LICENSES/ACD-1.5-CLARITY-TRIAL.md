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
| **(c)** | *"It grants nothing by implication beyond what its words give."* | −15 | 3 件の型 | 黙示の許諾の排除 |

**測定**（`measure_clause_overlap.py --compare`・1.5 草案の確定直後の形に当てた・2026-11-23）: 3 案とも、条 80 のまま、先行詞の無い指示語 0、許可の声が増えた条 0、そろえ残し 0、新しく入った全称の句 0、外向きの依拠 0。外した文に依拠する記録は 7（against-2 #279・errata E71・SELF-AUDIT L861・CHANGELIST-REVIEWS の 1 行・UNIQUE-READING の §5.2(b) / §11.1 / §11.4 の 3 行）—— どれも 1.4 の文を引く記録で、採るときに「1.5 で置き換えた」の注を足す。(c) の代名詞 *It* / *its* の先行詞は、直前の文の *"This Dedication, in respect of the Work"* から動かない。§5.2(d) の *"Section 11.4 is unaffected"* と §1.5 の *"which Section 11.4 addresses"* は第 3 文（許しを与えない）を指すので残る。

**反例（portfolio-cd・2026-11-23）**: (b) を退ける —— 1.4 の本文で黙示の許諾を外しているのは *"It reaches nothing else"* の 1 文だけで、*implied* / *estoppel* / *no other licence* の類いは §13 の保証の否認の *IMPLIED* を除いて 0 件（grep）。この文を外すと、§15.1（広い読みが勝つ）と組み合わさって、§4 の *use* の許諾から、§8.4 の限定の外の Dedicator の特許について、米国の黙示の特許許諾の議論に足場を与える。B7 は §8.4 の限定を B10 との意図した取引として守っているので、(b) は B7 の釣り合いを黙って動かす。

**(c) の逆側**: (i) *estoppel* を書かないのは §2.5（Dedicator が *estopped*）との混同を避けるためだが、そのぶん禁反言による許諾の排除は明示されない。(ii) 法が黙示の許諾や消尽を強行的に与える法域では、文で外せない（どの案でも同じ）。(iii) 第 1 文は網羅の主張を失い、「及ぶものの例示」に読まれうる。(iv) *"what its words give"* は、§2.5 の約束や §5.2 の授権のような「与える」でない文の扱いを読み手に委ねる —— ただしそれらは明示の語なので、黙示の排除の外に在る（cd）。(v) §15.6 *"no rule that construes a grant narrowly against the grantee"* と衝突しないか —— (c) は語の外の黙示を外す文で、§15.1 も *"that its words allow"* の中の読みなので、同じ線に立つ、と読む（5e）。(vi) 第 3 文の *"It grants no permission under the law of data protection …"* と並び、*It grants nothing … / It grants no permission …* の 2 文が続く —— 前者は量、後者は種類を限るので重ならない、と読む。

**採否**: 未決（反例の 2 巡目を待つ）。規則 1 の欄には SELF-AUDIT §3zd を書く。採るなら、`CHANGES-ACD-1.5.txt` に 1 行、`ACD-1.5-CHANGELIST.md` の表に 1 行、草案冒頭の語数を `sync_stated_counts.py --apply` で直す。

## 2. 決める側の文から作った点検の観点を 1.4 の本文に当てた（2026-11-23・観点は portfolio-d7 の採掘・当ては 5e）

| 観点（出典） | 1.4 の本文 | 結果 |
| :-- | :-- | :-- |
| 定義は *means* で書き、違う語は違う意味と読まれる（Chestek 氏 2025-07-19・委員長）| §1.1〜§1.10 はすべて *means* | 満たす |
| 許可は *permission* として書き、受動態で書かない（Perens 氏 1999-06-16・07-13）| 許可の文の受動態は 16 文。主たる許諾で許す者が書かれていないのは §6.1 *"Computational Use of the Work is expressly permitted"* だけ | 立たない —— THIRD §15.45 の 9 巡目が行為者を文脈（Dedicator）で一つに決め、§6 が独立の足場か宣言的かは T108 と UNIQUE-READING の §6.5 の行で閉じている。能動にする案（*"The Dedicator expressly permits Computational Use of the Work, …"*・+1 語）は分岐を閉じず、文を分けず語も減らさないので、方針の規則 1 で入らない |
| 同じことを別の文で言い直すと解釈が割れる（Rosen 氏 2002-08-01）| 「§16 は Work の利用への条件でない」が 4 か所、「限界であって条件でない」が 2 か所 | 当てた —— `ACD-1.4-CLARITY-TRIAL.md` §4.1（F2 の試作 (b)）で、どれも条件か否かの曖昧さをその場で閉じる働きを持つと読んで不採用。Chestek 氏・Rosen 氏 2021-06-09（3D Slicer: ある句が許諾の条件かが問われた）は残す側の根拠 |
| 否認は目立つ形で（Smith 氏 2025-12-05）| §13.1・§13.2・§14.1 は大文字 | 満たす |
| *term* は期間の合意と読まれ、一部の法域で解約できる（Piana 氏 2025-02-24）| §3.2 *"for the full term for which the Covered Rights would otherwise subsist"*（権利の存続期間）、§1.10 *"contractual term"*、§2.2 *"further term, condition, or restriction"* | 反例の担当（portfolio-cd）へ —— §3.2 の *term* は権利の存続期間で合意の期間ではない、と読むが、§2.2 の撤回不能と組み合わせて当てる |
