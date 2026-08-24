---
file: docs/architecture/acd-license-rationale.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: LICENSES/ACD-1.0.txt / LICENSE / AI2AI.md / robots.txt
---

# Autonomous Commons Dedication 1.0 — 設計根拠と申請ドシエ

```
License Name      : Autonomous Commons Dedication
Version           : 1.0
Short identifier  : ACD-1.0
Full text         : LICENSES/ACD-1.0.txt
Steward           : Yuta Yokoi (横井雄太 / Yokoi Yuta)
Steward contact    : https://yutapr0117-design.github.io/portfolio/llms-full.txt
Status            : 起草完了・申請前。**本文はまだ freeze していない**（§7 参照）
```

> **この文書の役割**: ACD-1.0 を SPDX License List / OSI License Review へ提出する際に
> 必要になる根拠一式を、提出者がそのまま使える形で置く。**実際の提出は人間しか行えない**
> ので、AI 側は「提出可能な状態にする」ところまでを担当する。
>
> **免責**: 私（実装 AI）は弁護士ではなく、本書は法的助言ではない。本書は公開されている
> 審査基準に対して**機械的に照合した結果**であって、承認を保証するものではない。

---

## 1. なぜ新しいライセンスなのか（OSI の必須要件「既存で埋まらない gap を埋めること」）

OSI の License Review は、**「既存のライセンスでは埋まらない gap を埋めること」を明示的な
要件**にしている（proliferation 対策）。SPDX も「既存 License List のいずれとも一致しない
こと」を definitive requirement に置く。したがって「自由に使ってよい」だけのライセンスは
CC0 / Unlicense / MIT-0 と重複し、**それ自体が却下理由になる**。

ACD-1.0 が埋める gap は 3 つあり、**いずれも既存の OSI 承認ライセンスに存在しない**。

### Gap 1 — 機械学習・TDM に対する「積極的許諾」と留保の明示的放棄

現行の主要 FOSS ライセンスは、1990 年代のテキストを 2020 年代の技術に写像している状態で、
**「AI 学習」という語を話すライセンスは存在しない**。

**ここは正確に述べる必要がある（審査で最初に突かれる点）。** EU DSM 指令 (EU) 2019/790 第 4 条
(3) は、権利者が「適切な方法（オンライン上の著作物については機械可読な方法）で明示的に留保」
した場合にのみ TDM 例外を排除する。つまり **沈黙は留保ではない** —— 「沈黙＝拒否」と書くのは
法的に逆であり、そう書けば主張ごと崩される。**本当の gap はそこではない**:

1. **留保は権利者以外も付けられる。** robots.txt・HTTP ヘッダ・プラットフォーム側の opt-out
   レジストリなど、作品に**添付される**信号はホストやアグリゲータが操作でき、下流の消費者は
   それを作品と一体のものとして受け取る。ライセンスが沈黙している限り、**その信号を上書き
   する根拠が作品側に無い**。
2. **EU 域外では位置づけ自体が未確定。** 米国の fair use 訴訟は係属中で、沈黙から許諾を
   導けるかは法域ごとに割れている。
3. 結果として、**ライセンスだけを読む自動化された消費者は、Computational Use が許されるかを
   判定できない**。判定できない許諾は、学習されるための著作物にとっては許諾ではない
   （ACD-1.0 §6.5 が条文としてこれを述べている）。

ACD-1.0 §6 はこの 3 点すべてに正面から答える：Computational Use を**明示的に許諾**する
(§6.1)／留保を行わず、行うことを**明示的に拒否**する (§6.2)／**誰が付けたものであれ**作品に
添付された留保について、Dedicator 自身の権利の限りで撤回し依拠を否認する (§6.3・§2.7 で射程を
限定)／学習結果のモデル・重み・出力に一切の負担を課さない (§6.4)。さらに §8.4 が**特許許諾を
Computational Use とその成果物まで及ぼす**ので、「著作権では学習してよいが特許では危ない」という
半端な状態が残らない。**「留保しない」ことを作品側から機械可読に宣言し、かつ特許まで届かせる
ライセンスは、現時点で他に無い。**

