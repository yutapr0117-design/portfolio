"""
checks_jsonld_meta.py — JSON-LD ref-type + meta length + sitemap value coherence checks (221-235)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  221. JSON-LD `image` / `primaryImageOfPage` references resolve to
       `ImageObject` (type-safety): in index.html static JSON-LD, any
       `{"@id": "..."}` reference appearing as `image` or
       `primaryImageOfPage` MUST point to a node whose `@type` is
       `ImageObject` (allowing for subclasses by string match). Drift
       (e.g. image referring to `#person` or `#website` after rename)
       would silently make AI / SEO consumers retrieve a non-image entity
       when expecting an image asset — breaking image-card rendering,
       OG-style preview fallbacks, and knowledge-graph image extraction.
       Sibling of Check 216 (referential integrity) with type-safety added
       for image-slot references. (BLOCKING)

  222. JSON-LD `author` / `creator` / `reviewedBy` / `copyrightHolder` /
       `employee` refs resolve to Person OR Organization (type-safety):
       in index.html static JSON-LD, any `{"@id": "..."}` reference under
       these "agent-slot" properties MUST point to a node whose `@type` is
       `Person` or `Organization`. Drift (e.g. author referring to
       `#hero-image` or `#website` after rename) would silently make AI /
       SEO consumers attribute authorship to an image or website node,
       breaking the entity-graph "who created this" claim and corrupting
       knowledge-graph attribution. Sibling of Check 221 (image-slot type
       safety); Check 216 with type-safety added for agent-slot
       references. (BLOCKING)

  223. JSON-LD `isPartOf` refs resolve to `WebSite` | `WebPage` |
       `CreativeWork` (type-safety): in index.html static JSON-LD, any
       `{"@id": "..."}` reference under `isPartOf` MUST point to a node
       whose `@type` is `WebSite`, `WebPage`, or `CreativeWork` (the
       Schema.org-permitted containers). Drift (e.g. isPartOf →
       `#hero-image` after rename) would silently make AI / SEO consumers
       claim a WebPage / Article is part of an image, breaking hierarchical
       site structure for knowledge-graph rendering. Sibling of Check 221
       (image-slot) / Check 222 (agent-slot) type-safety for the structural
       isPartOf-slot. (BLOCKING)

  224. `<meta name="description">` content length in SEO-sane band: the
       index.html `<meta name="description">` content character length must
       be within [30, 300] characters. Below 30 = SERP snippet preview
       suppressed by Google (too short to extract); above 300 = silently
       truncated with ellipsis in SERP. Both extremes corrupt the SEO/AI
       crawler card. Check 154 enforces presence + og/twitter coherence;
       Check 224 enforces sanity of length. (BLOCKING)

  225. HTML `<title>` content length in SEO-sane band [10, 70]: the index
       .html `<title>` content character length must fall in [10, 70].
       Below 10 = title too sparse for SERP rendering; above 70 = silent
       truncation with ellipsis on Google SERP. Both extremes corrupt the
       primary entity card in search results. Check 66 enforces presence of
       canonical entity identifier in title; Check 225 enforces length
       sanity. (BLOCKING)

  226. og:title length in [10, 90] AND og:description length in [30, 250]:
       Open Graph card preview tools (Facebook/LinkedIn/Slack/Discord)
       render social cards using these fields. Title <10 = card title
       sparse; >90 = silent truncation by Facebook. Description <30 =
       suppressed preview; >250 = truncated. Both extremes corrupt the
       social-card entity preview. og:title byte-identical to twitter:title
       via Check 155, so this Check transitively covers Twitter as well.
       Length sanity sibling of Check 224 (description) / 225 (title) for
       the Open Graph surface. (BLOCKING)

  227. JSON-LD Person `name` matches canonical entity name: every node in
       index.html static JSON-LD with `"@type": "Person"` MUST have `name`
       equal to one of the canonical entity identifiers from CLAUDE.md §1:
       "Yuta Yokoi", "横井雄太", or "Yokoi Yuta". Drift (e.g. accidentally
       changing one of the 3 Person blocks' name to a typo or generic
       "Anonymous") would silently fragment AI/SEO entity identity across
       JSON-LD blocks. Sibling of Check 195 (Person alternateName) /
       Check 203 (Person givenName/familyName) for the Person `name`
       primary field. (BLOCKING)

  228. sitemap.xml `<changefreq>` values are valid per Sitemap Protocol:
       every `<changefreq>` element in sitemap.xml must contain one of the
       7 spec-allowed values: `always`, `hourly`, `daily`, `weekly`,
       `monthly`, `yearly`, `never`. Drift (e.g. `weakly` typo,
       `biweekly`, or empty) would silently make crawlers ignore the
       crawl-frequency hint — the URL is still discovered but the freshness
       hint that improves recrawl scheduling is lost. (BLOCKING)

  229. sitemap.xml `<priority>` values are float in [0.0, 1.0] (Sitemap
       Protocol): every `<priority>` element in sitemap.xml must parse as
       a float in the closed interval [0.0, 1.0]. Drift (e.g. `1.5` typo
       or `"high"`) is invalid per spec — crawlers silently fall back to
       the default 0.5, ignoring the priority signal entirely. Sibling of
       Check 228 (changefreq spec-valid) for the priority field. (BLOCKING)

  230. sitemap.xml has exactly one `<url>` with `<priority>1.0</priority>`,
       matching canonical URL: the sitemap must reserve `priority=1.0`
       (Sitemap Protocol's maximum) for THE single canonical homepage. Drift
       (multiple priority=1.0 entries, or priority=1.0 on a non-canonical
       URL) silently splits the SEO "this is the primary entry point"
       signal across multiple URLs, diluting the canonical authority for
       AI/search crawlers. Sibling of Check 229 (priority range) /
       Check 150 (og:url ↔ canonical) for the sitemap entry-point axis.
       (BLOCKING)

  231. main.js SITE_CONFIG.ROLE_TITLE matches canonical entity role: the
       `ROLE_TITLE` value in main.js SITE_CONFIG MUST equal one of the 3
       canonical entity roles from CLAUDE.md §1: "AI-Driven PM" /
       "IT Consultant" / "KERNEL Framework Designer". Drift silently
       misrepresents the entity in JS-rendered UI (used in page titles
       and meta descriptions emitted by the SPA renderer). Sibling of
       Check 169 (aio-manifest entity.role canonical markers) for the
       SITE_CONFIG.ROLE_TITLE axis. (BLOCKING)

  232. `<meta name="ai:*">` content URLs all use HTTPS: every
       `<meta name="ai:context|entrypoint|canonical|repository|aio-manifest|
       ...">` content value that is an absolute URL (scheme prefix) MUST
       start with `https://`. Drift to `http://` would silently downgrade
       the AIO routing layer's transport security — AI crawlers following
       these URLs hit Mixed Content blocking on HTTPS-served pages.
       Sibling of Check 207 (HTML src/href HTTPS) for the ai:* meta
       content surface. (BLOCKING)

  233. `<meta name="asset:*">` content URLs all use HTTPS: every
       `<meta name="asset:image:*|asset:audio:*">` content value that is
       an absolute URL (scheme prefix) MUST start with `https://`. Drift
       to `http://` would silently make AI / SEO crawler fetch the
       canonical asset over insecure transport — Mixed Content blocking
       and authenticity-grade degradation. Sibling of Check 232 (ai:*
       content HTTPS) for the asset:* meta surface. (BLOCKING)

  234. `<meta name="asset:*">` content URLs (absolute) share canonical URL
       prefix: every `<meta name="asset:*">` content value that is an
       absolute URL MUST start with the canonical URL prefix. Drift (e.g.
       asset:image:canonical pointing at a CDN or sibling project) would
       silently advertise non-canonical asset URLs to AI/SEO, splitting
       authority and breaking entity-asset linkage. Sibling of Check 171
       (ai:* canonical prefix) for the asset:* meta surface. (BLOCKING)

  235. JSON-LD Article/TechArticle nodes with `@id` (full definitions) have
       Schema.org required fields headline + author + datePublished:
       in index.html static JSON-LD, every Article/TechArticle node that
       has an `@id` (treated as a "full" definition rather than an external
       reference) MUST include `headline`, `author`, and `datePublished`.
       Drift (silent omission) would make Google rich-result eligibility
       fail and degrade AI search Article snippet generation. Article
       references WITHOUT `@id` (external URL pointers in `subjectOf` /
       `citation`) are exempt — they represent "this URL is an Article"
       rather than a self-described Article. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 221. JSON-LD image / primaryImageOfPage refs resolve to ImageObject (BLOCKING) ─
    # index.html 静的 JSON-LD で `image` / `primaryImageOfPage` の `{"@id":...}` 参照が、
    # 同 graph 内で `@type == "ImageObject"` の node に解決することを BLOCKING 強制。
    # Check 216 (referential integrity) に「参照先 @type が ImageObject」の type-safety を追加。
    # drift は SILENT に AI/SEO consumer が non-image entity を image slot で取得し、
    # image-card rendering / OG preview / 知識グラフ image extraction を破壊。
    _idx221 = ROOT / "index.html"
    if _idx221.exists():
        _isrc221 = _idx221.read_text(encoding="utf-8")
        _blocks221 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc221,
            flags=re.DOTALL,
        )
        _IMAGE_REF_PROPS221 = {"image", "primaryImageOfPage"}
        _typeof221: dict[str, str] = {}
        _img_refs221: list[tuple[str, str]] = []
        def _walk221(node: object, parent_key: str | None = None) -> None:
            if isinstance(node, dict):
                _t = node.get("@type")
                _id = node.get("@id")
                if isinstance(_t, str) and isinstance(_id, str):
                    _typeof221[_id] = _t
                if (
                    parent_key in _IMAGE_REF_PROPS221
                    and isinstance(_id, str)
                    and "@type" not in node
                ):
                    _img_refs221.append((parent_key, _id))
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk221(item, k)
                    else:
                        _walk221(v, k)
            elif isinstance(node, list):
                for item in node:
                    _walk221(item, parent_key)
        for _blk in _blocks221:
            try:
                _data221 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk221(_data221)
        _wrong_type221: list[str] = []
        for _prop, _rid in _img_refs221:
            _resolved_type = _typeof221.get(_rid)
            if _resolved_type != "ImageObject":
                _wrong_type221.append(f"{_prop}@id={_rid}: type={_resolved_type!r}")
        _ok221 = len(_img_refs221) > 0 and not _wrong_type221
        check(
            _ok221,
            f"Check 221: JSON-LD image/primaryImageOfPage refs {len(_img_refs221)} 件全て ImageObject @type へ解決",
            (f"Check 221: type 不一致 image refs: {_wrong_type221!r} — AI/SEO が "
             "non-image entity を image slot で取得し card rendering 破壊。"
             "参照先 node の @type を ImageObject へ揃えるか refs を訂正せよ"
             if _wrong_type221 else
             "Check 221: image/primaryImageOfPage refs 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 221: index.html present",
              "Check 221: index.html が無い", blocking=True)

    # ── 222. JSON-LD author/creator/reviewedBy/copyrightHolder/employee refs Person|Organization (BLOCKING) ─
    # index.html 静的 JSON-LD で `author` / `creator` / `reviewedBy` /
    # `copyrightHolder` / `employee` の `{"@id":...}` 参照が、同 graph 内で
    # `@type in {Person, Organization}` の node に解決することを BLOCKING 強制。
    # Check 221 (image-slot type safety) の agent-slot 軸版。drift は SILENT に
    # AI/SEO consumer が著者帰属を image や website へ誤帰属し knowledge-graph 攻撃。
    _AGENT_REF_PROPS222 = {
        "author", "creator", "reviewedBy", "copyrightHolder", "employee",
    }
    _AGENT_OK_TYPES222 = {"Person", "Organization"}
    _idx222 = ROOT / "index.html"
    if _idx222.exists():
        _isrc222 = _idx222.read_text(encoding="utf-8")
        _blocks222 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc222,
            flags=re.DOTALL,
        )
        _typeof222: dict[str, str] = {}
        _agent_refs222: list[tuple[str, str]] = []
        def _walk222(node: object, parent_key: str | None = None) -> None:
            if isinstance(node, dict):
                _t = node.get("@type")
                _id = node.get("@id")
                if isinstance(_t, str) and isinstance(_id, str):
                    _typeof222[_id] = _t
                if (
                    parent_key in _AGENT_REF_PROPS222
                    and isinstance(_id, str)
                    and "@type" not in node
                ):
                    _agent_refs222.append((parent_key, _id))
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk222(item, k)
                    else:
                        _walk222(v, k)
            elif isinstance(node, list):
                for item in node:
                    _walk222(item, parent_key)
        for _blk in _blocks222:
            try:
                _data222 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk222(_data222)
        _wrong_type222: list[str] = []
        for _prop, _rid in _agent_refs222:
            _resolved_type = _typeof222.get(_rid)
            if _resolved_type not in _AGENT_OK_TYPES222:
                _wrong_type222.append(f"{_prop}@id={_rid}: type={_resolved_type!r}")
        _ok222 = len(_agent_refs222) > 0 and not _wrong_type222
        check(
            _ok222,
            f"Check 222: JSON-LD agent-slot refs {len(_agent_refs222)} 件全て Person|Organization へ解決",
            (f"Check 222: type 不一致 agent refs: {_wrong_type222!r} — AI/SEO で "
             "著者帰属が non-agent entity に誤帰属し knowledge-graph 破壊。"
             "参照先 node の @type を Person|Organization へ揃えるか refs を訂正せよ"
             if _wrong_type222 else
             "Check 222: agent-slot refs 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 222: index.html present",
              "Check 222: index.html が無い", blocking=True)

    # ── 223. JSON-LD isPartOf refs resolve to WebSite|WebPage|CreativeWork (BLOCKING) ─
    # index.html 静的 JSON-LD で `isPartOf` の `{"@id":...}` 参照が、同 graph 内で
    # `@type in {WebSite, WebPage, CreativeWork}` の node に解決することを BLOCKING 強制。
    # Check 221 (image-slot) / Check 222 (agent-slot) の isPartOf 構造軸版。
    _ISPARTOF_OK_TYPES223 = {"WebSite", "WebPage", "CreativeWork"}
    _idx223 = ROOT / "index.html"
    if _idx223.exists():
        _isrc223 = _idx223.read_text(encoding="utf-8")
        _blocks223 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc223,
            flags=re.DOTALL,
        )
        _typeof223: dict[str, str] = {}
        _ip_refs223: list[str] = []
        def _walk223(node: object, parent_key: str | None = None) -> None:
            if isinstance(node, dict):
                _t = node.get("@type")
                _id = node.get("@id")
                if isinstance(_t, str) and isinstance(_id, str):
                    _typeof223[_id] = _t
                if (
                    parent_key == "isPartOf"
                    and isinstance(_id, str)
                    and "@type" not in node
                ):
                    _ip_refs223.append(_id)
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk223(item, k)
                    else:
                        _walk223(v, k)
            elif isinstance(node, list):
                for item in node:
                    _walk223(item, parent_key)
        for _blk in _blocks223:
            try:
                _data223 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk223(_data223)
        _wrong_type223: list[str] = []
        for _rid in _ip_refs223:
            _resolved_type = _typeof223.get(_rid)
            if _resolved_type not in _ISPARTOF_OK_TYPES223:
                _wrong_type223.append(f"isPartOf@id={_rid}: type={_resolved_type!r}")
        _ok223 = len(_ip_refs223) > 0 and not _wrong_type223
        check(
            _ok223,
            f"Check 223: JSON-LD isPartOf refs {len(_ip_refs223)} 件全て WebSite|WebPage|CreativeWork へ解決",
            (f"Check 223: type 不一致 isPartOf refs: {_wrong_type223!r} — AI/SEO が "
             "page/article を非構造 entity へ contain させ階層が破壊。"
             "参照先 node の @type を WebSite|WebPage|CreativeWork へ揃えるか refs を訂正せよ"
             if _wrong_type223 else
             "Check 223: isPartOf refs 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 223: index.html present",
              "Check 223: index.html が無い", blocking=True)

    # ── 224. <meta name=description> content length in [30, 300] (BLOCKING) ───────
    # index.html `<meta name="description">` content の character length が
    # SEO-sane band [30, 300] であることを BLOCKING 強制。<30 = SERP snippet preview
    # 抑制 (短すぎ抽出不能) / >300 = 静かに truncate (...)。Check 154 (presence) を
    # 補完する length sanity 軸。
    _idx224 = ROOT / "index.html"
    if _idx224.exists():
        _isrc224 = _idx224.read_text(encoding="utf-8")
        _desc224_m = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', _isrc224
        )
        _desc224 = _desc224_m.group(1) if _desc224_m else None
        _len224 = len(_desc224) if isinstance(_desc224, str) else 0
        _ok224 = _desc224 is not None and 30 <= _len224 <= 300
        check(
            _ok224,
            f"Check 224: <meta name=description> length={_len224} (SEO-sane band [30, 300])",
            (f"Check 224: description length={_len224} (band [30, 300] 違反) — "
             f"{'抽出不能で SERP snippet 抑制' if _len224 < 30 else '300 超えで SERP 末尾 truncate'}。"
             "description 長を band 内へ調整せよ"
             if _desc224 is not None else
             "Check 224: <meta name=description> が無い"),
            blocking=True,
        )
    else:
        check(False, "Check 224: index.html present",
              "Check 224: index.html が無い", blocking=True)

    # ── 225. <title> content length in [10, 70] (BLOCKING) ────────────────────────
    # index.html <title> content の character length が [10, 70] に収まることを
    # BLOCKING 強制。<10 = sparse 過ぎ SERP 表示不適 / >70 = SERP で末尾 truncate。
    # Check 66 (canonical 名 presence) を補完する length sanity 軸。
    _idx225 = ROOT / "index.html"
    if _idx225.exists():
        _isrc225 = _idx225.read_text(encoding="utf-8")
        _title225_m = re.search(r"<title>([^<]+)</title>", _isrc225)
        _title225 = _title225_m.group(1) if _title225_m else None
        _len225 = len(_title225) if isinstance(_title225, str) else 0
        _ok225 = _title225 is not None and 10 <= _len225 <= 70
        check(
            _ok225,
            f"Check 225: <title> length={_len225} (SEO-sane band [10, 70])",
            (f"Check 225: title length={_len225} (band [10, 70] 違反) — "
             f"{'sparse 過ぎ SERP 表示不適' if _len225 < 10 else '70 超えで SERP 末尾 truncate'}。"
             "title 長を band 内へ調整せよ"
             if _title225 is not None else
             "Check 225: <title> が無い"),
            blocking=True,
        )
    else:
        check(False, "Check 225: index.html present",
              "Check 225: index.html が無い", blocking=True)

    # ── 226. og:title [10, 90] + og:description [30, 250] length (BLOCKING) ───────
    # index.html `og:title` length [10, 90] / `og:description` length [30, 250] を
    # BLOCKING 強制。Facebook/LinkedIn/Slack/Discord の social card preview で
    # 短すぎ表示抑制 / 長すぎ silent truncate を阻止。Check 155 (og↔twitter byte-id)
    # によって twitter card にも同時適用。Check 224/225 の Open Graph 軸版。
    _idx226 = ROOT / "index.html"
    if _idx226.exists():
        _isrc226 = _idx226.read_text(encoding="utf-8")
        _og_t226 = re.search(
            r'<meta\s+property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', _isrc226
        )
        _og_d226 = re.search(
            r'<meta\s+property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']', _isrc226
        )
        _bad226: list[str] = []
        if _og_t226:
            _lt = len(_og_t226.group(1))
            if not (10 <= _lt <= 90):
                _bad226.append(f"og:title length={_lt} (band [10, 90] 違反)")
        else:
            _bad226.append("og:title 抽出不可")
        if _og_d226:
            _ld = len(_og_d226.group(1))
            if not (30 <= _ld <= 250):
                _bad226.append(f"og:description length={_ld} (band [30, 250] 違反)")
        else:
            _bad226.append("og:description 抽出不可")
        _ok226 = not _bad226
        check(
            _ok226,
            f"Check 226: og:title length={len(_og_t226.group(1)) if _og_t226 else 0} / "
            f"og:description length={len(_og_d226.group(1)) if _og_d226 else 0} 共に SEO-sane band 内",
            (f"Check 226: og length 違反: {_bad226!r} — "
             "social card preview が短すぎ抑制 / 長すぎ silent truncate。band 内へ調整せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 226: index.html present",
              "Check 226: index.html が無い", blocking=True)

    # ── 227. JSON-LD Person name == canonical entity name (BLOCKING) ──────────────
    # index.html 静的 JSON-LD の全 `"@type": "Person"` node の `name` が
    # canonical entity identifier ("Yuta Yokoi" / "横井雄太" / "Yokoi Yuta") の
    # いずれかに一致することを BLOCKING 強制。drift は SILENT に AI/SEO の entity
    # identity を block 跨ぎで断片化。
    _CANONICAL_PERSON_NAMES227 = {"Yuta Yokoi", "横井雄太", "Yokoi Yuta"}
    _idx227 = ROOT / "index.html"
    if _idx227.exists():
        _isrc227 = _idx227.read_text(encoding="utf-8")
        _blocks227 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc227,
            flags=re.DOTALL,
        )
        _names227: list[str] = []
        def _walk227(node: object) -> None:
            if isinstance(node, dict):
                if node.get("@type") == "Person" and isinstance(node.get("name"), str):
                    _names227.append(node["name"])
                for v in node.values():
                    if isinstance(v, list):
                        for item in v:
                            _walk227(item)
                    else:
                        _walk227(v)
            elif isinstance(node, list):
                for item in node:
                    _walk227(item)
        for _blk in _blocks227:
            try:
                _data227 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk227(_data227)
        _bad227 = [n for n in _names227 if n not in _CANONICAL_PERSON_NAMES227]
        _ok227 = len(_names227) > 0 and not _bad227
        check(
            _ok227,
            f"Check 227: JSON-LD Person.name {len(_names227)} 件全て canonical 名 ('Yuta Yokoi'/'横井雄太'/'Yokoi Yuta') に一致",
            (f"Check 227: 非 canonical Person.name: {_bad227!r} — AI/SEO entity identity "
             "が断片化。canonical 名へ揃えよ"
             if _bad227 else
             "Check 227: Person.name 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 227: index.html present",
              "Check 227: index.html が無い", blocking=True)

    # ── 228. sitemap.xml <changefreq> values are spec-valid (BLOCKING) ────────────
    # sitemap.xml 全 `<changefreq>` 要素の content が Sitemap Protocol 規定の 7 値
    # (always/hourly/daily/weekly/monthly/yearly/never) のいずれかであることを
    # BLOCKING 強制。drift (typo / 不正値) は SILENT に crawler が freshness hint を
    # 無視 → recrawl scheduling が劣化。
    _VALID_CHANGEFREQ228 = {
        "always", "hourly", "daily", "weekly", "monthly", "yearly", "never",
    }
    _sitemap228 = ROOT / "sitemap.xml"
    if _sitemap228.exists():
        _ssrc228 = _sitemap228.read_text(encoding="utf-8")
        _freqs228 = re.findall(r"<changefreq>([^<]+)</changefreq>", _ssrc228)
        _bad228 = [f for f in _freqs228 if f not in _VALID_CHANGEFREQ228]
        _ok228 = len(_freqs228) > 0 and not _bad228
        check(
            _ok228,
            f"Check 228: sitemap.xml changefreq {len(_freqs228)} 件全て spec-valid 値",
            (f"Check 228: spec 外 changefreq: {_bad228!r} — crawler が freshness hint "
             "を無視。Sitemap Protocol 規定値 ({always|hourly|daily|weekly|monthly|yearly|never}) へ揃えよ"
             if _bad228 else
             "Check 228: sitemap.xml <changefreq> 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 228: sitemap.xml present",
              "Check 228: sitemap.xml が無い", blocking=True)

    # ── 229. sitemap.xml <priority> values in [0.0, 1.0] (BLOCKING) ───────────────
    # sitemap.xml 全 `<priority>` 要素の content が float [0.0, 1.0] にあることを
    # BLOCKING 強制。drift (1.5 / "high" / 負値) は spec 違反で crawler が silent に
    # default 0.5 へ fallback → priority hint 喪失。Check 228 (changefreq) の priority 軸。
    _sitemap229 = ROOT / "sitemap.xml"
    if _sitemap229.exists():
        _ssrc229 = _sitemap229.read_text(encoding="utf-8")
        _prios229 = re.findall(r"<priority>([^<]+)</priority>", _ssrc229)
        _bad229: list[str] = []
        for _p in _prios229:
            try:
                _v = float(_p)
            except ValueError:
                _bad229.append(f"{_p!r} (not float)")
                continue
            if not (0.0 <= _v <= 1.0):
                _bad229.append(f"{_p!r} (out of [0.0, 1.0])")
        _ok229 = len(_prios229) > 0 and not _bad229
        check(
            _ok229,
            f"Check 229: sitemap.xml priority {len(_prios229)} 件全て float in [0.0, 1.0]",
            (f"Check 229: spec 外 priority: {_bad229!r} — crawler が default 0.5 へ "
             "fallback し priority hint 喪失。spec 規定 float [0.0, 1.0] へ揃えよ"
             if _bad229 else
             "Check 229: sitemap.xml <priority> 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 229: sitemap.xml present",
              "Check 229: sitemap.xml が無い", blocking=True)

    # ── 230. sitemap.xml ちょうど 1 <url> が <priority>1.0</priority> 且つ canonical (BLOCKING) ─
    # sitemap.xml の `<priority>1.0</priority>` が含まれる <url> が ちょうど 1 件で、
    # その <loc> が canonical URL と一致することを BLOCKING 強制。drift (priority=1.0
    # が複数 / non-canonical) は SILENT に「primary entry point」signal を分散させ
    # canonical authority を希釈。
    _sitemap230 = ROOT / "sitemap.xml"
    _idx230 = ROOT / "index.html"
    if _sitemap230.exists() and _idx230.exists():
        _ssrc230 = _sitemap230.read_text(encoding="utf-8")
        _isrc230 = _idx230.read_text(encoding="utf-8")
        _canon230_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc230
        )
        _canon230 = _canon230_m.group(1) if _canon230_m else None
        # 各 <url> block を抽出
        _url_blocks230 = re.findall(r"<url>(.*?)</url>", _ssrc230, flags=re.DOTALL)
        _p1_locs230: list[str] = []
        for _ub in _url_blocks230:
            if re.search(r"<priority>\s*1\.0\s*</priority>", _ub):
                _loc_m = re.search(r"<loc>([^<]+)</loc>", _ub)
                if _loc_m:
                    _p1_locs230.append(_loc_m.group(1))
        _violations230: list[str] = []
        if _canon230 is None:
            _violations230.append("canonical URL 抽出不可")
        if len(_p1_locs230) != 1:
            _violations230.append(f"priority=1.0 count={len(_p1_locs230)} (expected 1)")
        elif _canon230 and _p1_locs230[0] != _canon230:
            _violations230.append(f"priority=1.0 loc={_p1_locs230[0]!r} != canonical={_canon230!r}")
        _ok230 = not _violations230
        check(
            _ok230,
            f"Check 230: sitemap.xml priority=1.0 が 1 件で canonical URL ({_canon230!r}) に一致",
            (f"Check 230: 違反: {_violations230!r} — 「primary entry point」signal が "
             "分散し canonical authority 希釈。priority=1.0 は canonical homepage 1 件のみへ"),
            blocking=True,
        )
    else:
        check(False, "Check 230: sitemap.xml + index.html present",
              "Check 230: sitemap.xml もしくは index.html が無い", blocking=True)

    # ── 231. main.js SITE_CONFIG.ROLE_TITLE == canonical role (BLOCKING) ──────────
    # main.js SITE_CONFIG.ROLE_TITLE が canonical entity role 3 値 ("AI-Driven PM" /
    # "IT Consultant" / "KERNEL Framework Designer") のいずれかに一致することを
    # BLOCKING 強制。drift は SILENT に SPA renderer 出力 (title / meta) で entity を誤表現。
    _CANONICAL_ROLES231 = {
        "AI-Driven PM", "IT Consultant", "KERNEL Framework Designer",
    }
    _main231 = ROOT / "main.js"
    if _main231.exists():
        _msrc231 = _main231.read_text(encoding="utf-8")
        _role231_m = re.search(r"ROLE_TITLE:\s*['\"]([^'\"]+)['\"]", _msrc231)
        _role231 = _role231_m.group(1) if _role231_m else None
        _ok231 = _role231 is not None and _role231 in _CANONICAL_ROLES231
        check(
            _ok231,
            f"Check 231: SITE_CONFIG.ROLE_TITLE={_role231!r} が canonical role に一致",
            (f"Check 231: SITE_CONFIG.ROLE_TITLE={_role231!r} 非 canonical — "
             "SPA renderer 出力 (title/meta) で entity 役割が誤表現。"
             "{'AI-Driven PM','IT Consultant','KERNEL Framework Designer'} のいずれかへ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 231: main.js present",
              "Check 231: main.js が無い", blocking=True)

    # ── 232. <meta name=ai:*> content URLs all HTTPS (BLOCKING) ───────────────────
    # index.html `<meta name="ai:...">` content attribute の absolute URL (scheme 付き)
    # が全て `https://` で始まることを BLOCKING 強制 (negative invariant)。drift は
    # SILENT に AIO routing layer を downgrade し AI crawler が Mixed Content blocking。
    _idx232 = ROOT / "index.html"
    if _idx232.exists():
        _isrc232 = _idx232.read_text(encoding="utf-8")
        _ai_urls232 = re.findall(
            r'<meta\s+name=["\']ai:[^"\']+["\'][^>]*content=["\'](http://[^"\']+)["\']',
            _isrc232,
        )
        _ok232 = len(_ai_urls232) == 0
        check(
            _ok232,
            "Check 232: <meta name=ai:*> content に http:// 不在 (AIO routing HTTPS guard)",
            (f"Check 232: <meta name=ai:*> content に http:// URL: {_ai_urls232!r} — "
             "AI crawler が Mixed Content blocking で AIO routing 喪失。https:// に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 232: index.html present",
              "Check 232: index.html が無い", blocking=True)

    # ── 233. <meta name=asset:*> content URLs all HTTPS (BLOCKING) ────────────────
    # index.html `<meta name="asset:*">` content attribute の absolute URL (scheme 付き)
    # が全て `https://` で始まることを BLOCKING 強制 (negative invariant)。Check 232
    # (ai:* content HTTPS) の asset:* axis 版。drift は SILENT に AI/SEO crawler が
    # asset を Mixed Content blocking で fetch 失敗し authenticity-grade 劣化。
    _idx233 = ROOT / "index.html"
    if _idx233.exists():
        _isrc233 = _idx233.read_text(encoding="utf-8")
        _asset_urls233 = re.findall(
            r'<meta\s+name=["\']asset:[^"\']+["\'][^>]*content=["\'](http://[^"\']+)["\']',
            _isrc233,
        )
        _ok233 = len(_asset_urls233) == 0
        check(
            _ok233,
            "Check 233: <meta name=asset:*> content に http:// 不在 (AIO asset HTTPS guard)",
            (f"Check 233: <meta name=asset:*> content に http:// URL: {_asset_urls233!r} — "
             "AI/SEO crawler が Mixed Content blocking で asset fetch 失敗、authenticity 劣化。"
             "https:// に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 233: index.html present",
              "Check 233: index.html が無い", blocking=True)

    # ── 234. <meta name=asset:*> content URLs (absolute) share canonical prefix (BLOCKING) ─
    # index.html `<meta name="asset:*">` content attribute の absolute URL (http(s):// で
    # 始まる値) が canonical URL prefix で始まることを BLOCKING 強制。drift は SILENT に
    # AI/SEO へ non-canonical asset URL を流し entity authority を二分。Check 171
    # (ai:* canonical prefix) の asset:* 軸版。
    _idx234 = ROOT / "index.html"
    if _idx234.exists():
        _isrc234 = _idx234.read_text(encoding="utf-8")
        _canon234_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc234
        )
        _canon234 = _canon234_m.group(1) if _canon234_m else None
        _asset_urls234 = re.findall(
            r'<meta\s+name=["\']asset:[^"\']+["\'][^>]*content=["\'](https?://[^"\']+)["\']',
            _isrc234,
        )
        _drifts234: list[str] = []
        if _canon234 is None:
            _drifts234.append("canonical URL 抽出不可")
        if not _asset_urls234:
            _drifts234.append("asset:* 絶対 URL 0 件 — vacuous-fail")
        for _u in _asset_urls234:
            if _canon234 and not _u.startswith(_canon234):
                _drifts234.append(f"asset URL={_u!r} canonical prefix 不一致")
        _ok234 = not _drifts234
        check(
            _ok234,
            f"Check 234: <meta name=asset:*> 絶対 URL {len(_asset_urls234)} 件全て canonical prefix {_canon234!r} で始まる",
            (f"Check 234: drift: {_drifts234!r} — AI/SEO crawler が non-canonical asset を "
             "正規扱いし entity authority 二分。canonical prefix に揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 234: index.html present",
              "Check 234: index.html が無い", blocking=True)

    # ── 235. JSON-LD Article/TechArticle with @id has headline+author+datePublished (BLOCKING) ─
    # index.html 静的 JSON-LD で `@type in {Article, TechArticle}` かつ `@id` を持つ
    # (full definition) node が Schema.org 必須 field (headline + author +
    # datePublished) を持つことを BLOCKING 強制。@id 無し (subjectOf/citation の
    # 外部 URL 参照) は self-description でないため exempt。drift は Google rich-result
    # 失格 + AI search Article snippet 劣化。
    _REQUIRED_ARTICLE_FIELDS235 = ("headline", "author", "datePublished")
    _idx235 = ROOT / "index.html"
    if _idx235.exists():
        _isrc235 = _idx235.read_text(encoding="utf-8")
        _blocks235 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc235,
            flags=re.DOTALL,
        )
        _violations235: list[str] = []
        _full_count235 = 0
        def _walk235(node: object, path: str) -> None:
            nonlocal _full_count235
            if isinstance(node, dict):
                _t = node.get("@type")
                if isinstance(_t, str) and _t in ("Article", "TechArticle") and "@id" in node:
                    _full_count235 += 1
                    _missing = [f for f in _REQUIRED_ARTICLE_FIELDS235 if f not in node]
                    if _missing:
                        _violations235.append(f"{path} {_t}@id={node.get('@id')!r}: missing {_missing!r}")
                for k, v in node.items():
                    _walk235(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk235(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks235):
            try:
                _data235 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk235(_data235, f"block{_bi}")
        _ok235 = _full_count235 > 0 and not _violations235
        check(
            _ok235,
            f"Check 235: Article/TechArticle full def ({_full_count235} 件) 全て headline+author+datePublished を持つ",
            (f"Check 235: 必須 field 欠落: {_violations235!r} — Google rich-result 失格 + "
             "AI search Article snippet 劣化。Schema.org 必須 field を追加せよ"
             if _violations235 else
             "Check 235: @id 付き Article/TechArticle 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 235: index.html present",
              "Check 235: index.html が無い", blocking=True)
