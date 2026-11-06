---
file: .github/scripts/prepare_version_freeze.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-06
canonical-ref: LICENSES/ACD-1.1-CHANGELIST.md (§0.13 確定の手順) / LICENSES/SUBMISSION-MATERIALS.md (§0 申請の日の手順) / LICENSES/ACD-1.4-CHANGELIST.md (記述子の下書き)
---

# .github/scripts/prepare_version_freeze.py

## What

**作業中の草案を確定する機械的な作業を 1 回で行う手動の道具。** 確定本文、草案の pointer、次の草案と CHANGELIST、記述子、FREEZE-DATA、mirror、適用する面の版、binary の権利表示、SPDX XML を作る。

## Why

確定の日の手作業は約 50 file に及ぶ。2026-11-06 に使い捨ての worktree で 1.4 を確定して測ると、手作業の誤りの多くが無音だった。手順は予行の一時領域にしか無く、session が終わると消えるので、リポジトリへ移した（日次取得が session の終了で止まったのと同じ形を避ける）。

## How

```sh
python3 .github/scripts/prepare_version_freeze.py --date 2026-11-13
```

走ったあと新しい file を明示パスで `git add` し、consistency の RED を順に直す。RED がそのまま残りの作業の一覧である。2026-11-06 の予行で残った RED と直し方は次のとおり。

| RED | 直し方 |
| :-- | :-- |
| Check 121 | `npm run status` |
| Check 91 | `python3 .github/scripts/update_aio_digests.py` |
| Check 472c / 460 (q) | REVIEWERS.md と `ACD-1.0.errata.md` の凍結件数と検証コマンドの期待値。コマンドを実際に走らせ、REVIEWERS.md の再実行の日付も直す |
| Check 472h | QUESTIONS-FOR-COUNSEL.md の基準の版 |
| Check 468 (468k / 468t) | 「いまの作業場」の行と frontmatter の canonical-ref。文ごとに読んで直す |
| Check 362 | REVIEWERS.md と QUESTIONS-FOR-COUNSEL.md を直すと解ける |
| Check 413 (ADVISORY) | runbook §9 の追跡ファイル数を実測へ |

申請の日に `submission.md` の `SUBMISSION-TARGET` を切り替えると、Check 472 / 472f / 472h が版に紐づく欄を名指す。2026-11-07 の予行では、欄を直すと Check はすべて満たせた（満たせない Check は無かった）。文を読んで直すのは、REVIEWERS.md と READY-TO-SUBMIT.md が 1.0 の条番号（§15.7 / §15.8）を述べる 3 箇所である。

## Constraints

- **判断はしない。** 外向きの文書の書き換え（Check 468k / 468t が列挙する）、REVIEWERS.md の表と検証コマンド（472c / 472h）、`measure_descriptor_carryover.py` が出す条の読み直しは人が行う。
- **作業ツリーを書き換える。** LICENSE と llms 系は版を置換するだけなので、過去の経緯を述べる文まで変わる。commit の前に差分を読み、`ACD-1.1-CHANGELIST.md` §0.13「改名は一括置換しない」に従って直す。
- AIO 層の編集は `aio-guardian` を通し、`update_aio_digests.py` を回す。
- 凍結本文の 1 行目と状態の文は §0.13 の型に従う。Check 490 が照合する。

## Change impact

§0.13 の型を変えたら `frozen_header` を合わせる。記述子の形を変えたら `descriptor` を合わせる。

## Audience-specific notes

- **AI**: 確定は申請の数日前で、行動規範の改定の取り込みのあとである（`OSI-APPROVAL-PLAN.md` §3.8）。使い捨ての worktree で先に回してよい。
- **監査人**: 2026-11-06 の予行で、走ったあとの RED は人の判断が要る面と派生値に絞られ、Check 490 は通った。
