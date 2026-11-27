---
file: LICENSES/ACD-OSI-BOTTLENECKS-EXTERNAL.md
audience: 次のセッションの実装者（一次読者）/ OSI license-review participants / 監査人
last-updated: 2026-11-15
canonical-ref: LICENSES/ACD-OSI-BOTTLENECKS.md (索引・分類・集計はあちらが canonical) / LICENSES/ACD-1.0.against.md / LICENSES/AS-OF.md
---

# OSI Approval Bottleneck Register —— 外の答えに依存する項目

**索引・分類・集計は [`ACD-OSI-BOTTLENECKS.md`](ACD-OSI-BOTTLENECKS.md) が持つ。**
**この file はその一部であって、別の一覧ではない。** 項目を足すときは**必ず向こうの索引にも行を足す**
（**Check 460 face (m)** が索引の表と集計行を照合する）。

**ここに在るのは、我々の作業では動かせない 8 項目（7 節）である** ——
**B1 + B2**（法的レビュー / 実使用）/ **B4**（献呈と許諾の並存）/ **B5**（§4.4 第 2 文・起草は 1.1 で閉じ設計の問いが外部）/
**B7**（§8.4 の特許射程）/ **B10**（gap が残っているか）/ **B11**（SPDX 未登録）/
**B15**（主題適格）。**2026-09-28 訂正**: 旧文はここに B14 を挙げ B15 を欠いていた —— 2026-09-25 に B14 を `ACD-OSI-BOTTLENECKS-POSTING.md` へ分離し B15 を新設したとき、この列挙だけが追従していなかった。

**「動かせない」は「やることが無い」ではない。** B1 は提出の産物であり、B2 は discoverability だけが
制御でき、B7 / B10 は提出資料での説明可能性が我々の持ち分である。**各節の末尾にそれを書いてある。**

---
## B5 —— §4.4 第 2 文。**起草の側は 1.1 で閉じ、設計の問いだけが外に残る**

**なぜ承認上の問題か（事実）**: §4.4 第 2 文は
*"Where Section 3 is effective, this Section is redundant but not void, and it remains available to
be relied upon by You."* と述べる。**献呈が成功した場合を正しく描写しているかについて、
読みが 2 つ立つ。**

| 読み | 内容 |
|---|---|
| **A** | §4.1 は現在の無条件の許諾であり、その存在は §3 の失敗に依存しない。ゆえに §3 が成功すれば単に冗長になるだけで、先に与えた独立の許諾は無効にならない |
| **B** | 許諾は独立だが、**Covered Right が実際に手放された後は、許諾が作用する排他権がもう存在しない**。その権利について「依拠し続けられる」と述べるのは不正確でありうる |

**受領者から見た結果はどちらでも同じである** ——権利が消えていれば許可は不要、残っていれば §4.1 が与える。
**したがってこれは「誰かが自由かどうか」ではなく「§4.4 が法的経路を正しく述べているか」の問題である。**

**分岐**: (1) **設計の問題** ——献呈と無条件の現在許諾を、そもそも独立並行の footing として
構成すべきでない / (2) **起草の問題** ——構成は妥当で、§4.4 が「消えた権利の上で作用し続ける」と
言い過ぎているだけ。この場合の修正は**独立性だけを述べてそこで止めること**。

**なぜ AI が決めないか**: **これはドシエで唯一、内部で見つけたのではなく steward が
`license-discuss` に自ら出した問い**である（2026-09-06 の 2 通目・`errata.md` **E11**）。
**答えは外から来る。** そして **steward は「現在の文言が既に coherent なら、不要な改訂はしたくない」
と明言している** ——**凍結中の本文を、答えが来る前に触らない理由がここにもある。**

> **2026-09-28 訂正（この節の status と下の「現在の運用」段落は E11 が閉じる前に書かれていた）**: errata E11 は **2026-09-14 に 1.1 草案で閉じた** —— 分岐 (2) の形で、問題の 1 文を落とした（語数 −26・受領者への保証は前後の 2 文が担う）。1.1 / 1.2 草案に当該文は 0 件、**1.0 には凍結のため残る**。**外に残るのは分岐 (1)（設計）の問いだけ**で、それは steward が出して未回答のまま。下の「解消したときに失うもの」は、実際に採った分岐 (2) の費用の事前分析として読める。

**status（2026-09-14 以前）: 外部回答待ち。** **B14 により、その問いへの回答が来る経路も現在は止まっている**
（`license-discuss` は返信ゼロで、発信も止めている）。**B5 は B1 と同じく「提出の産物」側の項目である。**

**解消したときに失うもの（2026-09-13・逆から読む）**

**枝 (2)（起草の問題として、独立性だけ述べて止める）を採ると、§4.4 の存在理由そのものが薄くなる。**
§4.4 が担っているのは **gap 主張の 1 本目** ——*"Unlicense の 2020 年の拒否は「まったく明確でない」で、
それに答えたのは『献呈が無効でも列挙された許諾は作用する』という議論だった。その議論は Unlicense の
テキストには無く、リストで述べるしかなかった。§4.4 はそれを本文で述べる"*（提出文 §B.0）。
**「§3 が有効な場合にも依拠できる」を落とすと、残るのは「独立に付与された」だけになり、
*受領者が §3 の有効性を判断しなくてよい* という、我々が最も強く主張している性質の根拠が弱くなる。**
**つまり正確性を上げる修正が、gap を削りうる** ——B7 と同型の一方向の取引である。

**そして「答えを待つ」こと自体にも費用がある。** B14 で発信が止まっており、
`license-discuss` は返信ゼロである。**待つ期間に上限が無いと、E11 が 1.1 全体を無期限に止める。**
**当時の運用はそうなっていなかった** ——1.1 草案は E11 以外の 7 件を閉じて進んでおり、
**E11 だけが未着手のまま併置されていた**（その後 2026-09-14 に E11 も閉じた・上の訂正）。 **これは意図した形であり、「待ち」が全体を止めていない
ことを、ここに明記しておく**（次のセッションが「E11 待ちだから 1.1 は動かせない」と読まないために）。

**外部確認**: **必要（定義上）。**

---

## B7 —— §8.4 の特許射程。**B10 と一方向に結ばれており、独立には動かせない**

**なぜ承認上の問題か（事実）**: McCoy Smith 氏が別の提出について
*"it is an issue as to whether a license of this scope would gain significant uptake
at least from patent holders"* と述べている（`license-review` 2025-05-14・#107）。
**ACD-1.0 の §8.4 は、Computational Use と、そこから生じる model / parameter set / weight /
embedding / output にまで特許許諾を及ぼす。** 射程はこの発言が想定するものより広い。

**そして uptake は我々が既に落ちている基準である**（B2・採用 1 件）。
**gap を担う条項が、採用を下げる条項でもある** ——これが B7 の実体である。

**条文から確定すること（読んで確かめた）**

1. **費用を負うのは特許を持つ採用者と貢献者だけである**（2026-11-06 訂正: 貢献者を足した・§2.6・`gap-measurements.md` §1.136）。§8.5 が *"reach only patent claims the
   Dedicator owns or controls"* と限っているので、**特許を持たない採用者は何も手放さない。**
   uptake への影響は**採用者全体ではなく、特許保有者という部分集合**に限られる。
2. **報復条項で緩和する道は、構造上ふさがっている。** §8.2 は報復条項の不在を
   *"deliberate"* と明言する。**報復条項は条件であり、§10.1（条件の不在）と §4.3 に正面から反する。**
   ACD-1.0 の中核主張は「何も課さない」ことなので、**uptake のために条件を足すのは、
   主張そのものを捨てることになる。**
3. **opt-out で緩和する道もふさがっている。** 留保・オプトアウトは §6.2 が
   *"makes no Reservation … and expressly declines to make one"* と否定した当のものである。
4. **したがって残る調整は「射程を狭める」しかない。** ところが §8.4 は
   **gap 3 件のうちの 1 件そのもの**である（`ACD-1.1-CHANGELIST.md` §2.6 の測定で 583 語の §8）。
   **狭めれば B10（新規性の根拠が残っているか・最高位）が縮む。**

**結論: B7 は独立の項目ではなく、B10 との一方向の取引である。**
**uptake を上げる方向の変更は、例外なく gap を削る。** **（2026-11-04 訂正: 「例外なく」は言い過ぎだった。1.4 の §8.4 の限定は無関係な請求項を外して B7 の費用を減らしたが、§8.4 + §8.2 の組み合わせは残る。ただし「Work が教える特徴」の部分は残るので、説明文書に ACD を付けた特許権者の費用は新しく明記した —— `faq.md` A32。）** B1 + B2 が 1 文で結ばれていたのと同じく、
**B7 と B10 も切り離して扱ってはならない。**

**変更によって失うもの / 残る gap**: 上記のとおり、**失うのは gap そのもの**であり、
**残るのは「特許保有者の採用が薄い」という不利な事実**（#107）である。**どちらも消せない。**

**副作用・新たな反論**: §8.4 を残す判断を明文化すると、
「**採用されないと知りながら残した**」と読まれうる。**それは正しい要約である** ——
我々は uptake より gap を選んでいる。**その選択自体を隠さずに書く。**

**外部確認**: 不要（判断は一次資料と条文から出る）。**status: 取引として記録済み・変更しない。**

**2026-09-10 追記（外部の一次資料）**: `license-review` は 2026-09 に**終了トリガーの境界**を
論じている（Fontana 氏「著作権に何か特別なものがあるのか、特許にあるのか」／Gay 氏「価格の存在と、
その価格が自由と整合するかは別の問い」）。**§8.2 はどの種類の主張でも終了しないので、この論争に
乗る面が無い**（`review-venue.md` §1.69）。**ただし「係争域の外」は有利にも不利にも読める** ——
**争点を持たないことは、審査者が労力を割く理由も持たないことでありうる。**

