"""
checks_identifier_resolution.py — shipped-code の「使用した識別子 ⟹ 実際に定義されている」検査群
(checks_wiring.py から分離・check.py split track・category "identifier resolution").

【なぜ分けたか】
分離元 checks_wiring.py は 987 行で Check 365 の hard ceiling (1,000) まで残り 13 行だった。
しかも当時 `.github/scripts/checks_*.py` は 1 つも BUDGET-DATA に登録されておらず、
Check 52 の advisory が**構造的に一度も鳴らない**状態だったため、次に Check を 1 本足した
時点で「警告なしにいきなり BLOCKING」になる位置にいた (#1266 で塞いだ「早期警告が効かない層」
と同じ失敗形。あちらは advisory ≥ hard ceiling、こちらは advisory 不在)。

圧縮で誤魔化さず、**意味の異なる 2 クラスタ**へ割った:
  - checks_wiring.py          … 「file/anchor/selector が実際に配線・描画されているか」
                                 (存在 ≠ 配線。Checks 132/133/134/403/411)
  - checks_identifier_resolution.py … 「コードが使う識別子が実際に定義へ解決するか」
                                 (used ⟹ defined。本ファイル)

【なぜこの境界か】
本ファイルの 9 Check は例外なく「shipped code に現れた**名前**を集め、それが定義側の集合に
含まれるか」を照合する同型の検査で、いずれも typo / rename / 配線漏れが **silent** に
なる面を守る (未定義アイコンは空描画・未登録 action は no-op・dangling idref は支援技術が
迷子になる)。これらは「file が load されているか」を見る wiring とは走査対象も失敗モードも別。

分離は byte-equivalent: 移した section は 1 行も書き換えず、`ROOT` / `check` を ctx から
受け取るだけで動く (free-variable 解析で外部依存が この 2 つだけであることを実測してから割った)。

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  375. Shipped-JS createIcon name → icon-registry resolution: createIcon(name) (js/ui-components.js)
       looks up getIcons()[name] and, when the name is not a registry key, SILENTLY returns an empty
       text node — no throw, no console error, no e2e failure. A typo'd icon name (e.g.
       createIcon('lightbub') or a data field icon: 'trsah') therefore renders an invisible icon on
       an icon-only button (delete/close/menu affordances vanish) and slips past verify AND the
       behavior e2e AND the advisory screenshot. This is the same silent-wiring class as 133/134
       ("file exists ⟹ it is wired") applied to icon usage ("an icon name is used ⟹ it is actually
       defined"). This Check parses the getIcons() object's registry keys and every literal icon name
       reaching createIcon — both direct `createIcon('X')` calls and the `icon: 'X'` data fields that
       flow through `createIcon(item.icon)` / `createIcon(app.icon)` — across shipped JS (js/*.js) and
       asserts each resolves to a registry key, making "icon name used ⟹ defined" an enforced
       invariant so a typo can never silently blank an icon. Argument parsing takes the WHOLE
       first-argument expression (up to the top-level comma), so a ternary like
       `createIcon(open ? 'chevronUp' : 'chevronDwn', 16)` has BOTH branches validated — the
       initial version only matched a single literal right after `createIcon(` and therefore
       missed a typo in either branch (measured: injecting that exact call left the Check
       GREEN, i.e. one toggle state silently renders no icon). Literals in the CONDITION part
       (before the top-level `?`) are excluded so comparisons like `state.theme === 'dark' ?`
       are not mistaken for icon names. Comments are stripped and the root entry `main.js` is
       scanned too. (BLOCKING)
       375b is the REVERSE direction (defined ⟹ used): an icon sitting in the registry that no
       call site ever names is dead weight shipped to every visitor. Measured when adopting it:
       16 of 50 keys (1,996 bytes) were never wired — `git log -S "createIcon('<name>')"` returned
       zero commits for each, so they were speculative additions, not lost wiring. They silently
       ate into the Check 120 byte budget. If a future increment legitimately needs an icon
       defined ahead of its use, add the call site in the same PR or carve it out explicitly —
       do not delete the Check. (BLOCKING)
  376. data-action → ActionDelegator handler resolution: the AIDK ActionDelegator (js/aidk-rails.js)
       is a single document-level click delegator — an element carrying `data-action="X"` triggers
       `_handlers[X]` on click, and if X is not a registered handler key the lookup returns undefined
       and the click is a SILENT no-op (no throw, no console error, no e2e failure). A typo'd action
       (e.g. `data-action="drawr:open"` on the topbar menu button) therefore makes a critical control
       — menu / theme / BGM — do nothing, and slips past verify AND the behavior e2e AND the advisory
       screenshot. This is the same silent-wiring class as Check 375 (icon) / 133 / 134, applied to
       data-action producers ("an action is used ⟹ a handler is defined"). This Check parses the
       ActionDelegator `_handlers` object keys plus any `register('X', ...)` calls (the handler
       registry) and every `data-action="X"` / `'data-action': 'X'` producer in index.html and shipped
       JS, and asserts every producer resolves to a handler. The reverse (handler ⟹ producer) is NOT
       enforced: `drawer:close` is an intentionally symmetric unused handler (the drawer closes via
       direct onclick / Escape / nav-click), so this is a used⟹defined guard, not a bijection.
       Producer detection covers a NOTATION FAMILY: the HTML/JSX-ish attribute literal
       (`data-action="X"`), the h() prop (`'data-action': 'X'`), AND the DOM-API forms
       `setAttribute('data-action', 'X')` / `el.dataset.action = 'X'`. The initial version matched
       only the first two, so a typo'd action set through the DOM API passed GREEN (measured:
       injecting both DOM-API forms with typo'd names left the Check green — exactly the silent
       no-op button this Check exists to prevent). Scope includes the root entry `main.js`.
       Honest limit: dynamically composed names (template literals / variables) are not tracked.
       (BLOCKING)
  391. getElementById target → id definition resolution: every `getElementById('X')` literal in shipped
       JS must point at an id that is actually defined — as index.html `id="X"`, a shipped-JS `id: 'X'`
       h() prop, or a dynamic assignment (`el.id = 'X'` / `setAttribute('id','X')`). Renaming an id in
       index.html or another module while leaving `getElementById('old')` behind makes the DOM lookup
       return null and the button/feature a SILENT no-op (the behavior e2e only checks content render,
       the screenshot is advisory, so a dead lookup slips through every gate). Same silent-wiring class
       as #257 (palette NAV) / #262 (topbar). This is the DOM-id face of the used⟹defined wiring lens
       of Check 375 (icon) / 376 (data-action) / 377 (route→case): target ⊆ defined. (BLOCKING)
  392. aria idref / <label for> → id definition resolution: every static-literal a11y id reference
       (aria-labelledby / -describedby / -controls / -errormessage, plus <label for>) must point at a
       defined id. A dangling aria idref is higher-severity than Check 391's dead getElementById: the
       accessible name / description / control association silently breaks in assistive tech — a real
       WCAG 1.3.1 / 4.1.2 defect (screen reader announces a control with no label) that is visually
       invisible and slips past the behavior e2e (class of #563 a11y-attr leak / #728 label wiring).
       The a11y-idref face of the used⟹defined wiring lens (Check 391 DOM-id twin). Dynamic idrefs
       (aria-activedescendant='cmdk-opt-'+i template literals / setAttribute) are structurally
       self-consistent so only static literals are enforced; `for` colon matching is single-line
       [ \\t]* anchored to exclude the JS `for` keyword. (BLOCKING)
  393. CONSTANTS.* reference → definition resolution: every `CONSTANTS.<KEY>` (and nested
       `CONSTANTS.LIMITS.<M>` / `CONSTANTS.POMODORO_DEFAULT_SETTINGS.<M>`) reference in shipped JS
       (main.js + js/*.js) must resolve to a key actually defined in js/constants.js. A typo'd
       reference (e.g. `CONSTANTS.LIMITS.MAX_TASSK`, `CONSTANTS.DEBOUNCE_DELY`) is a valid JS property
       access that silently evaluates to `undefined` — no throw, no ESLint error (property access on a
       defined object is legal), no node --check failure. The consequence is a SILENT bug: `undefined`
       as a `.slice(0, undefined)` bound defeats a DoS/bloat truncation guard (returns the whole array),
       and `undefined` as a `setTimeout(fn, undefined)` delay fires immediately. This is the same
       used⟹defined wiring lens as Check 375 (icon) / 376 (data-action) / 377 (route→case) / 391
       (getElementById) / 392 (aria idref), applied to CONSTANTS access. The Check parses the top-level
       CONSTANTS keys (4-space-indented `KEY:` in the export) and, for object-valued top keys
       (LIMITS / POMODORO_DEFAULT_SETTINGS), their member keys via balanced-brace extraction; it then
       validates seg1 (the top key) for every reference and seg2 only when seg1 is a known object key —
       so a method chain on a scalar constant (`CONSTANTS.STORAGE_KEY.slice(...)`) is NOT mis-flagged.
       Values that are IIFEs/expressions (TAB_ID / DEBUG, whose value starts with `(` not `{`) are
       never treated as objects, so their internals never pollute the valid-key set. A cross-namespace
       Destructured access is followed too: `const { LIMITS } = CONSTANTS` / `const { LIMITS: L }
       = CONSTANTS` maps the alias back to its top key and validates `alias.MEMBER`. The
       initial version only matched dotted access starting at `CONSTANTS.`, so destructuring
       let a typo through (measured: `const { LIMITS } = CONSTANTS; LIMITS.MAX_TASSK` stayed
       GREEN). Comments are stripped so prose examples are not read as real references.
       Cross-namespace typo (`CONSTANTS.LIMITS.work`) is an accepted non-goal — the dominant misspelled-key class is
       enforced, not an exhaustive per-namespace bijection. (BLOCKING)
  395. Router.navigate() target (literal + データ駆動 path) → router route-segment resolution: every
       `Router.navigate('X')` call in shipped JS (main.js + js/*.js) must have its base path
       segment (X stripped of `?query` and taken up to the first `/`) resolve to a top-level route
       segment that router.js `_parseRoute` actually handles (a `case 'seg':` label, or the empty
       string = home default). router.js parses an UNKNOWN first segment as `name:'home'` and
       renders the homepage — so a typo'd nav target (`Router.navigate('rolesplit')`, a renamed route
       left stale) SILENTLY sends the user to the home page instead of the intended destination, with
       no throw, no console error, and no e2e failure (the behavior e2e asserts each route renders
       when visited directly, not that every in-page nav button points at a live route; the
       screenshot is advisory). Producer-side twin of Check 377 (route.name ⟹ a main.js render case):
       377 guards the consumer (a parsed route has a renderer), 395 guards the producer (a nav call
       targets a parseable route). Template-literal targets (`apps/${app}` / `projects/${slug}`) are
       structurally dynamic and excluded; only no-`$` string literals are enforced, and JS line
       comments are stripped so documentation examples never false-positive. Same used⟹defined wiring
       lens as Check 375 (icon) / 376 (data-action) / 391 (getElementById) / 392 (aria idref) / 393
       (CONSTANTS): navigate target ⊆ router-handled segments. (BLOCKING)
       Detection covers BOTH notations. The literal-only version missed the repo's OTHER, more common
       notation: a file that calls `Router.navigate(<identifier>)` keeps its destinations in a data
       array as `path: '<route>'` (the sidebar in js/components.js and the CTA cards in
       js/hiring-risk-page.js — 12 of the 19 enforced targets), so a typo there (`path: 'setting'`)
       passed GREEN and silently sent the user home. Files calling navigate with an identifier
       therefore also have their `path:` string literals resolved. Measured: mutating
       `path: 'settings'` → `path: 'setting'` turns this Check RED. The same "static Check sees only
       one spelling" hole as Checks 112 / 130 / 375 / 376 / 393 / 402. Palette destinations use
       `hash:` and are already covered by the Check 128 / 382 router bijections. (BLOCKING)
  396. Router route.name ⟹ PAGE_META entry: every route.name that router.js `_parseRoute` can emit
       (literal `route.name = 'X'` assignments, the initial `{ name: 'home' }` default, and the
       `app-${app}` template expanded from the app whitelist) must have an entry in js/page-meta.js
       PAGE_META. meta-management.js `applyMeta` does `const meta = PAGE_META[routeName]` and EARLY-
       RETURNS when a route has no entry — so a route missing from PAGE_META SILENTLY loses its
       `<title>` update, SEO meta (description/og), and the route-announcer title (a11y 2.4.2), with no
       throw or console error (the behavior e2e renders each route but does not assert the title/meta
       announcer; the screenshot is advisory). Consumer-side twin of Check 377 (route.name ⟹ a main.js
       render case) and complement to Check 148 (ARTICLE_ROUTES ⊆ PAGE_META): closes the meta face of
       the route mesh so adding a new router route (or a new `app-*` subroute) without a PAGE_META entry
       fails the build instead of shipping a title-less/meta-less page. Same used⟹defined wiring lens as
       Check 375/376/377/391/392/393/395. (BLOCKING)
  401. quiz?type= リテラル ⟹ QUIZ_TITLES キー (401a) / sidebar 非 aws 集合の一致 (401b):
       QuizPage は `QUIZ_DATA_MAP[quizType] || QUIZ_DATA_MAP.aws` で描画するため、リンク側の type が
       typo/未定義でも **例外にならず AWS 問題集が描画される** — 「PM問題集」ボタンを押すと黙って AWS の
       問題が出る silent wrong-content。401a は shipped JS/HTML の全 `quiz?type=X` リテラルが実キーへ
       解決することを強制する (Check 375/376/377/393 と同じ used⟹defined wiring レンズの query-value 面。
       Check 395 は Router.navigate の base path segment のみ見て ?query を落とすため本面は無防備だった)。
       401b は sidebar の active 判定が持つ非 aws キーのハードコード集合 (`['pm','quality','architecture']`)
       が map キー − {aws} と一致することを強制する — 5 つ目の quiz を足すと、その page は正しく描画される
       のに nav は「AWS 問題集」を active に光らせる control↔content desync (#781 class) が silent に
       生まれるため。両者とも throw せず「それらしく動く」ので behavior e2e も素通りする。
       honest carve-out: 401a は行全体がコメントの行を除外する (components.js が「無効 type
       #/quiz?type=zzz でも AWS が出る」というフォールバック挙動の説明を WHY コメントに書いており、
       それを実リンクと誤検出するため — 実バグでなく設計記述を捕捉した false-positive)。行末
       コメントは除外しない (コード行に紛れた実リテラルを見落とさないため)。(BLOCKING)
  418. Check 376 の逆方向 (定義 ⟹ 使用)。ActionDelegator の `_handlers` に登録されている
       全 handler key について、`data-action="X"` を持つ要素が index.html か shipped JS の
       いずれかに存在することを BLOCKING 強制する。発火経路の無い handler は **到達不能**で、
       しかもその handler のためだけに依存を引きずる (実例: 2026-08-10 に除去した
       `drawer:close` は main.js → late-binding holder → createAIDKRails の closeDrawer 引数、
       という配線を丸ごと必要としていた。`git log -S` で `data-action="drawer:close"` は
       **全履歴で 0 件** = 一度も配線されたことが無い never-wired な残骸と確認)。
       icon 面は Check 375 (使用⟹定義) と 375b (定義⟹使用) で既に双方向だったのに、action 面
       だけ片方向だった非対称を閉じる。producer 集合は Check 376 の抽出を共有する
       (同じ抽出を二重に持つと drift するため)。(BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 375. Shipped-JS createIcon name → icon-registry resolution (BLOCKING) ──────
    # createIcon(name) (js/ui-components.js) は getIcons()[name] を引き、name が registry key で
    # ないとき silent に空 text node を返す (throw も console error も e2e 失敗も無い)。typo した
    # icon 名 (createIcon('lightbub') や data field icon: 'trsah') は icon-only ボタン (削除/閉じる/
    # メニュー) のアイコンを不可視化するのに verify も behavior e2e も advisory screenshot も素通り
    # する。133/134 の「file 存在 ⟹ 配線済」と同じ silent-wiring class を icon 使用面 (「icon 名が
    # 使われる ⟹ 実際に定義済」) に適用する。getIcons() の registry key と、createIcon へ届く全
    # literal icon 名 (直接 `createIcon('X')` 呼び出し + `createIcon(item.icon)`/`createIcon(app.icon)`
    # へ流れる data field `icon: 'X'`) を shipped JS (js/*.js) から parse し、各々が registry key に
    # 解決することを強制する。
    _uic375 = ROOT / "js" / "ui-components.js"
    if _uic375.exists():
        _uicsrc375 = _uic375.read_text(encoding="utf-8")
        # getIcons() 関数本体を brace-balance で抽出し、registry key (obj の `key:` / `'key':`) を集める
        _gm375 = re.search(r"function\s+getIcons\s*\(\s*\)\s*\{", _uicsrc375)
        _keys375 = set()
        if _gm375:
            _gi375 = _uicsrc375.find("{", _gm375.start())
            _gd375 = 0
            _gbody375 = ""
            for _gk375 in range(_gi375, len(_uicsrc375)):
                _gc375 = _uicsrc375[_gk375]
                if _gc375 == "{":
                    _gd375 += 1
                elif _gc375 == "}":
                    _gd375 -= 1
                    if _gd375 == 0:
                        _gbody375 = _uicsrc375[_gi375:_gk375 + 1]
                        break
            # 各 key は `name: '<svg .../>'` または `'na-me': '...'` 形式で SVG 文字列値を持つ
            _keys375 = set(re.findall(r"['\"]?([A-Za-z][\w-]*)['\"]?\s*:\s*['\"`]", _gbody375))
        # shipped JS 全体から createIcon への literal icon 名を収集 (直接呼び出し + icon: data field)
        _used375 = {}  # name -> "file" (最初の出現 file を記録)
        # [FIX] 第 1 引数が **単一リテラルの場合しか見ていなかった**ため、三項など複数リテラルを含む
        #   式 (`createIcon(open ? 'chevronUp' : 'chevronDwn', 16)`) の **片枝の typo を見逃していた**
        #   (実測: 上記を leaf module に注入しても GREEN = トグルの片状態だけアイコンが消える silent
        #   broken-icon が素通り)。第 1 引数式を top-level ',' まで切り出し、その中の全 literal を
        #   検証対象にする。コメント除去 + 走査対象に root の main.js を追加。
        def _first_arg375(_t, _pos):
            """createIcon( の直後から top-level ',' または ')' までの第 1 引数式を返す。"""
            _d, _out, _i = 0, [], _pos
            while _i < len(_t):
                _c = _t[_i]
                if _c in "([{":
                    _d += 1
                elif _c in ")]}":
                    if _d == 0:
                        break
                    _d -= 1
                elif _c == "," and _d == 0:
                    break
                _out.append(_c)
                _i += 1
            return "".join(_out)

        for _f375 in sorted((ROOT / "js").glob("*.js")) + [ROOT / "main.js"]:
            if not _f375.exists():
                continue
            _t375 = re.sub(r"//[^\n]*", "", _f375.read_text(encoding="utf-8"))
            for _cm375 in re.finditer(r"createIcon\(", _t375):
                _arg375 = _first_arg375(_t375, _cm375.end())
                # 三項の **値位置** のリテラルだけを icon 名とみなす。条件部のリテラル
                # (`state.theme === 'dark' ? ...`) を icon 名と誤検出しないため、最初の top-level
                # '?' より後ろだけを対象にする (実測: これが無いと 'dark'/'system' を icon 名と誤認)。
                _d375, _q375 = 0, -1
                for _ci375, _cc375 in enumerate(_arg375):
                    if _cc375 in "([{":
                        _d375 += 1
                    elif _cc375 in ")]}":
                        _d375 -= 1
                    elif _cc375 == "?" and _d375 == 0:
                        _q375 = _ci375
                        break
                _vals375 = _arg375[_q375 + 1:] if _q375 != -1 else _arg375
                for _lm375 in re.finditer(r"['\"]([A-Za-z][\w-]*)['\"]", _vals375):
                    _used375.setdefault(_lm375.group(1), str(_f375.relative_to(ROOT)))
            for _mm375 in re.finditer(r"\bicon\s*:\s*['\"]([A-Za-z][\w-]*)['\"]", _t375):
                _used375.setdefault(_mm375.group(1), str(_f375.relative_to(ROOT)))
        _unresolved375 = sorted(
            f"{_n375} ({_used375[_n375]})" for _n375 in _used375 if _n375 not in _keys375
        )
        # [375b] 逆方向 (定義 ⟹ 使用)。registry に足したまま一度も使われないアイコンは全ユーザーへ
        #   配信される dead weight (実測: 16 件 = 1,996 bytes が never-wired。git -S で createIcon('<name>')
        #   を含む commit がゼロ＝lost-wiring でなく初版からの残骸と確認済)。Check 120 の byte 予算を
        #   無言で圧迫するため「定義したら使う」を強制する。先行定義が必要なら本 Check を落とさず、
        #   使用箇所を同 PR で足すか意図を明記して carve-out すること。
        _unused375 = sorted(_keys375 - set(_used375))
        check(
            not _unused375,
            f"Check 375b: getIcons() registry に未使用アイコンなし ({len(_keys375)} key すべて使用)",
            f"Check 375b: 一度も使われないアイコンが registry にある: {_unused375} — 全ユーザーへ配信される "
            "dead weight で Check 120 の byte 予算を無言で圧迫する。使用箇所を足すか registry から除去せよ",
            blocking=True,
        )
        check(
            bool(_keys375) and not _unresolved375,
            f"Check 375: shipped JS の全 literal icon 名 ({len(_used375)} 種) が getIcons() registry ({len(_keys375)} key) に解決 (silent broken-icon 防止)",
            f"Check 375: createIcon へ届く icon 名が registry に未定義: {_unresolved375} — "
            "createIcon(name) は未定義 name で silent に空アイコンを返すため typo が全 gate を素通りして "
            "アイコンが不可視化する。js/ui-components.js の getIcons() に該当 icon を追加するか、使用側の "
            "名前の typo を修正せよ"
            if _keys375 else
            "Check 375: js/ui-components.js の getIcons() から registry key を parse できない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 375: js/ui-components.js present",
              "Check 375: js/ui-components.js が無い — createIcon の icon-registry 解決を検証できない", blocking=True)

    # ── 376. data-action → ActionDelegator handler resolution (BLOCKING) ───────────
    # AIDK ActionDelegator (js/aidk-rails.js) は document 単一 click 委譲器で、`data-action="X"` を
    # 持つ要素の click が `_handlers[X]` を発火する。X が未登録 handler key だと lookup が undefined
    # を返し click は silent no-op (throw も console error も e2e 失敗も無い)。typo した action
    # (`data-action="drawr:open"` 等) は menu/theme/BGM の critical control を無反応にするのに verify
    # も behavior e2e も advisory screenshot も素通りする。Check 375 (icon) / 133 / 134 と同じ
    # silent-wiring class を data-action producer 面 (「action が使われる ⟹ handler が定義済」) に
    # 適用する。ActionDelegator の `_handlers` object キー + `register('X', ...)` 呼び出しを handler
    # registry として parse し、index.html + shipped JS の全 `data-action="X"` / `'data-action': 'X'`
    # producer を集めて各々が handler に解決することを強制する。逆方向 (handler ⟹ producer) は
    # **Check 418 が別途強制する**。従来ここには「`drawer:close` は意図的に symmetric な unused
    # handler ゆえ bijection にしない」と書かれていたが、2026-08-10 に `git log -S` で
    # `data-action="drawer:close"` が **全履歴で一度も存在しない** (= symmetry のための飾りであって
    # 到達不能) と確認し、handler と threaded な closeDrawer 依存を除去した。これで action 面も
    # icon 面 (Check 375 / 375b) と同じ双方向ガードになり、死んだ handler の蓄積を防げる。
    _rails376 = ROOT / "js" / "aidk-rails.js"
    _index376 = ROOT / "index.html"
    if _rails376.exists() and _index376.exists():
        _railsrc376 = _rails376.read_text(encoding="utf-8")
        # _handlers = { 'a:b': ..., ... } の object body を brace-balance で抽出し key を集める
        _hm376 = re.search(r"_handlers\s*=\s*\{", _railsrc376)
        _hkeys376 = set()
        if _hm376:
            _hi376 = _railsrc376.find("{", _hm376.start())
            _hd376 = 0
            _hbody376 = ""
            for _hk376 in range(_hi376, len(_railsrc376)):
                _hc376 = _railsrc376[_hk376]
                if _hc376 == "{":
                    _hd376 += 1
                elif _hc376 == "}":
                    _hd376 -= 1
                    if _hd376 == 0:
                        _hbody376 = _railsrc376[_hi376:_hk376 + 1]
                        break
            _hkeys376 = set(re.findall(r"['\"]([A-Za-z][\w:-]*)['\"]\s*:", _hbody376))
        # 動的登録 register('X', ...) も handler registry に含める (将来 producer 網羅性のため)
        _hkeys376 |= set(re.findall(r"\.register\(\s*['\"]([A-Za-z][\w:-]*)['\"]", _railsrc376))
        # producer: index.html の data-action="X" + shipped JS の data-action / 'data-action': 'X'。
        # コメントは除去する (aidk-rails.js の docstring `// AIは data-action="ACTION_NAME"` 等が
        # 説明用リテラルを producer と誤検出する false-positive を防ぐ。JS は行コメント `//`、HTML は
        # `<!-- -->` を strip)。
        _producers376 = {}  # action -> source file
        _html376 = re.sub(r"<!--.*?-->", "", _index376.read_text(encoding="utf-8"), flags=re.DOTALL)
        for _pm376 in re.finditer(r"data-action\s*=\s*['\"]([A-Za-z][\w:-]*)['\"]", _html376):
            _producers376.setdefault(_pm376.group(1), "index.html")
        # [FIX] producer の記法族を網羅する。従来は「属性リテラル」と「h() prop」の 2 綴りだけを見て
        #   おり、DOM API 経由の producer — `setAttribute('data-action', 'X')` と
        #   `el.dataset.action = 'X'` — を丸ごと見逃していた (実測: typo した action 名を両記法で
        #   leaf module に注入しても GREEN のまま = silent no-op ボタンが素通りする)。走査対象に
        #   root の main.js も追加する (従来 js/*.js のみ)。
        for _f376 in sorted((ROOT / "js").glob("*.js")) + [ROOT / "main.js"]:
            if not _f376.exists():
                continue
            _t376 = re.sub(r"//[^\n]*", "", _f376.read_text(encoding="utf-8"))
            for _pat376 in (r"data-action\s*=\s*['\"]([A-Za-z][\w:-]*)['\"]",
                            r"['\"]data-action['\"]\s*:\s*['\"]([A-Za-z][\w:-]*)['\"]",
                            r"setAttribute\(\s*['\"]data-action['\"]\s*,\s*['\"]([A-Za-z][\w:-]*)['\"]",
                            r"dataset\.action\s*=\s*['\"]([A-Za-z][\w:-]*)['\"]"):
                for _pm376b in re.finditer(_pat376, _t376):
                    _producers376.setdefault(_pm376b.group(1), str(_f376.relative_to(ROOT)))
        _unresolved376 = sorted(
            f"{_a376} ({_producers376[_a376]})" for _a376 in _producers376 if _a376 not in _hkeys376
        )
        check(
            bool(_hkeys376) and bool(_producers376) and not _unresolved376,
            f"Check 376: 全 data-action producer ({len(_producers376)} 種) が ActionDelegator handler ({len(_hkeys376)} key) に解決 (silent no-op 防止)",
            f"Check 376: data-action が ActionDelegator handler に未解決: {_unresolved376} — "
            "ActionDelegator は未登録 action で silent no-op になるため typo が全 gate を素通りして "
            "ボタンが無反応化する。js/aidk-rails.js の ActionDelegator _handlers に該当 action を追加するか、"
            "producer 側の data-action の typo を修正せよ"
            if (_hkeys376 and _producers376) else
            "Check 376: ActionDelegator の _handlers キーまたは data-action producer を parse できない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 376: js/aidk-rails.js and index.html present",
              "Check 376: js/aidk-rails.js または index.html が無い — data-action の handler 解決を検証できない", blocking=True)

    # ── 418. ActionDelegator handler ⟹ data-action producer (定義 ⟹ 使用) ────────────
    # Check 376 の逆方向。`_handlers` に登録されているのに `data-action="X"` を持つ要素が
    # どこにも無い handler は **到達不能なコード**で、しかも依存を引きずる (実例: 除去した
    # `drawer:close` は main.js → late-binding holder → createAIDKRails の closeDrawer 引数、
    # という配線を丸ごと必要としていた)。icon 面では Check 375 (使用⟹定義) と 375b (定義⟹使用) が
    # 既に双方向で守られており、action 面だけ片方向だった非対称を閉じる。
    # producer 集合は Check 376 が集めたものをそのまま使う (同じ抽出を二重に持つと drift するため)。
    if _rails376.exists() and _index376.exists():
        _dead418 = sorted(_hkeys376 - set(_producers376))
        check(
            bool(_hkeys376) and not _dead418,
            f"Check 418: ActionDelegator の全 handler ({len(_hkeys376)} key) に data-action producer が存在 (到達不能 handler なし)",
            (f"Check 418: 発火経路の無い ActionDelegator handler がある: {_dead418} — "
             "`data-action=\"X\"` を持つ要素がどこにも無い handler は到達不能で、"
             "多くの場合その handler のためだけに依存 (factory 引数 / late-binding holder) を"
             "引きずる。使わないなら handler と依存を除去し、必要なら producer 側に "
             "data-action を付けて配線せよ (Check 376 の逆方向・icon 面の Check 375b と同型)"
             if _hkeys376 else
             "Check 418: ActionDelegator の _handlers を parse できない (構造変更の可能性)"),
            blocking=True,
        )

    # ── 391. getElementById target → id definition resolution (BLOCKING) ───────────
    # 各 shipped JS の `getElementById('X')` リテラル target は、必ず index.html の `id="X"`・
    # shipped JS の `id: 'X'` (h() prop)・動的生成 (`el.id = 'X'` / `setAttribute('id','X')`) の
    # いずれかで定義される id を指していなければならない。id を index.html や別モジュールでリネーム
    # したのに `getElementById('old')` を残すと、DOM lookup が null を返し、button/feature が silent
    # no-op 化する (behavior e2e は content 描画のみ検査・screenshot は advisory ゆえ完全 silent。
    # 実例 class: #257 palette NAV 欠落 / #262 topbar 二重発火などの wiring 系 discoverability 破壊)。
    # Check 375 (createIcon→registry) / 376 (data-action→handler) / 377 (route→case) と同じ
    # used⟹defined wiring レンズの DOM-id 面。target ⊆ defined を機械強制して dead lookup を封じる。
    _html391 = ROOT / "index.html"
    _shipped391 = [ROOT / "main.js"] + sorted((ROOT / "js").glob("*.js"))
    _shipped391 = [p for p in _shipped391 if p.exists()]
    if _html391.exists() and _shipped391:
        _defined391 = set(re.findall(r'\bid="([a-zA-Z0-9_-]+)"', _html391.read_text(encoding="utf-8")))
        _targets391 = {}
        for _f391 in _shipped391:
            _s391 = _f391.read_text(encoding="utf-8")
            _defined391 |= set(re.findall(r"""\bid:\s*['"]([a-zA-Z0-9_-]+)['"]""", _s391))
            _defined391 |= set(re.findall(r"""\.id\s*=\s*['"]([a-zA-Z0-9_-]+)['"]""", _s391))
            _defined391 |= set(re.findall(r"""setAttribute\(\s*['"]id['"]\s*,\s*['"]([a-zA-Z0-9_-]+)['"]""", _s391))
            for _t391 in re.findall(r"""getElementById\(\s*['"]([a-zA-Z0-9_-]+)['"]""", _s391):
                _targets391.setdefault(_t391, str(_f391.relative_to(ROOT)))
        _dead391 = sorted(f"{_t} ({_targets391[_t]})" for _t in _targets391 if _t not in _defined391)
        check(
            bool(_targets391) and not _dead391,
            f"Check 391: 全 getElementById target ({len(_targets391)} 種) が定義済み id (index.html / shipped-JS id: / 動的 .id=) に解決 (dead DOM lookup 防止)",
            f"Check 391: getElementById の target が未定義 id を指す (silent no-op): {_dead391} — "
            "id を index.html や別モジュールでリネームしたのに getElementById('old') が残ると DOM lookup が "
            "null を返し button/feature が無反応化する。定義側の id を復元するか getElementById の target を修正せよ"
            if _targets391 else
            "Check 391: shipped JS に getElementById target が見つからない — DOM-id wiring を検証できない",
            blocking=True,
        )
    else:
        check(False, "Check 391: index.html and shipped JS present",
              "Check 391: index.html または shipped JS が無い — getElementById の id 解決を検証できない", blocking=True)

    # ── 392. aria idref / <label for> → id definition resolution (BLOCKING) ────────
    # 静的リテラルの a11y id 参照 (aria-labelledby / -describedby / -controls / -errormessage、
    # および <label for>) は、必ず定義済み id を指していなければならない。dangling な aria idref は
    # DOM lookup が null を返して silent no-op になる Check 391 (getElementById) より高 severity で、
    # accessible name / description / control の関連付けが assistive tech 上で切れる実 WCAG 欠陥
    # (1.3.1 Info and Relationships / 4.1.2 Name,Role,Value)。id を片方でリネームすると screen reader が
    # ラベルを解決できず「label 無し」の control をアナウンスするが、visual には無変化・behavior e2e も
    # 素通りする (実例 class: #563 の a11y 属性 leak / #728 の label 関連付け)。Check 391 の DOM-id
    # used⟹defined wiring の a11y-idref 面。動的 id 参照 (aria-activedescendant='cmdk-opt-'+i 等の
    # template literal / setAttribute) は構造上 self-consistent ゆえ対象外 = 静的リテラル参照のみ強制。
    # `for` は JS キーワードと衝突するため colon 周りを単一行 [ \t]* に固定し for-loop 誤検出を排除。
    _html392 = ROOT / "index.html"
    _shipped392 = [p for p in ([ROOT / "main.js"] + sorted((ROOT / "js").glob("*.js"))) if p.exists()]
    if _html392.exists() and _shipped392:
        _sources392 = _shipped392 + [_html392]

        def _strip_comments392(text, is_html):
            """コメントを除去する。除去しないと **説明コメント中の id 参照が実参照として数えられ**、
            定義側がリテラルでなくなった瞬間に false RED を出す (2026-08-11 に実際に発生:
            `aria-controls="nav-lab-body"` と書いた WHY コメントが dangling 参照と判定された)。
            Check 112 / 421 / 422 と同じ「コメントは違反にも充足にもしない」規律の idref 面。"""
            if is_html:
                return re.sub(r"<!--.*?-->", "", text, flags=re.S)
            text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
            # `https://` を行コメントと誤認しないため colon 直後の // は除外する (repo 共通の idiom)。
            return re.sub(r"(?<!:)//[^\n]*", "", text)

        _defined392 = set()
        for _f392 in _sources392:
            _s392 = _strip_comments392(_f392.read_text(encoding="utf-8"), _f392.suffix == ".html")
            _defined392 |= set(re.findall(r'\bid="([a-zA-Z0-9_-]+)"', _s392))
            _defined392 |= set(re.findall(r"""\bid:\s*['"]([a-zA-Z0-9_-]+)['"]""", _s392))
            _defined392 |= set(re.findall(r"""\.id\s*=\s*['"]([a-zA-Z0-9_-]+)['"]""", _s392))
            _defined392 |= set(re.findall(r"""setAttribute\(\s*['"]id['"]\s*,\s*['"]([a-zA-Z0-9_-]+)['"]""", _s392))
        _refs392 = {}  # idref value -> (attr, file)
        _aria392 = ["aria-labelledby", "aria-describedby", "aria-controls", "aria-errormessage"]
        for _f392 in _sources392:
            _s392 = _strip_comments392(_f392.read_text(encoding="utf-8"), _f392.suffix == ".html")
            _rel392 = str(_f392.relative_to(ROOT))
            for _attr392 in _aria392:
                for _pat392 in (rf'{_attr392}="([^"]+)"',
                                rf"""['"]?{re.escape(_attr392)}['"]?[ \t]*:[ \t]*['"]([^'"]+)['"]"""):
                    for _m392 in re.findall(_pat392, _s392):
                        for _idv392 in _m392.split():
                            if re.fullmatch(r"[a-zA-Z0-9_-]+", _idv392):
                                _refs392.setdefault(_idv392, (_attr392, _rel392))
            # <label for>: HTML for="X" + h() 単一行 for: 'X' / 'for': 'X' (for-loop 誤検出を [ \t]* で排除)
            for _pat392 in (r'\bfor="([a-zA-Z0-9_-]+)"',
                            r"""['"]?for['"]?[ \t]*:[ \t]*['"]([a-zA-Z0-9_-]+)['"]"""):
                for _m392 in re.findall(_pat392, _s392):
                    _refs392.setdefault(_m392, ("for", _rel392))
        _dangling392 = sorted(f"{_r} [{_refs392[_r][0]} in {_refs392[_r][1]}]"
                              for _r in _refs392 if _r not in _defined392)
        check(
            bool(_refs392) and not _dangling392,
            f"Check 392: 全 aria idref / label-for ({len(_refs392)} 種) が定義済み id に解決 (a11y 関連付け健全)",
            f"Check 392: aria idref / label-for が未定義 id を指す (a11y 関連付け切れ・WCAG 1.3.1/4.1.2): {_dangling392} — "
            "id を片方でリネームすると screen reader が accessible name/description/control を解決できず "
            "ラベル無しの control をアナウンスする。定義側の id を復元するか idref を修正せよ"
            if _refs392 else
            "Check 392: shipped JS / index.html に静的 aria idref が見つからない — a11y idref wiring を検証できない",
            blocking=True,
        )
    else:
        check(False, "Check 392: index.html and shipped JS present",
              "Check 392: index.html または shipped JS が無い — aria idref の id 解決を検証できない", blocking=True)

    # ── 393. CONSTANTS.* reference → definition resolution (BLOCKING) ───────────────
    # 各 shipped JS の `CONSTANTS.<KEY>` (および `CONSTANTS.LIMITS.<M>` /
    # `CONSTANTS.POMODORO_DEFAULT_SETTINGS.<M>`) 参照は、js/constants.js で実際に定義された key に
    # 解決しなければならない。typo (例 CONSTANTS.LIMITS.MAX_TASSK) は合法な property access ゆえ
    # 静かに undefined へ評価され、throw も ESLint error も node --check 失敗も起きない。結果は silent
    # bug: undefined を `.slice(0, undefined)` の bound に使うと切り詰めが無効化し (配列全体を返す=
    # DoS/bloat ガード沈黙)、`setTimeout(fn, undefined)` は即発火する。Check 375/376/377/391/392 と
    # 同じ used⟹defined wiring レンズの CONSTANTS-access 面。top-level key と object-valued key
    # (LIMITS / POMODORO_DEFAULT_SETTINGS) の member を balanced-brace で抽出し、seg1 (top key) は常に、
    # seg2 は seg1 が既知 object key の時だけ検証する (scalar 定数への method chain
    # `CONSTANTS.STORAGE_KEY.slice(...)` を誤検出しない)。値が IIFE/式 (TAB_ID / DEBUG=先頭が '(') の
    # top key は object 扱いしないので内部が valid-key を汚染しない。cross-namespace typo
    # (CONSTANTS.LIMITS.work) は非対象 = 主要な misspelled-key class のみ強制する。
    _const393 = ROOT / "js" / "constants.js"
    _shipped393 = [p for p in ([ROOT / "main.js"] + sorted((ROOT / "js").glob("*.js"))) if p.exists()]
    if _const393.exists() and _shipped393:
        _csrc393 = _const393.read_text(encoding="utf-8")

        def _bal393(_s, _oi):
            # _oi は開き '{' の index。対応する閉じ '}' までの内側テキストを返す (balanced)。
            _d = 0
            for _j in range(_oi, len(_s)):
                if _s[_j] == "{":
                    _d += 1
                elif _s[_j] == "}":
                    _d -= 1
                    if _d == 0:
                        return _s[_oi + 1:_j]
            return _s[_oi + 1:]

        # top-level CONSTANTS keys = export 内の 4-space-indent `KEY:` (nested member は 8-space ゆえ除外)
        _top393 = set(re.findall(r"^    ([A-Za-z_]\w*)\s*:", _csrc393, re.M))
        # object-valued top key (`KEY: {`) の member key を balanced-brace で抽出
        _objmembers393 = {}
        for _tk393 in _top393:
            _mt393 = re.search(r"^    " + re.escape(_tk393) + r"\s*:\s*\{", _csrc393, re.M)
            if _mt393:
                _inner393 = _bal393(_csrc393, _mt393.end() - 1)
                _objmembers393[_tk393] = set(re.findall(r"\b([A-Za-z_]\w*)\s*:", _inner393))

        _bad393 = []
        for _f393 in _shipped393:
            _rel393 = str(_f393.relative_to(ROOT))
            # コメントは除去する (説明文中の `CONSTANTS.LIMITS.XXX` 例示を実参照と誤認しないため)。
            _src393f = re.sub(r"//[^\n]*", "", _f393.read_text(encoding="utf-8"))
            for _mm393 in re.finditer(r"\bCONSTANTS((?:\.[A-Za-z_]\w*)+)", _src393f):
                _segs393 = _mm393.group(1).lstrip(".").split(".")
                _seg1_393 = _segs393[0]
                if _seg1_393 not in _top393:
                    _bad393.append(f"CONSTANTS.{_seg1_393} ({_rel393})")
                elif len(_segs393) >= 2 and _seg1_393 in _objmembers393 and _segs393[1] not in _objmembers393[_seg1_393]:
                    _bad393.append(f"CONSTANTS.{_seg1_393}.{_segs393[1]} ({_rel393})")
            # [FIX] 分割代入で namespace を取り出した参照も辿る。従来は `CONSTANTS.` で始まる
            #   dotted access しか見ておらず、`const { LIMITS } = CONSTANTS; … LIMITS.MAX_TASSK` と
            #   書けば typo が素通りしていた (実測: leaf module へ注入しても GREEN)。
            #   `const { A, B: C } = CONSTANTS` の alias→top key 対応を作り、object-valued key の
            #   member 参照だけを検証する (scalar key の alias は method chain と区別できないため対象外)。
            for _dm393 in re.finditer(r"(?:const|let|var)\s*\{([^}]*)\}\s*=\s*CONSTANTS\b", _src393f):
                for _pair393 in _dm393.group(1).split(","):
                    _pp393 = [_x.strip() for _x in _pair393.split(":")]
                    if not _pp393 or not _pp393[0]:
                        continue
                    _key393 = _pp393[0]
                    _alias393 = _pp393[1] if len(_pp393) > 1 and _pp393[1] else _key393
                    if _key393 not in _top393:
                        _bad393.append(f"CONSTANTS.{_key393} (destructured, {_rel393})")
                        continue
                    if _key393 not in _objmembers393:
                        continue
                    for _am393 in re.finditer(r"\b" + re.escape(_alias393) + r"\.([A-Za-z_]\w*)", _src393f):
                        if _am393.group(1) not in _objmembers393[_key393]:
                            _bad393.append(f"CONSTANTS.{_key393}.{_am393.group(1)} (destructured as {_alias393}, {_rel393})")
        _bad393 = sorted(set(_bad393))
        check(
            bool(_top393) and not _bad393,
            f"Check 393: 全 CONSTANTS.* 参照 (top {len(_top393)} 種 + LIMITS/POMODORO member) が js/constants.js の定義に解決 (typo→undefined silent bug 防止)",
            f"Check 393: CONSTANTS.* 参照が js/constants.js の未定義 key を指す (silent undefined): {_bad393} — "
            "typo は合法な property access ゆえ throw せず undefined に評価され、slice bound / setTimeout delay を "
            "静かに壊す。js/constants.js に key を追加するか参照の typo を修正せよ"
            if _top393 else
            "Check 393: js/constants.js から top-level CONSTANTS key を抽出できない — CONSTANTS wiring を検証できない",
            blocking=True,
        )
    else:
        check(False, "Check 393: js/constants.js and shipped JS present",
              "Check 393: js/constants.js または shipped JS が無い — CONSTANTS 参照の解決を検証できない", blocking=True)

    # ── 395. Router.navigate() target (literal + データ駆動 path) → router route-segment resolution (BLOCKING) ──
    # 各 shipped JS の literal `Router.navigate('X')` は、base path segment (X から ?query を除き
    # 最初の '/' まで) が router.js _parseRoute の扱う top-level route segment (`case 'seg':` label、
    # または空文字=home default) に解決しなければならない。router.js は未知の第1 segment を
    # name:'home' として parse しホームを描画するため、typo した nav target
    # (`Router.navigate('rolesplit')`・リネーム後の stale target) はユーザーを意図先でなく silent に
    # ホームへ送る (throw も console error も e2e 失敗も無い。behavior e2e は各ルートを直接訪問した
    # 際の描画は見るが、in-page nav ボタンが live ルートを指すかは検査しない・screenshot は advisory)。
    # Check 377 (route.name ⟹ main.js render case) の producer 面の双子: 377 は consumer (parse 済
    # ルートに renderer が在る) を、395 は producer (nav 呼び出しが parse 可能ルートを指す) を守る。
    # template literal target (`apps/${app}` / `projects/${slug}`) は構造上動的ゆえ除外し no-`$` の
    # 文字列 literal のみ強制、JS 行コメントは strip して doc 例の false-positive を防ぐ。Check 375
    # (icon) / 376 (data-action) / 391 / 392 / 393 と同じ used⟹defined wiring レンズの navigate 面。
    _router395 = ROOT / "js" / "router.js"
    _shipped395 = [p for p in ([ROOT / "main.js"] + sorted((ROOT / "js").glob("*.js"))) if p.exists()]
    if _router395.exists() and _shipped395:
        _rsrc395 = _router395.read_text(encoding="utf-8")
        _segs395 = set(re.findall(r"case\s+['\"]([\w-]+)['\"]\s*:", _rsrc395))
        _segs395.add("")  # 空 navigate('') = home default
        _targets395 = {}  # target -> source file
        for _f395 in _shipped395:
            _t395 = re.sub(r"//[^\n]*", "", _f395.read_text(encoding="utf-8"))
            for _m395 in re.finditer(r"""Router\.navigate\(\s*['"]([^'"$]+)['"]""", _t395):
                _targets395.setdefault(_m395.group(1), str(_f395.relative_to(ROOT)))
            # データ駆動記法: `Router.navigate(<識別子>)` を呼ぶ file は nav 先を literal でなく
            # データ配列の `path: '<route>'` で持つ (sidebar / hiring-risk の CTA)。literal だけを
            # 見ると、その典型記法の typo (`path: 'setting'`) が全 gate を素通りして silent home
            # fallthrough を起こす — Check 112/130/375/376/393 と同じ「別記法の見逃し」class。
            if re.search(r"Router\.navigate\(\s*[A-Za-z_$][\w.$]*\s*\)", _t395):
                for _mp395 in re.finditer(r"""\bpath:\s*['"]([^'"$]*)['"]""", _t395):
                    _targets395.setdefault(_mp395.group(1), str(_f395.relative_to(ROOT)))
        _unresolved395 = sorted(
            f"{_tg395} ({_targets395[_tg395]})" for _tg395 in _targets395
            if _tg395.split("?")[0].split("/")[0] not in _segs395
        )
        check(
            bool(_segs395) and not _unresolved395,
            f"Check 395: 全 Router.navigate target ({len(_targets395)} 種・literal + データ駆動 path) が router.js の route segment ({len(_segs395) - 1} case) に解決 (silent home fallthrough 防止)",
            f"Check 395: Router.navigate の target が router.js の未定義 route segment を指す (silent home fallthrough): {_unresolved395} — "
            "router.js は未知の第1 segment を home として parse するため typo/リネーム残骸が全 gate を素通りして "
            "ユーザーをホームへ誤誘導する。router.js _parseRoute に該当 case を追加するか navigate target の typo を修正せよ",
            blocking=True,
        )
    else:
        check(False, "Check 395: js/router.js and shipped JS present",
              "Check 395: js/router.js または shipped JS が無い — Router.navigate target の解決を検証できない", blocking=True)

    # ── 396. Router route.name ⟹ PAGE_META entry (BLOCKING) ──
    # router.js _parseRoute が emit する全 route.name は js/page-meta.js の PAGE_META にエントリを
    # 持たねばならない。meta-management.js applyMeta は `PAGE_META[routeName]` が無いルートで早期
    # return するため、登録漏れのルートは <title> 更新 / SEO meta (desc/og) / route announcer title
    # (a11y 2.4.2) を silent に失う (throw も console error も無い・behavior e2e は描画は見るが title/
    # meta announcer は検査しない・screenshot advisory)。route.name の source: literal
    # `route.name = 'X'` + 初期 `{ name: 'home' }` default + `app-${app}` template を app whitelist
    # (`['task','todo',...]`) から展開。Check 377 (route.name ⟹ main.js render case) の consumer 面の
    # 双子 + Check 148 (ARTICLE_ROUTES ⊆ PAGE_META) の補完で route mesh の meta 面を閉じる
    # used⟹defined wiring。
    _router396 = ROOT / "js" / "router.js"
    _pagemeta396 = ROOT / "js" / "page-meta.js"
    if _router396.exists() and _pagemeta396.exists():
        _rsrc396 = re.sub(r"//[^\n]*", "", _router396.read_text(encoding="utf-8"))
        _routenames396 = set(re.findall(r"route\.name\s*=\s*['\"]([\w-]+)['\"]", _rsrc396))
        _routenames396.update(re.findall(r"\{\s*name:\s*['\"]([\w-]+)['\"]", _rsrc396))  # 初期 { name: 'home' }
        _appwl396 = re.search(r"\[([^\]]*)\]\.includes\(app\)", _rsrc396)
        if _appwl396 and re.search(r"app-\$\{app\}", _rsrc396):
            for _a396 in re.findall(r"['\"]([\w-]+)['\"]", _appwl396.group(1)):
                _routenames396.add(f"app-{_a396}")
        _psrc396 = _pagemeta396.read_text(encoding="utf-8")
        _mblock396 = re.search(r"export const PAGE_META\s*=\s*\{(.*)", _psrc396, re.S)
        _metakeys396 = set()
        if _mblock396:
            for _line396 in _mblock396.group(1).splitlines():
                _km396 = re.match(r"    (['\"]?)([A-Za-z][\w-]*)\1\s*:", _line396)
                if _km396:
                    _metakeys396.add(_km396.group(2))
        _missing396 = sorted(_routenames396 - _metakeys396)
        check(
            bool(_routenames396) and bool(_metakeys396) and not _missing396,
            f"Check 396: 全 router route.name ({len(_routenames396)} 種) が PAGE_META にエントリを持つ (applyMeta 早期 return による silent title/meta 欠落防止)",
            f"Check 396: router.js が emit する route.name が PAGE_META に未登録 (applyMeta が早期 return し title/SEO meta/route announcer を silent 欠落): {_missing396} — "
            "js/page-meta.js の PAGE_META に該当ルートの {title, desc} を追加せよ",
            blocking=True,
        )
    else:
        check(False, "Check 396: js/router.js and js/page-meta.js present",
              "Check 396: js/router.js または js/page-meta.js が無い — route.name ⟹ PAGE_META の解決を検証できない", blocking=True)

    # ── 401. quiz?type= リテラル ⟹ QUIZ_TITLES キー / sidebar 非 aws 集合の一致 (BLOCKING) ─────
    # QuizPage は `QUIZ_DATA_MAP[quizType] || QUIZ_DATA_MAP.aws` で描画するため、リンク側の type が
    # typo/未定義でも **例外にならず AWS 問題集が描画される**。「PM問題集」ボタンを押すと黙って AWS の
    # 問題が出る silent wrong-content class (Check 375/376/377/393 と同じ used⟹defined wiring レンズ)。
    # 401b は sidebar の active 判定が持つ非 aws キーのハードコード集合 (`['pm','quality','architecture']`)
    # が map と一致することを強制する — 5 つ目の quiz を足すと、その page は正しく描画されるのに nav は
    # 「AWS 問題集」を active に光らせる control↔content desync (#781 class) が silent に生まれるため。
    _qr401 = ROOT / "js" / "quiz-renderer.js"
    _cp401 = ROOT / "js" / "components.js"
    if _qr401.exists() and _cp401.exists():
        _qsrc401 = _qr401.read_text(encoding="utf-8")
        # [FIX 2026-08-21] 単一ソースは `QUIZ_DATA_MAP` から **`QUIZ_TITLES`** へ改名された
        #   (問題集データを動的 import で遅延読み込みへ移し、タイトルだけ静的に残したため)。
        #   キー集合の invariant は不変で、走査先の名前だけが変わっている。
        _mblock401 = re.search(r"const QUIZ_TITLES = \{(.*?)\};", _qsrc401, re.S)
        _keys401 = set(re.findall(r"^\s*(\w+)\s*:", _mblock401.group(1), re.M)) if _mblock401 else set()

        # 401a: shipped JS/HTML の全 `quiz?type=X` リテラルが map キーに解決する
        _consumers401 = [ROOT / "main.js", ROOT / "index.html"] + sorted((ROOT / "js").glob("*.js"))
        _used401 = {}
        for _f401 in _consumers401:
            if not _f401.exists():
                continue
            # honest carve-out: 行全体がコメントの行を除外する。components.js は「無効 type
            # (#/quiz?type=zzz 等 stale bookmark/手打ち) でも AWS が出る」という**フォールバック挙動の
            # 説明**を WHY コメントに書いており、それを実リンクと誤検出しないため (Check 364 と同じく
            # 実バグでなく設計記述を捕捉した false-positive は honest に carve-out する)。行末コメントは
            # 除外しない (コード行に紛れた実リテラルを見落とさないため)。
            _body401 = "\n".join(
                _ln401 for _ln401 in _f401.read_text(encoding="utf-8").splitlines()
                if not re.match(r"\s*(//|\*|/\*|<!--)", _ln401))
            for _t401 in re.findall(r"quiz\?type=([\w-]+)", _body401):
                _used401.setdefault(_t401, []).append(_f401.name)
        _unresolved401 = sorted(t for t in _used401 if t not in _keys401)
        check(
            bool(_keys401) and bool(_used401) and not _unresolved401,
            f"Check 401a: 全 quiz?type= リテラル ({len(_used401)} 種) が QUIZ_TITLES キー ({len(_keys401)} 種) に解決",
            f"Check 401a: quiz?type= の type が QUIZ_TITLES に未定義: "
            f"{[(t, _used401[t]) for t in _unresolved401]} — QuizPage は `|| QUIZ_DATA_MAP.aws` で "
            "フォールバックするため例外にならず、リンクのラベルと無関係な AWS 問題集が silent に描画される。"
            "type を実キーへ直すか QUIZ_TITLES に定義を足せ",
            blocking=True,
        )

        # 401b: sidebar の active 判定が除外する非 aws キー集合 == map キー − {aws}
        _csrc401 = _cp401.read_text(encoding="utf-8")
        _excl401 = re.search(r"!\[([^\]]*)\]\.includes\(route\.query\.type\)", _csrc401)
        _exclset401 = set(re.findall(r"'([\w-]+)'", _excl401.group(1))) if _excl401 else set()
        _expect401 = _keys401 - {"aws"}
        check(
            bool(_excl401) and _exclset401 == _expect401,
            f"Check 401b: sidebar の AWS-active 除外集合 {sorted(_exclset401)} == QUIZ_TITLES − aws {sorted(_expect401)}",
            f"Check 401b: components.js の AWS-active 除外集合 {sorted(_exclset401)} が QUIZ_TITLES − aws "
            f"{sorted(_expect401)} と不一致 (欠落={sorted(_expect401 - _exclset401)} / 余剰={sorted(_exclset401 - _expect401)})。"
            "新しい quiz を足すと、その page は正しく描画されるのに nav は「AWS 問題集」を active に光らせる "
            "control↔content desync が silent に生まれる (#781 class)。除外集合を map と同期せよ",
            blocking=True,
        )
    else:
        check(False, "Check 401: js/quiz-renderer.js and js/components.js present",
              "Check 401: js/quiz-renderer.js または js/components.js が無い — quiz?type wiring を検証できない", blocking=True)

