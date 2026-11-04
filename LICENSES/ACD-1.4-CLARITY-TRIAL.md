---
file: LICENSES/ACD-1.4-CLARITY-TRIAL.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-04
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt (試作の対象・この file は草案を上書きしない) / LICENSES/ACD-OSI-BOTTLENECKS.md (B3 / B13) / LICENSES/ACD-1.4-CHANGELIST.md (採用した変更の記録先)
---

# ACD-1.4 草案の明瞭性の試作 —— 法的効果を保ったまま、言い直しの族と読みの分岐を減らせるか

**目的（2026-11-04・オーナーが渡した外部 AI の見解を受けて、3 人が判断した作業 —— オーナーが求めたのは「承認確率を上げるための 3 人連携」で、手順の中身は外部 AI のもの）**: 許諾の範囲・権利主体・法的効果を保ったまま、
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
**採用は 2 件 —— §2.8 と §12.4 の理由の文を対で外した（−79 語・§4.6）と、bb の束（§13.2 への案内 3 か所・§11.4 の理由の文・§4.6 の指示語・−63 語・§4.7）。**
どちらも bb の反例テストをすべて通り（§5）、草案・冒頭の変更一覧・`ACD-1.4-CHANGELIST.md` の変更表へ反映した（2026-11-04）。
それ以外の候補は、この file の中で止めてある。

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

### 4.6 生きている候補 —— §2.8 と §12.4 の理由の文を対で外す（−79 語・反例テストの当て直し待ち）

**経緯**: 最初は §2.8 だけを外す試作（−41 語）を出した。bb の反例テスト（2026-11-04）は (a)・CE10 を通したが、
**5a が指摘した非対称が成立した** —— §2.8 だけ外すと、同じ型の理由の文（*"This is stated expressly because … longest-lived risk … open"*）が §12.4 にだけ残る。
2 つは対になっている（§2.8 の理由の文は §12.4 を名指しし、どちらも承継人について述べ、どちらも *longest-lived risk* という語で締める）。
並ぶ 2 つで片方だけに説明があるのは SELF-AUDIT §3r と同じ形なので、**§2.8 単独の試作は採らず、対で外す試作に組み直した。**

```
  2.8  This Dedication, in respect of the Work, binds the Dedicator's
       successors, assigns, heirs, and personal representatives, and any person
       to whom a Covered Right or a patent claim in the Work is transferred, to
       the fullest extent the law permits. A transferee takes subject to it,
       Section 6 included. Neither Section 5.3 nor Section 12.4 narrows this
       Section.

  12.4 The covenant in Section 12.2 binds the Dedicator's successors, assigns,
       heirs, personal representatives, and any person entitled to exercise or
       enforce Moral Rights in the Work after the Dedicator's death, to the
       fullest extent the law permits the Dedicator to bind them.
```

**消した文**:
- §2.8 の 3 文目 *"This is stated expressly because Sections 5.3 and 12.4 say as much for the covenants they contain, and silence here would invite the argument
  that the grants themselves stop at the Dedicator, which would leave the longest-lived risk, the change of hands, open."*（43 語）。
  末文 *"Neither of those Sections narrows this one."*（7 語）は、*those Sections* の先行詞が消した文の中にあったので、名指しに変えた（9 語・+2）。
  **5a の試算（−43 語）は 1 文だけを消しており、*those Sections* が先行詞を失っていた** —— その版は宙に浮いた指示語の反例になるので採らない。
- §12.4 の 2 文目 *"This is stated expressly because Moral Rights outlive the author in many jurisdictions and may be exercised by relatives or by a public authority,
  so a covenant that bound only the Dedicator would leave the longest-lived risk open."*（38 語）。

差し引き **−79 語**（語数は草案全体を空白で区切って数えた: 6,847 → 6,768。試作の全文は scratchpad の `trial-e.txt`、草案との差は上の 2 条だけ）。

**条ごとの対照**:

