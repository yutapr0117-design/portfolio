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
| `ACD-1.0.gap-measurements.md` 1.148 | B4（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B4 の節・公有化の分野の標準の文書の欠け） | この PR で反映先に番号を書き、grep で確かめた（2026-11-16・portfolio-30） |
| `ACD-1.0.gap-measurements.md` 1.149 | B10（`ACD-OSI-BOTTLENECKS-B10.md`・明示の特許許諾と共同体への必要の説明） | この PR で反映先に番号を書き、grep で確かめた（2026-11-16・portfolio-30） |
| `ACD-1.0.gap-measurements.md` 1.150 | B10（`ACD-OSI-BOTTLENECKS-B10.md` の G1・献呈と予備の許諾の両方への特許の許可の提案） | この PR で反映先に番号を書き、grep で確かめた（2026-11-16・portfolio-30） |
| `ACD-1.0.gap-measurements.md` 1.151 | errata E69 / THIRD（`ACD-1.4-SECOND-CLARITY-TRIAL.md`）/ 入口（`OSI-APPROVAL-PLAN.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.152 | B4（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B4 の節・Unlicense の審査の基準と後ろ盾） | この PR で反映先に番号を書き、grep で確かめた（2026-11-16・portfolio-30） |
| `ACD-1.0.gap-measurements.md` 1.153 | against #311 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.154 | B1 / against #305・#312 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.160 | 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.161 | 1c（`ACD-1.4.clause-reference.md` の §8.1・§8.4 の行・本文は変えない —— §8.1 の主題の限定と §8.4 の E66 の文が、Cowan 氏 2002 の「無関係なモジュールを足して許諾を主張する」手口を既に閉じている） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-16・portfolio-1c） |
| `ACD-1.0.gap-measurements.md` 1.162 | 入口（`ACD-1.0.review-responses-meta.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| `ACD-1.0.gap-measurements.md` 1.163 | against #309 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.164 | B10（`ACD-OSI-BOTTLENECKS-B10.md` の G1 の出典の段） | PR 3263 で反映先に番号を書いたことを grep で確かめた（2026-11-16・portfolio-30） |
| 1.165 | なし（ACD は §4 と §8 で著作権と特許を同じ文書で許諾し、著作権の無いものに特許だけを許諾する場面を持たない） | 節の読みを当て直して判断した（2026-11-15・portfolio-2f） |
| 1.166 | against #316 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.167 | B2・B10・B15（`ACD-OSI-BOTTLENECKS.md`）/ against #302・#323 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.168 | B10（`ACD-1.0.board-decisions.md` の追加テストの段が出典として引く） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.169 | B15（データベース権と 1 つの道具で覆う需要）/ B14（提出者の名前・`ACD-OSI-BOTTLENECKS-POSTING.md`。2f の送り先は B6 だったが中身に合わせた） | PR 3263 で反映先に番号を書いたことを grep で確かめた（2026-11-16・portfolio-30） |
| 1.170 | 入口（`ACD-1.0.review-responses-meta.md` の SimPL の段・立証の責任は提出者にある） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.171 | against #318 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.172 | against #302・#309・#318 / 入口（`SUBMISSION-MATERIALS.md` の手順 6） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.173 | B15（`ACD-OSI-BOTTLENECKS.md`）/ 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.174 | B2（`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B2 の節・関心の表明を並べた ECL も止まった） | PR 3263 で反映先に番号を書いたことを grep で確かめた（2026-11-16・portfolio-30） |
| 1.175 | B15（`ACD-OSI-BOTTLENECKS.md`）/ 入口（`SUBMISSION-MATERIALS.md` の主題の行） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.176 | against #257 / 入口（`SUBMISSION-MATERIALS.md` の手順 7） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.177 | B10（`ACD-OSI-BOTTLENECKS-B10.md`・2005 年の「全部か良いものだけか」） | PR 3263 で反映先に番号を書いたことを grep で確かめた（2026-11-16・portfolio-30） |
| 1.178 | THIRD（`ACD-1.4-THIRD-CLARITY-TRIAL.md`）/ 入口（`SUBMISSION-MATERIALS.md` の OSI の FAQ の段） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-2f） |
| 1.179 | against #312（審査の 4 つの問い） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.180 | against #321（契約でないライセンスの保証の否認）/ 入口（`SUBMISSION-MATERIALS.md` §2 の先に名指す反論・`FAQ.md` A24） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.181 | B2（`ACD-OSI-BOTTLENECKS.md` の B2 の行・`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の B2 の節）/ against #322 / 入口（`SUBMISSION-MATERIALS.md` §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.182 | against #323（理事会が却下するもの・2007 年の分類）/ 入口（`SUBMISSION-MATERIALS.md` §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.183 | against #262・#320（個人の起草者に示された順序と、法律家を最後に置くこと） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.184 | B4 と B10（`ACD-OSI-BOTTLENECKS.md` の B4・B10 の行と英語の索引）/ 入口（`REVIEWERS.md`・`SUBMISSION-MATERIALS.md` §1c と §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.185 | B2（`ACD-OSI-BOTTLENECKS.md` の B2 の行）/ against #289・#322 / 入口（`SUBMISSION-MATERIALS.md` §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.186 | against #262（弁護士は要るか）/ 入口（`SUBMISSION-MATERIALS.md` §2） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.187 | against #257（list の沈黙は読んだ印ではない）/ 入口（`REVISION-PROTOCOL.md` 分岐 B・`OSI-APPROVAL-PLAN.md` 3.8） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.188 | 入口（`SUBMISSION-MATERIALS.md` §2 の先に名指す反論・利用者の数は承認の理由にならない）。against には行を立てていない（使用の論点は B2 と #322 が持つ） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.189 | 入口（`SUBMISSION-MATERIALS.md` の OSD 10 条の表・ACD は利用に条件を課さない）。不利な事実ではないので against には行を立てていない | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
| 1.190 | against #321（本文を添えずに配ることへの懸念）/ 入口（`SUBMISSION-MATERIALS.md` §0 と §2・OSD 10 条の表、`FAQ.md` A24） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-30） |
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
| 1.202 | B13（`ACD-OSI-BOTTLENECKS.md` の B13 の行）/ 入口（`ACD-1.4.clause-reference.md` の §1.7 の行）。§1.7 の定義の試作は `ACD-1.4-SECOND-CLARITY-TRIAL.md` の (2) が起点にした | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.203 | THIRD（§2.6 の識別の形・T69）/ B1・B10（`ACD-OSI-BOTTLENECKS.md` の行）/ 入口（`ACD-1.4-CHANGELIST.md` の §2.6 の行） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.204 | 入口（`SUBMISSION-MATERIALS.md` §1c の OSD 10 の行・CNRI の審査での Fontana 氏と Chestek 氏の読みと、§2.3 の差は問いを 1 つ減らす差という逆側） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.205 | against #325 / B1・B10・B13（`ACD-OSI-BOTTLENECKS.md`・`ACD-OSI-BOTTLENECKS-B10.md`）/ 入口（`SUBMISSION-MATERIALS.md` §0d・`OSI-APPROVAL-PLAN.md` の段 6b・`ACD-1.0.board-decisions.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.206 | B14（`ACD-OSI-BOTTLENECKS.md` の B14 の行）/ 入口（`REVISION-PROTOCOL.md` §3.6 の 6b・`SUBMISSION-MATERIALS.md` の 0b と §0d・`ACD-1.0.submission.md` §D・`OSI-APPROVAL-PLAN.md` の段 6b） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-15・portfolio-50） |
| 1.207 | 入口（`SUBMISSION-MATERIALS.md` §1c の新規ライセンスの基準 7 の行・§9 は既存のライセンスも及ばないだけで足りるので gap の理由に数えない） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-15・portfolio-50） |
| 1.208 | 1c（`ACD-1.4.clause-reference.md` の §4.1・§8.1 の行・`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.38 の sublicensable）/ 入口（`REVISION-PROTOCOL.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.209 | 1c（`ACD-1.4-THIRD-CLARITY-TRIAL.md` の冒頭の規則 (4)・明晰さの試作の根拠）/ B1・B3・B10・B13（同じ節の読みが register の各項目の材料） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-16・portfolio-1c） |
| 1.210 | B1 / B14 / B2（`ACD-OSI-BOTTLENECKS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.211 | 1c（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.39 の §1.3）/ B10 / B15（`ACD-OSI-BOTTLENECKS.md`）/ against #46 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.212 | B1 / B10 / B11 / B13 / B14 / B2 / B3（`ACD-OSI-BOTTLENECKS.md`）/ 入口（`ACD-1.0.review-responses-clauses.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.213 | 1c（`ACD-1.4.clause-reference.md` の §8.1 の行・Piana 氏 2012 の滑りやすい坂）/ B4（Rosen 氏の放棄の効果） | この PR で反映先にこの節の番号を書き、grep で確かめた（2026-11-16・portfolio-1c） |
| 1.214 | B1 / B14 / B2 / B3 / B4（`ACD-OSI-BOTTLENECKS.md`）/ against #270 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.215 | 1c（`ACD-1.4.clause-reference.md` の §2.6 の行・`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.43） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.216 | 1c（`ACD-1.4.clause-reference.md` の §10.2 の行・`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.43）/ against #326 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.217 | B10 / B2（`ACD-OSI-BOTTLENECKS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.218 | 1c（`ACD-1.4-CHANGELIST.md` の §12.2 の行・`ACD-1.4.clause-reference.md` の §12.2 の行・`ACD-1.4-THIRD-CLARITY-TRIAL.md` §15.1・T67）/ 入口（`README.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.219 | 1c（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.44・T66）/ against #327 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.220 | 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.221 | B1 / B14（`ACD-OSI-BOTTLENECKS.md`）/ 入口（`REVISION-PROTOCOL.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
| 1.222 | B2（`ACD-OSI-BOTTLENECKS-EXTERNAL.md`）/ 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-1c） |
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
| 1.70 | 1c（`ACD-1.4-CLARITY-TRIAL.md`） / B10 / against #129 / against #130 / against #132 / against #145 / errata E18 / 入口（`OSI-APPROVAL-PLAN.md`・`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against.md:391・ACD-1.0.against.md:392・ACD-1.0.against.md:394・ACD-1.0.against.md:407） |
| 1.76 | 入口（`OSI-APPROVAL-PLAN.md`・`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.review-rules.md:214・ACD-1.0.review-rules.md:8・OSI-APPROVAL-PLAN.md:125・README.md:39） |
| 1.81 | against #137 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against.md:399・ACD-1.0.review-rules.md:8・README.md:39） |
| 1.82 | against #146 / against #148 / against #183 / 入口（`REVISION-PROTOCOL.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against.md:408・ACD-1.0.against.md:410・ACD-1.0.against.md:445・ACD-1.0.board-decisions.md:143） |
| 1.86 | against #137（Code of Conduct を 1 項ずつ当てた —— 同じ論点） | 節の本文が名指す against #137 の行が同じ Code of Conduct の論点を持つことを読んで確かめた（行はこの節の番号を引いていない・2026-11-16・portfolio-9b） |
| 1.102 | against #84 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against.md:366・ACD-1.0.board-decisions.md:36・ACD-1.0.board-decisions.md:582・ACD-1.0.board-decisions.md:714） |
| 1.103 | B14 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.gap-measurements.md:181・ACD-1.0.review-corpus.md:30・ACD-OSI-BOTTLENECKS-POSTING.md:50・PEER-REVIEW-WATCH.md:606） |
| 1.124 | against #267 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:62・ACD-1.0.submission-reference.md:732・PEER-REVIEW-WATCH.md:593・SUBMISSION-MATERIALS.md:113） |
| 1.141 | B1 / against #297 / 入口（`OSI-APPROVAL-PLAN.md`・`REVIEWERS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:92・ACD-1.0.reviewer-positions.md:678・ACD-1.0.reviewer-positions.md:799・ACD-OSI-BOTTLENECKS-EXTERNAL.md:288） |
| 1.84 | against #147 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against.md:409・ACD-1.0.review-doctrine.md:17・ACD-1.1-CHANGELIST.md:754・BLIND-SPOTS.md:593） |
| 1.100 | against #179 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against.md:441・ACD-1.0.review-doctrine.md:17・BLIND-SPOTS-LOG.md:136・BLIND-SPOTS-LOG.md:172） |
| 1.101 | B10（`ACD-OSI-BOTTLENECKS-B10.md` の H3 —— 許諾は TDM の例外とは別の経路で効く） | 節の本文（学習のための複製が侵害か・TDM 例外の名指し）と B10 の H3 の行が同じ論点を持つことを読んで確かめた（行はこの節の番号を引いていない・2026-11-16・portfolio-9b） |
| 1.109 | against #238（特許の 3 段 —— 提出者側の弁護士 2006 を 5 人目に数える） | 節の本文が名指す against #238 の行が同じ 2006 年の 2 スレッド（Rivard 氏・Rosen 氏）を引くことを読んで確かめた（行はこの節の番号を引いていない・2026-11-16・portfolio-9b） |
| 1.111 | against #244 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:39・ACD-1.0.review-doctrine.md:385） |
| 1.112 | against #246 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:41・ACD-1.0.submission.md:268・SUBMISSION-MATERIALS.md:119） |
| 1.114 | against #251 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:46） |
| 1.117 | against #256 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:51） |
| 1.123 | against #265 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:60・ACD-1.0.objection-map.md:52・ACD-1.0.review-responses-clauses.md:682・ACD-1.2-CHANGELIST.md:41） |
| 1.125 | B15 / against #266 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:61・ACD-1.0.objection-map.md:56・ACD-OSI-BOTTLENECKS-EXTERNAL.md:554・PEER-REVIEW-WATCH.md:593） |
| 1.127 | against #268 / against #269 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:63・ACD-1.0.against-2.md:64・SUBMISSION-MATERIALS.md:140） |
| 1.128 | against #270 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:65・ACD-1.0.submission-reference.md:733） |
| 1.88 | against #148 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against.md:410・ACD-1.0.comparison.md:114・ACD-1.0.review-doctrine.md:26・ACD-1.0.review-outcomes.md:21） |
| 1.108 | against #237（理事会が実際に不承認にした審査の理由は主題だった）/ B15 | 節の本文が名指す against #237 の行が同じ MulanOWL の不承認を記録していることを読んで確かめた（行はこの節の番号を引いていない・2026-11-16・portfolio-9b） |
| 1.116 | against #254 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:49・ACD-1.0.review-outcomes.md:21・ACD-1.0.review-outcomes.md:349・ACD-1.0.review-outcomes.md:557） |
| 1.118 | against #257 / against #258 / against #317 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:112・ACD-1.0.against-2.md:52・ACD-1.0.against-2.md:53・ACD-1.0.review-outcomes.md:21） |
| 1.119 | against #259 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:54） |
| 1.120 | against #261 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:56・ACD-1.0.review-outcomes.md:497） |
| 1.121 | against #263 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:58） |
| 1.122 | against #264 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:59・ACD-1.0.review-outcomes.md:568） |
| 1.126 | against #264 / against #268 / 入口（`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:59・ACD-1.0.against-2.md:63・SUBMISSION-MATERIALS.md:230） |
| 1.223 | B15 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-OSI-BOTTLENECKS-B10.md:156） |
| 1.224 | B15 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-OSI-BOTTLENECKS-B10.md:160） |
| 1.225 | B3 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-OSI-BOTTLENECKS-EXTERNAL.md:491） |
| 1.226 | 1c（`ACD-1.4.clause-reference.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.4.clause-reference.md:218・ACD-1.4.clause-reference.md:219） |
| 1.227 | 1c（`ACD-1.4.clause-reference.md`・`ACD-1.4-THIRD-CLARITY-TRIAL.md`） / B1 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.4.clause-reference.md:61・ACD-1.4-THIRD-CLARITY-TRIAL.md:43・ACD-OSI-BOTTLENECKS-EXTERNAL.md:300） |
| 1.228 | B1 / B2 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-OSI-BOTTLENECKS-EXTERNAL.md:324・ACD-OSI-BOTTLENECKS.md:392） |
| 1.229 | B10 / against #328 / 入口（`OSI-APPROVAL-PLAN.md`・`SUBMISSION-MATERIALS.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:123・ACD-1.0.submission-osd.md:258・ACD-OSI-BOTTLENECKS-B10.md:136・OSI-APPROVAL-PLAN.md:157） |
| 1.230 | 入口（`REVISION-PROTOCOL.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・REVISION-PROTOCOL.md:406） |
| 1.231 | B11 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-OSI-BOTTLENECKS-EXTERNAL.md:227） |
| 1.232 | 1c（`ACD-1.4.clause-reference.md`） / against #286 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:81・ACD-1.4.clause-reference.md:58） |
| 1.233 | B2 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-OSI-BOTTLENECKS-EXTERNAL.md:326） |
| 1.234 | B1 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-OSI-BOTTLENECKS-EXTERNAL.md:296） |
| 1.235 | B6 / against #328 / 入口（`OSI-APPROVAL-PLAN.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:123・ACD-1.0.submission-osd.md:297・ACD-OSI-BOTTLENECKS.md:221・OSI-APPROVAL-PLAN.md:157） |
| 1.236 | B10 / B12 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-OSI-BOTTLENECKS.md:537） |
| 1.237 | B2 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-OSI-BOTTLENECKS-EXTERNAL.md:324） |
| 1.238 | 1c（`ACD-1.4-THIRD-CLARITY-TRIAL.md`） / B15 / B6 / 入口（`REVISION-PROTOCOL.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.4-THIRD-CLARITY-TRIAL.md:19・ACD-OSI-BOTTLENECKS-B10.md:138・ACD-OSI-BOTTLENECKS.md:224・REVISION-PROTOCOL.md:426） |
| 1.239 | 1c（`ACD-1.4.clause-reference.md`） / B1 / B2 / B6 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.4.clause-reference.md:218・ACD-OSI-BOTTLENECKS-EXTERNAL.md:298・ACD-OSI-BOTTLENECKS-EXTERNAL.md:328・ACD-OSI-BOTTLENECKS.md:224） |
| 1.240 | against #320 | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.0.against-2.md:115） |
| 1.241 | 1c（`ACD-1.4-THIRD-CLARITY-TRIAL.md`） / 入口（`REVISION-PROTOCOL.md`） | 反映先の文書がこの節の番号を引いていることを grep で確かめた（2026-11-16・portfolio-9b・ACD-1.4-THIRD-CLARITY-TRIAL.md:92・REVISION-PROTOCOL.md:279） |
