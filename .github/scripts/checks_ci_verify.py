"""
checks_ci_verify.py — CI verification-chain wiring checks — verify layers / consistency guard / behavior e2e gate (345-347)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  345. The package.json `verify` aggregate script MUST chain ALL four
       verification layers: `check`, `lint:css`, `lint`, `lint:js` (each
       referenced as an `npm run <name>`). `verify` is the primary gate
       run before every delivery (CLAUDE.md §5). Dropping one `&& npm run
       <layer>` link silently disables a whole verification layer in the
       aggregate — e.g. losing `lint:css` stops CSS linting from running
       under `npm run verify` while `verify` still exits 0, a classic
       vacuous-gate drift. Sibling of Check 46 (lint JS coverage) /
       Check 50b (flat-config lint invocation) for the verify-chain
       completeness axis. (BLOCKING)

  346. `.github/workflows/architecture-validation.yml` MUST invoke
       `python3 .github/scripts/check_repository_consistency.py` in a
       `run:` step. This is the meta-guard that protects the guard itself:
       the entire consistency suite (300+ Checks) only gates PRs because
       CI runs this one line. Deleting or commenting it out silently
       disables EVERY consistency Check at once while CI still goes green —
       the ultimate vacuous-gate. Sibling of Check 55 (CI lint-target
       coupling) / Check 345 (verify-chain completeness) for the
       CI-invokes-the-guard axis. (BLOCKING)

  347. `.github/workflows/playwright-regression.yml` MUST invoke the
       behavior e2e (`playwright test ... --grep-invert "screenshot
       regression"`) in a `run:` step, AND that step MUST NOT be marked
       `continue-on-error` (it is the BLOCKING functionality gate per
       Session Record #20 §3B). Drift = removing the behavior invocation
       OR flipping its step to `continue-on-error: true` silently turns
       the functionality gate advisory — every route-renders / no-fatal
       assertion stops blocking merges while CI stays green. Check 142
       guards the paths filter but not the invocation itself. This is the
       behavior-gate twin of Check 346 (consistency-gate). Sibling of
       Check 142 (e2e toolchain coverage) / Check 346 (CI invokes the
       consistency guard) for the CI-invokes-the-guard axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 345. package.json verify chains all 4 verification layers (BLOCKING) ─────
    _pkg345 = ROOT / "package.json"
    if _pkg345.is_file():
        try:
            _pj345 = json.loads(_pkg345.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _pj345 = None
        if _pj345 is not None:
            _verify345 = str(_pj345.get("scripts", {}).get("verify", ""))
            _required_layers345 = ("check", "lint:css", "lint", "lint:js")
            _missing345: list[str] = []
            for _layer in _required_layers345:
                # `npm run <layer>` を単語境界で厳密検出 (lint と lint:css/lint:js の誤検出を防ぐ)
                if not re.search(rf"npm run {re.escape(_layer)}(?![:\w])", _verify345):
                    _missing345.append(_layer)
            _ok345 = not _missing345
            check(
                _ok345,
                f"Check 345: package.json verify が全 4 検証層を連結 ({_verify345!r})",
                (f"Check 345: verify チェーンに欠落: {_missing345!r} — "
                 "verify は delivery 前の主要 gate。1 link 欠落で該当検証層が "
                 "npm run verify で silent に skip される vacuous-gate drift。"
                 "`&& npm run <layer>` を復元せよ"),
                blocking=True,
            )
        else:
            check(False, "Check 345: package.json parseable",
                  "Check 345: package.json が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 345: package.json present",
              "Check 345: package.json が無い", blocking=True)

    # ── 346. CI workflow invokes the consistency guard itself (BLOCKING) ─────────
    # meta-guard: 全 consistency Check が PR を gate するのは CI がこの 1 行を走らせる
    # からのみ。この invocation が消えると全 Check が silent に無効化される。
    _wf346 = ROOT / ".github" / "workflows" / "architecture-validation.yml"
    if _wf346.is_file():
        _wsrc346 = _wf346.read_text(encoding="utf-8")
        # コメント行 (# で始まる) を除外して実 run: step の invocation を探す
        _run_lines346 = [
            _ln for _ln in _wsrc346.splitlines()
            if "check_repository_consistency.py" in _ln
            and not _ln.lstrip().startswith("#")
        ]
        _invokes346 = any(
            re.search(r"python3?\s+\.github/scripts/check_repository_consistency\.py", _ln)
            for _ln in _run_lines346
        )
        check(
            _invokes346,
            "Check 346: architecture-validation.yml が check_repository_consistency.py を実行",
            "Check 346: architecture-validation.yml に consistency guard の invocation "
            "(`python3 .github/scripts/check_repository_consistency.py` の run: step) が無い — "
            "全 consistency Check が silent に無効化される ultimate vacuous-gate。invocation を復元せよ",
            blocking=True,
        )
    else:
        check(False, "Check 346: architecture-validation.yml present",
              "Check 346: architecture-validation.yml が無い", blocking=True)

    # ── 347. CI behavior e2e gate is invoked AND blocking (BLOCKING) ─────────────
    # meta-guard (behavior-gate 版): behavior e2e が実行され、かつ continue-on-error
    # でない (= BLOCKING) ことを守る。Check 346 の consistency-gate 版に対する双子。
    _pwf347 = ROOT / ".github" / "workflows" / "playwright-regression.yml"
    if _pwf347.is_file():
        _lines347 = _pwf347.read_text(encoding="utf-8").splitlines()
        _behavior_run_idx347 = -1
        for _i, _ln in enumerate(_lines347):
            if _ln.lstrip().startswith("#"):
                continue
            if ("playwright test" in _ln
                    and 'grep-invert "screenshot regression"' in _ln):
                _behavior_run_idx347 = _i
                break
        _problems347: list[str] = []
        if _behavior_run_idx347 < 0:
            _problems347.append("behavior e2e invocation (grep-invert screenshot regression) が無い")
        else:
            # behavior run 行から step 先頭 (- name:) まで遡り、その間に
            # continue-on-error: true が無いことを確認 (= BLOCKING step)。
            _j = _behavior_run_idx347
            while _j >= 0 and "- name:" not in _lines347[_j]:
                if re.search(r"continue-on-error:\s*true", _lines347[_j]):
                    _problems347.append("behavior step が continue-on-error: true (advisory 化)")
                _j -= 1
        _ok347 = not _problems347
        check(
            _ok347,
            "Check 347: playwright-regression.yml が behavior e2e を BLOCKING gate として実行",
            (f"Check 347: behavior gate drift: {_problems347!r} — "
             "behavior e2e invocation の除去 or continue-on-error 化で機能性 gate が "
             "silent に advisory 化 (route-renders / no-fatal assertion が merge を "
             "gate しなくなる)。BLOCKING invocation を復元せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 347: playwright-regression.yml present",
              "Check 347: playwright-regression.yml が無い", blocking=True)
