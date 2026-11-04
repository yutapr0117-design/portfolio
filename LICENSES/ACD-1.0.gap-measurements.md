---
file: LICENSES/ACD-1.0.gap-measurements.md
audience: OSI license-review participants / licence reviewers / 監査人 / 後任 AI
last-updated: 2026-11-04
canonical-ref: LICENSES/ACD-1.0.comparison.md (切り出し元・条項比較) / LICENSES/ACD-1.0.gap-census.md (同じ 141 本への 3 gap の全数表)
---

# gap の主張を既存ライセンスの本文に当てた測定（§1.96 / §1.97 / §1.104 / §1.129 / §1.130 / §1.133）

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
| **Unlicense** | *"dedicate any and all **copyright interest**"* ＋ 許可の文 *"Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software"*（2026-11-04 訂正: 旧版は語順を変え compile / sell を落とした形で逐語の記法に入れていた・5a の照合） | **自ら「copyright interest」と限定している** |
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

## 1.129 献呈の文言が「CC0 並みに comprehensive か」は、委員会側が言葉にした試験である —— 当てると 5 要素中 4 つが被覆、1 つが未対応（2026-09-28）

**`license-review` の全期間 census（199 か月・2026-09-28 実行）が挙げた我々の類型 27 件のうち、
ドシエ未言及だった 2 件を読んだ**（逐語は
`rounds/2017-04-license-review-pd-type-submissions-observed-1of2.txt` ほか）。
そこに **公有化の献呈が測られる試験**が、言葉で置かれている。

McCoy Smith 氏（2017-04-14・PD 用の Modified MIT を提出した者へ）:

> *"The current draft just says ' Public Domain or legal equivalent ' Have you confirmed that
> that statement is **legally effective to result in a dedication to the public domain**? I know
> CC did a lot of work and research into how (in many jurisdictions) one goes about making a
> legally effective public domain dedication, and **the wording they use in CC0 is much more
> comprehensive in the language it uses (in Sec. 2)**. The language you use is **quite brief** …"*

**同じスレッドの最初の実質返信は、Rob Landley 氏が後に我々へ向けたのと同じ問いである** ——
Richard Fontana 氏 *"Are you aware of the Free Public License 1.0.0, also known as the
Zero-Clause BSD license? … **Do you see anything distinctive about your license relative to
FPL/0BSD?**"*（2017-04-13）。**#84 は 2026 年に初めて出た問いではない。**

### 当てた結果

| | 語数 |
| :-- | :-- |
| **CC0 §2（Waiver）** | **173 語**（SPDX の `licenseText` から実測・2026-09-28）|
| **ACD-1.0 §3（放棄）** | **114 語**（3 条）|

**語数では短い。** だが**要素で当てるのが正しい測り方**である ——
CC0 §2 が明文で挙げる 5 要素を ACD の全文へ当てると:

| CC0 §2 の要素 | ACD ではどこか |
| :-- | :-- |
| 全世界・最大期間（延長・復活を含む）| **§3.1「各法域の法が許す最大限まで」＋ §3.2「延長・回復・復活を含む全期間」**。**さらに ACD は §3.2 で補償金・使用料・徴収金まで明示しており、CC0 §2 にはこの語が無い** |
| 現在または将来のあらゆる媒体・形式 | **§4.2** *"in object form, or in any other form, in any medium, and by any means now known or later devised"* |
| 目的を問わない | **§4.1** *"for any purpose whatsoever"* |
| 相続人・承継人に及ぶ | **§2.8**（§3 / §4 / §6 / §8 が承継人・譲受人・相続人を拘束する）|
| **付随する請求権および訴訟原因（既知・未知を問わない）** | **無い。§5.1 の不行使の約束は Covered Rights に限られる**（`against.md` #272）|

**⚠ 5 要素のうち 4 つは、§3 の外に在るが在る。** **「§3 が短い」は「文書が言っていない」ではない。**
**残る 1 つは実際に無い** —— しかも **§1.5 は Covered Rights から特許を除いている**ので、
**そこから外れる請求権（不当利得・不正競争など）には §5.1 が届かない。**

