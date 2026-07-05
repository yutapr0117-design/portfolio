"""
checks_behavioral.py — shipped-JS behavioral regression guards
(extracted from check_repository_consistency.py — check.py split track・category "behavioral guards").

This module owns the contiguous cluster of Checks 128-131 that statically enforce shipped-JS
runtime UX invariants discovered from real bugs: command-palette ↔ router app-route coherence
(128), topbar data-action button double-fire guard (129), live-input oninput focus-loss guard
(130, via brace-balance parsing of oninput handlers), and service-worker decodeURIComponent
try/catch guard (131). Each Check reads its own shipped-JS target files directly (js/*.js,
main.js, sw.js) via Path.read_text(); none depends on the monolith's global html/style/mainjs
content, so the cluster is self-contained and needs no ctx enrichment. Check 130's brace-parser
uses generic scratch locals (_i/_j/_h/_depth/_nl/…) that are reassigned before use within the
section, so relocating them is behavior-preserving.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  128. Command palette ↔ router app-route coherence: the command palette (js/command-palette.js)
       advertises itself as cross-cutting quick-nav, so every built-in app the router can route to
       (`apps/<app>` — the whitelist in js/router.js: task/todo/pomodoro/ai/notes) must have a
       matching `hash: 'apps/<app>'` destination in the palette's NAV list. Without this, an app
       added to the router but forgotten in the palette becomes unreachable via Cmd/Ctrl+K (exactly
       how the Markdown notes app was missing until this Check was added). The router's app
       whitelist is parsed as the source of truth so the palette can never silently fall behind it.
       (BLOCKING)
  129. Topbar data-action button double-fire guard: the topbar buttons menuBtn / themeBtnTop /
       bgm-btn-top carry `data-action` attributes that the AIDK ActionDelegator handles via a single
       delegated document click listener. main.js init MUST NOT ALSO attach a direct
       `addEventListener('click', ...)` to these buttons — doing so makes a single click fire the
       handler twice (the confirmed bug: theme advanced two steps per click skipping a theme; the
       mobile drawer opened twice, corrupting __lockBodyScroll's saved scrollY to 0 so closing it
       jumped the page to the top; BGM toggled twice). This Check asserts main.js contains no direct
       click-listener wiring for any of the three delegated topbar button ids, locking the
       single-source (ActionDelegator) contract so the double-fire class cannot return. (BLOCKING)
  130. Live-input oninput focus-loss guard: an `oninput:` handler in shipped JS must NOT call
       `State.update(` — State.update → notify → State.subscribe(render) clears #content and
       rebuilds the whole page, destroying the focused input on every keystroke (the confirmed bug
       that made the quiz search and Markdown notes inputs unusable: only the first char landed
       before focus was lost). High-frequency live inputs must persist via `State.updateSilently(`
       (no re-render) and update their own sub-DOM manually (cf. ProjectsPage renderGrid). This
       Check brace-balances each oninput handler body and fails if it contains a `State.update(`
       call (updateSilently is allowed — the literal `State.update(` does not match
       `State.updateSilently(`), structurally guarding the whole class beyond the per-input e2e
       tests. (BLOCKING)
  131. Service-worker decodeURIComponent guard: sw.js intercepts EVERY fetch and runs every
       request's pathname through normalizePath → decodeURIComponent, which throws a URIError on a
       malformed percent-escape (e.g. '/portfolio/%'). Without a guard, such a request makes the SW
       fetch handler throw — an uncaught error inside the service worker on a hot path that touches
       all requests (the bug fixed in the sw normalize hardening). This Check asserts sw.js's
       normalizePath wraps decodeURIComponent in a try/catch so a malformed URL can never throw out
       of the SW. The fix had no e2e/Check guard (service workers are hard to e2e), so this static
       presence check is its regression guard. (BLOCKING)
"""
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 128. Command palette ↔ router app-route coherence (BLOCKING) ───────────────
    # command-palette (js/command-palette.js) は「横断 quick-nav」を標榜するため、router
    # (js/router.js) が route できる全 built-in app (`apps/<app>` = router の whitelist
    # task/todo/pomodoro/ai/notes) に対応する `hash: 'apps/<app>'` destination を NAV に持た
    # ねばならない。router に app を足して palette を更新し忘れると Cmd/Ctrl+K からその app へ
    # 到達できなくなる (実際 Markdown notes app が本 Check 追加まで NAV から欠落していた)。
    # router の app whitelist を source of truth として parse し、palette が silent に遅れない
    # ことを機械強制する。
    _router128 = ROOT / "js" / "router.js"
    _palette128 = ROOT / "js" / "command-palette.js"
    if _router128.exists() and _palette128.exists():
        _router_src128 = _router128.read_text(encoding="utf-8")
        _palette_src128 = _palette128.read_text(encoding="utf-8")
        # router の app whitelist: `['task', 'todo', 'pomodoro', 'ai', 'notes'].includes(app)`
        _wl_m128 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _router_src128)
        _apps128 = []
        if _wl_m128:
            _apps128 = re.findall(r"['\"]([a-z]+)['\"]", _wl_m128.group(1))
        _missing128 = [a for a in _apps128
                       if (f"apps/{a}'" not in _palette_src128 and f'apps/{a}"' not in _palette_src128)]
        check(
            bool(_apps128) and not _missing128,
            f"Check 128: command-palette NAV が router の全 {len(_apps128)} built-in app ({', '.join(_apps128)}) を網羅",
            f"Check 128: command-palette NAV に router app route が欠落: {_missing128} — "
            f"`{{ label: '...', hash: 'apps/<app>' }}` を NAV へ追加せよ (Cmd+K で到達不能になる)"
            if _apps128 else
            "Check 128: router.js の app whitelist (`[...].includes(app)`) を parse できない — coherence 検証が無効化された",
            blocking=True,
        )
    else:
        check(False, "Check 128: router.js / command-palette.js present",
              "Check 128: router.js または command-palette.js が見つからない — palette↔router coherence を検証できない", blocking=True)

    # ── 129. Topbar data-action button double-fire guard (BLOCKING) ────────────────
    # topbar の menuBtn / themeBtnTop / bgm-btn-top は data-action を持ち AIDK ActionDelegator が
    # 単一の delegated click リスナーで処理する。main.js init がこれらに直接 addEventListener('click')
    # も付けると 1 クリックで二重発火する (theme が 2 段送り / drawer 二重 open で scroll 復元が先頭
    # ジャンプ / BGM 二重 toggle の実バグだった)。本 Check は main.js にこれら 3 ボタンへの直接 click
    # リスナー配線が無いことを presence-negative で機械強制し、ActionDelegator 単一経路契約を守る。
    _main129 = ROOT / "main.js"
    _TOPBAR_DELEGATED_IDS129 = ["menuBtn", "themeBtnTop", "bgm-btn-top"]
    if _main129.exists():
        _src129 = _main129.read_text(encoding="utf-8")
        _viol129 = []
        for _line129 in _src129.splitlines():
            if "addEventListener('click'" in _line129 or 'addEventListener("click"' in _line129:
                for _id129 in _TOPBAR_DELEGATED_IDS129:
                    if f"'{_id129}'" in _line129 or f'"{_id129}"' in _line129:
                        _viol129.append(_id129)
        check(
            not _viol129,
            "Check 129: main.js は topbar data-action ボタン (menuBtn/themeBtnTop/bgm-btn-top) に直接 click リスナーを付けていない (ActionDelegator 単一経路)",
            f"Check 129: main.js が data-action ボタンに直接 click リスナーを重複登録している: {sorted(set(_viol129))} — "
            "二重発火 (theme 2 段送り / drawer scroll 先頭ジャンプ / BGM 二重 toggle) になるため直接リスナーを撤去し "
            "data-action + ActionDelegator に一本化せよ",
            blocking=True,
        )
    else:
        check(False, "Check 129: main.js present",
              "Check 129: main.js が見つからない — topbar double-fire guard を検証できない", blocking=True)

    # ── 130. Live-input oninput focus-loss guard (BLOCKING) ───────────────────────
    # shipped JS の `oninput:` ハンドラは State.update( を呼んではならない。State.update → notify →
    # State.subscribe(render) が #content を clear して全再描画し、focused input を毎キーストローク破棄
    # するため focus を失う (quiz 検索 / Markdown notes が使用不能だった実バグ)。高頻度 live-input は
    # State.updateSilently( (再描画しない) で永続化し、自前で sub-DOM を更新せよ (cf. ProjectsPage
    # renderGrid)。本 Check は各 oninput ハンドラ本体を brace-balance で抽出し State.update( を含むなら
    # fail する (updateSilently は許可。リテラル "State.update(" は "State.updateSilently(" に一致しない)。
    def _extract_handler_body130(text, start):
        _arrow = text.find("=>", start)
        _fn = text.find("function", start)
        # arrow か function、近い方を本体開始の手掛かりにする (どちらも無ければ空)
        _cands = [c for c in (_arrow, _fn) if c != -1]
        if not _cands:
            return ""
        _h = min(_cands)
        _i = text.find("{", _h)
        # arrow 単一式 (=> expr, 中括弧なし) は次の改行までを本体とみなす
        _arrow_nl = text.find("\n", _h)
        if _i == -1 or (_arrow != -1 and _i > (_arrow_nl if _arrow_nl != -1 else len(text))):
            _nl = text.find("\n", _h)
            return text[_h:_nl if _nl != -1 else len(text)]
        _depth = 0
        _j = _i
        while _j < len(text):
            if text[_j] == "{":
                _depth += 1
            elif text[_j] == "}":
                _depth -= 1
                if _depth == 0:
                    return text[_i:_j + 1]
            _j += 1
        return text[_i:]
    _js130 = sorted((ROOT / "js").rglob("*.js"))
    _viol130 = []
    _oninput_count130 = 0
    for _f130 in _js130:
        _txt130 = _f130.read_text(encoding="utf-8")
        _pos130 = 0
        while True:
            _oi130 = _txt130.find("oninput", _pos130)
            if _oi130 == -1:
                break
            _pos130 = _oi130 + 7
            _oninput_count130 += 1
            _body130 = _extract_handler_body130(_txt130, _oi130)
            if "State.update(" in _body130:
                _viol130.append(str(_f130.relative_to(ROOT)))
    check(
        not _viol130,
        f"Check 130: 全 {_oninput_count130} 個の oninput ハンドラが State.update( を呼ばない (live-input focus-loss 防止)",
        f"Check 130: oninput ハンドラが State.update( を呼んでおり focus-loss を起こす module: {sorted(set(_viol130))} — "
        "State.updateSilently( + sub-DOM 手動更新へ変更せよ (State.update は全再描画で focused input を破棄する)",
        blocking=True,
    )

    # ── 131. Service-worker decodeURIComponent guard (BLOCKING) ───────────────────
    # sw.js は全 fetch を intercept し、各リクエストの pathname を normalizePath→decodeURIComponent に
    # 通す。decodeURIComponent は不正な % エスケープ ('/portfolio/%' 等) で URIError を throw するため、
    # ガード無しだと そうした URL リクエストで SW fetch ハンドラが uncaught error になる (全リクエストを
    # 触る hot path)。本 Check は sw.js の normalizePath が decodeURIComponent を try/catch で囲むことを
    # presence で機械強制する。この修正は e2e/Check ガードが無かった (service worker は e2e 困難) ため、
    # 本静的 presence check がその回帰ガードになる。
    _sw131 = ROOT / "sw.js"
    if _sw131.exists():
        _swsrc131 = _sw131.read_text(encoding="utf-8")
        # normalizePath 関数本体を抽出 (function normalizePath(...) { ... })
        _m131 = re.search(r"function\s+normalizePath\s*\([^)]*\)\s*\{", _swsrc131)
        _ok131 = False
        if _m131:
            # 関数本体を brace-balance で抽出
            _i131 = _swsrc131.index("{", _m131.start())
            _depth131 = 0
            _body131 = ""
            for _k131 in range(_i131, len(_swsrc131)):
                _c131 = _swsrc131[_k131]
                if _c131 == "{":
                    _depth131 += 1
                elif _c131 == "}":
                    _depth131 -= 1
                    if _depth131 == 0:
                        _body131 = _swsrc131[_i131:_k131 + 1]
                        break
            # body に decodeURIComponent があるなら try と catch も同 body 内に存在すること
            if "decodeURIComponent" in _body131:
                _ok131 = ("try" in _body131 and "catch" in _body131)
            else:
                # decodeURIComponent を使わない実装なら throw リスク無し ＝ guard 不要で OK
                _ok131 = True
        check(
            _m131 is not None and _ok131,
            "Check 131: sw.js normalizePath が decodeURIComponent を try/catch でガード (不正 % URL で SW が throw しない)",
            "Check 131: sw.js normalizePath が decodeURIComponent を try/catch で囲んでいない — 不正な % エスケープ URL "
            "('/portfolio/%') で SW fetch ハンドラが URIError を throw する (全リクエストを触る hot path)。try/catch で "
            "raw pathname へフォールバックせよ"
            if _m131 else
            "Check 131: sw.js に normalizePath 関数が見つからない (構造変更の可能性) — decodeURIComponent guard を検証できない",
            blocking=True,
        )
    else:
        check(False, "Check 131: sw.js present",
              "Check 131: sw.js が見つからない — SW decodeURIComponent guard を検証できない", blocking=True)
