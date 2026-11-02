"""
checks_ci_verify.py — CI verification-chain wiring checks — verify layers / consistency guard / behavior e2e gate (345-347, 437, 486-488)
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

  437. install の step timeout が単一ソースから引かれ、mirror doc とも一致する: the behavior
       gate's install step has a `timeout-minutes`, and the failure-attribution step tells the
       reader how many minutes it waited. On 2026-08-20 the attribution message still said
       **8 分** while the actual timeout was **11**: the layer built specifically to prevent
       mis-diagnosing a red CI was itself stating a wrong number, and it is read exactly when
       someone is under pressure. The value now lives once in the job-level env
       `INSTALL_TIMEOUT_MIN`, so message and timeout cannot drift apart. This Check closes the
       remaining surface — the mirror doc's prose — by requiring it to state the same number.
       (BLOCKING)

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
       consistency guard) for the CI-invokes-the-guard axis. **347b**: the ADVISORY
       screenshot step has an `id` and a following step emits `::warning::` when its
       `outcome == 'failure'` — continue-on-error otherwise reports success in the API /
       badge, and on 2026-11-02 the screenshot had failed on every run since at least
       2026-09-10 without anyone seeing it. (BLOCKING)

  486. CI の presence 型 advisory (`grep -q X F || echo "::warning::…"`) は、いまの tree で一致する:
       対象が移ると、この形は黙るのではなく**すべての run で同じ warning を出し続ける**形で壊れる。
       2026-11-02 に、Trusted Types 検査が 2026-05-24 の分割で main.js へ移った policy を index.html に
       探し、5 か月間毎回鳴っていたのを発見した。毎回鳴る警告は本物の警告を読まれなくする。検出は
       実際に grep を同じ引数で走らせて行い、床 4 件で検出自体の vacuous 化も止める。(BLOCKING)

  487. bot が commit するファイルを STATUS 生成器が読むなら、その bot は STATUS.md を同じ commit で
       再生成する: `git push` を持つ workflow の `git add` 対象と、`generate_status.py` の `_read("…")`
       入力が交わるなら、その workflow は generate_status.py を走らせ STATUS.md を add すること。
       2026-11-02 に STATUS.md へ「AIO 監視の実測」(ログ 29 run すべてで測れた query 0 件・バッジは緑)
       を導出して出したことで、週次 aio-monitoring.yml がこの条件に入った。bot の main 直 push は PR
       ゲートを通らず、ずれは次の無関係な PR の Check 121 で初めて赤くなる (#252 と同じ形)。(BLOCKING)

  488. すべての workflow job が `timeout-minutes` を持つ: 2026-11-02 に 8 job 中 3 つ
       (aio-monitoring / architecture-validation / auto-update-aio-digests) に上限が無かった。無いと
       既定の 6 時間まで居座り、concurrency で後続の run を塞ぐ。YAML として読めない workflow と、
       job 検出 5 未満も RED。(BLOCKING)

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
    # 347b: ADVISORY の screenshot は continue-on-error ゆえ失敗しても conclusion が success になり、
    # API / バッジでは見えない (2026-11-02 実測: 少なくとも 2026-09-10 から全 run で失敗していた)。
    # visual step が id を持ち、その outcome が failure のときに ::warning:: を出す step が在ること。
    _wf347b = _pwf347.read_text(encoding="utf-8") if _pwf347.is_file() else ""
    _vid347b = re.search(r"- name: Run visual regression[^\n]*\n\s+id:\s*(\w+)", _wf347b)
    _surf347b = bool(_vid347b) and bool(re.search(
        r"if:[^\n]*steps\." + re.escape(_vid347b.group(1)) + r"\.outcome\s*==\s*'failure'[^\n]*\n"
        r"\s+run:\s*\|\n\s+echo \"::warning", _wf347b))
    check(
        _surf347b,
        "Check 347b: ADVISORY の screenshot の失敗が ::warning:: として表に出る (continue-on-error で見えなくならない)",
        "Check 347b: visual regression step に id が無いか、その outcome が failure のとき ::warning:: を出す step が無い "
        "—— continue-on-error の step は失敗しても success と表示され、advisory が誰にも見えない (2026-11-02 に "
        "少なくとも 2 か月分の失敗が見えていなかった)",
        blocking=True,
    )

    # ── 437. install の step timeout が単一ソース ⟺ mirror doc と一致 (BLOCKING) ──────
    # 2026-08-20: 帰属メッセージだけ「8 分」のまま drift していた (実際は 11)。**赤の誤診を
    # 防ぐために作った層が誤った数値を出す**のは、読まれる場面 (CI が赤いとき) を考えると
    # 特に害が大きい。値は job env `INSTALL_TIMEOUT_MIN` に一本化したので message と
    # timeout は構造的に drift しない。残る面 = mirror doc の散文をここで縛る。
    _wf437 = (ROOT / ".github" / "workflows" / "playwright-regression.yml").read_text(encoding="utf-8")
    _m437 = re.search(r"INSTALL_TIMEOUT_MIN:\s*(\d+)", _wf437)
    _doc437 = (ROOT / "docs" / "files" / ".github" / "workflows"
               / "playwright-regression.yml.md").read_text(encoding="utf-8")
    if _m437:
        _v437 = _m437.group(1)
        _stated = set(re.findall(r"step (?:個別 )?timeout[（(](\d+) 分[)）]", _doc437))
        check(
            _stated and _stated == {_v437},
            f"Check 437: install の step timeout が単一ソース ({_v437} 分) で mirror doc と一致",
            (f"Check 437: mirror doc が述べる install の step timeout {sorted(_stated)} が "
             f"workflow の単一ソース INSTALL_TIMEOUT_MIN={_v437} と一致しない。"
             "この数値は **CI が赤いときに読まれる**ので、古い値は誤診に直結する "
             "(2026-08-20 に帰属メッセージが 8 分のまま drift していた実例)"),
            blocking=True,
        )
    else:
        check(False, "Check 437: INSTALL_TIMEOUT_MIN",
              "Check 437: playwright-regression.yml に INSTALL_TIMEOUT_MIN が無い — "
              "install timeout の単一ソースが失われると message と timeout が再び drift する",
              blocking=True)

    # ── 486. CI の「grep -q X F || echo ::warning」は、いまの tree で一致する (BLOCKING) ──────
    # 2026-11-02: architecture-validation.yml の Trusted Types 検査は index.html に
    # trustedTypes.createPolicy を探していたが、policy は 2026-05-24 の分割で main.js へ移っており、
    # **以後 5 か月間すべての run で同じ warning を出し続けていた**。毎回鳴る警告は「何も起きて
    # いない」と同じ意味になり、本物の警告まで読まれなくする。presence 型の advisory は、対象が
    # 動くと**黙らずに永久に鳴る**形で壊れるので、いま一致することをここで縛る。
    import subprocess as _sp486
    _pat486 = re.compile(
        r"""^\s*grep\s+-q(E?)\s+(?:"([^"]+)"|'([^']+)')\s+(\S+)\s*\|\|\s*echo\s+["']::(?:warning|error)""")
    _seen486, _bad486 = 0, []
    for _wf in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        for _ln in _wf.read_text(encoding="utf-8").splitlines():
            _m = _pat486.match(_ln)
            if not _m:
                continue
            _seen486 += 1
            _args = ["grep", "-q"] + (["-E"] if _m.group(1) else []) + ["--", _m.group(2) or _m.group(3), _m.group(4)]
            if _sp486.run(_args, cwd=ROOT).returncode != 0:
                _bad486.append(f"{_wf.name}: {(_m.group(2) or _m.group(3))} in {_m.group(4)}")
    check(
        _seen486 >= 4 and not _bad486,
        f"Check 486: CI の presence 型 advisory {_seen486} 件がすべていまの tree で一致する (毎回鳴る警告が無い)",
        (f"Check 486: CI の presence 型 advisory が一致しない (={_bad486}) か、検出が {_seen486} 件で床 4 を"
         "下回る。一致しない grep は**すべての run で同じ warning を出し続け**、警告を読む習慣そのものを壊す "
         "(2026-11-02: Trusted Types 検査が main.js へ移った policy を index.html に探し 5 か月鳴り続けていた)。"
         "対象ファイルを実体へ直すか、BLOCKING の Check が既に守っているならその行を消す"),
        blocking=True,
    )

    # ── 487. bot が commit するファイルを STATUS 生成器が読むなら、その bot が STATUS.md も再生成する (BLOCKING) ──
    # 2026-11-02: STATUS.md に「AIO 監視の実測」(ログから導出) を出したので、週次の aio-monitoring.yml が
    # ログだけを commit すると STATUS.md が生成器の出力とずれ、Check 121 が**次の PR**を BLOCKING で
    # 赤くする。bot の main 直 push は PR ゲートを通らないので、ずれは作った run ではなく次の無関係な PR で
    # 初めて見える (#252 の digest desync と同じ形)。生成器の入力は `_read("…")` から導出する。
    _gen487 = ROOT / ".github" / "scripts" / "generate_status.py"
    _inputs487 = set(re.findall(r'_read\("([^"]+)"\)', _gen487.read_text(encoding="utf-8"))) if _gen487.exists() else set()
    _bots487, _bad487 = 0, []
    for _wf in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        _code = "\n".join(_l for _l in _wf.read_text(encoding="utf-8").splitlines()
                          if not _l.lstrip().startswith("#"))
        if "git push" not in _code:
            continue
        _bots487 += 1
        _added = set()
        for _blk in re.findall(r"git add((?:[^\n]*\\\n)*[^\n]*)", _code):
            _added |= {_t for _t in _blk.replace("\\", " ").split() if not _t.startswith("-")}
        _shared = sorted(_added & _inputs487)
        if _shared and not ("generate_status.py" in _code and "STATUS.md" in _added):
            _bad487.append(f"{_wf.name}: {_shared}")
    check(
        len(_inputs487) >= 3 and _bots487 >= 1 and not _bad487,
        f"Check 487: commit する bot workflow {_bots487} 本は、STATUS 生成器の入力 {len(_inputs487)} 件を"
        "書くなら STATUS.md を同じ commit で再生成する",
        (f"Check 487: bot workflow が STATUS 生成器の入力を commit するのに STATUS.md を再生成していない "
         f"({_bad487})、または検出が床を下回る (入力 {len(_inputs487)} / bot {_bots487})。bot の main 直 push は "
         "PR ゲートを通らないので、STATUS.md のずれは次の無関係な PR の Check 121 で初めて赤くなる。"
         "commit step の前で `python3 .github/scripts/generate_status.py` を走らせ、`git add` に STATUS.md を足す"),
        blocking=True,
    )

    # ── 488. すべての workflow job が timeout-minutes を持つ (BLOCKING) ───────────────
    # 2026-11-02: 8 job のうち 3 つ (aio-monitoring / architecture-validation / auto-update-aio-digests)
    # に上限が無かった。無いと GitHub の既定 6 時間まで居座り、concurrency の group で後続の run を
    # 塞ぐ。aio-monitoring は外部 API を待ち、同日に push の再試行 loop も持ったので、ハングの経路が
    # 実在する。値は各 job の実測の 10 倍以上 (秒単位の job に分単位の上限)。
    try:
        import yaml as _y488
    except ImportError:
        _y488 = None
    _jobs488, _bad488 = 0, []
    if _y488 is not None:
        for _wf in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
            try:
                _d = _y488.safe_load(_wf.read_text(encoding="utf-8")) or {}
            except Exception:
                _bad488.append(f"{_wf.name}: YAML として読めない")
                continue
            for _jn, _jv in (_d.get("jobs") or {}).items():
                _jobs488 += 1
                _tm = (_jv or {}).get("timeout-minutes")
                if not (isinstance(_tm, int) and _tm >= 1):
                    _bad488.append(f"{_wf.name}:{_jn}")
    check(
        _y488 is not None and _jobs488 >= 5 and not _bad488,
        f"Check 488: workflow の全 job ({_jobs488}) が timeout-minutes を持つ",
        (f"Check 488: timeout-minutes の無い job がある ({_bad488}) か、job の検出が床 5 を下回る "
         f"({_jobs488}・yaml={'あり' if _y488 else '無し'})。上限の無い job は既定の 6 時間居座り、"
         "concurrency で後続の run を塞ぐ。実測の 10 倍程度の上限を置く"),
        blocking=True,
    )
