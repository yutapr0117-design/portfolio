#!/usr/bin/env python3
"""mutation_probe.py — Safety-net verification via curated source mutations (on-demand meta-QA).

このリポジトリの価値は「機械強制された一貫性 Check + behavior e2e」という安全網そのものである。
本ツールは、その安全網が本当に回帰を捕捉するかを再現可能に検証する completeness-critic である。
過去に実際に修正した bug class を表す curated mutation を 1 つずつソースへ適用し、対応する gate
(check_repository_consistency.py) が確かに RED になる (= 捕捉する) ことを確認して即座に復元する。

- SURVIVED (意図した Check が発火しなかった) な mutation はカバレッジの穴を意味する。
- catch の帰属 (attribution): mutation 適用でその mutation 自身の find-anchor が消えるため
  Check 362 (anchor 解決) は **必ず** RED になる。gate の exit code だけで caught を判定すると
  全 mutation が Check 362 の副作用で自動的に caught になり、probe が何も検証しない vacuous な
  meta-QA と化す。ゆえに caught は「Check 362 以外の error が 1 件以上ある」ことで判定する
  (Check 399 がこの判定の維持を BLOCKING 強制)。
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

import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / ".github" / "scripts" / "check_repository_consistency.py"

# 肥大化解消 (2026-07-04): curated mutation データ (~1,450 行) は mutation_samples.py へ分離。
# 本ファイルは runner (completeness-critic) 専任。増分の追記はデータ側 (mutation_samples.py) に行う。
from mutation_samples import MUTATIONS, E2E_MUTATIONS  # noqa: E402 (ROOT/CHECK 定義後に import)



# [FIX] catch の帰属 (attribution)。mutation を適用すると、その mutation 自身の find-anchor が
# 対象 file から消えるため Check 362 (mutation find-anchor 解決) が **必ず** RED になる。gate の
# exit code だけで「捕捉」を判定すると全 mutation が Check 362 の副作用で自動的に caught となり、
# 本 probe が検証したいはずの「意図した Check が本当に捕捉するか」を一切検証しない vacuous な
# meta-QA と化す (Check 362 導入以降そうなっていた)。実証: どの Check も見ない inert な prose を
# 対象にした対照 mutation で gate は RED になり、その error は Check 362 の 1 件のみだった。
# ゆえに「捕捉」は **Check 362 以外の error が 1 件以上ある** ことで判定する。
ANCHOR_ORPHAN_MARKER = "Check 362:"


def run_gate() -> tuple[int, str]:
    """Run the consistency checker; return (exit code, combined output). 0 = green."""
    r = subprocess.run(
        [sys.executable, str(CHECK)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def caught_by_real_check(out: str) -> bool:
    """True iff the gate reported >=1 error OTHER than the anchor-orphan artifact.

    Check 362 は mutation 適用の副作用で必ず発火するため、これだけを根拠に caught と
    数えてはならない (全 mutation が自動的に caught になり probe が無意味になる)。
    """
    errs = [ln for ln in out.splitlines() if "::error::" in ln]
    return any(ANCHOR_ORPHAN_MARKER not in ln for ln in errs)


def run_e2e_test(pattern: str) -> int:
    """Run a single Playwright behavior test by -g pattern; return exit code (0 = pass/green)."""
    # re.escape ensures test titles with regex metacharacters (e.g. '(?q=)', '+', '.')
    # are treated as literal strings in Playwright's --grep JavaScript regex engine.
    # MUTATION_PROBE=1: playwright.config.cjs がこれを見て serviceWorkers:'block' を有効化する。
    # sw.js の SWR キャッシュが「壊す前」の旧 JS を配信して mutated コードを masking し、mutation を
    # 見逃す false-result を防ぐ (probe を決定的にする)。通常 e2e/CI はこの env を持たず SW 有効のまま。
    # E2E_HERMETIC=1: playwright.config.cjs がこれを見て Chromium の host-resolver-rules で
    # localhost 以外を即 NOTFOUND にする。**probe では通常の CI 以上に重要**で、外部 CDN
    # (KARTE / Google Fonts) の一時的な失敗で test が落ちると、probe はそれを
    # 「mutation を捕捉した」と報告する = **false CAUGHT**。安全網の自己検証そのものが
    # 嘘をつくことになり、しかも週次実行ゆえ誰も rerun しないので気付けない。
    # 実測でも 1 ナビゲーションあたり 6 ホストへ 9 リクエストが飛び goto がそれを待っていた
    # (447ms → 39ms)。probe は e2e を mutation ごとに起動するため所要短縮の効果も大きい。
    # probe は screenshot test を実行しないので、実フォントを要する制約はここには無い。
    probe_env = {**os.environ, "MUTATION_PROBE": "1", "E2E_HERMETIC": "1"}
    r = subprocess.run(
        ["npx", "playwright", "test", "--config=playwright.config.cjs", "-g", re.escape(pattern)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=probe_env,
    )
    return r.returncode


def main() -> int:
    if not CHECK.exists():
        print(f"ERROR: gate not found: {CHECK}")
        return 1

    # baseline: gate は実行前に GREEN でなければ結果が無意味。
    if run_gate()[0] != 0:
        print("ERROR: baseline gate is RED before any mutation — fix the repo first.")
        return 1

    survived: list[str] = []
    drifted: list[str] = []
    crashed: list[str] = []

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
            # 「捕捉」は Check 362 (anchor orphan) 以外の error があることで判定する。
            # exit code だけを見ると mutation 適用の副作用で必ず RED になり全件 caught になる。
            _rc, _out = run_gate()
            if caught_by_real_check(_out):
                print(f"  caught  : {m['name']}")
            elif _rc != 0 and "Traceback (most recent call last)" in _out:
                # gate は RED だが Check ではなく **traceback** で停止した。merge は止まるものの
                # (a) 診断が Python の traceback で actionable でない (b) crash 地点以降の Check が
                # 全て skip され他の drift を masking する — Check としては死んでいる状態。
                crashed.append(m["name"])
                print(f"  CRASHED : {m['name']}  <-- gate が traceback で停止 (Check 未到達)")
            else:
                survived.append(m["name"])
                print(f"  SURVIVED: {m['name']}  <-- COVERAGE GAP")
        finally:
            f.write_text(original, encoding="utf-8")

    # 復元確認: 全 mutation 後に gate が GREEN へ戻ること (ファイルが汚れて残っていないこと)。
    if run_gate()[0] != 0:
        print("\nERROR: gate is RED after restore — source files may be left mutated! Check `git status`.")
        return 1

    print()
    if drifted:
        print(f"{len(drifted)} mutation(s) DRIFTED (anchors missing) — update mutation_probe.py:")
        for d in drifted:
            print(f"  - {d}")
        return 1
    if crashed:
        print(f"{len(crashed)} mutation(s) CRASHED the gate (traceback instead of a Check verdict):")
        for c in crashed:
            print(f"  - {c}")
        return 1
    if survived:
        print(f"{len(survived)} mutation(s) SURVIVED — the safety net has a gap:")
        for s in survived:
            print(f"  - {s}")
        return 1
    print(f"All {len(MUTATIONS)} mutations were caught by the safety net. Net is healthy. ✓")
    return 0


def _parse_shard() -> tuple[int, int]:
    """`--shard i/n` を解析する。未指定は 1/1 (= 全件)。

    分割は `index % n == i-1` の決定的な剰余で行う。連続ブロック分割ではなく剰余にするのは、
    mutation の所要時間が file ごとに偏る (重い e2e が固まっている領域がある) ため、
    剰余の方が各 shard の負荷が均されるから。
    """
    for a in sys.argv:
        if a.startswith("--shard="):
            spec = a.split("=", 1)[1]
        elif a == "--shard":
            idx = sys.argv.index(a)
            spec = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "1/1"
        else:
            continue
        try:
            i, n = spec.split("/")
            i, n = int(i), int(n)
        except (ValueError, IndexError):
            raise SystemExit(f"ERROR: invalid --shard spec {spec!r} (expected i/n)")
        if not (1 <= i <= n):
            raise SystemExit(f"ERROR: --shard {i}/{n} out of range")
        return i, n
    return 1, 1


def e2e_main() -> int:
    """--e2e モード: behavior e2e (Playwright) 安全網の非 vacuous 検証。

    各 mutation を (1) clean で対象テストが pass・(2) mutated で対象テストが fail (= 捕捉) の
    二段で検証する。clean-pass が「常に失敗する壊れたテスト」を、mutated-fail が「mutation を
    素通しする vacuous test」を、それぞれ排除する。slow ゆえ on-demand。
    """
    survived: list[str] = []
    drifted: list[str] = []
    broken: list[str] = []

    # [FIX] **シャーディング**。behavior probe は mutation ごとに Playwright を起動するため
    #   所要時間が mutation 数にほぼ比例する。2026-08-17 に mutation を 240 → 289 件へ増やした
    #   結果、単一ジョブの実測が **55 分 17 秒**となり `timeout-minutes: 55` に到達して
    #   **cancelled** で打ち切られた。cancelled は success でも failure でもないので、
    #   **安全網の自己検証が「結果不明」のまま静かに止まる**最悪の形になる
    #   (しかも週次実行ゆえ誰も rerun しない)。timeout を上げるだけでは mutation を足すたび
    #   同じことが再発するので、`--shard i/n` で分割して wall-clock を n 分の 1 にする。
    #   分割は決定的 (index % n) で、全 shard の和が必ず全 mutation を 1 回ずつ覆う。
    _shard, _shards = _parse_shard()
    _targets = [m for i, m in enumerate(E2E_MUTATIONS) if i % _shards == _shard - 1]

    print(f"mutation-probe (e2e): verifying {len(_targets)}/{len(E2E_MUTATIONS)} behavior mutations "
          f"(shard {_shard}/{_shards}) via Playwright...\n")
    for m in _targets:
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

