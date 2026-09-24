---
file: LICENSES/ACD-1.0.board-decisions.md
audience: 次のセッションの実装者（一次読者）/ OSI license-review participants / 監査人
last-updated: 2026-09-24
canonical-ref: LICENSES/rounds/2026-09-13-osi-board-meeting-minutes-2025-06-to-2026-06.txt (逐語の一次資料) / LICENSES/ACD-1.0.review-corpus.md (アーカイブ全体の測定) / LICENSES/ACD-OSI-BOTTLENECKS.md (B2 / B10)
---

# OSI 理事会の決定 —— 議事録という一次資料から

**この文書の対象は「理事会が何を決めたか」である。** メーリングリスト上の議論は
`ACD-1.0.review-corpus.md`（アーカイブ全体の測定）と `ACD-1.0.review-precedents.md`
（個別スレッドの読み）が扱う。**同じ出来事について、リストは議論を、理事会は決定を残す。**
**節を足すときは、その文が「議論」か「決定」かで行き先を決める。**

**一次資料は `rounds/2026-09-13-osi-board-meeting-minutes-2025-06-to-2026-06.txt` に無改変で在る。**
ここに書くのは分析であり、逐語の権威はあちらである。

## 1. 何を読んだか、そして公開分が不完全であること

**このドシエの「結果」データは、2026-09-13 まで `license-review` の告知メールだけに依っていた**（§1.68 / §1.69）。
告知は提出型スレッド 21 件のうち **8 件**しか出ておらず、残り 13 件の帰結は不明と記録してあった。
**決定そのものは理事会で動議として記録される。** 2026-09-13 に
`https://opensource.org/minutes` から**公開されている全 12 回**（2025-06-20〜2026-06-29）を取得し、
逐語を `rounds/2026-09-13-osi-board-meeting-minutes-2025-06-to-2026-06.txt` に保存した。

**⚠ 公開分は不完全である。** 索引ページ自身が *"This page is under construction … If you can't find
the minutes here, check the wiki"* と述べ、**索引に並ぶ最古が 2025-06-20**（ページ作成は 2007 年）、
**最新が 2026-06-29**。**「議事録に無い」は「決定が無かった」を意味しない。**
§2〜§8 の件数はすべて**索引に並ぶ 12 回の範囲での**件数である。

### 1a. 🔴 訂正（2026-09-20）—— 索引に無いだけで、2005 年以降の議事録は公開されている

**上の「最古が 2025-06-20」は、索引ページについての事実であって、公開されているものについての
事実ではなかった。** OSI 自身のライセンス API（`review-rules.md` §1.102）は各ライセンスに
`board_minutes` のリンクを持っており、**そこを辿ると 2005-09-12 から 2026-06-29 まで
36 回分が実際に開ける**（`https://opensource.org/meeting-minutes/<日付>`）。

**一般形: 索引に載っていないことは、公開されていないことの証拠ではない。**
**我々は索引を読んで「公開分は 12 回」と書き、その 1 週間後に 36 回を開いた。**
**⚠ ただし完全でもない** —— 8 件の `board_minutes` は `wiki.opensource.org` を指しており、
そこは**現在 XWiki 社の宣伝ページに解決する**（**Unlicense と MIT-0 の決定回がこれに当たる** ——
**我々にとって最も近い 2 つの先例の決定記録が、OSI 自身のリンクから辿れない**）。
2010 年代の一部のページは本文が空で、cookie バナーしか返さない。

## 2. 🔴 第 3 の帰結 —— 「reject」ではなく「not approved」。そして我々の輪郭がそこに当たる

**License Committee が理事会に直接こう問うている**（2025-07-18・逐語）:

> *"The license committee requests clarification on whether it's possible to reject licenses entirely
> on **non-proliferation grounds**; particularly, **should the LC reject a license proposal that is
> valid but is not in use anywhere?**"*

**理事会の答えは 3 文である。**

> *"The board agrees on the goal of **limiting license proliferation** and insists that it should be
> communicated clearly on the License process page first. Also, the board agrees that **a license
> should be rejected only if it violates the OSD**. **But a license could stay in a status where it is
> not approved if it is duplicative and not used by a project.**"*

**「有効だが、どこでも使われていない」提出は、否決されるのではなく「承認されない状態に留まりうる」。**
**これは我々のドシエが持っていなかった状態である** ——§1.68 / §1.69 の分布は**承認 / 否決の 2 値**で、
**「否決もされないまま承認されない」は数えられていない。** そして
**duplicative（#84「なぜもう一つ PD 等価を？」）** と **not used by a project（B2 = 採用 1 件）**の
**両方が我々に当たる。**

