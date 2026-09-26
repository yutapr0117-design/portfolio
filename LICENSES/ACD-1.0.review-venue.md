---
file: LICENSES/ACD-1.0.review-venue.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-09-26
canonical-ref: LICENSES/ACD-1.0.reviewer-positions.md (主題ごとの審査者の立場) / LICENSES/ACD-1.0.review-corpus.md (アーカイブ全体の測定) / LICENSES/ACD-1.0.against.md
---

# 審査の場・手続き・人 —— venue がどう働き、誰が書いているか

**`ACD-1.0.reviewer-positions.md` から 2026-09-24 に切り出した**（998 行で Check 365 の 1,000 行上限まで
2 行しか残っていなかったため・**節番号は変えていない**ので既存の `§1.67` / `§1.68` / `§1.92` /
`§1.99` / `§1.106` / `§1.107` 参照はそのまま解決する）。**分ける基準**: 元の file に残したのは
「**ある主題について審査者が何と言っているか**」（人格権・特許・長さ・構造…）で、
ここへ移したのは「**審査の場がどう働き、誰がそこで書いているか**」（pre-review としての
`license-discuss`・沈黙の比較・書き手の記録・steward 自身の分析・moderator が引いた CoC）である。

## 1.67 `license-discuss` を pre-review として使った唯一の先例（2024-09〜10・15 通）

**我々と同じ使い方をしたスレッドが 1 つだけ見つかった。** 提出者は
*"Complying to https://opensource.org/licenses/review-process process, I wish to invite everyone
here to **discuss and pre-review** my newly drafted open-source licenses … **before submitting to
license-review**"* と書いて始めている。

### venue の設計が、否定形ではなく肯定形で述べられている

**McCoy Smith 氏・2024-09-30（同日）**:

> So, if you want this to be reviewed and approved, "license-discuss" is not the right mail list to
> do that. However, **if you want people to give comments before you submit for approval, this is
> the correct mailing list.**

**ドシエがこれまで持っていたのは否定形だけ**だった（「`license-discuss` は承認の窓口ではない」・
2026-08-04）。**肯定形の一次資料はこれが最初**である。**我々の venue 選択は、設計どおりの使い方
である。**

### そして pre-review は、機能するときは速く機能する

同日に McCoy 氏、翌日に Josh Berkus 氏と Pamela Chestek 氏、Bruce Perens 氏、Aaron Williamson 氏。
**15 通。** 条項の具体的な欠陥（特許・営業秘密の不許諾が承認を妨げる）まで踏み込んでいる。

### 我々に当たる 3 つ

**(1) 長さ —— 委員長が「読んでいない」と述べた記録の 2 例目（#116）。**

> **Pamela Chestek 氏・2024-10-05**: I have **not read these licenses in detail** because the are [sic]
> **extremely long, approximately 4500 words**, appear from the definitions alone to have way more
> detail than a typical open source license, and **are not understandable**…

**⚠ `the are [sic]` は原文どおりである。** **2026-09-19 まで我々は `they are` と書いていた** ——
**出典の誤植を黙って直していた。** 逐語引用は逐語でなければならず、**直せば、審査者が
アーカイブを検索しても我々の引用に辿り着けない。** 見つけ方は
`verify_dossier_quotations.py` を**初めて全 corpus に対して**回したこと（`against.md` #165）。

**ACD-1.0 は 4,896 語である**（§1.60 の実測）。**彼女が詳細に読まなかったものより長い。**
**ただし理由は連言で述べられている**（長い ∧ 典型より詳細 ∧ 理解できない）ので、
**長さだけを取り出して引くのは相手の理由を歪める。**

**(2) 非弁護士の起草 —— 名前のついた歴史的事例。**

> **Bruce Perens 氏・2024-10-01**: I was expert witness in the appeal of one of the first Open
> Source license cases, which resulted from **Larry Wall drafting the Artistic License 1.0 without
> the knowledge of a legal professional**, resulting in the lower court…

そして 10-05 に *"**there should be some sort of gateway**"* と述べている。
**#113（法的レビューか実使用か）に、最も具体的な形を与える発言である。**

**(3) "shall" —— 当たらない。**

