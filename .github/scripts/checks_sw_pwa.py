"""
checks_sw_pwa.py — service-worker & PWA registration + potentialAction structure checks (251-254)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  251. JSON-LD `potentialAction` block has required `@type` + `target`:
       every `potentialAction` block in index.html static JSON-LD MUST
       have a non-empty `@type` (Schema.org Action subclass — e.g.
       ReadAction / SearchAction) AND a `target` field (URL string or
       array). Drift would silently break AI/voice assistant action
       invocation. Sibling of Check 209 (target canonical prefix) for
       the potentialAction required-fields axis. (BLOCKING)

  252. sw.js registers `install` + `activate` + `fetch` event handlers:
       service-worker code MUST register all 3 event listeners. Drift
       (silent removal of any) breaks SW lifecycle (no install → no
       cache prefill, no activate → no cleanup, no fetch → no offline /
       SWR). Sibling of Check 19 (CACHE_NAME version) for the SW
       lifecycle handler presence axis. (BLOCKING)

  253. main.js registers `navigator.serviceWorker.register('./sw.js'`:
       main.js MUST contain a `navigator.serviceWorker.register('./sw.js'`
       call. Silent removal would mean sw.js exists but never installs
       on visiting browsers — Check 252 confirms the SW has handlers, but
       without registration the SW is dead code. Sibling of Check 252
       (SW handlers) for the SW registration call-site axis. (BLOCKING)

  254. .well-known/index.json skill name uniqueness + digest format:
       every entry in `.well-known/index.json` `skills[]` MUST satisfy:
       (a) non-empty `name` field, all unique within the file;
       (b) `digest` field matches `^sha-256:[0-9a-f]{64}$`. Drift would
       silently break agent-skills discovery (duplicate name causes
       conflict, malformed digest causes mismatch). Sibling of Check 5
       (.well-known/index.json byte-identical mirror) for the schema
       structural validity axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 251. JSON-LD potentialAction has required @type + target (BLOCKING) ───────
    # index.html JSON-LD の全 `potentialAction` block が `@type` (Schema.org Action
    # subclass) AND `target` を持つことを BLOCKING 強制。drift で AI/voice assistant の
    # action invocation 破壊。Check 209 (target canonical prefix) の required-fields 軸。
    _idx251 = ROOT / "index.html"
    if _idx251.exists():
        _isrc251 = _idx251.read_text(encoding="utf-8")
        _blocks251 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc251,
            flags=re.DOTALL,
        )
        _violations251: list[str] = []
        _pa_count251 = 0
        def _walk251(node: object, path: str) -> None:
            nonlocal _pa_count251
            if isinstance(node, dict):
                for k, v in node.items():
                    if k == "potentialAction":
                        if isinstance(v, dict):
                            _pa_count251 += 1
                            if not isinstance(v.get("@type"), str) or not v.get("@type", "").strip():
                                _violations251.append(f"{path}.potentialAction @type 欠落/空")
                            if "target" not in v:
                                _violations251.append(f"{path}.potentialAction target 欠落")
                        elif isinstance(v, list):
                            for _i, _it in enumerate(v):
                                _pa_count251 += 1
                                if not isinstance(_it, dict):
                                    _violations251.append(f"{path}.potentialAction[{_i}] non-dict")
                                    continue
                                if not isinstance(_it.get("@type"), str) or not _it.get("@type", "").strip():
                                    _violations251.append(f"{path}.potentialAction[{_i}] @type 欠落/空")
                                if "target" not in _it:
                                    _violations251.append(f"{path}.potentialAction[{_i}] target 欠落")
                    if isinstance(v, list):
                        for item in v:
                            _walk251(item, f"{path}.{k}")
                    else:
                        _walk251(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk251(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks251):
            try:
                _data251 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk251(_data251, f"block{_bi}")
        _ok251 = _pa_count251 > 0 and not _violations251
        check(
            _ok251,
            f"Check 251: potentialAction {_pa_count251} block 全て @type + target 保有",
            (f"Check 251: 違反: {_violations251!r} — AI/voice assistant action invocation 破壊。"
             "@type (Schema.org Action subclass) + target を付与せよ"
             if _violations251 else
             "Check 251: potentialAction 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 251: index.html present",
              "Check 251: index.html が無い", blocking=True)

    # ── 252. sw.js registers install + activate + fetch handlers (BLOCKING) ───────
    # sw.js が install / activate / fetch 3 event handler を全て登録することを
    # BLOCKING 強制。silent 欠落で SW lifecycle 破壊 (precache 不能 / cleanup 不能 /
    # offline+SWR 不能)。Check 19 (CACHE_NAME version) の SW handler presence 軸。
    _sw252 = ROOT / "sw.js"
    if _sw252.exists():
        _ssrc252 = _sw252.read_text(encoding="utf-8")
        _required_evts252 = ["install", "activate", "fetch"]
        _missing252: list[str] = []
        for _e in _required_evts252:
            _pat = re.compile(
                r'(?:self|globalThis)\s*\.\s*addEventListener\s*\(\s*[\'"]' + re.escape(_e) + r'[\'"]'
            )
            if not _pat.search(_ssrc252):
                _missing252.append(_e)
        _ok252 = not _missing252
        check(
            _ok252,
            f"Check 252: sw.js registers {_required_evts252!r} handlers (all 3)",
            (f"Check 252: missing SW handlers: {_missing252!r} — SW lifecycle 破壊 "
             "(precache/cleanup/offline 不能)。self.addEventListener で 3 event 全登録"),
            blocking=True,
        )
    else:
        check(False, "Check 252: sw.js present",
              "Check 252: sw.js が無い", blocking=True)

    # ── 253. main.js calls navigator.serviceWorker.register('./sw.js' (BLOCKING) ──
    # main.js が `navigator.serviceWorker.register('./sw.js'` を呼ぶことを BLOCKING
    # 強制。silent 欠落で sw.js handler は存在しても install されず offline+SWR 機能
    # 全停止。Check 252 (handler presence) の register call-site 軸。
    _main253 = ROOT / "main.js"
    if _main253.exists():
        _msrc253 = _main253.read_text(encoding="utf-8")
        _has253 = re.search(
            r"navigator\s*\.\s*serviceWorker\s*\.\s*register\s*\(\s*['\"]\./sw\.js['\"]",
            _msrc253,
        ) is not None
        check(
            _has253,
            "Check 253: main.js が navigator.serviceWorker.register('./sw.js'...) を呼ぶ",
            ("Check 253: main.js に navigator.serviceWorker.register('./sw.js') 呼び出しが無い — "
             "sw.js handlers (Check 252) は存在しても install されず offline+SWR 停止。"
             "main.js の SW 登録 call-site を復元せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 253: main.js present",
              "Check 253: main.js が無い", blocking=True)

    # ── 254. .well-known/index.json skill name uniqueness + digest format (BLOCKING) ─
    # .well-known/index.json の skills[] 各 entry の name が非空+block 内 unique で、
    # digest が `sha-256:<64-hex>` regex に一致することを BLOCKING 強制。Check 5
    # (byte-identical mirror) の schema structural validity 軸。
    _widx254 = ROOT / ".well-known" / "index.json"
    if _widx254.exists():
        try:
            _wd254 = json.loads(_widx254.read_text(encoding="utf-8"))
        except json.JSONDecodeError as _e254:
            _wd254 = None
        _skills254 = _wd254.get("skills", []) if isinstance(_wd254, dict) else []
        _bad254: list[str] = []
        _names254: list[str] = []
        _digest_re254 = re.compile(r"^sha-256:[0-9a-f]{64}$")
        for _i, _s in enumerate(_skills254):
            if not isinstance(_s, dict):
                _bad254.append(f"skills[{_i}]: non-dict")
                continue
            _nm = _s.get("name")
            if not isinstance(_nm, str) or not _nm.strip():
                _bad254.append(f"skills[{_i}]: name 欠落/空")
            else:
                _names254.append(_nm)
            _dg = _s.get("digest")
            if not isinstance(_dg, str) or not _digest_re254.match(_dg):
                _bad254.append(f"skills[{_i}].digest={_dg!r} format 不正 (sha-256:<64-hex>)")
        from collections import Counter as _Counter254
        _dupes254 = [n for n, c in _Counter254(_names254).items() if c > 1]
        if _dupes254:
            _bad254.append(f"name 重複: {_dupes254!r}")
        _ok254 = len(_skills254) > 0 and not _bad254
        check(
            _ok254,
            f"Check 254: .well-known/index.json skills ({len(_skills254)} 件) 全て name 一意 + digest 形式正",
            (f"Check 254: 違反: {_bad254!r} — agent-skills discovery 破壊。"
             "name 一意 + digest=sha-256:<64-hex> へ整理"
             if _bad254 else
             "Check 254: .well-known/index.json skills 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 254: .well-known/index.json present",
              "Check 254: .well-known/index.json が無い", blocking=True)
