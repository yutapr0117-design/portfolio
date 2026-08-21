---
file: docs/session-records/AI2AI-archive-2.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-21
canonical-ref: AI2AI.md / docs/session-records/AI2AI-archive.md / docs/session-records/AI2AI-archive-old.md / .well-known/aio-manifest.json
---

# docs/session-records/AI2AI-archive-2.md

## What

`AI2AI.md` から log-rotation で退避した **Session Record #15–#19**（2026-05-29〜05-31・
v80+ track 立ち上げ期）の読み取り専用アーカイブ。archive 系列の 3 つ目。

    AI2AI-archive-old.md (#1–#4 + 旧 protocol notes)
      → AI2AI-archive.md (#5–#14)
        → **本ファイル (#15–#19)**

## Why

`AI2AI.md` は Session Record が append-only で伸び、2026-08-21 に **Check 365 の
1,000 行 BLOCKING にちょうど到達**した。次のセッションが Session Record を追加できない
＝ハンドオフが物理的に止まる状態だったので、**今の size ではなく無限成長の方を止める**
（mutation_samples.py と同じ log-rotation 規約・CLAUDE.md §7）。

**なぜ既存 archive へ追記せず新ファイルを起こしたか**（実測 2026-08-21）:

| ファイル | 行数 | 1,000 まで |
| --- | --- | --- |
| `AI2AI-archive-old.md` | 832 | 168 |
| `AI2AI-archive.md` | 858 | 142 |

退避対象の #15–#19 は **280 行**あり、どちらへ足しても**受け皿自身が 1,000 行を超える**
（＝違反を移動するだけ）。3 つ目が構造的に必要だった。

## How (usage)

- 過去 run の詳細を追うとき以外は読む必要がない。**cold-start の読み順は
  `CLAUDE.md` §7 → `AI2AI.md` の最新 Session Record**。
- 追記（次の rotate）をするときは、**本ファイルの余裕を実測してから**「ここへ足す」か
  「4 つ目を起こす」かを決めること。

## Constraints

- **読み取り専用**: 過去の Session 内容を書き換えない（履歴を偽ることになる）。
- **Check 365**: 1,000 行以内。現在 310 行なので当面の余裕はある。
- **Check 108**: 本 mirror doc が存在すること。
- **AIO 層 (C6)**: 本ファイルは `.well-known/aio-manifest.json` に**未登録**。
  `AI2AI-archive-old.md` も元から未登録なので、未登録 archive の存在自体は既存の状態。
  範囲を `#1-#19` へ広げる案は **consistency Check が role の範囲を `AI2AI-archive.md` の
  最大 Session 番号に紐付けて検証している**ため RED になり撤回した。
  結果として「**AIO 層が宣言する archive 範囲は #14 まで**」であり、これを埋めるには
  manifest の semantic 編集＝ **C6（要 orchestrator 承認）** に当たるため、
  AI 側の判断では書き換えず**未解決として明記**している。

## Change impact

- rotate するときは **AI2AI.md 本体のポインタ・退避先ファイル・（必要なら）manifest** を
  セットで更新する。片方だけ動かすと「どこに何があるか」が判らなくなる。
- `AI2AI-archive.md` の冒頭 NOTE は長らく「#5–#11」と書きながら実際は #14 まで入っていた
  （2026-08-21 に是正）。**追記したら範囲表記も必ず直す**こと。

## Audience-specific notes

### For AI agents
- 役割タグ: `handoff`, `session-records`, `archive`, `log-rotation`
- ここは**歴史記録**。現行の規範（C1–C7 / KERNEL / Operating Model）は `AI2AI.md` 本体が唯一の権威。

### For human engineers (新卒レベル)
- append-only のログは「今の大きさ」ではなく「無限に伸びること」が問題。
  受け皿の余裕を測ってから退避先を決める、というのがこの rotate の考え方。

### For auditors / third parties
- AI 自走下でハンドオフ記録が物理的な上限に当たり、**canon を壊さずに構造で解消した**記録。