> **Bruce Perens 氏**: The word "SHALL" **must not** be used in a license. Please replace all
> occurrences of "SHALL" with "MUST"…

**ACD-1.0 の "shall" は 0 件、"must" も 0 件である**（実測 2026-09-09）。
条件を課さない instrument なので**義務語がそもそも要らない** —— §10.1 の帰結であり、
Check 441d が列挙した構文の不在を BLOCKING で守っている。
**なお McCoy 氏はこの点で Perens 氏に完全には同意していない**（*"it is one of those things that
is so ingrained in legal drafting that we'll likely never be rid of it"*）—— **リストは一枚岩ではない。**

---

## 1.68 「pre-review」という下位集合を数えると、我々だけが沈黙している（#117）

**朝に測った基準率**（`license-discuss` のスレッドの 22%、ライセンスを持ち込んだものでも 18% が
返信ゼロ・#109）は**全体についての数**である。**その中に、我々の使い方と正確に一致する
下位集合がある** —— **「`license-review` へ出す前の pre-review として明示的に投稿したもの」。**

### 見つかった 3 件

| 日付 | 投稿者 | 形 | 返信 |
|---|---|---|---|
| 2024-09-30 | 個人（非弁護士）| *"discuss and **pre-review** … **before submitting to license-review**"* | **15 通**（McCoy 氏が同日）|
| 2025-10-27 | **企業**（Teradyne Robotics A/S・IPR Manager）| *"collect feedback on the proposed license **before submitting the license for a formal review by the OSI**"* | **29 通**（Berkus 氏・Perens 氏・McCoy 氏・Phipps 氏・Behlendorf 氏）|
| **2026-08-26** | **我々** | ACD-1.0 の議論依頼 | **0 通** |

**n = 3 で、沈黙しているのは我々だけである。**

**⚠ 逆側（2026-09-15 追記・種類 8 の掃引で出た）。この節は n = 3 から結論を引いており、#109 が同じ日に確立した規律**（*「比較対象を挙げるときは、それがどの母集団からどう選ばれたかを同じ場所に書く」*）**を、自分には当てていない。**

**3 件の内訳は同型ではない**: 1 件は**企業の IPR Manager**、1 件は**非弁護士の個人**で、**後者は 15 通を得ている**。**「pre-review として明示した」以外に共通点は無く、n = 3 は率を支えない。**

**そして書かれた後に、説明が 1 つ増えた** —— **我々の 2 通は moderation の案件として扱われていた可能性がある**（B14・2026-09-07 に moderator が我々へ直接 5 問を送っている）。**これは #109 が「第 4 の説明」として記録したもので、本節が書かれた時点では存在しなかった。**

**さらに、我々の投稿だけが 5,778 語で届いている**（§1.85）。**沈黙の説明として長さが効いているかは分からないが、3 件のうち我々だけが桁の違う量を送っている**ことは書いておく。

**2026-09-15 追記 —— 母数を作り直した。** `license-discuss` の**全 307 か月**（22,608 通）を走査すると、pre-review を明示した投稿は **27 年で 5 件**で、**返信がゼロなのは我々だけ**だった（`review-corpus.md` §1.90）。**n = 3 の指摘は正しかったが、n = 5 にしても結論は変わらず、むしろ強くなった。****そして最も近い類型（PUWL = universal waiver・個人・`[DISCUSS]` 投稿）が 30 通で最多である。**

**確立するのは 1 点だけ**: **この形の投稿に返信が付いた例が 4 件あり、我々には無い。率ではなく、存在の話である。**

### これが establish すること / しないこと

**establish する**: **#109 の慰めは、この下位集合には及ばない。** 全体の 18% という数は
「ライセンスや草案を持ち込んだ」広い集合についてのもので、**その中で最も我々に近い形**を
取り出すと、**返信が付かなかったのは我々の 1 件だけ**である。

**establish しない**: **原因**。n = 3 は率を出せる大きさではない。**他の 2 件との差は複数ある** ——
1 つは**企業**の提出であり（もう 1 つは個人）、どちらも**具体的な設計上の問題を抱えていた**
（OSD 6 に触れる利用制限・特許/営業秘密の不許諾）。**議論しやすい欠陥がある提出の方が
返信を集めるのは自然**で、これは **#96 の (a)** と同じ形である ——
**「論争が少ない」を有利に読むな**、と同時に**「論争が無い」を不利に読み切ることもできない。**