| 観点 | §2.8 Before → After | §12.4 Before → After |
|---|---|---|
| 許諾・約束の範囲 | Dedication 全体（1.4 で E49 を閉じるために列挙から「This Dedication」へ変えた）→ 同じ | §12.2 の covenant → 同じ |
| 拘束される者 | 承継人・譲受人・相続人・人格代表者・Covered Right / 特許の譲受人 → 同じ | 承継人・譲受人・相続人・人格代表者・**死後に人格権を行使できる者** → 同じ |
| 条件・除外 | 無し / §6 を含む → 同じ | 無し → 同じ |
| 法域ごとの結果 | *"to the fullest extent the law permits"* → 同じ | *"to the fullest extent the law permits the Dedicator to bind them"* → 同じ |
| 他の条との関係 | §5.3・§12.4 は §2.8 を狭めない → 同じ（末文を名指しにした）| —— |
| 失うもの | 「なぜ明示したか」の説明 | 「なぜ死後まで及ぼすか」の説明 |

**反対解釈を封じているもの（bb の (a) の結果）**: 理由の文ではなく、§2.8 の第 1 文 *"This Dedication, in respect of the Work, binds …"* である。
理由の文が防いでいた「列挙の外の沈黙は止まる」読みは、1.4 で §2.8 が列挙をやめた時点（E49）で構造上立たない。
末文は covenant 側の狭い語（*"the law permits the Dedicator to bind them"*）が §2.8 へ移るのを止め、§15.1（受領者に多く与える読みが優先する）も狭い読みを退ける。
§5.3 の末文 *"Sections 3 and 4 operate in their favour independently of this Section"* も、covenant についての §5.3 の書き方が §3・§4 を限らないことを述べる。**理由の文の代わりは 3 重以上に在る。**
§12.4 の理由の文が名指す *"relatives or by a public authority"* は、作用の文の *"any person entitled to exercise or enforce Moral Rights in the Work after the Dedicator's death"* に含まれ、
公的機関のような法人は §15.5 の *"person" includes an entity*（E58）で覆われる（bb の CE10）。

**残す同型の文と、その理由**: §6.5 第 2 文 *"It is stated expressly because silence on this subject has proved ambiguous in practice, …"* は残す。
§2.8 / §12.4 の対とは主題が違い（承継ではなく Computational Use）、ドシエが #85 などで原理として引く文である。
後半を「機械が判定できない許可は無い」という**作用の文として**読む敵対的な読みは、理由の節の中の文であり §15.1・§6.1・§4.4・§9.3 が在るので立たない（bb の (c)）。

**消してよいと考える理由**: 2 つの理由の文はどちらも権利義務を運ばず、作用の文が既にすべてを名指している。
加えて §2.8 の理由の文は *"silence here would invite the argument"* と、**沈黙が反対の議論を招くことを本文自身が認める**文であり、
本文が沈黙している別の事柄（例: 準拠法 —— §15.7 は置いていない）に、本文の言葉で向けられうる。

**従属する作業（採用した場合）**: 想定問答 `review-responses-clauses.md` 510 行付近は §12.4 の理由の文を引いている。出す版が 1.4 になったら、答えの側で理由を述べ直す（bb が持つ）。
`against.md` #104 の *"§12.4 extends it to heirs because moral rights outlive the author"* は 1.0 の本文についての設計の説明で、1.4 で理由の文が消えても偽にならない。

**結果（2026-11-04）**: bb が対の試作に反例を当て直し、すべて通過した（§5）。草案へ反映した —— 冒頭の変更一覧に 1 項目（−81 語）を足し、既存の §2.8 末文の項目を +7 → +9 に直し、申告を 5,547 → 5,468 語にした。

### 4.7 bb の束 —— §13.2 への案内 3 か所・§11.4 の理由の文・§4.6 の指示語（−63 語・採用）

**bb が反例の立たないことを確かめてから出した束**を試作 f にした（Before = main の草案・byte 一致を bb も cmp で確認）。

| 条 | Before | After | 語 |
|---|---|---|---|
| §2.7 | 末文 *"Section 13.2 states the corresponding absence of warranty."* | 外す | −8 |
| §8.5 | 同じ案内の文 | 外す | −8 |
| §11.4 | *"This matters here because a work meant to be learned from is often data about people, and a reader is entitled to know exactly where this instrument stops. Section 2.7 states the general principle and Section 13.2 the corresponding absence of warranty; this Section states a limit of reach, it is not a condition upon You, and Section 10.1 is unaffected by it."* | *"This Section states a limit of the Dedication's reach; it is not a condition upon You, and Section 10.1 is unaffected by it."*（§11.3 の末文と一字一句同じ）| −40 |
| §4.6 | *"Section 4.5 concerns the terms You may add. It does not cut …"* | *"Section 4.5 does not cut …"* | −7 |

