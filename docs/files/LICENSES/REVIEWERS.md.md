---
file: LICENSES/REVIEWERS.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-27
canonical-ref: LICENSES/ACD-1.0.txt / LICENSES/FROZEN.md / LICENSES/ACD-1.0.submission.md / README.md
---

# LICENSES/REVIEWERS.md

## What

OSI の `license-discuss` から来た審査者が**最初に読む英語の入口**。提出の現況（受理済み・
返信待ち・license-review へも SPDX へも未提出）、本文の場所、開示すべき事実（弁護士不関与 /
起草は AI / 採用 1 件）、主張を自分で検証するコマンド、そして**日本語文書の英語での地図**を置く。

## Why

ドシエの大半は日本語だが、議論は英語で行われる。「リポジトリを見に来る」ことは確実に起きる
のに、入口が日本語だと**読まれる前に諦められる**。全訳は現実的でないので、
「どの文書に何が書いてあるか」を英語で示し、必要なものを名指しで翻訳依頼できる形にした。

root README の license バッジが `Public Experiment` のまま提出中のライセンス名と食い違って
いたのも同じ増分で是正した —— 審査者が最初に見る面が、提出物と違う名前を表示している状態
だったため。

## How

主張は**すべて 1 コマンドで検証できる形**で書く（固有名詞 0 件 / 置換テキスト 0 件 / 節数 16 /
凍結 digest）。検証を CI に任せている部分は Check 番号で示す（444 / 460 / 453）。

## Constraints

- **ライセンス本文は凍結中**（Check 453）。本ページは本文に触れない。
- 現況（どの list に出したか）の単一ソースは `FROZEN.md`。本ページはそれを参照する側で、
  食い違ったら FROZEN.md が正。
- 索引（`LICENSES/README.md`）への掲載は Check 459 が BLOCKING で強制する。

## Change impact

提出の段階が進んだら（license-review へ出す / 結果が出る）、本ページの Status 節と
`FROZEN.md` を同じ commit で更新する。**片方だけ直すと、審査者が読む面が古くなる。**

## Audience-specific notes

- **審査者**: 弱点を探す必要はない。`READY-TO-SUBMIT.md` に自分から書いてある。
- **監査人**: 「日本語だから読まれない」という実務上の障壁を、全訳ではなく地図で解いた例。
