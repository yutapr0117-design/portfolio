---
file: LICENSES/ACD-1.0.review-corpus.md
audience: 次のセッションの実装者（一次読者）/ OSI license-review participants / 監査人
last-updated: 2026-09-13
canonical-ref: LICENSES/ACD-1.0.review-precedents.md (個別スレッドの読み・§1.45〜§1.66) / LICENSES/ACD-OSI-BOTTLENECKS.md (canonical なボトルネック一覧) / LICENSES/AS-OF.md (外部事実と検証日)
---

# `license-review` アーカイブ**全体**から測ったこと（§1.67 以降）

**この file は `ACD-1.0.review-precedents.md` から 2026-09-13 に切り出した。** 分けた理由は
行数ではなく**種類**である —— `review-precedents.md` は**個別スレッドを読んで得た指摘**（§1.45〜§1.66）、
本 file は**アーカイブ全体を取得して数えたこと**（基準・規則・結果・所要日数・手続きの実態）である。
**前者は読みで、後者は測定である**（`against.md` #131 ——**測定を読みに優先せよ**）。

**節番号は動かしていない。** §1.67 は §1.67 のまま、この file にある ——
**既存の参照をすべて有効に保つため**（`comparison.md` → `review-precedents.md` の分割と同じ規約）。
**新しい節をどちらに足すかの規則**: **個別スレッドの読み → `review-precedents.md`、
アーカイブ全体の測定 → 本 file。**

**取得物の共通仕様**: `license-review` **2024-01〜2026-09（33 か月）**、`license-discuss`
**2024-01〜2026-09（30 か月・3 か月は投稿ゼロ）**。ブラウザ相当の UA で月次 `.txt` を取得し、
**折り返しヘッダを先に展開してから**解析している（#99 の教訓）。

## 1.67 委員会が実際に述べた「承認しない／受け入れる」規則の全数（2024-01〜2026-09）と、ACD-1.0 の当たり方

**方法**: `license-review` の 2024-01〜2026-09（33 か月・804 通・111 スレッド）を取得し、
**引用行を除いた本文**から `OSI will/does not approve` / `OSI will accept` / `OSI requires` /
`cannot be approved` の形を全数抽出した。**名称検索ではなく形の全数列挙である**（#87 / #99 の
「名前で数えると母集団を数えたことにならない」を避けるため）。**得られたのは 5 件**で、
うち 4 件は Licensing Committee 委員長（Pamela Chestek 氏）の発言である。

| # | 述べられた規則（逐語） | 出典 | ACD-1.0 の位置 |
|---|---|---|---|
| R1 | *"OSI **requires prior review by a lawyer** because there are things that a layman very likely cannot consider, not just to enrich lawyers (who mostly do this job **pro bono**, as we are doing now)"* | Carlo Piana 氏・2024-12-18・PBZC スレッド。**"in his own capacity" と自ら明記している** | **⚠ 我々に不利で、しかも既存の記述と食い違う。** B1 は委員長の *"recommended … not a blocker"*（同じ 2024-12 の PBZC スレッド）と Berkus 理事の同趣旨（2025-05）に依っている —— **同一スレッドの中で、2 人の OSI 関係者が期待値を別の言葉で述べている。** 我々の disposition は変えない（委員長は委員会として述べ、Piana 氏は個人の資格と明記している）が、**この逐語を B1 の隣に置かずに「recommended だ」とだけ書くのは、有利な側だけを引くことである** |
| R2 | *"OSI will not approve licenses that are **not self-contained** because of the high likelihood that the added content will not comply with the OSD or OSAID"* | Chestek 氏・2025-02-14・MGB 1.0（annex を許す構造への指摘） | **通る。実測: ACD-1.0 本文に外部参照は 0 件**（`http` / `annex` / `available at` / `incorporated by reference` のいずれも 0）。**付属文書も、後から差し替わる余地もない** |
| R3 | *"The OSI **will not approve a license that attempts to describe which claims are licensed and which are not by what type of rights the user is exercising** - they must be allowed to exercise them all"* | Chestek 氏・2025-02-14・MGB 1.0。MGB は特許許諾を「再現・派生に必要な範囲」に限っており、**ソフトウェアを実行するだけの人に許諾が届かない**ため OSD 6 違反と判断された | **当たらない。** §8.1 の限定は**行使する権利の種類**ではなく **Work との関係**である —— *"every patent claim … that would be infringed by making, having made, **using**, offering to sell, selling, importing, or otherwise transferring the Work"*。**"using" が入っているので、実行するだけの受領者にも届く**（MGB が落ちた当の点） |
| R4 | *"The OSI **will accept** a patent grant that is limited to only the claims that are **necessarily infringed by the patentee's contribution** (alone or in combination with the preexisting software) and temporally limited to only what was granted at the time of the contribution"* | 同上（R3 の直後・**受け入れる形を名指しした唯一の発言**） | **この形に一致する。** §8.1 末尾は *"where the infringement is caused by subject matter contained in the Work as made available by the Dedicator"* ——**寄与によって必然的に侵害される請求項に限る**という同じ限定である。**ただし ACD は時点による限定を置いていない**（*"now or in future"*）—— これは受け入れ条件より**広い**方向の差であり、狭い方向の差ではない |
| R5 | *"OSI will not approve licenses where the **title refers to a particular person, entity or software** or that have them 'hard coded' into the license (see **'Standard for New Licenses' para. 1**)"* | Chestek 氏・2026-04-18・CNPL-1.0（名称に "CompanioNation" を含むことへの指摘） | **通る。** 名称に人・団体・ソフトウェアの名は無く、**本文の固有名詞は 0 件・置換テキストも 0 件**（`submission.md` §4b の実測）。**B6 が扱っているのは別の懸念**（"Commons" が CC/ODC の house mark と衝突しうること）で、**この規則そのものには当たらない** |

