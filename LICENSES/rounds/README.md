---
file: LICENSES/rounds/README.md
audience: 次のセッションの実装者（一次読者）/ OSI license-discuss・license-review participants / 監査人
last-updated: 2026-09-25
canonical-ref: LICENSES/REVISION-PROTOCOL.md (§1 の ① 受領 / §3 のゲート 1) / LICENSES/ACD-1.0.discussion-log.md (分解と分類はこちら)
---

# `LICENSES/rounds/` — 受け取った本文を、そのまま置く場所

`REVISION-PROTOCOL.md` は 3 箇所でこのディレクトリを指している —— §0 の英文コミットメント、
§1 の「① 受領」、§3 のゲート 1。**にもかかわらず 2026-09-06 までディレクトリは存在しなかった。**
公開している約束が指す先が無い状態で、審査者が 5 秒で確かめられる種類の乖離だったので、
先に作った。**返信が来てから作ると、いちばん急いでいるときに置き方を決めることになる。**

## 何を置くか

**やり取りした本文そのもの。1 メッセージ 1 ファイル**（例外は規則 6）**。**

```
<YYYY-MM-DD>-<venue>[-<thread>]-<sent|<相手>-received|<相手>-observed>.txt
```

当初の規約は `<round>-<venue>-raw.md` で、**受け取った本文だけ**を想定していた。
2026-09-06 に 2 度、その想定が実態に足りないことが分かった ——
**(1)** 自分が送った本文がリポジトリのどこにも無かった（`against.md` #82）。
**(2)** やり取りは「ラウンド」ではなく**日付と相手**で識別される（同じ日に別スレッドが並走する）。
規約を実態へ合わせた。**送信も受領も同じ規則で置く** —— 記録が誤ってはならない理由は
向きによって変わらない。2026-09-09 に 3 つ目の向きを足した ——**観測**（`-observed` /
`-cites` / `-call-for-comments`）。我々宛ではないが、我々の判断を動かした本文である。
**この向きの記録を「受領」と同じ欄に混ぜると、記録が実態より良く見える** ——
だから語尾で区別する。

## 規則

1. **無改変。** 整形しない、要約しない、翻訳しない、並べ替えない、typo も直さない。
   **⚠ 第三者との private off-list correspondence だけは例外で、本文を置かず stub にする**
   （下の「例外」節）。**公開リスト由来の本文には例外は無い。**
   **ここで手を入れると、以降のすべての判断が検証不能になる**（`REVISION-PROTOCOL.md` §1 の「落とし穴」欄）。
2. **分析は書かない。** 読み・反論・分類は `ACD-1.0.discussion-log.md` へ。
   **こちらの読みは誤りうるが、何と言われたかの記録は誤ってはならない** —— だから物理的に分ける。
3. **先頭に最小限のヘッダだけ足してよい**（取得元 / 取得日 / Date / From / Subject / 一行の位置づけ）。
   本文との境界は `----- begin verbatim -----` で示す。ヘッダは受領文の一部ではない。
4. **個人名を推測で足さない。** メーリングリストのアーカイブは公開なので、**アーカイブに現れる
   とおりに**引く。現れていない属性を補わない。
5. **出典は「自分の送信控え」ではなく公開アーカイブから取る。** 送信控えは手元にしか無く、
   審査者が確かめられない。アーカイブは**配送された形**であり、読み手が実際に読むものである。
6. **証拠がスレッドの形そのものであるときに限り、1 スレッド 1 ファイルにしてよい。**
   規則 1 の「1 メッセージ 1 ファイル」は、**編集しないこと**と**どのメッセージの話かを
   曖昧にしないこと**のために在る。「誰が何時間で答えたか」「要求に対して何が返ってきたか」が
   証拠であるとき、メッセージを別ファイルへ割ると**その形自体が記録から消える**。
   条件は 3 つ —— **各メッセージがアーカイブのヘッダを完全に保っていること**、
   **ヘッダにメッセージ数と送信者を明記すること**、そして
   **束ねた結果が 1,000 行（Check 365 の BLOCKING）を越えないこと**。
   分割の代わりに束ねてよい理由は「読みやすいから」ではなく「証拠の単位がそこだから」である。

   **3 つ目は 2026-09-09 に、規則 6 を書いた当日に付いた。** 15 通のスレッドを束ねたら
   **1,581 行**になり Check 365 が BLOCKING で止めた。**そこで分かったのは、規模の問題ではなく
   一貫性の問題だった** —— 同じ日に読んだ他の大きなスレッド（Blue Oak 15 通 / Ritchey 39 通 /
   0BSD 改名 54 通）は**どれも逐語保存していない**。決定的な箇所を発言者と日付つきで
   `reviewer-positions.md` に引いてある。**`rounds/` は「我々のやり取り」と「我々を名指しした
   短い観測」のための場所**であって、第三者スレッドの丸ごとの複製ではない。
   **アーカイブは公開されており、読み手は自分で取れる。**

