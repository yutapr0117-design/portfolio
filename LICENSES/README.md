---
file: LICENSES/README.md
audience: 誰でも（ここが入口）
last-updated: 2026-09-24
canonical-ref: LICENSES/ACD-1.0.txt (このリポジトリに適用している本文) / LICENSES/FROZEN.md (凍結と投稿先の単一ソース)
---

# LICENSES/ — 何がどこにあるか

> **発信の状態はここに書かない** —— 単一ソースは `FROZEN.md` の `POSTING-STATUS` marker である（状態を写した面は再開後も「停止」と言い続けた・`ACD-1.0.against.md` #195 / #221）。経緯だけを日付つきで置く: 2026-09-09 に OSI Moderators の通知を受けて停止し（#119 / `ACD-OSI-BOTTLENECKS.md` **B14**・逐語は `rounds/`）、2026-09-17 に再開した。**再開後にオーナーが `license-discuss` へ送った 1 通は moderation で拒否されている**（#215）。


> **Reviewing ACD-1.0 and cannot read Japanese?** Start at
> **[`REVIEWERS.md`](REVIEWERS.md)** — it is in English, states the submission status, says which
> documents are already in English, and gives the commands to verify every claim made here.
> The authoritative text is [`ACD-1.0.txt`](ACD-1.0.txt); the case against approving it is
> [`ACD-1.0.against.md`](ACD-1.0.against.md), written by us.

このディレクトリには **Autonomous Commons Dedication 1.0 (ACD-1.0)** の本文と、その周辺文書が
置いてある。**目的は「疑問がこのリポジトリを見れば潰せる」ことである。**

**このリポジトリに適用されている本文は `ACD-1.0.txt` だけ**である。`ACD-1.1.txt` は 1.1 という別識別子の本文として権威を持つが、このリポジトリには適用していない。それ以外はすべて非規範で、齟齬があれば各版の本文が勝つ。

---

## 1. 目的別に、どれを読むか