**この 3 文は、同時に 1 つの天井を弱める** ——§1.67 は
*"consensus … even where they cannot identify a specific aspect of the OSD … that is not met"* を
引いて「OSD 違反を指摘できなくても却下しうる」と記録した。**理事会は「OSD に違反する場合にのみ
*reject* する」と述べている。** **矛盾ではない** ——両立する読みは、
**「reject は OSD 違反に限るが、承認しないことは OSD 違反を要しない」**である。
**その読みが正しければ、我々にとって天井は下がっていない。名前が変わっただけである。**

### 2a. 逆から読む —— この 3 文には、我々に有利な面が 2 つある（そして片方は、同じ記録に潰される）

**上の段落は、有利な材料を見つけた直後に不利な結論で閉じている。** オーナーからの依頼
（*"常に逆説もセットで考えてね"*・2026-09-13。**オーナーは指示を出さない —— 全面委任を成立させる
ための意図的な姿勢であり、canon の Check 102g がこれを強制している**）を受けて読み直すと、
**書き落としていた面が 2 つある。**
**#131 が記録したとおり、不利な一覧を持つ規律は、自分に不利な誤りを検算しにくくする。**

**有利 (1) —— 「承認されない」と「否決される」は、我々にとって同じ重さではない。**
否決は**公表される判断**であり、記録には理由が残る（*"does not comply with the OSD"* 等）。
**「承認されないまま」には、OSD 不適合の認定が無い。** 本ドシエの姿勢は *"check us, do not
believe us"* であり、**その姿勢は「OSD に違反すると判断された」という一行によって最も傷つく。**
**留め置きはそれを生まない。** そして留め置きは**終端ではない** ——§2b が示すとおり、
**この記録の中で、いったん取り下げられたものが後に承認されている。**

**有利 (2) —— 否決の門は、理事会自身の言葉で狭められている。**
*"a license should be **rejected only if it violates the OSD**"*。
§1.75 は「我々に当たりうる否決理由の束は**起草の粗さ・解釈問題**だけ」と記録した。
**その束が否決になるには、OSD 違反を経由しなければならない**ことになる。

**⚠ そして有利 (2) は、同じ議事録の 2 か月後に潰される。**
2026-02-20、理事会は Project Tick GPL をこう否決している:

> *"rejects the Project Tick GPL because **ambiguities in drafting make it impossible to determine
> whether or not it complies with the OSD**."*

**これは「起草の粗さ」から「OSD 違反」への橋が、記録の中で既に架けられている実例である。**
**曖昧さは、OSD 違反の認定ではなく「OSD 適合を判定できないこと」を通って否決に至る。**
**したがって門は狭まっていない** ——狭まったのは*語*であって*経路*ではない。
**B13（理解コスト）と B3（長さ）の重みは、この実例のぶんだけ上がる。**

**残るのは有利 (1) だけである。** だがそれは**結果の質**についての話で、**承認確率には効かない。**
**「最悪の結果が少しましになる」ことと「良い結果が近づく」ことを混ぜない。**

### 2b. 取り下げは終端ではない —— 同じ記録の中で、取り下げられたものが承認されている

**本ドシエは提出を「一発勝負」として扱ってきた。** 記録はそう読めない。

| 日付 | NIST Software License について議事録が述べていること |
|---|---|
| 2025-12-19 | *"The committee **has withdrawn** the NIST Software License (Legacy) and the Irrevocable MIT License"* |
| 2026-01-16 | *"NIST Software License and ModelGo Licenses (OSAID) are **still in discussions**"* |
| 2026-02-20 | *"the Board … **approves** the NIST Software License in the Legacy category"* |

**「取り下げ」の語が何を指していたかは、議事録からは決まらない**（版の取り下げか、議題からの
取り下げか、審査そのものの取り下げか）。**そこは確定させない。**
**確定できることは 1 つ ——それが何であれ、審査を終わらせなかった。**
2 か月後には「議論継続中」と述べられ、その翌月に**承認されている。**

**これは §1.82 で引いた process ページの規則と整合する** ——
*"the current version of the license should be **withdrawn from review and an updated version
submitted**"*。**取り下げは、手続きが想定している通常の一手である。**

