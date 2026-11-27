---
file: .github/scripts/list_open_items.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-27
canonical-ref: LICENSES/ACD-1.0.against.md / LICENSES/ACD-1.0.against-2.md / LICENSES/ACD-1.0.errata.md / LICENSES/ACD-OSI-BOTTLENECKS.md / .github/scripts/prepare_version_freeze.py
---

# .github/scripts/list_open_items.py

## What

ACD の OSI 承認に向けて「開いている項目」をドシエ全体から 1 つの一覧に集める。register の CLOSED / TRADE でない行（我々が手を
打てる TEXT・DOSSIER・OPEN・UNTRIAGED と、外部に依る EXTERNAL を分ける）、閉じていない errata、決着していない B、確定のゲート
（gate_6b・gate_6c）の満たしていない条件、AS-OF の答えていない問い、合成の文書（READINGS-SYNTHESIS.md）§6 の残り、合否の基準を書いてまだ満たしていない register の行、オーナーにしかできない行為の表、法律家と実務家への問い、候補（SELF-AUDIT の 🔴 と先に登録した反例・閉じたかは読んで確かめる）、`--advisory` で consistency の ADVISORY の警告（30 と 1c の依頼で足した）。担当の候補の列つき。

## Why

2026-11-16 のオーナーの依頼「ACD の OSI 承認に向けての全ての改善項目を洗い出し尽くした上で行い続けて」。開いている項目は文書ごとに
散らばり、人が拾うと漏れるので、拾い方を 1 つの道具に置き、5 人で分ける一覧にする。

## How

どれも現物から導く（件数を宣言しない）。register の状態は Check 474 と同じトークン、errata は prepare_version_freeze.errata_closures、
ゲートは同じ道具の gate_6b / gate_6c を呼ぶ。

## Constraints

- **載るのはドシエが自分で「開いている」と書いた項目と道具が数えられる欠けだけ**で、誰も書いていない欠陥は載らない。洗い出しの残りは、
  読み・反例・模擬委員会が見つける。担当の候補は目安。担当の候補は役の名（本文・ドシエ・統合・採掘・機械層）で出す。内部の記録はセッションの名で書かれているので、表に出す所で担当の欄だけを読み替える（セッションの名はセッションが替わるたびに古くなる・2026-11-27）。

## Change impact

- register の状態の語彙（Check 474）や B の表の列を変えたら、ここの読み方も合わせる。

## Audience-specific notes

- **AI / 後任**: 一覧の数を外向きの文書に書き写さない（すぐ古くなる）。必要なら道具の名と日付を添えて引く。