**そして #109 は撤回しない。** あれは「沈黙は欠陥の証拠でも拒絶の証拠でもない」を establish して
おり、**それは本節でも変わらない。** 変わったのは**慰めの範囲**である ——
**全体の基準率を、自分の下位集合の基準率として使ってはならない。**
**これは #109 が記録した失敗（標本を率として報告した）の、鏡像である** ——
今度は**率を、より狭い集合へそのまま持ち込もうとした。**

### 同じスレッドから、我々に有利な材料も 2 つ

**(1) プロジェクト固有性は採用の障害である、とリスト上で述べられている。**
Bruce Perens 氏（2025-10-28）——licensed material を特定のファイル形式で定義していることについて:

> this is also **so specific to your application that there is no use for other parties to adopt the
> license** and thus less incentive…

**§4b（「提出者専用ではないことの実証」）が測っているのは、まさにこの性質である**
（固有名詞 0・置換テキスト 0（§16.1 の推奨 notice の雛形 1 欄 `<location of this file>` を除く —— 採用者が自分の notice に書く欄で、本文は編集しない）・採用に本文編集が 1 箇所も要らない）。
**我々は「使える」ことを測ってきたが、その測定が「なぜ重要か」はリスト上に在った。**

**(2) OSD 6 の著者が、その条項について直接語っている。**
Perens 氏 *"I would consider any use restriction at all to be in contravention of the Fields of
Endeavor clause. **I wrote that clause.**"* ——ACD-1.0 §4.3 / §10.1 は利用制限を一切持たない。

## 1.69 終了トリガーの境界論争（2026-09・OpenMDW）—— ACD-1.0 は係争域の外に在る

**2026-09 の `license-review` は、OpenMDW の終了条項をめぐって「どの種類の主張なら
許諾を終了させてよいか」を論じている。** これは我々についての議論ではないが、
**§8.2（報復条項ゼロ）が置かれている場所を、審査者自身の言葉で位置づけられる。**

**Richard Fontana 氏（2026-09-01）** —— 論点そのものの定式化:
> This is clearly one of the questions the OSI needs to resolve: is there something special about
> copyright? Or is there something special about patent? … If a copyright trigger for license
> termination … is okay in addition to a patent litigation trigger, **what about other kinds of
> claims? Trademark infringement? Trade secret? What about claims concerning things having no
> connection to the software (or model, etc.) being licensed?**

**Joshua Gay 氏（2026-09-03・OSI Board Member）** —— 審査が何を問うべきかの分離:
> Those are separate inquiries: **1.** Every restrictive condition can be characterized as the price
> a licensor demands in exchange for use of its work. **2.** Open-source review must still determine
> **whether imposing that price is consistent with the freedoms the license is supposed to carry to
> users**.

そして**特許許諾がなぜ要るか**についての説明:
> A copyright license alone may not provide practical freedom to make, use, or distribute software
> **because patents can independently prohibit those same activities**. … The patent grant closes
> that gap.

### ACD-1.0 への還元（3 点・いずれも条文で確かめた）

1. **境界論争そのものが当たらない。** §8.2 は *"subject to no condition and are not terminable by
   the Dedicator on any ground"*、*"This Dedication contains no patent retaliation provision, and
   its absence is deliberate."* と述べる ——**どの種類の主張であれ終了しない**ので、
   Fontana 氏の「では他の種類は？」という滑り坂に乗る面が無い。
2. **Gay 氏の第 2 の問い（価格が自由と整合するか）は、我々には自明に満たされる** ——
   **価格が無い**（§10.1 / §4.3）。**ただしこれは「承認される」という意味ではない**：
   同じ検査を通ることと、承認に値することは別である。
3. **Gay 氏の「特許許諾がなぜ要るか」の説明は、§8.3 が条文で述べていることと同じである** ——
   *"software cannot be practised without practising whatever patent claims it embodies"*。
   **#124（四隅）の基準で言えば、この理由は我々の場合は条文の中に在る。**

