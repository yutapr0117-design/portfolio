---
file: LICENSES/rounds/README.md
audience: 次のセッションの実装者（一次読者）/ OSI license-discuss・license-review participants / 監査人
last-updated: 2026-11-07
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

## いまの状態（件数は書かない —— Check 465 の OK 行が実測を出す・`ls LICENSES/rounds | grep -vc README`）

| 日付 | venue | 相手 / 向き | 中身 |
|---|---|---|---|
| 2002〜2005 | `license-discuss` | **観測（著作権を伴わない特許の許諾と、標準の特許方針・3 通）** | `2002-to-2005-license-discuss-standalone-patent-licences-observed.txt` |
| 2012-02 | `license-review` | **観測（CC0 の審査から、特許について述べた 7 通）** | `2012-02-license-review-cc0-submission-patent-statements-observed.txt` |
| 2013-10〜12 | `license-review` | **観測（Tidepool Open Access to Health Data Software License の審査から 13 通・2 部の 1）** | `2013-10-to-12-license-review-tidepool-health-data-observed-1of2.txt` |
| 2013-11 | `license-discuss` | **観測（Rosen 氏の 1 通・OSL と AFL は版を重ねて承認された）** | `2013-11-license-discuss-osl-afl-rosen-iterations-observed.txt` |
| 2013-11 | `license-review` | **観測（Berkus 氏の 1 通・提出者は理事会の過半数に、オープンソース・法的に有効・必要の 3 つを立証する）** | `2013-11-license-review-sfsl-berkus-burden-three-observed.txt` |
| 2013-11 | `license-discuss` | **観測（Rosen 氏の 1 通・FOSS の許諾は永遠、旧版を勧めなくても配った物は変わらない）** | `2013-11-license-discuss-osl-afl-rosen-forever-observed.txt` |
| 2013-10〜12 | `license-review` | **観測（同・2 部の 2。取り下げの通と、同じ報告のスレッドの NOSA 2.0 についての 1 通を含む）** | `2013-10-to-12-license-review-tidepool-health-data-observed-2of2.txt` |
| 2008-07〜09 | `license-review` / `license-discuss` | **観測（MirOS Licence の審査と、承認を勧めた 2008-09 の委員会報告・8 通）** | `2008-07-to-09-license-review-miros-licence-approval-observed.txt` |
| 2005-09 | `license-discuss` | **観測（2005 年 9 月の委員会報告・改訂版・理事会の対応と返信。3 つの基準をめぐる 9 通）** | `2005-09-license-discuss-committee-report-three-criteria-observed.txt` |
| 2009-01 / 2012-02 | `license-review` | **観測（CC0 の審査の手続きの枝と TGPPL の枝から 4 通）** | `2009-to-2012-license-review-cc0-process-and-tgppl-branches-observed.txt` |
| 2005-03 | `license-discuss` | **観測（委員長が 3 つの基準を提案したスレッドから 11 通）** | `2005-03-license-discuss-three-proposed-osd-terms-observed.txt` |
| 2007-07〜08 | `license-discuss` | **観測（2007 年 7 月の委員会報告と、承認の手続きをめぐる枝から 6 通）** | `2007-07-to-08-license-discuss-committee-report-and-approval-process-observed.txt` |
| 2009-09〜11 | `license-review` | **観測（2009 年 9 月の委員会報告と Falcon の審査から 6 通）** | `2009-09-to-11-license-review-committee-report-and-falcon-observed.txt` |
| 2009-11 | `license-review` | **観測（Piana 氏・起草の質と OSD 適合を分ける・1 通）** | `2009-11-license-review-piana-blackbox-drafting-vs-osd-observed.txt` |
| 2007-09 | `license-discuss` | **観測（2007 年 8 月分の委員会報告と理事会の対応・オープンソースハードウェアを範囲に入れた答えを含む 4 通）** | `2007-09-license-discuss-committee-report-august-and-board-remit-observed.txt` |
| 2026-03 / 2026-08 | `license-review` | **観測（本文を AI が書いたことは問題か —— AI-MIT の審査の 4 通と、承認が AI の著作権訴訟で引かれる懸念 —— OpenMDW の審査の 1 通）** | `2026-03-and-08-license-review-ai-drafting-and-endorsement-observed.txt` |
| 2018-11 | `license-review` | **観測（SSPL の審査で Kuhn 氏が起草の時間について書いた 2 通）** | `2018-11-license-review-kuhn-sspl-drafting-time-observed.txt` |
| 2004-01 / 2019-10 / 2026-09 | `license-discuss` / `license-review` | **観測（禁反言と bare license・Rosen 氏、本文の外の説明・Chestek 氏の 3 通）** | `2004-to-2026-license-lists-bare-licence-and-extrinsic-statements-observed.txt` |
| 2004-06 / 2004-08 / 2009-11 | `license-discuss` / `license-review` | **観測（ECL の 2004 年の審査から 4 通と、2009 年 12 月分の委員会報告）** | `2004-to-2009-license-lists-ecl-and-committee-report-december-2009-observed.txt` |
| 2008-11 | `license-review` | **観測（SIL Open Font License 1.1 の審査から 5 通・フォントをソフトウェアとして扱う読み、ハードウェアについての当時の扱い）** | `2008-11-license-review-sil-open-font-license-observed.txt` |
| 2012-04〜05 | `license-review` | **観測（CeCILL v2.1 の審査から 3 通・権利の総称、2 つの正本、既存のもので足りるか）** | `2012-04-to-05-license-review-cecill-2-1-observed.txt` |
| 2012-05 | `license-review` | **観測（Fontana 氏の 1 通・なぜ CC0 を使わないのか）** | `2012-05-license-review-svoboda-fontana-why-not-cc0-observed.txt` |
| 2012-05 | `license-review` | **観測（Perens 氏の 1 通・短い公有の文は crayon license）** | `2012-05-license-review-svoboda-perens-crayon-observed.txt` |
| 2012-05 | `license-review` | **観測（Callaway 氏の 1 通・CC0 が長いのは徹底しているから）** | `2012-05-license-review-svoboda-callaway-cc0-thorough-observed.txt` |
| 2012-05 | `license-review` | **観測（Callaway 氏の 1 通・既存で解けない問題を述べることを提出の必須の前提に）** | `2012-05-license-review-svoboda-callaway-state-the-problem-observed.txt` |
| 2012-05 | `license-review` | **観測（Nelson 氏の 1 通・CC0 が長いのは世界中で確実に手放すため、承認されないのは特許のため）** | `2012-05-license-review-svoboda-nelson-cc0-length-observed.txt` |
| 2005-09 | `license-discuss` | **観測（"License Proliferation" から 5 通・OSD に適合するものを全部か良いものだけか、理事が述べた 3 つの基準の使い方）** | `2005-09-license-discuss-license-proliferation-observed.txt` |
| 2012-06 | `license-discuss` | **観測（OSI のライセンスのページの見せ方の提案から 4 通・承認しない方針は正式に定められていないという理事の理解と、それと並ぶ理解）** | `2012-06-license-discuss-licensing-pages-proposal-observed.txt` |
| 2015-09〜11 | `license-review` | **観測（OSET Public License の審査から 6 通・審査の 4 つの問い、提出者の名の外し、承認）** | `2015-09-to-11-license-review-oset-public-license-observed.txt` |
| 2015-09 | `license-discuss` | **観測（Rosen 氏の 1 通・オープンソースのライセンスは裸の約束ではない、対価はあふれている）** | `2015-09-license-discuss-violations-rosen-consideration-abounds-observed.txt` |
| 2015-09 | `license-review` | **観測（Berkus 氏の 1 通・既にそうなら条は要らず、そうでないなら条は悪い）** | `2015-09-license-review-oset-ns-berkus-not-needed-observed.txt` |
| 2015-09 | `license-review` | **観測（Fontana 氏の 1 通・OSD に合っても OSI が承認するとは考えられないライセンスがある）** | `2015-09-license-review-oset-ns-fontana-inconceivable-observed.txt` |
| 2002-08 | `license-discuss` | **観測（"Legal soundness comes to open source distribution" から 4 通・契約でないライセンスと保証の否認、AFL の承認）** | `2002-08-license-discuss-legal-soundness-observed.txt` |
| 2002-08 | `license-discuss` | **観測（Rosen 氏の 1 通・切り離しの条で利用者に写しの破棄を求めるのは苛酷）** | `2002-08-license-discuss-rpsl-rosen-severability-harsh-observed.txt` |
| 2002-08 | `license-discuss` | **観測（"why does allowing click-through licenses …" から 1 通・Behlendorf 氏 2002-08-06）** | `2002-08-license-discuss-click-through-behlendorf-ignore-observed.txt` |
| 2014-04 | `license-discuss` | **観測（"why standard licenses" の FAQ の下書きから 4 通・承認は受け入れの床か信頼か）** | `2014-04-license-discuss-why-standard-licenses-observed.txt` |
| 2015-05・08 | `license-discuss` | **観測（Apache の第三者ライセンス方針の 2 件名から 7 通・下流の一覧は各組織が決める、opensource.org からの返信）** | `2015-05-and-08-license-discuss-apache-third-party-policy-observed.txt` |
| 2007-04 | `license-discuss` | **観測（"License Proliferation Dissatisfaction" から 5 通・分類の採択、理事会が何を却下するか、承認を閉じる案）** | `2007-04-license-discuss-license-proliferation-dissatisfaction-observed.txt` |
| 2007-06 | `license-discuss` | **観測（Phipps 氏・準拠法は名前空間の宣言・1 通）** | `2007-06-license-discuss-phipps-choice-of-law-namespace-observed.txt` |
| 2007-06 | `license-discuss` | **観測（Phipps 氏・準拠法が使うたびに変わる・1 通）** | `2007-06-license-discuss-phipps-law-varying-by-use-observed.txt` |
| 2007-06 | `license-discuss` | **観測（DiBona 氏・新しいライセンスは混乱を増やす・1 通）** | `2007-06-license-discuss-dibona-every-new-licence-confusion-observed.txt` |
| 2007-06 | `license-discuss` | **観測（Phipps 氏・法体系は書くか何も書かないか・1 通）** | `2007-06-license-discuss-phipps-fixed-law-or-none-observed.txt` |
| 2007-04 | `license-discuss` | **観測（Rosen 氏・承認の指針は独自性の証明・1 通）** | `2007-04-license-discuss-rosen-uniqueness-observed.txt` |
| 2019-08 | `license-discuss` | **観測（"For Public Comment: The Libre Source License" から 4 通・個人の起草者に示された順序、list に出すことの適否）** | `2019-08-license-discuss-libre-source-license-observed.txt` |
| 2019-12 | `license-review` | **観測（Piana 氏の 1 通・正本の言語は 1 つに）** | `2019-12-license-review-mulan-psl-piana-one-authoritative-version-observed.txt` |
| 2019-12 | `license-review` | **観測（提出者の 1 通・正本を 1 つにする文を v2 で足した）** | `2019-12-license-review-mulan-psl-v2-chinese-prevails-observed.txt` |
| 2019-12 | `license-review` | **観測（Piana 氏の 1 通・訳の不具合で同名の別のライセンスが生まれる）** | `2019-12-license-review-mulan-psl-piana-translation-glitch-observed.txt` |
| 2020-01 | `license-review` | **観測（Smith 氏の 1 通・bare license で party の語を使う危うさ）** | `2020-01-license-review-mulan-psl-smith-party-bare-license-observed.txt` |
| 2008-03・2012-04 | `license-discuss`・`license-review` | **観測（公有化の 2 スレッドから 7 通・公有のソフトウェアは open source か、FAQ の公有化と CC0 の答えの受け取られ方）** | `2008-03-and-2012-04-license-lists-public-domain-faq-observed.txt` |
| 2015-10 | `license-discuss` | **観測（"Short permissive no attribution required open source license" から 4 通・公有化の献呈と帰属を求めない fallback の提案、「十分すぎるほど在る」）** | `2015-10-license-discuss-short-permissive-no-attribution-observed.txt` |
| 2015-10 | `license-review` | **観測（"License Committee Report" から 1 通・Fontana 氏 2015-10-13・出所の記録）** | `2015-10-license-review-committee-report-fontana-provenance-observed.txt` |
| 2015-10 | `license-discuss` | **観測（Woolley 氏の 1 通・献呈は欧州では不可能、米国でも疑いがある）** | `2015-10-license-discuss-bsd3-woolley-pd-europe-observed.txt` |
| 2015-10 | `license-discuss` | **観測（Moen 氏の 1 通・献呈が効かない所で働く許諾が CC0 を隙の無いものにし、その代わりに長くした）** | `2015-10-license-discuss-bsd3-moen-cc0-airtight-observed.txt` |
| 2006-03 | `license-discuss` | **観測（"Looking for license stewards" から 1 通・連絡の取れない steward の承認済みライセンス 12 本）** | `2006-03-license-discuss-looking-for-license-stewards-observed.txt` |
| 2012-01 | `license-review` | **観測（"[PROPOSAL] Invite Creative Commons to submit CC0 Dedication." から 5 通・CC0 を招く前の、放棄と許諾を 1 つに持つ文書を審査できるかの議論）** | `2012-01-license-review-invite-cc0-observed.txt` |
| 2012-02 | `license-review` | **観測（"OSI recognition for Creative Commons Zero License?" から 7 通・CC が出す前に利用者が承認を求めた、既存の許容型で足りるか、誰が出すべきか）** | `2012-02-license-review-osi-recognition-cc0-observed.txt` |
| 2013-07〜08 | `license-discuss` | **観測（"Open source license chooser choosealicense.com launched." から 5 通・選択サイトを案内するか、偏り、「無名には理由がある」、増殖の何が悪いか）** | `2013-07-and-08-license-discuss-choosealicense-observed.txt` |
| 2013-03 | `license-review` | **観測（"CeCILL license V2.1 for Approval" の 2013 年の会話から 2 通・1 年止まった提出の再開と、委員長の謝罪）** | `2013-03-license-review-cecill-2-1-restart-observed.txt` |
| 2013-03 | `license-discuss` | **観測（Villa 氏の 1 通・Fontana 氏の「Frameworx は急いで承認された」を引いて取り下げの手続きを問う）** | `2013-03-license-discuss-delisting-villa-opener-observed.txt` |
| 2013-03 | `license-discuss` | **観測（Villa 氏の 1 通・起草の質の評価は主観的）** | `2013-03-license-discuss-delisting-villa-subjective-observed.txt` |
| 2013-03 | `license-discuss` | **観測（Fontana 氏の 1 通・取り下げの理由は OSD だけ、OSD の解釈に法律家は要らない）** | `2013-03-license-discuss-delisting-fontana-osd-only-observed.txt` |
| 2013-03 | `license-discuss` | **観測（Perens 氏の 1 通・法律家なしの起草は容易に見分けられる）** | `2013-03-license-discuss-delisting-perens-diagnose-observed.txt` |
| 2013-03 | `license-discuss` | **観測（Perens 氏の 1 通・取り下げの理由 3 つ、法律家なしの起草を含む）** | `2013-03-license-discuss-delisting-perens-justifications-observed.txt` |
| 2013-03 | `license-discuss` | **観測（"FAQ entry for slight variations in licenses?" から 4 通・承認済みライセンスの変種の確認に弁護士は要るか、で 2 人の弁護士が反対を向いた）** | `2013-03-license-discuss-slight-variations-lawyer-observed.txt` |
| 2013-03 | `license-review` | **観測（2013 年 3 月の委員会報告 2 本から 3 通・理事会が求めて復活した正式の報告、CeCILL 2.1 の推薦、個人の起草者への勧め）** | `2013-03-license-review-committee-reports-observed.txt` |
| 2017-01〜02 | `license-review` | **観測（"License Committee Report - January 2017" から 4 通・推薦は委員長個人のもの、list の沈黙、理事会は前もって判断を示さない）** | `2017-01-and-02-license-review-committee-report-observed.txt` |
| 2017-02 | `license-discuss` | **観測（Rosen 氏の 1 通・法律家でない人を通してライセンスを出すことへの反発）** | `2017-02-license-discuss-arl-osl-rosen-non-lawyer-funnel-observed.txt` |
| 2005-04 | `license-discuss` | **観測（"Official License Anti-Proliferation policy?" から 4 通・OSI の 2005-04-08 の声明の写しと、3 つの新しい基準の当てはめ方の説明）** | `2005-04-license-discuss-proliferation-statement-observed.txt` |
| 2016-06・2017-01 | `license-review` | **観測（"Approval request for ZENTAO PUBLIC LICENSE" から 4 通と 2017-01 の委員会報告の会話から 1 通・badgeware、中国語の正本、利用者の多さでは足りなかった提出）** | `2016-06-license-review-zentao-public-license-observed.txt` |
| 2017-05・07 | `license-review` | **観測（"EUPL v1.2" から 2 通・International の分類の目的、全ての言語の版に及ぶ承認）** | `2017-05-and-07-license-review-eupl-1-2-observed.txt` |
| 2017-07 | `license-review` | **観測（Piana 氏の 1 通・大文字の語が定義されていない）** | `2017-07-license-review-hooyami-piana-capitalised-undefined-observed.txt` |
| 2017-08 | `license-review` | **観測（Piana 氏の 1 通・contra proferentem は法域で違い、当たらないこともある）** | `2017-08-license-review-w3c-piana-contra-proferentem-observed.txt` |
| 2019-02 | `license-review` | **観測（"For Approval: Twente License" から 4 通・プライバシーと人権の条件を利用に課して OSD 6 で退けられた）** | `2019-02-license-review-twente-license-observed.txt` |
| 2002-10 | `license-discuss` | **観測（"click-wrap is legally supportable?" から 3 通・同意を求めないライセンスの条項は争われうるか）** | `2002-10-license-discuss-click-wrap-observed.txt` |
| 2002-10 | `license-discuss` | **観測（"BXAPL - request for comments" から 1 通・Rosen 氏 2002-10-27）** | `2002-10-license-discuss-bxapl-rosen-not-a-contract-observed.txt` |
| 2002-10 | `license-discuss` | **観測（"Right to Use" から 1 通・Rosen 氏 2002-10-29）** | `2002-10-license-discuss-right-to-use-rosen-observed.txt` |
| 2002-10 | `license-discuss` | **観測（"Moral Rights" から 1 通・Rosen 氏 2002-10-03）** | `2002-10-license-discuss-moral-rights-rosen-question-observed.txt` |
| 2002-10 | `license-discuss` | **観測（"Moral Rights" から 1 通・Rosen 氏 2002-10-06）** | `2002-10-license-discuss-moral-rights-rosen-attorney-observed.txt` |
| 2002-10 | `license-discuss` | **観測（"Modified Artistic License (eNetwizard …)" から 1 通・Nelson 氏 2002-10-03）** | `2002-10-license-discuss-enetwizard-nelson-redundant-observed.txt` |
| 2002-10 | `license-discuss` | **観測（"Moral Rights" から 1 通・Nelson 氏 2002-10-07）** | `2002-10-license-discuss-moral-rights-nelson-volunteers-observed.txt` |
| 2015-07〜08 | `license-review` | **観測（"Request for approval of the Non-Coercive Copyleft Licence (NCCL) 1.0" から 4 通・本文を添えずに配ることへの懸念、同意を求めない形、誰も賛成せず 18 日で「却下」）** | `2015-07-and-08-license-review-nccl-observed.txt` |
| 2012-04 | `license-discuss` | **観測（"Draft of new OSI licenses landing page; please review." から 4 通・短い一覧へ導く案、特許を正しく扱うこと、献呈の型を勧める弁護士の文）** | `2012-04-license-discuss-licenses-landing-page-observed.txt` |
| 2003-08 | `license-discuss` | **観測（"Can abandonment be irrevocable?" から 7 通・放棄の代わりに撤回できない許諾を、と勧めた翌日に、撤回された許諾も放棄と変わらないかもしれないと書いた弁護士の文、禁反言は依拠した人しか守らないという読み）** | `2003-08-license-discuss-can-abandonment-be-irrevocable-observed.txt` |
| 2003-09 | `license-discuss` | **観測（Cowan 氏の 1 通・"may not" は読み違えられやすい）** | `2003-09-license-discuss-ossal-cowan-may-not-misreading-observed.txt` |
| 2000-03 | `license-discuss` | **観測（"Wired Article on the GPL" から 15 通・cphack の譲渡のあとで GPL を撤回できるか、署名した書面が無い許諾は譲渡に優先するか（17 U.S.C. §205(e)）、条件が対価になるか）** | `2000-03-license-discuss-gpl-revocation-cphack-observed.txt` |
| 2000-03 | `license-discuss` | **観測（Cowan 氏の 1 通・無条件の公の許諾は公有への献呈と取られうる）** | `2000-03-license-discuss-rms-position-cowan-unconditional-dedication-observed.txt` |
| 2000-08 | `license-discuss` | **観測（"Public Domain and liability" と "Abandonment" から 3 通・公有化した作品の免責、登録の無い宣言による公有化）** | `2000-08-license-discuss-public-domain-liability-and-abandonment-observed.txt` |
| 2001-02 | `license-discuss` | **観測（Cowan 氏の 1 通・"may not" は "must not" に）** | `2001-02-license-discuss-osd-wording-cowan-may-not-must-not-observed.txt` |
| 2001-03 | `license-discuss` | **観測（"Subscription/Service Fees - OSD Intent" から 1 通・Taylor 氏 2001-03-28）** | `2001-03-license-discuss-subscription-fees-taylor-run-observed.txt` |
| 2001-03 | `license-discuss` | **観測（"Subscription/Service Fees - OSD Intent" から 1 通・Taylor 氏 2001-03-28・Nelson 氏の引用）** | `2001-03-license-discuss-subscription-fees-taylor-nelson-quote-observed.txt` |
| 2005-09 | `license-discuss` | **観測（"When can licenses be revoked?" から 5 通・対価の無い許諾だけが随意に撤回できる、受領者の義務は免責の受け入れまで対価になりうる）** | `2005-09-license-discuss-when-can-licenses-be-revoked-observed.txt` |
| 2011-05 | `license-discuss` | **観測（"GPL revokability" から 3 通・GPL 3.0 は条件を守る限り撤回できないと定めた、1.0 と 2.0 は事実と法域による）** | `2011-05-license-discuss-gpl-revokability-observed.txt` |
| 2011-08 | `license-discuss` | **観測（Linksvayer 氏の 1 通・CC0 は FSF と共に公有を望むソフトウェアに推奨した・2011）** | `2011-08-license-discuss-dual-licence-linksvayer-cc0-fsf-observed.txt` |
| 2000-03 | `license-discuss` | **観測（"Licenses versus contracts" から 3 通・ライセンスは契約か許可か）** | `2000-03-license-discuss-licenses-versus-contracts-observed.txt` |
| 2000-08 | `license-discuss` | **観測（"The different between GPL and non-license" から 7 通・著作権者は自分で公有に置けるか、放棄の抗弁は 1976 年法の下で生きているか）** | `2000-08-license-discuss-gpl-and-non-license-observed.txt` |
| 2002-10〜11 | `license-discuss` | **観測（"a proposed change to the OSD" から 12 通・委員長の「使用と改変を制限しない」案、受け入れの手順と免責をめぐる委員長と弁護士の対立）** | `2002-10-license-discuss-proposed-osd-change-use-and-click-wrap-observed.txt` |
| 2004-02〜2005-02 | `license-discuss` | **観測（委員会報告 3 本と返信から 9 通・似たライセンスは「改善でない」が「望めば承認する」、使う人への引用の要求は使用の制限）** | `2004-license-discuss-committee-reports-observed.txt` |
| 2004-02 | `license-discuss` | **観測（Rousskov 氏の 1 通・長いライセンスは使う人を遠ざける）** | `2004-02-license-discuss-non-lawyers-rousskov-100-page-observed.txt` |
| 2004-02 | `license-discuss` | **観測（Taylor 氏の 1 通・承認済みのほとんどは法的な助言を受けて書かれた）** | `2004-02-license-discuss-non-lawyers-taylor-legal-advice-observed.txt` |
| 2004-02 | `license-discuss` | **観測（Taylor 氏の 1 通・法的に確かであることの代価としての長さ）** | `2004-02-license-discuss-simple-permissive-taylor-length-soundness-observed.txt` |
| 2004-03 | `license-discuss` | **観測（Cowan 氏の 1 通・公の許諾は常に取り消せないものとして扱われてきた、撤回は期待に反し禁反言に当たる）** | `2004-03-license-discuss-must-read-cowan-irrevocable-expectation-observed.txt` |
| 2008-11〜2012-03 | `license-review` / `license-discuss` | **観測（委員会報告 3 本と "license committee" から 10 通・条件を放棄しても承認は外れないという案、簡単な方がよいとは限らない、何でもしてよい式の差し戻し）** | `2008-to-2012-license-lists-committee-reports-observed.txt` |
| 2025-12 | `license-review` | **観測（BarrerSoftware License の審査から 4 通・OSD 6 で承認できない、本文が AI の道具で書かれたように読めることを読むのをやめる理由に挙げた審査者）** | `2025-12-license-review-barrersoftware-observed.txt` |
| 2025-12 | `license-review` | **観測（Piana 氏の 1 通・否認の主語と許諾の主語が揃わない）** | `2025-12-license-review-qmdeve-piana-authors-contributors-observed.txt` |
| 2025-12 | `license-discuss` | **観測（Berkus 氏の 1 通・非対称を作らない限り OSD 違反は無い）** | `2025-12-license-discuss-contributor-clauses-berkus-asymmetry-observed.txt` |
| 2025-12 | `license-discuss` | **観測（Smith 氏の 1 通・提出する行為が同意の表示になる）** | `2025-12-license-discuss-contributor-clauses-smith-manifestation-observed.txt` |
| 2025-12 | `license-discuss` | **観測（Chestek 氏の 1 通・inbound=outbound の明示に賛成、受諾を通じて執行できる）** | `2025-12-license-discuss-contributor-clauses-chestek-express-observed.txt` |
| 2025-12 | `license-discuss` | **観測（Smith 氏の 1 通・非相互の貢献の条件は差別的）** | `2025-12-license-discuss-contributor-clauses-smith-nonreciprocal-observed.txt` |
| 2025-12 | `license-discuss` | **観測（Berkus 氏の 1 通・OSD 違反ではないが no-op）** | `2025-12-license-discuss-contributor-clauses-berkus-noop-observed.txt` |
| 2025-12 | `license-discuss` | **観測（Berkus 氏の 1 通・貢献の条項はライセンスに場所が無い）** | `2025-12-license-discuss-contributor-clauses-berkus-opener-observed.txt` |
| 2017-04・2019-08 | `license-review` / `license-discuss` | **観測（BSD+Patent の承認の告知と "Fact-gathering on OSI-approved licenses" から 5 通・分類は当面「特別な目的」、承認しない処分は却下に等しいと言え、CC0 の取り下げを「却下」と呼んだ委員）** | `2017-04-and-2019-08-license-lists-bsd-patent-approval-and-cc0-disposition-observed.txt` |
| 2005-09 | `license-discuss` | **観測（OSL 3.0 / AFL 3.0 の提出から 3 通・改変版を許す第 16 条と steward、提出の件名の形）** | `2005-09-license-discuss-osl-afl-3-0-section-16-and-submission-form-observed.txt` |
| 2011-04 | `license-discuss` | **観測（"Accidental Public License?" から 2 通・法務部門は既存の複雑さを一度学べばよい、新しく試されていないライセンスの限界費用）** | `2011-04-license-discuss-accidental-public-license-observed.txt` |
| 2013-04〜06 | `license-review` | **観測（"Comment on MOSL and similar licenses" とその枝から 6 通・法的な助言なしの起草、支持者と採用を求める案への反対、OSD に適合しても退ける裁量、却下の 3 理由）** | `2013-04-to-06-license-review-mosl-legal-review-and-approval-bar-observed.txt` |
| 2013-05 | `license-discuss` | **観測（Fogel 氏の 1 通・新しいライセンスを作ることは強く勧めない）** | `2013-05-license-discuss-akshar-fogel-discourage-observed.txt` |
| 2013-05 | `license-discuss` | **観測（Villa 氏の 1 通・2013 年の承認の規則の 5 項目）** | `2013-05-license-discuss-akshar-villa-approval-rules-observed.txt` |
| 2004-11・2007-12 | `license-discuss` / `license-review` | **観測（3 通・審査中に直すことへの法律家の受け止め、自動で新しい版へ移す条、曖昧でないライセンスと行数）** | `2004-11-and-2007-12-license-lists-rewriting-upgrade-and-length-observed.txt` |
| 2004-12 | `license-discuss` | **観測（"For Approval: German Free Software License" から 1 通・Nelson 氏 2004-12-01）** | `2004-12-license-discuss-gfsl-nelson-intrinsic-need-observed.txt` |
| 2003-07〜08 | `license-discuss` | **観測（"Academic Free License version 2.0" から 4 通・BSD 型が欠く細部を埋める、明確にするのに要る語数）** | `2003-07-and-08-license-discuss-afl-2-0-gaps-and-length-observed.txt` |
| 2003-07 | `license-discuss` | **観測（Taylor 氏の 1 通・新しいライセンスの前に、既存のどれも合わない理由をリストに説明せよ）** | `2003-07-license-discuss-license-idea-taylor-first-step-observed.txt` |
| 2007-10 | `license-discuss` | **観測（"For Approval: Microsoft Public License" から 2 通・残る異議は「また 1 つのライセンス」と「Microsoft だ」、ライセンスか提出者か）** | `2007-10-license-discuss-ms-pl-remaining-objections-observed.txt` |
| 2012-06 | `license-discuss` | **観測（ライセンスの頁の再編の議論から 1 通・open source でも OSI に承認されない理由 3 つ）** | `2012-06-license-discuss-open-source-but-not-osi-approved-observed.txt` |
| 2005-12〜2007-10 | `license-discuss` | **観測（Microsoft Community License と Reciprocal License の審査から 13 通・弁護士が指摘し提出者が認めた曖昧さが、本文を変えないまま承認された）** | `2005-12-to-2007-10-license-discuss-ms-cl-and-ms-rl-observed.txt` |
| 2007-11 | `license-discuss` | **観測（"Question on OSD #5" から 3 通・合衆国の取り戻しの規定があるので本当に perpetual なライセンスは無い）** | `2007-11-license-discuss-question-on-osd-5-perpetual-observed.txt` |
| 2007-11 | `license-discuss` | **観測（Nelson 氏・承認はどれも費用を課す・1 通）** | `2007-11-license-discuss-nelson-every-licence-a-cost-observed.txt` |
| 2007-12 | `license-discuss` | **観測（Nelson 氏・保証の否認と契約・1 通）** | `2007-12-license-discuss-nelson-warranty-contract-observed.txt` |
| 2007-12 | `license-discuss` | **観測（Tiemann 氏・or later は範囲外・1 通）** | `2007-12-license-discuss-tiemann-or-later-scope-observed.txt` |
| 2008-01〜02 | `license-review` | **観測（GNU Affero GPLv3 の提出から 7 通・分類の基準をめぐる意見の違い）** | `2008-01-license-review-agpl-category-observed.txt` |
| 2008-01 | `license-discuss` | **観測（"License committee report for January 2008"・Nelson 氏 2008-01-09・Boost の承認勧告ほか）** | `2008-01-license-discuss-committee-report-nelson-boost-observed.txt` |
| 2008-02 | `license-discuss` | **観測（Nelson 氏・約束は見知らぬ者の間に成り立つか・1 通）** | `2008-02-license-discuss-nelson-covenant-strangers-observed.txt` |
| 2009-01〜02 | `license-review` | **観測（caGrid License の legacy approval の求めから 5 通・数百の配備は広い分類に足りない）** | `2009-01-license-review-cagrid-legacy-approval-observed.txt` |
| 2011-05〜08 | `license-review` | **観測（Python のライセンスの改訂の承認の求めから 3 通・先例は参考であって拘束しない、古い版を非推奨にしても効かない）** | `2011-05-to-08-license-review-python-license-changes-observed.txt` |
| 2008-10 | `license-review` | **観測（AFL に論文の引用の義務を足したいという問いから 5 通・承認済みに似た条が在ることは新しい条を正当化しない）** | `2008-10-license-review-afl-citation-and-old-mistakes-observed.txt` |
| 2007-08 | `license-discuss` | **観測（"Groklaw's OSI item" から 2 通・OSI は認証を取り消したことがない、提出者の素性で差別も優遇もしない）** | `2007-08-license-discuss-groklaw-certification-not-pulled-observed.txt` |
| 2007-08 | `license-discuss` | **観測（Engelfriet 氏の 1 通・大陸法に bare license の概念は要らない）** | `2007-08-license-discuss-copyleft-blow-engelfriet-civil-law-observed.txt` |
| 2008-05・2009-02 | `license-review` | **観測（EUPL の承認の求めから 2 通・言語の版の食い違いは受領者に有利に決めるべきだという提案と、それは要件にならなかったこと）** | `2008-05-to-2009-02-license-review-eupl-ties-in-favor-of-licensee-observed.txt` |
| 2008-05 | `license-review` | **観測（Perens 氏の 1 通・大きな問題で通らないと分かれば小さな問題は誰も見ない）** | `2008-05-license-review-iwl-perens-bigger-issues-observed.txt` |
| 2008-05 | `license-review` | **観測（Nelson 氏の 1 通・既存のライセンスから始めて適合を求めるのは良くない）** | `2008-05-license-review-iwl-nelson-existing-license-observed.txt` |
| 2008-05 | `license-review` | **観測（Nelson 氏の 1 通・承認は一語も変えない本文に対するもの、型板にすべき）** | `2008-05-license-review-iwl-nelson-not-one-word-observed.txt` |
| 2011-03〜04 | `license-discuss` | **観測（"Announcing OWFa and CLA 1.0" から 3 通・寄与は同じライセンスで入れば足りる）** | `2011-03-license-discuss-owfa-cla-inbound-outbound-observed.txt` |
| 2007-07〜08 | `license-discuss` | **観測（OSD 2 の不一致の問いから 2 通・OSD 2 はライセンスでなく配られる物について述べる）** | `2007-07-license-discuss-osd-2-inconsistency-observed.txt` |
| 2007-03 | `license-discuss` | **観測（Socialtext Public License の審査から 2 通・承認済みの条から取ったので推定が働くべきだという主張と、それへの反論）** | `2007-03-license-discuss-stpl-presumption-from-approved-observed.txt` |
| 2007-03 | `license-discuss` | **観測（Rosen 氏・ライセンスに商標の許諾を入れない・1 通）** | `2007-03-license-discuss-rosen-no-trademark-licence-observed.txt` |
| 2003-08 | `license-discuss` | **観測（"Open Source Licensing" の全 3 通・OSL の perpetual と 17 U.S.C. §203、法はどのみち勝つので書く必要は無いという文の引用）** | `2003-08-license-discuss-osl-perpetual-and-section-203-observed.txt` |
| 2007-07〜08 | `license-discuss` | **観測（GPLv3 の審査の進め方から 2 通・審査を OSD だけに絞る主張と、その前提だった採用と検討）** | `2007-07-license-discuss-gplv3-review-scope-observed.txt` |
| 2018-06 | `license-review` | **観測（"moving to an issue tracker" から 5 通・理事会が変更を求める 2 つの場面と、独自の価値の問い）** | `2018-06-license-review-board-change-requests-and-unique-value-observed.txt` |
| 2018-06 | `license-review` | **観測（Perens 氏の 1 通・切り離しの攻撃は起きていない）** | `2018-06-license-review-nosa-perens-no-severability-attack-observed.txt` |
| 2018-06 | `license-review` | Villa 氏 2018-06-19 | `2018-06-license-review-submitter-notes-villa-industry-changed-observed.txt` |
| 2018-09 | `license-review` | **観測（Smith 氏の 1 通・先例の主張への否定的な反応、運用は OSD の文言より厳しい）** | `2018-09-license-review-cfsl-smith-interpretive-history-observed.txt` |
| 2018-06 | `license-review` | **観測（Perens 氏の 1 通・ライセンスに関心を持つ人を紹介してほしい）** | `2018-06-license-review-l0r-perens-interest-observed.txt` |
| 2018-06 | `license-review` | **観測（Cowan 氏の 1 通・RPL は不透明でも善意だから承認したが誤りだった）** | `2018-06-license-review-l0r-cowan-rpl-observed.txt` |
| 2026-06 | `license-review` | **観測（The Mutualist License の審査から 3 通・語の正確さ、解釈の規則は語の不明確さを補わない、専門家の読み）** | `2026-06-license-review-mutual-drafting-and-canons-observed.txt` |
| 2019-01〜2020-03 | `license-discuss` | **観測（2 つの会話から 4 通・意図は明確に、ただし曖昧で広すぎる語でなく。倫理的なライセンスは OSD と両立しない。moderation で落とされた通）** | `2019-01-to-2020-03-license-discuss-intent-precision-and-moderation-observed.txt` |
| 2019-01 | `license-discuss` | **観測（Perens 氏の 1 通・著作権の拡張は強制に役立つ場合でもオープンソースに悪い）** | `2019-01-license-discuss-extension-of-copyright-perens-observed.txt` |
| 2019-01 | `license-discuss` | **観測（Perens 氏の 1 通・Autonomous Agent License の API の条項は承認しないよう強く勧める）** | `2019-01-license-discuss-autonomous-agent-license-perens-observed.txt` |
| 2019-01 | `license-discuss` | **観測（Lindberg 氏の 1 通・後の CAL の前身「Autonomous Agent License」の事前の告知）** | `2019-01-license-discuss-autonomous-agent-license-lindberg-observed.txt` |
| 2019-01 | `license-review` | **観測（Phipps 氏の 1 通・四つの自由は評価の前提、一般の利用のための承認、対等な権利）** | `2019-01-license-review-cfsl-phipps-general-use-observed.txt` |
| 2015-01 | `license-discuss` | **観測（"FAQ entry on CLAs" から 3 通・OSI は外向きのライセンスだけを審査する）** | `2015-01-license-discuss-osi-reviews-outbound-only-observed.txt` |
| 2015-01 | `license-discuss` | **観測（Woolley 氏の 1 通・公有のライセンスは放棄の試みと代わりの許諾の組み合わせ）** | `2015-01-license-discuss-pd-customized-woolley-no-pd-licence-observed.txt` |
| 2005-08 | `license-discuss` | **観測（OVPL の会話から 6 通・委員長の逐語の再利用の要求と、認証の要件は OSD に限るべきだという理事の反対）** | `2005-08-license-discuss-ovpl-verbatim-reuse-observed.txt` |
| 2005-08 | `license-discuss` | **観測（Rosen 氏の 1 通・受諾が無ければ bare license）** | `2005-08-license-discuss-bare-licenses-rosen-assent-observed.txt` |
| 2002-08 | `license-discuss` | **観測（"A new "use" clause in the OSD" から 4 通・許される制限だけを列挙する OSD の条の案）** | `2002-08-license-discuss-osd-use-clause-observed.txt` |
| 2018-10 | `license-review` | **観測（SSPL と OSD 9 の会話から 3 通・OSD は別の時代のために書かれた、承認済みのライセンスは OSD の隙を整えられる）** | `2018-10-license-review-osd9-written-for-another-time-observed.txt` |
| 2018-10 | `license-review` | **観測（Cowan 氏の 1 通・定義されない語は普通の意味で読まれる）** | `2018-10-license-review-sspl-cowan-functionality-undefined-observed.txt` |
| 2018-10 | `license-review` | **観測（Phipps 氏の 1 通・著者に代わって未解決の論点を集めた、改訂版が要る）** | `2018-10-license-review-cfsl-phipps-open-issues-observed.txt` |
| 2018-10 | `license-review` | **観測（Phipps 氏の 1 通・指摘が改訂版で扱われていないので理事会は判断を延ばした）** | `2018-10-license-review-cfsl-phipps-postponed-observed.txt` |
| 2019-06 | `license-discuss` | **観測（"Copyright on APIs" から 2 通・在るか分からない権利を主張すること、名指すことが権利の拡張の例になること）** | `2019-06-license-discuss-api-copyright-claiming-rights-observed.txt` |
| 2019-07 | `license-discuss` | Villa 氏 2019-07-02 | `2019-07-license-discuss-how-global-villa-2019-observed.txt` |
| 2025-12 | `license-discuss` | **観測（"Total Reciprocity Public License (TRPL v1.0)" から 3 通・出力を派生物とみなす条は使用の制限か、ライセンスが法の語を作り直すこと）** | `2025-12-license-discuss-trpl-functional-output-observed.txt` |
| 2025-12 | `license-discuss` | **観測（同じ会話から 2 通・同じ誤解がほぼ月に一度来ること、出力への条件は契約でしか働かず同意した者しか縛らないこと）** | `2025-12-license-discuss-trpl-once-a-month-and-contract-observed.txt` |
| 2025-07〜10 | `license-review` | **観測（PPPL BSD-3 の提出から 4 通・名前だけが違う同じライセンスは承認しない、著作権者の表示はライセンスの外に置く、名は steward が決める）** | `2025-07-to-10-license-review-pppl-same-license-new-name-observed.txt` |
| 2025-08 | `license-review` | **観測（Berkus 氏の 1 通・撤回不能の明記は少し冗長、撤回の実例は無い）** | `2025-08-license-review-mit-i-berkus-irrevocable-redundant-observed.txt` |
| 2026-03 | `license-review` | **観測（CNRI-Python-GPL-Compatible の提出から 4 通・clickwrap の文と OSD 10、同意の別の道が在れば反しないという読み）** | `2026-03-license-review-cnri-python-clickwrap-osd10-observed.txt` |
| 2026-01 | `license-discuss` | **観測（Project Tick の草案から Perens 氏の 1 通・選択で起動する条項はライセンスを増やす、提出の前に法律家を使え）** | `2026-01-license-discuss-project-tick-attorney-observed.txt` |
| 2026-01〜02 | `license-review` | **観測（Project Tick の提出から 2 通・提出した文は変えられない、`license-discuss` で固めてから出す、否決の勧告と既存のライセンスか法律家か）** | `2026-01-to-04-license-review-project-tick-discuss-first-observed.txt` |
| 2019-08 | `license-review` | **観測（CAL の審査で Berkus 氏が条ごとに付けた所見の 1 通・迂回を禁じる法には政府の行為の例外が要るか）** | `2019-08-license-review-cal-anti-circumvention-exemption-observed.txt` |
| 2019-05 | `license-discuss` | **観測（"Government licenses" から 4 通・著作権の無い部分には既存のライセンスが及ばないだけで足りる、パブリックドメインを契約で縛るのは奇妙）** | `2019-05-license-discuss-government-works-uncopyrightable-parts-observed.txt` |
| 2014-09 | `license-review` | **観測（"Sublicensing" から 4 通・再許諾で約束は落ちる、FOSS は直接の許諾、再許諾を許す理由を示せ）** | `2014-09-license-review-sublicensing-privity-observed.txt` |
| 2013-08 | `license-discuss` | **観測（"License incompatibility" から 2 通・法律上の語を定義するのはライセンスの役目ではない、新しいライセンスは最後の手段）** | `2013-08-license-discuss-incompatibility-statutory-terms-last-resort-observed.txt` |
| 2013-09 | `license-review` | **観測（Fontana 氏の 1 通・表記だけの改訂でも改訂版は承認済みと呼べない）** | `2013-09-license-review-miros-fontana-editorial-not-approved-observed.txt` |
| 2013-09 | `license-review` | **観測（Villa 氏の 1 通・おおむね正しい、BSD・MIT の既定の本文は例外）** | `2013-09-license-review-miros-villa-roughly-right-observed.txt` |
| 2013-08 | `license-discuss` | **観測（Rosen 氏の 1 通・OWFa の後継者を縛る約束、倒産法 365(n)、迂回しない約束）** | `2013-08-license-discuss-owfa-successors-bankruptcy-observed.txt` |
| 2016-06 | `license-review` | **観測（Moritz30 の提出から 6 通・読めなければ適合しないと推定する、法律家への相談を要件にしない、長い語は効くために要る）** | `2016-06-license-review-moritz30-unclear-means-nonconformant-observed.txt` |
| 2025-02 | `license-review` | **観測（ModelGo への Berkus 氏の所見 1 通・機械学習の条項に AI を作る実務家の読みを、英語に母語話者の編集者を）** | `2025-02-license-review-modelgo-berkus-practitioner-review-observed.txt` |
| 2026-08 | `license-review` | **観測（OpenMDW の審査から 3 通・著作権の反訴による終了は公平か、ソフトウェアでないものに及ぶライセンスを「ソフトウェアなら」の基準だけで量らない）** | `2026-08-license-review-openmdw-antisuit-and-non-software-observed.txt` |
| 2026-08 | `license-review` | Villa 氏 2026-08-14 | `2026-08-license-review-openmdw-villa-mpl2-defensive-clause-observed.txt` |
| 2024〜2026 | `license-review` | **観測（ドシエが引いていなかった決める側の 6 通・前例を論拠にするな、精確な語は品質の問題、AI 生成の表示はファイル単位で、完全な許諾は全法域の動詞を持つ）** | `2024-to-2026-license-review-unquoted-decider-messages-observed.txt` |
| 2012-03 | `license-review` / `license-discuss` | **観測（"CC0 incompliant with OSD on patents" から 5 通・著作権だけのライセンスは滑りやすい坂、放棄の効果を論じるのは時間の無駄）** | `2012-03-license-review-cc0-incompliant-patents-observed.txt` |
| 2012-03 | `license-review` | **観測（Piana 氏の 1 通・沈黙のライセンスは禁反言に頼れるが、明示に外したライセンスは頼れない）** | `2012-03-license-review-mxm-cc0-piana-agnostic-estoppel-observed.txt` |
| 2020-02 | `license-discuss` | **観測（Persona non Grata の前文の会話から 2 通・採用の見込みは承認の基準ではなかった、拘束しない語は要らない）** | `2020-02-license-discuss-adoption-not-a-criterion-observed.txt` |
| 2020-02 | `license-review` | **観測（Chestek 氏の 1 通・CAL 7.6 の切り離しの文を引く）** | `2020-02-license-review-cal-chestek-text-severability-7-6-observed.txt` |
| 2010-05〜06 | `license-review` / `license-discuss` | **観測（WebM: BSD と別の特許許諾・4 通）** | `2010-05-to-06-license-lists-webm-patent-grant-observed.txt` |
| 2010-06 | `license-discuss` | **観測（Nelson 氏・オープンデータの定義・1 通）** | `2010-06-license-discuss-nelson-open-data-definition-observed.txt` |
| 2010-10 | `license-review` | **観測（Phipps 氏の 1 通・特定の相手への通知を条件にすると、相手が消えれば許諾が使えなくなり OSD に合わない）** | `2010-10-license-review-netx-phipps-unreachable-observed.txt` |
| 2010-10 | `license-review` | **観測（Perens 氏の 1 通・最善は承認済みのライセンスを使うこと）** | `2010-10-license-review-netx-perens-approved-license-observed.txt` |
| 2010-10 | `license-review` | **観測（Perens 氏の 1 通・サイトが消えてもライセンスは続かなければならない）** | `2010-10-license-review-netx-perens-website-observed.txt` |
| 2010-11 | `license-review` | **観測（Villa 氏の 1 通・OSI と同時に FSF にも一覧への掲載を求めている）** | `2010-11-license-review-mpl2-s11-villa-fsf-too-observed.txt` |
| 2010-11 | `license-review` | **観測（Perens 氏の 1 通・追加の許可は本文の外で、ライセンスは不変に）** | `2010-11-license-review-mpl2-s11-perens-invariant-observed.txt` |
| 2021-04 | `license-discuss` | **観測（0BSD の作者が名前の付け方の戦略を述べた 1 通）** | `2021-04-license-discuss-0bsd-naming-strategy-observed.txt` |
| 2012〜2020 | `license-review` | **観測（特許を扱う新しい permissive の必要性と、増殖の分類の現状・4 通）** | `2012-to-2020-license-review-need-and-proliferation-categories-cited-observed.txt` |
| 2002-11〜12 | `license-discuss` | **観測（寄与者の特許の許諾が派生物まで届くか・3 通）** | `2002-11-to-12-license-discuss-mpl-patent-grants-on-derivatives-observed.txt` |
| 2003-01 | `license-discuss` | **観測（"\"Derivative Work\" for Software Defined" から 1 通・Rosen 氏 2003-01-14）** | `2003-01-license-discuss-derivative-work-rosen-interpretive-observed.txt` |
| 2002-11 | `license-discuss` | **観測（"Approval Requested for AFL 1.2 and OSL 1.1" から 1 通・Rosen 氏 2002-11-06）** | `2002-11-license-discuss-afl-osl-rosen-real-reader-observed.txt` |
| 2002-11 | `license-discuss` | **観測（"Approval Requested for AFL 1.2 and OSL 1.1" から 1 通・Rosen 氏 2002-11-06）** | `2002-11-license-discuss-afl-osl-rosen-country-neutral-observed.txt` |
| 2002-11 | `license-discuss` | **観測（"Approval Requested for AFL 1.2 and OSL 1.1" から 1 通・Rosen 氏 2002-11-06）** | `2002-11-license-discuss-afl-osl-rosen-no-preamble-observed.txt` |
| 2002-11 | `license-discuss` | **観測（"time frame between request for approval …" から 1 通・Nelson 氏 2002-11-20）** | `2002-11-license-discuss-time-frame-nelson-pre-vet-observed.txt` |
| 2002-11 | `license-discuss` | **観測（"time frame between request for approval …" から 1 通・Rosen 氏 2002-11-20）** | `2002-11-license-discuss-time-frame-rosen-buzz-observed.txt` |
| 2002-11 | `license-discuss` | **観測（"time frame between request for approval …" から 1 通・Rosen 氏 2002-11-21）** | `2002-11-license-discuss-time-frame-rosen-no-legal-blessing-observed.txt` |
| 2016-12 | `license-discuss` | **観測（React の別ファイルの特許許諾と、CC0 に添える特許の文言・4 通）** | `2016-12-license-discuss-react-patents-and-cc0-patent-language-observed.txt` |
| 2025-05〜12 | `license-review` | **観測（ModelGo の再提出の審査から、出力・AI の語彙・権利の列挙・3 通）** | `2025-05-to-12-license-review-modelgo-outputs-and-vocabulary-observed.txt` |
| 2023-11〜2024-01 | `license-review` | **観測（Blue Oak の審査から承認の告知まで・6 通）** | `2023-11-to-2024-01-license-review-blue-oak-approval-observed.txt` |
| 2018-11 | `license-discuss` | **観測（OSD は特許にも及ぶという言明と、特許を含む定義の案・3 通）** | `2018-11-license-discuss-osd-and-patents-observed.txt` |
| 2017-01〜04 | `license-discuss` | **観測（人気の一覧の作り方の提案と返信・3 通）** | `2017-01-to-04-license-discuss-systematic-approach-popular-licenses-observed.txt` |
| 2024-11 | `license-discuss` | **観測（学術医療機関が特許の許諾を狭める案・3 通）** | `2024-11-license-discuss-academic-medical-center-patents-observed.txt` |
| 2016-08〜2017-03 | `license-discuss` | **観測（ARL OSL の議論から引いた 21 通・1/2 部）** | `2016-08-to-2017-03-license-discuss-arl-osl-cited-observed-1of2.txt` |
| 2016-08 | `license-discuss` | **観測（"U.S. Army Research Laboratory Open Source License (ARL OSL)" から 1 通・Fontana 氏 2016-08-20）** | `2016-08-license-discuss-arl-fontana-nosa-too-complex-observed.txt` |
| 2016-08〜2017-03 | `license-discuss` | **観測（ARL OSL の議論から引いた 21 通・2/2 部）** | `2016-08-to-2017-03-license-discuss-arl-osl-cited-observed-2of2.txt` |
| 2014-04〜2015-02 | `license-review` | **観測（UPL の審査から引いた 23 通・1/3 部）** | `2014-04-to-2015-02-license-review-upl-cited-observed-1of3.txt` |
| 2014-04〜2015-02 | `license-review` | **観測（UPL の審査から引いた 23 通・2/3 部）** | `2014-04-to-2015-02-license-review-upl-cited-observed-2of3.txt` |
| 2014-04〜2015-02 | `license-review` | **観測（UPL の審査から引いた 23 通・3/3 部）** | `2014-04-to-2015-02-license-review-upl-cited-observed-3of3.txt` |
| 2015-02-04 | OSI 理事会 | **観測（UPL を承認した議決・議事録の抜き出し）** | `2015-02-04-osi-board-minutes-upl-approval-observed.txt` |
| 2026-11-16 | FSF・Debian | **観測（FSF の license-list の CC0・Unlicense・公有の項と、Debian Wiki の DFSGLicenses の公有の段・WebFetch の逐語の片で、バイト単位の写しではない）** | `2026-11-16-fsf-license-list-and-debian-dfsg-public-domain-snapshot.txt` |
| 2026-11-16 | 米国最高裁・米国法典 | **観測（Mission Product Holdings v. Tempnology（2019）の 4 文と 11 U.S.C. §365(n)(1) の冒頭の句・WebFetch の逐語の片で、バイト単位の写しではない・問い 8 の米国の法源）** | `2026-11-16-us-bankruptcy-tempnology-and-365n-snapshot.txt` |
| 2026-11-16 | EU 指令 | **観測（製造物責任指令 2024/2853 の第 2 条 2 項・前文 14・第 15 条と、デジタルコンテンツ指令 2019/770 の第 3 条 1 項・5 項 (f)・自由でオープンなソフトウェアの除外・WebFetch の逐語の片で、EUR-Lex の文ではない）** | `2026-11-16-eu-product-liability-and-digital-content-foss-snapshot.txt` |
| 2026-11-16 | UCC・VARA・EU 商標規則 | **観測（UCC §2-316・§2-312(2)、17 U.S.C. §106A(a)・(e)(1)、EU 商標規則 2017/1001 第 14 条 1 項 (c)・2 項・WebFetch の逐語の片で、バイト単位の写しではない・THIRD §18.4 の法源）** | `2026-11-16-us-ucc-vara-and-eu-trademark-snapshot.txt` |
| 2026-11-16 | EU 指令・ローマ I・II | **観測（DSM 指令 2019/790 第 4 条 1〜3 項と前文 18、ローマ I 第 1 条 1 項・第 4 条、ローマ II 第 8 条 1 項・3 項・WebFetch の逐語の片で、バイト単位の写しではない・問い 6・7 の法源）** | `2026-11-16-eu-tdm-and-conflict-of-laws-snapshot.txt` |
| 2026-11-16 | EU データベース指令 | **観測（96/9/EC 第 7 条 1・3・5 項、第 8 条 1 項、第 15 条・WebFetch の逐語の片で、バイト単位の写しではない・THIRD §18.6 の §7 の法源）** | `2026-11-16-eu-database-directive-snapshot.txt` |
| 2026-11-16 | 弁護士の公開の分析（独・CC0） | **観測（Kreutzer 氏の CC0 のドイツ法上の有効性の分析・2011 年頃・放棄は無効、fallback の許諾は有効、公有の宣言は公の許諾と読み替えられるのが通説、不行使の約束は有効・PDF からこの session で取り出した・問い 1 の法源）** | `2026-11-16-kreutzer-cc0-german-law-analysis-snapshot.txt` |
| 2026-11-18 | SPDX が保持する GPL-3.0 | **観測（GPL-3.0 の頭の 6 行・「逐語の写しは誰でも頒布できるが変更は許されない」・GitHub の API で byte のまま・commit 60fbd82 に固定・§16.4 の法源）** | `2026-11-18-gpl-3-0-header-spdx-snapshot.txt` |
| 2026-11-19 | 米国法典 | **観測（17 U.S.C. §203(a)・(a)(3)〜(5)・(b) と §1201(a)(1)(A)・(a)(3) の定義・Cornell LII から WebFetch の逐語の片で、バイト単位の写しではない・§203 は 125 字で切れた片）** | `2026-11-19-us-17-usc-203-1201-snapshot.txt` |
| 2026-11-19 | 独 判例 | **観測（BGH 2016-04-06 XII ZR 29/15 Rn. 19・効力維持的縮減の禁止・WebFetch の逐語の片で、バイト単位の写しではない・二次の出版元）** | `2026-11-19-bgh-xii-zr-29-15-geltungserhaltende-reduktion-snapshot.txt` |
| 2026-11-19 | 英 Find Case Law | 観測（Noel Redding Estate v Sony [2026] EWHC 983 (Ch) が Fisher v Brooker の上告審を要約・引用した段落・Find Case Law の逐語の片） | `2026-11-19-uk-noel-redding-v-sony-2026-fisher-v-brooker-hl-snapshot.txt` |
| 2026-11-19 | 英 legislation.gov.uk（EU 指令の英国保持版） | **観測（指令 2009/24/EC 5 条・6 条 1 項・2 項 (c)・8 条・プログラムの例外と逆コンパイル・英国保持版・WebFetch の逐語の片）** | `2026-11-19-eu-software-directive-2009-24-art-5-6-8-snapshot.txt` |
| 2026-11-19 | 英 Find Case Law | 観測（Fisher v Brooker [2008] EWCA Civ 287 の 136・138・140・141 段落・Find Case Law の逐語の片） | `2026-11-19-uk-fisher-v-brooker-2008-paras-136-141-snapshot.txt` |
| 2026-11-19 | 英 legislation.gov.uk（EU 指令） | **観測（DSM 指令 15 条 1 項・2 項・報道出版者の権利・WebFetch の逐語の片）** | `2026-11-19-eu-dsm-2019-790-art-15-snapshot.txt` |
| 2026-11-19 | 英 Find Case Law | 観測（Fisher v Brooker [2008] EWCA Civ 287・著作権の無償の許諾の撤回・Find Case Law の逐語の片） | `2026-11-19-uk-fisher-v-brooker-2008-ewca-civ-287-gratuitous-licence-snapshot.txt` |
| 2026-11-19 | e-Gov・gesetze-im-internet | 観測（著作権法 15 条・UrhG 43 条・69b 条・職務著作・e-Gov 法令 API と gesetze-im-internet の逐語の片） | `2026-11-19-jp-chosakukenho-15-urhg-43-69b-employee-works-snapshot.txt` |
| 2026-11-19 | 英 legislation.gov.uk | 観測（Law of Property (Miscellaneous Provisions) Act 1989 1 条・捺印証書の要件・WebFetch の逐語の片） | `2026-11-19-uk-lpmpa-1989-s1-deeds-snapshot.txt` |
| 2026-11-19 | 米 LII（17 U.S.C.） | **観測（17 U.S.C. §101 の職務著作の定義・§106 の (1)〜(3)・§201(a)(b)・WebFetch の逐語の片）** | `2026-11-19-us-17-usc-101-wmfh-106-201-snapshot.txt` |
| 2026-11-19 | 英 legislation.gov.uk | 観測（CDPA 1988 296ZF・296ZA・296 条・技術的手段の定義と回避・WebFetch の逐語の片） | `2026-11-19-cdpa-1988-s296-s296za-s296zf-snapshot.txt` |
| 2026-11-19 | 英 legislation.gov.uk（EU 指令の英国保持版） | **観測（指令 2001/29/EC 6 条 1 項・3 項、7 条 1 項 (a)・2 項・英国の保持版・WebFetch の逐語の片）** | `2026-11-19-eu-infosoc-2001-29-art-6-7-snapshot.txt` |
| 2026-11-19 | 米 LII（17 U.S.C.） | **観測（17 U.S.C. §1202(b)(c)・§1203(a)・著作権管理情報と民事の救済・WebFetch の逐語の片）** | `2026-11-19-us-17-usc-1202-1203-snapshot.txt` |
| 2026-11-19 | 英 legislation.gov.uk | 観測（1997 年のデータベース規則 13・16・19 条、CDPA 29A 条・WebFetch の逐語の片） | `2026-11-19-uk-database-regulations-1997-cdpa-29a-snapshot.txt` |
| 2026-11-19 | カナダ法 | **観測（カナダ著作権法 14.1 条 (1)〜(4)・人格権は譲れないが放棄できる・WebFetch の逐語の片で、バイト単位の写しではない・まだ当てていない法域）** | `2026-11-19-canada-copyright-act-14-1-moral-rights-snapshot.txt` |
| 2026-11-19 | デジタル庁（e-Gov 法令 API） | 観測（著作権法 19・20・30 条の 4、特許法 68・78・94・99 条・e-Gov 法令 API・WebFetch の逐語の片） | `2026-11-19-jp-chosakukenho-19-20-30-4-tokkyoho-68-78-94-99-snapshot.txt` |
| 2026-11-19 | 独 BGB・EU 指令・ベルヌ条約 | **観測（BGB 305c 条・指令 93/13 第 5 条・ベルヌ条約 5 条 2 項・WebFetch の逐語の片で、バイト単位の写しではない・THIRD §18.5 の「未取得」だった法源）** | `2026-11-19-bgb-305c-directive-93-13-art5-berne-5-2-snapshot.txt` |
| 2026-11-16 | CC0 FAQ（steward の説明） | **観測（CC0 は一方通行・放棄が効かない所では無条件で撤回不能の許諾・法域によっては全ての権利を放棄できない・商標と特許は影響を受けない・ソフトウェアに適する・OSI の承認は無い・WebFetch の逐語の片で、2 度の取得で確認）** | `2026-11-16-cc0-faq-steward-interpretation-snapshot.txt` |
| 2026-11-16 | 米国連邦巡回区 | **観測（TransCore v. Electronic Transaction Consultants（2009）の、非独占の特許の許諾は訴えない約束と同じ効果、の 3 文・WebFetch の逐語の片で、バイト単位の写しではない・問い 2・8 の法源）** | `2026-11-16-us-transcore-covenant-equals-license-snapshot.txt` |
| 2026-11-16 | 米国第 9 巡回区 | **観測（Asset Marketing Systems v. Gagnon（2008）の「対価を払ったので撤回できない」「対価に支えられた非独占の許諾は契約」の段・法律事務所の PDF からこの session で取り出した・裁判所の写しではない・撤回不能の不利な側の法源）** | `2026-11-16-us-asset-marketing-v-gagnon-consideration-snapshot.txt` |
| 2026-11-16 | 米国の州最高裁 | **観測（契約法リステイトメント第 2 版 §90(1) の約束的禁反言の規準を、イリノイ（2009・全文）・メイン（1989）・アラスカの判決の引用で・WebFetch の逐語の片で、バイト単位の写しではない・§2.5 の米国の法源）** | `2026-11-16-us-restatement-90-promissory-estoppel-snapshot.txt` |
| 2026-11-16 | 独連邦司法省（gesetze-im-internet.de） | **観測（UrhG 31 条 5 項・目的移転の原則の条文・WebFetch の逐語の片で、バイト単位の写しではない）** | `2026-11-16-urhg-31-5-gesetze-im-internet-snapshot.txt` |
| 2010-10-07 | Schmitz 氏（EUPL の起草者） | **観測（netX の審査・一般的な免責は欧州で不当とされ、EUPL は故意と自然人への損害を除外しない理由・Wilson 氏の問いの引用つき）** | `2010-10-license-review-netx-schmitz-liability-exclusion-observed.txt` |
| 2026-11-16 | 独連邦司法省（gesetze-im-internet.de） | **観測（BGB 276 条 3 項・307 条 1 項・309 条 7 号・521 条・524 条 1 項・WebFetch の逐語の片）** | `2026-11-16-bgb-276-307-309-521-524-gesetze-im-internet-snapshot.txt` |
| 2026-11-16 | 独連邦司法省（gesetze-im-internet.de） | **観測（BGB 151 条・受諾の表示を要しない場合・WebFetch の逐語の片）** | `2026-11-16-bgb-151-gesetze-im-internet-snapshot.txt` |
| 2026-11-20 | 英 legislation.gov.uk | **観測（CDPA 1988 9 条・78 条・79 条・81 条・84 条・94 条・人格権の章のうちプログラムとコンピュータ生成物の例外と偽の帰属・WebFetch の逐語の片）** | `2026-11-20-cdpa-1988-s9-s78-s79-s81-s84-s94-legislation-gov-uk-snapshot.txt` |
| 2026-11-18 | 独連邦司法省（gesetze-im-internet.de） | **観測（BGB 306 条・約款の無効の効果 —— 法律の規定が代わる・WebFetch の逐語の片）** | `2026-11-18-bgb-306-gesetze-im-internet-snapshot.txt` |
| 2026-11-18 | 仏 Légifrance | **観測（トゥーボン法 2 条・5 条の第 1 段・フランス語の使用・WebFetch の逐語の片）** | `2026-11-18-loi-toubon-94-665-art-2-5-legifrance-snapshot.txt` |
| 2026-11-19 | 米 LII（17 U.S.C.・35 U.S.C.）・英 legislation.gov.uk（EU 指令） | **観測（17 U.S.C. の 101 条の定義・107 条・201 条 (d)・203 条・204 条 (a)、35 U.S.C. の 261 条・271 条 (a)、DSM 指令 2 条・3 条 1 項・7 条、DB 指令 9 条・WebFetch の逐語の片・2026-11-19 のオーナーの提案の 2f の分担）** | `2026-11-19-us-title-17-35-and-dsm-2-3-7-snapshot.txt` |
| 2017-02-13 | 英控訴院（Find Case Law・2026-11-17 取得） | **観測（Harvey v Dunbar Assets [2017] EWCA Civ 60 第 62 段落・約束的禁反言は盾であって剣でない・WebFetch）** | `2026-11-17-harvey-v-dunbar-2017-ewca-civ-60-promissory-estoppel-snapshot.txt` |
| 2026-11-16 | 日・独・英・仏の公式の条文サイト | **観測（特許の及ぶ行為: 特許法 2 条 3 項・PatG 9 条・Patents Act 1977 s.60(1)・CPI L613-3・WebFetch）** | `2026-11-16-patent-acts-jp-de-uk-fr-snapshot.txt` |
| 2026-11-16 | 独連邦司法省（gesetze-im-internet.de） | **観測（BGB 305 条 1 項・310 条・標準約款の定義と適用範囲・WebFetch の逐語の片）** | `2026-11-16-bgb-305-310-gesetze-im-internet-snapshot.txt` |
| 2026-11-16 | 日・英・独の公式の条文サイト | **観測（第三者のための契約: 民法 537 条・Contracts (Rights of Third Parties) Act 1999 s.1・BGB 328 条 1 項・WebFetch）** | `2026-11-16-third-party-beneficiary-minpo-537-crtpa-1999-bgb-328-snapshot.txt` |
| 2026-11-16 | デジタル庁（e-Gov 法令 API） | **観測（消費者契約法 2 条・8 条 1 項 1 号 2 号・8 条 3 項・WebFetch）** | `2026-11-16-shohisha-keiyaku-ho-2-8-e-gov-api-snapshot.txt` |
| 2026-11-20 | LII・gesetze-im-internet.de・WIPO Lex・WTO | **観測（35 U.S.C. 271・261 条、PatG 11・15 条、ベルヌ条約 5 条 2 項・6 条の 2、TRIPS 28・30 条・WebFetch）** | `2026-11-20-patent-usc-patg-berne-trips-snapshot.txt` |
| 2026-11-16 | 英 legislation.gov.uk | **観測（CDPA 1988 87 条 1〜4 項・90 条 1・3・4 項・同意と放棄と禁反言、許諾の承継人への拘束・WebFetch の逐語の片）** | `2026-11-16-cdpa-1988-s87-s90-legislation-gov-uk-snapshot.txt` |
| 2026-11-16 | 英 legislation.gov.uk | **観測（消費者権利法 2015 の 2 条・61 条・65 条・事業者と消費者の間の免責の規制・WebFetch の逐語の片）** | `2026-11-16-consumer-rights-act-2015-s2-s61-s65-legislation-gov-uk-snapshot.txt` |
| 2026-11-16 | 独連邦司法省（gesetze-im-internet.de） | **観測（UrhG 29 条・著作権の譲渡の不可と許される取引・WebFetch の逐語の片）** | `2026-11-16-urhg-29-gesetze-im-internet-snapshot.txt` |
| 2026-11-16 | 独・日・仏の公式の条文サイト | **観測（不当利得: BGB 812 条 1 項 1 文・民法 703 条・Code civil 1303 条と 1303-1 条・WebFetch）** | `2026-11-16-unjust-enrichment-bgb-812-minpo-703-code-civil-1303-snapshot.txt` |
| 2026-11-16 | 仏 Légifrance | **観測（CPI L121-1 条・L121-7 条・人格権の性質とソフトウェアの例外・WebFetch）** | `2026-11-16-cpi-l121-1-l121-7-legifrance-snapshot.txt` |
| 2026-11-16 | 英 legislation.gov.uk | **観測（UCTA 1977 1 条 3 項・2 条 1 項 2 項・免責の規制は事業上の責任に限る・WebFetch の逐語の片）** | `2026-11-16-ucta-1977-s1-s2-legislation-gov-uk-snapshot.txt` |
| 2026-11-16 | デジタル庁（e-Gov 法令 API） | **観測（民法 527・549・550 条、著作権法 59・60・63・63 条の 2・WebFetch）** | `2026-11-16-minpo-chosakukenho-e-gov-api-snapshot.txt` |
| 2026-11-16 | 仏 Légifrance | **観測（民法典 931 条・953 条・955 条・957 条・960 条・贈与の方式と撤回の事由・WebFetch の逐語の片）** | `2026-11-16-code-civil-931-953-955-957-960-legifrance-snapshot.txt` |
| 2026-11-16 | 独連邦司法省（gesetze-im-internet.de） | **観測（UrhG 14 条・30 条・39 条、BGB 1922 条・1967 条・人格権の変更の合意と死後の承継・WebFetch の逐語の片）** | `2026-11-16-urhg-14-30-39-bgb-1922-1967-gesetze-im-internet-snapshot.txt` |
| 2026-11-16 | 独連邦司法省（gesetze-im-internet.de） | **観測（BGB 530 条・533 条・327 条、UrhG 31a 条・贈与の撤回、未知の利用方法、デジタル製品の規定と自由なソフトウェア・WebFetch の逐語の片）** | `2026-11-16-bgb-530-533-327-urhg-31a-gesetze-im-internet-snapshot.txt` |
| 2026-11-16 | 独連邦司法省（gesetze-im-internet.de） | **観測（InsO 103 条・129 条 1 項・134 条・143 条・倒産の履行選択と無償の給付の否認・WebFetch の逐語の片）** | `2026-11-16-inso-103-129-134-143-gesetze-im-internet-snapshot.txt` |
| 2026-11-15 | OSI 理事会 | **観測（2026-09-24 の議事録・オーナーがブラウザから写した本文）** | `2026-11-15-osi-board-minutes-2026-09-24-snapshot.txt` |
| 2026-11-07 | SPDX | **観測（収録基準の現行と前の版）** | `2026-11-07-spdx-license-inclusion-guidelines-snapshot.txt` |
| 2003-03 | `license-discuss` | **観測（Public Domain を一覧に載せる求め・5 通）** | `2003-03-license-discuss-public-domain-on-the-list-observed.txt` |
| 2003-05 | `license-discuss` | **観測（Cowan 氏の 1 通・既に与えた許諾が取り消せないかは明らかでない）** | `2003-05-license-discuss-language-question-cowan-irrevocable-observed.txt` |
| 2003-05 | `license-discuss` | **観測（Cowan 氏の 1 通・許諾の維持を目的とする法人に移せば取り消せない）** | `2003-05-license-discuss-language-question-cowan-corporation-observed.txt` |
| 2003-05 | `license-discuss` | **観測（Cowan 氏の 1 通・取り消せないと書いても自分への約束で拘束しない）** | `2003-05-license-discuss-language-question-cowan-promise-observed.txt` |
| 2020-03〜04 | `license-review` | **観測（Unlicense の審査から引いた 4 通）** | `2020-03-to-04-license-review-unlicense-cited-observed.txt` |
| 2020-03 | `license-discuss` | **観測（Berkus 氏の 1 通・公開されたライセンスは共同体全体のもの）** | `2020-03-license-discuss-aal-berkus-name-belongs-community-observed.txt` |
| 2020-03 | `license-discuss` | **観測（Berkus 氏の 1 通・承認済みの AAL はもはや大きく使われていない）** | `2020-03-license-discuss-aal-berkus-no-significant-use-observed.txt` |
| 2020-03 | `license-discuss` | **観測（Smith 氏の 1 通・承認済みの AAL の作者は法律家ではないと OSI のサイトが書く）** | `2020-03-license-discuss-aal-smith-non-attorney-author-observed.txt` |
| 2020-03 | `license-discuss` | **観測（Chestek 氏の 1 通・license-review は本物のライセンスに限る、思考実験は license-discuss で）** | `2020-03-license-discuss-what-fits-chestek-thought-experiments-observed.txt` |
| 2026-10-17 | Hugging Face hub-docs | **観測（ライセンスの識別子の一覧・文書の写し）** | `2026-10-17-huggingface-hub-docs-licenses-snapshot.txt` |
| 2012-02 | `license-review` | **観測（CC0 が特許を除いた理由と大学の事情・6 通）** | `2012-02-license-review-cc0-patents-and-universities-observed.txt` |
| 2012-02 | `license-review` | **観測（CC への特許の相談・4 通）** | `2012-02-license-review-cc0-patent-consultation-observed.txt` |
| 2011-09 | `license-discuss` | **観測（Can OSI specify that public domain is open source?・4 通）** | `2011-09-license-discuss-can-osi-specify-public-domain-observed.txt` |
| 2011-12 | `license-review` | **観測（"Submitting MPL for Approval" から 1 通・Fogel 氏 2011-12-15）** | `2011-12-license-review-mpl2-fogel-proliferation-not-grounds-observed.txt` |
| 2018〜2019 | `license-discuss` | **観測（審査の手順の 2 本から引いた 4 通）** | `2018-to-2019-license-discuss-review-process-cited-observed.txt` |
| 2019-03 | `license-discuss` | **観測（The per se license constructor・全 15 通）** | `2019-03-license-discuss-per-se-license-constructor-observed.txt` |
| 2019-03 | `license-review` | **観測（Perens 氏の 1 通・法律家のボランティアの助けを得て出し直せ）** | `2019-03-license-review-whonix-perens-lawyer-volunteer-observed.txt` |
| 2019-03 | `license-review` | **観測（Fontana 氏の 1 通・v1.4 を共同体の合意と改訂の見込みの無さを理由に却下）** | `2019-03-license-review-cfsl-fontana-rejected-observed.txt` |
| 2020-04 | `license-discuss` | **観測（Certifying MIT-0・3 通）** | `2020-04-license-discuss-certifying-mit0-observed.txt` |
| 2025-03 | `license-review` | **観測（ModelGo の出力の通知の条項・4 通）** | `2025-03-license-review-modelgo-output-notice-observed.txt` |
| 2014〜2024 | `license-discuss` | **観測（公有・特許・AI の 3 本から引いた 11 通）** | `2014-to-2024-license-discuss-public-domain-patents-ai-cited-observed.txt` |
| 2011〜2017 | `license-discuss` / `license-review` | **観測（waive all rights と BSD + Patent から引いた 16 通・2 分割の 1/2 部）** | `2011-to-2017-license-lists-cc0-patents-and-bsd-patent-cited-observed-1of2.txt` |
| 2011〜2017 | `license-discuss` / `license-review` | **観測（waive all rights と BSD + Patent から引いた 16 通・2 分割の 2/2 部）** | `2011-to-2017-license-lists-cc0-patents-and-bsd-patent-cited-observed-2of2.txt` |
| 2011-05 | `license-discuss` | **観測（NASA の依頼の会話から 2 通・政府のコードがパブリックドメインなのは米国の中だけ、同意の無い人に条件はどう及ぶか）** | `2011-05-license-discuss-nasa-us-only-public-domain-observed.txt` |
| 1999〜2026 | `license-review` / `license-discuss` | **観測（未読スレッドから引いた 57 通・5 分割の 1/5 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`1999-to-2026-license-lists-unread-threads-cited-observed-1of5.txt` |
| 1999〜2026 | `license-review` / `license-discuss` | **観測（未読スレッドから引いた 57 通・5 分割の 2/5 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`1999-to-2026-license-lists-unread-threads-cited-observed-2of5.txt` |
| 1999〜2026 | `license-review` / `license-discuss` | **観測（未読スレッドから引いた 57 通・5 分割の 3/5 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`1999-to-2026-license-lists-unread-threads-cited-observed-3of5.txt` |
| 1999〜2026 | `license-review` / `license-discuss` | **観測（未読スレッドから引いた 57 通・5 分割の 4/5 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`1999-to-2026-license-lists-unread-threads-cited-observed-4of5.txt` |
| 1999〜2026 | `license-review` / `license-discuss` | **観測（未読スレッドから引いた 57 通・5 分割の 5/5 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`1999-to-2026-license-lists-unread-threads-cited-observed-5of5.txt` |
| 2004〜2026 | `license-review` / `license-discuss` | **観測（規則の全数から引いた 30 通・6 分割の 1/6 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`2004-to-2026-license-lists-rule-census-cited-observed-1of6.txt` |
| 2004〜2026 | `license-review` / `license-discuss` | **観測（規則の全数から引いた 30 通・6 分割の 2/6 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`2004-to-2026-license-lists-rule-census-cited-observed-2of6.txt` |
| 2004〜2026 | `license-review` / `license-discuss` | **観測（規則の全数から引いた 30 通・6 分割の 3/6 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`2004-to-2026-license-lists-rule-census-cited-observed-3of6.txt` |
| 2004〜2026 | `license-review` / `license-discuss` | **観測（規則の全数から引いた 30 通・6 分割の 4/6 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`2004-to-2026-license-lists-rule-census-cited-observed-4of6.txt` |
| 2004〜2026 | `license-review` / `license-discuss` | **観測（規則の全数から引いた 30 通・6 分割の 5/6 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`2004-to-2026-license-lists-rule-census-cited-observed-5of6.txt` |
| 2004〜2026 | `license-review` / `license-discuss` | **観測（規則の全数から引いた 30 通・6 分割の 6/6 部）** | 長い 2 通は署名までで切り、ヘッダにそう書いた。`2004-to-2026-license-lists-rule-census-cited-observed-6of6.txt` |
| 2013-04〜06 | `license-review` | **観測（法律家を要件にするかの議論・13 通・2 分割の 1/2 部）** | `2013-license-review-drafting-quality-cited-observed-1of2.txt` |
| 2013-04〜06 | `license-review` | **観測（法律家を要件にするかの議論・13 通・2 分割の 2/2 部）** | `2013-license-review-drafting-quality-cited-observed-2of2.txt` |
| 2022-07 | Fedora legal list / LWN / BleepingComputer / Fedora のデータ | **観測（CC0 をコードから外した判断と、いまのデータ）** | 最初の 1 通は取得できず、LWN と BleepingComputer の引用で置いた。`2022-07-fedora-legal-cc0-classification-observed.txt` |
| 2022-12 | `license-discuss` | **観測（Perens 氏の 1 通・より良いライセンスを作るのは弁護士資格を持つ人の仕事）** | `2022-12-license-discuss-retro-disapprove-perens-bar-observed.txt` |
| 2022-12 | `license-discuss` | **観測（Smith 氏の 1 通・起草の拙さとあいまいさは OSD の外の承認の要素）** | `2022-12-license-discuss-retro-disapprove-smith-drafting-observed.txt` |
| 2012-01〜04 | `license-review` | **観測（CC0 の審査から引いた 27 通・2 分割の 1/2 部）** | ドシエが引いた通だけを束ねた。スレッド全体ではない。`2012-01-to-04-license-review-cc0-cited-observed-1of2.txt` |
| 2012-01〜04 | `license-review` | **観測（CC0 の審査から引いた 27 通・2 分割の 2/2 部）** | 同じ束の 2/2 部。`2012-01-to-04-license-review-cc0-cited-observed-2of2.txt` |
| 2012-03 | `license-review` | **観測（CC0 の意向調査・全 25 通・2 分割の 1/2 部）** | 票数そのものが証拠なのでスレッドを全部置いた（規則 6）。`2012-03-license-review-cc0-straw-poll-observed-1of2.txt` |
| 2012-03 | `license-review` | **観測（CC0 の意向調査・全 25 通・2 分割の 2/2 部）** | 同じ束の 2/2 部。`2012-03-license-review-cc0-straw-poll-observed-2of2.txt` |
| 2014-04-15 | `license-review` | **観測（UPL の審査の 1 通）** | `2014-04-15-license-review-upl-cowan-observed.txt` |
| 2019-05〜06 | `license-review` / `license-discuss` | **観測（2019 年の通知と、その筆者たちの発言・10 通・2 分割の 1/2 部）** | `2019-05-license-lists-review-process-cited-observed-1of2.txt` |
| 2019-05〜06 | `license-review` / `license-discuss` | **観測（同じ束の 2/2 部）** | `2019-05-license-lists-review-process-cited-observed-2of2.txt` |
| 2019-05〜06 | `license-discuss` | **観測（2012 年の CC0 の審査を 7 年後に語った 6 通）** | `2019-05-license-discuss-cc0-retrospective-observed.txt` |
| 2018-12 | `license-review` | **観測（第 3 の帰結が選ばれた実例・2 通）** | **`board-decisions.md` が議事録から確立した「承認でも否決でもない第 3 の帰結」の、リスト側の実例。** Fontana 氏 *"I recommended that the OSI **reject** … Subsequently … the OSI decided to **withhold approval** … **pending submission of a redrafted version**"*／Phipps 氏（President）*"OSI's Board **does not give legal advice, practice law or design licenses** … we opted to **withhold approval instead (under the clarified process)**"*。**後者は §1.52（提出が弁護士の目を通す経路）の射程を狭める**（`against.md` #274）。**⚠ 両刃** —— 「否決されにくい」の証拠にも「決まらないまま置かれる」の証拠にもなる。 |
| 2018-12 | `license-discuss` | **観測（Perens 氏の 1 通・以前の理事会のいちばんの失敗は crayon license を受け入れたこと）** | `2018-12-license-discuss-decision-process-perens-crayon-ofl-observed.txt` |
| 2018-12 | `license-review` | **観測（Perens 氏の 1 通・問題は承認の欠如ではなく関心の欠如）** | `2018-12-license-review-sspl-support-perens-fairy-dust-observed.txt` |
| 2018-06 | `license-review` | **観測（Perens 氏の「提出者への注意書き」1 通・効果の重複は判例の新しい展開か明白な法的欠陥のためでなければ受け入れない、法律家なしでは裁判所での実行のされ方が分からない）** | `2018-06-license-review-perens-notes-for-submitters-observed.txt` |
| 2018-06 | `license-review` | **観測（NOSA 2.0 の会話から 2 通・作品全体に許諾する、プログラムの一部は機械の仕事、許諾は 1 つに統合された文書で）** | `2018-06-license-review-nosa-whole-work-machine-portions-observed.txt` |
| 2010-04 / 2017-04〜05 | `license-review` | **観測（我々の類型の提出 2 件・全 10 通・2 分割の 1/2 部）** | **全期間 census（199 か月）が挙げた 27 件のうち、ドシエ未言及だった 2 件。** **(B) の最初の実質返信は Fontana 氏の *"Do you see anything distinctive about your license relative to FPL/0BSD?"*** ——**Landley 氏が後に我々へ向けたのと同じ問いが 9 年前に在った**。**そして McCoy 氏が試験を言葉にしている** —— *"the wording they use in CC0 is **much more comprehensive** … The language you use is **quite brief**"*。**当てた結果は 5 要素中 4 つ被覆・1 つ未対応**（`review-doctrine.md` §1.129）。**(A) は我々の類型で返信ゼロの 1 例。** |
| 2010-04 / 2017-04〜05 | `license-review` | **観測（我々の類型の提出 2 件・2 分割の 2/2 部）** | **同じ束の 2/2 部。** 本文は無改変で、2 部を順に結合すれば元に戻る（分割は早期警告 800 行のため・**行境界**。**一次資料に予算行を与えるのではなく、下に収める**）|
| 2026-10-24 | `license-discuss` | **観測（OSEL 0.2 の議論依頼・我々宛ではない）** | **2026-10-27 03:04 UTC に portfolio-01 が取得。** OpenReciprocal が *"This is not a license-review submission"* と断って議論を求めた 1 通。commit を固定し *"I will not edit that file while it is under discussion"*、*"The text has not been reviewed by counsel. I am not a lawyer. No software project outside this repository uses the draft."* と開示する ——**提出の形は我々の 2026-08-26 とほぼ同じ**。中身は逆向き（より厳しい承認済みライセンスへの一方向の付け替え）。読みは `OSI-EVENTS-2026-10.md` の 10-27 行 |
| 2026-10-25 | `license-review` | **観測（ModelGo の投票の照会・我々宛ではない）** | **同上の取得。** Moming Duan 氏 *"Any word on the vote for MG0 and MG-BY?"* の 1 行（下は 9 月の議論の引用で読了済み・`review-doctrine.md` §1.123）。FINAL CALL の締切 2026-09-24 から約 1 か月、**steward が結果を知らない**ことを示す決定時期の実測材料 |
| 2026-09-27〜28 | `license-review` | **観測（Python ライセンスのスレッドの後続 3 通・我々宛ではない）** | **2026-10-04 11:41 UTC にローカルから取得。** Rikken 氏が Python-2.0.1 / CNRI-Python-GPL-Compatible の承認に謝意を述べ、OSI の一覧の SPDX ID 誤記を指摘／Mehl 氏 *"For PSF-2.0, I have filed a submission for review a few weeks ago, with no replies so far"*／Vidal 氏が誤記を修正。**採用実績のある提出（PSF-2.0）も約 3 週間返信ゼロ**という観測で、沈黙の基準率（#109）の側の 1 例。**⚠ 承認の日付はこのスレッドではなく OSI のライセンス頁（Approved: June 29, 2026）が権威** —— 2026-09-24 の理事会の結果ではない。分析は `OSI-EVENTS-2026-10.md` の取り込みログ。 |
| 2012-08 | `license-discuss` | **観測（著作権の放棄可能性・全 34 通・3 分割の 1/3 部）** | **ACD が立っている 2 問（著作権は放棄できるか / 「irrevocable」に何が残るか）を、リスト自身がどう扱ったか。****不利**: 実務弁護士 Lawrence Rosen 氏が *"If you want to worry about copyright law, consider **17 USC 203**"* と、我々が `jurisdictions.md` 5a で statute から見つけた当の条文を「心配すべき橋」として名指ししている。**有利**: Tom Callaway 氏（Fedora）が Red Hat Legal の結論として *"such a declaration, were it to go to trial, would likely **limit the effectiveness of the copyright 'holder' suing for infringement**"* ——**放棄の可否が不確かでも、明確な献呈は効果を持つ**（`jurisdictions.md` 5c） |
| 2012-08 | `license-discuss` | **観測（著作権の放棄可能性・全 34 通・3 分割の 2/3 部）** | **同じスレッドの 2/3 部。** 本文は無改変で、3 部を順に結合すれば元に戻る（分割は Check 365 の 1,000 行上限のため・**行境界**） |
| 2012-08 | `license-discuss` | **観測（著作権の放棄可能性・全 34 通・3 分割の 3/3 部）** | **同じスレッドの 3/3 部。** 本文は無改変で、3 部を順に結合すれば元に戻る（分割は Check 365 の 1,000 行上限のため・**行境界**） |
| 2020-05〜06 | `license-review` | **観測（Unlicense への反対・全 17 通）** | **依拠している先例に逆らった側の議論を、我々は持っていなかった**（理由書は `AS-OF.md` が逐語で持っていた）。実務弁護士 Stuart Langley 氏 *"**this is not a license** … a description of what the author thinks public domain means, **not a clear intent to convey rights**"* / *"conventional, **well-trodden language of license such as 'Licensor grants X rights....'**"*。**ACD-1.0 §4.1 はその形そのもの**（*"The Dedicator **grants You** …"*）で、**試験に通る**（`review-doctrine.md` §1.128）。**⚠ ただし同じ反対者は *"wide use without any problems is a big factor"* とも述べており、そちらに我々は答えられない。****⚠ そして反対は承認を止めなかった。** |
| 2020-05〜06 | `license-review` | **観測（Unlicense の承認の議論から 4 通・法律家が反対しなかったことを根拠に承認を検討、既に広く使われている、危険は他と量的に違わない）** | `2020-05-to-06-license-review-unlicense-attorneys-cleared-observed.txt` |
| 2005〜2007 | `license-discuss` | **観測（Ms-PL 審査・決める側 26 通・3 分割の 1/3 部）** | **#243 の census が挙げた最大の未読スレッド（331 通）から、決める側の 26 通だけを規則を明記して抜いた。****有利 1 件**: vanity の異議に理事会が *"does not give that argument much weight **as long as the license is reusable**"* と答えている（提出パケット §4b が答えている当の項目）。**不利 1 件**: Tiemann 氏（当時の会長）の評価関数 *"if a license is submitted with **promise X**, then we should **evaluate promise X as well as the OSD**"* ——**ACD の gap は存在理由であると同時に、測られる基準にもなる**（`review-doctrine.md` §1.127） |
| 2005〜2007 | `license-discuss` | **観測（Ms-PL 審査・決める側 26 通・3 分割の 2/3 部）** | **同じ束の 2/3 部。** 本文は無改変で、3 部を順に結合すれば抜き出した形に戻る（分割は Check 365 の 1,000 行上限のため・**行境界**） |
| 2005〜2007 | `license-discuss` | **観測（Ms-PL 審査・決める側 26 通・3 分割の 3/3 部）** | **同じ束の 3/3 部。** 本文は無改変で、3 部を順に結合すれば抜き出した形に戻る（分割は Check 365 の 1,000 行上限のため・**行境界**） |
| 2026-09-24 | `license-review` | **観測（ModelGo Attribution 2.0 FINAL CALL・9 通・3 分割の 1/3 部）** | **主題が最も近い同時代 instrument の、決定段階の区間。** `rounds/` は 09-08 までしか持っていなかった。**Chestek 氏（委員・元委員長）（**2026-10-17 訂正**: 旧文は「委員長」。発言者 Chestek 氏は 2025-03 まで委員長で、2025-04 から委員。この時点の委員長は McCoy Smith 氏。`rounds/` の本文ファイルは無改変のまま、この索引の要約だけを直した・`against.md` #186 の訂正注記）が公表基準 *"does not have terms that structurally put the licensor in a more favored position than any licensee"* を具体条項へ当てている唯一の実例**で、*"**This does put the licensor in a more favored position than a licensee**"* と述べている。McCoy 氏は *"the **canonical versions** of the license (which is what, ultimately, **OSI needs to be able to see** in order to ensure we know what it is is being approved/disapproved)"* と、**審査対象テキストが見える形で一致していること**を要求した（`review-doctrine.md` / `review-rules.md`）|
| 2026-09-24 | `license-review` | **観測（ModelGo Attribution 2.0 FINAL CALL・9 通・3 分割の 2/3 部）** | **同じスレッドの 2/3 部。** 本文は無改変で、3 部を順に結合すれば取得したバイト列が復元される（分割は Check 365 の 1,000 行上限のため・**行境界**で切ってある —— ここには 399 行の 1 通があり、メッセージ境界では 1,000 行を超える）|
| 2026-09-24 | `license-review` | **観測（ModelGo Attribution 2.0 FINAL CALL・9 通・3 分割の 3/3 部）** | **同じスレッドの 3/3 部。** 本文は無改変で、3 部を順に結合すれば取得したバイト列が復元される（分割は Check 365 の 1,000 行上限のため・**行境界**で切ってある —— ここには 399 行の 1 通があり、メッセージ境界では 1,000 行を超える）|
| 2026-09-14 | `license-review` | **観測（OpenMDW・2 通）** | **§1.78 が読んだ 2026-09-12 より後の区間。** Dolan 氏の束ね擁護 *"The **unit of open source licensing has always been the work as provided**"*（Apache-2.0 の特許終了は Work 全体に及ぶ、を論拠にする）と、Berkus 氏の「偶発的な侵害コピーはどう起きるか」8 経路（*"GenAI & Autocomplete"* を含む）。**どちらも両刃**で、前者は ACD の束ねに有利だが **Fontana 氏の *"flawed in its basic conception"* は終了より広い**、後者は #134 の重さを裏づける |
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
| 2014-05-04 | `license-discuss`（観測）| **Karl Fogel 氏の 1 通 → 観測保存** | *"would certify PD *when accompanied by* a particular patent non-assertion text"*。§3 と §8.6 の組み合わせに近い形への発言で、ドシエに記録が無かった |
| 2017-10-26 | `license-discuss`（観測）| **Christopher Sean Morrison 氏の 1 通 → 観測保存** | *"something close to public domain yet still addressing indemnification and contributor patent grants"*。受益者が少ないという反論（#284）に当たる需要の記述で、採用の実績ではない |
| 2017-10 | `license-review` | **観測（Phipps 氏の 1 通・OSI・FSF・Debian の全部に承認されるかは良い事前点検）** | `2017-10-license-review-l0r-phipps-preflight-observed.txt` |
| 2017-10 | `license-review` | **観測（Perens 氏の 1 通・使うだけの人には法的な負担を限りなく 0 に）** | `2017-10-license-review-l0r-perens-no-legal-load-observed.txt` |
| 2026-11-06 | **OSI の公式 FAQ（public domain / CC0 の 2 問）** | 一次資料 → 自己取得 | *"it's still not a license"* と、CC0 の最も重い懸念が clause 4(a) だったことを OSI 自身が述べている。ドシエは委員長の発言の中の URL としてしか触れていなかった |
| 2012-03-07 | **OSI 理事会の議事録（CC0 の結果の報告）** | 一次資料 → 取得物から切り出し | *"Recommend disapprove, due to clause 4a"*。CC0 が止まった理由の、組織の側の一次資料である |
| 2007-11-07 | **OSI 理事会の議事録（SimPL の報告）** | 一次資料 → 取得物から切り出し | 再ライセンスを許すライセンスは *"does not create a licensing dead-end"* と述べる。#84 への、理事会の言葉の答えである |
| 2024-12-18 | `license-review`（観測）| **Carlo Piana 氏の撤回の 1 通（PBZC 審査）→ 観測保存** | *"I stand corrected re: Pam's message on requiring legal review, bad choice of words on my side."* と *"I actually advise to use both"* が同じ 1 通に在る。2 か月間、撤回前の発言だけを不利な事実として数えていた（`ACD-1.0.against.md` #127）|
| 2026-09-04 | `license-review` | Moming Duan → 受領 | 上記 ModelGo 質問への回答（審査履歴 4 件を引用）|
| 2026-09-04 | `license-review` | 送信 | Dolan 氏の回答を受けた閾値問題の分解（返信なし）|
| 2026-09-04 | `license-review` | Shuji Sado → **引用** | 我々宛ではないが、我々の質問を明示的に引いて議論を進めている |
| 2026-09-05 | `license-review` | Ruby Anna → 受領 | ModelGo 側からの確認。**我々の 2026-09-05 12:31 送信を引用の形でのみ含む** |
| 2026-09-05 | `license-discuss` | 観測（3 通のスレッド）| 新規の単独参加者の短い質問に **約 4 時間で 1 通目**。比較対象として置く |
| 2026-09-06 | `license-discuss` | 送信 | **ACD-1.0 の 2 通目。§3 と §4 の関係だけに絞った 1 問**。本文は再送していない（凍結中・URL のみ）|
| 2026-09-06 | `license-discuss` | 送信 | **ACD-1.0 についてではない** —— 他者のネットワーク・コピーレフト質問への実質的回答（CPAL-1.0 / OSL-3.0）|
| 2026-09-07 | `license-review` | McCoy Smith → 公開の意見募集 | ModelGo 2 件への CALL FOR COMMENTS。**我々宛ではない**が、4 問はいずれも ACD-1.0 に構造上あたらない |
| 2026-09-07 | `license-review` | 観測（2 通）| Pamela Chestek 氏（Licensing Committee 委員・元委員長）が CALL FOR COMMENTS に対し**まず本文を要求**している（**2026-10-17 訂正**: 旧文は「委員長」。発言者 Chestek 氏は 2025-03 まで委員長で、2025-04 から委員。この時点の委員長は McCoy Smith 氏。`rounds/` の本文ファイルは無改変のまま、この索引の要約だけを直した・`against.md` #186 の訂正注記） |
| 2026-09-08 | `license-review` | Moming Duan → 参照 | 上記への steward 回答。**背景資料として「Yokoi-san」を 2 度引用**（我々宛ではない）|
| 2026-09-08 | `license-review` | Preston Maness → 観測 | OpenMDW への反対。**「AI モデルに関するあらゆるライセンス」への反対**として述べられている |
| 2026-09-07 | **リスト外（off-list）** | **Nick Vidal → 受領 + 送信（往復）** | **moderator が ACD-1.0 を名指しして 5 問を出し、「ACD-1.0 に関する次の提出の前に直接返信せよ」と求めた。steward は 5 問すべてに答えた。****公開アーカイブには存在しない** —— 2026-09-10 に steward が逐語で提供したもので、**それがこの記録の唯一の根拠である** |
| 2026-09-13 | — | **第三者ページのスナップショット** | **更新前の OSI Mailing List Code of Conduct 全文**（769 語・sha256 つき）。**2026-09-09 の通知が「AI の利用を反映するよう更新する」と予告した当の文書**で、更新後は live から取得できなくなる。**「保存済み」と記録しながら 1 節の引用しか無かった**のを是正した（#82 と同じ形）|
| 2026-09-12 〜 13 | **リスト外（off-list）** | **送信 + Nick Vidal → 受領 + 送信** | **moderator 往復の続き。** steward が「**substantive な review メッセージが 2 通 moderator に拒否され、ModelGo と BOS の提出者にフィードバックが届かなかった**」と報告し、その応答と steward の返信を含む。**公開アーカイブには存在しない。** ——**この記録により「アーカイブに我々の投稿が無い」は「送っていない」を意味しなくなった**（`against.md` #136）|
| 2026-09-09 | `license-discuss` | **OSI Moderators → 観測** | **AI 生成投稿は拒否すると宣言し、両リストが「AI が自律的に参加しライセンスを起草する proof-of-concept」に使われていると名指ししている。名前は出ていない** |
| 2026-09-09 | `license-review` | **OSI Moderators → 観測** | 同文（同日 09:58・両リストへ）|
| 2026-09-09 | `license-discuss` | **Bruce Perens → 観測（上の通知への唯一の返信）** | **内容は他の投稿者の表示名についての一言のみ。誰を指した通知かは述べていない** |
| 2026-09-10 | `license-review` | **Pamela Chestek（Licensing Committee 委員・元委員長）→ 名指し**（**2026-10-17 訂正**: 旧文は「委員長」。発言者 Chestek 氏は 2025-03 まで委員長で、2025-04 から委員。この時点の委員長は McCoy Smith 氏。`rounds/` の本文ファイルは無改変のまま、この索引の要約だけを直した・`against.md` #186 の訂正注記） | **我々宛ではない**（OpenMDW の審査中の発言）が、*"I would like to thank **Yuta-san** for their **insightful view on the termination provision**, which I find helpful"* と**名指しで謝辞している**。**moderator 通知（2026-09-09）の翌日である** |
| 2026-09-09 | `license-review` | Max Mehl → 観測 | **同日の新規提出（PSF-2.0）**。約 270 語で、**採用実績と既承認ライセンスとの関係**に依っている |
| 2026-09-20 | （リスト外）| **ACD-1.2 草案への外部レビュー（敵対的検証）→ 受領** | **2 回目の受け渡しで初めて届いた 3 件目。** **同日の他 2 件が指摘ゼロだったのに対し、条ごとに名前のある法源・判例を挙げて攻撃ベクターを述べる**（Kneschke v. LAION / Ryanair v PR Aviation / Qimonda / 17 U.S.C. §201(b) / DMCA §1202 / 消費者契約法 8 条 / droit de retrait / 不公正契約条項指令）。**我々はこれらをオフラインで確認できていない** ——`against.md` #170 に**未検証の研究キュー**として置いた |
| 2026-09-20 | （リスト外）| **ACD-1.2 草案への外部レビュー（好意的検証）→ 受領** | オーナー経由。**PDF 原本は `Check 122` により tracked できないので、抽出テキストを sha256 つきで保存**（本ファイルは原本ではない）。**全条項を「適切」「完璧」と評価し、欠陥の指摘は 1 件も無い** ——**その読みが establish するのは文書ではなくレビューの側である**（`against.md` #168）|
| 2026-09-20 | （リスト外）| **ACD-1.2 草案への外部レビュー（条項適切性）→ 受領** | 同上。**条ごとに「適切」の判定を並べる形式。****⚠ オーナーが共有した 3 ファイルのうち 2 つは byte 同一**（sha256 一致）で、**実体は 2 件である**（#168）|
| 2026-09-19 | （リスト外）| **第三者 AI レポート① 承認プロセスの調査 → 受領** | オーナー経由。**リストの発言ではないので、証拠ではなく*測り方*として扱う** |
| 2026-09-19 | （リスト外）| **第三者 AI レポート② 敵対的検証 → 受領** | **前提に事実誤りがある** ——解析対象を `against.md` と取り違えている（`against.md` #158）|
| 2026-09-19 | （リスト外）| **第三者 AI レポート③ 好意的検証 → 受領** | **「クレヨン・ライセンス」の語を運んできた** ——アーカイブで実在を確認し、委員長の発言に到達した（`review-labels.md` §1.98）|
| 2026-09-22 | （リスト外）| **ACD-1.2 草案への外部レビュー（OSI 承認準備）→ 受領** | オーナー経由。**渡されたレビュー対象が現行 `ACD-1.2-DRAFT.txt` と sha256 一致**（`1356b2b0…`）—— **この評は現行の byte に当たっている**（09-20 の 3 件は PDF 抽出で、`against.md` #167 の破損ヘッダを含む版を読んでいた）。**確定した実欠陥 1 件**: 冒頭が「1.1 と同一」と述べたまま下に 9 件の変更が並んでいた（`against.md` #207・**4 日間偽で、09-20 の 3 件は報告していない**）。**5 条の指摘のうち §6.2 / §6.3 は、勧める分離が既に本文にある** |
| 2001-11 | `license-discuss`（観測）| **Intel's proposed BSD + Patent License → 観測保存（1of4 部）** | **特許許諾を GPL の OS に条件づけた 2001 年版が OSD 3 / 6 / 8 で争われ、承認されなかった。** 2016 年の無条件版は承認されている（`2016-01-...` を参照）。**ACD §8.2 が無条件・終了不能である理由に当たる。** |
| 2002-01 | `license-discuss` | **観測（"Advertising Clauses in Licenses" から 1 通・Perens 氏 2002-01-20）** | `2002-01-license-discuss-advertising-perens-run-observed.txt` |
| 2002-01 | `license-discuss` | **観測（"Advertising Clauses in Licenses" から 1 通・Rosen 氏 2002-01-20）** | `2002-01-license-discuss-advertising-rosen-praise-observed.txt` |
| 2002-01 | `license-discuss` | **観測（"NCSA Open Source License" から 1 通・Rosen 氏 2002-01-20）** | `2002-01-license-discuss-ncsa-rosen-no-opinion-observed.txt` |
| 2002-02 | `license-discuss` | **観測（"Advertising Clauses in Licenses" から 1 通・Nelson 氏 2002-02-13）** | `2002-02-license-discuss-advertising-nelson-use-observed.txt` |
| 2002-03 | `license-discuss` | **観測（"Static v. Dynamic Linking -- redux" から 1 通・Nelson 氏 2002-03-16）** | `2002-03-license-discuss-static-dynamic-nelson-interpret-observed.txt` |
| 2002-03 | `license-discuss` | **観測（"OSD modification regarding what license can require of user" から 1 通・Perens 氏 2002-03-13）** | `2002-03-license-discuss-osd-modification-perens-not-no-use-observed.txt` |
| 2002-03 | `license-discuss` | **観測（"OSD modification regarding what license can require of user" から 1 通・Nelson 氏 2002-03-16）** | `2002-03-license-discuss-osd-modification-nelson-use-restricted-observed.txt` |
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
| 2014〜2018 | `license-review` | **観測（3 つの提出から 3 通・知らない受益者は成り立つか、直接の許諾は privity を避ける、受益者は契約法の特別な意味を持つ）** | `2014-to-2018-license-review-third-party-beneficiary-privity-observed.txt` |
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
| 2009-04 | `license-review` | **観測（"License Committee Report for April 2009" から 1 通・Prabhakar 氏 2009-03-31）** | `2009-04-license-review-committee-report-prabhakar-net-benefit-observed.txt` |
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
| 1999〜2010 | `license-discuss` | **観測（4 つの会話から 4 通・改変した本文に元の名を使うな、名前は商標で守る、Steward の役割は譲れる〔CPL・EPL〕）** | `1999-to-2010-license-discuss-licence-name-and-steward-assignment-observed.txt` |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（1/22 部）** | **記録の中で、単独の起草者による審査がいちばん長く続いた例**（15 か月・220 通）で、**結末は「委員長が却下を勧告 → 提出者が事実上取り下げ → 理事会は決定せず」**。**OSD に書かれていない審査基準が、参加者自身の言葉で列挙されている** —— Moen 氏 *"**vanity license or duplicative** ... **needlessly specific to one business entity** ... **unjustifiably opaque or ambiguous** ... **was not drafted with a lawyer**"*、Villa 氏（元理事）*"OSI approval is a **political game, not an actual objective test**"*（#248） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（2/22 部）** | **同じ束の 2/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（3/22 部）** | **同じ束の 3/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（4/22 部）** | **同じ束の 4/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（5/22 部）** | **同じ束の 5/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（6/22 部）** | **同じ束の 6/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（7/22 部）** | **同じ束の 7/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（8/22 部）** | **同じ束の 8/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（9/22 部）** | **同じ束の 9/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（10/22 部）** | **同じ束の 10/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（11/22 部）** | **同じ束の 11/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（12/22 部）** | **同じ束の 12/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（13/22 部）** | **同じ束の 13/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（14/22 部）** | **同じ束の 14/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（15/22 部）** | **同じ束の 15/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（16/22 部）** | **同じ束の 16/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（17/22 部）** | **同じ束の 17/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（18/22 部）** | **同じ束の 18/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（19/22 部）** | **同じ束の 19/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（20/22 部）** | **同じ束の 20/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（21/22 部）** | **同じ束の 21/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-09 | `license-review`（観測）| **License Zero Reciprocal (L0-R) の承認審査 220 通 → 観測保存（22/22 部）** | **同じ束の 22/22 部。** 本文は無改変で、22 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（1/15 部）** | **理事会が承認の際に準拠法条項について自分の立場を述べている** —— *"it does not believe that **choice of law provisions are necessary or advisable** in open source licenses"*（2023-03-18）。**ACD-1.0 §15.7 は置いていない**（#254）。**法律事務所が起草に同伴した提出でも承認まで 11 か月・3 版**を要し、Kuhn 氏が vanity の 2 段判定を述べている（#255） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（2/15 部）** | **同じ束の 2/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（3/15 部）** | **同じ束の 3/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（4/15 部）** | **同じ束の 4/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（5/15 部）** | **同じ束の 5/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（6/15 部）** | **同じ束の 6/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（7/15 部）** | **同じ束の 7/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（8/15 部）** | **同じ束の 8/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（9/15 部）** | **同じ束の 9/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（10/15 部）** | **同じ束の 10/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（11/15 部）** | **同じ束の 11/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（12/15 部）** | **同じ束の 12/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（13/15 部）** | **同じ束の 13/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（14/15 部）** | **同じ束の 14/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-04 | `license-review`（観測）| **Open Logistics License の承認審査 106 通（v1.1〜v1.3・2023-03 承認） → 観測保存（15/15 部）** | **同じ束の 15/15 部。** 本文は無改変で、15 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2020-12 | `license-review`（観測）| **ViraTrace Public Source License と GDPR × ライセンス条項 35 通 → 観測保存（1/6 部）** | **データ保護法とライセンスの境界について、Chief Privacy Officer の明確な一文** —— Turner 氏 *"data protection law ... is about ... organisations **in control of personal data** ... **software licensors are not part of the picture**"*。**§1.5 が Covered Rights にデータ保護を含めず §11.4 が "It reaches nothing else" と述べることの外からの裏づけ**（#256）。**McCoy Smith 氏の *"Freedom Zero ... inherently, part of the OSD"* も在る**（#248 / #251 の line） |
| 2020-12 | `license-review` | **観測（Brasseur 氏の 1 通・SPDX は既存の団体との混同を避けて識別子を変えた）** | `2020-12-license-review-oin-brasseur-spdx-identifier-observed.txt` |
| 2020-12 | `license-review` | **観測（Berkus 氏の 1 通・承認の投票の前に、既存の団体と重なる略称の変更を求める）** | `2020-12-license-review-oin-berkus-acronym-observed.txt` |
| 2020-12 | `license-review` | **観測（Phipps 氏の 1 通・OSI に承認されることがなぜ大事なのか簡潔に説明してほしい）** | `2020-12-license-review-viratrace-phipps-why-approval-observed.txt` |
| 2020-12 | `license-review`（観測）| **ViraTrace Public Source License と GDPR × ライセンス条項 35 通 → 観測保存（2/6 部）** | **同じ束の 2/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2020-12 | `license-review`（観測）| **ViraTrace Public Source License と GDPR × ライセンス条項 35 通 → 観測保存（3/6 部）** | **同じ束の 3/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2020-12 | `license-review`（観測）| **ViraTrace Public Source License と GDPR × ライセンス条項 35 通 → 観測保存（4/6 部）** | **同じ束の 4/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2020-12 | `license-review`（観測）| **ViraTrace Public Source License と GDPR × ライセンス条項 35 通 → 観測保存（5/6 部）** | **同じ束の 5/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2020-12 | `license-review`（観測）| **ViraTrace Public Source License と GDPR × ライセンス条項 35 通 → 観測保存（6/6 部）** | **同じ束の 6/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（1/23 部）** | **「承認でも否決でもない留め置き」の記録上いちばん長い実例** —— 委員長 Fontana 氏 2017-01-05 *"NOSA 2.0 [1] has been **languishing in a limbo review state for an extremely long time**"*（提出から 3 年半）+ *"it was contrary to **de facto OSI policy to reject a license outright**"*（#257）。**copyfraud（17 U.S.C. §506(c)）の分析と、Glaser 氏の *"even US government work may be copyright-protected e.g. in Germany. So, in the end, we need a copyright licence period."* も在る** ——**§3 と §4 を並置する理由そのもの**（#258） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（2/23 部）** | **同じ束の 2/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（3/23 部）** | **同じ束の 3/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（4/23 部）** | **同じ束の 4/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（5/23 部）** | **同じ束の 5/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（6/23 部）** | **同じ束の 6/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（7/23 部）** | **同じ束の 7/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（8/23 部）** | **同じ束の 8/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（9/23 部）** | **同じ束の 9/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（10/23 部）** | **同じ束の 10/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（11/23 部）** | **同じ束の 11/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（12/23 部）** | **同じ束の 12/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（13/23 部）** | **同じ束の 13/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（14/23 部）** | **同じ束の 14/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（15/23 部）** | **同じ束の 15/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（16/23 部）** | **同じ束の 16/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（17/23 部）** | **同じ束の 17/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（18/23 部）** | **同じ束の 18/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（19/23 部）** | **同じ束の 19/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（20/23 部）** | **同じ束の 20/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（21/23 部）** | **同じ束の 21/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（22/23 部）** | **同じ束の 22/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review`（観測）| **NASA Open Source Agreement 2.0 の審査と派生議論 225 通（2013〜2018） → 観測保存（23/23 部）** | **同じ束の 23/23 部。** 本文は無改変で、23 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2013-06 | `license-review` | **観測（"License drafting quality and process" から 5 通・多段階の承認とまず license-discuss、使用の数を要件にすれば萎縮、断る手段が無い、新しいライセンスの基準率）** | `2013-06-license-review-drafting-quality-and-process-observed.txt` |
| 2017-11 | `license-review`（観測）| **Unicode の 2 つの承認 16 通（2018 legacy / 2023 v3） → 観測保存（1/3 部）** | **OSI は「data files」を主題に明記したライセンスを 2 度承認している**（2018 legacy / 2023 v3・どちらもカテゴリつき）——**B15 にとってフォントに続く 2 つ目の counterweight**（#259）。**2023 年の提出は「一般化」を目的に明記し、著作権表示を *"fill in the blanks"* にした本文で承認された** ——*"to **genercize it so that it may be used by entities other than the Unicode Consortium**"*（#260） |
| 2017-11 | `license-discuss` | **観測（Morrison 氏の 1 通・CC0 には特許の条を消すか特許の許諾を組み込め）** | `2017-11-license-discuss-cc0-request-morrison-patent-observed.txt` |
| 2017-11 | `license-discuss` | **観測（Ingo 氏の 1 通・ソフトウェアには承認済みのライセンスを、CC0 が承認されなかった理由は特許の除外）** | `2017-11-license-discuss-cc0-request-ingo-observed.txt` |
| 2018-05 | `license-review` | **観測（Perens 氏の 1 通・論点を本文でなく FAQ で答える応答への評価は「meh」）** | `2018-05-license-review-esa-pl-perens-faq-not-text-observed.txt` |
| 2017-11 | `license-review` | **観測（Berkus 氏の 1 通・承認済みに無いことを複数するライセンスの審査は速くも簡単でもない）** | `2017-11-license-review-l0r-berkus-novel-not-fast-observed.txt` |
| 2017-11 | `license-review`（観測）| **Unicode の 2 つの承認 16 通（2018 legacy / 2023 v3） → 観測保存（2/3 部）** | **同じ束の 2/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2017-11 | `license-review`（観測）| **Unicode の 2 つの承認 16 通（2018 legacy / 2023 v3） → 観測保存（3/3 部）** | **同じ束の 3/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-03 | `license-review`（観測）| **YATeam Public License v1 の否決 9 通（2023-09-15 理事会） → 観測保存（1/5 部）** | **否決の Rationale Document が逐語で在る** —— *"**Unless a license meets the OSD in every possible iteration, it cannot be approved** as an open source license. **The license is also unintelligible in the English language version.**"* ——**英語としての不可解さが実際の否決理由として書かれている**。二言語ライセンスについて Chestek 氏 *"translations shouldn't be part of the formal agreement"*（#261） |
| 2022-03 | `license-review`（観測）| **YATeam Public License v1 の否決 9 通（2023-09-15 理事会） → 観測保存（2/5 部）** | **同じ束の 2/5 部。** 本文は無改変で、5 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-03 | `license-review`（観測）| **YATeam Public License v1 の否決 9 通（2023-09-15 理事会） → 観測保存（3/5 部）** | **同じ束の 3/5 部。** 本文は無改変で、5 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-03 | `license-review`（観測）| **YATeam Public License v1 の否決 9 通（2023-09-15 理事会） → 観測保存（4/5 部）** | **同じ束の 4/5 部。** 本文は無改変で、5 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2022-03 | `license-review`（観測）| **YATeam Public License v1 の否決 9 通（2023-09-15 理事会） → 観測保存（5/5 部）** | **同じ束の 5/5 部。** 本文は無改変で、5 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-05 | `license-review`（観測）| **Master-Console's Open-Source Definitive License の取り下げ 15 通 → 観測保存（1/2 部）** | **非弁護士の起草に対する記録上いちばん鋭い警告** —— Perens 氏 *"**Jacobsen v. Katzer** ... **tens of thousands of dollars in losses and five years of hardship in court** ... an **active disservice to the programmers of the world** ... **So, please get a lawyer to write a license for you.**"*。**そして委員長が示した経路（取り下げ → license-discuss → 再提出）は、我々がいま辿っている経路そのもの**（#262） |
| 2019-05 | `license-review`（観測）| **Master-Console's Open-Source Definitive License の取り下げ 15 通 → 観測保存（2/2 部）** | **同じ束の 2/2 部。** 本文は無改変で、2 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2008-12 | `license-review`（観測）| **Transitive Grace Period Public Licence の審査 134 通（未承認） → 観測保存（1/8 部）** | **「OSD 適合は十分条件ではない」の理由が、当時の OSI 会長の言葉で述べられている唯一の場所** —— Nelson 氏 *"There are **reasons beyond OSD conformance** ... **Because we have a trademark to preserve.** If you can figure out some way to **comply with the OSD in a way that does not achieve the desired open source effect** ... **then we MUST deny your license OSI approval (trademark law gives us no choice)**."* + *"**Somebody has to decide what OSD conformance means. It's us.**"*（#263） |
| 2008-12 | `license-review` | **観測（"For Approval: Transitive Grace Period Public Licence" から 1 通・Phipps 氏 2008-12-15）** | `2008-12-license-review-tgppl-phipps-reasons-beyond-osd-observed.txt` |
| 2008-12 | `license-review`（観測）| **Transitive Grace Period Public Licence の審査 134 通（未承認） → 観測保存（2/8 部）** | **同じ束の 2/8 部。** 本文は無改変で、8 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2008-12 | `license-review`（観測）| **Transitive Grace Period Public Licence の審査 134 通（未承認） → 観測保存（3/8 部）** | **同じ束の 3/8 部。** 本文は無改変で、8 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2008-12 | `license-review`（観測）| **Transitive Grace Period Public Licence の審査 134 通（未承認） → 観測保存（4/8 部）** | **同じ束の 4/8 部。** 本文は無改変で、8 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2008-12 | `license-review`（観測）| **Transitive Grace Period Public Licence の審査 134 通（未承認） → 観測保存（5/8 部）** | **同じ束の 5/8 部。** 本文は無改変で、8 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2008-12 | `license-review`（観測）| **Transitive Grace Period Public Licence の審査 134 通（未承認） → 観測保存（6/8 部）** | **同じ束の 6/8 部。** 本文は無改変で、8 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2008-12 | `license-review`（観測）| **Transitive Grace Period Public Licence の審査 134 通（未承認） → 観測保存（7/8 部）** | **同じ束の 7/8 部。** 本文は無改変で、8 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2008-12 | `license-review`（観測）| **Transitive Grace Period Public Licence の審査 134 通（未承認） → 観測保存（8/8 部）** | **同じ束の 8/8 部。** 本文は無改変で、8 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（1/61 部）** | **アーカイブ中で最大の提出スレッド。** ドシエは CAL-1.0 の**本文**を分析していたが、その**審査**は一度も読んでいなかった（**「言及 ≠ 読了」**・#264）。**委員長が反対意見を繰り返し条文と OSD へ差し戻している** —— *"Can you explain **what OSD is not met and where you find that in the license**?"*。**2020-02-14 の理事会で承認**（賛成 8・反対 0・棄権 1・欠席 2） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（2/61 部）** | **同じ束の 2/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（3/61 部）** | **同じ束の 3/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（4/61 部）** | **同じ束の 4/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（5/61 部）** | **同じ束の 5/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（6/61 部）** | **同じ束の 6/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（7/61 部）** | **同じ束の 7/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（8/61 部）** | **同じ束の 8/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（9/61 部）** | **同じ束の 9/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（10/61 部）** | **同じ束の 10/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（11/61 部）** | **同じ束の 11/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（12/61 部）** | **同じ束の 12/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（13/61 部）** | **同じ束の 13/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（14/61 部）** | **同じ束の 14/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（15/61 部）** | **同じ束の 15/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（16/61 部）** | **同じ束の 16/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（17/61 部）** | **同じ束の 17/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（18/61 部）** | **同じ束の 18/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（19/61 部）** | **同じ束の 19/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（20/61 部）** | **同じ束の 20/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（21/61 部）** | **同じ束の 21/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（22/61 部）** | **同じ束の 22/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（23/61 部）** | **同じ束の 23/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（24/61 部）** | **同じ束の 24/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（25/61 部）** | **同じ束の 25/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（26/61 部）** | **同じ束の 26/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（27/61 部）** | **同じ束の 27/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（28/61 部）** | **同じ束の 28/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（29/61 部）** | **同じ束の 29/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（30/61 部）** | **同じ束の 30/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（31/61 部）** | **同じ束の 31/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（32/61 部）** | **同じ束の 32/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（33/61 部）** | **同じ束の 33/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（34/61 部）** | **同じ束の 34/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（35/61 部）** | **同じ束の 35/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（36/61 部）** | **同じ束の 36/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（37/61 部）** | **同じ束の 37/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（38/61 部）** | **同じ束の 38/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（39/61 部）** | **同じ束の 39/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（40/61 部）** | **同じ束の 40/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（41/61 部）** | **同じ束の 41/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（42/61 部）** | **同じ束の 42/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（43/61 部）** | **同じ束の 43/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（44/61 部）** | **同じ束の 44/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（45/61 部）** | **同じ束の 45/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（46/61 部）** | **同じ束の 46/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（47/61 部）** | **同じ束の 47/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（48/61 部）** | **同じ束の 48/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（49/61 部）** | **同じ束の 49/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（50/61 部）** | **同じ束の 50/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（51/61 部）** | **同じ束の 51/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（52/61 部）** | **同じ束の 52/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（53/61 部）** | **同じ束の 53/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（54/61 部）** | **同じ束の 54/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（55/61 部）** | **同じ束の 55/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（56/61 部）** | **同じ束の 56/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（57/61 部）** | **同じ束の 57/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（58/61 部）** | **同じ束の 58/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（59/61 部）** | **同じ束の 59/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（60/61 部）** | **同じ束の 60/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2019-04 | `license-review`（観測）| **Cryptographic Autonomy License の承認審査 585 通 → 観測保存（61/61 部）** | **同じ束の 61/61 部。** 本文は無改変で、61 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2004-09 | `license-discuss`（観測）| **Allegro Giftware License の承認相談 11 通 → 観測保存（1/1 部）** | **proliferation の反対が「すべてを与える」ライセンスへ向けられている唯一の記録** —— Moen 氏 *"even an extremely permissive one like yours ... **needlessly putting it in a ghetto of your devising**"*。**そして「献呈 + 許諾の組み合わせ」を出すという発想が 2004 年に在る** —— Rousskov 氏 *"a **'Public Domain or whatever license you want' dedication/license combo** for OSI approval"*（#253）|
| 2001-06 | `license-discuss`（観測）| **qmail のライセンスと OSD 4 21 通 → 観測保存（1/2 部）** | **OSD 3 の後半が実際に判定の決め手として使われている例**（Moen 氏 *"OSD clause #3, immediately preceding, strikes me as disambiguating this."*）。**条件一般について Cowan 氏** —— *"a claim that 'X must allow Y' is satisfied by a statement by X that 'Y is allowed under conditions Z' **can't be true in general, since the conditions Z can be arbitrarily restrictive**."*（#251） |
| 2001-06 | `license-discuss`（観測）| **qmail のライセンスと OSD 4 21 通 → 観測保存（2/2 部）** | **同じ束の 2/2 部。** 本文は無改変で、2 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2004-09 | `license-discuss`（観測）| **Academic Citing License の相談 36 通 → 観測保存（1/3 部）** | **「使用の制限は OSD に無い」ことをリストが自分で認めている場所** —— Prodromou 氏 *"It'd be more accurate to say **'no restrictions on use not covered by copyright law.'**"*。**そして我々の類型についての知覚が記録されている** —— Moen 氏の 800 件の audit で *"'public domain' did indeed comprise an **overwhelming majority of those with serious licensing problems**"*、逆側に Cowan 氏 *"they aren't licensed at all. **But they are clearly Open Source.**"*（#250 / #251） |
| 2004-09 | `license-discuss`（観測）| **Academic Citing License の相談 36 通 → 観測保存（2/3 部）** | **同じ束の 2/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2004-09 | `license-discuss`（観測）| **Academic Citing License の相談 36 通 → 観測保存（3/3 部）** | **同じ束の 3/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2009-02 | `license-review`（観測）| **IPA Font License v1.0 の承認審査 41 通（2025-09 の後日談を含む） → 観測保存（1/3 部）** | **`review-precedents.md` §1.105 が「記録に在る唯一の日本発の提出」と述べていたのは誤りで、これが 2 件目である —— しかも承認されている**（#242）。提出者は **Mori Hamada & Matsumoto の弁護士**が**IPA を代理**しており、**成功した日本の先例には弁護士が付いていた**。**Swiger 氏は "Non-reusable licenses" カテゴリへの収容を勧めたうえで承認を推している** ——**再利用の見込みの無さは却下ではなく分類で処理された** |
| 2009-03 | `license-review` | **観測（Perens 氏・本気のライセンスは法律家の審査を経る・1 通）** | `2009-03-license-review-perens-serious-licence-legal-review-observed.txt` |
| 2009-03 | `license-review` | **観測（"Revised License Committee Report for March 2009" から 1 通・Nelson 氏 2009-03-14・WTFPL）** | `2009-03-license-review-wtfpl-nelson-no-reason-to-exist-observed.txt` |
| 2009-02 | `license-review`（観測）| **IPA Font License v1.0 の承認審査 41 通（2025-09 の後日談を含む） → 観測保存（2/3 部）** | **同じスレッドの 2/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2009-02 | `license-review`（観測）| **IPA Font License v1.0 の承認審査 41 通（2025-09 の後日談を含む） → 観測保存（3/3 部）** | **同じスレッドの 3/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界**） |
| 2006-07 | `license-discuss`（観測）| **Broad Institute Public License（BIPL）の承認審査 28 通 → 観測保存（1/3 部）** | **特許について、我々に有利な発言と不利な発言が同じスレッドに在る。** Rosen 氏 *"many people hope that the old BSD- and MIT-style licenses have 'implicit patent licenses,' but that's **a thin reed** ... All modern, professionally-written open source licenses ... contain explicit patent grants."* に対し、提出者側弁護士 Rivard 氏 *"The requirements for OSI certification do not include a requirement that the originator of the software offer a license to originator owned patents."*（#236 の 4 人に続く 5 人目）。**Unlicense 先例への依拠に当たるもの**も在る —— Dillard 氏 *"there are some previously approved licenses that would not be approved if submitted today"*（#238 / #239） |
| 2006-07 | `license-discuss`（観測）| **Broad Institute Public License（BIPL）の承認審査 28 通 → 観測保存（2/3 部）** | **同じスレッドの 2/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-07 | `license-discuss`（観測）| **Broad Institute Public License（BIPL）の承認審査 28 通 → 観測保存（3/3 部）** | **同じスレッドの 3/3 部。** 本文は無改変で、3 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（1/6 部）** | **Rosen 氏の、特許条項そのものに向けられた proliferation 反対** —— *"I don't think there's much enthusiasm to come up with yet another way to say these things about patents."* **ACD-1.0 §8.4 は「特許について言う、もう一つの言い方」そのものである**（#239） |
| 2006-11 | `license-discuss` | **観測（Tiemann 氏・表示は偽らないことが芯・1 通）** | `2006-11-license-discuss-tiemann-attribution-misrepresented-observed.txt` |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（2/6 部）** | **同じスレッドの 2/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（3/6 部）** | **同じスレッドの 3/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（4/6 部）** | **同じスレッドの 4/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（5/6 部）** | **同じスレッドの 5/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2006-11 | `license-discuss`（観測）| **Biological Open Source（BiOS）の非ソフトウェア特許ライセンス相談 11 通 → 観測保存（6/6 部）** | **同じスレッドの 6/6 部。** 本文は無改変で、6 部を順に結合すれば元の連続に byte 単位で戻る（**分割は行境界** —— 単一メッセージが Check 365 の 1,000 行上限を超えるため） |
| 2023-02 | `license-review`（観測）| **Mulan Open Works Licenses 4 本の承認審査 14 通 → 観測保存（1/11 部）** | **理事会が実際に不承認を議決した、我々の時代にいちばん近い審査。** 委員長 Chestek 氏が **CC0 が承認されていない理由**を名指しし（*"they expressly state that they do not grant a patent license. This is the reason that the CC-0 license is not an OSI-approved license ... although it has not been definitively decided due to Creative Commons' withdrawal"*）、**不承認の理由は OSD 違反ではなく主題**だった（*"open culture licenses are outside the purview of the Open Source Initiative"*）。その主題の定義は *"...an audiovisual work, a graphic work, and a model work"* で、**ACD-1.0 §1.2 の列挙は "audiovisual material" を含む**（#237 / #238） |
| 2023-02 | `license-discuss` | **観測（Chestek 氏の 1 通・放棄できない責任と、「法の許す限り」の句が国によっては句ごと無視されること）** | `2023-02-license-discuss-unless-required-chestek-unwaivable-observed.txt` |
| 2023-08 | `license-review` | **観測（Smith 氏の 1 通・特許の否認は承認できない、コンテンツのライセンスを除くなら方針として決めよ）** | `2023-08-license-review-mulan-owl-smith-content-patent-observed.txt` |
| 2023-08 | `license-review` | **観測（Berkus 氏の 1 通・コンテンツのライセンスの承認の基準は未整備で、作るのは大きな作業）** | `2023-08-license-review-mulan-owl-berkus-content-criteria-observed.txt` |
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
| 2023〜2025 | `license-review` | **観測（3 つの提出から 3 通・直した版は新しいスレッドで、1 つの完全な本文で、変更は番号つきの一覧で）** | `2023-to-2025-license-review-revised-versions-and-diffs-observed.txt` |
| 2025-09-11 | `license-review`（観測）| **委員会の Tiwaz への保留（Berkus 氏の報告）→ 観測保存** | *"voted to \*defer\* any recommendation"* と、解く条件 *"one or more projects begin using this license or express an interest in doing so"* が在る。B2 に効く決定で、窓の外にあって 14 か月未収録だった（`board-decisions.md` §2c / `against.md` #285）|
| 2025-09 | `license-review` | **観測（Smith 氏の 1 通・語の使い方の不一致）** | `2025-09-license-review-mgb-smith-inconsistent-terminology-observed.txt` |
| 2025-10 | `license-review` | **観測（Orivex への Piana 氏の所見 1 通・licensor と貢献者の扱いの差は OSD 5 に触れうる、改変物を頒布する語）** | `2025-10-license-review-orivex-licensor-contributor-observed.txt` |
| 2025-10 | `license-discuss` | **観測（PUWL の草案から 4 通・人格権は放棄＋不行使の約束＋虚偽の著者表示の除外＋可分、特許の許諾は CC0 との違い）** | `2025-10-license-discuss-puwl-moral-rights-observed.txt` |
| 2024-12-23 | `license-review`（観測）| **OSC License の提出の 1 通 → 観測保存** | *"there are currently no projects using the license. However, it is planned that the license will be used in mid/late January."* 計画段階の利用で承認された例である（`board-decisions.md` §2c）|
| 2026-06-19 | `license-review`（観測）| **Carlo Piana 氏の Linkumori への 1 通 → 観測保存** | *"not having an active project with an urgency to adopt a license or to have it approved, I would suggest deferring license review"*。個人の自著の利用が足りるとは限らないことの逆側である（`board-decisions.md` §2c）|
| 2020-08-04 | `license-review`（観測）| **委員会の MIT-0 の勧告と Rationale Document → 観測保存** | *"this is not a basis for rejection that the OSI has applied in the past (and the OSI has historically approved newly drafted licenses not yet in use)"*。理事会はこの勧告どおり承認した（`board-decisions.md` §2d）|
| 2020-10 | `license-review` | **観測（Brasseur 氏の 1 通・リストの参加者は相談すべき法律家の代わりを務めない）** | `2020-10-license-review-digest95-brasseur-consult-lawyer-observed.txt` |
| 2020-02 | `license-discuss` | **観測（委員長の Chestek 氏の 1 通・書いた本人が説明し、代理人はうまくいかなかった、直す意思が要る）** | `2020-02-license-discuss-authors-explain-not-proxies-observed.txt` |
| 2021-09-12 | `license-review`（観測）| **委員会の Jam の勧告と Rationale Document → 観測保存** | *"to date, OSI has not used the number of projects adopting a license as a factor in deciding whether a license can be approved"*（`board-decisions.md` §2d）|
| 2021-09 | `license-discuss` | **観測（Crane 氏の 1 通・AFL の文言は REUSE と SPDX の識別子での使用を妨げる）** | `2021-09-license-discuss-afl-reuse-crane-observed.txt` |
| 2021-01-09 | `license-review`（観測）| **委員会の CERN-OHL の勧告と Rationale Document → 観測保存（抜粋）** | *"they are written such that they can be used for software, so they are appropriate for the OSI's review"*。審査対象の基準である（`board-decisions.md` §2e）。本文の Exhibit A（ライセンス全文）は省いた |
| 2015-11-12 | `license-review`（観測）| **Richard Fontana 氏の 0BSD（当時 Free Public License）承認の告知 → 観測保存** | *"the OSI obtained outside legal counsel concerning the legal and policy issues raised by 'ultra-permissive' licenses like the FPL which do not impose conditions on the licensee"*。助言の中身は公開されていない（`board-decisions.md` §8.6）|
| 2015-10-13 | `license-review`（観測）| **Richard Fontana 氏の委員会報告 → 観測保存** | Free Public License（現 0BSD）について *"Approval, or else OSI to adopt some formal maturity/real-world-use factor"*（`board-decisions.md` §8.6）|
| 2015-10-13 | `license-review`（観測）| **Richard Fontana 氏の Berkus 氏への返信 → 観測保存** | *"there doesn't seem to be any proliferation concern with FPL"*。引用部に Berkus 氏の法的レビューの懸念が在る（`against.md` #287）|
| 2015-08〜09 | `license-review` | **観測（Free Public License〔今の 0BSD〕の審査から 5 通・写しからライセンスを剥がせることは方針の問いか、印の無いコードは汚染されている）** | `2015-08-to-09-license-review-fpl-license-stripping-observed.txt` |
| 2020-03 | `license-discuss` | **観測（Chestek 氏の 1 通・米国ではソフトウェアに人格権は無い）** | `2020-03-license-discuss-author-attachment-chestek-moral-right-observed.txt` |
| 2020-12 | `license-discuss` | **観測（Atkinson 氏の 1 通・前文は役に立つが、調子は中立でも足りる）** | `2020-12-license-discuss-invariant-manifestos-atkinson-preamble-observed.txt` |
| 2020-12 | `license-discuss` | **観測（Chestek 氏の 1 通・法的な文書に拘束しない部分は無い、前文は意図の解釈に使われる）** | `2020-12-license-discuss-invariant-manifestos-chestek-no-non-binding-observed.txt` |
| 2024-09-01 | `license-review`（観測）| **Stefano Maffulli 氏（事務局長）の問い → 観測保存** | *"non-software artifacts like datasets, documentation, and model parameters (aka weights)"*（`board-decisions.md` §2g）|
| 2024-09 | `license-review` | **観測（Berkus 氏の 1 通・ソフトウェアのライセンスでない承認済みの文書は別に並べる）** | `2024-09-license-review-ai-process-berkus-list-separately-observed.txt` |
| 2024-09 | `license-review` | **観測（Maffulli 氏の 1 通・AI には一般化に使える実践の例がまだ無い）** | `2024-09-license-review-ai-process-maffulli-no-practice-observed.txt` |
| 2024-09-10 | `license-review`（観測）| **Pamela Chestek 氏（委員長）の 1 通 → 観測保存** | *"legal mechanisms other than a license"*（`board-decisions.md` §2g）|
| 2024-09-10 | `license-review`（観測）| **Pamela Chestek 氏（委員長）の 1 通 → 観測保存** | *"This area needs room to develop"*。1 本か複数かを OSI が決めないと述べる（`board-decisions.md` §2g）|
| 2024-03 | `license-discuss` | **観測（Blue Oak についての Perens 氏の 1 通・法律家の新しい permissive も採用されず承認済みの数を増やしただけ）** | `2024-03-license-discuss-blue-oak-reinvention-observed.txt` |
| 2024-08 | `license-discuss` | **観測（Fontana 氏の 1 通・OSI は識別子ではなくライセンスを承認する）** | `2024-08-license-discuss-gplv2-spdx-fontana-observed.txt` |
| 2024-03 | `license-discuss` | **観測（Ombredanne 氏の 1 通・本文の URL は古びた、本文は直さず SPDX の札を使え）** | `2024-03-license-discuss-ecl-stale-link-ombredanne-observed.txt` |
| 2026-11-07 | 一次資料（OSI のサイト）| **記事 *Public Domain Is Not Open Source*（2017-07-28・署名 OSI Policy Team）→ スナップショット** | *"A solution would be"*、放棄できる法域では放棄し、できない法域のために許諾を与える形。CC0 が止まった理由は特許の議論だと述べ、結びは MIT を勧める（`board-decisions.md` §2f）|
| 2026-11-07 | 一次資料（OSI のサイト）| **McCoy Smith 氏の記事 *Patents and Open Source*（2025-12-04）→ スナップショット** | *"(with or without defensive termination provisions)"* と、CC0 の特許の除外への懸念を述べる。同じ記事は Apache-2.0 の防御的終了を肯定する |
| 2026-03〜04 | `license-review` | **観測（2 つの提出への最初の返信 2 通・元のライセンスとの差、使う（使うと表明する）プロジェクト、手順の項目、何を達成したいか）** | `2026-03-to-04-license-review-first-questions-observed.txt` |

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

**2026-11-07 に、分析の側に残っていた相手の言葉の逐語引用も要約へ置き換えた。** 本文を撤去しても、
引用が残っていれば相手の私信を公開していることになる。**steward 本人の言葉は本人のものなので残す。**
事実と不利な記録は要約のまま残る。

**現在この例外が適用されている file**: `*-offlist-nick-vidal-*.txt`（5 件）。

## なぜ raw を残すのか

次の venue（`license-review`）へ進むとき、**前段で何が起きたかを示せるかどうかで受け取られ方が
変わる**。示せなければ、提出は「前の議論を無視してもう一度出してきた」ように見える。
そのとき示す材料は、要約ではなく**原文**である必要がある —— 要約の正しさは、原文が在って初めて
確かめられる。
