---
file: LICENSES/READ-THREADS-LOG.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-15
canonical-ref: LICENSES/READ-THREADS.txt (読んだ件名の一覧・census の唯一の「読んだ」の源) / LICENSES/AS-OF.md (「未読スレッドの残り」の件数と直近の 1 件)
---

# 未読スレッドの読了の記録 —— どのスレッドを読み、どの節へ運んだか

**`AS-OF.md` の「未読スレッドの残り」のセルから 2026-11-15 に移した 65 件で、本文は移す前と 1 字も変えていない**
（移した時点でセルは 32,534 バイトあり、`AS-OF.md` を byte 予算の advisory 130,000 より上に置いていた・
`docs/architecture/file-size-budget.md` の BYTE-BUDGET-DATA）。**移したのは区切りだけ** —— セルの中では
「。」の後に次の日付が続いていたのを、1 件 1 項目にした。並びも移す前のまま（新しい読了が上）。

**なぜ消さずに移したか**: 節の側に読んだスレッドの件名を持たないものがある（移した日に照合して、件名と節の
組 49 のうち 26 が節の本文に件名を持たなかった）。このセルが件名から節を引く唯一の対応表だった。

**新しく読んだら**: この一覧の先頭に 1 件を足し、`AS-OF.md` のセルの「直近の 1 件」と件数を入れ替える。
件名は同じ commit で `READ-THREADS.txt` にも足す（census が「読んだ」と数えるのはそちらだけ）。

## 2026-11-15 の読了（新しいものが上）

- 2026-11-15 に "Project Tick General Public License v1.0"（`license-discuss` 2026-01・11 通）を `review-readings.md` §1.205 へ（新しい文そのものを既存のライセンスとの差として示せ、提出の前に法律家を使え・Perens 氏）。

- 2026-11-15 に "Submission: CNRI-Python-GPL-Compatible"（`license-review` 2026-03・5 通）を読み `review-readings.md` §1.204 へ（clickwrap の文と OSD 10。ACD の §2.3 は同意を求めない。clickwrap の文を持ったまま承認された）。

- 2026-11-15 に "OSI License Submission - PPPL BSD-3"（`license-review` 2025-07 と 2025-10 の 2 つの会話・16 通）を読み `review-readings.md` §1.203 へ（名前だけが違うライセンスは承認しない、著作権者の表示はライセンスの外に置く、名は steward が決める）。

- 2026-11-15 に 2021 年以降の未読 8 本を新しい順に読み始め、"Total Reciprocity Public License (TRPL v1.0)"（2025-12・20 通・決める側の通に絞った）を `review-readings.md` §1.202 へ（出力を派生物とみなす条と、権利の有無を決めずに置く ACD の §6.4）。

## 2026-11-12 以前の読了（新しいものが上）

- 2026-11-12 に "Ethical open source licensing - Persona non Grata Preamble"（2020-02・47 通・決める側の通に絞った）を読み `review-readings.md` §1.201 へ（採用の見込みは、増殖と重複を除けば承認の基準ではなかった・元理事。拘束しない語はライセンスに要らない・Nelson 氏）。

- 2026-11-12 に "Copyright on APIs"（2019-06・72 通・決める側の通に絞った）を読み `review-readings.md` §1.200 へ（在るか分からない権利を在るものとして主張しないこと、名指すことが権利の拡張の例になる懸念）。

- 2026-11-12 に census の論点の順位から "OSD #9 would not make SSPL OSD-incompliant"（`license-review` 2018-10・31 通・決める側の通に絞った）を読み `review-readings.md` §1.199 へ（OSD は別の時代のために書かれた、承認済みのライセンスは OSD が明示しないことを整えられる、ライセンスを読まなくても動かせる）。

- 2026-11-12 に "A new "use" clause in the OSD"（2002-08・12 通）を読み `review-readings.md` §1.180 の追記の前段へ（委員長が許される制限だけを列挙する OSD の条を提案した。ACD は最も狭い案の下でも当たらない）。"newsforge story"（2001-09・26 通・決める側の通に絞った）は読了の記録だけにした（急いで承認した APSL 1.0 を誤りとして挙げた委員長の文で、#239 の線に新しい点を足さない）。これで portfolio-9b が絞った「途中に決める側」の 12 本は全部読んだ。