**同じ 2026-04-18 の CNPL への指摘には、規則の形をとっていないがもう 1 つ重要な点がある**:
*"The license does not grant all the rights under copyright, at least under US law. US law also
includes the right to **publicly perform and publicly display** … it is also **better practice not
to define the grant by enumerating specific rights**, since those may be country-specific."*
**ACD-1.0 はこの指摘の両方に対して逆側に立っている** —— §4.1 は列挙ではなく
*"all Covered Rights in the Work for any purpose whatsoever"* という**範囲による許諾**で、
§4.2 は *"includes, **without limitation**"* と明示したうえで
**"publicly display, publicly perform" を実際に含んでいる**。

**この節が意味すること（過大に読まないための注記）**: **R2 / R3 / R5 に「当たらない」ことは、
承認されることを意味しない。** これらは**失格の形**であって合格の条件ではなく、我々の 2 大弱点
（B1 法的レビュー・B2 実使用）はここでは 1 つも解消していない。**それでも記録する理由は 2 つ**
——**(a)** これまでドシエは「我々は OSD に適合すると考える」という**自分の推論**を積んでおり、
**委員会が実際に口にした規則に対して当てた記録が無かった**。**(b)** R1 は不利であり、
**探して見つかったのが有利な 4 件だけだったのではないことを、同じ表の中で示す必要がある。**

## 1.68 33 か月分の**結果**を数えた —— 承認 2 件・否決 6 件、そして承認された 2 件の輪郭

**方法**: §1.67 と同じ取得物（`license-review` 2024-01〜2026-09・804 通）から、
**理事会の決定を告知した本文**（*"the Board voted"* / *"declined to accept"* /
*"voted not to accept"* / *"the Board approved"*）を全数抽出した。**告知は委員長または理事が出す**。

| 結果 | ライセンス | 決定日 | 輪郭 |
|---|---|---|---|
| **否決** | Zeppelin Public License 1.0 | 2024-01-19 | 個人・新規 |
| **否決** | Adversary Public License 1.0 | 2024-12-20 | 個人・新規 |
| **否決** | Berkeley Artistic License V5 | 2025-01-17 | 個人・新規 |
| **否決** | Python Statistics Calculator License | 2025-01-17 | 個人・新規 |
| **否決** | Accountable Resolver License | 2025-01-17 | 個人・新規 |
| **否決** | AFN License | 2025-09-04 | 個人・新規 |
| **承認** | **OSC License version 1** | **2025-03-21** | **弁護士が依頼者（ドイツ・ゾーリンゲン市）の代理で提出。MIT に、ドイツ法で有効な責任制限を足しただけの差分** |
| **承認** | **BSD-3-Clause-Open-MPI** | **2025-07-18** | **機関（Open MPI）。BSD-3-Clause の変種** |

**告知されたのは 21 の提出型スレッドのうち 8 件だけである** —— 残りは撤回・停止・告知なしで、
**「否決 6・承認 2」は決定の全体ではなく、決定として公表された分の全体である。**

**承認された 2 件に共通するもの（数えたのではなく、読んで分かること）**:

1. **既に承認されているテキストからの小さな差分である。** OSC は MIT ＋ 責任制限 1 段落、
   Open MPI は BSD-3-Clause の変種。**どちらも「新しい種類の道具」ではない。**
2. **背後に機関がある。** 市、あるいは大学連合のプロジェクト。
3. **起草または提出に弁護士が関与している。** OSC の提出者は *"on behalf of my client"* と
   書いており、委員長との往復はドイツ法の解釈についての専門的な問答になっている。
4. **gap の述べ方が 1 点で、具体的である。** OSC の主張は
   *"the versatile MIT license does not contain a limitation of liability that is effective
   under German law"* ——**特定の法域で、既存の承認済みライセンスの特定の条項が効かない**、
   というそれだけである。**3 か月・約 14 通で決定に至っている。**

**⚠ この節の数（承認 2・否決 6）は、同じ日のうちに §1.69 で訂正された。** 検出器が理事会の告知文だけを見ており、**委員会の Rationale Document を読んでいなかった**。**正しくは承認 4・否決 8・「新規ではない」1 である。** 以下の読み（我々の輪郭が否決側に一致する）は**訂正後の数でも変わらない**（承認 4 件はいずれも既存テキストで、新規の道具は 1 件も無い）。

