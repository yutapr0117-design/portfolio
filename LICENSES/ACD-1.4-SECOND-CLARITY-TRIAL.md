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