### この節が establish しないこと

**McCoy 氏の試験は 2017 年の 1 通であり、委員会の公式基準ではない。**
**そして「4 つ被覆」は我々の読みであって、審査者の読みではない** ——
**審査者は §3 だけを読んで「quite brief」と判定しうる**（危険は構造ではなく読まれ方に在る、
という `ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B15 節と同じ形）。

## 1.130 審査者が何を言うかは厚く読んだが、通った提出者が*どう振る舞ったか*は一度も測っていなかった（2026-09-28）

**ドシエは審査者側の発言を大量に持っている。****提出者側の振る舞いは 1 つも測っていない。**
我々の提出パケットは*提出者側*の成果物なので、この非対称は測る価値がある。

**窓と道具**: `license-review` の月次アーカイブ 199 か月（2026-09-27 取得）。スレッドは件名の
正規化で束ね、**提出者 = そのスレッドで最も早い 1 通の差出人**と定義した。「返信中央値」は
**他者の発言の後に提出者が次に書くまでの時間**の中央値。

| スレッド | 通数 | 提出者の通数 | 割合 | 返信中央値 | 期間 |
| :-- | --: | --: | --: | --: | --: |
| **CAL**（2020 承認）| 465 | 118 | **25%** | **0.9 時間** | 334 日 |
| **Unlicense**（2020 承認・legacy）| 12 | **1** | 8% | （返信なし）| 80 日 |
| **Unicode v3**（2023 承認）| 8 | 4 | 50% | 3.7 時間 | 97 日 |
| OpenMDW（審査中）| 120 | 12 | 10% | 3.9 時間 | 32 日 |
| ModelGo BY（審査中）| 54 | 28 | 52% | **22.3 時間** | 588 日 |
| **我々（2026-08-26・`license-discuss`）** | **1** | **1** | 100% | **測れない** | — |

### 読み取れること 1 つ

**我々の類型に最も近い承認（CAL = 新規・激しい係争・テキストで立った）の提出者は、
465 通のうち 118 通を書き、他者の発言に中央値 0.9 時間で返している。**
**1 年にわたって、ほぼ即時に、全体の 4 分の 1 を書いた。**

### ⚠ 確立しないこと 4 つ

**(1) n が小さい**（承認は 3 件）。**振る舞いと結果の関係は、この数では因果にならない。**

**(2) 資源の差が混ざっている。** CAL の提出者は弁護士で client を持っていた。
**0.9 時間の中央値は「規律」ではなく「専従できたこと」の反映かもしれない。**

**(3) 逆の例が同じ表に在る。** **Unlicense の提出者は 1 通しか書いていない**（legacy 経路）。
**経路 B（既に使われていること）で通るなら、関与の量は要らない。**
**我々は経路 A しか使えないので、CAL 側が近い**（`board-decisions.md`）。

**(4) そして、これは新しい打ち手ではない。** **この振る舞いは B14（moderation による拒否・発信状態は `FROZEN.md` の POSTING-STATUS）が阻んでいる当のこと
である。** 測って分かったのは**やるべきことが増えた**のではなく、
**#268 / #270 が言っていた「議論の場に居ることが効く」の、提出者側からの裏づけ**である。
**本文を磨くことでは代替できない。**

### 我々の側で、いま決められること

**返信が来たときに何をするかは、いま決めておける。**
`REVISION-PROTOCOL.md` §1 は受領→分解→分類→応答の順序を定めているが、**速さについては何も
言っていない。** **CAL の 0.9 時間は目標ではない**（資源が違う）が、
**「同じ日のうちに、少なくとも受領の確認と、分解の途中経過を返す」**なら、
**AI が下書きを作らずとも steward だけで実行できる**（B14 の下でも、返信は steward 自身が書く）。
**⚠ 返信を書いて送るのは steward 自身である**（B14）。**この速さの方針は AI が決めて置いておく** ——オーナーの裁可を要する項目は無い（2026-11-01 オーナー明言「3人全員に全委任してるからあなた含めた全員に全て許可する。3人全員が私に裁可を求める必要は無い」・2026-10-24「OSI通過の為の何かで私の裁可が必要なものは無いよ」）。

## 1.133 既存ライセンスでは達成できない法的効果を 1 件、承認済み 141 本の原文で閉じた —— §8.4 + §8.2（2026-11-04）

**きっかけ（2026-11-04）**: 別の AI の見解をオーナーが渡した（オーナーの指示ではない）。その見解が置いた成功条件は「既存ライセンスでは達成できない ACD 固有の法的効果を、
少なくとも 1 件、比較対象の原典と具体的な条文で裏付けること。立証できなければ未達と記録する」。
**分担**: 25 = 条文の対置と分割の証明（この節）/ bb = 敵対仮説 6 本の反証と B15（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` B10「2026-11-04 原典による立証」）/
5a = SPDX 原文の取得の再現と逐語照合（census を最新の SPDX で生成し直し、141 本の判定は 1 件も変わらない）。

