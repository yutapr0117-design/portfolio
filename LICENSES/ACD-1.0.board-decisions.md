---
file: LICENSES/ACD-1.0.board-decisions.md
audience: 次のセッションの実装者（一次読者）/ OSI license-review participants / 監査人
last-updated: 2026-11-09
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

**2026-11-06 追記**: 2026-10-17 の取得物に在る 286 回の議事録（2005〜2026）を語で掃引した（*patent / public domain / dedication / proliferation / new license / vanity* と、許容型・免責・AI の語）。ドシエに無かった記録は §6 の (3)(4) の 2 件だった。**読み切ったのではなく語の掃引であり、語を持たない判断は拾えない。**

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
**両方が我々に当たる。** **（2026-11-07: 「not used」の読みは §2c で訂正した。）**

**この 3 文は、同時に 1 つの天井を弱める** ——§1.67 は
*"consensus … even where they cannot identify a specific aspect of the OSD … that is not met"* を
引いて「OSD 違反を指摘できなくても却下しうる」と記録した。**理事会は「OSD に違反する場合にのみ
*reject* する」と述べている。** **矛盾ではない** ——両立する読みは、
**「reject は OSD 違反に限るが、承認しないことは OSD 違反を要しない」**である。
**その読みが正しければ、我々にとって天井は下がっていない。名前が変わっただけである。**

**⚠ 2026-09-28 追記 —— この天井は 2003 年からある。** #243 の census が残していた
Open Source Software Alliance License（2003-09・119 通）を、通数ではなく決める側の発言で絞って
読んだところ、**同じ問題がリスト上で 23 年前に述べられていた**:

> *"Some people think licenses that are ideologically anti-GPL *ought* to be not open source,
> but **nobody can point to a specific OSD that is violated**. This is not necessarily conclusive:
> **if the OSI Board thinks a particular license is not open source but doesn't fit under anything
> in the OSD, it can change the OSD.**"* —— John Cowan 氏・2003-09-29

**確立するのは 1 点だけ** —— **「OSD の条文を指せないが承認したくない」という状況は、
最近の運用上の工夫ではなく、リストが最初期から抱えていた問題である。**
**§1.67 の引用（review-process ページ）と §2 の議事録は、その古い問題の現在の言い方である。**

**⚠ 確立しないこと 2 つ。** **(1) 後半（理事会は OSD を変えられる）は Cowan 氏の見解であって
OSI の声明ではない** ——氏は理事ではなく、リストの参加者である。**我々はこの主張をオフラインで
検証できない**ので、**「そう述べられた」までしか書かない。** **(2) OSSAL 固有の争点（反 GPL 的で
あること）は ACD に当たらない** ——ACD は §10.1 により条件を持たず、互換性の争いを生まない。
**転用できるのは天井の古さだけである。**

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

### 2c. 委員会はこの留め置きを実際に使い、解く条件を 1 文で述べている（2025-09-11・2026-11-07 に読んだ）

理事会の答えの 55 日後に、License Committee は Tiwaz License v1.0 についてこう決めた（Josh Berkus 氏が
*OSI Board Member* として報告・`rounds/2025-09-11-license-review-tiwaz-committee-deferral-observed.txt`）:

> *"The License Committee has voted to \*defer\* any recommendation of the Tiwaz license, because it is
> a close variant of an existing license, and there have been no demonstrated uses or planned uses of
> the license. Should one or more projects begin using this license or express an interest in doing
> so, please share that information here and we will remove the hold and submit our recommendation to
> the Board."*

`license-review` の全期間で、委員会の決定を告げた文を探した範囲では、保留はこの 1 件である。
我々は 2026-09-08 に Tiwaz を「読了」と記録したが、読んだ窓は 7 月までで、この 1 通は窓の外だった（#285）。

**分かること 3 つ。**

1. **理由は *and* で結ばれた 2 項で、理事会の 2 項と同じ形である。** 委員会は理事会の答えを引いていないので、
   その適用だとは書かれていない。