### この節が establish しないこと

- **これは我々についての議論ではない。** OpenMDW の終了条項についての論争であり、
  **ACD-1.0 が承認されやすいことを示すものではない。**
- **「係争域の外に在る」は有利にも不利にも読める** ——争点を持たないことは、
  **審査者が労力を割く理由も持たないこと**でありうる（#116 / §1.60 の長さの議論と同じ向き）。
- **引用は 2026-09-10 にアーカイブから取得した。スレッドは進行中であり、立場は動きうる。**


## 1.92 いま返信を書いている 14 人のうち、記録が無かったのは 1 人だった（2026-09-17・93 か月の実測）

`license-discuss` の 2019-01〜2026-09 を取得し、**2024 年以降に返信を書いている人**を返信数順に並べて、
**その人の立場がドシエのどこかに記録されているか**を機械的に照合した（`review-corpus.md` §1.91 の掘削の副産物）。

| 返信数 (2024〜) | 誰 | 記録 |
| --: | :-- | :-- |
| 57 | Bruce Perens | あり |
| 27 | McCoy Smith | あり |
| 25 | Josh Berkus | あり |
| 25 | Pamela Chestek（Licensing Committee 委員長）| あり |
| 15 | David Woolley | あり |
| 11 | Kevin P. Fleming | あり |
| **11** | **Roland Turner** | **🔴 無し** |
| 11 | Richard Fontana | あり |
| 10 | Shuji Sado | あり |
| 9 | Rob Landley | あり |

**14 人中 13 人は既に追えていた。** これは「知らない人から来る」よりずっと良い状態だが、
**1 人だけ抜けていた**ので埋める。

### Roland Turner（`roland at rolandturner.com`・2020-12〜2025-02 に 18 通）

**主題は繰り返している**: AGPL の何が問題か（3 通）/ 倫理的ライセンスの非執行可能性（2 通）/
公開仕様のライセンス（2 通）/ GDPR とライセンス条項 / 「or later」条項の保証人としての OSI。

**論法の型**（逐語はアーカイブ・要旨のみここに置く）:

- **「2 つの別の論点を混同している」と切り分けてから答える** ——
  *"You are confusing two separate issues: 1. … 2. …"*（2024-07-16）。
- **「〜への fall-through があっても、そのライセンス自体は open source ではない」** ——
  ***このライセンスは* open source か**と**その先で何が起きるか**を分けて問う（2024-10-03）。
- **起草の粗さを、OSD 違反とは別に指摘する** —— *"there are better ways of drafting this … it needs to
  be clear in a legally robust sense"* と述べつつ *"doesn't appear to conflict with OSD6"* と分ける（2024-10-06）。

**ACD にとっての含意**: **この人の型は「境界を切って別々に問う」**で、
**ACD が §3 / §4 / §5 を並置していること**は、まさにその型が当たる構造である。
**想定される問い**: 「献呈が効いた法域と効かない法域で、あなたは*同じ*ライセンスだと言えるのか」。
**答えは §4.4 と §2.4 にあり**（許諾は §3 と独立に付与され、受領者は §3 の有効性を判断しなくてよい）、
**`review-responses-clauses.md` の §4 の問答が既にその形で書かれている。**

**⚠ 確立しないこと**: 本人が ACD について何か述べた記録は**無い**。これは
**「返信を書く人の型」を先に読んでおく**ための記録であって、予測ではない。

## §1.98 と §1.99 の移転先

**2026-09-19 に `LICENSES/ACD-1.0.review-labels.md` へ切り出した**（Check 365 の 1,000 行に当たったため）。
**節番号は動かしていない**ので `§1.98` / `§1.99` への既存参照はそのまま意味を保つ。

- **§1.98 「クレヨン・ライセンス」** —— 誰が書いたかの label。**Licensing Committee 委員長の
  *unpredictable interpretation* の一文**はここにある。
- **§1.99 「vanity license」** —— 誰のためのテキストかの label。**OSI の Proliferation Report に
  定義があり、Marc Jones 氏の 4 段テストに 1 つずつ当てた結果もここにある。**

