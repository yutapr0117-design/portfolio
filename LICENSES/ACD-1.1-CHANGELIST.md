---
file: LICENSES/ACD-1.1-CHANGELIST.md
audience: ai, 監査人, OSI license-review / license-discuss participants, 第三者全般
last-updated: 2026-09-06
canonical-ref: LICENSES/ACD-1.0.errata.md (欠陥の一次記録) / LICENSES/REVISION-PROTOCOL.md (§1 ラウンドの流れ・§2 版管理) / LICENSES/FROZEN.md (1.0 が動かないことの機械強制)
---

# ACD-1.1 変更リスト —— 議論中に貯まっていくものの、単一の集約点

## What

**次版に反映する候補を、1 か所に集める。** 1.0 は凍結中で、欠陥を見つけても直さず記録する運用に
なっている（`FROZEN.md` / Check 453）。**その記録の行き先が 4 か所以上に散っていた**ので、
ここへ集約する。

**この文書は適用しない。** ここに載ることは「1.1 でこうする」という記録であって、1.0 の本文は
1 バイトも動かない。

## Why

**凍結は「1.0 を通すために動かせない」ではなく「読まれている版が動かない」である。**
議論の目的は意見を集めることで、**集めたものを反映した版を出す**のが次の段。オーナーの運用方針
（2026-09-04）はそのループを明示している ——「届いた議論をそのまま全部取り込む → 本申請 →
レビュー → 全部取り込んだ改善版を申請 → …… を承認されるまで繰り返す」。

**そして反映対象は、届いた意見だけではない。** 議論の最中にこちら側で見つけたもの（errata・
不利な事実の掃引で出た条文上の不備・機械可読形の不整合）も同じ入力である。**議論が終わってから
4 か所を回って集めるのでは落ちる**ので、**貯まる先を先に 1 つにしておく。**

## How

- **errata は一次記録、ここは索引。** 内容を複製しない —— 複製は必ず drift する（本ドシエが
  2026-09-06 だけで 6 件見つけた class）。`E<n>` を引き、状態だけをここで持つ。
- **Check 464 (BLOCKING)** が `errata.md` の全 `E<n>` がこの表に現れることを強制する。
  **落とすことを機械的に不可能にするのが、この文書の唯一の実効部分**である。
- 届いた指摘は `rounds/` に無改変で保存し、分解と分類は `discussion-log.md`。そこで
  **帰結が `1.1 候補` になったものを、ここへ移す。**
- **1.0 の本文・`spdx.xml`・`machine.json` は編集しない。** Check 453 が sha256 で止める。

## 0. 実物はどこにあるか（2026-09-10 新設）

**`LICENSES/ACD-1.1-DRAFT.txt`** —— **NOT IN FORCE / NOT SUBMITTED / NOT APPLIED** と
自分で述べる草案。**オーナーが 2026-09-10 に「現行ライセンスはそのまま保持する必要があるが、
次版を作成して改善し続けるのは問題ない」と述べた**ので、設計だけで止めていたものを実物にした
（`REVISION-PROTOCOL.md` §2 が最初から定めていた「1.0 は永久凍結・次版は併置」の形）。

**第 1 段（machinery のみ）で入った変更**: §2.2 が §15.5 を吸収 / §2.5 圧縮 / §2.9 は事実を残し
結論を落とす（E5）/ §15.2・§15.3・§15.5・§15.6 を削除して繰り上げ / §16.4 が翻訳の但し書きを吸収し
**識別子の保護を族へ拡張**（E14）。**4,896 語 82 条 → 4,594 語 77 条。**

**第 2 段で扱う（まだ入れていない）**: E11（外部回答待ちなので触らない）/ E13（定義の並び）/
E15（§8.4 の程度の限定）/ E16（§2.6 の opt-out の可視性）。

**規律**: **記録の無い変更を草案へ入れない。** 本ファイルが集約点である。

## 1. errata 由来（`ACD-1.0.errata.md` が一次記録）

