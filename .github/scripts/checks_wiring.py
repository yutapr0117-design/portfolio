"""
checks_wiring.py — shipped-asset & AIO wiring / discoverability checks
(extracted from check_repository_consistency.py — check.py split track・category "wiring/discovery").

This module owns the cluster of Checks 132-134 (plus 375, 376) that assert shipped assets and AIO
evidence are actually wired up and discoverable (not merely present): AIO evidence ↔ sitemap
discoverability (132), aio-guard.js `<script src>` wiring (133), root-script wiring
completeness (134), and shipped-JS createIcon name → icon-registry resolution (375, the
"used icon name ⟹ it is actually defined" wiring twin of 133/134's "file exists ⟹ wired").
Each Check reads its own target files directly (index.html, sitemap.xml,
aio-manifest.json, js/*.js) via Path.read_text(); a free-variable analysis confirms zero external `_`-vars
and no global html/style/mainjs dependency, so the cluster is self-contained and needs no ctx
enrichment. NOTE: Check 135 (stylesheet wiring) is the natural sibling but reads the global
`style` content, so it stays in the monolith until a ctx-enrich phase.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  132. AIO evidence ↔ sitemap discoverability: every text document registered as authoritative
       evidence in .well-known/aio-manifest.json (source_of_truth / supporting_evidence /
       observational_evidence whose path ends in .md / .txt / .json) must also appear as a <loc> in
       sitemap.xml. The manifest declares a doc authoritative for AI crawlers, but a crawler that
       discovers the site via sitemap.xml will never reach a registered doc that is absent from the
       sitemap — a silent discoverability gap (real-work-claims.md and AI2AI-archive.md were
       registered but missing from the sitemap until this Check was added). Binary assets
       (.webp/.mp3) are excluded (images/audio are not sitemap-indexed text). This makes
       "registered-as-evidence ⟹ sitemap-discoverable" an enforced invariant. (BLOCKING)
  133. AIO guard script wiring: aio-guard.js is the AIO asset-anchor lifecycle monitor & self-repair
       mechanism — it watches the hidden <div id="aio-asset-anchor"> and restores it if any AI-run
       "dead code purge" removes it (the anchor is invisible but semantically critical to the AIO
       layer). The monitor only works if index.html actually loads it before the main SPA IIFE.
       The mirror-bijection check only asserts the FILE exists; nothing enforced that index.html
       still REFERENCES it, so deleting the <script src="./aio-guard.js"> tag would leave the file
       present (verify green) while silently deactivating the self-repair monitor — only a
       non-blocking CI advisory caught this. This Check asserts index.html contains a
       <script src="./aio-guard.js"> reference, making "guard file exists ⟹ guard is wired" an
       enforced invariant (regression guard for the AIO self-repair monitor). (BLOCKING)
  134. Root script wiring completeness: index.html must keep loading the root scripts it depends
       on (theme-init.js / karte-init.js / main.js) via a <script src> reference. Like Check 133
       (aio-guard.js), the mirror-bijection only asserts the FILE exists — nothing enforced that the
       <script> tag remains. Removal degrades SILENTLY: theme-init.js is the pre-paint FOUC guard
       (its loss is a flash of unstyled/wrong-theme content that no behavior e2e asserts, and the
       screenshot e2e is now ADVISORY per §3(B) so it would not block); karte-init.js silently
       disables analytics; main.js is the SPA entry point (e2e catches its loss, but a static check
       makes the entry-point wiring explicit and survives an e2e outage). error-suppressor.js is
       NOT covered here because it is inlined (Check 7/7b enforce its inline byte-identity + CSP
       hash), and aio-guard.js is covered by Check 133. This makes "root script file exists ⟹ it is
       wired into index.html" an enforced invariant for the remaining external root scripts.
       (BLOCKING)
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
       invariant so a typo can never silently blank an icon. (BLOCKING)
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
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 132. AIO evidence ↔ sitemap discoverability (BLOCKING) ────────────────────
    # aio-manifest.json に authoritative evidence として登録された text doc (.md/.txt/.json) は
    # sitemap.xml の <loc> にも載っていなければならない。manifest は AI crawler 向けに doc を権威と
    # 宣言するが、sitemap 経由で discovery する crawler は sitemap 未掲載の登録 doc に到達できない
    # (silent discoverability gap。real-work-claims.md / AI2AI-archive.md が登録済なのに sitemap 欠落
    # だった)。binary (.webp/.mp3) は sitemap-index 対象外ゆえ除外。「evidence 登録 ⟹ sitemap 到達可」
    # を機械強制する。
    _manifest132 = ROOT / ".well-known" / "aio-manifest.json"
    _sitemap132 = ROOT / "sitemap.xml"
    if _manifest132.exists() and _sitemap132.exists():
        _mdata132 = json.loads(_manifest132.read_text(encoding="utf-8"))
        _sitemap_src132 = _sitemap132.read_text(encoding="utf-8")
        _ev_paths132 = []
        for _sec132 in ("source_of_truth", "supporting_evidence", "observational_evidence"):
            for _e132 in _mdata132.get(_sec132, []):
                _p132 = _e132.get("path", "")
                if _p132.endswith((".md", ".txt", ".json")):
                    _ev_paths132.append(_p132)
        _missing132 = [p for p in _ev_paths132 if ("/" + p + "<") not in _sitemap_src132 and ("/" + p + "\n") not in _sitemap_src132 and (p + "</loc>") not in _sitemap_src132]
        check(
            bool(_ev_paths132) and not _missing132,
            f"Check 132: aio-manifest の text evidence {len(_ev_paths132)} 件すべてが sitemap.xml に <loc> 掲載 (crawler discoverability)",
            f"Check 132: aio-manifest 登録 evidence が sitemap.xml に欠落: {_missing132} — "
            "登録済 doc は sitemap.xml にも <loc> を追加せよ (sitemap 経由 crawler が到達できない discoverability gap)"
            if _ev_paths132 else
            "Check 132: aio-manifest から text evidence path を抽出できない (manifest 構造を確認せよ)",
            blocking=True,
        )
    else:
        check(False, "Check 132: aio-manifest.json / sitemap.xml present",
              "Check 132: aio-manifest.json または sitemap.xml が無い — AIO evidence↔sitemap 整合を検証できない", blocking=True)

    # ── 133. AIO guard script wiring (BLOCKING) ───────────────────────────────────
    # aio-guard.js は AIO asset-anchor の lifecycle monitor & self-repair 機構で、hidden な
    # <div id="aio-asset-anchor"> を監視し AI の "dead code purge" 等で除去されたら復元する
    # (anchor は不可視だが AIO 層に semantically critical)。この monitor は index.html が main SPA
    # IIFE より前に aio-guard.js を実際に load して初めて稼働する。mirror-bijection は FILE の存在
    # しか見ないため、<script src="./aio-guard.js"> タグを消しても file は残り verify は緑のまま
    # monitor だけが silent に無効化される (従来は非ブロックの CI advisory だけが捕捉)。本 Check は
    # index.html が aio-guard.js を script 参照することを BLOCKING 強制し、「guard file 存在 ⟹ guard
    # が配線済」を invariant 化する (AIO self-repair monitor の回帰ガード)。
    _index133 = ROOT / "index.html"
    if _index133.exists():
        _html133 = _index133.read_text(encoding="utf-8")
        _wired133 = re.search(r'<script\b[^>]*\bsrc\s*=\s*["\']\.?/?aio-guard\.js["\']', _html133)
        check(
            bool(_wired133),
            "Check 133: index.html が aio-guard.js を <script src> 参照 (AIO self-repair monitor が配線済)",
            "Check 133: index.html に <script src=\"./aio-guard.js\"> 参照が無い — "
            "aio-guard.js (AIO asset-anchor self-repair monitor) が load されず silent に無効化される。"
            "main IIFE より前に <script src=\"./aio-guard.js\"></script> を index.html へ戻せ",
            blocking=True,
        )
    else:
        check(False, "Check 133: index.html present",
              "Check 133: index.html が無い — aio-guard.js の配線を検証できない", blocking=True)

    # ── 134. Root script wiring completeness (BLOCKING) ───────────────────────────
    # index.html が依存する root スクリプト (theme-init.js / karte-init.js / main.js) を
    # <script src> で実際に load し続けることを BLOCKING 強制する。Check 133 (aio-guard.js) と
    # 同様、mirror-bijection は FILE 存在しか見ず <script> タグの残存は強制されない。タグ除去は
    # silent に劣化する: theme-init.js は pre-paint FOUC ガード (除去すると未スタイル/誤テーマの
    # 一瞬の flash になるが behavior e2e は検査せず、screenshot e2e は §3(B) で advisory ゆえ block
    # しない)、karte-init.js は analytics を無音停止、main.js は SPA エントリポイント (除去は e2e が
    # 捕捉するが静的 check でエントリ配線を明示し e2e 不在時も生存させる)。error-suppressor.js は
    # inline ゆえ対象外 (Check 7/7b が inline byte-identity + CSP hash を強制)、aio-guard.js は
    # Check 133 が担当。「root script file 存在 ⟹ index.html に配線済」を残る外部 root script へ
    # invariant 化する。
    _index134 = ROOT / "index.html"
    if _index134.exists():
        _html134 = _index134.read_text(encoding="utf-8")
        _required134 = ["theme-init.js", "karte-init.js", "main.js"]
        _unwired134 = [
            _s for _s in _required134
            if not re.search(r'<script\b[^>]*\bsrc\s*=\s*["\']\.?/?' + re.escape(_s) + r'["\']', _html134)
        ]
        check(
            not _unwired134,
            f"Check 134: index.html が依存 root script {_required134} をすべて <script src> 配線 (silent degradation 防止)",
            f"Check 134: index.html に <script src> 配線が欠落: {_unwired134} — "
            "これらは除去しても file が残り verify 緑のまま silent に劣化する "
            "(theme-init.js=FOUC / karte-init.js=analytics / main.js=SPA entry)。index.html へ "
            "<script src> 参照を戻せ",
            blocking=True,
        )
    else:
        check(False, "Check 134: index.html present",
              "Check 134: index.html が無い — root script の配線を検証できない", blocking=True)

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
        for _f375 in sorted((ROOT / "js").glob("*.js")):
            _t375 = _f375.read_text(encoding="utf-8")
            for _pat375 in (r"createIcon\(\s*['\"]([A-Za-z][\w-]*)['\"]",
                            r"\bicon\s*:\s*['\"]([A-Za-z][\w-]*)['\"]"):
                for _mm375 in re.finditer(_pat375, _t375):
                    _used375.setdefault(_mm375.group(1), str(_f375.relative_to(ROOT)))
        _unresolved375 = sorted(
            f"{_n375} ({_used375[_n375]})" for _n375 in _used375 if _n375 not in _keys375
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
    # 強制しない: `drawer:close` は意図的に symmetric な unused handler (drawer は直接 onclick /
    # Escape / nav-click で閉じる) ゆえ used⟹defined ガードで bijection ではない。
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
        for _f376 in sorted((ROOT / "js").glob("*.js")):
            _t376 = re.sub(r"//[^\n]*", "", _f376.read_text(encoding="utf-8"))
            for _pat376 in (r"data-action\s*=\s*['\"]([A-Za-z][\w:-]*)['\"]",
                            r"['\"]data-action['\"]\s*:\s*['\"]([A-Za-z][\w:-]*)['\"]"):
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
        _defined392 = set()
        for _f392 in _sources392:
            _s392 = _f392.read_text(encoding="utf-8")
            _defined392 |= set(re.findall(r'\bid="([a-zA-Z0-9_-]+)"', _s392))
            _defined392 |= set(re.findall(r"""\bid:\s*['"]([a-zA-Z0-9_-]+)['"]""", _s392))
            _defined392 |= set(re.findall(r"""\.id\s*=\s*['"]([a-zA-Z0-9_-]+)['"]""", _s392))
            _defined392 |= set(re.findall(r"""setAttribute\(\s*['"]id['"]\s*,\s*['"]([a-zA-Z0-9_-]+)['"]""", _s392))
        _refs392 = {}  # idref value -> (attr, file)
        _aria392 = ["aria-labelledby", "aria-describedby", "aria-controls", "aria-errormessage"]
        for _f392 in _sources392:
            _s392 = _f392.read_text(encoding="utf-8")
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
