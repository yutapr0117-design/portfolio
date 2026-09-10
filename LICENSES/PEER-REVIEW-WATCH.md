---
file: LICENSES/PEER-REVIEW-WATCH.md
audience: 次のセッションの実装者（一次読者）
last-updated: 2026-09-04
canonical-ref: LICENSES/ACD-1.0.comparison.md §1.5 (比較の本体) / LICENSES/ACD-1.0.against.md #28-#31 (不利な材料) / LICENSES/REVISION-PROTOCOL.md (改訂サイクル)
---

# 同時代 instrument の経過観察（OpenMDW / ModelGo）

> **我々の発信は 2026-09-09 から停止している**（本書が観測している OpenMDW / ModelGo の話ではない）。 OSI Moderators が両リストへ「AI が全部または大半を書いたと疑われる投稿は拒否する」と投稿したため（`ACD-1.0.against.md` #119 / `ACD-OSI-BOTTLENECKS.md` **B14**・逐語は `rounds/`）。**単一ソースは `FROZEN.md` の `POSTING-STATUS` marker**で、**Check 467 が 4 面と両方向で照合する。**


**方針（2026-09-04 オーナー）**: OpenMDW と ModelGo も長期戦になるので、**日数を空けながら
経過を見て**、議論・改訂・レビュー結果から ACD に役立つものがあれば自然に取り込む。
頻度とやり方は委任。

**この文書の目的は「毎回ゼロから読み直さない」こと。** 下のベースラインは 2026-09-04 に
**実際に観測した内容**であり、次に見るときは**差分だけ**を扱えばよい。ベースラインが無いと、
観測のたびに全部を再構成することになり、しかも「何が新しいのか」を判定できない。

**位置づけ（2026-09-04 オーナー）**: 共有された 2 件は「**現在、申請とレビューを繰り返して
いる唯一の AI ライセンス**」である。つまりこれは「似た instrument をいくつか眺める」話ではなく、
**同じ土俵で同じことを反復している 2 件を、こちらも反復しながら見る**という関係にあたる。

## 0.5 なぜ「向こうの成功」がこちらの利益になるのか

**AI ライセンスは OSI 承認の前例がゼロである**（承認済みリストを 2026-09-04 に確認。
モデル・重み・データセットに特化した承認済みライセンスは 1 件も無い）。したがって審査者は
**この種の instrument を通した経験を持たないまま**読むことになり、その負担は分野の全員に
等しくかかる。

**どちらかが承認されれば、その壁は全員から消える。** ACD-1.0 が OpenMDW や ModelGo と
競合しないのはもちろん（軸が違う。§1.5）、**競合していたとしても、先に 1 件通ることは
こちらの利益になる**。前例のあるカテゴリと、前例の無いカテゴリでは、審査の難度が違うからである。

**オーナーは両者のレビューに実際に参加している**（2026-09-04 時点。反復を早める意図での
参加）。これは記録しておくべき事実で、ACD の提出者が**自分の提出を待つだけでなく、同じ
分野の他の提出を読んで意見を返している**という関係にあたる。

**ただし「競合しない」は proliferation の答えにはならない。** 目的が違うことと、
「この生態系にもう 1 つ instrument が要るか」は別の問いである。前者は §1.5 が示すとおり
違う。後者は list の判断で、`against.md` #28 と #33 が扱う。**ここを混ぜると、答えたつもりで
答えていないことになる。**

## 0.6 オーナー自身が両方のレビューに参加している（2026-09・実物を確認）

**この観測はここでは二次情報ではない。** オーナーは Yuta Yokoi / 横井雄太として
license-review に実際に投稿しており、その投稿と返信をアーカイブで直接読んだ（2026-09 分・
4 通）。**「読んで還元する」対象に、こちら側の投稿とその応答が含まれる**という関係にある。

| 投稿 | 何を問うたか | 何が返ってきたか |
|---|---|---|
| OpenMDW (006239) | 許諾は著作権・特許・営業秘密・DB 権に及ぶのに、**終了トリガーは特許と著作権の主張だけ**。DB 権侵害の主張では許諾が残るのか、営業秘密でも残るのか、**その境界を説明する原理は何か** | 提出者が境界を確認（著作権・特許のみが終了を引き起こす） |
| ModelGo (006241) | 「Distribution」は**ホスト型・API 提供を明示的に含む**のに、§2.2(a) の帰属条件は通知を頒布と**共に**提供せよと書く。出力しか届かない形態で**何をすれば遵守になるのか** | 提出者が「**定義上の頒布に当たる**」ことを認めたうえで「**義務は生じない** —— ライセンスを添付すべき Licensed Material が存在しないから」と回答。出力への通知要件の追加は**オープンソース原則と相容れない**として明確に拒否し、将来は「利用の条件としてではなく、帰属を満たす方法として」書くと述べた |
| OpenMDW (006246) | 議論を**閾値の問題**へ絞り込む —— 「主張された権利に対応する許諾だけを終了させる最小版」を仮に置き、**それでもオープンソース原則に反するか**を問う。反するなら著作権訴訟トリガー自体が問題で、反しないなら問題は §5 の 3 つの広さ（**全権利を終了させる / 第三者に及ぶ / 本案判断の前に終了する**）にある | 議論が継続中 |
| ModelGo (2026-09-05) | Duan 氏の回答を受けて読みを確定させ、閉じた | Ruby Anna 氏（ModelGo 側）が "**Your understanding is 100% correct**" / "thank you for the clear and thorough analysis" と確認 |

**返信だけを数えると関与を 1 つ落とす。** Shuji Sado 氏は我々宛ではなく list 宛の分析の中で、
我々の質問を明示的に引いて議論を進めている ——
*"Yokoi-san's question and Mike's answer help here as well."*（2026-09-04）。
**引用は、返信とも名指しの応答とも別の経路**であり、`In-Reply-To` を追う検出でも宛先照合でも
拾えない。同氏は AI-MIT / AIAL-1.0 に反対した 3 名の 1 人で、その反対理由は
`comparison.md` §1.45 が ACD-1.0 に構造上あたらないと分析している当の人物である。

**一次資料は `rounds/` にある**（2026-09-06 に公開アーカイブから逐語で複製・8 file）。
それまで本節は分析だけを持っており、**依拠する原文はリポジトリに存在しなかった**（`against.md` #92）。

**配送の形についての観測**: steward が `license-review` へ送った 3 通は、いずれも
`In-Reply-To` も `References` も持たない —— 件名だけを引き継いだプロトコル上の新規スレッドと
して配送されている。同じスレッドの他者のメッセージは完全な References 鎖を持つので、
アーカイブの性質ではない（`against.md` #90）。**鏡像も測ってある**: 返信が付かなかった 1 通は
確かにこの形だが、**同じ形の 2 通は回答を得ている**ので decisive ではない。

**ACD へ還元した判断軸**（条項ではなく原理を持ち込む・`comparison.md` の方針どおり）:

1. **許諾する集合と、反応する集合が違うなら、その差を説明できなければならない。**
   → ACD は §10.4 / §8.2 により**反応する集合を持たない**ので、この問いが構造的に生じない。
   代償は防御的終了の不在（against.md #16 / #46）。
2. **条件は、そのライセンスが定義するすべての頒布形態で満たしうるものでなければならない。**
   満たしようがない形態があると、**条件は配送手段によって効いたり効かなかったりする規則**に
   なる。AI では hosted inference が主流なので、この分岐は周縁ではなく中心。
   → ACD は §10.1 / §4.3 が条件を持たず、§10.5 / §16.6 が §16 の条件を**文書としての本文**に
   限定するので生じない（against.md #47）。
3. **論点は「全体として妥当か」ではなく「どこで境界を越えるか」に絞ると前へ進む。**
   最小版を仮に置いて閾値を探す進め方は、ACD が自分の条項を弁護するときにも使える ——
   「§X は妥当か」ではなく「§X のどの要素が問題で、それを外した最小版なら通るのか」。

## 1. いつ見るか

- **数日〜2 週間ほど間を空けて**。毎日見る種類の対象ではない（審査は月単位で動く）。
- **ACD が何かを提出する直前は必ず**。向こうの結果は ACD の位置づけ（proliferation の
  答え方・先例の使い方）を直接動かすため。
- **どちらかが承認・却下・改訂された報が入ったとき**は、間隔に関わらず。

## 2. 何を見るか

