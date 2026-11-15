---
file: LICENSES/REFLECTION-BACKFILL.md
audience: 監査人, ai, OSI license-review / license-discuss participants
last-updated: 2026-11-15
reachable-via: README.md
canonical-ref: LICENSES/ACD-1.0.review-readings.md / LICENSES/ACD-1.0.review-readings-2.md / LICENSES/REVISION-PROTOCOL.md (§3.6 の 6c)
---

# 古い節の反映先（§1.242 より前の review-readings の節）

2026-11-15 から、`ACD-1.0.review-readings*.md` の節は末尾に「**反映**:」の行を持つ（2f の提案・Check 501）。それより前に書いた §1.164〜§1.241 には欄が無かった。提出のゲート（`REVISION-PROTOCOL.md` §3.6 の 6c）は「読んだ節がすべて反映されている」ことを求めるので、古い節の反映先をここに表で置く。

**節の末尾に足さず表にした理由。** 古い節の多くが在る `ACD-1.0.review-readings.md` は 989 行で、54 節に 2 行ずつ足すと 1,000 行の上限（Check 365）を越える。節を別の文書へ動かすと、他の文書が `review-readings.md` の節を番号で引いている参照が壊れる。表なら、どちらも起きない。**逆側**: 節を読む人は、反映先を知るためにこの表を引く必要がある。

**書き方。** 1 節に 1 行。番号のセルは「1.179」と書き、§ を付けない（まだ在らない節を § で引くと Check 471 (e) が RED になるため）。反映のセルは Check 501 と同じ語彙（B# / against #N / errata E# / 1c / THIRD / 入口 / なし（理由） / 未定）で書く。確かめ方のセルには、その反映先が本当にその節を引いているかをどう確かめたかを書く。同じ節に、末尾の欄とこの表の行の両方を置かない（Check 501 が RED にする）。帯の分け方は 9b が数えた（2f 1.164〜1.178・30 1.179〜1.191・50 1.192〜1.207・1c 1.208〜1.222・9b 1.223〜1.241）。**§1.163 以前の行は、文書の名を番号の前に置く**（例「`ACD-1.0.review-precedents.md` 1.45」・Check 501b がこの形で見出しに当てる）。§1.69 以下は文書ごとの番号で 1.67〜1.69 が review-corpus と review-venue の両方に在り（Check 500 の床）、番号だけではどちらの節かを決められないため。この帯は文書ごとに分けた（2f の案・2026-11-15）。**床の下の行の確かめ方**: 引く側の行が「§1.49」と書いていても、別の文書の §1.49 のことがある。引く側の行がその文書の名も挙げているかを見て、挙げていなければ中身の一致を読んで確かめたと書き分ける（portfolio-30 の注意）。

