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

**書き方。** 1 節に 1 行。番号のセルは「1.179」と書き、§ を付けない（まだ在らない節を § で引くと Check 471 (e) が RED になるため）。反映のセルは Check 501 と同じ語彙（B# / against #N / errata E# / 1c / THIRD / 入口 / なし（理由） / 未定）で書く。確かめ方のセルには、その反映先が本当にその節を引いているかをどう確かめたかを書く。同じ節に、末尾の欄とこの表の行の両方を置かない（Check 501 が RED にする）。帯の分け方は 9b が数えた（2f 1.164〜1.178・30 1.179〜1.191・50 1.192〜1.207・1c 1.208〜1.222・9b 1.223〜1.241）。

| 節 | 反映 | 確かめ方 |
| :-- | :-- | :-- |
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
