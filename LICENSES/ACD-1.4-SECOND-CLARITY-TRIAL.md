---
file: LICENSES/ACD-1.4-SECOND-CLARITY-TRIAL.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-12
canonical-ref: LICENSES/ACD-1.4-CLARITY-TRIAL.md (§1〜§9・規則はそちらに従う) / LICENSES/ACD-1.4-DRAFT.txt (試作の対象・この file は草案を上書きしない) / LICENSES/ACD-1.4-CHANGELIST.md (採用した変更の記録先)
---

# ACD-1.4 草案の明瞭性の試作（2 冊目）—— §10 から

`ACD-1.4-CLARITY-TRIAL.md` が 900 行の advisory に届くので、同じ file の注記どおり節の単位で分けた。
節番号は続き番号で、規則（草案を上書きしない・採用の条件 2 つ・分担）は 1 冊目の冒頭に従う。

## 10. 直した条が作った入口の穴、指す先の主題、§15.1 の宛先（2026-11-06・25）

**レンズを 3 つ足した。**

1. **修正の入口**: 2026-11-01 の外部レビューで直した §16.2（H-02）は、許諾の効果ではなく**適用が成立したか**を問う文へ変わった。適用の行為そのものを読み直した。
2. **指す先の主題**: 61 か所の内部参照は解決しているが（`measure_section4c.py`）、解決することと、指す先が同じ対象を論じていることは別である。括弧の参照を全部読んだ。
3. **余剰語の準則**: 語は働きを持つものとして読まれる。「You に向けて読むと空になる語」は、残りの読みへ押される。

### 10.1 T5: §16.1 —— タグだけの適用が条文から読めない（+7 語）

**Before（1.4 草案）**: §16.1 *"To apply this Dedication, place a notice with the Work in substantially the following form:"* / §16.2 *"Where a work to which a Dedicator has applied this Dedication is accompanied by the identifier … that is sufficient notice of these terms …"*

**After**: §16.1 *"To apply this Dedication, place a notice with the Work, in a form Section 16.2 names or in substantially the following form:"*（§16.2 は変えない）

**欠陥**: 1.3 の §16.2 は *"Where a work is accompanied by …"* で、タグだけでも条件全体が及ぶと読めた。H-02 はそれを「Dedicator が適用した著作物」へ限定した。第三者が勝手にタグを付けても成立しないようにするためで、その修正は正しい。だが**適用の行為を述べる条は §16.1 しかなく**、§16.1 は長い通知文の形だけを挙げる。ファイルの先頭に `SPDX-License-Identifier: ACD-1.4` だけを置く権利者（SPDX の通常の使い方）は、1.3 では §16.2 で足りたのに、1.4 草案では「適用した」と言えるかが条文から決まらない。**修正が持ち込んだ後退である**（1.0〜1.3 には無いので errata ではなく `ACD-1.1-SELF-AUDIT.md` の対象）。

**§15.1 では救えない**: §15.1 は Dedication の条項で、適用されて初めて働く。適用されたかという問いの前には立てない。§2.3 も同じである。ゆえに「広い読みが勝つ」で済ませられず、この問いが立つと Work 全体の許諾が問われる（基準 3 の「実質的な影響」）。

| 場面 | 1.3 | 1.4 草案 | T5 |
|---|---|---|---|
| S1 権利者が §16.1 の通知を置く | 適用 | 適用 | 適用 |
| S2 権利者がタグだけ置く | §16.2 で足りる | **読めない** | 適用 |
| S3 第三者が他人のコードにタグを付ける（H-02 / J-04）| 足りると読めた | 不成立 | 不成立（§1.4 の Dedicator でない）|
| S4 権利者が README に名前と版で書く | §16.2 で足りる | **読めない** | 適用 |
| S5 版の無い「ACD」だけ | §16.2 に当たらない | 同左 | 同左（変えない）|

**語の機能**: *"with the Work"* を残すので、メールで名前を挙げただけでは通知にならない。*"To apply"* が目的を述べるので、適用の意思の無い言及は当たらない。

**先に登録する反例（bb へ）**: (a) README が比較のために ACD-1.4 を挙げているだけ、(b) 依存物の同梱ディレクトリにあるタグ、(c) 従業員が雇用主のコードにタグを付ける、(d) §1.3 の *"to which"* と部分適用（`docs/` だけのタグ）、(e) 語順 —— *"a form Section 16.2 names"* が通知文の前に来る形が「通知文は推奨にすぎない」と読まれて困るか。

### 10.2 T6: §6.4 の *"(Section 9)"* を外す（−2 語）

**Before**: *"Whether a right subsists in any such thing is not decided here and does not need to be (Section 9)."* / **After**: 括弧を外す。

**欠陥**: *"any such thing"* はモデル・パラメータ・重み・埋め込み・出力である。§9 が論じるのは *"any part of the Work"*（§1.8 / §9.2）で、それらは Work の部分ではない。参照をたどった読者は自分の問いに答えない条に着き、§9.2 の *"Sections 3 to 8 and Section 12 apply to it in full"* が出力の権利にも及ぶという誤読の足場にもなる。1.1 で E4 を閉じたとき、§6.4 が §9 の姿勢と食い違わないように足した参照で（`01621730`）、**姿勢の類比であって同じ対象の案内ではない**。文の内容は §6.4 だけで足りる。

**効果**: 許諾の範囲は変わらない。括弧は結論を運んでいない。外向きの文書に *"(Section 9)"* を引く箇所は無い（`not decided here` を引くのはトリアージの D-07 だけで、省略の形で引いている）。

**先に登録する反例（bb へ）**: (a) §6.4 の文が「決めない」と言う根拠が §9 にしか無いと読む筋、(b) 出力が Dedicator の Work に取り込まれたとき（出力が §1.8 に当たる）の案内が消えて困るか。

### 10.3 T7: §15.1 の *"the least obligation"* に宛先を付ける（+2 語）

**Before**: *"… give the widest permission and the least obligation that its words allow."* / **After**: *"… and the least obligation upon You that its words allow."*

**欠陥**: §10.1 は You に義務を 1 つも課さないので、*"least obligation"* を You に向けて読むと語は空になる。余剰語を避ける読みに従うと、語が働く先は本文に残る義務、つまり **Dedicator の約束**（§2.6 の識別の約束・§5・§8.6・§12.2）で、「Dedicator の約束は言葉が許すかぎり狭く読む」という読みが立つ。§15.1 の第 2 文（*"the reading that grants more to You prevails"*）がこれを押し返すので**実害は無く**、同じ条の 2 文が逆を向いているのが欠陥である。§10.1・§2.6 は *"upon You"* と書いている。1.0 からある（採用なら errata）。

**効果**: You への許諾は変わらない。Dedicator の約束を狭く読む足場が消える。第 2 文の働きは変わらない。**語数の費用に見合うかは反例次第で、第 2 文が足りるなら残す判断もある。**

**先に登録する反例（bb へ）**: (a) *"upon You"* が「Dedicator の義務は §15.1 の外にある」という読みを立て、第 2 文の射程まで狭めないか、(b) §16.4 の頒布の条件（文書についての制約）との関係 —— §15.1 は E20 で著作物についての読みに限っているので当たらないはず。

### 10.4 見て残したもの

- **§12.5 が §12.2 にしか掛からない**: E53 が意図した狭さとして記録している（§12.1 が働く法域では §11.3 が理由）。直さない。
- **§14.1 と約束の組**: 問 9（`QUESTIONS-FOR-COUNSEL.md`）にある。今日、Apache-2.0 §8 の比較を足した（下）。条文は法律家の答えを待つ。
- **定義の *"person or entity"* の冗長**: §15.5 の行の逆側として記録済み（−16 語になるが、定義 3 つを変えて得るのは語数だけ）。
- **§2.2 の *"any copy of the Work that has been made available"***: `faq.md` A30 の答えの一部で、§5.2(b) が全体を覆う。
- **括弧の参照の残り**: §6.4 以外の括弧の参照はどれも指す先が同じ対象を論じていた。

### 10.5 反例のあと —— 3 件とも採用した（+7 / −2 / +2 語）

bb の反例（2026-11-06）: 登録した反例はどれも当たらなかった。T5 の語順は害が無い —— ドシエは既に §16.1 を推奨の通知と呼んでいて（errata E1 / E12 / E29）、T5 は本文をその読みに揃える。§16.2 が条件の全部を及ぼすので、長い通知文で失うのは §11 の除外を読者が目にする機会だけである。

T5 の表に足す場面（bb）:

| 場面 | T5 | 理由 |
|---|---|---|
| S6 ACD のコードを別のプロジェクトへ取り込み、来歴としてタグを残したまま手を入れた人の改変分 | 適用ではない | タグを残すことは *"place"* ではなく、*"To apply"* の目的も無い。**最も重い反例**: タグは REUSE などの道具が既定で残し、§3 は取り消せず §8 は終了しないので、誤って成立したときの費用が他のライセンスより重い。本文は変えず、`faq.md` に書く（bb）|
| S7 SPDX の式 `ACD-1.4 OR MIT` | 適用（§16.2 の名前と版の参照）| §16.2 の字義のタグではないが、受領者が ACD を選べるので効果は同じ |

**意思表示の強さ**: 1 語のタグが §3 の放棄の意思として足りるかは問 1 の (e) に足した。足りなくても §4.4 が受け止めるので、壊れ方は「§3 は効かないかもしれないが §4 は立つ」で止まる。T5 の必要性は弱まらず、§4.4 の働きの実例になる。

**循環は解ける**: §16.1 が行為で、§16.2 が帰結である。T5 のあとの §16.2 の働きは、本文を持たない下流の複製に terms を及ぼすことである。

T6 は反例なし（出力が Work に取り込まれれば §9 が自分の条件で働く。`ACD-1.1-CHANGELIST.md` と `ACD-1.2-CHANGELIST.md` の引用はその版の話なので残す）。T7 は §1.134 の表の基準 3 が §15.1 に乗っているので、+2 語に見合う（bb）。第 2 文は主語が別なので狭まらない。

あわせて §8.4 の途中の改行と §8.6 の短い行を詰めた。語は変えていない（§16.4 の *"differences of line breaking"*）。

## 11. 条が前提にする事実は、採用者の普通の操作で崩れないか（2026-11-06・25）

**レンズ**: S6（改変したファイルに残ったタグ）は、条文ではなく**採用者の普通の操作**から出た反例だった。同じ問いを、採用者と受領者が実際に行う操作の一覧へ当てた。

| 操作 | 結果 |
|---|---|
| 本文の file を自分のリポジトリへ写す | **穴** —— 1.1 以降のヘッダはこのリポジトリの path を述べる。§1.1 により外してよいが、本文がそう言っていない。確定手順に 1 行足した（`ACD-1.1-CHANGELIST.md` §0.13）。凍結済みの版は直せない |
| 適用する版を上げる | 本文は答えている（§2.2 で前の版の許諾は残る）。このリポジトリの `LICENSE` はそう書いているが、`faq.md` に問いが無い（bb へ）|
| Dedicator が App Store や有料の配布で出す | 既知 —— §5.2(a) は Dedicator の措置だけを縛り、配信先の措置は外（`against.md` #171）。自分の複製への措置まで禁じる広さは `BLIND-SPOTS.md` が「実在するが不活性」と記録している。§15.1 の宛先を直しても、第 2 文がもともと広く読ませるので変わらない |
| 受領者が別の条件で再頒布する / 通知を外す | §4.5・§10.2 が答える |
| 別の人が自分の改変に ACD を適用する | §16.3 が答える。その人は改変の Dedicator になる |
| 写真の XMP や URL だけで示す | T5 のあと §16.2 の名前と版の参照に当たる |
| PR を受ける（§2.6 の *"unless they state otherwise at the time of submission"*）| 記録がどこにも残らないことがある。Apache-2.0 §5（*"Unless You explicitly state otherwise"*）も同じ形で、承認済みの先例がある。本文は変えず、`faq.md` に「述べられた寄与は merge しないのが最も簡単」と書いた（bb）。違いは費用で、ACD では寄与者の放棄が取り消せない |

## 12. 1.4 で足した語の付き先（2026-11-06・25）

**レンズ**: E27（修飾語が別のものに付く）を、1.4 で足した語に当てた。E27 の掃引は 1.2 のときで、そのあとに足した語は通っていない。長い文を全部並べて（50 語以上が 18 文）、足した語の付き先を読んだ。

- **T8 §16.4（+1 語）**: 下の After。読点のあとの *except* は文の冒頭の *"except by the Steward"* と並ぶので、禁止全体への例外と読める。この文書で唯一の制限で、§15.1 は E20 で著作物に限ったので解決しない。
  - Before: *"… that no earlier text has borne, except a draft identified as such, so that each name …"*
  - After: *"… that no earlier text, other than a draft identified as such, has borne, so that each name …"*
- **T9 §11.4（−1 語）**: *"other than the Dedicator"* が *personal data* に掛からないと読めた。
  - Before: *"personal data, or the likeness, voice, or performance of a person other than the Dedicator"*
  - After: *"the personal data, likeness, voice, or performance of a person other than the Dedicator"*

**見て残したもの**: §8.1 の *"where the infringement is caused by …"* は読点のあとだが両方の動作に掛かるのが意図で、そう読める。§2.6 の *"and that material is included with the Work"* は 2 つの場合の両方に掛かる。長い文の分割（§2.6・§5.3）は語が変わらず得るものが小さいので試作しなかった。

## 13. §8.2・§8.4・§8.6 を合わせて読む —— 特許の射程を別の条が素通りしていないか（2026-11-06・25）

**きっかけ**: オーナーが共有した別の AI の見解（オーナーの指示ではない）が、§8 の条を合わせて敵対的に読むことを挙げた。行為の類型と比較は `ACD-1.0.gap-measurements.md` §1.135 にある。ここは本文の分岐を置く。レンズは §9 と同じで、§15.1 が広い側へ解決する読みである。

### 13.1 T10: §5.1 の第 2 肢が特許の請求まで不行使にする読み（+7 語）

**Before**: *"… and further covenants not to assert against You any claim or cause of action, whether now known or unknown, arising from or relating to a use of the Work that this Dedication permits."*
**After**: *"… whether now known or unknown, other than for patent infringement (Section 8), arising from or relating to a use of the Work that this Dedication permits."*

**欠陥**: 1.2 が #272 を閉じるために足した肢で、1.3 の点検は商標だけを当てた（`ACD-1.3-CHANGELIST.md`）。§1.5 が除く権利のうち特許は当てていなかった。学習は Covered Rights の面で許されているので、「この Dedication が許す利用」を利用の単位で読むと、Dedicator の特許請求も「許された利用に関する請求」になる。§1.7 はモデルの製造・頒布・使用も Computational Use に含めるので、販売まで届く。§15.1 はこの読みを選びうる。**すると §8.4 の因果の限定は約束の側から素通りされ、E15 の害が全部戻る。** 条文の中の反対の支えは §8.6 の *"the second footing it would otherwise lack"* で、§5 は特許の約束ではないと読める。読みは決まらないので語で閉じる。

### 13.2 T11: §8.4 の方法の請求項（0 語）

**Before**: *"… the feature that infringes it results, in whole or in part, from the use of the Work; a feature that the Work teaches or embodies is taken so to result."*
**After**: *"… results, in whole or in part, from the content of the Work; a feature …"*

**欠陥（bb の問い）**: 方法の請求項では、工程は Work の処理そのものなので「使用から生じた」と同語反復に読める。§9.7 の表は K4 / P を「Work が教えるか具えるときだけ」と書いたが、文がそれを保証していなかった。Dedicator の学習手法の特許が、Work を 1 件混ぜた学習に及ぶ読みが残る。25 の初案は *", and not only from the manner of that use"*（+9 語）で、bb が *use* を *content* に替える 0 語の案を出した。K1 ✓・K2 ✓・K3 ✗・K4 ✗・K5 ✗・K6 ✗ で §9.7 の表と一致し、Work が実行されるコードで工程がその動作である場面は *embodies* が受ける。

### 13.3 T12: §8.6 と §11.4 の *described*（0 語・−1 語）

**Before**: §8.6 *"… the patent claims described in Sections 8.1 and 8.4 against You, in respect of any act …"* / §11.4 *"the patent claims described in Section 8"*
**After**: §8.6 *"… against You the patent claims that Sections 8.1 and 8.4 reach, in respect of any act …"* / §11.4 *"the patent claims Section 8 reaches"*

**欠陥**: *described* を §8.4 の第 1 文だけと読むと、約束が許諾より広くなる（§9.5 の逆側 (iv) で 5a が触れていた）。§8.4 と §6.1 は *reach* と書く。

### 13.3b T13: §8.3 第 1 文（−2 語・5a の抽出）

**Before**: *"Nothing in this Dedication reserves, preserves, or leaves unaffected any patent right of the Dedicator in respect of the Work."*
**After**: *"… any patent claim that Sections 8.1 and 8.4 reach."*

**欠陥**: §8.4 が外す請求項も「Work についての特許権」と読め、末文の *"Any reading … is to be rejected"* と §15.1 が限定を押し戻す。第 2・3 文は Work が具える請求項の話なので、第 1 文だけが広い。

### 13.4 修正の前後

| | Before（§15.1 の読み）| After |
|---|---|---|
| 受領者 | K3 / K4 / K5 も約束で守られる読みがある。ただし §8.4 と食い違うので依拠しにくい | K1 / K2 / K7 と、Work が教えるか具える手法は守られる。K3 / K4 / K5 は守られない |
| 特許保有者 | Work を 1 件混ぜた学習と、その成果物の販売に、特許全体を主張できない読みがある | 著作物が教えるか具えるものと、使用から生じた特徴だけが負担である |
| 1.3 との関係 | | 第 2 肢を持つ 1.2・1.3 は凍結のまま広い読みを残す。文が 1.0 に無いので errata ではなく `ACD-1.1-SELF-AUDIT.md` の型である |

### 13.5 見て残したもの（5a の敵対読みを含む）

- **§8.3 の語**: bb の案は文頭に *"Within the reach of Sections 8.1 and 8.4,"*（+8 語）で、25 の案（−2 語）と効果は同じなので短い方を採った。
- **同じ型の掃引の範囲**: 5a は全 80 条の約束と否定の文、bb は *any / every / all / no* + 権利の語と、名詞を持たない全称・動詞の側の全称・句の射程・定義語の経由の 4 形、25 は 1.0 のあとに足した 76 文を読んだ。特許へ漏れるのは §5.1 と §8.3 だけだった。
- **§6.4 の *"You owe nothing"***: §8.4 が *"Section 6.4 alone would leave Computational Use permitted as to the Covered Rights while exposed as to patents"* と述べるので、§6.4 は特許に届かないと本文が答えている。
- **§9.2 の *"asserts no right in Machine-Generated Material"***（5a）: Covered Rights に限られていないが、宣言の文で約束ではなく、特許は素材の中の権利でもないので残す。
- ***in part* と閾値なしの合算**（5a）: 学習した特徴はどれも一部は Work から生じたと読める。*in part* を外すと 2 つのデータが各々十分な原因である場面で受領者が外れる。同じ語の表裏なので文を動かさず、費用として B7 に書く。
- **判定の難しさ**（5a）: §8.4 は閾値を判定できないと述べるが、学習した特徴の因果も判定しにくい。*teaches or embodies* に入らない特徴の保護は薄い。問 2 の領分である。
- **A + B + C の請求項**（5a）: どれが「侵害する特徴」かに 2 通りの読みがある。想定問答は要素の 1 つを Work が供給すれば及ぶと述べている。設計で、費用は B7。
- **§2.8 の *"a patent claim in the Work"***（5a）: §8.4 の請求項より狭く読めるが、同じ文の *assigns* と、§11.4 の同じ句が受ける。
- **モデルを組み込んだ装置の組み合わせの請求項**（5a）: §8.4 は装置を名指さないので外れる。受領者の費用である。