2. **解く条件は *or* で、採用より軽い。** 1 つ以上のプロジェクトが使い始めるか、関心を示せば足りる。
   §2 が「後者は AI には解けない」と書いたのは今も正しいが、必要なものは採用の実績より小さかった。
3. **計画段階の利用も数えられている。** *"demonstrated uses **or planned uses**"* と述べている。

**同じ年の承認が、これと対になる。** どちらも既存ライセンスの近い変種である。

| | Tiwaz v1.0 | OSC License v1 |
|---|---|---|
| 親 | MPL-2.0 | MIT |
| 提出時の利用 | 無く、計画も示されていない | *"there are currently no projects using the license. However, it is planned that the license will be used in mid/late January."*（`rounds/2024-12-23-license-review-osc-planned-use-observed.txt`）|
| 誰の利用か | —— | 提出者の依頼者（ゾーリンゲン市）自身の案件 |
| 結果 | 保留（2025-09-11） | 承認（2025-03-21） |

**ACD に当てると、2 項とも Tiwaz と同じ位置には無い。** 第 1 項について、ACD は既存ライセンスの派生ではない
（6 本と 8 語の連なりを共有しない）。第 2 項について、ACD は 1 つのプロジェクトに適用されている ——
このリポジトリである。したがって、この文書と入口が書いていた「使われていないは ACD に当たる」は、
出典より不利に書いていた。出典の語は *"not used by a project"* と *"no demonstrated uses or planned uses"* で、
第三者の利用に限っていない。OSC の利用も提出者の側のものだった。

**逆側を同じ重さで書く。**

- **提出者自身の利用が足りるとは、誰も述べていない。** Carlo Piana 氏は、個人の著者が「自分の著作物のために書いた」と
  述べた Linkumori について *"not having an active project with an urgency to adopt a license or to have it approved,
  I would suggest deferring license review"* と書いた（2026-06-19・`rounds/2026-06-19-license-review-piana-linkumori-observed.txt`）。
  同じ 1 通は、同じ提出者の *"Plenty of OSI-approved licenses started exactly there"* に対して
  *"\"this happened in the past\" is not a valid argument for the same to happen in the future"* と答えている。
  OSC の側には市と弁護士が居たが、ACD の側に在るのは個人のリポジトリ 1 つである。
- **保留に期限は無い。** 2026-11-07 に取得したアーカイブ（2026-10 まで）に、Tiwaz の後続は無い。
- **解けたあとに約束されているのは勧告であって承認ではない。** *"submit our recommendation"* の向きは書かれていない。
- **第 1 項の答えは「duplicative」の広さに依存する。** 委員会がこれを *close variant* より広く読めば、#84 が残る。
  答えは gap の 1 点である（`gap-measurements.md`）。
- **n は 1 ずつで、規則ではない。** 宛先は Tiwaz の 1 件で、process ページには無い（§3）。
  近い変種に向けた文を、新規のテキストへそのまま移せるとも限らない。

**打てる手。** 実在のプロジェクトが関心を示すことは、AI には作れないが、オーナーは尋ねることができる。
リポジトリの側では `ADOPTING.md` に、使う人が公に述べられる場所を案内した。捏造は失格事由である。

### 2d. 使われていないことは、単独では理由にされてこなかった（2026-11-07 に読んだ委員会の理由書）

委員会が理事会へ出す勧告には Rationale Document が付く。使用について述べた 2 通が在り、どちらも承認の勧告である。
MIT-0 は我々と同じ PD 等価の類型で、理事会は 2020-08-14 にこの勧告どおり承認した。

> *"There was some discussion whether the license was actually in use, but this is not a basis for rejection
> that the OSI has applied in the past (and the OSI has historically approved newly drafted licenses not yet
> in use)."* —— License Committee, Rationale Document, MIT-0（Chestek 委員長・2020-08-04・`rounds/2020-08-04-license-review-mit0-committee-rationale-observed.txt`）

