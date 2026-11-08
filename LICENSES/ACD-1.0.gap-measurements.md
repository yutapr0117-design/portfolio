---
file: LICENSES/ACD-1.0.gap-measurements.md
audience: OSI license-review participants / licence reviewers / 監査人 / 後任 AI
last-updated: 2026-11-07
canonical-ref: LICENSES/ACD-1.0.comparison.md (切り出し元・条項比較) / LICENSES/ACD-1.0.gap-census.md (同じ 141 本への 3 gap の全数表)
---

# gap の主張を既存ライセンスの本文に当てた測定（§1.96 / §1.97 / §1.104 / §1.129 / §1.130 / §1.133 / §1.134 / §1.135 / §1.136）

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

**ACD は、Work の計算的利用（学習）と、そこから生じたモデル・出力を作り・使い・売り・輸入する行為について、Dedicator の特許請求項を（1.4 草案では、侵害する特徴が Work の内容から生じるものに限って）、
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
D は 3 つの請求項を持つ。C1 は R が選んだ学習の手法の請求項で、Work はその手法を教えない。C2 は M の構造についての請求項で、Work と関係が無い。C3 は Work が教える方法の請求項で、M の出力がそれを実施する。

| 文書 | R は許諾を持つか |
|---|---|
| ACD-1.0 | C1・C2・C3 とも**持つ**（1.0 に因果の限定は無い）。(2)(3) は許諾を終わらせない（§8.2・§10.1・§10.4）|
| ACD-1.1〜1.3 | **読みで分かれる** —— 限定を請求項の単位で読めば 3 つとも外、場面の単位で読めば 3 つとも内（`ACD-1.1-SELF-AUDIT.md` §3t）。(2)(3) は許諾を終わらせない |
| ACD-1.4 草案 | **C3 は持つ。C1・C2 は持たない**（侵害する特徴が Work の内容から生じない）。(2)(3) は許諾を終わらせない |
| CERN-OHL-P-2.0 | C3 が *"necessarily infringed by exercising rights under the Covered Source"* に当たるかは読みに依存する。**当たるとしても** (2) は §4 の条件、(3) は §6.2 の終了に当たる |
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
**1.4 草案は限定を侵害する特徴の単位へ書き直した**（`ACD-1.4-CLARITY-TRIAL.md` §9.5〜§9.7・`ACD-1.1-SELF-AUDIT.md` §3t）。§6.1 の超過も同時に閉じた。**1.1〜1.3 の読みの割れは凍結のまま残る。**
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
| **法的効果の解釈に依存する差** | §8.4 がモデルの販売に届く範囲（1.1〜1.3 の読みの割れ・1.4 では *"results"* と *"teaches or embodies"* の読み）/ CERN-OHL-P の Products と「必然的に」の読み / BlueOak の *"with this software"* と、学習だけの受領者への実益 / 黙示の許諾の範囲 / 一方的な文書による無条件の許諾の有効性（register B1）|
| **OSI の判断に依存する必要性** | 組み合わせが gap に足りるか（Berkus 氏 #276）/ 具体的な用途（Kuhn 氏 #255）/ 主題（B15）/ 重複かつ未使用の留め置き（#139）|

### OSI の基準との対応

- **新規ライセンスの基準 7（既存のライセンスで埋まらない gap を埋める・`ACD-1.0.review-rules.md` §1.70）**: この節がその 1 件の効果を原文で示す。**基準を満たすかは OSI の判断**で、我々が言えるのは「示せる形にした」ことまで。
- **提出要件「最も近い承認済みライセンスとの比較」**: 範囲で最も近いのは CERN-OHL-P-2.0、条件の少なさで最も近いのは BlueOak-1.0.0 で、差は上の 2 表のとおり。
- **#269（gap は存在理由であると同時に、果たしているかを測られる基準）**: §8.4 は 1.1 で因果の限定が足されたので、**測られる対象は 1.0 と 1.1 以降で別である**（2026-11-04 訂正: 旧文は「1.0 から 1.4 草案まで作用を変えていない」で誤りだった・5a の指摘）。

**項目ごとの効果の対照（MIT / 0BSD / CC0・独自性の根拠から除外した項目）と、審査基準 8 条の 1.4 の条番号は §1.134 に在る。**

### Before / After

| | Before（2026-11-03 の再検証）| After（2026-11-04）|
|---|---|---|
| §8.4 | 「新しい —— 名指し + 内容限定の除去」を、最近傍 10 本を読んで述べた | **141 本の分割で閉じ、7 本は逐語で当てた**。主張の形は「3 つ同時」へ。**同日後半**: OSI の頁だけに在る 8 本を足しても 0 本のまま。ただし限定の読みの割れが見つかり、1.4 草案で直した。モデルへの届き方は「Work が教える特徴について」に狭まり、「解釈に依存する差」へ移した |
| §7 データベース権 | 「新しい —— 承認済みの許諾は copyright と patent に限られる」 | **作用としては反証できない**（MIT *"to deal in the Software without restriction"*・0BSD *"Permission to use, copy, modify, and/or distribute this software for any purpose"* は許可を著作権に限らない・bb の H2）。**明示としては新しい**（REVIEWERS「In one screen」(i) は *"expressly reaches"* の形で、真のまま）|
| §6.2 / §6.3 / §5.2(b) | 「新しい」| **限定つき** —— 受領者が例外に依る場面か、許諾が無効とされた場面でだけ効く（bb の H3）|
| §12 | 「EUPL に先例」| 同じ（bb の H4）|

## 1.134 gap の項目ごとに、効果の差が立証できるかを分けた —— MIT / 0BSD / CC0 と審査基準 8 条（2026-11-04）

**きっかけ**: 別の AI の見解をオーナーが渡し、確認のうえ実施するよう依頼があった（課題設定は別の AI のもの）。§1.133 が 1 件の効果を閉じたので、残りの項目を同じ基準で分ける。
**原典**: MIT / 0BSD は §1.133 と同じ取得（SPDX `8791eda`）。CC0 1.0 は `creativecommons.org/publicdomain/zero/1.0/legalcode`（2026-11-04 取得）。§2 の 5 要素は §1.129 を再利用する。CC0 は OSI 承認済みではないので、基準 7 の比較対象ではなく、最も近い形の確認として置く。
**読み方**: 「差」は本文が与える効果の差で、裁判所での実現は別問題である（法的レビューは受けていない・register B1）。法域は本ドシエの一次資料が在るものだけを書いた。

