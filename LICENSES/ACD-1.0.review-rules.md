---
file: LICENSES/ACD-1.0.review-rules.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-09-24
canonical-ref: LICENSES/ACD-1.0.review-corpus.md (アーカイブ全体の測定) / LICENSES/ACD-1.0.review-precedents.md (個別スレッドの読み) / LICENSES/ACD-1.0.board-decisions.md (理事会の決定) / LICENSES/rounds/ (原典の保存)
---

# OSI が**公表している規則**を原典で読んだもの（§1.70 / §1.76 / §1.81 / §1.82 / §1.86）

**この file は `ACD-1.0.review-corpus.md` から 2026-09-15 に切り出した。** 分けた理由は
行数ではなく**資料の種類**である ——**本 file は「OSI が公表しているページ」を原典で読んだ記録**で、
corpus は**メーリングリストのアーカイブ全体を測った記録**、`review-precedents.md` は
**個別スレッドの読み**、`board-decisions.md` は**理事会という別の発話主体の記録**である。

**同じ出来事について、公表ページは規則を、リストは議論を、理事会は決定を残す。**
**1 つの file に置くと「誰が言ったか」が節の位置から読めなくなる。**

**節番号は動かしていない。** §1.70 は §1.70 のまま、この file にある ——
**既存の参照をすべて有効に保つため**（`review-precedents.md` / `review-corpus.md` の分割と同じ規約）。
**新しい節をどこに足すかの規則**: **公表ページの逐条 → 本 file、アーカイブ全体の測定 → corpus、
個別スレッドの読み → precedents、理事会の決定 → board-decisions。**

## 1.70 **新規ライセンスに適用される 8 つの基準**（原典・2026-09-11 取得）と、ACD-1.0 の当たり方

**このドシエは、これを一度も条ごとに当てていなかった。** `review-process` ページは #77 で
「提出時に何を出すか」のために読んだが、**同じページの「License approval standards」節、
すなわち承認の基準そのものは、`Standard for New Licenses` という語で 1 度引用しただけだった**
（R5・§1.67）。**逐語は以下**（`https://opensource.org/licenses/review-process` ——
ページ自身が *"Last modified on March 13, 2024"* と述べている。2026-09-11 取得）。

**⚠ 検出器の注意**: このページを最初に走査したとき「該当なし」と出た ——
**`Standard for New Licenses` を大文字のまま探したが、ページ上の見出しは
`Standard for new licenses` である。** 大小の 1 文字で「基準は存在しない」と読むところだった。

| # | 逐語（*"In addition to meeting the Open Source Definition, the following standards apply to new licenses"*） | ACD-1.0 の位置 |
|---|---|---|
| 1 | *"The license must be **reusable**, meaning that it can be used by any licensor **without changing the terms** or **having the terms achieve a different result for a different licensor**"* | **前半は測ってある** —— 固有名詞 0・置換テキスト 0・採用に本文編集は不要（§4b）。**後半は我々が一度も検討していない** —— **§12（人格権）は法域によって効果が変わる**（放棄できる法域では放棄、できない法域では不行使の合意）。**これは条項が licensor を区別しているのではなく法が異なるのだが、「異なる licensor には異なる結果になる」と読まれうる。**（`against.md` #129）**同じ日に、同じ corpus から答えが出た** —— **OSC License v1 は、「MIT の免責がドイツ法では効かない」ことを理由に承認されている**（§1.69・委員会の理由書: *"under German law, an attempt to disclaim liability that cannot lawfully be disclaimed might create greater liability than necessary for the copyright owner"*）。**MIT は承認されたままである。****つまり OSI は、効果が法域で変わるライセンスを承認しており、しかも「効果が法域で変わること」を理由に別のライセンスを承認した。** ゆえに基準 1 の第 2 枝は「効果に法域差があってはならない」とは読めず、**「本文が特定の licensor に合わせて作られていてはならない」**（第 1 枝と同じ趣旨）と読むほかない。**§12 の本文はどの licensor に対しても同一である。** 併せて、*"to the fullest extent permitted by law"* 型の免責と §15.4 の可分性は**承認済みライセンスに遍在する**同型の構造である |
| 2 | *"The license does not have terms that **structurally put the licensor in a more favored position** than any licensee"* | **当たらない方向に作ってある。** 受領者に条件は一切なく（§10.1）、Dedicator の側に義務がある（§5 の不行使の約束・§12・§2.6 の特定義務）。**licensor にだけ有利な留保は §11 の商標のみ**で、これは承認済みライセンスに広くある。**⚠ この基準は生きている（2026-09-24 追記）** —— 委員長 Pamela Chestek 氏が 2026-09-22 に ModelGo の特許終了条項（Licensor を訴えたときだけ終了）へ当て、*"This does put the licensor in a more favored position than a licensee"* と述べた。提出者は翌日、誰を訴えても終了する形へ改めた（`license-review` 2026-09 アーカイブ）。**ACD-1.0 には終了条項が無い**（§10.4）ので当たらない。**ただし次版には 1 つ licensor 側の留保がある** —— 1.1 / 1.2 草案の §16.4 は、改変テキストを同じ名前・識別子で頒布することを **Steward にだけ**許す。これは §16.6 が「本著作物の条件ではなく、受領者を拘束しない」と定める**文書の版管理**についての留保で、利用者の権利を狭めない。**それでもこの基準の文言に対して読まれうる箇所として、提出前に説明を用意しておく**（`against.md` #221）|
| 3 | *"To the extent that any terms are **ambiguous, the ambiguity must not have a material effect** on the application of the license"* | **§15.1**（最も広い許諾を与えるように解釈する）と **§15.3**（起草者不利の解釈準則を排除しない —— 排除**しない**と明記）が、まさにこの基準に向けて書かれている |
| 4 | *"The license must be **grammatically and syntactically clear** to a speaker of the language of the license"* | **我々の生きたリスク。** 非母語話者が起草し弁護士のレビューが無く、4,896 語ある（B3 / #116）。**否決された「起草が粗い」3 件はいずれも我々より短い**（§1.69）|
| 5 | *"**Every possible variation** of the application of the license must meet the OSD"* | **条件が無いので変化の幅が小さい** —— 適用者は本文を編集せず、選択肢も持たない（§10.1 / §4b）|
| 6 | *"It must be **possible to comply with the license on submission**"*（例として SSPL が挙がっている） | **義務が 1 つも無いので、遵守は自明に可能である。** この基準は ACD にとって最も安全な 1 行 |
| 7 | *"The license must **fill a gap that currently existing licenses do not fill**"* | **gap の主張は任意ではなく要件だった。** B10 がこれに当たる。1 文の形は §B.0 と入口ページに置いた |
| 8 | *"The text must be the **complete license**; overlays like Commons Clause and exceptions like ClassPath will not be approved in isolation"* | **通る。外部参照 0 件・付属文書なし**（§1.67 R2 と同じ測定）|

