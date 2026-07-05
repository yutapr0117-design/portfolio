"""
checks_jsonld_primary.py — JSON-LD primary-node required-field completeness checks — WebPage/Person/WebSite/Org/hero/BGM (256-261)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  256. Primary JSON-LD WebPage has `dateModified` + `inLanguage` +
       `isPartOf`: in index.html static JSON-LD, the primary WebPage node
       (`@id == canonical + "#webpage"`) MUST have `dateModified` (string),
       `inLanguage` (string), AND `isPartOf` (object/string). Drift would
       silently remove recency / language / hierarchy signals from the
       primary page entity. Sibling of Check 235 (Article required fields)
       for the primary WebPage required-fields axis. (BLOCKING)

  257. primary JSON-LD Person has jobTitle + image + sameAs + worksFor +
       description: in index.html static JSON-LD, the primary Person node
       (`@id == canonical + "#person"`) MUST have all 5 fields: jobTitle
       (str), image (dict/string), sameAs (list), worksFor (dict/string),
       description (str). Drift would silently strip entity-rich-profile
       data from AI/SEO consumers (knowledge-graph card would shrink).
       Sibling of Check 256 (primary WebPage) for the primary Person
       required-fields axis. (BLOCKING)

  258. primary JSON-LD WebSite has inLanguage + potentialAction: in
       index.html static JSON-LD, the primary WebSite node (`@id ==
       canonical + "#website"`) MUST have `inLanguage` (str) AND
       `potentialAction` (dict/list). Drift would silently remove the
       site-level language signal and the AI/voice action descriptor
       from the WebSite root entity. Sibling of Check 256 (primary
       WebPage) / Check 257 (primary Person) for the primary WebSite
       required-fields axis. (BLOCKING)

  259. primary JSON-LD Organization (nkgr.co.jp) has name + url +
       alternateName + description + employee: the canonical Organization
       node (`@id == "https://nkgr.co.jp/#organization"`) MUST have all
       5 fields. Drift would silently strip employer-rich data from
       AI/SEO consumers (worksFor target loses richness, knowledge-graph
       Organization card shrinks). Sibling of Check 257 (primary Person)
       for the primary Organization required-fields axis. (BLOCKING)

  260. primary hero ImageObject has caption + width + height +
       encodingFormat: in index.html static JSON-LD, the primary hero
       ImageObject node (`@id == canonical + "#hero-image"`) MUST have
       caption (non-empty str), width + height (numeric-parsable string
       or int), encodingFormat (non-empty str). Drift would silently
       degrade Google Image rich-result eligibility (width/height
       required for CWV LCP-image preload coordination, caption required
       for accessibility / Google Lens). Sibling of Check 247
       (MediaObject required) for the hero-image required-fields axis.
       (BLOCKING)

  261. primary BGM AudioObject has encodingFormat + creator: in index.html
       static JSON-LD, the primary BGM AudioObject node (`@id == canonical
       + "#portfolio-bgm"`) MUST have `encodingFormat` (non-empty str)
       AND `creator` (dict or string @id reference). Drift would silently
       degrade AI search audio classification (no encodingFormat → mime
       type unknown) and remove attribution (no creator → audio uploaded
       by "Anonymous"). Sibling of Check 260 (hero image) for the
       primary audio required-fields axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 256. primary WebPage has dateModified + inLanguage + isPartOf (BLOCKING) ──
    # index.html 静的 JSON-LD の primary WebPage node (@id == canonical+#webpage) が
    # `dateModified` + `inLanguage` + `isPartOf` を持つことを BLOCKING 強制。drift で
    # recency/language/hierarchy 信号 silent 喪失。Check 235 の primary WebPage 軸版。
    _idx256 = ROOT / "index.html"
    if _idx256.exists():
        _isrc256 = _idx256.read_text(encoding="utf-8")
        _canon256_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc256
        )
        _canon256 = _canon256_m.group(1) if _canon256_m else None
        _expected_wid256 = (_canon256 or "") + "#webpage"
        _blocks256 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc256,
            flags=re.DOTALL,
        )
        _primary_wp256 = None
        def _walk256(node: object) -> None:
            nonlocal _primary_wp256
            if isinstance(node, dict):
                if node.get("@type") == "WebPage" and node.get("@id") == _expected_wid256:
                    _primary_wp256 = node
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk256(item)
                    else:
                        _walk256(v)
            elif isinstance(node, list):
                for item in node:
                    _walk256(item)
        for _blk in _blocks256:
            try:
                _walk256(json.loads(_blk))
            except json.JSONDecodeError:
                continue
        _missing256: list[str] = []
        if _primary_wp256 is None:
            _missing256.append(f"primary WebPage @id={_expected_wid256!r} 不在")
        else:
            if not isinstance(_primary_wp256.get("dateModified"), str):
                _missing256.append("dateModified 欠落")
            if not isinstance(_primary_wp256.get("inLanguage"), str):
                _missing256.append("inLanguage 欠落")
            if not isinstance(_primary_wp256.get("isPartOf"), (dict, str)):
                _missing256.append("isPartOf 欠落")
        _ok256 = not _missing256
        check(
            _ok256,
            f"Check 256: primary WebPage ({_expected_wid256}) has dateModified + inLanguage + isPartOf",
            (f"Check 256: 違反: {_missing256!r} — recency/language/hierarchy 信号喪失。"
             "primary WebPage に 3 field を揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 256: index.html present",
              "Check 256: index.html が無い", blocking=True)

    # ── 257. primary Person 必須 5 fields (BLOCKING) ──────────────────────────────
    # index.html 静的 JSON-LD の primary Person node (@id == canonical+#person) が
    # jobTitle (str) / image (dict|str) / sameAs (list) / worksFor (dict|str) /
    # description (str) 全 5 field を持つことを BLOCKING 強制。drift で entity-rich
    # profile data 喪失 → knowledge-graph card 縮小。Check 256 の primary Person 軸版。
    _idx257 = ROOT / "index.html"
    if _idx257.exists():
        _isrc257 = _idx257.read_text(encoding="utf-8")
        _canon257_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc257
        )
        _canon257 = _canon257_m.group(1) if _canon257_m else None
        _expected_pid257 = (_canon257 or "") + "#person"
        _blocks257 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc257,
            flags=re.DOTALL,
        )
        _primary_p257 = None
        def _walk257(node: object) -> None:
            nonlocal _primary_p257
            if isinstance(node, dict):
                if node.get("@type") == "Person" and node.get("@id") == _expected_pid257 and _primary_p257 is None:
                    _primary_p257 = node
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk257(item)
                    else:
                        _walk257(v)
            elif isinstance(node, list):
                for item in node:
                    _walk257(item)
        for _blk in _blocks257:
            try:
                _walk257(json.loads(_blk))
            except json.JSONDecodeError:
                continue
        _missing257: list[str] = []
        if _primary_p257 is None:
            _missing257.append(f"primary Person @id={_expected_pid257!r} 不在")
        else:
            _str_fields = ("jobTitle", "description")
            for _f in _str_fields:
                if not isinstance(_primary_p257.get(_f), str) or not _primary_p257[_f].strip():
                    _missing257.append(f"{_f} 欠落/空")
            if not isinstance(_primary_p257.get("image"), (dict, str)):
                _missing257.append("image 欠落")
            if not isinstance(_primary_p257.get("sameAs"), list) or not _primary_p257["sameAs"]:
                _missing257.append("sameAs 欠落/空 list")
            if not isinstance(_primary_p257.get("worksFor"), (dict, str)):
                _missing257.append("worksFor 欠落")
        _ok257 = not _missing257
        check(
            _ok257,
            f"Check 257: primary Person ({_expected_pid257}) has 5 required fields",
            (f"Check 257: 違反: {_missing257!r} — entity-rich profile 喪失で knowledge-graph "
             "card 縮小。primary Person に 5 field を揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 257: index.html present",
              "Check 257: index.html が無い", blocking=True)

    # ── 258. primary WebSite has inLanguage + potentialAction (BLOCKING) ──────────
    # index.html 静的 JSON-LD の primary WebSite node (@id == canonical+#website) が
    # inLanguage (str) + potentialAction (dict|list) を持つことを BLOCKING 強制。
    # drift で site-level 言語信号 + AI/voice action descriptor 喪失。Check 256/257
    # の primary WebSite 軸版。
    _idx258 = ROOT / "index.html"
    if _idx258.exists():
        _isrc258 = _idx258.read_text(encoding="utf-8")
        _canon258_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc258
        )
        _canon258 = _canon258_m.group(1) if _canon258_m else None
        _expected_wid258 = (_canon258 or "") + "#website"
        _blocks258 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc258,
            flags=re.DOTALL,
        )
        _primary_ws258 = None
        def _walk258(node: object) -> None:
            nonlocal _primary_ws258
            if isinstance(node, dict):
                if node.get("@type") == "WebSite" and node.get("@id") == _expected_wid258 and _primary_ws258 is None:
                    _primary_ws258 = node
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk258(item)
                    else:
                        _walk258(v)
            elif isinstance(node, list):
                for item in node:
                    _walk258(item)
        for _blk in _blocks258:
            try:
                _walk258(json.loads(_blk))
            except json.JSONDecodeError:
                continue
        _missing258: list[str] = []
        if _primary_ws258 is None:
            _missing258.append(f"primary WebSite @id={_expected_wid258!r} 不在")
        else:
            if not isinstance(_primary_ws258.get("inLanguage"), str):
                _missing258.append("inLanguage 欠落")
            if not isinstance(_primary_ws258.get("potentialAction"), (dict, list)):
                _missing258.append("potentialAction 欠落")
        _ok258 = not _missing258
        check(
            _ok258,
            f"Check 258: primary WebSite ({_expected_wid258}) has inLanguage + potentialAction",
            (f"Check 258: 違反: {_missing258!r} — site-level 言語 / action descriptor 喪失。"
             "primary WebSite に 2 field を揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 258: index.html present",
              "Check 258: index.html が無い", blocking=True)

    # ── 259. primary Organization (nkgr.co.jp) 必須 5 fields (BLOCKING) ──────────
    # index.html JSON-LD の primary Organization node
    # (@id == "https://nkgr.co.jp/#organization") が name + url + alternateName +
    # description + employee 5 field を持つことを BLOCKING 強制。drift で employer-rich
    # data 喪失 → knowledge-graph Organization card 縮小。Check 257 の Organization 軸版。
    _PRIMARY_ORG_ID259 = "https://nkgr.co.jp/#organization"
    _idx259 = ROOT / "index.html"
    if _idx259.exists():
        _isrc259 = _idx259.read_text(encoding="utf-8")
        _blocks259 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc259,
            flags=re.DOTALL,
        )
        _primary_org259 = None
        def _walk259(node: object) -> None:
            nonlocal _primary_org259
            if isinstance(node, dict):
                if (
                    node.get("@type") == "Organization"
                    and node.get("@id") == _PRIMARY_ORG_ID259
                    and _primary_org259 is None
                ):
                    _primary_org259 = node
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk259(item)
                    else:
                        _walk259(v)
            elif isinstance(node, list):
                for item in node:
                    _walk259(item)
        for _blk in _blocks259:
            try:
                _walk259(json.loads(_blk))
            except json.JSONDecodeError:
                continue
        _missing259: list[str] = []
        if _primary_org259 is None:
            _missing259.append(f"primary Organization @id={_PRIMARY_ORG_ID259!r} 不在")
        else:
            for _f in ("name", "url", "description"):
                if not isinstance(_primary_org259.get(_f), str) or not _primary_org259[_f].strip():
                    _missing259.append(f"{_f} 欠落/空")
            if not isinstance(_primary_org259.get("alternateName"), list) or not _primary_org259["alternateName"]:
                _missing259.append("alternateName 欠落/空 list")
            if not isinstance(_primary_org259.get("employee"), (dict, list, str)):
                _missing259.append("employee 欠落")
        _ok259 = not _missing259
        check(
            _ok259,
            f"Check 259: primary Organization ({_PRIMARY_ORG_ID259}) has 5 required fields",
            (f"Check 259: 違反: {_missing259!r} — employer-rich data 喪失 → "
             "knowledge-graph Organization card 縮小。primary Organization に 5 field を揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 259: index.html present",
              "Check 259: index.html が無い", blocking=True)

    # ── 260. primary hero ImageObject 必須 4 fields (BLOCKING) ────────────────────
    # index.html JSON-LD の primary hero ImageObject node (@id == canonical+#hero-image)
    # が caption (非空 str) + width (numeric-parsable) + height (numeric-parsable) +
    # encodingFormat (非空 str) を持つことを BLOCKING 強制。drift で Google Image
    # rich-result + CWV LCP preload + accessibility 劣化。Check 247 の hero-image 軸版。
    _idx260 = ROOT / "index.html"
    if _idx260.exists():
        _isrc260 = _idx260.read_text(encoding="utf-8")
        _canon260_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc260
        )
        _canon260 = _canon260_m.group(1) if _canon260_m else None
        _expected_hid260 = (_canon260 or "") + "#hero-image"
        _blocks260 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc260,
            flags=re.DOTALL,
        )
        _primary_hero260 = None
        def _walk260(node: object) -> None:
            nonlocal _primary_hero260
            if isinstance(node, dict):
                if (
                    node.get("@type") == "ImageObject"
                    and node.get("@id") == _expected_hid260
                    and _primary_hero260 is None
                ):
                    _primary_hero260 = node
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk260(item)
                    else:
                        _walk260(v)
            elif isinstance(node, list):
                for item in node:
                    _walk260(item)
        for _blk in _blocks260:
            try:
                _walk260(json.loads(_blk))
            except json.JSONDecodeError:
                continue
        _missing260: list[str] = []
        if _primary_hero260 is None:
            _missing260.append(f"primary hero ImageObject @id={_expected_hid260!r} 不在")
        else:
            for _f in ("caption", "encodingFormat"):
                if not isinstance(_primary_hero260.get(_f), str) or not _primary_hero260[_f].strip():
                    _missing260.append(f"{_f} 欠落/空")
            for _f in ("width", "height"):
                _v = _primary_hero260.get(_f)
                try:
                    if isinstance(_v, str):
                        int(_v)
                    elif isinstance(_v, int):
                        pass
                    else:
                        raise ValueError("not numeric")
                except (TypeError, ValueError):
                    _missing260.append(f"{_f}={_v!r} 非 numeric/欠落")
        _ok260 = not _missing260
        check(
            _ok260,
            f"Check 260: primary hero ImageObject has caption + width + height + encodingFormat",
            (f"Check 260: 違反: {_missing260!r} — Google Image rich-result + CWV LCP + "
             "accessibility 劣化。caption(str) + width/height(numeric) + encodingFormat(str) を揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 260: index.html present",
              "Check 260: index.html が無い", blocking=True)

    # ── 261. primary BGM AudioObject 必須 fields (BLOCKING) ───────────────────────
    # index.html JSON-LD の primary BGM AudioObject (@id == canonical+#portfolio-bgm)
    # が encodingFormat (str) + creator (dict|str) を持つことを BLOCKING 強制。drift で
    # AI search audio classification + attribution 喪失。Check 260 の audio 軸版。
    _idx261 = ROOT / "index.html"
    if _idx261.exists():
        _isrc261 = _idx261.read_text(encoding="utf-8")
        _canon261_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc261
        )
        _canon261 = _canon261_m.group(1) if _canon261_m else None
        _expected_bid261 = (_canon261 or "") + "#portfolio-bgm"
        _blocks261 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc261,
            flags=re.DOTALL,
        )
        _primary_bgm261 = None
        def _walk261(node: object) -> None:
            nonlocal _primary_bgm261
            if isinstance(node, dict):
                if (
                    node.get("@type") == "AudioObject"
                    and node.get("@id") == _expected_bid261
                    and _primary_bgm261 is None
                ):
                    _primary_bgm261 = node
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk261(item)
                    else:
                        _walk261(v)
            elif isinstance(node, list):
                for item in node:
                    _walk261(item)
        for _blk in _blocks261:
            try:
                _walk261(json.loads(_blk))
            except json.JSONDecodeError:
                continue
        _missing261: list[str] = []
        if _primary_bgm261 is None:
            _missing261.append(f"primary BGM AudioObject @id={_expected_bid261!r} 不在")
        else:
            if not isinstance(_primary_bgm261.get("encodingFormat"), str) or not _primary_bgm261["encodingFormat"].strip():
                _missing261.append("encodingFormat 欠落/空")
            if not isinstance(_primary_bgm261.get("creator"), (dict, str)):
                _missing261.append("creator 欠落")
        _ok261 = not _missing261
        check(
            _ok261,
            f"Check 261: primary BGM AudioObject ({_expected_bid261}) has encodingFormat + creator",
            (f"Check 261: 違反: {_missing261!r} — AI search audio classification + "
             "attribution 喪失。encodingFormat (str) + creator (dict/str) を揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 261: index.html present",
              "Check 261: index.html が無い", blocking=True)