| 項目 | 法域・権利主体・対象行為 | MIT | 0BSD | CC0 1.0 | 判定 |
|---|---|---|---|---|---|
| §6.1 学習の許可 | 全法域・Dedicator の権利・学習のための複製等 | *"to deal in the Software without restriction"* が覆う | *"to use, copy, modify, and/or distribute this software for any purpose"* が覆う | §2 の waiver が覆う | **差なし。独自性の根拠から除外**（明示の価値だけが残る）|
| §6.2 / §6.3 留保をしない | EU（DSM 指令 4 条 3 項）・Dedicator 自身の留保・例外に依る学習 | 沈黙 | 沈黙 | 沈黙 | **限定つきの差**。受領者が例外に依る場面か許諾が無効とされた場面でだけ効く（EXTERNAL の G3）|
| §6.4 モデル・出力を縛らない | 全法域・Dedicator・モデルの頒布 | notice の条件 *"in all copies or substantial portions"* がモデルに及ぶかは未解決 | 条件が無いので差なし | 条件が無いので差なし | **MIT に対してだけ差**（解釈依存）|
| §7 データベース権 | EU（指令 96/9）・Dedicator・抽出と再利用 | 許可は著作権に限らないが名指さない | 同じ | §1 が *"database rights (such as those arising under Directive 96/9/EC"* と *"rights protecting the extraction, dissemination, use and reuse of data in a Work"* を名指す | **効果の差は立証できない。独自性の根拠から除外**（承認済みに対して残るのは名指しだけ・EXTERNAL の G2）|
| §8.4 + §8.2 特許 | 全法域・Dedicator の特許・学習とモデルの製造販売 | 特許の語が無い（黙示の許諾は判例に依存し、モデルの販売へ及ぶ根拠は条文に無い）| 同じ | §4(a) *"No trademark or patent rights held by Affirmer are waived, abandoned, surrendered, licensed or otherwise affected"* が**明示に除く** | **差あり**（§1.133。CC0 に対しては正反対の条文で最も明確）|
| §9 機械生成物 | 全法域・Dedicator・権利の存否が不明な部分 | 権利が在れば許可し、無ければ不要 | 同じ | 同じ | **差なし。独自性の根拠から除外**（§9.2 自身が *"adds nothing"* と述べる）|
| §12 人格権 | 日本（著作権法 59 条）ほか・著作者・人格権の行使 | 沈黙 | 沈黙 | §1 が *"moral rights retained by the original author(s)"* を名指す | **MIT / 0BSD に対して差**（不行使の約束の有効性は解釈依存・承認済みでは EUPL に先例）|

**したがって**: 効果の差として残るのは §8.4 + §8.2、§12、§6.2 / §6.3（限定つき）、§6.4（MIT に対してだけ）である。**§6.1・§7・§9 は独自性の根拠にしない。**
**⚠ 提出面への波及**: `REVIEWERS.md` の "The gap it claims, in one sentence" は §7 を 3 つの脚の先頭に置く。*"expressly reaches"* の形なので偽ではないが、先頭の脚は効果の差を立証できない項目である。文の順序と重みは 25 の判断に渡した。**2026-11-06 追記**: 波及先はこの 1 文だけではなかった。申請日に使う `SUBMISSION-MATERIALS.md` の gap の行は §6 / §8.4 / §9 を 3 点と書いたままで、`REVIEWERS.md` の *"The same gap, in detail"* も同じだった（どちらも同日に直した）。1.0 の提出パケット `submission.md` §B.0 と想定問答 `review-responses.md` の同じ 3 点は、1.0 の記録として残す（申請の日に使わない・`SUBMISSION-MATERIALS.md` 冒頭）。

### 審査基準 8 条と 1.4 の条

基準の逐語は §1.70（`review-rules.md`）。2026-11-04 に公式ページを取り直し、8 条の文言と *"Last modified on March 13, 2024"* が変わっていないことを確かめた。§1.70 の表の条番号は 1.0 のものなので、ここに 1.4 の番号を置く。

| # | 1.4 の条 | 状態 |
|---|---|---|
| 1 再利用できる | §16.1（notice の 1 欄だけ）・§16.3 | 前半は測定済み。後半（licensor ごとに結果が変わらない）は §12 が法域で変わるので OSI 判断 |
| 2 licensor を優位に置かない | §5.1・§8.6・§10.1。残るのは §11.1 の商標と §13 / §14 の免責 | OSI 判断（#265 の 3 つの逆側）|
| 3 曖昧さが重大な効果を持たない | §15.1 | **この日に実例が出た** —— §8.4 の末文の読みの分岐は効果を左右したので、25 が 1.4 で限定を 1 本に直す（`ACD-1.4-CLARITY-TRIAL.md` §9.5・§9.6）|
| 4 文法・構文が明晰 | 全文 | 測定: 1.4 草案 182 文・平均 27.8 語・最長 81 語（`measure_clause_clarity.py`・2026-11-07）。判断は OSI |
| 5 どの適用も OSD を満たす | §10.1 | 適用者に選択肢が無い |
| 6 提出時に遵守できる | §10.1 | 義務が無いので自明 |
| 7 gap を埋める | §8.4 + §8.2（§1.133）・上の表 | **足りるかは OSI の判断** |
| 8 完全なテキスト | 全文 | 外部参照なし（`measure_section4c.py`）|

### 反例の探索と残り

- **既存ライセンスで同等の効果が成立するか**: §6.1・§7・§9 は成立するので除外した。§8.4 + §8.2 は 141 本で不成立（`measure_patent_reach.py --express`）。ただし学習だけで Work を配らない受領者には、BlueOak の条件は発動しない（§1.133）。
- **B15**: 新しい証拠は無い。**未解消**で、判断は OSI に残る。訂正を 1 件した —— 「*audiovisual material* を落とすと gap の対象が定義から外れる」は誤りで、列挙は例示（§15.5）なので範囲は変わらない（`ACD-1.4-CLARITY-TRIAL.md` の A1）。範囲が縮むのはソフトウェアに限る案（A2）だけで、そのときも §8.4 + §8.2 の組み合わせはソフトウェアの Work について残る。A1 を採らない理由（疑義を見えにくくするだけ）は変わらない。

### Before / After

| 障害 | Before | After | 減ったか |
|---|---|---|---|
| B10 | 3 つの脚を同じ重さで述べていた | 効果の差が立証できない 3 項目を根拠から外し、残る項目を分けた | **主張の誤りは減った。gap が足りるかの判断は動いていない** |
| 基準 3 | §8.4 に効果を左右する読みの分岐 | 1.4 で限定を 1 本へ | **減った**（1.4 を出す場合）|
| B15 | 判断は OSI | 同じ（訂正 1 件のみ）| **未解消** |
| B1 / B3 / B13 / B14 | — | この節では動かしていない | **未解消** |

## 1.135 特許の 4 類型を、ACD と BlueOak・CERN-OHL-P・UPL の原文で当てた —— 差が立つのは学習のあとの行為である（2026-11-06）