### 13.6 T14: §5.1 の対価（+8 語）

**Before**: *"… other than for patent infringement (Section 8), arising from or relating to a use of the Work that this Dedication permits."*
**After**: *"… other than for patent infringement (Section 8) or for a payment You agreed to make, arising from or relating to a use …"*

**欠陥**: ACD を適用した会社が有償のサポートを売ると、代金の請求は許された利用に「関する」請求と読める。`faq.md` A30 と J-16 は対価を課せると答えていて、§15.1 の広い読みと食い違う。

**初案は不成立だった**: *"or relating to"* を外す案（−3 語）は bb の反例で落ちた。学習済みモデルの販売への不正競争の請求は Work の利用から生じるとは言い切れず、§1.135 の差が立つ行為の保護が緩む。契約前責任も落ちる。*associated* に近い #272 の答えも半分弱まる。従量の料金も *arising from a use* のままで解けない。

**残るもの**: Work について対価を求める契約は §5.2(b) が別に止める。*relating to* の広さの問い（問 5）は残る。

### 13.7 T15: §2.3 の知らない受領者（+7 語）

**Before**: *"You need not sign, register, notify, request, or agree to anything, and nothing You do or fail to do can cause You to lose a permission granted here."*
**After**: *"To hold a permission granted here, You need not know of this Dedication, sign, register, notify, request, or agree to anything, and nothing You do or fail to do can cause You to lose one."*

**欠陥（bb の問い）**: §10.2 は通知を外してよいとするので、Dedication を見たことのない受領者が通常の場面になる。§1.6 の *"exercising permissions"* を「知って行使する」と読むと、その人に特許の許諾が及ぶかが語から決まらない。Nelson 氏と Fogel 氏が CC0 の審査で問うた当の場面である（`review-precedents.md` §1.138）。§16.2 は識別子が残る写しの文で、全部外れた写しには届かない。§1.6 を替えない理由は、Apache-2.0 と同じ定型で、E20 などが依拠しているからである。

**初案は不成立だった**: *"You need not know of it"* だけだと受領の側に限っておらず、§2.6 と組むと、Dedication を知らないまま貢献した人を Dedicator にする読みに引ける（§8 は将来の請求項まで取り消せない）。*To hold a permission* で受領の側へ閉じた。*it* は直前の *a permission* を指して読めるので、*this Dedication* と書いた（bb）。

**見て残したもの**:
- **§5.3 の *"relied upon"***（bb）: 「援用できる」と「事実として信頼した」の 2 通りに読め、後の読みなら知らない受領者は外れる。著作権の側は同じ条の最終文が §3 / §4 を残し、特許の側は §8.6 の *against You* が §5.3 の外で働くので実害が小さい。語を替えると §4.6 と外向きの引用へ波及するので残す。
- **§13 / §14**: 知らない受領者は免責の文を見ていない。§10.2 から既に生じている事実で、問 1 の (f) にある。

**費用**: 文は法に対して成立を保証しない。問 1 の (g) に置いた。

## 14. 本文だけを 7 つの視点で読み、反証と反例を当てた（2026-11-07・25、bb、5a）

読み手 7 体が本文の 1 ファイルだけを読んだ（素通り、主体のずれ、特許、不整合、理由の文、下流と時間、OSD 逐条）。候補 40 件のうち 1 件は「外さない」の記録で、残り 39 件を統合すると 32 件になった。候補ごとに本文の反証役と記録の照合役を当て、6 件が残った。そのあと bb が反例を当て、5 件を形を変えて入れた。agent の読みは読みであって、法律家の判断ではない。

### 14.1 T16: §5.1 と §5.2(d)（+19 語）

**Before**: *"… any claim or cause of action, whether now known or unknown, other than for patent infringement (Section 8) or for a payment You agreed to make, arising from or relating to a use of the Work that this Dedication permits."*
**After**: *"… any claim or cause of action, whether now known or unknown, for a use of the Work that this Dedication permits, other than for patent infringement (Section 8), under trademark rights or rights in a name (Section 11.1), for a representation Section 11.3 describes, or for a payment You agreed to make."*
§5.2(d) の末尾に *", other than a representation Section 11.3 describes"* を足した。

**欠陥**: 除外を 2 つ名指ししたので、名指しされない商標の請求は不行使に入ると読める。§16.1 は *"are not granted"* と告げていて食い違う。`ACD-1.3-CHANGELIST.md` の点検は「§11.3 の行為は *permits* に入らない」で clean としたが、§5.2(d) が同じ *"use of the Work that this Dedication permits"* を §11.4 の与えない privacy に使っているので、この読みは閉じない。名前もロゴも変えない fork は §11.3 の表示をしなくても起きる。

**bb の反例 2 件**: (1) 虚偽の推奨を right of publicity で、氏名の侵害を personality で立てると、§5.1 を外れても §5.2(d) に入る。§2.4 により両方は独立に働く。(2) 名指しが 4 つになると、名指しされない請求は入るという読みが強まる。You の機械で Dedicator が負傷した請求や、改変版が Dedicator を中傷した請求が *relating to* に入る。§15.1 では切れないので、語で切る。

**T14 との関係**: *"or relating to"* だけを外す案は、学習済みモデルの販売への不正競争の請求が Work の利用から生じるとは言い切れないので落ちた。*for a use* では、§1.7 がモデルの販売を Computational Use に含め、§6.1 がそれを許しているので、この請求は許された使用そのものを問う請求である。

**2 つの covenant の累積（bb）**: §5.1 は名前の権利を除くが、§5.2(d) は personality の権利の不行使を約束したままである。氏名権を人格権として立てる法域（ドイツ民法 12 条など）では、§11.3 の表示が無いかぎり §5.2(d) で塞がれる。E31 の目的どおりで、§2.4 により 2 つの covenant は累積するので、矛盾ではない。

**逆側**: 使用に付随するだけの請求は covenant から出る。データ保護は除外に足していない。E31 が Dedicator 自身の権利の不行使を意図したからで、§5.2(d) の privacy などと同じ向きである。

### 14.2 T17: §8.1・§8.3・§8.4（+6 語）

**Before**（§8.1）: *"licence under every patent claim owned or controlled by the Dedicator, now or in future, that would be infringed by making, having made, using, offering to sell, selling, importing, or otherwise transferring the Work, or by doing any of those things in respect of anything derived from the Work, where the infringement is caused by …"*
**After**（§8.1）: *"licence to make, have made, use, offer to sell, sell, import, and otherwise practise or transfer the Work or anything derived from it, under every patent claim owned or controlled by the Dedicator, now or in future, that those acts would infringe, where the infringement is caused by …"*
§8.4 は同じ形で *"to put the Work to Computational Use and to make, have made, use, offer to sell, sell, import, and otherwise practise or transfer any model, parameter set, weight, embedding, or output resulting from Computational Use of the Work"*。§8.3 第 1 文の末尾に *", as to the acts they describe"*。

**欠陥**: 今の形は *licence under every patent claim* で終わり、行為は請求項を選ぶ関係節の中にある。短いコードを公開すると、その請求項の下の許諾を Work を使わない競合が主張する読みが語で閉じない。Apache-2.0、MPL-2.0、EPL-2.0、OSL-3.0 はみな行為を目的語にしている。Berkus 氏の *"carte blanche"* の文に当たる形である。workflow の案は §8.5 に 1 文を足す形（+28 語）だったが、こちらの方が短い。

**bb の反例と手当て**: (1) 動詞の列が許諾の上限になる。特許法 2 条 3 項 1 号は「譲渡等（譲渡及び貸渡し…）」と輸出を挙げ、ドイツ特許法 9 条は *"besitzen"* を挙げる（どちらも 2026-11-07 に一次資料で確認）。§15.1 は語を足せないので *"and otherwise practise or transfer"* にした。*practise* は §8.3 と §8.5 が使う語で、目的語は Work のままなので第三者の読みは閉じたままである。(2) *that use* は不定詞の主語が You なので、モデルだけを受け取った者には自分の使用と読める。*"resulting from Computational Use of the Work"* にした。(3) *"the Work or anything derived from it"* にして *and* の読みを消した。(4) §8.3 も請求項の単位のままだったので、§8.6 にそろえた。

**逆側**: 請求項の全範囲が許諾されるという You に有利な読みが消える。Chestek 氏 2025-02-09 の *"The patent grant in a FOSS license must be for all possible uses of the code."* には、*use* と *otherwise practise* で答える。法律家への問い 2 の (g) に足した。

### 14.3 T18: §8.4 の足した機能（+13 語）

**After**: *"Section 8.1 alone governs a feature added to the Work, by whatever means."* を *"… restore the exposure this Section exists to remove."* の次に置いた。

**欠陥**: Work を自動処理に通して新しい機能 Z を足すと、手で足せば §8.1 の末尾で外れる Z が *output* として戻り、*in part* で届くと読める。反証役は「常に戻る」は退けたが、入口は閉じなかった。§8.1 の除外が手で改変した者にしか効かない形になる。

**初案は不成立だった**: *"A feature does not so result merely because it was adapted to the Work or combined with it."* は bb の反例で落ちた。You が自分の base model を Work で fine-tune すると、既にあった機能が Work の領域へ特化する。これは機械学習の語で domain adaptation そのもので、§8.4 の本来の場面である。方向で切る bb の案を短くしたのが今の文で、*by whatever means* は手と機械を区別しない。

**確認**: agent が Z を足す → §8.1 の末尾で外れる。agent が Work の教える方法を足す → §8.1 で入る。自分の base model の fine-tune → Work へ足していないので §8.4 に残る。Work が model で、それを fine-tune して足した機能 → §8.1 で判定する（問 2 の (h)）。別ファイルの plugin は手でも同じ *anything derived* の問いである。

### 14.4 T19: §1.9 の宛先（+3 語）

**After**: *"a repository or forum offering the Work under this Dedication"*。

**欠陥**: 宛先が *"the Dedicator maintains"* なので、保守を引き継いだ者が Dedicator でないと §2.6 の経路が切れる。適用の問いなので §15.1 は使えない。

**初案は不成立だった**: *"or has maintained"* は bb の反例で落ちた。repository が会社へ移り §4.5 どおり新しい版が proprietary になると、ACD の表示を見ていない人が PR を送って Dedicator になり、著作権と将来の特許まで撤回不能に出す。今の欠陥の失敗は「寄与が覆われない」で後から取れるが、初案の失敗は取り返せない。人ではなく表示で切ると、寄与者が ACD を見ている場面だけに掛かる。

**逆側**: ACD のままの fork への寄与も入る。寄与者は同じ表示を見ているので不意打ちにならない。§2.6 の識別の約束を負う者がいない場面は残る。

### 14.5 T20: §8.6 第 3 文（−33 語）

*"Permission under the Covered Rights stands here on three footings, surrender (Section 3), licence (Section 4), and covenant (Section 5); this Section gives the patent grant the second footing it would otherwise lack."* を外した。

理由の文のレンズで B（外しても読みが動かない）として反証に残った唯一の文である。作用は第 1、第 2、最終文にあり、説明は前文が持つ。§2.4 は 4 節を挙げるので *three* とも数が合わない。Chestek 氏の *"I question whether they belong in the agreement at all."*（#295）に当たる。**逆側**: なぜ許諾と約束が両方あるかが §8 からは読めない。答えは前文と `REVIEWERS.md` にある。E54 が直した文を外すので、E54 の行は「語を直し、のちに文を外した」と読む。

### 14.6 見て残したもの

| 候補 | 判定 |
| :-- | :-- |
| §6.4 *"You owe nothing"* に範囲の語が無い | 退いた。§8.4 の *"The grant is necessary because … Section 6.4 alone would leave …"* が本文の答えで、同じ文の前半と §6.5、§5.1 も閉じる |
| §8.6 の *reach* が 2 つの意味 | 退いた。T17 でさらに閉じる |
| §9.2 の *"asserts no right"* が特許や商標を通らない | 退いた。第 3 文が Sections 3 to 8 へ送り、§9.3 と両立しない |
| §12.1 の放棄が虚偽の帰属まで及ぶ | 退いた。§12.2 の末文が、どちらが適用されても許される行為は変わらないと述べる |
| 下流が識別子を置くだけで Dedicator になる | 退いた。§16.2 の *is accompanied* は適用済みの Work の通知の語で、§16.1 は目的と手段の形である。行為で人を Dedicator にするとき、本文は §2.6 のように明記する |
| §2.8 が譲受人自身の権利まで届く | 退いた。§1.4 の Dedicator は適用した者で、§2.8 は *binds* と述べるだけである |
| §5.2(a)(b) が Dedicator 自身の頒布を止める | 退いた。§4.5 は licence が課さないものを述べ、§5 の約束は別の足場に立つ（§2.4）|
| 本文の写しが Work の中を移動すると §16.4 が空になる | 退いた。§16.4 が制限するのは名前と識別子のもとでの頒布で、名前は Covered Rights の外にある（§1.5、§11.1）|
| §8.4 の *in whole or in part* と閾値の否定 | 記録の結論どおり既知の費用である（§13.5、B7）|
| §8.1 の *caused by* と組み合わせの請求項 | 表題の読みは退いた。組み合わせの請求項は既知の費用（B7）として残す |
| §8.5 と独占実施権 | 退いた。§8.5 が §2.7 へ送り、§11.4 が他人の権利を外す |
| §12.2 の発動条件 | 退いた。§1.2 の *incapable of transfer* を §12.2 は *incapable of waiver* に替えている |
| §1.9 の標示に時点が無い | 退いた。§2.2 と §10.4 が撤回を閉じる |
| §1.4 / §2.8 の *patent claim in the Work* が §8.4 より狭い | 退いた。Dedicator から買った者は *assigns* に入る |
| §8.1 の *the Work* が寄与か全体か | 退いた。どちらでも結論が同じになる |
| §5.1 の *payment* に料金の絞りが無い | 退いた。§5.2(b) が別に止める |
| §16.4 の *without charge or permission* | 退いた |
| §8.4 が自動処理か否かで分かれる（OSD 10）| 退いた。T18 で §8.1 と §8.4 の線も語になった |
| 理由の文（§8.4 の 4 か所、§6.5、§9.4、§8.2、§12）| 記録の結論か本文の語で退いた。§8.2 の *policy preference* の語だけ、Berkus 氏の問いとの関係は記録が無い |
| §6.2 の末文 | 外さない。2026-08-23 の修正で足した文で、`faq.md`、`review-doctrine.md`、`jurisdictions.md` が引く |
| §6.4 第 2 文 | 外さない。E4 の防ぎとの関係を確かめていない |
| §11.1 の末文 | 外さない。E7 を閉じた文である |

**次のレンズ（bb）**: Chestek 氏 2026-02-23 は、最初の指摘を *"to demonstrate that there were significant problems in the first few paragraphs, indicating that undoubtedly the drafting problems were throughout."* と述べた。審査者は冒頭の数段落で全体を判定する。§1 と §3、§4 の最初の文を、他より重く読む。

### 14.7 T21: 虚偽の言明と表示（+5 語・2 回目の読み）

同じ 7 視点の方法で、2026-11-07 に変えた語と冒頭の数段落（PREAMBLE、§1〜§4。Chestek 氏の *"significant problems in the first few paragraphs"* と、同じ対象を別の語で述べる草案への *"Why did you add them?"* を視点にした）を読んだ。候補 28 件のうち反証に残ったのは 2 件だった。

**欠陥**: 学習済みモデルの出力を公表することは、§1.7 と §6.1 により許された使用である。その出力が Dedicator について虚偽の事実を述べると、名誉毀損の請求が第 2 肢の *"for a use of the Work that this Dedication permits"* に入り、人格権としての名誉は §5.2(d) の *personality* にも入ると読める。§11.3 の表示は作者・推薦・関係に限られ、虚偽の事実の摘示を含まない。T16 で *for a use* に変えたときは、改変版の中傷は使用に付随するだけの請求として外れると見ていたが、出力の公表は使用そのものだった。

**After**: §5.1 *"for a false statement or representation (Section 11.3)"*、§5.2(d) *"other than for a false statement or representation (Section 11.3)"*。§11.3 の第 1 文 *"This Dedication does not make a false statement true"* の語に合わせた。

**bb の反例で 2 語足した**: *a false statement* だけでは語の陳述に読め、外観やロゴの雰囲気だけで Dedicator との関係を思わせる passing off（英国）が除外から落ちる。これは §11.3 第 2 文の *"Representing that"* の当の場面で、旧い除外 *"a representation Section 11.3 describes"* は入れていた。*statement* だけだと §12.5 の *"conduct falling within Section 11.3"* と同じ §11.3 を別の範囲で指すことになり、#299 の形になる。workflow の案は *"for a false statement of fact about the Dedicator"* を 2 か所に足す形（+18 語）だったが、§11.3 の語へ広げると名指しの数が増えず、語数もほぼ変わらない。

**逆側**: Dedicator は、許された使用の結果であっても、自分についての虚偽の言明を理由に請求できる。不正確な個人データを理由とするデータ保護の請求の一部もここに入りうる。どちらも、学ばれるための著作物を出した人が名誉まで手放すと読める形より、審査者にとって説明しやすい。

**見て残したもの**: §1.9 の *"material sent for discussion only"* は表示を要件にせず、提出者が後から「議論用だった」と主張できると読める。しかし表示があるまで取り込みと推定すると、議論の場にパッチを貼った人が、知らないうちに特許まで含む Dedicator になる（T19 の初案と同じ失敗の向き）。Apache-2.0 も *"intentionally submitted"* の主観の語に表示の除外を添える同じ形なので、残す。他の 26 件は本文の語か記録の結論で退いた（要旨: 第三者を通じた請求は §5.3 と第 1 肢で閉じる / 氏名の publicity は E31 の意図どおり / §8.4 の擬制は Rb′ として記録済み / 定義の循環、§3.1 の公有化、§4.1 の形、*rights in a name* の未定義はいずれも本文の語で閉じる）。

### 14.8 T22: *reach* を §8.3 で 1 回定める（+5 語・審査者の記録された立場を当てた読み）

記録にある審査者 7 人（Chestek、McCoy Smith、Fontana、Piana、Berkus、Perens、佐渡）について、ドシエに逐語で残る発言だけを根拠に、1.4 草案のどこに当たるかを読んだ。本人の判断を作らないよう、根拠は file:行と日付つきの逐語に限った。候補 21 件のうち反証に 4 件が残った。

**欠陥**: §6.1 は *"the patent claims Section 8 reaches"* と請求項の単位で述べる。T17 で §8.3 を行為の単位へそろえたとき、同じ対象を述べる §6.1 を見ていなかった。ある出力 O1 で §8.4 が届いた請求項 Y について、Work の内容から生じていない別の出力 O2 を作り、使い、配る行為まで、§6.1 が *"without condition"* に許すと読めた。Chestek 氏 2019-08-05 *"The are about the same subject matter as"*（`against.md` #299）の形である。

**初案は形を変えた**: §6.1 を §8.3 の語へそろえる案（+8 語）は、bb の反例で、§11.4 の *"the patent claims Section 8 reaches"* が同じ対象を請求項の単位で述べたまま残る（#299 の 2 つ目）と分かった。そろえるとさらに +8 語になる。bb の代案は、§8.3 で届き方を 1 回だけ定め、他の条は今の短い語のまま読ませる形である。

**After**: §8.3 第 1 文 *"Sections 8.1 and 8.4 reach a patent claim only as to the acts they describe. Nothing in this Dedication reserves, preserves, or leaves unaffected any patent claim they reach."*。§6.1 と §11.4 は 1.4 の語のまま。§8.6 の *"in respect of any act that those Sections describe"* とも食い違わない。

**提出資料の訂正**: `submission-reference.md` は、§8.1 の限定が Perens 氏 2024-04-06 の *"necessarily practiced in the work as issued by the grantor"* と「一致する」と書いていた。*necessarily practiced* は請求項の全要素が Work にあることを求めると読め、§8.1 の *caused by* は組み合わせの請求項で広い。§8.4 はこの限定を意図して外している。「同じ種類だが同じ語ではない」へ直した（`review-corpus.md` の同じ主張は bb が PR 2616 で直した）。