**同じ節に、基準の外側から効く 2 文がある。どちらも我々に不利な向きである。**

1. *"**Approval of a license with the same or similar terms in the past does not bind the OSI**
   to approval of a newly submitted license."* ——**§1.69 で見つけた「MIT-CMU は *redundant* と
   名指しされて承認された」を、そのままは押せない。** 重複が障害でないことは示すが、
   **過去の承認は次の承認を拘束しない**と明文で述べられている。
2. *"Members of the license-review list are highly skilled … **Their consensus that a license does
   not ensure software freedom may, in some cases, be the justification for rejecting a license
   even where they cannot identify a specific aspect of the OSD or the approval guidelines below
   that is not met**."* ——**列挙された基準を全部通ることは、承認を意味しない。**
   我々の証拠戦略（OSD 逐条・機械的検証・§1.67 の規則に当たらないこと）は**必要条件の側だけを
   固めている**のであって、**十分条件は存在しない。**（`against.md` #130）

### 1.70a 基準 4（明晰さ）だけは主張ではなく測定にできる —— 承認済みライセンスとの文長比較

**⚠ この節は公開した数時間後に、同じ日のうちに全面訂正した。最初の表は誤りで、しかも
我々が最も悪く見える向きに誤っていた。** 経緯を消さずに書く ——**誤った数を出した記録の方が、
出したことを隠した記録より価値がある。**

**何が起きたか。** 文の切り方を「`. ; :` の後に**大文字・引用符・括弧**が続く位置」と定義した。
**ACD は条番号が本文と同じ行に続く形式（`8.1 The Dedicator grants …`）なので、`.` の次が数字であり
切れ目として認識されない** ——**2 つ以上の条が 1 文として数えられ、平均も最長も長文率も膨らんだ。**
**Apache-2.0 と MPL-2.0 は見出しが別行なので同じ instrument でも数値が変わらない** ——
**つまり歪みは比較対象ではなく我々の側だけに掛かっていた。**
**instrument が、我々が使っている書式だけを罰していた。**

**訂正した instrument**: 切れ目の条件に「数字 + ピリオド」を足す（`(?=[A-Z"(]|\d+\.\d|\d+\. )`）。
**検証**: 同じ変更で **Apache-2.0 と MPL-2.0 の数値は 1 文も動かない**（43 文 / 80 文のまま）——
**変わったのは条番号が行内にある text だけ**である。