**この 2 つを分けた理由**: 他の §1.x は「**特定の人 / 特定の提出**についての記録」だが、
§1.98 / §1.99 は「**リストが我々の類型に付ける呼び名**についての記録」で、読む動機が違う。

## 1.106 steward 自身が公開の場で展開した分析を、我々は回数として数えていた（2026-09-22）

**オーナーの指摘**: *「使って無かったがそもそも勿体ない。それこそ固定観念やんけ」*。

**ドシエは steward の list 上の寄稿を「4 通送信・4 人が関与」「Duan 氏が three-axis framing を
引いた」と**注意の計量**として記録してきた。**中身を使ったことは一度も無い。**

**アーカイブから中身を出す。5 件あり、そのうち 3 件は ACD-1.0 自身の設計に直接効く。**

| 日付 / 場 | 何を論じたか | ACD-1.0 のどこに効くか |
|---|---|---|
| 2026-09-03 `license-review`（OpenMDW）| **終了条項の限定原理** ——OpenMDW-1.1 は著作権・特許・営業秘密・データベース権を付与しながら、**終了の引き金は特許と著作権の訴訟に限られる**。*"That creates an apparent asymmetry between the scope of the grant and the scope of the termination trigger, and I would like to understand whether that asymmetry is deliberate."* | **§10.4** ——ACD は**終了条項を持たない**。非対称が生じる余地そのものが無い |
| 2026-09-03 `license-review`（ModelGo）| **hosted-only の Distribution で §2.2(a) の条件がどう働くか** ——定義は API / web アクセスを Distribution に含むのに、課される条件は複製の引き渡しを前提にしている | **§6.4 / Computational Use** ——ACD は出力にもモデルにも何も課さないので、この gap が生じない |
| 2026-09-04 `license-review`（OpenMDW）| **threshold question の切り出し** ——*"whether copyright litigation may legitimately trigger termination"* を、nexus（請求と対象の近さ）と proportionality（結果の広さ）から分けた。**佐渡氏の論点を名指しで受けて発展させ**、Gay 氏・Chestek 氏がこの段落を引いた | **§10.4 + §8.2**（報復条項が無いことは設計であり、§8.2 がそれを明示する）|
| 2026-09-06 `license-discuss`（ACD-1.0）| **§3 と §4 の 1 点に絞った threshold question。** 2020 年の Unlicense 審査を読んだうえで、*"I do not regard approval of the Unlicense as controlling precedent for ACD-1.0"* と**自分から先例性を退けている** | **B4**（献呈と許諾の並置）——register は「Unlicense が先例」と「legacy ゆえ切り離されうる」の両方を書いているが、**steward が自分で先例扱いを退けている事実を使っていない** |
| 2026-09-06 `license-discuss`（network copyleft）| **trigger と scope は独立した設計次元である** ——*"the event that triggers reciprocity and the code to which reciprocity applies are separate drafting dimensions"*。CPAL-1.0 を例に挙げた | 同上（終了・報復の設計を語る語彙そのもの）|

### なぜこれが使える材料なのか、そして使えない部分

**使える**: **これは我々のドシエの中の主張ではなく、`license-review` 上で OSI の参加者に当てられ、
受け止められ、引き継がれた推論である** ——佐渡氏が発展させ、Gay 氏と Chestek 氏が引いた。
**「我々がそう書いた」と「公開の場で当てて誰も倒さなかった」は別の強さを持つ。**

**⚠ 使えない**: **これは B1 を治さない。** 弁護士のレビューではないし、
**他人の instrument について正しく論じられることは、自分の instrument が正しい証拠ではない。**
**そして自分の分析を自分の支持として引くのは循環に近い** ——だから
**引くのは結論ではなく、その推論が公開で当てられたという事実だけにする。**

**⚠ さらに**: 上の 3 件が効くのは**「ACD が終了を持たないのは設計である」の説明**であって、
**終了を持たないこと自体の正当化ではない**（それは #46 が費用込みで記録している）。

## 1.107 第 4 系統を初めて通した —— OpenMDW / ModelGo 審査を「設計の作業」として読む（2026-09-22）