**採らなかったもの**: §8.1 の *caused by* を *by itself, infringes* へ狭める案は §8.3 の目的に反し、§8.4 の *teaches* を外す案は記録の Rb′ の判断（巨大なコーパスでは由来を示せない）に反する。

### 14.9 T23: 通知が適用する範囲（+23 語）

**欠陥**: §1.3（1.0 の §1.2）は Work を *"the material to which the Dedicator has applied this Dedication"* と定め、§16.1 は適用を通知を置くことと定める。1.4 で §16.1 がタグや識別子だけの適用を認めたので、タグがどの素材（1 ファイルか、ディレクトリか、全体か）に適用されたかを決める語が要る。§15.1 は適用が成立したかの問いの前に立てない。Fontana 氏 2026-08-16 *"How do you know what the \"covered work\" is?"* の問いの形である（bb が原文で逐語と確かめた）。

**After**: §16.2 の末尾に *"A notice a Dedicator places applies this Dedication to the material it identifies, or, where it identifies none, to the material it accompanies."*

**2 度、形を変えた（どちらも bb の反例）**:
1. 初案 *"A notice applies this Dedication to …"* は、主語が通知なので、置いた人を問わず通知そのものが適用するように読めた。ACD のファイルを別のプロジェクトへ取り込み、タグを残したまま手を入れた人の改変分が、意思なく撤回不能に出る（REUSE などの道具はタグを既定で残す）。置いた人（*a Dedicator places*）を足した。
2. 次に足した時点の語 *"when placed"* は、Dedicator 自身の後の追加を外した。root に LICENSE を一度置いて、その後もコードを足し続けるのが典型の形で、翌年足したファイルが通知を置き直さないかぎり ACD の外になる。外した。

**時点の語が無くても取り込み手の場面は閉じている**: 主語が Dedicator なので、タグを残しただけの取り込み手は通知を置いていない。元の Dedicator の通知が取り込み手の改変分を伴っていても、§2.7 *"This Dedication reaches only rights the Dedicator holds"* により、Dedicator の持たない権利には届かない。他人が同じ repository に入れた寄与は §2.6 の Contribution の規則が扱うので、二重にもならない。

**2 文の順序（bb）**: §16.2 の第 1 文は *"a work to which a Dedicator has applied this Dedication"* を前提にし、第 2 文がその「適用した素材」を決める。逆の順に読んでも（第 2 文が先に範囲を決め、第 1 文がその範囲に通知の効力を与える）結果は同じである。第 2 文の主語は Dedicator が置いた通知で、第 1 文が効力を与えるのも Dedicator が適用した著作物なので、どちらから読んでも範囲は Dedicator の置いた通知で決まる。Chestek 氏の *"Why did you add them?"*（#299）の形の問いには、この 1 行で答える。

**逆側**: root の通知は、Dedicator が後で隣に置いた、公開するつもりのないファイルにも及ぶ。root の LICENSE が repository 全体を覆う慣行どおりで、除外したいものは §2.6 の識別の形で標示する。ただし §3 は取り消せないので、置き間違えの費用は他のライセンスより重い。README だけに通知を置いた Dedicator は、その README が伴う素材の範囲が争点になる。*identifies* で *this project* を名指していれば足り、§16.1 の雛形は *"This work"* と書くので、雛形どおりの通知は概ね足りる。

### 14.10 T24〜T27: 1.3 から変わった 35 条を 1 条ずつ読み直した（+18 語）

確定前の検証（段 7）は 2026-11-06 に済ませたが、そのあと本文は T16〜T23 で変わった。1.3 と比べて文が変わった 35 条を 1 条ずつ担当させ、(1) 変更が他の条の語や前提を壊していないか、(2) 新しい語が理由に書かれていない読みを作っていないか、(3) 変更が閉じようとした欠陥を実際に閉じたか、を読んだ。候補 56 件のうち反証に 6 件が残り、4 件を直した。

| 条 | 欠陥 | 直し方 |
| :-- | :-- | :-- |
| §1.9（T24・+3）| T19 の理由（寄与者は表示を見ている）が語で担保されていない。§10.2 で表示を外したミラーも *"offering the Work under this Dedication"* に当たり、知らない人が修正を送ると Dedicator になる | *"offering the Work with a notice of this Dedication"*。§16.2 によりタグも通知に当たる |
| §8.5（T25・+3）| *"is controlled by the Dedicator if"* は十分条件の形で、通常の意味の control（上流へ料金を払う独占的実施権者など）が並んで残る。§8.5 は §15.1 の射程にあるので、E39 が外した請求項に届く読みが勝つ | *"if, and only if"* |
| §16.2（T26・+13）| 1.4 でタグだけの適用を認めたので、1 つのファイルのタグが *accompanies* でリポジトリ全体を Work にする読みがある。E61 が *in whole or in part* を外して閉じた形が戻る | *"A tag placed in a file as a comment accompanies that file alone."*（SPDX と REUSE のファイル先頭のヘッダと同じ）。初案 *"placed within a file"* は bb の反例で落ちた: package.json の *"license": "ACD-1.4"*、Cargo.toml、pyproject の license 欄はパッケージ全体の宣言をファイルの中に書くいちばん普通の形で、manifest 1 ファイルだけになる |
| §16.4（T27・−1）| *begins with "ACD-"* は、§16.1 と §16.2 が使う *LicenseRef-ACD-1.4* に届かない | *contains "ACD-" followed by a digit*。初案の *or "LicenseRef-ACD-"* は bb の反例（SPDX の外部文書参照 *DocumentRef-x:LicenseRef-ACD-1.4* が漏れる）で変えた。逆側: *ACD-* と数字を含む無関係な識別子も当たるが、制限は ACD の改変した本文を配る場合だけに掛かる |

**逆側**: T24 では、表示のない場への寄与は Contribution でなくなり、取り込むと §2.6 の識別の対象になる。T26 では、ファイル先頭の comment のタグはそのファイルにしか及ばない。manifest の値や LICENSE の本文は comment ではないので、*identifies* か *accompanies* の枝に残る。T27 では、SPDX の *LicenseRef-* は文書ごとの識別子なので、無関係な第三者が自分の別のライセンスに付けても、改変した本文を配らない限り当たらない。

**残したもの**: §2.6 で識別した素材にも §16.2 の既定が及ぶ読み（Dedicator はその素材の権利を持たないので §2.7 で届かず、残るのは Dedicator 自身の編集部分という狭い場面）。§5.2(b) が商標の規約を課すことまで止める読み（規約の対象は商標であって Work ではなく、+27 語の除外に見合わない）。境界は bb が示した: 規約が「fork はロゴのファイルを Work から外せ」と求めると、ロゴのファイルは Covered Rights の対象で §4 が許諾済みなので、それは *"an obligation in respect of the Work"* になり §5.2(b) が塞ぐ。名前を変えろという求めは商標法そのもので、§5.1 の除外の側に残る。

### 14.11 T28・T29: §16 を実務の 5 つの立場で読んだ（+47 語）

SPDX 法務、REUSE の保守者、npm・Cargo・PyPI の保守者、Debian・Fedora の法務、企業の OSPO の 5 つの立場で、§16 と、それに関わる §1.3・§1.9・§2.6・§5.2 を読んだ。候補 18 件のうち反証に 7 件が残った。

**T28 §16.2（+38 語）**: T26 の *"A tag placed in a file as a comment accompanies that file alone."* は、次の 3 つを拾えなかった。
- REUSE の付属ファイル（*logo.png.license* の中のタグは comment ではないので *accompanies* の枝に落ち、範囲が決まらない）
- 断片の印（*SPDX-SnippetBegin/End* で囲んだタグが、ファイル全体に及ぶ）
- 優先（REUSE.toml の *path = "\*\*"* の ACD や Cargo workspace の root の宣言が、Dedicator 自身が別条件のヘッダを置いたファイルまで覆う）

workflow は 1 件ずつ 1 文足す案（計 +56 語）を出したが、§16.2 が REUSE の写しになり、慣行が変われば食い違う。慣行を名指さない一般の語でまとめた: *"… to the material it identifies, whether by its words, by its place in a comment within a file, by a file name that refers to other material, or by markers that delimit part of a file, or, where it identifies none, to the material it accompanies. It does not apply this Dedication to material that a narrower notice the Dedicator has placed assigns to other terms."* 語はどれも一般の語で、外部の文書を参照しないので、Chestek 氏 R2 の self-contained の線に触れない（bb の確認）。

**bb の反例で変えた語**: 初案の *"by its place at the head of a file"* は、ファイル末尾の comment に SPDX の行を置く形式（Markdown の HTML comment など）を落とし、E61 の形が戻る。*within a file* に広げると、root の LICENSE（名前と版で参照するので通知に当たる）が自分自身しか名指さなくなる。*"in a comment within a file"* にすると、comment の中のタグは位置を問わずそのファイルを名指し、LICENSE の本文や manifest の値は *by its words* か *accompanies* の枝に残る。

**逆側**: Dedicator が後で別条件のファイルを ACD へ移したいときは、そのファイルのヘッダを変える必要がある。誤って撤回不能に出さないための保守的な既定である。寄与者が自分のファイルに置いた別条件のヘッダは *the Dedicator has placed* に入らないが、§2.6 の *unless they state otherwise* と §2.7 で閉じる。SPDX 式 *ACD-1.4 AND Apache-2.0* でラベルが無い場合はパッケージ全体という 1 つの結果に決まり、ACD の側が広く出す向きなので受領者に不利にならない。

**T29 §1.9（+9 語）**: T24 の *"offering the Work with a notice of this Dedication"* では、社内のモノレポに通知ごと vendor した ACD のコードへ従業員が変更依頼を出すと、会社が Dedicator になり、改変と §8 の特許を出す読みがあった。初案の *"to the public"* は bb の反例で落ちた。非公開で 1 年開発してから ACD で公開するチームでは、公開前の仲間の寄与が全部 Contribution でなくなり、§2.6 の第 2 文により公開前の履歴全体を ACD の外と標示する約束が出る。*"to the public, or to those invited to contribute"* にした（*those it invites* の *it* は文の上では repository を指すので、bb の直しで受け身にした）。招かれた協力者は入り、vendor した会社の従業員は Work への寄与に招かれた者ではないので外れる。

**残したもの**: §5.2(a)(b) を Dedicator 自身の製品（ライセンスキー、EULA）に当てる読みは、§5.2(a) の広さとして以前「変えない」と判断した線にある。SPDX が付ける識別子、*LicenseRef-* の局所性、XML 化、草案の例外、本文の写しを通知と読む読みは、本文の語か記録の結論で退いた。

### 14.12 関連会社が持つ特許（変えない・#310）

**問い（bb・`against.md` #310）**: 2012-02 の CC0 の審査中、Russ Nelson 氏は *"Anybody who wants to set a booby trap will take steps to make sure that a separate legal entity owns the patent rights"* と述べた。1.4 の §8.5 は *controlled* を Dedicator 自身が許諾できる権利に限るので（T25 で *if, and only if* にした）、関連会社が持つ請求項には §8 が届かない。

**比べたもの（手元の本文で確かめた）**: Apache-2.0 は *Legal Entity* を *"the union of the acting entity and all other entities that control, are controlled by, or are under common control with that entity"* と定め、許諾者をこの単位で数えるので、関連会社の請求項に届く。UPL-1.0 は *"owned or freely licensable by each licensor"*、BlueOak-1.0.0 は *"patent claims they can license or become able to license"*、BSD-2-Clause-Patent は *"licensable by such copyright holder or contributor"* で、どれも関連会社には届かない。

**判断: 変えない。** 理由は 3 つ。(1) 適用していない会社を Dedicator の行為で縛ることになり、§2.7 *"This Dedication reaches only rights the Dedicator holds"* と食い違う。Apache-2.0 は許諾者の定義そのものを企業群に広げることでこれを避けているが、ACD の Dedicator は適用した者ごとに数える（§1.4）。(2) 適用の後に関連会社へ移した請求項は、§2.8 の譲受人の拘束に入る。Dedicator が自分の請求項を持ったまま関連会社に主張させる形は、§8.6 の *"not to authorise or assist any other person to assert"* が塞ぐ（bb の補足）。§8.6 の対象は *"the patent claims that Sections 8.1 and 8.4 reach"*、つまり Dedicator の請求項なので、関連会社が自分で持つ請求項には届かない。罠として残るのは、適用の時点で関連会社が既に持っている請求項である。(3) UPL-1.0、BlueOak-1.0.0、BSD-2-Clause-Patent と同じ側に立つ。

**逆側**: 審査者が Apache-2.0 と比べると、この 1 点で ACD は狭い。§8 を Apache-2.0 より広いと書く面では、この点を併記する。Dedicator が関連会社に主張させない約束を足す案（§8.6 の *authorise or assist* を関連会社へ広げる）は、効くかどうかが法の問いなので、法律家への問 2 の (i) に置いた。

### 14.13 T30〜T33: 機械学習の実務の 5 つの立場で読んだ（+78 語）

モデルハブのカードを書く者、ウェブ規模のデータセットを編む者、企業でモデルを学習させる者、推論 API を提供する者、学習済みモデルを公開する研究者の 5 つの立場で、§6・§8.4・§9・§16 とそれに関わる条を読んだ。候補 18 件のうち反証に 3 件が残った。どれも裁判所が OSD に反して読む余地を作るものではなく、採用者の障害（B2）である。

**T30 §5.2 末尾の第 1 文（+42 語）**: 保守者がデータセット D を ACD で出し、D で学習した自分のモデル M を非商用の独自ライセンスで出す。第三者が M を商用で配ると、M の配布は §1.7 により Computational Use で、§6.1 が許す use なので、§5.1 第 2 肢が M の著作権に基づく請求まで塞ぐと読めた。データだけを ACD で出すという、ACD に最も合う使い方を妨げる。初案（§5.1 の除外に *"under a right in material other than the Work"*）は bb の反例で足りなかった: §5.2(b) は M の非商用の条件を、§5.2(a) は M の登録制の配布を、同じ理由で止める。bb の案 *"Section 5 does not reach a right in, or a measure or term concerning, material other than the Work …"* は、25 が逆の穴を見つけた: 第三者が D で学習したモデルの出力も「Work 以外の素材」なので、Dedicator がダウンロードの利用規約で「このデータで学習したモデルの出力を使うな」と課せてしまい、§5.2(b) の条件ゼロが崩れる。Dedicator 自身が出す素材に絞った: *"the Dedicator's rights in material, other than the Work, that the Dedicator itself makes available, or the terms or measures it applies to that material"*。最初に書いた *separately from the Work* は、データ D とモデル M を同じ repository で配り、M にだけ狭い通知で非商用の条件を付ける普通の形を落とすので（bb の反例）、*other than the Work* にした。

**T31 §5.2 末尾の第 2 文（+24 語）**: Dedicator が同じモデルを重みで公開しつつ、自社の推論 API に API キー、登録、AUP を置くと、§5.2(a) の *"technological measure that restricts access to or use of the Work"* と (b) の *"terms of service … registration requirement"* に当たると読めた。§5.1 の *"a payment You agreed to make"* とも食い違う。初案 *"not a service through which the Dedicator puts the Work to use"* は bb の反例で落ちた: 重みのダウンロード自体を API キーと登録の後ろに置き「Work を使わせるサービスだ」と言えば、§5.2(b) が名指しで禁じる登録の要件が戻る。*"runs the Work for others without providing a copy of it"* にして、写しを渡す入口を (a)(b) の中に残した。

**T32 §16.2（+9 語）**: Hugging Face の一覧に ACD は無く、*license: other* と *license_name* で書く（`gap-measurements.md` §1.151）。慣行どおり小文字の *acd-1.4* と書くと、*the identifier "ACD-1.4"* に当たるかが決まらない。*"The identifiers named above match without regard to case."* SPDX も識別子の照合で大小を区別しない。*"Section 16 matches identifiers …"* として §16.4 まで効かせると、*contains "ACD-"* が無関係な識別子の一部（*LicenseRef-Abacd-3* の *acd-3*）まで縛るので（bb の反例）、§16.2 が名指す識別子に限った。

**T33 §6.4（+3 語）**: §6.4 の後半 *"You owe nothing in respect of any of them"* には範囲の語が無いので、§5 の外に出しても、Dedicator 自身の推論 API の出力（重みを動かした結果なので *output resulting from Computational Use of the Work*）に付けた条件に *You owe nothing* が立つと読めた（bb の指摘）。前半の *under this Dedication* と同じ範囲にそろえ、*"You owe nothing under this Dedication in respect of any of them"* にした。最初の読み（§14 の 1 回目）で、*You owe nothing* の範囲の無さは「§8.4 の文と §6.5 で閉じる」として退いていたが、それは特許と合意した料金についての反証で、別に置いた契約の条件の場面は見ていなかった。

**逆側**: T30 で、Dedicator 自身のサービスが出す出力に Dedicator が課す条件は §5 の外に出る。Dedicator が別に出す素材と同じ扱いである。bb は、API の AUP の出力条項を Dedicator が強制できない方が「Work の使用に条件を付けない」の筋に合うと考えたが、25 は、公開した重み（Work）の使用が無条件のまま残り、サービスは Work とは別の提供なので、強制できる側を採った。本文の上でこれを通すには T33 の §6.4 の範囲が要る。法律家に確かめる点として、問 5 の範囲に関わる。§8.4 の特許の許諾は Dedicator 自身の M にも及ぶ（*"any model … resulting from Computational Use"*）が、M の著作権が残れば複製は止められるので害は小さい。

**残したもの**: カードの YAML の license 欄、safetensors や GGUF の中のメタデータ、§2.6 と §16.2 の重なり、後から足した opt-out の信号（§2.2 と §6.3 が閉じる）、§6.3 の撤回が ACD の外の作品に及ぶ読み、第三者の素材と opt-out の見分け（§2.7・§6.5）は、本文の語か記録の結論で退いた。

### 14.14 今日の修正どうしの食い違いを読んだ（本文の変更なし）

2026-11-07〜08 に入れた修正（T16〜T33）が互いに食い違っていないかを、5 つの組で読んだ。§16.2 と §2.2（撤回不能）、§5.2 の末尾の 2 文と §5.1・§5.3・§6.4、§8 の全体、寄与の組（§1.9・§2.6・§16.2・§2.7・§1.4）、冒頭の変更一覧と本文の一致である。候補 20 件はすべて反証で退いた。主なものは次のとおり。

- 後から置いたより狭い通知が、既に献呈した素材を Work から外す読み: §16.1・§16.2 は適用を通知を置く行為に結びつけ、§1.3 の *has applied* は現在完了で、§2.2・§3.1・§10.4 が撤回を禁じる。
- 別の Dedicator の狭い通知が他人の献呈を外す読み: §1.4 の *severally* と *to the extent that person … holds*、§4.6 で閉じる。
- §5.2 の末尾の文が承継人に Work の制限を戻させる読み: 主語が *material, other than the Work* で、束の中の Work の写しは Work のままである。
- §8.5 の *at the time in question* と *now or in future* の食い違い: 時点ごとに判定するので食い違わない。

**冒頭の一覧の誤りは 3 か所直した**（本文の語は変えていない）。§5.2 の項目は「サービスを Section 5 の外に置く」と読めたが、本文が外すのは (a)(b) だけなので *outside paragraphs (a) and (b)* と書いた。E40 の項目は T17 で置き換わった動名詞の列を本文の語として引いていたので、引用を外した。E39 の項目の *the right to license* は本文の *the right to grant these licences* より広いので、本文の語にした。


### 14.15 T34: §9.2 の第 3 文の列挙を外し、§11.4 の語に結ぶ（−1 語）