**ACD-1.0 の輪郭は、承認された側ではなく否決された側に一致する** ——
**新規・単独著者・非弁護士・採用 1 件**。**これは感想ではなく、上の表の読み方である**
（`against.md` #128）。**同時に、gap の論の形は OSC と同型でもある** ——
「既存の承認済みライセンスが、ある領域で効かない」。**違いは幅である**: OSC は 1 法域の 1 条項、
ACD は ML/TDM・特許・機械生成物の 3 つを述べている。**この差は本文ではなく提出文で縮められる**
（B13・入口の設計）—— **本文は凍結中で触れないが、gap を 1 文で言い切る形は提出文の側の仕事である。**

## 1.69 §1.68 の数を訂正する —— 委員会の Rationale Document を読んでいなかった

**§1.68 は同じ日のうちに誤りだと分かった。** 検出器が拾っていたのは**理事会の決定を告知する
文面**（*"the Board voted"* / *"declined to accept"*）だけで、**委員会が list に投稿する
Rationale Document**（*"Resolved that it is the opinion of the OSI that …"*）を見ていなかった。
**同じ corpus に、決議は 11 件あった。** これは #87 / #99 と同じ形である ——
**当て方を変えたら母集団が変わった。**

**訂正後の全体（2024-01〜2026-09・決議と告知を合わせた）**:

| 結果 | ライセンス | 分類・理由（逐語の要点） |
|---|---|---|
| **承認** | **MIT-CMU License**（2024-09） | **"Redundant with More Popular" category** ——*"a simple license that grants full rights … without any restrictions"* |
| **承認** | **Los Alamos National Labs BSD-3 Variant**（2024-09） | **"Non-Reusable" category** ——*"a legacy license, already in use for a number of projects"* |
| **承認** | **OSC License version 1**（2025-03） | **"International" category** —— MIT と同等で、**ドイツ法に合わせた免責**。弁護士が市の代理で提出 |
| **承認** | **BSD-3-Clause-Open-MPI**（2025-07） | 機関・BSD 変種（告知のみ・rationale は corpus に無い） |
| 否決 | Zeppelin Public License 1.0 | **起草が粗く解釈問題を生む**。"contribution" が未定義で OSD 9 に触れうる |
| 否決 | Setup Tooling License 1.3 | 決議のみ（理由は corpus の抜粋範囲外） |
| 否決 | Open Source Protection License | *"Adaptations should respect the original Work's integrity"* / *"align with the original Author's vision"* → **OSD 6**。*"No reviewer was in favor"* |
| 否決 | Adversary Public License 1.0 | **MIT ＋ 7 つの追加条件** —— 条件として読むと**適用不能**になり複数の OSD に触れる |
| 否決 | Berkeley Artistic License V5 | **全コメントが否定的**・解釈問題・**題名が誤認を招く**（Berkeley 由来でも Artistic 由来でもない） |
| 否決 | Python Statistics Calculator License | **OSD 5**（経験ある開発者しか改変できない）と **OSD 6**（教育目的を差別） |
| 否決 | Accountable Resolver License 1.0 | §4.6 の**利用制限**（プライバシー）→ **OSD 6**。加えて起草が粗い |
| 新規でない | W3C Software and Document license 2023 | *"is not a new license"* —— サイト表記の修正で処理 |

**否決の理由は 2 つの束に落ちる**: **(a) 条件・利用制限・差別**（OSPL / Adversary / PSCL /
Accountable Resolver）と **(b) 起草の粗さと解釈問題**（Zeppelin / Berkeley Artistic /
Accountable Resolver）。**題名の誤認**（Berkeley Artistic）が 1 件。

**ACD-1.0 の当たり方**: **(a) には構造上あたらない** —— §10.1 が条件を一切持たないので、
「条件として読むと適用不能」も「利用制限」も生じようがない。**(b) が我々の生きたリスクである**
—— 4,896 語・弁護士のレビュー無しで、**否決された「起草が粗い」3 件はいずれも我々より短い**。
**長さは明晰さと同じではないが、解釈問題は我々に最も起こりやすい失敗の形である。**
**題名は誤認を招かない**（由来を主張していない）。

**そして、この掘削でいちばん効く 1 件が出た。** **"Redundant with More Popular" は承認の
category である** —— MIT-CMU は *"redundant"* と名指しされたうえで **2024 年に承認されている**。
**つまり、既存と重複していることは承認の障害ではなく、棚の名前である。**
これは **#84（Rob Landley 氏「PD 等価は代替可能な唯一の類型で 0BSD がある。なぜもう一つ？」）に
対する、我々の推論ではない答え**である —— **リスト自身の運用が、重複を理由に落としていない。**
（**過大に読まない**: 重複が障害でないことと、承認されることは別である。MIT-CMU は
**既に広く使われている実テキスト**であり、我々は採用 1 件である。）

**同じ Rationale から、手続きについて 2 つ。** **(1)** Berkeley Artistic の理由には
*"the license submitter **agreed that a revision was advisable** … however, the license submitter
**only solicited others to revise the license and did not submit an amended version**"* とある ——
**「直すべきだと認めること」は、直したテキストを出すことの代わりにならない。** 指摘に同意したなら、
**改訂版はこちらが書いて出す**（`REVISION-PROTOCOL.md` §1 の ⑤⑥ に規則として足した）。
**(2)** 同じ決議の Exhibit A は、そのライセンスが *"Project:(project name here)"* のような
**空欄を持つ様式**だったことを示している —— **ACD-1.0 は固有名詞 0・置換テキスト 0**
（`submission.md` §4b）で、**採用に本文の編集を 1 箇所も要しない。** これは §4b が
「提出者専用ではない」ために書かれた測定だが、**同時に「様式ではない」ことの測定でもある。**

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
| 2 | *"The license does not have terms that **structurally put the licensor in a more favored position** than any licensee"* | **当たらない方向に作ってある。** 受領者に条件は一切なく（§10.1）、Dedicator の側に義務がある（§5 の不行使の約束・§12・§2.6 の特定義務）。**licensor にだけ有利な留保は §11 の商標のみ**で、これは承認済みライセンスに広くある |
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

