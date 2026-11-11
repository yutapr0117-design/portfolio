---
file: LICENSES/ACD-OSI-BOTTLENECKS.md
audience: 次のセッションの実装者（一次読者）/ OSI license-review participants / 監査人
last-updated: 2026-11-07
canonical-ref: LICENSES/ACD-1.0.against.md (不利な事実の本体) / LICENSES/ACD-1.0.errata.md (本文の既知欠陥) / LICENSES/AS-OF.md (外部事実と検証日) / LICENSES/ACD-1.0.objection-map.md (反論の当否)
---

# OSI Approval Bottleneck Register

**この文書が唯一の canonical なボトルネック一覧である。** 他の文書はここを参照し、
同じ問題を独立に管理しない。

**目的は欠陥を数えることではない。** 目的は **OSI Approved への到達を阻害する要因を除去し、
残る不可制御要因を減らすこと**である。不利な事実（`against.md`）は**入力**であって、
ここに載るのは**承認確率に効くもの**だけである。

## English index for reviewers

**The analysis below is mostly in Japanese, so this table is the whole register in English.** "Who can
move it" names who has to act. The status is our own reading, not OSI's. Section numbers are those of
the 1.0 text.

| ID | The problem | Severity | Where it stands | Who can move it |
|---|---|---|---|---|
| B1 | No legal review | Highest | Nothing here supplies it. It is not a requirement: the process asked for an analysis by a licensed practitioner until December 2007 and then dropped it (`review-rules.md` §1.141). Members keep asking submitters for one (#291), and the review is *"not for workshopping a license"* (#298). Of at least 24 new licences submitted with no review, one is on the list (#297). The questions a lawyer would need are in `QUESTIONS-FOR-COUNSEL.md` | The owner, by engaging one |
| B2 | One adopter: this repository | Highest | We can improve discoverability. We cannot produce adoption, and will not claim any. Non-use alone has not been a ground (Committee rationale, 2020 and 2021). The one hold on record (Tiwaz, 2025-09-11) lifts if one project uses the licence or expresses interest | Third parties; the owner can ask |
| B3 | Length: 4,896 words, 16 sections, 82 clauses | High | It can be shortened but not answered | Us, in part |
| B4 | The §3 surrender beside the §4 licence | High | Tested as a possible structural refusal, and that was rejected. An article on OSI's site named the two parts as the solution in 2017. In the 2012 straw poll on CC0 all 13 votes against named patents and none named the structure, though one reviewer objected to the form that year. What OSI reviews is the licence part: *"OSI could analyze CC0 for its license fallback terms, but not as a public domain dedication"* (Lawrence Rosen, 2011; the same line in 2003, `gap-measurements.md` §1.143, §1.146). The judgment is OSI's | OSI |
| B5 | The legal account in §4.4 | Medium | The drafting defect closed in 1.1. The design question stays open | OSI |
| B6 | The name | Medium | Decided on 2026-10-24: no rename | Decided |
| B7 | §8.4's patent reach may lower uptake | Medium | A one-way trade with B10. Both mitigations are structurally closed | OSI |
| B8 | §12 moral rights | Medium | The same clause has been called a gap and mission creep. Both are recorded | A lawyer |
| B9 | §7 database right | Low | Checked and kept | Decided |
| B10 | Is the remaining gap enough for a new licence? | Highest | One effect stands on the text of all 141 approved licences: a patent grant beyond the work with no condition and no termination. John Cowan observed in 2014: *"We may not be in the business of approving licenses without patent grants any more"* (`gap-measurements.md` §1.144). Reach past the work has been approved once, to works the licensor lists: UPL in 2015, after Lawrence Rosen said such reach is *"more generous than the OSD requires"* (`gap-measurements.md` §1.154). No one close to the decision has supported a reach to a model or its output (#305). Whether that is enough is OSI's call | OSI |
| B11 | SPDX and REUSE naming | Low | Deliberately not submitted yet | OSI, then SPDX |
| B12 | One steward, and succession | Low | The recorded worry is control, and ACD has no upgrade clause. No successor is named | The owner, and someone willing |
| B13 | The cost of understanding this submission | High | Continuing. It is the only real relief for B3 | Us |
| B14 | The moderators' notice on AI-written posts | Highest | The decision is OSI's. At least three posts were rejected by moderation | OSI, the owner |
| B15 | Subject matter: §1.2's list touches a reason the Board gave in 2023 | High | The Committee stated a test in 2021 (CERN-OHL): licences *"written such that they can be used for software"* are appropriate for review. ACD meets it on its face. In 2024 OSI's Executive Director said review may reach datasets and model parameters. §1.2 is wider than CERN's, and the judgment is OSI's | OSI |

## 2026-09-11 の掘削で確定したこと（この節は結論だけ。逐語は `review-corpus.md` §1.67〜§1.70a）

**この日、`license-review` の 2024-01〜2026-09（33 か月・804 通・111 スレッド）を取得し、
基準・規則・結果の 3 層を一次資料で押さえた。register の各項目はこれを前提に読む。**

1. **承認の基準は 8 条あり、原典に書いてある。** `review-process` の "Standard for new licenses"。
   **7 条は我々の側で確かめられ、いずれも通る** ——再利用可能性（前半）/ licensor 優遇なし /
   曖昧性の実質的影響（§15.1・§15.3）/ 適用の変化幅 / **提出時点で遵守可能（義務ゼロなので自明）** /
   完全なテキスト（外部参照 0）/ **gap を埋めること**。**8 条目（明晰さ）だけが判断の余地を残す。**
2. **その明晰さも、代理指標では良い側にある**（§1.70a / §1.70b・**ただし二度の訂正を経ている**）——
   **平均文長 26.0（7 本中 3 番目に短い）/ 45 語超の割合 10.3%（最小）**。
   **⚠ 2026-09-14 に 2 つ取り下げた**: *「最長文は 6 本中で最短」*（再実行では OSL-3.0 の 76 語が
   ACD の 81 語より短く、**順位が方法に依存する**）と *「従属節を 2 つ以上積んだ長文は 0 件」*
   （**その列の定義がどこにも記録されておらず再実行できない**。方法を書いた指標では 61.1% で
   結論が逆向きになる）。**したがって *「解析の負荷という意味では最も軽い」* は register から外した。**
   **これが動かさないもの: B1（弁護士レビュー無し）は 1 ミリも動かない。**
3. **gap は「あれば良いもの」ではなく要件だった**（基準 7）。**B10 の位置づけが上がる。**
4. **委員長（当時）・委員・理事が述べた「承認しない／受け入れる」規則は 5 件**（§1.67・**2026-09-21 に「委員会が」から狭めた**・#188）。**4 件は当たらないか
   一致する。1 件（*"OSI requires prior review by a lawyer"* ・Piana 氏）は B1 に不利で、
   B1 の欄に逐語で置いた。** **⚠ 2026-11-06 訂正: その 1 件は本人が同じ日に撤回している** —— *"I stand corrected re: Pam's message on requiring legal review, bad choice of words on my side."*（2024-12-18 18:29・`rounds/2024-12-18-license-review-piana-correction-observed.txt`）。**B1 に不利な 1 件として数えていたのは誤りだった。** **⚠ 2026-09-22 に根拠を差し替えた（#186）** ——旧文は
   「個人の資格だから軽い」と読んでいたが、process ページは *"Board members and employees of OSI
   may participate in license review **in their individual capacity**"* と定めており、
   **その断り書きは理事が参加するときの印である。Piana 氏は OSI 理事**（2025-06〜2026-06 の名簿 12 回）。
   **disposition は変わらない**が、支えるのは我々の推論ではなく公表規則 ——
   *"**no one person, including a Board member, has the authority to approve or reject a license**"*。
5. **結果の分布**（§1.68・§1.69・**同日に自己訂正した**）: 決議 11 件 + 告知で、**承認 4・否決 8**。
   **承認 4 件はいずれも既存テキストである**（MIT-CMU / Los Alamos BSD-3 Variant /
   OSC License v1 = MIT + ドイツ法対応 1 段落 / BSD-3-Clause-Open-MPI）——**新規の道具は 1 件も無い。**
   **我々の輪郭は否決側に一致する**（`against.md` #128）。
6. **否決の理由は 2 束** ——**条件・利用制限・差別**（§10.1 により構造上あたらない）と
   **起草の粗さ・解釈問題**（当たりうる唯一の束）。
7. **「重複」は承認の category である**（MIT-CMU は *"Redundant with More Popular"* として承認）——
   **#84「なぜもう一つ PD 等価を？」への、我々の推論ではない答え。**
8. **⚠ 上の全部に掛かる天井が 2 つある**（`against.md` #130）:
   *"Their consensus that a license does not ensure software freedom may … be the justification for
   rejecting a license **even where they cannot identify a specific aspect of the OSD or the approval
   guidelines … that is not met**"* と、*"**Approval of a license with the same or similar terms in
   the past does not bind the OSI**"*。**必要条件はいくら積んでも十分条件にならない。**

## 解消可能性の分類

`1` 文言修正 / `2` 条項削除 / `3` 条項縮小 / `4` 条項統合 / `5` 構造変更 /
`6` 名称・識別子変更 / `7` 提出方法変更 / `8` 法律家レビュー / `9` 外部証拠・第三者利用 /
`10` OSI 判断依存 / `11` 解消方法不明 / `12` 構造的に両立不能の可能性

**`11` と `12` を最優先で探索する。** 軽微な修正可能事項を大量に見つけても安心しない。
**1 件の構造的問題は 100 件の軽微 errata より重い。**

## 索引（2026-09-09 に現物と一次資料から再構築）

| ID | 問題 | 重大度 | 分類 | status | 人間 | 弁護士 | OSI |
|---|---|---|---|---|---|---|---|
| **B1** | 法的レビューが無い | **最高** | 8 | **提出の産物**（「待ち」ではない・§B1+B2）| ○ **2026-11-08**: UPL（2015）は社外の法律家も見たと書いた提出でも独立の審査を求められ、出された記録の無いまま承認された（`gap-measurements.md` §1.154）。Fontana 氏 2017 は法律家の関与を品質の印としにくいと述べた（`reviewer-positions.md` §1.156）。 | ○ | — |
| **B2** | 実使用が 1 リポジトリのみ | **最高** | 9 | 解消可能・未実施（discoverability のみ制御可）。**2026-11-09: MirOS（2008）は、提出者が「大きいプロジェクト 1 つと小さいもの 2〜3」と書いた利用で、理事の *"only used in code copyrighted by you"* という問いを受けたまま、2 か月後に承認された（承認日 2008-09-10・`review-readings.md` §1.167）。逆側: MirOS の利用は ACD の 1 件より多く、2025 年の理事会の文より 17 年前の運用である。****2026-09-13 追記: 帰結は否決ではなく「承認しないまま留め置かれる」**（理事会 2025-07-18・#84 と連言）。**2026-11-04 確認**: GitHub のコード検索（*"Autonomous Commons Dedication"*・上限 100 件）で現れるリポジトリは本リポジトリ 1 つだけ（45 ファイル）—— **独立した第三者の採用は公開情報で確認できない**（検索が見るのは GitHub が索引した範囲だけ）| — **2026-11-08**: 利用を承認の理由に挙げた記録が増えた —— UPL を承認した理事会の議事録（2015-02-04）は *"Oracle intends to release software soon"* を挙げ、審査では Berkus 氏が提出者の利用の予定を、Villa 氏が anchor tenant を求めた（#312）。Blue Oak は 5 年の使用の後に出された（`reviewer-positions.md` §1.158）。逆側: Fontana 氏 2014 は利用の予定の無い提出を退けないと述べ、Villa 氏 2017 の案は OSD を満たせば承認して目立つ一覧に載せない形だった（#315・§1.156）。 | — | ○ |
| **B3** | 長さ 4,896 語 / 16 節 82 項 | **高** | 3 / 4 | **縮められるが答えきれない**（実測 306 語・機構部を削っても 3,888 語に届かない）。**2026-11-07: CC0 の審査で、放棄と許諾と特許を持つ道具は *"a 10-15 line"* の短さで求められていた**（Evans 氏 2012・§1.138）。**2026-09-20 追記: この bottleneck が実際に決定を生んだ例が出た** ——2017 秋の理事会は NOSA 2.0 について *"in view of the length, complexity, and ambiguities … conformance … cannot be assured"* として**承認も却下もしない**決議を採った（#183）。2026-11-04: 1.4 草案で読みの分岐を 4 件減らしたが結論は不変（下の B3 節）| — | — | — |
| **B4** | §3 献呈と §4 許諾の並存 | **高** | 10 | **OSI 判断依存**（12 候補として検証し否定）。**2026-11-07: CC0 の審査本体を読んだ。2012 年の意向調査は 13 対 8 で反対だったが、−1 の 13 人は全員が特許を理由に含め、構造を理由にした人はいない**（`review-precedents.md` §1.138）。**⚠ 同じ審査に、特許の許諾を公有化の宣言に結びつける形そのものへの反対が 1 人ある（#288）。****2026-11-07: OSI のサイトの記事（2017）が、放棄と許諾の 2 部構成を *"A solution would be"* と述べていた**（`board-decisions.md` §2f。決定ではない）。**2026-11-06 追記: OSI の FAQ が、公有化は *"still not a license"* で審査の対象にならないと述べ、§4 が要る理由は OSI の文で言える。同じ FAQ の *"rather than try to waive copyright altogether"* は §3 に当たる**。**2026-09-20 追記: 献呈だけの instrument が「著者は自分で献呈できる」という理由で却下された実例（WTFPL・2009-03-04）が理事会記録に在り、同じ 4 行に「ヨーロッパに public domain は無い」という §4 の存在理由も並んでいる**（#182）| — | — | ○ |
| **B5** | §4.4 の法的説明の正確性 | 中 | 1 / 5 | **起草は閉じ、設計の問いだけ外部**（E11 は 2026-09-14 に 1.1 で閉じた —— 過大な 1 文を削除し 1.1 / 1.2 草案に 0 件。steward が自ら出した問いの設計側（読み A）は未回答・1.0 には文が残る。**2026-09-28 訂正**）| — | — | ○ |
| **B6** | 名称 "Autonomous Commons Dedication" | 中 | 6 | **決定済み（2026-10-24）: 改名しない**（測定: 識別子は空き・"Commons" 58/58 が CC・ODC / "Dedication" は半分しか言っていない。理由と逆側は §B6）| — **2026-11-08**: 1.4 草案は §16.4 の名前の保護を「名前を含む名前」にも及ぼした（errata E76・T44）。「1 つの名前が 1 つの本文を指す」という改名しない判断の前提が、語で守られる。 | — | — |
| **B7** | §8.4 の特許射程が uptake を下げる | 中 | 3 | **B10 との一方向の取引**（緩和策 2 つは構造上ふさがっている）。**2026-11-06**: 1.4 草案は §5.1 と §8.3 が §8.4 の限定を素通りする読みを閉じ、費用を限定の内へ戻した。費用の一覧は `gap-measurements.md` §1.136 **2026-11-08**: 広さが承認を止めた記録は無い —— UPL（2015）と Blue Oak（2024）は広い特許許諾のまま承認され、Piana 氏 2023 は特許を持つ側が結果を理解すればよいと述べた。費用は採用の側に出る: 学術医療機関は Apache-2.0 すら避け（2024・#311）、寄与者への警告が 2014 年と 2023 年に出ている（#313）。 | — | — | ○ |
| **B8** | §12 人格権（licensable でない / mission creep）| 中 | 3 / 4 / 8 | **分岐を記録済み**（同じ条項が gap とも creep とも呼ばれている）| — | ○ | — |
| **B9** | §7 データベース権の必要性 | 低 | 2 | **検証済み・保持**（§7.2 は行為の語で独立に働く）| — | — | — |
| **B10** | **新規ライセンスを承認するだけの gap が残っているか** | **最高** | 10 | **2026-11-09: 2008 年の委員長は MirOS を *"Yet Another academic license of limited difference and limited value"* と書き、提出者が既存のライセンスへの移行を断ったうえで、OSD 適合を理由に *"Recommend: approval"* とした。理事会は報告を受け入れ、承認されたが推奨はされなかった（`review-readings.md` §1.167・#302 の逆側）。同じ委員長は同じ年に、MIT/X11 に近い別のライセンスに類似を理由とする却下を勧めており、線は記録に無い。** **2026-11-07: Fedora は 2022 年に CC0 をコードから外し、公有化の形は外していない。代わりに勧められた MIT-0 は特許に触れない（`gap-measurements.md` §1.139・#290）。** **OSI 判断依存**（2026-11-04: 既存の承認済み 141 本では達成できない効果を**少なくとも 1 件、原典の条文で立証** —— §8.4 + §8.2「作品を超える対象への特許許諾 ∧ 条件も終了も無い」を同時に持つものは 0 本。**gap が承認に足りるかは依然 OSI の判断**・EXTERNAL の B10 節。**同日後半の再検証: 条文比較で立つのは「明示の特許許諾 ∧ 無条件 = OSI の全テキストで 0 本」で、モデルの販売への届き方は §8.4 末文の読みに依存する** —— `ACD-1.0.gap-measurements.md` §1.133。**2026-11-06**: 行為の類型で当て直し、差が立つのはモデルの販売と出力の利用だと絞った（§1.135）。最強の反論は受益者の少なさ（#284・§1.136））| — | — | ○ |
| **B11** | SPDX 未登録 / REUSE 命名（#108）| 低 | 承認で消える | **意図的に未実施**（所在を動かさない・#106 は承認後も残る）。**2026-11-07: SPDX の基準は 2026-10-27 に書き直された。*"only by the license drafter"* は実使用に数えず、OSI 承認と Fedora / Debian の受け入れが審査なしの経路である（#296）**| — | — | ○ |
| **B12** | steward が 1 人 / 承継 | 低 | 9 | **リストが恐れたのは支配で、ACD に upgrade 条項は無い。承継先は未定**（2026-11-07 に 11 から移した）| ○ **2026-11-08**: 1.4 草案の §16.5 は、譲渡の後の Steward を最後に譲り受けた者に限る（T45）。継承の線が 1 本に定まり、1 回の譲渡で複数の者を共同の Steward にすることもできる（§15.5）。Steward が譲渡しないまま死亡・解散した場合は、本文は答えない。 | — | — |
| **B13** | reviewer の理解コスト | 高 | 1 / 3 | **継続対象**（B3 の結論により、長さへの唯一の実効的緩和）| — | — | — |
| **B14** | **AI 起草の投稿は拒否すると両リストの moderator が宣言した（2026-09-09）** | **最高** | 新設 | **規制判断は OSI（組織）**（AI には解けない）。**2026-11-11: 本文を AI が書いたこと自体は、委員会の 3 人が 2026-03 に問題にしないと答えていた** —— Chestek 氏 *"Why does that matter to how the license operates?"*、Fontana 氏 *"I'm not sure the possibility that any part of this license is AI-generated matters though."*、Berkus 氏 *"There is no requirement that the license be copyrightable."*（AI-MIT の審査・`review-responses-meta.md` Q36）。B14 の moderator の宣言は投稿の文面についてで、本文の起草についてではない。逆側: 起草したモデルの会社と利害の関係は残る（#319）。**2026-09-28 訂正（旧文「オーナーは Nick 氏個人とリスト外で対応中」は 09-10 時点の現在形のまま残っていた）**: 発信は 2026-09-17 に再開（状態の単一ソースは `FROZEN.md` の `POSTING-STATUS`）、**少なくとも 3 通が moderation で拒否**（#136 / #215 / #222）、リスト外の往復は `rounds/` に 09-07 / 09-13 / 09-15 / 09-17〜18 の記録がある（本文は撤回済みの stub・#217）。**それ以後の状態は我々からは分からない** ——「対応中」とも「終わった」とも書かない | ○ | — | ○ |
| **B15** | **主題適格 —— §1.2 の列挙が、2023 年に理事会が不承認とした当の理由に触れている** | **高** | 10 | **OSI 判断依存**。**2026-11-11: 理事会は 2007-09-06 に *"Open Source Hardware falls within the remit of the Open Source Initiative"* と述べていた（`review-readings.md` §1.173）。ソフトウェアでないものを範囲に入れた記録で、その後の 2021 年の基準と 2023 年の不承認は、範囲を狭く引き直した側の記録になる。** **2026-11-09: MirOS（2008 承認）の提出文は "software" の代わりに "work" の語を使い、Open Knowledge Definition にも適合するはずだと書いた。読んだ範囲でこの点への反対は無い（`review-readings.md` §1.167）。逆側: MirOS はソフトウェアでないものを列挙していない。** **2026-11-07: 委員会は 2021 年に審査対象の基準を述べていた** —— *"written such that they can be used for software"*（CERN-OHL・`board-decisions.md` §2e）。事務局長は 2024 年に、審査はデータセットとパラメータの文書にも及ぶと述べた（§2g）。ACD はこれに本文で答える。本文を変えて解く手は無い（列挙の語を落としても範囲は変わらず、範囲を縮めると非コード資産を失う・#237・`gap-measurements.md` §1.134。2026-11-04: 1.4 が §1.3 と §9.1 で自分で足したパラメータの名指しは戻した —— 範囲・B10 は不変・`ACD-1.4-CLARITY-TRIAL.md` §7）| — | — | ○ |

**深い分析の所在**: **B1 + B2 / B4 / B5 / B7 / B10 / B11 / B15** は [`ACD-OSI-BOTTLENECKS-EXTERNAL.md`](ACD-OSI-BOTTLENECKS-EXTERNAL.md) に在る（**外の答えに依存する項目**）。**B14 だけは [`ACD-OSI-BOTTLENECKS-POSTING.md`](ACD-OSI-BOTTLENECKS-POSTING.md)** ——**instrument の中身ではなく、そもそも投稿できるかという手続きの問題**だから（2026-09-25 に主題で分離）。**B3 / B6 / B8 / B9 / B12 / B13** はこの file の下。**索引・分類・集計は分離していない。**

**集計（表から導出・Check 460 (m) が照合する）**: 主要 15 / 解消済み 0 /
**OSI の判断が要る 8** / **弁護士が要る 2** / **人間が要る 3** / **構造的拒否候補 0**。
「解消済み」は status 欄が「**解消済み**」で始まる行の数で、「構造的拒否候補」は分類の列に `12` を持つ行の数である。項目を閉じるときは status をその語で始める（2026-11-08・Check 498 (e) が同じ数え方で照合する）。

> **⚠ この行は 2026-09-10 に直した。** 直前まで「**OSI 判断依存 3**（B4・B10・B11 の一部）」と
> 書いてあり、**実際に ○ が付いている行は 6 つ**だった（B4 / B5 / B7 / B10 / B11 / B14）。
> **項目を足すたびに列は増えるのに、集計行は最初に書いた数のまま動かなかった。**
> **しかも過少申告である** —— `All N adverse facts` が 118 に対し 14 と書いてあったのと
> **同じ向きの誤り**（#58）。**自分の状態について書いた文は、いま真か。**
> 以後は **Check 460 (m)** が表から導出して照合する。

---

> **⚠ 2026-09-14: 各項目の深い分析のうち、「外の答えを待つもの」を分離した。**
> **索引・分類・集計はここに残る** —— **「この文書が唯一の canonical なボトルネック一覧である」は、
> 一覧＝上の表のことなので、その性質は保たれている。**
> **分離先**: [`ACD-OSI-BOTTLENECKS-EXTERNAL.md`](ACD-OSI-BOTTLENECKS-EXTERNAL.md)
> —— **B1 + B2 / B4 / B5 / B7 / B10 / B11 / B14**（弁護士・第三者の採用・OSI の判断・moderator の
> 決定に依存するもの）。**この file に残るのは、我々の作業で動かせるもの** ——B3 / B6 / B8 / B9 / B12 / B13。
>
> **⚠ 分割線は、前日に測らずに書いた線とは違う。** 2026-09-13 に
> 「次に鳴ったら**索引+status** と **深い分析**で割る」と書いてあったが、**実測すると 85 / 871** で
> **受け皿が即座に再び鳴る**。**測ってから「行為主体で割る」へ変えた（370 / 586）。**
> **見積もりは、現物を測るまで自分に都合よく外れる** ——分割線も例外ではない。

## B6 —— 名称。**識別子は空いている。問題は「Commons」と「Dedication」の 2 語である**

**2026-11-07 に足した**: 「dedication」という語について、CC0 の提出の前に Karl Fogel 氏が述べている（2012-01-02）—— *"Those sorts of promises are what the OSI evaluates and sometimes approves."*、*"I just don't think we should decide that on the basis of nominalism."* 同じ文に *"We could decide, for other reasons, not to evaluate any PD dedications."* も在る（`review-precedents.md` §1.138）。

**2026-11-08 に足した —— 名前は採用の側にも効く。** 0BSD の作者 Rob Landley 氏は、公有化に等しいライセンスに BSD 系の名前を付けた理由を *"In terms of decision making, "4 clause, 3 clause, 2 clause, zero clause BSD" tends to get rubber stamped. Despite other public domain equivalent licenses such as CC0 or MIT-0 having significant pushback from the same departments (when proposed independently)."* と述べ、*"there was explicit marketing strategy in my attempt to make a public domain equivalent license palatable to a broader population, and that strategy was working."* と書いた（`license-discuss` 2021-04・`rounds/2021-04-license-discuss-0bsd-naming-strategy-observed.txt`）。"Autonomous Commons Dedication" は既知の系列に属さない名前なので、企業の法務で同じ押し返しを受けうる（B2 の採用の側）。**逆側**: 審査は本文で決まる（Piana 氏 2018 *"A license must be approved for its text, not for its context"*・`reviewer-positions.md` §1.140）。Landley 氏の証言は一人の作者の経験で、法務の判断を測ったものではない。2026-10-24 の改名しない判断は変えない。

**#112 が記録したとおり、我々は数週間テキストを敵対的に読みながら、
「名前そのもの」を一度も検査していなかった。** 0BSD の改名は `license-review` で 54 通を要している。

**⚠ この測定は新しくない。** `AS-OF.md` に **2026-09-09 付**で同じ測定が既に在り、
**しかもそちらの方が詳しい**（最近似は `CAL-1.0` "Cryptographic Autonomy License" で語幹のみ共有、
という事実をこちらは持っていなかった）。**本節が足したのは disposition であって測定ではない。**
**「初めて検査した」と書きかけて、grep して取り下げた** —— #88 / #92 と同じ形
（**「X はどこにも無い」と書く前に X を grep する**）。

**測定（SPDX License List 3.28.0・727 件・`AS-OF.md` 2026-09-09 / 本増分で 2026-09-10 に再確認）**

| 検査 | 結果 |
|---|---|
| `ACD` で始まる識別子 | **0 件。空いている** |
| 名称に "Autonomous" を含むもの | **0 件** |
| 名称に **"Commons"** を含むもの | **58 件 —— 内訳は Creative Commons 55 / Open Data Commons 3。例外なし** |
| 名称に "Dedication" を含むもの | 2 件（`CC-PDDC` / **`PDDL-1.0` = *"Public Domain **Dedication & License**"***）—— **ただしどちらも OSI 承認ではない**。**命名の先例ではあるが、承認の先例ではない** |

**そこから出る 2 点**

1. **"Commons" は、この名前空間では事実上 2 つの組織のハウスマークである**（58 件すべて）。
   **商標の主張は誰もしていないし、我々も §11 で商標を持ち出さない。**
   だが**審査者が「Commons 系列の一員」と読む余地**はあり、
   **名前は merits として争われる**（#112）。
2. **"Dedication" だけの名前は、この instrument の半分しか言っていない。**
   本体は**献呈（§3）と、それとは独立に付与される許諾（§4・§4.4）**である。
   **Chestek 氏（委員・元委員長）の *"Which is it, a dedication to the public domain or a license?"*（#110）は、
   名前そのものによって強められている。**
   **そして同じ表に、その解き方が載っている** —— PDDL は
   ***"Public Domain Dedication & License"*** と名乗る。
   **ただし PDDL は OSI 承認ではない。使えるのは「名前でその対を表す前例が在る」ことまでで、
   「その対が承認された」ことではない。**

**最小の解消方法**: **1.0 は改名しない。** 凍結中であり、この名前で既に投稿され、
識別子は `machine.json` / `spdx.xml` / `FROZEN.md` / Check 441・453 に pin されている。
**successor 候補として、両方の半分を名前に持たせる案を記録する。**

**変更によって失うもの**: 改名は**継続性を失う** —— 既に公開した名前・識別子・digest・
`rounds/` の投稿本文がすべて旧名を指す。**#108（REUSE の命名要件）とも二重に絡む。**

**副作用・新たな反論**: 名前を変えれば「中身が変わった」と読まれる。
**逆に変えなければ、"Which is it" に対して名前が反証材料であり続ける。**
**どちらも実在する費用であり、片方だけを書かない。**

**外部確認**: 不要（測定は完了）。**status: 1.0 は改名しない。識別子の穴（E14）は 1.1 草案で閉じた** ——`ACD-N` / `ACD-N.N` の族へ保護を広げてある（**2026-11-01 追記**: その形は `ACD-1.4.1` のような 3 段の版番号を外していた。1.4 草案は「`ACD-` に数字が続く識別子」へ広げ、Steward の例外も新しい版番号と識別子に限った —— `ACD-1.0.errata.md` E14・`ACD-1.4-ADVERSARIAL-TRIAGE.md` の H-01 / H-17）。**名前そのもの（"Commons" / "Dedication"）は草案でも変えていない** ——**改名が継続性を失うという費用は、識別子の穴を塞いでも消えない**からである。

**2026-10-24 決定（AI・オーナーの委任による）—— 1.3 でも、承認まで改名しない。**
オーナー明言（同日）「OSI通過の為の何かで私の裁可が必要なものは無いよ」を受け、それまで「オーナーの判断待ち」と
されていたこの項目を AI が決めた。

**改名しない理由（3 つ）**:
1. **記録の継続性。** 1.0 はこの名前で `license-discuss` に投稿され、`rounds/`・機械可読面・digest・`FROZEN.md` が
   すべてこの名前を指す。**最初の `license-review` の直前に名前を変えると「中身が変わった」と読まれ、記録が 2 つに割れる。**
2. **"Which is it" に答えるのは名前ではなく本文である。** §4.1 は Langley 氏の試験（*"Licensor grants X rights"*）に
   通る許諾の動詞を持ち、§4.4 が許諾を §3 から独立させている（#270）。**Unlicense は名前に "license" を否定する語を
   持ったまま、承認されている** ——category は名前ではなく献呈という性質で決まった（*"Special Purpose"*）。
3. **名前の議論は高くつく。** 0BSD の改名は 54 通を要した（#112）。**新しい名前は、提出の瞬間に名前そのものの
   merits の議論を新しく開く。**

**逆側（改名しないことの費用・同じ重さで）**:
- **"Dedication" は半分しか言っていない**ので、名前を見ただけで Chestek 氏（委員・元委員長）の *"Which is it"* の枠に
  入れられうる（#110）。
- **"Commons" は CC / ODC の系列と読まれうる。** CC0 は特許の扱いで OSI の審査から撤回されたので、その連想は
  我々に不利に働きうる（ただしその特許の点こそ ACD が CC0 と違うところでもある）。
- **承認後は改名できない。** 改名が安いのは今だけである。

**それでも決定が保たれる理由**: 改名しない費用は**枠の費用**で、提出文と本文（§4.1 / §4.4）で答えられる。
改名する費用は**記録の継続性と新しい議論**の費用で、本文では答えられない。**見直す条件**: `license-review` で
審査者が名前そのものに merits の異議を述べたら、後継版で改名する（そのときの費用は今と同程度）。

**2026-09-10 追記（敵対的な利用者の視点で読んで出た）**: **§16.4 の保護は名前と識別子で非対称である。**
名前 *"Autonomous Commons Dedication"* は版を含まない形で書かれているので後続版にも及ぶが、
**識別子は `ACD-1.0` だけ**なので、**第三者が改変版を `ACD-1.1` として頒布しても条文には当たらない。**
**我々自身が 1.1 を予定しているため実務的な空きである**（`errata.md` **E14**）。
**承認されれば SPDX が識別子を固定するので、この穴は B11 と同じく承認で縮む。**

---

## B8 —— §12 人格権。**同じ条項が「gap」と「mission creep」の両方で名指しされている**

**この項目が難しいのは、賛否が割れているからではなく、賛否が同じ条項の別の面を見ているからである。**

**不利な側（3 件・いずれも一次資料）**

| 発言 | どこに当たるか |
|---|---|
| Carlo Piana 氏 *"these are **not licensable**, so anything the license says one way or the other, nothing changes"*（`license-review` 2023-11・#104）| **§12.1（放棄）に当たる。** ただし §12.2（不行使の合意）は**約束**であって許諾ではないので、同じ反論では倒れない |
| Pamela Chestek 氏が人格権条項の追加を **"mission creep"** と名指し（`license-discuss` 2026-06-23・#6）| **§12 全体に当たる。** 「ライセンスは著作権を扱うもので、人格権まで手を伸ばすのは範囲外だ」という筋 |
| **法域による非対称**（#118・2026-09-09 に自分で発見）| **§12.5 に当たる。** 虚偽の帰属に対抗する利益は、放棄が有効な法域では放棄され、**放棄不能な法域でだけ残る** ——「一貫していない」と読まれうる |

**有利な側（1 件・そして重い）**

Shuji Sado 氏（Open Source Group Japan 会長）は 2024-03 に、**著作権だけを述べるライセンス**は
—— Blue Oak を例に、0BSD と MIT-0 も同じ読みだとして ——
***"not open source, at least not in Japan"*** と論じている（§1.59）。**理由は同一性保持権が
日本ではソフトウェアに及び、改変を止めるのに使えるからである。**

**2026-11-07 追記 —— 同じ Chestek 氏の、逆向きの 2 通が在る。** 2021-02-20（本人の資格で・Ritchey）: *"Maybe your intention is to allow all permitted uses under
copyright law. But what about patent law? What about moral rights?"* 許諾が述べない権利は *"we are left only to guess"* と続く。
2024-09-09（`license-review`）: *"We consider patent rights specifically, and we have recently discussed moral rights. I believe there is sufficient expertise on the committee to
evaluate non-copyright provisions."* どちらも §12 を支持した文ではなく、2026 年の *"mission creep"* のほうが新しい。言えるのは、委員長が人格権を審査の外とは述べていないことである。

**つまり同じ §12 が、一方では「範囲外」と呼ばれ、他方では「これが無いと OSD 3 を
満たさない法域がある」と論じられている。** どちらも `license-discuss` / `license-review` 上の発言である。

**分岐（決めるのは我々ではない）**

| もし審査者が採るなら | §12 に起きること | 我々に残るもの |
|---|---|---|
| 「人格権は licensable でない」（Piana 氏）| §12.1 は無害だが**空**になる | **§12.2 は残る**（不行使の約束）。ただし約束が人格権について有効かは別途争われる |
| 「mission creep」（Chestek 氏）| §12 を削れという圧力 | **Sado 氏の論点が答えになる** ——削れば、日本で改変が止まりうる |
| 「法域で結果が変わるのは不整合」（#118）| §12.5 の書き直し | **1.1 には入らず、1.2 草案で扱った**（errata **E26**: §12.2 が *"You are not required to determine which of Section 12.1 and this Section applies … and nothing permitted by this Dedication depends on that question"* と述べ、非対称を条文の側から説明する。**§12.5 自体は書き直していない**。**2026-09-28 訂正**: 旧文は「1.1 候補として `errata.md` に記録済み」だったが、errata に §12.5 の項目は無く、指し先が実在しなかった）|

**最小の解消方法（分類 1・提示の変更）**: **§12 を「人格権も扱う」ではなく
「改変の自由を、著作権だけでは保証できない法域で保証するための条項」として提示する。**
**mission creep への答えは、範囲の弁明ではなく OSD 3 との接続である。**

**変更によって失うもの**: 無し（提示の変更のみ）。**条文は凍結中で触らない。**

**残る gap**: **§12 が有効かどうかは、我々には決められない。**
§12.2 は「不行使の約束」であって、**それが人格権について各法域で有効かは弁護士の領域**である
（B1 と同じ壁）。**「無効かもしれない」と書いてある条項を、有効であるかのように書かない。**

**外部確認**: **必要**（B1 と同じ）。**status: 分岐を記録済み・提示のみ調整可。**

---

## B9 —— §7 データベース権。「未検証・削除候補」だったので、検証した。**削除しない**

**検証したこと**: §7 は 67 語 2 項。**§1.5（Covered Rights の定義）が既に
*"sui generis database rights"* と *"rights against unfair extraction"* を含んでいる**ので、
**§7 は丸ごと重複ではないか**を確かめた。

| 項 | 語数 | 判定 |
|---|---:|---|
| **§7.1**（DB 権は Covered Right であり §3〜§6 が適用される）| 24 | **重複である。** §1.5 が権利を含み、§3〜§6 は Covered Rights 全体に働く。*"To the extent … subsists"* も §1.5 の *"whether or not presently subsisting"* と同じ |
| **§7.2**（全部または実質的部分を、反復的・組織的に、無制限・無条件に抽出し再利用してよい）| 43 | **重複ではない。削除しない** |

**⚠ 逆側（2026-09-15 追記・種類 8 の掃引で出た）。** **この節の見出しは「削除しない」と述べるが、同じ節の表は §7.1 を「重複である」と述べている。** 見出しが表より広い。
**保持の費用は 24 語** ——**B3（長さ）の測定に直接乗る量であり、しかも「重複」は *"excessively wordy"* という既出の批判が名指ししうる形そのものである。**
**それでも保持する理由**（明示しておく）: §7.1 は §1.5 と §3〜§6 の関係を**その場で読める形**にしており、**削れば読み手は 3 条を辿ることになる**（#99 の読み順問題と同じ）。**24 語はその対価である。**
**この判断は再検討しうる** —— B3 の削減候補一覧（`ACD-1.1-CHANGELIST.md`）に **§7.1 は入っていない**ので、**入れるかどうかは次版を確定するときの判断**である。**「削除しない」はここでは §7.2 についてだけ確定している。**

**§7.2 が独立に働く理由**: sui generis 権は **行為の語**（抽出 / 再利用 / 実質的部分 /
反復的かつ組織的）で定義されており、**一般的な許諾文が同じ行為に届くかは自明ではない。**
とくに *"repeatedly and systematically"* は、**些少部分の反復抽出を禁じる側の規律**に
正面から当たる語である。**学習用データセットの構築は、まさにこの行為の形をしている。**

**さらに、これは委員長が「モデルを保護しうる理論の一つ」として挙げた当の権利である**
（`reviewer-positions.md`）。**削るのは、審査者が名指しした論点から条文を引くことになる。**

**変更によって失うもの**: §7.1 を落とせば 24 語（本体の 0.5%）。**B3 の結論
（機構部を削っても届かない）を踏まえると、この 24 語のために「EU の審査者が
見出しから中身へ入ったとき、まず権利の帰属が書いてある」構造を崩す価値は無い。**

**結論: §7 は削除しない。§7.1 は successor で 1 文に圧縮する余地があるが、優先度は低い。**
**表の status を「未検証（削除候補）」から「検証済み・保持」へ変える。**

**外部確認**: 不要。**status: 検証済み。**

---

## B13 —— 理解コスト。B3 の結論により、これが長さへの唯一の実効的な緩和になった

**位置づけの変更（2026-09-09）**: B3 は「縮められるが答えきれない」と結論した（§2.8）。
**したがって長さへの実効的な緩和は本文の外にしか無く、それが B13 である。**
表の impact 高は据え置き、**status を「部分的に解消済み」から「継続対象」へ変える。**

**測定（2026-09-09・語オフセット）**

| 面 | 規模（**2026-09-09 実測**）| 審査者が必要な答えに到達するまで |
|---|---:|---|
| 送る文面 `submission.md` §B.0 | **972 語** | gap 24% / 最近似 49% / 法的レビュー 8% / 提出者専用でないこと 85% |
| 入口 `REVIEWERS.md` | 2,402 語 | **改善前: gap 35% / 最近似 30% / 法的レビュー 29%** → **改善後: 5% / 8% / 9%** |
| `objection-map.md` | 653 語 | 1 つの表 |
| `against.md` | 29,586 語 | 完全な記録（#120 で経路を直した）|

**この表は 2026-09-09 の測定である。** **数え方は macOS の `wc -w`（UTF-8）で、記録に書いていなかった**（2026-11-02 に各 file の当日の git 版で再現して特定）。英語だけの `REVIEWERS.md` は空白区切りでも同じ値になるが、**日本語を含む 2 つは数え方で値が割れる** —— `objection-map.md`（09-09 23:44 の版）は `wc -w` 653・空白区切り 634・ASCII 文字を含む語 367、`against.md`（09-09 23:54 の版）は 29,586・29,583・28,563。比べるときは同じ数え方で数え直すこと。 §B.0 はその後 1,362 語（2026-09-24）に伸びた。現在値は §B.0 の見出しを読むこと（Check 460 (p)）。
**🔴 2026-09-24 に測り直した入口ページ**: `REVIEWERS.md` は **2,402 → 4,353 語（+81%）** に伸び、冒頭へ "The short path" と "Which text you are looking at" が足された結果、**"In one screen" は 4% → 15% の位置へ押し下げられ**、gap への到達は **5.7% → 16.2%**、最近似への到達は **8.4% → 24.8%** に悪化していた（上の「改善後」は、その後の追記で黙って崩れていた）。**"In one screen" を "Which text" の前へ移した**（引く条 §4.4 / §6 / §8.4 / §9 はどちらの版でも同じ番号なので、版の対応表より先に読んでも意味が変わらない）。移動後は **In one screen 6.9% / gap 8.2% / 最近似 16.8%**。2 つの弱点は "The short path" の表で **約 3%** に在る。**⚠ 逆側: 4% には戻っていない** —— 冒頭の "The short path"（読む量の見積もりと、止めたときに失うもの）は審査者の時間を節約するための節で、削らない。**入口が伸びるのは開示を足すたびに起きるので、次に入口へ節を足すときは "In one screen" より前に置かないこと。**

**🔴 2026-11-06 に測り直した入口ページ**: `REVIEWERS.md` は **4,353 → 5,370 語（+23%）** に伸びていた。"In one screen" は 641 語で 1 画面ではなくなり、Status は 1,159 語で、審査者が主張へ着く前に経緯の段落を読む形だった。中身も 11-04 の結論からずれていて、*"The same gap, in detail"* が §6 / §8.4 / §9 を「同じ gap」と名乗り、§1.134 が独自性の根拠から外した §6.1 と §9 を含む別の 3 項目を挙げていた。直して **4,411 語**、"In one screen" は 7 割（**先頭から 375 語の位置**）、最近似への到達は **886 → 666 語**、Status は 524 語にした。経緯の細部は B14 と `against.md` に既に在るものだけを外し、開示は減らしていない。**2 度目の退行である**（1 度目は 09-24）——**追記のたびに伸びるのは入口ページの性質で、1 度直しても止まらない。**

**🔴 2026-11-06: 勧めた文書が、勧めた相手に読めなかった。** `REVIEWERS.md` は英語の審査者へ「3 つ読めば足りる」と案内し、その 1 つが `objection-map.md` だが、**表の 30 行中 28 行に日本語が入っていた**（案内の 827 語は ASCII を含む語だけの数で、日本語の分を数えていなかった）。"short path" の 3 分の 1 が審査者に読めない状態で、2026-09-09 から続いていた。本文を英語へ書き直し、09-22 以降に抜けていた反論（#211 / #265 / #266 / #276）と、窓の外でも判断を左右する 6 件（#237 / #255 / #262 / #263 / #270 / #280）を足した。Landley 氏の行の答えは §1.133 の結論へ改め、「GPLv3 より 43 語短い」は相手がしていない比較なので外した（#116）。**短い道は 5,950 語から約 7,450 語へ増えた** —— 語数が増えたのではなく、数えていなかった分が見えた。

**2026-11-07**: 決める側の文書から足した記録で、短い経路は約 7,550 語から約 8,050 語へ伸びた（`objection-map.md` 2,451 → 2,938 語）。最初の画面は 500 語の上限を保った。**記録を足すほど B13 の費用は上がる**ので、次に足すときは同じ行の説明を削れないかを先に見る。

**2026-11-06 後半**: 有利な記録の表（OSI の FAQ・理事会の議事録・審査者の発言）と基準 8 条の表を足し、`REVIEWERS.md` は 5,518 語へ戻った。**増えた大半は後ろの "The case" の節で、"In one screen" の位置は 375 → 391 語、最近似への到達は 666 → 758 語へ少し伸びた**（承認されるべき理由を先に足した分）。Check 472d / 472g が先頭の 2 節を守り、それより後ろは守らない。

**やったこと**: 入口ページの冒頭に **"In one screen"** を置いた ——**何であるか / 主張する gap /
最近似の承認済みライセンス / 2 つの弱点 / 提出者専用でないこと / 次に読む 1 件**。
**弱点（法的レビュー無し・採用 1 件）を、主張より前ではなく同じ画面に置いた** ——
後ろに置けば「見つけさせる」形になる。

**なぜ改善前は 30% だったのか（自作の退行）**: **B14 の停止告知を Status に足したのは同じ日の
自分である。** 状態の説明が増えた分だけ、主張と弱点が下へ押し出された。
**#120 と同じ族 ——最後に書かれ、最初に読まれるページ。**

**2026-09-10 追記 —— B13 には天井がある。** Chestek 氏（委員・元委員長）は 2026-09-01 に、条文の外にある説明について
*"you can't count on FAQs to prevent an unintended interpretation"* と述べ、
**「四隅の外」の記述は intention の証拠にしかならないとした**（#124）。
**短い入口は読まれる確率を上げるが、それ以上は上げない ——審査は四隅で決まる。**
したがって **B13 の投資は「読まれる確率」までで頭打ちであり、答えは条文の中に置くしかない**
（§4.4 がその唯一の実例）。

**⚠ ただし四隅の原則が当たる範囲を、広く取りすぎないこと。**
**この原則は「条文がどう解釈されるか」に当たる。「OSI が承認すべきか」には当たらない。**
後者は委員会への議論であり、**ドシエこそが正しい容れ物である。**

**当たる 9 件を手で分類した（2026-09-10・grep ではなく読んで）**

| 反論 | 答えの在り処 | 種別 |
|---|---|---|
| 献呈と許諾の並置（#110）| **§3 / §4 / §4.4 / §11.3** | **条文内・構成の問題** |
| 人格権は licensable でない（#104）| **§12.1 と §12.2 の二段構え** | **条文内・構成の問題** |
| 特許射程が uptake を下げる（#107）| **§8.1 / §8.4 / §8.2（報復ゼロ）** | **条文内・構成の問題** |
| mission creep（#6）| **§12 は条文内**だが、必要性の論拠（日本の同一性保持権）は散文 | 混在 |
| なぜもう一つ（#84）| **§12 は条文内**だが、「類型に 1 件足す費用」の議論は散文 | 混在 |
| 弁護士が要る（#5 / #79）| **条文では答えられない** ——事実の欠落である | 承認政策 |
| 長すぎる（#6）| 語数と比較は散文（§4c）| 承認政策 |
| 1 文書に 3 つのこと（#105）| 構成の説明は散文 | 承認政策 |
| 一つの instrument に一つの権利（#102）| 同上・しかも #105 と逆を向く | 承認政策 |

**読み方**: **構成の問題 3 件は条文内で答えており、四隅の基準を満たす。**
**混在 2 件は、条文が「何をするか」は述べているが「なぜそれが要るか」は述べていない** ——
**そして「なぜ」は解釈の対象ではないので、散文で足りる。**
**承認政策 4 件は、条文に書いても解決しない**（むしろ B3 の長さを悪化させる）。

**したがって successor で条文へ移すべきものは、実は多くない。**
**#124 を「全部を条文へ入れろ」と読むのは過剰修正である。**

**この節が establish しないこと**: **理解コストを下げても、長さそのものは変わらない。**
Chestek 氏が engage しなかった 2 例は**ライセンス本文**の語数で述べられている（#116）。
**短い入口は「読んでもらえる確率」を上げるだけで、「長い」という評価を消さない。**

**外部確認**: 不要（AI だけで前進可能）。**status: 継続対象。**

---

## B3 —— 長さ。測定が解消経路を示した

**なぜ承認上の問題か（事実）**: Chestek 氏が長さを理由に engage しなかった記録が **2 件**ある（2024-10 は委員長として・2026-06 は委員として） ——
*"approximately 4500 words … **I have not read these licenses in detail**"*（2024-10-05）と
*"3888 words … **excessively wordy** … not a good candidate for approval"*（2026-06-23）。
**ACD-1.0 は 4,896 語**（本体 4,574）で、**両方より長い**。

**測定（本体 4,574 語・2026-09-09）**

| 区分 | 語数 | 割合 |
|---|---|---|
| **gap 部**（§6 ML/TDM 282・§8 特許 583・§9 機械生成物 176）| **1,041** | **23%** |
| **machinery 部**（§1 575・§2 558・§13 108・§14 98・§15 328・§16 356）| **2,023** | **44%** |
| その他（§3 §4 §5 §7 §10 §11 §12）| 1,510 | 33% |

**最小の解消方法（分類 2 / 3 / 4・gap 損失ゼロ）**

| 対象 | 語数 | 削れる理由 |
|---|---|---|
| §2.9 | 111 | *"not executory"* は forum が決める分類（**E5 が既に記録**）。事実だけ述べて結論を落とす |
| §15.2 / §15.3 / §15.5 / §15.6 | 168 | 単複・contra proferentem・沈黙・代理否認。**MIT / 0BSD は 1 つも持たない** |
| **§16.4 + §16.5** | **165** | 文書自体の再頒布制限と翻訳例外。**落とすと E2 / E3 / E12 と #108 隣接も同時に縮む** |
| §1.10 "Reservation" の inline 化 | ≈40 | 使用箇所は §6.2 / §6.3 のみ |
| §2.5 の圧縮 | ≈45 | estoppel は §2.2 の irrevocable と重複が大きい |

**合計 ≈529 語（本体の 12%）。** ← **2026-09-09 に実際に置換文を起草して数え直した結果、正しくは 306 語（6.7%）である**（内訳と起草文は `ACD-1.1-CHANGELIST.md` §2.6）。**見積もりは 42% 外れていた** —— 節の大きさを削減量として数えたためで、§2.9 は事実を残すので 56、§15.5 は統合なので 57、§16.4+§16.5 は書き足すので 45、**§1.10 の inline 化は撤回**（"Reservation" は §2 でも使われており、74 語の列挙を3 箇所へ展開すれば長くなる）。

**そしてこれで足りないことが分かった** —— 改定後は全体で約 4,590 語で、**Chestek 氏が engage しなかった 2 例（3,888 / 約 4,500）をどちらも下回らない**。**B3 は「無駄を削る」問題ではない。** そして **(b) 構造変更（説明的な節を附属文書へ出す）も成立しない** ——測って否定した（`ACD-1.1-CHANGELIST.md` §2.7）。**附属文書は審査対象ではないので移せるのは「争われても条文で答える必要がないもの」だけ**だが、引用密度が最も低い 4 節（§14 責任制限 / §13 無保証 / §5 不行使の合意 / §15 解釈・可分性）は**どれも移せない**（無保証条項の不在は permissive ライセンスとして成立しない／§5 は §3 が無効な場合の受け皿で§4.4 と対の中核主張／§15.4 は他条が名指しで参照）。

**残る道は (c) 本文内での圧縮のみで、対象は §1 + §2 + §15 + §16 = 1,797 語（本体の 39%）。**
**3,888 語を下回るにはこれを半分以下にする必要があり、gap を損なわずに可能かは未実証。**
**実際に最大の定義 3 件を書き直して測った（§2.8）—— 228 → 182 語＝ 20%、意味の変化なし。**
**その率を機構部 1,797 語すべてに外挿しても約 360 語**（外挿であって測定ではない）で、
§2.6 の 306 語と合わせて **4,896 → 約 4,230 語。3,888 語には届かない。**

**2026-09-10 夜・実物で確かめた**（**語数はその後の errata 修正で動いた** —— 権威は草案自身の宣言と Check 468。2026-09-11 実測 **4,866 語**）: 1.1 草案は **4,742 語・77 条**（1.0 は 4,896 語・82 条）で、
**正味 −154 語（3.1%）にしかならなかった。** 内訳は **機構部で −302**、
**正確さのために +148**（E12 の notice の限定 +18 / E16 の opt-out 可視化 +55 /
E15 の因果の限定 +75）。**削減の半分が、欠陥を閉じる語で相殺された。**

**そこから出る、B3 についての最も重要な事実**: **長さは正確さと直接競合する。**
**「短くする」を目標にすると、閉じるべき欠陥を閉じない方向へ圧力がかかる。**
我々は**正確さを選んだ**（言い過ぎを削るのに語が要るなら、語を足す）。
**したがって B3 は successor でも解消されない。**

**🔴 2026-09-24 追記（上の 4,742 / 4,866 は凍結前の途中値だった）**: **凍結された 1.1 は 5,051 語・78 条で、1.0（4,896 語）より +155 語（+3.2%）長い。** 1.2 草案は**その時点で** 5,299 語・80 条（+403 語・+8.2%）だった。**草案は伸びるので現在値は草案冒頭の申告を読むこと**（Check 468c が実測と照合する・2026-09-26 時点は 5,335 語）。1.1 は凍結 pin が実測と一致させている。**この節は「1.1 で −154 語」までしか書いておらず、successor が 1.0 より短いと読める状態で止まっていた。** **結論（縮められるが答えきれない）は変わらない。変わったのは向きで、successor は実際には長くなり、長さは正確さと競合するという上の事実を実物が裏づけた。**

**2026-11-04 追記 —— 語数ではなく読みの分岐を対象に、1.4 草案で試した（`ACD-1.4-CLARITY-TRIAL.md`）。** 採用したのは −157 語（§2.8・§12.4 の理由の文 −79 / §13.2 への案内と §11.4 の理由の文ほか −63 / §1.3 と §9.1 のパラメータの名指し −15）で、本文が自分で作っていた反対解釈の分岐が 3 件と、§4.6 の指示語の分岐が 1 件消えた。草案全体は 1.3 の 5,443 語より短くなった（現在値は草案冒頭の申告が権威）。
**⚠ 逆側**: 理由の文 9 件のうち 6 件は残した。§6.5 前半と §8.4 は審査者向けの文書が本文の言葉として引いており、§11.3 は §9.4 が指す理由そのもので、§8.3 は操作条項の指示語の先である。**理由の文は反対解釈の種であると同時に、我々の答えの置き場でもある** ——四隅の原則（#124）のもとでは、外すと答えが本文の外へ出る。**−157 語は本文の約 3% で、下の結論は変わらない。**

**結論: B3 は「解消できる項目」ではなく「縮められるが答えきれない項目」である。**
gap 部 1,041 語を削れば届くが、**それは B10（新規性の根拠が残っているか・最高位）を
悪化させるので取引として成立しない。** **残る緩和は本文の外にある短い入口だけ**で、
2026-09-09 の実測では送る文面 972 語 / 入口ページ約 1,900 語（**同日の B13 の表は 2,402 語で、git の同日版も 2,402 語。約 1,900 は誤り**）/ objection-map 653 語（`wc -w`・空白区切りなら 634。数え方は B13 の表の注）＝
**審査者が最初に触れる面は本文の 1/5 だった。**
**⚠ 2026-09-24: 送る文面は 1,362 語になった**（+40%・現在値の権威は `submission.md` §B.0 の見出しで、Check 460 (p) が実測と照合する）。増えた分は来歴と弱点の開示であって削れる無駄ではないが、**唯一の実効的な緩和である短い入口が、本文の 1/5 から 28% へ伸びている。**
**successor 候補の置換文は 7 件・約 350 語・gap 損失ゼロ**（§2.6 + §2.8）。

**より大きな再設計**: §1 の定義 10 件のうち `Contribution`（§2.6 のみ）と
`Machine-Generated Material`（§9 のみ）を使用箇所へ inline すると更に ≈100 語。
**ただし §1 は前方参照が 3 件ある（E13）ので、並べ替えと同時に行う。**

**変更によって失うもの**: §15.2〜§15.6 は「争われたときの防御」であって「許諾の内容」ではない。
**失うのは防御であって gap ではない。** §16.4 を落とすと**識別子が固定テキストを指す保証**が
消える —— これは §16.4 の目的そのものなので、**代替（凍結 + 公開 digest）で置き換えられるかを
検討してから決める。**

**変更後も残る gap**: §6 / §8.4 / §9 は 1 語も触らない。**23% がそのまま残る。**

**副作用・新たな反論**: 短くすると「防御が薄い」と読まれうる。ただし
**MIT・0BSD・Unlicense はいずれもこの種の防御を持たずに承認されている**ので、
**先例のある方向への移動である。**

**外部確認**: 不要（AI だけで前進可能）。**status: successor candidate 化済み** ——条項ごとの判定は `ACD-1.1-CHANGELIST.md` §2.5。

**⚠ 見積もりを 1 件撤回した。** 当初「§16.4 + §16.5 を落として 165 語」としたが、§11 の問い（**これが無いと何が壊れるか**）を当てると **§16.4 は登録されるまでの橋**だと分かった ——MIT / 0BSD / Unlicense が同じ条項を持たないのは **SPDX と OSI がテキストを固定しているから**で、**ACD-1.0 はまだどちらにも載っていない**。**削除ではなく §16.5 を §16.4 へ統合**し、節約は 165 → **≈85 語**。**総計 ≈529 語は据え置き**（他候補の内訳で吸収）。

---

## B12 —— class 9（2026-11-07 に 11 から移した）

**steward が 1 人**で、承継の仕組みが無い。**設計変更では解けない**（条文を直しても steward は
増えない）。分類 9（外部証拠）に見えるが、**採用を増やすためにライセンスを歪めない**という
方針に照らすと、**現時点で我々が取れる行動が無い**ため 11 とする。
**採用が自然に増えたときに 9 へ移る。**

**⚠ 2026-09-17 ——「解消方法不明」は、束をほどかずに出した結論だった。**
この項目は **2 つの別の事実**を束ねていた: **(a) steward が 1 人であること**（世界についての事実）と
**(b) 承継の仕組みが無いこと**（**文書についての事実**）。**(b) は条文で扱える。**
1.1 草案の §16.5 が *"the Steward"* を機能で定義し、**その役割が譲渡されうることを条文に置いた**
（先例は EPL-2.0 —— *"may assign the responsibility to serve as the Agreement Steward to a suitable
separate entity"*・SPDX の canonical text で逐語確認）。

**分類は 11 のままにする。** 残っているのは **(a)** で、そこは条文では動かない ——
**「半分が条文の問題だった」を「解消した」と読み替えない。** 承継が*可能*であることと、
**承継先が実在すること**は別であり、後者はいま存在しない。

**⚠ 2026-11-07 ——「解消方法不明」も、出典より不利に書いていた。分類を 9 へ移す。**
残っていた (a) を一次資料へ当てると、リストが恐れてきたのは人数ではなく**支配**だった。

- **信頼が要る場面は名指しされている。** Bradley Kuhn 氏（`license-review` 2018-11-22・SSPL の審査）:
  *"Brendan's comments caused me to realize that OSI really does need to trust the license steward when an
  upgrade clause is in play."* ACD に upgrade 条項は無い。§16.2 は版を名指し、§16.4 は各名前と識別子を 1 つの固定テキストに結ぶので、
  受領者は steward を信頼しなくても固定の本文に依拠でき、新しい版は既に献呈された著作物へ届かない。
- **個人への不信は実際に述べられ、解かれている。** Lawrence Rosen 氏の回想（`license-discuss` 2012-10-03）:
  *"Nobody trusted that I personally (or my heirs) would forever have the good of the community at heart. I agreed
  with them. That was my incentive to write section 16 of those licenses, which declared authorship but disclaimed
  control over changes."* その §16 は、改変を別の名前でなら許し、名前を独占し、既存の著作物の再許諾を封じる形で、
  ACD §16.4 と同じ構造である。AFL-3.0 / OSL-3.0 / NPOSL-3.0 は今も承認済みの一覧に在り、
  本文は *"Copyright © 2005 Lawrence Rosen"* と述べ、本人は 2016 年に *"this license steward (me!)"* と書いている。
- **steward を持たないことも普通である。** 141 本の本文を測ると、*license steward* / *agreement steward* の語を持つものは
  8 本である（語の検索なので床）。Richard Fontana 氏（`license-discuss` 2019-05-31）:
  *"MIT is not the license steward of the MIT license -- there is no license steward"*。
- **上の版を外す選択も退けられていない。** Piana 氏（`license-review` 2025-05-29・Tiwaz）:
  *"a legitimate choice and I won't fuss about it. There are different views on this kind of provisions."*

**逆側を同じ重さで書く。**

- **steward が誰かは見られる。** 同じ Kuhn 氏の同じ 1 通: *"I \*do\* think OSI should consider who the license steward is
  and what their motivations are as part of the license approval process."* 氏の見解であって OSI の声明ではないが、
  upgrade 条項に限っていない。
- **版を動かせない設計には費用がある。** Rob Landley 氏（`license-review` 2025-07-19）:
  *"Given that the law tends to change every few years even in individual jurisdictions, walling that option off for
  anything nontrivial seems a bit weird."* Brendan Hickey 氏（同 2019-01）: *"Use a well known open license with an upgrade
  clause if you're concerned about novel legal developments."* ACD の答えは新しい版と再適用で、すでに配られた著作物には届かない。
- **Rosen 氏は弁護士で、回想は 1 人の記憶である。** 同じ解き方が個人の非弁護士にも効くとは言えない。
  Piana 氏は「個人であること」を理由に下げないでほしいという提出者への返信で、審査の延期を勧めている（2026-06-19）。
- **§16.4 は Steward に新しい版の権利を残す。** OSL の §16 との差は 2 点で、OSL は改変ライセンスに OSI の承認なしで
  open source と言うなと足し、ACD は Steward の版の出し方を書く。役割の非対称は `submission-osd.md` §3b-i に在る。
- **承継先は実在しない。** §16.5 は譲渡を許すが、譲渡の前に steward が欠ければ、本文では役割は空く（§2.8 の承継人は Work についての文で、§16.6 が §16.4 / §16.5 を Work の条項から外す）。一般の承継法が別の結果を与えるかは未確認である。その場合に止まるのは
  その名前での新しい版だけで、著作物の許諾は何も変わらない（§10.4）。別の名前での改変も止まらない。

**分類を 9 に移す理由。** 解き方は分かっている —— 引き受ける人を見つけて §16.5 で指名することである。
必要なのは第三者の同意で、それは分類 9 の形である。**steward が 1 人である事実は変わっていない。**
**「解き方が分かった」を「解けた」と読まない。**

**一般形**: **1 つの項目を確かめて、項目が指す集合について結論していた。**
`BLIND-SPOTS.md` が「集合の 1 つを確かめて集合について結論した」と呼んでいる形の、register 側の実例である。

---

## 更新規約

- 新しい問題は**必ずこの表へ入れ、分類を付ける**。分類が付かないものはボトルネックではなく
  `against.md` の不利な事実に留める。
- **詳細分析**（なぜ承認上の問題か / 事実・推論・予測の別 / 最小の解消方法 / より大きな再設計 /
  失うもの / 残る gap / 副作用 / 新たな反論 / 外部確認の要否）は当該項目の節に書く。表は索引。
- **revision のたびに集計を比較する。** 減っていなければ revision 自体を疑う。