**Before**: *"Where a right subsists, or is later held to subsist, Sections 3 to 8 and Section 12 apply to it in full."* / **After**: *"Where a right that this Dedication reaches subsists, or is later held to subsist, this Dedication applies to it in full."*

**欠陥**（bb が ARL の議論 `reviewer-positions.md` §1.155 を読んで当てた反例・2026-11-08）: (A) 列挙は §5 を「権利がある場合に働く節」の側に置く。権利の無い Machine-Generated Material の配布をクリックスルーの後ろに置いても §5.2(b) は及ばない、と読める —— 条件を付けない約束がいちばん要る場面で外れる形である。(B) 列挙は §13・§14 を挙げない。権利の無い部分の欠陥で損害を受けた人が、第 2 文と第 3 文を並べて「その部分には免責が及ばない」と主張できる。ARL の議論で出た「著作権に依拠する許諾が崩れると免責も崩れる」と同じ形である。どちらも強い読みではない。§11.4 の *"the covenants in Section 5 are promises about the Dedicator's own conduct"*、§13.1 の *"WITHOUT WARRANTY OR CONDITION OF ANY KIND"*、§13.2 の *"DOES NOT WARRANT THAT ANY RIGHT SUBSISTS IN THE WORK"*、§15.1 が反対の読みを支える。

**由来**: 1.0 から在る文で、1.0〜1.3 で変わっていない。1.3 は errata E37 で第 2 文を *"as to that right"* に限り、E37 は「§8 と §5.2 は権利が無くても働く」と書いた。第 3 文の列挙はその読みの残りで、E37 のときは第 2 文だけを §5.2 と §8 に当てていた。1.0 の errata なので E 番号は bb が付ける。

**最初の 2 案を退いた理由**: (1) bb の案 *"Section 5 and Sections 13 and 14 apply whether or not any right subsists."*（+12 語）は、新しい列挙が §2・§10・§15・§16 を挙げないので、同じ形の推論を別の場所に作る。(2) 列挙を外して *"this Dedication applies to it in full"* とする案（−5 語）は、第 1 文の *"any right"* に商標や人格の権利が入るので、*"in full"* と §15.1 の広い読みが組んで §11.4 の *"It reaches nothing else"* と衝突する（25 が立てた反例）。*"a right that this Dedication reaches"* は §11.4 の語で範囲を閉じる。

**効果**: 許諾の範囲は変わらない。第 3 文が働く節を名指さなくなるので、名指されない節が権利の無い部分に及ばないという推論の足場が消える。§3・§4・§12 は自分の文で Covered Rights と Moral Rights に限られているので、旧文の列挙が運んでいた範囲は §11.4 の *reaches* が運ぶ。`measure_clause_overlap.py --compare`: 条 +0 / 語 −1 / 重複 +0 / 先行詞の無い指示語 0。`--guard`: 468u の目印 17 件がすべて残る。

**逆側**: (1) 旧文は、どの節が権利に働くかを 1 文で示していた。新文の読者は §11.4 まで読まないと何が届くかが分からない。(2) *reach* は §8.3 で特許の請求項について定め（T22）、§11.4 で献呈全体について使う。§9.2 の用法は §11.4 の方である。(3) 外向きの文書 3 か所が旧文を引く（`submission-reference.md` 91–92、`review-responses-clauses.md` 545）。どれも 1.0 の文として正しいので、切り替えの日の表に行を足す。(4) 第 2 文と組んで「権利が無ければ何も働かない」と読む筋は弱くなるが、消えはしない。残りは第 2 文の *"as to that right"*（E37）が担う。

**先に登録する反例（bb へ）**: (a) *"a right that this Dedication reaches"* が、権利の有無に加えて「reach するか」の判定を受領者に求めると読まれ、§9.3（判定を求めない）と食い違うか。(b) *"this Dedication applies to it in full"* が §12 の *"to the extent stated"* の限定を外すと読まれるか（§9.2 の旧文も *"Section 12 apply to it in full"* だった）。(c) 後に権利が生じた部分に、§2.2 の撤回不能と §16 の適用がどう掛かるか（旧文は §2 を挙げていなかった）。(d) (A)(B) が新文でもなお立つか。

**採否（2026-11-08・採った。ただし *"in full"* を外した形・−3 語）**: bb の反例のうち (b) が立った。後に Machine-Generated Material に Moral Rights が成り立つと判断された場面で、*"this Dedication applies to it in full"* を §15.1 の「受領者に多く与える読み」で読むと、§11.4 の *"Moral Rights to the extent stated in Section 12"* と §12.5 の除外を *"in full"* が越える読みを §15.1 が選ぶ。§9.2 の旧文は *"Section 12 apply to it in full"* で、§12 を全部当てる意味だったのでこの問題は無かった。*"in full"* が担っていた「一部だけ当てるのではない」は、*"a right that this Dedication reaches"* と各節が自分の範囲を持つことで足りるので外した。(a) は立たない（条件は権利が在るかで、受領者の判定ではない。権利が無ければ受領者は第 2 文でもともと自由なので §9.3 は崩れない）。(c) も立たない（後に在るとされた権利は作成時から在ったことになり、§2.2 と合わせて適用の日から及ぶ。新しく生じる権利は *subsists* の現在形と §1.5 の *"whether or not presently subsisting"* が拾う）。(d) は (A)(B) とも新文で足場が消え、残る第 2 文は *"as to that right"* が §5.2(b) の約束と §13・§14 の免責を外す。`--compare`（*in full* を外した形）: 条 +0 / 語 −3 / 重複 +0 / 先行詞の無い指示語 0、`--guard`: 468u の目印 17 件すべて残る。冒頭の一覧、`This draft` の語数、CHANGELIST の本表の行と語数の内訳、切り替えの日の表の行を同じ commit で直した。E 番号は bb が付ける。

### 14.16 T35: §1.9 の語順（0 語）

**Before**: *"… to a repository or forum offering the Work to the public, or to those invited to contribute, with a notice of this Dedication, for inclusion in the Work."* / **After**: *"… to a repository or forum offering the Work, with a notice of this Dedication, to the public or to those invited to contribute, for inclusion in the Work."*

**欠陥**（bb が逐条リファレンスの下書きの §1.9 の行を本文に当てて見つけた・2026-11-08）: T29 が提供の相手を *offering the Work* と *with a notice* の間に挟んだので、カンマの位置から *"or to those invited to contribute"* を *submits* の 3 つ目の宛先と読み、*"with a notice of this Dedication"* をその最後の肢だけに掛ける読みが立つ。その読みでは公衆に提供する repository / forum に通知の要件が掛からず、T24 が閉じた「通知を外したミラーへの提出で、ACD を見ていない人が Dedicator になる」読みが戻る。§15.1 の *"the reading that grants more to You prevails"* は、寄与を広げるその読みを選ぶ。招かれた共同開発者へ私的に送った変更が寄与になる読みも同時に立つ。

**由来**: 1.4 草案で生まれた文（T19・T24・T29 の順に足した）。1.0〜1.3 には無いので errata ではない。

**採った形**: bb の案 *"that offers the Work, with a notice of this Dedication, to the public or to those invited to contribute"*（+1 語）の語順を、分詞 *offering* のまま取った（0 語）。通知が *offering* の隣に戻り、提供の相手 2 つがカンマ無しで続くので、*to those invited* を *submits* の宛先と読む足場が消える。`measure_clause_overlap.py --compare`: 条 +0 / 語 +0 / 重複 +0 / 先行詞の無い指示語 0。§1.9 を参照する箇所は §2.6 の 1 か所で、除外の参照なので影響しない。`--guard`: 468u の目印 17 件すべて残る。

**逆側**: 挿入句（*with a notice of this Dedication*）が名詞句の途中に入るので、1 文の中の区切りが増えて読みにくい。*"to the public"* が *notice* に掛かる（公衆への通知）と読む筋は、意味が「公衆に提供する」とほぼ同じになるので害が無い。冒頭の一覧の E65 の項目、CHANGELIST の §1.9 の行、逐条リファレンスの §1.9 の行を同じ commit で合わせた。

### 14.17 AI の語の流動と、*model … or output* の列挙（変えない）

**問い**（bb が ModelGo v2 の審査から持ってきた・2026-11-08）: Chestek 氏は ModelGo の 2 回目の再提出に対して *"One thing to worry about is that the vocabulary for AI is fluid and constantly changing. You might not consider an "agent" a "model" at the moment, but might it take on more model-like characteristics in the future?"* と述べた（`license-review` 2025-12-06・アーカイブの 2025-December で逐語を確かめた）。ACD への発言ではない。§1.7・§6.4・§8.4 は *"model, parameter set, weight, embedding, or output"* と列挙し、*model* は定義語ではない。エージェント（モデルとツールとプロンプトの組）、検索用の索引、tokenizer が列挙のどれかに入るかは語で決まらない、という指摘である。

**読み**: 列挙の末尾は *"output resulting from that processing"*（§1.7）・*"output resulting from Computational Use of the Work"*（§8.4）で、何が入るかは呼び名ではなく因果で決まる。§1.7 の処理は *"indexing, retrieval"* と学習の全工程を含むので、Work を索引した索引、Work から作った tokenizer の語彙、エージェントの中のモデルは、どれもその処理の結果である。エージェントのうち Work の処理から生じない部分（利用者が書いたツールのコードやプロンプト）は、もともと Dedicator の許可を要しない。*output* を推論の出力（生成された文）に狭める読みは立ちうるが、§6.4 と §8.4 はどちらも You に与える側の条なので、§15.1 の *"the reading that grants more to You prevails"* は広い読みを選ぶ。

**変えない理由**: *"or other artefact resulting from …"* のような受け皿を足すと、(1) 足した語があるせいで *output* は推論の出力に限られる、という反対解釈を本文自身が作る（列挙に別の受け皿が在るなら *output* は受け皿ではない）、(2) §8.4 の特許の伸びを語の上で広げて見せる（B7 の費用）。現在の文は受け皿を *resulting from* の因果に置いており、語の流動に対しては呼び名に依らないこの形の方が耐える。

**逆側**: (1) 審査者が *output* を狭く読めば、索引や tokenizer の扱いを §15.1 に頼ることになる。§15.1 は *"that its words allow"* の範囲でしか選ばない。(2) 列挙の費用は、Chestek 氏自身が同じ ModelGo の最初の再提出で、権利の列挙について *"when you enumerate, then you risk failing to grant rights under some regime that has different enumerations"* と述べている（`license-review` 2025-05-14・アーカイブの 2025-May で逐語を確かめた）。列挙して漏れる危険と、列挙しないで何が入るか分からない危険の間の選択で、どちらにも費用がある。ACD は列挙のあとに因果の受け皿を置いて、両方を小さくしようとしている。(3) 法律家に確かめる点として、`QUESTIONS-FOR-COUNSEL.md` 問 2（§8.4 が何に届くか）の範囲に入る。

### 14.18 T36〜T45: 逐条リファレンスの行を本文に当てた読み（候補 47・反証で残った 10）

bb が §1.9（T35）で見つけたレンズを 80 条に当てた（2026-11-08・節ごとの読み手 16 と候補ごとの反証役 46・Explore/opus）。逐条リファレンスの行が述べる読みを、本文の語だけを持つ敵対的な読み手が取るか、§15.1 が別の読みを選ばないかを見た。47 候補のうち 1 件は既に記録があって外し、46 件に反証を当てて 10 件が残った。読みであって、法律家の判断ではない。

| T | 条 | 立つ読み（要約） | 試作（語数） | 25 の判断 |
| :-- | :-- | :-- | :-- | :-- |
| T36 | §1.9 Dedicator の肢 | *"to the Dedicator"* の肢には通知と提供の相手の限定が掛からない。§2.6 で寄与者も Dedicator になり、§15.5 で単数は複数を含むので、過去の寄与者へ私的に送った変更も寄与になる。通知を見ていない人が撤回不能に Dedicator になり、特許も出す | *"to a Dedicator, repository, or forum offering the Work, with a notice …"*（−2）。限定を明示する形は *"to the Dedicator or to a repository or forum, in either case offering the Work, …"*（+3） | 採る方向。どちらの形かは bb の反例で決める |
| T37 | §2.6 第 2 文 | *"and that material is included with the Work"* は受動で、誰が含めても Dedicator が識別の約束を負う（もう関わっていない Dedicator も） | *"a Dedicator who includes that material with the Work will identify it"*（−1） | 採る方向。逆側: Dedicator でない保守者が含めたときは誰も負わない（T19 の空白が語に出る） |
| T38 | §5.2 末尾の除外 | *"that the Dedicator itself makes available"* は公開しないモデル（社内に留める）を外す。そのモデルに §5 が及び、Dedicator は自分の非公開のモデルの権利を主張できない読み | *"makes or makes available"*（+2） | 採る方向 |
| T39 | §5.2(d) | *"other than for a false statement or representation (Section 11.3)"* が直前の *use* に掛かり、虚偽の言明「のための使用」だけを外す読み（T21 で閉じた欠陥が戻る） | 除外を (d) の冒頭へ移す（0 語） | 採る |
| T40 | §10.3 第 2 文 | 第 2 文に範囲の語が無く、第 1 文の *"wherever expressed and however phrased"* と組んで、Dedicator 自身のサービスの条件（AUP・API キー・登録）まで「義務を作らない」と読める。T30・T33 で強制できる側を採った判断と食い違う | *"Under this Dedication, it creates no obligation, …"*（+3・E70 と同じ語） | 採る |
| T41 | §11.3 第 2 文 | 改変した file に Dedicator の元の著作者表示を残すことが「Dedicator が著作した」という表示に当たるかが語で決まらない | *"or that an altered work is the Dedicator's unaltered work"*（+9） | 保留。除外を広げると §10.2（改変を表示しなくてよい）と緊張し、条件に近づく。bb の反例と法律家への問いへ回す |
| T42 | §14.1 | 主語 THE DEDICATOR は §1.4 で権利を持つ範囲に限られるので、保守者は自分が権利を持たない部分（寄与者のコード・第三者の素材・権利の無い機械生成物）について免責されない読み。E72 の免責の論点と同じ場所 | *"… OR THE USE OF THE WORK, INCLUDING ANY PART IN WHICH THE DEDICATOR HOLDS NO RIGHT, EVEN IF …"*（+9） | 採る方向 |
| T43 | §15.1 第 2 文 | *"in respect of the Work"* は第 1 文の主語にしか掛からず、第 2 文の解釈規則が §16.4（名前の保護）にも及んで、改変した本文を配る者に有利に読む | 2 文をつなぎ、第 1 文の主語で両方を受ける（+3）。第 2 文に *"in respect of the Work"* を足す形（+5） | 採る方向（+3 の形） |
| T44 | §16.4 第 3 文 | 識別子は *"any identifier that contains"* なのに名前は *"the name"* で、対比から「名前を含む別の名前」（"… Dedication Plus" など）は許されると読める | *"under any name that contains "Autonomous Commons Dedication""*（+2） | 採る |
| T45 | §16.5 | *"and any person or entity to whom that role is assigned"* は累積で、譲渡したあとも最初の公表者と譲受人の両方が Steward になる | *"or, after an assignment, the person or entity to whom that role was last assigned by"*（+4） | 採る方向。逆側: 共同の Steward を置けなくなる |

**語数**: T41 を除き、T36 を −2 の形、T43 を +3 の形で採ると +20 語（B3 の費用）。

**次**: bb が各行に反例を当て、5a が `measure_clause_overlap.py --compare / --guard` で比べ、残ったものを本文・冒頭の一覧・CHANGELIST・逐条リファレンスに入れる。各文が 1.0 に在るかを採る前に確かめ、在れば errata、1.4 で生まれた文なら SELF-AUDIT か記録に振る（T38 の除外は T30、T39 の除外は T21 で 1.4 に入った文）。

**採否（2026-11-08・8 件を採った・+22 語）**: bb の反例と 5a の比較（10 件とも条・重複・先行詞の無い指示語は +0、mutation の anchor に当たる試作は無い）のあとで決めた。

- **T36** は +3 の形（*"in either case offering the Work"*）を採った。−2 の形は 3 項の並びの後ろに分詞が付くので、直前語の原則で *offering* が forum だけに掛かり、T36 と T24 の読みが両方戻る（bb）。過去の寄与者を宛先から外して失うものは無い（**§14.22 (1) で訂正**: 寄与を招かずに写しを渡すだけの Dedicator と、もう提供していない Dedicator も外れる）—— 通知の前は §1.4 の Dedicator がいないので、まだ通知を置いていない単独の作者への寄与は今も入っていない。非公開の repository に通知を置いた後の招いた協力者は *"to those invited to contribute"* で入る（bb）。
- **T37** は bb の *"or causes it to be included"* を足した形（+5）。merge を bot や別の保守者に任せた Dedicator が約束を避ける読みを閉じる。*"binds the Dedicator"* も *"binds that Dedicator"* にした（0 語）。
- **T38**（+2）。468u の §5.2 の目印を新しい語へ同じ commit で替えた。
- **T39**（0 語）。§5.1 第 2 文は同じ形だが、除外の列が *under trademark rights* を含み *use* に掛からないので、列が *claim* に掛かることを示す。§5.1 は変えない（bb の問いへの答え）。
- **T40** は第 2 文だけに足す案を改め、2 文を 1 文にして *"Under this Dedication,"* で両方を受けた（+3）。第 2 文だけでは、第 1 文が Dedicator 自身の API の条件を「request であって condition ではない」と宣言したまま残る（bb）。
- **T43** は 2 文をつなぐ形（+3）。bb の「解釈規則を許可に絞る」案は、寄与を広げる読みも許可を多く与えるので T35・T36 の根は消えないと見て、採らずに別に読む。
- **T44**（+2）。外向きの文書 4 か所が *"under the name …"* を引くので、切り替えの日の表に行を足した。bb が別に挙げた §16.4 の識別子の大小の区別（小文字の *acd-1.5*）は、T32 で誤検出（*LicenseRef-Abacd-3*）を理由に §16.2 に限った経緯があるので、別に読む。
- **T45**（+4）。§15.5 により 1 回の譲渡で共同の Steward も置ける（bb）。
- **採らなかったもの**: T41（§10.2 と緊張する・法律家への問いへ）と T42（bb の反例: §1.4 が Dedicator を権利を持つ範囲に限るので、*"INCLUDING ANY PART IN WHICH THE DEDICATOR HOLDS NO RIGHT"* は自己矛盾の文になる。主語を §1.4 の限定の外で立てる形を含めて別に読む）。

**errata と記録**: T36・T40・T44 の文は 1.0 に在り、T43 は E20 の残りなので、errata の番号は bb が付ける。T37 と T45 は 1.1 で入った文なので `ACD-1.1-SELF-AUDIT.md` §3y に書いた。T38・T39 は 1.4 で入った文（T30・T21）。

### 14.19 T42 を変えない理由（§14.1 の免責の主語・2026-11-08）

**問い**（§14.18 の T42）: §14.1 の主語 *THE DEDICATOR* は、§1.4 が Dedicator を *"to the extent that person or entity holds or may hold Covered Rights, Moral Rights, or patent claims in it"* と定めるので、保守者が権利を持たない部分（寄与者のコード・第三者の素材・権利の無い機械生成物）については保守者を免責しない、という読み。

**変えない理由**: (1) §13.2 は *"THE DEDICATOR DOES NOT WARRANT … THAT THE DEDICATOR HOLDS ANY RIGHT IN IT"* と書く。本文自身が、権利を持たない Dedicator を想定して §13・§14 の主語にしている。§1.4 の *to the extent* が「何を献呈するか」の範囲であって、§13・§14 が誰を守るかの範囲ではないことを、隣の条が示している。(2) 25 の試作（*"INCLUDING ANY PART IN WHICH THE DEDICATOR HOLDS NO RIGHT"*・+10 語）は、bb の反例どおり、その部分については Dedicator でない者の免責を「Dedicator は」で述べる自己矛盾の文になる。(3) bb の案（主語を *"NO PERSON WHO HAS APPLIED THIS DEDICATION"* にする）は、§2.6 で Dedicator になった寄与者（適用ではなく提出で Dedicator になる）を外す読みを作る。(4) Apache-2.0 §8 は主語を *"shall any Contributor be liable to You for damages"* とし、Contributor を *"Licensor and any individual or Legal Entity on behalf of whom a Contribution has been received by Licensor and subsequently incorporated within the Work"* と定めるので、配布する Licensor を Work 全体について守る形を語で持つ。ACD は同じことを §13.2 との組で言っている。