| Errata | 対象 | 1.1 での扱い（要約は errata 側が権威） | 状態 |
|---|---|---|---|
| E1 | §16.1 | 推奨 notice の SPDX 識別子表記 | 反映予定 |
| E2 | §16.3 | 「誰でも・どの著作物にも」の広すぎる言い回し | 反映予定 |
| E3 | §16.1 notice（+ `machine.json` の `notice`）| 「no conditions are imposed」に §10.1 の限定「in respect of the Work」が無い —— 通知文だけを読むと §16 の本文条件まで否定して読める | 反映予定 |
| E4 | §6.4 | 「No model … is encumbered」が、**権利が存在しない**と述べているようにも読める。意図は「行使可能な請求が生じない」であって存否の主張ではない | 反映予定 |
| E5 | §2.9 | 「and so is not executory」は法廷地の倒産法が決める分類を本文が断定している。支える事実（継続債務の不在）は先に述べているので、断定を落とす | 反映予定 |
| E6 | §8.4 | §8.1 の「Work に含まれる主題に起因する侵害に限る」proviso を意図的に落としている。意図は正しいが、**落としたことが読み取れない** | 反映予定 |
| E7 | §11.1 と §16 の読み順 | §11.1 が「名称に権利を与えない」と述べた直後に §16.2 が名称へ法的効果を持たせる。整合は §10.5 / §16.6 にあるが**読み順が逆**で、読者は矛盾に見える箇所を先に読む | 反映予定 |
| E8 | §16.4 | SPDX 登録が要求する XML と「identifier 下での改変形」の関係 | 反映予定 |
| E9 | §10.4 | 第 2 文だけが未限定（定義語 "You" の射程） | 反映予定 |
| E10 | `machine.json` | `reservationsAndLimits` が唯一の制限を記述していない | 反映予定 |
| E11 | §4.4 | 「§3 が有効な場合も relied upon され得る」の記述が正確か。**architectural か drafting か**を `license-discuss` で問い中 | **外部の回答待ち**（唯一、社内で見つけたのではなくリスト上で提起した項目）|
| E12 | §16.1 notice | 「No rights are reserved」に限定が無い（§11.1 は商標を渡さない）。**E3 と同じ 1 文の前半** | 反映予定 |
| E13 | §1 の並び順 | 定義が 3 回、後で定義される語を使う。並べ替えで 2 件は消せる（相互定義の 1 件は消せない）| 反映予定 |
| E14 | §16.4 | **識別子の保護がこの版だけ** ——`ACD-1.1` / `ACD-2.0` を第三者が使っても条文に当たらない。**我々自身が 1.1 を予定しているので実務的な空きである**（B6 / B11 と接続）| 反映予定（版番号のパターン化か、SPDX 登録へ委ねるか）|
| E15 | §8.4 | **「その使用から生じた」に程度の限定が無い** ——極少量の混入で広い特許許諾を主張しうる読みを条文が誘う。**閾値を入れれば gap が縮む**（B7 = B10 との一方向の取引）| **設計判断が要る**（記録のみ）|
| E16 | §2.6 / §16.2 | **痕跡を残さない opt-out と「terms apply in full」の衝突**。**§6.5 が定める基準（自動化システムが判定できない許諾は許諾ではない）に、自分の 1 条が届いていない**| 反映予定（記録要件を付けるか、DCO へ委ねるか）|

## 2. 他文書に散っていた候補（ここが集約点になる）

| 出所 | 候補 | 状態 |
|---|---|---|
| `review-responses-meta.md` | 「新版の公開は旧版で与えた許諾に影響しない」旨の明文化 | 検討中 |
| `against.md` #101（外部レビューの実例由来）| **§16 の「文書についての制限であって著作物についてではない」を、読者がぶつかる場所に置く。** McCoy Smith 氏は MIT-I 審査（2025-08-14）で「may not **modify** … this version of the Software」を OSD 3 違反と述べた。§16.4 の対象は文書だが、**その旨は §10.5 / §16.6 にあり、読者は先に §16.4 に着く**（errata E7 が同じ読み順問題を記録している）| 検討中 |
| `against.md` #100（外部レビューの実例由来）| **§12 に「結果は法域で変わらない」を明示する。** McCoy Smith 氏は PBZC 審査（2024-12-18）で「PD 法域では公有・それ以外ではコピーレフト」という構造を *likely violates OSD 5* と述べた。ACD-1.0 で法域により変わるのは §12 の**機構**だけで、§4.4 / §10.1 / §10.4 により**受領者が得るものは同一**である。だが**その一文が §12 の側に無い**ので、審査者は §12 だけを読んで結論しうる | 検討中 |
| `review-responses-clauses.md` | 条項レベルの想定問答で「1.1 候補として残す」とした論点 | 検討中 |

## 2.5 縮小候補（B3・gap を 1 語も削らずに ≈529 語）