| ライセンス | 文数 | 平均 | 中央値 | 最長 | **45 語超** | うち列挙型 | うち従属節 2 つ以上 |
|---|---|---|---|---|---|---|---|
| **ACD-1.0** | 179 | **27.3** | 25.0 | **85** | **11.7%** | 76.2% | **0.0%** |
| **ACD-1.1 草案** | 173 | 28.0 | 25.0 | **85** | 13.3% | 69.6% | **0.0%** |
| Apache-2.0 | 43 | 36.5 | 30.0 | 180 | 25.6% | 81.8% | 18.2% |
| MPL-2.0 | 80 | 30.0 | 25.5 | 108 | 18.8% | 66.7% | 13.3% |
| EPL-2.0 | 50 | 42.5 | 28.5 | 195 | 28.0% | 71.4% | 21.4% |
| OSL-3.0 | 47 | 34.8 | 33.0 | 119 | 23.4% | 54.5% | 0.0% |
| CDDL-1.0 | 95 | 26.3 | 24.0 | 151 | 11.6% | 63.6% | 9.1% |

**訂正後の読み**:

- **平均文長は比較した 5 本のうち 4 本より短い**（27.3 —— CDDL-1.0 の 26.3 に次ぐ）。
- **最長文は 6 本中で最も短い**（85 語。次点は CDDL-1.0 の 151、EPL-2.0 は 195）。
- **45 語超の割合も最小に近い**（11.7% —— CDDL-1.0 の 11.6% とほぼ同じ）。
- **従属節が 2 つ以上積まれた長文は 0 件**（Apache-2.0 は 18.2%、EPL-2.0 は 21.4%）——
  **解析の負荷という意味では、比較した中で最も軽い。**

**したがって、前の版が出した作業項目（「1.1 で長文の割合を下げる」）は撤回する。**
**下げるべき値ではなかった** ——**数字は既に比較群の良い側にあり、下げようとして列挙を切れば
語数が増えて明晰さは上がらない。** **測り直した結果、やるべきでないと分かった作業を
やらないことも成果である。**

#### 1.70b 二度目の訂正（2026-09-14）—— 表の 7 列のうち 2 列は、方法が書かれていなかった

**上の訂正は文の切り方だけを直した。** 敵対的検証（主張の種類 6）で同じ表を当たると、
**最後の 2 列「うち列挙型」「うち従属節 2 つ以上」の定義が、この節にもドシエのどこにも無い。**
**定義の無い数字は再実行できない。** そして**結論を運んでいるのはその 2 列である**
（*「解析の負荷という意味では、比較した中で最も軽い」*）。

**方法を書いて測り直した。** 道具は `.github/scripts/measure_clause_clarity.py`（committed・
定義は docstring に書いてある。切れ目は上の訂正で確定した条件、「列挙型」＝45 語超でカンマ 3 つ以上、
「従属節 2 つ以上」＝従属を導く語が 2 回以上出現）。比較対象は SPDX の清書テキスト。

| ライセンス | 文数 | 平均 | 中央値 | 最長 | 45 語超 | うち列挙型 | **うち従属節 2 つ以上** |
|---|---|---|---|---|---|---|---|
| **ACD-1.0** | 175 | 26.0 | 23 | **81** | 10.3% | 83.3% | **61.1%** |
| **ACD-1.1 草案** | 172 | 26.7 | 23.0 | 81 | 12.2% | 81.0% | **61.9%** |
| Apache-2.0 | 50 | 31.3 | 27.0 | 110 | 22.0% | 81.8% | 54.5% |
| MPL-2.0 | 96 | 24.7 | 19.5 | 108 | 13.5% | 92.3% | 38.5% |
| EPL-2.0 | 62 | 34.2 | 25.0 | 183 | 21.0% | 84.6% | 61.5% |
| OSL-3.0 | 67 | 24.4 | 20 | **76** | 13.4% | 66.7% | **33.3%** |
| CDDL-1.0 | 98 | 25.4 | 24.0 | 151 | 10.2% | 70.0% | 50.0% |

**🔴 撤回するもの（2 つ）**

1. ***「従属節が 2 つ以上積まれた長文は 0 件」*** —— 方法を書いた指標では **61.1%** で、
   **比較群の中でも高い側**に来る。**記録の 0.0% を「誤り」とは言わない** ——「積まれた」が
   *入れ子だけ*を意味していた可能性は排除できないからである。**言えるのは、
   この数字は再実行できず、方法を書いた指標では結論が逆向きになる、ということだけ。**
   **したがって *「解析の負荷という意味では、比較した中で最も軽い」* は取り下げる。**
2. ***「最長文は 6 本中で最も短い」*** —— 再実行では **OSL-3.0 が 76 語**で ACD の 81 語より短い。
   **順位が方法に依存する** のに、依存しないかのように書いていた。

**🟢 残るもの（同じ再実行で支持された）**

- **平均・中央値・45 語超の割合は、いずれも比較群の良い側**（平均 26.0 は 7 本中 3 番目に短く、
  45 語超 10.3% は**最小**）。**「代理指標では良い側にある」という register の要旨は生き残る。**
- **B1（弁護士レビュー無し）には何の影響も無い。** この節が動いても動かなくても、
  **1 ミリも動かない**ことは前から書いてあるとおりである。

