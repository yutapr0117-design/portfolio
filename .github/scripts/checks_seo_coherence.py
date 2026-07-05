"""
checks_seo_coherence.py — AIO/SEO cross-surface URL, canonical & format coherence checks
(extracted from check_repository_consistency.py — check.py split track・category "SEO/URL coherence").

This module owns the contiguous cluster of Checks 273-302 — a large, coherent block enforcing
cross-surface consistency of the site's canonical URL, HTTPS-only URLs, manifest↔JSON-LD entity
equality, strict format contracts (VERSION / CACHE_NAME / manifest_version), and og/twitter/meta
coherence. Each Check reads its own target files directly via Path.read_text(); an
annotation-aware, def-aware free-variable analysis confirms zero external `_`-vars and no global
html/style/mainjs dependency. Several sections use a nested walker/counter that mutates a
section-local accumulator; at module level that used a `global` declaration, so when relocated
into run() those `global _accNNN` are mechanically converted to `nonlocal _accNNN` (identical
semantics — the accumulator is a run()-local, defined at section scope before the nested fn).
NOTE: these are READ-ONLY coherence assertions — the module moves check *code* only (no C6 edit).

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  273. JSON-LD `datePublished` / `dateModified` / `dateCreated` NOT in
       future: every date value in index.html static JSON-LD MUST be on
       or before today. Drift silently corrupts AI/SEO recency-weighted
       retrieval (this site does not schedule pre-publish). Sibling of
       Check 243 (SITE_CONFIG/ai:last-modified not future) / Check 218
       (datePublished <= dateModified) for the JSON-LD date not-future
       axis. (BLOCKING)

  274. aio-manifest `entity.name` matches primary Person `name` (JSON-LD):
       the `.well-known/aio-manifest.json` `entity.name` value MUST equal
       the primary JSON-LD Person `name` (where `@id == canonical +
       "#person"`) — currently both `"Yuta Yokoi"`. Drift silently splits
       the entity identity between the AIO manifest layer and the
       JSON-LD layer. Sibling of Check 172 (entity name variants combined)
       for the manifest ↔ JSON-LD name direct-equality axis. (BLOCKING)

  275. aio-manifest affiliation.organization_name == JSON-LD Organization
       `name` (nkgr.co.jp/#organization): the `.well-known/aio-manifest.json`
       `entity.affiliation.organization_name` value MUST equal the JSON-LD
       primary Organization node `name` where `@id ==
       "https://nkgr.co.jp/#organization"` (currently both "株式会社日本経営").
       Sibling of Check 274 (Person name equality) for the manifest ↔
       JSON-LD Organization name direct-equality axis. (BLOCKING)

  276. aio-manifest affiliation.organization_url == JSON-LD Organization
       `url`: the `.well-known/aio-manifest.json`
       `entity.affiliation.organization_url` value MUST equal the JSON-LD
       primary Organization node `url` (`@id ==
       https://nkgr.co.jp/#organization`, currently both
       "https://nkgr.co.jp/"). Sibling of Check 275 (Organization name)
       for the manifest ↔ JSON-LD Organization url direct-equality axis.
       (BLOCKING)

  277. aio-manifest entity.authoritative_context == canonical + llms-full.txt:
       the `.well-known/aio-manifest.json` `entity.authoritative_context`
       value MUST equal `<canonical>llms-full.txt` (canonical URL prefix +
       "llms-full.txt" — currently
       "https://yutapr0117-design.github.io/portfolio/llms-full.txt").
       Drift silently misroute AI/agent authoritative-context ingestion.
       Sibling of Check 274/275/276 for the manifest authoritative-context
       URL derivation axis. (BLOCKING)

  278. sitemap.xml all `<loc>` URLs use HTTPS: every `<loc>` value in
       sitemap.xml MUST start with `https://`. Drift to `http://` would
       silently expose crawler paths on insecure transport (Mixed Content
       intervention on HTTPS-hosted crawler contexts). Sibling of Check
       206/207/214 for the sitemap loc HTTPS-only axis. (BLOCKING)

  279. robots.txt `Sitemap:` directive URL uses HTTPS: every `Sitemap:`
       line in robots.txt MUST advertise an `https://` URL. Drift to
       `http://` would silently make crawlers fetch the sitemap over
       insecure transport. Sibling of Check 278 (sitemap.xml loc HTTPS)
       for the robots.txt sitemap-directive HTTPS axis. (BLOCKING)

  280. main.js SITE_CONFIG CANONICAL_URL + REPO_URL use HTTPS: both URL
       string literals in SITE_CONFIG MUST start with `https://`. Drift
       to `http://` in either would silently downgrade JS-emitted URL
       references (JSON-LD injection / SPA meta emission all use these).
       Sibling of Check 279 (robots.txt Sitemap: HTTPS) for the JS
       SITE_CONFIG URL-scheme axis. (BLOCKING)

  281. main.js SITE_CONFIG.REPO_URL == HTML `<meta name="ai:repository">`:
       the JS-side canonical repo URL and the AIO meta-declared repo URL
       MUST match exactly. Drift silently makes JS-emitted code
       references diverge from the AI crawler discovery layer. Sibling of
       Check 280 (SITE_CONFIG URL scheme) for the SITE_CONFIG.REPO_URL ↔
       ai:repository equality axis. (BLOCKING)

  282. main.js SITE_CONFIG.CANONICAL_URL == HTML `<meta name="ai:canonical">`
       content: the JS-side canonical URL and the AIO meta-declared
       canonical URL MUST match exactly. Check 149 covers three-way
       equality across `<link rel="canonical">` / aio-manifest /
       SITE_CONFIG.CANONICAL_URL, but the parallel ai:canonical meta axis
       is separate. Sibling of Check 281 (REPO_URL ↔ ai:repository) for
       the SITE_CONFIG.CANONICAL_URL ↔ ai:canonical direct-equality axis.
       (BLOCKING)

  283. HTML `<meta name="ai:aio-manifest">` content == canonical +
       ".well-known/aio-manifest.json": the ai:aio-manifest meta content
       MUST equal canonical URL prefix + ".well-known/aio-manifest.json"
       exactly. Check 184 verifies the path resolves to some existing
       file; Check 283 asserts it targets the canonical `.well-known/`
       location. Sibling of Check 282 for the ai:aio-manifest exact-URL
       derivation axis. (BLOCKING)

  284. HTML `<meta name="ai:context">` == canonical+"llms-full.txt" AND
       `<meta name="ai:entrypoint">` == canonical+"llms.txt": the two
       ai:* discovery meta URLs MUST match their canonical exact
       derivations. Sibling of Check 283 (ai:aio-manifest exact
       derivation) for the ai:context / ai:entrypoint exact-URL
       derivation axis. (BLOCKING)

  285. main.js SITE_CONFIG.VERSION strict format `v\d+`: the VERSION
       string literal MUST match `^v\d+$` (single lowercase 'v' followed
       by one or more digits). Check 2 (ai:version == SITE_CONFIG.VERSION)
       ensures parity but format itself is a separate invariant. Drift to
       e.g. `V74` / `v74.1` / `v-74` silently breaks downstream regexes
       and human recognition. (BLOCKING)

  286. sw.js CACHE_NAME strict format `^portfolio-aio-v\d+$`: the CACHE
       _NAME literal MUST match `^portfolio-aio-v\d+$` exactly. Check 19
       ensures version parity with ai:version, but the constant format
       itself is a separate invariant (a rename to `portfolio-cache-v74`
       still parses via Check 19 regex but breaks the semantic contract).
       Sibling of Check 285 (SITE_CONFIG.VERSION format) for the sw.js
       CACHE_NAME format axis. (BLOCKING)

  287. aio-manifest.json `manifest_version` strict format `^\d+\.\d+$`:
       the `.well-known/aio-manifest.json` `manifest_version` field MUST
       match `^\d+\.\d+$` (major.minor form). Drift to non-semver strings
       silently breaks manifest schema consumers that parse this field.
       Sibling of Check 285/286 (SITE_CONFIG.VERSION / CACHE_NAME) for
       the manifest_version format axis. (BLOCKING)

  288. main.js SITE_CONFIG.ARTICLE_ROUTES entries all resolve to router
       cases in js/router.js: every string element in the
       ARTICLE_ROUTES array MUST appear as `case '<route>':` in
       js/router.js. Drift = a ghost route name → og:type=article dead
       pointer / meta-management applies Article JSON-LD to a
       non-existent route. Sibling of Check 137 (router↔switch case
       coverage) for the ARTICLE_ROUTES ↔ router cases axis. (BLOCKING)

  289. aio-manifest.json evidence list minimum counts + path uniqueness:
       `source_of_truth[]` MUST have >= 3 entries, `supporting_evidence[]`
       and `observational_evidence[]` MUST each have >= 1 entry, and
       within each list, `path` values must be unique. Drift = accidental
       shrinkage or duplicate-entry ingestion problems. Sibling of Check
       219 (path ⊆ MANIFEST_PATH_TO_LOCAL) for the evidence list
       structural axis. (BLOCKING)

  290. aio-manifest entity.role is EXACTLY the 3 canonical values (strict):
       the `entity.role` list in `.well-known/aio-manifest.json` MUST be
       exactly `{"AI-Driven PM", "IT Consultant", "KERNEL Framework
       Designer"}` (as a set — no extras, no missing, no duplicates).
       Check 169 enforces substring presence but drift to `[..., "Extra
       Role"]` still passes 169 yet corrupts AIO entity role parity.
       Check 290 covers strict set-equality. (BLOCKING)

  291. aio-manifest entity.name_alt strict set-equality: the
       `entity.name_alt` list in .well-known/aio-manifest.json MUST be
       exactly `{"Yokoi Yuta", "yuta"}` (as a set — no extras, no
       missing, no duplicates). Check 172 covers combined name-variants
       coverage but strict set-equality is a separate invariant. Sibling
       of Check 290 (role strict set-equality) for the name_alt axis.
       (BLOCKING)

  292. aio-manifest entity.name_ja == "横井雄太" (strict equality):
       the `entity.name_ja` value in .well-known/aio-manifest.json MUST
       equal `"横井雄太"` exactly. Sibling of Check 290/291 for the
       name_ja strict-equality axis. (BLOCKING)

  293. aio-manifest entity.disambiguation contains all 5 canonical
       academic domains: the `entity.disambiguation` string MUST contain
       all of `agriculture`, `chemistry`, `medicine`, `entomology`,
       `computer science` (case-sensitive substring). Drift = silently
       weakening the disambiguation against academic Yuta Yokoi
       researchers in specific fields. Sibling of Check 170
       (disambiguation top-level markers) for the disambiguation
       academic-domain axis. (BLOCKING)

  294. aio-manifest disambiguation contains all 4 non-academic markers:
       `entity.disambiguation` MUST contain all of `diplomat`, `artist`,
       `musician`, `patent inventor` (case-sensitive substring). Sibling
       of Check 293 for the disambiguation non-academic-domain axis.
       (BLOCKING)

  295. HTML `<meta name="publisher">` content contains canonical entity
       names: the `<meta name="publisher">` content in index.html MUST
       contain BOTH `"Yuta Yokoi"` AND `"横井雄太"`. Sibling of Check 186
       (author meta) for the publisher meta canonical-name axis.
       (BLOCKING)

  296. index.html has `<link rel="alternate">` for both AIO canonical
       routes: `href="./llms.txt"` AND `href="./llms-full.txt"` MUST
       exist as `<link rel="alternate">` tags in index.html. Drift =
       silent removal of canonical AIO discovery entrypoint from the
       HTML head. Sibling of Check 283/284 (ai:* exact URL derivation)
       for the alternate link discovery-entrypoint axis. (BLOCKING)

  297. sitemap.xml canonical (priority=1.0) entry structural completeness:
       the sitemap.xml `<url>` entry with `<priority>1.0</priority>` MUST
       contain `<loc>`, `<lastmod>`, `<changefreq>`, `<priority>`, AND at
       least one `<image:image>` child. Drift = the canonical entry
       silently loses image sitemap coverage. Sibling of Check 230
       (canonical priority=1.0 uniqueness) for the canonical entry
       structural-completeness axis. (BLOCKING)

  298. og:image:width and og:image:height values are numeric integers:
       the index.html `<meta property="og:image:width">` /
       `<meta property="og:image:height">` content values MUST parse as
       positive integers. Drift = social card layout collapses (Facebook
       falls back to default sizing when width/height are non-numeric).
       Sibling of Check 20 (presence) for the og:image:width/height
       numeric-value axis. (BLOCKING)

  299. `<meta name="twitter:card">` content is a valid Twitter card type:
       the index.html `<meta name="twitter:card">` content MUST be one of
       `summary`, `summary_large_image`, `player`, `app` (Twitter spec).
       Drift = Twitter falls back to link-preview default. Sibling of
       Check 155 (og:title ↔ twitter:title) for the twitter:card value
       axis. (BLOCKING)

  300. `<meta property="og:image:alt">` content contains canonical entity
       + role markers: the index.html og:image:alt content MUST contain
       both `"横井雄太"` AND `"AI-Driven PM"`. Drift = accessibility
       alt text loses entity attribution / role signal. Sibling of Check
       20 (og:image:alt presence) for the og:image:alt content-value axis.
       (BLOCKING)

  301. index.html `<link rel="preconnect">` for Google Fonts hosts: both
       `href="https://fonts.googleapis.com"` AND
       `href="https://fonts.gstatic.com"` MUST exist as preconnect hints.
       Silent removal degrades LCP / CWV because font stylesheets and
       woff2 files come from different hosts. Sibling of Check 73a
       (preload as= attribute) for the preconnect axis. (BLOCKING)

  302. `<body data-canonical>` attribute matches `<link rel=canonical>`
       href: the `<body>` tag `data-canonical` attribute MUST equal the
       canonical URL. Drift silently misroutes JS reader hydration and
       runtime canonical detection. Sibling of Check 149 (canonical
       URL three-way coherence) for the body attribute axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 273. JSON-LD dates NOT in future (BLOCKING) ───────────────────────────────
    # index.html JSON-LD の全 `datePublished` / `dateModified` / `dateCreated` 値が
    # today 以下であることを BLOCKING 強制。Check 243 (SITE_CONFIG/ai:last-modified
    # not future) の JSON-LD date 軸版。
    from datetime import date as _date273
    _idx273 = ROOT / "index.html"
    if _idx273.exists():
        _isrc273 = _idx273.read_text(encoding="utf-8")
        _today273 = _date273.today()
        _date_fields273 = ("datePublished", "dateModified", "dateCreated")
        _blocks273 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc273,
            flags=re.DOTALL,
        )
        _futures273: list[str] = []
        _total_dates273 = 0
        def _walk273(node: object, path: str) -> None:
            nonlocal _total_dates273
            if isinstance(node, dict):
                for _f in _date_fields273:
                    _v = node.get(_f)
                    if isinstance(_v, str):
                        _total_dates273 += 1
                        try:
                            _d = _date273.fromisoformat(_v[:10])
                        except ValueError:
                            continue  # Check 208 が format を担う
                        if _d > _today273:
                            _futures273.append(f"{path}.{_f}={_v!r}")
                for k, v in node.items():
                    _walk273(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk273(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks273):
            try:
                _walk273(json.loads(_blk), f"block{_bi}")
            except json.JSONDecodeError:
                continue
        _ok273 = _total_dates273 > 0 and not _futures273
        check(
            _ok273,
            f"Check 273: JSON-LD date ({_total_dates273} 件) 全て today ({_today273.isoformat()}) 以前",
            (f"Check 273: 未来日 detected: {_futures273!r} — AI/SEO recency 誤認 / "
             "ranking corruption。today 以下へ修正"),
            blocking=True,
        )
    else:
        check(False, "Check 273: index.html present",
              "Check 273: index.html が無い", blocking=True)

    # ── 274. aio-manifest entity.name == primary Person.name (JSON-LD) (BLOCKING) ─
    # .well-known/aio-manifest.json の entity.name が index.html JSON-LD の primary
    # Person node (@id == canonical+#person) の name と strict 一致することを BLOCKING
    # 強制。Check 172 (name variants combined) の direct-equality 軸版。
    _mani274 = ROOT / ".well-known" / "aio-manifest.json"
    _idx274 = ROOT / "index.html"
    if _mani274.exists() and _idx274.exists():
        try:
            _mdata274 = json.loads(_mani274.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata274 = None
        _entity_name274 = None
        if isinstance(_mdata274, dict):
            _entity_name274 = _mdata274.get("entity", {}).get("name")
        _isrc274 = _idx274.read_text(encoding="utf-8")
        _canon274_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc274
        )
        _canon274 = _canon274_m.group(1) if _canon274_m else None
        _expected_pid274 = (_canon274 or "") + "#person"
        _blocks274 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc274,
            flags=re.DOTALL,
        )
        _primary_pname274 = None
        def _walk274(node: object) -> None:
            nonlocal _primary_pname274
            if isinstance(node, dict):
                if (
                    node.get("@type") == "Person"
                    and node.get("@id") == _expected_pid274
                    and _primary_pname274 is None
                    and isinstance(node.get("name"), str)
                ):
                    _primary_pname274 = node["name"]
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk274(item)
                    else:
                        _walk274(v)
            elif isinstance(node, list):
                for item in node:
                    _walk274(item)
        for _blk in _blocks274:
            try:
                _walk274(json.loads(_blk))
            except json.JSONDecodeError:
                continue
        _ok274 = (
            isinstance(_entity_name274, str)
            and isinstance(_primary_pname274, str)
            and _entity_name274 == _primary_pname274
        )
        check(
            _ok274,
            f"Check 274: aio-manifest entity.name={_entity_name274!r} == primary Person.name={_primary_pname274!r}",
            (f"Check 274: name drift: aio-manifest.entity.name={_entity_name274!r}, "
             f"JSON-LD primary Person.name={_primary_pname274!r} — entity identity split。"
             "両者を同一 canonical name へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 274: aio-manifest.json + index.html present",
              "Check 274: aio-manifest.json もしくは index.html が無い", blocking=True)

    # ── 275. aio-manifest affiliation.organization_name == JSON-LD Org.name (BLOCKING) ─
    # .well-known/aio-manifest.json の entity.affiliation.organization_name が
    # index.html JSON-LD primary Organization node (@id ==
    # https://nkgr.co.jp/#organization) の name と strict 一致することを BLOCKING 強制。
    # Check 274 の Organization 軸版。
    _PRIMARY_ORG_ID275 = "https://nkgr.co.jp/#organization"
    _mani275 = ROOT / ".well-known" / "aio-manifest.json"
    _idx275 = ROOT / "index.html"
    if _mani275.exists() and _idx275.exists():
        try:
            _mdata275 = json.loads(_mani275.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata275 = None
        _aff_org275 = None
        if isinstance(_mdata275, dict):
            _aff_org275 = (
                _mdata275.get("entity", {}).get("affiliation", {}).get("organization_name")
            )
        _isrc275 = _idx275.read_text(encoding="utf-8")
        _blocks275 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc275,
            flags=re.DOTALL,
        )
        _primary_org_name275 = None
        def _walk275(node: object) -> None:
            nonlocal _primary_org_name275
            if isinstance(node, dict):
                if (
                    node.get("@type") == "Organization"
                    and node.get("@id") == _PRIMARY_ORG_ID275
                    and _primary_org_name275 is None
                    and isinstance(node.get("name"), str)
                ):
                    _primary_org_name275 = node["name"]
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk275(item)
                    else:
                        _walk275(v)
            elif isinstance(node, list):
                for item in node:
                    _walk275(item)
        for _blk in _blocks275:
            try:
                _walk275(json.loads(_blk))
            except json.JSONDecodeError:
                continue
        _ok275 = (
            isinstance(_aff_org275, str)
            and isinstance(_primary_org_name275, str)
            and _aff_org275 == _primary_org_name275
        )
        check(
            _ok275,
            f"Check 275: aio-manifest affiliation.organization_name={_aff_org275!r} == JSON-LD Organization.name={_primary_org_name275!r}",
            (f"Check 275: Organization name drift: aio-manifest={_aff_org275!r} / "
             f"JSON-LD={_primary_org_name275!r} — employer identity split。両者を同一値へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 275: aio-manifest.json + index.html present",
              "Check 275: aio-manifest.json もしくは index.html が無い", blocking=True)

    # ── 276. aio-manifest affiliation.organization_url == JSON-LD Org.url (BLOCKING) ─
    # .well-known/aio-manifest.json の entity.affiliation.organization_url が
    # index.html JSON-LD primary Organization (@id == https://nkgr.co.jp/#organization)
    # の url と strict 一致することを BLOCKING 強制。Check 275 の url 軸版。
    _PRIMARY_ORG_ID276 = "https://nkgr.co.jp/#organization"
    _mani276 = ROOT / ".well-known" / "aio-manifest.json"
    _idx276 = ROOT / "index.html"
    if _mani276.exists() and _idx276.exists():
        try:
            _mdata276 = json.loads(_mani276.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata276 = None
        _aff_url276 = None
        if isinstance(_mdata276, dict):
            _aff_url276 = (
                _mdata276.get("entity", {}).get("affiliation", {}).get("organization_url")
            )
        _isrc276 = _idx276.read_text(encoding="utf-8")
        _blocks276 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc276,
            flags=re.DOTALL,
        )
        _primary_org_url276 = None
        def _walk276(node: object) -> None:
            nonlocal _primary_org_url276
            if isinstance(node, dict):
                if (
                    node.get("@type") == "Organization"
                    and node.get("@id") == _PRIMARY_ORG_ID276
                    and _primary_org_url276 is None
                    and isinstance(node.get("url"), str)
                ):
                    _primary_org_url276 = node["url"]
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk276(item)
                    else:
                        _walk276(v)
            elif isinstance(node, list):
                for item in node:
                    _walk276(item)
        for _blk in _blocks276:
            try:
                _walk276(json.loads(_blk))
            except json.JSONDecodeError:
                continue
        _ok276 = (
            isinstance(_aff_url276, str)
            and isinstance(_primary_org_url276, str)
            and _aff_url276 == _primary_org_url276
        )
        check(
            _ok276,
            f"Check 276: aio-manifest affiliation.organization_url={_aff_url276!r} == JSON-LD Organization.url={_primary_org_url276!r}",
            (f"Check 276: Organization url drift: aio-manifest={_aff_url276!r} / "
             f"JSON-LD={_primary_org_url276!r} — canonical URL split。両者を同一値へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 276: aio-manifest.json + index.html present",
              "Check 276: aio-manifest.json もしくは index.html が無い", blocking=True)

    # ── 277. aio-manifest entity.authoritative_context == canonical+llms-full.txt (BLOCKING) ─
    # .well-known/aio-manifest.json の entity.authoritative_context 値が
    # canonical URL + "llms-full.txt" に一致することを BLOCKING 強制。
    _mani277 = ROOT / ".well-known" / "aio-manifest.json"
    _idx277 = ROOT / "index.html"
    if _mani277.exists() and _idx277.exists():
        try:
            _mdata277 = json.loads(_mani277.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata277 = None
        _auth_ctx277 = None
        if isinstance(_mdata277, dict):
            _auth_ctx277 = _mdata277.get("entity", {}).get("authoritative_context")
        _isrc277 = _idx277.read_text(encoding="utf-8")
        _canon277_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc277
        )
        _canon277 = _canon277_m.group(1) if _canon277_m else None
        _expected277 = (_canon277 or "") + "llms-full.txt"
        _ok277 = (
            isinstance(_auth_ctx277, str)
            and _auth_ctx277 == _expected277
        )
        check(
            _ok277,
            f"Check 277: aio-manifest entity.authoritative_context={_auth_ctx277!r} == canonical+llms-full.txt={_expected277!r}",
            (f"Check 277: authoritative_context drift: aio-manifest={_auth_ctx277!r} / "
             f"expected={_expected277!r} — AI/agent authoritative-context ingestion 誤 route"),
            blocking=True,
        )
    else:
        check(False, "Check 277: aio-manifest.json + index.html present",
              "Check 277: aio-manifest.json もしくは index.html が無い", blocking=True)

    # ── 278. sitemap.xml all <loc> URLs use HTTPS (BLOCKING) ──────────────────────
    # sitemap.xml の全 <loc> URL が `https://` で始まることを BLOCKING 強制 (negative
    # invariant: http:// 0)。drift で crawler が非 secure transport で URL を取得。
    _sitemap278 = ROOT / "sitemap.xml"
    if _sitemap278.exists():
        _ssrc278 = _sitemap278.read_text(encoding="utf-8")
        _locs278 = re.findall(r"<loc>([^<]+)</loc>", _ssrc278)
        _bad278 = [u for u in _locs278 if u.startswith("http://")]
        _ok278 = len(_locs278) > 0 and not _bad278
        check(
            _ok278,
            f"Check 278: sitemap.xml <loc> URLs {len(_locs278)} 件全て HTTPS",
            (f"Check 278: sitemap.xml に non-HTTPS <loc>: {_bad278!r} — crawler が "
             "insecure transport で fetch。https:// に揃えよ"
             if _bad278 else
             "Check 278: sitemap.xml <loc> 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 278: sitemap.xml present",
              "Check 278: sitemap.xml が無い", blocking=True)

    # ── 279. robots.txt Sitemap: directive URL HTTPS (BLOCKING) ───────────────────
    # robots.txt の全 `Sitemap:` directive の URL が `https://` で始まることを
    # BLOCKING 強制。Check 278 の robots.txt sitemap-directive 軸版。
    _robots279 = ROOT / "robots.txt"
    if _robots279.exists():
        _rsrc279 = _robots279.read_text(encoding="utf-8")
        _smaps279 = re.findall(r"^Sitemap:\s*(\S+)", _rsrc279, flags=re.MULTILINE)
        _bad279 = [u for u in _smaps279 if u.startswith("http://")]
        _ok279 = len(_smaps279) > 0 and not _bad279
        check(
            _ok279,
            f"Check 279: robots.txt Sitemap: URL {len(_smaps279)} 件全て HTTPS",
            (f"Check 279: robots.txt に non-HTTPS Sitemap: {_bad279!r} — crawler が "
             "insecure transport で sitemap fetch。https:// に揃えよ"
             if _bad279 else
             "Check 279: robots.txt Sitemap: 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 279: robots.txt present",
              "Check 279: robots.txt が無い", blocking=True)

    # ── 280. main.js SITE_CONFIG CANONICAL_URL + REPO_URL HTTPS (BLOCKING) ────────
    # main.js SITE_CONFIG CANONICAL_URL + REPO_URL 両 URL string literal が `https://`
    # で始まることを BLOCKING 強制。Check 279 の JS SITE_CONFIG URL-scheme 軸版。
    _main280 = ROOT / "main.js"
    if _main280.exists():
        _msrc280 = _main280.read_text(encoding="utf-8")
        _canon_lit280 = re.search(r"CANONICAL_URL:\s*['\"]([^'\"]+)['\"]", _msrc280)
        _repo_lit280 = re.search(r"REPO_URL:\s*['\"]([^'\"]+)['\"]", _msrc280)
        _bad280: list[str] = []
        for _lbl, _m in (("CANONICAL_URL", _canon_lit280), ("REPO_URL", _repo_lit280)):
            if _m is None:
                _bad280.append(f"{_lbl} 抽出不可")
                continue
            _v = _m.group(1)
            if not _v.startswith("https://"):
                _bad280.append(f"{_lbl}={_v!r}")
        _ok280 = not _bad280
        check(
            _ok280,
            f"Check 280: SITE_CONFIG CANONICAL_URL + REPO_URL 共に https://",
            (f"Check 280: 違反: {_bad280!r} — JS 側 URL emission が insecure に。https:// へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 280: main.js present",
              "Check 280: main.js が無い", blocking=True)

    # ── 281. main.js SITE_CONFIG.REPO_URL == HTML ai:repository (BLOCKING) ────────
    # main.js SITE_CONFIG.REPO_URL の値と index.html `<meta name="ai:repository">` の
    # content が strict 一致することを BLOCKING 強制。Check 280 の direct-equality 軸版。
    _main281 = ROOT / "main.js"
    _idx281 = ROOT / "index.html"
    if _main281.exists() and _idx281.exists():
        _msrc281 = _main281.read_text(encoding="utf-8")
        _isrc281 = _idx281.read_text(encoding="utf-8")
        _repo_lit281_m = re.search(r"REPO_URL:\s*['\"]([^'\"]+)['\"]", _msrc281)
        _ai_repo281_m = re.search(
            r'<meta\s+name=["\']ai:repository["\']\s+content=["\']([^"\']+)["\']', _isrc281
        )
        _repo_lit281 = _repo_lit281_m.group(1) if _repo_lit281_m else None
        _ai_repo281 = _ai_repo281_m.group(1) if _ai_repo281_m else None
        _ok281 = (
            isinstance(_repo_lit281, str)
            and isinstance(_ai_repo281, str)
            and _repo_lit281 == _ai_repo281
        )
        check(
            _ok281,
            f"Check 281: SITE_CONFIG.REPO_URL={_repo_lit281!r} == ai:repository={_ai_repo281!r}",
            (f"Check 281: repo URL drift: SITE_CONFIG.REPO_URL={_repo_lit281!r} / "
             f"ai:repository={_ai_repo281!r} — JS 側 code URL と AI 側 discovery が"
             " split。両者を canonical GitHub URL へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 281: main.js + index.html present",
              "Check 281: main.js もしくは index.html が無い", blocking=True)

    # ── 282. main.js SITE_CONFIG.CANONICAL_URL == HTML ai:canonical (BLOCKING) ────
    # main.js SITE_CONFIG.CANONICAL_URL 値と index.html `<meta name="ai:canonical">` の
    # content が strict 一致することを BLOCKING 強制。Check 281 の canonical URL 軸版。
    _main282 = ROOT / "main.js"
    _idx282 = ROOT / "index.html"
    if _main282.exists() and _idx282.exists():
        _msrc282 = _main282.read_text(encoding="utf-8")
        _isrc282 = _idx282.read_text(encoding="utf-8")
        _cu_lit282_m = re.search(r"CANONICAL_URL:\s*['\"]([^'\"]+)['\"]", _msrc282)
        _ai_cu282_m = re.search(
            r'<meta\s+name=["\']ai:canonical["\']\s+content=["\']([^"\']+)["\']', _isrc282
        )
        _cu_lit282 = _cu_lit282_m.group(1) if _cu_lit282_m else None
        _ai_cu282 = _ai_cu282_m.group(1) if _ai_cu282_m else None
        _ok282 = (
            isinstance(_cu_lit282, str)
            and isinstance(_ai_cu282, str)
            and _cu_lit282 == _ai_cu282
        )
        check(
            _ok282,
            f"Check 282: SITE_CONFIG.CANONICAL_URL={_cu_lit282!r} == ai:canonical={_ai_cu282!r}",
            (f"Check 282: canonical URL drift: SITE_CONFIG.CANONICAL_URL={_cu_lit282!r} / "
             f"ai:canonical={_ai_cu282!r} — JS 側 canonical と AI 側 discovery が split。"
             "両者を同一 canonical URL へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 282: main.js + index.html present",
              "Check 282: main.js もしくは index.html が無い", blocking=True)

    # ── 283. HTML ai:aio-manifest == canonical + .well-known/aio-manifest.json (BLOCKING) ─
    # index.html `<meta name="ai:aio-manifest">` content が
    # canonical URL + ".well-known/aio-manifest.json" と strict 一致することを
    # BLOCKING 強制。Check 184 (path resolves) の exact derivation 軸版。
    _idx283 = ROOT / "index.html"
    if _idx283.exists():
        _isrc283 = _idx283.read_text(encoding="utf-8")
        _canon283_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc283
        )
        _canon283 = _canon283_m.group(1) if _canon283_m else None
        _ai_aiom283_m = re.search(
            r'<meta\s+name=["\']ai:aio-manifest["\']\s+content=["\']([^"\']+)["\']', _isrc283
        )
        _ai_aiom283 = _ai_aiom283_m.group(1) if _ai_aiom283_m else None
        _expected283 = (_canon283 or "") + ".well-known/aio-manifest.json"
        _ok283 = (
            isinstance(_ai_aiom283, str)
            and _ai_aiom283 == _expected283
        )
        check(
            _ok283,
            f"Check 283: ai:aio-manifest={_ai_aiom283!r} == canonical+.well-known/aio-manifest.json={_expected283!r}",
            (f"Check 283: ai:aio-manifest drift: {_ai_aiom283!r} / expected={_expected283!r} "
             "— AIO discovery が canonical .well-known/ location 外を参照。訂正せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 283: index.html present",
              "Check 283: index.html が無い", blocking=True)

    # ── 284. ai:context + ai:entrypoint exact-URL derivation (BLOCKING) ───────────
    # index.html `<meta name="ai:context">` == canonical + "llms-full.txt" AND
    # `<meta name="ai:entrypoint">` == canonical + "llms.txt" を BLOCKING 強制。
    # Check 283 の ai:context / ai:entrypoint 軸版。
    _idx284 = ROOT / "index.html"
    if _idx284.exists():
        _isrc284 = _idx284.read_text(encoding="utf-8")
        _canon284_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc284
        )
        _canon284 = _canon284_m.group(1) if _canon284_m else ""
        _pairs284 = [
            ("ai:context", "llms-full.txt"),
            ("ai:entrypoint", "llms.txt"),
        ]
        _bad284: list[str] = []
        for _name, _suffix in _pairs284:
            _m = re.search(
                rf'<meta\s+name=["\']{re.escape(_name)}["\']\s+content=["\']([^"\']+)["\']',
                _isrc284,
            )
            _v = _m.group(1) if _m else None
            _expected = _canon284 + _suffix
            if _v != _expected:
                _bad284.append(f"{_name}={_v!r} (expected {_expected!r})")
        _ok284 = not _bad284
        check(
            _ok284,
            f"Check 284: ai:context + ai:entrypoint 全 exact-URL derivation OK",
            (f"Check 284: 違反: {_bad284!r} — AI/agent discovery 経路が canonical exact "
             "location から drift。canonical + suffix に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 284: index.html present",
              "Check 284: index.html が無い", blocking=True)

    # ── 285. main.js SITE_CONFIG.VERSION strict format v\d+ (BLOCKING) ────────────
    # main.js SITE_CONFIG.VERSION 値が `^v\d+$` (小文字 v + 数字) regex に一致することを
    # BLOCKING 強制。Check 2 (parity) の format 軸版。
    _main285 = ROOT / "main.js"
    if _main285.exists():
        _msrc285 = _main285.read_text(encoding="utf-8")
        _ver285_m = re.search(r"VERSION:\s*['\"]([^'\"]+)['\"]", _msrc285)
        _ver285 = _ver285_m.group(1) if _ver285_m else None
        _ok285 = isinstance(_ver285, str) and bool(re.match(r"^v\d+$", _ver285))
        check(
            _ok285,
            f"Check 285: SITE_CONFIG.VERSION={_ver285!r} matches ^v\\d+$",
            (f"Check 285: SITE_CONFIG.VERSION={_ver285!r} format 違反 — v<数字> 以外は "
             "downstream regex/parser を破壊。'v74' 等 canonical format へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 285: main.js present",
              "Check 285: main.js が無い", blocking=True)

    # ── 286. sw.js CACHE_NAME strict format ^portfolio-aio-v\d+$ (BLOCKING) ───────
    # sw.js CACHE_NAME 値が `^portfolio-aio-v\d+$` regex に一致することを BLOCKING
    # 強制。Check 19 (version parity) の format 軸版。
    _sw286 = ROOT / "sw.js"
    if _sw286.exists():
        _ssrc286 = _sw286.read_text(encoding="utf-8")
        _cache_lit286_m = re.search(r"CACHE_NAME\s*=\s*['\"]([^'\"]+)['\"]", _ssrc286)
        _cache_lit286 = _cache_lit286_m.group(1) if _cache_lit286_m else None
        _ok286 = isinstance(_cache_lit286, str) and bool(re.match(r"^portfolio-aio-v\d+$", _cache_lit286))
        check(
            _ok286,
            f"Check 286: sw.js CACHE_NAME={_cache_lit286!r} matches ^portfolio-aio-v\\d+$",
            (f"Check 286: sw.js CACHE_NAME={_cache_lit286!r} format 違反 — semantic contract "
             "崩壊。'portfolio-aio-v<数字>' へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 286: sw.js present",
              "Check 286: sw.js が無い", blocking=True)

    # ── 287. aio-manifest.json manifest_version strict format ^\d+\.\d+$ (BLOCKING) ─
    # .well-known/aio-manifest.json の manifest_version 値が `^\d+\.\d+$` regex
    # (major.minor) に一致することを BLOCKING 強制。Check 285/286 の manifest_version
    # 軸版。
    _mani287 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani287.exists():
        try:
            _mdata287 = json.loads(_mani287.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata287 = None
        _mver287 = None
        if isinstance(_mdata287, dict):
            _mver287 = _mdata287.get("manifest_version")
        _ok287 = isinstance(_mver287, str) and bool(re.match(r"^\d+\.\d+$", _mver287))
        check(
            _ok287,
            f"Check 287: aio-manifest.json manifest_version={_mver287!r} matches ^\\d+\\.\\d+$",
            (f"Check 287: manifest_version={_mver287!r} format 違反 — schema consumer が "
             "parse 失敗。'major.minor' form へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 287: aio-manifest.json present",
              "Check 287: aio-manifest.json が無い", blocking=True)

    # ── 288. SITE_CONFIG.ARTICLE_ROUTES entries ⊆ js/router.js switch cases (BLOCKING) ─
    # main.js SITE_CONFIG.ARTICLE_ROUTES 配列の全 string 要素が js/router.js の
    # `case '<route>':` に出現することを BLOCKING 強制。Check 137 の ARTICLE_ROUTES 軸版。
    _main288 = ROOT / "main.js"
    _router288 = ROOT / "js" / "router.js"
    if _main288.exists() and _router288.exists():
        _msrc288 = _main288.read_text(encoding="utf-8")
        _rsrc288 = _router288.read_text(encoding="utf-8")
        _ar288_m = re.search(r"ARTICLE_ROUTES:\s*(\[[^\]]*\])", _msrc288)
        _ar288: list[str] = []
        if _ar288_m:
            _ar288 = re.findall(r"['\"]([^'\"]+)['\"]", _ar288_m.group(1))
        _cases288 = set(re.findall(r"case\s+['\"]([^'\"]+)['\"]", _rsrc288))
        _missing288 = [r for r in _ar288 if r not in _cases288]
        _ok288 = len(_ar288) > 0 and not _missing288
        check(
            _ok288,
            f"Check 288: ARTICLE_ROUTES ({_ar288!r}) 全て js/router.js switch cases に出現",
            (f"Check 288: ghost route: {_missing288!r} — og:type=article dead pointer。"
             "ARTICLE_ROUTES から除去 or js/router.js に case 追加"
             if _missing288 else
             "Check 288: ARTICLE_ROUTES 0 件 — vacuous-fail (article route が全く無い)"),
            blocking=True,
        )
    else:
        check(False, "Check 288: main.js + js/router.js present",
              "Check 288: main.js もしくは js/router.js が無い", blocking=True)

    # ── 289. aio-manifest evidence list counts + path uniqueness (BLOCKING) ───────
    # aio-manifest.json の source_of_truth (>= 3) + supporting_evidence (>= 1) +
    # observational_evidence (>= 1) 各 minimum count と、各 list 内 path 一意性を
    # BLOCKING 強制。Check 219 の structural axis 版。
    _mani289 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani289.exists():
        try:
            _mdata289 = json.loads(_mani289.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata289 = None
        _requirements289 = [
            ("source_of_truth", 3),
            ("supporting_evidence", 1),
            ("observational_evidence", 1),
        ]
        _violations289: list[str] = []
        if isinstance(_mdata289, dict):
            for _key, _minc in _requirements289:
                _lst = _mdata289.get(_key, [])
                if not isinstance(_lst, list):
                    _violations289.append(f"{_key} は list でない")
                    continue
                if len(_lst) < _minc:
                    _violations289.append(f"{_key} count={len(_lst)} < {_minc}")
                # path uniqueness
                _paths = [e.get("path") for e in _lst if isinstance(e, dict) and isinstance(e.get("path"), str)]
                from collections import Counter as _Counter289
                _dupes = [p for p, c in _Counter289(_paths).items() if c > 1]
                if _dupes:
                    _violations289.append(f"{_key} 重複 path: {_dupes!r}")
        else:
            _violations289.append("aio-manifest parse 失敗")
        _ok289 = not _violations289
        check(
            _ok289,
            f"Check 289: aio-manifest evidence lists minimum counts + path uniqueness OK",
            (f"Check 289: 違反: {_violations289!r} — evidence structural sanity 崩壊。"
             "minimum count と path uniqueness を復旧"),
            blocking=True,
        )
    else:
        check(False, "Check 289: aio-manifest.json present",
              "Check 289: aio-manifest.json が無い", blocking=True)

    # ── 290. aio-manifest entity.role strict set-equality (BLOCKING) ──────────────
    # .well-known/aio-manifest.json entity.role が canonical 3 role の set と strict
    # 一致することを BLOCKING 強制。Check 169 (substring presence) の strict axis 版。
    _CANONICAL_ROLES290 = {"AI-Driven PM", "IT Consultant", "KERNEL Framework Designer"}
    _mani290 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani290.exists():
        try:
            _mdata290 = json.loads(_mani290.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata290 = None
        _roles290 = None
        if isinstance(_mdata290, dict):
            _roles290 = _mdata290.get("entity", {}).get("role")
        _ok290 = (
            isinstance(_roles290, list)
            and set(_roles290) == _CANONICAL_ROLES290
            and len(_roles290) == len(_CANONICAL_ROLES290)  # no duplicates
        )
        check(
            _ok290,
            f"Check 290: aio-manifest entity.role={_roles290!r} == canonical 3 role set (strict)",
            (f"Check 290: entity.role drift: got={_roles290!r}, expected set="
             f"{sorted(_CANONICAL_ROLES290)!r} — extras/missing/duplicates。canonical 3 role のみへ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 290: aio-manifest.json present",
              "Check 290: aio-manifest.json が無い", blocking=True)

    # ── 291. aio-manifest entity.name_alt strict set-equality (BLOCKING) ──────────
    # .well-known/aio-manifest.json entity.name_alt が canonical variant set
    # ("Yokoi Yuta", "yuta") と strict 一致することを BLOCKING 強制。Check 290 の
    # name_alt 軸版。
    _CANONICAL_NAME_ALT291 = {"Yokoi Yuta", "yuta"}
    _mani291 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani291.exists():
        try:
            _mdata291 = json.loads(_mani291.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata291 = None
        _names291 = None
        if isinstance(_mdata291, dict):
            _names291 = _mdata291.get("entity", {}).get("name_alt")
        _ok291 = (
            isinstance(_names291, list)
            and set(_names291) == _CANONICAL_NAME_ALT291
            and len(_names291) == len(_CANONICAL_NAME_ALT291)
        )
        check(
            _ok291,
            f"Check 291: aio-manifest entity.name_alt={_names291!r} == canonical variant set (strict)",
            (f"Check 291: name_alt drift: got={_names291!r}, expected set="
             f"{sorted(_CANONICAL_NAME_ALT291)!r} — extras/missing/duplicates。canonical variants のみへ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 291: aio-manifest.json present",
              "Check 291: aio-manifest.json が無い", blocking=True)

    # ── 292. aio-manifest entity.name_ja == "横井雄太" (strict) (BLOCKING) ────────
    # .well-known/aio-manifest.json entity.name_ja が canonical Japanese 名
    # "横井雄太" と strict 一致することを BLOCKING 強制。Check 290/291 の name_ja 軸版。
    _mani292 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani292.exists():
        try:
            _mdata292 = json.loads(_mani292.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata292 = None
        _nja292 = None
        if isinstance(_mdata292, dict):
            _nja292 = _mdata292.get("entity", {}).get("name_ja")
        _ok292 = isinstance(_nja292, str) and _nja292 == "横井雄太"
        check(
            _ok292,
            f"Check 292: aio-manifest entity.name_ja={_nja292!r} == '横井雄太' (strict)",
            (f"Check 292: name_ja drift: got={_nja292!r}, expected='横井雄太' — "
             "canonical Japanese 名へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 292: aio-manifest.json present",
              "Check 292: aio-manifest.json が無い", blocking=True)

    # ── 293. aio-manifest disambiguation contains 5 academic domains (BLOCKING) ───
    # .well-known/aio-manifest.json entity.disambiguation が canonical 5 academic
    # domains 全てを含むことを BLOCKING 強制。Check 170 の academic-domain 軸版。
    _ACADEMIC_DOMAINS293 = [
        "agriculture", "chemistry", "medicine", "entomology", "computer science",
    ]
    _mani293 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani293.exists():
        try:
            _mdata293 = json.loads(_mani293.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata293 = None
        _disamb293 = None
        if isinstance(_mdata293, dict):
            _disamb293 = _mdata293.get("entity", {}).get("disambiguation")
        _missing293 = []
        if isinstance(_disamb293, str):
            _missing293 = [d for d in _ACADEMIC_DOMAINS293 if d not in _disamb293]
        else:
            _missing293 = ["entity.disambiguation 欠落/非 string"]
        _ok293 = not _missing293
        check(
            _ok293,
            f"Check 293: aio-manifest disambiguation contains all 5 academic domains",
            (f"Check 293: 欠落 academic domain marker: {_missing293!r} — disambiguation "
             "が学術系 Yuta Yokoi との分離を弱化。5 domain 全てを disambiguation に含めよ"),
            blocking=True,
        )
    else:
        check(False, "Check 293: aio-manifest.json present",
              "Check 293: aio-manifest.json が無い", blocking=True)

    # ── 294. disambiguation 4 non-academic markers (BLOCKING) ─────────────────────
    # .well-known/aio-manifest.json entity.disambiguation が 4 non-academic markers
    # (diplomat/artist/musician/patent inventor) を全て含むことを BLOCKING 強制。
    # Check 293 の non-academic 軸版。
    _NON_ACADEMIC294 = ["diplomat", "artist", "musician", "patent inventor"]
    _mani294 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani294.exists():
        try:
            _mdata294 = json.loads(_mani294.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata294 = None
        _disamb294 = None
        if isinstance(_mdata294, dict):
            _disamb294 = _mdata294.get("entity", {}).get("disambiguation")
        if isinstance(_disamb294, str):
            _missing294 = [d for d in _NON_ACADEMIC294 if d not in _disamb294]
        else:
            _missing294 = ["entity.disambiguation 欠落/非 string"]
        _ok294 = not _missing294
        check(
            _ok294,
            f"Check 294: aio-manifest disambiguation contains all 4 non-academic markers",
            (f"Check 294: 欠落 non-academic marker: {_missing294!r} — disambiguation "
             "が非学術系 Yuta Yokoi (外交官/芸術家/音楽家/発明家) との分離を弱化。"
             "4 marker 全てを disambiguation に含めよ"),
            blocking=True,
        )
    else:
        check(False, "Check 294: aio-manifest.json present",
              "Check 294: aio-manifest.json が無い", blocking=True)

    # ── 295. HTML meta publisher contains canonical names (BLOCKING) ──────────────
    # index.html `<meta name="publisher">` content が canonical entity name 両方
    # ("Yuta Yokoi" AND "横井雄太") を含むことを BLOCKING 強制。Check 186 (author meta)
    # の publisher 軸版。
    _idx295 = ROOT / "index.html"
    if _idx295.exists():
        _isrc295 = _idx295.read_text(encoding="utf-8")
        _pub295_m = re.search(
            r'<meta\s+name=["\']publisher["\']\s+content=["\']([^"\']+)["\']', _isrc295
        )
        _pub295 = _pub295_m.group(1) if _pub295_m else None
        _required295 = ["Yuta Yokoi", "横井雄太"]
        _missing295 = []
        if isinstance(_pub295, str):
            _missing295 = [n for n in _required295 if n not in _pub295]
        else:
            _missing295 = ["publisher meta 欠落"]
        _ok295 = not _missing295
        check(
            _ok295,
            f"Check 295: <meta name=publisher> content={_pub295!r} contains 両 canonical name",
            (f"Check 295: 欠落 canonical name: {_missing295!r} — publisher meta が "
             "entity 帰属を薄める。'Yuta Yokoi (横井雄太)' 形式へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 295: index.html present",
              "Check 295: index.html が無い", blocking=True)

    # ── 296. <link rel=alternate> for AIO canonical routes (BLOCKING) ─────────────
    # index.html に `<link rel="alternate" ... href="./llms.txt">` AND
    # `<link rel="alternate" ... href="./llms-full.txt">` が存在することを BLOCKING
    # 強制。Check 283/284 の alternate link discovery-entrypoint 軸版。
    _idx296 = ROOT / "index.html"
    if _idx296.exists():
        _isrc296 = _idx296.read_text(encoding="utf-8")
        _required_alts296 = ["./llms.txt", "./llms-full.txt"]
        _missing296 = []
        for _href in _required_alts296:
            _pat = re.compile(
                r'<link\s+rel=["\']alternate["\'][^>]*href=["\']' + re.escape(_href) + r'["\']'
            )
            if not _pat.search(_isrc296):
                _missing296.append(_href)
        _ok296 = not _missing296
        check(
            _ok296,
            "Check 296: index.html has <link rel=alternate> for both llms.txt and llms-full.txt",
            (f"Check 296: 欠落 alternate link href: {_missing296!r} — AIO discovery "
             "entrypoint が HTML head から欠落。<link rel=alternate href=./llms.txt|llms-full.txt> を追加"),
            blocking=True,
        )
    else:
        check(False, "Check 296: index.html present",
              "Check 296: index.html が無い", blocking=True)

    # ── 297. sitemap.xml canonical priority=1.0 entry structural completeness (BLOCKING) ─
    # sitemap.xml で <priority>1.0</priority> を持つ <url> entry が loc / lastmod /
    # changefreq / priority + <image:image> 全 5 要素を持つことを BLOCKING 強制。
    # Check 230 (canonical priority=1.0 uniqueness) の structural completeness 軸版。
    _sitemap297 = ROOT / "sitemap.xml"
    if _sitemap297.exists():
        _ssrc297 = _sitemap297.read_text(encoding="utf-8")
        _canonical_entry297 = None
        for _url_block in re.findall(r"<url>(.*?)</url>", _ssrc297, flags=re.DOTALL):
            if re.search(r"<priority>\s*1\.0\s*</priority>", _url_block):
                _canonical_entry297 = _url_block
                break
        _missing297 = []
        if _canonical_entry297 is None:
            _missing297.append("priority=1.0 entry 不在")
        else:
            _required_tags297 = ["<loc>", "<lastmod>", "<changefreq>", "<priority>", "<image:image>"]
            for _tag in _required_tags297:
                if _tag not in _canonical_entry297:
                    _missing297.append(f"canonical entry から {_tag} 欠落")
        _ok297 = not _missing297
        check(
            _ok297,
            f"Check 297: sitemap canonical entry has all required tags + <image:image>",
            (f"Check 297: 違反: {_missing297!r} — canonical entry の structural "
             "completeness 崩壊。5 tag 全てを canonical entry に含めよ"),
            blocking=True,
        )
    else:
        check(False, "Check 297: sitemap.xml present",
              "Check 297: sitemap.xml が無い", blocking=True)

    # ── 298. og:image:width / og:image:height are positive integers (BLOCKING) ────
    # index.html `<meta property="og:image:width">` / `og:image:height` content が
    # positive integer に parse できることを BLOCKING 強制。Check 20 (presence) の
    # numeric-value 軸版。
    _idx298 = ROOT / "index.html"
    if _idx298.exists():
        _isrc298 = _idx298.read_text(encoding="utf-8")
        _pairs298 = [
            ("og:image:width", None),
            ("og:image:height", None),
        ]
        _bad298: list[str] = []
        for _name, _ in _pairs298:
            _m = re.search(
                r'<meta\s+property=["\']' + re.escape(_name) + r'["\']\s+content=["\']([^"\']+)["\']',
                _isrc298,
            )
            if _m is None:
                _bad298.append(f"{_name} 抽出不可")
                continue
            _v = _m.group(1)
            try:
                _n = int(_v)
                if _n <= 0:
                    _bad298.append(f"{_name}={_v!r} <= 0")
            except ValueError:
                _bad298.append(f"{_name}={_v!r} not int")
        _ok298 = not _bad298
        check(
            _ok298,
            f"Check 298: og:image:width + og:image:height 両方 positive integer",
            (f"Check 298: 違反: {_bad298!r} — social card layout collapse。"
             "og:image:width/height を正整数 string に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 298: index.html present",
              "Check 298: index.html が無い", blocking=True)

    # ── 299. <meta name=twitter:card> spec-valid content (BLOCKING) ───────────────
    # index.html `<meta name="twitter:card">` content が Twitter spec 4 値
    # (summary / summary_large_image / player / app) のいずれかであることを BLOCKING
    # 強制。Check 155 の twitter:card 軸版。
    _VALID_TWITTER_CARDS299 = {"summary", "summary_large_image", "player", "app"}
    _idx299 = ROOT / "index.html"
    if _idx299.exists():
        _isrc299 = _idx299.read_text(encoding="utf-8")
        _tc299_m = re.search(
            r'<meta\s+name=["\']twitter:card["\']\s+content=["\']([^"\']+)["\']', _isrc299
        )
        _tc299 = _tc299_m.group(1) if _tc299_m else None
        _ok299 = isinstance(_tc299, str) and _tc299 in _VALID_TWITTER_CARDS299
        check(
            _ok299,
            f"Check 299: twitter:card={_tc299!r} is valid card type",
            (f"Check 299: twitter:card={_tc299!r} not in {sorted(_VALID_TWITTER_CARDS299)!r} — "
             "Twitter が link-preview default fallback。spec-valid 値に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 299: index.html present",
              "Check 299: index.html が無い", blocking=True)

    # ── 300. og:image:alt contains canonical entity + role markers (BLOCKING) ─────
    # index.html `<meta property="og:image:alt">` content が "横井雄太" AND "AI-Driven PM"
    # 両 marker を含むことを BLOCKING 強制。Check 20 (presence) の content-value 軸版。
    _idx300 = ROOT / "index.html"
    if _idx300.exists():
        _isrc300 = _idx300.read_text(encoding="utf-8")
        _alt300_m = re.search(
            r'<meta\s+property=["\']og:image:alt["\']\s+content=["\']([^"\']+)["\']', _isrc300
        )
        _alt300 = _alt300_m.group(1) if _alt300_m else None
        _required300 = ["横井雄太", "AI-Driven PM"]
        _missing300 = []
        if isinstance(_alt300, str):
            _missing300 = [m for m in _required300 if m not in _alt300]
        else:
            _missing300 = ["og:image:alt 欠落"]
        _ok300 = not _missing300
        check(
            _ok300,
            f"Check 300: og:image:alt content={_alt300!r} contains 両 canonical marker",
            (f"Check 300: 欠落 marker: {_missing300!r} — accessibility alt-text が entity "
             "attribution / role signal を失う。両 marker を alt 内に含めよ"),
            blocking=True,
        )
    else:
        check(False, "Check 300: index.html present",
              "Check 300: index.html が無い", blocking=True)

    # ── 301. <link rel=preconnect> for Google Fonts hosts (BLOCKING) ──────────────
    # index.html に `<link rel=preconnect href=https://fonts.googleapis.com>` AND
    # `<link rel=preconnect href=https://fonts.gstatic.com>` 両方が存在することを
    # BLOCKING 強制。CWV LCP / font waterfall 最適化のため。Check 73a の preconnect 軸版。
    _idx301 = ROOT / "index.html"
    if _idx301.exists():
        _isrc301 = _idx301.read_text(encoding="utf-8")
        _required_preconn301 = ["https://fonts.googleapis.com", "https://fonts.gstatic.com"]
        _missing301 = []
        for _href in _required_preconn301:
            _pat = re.compile(
                r'<link\s+rel=["\']preconnect["\'][^>]*href=["\']' + re.escape(_href) + r'["\']'
            )
            if not _pat.search(_isrc301):
                _missing301.append(_href)
        _ok301 = not _missing301
        check(
            _ok301,
            "Check 301: index.html has <link rel=preconnect> for both fonts.googleapis.com and fonts.gstatic.com",
            (f"Check 301: 欠落 preconnect href: {_missing301!r} — CWV LCP / font "
             "waterfall 劣化。両 preconnect link を復元"),
            blocking=True,
        )
    else:
        check(False, "Check 301: index.html present",
              "Check 301: index.html が無い", blocking=True)

    # ── 302. <body data-canonical> == <link rel=canonical> href (BLOCKING) ────────
    # index.html の <body> tag data-canonical 属性が <link rel=canonical> href と
    # strict 一致することを BLOCKING 強制。Check 149 の body attribute 軸版。
    _idx302 = ROOT / "index.html"
    if _idx302.exists():
        _isrc302 = _idx302.read_text(encoding="utf-8")
        _canon302_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc302
        )
        _canon302 = _canon302_m.group(1) if _canon302_m else None
        _body_canon302_m = re.search(
            r'<body\s+[^>]*data-canonical=["\']([^"\']+)["\']', _isrc302
        )
        _body_canon302 = _body_canon302_m.group(1) if _body_canon302_m else None
        _ok302 = (
            isinstance(_canon302, str)
            and isinstance(_body_canon302, str)
            and _canon302 == _body_canon302
        )
        check(
            _ok302,
            f"Check 302: <body data-canonical>={_body_canon302!r} == <link rel=canonical>={_canon302!r}",
            (f"Check 302: canonical drift: body-attr={_body_canon302!r} / link-rel={_canon302!r} "
             "— JS reader hydration が canonical から drift。両者を strict 一致へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 302: index.html present",
              "Check 302: index.html が無い", blocking=True)
