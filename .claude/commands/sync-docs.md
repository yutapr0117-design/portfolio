---
description: Sync the three governance documents (check-repository-consistency-map.md / total-check-runbook.md §9 / file-size-budget.md) after a Check addition or count change. Verifies Check 45 / 64 / 70 / 59 hold.
allowed-tools: Read, Edit, Bash(grep*), Bash(python3 .github/scripts/check_repository_consistency.py)
---

Check 追加 / 削除 / 番号変更後に走らせる文書同期コマンド。以下の整合を一括で確認・修正する:

## 同期対象

1. **`docs/architecture/check-repository-consistency-map.md`**
   - table の Check 番号が 1..N で全カテゴリ一意か (Check 64)
   - 新規 Check 番号がカテゴリ表に行追加されているか
   - §3 級別 table の BLOCKING / ADVISORY 件数が実態に一致するか
   - `Last-Updated:` 値が今日 (or 直近 commit) に同期されているか (Check 65)
   - Subject `Check 1〜N` の N が実装最大値に一致するか

2. **`docs/architecture/total-check-runbook.md` §9**
   - 「consistency Check 総数」値が実装最大 N に一致するか (Check 70)
   - 新規 Check の説明が追記されているか
   - `Last-Updated:` 値が同期されているか (Check 65)

3. **`docs/architecture/file-size-budget.md`**
   - 新規ファイルが §2 表と §4 BUDGET-DATA の両方に追加されているか (Check 59)
   - 全 BUDGET-DATA path が実在するか (Check 71)
   - `<!-- ESLINT-BASELINE-DATA <N> -->` が消失していないか (Check 60)

4. **`.github/scripts/check_repository_consistency.py` 自身**
   - docstring inventory ↔ `# ── N.` section header ↔ implementation の 3 者一致 (Check 45a/b/c)

## 手順

1. 各文書を read で確認
2. drift を発見したら Edit で修正
3. 最後に `python3 .github/scripts/check_repository_consistency.py` を実行して exit 0 を確認
4. 結果を 5 行以内で報告 (Japanese)

## 出力

```
sync 結果:
- map.md: <fixed N items / no drift>
- runbook §9: <fixed N items / no drift>
- budget: <fixed N items / no drift>
- self-integrity: <Check 45 PASS / FAIL>
- final verify: <exit 0 / exit 1>
```