- 2026-11-12 に "Change ot topic, back to OVPL"（2005-08・65 通・決める側の通に絞った）を読み `review-readings.md` §1.198 へ（委員長が承認済みの語の逐語の再利用を求め、理事は認証の要件を OSD に限るべきだと反対した）。

- 2026-11-12 に「途中に決める側」の 3 本を決める側の通に絞って読んだ。"FAQ entry on CLAs"（2015-01・26 通）は `against.md` #286 の 2 つ目の追記へ（OSI は外向きのライセンスを審査し、内向きの寄与の方針は審査しない・Randal 氏と OSI の顧問の Radcliffe 氏）。"Intimacy in open source (SSPL and AGPL)"（2019-01・34 通）と "Ethical open source licensing - Dual Licensing for Justice"（2020-02・28 通）は `review-readings.md` §1.197 へ。

- 2026-11-12 に "The Mutualist License (MutuaL) v1.2"（`license-review` 2026-06・5 通）を読み `review-readings.md` §1.196 へ（単独の非法律家の新しいライセンスに、ACD の投稿の 2 か月前に Chestek 氏が書いた基準: 文体ではなく語の正確さ、解釈の規則は語の不明確さを補わない）。

- 2026-11-12 に「途中に決める側」の 2 本を読んだ。"moving to an issue tracker"（`license-review` 2018-06・32 通・決める側の通に絞った）は `review-readings.md` §1.195 へ（理事会が変更を求めるのは OSD に反するときと OSD に適うか曖昧なとき、新しいライセンスは独自の価値を問われる、役に立つライセンスは 3 つでほかは飾り）。"Creative Commons Attribution"（2004-06・8 通）は読了の記録だけにした（帰属を求めるのはよいが、帰属のコードを変えることを禁じてはいけない、という委員長の文で、帰属を求めない ACD に新しい点は無い）。

- 2026-11-12 に "conducting a sane and efficient GPLv3, LGPLv3 Review"（2007-07・84 通、決める側の通に絞った）を読み `against.md` #248 の追記へ（審査を OSD だけに絞る主張は、採用と広い検討が済んだ本文を前提にしていた）。これで census の「決める側・未読」（最初の通を決める側が書いた会話）は 0 本になった。

- 2026-11-12 に "Open Source Licensing"（2003-08・3 通）を読み、`jurisdictions.md` §5c の追記の逆側（Rosen 氏: 当事者が本当に永遠を意図するなら perpetual と書いてよく、§203 は職務著作に及ばない）と `against.md` #6 の追記（法はどのみち勝つので書く必要は無い、という文と、それへの portfolio-aa の逆側）へ。

- 2026-11-12 に "Announcing OWFa and CLA 1.0"（2011-03・5 通）を読み `against.md` #286 の追記へ（寄与は同じライセンスで入れば足り、CLA は要らない）、"inconsistency in OSD- software (#2) v. licenses/rights (every other plank)"（2007-07・6 通）を読み `review-readings.md` §1.194 へ（OSD 2 はライセンスでなく配られる物について述べる）。足した語で候補の外から一覧に入った "For Approval: Socialtext Public License ("STPL")"（2007-03・24 通）も読み `against.md` #239 の 2 つ目の追記へ（承認済みの条から取ったので推定が働くべきだという提出者の主張が退けられた）。"Proposed License-RPL"（2002-05）、"RPL version 1.1"（2002-10）、"Draft 1 of the OpenDesk.com Public Source License"（1999-11・29 通）は読了の記録だけにした。

- 2026-11-12 に "question before attempting an update on AFL"（`license-review` 2008-10・18 通）と "Groklaw's OSI item"（2007-08・69 通）を読み、`against.md` #239 の 2 つ目の追記（承認済みに似た条が在ることは新しい条を正当化しない・4 人）と #161 の追記（審査の対象は本文で書き手の素性ではない）へ。"I don't mean to whine, but"（2002-02・11 通）は読了の記録だけにした（委員長が list の拒否権を使うよう促した通で、ACD への新しい点は #83 の沈黙の記録に足すほどではない）。portfolio-9b に、census の「途中に決める側」の 82 本の中で 68 本が bare の "approved" だけで入っていることを測って伝えた。

- 2026-11-12 に "FOR APPROVAL - Python License Changes"（`license-review` 2011-05 と 2011-08 の 2 本）を読み、`against.md` #239 の追記（承認済みの語でも今は承認できないことがある・先例は参考であって拘束しない）と #320 の追記（古い版を非推奨にしても効かない）へ。