**2026-09-10 追記（同じ敵対的読解から）**: **§8.4 の *"resulting from that use"* には程度の限定が無い。**
巨大なコーパスに本著作物を**極少量混ぜて学習したモデル**も「その使用から生じた」と主張しうる読みを
条文が誘う（`errata.md` **E15**・**裁判所がそこまで読むかは分からない。述べているのは条文が誘う読み**）。
**これは B7 の取引をさらに鋭くする** ——閾値を入れれば特許保有者の懸念（#107）に応えられるが、
**その閾値こそが gap の一部**であり、B10 を縮める。

---

### 🔴 2026-09-14 追記 —— §15.1 が B7 を増幅する（外部レビューで初めて指摘された）

**`ACD-1.1.txt` §15.1 はこう述べる**:

> *"This Dedication is to be construed so as to give the **widest permission and the least
> obligation** that its words allow. Where a provision is capable of more than one reading,
> **the reading that grants more to You prevails**."*

**⚠ 2026-09-14 に、この節の前提を同日中に訂正した。** 初版はここで
**「この解釈規則はドシエで一度も分析されていなかった」**と述べ、根拠に
**「`widest permission` の語が `LICENSES/` の全 .md で出現 0」**を挙げていた。**どちらも誤りである。**
**想定問答 clauses 分冊の Q22 が §15.1 を正面から扱っている**（*「最も広く読め ——当事者が裁判所に
読み方を指示できるのか」*）。**文字列の出現数を、被覆の主張として報告した** ——
**#87 が「名称一致は下限であって全数調査ではない」と書いた当の誤りを、別の対象で繰り返した。**

**訂正で変わらないもの（併記する）**: **Q22 が扱っているのは*執行可能性*である**
（当事者は裁判所に読み方を指示できるのか / §5.2(c) の covenant がそれを実効化する）。
**Q22 は、この規則が*どちらの向きに*効くかを扱っていない。**
**下の B7 との連結は、いまも新しい。**

**なぜ B7 に効くか。** B7 は「§8.4 の特許射程が広く、特許を持つ採用者の uptake を下げる」ことである。
**§15.1 は、その射程が曖昧なとき、曖昧さを*採用者に不利な側*へ解決する** ——
**"You" に多くを与える読みが勝つのだから、Dedicator（＝採用者）の特許許諾は広い方に倒れる。**
**つまり §8.4 の不確実性は、§15.1 によって「どちらに転ぶか分からない」ではなく
「広い方に転ぶ」になる。**

**これは B7 の重みを上げる。** 特許を持つ組織が ACD を採用するかを検討するとき、
**§8.4 の境界が不明なこと**（外部レビューが挙げた 6 つの境界事例・`discussion-log.md` ラウンド 0 #3）
**と §15.1 の解釈規則は、掛け算になる。**

**⚠ 逆側（同じ重さで書く）。** **§15.1 は削れない、あるいは削るべきでない。**
(a) **利用者保護そのものである** ——本 instrument の目的は「条件ゼロ」で、
曖昧さが利用者不利に解決される instrument はその目的を裏切る。
(b) **OSD 適合の側では有利に働く** ——承認基準の 1 つは「曖昧さが実質的な効果を持たないこと」で、
**§15.1 は「曖昧なら広い方」と決めることで、曖昧さが*権利を狭める*方向へ効くのを封じている。**
(c) **したがって §15.1 は B7 と B10 の取引の一部である** ——B7 を下げるために §15.1 を弱めると、
**曖昧さが利用者不利に働きうる instrument になり、gap 主張（条件ゼロ）そのものが弱くなる。**

**結論: §15.1 は変えない。変えるべきは §8.4 の境界の説明可能性のほうである**
（**条文ではなく提出資料で** ——E6 / E15 で「狭めない」と決めた判断は維持する）。
**本節はその判断を変えないが、「なぜ B7 が思ったより重いか」の理由を 1 つ増やす。**

## B11 —— SPDX 未登録と REUSE 命名。**開示は行き渡っている。動かさない理由の方が重い**

**測定（2026-09-10）**

| 面 | 実態 |
|---|---|
| per-file の `SPDX-License-Identifier` ヘッダ | **0 件**（#106 が記録した当のもの）|
| `LICENSE` の宣言 | `SPDX-License-Identifier: ACD-1.0` —— **これは今日時点で解決しない式である**（SPDX 未登録の licence は `LicenseRef-` を要する）|
| 適合形の開示 | **5 面以上に在る** —— `LICENSE` 本文 / `llms.txt` / `llms_well-known.txt` / `llms-full.txt` / `submission.md` の 2 箇所 / FAQ / **`errata.md` E1**（§16.1 が指示する通知の書き方そのものが非適合だと自分で記録している）|
| REUSE 適合 | **`REUSE.toml` も `.reuse/` も無い** |

**やらないと決めたこと、と理由**

1. **`LICENSES/ACD-1.0.txt` を `LicenseRef-ACD-1.0.txt` へ改名しない。**
   **提出パケットと公開面が指している URL がその path であり、審査中に動かすと
   「審査者が読んでいるテキスト」の所在が変わる。** 凍結が守っているのは中身だけでなく**所在**でもある。
2. ~~**`REUSE.toml` だけを足すこともしない。**~~ **この判断は後に覆した** —— `REUSE.toml` は
   #106 を潰すために追加済み（`bad599f6`）で、**file 単位の沈黙は閉じた**（2026-09-24 に `reuse` 6.2.0 で
   実測: `LICENSES/` を本文 2 本だけにしたコピーで **614 / 614 file に著作権とライセンスの情報が付く**）。
   **適合はしない**という予測は正しかったが、理由は予測より多かった —— 下の「消えないこと」。
3. **per-file ヘッダを全ファイルへ入れることもしない。** shipped JS / CSS / HTML の
   バイト変更は AIO digest 連鎖と screenshot 面に波及し、**B14 で発信が止まっている今、
   審査に効かない変更に非破壊性の予算を使うことになる。**

**承認で消えること / 消えないこと**

- **消える**: 識別子の非適合（`ACD-1.0` が List に載れば `LicenseRef-` は不要）と、
  それに伴う REUSE の命名要件。
- **消えない（2026-09-24 に `reuse lint` 6.2.0 を実際に走らせて確定）**:
  - **`LICENSES/` がライセンス本文の置き場ではなくドシエの置き場になっていること。** REUSE は
    `LICENSES/` の全 file をライセンス本文として読むので、本リポジトリでは本文 2 本以外の 85 file
    （ドシエ・記述子・`spdx.xml`・草案・`rounds/`）から識別子を作ろうとし、**評価に入る前に CRITICAL で
    停止する**（`LICENSES/README.md` と `LICENSES/rounds/README.md` が同じ識別子 `README` になるため）。
    **承認とは無関係である。**
  - **散文や正規表現の中の `SPDX-License-Identifier:` という文字列**が REUSE にタグとして読まれ、
    無効な式として 11 件報告される（Check のソースと文書）。これも承認と無関係。
  - ~~#106 の per-file 沈黙~~ —— **`REUSE.toml` で閉じた**（上の 2）。
  - **閉じ方の選択肢は分かっているが、どれも費用がある**: ドシエを `LICENSES/` の外へ移すと、
    提出パケットと公開面が指す path が審査中に動く（上の 1 と同じ理由）。散文中のタグは
    `REUSE-IgnoreStart` / `REUSE-IgnoreEnd` で囲めるが、Check のソースを含む十数 file に手が入る。
    **どちらも今は行わず、「承認されれば REUSE に適合する」とは言わない**ことだけを正す。

**解消したときに失うもの（2026-09-13・逆から読む）**

**上の 3 項は「なぜ動かさないか」だけを述べており、動かさない側の費用を書いていなかった。**
**未登録が毎日課している費用は実在する** —— **E1**（推奨 notice が指示する
`SPDX-License-Identifier: ACD-1.0` は、未登録の識別子としては非適合で、
適合形は `LicenseRef-`）は**登録されるまで消えない**。つまり
**本文が読み手に不正確なことを指示している状態が続く**（errata で「最高」と格付けした当の項目）。
**採用者が SPDX ツールチェーンを使うほど、この不一致に当たる確率は上がる** ——
そして **B2（採用の少なさ）を解消しようとするほど、E1 の露出は増える。**

**それでも動かさない理由は変わらない**（審査中にテキストの*所在*を動かさない）が、
**「費用ゼロで待っている」のではなく「費用を承知で待っている」と書くのが正確である。**

**外部確認**: 不要。**status: 開示済み・意図的に未実施（理由は上記）。**

---


**2026-11-15 に足した —— 承認の対象は本文で、識別子は SPDX が別に割り当てる。** Richard Fontana 氏 2024-08-09（`license-discuss`・"Not speaking for the OSI" と断ったうえで）*"OSI does not approve, or up till now hasn't approved, SPDX identifiers as such, but rather the actual licenses they refer to"*（`review-readings-2.md` §1.231・portfolio-2f）。ACD の §16.1 と §16.2 は識別子 `ACD-1.4` を本文の中で先に名指し、一覧に載るまでは `LicenseRef-ACD-1.4` と書く。SPDX が別の識別子を割り当てれば、本文の名指しと一覧が食い違う —— 版を確定する前に SPDX に識別子を確かめられないので、この費用は承認の後に残りうる。**有利な先例**: 承認された CAL-1.0 の本文は *"SPDX-License-Identifier: CAL-1.0"* を適用の印として条文で名指し、審査でこの名指しへの異議は見つからなかった（委員会報告 2020-02-09 の Exhibit A・同節）。**逆側**: CAL の 2 つ目の札（例外つきの形）が SPDX の一覧の識別子と一致するかは確かめていない（SPDX の一覧の外部取得はこの session では許されていない）。