**この測定が establish しないもの（訂正前と同じく、ここは変わらない）**:
**短い文は明晰であることを意味しない。** 文長は代理指標であって明晰さそのものではなく、
**非母語話者の起草に固有の誤り（冠詞・前置詞・時制の一致）はこの測定に一切現れない。**
**弁護士のレビューが無いという事実（B1）は、この測定では 1 ミリも動かない。**

## 1.71 `license-discuss` を先に通すのは、例外である —— 20 件中 15 件が直接 `license-review` へ出している

**なぜ測ったか。** 我々は `license-discuss` に出しており、そこが沈黙のままなら
**「議論を経ずに本申請へ出すのは異例ではないか」**という懸念が残る。**測れる問いなので測った。**

**方法**（2026-09-11）: `license-review` 2024-01〜2026-09（804 通）と
`license-discuss` 同期間（**443 通・30 か月分**）を取得し、`license-review` に現れた提出ごとに
**その最初の投稿より前に `license-discuss` に同名の件名があるか**を数えた。
**⚠ これは名称一致であり floor である**（#87 / #99）。

| 先に `license-discuss` に出ていたもの（5 件） | 先行通数 | 最初の言及からの間隔 | その後 |
|---|---|---|---|
| MIT-CMU | 2 | 2 日 | **承認** |
| MGB 1.0 | 3 | 約 2.5 か月 | 否決・再提出・撤回 |
| Misty Foundation | 2 | 1 日 | 撤回 |
| OpenMDW | 5 | 約 14 か月 | 審査中 |
| ModelGo | 7 | 2 日 | 審査中 |

**残る 15 件は、`license-discuss` に一度も現れずに `license-review` へ出ている**
（Zeppelin / Setup Tooling / OSPL / Berkeley Artistic / PSCL / Accountable Resolver / AFN /
Los Alamos / ESA-PL / Milenium / BOS / PSF-2.0 / CompanioNation / NIST / UPD）。

**読み（過大にも過小にもしない）**:

- **直接 `license-review` へ出すのが普通の形である。** 我々が discuss を先に通したことは
  **必須の手順を踏んだのでも、異例なことをしたのでもない。**
- **先に議論したかどうかは結果を予測しない** —— 上の 5 件は承認 1・撤回 2・審査中 2 に割れる。
- **したがって「discuss が沈黙だから本申請へ出せない」は、この記録からは支持されない。**
  **同時に「discuss を通したから有利」も支持されない。** 提出文にはそのまま書く（§B.0 の沈黙版）。

**この測定の限界を、結果と同じ場所に書く**: **名称一致は floor であり、実例で外している。**
**2025-03 に承認された OSC License v1 は、この測定に現れない** —— スレッドの件名が
*"Request for a new license review"* で、**ライセンス名が件名に一度も出てこない**からである。
**同じ理由で、名前を件名に出さずに議論された提出は数えられていない。**

**副産物**: `license-discuss` には **2024-12 / 2025-01 / 2025-08 の 3 か月、1 通も投稿が無い**
（アーカイブの索引に月次ファイルそのものが存在しない）。**33 か月のうち 3 か月は完全な沈黙である**
——**沈黙を「我々に対する反応」と読んではならない**という #109 の基準率に、月単位の形を 1 つ足す。

## 1.72 提出から理事会の決定まで、実測でどれくらいか —— 中央値およそ 3 か月

**なぜ測るか。** 経路 B を採るなら「出してから、いつ答えが出るか」が計画の前提になる。
**これまで我々が持っていたのは 2 つの言明だけだった** —— 委員長 McCoy Smith 氏の
*"We work on a **two-month review cycle**"*（2026-08-28）と、process ページの
*"Decision date: due no later than the first Board meeting after \<提出 + 60 日\>"*。
**どちらも規則であって実績ではない。**

**方法**（2026-09-11）: `license-review` 2024-01〜2026-09 の 804 通を**件名で正規化してスレッドに束ね**、
**各スレッドの最初の日付**と、**そのスレッド内で理事会の決定を告知した本文の日付**の差を取った。
**名称一致は使っていない**（§1.71 で floor だと分かったため）。委員会の理由書が
**提出日を明記している場合**は、そちらを提出日として採った。

| 日数 | ライセンス |
|---|---|
| 59 | BSD-3-Clause-Open-MPI |
| 83 | Python Statistics Calculator |
| 92 | Zeppelin Public License（理由書の提出日 2023-10-19 → 2024-01-19）|
| 93 | Accountable Resolver |
| 93 | Setup Tooling 1.3（理由書の提出日 2024-05-15 → 理事会 2024-08-16）|
| 109 | Berkeley Artistic V5 |
| 109 | OSC License version 1 |
| 120 | W3C 2023（理由書の提出日 2024-04-18 → 理事会 2024-08-16）|
| 133 | AFN License |
| 139 | Adversary Public License 1.0 |