**条ごとの効果**: 範囲・主体・条件・除外・法域はどの条でも変わらない。
§13.2 は独立した無保証の条で、§13.1 が非侵害を含むすべての保証を目立つ形で否認するので、§8.5 の *"neither a representation nor a warranty"* と §13.2 の語の違いは保証に隙間を作らない。
§11.4 の *"any right held by a person other than the Dedicator"* は §2.7 と同じ範囲を述べ、§2.7 への操作上の参照は §6.1 / §6.2 / §7.2 / §8.5 に残る。
§4.6 は *It* が §4.5 とも「You が足す terms」とも読めた分岐が消え、§4.5 が terms の条であることは同じ条の *"Terms You add govern what You give"* が述べ続ける。
**消えた読みの分岐**: §11.4 の理由の文が作っていた「人についてのデータでない Work では限界が効かない」という反対解釈と、§4.6 の指示語の分岐。
**非対称**: §13.2 への案内は 1 つも残らず、§11.3 と §11.4 の末文はそろう（§4.1 で残っていた *limit of the Dedication's reach* / *limit of reach* の綴りもここで片づいた）。
**費用（5a）**: §13.2 は全体に及び効果は変わらないが、読み手を免責へ案内する導線が §2.7・§8.5・§11.4 の 3 か所で無くなる —— B13（読みの負荷）には小さな逆向きの費用である。5a の効果語の差分で減ったのは §4.6 の *you / may*（消した *"the terms You may add"* の語）と §11.4 の *where*（目的の文の *"where this instrument stops"*）だけで、条件文 *"Where the Work contains personal data …"* は残る。
**従属する作業**: `against.md` #173 は 1.1 / 1.2 の notice を論じて §11.4 の理由の文を逐語で引くので、bb が注を付ける。`review-responses-meta.md` の答え（215 行付近）は steward の言葉として同じ理由を述べており、本文の引用ではない。

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

### 5.2 試作に当てた結果（2026-11-04）

#### 試作 (b)（F2 を §10.5 の一般則へ）

25 が §4.1 の反例 3 つで退けた。先に登録した CE1〜CE4 の結果も書いておく —— **退けた判断を、事前に登録した反例の側からも確かめるため**。

| # | 結果 | 理由 |
|---|---|---|
| CE1 | 通過 | 一般則 *"no statement … of what it does not reach or grant, is a condition upon Your use"* は、§11.3 第 2 文が *"is outside what this Dedication reaches"* と自分を分類するので覆う。条件でない以上、限界の外の行為は許諾に影響しない。**ただし §11.3 第 1 文 *"does not make a false statement true"* が「reach しない文」に当たるかは境界**（25 の反例 2・5a の指摘と同じ）|
| CE2 | 通過 | *"Nothing in Section 16"* が §16.4 の但し書きを覆う。**ただし §3r はまさに §10.5 が在る場所で起きている**（25 の指摘）—— 一般則は具体的な但し書きが条件のように読まれることを止めなかった |
| CE3 | 通過 | 一般則の射程は *"Your use"* で、Dedicator の義務（§2.6）に及ばない |
| CE4 | 通過 | §4.3 / §8.2 は変えていない |

**結論は 25 と同じで採らない** —— 事前の 4 件は通過したが、25 の反例 1（E7 の読み順）と反例 3（*use* / *in respect of* の対比が §5.1 を狭く読ませる）は、**事前に登録していなかった種類**だった。**事前の登録は、登録した種類しか捕まえない**（それでも登録しておくことで、試作に引きずられた反例だけで判断することは避けられる）。

#### §2.8 の理由の文を消す（25 の §4.6・−41 語）