> *"There was some discussion about whether a license in such limited use should have the attention of the OSI,
> but it has been submitted for approval and, to date, OSI has not used the number of projects adopting a license
> as a factor in deciding whether a license can be approved."* —— 同・Jam（2021-09-12・`rounds/2021-09-12-license-review-jam-committee-rationale-observed.txt`）

**組み合わせると、記録はこう並ぶ。** 2020 と 2021 の理由書は「使用は拒否の根拠でも要素でもない」と述べ、
2025 の理事会は「拒否は OSD 違反に限る」と述べ、使用を持ち出すのは *duplicative* と結んだときだけである。
**使われていないことが単独で否決の理由になった記録は、我々の読んだ範囲に無い。** Atkinson 氏の 2021-02 の文
（法的レビューも使用も無い）は参加者の見解で、その 7 か月後の委員会の理由書は別のことを述べている。

**使用の短さが効いた先は区分だった。** Mulan PSL の理由書（2020）は *"The license has not been in existence long enough to be
considered for the 'Popular and Widely Used or With Strong Communities' category"* と述べ、承認したうえで International へ置いている。

**逆側を同じ重さで書く。**

- **どちらも過去についての文である。** *"in the past"* と *"to date"* と述べており、今後を約束していない。
- **後の記録は向きが変わっている。** 同じ Chestek 氏が 2026-08-26 に、委員としてこう述べている ——
  *"We want to see licenses early to correct them, but are less inclined to approve a license that doesn't have a
  track record."* 理事会の留め置き（2025）と Tiwaz の保留（§2c）も 2021 より後である。
- **同じ年に、決める側の 2 人の記憶は割れている。** Josh Berkus 氏（`license-discuss` 2020-08-26）: *"I don't know that we've passed a license that didn't have at
  least one substantial project behind it in the last 10 years."* 同じ日の Fontana 氏の返信が逆である: *"several of the licenses approved by OSI in the past 10 years were not, at
  the time of approval, in use by any substantial project ... and I believe several may not have been used by any projects at all."* 氏はそれを *"thought experiment licenses"* の傾向と呼び、
  少なくなったとも述べている。ACD の 1 件が *"substantial"* かは誰も述べていない。
- **実績の無さへの反対は実際に述べられている。** Bradley Kuhn 氏（2020-01-01・CAL の審査）: *"I can't find an example when OSI approved a novel
  copyleft license that hadn't yet been used in practice and therefore had no track record of use for any FOSS project."*
  同じ 1 通は *"OSI also made a decision to cease considering such single-use licenses"* とも述べる（氏の見解で、我々は決定の原文を確かめていない）。
  CAL は 2 か月後に承認され、理由書の批判の一覧にこの点は無い。
- **理由書の 2 通は承認の側で、既存テキストの legacy 承認である。** MIT-0 は MIT から 1 文を除いたもの、Jam は 20 年使われたもので、
  新規の長いテキストについての文ではない。ただし MIT-0 の括弧書き（*"newly drafted licenses not yet in use"*）は新規について述べている。
- **理由書は OSI を拘束しない。** *"prior approval … does not bind"* は我々に有利な先例にも同じように当たる。

### 2e. 委員会は審査対象の基準を述べている（CERN-OHL・2021・2026-11-07 に読んだ）

B15 は「主題で不承認になった例が在る」から始まるが、同じ委員会が審査対象の基準を理由書に書いていた。

> *"There was discussion about whether the licenses, primarily intended for hardware, were appropriate for review by
> the OSI. The intention of the license drafters was to create a single license that could be used for designs that
> includes both hardware and software. Although software is not the primary use case for the license, and the licenses
> include some unusual terminology that make the licenses more difficult to interpret, they are written such that they
> can be used for software, so they are appropriate for the OSI's review."*
> —— License Committee, Rationale Document, CERN-OHL（Chestek 委員長・2021-01-09・`rounds/2021-01-09-license-review-cern-ohl-committee-rationale-observed.txt`）