**原典**: SPDX `license-list-data`（licenseListVersion `8791eda`・releaseDate 2026-10-28・OSI 承認かつ非 deprecated 141 本・取得失敗 0・
取得 2026-11-04T00:06:37Z・`generate_gap_census.py --fetch`）。以下の引用は空白を正規化した逐語。

### 主張（1 文）

**ACD は、Work の計算的利用（学習）と、そこから生じたモデル・出力を作り・使い・売り・輸入する行為について、その利用に依存して侵害される Dedicator の特許請求項を、
条件なしに、どの理由でも終了しない形で許諾する。承認済み 141 本のどれも、この 3 つ（範囲・無条件・終了なし）を同時に与えない。**

**⚠ 2026-11-04 後半に訂正した（25 の指摘と bb の再検査）**: この節の初版は主張を「その利用が実際に侵害する請求項」と書き、下の場面を 1.0 の文で組んでいた。1.1 以降の §8.4 には因果の限定があり、**請求項の範囲で CERN-OHL-P に差を付ける根拠にならない**。主張の強さの分類は下の「独立の再検証」にある。

ACD 側（下の 2 つの引用は 1.0 の文。**1.1 以降の §8.4 は因果の限定の 2 文を足している** —— 1.4 草案 *"This Section reaches only claims whose infringement depends upon the use of the Work; it does not license a claim that would be infringed by a model, parameter set, weight, embedding, or output produced without any use of the Work."*）:
- §8.4 *"under every patent claim owned or controlled by the Dedicator, now or in future, that would be infringed by Computational Use of the Work or by the making, having made, use, offering for sale, sale, importation, or other transfer of any model, parameter set, weight, embedding, or output resulting from that use"*、
  かつ *"The proviso in Section 8.1 as to subject matter contained in the Work is deliberately absent from this Section"*。
- §8.2 *"are subject to no condition and are not terminable by the Dedicator on any ground, including the commencement of or participation in patent litigation by You against the Dedicator or any other person"*。
- §10.1 *"This Dedication imposes no condition, obligation, restriction, or requirement upon You in respect of the Work."* / §10.4 *"No permission granted by this Dedication terminates for any reason."*

### 分割の証明 —— 141 本を 4 つに分け、各組が 3 つのどれを欠くかを原文で示す

**最も強い形は S1 / S2 / S3 に依らない（25 の提案）**: 受領者に条件を課さない承認済みは 3 本（0BSD / MIT-0 / Unlicense・§1.97）で、3 本とも *patent* の語を持たない。**ゆえに「明示の特許許諾 ∧ 無条件」は 141 本中 0 本である。** **⚠ 逆側**: この形なら §8.4 が無くても §8.1 だけで成り立ち、差の中身は条件 1 種である（#241 (2)）。§8.4 に固有の残りは下で分ける。

census（`ACD-1.0.gap-census.md`）は各ライセンスの特許の扱いを「明示 / それ以外」に、明示 65 本の範囲を S1 / S2 / S3 に分けている（判定は 1 本ずつ sha256 つきで表にある）。

