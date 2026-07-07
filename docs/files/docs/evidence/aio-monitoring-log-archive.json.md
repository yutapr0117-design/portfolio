---
file: docs/evidence/aio-monitoring-log-archive.json
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-07
canonical-ref: docs/evidence/aio-monitoring-log.json (current runs) / .github/scripts/aio_monitoring.py / Check 25
---

# docs/evidence/aio-monitoring-log-archive.json

## What

`docs/evidence/aio-monitoring-log.json` のログローテーションで分離した**古い runs (1–6, 2026-05-11 〜 2026-05-12)**。構造は main ファイルと同一（schema_version / monitored_signals / runs 配列）。現行の runs は `aio-monitoring-log.json` に残る。

## Why

`aio-monitoring-log.json` が 1,093 行に達し owner 目標「A 以外の全ファイル ≤1,000 行」を超過。runs 1–6（旧日付）を本ファイルに分離し main を 759 行に圧縮。mutation_samples の log-rotation パターンと同じ手順（純データの append-log は「今の size」でなく「無限成長」を止める）。

## How

- `aio_monitoring.py` は `aio-monitoring-log.json` のみ読み書きする（本ファイルは write しない）
- 本ファイルは読み取り専用アーカイブ。Check 25（evidence_policy key）は main ファイルのみ対象
- Check 96（1-to-1 mirror bijection）が `docs/files/docs/evidence/aio-monitoring-log-archive.json.md`（= 本ファイル）の存在を BLOCKING で強制

## Constraints

- **変更不可**: runs 1–6 の観測データは immutable historical record
- **Check 96**: 本 mirror doc が tracked-file bijection を満たす
- main ファイルとは別に git-tracked（`git ls-files` で確認可）

## Change impact

- アーカイブの追加により Check 96 が 1 件増加（本 mirror doc が必要になった）
- `aio_monitoring.py` の動作は不変（main ファイルのみ読み書き）
- runs 1–6 の AIO digest は aio-manifest.json の observational_evidence に含まれる（C6 A2 由来の derived value）

## Audience-specific notes

### For AI agents
- 役割タグ: `observation-log`, `archive`, `log-rotation`, `runs-1-6`
- **アーカイブ追記は禁止**。新規 runs は `aio-monitoring-log.json` へ自動 append される
- 次のローテーション時: main が再び 1,000 行超になったら古い runs を本ファイルに移すか新しい archive-2 を作る

### For human engineers（新卒レベル）
- 古い観測記録。直接編集不要。現在の記録は `aio-monitoring-log.json` を見る。

### For third parties / auditors
- 2026-05-11〜05-12 の 6 回分の AIO 観測試行記録。引用 0 件（honest attempt_log_only）。