**基準は「ソフトウェアに使えるように書かれているか」である。** ソフトウェアが主な用途でなくてよい、と述べている。
CERN-OHL の 3 本は承認済みの 141 本に在る。

**ACD はこの基準に本文で答える。** §1.2 は source code と object code から始まり、PREAMBLE の第 1 文は *"Software and the works
that surround it"* で、適用先はソフトウェアのリポジトリである。**Mulan の不承認（2023）とも矛盾しない** ——
Mulan の定義にはソフトウェアが 1 語も無く、Chestek 氏の *"tied to software"*（2023-08-10）と同じ線である。

**同じ理由書は、用語が解釈を難しくしていても審査対象性を変えなかった**（*"more difficult to interpret"*）。
これは審査対象性についての文で、承認の基準についての文ではない。

**逆側を同じ重さで書く。**

- **ACD の列挙は CERN より広い。** CERN の意図は *"designs that includes both hardware and software"* で、§1.2 は
  *"audiovisual material"* まで名指す。Fontana 氏は OpenMDW について、1 本ですべてを覆う設計を *"flawed in its basic conception"* と述べた（2026-09-11）。
  同じ氏は OFL を *"wrongly approved"* と述べており、承認の側の先例も軽くなりうる（register B15）。
- **2021 の文で、2023 の不承認より前である。** 基準が今も同じだとは誰も述べていない。
- **審査対象であることと承認されることは別である。** CERN は CERN が提出し、機関の steward が居た。
- **理由書は OSI を拘束しない。**

**B1 についても同じ通読で 1 点測った。** 不承認側の理由書 12 本（Vaccine / YOS / Ritchey / YATeam / Mulan / Zeppelin / Setup Tooling / OSPL / ADVPL /
Berkeley Artistic / PSCL / Accountable Resolver）に、lawyer / attorney / counsel / legal review の語は 1 度も出ない。
Zeppelin の提出者は法律家を付けられなかったと述べたが、理由書が挙げたのは *"poorly drafted"* だった。
**害として名指されるのは起草で、法律家の不在ではない。** 語の検索なので床であり、B1 が起草の質に効くこと自体は変わらない。

### 2f. OSI のサイトの記事は、放棄と許諾の 2 部構成を「解決策」と述べている（2017・2026-11-07 に読んだ）

OSI の公式サイトの記事 *Public Domain Is Not Open Source*（2017-07-28・署名 OSI Policy Team・区分 Press Releases・
`rounds/2026-11-07-osi-blog-public-domain-is-not-open-source-snapshot.txt`）は、公有化の問題を述べたあとで続ける。

> *"A solution would be to create a form of words to be used by the author to dedicate something to the public domain.
> It could simply disclaim ownership for the jurisdictions where that is possible, and then grant a copyright license that
> has the same practical effect as a public domain dedication for jurisdictions where ownership of copyright can never be
> disclaimed. Such a formulation has been published by the Creative Commons. They call it "CC0" and it is widely used and
> well respected. There's an issue though; it has not received OSI approval. Many reviewers believe it should, but its
> authors withdrew it from the approval process during a complex discussion about patent rights and it remains unapproved."*

**ACD はこの 2 部を持つ。** §3 が放棄し、§4 が許諾する。差も書く —— 記事の許諾は放棄できない法域のためのもので、§4 は法域を問わず独立に働く（§4.4 *"not as a fallback"*）。記事が挙げた障害は特許の 1 点で、ACD は §8 で特許を許諾する。
FAQ（2025）の 2 点と同じ結論へ、別の文書から届く。Chestek 氏の *"You can't have it both ways"*（2025-10-16）に対しても、
両方を置く形が OSI のサイトに書かれていたことになる。同じ形を勧めた Piana 氏の *"use both"*（2024-12-18）とも揃う。

