---
file: LICENSES/ACD-1.4-CLARITY-TRIAL.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-04
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt (試作の対象・この file は草案を上書きしない) / LICENSES/ACD-OSI-BOTTLENECKS.md (B3 / B13) / LICENSES/ACD-1.4-CHANGELIST.md (採用した変更の記録先)
---

# ACD-1.4 草案の明瞭性の試作 —— 法的効果を保ったまま、言い直しの族と読みの分岐を減らせるか

**目的（2026-11-04・オーナー経由の外部 AI の依頼）**: 許諾の範囲・権利主体・法的効果を保ったまま、
重複する条と読みの分岐を減らす。OSI の新規ライセンスの承認基準のうち **基準 3（曖昧さが実質的影響を持たない）**
と **基準 4（文法的・構文的に明晰）**（`OSI-APPROVAL-PLAN.md` §3.2・原典は `ACD-1.0.review-rules.md` §1.70）に
直接当たる作業である。**語数を減らすこと自体は目的にしない** —— B3 は 2026-09-09 に「縮められるが答えきれない」と
結論済みで（`ACD-OSI-BOTTLENECKS.md` B3）、その後の版は正確さのために語を足してきた。

**規則**:
- **草案（`ACD-1.4-DRAFT.txt`）を直接上書きしない。** 試作はこの file に書き、採用が決まったものだけを草案と
  `ACD-1.4-CHANGELIST.md` に反映する。
- **採用の条件は 2 つ**: (1) 条ごとに、許諾の範囲・主体・条件・除外・法域ごとの結果が変わらないことを説明できる、
  (2) 敵対的な反例（元では許され試作では許されない利用・読み、またはその逆）が出ない。**どちらかを満たせない案は採らず、残余リスクを書く。**
- **法的効果を変える案は「新規版候補」として扱い、この file では採用しない。**
- **分担**（3 セッション）: bb = 候補表（手順 1〜3）と反例探し / 25 = 試作文と Before/After の効果対照（手順 4〜5）/
  5a = 道具（6 語以上一致の全数抽出・KPI・効果を運ぶ語の条ごとの差分・採用後の Check）。

## 1. 既に済んでいるもの（手順 1・除外する）

- **語数の削減**: 2026-09-09 に置換文 7 件・約 350 語・gap の損失ゼロまで起草して測った（`ACD-1.1-CHANGELIST.md` §2.5〜§2.8）。
  1.1 で一部（§2.5 の圧縮など）を適用し、**1.2 で §15.5 / §15.6 を一字一句戻した**（E24 / E25 —— 削った結果、両 canon を止めていた）。
  **「削る → 正確さのために戻す」は一度起きている。** 今回はこの経路を繰り返さない。
- **附属文書への移出（構造変更）**: 測って否定済み（`ACD-1.1-CHANGELIST.md` §2.7）。
- **短い入口（B13）**: 本文の外の緩和で、継続中（`ACD-OSI-BOTTLENECKS.md` B13）。
- **2026-11-02〜03 の掃引**: 文法上の性質（E50〜E53）、同じ集合を別の語で呼ぶ（E54〜E58）、見出し（E59）、
  「this Section」の指す先（E57）、*here* の全 14 件（clean）は既に当てた。**この file はそれを繰り返さない。**

## 2. 構造（手順 2・1.4 草案 2026-11-04 時点・道具で導出）

**ベースライン**: 80 項・本文 5,049 語（見出しと前文を除く・草案冒頭の申告 5,547 語は数え方が違う —— 権威は草案冒頭と Check 468）。
条番号への相互参照 91 か所 / 理由・案内・念押しの文 40 文・1,234 語 / 法域で分岐する言い回し 35 か所 / **受領者への義務の語 0 か所**。
型と主体は機械的な分類で、**読んで確かめたものではない**（列「型」は条の主な働きの目安）。