| # | 反例 | 結果 | 理由 |
|---|---|---|---|
| (a) | 理由の文が無いと、§5.3 / §12.4 が covenant について承継を明記していることと並べて、「許諾は Dedicator で止まる」と読む余地が戻るか | **通過** | 封じているのは理由の文ではなく第 1 文 —— *"This Dedication, in respect of the Work, binds the Dedicator's successors … and any person to whom a Covered Right or a patent claim … is transferred"*。**1.4 で列挙を「This Dedication」へ変えた（E49）時点で、理由の文が防いでいた読み（列挙の外の沈黙）は構造上もう立たない**。末文 *"Neither Section 5.3 nor Section 12.4 narrows this Section"* が covenant 側の狭い語（*"the law permits the Dedicator to bind them"*）が §2.8 へ移る読みを止める。**§15.1 も同じ向きに働く** —— 1.4 の §15.1 は *"This Dedication, in respect of the Work, is to be construed so as to give the widest permission … the reading that grants more to You prevails"* で、「許諾は Dedicator で止まる」は狭い方の読みなので退けられる。**理由の文の代わりは 3 重に在る**（第 1 文・末文・§15.1）|
| CE10 | 理由の文が、操作条項に無い場面を名指して効果を運んでいないか | **通過** | 理由の文の *"the change of hands"* は第 1 文の譲受人・権利の譲受人に含まれる |
| 5a | **§2.8 だけ理由を外すと、対になる §12.4 にだけ理由が残る**（§12.4 は *"would leave the longest-lived risk open"*）。「§2.8 は理由を持たないので狭く読む」という逆向きの読みの起点になる | **成立** | SELF-AUDIT §3r と同じ「並ぶ 2 つで片方だけ」の形。**§2.8 だけの試作は採らない** |
| (b) | 想定問答 `review-responses-clauses.md` 510 行（*"longest-lived risk"*）が、1.4 を引く版でも成り立つか | **§12.4 の理由を引いている**（§2.8 ではない）| §2.8 だけの試作には影響しない。§12.4 の理由も外すなら、出す版が 1.4 になったときに答えの中で理由を述べ直す必要がある（理由は本文ではなくドシエが持てばよい）|
| (c) | §6.5 第 2 文の後半 *"a permission that an automated system cannot determine is … no permission at all"* を**作用の文として**読む —— 機械が判定できない場面では ACD 自身の許可も無い、という自己否定の読み | **立たない** | (i) 文の位置が *"It is stated expressly because …"* の理由の節の中で、何も付与・剥奪していない、(ii) §15.1（許可を広く読む）、(iii) §6.1 の許諾は無条件で、§4.4 / §9.3 が「判定に依存しない」と述べる。**ただし言い切りの強さ（*no permission at all*）は B13 の目で見ると読み手に 1 段の推論を求める** —— 試作の対象にはしない（CE11・gap の論拠）|

#### 改めた候補 —— §2.8 と §12.4 の理由の文を対で消す（−41 −38 = −79 語）

5a の非対称の反例を避けるには、**対の両方から理由を外す**しかない。§12.4 にも CE10 を当てた:
理由の文の *"may be exercised by relatives or by a public authority"* は、操作条項の *"any person entitled to exercise or enforce Moral Rights in the Work after the Dedicator's death"* に含まれ、
**公的機関のような法人も、1.4 が §15.5 に足した「person は entity を含む」（E58）で覆われる**。*"Moral Rights outlive the author in many jurisdictions"* の反対解釈（作者の死で消える法域では §12.4 が働かない）は、拘束する相手がいないので害が無い。
**→ 通過。25 へ戻して、対の試作（§2.8 + §12.4）として §4.6 を書き直してもらう。** 採用すれば、出す版が 1.4 になったときに想定問答 510 行の理由を答えの側へ移す（従属する作業）。

#### 試作 e（§2.8 と §12.4 の理由の文を対で外す・−79 語）に当て直した結果 —— **全件通過**

