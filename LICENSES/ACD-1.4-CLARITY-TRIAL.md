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

**結論を先に書く（2026-11-04 時点）**: 試作した 1 族（F2）は**反例が 3 つ立ったので採らない**。
検討だけで退けた族が 4 つ（F1・成果物の列挙・§10.4 の *because*・5a が渡した §12 の問い）。
**生きている候補は 1 件（§2.8 の理由の文・−41 語）で、bb の反例テストへ渡す**（§4.6）。
採用した変更はまだ無い。草案（`ACD-1.4-DRAFT.txt`）は触っていない。

### 4.1 F2「条件ではない」を §10.5 の一般則へまとめる —— 試作 (b)・採らない

**試作 (b)**（main f42a9b76 の草案に当てた。5a の比較モードで測定済み）:

```
  10.5 Section 16 concerns the text of this Dedication as a document, and not
       the Work. Nothing in Section 16, and no statement in this Dedication of
       what it does not reach or grant, is a condition upon Your use of the
       Work, and Section 10.1 is unaffected by them.
```

あわせて §11.1 の末文（*"Where Section 16 speaks of the name … (Section 10.5)."*）と、§11.3 の末文、
§11.4 の末尾 *"; this Section states a limit of reach, it is not a condition upon You, and Section 10.1 is unaffected by it"* を消した。

**5a の測定**: 語 5,049 → 4,977（−72）/ 6 語以上の重複 79 → 72 / 族 58 → 53 / 項 80 のまま。
減った効果の語は §11.1・§11.3・§11.4 の *you / not / upon*（§11.1 は *where / nothing*）で、すべて消した断りの文。

**条ごとの対照**（一般則が消した文の働きを引き取れるか）:

| 条 | Before の働き | (b) で引き取る先 | 範囲・主体・条件・除外・法域 | 判定 |
|---|---|---|---|---|
| §10.5 | §16 は Work の使用への条件ではない | 同じ文に「限界を述べる文」を足す | 変わらない（足しただけ）| — |
| §11.1 末文 | §11.1 を先に読む読者に、§16 の名前の規定は Work に何も求めないと**その場で**告げる | §10.5 | 変わらない | **反例 1**（下）|
| §11.3 末文 | 虚偽の関与表示の条を「条件ではない」と**その場で**言い切る | §10.5（§11.3 が「reach しない文」に分類されれば）| 変わらない | **反例 2** |
| §11.4 末尾 | 個人データ等の限界を「条件ではない」と言い切る | §10.5（*"It reaches nothing else"* が自分を分類する）| 変わらない | 反例 2 の対称で残す |

**反例 1 —— §11.1 の末文を消すと errata E7 が戻る。** その文は 1.1 で E7（`against.md` #45）を閉じるために足した前方参照で、
問題は「§11.1（名前に権利を与えない）を先に読む読者が、§16 は §11 が与えなかったものを求めていると読む」読み順だった。
和解の文（§10.5・§16.6）は 1.0 から在ったのに、**読者が衝突に出会う場所に無かった**ことが欠陥だった。
一般則へ寄せると、和解が再び衝突の場所から離れる。**試作 (b) を作った時点でこの経緯を確かめていなかった**（bb の F1 (i) と同じ「1 条だけを読む読者」の論点）。

**反例 2 —— §11.3 は局所の断りが要る（5a の指摘）。** §11.3 は BSD-3-Clause の第 3 項（推奨表示の禁止）に似ており、
審査者が条件と読みやすい条である。試作では「§11.3 は reach しない文だ」と分類して初めて一般則に入り、
冒頭の *"does not make a false statement true"* がその分類に当たるかは境界にある。**効果は同じでも審査者に推論を 1 段挟ませる**（B13 に逆向き）。
§11.3 に断りを残すなら、**SELF-AUDIT §3r の形（並ぶ 2 つで片方だけが断る）を避けるため §11.4 にも残す**ことになる。

**反例 3 —— 一般則の語を §10.1 にそろえると、別の条が狭く読める。** 5a は一般則を *"upon Your use of the Work"* ではなく
*"upon You in respect of the Work"*（§10.1 と同じ語）にすれば救いの句に頼らずに済むと提案した。
しかしこの本文では *use of the Work* が**総称**として働いている —— §5.1 の covenant は *"against You in respect of any use of the Work"*、
§3.2 は *"arising from any use of the Work"*、§5.2(d) は *"in respect of any use of the Work that this Dedication permits"*。
§10.5 だけを *in respect of* へ移すと、「本文が全部を言いたいときは *in respect of* と書く。*use* と書いた条は使用だけだ」という対比が立ち、
**§5.1 の covenant が頒布・改変に及ばないという読みを本文自身が支えてしまう。** 不利な方向の反例なので、語はそろえない。