| 条 | 語 | 型 | 主体 | 法域分岐 | 相互参照 | 理由・案内・念押しの文 |
|---|--:|---|---|:-:|--:|--:|
| 1.1 | 9 | 定義 | — |  | 1 |  |
| 1.2 | 67 | 定義 | — | ○ | 0 |  |
| 1.3 | 51 | 定義 | Dedicator |  | 0 |  |
| 1.4 | 61 | 定義 | Dedicator・person |  | 0 |  |
| 1.5 | 109 | 定義 | Dedicator | ○ | 4 | 2 |
| 1.6 | 67 | 定義 | You・person |  | 0 | 1 |
| 1.7 | 61 | 定義 | — |  | 0 |  |
| 1.8 | 31 | 定義 | person |  | 0 |  |
| 1.9 | 72 | 定義 | Dedicator・person |  | 0 |  |
| 1.10 | 74 | 定義 | — |  | 0 |  |
| 2.1 | 16 | 宣言 | — |  | 0 |  |
| 2.2 | 51 | 限定・念押し | Dedicator |  | 0 |  |
| 2.3 | 39 | 限定・念押し | You |  | 0 |  |
| 2.4 | 54 | 許諾・不行使の約束 | — |  | 2 | 1 |
| 2.5 | 71 | 限定・念押し | Dedicator | ○ | 0 |  |
| 2.6 | 151 | 限定・念押し | Dedicator・You・person |  | 2 | 1 |
| 2.7 | 49 | 限定・念押し | Dedicator・person |  | 1 | 1 |
| 2.8 | 99 | 許諾・不行使の約束 | Dedicator・person | ○ | 2 | 1 |
| 2.9 | 57 | 宣言 | Dedicator・person |  | 1 |  |
| 3.1 | 42 | 放棄 | Dedicator | ○ | 0 |  |
| 3.2 | 44 | 放棄 | — |  | 1 |  |
| 3.3 | 25 | 放棄 | Dedicator | ○ | 0 |  |
| 4.1 | 26 | 許諾 | Dedicator・You |  | 0 |  |
| 4.2 | 74 | 宣言 | — |  | 1 |  |
| 4.3 | 74 | 許諾 | — | ○ | 1 | 2 |
| 4.4 | 56 | 許諾 | You | ○ | 4 |  |
| 4.5 | 65 | 限定・念押し | You |  | 0 | 1 |
| 4.6 | 88 | 不行使の約束 | Dedicator・You・person |  | 4 | 2 |
| 5.1 | 63 | 不行使の約束 | Dedicator・You・person |  | 0 |  |
| 5.2 | 168 | 許諾・不行使の約束 | Dedicator・You・person |  | 3 | 1 |
| 5.3 | 73 | 不行使の約束 | Dedicator・You | ○ | 2 |  |
| 6.1 | 39 | 限定・念押し | Dedicator・person |  | 1 |  |
| 6.2 | 94 | 限定・念押し | Dedicator |  | 2 | 1 |
| 6.3 | 86 | 限定・念押し | Dedicator・person | ○ | 1 |  |
| 6.4 | 79 | 限定・念押し | Dedicator・You |  | 1 | 1 |
| 6.5 | 56 | 限定・念押し | — |  | 2 | 2 |
| 7.1 | 40 | 宣言 | — |  | 1 |  |
| 7.2 | 38 | 宣言 | Dedicator・You |  | 1 |  |
| 8.1 | 80 | 許諾 | Dedicator・You |  | 0 |  |
| 8.2 | 83 | 限定・念押し | Dedicator・You・person |  | 2 | 2 |
| 8.3 | 60 | 宣言 | Dedicator |  | 0 | 1 |
| 8.4 | 276 | 許諾 | Dedicator・You |  | 8 | 2 |
| 8.5 | 83 | 許諾 | Dedicator・person |  | 3 | 1 |
| 8.6 | 133 | 許諾・不行使の約束・放棄 | Dedicator・You・person | ○ | 5 |  |
| 9.1 | 22 | 宣言 | — |  | 0 |  |
| 9.2 | 66 | 限定・念押し | Dedicator |  | 2 |  |
| 9.3 | 35 | 限定・念押し | You | ○ | 0 |  |
| 9.4 | 60 | 限定・念押し | You・person |  | 3 | 1 |
| 10.1 | 16 | 限定・念押し | You |  | 0 | 1 |
| 10.2 | 35 | 限定・念押し | You |  | 0 |  |
| 10.3 | 55 | 限定・念押し | Dedicator |  | 0 | 1 |
| 10.4 | 33 | 限定・念押し | You |  | 0 | 1 |
| 10.5 | 35 | 限定・念押し | — |  | 3 | 2 |
| 11.1 | 79 | 許諾 | Dedicator・You・person |  | 3 |  |
| 11.2 | 29 | 宣言 | Dedicator・You |  | 0 | 1 |
| 11.3 | 66 | 限定・念押し | Dedicator・You |  | 1 | 2 |
| 11.4 | 184 | 許諾・不行使の約束 | Dedicator・You・person | ○ | 6 | 2 |
| 12.1 | 24 | 放棄 | Dedicator | ○ | 0 |  |
| 12.2 | 86 | 不行使の約束 | Dedicator・You・person | ○ | 2 |  |
| 12.3 | 49 | 不行使の約束 | Dedicator |  | 2 |  |
| 12.4 | 80 | 不行使の約束 | Dedicator・person | ○ | 1 | 1 |
| 12.5 | 26 | 不行使の約束 | — |  | 2 |  |
| 12.6 | 24 | 限定・念押し | — | ○ | 2 |  |
| 13.1 | 38 | 無保証・責任 | — |  | 0 |  |
| 13.2 | 46 | 無保証・責任 | — |  | 0 |  |
| 13.3 | 18 | 無保証・責任 | Dedicator |  | 0 |  |
| 14.1 | 59 | 無保証・責任 | — |  | 0 |  |
| 14.2 | 33 | 無保証・責任 | — |  | 1 |  |
| 15.1 | 44 | 解釈 | You |  | 0 |  |
| 15.2 | 56 | 解釈 | — | ○ | 0 |  |
| 15.3 | 30 | 解釈 | — | ○ | 0 | 1 |
| 15.4 | 23 | 解釈 | — |  | 0 |  |
| 15.5 | 49 | 解釈 | person |  | 0 |  |
| 15.6 | 28 | 解釈 | — |  | 0 |  |
| 16.1 | 93 | 文書の扱い | — |  | 1 | 1 |
| 16.2 | 59 | 文書の扱い | Dedicator |  | 0 |  |
| 16.3 | 43 | 文書の扱い | person | ○ | 0 |  |
| 16.4 | 213 | 文書の扱い | Steward |  | 3 | 1 |
| 16.5 | 43 | 文書の扱い | Steward・person |  | 1 |  |
| 16.6 | 36 | 文書の扱い | — |  | 2 |  |