| # | 反例 | 結果 |
|---|---|---|
| (a) | 許諾は Dedicator で止まる、という反対解釈 | **通過**（第 1 文・末文 *"Neither Section 5.3 nor Section 12.4 narrows this Section"*・§15.1 の 3 重）|
| CE10 | 理由の文が操作条項に無い場面を名指していないか（§2.8 / §12.4 の両方）| **通過** |
| 5a の非対称 | 対の片方にだけ理由が残る | **解消**（両方から外した。残る *"stated expressly because"* は §6.5 だけで、対になる条は無い）|
| 新 | 理由が消えると §12.4 は §2.8（Dedication 全体が承継人を拘束）と重複して見えるか | **通過** —— §12.4 には「承継人でない、作者の死後に人格権を行使できる者」という独自の拘束が明示されている。§12.4 の狭い語（*"the law permits the Dedicator to bind them"*）が §2.8 へ移る読みは、§2.8 の末文が止める |
| 新 | 末文の *"this Section"* がどの範囲を指すか | **通過** —— E57 の直しで、1.4 の *"this Section"* はその条（§2.8）を指す |
| 5a | 機械的な差分（効果を運ぶ語）| **効果語の減少なし・先行詞の無い指示語 0 件**。§12.4 の理由が名指した *public authority* と §2.8 の会社の譲受人は、1.4 §15.5 の「person は entity を含む」（E58）で残る本文の *any person* に含まれる —— person / entity の分岐は §15.5 で閉じている |

**→ 採用候補。草案への反映は 25（ヘッダの箇条・CHANGELIST の変更表・語数の申告 −79）。**
**従属する作業（bb）**: 想定問答 `review-responses-clauses.md` 510 行は §12.4 の理由を引いている。出す版が 1.4 になったときに、理由を答えの側で述べ直す（理由は本文ではなくドシエが持つ）。

#### CE8 の書き換え案（§8.3 の *software* の反対解釈を消す）—— **不成立**

第 3 文に結果を書き込む案 *"Any reading of this Dedication that gives away a Covered Right while withholding a patent right is to be rejected"* を当てた。
**§8.4 の末文**は *"it does not license a claim that would be infringed by a model, parameter set, weight, embedding, or output produced without any use of the Work"* と、
**意図して**ある種の特許を許諾しない。新しい規則は、その意図した除外まで「退けるべき読み」にしてしまう ——**読みの分岐を 1 つ消して、条と条の衝突を 1 つ作る**。
**§8.3 は変えない。残余リスク**: 第 2 文の *"because software cannot be practised …"* から「ソフトウェアでない Work（データセット・モデル）では特許の留保が許される」と読む余地は残る。
弱めているのは §8.4（モデル・出力を名指して許諾する）と §15.1。**この 1 件は、効果を保ったまま消す書き方が見つからなかったものとして記録する。**

#### 試作 f（§13.2 への案内 3 か所・§4.6 の指示語・§11.4 の理由の文・−63 語）に当てた結果 —— **全件通過**

Before は main の草案と byte 一致（25 が確認・bb も `cmp` で確認）。

| # | 反例 | 結果 |
|---|---|---|
| 25 (1) | §11.4 から §2.7 への案内（*"Section 2.7 states the general principle"*）が消えると、§11.4 の *"any right held by a person other than the Dedicator"* が §2.7 と別の射程に読まれるか | **通過** —— §2.7（Dedicator が持つ権利にしか及ばない）と §11.4 の該当句は同じ範囲を述べており、案内が無くても食い違う読みは立たない。§2.7 への参照は §6.1・§6.2・§7.2・§8.5 に残るが、これらは**許諾の射程を Dedicator の権利に限る**操作上の参照で、限界を述べる §11.4 が引かなくても射程の読みは変わらない |
| 25 (2) | §13.2 への案内を外すと、§8.5 の *"neither a representation nor a warranty that practising the Work infringes no claim"* が §13.2 と別の保証の扱いに読まれるか（§8.5 は *practising*、§13.2 は *use*）| **通過** —— **§13.1 が非侵害を含むすべての保証を目立つ形で否認している**（*"WITHOUT WARRANTY OR CONDITION OF ANY KIND … INCLUDING … NON-INFRINGEMENT"*）。*practising* と *use* の語の違いは、保証の扱いに隙間を作らない |
| 非対称 | §13.2 への案内が 3 か所のうち一部だけ残るか | **解消** —— 試作 f に *"Section 13.2"* を名指す文は 1 つも残らない |
| 指示語 | §4.6 の *"It"* | **分岐が 1 つ消えた** —— 元の *"It does not cut Your recipients off"* は §4.5 とも「You が足す terms」とも読めたが、試作は §4.5 を名指す。末文 *"Terms You add … do not narrow"* が terms の側を別に述べるので、どちらの読みの内容も残る |
| CE10 | §11.4 の理由の文が操作条項に無い内容を運んでいないか | **通過** —— *"a reader is entitled to know exactly where this instrument stops"* は読み手への説明で、操作条項（届く範囲・個人データ）は残る |
| 一致 | §11.3 と §11.4 の末文 | **一字一句同じ**（*"This Section states a limit of the Dedication's reach; it is not a condition upon You, and Section 10.1 is unaffected by it."*）—— *limit of reach* / *limit of the Dedication's reach* の綴りの揺れも消えた |

