---
file: LICENSES/ACD-1.5-CLARITY-TRIAL.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-23
canonical-ref: LICENSES/ACD-1.5-CHANGELIST.md / LICENSES/ACD-1.5-DRAFT.txt / LICENSES/ACD-1.4-THIRD-CLARITY-TRIAL.md
---

# LICENSES/ACD-1.5-CLARITY-TRIAL.md

## What

1.5 草案に入れる変更の試作。試作ごとに Before / After、欠陥、逆側、測定（`--compare`・文長）、反例、採否を書く。試作の番号は 1.4 の T134 に続けて T135 から、節番号はこの file の中で §1 から。

## Why

ACD-1.4 は 2026-11-23 に確定・凍結し、作業場は `ACD-1.5-DRAFT.txt` へ移った。1.4 の試作の 3 冊目（`ACD-1.4-THIRD-CLARITY-TRIAL.md`）は 982 行で Check 365（1,000 行の BLOCKING）の手前にあり、版も違うので、1.5 の試作は新しい file に書く。

## How (usage)

新しい試作は「## N. T番号 —— …」の形で足す。採否は `ACD-1.5-CHANGELIST.md` の「方針」の規則（閉じる errata / SELF-AUDIT の番号か、消す読みの分岐を書く。例外は読みを変えずに文を分けるか語を減らす変更）で決める。

## Constraints

- 草案を上書きしない。採った試作だけを草案・`CHANGES-ACD-1.5.txt`・CHANGELIST の表へ同じ commit で入れる。
- 1.4 の試作の記録は移さない（ドシエが条番号つきで引いている）。

## Change impact

- 試作の file を名で決め打ちしている道具（Check 468y ほか）にこの file を読ませる直しは、機械層が後続の PR で入れる（2026-11-23 の fc の約束）。

## Audience-specific notes

### For AI agents（次担当）

- 番号を重ねない: 1.4 の T1〜T134 は確定した記録で、1.5 は T135 から。

### For human engineers（新卒レベル）

ライセンスの次の版の文を書き直す試作のノート。

### For third parties / auditors

採った試作は `ACD-1.5-CHANGELIST.md` の表に記録される。
