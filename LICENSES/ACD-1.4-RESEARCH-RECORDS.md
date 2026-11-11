---
file: LICENSES/ACD-1.4-RESEARCH-RECORDS.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-12
canonical-ref: LICENSES/ACD-1.4-CHANGELIST.md (1.4 の変更の記録・この file の節はもとはそこに在った) / LICENSES/ACD-1.4-DRAFT.txt (当てた対象)
---

# ACD-1.4 の作業で外部資料を当てた記録（2026-10-28）

`ACD-1.4-CHANGELIST.md` がバイトの予算の advisory（200,000）を超えたので、2026-11-12 に、どの Check も読んでいない 2026-10-28 の調査記録 4 節をここへ移した。**本文は無改変**で、節の見出しも元のままである。節の中の「上の表」「下の表」は、移す前の `ACD-1.4-CHANGELIST.md` の主表を指す。

## 外部資料 5 本を当てた結果（2026-10-28・オーナーが URL を渡した・clean も書き残す）

5 本とも全文を取得した（Osler は本家が 403 を返したため Wayback の 2025 年版）。1 本ずつ条に当て、**本文を変えたのは上の表の 3 件だけ**。

| 資料 | 条文に当てて分かったこと | 扱い |
| :-- | :-- | :-- |
| OSI ブログ "Opening New Paths for Open Source"（2026-10-19・会員向けニュースレター） | EU 委員会が AI と著作権（TDM を含む）について意見募集をしている。§1.10 は Directive 2019/790 第 4 条 3 項を名指すが、§15.5 が「法令の改正・置換を含む」と述べるので、改正されても参照は壊れない。curl ライセンスの承認はドシエ側の事実で、本文には関係しない | 本文は変えない |
| OSI のメディア掲載ページ（The New Stack・2026-10-09） | OSI は 2 年のフェローシップで OSAID の改訂を検討する | **本文は OSAID を参照しない**（改訂されても条文の意味が動かない）。これを理由に、今回も参照を入れない |
| OSI ブログ "OSI brings the State of the Source to All Things Open 2026"（2026-09-10） | Licensing 101 は審査手続き・OSD・OSAID を扱う。Toscano 氏のセッションは AI に関わるライセンスの実証データを扱う。録画は「後日公開」 | 録画が出たら当て直す（監視は `OSI-EVENTS-2026-10.md`） |
| Osler（2024・OSAID RC1 の解説） | 改変に適した形 = データ情報・コード・パラメータ（重みと設定を含む）。訓練データそのものは求めない。データには著作権・個人情報の制約がある | §1.3（上の表）。データの制約は §2.7 / §11.4 が既に「この本文が与えられないもの」として述べている |
| Moesif（2026-05・OSAID 1.0 の実務解説） | 4 つの自由。「出力を変えることを含む改変」。ライセンスは**利用分野・下流の利用者数・出力**のいずれも制限してはならない。AUP は公開後に改訂される | §4.3 / §5.2(b)（上の表）。出力については §6.4 が既に「何の請求も生じない」と述べる —— **これは Chestek 氏の「出力に触れる価値は無い」（`against.md` #133）への、OSAID 本文に由来する反対側の材料**である（OSAID 1.0 の自由の定義が出力の改変を名指している）。ただし Moesif は OSI ではなく、承認基準は OSD であって OSAID ではない |

**採らなかったもの（理由つき）**:

- **トークナイザ等を §1.7 / §6.4 / §8.4 の列挙に足すこと** —— 学習から生じる成果物は「output」に含まれる読みが通り、§15.1 が広い読みを取るよう求める。4 箇所の列挙を伸ばす費用（B3）に見合う差が無い。
- **「この本文を重みに付けても、それだけで Open Source AI にはならない」と本文に書くこと** —— オープンウォッシングの懸念（The New Stack・Moesif）は本物だが、OSAID が求めるのは**資料一式の公開**であってライセンスの文言ではない。他の定義の充足を本文で論じると、その定義が改訂されるたびに本文が古くなる。ドシエ（`SUBMISSION-MATERIALS.md`）で述べる。
- **EU AI Act の open-source 例外（Moesif・Osler）に合わせた文言** —— 例外の要件はアクセス・利用・改変・頒布を許すことで、§4 / §6 / §8 は既に全部許す。法令の要件を本文へ写すと、法令が動くたびに本文が古くなる。