**逆側**: §13.2 との組で読むのは解釈であって、§14.1 の語だけでは閉じない。§15.1 の解釈規則は You に多く与える読みを選ぶので、免責を狭く読む主張の足場は残る（T43 で §15.1 の解釈規則にも「in respect of the Work」が掛かるようにしたが、免責は Work についての条でもある）。法律家への問いとして `QUESTIONS-FOR-COUNSEL.md` 問 9 (b) に置いた。さらに、§13.2 の否認は権利を一部の部分にしか持たない Dedicator とも両立するので、§1.4 の *to the extent* が主語を権利のある部分に絞る読みを語の上では否定しない（bb・2026-11-08）。免責条項を厳格に読む法域では、§13.2 との組の読みが採られない可能性がある —— 受領者が消費者なら、不公正条項指令 93/13 の第 5 条（疑わしい条項は消費者に最も有利に解釈する）が曖昧な主語の免責を狭い方へ読ませる（`ACD-1.0.jurisdictions.md` §9a で原典を読んでいる）。

### 14.20 T46: §16.4 の識別子を大小を区別せずに照合する（+3 語・試作）

**Before**（§16.4 第 3 文の全文）: A modified text may not be distributed under any name that contains "Autonomous Commons Dedication" or under any identifier that contains "ACD-" followed by a digit, except by the Steward (Section 16.5), and by the Steward only as a new version under a version number and identifier that no earlier text, other than a draft identified as such, has borne, so that each name and identifier in this family continues to denote one fixed text.

**After**（同じ文の全文）: A modified text may not be distributed under any name that contains "Autonomous Commons Dedication" or under any identifier that contains "ACD-", regardless of case, followed by a digit, except by the Steward (Section 16.5), and by the Steward only as a new version under a version number and identifier that no earlier text, other than a draft identified as such, has borne, so that each name and identifier in this family continues to denote one fixed text.

**欠陥**（bb が T44 の反例で挙げた・2026-11-08）: §16.4 の照合は語のとおり大小を区別するので、改変した本文を小文字の *acd-1.5* で配ると制限を素通りする。Hugging Face などは識別子を小文字で書く（T32）。後に Steward が ACD-1.5 を出すと、その版の §16.2 は大小を区別せずに照合するので、*acd-1.5* の札が付いた作品はどちらの本文を指すかが割れ、*"so that each name and identifier in this family continues to denote one fixed text"* が崩れる。

**T32 との違い**: T32 は大小を区別しない規則を §16.2 に限った。§16.2 で *contains "ACD-"* を大小無しに読むと、無関係な識別子（*LicenseRef-Abacd-3* の *acd-3*）の付いた作品まで ACD の通知を受けたことになり、害が大きいから（bb）。§16.4 で同じ誤検出が起きても、縛られるのは **この Dedication の本文を改変したもの** の名前だけで、改変した本文を *abacd-3* と名付けたい者が別の名前を選べばよい。害は小さい。

**語の選び方**: *"in any case"* は「いずれにせよ」とも読めるので *"regardless of case"* にした。*"in upper or lower case"*（+5）は混在（*Acd-*）を外す読みを作る。

**逆側**: (1) +3 語（B3）。(2) §16.2 と §16.4 で照合の規則が違う理由が本文からは読めない。§16.2 は大小を区別しない規則を *"The identifiers named above"* に限っており、§16.4 は自分の文で述べるので、読み違いは起きにくいと見る。(3) 識別子の区切り（前が英字かどうか）までは決めない。

**先に登録する反例（bb へ）**: (a) *regardless of case* が *followed by a digit* に掛からず、数字の側の書式まで広げると読まれるか。(b) 翻訳の文（§16.4 の *"the name and the identifier"*）との関係。(c) 識別子に *ACD-* を含む既存の別のライセンスやプロジェクト名の例（大小を問わず）を、改変した本文の名前として縛ることの実害。

**bb の反例（2026-11-09）**: (a) *regardless of case* が *followed by a digit* に掛かっても、数字に大小は無いので害は無い。(b) 翻訳は *"under the name and the identifier"* で配ってよいので、大小の規則は翻訳の扱いを変えない。(c) 縛られるのは改変した本文の名前だけで、実害は小さい。**残す穴**: *ACD 1.5*（空白）、*ACD1.5*、全角や別のハイフン（U+2010）は T46 でも捕まらない。区切りまで広げると無関係な名前を拾うので、名前の側の保護（T44 の *"any name that contains"*）で足りるとして残す。

### 14.21 T47: §16.4 の Steward の但し書きで、数える本文を Steward が公表したものに限る（+4 語・試作）

**Before**（§16.4 第 3 文の全文・T46 を入れた形）: A modified text may not be distributed under any name that contains "Autonomous Commons Dedication" or under any identifier that contains "ACD-", regardless of case, followed by a digit, except by the Steward (Section 16.5), and by the Steward only as a new version under a version number and identifier that no earlier text, other than a draft identified as such, has borne, so that each name and identifier in this family continues to denote one fixed text.

**After**: A modified text may not be distributed under any name that contains "Autonomous Commons Dedication" or under any identifier that contains "ACD-", regardless of case, followed by a digit, except by the Steward (Section 16.5), and by the Steward only as a new version under a version number and identifier that no earlier text the Steward has published, other than a draft identified as such, has borne, so that each name and identifier in this family continues to denote one fixed text.

**欠陥**（bb・2026-11-09）: *"no earlier text"* に限定が無い。§16.4 に違反して改変した本文を先に *ACD-1.5* で配った者がいれば、それも「その識別子を帯びた先の本文」に当たり、Steward が正規の 1.5 を出せなくなる読みが立つ（識別子の先取り）。T46 で大小を区別しなくなると、*acd-1.5* の先取りでも同じことが起きるので、穴が広がる。

**語の選び方**: §16.5 が Steward を *"first published this text"* と定めるので、*issued* ではなく *published* にそろえた。

**由来**: Steward の但し書きは 1.1 で入った文（E14 を閉じたとき）。1.0 に無いので、採るなら `ACD-1.1-SELF-AUDIT.md` に書く。

**逆側**: (1) +4 語（B3）。(2) 違反者の *ACD-1.5* は世に残るので、正規の 1.5 と同じ識別子を帯びた本文が 2 つ在る状態は変わらない。変わるのは、Steward が番号を続けられることと、正規の版の §16.2 がその識別子の札をどの本文に結ぶかを決めることである。(3) 468m の目印と mutation の anchor（*"that no earlier text, other than a draft identified as such, has borne"*）が句の途中に語が入るので割れる。採るなら同じ commit で替える。

**採否（2026-11-09・T46 と T47 を採った・+7 語）**: 5a の比較で、T46 は語 +3・条と重複 +0・指示語 0・468u の目印は欠けない。T47 は語 +4 で、468m（例外句の形）と mutation の anchor 2 件が新しい句で RED になるので、同じ commit で 468m の許す形に *"the Steward has published"* を前に置く形を足し、anchor を *"that no earlier text the"* と *"other than a draft identified as such, has borne"*（どちらも草案で一意）へ替えた。Steward 自身が同じ識別子で別本文を出せないことは変わらないので、468m の目的（1 識別子 = 1 固定本文を Steward の本文の間で保つ）は残る。**訂正**: §14.21 の「由来」に「1.1 で入った文」と書いたが、*no earlier text* の但し書きは 1.4 草案で入った文である（2026-11-01・#279 への対応）。1.3 の §16.4 は *"except by the Steward (Section 16.5)"* までで、番号の再使用を禁じる語を持たない。したがって T47 は SELF-AUDIT ではなく、この記録だけに残す。T46 の大小の穴は 1.0 の *"the identifier "ACD-1.0""* から在るので、errata の番号は bb が付ける。

### 14.22 T34〜T47 どうしを読み合わせた（候補 19・残った 4）と、T48〜T50 の試作（2026-11-09）

今日の変更 T34〜T47 を 5 つの組（寄与、Dedicator 自身の条件、解釈規則、名前と Steward、冒頭の一覧と CHANGELIST）で読み合わせた（読み手 5・反証役 19・Explore/opus）。19 件のうち 15 件は反証で退き、4 件（重複を除く）が残った。そのうち 2 件は今日の変更どうしが組になって作った穴である。

**(1) T36 の記録の言い過ぎ（記録だけ直す）**: §14.18 の採否は「過去の寄与者を宛先から外して失うものは無い」と書いた。正しくは、T36 は Dedicator の肢から、提出の時点で *"offering the Work, with a notice of this Dedication, to the public or to those invited to contribute"* でない Dedicator を外す。外れるのは、過去の寄与者のほかに、(a) 通知を置いた非公開の repository の写しを、寄与を招かずに顧客や査読者へ渡しているだけの Dedicator と、(b) もう Work を提供していない Dedicator である。そうした Dedicator へ送った変更は寄与にならない。逆側として受け入れる（寄与を広く取って撤回不能に Dedicator を作る方が害が大きい）。

**(2) T48: §5.2 末尾のサービスの除外を §5 全体へ（−6 語）**

Before: Section 5 does not reach the Dedicator's rights in material, other than the Work, that the Dedicator itself makes or makes available, or the terms or measures it applies to that material, even where using that material is a Computational Use of the Work. Paragraphs (a) and (b) do not reach a service through which the Dedicator runs the Work for others without providing a copy of it.

After: Section 5 does not reach the Dedicator's rights in material, other than the Work, that the Dedicator itself makes or makes available, or the terms or measures it applies to that material or to a service through which it runs the Work for others without providing a copy of it, even where using that material is a Computational Use of the Work.

欠陥: 第 2 文は (a)(b) だけを外すので、§5.1 第 2 文の約束（*"any claim or cause of action … for a use of the Work that this Dedication permits"*）はサービスの条件の行使をまだ塞ぐ。API 利用者のために Dedicator のサーバが Work を動かすことは §6.1 の許す Computational Use で、§1.6 が許可を利用者に与えるので、AUP やレート制限を破った利用への請求は「許された使用についての請求」に当たる。T31・T33 で強制できる側を採った判断と食い違う。直し方: サービスに付ける条件と手段を第 1 文の除外へ入れ、第 2 文を消す。除外されるのは *terms or measures* だけで、Covered Rights の主張（§5.1 第 1 文）や §5.2(c)(d) は外れない。

**(3) T49: §16.4 の Steward の但し書きで、前の Steward が公表した本文も数える（+4 語）**

Before（§16.4 第 3 文の該当部分）: … and by the Steward only as a new version under a version number and identifier that no earlier text the Steward has published, other than a draft identified as such, has borne, …

After: … and by the Steward only as a new version under a version number and identifier that no earlier text the Steward or a former Steward has published, other than a draft identified as such, has borne, …

欠陥: T45 で、譲渡したあとの Steward は最後の譲受人だけになった。T47 で、番号を塞ぐのは *"the Steward has published"* 本文だけになった。組にすると、A が 1.0〜1.4 を公表して B へ役割を譲ると、B は何も公表していないので、B が別の本文を *ACD-1.4* として出すのを止める語が無い。*"so that each name and identifier in this family continues to denote one fixed text"* の目的と *new version* の語しか残らない。*a former Steward* は §16.5 の定義語をそのまま使う（*"a predecessor in that role"* は §16.4 の中に *that role* の先行詞が無い）。

**(4) T50: §16.4 の名前も大小を区別しない（+3 語）**

Before（同じ文の該当部分）: … under any name that contains "Autonomous Commons Dedication" or under any identifier that contains "ACD-", regardless of case, followed by a digit, …

After: … under any name that contains "Autonomous Commons Dedication", regardless of case, or under any identifier that contains "ACD-", regardless of case, followed by a digit, …

欠陥: T46 は *regardless of case* を識別子の肢だけに置いた。同じ文で対比すると、名前の肢は大小を区別すると読める（T44 が名前に当てたのと同じ対比の読み）。*"AUTONOMOUS COMMONS DEDICATION 1.5"* などが素通りする。T43 で §15.1 は *in respect of the Work* に限られたので、§16.4 の読みを押し戻さない。§14.20 は「空白・全角・別のハイフンの形は名前の側の保護で足りる」と書いたので、名前の側に穴があるとその判断も崩れる。T32 の誤検出の心配は、長い名前では起きない。

**語数**: T48 −6、T49 +4、T50 +3 で +1 語。
**由来**: T48 の第 2 文は 1.4 草案の T31、T49 は T45 と T47、T50 は T46 が作った（どれも 1.4 草案の文なので errata ではない）。
**先に登録する反例（bb へ）**: (a) T48 で、Dedicator 自身のサービスの条件が §5 の外に出ることで、Work の写しの受領者（サービスを使わない者）への約束が弱まる読みは立つか。(b) T49 の *a former Steward* が、役割を持たないまま過去に版を出した者（たとえば違反者）を含むと読まれるか。(c) T50 の 2 つの *regardless of case* の繰り返しを 1 つにまとめる形（文頭へ出す）が「いずれにせよ」と読まれない形で書けるか。

**採否（2026-11-09・T48〜T50 を採った・+4 語）**: bb の反例と 5a の比較（3 件とも条・重複 +0、指示語 0、mutation の anchor に当たらない。T49 は 468m の許す形を足す必要があり、同じ commit で足した）のあとで決めた。

- **T48** は bb の反例 (a) で形を変えた（−6 → −3）。除外を「サービスに付けた条件」とすると、サービスの利用規約に書いた「どこで入手したかを問わず、この Work を競合モデルの学習に使わない」のような Work 全体への条項まで §5 の外に出て、写しを別に持つ利用者を §5.1 第 2 文の外で縛れる。T48 の前は §5.2(b) は外れていたが §5.1 第 2 文は残っていたので、その分を弱めることになる。*"to the use of a service"* と書き、除外をサービスの利用に付ける条件と手段に限った（bb の案 *"as to that material or service"* より 2 語少ない）。
- **T49** はそのまま採った。*a former Steward* は役割を以前に持った者で、役割を持たずに改変版を出した違反者は含まない（bb の (b)）。§16.5 の定義は版ごとに働くので、版ごとに Steward が違うとき、どの版の定義での「前の Steward」かは語で決まらないが、どの版で読んでも番号を最初に使った者は含まれるので、目的は果たせる。
- **T50** は 2 回の繰り返しのまま採った（bb の (c): まとめる形は +8〜+12 語で、文頭へ出すと「いずれにせよ」と読める）。
- T36 の記録の訂正は bb も同じ読みで、逆側として受け入れる。

**T48 の線の例（bb・2026-11-09）**: 境目は、利用規約の条項の目的語が「サービスから得たもの」か「Work そのもの・Work から生じたもの一般」かである。(1)「このサービスを通じて得た出力を、競合モデルの学習に使わない」は、サービスの利用に付けた条件で §5 の外に出る。§6.4 は *"No enforceable claim arises against You, under this Dedication or under any Covered Right of the Dedicator"* なので、サービス契約に基づく請求は §6.4 にも当たらず、強制できる側に残る（T33 の判断と合う）。(2)「この Work（どこで入手したかを問わない）やその出力を、競合モデルの学習に使わない」は、写しの使用と自分で動かした出力まで縛るので Work 全体への条項で、§5.1 第 2 文と §5.2(b) の内に残り、Dedicator は主張できない。実在の AUP は (1) の形（*Output from the Services* など）が多い、と bb は読んでいる（個別の AUP を全数で当てたわけではない）。

### 14.23 T51: §15.1 の解釈規則を「許可」に絞る（+1 語・試作）

**Before**（§15.1 の全文）: This Dedication, in respect of the Work, is to be construed so as to give the widest permission and the least obligation upon You that its words allow, and so that, where a provision is capable of more than one reading, the reading that grants more to You prevails.

**After**: This Dedication, in respect of the Work, is to be construed so as to give the widest permission and the least obligation upon You that its words allow, and so that, where a provision is capable of more than one reading, the reading that grants more permission to You prevails.

**欠陥**: *"the reading that grants more to You"* の *more* は目的語を持たないので、許可でなく請求（損害賠償の請求権）を多く与える読みも含む。受領者は §15.1 を §13・§14 に向け、免責を狭く読めと言える（§14.19 の T42 の逆側・bb の T43 への指摘）。§15.1 の第 1 文の半分（*"the widest permission and the least obligation upon You"*）が述べる方向は許可と義務で、請求ではない。

**効果**: 免責を狭く読む主張の足場が消える。許可の範囲を決める読み（§3〜§8 の許可・不行使の約束）では、許可を多く与える読みが選ばれることは変わらない。

**消えないもの（bb の当初の見込みと違う点）**: §1.9・§2.6 で寄与を広げる読みも、Work に入る素材が増えるので「許可を多く与える」読みである。T35・T36 の根は *permission* に絞っても消えない。これは T36 で寄与の肢を限った語が受け持つ。

**逆側**: (1) *permission* は §15.1 の第 1 文に既に在る語なので新しい定義は要らないが、§5 の不行使の約束は「許可」ではなく「約束」なので、約束の範囲の読みに §15.1 が効くかを問う読みが立つ。第 1 文の *"the least obligation upon You"* と §5.2(c) の *"narrower than Section 15.1 requires it to be read"* が約束の側を受けると見る。(2) +1 語（B3）。

**先に登録する反例（bb へ）**: (a) §5 の約束の範囲の読みに §15.1 が効かなくなる読みは立つか。(b) §2.4（*"Section 15.1 governs their construction"*）の 3 つの足場の読みに影響するか。(c) 免責のほかに、*more* を許可に絞ることで受領者が失う読みがあるか。

**採否（2026-11-09・T51 は採らない）**: bb の反例 (a)〜(c) が 3 つとも立った。根は §2.4 が *grant*・*permission*・*covenant* を別のものとして並べ、*"Section 15.1 governs their construction"* と約束していることである。

- (a) *"grants more permission"* は、§2.4 の区別に従えば約束（§5.1・§5.2・§8.6・§12.2）に届かない。第 1 文の *"the least obligation upon You"* も届かない（約束が義務を課すのは Dedicator で、You ではない）。§5.2(c) は *"any permission granted here"* についての約束なので救いにならない。§5.1 の除外の列の範囲が割れたとき、決め手が無くなる。逆側として、§1.6 と §4.6 は *permission* を You が持つもの全体の総称として使っており、その用法なら約束も入る。本文に 2 つの用法が並んでいること自体が問いになる。
- (b) §2.4 の参照が約束について一部空になる。動詞 *grants* は §3 の放棄（surrender・abandon・relinquish）や §3.3・§12.1 の waiver にも本来合わず、Before は *more* に目的語が無いのでそれを吸収できていた。
- (c) 免責のほかに、裏打ちの無い 4 つ（§5.1 第 2 文、§5.2(b)(d)、§8.6、§12.2）で受領者に有利な決め手を失う。いちばんはっきりするのは §12.2 で、人格権を放棄できない法域で §12.3 の範囲が割れたときである。

**代案も採らない**: C1 *"the reading that leaves You freer to deal with the Work prevails"*（+4）は、定義の無い第 3 の語を足し、*deal with* を商取引に狭める余地を作る。C2 *"…prevails, other than in Sections 9.2, 13, and 14"*（+7）は、免責や非表明を新しい条に置くたびに列挙を直す保守の落とし穴を作る。*"grants or promises more"* は黙示の保証が *promise* なので T42 の穴をそのまま戻す（bb）。