**→ 採用候補。** 従属する記録: `against.md` #173 は §11.4 の理由の文を逐語で引く（1.1 / 1.2 の notice についての記述で、その版としては偽にならない）。
1.4 を論じる文に引き継ぐときは注を置く（bb）。`review-responses-meta.md` の答えは steward の言葉で理由を述べており本文に依存しない。#49 も本文に依存しない。

## 6. KPI（5a の道具で導出）

| 指標 | Before（1.4 草案・11-04 朝）| After 1（§2.8・§12.4）| After 2（+ bb の束）|
|---|---|---|---|
| 項の数 | 80 | 80 | 80 |
| 本文の語数（見出し・前文を除く・5a の道具）| 5,049 | 4,970（−79）| 4,907（−63）|
| 草案冒頭の申告（Check 468 が強制する数え方）| 5,547 | 5,468 | 5,405 |
| 理由・案内・念押しの文 | 40 文・1,234 語 | 2 文・81 語減 | さらに理由 1 文・案内 4 文が減る（数え直しは 5a）|
| 6 語以上の重複 / 族の数（5a の道具）| 79 / 58 | 79 / 58 | 76 / 55 |
| 先行詞の無い指示語（5a の道具）| 0 | 0 | 0（道具は *those Sections* の形だけを見て裸の *It* は見ない。§4.6 の改善は読みで確かめた）|
| 意味の異なる解釈候補 | F3 の 9 件 + F1 / F2 の反例の種 | F3 の 7 件 | F3 の 6 件 + §4.6 の指示語の分岐が消えた |
| 反例テスト | — | 対の試作 = **通過** / §2.8 単独 = 不成立 / F2 の試作 (b) = 不成立（反例 3）/ §8.3 の書き換え（bb）= 不成立 | 試作 f = **通過** |
| 効果の保存を説明できた条 | — | 2（§2.8・§12.4）| 6（+ §2.7・§8.5・§11.4・§4.6）|
| OSI の阻害理由への効き | — | 基準 3（曖昧さ）: 「沈黙は議論を招く」と本文が認める文が消えた | 基準 3: 反対解釈 1 件と指示語の分岐 1 件が消えた。B3（長さ）は累計 −142 語（本文の約 2.8%）で、B3 の結論（縮めても答えきれない）は変わらない |

**この表の数字は、採用の根拠ではない。** 依頼の条件どおり、語数の削減・CI の成功・文書の追加を承認確率の向上と扱わない。

## 7. B15（主題適格）の試作 —— B10 を保ったまま、主題の疑義を条文で弱められるか（2026-11-04・25）

**きっかけ**: 別の AI の見解をオーナーが渡した（オーナーの指示ではない）。問い自体は、3 人が 11-03 に逆側として自分で記録していたもの
（`ACD-1.4-CHANGELIST.md` §1.3 行の逆側 *「重みを名指すと B15 の論点をこちらから出す」*）なので、3 人の判断として検証する。
その見解にある承認確率の値や状態の分類の枠は、このドシエのものではないので使わない。
**採用の条件**: (1) B10 の立証済みの効果（`ACD-1.0.gap-measurements.md` §1.133・§8.4 + §8.2 + §10.1 / §10.4）を失わない、
(2) AI 資産（データセット・重み）への許可を失わない、(3) B15 の疑義を**中身で**弱める（見えにくくするだけの変更は数えない）。満たせなければ「未成立」と書く。

