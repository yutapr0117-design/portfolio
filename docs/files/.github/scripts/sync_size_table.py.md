---
file: .github/scripts/sync_size_table.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-06
canonical-ref: docs/architecture/file-size-budget.md (§2 の表) / .github/scripts/checks_size_budget.py (Check 424)
---

# .github/scripts/sync_size_table.py

## What

**`file-size-budget.md` §2 の「実測行数」列のうち、Check 424 が赤くする行だけを実測へ直す道具。** `allowed_drift()` が許す差の定義も持ち、Check 424 と共有する。

## Why

列の行が隣り合うので、別の file を直した PR どうしが git の上で衝突していた（2026-11-06 に 1 日 3 回）。`LICENSES/` の文書は毎日書かれるので ±50 行の幅を許し、幅の中ではこの列に触らない。上限の判定は Check 52 / 365 が実物の行数で行うので、幅は上限を緩めない。

## How

```sh
npm run sync-sizes
```

衝突したら main の表を取り直してから回す。

```sh
git checkout origin/main -- docs/architecture/file-size-budget.md
npm run sync-sizes
```

## Constraints

- 幅を許すのは `LICENSES/` の行だけである。コードと shipped 面の行は `wc -l` と一致させる（main.js の行数は §2 が権威）。
- 表に行を足す道具ではない。ファイル集合の一致は Check 59 が見る。

## Change impact

幅を変えるなら `allowed_drift()` だけを変える。Check 424 はそれを読む。

## Audience-specific notes

- **AI**: 行数の RED が出たら表を手で直さず、これを回す。
- **監査人**: `LICENSES/` の行の値は概数である。正確な値が要るときは `wc -l` で測る。
