---
file: LICENSES/ACD-1.0.objection-map.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-09-09
canonical-ref: LICENSES/ACD-1.0.review-precedents.md (各反論の原文と読みはこちら) / LICENSES/ACD-1.0.against.md (不利な事実の本体) / LICENSES/REVIEWERS.md (入口)
---

# 既知の反論が ACD-1.0 に当たるか —— 1 表

**この文書は 1 節しか持たない。** `ACD-1.0.review-precedents.md` から 2026-09-09 に切り出した
（同 file が advisory を越えたため）。**節番号 §1.62 は変えていない**ので既存の参照は解決する。

**分けた理由は規模だけではない。** ここに在るのは**他の節の合成**であって precedent の記録では
なく、**審査者が最初に読むべきもの**である。900 行の末尾に置いておくのは、
`against.md` #6（長さ）に対して我々ができる数少ない実務的な対処を捨てることになる。

## 1.62 直近 24 か月にこのリストで出た反論を全部並べ、ACD-1.0 に当たるかを 1 表にする

**この節は「我々が正しい」を示すためのものではない。** 審査者が最初に知りたいのは
**どの既知の反論がこの提出に当たり、どれが当たらないか**であり、それを 1 箇所で読めるように
する。`REVIEWERS.md` の規約に従い **当たるものを先に置く**。

**出典は全て `license-review` / `license-discuss` の公開アーカイブで、日付と発言者を書く。**
**「当たらない」は我々の読みであって、審査者の判断ではない。**

### 当たるもの

| 反論（原文の要点） | 出所 | ACD-1.0 のどこに当たるか | 記録 |
|---|---|---|---|
| *"you'd likely need to have the help of a lawyer. **Waivers/disclaimers of IP rights are quite complex**"* | McCoy Smith・`license-discuss` 2026-08-07 | **法的レビューが無い。** 答えは「そのとおりで、我々にはそれが無い」以外に無い | #5 / #79 / §1.52 |
| *"**why you're doing another one?**"*（PD 等価は代替可能な唯一の類型で 0BSD が在る）| Rob Landley・同 2026-08-07 | **類型に 1 件足す理由。** 部分的な答えは §1.59（人格権）と不在の 3 主題 | #84 / §1.59 |
| *"**It is excessively wordy** and proscriptive… no one other than you will ever use this license"* | Pamela Chestek・同 2026-06-23 | **長さと採用。** 語数は GPLv3 本体より 43 語短い（§4c）が、**採用 1 件は動かない** | #6 / §1.60 |
| *"**Which is it, a dedication to the public domain or a license? You can't have it both ways.**"* | Pamela Chestek・同 2025-10-16 | **§3 + §4 + §4.4 の構造そのもの。** §11.3 は予期して書かれているが、答えは 4 条を要する | #110 / §1.61 |
| **人格権条項の追加を "mission creep" と名指し** | Pamela Chestek・同 2026-06-23 | **§12。** §1.59 が「incumbent に無い穴」と評価した当の条項 | #6 / §1.59 / §1.60 |
| *"**these are not licensable**, so anything the license says one way or the other, nothing changes"*（人格権） | Carlo Piana・`license-review` 2023-11 | **§12.1（放棄）に当たる。** §12.2（不行使の合意）は同じ反論では倒れない | #104 |
| *"**it is an issue as to whether a license of this scope would gain significant uptake at least from patent holders**"* | McCoy Smith・`license-review` 2025-05-14 | **§8.1 + §8.4 + 報復ゼロ。** OSD 違反ではないが **SPDX の実使用条件**に効く | #107 / §1.58 |
| *"three different things with one document"* | Pamela Chestek・`license-discuss` 2026-03-29 | **16 節の構成。** ただし ACD-1.0 の各節は同一 Work に作用する法的機構である | #105 |
| **「一つの instrument に一つの権利」** | Rob Landley | **§3〜§12 が複数の権利種を扱うこと。** #105 と逆を向いており、並べ替えでは両立しない | #102 |