**一次根拠（register B15 に逐語で在るもの）**: Mulan Open Works Licenses の不承認（2023-09-15）は OSD 違反を挙げず
*"as open culture licenses, are not appropriate for OSI approval"* とし、理由に引いたのはそのライセンスが定義した対象の列挙
（*"… a photographic work, an audiovisual work, a graphic work, and a model work"*）だった。境界は委員会自身が
*"Sometimes an OSI license will cross over into data or hardware when tied to software, but not a license altogether unrelated to software."*（Chestek 氏 2023-08-10）と述べている。
ACD の Work の定義は source code / object code から始まり、前文の第 1 文は *"Software and the works that surround it"* である。

### 7.1 比べる 4 案

| 案 | §1.3 の列挙 | 範囲（受領者が依拠できるもの）|
|---|---|---|
| **B**（1.4 草案のまま）| *"… documentation, data, metadata, audiovisual material, the parameters, weights, and configuration of a machine learning model, and any collection or compilation of these"* | —（比較の基準）|
| **A1′**（1.4 の追加だけを戻す）| 凍結 1.0〜1.3 と同じ *"… documentation, data, metadata, audiovisual material, and any collection or compilation of these"*（−10 語）| **変わらない** —— 列挙は例示（§15.5）で、重みは *data* と *"in any medium and in any form"*（Work の定義・1.0 では §1.2）に入る。CHANGELIST の §1.3 行自身が「受領者が依拠できるものは増えない」と書いた追加である |
| **A1**（A1′ + *audiovisual material* も外す・bb の案）| *"… documentation, data, metadata, and any collection or compilation of these"* | 変わらない（*"in any medium and in any form"*・1.0 では §1.2）|
| **A2**（UPL 型の結び付け）| 例: *"software, associated documentation, and data distributed with or for use with that software"* | **狭まる** —— 単体のデータセット・単体の重みが Work から外れる |

### 7.2 6 つの場面の Before / After（B に対して）

| 場面 | A1′ | A1 | A2 |
|---|---|---|---|
| ソースコード単体 | 同じ | 同じ | 同じ |
| ソフトウェアに付随する学習データ | 同じ（*data*）| 同じ | 同じ（付随するなら）|
| 学習済みモデルの重みだけ | 同じ（*data* / *in any form*。1.0〜1.3 と同じ扱い）| 同じ | **Work でなくなる** —— §3 / §4 / §6 の許可が無い |
| ソフトウェアで学習して生じたモデル | 同じ（§6.4 / §8.4 は Work の定義ではなく「結果」として名指す）| 同じ | Work がソフトウェアなら同じ / データの Work からの結果は**失う** |
| 生成された出力の販売・改変 | 同じ（§6.4）| 同じ | データの Work からの出力は**失う** |
| 元の Work に関わる特許の行使 | 同じ（§8.1 / §8.4）| 同じ | データの Work については**失う**（§8.4 の効果がソフトウェアの Work に縮む）|

**B10 への作用**: A1′ と A1 は §8.4 / §8.2 / §10 に触れず、§1.133 の 3 つ（範囲・無条件・終了なし）はそのまま残る。A2 は §8.4 の効果をソフトウェアの Work に縮め、AI 資産への許可を失う。

### 7.3 判定（暫定・bb の敵対的検証の前）

- **A2 は採らない** —— 採用の条件 (2) を満たさない。主題を「ソフトウェアに結び付ける」ことは範囲を狭めることでしか達成できず、狭めれば register B15 の見出しどおり B10 を自分で折る。
- **A1 は採らない** —— *audiovisual material* は 1.0 から在る語で、範囲を変えずに語だけ消すのは**疑義への答えではなく、疑義を見えにくくすること**である（条件 (3) を満たさない）。
  しかも凍結版との差が「1.4 は audiovisual を外した」という反対解釈の材料になる。Mulan の理由に引かれた語と同じ語を持つことは、`submission.md` §B.0 と `submission-reference.md` §3d で**先に言ってある**。
