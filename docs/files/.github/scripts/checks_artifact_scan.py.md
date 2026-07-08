---
file: .github/scripts/checks_artifact_scan.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-08
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol)
---

# .github/scripts/checks_artifact_scan.py

## What

`check_repository_consistency.py` 分割トラックの split module。生成/キャッシュアーティファクトの追跡ガード **Check 37** を内包し、`run(ctx)` で monolith から呼ばれる。

- **37** (アーティファクト追跡 BLOCKING): `node_modules`・`__pycache__`・`*.pyc`・`test-results`・`playwright-report`・`blob-report`・`.pytest_cache`・`.DS_Store`・`Thumbs.db`・`npm-debug.log` などの生成/キャッシュファイルが git に追跡されていないことを BLOCKING 強制。

`.gitignore` は新規の誤追加を防ぐが、既に追跡済みのファイルや ZIP エクスポートに紛れ込んだアーティファクトは検出しない。本 Check は `ctx._member_paths` (= `git ls-files` 結果) を single source of truth として使用する。

## Why

owner 合意 C-first の check.py 段階分割 (Phase 3D)。Check 37 は `ctx._member_paths` + module 内定数のみで自己完結。`FORBIDDEN_*` 定数は安定定数のため module 内に複製する (Check 45/70/105 で整合が機械強制される)。

## How

- monolith: Check 37 の位置で `checks_artifact_scan.run(_ctx)` を 1 回呼ぶ。`_ctx._member_paths` は monolith の setup-global で事前計算済み。
- `run()` は `check` / `_member_paths` を ctx から unpack し、module-local `_FORBIDDEN_*` 定数でフィルタリング。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約し、Check 45/70/105 が自己整合を BLOCKING 強制。

## Constraints

- **ctx-enrich**: `ctx._member_paths` が必須 (pre-computed by monolith setup `_repo_member_paths()`)。
- **module-global 結合なし**: `exec` 不使用。依存は全て ctx 経由または module-local 定数。
- **FORBIDDEN 定数の複製**: monolith の `FORBIDDEN_GENERATED_*` と本 module の `_FORBIDDEN_*` は同一値で同期。安定定数のため drift リスクは低い。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- monolith 行数: Phase 3D 適用後に約 25 行縮小。
- 新 tracked file ゆえ Check 108 が本 doc を BLOCKING で要求。

## Audience-specific notes

### For AI agents（次担当）

- 役割タグ: `check-split`, `artifact-scan`, `phase3d`
- ctx._member_paths (= git ls-files の結果) を消費する pattern。FORBIDDEN 定数は module 内に複製 — drift を Check 45/70/105 が自動検出する設計。

### For human engineers（新卒レベル）

- git に追跡されてしまった node_modules や __pycache__ などのゴミファイルを CI で検出する Check。`.gitignore` で防げない「既追跡済み」ケースを補う。

### For third parties / auditors

- Phase 3D: 単一 Check の ctx._member_paths 消費パターン。verify exit 0 + Check 45/70/105 緑で byte-equivalent を実証。