| 対象 | 場所 | 変化したら効くもの |
|---|---|---|
| OpenMDW 本文 | `github.com/OpenMDW/OpenMDW` の `1.x/LICENSE.OpenMDW-*` | 版が上がれば条項が動く。とくに notice 条件・特許報復・trade secret の扱い |
| ModelGo 本文 | `github.com/Xtra-Computing/ModelGo` の `MGL/V2/*/LICENSE` | distillation 除外の扱い・trademark/publicity 条項 |
| OSI Discuss | `discuss.opensource.org` の OpenMDW スレッド / AI ライセンス比較スレッド | reviewer の論点。**ACD へ最も還元しやすい層** |
| license-review アーカイブ | `lists.opensource.org/pipermail/license-review_*` | 正式審査での指摘と提出者の応答 |
| **既存大型ライセンスの steward** | fsf.org / apache.org / creativecommons.org | **ライセンス本文**の改訂（GPLv4・Apache の改訂・CC0 の再提出）。announce されれば `comparison.md` §1.3 は**書き直す** —— あの節は「彼らは本文を変えていない」という**反証可能な観測**の上に立っており、変わったら弁護せず書き換える |

## 3. ベースライン（2026-09-04 観測）

### OpenMDW-1.1（Linux Foundation 起草）

- 対象 = **Model Materials**:「1 つ以上の機械学習モデル（アーキテクチャとパラメータを含む）
  および全ての関連 artifacts（付随するデータ・文書・ソフトウェアを含む）」。
- 許諾 = 「Model Materials を制限なく扱う」ことを、**著作権・特許・データベース権・
  営業秘密**の各権利の下で。
- 条件 = **本契約書の写しと、原出所表示・著作権表示の保持**（＝通知条件がある）。
- 特許報復 = 侵害主張の訴訟を提起・維持・自発的に参加すると**権利が終了**（先行提訴への
  応答は除く）。
- 出力 = 「Model Materials を使って生成された出力の使用・改変・共有について、制限も義務も
  課さない」。
- 利用者側 = 第三者権利のクリアランスと due diligence は受領者が行う。

### ModelGo v2（シンガポール国立大学）

- **MG0-2.0**: 対象 = Model + Complementary Materials。**事前学習データセットは対象外**。
  Derivative Materials から **distillation・合成データ生成由来のモデルを明示的に除外**。
  許諾は著作権・特許・データベース権ほか。条件は **Licensor への言及・商標の宣伝利用に
  事前の書面同意**。帰属条件は無い。
- **MG-BY-2.0**: MG0 に加え、頒布時に **①本 License の写しを添付 ②Derivative には改変した旨と
  改変日を目立つ形で表示 ③既存の著作権・帰属・著者表示を保持**。出力にはこれらは及ばない。
  **特許訴訟の提起で即時終了**。

### OSI 側の議論（観測時点）

- OpenMDW スレッドで挙がった論点: **営業秘密を許諾対象に含める法的意味**／**特許条項が
  間接侵害まで及ぶ副作用**／**due diligence を利用者へ押し付ける条項**／**データライセンス
  としては Creative Commons に劣る**／**openwashing を助長しうる**。
- 手続き上の観察:「**OSI コミュニティは著作権を超えた知的財産権について蓄積した議論が
  乏しい**」。
- 評価枠組みとして **OSAID（Open Source AI Definition）** が参照されるが、OSAID に基づく
  体系的な比較は**ほとんど公開されていない**。

### ベースラインの不確かさ（2026-09-04 に一部解消）

観測した OSI Discuss の投稿には「**まだ OSI のライセンス承認プロセスには提出されていない**」
という記述があった。**オーナーの説明（2026-09-04）で解消した** —— 共有された 2 件は
「**現在、申請とレビューを繰り返している唯一の AI ライセンス**」であり、オーナー自身が
メーリングリストで経過を追っている。つまり**あの投稿は提出前の時点のもの**と読むのが自然で、
現在は審査の反復に入っている。

**ModelGo の経過（2026-09-04 に公開スレッドで確認・オーナーの「formal review の反復段階」と一致）**:

| 時期 | 出来事 |
|---|---|
| 2025-02 | MG0-2.0 を license-review へ提出（提出者 Moming Duan・NUS） |
| 2025-12 | **3 回目の再提出** |
| 2026-01-27 / 05-26 / 07-26 | 提出者からフォローアップ（3 回）|
| 2026-09 時点 | **いずれにも返信なし。** 提出者自身が「審査は静かな状態が続いている」と書いている |

**つまり約 19 か月・3 回の再提出を経て、直近 8 か月は沈黙している。** 提出者は「モデル
ライセンスのような新しいものは審査に時間がかかると理解している」とも述べており、
**これは異常事態ではなく、この分野の審査の実際の速度である**と読むのが妥当。

**OpenMDW の経過（2026-09-04・オーナーがメーリングリストで観測）**:

| 項目 | 観測 |
|---|---|
| 段階 | **まだ初回の正式申請**（再提出に至っていない）|
| 2026-08 のスレッド | **約 48 通**（初回申請 1 通＋以後 47 通）、参加者は提出者を含め **約 12 名** —— **2026-09-10 15:25 JST に測り直すと 2026-08 だけで 86 通**、2026-09 が 19 通で**2 か月計 105 通・参加者 20 名**。**この行の数字は 2026-09-04 の観測値で、スレッドはその後も伸びている。引用する前に測り直すこと** |
| 内容 | 厳しい指摘だけでなく、**提出者の説明で懸念が解消されたという趣旨の評価も出ている** |

**この 2 例は同じ方向を指していない。** ModelGo は 19 か月・3 回の再提出・8 か月の沈黙、
OpenMDW は初回申請のまま 1 か月で 48 通の実質的な議論。**片方だけを見て期間を一般化しない。**
ACD がどちらのパターンになるかは、いまの材料では決まらない。

### OpenMDW スレッドから読み取れた論点（2026-09-04・アーカイブを直接確認）

スレッドは **2026-08-13 開始・当月のアーカイブ 102 通のうち 86 通**を占め（**2026-09-10 にヘッダの折り返しを解いて数え直した値。折り返しを解かない最初の集計は 85 と出た** ——**pipermail の Subject は継続行へ折り返されうるので、数える前に unfold する**）、
Richard Fontana / Pamela Chestek / Luis Villa / McCoy Smith / Rob Landley / Stefano Maffulli /
Carlo Piana ら**審査の中心にいる参加者が多数**関与している。提出者は Mike Dolan（Linux
Foundation・SVP Legal & Strategic Programs）。

**提出文の作り（ACD が持たないものが明確に分かる）**:

| 要素 | OpenMDW | ACD-1.0 |
|---|---|---|
| gap の述べ方 | 「既存の承認済みライセンスは**主にソフトウェア向けに起草されている**」+ 実際の困りごと（MOF 採用者が「どのライセンス文をどの部分に入れるか分かりにくい」と報告） | 3 つの問い（ML/TDM・特許・著作者性）で述べる |
| 比較対象 | **MIT と Apache-2.0 の 2 つに絞り、共通点と差分を逐条で**述べる | MIT-0 / 0BSD / Unlicense / CC0 / Apache-2.0（§1 で 5 つ） |
| 法的レビュー | **弁護士起草**。1.0 は LF と PyTorch Foundation の協働、1.1 は企業法務のフィードバックによる小改訂 | **無し**（#1） |
| 採用実績 | **8 組織以上**（NVIDIA が 19 モデル、ByteDance、IBM ほか） | **1 件**（#4） |
| 提出範囲 | 1.1 のみを審査対象とし、1.0 も必要なら含めると申し出る | 1.0 のみ |

**議論で出ている論点**:

1. **管轄そのもの** —— 「**OSI が非ソフトウェア（データ・モデル）のライセンスを審査すべきか**」。
   これが繰り返し現れる。**ACD はより正面から当たる** —— OpenMDW の対象は Model Materials
   だが、ACD は「any Work」で、データ・メタデータ・視聴覚素材を定義に明示している（§1.2）。
2. **proliferation** —— Fontana / McCoy Smith が長いやり取り。承認が不要な増殖を招かないか。
3. **OSD 適合** —— Chestek が実質的な寄与を複数回。
4. **通知・帰属条件の負担** —— 保持義務がコンプライアンス負担と目的の釣り合いを保つか。
5. **議論の量そのもの** —— Villa が「list の作法（量について）の注意喚起」を投稿するほど。

**最も重い 1 件（Maffulli, 006166）**: 「**この難問は open source AI definition 論争の中心に
あり、ライセンスでは解決できず、政策レベルで解くべきだ**」「（OpenMDW の）審査が政策論に
**足を取られるべきではない**」。透明なモデルは、公開ライセンスされた学習データが足りないか、
データセットを開示すると訴訟に晒されるかのどちらかになる、という緊張を指摘し、
「**米国のフェアユースや EU の TDM 例外とどう折り合いをつけるのか**」と問うている。

