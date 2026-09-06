---
file: LICENSES/rounds/2026-09-03-license-review-modelgo-sent.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-06
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/rounds/2026-09-04-license-review-modelgo-duan-received.txt / LICENSES/PEER-REVIEW-WATCH.md
---

# LICENSES/rounds/2026-09-03-license-review-modelgo-sent.txt

## What

**2026-09-03 に `license-review` の ModelGo (MG0-2.0 / MG-BY-2.0) スレッドへ送った質問。**
MG-BY-2.0 の "Distribution" 定義はホスト型・API 経由のアクセスを明示的に含むのに、§2.2(a) の
「ライセンスの写しを添える」「通知を保持する」義務は、遠隔利用者が Output しか受け取らない
場合に何に付着するのか —— を問うている。

## Why

`rounds/` の規約は当初 **受け取った本文だけ**を想定していた（`against.md` #82 で
自分の送信へ拡張された）。2026-09-06 に測って分かったのは、**その拡張でもまだ足りなかった**
ことである —— steward は `license-review` に 4 通書き、3 名から応答を得ていたのに、
その一次資料はリポジトリのどこにも無く、`AS-OF.md` は「Responses received: None」と述べていた。
その記述は *ACD-1.0 のスレッドについて* は真だが、**読み手には「このリストで我々に誰も応じて
いない」と読める**。記録の射程が「我々の提出」に絞られており、「我々の活動」を覆っていなかった。

## How

- 出所は同上のアーカイブ
- **`In-Reply-To` / `References` なし**（上と同じ）
- 翌日 steward の Moming Duan 氏が条文に即して回答し、2025-03 の審査履歴 4 件を URL で引いた

## Constraints

- 逐語部分は無改変（`rounds/README.md` 規則 1）。**誤字も改行も配送されたままにする**
- 分析はここに書かない（`ACD-1.0.discussion-log.md` が担当・規則 2）
- Check 108 が `docs/files/` mirror との 1 対 1 を BLOCKING で強制する
- ACD-1.0 本文の凍結（Check 453）とは無関係 —— この file は本文ではない

## Change impact

逐語部分を変更する正当な理由は存在しない。ヘッダ（出所・取得日・位置づけ）を
正確にするための修正は可。**アーカイブ側が後から更新されたら、追記ではなく取り直して日付を更新する。**

## Audience-specific notes

- **審査者**: 我々が他者の条文をどう読むかの実例
- **後任 AI**: この質問の形（定義語の射程を、定義する節ではなく**使う節**から追う）は
  `BLIND-SPOTS.md` の「定義語の射程」次元と同じもので、**自分の本文に当てて #57 を出した**