| 知りたいこと | 見る場所 |
|---|---|
| **条文そのもの** | [`ACD-1.0.txt`](ACD-1.0.txt) |
| この条項は何のためにあるのか（**全 82 条**） | [`ACD-1.0.clause-reference.md`](ACD-1.0.clause-reference.md) |
| 「既存の X で足りるのでは」 | [`ACD-1.0.comparison.md`](ACD-1.0.comparison.md) |
| 「この提出は実際に何を言われるのか」 | [`ACD-1.0.review-precedents.md`](ACD-1.0.review-precedents.md) —— **個別スレッドを読んで**得た、当たる指摘と当たらない指摘（§1.45〜§1.66）|
| 「アーカイブ全体では何が起きているのか」 | [`ACD-1.0.review-corpus.md`](ACD-1.0.review-corpus.md) —— **アーカイブを全部取得して測った**こと（承認の基準 8 条 / 委員会が述べた規則 / 決議の分布 / 提出から決定までの所要 / 手続きの実態・§1.67〜）。**前者は読み、後者は測定である** |
| 「OSI が**公表している規則**は何と書いてあるのか」 | [`ACD-1.0.review-rules.md`](ACD-1.0.review-rules.md) —— **公表ページを原典で読んだ**記録（承認基準 8 条 / 提出の要件リスト / Code of Conduct の逐条 / 本文を変えたい提出者への手続き・§1.70 / §1.76 / §1.81 / §1.82 / §1.86）。**公表ページは規則を、リストは議論を、理事会は決定を残す** ——資料の種類で分けてある |
| 「**理事会は実際に何を決めたのか**」 | [`ACD-1.0.board-decisions.md`](ACD-1.0.board-decisions.md) —— **公開議事録という別の一次資料**から読める決定（承認 8・否決 9・取り下げ 2／公開 12 回の範囲）。**最も重いのは、公表されていない第 3 の帰結** ——*reject* ではなく *"not approved … if it is **duplicative and not used by a project**"*。**リストは議論を、理事会は決定を残す** |
| 「うちの国では効かないのでは」 | [`ACD-1.0.jurisdictions.md`](ACD-1.0.jurisdictions.md) |
| **使ってよいか / どう使うか / 法務に何を見せるか** | [`ACD-1.0.faq.md`](ACD-1.0.faq.md) |
| レビューで来るであろう指摘への回答（総論・OSD・認める弱点） | [`ACD-1.0.review-responses.md`](ACD-1.0.review-responses.md) |
| 同・条項別 | [`ACD-1.0.review-responses-clauses.md`](ACD-1.0.review-responses-clauses.md) |
| 同・定型条項と解釈条項への攻撃（Q22〜Q33）| [`ACD-1.0.review-responses-boilerplate.md`](ACD-1.0.review-responses-boilerplate.md) |
| 同・起草の出自 / 名称 / 運用（**LLM 起草の扱い・撤回条件**） | [`ACD-1.0.review-responses-meta.md`](ACD-1.0.review-responses-meta.md) |
| **実際に来た指摘**とその答え | [`ACD-1.0.discussion-log.md`](ACD-1.0.discussion-log.md) |
| **審査者が最初に読む英語の入口**（license-discuss から来た人向け） | [`REVIEWERS.md`](REVIEWERS.md) |
| **受け取った議論の原文**（無改変で置く場所・一覧と件数は `rounds/README.md` が実 file から導出して持つ） | [`rounds/`](rounds/README.md) |
| **疑問から引く索引（審査者向け・英語）** | [`QUESTION-INDEX.md`](QUESTION-INDEX.md) |
| **不利な事実の網羅（先に読ませる用・英語）** | [`ACD-1.0.against.md`](ACD-1.0.against.md) |
| **既知の欠陥と、直さない理由（英語）** | [`ACD-1.0.errata.md`](ACD-1.0.errata.md) |
| **1.1 で何を変えたか（1.0 → 1.1 の記録）** | [`ACD-1.1-CHANGELIST.md`](ACD-1.1-CHANGELIST.md) |
| **1.0 の後継として確定したテキスト（2026-09-17 凍結）** | [`ACD-1.1.txt`](ACD-1.1.txt) —— 1 行目は **FROZEN TEXT. NOT SUBMITTED FOR APPROVAL. NOT APPLIED TO THIS REPOSITORY.**（草案ではない）。オーナーが同日 `license-discuss` へ送った 1 通は moderation で拒否されており（`ACD-1.0.against.md` #215）、**リストはまだこのテキストを受け取っていない**。閉じた欠陥の数は 1.1 自身の冒頭が述べる（凍結時点の数）。**条番号は §1 の定義（§1.2〜§1.4 / §1.6）と §15・§16 で 1.0 と異なる**ので、**1.0 を引くときは 1.0 の本文から**（定義語による対応は `REVIEWERS.md`「Which text you are looking at」）|
| **その機械可読記述子** | [`ACD-1.1.machine.json`](ACD-1.1.machine.json) |
| **次版の草案（作業場）** | [`ACD-1.2-DRAFT.txt`](ACD-1.2-DRAFT.txt) |
| **次版に反映するものの集約点（1.2）** | [`ACD-1.2-CHANGELIST.md`](ACD-1.2-CHANGELIST.md) |
| **93 か月の掘削と仮説の検定** | [`ACD-1.0.dig-2026-09.md`](ACD-1.0.dig-2026-09.md) |
| **草案を我々自身が掃引して出たもの** | [`ACD-1.1-SELF-AUDIT.md`](ACD-1.1-SELF-AUDIT.md) |
| **改訂サイクルの手順（長期戦の骨格）** | [`REVISION-PROTOCOL.md`](REVISION-PROTOCOL.md) |
| **盲点の探し方（どの次元をまだ測っていないか）** | [`BLIND-SPOTS.md`](BLIND-SPOTS.md) |
| **その適用の日次ログ（いつ何を使い、何が出たか）** | [`BLIND-SPOTS-LOG.md`](BLIND-SPOTS-LOG.md) |
| **同時代 instrument の経過観察（OpenMDW / ModelGo）** | [`PEER-REVIEW-WATCH.md`](PEER-REVIEW-WATCH.md) |
| 提出用の英文一式（**送るだけ**） | [`ACD-1.0.submission.md`](ACD-1.0.submission.md) |
| 提出文の背後にある参考資料（**貼らない**・§1〜§5） | [`ACD-1.0.submission-reference.md`](ACD-1.0.submission-reference.md) |
| **承認阻害ボトルネックの一覧（canonical）** | [`ACD-OSI-BOTTLENECKS.md`](ACD-OSI-BOTTLENECKS.md) |
| 「**外の答えを待っている項目は何か**」 | [`ACD-OSI-BOTTLENECKS-EXTERNAL.md`](ACD-OSI-BOTTLENECKS-EXTERNAL.md) —— 我々の作業では動かせない 7 項目の深い分析（法的レビュー / 実使用 / §4.4 の外部回答待ち / 特許射程 / gap / SPDX / AI 起草の扱い）。**索引と集計は上の register が canonical** |
| 既知の反論が当たるか（**1 表・審査者が最初に読む**） | [`ACD-1.0.objection-map.md`](ACD-1.0.objection-map.md) |
| 審査者は主題について何と言っているか（人格権 / 特許 / 長さ / 構造 …） | [`ACD-1.0.reviewer-positions.md`](ACD-1.0.reviewer-positions.md) |
| リストが我々の類型に付ける呼び名（「クレヨン」「vanity」）と、それが実際に指している害 | [`ACD-1.0.review-labels.md`](ACD-1.0.review-labels.md) |
| 提出判断と**残る弱点** | [`READY-TO-SUBMIT.md`](READY-TO-SUBMIT.md) |
| **いまどの段階か / 凍結の状態** | [`FROZEN.md`](FROZEN.md) |
| **古くなりうる事実と、最後に確かめた日（英語）** | [`AS-OF.md`](AS-OF.md) |
| 機械可読な記述子 | [`ACD-1.0.machine.json`](ACD-1.0.machine.json) / [`ACD-1.0.spdx.xml`](ACD-1.0.spdx.xml) |
| 「**その記述は、本当に確かめられたのか**」 | [`AUDIT-LEDGER.md`](AUDIT-LEDGER.md) —— **ドシエ自身への敵対的検証の台帳**。主張を種類（逐語引用 / 件数 / 不在の主張 / 条項の挙動…）に分け、種類ごとに母数・確認済み・道具を持つ。**進捗は宣言せず道具から導出する** |
| 「**機械可読な面（記述子・spdx.xml・LICENSE・REUSE.toml・manifest）が述べていることは、いま真か**」 | [`MACHINE-SURFACES-AUDIT.md`](MACHINE-SURFACES-AUDIT.md) —— 2026-09-24 の検証報告。**欠陥は直さず候補として列挙**してある |

