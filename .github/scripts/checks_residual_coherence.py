"""
checks_residual_coherence.py — residual project/Speakable/route + theme-color/sitemap/manifest coherence
(extracted from check_repository_consistency.py — check.py split track・category "residual coherence").

Non-contiguous cluster of two small self-contained groups: 146(default-project relatedProjectIds
integrity)/147(Speakable cssSelector → live shipped elements)/148(ARTICLE_ROUTES ⊆ PAGE_META), and
304(theme-color 6-digit hex)/305(theme-color light+dark media)/307(sitemap XML decl + close)/
308(sitemap namespaces)/309(aio-manifest all-URLs HTTPS). Each Check reads its own target files
directly; no global-content or cross-section var coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  146. Default projects' relatedProjectIds are referentially intact: every id listed in a
       defaultProjects entry's relatedProjectIds (store.js) must reference an actually-existing
       default project id. A dangling reference (a typo'd or removed-project id) is SILENT: the
       related-projects UI falls back to autoRelatedCandidates (a similarity score), which quietly
       fills the gap so the section still looks populated — the curator's explicit, intended
       relation is lost with no visible symptom (the graceful-fallback-masks-a-bug class, cf. the
       NotFound/FatalPage vacuous-pass lesson). This Check collects the project-id set (proj() first
       arg) and every pNN id referenced in a relatedProjectIds array literal, asserting no reference
       is dangling (and that some references exist, so it can't pass vacuously). Sibling of Check 141
       (which guards id/slug uniqueness); this guards referential integrity. (BLOCKING)
  147. Speakable cssSelector tokens point to live shipped elements: every #id / .class token in
       js/meta-management.js's SPEAKABLE_SELECTORS literal (the route-keyed AIO wiring that drives
       JSON-LD SpeakableSpecification) must appear as a literal token somewhere in the shipped DOM
       corpus (index.html ∪ js/*.js ∪ main.js, minus meta-management.js itself to avoid self-match).
       A dangling selector (referencing an element that no renderer emits) is SILENT: the
       SpeakableSpecification still ships, but voice assistants find no node and silently fail to
       extract — an AIO precision regression with no console error and no behavior-test signal. This
       is a demonstrated bug-class: the [FIX] history block above SPEAKABLE_SELECTORS (L152-156)
       records hand-removal of dead .hero-tagline / .core-thesis selectors and a .role-split-table
       → #role-split-table correction, never systematized. This Check parses the object literal
       (arrays only, so route keys are not mis-scanned), exempts generic catch-alls (h1 /
       [data-speakable] / .sr-only / .sr-only[data-ai-entity] and attribute-only selectors), and
       asserts each remaining #id/.class token exists in the corpus by word-boundary literal scan.
       Fails vacuously if SPEAKABLE_SELECTORS cannot be extracted or yields zero non-generic tokens
       to check. (BLOCKING)
  148. SITE_CONFIG.ARTICLE_ROUTES ⊆ PAGE_META keys (Article JSON-LD route coherence): every route
       name listed in SITE_CONFIG.ARTICLE_ROUTES (main.js — the routes that get og:type=article and
       an injected Article JSON-LD node) must exist as a top-level key in PAGE_META (js/page-meta.js).
       A dangling ARTICLE_ROUTES entry is SILENT: applyMeta() early-returns when meta is missing,
       leaving fullTitle/desc empty; injectStructuredData() still runs (it does not consult
       PAGE_META) and emits an Article node with empty headline/description — a silently malformed
       AIO surface with no console error and no behavior-test signal (sibling class to Check 147
       dangling Speakable selectors). This Check parses the array literal in main.js, parses
       PAGE_META top-level keys (4-space-indented `key: {` form), and asserts ARTICLE_ROUTES is
       non-empty, PAGE_META is non-empty, and the subset holds. (BLOCKING)
  304. All `<meta name="theme-color">` values are 6-digit hex colors:
       every `<meta name="theme-color">` content in index.html MUST match
       `^#[0-9a-fA-F]{6}$`. Drift = mobile browser chrome color falls
       back to default (loses brand cohesion). Sibling of Check 174
       (theme-color literals in style.css) for the theme-color value-
       format axis. (BLOCKING)

  305. `<meta name="theme-color">` has both light AND dark media
       variants: index.html MUST contain one theme-color for
       `media="(prefers-color-scheme: light)"` AND one for
       `media="(prefers-color-scheme: dark)"`. Drift silently makes
       mobile browser chrome color inconsistent between OS-level
       light/dark modes. Sibling of Check 304 (theme-color hex format)
       for the theme-color media-coverage axis. (BLOCKING)

  307. sitemap.xml opens with XML declaration + closes with `</urlset>`:
       sitemap.xml MUST start with `<?xml version="1.0" encoding="UTF-8"?>`
       and end with `</urlset>` (trailing whitespace allowed). Drift =
       structurally malformed sitemap parses as invalid → crawler drops
       entire sitemap. Sibling of Check 306 (index.html structural
       closure) for the sitemap.xml structural axis. (BLOCKING)

  308. sitemap.xml `<urlset>` declares both sitemap + image namespaces:
       the sitemap.xml `<urlset>` opening tag MUST declare both
       `xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"` AND
       `xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"`.
       Drift = `<image:image>` blocks parsed as unknown → Google Image
       sitemap coverage collapses. Sibling of Check 297 (canonical entry
       image:image) for the sitemap.xml namespace-declaration axis.
       (BLOCKING)

  309. .well-known/aio-manifest.json all URLs use HTTPS: the manifest
       JSON MUST NOT contain any `http://` URL (negative invariant).
       Drift silently downgrades AIO discovery transport security.
       Sibling of Check 232/233/234 (ai:* / asset:* HTTPS) for the
       aio-manifest.json HTTPS axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract

    # ── 146. Default projects' relatedProjectIds are referentially intact (BLOCKING) ─
    # defaultProjects (store.js) の各エントリの relatedProjectIds に列挙される全 id が、実在する
    # default project id を参照することを強制。dangling 参照 (typo / 削除済 project の id) は SILENT:
    # 関連プロジェクト UI は autoRelatedCandidates (類似度スコア) で欠落を埋めるため section は
    # populated に見え、curator の明示的・意図的な関連付けが無症状で失われる (graceful-fallback が
    # bug を masking する class・cf. NotFound/FatalPage の vacuous-pass 教訓)。本 Check は project-id
    # 集合 (proj() 第1引数) と relatedProjectIds 配列リテラル内の全 pNN 参照を収集し、dangling が無い
    # こと (かつ参照が 1 件以上存在し vacuous に pass しないこと) を検証する。Check 141 (id/slug
    # 一意性) の兄弟で、こちらは referential integrity を守る。
    _store146 = ROOT / "js" / "store.js"
    if _store146.exists():
        _src146 = _store146.read_text(encoding="utf-8")
        _ids146 = set(re.findall(r'proj\(\s*"([a-z0-9_]+)"', _src146))
        # relatedProjectIds = pNN のみから成る配列リテラル (store.js で純 pNN 配列は relatedIds のみ)
        _ref146 = set()
        for _arr146 in re.findall(r'\[((?:\s*"p[0-9]+"\s*,?)+)\]', _src146):
            for _r146 in re.findall(r'"(p[0-9]+)"', _arr146):
                _ref146.add(_r146)
        _dangling146 = sorted(_ref146 - _ids146)
        check(
            bool(_ids146) and bool(_ref146) and not _dangling146,
            f"Check 146: defaultProjects の relatedProjectIds は全て実在 project を参照 "
            f"({len(_ids146)} projects, {len(_ref146)} 参照, dangling 0)",
            (f"Check 146: dangling relatedProjectId 検出: {_dangling146} — 実在しない project を "
             "参照している。関連プロジェクト UI は autoRelatedCandidates (類似度 fallback) で欠落を "
             "silent に埋めるため curator の明示的関連付け意図が無言で失われる。store.js の "
             "defaultProjects で参照先 id を修正せよ"
             if _ids146 and _ref146 else
             "Check 146: store.js から project id / relatedProjectIds を抽出できない "
             "(defaultProjects の構造を確認せよ)"),
            blocking=True,
        )
    else:
        check(False, "Check 146: js/store.js present",
              "Check 146: js/store.js が無い — relatedProjectIds 整合性を検証できない", blocking=True)

    # ── 147. Speakable cssSelector tokens point to live shipped elements (BLOCKING) ─
    # js/meta-management.js の SPEAKABLE_SELECTORS は AI 音声アシスタント (JSON-LD
    # SpeakableSpecification) が抽出対象とする DOM ノードを route ごとに宣言する AIO 配線。
    # selector が指す要素が shipped DOM に実在しないと、宣言上は speakable でも実際の DOM ノードが
    # 無く抽出が silent に空振りする AIO 精度劣化になる (console error なし・behavior e2e 非検出)。
    # 同ファイル L152-156 の [FIX] コメントが過去の手動修正履歴 (.hero-tagline / .core-thesis を除去 /
    # .role-split-table → #role-split-table) を残す demonstrated bug-class だが、これまで未 systematize
    # だった。本 Check は SPEAKABLE_SELECTORS object literal の各配列内文字列を抽出し、generic
    # catch-all (h1 / [data-speakable] / .sr-only / .sr-only[data-ai-entity] と属性のみセレクタ) を
    # 除く各 #id / .class token が shipped 面 (index.html ∪ js/*.js ∪ main.js のうち
    # meta-management.js 自身を除く) に literal で実在することを BLOCKING 強制する。
    # SPEAKABLE_SELECTORS が空 / 抽出不可 / 非 generic token ゼロ なら vacuous-fail。
    _meta147 = ROOT / "js" / "meta-management.js"
    if _meta147.exists():
        _msrc147 = _meta147.read_text(encoding="utf-8")
        _block147 = re.search(r"const SPEAKABLE_SELECTORS\s*=\s*\{([^}]*)\}", _msrc147)
        _selectors147: list[str] = []
        if _block147:
            # block 内の全 quoted string を拾う (route 名 key も含むが、_m147 regex が #/. 始まりだけ通すので
            # 'home' 等の key は自然に skip される — `\[...\]` で囲もうとすると `[data-speakable]` 内の `]`
            # で早期終了し silent に末尾 selector を取りこぼす real footgun を回避する)
            for _sel147 in re.findall(r"['\"]([^'\"]+)['\"]", _block147.group(1)):
                _selectors147.append(_sel147)
        # generic catch-all — どんな well-formed page でも常に matche する想定で exempt
        _generic147 = {"h1", "[data-speakable]", ".sr-only", ".sr-only[data-ai-entity]"}
        # shipped 面 corpus を構築 (self-match を避けるため meta-management.js は除く)
        _corpus147_paths: list[Path] = [ROOT / "index.html", ROOT / "main.js"]
        _corpus147_paths += sorted((ROOT / "js").glob("*.js"))
        _corpus147 = ""
        for _p147 in _corpus147_paths:
            if _p147.name == "meta-management.js":
                continue
            if _p147.exists():
                _corpus147 += _p147.read_text(encoding="utf-8") + "\n"
        _dangling147: list[str] = []
        _checked147 = 0
        for _sel147 in _selectors147:
            if _sel147 in _generic147:
                continue
            # 属性のみセレクタ ([attr] / [attr=val]) は catch-all 的に扱い exempt
            if _sel147.startswith("["):
                continue
            # 先頭 #id か .class の token を抽出 (.foo.bar や #foo.bar は最初の token のみ評価)
            _m147 = re.match(r"^([#.])([A-Za-z][\w-]*)", _sel147)
            if not _m147:
                # 形式が想定外なら scope 外として skip (false-positive 回避)
                continue
            _token147 = _m147.group(2)
            _checked147 += 1
            # shipped 面に literal で 1 件以上存在するか (word-boundary)
            if not re.search(r"\b" + re.escape(_token147) + r"\b", _corpus147):
                _dangling147.append(_sel147)
        check(
            bool(_selectors147) and _checked147 > 0 and not _dangling147,
            f"Check 147: SPEAKABLE_SELECTORS の全 selector が shipped 面に実在 "
            f"({len(_selectors147)} selectors, {_checked147} non-generic checked, dangling 0)",
            (f"Check 147: dangling Speakable selector: {_dangling147} — 宣言した cssSelector が "
             "shipped DOM (index.html ∪ js/* ∪ main.js) に実在しない。AI 音声アシスタントが "
             "SpeakableSpecification 経由で抽出に失敗し silent に空振りする (console error 無し・"
             "behavior e2e 非検出)。js/meta-management.js の SPEAKABLE_SELECTORS を実在 id/class へ "
             "修正するか dead selector を除去せよ (cf. 同ファイル L152-156 [FIX] history)"
             if _selectors147 and _checked147 > 0 else
             "Check 147: js/meta-management.js から SPEAKABLE_SELECTORS の非 generic token を抽出 "
             "できない (object literal 構造 / generic 集合 を確認せよ)"),
            blocking=True,
        )
    else:
        check(False, "Check 147: js/meta-management.js present",
              "Check 147: js/meta-management.js が無い — Speakable selector 整合性を検証できない",
              blocking=True)

    # ── 148. SITE_CONFIG.ARTICLE_ROUTES ⊆ PAGE_META keys (BLOCKING) ─────────────────
    # SITE_CONFIG.ARTICLE_ROUTES (main.js) は injectStructuredData が「og:type=article かつ
    # Article JSON-LD ノード注入」を適用する route 集合。route 名が PAGE_META (js/page-meta.js)
    # に無いと applyMeta が早期 return し fullTitle/desc が空のまま、injectStructuredData は
    # (PAGE_META を参照せずに) Article JSON-LD を空 headline/description で注入する silent
    # AIO 不整合 (console error 無し・behavior e2e 非検出)。本 Check は ARTICLE_ROUTES の
    # 全 route 名が PAGE_META top-level keys に存在することを BLOCKING 強制し、ARTICLE_ROUTES
    # が空 / 抽出不可 / PAGE_META が空 / dangling >0 なら fail。Check 147 (dangling Speakable
    # selector) の AIO 配線版兄弟。
    _main148 = ROOT / "main.js"
    _meta148 = ROOT / "js" / "page-meta.js"
    if _main148.exists() and _meta148.exists():
        _msrc148 = _main148.read_text(encoding="utf-8")
        _psrc148 = _meta148.read_text(encoding="utf-8")
        _ar148 = re.search(r"ARTICLE_ROUTES:\s*\[([^\]]+)\]", _msrc148)
        _routes148: list[str] = []
        if _ar148:
            _routes148 = re.findall(r"['\"]([^'\"]+)['\"]", _ar148.group(1))
        # PAGE_META top-level key = 4-space indent + (quoted|bare) ident + `:` + `{`
        # 値オブジェクトの内側は 8-space indent なので 4-space 完全一致で top-level だけを拾える。
        _pm_keys148: set[str] = set()
        for _k148 in re.findall(r"^\s{4}'?([A-Za-z][\w-]*)'?:\s*\{", _psrc148, re.MULTILINE):
            _pm_keys148.add(_k148)
        _dangling148 = sorted(r for r in _routes148 if r not in _pm_keys148)
        check(
            bool(_routes148) and bool(_pm_keys148) and not _dangling148,
            f"Check 148: ARTICLE_ROUTES ({_routes148}) すべて PAGE_META keys "
            f"({len(_pm_keys148)} 件) に存在 (Article JSON-LD 整合性)",
            (f"Check 148: dangling ARTICLE_ROUTES: {_dangling148} — PAGE_META に存在しない route 名。"
             "applyMeta は早期 return し fullTitle/desc が空のまま Article JSON-LD が空 headline/"
             "description で silent に注入される。main.js SITE_CONFIG.ARTICLE_ROUTES から dead "
             "route を除去するか js/page-meta.js PAGE_META に対応 entry を追加せよ"
             if _routes148 and _pm_keys148 else
             "Check 148: ARTICLE_ROUTES もしくは PAGE_META keys を抽出できない "
             "(main.js / js/page-meta.js の構造を確認せよ)"),
            blocking=True,
        )
    else:
        check(False, "Check 148: main.js + js/page-meta.js present",
              "Check 148: main.js もしくは js/page-meta.js が無い — ARTICLE_ROUTES 整合性を検証できない",
              blocking=True)

    # ── 304. <meta name=theme-color> content values are 6-digit hex (BLOCKING) ────
    # index.html の全 `<meta name="theme-color">` content が `^#[0-9a-fA-F]{6}$`
    # regex に一致することを BLOCKING 強制。Check 174 (style.css literal) の
    # value-format 軸版。
    _idx304 = ROOT / "index.html"
    if _idx304.exists():
        _isrc304 = _idx304.read_text(encoding="utf-8")
        _tc_vals304 = re.findall(
            r'<meta\s+name=["\']theme-color["\'][^>]*content=["\']([^"\']+)["\']',
            _isrc304,
        )
        _bad304 = [v for v in _tc_vals304 if not re.match(r"^#[0-9a-fA-F]{6}$", v)]
        _ok304 = len(_tc_vals304) > 0 and not _bad304
        check(
            _ok304,
            f"Check 304: <meta name=theme-color> {len(_tc_vals304)} 件全て 6-digit hex",
            (f"Check 304: 非 hex theme-color: {_bad304!r} — mobile browser chrome color "
             "が default fallback。#XXXXXX 形式へ揃えよ"
             if _bad304 else
             "Check 304: <meta name=theme-color> 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 304: index.html present",
              "Check 304: index.html が無い", blocking=True)

    # ── 305. <meta name=theme-color> covers both light + dark media (BLOCKING) ────
    # index.html に `<meta name=theme-color media="(prefers-color-scheme: light)">`
    # AND `<meta name=theme-color media="(prefers-color-scheme: dark)">` 両方が
    # 存在することを BLOCKING 強制。Check 304 の media-coverage 軸版。
    _idx305 = ROOT / "index.html"
    if _idx305.exists():
        _isrc305 = _idx305.read_text(encoding="utf-8")
        _tc_light305 = re.search(
            r'<meta\s+name=["\']theme-color["\'][^>]*media=["\']\(prefers-color-scheme:\s*light\)["\']',
            _isrc305,
        )
        _tc_dark305 = re.search(
            r'<meta\s+name=["\']theme-color["\'][^>]*media=["\']\(prefers-color-scheme:\s*dark\)["\']',
            _isrc305,
        )
        _missing305 = []
        if not _tc_light305:
            _missing305.append("theme-color for light media")
        if not _tc_dark305:
            _missing305.append("theme-color for dark media")
        _ok305 = not _missing305
        check(
            _ok305,
            f"Check 305: theme-color has both light + dark media variants",
            (f"Check 305: 欠落: {_missing305!r} — mobile browser chrome color が "
             "OS-level light/dark mode 遷移で inconsistent。両 media variant を追加"),
            blocking=True,
        )
    else:
        check(False, "Check 305: index.html present",
              "Check 305: index.html が無い", blocking=True)

    # ── 307. sitemap.xml opens with XML decl + closes with </urlset> (BLOCKING) ───
    # sitemap.xml が `<?xml version="1.0" encoding="UTF-8"?>` で始まり `</urlset>`
    # で終わることを BLOCKING 強制。Check 306 (index.html structural closure) の
    # sitemap.xml structural axis 版。
    _sitemap307 = ROOT / "sitemap.xml"
    if _sitemap307.exists():
        _ssrc307 = _sitemap307.read_text(encoding="utf-8")
        _bad307: list[str] = []
        if not _ssrc307.lstrip().startswith('<?xml version="1.0" encoding="UTF-8"?>'):
            _bad307.append("XML declaration 欠落/drift")
        if not _ssrc307.rstrip().endswith("</urlset>"):
            _bad307.append("</urlset> closing 欠落")
        _ok307 = not _bad307
        check(
            _ok307,
            "Check 307: sitemap.xml opens with XML decl + closes with </urlset>",
            (f"Check 307: 違反: {_bad307!r} — sitemap.xml structural malformation。"
             "crawler 全 sitemap drop リスク"),
            blocking=True,
        )
    else:
        check(False, "Check 307: sitemap.xml present",
              "Check 307: sitemap.xml が無い", blocking=True)

    # ── 308. sitemap.xml <urlset> declares both namespaces (BLOCKING) ─────────────
    # sitemap.xml の <urlset> tag が sitemap + image 両方の xmlns 宣言を含むことを
    # BLOCKING 強制。Check 297 (canonical entry <image:image>) の namespace 軸版。
    _sitemap308 = ROOT / "sitemap.xml"
    if _sitemap308.exists():
        _ssrc308 = _sitemap308.read_text(encoding="utf-8")
        _required_ns308 = [
            ('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', "sitemap 0.9"),
            ('xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"', "image 1.1"),
        ]
        _urlset308_m = re.search(r"<urlset\s+[^>]*>", _ssrc308, flags=re.DOTALL)
        _urlset308 = _urlset308_m.group(0) if _urlset308_m else ""
        _missing308 = [_label for _pat, _label in _required_ns308 if _pat not in _urlset308]
        _ok308 = not _missing308 and bool(_urlset308_m)
        check(
            _ok308,
            f"Check 308: sitemap.xml <urlset> declares both sitemap + image namespaces",
            (f"Check 308: 欠落 xmlns: {_missing308!r} — <image:image> block が unknown "
             "parse で Google Image sitemap coverage 崩壊"),
            blocking=True,
        )
    else:
        check(False, "Check 308: sitemap.xml present",
              "Check 308: sitemap.xml が無い", blocking=True)

    # ── 309. aio-manifest.json all URLs HTTPS (BLOCKING) ──────────────────────────
    # .well-known/aio-manifest.json に `http://` URL が 0 であることを BLOCKING 強制
    # (negative invariant)。Check 232/233/234 の aio-manifest.json HTTPS 軸版。
    _mani309 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani309.exists():
        _msrc309 = _mani309.read_text(encoding="utf-8")
        _http_urls309 = re.findall(r'"(http://[^"]+)"', _msrc309)
        _ok309 = len(_http_urls309) == 0
        check(
            _ok309,
            "Check 309: aio-manifest.json に http:// URL 不在 (HTTPS-only)",
            (f"Check 309: aio-manifest.json に http:// URL: {_http_urls309!r} — "
             "AIO discovery transport が insecure に downgrade。全 URL を https:// へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 309: aio-manifest.json present",
              "Check 309: aio-manifest.json が無い", blocking=True)
