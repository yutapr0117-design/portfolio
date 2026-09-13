---
file: LICENSES/ACD-1.0.board-decisions.md
audience: 次のセッションの実装者（一次読者）/ OSI license-review participants / 監査人
last-updated: 2026-09-13
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
the minutes here, check the wiki"* と述べ、**最古が 2025-06-20**（ページ作成は 2007 年）、
**最新が 2026-06-29**。**「議事録に無い」は「決定が無かった」を意味しない。**
以下の件数はすべて**公開されている 12 回の範囲での**件数である。

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
except for the names of the departments"* だった。**提出パケット §4b（本文の固有名詞 0・置換テキスト 0・
採用に本文編集が 1 箇所も要らない）は、我々が思いついた論点ではなく、
委員会が現に手を動かしている論点である。**

## 7. この文書が establish しないこと

- **公開分が不完全**なので、上の件数は「公開されている範囲で」に限られる。**母数は分からない。**
- **議事録は決定を記録するが、議論を記録しない。** 理由が書かれた否決は 4 件で、
  残りは動議の文だけである。**理由の分布をここから読んではいけない。**
- **§2 の「両立する読み」は我々の読みであって、OSI の説明ではない。**
  *"reject"* と *"not approved"* の区別は**まだ公表されていない**（§3）ので、
  **区別の内容を我々が確定させることはできない。**
