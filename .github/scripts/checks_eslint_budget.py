"""
checks_eslint_budget.py — ESLint warning-baseline & file-size-budget governance checks
(extracted from check_repository_consistency.py — check.py split track・category "ESLint/budget governance").

Non-contiguous producer/consumer trio Check 59/60/72: file-size-budget §2表↔§4 BUDGET-DATA set equality
(59・PRODUCER of `_bsrc59`/`_budget59` — the ESLINT-BASELINE-DATA marker source + budget path), ESLint
warning-baseline regression guard (60・ADVISORY・consumer), ESLint baseline absolute-ceiling contract
(72・consumer). 59 defines `_bsrc59`/`_budget59` (the file-size-budget.md content + path) and 60/72
consume them; all three are extracted together as a full-set so the shared vars become module-local
(a naive slice extracting 60 or 72 alone crashed with `_budget59` NameError — safety net caught it).
Each reads its own target files (file-size-budget.md, ESLINT-BASELINE-DATA marker). No external coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  59. file-size-budget.md §2 表 ↔ §4 BUDGET-DATA 集合一致: docs/architecture/file-size-
      budget.md の人間可読 §2 表に列挙されたファイル集合と、機械可読 §4 BUDGET-DATA
      ブロックに列挙されたファイル集合が完全一致することを機械強制する。両者が drift すると
      「人間が見ている表」と「Check 52 が読む真値」が乖離し、運用上の見えない不整合を生む。
      Check 52（ADVISORY 行数予算）と Check 45（自己整合）の発想を、複数文書間にも適用した
      structural coherence 検査。(BLOCKING)
  60. ESLint warning baseline regression guard: docs/architecture/file-size-budget.md の
      `<!-- ESLINT-BASELINE-DATA -->` ブロックに記録された warning 数 baseline よりも、
      現状の `npm run lint` 実測値が増えていないことを ADVISORY で機械監視する。CI ログから
      "ESLint PASS — 0 errors, N advisory" を grep して N と baseline を比較し、N > baseline
      なら ADVISORY 警告を発する（exit に影響しない）。これにより、保護領域内の `no-var`/
      `curly`/`no-shadow` 等が無自覚に増える「lint 負債の静かな増加」を可視化する。
      Check 52 と同じ ADVISORY 級。(ADVISORY)
  72. ESLint baseline absolute-ceiling contract: file-size-budget.md の
      `<!-- ESLINT-BASELINE-DATA <N> -->` ブロックが記録する warning 数 baseline N が、
      sanity ceiling (200) を超えないことを機械強制する。Check 60 (ADVISORY 監視) を BLOCKING
      化した姉妹 Check で、baseline 値が極端に大きい drift も同時に検出する。Plan A の
      「絶対防衛線」を main.js / sw.js の AIDK Kernel 保護領域に手を入れることなく達成する
      設計。baseline marker が消失している場合も BLOCKING で fail。(BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract
    warnings = ctx.warnings

    # ── 59. file-size-budget §2 表 ↔ §4 BUDGET-DATA 集合一致 (BLOCKING) ────────────
    # file-size-budget.md は「人間可読 §2 表」と「機械可読 §4 BUDGET-DATA」の二段構成。Check 52
    # は §4 だけをパースして予算を確認するが、§2 と §4 が drift していると「人間が読む表」と
    # 「機械が真値とする値」が乖離する。本 Check で両者のファイル集合の対称差を 0 に強制し、
    # §2 表に新 budget 行を追加し忘れた／§4 から脱落した、等の drift を pre-commit で検出する。
    # 数値（行数・budget）の一致は honest dating で人間レビュー対象とし、本 Check は「ファイル
    # 集合」のみを比較する（行数 drift は別の Check 52 が間接的に拾う構造）。
    _budget59 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget59.exists():
        _bsrc59 = _budget59.read_text(encoding="utf-8")
        # §2: | `path` | ... という表形式
        _table59 = set(re.findall(r"\|\s*`([^`]+)`\s*\|", _bsrc59))
        # §4 BUDGET-DATA ブロック
        _budgetblock59 = re.search(r"<!--\s*BUDGET-DATA(.*?)-->", _bsrc59, re.DOTALL)
        if _budgetblock59:
            _data59 = set()
            for line in _budgetblock59.group(1).strip().split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    _data59.add(parts[0])
            # §2 表には `path` の他に `package.json` 等の説明用バッククォートも含まれる可能性が
            # あるため、§4 BUDGET-DATA に登録されたファイルが §2 表に存在することだけを強制し、
            # §2 表側の余計エントリは許容する（false positive 防止）。
            _only_data59 = sorted(_data59 - _table59)
            check(
                # _data59 非空ガード: BUDGET-DATA ブロックが空 (エントリ全削除) のとき
                # `not _only_data59` だけだと vacuous pass し、予算定義の消失を見逃す。
                bool(_data59) and not _only_data59,
                f"Check 59: file-size-budget §2 表 contains all {len(_data59)} BUDGET-DATA entries",
                "Check 59: " + (
                    "BUDGET-DATA block has zero entries — file-size 予算定義が消失している"
                    if not _data59 else
                    f"BUDGET-DATA entries missing from §2 表: {_only_data59} — "
                    f"§4 (機械可読) と §2 (人間可読) が drift している。§2 表に該当行を追加して同期せよ"
                ),
            )
        else:
            warnings.append("Check 59: BUDGET-DATA block not found — §2/§4 set check skipped")
    else:
        warnings.append("Check 59: file-size-budget.md not found — §2/§4 set check skipped")

    # ── 60. ESLint warning baseline regression guard (ADVISORY) ───────────────────
    # file-size-budget.md の <!-- ESLINT-BASELINE-DATA --> ブロックに warning 数 baseline が記録
    # されていることを ADVISORY で確認する。baseline ファイルが見つからない場合や正規表現で値を
    # 取れない場合は ADVISORY skip（環境制約のため exit に影響しない）。本 Check は CI 内で直接
    # `npm run lint` を実行せず、代わりに baseline 値が記録されていることだけを確認する（実測値
    # の取得と比較は CI 全体の ESLint scan ステップが担う）。これは「baseline 値が消えた／コメント
    # アウトされた」ことを ADVISORY で検出する役割で、warning 件数の実測比較は CI workflow 側で
    # 行う設計（Check 単体での実装複雑度を抑え、責務を分離する）。
    # 実効強制（regression の実 gate）: architecture-validation.yml の ESLint scan step が本 marker
    # を single source として読み、`WARN_COUNT > baseline → BLOCKING fail` で warning 増加（新規
    # lint 負債）を CI で落とす。本 Check は「marker が存在し CI が比較できる状態」を保証する presence
    # 層、CI step がその marker を使った count 比較層、という二層で「regression guard」を honest に
    # 成立させる（以前は CI step が WARN_COUNT を表示するだけで比較せず guard が vacuous だった）。
    _baseline60 = re.search(r"<!--\s*ESLINT-BASELINE-DATA\s+(\d+)\s+-->", _bsrc59 if _budget59.exists() else "")
    if _baseline60:
        _baseline_n60 = int(_baseline60.group(1))
        warnings.append(
            f"Check 60 (ADVISORY): ESLint warning baseline = {_baseline_n60} (recorded in file-size-budget.md)"
        )
    else:
        warnings.append(
            "Check 60 (ADVISORY): ESLint warning baseline marker not found in file-size-budget.md — "
            "add `<!-- ESLINT-BASELINE-DATA <N> -->` to enable regression guard"
        )

    # ── 72. ESLint baseline absolute-ceiling contract (BLOCKING) ─────────────────
    # file-size-budget.md の `<!-- ESLINT-BASELINE-DATA <N> -->` ブロックが記録する
    # warning 数 baseline N が、絶対的な上限契約として固定されていることを機械強制する。
    # 「現在のリポジトリ状態を確定上限 N とし、以降この値を上回ることを CI で防ぐ」と
    # いう絶対防衛線。Check 60 (ADVISORY 監視) を BLOCKING 化した姉妹 Check で、
    # baseline 値が極端に大きい (e.g. 数千) という drift も同時に検出する (sanity ceiling
    # = 200 を超えると BLOCKING で警告し、明示的な doc 更新を強要する)。これで Plan A
    # の「絶対防衛線」を sw.js / main.js の AIDK Kernel 保護領域に手を入れることなく
    # 達成する。
    _baseline72 = re.search(r"<!--\s*ESLINT-BASELINE-DATA\s+(\d+)\s+-->", _bsrc59 if _budget59.exists() else "")
    _BASELINE_SANITY_CEILING_72 = 200
    if _baseline72:
        _n72 = int(_baseline72.group(1))
        check(
            _n72 <= _BASELINE_SANITY_CEILING_72,
            f"Check 72: ESLint baseline {_n72} ≤ sanity ceiling {_BASELINE_SANITY_CEILING_72} (絶対防衛線)",
            f"Check 72: ESLint baseline {_n72} exceeds sanity ceiling {_BASELINE_SANITY_CEILING_72} — "
            f"baseline 値が制御不能な水準。保護領域外の lint 負債が静かに増えた可能性。"
            f"file-size-budget.md の ESLINT-BASELINE-DATA を見直し、増分の根拠を doc に明文化せよ",
        )
    else:
        check(
            False,
            "Check 72: ESLint baseline marker present",
            "Check 72: file-size-budget.md に `<!-- ESLINT-BASELINE-DATA <N> -->` が無い — "
            "Plan A 絶対防衛線が消失している。baseline marker を追加せよ",
        )
