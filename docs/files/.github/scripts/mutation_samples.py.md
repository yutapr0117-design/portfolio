---
file: .github/scripts/mutation_samples.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-04
canonical-ref: .github/scripts/mutation_probe.py (runner) / check_repository_consistency.py (gate)
---

# .github/scripts/mutation_samples.py

## What

`mutation_probe.py` (runner / completeness-critic) から **curated mutation データのみ** を分離した葉モジュール。`MUTATIONS`（consistency Check 安全網を検証する mutation 群）と `E2E_MUTATIONS`（behavior e2e 安全網を検証する mutation 群、`--e2e` モード）の 2 つの list を提供する。副作用も実行ロジックも持たないデータ専任。

## Why

肥大化解消 (2026-07-04): 元は `mutation_probe.py` 単一ファイルに runner ロジックと ~1,450 行の curated mutation データが同居しており、増分ごとに mutation を追記するたびにファイル全体 (1,700+ 行) を扱う必要があった。データと runner を分離することで、(a) 増分の追記はデータ側 (本ファイル) だけに閉じ、(b) runner (mutation_probe.py) は ~175 行の見通しの良い実行ロジックに縮小し、保守性と AI 自走効率 (コンテキスト負荷) を改善する。

## How (usage)

本ファイルは直接実行しない。`mutation_probe.py` が `from mutation_samples import MUTATIONS, E2E_MUTATIONS` で取り込む。`python3 .github/scripts/mutation_probe.py` 実行時、Python は script のディレクトリ (`.github/scripts/`) を `sys.path[0]` に追加するため cwd に依らず import が解決する。

各 mutation の意味・非 vacuous 保証 (find-anchor 存在 assert)・try/finally 復元・2 モード (consistency / e2e) の実行機構は `mutation_probe.py` の docstring を参照。

## Constraints

- **データのみ**: dict の list (`{name, file, find, replace}` / e2e は `+test`) 以外を置かない。実行ロジックは runner (`mutation_probe.py`) に閉じる。
- **ROOT / CHECK** を `mutation_probe.py` と同じ計算 (`Path(__file__).resolve().parents[2]`) で独立定義する（data 中の `"file": ROOT / ...` 参照のため）。
- 新規 mutation は「過去に実際に修正した bug class の再現」であること (padding 禁止)。件数は genuine 増分の OUTPUT であり TARGET ではない。
- Python 3.10+ 前提 (import 側 `mutation_probe.py` と揃える)。

## Change impact

- mutation を追加/変更しても runner (`mutation_probe.py`) は不変 → CI 挙動不変。
- 本ファイルの構文エラーは Check 10 (`.github/scripts/*.py` parse) が捕捉。
- 本ファイルは git-tracked ゆえ Check 108 (docs/files full bijection) が本 mirror doc の存在を BLOCKING で要求する。

## Audience-specific notes

- **AI (次担当)**: mutation の追記は本ファイルの `MUTATIONS` / `E2E_MUTATIONS` 末尾に行う。runner は触らない。
- **監査人**: 安全網の「守りが効いているか」を検証する completeness-critic のデータ層。runner と分離されているが両者で 1 つのツール。
- **第三者**: テストのテスト (protect the protector) を支える curated サンプル集。