| 節 | 反映 | 確かめ方 |
| :-- | :-- | :-- |
| `ACD-1.0.dig-2026-09.md` 1.91 | against #164 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.dig-2026-09.md` 1.93 | against #164 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.dig-2026-09.md` 1.94 | なし（測り方の訂正で、ACD の論点に当たる読みを持たない） | 節の読みを当て直して判断した（2026-11-15・portfolio-2f） |
| `ACD-1.0.dig-2026-09.md` 1.95 | against #150 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.96 | 入口（`ACD-1.0.submission-reference.md`・`ACD-1.0.comparison.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.97 | 入口（`REVIEWERS.md`・`ACD-1.0.comparison.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.104 | 入口（`ACD-1.0.comparison.md` の比較の本文） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.129 | against #272 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.130 | 入口（`REVISION-PROTOCOL.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.133 | B10（`ACD-OSI-BOTTLENECKS.md` の B10 の行と #84 への答えの段）/ THIRD（`ACD-1.4-CLARITY-TRIAL.md`）/ 入口（`REVIEWERS.md`・`ACD-1.0.submission-reference.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.134 | B13・B15（`ACD-OSI-BOTTLENECKS.md`）/ against #237・#283 / THIRD（`ACD-1.4-SECOND-CLARITY-TRIAL.md`）/ 入口（`ACD-1.0.submission-reference.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.135 | B10 / THIRD（`ACD-1.4-SECOND-CLARITY-TRIAL.md`）/ 入口（`ACD-1.0.submission-reference.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.136 | B7・B10 / against #284 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.137 | B10（`ACD-OSI-BOTTLENECKS.md` の #84 への答えの段） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.139 | B10 / against #290 / 入口（`SUBMISSION-MATERIALS.md`・`OSI-APPROVAL-PLAN.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.143 | B4（`ACD-OSI-BOTTLENECKS.md` の英語の索引）/ against #307 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.144 | B10（`ACD-OSI-BOTTLENECKS.md` の英語の索引）/ 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.145 | against #307 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.146 | B4・B10 / against #314 / 入口（`REVIEWERS.md`・`SUBMISSION-MATERIALS.md`・`QUESTIONS-FOR-COUNSEL.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.148 | 未定（B10・2011 年の「公有化の標準の文書が無い」・30 へ） | この節の番号を引く反映先は grep で 0 件だった（2026-11-15・portfolio-2f）。送り先を書いた |
| `ACD-1.0.gap-measurements.md` 1.149 | 未定（B10・明示の特許許諾と共同体への必要性の説明・30 へ） | この節の番号を引く反映先は grep で 0 件だった（2026-11-15・portfolio-2f）。送り先を書いた |
| `ACD-1.0.gap-measurements.md` 1.150 | 未定（B10・CC0 の審査中に出た直し方の提案。引く側は `ACD-1.0.reviewer-positions.md` の分析だけ・30 へ） | この節の番号を引く反映先は grep で 0 件だった（2026-11-15・portfolio-2f）。送り先を書いた |
| `ACD-1.0.gap-measurements.md` 1.151 | errata E69 / THIRD（`ACD-1.4-SECOND-CLARITY-TRIAL.md`）/ 入口（`OSI-APPROVAL-PLAN.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.152 | 未定（B4・Unlicense の審査の「裁判所が OSD に反して読みうるか」の基準・30 へ） | この節の番号を引く反映先は grep で 0 件だった（2026-11-15・portfolio-2f）。送り先を書いた |
| `ACD-1.0.gap-measurements.md` 1.153 | against #311 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.154 | B1 / against #305・#312 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.160 | 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.161 | 未定（1c 種・§8 の特許の許諾をどこまで伸ばすと許諾者の特許が空になるか・1c へ） | この節の番号を引く反映先は grep で 0 件だった（2026-11-15・portfolio-2f）。送り先を書いた |
| `ACD-1.0.gap-measurements.md` 1.162 | 入口（`ACD-1.0.review-responses-meta.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.163 | against #309 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.164 | 未定（B10 の G1 の説明の出典・2012 年の CC0 の審査で特許の明示の除外が論点だったことの一次資料・30 へ） | この節の番号を引く反映先は grep で 0 件だった（2026-11-15・portfolio-2f）。送り先を書いた |
| 1.165 | なし（ACD は §4 と §8 で著作権と特許を同じ文書で許諾し、著作権の無いものに特許だけを許諾する場面を持たない） | 節の読みを当て直して判断した（2026-11-15・portfolio-2f） |
| 1.166 | against #316 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.167 | B2・B10・B15（`ACD-OSI-BOTTLENECKS.md`）/ against #302・#323 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.168 | B10（`ACD-1.0.board-decisions.md` の追加テストの段が出典として引く） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.169 | 未定（データベース権の枝は B15 の材料、提出者の名前の枝は B6 の材料・30 へ） | この節の番号を引く反映先は grep で 0 件だった（2026-11-15・portfolio-2f）。送り先を書いた |
| 1.170 | 入口（`ACD-1.0.review-responses-meta.md` の SimPL の段・立証の責任は提出者にある） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.171 | against #318 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.172 | against #302・#309・#318 / 入口（`SUBMISSION-MATERIALS.md` の手順 6） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.173 | B15（`ACD-OSI-BOTTLENECKS.md`）/ 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.174 | 未定（B2・採用の表明があっても使用を制限する条件で止まった例・30 へ） | この節の番号を引く反映先は grep で 0 件だった（2026-11-15・portfolio-2f）。送り先を書いた |
| 1.175 | B15（`ACD-OSI-BOTTLENECKS.md`）/ 入口（`SUBMISSION-MATERIALS.md` の主題の行） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.176 | against #257 / 入口（`SUBMISSION-MATERIALS.md` の手順 7） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.177 | 未定（B10・§1.168 と同じ線の「OSD に適合するものを全部か良いものだけか」・30 へ） | この節の番号を引く反映先は grep で 0 件だった（2026-11-15・portfolio-2f）。送り先を書いた |
| 1.178 | THIRD（`ACD-1.4-THIRD-CLARITY-TRIAL.md`）/ 入口（`SUBMISSION-MATERIALS.md` の OSI の FAQ の段） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.179 | against #312（審査の 4 つの問い） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.180 | against #321（契約でないライセンスの保証の否認）/ 入口（`SUBMISSION-MATERIALS.md` §2 の先に名指す反論・`ACD-1.0.faq.md` A24） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.181 | B2（`ACD-OSI-BOTTLENECKS.md` の B2 の行・`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B2 の節）/ against #322 / 入口（`SUBMISSION-MATERIALS.md` §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.182 | against #323（理事会が却下するもの・2007 年の分類）/ 入口（`SUBMISSION-MATERIALS.md` §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.183 | against #262・#320（個人の起草者に示された順序と、法律家を最後に置くこと） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.184 | B4 と B10（`ACD-OSI-BOTTLENECKS.md` の B4・B10 の行と英語の索引）/ 入口（`REVIEWERS.md`・`SUBMISSION-MATERIALS.md` §1c と §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.185 | B2（`ACD-OSI-BOTTLENECKS.md` の B2 の行）/ against #289・#322 / 入口（`SUBMISSION-MATERIALS.md` §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.186 | against #262（弁護士は要るか）/ 入口（`SUBMISSION-MATERIALS.md` §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.187 | against #257（list の沈黙は読んだ印ではない）/ 入口（`REVISION-PROTOCOL.md` 分岐 B・`OSI-APPROVAL-PLAN.md` 3.8） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.188 | 入口（`SUBMISSION-MATERIALS.md` §2 の先に名指す反論・利用者の数は承認の理由にならない）。against には行を立てていない（使用の論点は B2 と #322 が持つ） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.189 | 入口（`SUBMISSION-MATERIALS.md` の OSD 10 条の表・ACD は利用に条件を課さない）。不利な事実ではないので against には行を立てていない | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.190 | against #321（本文を添えずに配ることへの懸念）/ 入口（`SUBMISSION-MATERIALS.md` §0 と §2・OSD 10 条の表、`ACD-1.0.faq.md` A24） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.191 | errata E79（§2.8 の第 2 文・譲受人への効力）/ against #41・#152・#324 / 入口（`SUBMISSION-MATERIALS.md` §2・`ACD-1.0.review-responses-clauses.md` §2・`ACD-1.0.jurisdictions.md` 5d） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.192 | 入口（`SUBMISSION-MATERIALS.md` §1c の新規ライセンスの基準 4 の行・法律家を入れるよう勧めた提出と、何でもしてよい式の差し戻し）。B1 と B3 の不利な面として読んだが、register には行を立てていない（法律家の不在は B1 が、短さの論点は B3 が既に持つ） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.193 | against #239・#248 / 入口（`SUBMISSION-MATERIALS.md` §2 の「出力に触れるのは曖昧さを生む」の行と §3） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.194 | 入口（`SUBMISSION-MATERIALS.md` §1c の OSD 2 の行・配られる物が source の形かは ACD を何に付けるかで決まり、重みの問いは B15 の側） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.195 | 入口（`SUBMISSION-MATERIALS.md` §1c の新規ライセンスの基準 3 と 7 の行・Randal 氏の変更を求める 2 つの場合と独自の価値、Perens 氏の「3 つだけ」を不利な面として） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.196 | 入口（`SUBMISSION-MATERIALS.md` §2 の「解釈の規則に頼る時点で負けている」の行） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.197 | 入口（`SUBMISSION-MATERIALS.md` §1c の基準 3 の行に Rosen 氏の「意図を明確に」、OSD 2 の行の逆側に Nelson 氏の承認の効き目）。moderation の先例は B14 の行が moderator の 2026-09-09 の宣言で持つので、ここからは引いていない | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.198 | 入口（`SUBMISSION-MATERIALS.md` §0d の材料の表の「新しい語と、最も近い承認済みの文」の行・委員長の逐語の再利用） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.199 | 入口（`SUBMISSION-MATERIALS.md` §1c の基準 7 の行・承認済みのライセンスが OSD の明示しないことを整えてよい、ただし挙げた例は許す側の明示） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.200 | 入口（`SUBMISSION-MATERIALS.md` §2 の「出力に触れるのは曖昧さを生む」の行・「在るなら」の形と、その逆側） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.201 | 入口（`SUBMISSION-MATERIALS.md` §1 の「使うと表明しているプロジェクト」の行の逆側・委員会の理由書は使用を基準にしない） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.202 | B13（`ACD-OSI-BOTTLENECKS.md` の B13 の行）/ 入口（`ACD-1.4-CLAUSE-REFERENCE-DRAFT.md` の §1.7 の行）。§1.7 の定義の試作は `ACD-1.4-SECOND-CLARITY-TRIAL.md` の (2) が起点にした | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.203 | THIRD（§2.6 の識別の形・T69）/ B1・B10（`ACD-OSI-BOTTLENECKS.md` の行）/ 入口（`ACD-1.4-CHANGELIST.md` の §2.6 の行） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.204 | 入口（`SUBMISSION-MATERIALS.md` §1c の OSD 10 の行・CNRI の審査での Fontana 氏と Chestek 氏の読みと、§2.3 の差は問いを 1 つ減らす差という逆側） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.205 | against #325 / B1・B10・B13（`ACD-OSI-BOTTLENECKS.md`・`ACD-OSI-BOTTLENECKS-B10.md`）/ 入口（`SUBMISSION-MATERIALS.md` §0d・`OSI-APPROVAL-PLAN.md` の段 6b・`ACD-1.0.board-decisions.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.206 | B14（`ACD-OSI-BOTTLENECKS.md` の B14 の行）/ 入口（`REVISION-PROTOCOL.md` §3.6 の 6b・`SUBMISSION-MATERIALS.md` の 0b と §0d・`ACD-1.0.submission.md` §D・`OSI-APPROVAL-PLAN.md` の段 6b） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.207 | 入口（`SUBMISSION-MATERIALS.md` §1c の新規ライセンスの基準 7 の行・§9 は既存のライセンスも及ばないだけで足りるので gap の理由に数えない） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.reviewer-positions.md` 1.49 | against #84・#104・#111 / 入口（`AS-OF.md` の Status） | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.50 | against #102 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.52 | against #1・#113・#163・#274 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.55 | B15（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B15 の節・Agent Skills は著作物でありうる） | この PR で反映先に番号を書き、grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.56 | B11（REUSE の file 単位の宣言の欠落）/ against #106 | B11 の節と #106 が同じ欠落を扱い、`REUSE.toml` を足して閉じたと書いている。番号では引かれていない（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.58 | against #107 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.59 | B8 / against #6・#84・#111 / 入口（`ACD-1.0.submission.md` B.0） | against と submission の行は文書の名を挙げて番号を引く。B8 の節は名を挙げずに「§1.59」と引くが、引いている中身（日本の同一性保持権・*"not open source, at least not in Japan"*）がこの節と一致することを読んで確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.60 | against #116・#165 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.61 | against #110・#114 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.64 | against #113 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.65 | against #114（この節は #114 を書いた経緯と、その訂正の記録で、結論は #114 の行が持つ） | #114 の行が前文と条文の食い違いを記録していることを読んで確かめた。#114 は番号で引いていない（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.140 | B1・B6 / against #291・#292 / 入口（`SUBMISSION-MATERIALS.md` §1c） | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.142 | 入口（`SUBMISSION-MATERIALS.md` §1c） | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.147 | against #309 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.155 | errata E72 / against #314 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.156 | against #315 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.157 | against #233（逆側として・OSD は特許にも及ぶという当時の標準化担当の言明） | この PR で反映先に番号を書き、grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.158 | against #313 | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.reviewer-positions.md` 1.159 | 入口（`QUESTIONS-FOR-PRACTITIONERS.md` の問い 2） | 反映先の文書が、この文書の名を挙げてこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.objection-map.md` 1.62 | 入口（この節そのものが入口の面で、審査者が当たる反論の一覧である） | `objection-map.md` が `REVIEWERS.md` から入口として引かれていることを確かめた（2026-11-15・portfolio-30） |
| `ACD-1.0.review-precedents.md` 1.45 | 入口（`SUBMISSION-MATERIALS.md` §1c の新規ライセンスの基準 7 の行・AI-MIT が受けた 3 つの反論は条件を課さない ACD では発火しない、と逆側） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.46 | against #99 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.47 | 1c（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.40・§2.2 の撤回不能の語） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.48 | against #87・#102（Modified 0BSD の却下と、Landley 氏の「権利はそれぞれ別の物」） | 反映先の行が同じ会話（日付と発言者）を引いていることを確かめた。行は節の番号を引いていない（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.51 | against #271 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.53 | 入口（`SUBMISSION-MATERIALS.md` §1c の新規ライセンスの基準 2 の行・撤回不能と自動終了の同居）/ against #114・#149（PUWL の同じ会話） | 入口はこの PR で節の番号を書き grep で確かめた。against の 2 行は同じ会話を引くが節の番号は引いていない（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.54 | against #105（AIAL v2 への Chestek 氏の「1 つの文書で 3 つのこと」） | 反映先の行が同じ会話（日付と発言者）を引いていることを確かめた。行は節の番号を引いていない（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.57 | 入口（`SUBMISSION-MATERIALS.md` §2・`ACD-1.0.submission.md` の B.0） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.63 | against #112 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.66 | なし（PSF-2.0 との比較は提出の形の完全さだけで、PSF-2.0 は数十年使われた既存の構成要素なので類型が違い、審査の論点を運ばない。提出物の項目は `ACD-1.0.submission.md` §D と `SUBMISSION-MATERIALS.md` §1 が持つ） | 反映先が無いことを、節の番号と「PSF-2.0」で grep して確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.105 | against #200・#242 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.110 | against #242 / B15（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B15 の節）/ 1c（`ACD-1.4-CLARITY-TRIAL.md` §7.4） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.115 | against #253 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.131 | against #243・#280 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.132 | against #243 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-precedents.md` 1.138 | B3・B4・B6（`ACD-OSI-BOTTLENECKS.md`・`ACD-OSI-BOTTLENECKS-EXTERNAL.md`）/ against #288 / 入口（`SUBMISSION-MATERIALS.md` §1c・`OSI-APPROVAL-PLAN.md` §2・`ACD-1.0.review-responses.md` Q2）/ 1c（`ACD-1.4-CHANGELIST.md`・`ACD-1.4-SECOND-CLARITY-TRIAL.md` §13.7） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-labels.md` 1.98 | against #157・#164 / B1（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の 2026-09-19 の節）。`ACD-1.1-SELF-AUDIT.md` §3l も引く | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-labels.md` 1.99 | against #160・#161・#164・#208 / 入口（`ACD-1.0.review-responses-meta.md` Q32c） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.67 | against #127・#186・#188 / B1・B2（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B1 + B2 の節・`ACD-OSI-BOTTLENECKS.md` の 2026-09-11 の節） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.68 | against #128 / 入口（`ACD-1.0.submission.md` の B.0） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.69 | against #128 / 入口（`REVISION-PROTOCOL.md` §1・`ACD-1.0.submission-reference.md` 4c） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.71 | 入口（`REVISION-PROTOCOL.md` の分岐 B） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.72 | against #186 / B2（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の 2026-09-13 の追記）/ 入口（`ACD-1.0.submission.md` §D） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.74 | 入口（`ACD-1.0.submission-reference.md` 4c） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.75 | against #200 / 入口（`SUBMISSION-MATERIALS.md` §1） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.77 | against #133 / 入口（`ACD-1.1-CHANGELIST.md` §0.7 の直さないと決めた errata） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.78 | against #134・#266 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.79 | against #135 / 入口（`ACD-1.0.submission-reference.md` 4c） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.80 | against #208・#214 / 入口（`SUBMISSION-MATERIALS.md` の「メールの長さと順序の目安」の節） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.83 | against #148 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.85 | B10（`ACD-OSI-BOTTLENECKS-B10.md` の (2)）。`ACD-1.1-SELF-AUDIT.md` も引く | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.87 | 入口（`PEER-REVIEW-WATCH.md` の観測の窓）。帰結の数は review-corpus 1.90 と against #149 が持つ | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-corpus.md` 1.90 | against #149 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-venue.md` 1.67 | against #117（2024-09-30 の pre-review の会話と McCoy Smith 氏の同日の返信） | 反映先の行が同じ会話（日付と発言者）を引いていることを確かめた。行は節の番号を引いていない（2026-11-15・portfolio-50） |
| `ACD-1.0.review-venue.md` 1.68 | against #149 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-venue.md` 1.69 | B7（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B7 の節） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-venue.md` 1.73 | なし（委員の謝辞が何を示さないかを節自身が書く。入口に置けば謝辞を支持と読ませることになり、沈黙を支持と読ませない線と同じ理由で置かない） | 反映先が無いことを、節の番号と謝辞の原文の語で grep して確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-venue.md` 1.89 | B10（`ACD-OSI-BOTTLENECKS-B10.md` の「測ったが、答えには使わない材料」） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-venue.md` 1.92 | なし（ドシエが返信者の立場を記録しているかの測定で、ACD への論点を持たない。抜けていた 1 人は `ACD-1.0.reviewer-positions.md` に埋めた） | `ACD-1.0.reviewer-positions.md` がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-venue.md` 1.106 | against #204 / 1c（`ACD-1.2-CHANGELIST.md` の我々宛でない議論からの採用候補） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-venue.md` 1.107 | against #206 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| `ACD-1.0.review-venue.md` 1.113 | against #248 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
