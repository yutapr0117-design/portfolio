---
file: .github/workflows/update-playwright-snapshots.yml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-02
canonical-ref: e2e/portfolio.spec.js / .github/workflows/playwright-regression.yml
---

# .github/workflows/update-playwright-snapshots.yml

## What

Playwright 視覚回帰 baseline の **手動更新 workflow**。workflow_dispatch のみ。`--update-snapshots` で新 baseline を生成 → PR として提出 → 人間レビュー → merge → 次回 playwright-regression が新 baseline を使用。

## Why

baseline 更新は人間レビューが必須 (意図的な視覚変更を承認する gate)。直接 main commit せず PR 経由にすることで、AI 暴走防止 + 人間 review gate を両立。

## How (usage)

```
on: workflow_dispatch (手動)
└─ checkout + setup-node + npm ci + playwright install
└─ PLAYWRIGHT_UPDATE_SNAPSHOTS=1 で test:e2e --update-snapshots
└─ peter-evans/create-pull-request@v8 で snapshot PR を自動提出
└─ 人間が PR をレビュー / merge
```

## Constraints

- **Check 23**: YAML 構文 valid
- **Check 48**: PR 作成 step がある場合は contents:write + pull-requests:write の両方明示
- **Check 51**: Playwright の pin（`package.json` が権威・版数はここに書き写さない）を runbook と整合
- **Check 67**: permissions 明示

**baseline を再生成する前に読むこと（2026-11-02 実測）**: いまの baseline は 2026-06-10 の run 27243953369 で作られ、
当時の `ubuntu-latest` は 24.04 だった。GitHub は 2026-10-19 から `ubuntu-latest` を **26.04** へ順に移しており、
11-02 時点で mutation-probe と aio-monitoring の run は `Image: ubuntu-26.04` で走っている（probe の behavior 側
407 件は 26.04 で全件 pass ＝ 機能面の移行は済んでいる）。screenshot はフォント描画が OS で変わりうるので、
**再生成は新しい image で行う**のが正しい（この workflow も `ubuntu-latest` なので、dispatch すれば自然にそうなる）。
ADVISORY の screenshot は少なくとも 09-10 から全 run で失敗しており、差分の大半は意図したヒーローの文言の
書き換え（h1 の focus 枠は #2258 で別に直した）。

## Change impact

- baseline 生成 → e2e/portfolio.spec.js-snapshots/ 配下に PNG が増える
- workflow trigger に schedule 追加禁止 (人間 gate を保つ設計)

## Audience-specific notes

### For AI agents
- 役割タグ: `baseline-generator`, `human-gate`, `manual-dispatch-only`

### For human engineers (新卒レベル)
- 意図的に画面を変えたら、Actions UI から手動で実行 → 出てくる PR をレビュー → merge

### For third parties
- AI 実装の視覚回帰における人間 review gate の保ち方の実装例
