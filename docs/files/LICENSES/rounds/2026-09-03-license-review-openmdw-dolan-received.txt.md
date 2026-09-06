---
file: LICENSES/rounds/2026-09-03-license-review-openmdw-dolan-received.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-06
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/rounds/2026-09-03-license-review-openmdw-sent.txt / LICENSES/PEER-REVIEW-WATCH.md
---

# LICENSES/rounds/2026-09-03-license-review-openmdw-dolan-received.txt

## What

**Michael Dolan 氏（Linux Foundation・OpenMDW steward）からの受領文。** 冒頭で
"Sado-san, Yokoi-san, thank you both for your detailed questions about the scope of the
termination trigger." と名指しで応答し、"directly or indirectly" の意味、Apache-2.0 / EPL-2.0 /
CDDL-1.1 / MPL-2.0 の同型表現、終了引き金の境界について答えている。

## Why

`rounds/` の規約は当初 **受け取った本文だけ**を想定していた（`against.md` #82 で
自分の送信へ拡張された）。2026-09-06 に測って分かったのは、**その拡張でもまだ足りなかった**
ことである —— steward は `license-review` に 4 通書き、3 名から応答を得ていたのに、
その一次資料はリポジトリのどこにも無く、`AS-OF.md` は「Responses received: None」と述べていた。
その記述は *ACD-1.0 のスレッドについて* は真だが、**読み手には「このリストで我々に誰も応じて
いない」と読める**。記録の射程が「我々の提出」に絞られており、「我々の活動」を覆っていなかった。

## How

- 出所は同上のアーカイブ
- **このメッセージは我々の Message-ID を参照していない。** スレッド内の別メッセージへの返信
  として配送され、本文で名指しに応答している。**ID 参照だけを追う検出では取りこぼす**
  —— 実際、最初の掃引で「OpenMDW 側は返信ゼロ」と誤って読みかけた

## Constraints

- 逐語部分は無改変（`rounds/README.md` 規則 1）。**誤字も改行も配送されたままにする**
- 分析はここに書かない（`ACD-1.0.discussion-log.md` が担当・規則 2）
- Check 108 が `docs/files/` mirror との 1 対 1 を BLOCKING で強制する
- ACD-1.0 本文の凍結（Check 453）とは無関係 —— この file は本文ではない

## Change impact

逐語部分を変更する正当な理由は存在しない。ヘッダ（出所・取得日・位置づけ）を
正確にするための修正は可。**アーカイブ側が後から更新されたら、追記ではなく取り直して日付を更新する。**

## Audience-specific notes

- **監査人**: 受領の有無は「ID 参照」ではなく「本文の名指し」でも成立する
- **後任 AI**: 検出器が 0 を返したときは、検出器の当て方を先に疑うこと