- 2026-11-12 に "For approval: GNU Affero General Public License"（`license-review` 2008-01・9 通）を読み `against.md` #7 の追記へ（使われていないことを理由に特別目的へ、という分類の基準が list で争われていた）。足した語で候補の外から一覧に入った "caGrid Open Source License For Legacy Approval"（2009-01・6 通）も読み、同じ追記へ（数百の配備は広い分類に足りない）。"OKL4 license"（2009-12・3 通）は読了の記録だけにした（2008 年の議事録の Iggy Wanna License の却下を引くだけで、ACD への新しい点は無い）。

- 2026-11-12 に "For Approval: Microsoft Community License"（2005-12・10 通と 2007-08・16 通）と "For Approval: Microsoft Reciprocal License"（2007-10・9 通）を読み `review-readings.md` §1.193 と `against.md` #248 の追記へ（弁護士が指摘し提出者が認めた曖昧さが、本文を変えないまま承認された）。足した語で候補の外から一覧に入った "Question on OSD #5"（2007-11・54 通）も同じ日に読み、`jurisdictions.md` §5c の追記へ（合衆国の取り戻しの規定があるので本当に perpetual なライセンスは無い、という 2007 年の文）。

- 2026-11-12 に OSI のライセンスの頁の再編をめぐる 2 つの会話（"Alternative Proposal: The OSI licensing pages" 2012-06 と "… [revisited]" 2012-11）を読み、読了の記録だけにした。同じ年の 6 月の本体の会話（読了済み）に在った John Cowan 氏の「open source でも承認されない理由 3 つ」を `against.md` #248 に足した。

- 2026-11-12 に "For Approval: Microsoft Public License"（2007-10・27 通）を読み `against.md` #161 の逆側へ（委員長が残る異議を「また 1 つのライセンス —— どの承認にもある」と「Microsoft だ」にまとめ、MS-PL は承認された）。

- 2026-11-12 に "Academic Free License version 2.0"（2003-07）を読み `gap-measurements.md` §1.143 の追記と `against.md` #6 の追記へ（BSD 型が欠く細部を埋める、という AFL の提出文は ACD の B10 の主張と同じ形で、AFL は承認された。長さへの答えは「明確にするのに要る語数なら仕方がない」）。

- 2026-11-12 に読了の記録だけの 3 本（portfolio-9b の「決める側・未読」の一覧から）: "testing kit conformance as a condition of distribution"（2004-06 —— 互換の検証を配布の条件にする通知は open source と両立しないという議論。ACD は配布に条件を置かない）、""De-approve" the Intel Open Source License"（2005-03 —— steward が自ら非推奨を申し出た。OSI は使うことを止める仕組みを持たないと委員が書いた）、"Coherent Open Source - Getting underway next Friday"（2019-09 —— ライセンスを少数に絞る提案で、B10 の既知の線を超える材料は無い）。

- 2026-11-12 に "For Approval: Some License Or Another"（2004-11）と "Æsthetic Permissive License - For Approval"（2007-12）を読み `against.md` #249（審査中に直すことに法律家が耳を貸さなくなる・Rosen 氏）、#10（自動で新しい版へ移す条は承認されない・Taylor 氏）、#6（曖昧でないライセンスは決めた行数には収まらない・委員長）へ。

- 2026-11-12 に "Comment on MOSL and similar licenses"（2013-04〜06・35 通）に行を持たせた。Fontana 氏の 2 文を `reviewer-positions.md` と #294 が既に引いていた登録漏れで、残りも読み、Berkus 氏の却下の 3 理由と Cowan 氏の「OSD に適合しても退ける裁量」を `against.md` #323 に足した。

- 2026-11-12 に "Accidental Public License?"（2011-04）を読み `against.md` #322 の追記へ（法務部門は既存のライセンスの複雑さを一度学べばよく、新しく試されていないライセンスより限界の複雑さは小さい —— Karl Fogel 氏）。同じ日に読了の記録だけの 2 本: "Bruce Perens rejected from license-proliferation committee."（2005-08・53 通・増殖委員会の人選と OSI の運営をめぐる議論。委員長は委員会が勧告だけをする諮問の機関だと書いた）と "Discussing proposed new licenses"（2015-09・選挙の機器のライセンスの議論の場をめぐる通）。