**中央値 101 日・範囲 59〜139 日 —— およそ 2 か月から 4 か月半、中央値でほぼ 3 か月。**

**規則と実績の関係**: 60 日は**下限を作る規則**であって所要時間ではない。
**実測の最短が 59 日**であることは、**規則どおり「60 日後の最初の理事会」で決まった場合が
実際に存在する**ことを示す。**中央値がその 1.7 倍であることは、多くの場合そこまでに決まらない
ことを示す。** どちらも同じ記録から読める。

**この測定が establish しないもの**: **決定が告知されなかった提出は入っていない**
（§1.69 のとおり 21 の提出型スレッドのうち告知は 8 件）。**撤回・停止・沈黙で終わったものは
「時間がかかった」ではなく「決まらなかった」であり、この中央値には現れない。**
**したがってこれは「決まった場合の所要時間」であって「出せば 3 か月で決まる」ではない。**

## 1.73 Licensing Committee 委員長が、我々を名指しで謝辞した（2026-09-10）—— そして、それが何を示さないか

**逐語**（`rounds/2026-09-10-license-review-chestek-names-us.txt`・OpenMDW-1.1 の審査スレッド）:

> *"I would like to thank **Yuta-san** for their **insightful view on the termination provision**,
> which I find helpful."* —— Pamela Chestek（**Licensing Committee 委員長**・2026-09-10 18:07）

**これで `license-review` 上で我々の投稿に反応した人は 6 人になった**（2026-09-13 に全数で確認）:
Michael Dolan 氏（LF・OpenMDW steward・名指しで回答）/ Moming Duan 氏（ModelGo steward・条文に即した
回答 + 2026-09-08 に参照リストへ採録）/ Shuji Sado 氏（我々の質問を引いて議論を進めた）/
Ruby Anna 氏（*"Hi Yuta … You have interpreted …"*）/ **Pamela Chestek 氏（委員長）**。

**示すこと（狭く書く）**:

- **委員長は我々の寄与を読み、有用だと述べ、承認リスト上で名指しした。**
- **それは moderator 通知（2026-09-09）の翌日である。** ——**通知の後も、委員長による実質的な
  やり取りは続いている。**

**示さないこと（同じ精度で書く）**:

- **ACD-1.0 について何も言っていない。** 発言は**他者の提出**（OpenMDW-1.1）の審査中のもので、
  **我々の提出への応答ではない。ACD-1.0 への返信は依然としてゼロである**（2026-09-13 時点・
  `license-discuss` 2026-09 は 9 通のままで、我々の 2 通に返信は無い）。
- **我々が moderator 通知の名宛人だったかを決めない。** 翌日に委員長が謝辞したことは、
  **「通知は我々のことではなかった」とも「我々は問題視されていない」とも読めない。**
  通知は moderators が出し、謝辞は委員長が出した ——**別の人が、別のことについて述べている。**
- **B1（法的レビュー無し）と B2（採用 1 件）を 1 ミリも動かさない。**

**議論の中身も記録しておく（ACD の設計に直接あたる）。** このスレッドの争点は
**「著作権の主張を引き金にした許諾の終了」が open source と両立するか**である。委員長は
*"I do find it inconsistent with my understanding of open source … that someone who intentionally
committed a wrongful act should be allowed to avoid the consequences"* と述べ、
Josh Berkus 理事は逆に *"accidental infringing copying happens all the time"* と述べ、
Richard Fontana 氏は *"OpenMDW-1.1 is different in this respect because its copyright-triggered
termination reaches **all** sorts of copyright claims"* と述べている。
**ACD-1.0 はこの争点の外にある** ——**終了条項を持たず（§10.4）、報復条項も持たない（§8.2）。**
**ただしこれは「だから承認される」ではない**: 争点の外にあることは失格を 1 つ免れることであって、
**承認の理由にはならない**（§1.70 の天井 —— 必要条件は十分条件にならない）。

## 1.74 **モデルの出力に条件を課すことは OSD 9 違反である**と委員長が述べている —— ACD は条件ではなく放棄で扱っている

**ドシエはこの論点を一度も扱っていなかった**（2026-09-13 に `grep` で確認 ——
`OSD 9` と `output` を同時に含む行が LICENSES/ 全体で 0 件だった）。**逐語は 2 件ある。**

> *"I do not believe that **putting conditions on output of a model is workable** and, where the
> output is **not a derivative work** under copyright law, **it violates OSD9, 'License Must Not
> Restrict Other Software.'**"* —— **Pamela Chestek 氏（Licensing Committee 委員長）**・2025-12-05・
> MG-BY-2.0 / MG-BY-SA 宛。同じメールで、派生物の定義を「モデルと**機能的に似た振る舞いを achieve する**
> ために」と狭めた改訂について *"does not address this problem and, in fact, **exacerbates** it"*
> と述べている ——**狭めても、著作権法上の派生物でない出力に届く限り同じ問題である。**