**そして、まとめる側の最強の論拠（bb の F2 反例の種 (i)）は SELF-AUDIT §3r 自身が弱めている。**
§3r の欠陥（§16.4 の re-encoding の但し書きが条件と読まれうる）は、**§16 全体について既に一般則（§10.5・§16.6）が在る場所で起きた**。
一般則は、具体的な但し書きが条件のように読まれることを止めなかった。§3r の直し方も一般則ではなく、**その場の断り**だった。
特定の文と一般の文が衝突するとき特定が優先するという読みの規則がある以上、**一般則を足しても「付け忘れた 1 か所」の欠陥類は構造的には消えない。**

**残るもの**: 反例 1〜3 を避けると、§11.1 は変えず、§11.3・§11.4 は短い断りを残すことになり、
得られるのは §11.3 の −5 語・§11.4 の −3 語と一般則の +15 語（差し引き +7 語）、それに *limit of the Dedication's reach* / *limit of reach* の綴りの統一だけになる。
**読みの分岐は減らない**（一般則が覆う先はすべて §10.1 が既に覆っている）。**採らない。**

### 4.2 F1「判定しなくてよい」を 1 か所へまとめる —— 検討して採らない

一般則にすると**偽の文になる**。§4.4・§8.6・§9.3・§12.2 の念押しは、それぞれ**特定の 2 つの足場の組**（§3 と §4 / 特許の 2 経路 / 機械生成か否か / §12.1 と §12.2）について
「どちらでも許可は同じ」と述べており、各組についてはそれが真である。
しかし「この Dedication の許可は、どの足場が有効かに依存しない」という一般則は、**すべての足場が無効な法域**（§3 の放棄も §4 の許諾も効かない仮定の法域）では偽である ——
許可は少なくとも 1 つの足場の有効性に依存している。一般則を真にするには組を列挙する必要があり、列挙は E46 / E49 と同じ「列挙の漏れ」の危険を戻す。
加えて bb の反例の種 (i)〜(iii)（E26 の読み順・§9.3 は事実の問い・主語の射程）がそのまま当たる。5a も同意（2026-11-04）。

### 4.3 §1.7 の成果物の列挙（§6.4 / §8.4）を定義語にまとめる —— 検討して採らない

bb の F0 が「並行起草の定型句」として残す側に分けたもの。理由を 2 つ足す。
(1) §8.4 の動詞列（1.0 では §8.1）*"making, having made, using, offering to sell, selling, importing, or otherwise transferring"* は特許の実施行為で、
§1.7 の *"the making, distribution, and use"* より広い。重複ではない。
(2) 共通部分 *"model, parameter set, weight, embedding, or output"* を新しい定義語にすると、§1.7 が「それらを作ること」を Computational Use に含めているため、
その定義語を Computational Use で定義すると**循環する**。提出参考資料 §4c は「定義の依存に悪い循環が無い」ことを審査者が確かめられる主張として示しているので、それを崩す。
語数も定義に約 20 語・4 か所で約 24 語の削減で、ほぼ 0。

### 4.4 F3 §10.4 の *because* —— 検討して採らない

§10.4 の *"because it contains nothing that You could breach"* を並列の主張（*"…no revival provision, and nothing that You could breach"*・−3 語）に変える案を検討した。
反対解釈（違反しうるものが見つかれば終了できる）は、**同じ条の第 1 文 *"No permission granted by this Dedication terminates for any reason"* が無条件なので立たない** ——
理由の前提が崩れても、結論は第 1 文が独立に支える。逆に *because* は、終了条項の不在が方針の好みではなく**構造から来る**ことを述べる形で、
1.2 が §8.2 を同じ形へ直した（`against.md` #265 (b)・*"deliberate"* が Chestek 氏の *"intentional"* への懸念に当たったため）のと揃っている。
想定問答（`review-responses-clauses.md` の set-A / set-B の答え）もこの文を引く。`ACD-1.4-CHANGELIST.md` の「本文が自分で述べる理由を 1 つずつ当てる」行（11-02）も同じ結論。

### 4.5 5a が渡した §12.1 / §12.2 の問い —— 明瞭化の候補にはしない