**きっかけ**: オーナーが共有した別の AI の見解（オーナーの指示ではない）が、§1.133 の組み合わせを具体的な行為と請求項で当て直すことを挙げた。§1.133 は 1 つの場面で比べていて、行為の類型ごとには分けていなかった。原文は SPDX `license-list-data` の main から 2026-11-06 に取り直した（sha256 の先頭: BlueOak-1.0.0 `8a1af140fdfb` / CERN-OHL-P-2.0 `eeecc593866f` / UPL-1.0 `2f81e75033a0`）。法律家の読みではない。

**場面**: D は特許を持ち、R は D の著作物を使う。請求項を 4 つ置く。P1 は R が選んだ学習の手法、P2 は著作物が教える方法、P3 はモデルの構造で著作物と関係が無い、P4 はモデルが著作物から学んだ性質である。

| 類型 | 請求項 | ACD 1.4 草案 | BlueOak-1.0.0 | CERN-OHL-P-2.0 | UPL-1.0 |
|---|---|---|---|---|---|
| A 学習の実行 | P2 | 及ぶ | 及ぶ | 及ぶ読みが立つ | 請求項がソフトウェアを覆うなら及ぶ |
| A 学習の実行 | P1 | **及ばない** | **及ぶ**（そのソフトウェアで行う学習なら）| 及ばない（*"necessarily"*）| 及ばない |
| B モデルの製造 | P4 | 及ぶ（示すのは R）| 読みが分かれる | 読みが分かれる | 及ばない |
| B モデルの製造 | P3 | 及ばない | 読みが分かれる | 及ばない | 及ばない |
| C モデルの販売 | P4 | **及ぶ** | 素直には及ばない | モデルが Product なら読みが立つ | 採用者が `lrgrwrks.txt` に書いたモデルなら及ぶ。これから生じるモデル一般は及ばない|
| C モデルの販売 | P3 | 及ばない | 及ばない | 及ばない | 及ばない |
| D 出力の利用 | P2 | **及ぶ** | 素直には及ばない | 出力が Product なら読みが立つ | 及ばない |
| 対象外 | 著作物を使わないモデル | 及ばない | 及ばない | 及ばない | 及ばない |

**条件と終了（原文）**: BlueOak は *"You must ensure that everyone who gets a copy of any part of this software from you"* が通知の条件で、終了はその不履行だけである（*"your license ends immediately"*・30 日の猶予）。特許訴訟による終了は無い。CERN-OHL-P は §4 の通知、§6.1 の *"or where terminated by the Licensor for cause"*、§6.2 の特許訴訟による終了を持つ。UPL は通知の条件を持ち、終了の文は無い。ACD は §8.2 と §10.1 によりどれも持たない。

**分かったこと**:

1. **類型 A では ACD に差が無く、請求項の範囲は BlueOak の方が広い場面がある。** BlueOak の許諾は *"any patent claims they can license or become able to license"* で因果の限定が無い。R が複製を配らず学習するだけなら通知の条件も発火しない。1.4 草案の ACD は P1 に及ばない。**§1.133 の組み合わせは「作品を超える対象」で立つので結論は変わらないが、学習の実行そのものを差として言ってはならない。**
2. **効果の差が立つのは類型 C と D である。** モデルの販売と出力の利用について、許諾が届く読みを持つのは ACD と CERN-OHL-P で、CERN-OHL-P は §4 の条件と §6.2 の終了を持つ。
3. **買い手の位置**: ACD の買い手は §1.6 の You として §8.4 の *using* の許諾を直接受ける。R からの再許諾を要しない。CERN-OHL-P も §2.2 で Licensor から直接許諾されるが、同じ条件が付く。
4. **別個の誓約は 4 類型すべてで同じ効果を出せる**（0BSD + 無条件の特許の不行使の誓約・§1.133 の ⑥・`against.md` #276 (e)）。差は審査済みの 1 本の本文かどうかで、効果の差ではない。

**分類**: この節は**説明の改善**である。主張を類型 C / D へ絞り、法的効果は変えていない。同じ検証で出た本文の分岐（§5.1 の第 2 肢・§8.4 の方法の請求項・§8.6 の *described*）は**効果の改善**の候補で、`ACD-1.4-SECOND-CLARITY-TRIAL.md` §13 に置く。

**確立しないこと**: 表の「読みが立つ」「及ぶ」は本文の語の読みで、裁判所の判断ではない。モデルや重みが特許法上の物に当たるか、販売や輸入の行為がどう扱われるかは法域の問いで、法的レビューは受けていない（B1）。Source がデータを含むかは CERN-OHL の定義の読みである。

## 1.136 B7 の費用を主体ごとに数え、B10 を弱める最強の反論を立てる（2026-11-06）

**きっかけ**: 別の AI の見解をオーナーが渡した（課題設定は別の AI のもの・検証は現物に当てて行った）。行為の類型ごとの条文の当て直しは 25 が持ち、この節は誰が何を失うかと、gap への最強の反論を持つ。条番号は 1.4 草案のもの。

### 誰が何を失うか

| 主体 | 起きること | 条 | 既存ライセンスとの差 |
|---|---|---|---|
| 特許権者が、方法を説明する文書へ適用する | Work が教える方法は、学習を経由した者に許諾される。小さなモデルで足りる（`faq.md` A32）| §8.4 *"a feature that the Work teaches or embodies is taken so to result"* | Apache-2.0 §3 は *"necessarily infringed by their Contribution(s) alone or by combination"* で、文書の読者がその方法を実施しても許諾の外である。**費用として最大** |
| 貢献者（2026-11-06 に足した）| 別段の意思表示なしの貢献で Dedicator になり、その貢献が教える特徴に §8.4 が及ぶ。会社の特許に及ぶのは、貢献が本人または本人のために行われたときである（§1.9）| §2.6・§1.4・§8.4 | Apache-2.0 §5 も既定は同じ（*"Unless You explicitly state otherwise"*）だが、特許の範囲は §3 の必然の侵害に閉じる。**register B7 の「費用を負うのは採用者だけ」は貢献者を落としていた** |
| 将来の特許 | Dedicator が後で持つ請求項も及ぶ | §8.1・§8.4 *"now or in future"* | GPL-3.0 §11 が同じ広さを持つ（*"whether already acquired or hereafter acquired"*）。この点だけなら先例がある |
| 提訴された Dedicator | 相手の許諾を止められない。競合は Work を使ったまま Dedicator を訴えられる（#174）| §8.2 | Apache-2.0 §3 と GPL-3.0 §10 は止められる。**§10.1 と両立しないので直せない** |
| 改良の請求項 | 請求項が A（Work が教える）+ B（受領者の独自）のとき、1.4 の §8.4 の「全部または一部」の語により及ぶ。設計どおりである（`ACD-1.4-CLARITY-TRIAL.md` §9.6・25）| §8.4 | Apache-2.0 §3 の *"by combination"* は寄与と Work の組み合わせに閉じる |
| 少量の混入 | Work を学習データの一部に入れるだけで、学習で獲得した特徴について、1.4 の §8.4 の「全部または一部」と閾値なしの文を主張する読みが残る。*content* へ変えても消えない。逆に「一部」を外すと、2 つのデータが各々十分な原因である場面で受領者が外れるので、文は動かさず費用として書く（E15・`ACD-1.4-ADVERSARIAL-TRIAGE.md` E-01・5a）| §8.4 | 閾値を置く承認済みの例は census に無い |
| 吸収される小さな Dedicator | 特許を多く持つ会社へ吸収されると、後継者の請求項に及ぶ読みが立つ（25）| §2.8・§8.1 *"now or in future"* | GPL-3.0 §11 は contributor の範囲で同じ広さを持つ |