**ACD への還元**: ACD の §6 は TDM を正面から扱い、§6.2 で**留保をしないと明言**する。
これは「政策の問題」に見える領域へ、ライセンスの側から踏み込む条項である。したがって
ACD は **Maffulli の警告の両側に触れる** —— 政策論を持ち込んだと見られる危険と、
政策論に足を取られる危険の両方。**審査の場では、§6 が政策的主張ではなく
「Dedicator 自身の権利についての言明」であることを示せなければならない**
（本文は既にそう限定している —— §6.2 は「Dedicator の Covered Rights と特許クレームに
関する限り」と書き、§2.7 と §6.3 が他者の権利には及ばないことを述べる）。

**残る不確かさ**: ModelGo の各再提出で何がどう変わったか、OpenMDW の各論点が最終的にどう
決着するかは未確認。次に見るときは **license-review アーカイブで改訂の差分と未解決の論点**を
確かめること。**ラウンドの区切りを推測で書かない。**

### 2026-09-05 に届いた観測（オーナー経由・両レビューに参加している側からの一次情報）

**渡され方**: 材料と「何かありそう」という観測だけ。場所も答えも指定されなかった。**その形が
結果を決めた**ので、次に来たときも同じ形で受ける（`BLIND-SPOTS.md`「外から来た材料は、事実では
なく測り方として受け取る」）。

**ModelGo —— hosted-only 配信で義務は発火するか**

- hosted / API / web access は**定義上 Distribution に含まれる**。一方、remote user が Output
  だけを受け取り Licensed Materials / Derivative Materials を受け取らない hosted-only の場合、
  §2.2(a) の license-copy / notice obligations は**生じない** —— 提出者からの明示的な解釈。
- さらにその結果は単なる drafting gap ではなく、**2025-03 に Output への notice requirement が
  「mere use への条件になり得る」という議論を経て削除された経緯と整合する**、という説明も得られている。

**ACD への還元（論点であって条項ではない）**: `against.md` #47 は既にこの構造を記録していたが、
そこでは「提出者の解釈で救われた」と書いた。**新しいのは、この軸が審査の側で実際に一度 drafting
を動かした証跡があること**。つまり「**義務が mere use に掛かっていないか**」は我々が構成した理論
ではなく、レビューが実際に強制する軸である。ACD は §10.1 / §4.3 が Work に関して条件を課さないと
述べるため、配信経路がどうであれ発火する義務が無い —— *解釈を要さずテキストが答える*点が差だが、
同じ構造が #41（弱い disclaimer）と #46（防御的終了の不在）を生んでいることも同時に真である。

**OpenMDW —— litigation termination はどこで越えるのか**

最小の hypothetical を置いて境界を分解する問いが投げられている:

1. **copyright litigation trigger そのもの**が駄目なのか
2. trigger 自体は許容されても、**all grants termination** が広すぎるのか
3. **"any person or entity"** まで対象にすることが広すぎるのか
4. **merits determination 前**に filing / maintaining だけで termination することが問題なのか

**ACD への還元**: ACD は 1〜4 の**どれにも当たらない**。§10.4 が「for any reason」終了しないと
述べ、§8.2 が patent retaliation の不在を "deliberate" と明言するため、境界の手前にいるのではなく
**軸の外**にいる。`against.md` #46 の「ACD はこれを問われ得ない」は、この分解に照らして正しい。
ただし無償ではなく、対価（**訴えた相手も全権利を保持する**）は #46 が記録したとおり。

**手順として持ち帰ったもの**: 分解の型そのものを `REVISION-PROTOCOL.md` §1.5 へ。指摘が
「この条項は open source ではない」の形で来たときに、認める / 反論する の前に置く工程になる。

### 単独提出者は無視されない —— 12 スレッドの実測（2023〜2026・`license-review`）

**我々の状況は「単独・非弁護士・無名・採用ゼロ」である。** その状況の提出が実際にどう扱われるかを、
**個別に読むのではなく類型として測った**（2026-09-08・`license-review` 2023-01〜2026-09）。

| 提出 | 初回 | メッセージ数 | 応答した人数 | 初回応答まで |
|---|---|---|---|---|
| MAPOD4D | 2023-01 | 7 | 6 | 59.6 h |
| Open Source Protection License | 2024-06 | 6 | 4 | **270.7 h** |
| Accountable Resolver | 2024-10 | 6 | 4 | 22.3 h |
| Orivex Syscall Note | 2025-10 | 14 | 6 | 24.2 h |
| CingXaero | 2025-12 | 9 | 6 | 31.1 h |
| Misty Foundation | 2025-12 | 8 | 3 | 106.6 h |
| BarrerSoftware | 2025-12 | 9 | 6 | **3.7 h** |
| Project Tick | 2026-01 | 21 | 5 | 68.5 h |
| FARCL | 2026-02 | 8 | 3 | 8.1 h |
| CompanioNation | 2026-04 | 4 | 2 | 13.7 h |
| Milenium | 2026-05 | 7 | 4 | 44.1 h |
| Linkumori | 2026-06 | 9 | 4 | 21.7 h |

**応答者数の中央値 4 人・初回応答までの中央値 27.7 時間・最長 270.7 時間（約 11.3 日）。
応答ゼロのスレッドは 12 件中 0 件。**

**読み方（両面）**:
- **有利**: `license-review` は**無名の単独提出者を無視しない**。「小さい提出は相手にされない」
  という懸念は、この 4 年の記録では支持されない。
- **不利**: したがって**我々の沈黙は「リストが静かだから」では説明できない**（#83 / #96 が
  別の方法で出した結論と一致し、今回は 12 件で定量化された）。
- **ただし直接比較にはならない**: 我々の 1 通は **`license-discuss`** に出ており、上の 12 件は
  すべて **`license-review`** である。**リストが違えば読者も作法も違う**（McCoy 氏
  2026-08-04「`license-discuss` は承認の窓口ではない」）。**この差を無視して「無視された」と
  読むのは、venue の取り違えを 2 度目にやることになる。**

**最長の 270.7 時間（約 11.3 日）は、我々の沈黙（13 日・2026-09-08 時点）より短い。**
`license-review` 上では観測された全 12 件を超える長さだが、**`license-discuss` にはこの
ベースラインが無い**ので、そこから何かを結論しない。

### FFOL（2024-10・5 通）—— #97 で直した当の項目が、名指しで欠落を指摘されている

Forever Free & Open License。McCoy Smith 氏の返信（2024-10-13）が、**OSI の要求項目のうち
欠けているものを箇条書きで名指しした**:

> The process for license approval has a couple of other requirements, which it doesn't look like
> you've done completely here … It looks like you haven't done the following:
> * **Affirmatively state that the license complies with the Open Source Definition, including
>   specifically affirming it meets OSD 3, 5, 6 and 9.**
> * Identify what projects are already using the license.
> * Describe any legal review the license has been through, including whether it was drafted by a lawyer.

**1 つ目は、2026-09-07 に我々が §B.0 で欠いていたと分かった当の項目である**（`against.md` #97）。
**「specifically affirming it meets OSD 3, 5, 6 and 9」は、審査者が名指しで確認する項目だ**という
直接の証拠であり、**直していなければこの返信を受けていた**。

これで**要求情報の欠落に対する反応は 3 例**になった —— McCoy 氏（2024-10・FFOL / 2026-03・
Modified 0BSD）と Piana 氏（2026-09・BOS）。**2 名・3 回・2 年にわたって同じ形である。**

**本題（我々には当たらない）**: FFOL は対価の徴収を禁じようとしており、Piana 氏が
*"The inability to charge a price for accessing the program is **directly against OSD #6**"*、
そして **許諾そのものに対価や制限を課してはならない**（ソフトウェアを売ること自体は妨げられない）
と整理している。ACD-1.0 は §4.3 / §10.1 により対価も制限も持たない。

### Tiwaz License v1.0（2025-05 / 07・16 通）—— 手続きの観測 3 件（2026-09-08 読了）

MPL-2.0 から Secondary License 条項を除いた派生。ACD-1.0 とは類型が違うが、**審査者の作法**が
3 つ観測できた。

**1. 法的レビューは要件ではない —— 3 例目、しかも OSI 理事から。**
Josh Berkus 氏（**OSI Board Member** として署名・2025-05-27）:
> where the opinions on these flaws in the MPL, and the revisions to them, drafted by an attorney
> or with the help of one? **It's not a requirement, but lets us know how to regard the text of the
> changes.**