> *"there is an argument that that obligation **arguably violates OSD 9** — even though
> **OSD 9 talks about 'other software' not 'other output' or 'other content'**"* ——
> **McCoy Smith 氏**・2025-05-14・出力への attribution 義務について。

**ACD-1.0 の位置（有利な側）**: **出力に条件を 1 つも課していない。** §6.4 は
*"No model, parameter set, weight, embedding, or output derived from Computational Use of the Work
is encumbered … and **You owe nothing** in respect of any of them. **Nothing in this Dedication
requires You to license, disclose, or attribute any such thing.**"* ——**委員長が「workable でない」
と述べた設計（出力に条件）の、ちょうど反対側である。** §9.2 / §9.3 も同じ向きで、
**受領者は「どの部分が機械生成か」を判定する必要がない。**

**これで、リストの生きた争点 3 つすべてについて、ACD が外側にいることが確かめられた** ——
**終了条項**（§1.73・§10.4 が持たない）/ **条件・利用制限**（§1.69 の否決理由 (a)・§10.1 が持たない）/
**出力への条件**（本節・§6.4 が持たない）。**共通の理由は 1 つで、ACD は何も足していないからである。**

**不利な側（同じ精度で書く）**: **McCoy 氏の一文は、OSD が我々の領域を想定して書かれていないことを
committee 側が認めている記録でもある** ——*"OSD 9 talks about 'other software' not 'other output'"*。
**これは gap の主張を支える一方で、我々を承認する OSD 上の足場も無いことを意味する。**
**そして §1.70 の天井が効く** ——*"consensus that a license does not ensure software freedom may …
be the justification for rejecting a license **even where they cannot identify a specific aspect of
the OSD** … that is not met"*。**争点の外にいることは、失格を 3 つ免れることであって、承認の理由ではない。**

**副次的に確かめたこと**: 委員長は 2026-05-04 に、**OSD 9 と「新規ライセンスの基準 1（再利用可能性）」を
同じ段落で併用している**（Milenium License が、そのライセンスを使う**他人のプロジェクト**に
起草者の著作権表示を要求していた件）。**#129 で我々が literal に読んで不安に思った基準 1 が、
実際に適用された唯一の例はこれである** ——**適用対象は「本文に起草者固有のものが埋め込まれている」
ケースであって、法域による効果の差ではなかった。** §1.70 row 1 の読みを、実例が 1 つ支持する。

## 1.75 我々と同じ類型の提出が止まっている理由は、テキストではなく**手続き**だった（3 件を通しで読んだ）

**個人が単独で出した直近 3 件を、スレッドの最初から最後まで読んだ。** 共通しているのは、
**審査者が本文の評価に入る前に、required information の欠落で止めている**ことである。

| 提出 | 経過 | 審査者が実際に言ったこと |
|---|---|---|
| **Misty Foundation License**（2025-12・**5 日で撤回**）| 6.3 → 1.7 を 2 日で差し替え | Chestek 氏: *"You should **read this page** … and submit the license **with the additional information** as outlined on that webpage"* / Piana 氏: *"**a brief introduction to oneself and a signature of a real person** … would probably be a modicum of courtesy"* |
| **Milenium License**（2026-05・**5 日**）| 1.0 → 1.1 を 2 日で差し替え | Kevin Fleming 氏: *"There are **a number of details which you will need to provide in addition to the license text itself**"* / McCoy 氏: *"this submission **has not followed the process of answering the questions**"* |
| **BOS Public License**（2026-07-22 〜 2026-09-07・**6 週間以上・3 版**）| 1.0 → 1.2（2 日）→ 1.3（6 週後）| Berkus 氏: *"Please **attach a copy of the text** … Also, **your links are broken**"* / Chestek 氏: *"Please provide **all the information as required** … and **in particular do not skip 'Describe any legal review the license has been through, including whether it was drafted by a lawyer.'**"* / Chestek 氏（v1.2 に対して）: *"Please provide **the rest of the information**"* / Piana 氏（v1.3 に対して・6 週間後）: *"the submission **does not include the required information** and therefore **I will not comment it until the deficiencies are remedied**"* |

**読み取れること（3 点・いずれも我々の側で使える）**:

1. **版を差し替えても進まない。** 3 件とも数日で改訂版を出したが、**審査者の要求は変わらなかった**
   ——欠けていたのは条文ではなく提出物だったからである。**「まず出して、指摘されたら直す」は、
   この類型では機能していない。** オーナーの方針（**自信を持って出せる版ができるまで出さない**）は、
   この記録と整合する。
2. **審査者は required information が揃うまで本文を読まない、と明言する。** Piana 氏の
   *"I will not comment it until the deficiencies are remedied"* が最も明確である。
   **つまり手続きの不備は、悪い評価ではなく評価そのものの不在を招く。**
3. **委員長が名指しした唯一の項目が「法的レビューの有無」だった。** ——**我々の最大の弱点
   （B1）を述べる項目である。** 我々の §B.0 は *"**Legal review: none.** No lawyer has drafted or
   read it."* と書いており、**Check 463 がその文言の存在を BLOCKING で強制している**
   （2026-09-13 に実測: この行を "Legal review status." に変えると RED）。
   **弱点を述べる項目ほど、書き落とす方向の圧力が構造的にある**ので、機械で縛る意味がある。