**費用を負わない者**: 特許を持たない適用者。Work の使用と関係の無い特徴を持つ請求項（1.4 の §8.4 の限定・`ACD-1.4-CLARITY-TRIAL.md` §9.5 の K3〜K6）。第三者の特許（§8.5）。

### B10 を弱める最強の反論

**R1 受益者がほとんど居ない（2026-11-06 に立てた・これが最も重い）。** 特許を持つ者は §8 を嫌って採らず（#107）、特許を持たない者には §8 が中身を持たない。すると gap の効果が実際に働く主体がほとんど居ない。このリポジトリも、Dedicator が関連する特許を持つと確かめられていないので、§8.4 が働いた実例は 1 件も無い。**効果の差は条文の上の差で、実使用の差ではない。**

**R1 への答えは部分的である。** (a) 複数の貢献者を持つプロジェクトでは、貢献者が Dedicator になる（§2.6）。特許を持つ会社の従業員が会社のために貢献すれば、受領者はその会社の特許について §8 を持つ。0BSD にこれは無い。**ただし同じ事実が上の表の費用でもあり、会社は従業員の貢献を止めるかもしれない。** (b) 許諾は将来の請求項に及ぶので、いま特許を持たない適用者の効果が 0 とは限らない。(c) 需要の記述は記録に在る。Morrison 氏は 2017-10-26 に、連邦機関が *"something close to public domain yet still addressing indemnification and contributor patent grants"* を探し、CC0 や新しいライセンスへ分かれていると述べた（`rounds/2017-10-26-license-discuss-morrison-federal-need-observed.txt`）。著作権が生じない著作物に権利を主張しない形（§9.2・#258）は、この層の問いに近い。**ただし 9 年前の 1 人の発言で、いまも在るかは確かめておらず、採用ではない。** **どの答えにも実例は無い。**

**⚠ 同じ検索の逆側**: Nigel Tzeng 氏は 2018-10-16 に、CC が特許許諾を足さなかった理由を、既存の CC0 の利用者が望まなかったからだと述べた（`license-review` の 0BSD 改名スレッド）。gap が埋まらないまま残っている説明であると同時に、需要が無いという読みの材料でもある。

**R2 別個の特許の誓約で同じ効果が出る。** 0BSD に無条件の誓約を添えれば効果は出せる（Landley 氏・#276 (e)・EXTERNAL の H1-f）。**答えは「不可能」ではなく、案件ごとの未審査の文になり、Work と一緒に移らないことである。** 効果の不可能性を主張しない。

**R3 OSD は特許許諾を求めていない**（#236）。gap は OSD の要件ではなく基準 7 の話で、**足りるかは OSI が決める。**

**R4 CERN-OHL-P との差は通知 1 種と終了である。** 請求項の範囲の差は主張しない（§1.133）。差が小さいと読まれれば、Berkus 氏の *"It's not the goal of the OSI to have licenses for every possible combination of conditions"* に当たる。

**R5 類型によっては差が消える（5a の原文の読み）。** 学習の実行だけなら、BlueOak-1.0.0 の *"do everything with this software"* に因果の限定は無く、再頒布しない受領者に条件は発動しない。**この類型では BlueOak は 1.4 の §8.4 より広い可能性がある。** 差が立つのはモデルを売る場面である。CERN-OHL-P の Product は機器を含むので、モデルを組み込んだ機器については ACD より広い。

**R6 UPL の採用者は lrgrwrks.txt にモデルを書ける（5a）。** 承認済みの本文のままモデルへ届かせる構成が考えられる。*"listed"* と *"to which the Software is contributed"* が、学習で後から生じるモデルに当たるかは読みである。当たるとしても UPL の条件は残る。

**別個の誓約の記録（R2 への補足・5a）**: 承認の審査に掛かった別個の誓約の実例はアーカイブに見つからなかった。Duan 氏（2025-05-15）は別個の promise について *"may not be effective/enforceable (especially if the Licensor transfers or sells the patent to someone else)"* と述べたが、§8.6 にも同じ問いが返る。

### この節が変えたもの

**この節は費用と反論の正確な記録で、それ自体は説明の改善である。** 承認の見込みの根拠に数えない。**同じ検証から本文の効果が変わったのは別にある** —— §5.1 と §8.3 が §8.4 の限定を素通りする読みを 1.4 草案が閉じた（`ACD-1.1-SELF-AUDIT.md` §3x）。上の表の費用は、その修正のあとの射程で読む。

## 1.137 承認された新規の許容型は、隣との差が 1 点だった。それだけでは足りないことも記録に在る（2026-11-07）

**問い**: gap が狭いことは、それ自体で問題か（B10）。承認された許容型の差の大きさを、提出と理由書で測った。

| ライセンス | 承認 | 隣との差 | 記録された理由 |
|---|---|---|---|
| 0BSD（当時 Free Public License）| 2015 | ISC から notice の条件を除く | 議事録 *"basically the ISC License"*。*"is it really going to be used?"* と問われて承認 |
| BSD-2-Clause-Patent | 2017 | BSD-2-Clause に明示の特許許諾を足す | McCoy Smith 氏の提出（2016-01）*"a specific problem that has been encountered with existing licenses"*。GPLv2 と両立する許容型で明示の特許許諾を持つものを、組織が望んでいた |
| MIT-0 | 2020 | MIT から帰属を除く | 理由書 *"the same language as the MIT License except that the attribution requirement of the MIT License in its second paragraph is removed"* |
| OSC License v1 | 2025 | MIT にドイツ法で有効な責任制限を足す | 提出 *"does not contain a limitation of liability that is effective under German law"* |

**4 本とも差は 1 点である。** ACD の効果の差も 1 点と言える。0BSD から見れば、条件が無いことは既に持っている性質で、
足すのは作品を超える特許許諾だけである（§8.2 はその許諾に同じ性質を保つ文）。BlueOak や CERN-OHL-P から見れば、差は条件と終了の有無である。
差が狭いこと自体が承認を止めた記録は、この 4 本には無い。
**ただし効果の差は 1 点でも、本文の差は 1 点ではない。** 4 本は既存の本文の小さな派生で、ACD はその 1 点のために 5,400 語の新しい本文を持つ（B3）。

**逆側を同じ重さで書く。**