## いまの状態（2026-09-25 時点・106 ファイル）

| 日付 | venue | 相手 / 向き | 中身 |
|---|---|---|---|
| 2026-09-15 | **OSI のメーリングリスト CoC** | 一次資料 → 自己取得 | **我々は 2 つある CoC のうち別の方を pin していた。**リストを規律するのは `/code-of-conduct`（"Code of Conduct for OSI Mailing Lists"）で、本文はほぼ同一だが**条を引かれた相手はこちら**。**予告された AI 関連の更新は 6 日経っても起きていない**（自称更新日 2023-05-04 のまま）|
| 2026-09-15 | **リスト外（off-list）** | **送信** | **moderator の 3 問への返信。steward が自分で書いた**（本リポジトリは文面を起草していない）。**271 語・62.4 パーセンタイル** ——「長い」と言われた問いに短い文で答えている。不利な数を先に出し、貼り付け→添付の是正を自分で名指しし、**素直な読みを自分に当てて "so I will change my approach" と先に述べている** |
| 2026-09-07 〜 15 | **リスト外（off-list）** | **受領 + 送信（moderator 往復・第 3 ラウンド）** | **moderator の 5 問 → steward の回答 → 「ゲーム」の提案 → steward の長文説明（身元証拠の PDF 2 通を添付・**本リポジトリには置かない**）→ **moderator が Code of Conduct の *"Respect time and attention"* との整合と、メールの長さ・密度の実測比較を求めた**（2026-09-15）。**測定は `review-corpus.md` §1.85**、道具は `measure_list_verbosity.py` |
| 2026-09-14 | `license-review` | **観測（OpenMDW スレッド・2 通）** | **我々宛でも ACD-1.0 についてでもない。** Fontana 氏 *"The OSI does not currently have a process for **de-listing** licenses"*（配送された本体を保存）と、Piana 氏 *"revising **ALL** the approved licenses (which we have done recently), some approved licenses … leave licensing experts **scratching their heads**"*。**承認は取り消せず、承認済みに首をかしげる起草が実在すると承認する側が述べている** ——**有利・不利の両方に読める**（`review-precedents.md` §1.88）|
| 2026-09-18 | （リスト外）| **受領（moderator とのやり取り round 4・Gmail 逐語）** | **`license-discuss` への投稿が拒否された** ——**discuss 側の拒否は、これまでどこにも記録が無かった**（記録は review 側の 2 通のみ）。steward は *"content of this specific message, or … my current moderation status"* のどちらかを問い、**その問いには答えが返っていない**。**moderator が警告の根拠として引いたのは、我々が `LICENSE` に載せている開示文そのもの**（`against.md` #215）。**#214 の一次資料でもある** |
| 2026-04-06 | `license-discuss` | **観測（AI エージェントの skill のライセンス・全 3 通）** | **ACD が立つ 3 つの gap の 1 つに正面から当たる。** Fontana 氏 *"open source software licenses are extensively used for non-software material"* / *"appropriate **even in situations where copyrightability is relatively dubious**"* ——**§9 が在る理由そのものの状況**（`against.md` #211）。**⚠ 同じ 1 通が逆にも働く**（*"sufficiently creative prompts may be copyrightable"* = 境界は本当に不確か）。**主題は我々が実際に公開している資料の類型でもあり、そこを測って #212 が出た** |
| 2026-01-03 | `license-discuss` | **観測（curl ライセンスの追加・discuss 側 4 通）** | **B1 / B2 の二経路が投票の言葉で現れた唯一の例。** Piana 氏 *"**If it was a new license, I would advise to non-accept it.** But since it's a widely used and for a long time license … **proliferation concerns are moot at this point**"* / Chestek 氏「legacy category は ***a more liberal review***」。**四票が付いた上で 3 か月動かなかった** ——**全会一致の支持は決定ではない**（`against.md` #220）|
| 2026-02-04 | `license-review` | **観測（curl ライセンスの追加・review 側 7 通）** | **承認する側の投票が出た側。** 同上（`against.md` #220）|
| 2026-03-10 | `license-discuss` | **観測（OSI が承認済みライセンスの URL を SPDX 識別子へ標準化・全 6 通）** | **§16.4 / E14 に両向きで当たる。** **有利**: Fontana 氏が GPL の `-only`/`-or-later` 分割を *"a complete debacle"*、Šuklje 氏が *"the GNU license naming debacle"* と呼ぶ ——**識別子が 1 つの固定テキストを指さなくなる害の、初めての外部の証人**。**不利**: Fontana 氏 *"one level of abstraction removed from its actual application"* / Phipps 氏 *"deployment options … do not reflect the licenses that OSI has actually approved"* ——**OSI 自身の模型は 1 識別子対多形態で、§16.4 は 1 対 1 を主張する。** しかも **11 時間で方針が 1 度変わっている**（`against.md` #210）|
| 2026-05-04 | `license-review` | **観測（PHP ライセンスの自主的 retire・全 4 通）** | **承認が steward 自身の申し出で巻き戻された 1 例。** OSI が歓迎し Licensing Committee の委員が *"Kudos"* と応じ、**誰も「そういう手続きは無い」とは述べていない。** **`against.md` #146 の *"An approval cannot be undone"* を限定する**（#209）。**⚠ 有利な材料なので狭く** ——n=1・**提出者自身が手続きの不在を述べ、誰も答えていない**・retire は「承認されなかったこと」ではない・**steward が生きていることが要る（#10）** |
| 2026-08-28 | `license-review` | **観測（Luis Villa 氏 → Rob Landley 氏・volume の作法）** | **B14 の moderator 通知が引いたのと同じ CoC 条項が、その 12 日前に、AI とは無関係に、人間へ向けて引かれている。** *"concise and low-volume … The people we most need on this list are those whose time is very precious"*。**条項が在ることと、社会的に強制されていることは別で、後者の一次資料はこれが初めて**（`review-venue.md` §1.99・`against.md` #208）。**⚠ 同じ 1 通が volume を正当化する側にも働くが、それは*議論*の volume であって本文の語数（B3）ではない** |
| 2026-08-28 | `license-review` | **観測（McCoy Smith 氏 → ModelGo steward）** | **ドシエが 4 文書で引きながら、原文を持っていなかった 1 通。** *"We work on a **two-month review cycle**"* と「時計は**最終**提出から動く」の出典であり、同時に資格表示 *"[on behalf of the Licensing Committee]"* の出典でもある。**2026-09-21 に原文で確認: 角括弧は本人の署名であって我々の挿入ではない**（clean）。**⚠ ただし送信元は法律事務所のアドレス** ——アドレスの慣習と自己表示が 1 通の中で逆を向いている（`review-rules.md` §1.103）|
| 2026-08-26 | `license-discuss` | 送信 | ACD-1.0 の議論依頼（5,778 語）|
| 2026-09-14 | **OSI / REUSE の規範ページ 5 件** | 一次資料 → 自己取得 | **我々が「基準」として引いているページの、その日の姿。** review-process / 拒否理由 / OSD / OSAID / REUSE 3.3。**敵対的検証で見つかった第 3 の source class** —— アーカイブを全部取っても出てこず、**予告なく変わる**（理事会が 2 度公表を指示した項目は、この時点でまだ入っていない）。分析は `AUDIT-LEDGER.md` §6 |
| 2026-09-14 | **リスト外**（Perplexity）| レビュー → オーナー経由で受領 | **1.1 草案本文への、初めての実質的な外部レビュー。** 出自は AI レビューで、**リスト参加者でも弁護士でもなく、公開アーカイブにも無い** ——**B1 を動かさない。** **唯一の改変**: 本文中の presigned URL が AWS の資格情報を含んでいたため query string のみ伏せた（**理由は file の header に明記**。無改変規約と、資格情報を公開しない義務が衝突し、**他者を守る側を採った**）。分解は `ACD-1.0.discussion-log.md`「ラウンド 0」|
| 2026-09-13 | **OSI 理事会議事録**（`opensource.org/meeting-minutes/`）| 一次資料 → 自己取得 | **公開されている全 12 回**（2025-06-20〜2026-06-29）を**選別せずに**保存。決定の在る回だけを選ぶと、選んだこと自体を読者が検証できない。**index ページ自身が「under construction / 見つからなければ wiki を見よ」と述べており、公開分は不完全**（最古が 2025-06-20・最新が 2026-06-29）。分析は `ACD-1.0.review-corpus.md` §1.83 |
| 2026-09-03 | `license-review` | 送信 | OpenMDW-1.1 §5 の終了引き金の非対称について steward への質問 |
| 2026-09-03 | `license-review` | 送信 | MG-BY-2.0 のホスト型 Distribution と §2.2(a) の適用について |
| 2026-09-03 | `license-review` | Michael Dolan → 受領 | 上記 OpenMDW 質問への回答（名指しで応答）|
| 2026-09-04 | `license-review` | Moming Duan → 受領 | 上記 ModelGo 質問への回答（審査履歴 4 件を引用）|
| 2026-09-04 | `license-review` | 送信 | Dolan 氏の回答を受けた閾値問題の分解（返信なし）|
| 2026-09-04 | `license-review` | Shuji Sado → **引用** | 我々宛ではないが、我々の質問を明示的に引いて議論を進めている |
| 2026-09-05 | `license-review` | Ruby Anna → 受領 | ModelGo 側からの確認。**我々の 2026-09-05 12:31 送信を引用の形でのみ含む** |
| 2026-09-05 | `license-discuss` | 観測（3 通のスレッド）| 新規の単独参加者の短い質問に **約 4 時間で 1 通目**。比較対象として置く |
| 2026-09-06 | `license-discuss` | 送信 | **ACD-1.0 の 2 通目。§3 と §4 の関係だけに絞った 1 問**。本文は再送していない（凍結中・URL のみ）|
| 2026-09-06 | `license-discuss` | 送信 | **ACD-1.0 についてではない** —— 他者のネットワーク・コピーレフト質問への実質的回答（CPAL-1.0 / OSL-3.0）|
| 2026-09-07 | `license-review` | McCoy Smith → 公開の意見募集 | ModelGo 2 件への CALL FOR COMMENTS。**我々宛ではない**が、4 問はいずれも ACD-1.0 に構造上あたらない |
| 2026-09-07 | `license-review` | 観測（2 通）| Licensing Committee 委員長が CALL FOR COMMENTS に対し**まず本文を要求**している |
| 2026-09-08 | `license-review` | Moming Duan → 参照 | 上記への steward 回答。**背景資料として「Yokoi-san」を 2 度引用**（我々宛ではない）|
| 2026-09-08 | `license-review` | Preston Maness → 観測 | OpenMDW への反対。**「AI モデルに関するあらゆるライセンス」への反対**として述べられている |
| 2026-09-07 | **リスト外（off-list）** | **Nick Vidal → 受領 + 送信（往復）** | **moderator が ACD-1.0 を名指しして 5 問を出し、「ACD-1.0 に関する次の提出の前に直接返信せよ」と求めた。steward は 5 問すべてに答えた。****公開アーカイブには存在しない** —— 2026-09-10 に steward が逐語で提供したもので、**それがこの記録の唯一の根拠である** |
| 2026-09-13 | — | **第三者ページのスナップショット** | **更新前の OSI Mailing List Code of Conduct 全文**（769 語・sha256 つき）。**2026-09-09 の通知が「AI の利用を反映するよう更新する」と予告した当の文書**で、更新後は live から取得できなくなる。**「保存済み」と記録しながら 1 節の引用しか無かった**のを是正した（#82 と同じ形）|
| 2026-09-12 〜 13 | **リスト外（off-list）** | **送信 + Nick Vidal → 受領 + 送信** | **moderator 往復の続き。** steward が「**substantive な review メッセージが 2 通 moderator に拒否され、ModelGo と BOS の提出者にフィードバックが届かなかった**」と報告し、その応答と steward の返信を含む。**公開アーカイブには存在しない。** ——**この記録により「アーカイブに我々の投稿が無い」は「送っていない」を意味しなくなった**（`against.md` #136）|
| 2026-09-09 | `license-discuss` | **OSI Moderators → 観測** | **AI 生成投稿は拒否すると宣言し、両リストが「AI が自律的に参加しライセンスを起草する proof-of-concept」に使われていると名指ししている。名前は出ていない** |
| 2026-09-09 | `license-review` | **OSI Moderators → 観測** | 同文（同日 09:58・両リストへ）|
| 2026-09-09 | `license-discuss` | **Bruce Perens → 観測（上の通知への唯一の返信）** | **内容は他の投稿者の表示名についての一言のみ。誰を指した通知かは述べていない** |
| 2026-09-10 | `license-review` | **Pamela Chestek（Licensing Committee 委員長）→ 名指し** | **我々宛ではない**（OpenMDW の審査中の発言）が、*"I would like to thank **Yuta-san** for their **insightful view on the termination provision**, which I find helpful"* と**名指しで謝辞している**。**moderator 通知（2026-09-09）の翌日である** |
| 2026-09-09 | `license-review` | Max Mehl → 観測 | **同日の新規提出（PSF-2.0）**。約 270 語で、**採用実績と既承認ライセンスとの関係**に依っている |
| 2026-09-20 | （リスト外）| **ACD-1.2 草案への外部レビュー（敵対的検証）→ 受領** | **2 回目の受け渡しで初めて届いた 3 件目。** **同日の他 2 件が指摘ゼロだったのに対し、条ごとに名前のある法源・判例を挙げて攻撃ベクターを述べる**（Kneschke v. LAION / Ryanair v PR Aviation / Qimonda / 17 U.S.C. §201(b) / DMCA §1202 / 消費者契約法 8 条 / droit de retrait / 不公正契約条項指令）。**我々はこれらをオフラインで確認できていない** ——`against.md` #170 に**未検証の研究キュー**として置いた |
| 2026-09-20 | （リスト外）| **ACD-1.2 草案への外部レビュー（好意的検証）→ 受領** | オーナー経由。**PDF 原本は `Check 122` により tracked できないので、抽出テキストを sha256 つきで保存**（本ファイルは原本ではない）。**全条項を「適切」「完璧」と評価し、欠陥の指摘は 1 件も無い** ——**その読みが establish するのは文書ではなくレビューの側である**（`against.md` #168）|
| 2026-09-20 | （リスト外）| **ACD-1.2 草案への外部レビュー（条項適切性）→ 受領** | 同上。**条ごとに「適切」の判定を並べる形式。****⚠ オーナーが共有した 3 ファイルのうち 2 つは byte 同一**（sha256 一致）で、**実体は 2 件である**（#168）|
| 2026-09-19 | （リスト外）| **第三者 AI レポート① 承認プロセスの調査 → 受領** | オーナー経由。**リストの発言ではないので、証拠ではなく*測り方*として扱う** |
| 2026-09-19 | （リスト外）| **第三者 AI レポート② 敵対的検証 → 受領** | **前提に事実誤りがある** ——解析対象を `against.md` と取り違えている（`against.md` #158）|
| 2026-09-19 | （リスト外）| **第三者 AI レポート③ 好意的検証 → 受領** | **「クレヨン・ライセンス」の語を運んできた** ——アーカイブで実在を確認し、委員長の発言に到達した（`review-labels.md` §1.98）|
| 2026-09-22 | （リスト外）| **ACD-1.2 草案への外部レビュー（OSI 承認準備）→ 受領** | オーナー経由。**渡されたレビュー対象が現行 `ACD-1.2-DRAFT.txt` と sha256 一致**（`1356b2b0…`）—— **この評は現行の byte に当たっている**（09-20 の 3 件は PDF 抽出で、`against.md` #167 の破損ヘッダを含む版を読んでいた）。**確定した実欠陥 1 件**: 冒頭が「1.1 と同一」と述べたまま下に 9 件の変更が並んでいた（`against.md` #207・**4 日間偽で、09-20 の 3 件は報告していない**）。**5 条の指摘のうち §6.2 / §6.3 は、勧める分離が既に本文にある** |
| 2001-11 | `license-discuss`（観測）| **Intel's proposed BSD + Patent License → 観測保存（1of4 部）** | **特許許諾を GPL の OS に条件づけた 2001 年版が OSD 3 / 6 / 8 で争われ、承認されなかった。** 2016 年の無条件版は承認されている（`2016-01-...` を参照）。**ACD §8.2 が無条件・終了不能である理由に当たる。** |
| 2001-11 | `license-discuss`（観測）| **Intel's proposed BSD + Patent License → 観測保存（2of4 部）** | **特許許諾を GPL の OS に条件づけた 2001 年版が OSD 3 / 6 / 8 で争われ、承認されなかった。** 2016 年の無条件版は承認されている（`2016-01-...` を参照）。**ACD §8.2 が無条件・終了不能である理由に当たる。** |
| 2001-11 | `license-discuss`（観測）| **Intel's proposed BSD + Patent License → 観測保存（3of4 部）** | **特許許諾を GPL の OS に条件づけた 2001 年版が OSD 3 / 6 / 8 で争われ、承認されなかった。** 2016 年の無条件版は承認されている（`2016-01-...` を参照）。**ACD §8.2 が無条件・終了不能である理由に当たる。** |
| 2001-11 | `license-discuss`（観測）| **Intel's proposed BSD + Patent License → 観測保存（4of4 部）** | **特許許諾を GPL の OS に条件づけた 2001 年版が OSD 3 / 6 / 8 で争われ、承認されなかった。** 2016 年の無条件版は承認されている（`2016-01-...` を参照）。**ACD §8.2 が無条件・終了不能である理由に当たる。** |
| 2001-11 | `license-discuss`（観測）| **Response to comments on Intel's proposed BSD+Patent lice → 観測保存** | 上記への提出者 Intel の応答。**「BSD より多くの権利を与えるライセンスが open でないとは論理的でない」**という主張と、その反論。 |
| 2004-01 | `license-discuss`（観測）| **Public domain mistake? → 観測保存** | **promissory estoppel の 4 要件と、公開ライセンスに当てたときの反論** ——Cowan 氏「licensor は相手を知らないので要件 (2) が立たない」、Rosen 氏「estoppel は契約の法理で bare license とは無関係」。**§2.5 に直接当たる。** |
| 2004-02 | `license-discuss`（観測）| **International treatment of the public domain → 観測保存** | **Engelfriet 氏「人格権は譲渡も放棄もできず、それゆえ他の方法で真に public domain へ入ることは不可能かもしれない」** —— §3 と §12 の中核問題に当たる 2004 年の議論。 |
| 2005-04 | `license-discuss`（観測）| **Proposed new OSD item - patent termination → 観測保存（1of2 部）** | **Perens 氏「BSD には黙示の特許許諾が在る —— 自分の特許を体現するソフトを使用許諾つきで頒布すれば、その特許について estoppel を与えたことになる」**、Garrett 氏「OSD はそもそも特許許諾を要求していない」。**特許 gap の重みに直接当たる。** |
| 2005-04 | `license-discuss`（観測）| **Proposed new OSD item - patent termination → 観測保存（2of2 部）** | **Perens 氏「BSD には黙示の特許許諾が在る —— 自分の特許を体現するソフトを使用許諾つきで頒布すれば、その特許について estoppel を与えたことになる」**、Garrett 氏「OSD はそもそも特許許諾を要求していない」。**特許 gap の重みに直接当たる。** |
| 2014-05 | `license-discuss`（観測）| **Can OSI take stance that U.S. public domain is open sour → 観測保存（1of2 部）** | **当時の OSI 会長 Simon Phipps 氏が「CC0 は OSI が否決したのではなく取り下げられた」と明言**し、Fontana 氏が「CC0 は明らかに小文字の open source」、Cowan 氏が「明示的特許許諾が無いライセンスを open source でないとは誰も言えない」と述べている。**§3 の枠と特許 gap の重みの両方に当たる。** |
| 2014-05 | `license-discuss`（観測）| **Can OSI take stance that U.S. public domain is open sour → 観測保存（2of2 部）** | **当時の OSI 会長 Simon Phipps 氏が「CC0 は OSI が否決したのではなく取り下げられた」と明言**し、Fontana 氏が「CC0 は明らかに小文字の open source」、Cowan 氏が「明示的特許許諾が無いライセンスを open source でないとは誰も言えない」と述べている。**§3 の枠と特許 gap の重みの両方に当たる。** |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（1/10 部）** | **`BSD-2-Clause-Patent` の承認審査。我々の特許 gap にとって最も近い承認済みの隣人**で、**テキストの census からは出ない「承認理由の逐語」**が在る —— *"the desire of certain organizations to have a simple permissive license that is compatible with the GNU General Public License (GPL), version 2, but which also has an express patent grant included"*（提出者 McCoy Smith 氏）。**我々の理由とは違う**（#235） |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（2/10 部）** | **同じスレッドの 2/10 部。** 本文は無改変で、順に結合すれば元の連続になる |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（3/10 部）** | **同じスレッドの 3/10 部。** 本文は無改変で、順に結合すれば元の連続になる |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（4/10 部）** | **同じスレッドの 4/10 部。** 本文は無改変で、順に結合すれば元の連続になる |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（5/10 部）** | **同じスレッドの 5/10 部。** 本文は無改変で、順に結合すれば元の連続になる |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（6/10 部）** | **同じスレッドの 6/10 部。** 本文は無改変で、順に結合すれば元の連続になる |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（7/10 部）** | **同じスレッドの 7/10 部。** 本文は無改変で、順に結合すれば元の連続になる |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（8/10 部）** | **同じスレッドの 8/10 部。** 本文は無改変で、順に結合すれば元の連続になる |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（9/10 部）** | **同じスレッドの 9/10 部。** 本文は無改変で、順に結合すれば元の連続になる |
| 2016-01 | `license-review`（観測）| **BSD + Patent の承認審査 68 通 → 観測保存（10/10 部）** | **同じスレッドの 10/10 部。** 本文は無改変で、順に結合すれば元の連続になる |
| 2012-03 | `license-review`（観測）| **CC0 の OSD 適合をめぐる特許論争 69 通 → 観測保存（1/6 部）** | **我々の gap 主張が依拠している当の議論で、ドシエは一度も引いていなかった**（#233）。Rosen 氏が *"In some cases, they expressly \*exclude\* a patent grant (e.g., CC0)"* と問題を定式化し、Piana 氏が特許除外を OSD 違反として争い、**Nelson 氏が対称性の反論**（*"The BSD has no explicit patent waiver … your own logic demands that we deprecate the BSD OR that we give up on requiring patent waivers"*）を出している。**Tzeng 氏は CC0 を "first a public domain COPYRIGHT dedication with a permissive fallback" と述べており、これは ACD の §3+§4 の構造そのものである** |
| 2012-03 | `license-review`（観測）| **CC0 の OSD 適合をめぐる特許論争 69 通 → 観測保存（2/6 部）** | **同じスレッドの 2/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続になる（分割は Check 365 の 1,000 行上限のため・メッセージ境界で切ってある） |
| 2012-03 | `license-review`（観測）| **CC0 の OSD 適合をめぐる特許論争 69 通 → 観測保存（3/6 部）** | **同じスレッドの 3/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続になる（分割は Check 365 の 1,000 行上限のため・メッセージ境界で切ってある） |
| 2012-03 | `license-review`（観測）| **CC0 の OSD 適合をめぐる特許論争 69 通 → 観測保存（4/6 部）** | **同じスレッドの 4/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続になる（分割は Check 365 の 1,000 行上限のため・メッセージ境界で切ってある） |
| 2012-03 | `license-review`（観測）| **CC0 の OSD 適合をめぐる特許論争 69 通 → 観測保存（5/6 部）** | **同じスレッドの 5/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続になる（分割は Check 365 の 1,000 行上限のため・メッセージ境界で切ってある） |
| 2012-03 | `license-review`（観測）| **CC0 の OSD 適合をめぐる特許論争 69 通 → 観測保存（6/6 部）** | **同じスレッドの 6/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続になる（分割は Check 365 の 1,000 行上限のため・メッセージ境界で切ってある） |
| 2009-04 | `license-review`（観測）| **MXM Public License の承認審査 59 通 → 観測保存（1/4 部）** | **Piana 氏が 2023 年に、特許を除外した著作権のみのライセンスの先例として名指しした 3 件のうちの 1 件**（*"see discussion of CC0 or **the MXM license** or the W3C license"*）—— **そして氏自身が提出者だった**。**最も重いのは OSD の起草者本人の発言** —— Perens 氏 *"The OSD does not distinguish between copyright, **moral rights**, patents, contract restriction, or any other means of restricting what someone can do with software. **It applies equally to all of those.**"*（#244 / #245） |
| 2009-04 | `license-review`（観測）| **MXM Public License の承認審査 59 通 → 観測保存（2/4 部）** | **同じスレッドの 2/4 部。** 本文は無改変で、4 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2009-04 | `license-review`（観測）| **MXM Public License の承認審査 59 通 → 観測保存（3/4 部）** | **同じスレッドの 3/4 部。** 本文は無改変で、4 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2009-04 | `license-review`（観測）| **MXM Public License の承認審査 59 通 → 観測保存（4/4 部）** | **同じスレッドの 4/4 部。** 本文は無改変で、4 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 1999-2024 | `license-review`（観測）| **W3C Software License をめぐる 25 年分 72 通（件名で束ねたもの） → 観測保存（1/7 部）** | **Piana 氏が名指しした 3 件（CC0 / MXM / W3C）のうち唯一「承認された」もの。** W3C の弁護士 *"This is a **copyright-only license**. It makes no statement about the presence or absence of patent claims"* に Piana 氏が反対したが**保留を求めず、2017-11-29 に承認**（#246）。**2001 年には 19 か月放置された提出への OSI の答えも在る** —— Nelson 氏 *"if you want it approved, and you've submitted it and haven't heard from us, **resubmit it**."* |
| 1999-2024 | `license-review`（観測）| **W3C Software License をめぐる 25 年分 72 通（件名で束ねたもの） → 観測保存（2/7 部）** | **同じ束の 2/7 部。** 本文は無改変で、7 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 1999-2024 | `license-review`（観測）| **W3C Software License をめぐる 25 年分 72 通（件名で束ねたもの） → 観測保存（3/7 部）** | **同じ束の 3/7 部。** 本文は無改変で、7 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 1999-2024 | `license-review`（観測）| **W3C Software License をめぐる 25 年分 72 通（件名で束ねたもの） → 観測保存（4/7 部）** | **同じ束の 4/7 部。** 本文は無改変で、7 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 1999-2024 | `license-review`（観測）| **W3C Software License をめぐる 25 年分 72 通（件名で束ねたもの） → 観測保存（5/7 部）** | **同じ束の 5/7 部。** 本文は無改変で、7 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 1999-2024 | `license-review`（観測）| **W3C Software License をめぐる 25 年分 72 通（件名で束ねたもの） → 観測保存（6/7 部）** | **同じ束の 6/7 部。** 本文は無改変で、7 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 1999-2024 | `license-review`（観測）| **W3C Software License をめぐる 25 年分 72 通（件名で束ねたもの） → 観測保存（7/7 部）** | **同じ束の 7/7 部。** 本文は無改変で、7 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2009-02 | `license-review`（観測）| **IPA Font License v1.0 の承認審査 41 通（2025-09 の後日談を含む） → 観測保存（1/3 部）** | **`review-precedents.md` §1.105 が「記録に在る唯一の日本発の提出」と述べていたのは誤りで、これが 2 件目である —— しかも承認されている**（#242）。提出者は **Mori Hamada & Matsumoto の弁護士**が**IPA を代理**しており、**成功した日本の先例には弁護士が付いていた**。**Swiger 氏は "Non-reusable licenses" カテゴリへの収容を勧めたうえで承認を推している** ——**再利用の見込みの無さは却下ではなく分類で処理された** |
| 2009-02 | `license-review`（観測）| **IPA Font License v1.0 の承認審査 41 通（2025-09 の後日談を含む） → 観測保存（2/3 部）** | **同じスレッドの 2/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2009-02 | `license-review`（観測）| **IPA Font License v1.0 の承認審査 41 通（2025-09 の後日談を含む） → 観測保存（3/3 部）** | **同じスレッドの 3/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2006-07 | `license-discuss`（観測）| **Broad Institute Public License（BIPL）の承認審査 28 通 → 観測保存（1/3 部）** | **特許について、我々に有利な発言と不利な発言が同じスレッドに在る。** Rosen 氏 *"many people hope that the old BSD- and MIT-style licenses have 'implicit patent licenses,' but that's **a thin reed** ... All modern, professionally-written open source licenses ... contain explicit patent grants."* に対し、提出者側弁護士 Rivard 氏 *"The requirements for OSI certification do not include a requirement that the originator of the software offer a license to originator owned patents."*（#236 の 4 人に続く 5 人目）。**Unlicense 先例への依拠に当たるもの**も在る —— Dillard 氏 *"there are some previously approved licenses that would not be approved if submitted today"*（#238 / #239） |
| 2006-07 | `license-discuss`（観測）| **Broad Institute Public License（BIPL）の承認審査 28 通 → 観測保存（2/3 部）** | **同じスレッドの 2/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-07 | `license-discuss`（観測）| **Broad Institute Public License（BIPL）の承認審査 28 通 → 観測保存（3/3 部）** | **同じスレッドの 3/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（1/6 部）** | **Rosen 氏の、特許条項そのものに向けられた proliferation 反対** —— *"I don't think there's much enthusiasm to come up with yet another way to say these things about patents."* **ACD-1.0 §8.4 は「特許について言う、もう一つの言い方」そのものである**（#239） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（2/6 部）** | **同じスレッドの 2/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（3/6 部）** | **同じスレッドの 3/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（4/6 部）** | **同じスレッドの 4/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（5/6 部）** | **同じスレッドの 5/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（6/6 部）** | **同じスレッドの 6/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（1/11 部）** | **理事会が実際に不承認を議決した、我々の時代にいちばん近い審査。** 委員長 Chestek 氏が **CC0 が承認されていない理由**を名指しし（*"they expressly state that they do not grant a patent license. This is the reason that the CC-0 license is not an OSI-approved license ... although it has not been definitively decided due to Creative Commons' withdrawal"*）、**不承認の理由は OSD 違反ではなく主題**だった（*"open culture licenses are outside the purview of the Open Source Initiative"*）。その主題の定義は *"...an audiovisual work, a graphic work, and a model work"* で、**ACD-1.0 §1.2 の列挙は "audiovisual material" を含む**（#237 / #238） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（2/11 部）** | **同じスレッドの 2/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（3/11 部）** | **同じスレッドの 3/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（4/11 部）** | **同じスレッドの 4/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（5/11 部）** | **同じスレッドの 5/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（6/11 部）** | **同じスレッドの 6/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（7/11 部）** | **同じスレッドの 7/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（8/11 部）** | **同じスレッドの 8/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（9/11 部）** | **同じスレッドの 9/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（10/11 部）** | **同じスレッドの 10/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（11/11 部）** | **同じスレッドの 11/11 部。** 本文は無改変で、11 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |

