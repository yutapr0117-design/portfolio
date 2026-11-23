---
file: .github/scripts/prepare_version_freeze.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-07
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

走ったあと新しい file を明示パスで `git add` し、consistency の RED を順に直す。RED がそのまま残りの作業の一覧である。

道具は、機械で決まるものも片付ける。凍結件数と検証コマンドの期待値（REVIEWERS / errata / AS-OF の「Text frozen」の行）、入口の「ドシエ全体は N 語・本文の M 倍」とその測定日（Check 472m が 10% の幅で照合する。確定で増える file で約 1 万語増える）、質問票の基準の版と *the 1.4 draft* の語、「いまの作業場」の行（Check 468k / 468t が名指す）、digest、`STATUS.md`、予算表である。2026-11-07 の予行で残った RED は次の 2 種だった。

| RED | 直し方 |
| :-- | :-- |
| Check 444m | 適用していない版を「適用している」と述べる行。文を読んで直す |
| Check 362 | 444m を直すと解ける |
| Check 311 | `--date` が **UTC の**今日より先のときに出る（sitemap の lastmod が CI の UTC の日付から見て未来になる）。JST の 0:00〜9:00 に JST の今日で確定すると出る（2026-11-23 の 1.4 の確定で踏んだ）。UTC の日付が追いつけば、failed job の rerun で消える。道具はこの場合に NOTE を出す |

2026-11-08 の予行では、Check 496 の mutation が草案の版で CHANGELIST を引いていて、確定すると空の次版を指して 362 に加わった。表の在る 1.4 の記録へ固定して直した。週次の予行は 362 が名指す mutation も見る。

RED にならないものが 1 つある。質問票の問 2 と問 5 は 1.3 の文のあとに 1.4 の差を述べる順なので、`ACD-1.4-CHANGELIST.md` の切り替えの表に従って順を入れ替える。

提出対象を切り替える前に、読む行を一覧で出す。何も書き換えない。

```sh
python3 .github/scripts/prepare_version_freeze.py --report 1.4
```

一覧は 4 種類である。番号が残って別の条になる行（Check 472 は無くなった条しか見ないので、ここは黙って通る）、`submission.md` の §A が前の版を述べる行、日付つきの実測、版を決め打ちした検証コマンド。送る本文が述べる版は Check 472o が RED で止める。上の段は全部読み、下の段は前の版と名指していない行だけ読む。範囲は `measure_clause_overlap.py` の `_OUTWARD` から導出する。

申請の日に `submission.md` の `SUBMISSION-TARGET` を切り替えると、Check 472 / 472f / 472h が版に紐づく欄を名指す。2026-11-07 の予行では、欄を直すと Check はすべて満たせた（満たせない Check は無かった）。Check が止めない行は上の `--report` で読む。

`--report` の「{版} 草案は … と述べる」の段（2026-11-16）は、その版だけを名乗る文が、その版の本文に無い語（試作で外した語）を引いている行を出す。errata・against と、版を名に持つ作業の文書、ほかの版も名乗る文は除く。測った値: main で 1 件（clause-reference の経緯の文・正しい）、T77 の枝で +2 件（§1.453 と submission-osd の OSD 5 の行・本物）。Check にしなかった理由は `check-repository-consistency-map.md` §2.9。

## Constraints

- **判断はしない。** 文を読む書き換え（Check 444m）と、`measure_descriptor_carryover.py` が出す条の読み直しは人が行う。
- **作業ツリーを書き換える。** LICENSE と llms 系は版を置換し、版を述べる行の適用の日付も直す（Check 444l が照合する）。過去の経緯を述べる文まで変わることがある。commit の前に差分を読み、`ACD-1.1-CHANGELIST.md` §0.13「改名は一括置換しない」に従って直す。
- AIO 層の編集は `aio-guardian` を通し、`update_aio_digests.py` を回す。
- 凍結本文の 1 行目と状態の文は §0.13 の型に従う。Check 490 が照合する。

`rehearse_version_freeze.py` が週次でこの道具を確定まで回す。残る RED の一覧を変えたら、同じ file の `EXPECTED` も合わせる。

## Change impact

§0.13 の型を変えたら `frozen_header` を合わせる。記述子の形を変えたら `descriptor` を合わせる。

## Audience-specific notes

- **AI**: 確定は申請の数日前で、行動規範の改定の取り込みのあとである（`OSI-APPROVAL-PLAN.md` §3.8）。使い捨ての worktree で先に回してよい。
- **監査人**: 2026-11-06 の予行で、走ったあとの RED は人の判断が要る面と派生値に絞られ、Check 490 は通った。

確定の日に冒頭の一覧を CHANGELIST の付録へ逐語で移すとき、CHANGELIST に `<!-- APPENDIX-NOTE: … -->` があれば、その文を付録の見出しの直下に置く（2026-11-16・portfolio-30 の案）。冒頭の一覧の形が草案の途中で変わったとき（1.4 では 11-16 に理由の句を外した・bd5d71e3）に、前の形の在りかを指す。文は版ごとに CHANGELIST が持ち、道具は版を決め打ちしない。