- 2026-11-12 に OSL 3.0 / AFL 3.0 の提出の 2 つの会話（2005-09）を読み `against.md` #10 の追記へ（改変版を許す第 16 条は steward である問題を除くためだった、と提出者が書いた。逆側に増殖）。同じ日に `comparison.md` §1.4 の見出しを「否定的な反応のあとで取り下げられた先例（2012・正式の否決は無い）」に直した（portfolio-aa の指摘）。

- 2026-11-12 に "New license approvals"（2017-04・BSD+Patent の承認の告知）と "Fact-gathering on OSI-approved licenses"（2019-08）を読み、`gap-measurements.md` §1.143 の追記、`against.md` #236 (c) の逆側、`comparison.md` §1.4 の逆側へ（委員長が BSD+Patent の分類を当面「特別な目的」とした。同じ Fontana 氏が 2019 年に、承認しない処分は却下に等しいと言え、CC0 の取り下げを「却下」と呼んだ）。同じ日に、`against.md` #44 に 2025-12 の Atkinson 氏の「既に与えた許可の言い直しは、その分野に限る読みを生む」を足した（§6 にも当たる・portfolio-aa の指摘）。

- 2026-11-12 に "Request for License Review - BarrerSoftware License (BSL)v1.0"（2025-12）を読み `against.md` #292 の追記と objection-map の行へ（Lukas Atkinson 氏が、本文が AI の道具で書かれたように読めることを *"This alone should be grounds to stop reading the license"* と書いた。#292 の 2 例目）。"License Consistency Working Group, call for volunteers"（2023-06）は理事会が承認済みのライセンスの一貫性を見直す作業部会を募った告知で、読了の記録だけ。

- 2026-11-12 に、portfolio-9b の「決める側・未読」の一覧（PR 2937）から委員会報告 3 本（2008-11・2010-06・2010-11）と "license committee"（2012-03）を読み `review-readings.md` §1.192 へ（条件を放棄しても承認は外れないという委員長の案、簡単な方がよいとは限らない、何でもしてよい式の差し戻し、法律家を入れるよう勧める文）。同じ日に、portfolio-9b の帰属の照合（`--attribution`）の候補 12 件を原文で確かめ、本物の取り違えは 0 件だった（EUPL の告知者の名を本文で明記した 1 か所だけを直した）。

- 2026-11-12 に 2004 年の委員会報告 3 本（"License Committee report" 2004-02・"License Committee Report" 2004-11・"License Committee Report for December 2004"）を読み `board-decisions.md` 8.11 節と `against.md` #314 の追記へ（似たライセンスは「改善でない」が「望めば承認する」、使う人への引用の要求は使用の制限として却下が勧められた。11 月の版は理事会に出されなかった。12 月の版は list に出された）。2 本は portfolio-9b の「名が在る・未読」に出ていたが、ドシエが引いていたのは別の年の報告で、本当の未読だった。12 月の報告はこの PR の語で「候補の外・未読」へ移り、同じ PR で読んだ。

- 2026-11-12 に "a proposed change to the OSD"（2002-10〜11・74 通。前の PR で「いまの語では候補でないが一覧に在る」へ移った 3 本の 1 本）を読み `review-readings.md` §1.180 の 2 つ目の追記と `against.md` #321 の追記へ（委員長が OSD に「使用と改変を制限しない」を足そうとし、議論は受け入れの手順と免責へ移った。提出した会社の側の人（署名に肩書きは無い）が、同意の明確な表示が無い構造は *"may not be enforced by many courts in many cases."* と書いた）。移った残りの 2 本も同じ日に読み、読了の記録だけにした: "Plan 9 license"（2000-07〜09・116 通 —— 委員長が問題にしたのは、どんな知的財産の訴訟でも許諾が終わる条項で、ACD は終了を持たない（§10.4）。残りの大半は FSF と OSI の定義の違いと「海賊行為」という語の議論）と "discuss: OCLC Office of Research Open Source License"（2002-09・9 通 —— 提出された文の起草の指摘で、ACD に当たる新しい材料は無い）。