**逆側を同じ重さで書く。**

- **決定でも規則でもない。** 本文は一人称で *"That's not a legal opinion (I'm not a lawyer so only entitled to layman's opinions)"* と述べ、
  末尾は初出が Meshed Insights だと述べる。理事会も委員会もこの文を採っていない。9 年前の文である。
- **同じ記事の結びは MIT を勧める。** *"In the mean time, it's probably safer to use a license like MIT instead."*
- **FAQ のほうが新しい。** *"rather than try to waive copyright altogether"*（2025）は §3 に当たる。
- **記事が名指す実物の CC0 は、今も承認されていない。** 「再開された」と記事が述べたあとも承認は無い。
- **ACD は CC0 でも記事の形そのものでもない。** 言えるのは 2 部を持つことまでで、§4.4 は独立の許諾である。記事が ACD を評価したわけではない。

### 2g. OSI の事務局長と委員長は、AI 向けの文書の審査をどう述べたか（2024-09・2026-11-07 に読んだ）

Mulan の不承認（2023-09）の 1 年後、OSI の事務局長が `license-review` へ問いを出した（スレッド *Adapting the license-review process to AI*・23 通）。
ドシエはこのスレッドを持っていなかった。

> *"It is likely that OSI will be receiving requests to approve new licenses, agreements, and terms of use/distribution for open
> source AI works. These documents may apply, not just to copyrighted software, but to non-software artifacts like datasets,
> documentation, and model parameters (aka weights)."* —— Stefano Maffulli 氏（Executive Director・2024-09-01）

委員長の答えは 3 点である。

> *"The reason to use the word "terms" instead of "license" is because the documents may assure the necessary rights through the
> use of legal mechanisms other than a license."* —— Pamela Chestek 氏（Chair・2024-09-10 00:09）

> *"it is going to take some creativity to create a document or documents that ensure the necessary freedoms are granted. I don't
> know anyone who has figured it out yet, although a lot of people are thinking about it. We don't even all agree on what rights
> mechanisms might apply to models in particular, and data to a lesser degree. Copyleft was a brilliant insight; there may be an
> equally brilliant insight that figures out how to manage this much more difficult area. This area needs room to develop, which
> may not happen if the OSI dictates what it believes the correct approach is, including whether that is a single license for all
> components or separate licenses for different components."* —— 同（2024-09-10 08:51）

> *"We consider patent rights specifically, and we have recently discussed moral rights. I believe there is sufficient expertise on
> the committee to evaluate non-copyright provisions."* —— 同（2024-09-09）

**ACD の論点へ当てると 4 つ動く。**

- **B15**: 審査の対象は、データセット・文書・パラメータに及ぶ文書を含むと事務局長が述べた。§2e の CERN-OHL より新しく、Mulan の不承認より後の文である。
- **B4**: 権利を保証する手段はライセンスに限らないと委員長が述べた。§3 と §4 の 2 部構成に当たる。
- **1 本で全部を覆う設計**: Fontana 氏の *"flawed in its basic conception"*（2026）の前に、委員長は 1 本か複数かを OSI が決めないと述べていた。
- **B8 / B9**: 非著作権の条項を委員会は評価できると委員長が述べた。§7 と §12 は審査の外ではない。

**逆側を同じ重さで書く。**

- **文脈は OSAID の *"OSI-approved terms"* である。** ACD は license として出す。委員長は同じ日に *"as I see it, and I may be completely wrong"* とも書いている。
- **2024 年の見解で、規則ではない。** process ページは変わっておらず、OpenMDW と ModelGo の決定は取得時点で公表されていない。
- **Fontana 氏の批判は後の文で、委員の 1 人のものとして今も立っている。** 委員長の文は「OSI が決めない」であって「1 本でよい」ではない。
- **同じスレッドの Berkus 氏は、審査はこれまで著作権の枠内だったと述べ**、学ぶ必要があると書いた。Maffulli 氏は *"limp along, mess up and be ready to iterate quickly"* と述べている。審査の費用は高い。
- **佐渡氏は同じスレッドで、データのライセンスには人格権・パブリシティ権・プライバシー権を行使させない確保が要ると述べた。** ACD §11.4 はパブリシティとプライバシーを許諾しない。§12 が答えるのは人格権までである。

