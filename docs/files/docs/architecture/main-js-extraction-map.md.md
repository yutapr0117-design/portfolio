---
file: docs/architecture/main-js-extraction-map.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: main.js / docs/architecture/repository-maintainability-map.md
---

# docs/architecture/main-js-extraction-map.md

## What

main.js の Stage 0〜5 物理分割計画 + factory pattern 確立経緯 (§3.10〜§3.11) + 危険度別ゲート (§3.5)。7,785 → 1,086 行 (−86%) 達成までの設計記録。

## Why

「いきなり物理分割してはいけない」原則の運用化。分割前に map を作り、危険度別ゲートで安全に進める。

## How (usage)

Stage 5 物理分割を進めるとき、各 sub-stage が map に従って実施。

## Constraints

- **Stage 5 gate**: Playwright baseline 取得が前提

## Change impact

- 新 Stage 追加 → repository-maintainability-map.md と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `extraction-plan`, `staged-physical-split`, `factory-pattern-source`

### For human engineers (新卒レベル)
- 「main.js をなぜ分割したか / どう分割したか」の全記録

### For third parties
- 大規模 monolith の段階的解体の実装例