- 2026-11-12 に、候補の外の 2000 年の 2 本（"Licenses versus contracts" と "The different between GPL and non-license"）を読み、`jurisdictions.md` §5d（法学の教員が、放棄の抗弁が 1976 年法の下で生きているかは深刻に疑わしいと述べた）、`review-readings.md` §1.191 の追記、`against.md` #152 と #324 の追記へ。"Public domain mistake?"（2004-01）は `against.md` #236 が引いていた登録漏れで、残りの通も読んで行を持たせた（portfolio-9b の数え方の (B)）。話題の一覧の未読は 22 → 19 件。この 2 本の rounds で語の当たりが変わり、未読の候補 3 本（"Plan 9 license" 2000-07、"discuss: OCLC Office of Research Open Source License" 2002-09、"a proposed change to the OSD" 2002-10）が「いまの語では候補でないが一覧に在る」の側へ移った。一覧に残るので母数は変わらず、次に読む。

- 2026-11-12 に、候補の外の 2000 年の 3 本（"Wired Article on the GPL"・"Public Domain and liability"・"Abandonment"）を読み `review-readings.md` §1.191、`against.md` #324 と #152・#41 の追記へ（GPL は撤回できるか、譲渡の後も続くか、条件が対価になるか。合衆国法典 17 編 205 条 (e) がドシエに無かった）。候補の外なので母数は動かない。portfolio-9b の話題の一覧（*revoc*・*revok*・*abandon* に本文で 3 回以上当たる、候補の外の 3 通以上の会話・PR 2910）は 26 件で、未読は 26 → 22 件。同じ日に "When can licenses be revoked?"（2005-09・§1.191 の追記と #324 へ。受領者の義務が対価になって撤回を防ぐ、という 2000 年と同じ答え）と "GPL revokability"（2011-05・§1.191 の追記へ。撤回できないと書くことが GPL 3.0 の答えだった、と弁護士と名乗る人が述べた）を読み、2026-10-11 の "Pre-submission discussion: Zero-Clause BSD with Patent Grant (0BSD-P)"（全 4 通を `against.md` #276 が既に読んでいた登録漏れ）に行を持たせた。"Public Domain and liability" と "Abandonment" は下限に届かず一覧に出ない。

- 2026-11-12 に "Can abandonment be irrevocable?"（2003-08）を読み `gap-measurements.md` §1.146 の追記と `review-responses-clauses.md` §2 の禁反言の問いへ（放棄の代わりに撤回できない許諾を、と勧めた弁護士が、翌日には撤回された許諾も放棄と変わらないかもしれないと書いた。問いは開いたまま終わった）。それより前の 2000 年の 3 本（"Wired Article on the GPL"・"Public Domain and liability"・"Abandonment"）は候補の外に在り、まだ読んでいない。同じ日に読了の記録だけの 2 本: "Open source license with obligation to display an attribution?"（2018-12 —— 帰属の表示を利用に課す型の話で、ACD は帰属を求めない。Perens 氏の、使うだけの人に許諾を読むことは期待しない、という文は ACD の条件の無さと同じ向きだが、帰属の文脈の発言である）と "Weak copyleft license with network use requirement?"（2026-09 —— 3 通は `rounds/2026-09-05-license-discuss-weak-copyleft-thread-observed.txt` に在り、残りの 2 通は質問者の「関係が無い」と Perens 氏の LGPL-3.0 の提案で、ACD に当たる材料は無い。portfolio-9b の道具の修正で「rounds に在るが READ-THREADS に無い」に出た）。

- 2026-11-12 に読了の記録だけの 2 本: "License for approval"（2008-03・UOML —— 規格への適合を利用の条件にして「著作権のライセンスでそれをするなら承認しない」と返された。条件を持たない ACD には有利な対比にとどまる）と "For Approval: TVA Open Source License"（2009-09 —— 米国政府の作品の公有化と外国での著作権の扱い。ACD の §3 と §4 の並存の理由と同じ既知の論点）。

- 2026-11-12 に "Draft of new OSI licenses landing page; please review." と、件名が変わった枝 "BSD, MIT"（2012-04）を読み `review-readings.md` §1.178 の追記へ（特許を正しく扱うことを一覧の先頭の理由にした委員会の側の文、献呈の型を勧める弁護士の文）。"Procedure for using an approved license"（2002-10）は MPL の使い方の相談で、スチュワードの新しい版への不安は B12 の Kuhn 氏 2018 と同じ論点のため読了の記録だけ。