**⚠ 逆側**: 3 件の変更はどれも「既に排除していたものを名指した」だけで、受領者の権利は 1 つも増えていない。それでも語数は 24 増え（5478 → 5502）、長さ（B3）は悪化する方向にしか動いていない。採った理由は、比較する読み手が探す場所に答えを置くことが入口の短さ（B13）と同じ方向に効くからだが、**この判断が B3 との取引であることは変わらない**。

## OSAID 1.0 の原文と日本語参考訳を当てた結果（2026-10-28・オーナーが URL を渡した）

3 本とも全文を取得した: OSI の OSAID 1.0 原文 / オープンソース・グループ・ジャパン（OSGJ）の日本語参考訳 / OSGJ の支持表明（2024-10-29）。**上の 5 本（解説記事）より重い一次資料**で、§1.3 の行が解説記事から引いていた「コード・パラメータ・データ情報」は**原文でも同じ 3 要素**であることを確かめた。本文を変えたのは §9.1 の 1 件だけ。

| 原文の要素 | ACD での位置 | 扱い |
| :-- | :-- | :-- |
| 4 つの自由（使用・研究・改変・共有）。使用は *"without having to ask for permission"*、改変は *"including to change its output"* | §4.1〜§4.3 / §2.3（受諾不要）/ §6.4（出力に何の請求も生じない） | 本文は変えない。**改変の自由が出力の変更を名指している**ことは、Chestek 氏の「出力に触れる価値は無い」（`against.md` #133）への反対側の材料として、解説記事ではなく**原文から**引けるようになった。⚠ ただし承認の基準は OSD で、OSAID ではない |
| 自由は *"a fully functional system and … discrete elements"* の両方に及ぶ | §2.1（全体と分離できる各部分） | 本文は変えない |
| 改変に適した形 = データ情報・コード・パラメータ。**コードは "OSI-approved licenses"、データ情報とパラメータは "OSI-approved terms"** | §1.3（コード・文書・データ・パラメータを名指す・1.4 で追加） | **ACD が承認されれば 3 要素すべてに使える 1 本の文書になる**。⚠ 逆側: 3 要素を 1 本で覆うことは Fontana 氏の「1 本で全部」批判（`against.md` #266）の形に当たる。#266 は「素材固有の条がどれも義務を外す側にしか働かない」ので当たらないと結論しており、その結論は変わらない |
| パラメータの例として「中間チェックポイント」「最終的なオプティマイザの状態」 | §1.3 の列挙は例示（§15.5）。学習から生じたものは §1.7 / §6.4 / §8.4 の "parameter set … or output" | 本文は変えない（列挙を 4 箇所で伸ばす費用に見合わない） |
| 改変版を同じ条件で出すよう求める条件（コピーレフト）は許される | §4.5 / §10.1（ACD は課さない） | 本文は変えない。OSAID はコピーレフトを**許す**のであって求めないので、条件ゼロと矛盾しない |
| 法的な仕組みを特定しない —— パラメータは *"free by their nature"* でありうる | §9（権利が生じていてもいなくても働く）/ §3〜§5 の 3 本の足 | **§9.1 を変えた（上の表）**。gap 3（機械生成物）が OSAID の開いたままの問いに直接答えていることの、原文に依る裏づけ。⚠ 逆側: OSAID が開いているのは OSAID についての問いで、license-review の承認基準ではない。「公有化の献呈は単体では承認されない」という OSI の立場（§3 と §4 の並置の理由）は変わらない |
| 「AI システム」「機械学習」の定義を OECD から借りる | ACD は "machine learning model" を定義しない（§1.7 が「あらゆる自動処理」で範囲を決めている） | **定義を足さない**。範囲は §1.7 の広い定義が決め、未定義の語は包含の列挙の中にしか出てこない。OECD の定義は改訂されうるので、本文に写すとそのたびに古くなる |
| OSGJ（理事長 佐渡秀治氏）が OSAID 1.0 を支持し、日本語参考訳を公開 | §15.4（英語が正文・翻訳は便宜） | 本文は変えない。ドシエ側の事実: **佐渡氏は OSAID を支持し、同時に AI-MIT の条件に反対した参加者の 1 人**（`AS-OF.md` の「nearest contemporary comparator」行）。条件を足した AI 向けライセンスへの反対と、OSAID の支持は両立している —— 条件ゼロの ACD はその両方と矛盾しない。⚠ 佐渡氏が ACD について何かを述べたわけではない |

