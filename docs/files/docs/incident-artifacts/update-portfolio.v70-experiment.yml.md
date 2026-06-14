---
file: docs/incident-artifacts/update-portfolio.v70-experiment.yml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md Incident: GitHub Copilot v70 experiment
---

# docs/incident-artifacts/update-portfolio.v70-experiment.yml

## What

過去 v70 系の **archived workflow file**。GitHub Copilot 大規模リファクタリング実験で使用された workflow を `docs/incident-artifacts/` に物理移動して保存。`workflow_dispatch` trigger を持つため `.github/workflows/` には戻さない (誤って手動実行されると本番事故)。

## Why

historical evidence として保持。AIDK governance の「proof-of-work は減らさない」原則。

## Constraints

- **CLAUDE.md §3 で明文化**: 本ファイルを `.github/workflows/` に戻すことは禁止
- **Check 42**: incident-artifacts 直下の `*.yml` パターン

## Change impact

- `.github/workflows/` へ戻さない (絶対)

## Audience-specific notes

### For AI agents
- 役割タグ: `archived-workflow`, `do-not-restore`, `c5-incident-evidence`

### For human engineers (新卒レベル)
- 過去の実験 workflow — 触らない・戻さない

### For third parties (監査 / 採用 / 研究)
- AI 暴走 incident の証跡 (v70-series Copilot 実験 → revert)
