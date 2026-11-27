---
file: .github/scripts/census_board_self_identification.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-27
canonical-ref: .github/scripts/census_decision_statements.py / LICENSES/rounds/2026-09-13-osi-board-meeting-minutes-2025-06-to-2026-06.txt
---

# .github/scripts/census_board_self_identification.py

## What

公開アーカイブの写し（`~/osi-archive-cache`）から、送り手自身が OSI の理事・役員であると述べた行を、送り手×月で数える手で回す道具。

## Why

ドシエの「当時の理事」「当時の会長」の根拠は、repo では 2025-06〜2026-06 の議事録の名簿だけで、それより前の文は根拠を持てなかった。理事会ページの過去の写しは取得の経路で拒否された（2026-11-27）。本人の通（月の file と行）を根拠として指せるようにする。初回の全数で、ドシエが 2008-07 に「理事」と書いた人が、前後の 14 通で "OSI Board Observer" と署名していたことが分かった。

## How (usage)

`DOSSIER_ARCHIVE_CACHE=<dir> python3 .github/scripts/census_board_self_identification.py [<名の正規表現>]`

## Constraints

- **在任の下限の根拠だけ。否定の根拠にしない**（名乗らない月も在任でありうる）。署名は自己申告で正式な記録ではない。
- body の行の多くは理事会への言及で、自己申告ではない。読んで選ぶ。
- CI に入れない・Check にしない（否定の根拠にできないので RED の基準にならない）。

## Change impact

- 出力は判断の材料。ドシエの役の文を直すのは、その file の担当（readings は採掘、register はドシエ）。

## Audience-specific notes

### For AI agents（次担当）

- "wrote:" で本文を切らない（行間に答える形では署名が引用の後ろに来る）。

### For human engineers（新卒レベル）

メールの署名に書かれた肩書きを集めて、その人がいつ理事などを名乗っていたかを一覧にする道具。

### For third parties / auditors

肩書きは本人の申告で、OSI の公式の名簿ではない。