## 3. 候補（手順 3）

### F0. 5a の全数抽出（6 語以上一致・58 族）の振り分け —— 言い直しか、並行起草の定型句か

**道具**: 5a の `measure_clause_overlap.py`（main f42a9b76 の 1.4 草案・79 箇所・関わる条 43・族 58）。
**58 族の大半は言い直しではなく、並行起草の定型句である** —— 同じ働きの条が同じ語で書かれていることは、
今日の E54〜E58 が示したとおり**食い違いを防ぐ側**にある（直し方そのものが「語をそろえる」だった）。

| 振り分け | 例（5a の族）| 扱い |
|---|---|---|
| **言い直し**（同じ主張を複数の条で繰り返す）| 「You are not required to determine」（§4.4 / §8.6 / §9.3 / §12.2）/ 「Section 10.1 is unaffected by it」（§10.5 / §11.3 / §11.4）/ 「Section 13.2 states the corresponding absence of warranty」（§2.7 / §8.5）| **まとめ候補**（F1 / F2 / F4）|
| **並行起草の定型句**（別々の条が別々の効果を、同じ語で述べる）| 「To the fullest extent permitted by the law of each jurisdiction」（§3.1 / §12.1 / §14.1）/ 「authorise or assist any other person to assert」（§5.1 / §5.2 / §8.6 —— §5.2(d) は SELF-AUDIT §3s でそろえた）/ 承継人の列挙（§2.8 / §5.3 / §12.4）/ 許諾の性質の列挙（§4.1 / §8.1）/ §1.7 の成果物の列挙（§6.4 / §8.4 —— E47 / E56 でそろえた）/ 「in respect of the Work」（§2.8 / §10.4 / §11.4 / §15.1 —— E9 / E44 / E48 / E20 の限定）| **残す**。まとめると、各条が自分の効果を述べなくなり、片方だけ変わる余地が戻る |