- 2026-11-12 に "Request for approval of the Non-Coercive Copyleft Licence (NCCL) 1.0"（2015）を読み `review-readings.md` §1.190 と #321 の追記へ（本文を添えずに配ることの両面、同意を求めない形、誰も賛成せず 18 日で「却下」）。"BSD-like licenses and the OSI approval process"（2007）は許容型の細かな変種の提出への不満と収集物の許諾の話で、ACD に新しく当たる発言は無かった（読了の記録だけ）。

- 2026-11-12 に "click-wrap is legally supportable?"（2002-10）を読み `review-readings.md` §1.180 の追記と #321 の追記へ（同意を求めないライセンスの条項は、相互の同意の表示が無いことを理由に争われうる、という法律家の肩書きを持つ人の文）。

- 2026-11-12 に "For Approval: Twente License"（2019）を読み `review-readings.md` §1.189 へ（プライバシーの条件を利用に課して OSD 6 で退けられた —— ACD の §11.3・§11.4 が条件でなく到達の限界と書く理由の対比）。同じ日に "EUPL v1.2"（2017）を読み §1.188 の追記へ（International の分類の目的）。

- 2026-11-12 に ZENTAO の 2 つの会話（"ZENTAO PUBLIC LICENSE For Approval" と "Approval request for ZENTAO PUBLIC LICENSE"・2016-06・長く一覧に残っていた未読）を読み `review-readings.md` §1.188 へ（数十万の利用者を挙げても、OSD への疑義と提出の形の不備で却下が勧められた。正本が中国語であることが審査を止めた）。

- 2026-11-12 に "Official License Anti-Proliferation policy?"（2005-04）を読み `board-decisions.md` の 8.7 節の追記へ（3 つの基準は OSI の声明として新しい提出に当てる規則と公表されていた。8.8 節の 2013 年「成文の規則は無い」と食い違う向き）。

- 2026-11-12 に "License Committee Report - January 2017" を読み `review-readings.md` §1.187 と #257 の追記へ（委員長の推薦は個人のもの、list の沈黙は読まれていない印、理事会は OSD について前もって判断を示さない）。

- 2026-11-12 に 2013 年 3 月の委員会報告 2 本（"License Committee Report - 2013-03-06" と "… for board meeting of 2013-04-03"）を読み、`review-readings.md` §1.176 の追記へ（理事会が求めて復活した正式の報告と、CeCILL 2.1 の推薦）。この 2 本が rounds に入って語の当たりが増え、未読の "EUPL v1.2"（2017-05）が「いまの語では候補でないが一覧に在る」の側へ移った —— 一覧に残るので母数は変わらない。

- 2026-11-11 に "FAQ entry for slight variations in licenses?"（2013）を読み `review-readings.md` §1.186 と #262 の追記へ（弁護士は要るか、で list の弁護士 2 人が反対を向いた）。同じ日に、ACD の阻害要因に当たる発言の無かった 7 本を読了の記録だけにした: 会話単位で未読に出た兄弟の 5 本（"Updating the License List" 2011・"proposal: DotGNU Trademark License" 2004・"further license presentation improvements?" 2013・"The license of OpenMotif" 2019・"License pages cleanup project underway" 2023）と、"Machine readable source of OSI approved licenses?"（2013）、"a data licensing problem"（2002）。

- 2026-11-11 に "CeCILL license V2.1 for Approval" の 2013 年の会話（会話単位にして未読に出た兄弟の 1 本）を読み、理事会の議事録と合わせて `review-readings.md` §1.176 の追記と #257 の追記へ（提出から約 14 か月で承認、委員長が遅れを謝った）。**2026-11-11 に数え方を会話単位に改めた**（portfolio-00 の判断）: 件名だけでまとめると年をまたいで同じ件名の別の会話を 1 本に数え、1 つを読むと別の会話まで読了に数えて未読を少なく出していた（候補の件名 778 本の中の 48 本が複数の会話を含み、23 本は読了と記録されていた・有利な側の偏り）。いまは件名 + 90 日を越える空白で切った会話を 1 本と数え、THREAD-CANDIDATES.txt も会話ごとの行にした。旧い数え方の最後の値は候補 778 本・読了 401 本・未読 377 本。READ-THREADS の 35 行は日付が会話の始まりと違っていた。どれも件名が候補の会話を 1 つしか持たないので、日付をその会話の始まりに直した（数は動かない）。読んだ証拠（rounds の通・節の出典）の無い会話は行を持たせず、未読に数える。道具が「rounds に在るが READ-THREADS に無い」と挙げる 8 件のうち 4 件（2013 の CeCILL V2.1・2004 の委員会報告 2 本・2019 の Blue Oak）は、件名だけで rounds と照らした見かけで、その会話の通は rounds に 0 通である。