| 組 | 本数 | 欠くもの | 原文の根拠 |
|---|---|---|---|
| P0 特許の明示の許諾が無い | 76 | **範囲**（明示の特許許諾そのもの）| 条件の無い 3 本（0BSD / MIT-0 / Unlicense）は *patent* の語を 1 回も使わない（census (b)）。黙示の許諾が及ぶとしてもそのソフトウェアの使用についてで、そこから生じたモデルの販売へ及ぶ根拠は条文に無い |
| P1 範囲が作品・寄与に閉じる（S1）| 58 | **範囲** | 代表: Apache-2.0 *"necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Work to which such Contribution(s) was submitted"*。モデルの性質や学習の手法についての請求項で、寄与が実施しないものは外れる |
| P2 行為の限定が緩い（S2）| 3 | **範囲 + 条件（+ 終了）** | 下表 |
| P3 作品を超える対象を名指す（S3）| 4 | **範囲 + 条件（+ 終了）** | 下表 |

**P2・P3 の 7 本（逐語）**:

| ライセンス | 範囲の限定 | 条件 | 終了 |
|---|---|---|---|
| BlueOak-1.0.0 | *"Each contributor licenses you to do everything with this software that would otherwise infringe any patent claims they can license or become able to license."* —— 行為は無限定だが**このソフトウェアで行うこと**に限る。できたモデルを後で売る行為はソフトウェアで行うことではない | *"The rules of this license are both obligations under that agreement and conditions to your license."* / Notices *"You must ensure that everyone who gets a copy of any part of this software from you, with or without changes, also gets the text of this license or a link …"* | Excuse *"If you do not do so, your license ends immediately."*（*"No contributor can revoke this license"* はあるが、受領者の不履行での終了は残る）|
| EUPL-1.1 / EUPL-1.2 | *"to any patents held by the Licensor, to the extent necessary to make use of the rights granted on the Work under this Licence"* —— Work に与えた権利の行使に必要な範囲 | *"The grant of the rights mentioned above is subject to some restrictions and obligations imposed on the Licensee"*（Attribution right・Copyleft clause）| *"The Licence and the rights granted hereunder will terminate automatically upon any breach by the Licensee of the terms of the Licence."* |
| CERN-OHL-P-2.0 | §6.1 *"patent license to Make, have Made, use, offer to sell, sell, import, and otherwise transfer the Covered Source and Products, where such licence applies only to those patent claims licensable by such Licensor that are necessarily infringed by exercising rights under the Covered Source as Conveyed by that Licensor"* —— Products（*"any device, component, work or physical object … arising from the use, application or processing of Covered Source"*）は**モデルを含みうる**が、請求項は「Covered Source の権利の行使で**必然的に**侵害されるもの」に限る | §4 *"You may Make Products, and/or Convey them, provided that You ensure that the recipient of the Product has access to any Notices applicable to the Product."* | §6.1 *"irrevocable (except as stated in this section 6, or where terminated by the Licensor for cause)"* / §6.2 特許訴訟または無効の確認を求めたとき *"any rights granted to You under this Licence shall terminate"* |
| CERN-OHL-S-2.0 / CERN-OHL-W-2.0 | P と同じ §6.1 の文（*"necessarily infringed by exercising rights under the Covered Source as Conveyed"*）| 互恵（S は強・W は弱）の頒布条件 | §6.1 *"irrevocable (except as stated in subsections 7.2 and 8.4)"* / §7.2 は P の §6.2 と同文 |
| UPL-1.0 | *"(ii) the Larger Works (as defined below) … (b) any piece of software and/or hardware listed in the lrgrwrks.txt file if one is included with the Software"* —— 作品を超えるのは**事前に列挙した** Larger Works だけで、学習でこれから生じるモデルは列挙できない | *"This license is subject to the following condition: The above copyright notice and either this complete permission notice or at a minimum a reference to the UPL must be included in all copies or substantial portions of the Software."* | （終了の定めは無い。条件は在る）|