**ACD-1.0 そのものについては、依然として受領がゼロである。** 2026-09-09 時点で
**ACD-1.0 の投稿は 2 通あり、どちらも別スレッドとして立ち、どちらにも返信が無い**
（2026-08-26 と 2026-09-06。後者は `In-Reply-To` を持たないため前者への返信として繋がっていない
—— `against.md` #90）。上の 3 件の受領は**他者の提出に対する我々の質問への回答**であって、
我々の提出への応答ではない。**この区別を落とすと記録が実態より良く見える。**

## ⚠ 例外 —— 第三者との private off-list correspondence（2026-09-23 に steward が定めた）

**公開メーリングリスト由来の本文は、これまでどおり逐語で保存する。**

**第三者との private な off-list 往復は、本文を公開せず、metadata と stub だけを残す。**
残すのは **日付 / 相手 / 向き / 分析への指し先**で、**本文は置かない。**

**理由は 2 つある。** **(1)** 相手の私信であり、公開の可否は我々が決めてよいものではない。
**(2)** それでも「やり取りが在ったこと」まで消すと**接触量を実態より小さく見せる**ことになり、
**このディレクトリが防ぐために在る失敗そのもの**になる（`against.md` #89）。

**⚠ 撤去は「復元できない」ことを意味しない。** git 履歴には残っており、
**このリポジトリは公開済みの履歴を書き換えない。** 変わったのは提示するものだけである。

**⚠ 費用**: その本文に依拠していた逐語引用は、**リポジトリ内では検証できなくなる**
（`verify_dossier_quotations.py` が未確認として挙げる）。
**読み手が我々を信用せずに確かめられる量の、実際の減少である**（`against.md` #217）。

**現在この例外が適用されている file**: `*-offlist-nick-vidal-*.txt`（5 件）。

## なぜ raw を残すのか

次の venue（`license-review`）へ進むとき、**前段で何が起きたかを示せるかどうかで受け取られ方が
変わる**。示せなければ、提出は「前の議論を無視してもう一度出してきた」ように見える。
そのとき示す材料は、要約ではなく**原文**である必要がある —— 要約の正しさは、原文が在って初めて
確かめられる。