Chestek 氏（委員長・2024-12）と Piana 氏の撤回に続く**独立した 3 例目**であり、
**最も有用な言い回し**でもある —— *"lets us know **how to regard** the text"*。
**要件ではないが、テキストの読まれ方を変える。** 我々のドシエはこの温度で書くのが正しい
（「blocker ではない」を「軽い」と読ませない）。

**2. 審査者は提出者の URL を叩き、死んでいれば言う。**
同じメッセージ: *"Note that the **tiwaz.fyi domain appears to be non-functional right now**."*
→ 我々は 2026-09-07 に `LICENSES/**` の全 URL 30 件を実測し、**29/29 が 200**（残る 1 件は
XML 名前空間 URI で link ではない）。`AS-OF.md`。**この掃引は儀式ではなかった。**

**3. McCoy 氏の既定の審査方法は「既存ライセンスとの redline」であり、我々には使えない。**
McCoy 氏（2025-05-28）: *"i did a compare of this license vs mpl-2.0 and posted it to github.
**i find this an easier way of reviewing licenses that are derived from a preexisting license**"*
—— 2026-09-07 の ModelGo 意見募集でも同じことをしている（**3 例目**）。
**ACD-1.0 は既存ライセンスの派生ではないので redline が原理的に作れない。**
黙っていると「比較材料を出さない提出」に見えるので、**作れない理由（祖先テキストが無い）を
先に述べ、代わりに条項単位の比較（`comparison.md`）を出す**のが正しい（MGB の節と同じ結論）。

**おまけ（実際に効いた）**: McCoy 氏は同スレッドで、MPL-2.0 が免責と責任制限を**黄色で強調**して
いるのは米国 UCC の「conspicuous」要件のためで、ASCII 版では ALL CAPS やアスタリスク列で
代替されると述べている。**ACD-1.0 の §13.1 / §13.2 / §14.1 は既に ALL CAPS である**
（`submission-reference.md` §4c に実測として追加）。

### 進行中の CALL FOR COMMENTS —— 4 つの問いが、すべて ACD には当たらない（2026-09-07〜08）

McCoy Smith 氏が ModelGo 2 件について**公開の意見募集**を出した。宛先は
*"those interested in either: a) **approval of AI-directed licenses**; or b) approval of licenses
in general"*。**いま AI 向けライセンスに何が問われているかの、最新かつ最も権威的な一覧である。**

| McCoy 氏の問い | ACD-1.0 に当たるか |
|---|---|
| **Q1** 「Distribution」がホスト型・API 提供を含み、そこで義務が発火する。**AI モデルにとって Freedom Zero の問題にならないか** | **当たらない。** §10.1 が条件を一切課さないので、発火する義務が存在しない |
| **Q2** モデルと付随ソフトウェアを 1 つの定義（Licensed Materials）に束ねてよいか（OpenMDW でも懸念が出た） | **当たらない。** ACD-1.0 は*材料*を束ねる定義を持たず、§1.5 は*権利*を分ける（特許 §8 / 商標 §11 / 人格権 §12 を明示的に除外）|
| **Q3** 終了条項が **Licensor に対する訴訟にだけ**適用されるのは OSD 5 の問題か。特許主張が**著作権の許諾まで**終了させてよいか | **当たらない。** §8.2 が「特許報復条項は無く、その不在は意図的」と明言し、§10.4 が「いかなる理由でも終了しない」と述べる |
| **Q4** 特許主張による終了が **Derivative Materials**（他者の後続改変）にまで及ぶのは広すぎないか（GPLv2 の "Liberty or Death" 論争） | **当たらない。** 同上 —— 終了機構そのものが無い |

**4 問すべてが「義務・終了・束ね方」についてであり、ACD-1.0 はそのどれも持たない。**
これは我々の設計が正しいことの証明ではないが、**リストが現に労力を割いている論点の集合と、
ACD-1.0 が持つ表面の集合が、交わらない**ことの直接の観測である。
`comparison.md` §1.45 / §1.48 / §3.x の結論（条件を足す AI ライセンスが止まっている）と同じ向き。

**副次的な観測 2 つ**:
- **委員長ですらスレッド内に本文を求める** —— Chestek 氏は McCoy 氏の募集に対し即座に
  *"Can you provide a link or copy of the text of each license?"* と返した。
  **「plain text で添付せよ」という要件の実務的な意味がここに出ている**（`READY-TO-SUBMIT.md` 手順 2）。
- **審査者は自分で差分を作る** —— McCoy 氏は 2 つの ModelGo を突き合わせた redline を
  自分の GitHub に置いて共有した。MGB の節で記録した「手で差分を作らせるな」と同じ現象。

**そして steward の回答（2026-09-08）が、我々を 2 度引いた** —— Q1 に
*"Yokoi-san, Sep 2026: asked how the Section 2.2(a) conditions operate for hosted-only deployments"*、
Q3 に *"**Yokoi-san's three-axis framing**"*、いずれもアーカイブ URL つきで、
Chestek 氏・McCoy 氏・Berkus 氏と同じ列に。**ACD-1.0 への支持ではない**（誰も ACD-1.0 について
述べていない）が、**#90 の読みは訂正を要する** —— 三軸のメッセージには直接の返信が付かなかったが、
**4 日後に正式な意見募集の背景資料として引かれている。「返信が無い」は「効いていない」ではない。**

### AI ライセンスは 2023 年から出ている —— RAIL（2023-04・4 日で撤回）

**我々が「2024 年より前にゼロ」と述べていたのは、トラッカーの分類であって記録ではなかった**
（`against.md` #103）。アーカイブを直接読むと 2023 年に 2 件ある。

**Restricted Artificial Intelligence License (RAIL)** —— 2023-04-17 提出、**04-21 撤回**。
提出者は個人（言語学出身のソフトウェア技術者）。

**Carlo Piana 氏（2023-04-18）**:
> it is **not a license, but a restriction applied on the top of a license**. As the name suggests,
> the main intent of this document is to impose a restriction on certain uses, users and fields of
> endeavour: **for that it is directly against #5 and #6**, in my reading. **That alone disqualifies
> the "license".** Have you spent time considering the OSD before applying for approval, in the face
> of this striking problem, **without even trying to address it with a convincing rationale**?

**Simon Phipps 氏（同日・個人資格）**:
> I do not believe this submission represents a valid license, since it is **a manifesto for an
> unspecified text** intended to be applied to modify unspecified open source licenses. **Since we
> do not have the full text of any combination to consider for approval**, I believe this submission
> should be automatically rejected.

**ACD へ還元した判断軸 3 つ**:

1. **利用制限を課す AI ライセンスは OSD 5/6 で落ちる** —— これで**3 例目**（RAIL 2023 /
   AI-MIT 2026 / Modified 0BSD 2026）。`comparison.md` §1.45 の結論が、別の年・別の instrument・
   別の批判者で再現し続けている。**ACD-1.0 が条件を持たないことは、この類型で唯一空いている道である。**
2. **OSD への rationale を「先に自分から」出していないと、それ自体が非難される** ——
   *"without even trying to address it with a convincing rationale"*。`submission-reference.md` §3 / §3b が
   その位置にある（§3b は「審査者が逆を論じられる箇所」を我々の側から書く節）。
3. **提出物は自己完結した全文でなければならない** —— 「他のライセンスに重ねて使う断片」は
   *automatically rejected* と述べられている。ACD-1.0 は単独で成立し、置換テキストも
   プロジェクト固有要素も持たない（Check 441g）。

**もう 1 件（Open Constitution License・2023）** は「AI ネットワーク上にホストされたソースコードへ
知的財産権を付与する」と自称する。**本文は未読**（優先度は低い —— 我々の類型ではない）。

**Stefano Maffulli 氏（当時 OSI 事務局長）が同スレッドで語調を戒めている** ——
*"Please, a reminder to everyone to moderate your tones and keep the conversation civil."*
**このリストは荒れることがある**、というのは提出者側が知っておくべき事実である。

### 「取り込んで再提出」を実際にやった提出 —— MGB 1.0（2025-02 / 03 / 09・3 ラウンド 47 通）

オーナー方針は「**届いた議論を全部取り込む → 再提出 → …… を承認されるまで**」である。
**それを実際にやった提出が 1 件ある**ので、手順の側を読んだ（2026-09-07）。提出者は
Mass General Brigham（機関）で、Apache-2.0 を改変した本文を 3 ラウンド出した。