**`ACD-OSI-BOTTLENECKS.md` B3 の測定に基づく。** 本体 4,574 語のうち **gap 部は 23%
（§6 / §8.4 / §9）**、**machinery 部が 44%**。**削減はすべて machinery 側で行う。**

各候補について「**これが無いと何が壊れるか**」を先に答える（§11 の規律）。

| 候補 | 語数 | これが無いと何が壊れるか | 判定 |
|---|---|---|---|
| **§2.9**（fully performed / not executory）| 111 | **何も壊れない。** 倒産法上の分類は forum が決めるもので、条文が宣言しても拘束しない（**E5 が既に記録**）。支える事実（継続債務が無い）は §2.2 / §10.4 に在る | **削除。事実は残し、結論を落とす** |
| **§15.2**（単複・"including"）| 45 | **何も壊れない。** MIT / 0BSD / Unlicense はいずれも持たない | **削除** |
| **§15.3**（contra proferentem 否認）| 28 | §15.1 が既に「最も広い許諾・最も少ない義務」へ construe せよと述べており、**同じ方向を二重に言っている** | **削除** |
| **§15.5**（沈黙が復活を意味しない）| 75 | §2.2（irrevocable・further term 不可）と §10.4（何も終了しない）が同じことを述べる | **§2.2 へ 1 文で統合** |
| **§15.6**（代理・組合の否認）| 20 | 条件を一切課さない instrument で、代理関係が読み込まれる筋が薄い | **削除候補（最小の価値）** |
| **§1.10 "Reservation"**（定義）| 74 | 使用箇所は **§6.2 / §6.3 のみ**。定義語にする必要が薄い | **使用箇所へ inline（≈40 節約）** |
| **§2.5**（reliance / estoppel）| 90 | **半分は壊れる。** 無償の一方的許与に対する「約因が無い」攻撃への備えで、§2.2 の irrevocable だけでは同じ働きをしない | **圧縮（≈45 節約）。削除はしない** |

**合計 ≈529 語（本体の 12%）。gap 部には 1 語も触れない。**

### §16.4 / §16.5 —— 削除ではなく、統合が正解だった

**当初は「§16.4 + §16.5 を落とせば 165 語」と見積もった。§11 の問いを当てて撤回する。**

**§16.4 が無いと何が壊れるか**: 名前と識別子が 1 つの固定テキストを指す保証が消える。
**MIT / 0BSD / Unlicense はこの条項を持たないが、代わりに SPDX と OSI がテキストを固定している。**
**ACD-1.0 はまだどちらにも載っていない** —— **つまり §16.4 は、登録されるまでの橋である。**
（CC は商標で同じ働きをさせるが、ACD は商標を持ち出さない。）

**したがって削除しない。代わりに §16.5 を消す。**
§16.5（100 語）は「翻訳は改変ではない」と述べるためだけに在り、
**それは §16.4 の側に 1 節で書ける**（*"a translation, identified as such and stating that the
English text prevails, is not a modified text for this purpose"*）。
**§15.8 との緊張も同時に消える** —— §16.5 はその緊張を後から埋める節だった。

**節約 ≈85 語。そして E2 / E3 / E12 が触る面が 2 節から 1 節へ減る。**

### この節が establish しないこと

- **これは改訂の実行ではない。** 本文は凍結中であり、`license-discuss` の結果を取り込む前に
  successor を確定しない（`REVISION-PROTOCOL.md` §2 / オーナー確認済みの計画）。
- **削減量は目標ではない。** 「短くする」ために gap を削らない。上の表は
  **gap を担う §6 / §8.4 / §9 を対象から外したうえで**作ってある。
- **失うのは防御であって許諾ではない。** §15.2〜§15.6 は争われたときの備えで、
  **MIT・0BSD・Unlicense はそれを持たずに承認されている** —— 先例のある方向への移動である。

## 2.6 縮小候補を**実際に書いてみた**結果 —— 見積もりは 42% 外れていた

**§2.5 の表は語数を「節の大きさ」で並べていた。書き換え後の文を実際に起草して数えると、
削減量は ≈529 語ではなく **306 語（本体 4,574 → 4,268・6.7%）** だった。**
**見積もりを訂正する。**