**帰結（分岐 B の判断に直接効く）**: **提出の不可逆性を、実際より高く見積もっていた。**
`REVISION-PROTOCOL.md` §2 は今日、取り下げを**本文を差し替えるときの機構**として書き足したが、
**それは同時に「出してみて、必要なら退いて、出し直せる」という意味でもある。**
**⚠ ただし逆側も書く**: 退いて出し直すたびに **Decision Date の時計は動き**（改訂版は提出から
30 日・初回から 60 日を下回らない / 委員は *"two months from your **final** submission"*）、
**process ページは「何度も取り下げて出し直すな、変更はまとめて 1 回で」と明文で戒めている。**
**安いのは「退けること」であって「何度も退くこと」ではない。**

## 3. 🔴 その区別は、14 か月経っても公表されていない

同じ議事録の次の文はこう続く:

> *"The License committee will **articulate the difference between "reject" and "not-approved"** and
> submit changes that clarify this and **other non-OSD criteria** on the License process page
> **before the next board meeting**."*

**2026-09-13 15:00 JST に process ページを実測した結果**:

| 語 | 出現 |
|---|---|
| `prolifer`（proliferation 等）| **0** |
| `not-approved`（状態としての）| **0** |
| `non-OSD` | **0** |
| ページの自己申告 last modified | **March 13, 2024** |

**「次の理事会まで」と述べられた改訂は、14 か月後の今日も入っていない。**

**そしてこれは 1 件ではない。** 2026-01-16 の議事録にも同じ形がある ——
*"BarrerSoftware License **will be withdrawn** as it is a non-commercial license. **We have to update
the list of common problems with licenses to make it clear that non-commercial licenses will be
withdrawn**."*
**拒否理由ページを実測すると、`Non-commercial and ethical clauses` の項は在るが、
それが*否決*ではなく*取り下げ*になると述べる文は無い**（同ページの `withdraw` の唯一の出現は
cookie バナーである）。**ページの自己申告 last modified は March 12, 2024** ——
**この指示より 22 か月前である。**

**⚠ 一般化しすぎない。** 言えるのは **「理事会が公表を指示した 2 件が、公表されていない」**ことだけで、
**OSI のページ全般が古いとも、指示が無視されたとも述べていない**（内部で進行中かもしれない）。
**我々にとっての含意は 1 つだけ ——公表された基準を読み尽くしても、委員会が実際に使う基準を
読み尽くしたことにはならない。**
（`duplicative` は 1 回出るが *"Purpose of the process: Discourage duplicative and poorly written
licenses"* で、**2024 年から在る文言**である ——**懸念は目的として公表されているが、
帰結の状態と非 OSD 基準は公表されていない。**）

**これが提出戦略に効く。** 我々は**公表された基準**（8 条の standard / OSD / 拒否理由ページ /
提出要件）を原典で読み、1 項目ずつ当ててきた。**だが我々の輪郭に最も当たりうる基準は、
そのどれにも書かれていない。** **公表されていない基準に対しては、当てて確かめることができない。**

**打てる手は 1 つだけある** ——**先に自分から名指しする。** #84 への答え
（「この類型に 1 件足す費用が低い」・`comparison.md` §1）は既に書いてあるが、
**それは「重複」への答えであって「重複 かつ 未使用」への答えではない。**
**後者は B2 と結ばれており、B2 は AI には解けない**（採用の捏造は失格事由・制御できるのは
discoverability だけ）。**ここは「答える」ではなく「知っていると示す」ことしかできない。**

## 4. 🔴 応答しない提出者は、理事会の議決なしに却下できる（2026-05-22）

> *"Motion: Carlo moves that the Open Source Initiative Board of Directors **authorize the License
> Committee to reject a license without Board approval when the submitter does not respond to
> requests for information or explain how they have responded to constructive feedback**."*
> Second: Thierry seconds. Result: All others approve.

process ページは以前から *"If they are not [responsive] … the license will be at **high risk of
rejection**"* と述べていたが、**2026-05-22 にそれが委任された権限になった。**

**我々にとっての意味を、正確に書く。** **いま危険が現実化しているわけではない**
——`license-review` に ACD-1.0 を出していないので、却下されうる係属中の提出が無い。
**だが条件付きの危険は実在する**: 2026-09-13 に確認したとおり、
**我々が `license-review` へ送った substantive なメッセージ 2 通は moderation に拒否されて届いていない**
（#128）。**リストの側から見れば、「送れていない」と「応答しない」は区別がつかない。**
**提出するなら、この経路が通ることを先に確かめる必要がある。**