**#205 で経路を開いた。ここはその最初の通し。** 対象は `license-review` の OpenMDW 審査
（**85 通・85,884 語・2026-08-13〜08-31** と 9 月の続き）と ModelGo。
**読み方は「この反論は我々に当たるか」ではなく「彼らが作業した結果は何か」。**

### (A) 委員長の一般則 —— 冗長な条項は無害ではない。そして ACD は最後の鎖で切れている

> *"The licensor has a typical statement that the materials are provided as-is (and disclaimers of
> warranty and liability) so the above clause is, in my opinion, **redundant or unnecessary**.
> **The problem with having it is that it can be construed as a positive duty under the license
> which can be breached, terminating the license.** This seems problematic; **no other widely used
> open source license come to mind that impose burdens beyond the license notice, attribution and
> copyleft**."*
> —— Pamela Chestek 氏・`license-review` 2026-08-16（佐渡氏が 08-19 に同じ段落を引いて議論を続けた）

**一般則**: **冗長 → 義務と構成されうる → 破られうる → 終了する。**

**ACD-1.0 への当たり方**: **最後の鎖が存在しない。§10.4 は終了条項を持たず、
*"contains nothing that You could breach"* と述べる。** したがって
**この一般則が向かう先は ACD では起きない。**

**⚠ ただし最初の鎖は残る。** 「冗長な条項が義務と構成されうる」までは当たり、
**ACD は冗長な条項を意図的に持ち、本文でそう述べている**
（§4.4 *"this Section is redundant but not void"*、§6.5 *"states expressly what Sections 3 to 5
would in any event permit"*）。**答えは no-condition mesh**（§10.1 / §10.3 / §10.5 / §11.3 / §11.4 / §16.6）
**だが、その mesh の 1 文が限定を欠いていることは E9 / #57 が既に記録している。**

**⚠ そして「他の広く使われる OSS ライセンスは notice / attribution / copyleft を超える負担を課さない」
という後段は、ACD には**有利**に当たる** ——**ACD はそのいずれも課さない**（§10.2）。

### (B) 提出者側の設計論 —— estoppel に委ねるか、条文に書くか

> *"a party should not be able to exploit a work while maintaining that the work is unlawful.
> OpenMDW-1.1 **writes that expectation into the license prospectively and neutrally, for everyone
> equally, instead of leaving it to after-the-fact estoppel and waiver arguments**."*
> —— Michael Dolan 氏（OpenMDW steward）・2026-08-24

**ACD-1.0 は反対の側を選んでいる。** §2.5 は **estoppel** そのものである ——
*"The Dedicator will not assert that this Dedication is revocable … and **is estopped from doing so**"*。

**⚠ 向きが違うので直接の対立ではない。** Dolan 氏が条文化したのは**受領者**に対する期待
（訴えながら使い続けるな）で、**ACD の §2.5 は Dedicator 自身を縛る**。
**ACD は受領者に何も課さないので、条文化すべき期待がそもそも無い。**
**だが「estoppel に委ねるのは弱い」という彼の論は、§2.5 の強さについての問いとして残る**
——そして **#135（Perens 氏「献呈として読まれ、grantor をどれだけ拘束するか疑問」）と同じ根**である。

### この節が establish しないこと

**どちらも ACD-1.0 について述べられたものではない。** 我々が当てただけである。
**(A) は我々に有利に働く**ので、**#83 が自分に課した規律（我々宛でないものを我々の証拠にしない）が
より強く当たる** ——有利な向きだからこそ、確立する範囲を狭く書く。


## §1.99 B14 の moderator が引いた CoC 条項は、その 12 日前に、AI とは無関係に、人間へ向けて引かれていた

**2026-09-22 に、未読スレッドの全数列挙から出た 1 通**（`rounds/2026-08-28-license-review-villa-volume-etiquette-observed.txt`）。
**件名だけを見て飛ばしていた** —— *"Reminder of list etiquette around volume"* は、
我々がライセンスの話として探していた語を 1 つも含まない。

> *"a polite reminder that **the list's code of conduct has, since it was first written, asked
> people to respect each other's precious time by being concise and low-volume**. **The people we
> most need on this list are those whose time is very precious.**"*
> —— Luis Villa 氏・`license-review` 2026-08-28（OpenMDW 審査スレッド中、Rob Landley 氏宛）

