---
file: LICENSES/ACD-1.0.gap-measurements.md
audience: OSI license-review participants / licence reviewers / 監査人 / 後任 AI
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.comparison.md (切り出し元・条項比較) / LICENSES/ACD-1.0.gap-census.md (同じ 141 本への 3 gap の全数表)
---

# gap の主張を既存ライセンスの本文に当てた測定（§1.96 / §1.97 / §1.104）

**`ACD-1.0.comparison.md` から 2026-09-25 に切り出した**（893 行で advisory 900 の手前に達したため）。
**節番号は動かしていない**（`§1.xx` の共有採番のまま）。切り出し元には案内の節を残した。

**なぜ分けたか**: 切り出し元は「既存ライセンスと ACD-1.0 を**条項で比べる**」文書で、ここに移した 3 節は
「**我々の gap の主張が、既存ライセンスの本文に当てて成り立つか**を測った」記録である。
**同じ用途の全数表は [`ACD-1.0.gap-census.md`](ACD-1.0.gap-census.md)** にあり、読み手が重なる。

## 1.96 gap を「語の不在」から「法的効果の不在」へ移した —— 承認済み instrument の grant を逐語で当てた（2026-09-18）

**これまでの gap 論証は語の不在に寄っていた**（§1.95 の実測: 承認済み 141 本に "sui generis" / TDM /
machine learning が **0 件**）。**その caveat は我々自身が同じ節に書いている** ——
***語が無いことは、効果が無いことではない。*** MIT の *"deal in the Software without restriction"* が
黙示に及ぶ、という読みは成り立つ。

**だから grant 条項を逐語で読んだ。** OSI の承認基準は「既存で埋まらない gap」を要求し、
**承認された新規 instrument の実例（OSC License v1）は、gap を *1 条・1 法域* の具体で述べている**
（`review-corpus.md` §1.69）。**我々も同じ粒度まで降りる。**

### 逐語（SPDX の canonical text・2026-09-18 取得）

| instrument | grant の文言 | 射程 |
| :-- | :-- | :-- |
| **MIT / MIT-0** | *"to deal in the **Software** without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell"* | **広いが、権利の種類を名指ししない。** 非著作権の権利に及ぶかは**解釈**である |
| **0BSD** | *"Permission to **use, copy, modify, and/or distribute** this software for any purpose"* | **著作権の動詞を列挙している。** *extraction* / *re-utilisation* は無い |
| **Unlicense** | *"dedicate any and all **copyright interest**"* ＋ fallback で *"to use, copy, modify, publish, distribute"* | **自ら「copyright interest」と限定している** |
| **Apache-2.0 §2** | *"**copyright license** to reproduce, prepare Derivative Works of, publicly display, publicly perform, sublicense, and distribute the Work"* | **明示的に copyright license である** |
| **Apache-2.0 §3** | *"patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer **the Work**"*、かつ *"necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with **the Work**"* | **Work に限定。** 訓練で生じたモデル・出力には届かない |
| **CAL-1.0 §3.1(a)** | *"Take any action with the Work that would infringe the **non-patent intellectual property laws of any jurisdiction**"* | **非特許 IP 全般に及ぶ** ——**database 権にも届く。ただし §3.1 は「§4 の遵守を条件とする」** |
| **CAL-1.0 §3.1(b)/§3.2(a)** | claims *"embodied in the Work as distributed by Licensor"*、かつ **combination で初めて侵害されるクレームは明示的に除外** | **モデル（＝他要素との結合）には届かない** |

### そこから出る gap —— 1 文で述べられる

> **OSI が承認した instrument の中に、(i) データについての非著作権の権利へ*明示的に*及ぶ grant と、
> (ii) 著作物がモデルへ変換された後も残る特許許諾と、(iii) 受領者への条件ゼロ、
> の 3 つを同時に満たすものは無い。**

**3 つのうち 2 つまでは存在する。**

- **条件ゼロで広い**（0BSD / MIT-0 / Unlicense）——しかし **grant は著作権の語彙で書かれ、特許が無い。**
- **非著作権の権利に届く**（CAL-1.0）——しかし **条件が重く**、**特許は結合を明示的に除外する。**
- **特許がある**（Apache-2.0）——しかし **copyright license と自称し**、**特許は Work に限定される。**

**ACD はこの 3 つを同時に満たす**（§1.5 が Covered Rights に sui generis database 権を含め、
§7 がその行為の語（*extract / re-utilise*）で許し、§8.4 がモデル・パラメータ・出力へ届き、
§10.1 が条件を置かない）。

### ⚠ 逆側 —— この節が establish しないこと（同じ重さで書く）

1. **MIT の *"without restriction"* が非著作権の権利に及ぶ、という読みは十分に成り立つ。**
   **我々は「及ばない」と主張していない。** 主張しているのは **「明示されていないので解釈になる」**
   ことだけで、**§6.5 の基準（自動化システムが判定できない許諾は許諾ではない）に照らすと
   解釈に委ねること自体が費用になる**、という位置づけである。**これは法的主張ではなく設計上の主張である。**