**この節が establish しないこと（逆は言えない）**: **「required information が揃っていれば
engagement が得られる」とは言えない。** 上の 3 件が示すのは **「欠けていると読まれない」**という
一方向だけである。**我々自身が反例になりうる** —— `license-discuss` への 2 通は必要な材料を
添えて出したが、**返信はゼロである**（2026-09-13 時点）。
**ただし `license-discuss` は提出の窓口ではないので、同じ要求が働く場ではない**（#83 / §1.71）。

**併せて記録する不利な材料**: Piana 氏は BOS v1.3 を *"the **10,354th** submitted MIT derivative"*
と呼び、Misty に対しては *"**Why another MIT-style license, the hundredth or so?**"* と書いている。
**proliferation への疲れは、条文とは独立に、提出そのものへの心証として存在する** ——
#84 / B6 と同じ族で、**我々の答え（この類型に 1 件足す費用が低い）は、この心証には届かない。**

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

## 1.77 ModelGo Zero の審査から —— 我々の §6 に**直撃する**委員長の見解と、名称規約についての有利な先例

**ModelGo は 2025-02 から 2026-09 まで 19 か月・124 通・3 度の再提出を経て、まだ決定されていない。**
**我々に最も近い候補（Zero ＝ 最も条件の少ない版）**に絞って、steward 以外の 20 通を読んだ。

### (a) 🔴 委員長は「出力に言及すること自体が曖昧さを作る」と述べている —— これは §6 への直撃である

> *"But does the fact that **you mention it in the first place lead to a negative implication** that
> you haven't granted the necessary rights to create Output? With software it's been a fairly bright
> line that any output isn't subject matter of the license unless it's a derivative work. Here,
> though, **you have created ambiguity about the legal status of the output by mentioning it** and
> also made the license much more complicated. **In my view it's not worth including Output at all in
> the license.** … **although I wouldn't reject the license for that reason.**"*
> —— Pamela Chestek 氏・2025-12-15

**ACD-1.0 は出力に明示的に言及している**（§6.4 —— モデル・パラメータ・重み・埋め込み・出力は
encumbered でなく、受領者は何も負わない）。**つまり委員長が「やらない方がよい」と述べた設計を、
我々は意図的に採っている。**

**我々の答えは本文の中にある。** §6.5:
*"Section 6 states expressly what Sections 3 to 5 would in any event permit. It is stated expressly
because **silence on this subject has proved ambiguous in practice**, and because **a permission that
an automated system cannot determine is … no permission at all**."*
**前提が正面から逆である** —— 委員長は「言及が曖昧さを作る」と言い、§6.5 は「沈黙が曖昧さを作る」と言う。

**この対立について、正直に言えること 3 つ**:

1. **委員長自身が「それを理由に却下はしない」と明記している**（*"I wouldn't reject the license for
   that reason"*）。**したがってこれは失格事由ではなく、設計の良し悪しについての見解である。**
2. **対象が違う可能性がある。** 委員長が問題にしたのは **MG-BY の責任制限の中の出力への言及**で、
   *"The only liability you might be avoiding is from the person creating the output"* と続いている
   ——**義務や責任の側の言及**である。**§6.4 は義務を課さず、むしろ取り除く方向の言及である。**
   **ただしこれは我々の読みであって、委員長がそう区別する保証はない。**
3. **negative implication の議論は我々にも当たりうる。** 出力について「encumbered でない」と
   書けば、**書いていない何かについては encumbered なのかという読みを招く**。
   **ACD にはこれを塞ぐ一般条項がある**（§10.1 が条件を一切持たず、§4.1 が *"all Covered Rights …
   for any purpose whatsoever"* を与える）が、**§6.4 の列挙は依然として列挙である。**

**やらないこと**: **本文は凍結中なので直さない。** そして **1.1 でも直さない方に傾く** ——
§6 を削れば **gap の主張の 3 分の 1 が消える**（基準 7 は gap を要件としている・§1.70）。
**これは「どちらかが正しい」ではなく、我々が意図的に取っているトレードオフである**ことを
提出文で先に述べるのが正しい扱いだと考える（`ACD-1.1-CHANGELIST.md` へ候補として記録）。

### (b) 🟢 「Zero」「-0」という名称は、本文と一致しているかを審査される —— そして我々は一致している

> *"**'Zero' or '-0' with open source licensing typically means something akin to public domain or at
> least a license that imposes no (i.e., 'zero') obligations** on the recipient of the license.
> The latest draft of this license **does impose at least one obligation**: in Section 2.2(a)(i) the
> licensee is obligated to pass along a copy of the license with any distribution."*
> —— McCoy Smith 氏・2025-05-14。**Chestek 氏は翌メールで *"I agree with this."* と述べている。**

**これは名称についての審査が実際に行われた記録である。** ACD-1.0 の名称に含まれる
**"Dedication"** は「公有への献呈」を意味する語で、**本文がそれに一致しているかが問われうる。**
**一致している** —— §3 が献呈であり、**§10.1 が条件を 1 つも持たない**（ModelGo Zero が
*"at least one obligation"* で指摘された当の点を、ACD は持たない）。
**`submission.md` §4b の「本文の固有名詞 0・置換テキスト 0・採用に編集不要」は、
この照合に耐えることの一部の証拠になる。**

