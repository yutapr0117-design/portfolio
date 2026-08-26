"""
checks_behavioral.py — shipped-JS behavioral regression guards
(extracted from check_repository_consistency.py — check.py split track・category "behavioral guards").

This module owns the cluster of Checks 128-131 (plus 373, 374, 382) that statically enforce shipped-JS
runtime UX invariants discovered from real bugs: command-palette ↔ router app-route coherence
(128), topbar data-action button double-fire guard (129), live-input oninput focus-loss guard
(130, via brace-balance parsing of oninput handlers), service-worker decodeURIComponent
try/catch guard (131), and store default-appsData field ⟹ normalizeAppsData preserve round-trip
(373, guarding the producer/consumer persist drift that silently dropped quizSearch on reload),
and settings-io importJSON normalize-before-adopt ingestion guard (374, keeping raw external JSON
from reaching render — the ingestion counterpart of 130).
Each Check reads its own shipped-JS target files directly (js/*.js,
main.js, sw.js) via Path.read_text(); none depends on the monolith's global html/style/mainjs
content, so the cluster is self-contained and needs no ctx enrichment. Check 130's brace-parser
uses generic scratch locals (_i/_j/_h/_depth/_nl/…) that are reassigned before use within the
section, so relocating them is behavior-preserving.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  128. Command palette ↔ router app-route bijection: the command palette (js/command-palette.js)
       advertises itself as cross-cutting quick-nav, so its `hash: 'apps/<app>'` NAV entries and the
       router's app whitelist (js/router.js: task/todo/pomodoro/ai/notes) must agree in BOTH
       directions. (a) missing (router - palette) — an app added to the router but forgotten in the
       palette becomes unreachable via Cmd/Ctrl+K (how the Markdown notes app was missing until this
       Check). (b) extra (palette - router) — a NAV entry for an app the router does not whitelist
       navigates to apps/<app> → not-found = a dead 404 Cmd+K entry (the old one-directional Check
       passed this direction silently, #788 AppsPage bijection class). The router whitelist is parsed
       as source of truth and set-equality with the palette apps is asserted. (BLOCKING)
  129. Topbar data-action button double-fire guard: the topbar buttons menuBtn / themeBtnTop /
       bgm-btn-top carry `data-action` attributes that the AIDK ActionDelegator handles via a single
       delegated document click listener. main.js init MUST NOT ALSO attach a direct
       `addEventListener('click', ...)` to these buttons — doing so makes a single click fire the
       handler twice (the confirmed bug: theme advanced two steps per click skipping a theme; the
       mobile drawer opened twice, corrupting __lockBodyScroll's saved scrollY to 0 so closing it
       jumped the page to the top; BGM toggled twice). This Check asserts main.js contains no direct
       click-listener wiring for any of the three delegated topbar button ids, locking the
       single-source (ActionDelegator) contract so the double-fire class cannot return. (BLOCKING)
  425. data-action ↔ onclick の併存禁止 (Check 129 の一般化): `data-action` を持つ要素は AIDK
       ActionDelegator が **単一の delegated click リスナー**で処理する。同じ要素に `onclick:` も
       付けると 1 クリックで **必ず二重発火**する (#262 の実バグ = theme が 2 段送り / drawer 二重
       open で scroll 復元が先頭ジャンプ / BGM 二重 toggle)。Check 129 は **main.js の topbar 3 ボタン
       だけ**を見ているため、他の shipped JS で同じ形を書いても素通りする。実際 BGM は topbar が
       delegation・sidebar/drawer が onclick 直付けという 2 系統で配線されており、片方に他方を
       足した瞬間に二重発火する状態にある。h() の props を brace-match し、両方を持つ組を禁じる。
       (BLOCKING)
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
       Detection covers BOTH notations and runs on COMMENT-STRIPPED code: the h() prop
       (`oninput: …`) AND `addEventListener('input', …)`. The initial version matched only the
       literal `oninput`, so an equivalent `el.addEventListener('input', e => State.update(…))`
       — the very focus-destroying pattern this Check exists to stop — passed GREEN (measured).
       It also counted `oninput` occurrences inside COMMENTS (8 reported vs 4 real handlers) and
       could mis-analyse the next unrelated function body from a prose mention (measured: a WHY
       comment alone turned an unrelated helper into a violation). Handlers passed by NAME
       (`oninput: handleSearch`) are now resolved to their definition in the same file, and the
       root entry `main.js` is scanned too. Honest limit: handlers defined in another module or
       built dynamically are not followed. (BLOCKING)
  131. Service-worker decodeURIComponent guard: sw.js intercepts EVERY fetch and runs every
       request's pathname through normalizePath → decodeURIComponent, which throws a URIError on a
       malformed percent-escape (e.g. '/portfolio/%'). Without a guard, such a request makes the SW
       fetch handler throw — an uncaught error inside the service worker on a hot path that touches
       all requests (the bug fixed in the sw normalize hardening). This Check asserts sw.js's
       normalizePath wraps decodeURIComponent in a try/catch so a malformed URL can never throw out
       of the SW. The fix had no e2e/Check guard (service workers are hard to e2e), so this static
       presence check is its regression guard. (BLOCKING)
  406. Toast auto-dismiss focus-pause contract: `Toast.show` in js/ui-components.js must pause its
       dismiss timer on `focusin` and resume it on `focusout` (i.e. register both listeners and use
       `clearTimeout`). A toast is removed from the DOM when its duration elapses; if the user has
       tabbed to the close button ("通知を閉じる") at that moment the focused element itself
       disappears and focus falls to `<body>` (measured: activeElement=BODY). In a SPA that means
       the next Tab restarts from the top of the document — the keyboard user loses their place
       (WCAG 2.4.3 Focus Order / 2.2.1 Timing Adjustable). WHY A STATIC CHECK: an e2e for this
       depends on real focus working, but with parallel workers only one page can be the active
       document and on the others focus is reported "inactive" so `focusin` never fires (measured:
       `toBeFocused` fails with `unexpected value "inactive"`; `bringToFront()` does not help; 3 of
       8 parallel repeats RED). A flaky test rots the gate, so the contract is pinned statically
       instead. Comments are stripped before matching. (BLOCKING)
  407. Single-writer contract for the SR announcement channel: the sr-only `#action-announcement`
       region is the ONE channel used to speak to screen readers. Only `announce()` in
       js/ui-components.js may write to it; no other shipped JS may grab it via
       `getElementById('action-announcement')` / `querySelector('#action-announcement')`. Multiple
       writers cause (a) the same content arriving through two paths = double announcement (the real
       Toast bug #901) and (b) bypasses that get left behind when the channel implementation
       changes — exactly what had happened: ai-page.js wrote to the element directly while
       everything else went through Toast. Comments are stripped and ui-components.js itself is
       excluded (it hosts the legitimate writer). (BLOCKING)
  382. Command palette ↔ router static top-level route bijection: Check 128 guards the `apps/<app>`
       app routes; this Check guards the static top-level routes the router resolves (the `case '<name>':`
       labels in js/router.js _parseRoute — projects/apps/settings/about/resume/contact/quiz/
       hiring-risk/ai-knowhow/role-split) against the palette NAV in BOTH directions. (a) missing (router
       - palette) — a newly added static page could silently miss its `hash: '<name>'` entry and become
       unreachable via Cmd/Ctrl+K (the silent-discoverability-loss class of Check 128, added after the
       Markdown notes app went missing). (b) extra (palette - router) — a palette top-level `hash: '<x>'`
       (excluding home '' and the `apps/<x>` routes of Check 128) that is not a router case navigates to
       not-found = a dead 404 Cmd+K entry (the old one-directional Check passed this silently, #788/#789
       bijection class). It parses the router switch case labels and the palette's top-level static hashes
       and asserts set-equality, closing the app-only asymmetry of Check 128 in both directions. (BLOCKING)
  435. quiz の模範解答フォームが作る mailto URL が実行可能な長さに収まる: the quiz contact form
       builds `mailto:?subject=...&body=...` from three maxlength-bounded inputs plus the quiz title.
       Japanese characters percent-encode to 9 bytes each, so the URL grows ~9x faster than the
       character count suggests. Windows truncates mailto invocation at roughly 2,048 characters —
       past that the body is silently cut or the mail client never opens, and **the user is told
       nothing**. The bounds were chosen in #1082 by measuring the worst case, but nothing enforced
       the result: measured 2026-08-20, the longest quiz title ('品質・プロセス問題集') yields
       **2,027** characters — only 21 below the limit. Renaming a quiz title, or raising any
       maxlength, silently crosses it. This Check reconstructs the worst case (every free-text field
       filled with Japanese) for every quiz type and fails if any exceeds the limit. (BLOCKING)
       435b guards this Check's own scope: 435 hardcodes js/quiz-renderer.js, so a **new** mailto
       builder would not be length-checked at all (the scope-drift class of 124 / 411 / 434b).
       The set of shipped JS files that assemble a mailto with an interpolated query string is
       derived and must equal the known set. components.js (ContactPage) is in the set but exempt
       from the length computation because its subject/body are fixed literals — only the
       normalized profile.email varies, so the URL is structurally bounded. A third builder fails
       the Check and forces an explicit decision about whether it is variable-length.

"""
import re
from urllib.parse import quote


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 128. Command palette ↔ router app-route bijection (BLOCKING) ────────────────
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
        # 逆方向 (palette - router): palette NAV の `hash: 'apps/<x>'` が router whitelist に無いと、
        # その NAV は Cmd+K 選択で apps/<x> へ navigate → not-found = 開くと 404 の dead entry
        # (#788 AppsPage bijection と同 class・旧 Check は片側 router⊆palette のみで本方向を素通していた)。
        _palette_apps128 = set(re.findall(r"hash:\s*['\"]apps/([a-z]+)['\"]", _palette_src128))
        _extra128 = sorted(_palette_apps128 - set(_apps128))
        check(
            bool(_apps128) and not _missing128 and not _extra128,
            f"Check 128: command-palette NAV が router の全 {len(_apps128)} built-in app ({', '.join(_apps128)}) と bijection",
            f"Check 128: command-palette NAV が router app whitelist と drift — "
            f"欠落(Cmd+K で到達不能): {_missing128} / 余剰(選択で not-found へ飛ぶ dead entry): {_extra128}。"
            f"NAV の `hash: 'apps/<app>'` を router whitelist と一致させよ "
            f"(欠落は `{{ label: '...', hash: 'apps/<app>' }}` 追加 / 余剰は router 未登録 entry 除去)"
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

    # ── 425. data-action ↔ onclick の併存禁止 (BLOCKING) ──────────────────────────
    # `data-action` を持つ要素は AIDK ActionDelegator が単一の delegated click リスナーで処理する。
    # 同じ要素に `onclick:` も付けると 1 クリックで **必ず二重発火**する (#262 の実バグ)。
    # Check 129 は main.js の topbar 3 ボタンだけを見ているため、他の shipped JS で同じ形を
    # 書いても素通りする。実際 BGM は topbar=delegation / sidebar・drawer=onclick 直付けという
    # 2 系統で配線されており、片方に他方を足した瞬間に二重発火する状態にある。
    # 走査はコメント除去後に h() の props を brace-match して行う (説明コメント中の
    # `onclick:` や `data-action` で誤検出しないため)。
    _JS425 = sorted(list((ROOT / "js").glob("*.js"))) + [ROOT / "main.js"]
    _viol425 = []
    for _f425 in _JS425:
        if not _f425.exists():
            continue
        _src425 = re.sub(r"//.*", "", _f425.read_text(encoding="utf-8"))
        for _m425 in re.finditer(r"h\(\s*['\"][\w-]+['\"]\s*,\s*\{", _src425):
            _i425 = _src425.index("{", _m425.start())
            _depth425 = 0
            _j425 = _i425
            for _j425 in range(_i425, len(_src425)):
                if _src425[_j425] == "{":
                    _depth425 += 1
                elif _src425[_j425] == "}":
                    _depth425 -= 1
                    if _depth425 == 0:
                        break
            _props425 = _src425[_i425:_j425 + 1]
            _hasAction425 = (
                "'data-action'" in _props425
                or '"data-action"' in _props425
                or re.search(r"dataset\s*:\s*\{[^}]*\baction\b", _props425)
            )
            if _hasAction425 and re.search(r"\bonclick\s*:", _props425):
                _viol425.append(f"{_f425.name}: {_props425[:60].replace(chr(10), ' ')}")
    check(
        not _viol425,
        f"Check 425: data-action と onclick を同時に持つ要素は無い ({len(_JS425)} files)",
        f"Check 425: data-action と onclick が併存し 1 クリックで二重発火する: {_viol425[:4]} — "
        "ActionDelegator が delegated に処理するので直接の onclick は撤去せよ "
        "(#262 = theme 2 段送り / drawer scroll 先頭ジャンプ / BGM 二重 toggle の実バグ)",
        blocking=True,
    )

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
    def _code130(_t130):
        """コメントを除去したコードのみを返す。

        [FIX] 旧実装は生テキストから "oninput" を探していたため、**コメント中の言及**まで
        ハンドラとして数え (実測: 実際の oninput prop は 4 個なのに 8 個と報告)、直後の無関係な
        関数本体を誤って解析していた (実測: `// … oninput に渡す` というコメントだけで無関係な
        関数が violation として RED になった)。Check 112/403 と同じ「説明文が Check を狂わせる」class。
        """
        _t130 = re.sub(r"/\*.*?\*/", "", _t130, flags=re.S)
        return re.sub(r"//[^\n]*", "", _t130)

    def _named_body130(_txt, _name):
        """同一 file 内の名前付きハンドラ (function f(){} / const f = () => {}) の本体を返す。"""
        _m = re.search(r"(?:function\s+%s\s*\(|(?:const|let|var)\s+%s\s*=)" % (re.escape(_name), re.escape(_name)), _txt)
        if not _m:
            return ""
        return _extract_handler_body130(_txt, _m.start())

    def _value_expr130(_txt, _pos):
        """`oninput:` の直後の値式を depth 0 の ',' / '}' まで切り出す (名前付き参照の判定用)。"""
        _c = _txt.find(":", _pos)
        if _c == -1:
            return ""
        _i, _depth, _out = _c + 1, 0, []
        while _i < len(_txt):
            _ch = _txt[_i]
            if _ch in "([{":
                _depth += 1
            elif _ch in ")]}":
                if _depth == 0:
                    break
                _depth -= 1
            elif _ch == "," and _depth == 0:
                break
            _out.append(_ch)
            _i += 1
        return "".join(_out).strip()

    # [FIX] 走査対象: js/**.js に加えて root の shipped entry main.js も含める。
    _js130 = sorted((ROOT / "js").rglob("*.js")) + [ROOT / "main.js"]
    _viol130 = []
    _oninput_count130 = 0
    for _f130 in _js130:
        if not _f130.exists():
            continue
        _txt130 = _code130(_f130.read_text(encoding="utf-8"))
        # (1) h() prop 記法: `oninput: ...`
        _pos130 = 0
        while True:
            _oi130 = _txt130.find("oninput", _pos130)
            if _oi130 == -1:
                break
            _pos130 = _oi130 + 7
            _oninput_count130 += 1
            _expr130 = _value_expr130(_txt130, _oi130)
            # 名前付きハンドラ参照 (`oninput: handleSearch`) は同 file 内の定義本体を解決して解析する。
            if re.fullmatch(r"[A-Za-z_$][\w$]*", _expr130):
                _body130 = _named_body130(_txt130, _expr130)
            else:
                _body130 = _extract_handler_body130(_txt130, _oi130)
            if "State.update(" in _body130:
                _viol130.append(str(_f130.relative_to(ROOT)))
        # (2) addEventListener('input', ...) 記法。
        # [FIX] 旧実装は "oninput" リテラルだけを見ており、**同義の addEventListener('input', …) を
        #   丸ごと見逃していた** (実測: `el.addEventListener('input', (e) => { State.update(...) })` を
        #   leaf module に注入しても GREEN のままだった。これは毎キーストローク全再描画で focus を破棄する
        #   実バグそのもの)。
        for _m130 in re.finditer(r"addEventListener\(\s*['\"]input['\"]\s*,", _txt130):
            _oninput_count130 += 1
            _rest130 = _txt130[_m130.end():].lstrip()
            _idm130 = re.match(r"([A-Za-z_$][\w$]*)\s*[),]", _rest130)
            if _idm130:
                _body130 = _named_body130(_txt130, _idm130.group(1))
            else:
                _body130 = _extract_handler_body130(_txt130, _m130.end())
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
            # [vacuous-gate fix] comment/文字列リテラルを除去してから substring 判定する。素の
            # `"try"/"catch" in _body131` は、実 try/catch guard を除去してもコメント (例
            # "かつては try/catch でガード" / "uncaught error のリスク") 内の "try"/"catch" 部分文字列で
            # 満たされ vacuous pass しうる = guard 撤去 (#270 URIError 回帰) を silent 見逃す latent 穴。
            # Check 353/239/373 と同じ comment-strip idiom で実コードに限定する。
            _stripped131 = re.sub(r"/\*.*?\*/", "", _body131, flags=re.DOTALL)
            _stripped131 = re.sub(r"//[^\n]*", "", _stripped131)
            _stripped131 = re.sub(r"'(?:\\.|[^'\\])*'", "''", _stripped131)
            _stripped131 = re.sub(r'"(?:\\.|[^"\\])*"', '""', _stripped131)
            _stripped131 = re.sub(r"`(?:\\.|[^`\\])*`", "``", _stripped131)
            # body に decodeURIComponent があるなら try と catch も同 body 内 (実コード) に存在すること
            if "decodeURIComponent" in _stripped131:
                _ok131 = ("try" in _stripped131 and "catch" in _stripped131)
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

    # ── 406. Toast auto-dismiss focus-pause contract (BLOCKING) ───────────────────
    # toast は duration 経過で DOM ごと削除されるため、閉じるボタン (aria-label='通知を閉じる') に
    # Tab で到達した状態で時間切れになると **フォーカス中の要素ごと消え focus が body へ落ちる**
    # (実測: activeElement=BODY)。SPA では body 落ち = 次の Tab が文書先頭からやり直しとなり操作位置を
    # 失う (WCAG 2.4.3 / 2.2.1)。ゆえに Toast.show は focusin で計時を止め focusout で再開しなければ
    # ならない。**なぜ静的 Check か**: この挙動の e2e は「実 focus が効くこと」に依存するが、並列
    # ワーカーでは 1 ページしか active document になれず非アクティブ側では focus が "inactive" 扱いで
    # focusin が届かない (実測: toBeFocused が `unexpected value "inactive"`・bringToFront でも解消せず
    # 8 回中 3 回 RED)。flaky な e2e は gate を腐らせるため、契約 (listener + clearTimeout) を静的に
    # 固定する方式を選んだ。
    _uic406 = ROOT / "js" / "ui-components.js"
    if _uic406.exists():
        _src406 = re.sub(r"//[^\n]*", "", _uic406.read_text(encoding="utf-8"))
        _has_in406 = re.search(r"addEventListener\(\s*['\"]focusin['\"]", _src406)
        _has_out406 = re.search(r"addEventListener\(\s*['\"]focusout['\"]", _src406)
        _has_clear406 = "clearTimeout(" in _src406
        check(
            bool(_has_in406) and bool(_has_out406) and _has_clear406,
            "Check 406: Toast の自動消滅が focusin で停止し focusout で再開する (フォーカス奪取防止)",
            "Check 406: js/ui-components.js の Toast に focus-pause 契約が無い "
            f"(focusin={bool(_has_in406)} / focusout={bool(_has_out406)} / clearTimeout={_has_clear406}) — "
            "閉じるボタンに Tab で到達した状態で duration が経過すると要素ごと削除され focus が body へ落ちる "
            "(SPA では次の Tab が文書先頭からやり直し = 操作位置の喪失・WCAG 2.4.3)。"
            "focusin で clearTimeout / focusout で再スケジュールを復元せよ",
            blocking=True,
        )
    else:
        check(False, "Check 406: js/ui-components.js present",
              "Check 406: js/ui-components.js が無い — Toast の focus-pause 契約を検証できない", blocking=True)

    # ── 407. SR 通知チャネルの単一 writer 契約 (BLOCKING) ──────────────────────────
    # sr-only の #action-announcement は SR への唯一の通知チャネル。書き込み口が分散すると
    # (a) 同じ内容が複数経路で流れて二重読み上げになる (Toast の実バグ #901)、(b) チャネル実装を
    # 変えたとき取り残される bypass が生まれる (実際 ai-page.js だけ getElementById で直書きしていた)。
    # ゆえに **書き込みは ui-components.js の announce() だけ**に限定し、他の shipped JS が
    # `#action-announcement` を getElementById/querySelector で掴んで textContent を書くことを禁止する。
    # (e2e/テストや comment 内の言及は対象外 — shipped JS のコードのみを見る)
    _uic407 = ROOT / "js" / "ui-components.js"
    _shipped407 = [p407 for p407 in ([ROOT / "main.js"] + sorted((ROOT / "js").glob("*.js"))) if p407.exists()]
    _writers407 = []
    for _f407 in _shipped407:
        if _f407.name == "ui-components.js":
            continue  # announce() 本体が唯一の正当な writer
        _src407 = re.sub(r"//[^\n]*", "", _f407.read_text(encoding="utf-8"))
        if re.search(r"(?:getElementById\(\s*['\"]action-announcement['\"]|querySelector\(\s*['\"]#action-announcement['\"])", _src407):
            _writers407.append(str(_f407.relative_to(ROOT)))
    _has_announce407 = _uic407.exists() and re.search(r"export function announce\s*\(", _uic407.read_text(encoding="utf-8"))
    check(
        bool(_has_announce407) and not _writers407,
        f"Check 407: SR 通知チャネル #action-announcement の writer は announce() のみ ({len(_writers407)} bypass)",
        f"Check 407: #action-announcement へ直接アクセスする shipped JS がある: {_writers407} "
        f"(announce() export={bool(_has_announce407)}) — 書き込み口が分散すると同じ内容が複数経路で流れて "
        "二重読み上げになり (#901)、チャネル実装変更時に取り残される bypass も生まれる。"
        "js/ui-components.js の announce() を factory 経由で注入して使え",
        blocking=True,
    )

    # ── 382. Command palette ↔ router static top-level route bijection (BLOCKING) ─
    # Check 128 は `apps/<app>` の app route のみ palette 網羅を強制する。router (_parseRoute) が
    # switch(parts[0]) で解決する静的 top-level route (case '<name>': = projects/apps/settings/about/
    # resume/contact/quiz/hiring-risk/ai-knowhow/role-split) は palette NAV に対し未強制で、新しい静的
    # ページを router に足して palette への `hash: '<name>'` 追加を忘れると Cmd/Ctrl+K から到達できなく
    # なる (Check 128 と同じ silent-discoverability-loss class の app-only 非対称)。router switch の
    # case ラベルを source of truth として parse し、各々が palette NAV に `hash: '<name>'` を持つことを
    # 機械強制して Check 128 の非対称を閉じる。
    _router382 = ROOT / "js" / "router.js"
    _palette382 = ROOT / "js" / "command-palette.js"
    if _router382.exists() and _palette382.exists():
        _router_src382 = _router382.read_text(encoding="utf-8")
        _palette_src382 = _palette382.read_text(encoding="utf-8")
        # _parseRoute の switch(parts[0]) の `case '<name>':` = 全 top-level 静的 route。
        _cases382 = re.findall(r"case '([a-z][a-z-]*)':", _router_src382)
        _missing382 = [c for c in _cases382
                       if (f"hash: '{c}'" not in _palette_src382 and f'hash: "{c}"' not in _palette_src382)]
        # 逆方向 (palette - router): palette NAV の top-level static hash (空=home と app route `apps/<x>` を
        # 除外) が router switch case に無いと、その NAV は Cmd+K 選択で not-found へ飛ぶ dead entry
        # (#788/#789 の app-route bijection と同 class・旧 Check は片側 router⊆palette のみで本方向を素通)。
        _palette_static382 = set(
            h for h in re.findall(r"hash:\s*['\"]([^'\"]*)['\"]", _palette_src382)
            if h and "/" not in h  # 空 hash='' (home) と apps/<x> (Check 128 の domain) を除外
        )
        _extra382 = sorted(_palette_static382 - set(_cases382))
        check(
            bool(_cases382) and not _missing382 and not _extra382,
            f"Check 382: command-palette NAV が router の全 {len(_cases382)} 静的 top-level route ({', '.join(_cases382)}) と bijection",
            (f"Check 382: command-palette NAV が router 静的 route と drift — "
             f"欠落(Cmd+K で到達不能): {_missing382} / 余剰(選択で not-found へ飛ぶ dead entry): {_extra382}。"
             "NAV の top-level `hash: '<route>'` を router switch case と一致させよ (Check 128 の静的 route 版)")
            if _cases382 else
            "Check 382: router.js の switch case を parse できない — palette↔router 静的 route coherence が無効化された",
            blocking=True,
        )
    else:
        check(False, "Check 382: router.js / command-palette.js present",
              "Check 382: router.js または command-palette.js が見つからない — palette↔router 静的 route coherence を検証できない", blocking=True)

    # ── 435. quiz 模範解答フォームの mailto URL が実行可能な長さに収まる (BLOCKING) ──
    # 日本語は percent-encode で 1 文字 9 バイトになるため、URL は文字数の見た目より
    # 遥かに速く伸びる。Windows の mailto 実行は約 2,048 文字で切られ、**本文が欠けるか
    # メールソフトが開かない silent failure** になる (#1082 で ContactPage 側に同じ規律を
    # 入れた)。上限は #1082 で実測して決めたが **その結果を守る層が無かった**。
    # 実測 (2026-08-20): 最長タイトル「品質・プロセス問題集」で 2,027 文字 = 余裕 21 文字。
    # タイトルを少し変えるか maxlength を上げるだけで silent に超える。
    _qr435 = (ROOT / "js" / "quiz-renderer.js").read_text(encoding="utf-8")
    # [FIX 2026-08-21] タイトルは `{ title: '…', data: … }` の入れ子から **`QUIZ_TITLES` の
    #   フラットな `key: '…'`** へ変わった (データを動的 import で遅延読み込みへ移したため)。
    #   ブロックを限定して拾う —— file 全体を舐めると無関係な文字列まで「タイトル」に数えて
    #   しまい、最長タイトル判定が誤る。
    _tblock435 = re.search(r"const QUIZ_TITLES = \{(.*?)\};", _qr435, re.S)
    _titles435 = re.findall(r"'([^']+)'", _tblock435.group(1)) if _tblock435 else []
    _max435 = {m.group(1): int(m.group(2)) for m in re.finditer(
        r"const (nameInput|emailInput|messageInput) = h\([^;]*?maxlength:\s*(\d+)", _qr435, re.S)}
    _LIMIT435 = 2048
    if _titles435 and len(_max435) == 3:
        _addr435 = "yuta.yokoi.r@gmail.com"  # 最長の実アドレス相当 (profile.email は正規化済)
        _over435 = []
        for _t in _titles435:
            _subj = quote(f"{_t}の模範解答について", safe="")
            _body = quote(
                "お名前: " + "あ" * _max435["nameInput"]
                + "\nメールアドレス: " + "a" * _max435["emailInput"]
                + "\n\nメッセージ:\n" + "あ" * _max435["messageInput"], safe="")
            _len = len(f"mailto:{_addr435}?subject={_subj}&body={_body}")
            if _len > _LIMIT435:
                _over435.append(f"{_t}={_len}")
        check(
            not _over435,
            f"Check 435: quiz {len(_titles435)} 種の mailto 最悪ケース URL が {_LIMIT435} 文字以内",
            (f"Check 435: mailto URL が実行可能な長さを超える: {_over435} (上限 {_LIMIT435})。"
             "日本語は percent-encode で 1 文字 9 バイト。超えると Windows で本文が黙って切られるか "
             "メールソフトが開かず、**利用者には何も伝わらない**。quiz タイトルを短くするか "
             "js/quiz-renderer.js の maxlength を下げよ (#1082 と同じ規律)"),
            blocking=True,
        )
    else:
        check(False, "Check 435: quiz mailto 長",
              f"Check 435: quiz タイトル ({len(_titles435)} 件) か入力の maxlength "
              f"({len(_max435)} 件・3 件必要) を抽出できない — 走査対象が変わったので追従せよ",
              blocking=True)

    # 435b: **この Check 自身の走査対象が漏れないようにする。** 435 は
    # js/quiz-renderer.js を決め打ちで見るので、**新しく mailto を組む面が増えても
    # 気付けない** (Check 124/411/434b と同じ scope-drift class)。
    # 「利用者入力を subject/body へ埋める mailto」を持つ shipped JS の集合を導出し、
    # 既知集合と一致することを強制する。増えたら 435 の計算へその面も足す判断を迫る。
    # 現在の既知集合:
    #   quiz-renderer.js — 3 つの入力欄を埋める = **長さが可変** → 435 が長さを検証する
    #   components.js    — ContactPage。subject/body は**固定文**で、可変なのは
    #                      正規化済み profile.email のみ (実測 578 文字 + アドレス長) →
    #                      構造的に上限内なので 435 の計算対象外
    # 3 つ目が現れたら「可変長か」を判断して 435 へ足すこと。
    _mailto435 = set()
    for _f in sorted(list((ROOT / "js").glob("*.js")) + [ROOT / "main.js"]):
        _src = _f.read_text(encoding="utf-8")
        for _m in re.finditer(r"mailto:[^\n]*subject=", _src):
            _line = _src[_m.start():_src.find("\n", _m.start())]
            # 変数/テンプレート補間を伴うものだけを対象にする (固定文だけなら長さは不変)
            if "${" in _line or "+ subject" in _line or "+ body" in _line:
                _mailto435.add(_f.name)
    check(
        _mailto435 == {"quiz-renderer.js", "components.js"},
        f"Check 435b: mailto を組む面が既知集合と一致 ({sorted(_mailto435)})",
        (f"Check 435b: mailto を組む面の集合が変わった: {sorted(_mailto435)} "
         "(既知は ['components.js', 'quiz-renderer.js'])。Check 435 は quiz-renderer.js を"
         "決め打ちで長さ検証する。新しい面が増えたなら **可変長かを判断し、可変なら 435 の"
         "計算へ足す**こと —— 足さないと "
         "「約 2,048 文字を超えて mailto が silent に失敗する」class を新しい面だけ素通しする"),
        blocking=True,
    )