**⚠ そしてこの訂正自身の逆側**: 審査者がこの測定を自分で走らせる見込みは高くない。
**露出しているのは「我々が引用した」という事実のほうであって、彼らが検算することではない。**
**だが我々のドシエは *"check us"* を掲げている** ——検算されない前提で数字を置くなら、
その掲示のほうが嘘になる。**だから直した。**

**この測定が establish しないもの（訂正前と同じく、ここは変わらない）**:
**短い文は明晰であることを意味しない。** 文長は代理指標であって明晰さそのものではなく、
**非母語話者の起草に固有の誤り（冠詞・前置詞・時制の一致）はこの測定に一切現れない。**
**弁護士のレビューが無いという事実（B1）は、この測定では 1 ミリも動かない。**

## 1.76 要件リストを原典で 1 項目ずつ当てたら、1 件だけ答えていなかった

**§1.75 で「手続きの不備は評価の不在を招く」と分かったので、次にやることは決まっていた** ——
**求められている項目と、我々が実際に送る文面を、1 項目ずつ突き合わせる。**
`review-process` ページの "How to submit a request" を取り直し（2026-09-13）、
**legacy 8 項目 + new 3 項目**を §B.0 に当てた。

**11 項目中 10 項目は満たしていた。** 欠けていたのは 1 つだけである:

> *"Provide **any additional information** that the submitter believes would be helpful for license
> review. **For example, approval of the license by Debian, the FSF or the Fedora Project** would be
> relevant to the review process."*

**我々の答えは「無い」である。** だが**答えが「無い」の項目ほど、書かなくても文面は自然に読める**
——これは #77（ScanCode 識別子・提案 tag）で 2 度踏んだ形と同じで、
**「我々の弱点を述べる項目ほど、静かに落ちる」**という一般形になる。
`Third-party Endorsement: None (no Debian, FSF or Fedora review)` を両方の metadata block に足し、
**Check 463 の要求項目へ加えた。**

**この増分で、Check 自身の欠陥も 1 つ出た。** Check 463 の**成功メッセージ**が
*"OSI の要求 **11 項目**をすべて含む"* とリテラルで述べており、**項目を足しても 11 のままだった。**
**Check 460 が他所で禁じている「自己申告の件数が実測とずれる」を、Check 自身の成功メッセージで
やっていた** ——しかも**成功メッセージは読み手が最も信用する場所**なので、ここでの drift は最も悪い。
`len(_req463)` からの導出へ直した（現在 **12 項目**）。

**併せて、先に足した Check 460 face (p) が即座に働いた。** 文面に 1 行足した瞬間、
**申告語数 1098 と実測 1107 のずれを検出した** ——**face (p) を足したのが同じ日の午前で、
その日の午後に元を取った。**

## 1.81 規範文書の「読んだ」と「1 条ずつ当てた」を棚卸しし、未適用が 1 つ出た —— **Code of Conduct を我々自身に当てていなかった**

**2026-09-13 に同じ形の欠落が 3 度出たので**（提出要件の third-party endorsement / OSD 3 の後半 /
#77 の 3 件）、**承認に効く規範文書を列挙し、「読んだだけ」と「1 条ずつ当てた」を分けて数えた。**

| 規範文書 | 読んだ | **1 条ずつ当てた** | 置き場 |
|---|---|---|---|
| **Open Source Definition**（10 条）| 2026-09-06 | **✅ 2026-09-13 に完了**（4/6/7/9/10 は 09-06、1/2/3/5/8 は 09-13）| `submission-reference.md` §3 / §3b |
| **review-process "How to submit a request"**（legacy 8 + new 3）| 2026-09-06 | **✅ 2026-09-13**（1 件欠落を発見・補填）| §1.76 / Check 463（**12 項目を機械強制**）|
| **review-process "Standard for new licenses"**（8 条）| 2026-09-11 | **✅ 2026-09-11** | §1.70 |
| **review-process "License approval standards" 前文** | 2026-09-11 | **✅**（天井 2 つ）| `against.md` #130 |
| **common-reasons-for-rejection** | 2026-09-07 | **✅** | `submission-reference.md` §3c |
| **OSAID v1.0** | 2026-09-06 | **✅** | `review-responses-meta.md` Q32d |
| **SPDX inclusion principles** | 2026-09-06 | **✅** | `against.md` #78 |
| **Mailing List Code of Conduct** | 2026-09-09（**全文確保は 09-13**）| **❌ 我々自身の行動に当てていなかった** | **本節** |

**最後の 1 行が、いちばん当てるべきものだった** ——**2026-09-09 の通知が援用したのはこの文書である。**

### 当てた結果 —— 1 件、我々は満たしていない

**"Disclose potential conflicts"**（逐語）:
> *"List discussions often involve **interested parties**. We expect participants to be aware when
> they are conflicted due to employment or **other projects they are involved in**, and **disclose
> those interests** to other project members. … **When in doubt, over-disclose.** Perceived
> conflicts of interest are important to address, so that the lists' decisions are credible."*