**1. 審査者は「何が新しいのか」を自分で差分にする —— そして下手にやったと言う。**
Pamela Chestek 氏（2025-09-19・リスト宛）:
> For easier reference, I'm attached a copy **marked up with what has changed from the Apache
> license**. The definitions were re-ordered in this license, so **a mechanical comparison didn't
> work**, meaning **there may be errors in my manual markup**.

**手で差分を作らせると、その差分の誤りごと議論が進む。** ACD-1.0 は既存ライセンスの改変では
ないので diff は作れないが、**「何が新しいか」を審査者の側の労力ゼロで示す義務は同じ**である。
`comparison.md` の逐条比較がその役割を負う —— **そして「diff が作れない理由（祖先テキストが
無い）」を先に述べる**ほうが、作れないことを黙っているより強い。

**2. 同じ識別子が 2 つのテキストを指すことは、その場で止められる。**
Chestek 氏（同日・提出者宛）:
> You previously submitted "MGB 1.0," which … you said was already in use. **Are you creating a
> second "MGB 1.0" license with different text? That's not workable, you'll need to have different
> names to distinguish the two licenses.**

**ACD-1.0 の凍結（`FROZEN.md` / Check 453）と §16.4 が防いでいるのは、まさにこの事故である。**
「議論の最中に本文を差し替えない」は我々の内部規律だが、**外部から見ても同じ理由で止められる**。
この観測は、凍結が慎重さではなく**手続き上の要件に近い**ことを示す。

**3. 法的効果を持たない説明的条項は「役割は何か」と問われる。**
Chestek 氏（2025-09-28）:
> does the paragraph change anything about the licensor's liability? **Isn't it still just advisory
> without any legal effect?** … I just think **we need to be clear about its value and role.**

ACD-1.0 にも宣言的・説明的な条項がある（§9.2 が「表明しない」と述べる形、§16 の一部）。
**それぞれが何をするのかを言えるようにしておく** —— 「読者の誤解を防ぐため」は答えになるが、
**答えとして用意しておく必要がある**（この提出者はその場で問われて答えた）。

**4. 借用は「似ている」ではなく指摘される。**
McCoy Smith 氏（2025-09-29）: MGB は MPL/GPL の特許文言を Apache 形の本文へ持ち込んでおり、
*"the problem here was to try to use those predecessor licenses' language in a license
(Apache-2.0) that doesn't formulate it that way"*。
→ **ACD-1.0 は 6 件のライセンスと 8 語連鎖を 1 つも共有しない**（実測・`submission-reference.md` §4c）。

### 要求情報の欠落は、議論を遅らせるのではなく**成立させない**（2026-09-07・BOS スレッドで観測）

Carlo Piana 氏が BOS Public License v1.3 の承認依頼へ返した全文（`license-review` 2026-09-07 09:15 CEST）:

> While on a cursory reading I see just little problems with the provided license text per se,
> in addition to a proliferation issue of being the 10,354th submitted MIT derivative, I cannot
> help but notice that **the submission does not include the required information and therefore
> I will not comment it until the deficiencies are resolved.** Please refer to
> https://opensource.org/licenses/review-process . I would suggest to resubmit.

**読み取れること 2 点**（その読みが establish しないことも併記する規律どおり）:

1. **要求情報の欠落は「指摘されて直す」ものではなく、「議論そのものが始まらない」ものである。**
   本文の中身については *"just little problems"* とまで言いながら、**コメントを保留している**。
   これは個人の対応であって OSI の裁定ではないが、**その人は 2026-07 の BOS v1.0 でも
   最初期に発言している常連**であり、同じことが我々にも起こりうる。
2. **proliferation が最初に来る。** *"the 10,354th submitted MIT derivative"* ——
   ACD-1.0 は MIT 派生ではないが、**「なぜもう 1 つ要るのか」が最初の関門である**ことの
   2 例目である（1 例目は Rob Landley 氏の代替可能性・`against.md` #84）。

**この観測が我々に何をさせたか**: 要件を原典で読み直し、**送る文面（§B.0）が
「OSD 3, 5, 6, 9 を specifically 明言する」要件を満たしていなかった**ことを見つけた
（`against.md` #97）。修正済み。Check 463 も一般的な準拠宣言では通らない形へ締めた。

### FMLL v1.0（2026-07・`license-discuss`）—— **姿勢が最も近い比較対象**（2026-09-07 に原典で読了）

**なぜこれが最も近いか**: 単独著者 / AI・機械学習のためのライセンス / **`license-review` ではなく
`license-discuss` へ「議論してほしい」として投稿** / 本文を投稿本文に貼り付け —— **我々の
2026-08-26 の投稿と姿勢が 4 点で一致する**。ドシエはこれまで FMLL を**件数として数えただけ**で、
スレッドを読んでいなかった（`AS-OF.md` の AI 時代 6 件のうちの 1 件）。

**何が起きたか**: 2026-07-16 に Mihail Poteha 氏が投稿。**約 5 時間後**に David Woolley 氏が
実質的な批判を返し、翌日にもう 1 往復。**計 4 通・2 名。**

**Woolley 氏の指摘 3 点と、ACD-1.0 への当たり方**（原文を引き、発言者を書く）:

| 指摘（2026-07-16 / 07-17） | ACD-1.0 に当たるか |
|---|---|
| *"In general, I don't think it is close to being well drafted"* —— 冒頭でいきなり起草の質を問題にしている | **当たる。** 単独著者・非弁護士という我々の既存の不利な事実（#5 / #79）に対する**2 例目の独立した観測** —— リストの読み手は AI 系の単独起草ライセンスに対して、条項の中身に入る前に起草の質を判断する |
| 再現性の要求は原理的に満たせない（乱数シード・並列スケジューリング・推論時にシードを設定できない UI・収束するのは統計的性質だけ）| **当たらない。** ACD-1.0 は §10.1 により**利用者に条件を一切課さない**ので、満たすべき要求が存在しない |
| *"I'm not sure if the OSD forces you to publish private modifications, but it is generally not part of the open source culture, and it is unenforceable, because it is happening in private"* | **当たらない。** 同上（§10.1 / §10.2 が「source を出さなくてよい」を明示）。ただし**逆向きの示唆がある** —— リストは「私的領域に踏み込む義務」を open source 文化の外と見る |
| *"If they contain private data, you cannot license them at all"*（07-17）| **当たらない**が、**§2.7 の設計と一致する** —— 保有していない権利は許諾できない、という同じ原理 |

**ACD へ還元した判断軸**: 3 点のうち 2 点は「**条件を課すこと**」への反対であり、ACD-1.0 が
条件を持たないことで構造的に回避している（`comparison.md` §1.45 が AI-MIT について出したのと
同じ結論が、別の instrument・別の批判者で再現した）。**同じ結論が独立に 2 回出たことは、
「条件を足す方向の AI ライセンスが止まっている」という読みの根拠を 1 つ強くする。**

**そして最も重い観測は、指摘の中身ではなく速度である。** 同じリスト・同じ姿勢・同じ AI 系で、
**5 時間で実質的な批判が付いた**。我々の投稿には 12 日間 0 通である（`against.md` #96）。

### BOS Public License v1.3（2026-09-06 に外部から共有・**本文は未読**）

`license-review` に**新規ライセンスの提出**が出ている。共有された内容は次の 2 点だけで、
**我々は本文を読んでいない** —— MIT を基礎とすること、public source distribution において
`UPSTREAM.txt` と `CREDITS.txt` を保持する構造であること。**ここに書けるのはこの 2 点だけで、
条項番号も状態もこちらからは書かない**（`AS-OF.md` に未検証として行を足した）。

**AI-native ではない。** OpenMDW / ModelGo と違い、我々と同じ問題領域の instrument ではない。
それでも**測り方**としては 2 つ持ち帰るものがある。

1. **「名指しした file を保持せよ」は、配信経路の問題を AI 文脈の外でも起こす。** ModelGo で
   問われたのは「hosted-only では受領者が Licensed Materials を受け取らないので義務が発火しない」
   だった（#47）。file 保持条件はその一般形である —— **file が届かない配信では、保持しようが
   ない**。我々は #47 を「AI 配備で支配的な形」として記録したが、**この軸は AI 特有ではない**。
   その事実は #47 の位置づけを弱めるのではなく、**軸としての一般性を上げる**（ACD は §10.1 で
   条件を持たないので、どの経路でも発火しない側にいる）。