**したがって**: 範囲の面でモデルに届きうるのは CERN-OHL-P / S / W の 3 本で、3 本とも条件と終了を持つ（**差の根拠はこの 2 つであって、請求項の範囲ではない** —— 「必然的に」の限定は §8.4 の因果の限定と比べて優劣を言えない）。
条件の無い 3 本（P0）は特許の明示の許諾を持たない。**141 本のどの 1 本も、範囲・無条件・終了なしを同時には満たさない。**

### 法的効果の対照 —— 1 つの場面で

**場面**: 受領者 R が Work を学習に使ってモデル M を作り、(1) M を販売し、(2) Work の複製を notice なしで配り、(3) 別件で Dedicator D に特許訴訟を起こした。
D は 2 つの請求項を持つ。C1 は学習の方法についての請求項で、R の学習が実施する。C2 は M の構造についての請求項で、Work を使わず作ったモデルでも侵害される。

| 文書 | R は許諾を持つか |
|---|---|
| ACD-1.0 | C1・C2 とも**持つ**（1.0 に因果の限定は無い）。(2)(3) は許諾を終わらせない（§8.2・§10.1・§10.4）|
| ACD-1.1〜1.4 草案 | C1 は**持つ**。**C2 は読みで分かれる** —— 末文を請求項単位で読めば許諾の外、場面単位で読めば M については持つ（下の「独立の再検証」②）。(2)(3) は許諾を終わらせない |
| CERN-OHL-P-2.0 | C1・C2 が *"necessarily infringed by exercising rights under the Covered Source"* に当たるかは読みに依存する。**当たるとしても** (2) は §4 の条件、(3) は §6.2 の終了に当たる |
| BlueOak-1.0.0 | M の販売は *"everything with this software"* の外と読むのが素直。仮に内と読んでも、(2) は Notices の不履行で、通知から 30 日で *"your license ends immediately"* |
| EUPL-1.2 | C は *"necessary to make use of the rights granted on the Work"* ではない。(2) は Attribution right の違反で *"terminate automatically"* |
| UPL-1.0 | M は lrgrwrks.txt に列挙されていない。(2) は条件の違反 |
| Apache-2.0 | C は寄与が必然的に侵害する請求項ではない。(3) は Work の侵害を主張する訴訟なら終了（*"alleging that the Work … constitutes direct or contributory patent infringement"*）|

### 再現（審査者が自分で確かめる手順）

```
python3 .github/scripts/generate_gap_census.py --fetch   # SPDX の原文を取得（取得日時と licenseListVersion を記録）
python3 .github/scripts/generate_gap_census.py --check   # census が取得物から再生成したものと一致するか
python3 .github/scripts/measure_patent_reach.py          # S2 / S3 の各本から条件と終了の文を逐語で出し、両立する本を数える
python3 .github/scripts/measure_patent_reach.py --express  # 明示の 65 本すべてから義務の文を出す（範囲の分類に依らない）
```

2026-11-04 の実行結果: S2 / S3 は 7 本、7 本すべてに条件の文、UPL-1.0 以外の 6 本に終了の文があり、**「作品を超える特許許諾 ∧ 条件が見つからない」は 0 本**（5a・`measure_patent_reach.py`）。**道具は S1 / S2 / S3 の分類そのものは検証しない**（上の「確立しないこと 2」と同じ限界）。

### 敵対仮説 —— 既存ライセンスでも実現できるか

bb が 6 本を立てて原文で反証した（H1-a BlueOak / H1-b CERN-OHL-P / H1-c UPL / H1-d Apache・BSD-2-Clause-Patent / H1-e 黙示の許諾 / H1-f 承認済みライセンス + 別の特許の誓約 —— 表は EXTERNAL B10）。
**H1-f は「ライセンスで」の外でだけ成り立つ**（誓約は Work と一緒に移らず、OSI が比べるのはライセンスの条文である）。25 が 1 本足す:

| 敵対仮説 | 反証 | 判定 |
|---|---|---|
| H1-g: 0BSD と BlueOak の二重ライセンスで足りる | 選択的（OR）なら、受領者が選んだ 1 本の性質しか得られない —— 0BSD を選べば特許の明示の許諾は無く、BlueOak を選べば条件と終了が付く。併用（AND）なら BlueOak の条件がその特許許諾に付いたまま残る。どちらでも 3 つは同時に揃わない | **反証できた**（ただし H1-f と同じく、複数の文書を組み合わせる形は「1 本のライセンスで」の外にある）|

