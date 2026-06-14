---
file: docs/architecture/check-repository-consistency-map.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .github/scripts/check_repository_consistency.py / Check 64
---

# docs/architecture/check-repository-consistency-map.md

## What

check_repository_consistency.py (約 3,600 行・Check 1〜99) の **構造地図**。6 機能カテゴリ (A: version sync / B: AIO surface / C: CSP / D: docs / E: file split / F: governance) に分類した table + helper inventory + 分割指針。

## Why

肥大化したスクリプトを将来安全に分割するための準備地図。Check 一覧の human-readable inventory。

## Constraints

- **Check 64**: Check 番号がカテゴリ間で一意

## How (usage)

Check 追加 / レビュー時に人間が table を読む。category 別に新規 Check の挿入位置を判断。

## Change impact

- Check 追加 → table + BLOCKING 件数 + Subject の "Check 1〜N" 同期

## Audience-specific notes

### For AI agents
- 役割タグ: `check-map`, `category-A-to-F`, `human-readable-inventory`

### For human engineers (新卒レベル)
- Check の全体を見渡す地図

### For third parties
- 99 Check の体系的整理
