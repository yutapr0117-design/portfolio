#!/usr/bin/env python3
"""mutation_probe.py — Safety-net verification via curated source mutations (on-demand meta-QA).

このリポジトリの価値は「機械強制された一貫性 Check + behavior e2e」という安全網そのものである。
本ツールは、その安全網が本当に回帰を捕捉するかを再現可能に検証する completeness-critic である。
過去に実際に修正した bug class を表す curated mutation を 1 つずつソースへ適用し、対応する gate
(check_repository_consistency.py) が確かに RED になる (= 捕捉する) ことを確認して即座に復元する。

- SURVIVED (gate が GREEN のまま) な mutation はカバレッジの穴を意味する。
- 非 vacuous 保証: 各 mutation は適用前に find-anchor の存在を assert する。anchor が消えていれば
  「probe 自身が drift した」と ERROR で報告する (mutation が no-op で偽 "caught" になるのを防ぐ)。
- 安全性: 各 mutation は try/finally で必ず元へ復元し、全実行後に gate が GREEN へ戻ることも確認する。
  CI gate ではなく on-demand ツール (`npm run mutation-probe`)。

二つの安全網それぞれを検証する 2 モード:
- (既定) consistency Check 安全網を検証 — 各 mutation で check_repository_consistency.py が RED 化するか。
- (`--e2e` / `npm run mutation-probe-e2e`) behavior e2e (Playwright) 安全網を検証 — 各 mutation で対応する
  特定の e2e テストが RED 化するか。各 e2e mutation は (1) clean で pass・(2) mutated で fail の二段で
  非 vacuous を実証する。Playwright を起動するため slow ゆえ on-demand 専用。

Exit codes: 0 = 全 mutation を捕捉 (安全網健全) / 1 = SURVIVED あり・probe drift・(e2e) baseline RED・復元失敗のいずれか。
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    # check_repository_consistency.py 等と同様 3.10+ 専用 (PEP 604 等)。明示エラーで早期停止。
    print("ERROR: mutation_probe.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / ".github" / "scripts" / "check_repository_consistency.py"

# 肥大化解消 (2026-07-04): curated mutation データ (~1,450 行) は mutation_samples.py へ分離。
# 本ファイルは runner (completeness-critic) 専任。増分の追記はデータ側 (mutation_samples.py) に行う。
from mutation_samples import MUTATIONS, E2E_MUTATIONS  # noqa: E402 (ROOT/CHECK 定義後に import)



def run_gate() -> int:
    """Run the consistency checker; return its exit code (0 = green)."""
    r = subprocess.run(
        [sys.executable, str(CHECK)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return r.returncode


def run_e2e_test(pattern: str) -> int:
    """Run a single Playwright behavior test by -g pattern; return exit code (0 = pass/green)."""
    # re.escape ensures test titles with regex metacharacters (e.g. '(?q=)', '+', '.')
    # are treated as literal strings in Playwright's --grep JavaScript regex engine.
    r = subprocess.run(
        ["npx", "playwright", "test", "--config=playwright.config.cjs", "-g", re.escape(pattern)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return r.returncode


def main() -> int:
    if not CHECK.exists():
        print(f"ERROR: gate not found: {CHECK}")
        return 1

    # baseline: gate は実行前に GREEN でなければ結果が無意味。
    if run_gate() != 0:
        print("ERROR: baseline gate is RED before any mutation — fix the repo first.")
        return 1

    survived: list[str] = []
    drifted: list[str] = []

    print(f"mutation-probe: applying {len(MUTATIONS)} curated mutations...\n")
    for m in MUTATIONS:
        f: Path = m["file"]
        original = f.read_text(encoding="utf-8")
        if m["find"] not in original:
            drifted.append(m["name"])
            print(f"  DRIFT  : {m['name']} — find-anchor absent (probe needs updating)")
            continue
        try:
            f.write_text(original.replace(m["find"], m["replace"], 1), encoding="utf-8")
            if run_gate() == 0:
                survived.append(m["name"])
                print(f"  SURVIVED: {m['name']}  <-- COVERAGE GAP")
            else:
                print(f"  caught  : {m['name']}")
        finally:
            f.write_text(original, encoding="utf-8")

    # 復元確認: 全 mutation 後に gate が GREEN へ戻ること (ファイルが汚れて残っていないこと)。
    if run_gate() != 0:
        print("\nERROR: gate is RED after restore — source files may be left mutated! Check `git status`.")
        return 1

    print()
    if drifted:
        print(f"{len(drifted)} mutation(s) DRIFTED (anchors missing) — update mutation_probe.py:")
        for d in drifted:
            print(f"  - {d}")
        return 1
    if survived:
        print(f"{len(survived)} mutation(s) SURVIVED — the safety net has a gap:")
        for s in survived:
            print(f"  - {s}")
        return 1
    print(f"All {len(MUTATIONS)} mutations were caught by the safety net. Net is healthy. ✓")
    return 0


def e2e_main() -> int:
    """--e2e モード: behavior e2e (Playwright) 安全網の非 vacuous 検証。

    各 mutation を (1) clean で対象テストが pass・(2) mutated で対象テストが fail (= 捕捉) の
    二段で検証する。clean-pass が「常に失敗する壊れたテスト」を、mutated-fail が「mutation を
    素通しする vacuous test」を、それぞれ排除する。slow ゆえ on-demand。
    """
    survived: list[str] = []
    drifted: list[str] = []
    broken: list[str] = []

    print(f"mutation-probe (e2e): verifying {len(E2E_MUTATIONS)} behavior mutations via Playwright...\n")
    for m in E2E_MUTATIONS:
        f: Path = m["file"]
        original = f.read_text(encoding="utf-8")
        if m["find"] not in original:
            drifted.append(m["name"])
            print(f"  DRIFT  : {m['name']} — find-anchor absent (probe needs updating)")
            continue
        # (1) clean baseline: 対象テストは現行ソースで pass しなければならない (壊れ/flaky 排除)。
        if run_e2e_test(m["test"]) != 0:
            broken.append(m["name"])
            print(f"  BROKEN : {m['name']} — target test '{m['test']}' is RED at baseline (fix/flaky?)")
            continue
        # (2) mutated: 対象テストが fail (= 捕捉) しなければ vacuous。
        try:
            f.write_text(original.replace(m["find"], m["replace"], 1), encoding="utf-8")
            if run_e2e_test(m["test"]) == 0:
                survived.append(m["name"])
                print(f"  SURVIVED: {m['name']}  <-- VACUOUS e2e (mutation 素通し)")
            else:
                print(f"  caught  : {m['name']}")
        finally:
            f.write_text(original, encoding="utf-8")

    print()
    if drifted:
        print(f"{len(drifted)} mutation(s) DRIFTED (anchors missing) — update mutation_probe.py:")
        for d in drifted:
            print(f"  - {d}")
        return 1
    if broken:
        print(f"{len(broken)} target test(s) RED at baseline — investigate before trusting the probe:")
        for b in broken:
            print(f"  - {b}")
        return 1
    if survived:
        print(f"{len(survived)} mutation(s) SURVIVED — the behavior e2e net has a vacuous gap:")
        for s in survived:
            print(f"  - {s}")
        return 1
    print(f"All {len(E2E_MUTATIONS)} behavior mutations were caught by the e2e net. Net is healthy. ✓")
    return 0


if __name__ == "__main__":
    sys.exit(e2e_main() if "--e2e" in sys.argv else main())