**B14 の moderator 通知（2026-09-09）が引いたのは、同じ条項である** ——
*"this behavior goes against the **"Respect time and attention"** from our Code of Conduct"*
（`rounds/2026-09-09-license-review-osi-moderators-observed.txt`）。

### 何が establish されるか

**(1) この規範は AI のために作られたものではなく、AI とは無関係に運用されている。**
我々は既に「現行 CoC の実質は簡潔さで、AI への言及は 1 語も無い」を**条文で**確かめていた
（B14）。**これはその条項が実際に list 上で発動した記録である。** 条文が在ることと、
社会的に強制されていることは別で、**後者を示す一次資料をこれまで持っていなかった。**

**(2) 同じ機構が、別の人物から独立にもう一度述べられている。** *"The people we most need on this
list are those whose time is very precious"* は、**委員長が 3,888 語 / 約 4,500 語の提出に
engage しなかった記録（#116）と同じ論理**である。**#116 は行動からの推定だったが、これは
明示された規範である。**

### ⚠ 逆側 —— 同じ 1 通が、長さの弁護にもなる

> *"This particular license is **obviously a complex problem and requires complex discussions**,
> so **the word count is going to be high**, but that's all the more reason to get to the point
> whenever possible."*

**複雑な instrument について volume が高くなること自体は、この list で正当と述べられている。**
**ただし述べられているのは*議論*の volume であって、*ライセンス本文*の語数ではない** ——
**B3（本文 4,896 語）へ流用してはならない。** 括ると片方の測定が他方の弁護に使われる
（#116 が記録した誤りと同じ形）。

**当たるのは `review-corpus.md` §1.80 の軸**（提出メールの長さ・我々は 94 パーセンタイル）である。
**§1.80 は「長さは engagement を予測しない（corr = −0.02）」と測った。この 1 通はそれを覆さない**
——相関が無いことと、規範が存在することは両立する。**変わるのは、短くする理由が
「返信が増えるから」ではなく「list が明示的にそう求めているから」になる**ことである。

### この節が establish しないこと

**我々について述べられたものではない。** 名指しされたのは Rob Landley 氏で、
**その文脈には Villa 氏が「他の人に任せる」と述べた人身攻撃の問題が併存している** ——
**volume の指摘だけを切り出すと、その 1 通の実際の主題を狭く伝えることになる。**

**そして Villa 氏は OSI の役員でも moderator でもない**（末尾の定型文が
*"The opinions expressed in this email are those of the sender and not necessarily those of the
Open Source Initiative"* と述べている）。**これは参加者の発言であって OSI の立場ではない。**

## 1.113 OSD に書かれていない審査基準を、参加者自身が列挙している —— そしてその一覧は我々の bottleneck 表とほぼ同じである（2026-09-26）

一次資料は `rounds/2017-09-license-review-license-zero-reciprocal-observed-*.txt`（220 通・22 部）。
**記録の中で、単独の起草者による審査がいちばん長く続いた例**（2017-09〜2018-12・15 か月）で、
**主題（maximalist copyleft）は ACD とは遠い。還元するのは手続きと基準についてだけである。**

### 「OSD を満たすこと」は必要条件であって十分条件ではない、と 3 人が別々に述べている

John Cowan 氏 2017-09-26 —— 提出者の *"OSI approval goes only to license terms"* に対し、
*"Actually, that turns out not to be the case. **The OSI approves OSD-conforming licenses only if
it believes that they further the goals of OSI.** That is part of the reason why license-review
exists, and why the Board is far from being a rubber stamp."*

Bruce Perens 氏（提出者が電話の内容を同日リストへ要約・本人 CC）2017-09-27 ——
*"licenses that conform to the Open Source Definition are open source licenses, but **some licenses
that conform to the Open Source Definition come before OSI, and leave without OSI approval**.
**Poorly drafted terms conceived by amateur drafters** came up a few times. As did needless,
proliferating reimplementations of existing terms."*

Bruce Perens 氏 2017-11-07 —— *"while I can reject it strictly on OSD grounds, **I should really
stress that this is an issue of principle. OSI should not endorse that sort of poor bargain with
certification of the license.**"*

