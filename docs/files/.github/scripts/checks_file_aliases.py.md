---
file: .github/scripts/checks_file_aliases.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol)
---

# .github/scripts/checks_file_aliases.py

## What

`check_repository_consistency.py` 分割トラックの split module。file alias byte-equality と required-presence を守る自己完結クラスタ Check **4/5/190** を内包し、`run(ctx)` で monolith から呼ばれる。

- **4** (llms alias 一致): `llms.txt` / `.well-known/llms.txt` / `llms_well-known.txt` / `.well-known/llms_well-known.txt` が byte-identical であることを強制。
- **5** (.well-known alias 一致): `.well-known/index.json` == `.well-known/agent-skills/index.json` (byte-identical)。
- **190** (.nojekyll 存在 BLOCKING): repo root の `.nojekyll` file 存在を BLOCKING 強制。欠落すると GitHub Pages が Jekyll を稼働させ `_` 始まり path が silent に 404 化する。

## Why

owner 合意 C-first の check.py 段階分割 (Phase 3)。Check 4/5/190 は全て自己完結 (ctx.ROOT/check/read_bytes のみ必要、global pre-loaded content 依存なし) で、分割パターンの最小コストルートを構成する。Check 190 は元位置 (line 762) から Check 4 の位置へ引き取り (独立・下流共有値なし・位置無関係)。

## How

- monolith: Check 4 の位置で `checks_file_aliases.run(_ctx)` を 1 回呼ぶ。
- `run()` は `ROOT`/`check`/`read_bytes` を ctx から unpack するのみ。global content 依存なし (html/mainjs/ai2ai 不要)。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **self-contained**: ctx.ROOT/check/read_bytes のみ使用。ctx-enrich 不要。
- **module-global 結合なし**: `exec` 不使用。依存は全て ctx 経由。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- monolith 行数: 920 → 886（−34・Phase 3）。
- 新 tracked file ゆえ Check 108 が本 doc を BLOCKING で要求。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `file-aliases`, `phase3`
- 最も単純な self-contained cluster の抽出パターン。ctx から ROOT/check/read_bytes のみ unpack し、全 file を run() 内で直接 read。

### For human engineers（新卒レベル）
- llms のエイリアスファイル (同内容で複数パスに置かれるテキスト) と .nojekyll (GitHub Pages の Jekyll バイパス) が正しいかを検証する 3 つの検査を抽出した。

### For third parties / auditors
- Phase 3: 自己完結クラスタの抽出。monolith 920→886 行。verify exit 0 + Check 45/70/105 緑で byte-equivalent を実証。