- **A1′ は採用候補（下の A1′+ の形で）** —— 範囲は変わらず、戻すのは 1.4 自身が足した例示だけなので、見えにくくする変更でもない（凍結版の状態へ戻る）。
  向きは一次資料で決まる。(i) CHANGELIST の §1.3 行は OSAID が改変に適した形を「コード・パラメータ・データ情報」とすることを追加の理由にしたが、
  OSAID 1.0 自身はパラメータについて *"They may be free by their nature or a license or other legal instrument may be required to ensure their freedom"*
  と答えを開いている（CHANGELIST の §9.1 行が引く原文）—— **OSI 承認ライセンスで扱えと述べてはいない**。
  (ii) Fontana 氏は OSAID を引いて *"the OSI contemplates that things other than OSI-approved licenses might be suitable for model parameters, but that does not apply to code or model architecture materials"*
  と素材の種類で線を引いている（`ACD-1.0.review-doctrine.md` の OpenMDW の節・(b)）。
  **(i) は我々の推論、(ii) は審査者側の直接の言明**なので、(ii) を取る。**§1.3 にパラメータを名指すことは、OSI が「承認ライセンス以外が適しうる」と述べた側へ、Work の定義から自分で寄ることである。**
- **A1′ には 1 つ足す（A1′+）** —— bb の指摘どおり、§9.1 の例示 *"such as the parameters of a machine learning model produced by training"* も 1.4 で足した文で、
  Work がパラメータでありうると述べたまま残る。例示を *"such as code produced by an automated system"*（§1.8 の語）へ替える。
  例示なので効果は変わらず（§9.2 / §9.3 は例示に依らない）、Fontana 氏の線の内側（code）の例になる。−4 語。
  **逆側**: §9 の典型例のうち、重みに ACD を付ける読み手に最も役立つ例（学習で生じるパラメータ）を名指す説明力が落ちる —— その読み手は §1.8 の定義から自分で導くことになる（1.0〜1.3 と同じ）。

**判定（2026-11-04・採用）**: **A1′+ を 1.4 草案へ反映した**（§9.1 の例示は bb の指摘で *such as* ではなく *including* にした —— *such as* は本文でここにしか無く、§15.5 の例示の規則が掛かっていなかった）。
1.4 草案に対しては、B15 の文言上の材料が 2 つ（§1.3 の列挙・§9.1 の例示）消え、§9.1 はソフトウェアに結び付いた例になる。
**凍結 1.3 に対しては、B15 の実質は変わらない**（1.3 は最初からパラメータを名指していない）—— 動かせたのは 1.4 が自分で足した信号だけで、
**B15 の実質（定義が software-specific でない）は残る**。範囲・B10・AI 資産への許可はどれも変わらない。


**反例テストと測定（2026-11-04）**: bb が 6 場面と §9.1 の 2 点（例示がコードに限るように読まれるか / 限界の書き方）に当てて全件通過。
5a の比較: 本文 4,907 → 4,893 語（*including* にした分を足すと草案冒頭の申告は 5,405 → 5,390）/ 重複 76・族 55 は不変 / 宙に浮いた指示語 0 /
468u の 5 句の欠け 0 / *Work* は 52 条 77 回・*Computational Use* は 4 条 5 回で当たり先は不変 / 消えた語は *weights*・*parameters*、*model* は 6 条 → 4 条（§1.7 / §1.10 / §6.4 / §8.4 に残る）。

**記録の仕方（5a の指摘どおり）**: これは **B15 の解消ではない**。範囲を変えずに、**OSAID の 3 構成要素に合わせる信号**を手放し、**非ソフトウェアの素材を名指す信号**を減らした取引である。
比べる相手で結論が違うので、2 つに分けて書く:
- **1.4 草案（変更前）に対して**: B15 の文言上の材料が 2 つ（§1.3 の列挙・§9.1 の例示）消え、§9.1 はソフトウェアに結び付いた例になった。
- **凍結 1.3 に対して**: B15 の実質は変わらない。§1.3 は同文に戻り、§9.1 には 1.3 に無かったソフトウェア寄りの例が加わるだけで、対象は広がりも狭まりもしない。
**「B10 を維持した B15 解消案」は未成立のまま**である —— 解消には定義をソフトウェアに結び付ける必要があり、それは A2 と同じく範囲を狭める。

**この節が確立しないこと**: B15 の中身（Work の定義がソフトウェア以外の素材を含むこと）は、どの案でも残る —— 残すことが AI 資産への許可と B10 の条件だからである。
動かせるのは、1.4 が自分で足した信号 1 つだけ（A1′）である。