2. **「よく知られたライセンスへの小さな追加」という、新規提出の最も普通の形。** BOS は
   MIT + 保持義務 2 file で、審査者が新規提出に対して必ず問う「なぜ MIT ではいけないのか」に
   **1 ページの差分で答える**形をとる。ACD-1.0 は逆で、16 節 82 条ある。**同時期の提出として
   並べられたとき、差分の大きさの対比はこちらに不利に働きうる**（#6 の長さ批判が、抽象論では
   なく同時代の実例と並ぶ形になる）。有利な読み方も可能だが、ここには書かない —— 不利な側を
   先に置くのが本ドシエの方式である。

**やらないこと**: 本文を読まずに BOS の条項を評価すること。読めるようになったら
`comparison.md` の「無条件系」ではなく「**条件付き permissive**」の比較軸として扱う。

## 3.9 アーカイブは直接取得できる（2026-09-06 に確定）—— 取得済みの窓と、そこで得たもの

**「この環境は外向きの取得ができない」は誤りだった**（`against.md` #76）。`curl` が**コマンドの
権限**で拒否されただけで、**ネットワークは通っている**。

```
https://lists.opensource.org/pipermail/license-review_lists.opensource.org/<YYYY>-<Month>.txt
```

**ブラウザ相当の User-Agent が要る**（既定の python UA では 403 が返る）。`WebFetch` ツールも
使える。**オーナーに落としてもらう必要はない。**

### 取得済みの窓と、そこで得たもの（**再読不要**）

| 窓 | 得たもの | 反映先 |
|---|---|---|
| **2012-01〜04** | Bruce Perens 氏の「abandonment **OR** acquiescence, but not both」—— **fallback という形そのものへの反対**。§4.4 はこれが届かないように書かれている | `comparison.md` §1.4 |
| **2020-03〜06**（**2026-09-08 に再読・論拠まで**）| License Review Committee の勧告本文。**加えて veto スレッド 49 通の論拠を初めて読んだ** —— Glaser 氏の「不明確でありライセンスの定義を満たさない」に対し、Chestek 氏の「**献呈が無効でも、列挙された許諾が抗弁になる**」が承認へ運んだ。**その読みは Unlicense の条文に無く、論証されたものである**（ACD §4.4 は条文にしている）。**§3.9 は「読了」としていたが、取り出していたのは結論 2 つだけだった** —— **「読了」と「論拠まで読んだ」は別である**。「dedication **taken alone** は承認されない」という**規則の出典**、および「lawyers **both US and non-US**」が一致したという決着の実体 | `submission-reference.md` §1b / #2 #3 #7 |
| **2025-03** | 出力への notice 要件が「**a restriction or condition on mere use. That would not be open source**」（Simon Phipps 氏・個人資格）と問われ、Fontana 氏が編集器の喩えと **Kyle Mitchell 氏の先行提出**にも言及、提出者が「somewhat oversteps」と認めて削除された | `review-responses-clauses.md` §6.4 |
| **2025-02** | ModelGo の**最初の提出**。提出は短いラベル付き header block で始まる（`Drafted By Lawyer` / `Approved or Used by Projects` 等）。**MG-BY-2.0 は採用ゼロで提出され 3 ラウンド審査された** —— 採用は **SPDX の基準**であって `license-review` のゲートではない | `submission.md` §A.0 / #4 |
| **2026-07** | **まるごと 1 件の新規提出のレビュー**（BOS v1.0 → 同月 v1.2）。審査者の最初の 2 通が 「**テキストを添付せよ。動的に変わらない版が要る**」と「**process ページの項目を飛ばすな、特に法的レビュー**」。3 通目に「**your links are broken**」。Carlo Piana 氏の経験則「**25 年誰も思いつかなかったなら問題ではない —— 何か新しいことが起きていない限り（SaaS、extensive AI model usage 等）**」 | `submission.md` §A / #79 / `comparison.md` §1.38 / `REVISION-PROTOCOL.md` ゲート 7b |
| **2026-08** | **OSD 9 の生きた読み方**（防御的終了条項自体が「restrictions」にあたりうる・Apache-2.0 の特許終了と GPLv2 非互換の歴史）。さらに**原理的な反対** ——「著作権侵害は copying を要する。**落ち度のない第三者に請求権を放棄させる**のは open source の原理に反する」 | `submission-reference.md` §3b / #46 / `review-responses-clauses.md` §11 |
| **2026-09** | オーナーの投稿 **4 通**（OpenMDW 2 / ModelGo 2。**うち 09-05 の 1 通はアーカイブに独立して存在せず、返信の引用の中にしか残っていない** —— `against.md` #91）、Mike Dolan 氏の「the trigger **is not designed to match the grant**」、Moming Duan 氏の hosted-only 解釈、**Shuji Sado 氏が我々の質問を引いて議論を進めた**、Ruby Anna 氏の "100% correct" 確認、BOS v1.3 の提出本文。**アーカイブ済み 22 通のうち steward は 3 通で最多タイ**（Fontana 氏・Dolan 氏と並ぶ）| 本書 §0.6 / `rounds/` 6 file / `AS-OF.md` |
| **`license-discuss` 2026-07〜09**（**別のリスト**・2026-09-06） | **我々の投稿そのものが原典で確認できた** —— 2026-08-26 17:17 の 1 通、同題の後続 **0 通**、9 月は別スレッド 2 通のみ。ドシエが述べてきた「投稿し受理された・返信ゼロ」は**初めて一次資料で裏が取れた**。同時に **3 つの不利な事実**が出た: 送った本文は **5,778 語**でリポジトリに存在しなかった（#82）／**19 日前の同型の投稿（単独著者・非弁護士・PD 等価・採用ゼロ・license-review から差し戻し）には約 10 時間で 6 通の返信**が付いていた（#83）／Rob Landley 氏の「PD 等価は**代替可能**な唯一の類型で 0BSD が既にある。なぜもう一つ作る？」に答えが無い（#84）。**有利な確認も 3 つ**: 同スレッドで指摘された商標まで放棄する欠陥は ACD-1.0 には無い（§1.5 / §11.1・条文で確認）／**投稿の件名慣行**（`license-review` は `For Approval: <名前>`）に `submission.md` §B.0 が既に一致していた／**「`license-discuss` は承認の窓口ではない」を McCoy Smith 氏が 2026-08-04 にリスト上で明言**していたので、この主張が断言から出典付きへ変わった。さらに**代替説明が 1 つ潰れた** —— 同じアーカイブに「返信が spam に振り分けられていた」提出者がいる＝実在する失敗モードだが、**アーカイブが配信の記録**なので我々には当てはまらない | `rounds/2026-08-26-license-discuss-sent.txt` / #82 #83 #84 / `REVIEWERS.md` |

### 読み方の規律

1. **原文を引き、発言者を書く。** 提出者による後の要約で代用しない（2025-03 は要約経由で一度
   書いてから、本文で書き直した）。
2. **その読みが**何を**establish しないか**を同じ場所に書く。個人資格での発言・提出者の判断・
   撤回は、いずれも **OSI の裁定ではない**。
3. **有利な材料も落とさない。** #70 が示したのは「擁護している側こそ古くなる」ことで、
   **有利な展開を落とすのは期限切れを残すのと同じ失敗**である。

### 手で毎回再構成しなくてよくなった資源（2026-08-28 にリスト上で公開）

**`LicenseAtlas` の審査トラッカー** —— `license-review` と `license-discuss` のアーカイブから
構築され、数時間ごとに自動更新される。ページは `https://morningd.github.io/license.atlas/tracker`、
**機械可読な実体は `https://morningd.github.io/license.atlas/data/tracker.json`**（約 18 MB）。
Richard Fontana 氏が「This looks really useful」と述べ、2011 年の議論を辿るのに使えたと書いている。

**我々にとっての意味は 2 つ**である。(1) 月ごとのアーカイブを手で読んで再構成してきた
「いつ提出され、いつどう決着したか」が **1 回の取得で得られる**。(2) **ACD-1.0 はそこに載っていない**
（#86）。19 日前の `license-discuss` 投稿は載っているので、discuss を対象外にしているわけではない。

**取得はリポジトリへ入れない。** 18 MB の第三者データで、我々の主張の根拠にするなら
**その時点の数値を `AS-OF.md` に日付つきで引く**のが正しい（丸ごと抱えると、更新されたときに
どちらが真か分からなくなる）。**分類の方法は未検証**なので、引くときは「トラッカーの数値」と明示する。

### 提出の全数調査（2026-09-07・`license-review` 2023-01〜2026-09）

