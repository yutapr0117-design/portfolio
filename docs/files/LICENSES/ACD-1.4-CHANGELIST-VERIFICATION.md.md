---
file: LICENSES/ACD-1.4-CHANGELIST-VERIFICATION.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.4-CHANGELIST.md (変更の記録の本体)
---

# LICENSES/ACD-1.4-CHANGELIST-VERIFICATION.md

## What

`ACD-1.4-CHANGELIST.md` の 2 つ目の分冊。確定前検証（段 7・2026-11-06・相互参照と機械可読性は 5a）の節を持つ。

## Why

本体が 286,712 バイトで、バイト数の上限（Check 495a・300,000）まで約 13 KB だった（2026-11-24）。確定の後も追記が続いていた
（2026-11-23 に 8 commit）。道具と Check が名で読む節（主表・付録の草案ヘッダ・条項の対応表）は本体に残し、段 7 を移した。

## How

節を無改変で移し、本体には見出しと「別の file へ移した」の 1 段落を残した。段 7 の中の「1.0 から何が変わったか」の下書きを読む
Check 498 (j) は、glob を `ACD-*-CHANGELIST*.md` に広げてこの分冊も読む。

## Constraints

本文を改変しない移動である。1.4 は凍結した版だが、この file は FREEZE-DATA に入っていない（本文の byte の約束の外）。

## Change impact

本体は約 246 KB になる。段 7 を引く文書は見出しの残る本体から辿れる。

## Audience-specific notes

- **ai**: 段 7 を引くときはこの file を読む。本体の見出しは指し先を残すための案内である。
- **監査人**: 本文の無改変は `git log -p --follow` で移動の commit を当てて確かめられる。