- **4 本は既存テキストの派生である。** 審査の費用が小さい。ACD は新規の長いテキストなので、差に見合うかの問いが重い（`board-decisions.md` §8.3 の *"the benefits aren't worth the cost"*）。
- **差が 1 点でも保留された例が在る。** Tiwaz は MPL-2.0 の近い変種で、*"no demonstrated uses or planned uses"* として保留された（`board-decisions.md` §2c）。BSD-2-Clause-Patent と OSC は具体的な需要を述べていた。0BSD と MIT-0 は使用を問われて通った。
- **ACD の組み合わせそのものが、リストで退けられている。** 0BSD-P への Berkus 氏の問いは具体的な用途で（#276）、提出者は答えられずに取り下げた。ACD が述べられる用途は 1 つである。
- **過去の承認は OSI を拘束しない。**

## 1.139 CC0 の特許の除外は、配布の判断を実際に変えた —— Fedora（2022）。代わりに勧められたのは特許に触れないライセンスだった（2026-11-07）

**Fedora は 2022 年に、CC0 をコードに使えない扱いへ変えた。** 原文の置き場は `rounds/2022-07-fedora-legal-cc0-classification-observed.txt`。リストの最初の 1 通は取得できず（bot の確認と 401）、その語は LWN と BleepingComputer の引用である。

Richard Fontana 氏（当時 Red Hat）の告知は、LWN の引用で *"Over a long period of time a consensus has been building in FOSS that licenses that preclude any form of patent licensing or patent forbearance cannot be considered FOSS."*。理由として CC0 の clause 4(a) を挙げている。BleepingComputer の引用では *"We plan to classify CC0 as allowed-content only, so that CC0 would no longer be allowed for code"*。

Fedora の文書は基準をこう書いている（`license-approval.adoc`）。コードに使える *allowed* の基準に対し、内容物の基準は *"The license may say that it does not cover patents or grant any patent licenses"* を例外として認める。つまりコードのライセンスは、特許を含まないと言ってはならない。CC0 については *"`CC0-1.0`, which has a clause that says that it does not license or otherwise "affect" patent rights, is no longer _allowed_, but it continues to be _allowed-content_."*

Fedora のいまのデータ（`fedora-licenses.json`・2026-11-07 取得）は次のとおりで、2022 年の扱いは続いている。

| 表現 | status |
|---|---|
| `CC0-1.0` | `allowed-content`。2022-08-01 より前の既存の利用は残し、*"We encourage Fedora package maintainers to ask upstreams to relicense such files."* |
| `Unlicense` / `CC-PDDC` / `WTFPL` / `LicenseRef-Fedora-Public-Domain` | `allowed` |
| `MIT-0` / `0BSD` / `BSD-2-Clause-Patent` / `UPL-1.0` / `BlueOak-1.0.0` | `allowed` |

**ここから言えること。** 公有化の形そのものはコードから外されていない。外れたのは特許を除外した 1 本である。§1.138 の審査の記録と同じ向きで、ACD の §8 は除外の逆にあたる。

**逆側（`against.md` #290）。** 代わりを問われた Fontana 氏の答えは *"These days in similar situations (Involving code, at least) I have typically been recommending MIT No Attribution (SPDX: MIT-0)"*（2022-07-23）で、MIT-0 は特許について何も書いていない。基準の語は *"preclude"* で、明示の許諾を求めていない。Fedora では、CC0 が空けた穴は承認済みのライセンスで埋まった。これは #84（もう 1 本要るのか）の、実務の側からの答えである。ACD が足すのは沈黙ではなく明示の許諾で、それが要るかは #236 / #238 の争点のままである。

**§8.4 についての逆側。** 同じ文書は内容物の例に *"checkpoints or comparable machine learning model files containing trained parameters"* を挙げる。学習済みパラメータのファイルでは、Fedora はライセンスが特許を含まないと言うことを認めている。§8.4 が届く先について、この基準は特許の許諾を求めていない。

**この節が establish しないこと。** Fedora の判断は OSI の決定ではない。Fedora の一覧に ACD は無く、載せる経路はいま使えない（`OSI-APPROVAL-PLAN.md` §3.6）。

## 1.143 CC0 の特許の除外は 2011 年から問題にされていた。許容型に特許を足した前例は特許の弁護士が書き、審査はその点を問うた（2026-11-08）

未読の候補から 2 本のスレッドを読んだ（`rounds/2011-to-2017-license-lists-cc0-patents-and-bsd-patent-cited-observed-*.txt`）。どちらもドシエに記録が無かった。

### 2011-04「waive all rights」のライセンスを OSI に（`license-discuss`・17 通）

Wikimedia の管理者 Derrick Coetzee 氏が、帰属を求めないライセンスを求めた。出所を問わず断片のコードを使う流れに合わせるためで、特許については *"I think it makes sense to waive any relevant patent rights explicitly and separately"* と書き、*"it'd be nice to have a web page somewhere with somebody officially saying"* ソフトウェアに使ってよいと、と結んだ。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"OSI could analyze CC0 for its license fallback terms, but not as a public domain dedication."* | Lawrence Rosen 氏 2011-04-18 | 審査されるのは許諾の部分である。§4 は §3 から独立した許諾で（§4.4）、審査の対象になる形をしている |
| *"The CC0 license says nothing about patents. I find this particularly troubling when a CC0 license (or the BSD license, for that matter!) is used for software or specifications by companies that have large patent portfolios. What are you withholding?"*、*"we ask for licenses for things we can just take, and ignore the important stuff (e.g., patents) we really need licenses for."* | 同 | §8 の理由と同じ向きで、2012 年の否決の理由（clause 4(a)）より 10 か月早い |
| *"I have recently suggested to Creative Commons that the issue should perhaps be revisited in future versions of CC0, now that its suitability for software has been acknowledged."*、*"use of CC0 on a substantial body of code might be another matter."* | Richard Fontana 氏 2011-04-18（当時 Red Hat）| CC0 の後継で特許を扱うことを CC に提案していた。CC0 はいまも 1.0 で、OSI の FAQ（2025）は clause 4(a) を懸念として挙げ続けている |
| *"For "waive all rights", CC0 is the best thing I can think of. It's not really a license, of course"* | Karl Fogel 氏 2011-04-18 | 翌年の *"Those sorts of promises are what the OSI evaluates and sometimes approves."*（`REVIEWERS.md`）の前の段階 |
| Intel の Sample Source Code License は *"grants rights equivalent to a permissive license (including patents) without requiring a notice or disclaimer"* | Andrew Wilson 氏（Intel）2011-04-18 | 通知を求めず特許を含める許諾を、企業は OSI の外で既に使っていた。OSI の承認は受けていない |

