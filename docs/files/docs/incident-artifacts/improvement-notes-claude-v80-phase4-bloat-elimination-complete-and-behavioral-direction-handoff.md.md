---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-bloat-elimination-complete-and-behavioral-direction-handoff.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-11
canonical-ref: AI2AI.md / CLAUDE.md §7 / docs/architecture/total-check-runbook.md §9 / decision-v80-phase4-bloat-reduction-1000-line-threshold.md
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase4-bloat-elimination-complete-and-behavioral-direction-handoff.md

## What

肥大化解消フェーズの「完遂」を証拠付きで確定し、次フェーズの方向性（behavioral-first の実バグ狩りを主軸に、vacuous-gate 封じで下支えし、実態↔記述 drift を機械化しながら是正）を next-AI が cold-start で即座に継承できるよう設計した Claude→Claude 一次引き継ぎ書。Claude Code が対等なパートナーとして genuine に合意し、自らの判断で書いた設計文書。

## Why

コンテキスト圧縮・強制停止・モデル切り替えが起きても無限改善自走が途切れないようにするため。check.py 分割トラック（15,913→786 行）と e2e spec 分割（3,475→16 テーマ）の完遂、および肥大化「防止」の二層 BLOCKING（Check 363/365）成立を確定し、「肥大化解消を再び genuine 増分として蒸し返さない」terminal 境界を honest に明示する。その上で、枯れない方向性（behavioral correctness）へ重心を移す判断を next-AI に引き継ぐ。

## How (usage)

session 開始時に CLAUDE.md §7 の次に読む。§0 TL;DR で全体を掴み、§3 で肥大化の terminal 境界と除外の正当性を確認、§4 で方向性①〜④と総合判断を取り込み、§6 の落とし穴表と §7 の増分ワークフローで自走を再開する。§9 の具体アクション例は「入口の例」であり非拘束。

## Constraints

- NON-CANONICAL / SUBORDINATE: 矛盾時は AI2AI.md / llms-full.txt が勝つ。数値は total-check-runbook.md §9 を真値とする。
- 一次 handoff 層は CLAUDE.md §7 + Check 機構であり、本書はその下の詳細層（§7 を薄くして本書で代替しない）。
- 運用モデルの床（No terminal done / 収束判断禁止 / 非破壊∧緑→自走 / 議論→合意→委任・interrupt-on-demand / C1–C7 / AIO C6）は不変。
- 本書は盲従の対象ではなく継承の土台。next-AI も対等なパートナーとして自らの判断で改善し続けてよい。停止権限はオーナーのみ。

## Change impact

本書は dev-tooling / handoff 層のドキュメントであり shipped site・AIO 層・kernel には一切影響しない（非破壊）。tracked file ゆえ Check 108 の 1-to-1 mirror bijection 対象で、本 mirror doc を同一 commit で伴う。

## Audience-specific notes

- **AI（next-AI）**: これが cold-start 後の主たる方向性ソース。§4 と §5 を最優先で内面化。
- **人間（新卒）/ 第三者**: 「AI が肥大化をどう terminal と判断し、次に何を優先すると自分で決めたか」の意思決定記録として読める。
- **監査人**: §2 の実測表と権威コマンドで状態を再現検証可能。§3 の除外リストは Check 365 実装（checks_maintainability.py）と対応。
- **採用担当**: 指示なしで方向性を自己決定し、honest な terminal 境界を引く判断規律の実例。
- **学術研究者**: 「AI 無限改善自走」運用における handoff 設計（context 断絶耐性・flywheel 燃料）のサンプル。