**4 つの型に分けた。** 各候補の「経緯」は、その文がどの版で、どの errata や指摘を閉じるために足されたかで、
**まとめるとその誤読が戻る危険がある**ので、反例の第一の材料になる。

### F1. 「You は判定しなくてよい / 許可はその問いに依存しない」の言い直し（4 か所・25 の指摘）

| 条 | 文 | 在る版 | 経緯 |
|---|---|---|---|
| §4.4 | *"You are not required to determine whether Section 3 is effective in any jurisdiction, and no permission granted here depends on that question or on how it is answered."* | 1.0〜 | 起草時。§4 が §3 の失敗を待たない並行の許諾であることの念押し（E11 で §4.4 の第 2 文は 1.1 に変わった）|
| §8.6 | *"… nothing permitted by this Dedication depends on that question or on how it is answered."* | 1.2〜（1.4 で文言をそろえた）| **E26**（法域で分岐する 4 条のうち 2 条だけが「どちらでも同じ」と読者に述べていた）を閉じるために足された |
| §9.3 | *"You are not required to determine which parts of the Work are Machine-Generated Material. No permission granted here depends on that question, or on how any jurisdiction answers it, or on whether the answer changes."* | 1.0〜 | 起草時。**問いが法域の問いだけでなく事実の問い（どの部分が機械生成か）でもある**点で他の 3 か所と違う |
| §12.2 | *"You are not required to determine which of Section 12.1 and this Section applies in a jurisdiction, and nothing permitted by this Dedication depends on that question or on how it is answered."* | 1.2〜 | **E26** と同じ |

**反例の種**: (i) E26 の論点は「1 条だけを読む読者」で、1 か所へまとめると、その読者が見る場所から念押しが消える（E19 / E21 と同じ「読み順の欠陥」—— #151 が記録する、単独の条で止まる読者を誤らせないための相互参照）。
(ii) §9.3 は事実の問いを含むので、「法域の答え」だけを語る一般則では覆いきれない。
(iii) 一般則の主語を「this Dedication」にすると、§16（文書の扱い）にまで「判定しなくてよい」が及ぶ読みが立つ。

### F2. 「条件ではない / §10.1 は影響を受けない」の念押し（25 の指摘）

| 条 | 文 | 在る版 | 経緯 |
|---|---|---|---|
| §10.1 | *"This Dedication imposes no condition, obligation, restriction, or requirement upon You in respect of the Work."* | 1.0〜 | 一般則そのもの |
| §10.5 | *"Nothing in Section 16 is a condition upon Your use of the Work, and Section 10.1 is unaffected by it."* | 1.0〜 | §16（文書の扱い）について |
| §11.3 | *"This Section states a limit of the Dedication's reach; it is not a condition upon You, and Section 10.1 is unaffected by it."* | 1.0〜 | 起草時 |
| §11.4 | *"… this Section states a limit of reach, it is not a condition upon You, and Section 10.1 is unaffected by it."* | 1.0〜 | 起草時 |
| §5.2 末 | *"This is a covenant about the Dedicator's own conduct and not a grant: Section 11.4 is unaffected …"* | 1.2〜 | **E31** を閉じるために足した (d) の説明 |
| §4.3 / §8.2 | *"subject to no condition of any kind"* / *"subject to no condition and are not terminable"* | 1.0〜 | 許諾ごとの無条件の宣言 |