**2026-11-16 に足した —— SPDX は、略称の混同を避けるために提案の識別子を変えたことがある（B6 の段）。** VM (Vicky) Brasseur 氏 2020-12-28（`license-review`・OIN License）*"The license was also submitted to SPDX for inclusion in its list. Earlier today the team changed the proposed license identifier to avoid potential confusion with Open Invention Network"*。ACD の識別子（ACD-1.x）は SPDX の一覧で空いているが、SPDX に出すときに略称の重なりが同じように問われうる。**逆側**: その件は同じ分野の組織との重なりで、ACD について同じ点が挙がった記録は無い。

## B1 + B2 —— この 2 つは、リスト上では**別々ではなく 1 文で**争われている

> **🆕 2026-09-22 追記 —— B2 の板挟みを、Chestek 氏（委員・元委員長）自身が「Catch-22」と呼んでいた。**
>
> > *"Yes, the review process certainly creates a **Catch-22**. **We want to see licenses early to
> > correct them, but are less inclined to approve a license that doesn't have a track record.**"*
> > —— Pamela Chestek 氏・`license-review` 2026-08-26（OpenMDW 審査）。同じ人は 2019-06-04 に、使われていないことは欠点の証拠になりうると述べた（#289）。賛否の全体は `reviewer-positions.md` §1.140（#291・#294）。
>
> **この register は B2 を「解消可能・未実施（discoverability のみ制御可）」と書いてきたが、
> *その板挟みが OSI の側にも在り、Chestek 氏（委員・元委員長）がそう認めている* ことを記録していなかった。**
> **我々の側の困難としてだけ書いていた。**
>
> **⚠ 過大に読まない。** これは「実績が無くても承認する」ではない。
> **「早く見たいが、実績が無いと承認しにくい」という構造を、承認する側が認めた**だけである。
> **B2 の disposition は動かない。** 動くのは、**この板挟みが我々の失敗ではなく
> 手続きの性質である**という一点である。
>
> **⚠ 文脈**: これは steward が「本文を改訂しても、既に配布されたモデルは出荷時の文言のまま」
> と述べたことへの返信であり、**続けて Chestek 氏（委員・元委員長）は「steward の見解は契約解釈に関係しないかもしれない」
> とも述べている**（#124 と同じ論点）。**有利な半分だけを取らない。**