### 2h. 2019 年の通知 —— 承認の文は動いている。いまの文は合意の手続きである（2026-11-07 に読んだ）

**理事会は 2019-05-24 に両リストへ通知を出した**（署名は委員長の Chestek 氏。Phipps 氏 *"authored collectively by the Board and is our shared view"*）。スレッド *"Evolving the License Review process for OSI"* は両リスト合わせて 126 通で、ドシエは一度も読んでいなかった。原文は `rounds/2019-05-license-lists-review-process-cited-observed-*`。

**(1) 承認の文は 2 度動いている。**

| 時点 | 文 |
|---|---|
| 2019-05 より前 | *"Approve, if (a) there is sufficient consensus emerging from community discussion that approval is justified, and (b) the OSI determines that the license conforms to the Open Source Definition and guarantees software freedom."* |
| 2019-05-24 | *"Approve if, after taking into consideration community discussion, the OSI determines that the license conforms to the Open Source Definition and guarantees software freedom."* |
| いまの process ページ | *"license approval is a consensus process"*。委員会は *"whether there is consensus on approving or rejecting the license"* を見る |

**2019 年の文を現行として引かないこと。** Fontana 氏の *"OSI has a responsibility to determine whether a license meets the OSD and provides software freedom regardless of what direction the l-r discussion is going in."*（2019-05-22）も当時の個人の見解である。いまの文は合意を求めるので、議論が起きないと決定へ進まない。B14 が手続きの不便で済まない理由はここにある。

**(2) 裁量の文には由来がある。** Phipps 氏 2019-06-01: *"We added the statement you so vigorously oppose when it became apparent that there were submitters who wanted to game the OSD"*、*"to explain the discretion OSI always has, and always will, choose to exercise when novel devices are unveiled."* Chestek 氏は同じ日、OSD は *"can be gamed to do exactly the opposite of what the goals and purposes of open source software are"* と述べた。`against.md` #130 の天井はここから来ている。向けられた先は、OSD の字句を満たしながら自由を狭める提出で、ACD は何も狭めない。**⚠ 逆側: 裁量の範囲は限定されていない。ACD は *"novel devices"* にあたり、自由を狭めないことは裁量の外に出る理由にならない。**

**(3) 同じ人が理由を書くと述べた。** Chestek 氏 2019-06-01: *"I am strongly opposed to any "because we say so" standard of license approval."*、*"I expect to be providing a rationale document about the OSI's decisions on license approval."* 2019 年以降の理由書（§2d・§2e）の出発点である。個人の資格の発言で、規則ではない。

**(4) 決定に至る提出は多くない。** Fontana 氏 2019-05-26: *"Of the licenses formally and informally submitted for approval, most never make it to a board decision."*、*"the licenses that tend to make it to a board decision are relatively uninteresting (from a commercial/community perspective) and non-controversial"*。BSD+Patent が通った理由も *"takes noncontroversial, widely used language"* と述べる。**⚠ ACD の本文は広く使われた文を借りていない。** 借用しないことは他所で有利に数えたが、ここでは逆に働く。

**(5) 通知のうち、いまのページに無い文がある。** 通知は *"discussion of substantive issues off-list is not recommended"* と述べ、提出者が off-list の問いに答えるときは *"encouraged to copy the license-review list also on their response after redacting the identity of the person sending the communication"* と勧めた。公開の場での開発も勧めている（*"We recommend that you carry out your license development process on a publicly viewable venue (preferably one where collaboration is also possible) and regularly seek views on license-discuss."*）。ACD の開発はこの形である。いまのページに残るのは *"we also encourage license submitters to ask for advice on the license-discuss list before formally submitting a license"* までで、どちらの文も現行の規則としては引けない。ただし委員会が見るのはリストなので、off-list で答えた内容は、提出の本文で述べ直さないと委員会の記録に入らない。

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

