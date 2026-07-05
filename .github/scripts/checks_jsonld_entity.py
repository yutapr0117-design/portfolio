"""
checks_jsonld_entity.py — JSON-LD Person/WebSite/WebPage/Organization canonical entity coherence checks (191-200)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  191. CNAME file absence (canonical URL is github.io subdomain): the repository
       root must NOT contain a `CNAME` file (negative invariant). The canonical
       URL (`https://yutapr0117-design.github.io/portfolio/`) is a GitHub Pages
       subdomain, not a custom domain. Adding a CNAME file would silently
       redirect GitHub Pages deployment to that custom domain — if the domain
       is unconfigured / unowned, the entire site 404s; if it's owned but
       unconfigured, AIO entity canonical URL diverges from the actual served
       URL (silent breaking of every URL coherence Check). Companion of Check
       190 (.nojekyll presence) — the two are the structural baseline for
       canonical GitHub Pages deployment. (BLOCKING)
  192. JSON-LD Person `url` matches canonical URL: in the static JSON-LD Person
       block in index.html, the `url` property must equal the canonical URL
       (`<link rel="canonical">` href). Drift would silently desync the entity's
       declared homepage from the canonical page that crawlers actually index,
       breaking AI/social crawler entity-to-page linking. Sibling of Check 176
       (@id own-origin canonical prefix) for the `url` property axis. (BLOCKING)
  193. JSON-LD WebSite `url` matches canonical URL: in the static JSON-LD WebSite
       block in index.html, the `url` property must equal the canonical URL
       (`<link rel="canonical">` href). Drift would silently desync the WebSite
       entity's declared URL from the canonical page, breaking JSON-LD
       WebSite-to-page anchor and confusing Search Console "About this result"
       enrichment. Sibling of Check 192 (Person.url) for the WebSite axis.
       (BLOCKING)
  194. JSON-LD WebPage `url` matches canonical URL: in static JSON-LD WebPage
       blocks in index.html, the `url` property must equal the canonical URL.
       Drift would silently desync the page entity's declared URL from the
       canonical page, breaking AI/search-engine page-to-canonical resolution
       (the WebPage block is the most-directly-page-mapped JSON-LD entity).
       Completes the Person/WebSite/WebPage URL-coherence triangle for the
       canonical-URL anchor (Checks 192 + 193 + 194). (BLOCKING)
  195. JSON-LD Person `alternateName` contains canonical name variants: in the
       primary JSON-LD Person block in index.html, the `alternateName` array
       must contain BOTH "横井雄太" AND "Yokoi Yuta" (canonical name variants
       from CLAUDE.md §1). Drift would silently weaken AI entity-matching for
       queries using these variants (Google/AI search by 横井雄太 / Yokoi
       Yuta wouldn't anchor back to this Person entity). Sibling of Check 172
       (aio-manifest entity.name_alt) and Check 173 (js/identity.js AUTHOR) for
       the JSON-LD Person.alternateName surface. (BLOCKING)
  196. JSON-LD Organization (nkgr.co.jp) `name` = "株式会社日本経営": in
       index.html, the JSON-LD Organization block with `@id` containing
       `nkgr.co.jp/#organization` must have `name` "株式会社日本経営" (the
       canonical affiliation name from CLAUDE.md §1). Drift would silently
       desync the JSON-LD Organization entity from the canonical affiliation
       declaration shared by WebP XMP (Check 81) / MP3 ID3 (82) / aio-manifest
       (83) / README (84) / Claude2Claude (85). Completes the affiliation-name
       coherence mesh with the JSON-LD surface. (BLOCKING)
  197. JSON-LD Organization (nkgr.co.jp) `url` = "https://nkgr.co.jp/": in the
       Organization block from Check 196, the `url` property must be
       `https://nkgr.co.jp/` (the canonical Organization URL from CLAUDE.md
       §1). Drift would silently send AI/social crawlers to the wrong
       Organization homepage, breaking employee→employer URL resolution. URL
       axis sibling of Check 196 (name axis). (BLOCKING)
  198. JSON-LD Person `jobTitle` contains canonical role markers: in the
       primary JSON-LD Person block, the `jobTitle` string must contain BOTH
       "IT Consultant" AND "KERNEL Framework Designer" (canonical role markers
       from CLAUDE.md §1). Drift would silently weaken the Person entity's
       professional role declaration on AI/search-engine entity panels.
       Sibling of Check 169 (aio-manifest entity.role) for the JSON-LD
       Person.jobTitle surface. (BLOCKING)
  199. JSON-LD Person `knowsAbout` contains technical positioning anchors: in
       the primary JSON-LD Person block, the `knowsAbout` array must contain
       BOTH "KERNEL Framework" AND "Vanilla JavaScript SPA" (the unique
       technical positioning anchors that distinguish this entity from
       generic AI / PM practitioners). Drift would silently weaken AI search
       discovery for queries like "KERNEL Framework" or "Vanilla JavaScript
       SPA AI" (knowsAbout feeds Knowledge Panel topics & expert-finder
       systems). (BLOCKING)
  200. JSON-LD Person `@id` derives from canonical URL: in the primary
       JSON-LD Person block, the `@id` must equal canonical URL + "#person"
       (e.g. `https://yutapr0117-design.github.io/portfolio/#person`).
       Drift would silently break the JSON-LD entity graph anchor: secondary
       Person references (e.g. `{"@id": "...#person"}` inside creator /
       author / about properties) reference this @id by string equality; if
       primary @id drifts but references don't, the entity graph fragments
       into disjoint nodes. The trailing-slash + #person fragment derivation
       is mechanically checkable. (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 191. CNAME file absence (canonical URL is github.io subdomain) (BLOCKING) ─
    # repo root に `CNAME` file が存在しないことを BLOCKING 強制 (negative invariant)。
    # canonical URL (yutapr0117-design.github.io/portfolio/) は GitHub Pages subdomain
    # ゆえ CNAME 追加は silent に deployment を custom domain へ redirect する
    # (未所有 → 全 site 404 / 所有未設定 → AIO entity canonical URL ↔ 実 URL 分裂で
    # URL coherence Check が cascade 崩壊)。Check 190 (.nojekyll) と並ぶ GitHub Pages
    # canonical deployment baseline。
    _cname191 = ROOT / "CNAME"
    _ok191 = not _cname191.exists()
    check(
        _ok191,
        "Check 191: CNAME file 不在 (canonical URL は github.io subdomain)",
        "Check 191: CNAME file が repo root に存在 — GitHub Pages が custom domain へ "
        "deployment を redirect し canonical URL (yutapr0117-design.github.io/portfolio/) と "
        "分裂。custom domain 採用は AIO entity canonical URL の全 surface 同期更新を伴うため "
        "本 Check は意図的に CNAME を禁止。CNAME を削除せよ",
        blocking=True,
    )

    # ── 192. JSON-LD Person url matches canonical URL (BLOCKING) ──────────────────
    # index.html 静的 JSON-LD の Person block の `url` property が canonical URL
    # (`<link rel="canonical">` href) と一致することを BLOCKING 強制。drift は SILENT に
    # entity の declared homepage を canonical page から desync させ AI/social crawler
    # の entity-to-page linking を破壊。Check 176 (@id own-origin canonical prefix) の
    # `url` property 軸版。
    _idx192 = ROOT / "index.html"
    if _idx192.exists():
        _isrc192 = _idx192.read_text(encoding="utf-8")
        _canon192_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc192
        )
        _canon192 = _canon192_m.group(1) if _canon192_m else None
        # Person block: find `"@type": "Person"` then collect within block the first url
        # Person block scope: from `"@type": "Person"` to the next `"@type":` (or
        # end of file). Within that scope we look for a `"url":` at the SAME
        # indentation as `"@type":` (Person's own property, not a nested sub-block).
        _person_blocks192 = []
        _type_positions192 = [m.start() for m in re.finditer(r'"@type":', _isrc192)]
        for _m in re.finditer(r'"@type":\s*"Person"', _isrc192):
            _start = _m.start()
            # find next @type position after this Person
            _next = next((p for p in _type_positions192 if p > _start), len(_isrc192))
            _scope = _isrc192[_start:_next]
            # detect Person's own indentation: the spaces before `"@type":` on its line
            _line_start = _isrc192.rfind("\n", 0, _start) + 1
            _indent = _isrc192[_line_start:_start]  # spaces (or tabs) before `"@type":`
            # match `\n<indent>"url": "..."` (same-indent sibling, not nested)
            _u = re.search(
                r'\n' + re.escape(_indent) + r'"url":\s*"([^"]+)"', _scope
            )
            if _u:
                _person_blocks192.append(_u.group(1))
        _drifts192 = [u for u in _person_blocks192 if _canon192 and u != _canon192]
        _ok192 = (
            _canon192 is not None
            and len(_person_blocks192) > 0
            and not _drifts192
        )
        check(
            _ok192,
            f"Check 192: JSON-LD Person.url {len(_person_blocks192)} 件全て canonical URL と一致 ({_canon192!r})",
            (f"Check 192: JSON-LD Person.url drift: {_drifts192!r} ≠ canonical={_canon192!r} — "
             "AI crawler の entity-to-page linking 破壊。Person.url を canonical URL と揃えよ"
             if _drifts192 else
             "Check 192: JSON-LD Person block or canonical 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 192: index.html present",
              "Check 192: index.html が無い", blocking=True)

    # ── 193. JSON-LD WebSite url matches canonical URL (BLOCKING) ─────────────────
    # index.html 静的 JSON-LD の WebSite block の `url` property が canonical URL
    # と一致することを BLOCKING 強制。drift は SILENT に WebSite entity の declared
    # URL を canonical page から desync し JSON-LD WebSite-to-page anchor 破壊 +
    # Search Console "About this result" enrichment 混乱。Check 192 (Person.url)
    # の WebSite 軸版。同じ sibling-indent 抽出で nested url を skip。
    _idx193 = ROOT / "index.html"
    if _idx193.exists():
        _isrc193 = _idx193.read_text(encoding="utf-8")
        _canon193_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc193
        )
        _canon193 = _canon193_m.group(1) if _canon193_m else None
        _site_blocks193 = []
        _type_positions193 = [m.start() for m in re.finditer(r'"@type":', _isrc193)]
        for _m in re.finditer(r'"@type":\s*"WebSite"', _isrc193):
            _start = _m.start()
            _next = next((p for p in _type_positions193 if p > _start), len(_isrc193))
            _scope = _isrc193[_start:_next]
            _line_start = _isrc193.rfind("\n", 0, _start) + 1
            _indent = _isrc193[_line_start:_start]
            _u = re.search(r'\n' + re.escape(_indent) + r'"url":\s*"([^"]+)"', _scope)
            if _u:
                _site_blocks193.append(_u.group(1))
        _drifts193 = [u for u in _site_blocks193 if _canon193 and u != _canon193]
        _ok193 = (
            _canon193 is not None
            and len(_site_blocks193) > 0
            and not _drifts193
        )
        check(
            _ok193,
            f"Check 193: JSON-LD WebSite.url {len(_site_blocks193)} 件全て canonical URL と一致 ({_canon193!r})",
            (f"Check 193: JSON-LD WebSite.url drift: {_drifts193!r} ≠ canonical={_canon193!r} — "
             "WebSite entity ↔ canonical page anchor 破壊。WebSite.url を canonical URL と揃えよ"
             if _drifts193 else
             "Check 193: JSON-LD WebSite block or canonical 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 193: index.html present",
              "Check 193: index.html が無い", blocking=True)

    # ── 194. JSON-LD WebPage url matches canonical URL (BLOCKING) ─────────────────
    # index.html 静的 JSON-LD の WebPage block の `url` property が canonical URL と
    # 一致することを BLOCKING 強制。drift は SILENT に page entity の declared URL を
    # canonical page から desync し AI/search-engine の page-to-canonical 解決を
    # 破壊。Check 192/193 と並ぶ Person/WebSite/WebPage URL coherence triangle 完成。
    _idx194 = ROOT / "index.html"
    if _idx194.exists():
        _isrc194 = _idx194.read_text(encoding="utf-8")
        _canon194_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc194
        )
        _canon194 = _canon194_m.group(1) if _canon194_m else None
        _page_blocks194 = []
        _type_positions194 = [m.start() for m in re.finditer(r'"@type":', _isrc194)]
        for _m in re.finditer(r'"@type":\s*"WebPage"', _isrc194):
            _start = _m.start()
            _next = next((p for p in _type_positions194 if p > _start), len(_isrc194))
            _scope = _isrc194[_start:_next]
            _line_start = _isrc194.rfind("\n", 0, _start) + 1
            _indent = _isrc194[_line_start:_start]
            _u = re.search(r'\n' + re.escape(_indent) + r'"url":\s*"([^"]+)"', _scope)
            if _u:
                _page_blocks194.append(_u.group(1))
        _drifts194 = [u for u in _page_blocks194 if _canon194 and u != _canon194]
        _ok194 = (
            _canon194 is not None
            and len(_page_blocks194) > 0
            and not _drifts194
        )
        check(
            _ok194,
            f"Check 194: JSON-LD WebPage.url {len(_page_blocks194)} 件全て canonical URL と一致 ({_canon194!r})",
            (f"Check 194: JSON-LD WebPage.url drift: {_drifts194!r} ≠ canonical={_canon194!r} — "
             "page entity ↔ canonical page 解決破壊。WebPage.url を canonical URL と揃えよ"
             if _drifts194 else
             "Check 194: JSON-LD WebPage block or canonical 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 194: index.html present",
              "Check 194: index.html が無い", blocking=True)

    # ── 195. JSON-LD Person alternateName contains canonical variants (BLOCKING) ──
    # index.html 静的 JSON-LD の primary Person block の `alternateName` array が
    # CLAUDE.md §1 canonical name variants ("横井雄太" + "Yokoi Yuta") を共に含む
    # ことを BLOCKING 強制。drift は SILENT に AI entity-matching を弱体化
    # (Google/AI search で 横井雄太 / Yokoi Yuta query が本 Person entity に anchor
    # しない)。Check 172 (manifest entity.name_alt) / 173 (identity.js AUTHOR) の
    # JSON-LD Person.alternateName 軸版。
    _idx195 = ROOT / "index.html"
    if _idx195.exists():
        _isrc195 = _idx195.read_text(encoding="utf-8")
        _required195 = ["横井雄太", "Yokoi Yuta"]
        _person_alt195 = []
        _type_positions195 = [m.start() for m in re.finditer(r'"@type":', _isrc195)]
        for _m in re.finditer(r'"@type":\s*"Person"', _isrc195):
            _start = _m.start()
            _next = next((p for p in _type_positions195 if p > _start), len(_isrc195))
            _scope = _isrc195[_start:_next]
            _line_start = _isrc195.rfind("\n", 0, _start) + 1
            _indent = _isrc195[_line_start:_start]
            # match `\n<indent>"alternateName": [ ... ]` (multi-line array literal)
            _arr = re.search(
                r'\n' + re.escape(_indent) + r'"alternateName":\s*\[([^\]]*)\]', _scope
            )
            if _arr:
                _names = re.findall(r'"([^"]+)"', _arr.group(1))
                _person_alt195.append(_names)
        # check primary (first) Person.alternateName covers required variants
        _primary195 = _person_alt195[0] if _person_alt195 else []
        _missing195 = [n for n in _required195 if n not in _primary195]
        _ok195 = len(_person_alt195) > 0 and not _missing195
        check(
            _ok195,
            f"Check 195: primary Person.alternateName が canonical variants {_required195} を網羅 "
            f"({len(_primary195)} entries)",
            (f"Check 195: primary Person.alternateName に必須 variant {_missing195} 欠落 "
             f"(現 alternateName={_primary195!r}) — AI entity matching を弱体化。"
             "JSON-LD Person.alternateName array に必須 variant を追加せよ"
             if _person_alt195 else
             "Check 195: JSON-LD primary Person block alternateName 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 195: index.html present",
              "Check 195: index.html が無い", blocking=True)

    # ── 196. JSON-LD Organization (nkgr.co.jp) name = 株式会社日本経営 (BLOCKING) ─
    # index.html 静的 JSON-LD の `@id` が nkgr.co.jp/#organization を含む Organization
    # block の `name` が "株式会社日本経営" (CLAUDE.md §1 canonical affiliation 名) と
    # 一致することを BLOCKING 強制。drift は SILENT に JSON-LD Organization entity を
    # canonical affiliation 宣言 (Check 81-85 で multi-surface 強制) から desync させる。
    # 本 Check は affiliation-name coherence mesh を JSON-LD surface まで拡張。
    _idx196 = ROOT / "index.html"
    if _idx196.exists():
        _isrc196 = _idx196.read_text(encoding="utf-8")
        # find Organization block with @id containing nkgr.co.jp/#organization
        _org196_m = re.search(
            r'"@type":\s*"Organization"[^{]*?"@id":\s*"[^"]*nkgr\.co\.jp[^"]*#organization"',
            _isrc196,
            re.DOTALL,
        )
        if not _org196_m:
            # try the other ordering: @id then @type
            _org196_m = re.search(
                r'"@id":\s*"[^"]*nkgr\.co\.jp[^"]*#organization"[^{]*?"@type":\s*"Organization"',
                _isrc196,
                re.DOTALL,
            )
        _org_name196 = None
        if _org196_m:
            # scope from match start onwards ~600 chars to find name
            _scope = _isrc196[_org196_m.start():_org196_m.start() + 600]
            _n = re.search(r'"name":\s*"([^"]+)"', _scope)
            if _n:
                _org_name196 = _n.group(1)
        _expected196 = "株式会社日本経営"
        _ok196 = _org_name196 == _expected196
        check(
            _ok196,
            f"Check 196: JSON-LD Organization (nkgr.co.jp).name = {_expected196!r}",
            (f"Check 196: JSON-LD Organization (nkgr.co.jp).name = {_org_name196!r} ≠ "
             f"{_expected196!r} — affiliation-name coherence (Check 81-85 と Multi-surface) "
             "から JSON-LD surface が drift。CLAUDE.md §1 canonical affiliation 名に揃えよ"
             if _org_name196 else
             "Check 196: JSON-LD Organization (nkgr.co.jp) block / name 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 196: index.html present",
              "Check 196: index.html が無い", blocking=True)

    # ── 197. JSON-LD Organization (nkgr.co.jp) url = https://nkgr.co.jp/ (BLOCKING) ─
    # index.html 静的 JSON-LD の Organization block (Check 196 と同 block) の `url`
    # property が "https://nkgr.co.jp/" (CLAUDE.md §1 canonical Organization URL) と
    # 一致することを BLOCKING 強制。drift は SILENT に AI/social crawler を別 home
    # へ誘導し employee→employer URL 解決を破壊。Check 196 (name 軸) の URL 軸版。
    _idx197 = ROOT / "index.html"
    if _idx197.exists():
        _isrc197 = _idx197.read_text(encoding="utf-8")
        # locate the canonical nkgr Organization block: @type=Organization + @id=
        # nkgr.co.jp/#organization + has both name and url (not the worksFor stub
        # which only has @id reference). Use Check 196's pattern (4-line block
        # signature) to anchor on the full block.
        _org197_m = re.search(
            r'"@id":\s*"https://nkgr\.co\.jp/#organization",\s*\n\s*"name":\s*"株式会社日本経営"',
            _isrc197,
        )
        _org_url197 = None
        if _org197_m:
            _scope = _isrc197[_org197_m.start():_org197_m.start() + 800]
            _u = re.search(r'"url":\s*"([^"]+)"', _scope)
            if _u:
                _org_url197 = _u.group(1)
        _expected197 = "https://nkgr.co.jp/"
        _ok197 = _org_url197 == _expected197
        check(
            _ok197,
            f"Check 197: JSON-LD Organization (nkgr.co.jp).url = {_expected197!r}",
            (f"Check 197: JSON-LD Organization (nkgr.co.jp).url = {_org_url197!r} ≠ "
             f"{_expected197!r} — AI/social crawler が別 Organization home へ誘導。"
             "CLAUDE.md §1 canonical Organization URL に揃えよ"
             if _org_url197 else
             "Check 197: JSON-LD Organization (nkgr.co.jp) url 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 197: index.html present",
              "Check 197: index.html が無い", blocking=True)

    # ── 198. JSON-LD Person jobTitle contains canonical role markers (BLOCKING) ───
    # index.html 静的 JSON-LD の primary Person block の `jobTitle` string が
    # CLAUDE.md §1 canonical role markers ("IT Consultant" + "KERNEL Framework
    # Designer") を共に含むことを BLOCKING 強制。drift は SILENT に AI/search-engine
    # entity panel 上の professional role 宣言を弱体化。Check 169 (manifest entity.role)
    # の JSON-LD Person.jobTitle 軸版。
    _idx198 = ROOT / "index.html"
    if _idx198.exists():
        _isrc198 = _idx198.read_text(encoding="utf-8")
        # locate primary Person block by `"@type": "Person"` then look for jobTitle
        # within scope (Person block can be ~3KB; jobTitle is sibling-indent).
        _person198_m = re.search(r'"@type":\s*"Person"', _isrc198)
        _jobtitle198 = None
        if _person198_m:
            _line_start = _isrc198.rfind("\n", 0, _person198_m.start()) + 1
            _indent = _isrc198[_line_start:_person198_m.start()]
            # find next "@type": (next entity boundary)
            _all_types = [m.start() for m in re.finditer(r'"@type":', _isrc198)]
            _next = next((p for p in _all_types if p > _person198_m.start()), len(_isrc198))
            _scope = _isrc198[_person198_m.start():_next]
            _jt = re.search(
                r'\n' + re.escape(_indent) + r'"jobTitle":\s*"([^"]+)"', _scope
            )
            if _jt:
                _jobtitle198 = _jt.group(1)
        _required198 = ["IT Consultant", "KERNEL Framework Designer"]
        _missing198 = [m for m in _required198 if _jobtitle198 and m not in _jobtitle198] if _jobtitle198 else _required198
        _ok198 = _jobtitle198 is not None and not _missing198
        check(
            _ok198,
            f"Check 198: primary Person.jobTitle が canonical role markers {_required198} を網羅",
            (f"Check 198: primary Person.jobTitle に必須 marker {_missing198} 欠落 "
             f"(現 jobTitle={_jobtitle198!r}) — AI/search entity panel の role 宣言を弱体化。"
             "CLAUDE.md §1 canonical role markers を jobTitle に含めよ"
             if _jobtitle198 else
             "Check 198: primary Person.jobTitle 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 198: index.html present",
              "Check 198: index.html が無い", blocking=True)

    # ── 199. JSON-LD Person knowsAbout contains technical anchors (BLOCKING) ──────
    # index.html 静的 JSON-LD の primary Person block の `knowsAbout` array が
    # unique 技術 positioning anchor ("KERNEL Framework" + "Vanilla JavaScript SPA")
    # を共に含むことを BLOCKING 強制。drift は SILENT に AI search discovery
    # (KERNEL Framework / Vanilla JavaScript SPA AI query) を弱体化。knowsAbout は
    # Knowledge Panel topics と expert-finder system の feed source。
    _idx199 = ROOT / "index.html"
    if _idx199.exists():
        _isrc199 = _idx199.read_text(encoding="utf-8")
        _person199_m = re.search(r'"@type":\s*"Person"', _isrc199)
        _know_topics199 = []
        if _person199_m:
            _line_start = _isrc199.rfind("\n", 0, _person199_m.start()) + 1
            _indent = _isrc199[_line_start:_person199_m.start()]
            # scope to the NEXT primary Person block (not nested @type entries
            # like Article sameAs items which share the Person block scope).
            _all_persons = [m.start() for m in re.finditer(r'"@type":\s*"Person"', _isrc199)]
            _next = next((p for p in _all_persons if p > _person199_m.start()), len(_isrc199))
            _scope = _isrc199[_person199_m.start():_next]
            # knowsAbout array starts at sibling indent and contains string entries
            _kw = re.search(
                r'\n' + re.escape(_indent) + r'"knowsAbout":\s*\[([^\]]*)\]', _scope
            )
            if _kw:
                _know_topics199 = re.findall(r'"([^"]+)"', _kw.group(1))
        _required199 = ["KERNEL Framework", "Vanilla JavaScript SPA"]
        _missing199 = [t for t in _required199 if t not in _know_topics199]
        _ok199 = len(_know_topics199) > 0 and not _missing199
        check(
            _ok199,
            f"Check 199: primary Person.knowsAbout が technical anchors {_required199} を網羅 "
            f"({len(_know_topics199)} topics)",
            (f"Check 199: primary Person.knowsAbout に必須 anchor {_missing199} 欠落 "
             f"(現 knowsAbout={_know_topics199!r}) — AI search Knowledge Panel での "
             "expert-topic 紐付けが弱体化。canonical 技術 anchor を knowsAbout に含めよ"
             if _know_topics199 else
             "Check 199: primary Person.knowsAbout 抽出不可"),
            blocking=True,
        )
    else:
        check(False, "Check 199: index.html present",
              "Check 199: index.html が無い", blocking=True)

    # ── 200. JSON-LD Person @id derives from canonical URL (BLOCKING) ─────────────
    # index.html 静的 JSON-LD の primary Person block の `@id` が canonical URL +
    # "#person" と一致することを BLOCKING 強制。drift は SILENT に JSON-LD entity
    # graph を分断 (secondary Person references が string-equality で primary @id を
    # 引くため primary だけ drift すると孤立 node を生む)。Check 176 (own-origin
    # canonical prefix) の Person @id 完全一致軸版。
    _idx200 = ROOT / "index.html"
    if _idx200.exists():
        _isrc200 = _idx200.read_text(encoding="utf-8")
        _canon200_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc200
        )
        _canon200 = _canon200_m.group(1) if _canon200_m else None
        _person200_m = re.search(r'"@type":\s*"Person"', _isrc200)
        _person_id200 = None
        if _person200_m:
            # @id should be within ~200 chars after @type for primary Person block
            _scope = _isrc200[_person200_m.start():_person200_m.start() + 400]
            _id = re.search(r'"@id":\s*"([^"]+)"', _scope)
            if _id:
                _person_id200 = _id.group(1)
        _expected200 = (_canon200 + "#person") if _canon200 else None
        _ok200 = (
            _canon200 is not None
            and _person_id200 is not None
            and _person_id200 == _expected200
        )
        check(
            _ok200,
            f"Check 200: primary Person.@id = canonical+#person ({_expected200!r})",
            (f"Check 200: primary Person.@id drift: @id={_person_id200!r} ≠ "
             f"canonical+'#person'={_expected200!r} — JSON-LD entity graph 分断 "
             "(secondary Person references が primary @id を引けない)。"
             "primary Person.@id を canonical URL + '#person' に揃えよ"
             if _person_id200 and _canon200 else
             f"Check 200: canonical URL or primary Person.@id 抽出不可 "
             f"(canonical={_canon200} / Person.@id={_person_id200})"),
            blocking=True,
        )
    else:
        check(False, "Check 200: index.html present",
              "Check 200: index.html が無い", blocking=True)
