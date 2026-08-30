---
file: LICENSES/README.md
audience: 誰でも（ここが入口）
last-updated: 2026-08-27
canonical-ref: LICENSES/ACD-1.0.txt (本文・唯一の権威) / LICENSES/FROZEN.md (凍結と投稿先の単一ソース)
---

# LICENSES/ — 何がどこにあるか

このディレクトリには **Autonomous Commons Dedication 1.0 (ACD-1.0)** の本文と、その周辺文書が
置いてある。**目的は「疑問がこのリポジトリを見れば潰せる」ことである。**

**権威は `ACD-1.0.txt` だけ**である。他はすべて非規範で、齟齬があれば本文が勝つ。

---

## 1. 目的別に、どれを読むか

| 知りたいこと | 見る場所 |
|---|---|
| **条文そのもの** | [`ACD-1.0.txt`](ACD-1.0.txt) |
| この条項は何のためにあるのか（**全 82 条**） | [`ACD-1.0.clause-reference.md`](ACD-1.0.clause-reference.md) |
| 「既存の X で足りるのでは」 | [`ACD-1.0.comparison.md`](ACD-1.0.comparison.md) |
| 「うちの国では効かないのでは」 | [`ACD-1.0.jurisdictions.md`](ACD-1.0.jurisdictions.md) |
| **使ってよいか / どう使うか / 法務に何を見せるか** | [`ACD-1.0.faq.md`](ACD-1.0.faq.md) |
| レビューで来るであろう指摘への回答（総論・OSD・認める弱点） | [`ACD-1.0.review-responses.md`](ACD-1.0.review-responses.md) |
| 同・条項別 | [`ACD-1.0.review-responses-clauses.md`](ACD-1.0.review-responses-clauses.md) |
| 同・起草の出自 / 名称 / 運用（**LLM 起草の扱い・撤回条件**） | [`ACD-1.0.review-responses-meta.md`](ACD-1.0.review-responses-meta.md) |
| **実際に来た指摘**とその答え | [`ACD-1.0.discussion-log.md`](ACD-1.0.discussion-log.md) |
| **審査者が最初に読む英語の入口**（license-discuss から来た人向け） | [`REVIEWERS.md`](REVIEWERS.md) |
| **不利な事実の網羅（先に読ませる用・英語）** | [`ACD-1.0.against.md`](ACD-1.0.against.md) |
| **既知の欠陥と、直さない理由（英語）** | [`ACD-1.0.errata.md`](ACD-1.0.errata.md) |
| 提出用の英文一式（**送るだけ**） | [`ACD-1.0.submission.md`](ACD-1.0.submission.md) |
| 提出judgment と**残る弱点** | [`READY-TO-SUBMIT.md`](READY-TO-SUBMIT.md) |
| **いまどの段階か / 凍結の状態** | [`FROZEN.md`](FROZEN.md) |
| 機械可読な記述子 | [`ACD-1.0.machine.json`](ACD-1.0.machine.json) / [`ACD-1.0.spdx.xml`](ACD-1.0.spdx.xml) |

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
