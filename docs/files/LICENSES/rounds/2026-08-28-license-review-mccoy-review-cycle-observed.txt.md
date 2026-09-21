---
file: LICENSES/rounds/2026-08-28-license-review-mccoy-review-cycle-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-21
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.review-rules.md §1.103 / LICENSES/ACD-1.0.against.md #188 / LICENSES/AS-OF.md
---

# LICENSES/rounds/2026-08-28-license-review-mccoy-review-cycle-observed.txt

## What

**McCoy Smith 氏が 2026-08-28 に `license-review` の ModelGo スレッドへ投稿したメール、逐語 1 通。**
宛先は ModelGo の steward であって我々ではない（向き = **観測**）。

**ドシエが 4 文書で引きながら、原文を持っていなかった 1 通である。** 2 つの主張の出典:

1. **審査の周期** —— *"We work on a **two-month review cycle**"*、および時計が
   **最終**提出から動くこと（*"the July Board meeting was prior to two months from your
   **final** submission"*）。`AS-OF.md` / `READY-TO-SUBMIT.md` / `PEER-REVIEW-WATCH.md` /
   `ACD-1.0.review-corpus.md` §1.72 がこれを引く。
2. **資格表示** —— 署名は `McCoy` の次行に `[on behalf of the Licensing Committee]`（**逐語。改行を含むので 1 行に畳まない** ——畳んで逐語記法で囲むと、それは引用ではなく要約である・#191）。
   ドシエはこれを角括弧付きで引用しており、**我々の編集挿入かどうかが読み手に判別できなかった。**

## Why

**#82 / #92 と同じ形を閉じるためである** ——**主張が依っている一次資料を、リポジトリが
持っていなかった。** 我々が持っていたのは「それについての文書」だけだった。

**2026-09-21 に原文を取得して照合した結果は clean である**: 角括弧は**本人の署名**であって
我々の挿入ではない。**確かめた結果が「正しかった」場合も記録する** ——
確かめていないことと、確かめて正しかったことは別の状態だからである。

## How

- 出所: `license-review` 公開アーカイブ `2026-August.txt`
  （**2026-09-21T17:53Z 取得**・ブラウザ相当 User-Agent。既定の python UA では 403）
- 向き: **観測**（`-observed`）。我々宛ではないので受領と同じ欄に混ぜない
- **1 通 1 ファイル**（規則 1）

## Constraints

- 逐語部分は無改変（規則 1）。分析は `review-rules.md` §1.103 に置く
- **このメールから資格を「アドレス」で推論してはならない。** 送信元は
  `mccoy at lexpan.law`（法律事務所）であり、process ページは「個人資格の参加は非 OSI
  アドレスが期待される」と定める。**1 通の中で、アドレスの慣習と自己表示が逆を向いている。**
- **周期についての 2 つの一次資料は食い違う。** 公表 process ページ（改訂は 30 日・
  初回から 60 日を下回らない）と、本メールが述べる委員会の実務（最終提出から 2 か月）。
  **`READY-TO-SUBMIT.md` は両方を記録して選ばない。** ここでも選ばない

## Change impact

逐語部分を変更する正当な理由は存在しない。**周期についての新しい一次資料が出たら、
本ファイルを書き換えず別ファイルとして足す。**

## Audience-specific notes

- **審査者**: 我々が引用の出典を保持し、角括弧が誰の言葉かを原典で確かめた記録
- **後任 AI**: **引用を 4 文書で引いていることは、その原文を持っていることを意味しない。**
  `rounds/` に在るかを検索してから「一次資料に基づく」と書くこと
