"""
checks_canonical_https.py — canonical URL, HTTPS-only & manifest/icon path coherence checks (202-214)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  202. Canonical URL pathname ends with `/`: the `<link rel="canonical">`
       href pathname must end with a trailing slash. Drift (canonical →
       `.../portfolio` without slash) would silently break every Check that
       uses canonical URL as a prefix for repo-relative path stripping
       (Check 153 / 164 / 166 / 171 / 182 / 184 / 188): URLs like
       `https://.../portfolio/llms-full.txt` would no longer share a clean
       prefix with `.../portfolio` (no slash), and `startswith` checks would
       still pass (string prefix), but `[len(prefix):]` would strip too few
       characters and the path tail would start with `/`, breaking
       repo-relative resolution. The trailing-slash invariant is the implicit
       contract those Checks depend on. (BLOCKING)
  203. JSON-LD Person `givenName`/`familyName` canonical decomposition: in
       the primary JSON-LD Person block, `givenName` must equal "雄太" and
       `familyName` must equal "横井" (the canonical Japanese-order name
       decomposition from CLAUDE.md §1). Drift would silently send wrong
       name parts to Schema.org-aware AI/SEO crawlers, breaking last-name /
       first-name search alignment and Knowledge Panel name display.
       Sibling of Check 195 (Person.alternateName variants) for the
       structured name-decomposition axis. (BLOCKING)
  204. JSON-LD WebSite `name` contains site brand markers: in the primary
       JSON-LD WebSite block, the `name` string must contain BOTH "yuta"
       (display brand) AND "AI-Driven PM" (positioning identifier). Drift
       would silently desync the AI/SEO WebSite-level brand signal from the
       canonical title (Check 66 covers `<title>`, this covers JSON-LD
       WebSite.name surface). Sibling of Check 156 (og:site_name presence)
       for the JSON-LD WebSite.name axis. (BLOCKING)
  205. JSON-LD `url` fields all use HTTPS: every `"url": "<URL>"` in index.html
       JSON-LD must start with `https://` (negative invariant — no http://).
       Drift to http:// would silently downgrade AI/SEO crawler URL signals
       (browser Mixed Content blocking, search engines penalising insecure
       URLs, AI crawlers treating http vs https as different origins). Check
       185 (canonical link HTTPS) anchors only the canonical URL declaration;
       this Check extends scheme-anchor invariant to every JSON-LD url
       property across all entity blocks. (BLOCKING)
  206. JSON-LD `@id` URI fields all use HTTPS: every `"@id": "<URI>"` in
       index.html JSON-LD must start with `https://` (URN/other-scheme @ids
       are not used in this site). Drift to http:// would silently fragment
       the JSON-LD entity graph because @id is matched by string-equality —
       a Person @id with http:// would not equal references to https://#person
       elsewhere, splitting entities into disjoint nodes. Sibling of Check 205
       (url HTTPS) for the @id axis; complements Check 176 (own-origin @ids
       use canonical prefix, which is https) for the external-origin @ids
       (nkgr.co.jp/#organization etc.) that 176 does not check. (BLOCKING)
  207. index.html external `src=`/`href=` attributes all use HTTPS: every
       absolute-URL `src="<URL>"` or `href="<URL>"` in index.html that starts
       with a scheme must start with `https://` (negative invariant — no
       http://). Drift to http:// for external sub-resources (Karte CDN,
       Google Fonts CSS, etc.) would silently trigger browser Mixed Content
       blocking on the HTTPS site — the sub-resource silently fails to load
       (no console error in production builds, just missing functionality).
       Sibling of Check 205/206 (JSON-LD url/@id HTTPS) for the HTML element
       attribute axis. (BLOCKING)
  208. JSON-LD date fields are strict ISO-8601 YYYY-MM-DD: every
       `"datePublished"` / `"dateModified"` / `"dateCreated"` value in
       index.html JSON-LD must match strict `YYYY-MM-DD` regex AND parse as a
       valid calendar date. Drift to locale formats (`2026/05/31`, `5/31/26`)
       would silently corrupt freshness signals — Schema.org / Search Console
       consume these dates to determine recency-weighted ranking, and
       non-ISO-8601 dates either fail to parse (dropping freshness signal) or
       misparse (showing wrong "last updated"). Sibling of Check 183 (sitemap
       lastmod ISO-8601) for the JSON-LD date surface. (BLOCKING)
  209. JSON-LD potentialAction `target` URLs share canonical URL prefix: in
       index.html JSON-LD, every `target` URL inside any `potentialAction`
       block must start with the canonical URL prefix. Drift (e.g.
       ReadAction.target pointing at sibling project path) would silently
       advertise the wrong page to AI/voice assistants that consume
       potentialAction (the action would land on a 404). Sibling of Check 153
       (og:image canonical prefix) / Check 171 (ai:* canonical prefix) for
       the potentialAction.target surface. (BLOCKING)

  210. manifest.webmanifest `start_url` / `scope` match canonical URL pathname:
       the PWA manifest's `start_url` and `scope` fields must equal the
       pathname portion of `<link rel=canonical>` href (e.g. canonical
       `https://yutapr0117-design.github.io/portfolio/` → pathname `/portfolio/`).
       Drift would silently install the PWA pointing at a different URL than
       the AIO canonical entity URL, splitting authority signals between two
       URLs (the PWA install lands somewhere AI/search engines do not treat
       as the entity's canonical home). Sibling of Check 150 (og:url ↔
       canonical) / Check 138 (entity url) for the manifest install surface.
       (BLOCKING)

  211. JSON-LD `contentUrl` / `thumbnailUrl` fields share canonical URL prefix:
       in index.html static JSON-LD, every `"contentUrl": "..."` and
       `"thumbnailUrl": "..."` value (ImageObject / MediaObject / AudioObject)
       must start with the canonical URL prefix (own-origin assets). Drift
       (e.g. contentUrl pointing at a CDN or sibling project) would silently
       advertise non-canonical asset URLs to AI/SEO crawlers, splitting
       authority. Sibling of Check 153 (og:image canonical prefix) / Check
       171 (ai:* canonical prefix) / Check 209 (potentialAction.target
       canonical prefix) for the JSON-LD media-asset surface. (BLOCKING)

  212. manifest.webmanifest `icons[].src` is canonical-pathname-prefixed and
       each referenced file is committed: every icon `src` in manifest must
       start with canonical URL pathname (e.g. `/portfolio/`) AND the file
       (mapped to repo root by stripping the pathname prefix) must exist.
       Drift would silently make PWA install fail to load icons (icon path
       points outside the canonical scope, or the file was removed without
       updating manifest). Sibling of Check 210 (manifest start_url/scope
       canonical pathname) / Check 39 (sitemap loc resolves) for the
       manifest icon surface. (BLOCKING)

  213. HTML `<link rel="icon">` / `<link rel="apple-touch-icon">` href starts
       with canonical URL pathname (non-data: only): every non-data: href in
       these tags must start with the canonical URL pathname (e.g.
       `/portfolio/`). Drift (e.g. `/icon.svg` without the `/portfolio/`
       prefix) would silently 404 on production GitHub Pages deploy where the
       site is served under the canonical pathname. Check 163 covers
       file-existence; Check 213 covers canonical-pathname-prefix coherence.
       Sibling of Check 210 / 212 (manifest start_url/scope/icons canonical
       pathname) for the HTML head icon-link surface. (BLOCKING)

  214. JSON-LD `sameAs` URLs all use HTTPS: in index.html static JSON-LD,
       every URL inside any `"sameAs": [...]` array must start with `https://`.
       Drift would silently weaken AI/SEO trust signals (mixed-content
       warnings, authenticity-grade degradation in knowledge graph
       evaluation). Sibling of Check 206 (JSON-LD `@id` HTTPS) / Check 207
       (HTML src/href HTTPS) for the JSON-LD sameAs external-link surface.
       (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 202. Canonical URL pathname ends with `/` (BLOCKING) ──────────────────────
    # index.html `<link rel="canonical">` href の pathname が `/` で終わることを
    # BLOCKING 強制。trailing slash の喪失は Check 153/164/166/171/182/184/188 が
    # 暗黙に依存する prefix 契約を破壊し、startswith は通るが repo-relative path
    # stripping が壊れる。
    from urllib.parse import urlparse as _urlparse202
    _idx202 = ROOT / "index.html"
    if _idx202.exists():
        _isrc202 = _idx202.read_text(encoding="utf-8")
        _canon202_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc202
        )
        _canon202 = _canon202_m.group(1) if _canon202_m else None
        _canon202_path = _urlparse202(_canon202).path if _canon202 else ""
        _ok202 = bool(_canon202_path) and _canon202_path.endswith("/")
        check(
            _ok202,
            f"Check 202: canonical URL pathname が `/` で終わる ({_canon202_path!r})",
            (f"Check 202: canonical URL pathname={_canon202_path!r} が trailing slash 無し — "
             "Check 153/164/166/171/182/184/188 の prefix-strip 契約を破壊。"
             "canonical URL を `/portfolio/` のように `/` で終わらせよ"
             if _canon202 else
             "Check 202: canonical URL 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 202: index.html present",
              "Check 202: index.html が無い", blocking=True)

    # ── 203. JSON-LD Person givenName/familyName canonical decomposition (BLOCKING) ─
    # index.html 静的 JSON-LD の primary Person block の `givenName` が "雄太"・
    # `familyName` が "横井" であることを BLOCKING 強制 (CLAUDE.md §1 canonical
    # 日本語名 decomposition)。drift は SILENT に Schema.org-aware AI/SEO crawler
    # へ誤名前要素を送り Knowledge Panel name display を破壊。Check 195 (alternateName)
    # の structured name-decomposition 軸版。
    _idx203 = ROOT / "index.html"
    if _idx203.exists():
        _isrc203 = _idx203.read_text(encoding="utf-8")
        _person203_m = re.search(r'"@type":\s*"Person"', _isrc203)
        _given203 = None
        _family203 = None
        if _person203_m:
            _line_start = _isrc203.rfind("\n", 0, _person203_m.start()) + 1
            _indent = _isrc203[_line_start:_person203_m.start()]
            _all_persons = [m.start() for m in re.finditer(r'"@type":\s*"Person"', _isrc203)]
            _next = next((p for p in _all_persons if p > _person203_m.start()), len(_isrc203))
            _scope = _isrc203[_person203_m.start():_next]
            _g = re.search(r'\n' + re.escape(_indent) + r'"givenName":\s*"([^"]+)"', _scope)
            _f = re.search(r'\n' + re.escape(_indent) + r'"familyName":\s*"([^"]+)"', _scope)
            _given203 = _g.group(1) if _g else None
            _family203 = _f.group(1) if _f else None
        _expected_g203 = "雄太"
        _expected_f203 = "横井"
        _ok203 = _given203 == _expected_g203 and _family203 == _expected_f203
        check(
            _ok203,
            f"Check 203: primary Person givenName={_given203!r} / familyName={_family203!r} canonical 一致",
            (f"Check 203: primary Person name decomposition drift: "
             f"givenName={_given203!r} (expected {_expected_g203!r}) / "
             f"familyName={_family203!r} (expected {_expected_f203!r}) — "
             "Schema.org 構造化名要素が canonical CLAUDE.md §1 から desync。"
             "JSON-LD givenName/familyName を canonical 値に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 203: index.html present",
              "Check 203: index.html が無い", blocking=True)

    # ── 204. JSON-LD WebSite name contains site brand markers (BLOCKING) ──────────
    # index.html 静的 JSON-LD の primary WebSite block の `name` string が site
    # brand marker ("yuta" + "AI-Driven PM") を共に含むことを BLOCKING 強制。
    # drift は SILENT に WebSite-level brand signal を canonical title (Check 66)
    # から desync させ AI/SEO crawler の site identity 認識を弱体化。Check 156
    # (og:site_name) の JSON-LD WebSite.name 軸版。
    _idx204 = ROOT / "index.html"
    if _idx204.exists():
        _isrc204 = _idx204.read_text(encoding="utf-8")
        _site204_m = re.search(r'"@type":\s*"WebSite"', _isrc204)
        _site_name204 = None
        if _site204_m:
            _line_start = _isrc204.rfind("\n", 0, _site204_m.start()) + 1
            _indent = _isrc204[_line_start:_site204_m.start()]
            _all_sites = [m.start() for m in re.finditer(r'"@type":\s*"WebSite"', _isrc204)]
            _next = next((p for p in _all_sites if p > _site204_m.start()), len(_isrc204))
            _scope = _isrc204[_site204_m.start():_next]
            _n = re.search(r'\n' + re.escape(_indent) + r'"name":\s*"([^"]+)"', _scope)
            _site_name204 = _n.group(1) if _n else None
        _required204 = ["yuta", "AI-Driven PM"]
        _missing204 = [m for m in _required204 if _site_name204 and m not in _site_name204] if _site_name204 else _required204
        _ok204 = _site_name204 is not None and not _missing204
        check(
            _ok204,
            f"Check 204: primary WebSite.name が brand markers {_required204} 全て含む ({_site_name204!r})",
            (f"Check 204: primary WebSite.name に必須 brand marker {_missing204} 欠落 "
             f"(現 name={_site_name204!r}) — WebSite-level brand signal が canonical title "
             "から desync。'yuta' + 'AI-Driven PM' を含む形に揃えよ"
             if _site_name204 else
             "Check 204: primary WebSite.name 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 204: index.html present",
              "Check 204: index.html が無い", blocking=True)

    # ── 205. JSON-LD url fields all use HTTPS (BLOCKING) ──────────────────────────
    # index.html 静的 JSON-LD 内の全 `"url": "<URL>"` の値が `https://` で始まる
    # ことを BLOCKING 強制 (negative invariant)。drift は SILENT に AI/SEO crawler の
    # URL signal を downgrade (Mixed Content block / search insecure penalty /
    # AI crawler が http vs https を別 origin と認識)。Check 185 (canonical link
    # HTTPS) の JSON-LD 全 entity の url field 軸版。
    _idx205 = ROOT / "index.html"
    if _idx205.exists():
        _isrc205 = _idx205.read_text(encoding="utf-8")
        # find all "url": "<value>" inside JSON-LD blocks (within <script
        # type="application/ld+json">...</script>). simplest: scan whole file.
        _all_urls205 = re.findall(r'"url":\s*"([^"]+)"', _isrc205)
        _http205 = [u for u in _all_urls205 if u.startswith("http://")]
        _ok205 = len(_all_urls205) > 0 and not _http205
        check(
            _ok205,
            f"Check 205: JSON-LD url field {len(_all_urls205)} 件全て https://",
            (f"Check 205: JSON-LD url field に http:// scheme drift: {_http205!r} — "
             "AI/SEO crawler の URL signal 劣化 (Mixed Content / scheme split)。"
             "JSON-LD url を全て https:// に揃えよ"
             if _http205 else
             "Check 205: JSON-LD url field 0 件 — vacuous-gate"),
            blocking=True,
        )
    else:
        check(False, "Check 205: index.html present",
              "Check 205: index.html が無い", blocking=True)

    # ── 206. JSON-LD @id URI fields all use HTTPS (BLOCKING) ──────────────────────
    # index.html 静的 JSON-LD 内の全 `"@id": "<URI>"` の値が `https://` で始まる
    # ことを BLOCKING 強制 (URN/other scheme は本 site で未使用)。drift は SILENT に
    # entity graph を分断 (string-equality で参照される @id が http vs https で別
    # entity 扱いになる)。Check 205 (url HTTPS) の @id 軸版・Check 176 (own-origin
    # canonical prefix) の external-origin (nkgr.co.jp 等) 補完。
    _idx206 = ROOT / "index.html"
    if _idx206.exists():
        _isrc206 = _idx206.read_text(encoding="utf-8")
        _all_ids206 = re.findall(r'"@id":\s*"([^"]+)"', _isrc206)
        _http206 = [u for u in _all_ids206 if u.startswith("http://")]
        _ok206 = len(_all_ids206) > 0 and not _http206
        check(
            _ok206,
            f"Check 206: JSON-LD @id field {len(_all_ids206)} 件全て https://",
            (f"Check 206: JSON-LD @id field に http:// scheme drift: {_http206!r} — "
             "entity graph 分断 (string-equality 参照で http vs https が別 entity 扱い)。"
             "JSON-LD @id を全て https:// に揃えよ"
             if _http206 else
             "Check 206: JSON-LD @id field 0 件 — vacuous-gate"),
            blocking=True,
        )
    else:
        check(False, "Check 206: index.html present",
              "Check 206: index.html が無い", blocking=True)

    # ── 207. index.html external src/href attributes all use HTTPS (BLOCKING) ─────
    # index.html の `src="<URL>"` / `href="<URL>"` で absolute URL (scheme 付き) の
    # 全てが `https://` で始まることを BLOCKING 強制 (negative invariant)。drift は
    # SILENT に Mixed Content blocking で sub-resource load 失敗 (production console
    # error 抑制化で気付きにくい)。Check 205/206 (JSON-LD url/@id HTTPS) の HTML
    # 属性 axis 版。
    _idx207 = ROOT / "index.html"
    if _idx207.exists():
        _isrc207 = _idx207.read_text(encoding="utf-8")
        # Extract src=/href= values where value starts with a scheme (e.g.
        # https?:// or //) — only flag http:// (relative paths and data: URIs
        # are exempt).
        _all_attrs207 = re.findall(
            r'(?:src|href)\s*=\s*["\'](http://[^"\']+)["\']', _isrc207
        )
        _ok207 = len(_all_attrs207) == 0
        check(
            _ok207,
            "Check 207: index.html src=/href= 属性に http:// 不在 (Mixed Content guard)",
            (f"Check 207: index.html src=/href= 属性に http:// scheme: {_all_attrs207!r} — "
             "browser Mixed Content blocking で sub-resource silent load 失敗。"
             "全 absolute URL を https:// に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 207: index.html present",
              "Check 207: index.html が無い", blocking=True)

    # ── 208. JSON-LD date fields are strict ISO-8601 YYYY-MM-DD (BLOCKING) ────────
    # index.html 静的 JSON-LD 内の全 `"datePublished"`/`"dateModified"`/`"dateCreated"`
    # 値が strict `YYYY-MM-DD` regex かつ実在カレンダー日付であることを BLOCKING 強制。
    # drift は SILENT に Schema.org / Search Console の recency-weighted ranking 用
    # freshness signal を corruption (locale 形式は parse 失敗 or 誤 parse)。Check 183
    # (sitemap lastmod ISO-8601) の JSON-LD date 軸版。
    from datetime import date as _date208
    _idx208 = ROOT / "index.html"
    if _idx208.exists():
        _isrc208 = _idx208.read_text(encoding="utf-8")
        _date_fields208 = ["datePublished", "dateModified", "dateCreated"]
        _dates208 = []
        for _fld in _date_fields208:
            for _m in re.finditer(rf'"{_fld}":\s*"([^"]+)"', _isrc208):
                _dates208.append((_fld, _m.group(1)))
        _bad208: list[str] = []
        for _fld, _v in _dates208:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", _v):
                _bad208.append(f"{_fld}={_v!r} (format)")
                continue
            try:
                _y, _mo, _d = _v.split("-")
                _date208(int(_y), int(_mo), int(_d))
            except (ValueError, TypeError) as _e:
                _bad208.append(f"{_fld}={_v!r} ({_e})")
        _ok208 = len(_dates208) > 0 and not _bad208
        check(
            _ok208,
            f"Check 208: JSON-LD date field {len(_dates208)} 件全て ISO-8601 (YYYY-MM-DD) かつ実在日付",
            (f"Check 208: JSON-LD date field 不正値: {'; '.join(_bad208)} — "
             "Schema.org freshness signal 破壊。strict YYYY-MM-DD に揃えよ"
             if _bad208 else
             "Check 208: JSON-LD date field 0 件 — vacuous-gate"),
            blocking=True,
        )
    else:
        check(False, "Check 208: index.html present",
              "Check 208: index.html が無い", blocking=True)

    # ── 209. JSON-LD potentialAction target shares canonical URL prefix (BLOCKING) ─
    # index.html 静的 JSON-LD 内の全 `potentialAction` block の `target` URL が
    # canonical URL prefix で始まることを BLOCKING 強制。drift は SILENT に AI/voice
    # assistant の action を間違った page (404 等) へ誘導。Check 153/171 の
    # potentialAction.target 軸版。
    _idx209 = ROOT / "index.html"
    if _idx209.exists():
        _isrc209 = _idx209.read_text(encoding="utf-8")
        _canon209_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc209
        )
        _canon209 = _canon209_m.group(1) if _canon209_m else None
        # find each potentialAction block scope (from `"potentialAction":` to next
        # closing `}` at the same indent — approx via lookahead of ~600 chars).
        _drifts209: list[str] = []
        _target_count209 = 0
        for _m in re.finditer(r'"potentialAction":', _isrc209):
            _scope = _isrc209[_m.start():_m.start() + 1500]
            for _t in re.finditer(r'"target":\s*(?:\[([^\]]*)\]|"([^"]+)")', _scope):
                if _t.group(1) is not None:
                    # array form: extract each quoted URL
                    for _u in re.findall(r'"([^"]+)"', _t.group(1)):
                        _target_count209 += 1
                        if _canon209 and not _u.startswith(_canon209):
                            _drifts209.append(f"target={_u!r}")
                else:
                    _u = _t.group(2)
                    _target_count209 += 1
                    if _canon209 and not _u.startswith(_canon209):
                        _drifts209.append(f"target={_u!r}")
                break  # only first target per potentialAction block
        _ok209 = (
            _canon209 is not None
            and _target_count209 > 0
            and not _drifts209
        )
        check(
            _ok209,
            f"Check 209: potentialAction.target {_target_count209} 件全て canonical prefix {_canon209!r} で始まる",
            (f"Check 209: potentialAction.target drift: {_drifts209!r} ≠ canonical prefix "
             f"{_canon209!r} — AI/voice assistant action が wrong page 誘導 (404)。"
             "target URL を canonical 配下に揃えよ"
             if _drifts209 else
             "Check 209: canonical / potentialAction.target 抽出不可 / 0 件"),
            blocking=True,
        )
    else:
        check(False, "Check 209: index.html present",
              "Check 209: index.html が無い", blocking=True)

    # ── 210. manifest.webmanifest start_url / scope == canonical pathname (BLOCKING) ─
    # index.html `<link rel=canonical>` href の pathname (例 /portfolio/) と
    # manifest.webmanifest の start_url / scope が一致することを BLOCKING 強制。drift は
    # SILENT に PWA install が canonical URL とは別の URL を home に持つことになり、
    # entity authority が二分される (AI/search は canonical を entity 識別子とする)。
    from urllib.parse import urlparse as _urlparse210
    _idx210 = ROOT / "index.html"
    _mani210 = ROOT / "manifest.webmanifest"
    if _idx210.exists() and _mani210.exists():
        _isrc210 = _idx210.read_text(encoding="utf-8")
        _canon210_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc210
        )
        _canon210 = _canon210_m.group(1) if _canon210_m else None
        _canon_path210 = _urlparse210(_canon210).path if _canon210 else None
        try:
            _mdata210 = json.loads(_mani210.read_text(encoding="utf-8"))
        except json.JSONDecodeError as _e:
            _mdata210 = None
            _parse_err210: str | None = str(_e)
        else:
            _parse_err210 = None
        _start210 = _mdata210.get("start_url") if isinstance(_mdata210, dict) else None
        _scope210 = _mdata210.get("scope") if isinstance(_mdata210, dict) else None
        _drifts210: list[str] = []
        if _canon_path210 is None:
            _drifts210.append("canonical pathname 抽出不可")
        if _parse_err210:
            _drifts210.append(f"manifest JSON parse 失敗: {_parse_err210}")
        if _start210 is None:
            _drifts210.append("start_url 欠落")
        elif _canon_path210 and _start210 != _canon_path210:
            _drifts210.append(f"start_url={_start210!r} != canonical pathname={_canon_path210!r}")
        if _scope210 is None:
            _drifts210.append("scope 欠落")
        elif _canon_path210 and _scope210 != _canon_path210:
            _drifts210.append(f"scope={_scope210!r} != canonical pathname={_canon_path210!r}")
        _ok210 = not _drifts210
        check(
            _ok210,
            f"Check 210: manifest.webmanifest start_url={_start210!r} / scope={_scope210!r} == canonical pathname={_canon_path210!r}",
            (f"Check 210: manifest drift: {_drifts210!r} — PWA install が canonical URL "
             "と異なる URL を home にし entity authority が二分。manifest.webmanifest の "
             "start_url / scope を canonical pathname (例 /portfolio/) に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 210: index.html + manifest.webmanifest present",
              "Check 210: index.html もしくは manifest.webmanifest が無い", blocking=True)

    # ── 211. JSON-LD contentUrl / thumbnailUrl share canonical URL prefix (BLOCKING) ─
    # index.html 静的 JSON-LD 内の全 `contentUrl` / `thumbnailUrl` 値が canonical URL
    # prefix で始まることを BLOCKING 強制。drift は SILENT に AI/SEO crawler へ
    # non-canonical な asset URL を流し authority を二分。Check 153/171/209 と同
    # canonical-prefix family の JSON-LD media-asset 軸版。
    _idx211 = ROOT / "index.html"
    if _idx211.exists():
        _isrc211 = _idx211.read_text(encoding="utf-8")
        _canon211_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc211
        )
        _canon211 = _canon211_m.group(1) if _canon211_m else None
        _url_fields211 = ["contentUrl", "thumbnailUrl"]
        _urls211: list[tuple[str, str]] = []
        for _fld in _url_fields211:
            for _m in re.finditer(rf'"{_fld}":\s*"([^"]+)"', _isrc211):
                _urls211.append((_fld, _m.group(1)))
        _drifts211: list[str] = []
        if _canon211:
            for _fld, _v in _urls211:
                if not _v.startswith(_canon211):
                    _drifts211.append(f"{_fld}={_v!r}")
        _ok211 = (
            _canon211 is not None
            and len(_urls211) > 0
            and not _drifts211
        )
        check(
            _ok211,
            f"Check 211: JSON-LD contentUrl/thumbnailUrl {len(_urls211)} 件全て canonical prefix {_canon211!r} で始まる",
            (f"Check 211: JSON-LD media-asset URL drift: {_drifts211!r} ≠ canonical "
             f"prefix {_canon211!r} — AI/SEO crawler が non-canonical asset URL を取得し "
             "entity authority が二分。contentUrl / thumbnailUrl を canonical 配下に揃えよ"
             if _drifts211 else
             "Check 211: canonical / contentUrl/thumbnailUrl 抽出不可 / 0 件"),
            blocking=True,
        )
    else:
        check(False, "Check 211: index.html present",
              "Check 211: index.html が無い", blocking=True)

    # ── 212. manifest.webmanifest icons src canonical pathname + 実在 (BLOCKING) ───
    # manifest.webmanifest の全 `icons[].src` が canonical URL pathname (例 /portfolio/)
    # で始まること + pathname を strip して repo root へ map した path が実在することを
    # BLOCKING 強制。drift は SILENT に PWA install が icon を 404 で取得失敗。
    from urllib.parse import urlparse as _urlparse212
    _idx212 = ROOT / "index.html"
    _mani212 = ROOT / "manifest.webmanifest"
    if _idx212.exists() and _mani212.exists():
        _isrc212 = _idx212.read_text(encoding="utf-8")
        _canon212_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc212
        )
        _canon212 = _canon212_m.group(1) if _canon212_m else None
        _canon_path212 = _urlparse212(_canon212).path if _canon212 else None
        try:
            _mdata212 = json.loads(_mani212.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata212 = None
        _icons212 = (
            _mdata212.get("icons", []) if isinstance(_mdata212, dict) else []
        )
        _icon_srcs212 = [
            _ic.get("src") for _ic in _icons212
            if isinstance(_ic, dict) and isinstance(_ic.get("src"), str)
        ]
        _drifts212: list[str] = []
        if not _canon_path212:
            _drifts212.append("canonical pathname 抽出不可")
        if not _icon_srcs212:
            _drifts212.append("icons[].src 0 件")
        for _src in _icon_srcs212:
            if _canon_path212 and not _src.startswith(_canon_path212):
                _drifts212.append(f"src={_src!r} canonical pathname {_canon_path212!r} 不一致")
                continue
            if _canon_path212:
                _rel = _src[len(_canon_path212):]
                _f = ROOT / _rel
                if not _f.exists():
                    _drifts212.append(f"src={_src!r} → {_rel!r} がリポジトリに無い")
        _ok212 = not _drifts212
        check(
            _ok212,
            f"Check 212: manifest icons[].src {len(_icon_srcs212)} 件全て canonical pathname {_canon_path212!r} prefix かつ実在",
            (f"Check 212: manifest icons drift: {_drifts212!r} — PWA install が "
             "icon を 404 で取得失敗。icons[].src を canonical pathname + 実在 file へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 212: index.html + manifest.webmanifest present",
              "Check 212: index.html もしくは manifest.webmanifest が無い", blocking=True)

    # ── 213. <link rel=icon/apple-touch-icon> href canonical pathname (BLOCKING) ──
    # index.html の <link rel="icon"> / <link rel="apple-touch-icon"> の href
    # (non-data: のみ) が canonical URL pathname (例 /portfolio/) で始まることを
    # BLOCKING 強制。drift は SILENT に production GitHub Pages で 404。
    from urllib.parse import urlparse as _urlparse213
    _idx213 = ROOT / "index.html"
    if _idx213.exists():
        _isrc213 = _idx213.read_text(encoding="utf-8")
        _canon213_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc213
        )
        _canon213 = _canon213_m.group(1) if _canon213_m else None
        _canon_path213 = _urlparse213(_canon213).path if _canon213 else None
        _hrefs213: list[tuple[str, str]] = []
        for _m in re.finditer(
            r'<link\s+rel=["\'](icon|apple-touch-icon)["\'][^>]*\shref=["\']([^"\']+)["\']',
            _isrc213,
        ):
            _hrefs213.append((_m.group(1), _m.group(2)))
        # also handle type=...; rel between attributes
        for _m in re.finditer(
            r'<link\s+rel=["\'](icon|apple-touch-icon)["\'][^>]*?\stype=["\'][^"\']+["\'][^>]*?\shref=["\']([^"\']+)["\']',
            _isrc213,
        ):
            if (_m.group(1), _m.group(2)) not in _hrefs213:
                _hrefs213.append((_m.group(1), _m.group(2)))
        _drifts213: list[str] = []
        if not _canon_path213:
            _drifts213.append("canonical pathname 抽出不可")
        _non_data213 = [(_r, _h) for _r, _h in _hrefs213 if not _h.startswith("data:")]
        if not _non_data213:
            _drifts213.append("非 data: な <link rel=icon/apple-touch-icon> 0 件")
        for _r, _h in _non_data213:
            if _canon_path213 and not _h.startswith(_canon_path213):
                _drifts213.append(f"<link rel={_r}> href={_h!r} canonical pathname {_canon_path213!r} 不一致")
        _ok213 = not _drifts213
        check(
            _ok213,
            f"Check 213: <link rel=icon/apple-touch-icon> non-data: href {len(_non_data213)} 件全て canonical pathname {_canon_path213!r} prefix",
            (f"Check 213: <link rel=icon/apple-touch-icon> href drift: {_drifts213!r} — "
             "production GitHub Pages で 404 化。canonical pathname prefix へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 213: index.html present",
              "Check 213: index.html が無い", blocking=True)

    # ── 214. JSON-LD sameAs URLs all HTTPS (BLOCKING) ─────────────────────────────
    # index.html 静的 JSON-LD 内の全 `sameAs` array の URL が `https://` で始まることを
    # BLOCKING 強制。drift は SILENT に AI/SEO の authenticity-grade を下げる
    # (mixed-content / 認証低下)。Check 206 (@id HTTPS) / Check 207 (HTML src/href HTTPS)
    # の sameAs external-link 軸版。
    _idx214 = ROOT / "index.html"
    if _idx214.exists():
        _isrc214 = _idx214.read_text(encoding="utf-8")
        _same_arrays214 = re.findall(r'"sameAs":\s*\[([^\]]*)\]', _isrc214)
        _urls214: list[str] = []
        for _arr in _same_arrays214:
            for _u in re.findall(r'"([^"]+)"', _arr):
                _urls214.append(_u)
        _bad214 = [u for u in _urls214 if not u.startswith("https://")]
        _ok214 = len(_urls214) > 0 and not _bad214
        check(
            _ok214,
            f"Check 214: JSON-LD sameAs URL {len(_urls214)} 件全て HTTPS",
            (f"Check 214: JSON-LD sameAs に non-HTTPS URL: {_bad214!r} — "
             "AI/SEO authenticity-grade 劣化。https:// へ揃えよ"
             if _bad214 else
             "Check 214: JSON-LD sameAs URL 抽出不可 / 0 件"),
            blocking=True,
        )
    else:
        check(False, "Check 214: index.html present",
              "Check 214: index.html が無い", blocking=True)