### 元理事が、書かれていない基準の存在を名指ししている

Luis Villa 氏 2017-10-24 —— *"it has never been explicit or clear either. And has led to many, many
rounds of confusion ... not to mention many (accurate?) accusations that **OSI approval is a
political game, not an actual objective test**. If the board wants to be transparent about the
current situation, it should amend the OSD to add: **'11. Whatever OSI's then-current board feels
is the interests of the open source movement.'** That wouldn't be ideal, but at least it would be
accurate and transparent."*

**これは `board-decisions.md` が記録した理事会の 2 つの天井** ——
*"consensus … even where they cannot identify a specific aspect of the OSD"* と
*"prior approval … does not bind"* —— **と同じことを、書かれていない側から述べている。**

### そして、その「書かれていない基準」の一覧が在る

Rick Moen 氏 2017-10-25、`https://opensource.org/approval` に載せるべき文面として ——

> *"Reasons participating individuals have cited for disinterest in some past licenses include
> perception that the license is a **vanity license or duplicative**, that it is **needlessly
> specific to one business entity**, that it is **unjustifiably opaque or ambiguous in its
> wording**, that it **was not drafted with a lawyer** ..."*

**4 項目のうち 4 つが、我々の bottleneck 表にそのまま在る**
（`ACD-OSI-BOTTLENECKS.md`）——
vanity = **B6** / duplicative = **B10 と #84** / one business entity = **提出パケット §4b** /
opaque or ambiguous = **B3 + B13** / not drafted with a lawyer = **B1**。

**これは我々の表が正しいことの証明ではない** ——**参加者が挙げた理由と、我々が自分で挙げた弱点が
一致した、という事実だけである。** だが **register を「我々の心配事の一覧」ではなく
「リストが実際に挙げてきた理由の一覧」として読んでよい**ことの、独立した裏づけではある。

### chicken-and-egg を、提出者が 2017 年に名指ししている

Kyle Mitchell 氏 2017-10-24 —— *"I'd imagined that I would find terms acceptable to OSI, start
using it and promoting its use ... and then approach SPDX with that evidence of use 'in the wild'
to hand. It's a goal of the license to be OSI-approved. **That creates a certain loop** ...
**The chicken-and-egg problem is a well-known brake on proliferation**"*

**我々の B2（採用 1 件）と B11（SPDX を意図的に見送っている）は、この loop の両端である。**
**同じ loop を、9 年前に別の提出者が同じ言葉で述べていた** ——
**我々の見送りの理由づけが特異なものではないことの裏づけになる。**
**⚠ ただし loop を名指しできることと、loop から出られることは別である。**

### 凍結の理由が、リスト側の言葉で在る

Josh Berkus 氏 2018-06-19 —— *"L0-R is a great example of where some format other than email would
help a LOT. Like, **I can't tell you whether I personally approve of the license at this point or
not, because I've completely lost track of what the current text is**, and what the lawyers had to
say about the meaning of certain pieces of language."*

**これは審査中に本文を書き直し続けた結果である。** `REVISION-PROTOCOL.md` §2 の凍結
（Check 453 が sha256 で機械強制）は、**我々の礼儀ではなく、審査者がこの状態に陥らないための
手段**だと、リスト側の言葉で裏づけられる。
**⚠ 逆側**: 凍結は**審査中に見つかった欠陥を直せない**ことでもある（errata の E 系列はその費用で、
`ACD-1.0.errata.md` が数えている）。**どちらを選んでも費用は消えない。**

### 結末

Richard Fontana 氏 2018-12-07 —— *"In my most recent License Committee Report **I recommended that
the OSI reject L0-R**. Subsequently, however, at its November board meeting, **the OSI chose not to
make any decision on L0-R, because it appeared that the license submitter had effectively withdrawn
the license from consideration**."*

**220 通・15 か月・弁護士である単独起草者・複数回の本文改訂の末に、決定は出ていない。**
**`board-decisions.md` §2b が記録した「取り下げは終端ではなく経路」と、
#139 の「第 3 の帰結（承認でも否決でもない留め置き）」の、3 つ目の形である。**