### 確立しないこと（同じ重さで）

1. **この効果が裁判所で実現するか**は別問題である —— 一方的な文書による無条件の特許許諾の有効性は法域ごとに違い、法的レビューは受けていない（register B1）。
   **立証したのは「本文が与えると述べる効果を、既存のどのライセンスの本文も与えない」ことまで**。
2. **範囲だけで比べる主張は census の S1 判定に依拠している。連言の結論は依拠しない** —— 明示の 65 本すべてに義務の文が在ることを `--express` が範囲の分類なしで再現する（5a）。S1 判定の依拠は（1 本ずつ sha256 つきで記録され、誰でも当て直せる。census は 2026-11-04 に**この節と同じ取得**（8791eda）から生成し直され、141 本の判定は 9 月の 3.29.0 版と 1 件も変わらない）。この節で逐語に当てたのは P2・P3 の 7 本と Apache-2.0 だけ。
3. **残余の広い読みが 2 つある**（bb）: BlueOak の *"with this software"* を「ソフトウェアを用いて作ったものについても」と読む余地、CERN-OHL の *"exercising rights under the Covered Source"* に「Products を使う権利の行使」が含まれるかの読み。
   どちらの読みを取っても、**条件と終了は残る**ので、3 つ同時の主張は崩れない。崩れるのは「範囲だけで比べたときの差」である。
4. **gap を示すことは、必要を示すことではない** —— Kuhn 氏の vanity の判定は *"widespread need"* と *"wholly unserved"* の連言で（#255）、この節が示すのは後者の 1 件だけである。
5. **この広さは費用でもある** —— #16（特許を持つ組織は受け入れにくい）・#276（帰属ゼロ + 特許許諾は「特許の放棄に等しい」と言われた）・register B7。
6. **「組み合わせとして唯一」は、リストが既に退けた形の主張である** —— Josh Berkus 氏は 2026-10-14 に 0BSD-P へ *"It's not the goal of the OSI to have licenses for every possible combination of conditions"* と述べ、続けて *"do you have a specific use"* と問うた（#276・ACD を名指してはいない）。
   この節が示すのは 2 つの性質の組み合わせなので、この文はそのまま当たる。**言えるのは、組み合わせが条件の足し引きではなく 1 つの効果を生むこと**（学習に使った人が、条件も終了も無く、モデルと出力まで特許で守られる）**まで**で、具体的な用途は 4. と同じく我々には答えられない。

### 独立の再検証（2026-11-04 後半・オーナーが渡した別の AI の見解を材料に、3 人が判断して行った）

**① 母集団は再現できるが、141 本は OSI のリストそのものではなかった。** `--fetch` を取り直すと分類は同じ（141 本・明示 65・S1 58 / S2 3 / S3 4）で、census の差は取得時刻の 1 行だけだった（`--check` はこの 1 行で DRIFT を返す）。一方 **OSI の一次リスト（`/licenses` の 126 頁・`/api/licenses`・取得 2026-10-29）と突き合わせると、census に無いテキストが 8 本ある**: SPDX が OSI 承認と標示しない MIT-CMU / NIST-Software / eCos-2.0 / GPL-1.0、deprecated の wxWindows、SPDX ID の無い Jabber / MITRE CVW / Los Alamos BSD-3 Variant。**8 本とも当たった**（SPDX 原文 5 本・OSI の頁 3 本）: MIT-CMU / NIST-Software / eCos-2.0 / GPL-1.0 / wxWindows / Los Alamos は *patent* の語が無く、Jabber と CVW は作品に限る特許許諾に条件と終了を持つ。**結論は変わらない** —— 「141 本」は「SPDX の標示で 141 本 + OSI の頁だけに在る 8 本」と読む。逆に 141 本のうち 30 本（`-only` / `-or-later` の別名など）は OSI の頁に 1 対 1 で無い。**`/api/licenses` の `approved` は BlueOak-1.0.0 でも false で、承認の判定に使えない**（126 件中 true は 7 件）。