**実測（2026-09-13・アーカイブの全文から）**: **`license-review` へ送った 3 通
（2026-09-03 ×2・2026-09-04）は、いずれも ACD-1.0 に一切触れていない。**
**`license-discuss` の 2026-09-06 04:47（他者のネットワーク・コピーレフト質問への回答）も
触れていない。** **つまり、他者のライセンスについて実質的な意見を述べた 4 通すべてで、
我々自身が同じ領域のライセンスを係属させていることを開示していない。**

**軽くする事情は書くが、消しはしない**: 4 通はいずれも**条文の作動についての質問と分解**であり、
承認への賛否を述べていない（2026-09-04 のものは *"I am not arguing for either outcome here"* と
明言している）。**だが CoC の基準は「賛否を述べたか」ではなく「利害があるか」であり、
*"when in doubt, over-disclose"* と書いてある。**

### やること（`REVISION-PROTOCOL.md` §3.7 に規則 7 として追加した）

**他者のライセンスについて述べるときは、1 行で開示する。** 例:
*"Disclosure: I am the steward of ACD-1.0, which is under discussion on license-discuss."*
**これは投稿再開の可否とは無関係に、こちらの側で先に決めておけることである。**

### この節が establish しないこと

**開示していなかったことが、通知の理由だったとは言えない。** 通知は AI 生成について述べており、
**利益相反には触れていない。** **2 つを結び付けるのは、我々の推測である。**
**記録するのは「CoC を当てたら 1 件出た」という事実だけである。**

## 1.82 凍結は我々の礼儀ではなく、OSI が書いている手続きである（2026-09-13・process ページを再取得）

**`REVISION-PROTOCOL.md` §2 は凍結を我々自身の理屈で正当化してきた** ——「読まれたテキストが動けば、
その議論は何についてのものでもなくなる」。**正しいが、OSI は同じことを規則として書いている。**
**我々はそれを一度も引いていなかった。**

**逐語**（`https://opensource.org/licenses/review-process`・2026-09-13 15:00 JST 取得）:

> *"However, **a license cannot be changed while it is being considered**. If the license submitter
> would like to change the language of the license, **the current version of the license should be
> withdrawn from review and an updated version submitted**."*

**これは 2 つのことを変える。**

**(1) 我々の方針が「規律」から「手続きの遵守」になる。** 審査者が `REVISION-PROTOCOL.md` を読んで
見るのは steward の自己規律だが、**規則を引けば、公表された手続きに従っていることの記述になる。**
**手続きが門番であることは §1.75 で実測済み**（我々と同じ類型の直近 3 件は、本文の評価に入る前に
required information の欠落で止まった）——**その門の内側にある規則を引かない理由が無い。**

**(2) 分岐 B の手順に、書かれていなかった一段がある。** 1.0 を `license-review` に出したあとで
次版に替えるなら、規則は「送り直す」ではなく **「取り下げてから、更新版を提出する」**である。
`REVISION-PROTOCOL.md` §2 の「1.0 は永久凍結・次版は併置」はこれと矛盾しないが、
**取り下げという手続き上の一手はどの文書にも書かれていなかった。**

**そして同じ段落が、オーナーの方針をそのまま推奨している。**

> *"We recommend that, if changes are going to be made, that the license submitter **wait and collect
> all the desired changes in a single new submission** rather than withdrawing and resubmitting the
> same license several times."*

**「届いた議論を全部取り込んだ改善版を出す」（2026-09-04 オーナー）は、我々が選んだ流儀ではなく、
OSI が明文で推奨している出し方だった。** 分岐 B（沈黙のまま自己改善版を出す）でも同じ形になる。

**⚠ 新しい事実ではないもの（混ぜない）**: Decision Date の規則
（*"(a) 60 days after a license is initially submitted … or (b) 30 days after submission of a revised
version … provided that date is no earlier than 60 days after the original"*）は
**`review-responses.md` §5 の 2026-09-10 補足に既に記録されている。** 本節は再導出で確認しただけである。
**なお、この公表規則と McCoy Smith 氏の *"two months from your final submission"*（2026-08-28）は
同じことを述べていない** ——規則では改訂は時計を初回起点のまま +30 日にするだけで、**2 か月へ戻さない。**
**どちらが実務を支配するかは我々には決められない**ので、両方を並べて置く。

**Code of Conduct は、予告されたが 2026-09-13 15:00 JST 時点でまだ更新されていない。**
ページの自己申告は **"Last modified on November 2, 2023"** のままで、
**本文に AI への言及は 1 語も無い**（"AI" の出現はナビゲーションの "Open Source AI" のみ）。
**これは B14 についての事実であって、通知の当否についての事実ではない。**

## 1.86 Code of Conduct を 1 項ずつ当てた —— 引かれた条は 3 つの番号付き小項目を持ち、我々は 1 つしか答えていなかった