**⚠ 逆側（全体）**: 今回の 1 件も「既に該当していたものを名指した」だけで、受領者の権利は増えていない。語数は 5502 → 5514 で、B3 はさらに悪化した。

## OSAID 1.0 への照合（2026-10-28・オーナー依頼「改定後のルールに合わせた ACD-1.4 に」）

オーナーに確かめたところ「改定後のルール」は **OSAID 1.0** を指す。あわせて OSI の他のルールも原典で取り直し、**review-process（最終更新 2024-03-13）・OSD（2024-02-16）・行動規範 2 ページ（2023 年）はどれも改定されていない**ことを確かめた。

OSAID の要件を 1 つずつ条文に当てた。**OSAID が定めるものには 2 種類ある** —— (a) 適用する**条件（terms）**が与えるべき自由と、(b) **公開の仕方**（改変に適した形を公開すること）。(b) をライセンスが義務づければ条件になり、§10.1 に反する。ACD が担うのは (a) で、(b) は ACD を使う人が公開のときに満たす。

| OSAID 1.0 の要件 | 種類 | ACD-1.4 の対応 | 判定 |
| :-- | :-- | :-- | :-- |
| 使用: あらゆる目的で、許可を求めずに | 条件 | §4.1（あらゆる目的）/ §4.3（条件なし）/ §2.3（受諾・通知不要）/ §10.3（要望は条件ではない） | 満たす |
| 研究: 仕組みを研究し、構成要素を検査する | 条件 | §4.1 / **§4.2（1.4 で名指し）** / §1.7（解析）/ §5.2(a)（技術的保護手段を使わない） | **名指しが欠けていたので足した** |
| 改変: あらゆる目的で、出力の変更を含む | 条件 | §4.2（改変・翻案）/ §6.4（モデルと出力に何の請求も生じない） | 満たす |
| 共有: 改変の有無を問わず、あらゆる目的で | 条件 | §4.2（頒布・サブライセンス）/ §4.5（どんな条件でも再頒布できる） | 満たす |
| 自由はシステム全体と個別の要素の両方に及ぶ | 条件 | §2.1（全体と分離できる各部分） | 満たす |
| コードは「OSI 承認ライセンス」 | 条件 | §1.3（source code / object code）。§4 が licence を与えるので「ライセンス」に当たる | **OSI に承認されて初めて満たす**（いまは承認されていない） |
| データ情報は「OSI 承認の terms」 | 条件 | §1.3（documentation / data / metadata） | 同上 |
| パラメータは「OSI 承認の terms」 | 条件 | §1.3（1.4 で名指し）/ §9（権利が生じていてもいなくても働く・1.4 で名指し） | 同上 |
| コピーレフト条件は許される | 条件 | ACD は課さない（§10.1）。許されるのであって求められない | 矛盾しない |
| 法的な仕組みを特定しない（パラメータは本来自由でありうる） | 条件 | §3〜§5 の 3 本の足 / §9 | 合う |
| 改変に適した形（データ情報・コード・パラメータ）の公開 | 公開の仕方 | ACD は公開を求めない（§10.2）。求めれば条件になる | **ACD の役割ではない**。ACD を付けた人が公開時に満たす |
| データ情報に訓練データの出所・入手先の一覧を含める | 公開の仕方 | §11.2（Work が何で、どこから来て、誰が作ったかを述べてよい）が、ACD の Work を訓練データとして一覧に挙げることを妨げない | 妨げない |
| 共有できないデータ（個人データ等）も説明する | 公開の仕方 | §11.4（個人データ等の許諾は ACD の範囲外）/ §2.7 | 妨げない（範囲外であることを本文が明示） |

