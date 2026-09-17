---
file: LICENSES/ACD-1.2-DRAFT.txt
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人, 後任 AI
last-updated: 2026-09-17
canonical-ref: LICENSES/ACD-1.1.txt (議論に付した確定テキスト・凍結) / LICENSES/ACD-1.2-CHANGELIST.md (何をなぜ変えるかの集約点) / LICENSES/ACD-1.0.errata.md (各変更が閉じる欠陥) / LICENSES/REVISION-PROTOCOL.md §2 (旧版は永久凍結・次版は併置)
---

# LICENSES/ACD-1.2-DRAFT.txt

## What

**次版 ACD-1.2 の草案。** 冒頭に **NOT IN FORCE / NOT SUBMITTED / NOT APPLIED** と自分で述べる。
**作成時点では ACD-1.1 と版番号・識別子以外は同一**で、変更はこれから入る。

## Why

**議論に付したテキストが動くと、その議論は何についてのものでもなくなる。**
だから 1.1 を凍結し、**改善は別 file で進める**（`REVISION-PROTOCOL.md` §2「旧版は永久凍結・次版は併置」）。
**作業場は常に 1 つ**にする —— 2 つあると、どちらが次版かが分からなくなる。

## How

- **Check 468 / 468d / 468e がこの file を見る**（身分表明・純 ASCII・節の連番・参照の解決・
  申告語数と条数の一致・gap 条項の生存・「まだ open な errata」の一致）
- **変更は `ACD-1.2-CHANGELIST.md` へ**、**この草案が自分で持ち込んだ欠陥は
  `ACD-1.1-SELF-AUDIT.md` へ**（後者は版ではなく**我々の掃引**の登録簿）
- 確定させる手順は `ACD-1.0.submission.md` §B.0 と `ACD-1.1-CHANGELIST.md` §0.13

## Constraints

- **`ACD-1.0.txt` と `ACD-1.1.txt` は編集しない**（Check 453 が sha256 で止める）
- **語数・条数の申告は実測と一致させる**（Check 468。消して黙らせない）
- **gap を担う §6 / §8.4 / §9 は、短くする圧力の下でも中身を失わない**（Check 468d）

## Change impact

**本文を触ったら**: 冒頭の申告語数・条数を測り直す／変更を `ACD-1.2-CHANGELIST.md` へ記録する／
**変えた条を引用・要約している他の条**を当て直す（`ACD-1.1-SELF-AUDIT.md` §3e の掃引）。

## Audience-specific notes

- **審査者**: これは議論の対象ではない。**議論の対象は `ACD-1.1.txt`**（凍結・sha256 pin 済み）
- **後任 AI**: **1.1 を直したくなったら、直すのは 1.2 である。** 1.1 は byte が pin されている