2. **0BSD / Unlicense の読みは、我々の逐語読解であって法律意見ではない。**
   **「著作権の動詞しか書いていないから database 権に及ばない」は、争える読みである。**
3. **CAL-1.0 は非著作権 IP に届く。** したがって **「承認済みに database 権へ届くものは無い」は偽**であり、
   **正しくは「条件ゼロで届くものが無い」**である。**この訂正は §1.95 の読みを狭める。**
4. **3 つを同時に満たす必要があること自体は、まだ実需で示されていない**（register B2）。
   **gap の存在と、その gap を埋める需要の存在は別である。**
5. **法律家のレビューを代替しない。** ここで行ったのは**条文の文言の比較**であって、
   各法域での効果の判定ではない。

## 1.97 gap を「選んだ 6 本」から「承認済み 141 本の全数」へ移した（2026-09-19）

**§1.96 は 6 本の grant 条項を逐語で比べた。** その形の弱点は `BLIND-SPOTS.md` が名指ししている ——
**比較対象を選ぶのは我々である。** **だから全数で当てた。**

### 方法（先に限界を書く）

SPDX の `license-list-data` から **`isOsiApproved` かつ非 deprecated の 141 本**を取得し、
**「受領者に義務を課す語」**（*provided that* / *must* / *required to* / *retain* /
*shall be included* / *may not* …）の出現を数えた。

**⚠ 免責の *shall* を条件と数えない。** *"IN NO EVENT SHALL THE AUTHOR BE LIABLE"* は義務ではない ——
初版はこれを数えて **0BSD を「条件 1 件」と報告した。**

**⚠ そしてコーパスは英語だけではない。** 非 ASCII を多く含む text が **18 本**あり、
**英語の語で数えると条件を見落とす。** 実際に 2 件出た:

- **`OSC-1.0`（ドイツ語）** —— *"Der obige Urheberrechtshinweis und dieser Genehmigungshinweis
  **müssen** in allen Kopien … enthalten sein"* ＝ **通知の保持義務がある。**
- **`LiLiQ-P-1.1`（フランス語）** —— *"les étiquettes ou mentions faisant état des droits d'auteur …
  **ne doivent pas être modifiées ou supprimées**"* ＝ **通知の改変禁止がある。**

**どちらも英語の検出器では「義務語 0 件」と出た。** **読んで落とした。**

### 結果 —— 受領者に条件を課さない承認済みライセンスは **3 本**である

| | 条件 | 特許許諾 | 非著作権の権利への明示 |
| :-- | :-- | :-- | :-- |
| **0BSD** | **無し** | **`patent` の語が 0 回** | 無し（*use, copy, modify, and/or distribute* の 4 動詞）|
| **MIT-0** | **無し** | **`patent` の語が 0 回** | 無し（*deal in the Software without restriction* ——**種類を名指ししない**）|
| **Unlicense** | **無し** | **`patent` の語が 0 回** | **無し。自ら *"any and all **copyright** interest"* と限定する** |

**残る 138 本は、受領者に何らかの義務を課す**（通知の保持・改変の表示・名称の不使用など）。

### したがって、gap は選択ではなく全数で述べられる

> **OSI が承認した 141 本のうち、受領者に条件を課さないのは 3 本であり、
> その 3 本はいずれも特許について 1 語も述べず、非著作権の権利を 1 つも名指ししない。**

**§1.96 の 1 文はこれで下支えされる** ——(i) データについての非著作権の権利、(ii) モデルへの変換後も
残る特許許諾、(iii) 条件ゼロ、**の 3 つを同時に満たすものが無い**のは、
**我々が 6 本を選んだからではなく、141 本のうち条件ゼロが 3 本しか無く、その 3 本が他の 2 つを持たないから**である。

### ⚠ 逆側 —— 同じ重さで

1. **「述べていない」は「及ばない」ではない**（§1.96 の逆側 (1) と同じ）。
   **MIT-0 の *without restriction* が特許や database 権に及ぶ読みは成り立つ。**
   **我々が主張するのは、及ばないことではなく、明示されていないことである。**
2. **条件があること自体は欠点ではない。** 138 本のほとんどは通知の保持だけを求めており、
   **それが重いと述べているのではない。** 述べているのは**「条件ゼロ」という集合の小ささ**である。
3. **分類は語の検出に基づく。** 非英語の 2 件は読んで訂正したが、
   **読んでいない text が残っている可能性は排除できない** ——
   **再現手順を置くので、誰でも同じ数を出し直せる。**
4. **この census は「だから承認せよ」を意味しない。** OSI の基準 7 は gap を要求するが、
   **gap の存在は承認の十分条件ではない**（理事会は *"even where they cannot identify a specific
   aspect of the OSD"* でも consensus で否決しうると述べている）。