## 6. 有利な事実（同じ規律で書く）

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

**(3) CC0 が止まった理由は、議事録が述べている（2026-11-06 に足した）。** 2012-03-07 の License Committee の報告は *"Recommend disapprove, due to clause 4a"* と述べ、Chris DiBona 氏の *"I don't think that any new licenses should be approved unless they include patent clauses"* を載せる（`rounds/2012-03-07-osi-board-minutes-cc0-outcome-observed.txt`）。§8 はこの理由に直接当たる。**⚠ 逆側**: 同じ報告は学術の利用者について *"the patent exception is important to them"* と述べる。特許の除外を望む利用者が居たという記録である。

**(4) 増殖の害は「行き止まり」で測られたことがある（2026-11-06 に足した）。** 2007-11-07 の議事録は、再ライセンスを許す SimPL について *"it does not create a licensing dead-end and thus does not exacerbate the negative aspects of licensing proliferation"* と述べ、それを承認の理由にしている（`rounds/2007-11-07-osi-board-minutes-simpl-dead-end-observed.txt`）。§4.5 は Work をどの条件でも出せるので、#84 の費用の側への答えになる。**⚠ 逆側**: 19 年前の 1 件で、SimPL の再ライセンス先は GPL に限られていた。2013-05-01 の議事録は *"we have no written rules about non-proliferation"* と述べていて、その後 2025 に理事会が重複の扱いを述べた（§2）。

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
`review-rules.md` §1.82 が記録した Project Tick GPL の *"ambiguities in drafting make it
impossible to determine whether or not it complies with the OSD"* と**同じ構造**で、
**こちらは 2017 年、あちらは近年**。**橋は 1 本ではなく 2 本架かっている。**
**⚠ 逆側**: NOSA は**条件と義務を持つ長い契約**で、ACD は §10.1 により条件を持たない。
**長さの由来が違う**（あちらは義務、こちらは説明）。**だが「読んで確かめられるか」は同じ問いである。**

### 8.3 第 3・第 4 の帰結が、20 年にわたって使われている

| 年 | 文言 | 帰結 |
|---|---|---|
| 2005-03 に Nelson 氏が引いた議事録（会議の年は不明）| *"we decided that even though it was open source, the differences were not significant enough to approve it outright. We resolved to send it back and ask him to use the BSD license. If he refuses, we'll re-consider approving it."*（Wonka Public License）| OSD に適合しても承認せず、BSD を勧めて戻した（#302）|
| 2007-06-06 | *"we **decline to approve at this time** and suggest that the committee in future consider compatibility for licenses that advertise simplification"*（Simple Public License）| 承認でも却下でもない |
| 2008-05 | *"return the UOML License to the submitter for justification due to similarity to the SISSL"* | 類似を理由に差し戻した |
| 2009-03-04 | *"Discussion continues, but Bruce says **'Deny approval' because the benefits aren't worth the cost**"*（TGPPL）| **費用対効果**で語られている |
| 2017 秋 | *"can **neither approve nor reject**"*（NOSA 2.0）| 上記 |
| 2025-07-18 | *"could stay in a status where it is **not approved** if it is duplicative and not used by a project"* | §2 |
| 2025-09-11 | *"voted to \*defer\* any recommendation"*（Tiwaz・委員会）| §2c |

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
   **⚠ 2026-11-07: そのレビューは行われている。** Richard Fontana 氏が 2015-11-12 にリストへ報告した ——
   *"In response to several comments from the license-review community concerning the FPL, the OSI obtained outside
   legal counsel concerning the legal and policy issues raised by 'ultra-permissive' licenses like the FPL which do not
   impose conditions on the licensee (particularly notice-preservation conditions)."*
   （`rounds/2015-11-12-license-review-fpl-outside-counsel-observed.txt`）。**OSI は ACD §10.1 と同じ型の問いに、外部の法律家の助言を取っている。**
   助言の中身は公開されておらず、有利だったかどうかも分からない。確かめられるのは、0BSD が承認のまま一覧に在ることだけである。
   FPL は短い許諾で、献呈も特許も持たないので、助言が ACD の条項に及ぶとは言えない。