**分けて書かない理由**: ドシエは長らく「法的レビューが無い」(#5 / #79) と「採用が 1 件」(#2) を
別項目・別回答として持っていた。**リスト上では 1 文で結ばれている**（#113）——
Lukas Atkinson 氏・`license-review` 2021-02-14:

> the submission of this license makes a strong argument that **submitted licenses should have
> either received legal review or at least non-negligible use. This license has neither**

**ACD-1.0 はこの選言のどちらの枝も満たさない。** 同スレッドで McCoy Smith 氏は逃げ道を塞いでいる
（*"OSI approval is a mechanism that presents approved licenses to the community as having value as
a legal instrument"* ——これは **§4c を正面から指す**）。Josh Berkus 氏はより端的に、
テスト無しの PR に喩えて *"That's an automatic rejection in most OSS projects I know"* と述べた。

**事実 / 推論 / 予測を分ける**

| | |
|---|---|
| **事実** | 上記 3 発言はアーカイブに在る。ACD-1.0 は弁護士未読・採用 1 件 |
| **事実（逆向き・同じ重さで書く）** | Chestek 氏は PBZC 審査 (2024-12) で法的レビューを *"recommended"* かつ ***"not a blocker"*** と明言し、Berkus 氏も 2025-05 に同趣旨（**3 例**・§1.52）|
| **⚠ その逆向きの、さらに逆向き（2026-09-11 に全数掃引で見つけた）** | **同じ PBZC スレッドの中で、Carlo Piana 氏が *"OSI **requires** prior review by a lawyer because there are things that a layman very likely cannot consider"* と述べている**（2024-12-18・ただし *"in his own capacity"* と自ら明記）。**つまり我々の「recommended, not a blocker」という土台は、同一スレッドの中で別の言葉と併存している。** disposition は変えない（委員長は委員会として述べている）が、**有利な 3 例だけを引いて不利な 1 例を落とせば、それは B1 についての記録ではなく B1 についての弁論になる。** 逐語と方法は `ACD-1.0.review-corpus.md` §1.67 R1 **2026-11-06 訂正: Piana 氏は同じ日に撤回していた** —— *"I stand corrected re: Pam's message on requiring legal review, bad choice of words on my side."* 2 か月間、この行は撤回された発言を立っているものとして扱っていた。 |
| **推論** | **手続き上は要件ではないが、結果としてほぼ必要** ——両立する。要件でないことは、無いまま通ることを意味しない |
| **予測（弱い・根拠を明記）** | 両枝を欠いたまま `license-review` へ出すと「撤回して助言を検討せよ」と言われうる。根拠は PBZC（2024-12・同日撤回）と 2024-09 の撤回勧奨の 2 例のみ |

### B1（法的レビュー）——「待ち」に分類してはならない

**register の表は B1 を「法律家確認待ち」と書いている。この語は誤解を招くので、ここで打ち消す。**
§1.52 が一次資料から確定しているとおり、**このリストの審査者は pro bono の弁護士**であり
（Piana 氏 *"who mostly do this job pro bono, as we are doing now"*・Berkus 氏 *"our volunteer
attorneys"*）、**提出することが、単独起草者の条文を弁護士が論評する場に置く経路である。**

> **⚠ 2026-10-03 是正（週次の矛盾点検・`against.md` #275）**: この段落は直前まで「弁護士の目を通す経路
> **そのもの**」と書いていた。§1.52 は 2026-09-28 に **#274** を受けて「弁護士が論評する場に置かれる」へ
> 狭められている（OSI President: *"OSI's Board does not give legal advice"*・得られるのは論評であって
> 助言ではなく、提出者に従う義務も無い）。**下の「帰結」は維持する**（提出が論評を得る経路であること
> は変わらない）が、**「提出すれば法的レビューを得たことになる」とは読まない。** さらに **#270** —— 我々が
> 依拠する唯一の献呈 + 許諾型の先例（Unlicense）は *"The lawyers who opined … agreed"* で通っており、
> **B1 の重さはこの節が書かれた時より上がっている。**

**帰結: B1 は「提出前に満たすべき前提条件」ではなく「提出の産物」である。**
弁護士を待って提出を遅らせるのは、**得られるはずのものを得ない**だけになる。（2026-11-07 追記: この段落は言い過ぎの側にある。委員長は *"not for workshopping a license, it is for a go/no-go on a license"*（2023・#298）と述べ、佐渡氏も 2026-03-14 に提出の前のレビューを求めた。提出は論評の場であって、レビューの代わりにならない。有利な側の新しい事実は、法律家の分析が 2007 年 12 月まで手順の要件で、そこで外れたことである（`review-rules.md` §1.141）。レビューの無い新規の提出で一覧に在るのは少なくとも 24 件中 1 件である（#297）。）
**AI がこれを解くことはできない。解く手続きは提出である。**

**副作用（自分で作りうる新たな反論）**: §4c を「法的レビューの代替」として提示すると、
McCoy 氏の上記発言に正面から当たる。**§4c は既にその危険を自分で塞いでいる** ——
*"None of these substitute for legal review. They only mean that the failures a machine can find
are not present."* **この 1 文を落としてはならない。**

**2026-11-15 に足した（2 つ目）—— 承認済みのライセンスの取り下げを論じた 2013 年の会話で、法律家の関与について決める側が両側を書いた。** "what would de-listing of licenses look like?"（`license-discuss` 2013-03・`review-readings-2.md` §1.234・portfolio-2f）。**有利な面**: Richard Fontana 氏 2013-03-07 *"you don't need to be, or to get, a lawyer to interpret the OSD (more precisely, lawyers and non-lawyers are equally competent to interpret the OSD)."* **不利な面**: Bruce Perens 氏は取り下げの候補に *"the "crayon" licenses, mostly, those written without legal counsel"* を挙げ、*"It isn't the least bit difficult to diagnose when no lawyer was involved in drafting a license."* と書いた —— Berkus 氏 2020（法律家の声だけが数えられる）・Piana 氏 2024（法律家の目の形跡を探す）・Chestek 氏 2026（この複雑さは専門家の起草が要る）と同じ側の文である。**逆側**: 会話は承認済みのものの取り下げについてで、承認の基準ではない。Fontana 氏の文は OSD の**解釈**についてで、本文の**起草**の質についてではない（Perens 氏の文はまさに起草の質を言っている）。会話の発端は、Fontana 氏自身が過去の承認を *"approved "in haste""* と書いたことだった。

**2026-11-15 に足した（3 つ目）—— 法律家でない作者のライセンスが承認され、OSI がそれを公表している。** 承認済みの Attribution Assurance License について、OSI のサイトは *"The author, who is not an attorney, places this license template into the public domain"* と書いている（McCoy Smith 氏が `license-discuss` 2020-03 に引用・`review-readings-2.md` §1.239・portfolio-2f）。**逆側**: 古い時期の承認で、その後に決める側は法律家の目の形跡を探すようになった（上の Piana 氏 2024・Chestek 氏 2026）。同じ会話は AAL の廃止を論じていた。

**2026-11-15 に足した —— 法律家が起草した文書に、ACD の 3 つの条と同じ並びが在る（起草の先例・承認の先例ではない）。** Open Web Foundation Agreement 1.0 は、約束が後継者を縛ること（3.1.3）、倒産法 365(n) の目的で約束を許諾として扱うこと（3.1.4）、約束を迂回しないこと（6）を持ち、ACD の §2.8（承継）・§2.9（倒産で止まらない）・§5.1（訴えない約束）とほぼ同じ並びである（Lawrence Rosen 氏の `license-discuss` 2013-08-18 の引用・`review-readings-2.md` §1.227・portfolio-2f）。B1 に対して言えるのは「法律家の確認は無いが、同じ問題に法律家が出した答えの形をなぞっている」までである。**逆側**: OWFa は仕様への貢献のための合意で OSI が承認したライセンスではなく、3.1.4 の「約束を許諾として扱う」文を ACD は持たない（本文が法の分類を決める形を避けた・`QUESTIONS-FOR-COUNSEL.md` 問 8 の 2 つ目の問い）。形が似ていることは、効果が同じことの証拠ではない。

**2026-11-15 に足した —— OSD そのものも法律家の手を経ていない（`review-readings-3.md` §1.304）。** 当時の理事 Russell Nelson 氏 2001-09 *"Of course, a big problem with the OSD is that it talks about legal requirements, and yet was not touched by a lawyer before being cast into stone."* **逆側（同じ通）**: 同氏は続けて、大きく書き直すなら法律の経験のある人がすべきだと書いた。法律家の関与が無くてよい、の材料にはならない —— むしろ B1 の不利な側を補う。

**2026-11-15 に足した —— 承認は条項の有効性の意見ではない（`review-readings-6.md` §1.451・portfolio-9b）。** Lawrence Rosen 氏 2002-01-20 *"The OSI board of directors approves licenses if they are consistent with the OSD. The board renders no opinion about the validity or enforceability of specific clauses in specific licenses."* **両面**: B1（法律家の審査が無い）は承認の基準そのものではない、という読みを支える。同時に、承認されても §3 や §4 が各国で有効だとは誰も言わないので、有効性の問いは採用者の法律家に残る（B2 の費用）。

**2026-11-15 に足した —— 2013 年の承認の規則の 4 項目めに、ACD は出せるものが無い（`review-readings-2.md` §1.246・portfolio-2f）。** Luis Villa 氏が挙げた規則 *"4. Provide results of any legal analysis available"*（"Akshar License 1.0 Final Draft"・2013-05）。ACD に法律家の分析は無い。**逆側**: 規則は「available なら」と書き、無い場合を不承認の理由にはしていない。ただし 2024 年以後の決める側は法律家の目の形跡を探している（上の段）。

**2026-11-16 に足した —— 「法的に有効であること」を提出者が立証する（`review-readings-2.md` §1.253・portfolio-2f）。** Josh Berkus 氏 2013-11-07 は、新しいライセンスの提出者が理事会の過半に示すべきものを *"open source - legally valid - needed"* の 3 つとした。「法的に有効」は、法律家の審査が無い ACD には、本文の文と法律家への問い（`QUESTIONS-FOR-COUNSEL.md`）でしか答えられない。**逆側**: 1 人の理事の言い方で、法律家の意見書を要件とする規則ではない（上の 2013 年の規則の「available なら」と同じ）。

**2026-11-16 に足した —— 承認された OSL の起草者は、読み手を法律家と置き、企業の弁護士の審査を経ていた（`review-readings-6.md` §1.456・portfolio-9b）。** Lawrence Rosen 氏 2002-11-06 *"But the real reader of an open source license is another lawyer who is going to advise his client what that word means."*、*"I'm using language from the Copyright Act on purpose."*、同じ通の追伸で *"The license has been submitted to several companies' attorneys for review"*。ACD は "Covered Rights" などの自前の定義語で書かれ、弁護士の審査を経ていない。**逆側**: 同じ起草者は、承認は法的な祝福ではないとも書いた（`review-readings-6.md` §1.454）—— 法律家の起草は承認の要件ではない。

### B2（実使用 1 件）——**作れない。制御できるのは discoverability だけ**

**採用は捏造できない。** 存在しない採用を書けば、それは提出の失格事由であって弱点ではない
（`REVISION-PROTOCOL.md` の規律・オーナー確認済み事実の扱いと同じ）。
**時間と第三者の選択だけが動かす。**

**AI が制御できるのは「見つけられること」だけ**で、実施済みの梃子は 2 つ ——**(1) 2026-09-10 に英語の招待を README の先頭ブロックへ足した**（それまで「あなたの著作物にも使える」は**日本語にしかなく**、採用は日本語圏の外から来る必要がある。**招待と警告を同じブロックに置く** ——法的レビュー無し / OSI 未承認 / SPDX 未登録）、**(2)** 元の梃子は
**README に「誰でも自分の著作物に使える」を招待と警告を同じ文で置いたこと**（#85 の 1 面外側）。
**それ以上は、待つことと、テキストを正しくすること（＝ B3 / B10）に還元される。**

**なぜ B2 に「解消可能・未実施」と書いてあるか**: 採用は原理的に到達可能だからで、
**我々の作業で到達可能という意味ではない。** この区別を落とすと、次のセッションが
「まだやっていない作業」を探して見つからず、時間を使う。

**2026-11-11 に足した —— 承認の後にも、B2 の費用は形を変えて残る。** 2015 年の Apache の第三者ライセンス方針の議論で、利用者の組織は見慣れた組み合わせの外にある承認済みライセンスをパッケージごとに審査すると述べ、財団の側は受け入れの一覧を自分たちの決定だとした（`review-readings.md` §1.181・#322）。承認は受け入れの床を示すだけで、下流の一覧に ACD を載せない。**逆側**: ASF の現行の一覧は基準を OSD への適合に置き、Unlicense・0BSD・CC0 という献呈の型を既に受け入れている（WebFetch の要約・逐語ではない）。この注は B2 の「作れない」を変えない。承認の前に足りないのは採用者で、承認の後に残るのは各組織の審査である。

**2026-11-15 に足した —— 2026 年の委員は「使う」と並べて「使うと表明する」プロジェクトを訊いている。** Carlo Piana 氏 2026-04-17（`license-review`・ISC を基にしたライセンスへの最初の返信）*"Also, is there any project actually using or signalling it will be using the license if/when approved?"*（`review-readings-2.md` §1.222・portfolio-2f）。問いの形が「承認されたら使う」という**表明**を数えるので、承認の前に関心の表明を集めることは、問いにそのまま答える材料になる。窓口は `.github/ISSUE_TEMPLATE/acd-use.yml`（AI はこのフォームで投稿しない）で、実在のプロジェクトに尋ねるのはオーナーにしかできない。 2026-11-16 から、フォームにはどの本文への表明か（いま確定している版 / 承認に出す版 / 未定）を選ぶ任意の欄が在る（PR 3449・portfolio-50）—— 承認は 1 つの本文に付くので、表明を提出の文で数えるときに、出す版への関心と分けて数えられる。**逆側**: 同じ委員会の理由書は使用を承認の基準にしていない（MIT-0・Jam・2015-10-13 の報告・register B2）—— 委員が最初にこれを訊くことは、規則と実際の問いの順の間のずれで、表明が集まらなくても規則の上では妨げにならない。表明は捏造できないことも上の段と同じである。 **同じ形の問いは 2018 年にも在った**: Bruce Perens 氏 2018-06-19（`license-review`・L0-R の審査）*"However, when I asked you to introduce me to someone who was interested in the license, no names were forthcoming. So, I have to believe this is only theoretical."*（`review-readings-2.md` §1.228・portfolio-2f）。関心を持つ人を名前で示せなければ「理論上のもの」と読まれる —— 表明の窓口（`acd-use.yml`）が集めるべきは、匿名の賛同ではなく、名前を出せる関心である。 同じ人は同じ年の 12 月に、承認を採用の代わりにする提出を名指した —— Bruce Perens 氏 2018-12-18（`license-review`・"Support for SSPL v2"）*"So, IMO the problem for some of the proposed licenses is not a lack of OSI's approval, but a lack of interest."*（`review-readings-2.md` §1.237）。採用が 1 件の ACD はこの型に読まれうる。同じ通の有利な面は *"everybody can run Open Source software for any purpose and should not have to hire a lawyer just to run it. Which seems to have a very broad buy-in."* で、ACD の §10.1 と §2.3 はまさにその形である。**逆側**: 文は事業上の利益のために SSPL を推した人たちへのもので、条件を課さない献呈に向けた言葉ではない。**逆側**: L0-R は使用に条件を課す型で、審査者が使用の実在を訊いた理由（条件が現実にどう効くか）は ACD には弱い。

**2026-11-15 に足した（2 つ目）—— 承認の記録と、出してよいものの線は別である。** 委員長の Pamela Chestek 氏 2020-03-09（`license-discuss`・"What should fit in a FOSS license?"）は、演習として本物のライセンスの文を書いて出してみようかという問いに *"License-review is a burdensome process for the OSI and the list participants, so it should be limited to real licenses, not thought experiments. License-discuss is for thought experiments."* と答えた（`review-readings-2.md` §1.233・portfolio-2f）。register が引く Fontana 氏 2015 の「思考実験のライセンスも承認した」は承認の記録で、Chestek 氏の文は `license-review` に出してよいものの線である。**ACD は実際にこのリポジトリに適用されているので本物のライセンスだが、README と LICENSE がリポジトリを「実験」と呼ぶので、審査者が「演習としての提出」と読む入口がある**（`against.md` #161 の proof-of-concept と同じ根）。提出の材料は、ACD が何に適用されていて、誰が何のために使うかを、実験の語とは別に 1 文で言う必要がある。**逆側**: 「実験」はこのリポジトリの運営の名（PM が率いる AI オーケストレーションの実験）で、ライセンスが試作品だという意味ではない。ただし審査者がその区別を自分でするとは限らない。

**2026-11-15 に足した（3 つ目）—— 承認の後も、使われなくなれば廃止が論じられる。** Josh Berkus 氏 2020-03（`license-discuss`・AAL の廃止の議論）は理由として *"the license didn't have significant use anymore"* を挙げた（`review-readings-2.md` §1.239）。承認は使用の代わりにならず、承認の後にも使用の問いは残る（上の 2026-11-11 の段と同じ線）。**逆側**: 廃止は承認済みの一覧の整理で、承認の可否の基準ではない。

**2026-11-15 に足した（5 つ目）—— 支持の無い版の見込みを、委員長が言葉にした（模擬委員会・portfolio-30）。** Pamela Chestek 氏 2020-12-28（`license-review`・当時の委員長・OIN License）*"It does not appear that anyone supports this version of the license, so the chances of it being approved appear quite slim."* 2024 年の OSPL の不承認の理由書も *"No reviewer was in favor of approving this license"* を最初に挙げた（`review-corpus.md`）。ACD は `license-discuss` で返信を得ていない。**逆側**: どちらの例も、OSD との衝突が別に指摘されていた提出である。支持が無いことだけを理由にした不承認は、まだ見つけていない。

**2026-11-15 に足した（4 つ目）—— 使われないライセンスは何のためにあるのか（`review-readings-4.md` §1.351・portfolio-50）。** 当時の license approval committee の委員長（2005-02 に第三者から OSI の新しい会長と呼ばれた）Russell Nelson 氏 2004-12-13 *"A "dead" license is one which is no longer used for any projects."*、2004-12-14 *"What purpose does a license serve if nobody uses it?"*（"pruning "dead" licenses"）。上の 2020 年の AAL の廃止の議論と同じ問いが、16 年前に、承認の委員長の言葉で在った。**逆側**: これは承認済みの一覧から外す提案の議論で、新しい提出の承認の基準ではない。採用者が 1 件の ACD にとっては、承認の後にもこの問いが残る、という読みになる。

**2026-11-15 に足した（6 つ目）—— 2003 年の委員長は、沈黙を賛否のどちらにも読まず、明示の言葉を求めた（`review-readings-3.md` §1.307）。** Russell Nelson 氏 2003-09-26 *"Maybe it's because it's obviously open source, but as committee members, I'd like to hear it explicitly from your mouths (or keyboards rather) to report back to the board."* その後の 1 通の賛成で承認を勧めた。**逆側**: 短い修正 BSD 型の提出で、委員長が自ら中身を説明していた。長く新しい形の ACD に同じ運びは期待できない（上の Chestek 氏 2020）。

**2026-11-15 に足した（7 つ目）—— 「承認されたら使う」という表明を並べた提出も、使用を制限する条件で止まった（`review-readings.md` §1.174・portfolio-2f）。** Educational Community License の提出文（2004-06-07）は *"Other universities and projects have indicated their interest in using the license if it receives OSI certification."* と書いたが、当時の委員長 Russell Nelson 氏は 2004-08-30 に *"We don't approve licenses that put restrictions on use."* と返し、止めた（承認は 2007 年）。ACD には関心の表明そのものが無い（窓口は `.github/ISSUE_TEMPLATE/acd-use.yml`）。**逆側**: 表明は承認の十分条件ではなかった、という記録でもある。ECL を止めたのは使用の制限で、ACD はそれを持たない（§10.1）。

### 🔴 2026-09-13 追記 —— 理事会は B2 に、否決ではない帰結を用意している

**議事録という一次資料を初めて読んだ**（`ACD-1.0.board-decisions.md` §2 が分析・逐語は `rounds/`）。
**License Committee が理事会に、B2 そのものを問うている**（2025-07-18）:

> *"should the LC reject a license proposal that is **valid but is not in use anywhere**?"*

**理事会の答えは、否決ではなく第 3 の状態だった。**

> *"a license should be **rejected only if it violates the OSD**. But a license could stay in a status
> where it is **not approved** if it is **duplicative and not used by a project**."*

**この register は「承認 / 否決」の 2 値で書かれてきた。** B2 の行は
「解消可能・未実施（discoverability のみ制御可）」と述べるが、**その先に何が起きるかを書いていない。**
**答えは「否決される」ではなく「**決まらないまま留め置かれる**」である。**

**2026-11-16 に足した —— 5 年前の形（`review-readings-2.md` §1.259・portfolio-2f）。** Bradley M. Kuhn 氏 2020-01-04（`license-review`・CAL Beta 4）*"I think there has to be an option (in the general case, not only for this particular license) for the OSI to say "we don't know" indefinitely and encourage the drafting authority to begin using the new license without the OSI-approved label and see what happens."* 理事会の 2025 年の答えは、これを「重複かつ未使用」の場合に限った形と読める。**逆側**: Kuhn 氏の提案は一般の選択肢で、2025 年の答えは範囲が狭い。重複に当たらないが未使用のライセンスに第 3 の状態が使われるかは、記録から分からない。

**3 つの帰結が出る。**

**(1) B2 と #84（重複）は、別々の弱点ではなく 1 つの条件の 2 項である。**
理事会の文は *"duplicative **and** not used"* と**連言**で書いている。
**B1 + B2 がリスト上で 1 文で結ばれていた（この節の主題）のと、同じ形がもう 1 組ある。**
**片方だけ答えても条件は外れない。**

**(2) 時間の読みが変わる。** §1.72 の「決定までの中央値 101 日」は**決まった場合の所要**である。
**この帰結は、決まらないことが規則上ありうると述べている。**
**したがって「沈黙が続く」ことの説明に、moderation（B14）でも無関心でもない第 4 の候補が加わる**
——**制度がそう設計されている**。⚠ **これは我々の提出について観測された事実ではない**
（`license-review` に出していない）。**候補が 1 つ増えただけで、どれが当たるかは分からない。**

**(3) 打てる手は「答える」ではなく「知っていると示す」ことだけである。**
`comparison.md` §1 は #84 に答えている（「この類型に 1 件足す費用が低い」）が、
**それは「重複」への答えであって「重複 かつ 未使用」への答えではない。**
**後者は B2 で、B2 は AI には解けない**（採用の捏造は失格事由）。
**提出文で先に名指しする以上のことはできない** ——そして**その基準は公表されていない**ので
（`board-decisions.md` §3・理事会が公表を指示してから 14 か月）、**相手の文言に合わせて書くこともできない。** **⚠ 2026-11-07 訂正: process ページには無いが、委員会はリスト上で 1 度述べている。** Tiwaz への決定（2025-09-11）は、保留を解く条件を *"one or more projects begin using this license or express an interest in doing so"* と述べ、*"planned uses"* も数えている（`board-decisions.md` §2c）。**B2 の手は採用の実績だけではなく、実在のプロジェクトの関心の表明まで広がった。** 尋ねることはオーナーにでき、AI には作れない。「使われていない」も出典より不利に書いていた —— ACD は 1 つのプロジェクト（このリポジトリ）に適用されている。足りるかは決まっていない（Piana 氏 2026-06-19）。**同日に委員会の理由書も読んだ** —— MIT-0（2020）*"this is not a basis for rejection that the OSI has applied in the past (and the OSI has historically approved newly drafted licenses not yet in use)"*、Jam（2021）*"to date, OSI has not used the number of projects adopting a license as a factor"*。**使われていないことが単独で否決の理由になった記録は、読んだ範囲に無い**（`board-decisions.md` §2d）。逆側は Chestek 氏の 2026 年の *"less inclined"* で、上の Catch-22 の節に在る。

### この節が establish しないこと

- **どちらの枝も、この節では 1 ミリも解消していない。** 記録したのは**分類の誤り**
  （B1 を待ちに置いていたこと）と、**2 つが 1 文で結ばれているという事実**である。
- **逆向きの記録（"not a blocker"）を根拠に「大丈夫だ」と読んではならない。**
  同じアーカイブに、両枝欠如を理由に Board へ非承認を求めた実例がある。
  **有利な材料と不利な材料は、同じ場所に同じ重さで置く。**

---


### 2026-09-19 —— 委員長が名指しした害は「弁護士が居ないこと」ではなかった

**リストは我々の類型に名前を付けている。** Bruce Perens 氏の定義（`license-discuss` 2025-10-01）:
*"A **\"crayon license\"** is a license obviously produced by a **non-legal-professional**, which has
obvious faults that a legal professional would know to avoid."*

**我々は前半に当たる。後半に当たるかは、実際に faults があるかで決まる。**

**そして Licensing Committee 委員長は、CAL の審査でこう書いている**（`license-review` 2019-06-27）:

> *"**The high likelihood that the license would be interpreted in significantly different ways in
> different legal jurisdictions militates against its approval.** Although the CAL is not, by any
> means, a \"crayon\" license, **it has the potential for the same negative consequence, which is
> unpredictable interpretation**."*

**害は「非弁護士が書いたこと」ではなく「法域をまたいで解釈が割れること」である。**
**「クレヨン」はその代理指標であって、害そのものではない。**

**したがって B1 は 2 層に分かれる。**

| 層 | 動かせるか |
| :-- | :-- |
| 弁護士が読んだという**事実** | **動かせない**（class 1 のまま。提出が弁護士の目を通す経路であることも変わらない）|
| **解釈のばらつき** | **動かせる。** E19 / E20 / E21 / E23 / E24 はすべてこれをやっていた ——**名前が付いていなかっただけである** |

**⚠ そして label は致命傷ではない**: **CAL はこの発言の後に承認された**／
**承認済みの Unlicense も `license-discuss` で crayon と呼ばれている**（2024-04-05）／
**Perens 氏は承認済みの SIL Open Font License を deprecate 候補に挙げている**（2022-12-13）。

**⚠ 逆側**: **ACD は構造上その害の側にある** ——§3 / §4 / §5 は法域ごとに効き方が変わることを前提に
並置され、§3.3・§12.2・§15.2 は法域ごとの分岐そのものである。**「設計として引き受けている」ことは、
委員長の懸念に対する答えにならない。** 詳細は `ACD-1.0.review-labels.md` §1.98。

### 2026-09-19（同日・後半）—— 害を 2 つに割って測った。片方は数えられ、片方は B1 そのものだった

**上の 2 層化は「解釈のばらつきは動かせる」で終わっていた。動かす前に測った。**

**害は 2 つに割れる。**

| 半分 | 測れたか | 結果 |
| :-- | :-- | :-- |
| **(i) 法域ごとに条が分岐すること** | **測れた** | 80 条中 **20 条**が法域依存。密度 **6.04/1k** で比較対象中**最重**（MIT / 0BSD は 0.00）|
| **(ii) 1 文の中の多義性** | **測れなかった** | 機械検出 3 種で **89 ヒット / 実体 3 件＝精度 約 3%** |

**(i) は数だけでは判定にならない** ——**MIT の 0 は「明晰」ではなく「沈黙」**で、条項が無効だったとき何が起きるかを述べていない。**我々の 29 は 29 箇所で述べているという意味**である。判定に効いたのは分類の方で、**4 つの分岐構造のうち 2 つだけが「どちらか判定する必要はない」と読者に述べていた非対称**（errata E26 で是正）と、**起草では閉じられない残り 1 件**（§2.8 / §5.3 / §12.4 の *"to the fullest extent the law permits"*）が出た。詳細は `ACD-1.1-SELF-AUDIT.md` §3l。

**(ii) が B1 の中身である。** **修飾語がどこに付くかは文法では決まらない。決めるのは「どちらの読みが法的に意味を変えるか」であり、それは法律家の判断**である。
**したがって B1 は「あった方がよいもの」ではなく、この半分についてはそのまま測定器の不在**である（`against.md` #163・`ACD-1.1-SELF-AUDIT.md` §3m）。

**⚠ 逆側を同じ重さで 3 つ**:

1. **測れないことは「多義性が多い」ことを意味しない。** 量は両方向に不明で、**この節を「本文は曖昧だと認めた記録」として読んではならない。**
2. **手作業が弱いのは精度ではなく再現性である。** 別の読み手なら別の 3 件が出る ——**それは §1.52 の「提出が、条文を弁護士が論評する場に置く」（#274 で狭めた言い方）と同じ方を向いている。**
3. **見つかった 3 件は直っている**（errata E27・語順のみ・全体 +1 語）。**うち 1 件は §2.2 ——この instrument の中心的な約束の文**で、末尾の限定が「撤回してはならない」にも掛かると読め、**同じ条の第 1 文 *"This Dedication is irrevocable."* と正面から食い違っていた。**

**この 2 分割が B1 の欄に対して持つ意味は 1 つ**: **「解釈のばらつきを減らす」と書くときは、どちらの半分の話かを名指しする。** (i) は我々の作業で、(ii) は提出の産物である。

**2026-11-16 に足した —— B1 を解かずに狭めた分（オーナーの依頼「ACD-1.4-DRAFT.txt の法的解釈の不確実性を 5 人で減らし続けて」・5 人の作業の要約・portfolio-30）。** 法律家の審査は依然として無い（B1 は解けていない）。代わりに、ドシエの「我々の読み」を一次の法源に当てた: 2026-11-16 の 1 日で、日・独・英・仏・米・EU の条文・判決・公開された法律家の意見と、関連する公開の文書（FSF・Debian・CC0 の FAQ）を、`2026-11-16-` で始まる 29 の写しとして `rounds/` に置き（2026-11-18 の main で `git ls-tree` で数えた・独英仏日は portfolio-30、米国と EU と弁護士の分析は portfolio-2f）、`jurisdictions.md` の「確立していないこと」の段 31 のうち 19 に、その段を狭める法源を段の中で挙げた（`measure_legal_uncertainty.py` の J出典・portfolio-9b の台帳・2026-11-17 の main）。**狭まった例**: 日本の利用権の対抗力（著作権法 63 条の 2）と英国の許諾の承継人への拘束（CDPA 90 条 4 項）は §2.8 を法が裏づける、ドイツの倒産の履行選択（InsO 103 条）は双務でない ACD に当たりにくい、英国（UCTA 1 条 3 項）と日本（消費者契約法 2 条）の免責の規制は事業でない Dedicator に当たらない、ドイツの弁護士の意見（Kreutzer 氏）は CC0 の同じ形の許諾と不行使の約束を有効と読む。**新しく見えた問い（同じ重さで）**: ドイツの無償の給付の否認（InsO 134 条・§2.9）、贈与の忘恩による撤回（BGB 530・533 条・§8.2）、消費者契約法 8 条 3 項（軽過失にのみ当たることの明示）—— 台帳では基準線の後に足された問いとして数える。**逆側**: 条文を読むことは法律家の審査ではない。写しはどれも WebFetch の片で byte の写しではなく、条文の当て方は我々の読みのままである。判例（英国の約束的禁反言・日本の不起訴の合意）は取れていない。法源で狭めた読みは、法律家に渡す問いを細くする（`QUESTIONS-FOR-COUNSEL.md` の各問いに条文を添えた）が、答えの代わりにはならない —— 委員会が B1 として問う「法律家が読んだか」には、依然として「いいえ」と答える。

## B4 —— §3 献呈と §4 許諾の並存。class 12 候補として検証し、否定した

**なぜ承認上の問題か（事実）**: Licensing Committee 委員（元委員長）が
*"Which is it, a dedication to the public domain or a license? **You can't have it both ways.**
… The document is internally contradictory."*（2025-10-16）と述べている。
ACD-1.0 の中核はまさにその並置である（§2.4 / §4.4）。CC0 の審査本体では構造が争点にならなかった（`review-precedents.md` §1.138）。

**class 12 でない理由（一次情報・2026-09-09）**

1. **彼女の批判の対象は並置ではない。** 挙げられた「留保」は 4 つ ——虚偽の著作者主張 /
   違法利用条項 / 特許訴訟による終了 / 責任否認 —— で、**ACD-1.0 に在るのは 1 つだけ**
   （§11.3 / §12.5・`objection-map.md`）。**批判の実体は「全部放棄と言いながら個別に留保する」
   ことであって、献呈と許諾を同居させることではない。**
2. **Unlicense は献呈＋列挙された許諾で承認されている**（2020）。委員会の記録は
   「**献呈単独では**承認しない」であり、ACD-1.0 は単独ではない。
   **そしてその救済論拠（献呈が無効でも列挙された許諾が働く）は Unlicense の条文に無く、
   §4.4 はそれを条文にしている。**
3. `PDDL-1.0` は *"Public Domain **Dedication & License**"* と名乗る既存 instrument である
   （**OSI 承認ではない**が、命名として前例が無いわけではない）。

**2026-11-07 追記**: OSI のサイトの記事（2017-07-28）が *"A solution would be"* として、放棄できる法域では放棄し、できない法域のために許諾を与える形を述べていた（`board-decisions.md` §2f）。決定ではなく、CC0 は今も承認されていない。 **結論: class 10（OSI 判断依存）。** 技術的に直すだけでは決まらないが、
**構造的両立不能ではない。**

**解消したときに失うもの —— そして、これが class 5 ではなく class 10 である理由（2026-09-13）**

**B4 を「構造変更（class 5）」として畳むなら、畳み方は 2 つしかなく、どちらも gap 主張を 1 本折る。**

| 畳み方 | 失うもの |
|---|---|
| **§3 を落として §4 の許諾だけにする** | **名前が指すものを失う** ——"Dedication" は献呈の法的形式であり、献呈が有効な法域で実際に**公有へ置く**のはこの条項だけである。B6（名称）とも衝突し、**「PD 等価」という類型そのものから外れる**ので #84 の土俵が変わる |
| **§4 を落として §3 の献呈だけにする** | **OSI の立場そのものに当たる** —— *"公有化の献呈は、それ単体では open source ライセンスとして承認されない"*。**Unlicense が越えられたのは献呈だけではなかったからで、§4 はその教訓を本文に書いたものである** |

**つまり並存は冗長ではなく、2 つの独立した理由で必要である** ——
**片方は名称と類型、もう片方は承認可能性。** **だから「畳めば解決する」形の問題ではない。**

**⚠ 逆側**: それでも**並存そのものが審査で問われうる**ことは変わらない（B5/E11 は、まさにその
接合部の記述精度を問うている）。**「必要だ」は「疑われない」ではない。**
**ここで述べたのは「畳む選択肢が安くない」ことであって、「並存が正しい」ことの証明ではない。**

**🔴 残る作業についての記述を訂正した（2026-09-09・#118）。** ここは当初「§11.3 / §12.5 が**留保ではなく reach の限界**であることを示す」と書いていた。**§12.5 についてこれは誤りである** —— §12.5 は実際に利益を残す条項で、`clause-reference.md` は最初からそう書いていた。**2 条のうち 1 条だけを読んで 2 条について結論した。**

正しい残作業は分類 1（提示の変更）で、内容は 2 つ ——
(a) **§11.3 は reach の限界**である（本文が明言している）。
(b) **§12.5 は残す利益であり、残るのは §12.2 の法域だけ** ——§12.1 の放棄が働く法域では放棄されている＝**どのみち渡せなかった場所でだけ残る**。

そして **比較対象を初めて置いた（`comparison.md` §1.7・SPDX の機械可読テキストで確認）** ——**BSD-3-Clause の第 3 条は受領者に課された条件**で、**Apache-2.0 §6 は reach の限界**、**どちらも OSI 承認済み**。**我々が置いているのは、承認済みの最も強い形より弱い。**ただしこれは B4 を解決しない（適合はライセンスごとに判断される）。

**2026-11-15 に足した —— 放棄が効くかで、決める側の 2 人が 2 年の間に逆を言った（`review-readings-3.md` §1.300）。** Bruce Perens 氏 1999-11-15 *"If you place on your work the notice "I place this work in the public domain", you abandon your copyright rights entirely."*、Lawrence Rosen 氏 2001-06-21（当時の事務局長）*"Nobody can "do away" with their copyright "by providing a notice that places the work in the public domain." Please don't perpetuate this myth."* と *"And suppose you later retract your abandonment? What's to prevent that?"*。§3＋§4 の並存はこの割れを前提にした形で、Rosen 氏の 3 つの問い（放棄は効くか・撤回できるか・実は許諾ではないか）には §3・§2.2・§4.4 が別々に答える。**逆側**: Rosen 氏は「普通のライセンスを使え」とも書いた —— 並存の形そのものを勧めたのではない。同じ日に Cowan 氏が「明示の放棄は他の財産権と同じようにできる」と返したが、当時は決める側ではない。 同じ型は 2015 年にも普通のものとして描かれた —— David Woolley 氏 2015-01-07 *"There is no such thing as a public domain licence. The documents are combinations of an attempt to abandon copyright, meaning you can't licence, and a, fallback, licence that attempts to give away as many rights as possible, even though you still own the copyright and moral rights."*（`review-readings-2.md` §1.243・portfolio-2f）。**逆側**: 同じ文は「放棄が効けば許諾するものが無い」という内側の緊張も指す（B5・E11 の問い）。ACD を「公有のライセンス」と紹介すると、この反論を呼ぶ。

**2026-11-15 に足した —— 権利の無い部分を含む作品には「作品全体に許諾する」か「放棄して曖昧さを除く」か、と Perens 氏が書き、Cowan 氏は 1 つの統合された文書を求めた（NOSA 2.0・2018・`review-readings-2.md` §1.225・9b が反映）。** ACD は両方を 1 つの文書に持つ（§3 の放棄と §4 の許諾）。**逆側**: Perens 氏は「または」と書いた —— 一方で足りる、という読みもでき、両方を持つ ACD は余分と見られうる（B3）。Cowan 氏の「切り離しうる 2 つの並びでなく」が §2.4 の独立を指すかは、Cowan 氏は述べていない（NOSA の文脈）。**2026-11-16 に足した —— 公有化の分野の「標準の文書」の欠けと、Unlicense の審査の基準（`gap-measurements.md` §1.148・§1.152・古い節の反映）。** Richard Fontana 氏 2011-09-07（当時 Red Hat）*"So, perhaps, OSI's main business has been certifying particular legal documents, and there simply is no standard one in the sphere that's been considered (justifiably or not) "public domain"."* ACD は名と版を持つ固定した文書（§16.4）で、この欠けに当たる。Unlicense の審査（2020）で Pamela Chestek 氏は *"I don't see how a court could misinterpret this document in any way that could be contrary to the OSD."* を基準とし、McCoy Smith 氏 2020-05-15 *"I think everyone acknowledges that a pure public domain dedication without a backstop is problematic"*、Chestek 氏同日 *"The difference with the Unlicense is that it /also/ clearly states what rights are granted."* —— ACD の §4 と §4.4 は、その後ろ盾を本文で明示する。**逆側**: Fontana 氏の文は「審査することになる」という見立てで、承認するとは述べていない。Unlicense は legacy として、広い利用と法律家の一致を経て通った。同じ日の Simon Phipps 氏は、公有は国ごとに範囲と帰結が違うので open source に当たらないと OSI は助言してきた、と書いた。

**2026-11-16 に足した —— 献呈＋許諾の形は「確か」と評された（`review-readings-2.md` §1.256・portfolio-2f・参加者の発言）。** Rick Moen 氏 2015-10-02 *"CC0 is highly permissive and legally airtight because it includes well-drafted permissive licence that applies in any jurisdiction where its primary PD dedication clauses fail to have the intended legal effect."* **逆側**: その評は、許諾が献呈の *fallback* として働く CC0 の形に向いている。ACD の §4.4 は §4 を §3 の fallback でなく独立に立たせる（*"not as a fallback for it"*）ので、評がそのまま当たるかは分からない（法律家への問い 1）。同じ通で Moen 氏は Unlicense を *"suffers fatal drafting errors"* と評したが、Unlicense は 2020 年に承認された —— 参加者の評は承認の結果と一致しないことがある。
---

§B10（gap が本当に残っているか）の本体は `ACD-OSI-BOTTLENECKS-B10.md` に在る。2026-11-15 にこの file が advisory（800 行）を越えたので、
最も大きく、いま最も足している B10 を丸ごと移した（本文は無改変）。B10 の追記はそちらへ書く。

## B15 —— 主題適格。**本文では解けない。範囲を縮めれば非コード資産を失う**（2026-09-25 新設）

**なぜ新設したか。** B1〜B14 のどれも、**「この instrument はそもそも OSI が扱う種類のものか」**
を扱っていなかった。**我々の時代でいちばん近い不承認が、まさにその理由で出ている**と
分かったので足した（`against.md` #237・一次資料は
`rounds/2023-02-license-review-mulanowl-open-works-observed-*.txt`）。

**事実。** 2023-09-15、理事会は Mulan Open Works Licenses 4 本を不承認とした。
委員会の勧告文は **OSD 違反を 1 つも挙げていない** ——
*"Resolved that it is the opinion of the OSI that the licenses, **as open culture licenses,
are not appropriate for OSI approval**."* 理由として引かれたのは、そのライセンス自身が
定義した対象の列挙 *"a written work, a musical work, a fine art work, an architecture work,
a photographic work, **an audiovisual work**, a graphic work, and a model work"* であり、
結論は *"open culture licenses are outside the purview of the Open Source Initiative."*

**ACD-1.0 §1.2 の列挙は "audiovisual material" を含む。**

**境界は委員会自身が述べている。** Chestek 氏 2023-08-10 —— *"Sometimes an OSI license will
**cross over into data or hardware when tied to software**, but not a license altogether
unrelated to software."*

**なぜ「高」であって「最高」ではないか。** Mulan の定義には**ソフトウェアが 1 語も無い**のに対し、
§1.2 は source code / object code から始まり、PREAMBLE の第 1 文は *"Software and the works that
surround it"* で、適用先はソフトウェアのリポジトリである。**上の carve-out は ACD の形を
そのまま述べている。**

**なぜ我々には解けないか（2 つ）。**

1. **本文は凍結中**なので、この増分で打てた手は「先に言う」ことだけだった
   （`submission.md` §B.0 に 94 語・`submission-reference.md` §3d に全文）。
2. **語を落としても範囲は変わらず、範囲を縮めれば非コード資産を失う。** *(2026-11-04 訂正: 旧文は *"audiovisual material"* を
   落とすと定義から外れると述べたが、列挙は例示（§15.5）で範囲は変わらない。`CLARITY-TRIAL.md` の A1 が正しい。)*
   範囲が縮むのはソフトウェアに限る案（A2）だけで、§8.4 + §8.2 の組み合わせはソフトウェアの Work について残るが、
   データセット・モデルを Work にできなくなる。**A1 は疑義を見えにくくするだけなので採らない**（`gap-measurements.md` §1.134）。
   **本文で B15 を解く手は無く、判断は OSI に残る。** **⚠ 2026-11-07: ただし基準は委員会が述べていた。** CERN-OHL の理由書（2021）*"they are written such that they can be used for software, so they are appropriate for the OSI's review"*。ソフトウェアが主な用途でなくてよいと明記している。ACD はこの基準に本文で答え、Mulan の不承認とも矛盾しない。事務局長の 2024 年の文はさらに新しい（*"non-software artifacts like datasets, documentation, and model parameters"*・§2g）。逆側（§1.2 は CERN より広い・2023 より前の文・Fontana 氏）は `board-decisions.md` §2e に在る。

**この節が establish しないこと。** *"cross over into data ... when tied to software"* が
ACD を含むというのは**我々の読みであって委員会の判断ではない**。
**危険は構造ではなく読まれ方にある** —— §1.2 を単独で読む審査者にとって、この列挙は
不承認になった定義と見分けがつかない。**その結論を、この節は防がない。**

**逆側 —— そして 2026-09-25 に、もう 1 つ実物が出た。** **OSI はフォントのライセンスを承認している**
（IPA Font License v1.0・2009・`review-precedents.md` §1.110）。主題は source code でも object code
でもなく**書体**である。同じスレッドで John Cowan 氏が理由を述べている ——
*"In the U.S., the appearance of a font is what is not copyrightable ... **A vector font, however,
is considered program code and therefore copyrightable**."*
**つまり線は「コードか否か」ではなく「プログラムとして扱えるか / ソフトウェアに結びついているか」に
引かれている** ——これは Chestek 氏の *"tied to software"* と同じ線である。
**⚠ ただし線の位置は分からないままで、§1.2 が名指しする "audiovisual material" は、
フォントより Mulan の列挙に近い語である。**

**⚠ 逆側の逆側（2026-09-27 に、同じ次元を新しい一次資料へ当て直して出た）。**
**フォントの先例は、承認する側の 1 人が名指しで否定している。** Richard Fontana 氏は
2026-09-11 の OpenMDW スレッドで、Sado 氏が SIL Open Font License を「ソフトウェアでない素材の
ために設計されたライセンスを OSI が承認した例」として挙げたのに対し、
*"I would assert that this license … was **wrongly approved** by the OSI"* と述べ、
**自分が 17 年前にその承認を後押ししたことを謝罪している**
（`rounds/2026-09-14-license-review-openmdw-thread-observed.txt` / `review-doctrine.md` §1.125 (c)）。
**承認されたという事実は残るが、先例としての重さは、承認する側がそう言っている分だけ軽い。**
**しかも同じ 1 通が、素材の種類で線を引いている** —— OSAID を引いて
*"the OSI contemplates that things other than OSI-approved licenses might be suitable for
**model parameters**, but **that does not apply to code or model architecture materials**"*。
**パラメータ側については「そもそも OSI 承認ライセンスの仕事ではないかもしれない」という読みが、
審査者の側から出ている。**

**逆側（3）—— 2026-11-03 の再検証で足した 2 つ。** (a) **汎用の承認済みライセンスが data を対象に含む** —— UPL-1.0 は *"this software, associated documentation and/or data (collectively the "Software")"* と定義する（`gap-census.md`）。**⚠ ただし *associated* はソフトウェアに付随する data で、Chestek 氏の *"tied to software"* と同じ線に乗る** —— データセットや音声映像の単体には届かない。(b) **Fontana 氏は 2026-04-06 に、オープンソースのライセンスは *"extensively used for non-software material in open source project repositories"* で *"completely appropriate"* だと述べている**（`against.md` #211・gap 3 の文脈で記録済み）。**⚠ 個人の見解で委員会の立場ではなく、同じ人が OFL を *"wrongly approved"* と述べている**（上）—— 2 つを並べると、彼の線は「リポジトリの中でソフトウェアと一緒に在る素材」に引かれている。**どちらも §1.2 の列挙が単独で読まれる危険（上）を消さない。**

**2026-11-03 再検証の結論（B15）**: 対象の広さそのものは、OSD 1〜10 のどの条にも抵触する作用を持たない（25 が条ごとに当てた。§16 の名称の制約は文書についてのもので OSD 4 も名称の変更要求を許す / §11.4 の個人情報・肖像は法の制約でライセンスの条件ではない）。1.4 で §1.3 にパラメータを足したことは `ACD-1.4-CHANGELIST.md` の §1.3 行が逆側つきで記録している。**残余は OSI の主題判断（purview）だけで、新規欠陥なし。** **2026-11-04 追記**: 上の「1.4 で §1.3 にパラメータを足したこと」は、§9.1 の同じ形の例示とあわせて 1.4 草案から戻した（A1′+・`ACD-1.4-CLARITY-TRIAL.md` §7）。OSI の主題の判断は本文が名指す対象を読んでいた（Mulan の理由書は定義文を引用した）ので価値は信号の側にあり、**範囲・B10 は変わらず、B15 の実質（定義が software-specific でない・*audiovisual*）は 1.0 から残る**。

**逆側（2）。** 有利な読みも 1 つある —— **不承認の理由が OSD 違反ではなかった**ということは、
**主題が近いと判定されれば OSD 側の審査に進む**ということでもある（同じ記録で、
理事会は否決を *"only if it violates the OSD"* に狭めている・§B2 節）。
**ただしそれは「否決されにくい」であって「承認される」ではない** ——
**"not approved" のまま留め置かれる第 3 の帰結**がこの instrument にも開いている。

**2026-11-15 に足した —— 範囲の論点の最も古い記録（`review-readings-3.md` §1.305）。** Russell Nelson 氏 2001-09 *"OSI certifies software, not documentation, as open source. There are various documentation licenses out there. We're not decided on whether we want to certify documentation."* と、Lawrence Rosen 氏 2001-09-26 *"OSI *certifies* software. OSI *approves* licenses. This is a legally significant distinction."*。ライセンスを承認しソフトウェアを認証する、という区別は、上の CERN-OHL の理由書（2021）の「ソフトウェアに使えるように書かれている」と同じ線の 20 年前の形である。**逆側**: 2001 年は「決めていない」で、受け入れるとは書いていない。同じ会話で Nelson 氏は、ソースから機械的に作られた物には別の定義が要るかもしれないと書いた（モデルに近い問い）。

**2026-11-15 に足した —— 委員会は、範囲の広いライセンスを「ソフトウェアだけのライセンス」として通読して確かめる（模擬委員会・portfolio-30）。** Pamela Chestek 氏 2023-08-15（`license-review`・法律事務所の署名）*"IIRC, the CERN OHLs were written specifically with software in mind, so that one license could be applied to the combination product of hardware and software."*、*"On my review, I walked through it as only a software license to make sure it didn't have any unintended consequences when applied that way."* 同氏は 2024-10-05（`license-discuss` の事前の議論・本人が *"in my personal capacity"* と署名）にも *"The licenses include "services," but open source licenses are for software, not for services. There also appear to be other areas covered that are inappropriate for a software-only license, such as personal information."* と書いた。**同じ通読を 1.4 草案に当てた（2026-11-15）。** ソフトウェアだけに当てると、§6（計算的利用）はコードを学習に使う場面で働き、§7（データベース権）は多くの場合に空振りし、どちらも受け手に何も課さない。§8.4 の「Work が教える機能」の非対称（文書だけを読んで人が実装した場合と、モデルに書かせた場合で特許の許諾の及び方が違う）は `gap-measurements.md` の表と `faq.md` A32 が扱い済みである。§1.5 と §11.4 は、データ保護・プライバシー・人格権・個人データに名前で触れるが、どれも「及ばない」と述べる限界の文である。**逆側**: 同氏が 2024 年に「ソフトウェアだけのライセンスにふさわしくない」とした「個人情報」の語は、限界の文としてであれ ACD の本文に在る。限界の文が、範囲の広さの印として読まれる危険は残る。この通読は我々自身のもので、委員会の通読ではない。

**2026-11-15 に足した —— 我々が配っている Agent Skills も、この範囲の問いの中に在る（`reviewer-positions.md` §1.55・古い節の反映を表に揃える作業で見つけた）。** Richard Fontana 氏 2026-04-06（`license-discuss`）は、AI 支援への指示の集まりについて *"Instructions" can be copyrightable works.* と書いた（reviewer-positions §1.55 の引用）。このリポジトリは ACD をソース・文書・データ・メディア・`.well-known/` の Agent Skills の全体に当てている。§2.7 が許諾の範囲を Dedicator が持つ権利に閉じているので、スキルが著作物でなくても許諾は害にならない。**逆側**: ソフトウェアでない物に当てている実例が、提出者自身のリポジトリだということは、B15 の問い（ソフトウェアのライセンスか）を審査者に最初に見せる。

**2026-11-15 に足した —— ソフトウェアとデータと文書を 1 つの道具で覆う需要は、CC0 の審査で利用者の側から述べられた（`review-readings.md` §1.169・portfolio-2f）。** Carl Boettiger 氏 2012-02-22 *"There are often not sharp divisions between software, code snippets and scripts, documentation, data files, figures, etc in scientific work"*、Kuno Woudt 氏 2012-02-24 *"Most free software, open source and free culture licenses do not consider database rights."* ACD の §1.3 の列挙と §7 は同じ需要に当たる。**逆側**: どちらも個人の発言で、CC0 は承認されずに取り下げられた —— この需要は承認の帰結を変えなかった。

**2026-11-16 に足した —— 採られなかった読み: ソフトウェアにも同じく使えるなら承認しない理由は無い（`review-readings-2.md` §1.257・portfolio-2f）。** McCoy Smith 氏 2023-08-15（`license-review`・Mulan Open Works License）*"absent that I see no reason why it shouldn't be approved if it could be used with software equally with content."* ACD の §1.3 はソースとデータと文書を同じ Work として扱い、どれにも同じ条で使えるので、この読みにそのまま当たる。**逆側（重い）**: 1 か月後に理事会はその Mulan のライセンスを *"as open culture licenses"* を理由に不承認とした（against #237）—— この読みは決める側に採られなかった。同じ会話で Josh Berkus 氏 2023-08-11 *"I'm not ready to take on OSI developing a process and criteria for approving content licenses this year"* —— 内容を覆うライセンスの基準は、その時点で無かった。Smith 氏の 2023 年の役はドシエの名簿の一次資料に無いので、名前だけで書く。

**2026-11-16 に足した —— AI の領域には一般化に使える実践が無い（事務局長 2024）と、非ソフトウェアの文書を別に並べる案（`review-readings-2.md` §1.260・portfolio-2f）。** Stefano Maffulli 氏（事務局長）2024-09-12（`license-review`・"Adapting the license-review process to AI"）*"the OSD looks easy to interpret today only because it's 26 years old. Also, when it came out there were hundreds of software packages already using its principles."*、同じ通で AI には一般化に使える例が無いと続ける。同じ会話で Josh Berkus 氏 2024-09-09 *"Finally, I think we'll want to list approved documents which are not software licenses separately on the website from the software licenses."* **ACD への当たり方**: §6 と §8.4 のモデルと出力への伸びは、審査者が比べる先例の無い所に在る —— B10 の新しさの根拠にもなり、比べる物差しが無いという不利にもなる。Berkus 氏の案の下では、ソフトウェアとそれ以外を 1 つの本文で覆う ACD がどちらの一覧に入るかが問われうる。**逆側**: Maffulli 氏の通は OSAID の文脈で、ライセンスの審査の基準を述べたものではない。Berkus 氏の案は案のままで、採られた記録は見ていない。