**逆側。** Rosen 氏は同じ日に *"Be very careful to include attribution and other conditions. It is only because a FOSS license imposes conditions that it may be enforceable by the parties. See /Jacobsen v. Katzer/."* とも述べた（#307）。ACD は条件を課さないので、ライセンサーが条件違反を訴える道も無い。ACD の答えは、守らせる義務がそもそも無いことと、理事会が 2015 年に条件の無いライセンスを 8 対 0 で承認したことである（0BSD・`board-decisions.md` §8.6）。

### 2016-01〜2017-03 BSD + Patent（`license-review`・95 通・2017 承認）

許容型に明示の特許許諾を足したライセンスで、いまの BSD-2-Clause-Patent である。提出者の McCoy Smith 氏は *"So, for what it's worth, I'm a patent lawyer"* と述べた。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"it's not as simple as including a patent grant. I'd really like to see a real patent attorney work on this question."*、*"is the patent grant language of the license correct and successful in granting a patent license on any concepts embodied in the code released, and only on those?"* | Josh Berkus 氏 2016-01-14、01-19 | 特許の許諾の語を特許の弁護士に見てほしいと求めた（#308）。範囲は作品に具わる概念に *"only on those"* かが問われた。§8.4 はそれを越える（#305）|
| *"This is not an objection, the retaliation is obviously not something that would increase the compliance with OSD"* | Carlo Piana 氏 2016-01-14 | §8.2 が報復条項を持たないことは、OSD の問いにならない |
| *"since it's not copyleft (at this stage of my analysis), I believe there is little proliferation damage compared to benefit."* | 同 2016-01-21 | §4.5 と同じ向き（B10）|
| *"adding incremental complexity to a very simple license, that may be more likely to raise doubts among potential users"* | Richard Fontana 氏 2016-01-20、Apache-2.0 に無い特許の機能について | §8.4 も Apache-2.0 に無い機能である |
| *"I recommend that the OSI approve this license."*（*"I have generally tended to be liberal on proliferationism"* とも）| 同 2017-03-31、理事会に諮るとして | 許容型に特許を足した形は承認された |
| *"Do you have any project or community intending to adopt it if approved?"* | Simon Phipps 氏 2017-03-31 | 採用の予定を問われた（B2）|

**この節が establish しないこと。** BSD + Patent の承認を除き、どれも個人の発言で OSI の決定ではない。話者の役割は付けず、当時の所属が文中に在るものだけを書いた。

## 1.144 公有の作品は open source か（2014）、特許を添える形（2017）、学習と OSD（2024）（2026-11-08）

未読の候補から 3 本を読んだ（`rounds/2014-to-2024-license-discuss-public-domain-patents-ai-cited-observed.txt`）。2014 年の 1 通（Fogel 氏の *"when accompanied by"*）は入口に引いていたが、スレッドは読んでいなかった。

### 2014-05「米国の公有の作品を open source と言えるか」

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The things we don't like about public domain (lack of explicit liability limitation, different definitions in different jurisdictions) are not in themselves counter to the OSD, after all."* | Karl Fogel 氏 2014-05-02 | 公有の型の弱点は OSD の問いではない。ACD は §13、§14 と §4 でその弱点に答える |
| *"It wouldn't have any attribution or no-warranty clause, but the *absence* of those clauses is not a problem w.r.t. the OSD."* | 同 2014-05-03 | §10.2 が帰属を求めないことは OSD の問いにならない |
| *"We may not be in the business of approving licenses without patent grants any more, but nobody can say that licenses that don't grant patent rights explicitly are not open-source licenses."* | John Cowan 氏 2014-05-03 | 新しいライセンスには特許の許諾が求められる、という当時の観察で、§8 の向き |
| *"I continue to think that our CC0 decision was wrong insofar as it can be read as saying that the CC0 license is not an open-source (as opposed to OSI Certified) license."* | 同 | CC0 の扱いを OSD の不適合の認定と読まない立場 |
| *"The analoguous explanation for why cc0 didn't qualify is that it explicitly said "you get rights a and b but not c", with c a necessary right to copy and use the software."* | Henrik Ingo 氏 2014-05-04 | 止まった理由を明示の除外に置く読みで、§8.3 はその逆を明示する |

**逆側。** Cowan 氏は同じスレッドで *"We also are supposed to "discourage vanity and duplicative licenses"."* と述べた。Fontana 氏は、政府の職員が書いた公有のコードに政府の特許が及ぶ場面を挙げ、*"the same old MXM/CC0 inconsistency problem in a different form"* と呼んだ。

### 2017-03「特許と OSD」

Richard Fontana 氏 2017-03-07 は、特許に触れないライセンスについて *"this license is Open Source to the extent that, when used, it is accompanied by [a separate appropriate patent license grant]"* という形を問いの形で述べた。特許を別に添える考えで、ACD は同じ文書の中で §3 と §8 を並べる。

### 2024-05「AI と派生物」

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I came to the conclusion that this could not be fixed under my own rules in the OSD."* | Bruce Perens 氏 2024-05-27、帰属も対価も無い学習について | 学習を止める条件は OSD の中では置けない、と OSD の起草者が述べた。§6 が学習を条件なしに許すのは OSD に沿った形である。Perens 氏は日本の選択を *"unfortunate"* と呼び、OSD の外の Post-Open へ進んだ |
| *"Training AI with open source code is basically considered legal"*、*"License washing is not permitted."* | 佐渡氏 2024-05-26、日本の著作権法 30 条の 4 について | 日本では学習の自由を法が与えるので、§6.1 が足すものは法域で違う。出力が原作と実質的に同じでも、ACD では §4 が許す |
| *"you will need to retain an attorney to answer this question, and they will likely tell you "it depends"."* | Josh Berkus 氏 2024-05-25 | 学習と派生物の問いは法域と裁判で動く。§6.5 が判定を要しないと書く理由である |

**この節が establish しないこと。** どれも個人の発言で、OSI の決定ではない。Cowan 氏の「特許の無い新しいライセンスは承認しない」は 2014 年の観察で、規則として公表された文ではない。

## 1.145 受領者に要件を課してよいのは、ライセンサーの利益と保護の範囲だけ —— 委員の 2025 年の文（2026-11-08）

