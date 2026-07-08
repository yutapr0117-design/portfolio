"""
checks_shipped_hygiene.py — shipped-JS/HTML security & hygiene checks — eval/setTimeout-string/document.write/console/loose-eq etc. (242-249, 366, 367)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  242. index.html inline `on*=` event handlers are restricted to the
       documented CSP-allowlisted pattern: every `on*=` attribute outside
       of HTML comments MUST match exactly `onload="this.media='all'"`
       (the documented async font-loading pattern that is whitelisted via
       CSP `'unsafe-hashes'`). Drift introduces an XSS entry vector that
       bypasses CSP `script-src` (inline event handlers execute as
       scripts). Sibling of Check 239/240/241 (eval/Function/timer/
       document.write) for the inline-event-handler surface. (BLOCKING)

  243. main.js SITE_CONFIG.LAST_UPDATED + ai:last-modified are NOT in the
       future: both date fields (synced via Check 17/180) MUST be on or
       before today. Drift to a future date silently corrupts AI/SEO
       recency-weighted retrieval (entity ranked as "from the future")
       and reveals temporal model integrity issues. This site does not
       schedule pre-publish dates; future is always a bug. Sibling of
       Check 36 (sitemap lastmod future WARNING) for the canonical-version
       date surface — BLOCKING here because LAST_UPDATED is the entity's
       primary canonical-version anchor. (BLOCKING)

  244. Every top-level node in JSON-LD `@graph` has `@type`: in index.html
       JSON-LD blocks, every direct top-level element of any `@graph`
       array MUST have a non-empty `@type` field. Drift (anonymous node)
       silently makes AI/SEO consumers ignore the node (no type → cannot
       reason about entity) and breaks Schema.org graph traversal.
       Sibling of Check 217 (top-level @id uniqueness) for the top-level
       @type presence axis. (BLOCKING)

  245. JSON-LD FAQPage `mainEntity[]` Q&A structure validity: every
       FAQPage node's `mainEntity` array MUST contain non-empty Question
       entries, each with `@type == "Question"` + non-empty `name` + an
       `acceptedAnswer` object with `@type == "Answer"` + non-empty
       `text`. Drift would silently break Google FAQ rich-result
       eligibility + AI search FAQ ingestion. Sibling of Check 235
       (Article required fields) for the FAQPage required-structure
       surface. (BLOCKING)

  246. JSON-LD BreadcrumbList `itemListElement` Schema.org structure:
       every BreadcrumbList's `itemListElement` array MUST contain
       ListItem entries, each with `@type == "ListItem"`, an integer
       `position`, a non-empty `name`, and an `item` (URL or @id ref).
       Drift would silently break Google breadcrumb rich-result and AI
       site-structure ingestion. Sibling of Check 245 (FAQPage Q&A) for
       the BreadcrumbList required-structure surface. (BLOCKING)

  247. JSON-LD ImageObject/AudioObject/VideoObject have required fields:
       every node with `@type in {ImageObject, AudioObject, VideoObject}`
       MUST have `name` AND at least one of `contentUrl` / `url`. Drift
       (e.g. silent strip of name) would silently break Google Image/
       Audio rich-result and AI/SEO entity-asset linkage. Sibling of
       Check 245 (FAQPage) / Check 246 (BreadcrumbList) for the
       MediaObject required-structure surface. (BLOCKING)

  248. `<meta charset>` value is `utf-8` (case-insensitive): the index
       .html `<meta charset>` attribute MUST resolve to `utf-8` exactly
       (case-insensitive accepts UTF-8 / utf-8). Drift to e.g.
       `shift_jis` or `iso-8859-1` silently mojibake Japanese content and
       break canonical entity name display. Check 157 enforces presence;
       Check 248 enforces value canonicality. (BLOCKING)

  249. `<meta name="viewport">` content has mobile baseline directives:
       the index.html `<meta name="viewport">` content MUST contain
       `width=device-width` AND `initial-scale=1`. Drift (e.g. fixed
       `width=900`) silently breaks mobile rendering (zoom locked,
       content cropped). Check 157 enforces presence; Check 249 enforces
       canonical mobile-baseline content. (BLOCKING)

  366. shipped JS (js/*.js non-recursive) の h() props で `target: '_blank'`
       を含む行の ±2 行以内に `noreferrer` が現れることを BLOCKING 強制。
       runtime は ui-components.js:h() が全 a[target=_blank] に
       noopener+noreferrer を付与する二重防御だが、source レベルの省略は
       「意図的に noreferrer を省いた」と誤読されるコード drift を生む
       (実例: ContactPage LinkedIn #322 が rel:'noopener' のみで push)。
       secureExternalLinks の mutation test (mutation_samples.py) とは独立した
       静的ソース軸の防止層。(BLOCKING)

  367. shipped JS (js/*.js 非再帰) の h('select', ...) 呼び出しで第2引数の
       attrs オブジェクトに `value:` キーが現れないことを BLOCKING 強制。
       `<select>` 要素には HTML 仕様上 `value` content attribute が存在しない。
       h('select', { value: x }) は el.setAttribute('value', x) を呼び、
       <select> の選択状態には一切反映されない (#7cbc4d9 class)。
       正しい実装は各 <option> に `selected: val === cur ? true : undefined`
       を付与すること (h() の undefined-skip line 128 が非選択 option に
       属性追加するのを防ぐ)。apps.js / settings-page.js / projects-page.js の
       全 h('select') を #668〜#670 + 本 increment で修正済。本 Check は
       再発防止の構造封じ。(BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 242. index.html inline on*= handlers are restricted to allowlist (BLOCKING) ─
    # index.html の全 `on*="..."` 属性 (HTML comment 外) が CSP unsafe-hashes で
    # whitelist された 1 パターン `onload="this.media='all'"` のみであることを
    # BLOCKING 強制。drift は CSP script-src を bypass する XSS entry vector。
    _ALLOWED_INLINE_HANDLERS242 = {"onload=\"this.media='all'\""}
    _idx242 = ROOT / "index.html"
    if _idx242.exists():
        _isrc242 = _idx242.read_text(encoding="utf-8")
        _stripped242 = re.sub(r"<!--.*?-->", "", _isrc242, flags=re.DOTALL)
        _handlers242 = re.findall(r'\bon[a-z]+\s*=\s*"[^"]*"', _stripped242)
        _bad242 = [h for h in _handlers242 if h not in _ALLOWED_INLINE_HANDLERS242]
        _ok242 = len(_handlers242) > 0 and not _bad242
        check(
            _ok242,
            f"Check 242: index.html inline on*= handlers {len(_handlers242)} 件全て allowlist 内",
            (f"Check 242: allowlist 外 inline handler: {_bad242!r} — CSP script-src "
             "bypass の XSS vector。allowlist は onload=\"this.media='all'\" のみ"
             if _bad242 else
             "Check 242: inline handler 0 件 — vacuous-fail (font async load の期待値は 2 件)"),
            blocking=True,
        )
    else:
        check(False, "Check 242: index.html present",
              "Check 242: index.html が無い", blocking=True)

    # ── 243. SITE_CONFIG.LAST_UPDATED + ai:last-modified NOT future (BLOCKING) ────
    # main.js SITE_CONFIG.LAST_UPDATED と <meta name="ai:last-modified"> content が
    # 共に today より未来でないことを BLOCKING 強制。Check 36 (sitemap lastmod 未来
    # WARNING) と異なり本サイトは pre-schedule しない設計のため BLOCKING。
    from datetime import date as _date243
    _main243 = ROOT / "main.js"
    _idx243 = ROOT / "index.html"
    if _main243.exists() and _idx243.exists():
        _msrc243 = _main243.read_text(encoding="utf-8")
        _isrc243 = _idx243.read_text(encoding="utf-8")
        _site243_m = re.search(r"LAST_UPDATED:\s*['\"]([^'\"]+)['\"]", _msrc243)
        _ai_lm243_m = re.search(
            r'<meta\s+name=["\']ai:last-modified["\']\s+content=["\']([^"\']+)["\']', _isrc243
        )
        _site243 = _site243_m.group(1) if _site243_m else None
        _ai_lm243 = _ai_lm243_m.group(1) if _ai_lm243_m else None
        _today243 = _date243.today()
        _futures243: list[str] = []
        for _label, _v in (("SITE_CONFIG.LAST_UPDATED", _site243), ("ai:last-modified", _ai_lm243)):
            if not isinstance(_v, str):
                _futures243.append(f"{_label}=抽出不可")
                continue
            try:
                _d = _date243.fromisoformat(_v[:10])
            except ValueError:
                # Check 215 が format を担う。本 check は format violation で fail せず skip。
                continue
            if _d > _today243:
                _futures243.append(f"{_label}={_v!r} (today={_today243.isoformat()} より未来)")
        _ok243 = not _futures243
        check(
            _ok243,
            f"Check 243: SITE_CONFIG.LAST_UPDATED + ai:last-modified 共に today ({_today243.isoformat()}) 以前",
            (f"Check 243: 未来日 detected: {_futures243!r} — AI/SEO recency が "
             "「未来から来た content」と誤認し ranking corruption。today 以下へ修正"),
            blocking=True,
        )
    else:
        check(False, "Check 243: main.js + index.html present",
              "Check 243: main.js もしくは index.html が無い", blocking=True)

    # ── 244. JSON-LD @graph 全 top-level node has @type (BLOCKING) ────────────────
    # index.html の各 JSON-LD <script> block の top-level `@graph` 配列の全 element に
    # 非空 `@type` がある (anonymous node 不在) ことを BLOCKING 強制。drift で AI/SEO
    # が無 type node を無視し Schema.org graph traversal 不能。
    _idx244 = ROOT / "index.html"
    if _idx244.exists():
        _isrc244 = _idx244.read_text(encoding="utf-8")
        _blocks244 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc244,
            flags=re.DOTALL,
        )
        _violations244: list[str] = []
        _total244 = 0
        for _bi, _blk in enumerate(_blocks244):
            try:
                _data244 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _g244 = _data244.get("@graph") if isinstance(_data244, dict) else None
            if not isinstance(_g244, list):
                continue
            for _j, _n in enumerate(_g244):
                _total244 += 1
                if not isinstance(_n, dict) or not isinstance(_n.get("@type"), str) or not _n.get("@type"):
                    _violations244.append(f"block{_bi}.@graph[{_j}] missing/empty @type")
        _ok244 = _total244 > 0 and not _violations244
        check(
            _ok244,
            f"Check 244: JSON-LD @graph top-level node {_total244} 件全て @type 保有",
            (f"Check 244: @type 不在 node: {_violations244!r} — AI/SEO 無視されて "
             "Schema.org graph traversal 破壊。各 top-level node に @type を付与せよ"
             if _violations244 else
             "Check 244: @graph top-level node 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 244: index.html present",
              "Check 244: index.html が無い", blocking=True)

    # ── 245. JSON-LD FAQPage mainEntity Q&A structure validity (BLOCKING) ─────────
    # index.html JSON-LD の全 FAQPage node の `mainEntity` 配列が Schema.org Q&A 構造
    # (Question + name + acceptedAnswer(Answer + text)) を満たすことを BLOCKING 強制。
    # drift は SILENT に Google FAQ rich-result 失格 + AI search FAQ ingestion 破壊。
    _idx245 = ROOT / "index.html"
    if _idx245.exists():
        _isrc245 = _idx245.read_text(encoding="utf-8")
        _blocks245 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc245,
            flags=re.DOTALL,
        )
        _violations245: list[str] = []
        _q_count245 = 0
        def _walk245(node: object, path: str) -> None:
            nonlocal _q_count245
            if isinstance(node, dict):
                if node.get("@type") == "FAQPage":
                    _me = node.get("mainEntity")
                    if not isinstance(_me, list) or not _me:
                        _violations245.append(f"{path}: FAQPage.mainEntity 欠落/空")
                    else:
                        for _i, _q in enumerate(_me):
                            _q_count245 += 1
                            if not isinstance(_q, dict):
                                _violations245.append(f"{path}.mainEntity[{_i}] non-dict")
                                continue
                            if _q.get("@type") != "Question":
                                _violations245.append(f"{path}.mainEntity[{_i}] @type != Question")
                            _n = _q.get("name")
                            if not isinstance(_n, str) or not _n.strip():
                                _violations245.append(f"{path}.mainEntity[{_i}] name 欠落/空")
                            _a = _q.get("acceptedAnswer")
                            if not isinstance(_a, dict):
                                _violations245.append(f"{path}.mainEntity[{_i}] acceptedAnswer 欠落")
                            else:
                                if _a.get("@type") != "Answer":
                                    _violations245.append(f"{path}.mainEntity[{_i}].acceptedAnswer @type != Answer")
                                _t = _a.get("text")
                                if not isinstance(_t, str) or not _t.strip():
                                    _violations245.append(f"{path}.mainEntity[{_i}].acceptedAnswer.text 欠落/空")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk245(item, f"{path}.{k}")
                    else:
                        _walk245(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk245(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks245):
            try:
                _data245 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk245(_data245, f"block{_bi}")
        _ok245 = _q_count245 > 0 and not _violations245
        check(
            _ok245,
            f"Check 245: FAQPage mainEntity Q&A {_q_count245} 件全て Schema.org 構造正",
            (f"Check 245: 違反: {_violations245!r} — Google FAQ rich-result 失格 + "
             "AI FAQ ingestion 破壊。Question+name+acceptedAnswer(Answer+text) 構造へ揃えよ"
             if _violations245 else
             "Check 245: FAQPage mainEntity Q 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 245: index.html present",
              "Check 245: index.html が無い", blocking=True)

    # ── 246. JSON-LD BreadcrumbList itemListElement Schema.org 構造 (BLOCKING) ────
    # index.html JSON-LD 全 BreadcrumbList の `itemListElement` 配列が ListItem +
    # position(int) + name(非空 str) + item(URL/string) を満たすことを BLOCKING 強制。
    # drift で Google breadcrumb rich-result + AI site-structure ingestion 破壊。
    _idx246 = ROOT / "index.html"
    if _idx246.exists():
        _isrc246 = _idx246.read_text(encoding="utf-8")
        _blocks246 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc246,
            flags=re.DOTALL,
        )
        _violations246: list[str] = []
        _items_count246 = 0
        def _walk246(node: object, path: str) -> None:
            nonlocal _items_count246
            if isinstance(node, dict):
                if node.get("@type") == "BreadcrumbList":
                    _ile = node.get("itemListElement")
                    if not isinstance(_ile, list) or not _ile:
                        _violations246.append(f"{path}: itemListElement 欠落/空")
                    else:
                        for _i, _it in enumerate(_ile):
                            _items_count246 += 1
                            if not isinstance(_it, dict):
                                _violations246.append(f"{path}.itemListElement[{_i}] non-dict")
                                continue
                            if _it.get("@type") != "ListItem":
                                _violations246.append(f"{path}.itemListElement[{_i}] @type != ListItem")
                            if not isinstance(_it.get("position"), int):
                                _violations246.append(f"{path}.itemListElement[{_i}] position not int")
                            _n = _it.get("name")
                            if not isinstance(_n, str) or not _n.strip():
                                _violations246.append(f"{path}.itemListElement[{_i}] name 欠落/空")
                            if "item" not in _it:
                                _violations246.append(f"{path}.itemListElement[{_i}] item 欠落")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk246(item, f"{path}.{k}")
                    else:
                        _walk246(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk246(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks246):
            try:
                _data246 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk246(_data246, f"block{_bi}")
        _ok246 = _items_count246 > 0 and not _violations246
        check(
            _ok246,
            f"Check 246: BreadcrumbList itemListElement {_items_count246} 件全て Schema.org 構造正",
            (f"Check 246: 違反: {_violations246!r} — Google breadcrumb rich-result 失格 "
             "+ AI site-structure ingestion 破壊。ListItem+position+name+item へ揃えよ"
             if _violations246 else
             "Check 246: BreadcrumbList items 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 246: index.html present",
              "Check 246: index.html が無い", blocking=True)

    # ── 247. JSON-LD ImageObject/AudioObject/VideoObject 必須 fields (BLOCKING) ───
    # index.html JSON-LD で `@type in {ImageObject, AudioObject, VideoObject}` の
    # node が `name` AND (`contentUrl` OR `url`) を持つことを BLOCKING 強制。drift で
    # Google Image/Audio rich-result 失格 + AI/SEO entity-asset linkage 破壊。
    _MEDIA_TYPES247 = {"ImageObject", "AudioObject", "VideoObject"}
    _idx247 = ROOT / "index.html"
    if _idx247.exists():
        _isrc247 = _idx247.read_text(encoding="utf-8")
        _blocks247 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc247,
            flags=re.DOTALL,
        )
        _violations247: list[str] = []
        _media_count247 = 0
        def _walk247(node: object, path: str) -> None:
            nonlocal _media_count247
            if isinstance(node, dict):
                _t = node.get("@type")
                if isinstance(_t, str) and _t in _MEDIA_TYPES247:
                    _media_count247 += 1
                    _missing = []
                    if not isinstance(node.get("name"), str) or not node.get("name", "").strip():
                        _missing.append("name")
                    if "contentUrl" not in node and "url" not in node:
                        _missing.append("contentUrl|url")
                    if _missing:
                        _violations247.append(f"{path} {_t}: missing {_missing!r}")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk247(item, f"{path}.{k}")
                    else:
                        _walk247(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk247(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks247):
            try:
                _data247 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk247(_data247, f"block{_bi}")
        _ok247 = _media_count247 > 0 and not _violations247
        check(
            _ok247,
            f"Check 247: MediaObject {_media_count247} 件全て name + contentUrl|url 保有",
            (f"Check 247: 違反: {_violations247!r} — Google Image/Audio rich-result 失格 "
             "+ AI/SEO entity-asset linkage 破壊。name + contentUrl|url を揃えよ"
             if _violations247 else
             "Check 247: MediaObject 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 247: index.html present",
              "Check 247: index.html が無い", blocking=True)

    # ── 248. <meta charset> value is utf-8 (case-insensitive) (BLOCKING) ──────────
    # index.html `<meta charset="...">` の値が utf-8 (case-insensitive) であることを
    # BLOCKING 強制。drift で Japanese mojibake → canonical entity 名表示破壊。
    # Check 157 は presence、Check 248 は value canonicality 軸。
    _idx248 = ROOT / "index.html"
    if _idx248.exists():
        _isrc248 = _idx248.read_text(encoding="utf-8")
        _cm248 = re.search(r'<meta\s+charset\s*=\s*["\']?([^"\'\s>]+)', _isrc248, re.IGNORECASE)
        _cv248 = _cm248.group(1) if _cm248 else None
        _ok248 = isinstance(_cv248, str) and _cv248.lower() == "utf-8"
        check(
            _ok248,
            f"Check 248: <meta charset>={_cv248!r} == utf-8 (case-insensitive)",
            (f"Check 248: charset 値違反: {_cv248!r} — Japanese mojibake で canonical "
             "entity 名表示破壊。utf-8 (case-insensitive) へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 248: index.html present",
              "Check 248: index.html が無い", blocking=True)

    # ── 249. <meta name=viewport> content has mobile baseline (BLOCKING) ──────────
    # index.html `<meta name="viewport">` content が `width=device-width` AND
    # `initial-scale=1` を含むことを BLOCKING 強制。drift で mobile rendering 破壊
    # (zoom 固定 / content cropped)。Check 157 (presence) の value 軸補完。
    _idx249 = ROOT / "index.html"
    if _idx249.exists():
        _isrc249 = _idx249.read_text(encoding="utf-8")
        _vm249 = re.search(
            r'<meta\s+name=["\']viewport["\'][^>]*content=["\']([^"\']+)["\']', _isrc249
        )
        _vv249 = _vm249.group(1) if _vm249 else None
        _missing249: list[str] = []
        if not isinstance(_vv249, str):
            _missing249.append("viewport 抽出不可")
        else:
            if "width=device-width" not in _vv249:
                _missing249.append("width=device-width 不在")
            if not re.search(r"initial-scale\s*=\s*1(\.0+)?\b", _vv249):
                _missing249.append("initial-scale=1 不在")
        _ok249 = not _missing249
        check(
            _ok249,
            f"Check 249: <meta name=viewport> content has mobile baseline ({_vv249!r})",
            (f"Check 249: viewport content 違反: {_missing249!r} — mobile rendering 破壊"
             " (zoom 固定/content cropped)。width=device-width + initial-scale=1 を付与"),
            blocking=True,
        )
    else:
        check(False, "Check 249: index.html present",
              "Check 249: index.html が無い", blocking=True)

    # ── 366. shipped JS target='_blank' に ±2行以内で noreferrer あり (BLOCKING) ────
    # js/*.js (非再帰・main.js 含む) の h() props 内で `target: '_blank'` を含む行の
    # ±2 行以内に `noreferrer` が現れることを強制。runtime 多重防御 (ui-components.js
    # h() 全 a[target=_blank] 強制 + secureExternalLinks patcher) はあるが source の
    # 省略は「意図的 noreferrer 省略」と誤読されるコード drift を生む。
    _violations366: list[str] = []
    _hit_count366 = 0
    for _f366 in sorted((ROOT / "js").glob("*.js")):
        _lines366 = _f366.read_text(encoding="utf-8", errors="replace").splitlines()
        for _li366, _ln366 in enumerate(_lines366):
            if "target: '_blank'" not in _ln366:
                continue
            _hit_count366 += 1
            _window366 = _lines366[max(0, _li366 - 2): _li366 + 3]
            if any("noreferrer" in _wl for _wl in _window366):
                continue
            _violations366.append(f"{_f366.relative_to(ROOT)}:{_li366 + 1}")
    check(
        not _violations366,
        f"Check 366: shipped JS {_hit_count366} 件の target='_blank' 全てに ±2行以内で noreferrer あり",
        (f"Check 366: noreferrer 欠落 {len(_violations366)} 件: {_violations366!r} — "
         "source drift は intentional 省略と誤読される。rel:'noopener noreferrer' へ揃えよ"
         if _violations366 else
         "Check 366: target='_blank' が shipped JS に 0 件 — vacuous-fail"),
        blocking=True,
    )

    # ── 367. shipped JS h('select', ...) に value: attr を禁止 (HTML 仕様違反) ──────
    # `<select>` 要素には HTML 仕様上 `value` content attribute が存在しない。
    # h('select', { value: x }) は el.setAttribute('value', x) を呼び、<select> の
    # 選択状態には一切反映されない (#7cbc4d9 class)。修正: 各 <option> に
    # `selected: val === cur ? true : undefined` を付与する (h() の undefined-skip
    # line 128 が非選択 option に属性追加するのを防ぐ)。
    # apps.js / settings-page.js / projects-page.js の全 h('select') を
    # #668〜#670 + 本 increment で修正済。本 Check は再発防止の構造封じ。
    #
    # 手法: h('select', の直後から最初の h('option', までのテキストに
    # `(?<![.\w])value\s*:` (オブジェクトキーとしての value:) を探す。
    # `e.target.value` は `;` で終わり `:` が後続しないため false-positive にならない。
    _violations367: list[tuple[str, int]] = []
    _select_pat367 = re.compile(r"h\('select'")
    _value_key_pat367 = re.compile(r"(?<![.\w])value\s*:")
    _option_pat367 = re.compile(r"h\('option'")
    _js_files367 = sorted((ROOT / "js").glob("*.js"))
    for _f367 in _js_files367:
        _src367 = _f367.read_text(encoding="utf-8", errors="replace")
        for _m367 in _select_pat367.finditer(_src367):
            _pos367 = _m367.end()
            _tail367 = _src367[_pos367:]
            _opt_m367 = _option_pat367.search(_tail367)
            _before_option367 = _tail367[:_opt_m367.start()] if _opt_m367 else _tail367[:300]
            if _value_key_pat367.search(_before_option367):
                _line367 = _src367[:_m367.start()].count("\n") + 1
                _violations367.append((str(_f367.relative_to(ROOT)), _line367))
    check(
        not _violations367,
        f"Check 367: shipped JS h('select') の attrs に value: キーなし "
        f"({len(_js_files367)} files scanned)",
        (f"Check 367: h('select') に value: attr が {len(_violations367)} 件: "
         f"{_violations367!r} — <select> に value content attribute は HTML 仕様上存在しない "
         "(el.setAttribute('value', x) は選択状態に反映されない #7cbc4d9 class)。"
         "各 <option> に `selected: val === cur ? true : undefined` を付与せよ"),
        blocking=True,
    )