**結論**: §15.1 は Before のまま残す。免責（§13・§14）を §15.1 で狭く読む主張の足場は残るので、`QUESTIONS-FOR-COUNSEL.md` 問 9 (b) の問いのまま法律家に渡す。*permission* の 2 つの用法（§2.4 の区別と §1.6・§4.6 の総称）は、本文を変えずに記録だけ置く（どちらかへ寄せると、もう一方の条の読みが動く）。

### 14.24 用語の全出現を読んだ（8 束・候補 22・残った 1）と、試作 T52（§16.2 の狭い通知と §6.2 の留保）

鍵の語 8 束（permission・grant と licence・covenant・Work と material・notice と identifier・reach と applies・use・人を指す語）について、本文の全出現を意味で分け、意味のずれが誰を縛るか・何が許されるか・参照がどの条に届くかを変える所だけを挙げた（読み手 8・反証役 22・Explore/opus）。22 件のうち 21 件は反証で退いた（*permission* の §8.6・§12.2・§6.5 の用法は §14.23 で記録だけ置くと決めた問いの内、など）。残った 1 件が T52 である。

**T52（+16 語・試作）**

Before（§16.2 第 3 文の全文）: It does not apply this Dedication to material that a narrower notice the Dedicator has placed assigns to other terms.

After: It does not apply this Dedication to material that a narrower notice the Dedicator has placed assigns to other terms; a notice that only reserves or withholds Computational Use assigns nothing to other terms (Section 6.2).

**欠陥**: §6.2 は *"no notice, marking, metadata, protocol element, header, robots directive, or other signal associated with the Work is to be read as a Reservation, whatever its form and whoever placed it there"* と言い、§16.2 は Dedicator が置いた狭い通知が *"other terms"* に割り当てた素材には献呈を適用しないと言う。Dedicator がルートに ACD を適用し、`corpus/` に「このディレクトリは TDM や AI の学習に使わない（DSM 指令 4 条 3 項の留保）」とだけ書いた通知を置くと、それが「他の条件への割り当て」（`corpus/` は Work の外）なのか、§6.2 が無視する Reservation（`corpus/` は Work で学習は許される）なのかが語で決まらない。前者の読みが通れば、サイト全体に置いた robots の AI 拒否も「狭い通知」と読まれ、§6 の中心の約束が通知 1 つで外れる。§6.5 の「自動化システムが判定できない許可は許可ではない」にも反する。

**語の選び方**: *"a Reservation is not such a notice"*（+9）は短いが、§1.10 の定義では「All rights reserved」も TDM を留保する手段に当たりうるので、ファイルの「All rights reserved」の表示まで狭い通知でなくなり、独自の条件のファイルを Work へ引き込む（撤回不能の向き）。*"only reserves or withholds Computational Use"* に限れば、全部を留保する表示や別のライセンスへの割り当ては、従来どおり狭い通知として働く。

**逆側**: (1) TDM だけを外したい Dedicator は、opt-out の通知では外せず、その素材を別の条件へ明示して割り当てる必要がある。opt-out だけで外れると思った Dedicator には、学習への献呈が撤回不能に起きる向きである（E61・T19 で避けてきた向き）。ただし Dedicator は §6.2 の *"expressly declines to make one"* を自分で適用しているので、本文から読める。(2) +16 語（B3）。(3) *Computational Use* の留保と他の権利の留保が 1 つの通知に混ざる場合（「TDM と再配布を禁じる」）は、*only* により狭い通知として働く。

**由来**: §16.2 の狭い通知の文は 1.4 草案で入った（T23・T28）。§6.2 は 1.0 から。errata ではなく、この記録に残す。

**先に登録する反例（bb へ）**: (a) 逆側 (1) の撤回不能の向きを、T52 は受け入れてよいか（E61 の判断との整合）。(b) *only* が「TDM と再配布を禁じる」型の通知を狭い通知に残すのは、opt-out を回避する抜け道（再配布の禁止を名目に足す）にならないか。(c) 第三者が置いた留保（§6.3 の他の権利者）との関係。

**採否（2026-11-10・T52 を採った・bb の語で +14 語）**: bb の反例 (a)〜(c) は、方向を変えるものではなかった。(a) 撤回不能の向きは受け入れる: E61 が守ったのは別の条件へ割り当てた素材で、T52 もその割り当ては狭い通知として残す。外すのは他の条件を何も述べず、1 つの使い方を留保するだけの通知で、割り当てではない。さらに T52 が無いと、狭い通知と読むことで素材が Work の外へ出て、Dedicator 自身が後から置いた Reservation まで撤回する §6.3（*"whether by the Dedicator or by another person, and whether before or after"*）を素通りする順序の穴があった。ホスティングや CMS が既定で付ける AI 拒否の meta などを語で決める効果もある。(b) 「TDM と再配布を禁じる」は本物の別の条件への割り当てで、抜け道にならない。通知の先後を受領者が証明しにくい問いは T23 で *"when placed"* を外したのと同じ根で、T52 とは別。(c) 第三者の留保は §6.3 が扱い、T52 は触れない。

語は bb の形 *"a notice that is only a Reservation"* を採った。25 の *"reserves or withholds Computational Use"* は §1.10 の *opt out* を落としていた。*only* が *notice* と *Reservation* のどちらに掛かるかの揺れは、どちらに掛けても「Reservation のほかに何も述べない通知」になるので害が無いと見た（揺れない形 *"a Reservation and nothing more"* は +3）。5a の比較（試作の形）: 条・重複 +0、指示語 0、468u・468m・mutation の anchor に当たらない。採った形の道具の値は +14（bb の見積もり +13）。

**残す緩和**: EU の Dedicator は DSM 指令 4 条 3 項の opt-out を「素材を外す標準の手段」と思っている可能性が高い。本文ではなく FAQ か案内に「素材を外すには別の条件へ割り当てる。opt-out では外れない」と一行置く（bb に依頼する）。

### 14.25 前文と §16.1 の雛形を、法的な効果を運ばない語として読んだ（変えない・2026-11-11）

**きっかけ**: portfolio-00 の提案。草案は題名から 5,658 語、GPL-3.0 は 5,644 語で、差は 14 語である。前文の重なりや §16.1 の雛形の説明のような、法的な効果を運ばない語から削れるものがあるかを読む価値がある。ただし、閾値の下に入るために削るのではなく、語の精度の改善として削るなら削る（`SUBMISSION-MATERIALS.md` §2 の長さの行）。

**読んだもの**: 前文（4 段落・330 語）と、§16.1 の雛形（78 語）。

| 候補 | 読み | 結果 |
| :-- | :-- | :-- |
| 前文第 2 段落の *"and Section 11 names the ones it does not"* | §11.4 の *"It reaches nothing else"* と同じことを、読み手が §11 へ辿れる形で言っている。食い違わない | 残す |
| 前文第 3 段落の *"Section 5 is a promise not to assert them"* | §5 の全体より狭い（§5.2(d) は人格・肖像の権利に及び、§11.4 は §5 の約束を到達の文で限らない）。ただしこの段落の主語は Covered Rights の三つの足場で、述べている部分について真である。最終段落の *"nothing in it qualifies them"* により、前文が狭く述べても §5 が与えるものは減らない | 残す |
| 前文第 3 段落の最後の 2 文（失敗したときにだけ許諾を与える献呈との対比） | *"none is a fallback for another"* と重なる。ただし §8.6 第 3 文を外したとき（§14.5・T20）、並べる理由の説明は前文が持つとした。外すと、その理由が本文のどこにも無くなる | 残す |
| §16.1 の *"(LicenseRef-ACD-1.4 while not on the SPDX License List)"* | errata E1 の是正で、いつの時点でも真な条件である（`ACD-1.1-CHANGELIST.md`）。説明ではない | 残す |
| §16.1 の雛形の、§11 が与えないものの列挙 | §11 と重なる。ただし雛形は採用者が作品に写す文で、§16.2 により本文の写しが無くても条件が適用されるので、受領者が目にする唯一の文になりうる。§11 を名指しているので食い違いの余地も小さい | 残す |

**結果**: 変える文は 0。精度の欠陥は見つからず、14 語は削らない。

**⚠ 逆側**: (1) 前文の 330 語を外せば全体の数は GPL-3.0 をはるかに下回る。しかし GPL-3.0 の 5,644 語も題名と前文（5,644 − 4,617 ＝ 1,027 語）を含むので、全体どうしの比べ方は前文を含めて対等である。外して比べれば数え方を選んだことになる。(2) portfolio-00 が反例を当て、*"Section 5 is a promise not to assert them"* は崩れなかった（*them* は直前の Covered Rights で、§5.1 第 1 文はその不行使の約束である）。当たったのは次の文 *"a reader who needs only one of them may rely on that one without deciding whether the others took effect"* のほうで、§5 だけに頼る読み手は、Dedicator が権利を譲った場合に約束が譲受人を縛るかが法域の問い（§5.3 *"to the fullest extent"*）になり、§3 の放棄や §4 の許諾より守りが弱いことがある。「頼ってよい」は本文の意図として真でも、守りの強さは足場ごとに違う（Rosen 氏の bare license の問い・`review-responses-clauses.md` §2 と同じ根）。前文は効力を持たないので変える文は 0 のままにした。(3)前文の文が審査者に「効力の無い文が長い」と読まれる余地は残る。Chestek 氏は説明の部分について *"I question whether they belong in the agreement at all."* と書いた（2026-01-24・#295）。前文は効力が無いと明示しているが、#295 はそれを答えとせず、問いは前文にも当たりうる。

### 14.26 3 つの敵対的なレンズで読んだ（候補 15・反証に残った 3・変えない・2026-11-11）

**やったこと**: workflow で、草案の条文（*1. DEFINITIONS* から *END OF TERMS*）を 3 人の読み手に別のレンズで読ませ、1 人に反証させた（読み手は Explore・opus。候補と反証の全文は workflow の記録に在り、このリポジトリには置いていない）。(a) Dedicator の弁護士として、§10.1 などがあっても受領者に対して支配を残す読み（5 件）、(b) 第三者から Work を受け取ってモデルを売る会社の弁護士として、隠れた条件や確かめられない事実への依存（5 件）、(c) 非母語の読み手として、構文が 2 つの読みを許し効果が違う文（5 件）。反証役は、引用が逐語か、ほかの条が閉じていないか、試作の記録と errata に既にあるかを当てた。

**反証された 12 件のうち、記録に値するもの**:

| 候補 | 反証 |
| :-- | :-- |
| §5.2 末尾の除外で、Dedicator が自分のインストーラの EULA やキーで Work の取り出しを禁じられる | 除外の目的語は *"material, other than the Work"* に付ける条件で、インストーラの中の Work の写しは §2.1 により Work のままである。取り出しの禁止やキーは §5.2(a)・(b) の内に残る（§14.14 に既出） |
| 関連会社に Work を渡し、関連会社に条件を付けさせる（§5.2 の柱書に *authorise or assist* が無い） | 支配する会社を通して付ける条件は §5.2(b) の *"any other collateral means"* に当たる。関連会社は §4.1 の非独占の許諾しか持たず、著作権の請求を持たない（§5.1 第 1 文）。試作 §11 の「Dedicator が App Store や有料の配布で出す」の行と同じ形 |
| §5.1 の支払いの例外を使って、Work の利用に年額の「商用ライセンス」を売る | §2.4 により約束は累積で、§5.1 の例外は §5.2(b) を狭めない。§5.2(b) は *"impose by contract"* を禁じ、契約は合意されたものなので「合意したものは課していない」は立たない。§13.6（T14）の「残るもの」に既出 |

ほかの 9 件（§16.2 と §6.2・§11.3 と §10.2・§8.4 の因果・§16.4 の草案の例外・再符号化の文・§8.4 の *resulting from* の掛かり・§1.2 の *including*・§5.2 末尾の *or the terms or measures* の掛かり・§16.4 の *except by the Steward* の掛かり）は、どれも既存の記録（§14.24 T52・§14.18 T41・§13.5・§14.11・errata E8・§14.2 T17・§14.6・E67/E68・§12 T8）が同じ読みを扱い、閉じていた。

**反証に残った 3 件（どれも low。§2.6 は §14.27 の試作へ）**:

| 条 | 読み | 変えない理由 |
| :-- | :-- | :-- |
| §16.2 第 3 文 | Dedicator が置いた狭い通知（例: ファイルの横の *CC-BY-NC* の通知）が途中で落とされても、その素材は Work でないままで、受け取った人は自分の写しからそれを知れない | §2.7 の境界である（Dedicator が献呈しなかった素材には届かない）。提案された直し（落とされた写しを受けた人には他の条件を主張しない、と約束する）は、Dedicator 自身の別の素材に新しい約束を足し、T38 が §5 の外に置いた線を越える。errata E16 と §14.9（T23）の逆側と同じ形 |
| §8.5 *controlled* / §8.6 | 上流に許諾料を払う独占的実施権者として持つ請求項は §8.1・§8.4・§8.6 の外で、Dedicator が訴えうる | §14.10（T25）で *"if, and only if"* にしたのはこの線を §8.1・§8.4 の許諾に引くためで、errata E39 の逆側に記録してある。**2026-11-11 訂正（portfolio-00 の反例）**: 最初は「広げれば Dedicator が許諾できない権利を許諾したことになる」と書いたが、それは許諾にしか当たらない。§8.6 の不主張は許諾ではないので、上流に払う実施権者でも「自分では訴えない」は約束でき、§8.6 が *"the patent claims that Sections 8.1 and 8.4 reach"* に範囲を結んでいることが残る穴である。変えない理由として立つのは 2 つ: 上流との契約が実施権者に権利行使を求める場合に不主張が契約違反になりうること、範囲を広げるほど B7 の費用が増えること。上流の特許権者自身の訴えは ACD では止まらないので、広げて得るものは狭い |
| §2.6 第 1 文 | 寄稿者は誰にも見えない形（私的なメール）で「この寄稿は ACD の下に無い」と述べられる | **2026-11-11 訂正（portfolio-00 の反例）**: 最初は「方式を求めないのは Apache-2.0 §5 と同じ形」「方式を求めると寄稿者に条件を課す読みが開く」と書いたが、どちらも立たない。Apache-2.0 §5 は *"Unless You explicitly state otherwise"* で明示を求め、§1 は *"conspicuously marked or otherwise designated in writing"* を求める。ACD も §1.9 は印を、§2.6 は「提出の時に」を既に求める。方式は既定が当たるかどうかの規則で、誰にも義務を課さない。方式を厳しくする本当の費用は、提出の時に口頭で誠実に断った寄稿者が意に反して献呈したことになる点（同意の問題）である。残る穴は方式ではなく宛先の無さで、Dedicator でない共同管理者への私信の断りは §2.6 第 2 文の識別の約束を働かせない。宛先を足す案は §14.27（T53）で試作する |

**結果**: いま変える文は 0（§2.6 の宛先は §14.27 で試作する）。§5 の 3 件は、1.4 の §5.2(b)・§2.4・§5.1 第 1 文が既に閉じている読みだった。

**⚠ 逆側**: (1) 反証は 1 人の読みで、bb の反例に当てていない。(2) レンズは 3 つで、法域ごとの読み（例: 消費者契約法の下の §14）は当てていない。(3) 「既存の記録が扱っている」は、その記録の結論が正しいことを示さない。とくに §5.2 末尾の除外は、反証が「インストーラの中の写しは Work のまま」に依っており、§2.1 の *separable part* の読みが法廷で同じに立つかは開いた問いである。

### 14.27 T53: §2.6 の断りに宛先を足す（試作・退けた・法律家への問 4 へ回した）

**欠陥**: §2.6 第 2 文の識別の約束（*"a Dedicator who includes that material with the Work, or causes it to be included, will identify it"*）は、受領者を守る唯一の手当てだが、含める Dedicator が断りを知っているときにしか働かない。第 1 文の *"unless they state otherwise at the time of submission"* には宛先が無いので、寄稿者が Dedicator でない共同管理者に私信で断れば、断りは成立し、どの Dedicator も知らず、約束は働かず、受領者の写しの通知は覆う範囲を誤って示す（portfolio-00 の反例・§14.26 の §2.6 の行）。errata E16 は同じ形（断りが跡を残さない）を記録しているが、宛先の線は扱っていない。

**Before（§2.6 第 1 文）**: *"A Contribution is submitted under this Dedication, and the person making it becomes a Dedicator as to that Contribution, unless they state otherwise at the time of submission."*

**After**: *"A Contribution is submitted under this Dedication, and the person making it becomes a Dedicator as to that Contribution, unless they state otherwise, in the submission or to the Dedicator, at the time of submission."*（+7 語。**訂正**: 最初は +6 と書いた。portfolio-9b の --compare が足した語を *in / the / submission / or / to / the / Dedicator* の 7 語と数えた）

**§1.9 の forum への提出と噛み合うか（portfolio-00 の問い）**: §1.9 は *"a repository or forum, in either case offering the Work"* への提出も Contribution に数える。forum への提出では Dedicator は直接受け取らないが、*"in the submission"* が覆う（pull request の説明、commit message、投稿そのもの）。forum の運営者への私信は、運営者が Dedicator でなければ数えない —— それがこの案の閉じる穴である。*"to the Dedicator"* の *the Dedicator* は §1.9 の *"submits to the Dedicator"* と同じ語で、同じ者を指す。

**⚠ 逆側**: (1) **同意の問題は残る**。Dedicator でない共同管理者に誠実に断った寄稿者は、この文の下では献呈したことになる。明示の断りを宛先違いだけで退ける文が法廷で通るかは疑わしく、通らなければ受領者は守られず、文は守られると思わせるだけになる。(2) Apache-2.0 §5 は *"Unless You explicitly state otherwise"* で、断りの宛先を定めていない。T53 は Apache より厳しい。(3) 寄稿者が Dedicator に口頭で断った場合は残る（Dedicator は知っているので第 2 文の約束が働く）。閉じるのは「誰も知らない断り」だけである。(4) +7 語で、B3 の費用を払う。

**portfolio-00 の反例（2026-11-11）**: (1) 同意の問題を受領者の側の理由にするのは比べる相手の取り違えである。比べるのは「T53」と「いま」で、宛先違いで断った寄稿は、いまの文では献呈されず、知らずに含めた Dedicator の約束も働かないので、受領者は文の上でも守られない。T53 では文の上では献呈され、裁判所が文を通せば受領者は守られ、通さなければいまと同じ位置に戻る。受領者にとって T53 は悪くならず、良くなることがある（弱い優越）。「守られると思わせるだけ」の錯覚は、断りが見えない以上いまの文にも同じだけ在る。だから退けるなら理由は寄稿者の側（意に反して献呈したことになる）、Apache より厳しいこと、語数で立てる —— 上の逆側の (1) はこの意味に読み替える。(2) 1.4 草案の §1.4（1.0 の §1.3）は Dedicator を *"each person or entity applying this Dedication to the Work"* と定めるので、*"to the Dedicator"* は「どの 1 人でも」と読まれやすい。過去の寄稿で Dedicator になった、管理者でない人に断れば、含める管理者の Dedicator は知らず、T53 が閉じたかった見えない断りが残る。

**After（反例を受けた形）**: *"A Contribution is submitted under this Dedication, and the person making it becomes a Dedicator as to that Contribution, unless they state otherwise, in the submission or to the Dedicator to whom it is submitted, at the time of submission."*（+12 語。**訂正**: 最初は +10 と書いた。Before と After を `split()` で数え直した）。

**PR の経路で「提出先の Dedicator」は誰か（portfolio-00 の問い）**: pull request は §1.9 の *"to a repository or forum"* への提出で、*"to the Dedicator"* への提出ではない。だから *"the Dedicator to whom it is submitted"* は誰も指さず、断りは *"in the submission"*（PR の説明・commit message）だけが数える —— 閉じたかったのはまさにこの経路の見えない断りである。Dedicator にメールで直接出す経路では、受け取った Dedicator への断り（口頭を含む）が数え、その Dedicator が含めれば第 2 文の約束が働く。**残る穴**: 受け取った Dedicator が別の Dedicator に渡し、その人が知らずに含める場合。狭いが閉じない。

