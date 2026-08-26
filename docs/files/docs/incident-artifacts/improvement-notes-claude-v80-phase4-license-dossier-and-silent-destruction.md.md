---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-license-dossier-and-silent-destruction.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-27
canonical-ref: CLAUDE.md / AI2AI.md / docs/architecture/total-check-runbook.md / LICENSES/README.md
---

# improvement-notes-claude-v80-phase4-license-dossier-and-silent-destruction.md

## What

2026-08-24 〜 2026-08-27 の run（PR #1292〜#1351・60 件）の経緯記録。2 本の軸を扱う ——
**提出中のライセンスについてリポジトリを見れば疑問が潰せる状態を作ること**と、
**利用者が何もしていないのに何かが失われ、しかも黙っている面を潰すこと**。

## Why

CLAUDE.md §7 は cold-start の AI が最初に読む一次ハンドオフだが、要点しか書けない。
本ファイルは §7 から指される詳細層で、**どう測ったか / どこで自分の測定を疑ったか /
なぜ作らなかったか**を残す。とくに起草主体の記述が 6 回の往復を経て確定した経緯は、
「書けるのは本人が述べたことかリポジトリの証跡だけ」という規律の由来として重要。

## How

run 中の実測値・非 vacuity 検証の結果・誤診しかけた 6 件を、テーマごとに記述する。
数値の権威は本ファイルではなく `total-check-runbook.md` §9（Check 総数）と
`file-size-budget.md`（行数・byte）にある。

## Constraints

- **NON-CANONICAL**。規範は `AI2AI.md`、数値は runbook §9 が正。
- **歴史記録**なので、後から事実が変わっても本文は書き換えない（履歴を偽らない）。
  訂正が要る場合は追記で示す。
- ライセンス本文は凍結中（Check 453）。本ファイルはその事実を記述するだけで、本文には触れない。

## Change impact

追加時は `docs/incident-artifacts/README.md` の inventory（Check 75）と本 mirror（Check 108）を
同じ commit で同期する。

## Audience-specific notes

- **監査人**: 「作らなかった判断」と「誤診しかけた測定」を明示的に残している。成功だけを記録した
  文書は、次に読む人が同じ罠を踏むのを防げない。
- **採用担当 / 第三者**: 自律的に動く実装者が、自分の測定と自分の記録をどう疑うかの実例。