- 2026-11-11 に "Open source license chooser choosealicense.com launched."（2013）を読み `review-readings.md` §1.185 と #289・#322 の追記へ（採用の入口としての選択サイト、「無名には理由がある」）。

- 2026-11-11 に "OSI recognition for Creative Commons Zero License?"（2012-02・CC が出す前に利用者が承認を求めた）を読み `review-readings.md` §1.184 の追記へ。「"Fairness" vs. mission objectives」（2020-02）は承認の取り消しと非推奨化の議論で、ACD の承認の判断に当たる発言は無かった（読了の記録だけ。承認の後に非推奨にされうることは、どの承認済みライセンスにも当たる一般の事実である）。

- 2026-11-11 に "Invite Creative Commons to submit CC0 Dedication."（2012-01・CC0 を招く前の議論）を読み `review-readings.md` §1.184 と B4 の行へ（放棄と許諾を 1 つに持つ文書は全体を審査する、という立場と構造への留保）。

- 2026-11-11 に "Looking for license stewards"（2006）を読み BOTTLENECKS の B12 へ（連絡の取れない steward の承認済み 12 本の中で 11 本が今も SPDX の印の 141 本に在る）。

- 2026-11-11 に "Public domain software is not open-source?"（2008）、"New OSI FAQ items posted about Public Domain and CC0."（2012）、"Short permissive no attribution required open source license"（2015・ACD と同じ型の提案への「十分すぎるほど在る」は #314 へ）を読み `gap-measurements.md` §1.146 の追記へ（献呈は承認の対象でないという線の言い直しと、FAQ の 2 問が「合意の無さ」の要約として受け取られたこと）。

- 2026-11-11 に "For Public Comment: The Libre Source License"（2019）を読み `review-readings.md` §1.183 と #262・#320 の追記へ（個人の起草者に示された順序 —— gap と概念を先に、最後に弁護士）。

- 2026-11-11 に "License Proliferation Dissatisfaction"（2007）を読み `review-readings.md` §1.182 と #323 へ（理事会の側が述べた却下の基準と、承認済みを絞る案を採らなかったこと）。

- 2026-11-11 に "FAQ entry (and potential website page?) on "why standard licenses"?"（2014）と Apache の第三者ライセンス方針の 2 件名（2015）を読み `review-readings.md` §1.181 と #322 へ（承認は受け入れの床で、下流の一覧は各組織が決める）。

- 2026-11-11 に "Legal soundness comes to open source distribution"（2002）を読み `review-readings.md` §1.180 と #321 へ、"Using opensource in a company not in the software business"（2016）は利用者の相談で、読了の記録だけ。

- 2026-11-11 に OSET Public License の審査の 3 件名（2015）を読み `review-readings.md` §1.179 と #312 へ。

- 2026-11-11 に OSI のライセンスのページの見せ方の提案（2012）を読み `review-readings.md` §1.178 へ。

- 2026-11-11 に "License Proliferation"（2005）を読み `review-readings.md` §1.177 へ。

- 2026-11-11 に CeCILL v2.1 の審査（2012）を読み `review-readings.md` §1.176 へ。

- 2026-11-11 に SIL Open Font License 1.1 の審査を読み `review-readings.md` §1.175 へ。

- 2026-11-11 に ECL の 2004 年の審査と 2009 年 12 月分の委員会報告を読み `review-readings.md` §1.174 と §1.172 の追記へ。2026-11-11 から、一度候補になったスレッドは `THREAD-CANDIDATES.txt` に残り、母数から外れない（portfolio-9b・PR 2770）。母数は 778 に戻り、読まずに外れていた 2 本から "License Committee Report for August 2007" を読んで `review-readings.md` §1.173 へ（理事会は 2007 年にオープンソースハードウェアを OSI の範囲に入るとしていた）。"Approval request for ZENTAO PUBLIC LICENSE" は 2026-11-12 に読んだ。道具の出力の「いまの語では候補でないが一覧に在る（149 件・うち未読 0 件）」—— 最後の 1 本だった "EUPL v1.2"（2017-05）も 2026-11-12 に読んだ。母数は 3 つの出どころ（いまの語での候補・`THREAD-CANDIDATES.txt`・`READ-THREADS.txt`）の和で、道具の出力の「決める側の語の閾値から外れたが一覧に在る」は 0 件（2026-11-11）。