**#99 が要求した「2 度目の走査」を、名称ではなく全件で行った。** 44 か月・7.0 MB を取得し、
`Subject:` を正規化して**提出スレッド 154 件**を列挙した（`For Approval` / `Submission` /
`Request for … approval` / `New License for Consideration` 等）。取得法は §3.9 と同じ。

**この方法が名称検索より強い理由**: PBZC は名称に public domain / dedication / waiver /
CC0 / Unlicense / 0BSD のどれも含まないので、**#87 の走査では原理的に出てこなかった**。
**件名の全数を出してから中身で絞る**と、名称の付け方に依存しなくなる。

| 読了 | スレッド | 反映先 |
|---|---|---|
| ✅ | PBZC v2.0（2024-12・撤回）| `comparison.md` §1.46 / #99 #100 |
| ✅ | Irrevocable MIT (MIT-I)（2025-07・18 通）| `comparison.md` §1.47 / #101 |
| ✅ | AI-MIT / AIAL-1.0（2026-03・撤回）| `comparison.md` §1.45 |
| ✅ | ModelGo 各版 / OpenMDW-1.1 | §0.6 / §1.5 |
| ✅ | BOS Public License v1.0〜v1.3 | §3.x / #79 |
| ✅ | FMLL v1.0（`license-discuss`）| §3.x / #96 |
| ✅ | Modified 0BSD (Maintenance-Required)（2026-03・却下）| `comparison.md` §1.48 / #102 |
| ✅ | MGB 1.0（2025-02/03/09・3 ラウンド 47 通）| 本書「取り込んで再提出」節 |
| ✅ | RAIL（2023-04・4 日で撤回）| 本書「AI ライセンスは 2023 年から」節 / #103 |
| ✅ | Tiwaz License v1.0（2025-05/07・16 通）| 本書「Tiwaz」節 |
| ✅ | FFOL（2024-10・5 通）| 本書「FFOL」節 —— #97 の外部裏付け |

**未読・優先順つき**（**この一覧は次に消費されるべき候補であって、網羅ではない**）:

| 優先 | スレッド | なぜ我々に効くか |
|---|---|---|
| 中 | **RAIL（Restricted AI License）**（5 通）| AI + 制限。**条件を足す AI ライセンスがどう扱われたか**の追加事例（`comparison.md` §1.45 の結論の検証） |
| ✅ 済 | 小規模・単独提出 12 件 | **類型として測った**（本書「単独提出者は無視されない」節）。応答者中央値 4 人・初回応答中央値 27.7 h・応答ゼロは 0 件 |

### 沈黙の基準率 —— `license-discuss` の全数調査（2026-09-09・2024-01〜2026-09）

**我々はこれまで、自分の沈黙を「返信が付いた 3 つのスレッド」と比べてきた**（#83 の同型投稿が
約 10 時間で 6 通 / #96 の FMLL が約 5 時間 / 2026-09-05 の Viatrix が約 4 時間）。
**基準率を一度も計算していなかった。** 計算した。

**方法**（再現可能）: `license-discuss` の 2024-01〜2026-09 を月次 `.txt` で取得（**取得できた
30 か月・439 通**）。`Subject:` は折り返しと RFC 2047 符号化を復号してから `Re:` を剥がし、
正規化した先頭 45 文字でスレッドへまとめる。Mailman の digest 通は除外。
**「誰かが自分のライセンスまたは草案を意見のために持ち込んだスレッド」**を件名の型で抽出した
（`Request for Comment|Feedback` / `License Review Request` / `[SUBMISSION]` / `[DISCUSS]` /
`[NEW LICENSE]` / `For Review:` / `Draft for discussion` / `Submission of` / `Proposal of` ほか）。
**分類は我々のものである。**

| | 実測 |
|---|---|
| スレッド総数（digest 除く） | **68** |
| うち返信ゼロ | **15（22%）** |
| 「ライセンス・草案を持ち込んだ」スレッド | **28** |
| **うち返信ゼロ** | **5（18%）** —— Lone Dynamics（2024-09-09）/ For Review: New strong copyleft（2025-06-26）/ PUWL の `[EXTERNAL]` 自動転送（2025-10-01・実質は複製）/ Citizen Research（2026-05-18）/ **我々（2026-08-26）** |
| 複製を除いた実質 | **4 / 27 = 15%** |
| 冒頭メッセージの大きさ（中央値） | **3,417 B** |

**再現した（2026-09-10・独立に数え直した）**: **71 スレッド / 返信ゼロ 17（24%）。**
上の 68 / 15（22%）と一致すると見てよい ——差は**アーカイブが 2026-09-09 以降に伸びたこと**と
正規化の細部による。**この数字は再導出せずに引用してよい。**

**ただし数え方が決定的である。** 同じ窓の **444 通のうち 224 通は `Subject:` が継続行へ
折り返されている**（pipermail の仕様）。**unfold せずに件名で束ねると 37%**、
**unfold のみだと 30%**、**unfold + MIME デコード + `[License-discuss]` 接頭辞の除去 +
小文字化まで行って 24%** になる ——**手順が違うだけで 13 ポイント動く。**

**再現手順（次に数えるときはこれを使う）**: ① 月次 `.txt` を取得 ② `From ` 行でメッセージへ分割
③ **先頭の空行までをヘッダとし、継続行を unfold** ④ `Subject:` を **MIME デコード** ⑤ `Re:` /
リスト接頭辞を除去し小文字化 ⑥ digest を除外 ⑦ 出現 1 回のものを「返信ゼロ」と数える。
| **我々の冒頭メッセージ** | **39,483 B —— 中央値の 11.6 倍。全 68 スレッド中 2 番目に大きい** |
| **最大の冒頭メッセージ** | **48,559 B（Project Tick・2026-01-21）→ 返信 11 通** |

### これが establish すること

1. **返信ゼロはこのリストで珍しくない。** ライセンスを持ち込んだスレッドの **7 件に 1 件**が
   そうなる。**我々の沈黙は、欠陥の証拠でも拒絶の証拠でもない。**
2. **我々の直前のメッセージ（Šuklje 氏・2026-08-25）も返信ゼロだった** ——
   何度もワークショップを重ねて合意した解決策の告知であり、書いたのは経験のある参加者である。
   **返信ゼロは投稿者についての評価ではない。**
3. **長さは決定的ではない。** 我々より大きい冒頭メッセージが 11 通の議論になっている。

### これが establish しないこと

- **「だから我々の投稿でよかった」ではない。** 冒頭メッセージの大きさは中央値の **11.6 倍**で、
  これは実測された外れ値である。次の venue でこの形を繰り返す理由にはならない
  （`REVISION-PROTOCOL.md` §3.7 と `submission.md` §B.0 は既に短い形を定めている）。
- **沈黙の原因**は依然として分からない。**分かったのは、原因を探すべき異常があるという前提の方が
  誤りだった**ということである。

### 我々の側の失敗として（#109）

**3 つの比較対象はいずれも「返信が付いた側」からの抽出だった。** 返信が付いたスレッドだけを
並べれば、返信ゼロは異常に見える。**標本を率として報告した** —— #87 が
「ある道具が出した数を、世界についての事実として報告した」と記録した失敗の、別の形である。
**比較対象を挙げるときは、その比較対象がどの母集団からどう選ばれたかを同じ場所に書く。**

**注**: これは**件名の全数調査であって通読ではない**（本節の直前の警告と同じ区別）。
28 スレッドのうち原典で読んだのは、別の節に記録した分だけである。

### ACD-1.0 が依拠する 3 主題は、このリストでは 2024 年より前にほぼ存在しない（2026-09-09・6 年分を計量）

**`license-discuss` の 2021-01〜2026-09 を取得し（**28 + 30 = 58 か月・745 通**）、
ACD-1.0 が依拠する主題の出現回数を年ごとに数えた。**

| 年 | 通数 | moral rights | sui generis / database right | ML・TDM | PD-equivalent | CC0 | estoppel |
|---|---|---|---|---|---|---|---|
| 2021 | 125 | 0 | 0 | 0 | 6 | 4 | 0 |
| 2022 | 86 | 1 | 0 | 1 | 0 | 0 | 6 |
| 2023 | 95 | 0 | 0 | 3 | 0 | 0 | 0 |
| 2024 | 189 | **92** | 1 | **37** | 2 | 17 | 1 |
| 2025 | 151 | **31** | 0 | 7 | 0 | 4 | **6** |
| 2026 | 99 | **106** | **15** | **30** | 6 | 4 | 0 |

**通数は年ごとに 86〜189 でほぼ一定なので、これは投稿量の増減ではない。**

