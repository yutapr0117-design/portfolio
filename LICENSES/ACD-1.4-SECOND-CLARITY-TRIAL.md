---
file: LICENSES/ACD-1.4-SECOND-CLARITY-TRIAL.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-06
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

**逆側**: root の通知は、Dedicator が後で隣に置いた、公開するつもりのないファイルにも及ぶ。root の LICENSE が repository 全体を覆う慣行どおりで、除外したいものは §2.6 の識別の形で標示する。ただし §3 は取り消せないので、置き間違えの費用は他のライセンスより重い。README だけに通知を置いた Dedicator は、その README が伴う素材の範囲が争点になる。*identifies* で *this project* を名指していれば足り、§16.1 の雛形は *"This work"* と書くので、雛形どおりの通知は概ね足りる。

### 14.10 T24〜T27: 1.3 から変わった 35 条を 1 条ずつ読み直した（+18 語）

確定前の検証（段 7）は 2026-11-06 に済ませたが、そのあと本文は T16〜T23 で変わった。1.3 と比べて文が変わった 35 条を 1 条ずつ担当させ、(1) 変更が他の条の語や前提を壊していないか、(2) 新しい語が理由に書かれていない読みを作っていないか、(3) 変更が閉じようとした欠陥を実際に閉じたか、を読んだ。候補 56 件のうち反証に 6 件が残り、4 件を直した。

| 条 | 欠陥 | 直し方 |
| :-- | :-- | :-- |
| §1.9（T24・+3）| T19 の理由（寄与者は表示を見ている）が語で担保されていない。§10.2 で表示を外したミラーも *"offering the Work under this Dedication"* に当たり、知らない人が修正を送ると Dedicator になる | *"offering the Work with a notice of this Dedication"*。§16.2 によりタグも通知に当たる |
| §8.5（T25・+3）| *"is controlled by the Dedicator if"* は十分条件の形で、通常の意味の control（上流へ料金を払う独占的実施権者など）が並んで残る。§8.5 は §15.1 の射程にあるので、E39 が外した請求項に届く読みが勝つ | *"if, and only if"* |
| §16.2（T26・+10）| 1.4 でタグだけの適用を認めたので、1 つのファイルのタグが *accompanies* でリポジトリ全体を Work にする読みがある。E61 が *in whole or in part* を外して閉じた形が戻る | *"A tag placed within a file accompanies that file alone."*（SPDX と REUSE の慣行と同じ）|
| §16.4（T27・+2）| *"begins with \"ACD-\""* は、§16.1 と §16.2 が使う *LicenseRef-ACD-1.4* に届かない | *"ACD-" or "LicenseRef-ACD-"* |

**逆側**: T24 では、表示のない場への寄与は Contribution でなくなり、取り込むと §2.6 の識別の対象になる。T26 では、root にタグ 1 行だけの LICENSE ファイルを置いた Dedicator は、そのファイルにしか適用していないことになる。§16.1 の雛形は *"This work"* と書くので、雛形どおりの通知はこれに当たらない。T27 では、SPDX の *LicenseRef-* は文書ごとの識別子なので、無関係な第三者が自分の別のライセンスに付けても、改変した本文を配らない限り当たらない。

**残したもの**: §2.6 で識別した素材にも §16.2 の既定が及ぶ読み（Dedicator はその素材の権利を持たないので §2.7 で届かず、残るのは Dedicator 自身の編集部分という狭い場面）。§5.2(b) が商標の規約を課すことまで止める読み（規約の対象は商標であって Work ではなく、+27 語の除外に見合わない）。

