---
file: LICENSES/rounds/2026-09-04-license-review-modelgo-duan-received.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-06
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/rounds/2026-09-03-license-review-modelgo-sent.txt / LICENSES/rounds/2026-09-05-license-review-modelgo-anna-received.txt
---

# LICENSES/rounds/2026-09-04-license-review-modelgo-duan-received.txt

## What

**Moming Duan 氏（ModelGo steward）からの受領文。** "Yokoi-san, Thank you for the careful
reading. Let me answer from the text as written." と応じ、(1) 定義の読みは正しい (2) しかし
§2.2(a) は付着すべき Licensed Materials が無い以上は発火しない (3) これは起草の穴ではない、と
3 点で回答し、2025-03 の審査スレッド 4 件をアーカイブ URL で引いている。

## Why

`rounds/` の規約は当初 **受け取った本文だけ**を想定していた（`against.md` #82 で
自分の送信へ拡張された）。2026-09-06 に測って分かったのは、**その拡張でもまだ足りなかった**
ことである —— steward は `license-review` に 4 通書き、3 名から応答を得ていたのに、
その一次資料はリポジトリのどこにも無く、`AS-OF.md` は「Responses received: None」と述べていた。
その記述は *ACD-1.0 のスレッドについて* は真だが、**読み手には「このリストで我々に誰も応じて
いない」と読める**。記録の射程が「我々の提出」に絞られており、「我々の活動」を覆っていなかった。

## How

- 出所は同上のアーカイブ
- **末尾に我々の送信本文が引用の形で含まれる**（Outlook 形式の引用ヘッダつき）
- 我々の Message-ID を `In-Reply-To` / `References` で参照している —— **この 1 件だけ**

## Constraints

- 逐語部分は無改変（`rounds/README.md` 規則 1）。**誤字も改行も配送されたままにする**
- 分析はここに書かない（`ACD-1.0.discussion-log.md` が担当・規則 2）
- Check 108 が `docs/files/` mirror との 1 対 1 を BLOCKING で強制する
- ACD-1.0 本文の凍結（Check 453）とは無関係 —— この file は本文ではない

## Change impact

逐語部分を変更する正当な理由は存在しない。ヘッダ（出所・取得日・位置づけ）を
正確にするための修正は可。**アーカイブ側が後から更新されたら、追記ではなく取り直して日付を更新する。**

## Audience-specific notes

- **審査者**: 他の steward が我々の読みを「正確」と扱った記録
- **後任 AI**: 引用された過去スレッド 4 件は ACD-1.0 §10 の「利用に条件を課さない」設計の
  外部裏付けとして使える（`PEER-REVIEW-WATCH.md` §3.10）