**結論**: 条件側の要件で欠けていたのは **§4.2 の名指し 1 件**だけで、直した。残る「OSI 承認の terms / licenses」は、ACD が承認されることでしか満たせない。

**⚠ 逆側**:
- **OSAID は承認の基準ではない**。license-review が当てるのは OSD で、OSAID に合っていることは承認に何も足さない。照合の価値は「AI 向けとして出すライセンスが、OSI 自身の AI の定義と食い違っていない」と示せることに限られる。
- **ACD を付けただけでは OSAID を満たさない**。データ情報とコードを公開しない重みの公開は、ACD の下でも OSAID の意味の Open Source AI にはならない。この区別は本文には書かず（他の定義の充足を本文で論じると改訂のたびに古くなる）、`SUBMISSION-MATERIALS.md` に置く。
- 1.4 の OSAID 関連の変更 5 件（§1.3 / §4.2 / §4.3 / §5.2(b) / §9.1）は**どれも既に及んでいたものの名指し**で、語数は 5478 → 5519（+41）。B3 を悪化させた分は、比較する読み手が探す場所に答えを置いた分とのトレードオフである。

## opensource.org の全ページを読み直した結果（2026-10-28・オーナー依頼）

**取得**: sitemap の 1,228 ページに、sitemap に無い個別ライセンスのページ（127）と理事会議事録の全回（84）を足し、**1,439 ページ・本文約 129 万語**を取得した（失敗は 403 のお問い合わせページ 1 件）。**ドシエが URL で引いていたのはこのうち数十ページ**で、ブログは 955 本中 9 本、議事録は 84 回中 12 回だった。

**読み方（全部を逐語で読んだわけではない）**: (1) 規範的なページ（AI の FAQ・チェックリスト・open weights・AI 政策・商標ガイドライン・do-not-use・authority・proliferation report）は全文を読んだ。(2) ブログ 955 本は ACD に関わる語（public domain / dedication / CC0 / patent / TDM / moral rights / 機械生成 / proliferation / license review / weights）で点数を付け、上位とドシエ未引用のものから全文を読んだ。(3) 議事録はドシエが日付で参照していない回から、ライセンス・承認・OSAID に触れる行を全回分抜き出した。**点数の低いブログの大半（イベント告知・会員向けの話題）は本文を読んでいない。**

**本文を変える新しい欠陥は 0 件**。根拠の差し替えが 1 件（上の表の §4.3 を Moesif から OSI の一次資料へ）。ドシエが一度も引いていなかった一次資料のうち、効くものは次のとおり:

