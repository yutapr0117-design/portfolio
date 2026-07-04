---
file: docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md
audience: ai, 監査人, 第三者全般
last-updated: 2026-07-04
canonical-ref: docs/architecture/file-size-budget.md / CLAUDE.md §7
---

# docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md

## What

2026-07-04 の肥大化解消セッションの decision record。owner 受諾の 1,000 行しきい値、実施した shipped JS 分割（pages/apps/mutation_samples）、Check 361 による機械強制、および残存 >1,000 行ファイル（check.py / e2e spec / style.css / index.html / main.js）の disposition（defer-with-reason / 設計制約）を記録する。

## Why

将来セッションが 15,700 行の check.py や 3,332 行の e2e spec に **無為に着手して token を浪費する / net-negative な分割を強行する**のを防ぐため、各ファイルを「なぜ今分割しないか」まで含めて明文化した load-bearing な判断記録。1,000 行しきい値を memory/convention でなく decision record + Check 361 で durable 化する。

## How

- shipped JS 分割は葉モジュール factory パターン（byte-equivalent）で実施。
- 「生じないように」は Check 361（BLOCKING・Check 71 の対称 exists⟹registered）で機械強制。
- 残存ファイルは表形式で行数・disposition・理由・（e2e は将来の de-risk 経路）を記載。

## Constraints

- `docs/incident-artifacts/` 配下（Check 42a/42b naming/placement）。
- README.md inventory に登録（Check 75）。
- 本 mirror doc は git-tracked ゆえ Check 108（docs/files 全 bijection）が要求。

## Change impact

- disposition が変わったら（例: check.py の safe split 手法が見つかった、e2e の 9-check glob 一般化を実施した）本記録を更新する。
- BUDGET-DATA / Check 361 の変更時は本記録の「実施したこと」表と整合を保つ。

## Audience-specific notes

- **AI (次担当)**: 肥大化トラックを再開する前に本記録を読む。check.py / e2e spec は defer 済（理由あり）。新 shipped JS を作ったら Check 361 が BUDGET-DATA 登録を強制する。
- **監査人**: 本セッションの 6 増分（#555-#559 + main 直 mutation split）の全体像と非破壊証明方針の索引。