近接するものとして Creative Commons の **CC Signals**（2025-06 発表）があるが、これは CC 自身が
「著作権を通じて機能するものではなく、CC ライセンスでもない — より広く採用されている *社会契約*
によって規律される」と述べているとおり **ライセンスではなく選好シグナル**であり、しかも
**条件を要求する方向**の枠組みである。ACD-1.0 とは機構も向きも異なり、gap は重ならない。

### Gap 2 — 公有化型ツールにおける明示的な特許許諾

CC0 は 2012 年に OSI へ提出されたが、**承認に至らず Creative Commons が取り下げた**。最大の
争点は CC0 第 4 条 (a) の「Affirmer の保有する特許権は放棄・licence されない」という明示的な
**特許不許諾**で、審査委員会は「これを承認すれば危険な先例となり、CC0 で公開されたソフトウェア
の利用者が持つ特許侵害の防御をむしろ弱めかねない」と懸念し、**OSD 7 に抵触しうる**と評価された。

ACD-1.0 §8 は**明示的な特許許諾**を置き、§8.2 で報復条項が無いことを明言し、§8.3 で
「特許権を留保する読み方は退ける」と解釈規範まで書いている。**CC0 を止めた当の争点を正面から
解消した公有化型ツールは他に無い。** これは ACD-1.0 が「CC0 の再提出」ではないことの中核根拠
でもある。

さらに §8.4 は、その特許許諾を **Computational Use（機械学習・TDM）とその成果物（モデル /
パラメータ / 埋め込み / 出力）まで明示的に及ぼす**。Apache-2.0 を含む既存の特許許諾条項は
「Work およびその Derivative Works の製造・使用・頒布」を射程とするのが通例で、**学習済み
モデルがそのどちらに当たるかは未解決**である。Gap 1（機械学習の積極的許諾）と Gap 2（特許
非留保）は、この一文で初めて**同じ利用者に対して同時に成立する** —— 片方だけでは「著作権では
学習してよいが特許では危ない」という半端な状態が残る。

### Gap 3 — 機械生成著作物における権利の不確実性そのものへの対処

既存ライセンスはいずれも「私が保有する著作権を許諾する」という構造を採る。しかし機械生成部分
については、**そもそも権利が発生するかが法域ごとに未確定**であり、権利が無ければ「許諾」は
空振りし、逆に将来発生すると解された場合には許諾の射程が争われる。

ACD-1.0 §9 は、**権利の存否を問わず結論が変わらない**構造にする：存否について表明を行わず、
機械生成部分に権利を主張せず、利用者に「どの部分が機械生成か」を判定させず、権利が生じた場合
には §3〜§8 と §12 が全面適用される。**権利の不存在と存在の両方に耐える設計を明文で持つ
ライセンスは他に無い。**

---

## 2. 既存ライセンスとの比較（非重複の証明）

| | 無条件（条件ゼロ） | 明示的な特許許諾 | AI 学習の積極的許諾 | TDM 留保の放棄 | 機械生成著作物条項 | 人格権の法域別フォールバック |
|---|---|---|---|---|---|---|
| **ACD-1.0** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| CC0-1.0 | ✅ | ❌ **明示的に不許諾** | ❌ | ❌ | ❌ | 一部（放棄のみ） |
| Unlicense | ✅ | ❌ 言及なし | ❌ | ❌ | ❌ | ❌ |
| MIT-0 | ✅ | ❌ 言及なし | ❌ | ❌ | ❌ | ❌ |
| 0BSD | ✅ | ❌ 言及なし | ❌ | ❌ | ❌ | ❌ |
| WTFPL | ✅ | ❌ 言及なし | ❌ | ❌ | ❌ | ❌ |
| Apache-2.0 | ❌ 表示・変更告知が条件 | ✅ | ❌ | ❌ | ❌ | ❌ |
| MIT / BSD | ❌ 表示が条件 | ❌ 言及なし | ❌ | ❌ | ❌ | ❌ |
| PDDL-1.0 | ✅（データ向け） | ❌ | ❌ | ❌ | ❌ | 一部 |
| CC-BY-4.0 | ❌ 表示が条件 | ❌ | 黙示的に可 | ❌ | ❌ | 一部 |
| CC Signals | — **ライセンスではない** | — | ❌ 逆向き（条件要求） | ❌ | ❌ | — |

