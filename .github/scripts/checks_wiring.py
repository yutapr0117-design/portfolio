"""
checks_wiring.py — shipped-asset & AIO wiring / discoverability checks
(extracted from check_repository_consistency.py — check.py split track・category "wiring/discovery").

This module owns the cluster of Checks 132-134 (plus 375) that assert shipped assets and AIO
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
