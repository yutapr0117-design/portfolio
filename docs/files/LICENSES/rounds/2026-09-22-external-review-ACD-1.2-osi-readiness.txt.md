---
file: LICENSES/rounds/2026-09-22-external-review-ACD-1.2-osi-readiness.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-22
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #207 / LICENSES/ACD-1.2-CHANGELIST.md
---

# LICENSES/rounds/2026-09-22-external-review-ACD-1.2-osi-readiness.txt

## What

**オーナーが別の AI に `ACD-1.2-DRAFT.txt` を読ませた結果を、そのまま渡してきたもの**
（2026-09-22 受領）。**我々が依頼したものではない。**

**受領時に最初に測ったのは、それが何を読んだかである** ——渡されたレビュー対象
`ACD-1.2-DRAFT_1.txt` は、受領時点の `LICENSES/ACD-1.2-DRAFT.txt` と
**sha256 が完全に一致した**（`1356b2b01396be4f4ff871bcc073599aee164cc39ffbb7684c499d326cc59c72`）。
**したがってこの評は現行の byte そのものに当たっており、「渡した時点の版」と
「いまの版」を読み分ける必要は無かった。** 2026-09-20 の 3 件（PDF 抽出・
`against.md` #167 の破損ヘッダを含む版）とはこの点が違う。

## Why

**1 件が確定した実欠陥だったから**（`against.md` #207）。冒頭の status block が
*"It is at present identical to ACD-1.1 apart from the version number and the identifiers
that name it"* と述べたまま、**すぐ下に 9 件（E22〜E30）が並んでいた。**
`git log -S` で測ると **2026-09-18 から 4 日間**偽であり、**同じ draft を読んだ
2026-09-20 の 3 件はこれを報告していない。**

**⚠ 残りは採らなかった、その理由ごと記録してある。** 5 条の指摘のうち
**§6.2 / §6.3 は、勧める分離が既に本文にほぼ逐語で在る。** §2.6 / §16.2 / §8.4 の
懸念は実在するが答えは §2.7 で、**その 3 条だけが §2.7 を引いていない。**
**ただし §6.2 / §6.3 は §2.7 を二度引いてなお矛盾に見えると報告された** ——
「相互参照を足す」という処方に、同じ文書内の反証がある。

## How

オーナーからローカル共有。**Markdown だったが本文は 1 バイトも変えていない**
（規約 1）。先頭に受領ヘッダを足し、`----- begin verbatim -----` で境界を示した（規約 3）。

## Constraints

- **無改変で保存する。** このディレクトリで byte を変えることは規約違反である。
- **分析は書かない**（規約 2）。読みと採否は `against.md` #207 と
  `ACD-1.2-CHANGELIST.md` にある。
- **OSI の審査者の発言ではない。** 提出物の中でリストの反応として引いてはならない。
- **末尾に「OSI 提出文の叩き台」が含まれるが、これは採用していない** ——
  投稿は register **B14** の下で止まっており、**AI はリストへ送る文面を完成品として
  作らない。**

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫も同じ commit で
  （**Check 465** が実 file から導出して照合する）。
- 引用を他の文書へ運ぶときは、**この file の逐語と照合してから書く。**

## Audience-specific notes

- **AI（実装者）**: **出自は提示と重み付けにのみ効く。** AI の評だからといって
  軽く扱わず、権威としても扱わない ——**1 件ずつ現物に当てた結果がここにある。**
- **監査人**: 対象版の sha256 が冒頭に書いてある。`LICENSES/ACD-1.2-DRAFT.txt` の
  当該 commit と突き合わせれば、何を読んだ評かが再現できる。
- **第三者**: **不利な指摘も、外した指摘も、同じ場所に残してある。**