- 2026-11-11 に 2009 年 9 月の委員会報告（Falcon の審査を含む）を読み `review-readings.md` §1.172 へ。母数の 778 → 776 で外れた 2 本（"Approval request for ZENTAO PUBLIC LICENSE" と "License Committee Report for August 2007"）は読まずに外れたもので、portfolio-9b が一度候補になったら外さない一覧を道具に足す（その後は母数が 778 に戻る）。

- 2026-11-11 に 2007 年 7 月の委員会報告と "what *is* the approval process?" を読み `review-readings.md` §1.171 と #318 へ。母数が 778 から 776 に動いたのは、ドシエに語が足されて候補から外れたスレッドがあるため。

- 2026-11-10 に道具が読了を `READ-THREADS.txt` だけから数える形に変わった（PR 2760）。切り替えの前の数え方では 378 / 400 で、差の 5 本は `rounds/` に 1〜2 通しか置いていない候補で、道具が「rounds に在るが READ-THREADS に無い」として別に名指す（名は `READ-THREADS.txt` の見出し）。

- 2026-11-10 に "Three new proposed OSD terms"（2005-03・3 つの基準の元の提案）を読み `review-readings.md` §1.170 へ。

- 2026-11-09 に 2005 年 9 月の委員会報告と理事会の対応の 2 件名を読み `review-readings.md` §1.168 へ、"Approval Status of MIT-0"（2019-12・委員長は承認の記録を見つけられなかった）は読了の記録だけ。

- 2026-11-09 に License Committee Report for September 2008 を読み、MirOS の承認の経過を `review-readings.md` §1.167 へ（#302 の逆側）。

- 2026-11-09 に Tidepool Open Access to Health Data Software License の審査（2013-10〜12）を読み、`review-readings.md` §1.166 と #316・#317 へ。

- 2026-11-09 に Boost Software License の審査（2007〜08）を読んだ。手続きの摩擦が中心で、ACD に当たるのは Cowan 氏の *"OSD #2 is expressly about the software, not about its license, so it need not be taken into account when evaluating licenses."* くらいだった（ACD はソースの頒布を求めない）。2026-11-09 から、道具が出す 1 行を写す（2026-11-10 からは `READ-THREADS.txt` の件名だけを読了に数える）。母数はドシエの語とアーカイブの月が増えると動く。2026-11-08 までは手で数えた 771 / 368 / 403。読んだ件名の一覧は `READ-THREADS.txt`（520 行・1 スレッドが 2 つの綴りの件名で出ている）。`reviewer-positions.md` §1.142、`gap-measurements.md` §1.143〜§1.145。2012 年の "License Stewards" は読んで、ライセンス本文の著作権の話で ACD に当たる発言は無かった。2020 年の "Certifying MIT-0" は §1.142 の表へ、2003 年の「Public Domain を一覧に」は §1.146 へ、2019 年の "The per se license constructor" は reviewer-positions §1.147 へ。2012 年の "objective criteria for license evaluation" は人気の測り方の話で当たる発言は無かった。2011 年の "Can OSI specify that public domain is open source?" は §1.148 へ、審査の手順の 2 本（2018〜19）は §1.149 へ、CC への特許の相談（2012-02）は §1.150 へ、Unlicense の審査の未収録の段落は §1.152 へ、"CC withdrawl of CC0 from OSI process" の特許の理由は §1.153 へ、UPL の審査（2014-04〜2015-02）と承認の議事録は `gap-measurements.md` §1.154 へ、ARL OSL の議論（2016-08〜2017-03）は reviewer-positions §1.155 へ —— 2016 年の 3 件名は候補の外で、2017 年の部分（件名 "Possible alternative"）は候補に在った（2026-11-09 に道具の出力の差で確かめて訂正）。"notes on a systematic approach" は §1.156、"Open source software licenses and the OSD" は §1.157、"avoid gray areas?" は `gap-measurements.md` §1.162、WebM の 2 件名は §1.163 へ
