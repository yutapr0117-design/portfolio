---
file: .github/scripts/mutation_samples_common.py
audience: ai, 監査人, 第三者全般
last-updated: 2026-07-04
canonical-ref: .github/scripts/mutation_samples.py / mutation_samples_archive.py / mutation_probe.py
---

# .github/scripts/mutation_samples_common.py

## What

`mutation_samples.py` と `mutation_samples_archive.py` が共通で参照するパス定数 `ROOT` / `CHECK` を単一定義する小モジュール。

## Why

mutation_samples.py を log-rotation 方式で `mutation_samples.py` (新) + `mutation_samples_archive.py` (旧) に分割した際、両者が同じ `ROOT` / `CHECK` を必要とするため、循環 import を避けつつ重複を排除する共有モジュールとして切り出した (2026-07-04・1000 行しきい値対応)。

## How

- `ROOT = Path(__file__).resolve().parents[2]` (リポジトリルート)。
- `CHECK = ROOT / ".github" / "scripts" / "check_repository_consistency.py"`。
- 各 mutation entry の `file` フィールドがこれらを参照する。

## Constraints

- データもロジックも副作用も持たない (定数のみ)。
- mutation_samples.py / mutation_samples_archive.py の双方が本モジュールから import する (循環なし)。

## Change impact

- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。
- パス定義変更は全 mutation entry の解決に影響するため mutation_probe を実行して確認する。

## Audience-specific notes

- **AI (次担当)**: mutation データを追記する際に触る必要はない (ROOT/CHECK は安定)。追記先は mutation_samples.py の MUTATIONS 末尾。
