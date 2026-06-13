---
file: .github/dependabot.yml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: package.json / Check 68
---

# .github/dependabot.yml

## What

GitHub Dependabot 設定。月次で `npm` (devDependencies: eslint / stylelint / playwright / http-server) と `github-actions` の 2 ecosystem を update する PR を自動提出。

## Why

dev tooling は月次低ノイズで update を受け取る。GitHub Actions の major tag 更新も同様。public site はランタイム依存ゼロ (C1 Boring Technology) なので dev 専用。

## How (usage)

```
GitHub Dependabot (毎月)
  ├─ npm group "dev-dependencies" → update PR 1 件
  └─ github-actions → update PR 1 件
```

## Constraints

- **Check 23**: YAML 構文 valid
- **Check 68**: npm + github-actions 両 ecosystem 含む

## Change impact

- schedule.interval 変更 → PR 頻度
- ecosystem 削除 → 該当領域の手動 update 負債が増える

## Audience-specific notes

### For AI agents
- 役割タグ: `dependency-management`, `monthly-cadence`

### For human engineers (新卒レベル)
- 月初に Dependabot PR が来る → CI green なら merge

### For third parties
- dev-tooling-only manifest + 月次低ノイズの依存更新パターン