**反例の種**: (i) **SELF-AUDIT §3r** —— 1.1 が §16.4 に足した re-encoding の但し書きは、隣の翻訳の但し書きと違ってこの念押しを持たず、
「使用への条件」と読まれうる欠陥になった。**念押しを各所に置く書き方は、付け忘れた 1 か所を欠陥にする**（E9 も同じ形）。
一般則 1 本にまとめれば、この族の欠陥が構造的に起きなくなる ——**これはまとめる側の最強の論拠**。
(ii) 逆側: 一般則が「限界を述べる条」「文書の但し書き」をすべて名指せないと、名指されない 1 か所が条件と読まれる（*expressio unius*）。
(iii) §4.3 / §8.2 の「無条件」は許諾の性質で、念押しではない。まとめの対象から外す。

### F3. 理由・目的を述べる文 —— 反対解釈の分岐を自分で作る（bb の指摘）

**理由を書くと、「その理由が当たらない場面では結論も当たらない」という読みの余地が生まれる。**

| 条 | 文（語数）| 在る版 | 生む分岐 |
|---|---|---|---|
| §2.8 | *"This is stated expressly because Sections 5.3 and 12.4 say as much … silence here would invite the argument …"*（43）| 1.0〜 | 明示していない他の場所の沈黙は「止まる」意味だ、という読み |
| §6.5 第 2 文 | *"It is stated expressly because silence on this subject has proved ambiguous in practice …"*（40）| 1.0〜 | 同上（沈黙の評価を本文が自分で下している）|
| §8.2 第 2 文 | *"A retaliation provision operates as a condition … so the absence follows from the structure … rather than from a policy preference …"*（35）| 1.2〜 | 構造が変われば（条件が足されれば）報復終了が入りうる、という読み |
| §8.3 | *"… leaves the recipient exposed, because software cannot be practised without practising whatever patent claims it embodies."*（26）| 1.0〜 | ソフトウェアでない Work では特許の留保が許される、という読み |
| §8.4 第 2 文 | *"The grant is necessary because Covered Rights exclude patent rights (Section 1.5), so Section 6.4 alone would leave …"*（50）| 1.0〜 | 必要性が無い場面では §8.4 は狭く読める、という読み |
| §10.4 | *"… contains no termination provision and no revival provision, because it contains nothing that You could breach."*（23）| 1.1〜 | **違反しうるものが見つかれば終了できる**、という読み |
| §11.3 | *"… is outside what this Dedication reaches, because it was never the Dedicator's to permit …"*（34 の一部）| 1.0〜 | Dedicator が許せる場合（自分の名の使用）には範囲内、という読み |
| §11.4 | *"This matters here because a work meant to be learned from is often data about people …"*（28）| 1.0〜 | 人についてのデータでない Work では §11.4 の限界は効かない、という読み（弱い）|
| §12.4 | *"This is stated expressly because Moral Rights outlive the author in many jurisdictions …"*（38）| 1.0〜 | 人格権が作者の死で消える法域では §12.4 は働かない、という読み（弱い）|

**反例の種**: 理由の文は**解釈の材料**でもある（目的に照らした読み）。消すと、§15.1（許諾を広く読む）だけが残る。
**消して失うものと、残して生むものを条ごとに比べる** —— 例えば §8.4 第 2 文は射程の説明として審査者に役立っており（#16 の費用の議論）、
§10.4 の *because* は反対解釈の害が具体的に立つ。

### F4. 他の条を案内するだけの文（bb の指摘）