| 対象 | 現 | 改定後 | 削減 | なぜ見積もりが外れたか |
|---|---:|---:|---:|---|
| §2.9 | 111 | **55** | **56** | 落とすのは *"not executory"* の**結論**であって節ではない。倒産手続が許諾に影響しないという**事実は残す**必要がある |
| §15.2 | 45 | 0 | 45 | — |
| §15.3 | 28 | 0 | 28 | — |
| §15.5 → §2.2 | 75 | **18** | **57** | 統合は削除ではない。1 文は残る |
| §15.6 | 20 | 0 | 20 | — |
| §2.5 | 90 | **35** | **55** | 圧縮のみ（estoppel の芯は残す）|
| §16.4 + §16.5 | 165 | **120** | **45** | **2 度目の訂正。** 165 → ≈85 と直したが、まだ多かった。翻訳の但し書きは §16.4 に**書き足す**ので、消えるのは重複部分だけ |
| ~~§1.10 の inline 化~~ | 74 | — | **0（撤回）** | **"Reservation" は §6.2 / §6.3 だけでなく §2 でも使われている**（実測 3 箇所）。74 語の列挙を 3 箇所へ展開すれば**長くなる** |

**合計 306 語。gap 部（§6 / §8.4 / §9・1,041 語）には 1 語も触れていない。**

### 起草した置換文（successor 候補・1.0 は凍結中につき適用しない）

**§2.9（結論と自己説明を落とし、事実を残す）**

```
  2.9  No insolvency, bankruptcy, administration, receivership, liquidation,
       dissolution, or similar proceeding in respect of the Dedicator, and no
       act of a trustee, administrator, receiver, liquidator, or equivalent
       officer, affects a permission granted here or revives a right given
       away. Such an officer is a person to whom rights are transferred for the
       purposes of Section 2.8.
```

**§2.2 の末尾へ（§15.5 の統合先）**

```
       Silence, delay, or non-enforcement by the Dedicator does not revive,
       reserve, or narrow anything this Dedication gives away.
```

**§2.5（圧縮）**

```
  2.5  The Dedicator makes this Dedication intending that others rely on it and
       incur effort and expense in doing so, and will not assert that it is
       revocable or ineffective for want of consideration or formality.
```

**§16.4（§16.5 を吸収）**

```
  16.4 The text of this Dedication may be copied and distributed verbatim by
       anyone, in any medium, for any purpose, without charge or permission. It
       may not be distributed in modified form under the name "Autonomous
       Commons Dedication" or under the identifier "ACD-1.0", so that the name
       and the identifier continue to denote one fixed text. A modified text
       may be distributed under a different name. A translation is not a
       modified text for this purpose, and may be distributed under the name
       and the identifier if it is identified as a translation and states that
       the English text prevails (Section 15.8); that proviso is a condition
       upon distributing the translated text, not upon any use of the Work
       (Section 10.5).
```

### そして、これで足りないことが分かった

**改定後は本体 4,268・全体で約 4,590 語。** 委員長が engage しなかった 2 例は
**3,888 語**と**約 4,500 語**である（#116）。**機構部だけを削っても、その 2 つを下回らない。**

**したがって B3 は「無駄を削る」問題ではない。** 下回るには次のどちらかが要る ——
**(a) gap 部（§6 / §8.4 / §9）を削る**＝新規性の根拠を捨てるので**採らない**、
**(b) 構造を変える**＝本文を短い中核に絞り、説明的な節（§2 の一部・§15・§16）を
**規範的でない附属文書へ出す**。

**(b) には代償がある** —— 附属文書は審査対象ではないので、**そこへ出した説明は「本文が
述べていること」ではなくなる**。§4.4（献呈が無効でも許諾は独立に働く）のような
**答えを条文で持っていること自体が我々の主張**だったので、どれを本文に残すかは
**語数ではなく「争われたときに条文が答えているか」で決める。**

**この判断は successor 設計の中心であり、まだ決めていない。**

## 2.7 では (b)「説明的な節を附属文書へ出す」は成立するのか —— 測って否定した

**§2.6 は「機構部を削っても 3,888 語を下回らない」で終わっていた。次の一手として
(b) 構造変更（本文を中核に絞り、説明的な節を規範的でない附属文書へ出す）を挙げていたので、
**成立するかどうかを測った。結論は「成立しない」。**

### 測り方

**節ごとに「語数」と「ドシエが実際に引いている回数」を数え、1 引用あたりの語数を出した。**
引用元は `objection-map` / `against` / `reviewer-positions` / `errata` / `review-precedents` /
`faq` / `jurisdictions` の 7 文書、**`§N.M` が本文に実在する条番号であるものだけ**を数えた。

