"""
checks_seo_meta.py — AIO/SEO meta + canonical URL + resource-resolution coherence checks
(extracted from check_repository_consistency.py — check.py split track・category "SEO meta coherence").

Contiguous cluster (149-166 minus the already-split 152) of Checks 149/150/151/153/154/155/156/157/
158/159/160/161/162/163/164/165/166 enforcing SEO/AIO meta and resource coherence: canonical-URL
three-way (149) / og:url (150) / e2e title uniqueness (151) / og·twitter image origin (153) /
description 3-way (154) / og·twitter title (155) / og:type enum (156) / mobile-PWA meta (157) /
Google-Fonts preconnect (158) / JSON-LD @context (159) / sw.js hardcoded paths (160) / robots.txt
baseline (161) / .gitignore baseline (162) / icon href resolve (163) / og·twitter image resolve (164)
/ api-catalog (165) / sitemap loc prefix (166). Each Check reads its own target files directly via
Path.read_text() / the ctx read helper; no global-content or cross-section var coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  149. Canonical URL three-way coherence (`<link rel="canonical">` ↔ aio-manifest.json
       entity.canonical_url ↔ main.js SITE_CONFIG.CANONICAL_URL): the canonical URL string must be
       byte-identical across all three primary declaration surfaces. Drift is SILENT but corrupts
       AIO entity identity — AI crawlers see conflicting canonical signals from different surfaces
       and cannot anchor the entity to one URL (the entire AIO surface is built on this single
       string being the authoritative identifier). Check 62 already enforces manifest ↔ llms-full.txt
       coherence; this Check closes the third edge (the link rel=canonical + the runtime SITE_CONFIG
       used by dynamic JSON-LD injection). Trailing slashes and origin must match exactly. (BLOCKING)
  150. og:url ↔ canonical URL coherence: the index.html `<meta property="og:url">` content must be
       byte-identical to the `<link rel="canonical">` href. Drift is SILENT — the OG/social card
       preview (LinkedIn / Slack unfurl / Twitter / Discord) shows a different URL than the
       canonical link, and AI/social crawlers may resolve to a different entity URL than the
       authoritative one. Extends the Check 149 canonical-URL invariant to the social/OG surface,
       which is the most-shared external mention of the site. (BLOCKING)
  151. e2e test() title uniqueness: every `test('...', ...)` title across all e2e/*.spec.js must be
       unique. Duplicate titles are SILENT in some Playwright reporters (the second run silently
       overrides the first's record) and always reduce diagnostic clarity — a class of
       vacuous-test-pair where one test's failure may be misattributed or masked by the other's
       pass. This Check parses all `test('...'` direct invocations and asserts the title multiset
       has no duplicates. (BLOCKING)
  153. og:image / twitter:image origin uses canonical URL prefix: every index.html `<meta
       property="og:image">` and `<meta name="twitter:image">` content URL must start with the
       `<link rel="canonical">` href (sharing the same origin + path prefix). Drift is SILENT — the
       social/OG card preview shows an image from a different origin, breaking the entity-asset
       coupling and possibly serving a stale or third-party image. Extends the Check 149/150
       canonical-URL invariant to the image surface of OG/Twitter cards (the visual portion of any
       external mention of the site). Both meta tags must be present; either drifting from the
       canonical prefix fails the Check. (BLOCKING)
  154. og:description ↔ twitter:description coherence + 3-way presence: the index.html `<meta
       property="og:description">` and `<meta name="twitter:description">` content must be
       byte-identical (both are card-preview descriptions with the same length budget), and
       `<meta name="description">` (the longer SERP-targeted description) must also be present.
       Drift between og: and twitter: descriptions is SILENT — different social/AI crawlers show
       different card text for the same page (LinkedIn/Slack vs Twitter), splitting the entity
       narrative. The `<meta name="description">` is intentionally a different (longer) string for
       SERP/AI crawler ingestion, so this Check does NOT require it to match og/twitter; only that
       it exists (vacuous-guard against silent removal). (BLOCKING)
  155. og:title ↔ twitter:title coherence: the index.html `<meta property="og:title">` and
       `<meta name="twitter:title">` content must be byte-identical. Both are card-preview titles
       with the same length budget; drift is SILENT — LinkedIn/Slack/OG consumers see one title
       while Twitter shows another, splitting the entity headline across social surfaces. Sibling
       of Check 154 (description coherence) for the title axis. The `<title>` tag is intentionally
       allowed to differ (different length budget for SERP vs cards), so this Check restricts to
       og/twitter pair only. Both meta tags must be present and equal. (BLOCKING)
  156. og:type valid enumeration + og:site_name presence: the index.html `<meta property="og:type">`
       must have a content value in the small valid OG type enumeration used by this site
       ('website' or 'article' — the only types referenced by meta-management.js's dynamic injection
       per SITE_CONFIG.ARTICLE_ROUTES), and `<meta property="og:site_name">` must be present (any
       non-empty value). Silent removal of og:site_name strips the site identifier from card
       previews (entity context loss); an invalid og:type value (typo / removed enumeration member)
       leaves social crawlers fallback to a generic preview, losing article-vs-page disambiguation.
       This Check is a presence + enumeration sanity gate, complementing the dynamic-injection
       coverage of Check 148 (ARTICLE_ROUTES ⊆ PAGE_META). (BLOCKING)
  157. Mobile / PWA baseline meta presence: the index.html `<head>` must declare a non-negotiable
       baseline of platform meta tags — `<meta charset="utf-8">`, `<meta name="viewport">`,
       `<meta name="theme-color">` (any media variant), `<link rel="icon">`, and `<link
       rel="apple-touch-icon">`. Silent removal causes regressions that mostly do not break the
       behavior e2e: missing viewport → mobile zoom is broken (no `width=device-width` scale=1),
       missing icon → browser tab and bookmark show a generic globe, missing apple-touch-icon →
       iOS Add-to-Home-Screen uses a downscaled screenshot, missing theme-color → mobile address
       bar / OS card chrome stays default. Each of these is shipped today; this Check enforces
       presence-only (content correctness is out of scope) as a vacuous-removal guard. (BLOCKING)
  158. Google Fonts preconnect / dns-prefetch presence (CWV first-paint guard): index.html must
       keep `<link rel="preconnect" href="https://fonts.googleapis.com">`, `<link rel="preconnect"
       href="https://fonts.gstatic.com">`, and `<link rel="dns-prefetch" href="https://
       fonts.googleapis.com">`. The site loads Google Fonts CSS + binary; these resource hints save
       ~100-200ms of DNS+TLS+handshake latency on first paint. Silent removal regresses LCP/FCP
       without any console error or behavior-test signal, and the regression is hard to bisect
       later (the missing hints are just slow, not broken). Three-marker presence check; any one
       missing fails. (BLOCKING)
  159. JSON-LD `@context` cross-surface coherence: every `"@context"` (or `'@context'`) value in
       JSON-LD scattered across index.html (static blocks) + main.js + js/meta-management.js
       (dynamic injections) must be the single canonical value `https://schema.org`. Drift to a
       trailing slash, an http:// variant, or a different schema vocabulary is SILENT — JSON
       parses, the block ships, but AI/SEO crawlers fail to recognize the schema and the entire
       structured-data signal collapses to "unknown vocabulary". Collected into a single set with
       cardinality 1 expected (the universally accepted canonical URL). (BLOCKING)
  160. sw.js hardcoded paths share the canonical URL pathname: every absolute path string in sw.js
       that starts with a `/<segment>/` form (e.g. the AIO_FILES list) must use the same first
       path-segment as the `<link rel="canonical">` href's pathname (e.g. `/portfolio/`). Drift is
       SILENT — if the GitHub Pages project is renamed (or the canonical URL's path changes), the
       SW continues to register but its hardcoded paths no longer match any incoming request URLs,
       so SW-cached AIO file requests silently miss the SW interception layer. Skips literal `/`
       (root). (BLOCKING)
  161. robots.txt User-agent: * baseline presence: robots.txt must declare a `User-agent: *` block
       and that block must permit crawling (no `Disallow: /` directive in it). Silent regression to
       `Disallow: /` would deindex the entire site from all generic crawlers (AI + search) — a
       category-collapse for an AIO-first site that the behavior e2e cannot detect (it runs against
       localhost, not the deployed crawl policy). This Check parses the `User-agent: *` section
       (up to the next `User-agent:` line) and asserts no full-site disallow is present. (BLOCKING)
  162. `.gitignore` baseline ignore-rules for CI/build artifacts: `.gitignore` must declare ignore
       rules for `node_modules/`, `__pycache__/`, `/test-results/`, `/playwright-report/`, and
       `/blob-report/`. Silent removal would allow accidental `git add <file>` of CI artifacts and
       node_modules (hundreds of MB) to land in the repo. Check 37 catches the artifact files
       themselves after they're tracked, but this Check protects the gate upstream so they never
       arrive in the staging area. (BLOCKING)
  163. `<link rel="icon">` / `<link rel="apple-touch-icon">` href resolves to an actual file:
       every non-data: href in `<link rel="icon">` and `<link rel="apple-touch-icon">` tags in
       index.html must resolve to an existing repo file (the canonical URL pathname is stripped to
       map href to repo-relative path). A dangling href ships a broken icon and is SILENT: the
       browser falls back to a default globe icon and the apple-touch-icon path returns 404 on iOS
       Add-to-Home (which then uses a downscaled site screenshot instead of the curated icon).
       data: URI hrefs (inline SVG fallbacks) are exempt. (BLOCKING)
  164. og:image / twitter:image content URL resolves to an actual file: the index.html
       `<meta property="og:image">` and `<meta name="twitter:image">` content URLs must resolve to
       existing repo files (after stripping the canonical URL prefix to get the local path). A
       dangling image is SILENT — social/OG card previews show a broken image with no console
       error or behavior-test signal. Extends Check 153 (canonical URL prefix) and Check 163
       (icon href resolves) to the social card image surface. (BLOCKING)
  165. `.well-known/api-catalog` JSON + anchor canonical origin: `.well-known/api-catalog` must be
       valid JSON with a `linkset` array containing at least one entry, and the `anchor` URL of the
       first linkset entry must start with the canonical URL (from `<link rel="canonical">`). A
       drift / malformed file silently breaks AI crawler discovery of authoritative API endpoints
       (the catalog is the entry point that points to mcp.json / agent-skills / aio-manifest /
       llms-full). (BLOCKING)
  166. sitemap.xml `<loc>` URLs all start with canonical URL prefix: every `<loc>` URL in
       sitemap.xml must start with the `<link rel="canonical">` href value (full prefix, not just
       origin). Check 63 enforces origin alignment only; this Check tightens to the full canonical
       URL (origin + base path). Drift to a sibling project path (e.g. `/portfolio2/about`) is
       SILENT — sitemap crawlers index URLs that 404 on the deployed site. (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract

    # ── 149. Canonical URL three-way coherence (BLOCKING) ──────────────────────────
    # canonical URL は AIO entity identifier の単一源。3 surface (index.html
    # <link rel=canonical> href / aio-manifest.json entity.canonical_url / main.js
    # SITE_CONFIG.CANONICAL_URL) が drift すると AI crawler が複数の canonical signal を
    # 見て entity を一つの URL に anchor できず AIO 全体が崩れる。Check 62 が manifest ↔
    # llms-full.txt 整合を強制済なので、本 Check は残る 2 edge (link[rel=canonical] と
    # SITE_CONFIG) を manifest と byte-identical に固定する。trailing slash / origin も完全一致必須。
    _idx149 = ROOT / "index.html"
    _man149 = ROOT / ".well-known" / "aio-manifest.json"
    _main149 = ROOT / "main.js"
    if _idx149.exists() and _man149.exists() and _main149.exists():
        _isrc149 = _idx149.read_text(encoding="utf-8")
        _msrc149 = _main149.read_text(encoding="utf-8")
        try:
            _mdata149 = json.loads(_man149.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mdata149 = {}
        _link149_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc149
        )
        _link149 = _link149_m.group(1) if _link149_m else None
        _manifest149 = _mdata149.get("entity", {}).get("canonical_url")
        _sc149_m = re.search(r"CANONICAL_URL:\s*['\"]([^'\"]+)['\"]", _msrc149)
        _site_config149 = _sc149_m.group(1) if _sc149_m else None
        _all_extracted149 = all([_link149, _manifest149, _site_config149])
        _all_match149 = _all_extracted149 and (_link149 == _manifest149 == _site_config149)
        check(
            _all_match149,
            f"Check 149: canonical URL 3-way 一致 ({_link149!r})",
            (f"Check 149: canonical URL drift: link[rel=canonical]={_link149!r} / "
             f"aio-manifest.entity.canonical_url={_manifest149!r} / "
             f"main.js SITE_CONFIG.CANONICAL_URL={_site_config149!r}. "
             "AI crawler が一つの entity を複数 canonical signal で見て identity が崩れる。"
             "3 surface を完全一致させよ (trailing slash / origin も含めて byte-identical)"
             if _all_extracted149 else
             "Check 149: 3 surface のいずれかから canonical URL を抽出できない "
             f"(link={_link149} / manifest={_manifest149} / SITE_CONFIG={_site_config149})"),
            blocking=True,
        )
    else:
        check(False, "Check 149: index.html + aio-manifest.json + main.js present",
              "Check 149: canonical URL 検証に必要な 3 source のいずれかが無い", blocking=True)

    # ── 150. og:url ↔ canonical URL coherence (BLOCKING) ──────────────────────────
    # index.html `<meta property="og:url">` content と `<link rel=canonical>` href が
    # byte-identical であることを BLOCKING 強制する。drift は SILENT — OG/social card
    # preview (LinkedIn / Slack unfurl / Twitter / Discord) が canonical link と別の URL
    # を提示し AI/social crawler の entity 識別が崩れる。Check 149 の canonical-URL
    # invariant を最も外部 mention の多い OG surface に拡張する。
    _idx150 = ROOT / "index.html"
    if _idx150.exists():
        _isrc150 = _idx150.read_text(encoding="utf-8")
        _og150 = re.search(
            r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']+)["\']', _isrc150
        )
        _link150 = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc150
        )
        _og150v = _og150.group(1) if _og150 else None
        _link150v = _link150.group(1) if _link150 else None
        check(
            _og150v is not None and _link150v is not None and _og150v == _link150v,
            f"Check 150: og:url == <link rel=canonical> ({_og150v!r})",
            (f"Check 150: og:url ({_og150v!r}) != canonical ({_link150v!r}) — "
             "OG card preview と canonical link が別 URL を提示し AI/social crawler の "
             "entity 識別に drift。index.html の og:url と <link rel=canonical> を一致させよ "
             "(Check 149 で manifest + SITE_CONFIG とも byte-identical を強制済)"
             if _og150v and _link150v else
             "Check 150: og:url もしくは <link rel=canonical> を抽出できない (index.html を確認せよ)"),
            blocking=True,
        )
    else:
        check(False, "Check 150: index.html present",
              "Check 150: index.html が無い — og:url canonical 整合を検証できない", blocking=True)

    # ── 151. e2e test() title uniqueness (BLOCKING) ───────────────────────────────
    # e2e/*.spec.js 全体の `test('...', ...)` title が一意であることを BLOCKING
    # 強制する。重複 title は Playwright reporter によっては silent に上書き
    # (同名の二件目が記録される / report 上で結果区別がつかない) し、vacuous-test-pair
    # の class を生む — 片方の fail が他方の pass で masked されたり、誰がどちらの
    # 期待を表しているか読めない。test() 直接呼び出しのみ対象 (test.skip/.fixme/.describe
    # は対象外 — title 衝突の影響範囲が異なる)。e2e 空 / 重複 >0 なら fail。
    # spec テーマ別分割 (2026-07-07) 後は e2e/*.spec.js 全体で title 一意性を強制する
    # (Playwright は title で結果を報告するため、ファイルを跨いだ重複も vacuous-pair を生む)。
    _specs151 = sorted((ROOT / "e2e").glob("*.spec.js"))
    if _specs151:
        _titles151 = []
        for _sp151 in _specs151:
            _titles151 += re.findall(r"^\s*test\(\s*['\"]([^'\"]+)['\"]",
                                     _sp151.read_text(encoding="utf-8"), re.MULTILINE)
        _seen151: dict[str, int] = {}
        for _t151 in _titles151:
            _seen151[_t151] = _seen151.get(_t151, 0) + 1
        _dupes151 = sorted(t for t, c in _seen151.items() if c > 1)
        check(
            bool(_titles151) and not _dupes151,
            f"Check 151: e2e {len(_titles151)} 件の test() title すべて一意 ({len(_specs151)} spec 横断)",
            (f"Check 151: 重複 e2e test title: {_dupes151} — Playwright reporter で "
             "silent 上書き / 同名で結果区別不能になり vacuous-test-pair を生む。"
             "e2e/*.spec.js で title を一意化せよ"
             if _titles151 else
             "Check 151: e2e/*.spec.js に test() が一つも見つからない (vacuous-fail)"),
            blocking=True,
        )
    else:
        check(False, "Check 151: e2e/*.spec.js present",
              "Check 151: e2e/*.spec.js が無い — test title 一意性を検証できない",
              blocking=True)

    # ── 153. og:image / twitter:image origin uses canonical URL prefix (BLOCKING) ──
    # index.html の `<meta property="og:image">` と `<meta name="twitter:image">` content
    # URL が `<link rel=canonical>` href を prefix として持つことを BLOCKING 強制する。
    # drift は SILENT — social/OG card preview が別 origin の image を提示し
    # entity-asset coupling を破壊、stale や third-party image を見せうる。
    # Check 149/150 の canonical-URL invariant を image surface (OG/Twitter card の
    # 視覚部分) に拡張する。両 meta が必須で片方でも canonical prefix から外れたら fail。
    _idx153 = ROOT / "index.html"
    if _idx153.exists():
        _isrc153 = _idx153.read_text(encoding="utf-8")
        _link153_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc153
        )
        _canon153 = _link153_m.group(1) if _link153_m else None
        _og_img153_m = re.search(
            r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', _isrc153
        )
        _tw_img153_m = re.search(
            r'<meta\s+name=["\']twitter:image["\']\s+content=["\']([^"\']+)["\']', _isrc153
        )
        _og_img153 = _og_img153_m.group(1) if _og_img153_m else None
        _tw_img153 = _tw_img153_m.group(1) if _tw_img153_m else None
        _drift153: list[str] = []
        if _canon153:
            if _og_img153 and not _og_img153.startswith(_canon153):
                _drift153.append(f"og:image={_og_img153!r}")
            if _tw_img153 and not _tw_img153.startswith(_canon153):
                _drift153.append(f"twitter:image={_tw_img153!r}")
        _ok153 = (
            _canon153 is not None
            and _og_img153 is not None
            and _tw_img153 is not None
            and not _drift153
        )
        check(
            _ok153,
            f"Check 153: og:image / twitter:image は canonical ({_canon153!r}) を prefix",
            (f"Check 153: 画像 URL canonical prefix drift: canonical={_canon153!r} / {_drift153} "
             "— OG/Twitter card preview が別 origin の image を見せ entity-asset coupling が崩れる。"
             "index.html の og:image / twitter:image を canonical URL prefix で始まる絶対 URL へ統一せよ"
             if _canon153 and _og_img153 and _tw_img153 else
             f"Check 153: canonical / og:image / twitter:image を抽出できない "
             f"(canonical={_canon153} / og:image={_og_img153} / twitter:image={_tw_img153})"),
            blocking=True,
        )
    else:
        check(False, "Check 153: index.html present",
              "Check 153: index.html が無い — image URL canonical 整合を検証できない",
              blocking=True)

    # ── 154. description 3-way presence + og/twitter coherence (BLOCKING) ─────────
    # index.html の og:description と twitter:description content が byte-identical
    # (card preview の同尺 description)、かつ <meta name="description"> も presence
    # 必須を BLOCKING 強制する。drift は SILENT — LinkedIn/Slack 等 OG consumer と
    # Twitter 等 twitter: consumer が同じ page を別 card text で見せ entity narrative
    # が split する。<meta name="description"> は SERP/AI crawler 向けに intentionally
    # 長文ゆえ og/twitter と一致は強制しない (presence のみ vacuous-guard)。
    _idx154 = ROOT / "index.html"
    if _idx154.exists():
        _isrc154 = _idx154.read_text(encoding="utf-8")
        _meta154_m = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', _isrc154
        )
        _og154_m = re.search(
            r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)["\']', _isrc154
        )
        _tw154_m = re.search(
            r'<meta\s+name=["\']twitter:description["\']\s+content=["\']([^"\']+)["\']', _isrc154
        )
        _meta154 = _meta154_m.group(1) if _meta154_m else None
        _og154 = _og154_m.group(1) if _og154_m else None
        _tw154 = _tw154_m.group(1) if _tw154_m else None
        _all_present154 = _meta154 and _og154 and _tw154
        _og_tw_match154 = _og154 == _tw154 if (_og154 and _tw154) else False
        check(
            bool(_all_present154) and _og_tw_match154,
            f"Check 154: description 3 surface presence ✓ + og==twitter byte-identical ✓",
            (f"Check 154: description drift / 欠落: meta-description {'OK' if _meta154 else '欠落'} / "
             f"og:description {'OK' if _og154 else '欠落'} / twitter:description "
             f"{'OK' if _tw154 else '欠落'} / og==twitter: {_og_tw_match154}。"
             "og:description と twitter:description は card preview 同尺で byte-identical 必須 "
             "(LinkedIn/Slack vs Twitter で別 card text を見せると entity narrative が split)。"
             "<meta name=\"description\"> は SERP 向けに別文字列でよいが presence は必須"
             if _all_present154 else
             f"Check 154: 必須 meta description が欠落 "
             f"(name=description={_meta154 is not None} / og:description={_og154 is not None} / "
             f"twitter:description={_tw154 is not None})"),
            blocking=True,
        )
    else:
        check(False, "Check 154: index.html present",
              "Check 154: index.html が無い — description 整合を検証できない",
              blocking=True)

    # ── 155. og:title ↔ twitter:title byte-identical (BLOCKING) ────────────────────
    # index.html の og:title と twitter:title content が byte-identical であることを
    # BLOCKING 強制する。両者は card preview の同尺 title で drift は SILENT —
    # LinkedIn/Slack/OG consumer と Twitter で別 headline を見せ entity の見え方が
    # split する。Check 154 (description coherence) の title 軸兄弟。`<title>` tag は
    # SERP vs card で intentionally 異なる尺ゆえ scope から外し og/twitter の pair のみ
    # 強制する。両 meta presence + byte-identical 必須。
    _idx155 = ROOT / "index.html"
    if _idx155.exists():
        _isrc155 = _idx155.read_text(encoding="utf-8")
        _og155_m = re.search(
            r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', _isrc155
        )
        _tw155_m = re.search(
            r'<meta\s+name=["\']twitter:title["\']\s+content=["\']([^"\']+)["\']', _isrc155
        )
        _og155 = _og155_m.group(1) if _og155_m else None
        _tw155 = _tw155_m.group(1) if _tw155_m else None
        _ok155 = (
            _og155 is not None and _tw155 is not None and _og155 == _tw155
        )
        check(
            _ok155,
            f"Check 155: og:title == twitter:title byte-identical ({_og155!r})",
            (f"Check 155: title drift: og:title={_og155!r} / twitter:title={_tw155!r} — "
             "LinkedIn/Slack OG consumer と Twitter で別 headline を見せ entity の見え方が split。"
             "index.html の og:title と twitter:title content を byte-identical に統一せよ"
             if _og155 and _tw155 else
             f"Check 155: og:title もしくは twitter:title meta が欠落 "
             f"(og={_og155 is not None} / twitter={_tw155 is not None})"),
            blocking=True,
        )
    else:
        check(False, "Check 155: index.html present",
              "Check 155: index.html が無い — title 整合を検証できない",
              blocking=True)

    # ── 156. og:type valid enumeration + og:site_name presence (BLOCKING) ─────────
    # index.html の og:type content が valid OG type enumeration ('website' or
    # 'article' — meta-management.js の dynamic injection / SITE_CONFIG.ARTICLE_ROUTES
    # で扱う唯一の type 集合) であり、og:site_name meta が presence であることを
    # BLOCKING 強制する。og:site_name 欠落は card preview から site 識別子を奪い
    # entity context が失われ、og:type の invalid 値 (typo / 列挙外) は social
    # crawler が generic preview にフォールバックし article-vs-page 区別が失われる。
    # presence + enumeration sanity の二段。Check 148 (ARTICLE_ROUTES ⊆ PAGE_META)
    # の dynamic injection 軸を補完する static surface 検証。
    _idx156 = ROOT / "index.html"
    if _idx156.exists():
        _isrc156 = _idx156.read_text(encoding="utf-8")
        _ogt156_m = re.search(
            r'<meta\s+property=["\']og:type["\']\s+content=["\']([^"\']+)["\']', _isrc156
        )
        _ogs156_m = re.search(
            r'<meta\s+property=["\']og:site_name["\']\s+content=["\']([^"\']+)["\']', _isrc156
        )
        _ogt156 = _ogt156_m.group(1) if _ogt156_m else None
        _ogs156 = _ogs156_m.group(1) if _ogs156_m else None
        _valid_types156 = {"website", "article"}
        _ok156 = (
            _ogt156 in _valid_types156
            and _ogs156 is not None
            and _ogs156.strip() != ""
        )
        check(
            _ok156,
            f"Check 156: og:type={_ogt156!r} ∈ {_valid_types156} + og:site_name 存在 ({_ogs156!r})",
            (f"Check 156: og 整合性 fail: og:type={_ogt156!r} (valid={_valid_types156}) / "
             f"og:site_name={_ogs156!r}. og:type は 'website'/'article' のいずれか・"
             "og:site_name は非空文字列 (card preview の site 識別子) 必須。"
             "index.html の <meta property=og:type> / <meta property=og:site_name> を修正せよ"
             if (_ogt156 is not None or _ogs156 is not None) else
             "Check 156: og:type / og:site_name meta を抽出できない"),
            blocking=True,
        )
    else:
        check(False, "Check 156: index.html present",
              "Check 156: index.html が無い — og:type/og:site_name 整合を検証できない",
              blocking=True)

    # ── 157. Mobile / PWA baseline meta presence (BLOCKING) ────────────────────────
    # index.html の <head> に非交渉 baseline meta が必ず存在することを BLOCKING 強制
    # する: charset / viewport / theme-color / icon / apple-touch-icon。これらの
    # silent 除去は behavior e2e にほぼ非検出だが、viewport 欠落=モバイルズーム破綻 /
    # icon 欠落=タブが generic globe / apple-touch-icon 欠落=iOS ホーム追加が縮小
    # screenshot / theme-color 欠落=モバイルアドレスバーがデフォルト色、と劣化する。
    # 全 5 marker が現状 shipped 済ゆえ presence-only (内容は scope 外) の
    # vacuous-removal guard。
    _idx157 = ROOT / "index.html"
    if _idx157.exists():
        _isrc157 = _idx157.read_text(encoding="utf-8")
        _markers157 = {
            "<meta charset>": re.search(r'<meta\s+charset\s*=', _isrc157, re.IGNORECASE) is not None,
            "<meta name=viewport>": re.search(
                r'<meta\s+name=["\']viewport["\']', _isrc157, re.IGNORECASE
            ) is not None,
            "<meta name=theme-color>": re.search(
                r'<meta\s+name=["\']theme-color["\']', _isrc157, re.IGNORECASE
            ) is not None,
            "<link rel=icon>": re.search(
                r'<link\s+rel=["\']icon["\']', _isrc157, re.IGNORECASE
            ) is not None,
            "<link rel=apple-touch-icon>": re.search(
                r'<link\s+rel=["\']apple-touch-icon["\']', _isrc157, re.IGNORECASE
            ) is not None,
        }
        _missing157 = sorted(k for k, present in _markers157.items() if not present)
        check(
            not _missing157,
            f"Check 157: mobile/PWA baseline meta {len(_markers157)} 件すべて presence "
            f"({sorted(_markers157.keys())})",
            f"Check 157: mobile/PWA baseline meta 欠落: {_missing157} — silent 削除で "
            "モバイル/PWA 体験が劣化する (viewport=zoom 破綻 / icon=タブ globe / "
            "apple-touch-icon=iOS 縮小 screenshot / theme-color=アドレスバー default / "
            "charset=文字化けリスク)。index.html <head> に該当 meta を再追加せよ",
            blocking=True,
        )
    else:
        check(False, "Check 157: index.html present",
              "Check 157: index.html が無い — mobile/PWA meta presence を検証できない",
              blocking=True)

    # ── 158. Google Fonts preconnect / dns-prefetch presence (BLOCKING) ────────────
    # CWV first-paint guard: index.html が Google Fonts への preconnect 2 件
    # (fonts.googleapis.com + fonts.gstatic.com) と dns-prefetch 1 件
    # (fonts.googleapis.com) を保持することを BLOCKING 強制する。silent 除去は LCP/FCP
    # を ~100-200ms 劣化させるが console error も behavior-test signal も出ず、後で
    # bisect しにくい (壊れていない・ただ遅い)。
    _idx158 = ROOT / "index.html"
    if _idx158.exists():
        _isrc158 = _idx158.read_text(encoding="utf-8")
        _hints158 = {
            "preconnect fonts.googleapis.com": re.search(
                r'<link\s+rel=["\']preconnect["\']\s+href=["\']https://fonts\.googleapis\.com["\']',
                _isrc158,
            ) is not None,
            "preconnect fonts.gstatic.com": re.search(
                r'<link\s+rel=["\']preconnect["\']\s+href=["\']https://fonts\.gstatic\.com["\']',
                _isrc158,
            ) is not None,
            "dns-prefetch fonts.googleapis.com": re.search(
                r'<link\s+rel=["\']dns-prefetch["\']\s+href=["\']https://fonts\.googleapis\.com["\']',
                _isrc158,
            ) is not None,
        }
        _missing158 = sorted(k for k, present in _hints158.items() if not present)
        check(
            not _missing158,
            f"Check 158: Google Fonts resource hint 3 件すべて presence",
            f"Check 158: Google Fonts resource hint 欠落: {_missing158} — LCP/FCP を "
            "~100-200ms silent 劣化させる (DNS+TLS+handshake)。index.html <head> に "
            "preconnect/dns-prefetch を復元せよ",
            blocking=True,
        )
    else:
        check(False, "Check 158: index.html present",
              "Check 158: index.html が無い — Google Fonts hint presence を検証できない",
              blocking=True)

    # ── 159. JSON-LD @context cross-surface coherence (BLOCKING) ───────────────────
    # 全 JSON-LD `@context` 値 (index.html 静的 ∪ main.js 動的 ∪ js/meta-management.js
    # 動的) が canonical 値 'https://schema.org' 一つに揃うことを BLOCKING 強制する。
    # drift (trailing slash / http: / 別 schema vocabulary) は SILENT — JSON 自体は
    # parse できるが AI/SEO crawler が schema を recognize できず structured-data signal
    # 全体が unknown vocabulary 扱いで崩壊する。全 surface から値を抽出し set
    # cardinality が 1 で且つ canonical 値であることを検証。
    _idx159 = ROOT / "index.html"
    _main159 = ROOT / "main.js"
    _meta159 = ROOT / "js" / "meta-management.js"
    if _idx159.exists() and _main159.exists() and _meta159.exists():
        _ctx159: set[str] = set()
        _count159 = 0
        for _p159 in [_idx159, _main159, _meta159]:
            _src159 = _p159.read_text(encoding="utf-8")
            for _v159 in re.findall(
                r"""['"]@context['"]\s*:\s*['"]([^'"]+)['"]""", _src159
            ):
                _ctx159.add(_v159)
                _count159 += 1
        _expected159 = "https://schema.org"
        _ok159 = _count159 > 0 and _ctx159 == {_expected159}
        check(
            _ok159,
            f"Check 159: JSON-LD @context {_count159} 件すべて canonical {_expected159!r}",
            (f"Check 159: @context drift: 観測値={_ctx159} (期待={_expected159!r}) — "
             "JSON-LD は parse できるが AI/SEO crawler が schema vocabulary を recognize できず "
             "structured-data signal 全体が unknown 扱いで崩壊する。"
             "index.html / main.js / js/meta-management.js の @context を 'https://schema.org' "
             "に統一せよ"
             if _count159 > 0 else
             "Check 159: JSON-LD @context が一件も見つからない (vacuous-fail)"),
            blocking=True,
        )
    else:
        check(False, "Check 159: index.html + main.js + js/meta-management.js present",
              "Check 159: JSON-LD @context coherence 検証に必要な 3 source のいずれかが無い",
              blocking=True)

    # ── 160. sw.js hardcoded paths share the canonical URL pathname (BLOCKING) ─────
    # sw.js が hardcode する `/<segment>/...` 形式の絶対パス (AIO_FILES 等) が、
    # index.html の <link rel=canonical> href の pathname と同じ first segment を
    # 使うことを BLOCKING 強制する。drift は SILENT — GitHub Pages の project rename
    # や canonical URL の path 変更で SW は登録され続けるが hardcoded paths が
    # incoming request URL と一致せず SW 介入層を silent に miss する。
    # 文字列リテラル中の `'/<segment>/...'` (quoted) のみ対象。literal '/' (root) は skip。
    _sw160 = ROOT / "sw.js"
    _idx160 = ROOT / "index.html"
    if _sw160.exists() and _idx160.exists():
        _isrc160 = _idx160.read_text(encoding="utf-8")
        _swsrc160 = _sw160.read_text(encoding="utf-8")
        _link160 = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc160
        )
        _canon_path160 = None
        if _link160:
            # parse pathname (e.g. https://yutapr0117-design.github.io/portfolio/ -> /portfolio/)
            from urllib.parse import urlparse as _urlparse160
            _canon_path160 = _urlparse160(_link160.group(1)).path
        # extract quoted absolute paths in sw.js: '/foo/...' or "/foo/..."
        _hardcoded160: list[str] = re.findall(r"""['"](/[^\s'"]+)['"]""", _swsrc160)
        # filter to only those starting with a segment (skip bare '/')
        _segment_paths160 = [p for p in _hardcoded160 if re.match(r"^/[A-Za-z][\w-]*/", p)]
        _drift160: list[str] = []
        if _canon_path160 and _canon_path160 != "/":
            for _p160 in _segment_paths160:
                if not _p160.startswith(_canon_path160):
                    _drift160.append(_p160)
        _ok160 = (
            _canon_path160 is not None
            and len(_segment_paths160) > 0
            and not _drift160
        )
        check(
            _ok160,
            f"Check 160: sw.js hardcoded paths ({len(_segment_paths160)} 件) all start with "
            f"canonical pathname {_canon_path160!r}",
            (f"Check 160: sw.js path drift: canonical pathname={_canon_path160!r} / "
             f"non-matching paths={_drift160}. canonical URL の pathname と一致しない hardcoded "
             "path は SW interception で incoming request と一致せず silent miss する。"
             "sw.js の path prefix を canonical URL pathname に揃えるか canonical URL を修正せよ"
             if _canon_path160 and _segment_paths160 else
             f"Check 160: canonical pathname もしくは sw.js segment paths が空 "
             f"(canonical={_canon_path160} / paths={len(_segment_paths160)})"),
            blocking=True,
        )
    else:
        check(False, "Check 160: sw.js + index.html present",
              "Check 160: sw.js もしくは index.html が無い — SW path coherence を検証できない",
              blocking=True)

    # ── 161. robots.txt User-agent: * baseline (no full-site disallow) (BLOCKING) ──
    # robots.txt が `User-agent: *` を持ち、そのブロック内に `Disallow: /` (全 site
    # 拒否) が無いことを BLOCKING 強制する。silent な `Disallow: /` 化は全 generic
    # crawler (AI + search) からの deindex を意味し AIO-first サイトには category-
    # collapse。behavior e2e は localhost に走るため crawl policy の劣化を検出できない。
    # `User-agent: *` の section (次の `User-agent:` 行まで) を抽出して full-site
    # disallow の存在を否定する。
    _rb161 = ROOT / "robots.txt"
    if _rb161.exists():
        _rbsrc161 = _rb161.read_text(encoding="utf-8")
        _lines161 = _rbsrc161.splitlines()
        _section161: list[str] = []
        _in_star161 = False
        for _ln161 in _lines161:
            _stripped161 = _ln161.strip()
            if _stripped161.startswith("#") or not _stripped161:
                continue
            if _stripped161.lower().startswith("user-agent:"):
                _agent161 = _stripped161.split(":", 1)[1].strip()
                _in_star161 = _agent161 == "*"
                continue
            if _in_star161:
                _section161.append(_stripped161)
        _has_star161 = _in_star161 or len(_section161) > 0 or any(
            ln.strip().lower() == "user-agent: *" for ln in _lines161
        )
        _full_disallow161 = any(
            _ln.lower().startswith("disallow:")
            and _ln.split(":", 1)[1].strip() == "/"
            for _ln in _section161
        )
        _ok161 = _has_star161 and not _full_disallow161
        check(
            _ok161,
            f"Check 161: robots.txt `User-agent: *` block presence + no full-site Disallow",
            (f"Check 161: robots.txt User-agent: * 不在 / 全 site Disallow 検出 "
             f"(presence={_has_star161} / full-disallow={_full_disallow161})。"
             "Disallow: / は AI + search crawler 双方からの全 site deindex を意味し AIO の "
             "全 discovery を category-collapse させる。robots.txt を修正し generic crawler を "
             "許容せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 161: robots.txt present",
              "Check 161: robots.txt が無い", blocking=True)

    # ── 162. .gitignore baseline ignore-rules for CI/build artifacts (BLOCKING) ────
    # .gitignore が node_modules / __pycache__ / test-results / playwright-report /
    # blob-report の 5 ルールすべて宣言することを BLOCKING 強制する。silent 削除は
    # 偶発的 `git add` で CI artifact (数百 MB 級) や node_modules を staging に
    # 載せうる。Check 37 は tracked 後の artifact ファイルを検出するが、本 Check は
    # その upstream の gate を守り artifact が staging 領域に着く前に防ぐ。
    _gi162 = ROOT / ".gitignore"
    if _gi162.exists():
        _gisrc162 = _gi162.read_text(encoding="utf-8")
        _required162 = [
            "node_modules/",
            "__pycache__/",
            "/test-results/",
            "/playwright-report/",
            "/blob-report/",
        ]
        _missing162 = [r for r in _required162 if r not in _gisrc162]
        check(
            not _missing162,
            f"Check 162: .gitignore baseline 5 rule 全て presence",
            f"Check 162: .gitignore baseline 欠落: {_missing162} — 偶発 `git add` で "
            "CI artifact や node_modules が staging に着く。.gitignore に該当 rule を復元せよ",
            blocking=True,
        )
    else:
        check(False, "Check 162: .gitignore present",
              "Check 162: .gitignore が無い", blocking=True)

    # ── 163. <link rel=icon> / apple-touch-icon href resolves to actual file (BLOCKING) ─
    # index.html の `<link rel="icon">` / `<link rel="apple-touch-icon">` の非 data:
    # href が実在 repo file に resolve することを BLOCKING 強制する。dangling は SILENT —
    # ブラウザは default globe icon に fall back し、apple-touch-icon は iOS Add-to-Home
    # で 404 →縮小 screenshot に fallback する。data: URI (inline SVG fallback) は exempt。
    # canonical URL pathname を href から strip して repo-relative path に map する。
    _idx163 = ROOT / "index.html"
    if _idx163.exists():
        _isrc163 = _idx163.read_text(encoding="utf-8")
        _link163 = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc163
        )
        _canon_path163 = "/"
        if _link163:
            from urllib.parse import urlparse as _urlparse163
            _canon_path163 = _urlparse163(_link163.group(1)).path or "/"
        _icon_hrefs163: list[tuple[str, str]] = []  # (rel, href)
        for _m163 in re.finditer(
            r'<link\s+rel=["\'](icon|apple-touch-icon)["\']\s+(?:type=["\'][^"\']*["\']\s+)?href=["\']([^"\']+)["\']',
            _isrc163,
        ):
            _icon_hrefs163.append((_m163.group(1), _m163.group(2)))
        _missing163: list[str] = []
        _checked163 = 0
        for _rel163, _href163 in _icon_hrefs163:
            if _href163.startswith("data:"):
                continue
            _checked163 += 1
            # strip canonical pathname prefix if matches (e.g. /portfolio/icon.svg -> icon.svg)
            _local163 = _href163
            if _canon_path163 != "/" and _href163.startswith(_canon_path163):
                _local163 = _href163[len(_canon_path163):]
            elif _href163.startswith("/"):
                _local163 = _href163.lstrip("/")
            _target163 = ROOT / _local163
            if not _target163.exists():
                _missing163.append(f"{_rel163}={_href163!r} -> {_local163} (not found)")
        check(
            bool(_icon_hrefs163) and _checked163 > 0 and not _missing163,
            f"Check 163: <link rel=icon|apple-touch-icon> href {_checked163} 件 "
            f"全て実 file に resolve ({len(_icon_hrefs163)} link 中 data: exempt)",
            (f"Check 163: dangling icon href: {_missing163} — ブラウザは default globe / "
             "iOS Add-to-Home は 縮小 screenshot に silent fallback する。"
             "index.html の <link rel=icon> / <link rel=apple-touch-icon> href を実在ファイルへ修正せよ"
             if _icon_hrefs163 else
             "Check 163: <link rel=icon> も <link rel=apple-touch-icon> も見つからない (vacuous)"),
            blocking=True,
        )
    else:
        check(False, "Check 163: index.html present",
              "Check 163: index.html が無い — icon href 解決を検証できない",
              blocking=True)

    # ── 164. og:image / twitter:image content URL resolves to actual file (BLOCKING) ─
    # index.html の og:image / twitter:image content URL が実 repo file に resolve
    # することを BLOCKING 強制する。dangling は SILENT — social/OG card preview が
    # broken image を提示し console error も behavior-test signal も出ない。
    # Check 153 (canonical URL prefix) と Check 163 (icon href resolves) を OG image
    # surface に拡張。canonical URL prefix を strip して repo-relative path に map。
    _idx164 = ROOT / "index.html"
    if _idx164.exists():
        _isrc164 = _idx164.read_text(encoding="utf-8")
        _link164 = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc164
        )
        _canon164 = _link164.group(1) if _link164 else None
        _img_metas164: list[tuple[str, str]] = []  # (name, content)
        _og164 = re.search(
            r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', _isrc164
        )
        if _og164:
            _img_metas164.append(("og:image", _og164.group(1)))
        _tw164 = re.search(
            r'<meta\s+name=["\']twitter:image["\']\s+content=["\']([^"\']+)["\']', _isrc164
        )
        if _tw164:
            _img_metas164.append(("twitter:image", _tw164.group(1)))
        _missing164: list[str] = []
        for _name164, _url164 in _img_metas164:
            _local164 = _url164
            if _canon164 and _url164.startswith(_canon164):
                _local164 = _url164[len(_canon164):]
            elif _url164.startswith("/"):
                _local164 = _url164.lstrip("/")
            _target164 = ROOT / _local164
            if not _target164.exists():
                _missing164.append(f"{_name164}={_url164!r} -> {_local164} (not found)")
        check(
            bool(_img_metas164) and not _missing164,
            f"Check 164: og:image / twitter:image {len(_img_metas164)} 件 全て実 file に resolve",
            (f"Check 164: dangling social image: {_missing164} — OG/Twitter card preview が "
             "broken image を見せ silent に entity-asset coupling 壊れる。"
             "index.html の og:image / twitter:image content を実在 file へ修正せよ"
             if _img_metas164 else
             "Check 164: og:image / twitter:image meta が見つからない (vacuous)"),
            blocking=True,
        )
    else:
        check(False, "Check 164: index.html present",
              "Check 164: index.html が無い — image URL 解決を検証できない",
              blocking=True)

    # ── 165. .well-known/api-catalog JSON + anchor canonical origin (BLOCKING) ─────
    # `.well-known/api-catalog` が valid JSON + linkset array (≥1 entry) + 最初 entry の
    # anchor URL が canonical URL prefix を持つことを BLOCKING 強制する。drift は
    # SILENT に AI crawler の API endpoint discovery を破壊する (catalog は mcp.json /
    # agent-skills / aio-manifest / llms-full への entry-point pointer)。
    _ac165 = ROOT / ".well-known" / "api-catalog"
    _idx165 = ROOT / "index.html"
    if _ac165.exists() and _idx165.exists():
        _isrc165 = _idx165.read_text(encoding="utf-8")
        _canon165_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc165
        )
        _canon165 = _canon165_m.group(1) if _canon165_m else None
        _ok165 = False
        _err165 = ""
        try:
            _ac_data165 = json.loads(_ac165.read_text(encoding="utf-8"))
            _linkset165 = _ac_data165.get("linkset")
            if not isinstance(_linkset165, list) or not _linkset165:
                _err165 = f"linkset が array/非空 でない (type={type(_linkset165).__name__})"
            else:
                _anchor165 = _linkset165[0].get("anchor")
                if not isinstance(_anchor165, str):
                    _err165 = f"linkset[0].anchor が文字列でない ({_anchor165!r})"
                elif not _canon165:
                    _err165 = "canonical URL を index.html から抽出できない"
                elif not _anchor165.startswith(_canon165):
                    _err165 = f"anchor={_anchor165!r} が canonical {_canon165!r} で始まらない"
                else:
                    _ok165 = True
        except json.JSONDecodeError as e:
            _err165 = f"JSON parse 失敗: {e}"
        check(
            _ok165,
            f"Check 165: .well-known/api-catalog valid JSON + anchor starts with canonical "
            f"({_canon165!r})",
            f"Check 165: .well-known/api-catalog 整合 fail: {_err165} — AI crawler の API "
            "endpoint discovery が silent に崩壊する。.well-known/api-catalog を修正せよ",
            blocking=True,
        )
    else:
        check(False, "Check 165: .well-known/api-catalog + index.html present",
              "Check 165: .well-known/api-catalog もしくは index.html が無い",
              blocking=True)

    # ── 166. sitemap.xml <loc> URLs all start with canonical URL prefix (BLOCKING) ─
    # sitemap.xml の全 `<loc>` URL が `<link rel=canonical>` href を full prefix と
    # して持つことを BLOCKING 強制する。Check 63 は origin-only 整合だが、本 Check は
    # canonical URL の full prefix (origin + base path) で揃える。drift (sibling
    # project path 等) は SILENT — sitemap crawler が 404 する URL を index する。
    _sm166 = ROOT / "sitemap.xml"
    _idx166 = ROOT / "index.html"
    if _sm166.exists() and _idx166.exists():
        _isrc166 = _idx166.read_text(encoding="utf-8")
        _smsrc166 = _sm166.read_text(encoding="utf-8")
        _canon166_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc166
        )
        _canon166 = _canon166_m.group(1) if _canon166_m else None
        _locs166 = re.findall(r"<loc>([^<]+)</loc>", _smsrc166)
        _drift166 = [u for u in _locs166 if _canon166 and not u.startswith(_canon166)]
        _ok166 = _canon166 is not None and bool(_locs166) and not _drift166
        check(
            _ok166,
            f"Check 166: sitemap.xml {len(_locs166)} 件 <loc> 全て canonical prefix で始まる "
            f"({_canon166!r})",
            (f"Check 166: <loc> prefix drift: canonical={_canon166!r} / drifted={_drift166[:3]}... "
             f"({len(_drift166)} 件) — sitemap crawler が 404 する URL を index する。"
             "sitemap.xml の <loc> を canonical URL prefix に揃えるか canonical を修正せよ"
             if _canon166 and _locs166 else
             f"Check 166: canonical もしくは <loc> 抽出不可 "
             f"(canonical={_canon166} / locs={len(_locs166)})"),
            blocking=True,
        )
    else:
        check(False, "Check 166: sitemap.xml + index.html present",
              "Check 166: sitemap.xml もしくは index.html が無い", blocking=True)