### 当たらないもの（理由は条文で確かめた）

| 反論 | 出所 | なぜ当たらないか |
|---|---|---|
| *"OSI doesn't approve **partial licenses or add-ons to existing licenses**"* | McCoy Smith・`license-discuss` 2026-08-03 | ACD-1.0 は既存ライセンスへの追加条項ではなく**独立した完結した文書**である（`ACD-1.0.txt` 単体で 16 節 82 項）|
| 商用・非商用で扱いを変える条項 | Henrik Ingo・同 2026-08-05 ほか。**OSD 6 の由来は Bruce Perens 氏が同 2026-08-06 に自ら説明している**（Berkeley SPICE の南アフリカ警察条項）| **§4.3** —— 許諾は「あなたが誰か」「何に使うか」に条件づけられない |
| **商標まで放棄している** | subham mahesh・同 2026-08-07 | **§1.5** が商標を Covered Rights から除き、**§11.1** が商標の権利を与えないと明言する |
| **特許訴訟による自動終了**（OSD 5 / 過度に広い引き金）| Chestek・2025-10-16 / McCoy・2026-09-07 の Q3・Q4 | **§8.2** —— *"contains no patent retaliation provision, and its absence is deliberate"* |
| **違法な利用を許さない条項**（留保に当たる）| Chestek・2025-10-16 | 本文に存在しない（`unlawful` / `illegal` の出現 **0 件**・実測 2026-09-09）|
| **「撤回不能」と「自動終了」の同居** | Chestek・`license-review` 2026-01（PUWL）| **§10.4** は何も終了させない。§4.1 は irrevocable かつ perpetual |
| **既存ライセンスからの文言の借用** | Atkinson 氏 / McCoy 氏が別の提出で名指し | **8 語連鎖の共有 0**（MIT / MIT-0 / 0BSD / Apache-2.0 / CC0 / Unlicense の 6 本に対し・§4c に測定法と control）|
| **モデルには開くべき source code が無く Freedom 1 と 3 が成立しない** | John Colagioia・`license-review` 2026-08-29 | ACD-1.0 は**モデルのライセンスではない**。対象は Work であり、§9.2 は機械生成物について**表明しない**と明言する |
| **訓練データが無ければ open ではない**（*"or any other license with similar flaws"*）| Preston Maness・同 2026-09-08 | 同上。ACD-1.0 は「あるモデルが open である」と一度も主張しない |
| **出力への表示義務・透明性義務**（AI 時代の提出が OSD 3 / 7 / 10 で止まった論点）| AI-MIT / RAIL / FMLL の各スレッド | **§10.1** —— 条件を一切課さない。§B.0 が「反対方向の賭け」と述べているのはこの点 |

### この表の限界

1. **「当たらない」は我々の読みである。** 審査者が同じ語をどの条項へ向けるかは我々が決められない
   —— とくに **AI** の語は、上の 3 つの型を反射的に呼びうる（`rounds/` の Maness 氏 mirror doc）。
2. **反論は組み合わさる。** 「長い」＋「採用 1 件」＋「弁護士が読んでいない」は、
   個別には答えられても**束ねられると 1 つの推論になる** —— Chestek 氏が実際にそう束ねている。
   **そして束ね方は 1 通りではない**: Lukas Atkinson 氏は 2021-02-14 に
   *"submitted licenses should have either received **legal review** or at least
   **non-negligible use**. This license has **neither**"* として、
   **弁護士と採用を 1 文で結んで**承認しないよう Board に求めている（#113 / `reviewer-positions.md` §1.64）。
   **上の表は 1 行ずつ答えるが、束ねられた 1 文には答えていない。**
3. **網羅ではない。** 読んだ窓は `PEER-REVIEW-WATCH.md` §3.9 と全数調査の節に列挙してある。