5a の問い: §12.2 の発動条件 *"personal to the author, inalienable, or incapable of waiver"* は「or」で 1 語当たれば足り、
§1.2 の定義自体が人格権を *"of a personal character"* と述べるので、§12.1（放棄）が働く法域は実務上ほとんど無いのではないか。
**答え**: 記録に例は無い（`QUESTIONS-FOR-COUNSEL.md` 問 3 (d) も「隙間にある法域を知らない」と書く）。ただし明瞭化の候補にはしない。
(i) §12.1 を「残りの場合」として従属させる並べ替えは、放棄 → 予備の順（§3 → §4・CC0 と同じ）を崩し、**§12.2 が「どちらが当たるか判定しなくてよい」と述べているので読者は順序に依存しない**。
(ii) 理由の句（将来・未知の法域の受け皿）を本文に足すのは F3 の型そのもので、「未知の法域でだけ働く」という反対解釈を作る。
**別の論点として記録する（新規版候補・この file では採らない）**: §12.2 を §12.1 の「代わりに」ではなく「並んで」働かせる形（§4.4 が §3 と §4 について使う形）にすれば、
発動条件の 3 語の分類が不要になり、問 3 (d) の隙間（放棄に方式が要り、かつ譲渡できる法域）も構造で閉じる。
**これは法的効果を変える**（§12.2 の法域でも放棄を試みる。*"to the fullest extent permitted"* が許されない部分を落とすが、公序の問 3 (c) と絡む）ので、明瞭化の作業ではない。

### 4.6 生きている候補 —— §2.8 の理由の文（−41 語・bb の反例テストへ）

```
  2.8  This Dedication, in respect of the Work, binds the Dedicator's
       successors, assigns, heirs, and personal representatives, and any person
       to whom a Covered Right or a patent claim in the Work is transferred, to
       the fullest extent the law permits. A transferee takes subject to it,
       Section 6 included. Neither Section 5.3 nor Section 12.4 narrows this
       Section.
```

**Before** は 3 文目に *"This is stated expressly because Sections 5.3 and 12.4 say as much for the covenants they contain, and silence here would invite the argument
that the grants themselves stop at the Dedicator, which would leave the longest-lived risk, the change of hands, open."*（43 語）を持ち、末文は *"Neither of those Sections narrows this one."*（7 語）。
After は理由の文を消し、末文の指示語の先を名指しに変えた（+2 語）。差し引き −41 語。

| 観点 | Before | After |
|---|---|---|
| 許諾の範囲 | Dedication 全体（1.4 で E49 を閉じるために列挙から「This Dedication」へ変えた）| 同じ |
| 主体（拘束される者）| 承継人・譲受人・相続人・人格代表者・権利の譲受人 | 同じ |
| 条件・除外 | 無し / §6 を含むと明示 | 同じ |
| 法域ごとの結果 | *"to the fullest extent the law permits"* | 同じ |
| §5.3・§12.4 との関係 | 狭めない（末文）| 同じ（末文を名指しにした）|
| 失うもの | 「なぜ明示したか」の説明 | —— |

**消してよいと考える理由**: この理由の文は、§2.8 が *"Sections 3, 4, 6, 7, and 8 bind"* と**列挙していた**ときに、列挙の外の沈黙が「止まる」と読まれる危険を説明していた。
1.4 で §2.8 は Dedication 全体を拘束する形に変わり、**本文に承継人について沈黙している条は残っていない**。
一方で理由の文は *"silence here would invite the argument"* と、**沈黙が反対の議論を招くことを本文自身が認める**文であり、本文が沈黙している別の事柄
（例: 準拠法 —— §15.7 は置いていない）に対して、本文の言葉で向けられうる。
**bb に当ててほしいこと**: (a) 理由の文が無いと、§5.3・§12.4 の明示と並べて「§2.8 は covenant 以外には及ばない」と読む余地が戻るか（末文が止めるか）。
(b) 想定問答 `review-responses-clauses.md` の §2.8 の答え（*longest-lived risk* を引く・510 行付近）が 1.4 を引く版でも成り立つか。
(c) §6.5 第 2 文（*"It is stated expressly because silence on this subject has proved ambiguous in practice, and because a permission that an automated system cannot determine is … no permission at all"*）は同じ型だが、
ドシエが #85 などで原理として引く文なので**この試作には含めない**。ただし後半を「機械が判定できない許可は無い」と**作用の文として**読む敵対的な読みが立つかは、別に当ててほしい。

## 5. 反例テスト（手順 6・bb）

（5a の「効果を運ぶ語」の差分を起点に、bb が書き足す。元では許され試作では許されない利用・読み、またはその逆）

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
