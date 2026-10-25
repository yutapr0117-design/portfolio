---
file: LICENSES/ACD-1.2.txt
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人, 後任 AI
last-updated: 2026-10-18
canonical-ref: LICENSES/ACD-1.2-CHANGELIST.md (1.1 からの全変更・確定時の草案ヘッダを逐語で保持) / LICENSES/FROZEN.md (sha256 pin) / LICENSES/ACD-1.0.errata.md (各変更が閉じる欠陥)
---

# LICENSES/ACD-1.2.txt

## What

**ACD-1.2 の確定テキスト（2026-10-17 凍結）。** 冒頭に **FROZEN TEXT / NOT SUBMITTED FOR APPROVAL / NOT APPLIED TO THIS REPOSITORY** と自分で述べ、`FROZEN.md` が sha256 で pin する（Check 453）。**次版の作業場は（当時）`ACD-1.3-DRAFT.txt`。** このリポジトリを覆っていたのは当時 1.0 で、**2026-10-25 から 1.3**（冒頭の「still ACD-1.0」はその日から偽だが、凍結テキストなので直せない）。

## Why

オーナーの依頼（2026-10-17）「ACD-1.2 も区切り良くして凍結して申請し、ACD-1.3 の改善に舵を切り替えて」による。**申請先は ScanCode の全文ルール**（OSI / SPDX への承認申請ではない）。

## How

**凍結の前に、6 観点の敵対的検証（相互参照・1.1 との差分と変更一覧・起草・OSD・機械可読性・errata の状態）を回し**、反証に耐えた欠陥のうち凍結前に直すべきものを直した（§5.2(b) の余分な or / §11.4 の「reaches nothing else」と §5 の約束の食い違い / §8.6 の自己矛盾した最終文 / §16.1 の通知文に personality が無い / 草案ヘッダの記録漏れと誤記）。条文は草案と同一で、**ヘッダだけを確定版の身分表示へ書き換えた**（1.1 と同じ形）。草案時代の変更一覧は `ACD-1.2-CHANGELIST.md` に逐語で移した。

## Constraints

- **本文は 1 byte も変えない**（Check 453）。欠陥を見つけたら `ACD-1.3-DRAFT.txt` で直し、errata に記録する。
- 純 ASCII（Check 441f）。

## Change impact

- 本文の条番号は 1.1 に従う（1.0 とは §15 以降が違う）。
- 機械可読の記述子は `ACD-1.2.machine.json`（Check 451d / 468h）。

## Audience-specific notes

- **審査者向け**: 議論の対象は依然 `FROZEN.md` の SUBMISSION-TARGET が名指す版である。
- **ScanCode 向け**: 全文ルールの申請対象（1.0 / 1.1 / 1.2）。
