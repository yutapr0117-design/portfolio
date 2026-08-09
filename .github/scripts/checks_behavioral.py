"""
checks_behavioral.py — shipped-JS behavioral regression guards
(extracted from check_repository_consistency.py — check.py split track・category "behavioral guards").

This module owns the cluster of Checks 128-131 (plus 373, 374, 382) that statically enforce shipped-JS
runtime UX invariants discovered from real bugs: command-palette ↔ router app-route coherence
(128), topbar data-action button double-fire guard (129), live-input oninput focus-loss guard
(130, via brace-balance parsing of oninput handlers), service-worker decodeURIComponent
try/catch guard (131), and store default-appsData field ⟹ normalizeAppsData preserve round-trip
(373, guarding the producer/consumer persist drift that silently dropped quizSearch on reload),
and settings-page importJSON normalize-before-adopt ingestion guard (374, keeping raw external JSON
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
  373. Store default-appsData field ⟹ normalizeAppsData preserve round-trip: js/store.js
       normalizeAppsData(data) is the choke point every ingestion path (load / import / cross-tab /
       snapshot-restore / settings 正規化) runs through, and it rebuilds appsData from
       deepClone(defaultAppsData) then re-applies each user field from `data.<field>`. If a field
       exists in defaultAppsData (the persisted shape) but normalizeAppsData never reads it back,
       that field is SILENTLY reset to its default on every reload even though callers persist it —
       exactly the confirmed quizSearch bug: QuizPage wrote the search term via
       State.updateSilently(s => s.appsData.quizSearch = val) (which schedules a localStorage save)
       and read it back on init to restore, but normalizeAppsData preserved tasks/todos/pomodoro/ai/
       notes and dropped quizSearch, so the "永続化された検索語を反映" restore silently failed each
       reload (a half-wired persist of the #294/#568 producer/consumer drift class). This Check
       brace-parses defaultAppsData's top-level keys and asserts every one is referenced as
       `data.<key>` inside the normalizeAppsData body (line comments stripped to avoid a comment-only
       vacuous pass), making "a field is persisted ⟹ normalize reads it back" an enforced invariant
       so no future appsData field can be added to the store default yet silently lost on reload.
       (BLOCKING)
  404. Store default-profile field ⟹ validateAndNormalize preserve round-trip: the profile-face
       twin of Check 373 (appsData face). Every top-level key of `defaultProfile` in js/store.js
       must be read back as `data.profile.<key>` inside the `store.profile = { … }` normalisation
       block. validateAndNormalize is the choke point every ingestion path goes through (load /
       import / cross-tab / snapshot-restore / settings normalise); a field that lives in the
       persisted shape but is not read back silently resets to its default on every reload.
       THIS ALREADY HAPPENED: #139 stripped github / linkedin / location so importing them did
       nothing — and the behavior e2e added then only guards those three fields, leaving any
       NEWLY added profile field unprotected. Line comments are stripped so a prose mention
       cannot vacuously satisfy the Check. (BLOCKING)
  405. Store top-level field ⟹ validateAndNormalize preserve round-trip: the top-level face of
       Checks 373 (appsData) and 404 (profile). Every top-level key of the persisted shape
       returned by `createDefaultStore()` must be read back as `data.<key>` inside
       validateAndNormalize. A key that is not read back silently resets to its default on every
       reload — a class that has already produced THREE real bugs here (quizSearch #684, profile
       github/linkedin/location #139, projectPrefs.hiddenIds #294 family). Carve-outs are the
       metadata regenerated by design: `schemaVersion` (stamps the current schema), `type` (fixed
       tag) and `lastModified` (save timestamp). With all three faces enforced, "a field added to
       the persisted shape is always read back" becomes an invariant at every level. Line comments
       are stripped so a prose mention cannot vacuously satisfy it. (BLOCKING)
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
  374. settings-page.js importJSON normalize-before-adopt ingestion guard: importJSON ingests
       external JSON. If it commits the raw parsed data via State.update(...), the notify → render()
       cycle paints un-normalized data (e.g. malformed projects with a null/non-object entry that
       SettingsPage dereferences via p.name/p.id and crashes on). restoreSnapshot already follows the
       established "normalize external input before adopting it" invariant (#295/#561) by committing
       State.set(Store.validateAndNormalize(...)); importJSON must too, rather than relying on the
       incidental render-abort ordering (the second normalize render aborting the first raw render
       before it reaches SettingsPage) for data-safety. This Check brace-parses the importJSON
       function body and asserts it does NOT call State.update( and DOES route through
       validateAndNormalize, structurally preventing re-introduction of raw ingestion that reaches
       render (the ingestion counterpart of Check 130's oninput no-State.update guard). (BLOCKING)
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
  410. UI 入力上限 ⟹ 保存上限の一致 (input/textarea maxlength coherence): a UI-layer shipped JS file
       (one that builds `h('input'` / `h('textarea'` elements) that persists user text via
       `.slice(0, CONSTANTS.LIMITS.<KEY>)` MUST also declare `maxlength: CONSTANTS.LIMITS.<KEY>` for the
       same KEY in the same file. Without it the field accepts more characters than are ever saved, so
       the overflow is dropped silently at persist time. The Markdown notes editor was the severe case:
       the textarea and its live preview kept rendering everything the user typed past NOTES_TEXT
       (20,000) while `State.updateSilently` stored only the truncated prefix — the loss became visible
       only on reload (the silent producer/consumer drift class of #684 quizSearch / #294, here between
       the UI bound and the persistence bound rather than between two data layers). task/todo/ai were the
       same asymmetry but visibly truncated on submit. Deriving both bounds from the one LIMITS constant
       makes "what can be typed" == "what is saved" structural. store.js is excluded automatically since
       it builds no input elements (it is the normalization layer, not a UI layer). (BLOCKING)
"""
import re


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

    # ── 373. Store default-appsData field ⟹ normalizeAppsData preserve round-trip (BLOCKING) ──
    # store.js normalizeAppsData(data) は全 ingestion 経路 (load/import/cross-tab/snapshot-restore/
    # settings 正規化) が通るチョークポイントで、appsData を deepClone(defaultAppsData) から再構築し
    # 各ユーザーフィールドを `data.<field>` から再適用する。あるフィールドが defaultAppsData (永続化
    # される shape) にあるのに normalizeAppsData が読み戻さないと、呼び出し側が永続化していても reload
    # 毎に default へ silent リセットされる — quizSearch の実バグそのもの (QuizPage が updateSilently で
    # 書き込み init で読み戻すのに normalize が tasks/todos/pomodoro/ai/notes だけ preserve し quizSearch
    # を drop していた・#294/#568 と同 producer/consumer drift class)。defaultAppsData の top-level key を
    # brace-parse し、各 key が normalizeAppsData 本体で `data.<key>` として参照されることを強制する
    # (行コメントは除去して「コメントに書いただけ」の vacuous pass を防ぐ)。これで「フィールドが永続化
    # される ⟹ normalize が読み戻す」を invariant 化し、将来 store default に足したフィールドが reload で
    # silent に失われる class を封じる。
    _store373 = ROOT / "js" / "store.js"
    if _store373.exists():
        _src373 = _store373.read_text(encoding="utf-8")

        def _balanced_obj373(text, marker):
            # marker 以降の最初の '{' から brace-balance して中身 (exclusive) を返す。文字列/テンプレートは skip。
            _idx = text.find(marker)
            if _idx == -1:
                return None
            _b = text.find("{", _idx)
            if _b == -1:
                return None
            _depth = 0
            _instr = None
            _k = _b
            while _k < len(text):
                _c = text[_k]
                if _instr:
                    if _c == "\\":
                        _k += 2
                        continue
                    if _c == _instr:
                        _instr = None
                elif _c in "\"'`":
                    _instr = _c
                elif _c == "{":
                    _depth += 1
                elif _c == "}":
                    _depth -= 1
                    if _depth == 0:
                        return text[_b + 1:_k]
                _k += 1
            return None

        def _top_keys373(body):
            # body 内 depth==0 の `key:` を抽出 (ネスト obj/array 内の key は無視)。
            _keys = []
            _depth = 0
            _instr = None
            _at_key = True
            _k = 0
            while _k < len(body):
                _c = body[_k]
                if _instr:
                    if _c == "\\":
                        _k += 2
                        continue
                    if _c == _instr:
                        _instr = None
                    _k += 1
                    continue
                if _c in "\"'`":
                    _instr = _c
                    _k += 1
                    continue
                if _c in "{[(":
                    _depth += 1
                    _k += 1
                    continue
                if _c in "}])":
                    _depth -= 1
                    _k += 1
                    continue
                if _depth == 0 and _c == ",":
                    _at_key = True
                    _k += 1
                    continue
                if _depth == 0 and _at_key and not _c.isspace():
                    _m373 = re.match(r"([A-Za-z_$][\w$]*)\s*:", body[_k:])
                    if _m373:
                        _keys.append(_m373.group(1))
                        _at_key = False
                        _k += _m373.end()
                        continue
                    _at_key = False
                _k += 1
            return _keys

        _default_body373 = _balanced_obj373(_src373, "const defaultAppsData")
        _keys373 = _top_keys373(_default_body373) if _default_body373 else []
        # normalizeAppsData 本体を `function normalizeAppsData` 〜 `return result;` の text region で切り出す
        # (`return result;` は normalizeAppsData 固有。validateAndNormalize は `return store;`)。行コメントは
        # 除去 (この region に `//` を含む文字列 URL は無いため素朴除去で安全)。
        _ns373 = _src373.find("function normalizeAppsData")
        _ne373 = _src373.find("return result;", _ns373) if _ns373 != -1 else -1
        _norm_body373 = re.sub(r"//[^\n]*", "", _src373[_ns373:_ne373]) if (_ns373 != -1 and _ne373 != -1) else None
        _unpreserved373 = [
            _key for _key in _keys373
            if _norm_body373 is None or not re.search(r"\bdata\." + re.escape(_key) + r"\b", _norm_body373)
        ]
        check(
            bool(_keys373) and _norm_body373 is not None and not _unpreserved373,
            f"Check 373: normalizeAppsData が defaultAppsData の全 {len(_keys373)} フィールド ({', '.join(_keys373)}) を preserve (persist round-trip)",
            f"Check 373: defaultAppsData のフィールドが normalizeAppsData で preserve されていない: {sorted(_unpreserved373)} — "
            "store.js normalizeAppsData に `data.<field>` の正規化/保存を追加せよ。write は QuizPage 等が "
            "State.updateSilently で永続化するのに reload の normalize が strip する producer/consumer drift で、"
            "quizSearch が毎 reload で捨てられていた実バグ (#294/#568 と同 class) を封じる"
            if (_keys373 and _norm_body373 is not None) else
            "Check 373: store.js の defaultAppsData / normalizeAppsData を parse できない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 373: js/store.js present",
              "Check 373: js/store.js が無い — appsData persist round-trip coherence を検証できない", blocking=True)

    # ── 404. Store default-profile field ⟹ validateAndNormalize preserve round-trip (BLOCKING) ──
    # Check 373 (appsData 面) の profile 面。validateAndNormalize は全 ingestion 経路 (load / import /
    # cross-tab / snapshot-restore / settings 正規化) が通るチョークポイントで、profile を
    # `store.profile = { ...store.profile, <field>: … }` の形で再構築する。defaultProfile (永続化
    # される shape) にあるフィールドを読み戻さないと、ユーザーが設定/import しても reload 毎に default へ
    # silent に戻る。**これは既に一度起きた実バグ**: #139 で github / linkedin / location が strip され、
    # import しても消えていた (behavior e2e は当時の 3 フィールドだけを守っており、**新しく足す
    # フィールド**は無防備なまま)。defaultProfile の top-level key を brace-parse し、各 key が
    # validateAndNormalize の profile ブロックで `data.profile.<key>` として参照されることを強制する。
    if _store373.exists():
        _profile_body404 = _balanced_obj373(_src373, "const defaultProfile")
        _keys404 = _top_keys373(_profile_body404) if _profile_body404 else []
        # profile 正規化ブロック = `store.profile = {` 〜 対応する閉じ '}' (行コメントは除去)。
        _ps404 = _src373.find("store.profile = {")
        _pblock404 = None
        if _ps404 != -1:
            _inner404 = _balanced_obj373(_src373[_ps404:], "store.profile =")
            if _inner404 is not None:
                _pblock404 = re.sub(r"//[^\n]*", "", _inner404)
        _unpreserved404 = [
            _k404 for _k404 in _keys404
            if _pblock404 is None or not re.search(r"\bdata\.profile\." + re.escape(_k404) + r"\b", _pblock404)
        ]
        check(
            bool(_keys404) and _pblock404 is not None and not _unpreserved404,
            f"Check 404: validateAndNormalize が defaultProfile の全 {len(_keys404)} フィールド ({', '.join(_keys404)}) を preserve (profile persist round-trip)",
            f"Check 404: defaultProfile のフィールドが validateAndNormalize で preserve されていない: {sorted(_unpreserved404)} — "
            "store.js の `store.profile = { ... }` に `data.profile.<field>` の読み戻しを追加せよ。"
            "設定/import しても reload の normalize が strip して default へ silent に戻る data-fidelity バグになる "
            "(#139 で github/linkedin/location が実際にこれで消えていた)"
            if (_keys404 and _pblock404 is not None) else
            "Check 404: store.js の defaultProfile / store.profile 正規化ブロックを parse できない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 404: js/store.js present",
              "Check 404: js/store.js が無い — profile persist round-trip coherence を検証できない", blocking=True)

    # ── 405. Store top-level field ⟹ validateAndNormalize preserve round-trip (BLOCKING) ──
    # Check 373 (appsData 面) / 404 (profile 面) の **top-level 面**。createDefaultStore() が返す
    # 永続化 shape の各 top-level key は、validateAndNormalize 本体で `data.<key>` として読み戻され
    # なければならない。読み戻さない key はユーザーが設定/import しても reload 毎に default へ silent に
    # 戻る (この class は既に 3 度実バグ化している: quizSearch=#684 / profile github・linkedin・
    # location=#139 / projectPrefs.hiddenIds=#294 系)。carve-out は **設計上その場で再生成される
    # メタデータ**のみ: schemaVersion (現行 schema を書く) / type (固定タグ) / lastModified (保存時刻)。
    # 3 面 (top-level / profile / appsData) が揃うことで「永続化 shape に足したフィールドは必ず
    # 読み戻される」が全階層で invariant になる。
    if _store373.exists():
        # createDefaultStore の **返り値オブジェクト** (`return { … }`) を取る。関数本体の '{' から
        # balance すると key が depth 1 に埋もれて 0 件になるため、`return` を marker にする。
        _cs405 = _src373.find("function createDefaultStore")
        _default_store405 = _balanced_obj373(_src373[_cs405:], "return ") if _cs405 != -1 else None
        _keys405 = _top_keys373(_default_store405) if _default_store405 else []
        _META405 = {"schemaVersion", "type", "lastModified"}
        _vs405 = _src373.find("function validateAndNormalize")
        _ve405 = _src373.find("return store;", _vs405) if _vs405 != -1 else -1
        _vbody405 = re.sub(r"//[^\n]*", "", _src373[_vs405:_ve405]) if (_vs405 != -1 and _ve405 != -1) else None
        _unread405 = [
            _k405 for _k405 in _keys405
            if _k405 not in _META405
            and (_vbody405 is None or not re.search(r"\bdata\." + re.escape(_k405) + r"\b", _vbody405))
        ]
        check(
            bool(_keys405) and _vbody405 is not None and not _unread405,
            f"Check 405: validateAndNormalize が createDefaultStore の全 top-level フィールド"
            f" ({', '.join(_k for _k in _keys405 if _k not in _META405)}) を読み戻す (store persist round-trip)",
            f"Check 405: 永続化 shape の top-level フィールドが validateAndNormalize で読み戻されていない: "
            f"{sorted(_unread405)} — store.js validateAndNormalize に `data.<field>` の正規化/採用を追加せよ。"
            "読み戻さないと設定/import しても reload 毎に default へ silent に戻る (quizSearch #684 / "
            "profile #139 / projectPrefs #294 と同 class)。再生成されるメタデータ "
            "(schemaVersion / type / lastModified) のみ carve-out 対象"
            if (_keys405 and _vbody405 is not None) else
            "Check 405: store.js の createDefaultStore / validateAndNormalize を parse できない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 405: js/store.js present",
              "Check 405: js/store.js が無い — store top-level persist round-trip を検証できない", blocking=True)

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

    # ── 374. settings-page.js importJSON normalize-before-adopt ingestion guard (BLOCKING) ──
    # importJSON は外部 JSON を取り込む ingestion 経路。生の parsed を State.update で adopt すると
    # notify→render() が正規化前の生データ (malformed projects 等) を描画しうる (strict モードの
    # `merged.projects = parsed.projects` 生代入が malformed entry を SettingsPage の p.name/p.id
    # dereference へ通し crash させうる)。restoreSnapshot は既に「外部 ingestion は adopt する前に
    # validateAndNormalize を通せ」(#295/#561) に従い State.set(Store.validateAndNormalize(...)) で
    # commit する。importJSON も incidental な render-abort ordering (State.set の 2 度目 render が
    # 1 度目の生 render を SettingsPage 到達前に abort する) に data-safety を依存させず、同じ
    # normalize-before-commit へ整合させる。本 Check は importJSON 関数本体を brace-balance で抽出し、
    # State.update( を含まず validateAndNormalize を通すことを強制する (raw ingestion 描画の再混入を
    # 構造封じ・Check 130 の oninput no-State.update と同型の ingestion 版)。
    _sp374 = ROOT / "js" / "settings-page.js"
    if _sp374.exists():
        _src374 = _sp374.read_text(encoding="utf-8")
        _m374 = re.search(r"function\s+importJSON\s*\(", _src374)
        _ok374 = False
        _has_update374 = True
        _has_norm374 = False
        if _m374:
            _i374 = _src374.find("{", _m374.start())
            _depth374 = 0
            _body374 = ""
            for _k374 in range(_i374, len(_src374)):
                _c374 = _src374[_k374]
                if _c374 == "{":
                    _depth374 += 1
                elif _c374 == "}":
                    _depth374 -= 1
                    if _depth374 == 0:
                        _body374 = _src374[_i374:_k374 + 1]
                        break
            _has_update374 = "State.update(" in _body374
            _has_norm374 = "validateAndNormalize" in _body374
            _ok374 = (not _has_update374) and _has_norm374
        check(
            _m374 is not None and _ok374,
            "Check 374: settings-page.js importJSON は生を State.update で adopt せず validateAndNormalize してから State.set (normalize-before-commit ingestion)",
            ("Check 374: settings-page.js importJSON の ingestion が normalize-before-commit でない — "
             + ("State.update( を呼んでおり生データが render に届きうる" if _has_update374 else "validateAndNormalize を通していない")
             + "。マージ結果を Store.validateAndNormalize してから単一 State.set( で commit せよ "
             "(restoreSnapshot と同じ #295/#561 ingestion invariant・Check 130 の ingestion 版)")
            if _m374 else
            "Check 374: settings-page.js に importJSON 関数が見つからない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 374: js/settings-page.js present",
              "Check 374: js/settings-page.js が無い — importJSON ingestion guard を検証できない", blocking=True)

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

    # ── 410. UI 入力上限 ⟹ 保存上限の一致 (maxlength coherence) (BLOCKING) ─────────
    # 保存側が LIMITS.<KEY> で slice するのに UI 側に maxlength が無いと、「入力できた文字数」と
    # 「保存される文字数」がずれ、超過分が黙って捨てられる (notes editor は画面にもプレビューにも
    # 表示され続けたまま保存だけされず、リロードで初めて消失に気付く silent data-loss だった)。
    # 対象は UI レイヤー = input/textarea を組み立てる shipped JS のみ (store.js は normalize 層で
    # 入力要素を持たないため自動的に対象外)。
    _ui410 = sorted((ROOT / "js").glob("*.js"))
    _viol410, _pairs410 = [], 0
    for _f410 in _ui410:
        _src410 = _f410.read_text(encoding="utf-8")
        if "h('input'" not in _src410 and "h('textarea'" not in _src410:
            continue
        _keys410 = set(re.findall(r"\.slice\(0,\s*CONSTANTS\.LIMITS\.([A-Z_]+)\)", _src410))
        for _k410 in sorted(_keys410):
            _pairs410 += 1
            if not re.search(r"maxlength:\s*CONSTANTS\.LIMITS\." + _k410 + r"\b", _src410):
                _viol410.append(f"{_f410.name}: LIMITS.{_k410}")
    check(
        _pairs410 > 0 and not _viol410,
        f"Check 410: UI 入力 {_pairs410} 件の maxlength が保存側 LIMITS と同一定数で一致",
        (f"Check 410: UI 上限と保存上限が drift — {_viol410}。"
         "保存側が LIMITS.<KEY> で slice する入力には同じ定数で maxlength を付けよ "
         "(無いと超過分が silent に捨てられ、リロードで初めて消失が判明する)")
        if _pairs410 else
        "Check 410: UI レイヤーの LIMITS slice を 1 件も検出できない — maxlength coherence が無効化された",
        blocking=True,
    )