| 資料 | 何と言っているか（逐語） | ACD への当たり |
| :-- | :-- | :-- |
| OSI ブログ "Public Domain Is Not Open Source"（2017-07・OSI Policy Team） | *"A solution would be to create a form of words … disclaim ownership for the jurisdictions where that is possible, and then grant a copyright license that has the same practical effect as a public domain dedication for jurisdictions where ownership of copyright can never be disclaimed."* CC0 は *"withdrew it from the approval process during a complex discussion about patent rights"* | **§3 + §4 の設計を、OSI 自身の公式の場が「解決策」として書いていた**。CC0 が止まった理由も特許で、§8 が扱う点。⚠ **逆側**: 記事の形は「公有化できない法域では代わりに許諾」という**代替**で、ACD の §4.4 は**並置**（代替ではない）。記事の形をそのまま採ったのは CC0 で、ACD はそこから意図的に外れている。記事は *"I'm not a lawyer"* と断っており、理事会の決定でもない |
| OSI ブログ "Patents and Open Source"（2025-12・McCoy Smith 氏） | CC0 §4(a) の特許の全面除外は *"was thought to potentially run afoul of at least OSD 7"*、*"Subsequent OSI license approval submissions with similar comprehensive patent license disclaimers have been similarly rejected."* 明示の許諾については *"The Benefits of Explicitness"* | **§8.1 / §8.3 / §8.4 の存在理由を、審査委員会の委員が OSI の公式な場で述べている**。`SUBMISSION-MATERIALS.md` の OSD 7 の行の根拠を強める。⚠ **逆側**: 同じ記事は Apache-2.0 の防御的終了条項を *"a form of mutual patent peace"* と肯定的に書いている。ACD はそれを持たない（§8.2・B7）ので、この記事を引けば防御条項が無いことも同じ記事から問われうる |
| OSI ブログ "License Consistency Working Group begins license review"（2023-10・Berkus 氏・理事） | *"provisions like patent grants have been shown to be necessary"* / *"We've also learned the value of non-proliferation."* | 特許許諾の必要性（§8）を理事が述べた一次資料。**同じ文が非増殖の価値も述べる** —— vanity / 重複の批判（#84・B2）は同じ源から来る |
| OSAID FAQ（`opensource.org/ai/faq`） | パラメータについて *"we require an explicit assertion accompanying the distribution of Parameters that assures that they are freely available to all"*。*"to be approved by the OSI, the terms for parameters must assure the freedom to use, study, modify and share"*。パブリックドメインについて *"the definition of public domain varies from country to country"* | (1) §16.1 の通知（*"No rights in this work are reserved and no conditions are imposed"*）は、権利が生じていなくても機能する**明示の表明**に当たる。(2) **OSI がパラメータの条件を承認する前提で書いている** —— 主題の適格性（B15）への反対側の材料。(3) §4.4（§3 の有効性を受領者が判断しなくてよい）の理由を OSI 自身が述べている。⚠ **逆側**: FAQ は OSAID の説明であって審査基準ではない |
| OSAID チェックリストの脚注 | *"Available under OSI-approved terms means that the OSI will review licenses and agreements to ensure that all materials are available under terms that conform with the Open Source Definition."* | データとパラメータの条件も **OSD で**審査される。ACD を OSD で審査してもらう経路（`license-review`）は、OSAID の 3 要素すべてに効く |
| 理事会議事録 2025-02-21 | Chestek 氏 *"We got the first AI licenses submitted for review to the License Committee."* | AI 向けライセンスの審査は 2025 年に始まったばかり。ACD はその初期の一群に入る |
| 理事会議事録 2023-03-17 | 準拠法条項について審査委員会が指針を起草し公開するよう提案 | **公開された指針は見つからなかった**（全 1,439 ページを検索）。§15.3（準拠法を置かない）について、委員会の公式な指針は無いまま。理事会は承認の告知で「必要でも望ましくもない」と述べている（`against.md` #254） |
| OSI ブログ "Why OSI License Approval Matters"（2017） | *"Others … are not entitled to assert that a non-approved license satisfies the OSD."* | **公開面を点検して clean**: `LICENSE`・README・`llms.txt` はいずれも「OSI 承認ではない」と明記し、OSD 適合を言い切っていない。提出の場で OSD 適合を明言するのは手続きが求めることで、これとは別 |
| 商標ガイドライン（`about/brand-and-trademark-guidelines`） | 「OSI Approved Open Source License」は登録商標。承認を示唆する使い方の禁止 | 同上の点検で clean。**承認後**に表示を変えるときは、このページの書き方（® と帰属表示）に従う |
| 2008 年の理事会ブログ "(Too-)Simple licenses" | *"Why not simply put your code into the public domain? Clearly, people license code because they want to put conditions on the distribution of the code."* | **逆側の材料**: 条件を課さないならライセンスの形を取る理由は何か、という古い問い。ACD の答えは 2017 年の記事と同じ（公有化は国ごとに確実でない）で、§4.4 の並置はそのため |

**⚠ 逆側（全体）**: 今回出たものの大半は**ACD に有利な一次資料**で、その偏りそのものを疑う必要がある。点数づけの語（public domain / patent / CC0）は ACD が答えている論点の語なので、**ACD が答えていない論点（長さ・採用実績・法的レビュー）を扱うページは点数が低くなる**。その種の論点は既に list のアーカイブ側で厚く記録されている（B1 / B2 / B3）ので、今回の読み直しで弱点が減ったわけではない。