| 条 | 文（語数）| 在る版 |
|---|---|---|
| §2.7 / §8.5 | *"Section 13.2 states the corresponding absence of warranty."*（8 × 2）| 1.0〜 |
| §4.6 | *"Section 4.5 concerns the terms You may add."*（8）| 1.0〜 |
| §6.5 第 1 文 | *"Section 6 states expressly what Sections 3 to 5 and 8 would in any event permit."*（16）| 1.3〜（**E36** を閉じるために "and 8" を足した）|
| §9.4 第 2 文 | *"Section 10 governs whether You need say so, and Section 11.3 explains why …"*（27）| 1.0〜 |
| §10.5 第 1 文 | *"Section 16 concerns the text of this Dedication as a document, and not the Work."*（15）| 1.0〜 |
| §11.4 末の前半 | *"Section 2.7 states the general principle and Section 13.2 the corresponding absence of warranty"* | 1.0〜 |
| §1.5 | 除外の各項に *"which Section N addresses"*（47）| 1.2〜 / 1.4 |

**反例の種**: 案内の文は権利義務を足さないように見えるが、**§6.5 第 1 文は E36 で中身が争われた**（「§3〜§5 だけ」と書いて特許を落としていた）。
案内の文も、間違えれば欠陥になる。**消せば間違える場所が減る**が、§15.1 と並んで解釈の材料になっている文がある。

## 4. 試作と効果の対照（手順 4〜5・25）

（25 が書き足す。条ごとに Before / After、許諾の範囲・主体・条件・除外・法域ごとの結果の対照）

## 5. 反例テスト（手順 6・bb）

**試作を見る前に、当てる反例を先に書いておく**（2026-11-04）—— 試作を読んでから反例を考えると、試作の書き方に引きずられる。
試作が来たら、5a の「効果を運ぶ語」の差分と合わせて、下の各行を 1 つずつ当てる。**1 つでも成立すれば、その試作は採らない。**

### 5.1 先に登録した反例（候補ごと）