**そしてこの帰結には、既に実例が 2 件ある。** 2026-01-16 の議事録 ——
*"QmDeve License and CinqXaero Open Source License are **likely to be withdrawn because of the lack
of communication with their submitters**."*
**取り下げの理由が、本文の欠陥ではなく「連絡が取れないこと」だけで記録されている。**
**2026-05-22 の委任は、この運用を権限として明文化したものである。**

**我々に当てはまる形を、正確に書く。** 我々は**沈黙していない** ——投稿し、5 問に当日回答している。
**だが我々の 2 通はリストに現れておらず、リストの記録だけを見る人には沈黙と同じに見える。**
**これは「不当に扱われる」という主張ではない**（誰も我々をそう扱ったという証拠は無い）。
**述べているのは、我々の側の記録と、リスト側から見える像が食い違っているという事実だけである。**

## 5. 公開 12 回で読める決定（告知メールより多い）

| 日付 | 決定 | 対象 | 記録された理由 |
|---|---|---|---|
| 2025-07-18 | 承認 | WordNet（legacy）/ CDDL1.1（legacy）/ **BSD-3-Clause-Open-MPI（regular）** | — |
| 2025-11-21 | 否決 | AFN License | *"does not comply with the OSD"* |
| 2025-12-19 | 否決 | Orivex Syscall License | **3 つ**: *"multiple drafting problems"* / *"Submitter has not responded to legal feedback"* / *"did not supply full information for the review request"* |
| 2025-12-19 | 取り下げ | NIST Software License（Legacy）/ **Irrevocable MIT License** | 委員会による withdraw |
| 2026-02-20 | 否決 | IDCIYMI-1.x / **Project Tick GPL** | 後者: *"ambiguities in drafting make it impossible to determine whether or not it complies with the OSD"* |
| 2026-02-20 | 承認 | NIST Software License（Legacy）| **一度取り下げてから承認された** |
| 2026-04-17 | 承認 | Curl License（legacy）| — |
| 2026-05-22 | 否決 | Free Archive License 1.0 / Open Source Copyleft License 1.0 / Dolby ATMOS/Vision FOSS 1.0 / **Modified 0BSD Standard License (Maintenance Required)** | — |
| 2026-06-29 | 承認 | CNRI-Python-GPL-Compatible（Legacy・supersede）/ Python-2.x | — |
| 2026-06-29 | 否決 | **キリル文字表記の露語ライセンス**（名称の逐語は `rounds/` の議事録にある ——**分析側にキリル文字を書き写さない**: Check 450 が日本語文への別スクリプト混入を BLOCKING で止めており、**逐語は無改変保存の側に置き、分析側は記述で指す**のが本ドシエの分け方である）| *ISC の翻訳であり、ISC は既に承認済み* |
| 2026-06-29 | **方針** | — | *"the board will not approve **translations** for approved licenses"* |

**承認 8・否決 9・取り下げ 2（公開 12 回の範囲）。** §1.68 の告知ベースの数（承認 4・否決 8・
期間はより長い 33 か月）より**多い** ——**告知メールは決定の部分集合である。**
**そして承認 8 件のうち 7 件が legacy か既存テキストで、"regular" は BSD-3-Clause-Open-MPI 1 件だけ。**
**§1.68 の「承認はいずれも既存テキスト」は、より良い資料でも崩れない。**

## 6. 有利な事実 2 件（同じ規律で書く）

**(1) AI/ML 向けライセンスは審査対象であり、承認されうる。** 2025-07-18 に理事会が確認している ——
*"when reviewing a license for an OS model, the committee can still **review the license against the
OSD and standard license criteria**, independently of the fact that the system can conform to the
OSAID or not"*、そして *"**When licenses aimed at AI/ML projects are approved**, OSI will clearly
communicate the difference between a license approval and OSAID compliance."*
**「承認されるとき」と書いてある。** OSAID 適合は承認の条件ではない（#62 の関心事に対する答え）。