**結論**: 「無条件」列を満たす既存ライセンスはいくつもあるが、**それらはいずれも特許・AI 学習・
機械生成著作物の 3 列すべてで沈黙している**。ACD-1.0 は 6 列すべてを満たす唯一の候補であり、
SPDX の matching guidelines における「既存テキストとの一致」にも当たらない。

### 2.1 最も近い OSI 承認ライセンスとの逐条差分（審査で必ず問われる点）

OSI の License Review は提出者に「**最も近い既承認ライセンスとの違いを述べよ**」を求める。
表の 1 行では答えにならないので、逐条で示す。近いものは方向の違う 2 つある。

#### (A) 0BSD — 「条件ゼロ」という点で最も近い（2015 承認）

0BSD の operative text は実質 1 文である:

> Permission to use, copy, modify, and/or distribute this software for any
> purpose with or without fee is hereby granted.

**共通する点**: 表示・変更告知・reciprocal のいずれも要求しない。条件ゼロという性格は同じ。

**0BSD が扱っていない面**（＝ ACD-1.0 が足している面）:

| 面 | 0BSD | ACD-1.0 | なぜ実務上効くか |
|---|---|---|---|
| 客体 | 「software」 | Work（source/object/**データ/メタデータ/音声・画像**・これらの編集物）§1.2 | 学習対象はコードだけではない。データセットや音声を同じ条項で扱えないと、同一リポジトリ内で権利関係が割れる |
| 特許 | 言及なし | §8.1–8.5（**Computational Use とモデル・出力まで**） | ソフトウェアは、それが体現する請求項を実施せずには使えない。沈黙は受領者を露出させる |
| ML / TDM | 言及なし | §6.1–6.5（許諾・留保の拒否・既存留保の撤回・成果物の非拘束） | 沈黙は拒否ではないが、**ライセンスだけを読む自動化された消費者は判定できない**（§1 Gap 1） |
| sui generis database right | 言及なし | §7.1–7.2 | EU では抽出・再利用が著作権とは別の権利で捕捉される。「software」の許諾では届かない |
| 人格権 | 言及なし | §12.1–12.6（放棄 → 不能な法域では**本著作物限定の不行使**、承継人まで） | 日本法 59 条のように一身専属で放棄不能な法域がある。放棄一本では起草者の居住国で空振りする |
| 機械生成著作物 | 言及なし | §9.1–9.4 | 権利が subsist するか自体が未確定。**判定を受領者に負わせない**ことを明文化する |
| 撤回不能性・承継人 | 言及なし | §2.2・§2.5（reliance / estoppel）・§2.8（承継人拘束） | 権利が人手に渡った時が最も長期のリスク |
| 許諾行為の列挙 | use / copy / modify / distribute | §4.2（**sublicense / 公衆送信 / 上映・実演 / 貸与 / 翻案**を含む） | 0BSD の 4 動詞は大陸法の支分権を網羅しない |

**したがって「0BSD で足りるのでは」への答えは**: 条件ゼロという*性格*は同じだが、
**0BSD は本ライセンスが埋めようとしている 7 面すべてで沈黙している**。0BSD に patent grant を
別途添えるという代替案も成り立たない —— 別紙の許諾は作品とともに流通せず、下流の受領者が
その存在を知る保証が無い（§6.5 が述べる「自動化された消費者が判定できるか」の問題）。

#### (B) Apache-2.0 — 「明示的な特許許諾」という点で最も近い

**共通する点**: 明示的な特許許諾を置く FOSS ライセンスであること。

**違い**:

| 面 | Apache-2.0 | ACD-1.0 |
|---|---|---|
| 条件 | 表示の保持・変更告知・NOTICE 継承が**条件** | 条件ゼロ（§4.3・§10.1） |
| 特許の射程 | 「Work and Derivative Works」の製造・使用・頒布等 | 同左 **＋ Computational Use とモデル・パラメータ・出力**（§8.4） |
| 特許報復 | あり（§3 後段で終了） | **無し**、かつ無いことを明文化（§8.2） |
| ML / TDM | 言及なし | §6 |
| 人格権 | 言及なし | §12 |
| 機械生成著作物 | 言及なし | §9 |

**Apache-2.0 の特許条項が「学習済みモデル」に届くかは未解決**である（"Work and Derivative
Works" のどちらでもない可能性がある）。ACD-1.0 §8.4 はそこを明示的に埋めた条項であり、
これは **ACD-1.0 に固有**の内容として審査で示せる。

---

---

## 3. Open Source Definition 適合（OSI が提出者に求める宣言）

OSI は提出者に対し **OSD 適合、とりわけ OSD 3・5・6・9 への適合を積極的に宣言すること**を
求める。ACD-1.0 は条件を一切課さないため、10 項目すべてを構造的に満たす。

| OSD | 要求 | ACD-1.0 の該当箇所 |
|---|---|---|
| 1 Free Redistribution | 販売・頒布を制限せず、ロイヤリティを要求しない | §4.2（sell / distribute を明記）／§4.3（無条件）／§3.2（remuneration の放棄） |
| 2 Source Code | ソース形態での頒布を許す | §4.2「in source form, in object form, or in any other form」 |
| 3 Derived Works | 改変と派生物の頒布を同条件で許す | §4.2（modify / derivative）／§4.3（reciprocal licensing を条件にしない） |
| 4 Integrity of Author's Source | 改変の制限を課さない | §10.2（変更告知すら不要）。パッチ要件なし |
| 5 No Discrimination Against Persons or Groups | — | §4.3「persons, groups … に関する制限を課さない」 |
| 6 No Discrimination Against Fields of Endeavor | — | §4.3「field of use / endeavours に関する制限を課さない」／§6.1（商用可） |
| 7 Distribution of License | 追加の許諾行為なしに再頒布先へ権利が及ぶ | §2.3（受諾行為不要）／§5.3（intended beneficiary として承継）／§16.2（識別子のみで通知足りる） |
| 8 License Must Not Be Specific to a Product | — | §16.3（いかなるプロジェクト・人・法域にも特定されない） |
| 9 License Must Not Restrict Other Software | — | §10.1（一切の条件なし）／§6.4（モデル・出力に負担を課さない） |
| 10 License Must Be Technology-Neutral | — | §4.2「by any means now known or later devised」／§2.3（クリックラップ不要） |

**OSD 7 に関する補足**: CC0 が問題視されたのは特許不許諾ゆえに「再頒布先が追加の許諾を要する」
状態になりうる点だった。ACD-1.0 は §8.1 で sublicensable かつ transferable な特許許諾を置き、
§8.2 で終了不能としているため、この懸念は生じない。

---

## 4. SPDX License List の inclusion principles 適合

| 原則 | 状況 |
|---|---|
| 既存ライセンスと一致しないこと | ✅ §2 の比較表のとおり。テキストも独自起草 |
| OSI 承認ライセンスは自動収録 | 該当すれば自動。未承認でも独立に申請可 |
| 実行形式のみでソース非提供のライセンスを除く | ✅ 該当しない |
| **テキストが確定し、起草途中でないこと** | ⚠️ **現在は未 freeze**（§7） |
| **steward が収録後に改変しないことをコミットすること** | ⚠️ **提出時に確約が必要**（§7） |
| **実際に相当程度使われていること** | ⚠️ **最も弱い点**（§7） |
| 特定のプロジェクト・団体・企業に固有でないこと | ✅ §16.3。プロジェクト固有の記述は `LICENSE` 側に分離済 |
| steward が提出を支持または少なくとも反対しないこと | ✅ steward = 提出者本人 |

---

## 5. 主要な起草判断とその理由

| 判断 | 理由 |
|---|---|
| **§3 公有化 と §4 許諾を独立させた**（§2.4 / §4.4） | 一方を他方の *フォールバック* にすると、公有化が有効な法域では「審査対象のライセンス」が消える。OSI が審査するのは *ライセンス* なので、CC0 型の構造は審査の土台を失う。両者を独立・累積とし、公有化が有効でも §4 は「冗長だが無効ではない」と明記した |
| **§8 に特許許諾を置いた** | CC0 が OSI で止まった当の理由（第 4 条 (a) の特許不許諾）。ここを解消しないかぎり同じ議論に着地する |
| **§8.4 で特許許諾を Computational Use とその成果物まで及ぼした** | **2026-08-23 の精読で見つかった実質的な欠陥の是正**。このライセンスの 2 つの目玉（§6 の機械学習許諾 / §8 の特許非留保）が**接続していなかった** —— §1.5 が Covered Rights から特許を除外するため、§6.4 の「output は Covered Right に縛られない」は特許に届かず、§8.1 の許諾は「Work およびその派生物の製造・使用等」止まりで、**学習済みモデルや出力がそのどちらでもない可能性**がある。結果、学習した受領者は著作権では守られるが**特許で露出しうる** —— §8.3 が「その結果を生む解釈は退ける」と述べている当のことが、条文の構造として残っていた。§8.4 で Computational Use とモデル・パラメータ・出力を明示的に射程へ入れた |
| **§8.1 の派生物側の動詞を Work 側と揃えた** | 旧文は Work について「製造・製造委託・使用・販売の申出・販売・輸入・その他の移転」を列挙しながら、派生物については「製造または使用」だけだった。**派生物の頒布が特許許諾から落ちる**読みが可能で、§8.3 の解釈規範と矛盾する |
| **§8.5 で特許許諾の射程限界を明記した** | 「Dedicator が保有・支配する請求項のみ」「第三者の請求項を侵害しないという表明ではない」を §2.7 / §13.2 と結び付けた。誠実さの問題であると同時に、**過大な保証と読まれて無効化されるリスク**を下げる |
| **§12 を法域別の二段構えにした** | 日本の著作権法 59 条は著作者人格権を一身専属とし譲渡を認めない。**「放棄」一本では起草者の居住国で空振りする**。放棄が可能な法域では放棄、不能な法域では**不行使の合意**へ切り替える |
| **§12.3 で不行使合意を「本著作物のみ」に限定した** | 日本では**範囲を限定しない**包括的な人格権不行使特約を公序良俗違反として無効とする見解がある。本著作物に限定し、他の著作物に及ばないことを明記して有効性を高めた |
| **提出用 XML に `standardLicenseHeader` を置いた** | SPDX ツールは**この要素でソースファイル中の通知を照合する**。本文だけ登録して header を省くと、`SPDX-License-Identifier` タグは拾えても **§16.2 が「十分な通知」と定める散文が機械に認識されない** —— §6.5 の「自動化システムが判定できない許諾は許諾ではない」に照らして、提出物側の同じ欠落。§16.1 の通知文から**導出**し、可変部は `<alt>` で表す（§16.4 とは衝突しない —— header は Work に添える通知であって本文ではない・§16.5）|
| **§4.4 を operative にした（「§3 が有効かを You が判定する必要はない」）** | 審査で最初に来る疑念は「これは CC0 型の *献呈* であって licence ではないのでは」。旧文も「§3 の不奏功に依存しない」と述べていたが、**読者に判定を残す形**だった。§9.3（機械生成著作物の判定を負わせない）と同じ書き方へ揃え、**判定義務そのものを消した**。前文にも「3 つの根拠は列ではなく並列」を明記（§3 surrender / §4 licence / §5 covenant）|
| **§15.5 を instrument の向きへ反転した** | 旧文は「不行使は放棄ではない」という定型で、**権利を手放す instrument の中では逆向き**に働く（Dedicator の後日主張を温存すると読める）。「Dedicator の作為・不作為・沈黙は、手放した権利を復活・留保・縮小させるものと読まない」へ書き換えた |
| **§11.4 で射程の限界を明記した（データ保護 / 人格権 / 第三者の権利）** | ML 向けライセンスで実務上いちばん問われるのが「**学習データに含まれる個人情報はクリアされるのか**」。§2.7 と §13.2 の組合せで導けるが、**読者が接続しないと分からない**。学習されるための著作物はしばしば人についてのデータなので、どこで止まるかを条文で示した。**執筆中に自分で欠陥を作り、読み直して直した**: 初版は「Covered Rights と特許請求項に届き、それ以外に届かない」と書いており、**Moral Rights に届く §12 と矛盾**していた |
| **§2.8 の承継人拘束に §6 を加えた** | 旧文は §3 / §4 / §8 だけを承継人に及ぼしており、**権利が人手に渡った後に承継人が新たな TDM 留保を付けられる**と読めた。「譲受人は留保を行えない」を明記 |
| **§1.7 の列挙を §6.4 / §8.4 と揃えた** | 定義側だけ weight / embedding が欠けており、「埋め込みはmodel でも output でもない」という敵対的読みの余地があった |
| **§5.2(b) を §10.1 直指しにした** | 「Sections 3 to 12 disclaim」では**どの義務か読み手が探す**。§10.1 が categorical に述べている以上そこを指す。click-through / registration も列挙（OSD 10 対応が読み取れる形）|
| **§6.2 を §2.7 で限定した** | §8 と**同種の緊張**の是正。「誰が置いたものであれ Reservation と読まない」という絶対的な書き方は、**他の権利者の留保まで無効化すると読め**、「この Dedication は Dedicator の持つ権利にしか及ばない」(§2.7) と衝突する。§6.3 は「Dedicator にできる限りにおいて」と正しく限定しているのに、§6.2 だけがその限定を欠いていた。**instrument にできないことを宣言する条項は、審査で信頼性を落とす** —— Dedicator 自身の Covered Rights と特許請求項に射程を限定し、§2.7 / §6.3 との関係を明記した |
| **§2.8 で §3 / §4 / §8 を承継人・譲受人まで及ぼした** | **2026-08-23 の精読で見つかった非対称の是正**。§5.3（不行使の約束）と §12.4（人格権）は承継人・遺族まで及ぶと明記していたのに、**最も重要な公有化・許諾・特許許諾については沈黙**していた。この沈黙は「grant は Dedicator で止まる」という主張を招き、**権利が人手に渡った時という最も長期のリスク**を開いたままにする。§2.8 で「譲受人はこれらに服して取得する」と明記した |
| **§12.4 で不行使合意を承継人・遺族まで及ぼした** | 人格権は**著作者の死後も遺族等が行使しうる**（日本は著作権法 60 条）。起草者だけを縛る合意では、**最も長期のリスクが開いたまま**残る |
| **§12.5 で虚偽帰属を不行使の対象外にした** | 人格権が守る中核利益（氏名表示の真正）を放棄させない。これは有効性の議論を弱めるためでもあり、§11.3 と整合する |
| **§2.5 で依拠と禁反言を明文化した** | 無償の許諾は法域によって**対価が無いことを理由に撤回可能**と解されうる。§2.2 の「撤回不能」宣言だけでは弱いので、「他者が依拠して労力と費用を投じることは本 Dedication の**目的**であって単なる予見可能な結果ではない」と述べ、禁反言の適用余地を作った |
| **§2.7 で「起草者が持つ権利にしか及ばない」ことを明文化した** | §1.5 の定義上は既にそうだが、明文が無いと**持っていない権利まで許諾しているように読める**（over-claim）。第三者素材を含む著作物に適用されたとき、受領者が「全部クリアされている」と誤信する余地を潰した。§13.2（担保責任の否定）と対になる |
| **`Contribution` を定義語にした（§1.9）** | 審査対象の法文として、寄与条項が普通名詞に依存するのは不正確。「議論のためだけに送られたもの」「寄与でないと明示されたもの」を除外まで書いた |
| **§2.6 で寄与を inbound = outbound にした** | 汎用ライセンスとして他者が使う以上、第三者の寄与の権利状態が不明だと採用できない。Apache 2.0 §5 と同型だが、**受理の条件として別途の合意を要求することを禁じる**一文を足して条件ゼロの設計と整合させた |
| **§5.2 で起草者側の不作為義務を置いた** | 条件ゼロを謳っても、起草者が後から DRM や利用規約で事実上の条件を課せるなら宣言は空洞化する。**利用者への条件ではなく起草者への不作為義務**として構成したので §10.1 と矛盾しない |
| **§10.3 で「お願い」を非条件と定義した** | 「表示してくれると嬉しい」型の記述が下流で*条件*と読まれる曖昧さは実在する。請求であって条件ではないと明文化した |
| **§16.4 の本文改変制限を Work の条件から切り離した**（§10.5 / §16.5） | 識別子が一つのテキストを指し続けるには命名制限が要る。しかしそれを Work の条件にすると §10.1 と矛盾し、本文自体を ACD 下に置くと循環して制限が自壊する。**本文＝文書に対する別建ての条項**として構成した |
| **報復条項を置かなかった**（§8.2） | 条件ゼロの設計と両立しない。意図的な不在であることを明文化した |
| **準拠法・裁判管轄を定めなかった**（§15.7） | 各法域の法の下で機能させる設計。特定法域への固定は OSD 8 / SPDX の「特定性」評価にも不利 |

---

## 6. 名称について

`Autonomous Commons Dedication` は 2026-08-23 時点で既存のライセンス名と衝突しない（SPDX
License List / OSI 承認一覧のいずれにも同名・類似識別子は存在しない）。

- **Autonomous** — 本リポジトリの運用モデル（AI が人間の関与なしに無限に改善を自走する）を指す
- **Commons** — 条件ゼロで共有領域に置くこと
- **Dedication** — 法的形式（許諾ではなく献呈／公有化）

識別子 `ACD-1.0` も既存 SPDX 識別子と衝突しない。

---

## 7. 正直な弱点と、提出前にやるべきこと

**承認を保証できない。** 以下は実測に基づく弱点であり、隠さず記録する。

1. **実使用の薄さ（最大の弱点）**
   SPDX は「相当程度の実使用」を求める。現時点の使用実績は本リポジトリ 1 件のみで、
   「小規模または個人プロジェクトでのみ使われるライセンス」は提出を控えるよう明示的に
   案内されている。**対策**: 提出前に、本リポジトリでの適用を公開・安定させ、
   採用実績を積む。急いで提出するより実績を作るほうが通過率に直結する。

2. **テキストの freeze が未了**
   SPDX は「起草途中でないこと」と「収録後に改変しないという steward のコミット」を求める。
   本文は現在も改善対象であり、**提出時点で 1.0 を凍結する**必要がある。以後の改善は
   1.1 / 2.0 という別バージョンとして行い、`ACD-1.0` が指すテキストは動かさない。

3. **OSI の審査は 60 日以上かかる**
   決定日は初回提出から通常 60 日後（改訂版提出の場合は 30 日後、ただし初回から 60 日以降）。
   即答は来ない。

4. **公有化型ツールは OSI で歴史的に難しい**
   CC0 の件が示すとおり、「ライセンスではなく献呈」という形式そのものに委員会の慎重論がある。
   §2.4 / §4.4 の独立構成はこの点への直接の対処だが、議論になることは想定しておくべき。

5. **法的レビューを受けていない**
   本書は公開審査基準への機械的照合であり、弁護士の確認を経ていない。とくに §12（人格権）は
   日本法の学説状況に依存するため、提出前の専門家確認に価値がある。

---

## 8. 提出手順（人間しか行えない部分）

### SPDX License List
1. https://tools.spdx.org/app/submit_new_license/ から提出（推奨経路）。
   代替として `spdx/license-list-XML` の new license request issue テンプレート。
2. 提出前に inclusion principles を再確認し、本書 §4 の ⚠️ 3 点を解消しておく。
3. 承認要件: SPDX-legal メンバー 3 名（うち 1 名は弁護士）の同意 ＋ GitHub issue で
   コミュニティから異議が出ないこと。Fedora / Debian で既に許容され当該ディストロに
   コードが存在する場合は 2 名で可という迅速経路がある。
4. **XML は既に生成済み** —— `LICENSES/ACD-1.0.spdx.xml` をそのまま渡せる。
   本文から導出しており (`npm run spdx-xml`)、Check 445 が同期を BLOCKING 強制しているので
   **提出物が本文と食い違うことはない**。テストテキストは `LICENSES/ACD-1.0.txt` そのもの。

### OSI License Review
1. `license-review` メーリングリストへ提出。
2. 提出時に **OSD 適合（とくに OSD 3・5・6・9）を積極的に宣言**する → 本書 §3 の表を使う。
3. **既存ライセンスが埋めない gap を埋めることを示す** → 本書 §1・§2 を使う。
4. 既に使用しているプロジェクトを明示する → 本リポジトリ。
5. license steward を明示する → 横井雄太。

### 提出時に貼り付ける OSD 自己証明文 (英文・そのまま使える)

OSI は提出者に OSD 適合の積極的な宣言、とくに OSD 3・5・6・9 への言及を求める。
以下は本書 §3 の表を宣言形へ直したもの。

> I affirm that the Autonomous Commons Dedication 1.0 (ACD-1.0) conforms to the Open Source
> Definition. It imposes no condition of any kind on the recipient (section 10.1), from which
> conformance to most criteria follows directly.
>
> **OSD 3 (Derived Works)**: section 4.2 grants the right to modify and to create derivative
> and collective works, and section 4.3 states that the grant is not conditioned on reciprocal
> or compatible licensing, so derived works may be distributed under any terms.
>
> **OSD 5 (No Discrimination Against Persons or Groups)** and **OSD 6 (No Discrimination
> Against Fields of Endeavor)**: section 4.3 states expressly that the grant is not conditioned
> on field of use, on the identity, character, or purpose of the user, or on any restriction as
> to persons, groups, technologies, endeavours, or jurisdictions. Section 6.1 permits
> computational use for any purpose, commercial or non-commercial.
>
> **OSD 9 (License Must Not Restrict Other Software)**: section 10.1 imposes no requirement on
> the recipient, and section 6.4 states that no model, parameter set, weight, embedding, or
> output derived from the work is encumbered by it.
>
> **OSD 7 (Distribution of License)**: no act of acceptance is required (section 2.3), the
> covenants run with the work and may be relied upon by downstream recipients as intended
> beneficiaries (section 5.3), and the patent licence is sublicensable, transferable, and not
> terminable (section 8). The concern that led the License Review Committee to decline CC0 —
> its express non-grant of patent rights — does not arise here.
>
> The licence is in use at https://github.com/yutapr0117-design/portfolio and I am its steward.

---

## 9. 出典

- OSI License Review process — https://opensource.org/licenses/review-process
- OSI「How the OSI checks if new licenses comply with the Open Source Definition」 — https://opensource.org/blog/how-the-osi-checks-if-new-licenses-comply-with-the-open-source-definition
- SPDX license inclusion principles — https://github.com/spdx/license-list-XML/blob/main/DOCS/license-inclusion-principles.md
- SPDX new license request — https://github.com/spdx/license-list-XML/blob/main/DOCS/request-new-license.md
- CC0 の OSI 取り下げ（特許条項が争点） — http://lists.opensource.org/pipermail/license-review_lists.opensource.org/2012-February/001600.html
- Creative Commons「Introducing CC Signals」 — https://creativecommons.org/2025/06/25/introducing-cc-signals-a-new-social-contract-for-the-age-of-ai/
- EU DSM 指令 (EU) 2019/790 — https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019L0790
- 日本 著作権法 59 条（著作者人格権の一身専属性） — https://www.dinf.ne.jp/doc/japanese/access/copyright/0818_copyrightlaw/chapter02_05.html