| # | 候補 | 反例（元では守られ、試作では守られない読み・利用 —— またはその逆）| 確かめ方 |
|---|---|---|---|
| CE1 | F2 を §10.1 の一般則へまとめる | **§11.3 の限界を越えた行為（Dedicator が推薦したと偽る）をした者は、§4 の許諾まで失うか。** 元は §11.3 自身が「条件ではない・§10.1 は影響を受けない」と述べるので、許諾は失われない。一般則が「限界を述べる条は条件ではない」とだけ言うと、**限界の外の行為が限界の内の許諾に影響しない**ことまで言えているかが問われる | 一般則の文が「限界の外の行為は、どの許諾にも影響しない」を含むか |
| CE2 | F2 | **§16.4 の 2 つの但し書き（翻訳・re-encoding）が、Work の使用への条件と読まれるか**（SELF-AUDIT §3r の再発）。元は §16.4 末尾と §10.5 の 2 か所が断っている | 一般則が §16 の但し書きを名指すか、§10.5 を残すか |
| CE3 | F2 | **§2.6 の識別の約束（Dedicator の義務）が、You の条件と読まれるか** —— 主語は Dedicator で、元も念押しは持たない | 一般則の主語・射程が You に限られているか |
| CE4 | F2 | **逆向き**: 一般則を足した結果、§4.3 / §8.2 の「無条件の許諾」の宣言が冗長になり、削られると「条件の不在」が許諾ごとに言えなくなるか | §4.3 / §8.2 は許諾の性質の宣言として残す（F2 の (iii)）|
| CE5 | F1 を 1 か所へまとめる | **§9.3 の問い（どの部分が機械生成か）は事実の問いで、法域の答えだけを語る一般則に入らない** —— 一般則の後、機械生成かどうかを判定しないまま使った者の許可が残るか | 一般則が「事実の問い」と「法域の答え」の両方を覆うか |
| CE6 | F1 | **1 条だけを読む読者**（E26 の論点）—— §12.2 だけを読んだ人が、日本で §12.1 と §12.2 のどちらが働くかを判定しなければならないと読むか | 各条に一般則への指し先が残るか（指し先だけなら語は減る）|
| CE7 | F1 | **一般則の主語を「this Dedication」にすると、§16（文書の扱い）について「判定しなくてよい」が及ぶ**読み —— 翻訳の正文や改変版の名称について「判定しなくてよい」は誤り | 一般則の射程が許可（permission）に限られているか |
| CE8 | F3: §8.3 の理由の文を削る | **削れない**: 第 3 文 *"Any reading … that would produce **that result** is to be rejected"* の *that result* は、第 2 文（理由の文）の「受領者が露出したままになる」を指している。**理由の文が操作条項の指示語の先として効果を運んでいる。** 一方で第 2 文の *"because software cannot be practised …"* は、**ソフトウェアでない Work（データセット・モデル）では特許の留保が許される**という反対解釈を生む | 試作が第 3 文に結果を書き込む形（例: *"Any reading … that gives away a Covered Right while withholding a patent right is to be rejected"*）なら、指示語の先を失わずに *software* の反対解釈を消せる。**削るだけの試作は CE8 で不成立** |
| CE9 | F3: §10.4 の *because* を削る | 元の *"because it contains nothing that You could breach"* は「違反しうるものが見つかれば終了できる」という反対解釈を生む。**削った後に失われる効果は無いはず** —— 第 1 文 *"No permission granted by this Dedication terminates for any reason"* が終了の不在を自分で述べている | 第 1 文が残っているか / 「revival provision が無い」の意味が理由なしで通るか |
| CE10 | F3: §2.8・§12.4 の *"This is stated expressly because …"* を削る | 削っても拘束の範囲は変わらないはず。ただし理由の文が**承継人の範囲の解釈の材料**（相続・倒産・売却の場面を名指す）になっていないか | 理由の文の中に、操作条項に無い場面の列挙が無いか（あれば、それは効果を運んでいる）|
| CE11 | F3: §6.5 第 2 文 | **削らない側に置く**: 「機械が判定できない許諾は許諾ではない」は gap の論拠そのもので、ドシエ（提出参考資料・想定問答・register B10）が依拠している。削ると、審査者に示す「なぜ明示が要るか」の本文側の根拠が消える | —（採らない候補として記録）|
| CE12 | F4 の案内の文を削る | §6.5 第 1 文は E36 で中身が争われた（「§3〜§5 だけ」と書いて特許を落とした）。**案内の文でも、言い過ぎれば欠陥になり、言い足りなければ別の欠陥になる** —— 削れば間違える場所が減る。逆に、§9.4 第 2 文のように **§10 と §11.3 の役割分担を述べる文**は、消すと §9.4 の射程が読み手に届かない | 各文について「消すと、どの条の射程が読み手から見えなくなるか」を 1 件ずつ |

### 5.2 試作に当てた結果

（25 の試作と 5a の差分が入ったら、CE1〜CE12 を当てて、成立 / 不成立を書く）

## 6. KPI（5a の道具で導出）

| 指標 | Before（1.4 草案）| After |
|---|---|---|
| 項の数 | 80 | — |
| 本文の語数（見出し・前文を除く）| 5,049 | — |
| 理由・案内・念押しの文 | 40 文・1,234 語 | — |
| 族の数（6 語以上一致・5a の道具）| 58（言い直し 3 族 / ほかは並行起草の定型句）| — |
| 意味の異なる解釈候補 | F3 の 9 件 + F1 / F2 の反例の種 | — |
| 反例テスト | — | 通過 / 不成立 |
| 効果の保存を説明できた条 | — | — |

**この表の数字は、採用の根拠ではない。** 依頼の条件どおり、語数の削減・CI の成功・文書の追加を承認確率の向上と扱わない。
