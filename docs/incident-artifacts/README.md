# docs/incident-artifacts/ — Inventory

```
Last-Updated  : 2026-06-13
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (post-Stage 5 「All Plans Combined」 で本 README を新設)
Subject       : 24 artifact files (decision records / improvement notes / 過去 workflow archive) の inventory
Canonical-Ref : AI2AI.md (canonical) / docs/README.md (artifact placement governance)
Status        : Plan D「物理移動なし、README で grouping を提供」設計の本体。append-only 文化を守りつつ認知 load を下げる。Check 75 で機械強制。
```

> **このファイルの目的:** `docs/incident-artifacts/` は increment ごとの decision records と improvement notes の append-only history を蓄積する。物理ファイルは増え続ける (24 件 → 100 件超え予定) ため、人間 / AI レビュアーが「最新は何か」「どの increment の話か」を一覧で掴むためのインデックスを提供する。**ファイル物理移動は行わない** (sha256 連鎖を破壊しないため)。本 README の inventory は Check 75 によって機械強制され、新規 artifact 追加時に本 README への列挙が抜けると pre-commit で BLOCKING fail する。

---

## 1. 命名規約 (Check 42 で機械強制)

`docs/incident-artifacts/` 直下に置く artifact は以下のいずれかの命名規約に従う:

| pattern | 用途 |
|---|---|
| `decision-*.md` | 設計判断記録 (なぜその path を選んだか) |
| `improvement-notes-*.md` | Claude / 人間が当該 increment で学んだこと・次の improvement 候補 |
| `*.yml` | 過去 GitHub Actions workflow のアーカイブ (実行禁止のため `.github/workflows/` から物理移動済み) |
| `README.md` | 本 inventory (Check 75 で機械強制) |

---

## 2. Decision Records (`decision-*.md`)

各 increment / phase の重要な設計判断の出自記録。

- `decision-v80-e2e-and-maintainability-stage-1.md`
- `decision-v80-maintainability-roadmap.md`
- `decision-v80-phase2-aio-update-canary.md`
- `decision-v80-phase2-artifact-governance.md`
- `decision-v80-phase2-ci-hygiene.md`
- `decision-v80-phase2-ci-hygiene-2.md`
- `decision-v80-phase2-ci-hygiene-3.md`
- `decision-v80-phase2-ci-hygiene-4.md`

---

## 3. Improvement Notes (`improvement-notes-*.md`)

各 increment 完了直後の Claude 視点での「学び」「次にやるべきこと」「機械化候補」の記録。次セッションでの状況復帰の起点として用いる。

- `improvement-notes-claude-v80-phase2-aio-update-canary.md`
- `improvement-notes-claude-v80-phase2-artifact-governance.md`
- `improvement-notes-claude-v80-phase2-baseline-gate-doc-hardening.md`
- `improvement-notes-claude-v80-phase2-ci-baseline-pipeline-hardening.md`
- `improvement-notes-claude-v80-phase2-ci-hygiene-4.md`
- `improvement-notes-claude-v80-phase2-consistency-invariant-hardening.md`
- `improvement-notes-claude-v80-phase2-console-fix-and-eslint-v10-and-research-application.md`
- `improvement-notes-claude-v80-phase2-dependency-modernization-and-flat-config.md`
- `improvement-notes-claude-v80-phase2-dev-ergonomics-and-lint-coverage.md`
- `improvement-notes-claude-v80-phase2-domain-authority-worksfor.md`
- `improvement-notes-claude-v80-phase2-lint-hygiene-and-doc-sync.md`
- `improvement-notes-claude-v80-phase2-public-freshness-observation.md`
- `improvement-notes-claude-v80-phase2-pure-utility-and-static-data-extraction.md`
- `improvement-notes-claude-v80-phase2-quiz-domain-split-and-bloat-governance.md`
- `improvement-notes-claude-v80-phase2-self-documentation-integrity.md`
- `improvement-notes-claude-v80-phase2-session-handoff-comment-injection.md`
- `improvement-notes-claude-v80-phase2-why-only-comment-injection.md`

---

## 4. Archived Workflows (`*.yml`)

「再実行禁止」の workflow を `.github/workflows/` から物理移動して保存した置き場。CLAUDE.md §3 で「`workflow_dispatch` を持つこれらの yml を `.github/workflows/` に戻してはならない」と明文化されている。

- `update-portfolio.v70-experiment.yml` — v70 実験用の手動 dispatch workflow (現在は禁止アーカイブ)

---

## 5. 機械強制 (Check 75)

`.github/scripts/check_repository_consistency.py` の **Check 75** は本 README に上記すべてのファイルが列挙されていることを BLOCKING で機械強制する。新規 incident-artifact 追加時は本 README の該当セクションへの追記を同一 commit で行う。