**2026-09-15 の moderator の問いは *"Respect time and attention"* を名指ししている。**
**その条を原典で読むと、番号付きの小項目が 3 つある**（逐語は
`rounds/2026-09-15-osi-mailing-list-code-of-conduct-snapshot.txt`）。
**§1.85 が答えたのは 1 だけである。**

### 🔴 まず、我々は 2 つある Code of Conduct のうち別の方を pin していた

| URL | 自称 | 我々の扱い |
|---|---|---|
| `/codeofconduct` | Page created 2007-11-19 / Last modified **2023-11-02** | **2026-09-13 に pin 済み** |
| `/code-of-conduct` | **"Code of Conduct for OSI Mailing Lists"**・created 2013-02-06 / Last modified **2023-05-04** | **2026-09-15 に pin（本増分）** |

**実測すると本文はほぼ同一**（776 語 対 789 語・差は箇条書きの番号と markup であって中身ではない）
なので、**前の pin から引いた結論に誤りは無い。** だが**リストを規律しているのは後者**であり、
**条を引かれた相手も後者**である。**「近い文書」は「その文書」ではない。**

### 🔴 そして、予告された更新はまだ起きていない

**2026-09-09 に moderators は CoC を *"updated to better reflect the use of AI"* にすると述べた。
2026-09-15 時点で、両ページとも変わっていない**（自称更新日は 2023-05-04 / 2023-11-02 のまま、
本文に AI の条項は 1 つも無い）。

**したがって、steward に引かれた規則** —— *"We do not allow posts generated by AI without careful
review from the author and will reject posts where we suspect that an AI has been responsible for
all or most of a message"* —— **は Code of Conduct には無い。** moderators のリスト投稿に在る。
**これは反論ではなく、どの文書に何が書いてあるかという事実である。**
**そして反論として使ってはならない** ——リストを運営しているのは moderators であり、
**published かどうかは、その方針が実在するかとは別の問いである。**

### 3 つの小項目に、1 つずつ当てた

| | 条文（要点）| 我々の実測 | 判定 |
|---|---|---|---|
| **1** | *"we value concision and clarity. Emails that are brief and to the point…"* | **散文の中央値 683 語 対 他 188 語。6 通すべてが 69〜95 パーセンタイル** | **🔴 当たる**（§1.85）|
| **2** | *"Conversations should remain focused and on-topic … **avoid flooding the list with long threads** by reading the entire thread first, instead of **responding quickly to many emails in a short period of time**"* | **6 通 / 活動 4 日 / 1 日最大 2 通 / 24 時間内に 3 通以上が 1 回**（2026-09-03 23:36・23:56 と 09-04 18:54 の 19.3 時間）。同じ窓で **Fontana 氏 13 回・Chestek 氏 5 回・McCoy 氏 5 回・Dolan 氏 1 回** | **🟢 当たらない（低い側）。ただし 0 ではない** |
| **3** | *"New members … should be careful to respect the time and energy of long-time list members by **doing research** … before asking questions"* | **6 通に条項・OSD の引用が計 55 件**（8/26 の投稿だけで OSD 十条中 11 の一意参照、9/6 の 1 通で条項 25 件）。**機械的に測れるのはここまで**で、「研究したか」そのものは測れない | **🟢 当たらない方向の証拠はある** |

**別条だが同じページの *"Disclose potential conflicts"* は、既に当てて外れていた** ——
他者のライセンスについて述べた 4 通すべてで、**我々が提出者であることを開示していなかった**
（#137・`REVISION-PROTOCOL.md` の規則 7 として前向きに閉じた）。

### この節が establish しないこと

**「小項目 2 と 3 に当たらない」は、小項目 1 に当たることを打ち消さない。**
CoC 自身が *"We expect it to be followed **in spirit as much as in the letter**"* と述べており、
**3 つのうち 1 つに当たれば、条に当たっている。**
**確立するのは「どこに当たり、どこに当たらないか」だけである。**


## 1.102 OSI 自身が機械可読な決定記録を公開している —— 初めて読んだ（2026-09-20）

**新しい source type である。** これまで我々が読んできたのは、メーリングリストのアーカイブ（議論）、
理事会の議事録（決定）、規範ページ（基準）の 3 つだった。**4 つ目は OSI の GitHub org と、
そこから辿れる新しい API である。**

```
https://opensource.org/api/licenses          # 一覧（126 件）
https://opensource.org/api/license/<id>      # 1 件
```

**旧 `api.opensource.org` は 404 で、`OpenSourceOrg/api` repo 自身が DEPRECATED、
`OpenSourceOrg/licenses` は UNMAINTAINED と名乗っている。** 現行の口は上の 2 つで、
`dotOrg`（opensource.org の公開 issue tracker）の **issue 199「Provide access to licenses data
via an API」が 2025-06 に閉じられた**（`#N` はこのドシエでは不利な事実の採番なので、外の採番は番号だけで書く）あとに生きている。

### 何が入っているか