### 読み方（これが establish すること / しないこと）

**establish する**: **§12（人格権）・§7（データベース権）・§6（学習と TDM）の 3 つは、
このリストの議論としては新しい。** 2021〜2023 の 3 年・306 通で、人格権は **1 回**、
データベース権は **0 回**、ML/TDM は **4 回**しか現れない。
**これは #29（「ACD-1.0 の最も特徴的な条項は、OSI の審査能力が最も薄い場所に在る」）を、
引用ではなく数で裏づけている。**

**establish しない**: 「リストがこれらの主題へ関心を向けた」。**内訳を見ると 1〜2 スレッドに
集中している** —— 2024 年の人格権 92 回はほぼ Blue Oak スレッド（83）、2026 年の 106 回は
Linkumori スレッドである。**「よく議論される主題になった」ではなく「たまに 1 本立つ」**である。
その意味では #29 の懸念はむしろ強まる —— **蓄積ではなく単発**だから。

**この計量で `license-discuss` の窓は閉じた。** 2021-01〜2026-09 を取得済みで、
主題別の計量と件名の全数調査（上の「沈黙の基準率」節）を通した。
**通読ではない**（読んだスレッドは各節に記録がある）。

### 決定の機構が原典で分かった（2026-09-09・McCoy Smith 氏 2026-08-28）

**ドシエは「OSI の決定は初回投稿から概ね 60 日」と 2 箇所で述べていた。誤りだった。**
Licensing Committee として書かれた 1 通が、機構を説明している。

> **We work on a two-month review cycle**, which normally would have put your licenses up for
> Board review in August (**the July Board meeting was prior to two months from your final
> submission**), but we don't have an August Board meeting (hard to get a quorum in August), in
> favor of our **face-to-face Board meeting on September 24**.
> …Please give any **final thoughts on these licenses before September 17 2026 so a recommendation
> can be provided to the Board** at our September meeting.

**分かること 3 つ。**

1. **時計は「最終提出」から回る。** *"prior to two months from your **final** submission"*。
   **改訂するたびに戻る。**
2. **委員会が勧告し、理事会が会合で決める。** 会合の日程（8 月は定足数が取れないので飛ばした）は
   リストからは見えない遅延要因である。
3. **遅れの理由が提出者の改訂に帰されている** —— 同じ 1 通で
   *"this is in part as a result of how your initial submission has progressed… **quite a bit of
   revision by you** since then"*。

**これは我々の版管理（`REVISION-PROTOCOL.md` §2「1.0 は永久凍結・次版は横に置く」）を、
外側から裏づける。** 凍結は礼儀ではなく、**決定までの時間を最短にする手段**でもある ——
審査中に本文を動かすと、その分だけサイクルが後ろへずれる。

**そして沈黙の見え方が変わった。** ModelGo の steward は 2026-01-27 / 05-26 / 07-26 に
フォローアップを出し、**どれにも返信が付かなかった**。**最初の返信は 2026-08-28** で、
**10 日のうちにリスト上で最も活発なスレッドになった**（正式な意見募集・委員長の本文要求・
4 人の関与）。**初回提出（2025-02）から 19 か月、最後の未応答フォローアップから 7 か月。**

**ドシエはこの例を「返信を得ていない」として 2 箇所で引いていた** —— 書いた時点では真だった。
**訂正済み**（`REVISION-PROTOCOL.md` §3.5 / §3.6）。**結論（移動の引き金を「返信」に置かない）は
変わらないが、理由は「来ないかもしれない」から「間隔が月単位で制御外である」へ変わった。**

### まだ読んでいない窓（候補）

> **この一覧は `AS-OF.md` と食い違いうる。** 実際 2026-09-06 に、**既に原典で読んだものが未読として
> 残り、しかも「そこには無い」という誤った所在まで述べていた**（#88）。**書き足すときも消すときも、
> `AS-OF.md` を先に grep すること** —— 権威は「何を読んだか」を記録している側であって、この一覧ではない。


- ~~**CC0 の撤回そのもの**~~ —— **既読だった**。`AS-OF.md` は 2026-09-06 の時点で「原典で読了・
  **CC 自身の撤回文（2012-02-24）を license-review 2012-02 から引用**・理由は estoppel と
  "on notice" の 2 点・特許の除外は**科学データ・コミュニティ**由来」と記録している。
  **この行は「読んでいない」と述べ、さらに「license-review には無い」と述べていたが、どちらも
  誤りだった**（`against.md` #88）
- ~~**FMLL v1.0**~~ —— **2026-09-07 に読了**（`license-discuss` 2026-07・4 通）。**姿勢が最も近い比較対象**で、指摘 3 点のうち 2 点は「条件を課すこと」への反対ゆえ ACD-1.0 には当たらない。**最も重い観測は速度**（5 時間で返信）。§3.x と `against.md` #96
- **ModelGo の 2nd 提出**（2025 年半ば）—— 1st（2025-02）と 3rd（2025-12 提出・2026-09 も継続）は読んだ。**何がラウンドを跨いで変わったか**の中間点が残っている
- ~~**2026-08 の残り**~~ —— **2026-09-06 に読了**。全 102 通は 5 筋しかなく（OpenMDW 85 / Python 13 / ModelGo 3rd 2 / 統治調査 1 / **volume の注意喚起 1**）、既読の OpenMDW 以外で得たものは: **Luis Villa 氏の code of conduct 引用**（2026-08-28・§3.7 に発言者と日付を追記）／**Pamela Chestek 氏「1 ライセンス 1 メール」**／**McCoy Smith 氏「OSI は提出者が求めたときにのみ審査する」**／**Max Mehl 氏の有利な反証** ——board 承認を受けた提出者が「レビュー要求への返信としてフィードバックがあればよかった」＝**スレッドに返信ゼロのまま承認されうる**（`AS-OF.md`・#83 の答えへ反映）／**`LicenseAtlas`**（下記）
- **`license-discuss` の過去分** —— **2026-09-09 に 2024-01〜2026-09 の 30 か月・439 通を取得し、件名の全数調査を行った**（上の「沈黙の基準率」節）。**通読ではない。** それ以前の記録: **2026-09-06 に 2026-01〜09 の全月を取得した**（1 月 17 / 2 月 2 / 3 月 33 / 4 月 4 / 5 月 1 / 6 月 11 / 7 月 4 / 8 月 23 / 9 月 2 = 計 97 通）。**ただし読了ではない** —— この取得で行ったのは **steward の投稿を全月から探す targeted な検索**だけで、通読はしていない（結果: 2026-08-26 の 1 通のみ）。**`license-review` とは参加者も話題も違うリスト**なので、CC0 の撤回など `license-review` に無い議論は依然こちら側にある可能性がある。**取得と読了を同じ語で書かないこと** —— 取得済みと書くと次のセッションは読んだものとして扱う

## 4. 結果が出たとき、ACD の何が動くか（先に決めておく）

改訂の圧力がかかった局面で考えると、都合よく読む。**先に決めておく。**

| 向こうの結果 | ACD 側で変えること |
|---|---|
| **承認された** | `comparison.md` §1.5 と `submission-reference.md` §1a の「審査中」を「承認済み」へ。**より重要なのは「最も近い承認済みライセンス」の集合が変わる**こと —— OSI の必須比較対象に入るので、§1 の比較を書き直す。against.md #28 の status も動かす（proliferation の問いが一段厳しくなる） |
| **却下された** | **理由が ACD にも当たるかを 1 件ずつ見る。** 当たるものは against.md へ足す。**当たらないものを「向こう固有」として片付けない** —— 却下理由は分野全体の基準を示すことが多い |
| **改訂された** | 差分を読み、**なぜ直したか**を見る。ACD の同じ箇所（notice / 特許報復 / 出力 / 蒸留）に同じ問題があれば errata へ |
| **議論が長期化した** | 論点そのものを収穫する。**結論が出ていなくても、何が争点かは ACD の想定問答に効く** |

## 5. やらないこと

- **自動監視を CI に入れない。** 外部フォーラムを定期取得する workflow は壊れやすく、
  `aio-monitoring.yml` の目的とも違う。手で見て、見たことをここに記録する。
- **向こう固有の問題を ACD へ持ち込まない。** trade secret の扱いや distillation 除外は
  向こうの設計判断であり、ACD が真似る理由にはならない。**還元するのは論点であって条項では
  ない。**
- **ACD に有利な材料だけを拾わない。** 拾った材料が ACD の独自性を弱めるものなら、
  `against.md` に足すのが正しい置き場である（#28〜#31 はそうやって入った）。