### (c) 審査が長引いた理由を、委員がその場で述べている

> *"this is **in part as a result of how your initial submission has progressed through the process**
> … those licenses have **undergone quite a bit of commentary and quite a bit of revision by you**
> since then … **We work on a two-month review cycle**, which normally would have put your licenses
> up for Board review in August"* —— McCoy Smith 氏・2026-08-27

**§1.75 の (1)（版を差し替えても進まない）と同じ結論に、committee 側の言葉で到達している** ——
**改訂そのものが時計を戻す。** `REVISION-PROTOCOL.md` §2 の凍結規律は、礼儀であると同時に
**決定までの時間を最短にする手段**でもある（既に §2 に書いてあるが、**根拠がこれで一次資料になった**）。

## 1.78 OpenMDW-1.1 の審査（117 通・1 か月）の中心論点と、ACD が当たるか当たらないか

**2026-08-13 から 2026-09-12 までの 117 通を読み、steward 以外の発言から論点を抽出した。**
**参加者は 12 人**で、内訳は Richard Fontana 氏 22 / Pamela Chestek 氏（委員長）19 /
McCoy Smith 氏 11 / Shuji Sado 氏 9 / Luis Villa 氏 8 / Rob Landley 氏 7 ほか。
**現時点で最も活発な審査であり、ACD と同じ「AI 時代の新規ライセンス」である。**

**中心論点は 2 つに収束している。**

### (a) **束ねること**（"Model Materials" 構成）—— OSD 9 の疑い

> *"across the whole set of conceptually distinct things, such that **a claim against one item
> triggers termination of rights in another item**, is possibly an **OSD 9 violation**"*
> —— Fontana 氏・2026-08-13。以後 1 か月にわたり *"I may come back to my OSD 9 concern"*
> *"this is what I mean when I say there may be an OSD 9 problem"* と繰り返している。
> **Sado 氏は反対の立場**（*"I am still not convinced that treating the Model Materials as a single
> unit is, by itself, an OSD 9 problem"*）で、**決着していない。**

**ACD の位置**: **当たらない。** OSD 9 が禁じるのは「一緒に頒布される**他の**ソフトウェアへの制限」で、
**ACD は制限を 1 つも置かない**（§10.1）。**束ねの問題が OSD 9 に化けるのは「1 つへの主張が
別のものの権利を終了させる」経路があるからで、ACD には終了そのものが無い**（§10.4）。
**ACD の "Work" も複数の種類の素材を 1 語で束ねている**（§1.2 —— source code / object code /
documentation / data / metadata / audiovisual material）**が、束ねた結果として起こることが
「全部が同じく無条件に使える」ことだけなので、束ねが不利益を伝播させない。**

### (b) **範囲の判定可能性** —— *"How do you know what the 'covered work' is?"*（Fontana 氏・2026-08-16）

**これは我々に当たる論点である。** 審査者が問うているのは「許諾が寛容か」ではなく
**「第三者が、何が対象かを判定できるか」**である。

**ACD の答えは 3 条に分かれている**: **§1.2** が Work を「Dedicator が本文を適用した素材」と
**適用行為**で定義し、**§2.7** が「Dedicator が持つ権利にしか及ばない」と述べ、
**§2.6** が **「他人の権利が混ざっている部分は、Work に付随する形で特定する」**という
**Dedicator 側の義務**を置いている。
**そして §6.5 が、なぜそれが重要かを本文の中で述べている** ——
*"a permission that an automated system cannot determine is … no permission at all"*。

**⚠ 初版は「ACD の答えは practice に乗っている」と書いたが、それは §16 を読む前に書いたもので、
同日に訂正した。** **§16.1 は SPDX タグを含む notice の形を与え、§16.2 は「識別子だけで十分な
notice である —— 本文の写しが付いていなくても」と述べている** ——**本文は範囲を示す機械可読な
標識を供給しており、沈黙してはいない。**

**変わらない部分が、実際の限界である** ——**本文は標識を供給するが、file ごとの付与を要求はしない。**
標識の無い tree は本文だけからは判定できず、**それは MIT をはじめ承認済みの寛容ライセンスが
すべて共有する性質である。**
**ACD は「何が Work か」を本文では決めず、適用行為に委ねている。**
**「この file には適用され、あの file には適用されていない」を判定する責任は、
実質的に Dedicator の運用（§2.6 の特定）に乗っている。**
**リポジトリ側でそれを機械可読にしているのが我々の実装**（`LICENSE` / SPDX タグ / `machine.json` /
`.well-known` の宣言）だが、**それはこのリポジトリの性質であって、本文が保証するものではない。**
**この非対称は `against.md` #134 に立てた。**

### この節が establish しないこと

**OpenMDW の論点が ACD に当たらないことは、ACD が承認されることを意味しない。**
**また、OpenMDW がどう決まるかもまだ分からない** —— 2026-09-12 時点で審査は継続中で、
**委員長は条件付きで賛成しうると述べ**（*"if my concerns about the paragraph enumerating the
licensee's obligations to clear rights are addressed"*）、**Fontana 氏の OSD 9 の疑いは
解消していない。** **同時代 instrument の経過観察として、決定が出たら読み直す**
（`PEER-REVIEW-WATCH.md` の 4 分岐）。
