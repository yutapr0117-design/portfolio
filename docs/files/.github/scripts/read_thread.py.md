---
file: .github/scripts/read_thread.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-15
canonical-ref: .github/scripts/census_decision_statements.py / LICENSES/AS-OF.md / LICENSES/THREAD-CANDIDATES.txt
---

# .github/scripts/read_thread.py

## What

census の会話 1 本（`--start` は会話の始まりの日付、`--subject` は件名）を、引用（`>` の行と Outlook の
"-----Original Message-----" 以降）と署名を除いて時刻順に出す。決める側の差出人には ★ を付ける。
`--deciders-only` は決める側の通と最初の通だけ、`--max-words` は 1 通の語数の上限。

## Why

2026-11-15 にオーナーが「未読の OSI スレッドを 5 人で無くして、反映して」と依頼した。census は会話を数えるが
本文を出さないので、5 人が月の file から通を手で拾うことになる。引用を除くのは、別人の文を発言者の文として
引く誤り（1c が同じ日に Outlook の形の引用で踏んだ）を減らすため。

## How

会話の切り方は `census_decision_statements.conversations()` をそのまま使う（読了の記録と同じ会話の単位になる）。
アーカイブの写しは `DOSSIER_ARCHIVE_CACHE`。CI には入れない（入力は手元の写し）。

## Constraints

- 出力は読むためのもので、引用の原文ではない。節に引く逐語は `rounds/` に置いた本文に当てる（Check 472n / 476）。
- 除くのは引用の形だけで、本文の言い換えはしない。

## Change impact

- census の会話の切り方を変えると、この道具の会話の単位も同じに変わる（意図どおり）。

## Audience-specific notes

- **AI / 後任**: 当て直し（2f の提案 (B)）にも使う。`--deciders-only` で拾い、論点のある会話は全文で読み直す。