> **⚠ 最初の集計は誤りだった。** `§(\d+)` で数えたので、`comparison.md` §1.45 のような
> **ドシエ自身の節番号**が「§1」として混入し、§1 が 129 回引かれていることになっていた。
> **有効な条番号 82 件の集合と突き合わせて数え直した**（正しくは 50 回）。
> **「測定系を疑う」は、自分の集計スクリプトにも当てる。**

| § | 語数 | 引用 | 語/引用 | 内容 |
|---:|---:|---:|---:|---|
| 10 | 174 | 67 | **3** | 条件の不在 |
| 16 | 346 | 97 | **4** | 適用方法とテキストの地位 |
| 11 / 12 | 290 / 273 | 55 / 54 | **5** | 商標・虚偽表示 / 人格権 |
| 4 | 382 | 54 | **7** | 許諾 |
| 13 | 105 | 15 | 7 | 無保証 |
| 6 | 272 | 27 | 10 | ML・TDM |
| 1 | 573 | 50 | 11 | 定義 |
| 2 | 554 | 43 | 13 | 範囲と効果 |
| 3 / 8 / 9 | 114 / 578 / 171 | 8 / 40 / 12 | 14 | 献呈 / 特許 / 機械生成物 |
| 7 | 67 | 4 | 17 | データベース権 |
| 5 | 178 | 8 | 22 | 不行使の合意 |
| 15 | 324 | 14 | **23** | 解釈と可分性 |
| 14 | 94 | 3 | **31** | 責任制限 |

**この指標が測っているのは「審査者の関心」ではなく「我々自身の関心」である。** 引用元は
すべて我々が書いた文書だからで、**外部の関心の代理には使えない。** 使えるのは 1 点だけ ——
**「争点として一度も出てこない節はどれか」。**

### なぜ (b) が成立しないか

**附属文書は審査対象ではない。** だから移してよいのは「争われても条文で答える必要がないもの」だけ。
ところが上の下位 4 つは、**どれも移せない。**

| 節 | なぜ移せないか |
|---|---|
| §14 責任制限 / §13 無保証 | **移せば instrument が無保証条項を持たないことになる。** 承認済みの permissive ライセンスは例外なく本文に持つ。**ALL CAPS の conspicuous 表示（McCoy 氏が言及した UCC 慣行）も、本文にあって初めて意味がある** |
| §5 不行使の合意 | **§3 が無効だった場合の受け皿**であり、§4.4 と対で「献呈が働かなくても受領者は守られる」を成立させる ——**我々の中核主張そのもの** |
| §7 データベース権 | 委員長が「モデルの保護理論の一つ」と述べた当のもの（§7 は 67 語で、**削っても 1.5% に満たない**）|
| §15 解釈・可分性 | §15.4（可分性）は §12.6・§2.6 などが**名指しで参照している**。移すと参照が本文の外を指す |

**そして最も重いのは §16 である。** 1 引用あたり 4 語＝**最も争点になっている節の一つ**で、
**§16.4 は識別子が固定テキストを指す保証**（§2.6 で「登録されるまでの橋」と確認した）。
**移動候補としては最下位である。**

### したがって B3 に残る道は 1 本だけ

**(c) 本文の中で圧縮する。** 対象は **§1（573）+ §2（554）+ §15（324）+ §16（346）= 1,797 語、
本体の 39%**。**§2.6 の 306 語はすでにこの領域から取っている。**

**そして、正直に書いておくべきことがある** ——**3,888 語（委員長が "excessively wordy" と述べた
提出物）を下回るには、この 1,797 語を半分以下にする必要がある。**
定義 10 件はすべて使われており（§4c・最少でも 3 箇所）、**削るのではなく書き直すことになる。**
**それが gap を損なわずに可能かどうかは、まだ実証していない。** §2.6 の教訓
（**見積もりは書いてみるまで当たらない**）をここにも当てる ——**次の増分は、見積もりではなく
実際の圧縮案 1 節分から始める。**

## 2.8 (c) 本文内圧縮を、いちばん大きい定義 3 件で実測した —— 20%、そして届かない

**§2.7 は「残る道は (c) 本文内圧縮のみ」で終わった。見積もりで語らないと決めたので、
最大の定義 3 件を実際に書き直した。**