**(2) 固有名詞を持たないことは、委員会が実際に気にしている性質である。** 2025-10-17 に理事会は
**「委員会が任意のライセンスを genericize（固有名を placeholder へ置換）する権限」を、
追加の理事会投票なしに**与えている ——きっかけは *"a license that was identical to the BSD-LBNL,
except for the names of the departments"* だった。**提出パケット §4b（本文の固有名詞 0・置換テキスト 0（§16.1 の推奨 notice の雛形 1 欄 `<location of this file>` を除く —— 採用者が自分の notice に書く欄で、本文は編集しない）・
採用に本文編集が 1 箇所も要らない）は、我々が思いついた論点ではなく、
委員会が現に手を動かしている論点である。**

## 8. 2005〜2026 の 36 回から出た決定（2026-09-20 取得）

**動議は理由つきで記録されている。** ACD に当たるものを、有利・不利の両方で並べる。

### 8.1 🔴 **我々と同じ類型が、まさにその理由で却下されている（2009-03-04・WTFPL）**

Licensing Committee の報告が理事会の議事録に逐語で入っている:

> Title: WTFPL … Comments: **It's no different from dedication to the public domain. Author has
> submitted license approval request — author is free to make public domain dedication.**
> Although he agrees with the recommendation, Mr. Michlmayr notes that **public domain doesn't
> exist in Europe.** Recommend: **Reject**

**却下の理由は「悪い条文だから」ではない。「それはライセンスでなく献呈であり、献呈は自分でできる」である。**
**これは #84 と B4 に対する、これまでで最も正面からの反証**で、
*「公有化の献呈は、それ単体では open source ライセンスとして承認されない」*という
我々が §7 handoff に書いてきた命題の、**理事会側の出典**でもある。

**⚠ そして同じ 4 行に、我々の §4 が存在する理由も書かれている。**
**推薦に同意した委員自身が「ヨーロッパに public domain は存在しない」と付言している。**
**ACD-1.0 の構造 ——§3 が献呈で、§4 が §3 と独立に付与される許諾—— は、
この 2009 年の記録の中で、反対意見と反論が同じ段落に並んでいる当のものである。**
**⚠ ただし WTFPL は許諾条項を持たない。** ACD は持つ。**だから同じ結論になるとは限らない**
——**が、「献呈と同じに見える」段階で止められる危険は、実例で示されている。**

### 8.2 🔴 **長さ・複雑さ・曖昧さが、承認でも却下でもない決議を生んだ（2017 秋 f2f・NOSA 2.0）**

> Resolved, That, **in view of the length, complexity, and ambiguities in the submitted drafts of
> the NASA Open Source Agreement version 2.0, it is the opinion of the OSI that the conformance of
> NOSA 2.0 to the OSD cannot be assured. OSI thus can neither approve nor reject the license**, and
> NASA is invited to submit a new draft of NOSA for consideration by the OSI.

**B3（長さ 4,896 語）と B13（審査者の理解コスト）が、抽象的な懸念ではないことを示す決議である。**
**「OSD に適合しない」ではなく「適合を確かめられない」で止まっている** ——
`review-corpus.md` §1.82 が記録した Project Tick GPL の *"ambiguities in drafting make it
impossible to determine whether or not it complies with the OSD"* と**同じ構造**で、
**こちらは 2017 年、あちらは近年**。**橋は 1 本ではなく 2 本架かっている。**
**⚠ 逆側**: NOSA は**条件と義務を持つ長い契約**で、ACD は §10.1 により条件を持たない。
**長さの由来が違う**（あちらは義務、こちらは説明）。**だが「読んで確かめられるか」は同じ問いである。**

### 8.3 第 3・第 4 の帰結が、20 年にわたって使われている

| 年 | 文言 | 帰結 |
|---|---|---|
| 2007-06-06 | *"we **decline to approve at this time** and suggest that the committee in future consider compatibility for licenses that advertise simplification"*（Simple Public License）| 承認でも却下でもない |
| 2009-03-04 | *"Discussion continues, but Bruce says **'Deny approval' because the benefits aren't worth the cost**"*（TGPPL）| **費用対効果**で語られている |
| 2017 秋 | *"can **neither approve nor reject**"*（NOSA 2.0）| 上記 |
| 2025-07-18 | *"could stay in a status where it is **not approved** if it is duplicative and not used by a project"* | §2 |

**「承認か却下か」で数えてきた我々の分布は、20 年分の記録に対して粗すぎた**（#139 の続き）。

### 8.4 翻訳は、3 か月前に方針として閉じられた（2026-06-29）

> Motion: McCoy moves to adopt a policy that **the board will not approve translations for approved
> licenses.**