**2026-11-07 追記 —— 投票の前日の委員会報告を読んだ。理事会は「使用の要素」を採らずに承認している。**
Richard Fontana 氏の報告（2015-10-13・`rounds/2015-10-13-license-review-fontana-committee-report-fpl-observed.txt`）:

> *"The license is clearly OSD-conformant. I do not find the policy objections to the Free Public License persuasive"*
> *"To me, the only reasonable basis of objection is that the license may be too 'immature' for OSI approval."*
> *"OSI has approved thought-experiment licenses before (e.g. the SimPL) as well as licenses that were not used prior to OSI approval (e.g. the UPL)."*
> *"Recommendation: Approval, or else OSI to adopt some formal maturity/real-world-use factor for approval considerations such that approval of this license would be deferred"*

提出者は個人で法律家ではなく、ライセンスはまだ使われていなかった。報告はそれを述べたうえで 2 択を示し、理事会は翌日 8 対 0 で承認した。
**これが ACD に最も近い先例である** —— 個人、非弁護士、未使用、条件なし。重複の問いにも答えがある。Berkus 氏の *"does the FPL offer anything which can not already be accomplished"* に、
Fontana 氏は *"there doesn't seem to be any proliferation concern with FPL. I think there's no other OSI-approved license like it."* と答えた（`rounds/2015-10-13-license-review-fontana-reply-berkus-fpl-observed.txt`）。

**逆側。** (1) FPL は ISC から 1 条件を除いた短い本文で、ACD は新しい長い本文である。(2) 同じ報告は SimPL について *"I am not sure the present-day OSI would be as happy to approve it"* と述べている。
(3) 2015 年に採らなかった使用の要素は、2025 年に留め置きの形で入った（§2・§2c）。(4) 重複の答えは 2015 年の FPL には使えたが、0BSD が在る今の ACD に使えるのは特許の 1 点である。
(5) Berkus 氏が同じ 1 通で挙げた懸念は §16.2 に当たる（#287）。

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
として提案され、**OSD に入れるかどうかが未決のまま**残った 3 つと同じである。同じ議事録には推奨へ落とす案が在るが、同じ日の Eric S. Raymond 氏の報告は *"They are passed policy decisions of the OSI and are to be applied to all licenses submitted after they were passed in March 2005."* と述べている（2026-11-07 訂正。旧文は「「推奨」に落とされた」で、案を結果のように書いていた。読みやすさの水準は `against.md` #304）。

**有利**: **これらは OSD の条項ではない。** 2025-07-18 の理事会も
*"a license should be rejected only if it violates the OSD"* と述べている（§2）。
**不利**: *"we can establish any criteria we want to"* が同じ記録に在り、
**2025 年の「duplicative and not used なら not approved のまま留め置かれうる」がその実装**である。
**20 年かけて、追加テストは「却下の根拠」ではなく「承認しないまま置く根拠」として形を得た。****2026-11-09 精密化**: リストの側の記録（`review-readings.md` §1.168）では、2005-09-12 の理事会は、重複と読みにくさを指摘された 2 本（ACE License・OVPL）を却下せずに保留した。「承認しないまま置く」は 20 年かけて得た形ではなく、基準を最初に当てた日から在った形である。同じ日に Open-Realty License は却下されたが、形式上の理由はどちらの版を承認するかが不明なことだった。

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
