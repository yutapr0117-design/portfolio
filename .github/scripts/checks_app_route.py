"""
checks_app_route.py — app-route whitelist coherence-mesh checks
(extracted from check_repository_consistency.py — check.py split track・category "app-route mesh").

This module owns the contiguous cluster of Checks 136-140 that hold the SPA's app-route
whitelist (js/router.js `[...].includes(app)`) as the single source of truth and machine-enforce
that every producer/consumer of the app list stays in agreement: store.js demoRoute (136),
main.js render switch (137), Sidebar app-nav (138), AppsPage app index (139), and the Settings
demo selector (140). Each Check reads its own target files directly (js/router.js, main.js,
js/components.js, js/settings-page.js) via Path.read_text(); none depends on the monolith's
global html/style/mainjs content, so the cluster is self-contained and needs no ctx enrichment.
Every local is `_NNN`-suffixed and confined to its section.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  136. demoRoute ↔ router app whitelist coherence: store.js normalizeProject() validates an imported
       project's demoRoute against a hardcoded app whitelist, and router.js resolves apps/<app> routes
       against its own hardcoded whitelist. These two lists must stay in sync — if router gains an app
       (e.g. 'notes' was added for the A-group Markdown notes app) but the store whitelist is not
       updated, importing a project whose demoRoute names the new app SILENTLY drops it to null (the
       demo button vanishes — a data-fidelity loss of the same class as Check 128 and the #139 profile
       strip). This Check parses both arrays and asserts the store demoRoute whitelist equals the router
       app whitelist, making "router supports app X ⟹ X is a valid project demoRoute" an enforced
       invariant. (BLOCKING)
  137. router app whitelist ↔ main.js render switch coherence: router.js resolves apps/<app> to
       route.name `app-<app>` for app in its whitelist, and main.js's renderer switch consumes that
       route.name via `case 'app-<app>':` to render the app component. Check 128 (cmdk) and 136 (store)
       constrain the PRODUCER side of the router whitelist, but the CONSUMER side (main.js switch) is
       only tied INDIRECTLY through ALL_ROUTES (Check 58) — so updating router + cmdk + store while
       forgetting main.js/ALL_ROUTES leaves every Check green yet makes apps/<app> fall through to
       not-found (a SILENT 404 while the palette and project demos still offer the route). This Check
       parses the router whitelist and the set of main.js `case 'app-<X>':` labels and asserts bijection,
       making "router can route app X ⟹ main.js can render app X" a directly enforced invariant (the
       missing direct edge in the app-route coherence mesh of Check 58/118/128/136). (BLOCKING)
  138. Sidebar app-nav ↔ router app whitelist coverage: the Sidebar (js/components.js) lab-nav lists
       built-in apps as `path: 'apps/<app>'` quick-nav links, and AppsPage lists every app as a card.
       Like the command palette (Check 128), the sidebar must cover every router-routable app — when the
       Markdown notes app was added (A-group) it was added to AppsPage + the palette (#257) but FORGOTTEN
       in the sidebar, so notes was the only built-in app unreachable from the persistent left nav. This
       Check parses the router whitelist and the sidebar's `path: 'apps/<app>'` entries and asserts every
       router app appears in the sidebar, making "router can route app X ⟹ X is in the sidebar nav" an
       enforced invariant (the sidebar counterpart of Check 128). (BLOCKING)
  139. AppsPage app index ↔ router app whitelist coverage: AppsPage (js/components.js) is the canonical
       "アプリ一覧" index — it renders every built-in app as a card whose "開く" button navigates to
       apps/<id>. It is the third app-route PRODUCER surface (with the palette/Check 128 and the
       sidebar/Check 138) but was the only one left unenforced. If the AppsPage `apps` array drifts from
       the router whitelist (a new app added to router/main.js/cmdk/sidebar but forgotten here), that app
       becomes undiscoverable from the canonical index even though it routes everywhere else. This Check
       scopes to the AppsPage `const apps = [...]` array, parses its `id: '<app>'` entries, and asserts
       every router app appears, completing the app-route coherence mesh so all three producer surfaces
       (palette/sidebar/AppsPage) track the router whitelist. (BLOCKING)
  140. Settings demo selector ↔ router app whitelist coverage: The Settings page manual-add form
       (js/apps.js SettingsPage) lets a user create a project and pick which app it demos via a
       `<select>` whose onchange writes `settingsNewDemo`. Its `<option value='<app>'>` list is the WRITE
       surface that decides which apps a hand-created project can ever link as a demoRoute. store.js
       normalizeProject accepts demoRoute ∈ router whitelist (Check 136) and the router can route every
       app, but if this selector drifts (a new app added to router/store/main.js/cmdk/sidebar/AppsPage but
       forgotten here), that app is silently unselectable as a demo — the exact recurring class where
       notes was forgotten in the store/sidebar/AppsPage/palette (#257/#292/#293). This Check scopes to
       the demo selector block, parses its non-empty `value: '<app>'` options, and asserts they equal the
       router whitelist (the empty "Demoなし" option is allowed), so every routable app stays selectable
       as a project demo. (BLOCKING)
"""
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 136. demoRoute ↔ router app whitelist coherence (BLOCKING) ─────────────────
    # store.js normalizeProject() は import したプロジェクトの demoRoute を hardcode された app
    # whitelist で検証し、router.js は apps/<app> ルートを自身の hardcode whitelist で解決する。
    # 両者は同期している必要がある — router に app が増えた (例: A 群で notes app 追加) のに store
    # 側 whitelist を更新し忘れると、その新 app を demoRoute に持つプロジェクトを import した際に
    # silent に null へ落ち、デモボタンが消える (Check 128 / #139 と同じ data-fidelity loss)。両配列を
    # parse し store demoRoute whitelist == router app whitelist を強制し、「router が app X を
    # サポート ⟹ X は有効な demoRoute」を invariant 化する。
    _router136 = ROOT / "js" / "router.js"
    _store136 = ROOT / "js" / "store.js"
    if _router136.exists() and _store136.exists():
        _rsrc136 = _router136.read_text(encoding="utf-8")
        _ssrc136 = _store136.read_text(encoding="utf-8")
        # router: [...].includes(app)
        _rm136 = re.search(r"\[([^\]]*)\]\.includes\(app\)", _rsrc136)
        # store: [...].includes(raw.demoRoute)
        _sm136 = re.search(r"\[([^\]]*)\]\.includes\(raw\.demoRoute\)", _ssrc136)

        def _parse_list136(_raw):
            return set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _raw or ""))

        _router_apps136 = _parse_list136(_rm136.group(1) if _rm136 else "")
        _store_apps136 = _parse_list136(_sm136.group(1) if _sm136 else "")
        _missing136 = _router_apps136 - _store_apps136
        _extra136 = _store_apps136 - _router_apps136
        check(
            bool(_router_apps136) and bool(_store_apps136) and not _missing136 and not _extra136,
            f"Check 136: store demoRoute whitelist == router app whitelist ({sorted(_router_apps136)})",
            f"Check 136: demoRoute ↔ router app whitelist drift — router のみ: {sorted(_missing136)} / "
            f"store のみ: {sorted(_extra136)}。store.js normalizeProject の demoRoute whitelist を "
            f"router.js の app whitelist と一致させよ (import 時の demoRoute silent-drop を防ぐ)"
            if (_router_apps136 and _store_apps136) else
            "Check 136: router/store の app whitelist 配列を parse できない (両ファイルの構造を確認せよ)",
            blocking=True,
        )
    else:
        check(False, "Check 136: js/router.js and js/store.js present",
              "Check 136: js/router.js または js/store.js が無い — demoRoute coherence を検証できない", blocking=True)

    # ── 137. router app whitelist ↔ main.js render switch coherence (BLOCKING) ──────
    # router.js は `apps/<app>` を app ∈ whitelist のとき route.name=`app-<app>` に解決し、main.js の
    # renderer switch がその route.name を `case 'app-<app>':` で受けて app コンポーネントを描画する。
    # Check 128 (cmdk) / 136 (store) は router whitelist の「提供側」を縛るが、「消費側」の main.js switch
    # は ALL_ROUTES 経由 (Check 58) でしか間接的に縛られない。ゆえに router + cmdk + store だけ更新して
    # main.js/ALL_ROUTES を忘れると、全 Check 緑のまま apps/<app> が default(not-found) へ落ち silent に
    # 404 化する (palette/project demo は依然その route を提示する)。router whitelist と main.js の
    # `case 'app-<X>':` 集合を parse し bijection を強制し、「router が app X を route 可能 ⟹ main.js が
    # app X を描画可能」を直接 invariant 化する (Check 58/118/128/136 の app-route coherence mesh に
    # 欠けていた直接 edge)。
    _router137 = ROOT / "js" / "router.js"
    _main137 = ROOT / "main.js"
    if _router137.exists() and _main137.exists():
        _rsrc137 = _router137.read_text(encoding="utf-8")
        _msrc137 = _main137.read_text(encoding="utf-8")
        _rm137 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _rsrc137)
        _router_apps137 = set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _rm137.group(1))) if _rm137 else set()
        _main_app_cases137 = set(re.findall(r"case\s+['\"]app-([a-z0-9_-]+)['\"]\s*:", _msrc137))
        _missing137 = _router_apps137 - _main_app_cases137  # router が生成するが main.js が描画不能 → silent 404
        _extra137 = _main_app_cases137 - _router_apps137     # main.js に case はあるが router が生成しない → dead case
        check(
            bool(_router_apps137) and bool(_main_app_cases137) and not _missing137 and not _extra137,
            f"Check 137: main.js の case 'app-<app>' == router app whitelist ({sorted(_router_apps137)})",
            f"Check 137: router ↔ main.js render switch drift — main.js に case 欠落 (silent 404): {sorted(_missing137)} / "
            f"main.js のみ (dead case): {sorted(_extra137)}。main.js renderer switch の `case 'app-<app>':` を "
            f"router.js の app whitelist と一致させよ (apps/<app> の silent not-found を防ぐ)"
            if (_router_apps137 and _main_app_cases137) else
            "Check 137: router.js の app whitelist (`[...].includes(app)`) または main.js の `case 'app-<X>':` を parse できない",
            blocking=True,
        )
    else:
        check(False, "Check 137: js/router.js and main.js present",
              "Check 137: js/router.js または main.js が無い — router↔switch coherence を検証できない", blocking=True)

    # ── 138. Sidebar app-nav ↔ router app whitelist coverage (BLOCKING) ────────────
    # Sidebar (js/components.js) の lab-nav は built-in app を `path: 'apps/<app>'` の quick-nav
    # リンクとして列挙し、AppsPage は全 app をカードで列挙する。command palette (Check 128) と同様、
    # sidebar も router が route 可能な全 app を被覆すべきである。A 群で Markdown notes app を追加した際、
    # AppsPage と palette (#257) には足したが sidebar には足し忘れ、notes だけが常設左ナビから到達不能
    # だった。router whitelist と sidebar の `path: 'apps/<app>'` エントリを parse し、router の全 app が
    # sidebar に出ることを強制し「router が app X を route 可能 ⟹ X は sidebar nav にある」を invariant
    # 化する (Check 128 の sidebar 版)。
    _router138 = ROOT / "js" / "router.js"
    _comp138 = ROOT / "js" / "components.js"
    if _router138.exists() and _comp138.exists():
        _rsrc138 = _router138.read_text(encoding="utf-8")
        _csrc138 = _comp138.read_text(encoding="utf-8")
        _rm138 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _rsrc138)
        _router_apps138 = set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _rm138.group(1))) if _rm138 else set()
        # sidebar の quick-nav リンクは `path: 'apps/<app>'` リテラル (AppsPage は `apps/${id}` テンプレ
        # ゆえ非該当)。apps index ('apps' 単体) は app ではないので slash 付きのみ抽出。
        _sidebar_apps138 = set(re.findall(r"path:\s*['\"]apps/([a-z0-9_-]+)['\"]", _csrc138))
        _missing138 = _router_apps138 - _sidebar_apps138
        check(
            bool(_router_apps138) and not _missing138,
            f"Check 138: sidebar nav が router の全 app を被覆 ({sorted(_router_apps138)})",
            f"Check 138: sidebar app-nav に router app route が欠落: {sorted(_missing138)} — "
            f"js/components.js の Sidebar labItems に `{{ ..., path: 'apps/<app>', ... }}` を追加せよ "
            f"(常設左ナビから到達不能になる・#257 と同 class)"
            if _router_apps138 else
            "Check 138: router.js の app whitelist (`[...].includes(app)`) を parse できない — coverage 検証が無効化された",
            blocking=True,
        )
    else:
        check(False, "Check 138: js/router.js and js/components.js present",
              "Check 138: js/router.js または js/components.js が無い — sidebar↔router coverage を検証できない", blocking=True)

    # ── 139. AppsPage app index ↔ router app whitelist coverage (BLOCKING) ──────────
    # AppsPage (js/components.js) は canonical な「アプリ一覧」index で、全 built-in app をカードで描画し
    # 各「開く」ボタンが apps/<id> へ遷移する。command palette (Check 128) / sidebar (Check 138) と並ぶ
    # 3 つ目の app-route producer 面だが、唯一未強制だった。AppsPage の `apps` 配列が router whitelist
    # から drift する (router/main.js/cmdk/sidebar には新 app を足したが AppsPage を忘れる) と、その app は
    # 他では route できるのに canonical index から発見不能になる。AppsPage の `const apps = [...]` 配列に
    # scope して `id: '<app>'` を parse し、router の全 app が出ることを強制する。これで 3 producer 面
    # (palette/sidebar/AppsPage) が全て router whitelist に追従し app-route coherence mesh が閉じる。
    _router139 = ROOT / "js" / "router.js"
    _comp139 = ROOT / "js" / "components.js"
    if _router139.exists() and _comp139.exists():
        _rsrc139 = _router139.read_text(encoding="utf-8")
        _csrc139 = _comp139.read_text(encoding="utf-8")
        _rm139 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _rsrc139)
        _router_apps139 = set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _rm139.group(1))) if _rm139 else set()
        # AppsPage の apps 配列に scope (他所の id: と混同しないため function AppsPage 内の const apps を抽出)
        _appspage139 = re.search(r"function AppsPage\(\)\s*\{.*?const apps\s*=\s*\[(.*?)\];", _csrc139, re.DOTALL)
        _appspage_apps139 = set(re.findall(r"id:\s*['\"]([a-z0-9_-]+)['\"]", _appspage139.group(1))) if _appspage139 else set()
        _missing139 = _router_apps139 - _appspage_apps139
        check(
            bool(_router_apps139) and bool(_appspage_apps139) and not _missing139,
            f"Check 139: AppsPage index が router の全 app を被覆 ({sorted(_router_apps139)})",
            f"Check 139: AppsPage index に router app が欠落: {sorted(_missing139)} — "
            f"js/components.js の AppsPage `const apps = [...]` に `{{ id: '<app>', title: ..., desc: ..., icon: ... }}` を追加せよ "
            f"(canonical アプリ一覧から発見不能になる)"
            if (_router_apps139 and _appspage_apps139) else
            "Check 139: router.js の app whitelist または AppsPage の `const apps = [...]` を parse できない (構造を確認せよ)",
            blocking=True,
        )
    else:
        check(False, "Check 139: js/router.js and js/components.js present",
              "Check 139: js/router.js または js/components.js が無い — AppsPage↔router coverage を検証できない", blocking=True)

    # ── 140. Settings demo selector ↔ router app whitelist coverage (BLOCKING) ──────
    # Settings の手動追加フォーム (js/apps.js SettingsPage) は、ユーザーがプロジェクトを作成し、その
    # プロジェクトがどの app をデモするかを `<select>` (onchange が settingsNewDemo を書き込む) で選ばせる。
    # この `<option value='<app>'>` リストは「手動作成プロジェクトが demoRoute に持てる app」を決める
    # WRITE 面である。store.js normalizeProject は demoRoute ∈ router whitelist を許容し (Check 136)、
    # router は全 app を route できるが、このセレクタが drift する (新 app を router/store/main.js/cmdk/
    # sidebar/AppsPage に足したがここを忘れる) と、その app は demo として silent に選択不能になる — notes が
    # store/sidebar/AppsPage/palette で忘れられた #257/#292/#293 と同一の再発クラス。デモセレクタブロックに
    # scope して非空の `value: '<app>'` オプションを parse し、router whitelist と一致することを強制する
    # (空の "Demoなし" オプションは許可)。これで全 routable app がプロジェクト demo として選択可能に保たれる。
    # 2026-07-05: SettingsPage を js/apps.js → js/settings-page.js へ分離したため Demo セレクタの探索先を追従。
    _apps140 = ROOT / "js" / "settings-page.js"
    _router140 = ROOT / "js" / "router.js"
    if _apps140.exists() and _router140.exists():
        _asrc140 = _apps140.read_text(encoding="utf-8")
        _rsrc140 = _router140.read_text(encoding="utf-8")
        _rm140 = re.search(r"\[([^\]]*)\]\.includes\(\s*app\s*\)", _rsrc140)
        _router_apps140 = set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _rm140.group(1))) if _rm140 else set()
        # settingsNewDemo を書き込む onchange を持つ select の option 群に scope。anchor は distinctive な
        # aria-label、終端は次の addProjectManual 配線 (フォームの「追加」ボタン)。
        _anchor140 = _asrc140.find("'Demo アプリの種類'")
        _block140 = ""
        if _anchor140 != -1:
            _endpos140 = _asrc140.find("addProjectManual", _anchor140)
            _block140 = _asrc140[_anchor140:_endpos140 if _endpos140 != -1 else _anchor140 + 800]
        # value: settingsNewDemo (無引用符) は対象外。value: '' (Demoなし) は空ゆえ除外。
        _demo_opts140 = set(v for v in re.findall(r"value:\s*['\"]([a-z0-9_-]*)['\"]", _block140) if v)
        _missing140 = _router_apps140 - _demo_opts140
        _extra140 = _demo_opts140 - _router_apps140
        check(
            bool(_router_apps140) and bool(_demo_opts140) and not _missing140 and not _extra140,
            f"Check 140: Settings demo selector options == router app whitelist ({sorted(_router_apps140)})",
            f"Check 140: Settings demo selector ↔ router app whitelist drift — selector に欠落 (demo 選択不能): "
            f"{sorted(_missing140)} / selector のみ (dead option): {sorted(_extra140)}。js/settings-page.js SettingsPage の "
            f"Demo セレクタに `h('option', {{ value: '<app>' }}, '<app>')` を追加/削除し router whitelist と一致させよ "
            f"(全 routable app をプロジェクト demo として選択可能に保つ・#257 と同 class)"
            if (_router_apps140 and _demo_opts140) else
            "Check 140: router.js の app whitelist または Settings の Demo セレクタ option を parse できない (構造を確認せよ)",
            blocking=True,
        )
    else:
        check(False, "Check 140: js/settings-page.js and js/router.js present",
              "Check 140: js/settings-page.js または js/router.js が無い — Settings demo selector coverage を検証できない", blocking=True)