ModelGo の「モデル出力に AI 生成と示す」条項について、Josh Berkus 氏が OSD に適合するかを問うたスレッド（`license-review` 2025-03・`rounds/2025-03-license-review-modelgo-output-notice-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"I believe the nature of open source licenses is that they impose requirements on the licensee only to the extent they assure that the licensor receives the benefit that is their motive for putting software under an open source license and to protect the licensor from harm when they have generously made a gift."* | Pamela Chestek 氏 2025-03-02（*"in my personal capacity"*）| 要件は、ライセンサーが得たい利益と、ライセンサーの保護のためだけに在る、という原則である。ACD の Dedicator は受領者から何も受け取らないので、要件が 0 になる（§10.1）。保護の側は §13 と §14 が持つ。#307（条件が無いと執行できない）への答えもここに在る。執行して得たいものが無い |
| *"Having a license that requires that you tell me if AI was used doesn't mean someone actually will tell me; licenses aren't self-enforcing."*、*"So, in my opinion, it's greater friction for no benefit."* | 同 2025-03-02 | 出力に通知を求める条項は摩擦だけを生む。§6.4 は出力に何も求めない |
| *"That sounds like a restriction or condition on mere use. That would not be open source."* | Simon Phipps 氏 2025-03-03（*"in a personal capacity"*）| 出力の扱いを縛る条件を OSD の外と見る。§6.4 と §10.1 はそうした条件を持たない |

**逆側。** どれも個人の資格の発言で、OSI の決定ではない。Chestek 氏の原則は条件を課すライセンスを退ける向きの文で、条件の無いライセンスを積極的に勧めた文ではない。理事会が条件の無い 0BSD を承認した 2015 年の議事録（`board-decisions.md` §8.6）が、その側の記録である。

## 1.146 2003 年の記録: 献呈はライセンスではないので審査の対象にならない（2026-11-08）

David A. Wheeler 氏が「Public Domain」を OSI のライセンスの一覧に載せるよう求めたスレッド（`license-discuss` 2003-03・50 通・`rounds/2003-03-license-discuss-public-domain-on-the-list-observed.txt`）。読んだ記録の中で、OSI 側が公有の献呈の扱いを述べた最も古いものである。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"The Creative Commons document entitled "Public Domain Dedication" is not a license."*、*"it is not something that gets approved by OSI. We only review open source licenses."* | Lawrence E. Rosen 氏 2003-03-14 | 献呈だけでは審査の対象にならない、という線は 2003 年から在る。ACD が §3 と別に §4 の許諾を持つ理由と同じで、2011 年の同氏の *"OSI could analyze CC0 for its license fallback terms"*（§1.143）へ続く |
| *"please consider using a regular open source license that contains a disclaimer of warranty. The Public Domain Dedication does not deal with such issues because it is not a license."* | 同 | 無保証を持たないことが献呈の弱点として挙げられた。ACD は §13 と §14 を持つ |
| *"it isn't a license that conforms with the OSD. As such, OSI has no basis to "approve" it."* | 同 2003-03-16 | 承認の根拠を OSD への適合に置く。ACD は §4 が OSD に照らして読める形をしている |
| *"in general any sort of property right can be abandoned either with words or with the appropriate actions."* | John Cowan 氏 2003-03-14 | 放棄そのものは可能だという立場。Rick Moen 氏は同じ日に、合衆国法典の 17 編に放棄を許す規定は見当たらないと述べた |

**逆側。** Rosen 氏は同じ日に *"I'm still not convinced that there's ever a good reason for those who write software, or those who use it, to rely on a simple dedication of software to the public. Use a license."* とも述べた。ACD の答えは、献呈に頼らず許諾も置くこと（§4.4）だが、§3 を置く理由そのものへの疑いはこの文に残る。

**この節が establish しないこと。** 2003 年の個人の発言で、OSI の決定ではない。役割は付けていない。

## 1.148 「公有化の標準の文書が無い」—— 2011 年に、標準の文書なら審査の対象になりうると述べられていた（2026-11-08）

`license-discuss` 2011-09「Can OSI specify that public domain is open source?」（`rounds/2011-09-license-discuss-can-osi-specify-public-domain-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"So, perhaps, OSI's main business has been certifying particular legal documents, and there simply is no standard one in the sphere that's been considered (justifiably or not) "public domain". There is CC-0, which I believe meets the OSD. I suppose, say, the SQLite project could offer their own legal notice as the equivalent of a license for certification, and then OSI would have to face the issue."* | Richard Fontana 氏 2011-09-07（当時 Red Hat）| 審査の対象は特定の文書で、公有化の分野には標準の文書が無かった、という見立て。ACD は名前と版を持つ固定した文書（§16.4）で、その欠けていたものに当たる。同じ文で CC0 は OSD に適合すると述べている |
| *"once it is established that something is in the public domain, that thing is open source."* | Karl Fogel 氏 2011-09 | 公有の状態そのものは open source と読む立場 |
| *"The issue is not whether PD works are open source, but whether they exist -- that is, whether merely saying so can make a work public domain."* | John Cowan 氏 2011-09 | 問題は宣言で公有になるかどうかだ、という指摘。§4.4 は §3 が効くかどうかに依らずに許諾を立てるので、この問いに答えを預けない |

**逆側。** Cowan 氏は同じスレッドで、公有の作品を改変すると改変分は改変者の著作物になると述べ、*"That's what makes public-domain notices really bad."* と書いた。ACD では寄与は §2.6 で同じ条件に入るが、寄与として出されない改変は改変者の条件で配られる（§4.5）。これは許容型と同じ性質で、ACD が直すものではない。

**この節が establish しないこと。** 個人の発言で、OSI の決定ではない。Fontana 氏の文は「審査することになる」という見立てで、承認するとは述べていない。

## 1.149 明示の特許許諾、すぐ退けられる類型、共同体への必要性の説明 —— 審査の手順をめぐる 2018〜19 年の議論（2026-11-08）

`license-discuss` の「Proposed license decision process」（2018-12）と「Evolving the License Review process for OSI」（2019-05〜06）から（`rounds/2018-to-2019-license-discuss-review-process-cited-observed.txt`）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"if a license now is proposed without an express patent grant, I'd object to it vociferously"*、*"OSI recently disapproved a license that expressly excluded a patent license"* | Lawrence Rosen 氏 2018-12-13 | §8 は明示の許諾である。新しいライセンスに明示の特許許諾を求める声は、2014 年の Cowan 氏（§1.144）に続いてここにも在る |
| すぐ退けられる類型の例として *"obviously discriminatory", "incoherently written", "explicit patent non-grant"* | Luis Villa 氏 2019-06 | 3 つ目は ACD に当たらない（§8.3 は除外の逆を明示する）。2 つ目の「支離滅裂な起草」は B3 と B13 の側の危険で、1.4 の読みが潰し続けている |
| *"The OSI process is as much about policy as it is about technically applying the OSD rules correctly."*、*"they fail to even attempt to explain how the new license is necessary or beneficial for the open source community as a whole."* | Henrik Ingo 氏 2019-05 | OSD に反しないことだけでは足りず、共同体にとっての必要と利益を説明せよ、という求め。ACD の説明は gap（B10）と、出力や学習で受領者を露出させないこと（§6.5）で、提出文はこれを依頼者の都合ではなく共同体の利益として書く必要がある |
| *"the passive user shouldn't need a lawyer to use the software."* | Bruce Perens 氏 2019-05 | ACD の受領者には義務が無い（§10.1）ので、使うだけの人は何も確かめなくてよい（§2.3、§6.5） |

**この節が establish しないこと。** どれも個人の発言で、OSI の決定ではない。Rosen 氏の言う「最近否決された」ライセンスが何かは、この通からは特定できない。