同じ回に、**キリル文字表記の露語ライセンス名**の 1 件が
*"as this is a translation of the ISC license which is already approved"* として却下されている。
（**名前はここに書き写さない** ——`rounds/` の逐語保存には在るが、Check 450 は日本語テキストへの
別スクリプト混入を BLOCKING で止める規約で、**その Check 自身の注記が同じ理由で同じ扱いをしている。**）

**ACD-1.0 §16.5 は翻訳を「改変されたテキストではない」として名称の下での頒布を許す。**
**この方針は「翻訳を承認しない」であって「翻訳を禁じる」ではない**ので §16.5 に矛盾はしないが、
**翻訳版を別の識別子で承認させる道は閉じている**と読める。
**⚠ 我々は翻訳を提出していないし、する予定も無い。** ここに書くのは、**方針が新しく、
かつ「既に承認済みのものと同じ」を理由に却下した直近の例だから**である（§8.1 と同じ族）。

### 8.5 有利な事実 —— 分類は柔らかく、承認の側で使われている

2023〜2026 の動議は **"in the special purpose category" / "in the International category" /
"in the legacy category" / "as a regular license"** と、**category を付けて承認している。**
`review-rules.md` §1.102 の `keywords` は、この category がそのまま機械可読に出ているものである。
**カテゴリは否決の道具としてではなく、承認の粒度として使われている。**
**⚠ 逆側**: §8.1 が示すとおり、**同じ分類感覚が却下側にも働く**（*redundant* / *duplicative*）。

### 8.6 🔴🟢 **0BSD の決定記録を読んだ —— #84 が引いている当のライセンスである**

**`board_minutes` が指す 2015-10-14 の議事録は、0BSD（提出時の名は Free Public License 1.0.0・
提出 2015-08-30 / 承認 2015-10-14）の審議そのものである。** 逐語:

> **Free Public License** Similar to CC0, getting at quasi-public domain, where there is a license
> with no conditions **Cannot be argued to violate OSD, appears more permissive that MIT**, i.e.
> no copyright notice required nor required to include license text. Review has focused about
> issues from a policy perspective: requireing preservation of copyright licenses and text.
> **Without such, users would not know who copyright holder is.** One benefit is that it
> **re-uses existing lanuage from existing and understood licenses (basically the ISC License)**.
> **This might be a thought experiment–is it really going to be used?**
> **Essentially the same as the WTFPL license.** **Should we consider criteria for use when
> assessing licenses.**

> Motion (Ricard): **Approve Free Public License 1.0.0** Second (Simon). … **Vote: 8 Yes; 0 No; 0
> Abstain.** **NOTE: we will have a review done to assess potencial harm to open source community
> with such a format.**

**（原文ママ。綴りの誤りも含めて直していない。）**

**有利な点が 3 つある。**

1. **条件を課さないライセンスについて、理事会自身が
   *"Cannot be argued to violate OSD, appears more permissive that MIT"* と述べている。**
   **notice の保持を要求しないこと**まで名指ししたうえでの評価である ——
   `submission-reference.md` §3b が「実際に争われるのは OSD 7 だ」と書いた当の点に、
   **理事会側の言明が在る。**
2. **同じ席で *"Essentially the same as the WTFPL license"* と言われながら承認されている。**
   **2009 年に却下された WTFPL との違いは、条文が献呈ではなく*ライセンス*として書かれていることである**
   （§8.1）。**ACD の §3 / §4 の並存は、この 2 つの記録の差そのものに当たる。**
3. **「本当に使われるのか」は問われ、そして承認を止めていない**（B2）。
   *"This might be a thought experiment–is it really going to be used?"*

**不利な点も同じ席に在る。**

1. *"Without such, users would not know who copyright holder is."* ——**notice を要求しない設計の費用**を
   理事会が明示している。**ACD §10.2 はさらに踏み込んでいる**（`against.md` の OSD 7 の項）。
2. *"Should we consider criteria for use when assessing licenses."* ——**2015 年に蒔かれたこの問いが、
   2025-07-18 の *"should the LC reject a license proposal that is valid but is not in use anywhere?"*
   へ育っている**（§2）。**B2 は 10 年かけて重くなった。**
3. **NOTE が付いている** ——*"we will have a review done to assess potencial harm … with such a format"*。
   **承認は、この形式への留保つきで出ている。**

### 8.7 我々の 3 大ボトルネックは、2005 年に「3 つの追加テスト」として提案されたものである

