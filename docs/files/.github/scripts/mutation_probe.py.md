---
file: .github/scripts/mutation_probe.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-23
canonical-ref: .github/scripts/check_repository_consistency.py (gate) / package.json (mutation-probe)
---

# .github/scripts/mutation_probe.py

## What

安全網 (consistency Check + e2e) が回帰を本当に捕捉するかを再現検証する on-demand meta-QA ツール (completeness critic)。過去に修正した実 bug class を表す curated mutation を 1 つずつソースへ適用し、対応する gate (`check_repository_consistency.py`) が RED になる (=捕捉する) ことを確認して即復元する。`npm run mutation-probe` から起動。CI gate ではない。

## Why

このリポジトリの価値は「機械強制された品質の安全網」そのもの。その安全網が劣化していないか (mutation が SURVIVE する穴が無いか) を機械的・再現的に確認する手段が必要。Check/e2e は守るが「守りが効いているか」自体は別途検証すべき (protect the protector)。手動 mutation 検証 (route 破壊→e2e 捕捉 等) を curated set として固定し再現可能化する。

## How (usage)

```
npm run mutation-probe  →  python3 .github/scripts/mutation_probe.py
  1. baseline gate が GREEN か確認 (RED なら中止)
  2. 各 mutation: find-anchor 存在を assert → 適用 → gate 実行 → 即復元 (try/finally)
       caught   = gate が RED になった (安全網が捕捉) ✓
       SURVIVED = gate が GREEN のまま (カバレッジの穴) → exit 1
       DRIFT    = find-anchor が現行ソースに無い (probe 自身が要更新) → exit 1
  3. 全実行後に gate が GREEN へ戻ることを確認 (ファイル汚れ残り検出)
```

現行 mutation (11 件): Check 45 (section bijection) / 112a (IME guard) / 129 (topbar double-fire) / 130 (oninput focus-loss) / 125 (dead-constant) / 126・50d (ESLint no-dupe-keys) / 131 (SW decode guard) / 118 (PAGE_META coverage) / 111 (e2e no-networkidle) / 114 (e2e no-.only) / 132 (AIO evidence↔sitemap)。

## Change impact

- 新しい bug class を Check で systematize したら、その class の mutation を MUTATIONS へ追加するのが理想 (安全網の自己検証範囲を増やす)
- 対象ソースの find-anchor がリファクタで変わると DRIFT 報告される → mutation の find/replace を更新

## Constraints

- **Python 3.10+ guard** 必須 (Check 104。npm から呼ばれる .github/scripts/*.py の規律)
- **非 vacuous**: 各 mutation は適用前に find-anchor 存在を assert (no-op で偽 "caught" を防ぐ)
- **安全性**: try/finally で必ず復元 + 全実行後の gate GREEN 確認
- **Check 10**: py 構文妥当 / **Check 108**: docs/files mirror bijection (本ファイルがその mirror)

## Audience-specific notes

### For AI agents
- 役割タグ: `meta-qa`, `mutation-testing`, `completeness-critic`, `on-demand`
- CI gate ではない。安全網の劣化検知に手動/定期で走らせる

### For human engineers (新卒レベル)
- mutation testing = わざとバグを入れてテストが気づくか試す手法。気づかなければテストの穴

### For third parties
- machine-enforced quality net を「mutation で自己検証する」meta-QA の実装例
