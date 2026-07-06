"""
checks_seo_baseline.py — SEO/AIO date-ISO + URL-resolution + HTTPS/meta baseline checks
(extracted from check_repository_consistency.py — check.py split track・category "SEO baseline").

Non-contiguous cluster of Checks 181/182/183/184/185/186/188/189: SITE_CONFIG.LAST_UPDATED ISO-8601
(181), ai:* meta URL endpoints resolve (182), sitemap lastmod ISO (183), sw.js AIO_FILES resolve
(184), canonical HTTPS (185), meta author entity identifiers (186), robots Sitemap URL resolve (188),
meta robots no-noindex (189). Each Check reads its own target files directly; no global-content or
cross-section var coupling. NOTE: 187 (og:locale) is already extracted (checks_html.py); 190 (.nojekyll)
consumes the setup-global `_assets` list so it stays in the monolith.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  181. main.js SITE_CONFIG.LAST_UPDATED is ISO-8601 (YYYY-MM-DD) and a real calendar
       date: the LAST_UPDATED string in main.js SITE_CONFIG must match strict
       `YYYY-MM-DD` and parse as a valid date. Free-form / locale-specific formats
       (e.g. '2026/05/31', '5/31/26') would silently survive Check 180 (byte-identical
       check) and propagate to ai:last-modified, but AI/SEO crawlers expect ISO-8601
       and would either drop the freshness signal entirely or misparse the date.
       Centralizes the format invariant at the source (SITE_CONFIG) so all downstream
       coherence (Check 91 / 180) implicitly inherits ISO-8601 correctness. (BLOCKING)
  182. ai:* meta URL endpoints resolve to actual repo files: the URL content of
       `<meta name="ai:context">`, `<meta name="ai:entrypoint">`, and
       `<meta name="ai:aio-manifest">` must map (via canonical-URL strip) to an
       existing repo file. Check 171 enforces only the canonical URL *prefix*; if the
       path after the prefix drifts (e.g. `llms-full.txt` renamed to
       `llms-context.txt` but ai:context not updated, or the manifest moved), 171
       still passes but the URL 404s when AI crawlers fetch it — silent discovery
       collapse. Sibling of Check 163/164 (icon/og:image file resolution) for the
       ai:* meta surface. (BLOCKING)
  183. sitemap.xml `<lastmod>` values are strict ISO-8601 YYYY-MM-DD: every
       `<lastmod>` element in sitemap.xml must match strict `YYYY-MM-DD` and parse as
       a valid calendar date. The W3C Datetime / sitemap protocol both allow more
       liberal formats (`YYYY-MM-DDThh:mm:ss+00:00`, `YYYY/MM/DD`, etc.), but most
       crawlers normalize to date-only and locale formats break parsers silently.
       Centralizing on strict YYYY-MM-DD avoids ambiguity. Sibling of Check 65 (docs
       ISO-8601) and Check 181 (SITE_CONFIG.LAST_UPDATED ISO-8601) for the sitemap
       surface. (BLOCKING)
  184. sw.js AIO_FILES paths resolve to actual repo files: every path listed in
       sw.js's `AIO_FILES` array (the special SWR fetch-intercept list) must map (via
       canonical-URL pathname strip) to an existing repo file. Check 160 enforces
       only the first-segment pathname coherence; if the path tail drifts (e.g.
       `/portfolio/llms.txt` renamed to `/portfolio/llms-entry.txt` but sw.js not
       updated), the SW would attempt to SWR a non-existent endpoint forever and
       silently 404 every cache miss while looking healthy. Sibling of Check 182
       (ai:* meta endpoint resolves) for the service-worker AIO surface. (BLOCKING)
  185. Canonical URL uses HTTPS scheme: the `<link rel="canonical">` href in
       index.html must start with `https://`. Drift to `http://` would silently
       degrade SEO/security signals — browsers warn "Not Secure", crawlers may treat
       the page as a different origin from HTTPS variants and split entity identity,
       and Mixed Content blocks would silently break sub-resource loads in places.
       Check 149 (3-way canonical coherence) catches partial drift, but if all 3
       surfaces flip to HTTP it passes — this check anchors the scheme itself.
       (BLOCKING)
  186. `<meta name="author">` content contains canonical entity identifiers: the
       `<meta name="author">` content in index.html must contain BOTH "Yuta Yokoi"
       AND "横井雄太" (the canonical name pair from CLAUDE.md §1). Drift would
       silently desync the HTML-surface author signal from the entity identity
       (sr-only / JSON-LD / AIO surfaces remain correct, but generic SEO/HTML
       crawlers that read `<meta name="author">` would see a different entity).
       Sibling of Check 173 (js/identity.js AUTHOR) and Check 172 (aio-manifest
       entity name variants) for the HTML <meta name=author> surface. (BLOCKING)
  188. robots.txt `Sitemap:` URL resolves to actual repo file: the `Sitemap:`
       directive URL in robots.txt must (after stripping the canonical URL
       pathname) map to an existing repo file. Check 63 enforces origin coherence
       but not the path tail — rename of `sitemap.xml` (e.g. to `sitemap-v2.xml`)
       without updating robots.txt would silently 404 the sitemap pointer, so
       crawlers like Googlebot would skip indexing every URL the sitemap was meant
       to declare. Sibling of Check 182/184 (ai:* / sw.js endpoint resolves) for
       the robots.txt surface. (BLOCKING)
  189. `<meta name="robots">` does not contain `noindex` / `none`: the
       `<meta name="robots">` content in index.html must NOT contain `noindex` or
       `none` (negative invariant — presence-of-allow rather than absence-of-deny
       is implicit in non-noindex). A silent drift to `noindex` would deindex the
       entire site from all search engines (Google/Bing/DuckDuckGo + AI search
       backed by these) — a catastrophic AIO discovery failure invisible to
       browser/console/behavior e2e. Companion to Check 161 (robots.txt full-site
       disallow guard) for the HTML meta robots surface. (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract

    # ── 181. main.js SITE_CONFIG.LAST_UPDATED is strict ISO-8601 (BLOCKING) ────────
    # main.js SITE_CONFIG.LAST_UPDATED が `YYYY-MM-DD` strict ISO-8601 で実在カレンダー日付
    # であることを BLOCKING 強制。free-form / locale-specific format ('2026/05/31',
    # '5/31/26' 等) は Check 180 (byte-identical) を素通りし ai:last-modified に伝播するが、
    # AI/SEO crawler は ISO-8601 期待ゆえ freshness signal を drop or 誤 parse する。
    # 中心 (SITE_CONFIG) で format を縛り downstream coherence (Check 91/180) が自動継承。
    from datetime import date as _date181
    _main181 = ROOT / "main.js"
    if _main181.exists():
        _msrc181 = _main181.read_text(encoding="utf-8")
        _lu181_m = re.search(r"LAST_UPDATED:\s*['\"]([^'\"]+)['\"]", _msrc181)
        _lu181 = _lu181_m.group(1) if _lu181_m else None
        _iso_ok181 = False
        _parse_err181 = None
        if _lu181 and re.match(r"^\d{4}-\d{2}-\d{2}$", _lu181):
            try:
                _y, _m, _d = _lu181.split("-")
                _date181(int(_y), int(_m), int(_d))
                _iso_ok181 = True
            except (ValueError, TypeError) as _e:
                _parse_err181 = str(_e)
        check(
            _iso_ok181,
            f"Check 181: SITE_CONFIG.LAST_UPDATED={_lu181!r} は ISO-8601 (YYYY-MM-DD) かつ実在日付",
            (f"Check 181: SITE_CONFIG.LAST_UPDATED={_lu181!r} が ISO-8601 (YYYY-MM-DD) 形式または実在日付でない "
             f"({_parse_err181 or 'regex mismatch'}) — ai:last-modified に伝播し AI/SEO crawler が "
             "freshness signal を drop / 誤 parse する。'YYYY-MM-DD' (例 '2026-05-31') 形式に揃えよ"
             if _lu181 else
             "Check 181: SITE_CONFIG.LAST_UPDATED が抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 181: main.js present",
              "Check 181: main.js が無い", blocking=True)

    # ── 182. ai:* meta URL endpoints resolve to actual repo files (BLOCKING) ──────
    # index.html の `<meta name="ai:context">`, `<meta name="ai:entrypoint">`,
    # `<meta name="ai:aio-manifest">` content URL が canonical URL prefix を strip した
    # repo-relative path で実在 file に resolve することを BLOCKING 強制。Check 171 は
    # prefix のみ検証で、prefix 後の path drift (例 llms-full.txt → llms-context.txt
    # rename + meta 未更新) は素通り→AI crawler が 404 で discovery 崩壊。Check 163/164
    # (icon/og:image resolves) の ai:* meta 軸版。
    _idx182 = ROOT / "index.html"
    if _idx182.exists():
        _isrc182 = _idx182.read_text(encoding="utf-8")
        _canon182_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc182
        )
        _canon182 = _canon182_m.group(1) if _canon182_m else None
        _ai_meta_names182 = ["ai:context", "ai:entrypoint", "ai:aio-manifest"]
        _dangling182: list[str] = []
        _extracted182: list[tuple[str, str]] = []
        for _name in _ai_meta_names182:
            _m = re.search(
                rf'<meta\s+name=["\']{re.escape(_name)}["\']\s+content=["\']([^"\']+)["\']',
                _isrc182,
            )
            if not _m:
                _dangling182.append(f"{_name}=<missing>")
                continue
            _url = _m.group(1)
            _extracted182.append((_name, _url))
            if _canon182 and _url.startswith(_canon182):
                _rel = _url[len(_canon182):]
            elif _canon182:
                # Try without trailing slash
                _cs = _canon182.rstrip("/") + "/"
                if _url.startswith(_cs):
                    _rel = _url[len(_cs):]
                else:
                    _dangling182.append(f"{_name}={_url} (canonical prefix 不一致)")
                    continue
            else:
                _dangling182.append(f"{_name}={_url} (canonical 抽出不可)")
                continue
            _target = ROOT / _rel.lstrip("/")
            if not _target.exists():
                _dangling182.append(f"{_name}={_url} → {_rel} (file 不在)")
        _ok182 = (
            _canon182 is not None
            and len(_extracted182) == len(_ai_meta_names182)
            and not _dangling182
        )
        check(
            _ok182,
            f"Check 182: ai:* meta URL 3 endpoint 全て実 file に resolve "
            f"({', '.join(n for n, _ in _extracted182)})",
            (f"Check 182: ai:* meta URL endpoint 不整合: "
             f"{'; '.join(_dangling182)} — AI crawler が fetch して 404 discovery 崩壊。"
             "ai:context / ai:entrypoint / ai:aio-manifest content URL を canonical 配下の "
             "実在 file に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 182: index.html present",
              "Check 182: index.html が無い", blocking=True)

    # ── 183. sitemap.xml <lastmod> values are strict ISO-8601 YYYY-MM-DD (BLOCKING) ─
    # sitemap.xml の全 `<lastmod>` 要素値が strict `YYYY-MM-DD` regex + 実在カレンダー
    # 日付であることを BLOCKING 強制。W3C Datetime / sitemap protocol は liberal format
    # 許容 (YYYY-MM-DDThh:mm:ss / YYYY/MM/DD 等) だが locale-specific 形式は crawler の
    # parser を silent に壊す。Check 65/181 の sitemap 軸版。
    from datetime import date as _date183
    _sm183 = ROOT / "sitemap.xml"
    if _sm183.exists():
        _smsrc183 = _sm183.read_text(encoding="utf-8")
        _lastmods183 = re.findall(r"<lastmod>([^<]+)</lastmod>", _smsrc183)
        _bad183: list[str] = []
        for _v in _lastmods183:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", _v):
                _bad183.append(f"{_v!r} (format)")
                continue
            try:
                _y, _m, _d = _v.split("-")
                _date183(int(_y), int(_m), int(_d))
            except (ValueError, TypeError) as _e:
                _bad183.append(f"{_v!r} ({_e})")
        _ok183 = len(_lastmods183) > 0 and not _bad183
        check(
            _ok183,
            f"Check 183: sitemap.xml <lastmod> {len(_lastmods183)} 件全て ISO-8601 (YYYY-MM-DD) かつ実在日付",
            (f"Check 183: sitemap.xml <lastmod> 不正値: {'; '.join(_bad183)} — "
             "crawler date parser を silent に壊す。strict YYYY-MM-DD に揃えよ"
             if _bad183 else
             "Check 183: sitemap.xml に <lastmod> 0 件 — vacuous-gate"),
            blocking=True,
        )
    else:
        check(False, "Check 183: sitemap.xml present",
              "Check 183: sitemap.xml が無い", blocking=True)

    # ── 184. sw.js AIO_FILES paths resolve to actual repo files (BLOCKING) ────────
    # sw.js の `AIO_FILES = [...]` 配列内文字列を抽出し、index.html canonical URL の
    # pathname (例 /portfolio/) を strip した repo-relative path で実在 file に resolve
    # することを BLOCKING 強制。Check 160 (pathname 第 1 segment 整合) は素通る path
    # tail drift (例 /portfolio/llms.txt → /portfolio/llms-entry.txt rename + sw.js
    # 未更新) を捕捉し SW の SWR 404 silent fail を防ぐ。Check 182 (ai:* meta 解決)
    # の SW 軸版。
    _sw184 = ROOT / "sw.js"
    _idx184 = ROOT / "index.html"
    if _sw184.exists() and _idx184.exists():
        _swsrc184 = _sw184.read_text(encoding="utf-8")
        _isrc184 = _idx184.read_text(encoding="utf-8")
        _canon184_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc184
        )
        _canon_path184 = ""
        if _canon184_m:
            from urllib.parse import urlparse as _urlparse184
            _canon_path184 = _urlparse184(_canon184_m.group(1)).path  # e.g. "/portfolio/"
        _aio_files184_m = re.search(
            r"const\s+AIO_FILES\s*=\s*\[([^\]]+)\]", _swsrc184
        )
        _aio_paths184: list[str] = []
        if _aio_files184_m:
            _aio_paths184 = re.findall(r"['\"]([^'\"]+)['\"]", _aio_files184_m.group(1))
        _dangling184: list[str] = []
        for _p in _aio_paths184:
            if _canon_path184 and _p.startswith(_canon_path184):
                _rel = _p[len(_canon_path184):]
            else:
                _rel = _p.lstrip("/")
            _target = ROOT / _rel
            if not _target.exists():
                _dangling184.append(f"{_p} → {_rel} (file 不在)")
        _ok184 = (
            _canon_path184 != ""
            and len(_aio_paths184) > 0
            and not _dangling184
        )
        check(
            _ok184,
            f"Check 184: sw.js AIO_FILES {len(_aio_paths184)} 件全て実 file に resolve "
            f"(canonical path '{_canon_path184}' を strip)",
            (f"Check 184: sw.js AIO_FILES 不整合: {'; '.join(_dangling184)} — "
             "SW が rename 後 endpoint を SWR で fetch して silent 404。AIO_FILES の path tail を canonical 配下の "
             "実在 file に揃えよ"
             if _dangling184 else
             "Check 184: sw.js AIO_FILES 抽出不可 / canonical pathname 抽出不可 / 0 件 — vacuous-gate"),
            blocking=True,
        )
    else:
        check(False, "Check 184: sw.js + index.html present",
              "Check 184: sw.js または index.html が無い", blocking=True)

    # ── 185. Canonical URL uses HTTPS scheme (BLOCKING) ────────────────────────────
    # index.html `<link rel="canonical">` href が `https://` で始まることを BLOCKING
    # 強制。`http://` drift は SILENT に SEO / security signal を劣化させる
    # (browser の "Not Secure" 警告 / crawler が HTTPS variant と別 origin と認識し
    # entity 同一性を split / Mixed Content block で sub-resource silent 失敗)。
    # Check 149 は 3 surface 一致を保証するが 3 surface 同時 HTTP 化を素通る scheme
    # 自体の anchor。
    _idx185 = ROOT / "index.html"
    if _idx185.exists():
        _isrc185 = _idx185.read_text(encoding="utf-8")
        _canon185_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc185
        )
        _canon185 = _canon185_m.group(1) if _canon185_m else None
        _ok185 = _canon185 is not None and _canon185.startswith("https://")
        check(
            _ok185,
            f"Check 185: canonical URL は HTTPS scheme ({_canon185!r})",
            (f"Check 185: canonical URL が HTTPS でない: {_canon185!r} — "
             "browser 'Not Secure' 警告 / crawler entity split / Mixed Content block。"
             "`https://` 始まりに揃えよ"
             if _canon185 else
             "Check 185: canonical URL 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 185: index.html present",
              "Check 185: index.html が無い", blocking=True)

    # ── 186. <meta name=author> contains canonical entity identifiers (BLOCKING) ──
    # index.html `<meta name="author">` content が canonical entity name 2 件
    # ("Yuta Yokoi" + "横井雄太") を共に含むことを BLOCKING 強制。drift は SILENT に
    # HTML 層 author signal を entity identity から desync させ generic SEO/HTML
    # crawler (= author meta を読む層) が別 entity を見る。Check 173 (js/identity.js
    # AUTHOR) / Check 172 (manifest entity name variants) の HTML <meta name=author>
    # surface 版。
    _idx186 = ROOT / "index.html"
    if _idx186.exists():
        _isrc186 = _idx186.read_text(encoding="utf-8")
        _author186_m = re.search(
            r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']', _isrc186
        )
        _author186 = _author186_m.group(1) if _author186_m else None
        _required186 = ["Yuta Yokoi", "横井雄太"]
        _missing186 = [n for n in _required186 if _author186 and n not in _author186] if _author186 else _required186
        _ok186 = _author186 is not None and not _missing186
        check(
            _ok186,
            f"Check 186: <meta name=author> に canonical entity name 全件含む ({_author186!r})",
            (f"Check 186: <meta name=author>={_author186!r} に必須名 {_missing186} 欠落 — "
             "HTML 層 author signal が entity identity から desync。CLAUDE.md §1 canonical name "
             "('Yuta Yokoi' + '横井雄太') を共に含めよ"
             if _author186 else
             "Check 186: <meta name=author> meta が抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 186: index.html present",
              "Check 186: index.html が無い", blocking=True)

    # ── 188. robots.txt Sitemap URL resolves to actual repo file (BLOCKING) ───────
    # robots.txt の `Sitemap:` directive URL が canonical URL pathname を strip した
    # repo-relative path で実在 file に resolve することを BLOCKING 強制。Check 63 は
    # origin 整合のみで path tail drift (sitemap.xml → sitemap-v2.xml rename + robots
    # 未更新) を素通る。crawler (Googlebot 等) は sitemap pointer を 404 で skip し
    # sitemap が宣言する全 URL を index しない。Check 182/184 の robots.txt 軸版。
    _rb188 = ROOT / "robots.txt"
    _idx188 = ROOT / "index.html"
    if _rb188.exists() and _idx188.exists():
        _rbsrc188 = _rb188.read_text(encoding="utf-8")
        _isrc188 = _idx188.read_text(encoding="utf-8")
        _canon188_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc188
        )
        _canon_path188 = ""
        if _canon188_m:
            from urllib.parse import urlparse as _urlparse188
            _canon_path188 = _urlparse188(_canon188_m.group(1)).path  # e.g. "/portfolio/"
        _sitemap188_urls = re.findall(r"(?im)^\s*Sitemap:\s*(\S+)", _rbsrc188)
        _dangling188: list[str] = []
        for _u in _sitemap188_urls:
            from urllib.parse import urlparse as _up
            _pth = _up(_u).path
            if _canon_path188 and _pth.startswith(_canon_path188):
                _rel = _pth[len(_canon_path188):]
            else:
                _rel = _pth.lstrip("/")
            _target = ROOT / _rel
            if not _target.exists():
                _dangling188.append(f"{_u} → {_rel} (file 不在)")
        _ok188 = len(_sitemap188_urls) > 0 and not _dangling188
        check(
            _ok188,
            f"Check 188: robots.txt Sitemap: {len(_sitemap188_urls)} 件全て実 file に resolve",
            (f"Check 188: robots.txt Sitemap: 不整合: {'; '.join(_dangling188)} — "
             "crawler が sitemap pointer を 404 で skip し sitemap 宣言 URL を index しない。"
             "robots.txt Sitemap: directive を canonical 配下の実在 file に揃えよ"
             if _dangling188 else
             "Check 188: robots.txt に Sitemap: directive 0 件 — vacuous-gate"),
            blocking=True,
        )
    else:
        check(False, "Check 188: robots.txt + index.html present",
              "Check 188: robots.txt または index.html が無い", blocking=True)

    # ── 189. <meta name=robots> does not contain noindex / none (BLOCKING) ────────
    # index.html `<meta name="robots">` content が `noindex` / `none` を含まないことを
    # BLOCKING 強制 (negative invariant)。silent な noindex drift は全 search engine
    # (Google/Bing/DuckDuckGo + これを backend にする AI search) からのサイト全 deindex
    # = AIO discovery 致命傷で、browser/console/behavior e2e に non-visible。Check 161
    # (robots.txt full-site disallow guard) の HTML meta robots 軸版。
    _idx189 = ROOT / "index.html"
    if _idx189.exists():
        _isrc189 = _idx189.read_text(encoding="utf-8")
        _robots189_m = re.search(
            r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']', _isrc189
        )
        _robots189 = _robots189_m.group(1).lower() if _robots189_m else None
        _forbidden189 = ["noindex", "none"]
        _hits189 = [tok for tok in _forbidden189 if _robots189 and tok in _robots189] if _robots189 else []
        _ok189 = _robots189 is not None and not _hits189
        check(
            _ok189,
            f"Check 189: <meta name=robots>={_robots189!r} に noindex/none 不在 (index 許容)",
            (f"Check 189: <meta name=robots>={_robots189!r} に禁止 token {_hits189} 検出 — "
             "サイト全 deindex (Google/Bing + AI search) で AIO discovery 致命傷。"
             "noindex/none を除去せよ"
             if _hits189 else
             "Check 189: <meta name=robots> 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 189: index.html present",
              "Check 189: index.html が無い", blocking=True)