設計根拠と申請ドシエは、このディレクトリの外にある
—— [`docs/architecture/acd-license-rationale.md`](../docs/architecture/acd-license-rationale.md)。

---

## 2. 立場別の読み順

### 使うかどうか決めたい人

1. [`ACD-1.0.faq.md`](ACD-1.0.faq.md) の A 節（**「使わないほうがよい」場合もそう書いてある**）
2. [`ACD-1.0.comparison.md`](ACD-1.0.comparison.md) §6 の 3 つの判断基準
3. 気になった条項だけ [`ACD-1.0.clause-reference.md`](ACD-1.0.clause-reference.md) で引く

### レビューする人 / 批判したい人

1. [`ACD-1.0.txt`](ACD-1.0.txt)（**これが権威**）
2. [`ACD-1.0.review-responses.md`](ACD-1.0.review-responses.md) §4「認める項目」——
   **弱点は先に自分から出してある**
3. [`READY-TO-SUBMIT.md`](READY-TO-SUBMIT.md)「残る弱点」
4. 反論したい条項を [`ACD-1.0.review-responses-clauses.md`](ACD-1.0.review-responses-clauses.md) で確認

### 監査する人

1. [`FROZEN.md`](FROZEN.md)（凍結対象の sha256・**Check 453 が機械強制**）
2. [`READY-TO-SUBMIT.md`](READY-TO-SUBMIT.md)（何をもって「達した」としたか）
3. 各文書の「扱っていないもの」「限界」の節 —— **抜けではなく判断であることを示してある**

---

## 3. いまの状態

**`FROZEN.md` の `VENUE-DATA` marker が投稿先の単一ソース**である（Check 458 が
複数ファイルとの整合を BLOCKING で強制する）。**ここには状態を直書きしない** ——
書けば必ず drift するからである（実際、2026-08-26 の 1 日で venue の記録が 2 度 drift した）。

**本文は凍結中**であり、妥当な批判への正しい返答は「**ACD-1.1 でこうする**」であって、
審査中のテキスト差し替えではない。

---

## 4. この索引自体について

**ここに載っていない `LICENSES/*.md` があってはならない。** 到達できない文書は無いのと同じ
だからである。これは **Check 459 が BLOCKING で機械強制**しており、新しい文書を足して
索引に載せ忘れると CI が止まる。

**逆に、ここに載っているのに答えが無い疑問が出たら、それは文書側の欠落である。**
その場合は該当文書へ追記し、必要ならこの表にも行を足すこと。