各 entry に `submission_date` / `approval_date` / `submission_url`（アーカイブの当の 1 通）/
`board_minutes`（決めた回の議事録）/ `keywords`（増殖カテゴリ）/ `stewards` が在る。
**これは #139 が「我々に無い」と述べた当のもの** ——**リストは議論の記録であって決定の記録ではない**が、
**この API は決定の側から、議論の当の 1 通へリンクを張っている。**

### 測ったこと（2026-09-20 取得・126 件）

| 量 | 値 |
| :-- | :-- |
| 提出日と承認日が両方在る | **60 件**（1 件は承認日が提出日より前という明らかな誤り ——`cal-1-0` ——除外後）|
| 提出 → 承認の日数 | **中央値 83 日**／平均 128／**四分位 59〜144**／最短 7（`ms-pl` / `ms-rl`）／最長 770（`rpl-1-5`）|
| 2023 年以降に承認された分 | n=14・**中央値 82 日** |
| `submission_url` が在る | 57 / 60 |
| `board_minutes` が在る | 58 / 60 |

**⚠ この中央値は「承認された提出について」の所要である。** 否決・取り下げ・留め置きは
この一覧に現れないので、**「出せば 83 日で決まる」とは読めない。**
**我々がアーカイブから再構成した中央値 101 日（`review-corpus.md`）とは母集団が違う** ——
**2 つの数を並べるときは、どちらも「決まった場合の」所要であることと、
数え方が違うことを同じ場所に書く。**

**⚠ データ自身に誤りが在る。** `approved` の boolean は **7 件しか true でない**が、
その 7 件は 2025-07 以降の承認で、**MIT-0 や Blue Oak は `approved: false` のまま承認日を持っている。**
**フィールド名が示すものと中身が違う** ——**この API を「承認済みか」の判定に使ってはならない。**
（126 件という総数も、SPDX から数えた承認済み 149 件と合わない。）

### 🟢 増殖カテゴリが、承認と両立している

`keywords` は OSI の増殖カテゴリそのもので、実測は
**`non-reusable` 25 / `superseded` 20 / `special-purpose` 15 / `uncategorized` 14 /
`redundant-with-more-popular` 12 / `popular-strong-community` 12 /
`other-miscellaneous` 11 / `international` 7 / `voluntarily-retired` 5 / `legacy` 4。**

**2 つが我々に直接効く。**

1. **`non-reusable` が 25 件ある**（PHP-3.01 / Multics / wxWindows / APSL-2.0 / IPL-1.0 ほか）。
   **「再利用できない」と OSI 自身が分類している 25 件は、いずれも承認されている。**
   `review-labels.md` §1.98 / §1.99 が扱う *crayon* / *vanity* のラベルは、**承認の障害として
   一貫して働いてきたわけではない。** **⚠ ただし 25 件はいずれも旧い承認で、
   現在の委員会が同じ扱いをする証拠ではない。** 我々の答えは依然 `submission-reference.md` §4b
   （固有名詞 0・置換テキスト 0（§16.1 の推奨 notice の雛形 1 欄 `<location of this file>` を除く —— 採用者が自分の notice に書く欄で、本文は編集しない））であって、この統計ではない。
2. **`redundant-with-more-popular` が 12 件ある。そこに Blue Oak が入っている** ——
   **承認日 2024-01-19、つまり最近の承認である。**
   **#84（「0BSD が在るのになぜもう 1 つ」）に対する、我々の推論ではない答えがここにある**:
   **OSI は 2024 年に 1 件承認し、そのうえでそれを「より普及したものと重複」に分類した。**
   **承認と重複は両立する。**
   **⚠ 逆側**: **分類されること自体は費用である。** 重複と名指しされたライセンスは
   採用の議論でそのラベルごと引かれるので、**B2（実使用）を悪化させる向きに働く。**

### 🔴 探して、無かったもの —— 「not approved のまま留め置く」状態は、どの公開面にも出ていない

理事会が 2025-07-18 に述べた第 3 の帰結（*"could stay in a status where it is **not approved** if it is
duplicative and not used by a project"*・`board-decisions.md` §2）を、**この機械可読な一覧の中で探した。**
**無い。** 提出日を持ち承認日を持たない entry は 23 件あるが、**中身は EPL-1.0 / OSL / CPAL-1.0 など
明らかに承認済みの古いもの**で、**データの欠落であって状態ではない**。

**つまり、その状態に置かれた提出は、外からは 1 件も見えない。**
**§3 が記録する「14 か月公表されていない」は、process ページだけの話ではなかった** ——
**機械可読な面にも出ていない。**
**⚠ これが establish するのは「公開面に無い」ことだけで、「その状態が使われていない」ことではない。**

### この source が establish しないこと

- **網羅ではない。** 126 件しか無く、承認済み全件ではない。
- **正確でもない**（`approved` の意味・`cal-1-0` の日付）。**authority が公開しているからといって、
  中身が自動的に正しいわけではない** ——**我々自身の自己申告について繰り返し学んだことが、
  相手側にも当てはまる。**