**② 法的効果 —— 末文に 2 つの読みがある（2026-11-04 に bb が見つけ、25 が条文側で検討中）。** *"it does not license a claim that would be infringed by a model … produced without any use of the Work"* は、請求項単位に読むと、モデルの構造や性質を読む請求項の大半を外す（Work を使わないモデルでも侵害されるから）。場面単位に読むと、同じ請求項でも Work から作った M には許諾される。**前者なら「モデルの販売に届く」は学習の方法の請求項と product-by-process に縮む。** §15.1 は後者へ解決するが、gap の柱を解釈規則に預けている。
**1.4 草案での扱いは 25 が試作中**（`ACD-1.4-CLARITY-TRIAL.md`・試作 T4）。場面の分類と反例は試作の側に置き、採否が決まったらこの節の場面を直す。
**しかも我々の想定問答は前者の側で答えている** —— `ACD-1.0.review-responses-clauses.md` は *"An identical model obtainable without the Work at all"* を *"Under 1.1 the claim does not depend on the Work, so it is outside"* とし、同じ問答の 1 件目は *"A model trained on the Work, then run for inference. Covered."* と限定なしで述べる。請求項単位なら、普通の製品請求項は Work を外しても侵害されるので 1 件目はほとんど当たらず、§8.4 が取り除くと述べる露出（*"restore the exposure this Section exists to remove"*）が残る。
**同じ文の前半と後半も割れる**: Work が技法 X を教え、Work を外すと M が X を持たない請求項 K は、前半の *"depends upon the use of the Work"* には当たる（5a）が、X を別の経路で持つモデルが在りうるので後半の請求項単位の読みでは外れる。

**②′ 「無条件」の実益も読みに依存する（5a）。** 条件の多くは頒布のときに発動する。Work を配らず学習してモデルを売るだけの受領者には BlueOak の条件は発動せず、BlueOak に特許の報復条項も無い。**その受領者について BlueOak と ACD の差は *"with this software"* の範囲の読みだけになる。** 上の場面は (2) を置くことで条件を発動させている。CERN-OHL-P には §6.2 と、モデルが Product なら §4 が残る。

**③ 既存ライセンスの組み合わせで同じ効果が出るか —— 出ない。ただしライセンスの外では出る。**

| 組み合わせ | 結果 |
|---|---|
| 0BSD **または** BlueOak / UPL / CERN-OHL-P（選択）| 特許が要る受領者は特許のある側を選ぶので、その条件と終了が付く |
| 0BSD **かつ** 同じ 3 本（両方を同時に許諾）| 著作権は 0BSD で無条件になるが、特許はその本の許諾なので**特許の面の条件と終了は残る** |
| 承認済み本文の改変（Apache-2.0 §3 の報復を外す など）| 改変した本文は承認済みではない。新規の提出である |
| 0BSD + 別の無条件の特許の誓約（Landley 氏・#276 (e)）| **効果は出せる。** 誓約は既存ライセンスではなく、案件ごとの未審査の文である。**gap は「効果が不可能」ではなく「審査済みの 1 本の本文に無い」である** |

**④ 特許の射程は必要か。** OSD は特許許諾を要求していないので、§8.4 を自由の保障に必要とは言えない（#236）。言えるのは、Apache-2.0 の許諾が *"the Work"* に閉じ、Work でない生成物は外れることまでである。**「不要な適用範囲の拡張」と評価されうるかの答えは Yes で、判断は OSI に残る**（25）。Perens 氏は OSD が権利の種類を区別しないと述べるが（#244）、**そこからモデル・出力へ広げる必要までは導けない**。これは「ソフトウェアの自由に必要」ではなく、ACD の目的（学習した受領者を露出させない）に必要な射程である。