**2005-09-12 の議題そのものが *"1. Three New Criteria"* で、中身は
*"a. Uniqueness b. Re-useable c. Readibility"*（原文ママ）。**

> Admit we didn't do a good job of building support for the 3 additional tests. Craft a plan to
> build acceptance now. **Question of whether they should be in the OSD…** … **Mr. Radcliffe says
> we can establish any criteria we want to. Mr. Coar is worried about appearing arbitrary.** …
> Mr. Ghosh wants to let License Proliferation take up the application of the "Three Qualities"
> **as separate from the application of the OSD**. … maybe **shouldn't be an administrative
> criteria but rather a recommendation** to be put into "how to submit to OSI"

**B10（gap = uniqueness）/ `submission-reference.md` §4b（提出者専用でない = re-usable）/
B13（理解コスト = readability）は、偶然 3 つなのではない。** 2005 年に**OSD とは別の追加テスト**
として提案され、**OSD に入れるかどうかが未決のまま**「推奨」に落とされた 3 つと同じである。

**有利**: **これらは OSD の条項ではない。** 2025-07-18 の理事会も
*"a license should be rejected only if it violates the OSD"* と述べている（§2）。
**不利**: *"we can establish any criteria we want to"* が同じ記録に在り、
**2025 年の「duplicative and not used なら not approved のまま留め置かれうる」がその実装**である。
**20 年かけて、追加テストは「却下の根拠」ではなく「承認しないまま置く根拠」として形を得た。**

### 8.8 「非増殖の成文規則は無い」は、2013 年に委員長が述べている

> Villa said that part of the reason CeCILL hasn't been approved in the past is that it feels like a
> violation of our proliferation report. However, **we have no written rules about
> non-proliferation** and it's otherwise a compliant license. … In the longer term, **put in
> concrete rules regarding proliferation**

**2013 年に「長期的に具体的な規則を入れる」とされ、2025-07-18 に理事会が
「まず License process ページで明確に伝えること」を求め（§2）、§3 が記録するとおり
14 か月後もそれは公表されていない。** **同じ項目が 13 年空いている。**
**⚠ これは怠慢の指摘ではなく、我々の予測に効く事実である** ——
**公表された基準を読み尽くしても、実際に使われる基準を読み尽くしたことにはならない**（§3 の再確認）。

### 8.9 「成功しそうか」は基準として使われてこなかった（2009-04-01）

> Bruce Perens doesn't think it will be successful, but **we've never used likelihood of achieving
> the author's goals as a criteria for license approval.**（SIL Open Font License 1.1・承認）

**B2 に対する、20 年の歴史側からの反証である。** **⚠ 逆側**: §8.6 が示すとおり
2015 年に *"Should we consider criteria for use when assessing licenses"* が提起され、
**2025 年には「使われていないなら not approved のまま」まで来ている。**
**「使われてこなかった」は「今も使われない」を意味しない。**

### 8.10 カテゴリは棚であって門ではない —— 同じ 1 回で 3 つの動議（2024-09-20）

| 動議 | 帰結 |
|---|---|
| Open Source Protection License | *"does not conform to the OSD and assure software freedom and the license is therefore **not approved**"* |
| MIT-CMU | *"be **approved** … in the **Redundant with More Popular** category"* |
| Los Alamos National Labs BSD-3 Variant | *"be **approved** … in the **Non-Reusable** category"* |

**同じ会議で、OSD 不適合は承認されず、重複と非再利用は承認されている。**
**門は OSD で、カテゴリは棚である**（§2 の *"rejected only if it violates the OSD"* と整合）。
**`review-rules.md` §1.102 の `keywords` は、この動議の言葉がそのまま機械可読になったものである。**
**⚠ 逆側**: **棚に置かれること自体は費用**で、`submission-reference.md` §4b が
「提出者専用ではない」を論証しているのは、**その棚を避けるためである。**

## 7. この文書が establish しないこと

- **公開分が不完全**なので、上の件数は「公開されている範囲で」に限られる。**母数は分からない。**
- **議事録は決定を記録するが、議論を記録しない。** 理由が書かれた否決は 4 件で、
  残りは動議の文だけである。**理由の分布をここから読んではいけない。**
- **§2 の「両立する読み」は我々の読みであって、OSI の説明ではない。**
  *"reject"* と *"not approved"* の区別は**まだ公表されていない**（§3）ので、
  **区別の内容を我々が確定させることはできない。**