- **次に見るときは取り直す。** 上の数はすべて 2026-09-20 の取得である。

## 1.103 リストの自動フッタは資格の規則である —— 5 つの `rounds/` file に逐語で在り、一度も読まれていなかった（2026-09-21）

**取得**: `license-review` / `license-discuss` の 2026-August・2026-September アーカイブ
（取得時刻 **2026-09-21T17:53Z / 17:54Z**）。**ブラウザ相当 UA。**

### 規則そのもの（逐語・全メッセージに自動付加される）

> *"The opinions expressed in this email are those of the sender and **not necessarily those of
> the Open Source Initiative**. **Communication from the Open Source Initiative will be sent
> from an opensource.org email address.**"*

**これは我々が既に持っていた。** `rounds/` の 5 file（Perens 返信 / Sado 引用 / OpenMDW スレッド /
Dolan 受領 ×2）に逐語で入っている。**引用の一部として保存され、規則として読まれていなかった。**
**理事会議事録のときと同じ形である**（#186）——**持っているが、その目的で読んでいない。**

### 効果 1 —— **既定は「個人の意見」であり、それは我々に有利な引用にも等しく掛かる**

ドシエは、リスト上の発言を「委員会が述べた」「OSI が述べた」と読む場面で重み付けしてきた。
**リスト自身の既定はその逆である。** B1 を支える *"we do not require review by a lawyer,
only recommend it"* も、R2〜R5 の 4 規則も、**既定では発言者個人の意見**である。

**⚠ ただしフッタは boilerplate なので、個々のメッセージについての証拠としては弱い。**
**既定を定めるだけであり、明示の自己表示はこれを上書きする。** 実際:

| 発言 | 明示の資格表示 | 既定に留まるか |
|---|---|---|
| Chestek 氏 2024-12「recommended, not a blocker」| **在り** —— *"Chair, Licensing Committee, Open Source Initiative"* と署名 | 上書きされる |
| McCoy 氏 2026-08-28「two-month review cycle」| **在り** —— *"[on behalf of the Licensing Committee]"*（**2026-09-21 に原文で確認。我々の挿入ではない**） | 上書きされる |
| Piana 氏 2024-12「OSI requires prior review by a lawyer」| **在り（逆向き）** —— *"in his own capacity"* | 個人 |
| R2〜R5（Chestek 氏 2025-02 / 2026-04）| **未確認** | **既定のまま = 個人の意見** |

**したがって R2〜R5 を「委員会が述べた規則」と呼ぶのは、確認していない資格に依っている。**
`review-corpus.md` §1.67 の見出しは「**委員会が実際に述べた**規則」と読める ——
**正しくは「委員長が述べた規則」であり、そのうち資格表示を確認したものは無い。**

### 効果 2 —— **B14 の通知だけが、3 つの制度的マーカーを揃えている（我々に不利）**

**2026-09-09 の moderator 通知を、リスト自身の慣習で測ると:**

1. **`nick.vidal at opensource.org` から送られている** ——フッタが「OSI からの連絡はこの
   アドレスから送られる」と名指ししている当のアドレス。
2. **署名が "OSI Moderators"** ——個人名ではない。
3. **🔴 そのフッタが付いていない。** 両リストの当該メッセージで **0 件**
   （2026-09-21 に原典を取り直して確認。**保存時の欠落ではない**）。
   **対照**: 同じ主題への Perens 氏の返信（同日・`bruce at perens.com`）には **1 件在る。**

**つまり、我々の corpus 全体で唯一、「発言者個人の意見である」という既定が働いていない
メッセージが、我々に最も不利なメッセージである。**

### ⚠ 逆側（同じ重さで）

- **「OSI からの連絡」は「OSI の決定」ではない。** 通知は moderation の運用と CoC 改定予告で
  あって理事会決議ではなく、**ACD-1.0 についての立場は依然 1 語も述べていない。**
  `CLAUDE.md` §7 の「組織の立場は依然不明」は**そのまま生きる** ——変わるのは
  「moderator の行為は一個人の行為ではない」という点だけである。
- **フッタの規則は必要条件であって十分条件ではない。** *"will be sent from an opensource.org
  email address"* は、そのアドレスからの全てが公式だとは述べていない。
- **アドレスから資格を推論してはならない。** McCoy 氏は**法律事務所のアドレス**から
  *"[on behalf of the Licensing Committee]"* と署名している ——**1 通の中で、アドレスの慣習と
  自己表示が逆を向いている。** process ページの「個人資格なら非 OSI アドレスを使うことが
  期待される」は、**実務では守られていない場合がある。**
- **有利な側**: 既定が「個人の意見」であることは、**我々に不利な発言にも等しく掛かる** ——
  McCoy 氏の *"waivers/disclaimers of IP rights は自力では難しい"*（B1 に不利・§1.51）も、
  Landley 氏の #84 も、既定では個人の意見である。**この規則は片側だけを削らない。**