## 1.104 既存ライセンスについての我々の主張を、その本文に当てた（2026-09-22）—— 5/6 が真、1 件を訂正

**未使用の次元だった。** このドシエの gap 論は「既存ライセンスは X を持たない」に依っているが、
**その主張を実際の本文に当てた記録は 1 つも無かった** ——本文はリポジトリに無く、Check も無い。

**取得**: SPDX license-list-data から 7 本（MIT / MIT-0 / 0BSD / Unlicense / CC0-1.0 /
Apache-2.0 / BlueOak-1.0.0・2026-09-22）。

| 我々の主張 | 実測 |
|---|---|
| MIT-0 / 0BSD / Unlicense は **TDM と EU sui generis データベース権に沈黙** | **真。** 3 本とも該当語 0 件。**主張が正しく 3 本に限定されている**ことも確認 |
| Apache-2.0 は **特許の機構を既に持つ** | **真** |
| CC0 は **特許を明示的に放棄しない** | **真。** §4(a) *"No trademark or patent rights held by Affirmer are waived…"* |
| 機械生成物・計算的利用に触れる既存本文は無い | **真。** 7 本すべてで該当語 0 件 |
| MIT / 0BSD / Unlicense は**列挙をほとんど持たない** | **真。** `including` が 2 / 1 / 1 件（ACD-1.0 は 14 件）|
| 🔴 MIT / 0BSD / Unlicense は**解釈準則を持たない** | **不正確だった。** 一般準則は確かに無いが、**MIT は operative grant で `including without limitation`**、Unlicense は免責で `including but not limited to` を使う ——**device は在り、規則として述べていないだけ**である。1.2 草案ヘッダを訂正した |

**なぜこの 1 件が重いか**: **MIT は世界で最も読まれているライセンス本文**であり、
この主張は**§15.5 を足す理由**として書かれている。**審査者は暗記している。**
訂正後の形は**論拠を弱めない** ——本当の論拠は後半（列挙がほとんど無いので準則が要らない）で、
そちらは実測で真である。

### ⚠ 検出器を 2 回疑った

1. **BlueOak が「機械学習」に一致した** ——**名称が Blue Oak *Model* License** だから。
2. **CC0 が「sui generis」に一致したと読んだ** ——実際は `find` が **-1** を返し、
   `t[max(0,i-130):...]` が **file の先頭**を表示していた。**「見つからない」が「見つかった」に見える形。**
   正しくは CC0 は `sui generis` の語を持たず、**`database rights`（Directive 96/9/EC を名指し）と
   `moral rights` を放棄対象に列挙している** ——どちらも我々の主張とは衝突しない
   （我々は MIT-0 / 0BSD / Unlicense に限定して述べている）。

### 第 2 巡 —— 比較表の逐語引用そのものを当てた（同日・12 件すべて一致）

**1 巡目は「X を持たない」型の主張を当てた。2 巡目は逆で、比較表が
既存ライセンスから*引いている逐語*が、その本文にそのまま在るかを当てた。**

| 当てた主張 | 結果 |
|---|---|
| Apache-2.0 §6 商標（*"This License does not grant permission to use the trade names…"*）| **一致** |
| Apache-2.0 §2 copyright license の動詞列 | **一致** |
| Apache-2.0 §3 patent license の動詞列 ＋ *"necessarily infringed by their Contribution(s)"* | **一致** |
| MIT *"to deal in the Software without restriction, including without limitation…"* | **一致** |
| MIT-0 *"deal in the Software without restriction"* | **一致** |
| 0BSD *"Permission to use, copy, modify, and/or distribute this software for any purpose"* | **一致** |
| Unlicense *"dedicate any and all copyright interest"* | **一致** |
| 0BSD / MIT-0 / Unlicense に `patent` が **0 回** | **一致（3 本とも 0）** |
| 0BSD に *extraction* / *re-utilisation* が無い | **一致** |

**12 件すべて一致。** **比較の土台は、実本文に当ててもそのまま立つ。**
**1 巡目で 1 件外れたことと、2 巡目が全件通ったことは、同じ重さで書く** ——
**外れたのは「持たない」型の否定命題で、通ったのは逐語引用である。**
**否定命題のほうが外れやすい**（何が無いかは、全部読まないと言えない）。

**⚠ この節を書いた最初の番号は §1.103 で、同じ日に `review-rules.md` が取った番号と衝突していた。**
共有採番は 4 file に分かれており、**衝突すると参照は解決するのに別の節へ着く**。
**gate（Check 471(f)）は正しく発火する** ——probe で確認した。**今回は私が grep で先に見つけただけで、
gate の穴ではない。** 空き番号を実測してから付けること。

**Check は作らない。** 外部本文はリポジトリに無く、取得を CI に入れるのは壊れやすい
（`PEER-REVIEW-WATCH.md` が外部フォーラムの定期取得について同じ判断をしている）。
**次に gap 論を書き換えるときは、この 6 行を手で当て直すこと。**