**⑤ B15 との構造的衝突 —— 残っている。** A1′+ は 1.4 が足した信号を戻したが、§8.4 は *model, parameter set, weight, embedding, output* を名指す。**B10 で固有の効果として立てるものと、B15 で「ソフトウェアに結びつくか」を問われるものは同じ語である。** Work がソフトウェアのときは、§8.4 はソフトウェアの受領者への特許許諾の延長と説明できる。Work がデータのときはその説明が効かない。**ただし §8.4 + §8.2 の組み合わせは Work がソフトウェアでも成り立つので、§1.3 の列挙を狭めてもこの 1 件は折れない**（5a・「列挙を狭めると B10 を折る」は全ての脚には当たらない）。**判定: 条文の矛盾ではないが、未解消の緊張である。B10 を強く言うほど B15 に触れる。解くのは OSI である。**

**⑥ 基準 7 を満たすか —— 我々は確定させない。** 原文（`/licenses/review-process`・2026-11-04 取得・最終更新 2024-03-13）は *"The license must fill a gap that currently existing licenses do not fill."* で、何を gap と数えるかの定めは無い。

**3 つに分けた結論**:

| 種類 | 内容 |
|---|---|
| **条文比較で成立する差** | 明示の特許許諾を持ち受領者に条件を課さない本文は、OSI の頁の全テキストに 0 本（明示 65 本すべてに義務の文が在る・5a が 1 本ずつ読んだ）/ モデル・パラメータ・重み・埋め込み・出力を名指す特許許諾は 0 本 / 特許訴訟でも終了しないと明記し、かつ無条件の本文は 0 本 |
| **法的効果の解釈に依存する差** | §8.4 がモデルの販売に届く範囲（末文の 2 読み）/ CERN-OHL-P の Products と「必然的に」の読み / BlueOak の *"with this software"* と、学習だけの受領者への実益 / 黙示の許諾の範囲 / 一方的な文書による無条件の許諾の有効性（register B1）|
| **OSI の判断に依存する必要性** | 組み合わせが gap に足りるか（Berkus 氏 #276）/ 具体的な用途（Kuhn 氏 #255）/ 主題（B15）/ 重複かつ未使用の留め置き（#139）|

### OSI の基準との対応

- **新規ライセンスの基準 7（既存のライセンスで埋まらない gap を埋める・`ACD-1.0.review-rules.md` §1.70）**: この節がその 1 件の効果を原文で示す。**基準を満たすかは OSI の判断**で、我々が言えるのは「示せる形にした」ことまで。
- **提出要件「最も近い承認済みライセンスとの比較」**: 範囲で最も近いのは CERN-OHL-P-2.0、条件の少なさで最も近いのは BlueOak-1.0.0 で、差は上の 2 表のとおり。
- **#269（gap は存在理由であると同時に、果たしているかを測られる基準）**: §8.4 は 1.1 で因果の限定が足されたので、**測られる対象は 1.0 と 1.1 以降で別である**（2026-11-04 訂正: 旧文は「1.0 から 1.4 草案まで作用を変えていない」で誤りだった・5a の指摘）。

### Before / After

| | Before（2026-11-03 の再検証）| After（2026-11-04）|
|---|---|---|
| §8.4 | 「新しい —— 名指し + 内容限定の除去」を、最近傍 10 本を読んで述べた | **141 本の分割で閉じ、7 本は逐語で当てた**。主張の形は「3 つ同時」へ。**同日後半**: OSI の頁だけに在る 8 本を足しても 0 本のまま。ただし末文の 2 読みが見つかり、モデルへの届き方は「解釈に依存する差」へ移した |
| §7 データベース権 | 「新しい —— 承認済みの許諾は copyright と patent に限られる」 | **作用としては反証できない**（MIT *"to deal in the Software without restriction"*・0BSD *"Permission to use, copy, modify, and/or distribute this software for any purpose"* は許可を著作権に限らない・bb の H2）。**明示としては新しい**（REVIEWERS「In one screen」(i) は *"expressly reaches"* の形で、真のまま）|
| §6.2 / §6.3 / §5.2(b) | 「新しい」| **限定つき** —— 受領者が例外に依る場面か、許諾が無効とされた場面でだけ効く（bb の H3）|
| §12 | 「EUPL に先例」| 同じ（bb の H4）|
