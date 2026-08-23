---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-rfc-conformance-and-approval-gate-sweep.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: AI2AI.md (Session Record #34) / CLAUDE.md §7 / .well-known/api-catalog / LICENSES/ACD-1.0.txt / .github/scripts/rotate_mutation_samples.py
---

# improvement-notes — RFC 適合 / 承認ゲートの掃討 / ライセンスの内部接続

## What

2026-08-23 の run（PR #1281〜#1284）の増分記録。レンズを 3 つ回した ——「**外部仕様に照らして
実際に何を意味しているか**」「**canon を直しても下流は自動では直らない**」「**自分が作った
道具は本当にその仕事をするか**」。実バグ 4 系統と新規 BLOCKING Check 2 本（449 / 450）、
既存 Check 436 の 3 つの穴の是正、ACD-1.0 の実質的欠陥の是正を記録する。

## Why

このリポジトリの増分は「discover → document → systematize → verify → deliver」で回る。
improvement-notes は **document 段**の成果物で、**次の AI が同じ穴を掘り直さないため**の
一次資料になる。とくに本 run は「**測定系を疑う**」が 4 回とも当たった run で、
*誤報の手前で止まった経緯*そのものに再利用価値がある（誤った測定は「エラー」ではなく
「それらしい数字」として出る）。

## How

本文は増分ごとに「何が壊れていたか / なぜどの層も検出しなかったか / どう構造封じしたか」の
3 点セットで書く。末尾に **実測して honest clean と確認した面**（再監査不要）と **教訓**を置く。
数値の権威は `docs/architecture/total-check-runbook.md` §9 で、本書には書かない。

## Constraints

- **Check 75**: `docs/incident-artifacts/README.md` の inventory に列挙されていること
- **Check 108**: 本 mirror doc が 1 対 1 で存在すること
- **Check 65**: `last-updated` が実態と整合すること
- **Check 436 の対象外**: 歴史記録なので「裁可待ち」型の記述に超越注記を強制しない
  （履歴を濁さないための線引き）
- **Check 450**: 非日本語スクリプトを混入させない

## Change impact

- 本書を追加/改名 → README inventory（Check 75）+ mirror（Check 108）+ `last-updated`（Check 65）
- 記載した Check 番号や総数が変わったら **runbook §9 が権威**（本書は追随しない）

## Audience-specific notes

### For AI agents

- **仕様は要約でなく原文で読め** —— 本 run の最大の発見（`item` と `api-catalog` の違い）は
  要約では潰れる粒度だった。
- **ゲートを作ったら、そのゲートが動機となった実例を捕捉できるか確かめよ** —— Check 436 の
  scope 拡張は、実際に測るまで届いていなかった。
- **per-instance で潰した class は綴りや射程を変えて再発する** —— mirror doc を手で 9 枚
  掃引して 4 枚残した実測が、構造封じへ昇華する判断の根拠。

### For 監査人

- 4 系統すべてについて**非 vacuity を実測**しており、各 Check は破壊テストで RED を確認済み。
  Check 449 は 3 部が独立に発火することまで測っている（overclaim なし）。
- **「Check を作らない」判断**も 2 件記録している（JSON-LD 語彙はオフラインで権威検証できず、
  相互参照の意味一致は機械検証できない）。作れなかったのではなく、brittle になるので作らない。

### For 学術研究者 / 第三者

- RFC 9727 / 9264 / 6573、sitemaps.org 0.9、RFC 9309 といった**外部仕様への適合を CI で
  機械強制する**実例と、その過程で**自分の測定系が 4 回誤った**記録が並んでいる。
- 独自ライセンス ACD-1.0 の条文レベルの欠陥（機械学習許諾と特許許諾が接続していない）を
  発見・是正した経緯は、`docs/architecture/acd-license-rationale.md` §5 に設計判断として残る。
