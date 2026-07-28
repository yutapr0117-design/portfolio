---
file: .github/scripts/mutation_samples_archive2.py
audience: ai, 監査人, 第三者全般
last-updated: 2026-07-28
canonical-ref: .github/scripts/mutation_samples.py / mutation_samples_archive.py / mutation_samples_common.py / mutation_probe.py
---

# .github/scripts/mutation_samples_archive2.py

## What

curated mutation データの**次に古い側 (rotated) の entries** を保持する archive part 2。`MUTATIONS_ARCHIVE2` (dict の list) を公開し、`mutation_samples.py` が part 1 archive と tail の間に連結して公開 API `MUTATIONS` を構成する（順序 = 時系列: `MUTATIONS_ARCHIVE`(最古) + `MUTATIONS_ARCHIVE2` + tail(新)）。本 part は Check 282-361 の連続ブロックを保持する。

## Why

curated mutation は増分ごとに時系列で追記され無限に成長するため、`mutation_samples.py` が 1000 行しきい値を超える。log-rotation 方式（part に分け・最新 part へ追記・肥大化したら最古を archive へ移す）が recurrence 防止として最も適切。part 1 (`mutation_samples_archive.py`) が 995 行で Check 365 の 1,000 hard cap に近接し実質枯渇したため、2026-07-28 に本 part 2 を新設し、hot log の最古の連続ブロック (Check 282-361・80 entries) を受領した。これにより hot log (`mutation_samples.py`) が ~489 行へ縮小し、bijection sweep 等で保留していた新規 mutation を再び追記できるようになった。

## How

- `from mutation_samples_common import ROOT, CHECK` でパス定数を得る（循環回避のため共有定数は common モジュールに単一定義）。
- `MUTATIONS_ARCHIVE2` は各 entry が `name` / `file` / `find` / `replace` を持つ dict の list（consistency mutation ゆえ `test` フィールドは持たない）。
- 各 entry の意味・非 vacuous 保証・実行機構は `mutation_probe.py` の docstring を参照。本ファイルはデータのみで副作用も実行ロジックも持たない。

## Constraints

- **編集は rotate 時のみ**（新規 mutation は常に `mutation_samples.py` の tail へ追記する規約）。本 archive を直接編集するのは、より新しい part から entries を rotate してくる時だけ。
- Check 365（全非 A テキスト ≤1,000 BLOCKING）に整合させ、ceiling は 1,000 とする。近接したら part をさらに増やす（`mutation_samples_archive3.py` 等）。
- Check 362 / 379 / 380（mutation-integrity mesh）は `mutation_samples` を import して公開 `MUTATIONS` / `E2E_MUTATIONS` を読むため、本 part 追加は透過的（公開 API の内容・順序は不変）。

## Change impact

本ファイルの entries を編集/削除すると、対応する consistency Check の非 vacuity 検証（mutation-probe で「clean=OK / mutated=ERROR」を実証する能力）が失われる。rotate は「hot log から最古ブロックを移す」機械的操作に限り、内容は byte-equivalent に保つ。

## Audience-specific notes

- **AI**: 新規 mutation を本ファイルへ追記しないこと（規約は hot log tail 追記）。本ファイルは受動的な rotated データ。
- **監査人**: 公開 `MUTATIONS` の総数・順序が rotate 前後で不変であることが分割の正しさの証明（`len(MUTATIONS)` と各 entry の順序で確認できる）。