| 条 | 現 | 改定案 | 削減 | 意味の変化 |
|---|---:|---:|---:|---|
| §1.5 Covered Rights | 89 | **66** | 23 | **無し。** 列挙（broadcast and recording rights → recordings）を縮め、除外 3 件を括弧参照へ。**除外の範囲は同一** |
| §1.9 Contribution | 72 | **53** | 19 | **無し。** 「意図的とは何か」の同語反復（*"intentional if it is made … for that purpose"*）を落とした。除外 2 件は残す |
| §1.4 You | 67 | **63** | 4 | **無し。** ほぼ圧縮余地が無い —— **既に締まっている条もある**という信号 |

**3 件で 228 → 182 語（20%）。**

### 起草した置換文（successor 候補・1.0 は凍結中につき適用しない）

```
  1.5  "Covered Rights" means every right the Dedicator holds or may come to hold
       in the Work, anywhere and however arising, now or in future, whether or
       not presently known or subsisting, including copyright, rights in
       performances and recordings, sui generis database rights, and rights
       against unfair extraction. It excludes patent rights (Section 8),
       trademarks and rights in a name (Section 11), and Moral Rights
       (Section 12).

  1.9  "Contribution" means any work of authorship, including a modification,
       addition, correction, translation, or accompanying material, that a
       person intentionally submits for inclusion in the Work to the Dedicator
       or to a repository or forum the Dedicator maintains. Material sent for
       discussion only, or marked by its sender as not a Contribution, is
       excluded.

  1.4  "You" means any person or entity exercising permissions under this
       Dedication, whether human, organisational, or automated, and "Your" is
       construed accordingly. Where an automated system exercises a permission,
       it is granted equally to the person or entity on whose behalf it acts and
       to the one that operates it, so that no permission fails for want of a
       legal person to hold it.
```

### 20% を機構部 1,797 語すべてに当てても、届かない

**外挿すると約 360 語**（**これは外挿であって測定ではない。§1.4 が示すとおり、
既に締まっている条ほど率は下がる**）。§2.6 の 306 語と合わせて **約 666 語**、
**4,896 → 約 4,230 語。**

**委員長が *"excessively wordy"* と述べた提出物は 3,888 語である（#116）。届かない。**

### したがって B3 の結論

**長さは「解消できる項目」ではなく「縮められるが答えきれない項目」である。**
gap 部 1,041 語を削れば届くが、**それは新規性の根拠を捨てることなので採らない**
（`ACD-OSI-BOTTLENECKS.md` B10 が「gap が残っているか」を最高位に置いている以上、
**B3 のために B10 を悪化させるのは取引として成立しない**）。

**残る緩和は 1 つだけで、それは本文の外にある** —— **短い入口**。
#116 の disposition が既にそう書いていた（*"長さへの実際に効く緩和は短い入口である"*）。
**現状の実測**: 送る文面は **972 語**（`submission.md` §B.0）、入口ページ `REVIEWERS.md` は
**約 1,900 語**、`objection-map.md` は **653 語の 1 つの表**。
**審査者が最初に触れる面はすでに本文の 1/5 である。**

**この結論は「何もしない」ではない。** §2.6 と §2.8 の置換文 7 件は successor 候補として
そのまま使える（**約 350 語・gap 損失ゼロ**）。**ただし「短くすれば通る」という筋書きは、
測定によって否定された。**

## 3. 議論から来たもの（返信を受け取ってから埋まる）

| ラウンド | 出所（`rounds/` の file） | 指摘 | 帰結 |
|---|---|---|---|
| — | — | **まだ届いていない。** `license-discuss` への投稿（2026-08-26）に返信はなく、原典で確認済み | — |

## Constraints

- **1.0 の本文は凍結。** ここに何が書かれても Check 453 が本文の変更を BLOCKING で止める。
- **版管理は併置。** `REVISION-PROTOCOL.md` §2 のとおり 1.0 は永久凍結し、1.1 は置き換えではなく
  並べて公開する。読まれたテキストが後から動けば、その議論は何についてのものでもなくなる。
- **反映は網羅的に。** 「全部取り込んだ改善版」がオーナーの方針であり、選り好みして取り込むと
  次のラウンドで同じ指摘が返ってくる。

## Change impact

`errata.md` に entry を足したら、この表にも同じ `E<n>` を足す（Check 464 が強制）。
`discussion-log.md` で帰結が `1.1 候補` になったら §3 へ移す。

## Audience-specific notes

- **審査者**: これは「指摘を受けたらどこへ行くか」の行き先である。1.0 の本文はこの文書の存在に
  よって一切変わらない。
- **後任 AI**: 議論が終わってから集めようとしないこと。**貯まる先を 1 つにしてあるのは、
  4 か所を回る手順が必ず落とすからである。**