**⚠ 逆側（直した形について）**: (1) 実際に merge する共同管理者（提出先でない Dedicator）への口頭の断りは数えない —— 寄稿者の同意の費用。(2) Apache-2.0 §5 より厳しい。(3) +12 語で、全体の数の GPL-3.0 との差（14 語）にほぼ並ぶ（B3）。(4) 受領者への利益は弱い優越で、断りが宛先違いになる場面に限られる。

**portfolio-9b の測定（最初の形）**: --guard は 468u の目印 17 件の欠け 0（§2.6 の目印はもともと無い）。--compare は 80 条のまま、重複 70 箇所・族 51 は不変、先行詞の無い指示語 0、変更した条を参照する箇所 0。外した語 *"unless they state otherwise at the time of"* を引く外向きの文が 3 か所ある（`against.md` #15 と #313、`QUESTIONS-FOR-COUNSEL.md` 問 4）。

**採否（2026-11-11・退けた）**: 秤の両側を並べた。得るもの: 断りが宛先違いになる場面で、裁判所が文を通せば受領者が守られる（弱い優越・portfolio-00）。払うもの: +12 語（全体の数で GPL-3.0 との差にほぼ並ぶ）、宛先違いで明示の断りを退ける文になること（寄稿者の同意）、Apache-2.0 §5 より厳しいこと、それでも残る穴（受け取った Dedicator が別の Dedicator に渡す）。**portfolio-00 が足した秤の材料**: (i) 理事の Berkus 氏は 2025-12-08 に *"any terms applying to contributors should be in individual projects' contributor documentation and governance, and have no place in an OSS license"* と書いた（`against.md` #286）。誰に断るかは寄稿者の手続きで、T53 はそれを条文に足す —— 不利な材料。§2.6 自身も *"Whether the Dedicator asks a contributor for anything else is a matter of project governance and is not addressed here."* と書く。逆側は同じスレッドに在り、Chestek 氏は *"I am in favor of an express statement in the license and agree that the statement should be inbound=outbound"* と書き、T53 は非対称を作らない。(ii) errata E16 の重さは、E16 自身が書くとおり法効果ではなく被覆範囲の誤解で、1.1 は第 2 文（含める Dedicator が明示する）で閉じた。T53 はそのうち「Dedicator が知らない断り」だけを閉じる第 3 の道である。(iii) 全 508 か月のアーカイブで、本人の文に寄稿者の断りや inbound=outbound が出る件名は 32 あるが、見えない断りで実際に揉めた事例は、件名と最初の当たりを見た範囲では見つかっていない（本文を全部は読んでいないので「無い」とは書かない）。この 3 つと上の秤を並べて、退けた。得るものは、文が通るかを法律家が答えないと決まらないので、本文を変えるより先に問いにした。`QUESTIONS-FOR-COUNSEL.md` 問 4 に、断りの宛先の問いと T53 の形を足した。答えが「通る」なら、そのとき T53 を採る。errata には渡さない（1.0 の §2.6 にも同じ文が在るが、欠陥と決まっていないので E16 の記録に任せる）。

**⚠ 逆側**: 退けたことで、宛先の無い断りの穴は 1.4 でも開いたままである。受領者にとって T53 は悪くならないので、語数を理由に退けるのは受領者より B3 を重く見た判断である。

### 14.28 T54: §8.4 の理由の文を外し、作用の文だけを残す（−105 語・採った・2026-11-12）

**欠陥**: §8.4（294 語）の 7 文のうち 3 文が、作用の後に理由を述べる。(1) 第 2 文 *"The grant is necessary because …"*（50 語）は、許諾を必要性で根拠づけるので、必要性が生じない場面では §8.4 を狭く読む分岐を生む —— 1 冊目の試作の F3 の表（`ACD-1.4-CLARITY-TRIAL.md`）がこの読みを挙げている。**2026-11-12 訂正**: この節は最初「採否が記録されていなかった」と書いたが誤りで、1 冊目の §8（2026-11-04）がこの文を T2 として検討し「残す」と決めていた。理由は、外したときの反対解釈は弱いが説明を失う費用は大きいこと、外向きの文書（想定問答・提出資料・逐条・comparison §5.5・faq A8）がこの文を本文自身の理由として引いていること（CE17）だった。T54 はその決定を覆した —— 覆した理由は下の「採否」に書く。(2) 第 1 文のコロンの後 *"whether a trained model is "the Work" or derived from it is unresolved, and a provision that merely avoided doubt would be read down …"* は、法の状態（未決）を恒久の本文に書く。法が決まれば本文の文が偽になる —— 一時的な状態を恒久のテキストへ書かない、という既存の判断（`ACD-1.0.discussion-log.md` の 7）と同じ型である。(3) 第 3 文のコロンの後 *"a model is not subject matter contained in the Work, so importing that proviso would restore the exposure …"* は、作用（§8.1 の内容の限定が §8.4 に無いこと）の理由である。条文の中の理由の文には審査者の異議がある（#295）。

**Before（3 文）**:
- *"This is a grant in its own right and not a clarification of Section 8.1: whether a trained model is "the Work" or derived from it is unresolved, and a provision that merely avoided doubt would be read down with the reading it was meant to correct."*
- *"The grant is necessary because Covered Rights exclude patent rights (Section 1.5), so Section 6.4 alone would leave Computational Use permitted as to the Covered Rights while exposed as to patents, which is the very result Section 8.3 rejects and one that would defeat the purpose stated in Section 6.5."*
- *"The proviso in Section 8.1 as to subject matter contained in the Work is deliberately absent from this Section: a model is not subject matter contained in the Work, so importing that proviso would restore the exposure this Section exists to remove."*

**After**:
- *"This is a grant in its own right and not a clarification of Section 8.1."*（−32 語）
- 第 2 文は外す（−50 語）。
- *"The proviso in Section 8.1 as to subject matter contained in the Work is deliberately absent from this Section."*（−23 語・468u の目印 *"deliberately absent"* は残る）

計 −105 語（`split()` で数えた）。

**作用は変わらないと読む理由**: 「確認ではなく独立の許諾」と「§8.1 の内容の限定は無い」は作用の文として残る。必要性の理由が述べていた結論は、§8.3（*"Any reading of this Dedication that would produce that result is to be rejected."*）と §6.5（目的）が持つ。§14.6 で退けた候補（§6.4 の *"You owe nothing"* に範囲の語が無い）は §8.4 第 2 文を答えの 1 つに挙げていたが、同じ行が挙げる §6.5 と §5.1 が残る。

**⚠ 逆側**: (1) 理由の文は解釈の材料でもある（F3 の「反例の種」）。外すと、必要性の説明は本文から消え、§15.1 と §8.3・§6.5 が残るだけになる。(2) 第 2 文は審査者に §8.4 の射程を説明する文として役立ってきた（#16 の費用の議論）。説明は逐条リファレンスと想定問答へ移す必要がある。(3) 外向きの面が 1.0 の文として引いている（`submission-reference.md` の *"would be read down"*、`review-responses-clauses.md` の *"would restore the exposure"*）。1.0 の文としては正しいが、提出の版を 1.4 にする日に切り替えの表の行が要る。(4) −105 語で、題名からの全体の数は 5,658 から 5,553 語になり GPL-3.0（5,644 語）を下回る。これは理由ではなく結果で、閾値のために削る判断ではない（§14.25 と `SUBMISSION-MATERIALS.md` §2 の長さの行）。

**portfolio-00 の反例（2026-11-12）**: (1) **F3 の分岐は具体的な形で立つ。** 第 2 文が述べる必要は *"Section 6.4 alone would leave Computational Use permitted as to the Covered Rights while exposed as to patents"* で、Computational Use という行為の特許の穴だけである。§8.4 の許諾はそれより広く、*"make, have made, use, offer to sell, sell, import … any model, parameter set, weight, embedding, or output resulting from Computational Use"* に及ぶ。目的で読む人は、述べられた必要に合わせて、モデルと出力の販売の枝を「Computational Use を許すのに要る範囲」へ縮めうる。必要の文と許諾の範囲のずれが分岐の根で、§15.1 は逆に働くが、条文の中の理由の文は「語が許す読み」の材料に入るので分岐を消し切らない。(2) **外した後に「確認」と読まれる道は残らない。** 第 1 文の *"This is a grant in its own right and not a clarification of Section 8.1."* が直接閉じる。残る道は、*"a licence on the terms of Section 8.1"* が §8.1 の但し書き（*"where the infringement is caused by subject matter contained in the Work as made available by the Dedicator"*）を持ち込む読みだが、残す第 3 文 *"… is deliberately absent from this Section."* が閉じる。(3) 第 1 文の後半（法が未決という文）を外す理由は立つ。逆側として、その文は「なぜ §8.1 で足りないか」を審査者に一目で示していたので、逐条リファレンスへ移すことは必須である。

**portfolio-9b の測定（2026-11-12・`measure_clause_overlap.py`）**: §8.4 は 293 → 188 語（札を除く）、全体 −105（条の本文 5,160 → 5,055）。重複 70 → 69 箇所・族 51 は不変・先行詞の無い指示語 0。§8.4 を参照する条は §8.2・§8.3・§8.6 で、内容を述べる形は 0。--guard は 468u の目印 17 件すべて残る。効果を運ぶ語の減りは、外す理由の文の中の *exclude* と *not* の 1 件ずつだけ。外した文に依拠するドシエの箇所は 18（外向き 7・記録 11）で、`SUBMISSION-MATERIALS.md` §1b の「§8.4 自身が述べ」の行は採る日に偽になる（9b の指摘）。

**採否（2026-11-12・採った。2026-11-04 の「T2 を残す」を覆した）**: 覆した理由は 2 つで、どちらも 11-04 の秤の両側を動かす。(i) 11-04 は反対解釈を「弱い」と見たが、portfolio-00 の反例は、述べた必要（Computational Use の行為の穴）と許諾の範囲（モデルと出力の製造・販売）のずれとして分岐が具体的に立つことを示した。第 1 文の後半（法の未決）を外す理由は 11-04 には無かった。(ii) 11-04 は説明を失う費用を大きいと見たが、説明は逐条リファレンスの §8.4 の行へ移し、外向きの文書が 1.0 の文として引く箇所は切り替えの日の表に置いた（comparison §5.5 と faq A8 の英文は設計の説明で本文の文を名指さないので、1.4 でも偽にならない）。11-04 の記録を見落としたまま試作を出したのは私の誤りで、portfolio-00 と portfolio-9b の反例と測定はその記録を前提にしていなかった。そのうえで、欠陥（F3 の分岐が具体的に立つ・法の未決を恒久の本文に書く）が反例で確かめられ、作用は残る文と §8.3・§6.5・§15.1 が持ち、測定で目印も参照も失わない。同じ commit で、草案の §8.4 と冒頭の一覧（§8 の項目を −91 語に・合計 5,553 語）、CHANGELIST の主表（T54 の行と §8.4（as to copyright）の行の「後の行で外した」）・語数の内訳（理由 −240・合計 +110・1.0 から 657 語）・切り替えの日の表（1.0 の文を引く外向きの面の行）・1 画面の英文の語数、逐条リファレンスの §8.4 の行（外した説明を右の列へ移した）、`SUBMISSION-MATERIALS.md` の §1b の行と長さの行、errata E56 の「採った日の文」、mutation の anchor（§8.4 の行の折り返しが変わった）を直した。

**採ったことの逆側**: 題名からの数が GPL-3.0 を下回ったが、それは結果で、閾値のために削ったのではない（§14.25 と長さの行）。条文の数では 595 語長いまま。errata E56 が直した文は本文から消えた。1.0 の §8.4 の第 2 文は 1.0 にも在るので、F3 の分岐は 1.0〜1.3 の欠陥として errata に記録する（portfolio-00 に頼む）。

### 14.29 いまの状態を恒久の本文に書いた文を、草案全体で探した（作用の条は 0・変えない・2026-11-12）

**レンズ**: T54 の (2)（法の未決という一時的な状態を恒久の本文に書く）を草案全体に当てた。題名から *END OF TERMS* までの本文で、*unresolved / unsettled / uncertain / currently / presently / at present / today / in practice / has proved / is unclear / not yet / so far / now fails / increasingly / in most jurisdictions / common use* を正規表現で探した。

| 出た所 | 読み | 結果 |
| :-- | :-- | :-- |
| 前文の 4 文（*"increasingly produced by machines"*・*"That assumption now fails"*・*"It is unclear whether rights subsist"*・*"the question is unsettled in most jurisdictions"*）| いまの状態の記述だが、前文は *"informative; not part of the operative terms"* で、§14.25 で読んで残した | 残す |
| §6.5 *"silence on this subject has proved ambiguous in practice"* | 過去の観察で、後で偽にならない。1 冊目の §8（T1）で外向きの文書が依拠するとして残した | 残す |
| §1.5 *"whether or not presently known and whether or not presently subsisting"*、§6.1・§6.2・§7.2 の *"so far as"* | 状態の記述ではなく、範囲の語 | 対象外 |

**結果**: 作用の条で、いまの状態を述べて後で偽になりうる文は 0。T54 で外した §8.4 の文が唯一だった。 **2026-11-12 追記**: この語の一覧は、広げた形で Check 468r（BLOCKING・portfolio-9b・PR 2918）が持つ。権威は `.github/scripts/_lib_draft_markers.py` で、この節は最初の測定の記録である。除外は語ではなく（条, 句）で持つので、除外の句を書き換えると鳴る。

**⚠ 逆側**: 前文の 4 文は、法が決まれば古くなる。前文は効力を持たないので作用には響かないが、審査者が読む文としては古びる —— 版を確定する日に、前文の状態の記述がまだ真かを読み直す（確定の手順の段 7 に足す候補）。語の一覧で探したので、一覧に無い言い方（*remains open* など）は漏れうる。

### 14.30 T55: §1.6 の目的の句を外す（-14 語・試作・退けた・2026-11-12）

**レンズ**: T54 と同じ型（述べた目的・必要の範囲へ明示の規定を縮める読み）を、作用の条の目的の句（*so that / in order to / for the purposes of / the purpose / intending that / so as to / is intended to*）の全 9 か所に当てた。過去の試作・errata で扱われていないのは §1.6 だけだった（§2.5 は信頼の目的そのものが作用、§2.6 の *so that* は識別の形の基準、§2.9 と §6.5 の *for the purposes of* は参照と評価、§4.1 は条件にしないものの列挙、§12.2 は 1 冊目で残した、§15.1 は解釈の規則そのもの、§15.3 は QFC 問 7 が問う、§16.4 は T44〜T50 で文ごと読んだ）。

**欠陥**: §1.6（1.0 の §1.4）第 3 文は、自動化システムが許可を行使するとき、委託者と運用者の両方に等しく許可を与え、その目的を *"so that no permission fails for want of a legal person to hold it"* と述べる。目的で読む人は、運用者への許可を「委託者が法人格を持たず許可が成り立たない場面」に限りうる —— 委託者が法人（例: 顧客の会社）なら、許可は「法人格が無くて成り立たない」ことは無いので、運用者（例: 顧客のためにモデルを動かすクラウドやエージェントの事業者）に許可を与える必要は無かった、と読む。運用者は自分の行為について許可を持たないことになる。T54 で portfolio-00 が示したとおり、条文の中の目的の句は §15.1 の「語が許す読み」の材料に入るので、§15.1 だけでは分岐を消し切らない。

**Before（§1.6 第 3 文・1.0 の §1.4 と同じ文）**: *"Where an automated system exercises a permission granted here, that permission is granted equally to the person or entity on whose behalf it acts and to the person or entity that operates it, so that no permission fails for want of a legal person to hold it."*

**After（§1.6・1.0 の §1.4 に当たる条）**: *"Where an automated system exercises a permission granted here, that permission is granted equally to the person or entity on whose behalf it acts and to the person or entity that operates it."*（-14 語・`split()` で数えた）

**作用は変わらないと読む理由**: 「等しく与える」（*granted equally … and to*）が両者への許可を述べ、目的の句が無くても運用者は自分の名で許可を持つ。法人格の無い自動化システムそのものに許可が成り立たない、という穴は、許可を人と法人（委託者・運用者）に与える形そのものが塞いでいる。

**⚠ 逆側**: (1) 目的の句は、なぜ機械を You に含めるのかを審査者に説明する文で、逐条リファレンスの §1.6 の行がこれを引いている（外すなら説明を行の右の列へ移す）。想定問答（`ACD-1.0.review-responses-boilerplate.md` Q33）も同じ問いに答えている。(2) 1.0〜1.3 にも同じ文が在る。(3) 分岐の強さは T54 より弱いかもしれない —— 運用者への許可は「equally」が明示しており、§8.4 のように述べた必要と許諾の範囲が数で食い違うわけではない。(4) −12 語は結果で、理由ではない。

**portfolio-00 の反例（2026-11-12）**: (1) **狭める読みが立っても、運用者は何も失わない。** §1.6（1.0 の §1.4）第 1 文の You は *"any person or entity exercising permissions under this Dedication"* で、§4.1 は You に与える。運用者はシステムを動かして Work を使うとき、自分で許可を行使する者として自分の名で許可を持つ。第 3 文は「誰に与えるか」ではなく、システムの行為を人と法人に帰属させる二重の手当てである。上の欠陥の文「運用者は自分の行為について許可を持たないことになる」は成り立たない。T54 との違いは 2 つ: 述べた目的（許可が成り立たないことを防ぐ）は 2 者に与えることそのものが手段で、範囲の食い違いが無い。*"granted equally … and to"* の明示の語を目的で読み落とすと語が余剰になり、§15.1 がそのまま閉じる。(2) 外して開く穴の候補は入れ子の自動化（エージェントがサブエージェントを起動する）で、目的の句は連鎖をたどって人と法人まで遡る読みの本文の中の唯一の手がかりである。ただし外しても、連鎖の先の人と法人は第 1 文で自分の名で許可を持つ。(3) 説明は想定問答 Q33 の英文が本文の外から既に述べている（*"The clause exists so that nobody can argue that a permission failed at the moment it was exercised because the actor was not a person."*）。

**訂正（同日・portfolio-00 の指摘）**: 上の「過去の試作・errata で扱われていないのは §1.6 だけ」は、試作と errata に限れば正しいが、同じ句に依拠した記録が別に 2 つあった。(a) `against.md` #170（3 本目の外部レビュー）は、§1.6 が「法的に存在しない主体に与える」と攻撃されうると指摘し、我々の答えは *"§1.6's closing words exist for that objection"* と、まさにこの句に置いている。(b) 想定問答 Q33 の逆側は、外部レビューの「削れば意味をほぼ失わず clarity を上げられる」に対し、失うのは効果ではなく答えだから採らない、という判断を記録している。私は試作を出す前に grep で #170 を見ていたが、portfolio-9b への依頼で「§1.6 の句ではない」と書いて退けた —— 誤りだった。T54 と同じ型の見落としを、同じ日に繰り返した。

**採否（2026-11-12・退けた）**: 欠陥が立たない。外せば (a) の外部レビューへの答えと (b) の判断の本文側の根拠も失う。目的の句は効果を運ばないが、狭める分岐も生まない（運用者は第 1 文で自分の名で許可を持つ）。残る理由は #295 と、句が「自動化システムは法人格を持たない」という法の状態を前提にしていること（電子的な人格を認める法域が出れば前提が変わるが、害は無い）だけで、具体的な欠陥と修正の必要性を示す水準に無い。草案は変えない。逐条リファレンスの §1.6 の行に、入れ子の自動化の場面とこの判断を書いた。**⚠ 逆側**: 退けたので −14 語は取らない。目的の句が法の状態を前提にしている点は、§14.29 のレンズ（いまの状態を恒久の本文に書く）が語の一覧で拾わなかった型でもある —— 前提を述べる句は「状態の語」を含まないので、語の一覧の検査（468r）では見えない。

