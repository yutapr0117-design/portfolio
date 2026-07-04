---
file: .github/scripts/mutation_samples_archive.py
audience: ai, 監査人, 第三者全般
last-updated: 2026-07-04
canonical-ref: .github/scripts/mutation_samples.py / mutation_samples_common.py / mutation_probe.py
---

# .github/scripts/mutation_samples_archive.py

## What

curated mutation データの**古い側 (rotated) の entries** を保持する archive part。`MUTATIONS_ARCHIVE` (dict の list) を公開し、`mutation_samples.py` が先頭に連結して公開 API `MUTATIONS` を構成する。

## Why

curated mutation は増分ごとに時系列で追記され無限に成長するため、`mutation_samples.py` が 1000 行しきい値を超えた (1,597 行)。「今の size」より「成長 trajectory」が本質的 bloat であり、**log-rotation 方式** (part に分け・最新 part へ追記・肥大化したら最古を archive へ移す) が recurrence 防止として最も適切。本ファイルはその part 1 (古い側 120 entries) を保持する (2026-07-04)。

## How

- `from mutation_samples_common import ROOT, CHECK` でパス定数を得る。
- `MUTATIONS_ARCHIVE = [ ... ]` に古い側の mutation entry を時系列順で保持。
- `mutation_samples.py` が `MUTATIONS = MUTATIONS_ARCHIVE + _MUTATIONS_TAIL` で連結 (順序 = 時系列)。

## Constraints

- データのみ (副作用・実行ロジックなし)。
- entry の意味・非 vacuous 保証・実行機構は mutation_probe.py の docstring が正 (本ファイルは重複記載しない)。
- **非破壊**: 分割は contiguous な時系列スライスの移動で、entry 内容は byte-equivalent。連結後の `MUTATIONS` は分割前と同一 (順序・件数不変)。

## Change impact

- 新規 mutation は本 archive ではなく `mutation_samples.py` の tail へ追記する (追記規約)。本 archive を編集するのは rotate 時 (mutation_samples.py の最古 tail entries をここへ移す) のみ。
- 新 tracked file ゆえ Check 108 (docs/files 全 bijection) が本 mirror doc を BLOCKING で要求。

## Audience-specific notes

- **AI (次担当)**: 追記は mutation_samples.py へ。本ファイルは rotate 運用時のみ触る。mutation_probe は `from mutation_samples import MUTATIONS` 経由で archive+tail を透過的に受け取る (import 経路不変)。
- **監査人**: 分割の非破壊性は「連結後 MUTATIONS の件数 (241) と順序が不変」で検証可能。mutation_probe が全 entry を実行して安全網の有効性を再確認する。
