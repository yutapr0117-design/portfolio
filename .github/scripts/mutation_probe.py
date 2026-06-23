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

Exit codes: 0 = 全 mutation を捕捉 (安全網健全) / 1 = SURVIVED あり・probe drift・復元失敗のいずれか。
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    # check_repository_consistency.py 等と同様 3.10+ 専用 (PEP 604 等)。明示エラーで早期停止。
    print("ERROR: mutation_probe.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / ".github" / "scripts" / "check_repository_consistency.py"

# 各 mutation = 過去に修正した実 bug class の再現。find は現行ソースに必ず存在する distinctive 文字列。
MUTATIONS = [
    {
        "name": "Check 45 (docstring↔section bijection): break a section-header number",
        "file": CHECK,
        "find": "# ── 1. ai:version",
        "replace": "# ── 998. ai:version",
    },
    {
        "name": "Check 112a (IME guard): drop !isComposing from an apps Enter handler",
        "file": ROOT / "js" / "apps.js",
        "find": "e.key === 'Enter' && !e.isComposing",
        "replace": "e.key === 'Enter'",
    },
    {
        "name": "Check 129 (topbar double-fire): add a direct menuBtn click listener in main.js",
        "file": ROOT / "main.js",
        "find": "document.getElementById('overlay')?.addEventListener('click', closeDrawer);",
        "replace": (
            "document.getElementById('menuBtn')?.addEventListener('click', openDrawer);\n"
            "            document.getElementById('overlay')?.addEventListener('click', closeDrawer);"
        ),
    },
    {
        "name": "Check 130 (live-input focus-loss): make a notes oninput call State.update",
        "file": ROOT / "js" / "apps.js",
        "find": "State.updateSilently(s => { s.appsData.notes",
        "replace": "State.update(s => { s.appsData.notes",
    },
    {
        "name": "Check 125 (dead-constant): add an unreferenced constant to js/constants.js",
        "file": ROOT / "js" / "constants.js",
        "find": "STORAGE_KEY: 'portfolio_enhanced_v45',",
        "replace": "STORAGE_KEY: 'portfolio_enhanced_v45',\n    PROBE_UNUSED_CONST: 'mutation-probe',",
    },
    {
        "name": "Check 126/50d (ESLint bug-catcher): drop no-dupe-keys from eslint.config.mjs",
        "file": ROOT / "eslint.config.mjs",
        "find": "'no-dupe-keys': 'error',",
        "replace": "'no-dupe-keys-DISABLED': 'error',",
    },
    {
        "name": "Check 131 (SW decode guard): un-guard decodeURIComponent in sw.js normalizePath",
        "file": ROOT / "sw.js",
        "find": "    try {\n        decoded = decodeURIComponent(pathname);\n    } catch {\n        decoded = pathname;\n    }",
        "replace": "    decoded = decodeURIComponent(pathname);",
    },
    {
        "name": "Check 118 (PAGE_META coverage): rename the app-notes PAGE_META key (route loses metadata)",
        "file": ROOT / "js" / "page-meta.js",
        "find": "'app-notes': { title: 'Markdown Notes'",
        "replace": "'app-notes-PROBE': { title: 'Markdown Notes'",
    },
    {
        "name": "Check 111 (e2e no-networkidle): use waitForLoadState('networkidle') in a behavior test",
        "file": ROOT / "e2e" / "portfolio.spec.js",
        "find": "waitForLoadState('domcontentloaded')",
        "replace": "waitForLoadState('networkidle')",
    },
    {
        "name": "Check 114 (e2e no-.only): add test.only (would silently skip the rest of the suite)",
        "file": ROOT / "e2e" / "portfolio.spec.js",
        "find": "test('AIO asset anchor must be hidden",
        "replace": "test.only('AIO asset anchor must be hidden",
    },
    {
        "name": "Check 132 (AIO evidence↔sitemap): drop a registered evidence doc from sitemap.xml",
        "file": ROOT / "sitemap.xml",
        "find": "https://yutapr0117-design.github.io/portfolio/docs/evidence/real-work-claims.md",
        "replace": "https://yutapr0117-design.github.io/portfolio/docs/evidence/real-work-claims-REMOVED.md",
    },
    {
        "name": "Check 133 (AIO guard wiring): remove the aio-guard.js <script> tag from index.html",
        "file": ROOT / "index.html",
        "find": '<script src="./aio-guard.js"></script>',
        "replace": "<!-- aio-guard.js PROBE-REMOVED -->",
    },
    {
        "name": "Check 134 (root script wiring): remove the theme-init.js <script> tag from index.html",
        "file": ROOT / "index.html",
        "find": '<script src="./theme-init.js"></script>',
        "replace": "<!-- theme-init.js PROBE-REMOVED -->",
    },
]


def run_gate() -> int:
    """Run the consistency checker; return its exit code (0 = green)."""
    r = subprocess.run(
        [sys.executable, str(CHECK)],
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


if __name__ == "__main__":
    sys.exit(main())