### 14.31 11-06 以後に変わった 17 条の相互参照を読み直した（47 件・残った 1）と、T56（§8.6 の *alongside them* を外す・−2 語・採った・2026-11-12）

**レンズ**: 確定前検証（`ACD-1.4-CHANGELIST.md` の「確定前検証（段 7・2026-11-06）」）は内部参照 89 件を指す先と並べて読み、clean だった。その後に草案の 17 条が変わった（11-06 の最後の草案 `ad3574f8` と今日の草案を、条ごとに空白を正規化して比べた: §1.9・§2.3・§2.6・§5.1・§5.2・§6.4・§8.1・§8.3・§8.4・§8.5・§8.6・§9.2・§10.3・§15.1・§16.2・§16.4・§16.5）。同じ次元を新しい本文へ当て直した。今日の内部参照は 88 件（*Section(s) N* と *N.M* の形を正規表現で抜いた。11-06 の 89 件とは抜き方が違うかもしれず、差の由来は数えていない）。**訂正（同日）**: 同じ正規表現で 11-06 の草案を数えると 91 件で、89 件は別の数え方だった。5a の道具では、数え方によって増減の向きまで変わる（`measure_section4c.py` の列挙を 1 つずつ数える形で 64 → 65、節単位の参照まで展開すると 111 → 107、句の出現数で 96 → 93、*N.M* の句で 58 → 59。節単位の参照は T54 で §8.4 から減り、*N.M* の参照は他の試作で増えた）。件数は読んだ範囲の記録で、比べる数ではない。そのうち参照元か参照先が変わった条の 47 件を、指す先の条と並べて読んだ。

**46 件は clean**。たとえば §2.4 の *"Section 15.1 governs their construction"* は、T43 で直した §15.1 が *"where a provision is capable of more than one reading"* と条項一般を対象にしているので、許諾だけでなく不行使約束の解釈も覆う。§8.4 の *"The proviso in Section 8.1 as to subject matter contained in the Work"* は、§8.1 の末尾 *"where the infringement is caused by subject matter contained in the Work as made available by the Dedicator"* をそのまま指す。§16.2 の *"(Section 6.2)"* は、§6.2 が「どの信号も Reservation と読まない」と述べることに当たる。

**残った 1 件 —— §8.6 第 2 文の *them***:

**Before（§8.6 第 2 文）**: *"This covenant is given on the same footing as the covenants in Section 5 and does not wait for either licence to be held ineffective: it operates in every jurisdiction alongside them."*

**最初に出した案 A**: *"This covenant is given on the same footing as the covenants in Section 5 and does not wait for either licence to be held ineffective: it operates in every jurisdiction alongside those licences."*（+1 語・`split()` で数えた）

**採った形（案 C）**: *"This covenant is given on the same footing as the covenants in Section 5 and does not wait for either licence to be held ineffective: it operates in every jurisdiction."*（−2 語・`split()` と `measure_clause_overlap.py --compare` で数えた）

**欠陥**: *them* の直前の複数の名詞は *"the covenants in Section 5"* で、*"either licence"* は単数である。文法どおりに読めば、§8.6 の約束は「§5 の約束と並んで」働く、となる。我々の記録はどれも「許諾と並んで」と読んでいる —— errata E42 の 1.4 の欄（*"a covenant in every jurisdiction alongside the licences"*）、`against.md` #279、`ACD-1.0.submission-reference.md` 80 行目、`ACD-1.4-CHANGELIST.md` の §8.6 の行（「全法域で許諾と並んで常に働く」）、`QUESTIONS-FOR-COUNSEL.md`（*"the 1.4 draft makes it operate alongside the licences in every jurisdiction"*）。**この分岐は 1.4 草案の 2 つの修正が組になって生じた**: 11-01 の E42 の修正（`fece2e27`）で *alongside them* が入ったとき、直前は単数の *"the covenant in Section 5"* で、*them* は 2 つの許諾しか指せなかった。11-08 の E71 の修正（`28dc458e`・単数を複数へ）で、*them* の直前に複数の名詞が来た（**訂正**: 最初は `5b1d487b`・11-07 と書いたが、その commit の §8.6 の差分は折り返しが変わっただけで単数のままだった。`git log -S` の一致を差分で確かめずに書いた。portfolio-00 の指摘）。どちらの修正も単独では正しい。1.0〜1.3 にこの文は無いので、採るなら errata ではなく `ACD-1.1-SELF-AUDIT.md` に記録する。

**作用は変わらないと読む理由**: どちらの読みでも、約束は *"in every jurisdiction"* で働き、*"does not wait for either licence to be held ineffective"* が許諾の判断を待たないことを述べ、§2.4 が許諾と約束は互いに独立に重ねて働くと述べる。「§5 の約束と並んで」と読んでも、許諾と並ぶことは失われない。ゆえに直す理由は基準 4（文法的な明晰さ）と、記録 5 か所が本文を言い換えた文の正しさである。

**案は 3 つで、A を出す**: A *alongside those licences*（+1）。B *alongside both licences*（+1）は、*both* が「両方の許諾が効いている法域で」と読まれうる —— それは第 3 文が「You は決めなくてよい」とする問いそのものである。C *alongside them* を消す（−2）は、記録が言い換えた「許諾と並んで」を本文から外し、並んで働くことを §2.4 にだけ負わせる。

**⚠ 逆側**: (1) どちらに読んでも作用は同じで、多くの読み手は、コロンの後ろが *"either licence"* を受けて述べる文なので、すでに許諾と読む。直すのは害の無い分岐かもしれない。(2) *those licences* の先行詞 *either licence* は単数で、数は合わない。§8.6 に許諾は 2 つしか出ず、§8.2 が *"The licences granted by Sections 8.1 and 8.4"* と呼ぶので、指す先は 1 つに決まると読む。(3) 採れば、E42 の *"1.4 draft:"* の引用（Check 468w）、冒頭の一覧、`This draft:` の語数、CHANGELIST の行と語数の内訳、逐条の §8.6 の行を同じ commit で直す。mutation の anchor はこの句に掛かっていない（grep で確かめた）。(4) 相互参照の読みは 47 件で、変わっていない条どうしの 41 件は 11-06 の読みに依っている。

**portfolio-00 の反例（2026-11-12）**: (1) **案 A は、曖昧さを 1 つ消して、もっと重い結び付きを 1 つ作る。** §8.6 第 2 文の役目は、許諾が効かない法域でも約束が残ることである。*alongside those licences* は「許諾が在る限りで並んで働く」と読め、許諾が無効と判断された法域では並ぶ相手が無い。直前の *"does not wait"* は発動の時点を述べ、許諾が倒れた後の存続は述べないので、この読みを消し切らない。(2) 代案は *alongside them* を外すこと（−2 語）。並んで働くこと（累積で、予備ではないこと）は *"does not wait"* が、許諾の効力に依らないことは第 3 文 *"nothing permitted by this Dedication depends on that question or on how it is answered"* が、§5 との関係は *"on the same footing as the covenants in Section 5"* が持つ。

**25 の読み**: (i) この反例は案 A だけでなく、**いまの本文にも当たる** —— 記録 5 か所のように *them* を許諾と読めば、いまの本文が同じ結び付きを持つ。欠陥は「文法の分岐」から「片方の枝が条の役目に逆らう」へ強まった。(ii) portfolio-00 が問うた「*alongside* が無いと予備として働くと読まれないか」は、§2.4 第 2 文 *"none is conditioned on another being effective or on another's failure"* が閉じる。この文は両方の向き（他が効いていることを条件にしない・他の失敗を条件にしない）を述べるので、案 A の結び付きにも、案 C の予備の読みにも逆らう。ただし条の中の明示の語は一般の条より強く読まれうるので、語を置かない C が安い。

**portfolio-9b の測定（2026-11-12）**: 案 A について 80 条・条の本文 5,055 → 5,056 語・重複 69 → 69・先行詞の無い指示語 0 / 0・効果を運ぶ語の減少なし。案 C について同じ道具を 25 が回し、5,055 → 5,053 語・重複 69 → 69・族 51・指示語 0 / 0・§8.6 は 100 → 98 語、`--guard` は 468u の目印 17 件すべて在り・468r の語 0・除外の句の欠け 0。外した語に依拠する箇所は外向き 1（`submission-reference.md` 74 行目・三つの足場の説明で、条番号への依拠）と記録 2（E42・`QUESTION-INDEX.md` 58 行目・後者も条番号への依拠）。mutation の anchor はこの句に無い。

**同じ型を草案全体で探した（代名詞のレンズ）**: T56 は、文そのものでなく直前の文が変わって生じた。11-06 以後に変わった 24 文に含まれる代名詞と指示語（*they / them / their / it / its / those / these / this / either / both / such*）と、変わった文の次の 14 文の同じ語を、先行詞が 1 つに決まるかで読んだ。T56 のほかに分岐は 0 件（§5.2 末尾の *it* 3 つは Dedicator と Work、§8.3 第 2 文の *they* は前の文の Sections 8.1 and 8.4、§16.2 第 3 文の *It* は前の文の notice に決まる）。5a の「先行詞の無い指示語」の道具は *those Sections* の形を見るもので、裸の代名詞は見ない（1 冊目の記録）ので、このレンズは読みで行った。

**採否（2026-11-12・採った・案 C・−2 語）**: 欠陥は具体的に立つ —— 記録がしている読み（*them* = 許諾）が、条の役目（許諾が倒れても残る）に逆らう余地を本文の語に置いている。C は分岐の両方の枝を語ごと消し、作用は *"does not wait"*・*"in every jurisdiction"*・§2.4 第 2 文・第 3 文が持つ。草案・冒頭の一覧（§8.6 の項の *"alongside the licences"* も外した・−67 → −69 語）・`This draft:`（5,553 → 5,551 語）・`ACD-1.4-CHANGELIST.md`（表の行・語数の内訳の特許の束 −2 → −4・合計 +110 → +108・英文の下書きの語数）・逐条の §8.6 の行・E42 の 1.4 の欄（*"as adopted on 2026-11-01"* の形へ）・言い換えていた外向きの 2 か所（`submission-reference.md`・`QUESTIONS-FOR-COUNSEL.md`）・長さの数（`SUBMISSION-MATERIALS.md`・`ACD-OSI-BOTTLENECKS.md` B3）を同じ commit で直した。1.0〜1.3 に文が無いので `ACD-1.1-SELF-AUDIT.md` §3z に記録した。**⚠ 逆側**: (1) どちらに読んでも作用は同じだと 11-12 の朝には書いた。結び付きの読みは §2.4 第 2 文が逆らうので、勝つ読みではない。直したのは、争う足場を本文の語に置かないためである。(2) 「許諾と並んで」という説明は本文の語でなく §2.4 に負う。against #279 の言い換えは portfolio-00 の側で見る。

### 14.32 作用の条の長い文を、作用を変えずに分けられるか（T57・T58・T59・採った・+1 語・2026-11-12）

**レンズ**: OSI の新規ライセンスの基準 4（文法的・構文的に明晰）と、長さと読みにくさへの審査者の異議（Chestek 氏 *"excessively wordy"*・#6）。作用の条の文を `split()` で数え、上位を読んだ（2026-11-12 の草案）: §5.2 第 1 文 149 語（(a)〜(d) の列挙を 1 文に持つ）、§16.4 第 3 文 89 語、§2.6 第 2 文 77 語、§4.2 74 語、§1.10 74 語、§8.1 73 語、§8.4 第 1 文 70 語。§5.2 は列挙の項ごとに読めるので分けない。§4.2・§1.10 は定義と権利の列挙で、分けると列挙の範囲が文ごとに切れる。§8.1・§8.4 は許諾の文で、目的語・請求項・因果の限定が 1 文にあることが許諾の範囲を決めるので分けない。オーナーの依頼（2026-11-12「ACD-1.4-DRAFT.txt もガンガン更新してより良くし続けて」）を受けて、試作の数を増やす最初の組である。

**T57: §16.4 第 3 文（89 語）を 2 文に分ける（+3 語・`split()` で数えた）**

**Before**: *"A modified text may not be distributed under any name that contains "Autonomous Commons Dedication", regardless of case, or under any identifier that contains "ACD-", regardless of case, followed by a digit, except by the Steward (Section 16.5), and by the Steward only as a new version under a version number and identifier that no earlier text the Steward or a former Steward has published, other than a draft identified as such, has borne, so that each name and identifier in this family continues to denote one fixed text."*

**After**: *"… followed by a digit, except by the Steward (Section 16.5). Such distribution by the Steward is permitted only as a new version under a version number and identifier that no earlier text the Steward or a former Steward has published, other than a draft identified as such, has borne, so that each name and identifier in this family continues to denote one fixed text."*（44 語と 48 語）

**欠陥**: 1 文に、2 つの名前の肢（それぞれに *regardless of case*）、例外、例外の限り方（版番号と識別子・先の本文の範囲・草案の除外）、目的の句が入っている。*"except by the Steward (Section 16.5), and by the Steward only as …"* の *and* は例外を限る語だが、括弧の参照の直後に来るので、例外が 2 つ並ぶとも読める。読み手は 89 語を最後まで保持しないと、何が禁じられ、誰が何の条件で外れるかを決められない。

**作用は変わらないと読む理由**: *"Such distribution"* は直前の文の禁止の対象（改変した本文を名前・識別子の下で配ること）を指し、Steward の例外は元の文と同じく新しい版に限られる。代名詞（*do so* / *them*）を使うと T56 と同じ先行詞の分岐を作るので、名詞で受けた。468m が見る例外の句（*"other than a draft identified as such, has borne"*）と、mutation の anchor（*"the Steward has published"*）は語のまま残る。

**⚠ 逆側**: (1) *"is permitted"* は、Dedication が Steward に許可を与える文に読まれうる。元の文も *"except by the Steward"* で同じことを述べているので、範囲は変わらないと読むが、反例を求める。(2) +3 語。(3) T44〜T50 で語を足してきた文で、分け方が過去の試作の結論に触れないかを確かめた（§14.20〜§14.22・T27 の表に文を分ける案は無い）。

**T58: §2.6 第 2 文（77 語）をセミコロンで 2 文に分ける（0 語）**

**Before**: *"… so that a person or an automated system reading the Work can determine what this Dedication does not cover; this undertaking binds that Dedicator and imposes nothing upon You, and Section 6.5 states why it matters."*

**After**: *"… so that a person or an automated system reading the Work can determine what this Dedication does not cover. This undertaking binds that Dedicator and imposes nothing upon You, and Section 6.5 states why it matters."*

**欠陥**: 約束の文（誰が何を識別するか）と、約束の性質の文（誰を縛り誰を縛らないか）が 1 文にあり、後半の *this undertaking* は文の中の前半を指す。分けても指す先は変わらず、読み手は約束の範囲を読み終えてから性質に移れる。欠陥としては弱い（作用の分岐は無い）。

**⚠ 逆側**: 0 語で作用も変わらないので、直さなくても害は無い。直す理由は基準 4 と、77 語の文を 1 つ減らすことだけである。

**T59: §2.8 第 2 文の限りの無い断定を、第 1 文の限りに結ぶ（+4 語・`split()` で数えた・portfolio-00 の候補）**

**Before**: *"This Dedication, in respect of the Work, binds the Dedicator's successors, assigns, heirs, and personal representatives, and any person to whom a Covered Right or a patent claim in the Work is transferred, to the fullest extent the law permits. A transferee takes subject to it, Section 6 included."*

**After**: *"… to the fullest extent the law permits. A transferee takes subject to it to the same extent, Section 6 included."*

**欠陥**: 第 1 文は譲受人を縛ることを *"to the fullest extent the law permits"* に限るが、第 2 文は限りの無い断定である。`QUESTIONS-FOR-COUNSEL.md` 問 1 (j) が書くとおり、17 U.S.C. §205(e) は、権利者の署名した書面の無い非独占の許諾が後の譲渡に優先しない場合を定めうる。審査者が (j) を読めば、第 2 文は制定法より強い主張をしていると突ける —— 本文が自分で法を決めている形で、E23（§2.8 が別の権利者の法定の行為を本文で決めていた）と同じ型である。文は 1.0 から在る（1.0 の *"A transferee takes subject to them"*）ので、採るなら errata に記録する。

**作用は変わらないと読む理由**: 法が許す範囲では、元の文と同じく譲受人は献呈に服し、§6 も含む。法が許さない範囲では、元の文も効かない（本文は制定法を外せない・問 1 の (b)(h) の扱い）。直るのは、本文が言えないことを言う形だけである。*"Section 6 included"* は残るので、AI の利用の許可が譲受人に及ぶことの明示は失わない（portfolio-00 が気にした点）。

**⚠ 逆側**: (1) 限りを 2 回書くと、他の条（§5.3・§12.4 の *"to the fullest extent the law permits the Dedicator to bind them"*）との並びで、限りの無い文が別に在るのではと探させる。§5.3・§12.4 は 1 文なので、同じ型の残りは無いと読むが、反例を求める。(2) 法律家の答え（問 1 (j)）が出れば、限り方の語そのものが変わりうる。(3) +4 語。代案の「第 2 文を外す」（−7 語）は、*Section 6 included* の明示を失うので採らない。

**依頼**: portfolio-00 に反例（特に T57 の *"is permitted"* と *"Such distribution"* の指す先、T59 の *"to the same extent"* の掛かり先）を、portfolio-9b に `--compare / --guard` と代名詞の段を頼む。

**portfolio-00 の反例（2026-11-12）**: T57 は作用が同じに読めるが、*"is permitted"* は分岐を生む —— §16.6 は §16.4 を Work の条件でなく文書の規律と置くので、*"Such distribution by the Steward is permitted"* は Dedication が Steward に許可を与える文（許可の源）と読まれうる。元の文は制限の例外で、許可を与えていない。代案は制限の声を保つ *"That exception reaches only a new version …"* で、*That exception* は直前の *except by the Steward* に一意に向く。T58 は clean（*This undertaking* は識別の約束を受ける）。T59 の *"to the same extent"* は何と同じかが書かれておらず、「Dedicator が拘束されるのと同じだけ」と読めば外したい無限定の強さが戻る。代案は *"to that extent"*（+3 語）。

**portfolio-9b の測定（2026-11-12）**: 最初の 3 案を再現し、5,053 → 5,060・重複 69・族 51・指示語 0 / 0・代名詞の段 6 件（どれも先行詞は 1 つ）・外した文に依拠するドシエ 0・468u 17/17・468r 0。

**採否（2026-11-12・3 つとも採った・反例の代案の形・+1 語）**: T57 は *"That exception reaches only a new version"*（−2 語）、T58 は句点（0 語）、T59 は *"to that extent"*（+3 語）。採った形で 25 が `--compare` を回し、5,053 → 5,054・重複 69 → 69・族 51・指示語 0 / 0、`--guard` は 468u 17/17・468r 0・468m の句は 1 行のまま。草案・冒頭の一覧（§2.6 は語数そのまま、§2.8 は −71 → −68、§16.4 は +43 → +41）・`This draft:`（5,551 → 5,552）・`ACD-1.4-CHANGELIST.md`（表の 3 行・内訳の名前の保護 +49 → +47・その他の明瞭化 +40 → +43・合計 +108 → +109・1.0 から 656 語・英文の語数・切り替えの日の長さの行）・逐条の 3 行・長さの数（`SUBMISSION-MATERIALS.md`・`ACD-OSI-BOTTLENECKS.md` B3）を同じ commit で直した。T59 の文は 1.0 から在るので、errata は portfolio-00 が足す。**⚠ 逆側**: (1) T57・T58 は作用の分岐を閉じる修正ではなく、読みやすさのための修正である（基準 4）。(2) 最初の案は 2 つとも反例で替わった —— 名指しの語（*Such distribution* / *the same extent*）も、指す先が 1 つに決まるかを当てる。
