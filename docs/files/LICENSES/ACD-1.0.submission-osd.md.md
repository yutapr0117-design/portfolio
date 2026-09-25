---
file: LICENSES/ACD-1.0.submission-osd.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.submission-reference.md / LICENSES/ACD-1.0.submission.md
---

# LICENSES/ACD-1.0.submission-osd.md

## What

提出参考資料（`ACD-1.0.submission-reference.md`）のうち、**Open Source Definition に関する 4 節**
（§3 OSD 逐条 / §3b 反対側から読んだ逐条 / §3c OSI の却下理由一覧への逐項回答 / §3d 主題適格）。
**送る文面ではない（貼らない）。** 審査者が OSD の話をしに来たときに開く参照資料。

## Why

切り出し元が 899 行で advisory（900）の 1 行手前に達した。予算表が事前に「次は §3 系を切り出す」と
宣言していたので、**越えてから動くのではなく、越える前に**その計画を実行した。§3 系は
「OSD に照らしてどうか」という単一の問いで読まれ、他の節と読み手が分かれる。

## How

- 節番号は動かしていない
- 切り出し元の同じ位置に**案内見出し**（`### 3b. … → submission-osd.md`）を残したので、
  他文書からの `submission-reference.md §3b` 等の参照は張り替えずに解決する
- 本文中の裸の `§4c` などは切り出し元の節を指す（本文冒頭に明記）

## Constraints

- Check 459 が索引（`LICENSES/README.md`）からの到達性を、Check 461c が `last-updated` を強制
- 凍結本文（ACD-1.0 / 1.1）には触れていない

## Change impact

OSD の節を足すときはここへ。切り出し元に同じ節を二重に書かない（案内見出しは本文を持たない）。

## Audience-specific notes

- **審査者**: 逐条の反対側（§3b）は同じファイルにある —— 有利な読みと不利な読みを並べて読める