## 1.150 CC0 の審査中に出た直し方の提案 —— 献呈と予備の許諾の両方に、明示の特許の許可を（2012-02）（2026-11-08）

`license-review` 2012-02「Request for consultation with CC on patent issue」（30 通・`rounds/2012-02-license-review-cc0-patent-consultation-observed.txt`）。§1.138 の CC0 の審査と同じ時期のスレッドで、ドシエは読んでいなかった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"CC should be asked to add language to CC0: an explicit permission to make use of patent claims necessary to use the software in the form that was dedicated or licensed. This should apply to both public domain, and the fallback license."* | Bruce Perens 氏 2012-02-19（Fontana 氏と同意見だと述べて）| 献呈と予備の許諾の両方に効く明示の特許の許可、という提案。ACD の §8 は §3 と §4 のどちらにも依らずに立ち（§2.4、§8.6）、この形に当たる。範囲は「献呈された形のまま使うのに要る請求項」までで、§8.4 はそれを越える（#305）|
| *"there is /one /party that needs the service the most. This is the private developer"*、*"The patent issue in CC0 is one such trap."* | 同 2012-02-21 | 特許の除外を、個人の開発者への罠と見る。§8.3 はその逆を明示する |
| *"we just want to respond properly"* | Christopher Allan Webber 氏（Creative Commons）2012-02-21 | CC は説明を用意すると述べた。CC0 はいまも 1.0 で、clause 4(a) は残っている |

**逆側（#310）。** Russ Nelson 氏は同じ日に *"Anybody who wants to set a booby trap will take steps to make sure that a separate legal entity owns the patent rights"* と述べた。1.4 の §8.5 は「支配する」を Dedicator 自身が許諾できる権利に限っており（E39）、関連会社が持つ特許には届かない。Apache-2.0 は許諾する者を Legal Entity、*"the union of the acting entity and all other entities that control, are controlled by, or are under common control with that entity"* で数えるので、ここは ACD の方が狭い。UPL-1.0、BlueOak-1.0.0、BSD-2-Clause-Patent も関連会社には届かないので、ACD はこの 3 本と同じ側に立つ。1.4 は変えないと決めた（PR 2647・問 2 (i)）。

**この節が establish しないこと。** 個人の発言で、OSI の決定ではない。CC がその後どう説明したかは、このスレッドの 30 通の中には無い。

## 1.151 Hugging Face で ACD はどう表されるか —— 一覧に無いので `license: other` になる（2026-11-08）

モデルとデータセットの主な公開先である Hugging Face Hub は、カードの `license` 欄に書ける識別子の一覧を持つ（`rounds/2026-10-17-huggingface-hub-docs-licenses-snapshot.txt`・2026-10-17 取得）。

**一覧の中身。** `apache-2.0`、`mit`、`cc0-1.0`、`unlicense`、`wtfpl` は在る。OSI 未承認の `openmdw-1.0` と `openmdw-1.1` も在る。OSI 承認済みの 0BSD、MIT-0、BSD-2-Clause-Patent、UPL-1.0、BlueOak-1.0.0 は無い。一覧に載るかと OSI の承認は別の事柄である。

**ACD を使う人の書き方。** 一覧に無いライセンスについて文書は *"In case of `license: other` please add the license's text to a `LICENSE` file inside your repo (or contact us to add the license you use to this list), and set a name for it in `license_name`."* と述べる。ACD のモデルやデータセットは `license: other` と `license_name` で書くことになり、ライセンスの絞り込みでは「other」の山に入る。

**件数の手がかり（API・2026-10-17・上限 1000）。** モデルは `openmdw-1.1` が 383、`openmdw-1.0` が 85、データセットはそれぞれ 33 と 31。`unlicense`、`wtfpl`、`cc0-1.0` のモデルは上限の 1000 に達しており、実数は取れていない（`~/osi-fetch/fetch/2026-10-17/hf/`・リポジトリの外）。

**B2 への当たり方。** OpenMDW は一覧に識別子を持ち、公開の時点で絞り込みに出る。ACD は採用者が `other` を選ぶので、探す人の目に入りにくい。文書は一覧へ足す依頼の道（*"contact us"*）を示しているが、これは外へ出す行為なので AI は送らない。送るならオーナーの行為で、OSI の承認とは独立に試せる。逆側: 採用の実績が 1 件の段階で一覧に載せる依頼が通るかは分からず、通っても採用そのものは生まれない。

**この節が establish しないこと。** 一覧は hub-docs の main で、取得の後に変わりうる。件数は API の上限で切れている。

## 1.152 Unlicense の審査で使われた基準 —— 「裁判所が OSD に反して読みうるか」（2020-03〜04）（2026-11-08）

献呈と許諾を併せ持つ唯一の承認済みの前例（2020-06-12 承認）の審査から（`rounds/2020-03-to-04-license-review-unlicense-cited-observed.txt`）。ドシエは理由書（#270）と拒否権のスレッドを読んでいたが、ここに置く 4 通の段落は記録していなかった。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"If I were asked to interpret this license, I would say that the use of the term "public domain" is naive and likely incorrect (including in the US), but the intent of the author is clear."*、*"I don't see how a court could misinterpret this document in any way that could be contrary to the OSD."* | Pamela Chestek 氏 2020-04 | 基準は「裁判所がこの文書を OSD に反して読みうるか」だった。ACD は献呈が効かない場合の許諾を §4.4 で明示しており、意図を推し量る必要がない |
| *"If the lawyers are OK with the Unlicense text, then I don't see any reason to object to it, as a developers."* | Josh Berkus 氏 2020-04 | 法律家の判断に寄せた賛成で、B1 の側に当たる（#270 の *"The lawyers who opined"* と同じ向き）|
| *"Unlicense contains two (use and sell) of the five (make, use, sell, offer to sell, import) patent "verbs" from the US patent statute."* | McCoy Smith 氏 2020-03-29 | Unlicense の特許は、許諾の動詞から暗に読む余地しかなかった。ACD の §8 は明示の許諾で、§8.1 は 5 つの動詞すべてと "otherwise practise" を持つ |
| *"I think that the Unlicense is a (bad but still) OSD-compliant device, modulo the lack of a patent license"* | Lukas Atkinson 氏 2020-03 | 承認された前例でさえ、特許の許諾の欠如が留保として挙がった。ACD はその留保に当たらない |

**逆側。** Unlicense は legacy として、広い利用と法律家の一致を経て承認された（#270）。新規の ACD は同じ道を持たない。Atkinson 氏は同じ通で *"The Unlicense is not safe to use and likely fails to achieve its stated goals"* とも述べた。

**この節が establish しないこと。** 個人の発言で、決定は理事会の承認（2020-06-12）だけである。McCoy Smith 氏の通は Outlook 形式で他人の文を引用の印なしに含むので、引いたのは同氏が書いた冒頭の 2 文だけにした。
